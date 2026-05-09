# InPlay Trading Challenge -- Single Game Page

> **Component:** [[information-layer]]
> **Date:** 2026-05-09
> **Status:** Collecting
> **Owner:** George Westbrook
> **Sources:** _[[meetings/08-05-2026-compoent-1]]_

---

## 1. What Does This Sub-Component Do?

**Functional purpose:**

The Single Game Page is the convergence point of the entire app -- where sports data, market data, and trading come together on a single screen for one specific matchup. This is where users spend the majority of their time during live games. It's the page a user lands on when they click into a game from Discovery or Game Day Overview.

The page shows two teams in a head-to-head matchup. Users can see the Sport Radar live match tracker (the game playing out visually), an annotated price chart (game events mapped to price movements), real-time game stats, and market data (bid/offer, order book depth). An embedded trading widget from the Trading component lets them buy or sell either team without leaving the page. A mini leaderboard widget shows their current position and gap to cashing. During live games, volatility moments (touchdowns, turnovers, injuries) trigger visual animations and sponsored micro-moments across the page.

The page exists in three states: pre-game (stats, weather, venue, matchup context), live (real-time everything), and post-game (final stats, results, chart review). It's also the primary surface for advertiser micro-moments -- sponsors own specific in-game events that trigger visual moments on this page.

**Entities that interact with it:**

- All three user personas (Young Aspiring Trader, Sports-Passionate Casual, Experienced Trader) -- all post-onboarding
- The Experienced Trader persona will spend the most time here and consume the most data (order book depth, chart annotations, market data)
- The Sports-Passionate Casual may use the match tracker as their primary way of following the game when broadcast isn't available

---

## 2. What Needs to Happen?

**Functional requirements:**

- User can view two teams in a head-to-head matchup with current stock prices and direction indicators for each
- User can view the Sport Radar live match tracker (embedded HTML5 widget) in pre-game, live, and post-game states
- User can view a price chart for this game's timeline, annotated with volatility moments (game events mapped to price movements)
- User can view real-time game stats and play-by-play data during live games
- User can view market data: current price, bid/offer, order book depth for both teams
- User can see their current positions in either team (if held) and unrealised P&L
- User can access buy/sell for either team without leaving the page (Trading component widget embedded)
- User can see their leaderboard position and gap to the nearest payout position (mini leaderboard widget)
- User can tap on a team name/logo to navigate to the Team Page for deeper research
- Volatility moments trigger visual animations and chart annotations in real time
- Sponsored micro-moments display during volatility events
- Page works across mobile and tablet (Sport Radar widgets are HTML5 responsive)

**Business rules:**

- Market data must update in real time during live games (SR pushes every 1-2 seconds)
- Language must use "earn" not "win" throughout
- Volatility moment animations must not obscure buy/sell buttons or critical pricing data
- Both teams in the matchup must be tradeable from this page (buy or sell either team)

**Edge cases:**

- What happens when SR data feed goes down during a live game? -> Show last known state with timestamp and "delayed" indicator
- What happens when T0 price feed is delayed? -> Disable buy/sell, show "trading paused" with explanation
- What if multiple volatility moments happen within seconds of each other? -> Group or stack annotations rather than overlapping
- What if the user is viewing a pre-game page and the game starts? -> Page should transition to live state automatically
- What if the user has no positions in either team? -> P&L section hidden or shows "no positions" rather than empty state

---

## 3. Entity Journeys

### 3a. Isolated Journeys

#### Journey 1: User views a live game

**Entity:** User (all personas)

**Input:** User clicks into a specific game from Discovery / Home or Game Day Overview

**Outcome:** User can see all relevant game and market data for this matchup and has enough context to decide whether to trade

**Steps:**

```mermaid
graph TD
    A[User selects game from Discovery] --> B[Single Game Page loads]
    B --> C[Match tracker shows current game state]
    B --> D[Price chart displays with annotations]
    B --> E[Market data: bid/offer/last for both teams]
    B --> F[Mini leaderboard shows user position]
    C --> G{Game status?}
    G -->|Pre-game| H[Pre-game stats, weather, venue]
    G -->|Live| I[Live play-by-play animation]
    G -->|Post-game| J[Final stats and results]
    H --> K[User has full context for this matchup]
    I --> K
    J --> K
```

**Acceptance criteria:**

- [ ] Page loads within 2 seconds of selection
- [ ] Both teams visible with current stock prices and direction indicators (up/down arrow, percentage)
- [ ] Sport Radar live match tracker displays in correct state (pre/live/post)
- [ ] Price chart shows game timeline with annotated volatility moments
- [ ] Market data (bid, offer, last price) updates in real time during live games
- [ ] Mini leaderboard shows user's current rank and gap to nearest payout position
- [ ] User can distinguish which team they hold a position in (if any)
- [ ] Page transitions automatically from pre-game to live when the game starts

---

#### Journey 2: Volatility moment occurs during a live game

**Entity:** User

**Input:** A key game event happens (touchdown, turnover, injury) during a live game the user is watching

**Outcome:** User sees the moment reflected across the page -- price movement, chart annotation, visual animation -- and can quickly assess whether to act

**Steps:**

```mermaid
graph TD
    A[Key game event occurs] --> B[Match tracker reflects the play]
    A --> C[Prices update for both teams]
    A --> D[Chart annotation appears at timestamp]
    A --> E[Volatility moment animation fires]
    E --> F[Sponsored micro-moment displays]
    B --> G[User sees converged update]
    C --> G
    D --> G
    F --> G
    G --> H{User response}
    H -->|Wants to trade| I[Moves to buy/sell - see cross-component journey]
    H -->|Continues watching| J[Stays on page, monitors next movement]
```

**Acceptance criteria:**

- [ ] Game events trigger visible annotations on the price chart within the SR data refresh window
- [ ] Volatility animation is noticeable but doesn't obscure buy/sell buttons or critical data
- [ ] Sponsored content during micro-moments feels integrated, not interruptive
- [ ] Prices for both teams update following the event
- [ ] User can see the magnitude of the price movement (not just direction)
- [ ] Previous volatility moments remain visible as annotations on the chart timeline
- [ ] 15-20 volatility moments per game on average (per Edwin/Cody estimate)

---

### 3b. Cross-Component Journeys

#### Journey 1: User executes a trade from the game page

**Entity:** User (all personas)

**Input:** User decides to buy or sell one of the two teams while viewing game data

**Handoff point:** User taps buy/sell -> Trading component's order entry widget opens. State passed: team selected, current price, game context. On return: updated P&L, updated position, potentially shifted leaderboard rank

**Components involved:** Information Layer (Single Game Page) -> Trading (Order Entry -> Confirmation) -> Information Layer (Single Game Page)

**Outcome:** User has executed a trade and returned to the game page with updated P&L and position

**Steps:**

```mermaid
graph TD
    A[User views game data, decides to trade] --> B{Which team and direction?}
    B -->|Buy Team A| C[Tap Buy on Team A]
    B -->|Sell Team A| D[Tap Sell on Team A]
    B -->|Buy Team B| E[Tap Buy on Team B]
    B -->|Sell Team B| F[Tap Sell on Team B]
    C --> G[HANDOFF: Order entry widget - Trading component]
    D --> G
    E --> G
    F --> G
    G --> H[User enters quantity or dollar amount]
    H --> I[User confirms trade]
    I --> J[Trade confirmation / receipt - Trading component]
    J --> K[RETURN: Back on game page]
    K --> L[P&L indicator updated]
    K --> M[Position for this game now visible]
    K --> N[Leaderboard position may have shifted]
```

**Acceptance criteria:**

- [ ] Buy/sell available for both teams in the matchup
- [ ] User can enter trade by dollar amount or share quantity (fractional shares supported)
- [ ] Order entry shows current bid/offer price and estimated cost/return
- [ ] After trade confirmation, user returns to the game page (not redirected elsewhere)
- [ ] P&L indicator updates immediately after trade execution
- [ ] Current positions for this game visible on the page after trading
- [ ] Mini leaderboard reflects any rank change from the trade

---

## 4. Look and Feel

**Design specifics:**

Data-dense but layered. The game page is the most information-rich screen in the app -- match tracker, price chart, market data, trading widget, leaderboard widget all coexist. On mobile this means vertical stacking with the most critical elements (match tracker, prices, buy/sell) visible without scrolling, and deeper data (full chart, order book, stats) accessible by scrolling down. Dark mode preferred for this screen specifically -- it's the "trading floor" experience.

**Reference products:**

- **Poly Market event page** -- clean layout with price, chart, and trade entry on one screen. Take: the density without clutter
- **FanDuel in-game view** -- match tracker with odds alongside. Take: the coexistence of game visualisation and trading data. Avoid: the information overload and internal ad banners
- **Bloomberg mobile** -- green/red directional arrows with percentage. Take: quick-glance price direction indicators

**UX principles specific to this sub-component:**

- Match tracker and buy/sell buttons must be visible without scrolling -- these are the two most-used elements during a live game
- Volatility moment animations must not obscure actionable elements (buy/sell, prices)
- Price chart annotations should be readable at mobile scale -- short labels ("TD Alabama", "INT") not full sentences
- The page must feel alive during a game -- real-time updates across multiple elements create the sense that "something is always happening" (Cody's point about subconscious engagement)

---

## 5. Data Requirements

| What | Direction | Description | Source / Destination |
|------|-----------|------------|---------------------|
| Live play-by-play events | In | Real-time game events (touchdowns, turnovers, injuries, drives). Updates every 1-2 seconds during live games | Sport Radar push API |
| Live match tracker widget | In | Embedded HTML5 visualisation of the game. Pre/live/post states | Sport Radar hosted solution |
| Win probabilities | In | Real-time probability calculations for both teams | Sport Radar |
| Game metadata | In | Teams, venue, weather, game time, status (pre/live/post) | Sport Radar |
| Current prices (bid/offer/last) | In | Real-time stock prices for both teams in this matchup | T0 ATS |
| Order book depth | In | Number of orders at each price level for both teams | T0 ATS |
| Price history for this game | In | Price movements since game start, for the chart timeline | T0 ATS |
| Volatility moment annotations | In | Cross-correlated data: which SR event mapped to which price movement, with timestamps | InPlay internal store |
| User's current positions | In | Whether the user holds shares in either team, quantity, average entry price | Trading component |
| User's P&L | In | Current unrealised P&L for positions in this game | Trading component |
| Leaderboard position | In | User's current rank, gap to payout, which vertical they're closest in | Leaderboard sub-component |
| Sponsored micro-moment content | In | Which advertiser owns this game/moment, creative assets | Advertising (cross-cutting) |

---

## 6. Dependencies

| Depends on | What we need | Blocking for build? |
|-----------|-------------|----------|
| Sport Radar | Live data feeds, match tracker widget, game metadata | Yes -- no SR, no game page |
| T0 ATS | Real-time prices, order book, price history | Yes -- no T0, no market data |
| Discovery / Home (sibling) | Navigation context -- which game was selected | No -- can load directly via deep link |
| Leaderboard (sibling) | User's current rank and proximity data for mini widget | No -- can mock or hide widget |
| Trading component | User positions, P&L, order entry widget | No -- can mock positions; order entry can be added later |
| Advertising (cross-cutting) | Sponsored content for micro-moments | No -- can run without ads initially |
| InPlay internal store | Cross-correlated volatility data for chart annotations | No -- chart works without annotations, just less rich |

**What siblings or other components need from this one:**

- Leaderboard needs to know which game the user is watching (for contextual ranking)
- Trading needs game context (which game, which team) when user initiates a trade
- Team Page may link back to this game page if a live game is in progress

---

## 7. Risks

**Specific risks:**

- SR data delay (30-40 seconds from real-world events) means users watching live TV see events before the app -- creates information asymmetry between users with and without broadcast access
- High-traffic moments (multiple touchdowns across games simultaneously) could cause T0 price feed latency or SR widget lag
- Mobile screen real estate is tight -- if too many elements compete for space, the experience becomes cluttered and unusable
- Chart annotations at mobile scale may be unreadable if too many volatility moments cluster in a short time window

**Controls to build into the journeys:**

- Data freshness indicator -- if data is delayed beyond acceptable threshold, show a "delayed" label so users don't trade on stale information
- Annotation density management -- if multiple events happen within seconds, group or stack annotations rather than overlapping
- Graceful degradation -- if SR feed drops, show last known state with timestamp; if T0 drops, disable buy/sell and show "trading paused"
- Performance budget -- page must remain responsive even with all real-time elements updating simultaneously

---

## 8. Priority

**Must-have at launch?** Yes -- this is the core screen. The entire product premise converges here.

**Sequencing rationale:** Build this first among the sub-components. It's the primary engagement surface, the most complex technically (multiple real-time data sources converging), and it drives design decisions for every other page. If this works, the rest follows. If this doesn't work, the product doesn't work.

---

## Sub-Sub-Components

Leaf node -- no further decomposition needed. The page has multiple elements (match tracker, chart, market data, trading widget, leaderboard widget) but they all share state and render on the same screen.

---

## Open Questions

1. How much order book depth to show on mobile? Full book or just top of book (best bid/best offer)?
2. Layout: how do match tracker, chart, stats, and trading widget coexist on a single mobile screen? Scrollable sections, tabs, or collapsible panels?
3. Does the match tracker go full-screen on landscape rotation?
4. The SR data delay is 30-40 seconds from real-world events. Is that acceptable, or do we need a visible disclaimer?
5. Should the page show a count of how many other users are viewing this game? (social proof / activity indicator)
