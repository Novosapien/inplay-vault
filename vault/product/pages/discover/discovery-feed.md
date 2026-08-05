---
description: "Page spec for the Discover feed — game ticker, game cards with sparklines, featured game, NFL/NCAA toggle and team search, with navigation paths and states"
---

# Discovery Feed

> **Tab:** Discover
> **Purpose:** Browse today's games and find trading opportunities.
> **Map:** [[product/pages/PAGES|App Pages]]

---

## What Users See

The front door to the app's trading activity. Users scan today's games, spot interesting matchups, and decide where to focus their attention and capital.

---

## Key Elements

- **Game Ticker** — horizontal scrolling strip at the top showing all today's games as compact chips. Live games appear first (with live scores), then upcoming games (with kickoff times), then completed games. Tapping any chip scrolls to or navigates to that game.

- **Game Cards** — the main content. Each card shows:
  - Two teams playing (with team colors/logos)
  - Game time or live status
  - Price direction sparkline (showing recent movement)
  - Mini P&L badge if the user holds a position in either team

  Cards are deliberately limited to 3 data points — enough to decide "is this interesting?" without overwhelming.

- **Featured Game** — one marquee matchup highlighted more prominently (bigger card, more context)

- **NFL / NCAA Toggle** — filter to show only NFL games, only college football, or both

- **Search Bar** — type-ahead search across all ~163 teams (NFL + NCAA). Results show team name, division, and current price direction. Tapping a result goes directly to that Team Page.

---

## Where Users Go From Here

- Tap a game card → [[product/pages/discover/single-game-page|Single Game Page]]
- Tap a team name on a card → [[product/pages/discover/team-page|Team Page]]
- Tap a search result → [[product/pages/discover/team-page|Team Page]]
- Tap the game ticker chip → [[product/pages/discover/single-game-page|Single Game Page]]

---

## States

- **Game day (live games):** Most active state. Live games at the top with real-time score updates and active sparklines.
- **Game day (pre-game):** Games show countdown to kickoff, pre-game odds/predictions.
- **No games today:** Shows next game day's schedule with countdown. "Next game in X days."
- **Post-game:** Completed games show final scores and settlement info.
