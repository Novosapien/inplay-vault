---
description: "The as-built runtime page — the tick and its bounded drains, the beat task, the sweep scheduler, the session clock, checkpoints, boot and composition"
---

# Build — Runtime

> Part of [[market-maker/build/index|As Built]] · Code: `mm/runtime/`
> (`loop.py` · `compose.py` · `__main__.py`) · Spec: §3.1.4 · N28.

The only code that reads a clock. Everything else reacts to events —
which is why the sweep is an event and not a method call.

## The beat (~250 ms, its own task — 06-08d)

The heartbeat is `run()`'s own asyncio task at `heartbeat_interval_s`
(0.25 s, the dictionary), independent of the tick's work — N15's
position and Hasan's guide agree: tick-tied, a tick that stalled 4 s
would go silent past the dead-man window and cost the whole book. A
dead beat task stops the run LOUDLY (a bot that cannot beat is already
swept). ⚠ The honest limit, recorded in `[beat-task]`: asyncio does not
preempt, so a synchronously blocking tick still starves the beat — that
is exactly what the VM jitter measurement watches before the window
tightens to ~1–1.5 s (the beat and the window move together).

⭐ **Progress-aware since 08-13 (always-quoting step 3, MM PR #27):**
the beat certifies "ticks are completing", never "the event loop is
idle". `run()` stamps a progress anchor when a tick completes and its
batch commits; the beat task WITHHOLDS the heartbeat once the anchor
ages past `heartbeat_stall_threshold_s` (5 s, the dictionary). A loop
that is alive but not advancing — a hung ack flush, a stuck await —
goes silent, and the dead-man pulls the book ~threshold + 4 s after
the wedge instead of never. Withhold/resume transitions log loudly
(`HEARTBEAT WITHHELD` / `RESUMED`) — `[progress-beat]`.

## The tick (1 s, `loop.py`)

In order, every second:

1. **Due polls** (the pull path; empty in live-after-switch).
2. **Drain bus readings** — each through the full pipeline (accept →
   journal → engines → sync). The observation stamp is taken from each
   message's `Fetched-At` (its envelope `receive_time`) **before and
   regardless of the accept verdict** — a §7.3 duplicate IS the
   publisher's deliberate liveness confirmation.
3. **Drain venue answers** — a fill the machine has not consumed means
   quoting inventory it no longer holds; a drained fill can move the
   book within the same tick.
   ⭐ **Both drains are BOUNDED since 08-13** (always-quoting step 1,
   MM PR #25): each stops at its per-tick cap
   (`drain_max_readings_per_tick` 256 · `drain_max_venue_per_tick` 512,
   the dictionary) and the leftover waits one tick. A flooded queue
   defers quotes by ticks instead of starving the heartbeat into a
   dead-man sweep — the 08-12 storm's exact path. A capped tick shouts
   `DRAIN_CAPPED` in the log line; unacked readings past the cap follow
   the `[ack-flush]` rules (deferred, never lost). Reasoning:
   `[drain-cap]` in `loop.py`.
4. **Daily discovery** if due (first tick runs it immediately; the
   composition owns the wall-clock→monotonic conversion at the edge;
   `ensure_game` is idempotent and re-stamps moved kickoffs).
5. **The sweep** if due.

The beat is deliberately NOT in this list any more — the poller lost it
(and its transport) to the beat task above. After the tick, `run()`
runs **the N31 group commit** (⭐ 08-13, MM PR #26) — ONE fsync makes
the whole tick's journal lines durable, before any await, so nothing
the tick produced can leave the process first — then **flushes the
readings' batched acks** — pop → commit → ack, the crash-safety
order — and writes a **§10.3 checkpoint when due** (hourly, at the
tick boundary — the state is quiescent because the tick is
synchronous). One tick never overlaps the next; a slow tick shortens
the following wait instead of drifting. The fsync ceiling this removes
and the crash analysis live on
[[market-maker/build/event-core|Event core]].

## Markets are independently failable (06-08d)

One security's engine fault must not cost the other 169 books (George).
The boundary is the orchestrator's per-security cycle
(`[quarantine]` in `orchestration/engine.py`): on a fault the security
is QUARANTINED — its outcome becomes `BookSuspended("quarantined: …")`,
the sync driver's existing suspension sweep cancels its resting book,
and later events repeat the suspended outcome WITHOUT re-running its
engines. Replay-safe with no new event type: engines are pure functions
of the event stream, so the same events reproduce the same fault and
the same quarantine. Deliberate boundaries both ways: event ingestion
and the transport stay FATAL (a wire fault must kill the process so the
dead-man sweeps). The tick reports a cumulative count; the log line
shouts `QUARANTINED=n`.

## The sweep (§3.1.4, N28)

`VALUATION_SWEEP` — the tenth event type, minted by a PRODUCER
(`SweepScheduler`) because the engines read no clock: a clock-driven
method call would have no legal `at` and would diverge on replay. Replay
consumes the emitted sweeps and never re-runs the scheduler.

- **Portfolio-wide**: ONE event per 2.0 s slot covers all 170 (§3.1.4 +
  §2.5 — 0.5 events/s, not 85).
- **Fixed slots**: a late tick catches up to the wall clock rather than
  drifting; a late sweep keeps its slot's identity (the key is the
  scheduled instant alone).
- **A stall emits ONE sweep carrying the missed count** — never a
  backlog (§3.1.4's own wording; a backlog would recompute identical
  universes and publish nothing per §3.1.5). The first call anchors and
  owes nothing.
- **The sweep carries the `observations` map** (game → last successful
  fetch stamp, sorted for hash stability): feed health, journalled, so
  replay reproduces the SAME suspensions. This is the producer half of
  the E38 observation-age design.
- The sweep is what §3.1.4's thresholds reach §3.4 status and §3.5
  confidence through — and it lets quiet books climb the promotion
  ratchet without waiting for a reading.

## Boot (`[boot]`)

    1 connect the transport
    2 beat once       — the dead-man is already counting; the beat task
                        takes over when the loop starts
    3 replay the journal — rebuild all memory (synchronous)
    4 reconcile against the venue's real book
    5 tick (run() starts the ~250 ms beat task here)

Step 3 runs inside the gateway's **30 s boot grace**. **§10.3
checkpoints are BUILT (06-08d):** the composition picks the newest
valid checkpoint before constructing the acceptor, `restore()` supplies
the memory, and step 3 replays only the journal TAIL past the
checkpoint's sequence — boot time is bounded to at most one hour of
tail (see [[market-maker/build/event-core|Event core]] for the format,
the guards and the equality proof). No valid checkpoint → full replay,
always correct, only slower; rejected files are printed loudly. ⚠ The restart drill demonstrated the
boot-reconcile gap live: dead-man-swept levels survive in the replayed
record because their sweep events published into our absence — parked
with eyes open (the §3.1.4 healer + an ICD snapshot are the fixes).

## The composition (`compose.py` + `python -m mm.runtime`)

Every construction decision in ONE file: the universe, the journal path,
the clock conversions, both drains, the readings wiring
(queue → `ReadingInbound` + `PendingAcks` → the runtime), the durable
consumer bind — and the WIRE IDENTITY: `Settings` is the one module
that reads env, and `MM_USER_ID` / `MM_BOT_ID` / `MM_VENUE_ACCOUNT`
become the `MMIdentity` every payload carries (the env-vs-dictionary
split, George 06-08b — env answers "who am I", the dictionary answers
"how do I behave"). Two modes:

- **loopback** — the full stack against the docker bench: real gateway
  binary, real NATS/JetStream, **real TEAM_BINDINGS** (a published
  reading routes to its real securities), synthetic T. Proves plumbing,
  boot order, the drains, the sweep and the venue leg — never prices.
  `MM_SECURITIES=IPTCCHIE,IPTCRAVE` names a drill's exact books;
  `MM_LIMIT_SECURITIES=N` caps politely for old rig configs (the real
  governor is 5,000 msg/s — Hasan's guide 05-08).
- **supervised** — the venue-plane test mode (built 07-08, ran the
  same day): ONLY explicitly named books, every number from a reviewed
  inputs file (`MM_SUPERVISED_INPUTS`, exact-set match, every
  violation listed at once), REAL identity required (loopback
  placeholders refuse), the readings leg unwired (no
  `sr.probabilities.>` grants exist; a book with no live game quotes
  from T alone). First production run 07-08: all six QA books
  two-sided at Edwin's sheet prices. `MM_CONFIG_VERSION` names the
  deployment's config version — a re-minting redeploy MUST bump it
  (the venue remembers ClOrdIDs; see
  [[market-maker/build/venue|Venue]]).
- **live** — **REFUSES to start and names its gates**: the S1/S7
  entitlement · the go-live ingestion switch (the live wiring consumes
  the bus; the poller keeps only the heartbeat) · N19 (Edwin's file
  delivery). Synthetic prices must never reach a real venue (§2.3), so
  the gate is a raise, not a warning.

The venue drain is `InboundDrain` (07-08): an untranslatable inbound
message is POISON — counted, logged loudly, skipped — after a real
no-ids fill event killed the engine live; deliberate alarms
(trade busts, unmapped fills) stay fatal. Fills use the subject's
order-id fallback exactly as acks do.

The entrypoint: fail-fast NATS connect, the boot order above, one log
line per tick (`polled/accepted/dup/drained/readings/swept/cycles` +
loud REJECTED/CONFLICT/MISSED counts), SIGINT/SIGTERM → clean shutdown.

## ⭐ The state publisher (`runtime/state_publisher.py`, built 12-08b)

The runtime edge's one observability job (spec R1). The loop supplies a
pulse; the publisher owns the cadence and the projection. Two optional
hooks on `Runtime`, both no-ops when the composition passes nothing:

- **`publish_state`** — called ONCE PER TICK from `run()`, after the
  tick's work and the checkpoint, before the operator's log line. In
  `run()` rather than `tick()` deliberately: `tick()` is the §2.4
  pipeline and nothing observational belongs inside it. Staging after
  the tick means the frame always describes a settled state.
  ⚠ It **STAGES only** — see the split below.
- **`publish_task`** — the publisher's own task, started and cancelled by
  `run()` exactly as the beat's is. It encodes and publishes staged
  frames, off the tick.
- **`on_positions`** — every `PositionRecord` the machine produces, from
  the tick AND from `boot()`'s replay, because the edge accumulates the
  realized-P&L total the position engine deliberately refuses to keep
  (§4.2's no-running-total rule stands; the derived state lives outside
  the engine).

**Two clocks in one.** A SLOT — every 2nd tick, ~1 s at TICK_S 0.5 — and
a FLUSH: this tick, whatever the slot says, on a global kill switch
(either direction), a new quarantine, or a new suspension. Detected by
DIFFING successive reads at the edge, never by a callback out of the
engines — an engine that notified an observer would be an engine with a
side effect. The every-tick diff is deliberately cheap
(`Orchestrator.suspended_books`); the full projection runs only on a
publishing tick.

**Failure is never fatal.** Every fault in the publisher is caught,
counted and logged loudly; none stops the loop. Same reasoning as the
[quarantine] boundary one layer out — a screen must never be able to cost
the book. What this cannot swallow is a dead NATS writer: the heartbeat
rides the same transport at 4× the rate and `run()` turns a dead beat
task into a loud stop, so the wire's death is caught 250 ms later by
design.

**The orchestrator gained read-only accessors only** — `universe`,
`global_kill_switch`, `missed_sweeps`, `suspended_books`, `observe()`.
`observe()` uses `.get()` where the cycle path uses `.setdefault()`,
because a screen looking at a book must not be the thing that gives that
book a market-state tracker.

**⭐ The tick STAGES; a separate task ENCODES and PUBLISHES.** The tick
keeps only what genuinely needs tick consistency — the transition diff
and the projection, which read engine state that moves between ticks.
Building the payload dict, measuring it against the budget and
`json.dumps` are pure functions of an immutable frame (`_Frame`: ints,
strings, Decimals and frozen `VenueOrder`s), so they have no business
holding up the §2.4 pipeline.

⚠ **The caveat that will be misread:** this reduces TICK latency, not
event-loop blocking. asyncio does not preempt, so the encode still blocks
the single loop for the same time — just at a different moment — and the
beat task is starved either way (`[beat-task]` says exactly this about
synchronous work). What the split genuinely buys beyond the number: the
loop's own cadence accounting stops absorbing encode time, and an
unpublished frame can be **superseded** by a newer one. A state snapshot
is worth nothing late; the inline version had no such option. The
`superseded` counter records it.

**Measured (12-08b, 170 books quoting two-sided ladders):** tick ~4.5 ms
→ ~4.9 ms with the publisher on — **+0.32 to +0.46 ms, +7% to +10%**,
which is ~0.98% of the 500 ms tick interval. With the encode inline it
was +1.98 ms (+43.7%). ✂ The spec's original "within 10%" AC was re-cut
to **≤ 10 ms/tick AND ≤ 5% of the tick interval**: a ratio against a
4.5 ms base could not survive one 208 KB `json.dumps`.

**`MM_STATE_PUBLISH=on|off`**, restart-applied, ships ON. The publisher's
tunable numbers — cadence, payload budget, hard ceiling, terminal
retention, the shipped default — live in the **Configuration Dictionary**
(`[ops-publisher]`), per §1.6-5. The taker's `SNTConfig` reads the same
rows rather than restating them, so the two processes cannot drift.

## What changes here next

[[market-maker/build/next|Next]]: the always-quoting build order
(George 08-13 — ~~1. bounded drain~~ built 08-13 · 2. N31 group commit ·
3. progress-aware heartbeat · 4. decoupled quote publication · 5. the
dead-man breaker) · the go-live switch (this page's live mode) · the
boot-reconcile healer · N15's window retune after the VM jitter
measurement. ~~§10.3 checkpoints~~ built 06-08d, equality-proven.

## The session clock and the detached checkpoint (08-12)

Two runtime facts born from the 08-12 incidents (session note:
[[market-maker/sessions/2026-08-12-session-roll-storm]]):

- **The engine knows tZERO's day.** `SessionClock` (a producer beside
  the SweepScheduler) mints one `SESSION_BOUNDARY` event per ET day per
  phase: **close at 23:59:00 ET** — the venue silently expires every
  resting order then, so the engine mirrors it (`expire_all()`: every
  non-terminal venue order → DONE_FOR_DAY, backoff reset) and shuts the
  send gate (`orchestrator.session_open`; the runtime AND the poller
  sync only while it is open); **open at 00:02:00 ET** — the gate lifts
  and the full universe cycles, so the reconciler re-stands every book
  into the venue's Single Price Open. Journalled, idempotent
  (phase + et_date), replay-identical. Boot anchors to now — no
  retroactive boundaries; a boot inside the 3-minute closed window
  posts into rejects until the open (accepted).
- **Checkpoints never block the loop.** `write_checkpoint_detached`
  forks; the child captures (sequence, state) from the frozen
  copy-on-write image and writes at leisure (double-fork, no zombies;
  flock, one writer). The synchronous form remains for fork-less
  platforms and tests. Cause: the hourly write reached 344 MB ≈ 22 s
  and the dead-man swept the book at :01 past every hour. ⚠ State
  growth itself (~70–90 MB/h at the 500 ms/180-book cadence) is a
  standing follow-up: terminal-record pruning.

Checkpoint schema is **5** (state carries `session_open`).
