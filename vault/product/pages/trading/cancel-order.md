# Cancel Order

> **Tab:** Trade
> **Purpose:** Confirmation before cancelling a pending order.
> **Map:** [[product/pages/PAGES|App Pages]]

---

## What Users See

A confirmation step before removing a pending limit order from the book. Prevents accidental cancellations.

---

## Key Elements

- **Order Details** — the order being cancelled (team, direction, price, quantity, time placed)
- **Confirm Cancel** — removes the order permanently
- **Keep Order** — go back without cancelling

---

## Where Users Go From Here

- Tap "Confirm Cancel" → order removed, returns to [[product/pages/trading/open-orders|Open Orders]]
- Tap "Keep Order" → returns to [[product/pages/trading/open-orders|Open Orders]] (order unchanged)

---

## States

Single state — always shows the order details and two action buttons.
