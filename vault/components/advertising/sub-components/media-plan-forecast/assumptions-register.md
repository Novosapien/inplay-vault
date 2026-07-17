# Media Plan Forecast — Assumptions Register

> **Parent:** [[media-plan-forecast]]
> **Status:** Living register — single source of truth for what the forecast model may assume
> **Last review:** Edwin, three review rounds, July 2026 (see [[edwin-feedback-media-plan-jul-2026]])

Every forecasting assumption is registered here with Edwin's ruling. **Status values:** `Agreed` (use in the model), `Corrected` (Edwin replaced the original value; use the corrected one), `Open` (unresolved, must not silently enter the base case). Reference entries by ID (A1, I2, P3...).

---

## A — Audience

| ID | Assumption | Ruling | Status |
|----|-----------|--------|--------|
| A1 | MAU is a **monthly ramp from ~10K toward the Year 1 target**, never 500K flat from day one. v2's 234K season average accepted as directionally right; final ramp curve needs the corrected calendar (C2) | Flat 500K rejected outright | **Corrected** |
| A2 | "Highly Active" cohort (250K users, 6 games/week, ~94% of inventory) | Upside case only. Half the audience at upside frequency is not a base case | **Corrected** |

## I — Inventory

| ID | Assumption | Ruling | Status |
|----|-----------|--------|--------|
| I1 | Opportunities per active hour: **60 downside / 120 base / 240 upside ceiling**. 240 = full screen capacity; 120 = ~50% delivery/utilisation of it, not a different architecture | Agreed three-case structure | **Agreed** |
| I2 | Refresh architecture: **four separately defined ad units** (Gamecast upper-left display, lower-left native/display, Win Probability slim, Market Price slim), each on a **60-second viewable refresh**, staggered at 0/15/30/45s. Refresh timer starts on viewability, pauses on background/out-of-viewport/video/Volatility overlays. Each unit = own auction, own ad-unit ID, own reporting | 15-second single-banner rotation **banned** (Google: 30s minimum, 60s recommended, declared + viewable-only). Strictest demand partner governs. Pending AppLovin's written answers to the 10 questions before locking | **Agreed** (conditional on AppLovin) |
| I3 | Terminology: pre-waterfall volume is **"eligible ad opportunities"**, never "impressions" | Required relabel | **Corrected** |
| I4 | Display yield reference formula: 180 min × 4/min × 60% fill × 80% viewability × 95% (1−IVT) ≈ **328 quality-adjusted impressions per full 3-hour user-game** (720 eligible opportunities) | Agreed as the reference calculation | **Agreed** |
| I5 | Season event count: **2,116 live events** | Suspected double-count (team appearances vs unique physical games). Only valid if each Team Company has a separate Gamecast, both generate inventory, and no user session is counted twice | **Open** |
| I6 | Live-game inventory share: deck shows ~9,100 total opportunities/HAU/month with live-game at 42.9%, but 120/hr × 6 games × 3h × 4.33 wk ≈ 9,353 for live-game alone | Formulas cannot all be true; Brett to supply the actual formula | **Open** |
| I7 | Inventory allocation: ~90% programmatic / 10% direct reserve | Unexplained. Unsold direct reserve: programmatic backfill or nothing? Must be explicit | **Open** |

## P — Pricing

| ID | Assumption | Ruling | Status |
|----|-----------|--------|--------|
| P1 | Gross blended CPM is **staged, not flat**: Launch $2.50 → Early scale $3.25 → Validated audience $4.25 → Strong PMP/video mix $5.50+ | Flat $4.50 (v1) and flat $2.50/$7.43 (v2 base/upside) all rejected | **Corrected** |
| P2 | Net realized eCPM targets per stage: $1.50–1.75 / $2.00–2.25 / $2.75–3.00 / $3.75–4.25 | Agreed target structure | **Agreed** |
| P3 | First-party-data uplift: **0% at launch**, 10% once audience validated, 20% once PMP/direct demand established, 35% only with demonstrated performance | Automatic 35% for possessing KYC data rejected. Uplift follows advertiser demand, not data possession | **Corrected** |
| P4 | Format mix (base share of filled inventory): banner/display 55%, native/in-feed 20%, outstream video 15%, interstitial 5%, rewarded video 5%. Weighted-average formula must be visible; outstream needs its own rate; rewarded stays small (affirmative user choice, cannot inflate the blend) | Required structure | **Agreed** |
| P5 | Channel mix after fill: open auction 80% @ $3.25 gross (31% channel cost), PMP 15% @ $6.50 (20%), direct guaranteed 5% @ $10.00 (15% sales cost) → **~$4.08 gross blend, ~$3.00 net before tZERO, ~$2.70 net to InPlay** per 1,000 quality-adjusted impressions | Agreed as the defensible base mix | **Agreed** |
| P6 | **Rate card ≠ realized price.** Sales quotes the rate card; the model uses realized. E.g. PMP $8 → $6–6.50; direct display $12 → $8–10; native play unit $15 → $10–12; Volatility Moment $25 → $15–18; 6s video $30 → $20–24; 15s video $40 → $27–32; halftime $55 → $35–42 | Two-column pricing mandatory | **Agreed** |
| P7 | **$3.25 prices open-auction display only.** Never Volatility Moments, field video, or Gamecast sponsorship. Five separate pricing models per screen (see [[media-plan-forecast]]) | Key pricing rule | **Agreed** |

## W — Waterfall and Deductions

| ID | Assumption | Ruling | Status |
|----|-----------|--------|--------|
| W1 | Single waterfall order: **eligible opportunities → served (fill) → valid (IVT) → viewable/billable → gross revenue → net InPlay revenue**. Fill and viewability live in the impression waterfall, not as repeated eCPM haircuts | v1's stacked deductions (60% fill × 78% viewability × 5% IVT × 31% exchange × 20% commission) partly double-counted | **Corrected** |
| W2 | 31% exchange cut = the programmatic selling friction. **20% sales commission applies to direct-sold inventory only**, never on top of an SSP deduction | Required separation | **Corrected** |

## E — Economics

| ID | Assumption | Ruling | Status |
|----|-----------|--------|--------|
| E1 | tZERO economics in every case: **10% of Net Simulation Marketing Revenue, capped at $1.75M aggregate/month, no fixed fee** for the 2026 football challenge. (v1's $26.8M → $24.12M after tZERO, illustrative) | Mandatory inclusion | **Agreed** |
| E2 | Direct-sold ($600K) and territory ($300K) revenue: **$0 in downside, probability-weighted in base, full only in upside**. Uncontracted until signed; the tZERO fee waiver is proposed economics, not a purchased territory | Required treatment | **Corrected** |
| E3 | CAC: paid-media CAC **$25**; "blended $1.96" is mislabeled (paid spend ÷ ending users). **Fully loaded CAC still to be calculated** and must include creative/agency, referral rewards, promotional cash, affiliate payments, attribution and fraud costs. Organic/referral share ~**92%**, not 98% | Terminology correction + open calculation | **Open** |
| E4 | **Sensitivity matrix required** separating: 120 vs 240 opportunities/hour; low vs staged vs validated CPM; audience downside/base/upside; programmatic-only vs contracted direct. Upside must not move several assumptions at once | Required deliverable | **Open** |

## C — Calendar

| ID | Assumption | Ruling | Status |
|----|-----------|--------|--------|
| C1 | Model the **actual 142-day challenge period (~Aug 22 → Jan 10)**. No four-month or six-month annualisations as headline; the six-month Aug–Feb figure is an upside extension only | Required | **Agreed** |
| C2 | Launch period and competition period get **separate date ranges**. v2's audience curve (Aug 1 → ~Dec 19) omits January entirely | Correction required in v3 | **Open** |
