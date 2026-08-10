---
description: "Page spec for the Portfolio screen — trading and referral wallet balances, open positions with unrealised P&L, and links to Orders, History and Wallet"
---

# Portfolio

> **Tab:** Trade
> **Purpose:** Overview of all current positions and trading activity.
> **Map:** [[product/pages/PAGES|App Pages]]

---

## What Users See

The user's trading headquarters. Everything they own, how it's performing, and quick access to manage trades.

---

## Key Elements

- **Trading Wallet Balance** — simulated capital available for new trades (capped at 100,000 InPlay dollars)

- **Referral Wallet Balance** — bonus capital earned from referring friends (uncapped, separate pool)

- **Open Positions** — list of all teams the user currently holds stock in, each showing:
  - Team name and colors
  - Quantity of shares held
  - Average entry price (what they paid)
  - Current market price
  - Unrealised P&L — profit or loss if they sold now (green = profit, red = loss)

- **Quick Links** — navigation to Orders (pending), History (past trades), and Wallet (balance details)

---

## Where Users Go From Here

- Tap a position → [[product/pages/trading/position-detail|Position Detail]]
- Tap "Orders" → [[product/pages/trading/open-orders|Open Orders]]
- Tap "History" → [[product/pages/trading/trade-history|Trade History]]
- Tap wallet area → [[product/pages/trading/wallet|Wallet Details]]

---

## States

- **Has positions:** Full list with P&L color coding
- **No positions:** Empty state encouraging first trade, links to Discovery
- **Mixed P&L:** Some positions green, some red — overall portfolio P&L shown at top
