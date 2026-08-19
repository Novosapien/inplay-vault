---
description: "Analysis session: Edwin's two pricing models reconciled, the 28-07 feed engine ruled normative-pending-E47, and the daily-feed ingestion pipeline designed"
---

# 2026-08-13c — the daily reference feed: analysis + pipeline design

> **Type:** analysis + design session (the brief:
> `vault/drafts/daily-reference-feed-analysis-brief.md`). George's
> constraints held: analysis and design only, **nothing deployed** — the
> live machine (supervised21/CFG-0020) was never touched; today is
> game-day (first real live games 23:00Z).
> **Deliverable:** [[market-maker/systems/daily-reference-feed]] — the
> analysis verdicts, the pipeline design, the sized build plan.

## What we did

1. **Answered the two-model question (the brief's Q2, first as ordered).**
   The 28-07 feed engine (`reference/inplay-reference-feed/`) is
   **normative for the daily file**; the 08-09 Gamecast bundle is the app
   mock's display pricing. Built on the plain-English guide's algebra
   (his live leg = ours × the maturity dial; `seasonFair` = the mock's
   stand-in for the daily file it cannot fetch), extended with the file
   question the guide did not ask: nothing in the 08-09 bundle describes
   the daily file's creation. The guide's unfiled asks are now **E47**.
2. **Answered the producer question (Q1).** Edwin owns the methodology
   and remains the producer; we consume, and run the NFL de-vig as a
   **verifier only** (recommendation on N18, George rules). Producing
   ourselves breaches §1.5 + the 22-07 remit line, and the NCAA leg
   needs a data-acquisition project (SR historical backfill, all-170
   schedules, conference groups) nobody has commissioned.
3. **Designed the ingestion pipeline (Q3)** — the systems doc, §3: bus
   delivery on the 05-08c ingestion-ruling shape (watcher worker
   validates → bucket → row → JetStream; the engine consumes, journals,
   fans out), the proposed `REFERENCE_NUMBERS` event for the N23 ask
   (one event per accepted FILE, basis `source_id + effective_time +
   revision`, rows + object hash in the payload), the monotonic apply
   guard, banked-wins from our own OFFICIAL_RESULTs, the stale-T ladder
   (mechanism ours, all three thresholds 🔴 Edwin's), and the phase-2
   upload page on the N29 panel pattern.
4. **Sized the build plan (Q4)**: phase 1 ≈ one working week, fits
   before the NCAA secondary open (~26–27 Aug) if the asks move now.
   Phase 3's break-glass producer is deliberately NOT sized in.
5. **Verified the Downloads bundle** (George's mid-session pointer:
   `~/Downloads/InPlay-Handoff-George/`). The two pricing docs are
   byte-identical to the vault's filed copies; the bundle adds the demo,
   the JSX source, and two HTML exports — no new pricing content. The
   JSX (`InPlayHomeV1423-SOURCE.jsx:331`) confirms the filed docs
   transcribe the mock's maths faithfully (`e0 = 5.5 + pct·6.5`, the
   5.25 coefficient, clamps 14/118 and 24/96).

## What we learned

- **The feed's `sigma` is consumed by nothing today.** Validated,
  stored, unused — quote width runs on measured volatility (E31/E44).
  "sigma sets quote width" in the handover was design intent, not the
  build. Honesty note added to its parameters row.
- **E43's schema half was already answered** — the 28-07 delivery +
  sample validate clean against `mm/adapters/reference_feed.py`. What is
  actually owed is his production stand-up date (the forward-looking
  gains model was unbuilt as of 07-08). E43 re-scoped 🟡.
- The Gamecast bundle's jitter/noise machinery is a **third independent
  instance of the invented-movement instinct** (after RPV-1/RPV-2) —
  logged into E47 as E34 evidence, not a new question.
- The 03-08 "the engine watches the bucket" wording predates the 05-08c
  ingestion ruling; the design supersedes it with bus delivery —
  explicitly flagged for George's approval rather than silently changed.

## What went wrong / got stuck

- Nothing blocking. The gamecast plain-English guide's questions had
  never been filed into open-questions — the analysis nearly re-derived
  them from scratch before finding the guide's reconciliation section.

## Decisions made

- **None.** Everything here is recommendation or proposed shape; the
  rulings are George's (bus-vs-bucket-watch, N18's verifier posture, the
  06:00 interim hand) and Edwin's/InPlay's (E47, N23, stale-T values,
  E43 date). No decisions.md entry filed.

## Questions opened / closed

- **Opened: E47** — Gamecast: display model or supersession? Carries the
  M dial, 5.25 vs 5.00, the C2/injury home, and the off-field method
  adoption. Ask first; blocks any Gamecast adoption.
- **Moved: E43** 🟡 (schema ✅, production date owed) · **N18**
  (recommendation filed — read his number, verify NFL) · **N19** (design
  filed; the 06:00 hand still George's) · **N23** (the proposed event
  shape filed; the ask rides N28's round).
- **Still open, unchanged:** who uploads at 06:00 ET until the page
  exists (George) · how long we may quote on a stale T (Edwin — now with
  the ladder mechanism + 🔴 parameter rows to ask with).

## Working docs touched

[[market-maker/systems/daily-reference-feed]] (new) ·
[[market-maker/open-questions]] (E47 new; E43/N18/N19/N23 notes) ·
[[market-maker/parameters]] (stale-T rows ×3 🔴, de-vig drift threshold
🔴, sigma honesty note) · [[market-maker/market-maker]] (systems table
row) · [[market-maker/build/ingestion]] (path-3 pointer).

## Next

1. **George reads [[market-maker/systems/daily-reference-feed]]** and
   rules on: bus delivery (§3.1) · N18's verifier posture (§2) · the
   06:00 interim hand (N19) · whether phase 1 starts before the N23
   blessing lands (the N28 precedent) — then build begins.
2. The E-round additions go out with the existing unsent round: **E47**
   (first) · the stale-T values · N23+N28's blessing · N22's extra field
   · E43's production date.
3. Vault branch still uncommitted across sessions — standing call
   (George).
