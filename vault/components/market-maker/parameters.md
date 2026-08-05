---
description: "Registry of every tunable MM number with value, status and source — valuation, sessions, quoting, supervision, SNT-1 defaults and profile multipliers"
---

# Market Maker — Parameters Registry

> **Component:** [[market-maker/market-maker]]
> **Purpose:** Every tunable number in the machine, in one place. This becomes
> the config file. Statuses: ✅ confirmed · 🟡 proposed/indicative · 🔴 TBD.
> Symbols cross-referenced in [[market-maker/glossary]].

---

## Valuation

| Parameter | Meaning | Value | Status | Source |
|---|---|---|---|---|
| `$/win` | Revenue value of one expected win (on-field) | **$5.00** — `ESV = OffField + $5.00 × E[wins]`, verified across all 32 NFL sheet rows | 🟡 decoded 22-07, Edwin sign-off pending (E1) | Client NFL IPO price sheet |
| `off-field model` | Off-field term in ESV | **Edwin's popularity index** — ~$14–30/team (Dallas ~$30 · low ~$14), static at start, already inside the NFL IPO prices, refreshed in the Wednesday drop. (EST/ACT earnings interplay deferred) | ✅ 23-07 | MM call 23-07 |
| `remaining-wins source` | Where E[remaining wins] comes from | **InPlay internal, weekly** (SR doesn't do season totals); Edwin automating; delivered Wednesdays | ✅ 23-07 | MM call 23-07 |
| `weekly data drop` | Off-field metric + remaining-game win probabilities delivery | Every **Wednesday**, plugged into the algo | ✅ 23-07 | MM call 23-07 |
| `initial valuation` | Opening ESV per team at IPO | NFL RP₀ sheet exists (Rams $81.93 … Cardinals $32.01); NCAA equivalent owed (E12) | 🟡 NFL known / 🔴 NCAA | Client sheet · Edwin (E3) |
| `long capacity` | Shares available for longs, per team | **5,000,000** | ✅ 21-07 (recorded 22-07) | George / client |
| `short capacity` | Shares available for shorts, per team | **5,000,000** (QA's 1,000-share reserve = test config only) | ✅ 21-07 (recorded 22-07) | George / client |
| `float basis for λ` | Denominator for inventory-as-%-of-float (skew gain) | ⚠ 5M vs the sheet's 875k changes effective gain ~5.7× — pick one and re-base λ | 🔴 reconcile — **E14, Thursday** | decisions 22-07 |
| `price band (valuation)` | Hard floor/cap on ESV/RP | floor 1 tick · cap **$127.50** | 🟡 sheet-derived | Client sheet 22-07 |
| `event trigger weights` | Per-event price impact | ✂ **Not needed in v1** — the in-game driver is SR's live win probability, pulled directly (E15 resolved) | ✂ 23-07 | MM call 23-07 |
| `recompute cadence` | Valuation update rhythm | **Bifurcated by game state:** live games ~200ms per call ("a second's too long") · non-live every 30–60s · earnings windows (Tue NFL / Wed NCAA) all ~170 symbols for ~5 min | ✅ 23-07 | MM call 23-07 |

## Market state / sessions

| Parameter | Meaning | Value | Status | Source |
|---|---|---|---|---|
| `sessions` | Liquidity session set | in-game / around-game / overnight | ✅ | 20-07 (Troy) |
| `overnight spread` | Deliberate wide spread outside games | ~$2.5–5 | 🟡 indicative | 20-07 (Troy) |
| `session boundaries` | When each session starts/ends | — | 🔴 TBD | N4 |
| `condition classes` | Health classifier outputs | Normal / Degraded / Protective / Recovery / Emergency | ✅ (doc) | CTS-002 |
| `classifier thresholds` | Staleness/latency limits per class | — | 🔴 TBD | N3 |
| `RP publication` | Reference price identity | RP = ESV (mid) · frozen on feed failure | ✅ | CTS-002 + 20-07 |

## Quoting engine

| Parameter | Meaning | Value | Status | Source |
|---|---|---|---|---|
| `buying power` | MM capital in tZERO | ~$100M–$100B ("never a limit") — set via `DTBPo` on account creation | ✅ decided, exact number 🟡 | 20-07 (Edwin/Troy) · OMS spec 22-07 |
| `refresh rate` | Quoting cadence | **Bifurcated (supersedes flat 5–10×/sec):** live games ~200ms · non-live 30–60s · earnings burst ~5 min all symbols | ✅ 23-07 | MM call 23-07 |
| `tick size` | Min price increment | **$0.01** | ✅ | Venue-verified 22-07 |
| `base spread` | Default half-spread per side (per profile) | Tick × S multiplier | 🔴 base TBD | PTS-001 §6.6.1 |
| `profile multipliers` | (S, D, Q, F, I) per pricing profile | table below | ✅ (doc defaults) | PTS-001 §6.6.1 |
| `λ (inventory sensitivity)` | Feedback gain: skew = λ × inventory% | λ_base 🔴 × I multiplier ✅ | 🔴 base TBD | PTS-001 |
| `ladder levels N` | Price levels per side | — | 🔴 TBD | E5 |
| `ladder spacing Δ` | Gap between levels (per side) | — | 🔴 TBD | E5 |
| `depth weights W` | Budget share per level (Σ=1) | front-loaded shape assumed | 🟡 | PTS-001 |
| `displayed size` | Size per team per side | — | 🔴 TBD (replaces descoped Ch 5 allocation) | E5 |
| `randomization bounds` | Quantity jitter limits (seeded) | **Quantities only** (esp. top-of-book size); **price is never randomized** (23-07). Bounds themselves still TBD | 🟡 shape ✅ · bounds 🔴 | MM call 23-07 · E5 |
| `aggressive-order bounds` | Limits on market-moving randomized orders | — | 🔴 TBD | E8 |
| `quote lifetimes` | Min/max age, expiry, aging variation | ✂ **Moot** — orders rest until fully gone (no top-ups, no aging); on price move: cancel + repost remaining qty; reload at top of book after a full fill | ✂ 23-07 | MM call 23-07 (N10 resolved) |
| `inventory ratios` | Target / warning / max (% of float) | warn 5% · max 10% — denominator blocked on E14 | 🟡 proposed | decision-cycle-reference |
| `validation retry cap` | Max reconstruction attempts per cycle before defensive fallback | 3 | 🟡 proposed 22-07 | PTS-001 §6.11 deferral |

### Pricing-profile multiplier table (PTS-001 §6.6.1 — the doc's only hard numbers)

| Profile | S (spread) | D (depth) | Q (size) | F (refresh) | I (inv. sens.) |
|---|---|---|---|---|---|
| Stable | 1.00 | 1.50 | 1.50 | 1.00 | 0.50 |
| Active | 1.50 | 1.00 | 1.00 | 0.50 | 1.00 |
| Defensive | 2.50 | 0.60 | 0.60 | 1.50 | 1.75 |
| Recovery | 1.75 | 1.00 | 0.90 | 1.00 | 2.50 |
| Liq. Preservation | 3.00 | 0.50 | 0.50 | 1.25 | 3.50 |
| Protective | 5.00 | 0.25 | 0.25 | restricted | 5.00 |

⚠ Needs merging with CTS-002's profile menu (Balanced/Emergency) into one
table → N2 in [[market-maker/open-questions]].

## Supervision

| Parameter | Meaning | Value | Status | Source |
|---|---|---|---|---|
| `band width` | Price corridor around RP | ~±30% | 🟡 "or whatever we come up with" | 20-07 (Edwin) |
| `band enforcement point` | Order entry vs execution vs both | — | 🔴 TBD | T3 |
| `bust criteria + SLA` | What qualifies, who triggers, how fast | — | 🔴 TBD | T4 |
| `halt triggers` | What halts a team's market | feed death, valuation freeze, extreme volatility (candidates) | 🔴 TBD | T5 |

## Synthetic market order

| Parameter | Meaning | Value | Status | Source |
|---|---|---|---|---|
| `N levels through` | How far a synthetic market order prices through | — | 🔴 TBD | N5 (Troy assisting) |
| `fallback walk` | Cancel-replace chase if unfilled | proposed: ~5s interval, time-bounded | 🟡 George's proposal | 20-07 |

## IPO warehousing

| Parameter | Meaning | Value | Status | Source |
|---|---|---|---|---|
| `max clip` | Largest single warehouse order | ~50k shares | 🟡 | 15-07 |
| `fill guarantee` | Share of float MM consumes if unsold | ~35% (up to 50%?) | 🟡 | 15-07 |

## SNT-1 (Synthetic Noise Taker)

All from Edwin's v1.0 reference implementation (30-07). Reference-impl defaults, so 🟡 proposed; `base_orders_per_hour` and the loss budget are the two levers Edwin expects to tune after seeing real books. Full spec: [[market-maker/systems/synthetic-noise-taker]]; code: `sources/snt1_noise_taker.py`.

| Parameter | Meaning | Value | Status | Source |
|---|---|---|---|---|
| `base_orders_per_hour` | Arrival rate, OVERNIGHT, weight-1.0 team | **9.0** | 🟡 **lever** (tune on real books) | SNT-1 v1.0 |
| `state_multiplier` | Intensity by activity state | OVERNIGHT 1x · PRE_KICKOFF 6x · **LIVE 75x** · POST 4x | 🟡 | SNT-1 v1.0 |
| `team_weight` | Per-team activity weight | range **0.25 to 4.0**, from the EAV / popularity model; default 1.0 | 🟡 (feed TBD) | SNT-1 v1.0 |
| `size_lognorm_mu` / `sigma` | Log-normal size params | mu **3.4** (median ~30) · sigma **0.9** | 🟡 | SNT-1 v1.0 |
| `min_size` / `max_size` | Size clip | **5** / **400** shares | 🟡 | SNT-1 v1.0 |
| `sweep_probability` | Share of orders that sweep (else at-touch IOC) | **0.10** | 🟡 | SNT-1 v1.0 |
| `max_impact_ticks` | Sweep limit cap through the touch | **3 ticks** | 🟡 | SNT-1 v1.0 |
| `max_fraction_of_touch` | At-touch qty cap vs displayed | **0.5** | 🟡 | SNT-1 v1.0 |
| `daily_loss_budget_per_team` | Spread-subsidy governor (cost-vs-mid) | **$100,000** / team / session | 🟡 **lever** | SNT-1 v1.0 |
| `max_spread_ticks_to_trade` | Skip books wider than this | **8 ticks** | 🟡 | SNT-1 v1.0 |
| `inventory_soft_cap` | Absolute inventory before flatten bias | **1,500 shares** | 🟡 | SNT-1 v1.0 |
| `flatten_bias` | P(trade reduces inventory) above the cap | **0.80** | 🟡 | SNT-1 v1.0 |
| `profit_take_bias_max` | Max P(flatten) when well in profit | **0.65** (from 0.50 base) | 🟡 | SNT-1 v1.0 |
| `profit_take_full_ticks` | Profit/share for full tilt | **10 ticks** | 🟡 | SNT-1 v1.0 |
| `tick` | Min price increment | **$0.01** | ✅ | venue-verified (matches MM) |
| `rng_seed` | Seed for reproducible sims | 20260729 | 🟡 (sim only) | SNT-1 v1.0 |

## External suggestions — platform doc 22-07 (NOT adopted; inputs to our design, see N9)

The platform team's `sdmm.py` prototype proposed defaults. Noted here because
several **converge with our own decision-cycle-reference proposals** — useful
corroboration, but per the 22-07 filter these bind nothing:

| Parameter | Their proposal | Our proposal ([[market-maker/systems/decision-cycle-reference]]) | Converge? |
|---|---|---|---|
| Base half-spread | 2 ticks | 2 ticks (`spread_ticks`) | ✅ same |
| Ladder spacing Δ | 3 ticks | 3 ticks (`spacing_ticks`) | ✅ same |
| Levels per side | 3 | ~4 (`n_base`, profile-scaled 2–6) | ~close |
| Side budget | 6,000 sh | 5,000 sh (`l_base`) | ~close |
| Depth weights | front-loaded 2^k | front-loaded 0.55^k | ~close |
| Inventory gain λ | 1500 ¢ per 100% float | 0.5 × price per 100% float (different units — reconcile) | ⚠ compare |
| Cadence | 200 ms full per-team replace on RP change | 200 ms heartbeat + event triggers, diff-based publish | ⚠ differs (full-replace vs diff) |
