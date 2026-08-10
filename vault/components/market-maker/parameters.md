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
| `probability poll interval` | How often the MM polls SR's probabilities endpoint (it never rides in the play-by-play payload) | **Start at 500ms in-game**, tune up or down. Slower outside games but **still polled** — the taker makes markets 24/7. ⚠ Supersedes George's 27-07 proposal of 2s, which was quota-driven; quota is no longer a constraint | ✅ 03-08 | Edwin + Cody, 03-08 |
| `next-game probability latency` | Delay before a new game's probability is available | **~15 min after the previous game ends**, typically faster. Derived from the posted odds line; the prior feed value carries in the gap | ✅ 03-08 | Cody, 03-08 |
| `RP formula (restated)` | Full reference-price expression | `RP = ((P(win now) − P(win at kickoff)) + E[remaining wins]) × $5 + off-field`. The in-game term is a **delta from kickoff**, not the raw probability | ✅ 03-08 | George, 03-08 |
| `stale-input response` | What happens when a valuation input dies | **Widen the bid/ask, do not cancel** (Edwin: "if I'm relying on say 20 inputs and one of them's down, my width of the bid ask automatically goes wide"). RP still published from fallbacks, bounded so it can't post something destructive | ✅ shape 03-08 · thresholds 🔴 | Edwin + George, 03-08 (fills N3) |
| `volatility half-life` | Decay constant in the spread-width equation (width comes from the volatility number, not a lookup table) | George floated **~20s**; **Edwin did not confirm** ("I don't know if that's right") | 🔴 TBD — **E21** | 03-08 |
| `own probability model` | Plan-B replacement for SR probabilities | Traditional ML model trained on **NFLverse** (all NFL data since 1999). **Not before launch** (George). Edwin taking a shot at a rudimentary interim model. Valued as proprietary IP and a licensable price feed | 🟡 direction agreed · not v1 | 27-07 · 31-07 |

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

⚠ **Re-based 31-07 / 03-08.** The 15-07 "MM warehouses unsold float in ~50k
clips" model is superseded by the two-MPID structure: the **broker dealer**
holds the whole issuance and sells it; the **taker** buys it. The MM (maker)
does not participate in the primary at all.

| Parameter | Meaning | Value | Status | Source |
|---|---|---|---|---|
| `primary issuance per team` | Shares loaded into the broker-dealer MPID | **1,000,000** per team company, **both** NFL and NCAA (Edwin overrode the earlier 900k NFL / 1M NCAA split; unsold shares simply aren't sold) | ✅ 03-08 | Edwin + Troy |
| `taker IPO target` | Shares the taker buys per team in the primary | **≥600,000** of the 1,000,000, expressed as a **range** (~600–650k), never an exact figure | ✅ floor 03-08 · exact range 🔴 **E22** | Edwin + Troy |
| `taker purchase pattern` | How the taker spaces its primary buying | Randomised **size** and randomised **heartbeat** inside Edwin-supplied share ranges and time blocks. Explicitly **not** participation-weighted in v1 | ✅ 31-07 | Edwin |
| `taker time blocks` | The scheduling windows the randomiser runs inside | Owed by Edwin | 🔴 TBD — **E22** | 31-07 |
| `NCAA primary window` | Length of the NCAA primary offering | **5 days**, all teams open at once | ✅ 31-07 | Troy |
| `NFL primary window` | Length of the NFL primary offering | **2 days** | ✅ 31-07 | Edwin |
| `treasury holdback` | Shares retained rather than offered | Float and public offering are two different numbers; remainder held in treasury as in production. Modelled against a ~**$75M** cap | 🟡 03-08 | Troy + Edwin |
| `price freeze lead time` | How long before IPO prices lock | **3 days.** tZERO make prices static once the IPO price is set, which blocks simulated trading — so publish early, freeze late. Roster changes, injuries and suspensions in the gap materially move price | ✅ 31-07 (**T14** to confirm with tZERO) | Edwin |
| ~~`max clip`~~ | Largest single warehouse order | ~50k shares | ✂ superseded 03-08 | 15-07 |
| ~~`fill guarantee`~~ | Share of float MM consumes if unsold | ~35% (up to 50%?) | ✂ superseded by the taker's ≥60% mandate | 15-07 |

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
