# InPlay Trading Challenge — Programmatic Media Playbook

> **Component:** [[advertising]]
> **Date:** 2026-06-17
> **Status:** Reference (operating model, not a user-facing flow)
> **Owner:** Brett (ad-tech / programmatic) + Novosapien AdOps
> **Sources:** _[[meetings/17-06-2026-touchdown]]_ · source artifact: `Inplay Outreach/ssp-priority-stack.html` (deployed copy in `ssp-guide-deploy/`)

---

## What This Is

The Programmatic Media Playbook is Brett's end-to-end guide to monetising InPlay's mobile inventory through programmatic demand. It was produced for the 17 June touchdown off the back of Cody's request and Edwin's outreach, and distributed to the team as the foundational reference for the ad business. It answers four questions: **which exchanges to onboard and in what order**, **how they wire together**, **how the day-to-day is run**, and **what each exchange is worth**.

Headline framing from the artifact:

- **18** exchanges ranked, **9** AI ops agents, **~63%** ops cost saved, **1** human FTE needed.
- Prepared **17 Jun 2026**, launch target **Aug–Sep 2026**, audience **US mobile-app, KYC 21+**.
- Two revenue motions sit side by side: **direct-sold sponsorships** (served via the mediator now, Kevel in phase 2) and **programmatic generalised inventory** (the SSP portfolio). This doc is the operating model for the programmatic side. See [[advertising]] for the split.

The playbook is organised into four parts: the SSP roster, the architecture, the operating model, and per-exchange cards.

---

## Part I — The SSP Roster

Every supply-side platform and ad network worth considering, ranked on three axes, scored 1–5 each. Higher composite means onboard sooner.

**Scoring axes:**
1. **Ease of registration.** 5 = open access, instant. 1 = months of legal review and a hard volume gate. Time-to-first-impression matters more than the last 5% of CPM at launch.
2. **Inventory availability.** Does the SSP buy US mobile in-app sports inventory at InPlay's scale? 5 = perfect format/channel match. 1 = wrong channel (CTV-only, web-only, geo-wrong).
3. **Value and premium.** Net CPM after take rate, DSP quality, brand-vs-performance mix. 5 = premium brand demand, transparent terms. 1 = bottom-tier net CPM, opaque pricing.

### Priority stack

| # | Exchange / Network | Tier | Ease | Avail. | Value | Composite | Role |
|---|--------------------|------|------|--------|-------|-----------|------|
| 1 | AppLovin MAX | Anchor | 5 | 5 | 4 | 14 | Mediator SDK + Exchange demand |
| 2 | Google AdMob | Anchor | 5 | 5 | 4 | 14 | Demand floor (AdSense + DV360) |
| 3 | Liftoff Monetize | Anchor | 4 | 5 | 5 | 14 | Performance + sports brand demand leader |
| 4 | PubMatic | Anchor | 4 | 5 | 5 | 14 | Independent SSP, Net 30, in-app strong |
| 5 | Unity LevelPlay | Wave 2 | 5 | 5 | 3 | 13 | Backup mediator / A-B competitor |
| 6 | Smaato | Wave 2 | 5 | 5 | 3 | 13 | Mobile-native independent SSP |
| 7 | ironSource (Unity) | Wave 2 | 5 | 5 | 3 | 13 | Performance + video via LevelPlay or MAX |
| 8 | AdColony / Digital Turbine | Wave 2 | 4 | 5 | 4 | 13 | Interstitial + sports brand demand depth |
| 9 | OpenX | Wave 2 | 4 | 4 | 4 | 12 | Solid independent SSP, US DSP-strong |
| 10 | Sharethrough | Premium | 4 | 3 | 5 | 12 | Native ads specialist, high CPMs |
| 11 | Magnite | Premium | 2 | 4 | 5 | 11 | Premium DSPs, needs traffic to onboard |
| 12 | Triplelift | Premium | 3 | 3 | 5 | 11 | Native + outstream video |
| 13 | Verve Group | Premium | 3 | 4 | 4 | 11 | Cookieless/ID-less story; overlaps Smaato |
| 14 | Index Exchange | Premium | 2 | 3 | 5 | 10 | Premium brand demand, selective gate |
| 15 | InMobi | Selective | 3 | 4 | 3 | 10 | Independent mobile-first |
| 16 | Chartboost | Selective | 4 | 3 | 3 | 10 | Gaming-heavy; via Liftoff |
| 17 | Mintegral | Selective | 4 | 4 | 2 | 10 | Strong CPMs, brand-safety overhead |
| 18 | Pangle (ByteDance) | Defer | 3 | 4 | 2 | 9 | Strong demand, geopolitical risk |

**Day-one anchors:** AppLovin MAX, AdMob, Liftoff, PubMatic. Brett has prior country-manager relationships at AdMob (onboarding potentially compressible to 2–3 days) and a VP-Europe connection at a premium SSP for the later premium wave.

### The portfolio approach

The right answer is a curated portfolio of **8 to 12 exchanges**, not "plug in everything and let MAX sort it out", and not "one or two and keep it simple". Both extremes break the economics.

**Why multiple exchanges:** auction competition lifts CPM (2 bidders typically +30–50% over 1; 5 bidders add another 15–25%; the curve flattens beyond 8); fill-rate insurance (one SSP caps around 60–75% fill, three in parallel cover ~95%); format coverage (no SSP is best at every format); payment-term diversification (Net 30 / 60 / 90 smooths cash flow); and suspension blast-radius (lose one SSP, lose 20% of revenue, not 100%).

**Why not all of them:** bidding latency (each adapter adds 50–150ms; 20 in parallel can push render past 500ms); diminishing CPM returns beyond 8–10 bidders; reconciliation overhead (every SSP is a separate invoice and three-way match); brand-safety surface area; demand cannibalisation (many SSPs source the same DSPs, so a duplicate just splits the same bid); and account-management cost (QBRs, check-ins).

**The optimal mix** spans four functional roles, skewed toward whichever role earns the most revenue:

| Role | Count | What it does | InPlay picks | % of revenue |
|------|-------|--------------|--------------|--------------|
| Anchor Demand | 2 | Always-on baseline fill, all formats | AppLovin Exchange, AdMob | ~35–45% |
| Premium Independent | 3–4 | Brand DSP premium, PMP deal-IDs | PubMatic, OpenX, Magnite, Index | ~25–35% |
| Performance / Video | 2–3 | Performance, UA, brand video | Liftoff, ironSource, AdColony | ~15–25% |
| Format Specialist | 1–2 | Best-in-class for one format | Sharethrough (native), Smaato (mobile) | ~5–10% |
| Selective / Conditional | 0–1 | Only if a unique niche justifies the overhead | Mintegral (strict controls) | ~0–5% |
| Reject | 0 | Wrong channel / audience / risk | Pangle, web-only, CTV-only | 0% |

**Sweet spot: 8 to 11 SSPs in production**, anchors doing ~40% of revenue, premium independents ~30%, performance/video ~20%, format specialist ~5%. Add beyond 12 only when revenue data proves the incremental SSP earns more than its operational drag costs.

---

## Part II — The Architecture

**One picture: AppLovin MAX is both the ad server and the mediator.** Every SSP plugs into MAX as an adapter. AdMob is one demand source among many, not a separate ad server. **There is no GAM.**

```
[ InPlay App ]
   ad slot fires (banner under live ticker · interstitial between rounds · premium home-page header)
        │
        ▼
[ AppLovin MAX SDK ]  ← the only ad-related SDK in the app
   ad server + mediator + CMP. House ads, frequency caps, targeting, A/B, in-app auction, reporting.
   (Phase 2: InPlay Kevel Ad Serving sits alongside, intercepting only moment-trigger slots, falling
    through to MAX for normal inventory.)
        │
        ▼  priority cascade (top-down, highest CPM wins inside each tier)
   1. House Ads & Direct-Sold Sponsorships   → exec-team direct deals (Doritos, Allstate). No SSP take. InPlay keeps 100%.
   2. In-App Bidding Auction (real-time)      → all SSPs bid simultaneously (~200ms each). Highest bid wins. Majority of revenue.
   3. Waterfall Fallback (legacy)             → sequential, rare in 2026, kept as safety net.
        │
        ▼
[ Demand Sources / SSPs as adapters ]  → each runs its own DSP auction, returns one bid
   Day one:      AppLovin Exchange · AdMob · Liftoff · PubMatic
   Months 1–3:   Smaato · OpenX · ironSource · AdColony/DT · Unity LevelPlay (offerwall optional)
   Months 3–9:   Magnite · Index · Sharethrough · Triplelift / Verve
        │
        ▼
[ DSPs / Brand Advertisers ]  → The Trade Desk, DV360, Amazon DSP, MediaMath, Yahoo, Meta Audience
   (same DSP may bid via multiple SSPs; duplication is fine, only the highest bid wins inside MAX)
        │
        ▼
[ Delivery & Reporting ]  → winning creative renders in <300ms; impressions logged both sides;
   each SSP reports revenue nightly; MAX aggregates into one dashboard.
        │
        └──► Continuous optimisation loop: data → InPlay analytics → ad ops (1 human + AI agents)
             → feeds forward into MAX (floors per SSP, waterfall A/B, kill underperformers,
               push first-party KYC segments to top bidders, frequency caps, creative blocklists).
```

**The path to Kevel:** MAX runs all programmatic and house-ad inventory on day one. When direct-sold moment-based sponsorships outgrow house-ad trafficking, **InPlay Kevel Ad Serving** is added in phase 2 to serve event-trigger slots ("Doritos owns Cowboys touchdowns") via its decision API, falling through to MAX for everything else. A **Kevel-ready house-ad/direct-sold SDK abstraction is built at setup** so the team can flip to Kevel later without engineering rework.

---

## Part III — The Operating Model

A 1M-user mobile publisher in this category typically staffs a **4.5-FTE AdOps team** (Head of Monetization ~$280K, Senior AdOps Manager ~$170K, Yield/Programmatic Analyst ~$135K, Ad Tech Engineer ~$245K, plus shared finance). The Novosapien model collapses that to **one dedicated human lead plus an agentic AI workforce** running the same surveillance, reconciliation, optimisation, and reporting loop 24/7, with the human reserved for judgment-bound work. This is the ~63% ops-cost saving and the "fit inside a 20% margin" target raised on the call.

### The human lead

Owns the InPlay relationship end to end: SSP commercial negotiation, MFN and rev-share renegotiation, MSA redlines, brand-safety calls, sponsor-conflict resolution with the InPlay exec team, game-day crisis comms, and the weekly exec review. **Approves every AI-proposed move above a dollar-impact threshold.** The single accountable human on Slack at 11pm on a primetime Sunday.

### The 9 AI agents

| Agent | Replaces / does | Cadence |
|-------|-----------------|---------|
| Yield Optimization | Floors, waterfalls, bidder priority, A/B tests in MAX | Every 15 min (major floor pushes 2x/day) |
| Anomaly Detection | Fill / eCPM / render watch | 60s polling |
| SSP Scorecard | Tier, PIP, sunset memos | Weekly |
| Creative QA | Blocklist drift, malicious-creative kill | Continuous |
| Fraud / IVT | SIVT make-goods, IDFA entropy, cohort quarantine | Streaming |
| Reconciliation | MAX vs SSP vs bank three-way match | Daily |
| Reporting | Daily / weekly / monthly, ad-hoc via Slack | Scheduled + on-demand |
| SSP Relationship | Drafts, QBR scheduling, inbound triage | Ongoing |
| Forecasting | 13-week rolling, game-day nowcast | Ongoing |

### The lean tooling stack

One mediator (**AppLovin MAX**), one warehouse (**Google BigQuery**), reporting (**Looker Studio** + the **Novosapien Reporting App**), comms (**Slack** + **Obsidian** git-backed runbooks), and the AI plane (**Novosapien Agent Platform** + **Anthropic Claude API**, Sonnet + Opus with aggressive caching, talking to SSP / BigQuery / Slack **MCP servers**). No SaaS sprawl; everything else deferred until a buyer or an incident forces it in.

### Calibrate before you optimise

The first **3 to 6 months are calibration, not optimisation**. Aggressive optimisation in the first 90 days destroys data: bid-density curves, eCPM-by-daypart patterns, and SSP-by-format breakdowns do not stabilise until there are at least 30 days of post-launch traffic plus a full football-season cycle to anchor against. Quarter 1 is telemetry, baselines, and observing without intervening. From Quarter 2 the optimisation loop opens up.

### Core KPIs (reported weekly)

| KPI | Target |
|-----|--------|
| ARPDAU | $0.15–0.30 at launch, $0.30–0.50 by end of season |
| Net eCPM (blended) | $4–6 at launch, $6–9 mature |
| Fill rate | ~30% launch baseline, ~45% Y1 Q4, >80% mature |
| Render rate | >97% |
| Viewability | >70% banner, >85% video |
| Auction latency | <200ms p50, <400ms p95 |
| Discrepancy | <3% per SSP |
| Ad-quality incidents | <5/week, goal <1 |

**Portfolio health signals:** 4–6 active bidders per auction (<3 means CPM compression); >70% bid-response rate per SSP (<40% is dead weight); top SSP <35% of revenue (>50% is critical suspension risk); 3+ bidders per format; <2x DSP overlap; <250ms p95 latency; <3% discrepancy per SSP.

### Optimisation cadence

- **Every 15 minutes (AI-driven, human approves material moves):** floor micro-adjustments per unit/geo/daypart; SSP bid throttling (drop adapters >300ms for 3 cycles); live-event surge handling (NFL kickoff = 5–10x traffic, pre-warm bidders, raise floors on sports inventory); fraud-cohort quarantine; adapter heartbeat.
- **Daily (AI executes, human reviews at standup):** waterfall re-ranking by 7-day eCPM; creative blocklist propagation; direct-sold pacing; three-way discrepancy reconciliation (auto-ticket >3%); eCPM drift detection; SDK/adapter health.
- **Weekly (human-led, Tuesday optimisation session):** A/B promote/kill (>5% lift); SSP scorecard (Tier 1 keep / 2 maintain / 3 PIP / 4 sunset-prep); format-mix analysis; viewability audit; Tier-1 AM check-ins; performance memo to InPlay exec.
- **Monthly:** full SSP review (kill anything <$50/mo); rev-share renegotiation prep; first-party KYC segment refresh (HOF / Starter / Rookie / Free-Agent + team affinity + deposit band); cash-flow / DSO tracking; blocklist refresh; board-pack appendix.
- **Quarterly:** rev-share + MFN renegotiation with top SSPs; QBRs; stack expansion/contraction review; privacy/consent audit (ATT, CCPA, EU CMP / TCF v2.2, state laws); AI-agent capability review (which tasks the workforce now owns end to end, next 2–3 to automate).

### Setup lifecycle (pre-launch, ~10 weeks elapsed / ~25 working days)

Key tasks and owners: developer infra + **app-ads.txt scaffolding** (hybrid, 2d); open and verify mediator + SSP accounts, tax/banking/KYB (human, ~5d over 2 weeks); negotiate and sign **SSP MSAs + IOs** (human, 4–8 weeks legal); **MAX SDK integration** into iOS + Android (human/InPlay eng, 5–8d, Novosapien advises); configure ad units, waterfalls, bidding with initial US floors (AI, 3d); wire SSP adapters + verify app-ads.txt lines via adstxt.guru (AI, 2d); build the **Kevel-ready house-ad / direct-sold abstraction** (human, 3–5d); privacy / ATT / Data Safety compliance pass (hybrid, 2d); **soft-launch traffic test** at 10–20k beta users to validate fill/latency/crash/SKAdNetwork before live load (hybrid, 2 weeks); ad-quality + brand-safety baseline blocklist (AI, 2d, excluding sportsbook competitors, predatory finance, alcohol-to-minors).

---

## Part IV — The Exchange Cards

The artifact carries per-exchange deep dives (onboarding steps, commercial terms, inventory type, net eCPM range, strengths, weaknesses, recommended action) for all 18 exchanges. These are not reproduced here; refer to the source artifact (`Inplay Outreach/ssp-priority-stack.html`) when onboarding a specific SSP. The four anchor cards (AppLovin MAX, AdMob, Liftoff, PubMatic) are the ones that matter for day one.

---

## Open Items (from the 17-06 call)

- **Ad-ops P&L:** confirm the 1-human + agent model fits inside a ~20% margin on ad revenue at the modelled impression volume. Logged in [[architecture/open-questions]].
- **The four anchor SSP applications** need to start immediately (week-1 timeline): domain-based business email (for example `novo@inplay-global.com`), payment/KYB accounts, MCP connectivity.
- **Impression model** to be reconciled with the inventory map: ~5 impressions/minute for the core trader cohort, ~25B+ over a four-month season at ~10k concurrent active traders; video the priority unit (~$3.58 baseline eCPM).
- **Relationship to the specialist-sponsorship territories** (in [[components/components#Cross-Cutting Concerns]]): the territories are the direct-sold motion served via house ads now and Kevel in phase 2; this playbook is the programmatic generalised inventory. The two should be reconciled into a single inventory map.
