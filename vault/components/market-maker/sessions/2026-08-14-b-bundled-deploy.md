---
description: "Step 4 phase B + taker boot rebase built; the bundled deploy (gateway #3, converger task, boot rebase) landed; the CFG-0018 import-root correction"
---

# 2026-08-14-b — the bundled deploy: gateway #3 · converger task · boot rebase

> **Type:** build + deploy session (daylight, no live games). George +
> Claude. **State at close:** gateway `main@124991e` (tag 9383 live,
> window 10 s) · engine **supervised28/CFG-0026**
> (`feat/always-quoting-step4b`, converger TASK mode) · taker
> **SNT-CFG-0019 / journal snt16** (`step4b-wash @ 5b10d68` — wash
> guard AND boot rebase).

## What we did

1. **Built step 4 phase B** (George: "implement, do not deploy"): the
   converger moves onto its own asyncio task at `converge_interval_s`
   (0.25 s). The tick stages; the task converges. Durability holds by
   construction (no yield inside stage → commit). A dead converger
   task stops the run loudly. `CONVERGE_STALE` (2 s) is the outbound
   DRAIN_CAPPED. Constructor default 0 keeps the phase-A shape for
   direct-drive tests; the composition opts production in.
2. **Built the taker BOOT REBASE** (the CLEM permanent fix): each
   book's FIRST exec-borne venue figure (tag 9383) after boot may be
   adopted as the float basis — journalled (`rebase`, replayed
   chronologically), loud, once per book per boot. Mid-session
   `[no-adopt]` holds. Exec-borne only — the `position.>` fallback can
   be one fill stale, precisely what must never be adopted.
   `SNT_BOOT_REBASE=off` reverts.
3. **Deployed the bundle on George's go** (11:46–11:51Z, ~4 min
   outage): gateway binary swap to `main@124991e` (#3 — "OE exec
   position" lines prove 9383 parsing), engine to supervised28/
   CFG-0026 (converger task live), taker to CFG-0018/snt15 (floats =
   env + snt14's 20,190-line drift; CLEM check 3794+44=3838 exact).
4. **Corrected a false regression alarm and closed the real gap.** The
   docs session flagged "wash guard lost"; `/proc/PID/environ` showed
   the taker's true import root is `~/snt-checkout` (PYTHONPATH), which
   was at `main@772e79c` — guard present, **boot rebase absent**. Fixed
   by merging origin/main into the branch (`5b10d68`, 885 tests) and a
   taker-only cutover to **CFG-0019/snt16** at 12:10Z — the first build
   carrying both features, verified in the running process.
5. **Validated the dual-publisher feed** for George: 5,612 readings
   since boot, zero conflicts/poison/rejects; §7.3 makes the two pools
   redundancy, not error.
6. Amended gateway PR #4 (the `oe_adapter.go` fallback now 10 s) and
   flagged the PR #37 trap (its head is ALL of `testing`, not the
   one-hunk hotfix).

## What we learned

- ⭐ **The taker's code root is `snt-checkout` via PYTHONPATH — never
  the ExecStart venv path.** Verify with `/proc/PID/environ`. Two
  sessions independently misread this; the runbook now records it.
- A branch cut from a deploy lineage silently misses later main merges
  — check `git merge-base --is-ancestor` against main before cutting a
  deploy branch, and against the RUNNING tree, not a lookalike.
- The local gateway repo's main was stale; the first binary built at
  `005fdd8` without #3. Pull before building deploy artifacts.
- Boot-rebase silence is itself a receipt: zero rebases fired at
  CFG-0019 = the mechanically recomputed floats agree with the venue.

## What went wrong / got stuck

- The 11:51Z receipt "boot rebase ACTIVE" was false (wrong import
  root). Corrected in the build-deploy-log the same hour; the peer
  session corrected the build pages.
- The gateway ops surface has no runtime dead-man toggle — env-only,
  restart to apply (already known, reconfirmed).

## Decisions made

- George: deploy the bundle in the daylight window (executed).
- George: cut the taker to the merged branch (CFG-0019) to make the
  running state carry both features.

## Questions opened/closed

- None formally. PR #37 handling (close-and-recut vs promote testing)
  sits with George + Hasan; the MM is safe either way (validated).

## Next

1. Missed-sweeps step 1 — the engine-cost measurement (quiet slot).
2. Tonight's slate is the converger task's first game-load test —
   re-arm the VM watch on `supervised28.log`.
3. George's rulings: the p_ref cutover rule · the vault docs branch
   commit · the MM PR review backlog (#21–#30 + step4b's PR to main).
