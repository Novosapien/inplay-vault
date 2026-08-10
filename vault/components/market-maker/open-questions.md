# Market Maker — Open Questions

> **Component:** [[market-maker/market-maker]]
> **Purpose:** The live blocker list, by owner. Update after every touchdown /
> tZERO call. Global architecture questions live in
> [[architecture/open-questions]]; this is the MM-specific working list.

**Next scheduled venues:** tZERO tech calls Tue + Thu · Mon/Wed/Fri touchdowns
· **13 Aug dry run** (secondary trading on a live preseason game).

**Next-call priority (reset 10-08 after the 27-07 → 07-08 block):** T13 tickers
(blocks all order testing) → T12 the two MPIDs → E19 taker requirements doc →
E20 daily-report schema → E22 taker share range + time blocks → E11 settlement
→ E12 NCAA scope → E14 float basis. Asked as **questions**.

> **What the 27-07 → 07-08 block changed:** the IPO market structure is settled
> (two MPIDs, taker as primary buyer, load-balancing algo dropped), the
> valuation input chain is confirmed end to end (SR probabilities contract
> signed, poll at 500ms, RP formula agreed), and E11/E12 are **still unasked**
> after three more calls. See [[market-maker/decisions]].

> **Stance (George, 22-07): we ask — we do not propose.** Parameter values and
> deferred math are InPlay's remit, not ours. The placeholder constants in
> [[market-maker/systems/decision-cycle-reference]] exist only to make the
> pseudocode runnable; they carry no authority and are not presented to Edwin
> as proposals. Interactive walk-through of every deferred item:
> `mm-pipeline.html` (this folder).
>
> **The remit line (22-07):** litmus test — *"if Edwin watched the book, could
> he tell the difference?"* **Yes → his algorithm, his question**: every
> number, formula, threshold, session boundary, and visible behaviour.
> **No → engineering mechanics, ours**: topology, transport, FIX plumbing,
> event-sourcing/replay implementation, retry caps, dead-man switch. N-items
> below that carry visible behaviour are marked **Edwin decides, we implement**.

---

## Jargon key (plain terms used below — full list in [[market-maker/glossary]])

- **Resting order** — an order sitting in the book, waiting to trade. Price
  named, nothing traded yet, cancellable any time.
- **OrderQty / CumQty / LeavesQty** — an order's total · how much has filled ·
  how much is still resting. 500 total, 250 filled → 250 resting.
- **Queue position** — at each price, first come first served. Your fills
  depend on your place in that queue.
- **Cancel-replace / amend (35=G)** — update a resting order's price/size in
  one atomic message; fills carry over to the updated order.
- **Crossed vs crossing** — *crossed* = a bid and offer overlapping while both
  REST in the book (nonsense state; we must never publish one). *Crossing* =
  an arriving order priced through the other side — it just executes
  immediately (normal; how the synthetic market order works).

## Owed by Edwin / InPlay

| # | Question | Blocks | Status |
|---|----------|--------|--------|
| E1 | **Sign off $5 per win** — the client's own price sheet works out to: each expected win adds **$5.00** to the share price. Confirm it, and say whether NCAA uses the same number | Valuation | 🟡 Decoded — needs sign-off |
| E2 | ~~Off-field: which number goes into the price?~~ **✅ RESOLVED 23-07:** Edwin's **popularity index** — ~$14–30 per team, static at the start, already inside the NFL IPO prices, refreshed in the **Wednesday data drop**. Residual: how the EST/ACT earnings mechanic interacts with it long-term — deferred | Valuation | ✅ Resolved (residual deferred) |
| E3 | **Opening prices** — who calculates each team's starting price at IPO, and from what? (NFL sheet exists; NCAA owed) | Valuation, IPO | 🟡 NFL known / 🔴 NCAA |
| E4 | ~~Edwin's old simulation code~~ **✅ CLOSED 31-07:** received and assessed. It **cannot be used as-is** — too much missing above and below it, plus the technical layer (200ms scheduling, cancel behaviour, state). We extract components (the volatility calculation named specifically) and replace the rest. Edwin ran ~5,000 sims/team over ~5 seasons with it | Calibration | ✅ Closed (assessed, not adopted) |
| E5 | **All the pricing numbers** — spreads, ladder shape, sizes, how hard the MM fights to stay flat (λ) — per session and profile. **We ask; we don't propose** | Quoting | 🔴 Open |
| E6 | **Week-zero college games** — how to price massive-mismatch openers | Valuation | 🔴 Open (Cody to ask) |
| E7 | **How strictly do the standards bind for season 1?** — which rules bend for launch (replay tooling, audit depth, the quote-aging chapter)? | Everything | 🟡 Needs explicit sign-off |
| E8 | **Limits on deliberate price-moving** — Edwin described the MM occasionally moving the price on purpose to exit stock. What bounds make that acceptable? (Agreed: not in v1) | Quoting, integrity | 🔴 Open |
| E9 | **Weekly Financial Report** — who produces it, what's in it, when | Market state, settlement | 🔴 Open |
| E10 | **The missing valuation-math chapter** — CTS-001 §3 is referenced everywhere and absent from our copy. Request the PDF | Valuation | 🔴 Open |
| E11 | **What does a share actually pay out at season end?** — THE most important question. If the answer is "off-field + $5 × actual wins", then the whole pricing engine is just a live estimate of that number and everything becomes simple | Everything | 🔴 **Top of agenda** |
| E12 | **Do NCAA teams trade this season?** — the price sheet covers 32 of 170 teams. NFL-only at launch, or does NCAA get prices too? Decides how many markets we run | Scope, plan | 🔴 Open |
| E13 | ~~How is "expected remaining wins" calculated?~~ **✅ RESOLVED 23-07:** produced **internally by InPlay, weekly** (Sport Radar doesn't do season totals — futures aren't updated); Edwin helping automate; delivered in the Wednesday drop | Valuation | ✅ Resolved |
| E14 | **Which share count for the skew?** — the MM's skew works off "inventory as a % of the float". Is the float 875k (the sheet) or 5M (the capacity)? The answer changes the skew's strength ~5.7× | Quoting | 🔴 Open |
| E15 | ~~When a play happens, what moves the price?~~ **✅ RESOLVED 23-07:** just Sport Radar's live win probability, pulled directly — no own event weights in v1 ("you don't have to create it") | Valuation | ✅ Resolved |
| E16 | **Is trading just… on, all day?** — confirm the product intent: continuous matching all day, every day (apart from the short daily maintenance gap) — no daily opening auction, no open/close ceremony (mirrors T9; opened 23-07) | Market state | 🔴 New |
| E17 | **SNT-1 x MM interaction during Primary Mandate rounds**, Edwin explicitly invited this: how the noise taker's flow interacts with the MM's quoting and inventory while the MM is absorbing unsold IPO float (completion sweep). Does SNT-1 run during the primary at all, or only once secondary opens? | SNT-1, MM | 🔴 New _(30-07, Edwin)_ |
| E18 | **SNT-1 tuning + weight feed**, the two levers Edwin expects to tune after real books are `base_orders_per_hour` and the daily loss budget. Also: confirm the per-team `team_weight` (0.25–4.0) feed from the EAV / popularity model | SNT-1 | 🟡 _(30-07, tune post-launch)_ |
| E19 | **Taker requirements document** — George asked for one in the same shape as the MM requirements doc Edwin already produced. Owed, not yet started | Taker build | 🔴 New _(07-08, Edwin acknowledged: "I actually owe you deliverables")_ |
| E20 | **Structure of the daily report the MM consumes** — Edwin's daily drop carries the pricing mechanism and expected wins. He confirmed it is codifiable rather than judgement ("it's a math problem, not a what I feel like") but has not built the forward-looking gains model yet. Need the schema so we can automate ingestion rather than hand-loading it | Valuation | 🔴 New _(03-08 / 07-08)_ |
| E21 | **Volatility half-life in the spread equation** — width now comes from the time-decaying volatility number, not a lookup table. George floated ~20 seconds; Edwin did not confirm ("I don't know if that's right") | Quoting | 🔴 New _(03-08)_ |
| E22 | **Taker share range and time blocks per team** — Edwin owes the concrete range (~600–650k of 1,000,000) and the time-block schedule the randomiser runs inside, per league window | Taker, IPO | 🔴 New _(31-07 / 03-08)_ |
| E23 | **Market operations after the primary closes** — Edwin plans to "do market operations to get everyone balanced" once secondary opens, deliberately as a tradeable information event. What are the rules, who triggers it, and does it run through the maker or the taker? | Taker, market state | 🔴 New _(31-07)_ |

## Owed by / with tZERO (Tue + Thu calls)

| # | Question | Blocks | Status |
|---|----------|--------|--------|
| T1 | **MM account — permission to create it** — we know the messages (create account, seed stock, move cash: `UAAR`/`UEPR`/`UBT`). Still needed: permission to send them on our connection + how account numbers map between the REST system and the OMS | All testing | 🟡 Mechanism known — permission pending |
| T2 | **Order-rate limit** — how many messages/sec will tZERO allow the MM account (`MaxOrdRate`)? Our own software is proven far faster than needed; the venue's allowance is the real ceiling. Need ~1–2k msg/s at peak — more if NCAA secondary happens (E12) | Quoting cadence | 🟡 Venue config question |
| T3 | **Reject out-of-band trades at source** — can the matching engine itself refuse any trade outside the price corridor, per team? If yes, voiding trades becomes a rare last resort | Supervision | 🔴 Open |
| T4 | **Voiding + correcting trades** — who decides, who triggers, how fast; positions/cash reverse automatically (plumbing known). Also (23-07): the spec lets tZERO **correct** a past trade's price/size instead of voiding it — when would they, and can a correction leave someone worse off? | Supervision | 🔴 Open |
| T5 | **Halting one team's market** — the data feed carries halt states (including manual halts), so we can *see* halts the moment they happen (23-07). Ask: who can trigger one, how fast, do resting orders survive it, who resumes | Supervision, market state | 🔴 Open — feed side confirmed |
| T6 | **IPO stock warehousing** — how the ledger records the MM absorbing unsold IPO stock (~50k blocks) | IPO fill guarantee | 🔴 Open (also in [[architecture/open-questions]]) |
| T9 | **Opening auction, or just always on?** — apart from the short daily gap, is it plain normal matching all day, every day? The venue supports opening auctions (collect orders, one opening price, then normal trading) — confirm we're NOT using one. Mirrors E16 (opened 23-07) | Market state, quoting | 🔴 Open — ask on next call |
| T10 | **One environment for everything** — tZERO have said it's basically one environment: all testing, QA, and production in the same place (George, 23-07). So every risky experiment (account setup, the queue test, rate limits, halt and bust drills) must be done **before real users arrive** — after that there is no sandbox. Ask: can we have **permanent test symbols** (~10)? ⚠ They'd be FINRA-regulated securities, so users must be **blocked from trading them in the app** — confirm what's allowed and how many we can have | All testing, the plan | 🔴 Open — top of list |
| T7 | ~~MM order entry = standard OE session?~~ **✅ RESOLVED 22-07:** no Quote/MassQuote interface exists in tZERO's FIX schema — the MM is order-based (resting limit orders via D/F/G) by necessity. Dedicated MM FIX session (isolation) remains a filed ask | — | ✅ Resolved |
| T8 | ~~Order-update behaviour~~ **✅ RESOLVED / MOOT 23-07:** **8.1 answered** — an updated order goes to the **back of the queue** (tZERO call + Troy: standard on every matching engine); Edwin: "we don't care about that." **8.2 moot** — we never top up partially-filled orders (new lifecycle). **8.3 moot for v1** — a momentary self-cross during a price adjustment is tolerated (George-confirmed). Self-match prevention follow-up → T11 | — | ✅ Resolved |
| T12 | **Stand up the two MPIDs** — `InPlay Markets` the **broker dealer** (preloaded 1,000,000 shares per team company + unlimited buying power, sells the primary) and `InPlay Markets` the **principal trading arm** (one wallet, maker + taker algos). Troy committing to configure it this way on tZERO; we need the account/wallet IDs and the entitlements | IPO, all MM testing | 🟡 New _(03-08, Troy actioning)_ |
| T13 | **Team company tickers** — the MM cannot start order testing until tZERO issue the tickers. Named as the immediate blocker on 07-08 ("once we get the tickers from T0… then we'll start testing it, making orders"). Ties to the C6 naming constraint in [[compliance/compliance]] | MM testing, 13 Aug dry run | 🟡 New _(07-08, chased same day)_ |
| T14 | **IPO price lock vs simulated trading** — tZERO make prices **static once the IPO price is set**, which blocks simulated trading. Agreed workaround: publish prices now, **freeze only 3 days before the IPO**. Confirm tZERO can hold prices unlocked until then, and that the 3-day freeze is enforceable on their side | IPO, price publication | 🔴 New _(31-07)_ |
| T11 | **What self-match prevention does tZERO have?** — Troy checking (23-07). Relates to the per-account wash-trade toggle in the OMS spec. For USER wash-trading the v1 policy is rulebook ban + order queries on high-volume accounts + removal from the event | Supervision | 🟡 Troy checking |

## Owed by Sport Radar

| # | Question | Blocks | Status |
|---|----------|--------|--------|
| S1 | ~~The probabilities API is broken~~ **✅ RESOLVED 03-08:** contract amendment signed by Troy at **no change in cost**, live probabilities now in the **production** account. Cody: "Done." | Valuation | ✅ Resolved |
| S2 | ~~More API allowance~~ **✅ RESOLVED 03-08:** quota stopped being the constraint under the amended contract. Edwin: "there's no limit on requests"; Cody: "I'm not worried about the API call limits." Supersedes the 27-07 concern about 8–10M calls/month | Valuation | ✅ Resolved |
| S3 | ~~Do they push updates to us, or do we keep asking?~~ **✅ ANSWERED 03-08:** we **poll**. Probability never rides in the play-by-play payload, so the MM polls the probabilities endpoint on its own clock — **500ms in-game** to start, slower but still polled outside games (the taker needs 24/7 prices). Next-game probabilities post **~15 min after the previous game ends** (typically faster), derived from the posted odds; the prior value carries until then | Valuation cadence | ✅ Answered |
| S4 | **Our probabilities must not lag the sportsbooks** — if the feed is behind DraftKings/FanDuel, users pick the MM off ("too easy for people to make money"). Still live: the probabilities are an extrapolation of posted odds, so lag is a function of how fast SR ingests the line. **The betting feed (faster play-by-play) was explicitly ruled out for this run**, so there is no faster path bought | MM integrity | 🔴 Open — Cody (23-07, re-scoped 03-08) |
| S6 | **What is a "key player"?** — the team page currently pulls the naive top four. Cody: SR sells facts, not subjective impact ratings, so the closest available primitive is the **depth chart** (QB1, RB1, WR1 plus a defensive player). An own impact algorithm is explicitly deferred ("let's not go down that rabbit hole") | [[information-layer/sub-components/team-page/team-page]] | 🔴 New _(07-08)_ |
| S5 | **Can Sport Radar actually serve it the way Edwin expects?** — live win probability per game, readable roughly every 200ms during play, with enough quota; plus the **simulation games** we want for testing (replay a past game in a ~4-hour window). Check their API products against this shape before the next MM call (George, 23-07) | Valuation, testing | 🔴 Open — check next |

## Ours to design (Novosapien)

| # | Question | Blocks | Status |
|---|----------|--------|--------|
| N1 | **How the price travels** — the pipe carrying each new fair value from the valuation engine to the quoting engine (likely a NATS topic per team). Ours; invisible to the book | Valuation → quoting | 🔴 Open |
| N2 | **One profile table** — the two standards list different profile menus; merge them into one. Structure ours; every number in it Edwin's | Market state, quoting | 🔴 Open |
| N3 | **When do we stop trusting our inputs?** — the staleness/delay thresholds that flip a market defensive. **Edwin decides the policy, we implement** | Market state | 🔴 Open |
| N4 | **When does each session start and end?** — in-game / around-game / overnight, per team (NCAA plays 6 days a week). **Edwin decides, we implement** | Market state | 🔴 Open |
| N5 | **"Just buy it" button depth** — how many price levels through a synthetic market order reaches; chase it if unfilled, yes/no; how it interacts with the wallet check | Trading app | 🔴 Open — Troy assisting |
| N6 | ~~Two algos were named — where's the line?~~ **✅ DISSOLVED for v1, 31-07:** Edwin **dropped the load-balancing algo entirely** for NFL and NCAA season 1 — one application, same behaviour, stretched over a 5-day (NCAA) or 2-day (NFL) window. Deferred to the **NBA in October**. The live pair is now **maker vs taker**, and that boundary is defined (03-08): same entity, same wallet, same MPID, two execution styles; taker-only during the primary, both in tandem in secondary | Architecture | ✅ Dissolved for v1 |
| N7 | **Service layout** — one MM service or several (valuation and quoting separate)? Where does it run? Ours, from scratch; the platform's offered plumbing is an input, not a constraint | Architecture | 🔴 Open |
| N8 | **How much replay tooling at launch?** — recording everything is cheap and mandatory; the tools to replay it are not. Where's the v1 line? | Quoting engine | 🟡 Proposal: record all, defer tooling |
| N9 | **The platform team's suggestions: accept or replace, one by one** — their prototype's formulas, their numbers, the 200ms full-refresh idea, the MM-as-a-user-account idea. All treated as input only; our from-scratch design accepts or replaces each explicitly | MM design | 🔴 Open |
| N10 | ~~Do quotes live one cycle, or get managed over time?~~ **✅ RESOLVED 23-07 — Edwin defined the lifecycle:** partially-filled orders **rest until completely gone** (no top-ups, no aging). On a price move: cancel the old level, post the **remaining** quantity at the new price. After a full fill at an unchanged price: reload at top of book. The standard's quote-aging chapter is moot | Quoting engine | ✅ Resolved |
| N11 | **Skew the sizes too, or just the prices?** — when the MM is long it could also show less on the bid and more on the offer, not just move prices. Directly visible in the book | Quoting engine | 🔴 **Edwin's call** |
| N13 | **What data the MM consumes, and how** — everything arrives pushed and sits in memory; the loop never reads a database. Proposed: the quoting engine needs only the fair price and its own orders; the venue's book feed is for the watchdog and monitoring, not for quoting (MD spec read 23-07 confirms the feed streams updates after one subscribe) | Architecture, supervision | 🟡 Proposed |
| N12 | ~~How old quotes become new ones each cycle~~ **✅ RESOLVED for v1, 23-07 (Edwin + George):** post the new quotes **without waiting** for cancel confirmations; a momentary self-cross during a price adjustment is acceptable ("on the first iteration… I don't care"). The 22-07 amend-in-place/reconciler analysis is **shelved, preserved in [[market-maker/learnings]]** for the augment-later phase | Quoting engine | ✅ Resolved for v1 |
| N14 | **Fill-response logic** — "if you get a fill, what do you do next?" e.g. outside games: filled at 6 → maybe leave the bid at 6 and let the ladder fill down (5, 4, 3) rather than instantly re-quoting. Rules to design with Edwin (opened 23-07) | Quoting engine | 🔴 Open — next call |
| N15 | **Build SNT-1's `ExchangeAdapter`**, implement the four-method adapter (`top_of_book`, `activity_state`, `send_marketable_ioc`, `position`) against the matching engine, and set the gateway account flags (`HOUSE_SYNTHETIC`, `leaderboard_eligible=false`, `participant_side=false`). The agent logic itself is Edwin's reference code | SNT-1 | 🔴 New _(30-07)_ |
| N16 | **SNT-1 production hardening**, the five items Edwin listed: (1) kill switch + logging + per-order notional cap; (2) persist pos/basis across restarts; (3) periodic position reconciliation vs the engine, halt the book on divergence; (4) rely on IOC limit enforcement as the real impact cap (stale TOB snapshots are fine); (5) `activity_state()` mapping (off-season/overnight → OVERNIGHT, IPO windows → PRE_KICKOFF minimum) | SNT-1 | 🔴 New _(30-07)_ |

---

## Resolved (moved to [[market-maker/decisions]])

Build ownership (all three standards = ours) · capital model (unlimited — Ch 5
descoped) · MM mechanics (resting liquidity, participant entity) · order types
(limit-only + crossing) · RP = mid = ESV · market isolation · sessions (three)
· band existence (~30%) + busting requirement · ops UI existence · synthetic
market order existence.

**23-07 MM call:** E2 (off-field = popularity index, Wednesday drop) · E13
(remaining wins = InPlay internal weekly) · E15 (probability-only in-game) ·
T8 (replace = back of queue; top-up + crossing edge cases moot) · N10 (quote
lifecycle: rest until gone, cancel + repost remaining on price move) · N12
(v1: post-first, momentary self-cross tolerated) · cadence bifurcated by game
state (supersedes flat 5–10/sec).

**27-07 → 07-08 touchdown block:** S1 (probabilities contract signed, in
production) · S2 (quota no longer a constraint) · S3 (we poll, 500ms in-game;
next-game probabilities ~15 min after the prior game) · E4 (Edwin's code
assessed, components extracted only) · N6 (load-balancing algo dropped for
v1; maker-vs-taker boundary defined instead) · IPO market structure (two
MPIDs, broker dealer holds and sells, taker buys ≥600k of 1M per team,
randomised size and heartbeat, not participation-weighted) · RP anchoring
confirmed correct by Edwin · RP formula agreed with kickoff-delta term.
