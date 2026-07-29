# InPlay Trading Challenge -- Integrations

> **Architecture:** [[architecture]]
> **Status:** Not started

Third-party services, APIs, and data feeds.

## Known Integrations

| Integration | Purpose | Status |
|------------|---------|--------|
| Sport Radar | Real-time sports data, live match tracker, historical stats, news feed | Licensed |
| T0 ATS | Trading engine, price data, order book, trade execution | Partnered |
| Persona | KYC / identity verification | Setup in progress |
| Pay.com (+ redundant processor) | Payouts and subscriptions / cash-out optionality | Vendor selection (23-07) |
| Brokerage Partners | Production trading (future -- not challenge scope) | Future |

> **T0 environments (23-07-2026, _[[23-07-2026-tZERO-weekly]]_):** the current T0 environment **becomes SIM**; a **separate PROD environment** will be stood up. Test/dummy assets (named after non-existent teams) live inside SIM. Payouts/subscriptions route through **Pay.com (+ redundancy)** and need **no tZERO direction** for launch. Full T0 deployment notes in [[t0]] §10.

> **T0 OMS Q&A + risk settings (29-07-2026, _[[29-07-2026-tZERO-rob-qa]]_):** Rob Colucci answered the OMS testing questions and delivered the IPLY risk-settings matrix ([[tzero-oms-risk-settings]]). Highlights: IPLY accounts **carry positions overnight**, account-scoped position tracking is **fixed** (was a TEST-credential routing bug), bid/ask is **driven by FIX orders** (market maker sets the market), ticker `IPTCCONH` is **created in OMS SIM**, and **Stop Wash Trades is ON**. Primary-issuance metrics belong on a **dedicated cap-table stack**, not the OMS. Detail in [[t0]] §11.

## Sport Radar: feeds, probabilities API, contract (24-07-2026)

Source: [[24-07-2026-touchdown]]. Additive detail on the SR relationship surfaced routing the gamecast speed question.

- **Two distinct SR feed families, different speeds and use cases:**
  - **Media data feeds** (what InPlay has licensed) power the **custom Gamecast** ("the pretty one"). For concluded games it is a normal API fetch; for live games it fetches the pre-event history then **streams events** as they happen.
  - **Betting data feeds** (the "ugly" licensed **live match tracker**) run off **betting data**, which is materially **faster** than the raw media feeds. The two feeds are built for two different use cases.
- **Access constraint (important):** SR sells the **betting feeds only to licensed sports books**. InPlay is **not** a licensed sports book, so it **cannot access the betting APIs** today, even though the licensed match-tracker widget renders off them. Cody: the widget only updates its own UI, it does not ping InPlay a request InPlay could consume.
- **Decision:** use the **fastest available feed** for the visual and for pricing signal, since latency must be TV-competitive so traders are not "picked off" (Edwin). The **delta** between a real-world event and SR delivering it is **not controllable** (it is whenever SR sends it); George to check whether the API exposes both event-time and delivery-time.
- **Probabilities:** the win/other probabilities InPlay wants are computed off the **betting feed** (faster). Interim solution runs off the **media probabilities API**. Probabilities are the **most valid reference signal** (they move first, then InPlay extrapolates price from them). See [[market-maker/market-maker]] for how the MM consumes probability (MM-owned, not restated here).
- **Probabilities-API issues to resolve (George → SR support email; Cody to align with Scott + David):**
  - Probabilities API is **not in the production environment** (SR has dev vs prod); currently only **probabilities v1**, with a **~1,000/month quota**.
  - Likely need **Global American Football Probabilities v2** (a different sports package than the trial key unlocks): v2 has a **bulk probability endpoint** that batches all teams into **one call** (~every 200 ms during a game) instead of ~170 separate calls, cutting query volume from ~2.5M to ~1M/month.
  - Cody: SR has moved to **one master API key that forks into all products** (versioning "no longer matters"; API-call counts "mean nothing" at real-time levels, effectively unlimited). But some queries with the master key return **not-authenticated** because the product (e.g. global American football probabilities) is **not allocated to InPlay's SR account**, which is the fix to chase commercially.
- **Contract:** **1 year**. Cody expects a natural price rise at renewal but not large, as sports are added (~6–10 more); SR will **never do an exclusive** (they serve ~900 sports books, "the Switzerland of everything"). Adding sports + unlocking the **betting feeds** are the **levers** for a longer-term deal. Cody is lobbying SR (call early next week) that InPlay is **more regulated than a sports-betting or prediction market**, to obtain the betting feeds in parallel.
