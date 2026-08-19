---
description: "Forensics: the Active/Defensive/Stable flapping on the panel is the portfolio-wide missed-sweep deduction — 11.7% of ticks miss a slot on supervised22"
---

# 2026-08-13-d — why the market state flaps: missed sweeps demote the whole book

> **Type:** investigation, read-only. George + Claude. Nothing deployed;
> the VM untouched beyond reads (+ a throwaway script in `/tmp`).
> **Trigger:** George: the panel shows Active, sometimes Defensive,
> sometimes Stable — why?

## What we did

Traced the observed state mix to its cause, code-first, then verified
live on the VM.

1. Read the Ch 6 engine (`mm/market_state/engine.py`). The §6.3 mapping
   is the only path that produces this exact trio: RP Status Warning →
   Active · Degraded → Defensive · Valid → Stable. Demotions are
   instant; promotions earn 10 s per rung.
2. Read the freshness engine (`mm/valuation/freshness.py`). Two rows
   drive it: `missed_sweeps == 1` → raw status Warning ·
   `missed_sweeps >= 2` → Degraded. The §3.5 confidence ceiling agrees
   (deduct 15 → conf 85 → Warning · deduct 30 → conf 60 → Degraded).
3. Confirmed the counter is **portfolio-wide**
   (`orchestration/engine.py::_note_sweep`): one missed sweep slot
   stamps every security's next status evaluation. All 180 books
   demote together on the same sweep.
4. Verified live on the VM (`supervised22.log`).

## What we learned

- **The live numbers (supervised22, ~17:53Z → 20:05Z):** 2,640 of
  22,549 ticks (**11.7%**) logged `MISSED_SWEEPS` — the same rate as
  supervised21's addendum-1 finding. **196 ticks logged `=2`**
  (→ Defensive). Median gap between miss ticks is **2.0 s**, p90 9.5 s,
  max 81 s.
- **The recovery arithmetic explains the mix.** After a clean sweep, a
  book needs ~20 s of quiet to read Stable again (status Warning →
  Valid 10 s dwell, then market state Active → Stable 10 s dwell). With
  misses arriving at the density above, a book can sit Stable roughly
  **8% of the time**. So the panel reads: mostly Active, Defensive on
  the double-miss bursts (~once a minute), Stable only in the rare
  quiet stretches. Exactly what George observed.
- **The misses are the known post-group-commit constraint** — engine
  time on ack bursts (08-13-b addendum 1). Miss ticks correlate with
  `drained=` spikes (100–200 acks); the overnight dwell republishes
  books in synchronized waves, so the acks clump. supervised22 also
  runs the state publisher (`pub=` counters, `PUB_SHED=33`), which adds
  tick cost the supervised21 measurement did not carry.
- **Quoting is unaffected.** Stable, Active and Defensive all permit
  quotation, and today they quote identically — the E31 per-state
  width floors are not wired. The flap is a label + §3.5 confidence
  effect, not a liquidity event. Suspended never fired.
- **The deployment state had moved past the vault notes** (George's
  flag, confirmed): the operating session cut the maker over to
  journal **supervised22 / CFG-0021** at ~17:53Z; the latest session
  notes stop at supervised21/CFG-0020. The taker runs snt14/CFG-0017.
- `mm.state` cannot be sampled with the `market-maker` NATS user —
  publish-only, subscribe draws a permissions violation. Verifying
  panel-visible state needs the admin proxy's credentials or a grant.

## What went wrong / got stuck

- Nothing material. The `mm.state` subscribe denial (above) closed the
  direct-sampling route; the log arithmetic answered instead.

## Decisions made

- None. Investigation only.

## Questions opened / closed

- None formally. Two observations for the always-quoting workstream
  (they ride existing items, not new numbers): (1) the sweep slot
  (0.5 s / 0.625 s max since the 08-11 ruling) is what the 11.7% miss
  rate is measured against — the step-4 design pass + drain-cap
  re-size already own the fix; de-phasing the dwell waves remains a
  candidate. (2) Whether a portfolio-wide missed-sweep deduction
  SHOULD demote all 180 books' visible state, or only the books whose
  cycle actually slipped, is a fair E-round flag — §3.1.4/§3.5 as
  written are portfolio-wide, and the build follows them.

## Next

- The step-4 design pass (decoupled quote publication) + the drain-cap
  re-size measurement — already queued in 08-13-b; this session adds
  the panel-visible symptom to their motivation.
- If the panel should read calm before those land: raising the sweep
  slot back toward the spec's 2.0/2.5 s would collapse the miss rate —
  George's call, it trades the 08-11 cadence ruling.
