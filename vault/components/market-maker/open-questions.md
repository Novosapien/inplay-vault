# Market Maker — Open Questions

> **Component:** [[market-maker/market-maker]]
> **Purpose:** The live blocker list, by owner. Update after every touchdown /
> T0 call. Global architecture questions live in
> [[architecture/open-questions]]; this is the MM-specific working list.

**Next scheduled venues:** T0 tech calls Tue + Thu · written blocking
questions to InPlay per spec §1.6-1.

**Priority (reset 24-07 after the v1.3 spec landed):** E17 quote lifecycle →
E18 cadence → E19 remaining-season probability source → S6 tie probability →
S7 SR product/quota ask → spec Ch 14-A ▸ value approvals → B-3…B-10 business
decisions. E11/E12/E1/E5/E14 are **answered by the spec** (see below).

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
| E1 | ~~Sign off $5 per win~~ **✅ RESOLVED 24-07 (v1.3 spec §3.1.2):** $5.00/win both leagues, plus a **$2.50 tie value** — new, never mentioned on a call | Valuation | ✅ Resolved |
| E2 | ~~Off-field: which number goes into the price?~~ **✅ RESOLVED 23-07:** Edwin's **popularity index** — ~$14–30 per team, static at the start, already inside the NFL IPO prices, refreshed in the **Wednesday data drop**. Residual: how the EST/ACT earnings mechanic interacts with it long-term — deferred | Valuation | ✅ Resolved (residual deferred) |
| E3 | **Opening prices** — who calculates each team's starting price at IPO, and from what? (NFL sheet exists; NCAA owed). **24-07: NCAA in motion** — Cody delivered the NCAA football team totals; Edwin updating the NCAA IPO prices and pushing them into the app same day. (Source: standup 2026-07-24) | Valuation, IPO | 🟡 NFL known / 🟡 NCAA in motion |
| E4 | **Edwin's old simulation code** — he's sending the original market-maker Python files ("functional, not a heavy lift") | Calibration | 🟡 In motion (23-07) |
| E5 | ~~All the pricing numbers~~ **✅ RESOLVED 24-07 (v1.3 spec §5.2/§5.6/§5.7/§12.2):** spreads $0.10/$0.20/$0.40, levels 3/2/1, sizes 10k/7.5k/5k, skew S=$1.00 cap $0.25. Most are ▸ proposed — build the mechanism as given; final values await InPlay approval (spec Ch 14-A) | Quoting | ✅ Resolved (▸ values pending) |
| E6 | **Week-zero college games** — how to price massive-mismatch openers | Valuation | 🔴 Open (Cody to ask) |
| E7 | **How strictly do the standards bind for season 1?** — which rules bend for launch (replay tooling, audit depth, the quote-aging chapter)? | Everything | 🟡 Needs explicit sign-off |
| E8 | **Limits on deliberate price-moving** — Edwin described the MM occasionally moving the price on purpose to exit stock. What bounds make that acceptable? (Agreed: not in v1) | Quoting, integrity | 🔴 Open |
| E9 | **Weekly Financial Report** — who produces it, what's in it, when | Market state, settlement | 🔴 Open |
| E10 | **The missing valuation-math chapter** — CTS-001 §3 is referenced everywhere and absent from our copy. Request the PDF | Valuation | 🔴 Open |
| E11 | ~~What does a share actually pay out at season end?~~ **✅ RESOLVED 24-07 (v1.3 spec §11.3):** `FSV = realized on-field + realized off-field` — $5/win + $2.50/tie summed over the regular season, plus the realized off-field pools. It IS the simple answer: the pricing engine is a live estimate of that number | Everything | ✅ Resolved |
| E12 | ~~Do NCAA teams trade this season?~~ **✅ RESOLVED 24-07 (v1.3 spec §2.5):** yes — 170 securities, evaluated 24 h/day | Scope, plan | ✅ Resolved |
| E13 | ~~How is "expected remaining wins" calculated?~~ **✅ RESOLVED 23-07:** produced **internally by InPlay, weekly** (Sport Radar doesn't do season totals — futures aren't updated); Edwin helping automate; delivered in the Wednesday drop | Valuation | ✅ Resolved |
| E14 | ~~Which share count for the skew?~~ **✅ RESOLVED 24-07 (v1.3 spec §4.3):** the denominator is **Reference Float = issued − treasury**. Actual share counts follow from issuance | Quoting | ✅ Resolved |
| E15 | ~~When a play happens, what moves the price?~~ **✅ RESOLVED 23-07:** just Sport Radar's live win probability, pulled directly — no own event weights in v1 ("you don't have to create it") | Valuation | ✅ Resolved |
| E16 | **Is trading just… on, all day?** — the v1.3 spec implies yes (24 h/day evaluation, no sessions, no auctions mentioned) but doesn't say it outright. Confirm with T0 on the venue side (T9) | Market state | 🟡 Spec implies yes — confirm |
| E17 | **Quote lifecycle — spec vs what you said (NEW 24-07, conflict):** the spec tops orders back up once half-eaten after 15 s (§5.9); on the 23-07 call Edwin said "rest until completely gone, no top-ups ever". Which one is v1? | Quoting engine | 🔴 **Blocking question** |
| E18 | **Live cadence — spec vs what you said (NEW 24-07, conflict):** the spec sweeps every 2.0 s and calls a 5 s-old probability "Current" (§3.1.4, §3.3.1); on the call Edwin said ~200 ms, "a second's too long". Which one is v1? | Valuation, quoting | 🔴 **Blocking question** |
| E19 | **Where does the rest-of-season number come from? (NEW 24-07, conflict + proof):** the spec demands per-game probabilities for all ~2,400 games from season open (D-1) and bans internally-generated probabilities (§1.5) — but SR prices games **rolling** (verified: NCAA 70 of ~1,700 today), so Σ GEV(g) can't be computed from SR alone. Options: (a) SR season win totals for the unpriced tail — NFL verified, NCAA absent; (b) InPlay-internal weekly (Edwin's own 23-07 model) via a §1.5 Change Order; (c) both. Needs a ruling. **24-07 touchdown signal:** Edwin re-affirmed the internal model live on the call — "I'll come up with a piece that you can pull… I'll build that model", agreeing SR doesn't give week-20 probabilities from week 1; George offered deriving rest-of-season probabilities from SR on-field data; a **weekly manual input via the MM platform** (e.g. Tuesdays) floated for on/off-field figures. Edwin: "we'll work that out over the next few days." (Source: standup 2026-07-24) | Valuation | 🔴 **Blocking question** |

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
| T11 | **What self-match prevention does T0 have?** — Troy checking (23-07). Relates to the per-account wash-trade toggle in the OMS spec. For USER wash-trading the v1 policy is rulebook ban + order queries on high-volume accounts + removal from the event. ⚠ NEW 24-07: the v1.3 spec **assumes** a matching-engine MM self-trade-prevention group (§11.2) — but tZERO's OE spec has no ExecInst/STP at order entry. Reconcile with Troy | Supervision | 🟡 Troy checking — spec tension added |

## Owed by Sport Radar

| # | Question | Blocks | Status |
|---|----------|--------|--------|
| S1 | ~~The probabilities API is broken~~ **🟡 DOWNGRADED 24-07:** the Probabilities product **works on the trial key** (live-verified 200s; NCAA + NFL priced games returned). The 403s were entitlement/key placement, not a broken API. ⚠ Correction (George, 24-07): we **already hold the production master key** — the ask is the Probabilities product being **allocated to that master key in the production environment** (works in trial/dev today), plus quota (S7). Trial key placed in the service's `PROBABILITIES_API_KEY` meanwhile | Valuation | 🟡 Production allocation pending |
| S2 | **More API allowance** — the trial quota is nearly half used; we need a production-sized allowance. 24-07: Cody claims limits are effectively unlimited at the real-time tier post-API-reshape — folded into the S7 email/ask | Valuation | 🟡 Cody on it — via S7 email |
| S3 | **Do they push updates to us, or do we keep asking?** — sets how stale our prices can get, and whether we can even measure the feed's delay | Valuation cadence | 🔴 Open (long-standing) |
| S4 | **Our probabilities must not lag the sportsbooks** — if the feed is behind DraftKings/FanDuel, users pick the MM off ("too easy for people to make money"). Cody owns getting the right feeds. **🟡 Partially mitigated 24-07:** Cody confirmed the **probabilities API runs off SR's betting-side feed** — faster than the media feeds that power the gamecast (the raw betting feeds themselves are licensed to sportsbooks only; InPlay can't buy them). The MM consumes the probability directly, so it moves at betting-feed speed; in-app users see events at the same time the MM does. Cody lobbying SR for the betting feeds in parallel (call early week of 27-07) — "we are more regulated than a sports betting market". (Source: standup 2026-07-24) | MM integrity | 🟡 Mitigated — Cody lobbying for betting feeds |
| S5 | ~~Can Sport Radar actually serve it?~~ **✅ RESOLVED 24-07 (code + live probes):** probabilities update **per play (~30–40 s)**, so nothing needs 200 ms polling — ~2 s per live game meets the spec's freshness bands (the decision cycle reads memory, never SR). **Simulation works today**: SR's playback host replays real recorded games (no auth, real-time) and a local JSONL fast-replay runs the same pipeline in seconds | Valuation, testing | ✅ Resolved |
| S6 | **No tie probability exists (NEW 24-07):** SR's feed is a 2-way home/away market — verified live. The spec requires win/**tie**/loss and forbids inferring a missing tie (§3.2.2). NFL games can tie. Needs an InPlay ruling: different SR product, provider tie-impossible flag, or a spec change | Valuation | 🔴 **Blocking question** |
| S7 | **The SR product/quota ask (NEW 24-07):** either **global AF probabilities v2** (its live-bulk endpoint = all live games in one call → ~200k calls/mo, 0.5 QPS — preferred; currently 403, separate package) or a production quota on the current product (~2.5M calls/mo, ~20 QPS peak NCAA Saturday). One line to SR via InPlay; feeds spec D-1. **Channel agreed on the 24-07 touchdown:** George emails **SR support + Scott + Cody**; Cody drives it commercially with Scott + David. Scope of the email (refined by George): (1) Probabilities allocated to the **existing production master key** (product works in trial/dev; same master key across all products), (2) production-sized **quota**. The **GAF Probabilities v2 ask is Cody-gated** — check with Cody before requesting it from SR, since it's a separate product/package with commercial implications. Cody's framing: one master key forking into all products, published call limits "basically mean nothing" at the real-time tier, versioning doesn't matter. Treat as unverified until allocation lands. (Source: standup 2026-07-24) | Valuation cadence, cost | 🟡 Email owed by George — v2 ask gated on Cody |

## Ours to design (Novosapien)

| # | Question | Blocks | Status |
|---|----------|--------|--------|
| N1 | **How the price travels** — the pipe carrying each new fair value from the valuation engine to the quoting engine (likely a NATS topic per team). Ours; invisible to the book | Valuation → quoting | 🔴 Open |
| N2 | ~~One profile table~~ **✅ RESOLVED 24-07 (v1.3 spec §5.2 + §6):** the merged table exists — Stable / Active / Defensive / Suspended with spread, levels, and sizes per state | Market state, quoting | ✅ Resolved |
| N3 | ~~When do we stop trusting our inputs?~~ **✅ RESOLVED 24-07 (v1.3 spec §3.3–3.5):** freshness bands (live 5/10/20 s; pregame by time-to-kickoff), status ladder (Valid/Warning/Degraded/Invalid) with quoting effects, confidence deductions — all specified. ⚠ the live band numbers are inside the E18 cadence conflict | Market state | ✅ Resolved (E18 caveat) |
| N4 | **When does each session start and end?** — in-game / around-game / overnight, per team (NCAA plays 6 days a week). **Edwin decides, we implement** | Market state | 🔴 Open |
| N5 | **"Just buy it" button depth** — how many price levels through a synthetic market order reaches; chase it if unfilled, yes/no; how it interacts with the wallet check | Trading app | 🔴 Open — Troy assisting |
| N6 | **Two algos were named — where's the line?** — "load-balancing" vs "market-making" (17-07); nobody has defined the boundary | Architecture | 🔴 Open |
| N7 | **Service layout** — one MM service or several (valuation and quoting separate)? Where does it run? Ours, from scratch; the platform's offered plumbing is an input, not a constraint | Architecture | 🔴 Open |
| N8 | **How much replay tooling at launch?** — recording everything is cheap and mandatory; the tools to replay it are not. Where's the v1 line? | Quoting engine | 🟡 Proposal: record all, defer tooling |
| N9 | **The platform team's suggestions: accept or replace, one by one** — their prototype's formulas, their numbers, the 200ms full-refresh idea, the MM-as-a-user-account idea. All treated as input only; our from-scratch design accepts or replaces each explicitly | MM design | 🔴 Open |
| N10 | ~~Do quotes live one cycle, or get managed over time?~~ **✅ RESOLVED 23-07 — Edwin defined the lifecycle:** partially-filled orders **rest until completely gone** (no top-ups, no aging). On a price move: cancel the old level, post the **remaining** quantity at the new price. After a full fill at an unchanged price: reload at top of book. The standard's quote-aging chapter is moot | Quoting engine | ✅ Resolved |
| N11 | ~~Skew the sizes too, or just the prices?~~ **✅ RESOLVED 24-07 (v1.3 spec §5.7.2):** yes, both — the position-side modifier shrinks the long side's buy size and grows its sell size (0.50–1.50×, off Effective Position Ratio) | Quoting engine | ✅ Resolved |
| N13 | **What data the MM consumes, and how** — everything arrives pushed and sits in memory; the loop never reads a database. Proposed: the quoting engine needs only the fair price and its own orders; the venue's book feed is for the watchdog and monitoring, not for quoting (MD spec read 23-07 confirms the feed streams updates after one subscribe) | Architecture, supervision | 🟡 Proposed |
| N12 | ~~How old quotes become new ones each cycle~~ **✅ RESOLVED for v1, 23-07 (Edwin + George):** post the new quotes **without waiting** for cancel confirmations; a momentary self-cross during a price adjustment is acceptable ("on the first iteration… I don't care"). The 22-07 amend-in-place/reconciler analysis is **shelved, preserved in [[market-maker/learnings]]** for the augment-later phase | Quoting engine | ✅ Resolved for v1 |
| N14 | ~~Fill-response logic~~ **🟡 SPEC-ANSWERED 24-07, gated on E17:** the spec defines it mechanically (§5.9 — replenish below 50 % after 15 s; immediate on full fill / side empty / price move). But that mechanism IS the E17 conflict with Edwin's rest-until-gone. Resolves whichever way E17 does | Quoting engine | 🟡 Gated on E17 |

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

**24-07 v1.3 spec intake:** E1 ($5/win + $2.50/tie) · E5 (pricing numbers, ▸
pending) · E11 (settlement = realized on+off field) · E12 (NCAA in, 170) ·
E14 (float = issued − treasury) · N2 (state table §5.2) · N3 (freshness/status
§3.3–3.5) · N11 (sizes skew too, §5.7.2) · S5 (per-play updates + simulation
verified). ⚠ The 23-07 resolutions **N10/N12 (lifecycle), cadence, and E13
(internal weekly wins)** are contradicted by the spec — held open as
**E17/E18/E19**, not silently re-resolved.
