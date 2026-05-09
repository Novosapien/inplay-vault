# InPlay Trading Challenge -- Single Game Page

> **Component:** [[information-layer]]
> **Status:** Collecting
> **Sources:** _[[meetings/08-05-2026-compoent-1]]_

---

Deep view of one matchup where sports data and market data converge. The primary engagement surface during live games.

## Key Elements (from component session)

- Sport Radar live match tracker (embedded HTML5 widget, pre/post/live states)
- Annotated price chart (SR game events cross-correlated with T0 price movements)
- Real-time game stats and play-by-play
- Market data: current price, bid/offer, order book depth
- Trading widget (owned by Trading component, embedded here)
- Leaderboard widget (mini -- user's current position and gap to cashing)
- P&L indicator (real-time)
- Volatility moment animations (micro-moments -- sponsored by advertisers)
- Both teams visible with buy/sell options for each

## Open Questions

- How much order book depth to show on mobile? Full book or just top of book (best bid/best offer)?
- Layout: how do match tracker, chart, stats, and trading widget coexist on a single mobile screen? Scrollable sections, tabs, or collapsible panels?
- Does the match tracker go full-screen on landscape rotation?
