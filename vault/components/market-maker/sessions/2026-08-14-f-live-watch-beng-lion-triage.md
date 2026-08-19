---
description: "Read-only live-test watch (13-08 slate) + the BENG/LION dead-price triage: the fresh-journal p_ref rebase found and measured; VM never touched"
---

# 2026-08-14-f — the live watch and the BENG/LION triage (read-only)

> **Type:** monitoring + triage session, 13-08 ~23:00Z → 14-08 ~01:20Z.
> George + Claude. **George's constraint held throughout: "do not break
> anything, only monitor" — every command on the VM was a read.**
> Nothing deployed, no process touched, no config changed.

## What we did

1. Full working-guide familiarization, then armed on the 13-08 live
   slate (the first real games end to end).
2. **Watched the first live load hit the engine.** At 23:10Z the tick
   rate collapsed 1.9/s → ~0.17/s (~6 s per tick): every tick pinned
   the venue drain cap (`drained=512, DRAIN_CAPPED=venue`),
   `MISSED_SWEEPS` ran 6–10 per sweep, `PUB_SHED` climbed 3 → 68.
   It recovered between kickoffs and returned with each new game.
   Quoting never stopped; zero `HEARTBEAT WITHHELD`; the dead-man
   never fired.
3. **Found an orphan cancel-reject flood riding the same window:**
   156 ClOrdIDs from supervised21 (CFG-0020) drew 18,500+
   `CANCEL_REJECTED "ORDER DEAD[DMA]"` events (~12/s at peak,
   ~71 repeats per id). The engine has no state for these ids and
   correctly drains them — so the retry source is upstream (gateway
   suspected, unproven; the gateway log was not read).
4. **Disproved "the MM's orders are not going through" / "only two
   levels":** sampled `market.book.*` directly off NATS — BENG, LION,
   STEE, PACK all two-sided, 6–9 levels a side, tight spreads,
   updating. Zero rejects on BENG since 23:00Z. The thin view was the
   panel: `PUB_SHED` sheds `resting_orders` from `mm.state` when the
   payload exceeds its 256 KB budget.
5. **Triaged George's 14-08 report (no price movement on IPTCBENG /
   IPTCLION) stage by stage.** Publisher polling ✓ · stream fresh for
   sr:competitor:4416/4419 ✓ · runtime binding correct, both books
   requoted (~2,600 acks each / 17 min) ✓ · freshness CURRENT ✓.
   **The feed was never dead.**
6. **Root cause: the fresh-journal p_ref rebase.** Three cutovers ran
   during the games (supervised25 → 26 first event 23:40:10Z → 27 /
   CFG-0025 first event 00:19:53Z), each `replayed 0`. On every boot
   the valuation engine meets an in-play game and freezes `p_ref` at
   the CURRENT probability (`[late-arrival]`,
   `mm/valuation/engine.py:331`). supervised27 anchored BENG at 0.866
   instead of the 23:03Z kickoff 0.711 → live adjustment −$0.09
   instead of +$0.69; the accumulated in-game move was erased on all
   live books at every cutover. CIN–DET being a decided blowout
   (0.848/0.152, saturated) left ~±$0.10 of visible movement — so
   only those two books read as frozen while close games kept moving.
7. Updated the [[market-maker/build-deploy-log]] triage row with the
   full finding.

## What we learned

- The venue drain cap (512) is too low for game-time ack volume — the
  saturation is the predicted post-group-commit engine-time constraint
  wearing its first live face.
- The `mm.state` shed makes the panel lie thin under exactly the load
  where you watch it hardest.
- The watch script's `readings/min` and `tick=` fields break when
  non-tick lines flood the log tail — its zeros were parse artifacts,
  not a dead engine.
- The kickoff freeze (N22's ruling) is derived state: it does not
  survive a fresh journal. Every mid-game deploy silently re-anchors
  every live book.
- SR posted CIN–DET's first probability 3 minutes after kickoff — a
  late first reading is normal for this slate, not an outage.

## What went wrong / got stuck

- ~25 minutes on wrong theories (dead feed, binding swap) before the
  price-vs-probability direction check exposed the rebase. The swap
  hypothesis fit the sign data; only the boot-time p_ref receipt
  killed it.
- The orphan cancel-reject SOURCE was never identified — the gateway
  log is on the gateway VM, out of this session's read scope.

## Decisions made

- None here. George's constraint (read-only) and the later rulings
  (fix-set, deploy freeze) belong to their own sessions.

## Questions opened / closed

- None numbered. The rebase finding is cross-referenced into **N22**
  (its kickoff ruling is violated on every cutover) and became
  **fix-set CA1 / ANCHOR_SEED** (MM PR #32). The cancel-retry source
  stays a loose end below.

## Next

1. **Identify the orphan cancel-retry source** — read the gateway VM's
   log for the 23:10Z window (who resends cancels for DMA-dead
   orders); file or clear the gateway-retry suspicion.
2. The saturation fixes ride the missed-sweeps rows in
   [[market-maker/build-deploy-log]] (measure → de-phase/incremental
   sweep → speed work); the `mm.state` shed wants a panel-side
   "payload degraded" badge so a thin book is never misread again.
3. ANCHOR_SEED (PR #32) closes the rebase defect — deploy gated on the
   freeze and George's go.
