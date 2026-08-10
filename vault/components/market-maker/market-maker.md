---
description: "Component hub for the internal market maker and SNT-1 — system map, the seven-system table, working-doc index and ownership boundaries"
---

# InPlay Trading Challenge — Market Maker

> **Vision:** [[vision]]
> **Date:** 2026-07-20 · restructured 2026-07-21 · v1 model set 2026-07-23
> **Status (06-08b): the ingestion move is BUILT on both sides and drilled end to end.** The sportradar service polls SR and publishes on JetStream (⭐ George: **every successful fetch publishes** — the re-offer is the liveness signal; msg-id names the publish attempt); the MM consumes the bus — adapter parity with the file path proven 1,089/1,089 on the real capture, finals minted MM-side (N16), acks batched after the journal, and the local docker drill passed incl. restart with zero redelivery. **534 MM tests · 577 service tests**, all commits local. The in-engine poller retires **at go-live** (George) — the live composition switches to the bus then. Earlier state (05-08c): the machine RUNS, all 170 sr-id bindings verified in code — ⭐ George's ingestion ruling re-cut the live path. Chapters 3–8 + 12, the sweep event (N28), the clock-owning runtime, tiered polling, the 170-security universe, the composition, the live `HttpSource` + the seam's failure contract, and `mm/bindings.py::TEAM_BINDINGS` (163 exact + 6 profile-verified + the Rams via the mappings bridge) — **512 tests**, drill-proven on the rig 05-08. ⭐ E38 deviation built: **a successful fetch confirms the number** — full status through halftime; 20 s of true silence suspends. ⭐ **Ingestion ruling (George, 05-08c): the sportradar SERVICE polls SR and publishes on NATS — the MM consumes the bus and never calls SR itself.** The build had drifted from the 24-07 ingestion decision (polling absorbed into the engine); the move is **scoped in writing and approved before any build** (service work: git pull → branch off `dev`). Live mode refuses until: S1/S7 · the ingestion move · Edwin's file delivery (N19). ⚠ The 05-08b/c MM commits are LOCAL, deliberately unpushed. External: **T1** (→ Hasan, with N30 + the governor) · **E27** (the day-one book) · the unsent round **E29–E38**. Still owed: §10.3 checkpoints (required — every deploy is a restart) · the boot-reconcile healer (parked) · §3.6 off-field · Ch 9 IPO · Ch 11 settlement. Baseline: the **v1.3 Build Spec** (24-07), superseded where [[market-maker/decisions]] says so. Repo: `inplay-market-maker` (Python), branch `feat/position-engine` · **Meeting block (27-07 → 07-08, merged 10-08): IPO market structure settled + valuation inputs confirmed · 13 Aug dry run target · E11 settlement + E12 NCAA still unasked**
> **Owner:** Kevin Murray (Head Execution Trader) / George Westbrook (engineering) / Edwin (co-build, domain expertise)
> **Sources:** _[[12-06-2026-touchdown]], [[15-06-2026-touchdown]], [[17-06-2026-touchdown]], [[24-06-2026-touchdown]], [[29-06-2026-touchdown]], [[15-07-2026-touchdown]], [[17-07-2026-touchdown]], [[20-07-2026-touchdown]], [[24-07-2026-touchdown]]_ · [[standards/README|the CTS/PTS standards]]

> ⚠️ **Custom structure.** This component deliberately does NOT follow the
> standard component/sub-component pattern. It's an internal engineering
> system, not a user-facing feature — so it's organised as `build/` (the
> as-built source of truth, one page per part) + `systems/` (design docs for
> the UNBUILT systems only; built systems' design narratives are in
> `archive/`) plus living working docs (decisions, open questions,
> parameters, plan, glossary). Promoted from a candidate `trading/market-maker`
> sub-component on 20-07-2026 after the market-maker Q&A with Edwin and Troy.

---

## What This Component Does

The Market Maker is an **internal, non-user-facing** market participant
operated by InPlay. It posts **resting liquidity** — passive two-sided bid/ask
limit orders — into tZERO's order book for every team market, so that from a
user's perspective there is always a potential to buy and always a potential
to sell. It is not a required counterparty: user orders that match each other
fill directly; the market maker's orders are simply always there alongside
them. (Source: standup 2026-07-20)

> **Two house agents (from 30-07-2026).** This component now houses two internal, non-user-facing agents: the **Market Maker** (posts resting liquidity, the maker) and the **[[market-maker/systems/synthetic-noise-taker|Synthetic Noise Taker, SNT-1]]** (crosses the spread as a controlled-loser taker so every book trades from IPO onward). Edwin delivered a spec-quality SNT-1 reference implementation. The rest of this doc describes the Market Maker; SNT-1 has its own system doc.

Its jobs, in priority order for the trading challenge (profit-seeking is
explicitly at the bottom during the challenge):

1. **Maintain stable, orderly market conditions** — two-sided liquidity in every market
2. **Guarantee IPO fill** — ensure no offering reads as zero sales (see [[ipo-module/ipo-module]]). ⚠ **Re-based 31-07 / 03-08:** this is now done by the **taker algo buying from a separate broker-dealer MPID**, not by the MM warehousing float. The maker does not participate in the primary at all. See the 27-07 → 07-08 block in [[market-maker/decisions]]
3. **Generate market data** — the challenge run produces the behavioural dataset used to model risk tolerance, spread tightness, and depth, and to pitch production market makers

In production the hierarchy flips: if InPlay becomes its own market maker
(Edwin: open another company and do it themselves if external MMs won't sign
at acceptable terms), **profitability moves to the top**. (Source: standup
2026-07-20)

**Scope (confirmed 20-07):** Novosapien builds the full stack — the valuation
engine (CTS-001), the market-operations layer (CTS-002, excluding tZERO's
matching engine), and the SDMM itself (PTS-001). Edwin: *"We will build them."*

## The One-Sentence Mental Model

> Quote two-sided ladders around a fair price we compute ourselves, sized
> generously, skewed to shed inventory — refreshed ~200ms during live games,
> every 30–60s otherwise — published to tZERO deterministically, for every team,
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
│ (PTS-001)             │  → validate → cancel-replace into tZERO
│                       │  (live ~200ms · non-live 30–60s · earnings burst)
└──────────┬────────────┘
           ▼
     tZERO order book  ◄──── users (Trading Service → FIX GW)
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
| [[market-maker/build/valuation\|Valuation Engine]] | Computes each team's fair value from win probabilities + Edwin's daily T | ✅ **Built** (Edwin's on-field leg, freshness/status/confidence §3.3–§3.5, replay-proven on the real Chiefs–Ravens game) · off-field §3.6 still mocked |
| [[market-maker/build/market-state\|Market State]] | Permission to quote: Stable/Active/Defensive/Suspended per security, kill switch, promotion ladder | ✅ **Built 01-08** (Ch 6; classifier superseded by σ² — decisions 30-07b) · Active/Defensive widening awaits E31 |
| [[market-maker/build/quoting\|Quoting Engine (SDMM)]] | The bot: σ² → width → ladder → sizes → publish-or-hold → reconcile → gateway | ✅ **Built + wire-proven 02-08** (loopback test 5/5 vs the real gateway) · values 🟡 pending E31 · §5.5/§5.9 gated (Ch 8 book feed / E17) |
| [[market-maker/systems/market-supervision\|Market Supervision]] | Price bands, halts, trade busting — orderly-markets enforcement | Policy TBD with tZERO (T3–T5) · busts currently refuse-and-raise (T4) |
| [[market-maker/systems/synthetic-market-order\|Synthetic Market Order]] | App-side market-order emulation via price-through crossing | Needed pre first NFL game — not ours to build in the MM repo |
| [[market-maker/systems/mm-ops-ui\|MM Ops UI]] | Desktop monitoring/control: algo params, order lookup, positions, P&L | Deliberately last · will own CONFIGURATION_ACTIVATION + the N19 upload page |
| [[market-maker/systems/snt-1-noise-taker\|SNT-1 — the Market Taker]] | Edwin's house noise taker: crosses the MM's spread with random clips so every book prints trades | ⭐ **Built 08-08** (`src/snt/`, MM PR #10) · **NOT deployed** — blocked on the IPLP account, E32 rulings, E33/T13 compliance · requirements: [[market-maker/market-taker-requirements]] |

## Working Docs

- **[[market-maker/working-guide]] — READ FIRST, every session.** The process:
  reading order, ground rules, the session loop.
- **[[market-maker/build/index|build/]] — how the machine is ACTUALLY
  built.** The as-built SOURCE OF TRUTH, one page per part of the machine:
  key equations as implemented, real-vs-mocked-vs-gated, what we build
  next, the module map. For agents and humans; the anchor for changes.
- `sessions/` — one note per working session: what we did, learned, what went
  wrong, next. Newest note = where to pick up.
- [[market-maker/decisions]] — dated log of confirmed decisions + standard-doc supersessions
- [[market-maker/open-questions]] — live blockers with owners (Edwin / tZERO / Sport Radar / us)
- [[market-maker/parameters]] — every tunable number: value, status, source
- **[[market-maker/requirements]] — the MM's normative go-live list** (what MUST
  be true), sourced and status-tracked; change it only through its dated addendum
- **[[market-maker/market-taker-requirements]] — the same for SNT-1**, the market
  taker. The build document for the taker phase
- **[[market-maker/test-plan]] — the live test matrix** (lifecycle · ops ·
  failure drills), with a status per case
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

- **tZERO owns:** the order book, matching (price-time), order lifecycle, trade
  records, and bust execution. Our MM is a participant; our supervision role is
  the operator's agent acting *through* tZERO.
- **[[trading/trading|Trading]] owns:** the user-facing order flow. The
  synthetic market order is specced here (it exists because of MM mechanics)
  but ships in the app.
- **[[earnings-report/earnings-report|Earnings Report]] owns:** the off-field
  EST/ACT mechanics that feed the valuation engine's off-field term.
- **[[ipo-module/ipo-module|IPO Module]] owns:** primary issuance. **Re-based
  03-08:** the issuance sits in a separate **broker-dealer MPID** that holds and
  sells 1,000,000 shares per team; the **taker algo** buys ≥600,000 of them per
  team with randomised sizing. The maker is absent from the primary entirely.
  Supersedes the 15-07 float-warehousing model (~50k clips, ~35–50% of float).
- **[[architecture/open-questions]]** tracks the MM rows in the global list.
