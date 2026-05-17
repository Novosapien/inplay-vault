# App Pages

> **Last updated:** 2026-05-17
> **Total screens:** 21

This directory documents every screen in the InPlay Trading Challenge app. Each page has its own file describing what users see, what they can do, and how they navigate to and from it.

---

## Structure

The app has 5 main tabs accessible from the bottom navigation bar:

| Tab | Label | Purpose |
|-----|-------|---------|
| [[home/dashboard\|Home]] | Home | Personal overview — wallets, rankings, upcoming games |
| [[discover/discovery-feed\|Discover]] | Discover | Find games and research teams |
| [[trading/portfolio\|Trade]] | Trade | Manage positions and execute trades |
| [[leaderboard/leaderboard\|Ranks]] | Ranks | Competition standings and gap-to-earn |
| [[more/settings-hub\|More]] | More | Referral, education, settings |

---

## Pages by Area

### Home (1 screen)
- [[home/dashboard|Dashboard]]

### Discover (6 screens)
- [[discover/discovery-feed|Discovery Feed]] — browse today's games
- [[discover/single-game-page|Single Game Page]] — the core trading screen
- [[discover/team-page|Team Page]] — research a single team
- [[discover/player-profile|Player Profile]] — individual player stats and bio
- [[discover/full-results|Full Results]] — complete season results for a team
- [[discover/full-screen-chart|Full-Screen Chart]] — expanded price chart

### Trading (8 screens)
- [[trading/portfolio|Portfolio]] — all open positions and balances
- [[trading/position-detail|Position Detail]] — deep view of one position
- [[trading/open-orders|Open Orders]] — pending unfilled orders
- [[trading/trade-history|Trade History]] — record of all executed trades
- [[trading/wallet|Wallet Details]] — balance breakdown
- [[trading/confirmation|Trade Confirmation]] — review before submitting
- [[trading/order-placed|Order Placed]] — success confirmation
- [[trading/cancel-order|Cancel Order]] — cancel a pending order

### Leaderboard (2 screens)
- [[leaderboard/leaderboard|Leaderboard]] — competition rankings
- [[leaderboard/trader-profile|Trader Profile]] — another trader's public stats

### More (4 screens)
- [[more/settings-hub|Settings Hub]] — main menu
- [[more/referral|Referral Program]] — invite friends, earn InPlay dollars
- [[more/education|Education Hub]] — learn how trading works
- [[more/settings|Settings]] — preferences and account

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
