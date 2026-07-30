# Market Maker — Decisions Log

> **Component:** [[market-maker/market-maker]]
> **Purpose:** Dated, source-attributed log of confirmed decisions — including
> where spoken decisions **supersede the written standards**. When a standard
> doc and this log conflict, **this log wins** (the standards are AI-generated
> context; Edwin: "meant for Claude to read… they're fairly simple").

Format: newest first. ✅ decision · ✂ supersession of a standard · ⚠ caveat.

---

## 2026-07-30, SNT-1 Synthetic Noise Taker added (Edwin email), [[market-maker/systems/synthetic-noise-taker]]

> Edwin delivered a spec-quality reference implementation (`sources/snt1_noise_taker.py`, ~349 lines) for a **second house agent**. Session note: `sessions/2026-07-30-snt1-noise-taker.md`.

- ✅ **A second house agent, SNT-1, is in scope.** A non-participant, taker-only house account that crosses the spread with random sizes at random times so every team book trades from IPO onward, including with no games on. It complements the MM (maker); SNT-1 is the taker.
- ✅ **Deliberately a controlled loser.** Its spread cost is the subsidy that seeds an active secondary market. Not trying to move price toward any target; flow is pure noise.
- ✅ **No off-field-split spec amendment needed.** SNT-1 prints against the MM carry zero participant sides, so they are excluded from the $2.50 off-field volume split under the existing >= 1-participant-side rule. `leaderboard_eligible = false`, so no leaderboard credit.
- ✅ **Design locked at v1.0** (all numbers in [[market-maker/parameters]], status 🟡): Poisson arrivals, log-normal sizes (5 to 400, median ~30), 50/50 direction, ~90% at-touch IOC (<= 50% of touch) / ~10% sweeps capped at 3 ticks through touch, intensity `base 9/hr x state x team_weight` (LIVE 75x), $100k per-team daily loss governor (metered cost-vs-mid), disposition-effect profit-take tilt (0.50 -> 0.65, losers ride at 50/50), 1,500-share inventory soft cap (80% flatten bias), taker-only, hard guards (no halted/locked/crossed/one-sided/RP-freeze/>8-tick books).
- ✅ **Account flags on the gateway:** `account_type = HOUSE_SYNTHETIC`, `leaderboard_eligible = false`, `participant_side = false`.
- ⚠ **Two levers to tune after real books:** `base_orders_per_hour` and the loss budget (Edwin).
- **Our side (not Edwin's):** implement the `ExchangeAdapter` against the matching engine, plus the five production-hardening tasks (kill switch + logging + per-order notional cap; persist pos/basis across restarts; periodic position reconciliation with halt-on-divergence; IOC limit enforcement as the impact cap; `activity_state()` mapping). See [[market-maker/open-questions]].

## 2026-07-23 — MM follow-up call (Edwin + Troy + team) — [[23-07-2026-market-maker-follow-up]]

> Not the planned deep-dive: **E11 (settlement) and E12 (NCAA) were never
> asked** — another MM call expected. George emailing the anchor doc to Edwin.
> Theme: **"really simple to start"** — augment over the next couple of months.

- ✂ **Quote lifecycle overturned — no top-ups, ever.** A partially-filled
  resting order is never refreshed; it rests until completely gone. On a
  price move: cancel the old level, post the **remaining** quantity at the
  new price. After a full fill at an unchanged price: reload at top of book.
  Supersedes the 22-07 amend-in-place recommendation (N12) and the
  top-up-replace mechanics (N10 → resolved).
- ✅ **Replace = cancel + new order at the back of the queue** — confirmed on
  the T0 call and by Troy ("common practice on just about every matching
  engine"). Edwin: **"we don't care about that."** (T8.1 resolved; 35=G's
  only remaining value is message count.)
- ✅ **v1 crossing tolerance (confirmed by George 23-07):** post the new
  quotes without waiting for cancel confirmations; a **momentary self-cross
  during a price adjustment is acceptable** in v1. Edwin: "new orders are
  faster than cancels… on the first iteration, if we have to cross in order
  to make the adjustment in price, I don't care." No cancel-first-wait gap.
- ✅ **Cadence bifurcated by game state:** live games **~200ms per call**
  ("a second's too long") · non-live **every 30–60s** · **earnings windows**
  (Tue NFL / Wed NCAA): call all ~170 symbols for **~5 minutes**. Supersedes
  the flat all-teams-every-cycle framing.
- ✅ **Randomizer = quantities only** (especially top-of-book size, so the
  book doesn't read programmatic). **Price is purely algorithmic** — no
  price randomization. Narrows the 20-07 randomizer decision.
- ✅ **In-game price driver = Sport Radar live win probability, pulled
  directly.** No own event-weight algorithm in v1 ("you don't have to create
  it — you just pull Sport Radar's probability in"). E15 resolved;
  `event trigger weights` not needed v1.
- ✅ **Remaining-season wins produced internally by InPlay, weekly.** SR
  doesn't compute season win probability (futures aren't updated/tradeable);
  Edwin helping automate. E13 resolved.
- ✅ **Off-field = Edwin's popularity index** — ranked attendance/merch/
  popularity, valued **~$14–30 per team** (Dallas ~$30; Carolina/Arizona
  ~$14); **static at the start** and already inside the NFL IPO prices;
  changes with winning + star-player effects. E2 substantially resolved.
- ✅ **The Wednesday data drop:** every Wednesday InPlay delivers the updated
  off-field metric + remaining-game win probabilities; we plug them into the
  algo. New operational cadence.
- ✅ **Betting-feed parity requirement:** our probabilities must not lag
  DraftKings/FanDuel "or we're going to get picked off." Cody owns getting
  the feeds. (New Phase-0 item.)
- ✅ **User wash-trading policy = rulebook + surveillance, not tech (v1):**
  prohibited in the rulebook; order-query on high-volume accounts; removal
  from the event. Troy checking what self-match prevention T0 employs (new
  T-item).
- ✅ **MM is a buyer at every IPO** — when buyers are short / to balance
  shares pushed into the market. Edwin: **"we're going to start with the
  IPO"** — sequencing signal; fuller session promised.
- ✅ **Testing via SR simulation games:** replay a past game in a ~4-hour
  window instead of waiting for preseason.
- ✅ **Edwin sending the original MM simulation Python files** ("functional,
  not a heavy lift") — E4 in motion.

## 2026-07-23 — tZERO Order Entry FIX spec v2.2 read (George + Claude, validated)

**Adopted — venue facts from the OE spec itself:**

- ✅ **FIX 4.2 only** (`BeginString` always FIX.4.2). Limit orders only
  (OrdType=2 is the sole value) — reconfirms 22-07. TIF = Day / GTC / GTD;
  GTC/GTD require `RoutingInst(9303)=DNRI`. Price field to 4 decimals (field
  precision — tick policy stays $0.01).
- ✅ **Order Replace Request (35=G) exists.** Symbol AND **Side must match the
  original order** — side is immutable; a bid can never become an offer.
- ✅ **Fills survive the replace chain:** Order Replaced carries `CumQty` +
  `AvgPx` forward. `OrderQty` on a replace = the new **total** for the chain;
  `LeavesQty = OrderQty − CumQty`. (Top-up to X resting = replace with
  `OrderQty = CumQty + X`.)
- ✅ **The fill-vs-cancel race has a defined reject:** Cancel/Replace Request
  Reject with `CxlRejReason 0 = "Too Late To Cancel"` (1 = unknown order).
- ✅ **Every execution report can carry `PosSIZ` / `PosCOST` / `PosRpnl` /
  `PosUpnl`** — venue-authoritative position + P&L per fill. Fields optional,
  so: our own event-sourced inventory stays primary; venue values used as a
  free cross-check (disagreement = bug alarm) + ops-UI P&L source.
- ✅ **No iceberg orders** — `MinQty`/`MaxFloor` "not supported on tZERO
  Matching Engine": displayed size = real size, always.
- ✅ **No `ExecInst`** — no post-only, no self-trade prevention at order
  entry. Our publish sequencing is the ONLY protection against executing
  against our own stale quotes.
- ✅ **Unsolicited cancels exist** (Order Cancelled has an unsolicited
  variant) — the reconciler must absorb venue-initiated cancels.
- ✅ **Execution Busted (ExecType=H)** confirmed at OE level; **Execution
  Corrected (ExecType=G)** also exists — a past fill's price/qty can be
  re-stated (either direction). Both reprocess through the same
  fill-reconciliation path. **Done for Day** message exists.
- ✅ `ClOrdID` ≤ 20 chars, **no leading zeroes**. Cancel/Replace *Pending*
  acks suppressed by default (request → silence → Replaced/Rejected).

**Adopted — our design consequences (validated 23-07):**

- ✅ Reconciler **never sends a replace with `OrderQty ≤ CumQty`** — where a
  shrink would go below what's filled, cancel + create fresh instead.
- ✅ Hot path is **push-only, memory-only**: FIX execution reports + bus RP
  push + in-memory state; per-cycle snapshot-at-start (atomic copy, live
  state keeps mutating, mid-cycle arrivals coalesce to next cycle); the
  append-only event log is disk-based, background-flushed, never blocks a
  cycle.
- ✅ **MM event log fully isolated from the production app database**
  (George, 23-07). It is not a transactional DB at all: one local append per
  cycle (few KB, sequential) → shipped asynchronously (log stream / object
  storage) → analysis store built from it later only if needed. The app never
  reads MM cycle records; the MM reads the log only at boot (state snapshot +
  tail replay for fast recovery). MM disk/log-shipping failure must never be
  able to touch the app (failure-domain isolation).

## 2026-07-22 — Share capacity + working process

- ✅ **Per team: 5,000,000 shares available for LONGS and 5,000,000 available
  for SHORTS** (learned 21-07, recorded by George 22-07). Supersedes the
  sheet's 875k float basis for capacity purposes; consistent with the IPO
  module's 5M float. ⚠ Consequences: the QA 1,000-share short reserve is a
  test config, not the product number; and **inventory-as-%-of-float maths
  (the skew gain λ) must be re-based** — 5M base vs 875k changes the
  effective gain ~5.7×. See [[market-maker/parameters]].
- ✅ **Working process established:** [[market-maker/working-guide]] +
  `sessions/` log + CLAUDE.md rule — any MM work starts by reading the guide,
  every session ends with a session note + working-doc updates.

## 2026-07-22 — Platform reality map (`trading-architecture.md` v1.0, live-verified)

> **Filter applied (George, 22-07): platform + venue facts from this doc are
> adopted as fact. Anything about the MM's own design (the `sdmm.py`
> prototype, its parameters, the "decided" 200 ms full-replace cadence,
> MM-as-user-account identity, the `gateway.orders.mm.*` seam) is treated as
> SUGGESTION ONLY — we design the MM from scratch. Those items live in
> open-questions as inputs, not here as decisions.**

**Adopted — venue facts (all test-verified, dates in source doc):**
- ✅ **Universe is 170 symbols: 32 NFL + 138 NCAA** (tickers `IPTC****`) —
  supersedes the standards' 163/131 count everywhere in this component.
- ✅ **tZERO has NO quote/mass-quote interface** — FIX schema is order-based
  only (D/F/G/8/9). Any MM is an order-based MM shaping the book with resting
  limit orders. (Closes T7.)
- ✅ **Limit orders only** (gateway hardcodes 40=2); **TIF = DAY / GTC / GTD
  only** — IOC and FOK do not exist in the venue spec.
- ✅ **No venue price band by default** — $0.01 and $1,000,000 limits both
  accepted verbatim. BUT the OMS Account/Position spec exposes a per-account
  collar (`LmtCents` + enforcement toggles) and wash-trade blocking — asks
  filed to enable on user accounts. Self-collar remains mandatory.
- ✅ **Shorts verified** (side=5): 1,000-share/security reserve ceiling,
  pre-trade enforced; stock-loan fee charged per short execution (absolute $,
  delivery not yet live on tZERO's side).
- ✅ **Session behaviour**: daily sequence reset 23:59 ET; resting DAY orders
  SURVIVE disconnects (cancel-on-disconnect empirically OFF) — a dead MM's
  stale quotes rest until end of day unless actively cancelled.
- ✅ **MM account mechanics exist in the OMS spec**: `UAAR` (create, with
  `MMType` + initial buying power), `UEPR` (seed per-symbol inventory),
  `UBT` (cash transfers). Entitlement ask filed. (T1 mechanism in hand.)
- ✅ **Our-side throughput is a non-issue**: Go gateway hot path measured
  ~460k orders/s/core. Binding constraint = tZERO's per-account
  `MaxOrdRate` + sustained-load authorization (ask filed). (Reframes T2.)

**Adopted — platform facts:**
- ✅ FIX gateway (Go) is live + battle-tested; two sessions (OE+MD); 170
  symbols subscribed; only 6 quoted two-sided in QA today.
- ✅ **Gateway gap #1: no outbound cancel (35=F) or cancel/replace (35=G)
  exists.** Cancel-system build committed 22-07 (owner Hasan) — includes an
  MM intake namespace, dead-man switch, Redis open-order index. Everything
  MM-shaped queues behind this build.
- ✅ Two trading planes: primary/IPO (internal, no venue) vs secondary (tZERO
  ATS). **The MM lives on the secondary plane only** — IPO fills never touch
  it.

**Adopted — economics (pending Edwin sign-off):**
- ✅ The client's real NFL IPO sheet exists and its economics decode to
  **`ESV = OffField + $5.00 × ExpectedWins`** — additive, arithmetic verified
  across all 32 rows. So **$/win = $5.00** (provisional). Float =
  **875,000/team**; price cap **$127.50**, floor 1 tick.
- ⚠ **Settlement definition** (what actually pays at season end) elevated to
  the single most important Edwin question.
- ⚠ **NCAA secondary-market scope for season 1 is OPEN** — the sheet covers
  32 of 170; NFL-only secondary is a live possibility.

**Noted as suggestions only (NOT adopted — MM is built from scratch):**
- The `sdmm.py` Phase-1 prototype and its Avellaneda-Stoikov formulation.
- Its proposed parameters (2-tick half-spread, λ 1500¢/100% float, 3
  levels/side, 6,000 sh/side, 2^k weights).
- The 200 ms full-per-team-cancel-replace cadence framing.
- MM identity as an individual user account.
- The `gateway.orders.mm.*` intake namespace (the platform's *offered* seam —
  our design may use it, but it doesn't bind the MM's architecture).

## 2026-07-20 — Market-maker Q&A (Edwin + Troy) — [[20-07-2026-touchdown]]

- ✅ **Scope: Novosapien builds CTS-001 and CTS-002** as well as PTS-001.
  George asked build-or-consume directly; Edwin: "We will build them." The
  matching engine / order book remain T0's.
- ✅ **Valuation formula given** (fills CTS-001's missing Section 3):
  `price = P(win this game)×$/win + E[remaining wins]×$/win + off-field`.
  Sport Radar live win probabilities are the input.
- ✂ **Unlimited capital — PTS-001 Ch 5 (Portfolio Allocation Engine)
  descoped.** Edwin: "The market maker will never have a limit on what it can
  do on capital"; buying power set to ~$100M–$100B. No finite pool, no
  zero-sum allocation. Per-team displayed-size config survives.
- ✅ **MM entity = ordinary participant + unlimited buying power + short-locate
  exemption.** T0 to stand up the synthetic MM entity in QA (asked via the new
  Tue/Thu T0 tech calls).
- ✅ **Limit orders only, including for the MM** — aggression via pricing
  through levels (bid 11 on a 7-at-8 market to sweep to 10).
- ✅ **Reference Price = the mid** between best bid and best ask.
- ✅ **Quoting = base spread ± per-side offsets around RP, with inventory
  skew** (long → offer drops toward RP to offload) — matches PTS-001 Ch 6.
- ✅ **Randomizer on quoted sizes** + occasional randomized **aggressive
  orders** that deliberately move price to exit inventory. ⚠ The aggressive
  behaviour goes beyond PTS-001's passive quoting — needs explicit bounds.
- ✅ **Cadence: cancel-replace ~5–10×/sec** intragame ("wipe the book and
  replace it"), plus event-triggered recompute. George's 200ms-baseline +
  event-trigger model approved by Troy for intragame.
- ✅ **Three liquidity sessions** — in-game / around-game / overnight
  (overnight deliberately wide, ~$2.5–5 spreads).
- ✅ **Markets truly isolated intragame**; each game a pairs trade; no
  rankings/tiebreaker effects; cross-game effects only between games.
- ✅ **Price band (~30%) + trade busting with T0** required for orderly
  markets — policy sessions "over the next couple of days."
- ✅ **NEW BUILD: synthetic market order** (app-side price-through) — before
  the first NFL game. Troy to help with logic. "A market order means whatever
  you get, you get" — no user-facing bounds.
- ✅ **NEW BUILD: MM ops desktop UI** — params, order lookup, positions, P&L;
  Kevin likely operates; sequenced last; first desktop surface of the app.
- ✅ **Priorities: challenge = stability first, profit last. Production =
  profit first** (if InPlay becomes its own MM — Edwin would open another
  company for it).
- ✅ **Terminology: "market state"** is Edwin's word for the condition/profile
  layer (not "market conditions").
- ⚠ **The standards are context, not constitution** — Edwin: "I meant it for
  Claude to read." Season-1 conformance bar to be signed off explicitly
  (Thursday 23-07).
- ✅ **T0 cadence: two tech calls/week (Tue + Thu)** from this week.
- ✅ **Deep-dive booked: Thursday 23-07, 3–4pm London.**

## 2026-07-15 / 17-07 — Standups — [[15-07-2026-touchdown]] · [[17-07-2026-touchdown]]

- ✅ **IPO fill guarantee / float warehousing:** the MM warehouses unsold IPO
  float in max clips (~50k), guaranteeing ~35% (possibly up to 50%) of every
  float — the straw-buyer mechanism. (15-07)
- ✅ **Reference-price blend** (on-field probability + off-field) named as the
  price driver; **load-balancing algo vs market-making algo** distinction
  raised — boundary still unclear. (17-07)
- ✅ Randomized, non-uniform quote sizes flagged (book must not read as a
  machine). (17-07)

## 2026-07-17 (commit) — Standards received

- ✅ CTS-001 / CTS-002 / PTS-001 master drafts (PDFs dated 01–02 Jul) mirrored
  into [[standards/README|standards/]] via `feat/technical-standards`.
- ⚠ CTS-001's Section 3 (valuation mathematics) absent from the converted
  copy — referenced throughout, file ends at §2.33.

## 2026-07-21 — Structure decisions (this vault)

- ✅ Component named **market-maker**, umbrella over all three standards +
  new build items, with custom `systems/` + working-docs structure (this
  folder) instead of the standard component/sub-component pattern.
- ✅ Clarified I/O direction of the profile layer (condition/session in →
  spread/depth/refresh targets out) and the three-role bust model
  (participant / venue / operator) — see
  [[market-maker/systems/market-supervision]].
