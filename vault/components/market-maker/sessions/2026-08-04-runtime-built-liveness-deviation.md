# 2026-08-04/05 — the runtime is built · a quiet game is not a dead feed

> **Who:** George + Claude
> **Type:** build session (spanning 04-08 → 05-08)
> **Refs:** `inplay-market-maker` commits `2eaa27b` (N28 sweep event) ·
> `cd6cf21` (mm/runtime/) · `de33ebb` + `6a79c9f` + `48b648d` (the
> liveness deviation, corrected twice) · **443 → 474 tests**, ruff +
> `mypy --strict` clean throughout

## What we did

1. **N28 built — the §3.1.4 sweep is an event** (`VALUATION_SWEEP`, the
   tenth type). The scheduler is a producer beside the poller; the
   engines stay clock-free; replay consumes the emitted sweeps.
   Idempotency key = the scheduled instant alone — a late sweep is still
   the sweep that was due then. `missed_intervals` is stamped by the
   producer and now feeds §3.4/§3.5, which were wired but never fed.
2. **`mm/runtime/` built** — the loop that owns the clocks, in ONE file
   (`runtime/loop.py`). A 1 s tick: beat first (inside the poller, so a
   slow source can never delay the dead-man), drain, due polls, due
   sweep. `SweepScheduler` keeps fixed slots (no drift), emits ONE sweep
   after a stall carrying the missed count (never a backlog), and owes
   nothing on its first call. `boot()` replays the journal; the boot
   order and the 30 s grace constraint are recorded in `[boot]`.
3. **The liveness deviation built end to end** — see below. The sweep
   carries an `observations` map (game → last successful fetch time);
   the orchestrator feeds it into the §3.4 status; §3.3.1's live bands
   now run on OBSERVATION age wherever the signal exists.

## The deviation, stated clearly (final form, 05-08)

**The rule: a successful fetch confirms the number. Only silence from
the source suspends the book.**

- Sportradar sends no heartbeat. Its `last_updated` advances only when
  the probability MOVES (98 % of timeline entries change the number).
  So the age of the reading cannot distinguish a quiet game from a dead
  feed.
- Measured on the real Chiefs–Ravens game (1,089 readings): gaps between
  updates run median 4 s · mean 16.3 s · p90 28 s · **max 2,862 s — the
  whole of halftime**. §3.3.1 as written (reading older than 20 s →
  Invalid → suspend) therefore suspends every book for all of halftime
  and on ~one update in six of a healthy live game.
- **The fix: run the live staleness bands on OBSERVATION age** — the
  time since our last SUCCESSFUL fetch — not on reading age:

  | Fetches | Condition | Book |
  |---|---|---|
  | Landing every ~2 s (halftime included) | CURRENT | **Full status, full confidence** |
  | Failing 5–10 s | WARNING | Quoting |
  | Failing 10–20 s | DEGRADED | Quoting, discounted |
  | Silent 20 s | INVALID | **Suspends** |

- The band VALUES (5/10/20 s) are untouched and remain Edwin's. They now
  measure the fact that actually indicates feed health.
- **It took two corrections from George to get here.** First cut: rescue
  the suspend but mark the book Degraded — wrong, because a confirmed
  number is not a weaker form of fresh. Final form: a confirmed number is
  CURRENT. Nothing is discounted while the source answers.
- Deliberate residues: **pregame stays on reading age** (the poller may
  not poll outside the pre-kickoff window; a frozen observation stamp
  would mis-suspend a healthy overnight book) · **no observation ever →
  the spec's original rule unchanged**, so nothing regresses before the
  producer runs live · the `condition_status` rescue (Invalid +
  confirmed-live → Degraded) stays as a defensive backstop only.
- Code markers: `[quiet-is-not-dead]` + `[invalid-cost]`
  (`freshness.py`) · `[liveness]` + `[observation-age]`
  (`orchestration/engine.py`) · `[observations]` (`runtime/loop.py`).

## What we learned

- ⭐ **The sweep is PORTFOLIO-WIDE, not per-security** (§3.1.4 + §2.5:
  "complete recalculation of the full universe each sweep"). Corrects
  the 03-08 note. One event per 2.0 s slot covers all 170 securities —
  0.5 events/s, not the feared 85 — so the emit-on-effect volume control
  is unnecessary and was dropped.
- **Why the fetch time cannot ride the probability key (pull path):** the
  poller re-fetches the WHOLE timeline every ~2 s and relies on §7.3
  dedup to discard the readings it already has. A fetch-time component in
  the key would re-mint the entire game history as new facts on every
  poll; a fetch-time in the payload alone would raise a CONFLICT alarm
  every 2 s (same key, different hash). Hence: feed health rides the
  sweep. **When the SR-service push path exists, its per-publish messages
  CAN carry the fetch stamp in their own key** — one stamp per publish,
  redeliveries share it — exactly George's design, in its right home.
- **The Sportradar upstream belongs to `inplay-sportradar-service`** —
  "the single owner of the SR upstream… do NOT poll from the app" (its
  own docs). The MM should consume from it, not own a second SR key.
  Its cache TTL and raw-vs-normalised shape are open asks; its win-prob
  worker is blocked on the same S1/S7 entitlement we are.
- **Capacity, measured (04-08):** a full engine pass over 70 hot
  securities takes **6.3 ms** — the earlier ~140 ms estimate was 22×
  pessimistic; 200 ms capability uses ~3 % of budget on compute. The
  Mac journal figure (35k fsync/s) is INVALID (macOS `fsync` does not
  flush the drive cache) — **N31 stays unmeasured until the real VM.**
- A fresh security starts DEGRADED and climbs (§3.4.1's ratchet) — so
  end-to-end threshold assertions belong on `raw_status`, not on the
  tracker.

## What went wrong

- Two false starts on the deviation, both corrected by George pushing
  back: "Degraded while confirmed" (fixed 05-08) and my earlier claim
  that reading time and `last_updated` were different fields (they are
  the same field; the adapter always used `last_updated`).
- The 03-08 sweep design note said "emit on effect, not on tick" and
  "85 events/s" — both artifacts of the per-security misreading, both
  dead. The vault rows are corrected this session.

## Decisions *(mirrored into decisions.md 04-08 / 05-08)*

The 200 ms republish is a CAPABILITY requirement (George + Edwin) ·
Python-then-Go parked, everything built in Python ($E25's date makes the
port not-now) · no new database — bucket + journal cover the engine ·
Cloud NAT exists · secrets via Terraform · the observation-age deviation
above (ours to build, Edwin's to bless via E38) · the liveness window =
20 s, deliberately §3.3.1's Invalid bound.

## Questions opened/closed

- **E38 opened** — halftime intent + the band values, with the
  measurement attached.
- **N31 opened** — group commit; unmeasured until the VM.
- **N7 · N29 resolved earlier this thread** (own VM · the trading admin
  panel). **N30 open** (real VPC layout, for Hasan).

## Next

1. **Tiered polling** — the poller still runs ONE interval for every
   game; the LIVE / PRE_KICKOFF / POST / OVERNIGHT tiers from the
   03-08 addendum are not wired. Needs the pre-kickoff number (🔴).
2. **The liveness producer goes live only with the live HTTP source** —
   `games_polled` already feeds it; the HTTP source itself is S1/S7.
3. **§10.3 checkpoints** — promoted to required (every deploy is a
   restart); its own session.
4. **Send the Edwin round** — now E29–E38 plus N23/N28.
5. **The composition script** (`main.py`: transport → boot → reconcile →
   run) — the wire test is the prototype; small once tiering lands.
