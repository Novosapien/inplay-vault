# Valuation Engine (IVS)

> **Component:** [[market-maker/market-maker]]
> **Standard:** [[standards/CTS-001-financial-valuation-standard|CTS-001]] · guide: [[standards/CTS-001-plain-english-guide]]
> **Status:** Formula known (20-07) — numbers and data feed outstanding
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

## Inputs

| Input | Source | Status |
|---|---|---|
| Live win probabilities (this game) | Sport Radar (~20 yrs historical backing) | ⚠️ API broken — 403s, only 8/32 NFL win totals; Cody chasing |
| Season win expectations (remaining games) | Sport Radar futures/win totals | ⚠️ same feed issue |
| $/win revenue value | Edwin | 🔴 owed — Thursday |
| Off-field revenue (EST/ACT) | [[earnings-report/earnings-report]] engine — ½ on-field winner, $250/game volume-allocated | Partially defined there |
| Game events (trigger recompute) | Sport Radar push/poll | Defined in [[architecture/integrations/integrations]] |

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

## Event Weighting & Calibration

- There is **no objective "big play" classification** — Sport Radar data is
  factual but materiality is subjective (a sack on 3rd down ≠ 1st down;
  garbage-time yards mean nothing). A prior Sport Radar content exercise
  produced ~40 qualifying data points, but subjectivity remains. (Source:
  standup 2026-07-20)
- Event weights start as guesses and are **learned from observed market
  reaction** over time — first weeks expected volatile while the model
  calibrates. Win probability does much of this implicitly; explicit trigger
  weights layer on top.
- **Edwin has a prior trigger script** from the ~2-years-ago simulations
  (Kevin believes a full script exists) — the calibration starting point.
- Open: how to value **week zero of college football** (blowout mismatches).

## Interfaces

- **Out:** one ESV per team → published as the Reference Price by
  [[market-maker/systems/market-state]]. Delivery mechanism TBD (bus topic?
  push? cadence?).
- **Never in:** anything from the market side.

## Open Items

Tracked in [[market-maker/open-questions]]: $/win value(s), off-field model
wiring, IPO initial valuations, Sport Radar feed fix, ESV delivery mechanism,
settlement convergence, Edwin's trigger script, week-zero policy.

> Note: CTS-001's Section 3 (the formal valuation math) is **missing from the
> vault copy** — the file ends at §2.33. Edwin's spoken formula above fills the
> gap; request the PDF anyway.
