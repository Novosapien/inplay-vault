# Trading Module -- Session Notes (2026-05-11)

> **Source:** [[meetings/11-05-2026-modules-2-and-3]]
> **Status:** Decisions captured, awaiting implementation spec

---

## 1. Trade Entry Points

The trade mechanism must be accessible from every page in the app. The number of clicks to execute varies by context.

```
┌─────────────────────────────────────────────────────────────┐
│                     ENTRY POINTS                            │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  Team Page   │  │ Game Day Page│  │  Any Other Page  │  │
│  │              │  │              │  │  (Leaderboard,   │  │
│  │  Team known  │  │  2 teams     │  │   Discovery,     │  │
│  │  already     │  │  in matchup  │  │   Education)     │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘  │
│         │                 │                    │            │
│    1-2 clicks        2-3 clicks           3 clicks max     │
│         │                 │                    │            │
│         ▼                 ▼                    ▼            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              TRADE EXECUTION MODAL                  │   │
│  │  ┌─────────┐  ┌──────────┐  ┌───────────────────┐  │   │
│  │  │  Team   │  │ Quantity │  │  Price (limit)    │  │   │
│  │  │ (pre-   │  │          │  │                   │  │   │
│  │  │  filled │  │          │  │  Best bid/offer   │  │   │
│  │  │  from   │  │          │  │  shown above      │  │   │
│  │  │  context│  │          │  │  buttons           │  │   │
│  │  └─────────┘  └──────────┘  └───────────────────┘  │   │
│  │                                                     │   │
│  │         ┌─────────┐    ┌──────────┐                 │   │
│  │         │   BUY   │    │   SELL   │                 │   │
│  │         │ (left)  │    │ (right)  │                 │   │
│  │         └─────────┘    └──────────┘                 │   │
│  │              No confirmation prompt                 │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Click Counts by Page

| Page | Assumed team | Clicks to execute | Flow |
|------|-------------|-------------------|------|
| Team page | The team being viewed | 1-2 | Buy/Sell → modal (team pre-filled) → execute |
| Game day page | Either team in the matchup | 2-3 | Choose team → Buy/Sell → modal → execute |
| Any other page | None assumed | 3 max | Trade button → search/select team → Buy/Sell → execute |

---

## 2. Persistent Buy/Sell Buttons

Buy and sell buttons are persistent across the app. They float above the bottom navbar and remain visible while scrolling.

```
┌──────────────────────────────┐
│                              │
│      Page Content            │
│      (scrollable)            │
│                              │
│                              │
│                              │
│                              │
├──────────────────────────────┤
│                              │
│  ┌─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┐   │
│  │  Persistent Buttons   │   │  ◄── Floats above navbar
│  │                       │   │
│  │  [  BUY  ]  [ SELL ]  │   │      Buy = left (blue/green)
│  │                       │   │      Sell = right (red)
│  │      [ ≡ collapse ]   │   │
│  └─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┘   │
│                              │
│  ┌───┬───┬───┬───┬───┐      │
│  │ ☰ │ 📊│Trade│ 🏆│ 📚│      │  ◄── Bottom navbar
│  └───┴───┴───┴───┴───┘      │
└──────────────────────────────┘
```

**Behaviour by page type:**

| Page type | Button state | Rationale |
|-----------|-------------|-----------|
| Team page / Trade page | Auto-expanded, team pre-filled | User is most likely here to trade |
| Game day page | Auto-expanded, both teams available | Trade intent is high |
| Leaderboard, Discovery, Education | Collapsed by default, trade icon in top-right to expand | Don't pollute non-trading pages |

**Collapse/expand:**
- Small toggle button to minimize the persistent buttons when not wanted
- Click again to restore
- Edwin: "I'm not saying I don't love that. I kind of like that."

---

## 3. Swipe Navigation Between Teams

On the game day trade view, users swipe between order tickets for each team in the matchup.

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│          ◄ swipe left          swipe right ►             │
│                                                          │
│  ┌────────────┐   ┌────────────┐   ┌────────────────┐   │
│  │            │   │            │   │                │   │
│  │  TEAM B    │   │  TEAM A    │   │   SEARCH       │   │
│  │  Order     │   │  Order     │   │   (find any    │   │
│  │  Ticket    │   │  Ticket    │   │    team)       │   │
│  │            │   │            │   │                │   │
│  │ [BUY][SELL]│   │ [BUY][SELL]│   │  [search bar]  │   │
│  │            │   │            │   │  Active games   │   │
│  └────────────┘   └────────────┘   └────────────────┘   │
│                        ▲                                 │
│                   Default view                           │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

- **Swipe right** from Team A → Team B order ticket
- **Swipe right again** → Search view (all active games + search bar)
- Familiar mobile gesture (Tinder/Hinge pattern)
- Multi-game trading page deferred to post-MVP

---

## 4. Order Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐     ┌─────────┐
│          │     │              │     │              │     │         │
│  User    │────▶│  InPlay App  │────▶│  FIX Gateway │────▶│  T0 ATS │
│  (mobile)│     │  (modal)     │     │  (FIX 4.2)   │     │         │
│          │     │              │     │              │     │         │
└──────────┘     └──────────────┘     └──────────────┘     └────┬────┘
                                                                │
                                                                │ Fill
                                                                │
┌──────────┐     ┌──────────────┐     ┌──────────────┐         │
│          │     │              │     │              │◄────────┘
│  User    │◄────│  Push        │◄────│  Trading     │
│  (notif) │     │  Notification│     │  Service     │
│          │     │              │     │              │
└──────────┘     └──────────────┘     └──────────────┘
```

### Order types

| Type | MVP? | How it works |
|------|------|-------------|
| **Limit order** | Yes | User specifies exact price. T0 native support. Only order type for simulation |
| **Synthetic market order** | No (post-MVP) | App auto-populates best bid/offer as a limit order with bounds. Cancels if not filled within threshold |

**Why limit orders only:**
- T0 does not support market orders natively
- Market orders risk disorderly markets
- Risk of "bus trades" -- exchange reversals on unreasonable prices
- Edwin: "I think for the simulation I think we just stick with limit orders"
- Troy: "Market orders are not a common order type on an exchange in equities world. They're order types that the brokers create on their platforms through their UIs"

### Synthetic market order concept (post-MVP)

George proposed and Troy confirmed this mirrors real equities:
1. User clicks "buy at market"
2. App reads current best offer (e.g., $9.00)
3. App places a limit order at best offer + X% threshold
4. If filled → done. If not filled within bounds → cancelled
5. Same in reverse for sell (limit at best bid - X%)

---

## 5. Fill Notifications

When a limit order gets filled while the user is elsewhere in the app:

```
┌──────────────────────────────────┐
│  🔔 Order Filled                 │
│                                  │
│  Bought 500 IGBI @ $3.00        │
│  Green Bay Packers Inc.          │
│                                  │
│  [Place Sell Order]  [Dismiss]   │
│                                  │
│  Sponsored by Bank of America    │
└──────────────────────────────────┘
```

- Push notification triggers immediately on fill
- Allows user to immediately place a counter-order (e.g., sell at $7 after buying at $3)
- Edwin: "The whole idea is as much trading as possible as quickly as possible"
- Notification is also an ad placement opportunity (sponsor-branded congratulations)

---

## 6. Team Symbology

Each team has a stock ticker symbol for search and trading.

- Convention already completed by Cody
- Example format: IGBI (InPlay Green Bay Inc.), INGI (InPlay New York Giants Inc.)
- Type-ahead search from any page (~163 teams: 32 NFL + ~131 NCAA)
- Search must handle overlaps (e.g., "Buffalo" → Bills vs. college team)

---

## 7. Reference Products

| Product | Take | Avoid |
|---------|------|-------|
| **MetaTrader 5** | Swipe-up chart for order entry. Buy limit, sell limit tabs. 5 seconds app-open to trade. Best bid/offer prices shown above buttons | Quantity slider may invite fat fingers |
| **Poly Market** | — | 3+ clicks to reach trade input. "Really irritating" (Edwin) |
| **Trading 212** | Single "Trade" button that expands to buy/sell options. Cleaner real estate | Extra click layer vs persistent buy/sell |

---

## Decisions Summary

| Decision | Detail | Status |
|----------|--------|--------|
| Limit orders only for simulation | T0 constraint + deliberate choice for orderly markets | Confirmed |
| Persistent buy/sell across all pages | Floats above navbar, collapsible | Confirmed |
| 3 clicks max to execute | Context-aware team pre-selection reduces clicks | Confirmed |
| Swipe between team order tickets | Left/right between teams in a matchup + search | Confirmed |
| No confirmation prompt | Click execute → order sent immediately | Confirmed |
| Bottom navbar with Trade button | Standard 5-point bottom nav | Confirmed |
| Buy left, Sell right | Industry convention | Confirmed |
| Synthetic market orders | Post-MVP | Deferred |
| Configurable nav position (top/bottom) | Too complex for MVP | Deferred |
| Multi-game trading page | Side-by-side teams won't work on mobile | Deferred |
