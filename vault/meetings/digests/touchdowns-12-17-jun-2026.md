---
description: "Digest of the 12–17 June 2026 touchdown syncs — onboarding flow locked, IPO draft naming, launch dates (CFB 22 Aug / NFL 2 Sept), and the SSP-first ad stack"
---

# Touchdown Sweep — 12–17 June 2026

> **Type:** Consolidated digest of touchdown (sync) meetings
> **Date compiled:** 2026-06-18
> **Sources:** [[12-06-2026-touchdown]], [[15-06-2026-touchdown]], [[17-06-2026-touchdown]]

Touchdowns are multi-topic status syncs. This digest captures the durable signal: **definitional changes** (things that change what a component *is*), **confirmations** of previously-pending items, and **genuinely new items** to triage. Pure build-status, banter, and scheduling logistics are omitted.

This sweep is dominated by two threads. First, the **pre-launch app** is taking concrete shape: the onboarding flow is locked (email code, then Persona KYC, then the IPO page), the IPO surface is named the **"IPO draft"**, and the launch dates firm up (College Football IPO **22 Aug**, NFL **2 Sept**). Second, advertising moves from "build nothing until we have advertisers" toward an actual **programmatic operating model**: Brett produced a full **programmatic media playbook** (17 June) that sets an **SSP-first stack on AppLovin MAX** with **Kevel pushed to phase 2** for moment-based sponsorships. The market-maker requirement also resurfaces across all three calls.

> **Parked (not extracted):** The 15 June call contained an extended **strategic / contingency discussion** (advertising-commitment risk ahead of launch, a possible university-only fall challenge, and an investor conversation). Per the product owner this was standup overflow that should not have happened in a sync and is **not** written into the vision, components, or any changelog. It is recorded here only so the conversation is traceable to a date. No graph impact.

---

## Per-component synthesis

### Customer Onboarding
- **Onboarding flow locked (17-06):** create account, **email verification code** (auto-fills on mobile), **Persona ID check**, then the user lands inside the app on the **IPO page**. First in-app action is browse and buy (buy-only during the IPO phase). _(17-06)_
- **Persona effectively done (12-06):** KYC integration is built; the tZERO-side wallet allocation is "grab an ID from the pool and allocate". A details call with the tZERO engineers (Hassan / Abhishek) is set for the following week. _(12-06)_
- **Wallet allocation timing resolved (17-06):** wallet IDs do **not** need to be provisioned at signup. They can be allocated the **day before trading starts** by feeding a small data payload to tZERO, which returns a pre-generated wallet ID. Troy has set up the wallets. Not on the pre-launch critical path. _(17-06)_
- **Launch blocker = the Apple developer account (17-06):** this is the single biggest gating item for the pre-launch app. Target is end-of-June to early-July if Apple approval clears; Google Play runs in parallel. A functional prototype build is expected in the prototype space by Mon–Tue. _(17-06)_

### Information Layer
- **Pre-launch data preview (15-06):** before live data exists, the app exposes **Sport Radar historical data** (additions/subtractions, schedule, historical win-total projections), with the **trading features grayed out** plus a **countdown** to the IPO dates. Cody argued for going back to **2013** so users can build predictive models for hours pre-launch; George preferred a **one-year-minimum** scope for simplicity. Data-depth decision still open. _(15-06)_
- **Title-sponsor splash screen (15-06):** a **2–3 second** branded welcome screen on app open ("welcome to the InPlay Trading Challenge, brought to you by [sponsor]") that dissolves into the main interface. New advertising surface on Discovery / Home. _(15-06)_

### IPO Module
- **Named "IPO draft" (17-06):** chosen over "draft board" (too close to fantasy sports) and bare "IPO" (unfamiliar to users). A **"What is an IPO draft?"** link sits to the right of the title and routes into Education to explain the mechanic, why to buy IPOs, and what a position means. _(17-06)_
- **Inventory visibility (17-06):** Edwin wants to **hide shares-remaining** until the offering is near close (for example only surface it when under ~500k shares left). A percentage display was rejected (would read 0% at the start and look weak). Implies a **straw buyer / market maker** to fill unsold inventory so an offering never looks like it had zero sales. _(17-06)_
- **Launch dates firm up:** College Football IPO **~22 Aug**, NFL **~2 Sept** (12-06 referenced an "August 22nd" launch; 15-06 and 17-06 confirm the two-date split). Refines the existing IPO Scheduling window note (NCAA ~Aug 20 / NFL ~7 days pre-Sept 9). _(12-06, 15-06, 17-06)_
- **Synthetic off-field pricing for the pre-launch preview (15-06):** IPO pricing for the preview combines a **synthetic on-field** number (from betting lines / futures) with a **synthetic off-field** number derived from a per-game ad-spend model (a game's ad spend distributed by each team's share of trade volume). Ad spend is not published until the earnings reports. This is a preview/simulation pricing input, not a live-trading decision. _(15-06)_

### Earnings Report
- **Placement finalised (15-06):** the earnings report gets its **own page** (reached from the more / discover area) **plus an embedded earnings box** on each team page, with the **trade button kept accessible**. A **push notification fires ~15 minutes before** the release. Consistent with the existing batched-release feed design. _(15-06)_

### Trading
- **Market maker required (12-06, 15-06, 17-06):** a recurring thread. **Kevin Murray (Head Execution Trader)** is leading the market-making algorithm work with George, position-based rather than high-frequency ("reflective of opinion in the market that day"), possibly with a data-science intern. Edwin separately flags the need to **build an internal market maker** (likely tZERO-integrated) to guarantee **IPO fill and ongoing liquidity**, and wants at least one **dummy IPO plus simulated events** to test before launch. Brett proposed a focused Mon–Tue ~90-minute session. See [[architecture/open-questions]] and the flag below. _(12-06, 15-06, 17-06)_
- **tZERO real-time P&L confirmed (12-06):** the tZERO call resolved a buying-power concern: **tZERO will handle real-time P&L calculations** on user holdings (unrealised gains/losses recalculate dynamically). _(12-06)_

### Challenge Website
- **Rebuilt on a new template (12-06)** to enable **Google Analytics**; a fresh deployment link was issued. **Microsoft Clarity** heat-mapping is to be added across the websites (session recording, scroll/click heat maps, dwell time). _(12-06)_
- **Build priority (12-06):** "how to enter" first, then the **referral program**; the **prize-pool page is deferred** pending the numbers. The funnel principle is "two clicks away from trading", with download CTAs that do not bombard. _(12-06)_
- **Prize pool finalised (17-06):** **$21M base + $4M flex** (the flex is ad-revenue-dependent), giving the **"up to $25M"** messaging target the team wants to lead with. This ties to the standing compliance rule: it is always "up to $25M", **never "guaranteed"**. _(17-06)_

### InPlay Global Website
- **Press / media page signed off (12-06)** and integrated. _(12-06)_
- **Screenshots later (12-06):** the main site still needs **app screenshots** and visual refinement in a later pass; current focus is getting the bulk of the structure and copy in place first. _(12-06)_
- **Microsoft Clarity heat-mapping** also applies here (see Challenge Website). _(12-06)_

### Education
- **Delivery method still open (12-06):** the team needs to align on how the first iteration is executed. Options on the table: **TikTok-style 30–40 second highlight videos** plus detailed text, **AI-generated voice narration**, **code-generated animation slides**, and a **podcast format** (10–20 min) for accessibility. _(12-06)_
- **Brand-owned modules (12-06):** an alternative to InPlay producing the content is a **brand taking full ownership** of an education module (visual design, ambassadors, voice talent, and spoken ad breaks within the content). A podcast variant could carry **programmatic AI-voice ad reads** sprinkled through. Cross-references the Advertising sponsor-ownership layer. _(12-06)_
- **Beta + session (12-06, 17-06):** Kevin and Troy to finalise a first module for a beta test; a dedicated brainstorm session was scheduled (the **18 June education session**). The **"What is an IPO draft?"** explainer link (above) routes here. _(12-06, 17-06)_

---

## Cross-cutting updates

### Advertising

This sweep is where advertising acquires an operating model. Two artifacts drive it: Max's **AI brand-preview tool** (15 June) and Brett's **programmatic media playbook** (17 June). The playbook is captured as a full sub-component: **[[advertising/sub-components/programmatic-media-playbook/programmatic-media-playbook]]**.

- **SSP-first stack on AppLovin MAX (17-06):** the recommendation is to start with **AppLovin MAX as both ad server and mediator**, plug **8–12 SSPs** in as adapters, and **defer Kevel to phase 2** for moment-based sponsorships ("Doritos owns Cowboys touchdowns"). This is cheaper to stand up than going Kevel-first. **There is no Google Ad Manager.** This reframes the earlier "Kevel + Booster" stack: Kevel now sits **alongside** MAX for event-trigger inventory only. _(17-06)_
- **SSP prioritisation (17-06):** exchanges graded on ease of registration, inventory availability, and inventory value. **AppLovin MAX, Google AdMob, Liftoff, and PubMatic** are the day-one anchors. Brett has prior relationships at AdMob (possible 2–3 day onboarding) and at a premium SSP for later. Registration needs a domain-based business email (for example `novo@inplay-global.com`), payment/KYB setup, and MCP connectivity. _(17-06)_
- **Latency and scale constraints (17-06):** keep the portfolio to **8–12 SSPs** with back-fill segmentation; an ad must serve fast (the playbook targets sub-300ms render, with a 200ms bid timeout) or the bid is dropped and eCPM tanks. Real-time optimisation (floors, throttling, surge handling) runs on a **15-minute loop**. _(17-06)_
- **AI-agent ad-ops model (17-06):** rather than the traditional ~4.5-FTE ad-ops team, run **one human campaign manager plus an agentic AI workforce**. The cost target is to keep ad-ops inside a **~20% margin** on ad revenue. Novo to build the agent workflows. Captured in detail in the playbook sub-component. _(17-06)_
- **Impression model (17-06):** revised down to **~5 impressions/minute** for the core "degenerate trader" cohort (from an earlier ~20/min), giving **~25B+ impressions** over a four-month season at ~10,000 concurrent active traders. Video is the priority unit (baseline eCPM ~$3.58). _(17-06)_
- **AI brand-preview tool (15-06):** Max demoed a tool where an advertiser pastes a URL/logo and AI generates brand-specific ad previews across ~10 in-app units, with a download or contact-sales option. The plan is to put the link in outreach emails so advertisers self-serve a preview before a sales conversation ("teach them how to fish"). _(15-06)_
- **Advertiser KPI framework (15-06):** buyers care about **cost-per-acquisition and impressions/CPM** far more than engagement-minutes ("they don't care about your minutes"); benchmarks are coming from agency contacts. InPlay must prove out against standard IAB currency. Kevel offers flexible tracking and API access to build client-facing reporting. Feeds the still-undefined Analytics & Funnel Measurement concern. _(15-06)_

### Analytics & Funnel Measurement
- First concrete tooling signal: **Google Analytics** on the rebuilt Challenge Website and **Microsoft Clarity** heat-mapping across the sites. Plus the open **advertiser-KPI** question above (CPA / CPM / engagement-minutes, IAB currency). Still no event-schema or ownership decision. _(12-06, 15-06)_

### Push / CRM
- No new tooling decisions. The earnings **~15-minute pre-release push** (see Earnings Report) and IPO countdown alerts are the new notification surfaces this sweep. _(15-06, 17-06)_

---

## New items — triaged (decisions made 2026-06-18)

| Item | Source | What it is | Decision |
|------|--------|-----------|----------|
| **Programmatic media playbook** | 17-06 | Brett produced an end-to-end playbook: SSP roster (18 exchanges ranked), AppLovin MAX architecture, a 1-human + 9-AI-agent ad-ops operating model, KPIs, and a launch lifecycle | ✅ **Written as a sub-component under Advertising** ([[advertising/sub-components/programmatic-media-playbook/programmatic-media-playbook]]); key decisions summarised in [[components/components]]. Source artifact: `Inplay Outreach/ssp-priority-stack.html` |
| **SSP-first stack (MAX now, Kevel phase 2)** | 17-06 | AppLovin MAX as ad server + mediator on day one; Kevel deferred to phase 2 for moment-based sponsorships; no GAM | ✅ **Advertising cross-cutting reframed** in [[components/components]]; detail in the playbook sub-component |
| **AI-agent ad-ops at ~20% margin** | 17-06 | 1 campaign manager + agent workforce; cost must fit inside ~20% of ad revenue | 🚩 **Ad-ops P&L open question logged** in [[architecture/open-questions]]; model lives in the playbook |
| **Market maker (IPO fill + liquidity)** | 12-06, 15-06, 17-06 | Internal market maker, tZERO-integrated, to guarantee IPO fill and ongoing liquidity; Kevin Murray leading the position-based pricing algo; wants a dummy IPO + sim events to test | 🚩 **Flagged for a dedicated scoping session** (Mon–Tue ~90 min). Logged in [[architecture/open-questions]] and noted in [[trading/trading]]. Candidate **new `trading/market-maker` sub-component** once scoped. Continues the 08-06 market-making-algorithm flag |
| **IPO draft naming + inventory visibility** | 17-06 | "IPO draft" name; hide shares-remaining until near close; straw buyer fills unsold inventory | ✅ **Noted in [[ipo-module/ipo-module]]**; inventory-visibility / straw-buyer mechanics logged in [[architecture/open-questions]] |
| **AI brand-preview tool** | 15-06 | Self-serve advertiser preview across ~10 units, link goes in outreach emails | ✅ **Advertising note** in [[components/components]] |
| **Synthetic off-field pricing (preview)** | 15-06 | Ad-spend-based off-field number for pre-launch IPO pricing | ✅ **Noted in [[ipo-module/ipo-module]]** as a preview/simulation pricing input; not a live-trading decision |
| **Prize pool $21M + $4M flex** | 17-06 | Confirms the "up to $25M" messaging; flex is ad-dependent | ✅ **Noted in [[challenge-website/challenge-website]]**; reinforces the "never guaranteed" compliance rule |
| **Payment-provider / investor thread** | 12-06, 15-06 | Several payment companies interested (Pay.com / Teddy Sagi and others), non-exclusive; an investor conversation also occurred | ⏸️ **Commercial / corp-dev, not a product component.** Noted here only; no doc change |
| **App feedback backlog (~20 items, ~4 weeks old)** | 15-06 | Initial-release feedback not yet worked | ℹ️ **Status only** — delivery backlog, no doc change |
| **Meeting cadence (Mon / Wed / Fri)** | 12-06 | Restructured sync cadence | ℹ️ **Status only** |

---

## Doc updates applied (2026-06-18)

1. ✅ **New component + sub-component** — created [[advertising/advertising]] (light index for the Advertising cross-cutting concern) and [[advertising/sub-components/programmatic-media-playbook/programmatic-media-playbook]] (full playbook built from `Inplay Outreach/ssp-priority-stack.html` + the 17-06 call).
2. ✅ **Customer Onboarding** — update block: onboarding flow locked (email code → Persona → IPO page), Persona effectively done, **wallet allocation can be day-before** (not at signup), **Apple developer account = the launch blocker**.
3. ✅ **Information Layer** — update block: pre-launch **historical data preview** (2013-vs-1-year open), grayed-out trading + IPO countdown, **title-sponsor splash screen** (2–3s on open).
4. ✅ **IPO Module** — update block: **"IPO draft"** naming + "What is an IPO draft?" link, **inventory-visibility / straw-buyer** approach, **launch dates** (CFB ~22 Aug / NFL ~2 Sept), **synthetic off-field** preview pricing.
5. ✅ **Earnings Report** — update block: placement finalised (own page + embedded team-page box, trade button kept), **~15-min pre-release push**.
6. ✅ **Trading** — update block: **market maker** (Kevin Murray, position-based; internal MM for IPO fill + liquidity; dummy IPO + sim events to test; flagged for a session), **tZERO real-time P&L** confirmed.
7. ✅ **Challenge Website** — update block: rebuilt for **Google Analytics** + **Microsoft Clarity**, build priority (how-to-enter → referral, prize-pool deferred), **prize pool $21M + $4M flex = "up to $25M"**.
8. ✅ **InPlay Global Website** — update block: **press page signed off**, app screenshots in a later pass, Microsoft Clarity heat-mapping.
9. ✅ **Education** — update block: delivery debate (TikTok + AI voice + code-gen animation + podcast), **brand-owned modules** with programmatic ad reads, beta first module + 18-06 session, "What is an IPO draft?" link.
10. ✅ **components.md** — Advertising cross-cutting **reframed to SSP-first on AppLovin MAX** (Kevel = phase 2), AI-agent ad-ops, AI brand-preview tool, link to the new playbook sub-component; Analytics & Funnel Measurement gets GA/Clarity + advertiser-KPI signal.
11. ✅ **architecture/open-questions** — added rows: **market-maker design / IPO fill**, **IPO inventory visibility + straw buyer**, **ad-ops P&L (~20% margin)**, **advertiser KPI framework**.

Not applied (out of scope / parked):
- **15 June strategic / contingency discussion** — parked per the product owner; recorded in the note above and the meeting's post-call analysis, no graph impact.
- **Payment-provider / investor thread** — commercial / corp-dev, noted in triage only.
- **App feedback backlog, meeting cadence** — status only.
