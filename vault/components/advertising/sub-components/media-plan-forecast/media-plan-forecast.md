# InPlay Trading Challenge — Media Plan Forecast

> **Component:** [[advertising]]
> **Date:** 2026-07-17
> **Status:** Active (model under revision, not yet the business-model base case)
> **Owner:** Brett (model build) / Edwin (review + sign-off)
> **Sources:** _[[edwin-feedback-media-plan-jul-2026]]_ · deck artifacts in shared: `InPlay Media Plan 500K`, `InPlay Media Plan - Base 120`, `InPlay Media Plan - Upside 240`, `InPlay Media Plan Calculator.pdf`

---

## What This Is

The Media Plan Forecast is the advertising revenue model for the trading challenge: the audience, inventory, pricing, and revenue-waterfall assumptions that produce the ad-revenue base case used with tZERO, Hard Rock, and investors. It is the successor to the "minutes to impressions forecast calculator" Brett committed to in the 18-29 June touchdowns.

The model is iterating through review rounds with Edwin. **No version is yet approved as the business-model base case.** Every forecasting assumption is tracked in the [[assumptions-register]], with Edwin's ruling recorded against each one. The register is the single source of truth for what the model may and may not assume; deck versions come and go, the register persists.

## Model Version History

| Version | Artifact | Headline | Edwin's verdict |
|---------|----------|----------|-----------------|
| v1 (16 Jul) | `InPlay Media Plan 500K` | $26.8M net over 4 months, 19.4B impressions, 500K MAU flat, $1.39 net eCPM | **Not defensible as base case.** "A media-sales case, not a defendable financial forecast." Inventory defensibility 3/10, investor-ready 5/10. Uses upside frequency (240/hr via 15-second rotation) for half the audience as base |
| v2 (17 Jul) | `InPlay Media Plan - Base 120` + `InPlay Media Plan - Upside 240` | Base $3.29M / Upside $20.01M over the 142-day challenge, 234K average MAU ramp | **Materially better, still not the forecast.** Base 120: 6.5/10 as internal planning summary. Upside 240: 4.5/10 as forecast, 7/10 as ceiling illustration. Nine corrections required (below) |

**What v2 fixed** (per Edwin): the opportunity-to-billable waterfall is now distinguished; average ramp audience (234K) replaces flat 500K; uncontracted direct sponsorship excluded from base; tZERO's 10% share and $1.75M monthly cap included; the $3.98 rate-card blend is arithmetically correct; the 142-day challenge is separated from the six-month extension.

## Required Corrections (v2 → v3, from Edwin's third review)

1. **Reframe the 240 case.** It is not a "15-second rotation." Correct description: four independently served placements, each refreshing every ~60 viewable seconds, producing up to 240 eligible opportunities per active hour. 120 base = ~50% utilisation of that capacity, not a different technical architecture.
2. **Fix the calendar.** Audience curve runs Aug 1 to ~Dec 19 while the 142-day competition runs ~Aug 22 to Jan 10. January is missing. Launch period and competition period need separate date ranges.
3. **Fix CAC language.** $1.96 is paid spend per ending user, not CAC. Report paid-media CAC ($25), fully loaded CAC (still to be calculated, must include referral rewards, creative, promo cash, affiliate, attribution/fraud costs), and organic share ~92% (not 98%).
4. **Reconcile live-game inventory.** At 120/hr the formula gives ~9,353 live-game opportunities per highly-active user per month, but the deck shows ~9,100 total with live-game at only 42.9% of inventory. Brett to supply the actual formula.
5. **Stage the CPM through the season.** Neither case levels CPM. Use the staged ramp (see register P1/P2); Edwin expects a credible central forecast to land between $3.29M and $20.01M.
6. **One assumption at a time in upside.** The upside doubles inventory, ~triples CPM, and adds direct sales simultaneously. Build the sensitivity matrix (register E4).
7. **Make the 90/10 programmatic/direct allocation explicit.** Does unsold direct inventory get programmatic backfill or nothing?
8. **Fix the upside eCPM arithmetic.** $20.01M / 4.23B billable = ~$4.73 net eCPM, not $4.66.
9. **Deliver the editable model.** Current decks are flattened PNGs in PowerPoint. Edwin requires the source calculator with audience, surface, and revenue formulas, plus the editable design file.

**Next deliverable:** one integrated model with base / downside / upside controls (not two disconnected decks), built on the agreed assumptions in the register.

## Screen Pricing Structure (Edwin's second review)

The Gamecast screen is not priced with one CPM. Five separate pricing models, each a row in the financial model:

| Product | Inventory driver | Selling unit | Base realized price |
|---------|------------------|--------------|---------------------|
| Standard display | Active minutes × 4 opportunities/min | Quality-adjusted CPM | $3.25–$4.08 gross blend |
| Native play-by-play unit | Qualified native views | vCPM | $10 |
| Volatility Moments | Qualified moment exposures | vCPM | $15 (rate card $25) |
| Field video (6s / 15s / halftime) | Completed views | CPM / CPCV | $22 / $28 / $38 |
| Presented-by modules + Gamecast territory | Contract | Fixed fee + escalators/overage | Win Prob & Market Price $500K floor each; territory $2M min → $9M cap |

Rule: **$3.25 belongs only to open-auction display.** It must never value Volatility Moments, field video, or the Gamecast sponsorship. Sponsorship territory revenue enters base only at contracted minimums; CPM value drives the escalators.

## GTM Implication (not a forecast assumption)

Edwin's second review also reset the direct-sales motion: stop leading with $2-9M territory packages pre-audience; sell a **Charter Advertiser Pilot** ($50K pilot / $150K launch partner / $300K charter partner, all with guaranteed delivery + makegood), target media-investment roles rather than CMOs, transact via Programmatic Guaranteed for agencies, run two commissioned independent sellers alongside founder-led sales, and get an explicit representation answer from Katz. Prelaunch target: 3-5 paying pilots, $250K-$750K contracted. This belongs to the [[advertising]] sales motion and is recorded here only because the pilot guarantees (impression quantities) must reconcile against the rate card in this model.

## Open Items

- AppLovin must answer the ten written questions on the four-unit / 60-second refresh architecture before it is locked into the forecast (see register I2).
- The 2,116-event count needs reconciliation: team appearances vs unique games (register I5).
- Fully loaded CAC calculation (register E3).
- Sensitivity matrix (register E4).
- v3 integrated model + editable calculator delivery.
