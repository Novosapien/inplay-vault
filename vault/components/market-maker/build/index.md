# The Market Maker — As Built

> **Component:** [[market-maker/market-maker]]
> **Purpose:** The SOURCE OF TRUTH for the machine — for agents working on
> it and for humans reading it. Three jobs: (1) what is actually built —
> key equations as implemented, each part of the build on its own page;
> (2) what is still to build ([[market-maker/build/next|next]], sequenced
> by [[market-maker/plan]]); (3) the anchor for changes — a proposal to
> change the machine starts by reading the page it touches, and the work
> that changes the machine ends by updating that page.
> Updated 2026-08-06.
>
> **Authority chain:** [[market-maker/decisions]] (dated rulings) outranks
> the **v1.3 Build Spec** (`standards/MM-build-spec-v1.3.html`), which
> outranks the CTS/PTS standards (historical context). These pages
> describe the RESULT — where the build deviates from the spec, the
> deviation is named here and sourced there. The `systems/` docs are the
> per-system DESIGN narratives, written before and during the build —
> where one disagrees with these pages, **these pages win** (they
> describe what exists).
>
> **Maintenance rule:** a session that changes the machine updates the
> touched page (part of the session loop in
> [[market-maker/working-guide]], and instructed in the repo's
> `CLAUDE.md`). Repo-side detail lives in
> `inplay-market-maker/docs/BUILD-LOG.md` (traceability matrix, session
> log); these pages are the shape and the mathematics.

Repos: `inplay-market-maker` (Python 3.12, `src/mm/`), 534 tests, ruff +
`mypy --strict` clean · `inplay-sportradar-service`
(`app/workers/mm_publisher/`), 577 tests.

---

## The machine in one paragraph

The market maker prices 170 team securities (32 NFL + 138 NCAA) and rests
two-sided limit-order ladders around its own fair price on tZERO's book.
Everything is an **event**: inputs arrive as envelopes, an acceptor
validates, deduplicates and journals them, and every engine downstream is a
pure function of the accepted stream — so replaying the journal reproduces
every price, every order and every suspension **byte-identically**. One
process, one journal, one writer. A 1-second runtime loop is the only code
that reads a clock.

## The pages

| Page | What it covers | Code |
|---|---|---|
| [[market-maker/build/event-core\|Event core]] | Envelope, acceptor, idempotency keys, the journal, determinism + replay | `mm/events/` |
| [[market-maker/build/ingestion\|Ingestion]] | The four data paths in — the bus (publisher + consumer), file replay, Edwin's file, venue events; finals; discovery; poll tiers | `mm/adapters/` · `mm/poller/` · service `mm_publisher/` |
| [[market-maker/build/valuation\|Valuation]] | RP, Edwin's on-field leg, GEV, freshness/status/confidence, the E38 observation-age deviation | `mm/valuation/` |
| [[market-maker/build/position\|Position]] | Net position, position ratio, the inventory skew, the reservation midpoint | `mm/position/` |
| [[market-maker/build/quoting\|Quoting]] | σ², width, the ladder, quantities, the publish gate, the check battery | `mm/quotes/` |
| [[market-maker/build/market-state\|Market state]] | The four states, the promotion ratchet, the kill switch | `mm/market_state/` |
| [[market-maker/build/venue\|Venue]] | The order record, the reconciler, sync, the NATS transport, gateway facts | `mm/venue/` |
| [[market-maker/build/runtime\|Runtime]] | The tick, the sweep, the drains, acks, boot, the composition | `mm/runtime/` |
| [[market-maker/build/infrastructure\|Infrastructure]] | Where it runs: the VPC, the VMs, storage, the local bench, deployment status | — |
| [[market-maker/build/next\|Next]] | Real vs mocked vs gated, and what we build next | — |

## Where things live — the module map

| Piece | Code |
|---|---|
| Envelope · acceptor · journal · keys | `mm/events/` |
| SR adapters (file + wire, finals) | `mm/adapters/sportradar.py` |
| Edwin's file reader | `mm/adapters/reference_feed.py` |
| Gateway event adapter | `mm/adapters/gateway.py` |
| Valuation (RP, on-field, freshness) | `mm/valuation/` |
| Position (NP, PR, IA, RM) | `mm/position/` |
| Quoting (σ², width, ladder, sizes, publish) | `mm/quotes/` |
| Market state + kill switch | `mm/market_state/engine.py` |
| Venue record, reconciler, sync, transport | `mm/venue/` |
| Poller (pull path + heartbeat + tiers) | `mm/poller/worker.py` |
| Bus consumer (durable, acks, poison) | `mm/poller/consumer.py` |
| Runtime (tick, sweep, boot) + composition | `mm/runtime/` |
| The 170 universe (ticker = security id) | `mm/universe.py` |
| The 170 sr-id → ticker bindings (verified) | `mm/bindings.py` |
| Every configurable number + status | `mm/config/dictionary.py` |
| Service-side publisher | `inplay-sportradar-service/src/app/workers/mm_publisher/` |

## Key numbers

Every number lives in [[market-maker/parameters]] with a status
(✅ confirmed · 🟡 proposed · 🔴 TBD) and reaches code only through
`mm/config/dictionary.py` (§1.6-5). The load-bearing set: $5.00/win ·
$2.50/tie ✅ · floats 900k/1M ✅ · S=$1.00, M=$0.25 ✅ (N20 caveat) ·
live bands 5/10/20 s ✅-values/🟡-basis (E38) · γ=0.02, k=1.2, h=20 s,
H=30 s, σ²∈[0.05,400] 🟡 (E31) · base 10,000 × 0.72^i, clamp
[1,000, 15,000] 🟡 · tick 1 s, sweep 2.0 s ✅ · tiers 2 s/15 s/30 min/
10 min (LIVE ✅ · PRE 🟡 · slow tiers George's) · dead-man 4 s (Hasan's
placeholder, N15).
