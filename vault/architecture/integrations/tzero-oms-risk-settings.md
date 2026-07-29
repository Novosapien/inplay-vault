# tZERO OMS Risk Settings (IPLY defaults)

> **Integration:** [[t0]] · [[integrations]]
> **Source:** `tZERO_OMS_Risk_Settings_Matrix_IPLY.xlsx` (Rob Colucci, tZERO), delivered with the [[29-07-2026-tZERO-rob-qa]] Q&A. Copied into the vault at `sources/tZERO_OMS_Risk_Settings_Matrix_IPLY.xlsx` (beside this doc).
> **Status:** Reference. These are the **default OMS risk-flag settings for IPLY** (the placeholder MPID for InPlay) accounts in SIM. Final configuration to be aligned with tZERO.

---

## What this is

The OMS applies a per-account matrix of pre-trade and post-trade risk flags. This doc records the **IPLY default configuration** so the team can align on how each flag should be set for the challenge. The full matrix is 63 settings; the ones that shape the challenge are called out below. The spreadsheet is the authoritative source.

## Settings that shape the challenge (ON)

| Setting | Value / threshold | Why it matters for InPlay |
|---------|------------------|--------------------------|
| **Is Margin Account** | ON | Required to allow short sales and short-sale-exempt orders. |
| **Margin Multiplier** | ON, set to **1x (cash-equivalent)** for IPLY | Accounts behave as cash accounts; no real leverage at launch. |
| **Release DTBP for covering initial positions** | ON | Frees buying power when closing an overnight position. Requires clearing-firm approval. |
| **Enable UOD (Unacknowledged Order Debit)** | ON | Risk is calculated for orders before the exchange fully processes them. |
| **Base Route Permissions** | ON, default **STX Matching Engine Route** (SIM) | Default destination for unlinked IPLY accounts. |
| **Short List Lookup** | ON (easy-to-borrow list) | Short sales are rejected for symbols not on the uploaded ETB list, or when borrow quantity is exhausted. Relevant to the market maker's short-locate exemption. |
| **Enable Account/Symbol Rule Controls** | ON | Per-account legal/regulatory rule table (affiliate, Rule 144, etc.). If enabled but an account is not defined on the backend table, it is effectively disabled. |
| **Enforce Limit Price Range % Aggressive** | ON (see tiers below) | The **price band** on taker-side limit orders. See below. |
| **Enforce Limit Price Range % Passive** | ON (see tiers below) | The price band on maker-side (resting) limit orders. |
| **Stop Wash Trades** | ON | Prevents trading against your own open orders (scans live orders for opposite-side at matching or crossed prices). This is the **self-match prevention** the market maker needed. |
| **Max Order Rate** | ON, **100 orders/sec** | Caps order submission rate; prevents flooding. |
| **Max Duplicate Order Rate** | ON, **20 duplicate orders/sec** | Blocks rapid identical orders (same symbol, side, order type). |
| **Stock Loan Fee** | ON | Calculates the stock-loan fee on short-sale orders in live buying-power (ties to the **$1.20/share** short fee, see [[t0]] §10.5). |
| **Enforce Day Trading Buying Power** | ON (alerts only) | Buying power from order cost, open positions, and realized P/L. |

## Settings deliberately OFF (challenge-relevant)

- **Don't Carry Overnight Positions: OFF**, i.e. IPLY accounts **carry positions overnight** (the intended behaviour; see the Q&A). Zero Buying Power Overnight is also OFF.
- **Reject Crossed Orders: OFF**, so buy orders priced above the ask / sell below the bid are allowed to cross. Relevant to synthetic market orders (which price through the book) and to the market maker crossing.
- **Liquidate Only / Stop All Orders / Test Stocks Only: OFF** (no account freezes at launch).
- Most hard caps are **OFF**: Max Quantity/Contracts/$-per-order/Notional/Open-orders/Positions/Position-size, Max Loss per account and per position, Enforce Percent Equity.
- Market-manipulation guards **OFF** at launch: Prevent Spoofing, Enforce Layer Limit, Layering Limit per exchange, Enforce Min ADV (and ADV % variants).
- **Prevent Pre-Open / Post-Close Trading: OFF** (no session-time blocks).
- Allow All Long Sales, Allow Riskless Allocation, Allow Naked Options, Allow Prime Locate, Stop Short Sales Against the Box, Stop Short Sale Exempt: **OFF**.
- Compute Order Commission: OFF (no live commission in buying power).

## Limit Price Range % (the price band)

Both aggressive (taker) and passive (maker) limit-price-range enforcement is ON, with four price tiers and separate core vs pre/post-market thresholds. A limit order priced further than the threshold away from the market price is blocked.

| Price range ($) | Aggressive, Core % | Aggressive, Pre/Post % | Passive, All % |
|-----------------|-------------------|------------------------|----------------|
| 0 to 1 | 14 | 24 | 95 |
| 1 to 25 | 10 | 20 | 90 |
| 25 to 50 | 5 | 10 | 85 |
| 50 and up | 3 | 6 | 80 |

**Reading it:** for a security priced $25 to $50, an aggressive (taker) limit order may sit at most **5%** away from the market in the core session; a passive (resting) order may sit up to **85%** away. This band is the OMS-level equivalent of the market maker's "price band / quote-bust" control. The market-maker workstream should reconcile its own price-band and quote-bust design against these OMS tiers (its own open item, tracked under `market-maker/`).

## Open items

- **Align final IPLY risk-flag configuration** with tZERO (this matrix is the starting default, not the confirmed final set).
- **Release DTBP** needs clearing-firm approval to avoid margin calls on overnight covers.
- The **price-band tiers** need reconciling with the market maker's quote-bust procedure and with the synthetic-market-order "price-through" logic in [[t0]].
