# InPlay Trading Challenge

> **Client:** InPlay (Edwin, Cody, Troy, Skye)
> **Status:** Components
> **Date started:** 2026-05-06

## Overview

A simulated sports equity trading platform where users trade team stocks during live NFL and college football seasons with no financial risk but real cash prizes. Currently in component deep-dive phase -- vision extracted and reviewed, component map identified (9 components), first component (Information Layer) documented with six sub-components.

## Documents

| Document | Description | Status |
|----------|------------|--------|
| [[vision]] | Product vision -- what we're building and why | Defined |
| [[architecture]] | Cross-cutting technical decisions -- tech stack, infrastructure, integrations | Not started |
| [[components]] | Component map -- all major parts of the product | In progress |

## What's New

- **Information Layer fully documented** -- component doc with all 10 sections complete, plus 6 sub-components with entity journeys, acceptance criteria, data requirements, and dependencies
  - [[single-game-page]] -- the core convergence screen, 3 journeys defined
  - [[leaderboard]] -- 3 verticals, 4 time horizons, proximity alerts, 3 journeys defined
  - [[discovery-home]] -- app entry point, search, game cards, 3 journeys defined
  - [[team-page]] -- research dashboard, historical data, live enrichment, 3 journeys defined
  - [[game-day-overview]] -- multi-game monitoring, aggregate P&L, 3 journeys defined
  - [[research-tab]] -- placeholder only, 10 questions for next call
- **Sub-component template updated** -- entity journeys now split into 3a (isolated) and 3b (cross-component) with handoff points and integration contracts
- **Vault restructured** -- `content/` renamed to `vault/`, full directory skeleton in place for all 8 components + architecture

## To-Dos

### Information Layer

- [ ] Resolve IA question: is [[game-day-overview]] a separate page or a tab within [[discovery-home]]?
- [ ] Define the [[research-tab]] -- needs dedicated session with Edwin and Cody
- [ ] Determine news feed placement -- where does the SR newswire appear? [[discovery-home]]? [[team-page]]? Both?
- [ ] Determine order book depth display -- how much Bloomberg-style data on mobile? Full book or top of book? ([[single-game-page]])
- [ ] Define "comeback trader" metric for [[leaderboard]] -- biggest absolute swing? percentage? recovery from negative?
- [ ] Define "risk-adjusted return" plain-English label for [[leaderboard]] -- can't use "Sharpe ratio" in UI
- [ ] Sport Radar client setup call -- logo toggle decision, widget customisation, ad placement within match tracker
- [ ] Define featured games selection criteria for [[discovery-home]] -- editorial? algorithmic? advertiser-driven?
- [ ] Determine whether [[team-page]] includes player-level data or team-level only
- [ ] Define leaderboard payout structure -- how many places pay out per vertical per time horizon?
- [ ] Define proximity alert thresholds for [[leaderboard]]
- [ ] Resolve daily leaderboard reset timing -- games spanning midnight ([[leaderboard]])

### Architecture

- [ ] Data source matrix: map what comes from Sport Radar, what from T0, what InPlay stores internally
- [ ] Define the cross-correlation data store ("mem store" per Brett) for volatility annotations
- [ ] Tech stack decisions -- not started

### Other Components

- [ ] Schedule Trading component deep-dive session
- [ ] Schedule remaining component sessions (Onboarding, Referral, Third Space, Education, Websites)

## Recent Activity

| Date | What happened |
|------|--------------|
| 2026-05-09 | Information Layer component and all 6 sub-components fully documented. Sub-component template updated with 3a/3b journey split. Vault restructured (content -> vault). Architecture skeleton created |
| 2026-05-08 | Component 1 deep-dive call -- Information / Bloomberg Terminal module. Covered discovery, game day, team pages, leaderboard, competitive app analysis (Poly Market, FanDuel, Hard Rock, Fanatics). Heavy tangent into ad monetisation and pricing model |
| 2026-05-06 | Vision workshop -- 2-hour session. Vision document extracted and reviewed. Component map created (9 components). Three personas defined. Cross-cutting concerns identified (Advertising, Push/CRM, Personal Dashboard) |
