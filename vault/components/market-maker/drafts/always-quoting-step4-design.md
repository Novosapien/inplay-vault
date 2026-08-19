---
description: "Design pass for always-quoting step 4 — decoupled quote publication: target-book staging plus a bounded round-robin converger, for George's review"
---

# Design — always-quoting step 4: decoupled quote publication

> **Status: PROPOSAL, for George's review. Nothing here is built.**
> From the 08-13 ruling, item 4: "quote publication on its own timer
> over the latest consistent state — ingestion lag makes quotes stale,
> never absent." Steps 1–3 are deployed (supervised21/CFG-0020).

## 1 · Why now — the evidence from last night

- `MISSED_SWEEPS` returned on supervised21: **8,197 of ~71k ticks
  (11.5%)** missed a sweep slot. Missed ticks drain **p50 99 / p90 178
  acks** vs 24/88 overall. With the fsync gone (group commit), the
  overrun is pure **engine time on ack bursts**.
- The bursts are **self-inflicted**: a sweep republishes many books in
  one pass (dwell phases align after a boundary re-stand), the venue
  answers in a ~100–200-ack clump, and the clump delays the next sweep.
- At NCAA scale the coupling collapses: ~70 LIVE books at the 500 ms
  redraw ≈ ~2,100 orders/s out → ~1,050 acks **per tick** back —
  permanently over the venue drain cap (512), sweeps permanently late.

## 2 · The load-bearing fact: sync is EDGE-ONLY

`SyncDriver.sync` runs on the live path only. Boot replay
(`orchestrator.replay`) rebuilds engine state and **never re-drives
sync**; the venue's answers are their own journalled events. So WHEN
instructions are sent is an edge concern — **publication timing can
move freely without touching §1.6-4 replay equality.** The
[register-then-send] invariant and the backoff's event-time `at` are
the only two contracts to carry.

## 3 · The design — stage targets, converge on a budget

Two phases, where phase A's data structure IS phase B's:

### Phase A — target-book staging + a bounded converger (in-tick)

1. **Cycles stop sending.** A `Published` cycle STAGES its book as the
   security's **target** (with the triggering event's `at` for the
   backoff). Latest target wins — supersede semantics, exactly the
   state publisher's frame rule: a quote intent is worth nothing late.
   `BookSuspended` stages a sweep-target the same way. `Held` stages
   nothing.
2. **One converger pass per tick, budgeted.** A round-robin cursor
   walks the dirty securities; each is reconciled against venue state
   (the existing `reconcile_book`) and its instructions sent — until
   the pass hits **`converge_max_instructions_per_tick`** (new
   dictionary row, 🔴 until measured). Leftover securities keep their
   targets; the cursor resumes next tick.
3. Register-then-send is untouched (it lives in `_send`). The backoff
   prices from the target's `at`, as today.

What A buys: the outbound side gets what step 1 gave the inbound side —
**no tick fans out an unbounded burst**. Smoothing the outbound smooths
the ack inflow (the waves de-phase through the round-robin), which is
what `MISSED_SWEEPS` is measuring. Tick time becomes bounded in BOTH
directions.

### Phase B — the converger on its own task ("the own timer")

Move the converger pass from tick-end onto its own asyncio task (the
beat-task / publish-task pattern), cadence `converge_interval_s`
(~100–250 ms, 🔴). The tick stages; the task converges.

- **Durability order is preserved for free:** targets derive from
  cycles whose events committed at the END of their tick (group
  commit); the task runs only between ticks, so every instruction it
  sends derives from an already-durable batch.
- **Consistency for free:** asyncio does not preempt — the task reads
  venue state only at await points, never mid-tick.
- **The honest limit:** the task runs no more often than the loop
  yields. Its genuine gains over A: quotes keep converging on ticks
  that have no sweep due, and the seam is clean if convergence ever
  moves off-thread. A first, B as the follow-on — A is the
  risk-reduced path and B is a small diff on top of it.

### What this design also gives a home

- **T2 / the venue rate limit** (`MaxOrdRate`, still unanswered): the
  converger budget is the natural enforcement point — one knob, not
  scattered throttles.
- **Step 5, the dead-man breaker** (paced re-stand after a sweep):
  a re-stand is just "every book dirty at once" — the converger
  already paces it. Step 5 reduces to arming targets + an alarm on the
  second sweep.

## 4 · What this does NOT fix — say it plainly

Pacing bounds starvation; it does not create throughput. If Saturday
needs ~2,100 instructions/s and the engine costs ~0.5–1 ms per ack
event, the engine spends ~1–2 s of every second on acks — no
scheduling fixes that. **The 500 ms (and ruled 200 ms-capable) redraw
at NCAA scale is a THROUGHPUT problem: per-event engine cost.** The
already-owed measurement (the drain-cap re-size) is the same
measurement this design needs for its budget — one instrumented run
sizes both, and tells us whether engine-cost optimization is the real
Saturday gap. Safety (stale-bounded quotes at any load) and speed
(500 ms redraw at 70 books) are different problems; step 4 solves the
first and scopes the second.

## 5 · Numbers this design needs (all rows to parameters.md before build)

| Number | Status | How it's set |
|---|---|---|
| `converge_max_instructions_per_tick` | 🔴 | from the engine-cost measurement; interim proposal ~256 |
| `converge_interval_s` (phase B) | 🔴 | ~100–250 ms; must beat the LIVE redraw floor |
| per-ack engine cost (ms) | 🔴 MEASURE | instrumented counter on supervised21, game-day load |
| target-staleness alarm (a target unconverged > N s) | 🟡 propose 2 s | the converger logs it loudly, like DRAIN_CAPPED |

## 6 · Test plan (sketch)

- Staging: latest target wins; Held stages nothing; a suspension
  stages the sweep.
- Budget honoured; round-robin fairness (no book starves behind a hot
  one); leftover resumes next tick.
- Register-then-send order preserved per instruction; backoff still
  prices from the target's `at` (replay-equal instructions on a fixed
  drive).
- Phase B: instructions only between ticks; a staged target survives a
  tick with no converger slot; the staleness alarm fires.
- The A2 replay drill re-gated end-to-end.

## 7 · Open questions for George

1. Approve the A → B order (or go straight to B)?
2. The 200 ms Saturday capability: hold it as ruled (then the engine
   cost work is IN scope for step 4's follow-up), or restate it as
   500 ms (then the measurement decides whether more is needed)?
3. Build timing: after tonight's games, deploy as CFG-0021 with the
   same cutover runbook?
