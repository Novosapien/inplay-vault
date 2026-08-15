---
description: "Trading component doc — the execution engine: limit orders via tZERO FIX, context-aware 3-click trade modal, wallets, fill notifications, and sub-component map"
---

# InPlay Trading Challenge -- Trading

> **Vision:** [[vision]]
> **Date:** 2026-05-11
> **Status:** Collecting — **end-to-end working in QA as of 29-07-2026**
> **Owner:** George Westbrook (engineering) / Brett StClair (client-facing)
> **Sources:** _[[meetings/06-05-2026-vision-workshop]], [[08-05-2026-component-1-simulation-app]], [[11-05-2026-trading-component]], [[27-07-2026-touchdown]], [[29-07-2026-touchdown]], [[03-08-2026-touchdown]]_
> **Updated:** 2026-08-10 — full order loop working into tZERO, short-while-long prohibited, arrow-direction bug logged, team naming moves to acronym tickers.

---

## 1. What Does This Component Do?

**Functional purpose:**

The Trading component is the execution engine of the InPlay app -- where users act on the decisions they've formed in the Information Layer. It covers the "Act -> Confirm -> Review" portion of the user journey. Users can buy and sell team stocks via limit orders routed through tZERO's ATS, manage open orders, view positions, and track P&L.

The component is designed to be accessible from anywhere in the app, not confined to a single page. A persistent trade capability follows the user across screens -- team pages, game day pages, leaderboard, and beyond. The core design principle is context-aware trading: the system infers which team(s) the user is most likely to want to trade based on where they are in the app, while always providing search as a fallback.

Trading must be fast. The target is 3 clicks or fewer from any page to a submitted order. A modal/overlay approach keeps users in context rather than navigating to a separate page.

> ### Update (27-07 → 03-08 touchdowns): trading is end-to-end working
>
> **Status change.** As of 29-07 the full loop runs: order placed in the app →
> tZERO → execution returned → handled and displayed in the app. George, after
> testing it with Hasan against Rob at tZERO: _"trading is pretty much there."_
> By 03-08 it was _"pretty much all there,"_ with the remaining gap being the
> things testing surfaces rather than anything known-missing. This is the
> component's first working end-to-end state.
>
> **What Hasan demoed** (27-07 and 29-07): buy and sell with quantity presets
> (25 / 100 / 250) plus free entry, expiry choice (day, 3 days, a week, or until
> explicitly closed), order preview, order-placed confirmation, partial fills
> shown correctly, cancel of a resting order, shorting with an explanatory
> message, and an automatic **sell/exit action pre-loaded on an open position**.
> Executions and full trade history surface at the bottom of the wallet screen.
> Ads are already placed in the same views.
>
> **Edwin's trading-desk feedback**, all of it recognisable market-maker
> instinct:
> - **Add a "max" quantity button** computed from buying power. _"Sometimes when
>   I'm trading quickly and I want to get an edge… I don't want to do the math in
>   my head or get out a calculator."_ Hasan can add it under the quantity
>   field.
> - The pre-loaded exit on a position is a **fat-finger guard** and he rates it
>   highly: under pressure people hit buy again instead of sell and end up
>   double-stuffed. _"This is fantastic for teaching how to trade."_
>
> **⚠ Bug (Jared, 29-07): the buy and sell arrows on the open-order screen point
> the wrong way** relative to every other trading app. Troy's rule: buying means
> you want the market up, selling means you want it down, so the arrows follow
> the market, not the asset. Agreed to flip. Lands in
> [[trading/sub-components/order-status/order-status]].
>
> **Short rule confirmed (Troy, 29-07): you cannot short a stock you are long.**
> You must sell your existing inventory and be **flat** first. tZERO track
> shorts not as a separate short coin but in **separate wallets** recording the
> outstanding borrowed shares. Edwin: _"you don't get short if you're already
> long. You've got to exit… and then to be short, you've got to be flat."_
> Constraint on [[trading/sub-components/order-entry/order-entry]].
>
> **Test access is gated.** Users must be added as approved test traders, and
> becoming one carries an extra step that allocates a wallet and onboards them
> to tZERO. Cody is assembling a test group of incoming interns — the
> out-of-the-gate target demographic — to work through every page. Edwin's
> instruction on 27-07: the InPlay team holds off until Hasan gives a green
> light.
>
> **QA data is real, not random** (29-07). Prices come from tZERO's market data,
> and tZERO run **replay of genuine historical games** through Sport Radar. Troy:
> _"it's all replay data."_ Cody's clarification matters for interpreting test
> results: real games, real stats, historically dated. InPlay makes the prices;
> tZERO does not.
>
> _Sources: [[27-07-2026-touchdown]], [[29-07-2026-touchdown]],
> [[03-08-2026-touchdown]]._

> ### ⚠ Update (14-08): Jared's trading test-run feedback
>
> Fourteen items from Jared Sapirman, recorded in full at
> [[jared-trading-feedback-aug-2026]]. His second written round after
> [[jared-app-feedback-jul-2026]] in July, and he is the one person testing the
> app the way a trader would rather than demonstrating it.
> Three of them are the same underlying problem and it is the serious one.
>
> **The displayed price is not the transactable price.** The price at the top of
> the team page contradicts the order book, so profit and loss is permanently
> wrong, the chart moves independently of the book, and the price offered when a
> user tries to buy is not the price they can transact at. On a product whose
> premise is that a price is the thing you own, a price the user cannot trust is
> a defect in the proposition rather than in a screen.
>
> **It makes the market order more necessary, not less.** The reporter's own
> conclusion: with a mismatched price, limit orders will frequently fail to fill
> and a retail user will not diagnose why. This is the strongest argument yet
> for the synthetic market order landing before real users arrive, see
> [[market-maker/systems/synthetic-market-order]].
>
> **Max buy is rejected when buying power is sufficient**, and still fails
> around $1,000 below the limit. Edwin asked for a max-quantity control on
> 27 July; this is that behaviour failing before the control exists.
>
> Also raised: open orders are hard to find, there is no default order size, an
> open order can only be cancelled rather than modified, positions are hard to
> locate, and bid and ask sometimes render blank. One crash: rotating to
> landscape and back left the tab bar unresponsive, with videos promised.
>
> _Source: [[jared-trading-feedback-aug-2026]]._

> ### Update (27-07): team naming and tickers
>
> Team companies cannot carry the real franchise name. Edwin does not want
> _"an unnecessary legal thing I've got to defend"_ or users thinking they are
> literally buying the New York Jets. Options weighed: prefixing with "InPlay"
> (rejected as too long), or Troy's proposal, **Kalshi-style acronyms** —
> `NYJ`, with an InPlay-style prefix pattern such as `IPG` available if needed.
> Edwin: _"I think that's perfect, Troy."_ Final form to be played with
> aesthetically and run past Marlin.
>
> The change itself is cheap: a **config update** that propagates across the app
> for all users (Hasan). The constraint is recorded as C6 in
> [[compliance/compliance]]. Tickers are also the current hard blocker on
> market-maker order testing (T13 in [[market-maker/open-questions]]).
> _Source: [[27-07-2026-touchdown]]._

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
- Buy button always on left, sell button always on right (industry convention, Edwin confirmed)
- Bottom navigation bar should include a dedicated "Trade" button alongside education and leaderboard (Edwin: "the navigation on the bottom should have a button called trade... takes you to the execution page")
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
- Symbol convention exists -- Cody confirmed: "I've got it all done already" (e.g., Edwin suggested IGBI for InPlay Green Bay Inc., INGI for InPlay New York Giants). Edwin described the autocomplete flow: type "Chicago" → Cubs, Bulls, Bears, White Sox appear

_Portfolio & Position Management (from vision -- not discussed in detail this session):_

- User can view current positions across all teams
- User can view P&L (daily/weekly/monthly)
- User can view trade history
- User can view and cancel open orders
- Trading wallet starts at 100K InPlay dollars
- Referral wallet reload when trading wallet drops below 25K

**Business rules and constraints:**

- Only limit orders for MVP -- tZERO does not support native market orders (Troy confirmed)
- Synthetic market order is a post-MVP feature -- George proposed setting a limit order at a percentage above/below current price, executing one side and cancelling the other. Troy confirmed this is standard broker practice (brokers populate best bid/offer in the UI). George flagged it as a heavy lift for MVP. Troy also noted CME Globex adds collars/"no bust ranges" to market orders, useful precedent for any tolerance-band implementation. **⚠ 20-07: moved up — Edwin wants it "before our first game or at least before the first NFL game."** Approach settled: **price-through** — take the current best bid/ask and cross N price levels through it, guaranteeing a fill at the best available prices (how CME / equity brokers implement market orders; Troy offered to help write the logic). George's time-bounded cancel-and-reprice idea superseded. Related control: fills outside the **price band** (~30% correction, TBD) can be **quote-busted** by the exchange with tZERO — see [[market-maker/market-maker]]. (Source: standup 2026-07-20)
- Only onboarded users can trade (Cody confirmed: "onboarded and signed up"). KYC requirement from vision session
- All language must use "earn" not "win" throughout -- regulatory requirement to position as skill-based competition, not chance-based (from vision session)
- Buy always left, sell always right -- industry convention (Edwin confirmed)
- V strategy is supported -- users can go long both teams, short both teams, or long one and short the other simultaneously (Edwin: "you could do a V strategy too, trading both teams at once")

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

Button placement is bottom of screen, optimised for thumb reach when holding a phone (George: "if I've got to click something at the top of the screen sometimes I might fumble it, whereas if it's just right by the bottom, it's quick... bam"). Note: Edwin suggested buy/sell should sit "above a chart somewhere, towards the top third" — the bottom placement prioritises thumb accessibility over Edwin's preference, and may need revisiting during wireframing. Troy raised configurable top/bottom (citing Apple's approach) — deferred for MVP due to complexity. George suggested building two versions and testing.

**Colour conventions:**

- Blue for buy, red for sell (proposed -- Troy confirmed PT used blue/red; Edwin mused "green for buy or blue for buy and red for sell." Not a final decision, can be revisited)
- Hover/touch glow effect on buttons to signal "you're about to act" -- Edwin suggested, but flagged as potentially v2

**Reference products discussed in this session:**

- **MetaTrader 5** (Cody demonstrated live) -- swipe up from chart to reveal trade interface. Tabs across bottom: buy now, buy limit, sell limit, buy stop, sell stop. Click, type quantity, hit trade. "Five seconds if that" to execute. Sliding quantity selector at top. Best bid/offer prices displayed above the buy/sell buttons. Troy: "that's our version of a market order because then you can just buy sell buy sell as you see the prices fluctuating"
- **Trading 212** (Max/Brett raised) -- single "Trade" button instead of separate buy/sell. Click trade, then options expand. Reduces persistent screen clutter to one button. Edwin: "I don't hate it... it's one more layer." Cody pushed back: "that's just another click that I don't necessarily like." Brett also raised a retention argument: a single buy/trade button (without visible sell) might keep users invested longer — not just a UX consideration but a behavioural one
- **Poly Market** (Edwin, negative reference for trade flow) -- "I got to click three times before I can actually even start inputting the amount... it's really irritating"

**Key UX principles (from this session):**

- 3 clicks or fewer from any page to a submitted order -- hard target
- Context-aware defaults reduce clicks: if the system knows which team is relevant, don't make the user tell it
- No "are you sure?" confirmation dialogs -- trade executes on click
- Don't interrupt the trade flow with advertising (Max: "when you're trading, let the trade flow happen"). Ads belong after the trade completes, not during — Skye: "when you've completed the sale, something else happens. Then that can be potentially owned by a brand"
- Persistent trade buttons should be collapsible for users who find them intrusive while browsing (George: specifically for when users are "annoyed they're there" while scrolling)
- Cross-team trading is a key use case: reading Packers news may compel a user to buy the Giants, because each team has independent market pricing (Edwin: "just because you're reviewing the Green Bay Packers doesn't mean you want to trade the Green Bay Packers"). Search within the trade modal and related-team suggestions (Skye's e-commerce-style "other things you might be interested in" idea, endorsed by George) serve this
- George framed pages as primary (team page, trade page — trading is the main action) vs secondary (leaderboard, education — trading is available but not the focus). UX should reflect this distinction
- Edwin noted significant ad real estate above the buy/sell buttons on MetaTrader: "look at all that real estate... why are you not advertising?" — connects trade UI directly to ad inventory value

---

## 4. How Are We Going to Solve It?

| Capability | Build/Buy/Access | Provider / Approach | Rationale |
|-----------|-----------------|-------------------|-----------|
| Order execution (limit orders) | Access | tZERO ATS via FIX 4.2 protocol | tZERO is the exchange. All orders routed through their Order Entry FIX session. They handle matching, fills, and execution reports |
| Market data for trade modal (best bid/offer) | Access | tZERO ATS via FIX Market Data feed | Live bid/ask displayed above buy/sell buttons so users can see the current price before committing. Troy: displaying best bid/offer above buttons is "our version of a market order" |
| Synthetic market orders (post-MVP) | Build | InPlay internal | Auto-populate limit price at best bid/offer with a tolerance band. George proposed, Troy confirmed this is standard broker practice. tZERO doesn't have native market orders -- brokers build this in their UI layer |
| Order management (cancel/replace) | Access | tZERO ATS via FIX 4.2 | Cancel via OrderCancelRequest (MsgType=F), replace via OrderCancelReplace (MsgType=G). tZERO handles atomically. _From architecture docs_ |
| Fill notifications (push) | Build | InPlay internal | Real-time push notification when a limit order fills. Delivered via WebSocket (Centrifugo) while user is in-app. Push notification if user is outside app (mechanism TBD). _Architecture: Centrifugo from architecture docs_ |
| Trade modal / overlay UI | Build | InPlay internal | Context-aware modal with team defaulting, search, quantity/price input, execute button. Core UX of the component |
| Persistent buy/sell buttons | Build | InPlay internal | Floating UI element across all pages with collapse/expand. Determines which teams to default based on page context |
| Wallet management | Build | InPlay internal | Trading wallet (100K cap), referral wallet reload (below 25K trigger). Balance checks before order submission |
| Position & P&L tracking | Build + Access | InPlay internal + tZERO | tZERO provides position fields on execution reports (PosSIZ, PosCOST, PosRpnl, PosUpnl). InPlay stores and displays. _FIX field tags from architecture docs_ |
| Team symbology / search | Build | InPlay internal | Symbol convention created by Cody/Kevin. Search with autocomplete across all teams |
| FIX Gateway (fan-out layer) | Build | InPlay internal | Single FIX session multiplexed across all users. Translates between FIX protocol and internal message bus (NATS). Handles session management, dedup, recovery. _From architecture docs_ |

---

## 5. What Data Does It Need?

| Data | Direction | Source / Destination | Notes |
|------|-----------|---------------------|-------|
| Best bid/offer (live) | In | tZERO FIX Market Data feed | Displayed above buy/sell buttons in the trade modal. Updates in real time. Troy: showing best bid/offer is how users make quick trading decisions without needing market orders |
| Order book depth | In | tZERO IOI + FIX Market Data feeds | For users who want to see beyond top-of-book before placing an order. Depth of display TBD |
| Order submission | Out | tZERO via FIX 4.2 Order Entry | NewOrderSingle (MsgType=D). Limit orders only (OrdType=2). ClOrdID max 20 chars, no leading zeroes |
| Execution reports | In | tZERO via FIX 4.2 Order Entry | Covers the full order lifecycle: acceptance, fills (partial/full), cancellations, replacements, rejects, busts, corrections, and end-of-day expiry. See `architecture/integrations/tzero.md` for full ExecType mapping. Proposed -- pending tZERO integration sessions to confirm |
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
| tZERO ATS | Order execution via FIX 4.2 Order Entry session (George confirmed in this call), market data (best bid/offer) via FIX Market Data feed, REST API for non-streaming data (account info, historical queries). FIX version discrepancy (PDFs say 4.2, online docs say 4.4) needs resolving _(discrepancy identified in architecture research, not this call)_ | Yes -- no tZERO, no trading |
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
- **Education component** needs to link to order type explanations -- Edwin assigned Kevin (who has the financial background) to build education content specifically covering how limit orders work when there are no market orders (Edwin's example: "if price is 8 bid at 9, bid for 12s to get as many as you want")

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

- Synthetic market orders ~~(George's tolerance-band approach -- "heavy lift for MVP")~~ — **⚠ re-scoped 20-07: wanted before the first NFL game**, via the price-through approach (see §2 business rules)
- Configurable button placement top/bottom (Troy raised, George flagged complexity)
- Swipe left/right team switching (needs UX exploration before committing)
- Hover/touch glow effects on buy/sell buttons (Edwin: "can be version two")
- Stop loss / take profit order types (Cody noted these on MetaTrader 5)
- Multi-game trading page with side-by-side teams (Edwin: "will not work on a mobile" — deferred post-MVP)

---

## 10. Risks

**Technical risks:**

- tZERO FIX version discrepancy -- PDFs specify FIX 4.2, online docs reference FIX 4.4. Must confirm before implementation. Wrong version means the gateway won't connect. _(From architecture research, not this call)_
- tZERO data model unknown -- George: "we think we're 80% there... it's just some of maybe this is what this table looks like, this is what that table looks like." Until resolved, we don't know what InPlay needs to store independently vs what we can query from tZERO
- VM requirement for trading infrastructure -- low-latency trading needs VMs, not containers. Max: VMs at ~$15K/month for 1000 concurrent users vs couple hundred on containers. Max framed the dual-infra split (VMs for trading, Kubernetes for everything else) as a competitive edge and cost differentiator vs competitors who load everything on VMs
- Single FIX session multiplexed across all users -- if the FIX gateway goes down, all trading stops. Architecture needs resilience here. _(From architecture docs)_

**UX risks:**

- Fat finger trades -- Edwin flagged this explicitly. Buy/sell buttons need clear spatial separation from all other UI elements. No confirmation dialog means an accidental tap is a real trade
- Persistent trade buttons could annoy users who aren't in a trading mindset -- collapse/expand mitigates but needs testing
- 3-click target may not hold on all page types -- game day page with two teams plus search could push beyond 3 in edge cases
- Limit orders only may confuse users who expect to just tap "buy" and get filled -- education module needs to clearly explain that you must specify a price

**Infrastructure risks:**

- Peak load at game moments (touchdowns, turnovers) -- architecture estimates ~250K orders in 2 seconds at spike. tZERO is the throughput bottleneck, not InPlay infrastructure. Users experience this as latency between "acknowledged" and "filled"
- Auto-scaling timing -- George described spinning up VMs 1 to 1.5 hours before the first game on a game day and scaling down a couple of hours after the last game finishes. If a game starts unexpectedly early or there's an unanticipated event, the system will still auto-scale but the pre-warmed capacity may not be ready

**Business risks:**

- Advertising integration with trade flow -- Max and Edwin agreed ads must not interrupt trading. But the fill notification moment (Edwin's "congratulations by Bank of America" example) is high-value ad inventory. Getting this wrong -- too intrusive -- could damage the trading experience

**Controls needed:**

- Wallet balance check before every order submission (prevent orders exceeding available funds)
- ClOrdID format validation (max 20 chars, no leading zeroes -- tZERO will reject otherwise). _(From architecture docs)_
- Rate limiting on order submission to prevent bot-driven trading
- Graceful degradation if tZERO connection drops -- show "trading unavailable" with last known state rather than allowing users to submit orders into a void

---

## Sub-Components

| Sub-Component | Overview | Status | Link |
|--------------|----------|--------|
| Order Entry | Buy/sell modal -- context-aware team defaults, quantity/price input, limit order execution. Persistent access across all pages. 3 clicks or fewer target | Collecting | [[sub-components/order-entry/order-entry]] |
| Order Status | View pending/open orders and their current state (pending, partial fill, etc.). Cancel and modify actions. Where users check "what's happening with my orders?" | Collecting | [[sub-components/order-status/order-status]] |
| Fill Confirmation | Notification when a fill happens (in-app + push) plus trade receipt/detail view. The moment the user learns their order executed. Potential high-value ad placement moment (post-MVP) | Collecting | [[sub-components/fill-confirmation/fill-confirmation]] |
| Portfolio View | Current positions across all teams, unrealised P&L, total portfolio value | Collecting | [[sub-components/portfolio-view/portfolio-view]] |
| Trade History | Past trades -- what was bought/sold, when, at what price, realised P&L | Collecting | [[sub-components/trade-history/trade-history]] |
| Wallet Management | Trading wallet (100K cap), referral wallet, reload mechanism (below 25K trigger), balance display | Collecting | [[sub-components/wallet-management/wallet-management]] |
| Trading-Engine Simulation / Admin Panel _(internal tooling)_ | **Internal, not user-facing.** Simulation harness with example traders ("Contrarian Carol", "Panic Pete") to stress-test order fulfilment, per-trade speed, latency, and bid-ask spread under bursts (~100k users) before tZERO integration. Intended to grow into an admin/monitoring panel. _Confirmed internal tooling (29-05/19-05)_ | Collecting | [[sub-components/trading-engine-sim/trading-engine-sim]] |

---

> **Architecture note (from May touchdowns):** **tZERO confirmed as the ATS/settlement partner** — FINRA-approved, first US ATS for tokenized assets; scale validated (~1M trades/sec, 3M wallets, no queueing). Backend uses a **FIX gateway** (built) + messaging bus + websocket connections; whitelisted IP sent to tZERO for parallel testing, pursuing GCP-to-GCP direct connect. Weekly Friday tZERO sync. _Sources: [[15-05-2026-touchdown]], [[18-05-2026-touchdown]], [[28-05-2026-touchdown]]._
>
> **Update (1–8 June touchdowns):** **VPC stood up** — locked down, secure, and connected to tZERO. The **FIX gateway was rebuilt** to handle very high concurrent request volume; **load testing (Hassan) is fast** ("room for improvement, but a really good starting point"). The **tZERO integration is working** with backend dashboards and a scale-test harness ready to push the integration. The good tZERO call (05-06) moved into edge cases / test scenarios. **Open homework (→ [[architecture/open-questions]]):** define how **buying power and the referral wallet** operate and look/feel, and **which parts NOVO builds vs tZERO** — refines the still-blocking "what does tZERO manage?" question. _Sources: [[03-06-2026-touchdown]], [[05-06-2026-touchdown]]._
>
> **Update (10 June — wallet / buying-power ownership RESOLVED):** **tZERO owns and manages the trading wallet** (tied to the digital wallet). **InPlay tracks the referral wallet** and builds the **<25K reload mechanism** (referral → trading). **Cash wallet host = still TBD** (tZERO vs third party). Critically, **tZERO does *not* calculate buying power** — they only do that in production *as the broker*; **InPlay must build an "InPlay market synthetic broker" element that tracks buying power** (a new InPlay-side responsibility). ⚠️ Business requirements for the synthetic broker are **not yet written** — flagged for the **Friday tZERO session** (IPO/primary-offering BRs are done). **Shorting mechanics:** a short *increases* buying power — short 100K → receive 100K in funds → need 200K buying power to close (buy back); a drawdown to ~100K triggers return of the shares. Hard on-chain — tokenization lacks the locates/reserve mechanisms traditional markets use; Troy is writing the **shorting business requirements** (also Friday). _Source: [[10-06-2026-Touchdown]]._
>
> **Update (12–17 June touchdowns):** **Market maker resurfaces across all three calls.** **Kevin Murray (Head Execution Trader)** is leading the market-making algorithm work with George, deliberately **position-based rather than high-frequency** ("reflective of opinion in the market that day"), possibly with a data-science intern. Separately, Edwin flags the need to **build an internal market maker** (likely tZERO-integrated) to guarantee **IPO fill and ongoing liquidity**, and wants at least one **dummy IPO plus simulated events** to test before launch (see the inventory-visibility / straw-buyer note in [[ipo-module/ipo-module]]). Brett proposed a focused **Mon–Tue ~90-minute session**; logged in [[architecture/open-questions]] and a candidate **new `trading/market-maker` sub-component** once scoped. **tZERO real-time P&L confirmed (12-06):** the tZERO call resolved a buying-power concern, tZERO will handle **real-time P&L calculations** on user holdings (unrealised gains/losses recalculate dynamically). _Sources: [[12-06-2026-touchdown]], [[15-06-2026-touchdown]], [[17-06-2026-touchdown]]. See [[digests/touchdowns-12-17-jun-2026]]._
>
> **Update (18–29 June touchdowns):** **Buying-power → tZERO mechanism (24-06, 26-06).** To let a user move funds from the **referral wallet into the trading wallet**, InPlay must give tZERO each account's **buying power** — initially a **start-of-day file** (decision: **no intraday wallet rebalancing**, to avoid complexity; tZERO calculates buying power intraday). George proposed a more **elegant API mechanism** — an API call that **increases the user's tZERO wallet buying power while InPlay consumes the referral** on its side (so it can't be reused) — instead of an FTP file load; Troy endorsed it and George is **drafting it to tZERO**. Reinforced framing: **buying power = "trading power"** (covers selling/shorting, not just buying); the **ledger = the clearing/settlement custodial record**; the **simulator uses a synthetic wallet**, production a **real digital wallet** (broker / stablecoin funded). **Market-maker session reconfirmed (24-06, 26-06, 29-06):** Edwin will **co-build the market-making algo with George** (he has the parameters from a prior "Xperry" algo; the hard part is API-connecting the **tZERO feeds**) — a separate session is needed. The session should also **capture market data for production market makers** to model on, and feeds **academic white papers** (Jim Angel; Josh's, scope TBD) on how the market behaves when an outcome is a foregone conclusion. _Sources: [[24-06-2026-touchdown]], [[26-06-2026-ai-agent-research-component]], [[29-06-2026-touchdown]]. See [[digests/touchdowns-18-29-jun-2026]]._
>
> **Update (20 July — Market Maker promoted to its own component):** the 20-07 mechanics session with Edwin and Troy resolved enough of the market-maker picture that it is now a **standalone component — see [[market-maker/market-maker]]** (the earlier "candidate `trading/market-maker` sub-component" framing is superseded). Headlines for Trading: the MM is a **synthetic tZERO entity** (unlimited buying power, short-locate exemption) posting resting liquidity — **user orders can match each other directly**, the MM is not a required counterparty; **everything stays limit orders** (crossing limit orders replace market orders); **cancel-replace quoting ~5–10×/sec**; **InPlay builds CTS1/CTS2** (the price engines — not consumed from tZERO); markets are **truly isolated per team** (pairs-trading frame — no cross-game or rankings effects intra-game). **tZERO tech calls now 2×/week (Tue/Thu)** alongside Mon/Wed/Fri touchdowns; tZERO asked to stand up the synthetic MM entity in QA. **MM ops UI = desktop version of this app**, built for the MM first (params, order lookup, positions/P&L — Kevin likely operator). MM deep-dive **Thu 23-07, 3–4pm London**. _Source: [[20-07-2026-touchdown]]._

> **Update (24 July, trading infra mapped, small items remain, sim testing route):** the team **mapped out every component of the trading infrastructure yesterday** (23-07), where each stands and what remains. Launch-readiness is **non-negotiable** ("it's going to be ready for launch"). What is left is **small and well-understood**: adding the **cancel feature** and a **cancel-and-request feature**, both tightly integrated with the market maker (the thing being traded against). Some items had been waiting on **tZERO** (one API linking to another). **Testing does not need a live game:** pick a **historical game** (Chiefs vs Ravens was used), **run a simulation** off it on a test version of the app, and **repeat multiple times a day**, verifying both the user-side experience and the market-maker side. Edwin also asked for a **read-only monitoring dashboard** over the market maker (inventory / shares held per market / bills) so an InPlay operator can watch it near-production; George notes the MM **is just another user**, so the **same inventory APIs** that show a user their positions serve the MM view, phased (backend-working, then data representation, then later variable control). MM specifics belong to [[market-maker/market-maker]]; not restated here. _Source: [[24-07-2026-touchdown]]._
>
> **Update (24 July touchdown):** **Trading is launch non-negotiable — target live for ~Aug 22** (Troy: "we need to get this live for the 22nd"; Edwin: "less than a month before this is all going to happen"). The full trading-infrastructure component map was completed 23-07 — "every single component… where are we at with all of it" — leaving a to-do list of small items (e.g. the **cancel feature** and **cancel-and-replace**), tightly integrated with the [[market-maker/market-maker|Market Maker]] ("the market maker is going to be the thing trading"). **Testing doesn't wait for live games:** SR simulation replays of past games (e.g. Chiefs–Ravens) can run multiple times a day, checked from both the user's perspective and the MM's side. **Launch-scope remainder named:** notifications, tax forms, payouts — payouts are the blind spot (payment-provider deal unsigned; worst case users see amounts owed and payouts are delayed a couple of weeks; Edwin fine with an interim manual rail — Zelle/wire). Cody's roadmap/bandwidth-visibility ask → Brett + George building a vault dashboard for release cadence. _Source: [[24-07-2026-touchdown]]._

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
