---
date: 2026-07-29
type: general
source: Written Q&A from Rob Colucci (tZERO), following a QA testing session with Novo (Hasan)
scope:
  - "[[t0]]"
  - "[[tzero-oms-risk-settings]]"
  - "[[primary-offering-execution]]"
  - "[[market-maker/market-maker]]"
status: extracted
extracted-to:
  - "[[t0]]"
  - "[[tzero-oms-risk-settings]]"
  - "[[primary-offering-execution]]"
  - "[[integrations]]"
  - "[[open-questions]]"
---

## Post-Call Analysis

Written answers from **Rob Colucci (tZERO)** after a QA testing session with Novo (Hasan), plus follow-up testing tZERO ran the same day. Covers primary issuance, overnight position carryover, position-scoping, market-data pricing, and ticker setup, and ships the **OMS risk-settings matrix** for IPLY (captured in [[tzero-oms-risk-settings]]). Two issues were fixed live during the session (account-scoped positions, ticker `IPTCCONH`). Date is receipt date; the session date is not stated in the notes.

> **Process note:** Rob asked to run real-time troubleshooting through the shared **Slack channel** and to schedule **QA sessions** when needed, to streamline testing and issue resolution.

### Primary issuance flow (OMS vs cap table)

- **Question:** send IPO orders through the OMS, or issue directly to the cap table?
- **Answer:** the OMS (secondary-trading environment) **can** set preliminary IPO prices by placing **BUY orders at set prices**; those orders rest on the book and become eligible for execution. The OMS **Previous Close Price** can be set as the **"IPO Reference Price"** for Market Data and Risk Management. **But** to track **primary-issuance metrics** (total capital raised, shares remaining available) the challenge should use a **dedicated cap-table management tech stack**.
- **Reconciliation:** this is consistent with the 23-07 decision to **mint directly to investor wallets via the transfer-agent workspace** (see [[t0]] §10.6 and [[primary-offering-execution]]). The OMS seeds a reference price for market data and risk; the **cap table is the system of record for issuance metrics**. Selecting/building that cap-table stack is a new open item.

### Position carryover and risk settings

- **Positions can be configured to carry or flatten overnight; IPLY accounts carry overnight by default.** The earlier "shares reset to 0" behaviour was a side effect of the firm-account credential issue below, not the intended config.
- Rob delivered `tZERO_OMS_Risk_Settings_Matrix_IPLY.xlsx` to align on risk-flag configuration. Captured in [[tzero-oms-risk-settings]].
- **Do not** restore positions by injecting Tag 9381 (Qto) / Tag 9382 (Eto) via UEPR on a user's first order of the day. Rely on automatic carry-over. Editing position criteria on order messages risks **race conditions** in risk management. Use UEPR only when deliberately modifying an account holder's position criteria.
- **UEPR and UEAR are both enabled** for account/position updates via the Order Entry Service. There is **no direct query to retrieve all account positions at once**. Using Edit Account Requests for EOD reconciliation is a **non-standard workaround**; if relied on heavily, set up a **dedicated session isolated from live order-entry messaging**.

### Account-level position aggregation (fixed)

- **Question:** positions aggregated at firm level rather than per account (Tag 1). Intended?
- **Cause:** the test accounts were onboarded with **TEST-environment credentials**, so they were never created in STAGE and passed into OMS SIM; all trades fell back to a **default firm account** (which was also set to not carry positions).
- **Update (fixed live):** tZERO and Novo corrected the **credential routing** during the QA session and verified the full account-onboarding flow. **Account-scoped position tracking now works as expected.**

### Market data, pricing and tickers

- **Bid/ask prices in the order book are driven by FIX orders.** Typically a **market maker maintains liquidity and sets the market**, operating alongside organic user order flow. (Confirms the internal-MM design, owned by [[market-maker/market-maker]].)
- **Ticker `IPTCCONH`** showed as invalid because it was **missing from the OMS SIM asset setup**. **Update (fixed):** it has now been **created and configured in OMS SIM**.

### Items flagged for the market-maker workstream (not written into the MM component here)

- **Self-match / wash prevention:** the OMS has **Stop Wash Trades ON** at account level (scans live orders for opposite-side at matching/crossed prices). This answers the MM's self-match-prevention question.
- **Price band:** the OMS **Enforce Limit Price Range %** tiers (see [[tzero-oms-risk-settings]]) are the OMS-level price band; reconcile against the MM quote-bust design and the synthetic-market-order price-through logic.
- **Crossing allowed:** **Reject Crossed Orders is OFF**, so limit orders may cross (supports synthetic market orders and MM crossing).
