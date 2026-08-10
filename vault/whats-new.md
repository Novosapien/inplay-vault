---
description: "Rolling changelog — dated entries for every major vault update, from the vision workshop through SNT-1, IPO pricing v1.0 and the tZERO OMS Q&A"
---

# InPlay Trading Challenge -- What's New

> **Project:** [[index]]

## 2026-08-10: Five touchdowns digested, and a new Compliance section

Processed the 27 July → 7 August touchdown block ([[27-07-2026-touchdown]],
[[29-07-2026-touchdown]], [[31-07-2026-touchdown]], [[03-08-2026-touchdown]],
[[07-08-2026-touchdown]]). Three weeks of calls, two weeks from the IPO.

**A new [[compliance/compliance|Compliance]] section.** The regulatory
constraints had been scattered through meeting notes; they now have a home, with
[[compliance/regulatory-positioning]] (the securities-not-gambling argument, the
SEC filing and gun-jumping risk, Rule 255, the Kalshi litigation, state-by-state
exposure) and [[compliance/eligibility-and-age-gating]] (who may hold which
account and what they may win). Eight live build constraints are listed, from
"never say regulated by the SEC" to "non-KYC users only see under-18-safe ads".

**Onboarding is now three tiers, not one.** KYC was killing the funnel, and
international students can never qualify for cash anyway, so
[[customer-onboarding/customer-onboarding]] splits into **Trader Full** (US tax
resident, 18+, full KYC, cash prizes), **Trader Medium** (international, KYC'd,
no cash) and **Trader Light** (email only, 13+, no cash). Everyone can trade —
it is a simulator. One hard blocker: tZERO's onboarding API still demands a
DOB of 18+, so Trader Light cannot be allocated a wallet until they relax it.
Ahead of all three sits Edwin's non-negotiable **first-open explainer and fork
screen**, because today a referred user's first sight of the app is a stadium
picture that explains nothing.

**The IPO's market structure is settled.** [[ipo-module/ipo-module]] and
[[market-maker/market-maker]] both re-based: a **broker-dealer MPID** holds and
sells the whole **1,000,000-share-per-team** issuance, and the **taker algo
buys ≥600,000** of it with randomised sizing and timing, purely so that no team
visibly fails to sell. The maker never touches the primary. NCAA opens for five
days, NFL for two, and the load-balancing algo is dropped until the NBA in
October. Prices publish early via OTA and **freeze three days out**.

**The valuation chain is confirmed end to end.** The Sport Radar probabilities
contract amendment is signed at no extra cost and live in production, closing
the S1 blocker that had no input at all. We poll at **500ms in-game**; the RP
formula gained its missing term (the in-game leg is a **delta from the kickoff
probability**, not the raw probability). Edwin also settled a real design worry:
the MM dragging price back toward the reference price is not a bug, it is how
every market works.

**Trading works end to end** into tZERO, with fills, partial fills, shorts and
notifications ([[trading/trading]]). The **Android app is live**. AdMob is
serving, with an SSP ladder capped at three networks and **Kochava** picked as
the MMP. **Avalara** is chosen for W-9 handling; the payout processor is still
the open gap. The app has been restructured into Teams / League / Schedule /
Games tabs with a live order book on the team page.

**Flagged for focused sessions, not written here:** micro-challenges and private
leaderboards for universities and frats; the strategy **back-test lab**; and the
**analyst portal** that the empty Analyst tab needs.

## 2026-07-30: SNT-1 Synthetic Noise Taker

Edwin introduced a **second house agent** for the Challenge and sent a spec-quality reference implementation, now processed into the market-maker component: [[market-maker/systems/synthetic-noise-taker]] (code safe-copied to `sources/snt1_noise_taker.py`).

SNT-1 is a **taker-only, non-participant house account** that crosses the bid/ask with random sizes at random times, so **every team book shows real trading from IPO onward, even with no games on**. It is deliberately a **controlled loser**: the spread it pays is the subsidy that seeds an active secondary market. It earns no leaderboard credit, and its prints against the Market Maker carry no participant side, so they fall outside the $2.50 off-field volume split automatically (no spec change needed). The realism layer mimics retail disposition-effect profit-taking, conditioning only on its own cost basis so the flow stays uninformed.

Processed per the market-maker working guide: the [[market-maker/market-maker]] hub now lists two house agents (MM + SNT-1), with decisions, parameters (all proposed, two tuning levers flagged), open questions (E17/E18 for Edwin, N15/N16 for us: the ExchangeAdapter build and five production-hardening tasks), a session note, and glossary/learnings entries all updated. The main open item Edwin flagged is how SNT-1 interacts with the MM's quoting and inventory during the IPO Primary Mandate rounds.
## 2026-07-29: IPO Pricing Model v1.0

Edwin delivered the **IPO pricing model** for the 2026 season, now stored safely in the vault and processed: [[ipo-pricing-2026]] (source workbook safe-copied to `components/ipo-module/sources/`).

It sets the **listed IPO price for every tradeable team company**, all **32 NFL** and **138 NCAA** teams, from a clear formula: **IPO = $5.00 x E[Wins] + $2.50 x E[Ties] (NFL only) + $2.50/game x expected volume-capture share**. The on-field leg comes from devigged BetMGM win totals; the off-field leg from a Popularity Index (0.6 x brand + 0.4 x performance) with Bradley-Terry per-game capture. Prices range from about **$81 (LA Rams)** down to **$21 (Charlotte)**. The doc also captures the parameters, the methodology, and the author's caveats (notably the North Dakota State / Sacramento State non-universe pricing, and that supplying the exact 2026 schedule CSV will move NCAA prices by ~$1 to $2).

This fixes per-share IPO value; the remaining open variable is float size (shares issued per team), tracked in [[open-questions]]. The $5/win, $2.50/tie and $2.50/game accruals are the same [[earnings-report]] settlement mechanics, so the IPO price is the expected sum of every future earnings distribution.

## 2026-07-29: tZERO OMS Q&A + Risk Settings

Processed Rob Colucci's (tZERO) written answers from a QA testing session, plus the IPLY OMS risk-settings spreadsheet, into the vault ([[29-07-2026-tZERO-rob-qa]]; matrix in [[tzero-oms-risk-settings]]; digested into [[tzero]] §11).

**Fixed live in the session:** account-scoped position tracking (positions had been aggregating at the firm level because test accounts used TEST-environment credentials; the credential routing was corrected), and ticker `IPTCCONH` (was missing from OMS SIM, now created).

**Answered:** IPLY accounts carry positions overnight by default; bid/ask is driven by FIX orders with a market maker setting the market (no pre-set price list); UEPR/UEAR are enabled but there is no bulk position query, so EOD reconciliation needs a dedicated session. This also closes two 23-07 open items: the OMS has **Stop Wash Trades ON** (the self-match prevention the market maker needed), and the **risk-settings matrix** Rob owed has been delivered. The matrix's **limit-price-range tiers** give the market maker its OMS-level price band to reconcile against.

**Primary issuance:** the OMS can seed an IPO reference price, but tracking capital raised and shares remaining needs a **dedicated cap-table management tech stack**, which sits alongside the 23-07 direct-mint decision. Selecting that stack is a new open item.

## 2026-07-24: Meeting-Notes Batch Digested

Processed the 22 Jul touchdown, the 23 Jul tZERO weekly tech sync, the 24 Jul touchdown, Jared Sapirman's written app feedback, and two subscription/research source docs into the vault. (The 20 Jul touchdown and 23 Jul market-maker follow-up were already processed and are not repeated here; the market-maker component already owns that material.)

**Subscriptions priced.** Research and Watch/Pro-View at $49.99/mo each, bundled "Pro Trading Package" at $79.99/mo (ads still run on those surfaces). This resolves the long-open [[research-tab]] pricing question and supersedes the earlier tiered headline. See [[22-07-2026-touchdown]].

**IPO issuance decided.** Bypass the Matching Engine and mint tokens straight to investor wallets via tZERO's transfer-agent workspace (single-price, long-only primary raise); Novo needs minting access. The tZERO environment also splits into SIM (the current one) plus a new PROD, with production symbology decoupled from team names and a $1.20/share short fee. See [[23-07-2026-tZERO-weekly]].

**Also on 22 Jul:** a W9 tax-automation vendor jumps the backlog to be ready for the 29 Aug first games; education adds AI-clone persona videos and an in-app "how to use the app" piece; SSP onboarding is gated on the live App Store URL.

**Jared's feedback folded in** ([[jared-app-feedback-jul-2026]]): contact-permission referral invites, a ~2s cold-start target (down from ~4s), public usernames with anti-impersonation guardrails, and a social-layer direction (Groups & Leagues, influencer-hosted groups, richer streaks) plus a Dynamic Island presence, flagged for a focused session.

**Subscription pricing + research reports** ([[research-tab]]): two source docs fold in a four-tier pricing ladder (Free trial / Plus $24.99 / Pro $49.99 / Elite $79.99) and the first concrete pre-canned report catalog. The tier prices are a proposal under review, not locked: the strategy doc itself calls $29.99 the "optimal" Pro launch price and the middle tier is floated at $34.99–$39.99. Research/subscriptions are not a launch feature (target ~October), though the research piece is wanted within 1–2 weeks so influencers can talk about it.

**24 Jul touchdown** ([[24-07-2026-touchdown]]): ad serving moves to the live path (AdMob verifying now the App Store ID has landed, first SSP imminent, Google Tag Manager + an MMP decision); the Sport Radar feed-speed question is settled by necessity (custom Gamecast runs off the media feed since the betting feed is inaccessible, probabilities-API fixes being chased); trading infra is fully mapped and testable via historical-game simulations; payouts and tax forms get a delay-payout launch fallback; the KYC-less variant is parked to September; and a new guest-analyst "Analyst Prices" page was requested.

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
- **[[product/pages/PAGES|App Pages]]** — complete screen map with descriptions and navigation flows (new)
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

- **Onboarding + Referral + Global Website extracted** from [[12-05-2026-onboarding-and-renewal-and-global-component]]
- **[[components/customer-onboarding/customer-onboarding|Customer Onboarding]]** — full 10-section component doc. Status `Collecting` → `Defined`. 5 sub-components surfaced: Discovery & App Acquisition, Registration+KYC, Wallet Provisioning, Holding State, Returning Login
  - Key decisions: registration and KYC happen as one step; tZERO owns auth credentials (SSO parked); cash wallet on tZERO chain (sidesteps store-of-value licensing); pre-funded wallet pool agreed in principle (pending tZERO cost); holding state UX is "gray out, never hide"
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
