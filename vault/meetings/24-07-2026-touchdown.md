---
date: 2026-07-24
type: standup
scope:
  - "[[frontend-deployment]]"
  - "[[integrations]]"
  - "[[advertising/sub-components/programmatic-media-playbook/programmatic-media-playbook]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[withdrawal-flow/withdrawal-flow]]"
  - "[[trading/trading]]"
  - "[[market-maker/market-maker]]"
  - "[[information-layer/sub-components/team-page/team-page]]"
  - "[[information-layer/sub-components/single-game-page/single-game-page]]"
  - "[[information-layer/sub-components/research-tab/research-tab]]"
status: extracted
extracted-to:
  - "[[frontend-deployment]]"
  - "[[integrations]]"
  - "[[advertising/sub-components/programmatic-media-playbook/programmatic-media-playbook]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[withdrawal-flow/withdrawal-flow]]"
  - "[[trading/trading]]"
  - "[[information-layer/sub-components/team-page/team-page]]"
  - "[[information-layer/sub-components/single-game-page/single-game-page]]"
---

## Post-Call Analysis

~51-minute Friday touchdown, < 1 month to launch. Present: Edwin, Cody, Troy (Inplay Global), Kevin, plus Brett, George, Max, Hasan (Novo). Very heavy banter (a long opening on avatars, market-maker war stories, Chicago anecdotes). Substantive content clustered around: the ad-server/SSP go-live (AdMob verification finally kicked off once the App Store ID landed 23-07), a tag manager + MMP (AppsFlyer vs Kochava) decision, release governance / OTA caps, the gamecast media-vs-betting feed speed decision and the Sport Radar probabilities-API problems, the trading-infra map + simulation testing route, a market-maker monitoring dashboard, payouts/tax-forms as the pre-launch blind spot, a KYC-less app variant for the academic competition, adoption numbers, a guest-analyst "analyst prices" swipeable page, and (reserved) subscription/research pricing. Market-maker mechanics were not re-discussed, see [[market-maker/market-maker]].

| Finding | Destination | Action |
|---------|-------------|--------|
| **Ad server live-path unblocked:** App Store ID landed **23-07**; Brett + Troy ran AdMob sign-ins/auth that night. AdMob verification **~24–48h**, then **at least one SSP serving**. Repeat once **Android** store goes live (grab ID/URL). All other SSPs need app-store IDs/URLs, different timelines. Goal: serve from an SSP ASAP to start **first-party data sets** flowing. | [[advertising/sub-components/programmatic-media-playbook/programmatic-media-playbook]] | 24-07 update block |
| **Google Tag Manager** as the analytics/attribution **container** (Hasan): install once (free), then drop any tags (GA, HubSpot, MMP, Facebook, cookies) with no further app change; just publish. Cody wants it live to tag content across influencers/other ventures. | [[advertising/sub-components/programmatic-media-playbook/programmatic-media-playbook]] | 24-07 update block |
| **MMP choice open: AppsFlyer vs Kochava.** Agency **Plexus** already uses **Kochava**; Cody floated standardising on it for simplicity, pending Plexus's proposal + Brett's review. No decision. | [[advertising/sub-components/programmatic-media-playbook/programmatic-media-playbook]] | 24-07 update block |
| **Release governance / OTA caps (Brett):** near-launch change = risk; Novo will push back + **backlog/schedule** requests. App-store changes go via **full push** (forced by some code changes) or **OTA** (stores **cap** how much you can push). Releases will be **staged** into caps. Two reasons for apparent stalls: **risk** + **app-store compliance**. Sits atop existing CI/CD. | [[frontend-deployment]] | New "Release Governance & OTA Caps" section |
| **Gamecast feed = SR media feeds; betting feed inaccessible.** Custom Gamecast runs on licensed **media data feeds**; the faster **betting feed** (powers the "ugly" licensed match tracker) is **only sold to licensed sports books**, so InPlay can't access it. Decision: use **fastest available feed**, keep TV-competitive; event→delivery **delta uncontrollable**. Probabilities are the reference signal (ideally off the betting feed; interim = media probabilities API). | [[integrations]] + [[information-layer/sub-components/single-game-page/single-game-page]] | New SR section in integrations; light note on single-game-page |
| **Sport Radar probabilities-API problems:** not in **production** env; only **probabilities v1** with ~**1,000/month** quota. Likely need **Global American Football Probabilities v2** (bulk endpoint: one batched call ~every 200 ms vs ~170 calls; ~2.5M→1M/month). Cody: SR now **one master API key** forking to all products (versioning/call-counts "mean nothing", effectively unlimited), but some products **not allocated** to InPlay's account → not-authenticated. George → SR support email; Cody aligns Scott + David. | [[integrations]] | New SR section |
| **Sport Radar contract = 1 year;** natural (small) renewal rise as sports added (~6–10 more); SR **never exclusive** (~900 sports books, "Switzerland of everything"). Adding sports + **betting feeds** = leverage for longer deal. Cody lobbying SR next week that InPlay is more regulated than a betting/prediction market to get betting feeds in parallel. | [[integrations]] | New SR section |
| **Trading infra mapped 23-07;** launch-readiness **non-negotiable**. Remaining items small (**cancel feature**, **cancel-and-request**), tightly integrated with MM; some waited on T0. **Testing via historical-game simulation** (Chiefs vs Ravens), run multiple times/day, on a test app version. | [[trading/trading]] | 24-07 update block |
| **Market-maker monitoring dashboard (Edwin):** read-only view of MM inventory / shares-per-market / bills for an InPlay operator, near-production. George: MM **is just another user** → same inventory APIs; phased (backend-working → data representation → later variable control). | [[trading/trading]] (MM specifics → [[market-maker/market-maker]]) | Noted in trading 24-07 update; MM detail flagged in return |
| **Payouts + tax forms = pre-launch blind spot.** Fallback: if payment-provider deal not signed/integrated by launch, **show qualified winners + amounts, delay actual payout** a couple weeks. Interim manual (**Zelle/wire**) acceptable; Edwin: payment processor "a bugaboo", method doesn't matter for interim. Notifications also a last structural add. | [[withdrawal-flow/withdrawal-flow]] | "What we know" update |
| **KYC-less app variant** being scoped (lift + whether it needs a **fresh Apple review**). De-prioritised: needed only by **first/second week of Sept** for the **first academic presentation** (~a month out); a different login route for the academic portion. Launch priority = trading live/tested for **the 22nd** (Aug 22 sim launch). | [[customer-onboarding/customer-onboarding]] | 24-07 update block |
| **Adoption snapshot:** Wed **22-07 = 37 first-time downloads** (23–24-07 not yet reported); ~130 logged-in running total. **83 approved KYCs** (was 64); ~19 of 37 KYC'd but some downloads are already-KYC'd (team/family), so genuinely-new is lower. **Newsletter out 24-07**; Hasan exporting updated registrations CSV (~25 more via email). | [[customer-onboarding/customer-onboarding]] | 24-07 update block |
| **"Analyst Prices" swipeable page (Edwin):** new team-surface swipe showing **guest analysts' prices** (4–5 analysts who publish in exchange for in-app distribution). First target **Preferred Walk-Ons** (college creators, ~200k, ex-PFF) for NCAA; NFL analyst still being sourced. Build questions: where analysts upload weekly, how InPlay consumes/serves/labels. Sample due Monday. | [[information-layer/sub-components/team-page/team-page]] | 24-07 update section |
| **T0 call cadence changed:** T0 tech calls no longer Fridays, now **Tue/Thu**; Novo touchdowns **Mon/Wed/Fri**. | Meeting doc only | Status |
| **Omnicom / John (US ad agency):** two-pager/info still to be sent to John; he never reached out. Repeated ask, mild frustration. | Meeting doc only | Status |
| **NCAA IPO prices:** Edwin cut the AI-generated valuation doc from **650 pages → ~30**; Cody supplied NCAA team totals; Edwin to push **NCAA football IPO prices** into the app **24-07**. (Freeze-paragraph trick to stop the model overwriting kept content.) | Meeting doc only | Status; overlaps IPO/valuation + MM inputs |
| **Roadmap / vault dashboard (Cody ask → Brett):** Cody wants a **visual roadmap/timeline + bandwidth view** instead of his notebook. Brett to build a **release/cadence dashboard in the vault**, fed from the meeting-digest + morning-standup task breakdown, so Cody can see capacity and slot/hold/push work (product-ownership tooling). | Meeting doc only (process) | Flagged: vault/process, not a product component |

### Reserved-topic capture (subscription pricing / research module, orchestrator owns)

- **Subscription packages + pricing** are being sent from Cody to George (tied to the analyst-prices/content offering). **Middle package** floated at **$39.99 vs $34.99** ("maybe $34.99 hits harder"); Cody stresses it stays a **work in progress even post-launch** (be agile).
- **Subscription math (from 23-07):** target **500k total users**, ~**half degens**; that netted ~**$2M/month in subscription revenue**. From a ~200k-follower creator base Edwin expects ~**100k signups** ("degens are the people who pay").
- **College content format for the research/analyst product:** short **video clips** of the **top 25**; **next ~110 teams** get a **~2–3-second blurb** on the week's pricing + matchup. **Video preferred**; if video can't live in-app, use it across socials/content instead. Preferred Walk-Ons will make a separate show or give InPlay a **30–45 min weekly slot** to chop into 30s–1min clips.
- **Timing:** research/subscriptions **not for launch**; Cody leaned October, but **Edwin wants the research piece inserted in the next 1–2 weeks** so influencers can start talking about it. (Cross-refs [[information-layer/sub-components/research-tab/research-tab]], NOT edited here.)

---

**Source transcript:** `Inplay - App - Touchdown – 2026_07_24 14_34 BST – Notes by Gemini.md` (raw, in `/home/brett/shared/inplay/meeting-notes/`). This is a digest; the raw transcript is not reproduced here.
