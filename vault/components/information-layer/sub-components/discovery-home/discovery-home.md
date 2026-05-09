# InPlay Trading Challenge -- Discovery / Home

> **Component:** [[information-layer]]
> **Status:** Collecting
> **Sources:** _[[meetings/08-05-2026-compoent-1]]_

---

Entry point to the app. Users browse today's games, search for teams, and see featured matchups.

## Key Elements (from component session)

- Horizontal scrolling game ticker at top of screen
- Search with type-ahead across ~163 teams (32 NFL + ~131 NCAA), disambiguation for overlaps (e.g., Buffalo)
- Featured/marquee games (top 5 college, top 5 NFL per week)
- Per-game cards with minimal info: game time, win probability, stock price direction (up/down indicator)
- "Last game of the day" visual indicator (critical for daily prize engagement)
- Mini P&L if user has active positions in today's games

## Open Questions

- Is this the same page as Game Day Overview, or are they separate views?
- How much personalisation? Can users pin favourite teams, hide sports they don't follow?
- Where does the news feed appear -- here, or only on deeper pages?
