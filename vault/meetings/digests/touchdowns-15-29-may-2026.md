---
description: "Digest of the 15–29 May 2026 touchdown syncs — tZERO confirmed as ATS, the AI Research Agent, HubSpot as CRM, and the multi-sport expansion decision"
---

# Touchdown Sweep — 15–29 May 2026

> **Type:** Consolidated digest of touchdown (sync) meetings
> **Date compiled:** 2026-06-02
> **Sources:** [[15-05-2026-touchdown]], [[18-05-2026-touchdown]], [[19-05-2026-touchdown]], [[28-05-2026-touchdown]], [[29-05-2026-touchdown]]
> **Note:** `20-05-2026-touchdown.md` is empty (0 bytes) — no transcript captured; skipped.

Touchdowns are multi-topic status syncs. This digest captures the durable signal: **definitional changes** (things that change what a component *is*), **confirmations** of previously-pending items, and **genuinely new items** to triage. Pure build-status (deploys, Slack migration, banter) is omitted.

---

## Per-component synthesis

### Trading
- **tZERO confirmed as the ATS / settlement partner** — FINRA-approved ATS, first US ATS for tokenized assets, ~30k active accounts. Scale concerns **resolved**: handles ~1M trades/sec, 3M wallets/users, no queueing (kills the earlier multi-day account-creation worry). Weekly **Friday tZERO sync** established. _(15-05, 18-05, 28-05, 29-05)_
- Backend architecture: **FIX gateway built**; still need the messaging bus + websocket connections deployed, then whitelisted IP to tZERO for parallel testing. Pursuing **GCP-to-GCP direct connect** to avoid a ~3-month application wait. _(28-05)_
- **Trading-engine simulation/testing tool** (internal) — example traders ("Contrarian Carol", "Panic Pete"); measures order fulfilment, latency, bid-ask spread under bursts; stress-test ~100k users before tZERO integration. Intended to grow into an **admin/monitoring panel**. _(19-05)_
- Trade entry reachable **"two clicks away" from every page**. _(18-05)_

### Information Layer
- **Research Tab is taking shape** via an **AI Research Agent** with three modes: (1) manual chat, (2) scheduled reports (e.g. weekly game-day price report), (3) event/webhook-triggered proactive research (e.g. on injury news). Floated as **premium ~$99.99/mo** (vs $5–20k/mo for raw Sport Radar data). _(18-05)_ — **this gives definition to the previously-undefined Research Tab and overlaps Third Space's Research AI Chat.**
- **Build process:** read Sport Radar docs → map available data against sub-module docs + old app → compute the "delta" → add components via an include/exclude menu. Layout largely as-is. _(18-05, 19-05)_
- **Team page enrichment:** season stats (offense/defense/special teams), recent results, injury reports, key players w/ stats, AP news feed. Single-game/moments tab (key moments, scoring, game stats, ad-on-events). _(18-05)_
- **AI insight feature** — historical scoring probability ("72% of the time") to inform trades. _(18-05, 19-05)_
- **Multi-sport expansion:** Edwin wants **baseball + soccer added to API polls by July** — viewable (World Cup, baseball) at download but **not tradable**. Data, once on, stays on permanently. ⚠️ George's concern: showing untradeable sports may dilute the focused value prop / push users to betting apps — *undecided* (lead-magnet vs focus). _(28-05)_

### Customer Onboarding
- **Lead-form fields:** add **last name, phone number, and "university or company"** (open text, not dropdown). _(18-05)_
- **PWA fallback** for app delivery — rebuild onto a new **"BP VPC"** stack; React Native, possibly re-rendered as server-side NextJS; Persona/KYC wired in, identical branding — so onboarding/referral can run **without app-store approval**. Login + KYC + referral = the first-version priority. _(28-05; also folded into Referral)_
- **Face ID / biometric login** being researched (where to capture during onboarding). _(15-05)_
- KYC via **Persona** — contract in Persona's legal review. Apple developer contract pending signature; Google Play set up. _(18-05)_

### Education
- **AI-linked learning:** an agent surfaces text + TikTok-style videos *inside chat*, renders video inline, supports back-and-forth Q&A, scoped to InPlay's content. _(18-05)_
- Hassan's integration into the academic system "going well"; partner responsive. _(29-05)_

### Third Space
- Framed as **one of three core pillars** (trade / data / chat). _(28-05)_
- **Chat market sentiment** floated as a potential pricing/strategy indicator. _(28-05)_

### Referral
- Confirmed as a **sponsorable tab**; flagged a top priority alongside KYC/data feed — start running ASAP. _(18-05, 28-05)_ _(Substantive referral detail captured separately from the 27-05 referral-programme session.)_

### InPlay Global Website
- **Live site launched** (delayed from Saturday over domain-production risk); Edwin using it as an outreach asset. _(18-05)_
- Added **Investor page** + **Partner With Us** form + **light-mode toggle** (toggle incomplete site-wide). _(15-05)_
- **Team page:** expand beyond 2 execs (add Skye, Cody, Kevin…); everyone drafts short bios with a personality element; **go live with bios first, images later** (LinkedIn portraits as placeholders). _(29-05)_
- **Dual-audience sales tool:** B2B (advertisers/brands) + users, messaging split. Downloadable **thought-leadership white papers** (Jim Angel / Georgetown; possible 2nd professor). **tZERO / Sport Radar partnerships featured** for credibility. Post-launch **live metrics ticker** ("George traded $87k this week") to drive return visits. _(29-05)_

### Challenge Website
- Standalone **"coming soon" landing page** built — countdown (August placeholder), American-footballer hero, lead-capture form; move onto correct domains. _(15-05, 18-05)_

---

## Cross-cutting updates

### Advertising
- **Per-tab sponsors** — each bottom-nav tab gets a dedicated sponsor (leaderboard, referral, research, education — e.g. Coursera/Kaplan for education). _(18-05)_
- **Native-integration mandate (Edwin, emphatic):** ad/sponsor units must NOT be "squeezed-in tiles" or placeholders — they must be **ingrained into each tab's visual layout as a cornerstone**, tied to volatility/special moments (glow behind a team chart, animated turnover dot, NFL flyover banner, exploding Dorito bag). Noticeable but not distracting; must not read as "a betting app." _(19-05)_
- **Google Ad Manager confirmed rejected** — tested, does not support custom per-minute / blocked-out game-play serving. Testing two new platforms (one fully API-based for agentic feeding of ad units + rulesets + stats) → consistent with the **Kevel + Booster** direction. _(18-05, 19-05)_
- **Controlled demo asset** for advertiser pitches (screen-recorded now, clickable later; not distributed). **B2B hype video** (brand-adjacency angle, not fan/sports hype). _(19-05, 29-05)_
- Live deals in motion: **tZERO willing to commit ad money**; **Windrust Bank** meeting (shown generic top-US-brand mockups, custom mockup offered as a "hard-to-get" close). _(15-05, 29-05)_

### Push / CRM
- **HubSpot selected as the CRM** (final contract stages, ~3-month evaluation; likely a 1:1 HubSpot onboarding partner providing API endpoints + tag manager/pixels). Lead-form data also stored in an **Airtable mini-CRM** with a dashboard + emailed to info@inplayglobal.com. _(18-05)_ — **resolves the previously-"undefined" Push/CRM tooling question.**

### Analytics & Funnel Measurement
- **Product analytics** (heatmaps, "finger trails") to compare stated vs actual user behaviour and inform phasing. _(15-05)_
- **Advertiser-facing KPI dashboards** (latency, bid-ask spread, engagement minutes) to reduce sales friction. _(19-05)_
- Idea: publish a **viral industry-metrics report** ("taste sample" of sellable data) to attract advertisers (Brett's AdMob analogy). _(29-05)_

---

## New items — triaged (decisions made 2026-06-02)

| Item | Source | What it is | Decision |
|------|--------|-----------|----------|
| **AI Research Agent** (3 modes, premium ~$99.99/mo) | 18-05 | Manual chat + scheduled reports + event-triggered proactive research over Sport Radar data | ✅ **Part of the Research Tab** ([[information-layer]] sub-component). Documented; manual-chat mode = Third Space's Research AI Chat (reconcile ownership) |
| **Trading-engine simulation / admin panel** (internal) | 19-05 | Internal stress-test + monitoring tool; example-trader simulation; pre-tZERO load testing | ✅ **Internal tooling.** Added as a Trading sub-component, marked internal/not-user-facing |
| **Multi-sport expansion** (baseball, soccer by July, view-only) | 28-05 | Non-tradable sports data as funnel/lead-magnet | ❌ **NOT doing this.** Was an exploratory ask only — decided against. Stays out of scope |
| **tZERO white-label** (InPlay app as tZERO's primary app for all products) | 28-05 | Exploratory: license InPlay app to tZERO for equities/futures/options/tokenized | Exploratory business deal — note in vision/commercial, not a build component yet |
| **B2B hype video / white papers / live metrics ticker** | 29-05 | Marketing/credibility assets on the Global Website | Belong to **InPlay Global Website** scope |

---

## Doc updates applied (2026-06-02)

1. ✅ **Information Layer → Research Tab** — defined via the AI Research Agent (3 modes, ~$99.99/mo production). Updated sub-component doc, changelog, and parent entries.
2. ✅ **Trading** — added the internal Trading-Engine Simulation / Admin Panel sub-component + a tZERO/architecture note (tZERO confirmed ATS, FIX gateway, scale validated).
3. ✅ **Push/CRM** cross-cutting bullet — recorded **HubSpot + Airtable** (resolves "undefined").
4. ✅ **Customer Onboarding** — added the PWA-first delivery note; confirmed **Persona** as the identity-verification vendor (already documented); clarified lead-form fields live on the website, not app registration.

Not applied (no change needed / out of scope):
- **Multi-sport expansion** — decided against (see above).
- **Advertising** per-tab sponsors / native-integration mandate / GAM-rejected — already captured in the enriched cross-cutting Advertising bullet from the May ad-sessions commit.
