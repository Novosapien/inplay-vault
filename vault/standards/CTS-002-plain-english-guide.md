# CTS-002 in Plain English — Market Operations (how the market runs)

> **Companion to:** [[standards/CTS-002-market-operations-standard]] (the authoritative source)
> **Audience:** Someone with no exchange-operations background who needs to understand — and now build — this system.
> **Status:** Derived explainer. Where this guide and the source disagree, the source wins — **except** where the [20-07 touchdown](#8-what-the-20-07-touchdown-changed) supersedes it (Edwin's spoken word beats the generated doc).
> **Scope note (20-07):** Edwin confirmed CTS-001/002 are Novosapien builds ("We will build them") — but in our stack a big chunk of this document (the order book and matching) is **tZERO's job**, and much of the rest gets absorbed into the SDMM service. §9 maps who owns what.
> **See also:** [[standards/CTS-001-plain-english-guide]] · [[standards/PTS-001-plain-english-guide]]

---

## The 30-second version

CTS-001 answers *"what's a team worth?"* PTS-001 answers *"how does the market-maker bot behave?"* CTS-002 is the layer between them: **the rulebook for running the market itself.**

It does five jobs:

1. **Publish the price anchor.** Take the ESV from CTS-001 and republish it, unchanged, as the **Reference Price** — the number the whole market orbits.
2. **Track whether the market is healthy.** The **Market Operating Condition**: are the data feeds alive, is valuation flowing, can we operate normally right now?
3. **Say what the market should look like.** The **Market Operations Profile**: given the health and the game state, how tight, deep and fast should the market be?
4. **Define the rules of engagement.** What order types exist, how orders match (best price first, then first-come-first-served), what states an order moves through.
5. **Define who provides liquidity.** In the simulation: the SDMM. In production: real market-making firms.

One sentence to keep: **CTS-001 determines value. CTS-002 runs the market around that value. Neither may do the other's job.** The market operations layer is explicitly forbidden from ever calculating, adjusting or second-guessing a price — it publishes the valuation it's given and manages everything *around* it.

---

## 1. Market-operations basics (skip if you know this)

Think of an **airport** (the exchange) versus the **planes** (prices):

- Air-traffic control doesn't decide where planes fly — it decides whether the runway is open, in what conditions, and in what order planes land. CTS-002 is air-traffic control: it never sets prices, it operates the environment in which prices happen.
- Sometimes visibility drops and operations degrade — fewer landings, wider spacing. That's the Market Operating Condition driving the Market Operations Profile.

Vocabulary:

| Term | Plain meaning |
|---|---|
| **Reference Price (RP)** | The ESV, republished as the market's price anchor. By law `RP = ESV`, always. Edwin confirmed: it's the mid between bid and ask. |
| **Market Operating Condition (MOC)** | Health classification of the market: *Normal · Degraded · Protective · Recovery · Emergency*. Edwin's term for this whole layer: **"market state."** |
| **Market Operations Profile (MOP)** | The target market shape for the current condition: spread, depth, refresh speed, protection level. *What it should look like*, not *how quotes are made*. |
| **Market Lifecycle** | Whether this security's market may operate at all: *Pre-IPO → IPO → Pre-Market → Open Market → Settlement → Archived*. |
| **Operational Lifecycle** | How an open market behaves through the season: *Pre-Game → Live → Post-Game → Weekly Report*, repeating per fixture. |
| **Market Interaction Framework (MIF)** | The participant rulebook: order types, matching priority, order lifecycle. Identical rules for everyone — including the market maker. |
| **Price-time priority** | Matching order: best price wins; among equal prices, earliest order wins. |
| **Liquidity provider** | Whoever keeps two-sided quotes alive. Simulation: the **SDMM**. Production: a **PLP** (real firm, real capital). |
| **Protected Reference Price State** | Failure mode: if valuation stops publishing, the last valid RP stands frozen. Nobody may estimate a replacement. |
| **Halt / band / quote-bust** | Orderly-market tools: pause trading, reject prices outside a band (~±30%), or cancel ("bust") a trade that printed at a silly price. |

---

## 2. Where CTS-002 sits — and its one hard rule

| Document | Role |
|---|---|
| **CTS-001** | Determines value (ESV). Wins any conflict about valuation. |
| **CTS-002** — this document | Runs the market around that value. Wins any conflict about market operation. |
| **PTS-001** | The simulation market maker — implements both within one bot. |

The hard rule, repeated obsessively in the source: **CTS-002 SHALL NOT determine, modify, reinterpret or replace the Expected Settlement Value.** The whole document is machinery for operating *around* a number it is never allowed to touch.

---

## 3. The seven operating principles (Ch 1)

1. **Fair** — same rules for every participant, no preferential treatment.
2. **Orderly** — continuous, sensible trading whenever the state permits; no chaos, no silly prints left standing.
3. **Continuously liquid** — executable two-sided quotes whenever the product standard requires them.
4. **Operationally independent** — running the market never changes the valuation.
5. **Deterministic** — same inputs → same operational decisions, every implementation.
6. **Resilient** — degraded conditions produce controlled degradation (wider, thinner, slower), not blank screens.
7. **Auditable** — every operational decision reproducible and permanently recorded.

Same DNA as the other two documents: determinism + auditability + separation of powers.

---

## 4. The two lifecycles (Ch 2) — the product's temporal skeleton

**Market Lifecycle** — may this market operate at all?

```
Pre-IPO → IPO → Pre-Market → OPEN MARKET → Settlement → Archived
```

- *Pre-IPO:* nothing public. *IPO:* primary issuance, subscriptions only, no secondary trading. *Pre-Market:* shares issued, RP publishing, infrastructure warming up. *Open Market:* trading live — everything else in the stack only exists here. *Settlement:* season done, rights final, ESV converges to the actual payout, trading ends. *Archived:* history retained for replay/audit.

**Operational Lifecycle** — the season rhythm inside Open Market, per fixture:

```
Pre-Game → Live → (Official Review) → Post-Game → Weekly Financial Report → Pre-Game …   ×18 weeks
final contest: Final Post-Game → Final Financial Report → Settlement
```

- States are **per game**: the Cowboys can be Live while the Packers are Post-Game.
- The **Weekly Financial Report** is a lifecycle driver — publishing it is what rolls the week over. (Open question: who produces it?)
- **20-07 addition (Troy):** three liquidity *sessions* hang off this rhythm — **in-game** (tight, fast, 5–10 quote refreshes/sec), **around-game**, and **overnight** (deliberately wide, ~$2.5–5 spreads — "let the market at least tell you where it is"). The session determines the profile.

---

## 5. The price and health layer (Ch 3–5)

**Reference Price (Ch 3).** `RP_t = ESV_t` — an identity, not a calculation. Publication carries timestamps, states and version so any published price can be reconstructed. If valuation stops flowing → **Protected Reference Price State**: freeze the last valid RP; no subsystem may invent a substitute. (This is the "what if Sport Radar dies mid-game" answer: the market keeps quoting around the frozen price, wide and defensive, until valuation resumes.)

**Market Operating Condition (Ch 4).** `MOC = F(inputs)` where the inputs are valuation availability, feed health/latency/staleness, system health, and lifecycle states. Classifications: *Normal · Degraded · Protective · Recovery · Emergency*. Famously, the source says **"Do NOT define F"** — a leftover generation instruction that confirms the classifier logic is deliberately ours to design. MOC measures *capability only*; behavior is the next layer's job.

**Market Operations Profile (Ch 5).** Maps (RP, condition, lifecycle states, config) → the target market shape: spread profile, displayed liquidity, depth, refresh, aggressiveness, inventory posture, protection level. Named profiles: *Stable · Active · Balanced · Defensive · Recovery · Emergency*. The mapping function G is never defined — also ours. Indicative starting proposal: Normal→Stable/Active/Balanced, Degraded→Defensive, Recovery→Recovery, Emergency→Emergency.

*(Note: PTS-001's pricing profiles are a slightly different six — Stable/Active/Defensive/Recovery/Liquidity-Preservation/Protective. The two lists never quite reconcile in the docs. In the build there will be one profile set; flag for Thursday.)*

---

## 6. The rules of engagement (Ch 6) — the Market Interaction Framework

**In our stack this chapter is mostly tZERO's implementation** — but we must know it cold, because both the app and the SDMM live inside these rules.

- **Order types (v1):** Market, Limit, Cancel, Cancel/Replace. Nothing else — no stops, no icebergs, no pegs, no hidden orders. **In practice tZERO is limit-only** (no native market orders — see §8 on synthetic market orders).
- **Matching:** price priority, then time priority. Partial fills allowed; remainders keep their queue position.
- **Order lifecycle:** *New → Accepted → Working → Partially Filled → Filled / Cancelled / Replaced / Expired* — deterministic, recorded, auditable.
- **Validation:** every order checked against market state, order type, price/quantity constraints, tick size before acceptance.
- **Equal access:** identical interaction rules for every participant — *including the market maker*, which is legally just another participant (confirmed 20-07: same entity type as a user, plus near-limitless buying power).
- **Execution-model independence:** participant rules never change based on who's providing liquidity.

---

## 7. Liquidity provision and execution (Ch 7–9)

**Who provides liquidity (Ch 7).** Two recognized models:
- **SDMM** — simulation designated market maker: no real financial risk, no capital constraints, deterministic, educational. (The star of PTS-001.)
- **PLP** — production liquidity provider: real firm, real capital, real risk, regulatory obligations. (Future state. Edwin, 20-07: if real market makers won't sign at acceptable terms, "we'll open up another company and become the market maker" — and then profit moves to the top of the priority list.)

The split of responsibilities is clean: **the standard defines required market behavior; the provider owns its proprietary methods.** CTS-002 says *what* the market must look like; it never prescribes the quoting algorithm.

**How quotes get made (Ch 8–9).** The Liquidity Provider Execution Engine consumes (RP, condition, profile, config) and produces the **Executable Quotation** — which must always carry eight elements: bid, offer, bid size, offer size, depth, refresh profile, status, priority attributes. Chapter 9's "Market Construction Mathematics" defines the same idea more formally (config → quotation function) and adds the constitutional constraints: deterministic construction, market objects are inputs never outputs, identical externally-observable behavior across implementations, full deterministic replay of every quote and execution. Practically, Ch 8–9 are the *requirements spec* for what PTS-001 then designs in detail — if you've internalized the SDMM guide, you've already absorbed them.

---

## 8. What the 20-07 touchdown changed

- **We build this.** But the matching engine and order book are tZERO's — CTS-002's Ch 6 machinery is consumed, not built. (And the docs themselves were "meant for Claude… fairly simple" — architecture over ceremony.)
- **"Market state"** is Edwin's word for the MOC/MOP layer. Use his vocabulary on calls.
- **Trading bands + quote busting are real requirements**: ~30% band around the reference; fills outside it can be busted "as the exchange or with tZERO… we have to maintain orderly markets." Policy to agree with tZERO in the coming days.
- **Synthetic market orders are a new build item** (app-side): tZERO has no market orders, but users will expect a "just buy it" button. Implementation: price through several levels (buy the 12s when it's 8 bid at 9) or a cancel-replace walk that chases until filled. Troy: this is exactly how real brokers fake market orders in equities; he'll help write the logic. **Edwin wants it before the first NFL game.**
- **Three liquidity sessions** (in-game / around-game / overnight) replace any elaborate reading of the lifecycle chapters — the practical question is just: which session are we in, and what profile does it select?
- **Cadence confirmed:** 5–10 quote refreshes/sec intragame via cancel-replace ("wipe the book and replace it"), event-triggered recompute on game events, wide-and-slow outside games.
- **MM ops UI is a build item** (desktop): set algo parameters, order lookup, positions, P&L. Kevin likely operates it. Deliberately last in the build order.

---

## 9. Who owns what — the build map

| CTS-002 piece | Owner in our stack | Build shape |
|---|---|---|
| Reference Price publication (Ch 3) | **Novosapien** | Thin pipe: valuation service output → published per team (`RP = ESV`), plus the frozen-price fallback state. |
| Market Operating Condition (Ch 4) | **Novosapien** | Small classifier inside/beside the SDMM service: feed health + valuation freshness + session → one enum. Mostly "Normal." |
| Market Operations Profile (Ch 5) | **Novosapien** | Config lookup: (condition, session) → profile parameters. Merges with PTS-001's pricing profiles into one table. |
| Lifecycles / sessions (Ch 2) | **Novosapien** | State machine driven by fixture schedule + Sport Radar event status. Drives everything else's timing. |
| Order book, matching, order lifecycle (Ch 6) | **tZERO** | Consumed via FIX. We validate app-side before submission but tZERO is authoritative. |
| Synthetic market orders | **Novosapien (app)** | New: price-through / cancel-replace walk. Pre-first-NFL-game. |
| Bands, halts, quote-bust (Ch 6/integrity) | **Joint with tZERO** | Policy + who pulls the trigger. To agree on the Tue/Thu calls. |
| Liquidity provision (Ch 7–9) | **Novosapien** | This *is* the SDMM service — see PTS-001 guide. |
| Ops audit / replay | **Novosapien** | Event-sourced records from day one; replay tooling later. |

---

## 10. Quirks and open questions

**In the source document:**
- **"Do NOT define F"** (§4.4) — a generation instruction left in the text. Harmless, but hard evidence the doc is AI-drafted context, and that the classifier is deliberately unspecified.
- **Profile-name mismatch** with PTS-001 (*Balanced/Emergency* vs *Liquidity-Preservation/Protective*). One merged profile set needed.
- **Ch 5 vs Ch 9 overlap** — the Market Operations Profile and the Market Configuration describe near-identical objects at different levels of formality. Build one thing.
- **Market orders** are a recognized type in Ch 6 but don't exist on tZERO (Troy). Synthetic market orders resolve this at the app layer.
- Formatting drift: broken bullet nesting, an underlined equation, sections that trail off — same conversion artifacts as the other docs.

**Genuinely open:**
1. **Band width and bust policy** — 30%? Who busts, us or tZERO, and how fast?
2. **Halt semantics** — what can halt a single team's market intragame, and who decides?
3. **Weekly Financial Report** — who produces it, what's in it, when does it publish?
4. **MOC classifier thresholds** — what feed-latency/staleness actually flips Normal → Degraded?
5. **Session boundaries** — when exactly does in-game become around-game become overnight (esp. NCAA's 6-day weeks)?
6. **Throughput** — 5–10 cancel-replaces/sec × 32+ books through tZERO's FIX session: confirm limits on the Tue/Thu calls.

---

## 11. TL;DR mental model

Air-traffic control for the sports stock market:

- **Publishes** the fair price it's given (never edits it — frozen if the feed dies).
- **Watches** health (feeds, valuation, systems) → one condition per market: Normal → … → Emergency.
- **Dictates shape**, not prices: tight/deep/fast in-game, wide/thin overnight, defensive when degraded.
- **Enforces the rulebook**: limit orders, price-time priority, equal rules for everyone including our own bot — with bands and busts to keep prints sane.
- **In our stack:** matching belongs to tZERO; nearly everything else here collapses into config, a couple of state machines, and policy agreements — absorbed into the valuation and SDMM services rather than standing alone.
