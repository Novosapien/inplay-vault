# 2026-08-06d — the wire-contract fixes · the quarantine · §10.3 checkpoints

> **Who:** George + Claude (wire fixes step-approved in chat; the
> checkpoint build run autonomously at George's "carry on", review at
> the boundary)
> **Type:** build session in `inplay-market-maker`
> **Refs:** MM branch `feat/position-engine`, commits `21dd7e1` ·
> `25e4578` · `a9085e8` · `3c2368f` · `7f81791` · `b5472d1` · `5c9c0aa`
> · `d6f2754` · `86607b8` · `43ba08d` — **534 → 561 tests**, ruff +
> mypy strict clean. ⚠ All commits LOCAL, unpushed (George's rule).
> Vault: build pages, parameters, decisions `2026-08-06d`.

## What we did

1. **The four wire-contract fixes** from the 06-08c intake, exactly to
   the recorded designs: the independent ~250 ms beat task (the poller
   lost the beat AND its transport; a dead beat task stops the run
   loudly) · `account` (FIX Tag 1) on every new order with identity
   riding env through `Settings` (`MMIdentity`; the loopback account
   string is `"loopback"`, deliberately unmistakable for `1797733477`)
   · `venue_price_cap` $127.50 with the ladder ceiling floored at
   min(MEV, cap) · the `[governor]` note corrected 50 → 5,000 msg/s.
2. **⭐ George's new requirement, built same session: markets are
   independently failable.** Per-security quarantine at the
   orchestrator's cycle boundary — a faulted security's outcome becomes
   `BookSuspended("quarantined: …")`, the existing suspension sweep
   cancels its book, its engines are never re-run, and the other 169
   keep quoting. Event ingestion and the transport stay FATAL by
   design. Replay-safe, no new event type.
3. **§10.3 checkpoints, the full five-step design:** `state()`/
   `restore()` on every engine + the orchestrator aggregate · the
   canonical hashed file (schema + config guards, atomic writes,
   keep-3) · the hourly writer at a tick boundary · boot =
   restore-newest-valid + tail replay, rejects printed loudly · **the
   equality proof on the real game PASSES** — checkpoint-resume ≡
   never-stopped ≡ full-replay, byte-identical.
4. **Dedup retention:** seen keys prune on the accepted-time high-water
   mark past the one-week redelivery bound; §12.3's slot filled per
   the recorded design; duplicates never refresh an age; checkpoint
   schema → 2.

## What we learned

- **The equality proof earns its place as the deliverable.** It caught
  a real bug mid-build: tail replay did not re-arm the acceptor's gate
  (sequence + seen keys), so a redelivered tail event after a
  checkpoint boot would have been accepted TWICE. No unit test of the
  file format would have found it.
- **An asyncio beat task is independence from tick *scheduling*, not
  from tick *blocking*.** asyncio does not preempt: a synchronously
  blocking tick (checkpoint write included) still starves the beat.
  Recorded in `[beat-task]`; it is exactly what the N15 VM jitter
  measurement watches before the window tightens.
- **Quarantine must not swallow wire death.** The first design sketch
  wrapped the sync driver too — which would have left a beating heart
  on a dead wire. The boundary is engine computation only; the
  transport raises through and the dead-man does its job.
- **Only accepted events read the acceptor's clock** — a duplicate
  consumes no time. The retention tests briefly assumed otherwise.

## Decisions *(mirrored into decisions.md 2026-08-06d)*

- ⭐ Markets independently failable (George) → the per-security
  quarantine, boundaries as recorded.
- ✅ The wire-contract designs and the checkpoint five-step design
  executed as recorded — no deviations.
- Autonomous, tagged in code: the quarantine's fatal boundaries ·
  BookSuspended as the quarantine outcome (rides the existing sweep) ·
  duplicates never refresh retention age · checkpoint schema guard
  separate from the integrity hash · tail replay re-arms the gate.

## What's open / next

1. **Deploy + drill on the VM** — the engine to `inplay-market-maker`
   (10.0.2.3), then the docker drill against the real rig incl. a
   checkpoint-boot restart; then the N15 jitter measurement (beat gaps
   name tick stalls) before any window change.
2. **The Hasan conversation** (George owes the send): the infra file ·
   wash-trade-vs-N12 (design-changing — before any venue drill) · NATS
   grants for `sr.probabilities.>` · his guide's stale facts.
3. Unchanged: the go-live ingestion switch (at push-live) · N31 group
   commit (measure the real fsync on the VM first) · the boot-reconcile
   healer (parked) · E29–E38 · pushing branches (George's call).
