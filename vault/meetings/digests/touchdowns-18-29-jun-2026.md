# Touchdown Sweep — 18–29 June 2026

> **Type:** Consolidated digest of sync / strategy meetings
> **Date compiled:** 2026-06-30
> **Sources:** [[18-06-2026-Education-component]] _(filed as "Education" but is an advertising / GTM strategy call — education was tabled to the 22-06 session)_, [[24-06-2026-touchdown]], [[29-06-2026-touchdown]]

These three calls capture the durable signal: **definitional changes**, **confirmations** of pending items, and **new items** to triage. Pure build-status, banter, and scheduling logistics are omitted. The 26-06 Research Tab deep-dive is **not** in this sweep — it was a focused sub-component session, extracted directly to [[information-layer/sub-components/research-tab/research-tab]].

Two threads dominate. First, **advertising anxiety turns into a plan**: with programmatic ad revenue looking thin and slow (18-06), the team pivots commercially — keep the SSP programmatic build moving, repurpose Skye to **user acquisition / brand** rather than ad sales, and stand up an **automated outreach workforce** for direct-sales pipeline. Second, the **pre-launch app + referral funnel goes live-ready**: the prize model is **restructured around participation-gated payouts**, the **referral program launches through the challenge website with KYC**, the challenge website is review-ready (embedded hype video, how-it-works, IPO calculator), and the **legal/T&C** surface gets an AI-drafted first pass pending counsel review.

> **Parked (not extracted):** The 26-29 calls carried substantial **corp-dev / commercial** material — a **Teddy Sagi family-office NDA** (pay.com / Hard Rock Digital connections, could close in July), **Goldman Sachs** intros across DraftKings/FanDuel, and a **Kalshi** thread ($40B valuation; InPlay positioned as the **underlying "source data"** for sports perpetual futures). This is commercial / vision-adjacent, recorded here for traceability only. No component change.

---

## Per-component synthesis

### Advertising _(cross-cutting — the spine of the 18-06 call)_

The 18-06 call was booked as an Education session but became a long, candid advertising / go-to-market discussion (Edwin: _"am I totally f***** here with this plan?"_). The reassurance and the plan:

- **SSP-first stays; registration starts now (18-06).** Brett is standing up `novo@inplayglobal.com` and **begins registering** with AppLovin **MAX first, then AdMob**, then three more over ~3–4 days, loading a test app to start seeing ads quickly. Premium SSPs (eCPM ~$11–12) are courted later (3–4 months) — Brett has ex-colleagues now running sales there. Reinforces the **17-06 SSP-first stack** (see [[advertising/sub-components/programmatic-media-playbook/programmatic-media-playbook]]); the message is "plug in, optimise, don't wait." _(18-06)_
- **Inventory-layering model (18-06).** Every digital media owner layers inventory: **direct buy ~20–30%** (most valuable), **premium programmatic via agencies ~15–20%**, **house ads ~5%** (cross-promo, IPO drives), with the **remaining bulk filled programmatically via SSPs**. Brett's lived experience: ~**90% of media owners live on programmatic/SSP revenue** — it's the consistent base; direct is the cherry on top. Sport Radar built its own DSP for exactly this reason (Cody). _(18-06)_
- **The "minutes → impressions" problem (18-06, 24-06).** Brett does not trust the minute-to-impression conversion the model currently leans on (a 30-year industry problem — everyone overestimates). He is building a **forecast / calculator** that uses standard industry mechanisms + uplift factors (logged-in ~2–2.5×, age/geo/finance dimensions), to be reviewed with Edwin/Cody as "the degenerates." **Target: ready for the following week's touchdown.** Continues the 17-06 impression-model revision (~5 impressions/min). _(18-06, 24-06)_
- **Click-behaviour unknown (18-06).** Trading/betting apps legally carry no ads, so the audience is **not conditioned to click** — direct-response performance is genuinely unknown. Edwin's counter: locked-in users will click contextual offers (DoorDash when hungry, beer when thirsty); needs advertiser diversification + the right micro-moment, which takes time. Logged as an unknown to plan conservatively around. _(18-06)_
- **Data play (18-06).** Beyond serving, InPlay accumulates a rich audience/volatility dataset that can be **sold to targeters at a ~$2–5 markup**. A second revenue stream, production-stage.
- **AI brand-preview tool (29-06):** the tool (paste a URL/logo → AI previews the brand across in-app units) **went missing from the challenge-site advertising page**; Max to restore it — Cody wants it ready to demo for the Mastercard call. Continues the 15-06 tool. _(29-06)_

### Referral _(+ prize / competition mechanics — major, 24-06)_

The 24-06 call **restructured the prize model** to de-risk the up-to-$25M against actual participation, and **launched the referral program**:

- **Participation-gated payouts (24-06).** The prize pool stays "**up to $25M**" but is **gated on a participation line** (number of qualifying competitors). Concrete shape landed on: **dailies on Saturday + Sunday** (college + pro football days) **plus a weekly payout resetting Tuesday** = **3 payouts/week**, roughly **$25k/day (~$200k/month)** to start, distributed **wide and small** (George's network-effect argument: a uni student winning $50 tells everyone). First month's structure may run as **qualifiers** that feed the monthly pool. The framing: start smaller but make it look officially big, and you can show advertisers real traction. _(24-06)_
- **Qualification criteria — keep it to ~3 (24-06).** Candidates: **minutes on app**, **number of trades**, **education completion**. **Referrals are explicitly NOT a hard gate** (Troy: 50 referrals is too high a hurdle / too much referral anxiety) — instead referrals get their **own leaderboard with a separate prize** (e.g. top-3 referrers win ~$1k each), plus referral **credits** as the driver. George floated a **multiplier model** (base payout × completed steps) and **badging**. Troy's caution: too many criteria = churn for ADD-prone Gen-Z. _(24-06)_
- **Referral program LIVE via the challenge website + KYC (24-06).** The referral program now runs **through the trading-challenge website** with **full KYC**, and can launch **the week of June 30 / July 4**. The **600 trading-challenge signups** get emailed (B2C transactional, consent already given). This is the first real referral activation. _(24-06)_

### Customer Onboarding _(app-store + delivery, 24-06 / 26-06 / 29-06)_

- **App-store status (24-06).** **Apple is moving again** — the $99/yr developer fee paid, the app processing; the team "figured out where everything was sitting." **Android Play Store verification is stuck** on **website + phone-number verification** (needs **owner**, not admin, access; the Novo team are admins). Brett offered Play Store contacts to unstick it. Continues the standing "**Apple developer account = the launch blocker**" (17-06). _(24-06)_
- **TestFlight up (26-06).** A TestFlight build is running; distribution needs each tester's **Apple ID** (up to **100 users**), not device IMEIs. The **pre-launch build strips functionality** (first-time user, referrals, IPO browse) and **removes the demo ad units** — demo ads stay on a separate branch for sales demos, not the production app. Builds (PWA vs TestFlight) are being **synced** so education etc. appears consistently. _(26-06, 29-06)_
- **KYC opt-in (29-06).** On the challenge-site signup, going through KYC should explicitly read as **opting in** to communications; copy to be adjusted. _(29-06)_

### Challenge Website

- **Legal / T&C first pass (29-06).** The site's **terms, privacy, and competition-rules pages are now AI-drafted and populated** (previously placeholders). They read well and generic, but **must be reviewed by legal counsel** (Matt Vogler / Marlin) before publish; Max to export them to a Word doc for redline. **Decision: disable the legal footer/links for go-live** until reviewed (no prize-pool / regulatory claims live yet). Continues the standing compliance rule: **"up to $25M", never "guaranteed"**, and the pre-deploy content-review control. _(29-06)_
- **Review-ready build (29-06).** Homepage carries the **hype video embedded in a phone frame** (well received); the rest of the homepage moved to a **"How It Works"** page (with a how-to-trade video). The **IPO pricing section is now an interactive calculator** (on-field expected wins vs ties vs trading-volume %), replacing a static formula. The **OG / social-share card image is the ugly default** and needs a designed asset (when a user copies/shares the link it looks broken). _(29-06)_
- **Newsletter vs link debate (29-06).** Long discussion on the first outreach to the 500–600 signups. Edwin: the goal is **action** (download → KYC → refer), not a read; he'd rather send the **trading-challenge homepage content** (hype video, $25M up top, referral CTA) than a traditional newsletter. Troy/Skye: keep a **light newsletter** because the audience expects substance after waiting since May. Landed: **lead with the homepage/hype content optimised for action; defer the fuller newsletter / community channel** (Brett's "Rebel Technologist" community framing) to later. Money (**$25M**) goes at the very top. _(29-06)_

### Information Layer _(minor app confirmations, 29-06)_

Edwin's app walkthrough surfaced confirmations/bugs (mostly delivery, noted for traceability): **buy/sell markers now render on the chart** (blue dot + "B" on buy, red dot + "S" on sell); the **community/chat view defaults to the most recent chat** (by design — don't scroll stale chats); the **open/splash screen should be the arrow only** (remove the "arrow over a mountain" — no "climbing-a-mountain contest" read). Price **integer/rounding glitches** are mock-data artefacts (no live T0 data yet); a **Visa header label is cut off / mis-scaled** (Max to fix). No doc rewrites — status/bugs. _(29-06)_

### Trading _(T0 buying-power mechanism, 24-06 + 26-06)_

- **Daily buying-power file → "elegant" API (24-06, 26-06).** To support moving funds from the **referral wallet into the trading wallet**, InPlay must give T0 each account's **buying power** — initially as a **start-of-day file** (no intraday wallet rebalancing, by decision, to avoid complexity; T0 calculates buying power intraday). George proposed a more **elegant mechanism**: an **API call** that increases the user's T0 wallet buying power while InPlay **consumes the referral** on its side (so it can't be reused) — instead of an FTP file load. Troy endorsed it; George is **drafting it to the T0 team**. Reinforces the standing split: **buying power = "trading power"** (covers selling/shorting, not just buying); the **ledger = clearing/settlement custodial record**; the simulator uses a **synthetic wallet**, production a **real digital wallet** funded from broker/stablecoin. _(24-06, 26-06)_
- **Market-maker session reconfirmed (24-06, 26-06, 29-06).** Edwin will **co-build the market-making algo with George** — he has the parameters (a prior algo from the "Xperry" platform; the hard part was API-connecting feeds), wants it integrated with **T0 feeds**. A separate session is needed (it's "another research agent / another call"). The MM session should also **capture data for prod market makers** to model on, and feeds **academic white papers** (Jim Angel; Josh's, scope TBD) on how the market behaves when outcomes are a foregone conclusion. Continues the existing market-maker flags. _(24-06, 26-06, 29-06)_

---

## Cross-cutting updates

### User acquisition / brand _(new emphasis, 18-06)_

The most consequential people-decision: **Skye should be pointed at user acquisition + brand-building, not media sales.** Brett's argument — Skye's experience (LIV Golf, BMW) is wasted selling ad inventory; brand + user acquisition is the priority now, and the harder challenge is doing it **with little budget** ("zero to hero, not field of dreams"). Edwin: focus is **getting users**; put someone else on direct brand sales. **Don't hire heavyweight media salespeople (~$350–380k) until ~500k users** — they won't engage a zero-audience product, and they'll come knocking once the audience exists. _(18-06)_

### Push / CRM & outreach automation

- **Automated outreach workforce (18-06).** Novo's agentic workforce (the same kind building the app) will run **24/7 outreach** — turning **InPlay's LinkedIn accounts + purchased domains** into lead-generation systems for the direct-advertising pipeline, plus amplifying Skye's content. Needs **domains** and **LinkedIn access**. Offered to InPlay **for free** (Novo absorbs LLM cost). _(18-06)_
- **B2B vs B2C email infrastructure (24-06).** **B2C** transactional emails to the 600 existing signups can go now (consent given). **B2B cold outreach** needs warm-up infra: **3 real-named mailboxes per domain** (~£8–9/license), **domain redirects** (e.g. `getinplaytradingchallenge.com` → challenge page), and a 2–3 week warm-up before sending, plus LinkedIn. George researching B2C deliverability for the already-consented list. _(24-06)_
- **Newsletter → community channel (29-06).** See Challenge Website — the newsletter is reframed as a future **owned community channel** (give-back content, tips, interviews), distinct from the first action-driving send. _(29-06)_
- **T0 partnership press release (29-06).** T0 PR scheduled **8:30 ET the next morning**; link to be embedded on the website + the first distribution. _(29-06)_

### Cybersecurity & compliance

- **Legal/T&C control (29-06)** reinforces the **pre-deploy content-review** concern: AI can draft the legal scaffolding, but **external counsel (Marlin / Matt Vogler) must clear it before publish**, and uncleared legal links are **disabled at go-live**. Standing rule holds: **"up to $25M", never "guaranteed"**. _(29-06)_

---

## New items — triaged (decisions / dispositions 2026-06-30)

| Item | Source | What it is | Decision |
|------|--------|-----------|----------|
| **Prize model → participation-gated payouts** | 24-06 | Up-to-$25M gated on a participation line; Sat/Sun dailies + Tue weekly (~$25k/day); ~3 qualification criteria (minutes, trades, education) — **referrals NOT a hard gate**; referral leaderboard with separate prize; multiplier/badging floated | ✅ **Captured in [[referral/referral]]** (changelog) + 🚩 **remaining design flagged** in [[architecture/open-questions]] (final criteria, payout schedule, multiplier mechanics) |
| **Referral program LIVE via challenge website + KYC** | 24-06 | Referral now runs through the challenge website with full KYC; launches ~July 4 week; 600 signups emailed | ✅ **Noted in [[referral/referral]] + [[challenge-website/challenge-website]] + [[customer-onboarding/customer-onboarding]]** |
| **Legal / T&C AI-drafted, counsel review, footer disabled at go-live** | 29-06 | T&C / privacy / competition-rules populated by AI; need Marlin/Vogler review; KYC opt-in copy | ✅ **Noted in [[challenge-website/challenge-website]]**; reinforces compliance concern in [[components/components]] |
| **Challenge-site build: hype video in phone, How-It-Works page, IPO calculator, OG image** | 29-06 | Review-ready homepage; interactive IPO pricing calculator; designed OG card still needed | ✅ **Noted in [[challenge-website/challenge-website]]** |
| **T0 buying-power: daily file → George's elegant API** | 24-06, 26-06 | Start-of-day buying-power file for referral→trading moves (no intraday rebalance); George drafting an API mechanism (increase wallet + consume referral) vs FTP | ✅ **Noted in [[trading/trading]]**; mechanism row added to [[architecture/open-questions]] |
| **App-store status (Apple moving, Android stuck)** | 24-06 | $99 Apple fee paid/processing; Android Play verification stuck on website+phone (needs owner access) | ✅ **Noted in [[customer-onboarding/customer-onboarding]]**; continues the "Apple = launch blocker" flag |
| **Skye → user acquisition / brand (not ad sales)** | 18-06 | Reposition Skye to brand + UA; don't hire heavyweight media sales until ~500k users | ✅ **Advertising / UA note in [[components/components]]** |
| **Automated outreach workforce + B2B/B2C email infra** | 18-06, 24-06 | Agentic 24/7 outreach via LinkedIn + domains; B2B warm-up (3 mailboxes/domain, redirects); B2C to consented 600 | ✅ **Push/CRM note in [[components/components]]** |
| **SSP registration starts + inventory-layering model + data play** | 18-06 | MAX→AdMob registration underway; 20-30% direct / 15-20% premium / ~5% house / bulk SSP; data resale at $2-5 markup | ✅ **Advertising note in [[components/components]]**; reinforces the [[advertising/sub-components/programmatic-media-playbook/programmatic-media-playbook|playbook]] |
| **Impression-forecast calculator** | 18-06, 24-06 | Brett building a minutes→impressions forecast on industry mechanics; due next touchdown | ℹ️ **Status** — feeds the impression model + Advertiser-KPI open question |
| **AI brand-preview tool missing from ad page** | 29-06 | Tool dropped off the challenge-site advertising page; Max to restore for Mastercard demo | ✅ **Noted in [[challenge-website/challenge-website]]** |
| **Newsletter vs action-first send** | 29-06 | First outreach optimised for download/KYC/referral; fuller newsletter/community deferred | ✅ **Push/CRM note in [[components/components]]** + challenge-website |
| **Market-maker session reconfirmed** | 24-06, 26-06, 29-06 | Edwin co-builds MM algo with George; T0-integrated; capture data for prod MMs + white papers | 🚩 **Reinforces existing flag** in [[architecture/open-questions]] |
| **App bugs / design confirmations** | 29-06 | Buy/sell chart markers, chat-defaults-to-latest, splash = arrow only, price rounding (mock data), Visa label cutoff | ℹ️ **Status / delivery** — no doc change |
| **Corp-dev: Teddy Sagi NDA, Goldman, Kalshi $40B / perpetuals** | 26-06, 29-06 | Family-office NDA (could close July); Goldman intros; InPlay as "source data" for sports perpetual futures | ⏸️ **Parked** — commercial / vision-adjacent, no component change |
| **Templated deck system (Max)** | 29-06 | One master-branded deck so per-market one-pagers stay consistent | ℹ️ **Status** — internal tooling |

---

## Doc updates applied (2026-06-30)

1. ✅ **components.md** — Advertising cross-cutting: SSP registration underway + inventory-layering model + data play + Skye→UA + don't-hire-sales-until-500k; Push/CRM: outreach workforce + B2B/B2C email infra + newsletter→community + T0 PR; compliance: legal/T&C counsel-review control.
2. ✅ **referral/referral.md** — changelog row: participation-gated prize model (Sat/Sun dailies + Tue weekly; ~3 criteria; referrals not a hard gate; referral leaderboard + separate prize; multiplier/badging); referral program LIVE via challenge website + KYC.
3. ✅ **challenge-website/challenge-website.md** — update block: legal/T&C AI-drafted + counsel review + footer disabled at go-live + KYC opt-in; hype video in phone; How-It-Works page; IPO pricing calculator; OG image needed; AI brand-preview tool restore; referral program live; newsletter-vs-link.
4. ✅ **customer-onboarding/customer-onboarding.md** — update block: app-store status (Apple moving / Android stuck), TestFlight distribution (Apple IDs, ≤100), pre-launch build strips functionality + demo ads, web KYC powers referral, KYC opt-in copy.
5. ✅ **trading/trading.md** — update block: buying-power daily file → George's elegant API (vs FTP), no intraday rebalance, buying-power = trading-power, ledger = settlement; market-maker session reconfirmed + prod-MM data capture + white papers.
6. ✅ **architecture/open-questions.md** — rows added: prize/competition mechanics (final criteria + payout schedule + multiplier); referral-funding-to-T0 mechanism (elegant API vs FTP).

Not applied (parked / status only):
- **Corp-dev thread** (Teddy Sagi NDA, Goldman, Kalshi perpetuals) — commercial / vision-adjacent, triage only.
- **App bugs + design confirmations, templated deck, impression-forecast calculator** — status / delivery, no doc change.
