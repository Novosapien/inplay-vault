---
description: "Fix-set implementation start: Phase 0 landed (dictionary batch PR #31, gateway /orders/mm PR #5, R11 recorded) and the two build streams spawned"
---

# 2026-08-14 — the fix-set build opens: Phase 0 + the team

> **Who:** Claude (implementation lead session) + George (handoff)
> **Type:** build coordination — Phase 0 of
> `specs/2026-08-14-mm-python-fix-set` (the "Python done" fix set).
> **Refs:** the spec folder (spec.md · progress.md · reviews/) ·
> [[market-maker/build-deploy-log]] · [[market-maker/parameters]] ·
> MM PR #31 · gateway PR #5

## What we did

- **Started the build over review-001's FAIL header, on George's
  explicit instruction.** The revision pass answered all 15 blocking
  items and George resolved Q1/Q2 on 14-08, but no review-002 ran. The
  override is recorded as a Known-Risk in the spec folder's
  `progress.md`.
- **P0a — R11 in force.** The operating rule (no maker cutovers while
  games are live; live = kickoff→final + the pre-kickoff hour;
  emergencies allowed, mirrored into the session note) was already
  dated in decisions.md (2026-08-14c). Added it to the engine repo's
  `deploy/OBSERVABILITY-REDEPLOY.md` and to the build-deploy-log's
  standing facts. AC11's two homes both carry the full text.
- **P0b — the dictionary batch.** MM **PR #31** (branch
  `phase0/fix-set-dictionary-batch`, base the running lineage
  `feat/always-quoting-step4b@5b10d68`): six rows, defaults only, no
  consumers — `prior_run_dir` (env `MM_PRIOR_RUN_DIR`) ·
  `tob_stale_after_s` 30 s 🟡 · `marketable_guard_enabled` on ·
  `boot_heal_enabled` on · `live_phase_offset_buckets` 8 🟡 ·
  `opening_position_shares` 0 🟡/E27. 885 tests, ruff + mypy clean.
  Rows mirrored into [[market-maker/parameters]] with statuses.
- **P0c — the healer's seam.** Gateway **PR #5**
  (`phase0/orders-mm-ops-route`, base `main@124991e`): `GET /orders/mm`
  wraps `LoadOpenMMOrders`, X-Ops-Key-gated (it discloses the whole
  resting MM book), miniredis-tested. → Hasan; the NATS ops lane stays
  his alternative.
- **Spawned Phase 1**: stream A (CA1 — the ANCHOR_SEED build) and
  stream B (CB1 — instrumentation + the six-game workload), each as one
  session under this guide's loop, branching from the dictionary batch.

## What we learned

- `mypy src` on the step4b lineage is clean at the tip — the "83
  pre-existing venv artifacts" baseline in the spec did not reproduce;
  the no-new-errors bar is simply "stay clean".
- The gateway's ops middleware fails closed and gates by exception
  (openRoutes allowlist), so a new GET route is key-gated by default —
  the safe direction for a book-disclosing route.

## What went wrong / got stuck

- Nothing yet. The review-gate override is the recorded risk to watch:
  if a fix-set chunk trips over a spec defect review-002 would have
  caught, that lands in the Drift Log.

## Decisions made *(mirror into [[market-maker/decisions]])*

- None new. R11 was decided 14-08c; this session made it effective in
  the runbook homes. The gate override is process, recorded in the spec
  folder.

## Questions opened / closed

- None. Hasan's HTTP-vs-NATS choice on the seam is tracked on gateway
  PR #5 (either satisfies CA4).

## Next

- Streams report back → per-phase review at the Phase 1 barrier → CA2 +
  CB2 spawn (CB2 merges after CA2 — the sync.py coordination rule).
- F5 merge train: PR #31 and every chunk PR get a REAL review pass
  (Q1) before merging; the replay drill gates on top.
- Nothing deploys without George's explicit go, per deploy; R11 gates
  timing. F2-before-a-game-night remains the desirable first deploy.
