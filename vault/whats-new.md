# InPlay Trading Challenge -- What's New

> **Project:** [[index]]

## 2026-05-17 — App Build Complete (Mock Data Phase)

The InPlay Trading Challenge mobile app now has all 20 screens built with full mock data. Every screen described in the vault sub-component specs is implemented, navigable, and styled to production standard. The app is ready for stakeholder review and user testing on-device via Expo Go or EAS builds.

### What's been built (May 12–17)

**Core Trading Screens**
- **Single Game Page** — the heart of the app. Head-to-head matchup, live match tracker (pre-game/live/post-game states), annotated price chart with time ranges, order book depth, embedded buy/sell, news feed, mini leaderboard widget
- **Portfolio** — all open positions with unrealised P&L, wallet balances, quick links to orders and history
- **Trade Confirmation Flow** — order entry → confirmation → placed screen → cancel order
- **Position Detail** — per-team position view with entry price, P&L, trade history

**Discovery & Research**
- **Discovery Feed** — horizontal game ticker, game cards with sparklines, NFL/NCAA filter, search with type-ahead across 163 teams
- **Team Page** — season price chart (candlestick), expandable season stats, division standings, schedule with results, injury report, player spotlight, team news, user's position P&L
- **Player Profile** — biographical data, position-specific stat tables, injury status, headline stats grid. Navigable from Team Page and Single Game Page
- **Full Results** — complete season game history per team
- **Full-Screen Chart** — expanded candlestick view (modal slide-up)

**Competition**
- **Leaderboard** — 3 verticals (Best P&L, Risk-Adjusted, Comeback) × 4 time horizons (Daily, Weekly, Monthly, Full Event). Gap-to-earn as the hero metric. Brand glow header (green = earning, red = not). Auto-scroll to user's position
- **Trader Profile** — public profile of other traders with performance stats

**Supporting Screens**
- **Dashboard (Home)** — wallet balances, ranking summary, proximity indicator, upcoming games
- **More tab** — Referral program (Get 1,000 / Give 500), Education hub, Settings
- **Wallet Details** — balance breakdown and transaction history

### Design System
- Dark mode default with full theme token system (colors, spacing, typography)
- Reusable component library: Card, FilterChips, SearchBar, StatusBadge, PriceIndicator, SectionHeader, ScreenGlow, GridBackground
- App-wide grid background at root layout level
- Standardised back gesture across all tab stacks
- Mobile-first — optimised for phone, consumer fintech aesthetic (not terminal UI)

### Mock Data Coverage
- 32 NFL teams + sample NCAA teams with realistic pricing
- 109 player profiles with position-appropriate stats
- 59 news items across team, game, and league categories
- Season candlestick data for historical charts
- Fake leaderboard with distinct data per vertical
- 8 trader profiles for leaderboard drill-down
- Order book depth data
- Portfolio with multiple open positions and P&L

### Product Documentation
- **[[product/app-pages]]** — complete screen map with descriptions and navigation flows (new)
- **Design system rules** added to CLAUDE.md — "change globally, not locally" principle
- **Sportradar data mapping** — confirmed all sub-component data requirements can be fulfilled by NFL/NCAA Player Profile, Team Roster, Game Summary, and Weekly Injuries endpoints

### Key Decisions
- No player images in app (requires separate NFLPA licensing) — jersey number badges used instead
- Player IDs are slug-based (`kc-patrick-mahomes`) for mock phase; will use Sportradar UUIDs in production
- Gap-to-earn is more prominent than rank number on leaderboard (per spec)
- 3 data points max per game card on Discovery (per spec)
- Bottom padding pattern (180px) on screens with floating trade button to clear tab bar

### What's Next
- Stakeholder review / on-device testing
- Backend integration planning (WebSocket for real-time prices, REST for user actions)
- State management library selection
- Authentication and KYC flow implementation

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
