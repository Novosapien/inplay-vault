---
description: "Register of third-party integrations — Sportradar, tZERO ATS, Persona, Pay.com — with SR feed/probabilities/contract detail and tZERO SIM/PROD notes"
---

# InPlay Trading Challenge -- Integrations

> **Architecture:** [[architecture]]
> **Status:** Not started

Third-party services, APIs, and data feeds.

## Known Integrations

| Integration | Purpose | Status |
|------------|---------|--------|
| Sport Radar | Real-time sports data, live match tracker, historical stats, news feed | Licensed |
| tZERO ATS | Trading engine, price data, order book, trade execution | Partnered |
| Persona | KYC / identity verification. **Two paths as of 07-08**: US tax resident, and non-tax-resident identity-only | Setup in progress |
| Pay.com (+ redundant processor) | Payouts and subscriptions / cash-out optionality | Vendor selection (23-07); **still unresolved 03-08**, merchant application reassigned to Edwin |
| **Avalara** | W-9 tax-form automation for cash withdrawals. **Middle-ground embed integration chosen 03-08**: one line of embed code on an InPlay-branded landing page, hyperlinked out of the app. Full in-app SDK deferred | ✅ Selected (03-08) |
| **AdMob** (Google) | Primary ad SSP. Verified and serving 27-07 | ✅ Live |
| **AppLovin MAX** | Second ad SSP | 🟡 Application chasing, warm intro sought |
| **Kochava** | Mobile measurement partner (MMP). Chosen over AppsFlyer 29-07 on price (~1/5 to 1/10). ⚠ **No direct AdMob integration** — workaround required | 🟡 Direction set, call pending |
| Brokerage Partners | Production trading (future -- not challenge scope) | Future |

> **tZERO environments (23-07-2026, _[[23-07-2026-tZERO-weekly]]_):** the current tZERO environment **becomes SIM**; a **separate PROD environment** will be stood up. Test/dummy assets (named after non-existent teams) live inside SIM. Payouts/subscriptions route through **Pay.com (+ redundancy)** and need **no tZERO direction** for launch. Full tZERO deployment notes in [[tzero]] §10.

> **tZERO OMS Q&A + risk settings (29-07-2026, _[[29-07-2026-tZERO-rob-qa]]_):** Rob Colucci answered the OMS testing questions and delivered the IPLY risk-settings matrix ([[tzero-oms-risk-settings]]). Highlights: IPLY accounts **carry positions overnight**, account-scoped position tracking is **fixed** (was a TEST-credential routing bug), bid/ask is **driven by FIX orders** (market maker sets the market), ticker `IPTCCONH` is **created in OMS SIM**, and **Stop Wash Trades is ON**. Primary-issuance metrics belong on a **dedicated cap-table stack**, not the OMS. Detail in [[tzero]] §11.

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

## Sport Radar: resolved (03-08-2026)

Source: [[03-08-2026-touchdown]], with the problem statement from
[[27-07-2026-touchdown]]. **This closes most of the 24-07 section above.**

- ✅ **The probabilities contract amendment is signed**, at **no change in
  cost**, and live probabilities are **in the production account**. Cody, asked
  whether a deal still had to be worked out: _"Done."_ Troy signed; a DocuSign
  lag meant he had not yet received his copy on the call.
- ✅ **Quota is no longer a constraint.** Edwin: _"there's no limit on
  requests."_ Cody: _"I'm not worried about the API call limits."_ This retires
  the 27-07 worry, where polling every 2 seconds implied **8–10M requests a
  month** and a v2 bulk endpoint was being chased to cut it to ~800k–1M. The
  binding question became **how fast the probabilities actually refresh**, not
  how many calls are allowed.
- ✅ **The betting feed is NOT being bought for this run.** It buys faster
  play-by-play only, and the **gamecast already runs off the betting feeds** via
  the licensed live match tracker. Edwin: _"we don't need anything over and
  above the gamecast and the live probability."_ Cody is keeping the
  conversation open with SR for later. ⚠ Consequence: no faster path has been
  purchased, so probability lag versus DraftKings and FanDuel is now purely a
  function of SR's odds ingestion (S4 in [[market-maker/open-questions]]).
- ✅ **Probability is a separate poll, never in the play-by-play payload.**
  Confirmed twice (Cody, 27-07 and 03-08). The push feed carries the event
  ("five yards gained by the Chiefs") but not the probability change it caused,
  so it must be fetched on our own clock. Fetching it **at event time** was
  rejected because the extra network request slows the hot path.
- ✅ **Poll cadence: 500ms in-game** to start, tuned from there (Edwin).
  Outside games it is polled more slowly but **still polled**, because the
  market taker makes markets 24/7 — Edwin overruled George's instinct to stop
  entirely: _"it does need to be called because there will be active market
  participation."_
- ✅ **Next-game probabilities post ~15 minutes after the previous game ends**,
  typically faster (Cody: _"we always said 15 minutes to cover our asses"_).
  They are an extrapolation of the posted odds — a 3-point favourite is roughly
  a 65% winner — so the moment the line posts, probability can be pulled. In
  the gap the prior feed value carries. Probabilities are **not** published
  continuously between games.
- 🔴 **Still open: what counts as a "key player."** SR sell facts, not
  subjective impact ratings. The nearest primitive is the **depth chart**. See
  [[information-layer/sub-components/team-page/team-page]].

## Own probability model (plan B)

Raised 27-07, developed 31-07. Not a launch item; recorded because it is
strategically load-bearing.

The idea is to stop depending on Sport Radar for win probability and compute it
in-house from a **traditional ML model** (explicitly not an LLM — George:
_"it's just outputting a probability, it's not like training an LLM"_) trained
on **NFLverse**, a free dataset covering every NFL event and result **since
1999**. Edwin's view is that precision is not required: _"they don't have to be
exact. In fact, the inexactness is probably going to be compelling for
traders."_ He took an action to attempt a rudimentary interim model himself.

George's assessment: **not possible before launch.** Cody's and Edwin's: worth
doing anyway, because it converts a licensed dependency into **proprietary IP**.
Edwin's 31-07 extension is the commercial case — once live, back-test past
seasons against actual share prices to learn which events move fair value, then
license the output: _"I can see where Kalshi, Polymarket, all the sports books
would want to license our proprietary data feed. It's not a probability feed,
it's actually a price feed that they can translate into betting odds in real
time."_
