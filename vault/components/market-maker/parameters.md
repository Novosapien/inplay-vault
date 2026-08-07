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
| **Shares outstanding per team** | **900,000 NFL · 1,000,000 NCAA** | ✅ **gospel 29-07** | IPO Requirements v2 §1.2, §5.1. **Supersedes the 875,000** in Edwin's email of the same day |
| Shares actually offered | 18 rounds × 50,000 = **900,000** per team | ✅ v2 §1.2 | Exactly the NFL float. Leaves **100,000 NCAA shares per team unoffered** — issued or treasury? → **N21** |
| Shares available for shorting | **900,000 NFL · 1,000,000 NCAA** — the full float | ✅ v2 §1.2, §5.2 | NEW in v2. Cap is total-or-per-participant unknown → **E26** |
| Mandate rounds | **10 or 16 or 18** | 🔴 **conflict — E24** | v2 §4 / §3 / §2.2. Max MM inventory 85 M / 136 M / 153 M shares |
| NCAA offering | opens **22 Aug** 1pm ET · closes **26 or 28 Aug** | 🔴 close date conflicts — E25 | v2 §1.1 vs §2.1 |
| **NCAA secondary trading** | **26 or 27 Aug** 9:30am ET | 🔴 **conflict — E25. THE DEADLINE** | v2 §5.2 vs §1.1 |
| NFL offering | **5–6 Sep**, 1–6pm ET, rounds 1-9 then 10-18 | ✅ v2 §1.1, §2.2 | |
| **NFL secondary trading** | **7 Sep** 9:30am ET | ✅ v2 §1.1, §5.2 | |
| Total value at IPO EV / listed | $8.45 bn / $8.27 bn · discount $180.7 m (2.14%) | ✅ derived 29-07 | `reference/ipo-prices-170.csv` × the share counts above |
| ~~float basis for λ — 5 M~~ | **retired** | ✅ resolved 29-07 | The 875 k in the old note was the NFL share count. The 5 M figure had no source and is withdrawn |
| Issued vs treasury split | — | 🟡 **E22 reduced** | We have shares *on offer*. §4.3 wants issued minus treasury. Confirm they are the same number |
| IPO listed-price rounding | **$0.01 tick** *(workbook)* vs **full precision** *(email)* | ⚠ **conflict — ask 29-07** | Parameters sheet says "rounding increment for listed IPO price"; all 170 listed prices are exact pennies. The email says "no rounding anywhere" |
| NFL expected ties per team | **0.08** → $0.20 a share | ✅ confirmed 29-07 | Workbook Parameters sheet. Settles E21: `engine.py` is right, `inplay_feed/ipo.py` is wrong ($0.17) |
| IPO discount method | normalised contested off-field share, **per league**, into 1–3 % | ✅ confirmed 29-07 | Workbook Parameters sheet. Settles E21: `engine.py` is right, `ipo.py`'s flat scale is wrong |
| Bradley-Terry gamma | 1 | ✅ | Workbook Parameters sheet |
| **Daily feed fields** | `team_id` · `league` · `effective_time` · `revision` · `is_correction` · `expected_remaining_wins` · `sigma` · `games_remaining` · `methodology_version` | ✅ verified 29-07 | `reference/sample_reference_feed_2026-08-29.json`, 170 records |
| **T** (whole-season expected wins) | **not published** — `T = banked wins + expected_remaining_wins` | ✅ we compute it | The feed field is remaining games only; Edwin's formula needs the whole-season basis. Both, deliberately — his definitions block governs |
| **`p_ref(g)`** (pregame probability per game) | **not in the feed** | 🔴 **N22** | We capture Sportradar's last pregame reading at kickoff, or recover it from SR's timeline later. Basis-drift risk vs his Elo/raked numbers |
| Adjustment window | **kickoff → the next T**, not kickoff → the final whistle | ✅ 29-07b | Dropping it at the whistle costs $2.17 on a Chiefs win, then returns it at 06:00 — a sawtooth. Edwin's unit test (c) |
| **Reservation Midpoint floor** | **$0.01** — §5.4's price floor, applied to RM | ✅ 30-07 | §4.6 requires RM inside the §5.4 bounds, and it is load-bearing: `RP $0.10 + IA −$0.25 = −$0.15` without it |
| **Reservation Midpoint ceiling** | **MEV**, per security — season-open NFL $127.50 | ✅ 30-07 | §5.4. Falls as games are played, so it is an argument rather than a constant |
| Position Ratio bounds | **none — deliberately not clamped to ±1** | ✅ 30-07 | Full-float shorting (v2) plus §4.1's no-inventory-limit means PR can exceed 1.0 legitimately → **E26** |
| Skew cap binding point | **25% of float** (M $0.25 ÷ S $1.00) | ⚠ **N20** | We will hold 50–100% after the IPO. Holding the whole float reads identically to holding a quarter |
| **NFL expected-wins conservation** | must sum to **272**; posted lines sum to 275.00, de-vigged 273.95 | 🟡 **N25 — parked** | +$0.30/share, one-directional, ≈$8.6 M across the float. George 30-07: minor, ask when convenient |

### ASMM-1 / SNT-1 (30-07b) — proposed, nothing here is ✅

From `inplay_algo_handoff_george.zip` + the Component Narrative (30-07). Rulings
area by area in [[market-maker/asmm1-adoption-spec]]. His §6 calls these
*"launch settings, not truths"*, fitted to **judged** target tape statistics.

| Parameter | Meaning | Value | Status | Notes |
|---|---|---|---|---|
| `vol_halflife_s` (`h`) | decay of the variance rate | **20 s** | 🟡 his | The volatility estimator's memory |
| `vol_horizon_s` (`H`) | window σ² is scaled to | **30 s** | 🟡 his | ⚠ Applied **once**, in step 5. The A-S risk term is `γσ²(T−t)` and the `(T−t)` is already inside — do not multiply again |
| `var_floor` / `var_ceil` | σ² bounds, ticks² | **0.05 / 400** | 🟡 his | The ceiling binds on any touchdown-sized move |
| `gamma` (`γ`) | risk aversion in the width | **0.02** | 🔴 **E31** | Book-visible → his remit |
| `k` | order-flow intensity; larger → tighter | **1.2** | 🔴 **E31** | |
| `width_const C` | `(2/γ)·ln(1 + γ/k)` | **1.653 ticks** | derived | Constant, because γ and k are. **Compute once at construction** |
| `width_extra` | random widening above the risk floor | **0–3 ticks**, seeded, held for the dwell | 🟡 | Additive, not `max()` — he changed this deliberately so the risk term always shows |
| `width_ref_price` · scale bounds | where `extra` is unscaled | **$65.00** · 0.6–1.6× | 🟡 | Keeps bps spread ~uniform across the price ladder |
| **`width_floor_by_state`** | minimum width, Defensive / Overnight | — | 🔴 **E31** | ⚠ **The gap.** σ² 400 caps the width at ~$0.13 on a $65 team, ever; §5.2 Defensive is $0.40 and overnight was indicated $2.50–$5.00. And a **dead feed produces LOW σ²**, so the equation quotes tight into the §2.3 danger case |
| `levels_range` | levels per side | **3–6**, drawn per dwell | 🟡 adopt | Removes another dependency on the unbuilt classifier |
| `level_step_ticks` | gap between levels | **1–4 ticks**, drawn per dwell | 🟡 adopt | |
| `size_decay` | per-level size multiplier | **0.72** | 🟡 adopt | Extends to any level count, unlike three hard-coded numbers |
| `base_size` | top-of-book size | **10,000 (ours)** — not his 250 | 🟡 ▸ §5.7.1 | His is 40× too small for a book we must distribute |
| size jitter | per-level quantity variation | **§5.7.3 seeded SHA-256** — not his `random.Random` ±35% | ✅ ours | The fixture we reproduced byte-exact; replay depends on it |
| dwell by state | how long a shape holds | LIVE 3–12 s · PRE 8–30 s · POST 10–40 s · OVERNIGHT 20–90 s | 🟡 **gated by N26** | Must not trigger a requote on its own |
| `inv_ref` | his lean denominator | **4,000 sh** | ✂ **rejected** | Keep §4.3's Reference Float. His pins at 12,000 sh, ours at 225,000 |
| `max_reservation_ticks` | his lean cap | **30 ticks ($0.30)** | ✂ n/a | Ours is `M` = $0.25 and the live question is **N20**, not this |
| `live_inv_cap` | one-sided quoting past this | **6,000 sh** | ✂ **rejected** | §4.1: inventory never prevents quoting. Run as shipped = no bid on any book |
| `kill_drawdown` | halt the book on MTM drawdown | **$25,000** | ✂ **rejected** | §1.5 excludes profit, so drawdown is not a signal. §6.3 is the kill switch we need |
| requote throttle | min gap / RP move / inventory move | 2.0 s · 2 ticks · 300 sh | ✅ **already ours** | §5.8's material-change thresholds, better specified |
| **RPV-2 impact** | RP movement per net flow | **10 ticks/1,000 sh** *(HANDOFF §3)* vs **6.0** *(`RPV2Config`)* | ⚠ **conflict** · 🔴 **E30** | Package described as clean-room verified |
| **RPV-2 trend cap** | invented random drift on the anchor | **80 ticks ($0.80)** | 🔴 **E30** | Not information. Build none of it pending his answer |
| `q_norm` clamp | his normalized inventory | **clamped ±1** *(HANDOFF §2 + Narrative)* vs **not clamped** *(code)* | ⚠ **conflict** | Second doc-vs-code disagreement. Clamped is *worse* for us — it would saturate at 4,000 sh exactly |
| `ActivityState` set | market states | **4** *(code)* vs **5, adding DAY** *(Narrative)* | ⚠ **conflict** | Third. Ask which is authoritative |
| SNT-1 `base_orders_per_hour` | arrival intensity, weight-1.0 team | **9/hr**, LIVE **×75** | 🟡 | ≈ 675 orders/hr ≈ **30,000 sh/hr per book** |
| SNT-1 `max_spread_ticks_to_trade` | widest book it will trade | **8 ticks** | 🔴 **E32** | **Narrower than §5.2 Stable's 10 ticks** — as configured it never trades |
| SNT-1 sweep cap | how far through the touch | **2–4 ticks** (v1.1, jittered) | ⚠ | Our ladder spacing is $0.05, so **every order lands on L1 only** → **E17** |
| SNT-1 `inventory_soft_cap` | before the flatten bias | **1,500 sh** | 🔴 **E32** | Exceeds tZERO's **1,000-sh per-security short reserve**, pre-trade enforced |
| SNT-1 `daily_loss_budget_per_team` | spread-cost governor | **$100,000/day** | ⚠ decorative | Burns ~$1,500/hr at LIVE — **cannot bind**, even over 24 h |
| SNT-1 cohort weights | NOISE / MOMENTUM / CONTRARIAN | **0.56 / 0.22 / 0.22** | 🟡 | ⚠ `net_drift_coeff()` exists to **prove the tilts cancel** — so SNT-1 provably exerts **no net directional pressure**, i.e. it cannot distribute the float, by design |
| SNT-1 `FlowImbalance` band | background buy fraction | **42–58%**, pulled to 50% | 🟡 | v1.1 only. Supersedes v1.0's flat 50/50 |
| distribution size asymmetry | offer-side size / levels vs bid-side while mandated position is large | — | 🔴 **E31** | The distribution tool (30-07 evening). Needs the §5.7.3 ceiling raised (15,000 binds first), §5.7.2's 1.5× widened, §5.2 symmetric levels relaxed |

### Chapter 5 as built (31-07) — the values the code carries today

| Parameter | Value | Status | Notes |
|---|---|---|---|
| Cold-start σ² | **the ceiling** — V₀ = ceil ÷ H = 13.33 ticks²/s | 🟡 ours → **E31** | Wide-when-ignorant; every book opens at max width and tightens as movement is measured. Book-visible on day one |
| Dwell (shape/extra lifetime) | **his four-row table, built 01-08c**: LIVE 3–12 s · PRE_KICKOFF 8–30 s · POST_GAME 10–40 s · OVERNIGHT 20–90 s, keyed on the activity axis | 🟡 his values → E31/N26 | Replaced the LIVE-only interim. N26's gate stands: expiry only permits, never causes |
| Odd-tick side | **stateless seeded 50/50** per draw | ✅ ours (remit line) | Strict alternation needs state; the hash bit gives the same fairness, replay-safe. Tagged `[odd-side]` |
| Width constant C | **derived at import** from γ and k, ≈1.653 | ✅ mechanism | Never a literal — a test enforces `WIDTH_CONST == width_constant()` so a stale C cannot survive an E31 change |
| §5.8 material thresholds | IA ≥ **$0.005** · quantity ≥ **500 sh** · any price · suspension flip | ✅ spec-fixed | Judged on pre-variation sizes and the held shape — the random draw can never cause a publish |
| Quote Version | `QV-{n:06d}`, increments **on publish only** | ✅ ours | Every seed keys on it; the replay identity hangs on this |
| §3.4.1 promotion dwells | Invalid→Degraded: 1 valuation · then **10 s per rung** | 🟡 ▸ spec | Demotions instant; relapse resets the clock |
| §3.5 deductions | 15/40/25/10/30/20/15/20, floor 0 | 🟡 ▸ spec | Confidence caps status: ≥90 Valid · ≥70 Warning · ≥40 Degraded · else Invalid |
| MEV | ROF + $5 × remaining + $2.50 × scheduled | ✅ §5.4 formula | In `reference_price.py`; `games_remaining` rides Edwin's daily feed — the engine holds no schedule (§2.5 gap) |
| split-lean `S₂` / `M₂` | skew and cap on the **mandated** part of the position | — | 🔴 proposal, blocked on **E27** | `traded = NP − OpeningPosition`; sentiment lean keeps ~§4.5's cap, distribution lean gets its own. §4.5 single-position lean stands meanwhile |

### Chapter 6 as built (01-08c) — market state

| Parameter | Value | Status | Notes |
|---|---|---|---|
| §6.4.1 promotion dwell | **10 s per rung**, Defensive→Active and Active→Stable; **Suspended→Defensive dwell-free** (mirrors §3.4.1's first-rung grant) | 🟡 ▸ spec | Demotions instant; dwell toward one rung never counts toward the next; versions mint on change only |
| Activity windows | PRE_KICKOFF = **1 h before kickoff** · POST_GAME = **1 h after the final** | 🟡 ours, interim → **N4** | The dwell table's boundaries. Pre window mirrors §3.3.2's tightest freshness band; Edwin defines the real session boundaries |
| Tracker start | **Suspended**; first healthy evaluation earns Defensive | ✅ ours (remit line) | Wide-when-ignorant's Ch 6 twin |
| Venue sync axis | derived from the Venue State Record: UNKNOWN order → Suspended · pending intents → synchronizing (blocks only the climb to Stable) | ✅ ours | `VenueEngine.sync_state()` |
| Venue connection axis | **runtime-supplied**; CONNECTED by construction for in-process transports | 🟡 NATS adapter owes real transitions | `Orchestrator.set_venue_connection()` |
| ⚠ §6.3 vs §6.4.1 on Recovery Ready | §6.3: Ready → Defensive · §6.4.1: Defensive→Active permitted with "Normal **or Ready**" | 🔴 spec defect — **E37** | Both literal, stricter wins; cannot bite until §10 exists |

### Ingestion + venue-interface numbers (not in the spec — ours or the venue's)

| Parameter | Meaning | Value | Status | Source |
|---|---|---|---|---|
| `probability poll interval` | How often the poller calls SR per live game | **~2 s** — matches the measured median update gap | 🟡 evidence-backed, E18 open | 24-07 measurement |
| `SR update cadence (observed)` | How often SR's probability actually changes in a live game | median **4 s** · mean 11.5 s · p90 28 s · 64 % ≤5 s · 1,089 updates/game | ✅ measured | Chiefs–Ravens capture 24-07 |
| `SR acquisition lag` | SR's own delay before publishing | ~5–15 s (media tier) **or** fast (betting tier) — **contradictory sources** | 🔴 S9 — measure in August | SR service research vs Cody |
| `ClOrdID` | Client order id format | ≤ **20 chars**, **no leading zeroes**, + gateway's MM prefix; replace/cancel carry **two** ids (new + orig), each ≤20 | ✅ venue-verified 24-07 | tZERO OE spec v2.2 |
| `MaxOrdRate` | tZERO's per-account message allowance | **5,000/s** · `MaxDupOrdRate` **200/s** (duplicate = same symbol + side + type; raised from the 20/s default for ladder churn) | ✅ **T2 answered** | Hasan's guide 05-08 (live-verified) |
| `gateway MM governor` | Token-bucket throttle on the MM namespace | **5,000 msg/s, burst 2,000** — ✂ supersedes the 50 msg/s placeholder (recorded here until 06-08). ⚠ Over-limit messages are **REJECTED** (`RATE_LIMITED`), never queued. ⚠ Local rig containers may still run old configs with the placeholder — `MM_LIMIT_SECURITIES` caps drills politely | ✅ **T2 answered** | Hasan's guide 05-08 · decisions 06-08c |
| `dead-man window` | Heartbeat silence before the gateway sweeps our book | **4 s** + latched sweep + arms only when the book holds orders + **30 s boot grace** (detail confirmed by Hasan's guide) | 🟡 **ours to set** (N15) — 4 s correct for now; tighten to ~1–1.5 s AFTER the VM beat-jitter measurement | Hasan's guide 05-08 · N15 position 06-08b |
| `heartbeat interval` | How often the MM beats on `gateway.orders.mm.heartbeat` | **0.25 s** — an INDEPENDENT asyncio task in the runtime since 06-08d (was 1 s inside the tick). The beat and the window move together (N15) | 🟡 ours (N15), window retunes after the VM measurement | Ch 8 build 01-08 · beat task 06-08d |
| `time-in-force` | TIF on every MM resting order | **DAY (0)** — self-cleaning at tZERO's 23:59 ET boundary; ⚠ nightly book gap → **E36** | 🟡 built as DAY, Edwin rules | Ch 8 build 01-08 |
| `ClOrdID scheme` | Deterministic order-id minting | **`MM` + 16 hex of SHA-256** over `security\|context\|side\|slot\|config` — 18 of 20 chars, no leading zero, no dots | ✅ ours (replay requirement 24-07) | `mm/venue/reconciler.py` |
| `MM identity` | `userId` / `botId` / `account` (FIX Tag 1) on the gateway | Loopback: `mm1` / `sdmm-1` / `"loopback"` · real: **`384925384799470102`** / **`mm-1`** / **`1797733477`** (Hasan's guide §4 — the userId keys the reply subject `order.{userId}.>`) | 🟡 **rides ENV, not the dictionary** since 06-08d (`MM_USER_ID` · `MM_BOT_ID` · `MM_VENUE_ACCOUNT` via `compose.Settings` — the env-vs-dictionary split, George 06-08b) | decisions 06-08c · `mm/venue/transport.py` |
| `EXECUTION idempotency key` | What names one fill | (venue, **client_order_id**, execution_id) — ⚠ supersedes §7.3's (venue, execution_id): **tZERO recycles ExecIDs** (incident 29-07) | ✅ venue-verified | Gateway `e37cd3d` · `mm/events/idempotency.py` |
| `gateway local-event naming` | Which field names the order on gateway-originated events | **The subject alone** (`order.{user}.{clOrdId}`) — loopback accepts and resolved cancels (dead-man/cancel_all sweeps) carry NO clOrdId in data; adapter falls back to the topic segment | ✅ wire-verified 02-08 | Loopback wire test · `[topic-fallback]` |
| `gateway event ordering` | Cross-subject timestamp order of order events | **Not guaranteed** — 8 publisher workers; acks for one security observed 10 µs reversed. Handled: per-security cycle-clock floor `[monotonic-at]` | ✅ wire-verified 02-08 | Loopback wire test |
| `LmtPerc aggressive band` | Max distance an order may CROSS through the opposite best | **3%** (5% seen on one symbol — per-symbol bands exist) | ✅ live-decoded 07-08 | Reject texts, real venue |
| `LmtPerc passive band` | Max distance a passive order may sit from its own side's best | **90%** | ✅ live-decoded 07-08 | Reject texts, real venue |
| `LmtPerc reference` | What the bands measure against | A **delayed snapshot** of the book (refresh ~minutes, not live); empty book → "No price available", ALL orders reject | 🔴 exact feed + cadence = the Hasan ask; gates the 163 empty books | 07-08 live |
| `MPID` | The MM's tape identity | **IPLM**, driven venue-side by Account1=1797733477; retail IPLY, future BD-prop IPLP | ✅ Rob Colucci 07-08 | decisions 07-08g |

### Runtime clocks (03-08 design session — `mm/runtime/` is UNBUILT)

The engine is event-driven: a book updates when an accepted fact arrives,
never on a timer (§5.8). "Every 200 ms" and "every 4–5 s" are **not** one
loop speed — they are three separate clocks the runtime owns. Full
reasoning: `sessions/2026-08-03-deployment-architecture.md`.

| Parameter | Meaning | Value | Status | Source |
|---|---|---|---|---|
| `runtime tick` | The loop's base rate: drain inbound → due polls → due sweeps (the beat is its OWN ~250 ms task since 06-08d) | **1 s**, fixed, unconditional | 🟡 ours | 03-08 design · beat task 06-08d |
| `checkpoint_interval_s` | §10.3: how often the runtime writes a complete-state checkpoint (bounds boot replay to one hour of tail) | **3,600 s**, written at a tick boundary, local disk beside the journal, keep last 3 | 🟡 ours — **built 06-08d**, equality-proven | `mm/config/dictionary.py` · design 06-08c |
| `event_idempotency_retention_s` | §12.3's slot: how long a seen idempotency key is remembered | **604,800 s (one week)** = JetStream's redelivery bound; pruned on EVENT time so replay reproduces the same set; duplicates never refresh an age | 🟡 ours — recorded design 06-08c, **built 06-08d** | `mm/events/acceptor.py` `[seen-retention]` |
| `poll tier — LIVE` | SR poll per live game (kickoff passed, no final) | **~2 s** — E18's evidenced rate; a 200 ms poll re-reads unchanged values against SR's 4 s median gap | 🟡 evidence-backed, E18 open · ✅ **built 05-08** | `cf2bc10` |
| `poll tier — PRE_KICKOFF` | SR poll within 1 h of the scheduled kickoff | **15 s** — the midpoint of George's 10–30 s range; one dictionary value to change when he picks | 🟡 **interim, built 05-08** | `cf2bc10` |
| `poll tier — OVERNIGHT` | SR poll for an upcoming game > 1 h out | **30 min** (George, 05-08, "to be safe"). ⚠ Doubles as the **N24 experiment** — the journal now records whether pregame probability moves at all | 🟡 **George's number, built 05-08** | `7ac6787` |
| `poll tier — POST_GAME` | SR poll after the final | **10 min through the 1 h post-game window, then never again** (George, 05-08). The watch re-offers the final each poll: identical → quiet duplicate; a CHANGED score → **CONFLICT alarm** in the PollReport (§3.1.3 wants a human, not an overwrite). The window bound stops finished games polling forever | 🟡 **George's number, built 05-08** | `7ac6787` |
| `tier decision location` | Where a game's tier is computed | **The poller, from poller-local facts** (scheduled kickoff via discovery — carried through `ensure_game` since 05-08; the final it publishes itself; its own clock). NOT the orchestrator's activity axis, which needs readings to know a game is live — circular for scheduling. The two derivations stay independent. A moved fixture re-stamps the kickoff and reschedules at once; an unknown kickoff errs busy at the live rate | ✅ built 05-08 | `[tiers]` note · researcher report |
| `earnings burst` | Tue/Wed ~07:30 window | Edwin's daily file → **burst-evaluate all 170** | ✅ the 23-07 ruling | 03-08 design |
| `peak SR call rate` | Worst case, NCAA Saturday | 30–40 live games → **15–20 calls/s** — this is the **S7** quota ask. Engine compute ~2 ms per reading, so the ceiling is venue messages (**T2**), never CPU | 🟡 derived | 03-08 design |
| `sweep emission` | When the §3.1.4 sweep writes a journal event | ✂ corrected 04-08: the sweep is **PORTFOLIO-WIDE** (§3.1.4 + §2.5) — **one `VALUATION_SWEEP` event per 2.0 s slot covers all 170 securities = 0.5 events/s**. The 03-08 "emit on effect / 85 events/s" plan was a per-security misreading, dropped. A stall emits ONE sweep carrying `missed_intervals`, never a backlog | ✅ **built 04-08** (`mm/runtime/loop.py`) — the N28 type blessing rides the Edwin round | `2eaa27b` · `cd6cf21` |
| `source_liveness_window_s` | How long after the last SUCCESSFUL fetch the source still counts as answering — the `[observation-age]` deviation's one number | **20 s** — deliberately §3.3.1's Invalid bound, so "no successful observation for 20 s" suspends on exactly the spec's timing, applied to the right fact | 🟡 ours (Ch 12) — flagged to Edwin inside **E38** | Built 04/05-08 |
| `live freshness basis` | Which age §3.3.1's live bands (5/10/20 s) measure | **OBSERVATION age** (time since the last successful fetch) wherever the liveness signal exists — a confirmed number is **CURRENT** through halftime; 20 s of true silence suspends. Reading age applies pregame and wherever no observation ever arrived (the spec's rule, unchanged). ⚠ Deviation from §3.3.1's letter; band VALUES untouched and Edwin's | 🟡 **built our way — E38 carries it to Edwin** with the measurement (SR has no heartbeat; halftime = 2,862 s) | `48b648d` · decisions 05-08 |
| `source_fetch_timeout_s` | How long one live HTTP fetch may take before it counts as a failed observation | **1.5 s** — short by design: fetches run serially inside the 1 s tick, the heartbeat rides the same tick, and the gateway dead-man sweeps at 4 s; two stuck fetches still leave the next beat inside the window. A timeout is `SourceUnavailable` → the observation stamp stays stale → the liveness rungs grade the silence. ⚠ The serial-fetch shape itself caps out near ~35 live games — the S7 live-bulk endpoint is the season fix | 🟡 ours (Ch 12), **built 05-08b** | `06d6853` · decisions 05-08c |
| `reaction bound` | Accepted reading → published book, in process | **single-digit ms** (measured, real-game tests). §5.8's "200 ms" is a **bound, not a timer** — the budget is spent waiting for SR, not for us | ✅ measured | Real-game tests · 03-08 |

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
| `price band (valuation)` | Hard floor/cap on the venue's book | floor 1 tick · cap **$127.50** — the venue REJECTS above it, never clamps. ✅ **Built 06-08d:** `venue_price_cap` in the dictionary; the ladder ceiling floors at min(MEV, cap) | ✅ live-verified (Hasan's guide 05-08) | Client sheet 22-07 · `mm/config/dictionary.py` |
| `event trigger weights` | Per-event price impact | ✂ **Not needed in v1** — the in-game driver is SR's live win probability, pulled directly (E15 resolved) | ✂ 23-07 | MM call 23-07 |
| `recompute cadence` | Valuation update rhythm | **Bifurcated by game state:** live games ~200ms per call ("a second's too long") · non-live every 30–60s · earnings windows (Tue NFL / Wed NCAA) all ~170 symbols for ~5 min | ✅ 23-07 | MM call 23-07 |

## Market state / sessions

| Parameter | Meaning | Value | Status | Source |
|---|---|---|---|---|
| `sessions` | Liquidity session set | in-game / around-game / overnight | ✅ | 20-07 (Troy) |
| `overnight spread` | Deliberate wide spread outside games | ~$2.5–5 | 🟡 indicative | 20-07 (Troy) |
| `session boundaries` | When each session starts/ends | interim built 01-08c: 1 h pre-kickoff / 1 h post-final windows on the activity axis | 🔴 TBD — Edwin's; interims tagged N4 in the Configuration Dictionary | N4 |
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

| Parameter | Their proposal | Our proposal (decision-cycle pseudocode, archived) | Converge? |
|---|---|---|---|
| Base half-spread | 2 ticks | 2 ticks (`spread_ticks`) | ✅ same |
| Ladder spacing Δ | 3 ticks | 3 ticks (`spacing_ticks`) | ✅ same |
| Levels per side | 3 | ~4 (`n_base`, profile-scaled 2–6) | ~close |
| Side budget | 6,000 sh | 5,000 sh (`l_base`) | ~close |
| Depth weights | front-loaded 2^k | front-loaded 0.55^k | ~close |
| Inventory gain λ | 1500 ¢ per 100% float | 0.5 × price per 100% float (different units — reconcile) | ⚠ compare |
| Cadence | 200 ms full per-team replace on RP change | 200 ms heartbeat + event triggers, diff-based publish | ⚠ differs (full-replace vs diff) |
