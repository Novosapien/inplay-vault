# InPlay Trading Challenge -- Trading

> **Vision:** [[vision]]
> **Date:** 2026-05-11
> **Status:** Collecting
> **Owner:** George Westbrook (engineering) / Brett StClair (client-facing)
> **Sources:** _[[meetings/06-05-2026-vision-workshop]], [[meetings/08-05-2026-compoent-1]], [[meetings/11-06-2026-trading-component]]_

---

## 1. What Does This Component Do?

**Functional purpose:**

The Trading component is the execution engine of the InPlay app -- where users act on the decisions they've formed in the Information Layer. It covers the "Act -> Confirm -> Review" portion of the user journey. Users can buy and sell team stocks via limit orders routed through tZERO's ATS, manage open orders, view positions, and track P&L.

The component is designed to be accessible from anywhere in the app, not confined to a single page. A persistent trade capability follows the user across screens -- team pages, game day pages, leaderboard, and beyond. The core design principle is context-aware trading: the system infers which team(s) the user is most likely to want to trade based on where they are in the app, while always providing search as a fallback.

Trading must be fast. The target is 3 clicks or fewer from any page to a submitted order. A modal/overlay approach keeps users in context rather than navigating to a separate page.

**Personas:**

| Persona | How they use this component | What they need from it |
|---------|---------------------------|----------------------|
| Young Aspiring Trader (18-25) | First-time trading experience. Learning by doing -- small positions, frequent trades, driven by leaderboard competition | Simple, intuitive order entry. No jargon. Education module links for order types. Low friction to first trade |
| Sports-Passionate Casual (25-45) | Trades based on sports knowledge -- reacts to game events, injury news, matchup data. Trades during live games | Speed. Persistent buy/sell so they can react instantly to what they're seeing on the field. Context-aware defaults so the right team is pre-selected |
| Experienced Trader (40-55) | Wants limit order control, position management, P&L tracking. Comfortable with trading mechanics | Order management depth -- open orders, fills, cancel/replace. Portfolio view with unrealised P&L. Familiar trading UX patterns |

---

## 2. What Needs to Happen?

**Functional requirements:**

_Order Entry:_

- User can place limit orders (buy or sell) for any team stock
- User can specify quantity and price on every order
- No confirmation dialog ("are you sure?") -- click and execute (Edwin: "we don't want that... we want to be able to just click and go")
- Buy button always on left, sell button always on right (industry convention, Edwin/Troy confirmed)
- Order entry via modal/overlay that appears on top of the current page, not a separate page navigation

_Trade Access (persistent across app):_

- User can access trade functionality from any page in the app
- On a team page: buy/sell defaults to that team (2 clicks to submit)
- On a game day page: buy/sell shows both teams in the matchup (3 clicks max)
- On other pages (leaderboard, etc.): a trade button opens the trade modal, user selects team (3 clicks max)
- User can search for any team from within the trade modal if the defaulted team isn't what they want
- Persistent buy/sell buttons can be collapsed/minimised if they're in the way, and re-expanded
- Swipe left/right to switch between teams -- proposed by Troy, positively received, but needs further UX exploration. Key questions: how does swiping interact with other phone gestures? What's the visual indicator that swiping is available? How many teams deep can you swipe? This needs wireframing and testing before committing

_Fill Notifications:_

- User receives a push notification when a limit order fills, regardless of which page they're on (Edwin: "we need something within the app that says you got filled")
- Notification enables immediate reaction -- e.g., filled on buy at 3, immediately place a sell at 7

_Team Search:_

- User can search for any team by name or symbol from within the trade modal
- Autocomplete/autocorrect on search (Edwin: "everyone's a d****** with spelling today")
- Symbol convention exists -- Cody/Kevin have created this (e.g., IGBI for InPlay Green Bay Inc.)

_Portfolio & Position Management (from vision -- not discussed in detail this session):_

- User can view current positions across all teams
- User can view P&L (daily/weekly/monthly)
- User can view trade history
- User can view and cancel open orders
- Trading wallet starts at 100K InPlay dollars
- Referral wallet reload when trading wallet drops below 25K

**Business rules and constraints:**

- Only limit orders for MVP -- tZERO does not support native market orders (Troy confirmed)
- Synthetic market order (auto-populate best bid/offer with tolerance band) is a post-MVP feature -- George proposed the mechanism, Troy confirmed this is how equities brokers do it, but George flagged it as a heavy lift for MVP
- Only onboarded users (completed signup + KYC) can trade (Cody confirmed: "onboarded and signed up")
- All language must use "earn" not "win" throughout -- regulatory requirement to position as skill-based competition, not chance-based
- Buy always left, sell always right -- non-negotiable convention

**Edge cases and error states:**

- Fat finger protection: buy/sell buttons need "their own kind of like private space that's very distinct from every other button" (Edwin) -- spatial separation to prevent accidental trades
- What happens when tZERO rejects an order? (Not discussed -- gap)
- What happens during a trading halt on a specific team stock? (Not discussed -- gap, though architecture docs cover the DFA)
- User places a limit order far from the current price -- do we warn them? (Not discussed -- gap)
- User tries to trade when their wallet balance is insufficient -- what's the UX? (Not discussed -- gap)

---

## 3. How Should It Look and Feel?

**Design direction:**

Speed and simplicity. The trading UX must feel instant -- no friction, no unnecessary screens, no confirmation dialogs. The persistent trade capability means the user is always one or two taps from executing. The modal/overlay approach keeps them in context rather than pulling them out of whatever they were doing.

Buy/sell buttons need clear visual separation from all other UI elements to prevent fat-finger errors. They should have "their own private space" (Edwin) -- distinct enough that accidental taps are unlikely, but accessible enough that intentional taps are effortless.

Bottom of screen is preferred placement for trade buttons -- optimised for thumb reach when holding a phone (George: "if I've got to click something at the top of the screen sometimes I might fumble it, whereas if it's just right by the bottom, it's quick... bam"). Configurable top/bottom placement discussed but deferred -- adds complexity (storing per-user settings, dynamically changing layout) and not viable for MVP.

**Colour conventions:**

- Blue for buy, red for sell (Troy/Edwin confirmed -- same as PT convention)
- Hover/touch glow effect on buttons to signal "you're about to act" -- Edwin suggested, but flagged as potentially v2

**Reference products discussed in this session:**

- **MetaTrader 5** (Cody demonstrated live) -- swipe up from chart to reveal trade interface. Tabs across bottom: buy now, buy limit, sell limit, buy stop, sell stop. Click, type quantity, hit trade. "Five seconds if that" to execute. Sliding quantity selector at top. Best bid/offer prices displayed above the buy/sell buttons. Troy: "that's our version of a market order because then you can just buy sell buy sell as you see the prices fluctuating"
- **Trading 212** (Max/Brett raised) -- single "Trade" button instead of separate buy/sell. Click trade, then options expand. Reduces persistent screen clutter to one button. Edwin: "I don't hate it... it's one more layer." Cody pushed back: "that's just another click that I don't necessarily like"
- **Poly Market** (Edwin, negative reference for trade flow) -- "I got to click three times before I can actually even start inputting the amount... it's really irritating"

**Key UX principles (from this session):**

- 3 clicks or fewer from any page to a submitted order -- hard target
- Context-aware defaults reduce clicks: if the system knows which team is relevant, don't make the user tell it
- No "are you sure?" confirmation dialogs -- trade executes on click
- Don't interrupt the trade flow with advertising (Max: "when you're trading, let the trade flow happen")
- Persistent trade buttons should be collapsible for users who find them intrusive while browsing

---

## 4. How Are We Going to Solve It?

| Capability | Build/Buy/Access | Provider / Approach | Rationale |
|-----------|-----------------|-------------------|-----------|
| Order execution (limit orders) | Access | tZERO ATS via FIX 4.2 protocol | tZERO is the exchange. All orders routed through their Order Entry FIX session. They handle matching, fills, and execution reports |
| Market data for trade modal (best bid/offer) | Access | tZERO ATS via FIX Market Data feed | Live bid/ask displayed above buy/sell buttons so users can see the current price before committing. Troy: displaying best bid/offer above buttons is "our version of a market order" |
| Synthetic market orders (post-MVP) | Build | InPlay internal | Auto-populate limit price at best bid/offer with a tolerance band. George proposed, Troy confirmed this is standard broker practice. tZERO doesn't have native market orders -- brokers build this in their UI layer |
| Order management (cancel/replace) | Access | tZERO ATS via FIX 4.2 | Cancel via OrderCancelRequest (MsgType=F), replace via OrderCancelReplace (MsgType=G). tZERO handles atomically |
| Fill notifications (push) | Build | InPlay internal | Real-time push notification when a limit order fills. Delivered via WebSocket (Centrifugo) while user is in-app. Push notification if user is outside app (mechanism TBD) |
| Trade modal / overlay UI | Build | InPlay internal | Context-aware modal with team defaulting, search, quantity/price input, execute button. Core UX of the component |
| Persistent buy/sell buttons | Build | InPlay internal | Floating UI element across all pages with collapse/expand. Determines which teams to default based on page context |
| Wallet management | Build | InPlay internal | Trading wallet (100K cap), referral wallet reload (below 25K trigger). Balance checks before order submission |
| Position & P&L tracking | Build + Access | InPlay internal + tZERO | tZERO provides position fields on execution reports (PosSIZ, PosCOST, PosRpnl, PosUpnl). InPlay stores and displays |
| Team symbology / search | Build | InPlay internal | Symbol convention created by Cody/Kevin. Search with autocomplete across all teams |
| FIX Gateway (fan-out layer) | Build | InPlay internal | Single FIX session multiplexed across all users. Translates between FIX protocol and internal message bus (NATS). Handles session management, dedup, recovery |

---

## 5. What Data Does It Need?

| Data | Direction | Source / Destination | Notes |
|------|-----------|---------------------|-------|
| Best bid/offer (live) | In | tZERO FIX Market Data feed | Displayed above buy/sell buttons in the trade modal. Updates in real time. Troy: showing best bid/offer is how users make quick trading decisions without needing market orders |
| Order book depth | In | tZERO IOI + FIX Market Data feeds | For users who want to see beyond top-of-book before placing an order. Depth of display TBD |
| Order submission | Out | tZERO via FIX 4.2 Order Entry | NewOrderSingle (MsgType=D). Limit orders only (OrdType=2). ClOrdID max 20 chars, no leading zeroes |
| Execution reports | In | tZERO via FIX 4.2 Order Entry | Covers the full order lifecycle: acceptance, fills (partial/full), cancellations, replacements, rejects, busts, corrections, and end-of-day expiry. See `architecture/integrations/t0.md` for full ExecType mapping. Proposed -- pending tZERO integration sessions to confirm |
| Cancel/replace requests | Out | tZERO via FIX 4.2 Order Entry | OrderCancelRequest (MsgType=F) and OrderCancelReplace (MsgType=G). Proposed -- pending tZERO integration sessions to confirm |
| Position data (size, cost, P&L) | In | tZERO execution reports | PosSIZ (9383), PosCOST (9384), PosRpnl (9385), PosUpnl (9389) -- recalculated by tZERO on every fill, bust, correction. Proposed -- pending tZERO integration sessions to confirm |
| Wallet balances | Stored | InPlay internal (PostgreSQL + Redis cache) | Trading wallet (100K cap) and referral wallet. Redis for fast reads on order validation, PostgreSQL as source of truth |
| Order history | Stored | InPlay internal (PostgreSQL) | All orders and their lifecycle events. Powers trade history view |
| Team symbology | Stored | InPlay internal | Symbol-to-team mapping. Created by Cody/Kevin. Powers search and display |
| Page context (which team/game user is viewing) | In | Information Layer component | Used to determine which team(s) to default in the trade modal. Team page -> that team. Game day page -> both teams in matchup |
| Fill notifications | Out | InPlay -> User (via Centrifugo WebSocket / push notification) | Real-time alert when a limit order fills. Edwin: critical for enabling users to react and place follow-up orders immediately |

**Open data question from this session:**

George flagged the need to understand what data tZERO stores vs what InPlay needs to store independently. Specifically: what do their tables look like? Can we query historical order/position data via their REST API, or do we need to persist everything ourselves? This is blocking final architecture decisions. Troy offered to set up collaboration sessions with tZERO to resolve.

---

## 6. Who Can Access It?

| Persona / Role | Access level | Notes |
|---------------|-------------|-------|
| Onboarded users (post-signup + KYC) | Full access | Cody confirmed: "onboarded and signed up" -- only users who have completed the full onboarding flow can trade |
| Unregistered / pre-KYC users | No access | Cannot trade. Trading requires a funded wallet (100K InPlay dollars credited on signup completion) |
| Users with zero wallet balance | Restricted | Can view the trade UI but cannot submit orders. If trading wallet drops below 25K, referral wallet reload is triggered (from vision session -- not discussed this call) |

---

## 7. How Do We Know It's Working?

- [ ] Users can execute a trade in 3 clicks or fewer from any page in the app
- [ ] Trade execution from team page completes in 2 clicks
- [ ] Time from tapping "execute" to seeing "order acknowledged" is under 50ms (from architecture target)
- [ ] Fill notifications arrive in real time -- users place follow-up orders within the same session after receiving a fill alert
- [ ] Context-aware defaults are correct -- when a user opens trade from a team page, the right team is pre-selected (measure how often users override the default via search)
- [ ] Users trade from multiple pages, not just a dedicated trade page (validates the persistent buy/sell approach)
- [ ] Fat finger rate is low -- accidental trades that are immediately cancelled stay below a threshold (TBD)
- [ ] Users who receive fill notifications place follow-up orders at a higher rate than those who don't

---

## 8. Dependencies

**What this component needs:**

| Depends on | What we need | Blocking? |
|-----------|-------------|----------|
| tZERO ATS | Order execution via FIX 4.2 Order Entry session, market data (best bid/offer) via FIX Market Data feed, REST API for non-streaming data (account info, historical queries). FIX version discrepancy (PDFs say 4.2, online docs say 4.4) needs resolving | Yes -- no tZERO, no trading |
| tZERO collaboration sessions | Clarity on: what data tZERO stores vs what InPlay stores, table structures, REST API endpoints, FIX session limits, FIX version confirmation. Troy offered to set up -- George to come back with questions after more architecture research | Yes -- blocking final architecture decisions |
| Information Layer component | Page context: which team/game the user is viewing, so trading can set context-aware defaults | No -- can default to search-only without context |
| Customer Onboarding | Authenticated, KYC'd user identity and funded trading wallet (100K InPlay dollars) | Yes -- must be onboarded before trading |
| Team symbology | Symbol-to-team mapping for search and order submission. Cody/Kevin have created the convention | No -- can use team names as placeholder |
| Push notification infrastructure | Delivery mechanism for fill notifications when user is elsewhere in the app or outside the app entirely | No -- core trading works without it, but the experience Edwin described depends on it |

**What other components need from this one:**

- **Information Layer** needs current price, position data, and P&L to display on game pages, team pages, and leaderboard
- **Leaderboard** (within Information Layer) needs trading P&L to calculate rankings across three verticals and four time horizons
- **Referral component** needs trading wallet balance to trigger the reload mechanism (below 25K)
- **Advertising (cross-cutting)** needs fill events and trading moments to trigger brand-sponsored notifications (e.g., "You cashed -- congratulations by Bank of America")
- **Education component** needs to link to order type explanations -- Edwin assigned Kevin to build education content covering how limit orders work

---

## 9. Priority

**Must-have at launch?** Yes -- this is the core product action. Without trading, the app is a sports data viewer. Edwin was explicit: "trading is number one, advertising is number two, user experience is number three."

**Sequencing rationale:**

Max/Brett identified trading as carrying the biggest risk of all components: "we think it's really important to get a head start on the trade module... that's the one with the biggest risk as far as we can see." The risk is driven by the tZERO integration -- FIX 4.2 protocol is specialised compared to standard REST APIs, VMs are likely needed instead of containers for low-latency requirements, and the data model dependency on tZERO is still unresolved.

**MVP scope (from this session):**

- Limit orders only
- Persistent trade access across all pages
- Context-aware team defaults (team page, game day page)
- 3 clicks or fewer to execute
- Fill notifications
- Basic position view and P&L

**Post-MVP (explicitly deferred):**

- Synthetic market orders (George's tolerance-band approach -- "heavy lift for MVP")
- Configurable button placement top/bottom (Troy raised, George flagged complexity)
- Swipe left/right team switching (needs UX exploration before committing)
- Hover/touch glow effects on buy/sell buttons (Edwin: "can be version two")

---

## 10. Risks

**Technical risks:**

- tZERO FIX version discrepancy -- PDFs specify FIX 4.2, online docs reference FIX 4.4. Must confirm before implementation. Wrong version means the gateway won't connect
- tZERO data model unknown -- George: "we think we're 80% there... it's just some of maybe this is what this table looks like, this is what that table looks like." Until resolved, we don't know what InPlay needs to store independently vs what we can query from tZERO
- VM requirement for trading infrastructure -- low-latency trading needs VMs, not containers. Max: VMs at ~$15K/month for 1000 concurrent users vs couple hundred on containers. Cost management is critical
- Single FIX session multiplexed across all users -- if the FIX gateway goes down, all trading stops. Architecture needs resilience here

**UX risks:**

- Fat finger trades -- Edwin flagged this explicitly. Buy/sell buttons need clear spatial separation from all other UI elements. No confirmation dialog means an accidental tap is a real trade
- Persistent trade buttons could annoy users who aren't in a trading mindset -- collapse/expand mitigates but needs testing
- 3-click target may not hold on all page types -- game day page with two teams plus search could push beyond 3 in edge cases
- Limit orders only may confuse users who expect to just tap "buy" and get filled -- education module needs to clearly explain that you must specify a price

**Infrastructure risks:**

- Peak load at game moments (touchdowns, turnovers) -- architecture estimates ~250K orders in 2 seconds at spike. tZERO is the throughput bottleneck, not InPlay infrastructure. Users experience this as latency between "acknowledged" and "filled"
- Auto-scaling timing -- George described spinning up VMs 1-1.5 hours before game day and scaling down after. If a game starts unexpectedly early or there's an unanticipated event, there could be a capacity gap before auto-scaling catches up

**Business risks:**

- Advertising integration with trade flow -- Max and Edwin agreed ads must not interrupt trading. But the fill notification moment (Edwin's "congratulations by Bank of America" example) is high-value ad inventory. Getting this wrong -- too intrusive -- could damage the trading experience

**Controls needed:**

- Wallet balance check before every order submission (prevent orders exceeding available funds)
- ClOrdID format validation (max 20 chars, no leading zeroes -- tZERO will reject otherwise)
- Rate limiting on order submission to prevent bot-driven trading
- Graceful degradation if tZERO connection drops -- show "trading unavailable" with last known state rather than allowing users to submit orders into a void

---

## Sub-Components

| Sub-Component | Overview | Status |
|--------------|----------|--------|
| Order Entry | Buy/sell modal -- context-aware team defaults, quantity/price input, limit order execution. Persistent access across all pages. 3 clicks or fewer target | Collecting | [[sub-components/order-entry/order-entry]] |
| Order Status | View pending/open orders and their current state (pending, partial fill, etc.). Cancel and modify actions. Where users check "what's happening with my orders?" | Proposed | |
| Fill Confirmation | Notification when a fill happens (in-app + push) plus trade receipt/detail view. The moment the user learns their order executed. Potential high-value ad placement moment (post-MVP) | Proposed | |
| Portfolio View | Current positions across all teams, unrealised P&L, total portfolio value | Proposed | |
| Trade History | Past trades -- what was bought/sold, when, at what price, realised P&L | Proposed | |
| Wallet Management | Trading wallet (100K cap), referral wallet, reload mechanism (below 25K trigger), balance display | Proposed | |

---

## Gaps and Questions for Next Call

### Gaps

- **Order confirmation flow:** Edwin said no "are you sure?" dialog, but no discussion of whether users see an order summary (team, quantity, price, total value) before hitting execute -- or is it truly one-tap?
- **Trade failure/rejection UX:** What does the user see if tZERO rejects their order? No discussion of error states in the UI
- **Position management depth:** Fill notifications discussed, but no detail on the portfolio view -- what does it look like? How much detail? Is P&L displayed per-position or aggregate?
- **Order management:** Can users cancel pending limit orders from within the app? Modify open orders? No discussion beyond architecture docs
- **Price display in trade modal:** How frequently does the bid/ask update on screen? Is it live-streaming or snapshot on modal open?
- **Trade size limits:** Any maximum order size? Any per-user position limits? Not discussed
- **Market hours:** When can users trade? Only during live games? All week? Season only? Not discussed this session
- **Desktop vs mobile trade UX:** Edwin said side-by-side teams "will not work on mobile" -- but desktop wasn't scoped. Is desktop trade experience different?
- **Swipe UX for team switching:** Troy proposed, positively received, but needs wireframing -- how does it interact with phone gestures, how many teams deep, what's the visual affordance?
- **tZERO data model:** George flagged as 80% there but needs collaboration sessions to resolve what tZERO stores vs what InPlay stores. Troy ready to set up sessions

### Questions for Edwin / Cody / Troy

1. When a user taps execute on a limit order, do they see any summary before it submits, or is it truly instant with no review step?
2. What should happen when an order is rejected by tZERO -- toast notification, modal error, inline message?
3. Can you walk through what the portfolio/positions view should look like? What data matters most at a glance?
4. Are there any trade size limits -- max shares per order, max position per team?
5. What are the trading hours? Can users place orders when no game is live, or is trading restricted to game windows?
6. For the persistent buy/sell buttons -- should they appear on every single page including education and onboarding, or only on "active" pages (team, game day, leaderboard)?
7. The swipe mechanism for switching teams -- can we schedule a wireframing session to explore this before committing?
