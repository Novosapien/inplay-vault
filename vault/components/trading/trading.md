# InPlay Trading Challenge -- Trading

> **Vision:** [[vision]]
> **Date:** 2026-05-06
> **Status:** Collecting
> **Sources:** _[[meetings/06-05-2026-vision-workshop]], [[meetings/08-05-2026-compoent-1]]_

---

Trade execution and portfolio management. Covers the "Act -> Confirm -> Review" portion of the user journey. Identified in vision workshop. Interlinking points captured during Information Layer session. Awaiting dedicated session.

## Key Elements (from vision)

- Buy/sell/long/short execution
- Order management
- Portfolio view
- P&L tracking (daily/weekly/monthly)
- Trading wallet (100K cap)
- Referral wallet reload (below 25K trigger)
- Position management (seconds to weeks)
- Real-time during live games

## Proposed Sub-Components (from Information Layer session -- not confirmed)

| Sub-Component | Overview | Status |
|--------------|----------|--------|
| Order Entry | Buy/sell widget -- embedded on Information Layer's Single Game Page. Both teams in a matchup available (buy/sell Team A, buy/sell Team B) | Proposed |
| Trade Confirmation / Receipt | Swipe-up confirmation page after trade execution. High-value ad placement opportunity | Proposed |
| Portfolio View | Current positions across all teams, unrealised P&L, total value | Proposed |
| Trade History | Past trades, what was bought/sold and when, realised P&L | Proposed |
| Order Management | Open orders, cancellations, modifications (if applicable) | Proposed |

## Interlinking with Information Layer

| Information Layer page | Trading element present | Data flow |
|---|---|---|
| Single Game Page | Order entry widget, real-time P&L indicator | IL shows market data -> user decides -> hits buy -> Trading takes over |
| Discovery / Home | Price direction per game (up/down arrow) | Trading engine provides current price, IL displays it |
| Team Page | "Trade this team" CTA, current position if held | Links through to order entry |
| Game Day Overview | Mini P&L if you have active positions in today's games | Trading provides position data, IL displays |
| Leaderboard | Ranking calculated from trading P&L | Trading provides P&L, Challenge rules calculate rank, IL displays |

## Sub-Components

_Proposed only. Awaiting dedicated session to confirm._
