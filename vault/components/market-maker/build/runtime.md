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

## The tick (1 s, `loop.py`)

In order, every second:

1. **Due polls** (the pull path; empty in live-after-switch).
2. **Drain bus readings** — each through the full pipeline (accept →
   journal → engines → sync). The observation stamp is taken from each
   message's `Fetched-At` (its envelope `receive_time`) **before and
   regardless of the accept verdict** — a §7.3 duplicate IS the
   publisher's deliberate liveness confirmation.
3. **Drain venue answers** to empty — a fill the machine has not
   consumed means quoting inventory it no longer holds; a drained fill
   can move the book within the same tick.
4. **Daily discovery** if due (first tick runs it immediately; the
   composition owns the wall-clock→monotonic conversion at the edge;
   `ensure_game` is idempotent and re-stamps moved kickoffs).
5. **The sweep** if due.

The beat is deliberately NOT in this list any more — the poller lost it
(and its transport) to the beat task above. After the tick, `run()`
**flushes the readings' batched acks** — pop → journal → ack, the
crash-safety order — and writes a **§10.3 checkpoint when due** (hourly,
at the tick boundary — the state is quiescent because the tick is
synchronous). One tick never overlaps the next; a slow tick shortens
the following wait instead of drifting.

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
- **live** — **REFUSES to start and names its gates**: the S1/S7
  entitlement · the go-live ingestion switch (the live wiring consumes
  the bus; the poller keeps only the heartbeat) · N19 (Edwin's file
  delivery). Synthetic prices must never reach a real venue (§2.3), so
  the gate is a raise, not a warning.

The entrypoint: fail-fast NATS connect, the boot order above, one log
line per tick (`polled/accepted/dup/drained/readings/swept/cycles` +
loud REJECTED/CONFLICT/MISSED counts), SIGINT/SIGTERM → clean shutdown.

## What changes here next

[[market-maker/build/next|Next]]: the go-live switch (this page's live
mode) · the boot-reconcile healer · N31 group commit (the journal's
fsync ceiling) · N15's window retune after the VM jitter measurement.
~~§10.3 checkpoints~~ built 06-08d, equality-proven.
