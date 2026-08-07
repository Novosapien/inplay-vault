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

## Addendum (07-08, same chat session) — the rig drill: 16/16

`scripts/rig_drill.py` (kept in the repo, MM `3ba52fa`) proved the
06-08d changes on the real docker rig: the ~250 ms beat on the wire
(20 beats/5 s, worst gap 257 ms — the 4 s dead-man never close) ·
`account` from the env on all 38 orders · pre-boot catch-up + a
re-offer landing as liveness, 8/8 readings drained · **the PRODUCTION
checkpoint boot**: a real `python -m mm.runtime` subprocess restored
checkpoint seq 67, replayed 3 tail events, redelivered ZERO, repriced
on the next reading, exited clean on SIGTERM. One drill-script
correction: outbound cancels are legitimate reconciler cancel-replace
traffic — the honest dead-man check is the worst beat gap.

## What's open / next

1. **Deploy + drill on the VM** — the engine to `inplay-market-maker`
   (10.0.2.3), then `scripts/rig_drill.py` re-run there incl. the
   checkpoint-boot restart; then the N15 jitter measurement (beat gaps
   name tick stalls) before any window change.
2. **The Hasan conversation** (George owes the send): the infra file ·
   wash-trade-vs-N12 (design-changing — before any venue drill) · NATS
   grants for `sr.probabilities.>` · his guide's stale facts.
3. Unchanged: the go-live ingestion switch (at push-live) · N31 group
   commit (measure the real fsync on the VM first) · the boot-reconcile
   healer (parked) · E29–E38 · pushing branches (George's call).

## Addendum (07-08b, same chat session) — the VM deploy: 16/16 on the real disk · N31 measured

The engine is ON the VM and drilled there. The VM has NO internet
egress (the NATs cover other subnets; extending one would also give the
NATS VM egress — deliberately not touched), so artifacts ship through a
new GCS bucket `inplay-mm-deploy` over Private Google Access (recorded
in the infra file addendum for Hasan). Python 3.12.13 standalone + uv +
wheels + amd64 docker images all offline; repo at the branch tip via
git bundles.

- **`scripts/rig_drill.py`: 16/16 on the VM**, journal + checkpoints on
  `/var/lib/mm` (the real pd-ssd). Worst beat gap **299 ms** on
  e2-medium — the first real N15 jitter data point.
- ⭐ **N31's number landed: fsync p50 1.70 ms · p99 2.47 ms → ~579
  events/s single-writer ceiling.** Under the 04-08 estimate
  (1,000–3,000/s) and far under the ~2,100/s the 200 ms capability
  needs. **Group commit: required, build next.**
- Two drill-script fixes the VM exposed (committed): the restart
  subprocess runs offline (`sys.executable`, not uv) · the drill
  ensures the stream (it plays the publisher; a virgin server has
  none). The Mac's arm64 docker images needed amd64 rebuilds.
- Deliberately NOT done: no systemd unit (the multi-day N15 jitter
  measurement means leaving a loopback engine running — George's call)
  · nothing touches production NATS or the gateway (the
  `sr.probabilities.>` grants remain the open ask).

## Addendum (07-08c, same chat session) — pushed to main · supervised mode built

- **⭐ George: push everything (Hasan's agent is engaging).** The
  standing local-only rule is superseded for the MM repo: the full
  build line merged to `main` via PR #4; `dev` and `testing` branches
  created from main. The vault and the sportradar service remain
  unpushed (the service branch carries the publisher half of the
  readings contract — flagged to George).
- **⭐ George: test against the QA venue's 7 populated tickers**
  (IPTCEAGL · IPTCPATR · IPTCBILL · IPTCGIAN · IPTCCOWB · IPTCSTEE ·
  IPTCJETS). Built: **supervised mode** (`feat/supervised-mode`,
  PR #5, 561 → 570 tests) — books NAMED, every number from a reviewed
  file (template in `docs/supervised-inputs.template.json`), real
  identity required, readings leg unwired, live mode untouched.
  Running it stays gated on Hasan's agreed posture + the
  wash-trade-vs-N12 decision.
- **What turns the mode into a real test:** (1) the wash-trade decision
  (George/Hasan) · (2) 7 T values from Edwin into the template ·
  (3) Hasan's posture sign-off. Then it is a config change.

## Addendum (07-08c→f, same chat session) — THE MACHINE IS LIVE ON THE VENUE

The full arc, recorded in decisions 2026-08-07 b–f: probes verified
wash-off · we seeded 100k × 7 (the transfer ledger) · the first
supervised run exposed the LmtPerc reject loop · the book walk ate the
stale quotes and anchored all six books at Edwin's prices · two more
live lessons (the no-id fill that killed the engine → the poison fix
PR #6; the duplicate-id deadlock → MM_CONFIG_VERSION PR #7) · and the
continuous run now STANDS: **all six books two-sided at Edwin's
prices, 8–17k shares/level, the poker walking them so the books
visibly breathe** — proven end to end by the gateway log showing the
engine cancelling a foreign resting order off its own book.

**Running on the VM right now:** the engine (`supervised3`, CFG-0002)
+ the poker (120 min from ~18:00Z). DAY orders die at 23:59 ET; the
dead-man sweeps if the engine stops. **Build items born today:** the
reject-backoff (three observed shapes) · N31 group commit · the N15
jitter recorder · eat the residual ghost quotes (George's call).
