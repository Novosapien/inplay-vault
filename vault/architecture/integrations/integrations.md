# InPlay Trading Challenge -- Integrations

> **Architecture:** [[architecture]]
> **Status:** In progress

Third-party services, APIs, and data feeds.

## Known Integrations

| Integration | Purpose | Status |
|------------|---------|--------|
| Sport Radar | Real-time sports data, live match tracker, historical stats, news feed | Licensed |
| T0 ATS | Trading engine, price data, order book, trade execution | Partnered -- integration active (see state below) |
| Persona | KYC / identity verification | Setup in progress |
| Brokerage Partners | Production trading (future -- not challenge scope) | Future |

## tZERO Integration State _(from [[meetings/12-07-2026-tZERO-questions-answered]])_

**Environments.** There is no sim-to-prod transition: the current segregated sim environment IS the live platform for the football challenge and gets promoted to prod. A fresh QA/staging environment is being stood up (Rob assessing feasibility against the **Aug 22 live target**), doubling as the staging ground for the October basketball challenge. The Onboarding API may move staging -> demo (Eric confirming). tZERO multi-tenancy: new issuer per environment/sport, scoped API keys. InPlay is on QA for FIX trading and Staging for the Onboarding API.

**Wallets.** Two blockchain wallets per user: one long, one short, same token (avoids bifurcating execution liquidity; makes long-vs-short legible; wallets are not a cost centre). Legacy trades missing wallet addresses are auto-assigned to the treasury wallet short-term; production pre-creates lots with known treasury wallets. The order simulator does not pass wallet addresses -- simulated orders go to a general placeholder wallet.

**Market and liquidity.** Sim order book runs on an order simulator across six NFL symbols (no real participants yet); six college football symbols were added and are pending confirmation (Chris). For the challenge, **Edwin is the designated market maker** -- the only API-connected trader; everyone else trades through the app, with API access opening in production. Edwin provides two-sided markets; participants can still add passive liquidity.

**Accounts and reconciliation.** Account onboarding: create account via API -> account number returned -> flows to the FIX session -> orders can be placed (Eric walking Hasan through the FIX message flow on Slack). End-of-day Account/Position files from Rob are the reconciliation mechanism (buying power + positions per account). Buying power resets at midnight tZERO-side; enabled in sim but one clearing-software connection piece is pending. Buying-power updates can be sent via the existing FIX OE session. The cap-table management API (blockchain layer) exposes per-customer balances and corporate-action APIs -- FIX/OMS remains the primary route; Eric setting up Hasan/George on the portal.

**Commercial/ops.** Commissions (long + short side, simulator) settled. Payouts deferred to the Tuesday call. Architecture diagrams requested from tZERO for Novo's development context. Previous tZERO stand-up recordings to be shared for knowledge-base ingestion.

**Still open:** DAY/GTC time-in-force confirmation (asked, unanswered -- see [[open-questions]]), EOD file cadence and filename convention, AccNUMB assignment rules in SIM, and whether the SIM OMS can book trades it did not execute.
