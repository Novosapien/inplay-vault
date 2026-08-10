---
description: "The valuation engine (IVS) — computes each team's ESV from live win probability, remaining wins and off-field value, with the resolved 23-07 input table"
---

# Valuation Engine (IVS)

> **Component:** [[market-maker/market-maker]]
> **Standard:** [[standards/CTS-001-financial-valuation-standard|CTS-001]] · guide: [[standards/CTS-001-plain-english-guide]]
> **Status:** Inputs resolved (23-07 MM call) — $5/win sign-off (E1), settlement (E11) and the Sport Radar fit check (S5) outstanding
> **One-liner:** Continuously answers "what is one share of this team worth right now?" — one number (ESV) per team, updated per play during live games.

---

## Purpose

Every team market needs a fair-value anchor before anyone can quote or trade
it. The valuation engine computes the **Expected Settlement Value (ESV)** —
the best estimate of what a share pays out at season end — continuously, for
the 170-symbol universe (32 NFL + 138 NCAA; NCAA secondary scope open — E12).

**22-07 breakthrough:** the client's real NFL IPO sheet decodes to
**`ESV = OffField + $5.00 × E[wins]`** — additive, verified across all 32
rows. $/win = $5.00 (pending sign-off). Float 875k/team; cap $127.50.
**Settlement definition (E11) is now the most important open question** — what
actually pays at season end determines whether ESV is a clean expectation.

The core law: **value and price are separate.** This engine computes value
from win probabilities and revenue economics only. Market prices, order flow,
sentiment, and MM inventory may never feed back into it.

## The Formula (Edwin, 20-07 — supersedes the doc's ceremony)

```
share price = on-field + off-field

on-field  = P(win THIS game) × $/win            ← live win probability, this game
          + E[wins, rest of season] × $/win     ← expected remaining wins, all other games

off-field = marketing / advertising revenue component
            (EST vs ACT mechanics — see earnings-report component)
```

- Two main price drivers: the probability for **the game happening right
  now**, and the probability across **all other remaining games combined** →
  together the on-field revenue; add **off-field revenue** → the share price.
  Off-field is not guaranteed per game, which keeps the market interpretive
  and tradeable. (Source: standup 2026-07-20)
- IPO anchor from the vision doc: e.g. 5 expected wins × $5 = $25/share, plus
  off-field.

## Inputs (resolved 23-07 — see [[market-maker/decisions]])

| Input | Source | Status |
|---|---|---|
| Live win probability (this game) | **Sport Radar, pulled directly** during live games (~200ms calls) — the event is already priced into the probability; no own event weights in v1 | ✅ model set · ⚠️ API broken (S1) · fit check owed (S5) |
| Expected remaining wins | **InPlay internal, produced weekly** (SR doesn't do season totals); Edwin helping automate; arrives in the **Wednesday drop** | ✅ 23-07 |
| $/win revenue value | $5.00 decoded from the client sheet | 🟡 sign-off pending (E1) |
| Off-field value | **Edwin's popularity index** — ~$14–30/team, static at start, already in the NFL IPO prices; refreshed in the Wednesday drop | ✅ 23-07 (EST/ACT interplay deferred) |
| The Wednesday data drop | InPlay → us, every Wednesday: updated off-field metric + remaining-game win probabilities, plugged into the algo | ✅ cadence agreed · format TBD |

## Behaviour

- **Event-driven, not clock-driven.** Recompute when something material
  happens — per play during live games (touchdown → up, turnover → down).
  Between games, updates arrive via revised win probabilities for future
  matchups.
- **Markets are truly isolated intragame.** Events in other games do not move
  this market during play; each game is effectively a pairs trade (two team
  companies on the probability of capturing the on-field revenue).
  Rankings/tiebreakers don't feed pricing. (Source: standup 2026-07-20)
- **Deterministic + explainable.** Same inputs → same ESV; every ESV
  decomposable into (this game / rest of season / off-field). Keep full
  lineage (every value reconstructible) — cheap if event-sourced from day one.
- **Failure mode:** if the probability feed dies, the ESV freezes at last
  valid value (the market-state layer handles the frozen publication — see
  [[market-maker/systems/market-state]]).

## Event Weighting — descoped for v1 (23-07)

- **v1 has no event-weight model.** Edwin: "you don't have to create it —
  you just pull Sport Radar's probability in." The in-game price channel is
  SR's live win probability, which already reflects every play in context
  (score, quarter, time left — a garbage-time score barely moves it; an
  early-game injury moves it a lot).
- Out-of-game events (injury, trade, draft) flow through the **weekly
  remaining-wins update** and the popularity index, not through live
  triggers.
- **Edwin is sending the original MM simulation Python files** ("functional,
  not a heavy lift") — reference material, not a dependency (E4 in motion).
- Still open: how to value **week zero of college football** (blowout
  mismatches, E6) — moot for launch if E12 lands NFL-only.

## Interfaces

- **Out:** one ESV per team → published as the Reference Price by
  [[market-maker/systems/market-state]]. Delivery mechanism TBD (bus topic?
  push? cadence?).
- **Never in:** anything from the market side.

## Open Items

Tracked in [[market-maker/open-questions]]: **E11 settlement** (what a share
actually pays — defines what ESV means), E1 $/win sign-off, E3 initial
valuations, S1 feed fix, **S5 Sport Radar fit** (can they serve live
probability at ~200ms-call cadence + simulation games?), S4 sportsbook
parity, N1 ESV delivery mechanism, E6 week zero, Wednesday-drop file format.

> Note: CTS-001's Section 3 (the formal valuation math) is **missing from the
> vault copy** — the file ends at §2.33. Edwin's spoken formula above fills the
> gap; request the PDF anyway.
