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
