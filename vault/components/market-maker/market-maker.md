# InPlay Trading Challenge — Market Maker

> **Vision:** [[vision]]
> **Date:** 2026-07-20
> **Status:** Collecting
> **Owner:** Kevin Murray (Head Execution Trader) / George Westbrook (engineering) / Edwin (co-build, domain expertise)
> **Sources:** _[[12-06-2026-touchdown]], [[15-06-2026-touchdown]], [[17-06-2026-touchdown]], [[24-06-2026-touchdown]], [[29-06-2026-touchdown]], [[15-07-2026-touchdown]], [[17-07-2026-touchdown]], [[20-07-2026-touchdown]]_

> ⚠️ **Partially scoped — not a formal deep-dive.** This component was promoted from a candidate `trading/market-maker` sub-component on 20-07-2026 after the market-maker Q&A session with Edwin and Troy. Content below is consolidated from standup discussions, not a dedicated component session. The focused deep-dive is scheduled for **Thursday 23-07, 3–4pm London**.

---

## 1. What Does This Component Do?

The Market Maker is an **internal, non-user-facing** market participant operated by InPlay. It posts **resting liquidity** — passive two-sided bid/ask limit orders — into T0's order book for every team market, so that from a user's perspective there is always a potential to buy and always a potential to sell. It is not a required counterparty: user orders that match each other fill directly; the market maker's orders are simply always there alongside them. (Source: standup 2026-07-20)

Its jobs, in priority order for the trading challenge (profit-seeking is explicitly at the bottom during the challenge):

1. **Maintain stable, orderly market conditions** — two-sided liquidity in every market
2. **Guarantee IPO fill** — warehouse unsold primary-offering float so no offering reads as zero sales (see [[ipo-module/ipo-module]])
3. **Generate market data** — the challenge run produces the behavioural dataset used to model risk tolerance, spread tightness, and depth, and to pitch production market makers

In production the hierarchy flips: if InPlay becomes its own market maker (Edwin: open another company and do it themselves if external MMs won't sign at acceptable terms), **profitability moves to the top**. (Source: standup 2026-07-20)

---

## 2. What We Know

### Entity model

- The market maker is a **synthetic market-maker entity inside T0** — technically the same as a user account, with two differences: effectively **unlimited buying power** (capital set to ~$100M+, "never a limit"), and **exemption from short-locate restrictions** (as a designated market maker providing liquidity, it doesn't have to locate shorts the way ordinary participants would in production). (Source: standup 2026-07-20)
- In production, designated market makers also tend to receive favourable risk/clearing treatment (membership capital buffers → more risk for less). (Source: standup 2026-07-20)
- Whether the synthetic MM persists into production as one of many participants is **undecided** — depends on how the football/basketball simulation goes and whether external MMs sign. (Source: standup 2026-07-20)
- **Ask in flight:** T0 to stand up the synthetic MM entity (with the unlimited buying power) in the **QA environment** so testing can start — raised for the new Tue/Thu T0 tech calls. (Source: standup 2026-07-20)

### Quoting mechanics

- **Market state** (Edwin's correction — not "market conditions") is the input set that determines the orders the MM sends to T0's book: spread plus ~five other variables driving pricing levels and order quantities. (Source: standup 2026-07-20)
- **Reference price = the mid** between best bid and best ask (confirmed by Edwin). Quotes are built as **base spread ± bid offset / ask offset** around the reference price. (Source: standup 2026-07-20)
- **Skewing:** the spread is not always symmetric. If the MM is long heavy inventory, it lowers its offer toward/at the reference price so buyers come in and it can offload. (Source: standup 2026-07-20)
- **Randomizer:** a condition where quoted sizes are randomized so the book doesn't read as a machine (no 500/500/500 lots — reinforces the 17-07 note). Occasionally a randomized **aggressive order** deliberately moves the market: e.g. long 50k wanting to be long 10k → buy another 10k aggressively, rip the price higher, then sell the (now 50k) excess into the backfilled higher prices. (Source: standup 2026-07-20)
- **Limit orders only** — everything stays a limit order, but a limit order can **cross**: if the market is 7 bid at 8 and you want filled up to 10, you bid 11 and sweep 8, 9, 10. Market-order behaviour without a native market-order type. (Source: standup 2026-07-20)

### Quote cadence

- **Cancel-replace regime:** the MM constantly wipes and replaces its quotes — "liquidity lag". Baseline expectation ~**5–10 times per second** (millisecond regime), plus **event-triggered recalculation** (touchdown → recompute now, then resume baseline). It does not wait to be traded against; it moves quotes on game action and market action. (Source: standup 2026-07-20)
- **Three liquidity sessions** with different profiles: in-game, around-game, and overnight/outside games — overnight the MM goes deliberately wide (e.g. ~$5 spread) rather than quoting tight into nothing. Exact profiles TBD. (Source: standup 2026-07-20)

### Event triggers and learning

- There is **no objective "big play" classification** — Sport Radar data is factual but materiality is subjective (a sack on 3rd down ≠ a sack on 1st down; garbage-time yards mean nothing). Cody: a prior Sport Radar content exercise produced ~40 qualifying data points, but the subjectivity remains. (Source: standup 2026-07-20)
- The MM therefore reads **order flow / investor behaviour** as much as event data: sell pressure → walk quotes down; touchdown → walk quotes up. Event weights start as guesses (touchdown = 0.5) and are **learned from observed market reaction** over time — the first few weeks of games are expected to be volatile on both sides while the model calibrates. (Source: standup 2026-07-20)
- Sport Radar **live win probabilities** (built on ~20 years of historical data) are available as a forecasting input. (Source: standup 2026-07-20)
- **Edwin has a prior trigger script** from the simulated games run ~2 years ago (Kevin believes a full script exists) — needs digging up. (Source: standup 2026-07-20)
- Open question flagged for Edwin: how to value **week zero of college football** (blowout mismatches) in the algorithm. (Source: standup 2026-07-20)

### Price inputs — CTS1 / CTS2

- **InPlay builds CTS1 and CTS2** — they are not consumed from T0. (Source: standup 2026-07-20)
- Two main price drivers: (a) the probability for **the game happening right now**, and (b) the probability across **all other remaining games combined** → together the on-field revenue; add **off-field revenue** → the share price. Off-field is not guaranteed per game, which keeps the market interpretive and tradeable. (Source: standup 2026-07-20; extends the 17-07 reference-price blend note)

### Market isolation

- Each team is its own market; a game is effectively a **pairs trade** (two team companies trading against each other on the probability of capturing the ~$5 on-field revenue). (Source: standup 2026-07-20)
- Markets are **truly isolated intra-game**: events in other games do not move this market during play. Rankings/tiebreakers don't feed pricing (no goal-difference analogue; earnings are on-field revenue capture + off-field, and the challenge doesn't run into the playoffs). Cross-game effects only arrive **between** games, via updated win probabilities for future matchups. (Source: standup 2026-07-20)

### Orderly-markets controls

- **Price band + quote busting:** a trading band (~30% correction, exact number TBD) around which the exchange (InPlay with T0) can **bust trades** that fill outside it — e.g. a crossing order filled at 85 on a 6-7 market. Required to maintain orderly markets; mass bad fills would destroy participation. Detail deferred to the coming days' sessions. (Source: standup 2026-07-20)

### IPO fill / warehousing

- The MM **warehouses unsold IPO float in max clips (~50k)**, guaranteeing ~35% (possibly up to 50%) of every float is consumed — it *is* the straw-buyer mechanism from the 17-06 inventory-visibility discussion. (Source: standup 2026-07-15; see [[ipo-module/ipo-module]] and [[architecture/open-questions]])

### Operations UI

- MM operations run on a **desktop version of the challenge app** — built for the market maker first, before any user-facing desktop rollout. Needs: set/modify algo parameters, order lookup, moderate orders, positions and P&L. The MM is "any other participant, with more capabilities", so the UI is the existing app plus a few components. Kevin likely operates it. Sequenced last — after the backend trading stack is done. Brett's warning: first cut will be rough. (Source: standup 2026-07-20)

---

## 3. What We Don't Know

- The full **market-state variable set** and the equations behind it (George working through Edwin's foundational docs — the PTS/CTS series — mapping them into something buildable)
- Exact **quote cadence** numbers and the three session liquidity profiles
- The **price-band percentage** and quote-bust procedure with T0
- Event **trigger weights** and the learning/calibration approach (initial script vs learned model)
- Whether the synthetic MM **persists in production** and the external-MM signing strategy
- **Load-balancing algo vs market-making algo** split (two pieces named 17-07) — boundaries unclear
- MM ops UI scope beyond the basics (parameters, order lookup, P&L)
- How **week zero college football** is valued
- Sub-component decomposition — candidates (plain text, not yet documented): quoting engine, price/valuation engine (CTS1/CTS2), event-trigger engine, ops desktop UI, T0 entity integration

---

## 4. Next Steps

- **Thursday 23-07, 3–4pm London** — market-maker deep-dive with Edwin (moved from Tuesday to allow a couple of days' prep)
- George: work through the remaining foundational PTS/CTS documents and map the mechanics (as done for PTS01)
- T0 Tue/Thu calls: request the **synthetic MM entity in QA** with unlimited buying power
- Locate **Edwin's prior simulation trigger script**
- Cody: ask Edwin how to value week zero of college football

---

## Cross-references

- **[[trading/trading]]** — the MM trades through the same T0 order book users do; synthetic market orders for users use the same price-through crossing mechanic
- **[[ipo-module/ipo-module]]** — IPO fill guarantee / float warehousing
- **[[earnings-report/earnings-report]]** — off-field revenue is a share-price input
- **[[architecture/open-questions]]** — MM algorithm co-build and internal-MM rows track the open items
- **T0** — hosts the synthetic MM entity; matching, market data feeds, quote-bust mechanics
- **Sport Radar** — event data + live win probabilities as pricing inputs
