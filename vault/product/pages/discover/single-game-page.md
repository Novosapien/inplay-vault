---
description: "Page spec for the Single Game Page, the core trading screen — match tracker, annotated price chart, order book, buy/sell and news across pre/live/post states"
---

# Single Game Page

> **Tab:** Discover
> **Purpose:** The core screen — where sports data, market data, and trading converge. This is where most trading happens.
> **Map:** [[product/pages/PAGES|App Pages]]

---

## What Users See

Everything needed to make a trading decision about a specific game, all on one screen. Two teams going head-to-head, with live game information, price charts, market depth, and the ability to buy or sell without leaving.

This is the screen users spend the most time on during live games.

---

## Key Elements

- **Team Header** — both teams displayed side by side with:
  - Team name and colors
  - Current stock price for each team
  - Price direction indicator (up/down arrow with percentage)
  - Tappable → goes to Team Page

- **Match Tracker** — the top section adapts based on game state:
  - **Pre-game:** Season form comparison, head-to-head record, key matchup stats, game time countdown
  - **Live:** Current score, quarter/time, possession indicator, last play description, running team stats
  - **Post-game:** Final score, game stats summary, "Market settled" indicator

- **Price Chart** — annotated candlestick/line chart showing price movement over time. Key game events (touchdowns, turnovers, injuries) are marked on the chart so users can see how events affected price. Time range selector: 1 Hour, 3 Hours, Full Game, Season.

- **Market Data** — bid price, offer price, last traded price, and spread for both teams

- **Order Book** — visual depth chart showing buy and sell orders stacked at different price levels. Shows market liquidity.

- **Buy/Sell Buttons** — for both teams. Users can place a trade directly from this page without navigating away. Tapping opens an order entry panel.

- **News Feed** — game-relevant news items (injury updates, analyst commentary, line movements)

- **Mini Leaderboard Widget** — shows user's current rank and gap-to-earn. Contextual motivation: "You're 47 places from earning today."

---

## Where Users Go From Here

- Tap team name → [[product/pages/discover/team-page|Team Page]]
- Tap a player name (in stats) → [[product/pages/discover/player-profile|Player Profile]]
- Tap Buy/Sell → Order entry panel (stays on page)
- After confirming trade → [[product/pages/trading/confirmation|Trade Confirmation]] → [[product/pages/trading/order-placed|Order Placed]]
- Tap leaderboard widget → [[product/pages/leaderboard/leaderboard|Leaderboard]]
- Tap news item → News detail modal

---

## States

### Pre-Game
Users are researching and positioning before kickoff. Market is active but lower volume. Screen emphasises historical data, matchup stats, and pre-game narratives.

### Live Game
Most active state. Prices moving in real-time, game events appearing, chart updating, order book shifting. This is where the excitement and urgency lives. Key game events (scores, turnovers, injuries) trigger visual "volatility moment" animations.

### Post-Game
Market settles to final value. Chart shows the complete game story. Users can see their final P&L. "Game Over" state clearly communicated. Market data shows settlement price.

---

## Why This Page Matters

This is the page that makes InPlay different from a sportsbook. Instead of placing a bet before the game and waiting, users are actively trading throughout the game — buying and selling as the situation changes, reacting to game events, managing risk. The Single Game Page is designed to support that active, engaged experience.
