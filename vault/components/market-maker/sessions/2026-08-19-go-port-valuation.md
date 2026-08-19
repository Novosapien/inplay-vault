---
description: "Porting the valuation engine to Go: the corpora drive two of its five entry points, and §3.2.1's tolerance band fights the pair-identity guard"
---

# 2026-08-19 — the Go port, the valuation engine

> **Who:** Claude (`/general-implementation-builder`) + George
> **Type:** build
> **Refs:** `specs/2026-08-18-mm-go-port/` · Go repo PR #12 ·
> [[market-maker/build/valuation]] ·
> [[market-maker/sessions/2026-08-18-go-port-phase-1]]

## What we did

Ported `valuation/` — the Reference Price, Edwin's on-field leg, the
freshness/status/confidence system with its E38 deviation, the §3.4.1 ratchet,
and the F2 anchor seed's three seats (the mint, the reader, the event).

Both committed corpora now fold **byte-identically** on the `valuation`,
`last_rp` and `mev_inputs` subtrees — the a2 pair and all 170 books.

Then built the chunk's own gate, because the corpora barely touch this engine.

## What we learned

### ⭐⭐ §3.2.1's tolerance band and the pair-identity guard contradict each other

§3.2.1 **accepts** any win/tie/loss triple whose sum is within a millionth of 1,
and uses the numbers **untouched** — that is the whole point of the band.
`_on_probability` then asserts the pair identity, `GEV(home) + GEV(away) =
$5.00` **exactly**. And `$5.00 × 1.0000005` is not `$5.00`.

So a reading the gate deliberately tolerated **raises out of `process()`**, and
nothing catches it — `cycle()` has no `except`.

Measured at the pin:

| | rate |
|---|---|
| accept-band triples whose sum is not EXACTLY 1 | **100%** raise |
| §3.2.1 **repaired** triples (the repair's own precision-28 residue) | **2.7%** raise |

⚠ **It is latent, not live** — and only by luck. Sportradar's two percentages
sum to exactly 100 on **all 1,089 readings** of the captured Chiefs–Ravens game.
That is a property of the **provider**, not of our code, and nothing checks it.
`adapters/sportradar.py:93-94` reads SR's two numbers rather than deriving one
from the other, so a provider that rounds differently one day starts raising.

Not fixed — Phases 0–4 are a faithful port and any change breaks the zero-diff
mandate. Reproduced exactly, pinned by test, and **owed to the maker team**.

### ⭐ Python's own `[exact-sum]` note is wrong where a repair is involved

The note reasons that the fold's order "cannot change the answer" because
Decimal addition at these magnitudes is exact. That holds while the terms are
**short**. A §3.2.1 repair produces a **28-significant-digit** probability, and
two such terms round as soon as the running total reaches 1.

A real window, read out of the pinned engine: the sorted order gives
`68.50635988904318442204161368`, and **four of the six orderings give …367**.

The sorted walk is **load-bearing**, not §1.6-4 hygiene.

### ⚠ The corpora drive two of the engine's five entry points

| | a2 | six-game |
|---|---|---|
| `probability_update` | 1,089 | 82 |
| **`official_result`** | **0** | **0** |
| **`anchor_seed`** | **0** | **0** |
| `ingest_reference_numbers` | a METHOD, not an event (N23) — no journal can drive it | |

So a byte-identical subtree says nothing about settlement (§3.1.3), the
`[settled]` guard, `[correction]`, `[unseen]`'s `p_ref=None`, or the whole
anchor seed — the paths a fresh-journal boot during a live game depends on, and
the one that cost **$0.685 a share** on 14-08.

The chunk therefore ships a 4-seed × 700-step Go↔Python differential fuzz, and
`diffreplay` now prints what the valuation leg did **not** drive, per run.

## What went wrong / got stuck

- **The fuzz stamped `provider_event_time` and `receive_time` identically**, so
  `[no-clock]` was untested — a plant that read receive time unconditionally
  passed. The two stamps now differ, and one reading in six carries no provider
  time at all.
- **Two cases the random draw could not reach**, both found by planting the
  defect and watching the gate pass:
  - the `[sort]` trap — every pair of timestamps the fuzz minted was minutes or
    days apart, where text and parsed comparison agree. Now a scripted probe
    ingests a T whose effective time is the same second as a kickoff, spelled
    with `.500Z`.
  - an order-sensitive window — it needs several **repaired** games in one
    security's window at once. Now a scripted burst.
- **One plant the fuzz catches on a coin flip**: an unsorted map walk. Go
  randomises map order per run, so it is pinned by a unit test on a real
  order-sensitive window instead of left as an unexplained miss.

## Decisions made *(mirror into [[market-maker/decisions]])*

1. **The accept-band / pair-guard contradiction is reproduced, not fixed** — and
   escalated as the third live Python defect this port has found.
2. **The sorted walk over a security's games is load-bearing**, and the
   `[exact-sum]` note is corrected in the as-built page.
3. **Package filing may differ from Python's where Go's import graph forces it.**
   Python imports by module; Go by package. The §3.2 gate moved down to the
   event door and `PythonISOFormat` to the codec. No rule changed.

## Questions opened / closed *(mirror into [[market-maker/open-questions]])*

- **Opened (N47):** should the §3.2.1 accept band tolerate a sum the pair guard
  refuses? Three readings are available — tighten the band to exact-1, relax the
  guard to the band's tolerance, or normalise inside the accept band too. It is
  Edwin's number and George's call, and it must be settled before a second
  provider or a schema change makes it live.

## Next

- **Phase 2's `position` chunk** — NP, PR, EP/EPR, IA, RM, and `sellable.py`'s
  `capacity = holding − livS`. ⚠ Name which of the FIVE order/position state-set
  questions is being answered before writing a line of it: `livS` is not §4.4's
  exposure set and is not the marketable guard's.
