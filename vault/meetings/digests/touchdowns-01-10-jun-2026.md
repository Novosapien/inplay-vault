# Touchdown Sweep — 1–10 June 2026

> **Type:** Consolidated digest of touchdown (sync) meetings
> **Date compiled:** 2026-06-09 (extended 2026-06-10)
> **Sources:** [[01-06-2026-touchdown]], [[03-06-2026-touchdown]], [[05-06-2026-touchdown]], [[08-06-2026-touchdown]], [[10-06-2026-Touchdown]]

Touchdowns are multi-topic status syncs. This digest captures the durable signal: **definitional changes** (things that change what a component *is*), **confirmations** of previously-pending items, and **genuinely new items** to triage. Pure build-status (deploys, banter, payment logistics) is omitted.

This is the build-sprint fortnight around a **sales conference (week of 9 June)** — much of the signal is the prototype coming to life (referral system, live Sport Radar data, app ad placements) plus a hard push to publish the Global Website before the conference. The 10 June call adds a **compliance incident + control** and **resolves the T0 wallet / buying-power ownership question**.

---

## Per-component synthesis

### Customer Onboarding
- **Persona contract SIGNED** (was "in legal review" in the May sweep). Implementation kicks off on intro from their sales to a tech/implementation engineer (onboard for ~8 weeks). Still **awaiting API keys** to wire into the flow. _(03-06, 05-06, 08-06)_
- **Onboarding flow built into the app** (Hassan) — create-account → optional referral-code entry (deep-link via QR being wired) → Persona ID check → **pass/reject** → QR/referral screen → into app. Demoed 10-06 (placeholder ID slowed to always pass). **Face-scan callback ~2–3 seconds.** _(08-06, 10-06)_
- **First-version app scope locked:** referrals + wallet + signup + **KYC (required, not optional)** + some live data for functionality. **Not** full in-app Apple trading. _(05-06, 08-06)_
- **Persona KYC speed validated:** government-ID + face-scan is ~99.5% AI-automated; approval in seconds. _(08-06, 10-06)_
- **App-store accounts:** **Google Play set up**; team being added. **Apple developer account reset to the beginning** — Apple must call/email **Edwin** to approve **Troy as company signatory** to sign the developer agreement (last time ~48–72h). _(03-06, 05-06, 08-06)_

### Referral
- **Referral system built and demoed** (Hassan). Confirms the documented mechanics: **lifetime-unique pre-generated codes** (tested ~1B users, no collision), QR-code page, referrer↔referee tracking table, **crediting gated on KYC approval** (currently a simulated approve button), **boost multipliers preset** for specific dates/weekends. _(05-06, 08-06)_
- **Cody's required share flow (refines Share Surfaces):** the referral/QR screen must be the **very next screen after KYC**; add **one-click social share** that prepopulates the *screen image* (not just text) into Instagram/X/text, ideally **per-platform styled**; after a referred user completes KYC, immediately surface **their own** unique code (feedback loop); also expose the code on the **profile page**. _(05-06)_
- **Wallet ownership clarified (10-06):** the **referral wallet is tracked by InPlay** (not T0); a **mechanism is needed to move funds from the referral wallet back into the trading wallet** (the <25K reload). _(10-06 — see Trading)_

### Information Layer
- **Sport Radar data live in the prototype** — real SR data streaming into the PWA; where data is placeholder it's explicitly labelled "demo data". _(05-06, 08-06)_
- **Replay simulation model:** SR feed is **fixed to a past point in time** (week 10 of 2024 in the 05-06 demo; 2025 season in 08-06) so completed games replay with **real** standings, results, injury reports, key-player stats, and **all moments per game** linked to a popup. Pricing/market data not yet linked. Live moments will run off the **SR provider simulation endpoint**. _(05-06, 08-06)_
- **Moments-per-game validated at ~18** (granularity can go up to ~170). Confirms Cody/Edwin's "15–20 highlight moments per game" premise. George: surfacing all 170 would dilute UX → **group moments by quarter** (Cody's playbyplay-widget pattern). _(08-06)_
- **Sport Radar entity-ID model:** one SR ID joins **play-by-play, AP editorial newswire, headshots, win-probability** across products. Pull **AP injury-article context** onto player cards (injuries are a major trade driver). Win-probability lives under the **global American-football API**, not the NFL API (IDs interoperate) — resolves George's 403 error. Headshots not yet licensed. _(08-06)_
- **Team page enriched:** all season stats, conferences, full results, week-level injury reports, key players. Decision: show **current + previous season only** (not 2024 as well). _(08-06)_

### InPlay Global Website
- **Full redesign (Max + Skye, ~5h joint session):** strong branding/brand colours; uses the **exact copy from Skye's deck** (no edits); **imagery stripped and added last** — establish text/copy on screen first, then build imagery around it (only the home hero had images at 05-06, rest to follow). _(03-06, 05-06)_
- **Home hero:** two players facing off (AI-generated); a **moments-of-the-game** section (turnover, QB limps off then returns → price spike) straight from Edwin's deck. _(05-06)_
- **Pages:** Home, **Partners** ("partner with InPlay"), Team (headshots), Football Challenge, **Careers** (job postings — AI-generated JDs need review; Troy + Brian writing real ones; go-to-market interns + more roles coming). _(05-06, 08-06, 10-06)_
- **Feedback applied:** **outline/"future" font made bolder/thicker/brighter** (was hard to read); team headshots cropped to **consistent framing/distance**; **remove the "Tony"/Anthony Verbillis quote**. _(05-06, 08-06)_
- **Lead routing:** every page has a CTA → **form with a reason selector** (just-a-user / advertising / media) → routed to the **appropriate email distribution list**; homepage has two CTAs (top + bottom). **Troy owns DL assignment** per category; Hassan wires the routing. _(05-06, 08-06)_
- **Mobile optimisation (10-06):** the **outline font overcrowds when scaled on mobile** and the **hero phone-screenshot gets cut off**. Decision: optimise **desktop→mobile** — thin outlines on desktop; restructure the hero so the phone screenshot **stacks below / tilts at a 3D angle** rather than being clipped to the side. Mobile-first rationale: conference visitors will hit the site on a phone first. _(10-06)_
- **Published before the Tuesday sales conference** after a page-by-page review (helmets improved). Further refinement continuing in the background. _(05-06, 08-06, 10-06)_
- **Press release:** Skye drafted a **T0 press release**; tZERO is also drafting one → **merge and time for Tuesday**. _(05-06)_

### Trading
- **T0 wallet / buying-power ownership RESOLVED (10-06):** **T0 owns and manages the trading wallet** (tied to the digital wallet). **InPlay tracks the referral wallet** and must build the **<25K reload mechanism** (referral → trading). **Cash wallet host = still TBD** (T0 vs third party). **Buying power: T0 does *not* calculate it** — they only do that in production *as the broker*. **InPlay must build an "InPlay market synthetic broker" element that tracks buying power.** ⚠️ Business requirements not yet written — Friday T0 session. _(10-06)_
- **Shorting mechanics (10-06):** shorting **increases** buying power — short 100K → receive 100K in funds → need 200K buying power to be able to close (buy back); a drawdown to ~100K triggers return of the shares. Hard on-chain — tokenization lacks the locates/reserve mechanisms traditional markets use. Troy is writing the **shorting business requirements**; **primary-offering (IPO) requirements done**; both for Friday. _(10-06)_
- *(May/early-June architecture signal — VPC + T0 integration — captured in the Trading doc's architecture note.)*

---

## Cross-cutting updates

### Advertising
- **In-app ad placements designed (Max)** and validated as **"elegant, not in-your-face"** (Troy): per-brand app heroes (Coca-Cola home, Gatorade discovery, Pepsi/Visa/Bud Light/FedEx/Amex pages); a redesigned MX/Amex banner **persistent across all game screens**. _(05-06, 08-06)_
- **Header lock vs scroll — decision:** leave the top sponsor banner **scrolling** for now (don't lock), keeping the design as **options to feel out advertisers**; big hero headers should *not* lock (too much screen). Priority order made explicit: **trader UX > advertiser > everything else**. Rationale: sponsorships are sold on **exposure-minutes** ("lock-and-load"), so the model must back the brand to hit promised minutes — but not at the cost of the trader experience. _(01-06, 05-06)_
- **"Territories" / page-ownership naming** floated — gamecast, information centre, referral bank — each a sellable "presented by" surface (Amex "owns the space" reference). _(01-06)_
- **Booster = too early.** It's an **order-management / ad-ops** system for scale; managing ~10 advertisers can be done **manually**. **Kevel is still required** even for sponsorship/impression serving — it places the sponsorship, rotates campaigns, and produces audits/metrics/minutes. Kevel call the following week. _(03-06)_
- **"Don't build until we have advertisers"** (Edwin) — first advertiser is likely Edwin himself; no ad server needed to place a static sponsor. _(03-06)_
- **Helmet realism (build asset):** replace flat SVG helmets with **AI-generated realistic helmets** for all **163 teams** (32 NFL + ~131 NCAA) using **exact team hex codes** (Kevin supplying; NFL done, NCAA in progress) + the "halo/gradient" effect. Pre-launch must-do; not a doc change. _(01-06, 03-06)_

### Cybersecurity & Data-Handling / Compliance Governance (new control, 10-06)
- **Incident:** the site-generation **AI agent invented a "trading challenge rules" policy** in the Global Website's legal footer (sourced from the learning repository) stating **"guaranteed prize money up to $25M"**. Edwin's hard rule: **always "up to $25M", never "guaranteed"** — a guarantee is real legal exposure ("could get sued by 50 states… on the hook for the $25M myself"). Caught and removed within ~1.5h.
- **Control adopted:** an **agent team reviews all copy before any deploy** — scans for sensitive/regulated terms ("guarantee", prize-money claims, securities-offer language) and blocks publish until cleared. AI-generated T&Cs/disclaimers stripped back to the **basic email-signature boilerplate**; **Troy to send disclaimer copy to external counsel (Marlin)** to confirm what's needed now vs at competition launch. Edwin's standard financial disclaimers required (no profit guarantee, "past performance…", "not an offer to sell securities"). _(10-06)_

### Push / CRM
- No new tooling decisions this sweep (HubSpot + Airtable stand from the May sweep). Website lead-form routing to per-category DLs is the operational join into CRM. _(05-06, 08-06)_

### Analytics & Funnel Measurement
- Website CTA→form→DL routing is the first concrete **top-of-funnel capture** join (reason-segmented). Feeds the still-undefined Analytics & Funnel Measurement doc. _(05-06, 08-06)_

### Internal Tooling (new this sweep)
- **CI-aware creative tooling + image repository.** Edwin spent ~36h hand-building a sales deck; agreed it should never fall on him. Brett/Max to build a **system prompt / skill** that bakes in CI + knowledge base for decks/creative, plus a **shared repository of approved images** + a ~1h best-practice training session. _(08-06)_
- **Agentic outreach at scale.** Brett to run agentic outreach alongside Edwin's manual brand outreach (liquor/wine brands) — package messaging + imagery + formatted email/deck per prospect, with Edwin tagged in to observe. _(08-06)_

---

## New items — triaged (decisions made 2026-06-09 / 2026-06-10)

| Item | Source | What it is | Decision |
|------|--------|-----------|----------|
| **Affiliate revenue stream (sportsbooks)** | 05-06 | FanDuel-style affiliate / rev-share — when a user leaves to place a bet then returns, InPlay still monetises the minutes (Edwin's "Schwab account" analogy). Conference targeting **operators**; "opening the floodgates to fill **$25M**" | ✅ **New monetisation lever — noted in Advertising/commercial.** Not a build component. Underpins the multi-sport argument below |
| **Multi-sport view-only (baseball/soccer/etc.)** | 05-06 | Re-raised: Cody can trial-activate SR real-time in one email. Show live data from other sports to prove live speed + stickiness | ⏸️ **May decision ("not doing this") stands; re-raised and now contested.** Edwin/Cody: monetise the minutes + affiliate rev-share → revisit as **v2.0 post-launch**. George: dilutes focus / drives users to betting apps. **Verbally tell prospects "we're adding other sports"; no build** |
| **InPlay synthetic broker (buying-power tracker)** | 10-06 | New architectural element — InPlay (not T0) must track buying power, as the synthetic broker; T0 only does this in production as the real broker | 🚩 **Open question RESOLVED + Trading note added; flagged for the Friday focused session** (business requirements being written). Not a standalone component doc yet |
| **Shorting mechanics (on-chain)** | 10-06 | Shorting increases buying power; close-out + share-return triggers; no on-chain locates/reserve. Troy writing business requirements | 🚩 **Trading note added; flagged for Friday.** IPO/primary-offering BRs already done |
| **Pre-deploy copy-review agent + legal disclaimer review** | 10-06 | Agent team scans all copy for sensitive terms before publish; counsel (Marlin) reviews disclaimers | ✅ **New control under [[Cybersecurity & Data-Handling]] cross-cutting concern + Global Website note** |
| **Market-making algorithm** | 08-06 | Edwin wants to **co-build a market-making algo over ~2 months** | 🚩 **Flagged for its own session.** Pricing/market-engine territory — outside the 12-component map. Logged in [[architecture/open-questions]] |
| **CI-aware creative tooling + image repository / agentic outreach** | 08-06 | Internal deck/creative skill + approved-image repo + agentic outreach at scale | ✅ **Internal tooling — noted in cross-cutting.** Brett + Max to build. Not a product component |
| **Helmet realism (163 teams)** | 01-06, 03-06 | AI-generated realistic helmets w/ exact hex codes, pre-launch | ✅ **Build asset / task.** Kevin supplying hex codes. No doc change |

---

## Doc updates applied (2026-06-09 / 2026-06-10)

1. ✅ **Customer Onboarding** — delivery note: **Persona contract signed** (awaiting API keys; impl engineer ~8 weeks), onboarding flow built into the app with **pass/reject** + ~2–3s face-scan callback, **KYC required in v1**, Google Play set up + Apple dev account reset.
2. ✅ **Referral** — changelog: system **built & demoed**; Cody's **one-click image-prepopulated social share** + **profile-page surface** + **post-KYC referral screen**; referral-wallet tracked by InPlay with <25K reload mechanism (cross-ref Trading).
3. ✅ **Information Layer** — touchdown note: **SR data live**, **replay-simulation model**, **~18 moments/game** (group-by-quarter), **SR entity-ID join model**, AP injury context, win-prob under global American-football API, team-page current+previous season, demo-on-mock-data.
4. ✅ **InPlay Global Website** — update block + Page Map: redesign on deck copy + brand colours, **imagery-last**, **outline font fixed**, **Partners/Team/Football-Challenge/Careers** pages, **CTA→form reason-routing to DLs**, publish-before-conference, T0 press-release merge, **mobile-optimisation rework**, **compliance-incident note** (guaranteed→up-to + pre-deploy copy review + counsel disclaimer review).
5. ✅ **Trading** — architecture note: **VPC up + FIX gateway rebuilt + T0 integration working**; **wallet/buying-power split RESOLVED** (T0 = trading wallet; InPlay = referral tracker + **synthetic broker** for buying power; cash wallet TBD; reload mechanism); **shorting mechanics**; synthetic broker + shorting BRs flagged for Friday.
6. ✅ **architecture/open-questions** — buying-power/referral-wallet row **RESOLVED**; added **synthetic broker design + BRs**, **shorting mechanics on-chain**, **cash-wallet host TBD**, and **market-making algorithm** (own session).
7. ✅ **components.md** — added the **pre-deploy copy-review + legal-disclaimer control** under the Cybersecurity & Data-Handling cross-cutting concern.

Not applied (no change needed / out of scope):
- **Multi-sport view-only** — May "not doing" decision stands; contested re-raise noted in triage, not written into component scope.
- **Affiliate revenue / $25M operator raise** — commercial lever; noted in this digest, no component doc.
- **Helmet realism, creative tooling, agentic outreach** — build assets / internal tooling; tracked here, not component docs.
