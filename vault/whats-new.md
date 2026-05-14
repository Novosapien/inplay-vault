# InPlay Trading Challenge -- What's New

> **Project:** [[index]]

## 2026-05-14

- **Onboarding + Referral + Global Website extracted** from [[meetings/12-06-2026-onboarding-and-renewal-and-global-component]]
- **[[components/customer-onboarding/customer-onboarding|Customer Onboarding]]** — full 10-section component doc. Status `Collecting` → `Defined`. 5 sub-components surfaced: Discovery & App Acquisition, Registration+KYC, Wallet Provisioning, Holding State, Returning Login
  - Key decisions: registration and KYC happen as one step; T0 owns auth credentials (SSO parked); cash wallet on T0 chain (sidesteps store-of-value licensing); pre-funded wallet pool agreed in principle (pending T0 cost); holding state UX is "gray out, never hide"
- **[[components/referral/referral|Referral]]** — full 10-section component doc merging vision content with new transcript. Status `Collecting` → `Defined`. 7 sub-components surfaced: Code Lifecycle, Share Surfaces, Bonus Campaigns, Cash Eligibility Tracking, Social Engagement Credits, Sponsor Redemption, Donor/Group Accounts (exploratory)
  - Key decisions: lifetime-stable codes; "Get 1,000 / Give 500" in orange on every surface; QR + dot card + t-shirt strategy; embedded-post QR mechanic; transparent eligibility checklist (no hidden T&Cs); cash eligibility rules owned here, surfaced at withdrawal moment
- **[[components/inplay-global-website/inplay-global-website|InPlay Global Website]]** — short summary + action list (design is in flight). Status `Collecting` → `In Design`
  - Multisport positioning locked; hero tagline "Trade sports as stocks. Buy, sell, hold — every play, every game, every season."; pages prioritised (Home / About / Advertising); Newsroom + Markets hidden; light-mode toggle to add
- **New component:** **[[components/withdrawal-flow/withdrawal-flow|Withdrawal Flow]]** (stub) — bank info + crypto wallet + 1099 captured at first withdrawal (not signup). Needs dedicated session
- **New cross-cutting concerns:**
  - **Analytics & Funnel Measurement** — end-to-end CTA tracking (social engagement → ad → install → onboard → first trade → referral conversion → LTV)
  - **Cybersecurity & Data-Handling Framework** — Troy flagged dedicated architecture session needed (PII from Persona, biometrics, location data, bank info)
- **[[audiences|Canonical audiences doc]]** created — 4 audiences (Crypto-Savvy Sports Trader, Analytical Fan / Armchair GM, Finance-Curious Student, Veteran Trader-Bettor). Brand-entity audience work merged with vision content. Audience #4 (Edwin's profile) added. Vision Section 2 refactored to link to canonical doc
- **Terminology fix:** "persona" now refers exclusively to the KYC vendor (Persona). User types are called "audiences"

## 2026-05-09

- **Information Layer fully documented** -- component doc with all 10 sections complete, plus 6 sub-components with entity journeys, acceptance criteria, data requirements, and dependencies
  - [[single-game-page]] -- the core convergence screen, 3 journeys defined
  - [[leaderboard]] -- 3 verticals, 4 time horizons, proximity alerts, 3 journeys defined
  - [[discovery-home]] -- app entry point, search, game cards, 3 journeys defined
  - [[team-page]] -- research dashboard, historical data, live enrichment, 3 journeys defined
  - [[game-day-overview]] -- multi-game monitoring, aggregate P&L, 3 journeys defined
  - [[research-tab]] -- placeholder only, 10 questions for next call
- **Sub-component template updated** -- entity journeys now split into 3a (isolated) and 3b (cross-component) with handoff points and integration contracts
- **Vault restructured** -- `content/` renamed to `vault/`, full directory skeleton in place for all 8 components + architecture
- **Component placeholders created** -- all 8 components have directories and entry-point docs with key elements from the vision workshop

## 2026-05-06

- **Vision document extracted** from 2-hour workshop session with Edwin, Cody, Troy, Skye
- **Component map created** -- 9 components identified, all in Collecting status
- **Three personas defined** -- Young Aspiring Trader, Sports-Passionate Casual, Experienced Trader
- **Cross-cutting concerns identified** -- Advertising, Push/CRM, Personal Dashboard
