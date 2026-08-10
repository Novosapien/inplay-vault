---
description: "Page spec for the Team Page research dashboard — price chart, season stats, standings, schedule, injuries, player spotlight, news and the user's position"
---

# Team Page

> **Tab:** Discover
> **Purpose:** Research dashboard for a single team — everything you need to know before trading.
> **Map:** [[product/pages/PAGES|App Pages]]

---

## What Users See

A comprehensive view of one team's performance, stats, and market data. This page exists whether or not the team is playing today — it's the place for deeper research beyond the immediate game context.

---

## Key Elements

- **Team Header** — team name, logo, colors, current record (e.g., 10-4), division standing

- **Price & Market Data** — current stock price, bid/offer spread, direction indicator (up/down with percentage change). Sticky "Trade this team" button always visible at the bottom.

- **Season Price Chart** — candlestick chart showing the team's stock price across the full season. Annotated with past volatility moments (big wins, upsets, injuries that moved the price). Time ranges available.

- **Season Stats** — expandable card with team performance statistics:
  - Passing stats (yards, TDs, completion %)
  - Rushing stats (yards, TDs, yards per carry)
  - Defensive stats (sacks, interceptions, points allowed)
  - Categories collapse/expand to manage information density

- **Division Standings** — where the team sits in their division. Win-loss record, games behind leader.

- **Schedule** — past results (with scores, W/L) and upcoming games (with dates, opponents). Past results are tappable.

- **Injury Report** — current injuries with player name, position, status (Out / Questionable / Probable), and injury type

- **Player Spotlight** — top 3-4 players with their headline stats (e.g., QB: passing yards, TDs, rating). Tappable to view full player profile.

- **Team News** — recent news items related to this team (coaching changes, signings, injury updates, game previews)

- **User's Position** — if the user holds stock in this team, shows current quantity, average entry price, and unrealised P&L

- **Live Game Banner** — when the team is currently playing, a banner links to the Single Game Page

---

## Where Users Go From Here

- Tap "Trade this team" → Order entry
- Tap a past result → [[product/pages/discover/single-game-page|Single Game Page]] for that game
- Tap "View all results" → [[product/pages/discover/full-results|Full Results]] page
- Tap a player in spotlight → [[product/pages/discover/player-profile|Player Profile]]
- Tap an upcoming game → [[product/pages/discover/single-game-page|Single Game Page]] (pre-game)
- Tap live game banner → [[product/pages/discover/single-game-page|Single Game Page]] (live)
- Tap "Your Position" → [[product/pages/trading/position-detail|Position Detail]] (Trade tab)

---

## States

- **Team playing now:** Live game banner at top, price actively moving, heightened urgency
- **Team not playing today:** Research mode — historical data, upcoming schedule, no live elements
- **User holds position:** "Your Position" card visible with P&L
- **User has no position:** "Your Position" section hidden, "Trade this team" button prominent

---

## Why This Page Matters

Not every trading decision happens in the heat of a live game. Some users want to research teams, look at form, check injury reports, and build a thesis before the game starts. The Team Page supports that deliberate, research-driven trading style — giving users confidence in their decisions.
