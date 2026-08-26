---
description: "Design session: retire Edwin's daily file — seed expected wins once, then maintain them from journalled events; the zero-jump absorber and the Saturday build list"
---

# 2026-08-26: the expected-wins pipeline — the daily file retires

> **Who:** George + Claude
> **Type:** design (thread from 08-09: Edwin's handoff decode → same-model
> finding → this pipeline)
> **Refs:** [[standards/gamecast-ev-plain-english-guide]] ·
> `reference/edwin-handoff-2026-08-09/` · `build/valuation.md` ·
> `build/ingestion.md` · artifact "reference-number-pipeline" (claude.ai)

## What we did

- Decoded Edwin's 09-08 handoff bundle (the Gamecast fair-value model) into
  [[standards/gamecast-ev-plain-english-guide]]. Filed the source docs under
  `reference/edwin-handoff-2026-08-09/`.
- Proved the Gamecast model is NOT a new model. Expanded, his `seasonFair` is
  the model we built from his 28-07 email, written as a delta from the IPO
  price. The live leg is ours times a damping dial `M`. Verified numerically
  on his own KC example.
- Found the one new piece: his off-field method (`offShare = 1.0 + pct×0.5`).
  It fails pool conservation — two elite teams claim $3.00 of a $2.50 pool.
- Designed the replacement for the daily file. George's ruling: Edwin cannot
  operate a daily hand-off, so we automate. Full design in the artifact;
  mirrored into [[market-maker/decisions]] 2026-08-26.

## What we learned

- **The daily file's real job is three separable layers.** Absorption
  (arithmetic), near-game repricing (consuming SR), form re-rate (the only
  model). Only the third needs Edwin.
- **The absorber moves the price by exactly $0.00** — proven:
  `contribution(g) = $5·x_g` both before and after the swap.
- **One update rule is the whole season:**
  `new expected wins = old + (result − kickoff probability)`, live version
  replaces result with the live probability.
- **The one-basis rule:** the number absorbed out of expected wins must be
  the number expected wins carried for that game. A game's entry tracks SR's
  pregame number (our pregame polls already fetch it), freezes at kickoff as
  `p_ref`, and is absorbed at that frozen value. This kills N22's basis
  drift.
- **Per-game probabilities for the far tail are not needed.** The price
  reads only the total. The flat split (`expected wins ÷ games remaining`)
  is scaffolding; SR replaces each share before its game kicks off; the
  shares sum to the seed, so expected wins end the season at exactly 0.
- **The journal is the durable store.** Everything after the seed is a fold
  over events already journalled (readings, freezes, `OFFICIAL_RESULT`).
  One new event type total: `EXPECTED_WINS_SEED`, one event, dictionary
  payload, all 170 teams (the `ANCHOR_SEED` shape).
- **The Gamecast's variability mechanisms** (re-rate jitter, injury draws,
  ε noise) are a third instance of manufactured price movement — evidence
  for E34, alongside E30.
- Cross-checks found in Edwin's docs: the KC worked example points the wrong
  way (share is DOWN $5.01 from its implied IPO, not up); `offShare` range
  stated two ways (1.0–1.5 coded vs 1.0–1.9 claimed); star values disagree
  between his two documents; the $5.25 forward coefficient is unexplained.

## What went wrong / got stuck

- The first version of the guide overstated the difference between the
  Gamecast and our engine. George's challenge ("this looks no different")
  was correct; the algebra confirmed it.
- This note covers a thread that ran 09-08 → 26-08 without logging. Too
  long — decisions made mid-thread (the automation ruling) sat unrecorded
  while the questions board moved underneath them.

## Decisions made *(mirrored into [[market-maker/decisions]])*

- ✅ Retire the daily file. Seed expected wins once from the July win-totals
  snapshot (de-vig per Edwin's 28-07 method, σ_mkt 2.7/2.2). Maintain by
  the absorber. George: "we're gonna have to automate it."
- ✅ The July snapshot is acceptable as the seed. Fresh is better; not
  blocking.
- ✅ One new event type: `EXPECTED_WINS_SEED`, one event, dict payload.
  Expected wins are derived state — seed + fold over the journal.
- ✅ Flat split for unpriced games, swapped for SR's number when SR prices
  each game. Deterministic, no internal model.
- 🟡 Layer 3 (form re-rate of the far tail) deferred behind Edwin's
  one-time blessing.

## Questions opened / closed *(mirrored into [[market-maker/open-questions]])*

- **N18 closed** — compute, mechanically; the model layer deferred.
- **N19 closed** — dies: there is no daily file to hand off.
- **N22 residual closed** — one basis; the drift cannot occur.
- **N23 closed** — the event type is `EXPECTED_WINS_SEED`; nothing else.
- **E34 updated** — Gamecast bundle logged as third corroboration.
- **E51 opened** — Edwin's one-time blessing: pipeline ownership, snapshot
  provenance (NCAA rows' source unconfirmed), and the three off-field asks
  (pool conservation, range, college band).

## Next

- Build, in order: (1) seed event + bucket write + de-vig run on the July
  file · (2) the fold (seed + readings + results → expected wins) ·
  (3) rewire `stand_the_book` · (4) regression: zero-jump table, replay
  equality, correction path. ⚠ Games go live Saturday 29-08.
