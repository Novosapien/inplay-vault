---
description: "The session-roll incident: tZERO wiped resting orders at 00:01 ET, 8 hours of phantom-cancel storm + 56 dead-man fires, recovered by clean restart + MD heal — B1 overturned"
---

# 2026-08-12 — the session-roll storm: the venue DOES wipe the book at 00:01 ET

> **Type:** incident + forensics + recovery. George spotted it (thin/one-sided
> depth on many books, mid-morning); Claude ran the diagnosis.
> **State at close:** maker `supervised16` (CFG-0015, journal
> `/var/lib/mm/supervised16/`), **180/180 books two-sided**, quote cache
> fresh on all 180 · taker SNT-CFG-0011 untouched and healthy.

## What George saw

Order-book depth missing or one-sided on many teams. The census agreed:
133/180 two-sided, 22 one-sided, 25 empty in the gateway's quote cache —
most with fresh timestamps (mid-churn snapshots), but CHIE's last MD
update was ~8 h old and EAGL's ~1.7 h.

## What actually happened (two failures, one trigger)

**The trigger: tZERO's session boundary at 23:59/00:01 ET.** The hourly
ack census makes it exact — at 04:00 UTC (00:00 ET) the journal flips
from ~2.4k cancel-rejects/hour to **~61k/hour, sustained for 8 hours**:

1. ⭐ **VENUE FACT — the session roll WIPED our resting orders.**
   ✂ **B1's 08-09 conclusion is OVERTURNED**: that test crossed two
   boundaries with a 6-book, mostly-idle engine and saw nothing; this
   night crossed one with ~750 resting orders and lost them all (no
   DONE_FOR_DAY was sent — the orders just stopped existing venue-side;
   every cancel/replace against them drew `UNKNOWN ORDER`). T14 (is
   there a session roll?) is answered by observation: YES, and it is
   SILENT.
2. **The phantom-cancel storm.** The engine's tracker still believed
   the ~750 orders rested. The reject-backoff capped each phantom at
   60 s, so ~750 phantoms retried forever at ~1/min each ≈ 61k
   rejects/hour. The backoff behaved as designed — the design never
   contemplated the venue forgetting the whole book at once.
3. **The dead-man sweep/repost loop.** The churn starved the ~250 ms
   heartbeat past the 4 s window ~56 times overnight (fire_count
   6 → 62). Each fire: the gateway sweeps everything → the engine sees
   an emptied venue as divergence → reposts → more churn. This is the
   known "cancel_all is a hammer" behaviour, now observed as a LOOP.
4. **Separately: MD subscriptions died at the boundary** for some
   symbols (the MD session re-logs with reset; CHIE's snapshot stream
   never resumed — 8 h stale; EAGL 1.7 h). The engine was fine on
   those books; only the DISPLAY path (LVC → panel) was blind.

## The recovery (11:56–12:03 UTC)

1. Stopped `supervised15`; the dead-man swept the real book
   (open orders 741 → 28 tracker residue).
2. `POST /md/book-resubscribe {}` (with the ops key,
   `inplay-fix-gateway-ops-key` in Secret Manager — the deployed
   gateway now guards mutating endpoints with `X-Ops-Key`):
   **180 resubscribed, 0 failed**.
3. Started `supervised16` (CFG-0015, fresh journal): "book standing:
   1636 instructions for 180 securities".
4. Verified: **180/180 two-sided in the quote cache, zero empty**,
   CHIE fresh, heartbeat silence 220 ms, **zero cancel-rejects** in
   the fresh journal, no new dead-man fires.

## What must change (filed)

- **R-D05 closes properly ENGINE-SIDE: retire an order on
  `UNKNOWN ORDER`.** The gateway already does this (its 08-11 commit
  `005fdd8`); the engine's venue state must do the same — a cancel
  reject with the UNKNOWN reason means the order is GONE: remove it
  from the tracker, let the diff re-post the level. This one change
  kills the phantom storm class. **Top MM build item.**
- **The session boundary is an operating fact**: every resting order
  dies at 00:01 ET, silently. Either the engine expects it (scheduled
  self-sweep + re-stand at the boundary) or T14 asks tZERO to confirm
  the roll semantics on production. Until built: expect one
  self-healing storm per night unless the engine restarts clean after
  00:01 ET.
- **The dead-man sweep/repost loop needs a breaker**: after a sweep,
  the engine should re-stand ONCE deliberately, not fight the gateway
  at churn speed (N15-adjacent design note).
- **MD subscriptions need a boundary heal**: re-run
  `/md/book-resubscribe` after the MD re-logon (gateway-side timer, or
  an ops cron), else stale panel quotes recur nightly.
- B1 and T14 rows updated in the test plan / open questions.

## Addendum (afternoon) — the 01:11 VATH halt re-explained by wire forensics

George pressed on the "lost fill report" — rightly. The FIX wire log
(the ground truth) says otherwise:

- All 26 VATH fills in the snt6 window are journalled 1:1. Nothing
  about any FILL was lost, ever.
- The triggering sell-31 exec carries `9383=4416` on the wire — the
  venue agreed with the taker's journal TO THE SHARE at the halt.
- The loss was the fill's companion `position.>` message (the gateway
  mints two bus messages per exec; the `order.>` one arrived, the
  `position.>` one did not), dropped at the phantom-storm's peak —
  gateway-side publish drop under burst (no slow-consumer events on
  the NATS server all day).
- So the halt was a FALSE POSITIVE on position divergence and a true
  detection of message loss. The taker's unfilled-send tail also
  fully decomposes: ~56 fast-market window misses (CHIE/RAVE at game
  cadence) + 4 venue wash-trade rejects (`Rmo_StopWashTrades` is ON
  for the taker's account — new venue fact) + 0 lost fills.
- ⚠ Two follow-ups: snt8's VATH float carries a +31 error (the
  recovery adopted the stale 4447; true base 4416) — patch at the
  next quiet cutover; and T-S05 should compare the exec's own 9383
  tag instead of the racing position feed (build item, filed in the
  taker requirements).

## Addendum 2 (16:4x) — the EAGL reseed EATEN; the book healed

George flagged EAGL: phantom resting orders 145–147.75 and a
bid-only maker. The morning recon's diagnosis held — the STX reseeder's
10:15Z batch anchors the venue band so high that every real maker ask
rejects as aggressive. Remedy per the 08-07e/08-11 pattern, adapted for
a RUNNING engine: all 16 phantom levels eaten AT their own prices from
the MM account under the scratch `walkops` user id (the engine
subscribes only its own user's subjects — no adoption risk; net
position change zero; ~$3.1k QA spread paid to the phantom
counterparty). **16/16 filled, zero rejects; the maker's ask side
accepted within a minute; the cache shows a real book again
(73.72 × 8,000 / 73.74 × 12,000).** ⚠ Recurs tomorrow ~10:15Z until
Rob disables the seeder (T19) — the eat is a 60-second operation with
`~/eat_eagl.py` on the MM VM (update the LEVELS list from a probe).

## Addendum 3 (17:0x–17:3x) — ⭐ ALL THREE FIXES BUILT AND DEPLOYED (MM PR #24)

George's ruling: no stopgap — fix the actual errors. Built in one
worktree session (`feat/session-boundary`, 698 tests, ruff +
mypy-strict green), deployed by bundle with PR #22's twins merged in,
running as **`supervised17` (CFG-0016, journal
`/var/lib/mm/supervised17/`)**, 180/180 two-sided verified post-stand:

1. **Fork-based checkpoints** (`write_checkpoint_detached`): the hourly
   write happens in a forked child against the frozen copy-on-write
   image — the loop never blocks. Double-fork (no zombies) + flock
   (one writer). The 17:01 stall (344 MB ≈ 22 s ≈ hourly dead-man
   sweep) is dead. ⚠ State GROWTH is only slowed, not fixed — terminal
   -record pruning stays a follow-up; the nightly session clock resets
   practical growth anyway only on restarts, so watch checkpoint sizes.
2. **Gone-retire** (`[gone-retire]`, venue engine): UNKNOWN ORDER /
   ORDER DEAD / ORDER IS DEAD / NOT_CANCELABLE now RETIRE the order
   (✂ supersedes 08-10c's suppress-and-retry for those verdicts). One
   reject instead of thousands; the diff reposts the level.
3. **The session clock** (`SESSION_BOUNDARY`, the eleventh event type):
   close 23:59:00 ET → every venue order expires locally
   (DONE_FOR_DAY) + the send gate shuts (runtime AND poller); open
   00:02:00 ET → gate lifts, the full universe cycles, the book
   re-stands into the Single Price Open. Once per ET day per phase,
   journalled, replay-identical. Checkpoint schema 4 → 5.

**Tonight's 00:01 ET boundary is the live test**: expect
"SESSION close" in supervised17's log at 23:59 ET, a quiet 3 minutes,
"SESSION open" + a full re-stand at 00:02 ET, and ZERO cancel-reject
storm. Still owed (filed): the taker's `fetched_at` staleness fix,
T-S05's compare-source fix, the VATH +31 float patch, venue-state
terminal pruning, and the MD boundary heal (gateway-side).

## Addendum 4 (21:45) — the fork fix PROVEN; ⚠ the taker had been halted 20 h (our miss)

**The checkpoint fix works.** `supervised17` ran 4 h 16 m across THREE
hourly checkpoints (19:28 · 20:29 · 21:29, 138 → 206 → 274 MB) with
**zero dead-man fires** (stuck at 70, last fired 17:28 = the
supervised16 stop sweep) and max MISSED_SWEEPS=2 (was 44 at the
synchronous write). 1.05 M acks, **zero rejects of any kind**, 180/180
two-sided, VM memory steady (1.3 GB used of 8 GB — the COW fork costs
nothing measurable at this state size).
⚠ **Growth is unchanged: ~68 MB/hour.** The stall is cured, the state
size is not — terminal-record pruning stays a real build item (at this
rate a checkpoint passes 1 GB overnight, and `keep=3` triples it).

⚠ **Our miss, recorded honestly: the taker was HALTED for 20 hours**
(01:16 → 21:46 UTC) and this session reported it "running and healthy"
at ~13:00 because it checked `systemctl is-active` and a fill count,
never the halt state — the exact failure MM CLAUDE.md rule 3 warns
about ("a silent bot is often just unresumed"). The halt was the
**predicted +31 VATH error** from the 01:11 false-positive recovery,
caught the moment VATH next traded: `venue=4359 ours=4390
(float=4447)` — the arithmetic matched the prediction to the share.
Recovery: floats recomputed from the RUNNING env + snt8 drift, **VATH
pinned to the venue's own 4359**, SNT-CFG-0012, journal `snt9`. Back
trading immediately: 87 fills in the first 90 s, zero halts; the
maker's executions resumed with it (house-to-house was dead all day).

📝 **Two operating rules earned** (→ MM repo CLAUDE.md next session):
(a) a taker health check MUST read the journal's last control action,
not just the unit state and a fill count; (b) a known float error is
an open incident — patch it at the next quiet moment, never "later",
because T-S05 will halt the bot the moment that book trades.

## Addendum 5 (22:1x) — working memory BOUNDED: pruning built (George: "prune what we don't need, but make sure everything is saved")

**It already is saved — that is what makes pruning safe.** The
**journal** is the permanent record of every event (§7.4), on the
`inplay-market-maker-journal` disk carrying `mm-journal-hourly`:
hourly snapshots, 7-day retention, **verified running** (latest 21:21Z,
all READY). The **checkpoint is only a fast-boot CACHE of working
memory** — pruning it discards nothing, because a full journal replay
rebuilds every pruned order and key and then prunes them identically.
That identity is the design constraint: both prunes read the EVENT's
own time, never a wall clock (asserted by a byte-equality test).

**Where checkpoints live:** `/var/lib/mm/<run>/checkpoints/`, `keep=3`
per run, on the 49 GB journal disk (20% used). ⚠ Old RUN directories
are never cleaned — supervised15 4.4 GB · supervised16 2.2 GB — a
housekeeping item (keep supervised12's journal for C2 and
supervised13's as the empty-book-gate evidence).

**What was growing (measured on supervised17, 4 h, 286 MB state):**

| Component | Size | Count |
|---|---|---|
| `acceptor.seen` | 193 MB (68%) | 1,007,387 keys (7-day window) |
| `venue.orders` | 92 MB (32%) | 492,091 orders — **490,447 (99.7%) terminal** |

**Built (MM PR #24, second commit; 702 tests, ruff + mypy green):**
- **`[terminal-prune]`** — `VenueOrder.terminal_at` stamped from the
  terminal event's time; terminal orders past
  `venue_terminal_retention_s` (**300 s** 🟡 ours) leave working memory.
  The window exists only for stragglers: an ack about a pruned order
  would re-admit an UNKNOWN (which counts as exposure), and the
  gateway's replace-pair gap is ~50 ms — 6,000× margin.
- **`[seen-retention]` scoped per leg** — bus events keep JetStream's
  genuine 7-day redelivery bound; venue acks/executions get **1 hour**
  (`venue_idempotency_retention_s` 🟡 ours) because core NATS is
  at-most-once and cannot redeliver late. Two time-ordered deques;
  `restore()` re-files each key by its §7.3 key prefix.
- Checkpoint **schema 5 → 6** (an unpruned checkpoint must not seed a
  pruning engine — rejected at boot, journal replays).
- Deployed as **`supervised18` (CFG-0017)**; 1,654 instructions stood.
  Expected: the checkpoint tracks the LIVE book (~1,600 orders) instead
  of everything that ever happened. First checkpoint ~1 h in is the
  proof point.

## Addendum 6 (22:2x) — ⚠ MY MISTAKE started a real one: the dead-man sweep/repost LOOP, reproduced

**What I did wrong:** ran the new journal-archive script (gzip of ~6 GB)
**on the trading VM while the engine was live**. gzip pinned the CPU, the
engine's ~250 ms heartbeat starved, and the gateway's dead-man swept the
book. George saw the books clear.

**What it exposed — a genuine defect, not just my error.** The sweep did
not settle when gzip finished. It became **self-sustaining for ~4
minutes / 16 sweeps** (dead-man fires 71 → 87, one every ~15 s):

    dead-man sweeps ~1,650 orders
      → the engine sees an empty venue and reposts the whole book
      → ~1,600 orders become 2,000-3,000 acks to drain
      → one tick spends 5+ s draining them (fsync-bound: N31 measured
        ~579 events/s, so 3,000 events ≈ 5 s)
      → the beat starves past the 4 s window → sweep again

This is exactly the **"dead-man sweep/repost loop needs a breaker"** item
filed in this note's "What must change" and NOT built — now reproduced,
measured, and no longer theoretical. ⭐ It also makes **N31 group commit
the binding constraint in practice**: the recovery burst is fsync-bound,
so any starvation big enough to trigger one sweep can feed itself.

**Recovery:** clean restart as **`supervised19` (CFG-0018)** — 1,666
instructions stood, 180/180 two-sided, zero dead-man fires since,
heartbeat silence ~190 ms.

⚠ **Residue:** ~1,000 orphan orders from supervised17/18 still rest at
the venue under retired config versions, so the current engine will never
cancel them (EAGL probes 17 levels instead of 6, with duplicate prices).
**Tonight's 23:59 ET session close clears them venue-side** — the same
event that tests the new session clock. No action taken deliberately:
a `cancel_all` now would also wipe the fresh book and trigger the very
repost burst described above.

**The archive tool is now safe:** it REFUSES to run while `mm.runtime`
is alive (override `FORCE=1`), and runs under `nice -19 ionice -c3`
otherwise. Archive during the venue's closed window, or from a snapshot
on another box — never against the live tick loop.

## Addendum 7 (22:33–22:41) — the orphans CANCELLED, both bots clean (George's call)

George: "cancel those resting orders — there seemed to be too many." Done
by the 08-11 books-clearing procedure, ordered so nothing could repost
into the clear:

1. **Engine stopped first** (no repost reflex while the book empties).
2. **Taker halted** on the control channel (nothing trades into a
   clearing book).
3. **`gateway.orders.mm.cancel_all`** — the gateway swept every MM order
   its tracker held, orphans from the retired config versions included
   (57,085 cancels sent lifetime; open orders 2,743 → 28).
4. **Verified at the VENUE, not the cache:** EAGL 0 resting levels,
   CHIE 0. ⚠ COWB showed 10 — **not ours**: the STX reseeder's 10:16Z
   ladder (53.30–54.25, 70–150 shares, 2 s spacing) against a real value
   of ~70.46. That is T19's junk, and it does not block our quoting.
5. **Restarted clean:** maker **`supervised20` / CFG-0019** (1,602
   instructions) · taker **SNT-CFG-0013**, journal `snt10`, floats folded
   from snt9 per rule 7. **180/180 two-sided; EAGL probes a textbook
   8-level book (4 bids / 4 asks, no duplicates); heartbeat 188 ms; no
   new dead-man fires.**

📝 The stale-orphan class is a real hazard worth naming: orders minted
under a RETIRED config version are invisible to the new engine (fresh
journal, different id space) and will rest until a sweep or the venue's
session roll. Any restart that does NOT go through cancel_all leaves
them. Either always clear on restart, or let the new session clock's
23:59 ET close do it — but never assume a fresh journal means a clean
venue book.

## Questions opened/closed

- Closed by observation: T14's "is there a session roll" — YES, silent,
  order-wiping. Remaining half: confirm production behaves the same.
- Opened: should the overnight engine simply RESTART itself at
  00:05 ET daily (clean journal, CFG bump) until the boundary handling
  is built?

## Next

1. The engine-side UNKNOWN-ORDER retire (R-D05) — build first.
2. The boundary strategy decision (self-sweep vs nightly restart) —
   George.
3. Watch tonight's boundary: if no fix lands today, expect the storm
   again ~00:01 ET and restart clean in the morning.
