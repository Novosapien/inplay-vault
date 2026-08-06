# Build — Runtime

> Part of [[market-maker/build/index|As Built]] · Code: `mm/runtime/`
> (`loop.py` · `compose.py` · `__main__.py`) · Spec: §3.1.4 · N28.

The only code that reads a clock. Everything else reacts to events —
which is why the sweep is an event and not a method call.

## The tick (1 s, `loop.py`)

In order, every second:

1. **Beat** — FIRST, inside the poller's `run_once`, before any work: the
   gateway's 4 s dead-man is counting, and a slow source must never
   delay the heartbeat. One beat per tick tolerates three missed ticks.
2. **Due polls** (the pull path; empty in live-after-switch).
3. **Drain bus readings** — each through the full pipeline (accept →
   journal → engines → sync). The observation stamp is taken from each
   message's `Fetched-At` (its envelope `receive_time`) **before and
   regardless of the accept verdict** — a §7.3 duplicate IS the
   publisher's deliberate liveness confirmation.
4. **Drain venue answers** to empty — a fill the machine has not
   consumed means quoting inventory it no longer holds; a drained fill
   can move the book within the same tick.
5. **Daily discovery** if due (first tick runs it immediately; the
   composition owns the wall-clock→monotonic conversion at the edge;
   `ensure_game` is idempotent and re-stamps moved kickoffs).
6. **The sweep** if due.

After the tick, `run()` **flushes the readings' batched acks** — pop →
journal → ack, the crash-safety order. One tick never overlaps the next;
a slow tick shortens the following wait instead of drifting.

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
    2 beat            — the dead-man is already counting
    3 replay the journal — rebuild all memory (synchronous)
    4 reconcile against the venue's real book
    5 tick

Step 3 runs inside the gateway's **30 s boot grace**, and the journal
grows all season — which is exactly why **§10.3 checkpoints are REQUIRED
before the season** (every deploy is a restart). Until then, boot time
is a number to watch. ⚠ The restart drill demonstrated the
boot-reconcile gap live: dead-man-swept levels survive in the replayed
record because their sweep events published into our absence — parked
with eyes open (the §3.1.4 healer + an ICD snapshot are the fixes).

## The composition (`compose.py` + `python -m mm.runtime`)

Every construction decision in ONE file: the universe, the journal path,
the clock conversions, both drains, the readings wiring
(queue → `ReadingInbound` + `PendingAcks` → the runtime), the durable
consumer bind. Two modes:

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
mode) · §10.3 checkpoints · the boot-reconcile healer · N31 group commit
(the journal's fsync ceiling).
