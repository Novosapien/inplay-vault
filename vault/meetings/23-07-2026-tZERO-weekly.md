---
date: 2026-07-23
type: general
scope:
  - "[[tzero]]"
  - "[[integrations]]"
  - "[[primary-offering-execution]]"
  - "[[customer-onboarding]]"
  - "[[market-maker/market-maker]]"
status: extracted
extracted-to:
  - "[[tzero]]"
  - "[[integrations]]"
  - "[[primary-offering-execution]]"
  - "[[customer-onboarding]]"
---

## Post-Call Analysis

Weekly tZERO tech sync the morning after the app landed on the Apple App Store (as "InPlay Challenge", light-beta build). This was a launch-preparation call: the group locked the SIM/PROD environment split, the production symbology strategy, SIM rate limiting, the stock-loan (short) fee, and the biggest decision, the IPO issuance path, which will **bypass the Matching Engine and mint tokens directly to investor wallets** via the transfer-agent workspace. Attendees included Troy McDonald Kane, Rob Colucci, Evangelos Tzoulafis, Chris Russell and Ganesh Pandey (tZERO/InPlay side) plus George, Hasan and Brett (Novo). Two facts here overlap the same-day market-maker follow-up and are already owned elsewhere; they are cross-referenced below, not restated. Targeting an **Aug 6 preseason dry run** and an **Aug 22 sim launch**.

### App Store & environments

- **App released to the Apple App Store** the previous day as a **light beta** used to clear the initial approval. Troy: **future in-app trading will require a second, separate approval round**. Minor updates can be pushed OTA; major changes trigger additional review. Captured in [[tzero]] deployment notes.
- **Environment split locked:** the current environment **becomes SIM**; a **separate PROD environment will be stood up**. Test/dummy assets (named after non-existent teams) live **inside SIM** to allow market-maker and feature testing without new infrastructure. Rob cautioned that heavy testing strains shared resources and should be kept **off the customer-facing side** where possible.

### Symbology

- **Production symbology strategy:** keep the current symbols for SIM but **truncate symbols for production** to meet standards. Front ends can reconfigure display symbols; the backend does not require a specific format. Use **system-generated IDs / descriptive IDs for back-end mapping**, **decoupled from team names** to avoid regulatory issues and naming conflicts across future seasons. A **background mapping is retained for auditing/historical purposes**. Goes to [[tzero]].

### Rate limiting & risk controls

- **SIM rate limiting:** no throttles exist today; tZERO will implement **rate limiters on incoming traffic and order flow** on SIM (particularly for the internal test accounts) to prevent resource exhaustion. George proposed using **custom FIX fields to prioritise live-user orders over test orders** if resources get constrained. Goes to [[tzero]].
- **Account risk parameters:** Rob to send a **list of relevant risk controls / default template settings** to apply to new accounts. Troy noted all users are treated equally with the **same initial capital of 100K**, and that high-frequency messaging is a lesser concern since most users won't have API access. Risk-template defaults are an open item (see below).

### Stock-loan (short) fee

- **Development complete** and functioning in the **segregated environment**. Rate set at **$1.20/share (adjustable)**. **Novo to test:** verify the **FIX tags on the gateway** and confirm **data flows correctly to the blockchain**. Goes to [[tzero]].

### Payments

- **Pay.com** is the leading vendor for **payouts and subscriptions**, with **discussions for a redundant processor** for cash-out optionality. Troy: **no further direction for tZERO required** on payments for launch. New integration recorded in [[integrations]]; cross-ref [[customer-onboarding]].

### IPO issuance (key decision)

- **Adopt a standard primary-issuance model:** the IPO will be treated like a **security with a primary raise**, **bypassing the Matching Engine** and using the **transfer-agent workspace to mint tokens directly to investor wallets** once Novo has the necessary access. The **IPO is long-only at a single price**. This resolves the standing "how does the issuance ledger work" open item on [[primary-offering-execution]] / [[ipo-module]]. Chris Russell and Rob Colucci weighed using the MS to set prices via buy orders vs. bypassing it; the group reached consensus on the direct-mint path. Goes to [[primary-offering-execution]]. **Action:** ensure the team has **minting access rights in the tokenization engine**.

### Reconfirmed (already owned elsewhere, not duplicated)

- **Cancel-replace is synthetic at the FIX gateway and loses queue priority.** Rob confirmed: because cancel-replace is synthetic at the FIX-gateway level, modifying a resting order's price/size makes it a **new order at the back of the queue**. Troy: **common practice on essentially every matching engine**, not tZERO-specific. Already recorded in [[market-maker/decisions]] (T8.1 resolved); this call reconfirmed it.
- **Market maker = a standard user account with much higher buying power**, consuming **Market Data V8**. Owned by [[market-maker/market-maker]]; see the open-questions row on the synthetic MM entity. Not restated here.

### Timeline / next steps

- **Aug 6 preseason dry run** with a focus group (interns + others); Troy to draft an outline for the next Tuesday meeting. George wants it to exercise **Sport Radar push notifications** and **simulated games**.
- **Aug 22** targeted **sim launch**.
- Outstanding tZERO actions: stock-loan-fee internal tests, Rob's risk-control template list, and provisioning **minting access** in the tokenization engine.

---

> **Source:** Gemini summary, _Novosapien ( Rebel Labs) \<\> InPlay \<\> tZERO: Weekly Tech Sync, 2026-07-23_. This is a structured summary, not a full transcript.
