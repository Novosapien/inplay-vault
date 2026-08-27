---
description: "Registry of every tunable MM number with value, status and source — valuation, sessions, quoting, supervision, SNT-1 defaults and profile multipliers"
---

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
| Quantity variation · increment / min / max | ±25% (seeded SHA-256, fixture verified) · **1 (grid dropped)** / 1,000 / 15,000 sh | ✅ variation · ✂ increment **1 since 15-08** (was §5.7.3's 500; George: any visible grid reads as an inactive book — raw integer sizes; book-visible → Edwin round) · MM #36, not merged/deployed | 5.7.3 · decisions 2026-08-15 |
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
| `sigma` (feed field) | schedule dispersion √(Σ p(1−p)) | ✅ | a **different object** — never enters the de-vig step. ➕ 13-08 honesty note: validated and stored, **consumed by nothing today** — quote width runs on measured volatility (E31/E44); any future width use of this field is Edwin's |
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
| **T-WARNING age** (missed 06:00 file → alarm, quote on) | ~26 h proposed — purely to make the ask concrete | 🔴 **Edwin's number** | Stale-T ladder, [[market-maker/systems/daily-reference-feed]] §3.5. Book-visible under the 22-07 line; measured deterministically (sweep `scheduled_time` − applied `effective_time`) |
| **T-DEGRADED age** (widen / Defensive posture) | ~50 h proposed | 🔴 **Edwin's number** | Same ladder — the "right for an hour, not obviously right for a Sunday" question in N19, now with a mechanism attached |
| **T-SUSPEND age** (the book comes down) | no proposal — his call entirely | 🔴 **Edwin's number** | Same ladder, third rung |
| **NFL de-vig drift threshold** (verifier alarm) | — | 🔴 TBD ours | Phase-3 verifier: recompute the 32 NFL rows from the current line per accepted file, alarm past this drift ([[market-maker/systems/daily-reference-feed]] §4) |

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
| `levels_range` | levels per side | ✎ **1–3, drawn per dwell — DEPLOYED 27-08 (`CFG-0045`)**. Was 3–6 proposed; Edwin cut it to **1 fixed** on 20-08 (E51 answer 2, "do not build the optionality into v1"); George restored the drawn range on 27-08 after the one-rung book proved it cannot heal a bitten rung. Live shape: 86 books at 1 rung, 92 at 2, 97 at 3 | ✅ deployed 🟡 **Edwin not yet told — book-visible** | decisions 2026-08-27 · sessions/2026-08-27-ncaa-only-maker-and-three-rungs |
| `level_step_ticks` | gap between levels | **1–4 ticks**, drawn per dwell. ⚠ Inert while `max_levels` was 1 (20-08 → 27-08); **live again from `CFG-0045`** | 🟡 adopt | |
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
| SNT-1 `base_orders_per_hour` | arrival intensity, weight-1.0 team | **9/hr**, LIVE ~~×75~~ **×400 (15-08 ruling)** | 🟡 | ~~≈ 675 orders/hr ≈ 30,000 sh/hr per book~~ → ≈ 3,600 orders/hr ≈ **160,000 sh/hr per book** in LIVE; the L1-erosion concern holds only for the dwell states (the LIVE ladder re-rolls every 500 ms) |
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
| `live test cadence` | Quote cadence for the pre-launch live-game runs | **500ms**, tightening toward **200ms** as launch approaches. Confirmed running across all 180 books | ✅ 12-08 | George, 12-08 |
| `taker cadence per market` | How often the taker touches any single book | roughly every **20 seconds** (it takes continuously across all markets) | ✅ 12-08 | George, 12-08 |
| `observed order volume` | Orders placed in a day by maker and taker together | ~**1.2 million** across 180 books, business-as-usual cadence | ✅ 12-08 | George, 12-08 |
| `probability poll interval` | How often the poller calls SR per live game | **~2 s** — matches the measured median update gap | 🟡 evidence-backed, E18 open | 24-07 measurement |
| `SR update cadence (observed)` | How often SR's probability actually changes in a live game | median **4 s** · mean 11.5 s · p90 28 s · 64 % ≤5 s · 1,089 updates/game | ✅ measured | Chiefs–Ravens capture 24-07 |
| `SR acquisition lag` | SR's own delay before publishing | ~5–15 s (media tier) **or** fast (betting tier) — **contradictory sources** | 🔴 S9 — measure in August | SR service research vs Cody |
| `ClOrdID` | Client order id format | ≤ **20 chars**, **no leading zeroes**, + gateway's MM prefix; replace/cancel carry **two** ids (new + orig), each ≤20 | ✅ venue-verified 24-07 | tZERO OE spec v2.2 |
| `MaxOrdRate` | tZERO's per-account message allowance | **5,000/s** · `MaxDupOrdRate` **200/s** (duplicate = same symbol + side + type; raised from the 20/s default for ladder churn) | ✅ **T2 answered** | Hasan's guide 05-08 (live-verified) |
| `gateway MM governor` | Token-bucket throttle on the MM namespace | **5,000 msg/s, burst 2,000** — ✂ supersedes the 50 msg/s placeholder (recorded here until 06-08). ⚠ Over-limit messages are **REJECTED** (`RATE_LIMITED`), never queued. ✂ 08-11: the local rig's mm-gateway container ran the 50/100 defaults until the 500 ms-churn drill hit them (348 RATE_LIMITED → the backoff suppressed a whole side); **the rig now runs `MM_RATE_LIMIT=5000 MM_RATE_BURST=2000`**, production-true | ✅ **T2 answered** · rig aligned 08-11 | Hasan's guide 05-08 · decisions 06-08c |
| `dead-man window` | Heartbeat silence before the gateway sweeps our book | **4 s** + latched sweep + arms only when the book holds orders + **30 s boot grace** (detail confirmed by Hasan's guide) | 🟡 **ours to set** (N15) — 4 s correct for now; tighten to ~1–1.5 s AFTER the VM beat-jitter measurement | Hasan's guide 05-08 · N15 position 06-08b |
| `heartbeat interval` | How often the MM beats on `gateway.orders.mm.heartbeat` | **0.25 s** — an INDEPENDENT asyncio task in the runtime since 06-08d (was 1 s inside the tick). The beat and the window move together (N15) | 🟡 ours (N15), window retunes after the VM measurement | Ch 8 build 01-08 · beat task 06-08d |
| `time-in-force` | TIF on every MM resting order | **DAY (0)** — self-cleaning at tZERO's 23:59 ET boundary; ⚠ nightly book gap → **E36** | 🟡 built as DAY, Edwin rules | Ch 8 build 01-08 |
| `ClOrdID scheme` | Deterministic order-id minting | **`MM` + 16 hex of SHA-256** over `security\|context\|side\|slot\|config` — 18 of 20 chars, no leading zero, no dots | ✅ ours (replay requirement 24-07) | `mm/venue/reconciler.py` |
| `MM identity` | `userId` / `botId` / `account` (FIX Tag 1) on the gateway | Loopback: `mm1` / `sdmm-1` / `"loopback"` · real: **`384925384799470102`** / **`mm-1`** / **`1797733477`** (Hasan's guide §4 — the userId keys the reply subject `order.{userId}.>`) | 🟡 **rides ENV, not the dictionary** since 06-08d (`MM_USER_ID` · `MM_BOT_ID` · `MM_VENUE_ACCOUNT` via `compose.Settings` — the env-vs-dictionary split, George 06-08b) | decisions 06-08c · `mm/venue/transport.py` |
| `MM universe` | Which books the maker quotes | ✎ **138 NCAA only from 27-08** (`MM_SECURITIES` + a matching `MM_SUPERVISED_INPUTS` file — the engine refuses a file naming tickers outside `MM_SECURITIES`). The 32 NFL books carry no maker quote | ✅ George 27-08 | sessions/2026-08-27-ncaa-only-maker-and-three-rungs |
| `EXECUTION idempotency key` | What names one fill | (venue, **client_order_id**, execution_id) — ⚠ supersedes §7.3's (venue, execution_id): **tZERO recycles ExecIDs** (incident 29-07) | ✅ venue-verified | Gateway `e37cd3d` · `mm/events/idempotency.py` |
| `gateway local-event naming` | Which field names the order on gateway-originated events | **The subject alone** (`order.{user}.{clOrdId}`) — loopback accepts and resolved cancels (dead-man/cancel_all sweeps) carry NO clOrdId in data; adapter falls back to the topic segment | ✅ wire-verified 02-08 | Loopback wire test · `[topic-fallback]` |
| `gateway event ordering` | Cross-subject timestamp order of order events | **Not guaranteed** — 8 publisher workers; acks for one security observed 10 µs reversed. Handled: per-security cycle-clock floor `[monotonic-at]` | ✅ wire-verified 02-08 | Loopback wire test |
| `LmtPerc aggressive band` | Max distance an order may CROSS through the opposite best | **3%** (5% seen on one symbol — per-symbol bands exist) | ✅ live-decoded 07-08 | Reject texts, real venue |
| `LmtPerc passive band` | Max distance a passive order may sit from its own side's best | **90%** | ✅ live-decoded 07-08 | Reject texts, real venue |
| `LmtPerc reference` | What the bands measure against | A **delayed snapshot** of the book (refresh ~minutes, not live). ✎ **08-11: the empty-book "No price available" total-reject is GONE** — in the full-book run all 164 virgin books ACCEPTED their first ladders (169/170 stood; only JETS rejected, against its stale ~$18.65 reference). The venue now takes first orders on unquoted symbols — the 07-08 IPTCBILL behaviour no longer reproduces | ✎ empty-book gate lifted (observed 08-11, full-book run); exact feed + cadence still the Hasan ask | 07-08 live · 08-11 full-book run |
| `MPID` | The MM's tape identity | **IPLM**, driven venue-side by Account1=1797733477; retail IPLY, future BD-prop IPLP | ✅ Rob Colucci 07-08 | decisions 07-08g |
| `reject_backoff_base_s` | R-R03/C4: first retry delay after a venue reject (submit rejects key on price; cancel/replace rejects key on the order) | **2 s** | 🟡 ours, built 08-10c (MM PR #13) — live C4 run owed | `mm/config/dictionary.py` · `mm/venue/backoff.py` |
| `reject_backoff_multiplier` | Escalation per consecutive reject: delay(n) = base × mult^(n-1) | **×2** (2, 4, 8, 16, 32, 60…) — success is the only reset | 🟡 ours, built 08-10c | same |
| `reject_backoff_cap_s` | The schedule's ceiling | **60 s** | 🟡 ours, built 08-10c | same |
| `test symbol scheme` | How a permanent test security is named | **Real ticker + `.TEST`** — e.g. `IPTCRAVE.TEST` (8 → 13 chars). tZERO tracks them separately; accounts can be entitled to `.TEST` symbols only. The dot is in the SYMBOL, never the `ClOrdID` | ✅ Rob Colucci 08-08 (**answers T10**) | decisions 08-08c · [[market-maker/test-symbols]] |
| `test symbol set` | Which securities the test books run on | **10:** RAVE · BILL · COWB · LION · PACK · TEXA · JAGU · CHIE · EAGL · COMM. Chosen for Sportradar replay coverage → **17 playable games** (46 of 102 recordings carry both push `events` and REST `pbp`; all 17 live-verified 08-08) | 🟡 **4 codes unattested** (LION · TEXA · JAGU · COMM are ours, pattern-derived); provisioning pending | [[market-maker/test-symbols]] |

### Runtime clocks (03-08 design session — `mm/runtime/` is UNBUILT)

The engine is event-driven: a book updates when an accepted fact arrives,
never on a timer (§5.8). "Every 200 ms" and "every 4–5 s" are **not** one
loop speed — they are three separate clocks the runtime owns. Full
reasoning: `sessions/2026-08-03-deployment-architecture.md`.

| Parameter | Meaning | Value | Status | Source |
|---|---|---|---|---|
| `runtime tick` | The loop's base rate: drain inbound → due polls → due sweeps (the beat is its OWN ~250 ms task since 06-08d) | ✂ **0.5 s** since 08-11 (`tick_interval_s`, was 1 s fixed) | ✅ ruled 08-11 | 03-08 design · MM PR #16 |
| `drain_max_readings_per_tick` | ⭐ Always-quoting step 1 (George's 08-13 ruling): the most bus readings one tick may process; the leftover waits one tick | **256** — ~×3 above the NCAA-Saturday arrival rate (~70/tick); a capped tick logs `DRAIN_CAPPED` | 🟡 **OURS (08-13)** — re-size after N31 group commit (engine time becomes the binding constraint) | `mm/config/dictionary.py` · `[drain-cap]` in `runtime/loop.py` · MM PR #25 |
| `drain_max_venue_per_tick` | ⭐ Always-quoting step 1: the most venue answers (fills, acks, cancels) one tick may process | **512** — ~×3 above the largest observed post-sweep ack burst (~134/tick); worst-case capped tick at p99 fsync 2.47 ms stays inside the 4 s dead-man window | 🟡 **OURS (08-13)** — ⚠ must RISE (~×2 of Saturday's ~1,050 acks/tick) once group commit deploys and engine time binds | `mm/config/dictionary.py` · MM PR #25 |
| `heartbeat_stall_threshold_s` | ⭐ Always-quoting step 3: how long ticks may fail to complete before the beat task WITHHOLDS the heartbeat and the dead-man takes over | **5 s** — above the worst legitimate tick (a fully capped drain at p99 fsync ≈ 2.7 s); a wedged engine's book gets pulled ~threshold + 4 s after the wedge instead of never | 🟡 **OURS (08-13)** | `mm/config/dictionary.py` · `[progress-beat]` in `runtime/loop.py` · MM PR #27 |
| `checkpoint_interval_s` | §10.3: how often the runtime writes a complete-state checkpoint (bounds boot replay to one hour of tail) | **3,600 s**, written at a tick boundary, local disk beside the journal, keep last 3 | 🟡 ours — **built 06-08d**, equality-proven | `mm/config/dictionary.py` · design 06-08c |
| `event_idempotency_retention_s` | §12.3's slot: how long a seen idempotency key is remembered | **604,800 s (one week)** = JetStream's redelivery bound; pruned on EVENT time so replay reproduces the same set; duplicates never refresh an age | 🟡 ours — recorded design 06-08c, **built 06-08d** | `mm/events/acceptor.py` `[seen-retention]` |
| `poll tier — LIVE` | SR poll per live game (kickoff passed, no final) | **500 ms** — ⭐ George's ruling 08-11, matching Edwin's 03-08 number: an unchanged successful fetch is CONFIRMATION (E38), and the cadence buys reaction latency to real changes. ✂ Supersedes the 2 s evidenced interim (SR's 4 s median gap). **Set on the DEPLOYED publisher pools** (`MMPUB_POLL_LIVE_S=0.5`, service PR #15 — #14 was fmt-only mislabelled). ⚠ The MM's IN-ENGINE poller still carries 2 s — it retires at the ingestion switch; if any live game runs on the in-engine path before the switch, bump it or switch first | ✅ **ruled 08-11 · deployed** | service PR #15 · `mm/config/dictionary.py` (engine interim) |
| `tick_interval_s` | The runtime loop's pace (drains, cycles, checkpoints-due) | **0.5 s** — ⭐ George 08-11 (was 1.0 s hardcoded); paired with the 500 ms live cadence | ✅ ruled 08-11 · MM PR #16 | `mm/config/dictionary.py` |
| `sweep_cadence_s` | §3.1.4's portfolio recompute — now the LIVE quote pulse | **0.5 s** — ✂ supersedes the spec's ✅ 2.0/2.5 s (George 08-11) | ✅ ruled 08-11 · MM PR #16 | `mm/config/dictionary.py` |
| `sweep_max_interval_s` | How late a sweep may run before it counts as a MISSED interval (§3.1.4) | ✂ **1.0 s** since 08-13 evening — restores the spec's ABSOLUTE slack (the 08-11 cadence ruling kept the 1.25 ratio, silently tightening 500 ms → 125 ms; ordinary ack churn then tripped it on ~7% of ticks and the portfolio-wide counter capped every book at ACTIVE) | ⭐ **ruled 08-13 (George: "let's do 1s")** — deployed supervised25/CFG-0023; first 435 ticks: ZERO misses | `mm/config/dictionary.py` |
| `converge_max_instructions_per_tick` | ⭐ Always-quoting step 4: the most venue instructions one converger PASS sends (suspends → LIVE → round-robin; books atomic) | ✂ **128** — the dictionary default since `g2-throttle` (was 256 at first deploy, halved 00:05Z 08-14 as the live-load lever) and baked into the deployed `feat/always-quoting-step4b`. Under phase B the budget is PER PASS at 0.25 s — outbound ceiling ~512 instr/s | 🟡 **OURS** — 256 (08-13, MM PR #30) → 128 (08-14, deployed in supervised28/CFG-0026) | `[converge]` in `mm/venue/sync.py` |
| `converge_interval_s` | ⭐ Always-quoting step 4 phase B: the converger runs on its OWN task at this cadence — the tick stages, the task converges; 0 restores the phase-A in-tick pass (the rollback lever and the direct-drive test shape) | **0.25 s** — under the 0.5 s LIVE redraw floor, so a staged live book never waits a full redraw | 🟡 **OURS (08-14)** — **built, NOT deployed** (`feat/always-quoting-step4b` @ `912ba27`) | `[converge-task]` in `mm/runtime/loop.py` |
| `converge_staleness_alarm_s` | Phase B's outbound staleness alarm: `CONVERGE_STALE` logs once per episode when dirty targets outwait this bound — the outbound DRAIN_CAPPED, an alarm not a mode | **2.0 s** — the step-4 design's §5 proposal | 🟡 **OURS (08-14)** — built, NOT deployed | same |
| `MM_DEADMAN_TIMEOUT_MS` (gateway) | The dead-man window: MM heartbeat silence before the gateway sweeps the whole resting book | ✂ **10,000 ms since 00:19Z 08-14** (was 4,000 — swept a live book ~130 times on the 08-13 slate at silence 4.0–4.7 s; every observed gap fits under 6 s, 10 s adds margin) | ✅ **deployed** (env row on the gateway VM; default bump in gateway PR #4) — N15 retune after the jitter measurement stands | `/opt/fix-gateway/.env` · `internal/config/settings.go` |
| `live_redraw_cadence_s` | The republish clock's FLOOR: threshold = max(drawn dwell, this) | **0.5 s** — "new orders every 500 ms, changed or not" in LIVE | ✅ ruled 08-11 · MM PR #16/#18 | `[live-timer]` in `mm/quotes/engine.py` |
| `dwell table = republish clock` | ✂ Every mode republishes a re-rolled book when its drawn dwell expires, changed or not; materiality publishes sooner | **LIVE 0–0 (500 ms floor) · pre-game 5–20 s · post-game 5–20 s · overnight 20–40 s** — ✂ supersedes Edwin's ASMM-1 rows (3–12/8–30/10–40/20–90) and implements his 23-07 "non-live 30–60 s" | ✅ ruled 08-11b · MM PR #18 · deployed supervised11, live-verified | `mm/config/dictionary.py::dwell_ranges_s` — Edwin flag rides E31/E17 |
| `poll tier — PRE_KICKOFF` | SR poll within 1 h of the scheduled kickoff | **15 s** — the midpoint of George's 10–30 s range; one dictionary value to change when he picks | 🟡 **interim, built 05-08** | `cf2bc10` |
| `poll tier — OVERNIGHT` | SR poll for an upcoming game > 1 h out | **30 min** (George, 05-08, "to be safe"). ⚠ Doubles as the **N24 experiment** — the journal now records whether pregame probability moves at all | 🟡 **George's number, built 05-08** | `7ac6787` |
| `poll tier — POST_GAME` | SR poll after the final | **10 min through the 1 h post-game window, then never again** (George, 05-08). The watch re-offers the final each poll: identical → quiet duplicate; a CHANGED score → **CONFLICT alarm** in the PollReport (§3.1.3 wants a human, not an overwrite). The window bound stops finished games polling forever | 🟡 **George's number, built 05-08** | `7ac6787` |
| `tier decision location` | Where a game's tier is computed | **The poller, from poller-local facts** (scheduled kickoff via discovery — carried through `ensure_game` since 05-08; the final it publishes itself; its own clock). NOT the orchestrator's activity axis, which needs readings to know a game is live — circular for scheduling. The two derivations stay independent. A moved fixture re-stamps the kickoff and reschedules at once; an unknown kickoff errs busy at the live rate | ✅ built 05-08 | `[tiers]` note · researcher report |
| `earnings burst` | Tue/Wed ~07:30 window | Edwin's daily file → **burst-evaluate all 170** | ✅ the 23-07 ruling | 03-08 design |
| `peak SR call rate` | Worst case, NCAA Saturday | 30–40 live games → **15–20 calls/s** — this is the **S7** quota ask. Engine compute ~2 ms per reading, so the ceiling is venue messages (**T2**), never CPU | 🟡 derived | 03-08 design |
| `sweep emission` | When the §3.1.4 sweep writes a journal event | ✂ corrected 04-08: the sweep is **PORTFOLIO-WIDE** (§3.1.4 + §2.5) — **one `VALUATION_SWEEP` event per slot covers all 170 securities — ✂ the slot is **0.5 s since 08-11** (was 2.0 s) = 2 events/s**. The 03-08 "emit on effect / 85 events/s" plan was a per-security misreading, dropped. A stall emits ONE sweep carrying `missed_intervals`, never a backlog | ✅ **built 04-08** (`mm/runtime/loop.py`) — the N28 type blessing rides the Edwin round | `2eaa27b` · `cd6cf21` |
| `source_liveness_window_s` | How long after the last SUCCESSFUL fetch the source still counts as answering — the `[observation-age]` deviation's one number | **20 s** — deliberately §3.3.1's Invalid bound, so "no successful observation for 20 s" suspends on exactly the spec's timing, applied to the right fact | 🟡 ours (Ch 12) — flagged to Edwin inside **E38** | Built 04/05-08 |
| `live freshness basis` | Which age §3.3.1's live bands (5/10/20 s) measure | **OBSERVATION age** (time since the last successful fetch) wherever the liveness signal exists — a confirmed number is **CURRENT** through halftime; 20 s of true silence suspends. Reading age applies pregame and wherever no observation ever arrived (the spec's rule, unchanged). ⚠ Deviation from §3.3.1's letter; band VALUES untouched and Edwin's | 🟡 **built our way — E38 carries it to Edwin** with the measurement (SR has no heartbeat; halftime = 2,862 s) | `48b648d` · decisions 05-08 |
| `source_fetch_timeout_s` | How long one live HTTP fetch may take before it counts as a failed observation | **1.5 s** — short by design: fetches run serially inside the 1 s tick, the heartbeat rides the same tick, and the gateway dead-man sweeps at 4 s; two stuck fetches still leave the next beat inside the window. A timeout is `SourceUnavailable` → the observation stamp stays stale → the liveness rungs grade the silence. ⚠ The serial-fetch shape itself caps out near ~35 live games — the S7 live-bulk endpoint is the season fix | 🟡 ours (Ch 12), **built 05-08b** | `06d6853` · decisions 05-08c |
| `reaction bound` | Accepted reading → published book, in process | **single-digit ms** (measured, real-game tests). §5.8's "200 ms" is a **bound, not a timer** — the budget is spent waiting for SR, not for us | ✅ measured | Real-game tests · 03-08 |

### The 08-14 fix-set batch (Phase 0 — `specs/2026-08-14-mm-python-fix-set`)

Landed in ONE dictionary PR (MM **#31**) so the fix-set chunks never
contend on `mm/config/dictionary.py`. Defaults only — each consumer
arrives with its chunk.

| Parameter | Meaning | Value | Status | Source |
|---|---|---|---|---|
| `prior_run_dir` (env `MM_PRIOR_RUN_DIR`) | F2: the PRIOR run's journal/checkpoint directory the ANCHOR_SEED reader mines at boot; a deployment fact, so it rides env through `compose.Settings` | **None** — no prior run → today's freeze-at-current fallback | 🟡 ours — row landed MM PR #31; reader/consumer is CA1 | `mm/config/dictionary.py` |
| `tob_stale_after_s` | R-Q09: how old the venue TOB cache may be before the marketable guard has NO OPINION (stale → send; refusing on stale data would silence quoting) | **30 s** — mirrors the taker's `book_stale_after_s` | 🟡 ours (taker parity, 08-08 evidence) — MM PR #31; guard is CA2 | same |
| `marketable_guard_enabled` (env `MM_MARKETABLE_GUARD`) | R-Q09's kill switch: the pre-flight marketable guard | **on** | 🟡 ours — MM PR #31; guard is CA2 | same |
| `converge_max_books_examined_per_pass` | **review-ca2 MED-4.** The most books one BUDGETED converger pass may DIFF. The instruction budget cannot bound a refused book — R-Q09 answers after the diff and the book then sends nothing, so it costs a whole `reconcile_book` and spends no budget; a phantom touch holding many books re-diffs all of them every pass, for ever. The unbudgeted `[compat]` flush (boot, pull path, direct-drive tests) is exempt and still converges everything | **64 books** — DERIVED: at `converge_max_instructions_per_tick` 128 and ~12 instructions per two-sided book, a pass can only SERVE about ten books, so 64 examinations is over 6× the productive work of a pass — it cannot bite on healthy traffic, and it holds the pathological case to 64 diffs/pass (256/s at the 0.25 s cadence) instead of the whole universe | 🟡 ours — second one-row addition of the CA2 chunk; added + consumed in MM PR #37 | `mm/config/dictionary.py` |
| `marketable_stall_passes` | **N41's alarm bound.** After this many CONSECUTIVE refusals of the SAME book, the guard logs `MARKETABLE_GUARD_STALLED` once per episode, naming the book, the touch holding it and the heal. A refusal keeps the target STAGED, so a book refused against a phantom touch stops publishing — this converts "an operator must notice a counter trending" into "an operator must read one alarm". An alarm, **not a mode** — it changes nothing about what is sent (sibling of `converge_staleness_alarm_s`) | **120 PASSES** — ✎ **re-derived (review-002); the old "≈30 s" was wrong.** The bound is in passes, and `converge_max_books_examined_per_pass` means a book in a class holding more than `cap` dirty books is only re-judged every ceil(N/cap) passes. Wall clock = `passes × ceil(N/cap) × converge_interval_s`: **~30 s at ≤64 dirty, ~60 s at 65, ~90 s at 180.** 120 passes is still right — long enough that a fast market crossing our staged price stays quiet, short enough to hear about a stuck book well inside a game. A test pins the dilation across four universe sizes (the old one multiplied two constants and pinned nothing) | 🟡 ours — one-row exception approved by the lead 14-08; added + consumed in MM PR #34 (CA2 follow-up) | same |
| `boot_heal_enabled` (env `MM_BOOT_HEAL`) | F4's kill switch: the boot healer; off restores the fresh-journal-per-deploy ceremony (R-D06). ✎ **15-08: CONSUMED (MM #42).** Off is total — no ops call, no diff, no cancels | **on** | 🟡 ours — MM PR #31; healer is CA4 (MM #38 → #42) | same |
| `MM_BOOT_HEAL_TIMEOUT_S` (env only) | F4: the whole budget of the healer's ops read (`GET /orders/mm`). A network-edge timeout, so it rides ENV rather than the dictionary — the same shape as the taker's `SNT_FLUSH_TIMEOUT_S`, and documented in the deploy runbook beside it. ⚠ A budget, never a fault switch: it bounds the READ, and expiring it means "no heal today", loudly | **5.0 s** — DERIVED: the call is one localhost GET over a Redis `SMEMBERS` + a pipelined `HGETALL` of ~2,000 rows, i.e. tens of ms, so 5 s is ~100× headroom and still only a sixth of the gateway's 30 s boot grace. Raising it eats that grace, and the dead-man does not care why the first heartbeat was late | 🟡 ours — added + consumed in MM PR #42 (CA4) | `mm/runtime/compose.py` (`BOOT_HEAL_TIMEOUT_S`) |
| `MM_GATEWAY_OPS_URL` · `MM_GATEWAY_OPS_KEY` (env only) | F4: where the gateway's ops server answers `GET /orders/mm`, and the `X-Ops-Key` it demands (the gateway's own `OPS_API_KEY`). Deployment facts, so env per the env-vs-dictionary split; the KEY is a secret and never enters the Configuration Dictionary. ⚠ **URL unset = NO HEAL**, loudly — a shape-A cutover with the URL missing silently becomes a shape-B cutover without the fresh journal, the one combination that leaves phantoms in the record | **unset** (no heal) | 🟡 ours — MM PR #42 (CA4) | `mm/runtime/compose.py` (`Settings`) |
| `live_phase_offset_buckets` | F1b de-phase: each LIVE book hashes into one of k buckets spread across the 500 ms pulse (deterministic on security id) — every book still redraws each 500 ms, only the alignment spreads | **8** | 🟡 ours — Q2 approved by George 14-08 ("as long as it works out"; AC2 proves it); MM PR #31. ⚠ **UNUSED as of 14-08**: CB2 (PR #35) built the bucket primitive (`quotes/phase.py`) and measured that it cannot move AC2 — the metric's window equals the pulse, so a within-pulse offset is invariant to it, and the books already free-run on independent phases. Nothing in the engine reads this row. It stays for the day the pulse or the converger cadence changes | same |
| `opening_position_shares` | R-Q08: the opening position the ask cap sizes from, until Edwin's IPO allocation publisher exists (E27). ✎ **15-08 (CA3): 0 means UNKNOWN, not "we hold nothing"** — R-V07's `Pos` is the VENUE's position while our journal starts at 0 on every fresh journal (14-08: IPTCJETS sold to net −197 from a zero journal position on seeded account inventory). At 0 the bound would be `0 − livS`, never positive, so **every book would go bid-only**; the engine therefore FAILS OPEN and logs `ASK_CAP_UNBOUNDED` once at boot. 🔴 **Setting this to the account's real holding is what turns R-Q08 on — a deploy input (N43).** Injectable at the orchestrator so a rig or test can stand a book that holds something | **0 sh** | 🟡 ours / **E27** stub — MM PR #31; cap is CA3 (MM #38) | same |

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
| `session boundaries` | When each session starts/ends | interim built 01-08c: 1 h pre-kickoff / 1 h post-final windows on the activity axis | 🔴 TBD — Edwin's; interims tagged N4 in the Configuration Dictionary | N4 |
| `condition classes` | Health classifier outputs | Normal / Degraded / Protective / Recovery / Emergency | ✅ (doc) | CTS-002 |
| `classifier thresholds` | Staleness/latency limits per class | — | 🔴 TBD | N3 |
| `RP publication` | Reference price identity | RP = ESV (mid) · frozen on feed failure | ✅ | CTS-002 + 20-07 |

## Quoting engine

| Parameter | Meaning | Value | Status | Source |
|---|---|---|---|---|
| `buying power` | MM capital in tZERO | ~$100M–$100B ("never a limit") — set via `DTBPo` on account creation | ✅ decided, exact number 🟡 | 20-07 (Edwin/Troy) · OMS spec 22-07 |
| `refresh rate` | Quoting cadence | **Bifurcated (supersedes flat 5–10×/sec):** live games ~200ms · non-live 30–60s · earnings burst ~5 min all symbols | ✅ 23-07 | MM call 23-07 |
| `tick size` | Min price increment | **$0.01** | ✅ | Venue-verified 22-07 |
| `base spread` | Default half-spread per side (per profile) | **8 to 12 ticks** (Edwin, 17-08). Supersedes the TBD: the weekend book was "like cement", too tight to the win probability for anyone to trade around | ✅ 17-08 | Edwin, 17-08 |
| `maker resting size` | Displayed size per level | **500 to 3,000**, down from ~10,000. The book was too thick to move | ✅ 17-08 | Edwin, 17-08 |
| `taker size` | Size the taker crosses with | **up to 5,000**, and **allowed to cross multiple price levels** rather than one. Was randomising ~3 to 400, which is negligible against a 10,000 book | ✅ 17-08 | Edwin, 17-08 |
| `target intra-game swing` | How far a share price should move within a game | roughly **$1.50 to $8**. The weekend produced only a couple of dollars. Arithmetic puts a win near $4.80; sentiment should swing wider than the maths | ✅ 17-08 | Edwin, 17-08 |
| `score offset per point` | Dollar value applied per point of score change, as an interim reference price while the win probability is stale | 🔴 **Owed by Edwin**, being derived from NFLverse win probabilities back to 1999. Must remain a point-differential offset only, not a model of injuries or form | 🔴 TBD, this week | Edwin, 17-08 |
| `interim price lifetime` | How long a score-derived price stands | Until the next live win probability arrives, which is then authoritative again. "We don't need to be accurate for more than 10 seconds" | ✅ 17-08 | Edwin, 17-08 |
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
| SNT-1 floats (venue-verified, 08-11) | The per-book float the sell gate + T-S05 trust — pinned to the account's REAL holdings via `SNT_FLOAT_OVERRIDES` after the kill-window divergences | **COWB 4959 · STEE 5256 · EAGL 5132 · GIAN 4737 · PATR 4836** (account `4963224393`) | ✅ venue-reconciled 08-11 — ⚠ LOAD-BEARING env state (`~/snt-0811.env`); re-derive as venue − journalled drift if lost | session 08-11 · T-S05 halts |
| `SNT_MINUTES` | The taker's run window (0 = continuous) | **0** since 08-11 — ⚠ the inherited QA env carried **15**, causing every "mystery exit" | ✅ ours, operational | session 08-11 |
| SNT-1 live stats (measured 08-11) | The taker's first real day vs Edwin's design | 198/198 fills, 0 rejects · 49.5% buys · clip mean 48 (his smoke test ~44) · crossing cost mean 2.3¢ max 4¢ · drift within the 1,500 cap | ✅ measured — data for the E41 tuning round | session 08-11 journal validation |
| `state_multiplier` | Intensity by activity state | ✂ **OVERNIGHT 1x · PRE_KICKOFF 20x · LIVE 400x · POST 20x** since 15-08 = one print per book every 6.7 min · 20 s · **1 s** · 20 s (was 1/6/75/4 = 6.7 min · 67 s · 5.3 s · 100 s, Edwin's v1.0) | 🟡 **GEORGE 15-08** (book-visible; Edwin confirms, E41) · MM PR #40, not deployed | decisions 2026-08-15e |
| `SNT_INTERVAL_{STATE}_S` | The same four rates as an operator sets them: seconds between prints on one weight-1.0 book; unset = the built multiplier | env, per state (LIVE 1 · PRE_KICKOFF 20 · POST 20 · OVERNIGHT 400 are the built values) | ✅ ours, MM PR #40 | `snt/config.py` `[rate-env]` |
| `SNT_INTERVAL_OVERNIGHT_S` — the running value | Seconds between prints on one quiet weight-1.0 book. Takes the ~170 non-game books from ~0.44 to ~4.35 orders/s | **40 s** | ✅ **George, 17-08 — CLEARED BY MEASUREMENT.** 20 h at 40 s ran the gateway at **0.02–0.04 s mean inbound lag**; the busiest hour of the weekend hit **286 msg/s at 0.04 s mean**; taker fill loss **6 in 230,847 (0.0026%)**. The earlier "40 s pushed the gateway 17–27 s behind" is withdrawn — that reading was sampled inside a 36-message minute during a dead FIX session | live `SNT-CFG-0027` · decisions 2026-08-17 |
| gateway inbound lag — the measurement | gateway log time − FIX tag 52 `SendingTime`, bucketed **per minute alongside the message count** | steady state **0.02–0.04 s**; > 2 s means a session break, not load | ✅ method, 17-08 | ⚠ never read this figure without its per-minute message count — that omission produced the wrong root cause |
| `tick_s` / `SNT_TICK_S` | The taker loop's tick — arrivals are served at ticks, so this is the arrival clock's grain | **0.25 s** (was a 0.5 s literal) — the pass costs 0.039 ms at 180 books; realised LIVE gap 1.012 s at 0.25 vs 1.057 s at 0.5 | 🟡 ours, 15-08 · MM PR #40 | `snt/config.py` `[tick]` |
| `max_orders_per_s` / `SNT_MAX_ORDERS_PER_S` | Portfolio-wide ceiling on taker arrivals per second across every book; each taker fill is one maker exec ack (~10 ms under live load, CB1) | **0 = OFF** (shipped) — a Sunday slate of ~20 LIVE books at 1 s ≈ 20 fills/s ≈ +20% of the maker's tick; NCAA Saturday ~60 | 🔴 **George's call (N44)** — mechanism ✅ built, MM PR #40 | `snt/runtime.py` `[portfolio-cap]` |
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

| Parameter | Their proposal | Our proposal (decision-cycle pseudocode, archived) | Converge? |
|---|---|---|---|
| Base half-spread | 2 ticks | 2 ticks (`spread_ticks`) | ✅ same |
| Ladder spacing Δ | 3 ticks | 3 ticks (`spacing_ticks`) | ✅ same |
| Levels per side | 3 | ~4 (`n_base`, profile-scaled 2–6) | ~close |
| Side budget | 6,000 sh | 5,000 sh (`l_base`) | ~close |
| Depth weights | front-loaded 2^k | front-loaded 0.55^k | ~close |
| Inventory gain λ | 1500 ¢ per 100% float | 0.5 × price per 100% float (different units — reconcile) | ⚠ compare |
| Cadence | 200 ms full per-team replace on RP change | 200 ms heartbeat + event triggers, diff-based publish | ⚠ differs (full-replace vs diff) |

## SNT-1 — the Synthetic Noise Taker (built 08-08; Edwin's reference numbers)

Source: Edwin's `snt1_noise_taker.py` (filed in reference/). 🟡 = his
reference value, built as given, tunable · 🔴 = conflicted, needs his
ruling. Code: `inplay-market-maker/src/snt/config.py`.

| Parameter | Value | Status | Note |
|---|---|---|---|
| Base arrival rate | 9 orders/hr (weight-1.0 team, OVERNIGHT) | 🟡 | his "first lever to tune" |
| State multipliers | ✂ OVERNIGHT ×1 · PRE_KICKOFF ×20 · LIVE ×400 · POST ×20 (15-08; was ×1/×6/×75/×4) | 🟡 GEORGE | one print per book every 6.7 min · 20 s · 1 s · 20 s; env `SNT_INTERVAL_{STATE}_S`; MM PR #40 |
| Team weight range | 0.25–4.0 (default 1.0) | 🟡 | feed from the popularity model, later |
| Size distribution | log-normal μ=3.4 σ=0.9, clip 5–400 sh | 🟡 | median ~30 |
| Sweep probability | 10% | 🟡 | else at-touch |
| Impact cap | 3 ticks through the touch | 🟡 | the real damage cap (his hardening pt 4) |
| At-touch size cap | 50% of displayed touch | 🟡 | |
| Daily loss budget | $100,000 / team / session | 🟡 | cannot bind at LIVE (~$1.5k/hr — E32) |
| Spread gate | 8 ticks | 🔴 | never trades §5.2 Stable ($0.10=10t); QA books 4–6t OK — E32 ruling |
| Inventory soft cap | 1,500 sh · 80% flatten bias | 🟡 | exceeds the 1,000 short reserve — E32 |
| Profit tilt | 0.50→0.65 ceiling, full at 10 ticks | 🟡 | flagged to compliance (E32 row) |
| IOC substitute window | cancel after 1.5 s | 🟡 | ours — tZERO has no IOC |
| Book staleness gate | 30 s | 🟡 | ours — the 08-08 MD evidence |
| Reject quiet guard | 5 consecutive → 60 s quiet | 🟡 | ours — interim until reject-backoff |
| **IPO float per team** | **5,000 sh** | 🟡 **E39** | ours, 09-08 — an ASSUMPTION, not a number anyone gave us. Sized so the holding wanders ~3,500–6,500 against the 1,500 drift cap and never nears zero. `float_shares` in `snt/config.py`; per-team overrides exist |
| **Float cost per share** | — | 🔴 **E39** | UNKNOWN. The IPO price is not settled, so the profit tilt still reads the VWAP of what the taker itself traded, not the true cost of the whole holding. Which basis the tilt uses once the price lands is Edwin's call |
| **Per-order notional cap** | **$25,000** | 🟡 **E32** | ours, 09-08 — Edwin named the cap (hardening pt 1) but no value. 400 sh × the $127.50 venue cap ≈ $51k worst case; $25k halves it, a median order (~$2k) never feels it. Cuts, never skips |
| **T-F07 pre-kickoff window** | **1 h before kickoff** | 🟡 | ours, 11-08 — copies the sportradar service's own tier boundary, so taker state and poll cadence flip together. `schedule_pre_kickoff_s` |
| **T-F07 POST window** | **1 h after the final** | 🟡 | ours, 11-08 — copies the service's post-game correction watch. `schedule_post_window_s` |
| **T-F07 LIVE staleness bound** | **10 min of feed silence** | 🟡 | ours, 11-08 — LIVE (×75) needs a fresh feed; silence past the bound decays the book to OVERNIGHT (err-quiet). ~20× the worst observed live reading gap (30 s) |
| **T-F07 file-game length** | **4 h from kickoff** | 🟡 | ours, 11-08 — the fallback file source learns no finals, so LIVE ends on this timer (long game + overtime), then the POST window. `schedule_file_game_s` |

## Venue risk + price bands — live-verified 08-09

Measured from reject texts on the real venue (decisions `2026-08-09`).
✅ = observed directly.

| Parameter | Value | Status | Note |
|---|---|---|---|
| Sellable quantity (side 2) | `Pos − livS` | ✅ | position minus shares already committed to LIVE RESTING SELLS. An order above it is rejected WHOLE — never partially filled |
| Oversell reject text | `FAILSRISK[acct]: You can SELL at most N shares of SYM. Pos=P livS=L` | ✅ | the venue states its own arithmetic |
| Flat-sell reject text | `FAILSRISK[acct]: You are not long SYM. There are NO shares to SELL.` | ✅ | the `Pos=0` case of the same rule |
| LmtPerc passive band — EAGL | 80% above the ASK | ✅ | per-symbol, NOT global |
| LmtPerc passive band — JETS | 90% above the ASK | ✅ | |
| LmtPerc aggressive band — EAGL/COWB/GIAN/PATR | 3% below the BID | ✅ | |
| LmtPerc aggressive band — STEE | 5% below the BID | ✅ | |
| LmtPerc aggressive band — JETS | 10% above the ASK | ✅ 08-11 | full-book run reject texts — a third per-symbol value |
| `venue_terminal_retention_s` | How long a TERMINAL venue order stays in working memory | **300 s** | 🟡 ours (08-12) | Only stragglers need it; the gateway's replace-pair gap is ~50 ms. 99.7% of venue state was terminal before this |
| `venue_idempotency_retention_s` | Dedup window for VENUE acks/executions | **3,600 s** | 🟡 ours (08-12) | Core NATS is at-most-once — it cannot redeliver a week later. Bus events keep the 7-day JetStream bound |
| LmtPerc anchor refresh | ~3–5 min, and it FOLLOWS prints | ✅ 08-11 | measured across the four JETS walk hops |
| LmtPerc reference | can be CROSSED | ⚠ | EAGL observed with BID 145.25 and ASK 77.80 simultaneously → no legal sell price exists on that book at all |
| DONE_FOR_DAY (39=3) | **never observed** | ⚠ | orders survive the 23:59 ET boundary — see T14; the 22-07 adopted "fact" is contradicted |

## Observability + manual orders — the 12-08 spec (`specs/2026-08-12-admin-trading-observability/`)

| Parameter | Value | Status | Notes |
|---|---|---|---|
| Manual order max quantity | 10,000 shares/order | ✅ Hasan 12-08 | engine-enforced (`SNT_MANUAL_MAX_QTY`), panel mirrors from `snt.state.guards` |
| Manual order price collar | ±20% of the collar reference | ✅ Hasan 12-08 | engine-enforced (`SNT_MANUAL_COLLAR_PCT`) |
| Manual order max notional | $500,000 | 🟡 proposed | not explicitly ruled; `SNT_MANUAL_MAX_NOTIONAL` |
| Manual order TIF | limit DAY only | ✅ spec 12-08 | no operator TIF choice in v1 |
| Manual order side | FIX side 2 always (never 5) | 🟡 ours 12-08b | an operator asking to sell has not asked to short — [manual-side] |
| Collar last-trade max age | 3,600 s | 🟡 ours 12-08b | the fallback reference's staleness bound; JETS's 18.65 was a last-trade FOSSIL (`SNT_MANUAL_LAST_TRADE_MAX_AGE_S`). A crossed book counts as no book |
| `open_orders` terminal retention | 60 s | 🟡 spec 12-08 | a finished order stays on the screen, then drops (`terminal_retention_s`) |
| Engine state publish cadence (`mm.state` / `snt.state.*`) | ~1 s — maker every 2nd tick · taker every 1.0 s | 🟡 proposed | ours, 22-07 remit line. In the **Configuration Dictionary** (`state_publish_every_n_ticks` · `state_publish_interval_s`), not a code literal. The maker also flushes within one tick of a kill switch / new quarantine / new suspension |
| `mm.state` payload budget | ≤ 256 KB | 🟡 proposed | active-books-only projection. **MEASURED 12-08b: 208,250 bytes at 170 books quoting two-sided ladders (~9.2 resting orders each); ~220 KB extrapolated to 180. ~14% headroom** |
| `mm.state` hard payload ceiling | 1 MB | ✅ NATS default | `max_payload`; a publish above it is REFUSED. The second shed stage exists only so this can never be reached |
| Publisher tick-latency cost (maker) | **+0.28 to +0.35 ms on a ~4.6 ms tick (+6% to +8%)** | ✅ measured 12-08c | the tick STAGES an immutable frame (0.37 ms); its own task encodes and publishes (1.61 ms). Was +1.98 ms (+43.7%) with the encode inline, then +0.32–0.46 ms after the split, then this after the double encode was removed. Loop utilisation ~0.98% of the 500 ms interval |
| `snt.state` payload budget | ≤ 256 KB, same two-stage shed as the maker | 🟡 ours 12-08c | **MEASURED: 1.9 KB at 5 books · 58.4 KB at 180** with one live order per book. R2 assumed the taker's book set was small — it is not; SNT-1 has run all 180 since 08-12. `open_orders[]` is the unbounded term |
| Manual-order delivery confirmation window | 2.0 s | 🟡 ours 12-08c | `SNT_FLUSH_TIMEOUT_S`. How long the engine waits for the server's round trip before reporting `submit_unconfirmed`. A TIMEOUT, not a fault switch — it can never stop an order being published, only make the engine pessimistic about confirming one that did go out |
| Manual order venue price cap | $127.50 | ✅ venue | checked FIRST and binds when the collar cannot measure a reference. The venue rejects above it rather than clamping |
| Publisher perf bound | ≤ 10 ms/tick AND ≤ 5% of the 500 ms tick interval | 🟡 re-cut 12-08b | replaces the spec's original "within 10%" — a ratio against a 4.5 ms base could not survive one 208 KB `json.dumps`. Measured: 4.92 ms, 0.98% |
| Manual-command reply timeout (proxy await) | 5 s | 🟡 proposed | timeout → indeterminate, resend reuses ref |
| Panel staleness thresholds | house 3 s/10 s · book 30 s/120 s · quote 60 s (amber/red) | 🟡 proposed | panel-side; tape has no red state |
| Centrifugo token TTL | connection 3600 s · house subscription 900 s | 🟡 proposed | session cookie authoritative |
