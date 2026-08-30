---
description: "The as-built index — the machine in one paragraph, the per-part page table, the module map and the load-bearing numbers"
---

# The Market Maker — As Built

> **Component:** [[market-maker/market-maker]]
> **Purpose:** The SOURCE OF TRUTH for the machine — for agents working on
> it and for humans reading it. Three jobs: (1) what is actually built —
> key equations as implemented, each part of the build on its own page;
> (2) what is still to build ([[market-maker/build/next|next]], sequenced
> by [[market-maker/plan]]); (3) the anchor for changes — a proposal to
> change the machine starts by reading the page it touches, and the work
> that changes the machine ends by updating that page.
> Updated 2026-08-14.
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
> ⚠ BUILD-LOG.md is STALE as of 14-08 — its newest entry is
> always-quoting step 3 and its status table is 06-08-era; nothing on
> the converger, the lock, the wash guard, the publishers or the boot
> rebase. Trust these vault pages + [[market-maker/build-deploy-log]]
> until a code session back-fills it.

Repos: `inplay-market-maker` (Python 3.12, `src/mm/` + `src/snt/`) —
**881 tests on the PRODUCTION lineage** (`feat/always-quoting-step4b`
@ `db45300`, ruff + `mypy --strict` clean). ⚠ `main` (@ `772e79c`)
runs BEHIND production: PRs #24–#27 (session clock · always-quoting
steps 1–3) and #30 (converger) are still OPEN under review while the
VM runs them — deliberate, George's call 08-13. Merged since:
#23 (state publishers + manual orders) · #28 (taker hardening) ·
#29 (wash guard — not in the raw step4b lineage; the merged
**`step4b-wash` @ `5b10d68`** closes that split and runs as the taker
since SNT-CFG-0019). · `inplay-sportradar-service`
(`src/app/workers/mm_publisher/`) — ⚠ PR #37 (carries the
universe-filter fix, but as a FULL testing→main promotion, 65
commits) still OPEN; main regresses the running hotfix until it or
the one-hunk `hotfix/…@d877b26` (no PR yet) merges.

---

## The machine in one paragraph

The market maker prices 170 team securities (32 NFL + 138 NCAA; plus
the ten `.TEST` twins = 180 books in production supervised mode) and
rests two-sided limit-order ladders around its own fair price on
tZERO's book. Everything is an **event**: inputs arrive as envelopes,
an acceptor validates, deduplicates and journals them, and every engine
downstream is a pure function of the accepted stream — so replaying the
journal reproduces every price, every order and every suspension
**byte-identically**. One process, one journal, one writer (enforced by
the single-engine lock). A 0.5-second runtime loop is the only code
that reads a clock; the tick stages, a converger task sends bounded
batches to the venue, and one fsync per tick makes the whole tick
durable before anything leaves the process.

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

**Beside the MM, in the same repo:** SNT-1, the market taker
(`src/snt/` — agent · schedule (T-F07) · pending · journal · runtime,
incl. the manual-order family and the boot rebase; built 08-08,
**deployed 08-11 and running since** on its own account `4963224393`,
all 180 books). Its design is
[[market-maker/systems/snt-1-noise-taker|the systems page]] and what it
must satisfy is [[market-maker/market-taker-requirements]]. Separate
process, separate account, separate journal — deliberately not inside
the MM engine (single-writer journal + the E33 account separation).

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
| The orchestrator (per-security cycles, quarantine, venue cap, missed-sweeps counter) | `mm/orchestration/engine.py` |
| Venue record, reconciler, backoff, sync, transport | `mm/venue/` |
| Poller (pull path + heartbeat + tiers) | `mm/poller/worker.py` |
| Bus consumer (durable, acks, poison) | `mm/poller/consumer.py` |
| Runtime (tick, sweep, boot) + composition | `mm/runtime/` |
| The single-engine lock | `mm/runtime/lock.py` |
| The session clock (SESSION_BOUNDARY producer) | `mm/runtime/` (beside the SweepScheduler) |
| The converger (staged targets → bounded sends) | `[converge]` in `mm/venue/sync.py` · `[converge-task]` in `mm/runtime/loop.py` |
| State publishers (`mm.state` projection + edge task) | `mm/venue/state.py` · `mm/runtime/state_publisher.py` |
| The 170 universe (ticker = security id; `.TEST` twins) | `mm/universe.py` |
| The 170 sr-id → ticker bindings (verified) | `mm/bindings.py` |
| Every configurable number + status | `mm/config/dictionary.py` |
| SNT-1 (agent · schedule · pending · reconcile · pnl · journal · state/runtime incl. manual orders) | `src/snt/` |
| Service-side publisher | `inplay-sportradar-service/src/app/workers/mm_publisher/` |

## Key numbers

Every number lives in [[market-maker/parameters]] with a status
(✅ confirmed · 🟡 proposed · 🔴 TBD) and reaches code only through
`mm/config/dictionary.py` (§1.6-5). The load-bearing set: $5.00/win ·
$2.50/tie ✅ · floats 900k/1M ✅ · S=$1.00, M=$0.25 ✅ (N20 caveat) ·
live bands 5/10/20 s ✅-values/🟡-basis (E38) · γ=0.02, k=1.2, h=20 s,
H=30 s, σ²∈[0.05,400] 🟡 (E31) · ✂ E51 20-08: min width 25 ticks,
floors 50/100, base 550 × 0.72^i, clamp [100, 15,000], lean ÷ 48,000
🟡 · rungs 1–3 ✂ 26-08 · tick 0.5 s, sweep 0.5 s, missed past 1.0 s
(✂ 08-11/08-13) · dwell = republish clock: LIVE 0–0 · pre 5–20 s ·
post 5–20 s · overnight 20–40 s ✅ 08-11b · tiers 500 ms (✂ 08-11)/
15 s/30 min/10 min (LIVE ✅ · PRE 🟡 · slow tiers George's) · drain
caps 256 readings / 512 venue per tick 🟡 · converger 128 instr/pass
(✂ from 256, 08-14) at 0.25 s 🟡 · beat 0.25 s, stall threshold 5 s 🟡 ·
dead-man 10 s (✂ env 08-14; binary default rides gateway PR #4, N15).
