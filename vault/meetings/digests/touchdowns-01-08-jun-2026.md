# Touchdown Sweep — 1–8 June 2026

> **Type:** Consolidated digest of touchdown (sync) meetings
> **Date compiled:** 2026-06-09
> **Sources:** [[01-06-2026-touchdown]], [[03-06-2026-touchdown]], [[05-06-2026-touchdown]], [[08-06-2026-touchdown]]

Touchdowns are multi-topic status syncs. This digest captures the durable signal: **definitional changes** (things that change what a component *is*), **confirmations** of previously-pending items, and **genuinely new items** to triage. Pure build-status (deploys, banter, payment logistics) is omitted.

This is the build-sprint fortnight ahead of a **sales conference (week of 9 June)** — much of the signal is the prototype coming to life (referral system, live Sport Radar data, app ad placements) plus a hard push to publish the Global Website before the conference.

---

## Per-component synthesis

### Customer Onboarding
- **Persona contract SIGNED** (was "in legal review" in the May sweep). Implementation kicks off on intro from their sales to a tech/implementation engineer. Still **waiting on API keys** to wire into the onboarding flow. _(03-06, 05-06, 08-06)_
- **Onboarding flow built into the app** (Hassan) — create-account → optional referral-code entry → Persona ID check (placeholder until keys land) → approved → QR/referral screen → into app. Currently placeholder screens; "A→B→C straightforward". _(08-06)_
- **First-version app scope locked:** referrals + wallet + signup + **KYC (required, not optional)** + some live data for functionality. **Not** full in-app Apple trading. _(05-06, 08-06)_
- **Persona KYC speed validated:** government-ID + face-scan is ~99.5% AI-automated; approval in seconds. Cody: _"the longest time… is walking from my couch to the kitchen to get my ID."_ _(08-06)_
- **App-store accounts:** **Google Play set up**; team being added. **Apple developer account reset to the beginning** — Apple must call/email **Edwin** to approve **Troy as company signatory** to sign the developer agreement (last time ~48–72h). Google verification needs identity + org-website + phone (doing it via `appdevelopment@inplayglobal.com`). _(03-06, 05-06, 08-06)_

### Referral
- **Referral system built and demoed** (Hassan). Confirms the documented mechanics: **lifetime-unique pre-generated codes** (tested ~1B users, no collision), QR-code page, referrer↔referee tracking table, **crediting gated on KYC approval** (currently a simulated approve button), **boost multipliers preset** for specific dates/weekends. _(05-06, 08-06)_
- **Cody's required share flow (refines Share Surfaces):** the referral/QR screen must be the **very next screen after KYC**; add **one-click social share** that prepopulates the *screen image* (not just text) into Instagram/X/text, ideally **per-platform styled**; after a referred user completes KYC, immediately surface **their own** unique code (feedback loop); also expose the code on the **profile page**. _(05-06)_

### Information Layer
- **Sport Radar data live in the prototype** — real SR data streaming into the PWA; where data is placeholder it's explicitly labelled "demo data". _(05-06, 08-06)_
- **Replay simulation model:** SR feed is **fixed to a past point in time** (week 10 of 2024 in the 05-06 demo; 2025 season in 08-06) so completed games replay with **real** standings, results, injury reports, key-player stats, and **all moments per game** linked to a popup. Pricing/market data not yet linked. Live moments will run off the **SR provider simulation endpoint**. _(05-06, 08-06)_
- **Moments-per-game validated at ~18** (granularity can go up to ~170). Confirms Cody/Edwin's "15–20 highlight moments per game" premise. George: surfacing all 170 would dilute UX → **group moments by quarter** (Cody's playbyplay-widget pattern). _(08-06)_
- **Sport Radar entity-ID model:** one SR ID joins **play-by-play, AP editorial newswire, headshots, win-probability** across products. Pull **AP injury-article context** onto player cards (injuries are a major trade driver). Win-probability lives under the **global American-football API**, not the NFL API (IDs interoperate) — resolves George's 403 error. Headshots not yet licensed. _(08-06)_
- **Team page enriched:** all season stats, conferences, full results, week-level injury reports, key players. Decision: show **current + previous season only** (not 2024 as well). _(08-06)_

### InPlay Global Website
- **Full redesign (Max + Skye, ~5h joint session):** strong branding/brand colours; uses the **exact copy from Skye's deck** (no edits); **imagery stripped and added last** — establish text/copy on screen first, then build imagery around it (only the home hero had images at 05-06, rest to follow). _(03-06, 05-06)_
- **Home hero:** two players facing off (AI-generated); a **moments-of-the-game** section (turnover, QB limps off then returns → price spike) straight from Edwin's deck. _(05-06)_
- **Pages:** Home, **Partners** ("partner with InPlay"), Team (headshots), Football Challenge. Feedback applied over the weekend: **outline/"future" font made bolder/thicker/brighter** (was hard to read); team headshots cropped to **consistent framing/distance**; **remove the "Tony"/Anthony Verbillis quote**. _(05-06, 08-06)_
- **Lead routing:** every page has a CTA → **form with a reason selector** (just-a-user / advertising / media) → routed to the **appropriate email distribution list**; homepage has two CTAs (top + bottom). **Troy owns DL assignment** per category; Hassan wires the routing. _(05-06, 08-06)_
- **Career tab** needed at top of nav (Troy) for job postings — first posting is **VP of Technology**. _(08-06)_
- **Publish target:** live **before the Tuesday sales conference** (Cody pressing — a dot-card swipe must land on the real site, not a blank page). Reviewed over the weekend and approved to publish, with further refinement to continue in the background. _(05-06, 08-06)_
- **Press release:** Skye drafted a **T0 press release**; tZERO is also drafting one → **merge and time for Tuesday**. _(05-06)_

### Trading
- *(see Architecture note below — VPC + T0 integration are the durable signal this sweep)*

---

## Cross-cutting updates

### Advertising
- **In-app ad placements designed (Max)** and validated as **"elegant, not in-your-face"** (Troy): per-brand app heroes (Coca-Cola home, Gatorade discovery, Pepsi/Visa/Bud Light/FedEx/Amex pages); a redesigned MX/Amex banner **persistent across all game screens**. _(05-06, 08-06)_
- **Header lock vs scroll — decision:** leave the top sponsor banner **scrolling** for now (don't lock), keeping the design as **options to feel out advertisers**; big hero headers should *not* lock (too much screen). Priority order made explicit: **trader UX > advertiser > everything else**. Rationale: sponsorships are sold on **exposure-minutes** ("lock-and-load"), so the model must back the brand to hit promised minutes — but not at the cost of the trader experience. _(01-06, 05-06)_
- **"Territories" / page-ownership naming** floated — gamecast, information centre, referral bank — each a sellable "presented by" surface (Amex "owns the space" reference). _(01-06)_
- **Booster = too early.** It's an **order-management / ad-ops** system for scale; managing ~10 advertisers can be done **manually**. Good visibility into how scale-stage data/audit/fill works, but defer. **Kevel is still required** even for sponsorship/impression serving — it places the sponsorship, rotates campaigns, and produces audits/metrics/minutes. Kevel call the following week. _(03-06)_
- **"Don't build until we have advertisers"** (Edwin) — first advertiser is likely Edwin himself; no ad server needed to place a static sponsor. _(03-06)_
- **Helmet realism (build asset):** replace flat SVG helmets with **AI-generated realistic helmets** for all **163 teams** (32 NFL + ~131 NCAA) using **exact team hex codes** (Kevin supplying; NFL done, NCAA in progress) + the "halo/gradient" effect. Pre-launch must-do; not a doc change. _(01-06, 03-06)_

### Push / CRM
- No new tooling decisions this sweep (HubSpot + Airtable stand from the May sweep). Website lead-form routing to per-category DLs (above) is the operational join into CRM. _(05-06, 08-06)_

### Analytics & Funnel Measurement
- Website CTA→form→DL routing is the first concrete **top-of-funnel capture** join (reason-segmented). Feeds the still-undefined Analytics & Funnel Measurement doc. _(05-06, 08-06)_

### Internal Tooling (new this sweep)
- **CI-aware creative tooling + image repository.** Edwin spent ~36h hand-building a sales deck; agreed it should never fall on him. Brett/Max to build a **system prompt / skill** that bakes in CI + knowledge base for decks/creative, plus a **shared repository of approved images** (feed an example image → AI produces on-brand lookalikes) + a ~1h best-practice training session. _(08-06)_
- **Agentic outreach at scale.** Brett to run agentic outreach alongside Edwin's manual brand outreach (liquor/wine brands) — package messaging + imagery + formatted email/deck per prospect, with Edwin tagged in to observe. _(08-06)_

---

## New items — triaged (decisions made 2026-06-09)

| Item | Source | What it is | Decision |
|------|--------|-----------|----------|
| **Affiliate revenue stream (sportsbooks)** | 05-06 | FanDuel-style affiliate / rev-share — when a user leaves to place a bet then returns, InPlay still monetises the minutes (Edwin's "Schwab account" analogy). Conference targeting **operators**; "opening the floodgates to fill **$25M**" (excluding some segments) | ✅ **New monetisation lever — noted in Advertising/commercial.** Not a build component. Underpins the multi-sport argument below |
| **Multi-sport view-only (baseball/soccer/etc.)** | 05-06 | Re-raised: Cody can trial-activate SR real-time in one email. Show live data from other sports (via a "more" button) to prove live speed + stickiness | ⏸️ **May decision ("not doing this") stands; re-raised and now contested.** Edwin/Cody: monetise the minutes + affiliate rev-share → revisit as **v2.0 post-launch**. George: dilutes focus / drives users to betting apps. **Verbally tell prospects "we're adding other sports"; no build.** Updates the existing ⚠️ note rather than reopening scope |
| **Market-making algorithm** | 08-06 | Edwin wants to **co-build a market-making algo over ~2 months** (has one built for the "Xperry" platform; polls/params differ). "Could put it in any market and make money." | 🚩 **Flagged for its own session.** Pricing/market-engine territory — outside the 12-component map; too undefined for a component doc. Logged in [[architecture/open-questions]] |
| **T0 homework: buying-power / referral-wallet design + responsibility split** | 05-06 | Define how **buying power and the referral wallet** operate and look/feel, and **which parts NOVO builds vs T0** — homework before the next T0 meeting | 🚩 **Open design question → [[architecture/open-questions]].** Refines the existing "what does tZERO manage" blocking question |
| **CI-aware creative tooling + image repository / agentic outreach** | 08-06 | Internal deck/creative skill + approved-image repo + agentic outreach at scale | ✅ **Internal tooling — noted in cross-cutting.** Brett + Max to build; ~1h team training. Not a product component |
| **Helmet realism (163 teams)** | 01-06, 03-06 | AI-generated realistic helmets w/ exact hex codes, pre-launch | ✅ **Build asset / task.** Kevin supplying hex codes. No doc change |

---

## Doc updates applied (2026-06-09)

1. ✅ **Customer Onboarding** — extended the delivery note: **Persona contract signed** (awaiting API keys), onboarding flow built into the app (placeholder KYC), **KYC required in the first iteration**, Google Play set up + Apple dev account reset (Edwin/Troy signatory step).
2. ✅ **Referral** — changelog entry: referral system **built & demoed** (lifetime-unique codes, QR, KYC-gated crediting, preset boost windows); added Cody's **one-click image-prepopulated social share** + **profile-page surface** + **referral screen as the immediate post-KYC step** to Share Surfaces / Code Lifecycle.
3. ✅ **Information Layer** — touchdown-sweep note: **SR data live in prototype**, **replay-simulation model** (fixed point-in-time, real stats/results/injuries, moments→popup), **~18 moments/game validated** (group-by-quarter UX), **SR entity-ID join model** (play-by-play / AP / headshots / win-prob), AP injury context on player cards, win-prob under the global American-football API, team-page = current+previous season only, demo-on-mock-data decision.
4. ✅ **InPlay Global Website** — touchdown-sweep note + action-list updates: redesign on exact deck copy + brand colours, **imagery-last** approach, **outline font fixed**, **Partners/Team/Football-Challenge** pages, **CTA→form reason-routing to DLs** (Troy owns), **Career tab** (VP of Technology), publish-before-Tuesday, **T0 press-release merge**.
5. ✅ **Trading** — extended the architecture note: **VPC stood up** (locked down, secure, connected to T0), **FIX gateway rebuilt** for high concurrency, **load testing (Hassan) fast**, T0 integration working with backend dashboards + scale-test harness ready.
6. ✅ **architecture/open-questions** — added two rows: **buying-power / referral-wallet design + NOVO-vs-T0 responsibility split**, and **market-making algorithm** (own session).

Not applied (no change needed / out of scope):
- **Multi-sport view-only** — May "not doing" decision stands; contested re-raise noted in triage above, not written into component scope.
- **Affiliate revenue / $25M operator raise** — commercial lever; noted in this digest, no component doc.
- **Helmet realism, creative tooling, agentic outreach** — build assets / internal tooling; tracked here, not component docs.
