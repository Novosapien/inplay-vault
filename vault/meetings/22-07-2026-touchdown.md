---
date: 2026-07-22
type: standup
scope:
  - "[[information-layer/sub-components/research-tab/research-tab]]"
  - "[[withdrawal-flow/withdrawal-flow]]"
  - "[[education/education]]"
  - "[[advertising/sub-components/programmatic-media-playbook/programmatic-media-playbook]]"
  - "[[advertising/advertising]]"
  - "[[information-layer/sub-components/single-game-page/single-game-page]]"
  - "[[market-maker/market-maker]]"
status: extracted
extracted-to:
  - "[[information-layer/sub-components/research-tab/research-tab]]"
  - "[[withdrawal-flow/withdrawal-flow]]"
  - "[[education/education]]"
  - "[[advertising/sub-components/programmatic-media-playbook/programmatic-media-playbook]]"
---

## Post-Call Analysis

~58-minute Tuesday touchdown. Present: Edwin, Cody + Troy (Inplay Global), Brett, George, Max, Hasan, Jared, Gary, Kevin. Heavy social banter, little of it substantive. Real content clustered around subscription pricing being set, a new W9 / tax-automation vendor for cash withdrawals, data replication / derivative-data storage, Hasan's charts demo, push-notification v1/v2 strategy, the SSP app-store-URL dependency, the volatility-moment billable-impression question, and education (an in-app "how to use the app" piece plus AI-clone persona videos). Market-maker was touched only as priority sequencing (understand, then technical, then test); mechanics were not re-discussed, see [[market-maker/market-maker]].

| Finding | Destination | Action |
|---------|-------------|--------|
| **Subscription pricing SET (Edwin, exec-level):** everything at **$49.99/mo**, two standalone monthly packages, **Research $49.99** and **Watch / Pro-View $49.99**, plus a **bundle ("Pro Trading Package") $79.99/mo**. All monthly; **ads still run on these surfaces** (George). Framed cheap vs fantasy data ($50–75/mo), betting picks (hundreds/mo), financial data (hundreds-to-thousands/mo); raw Sport Radar redistribution is $5–20k/mo per user. Free-taste vs graded-out split still to define (Cody + George deep pass). | [[information-layer/sub-components/research-tab/research-tab]] | Header + §2 pricing update. **Resolves** the research-tab pricing open question (supersedes 26-06 99c→$14.99 headline) |
| **W9 / tax-automation vendor:** cash-prize win + withdrawal over a threshold triggers an automation that fills a **W9**. Two vendors in conversation as of 21-07. **Jumped ahead of HubSpot** in the backlog. **Must be ready 29 Aug** (first games): a winner could withdraw that night; settle 29 Aug, payment 30 Aug, within the first 24h of games ending. | [[withdrawal-flow/withdrawal-flow]] | "What we know" + open-questions update |
| **Education, in-app "how to use the app" piece:** Edwin wants a navigating/tutorial piece that teaches the app itself (not just trading), since the depth (pro charts, volatility info cards, watch mode) could take a user all season to learn. | [[education/education]] | 22-07 update block |
| **Education, AI-clone persona videos:** Kevin + Cody met an AI-clone company. Create hyper-realistic AI clones, each a demographic-targeted persona (~20 clones), presenting tutorial + social content, choppable to any length, very inexpensive. Cody: LeBron reaches ~70% of the market, ~20 clones reach 95–100%. | [[education/education]] | 22-07 update block (extends the AI-UGC-avatar route) |
| **Education, social-clip length debate (unresolved):** Jared (Gen Z) wants 15–30s clips, platform-dependent (TikTok/IG short, YouTube long). Gary: too short and viewers don't understand, prefers ~45s. Edwin: do both, min ~15–30s per feature, users are not equal (build for whoever converts fastest first). Social videos, distinct from in-app modules. | [[education/education]] | 22-07 update block |
| **SSP onboarding blocked on live App Store URL (chicken-and-egg):** some SSPs need the live App Store URL before onboarding; the ones that don't are progressing; URL-gated ones wait on Apple approval (escalate Friday if silent). | [[advertising/sub-components/programmatic-media-playbook/programmatic-media-playbook]] | 22-07 update (reinforces 15-07 note) |
| **Volatility-moment billable-impression question:** Edwin, moments may be too quick to qualify as a billable impression. George, because they are **animated** IAB likely won't allow a **programmatic** unit there (programmatic wants static, fixed, aspect-ratio-controlled placements); volatility moments probably sell **direct** (relationship, not an API call). Needs research. | [[advertising/sub-components/programmatic-media-playbook/programmatic-media-playbook]] + open-questions | 22-07 update + new open-question row |
| **Side-ad wrong-edge bug (Watch Mode):** the side ad defaults to the top of the screen and gets blocked by the iPhone notch/window; should default to the bottom (George: "should be the other way around"). | [[advertising/advertising]] (light cross-link) | Noted in playbook 22-07 update as a QA item |
| **Data replication + derivative data products:** replicate everything T0 stores as a backup on InPlay's systems, plus real-time derivative data products (can't rely on T0 latency); **cold storage after N days** (a fraction of warm cost); **~5–6yr** regulatory retention (Edwin first said 10). Brett flagged compute/storage costs become real numbers, some of it is dead / non-monetizable. | Meeting doc only (candidate, see below) | Flagged as a NEW component/concern candidate for the orchestrator |
| **Push notifications v1/v2:** v1 **not user-configurable** (lean on fewer, not more); v2 **configurable** per favourites/watchlist (e.g. notify on a touchdown for followed teams vs every game event); some events always on (order fill assumed). | Meeting doc only (Push/CRM cross-cutting is in reserved [[components/components]]) | Captured here + open-question |
| **Charts demo (Hasan):** interactive zoom/drag, candlesticks, minute-level intervals, key-moment highlight (orange), **advanced/pro mode** (SMA/EMA/Bollinger + gridlines + high/low), watch-mode chart, info eye-icon showing price + win probability at a moment. **Standardise chart line colour, drop team colours** (dark-on-dark unreadable across ~160 teams; use one standard colour e.g. green line / white-on-navy). On Hasan's build already. Pro-view is monetizable (feeds Watch/Pro-View package). | Meeting doc only (light cross-link [[information-layer/sub-components/single-game-page/single-game-page]]) | Captured; no single-game-page edit (kept surgical) |
| **App Store status:** Apple silent >1 week; escalate if no response by Friday. George prefers reserving escalation for the trading build nearer launch. ~30 days to launch; Edwin pushing app signups hard (website signups lack the same gravity). | Meeting doc only (App Store row lives in reserved [[architecture/open-questions]]) | Status |
| **Sport Radar college team totals:** data absent across every endpoint checked; waiting on Sport Radar; Cody writing the press release; Edwin frustrated at being treated as a "half customer" despite paying (Kalshi/Polymarket signings noted). | Meeting doc only | Status / Cody + George own the chase |
| **TestFlight:** two app versions supported in TestFlight; the trading version to be in TestFlight by end of 22-07. | Meeting doc only | Status |
| **Deck-automation app / outreach:** Max building a deck-automation app (v2) so Edwin has full control; two-pager going to the US ad agency (John); Brett meeting Richard (WPP) 22-07 pm; outreach emails warming 32/day today toward 40–45/day over ~a week. | Meeting doc only | Status |
| **Bulk referral via contact permissions (Jared feedback):** enable contact permissions so a user can bulk-send referrals to all contacts (Snapchat-style). Cody re-sending Jared's 6-item feedback list; flagged as feature requests not to delay current work. | [[referral/referral]] (owned by another agent, not edited) | Note only |

---

**Source transcript:** `Inplay - App - Touchdown – 2026_07_22 14_30 BST – Notes by Gemini.md` (raw, in `/home/brett/shared/inplay/meeting-notes/`). This is a digest; the raw transcript is not reproduced here.
