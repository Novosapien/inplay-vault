---
description: "Page spec for the Wallet Details screen — trading wallet (100K cap) vs uncapped referral wallet, and the combined transaction history"
---

# Wallet Details

> **Tab:** Trade
> **Purpose:** Breakdown of wallet balances and transaction history.
> **Map:** [[product/pages/PAGES|App Pages]]

---

## What Users See

Full detail on where the user's InPlay dollars came from and how they've been spent. Two separate wallets with different rules.

---

## Key Elements

- **Trading Wallet** — the main capital used for buying and selling team stocks
  - Current balance
  - Cap reminder (100,000 InPlay dollars maximum)
  - Recent transactions (trades that affected this balance)

- **Referral Wallet** — bonus capital earned from referrals
  - Current balance (no cap)
  - Source breakdown (which referrals earned what)
  - Separate from trading wallet — may have different withdrawal rules

- **Transaction History** — combined log of all balance changes:
  - Trades (buys reduce balance, sells increase it)
  - Referral credits
  - Bonuses or promotions
  - Starting allocation

---

## Where Users Go From Here

- Back → [[product/pages/trading/portfolio|Portfolio]]

---

## States

- **New user:** Starting balance shown, no transaction history
- **Active user:** Full transaction history with running balance
