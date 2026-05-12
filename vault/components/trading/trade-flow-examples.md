# Trade Flow -- Button Press to Confirmation Card

> **Sources:** [tZERO Drop Copy API](https://apidocs.tzero.com/docs/fix/drop-copy#sample-messages), [tZERO Order Entry API](https://apidocs.tzero.com/docs/fix/order-entry), [[architecture/integrations/t0|T0 Integration Doc]]
> **Date:** 2026-05-12

---

## End-to-End Flow Overview

```
 USER (Mobile App)              INPLAY BACKEND                    tZERO ATS
 ──────────────────      ──────────────────────────      ─────────────────────
                         
 ① Tap [BUY] on         
    team page                    
         │                       
 ② Modal opens:                  
    Team: IGBI (pre-filled)      
    Qty: 500                     
    Price: 3.55                  
    [EXECUTE]                    
         │                       
 ③ Tap [EXECUTE] ──────▶ ④ Validate order              
                              │                          
                         ⑤ Generate ClOrdID ────────▶ ⑥ NewOrderSingle
                              (e.g., "INP20260911001")     (MsgType=D)
                                                             via FIX 4.2
                                                                │
                                                         ⑦ Order hits book
                                                                │
                         ⑧ Execution Report ◀──────────── ExecType=0
                              (Order Accepted)               (New)
                              │                          
 ⑨ "Order placed" ◀─────── Push to user                 
    toast notification         via WebSocket              
         │                       
    ... time passes ...          
    (price reaches 3.55)         
                                                                │
                                                         ⑩ Match found
                                                                │
                         ⑪ Execution Report ◀──────────── ExecType=2
                              (Filled)                      (Filled)
                              │                          
 ⑫ Confirmation ◀──────── Push to user                  
    card appears              via WebSocket               
```

---

## Example 1: Buy 500 Shares of IGBI (Green Bay Packers) at $3.55

### Step 1 -- User taps BUY on the Packers team page

The persistent buy button is visible. User taps it. Modal overlays the screen.

```
┌──────────────────────────────┐
│  🟢 BUY  ·  IGBI             │
│  InPlay Green Bay Inc.       │
│                              │
│  Qty    [ 500            ]   │
│  Price  [ 3.5500         ]   │
│                              │
│  Best Bid: 3.50  Ask: 3.55  │
│                              │
│  ┌──────────────────────┐    │
│  │     EXECUTE BUY      │    │
│  └──────────────────────┘    │
└──────────────────────────────┘
```

User enters 500 shares at $3.55 (buying the ask for immediate fill). Taps EXECUTE. No confirmation prompt.

### Step 2 -- App sends NewOrderSingle to FIX Gateway

The app generates a unique ClOrdID and sends to the Trading Service, which forwards via the FIX Gateway to tZERO.

**FIX message sent (NewOrderSingle, MsgType=D):**

| Tag | Field | Value | Notes |
|-----|-------|-------|-------|
| 35 | MsgType | D | New Order Single |
| 11 | ClOrdID | INP20260911001 | Max 20 chars, no leading zeroes |
| 1 | Account | INPLAY-SIM-001 | InPlay's account at tZERO |
| 55 | Symbol | IGBI | InPlay Green Bay Inc. |
| 54 | Side | 1 | 1=Buy |
| 38 | OrderQty | 500 | |
| 40 | OrdType | 2 | 2=Limit (only type tZERO supports) |
| 44 | Price | 3.5500 | 4 decimal places required |
| 59 | TimeInForce | 0 | 0=Day order |
| 100 | ExDestination | STX | tZERO's exchange destination |
| 60 | TransactTime | 20260911-23:15:42.331 | GMT timestamp |

### Step 3 -- tZERO accepts the order

tZERO validates and places the order on the book. Returns an Execution Report.

**FIX message received (Execution Report -- Order Accepted):**

```
8=FIX.4.4|35=8|11=INP20260911001|37=78452|55=IGBI|54=1|38=500|
40=2|44=3.550000|59=0|100=STX|20=0|150=0|39=0|17=90001|
32=0|151=500|14=0|60=20260911-23:15:42.445|76=STX|
```

| Tag | Field | Value | Meaning |
|-----|-------|-------|---------|
| 150 | ExecType | 0 | New -- order accepted |
| 39 | OrdStatus | 0 | New -- sitting on book |
| 37 | OrderID | 78452 | tZERO's internal order ID |
| 17 | ExecID | 90001 | Unique execution report ID |
| 32 | LastShares | 0 | No fill yet |
| 151 | LeavesQty | 500 | Full quantity still open |
| 14 | CumQty | 0 | Nothing filled yet |

**What the user sees:**

```
┌──────────────────────────────┐
│  ✓ Order Placed               │
│                              │
│  BUY 500 IGBI @ $3.55       │
│  Status: Open                │
│                              │
│  [View Orders]  [Dismiss]    │
└──────────────────────────────┘
```

Toast notification, auto-dismisses after 3 seconds. User continues browsing.

### Step 4 -- Order gets filled

A seller matches at $3.55. tZERO sends a fill Execution Report.

**FIX message received (Execution Report -- Fully Filled):**

```
8=FIX.4.4|35=8|11=INP20260911001|37=78452|55=IGBI|54=1|38=500|
40=2|44=3.550000|59=0|100=STX|20=0|150=2|39=2|17=90045|
9902=78452-STX-20260911|32=500|31=3.550000|6=3.550000|
151=0|14=500|30=STX|9730=R|
```

| Tag | Field | Value | Meaning |
|-----|-------|-------|---------|
| 150 | ExecType | 2 | Filled -- complete |
| 39 | OrdStatus | 2 | Filled |
| 32 | LastShares | 500 | This fill: 500 shares |
| 31 | LastPx | 3.550000 | Fill price |
| 6 | AvgPx | 3.550000 | Average price across all fills |
| 14 | CumQty | 500 | Total filled |
| 151 | LeavesQty | 0 | Nothing remaining |
| 9902 | MatchId | 78452-STX-20260911 | Unique trade match ID |
| 9730 | LiquidityFlag | R | Removed liquidity (hit the ask) |

### Step 5 -- Confirmation card

Push notification fires. User sees the confirmation card wherever they are in the app.

```
┌──────────────────────────────┐
│  ✅ Trade Executed            │
│                              │
│  BOUGHT 500 IGBI             │
│  InPlay Green Bay Inc.       │
│                              │
│  Price      $3.5500          │
│  Total      $1,775.00        │
│  Time       11:15:42 PM      │
│                              │
│  ── Sponsored by Doritos ──  │
│                              │
│  [Place Sell]  [View Pos.]   │
└──────────────────────────────┘
```

---

## Example 2: Sell 200 Shares of INGI (NY Giants) -- Partial Fill then Complete

User is on the Giants game page during a live game. Price is moving. They want to sell at $4.20 but the best bid is only $4.15.

### Step 1 -- User taps SELL, enters limit price above market

```
┌──────────────────────────────┐
│  🔴 SELL  ·  INGI            │
│  InPlay New York Giants Inc. │
│                              │
│  Qty    [ 200            ]   │
│  Price  [ 4.2000         ]   │
│                              │
│  Best Bid: 4.15  Ask: 4.22  │
│                              │
│  ┌──────────────────────┐    │
│  │     EXECUTE SELL     │    │
│  └──────────────────────┘    │
└──────────────────────────────┘
```

### Step 2 -- NewOrderSingle sent

| Tag | Field | Value |
|-----|-------|-------|
| 35 | MsgType | D |
| 11 | ClOrdID | INP20260911002 |
| 55 | Symbol | INGI |
| 54 | Side | 2 (Sell) |
| 38 | OrderQty | 200 |
| 40 | OrdType | 2 (Limit) |
| 44 | Price | 4.2000 |
| 59 | TimeInForce | 0 (Day) |
| 100 | ExDestination | STX |

### Step 3 -- Order accepted

```
150=0|39=0|32=0|151=200|14=0
```
ExecType=0 (New). 200 shares sitting on the book at $4.20.

### Step 4 -- Partial fill: 120 of 200 shares matched

A buyer takes 120 shares at $4.20.

**FIX message received (Partial Fill):**

```
8=FIX.4.4|35=8|11=INP20260911002|37=78460|55=INGI|54=2|38=200|
40=2|44=4.200000|20=0|150=1|39=1|17=90067|32=120|31=4.200000|
6=4.200000|151=80|14=120|30=STX|9730=A|
```

| Tag | Field | Value | Meaning |
|-----|-------|-------|---------|
| 150 | ExecType | 1 | Partial fill |
| 32 | LastShares | 120 | This fill: 120 shares |
| 31 | LastPx | 4.200000 | At $4.20 |
| 14 | CumQty | 120 | Total filled so far |
| 151 | LeavesQty | 80 | 80 still open on book |
| 9730 | LiquidityFlag | A | Added liquidity (was resting on book) |

**What the user sees (toast):**

```
┌──────────────────────────────┐
│  ⚡ Partial Fill              │
│                              │
│  SOLD 120 / 200 INGI        │
│  @ $4.2000                   │
│  80 remaining                │
└──────────────────────────────┘
```

### Step 5 -- Remaining 80 shares filled

Another buyer takes the rest.

**FIX message received (Full Fill):**

```
8=FIX.4.4|35=8|11=INP20260911002|37=78460|55=INGI|54=2|38=200|
40=2|44=4.200000|20=0|150=2|39=2|17=90072|32=80|31=4.200000|
6=4.200000|151=0|14=200|30=STX|9730=A|
```

| Tag | Field | Value | Meaning |
|-----|-------|-------|---------|
| 150 | ExecType | 2 | Filled -- complete |
| 32 | LastShares | 80 | This fill: 80 shares |
| 14 | CumQty | 200 | All 200 now filled |
| 151 | LeavesQty | 0 | Nothing remaining |

**Confirmation card:**

```
┌──────────────────────────────┐
│  ✅ Trade Complete            │
│                              │
│  SOLD 200 INGI               │
│  InPlay New York Giants Inc. │
│                              │
│  Avg Price   $4.2000         │
│  Total       $840.00         │
│  Fills       2 (120 + 80)    │
│                              │
│  ── Sponsored by Monster ──  │
│                              │
│  [Place Buy]  [View P&L]     │
└──────────────────────────────┘
```

---

## Example 3: Order Rejected -- Restricted Symbol

User tries to buy a symbol that's on the restricted list.

### NewOrderSingle sent → Rejection received

**FIX message received (Rejected):**

```
8=FIX.4.4|35=8|11=INP20260911003|37=INP20260911003|55=EXOD|54=2|
38=1500|40=2|44=4.320000|59=0|20=0|150=8|39=8|17=91001|32=0|
151=0|14=0|58=FAILSRISK[TZROATS01]: EXOD is on the restricted securities list|
```

| Tag | Field | Value | Meaning |
|-----|-------|-------|---------|
| 150 | ExecType | 8 | Rejected |
| 39 | OrdStatus | 8 | Rejected |
| 58 | Text | FAILSRISK... | Reason: restricted security |

**What the user sees:**

```
┌──────────────────────────────┐
│  ❌ Order Rejected            │
│                              │
│  EXOD is currently           │
│  restricted from trading.    │
│                              │
│  [OK]                        │
└──────────────────────────────┘
```

---

## Example 4: Trade Busted (Execution Reversal)

Rare but critical. A previous fill is reversed by the exchange.

**FIX message received (Bust):**

```
8=FIX.4.4|35=8|11=INP20260911002|37=78460|55=INGI|54=2|38=200|
40=2|20=1|150=H|39=4|17=91050|19=90067|9902=78460-STX-20260911|
32=120|31=4.200000|6=4.200000|151=0|14=80|
```

| Tag | Field | Value | Meaning |
|-----|-------|-------|---------|
| 20 | ExecTransType | 1 | Cancel (bust) |
| 150 | ExecType | H | Trade busted |
| 19 | ExecRefID | 90067 | References the original fill being reversed |
| 32 | LastShares | 120 | The 120-share fill is being reversed |

**What the user sees:**

```
┌──────────────────────────────┐
│  ⚠️ Trade Reversed            │
│                              │
│  Your sell of 120 INGI       │
│  @ $4.2000 has been          │
│  reversed by the exchange.   │
│                              │
│  Your position and P&L       │
│  have been updated.          │
│                              │
│  [View Position]  [OK]       │
└──────────────────────────────┘
```

---

## State Machine: What the User Sees

```
┌───────────┐    Execute     ┌──────────────┐   ExecType=0    ┌────────────┐
│           │   tapped       │              │   (Accepted)    │            │
│  MODAL    │───────────────▶│  SUBMITTING  │────────────────▶│  OPEN      │
│  (input)  │                │  (spinner)   │                 │  (on book) │
│           │                │              │                 │            │
└───────────┘                └──────┬───────┘                 └─────┬──────┘
                                    │                               │
                              ExecType=8                    ExecType=1 │ ExecType=2
                              (Rejected)                   (Partial)  │ (Filled)
                                    │                          │      │
                                    ▼                          ▼      ▼
                             ┌────────────┐           ┌──────────────────┐
                             │            │           │                  │
                             │  REJECTED  │           │  CONFIRMATION    │
                             │  (error)   │           │  CARD            │
                             │            │           │  (+ ad slot)     │
                             └────────────┘           │                  │
                                                      │  [Place counter] │
                                                      │  [View position] │
                                                      └──────────────────┘
                                                               │
                                                        ExecType=H (rare)
                                                               │
                                                               ▼
                                                      ┌──────────────────┐
                                                      │  BUST ALERT      │
                                                      │  (trade reversed) │
                                                      └──────────────────┘
```

---

## Key Implementation Notes

**From tZERO constraints:**
- All orders are limit orders (`OrdType=2`). tZERO does not support market orders
- ClOrdID max 20 characters, no leading zeroes
- Price must be 4 decimal places
- ExDestination always `STX`
- TimeInForce: `0`=Day (default), `1`=GTC, `6`=GTD
- GTC/GTD orders require `RoutingInst=DNRI` (tag 9303)
- Drop Copy session provides independent read-only execution reports for reconciliation

**From session decisions (2026-05-11):**
- Simulation uses limit orders only -- no synthetic market orders for MVP
- 3 clicks max to execute from any page
- No confirmation prompt -- EXECUTE triggers immediately
- Fill notifications push to user wherever they are in the app
- Confirmation card doubles as ad placement (sponsor-branded)
- Partial fills show running total with remaining quantity

**FIX tag quick reference for Execution Reports:**

| Tag | Name | Key Values |
|-----|------|------------|
| 150 | ExecType | 0=New, 1=Partial, 2=Filled, 3=DoneForDay, 4=Canceled, 5=Replaced, 8=Rejected, H=Busted, G=Corrected |
| 39 | OrdStatus | 0=New, 1=PartiallyFilled, 2=Filled, 4=Canceled, 8=Rejected |
| 20 | ExecTransType | 0=New, 1=Cancel (bust), 2=Correct |
| 32 | LastShares | Quantity in this fill |
| 31 | LastPx | Price of this fill |
| 14 | CumQty | Total quantity filled across all fills |
| 151 | LeavesQty | Quantity still open on book |
| 6 | AvgPx | Average price across all fills |
| 9730 | LiquidityFlag | A=Added (resting), R=Removed (aggressor) |
| 19 | ExecRefID | References original ExecID on bust/correct |
