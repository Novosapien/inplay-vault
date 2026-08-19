---
description: "Page spec for the Trade Confirmation review screen — order summary, wallet impact, market vs limit states, and the insufficient-balance disabled state"
---

# Trade Confirmation

> **Tab:** Trade
> **Purpose:** Review screen before submitting an order — last chance to check details.
> **Map:** [[product/pages/PAGES|App Pages]]

---

## What Users See

A summary of the order they're about to place. Everything laid out clearly so they can confirm or back out.

---

## Key Elements

- **Order Summary:**
  - Team name
  - Direction (Buy or Sell)
  - Quantity (number of shares)
  - Price (market price or limit price)
  - Total cost or proceeds
- **Wallet Impact** — balance before and after the trade
- **Confirm Button** — submit the order
- **Cancel / Back** — abandon the trade, return to previous screen

---

## Where Users Go From Here

- Tap Confirm → [[product/pages/trading/order-placed|Order Placed]] (success screen)
- Tap Cancel → back to previous screen ([[product/pages/discover/single-game-page|Single Game Page]], [[product/pages/discover/team-page|Team Page]], or [[product/pages/trading/portfolio|Portfolio]])

---

## States

- **Market order:** Shows current market price, notes it may vary slightly at execution
- **Limit order:** Shows the exact price specified by the user
- **Insufficient balance:** Confirm button disabled, warning shown
