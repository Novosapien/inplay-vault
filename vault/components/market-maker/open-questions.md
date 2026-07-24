# Market Maker — Open Questions

> **Component:** [[market-maker/market-maker]]
> **Purpose:** The live blocker list, by owner. Update after every touchdown /
> T0 call. Global architecture questions live in
> [[architecture/open-questions]]; this is the MM-specific working list.

**Next scheduled venues:** T0 tech calls Tue + Thu · **another MM call with
Edwin expected** (the 23-07 call never reached E11/E12; George emailing him
the anchor doc).

**Next-call priority (set 23-07):** E11 settlement → E12 NCAA scope → E14
float basis → E16 always-on trading → N14 fill-response walk-through → E1
$/win sign-off. Asked as **questions**.

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
| E4 | **Edwin's old simulation code** — he's sending the original market-maker Python files ("functional, not a heavy lift") | Calibration | 🟡 In motion (23-07) |
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

## Owed by / with T0 (Tue + Thu calls)

| # | Question | Blocks | Status |
|---|----------|--------|--------|
| T1 | **MM account — permission to create it** — we know the messages (create account, seed stock, move cash: `UAAR`/`UEPR`/`UBT`). Still needed: permission to send them on our connection + how account numbers map between the REST system and the OMS | All testing | 🟡 Mechanism known — permission pending |
| T2 | **Order-rate limit** — how many messages/sec will tZERO allow the MM account (`MaxOrdRate`)? Our own software is proven far faster than needed; the venue's allowance is the real ceiling. Need ~1–2k msg/s at peak — more if NCAA secondary happens (E12) | Quoting cadence | 🟡 Venue config question |
| T3 | **Reject out-of-band trades at source** — can the matching engine itself refuse any trade outside the price corridor, per team? If yes, voiding trades becomes a rare last resort | Supervision | 🔴 Open |
| T4 | **Voiding + correcting trades** — who decides, who triggers, how fast; positions/cash reverse automatically (plumbing known). Also (23-07): the spec lets T0 **correct** a past trade's price/size instead of voiding it — when would they, and can a correction leave someone worse off? | Supervision | 🔴 Open |
| T5 | **Halting one team's market** — the data feed carries halt states (including manual halts), so we can *see* halts the moment they happen (23-07). Ask: who can trigger one, how fast, do resting orders survive it, who resumes | Supervision, market state | 🔴 Open — feed side confirmed |
| T6 | **IPO stock warehousing** — how the ledger records the MM absorbing unsold IPO stock (~50k blocks) | IPO fill guarantee | 🔴 Open (also in [[architecture/open-questions]]) |
| T9 | **Opening auction, or just always on?** — apart from the short daily gap, is it plain normal matching all day, every day? The venue supports opening auctions (collect orders, one opening price, then normal trading) — confirm we're NOT using one. Mirrors E16 (opened 23-07) | Market state, quoting | 🔴 Open — ask on next call |
| T10 | **One environment for everything** — T0 have said it's basically one environment: all testing, QA, and production in the same place (George, 23-07). So every risky experiment (account setup, the queue test, rate limits, halt and bust drills) must be done **before real users arrive** — after that there is no sandbox. Ask: can we have **permanent test symbols** (~10)? ⚠ They'd be FINRA-regulated securities, so users must be **blocked from trading them in the app** — confirm what's allowed and how many we can have | All testing, the plan | 🔴 Open — top of list |
| T7 | ~~MM order entry = standard OE session?~~ **✅ RESOLVED 22-07:** no Quote/MassQuote interface exists in tZERO's FIX schema — the MM is order-based (resting limit orders via D/F/G) by necessity. Dedicated MM FIX session (isolation) remains a filed ask | — | ✅ Resolved |
| T8 | ~~Order-update behaviour~~ **✅ RESOLVED / MOOT 23-07:** **8.1 answered** — an updated order goes to the **back of the queue** (T0 call + Troy: standard on every matching engine); Edwin: "we don't care about that." **8.2 moot** — we never top up partially-filled orders (new lifecycle). **8.3 moot for v1** — a momentary self-cross during a price adjustment is tolerated (George-confirmed). Self-match prevention follow-up → T11 | — | ✅ Resolved |
| T11 | **What self-match prevention does T0 have?** — Troy checking (23-07). Relates to the per-account wash-trade toggle in the OMS spec. For USER wash-trading the v1 policy is rulebook ban + order queries on high-volume accounts + removal from the event | Supervision | 🟡 Troy checking |

## Owed by Sport Radar

| # | Question | Blocks | Status |
|---|----------|--------|--------|
| S1 | **The probabilities API is broken** — 403 errors; only 8 of 32 NFL win totals come back. The pricing engine has no input until this is fixed | Valuation | 🟡 Escalated — Cody chasing |
| S2 | **More API allowance** — the trial quota is nearly half used; we need a production-sized allowance | Valuation | 🟡 Cody on it |
| S3 | **Do they push updates to us, or do we keep asking?** — sets how stale our prices can get, and whether we can even measure the feed's delay | Valuation cadence | 🔴 Open (long-standing) |
| S4 | **Our probabilities must not lag the sportsbooks** — if the feed is behind DraftKings/FanDuel, users pick the MM off ("too easy for people to make money"). Cody owns getting the right feeds | MM integrity | 🔴 Open — Cody (23-07) |
| S5 | **Can Sport Radar actually serve it the way Edwin expects?** — live win probability per game, readable roughly every 200ms during play, with enough quota; plus the **simulation games** we want for testing (replay a past game in a ~4-hour window). Check their API products against this shape before the next MM call (George, 23-07) | Valuation, testing | 🔴 Open — check next |

## Ours to design (Novosapien)

| # | Question | Blocks | Status |
|---|----------|--------|--------|
| N1 | **How the price travels** — the pipe carrying each new fair value from the valuation engine to the quoting engine (likely a NATS topic per team). Ours; invisible to the book | Valuation → quoting | 🔴 Open |
| N2 | **One profile table** — the two standards list different profile menus; merge them into one. Structure ours; every number in it Edwin's | Market state, quoting | 🔴 Open |
| N3 | **When do we stop trusting our inputs?** — the staleness/delay thresholds that flip a market defensive. **Edwin decides the policy, we implement** | Market state | 🔴 Open |
| N4 | **When does each session start and end?** — in-game / around-game / overnight, per team (NCAA plays 6 days a week). **Edwin decides, we implement** | Market state | 🔴 Open |
| N5 | **"Just buy it" button depth** — how many price levels through a synthetic market order reaches; chase it if unfilled, yes/no; how it interacts with the wallet check | Trading app | 🔴 Open — Troy assisting |
| N6 | **Two algos were named — where's the line?** — "load-balancing" vs "market-making" (17-07); nobody has defined the boundary | Architecture | 🔴 Open |
| N7 | **Service layout** — one MM service or several (valuation and quoting separate)? Where does it run? Ours, from scratch; the platform's offered plumbing is an input, not a constraint | Architecture | 🔴 Open |
| N8 | **How much replay tooling at launch?** — recording everything is cheap and mandatory; the tools to replay it are not. Where's the v1 line? | Quoting engine | 🟡 Proposal: record all, defer tooling |
| N9 | **The platform team's suggestions: accept or replace, one by one** — their prototype's formulas, their numbers, the 200ms full-refresh idea, the MM-as-a-user-account idea. All treated as input only; our from-scratch design accepts or replaces each explicitly | MM design | 🔴 Open |
| N10 | ~~Do quotes live one cycle, or get managed over time?~~ **✅ RESOLVED 23-07 — Edwin defined the lifecycle:** partially-filled orders **rest until completely gone** (no top-ups, no aging). On a price move: cancel the old level, post the **remaining** quantity at the new price. After a full fill at an unchanged price: reload at top of book. The standard's quote-aging chapter is moot | Quoting engine | ✅ Resolved |
| N11 | **Skew the sizes too, or just the prices?** — when the MM is long it could also show less on the bid and more on the offer, not just move prices. Directly visible in the book | Quoting engine | 🔴 **Edwin's call** |
| N13 | **What data the MM consumes, and how** — everything arrives pushed and sits in memory; the loop never reads a database. Proposed: the quoting engine needs only the fair price and its own orders; the venue's book feed is for the watchdog and monitoring, not for quoting (MD spec read 23-07 confirms the feed streams updates after one subscribe) | Architecture, supervision | 🟡 Proposed |
| N12 | ~~How old quotes become new ones each cycle~~ **✅ RESOLVED for v1, 23-07 (Edwin + George):** post the new quotes **without waiting** for cancel confirmations; a momentary self-cross during a price adjustment is acceptable ("on the first iteration… I don't care"). The 22-07 amend-in-place/reconciler analysis is **shelved, preserved in [[market-maker/learnings]]** for the augment-later phase | Quoting engine | ✅ Resolved for v1 |
| N14 | **Fill-response logic** — "if you get a fill, what do you do next?" e.g. outside games: filled at 6 → maybe leave the bid at 6 and let the ladder fill down (5, 4, 3) rather than instantly re-quoting. Rules to design with Edwin (opened 23-07) | Quoting engine | 🔴 Open — next call |

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
