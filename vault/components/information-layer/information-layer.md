# InPlay Trading Challenge -- Information Layer

> **Vision:** [[vision]]
> **Date:** 2026-05-09
> **Status:** Collecting
> **Owner:** George Westbrook (engineering) / Brett StClair (client-facing)
> **Sources:** _[[08-05-2026-component-1-simulation-app]], [[meetings/06-05-2026-vision-workshop]]_

---

## 1. What Does This Component Do?

**Functional purpose:**

The Information Layer is the main stage of the InPlay app -- the data and intelligence layer where users discover games, consume sports and market data, and make trading decisions. It covers the "Discover -> See -> Understand -> Decide" portion of the user journey. Everything a trader needs to assess the market and form a view before executing a trade lives here.

The component spans multiple interconnected pages. Users land on a discovery homepage where they browse today's slate of games, search for specific teams, and see featured matchups. From there they can drill into a game day overview showing all live and upcoming games, or click directly into a single game page where sports data and market data converge -- a Sport Radar live match tracker, an annotated price chart mapping game events to price movements, real-time stats, and market data (bid/offer, order book depth). Team pages provide historical context: season performance, head-to-head matchup data, and stock price history over time. A leaderboard system tracks competition across three verticals (best P&L, best risk-adjusted return, comeback trader) and four time horizons (daily, weekly, monthly, full event), showing users where they rank and what they need to do to reach payout positions.

The component pulls from three data sources: Sport Radar (sports events, stats, live match tracker, news), T0 ATS (prices, order book, trade events), and InPlay's own data store (leaderboard rankings, cross-correlated volatility data, user preferences). The cross-correlation layer -- game events mapped to price movements -- is InPlay's proprietary IP. A research tab is planned but not yet scoped; it will be free during the simulation challenge and paywalled in production.

The Information Layer also hosts shared elements that appear across multiple pages: a news feed (AP-style editorial from Sport Radar), large block trade alerts, leaderboard position widgets, and market data snippets. Advertising surfaces within this component as a cross-cutting concern -- volatility moment animations, sponsored pages, and game-adjacent ad placements all live here but are governed by the advertising strategy, not this component.

```
Information Layer
├── Discovery / Home
│   ├── Game ticker (horizontal scroll)
│   ├── Search (type-ahead, ~163 teams)
│   ├── Featured/marquee games
│   └── Per-game cards (minimal info)
├── Game Day Overview
│   └── All live/upcoming games today
├── Single Game Page
│   ├── Sport Radar live match tracker (embed)
│   ├── Annotated price chart (SR events x T0 prices)
│   ├── Real-time game stats
│   ├── Market data (bid/offer, order book depth)
│   ├── Trading widget (owned by Trading component)
│   └── Leaderboard widget (mini)
├── Team Page
│   ├── Historical performance (10-15 years)
│   ├── Season stats / head-to-head matchups
│   ├── Stock price history
│   └── Live game data (when applicable)
├── Research Tab (undefined -- needs dedicated session)
└── Leaderboard (full view)
    ├── Three verticals (P&L, risk-adjusted, comeback)
    ├── Four time horizons (daily, weekly, monthly, event)
    ├── Proximity alerts ("you're X places from cashing")
    └── Special event days (Thanksgiving, Christmas)
```

**Personas:**

| Persona | How they use this component | What they need from it |
|---------|---------------------------|----------------------|
| Young Aspiring Trader (18-25) | Discovers games, learns by watching price movements correlate with game events. Relies on the annotated chart to understand _why_ prices move. Uses leaderboard to track progress toward prizes | Educational clarity -- the information layer is the training ground. Simple, visual explanations of market dynamics. Leaderboard proximity ("you're X places from cashing") |
| Sports-Passionate Casual (25-45) | Brings deep sports knowledge, uses game data and team stats to inform trades. Game day page is where they spend most time during live games. Watches match tracker when broadcast isn't available | Sports data richness -- team matchups, historical performance, live play-by-play. Needs to feel their sports knowledge gives them an edge. Quick navigation to games they care about |
| Experienced Trader (40-55) | Wants Bloomberg-style depth -- order book, bid/offer, price charts with annotations. Uses research tab heavily. Evaluates risk-adjusted positions | Sophisticated market data display, order book depth, the annotated volatility chart, research tools. This persona explicitly wants "Bloomberg Terminal-style data experience" |

---

## 2. What Needs to Happen?

**Functional requirements:**

- User can browse all upcoming and live games from the discovery homepage
- User can search for teams across ~163 teams (32 NFL + ~131 NCAA) with type-ahead (e.g., type "CHI" -> Chicago Bears; handle overlaps like Buffalo Bills vs. Buffalo college)
- User can see a horizontal scrolling ticker of live/upcoming games at the top of the screen
- User can see minimum info per game card: game time, win probability, stock price direction (up/down indicator)
- User can click into a specific game to view the single game page
- User can view Sport Radar live match tracker (embedded widget, not custom build) with pre-game, live, and post-game states
- User can view a price chart annotated with game events (touchdowns, turnovers, injuries mapped to price movements)
- User can view real-time game stats and play-by-play data
- User can view market data: current price, bid/offer, order book depth
- User can view team pages with historical performance data (10-15 years from SR), season stats, head-to-head matchups
- User can view leaderboard rankings across three verticals: best P&L, best risk-adjusted return, comeback trader of the day
- User can view leaderboard across four time horizons: daily, weekly, monthly, full event
- User can see their current ranking relative to the field and what they need to do to reach a payout position (gap to cashing)
- User receives proximity alerts when approaching or falling away from payout positions
- User can view a news feed with AP-style editorial content from Sport Radar (player news, injuries, team news)
- User can view large block trade alerts (anonymous: "a large block traded at X price at Y time")
- Visual indicator for "last game of the day" (critical for daily prize engagement)
- Featured/marquee games highlighted (top 5 college, top 5 NFL per week)
- Research tab available (scope undefined -- flagged for dedicated session)
- Light/dark mode toggle (dark preferred for trading screens, light for general browsing)

**Business rules and constraints:**

- Market data must update in real time during live games (SR pushes every 1-2 seconds)
- Leaderboard daily calculations: games count based on start time within the 24-hour period, not finish time (e.g., late Hawaii game starting at 10:30pm counts for that day even if it finishes past midnight)
- Language must use "earn" not "win" throughout -- regulatory requirement to position as skill-based competition, not chance-based
- Research tab free during simulation challenge, subscription-gated in production

**Edge cases and error states:**

- What happens when Sport Radar data feed goes down during a live game?
- What happens when T0 price feed is delayed or unavailable?
- Games spanning midnight -- how does the leaderboard handle the cutoff? (Edwin and Troy agreed to resolve offline; decision pending)
- User searching for a team that exists in both NFL and NCAA (e.g., Buffalo) -- disambiguation needed

---

## 3. How Should It Look and Feel?

**Design direction:**

Data-rich but not overwhelming. The core tension: Edwin wants Bloomberg-level depth, but mobile-first means progressive disclosure. Minimal info on discovery, richer as you drill in. Dark mode preferred for trading/game screens, light mode for general browsing, with a toggle for user preference. At most light/dark for MVP -- no further theme customisation.

**Reference products:**

- **Poly Market** -- clean iconography, odds/probability displayed inline on game cards, swipe-up receipt page. Edwin: "much better app" than Hard Rock. Take: clean data density, probability display, share/receipt mechanics
- **FanDuel / DraftKings** -- leaderboard with proximity notifications ("you're X places from cashing") in daily fantasy tournaments. Cody: "if you ever want to see a really good leaderboard, look at DraftKings daily fantasy tournaments." Take: leaderboard engagement mechanics. Avoid: information overload on desktop
- **Fanatics** -- sub-navigation pattern for information categories, swipeable sections. Take: mid-screen categorical navigation for information-rich pages
- **Hard Rock Bet** -- Edwin: "janky as f***", childish icons, 4 clicks to reach a betting page, internal ads taking up screen real estate. Avoid: everything about this UX
- **Bloomberg / CNBC ticker** -- simple green arrow up / red arrow down with percentage change. Take: quick visual price direction without requiring dollar values on discovery cards

**Key UX principles:**

- Minimum viable information per context -- 3 items max on discovery game cards, progressively more detail as user drills deeper
- Navigation must be fast -- max 2 taps to reach any game's trading page from discovery
- P&L and leaderboard position must be visible without navigating away from the game page
- Match tracker and trading widget coexist on the same screen during live games
- Ads must feel "supportive" of the experience, not interruptive -- Edwin's word. Volatility moment animations should signal "something is happening," not "here's an ad"
- Sport Radar widgets are HTML5 responsive across mobile and tablet
- Bottom navigation bar as primary navigation pattern (5-point, similar to standard mobile apps)
- Search must return results within 1-2 keystrokes -- users won't tolerate navigating through 163 teams manually

---

## 4. How Are We Going to Solve It?

| Capability | Build/Buy/Access | Provider / Approach | Rationale |
|-----------|-----------------|-------------------|-----------|
| Live match tracker | Access | Sport Radar embedded widget (hosted solution) | Already licensed. Includes pre/post/live states, HTML5 responsive across mobile and tablet. Custom build would take months for the same result. SR client setup team handles colours, fonts, branding |
| Real-time sports data (play-by-play, stats, historical) | Access | Sport Radar APIs (push + REST) | Licensed. 10-15 years historical depth, real-time push every 1-2 seconds, covers NFL + NCAA. Cody: "any data point that lives in a sports ecosystem, we will have access to it" |
| Win probabilities | Access | Sport Radar | Live probability calculations during games, included in existing licensing |
| Team logos in match tracker | Access | Sport Radar widget (toggle switch) | Included via Associated Press visualisation loophole at no extra cost. Can be toggled on/off. Risk of league pushback. **Decision pending:** use logos for authenticity vs. sell that ad space to sponsors. To be raised in SR client setup call |
| Market data (prices, order book, bid/offer) | Access | T0 ATS | T0 provides the trading engine and all price/order data. Information Layer consumes and displays; does not own |
| Annotated price chart (game events x price movements) | Build | InPlay proprietary | Cross-correlation of SR game events with T0 price data to produce annotated charts showing _why_ prices moved. This is InPlay's IP -- no third party provides this. Requires a data store for the cross-correlated dataset ("mem store" per Brett) |
| News feed (editorial) | Access | Sport Radar AP-style newswire | Player news, injuries, free agent signings, team news. Included in SR licensing |
| Leaderboard engine (rankings, calculations, proximity) | Build | InPlay internal | Three verticals, four time horizons, proximity calculations, prize distribution rules, special event day logic -- all custom business logic |
| Search (team lookup with type-ahead) | Build | InPlay internal | Type-ahead across ~163 teams with disambiguation for overlapping names |
| Light/dark mode | Build | InPlay internal | Standard mobile app theming. Two options max for MVP |
| Eye tracking / heat maps | TBD | TBD | Discussed for ~October post-launch. Would provide data to prove ad placement value to advertisers. Feasibility, provider, and privacy implications not yet assessed |

---

## 5. What Data Does It Need?

| Data | Direction | Source / Destination | Notes |
|------|-----------|---------------------|-------|
| Live play-by-play events | In | Sport Radar (push API) | Real-time, every 1-2 seconds during live games. Touchdowns, turnovers, injuries, drives, key plays |
| Historical team/player stats | In | Sport Radar (REST API) | 10-15 years depth. Matchup data, season performance, player stats |
| Live match tracker widget | In | Sport Radar (embedded HTML5) | Hosted solution, not raw data. Pre/post/live states. Customisable via SR client setup team |
| Win probabilities | In | Sport Radar | Live probability calculations, updated in real time during games |
| Game schedule / fixtures | In | Sport Radar | Which games are on, when, where. Drives discovery page and game day overview |
| AP-style news content | In | Sport Radar newswire | Player news, injuries, signings, team news |
| Current prices (bid/offer/last) | In | T0 ATS | Real-time during live games |
| Order book depth | In | T0 ATS | Number of orders at each price level |
| Large block trade events | In | T0 ATS / Trading component | Anonymous alerts generated when large trades execute |
| User positions / P&L summary | In | Trading component | Displayed on game page and discovery. Owned by Trading, consumed here |
| Cross-correlated volatility data | Stored | InPlay internal | SR game events mapped to T0 price movements. InPlay's proprietary dataset. Powers the annotated price chart. Requires precise timestamping between both data sources |
| Leaderboard rankings | Stored | InPlay internal | Calculated from Trading component P&L data across three verticals and four time horizons |
| User favourites / followed teams | Stored | InPlay internal | Personalisation for discovery page ordering and featured content |

---

## 6. Who Can Access It?

| Persona / Role | Access level | Notes |
|---------------|-------------|-------|
| All registered users (post-onboarding) | Full access | Information Layer available to all users after completing signup and KYC |
| Unregistered / pre-KYC users | TBD | Open question: can users browse game data before completing onboarding? Could aid conversion but adds complexity |
| Research tab users (production only) | Gated | Free during simulation challenge. Subscription-gated in production -- users get "conditioned" to rely on it, then pay when transitioning to real trading |

---

## 7. How Do We Know It's Working?

- [ ] Users spend >1 hour per session on game days (Edwin's baseline: "at least an hour every time someone logs in")
- [ ] Users navigate from discovery to single game page within 2 taps
- [ ] Users who view the annotated price chart execute trades at a higher rate than those who don't
- [ ] Leaderboard proximity alerts drive return visits (users who receive "you're X from cashing" re-engage within the session)
- [ ] Match tracker engagement: users who can't watch the broadcast use the match tracker as primary game-following tool
- [ ] Research tab usage during simulation predicts conversion to paid in production
- [ ] Discovery page surfaces relevant games -- users click into games from discovery rather than using search as primary navigation

---

## 8. Dependencies

**What this component needs:**

| Depends on | What we need | Blocking? |
|-----------|-------------|----------|
| Sport Radar | Data feeds (push + REST), live match tracker widget, news feed, historical data, win probabilities | Yes -- no SR, no information layer |
| T0 ATS | Real-time prices, order book data, trade event stream (for block alerts) | Yes -- no T0, no market data |
| Trading component | User P&L and position data (for display on game pages and leaderboard calculations) | No -- can mock with simulated data during build |
| Customer Onboarding | Authenticated user identity | Yes -- need to know who the user is |
| Sport Radar client setup call | Widget customisation (colours, fonts, logo toggle decision) | No -- can proceed with defaults, customise later |

**What other components need from this one:**

- **Trading component** needs game context (which game is the user viewing, which team) to populate the order entry widget
- **Referral component** may surface share functionality on discovery and game pages
- **Third Space component** may pull game page context for shared trades and discussion
- **Advertising (cross-cutting)** needs page context, game state, and volatility moment triggers to serve the right ads at the right time
- **Personal Dashboard (cross-cutting)** pulls leaderboard position, active game data, and news

---

## 9. Priority

**Must-have at launch?** Yes -- this is the core experience. Without the Information Layer, users have no context for trading decisions. The product premise is that sports data and market data converge to create a new trading experience; this component is where that convergence happens.

**Sequencing rationale:**

Brett identified this as the right component to build first: "We can figure out the brand experience, the user experience, the colors, the mechanisms. We can pull out a lot of design components, design systems. There's enough spread across elements... it's the core central model." Building this first exposes the Sport Radar and T0 integration challenges early, establishes the design system that cascades into all other modules, and validates the core user experience before building the surrounding components.

---

## 10. Risks

**Abuse vectors:**

- Scraping of SR data or InPlay's proprietary cross-correlated dataset by competitors or third parties
- Bots using the information layer programmatically to feed automated trading strategies, gaining unfair advantage over manual traders

**Data risks:**

- SR data has 30-40 second delay from real-world events -- users watching live TV see events before the app reflects them, creating information asymmetry between users with and without broadcast access
- T0 price data latency during high-volume moments (e.g., touchdowns affecting multiple games simultaneously could spike load)
- Cross-correlation accuracy -- mapping the right SR event to the right price movement requires precise timestamping between two independent data sources
- SR or T0 feed outages during live games -- partial data is worse than no data if users make decisions on stale information

**Compliance:**

- Team logos in match tracker may trigger IP issues with leagues despite SR's Associated Press loophole -- pending legal review and SR client setup call
- All language must maintain "skill-based competition" framing, not gambling framing ("earn" not "win")
- If eye tracking / heat maps are implemented, biometric data privacy laws in certain US states may apply

**Controls needed:**

- Data freshness indicators on UI -- if data is delayed, users must see a "delayed" label so they don't trade on stale information
- Rate limiting on search and API calls to prevent scraping
- Graceful degradation if SR or T0 feeds go down during a live game (show last known state with timestamp and "delayed" indicator)
- Bot detection on information consumption patterns (e.g., programmatic polling of price data at inhuman speeds)

---

## Sub-Components

| Sub-Component | Overview | Status | Link |
|--------------|----------|--------|------|
| Discovery / Home | Entry point -- game ticker, search, featured games, per-game cards with minimal info (3 items: game time, win probability, price direction) | Collecting | [[sub-components/discovery-home/discovery-home]] |
| Game Day Overview | Today's full slate of games -- all live/upcoming, scores, price movements, mini P&L for active positions | Collecting | [[sub-components/game-day-overview/game-day-overview]] |
| Single Game Page | Deep view of one matchup -- match tracker, annotated chart, real-time stats, market data (bid/offer, order book), embedded trading widget, leaderboard widget | Collecting | [[sub-components/single-game-page/single-game-page]] |
| Team Page | Persistent team view -- historical data (10-15 years), season stats, head-to-head matchups, stock price history. Enriched with live game data when applicable | Collecting | [[sub-components/team-page/team-page]] |
| Research Tab | Historical analysis and volatility research tools. Free in simulation, paywalled in production. Hosts the **Research AI Chat** sub-component of [[components/third-space/third-space\|Third Space]] (NLP queries on Sport Radar stats, Statmuse-style). **Otherwise still undefined -- needs dedicated session** | Collecting | [[sub-components/research-tab/research-tab]] |
| Leaderboard | Full rankings view across three verticals and four time horizons. Proximity alerts ("you need $X to reach payout position"). Widgets embedded across other pages. Special event days (Thanksgiving, Christmas) with enhanced prizes | Collecting | [[sub-components/leaderboard/leaderboard]] |

---

## Gaps and Questions for Next Call

### Gaps

- **Research Tab:** No definition beyond "historical analysis, free in sim, paid in production" plus confirmation that the Research AI Chat (from [[components/third-space/third-space\|Third Space]]) lives here. Otherwise needs a dedicated session to scope what's actually in it
- **Game-page naming:** the matchup / game-day landing page (two teams playing) lacks a settled name. Used variously as "game day page", "matchup page", "single game page", "game information page". Cody: _"I didn't to be honest, I didn't know we named it anything specific up to this point. I would vote, you know, matchup page, game day page, game information page. I think we can still dial that in."_ Decision needed before terminology bleeds further across documentation
- **News feed placement:** Vision doc specifies AP-style newswire from SR but nobody discussed where it appears in the UI or how prominent it is
- **Large block trade alerts:** Vision doc calls these out but the call didn't discuss format, frequency, or placement
- **Market data display (order book depth, bid/offer):** Not discussed on the call at all -- how much Bloomberg-style depth do we show on mobile?
- **Personalisation:** User favourites and followed teams mentioned in passing but not scoped
- **Game Day Overview vs. Discovery:** Are these the same page or separate? The boundary is unclear
- **Sport Radar logo toggle decision:** Logos for authenticity vs. selling that ad space. Needs input from SR client setup call and advertising strategy

### Questions for Edwin / Cody / Team

1. What specifically goes in the Research Tab? Can you walk through what a user would see and do?
2. How prominent should the news feed be? Is it a dedicated section, a sidebar, or notifications?
3. For the order book display -- how much depth do you want to show? Full order book or just top of book (best bid/best offer)?
4. Do users need to be able to customise their discovery page (pin favourite teams, hide sports they don't follow)?
5. The SR data delay is 30-40 seconds from real-world events. Is that acceptable, or do we need to surface a "data may be delayed" disclaimer?
6. For the risk-adjusted return leaderboard -- how do we communicate this to non-trader personas in a way they understand?
7. Should the game day overview and discovery homepage be the same page or separate views?
