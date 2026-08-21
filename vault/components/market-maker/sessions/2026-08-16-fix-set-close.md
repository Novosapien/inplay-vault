---
description: "Session close for the MM Python fix set: what shipped, what it proved live, what is still owed, and the rulings George holds"
---

# 2026-08-15/16 — the Python fix set: built, merged, deployed, proven

> **Who:** Claude (implementation lead, team mode: 2 streams + lead) + George
> **Type:** the `specs/2026-08-14-mm-python-fix-set/` build, end to end
> **Refs:** spec + `progress.md` Drift Log · `reviews/review-002-f5-merge-train.md`
> · `profile-cb1.md` · `profile-cb4-verdict.md` · `gate-v2-results.md` ·
> `scan-sweep.md` · [[market-maker/build-deploy-log]]

## What we did

Built all five fixes (F1–F5), reviewed every one adversarially, merged the
stack to `main`, and deployed it live.

| Fix | State |
|---|---|
| F2 anchors (`ANCHOR_SEED`) | live · **proven across 3 cutovers** |
| F3 marketable guard + refusal path | live · 3,201 refusals, alarms clean |
| F3 ask cap (R-Q08) | on main, **DARK** — needs N43 |
| F4 boot healer | on main, **INERT** — needs `MM_GATEWAY_OPS_URL` |
| F1c prune index | live · the miss-rate cure |
| F5 repo sync | ✅ **AC10 passes**: `main` == running, `src/` byte-identical |

## What it proved

- **AC4 live clause: 92,111 due-sweep ticks, ZERO missed** (bar < 1%).
  On the rig under the corrected v2 workload: 0.0000% at 1× and 10×.
- ⭐ **The anchor chain held across three consecutive live cutovers.**
  33→34 carried 10 anchors; **34→35 carried 12 from a run with NO usable
  checkpoint** ("the whole prior journal is the tail", 4,919 events folded).
  That second hop IS review-002's B1 scenario — the one the reviewer built
  to break it — working in production because the B1 fix put `ANCHOR_SEED`
  into `_ANCHOR_TYPES`.
- **R9/AC9 at rig scale:** 548.5 MB journal, two independent folds,
  byte-identical across 102.9 MB of canonical state.
- **The root cause of the missed sweeps was one function** —
  `_stamp_and_prune` re-scanned every retained dead order on every venue
  event (7,226 µs/call = 98.4% of per-ack cost). Indexed: 6.72 µs, 1,075×.

## What we learned (the transferable half)

1. **The four questions.** Four DIFFERENT order-state sets now exist, and
   each answers a different question: §4.4 "could this cost money" ·
   `_REPLAYABLE_EXPOSURE_STATES` "can a replay rebuild it" · livS "what
   can this pass not reclaim" · the guard's "is it in the book now and not
   already being removed". Reaching for a *nearby* set caused two HIGHs.
2. **Fairness traps come in classes.** The same starvation shape appeared
   FOUR times in one chunk. A written lesson is not a check — enumerate
   the classes a change touches.
3. **Measurement provenance.** Five rig arms silently measured the WRONG
   TREE (copied-venv `.pth` + a `sys.path` insert that could not resolve).
   Every arm now prints `mm.__file__` and asserts the fix is present.
4. **This rig drifts ~31% WITHIN a day** — only ADJACENT arms pair. The
   bridge arm that proved this was nearly skipped on my instruction.
5. **Silence is ambiguous.** Three different disguises in one day: a
   block-buffered log, a notification that never fired, a GC-thrashing
   process at 98% CPU. **Standing rule: any job over a few minutes emits
   a heartbeat, or it is not observable.**
6. **Estimates lose to measurements**, twice: a "~15%" follow-up measured
   <0.5% (killed), and a scan-sweep hypothesis eliminated by a stage
   breakdown that localised the real cost instead.

## What went wrong

- **I deleted a worktree a five-hour drill was still reading from.** A
  clean `git status` is not evidence a tree is idle. Checks 6–8 of that
  drill never ran; the salvage is still owed.
- **I collided with a parallel session's taker ceremony**, fixing the same
  crash-loop they were fixing. "One session drives the VM" exists for this.
- I told George the Go datum had moved favourably; **on v2 numbers it moved
  the other way** — NCAA Saturday sits ~6.3× beyond, not inside reach.

## Open — GEORGE'S RULINGS

1. **AC4's DRAIN_CAPPED clause** — reads "zero"; provably boot-re-stand
   only (tick indexes 0–6, first reading at tick 126, measured across five
   rig arms and live). One-line amendment owed.
2. **N43** — per-book opening positions. Until then the ask cap is dark
   and AC7 cannot be verified live. Four activation riders are on the N43
   row (sequencing, per-book input, `[post-first]` ordering, kept rungs).
3. **`MM_GATEWAY_OPS_URL`** — one env var; without it the healer never
   runs, AC8 is unmet, and the fresh-journal ceremony stays mandatory.
4. **Evidence standard** — AC5's rig drill was not run, but the live
   three-cutover chain is stronger evidence than the drill was designed to
   produce. Accept, or ask for the rig run?

## Open — engineering

- **The drain is still superlinear at high load:** 2.5× the acks costs
  6.5× per ack, net of drift. The stage breakdown localises ALL of it
  inside the venue drain (19.17 → 313.93 ms p50); sweep, commit, publish
  are flat or cheaper. CB4's prune fix flattened the FIRST curve; this is
  a second one further up the load range. **This is the pin's open
  question, and the Go port's brief.**
- `RejectBackoff.suppression()` is a live gap the rig **structurally
  cannot see** — the synthetic venue never rejects. Needs a
  reject-bearing workload variant.
- The SAIN/JAGU books sit through a tight market by a few cents — a
  pricing question (E31), not a guard defect.
- `scan-sweep.md` lists the remaining per-event full scans, incl. the
  taker's unbounded `_games` collection (grows with session length).
- The drill salvage (checks 6 + 8) is still running, pinned to `8bb20a4`.

## Next

George rules on 1–4 → the AC amendments land → the completion promise →
**pin the gospel → hard freeze → the Go port discovery opens.**
