# Synthetic Market Order

> **Component:** [[market-maker/market-maker]] · ships in [[trading/trading]]
> **Status:** New build item (20-07) — **Edwin wants it before the first NFL game (~09 Sep)**
> **One-liner:** tZERO has no market orders. Users expect a "just buy it" button. We fake it app-side the way real brokers do: a limit order priced through several levels.

---

## The Problem

- tZERO supports **limit orders only** — a user must name a price. (Source:
  standup 2026-07-20; Troy: "there actually aren't market orders on tZERO")
- Casual users placing a limit at a stale price will miss the market and get
  frustrated. Edwin: "we don't want the user experience to be frustrating."
- Fun fact from Troy: even in real equities, market orders barely exist —
  brokers synthesize them exactly this way.

## The Mechanic

**Price-through:** when the user taps "buy at market", the app submits a limit
order priced several levels through the book, which fills at the best
available prices anyway (a limit crossing the spread executes at the resting
prices, not the limit price).

> Edwin's example: market is 6 bid at 7 → a buy priced at 12 fills at 7, 8,
> 9… whatever's resting, best-first. "It's going to fill you at the best price
> anyway."

Mechanics to decide:

- **How many levels through** — Troy: take the current bid/offer and add/
  subtract N price levels (CME/broker style). N is a parameter.
- **Fallback walk (George's proposal):** if unfilled after a few seconds,
  cancel-replace at a better price and chase until filled — time-bounded.
  Probably unnecessary if N is generous, but useful in fast markets.
- **No user-facing bounds:** Edwin was explicit — "a market order means
  whatever you get, you get," until exhausted or no market.

## Interaction With the Price Band

A synthetic market order sweeping a thin book is exactly how an out-of-band
fill happens (the fill-at-85-on-a-6/7-market example). Two protections must
compose:

1. The price-through depth N caps how far a single order can sweep.
2. The band ([[market-maker/systems/market-supervision]]) catches anything
   that still prints outside it → bust.

Design the two together — N should keep fills comfortably inside the band in
normal depth.

## Ownership & Placement

- **Specced here** (it exists because of MM/venue mechanics) but it's an
  **app-side feature in the Trading component's order-entry flow** — likely
  Trading Service logic, not the SDMM.
- Troy offered to help write the logic.
- UX: present as "Market" order type in the app; under the hood it's
  limit-priced-through. Users never see the synthetic price.

## Open Items

Tracked in [[market-maker/open-questions]]: N (levels through), fallback-walk
yes/no + time bound, behaviour in a halted/empty book, interaction with the
trading wallet balance check (worst-case fill price vs available balance).
