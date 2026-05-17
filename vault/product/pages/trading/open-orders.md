# Open Orders

> **Tab:** Trade
> **Purpose:** All pending orders that haven't been filled yet.
> **Map:** [[product/pages/PAGES|App Pages]]

---

## What Users See

Limit orders the user has placed that are waiting to be matched. These are orders where the user specified a price they're willing to pay (or sell at), and the market hasn't reached that price yet.

---

## Key Elements

- **Order List** — each pending order shows:
  - Team name
  - Direction (Buy or Sell)
  - Price limit (the price they want)
  - Quantity
  - Time placed
  - Cancel button

---

## Where Users Go From Here

- Tap Cancel on an order → [[product/pages/trading/cancel-order|Cancel Order]] confirmation
- Back → [[product/pages/trading/portfolio|Portfolio]]

---

## States

- **Has pending orders:** List of orders with cancel buttons
- **No pending orders:** Empty state — "No open orders. Place a limit order from any game page."
