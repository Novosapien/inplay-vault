---
description: "Plain-English definitions for every market-maker term and equation symbol used across the standards, systems docs and calls"
---

# Market Maker — Glossary

> **Component:** [[market-maker/market-maker]]
> **Purpose:** Plain-English definitions for every term and equation symbol
> used across the standards, the systems docs, and the calls. Interactive
> version with clickable equations: `standards/sdmm-machine.html`.

---

## Market basics

| Term | Plain meaning |
|---|---|
| **Bid** | Price the MM (or any buyer) will buy at. Users *sell into* the bid. |
| **Offer / ask** | Price the MM (or any seller) will sell at. Users *buy from* the offer. |
| **Spread** | Gap between best bid and best offer. The MM's margin. |
| **Mid** | Halfway between best bid and offer. Edwin confirmed: the Reference Price sits here. |
| **Two-sided quote** | A live bid *and* offer at the same time — the MM's core obligation. |
| **Quote** | The MM's posted commitment: its resting limit orders, both sides, all levels. Mechanically just limit orders — "quote" flags the *obligation* to keep them there. |
| **Order book** | All live limit orders for one team from everyone (MM + users), sorted by price, two sides. |
| **Depth / ladder** | The levels beyond the best price. Level 0 = best bid/offer; level 1+ = progressively worse prices with more size. |
| **Resting liquidity** | Passive orders sitting in the book waiting to be hit (Edwin's phrase for what the MM posts). |
| **Maker / taker** | Maker posts resting liquidity (the MM); taker crosses the spread to hit it (users, and the Synthetic Noise Taker). |
| **Synthetic Noise Taker (SNT-1)** | The second house agent: a taker-only, non-participant account that crosses the spread with random noise flow so every book trades from IPO onward. A controlled loser by design. See [[market-maker/systems/synthetic-noise-taker]]. |
| **Noise flow** | Uninformative order flow (random direction/size/timing) that creates activity without predicting price. SNT-1 manufactures it. |
| **Disposition effect** | The retail tendency to take profits sooner than losses. SNT-1 mimics it: profit tilts its P(flatten) up to 0.65, losers ride at 50/50. |
| **Crossing / pricing through** | A limit order priced past the other side's best — executes immediately at the resting prices (bid 11 on a 7-at-8 market → fills at 8, 9, 10). Market-order behaviour without market orders. |
| **Price-time priority** | Matching rule: best price first; among equal prices, earliest first. |
| **Locked / crossed market** | Bid = offer (locked) or bid > offer (crossed). Nonsense states — never published. |
| **Inventory** | The MM's net position in a team, as % of the publicly tradable float. Long = bought too much; short = sold too much. |
| **Skew** | Deliberately asymmetric offsets to steer inventory back toward flat (long → offer drops toward RP to attract buyers). |
| **Cancel-replace** | The refresh mechanic: wipe the MM's resting orders, post updated ones. ~5–10×/sec intragame. |
| **Fill / execution** | A match. Arrives back as an execution report; changes inventory. Partial fills are normal — an order fills in chunks. |
| **OrderQty / CumQty / LeavesQty** | An order's three numbers: total · filled so far · still resting. 500 total, 250 filled → 250 resting. Fills survive a cancel-replace (CumQty carries to the updated order). |
| **Queue position** | At one price, resting orders fill first-come-first-served. Whether an update keeps your place or sends you to the back = T8.1. |
| **Pairs trade** | Two correlated symbols traded against each other — every game is one (Troy's frame). |
| **Bust** | Voiding an already-executed trade at a clearly-wrong price; positions/cash reversed by T0 (`ExecType=H`). Operator + venue power, never a participant's. |
| **Band** | Allowed price corridor around the RP (~±30%) — outside it, orders reject or fills get busted. |
| **Halt** | Matching stopped for a team (or all); defensive/pulled quotes until resumed. |

## The three-document stack

| Term | Plain meaning |
|---|---|
| **CTS-001** | Financial Valuation Standard — what a team is worth. Specifies the valuation engine. |
| **CTS-002** | Market Operations Standard — how the market runs around that value. |
| **PTS-001** | The SDMM standard — how the quoting bot behaves. Must obey both CTS docs. |
| **ESV** | Expected Settlement Value — the continuously updated estimate of what a share pays out at season end. The valuation engine's output. |
| **RP — Reference Price** | The ESV republished as the operational price anchor. `RP = ESV` by law; the mid. |
| **IVS** | InPlay Valuation System — the valuation engine (ours to build). |
| **SDMM** | Simulated Designated Market Maker — the quoting bot (ours to build). |
| **PLP** | Production Liquidity Provider — a real MM firm, future state. |
| **Market state** | Edwin's term for the condition/profile layer (MOC + MOP in the docs). |
| **MOC** | Market Operating Condition — health class: Normal · Degraded · Protective · Recovery · Emergency. |
| **MOP** | Market Operations Profile — the target market shape (spread/depth/refresh/protection) for the current condition + session. |
| **Decision Cycle** | One turn of the quoting loop: trigger → assess → price → build → validate → publish → commit. Never overlaps. |
| **Protected Reference Price State** | Valuation feed dies → last valid RP stands frozen; nobody may invent a substitute. |
| **Executable Quotation** | The formal record of the MM's whole posted market for one team: best bid/offer (B, O), their sizes (Q_B, Q_O), the deeper ladder (D), refresh profile (R), status (S), priority (P). |
| **Pricing profile** | A named regime (Stable … Protective) = a row of multipliers scaling spread, depth, size, refresh, inventory sensitivity. Gain scheduling. |
| **Behavioral mode** | The adaptation layer's stance for a cycle (Normal / Active / Recovery / Liquidity-Preservation / Protective). |
| **Economic Component** | CTS-001's representation of one revenue right. Collapses to ~3 per team for us: this game, rest of season, off-field. |
| **Deterministic replay** | Same inputs + version → byte-identical outputs; any past cycle reconstructible. Forces seeded randomness, no wall clocks. |

## Equation symbols (the recurring ones)

| Symbol | Meaning |
|---|---|
| `t` | Time — or the current decision cycle. |
| `i` | Team (issuer) index. |
| `P(win)` | Live win probability for this game (Sport Radar). |
| `$/win` | Revenue value of one win — the core economic constant (TBD, Edwin). |
| `RP_t` | Reference Price at time t (= ESV_t). |
| `BO / OO` | Bid Offset / Offer Offset — total distance from RP to the reservation bid/offer. |
| `BS / OS` | Base spread component per side (the profile's default margin). |
| `IS` | Inventory Skew component = λ × INV. Widens the loaded side. |
| `AS` | Activity adjustment — widens when flow gets fast/aggressive. |
| `PS` | Protection spread component (pricing) — or Protection State (lifecycle contexts). |
| `INV` | Inventory as % of public float. |
| `λ` (lambda) | Inventory sensitivity — the feedback gain, scheduled per profile. |
| `RBP / ROP` | Reservation Bid/Offer Price = RP − BO / RP + OO. The MM's true best prices. |
| `k` | Depth level index; k = 0 is best bid/offer. |
| `Δ` (delta) | Ladder spacing between levels (per side). |
| `ε` (epsilon) | Bounded, seeded price jitter per level. |
| `N` | Number of ladder levels per side. |
| `W` | Depth weight — share of size at level k (Σ = 1 per side). |
| `Q` | Displayed quantity (Q_B bid side, Q_O offer side). |
| `S, D, Q, F, I` | Profile multipliers: spread, depth, quantity, refresh, inventory sensitivity. |
| `EOB` | Executable Order Book — the MM's complete published market for one team. |
| `CFG` | Configuration — the parameter set in [[market-maker/parameters]]. |
| `F(·), G(·), f(·)` | Deliberately undefined functions in the standards — the argument list is the law (what may be consulted); the body is ours/Edwin's to write. |
