---
description: "The 12-08 addendum's two taker build items built: fetch-aged T-F07 freshness and exec-borne T-S05 reconciliation (MM PR #28 + gateway PR #3)"
---

# 2026-08-13 — taker hardening: the two 12-08 build items

> **Type:** build session (the T-F07/deploy session continuing).
> George's go: "we just build them now." Code only — the VM stays the
> operating session's; nothing deployed from here.

## What we did

1. **T-F07 freshness prices the fetch, not the delivery**
   (the 12-08 addendum's top item). `Fetched-At` (the publisher's own
   fetch instant, E38's stamp) drives the staleness clock: clamped
   against clock skew, never regressing on re-delivery, no header = no
   freshness (quiet). Redelivered finals no longer reopen POST. The
   restart-re-derives-LIVE class (three demonstrations 11/12-08) dies.
2. **T-S05 reads the exec report's own 9383.** Gateway **PR #3**
   forwards tag 9383 on the order event (`posSize` — same message as
   the fill; cannot race, cannot half-arrive). The taker prefers it;
   the parallel `position.>` feed serves only books that never saw an
   exec-borne figure (old gateway / pre-first-fill) — T-S05 never
   fails quiet, and 12-08's dropped-companion false halt cannot recur.
3. **MM PR #28** (`feat/snt-hardening`): 696 tests, ruff + mypy-strict
   green. Gateway PR #3: full suite green, one conditional field —
   Hasan's review.

## What we learned

- The reconciler's grace clock starts at the first mismatched CHECK,
  not at the venue report — the runtime tick tests must tick twice.
- The earlier gateway suite FAIL was an embedded-NATS timing flake;
  clean on `-count=1` rerun.

## Not done, deliberately

- The +31 VATH float patch (snt8) — an env change on the VM, the
  operating session's at its next cutover.
- Deploys: PR #28's item 2 activates only when gateway PR #3 deploys;
  until then behaviour is exactly today's.

## Late addition — merged AND the taker deployed (George's go)

- Both PRs merged (#28, gateway #3). **The taker cutover ran the full
  runbook from this session:** halt (0 cancels) → stop → binary to
  `main@c4c51b4` → env `SNT-CFG-0014`, fresh journal `snt11`, floats
  recomputed mechanically (env + snt10's 23,366 journalled fills, all
  180 books) → start. Boot clean: AUTO, 180 books, fresh journal.
  **51 fills in the first 2 minutes, zero reconcile alarms** — the
  recomputed floats agree with the venue on every book that traded.
  The −31 VATH hand-patch was NOT applied: the operating session had
  cut over twice since (CFG-0011 → 0013), and the rail halts safely if
  any float is still wrong.
- ⚠ **The gateway swap (PR #3's binary) is deliberately NOT done:** the
  MM engine is live-quoting for tonight's dry run, and the ordered
  rule requires it stopped first. Until the swap, the taker's T-S05
  runs on the position.> fallback — exactly today's proven behaviour.

## Late addition 2 — the WASH GUARD (George's go) built, merged, deployed

- George spotted rejects; forensics: `FAILSRISK[4963224393]: Wash
  trades are being stopped on this account` (CHIE ×3, RAVE ×1 in
  retained logs) — an arrival crossing the taker's own unfilled IOC
  remnant. **Ruling: the venue flag stays ON** (a self-print is
  manufactured volume; the reject is correct) **and the collision dies
  bot-side**: while an own order rests in its 1.5 s window, the
  opposite direction skips that arrival (same-side stays allowed).
  Realized flow unchanged — those orders were being rejected anyway.
  Fresh T13/T-C02 evidence en route: taker↔MM prints fine; self-prints
  blocked — house-vs-house allowed, self-wash enforced.
- **MM PR #29 merged; deployed by runbook cutover** (halt → stop →
  `main@772e79c` → CFG-0017, journal `snt14`, floats mechanically
  folded → start): boot clean, 46 fills in the first 2 min, zero
  alarms. ⚠ The env was at CFG-0016/snt13 — the operating session had
  cut over twice since this session's 0014; the script preserved its
  floats and state mechanically. One test rewritten to the guard's new
  truth (a fully-committed book sends NOTHING until the remnant
  settles). ⚠ mypy on `tests/` carries 51 pre-existing errors from
  main's new operator-screen test files — upstream, not this branch's.

## Next

1. **Gateway swap after tonight's game** (ordered sequence: taker down
   → engine down → gateway → engine → taker), coordinated with the
   operating session — it activates T-S05's exec-borne primary path.
2. Tonight's dry-run game remains the first live T-F07 proof (TT5) —
   now with the fetch-age fix deployed.
3. The vault branch is still uncommitted across four sessions —
   standing call.
