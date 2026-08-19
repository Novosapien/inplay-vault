---
description: "Index of all 21 app screens grouped by the 5 bottom-nav tabs, with links to each page doc and the key navigation flows between them"
---

# App Pages

> **Last updated:** 2026-05-17
> **Total screens:** 21

This directory documents every screen in the InPlay Trading Challenge app. Each page has its own file describing what users see, what they can do, and how they navigate to and from it.

---

## Structure

The app has 5 main tabs accessible from the bottom navigation bar:

| Tab | Label | Purpose |
|-----|-------|---------|
| [[product/pages/home/dashboard\|Home]] | Home | Personal overview — wallets, rankings, upcoming games |
| [[product/pages/discover/discovery-feed\|Discover]] | Discover | Find games and research teams |
| [[product/pages/trading/portfolio\|Trade]] | Trade | Manage positions and execute trades |
| [[product/pages/leaderboard/leaderboard\|Ranks]] | Ranks | Competition standings and gap-to-earn |
| [[product/pages/more/settings-hub\|More]] | More | Referral, education, settings |

---

## Pages by Area

### Home (1 screen)
- [[product/pages/home/dashboard|Dashboard]]

### Discover (6 screens)
- [[product/pages/discover/discovery-feed|Discovery Feed]] — browse today's games
- [[product/pages/discover/single-game-page|Single Game Page]] — the core trading screen
- [[product/pages/discover/team-page|Team Page]] — research a single team
- [[product/pages/discover/player-profile|Player Profile]] — individual player stats and bio
- [[product/pages/discover/full-results|Full Results]] — complete season results for a team
- [[product/pages/discover/full-screen-chart|Full-Screen Chart]] — expanded price chart

### Trading (8 screens)
- [[product/pages/trading/portfolio|Portfolio]] — all open positions and balances
- [[product/pages/trading/position-detail|Position Detail]] — deep view of one position
- [[product/pages/trading/open-orders|Open Orders]] — pending unfilled orders
- [[product/pages/trading/trade-history|Trade History]] — record of all executed trades
- [[product/pages/trading/wallet|Wallet Details]] — balance breakdown
- [[product/pages/trading/confirmation|Trade Confirmation]] — review before submitting
- [[product/pages/trading/order-placed|Order Placed]] — success confirmation
- [[product/pages/trading/cancel-order|Cancel Order]] — cancel a pending order

### Leaderboard (2 screens)
- [[product/pages/leaderboard/leaderboard|Leaderboard]] — competition rankings
- [[product/pages/leaderboard/trader-profile|Trader Profile]] — another trader's public stats

### More (4 screens)
- [[product/pages/more/settings-hub|Settings Hub]] — main menu
- [[product/pages/more/referral|Referral Program]] — invite friends, earn InPlay dollars
- [[product/pages/more/education|Education Hub]] — learn how trading works
- [[product/pages/more/settings|Settings]] — preferences and account

---

## Key Navigation Flows

**Browse → Trade (3 taps to execute a trade)**
Discovery Feed → tap game → Single Game Page → tap Buy/Sell → Confirmation → Done

**Research → Trade**
Team Page → review stats → tap "Trade this team" → Confirmation → Done

**Leaderboard → Trade**
Leaderboard → see gap-to-earn → go to Discovery → find game → trade

**Check Positions**
Dashboard → tap position → Position Detail → optionally sell

**Deep Research**
Discovery → Game Page → tap team → Team Page → tap player → Player Profile
