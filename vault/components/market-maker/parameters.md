# Market Maker — Parameters Registry

> **Component:** [[market-maker/market-maker]]
> **Purpose:** Every tunable number in the machine, in one place. This becomes
> the config file. Statuses: ✅ confirmed · 🟡 proposed/indicative · 🔴 TBD.
> Symbols cross-referenced in [[market-maker/glossary]].

---

## ⭐ v1.3 Build Spec registry (24-07) — THE authoritative set

The v1.3 spec's Configuration Dictionary (§12.2) supersedes the sections
below for implementation. ✅ = spec-fixed · 🟡 ▸ = build as given, value
pending InPlay approval (spec Ch 14-A) · 🔴 = no default, external closure
(spec §12.3). Rows tagged **E17/E18** sit inside an open conflict.

| Parameter | Value | Status | Spec § |
|---|---|---|---|
| Tick size | $0.01 | ✅ | 5.3 |
| Spread — Stable / Active / Defensive | $0.10 / $0.20 / $0.40 | ✅ | 5.2 |
| Quote levels — Stable / Active / Defensive | 3 / 2 / 1 | ✅ | 5.2 |
| Ladder offsets — Stable · Active | ±$0.05, ±$0.10 · ±$0.10 | 🟡 ▸ | 5.6 |
| Base quantities — Stable L1/L2/L3 · Active · Defensive | 10,000/7,500/5,000 · 7,500/5,000 · 5,000 | 🟡 ▸ | 5.7.1 |
| Inventory skew S · cap M | $1.00 · $0.25 | 🟡 ▸ | 4.5 |
| Pending-exposure weight · EPR clamp · modifier clamp | 0.50 · ±0.50 · 0.50–1.50 | ✅ | 4.4, 5.7.2 |
| Quantity variation · increment / min / max | ±25% (seeded SHA-256, fixture verified) · 500 / 1,000 / 15,000 sh | ✅ | 5.7.3 |
| Replenishment threshold · delay | 50% of target · 15 s | 🟡 ▸ **E17** | 5.9 |
| Material IA change · material qty change | $0.005 · 500 sh | ✅ | 5.8 |
| Public deviation threshold | max($0.50, 10% × RP) | 🟡 ▸ | 5.5 |
| Price bounds | min $0.01 · max = MEV (season-open NFL $127.50) | ✅ | 5.4 |
| Valuation sweep · max interval | 2.0 s · 2.5 s | ✅ **E18** | 3.1.4 |
| Live freshness bands | 5 / 10 / 20 s | ✅ **E18** | 3.3.1 |
| Pregame freshness bands | 24 h / 6 h / 60 min / 15 min | ✅ | 3.3.2 |
| Status + Market-State promotion dwells | 10 s each | 🟡 ▸ | 3.4.1, 6.4.1 |
| Confidence deduction schedule | table §3.5 | 🟡 ▸ | 3.5 |
| Game values — win / tie | $5.00 / $2.50 | ✅ | 3.1.2 |
| Probability sum bands | ±1e-6 accept · ±1% normalize · else reject | ✅ | 3.2.1 |
| MM IPO allocation | floor(85% × unsold shares) | ✅ | 9.2 |
| Off-field pool / window / cadence / zero-volume split | $2.50 per game · prior-final→final · weekly post-MNF (NFL), post-week-final (NCAA) · $1.25/$1.25 | ✅ | 3.6 |
| Popularity model — BDI clamp · blend horizon · capture clamp | 0.10–10.0 · 4 publications · 0.20–0.80 | 🟡 ▸ | 3.6.5 |
| Security universe | 32 NFL + 138 NCAA D-I = 170 | ✅ | 2.5 |
| Venue timeouts / retries / rate limits / book age / clock skew / retention / load profile / RTO | — no defaults; config only | 🔴 §12.3 | 12.3 |

### ⭐ Edwin's 28-07 answers + IPO Supplement A v1.3 (24-07) — authoritative

Sources: [[standards/MM-edwin-answers-28-07|Edwin's email, 28-07]] ·
`standards/IPO_Pricing_Subscription_Supplement_v1.3.docx` ·
`reference/` (his engine as code). Supplement provisions carry his own
[DECIDED] / [RECOMMENDED] / [OPEN] markers.

| Parameter | Value | Status | Source |
|---|---|---|---|
| **σ_mkt** — de-vig dispersion | **2.7 NFL · 2.2 NCAA** | ✅ confirmed | email item 1 + `engine.py` Parameters tab. ⚠ Replaces the unapproved 2.0–2.5 range; the ONLY sigma used to extract a mean from a posted line |
| `sigma` (feed field) | schedule dispersion √(Σ p(1−p)) | ✅ | a **different object** — never enters the de-vig step |
| Tie settlement | **x_g = 0.5 → $2.50/share** | ✅ | email item 5 (SDMM-1) |
| NFL tie rate | ~0.4 % of games *(email/`ipo.py`)* vs **0.08 per team-season** *(`engine.py`)* | ⚠ **conflict — E21** | $0.17 vs $0.20 per share |
| Reference-number feed cadence | **daily 06:00 ET**, heartbeat even when unchanged | ✅ | email items 3–4 |
| Missing feed file | **alarm, never a shrug**; hold last value | ✅ | email item 4 |
| Correction protocol | same `effective_time`, bumped `revision`, `is_correction=true` | ✅ | email item 4 |
| Popularity weights | **0.6 Brand · 0.4 PerfIndex** | ✅ | email item 6, Supplement §2.1 |
| Capture clamp | **[0.20, 0.80]** | ✅ | matches spec §3.6.5 |
| IPO discount band | **1 % – 3 %**, normalised on contested off-field share **per league** | ✅ [DECIDED] | Supplement §2.2 |
| No-discount rule | guaranteed accrual **> 20 % of EV** → lists at full EV | ✅ [DECIDED] | Supplement §2.2 |
| RP seeding at listing | **IPO EV**, not the listed price | ✅ email 28-07 | ⚠ Supplement §8 had this **[OPEN]** and warns every discounted name gaps **1–3 %** at the open with the MM as counterparty |
| Base allotment | **50,000 sh / team / round** | ✅ [DECIDED] | Supplement §1 — a per-round quantity, **not** a float cap |
| Guaranteed primary float after Round 10 | **500,000 sh / team** | ✅ [DECIDED] | Supplement §5. ⚠ **A floor on shares SOLD — not the issued count. §4.3 still has no number: E22** |
| MM max opening inventory | **85,000,000 sh (~$4.26 bn notional)** | ✅ [DECIDED] | Supplement §5 — ⚠ conflicts with spec §9.2's `floor(0.85 × Unsold)`: **E20** |
| Per-participant cap | **2,500 sh / team / round**; MM exempt | ✅ [DECIDED] | Supplement §5 |
| Offering window | **1 minute max per team**, sequential, alphabetical R1 | ✅ [DECIDED] | Supplement §3 |
| Termination | first complete round ≥ 11 with participant fills **< 1 %** of available allotment; MM fills excluded | ✅ [DECIDED] | Supplement §4 |
| **NCAA price freeze** | **Wed 19 Aug 2026** | ✅ [DECIDED] | Supplement §3.1 |
| **NCAA offering** | **Sat 22 Aug – Fri 28 Aug 2026** | ✅ [DECIDED] | Supplement §3.1 |
| **NFL price freeze** | **Wed 2 Sep 2026** | ✅ [DECIDED] | Supplement §3.2 |
| **NFL offering** | **Sat 5 Sep 2026** | ✅ [DECIDED] | Supplement §3.2 |
| **Shares per team at IPO** | **875,000 NFL · 1,000,000 NCAA** | ✅ **confirmed 29-07** | Edwin email. Different per league — "identical share count" means identical *within* a league. Total on offer **166,000,000 shares** |
| Total value at IPO EV / listed | $8.45 bn / $8.27 bn · discount $180.7 m (2.14%) | ✅ derived 29-07 | `reference/ipo-prices-170.csv` × the share counts above |
| ~~float basis for λ — 5 M~~ | **retired** | ✅ resolved 29-07 | The 875 k in the old note was the NFL share count. The 5 M figure had no source and is withdrawn |
| Issued vs treasury split | — | 🟡 **E22 reduced** | We have shares *on offer*. §4.3 wants issued minus treasury. Confirm they are the same number |
| IPO listed-price rounding | **$0.01 tick** *(workbook)* vs **full precision** *(email)* | ⚠ **conflict — ask 29-07** | Parameters sheet says "rounding increment for listed IPO price"; all 170 listed prices are exact pennies. The email says "no rounding anywhere" |
| NFL expected ties per team | **0.08** → $0.20 a share | ✅ confirmed 29-07 | Workbook Parameters sheet. Settles E21: `engine.py` is right, `inplay_feed/ipo.py` is wrong ($0.17) |
| IPO discount method | normalised contested off-field share, **per league**, into 1–3 % | ✅ confirmed 29-07 | Workbook Parameters sheet. Settles E21: `engine.py` is right, `ipo.py`'s flat scale is wrong |
| Bradley-Terry gamma | 1 | ✅ | Workbook Parameters sheet |

### Ingestion + venue-interface numbers (not in the spec — ours or the venue's)

| Parameter | Meaning | Value | Status | Source |
|---|---|---|---|---|
| `probability poll interval` | How often the poller calls SR per live game | **~2 s** — matches the measured median update gap | 🟡 evidence-backed, E18 open | 24-07 measurement |
| `SR update cadence (observed)` | How often SR's probability actually changes in a live game | median **4 s** · mean 11.5 s · p90 28 s · 64 % ≤5 s · 1,089 updates/game | ✅ measured | Chiefs–Ravens capture 24-07 |
| `SR acquisition lag` | SR's own delay before publishing | ~5–15 s (media tier) **or** fast (betting tier) — **contradictory sources** | 🔴 S9 — measure in August | SR service research vs Cody |
| `ClOrdID` | Client order id format | ≤ **20 chars**, **no leading zeroes**, + gateway's MM prefix; replace/cancel carry **two** ids (new + orig), each ≤20 | ✅ venue-verified 24-07 | tZERO OE spec v2.2 |
| `MaxOrdRate` | tZERO's per-account message allowance | — **not in any document**; per-account OMS setting | 🔴 T2 — ask with T1 | tZERO OE spec (absent) |
| `gateway MM governor` | Token-bucket throttle on the MM namespace | 50 msg/s — **Hasan's placeholder**, not a venue limit | 🟡 placeholder, cert item | Gateway 24-07 |
| `dead-man window` | Heartbeat silence before the gateway sweeps our book | 4 s (placeholder) + latched sweep | 🟡 **ours to set** (N15) | Gateway 24-07 |

---

> ⚠️ **Everything below this line predates the v1.3 spec (24-07).** Kept for
> history and for numbers the spec doesn't cover (capacity, IPO warehousing,
> synthetic MO). Where a row conflicts with the registry above, the registry
> wins.

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
| `buying power` | MM capital in T0 | ~$100M–$100B ("never a limit") — set via `DTBPo` on account creation | ✅ decided, exact number 🟡 | 20-07 (Edwin/Troy) · OMS spec 22-07 |
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

✂ **Superseded 24-07:** the merged table is the v1.3 spec's §5.2
(Stable/Active/Defensive/Suspended — see the registry above). N2 resolved.

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
