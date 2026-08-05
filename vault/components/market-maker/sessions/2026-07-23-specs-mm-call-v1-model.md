# 2026-07-23 — tZERO specs read · MM call · the v1 model lands

> **Who:** George + Claude (one continuous working session, 22-07 evening → 23-07)
> **Type:** design / research / call extraction
> **Refs:** [[23-07-2026-market-maker-follow-up]] · tZERO OE FIX spec v2.2 + MD spec v8 (PDFs) · `mm-pipeline.html` · commits `26df9fc` (before rework) + the after-rework commit

## What we did

- **Built the questions register properly:** every row in
  [[market-maker/open-questions]] rewritten in plain language (after several
  rounds of George pushing back on jargon and format changes); jargon key
  added; new questions opened across the session (E13–E16, T8–T11, N10–N14,
  S4–S5).
- **Stance set:** *we ask, we don't propose* — parameter values are InPlay's
  remit. Plus the remit line: *"if Edwin watched the book, could he tell the
  difference?"* Yes → his question; no → engineering mechanics, ours.
- **Built `mm-pipeline.html`** — 15-stage chronological walk-through of the
  whole machine with per-stage what-it-is / in-out / deferred / questions;
  equations rendered as equations, lookups as lookups, rules as rules
  (several formatting iterations to get it digestible).
- **Created [[market-maker/learnings]]** — the running distilled-understanding
  log; ~20 entries captured across the session.
- **Read both tZERO FIX specs end-to-end** (Order Entry v2.2, Market Data
  v8) and mined them: replace chain semantics, no iceberg/ExecInst,
  Pos*-per-fill, aggregated-only book, halt machinery on the feed, busts as
  public trade deletes, disconnect behaviour.
- **Prepped and supported the tZERO call** (plain-English ask list in chat) and
  **extracted the 23-07 MM follow-up call** in full — 17 findings routed into
  decisions / open-questions / parameters / plan / learnings.
- **Reworked all the docs to the v1 model** (hub, valuation engine, quoting
  engine, decision-cycle reference, market state, pipeline artifact), with
  before/after commits.

## What we learned

- **The v1 machine is far simpler than what we were designing.** Edwin's
  lifecycle (rest-until-gone, cancel+repost-remainder, reload-at-top) deleted
  the top-up arithmetic, quote aging, replenishment, and the amend-vs-cancel
  trilemma in one stroke. The reconciler analysis is shelved in learnings for
  the augment-later phase, not wasted.
- **Replace = back of the queue on every matching engine** (Troy), and here
  nobody cares — the MM isn't competing with other MMs.
- **The venue gives no self-cross protection at order entry** (no ExecInst) —
  and v1 explicitly tolerates a momentary self-cross during adjustments.
- **The MM is event-rate bound, not CPU/RAM bound**; hot path is push-only +
  in-memory with per-cycle snapshots; the event log is write-only, isolated
  from the prod DB, object-storage-shaped.
- Full list in [[market-maker/learnings]] (22-07 + 23-07 sections).

## What went wrong / got stuck

- **I repeatedly wrote to vault docs before George validated** — now a hard
  rule: discuss in chat, write only after a yes.
- **Simplification requests took several rounds** — first pass simplified only
  one table; second changed layout when only wording was asked for. Lesson:
  change exactly what was asked, everywhere it applies.
- **The planned deep-dive agenda didn't happen** — the 23-07 call went to
  launch status + the MM working session; **E11 and E12 were never asked.**
- The 22-07 sequencing/reconciler design work was overtaken within a day by
  Edwin's simpler model — right process (it produced sharp questions), but a
  reminder that design-ahead-of-Edwin has a short shelf life.

## Decisions made *(mirrored into [[market-maker/decisions]])*

- 23-07 MM-call batch: v1 lifecycle · post-first with momentary-cross
  tolerance (George confirmed #11) · bifurcated cadence · quantities-only
  randomizer · SR-probability-only in-game · remaining-wins internal weekly ·
  off-field = popularity index · Wednesday drop · betting-feed parity · IPO
  buyer + "start with the IPO" · simulation-game testing · v1 simplicity
  mandate.
- 23-07 spec-read batch: OE venue facts (replace chain, no iceberg, no
  ExecInst, Pos* fields, unsolicited cancels, corrections) + design
  consequences (never replace below CumQty; push-only hot path; event log
  isolated from prod DB).

## Questions opened / closed *(state in [[market-maker/open-questions]])*

- **Closed:** E2, E13, E15 (valuation inputs) · T8 (queue position answered;
  edge cases moot) · N10, N12 (lifecycle + sequencing — Edwin's model).
- **Opened:** N14 fill-response logic · T11 self-match prevention (Troy
  checking) · S4 sportsbook parity (Cody) · S5 Sport Radar fit check · T9/E16
  opening auction · T10 one-environment + permanent test symbols.
- **Still the top two, unasked:** **E11 settlement · E12 NCAA scope.**

## Context for processing incoming Edwin material

Material expected from Edwin (any new doc likely fulfils one of these):

- **The original MM simulation Python files** (E4 — "functional, not a heavy
  lift"). Read as *his prior working model*: mine for parameter values,
  formula shapes, and trigger logic — but it predates the v1 decisions above,
  so nothing in it binds.
- **The formula write-up** — on the call he said "I'll write the formula…
  it's fairly simple" (the game-by-game convergence behaviour: with 17 games
  left the remaining-season term dominates; with 1 game left the live
  probability dominates, like options converging to expiry).
- **The Wednesday-drop content** — off-field popularity index + remaining-game
  win probabilities (format not yet agreed).
- Possibly **CTS-001 §3** (E10) or an updated standards doc.

Processing protocol for ANY new Edwin document:

1. Read [[market-maker/working-guide]] first, as always.
2. The 23-07 v1 decisions in [[market-maker/decisions]] are the current
   truth. A new document does NOT silently supersede them — per the standing
   ground rule (spoken decisions outrank written docs), every conflict gets
   surfaced to George and adopted or rejected **explicitly**.
3. Check each claim against [[market-maker/open-questions]] — does it answer
   an open question (close it, cite the doc) or contradict a resolution
   (flag it)?
4. Numbers go into [[market-maker/parameters]] with a status and the doc as
   source — nothing becomes ✅ without George's validation.
5. **Nothing is written to the vault before George validates it in chat**
   (hard rule from this session).

## Next

1. **S5 — verify Sport Radar can serve the live win probability the way Edwin
   expects** (~200ms-readable per live game, quota, simulation games). Top
   unverified assumption in the design.
2. Sketch **N14 fill-response scenarios** so the next Edwin call lands into a
   design; get **E11 + E12 asked** on that call.
3. Receive + read **Edwin's Python files**; agree the **Wednesday-drop
   format**.
4. Keep chasing: gateway cancel build (Hasan), T1 QA account permission,
   T10 test-symbol answer.
5. Open the PR for this branch — the foundation + this session are committed
   but unreviewed.
