# InPlay Trading Challenge — Market Maker

> **Vision:** [[vision]]
> **Date:** 2026-07-20 · restructured 2026-07-21 · v1 model set 2026-07-23
> **Status:** **v1.3 Build Spec adopted as baseline (24-07)** — supersedes the CTS/PTS standards for implementation (`standards/MM-build-spec-v1.3.html`). E11/E12 answered by the spec; conflicts **E17–E19** + SR items **S6/S7** open with InPlay. **Build started:** `inplay-market-maker` (Python)
> **Owner:** Kevin Murray (Head Execution Trader) / George Westbrook (engineering) / Edwin (co-build, domain expertise)
> **Sources:** _[[12-06-2026-touchdown]], [[15-06-2026-touchdown]], [[17-06-2026-touchdown]], [[24-06-2026-touchdown]], [[29-06-2026-touchdown]], [[15-07-2026-touchdown]], [[17-07-2026-touchdown]], [[20-07-2026-touchdown]]_ · [[standards/README|the CTS/PTS standards]]

> ⚠️ **Custom structure.** This component deliberately does NOT follow the
> standard component/sub-component pattern. It's an internal engineering
> system, not a user-facing feature — so it's organised as `systems/` (one doc
> per buildable system) plus living working docs (decisions, open questions,
> parameters, plan, glossary). Promoted from a candidate `trading/market-maker`
> sub-component on 20-07-2026 after the market-maker Q&A with Edwin and Troy.

---

## What This Component Does

The Market Maker is an **internal, non-user-facing** market participant
operated by InPlay. It posts **resting liquidity** — passive two-sided bid/ask
limit orders — into T0's order book for every team market, so that from a
user's perspective there is always a potential to buy and always a potential
to sell. It is not a required counterparty: user orders that match each other
fill directly; the market maker's orders are simply always there alongside
them. (Source: standup 2026-07-20)

Its jobs, in priority order for the trading challenge (profit-seeking is
explicitly at the bottom during the challenge):

1. **Maintain stable, orderly market conditions** — two-sided liquidity in every market
2. **Guarantee IPO fill** — warehouse unsold primary-offering float so no offering reads as zero sales (see [[ipo-module/ipo-module]])
3. **Generate market data** — the challenge run produces the behavioural dataset used to model risk tolerance, spread tightness, and depth, and to pitch production market makers

In production the hierarchy flips: if InPlay becomes its own market maker
(Edwin: open another company and do it themselves if external MMs won't sign
at acceptable terms), **profitability moves to the top**. (Source: standup
2026-07-20)

**Scope (confirmed 20-07):** Novosapien builds the full stack — the valuation
engine (CTS-001), the market-operations layer (CTS-002, excluding T0's
matching engine), and the SDMM itself (PTS-001). Edwin: *"We will build them."*

## The One-Sentence Mental Model

> Quote two-sided ladders around a fair price we compute ourselves, sized
> generously, skewed to shed inventory — refreshed ~200ms during live games,
> every 30–60s otherwise — published to T0 deterministically, for every team,
> all season. v1 keeps it simple: orders rest until fully traded; on a price
> move, cancel and repost the remainder at the new price.

## System Map

```
Sport Radar (win probabilities, game events)
        │
        ▼
┌───────────────────────┐
│ VALUATION ENGINE      │  ESV = P(win)×$/win + E[remaining wins]×$/win + off-field
│ (CTS-001)             │  per team · per play during live games
└──────────┬────────────┘
           ▼
┌───────────────────────┐
│ MARKET STATE          │  publishes Reference Price (= ESV; frozen on feed failure)
│ (CTS-002)             │  condition classifier · profile · session (in-game/around/overnight)
└──────────┬────────────┘
           ▼
┌───────────────────────┐
│ QUOTING ENGINE (SDMM) │  decision cycle → reservation prices → ladders → sizes
│ (PTS-001)             │  → validate → cancel-replace into T0
│                       │  (live ~200ms · non-live 30–60s · earnings burst)
└──────────┬────────────┘
           ▼
     T0 order book  ◄──── users (Trading Service → FIX GW)
           │              limit orders only · price-time matching
           ▼
   fills (execution reports)
           │              ┌───────────────────────┐
           ├─────────────►│ MARKET SUPERVISION    │  bands (~30%) · halts · trade busts
           │              │ (separate from SDMM)  │
           ▼              └───────────────────────┘
   inventory feedback → next decision cycle
```

Plus two satellites: the [[market-maker/systems/mm-ops-ui|MM Ops UI]]
(desktop — params, positions, P&L; Kevin operates) and the
[[market-maker/systems/synthetic-market-order|Synthetic Market Order]]
(app-side "just buy it" mechanic; Edwin wants it before the first NFL game).

## Systems

| System | What it does | Status |
|--------|--------------|--------|
| [[market-maker/systems/valuation-engine\|Valuation Engine]] | Computes each team's fair value (ESV) from win probabilities + the revenue model | Inputs resolved 23-07 (SR live pull + Wednesday drop) · $5/win sign-off + E11 pending |
| [[market-maker/systems/market-state\|Market State]] | Publishes the Reference Price; classifies market condition; selects profile + liquidity session | Shape known · classifier ours to design |
| [[market-maker/systems/quoting-engine\|Quoting Engine (SDMM)]] | The bot: decision cycle, reservation prices, ladders, inventory skew, randomizer, cancel-replace | v1 model set 23-07 (rest-until-gone · bifurcated cadence) · numbers owed |
| [[market-maker/systems/market-supervision\|Market Supervision]] | Price bands, halts, trade busting — orderly-markets enforcement | Policy TBD with T0 |
| [[market-maker/systems/synthetic-market-order\|Synthetic Market Order]] | App-side market-order emulation via price-through crossing | Needed pre first NFL game |
| [[market-maker/systems/mm-ops-ui\|MM Ops UI]] | Desktop monitoring/control: algo params, order lookup, positions, P&L | Deliberately last |

## Working Docs

- **[[market-maker/working-guide]] — READ FIRST, every session.** The process:
  reading order, ground rules, the session loop.
- `sessions/` — one note per working session: what we did, learned, what went
  wrong, next. Newest note = where to pick up.
- [[market-maker/decisions]] — dated log of confirmed decisions + standard-doc supersessions
- [[market-maker/open-questions]] — live blockers with owners (Edwin / T0 / Sport Radar / us)
- [[market-maker/parameters]] — every tunable number: value, status, source
- [[market-maker/plan]] — build phases, dependencies, timeline anchors
- [[market-maker/glossary]] — terms + equation symbols in plain English
- [[market-maker/learnings]] — running log of distilled understanding (concepts that clicked, traps caught) — add every session

## Reference Material

- **THE spec (24-07):** `standards/MM-build-spec-v1.3.html` (+ source `.docx`) —
  the single authoritative build spec. Everything below is historical context.
- Plain-English guides: [[standards/CTS-001-plain-english-guide]] ·
  [[standards/CTS-002-plain-english-guide]] · [[standards/PTS-001-plain-english-guide]]
  (HTML renderings alongside each)
- Interactive map: `standards/sdmm-machine.html` — clickable engines + equations
  with symbol glossary, reconciled with the 20-07 touchdown
- The source standards ([[standards/README|standards/]]) are AI-generated
  context docs (Edwin: *"meant for Claude to read… they're fairly simple"*).
  Where they conflict with recorded decisions, [[market-maker/decisions]] wins.

## Boundaries

- **T0 owns:** the order book, matching (price-time), order lifecycle, trade
  records, and bust execution. Our MM is a participant; our supervision role is
  the operator's agent acting *through* T0.
- **[[trading/trading|Trading]] owns:** the user-facing order flow. The
  synthetic market order is specced here (it exists because of MM mechanics)
  but ships in the app.
- **[[earnings-report/earnings-report|Earnings Report]] owns:** the off-field
  EST/ACT mechanics that feed the valuation engine's off-field term.
- **[[ipo-module/ipo-module|IPO Module]] owns:** primary issuance; the MM's
  role there is fill guarantee / float warehousing (max clips ~50k,
  guaranteeing ~35–50% of every float — mechanics open on the T0 ledger side).
- **[[architecture/open-questions]]** tracks the MM rows in the global list.
