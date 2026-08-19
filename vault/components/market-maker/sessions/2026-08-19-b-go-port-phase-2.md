---
description: "Closing Phase 2 of the Go port: the engines are ported, and the gate's own corpus turned out never to move the price"
---

# 2026-08-19 — the Go port, Phase 2 complete

> **Who:** Claude (`/general-implementation-builder`) + George
> **Type:** build
> **Refs:** `specs/2026-08-18-mm-go-port/` · Go repo PRs #12–#15 ·
> [[market-maker/build/valuation]] · [[market-maker/build/position]] ·
> [[market-maker/build/quoting]] · [[market-maker/build/market-state]] ·
> [[market-maker/go-port-findings]]

## What we did

Ported the four numeric engines and R13's decay cache — the whole of Phase 2:

| chunk | what it covers |
|---|---|
| valuation | RP, Edwin's on-field leg, freshness/status/confidence, the F2 anchor seed |
| position | NP/PR/EP/IA/RM, the venue's own holding (tag 9383), livS and the ask cap |
| quoting | σ², the ASMM-1 width, the ladder, the sizes, §5.10's battery, R-Q08's cap |
| market-state | the four states, §6.2's precedence, the ratchet |
| decay-cache | R13, and AC23a |

**Phase 2's gate holds** — four arms × 2,178 cycles, comparing the outcome type,
the book field for field with prices as strings, the sixteen checks byte for
byte, the ask cap, the reasons, **and** the checkpointed state.

**AC5 and AC23a are closed.** The §5.7.3 golden fixture reproduces exactly, and
the decay cache is proven output-neutral on every arm.

## What we learned

### ⚠⚠ The gate's own corpus never moves the price

On `pure.jsonl` — the capture the spec names for the Phase-2 gate — **every game
kicked off BEFORE T was published**, so none is in G and the Reference Price is
`77.500` on all 1,089 readings.

A gate over a constant price exercises σ² only at its cold start, never the
ladder's outward rounding, and never the position-side modifier. **Three planted
defects survived the first three arms untouched.**

The fix is a fourth arm that moves T's effective time before the 2024 kickoff, so
the games enter G and the real captured probabilities drive a real price — **685
distinct Reference Prices**, plus a 180,000-share opening position so EPR and IA
stop being zero.

⭐ The evidence was on the page from Phase 0: the corpus's own manifest says
`publishes_during_replay: 0` and its `last_rp` is a constant. Nobody had read
those two numbers as *"the gate's corpus cannot move a price"*.

### ⭐ The spec's five comparator clauses cannot see a checkpointed exponent

Every clause ends in whole ticks and whole shares. `variance_rate` is a
checkpointed **string**, and Δt's spelling reaches it. Two more plants proved it
by surviving the book comparison. The gate now compares
`sha256(canonical(quotes.state()))` on every cycle too.

### ⚠⚠ Δt goes through a float, and the exponent survives

Python computes `Decimal(str(timedelta.total_seconds()))`. `observed_rate`
divides by Δt, division carries the ideal exponent, so a Δt of `2` and one of
`2.0` give variance rates that are the same number spelled differently.

The rule — `micros ÷ 1,000,000` reduced, except that an integral value carries
one decimal place because `str(2.0)` is `"2.0"` — is verified against CPython
over **160,000** microsecond values from 1 µs to 27 hours, zero mismatches.

### ⚠ Two committed corpora, and almost none of these engines

| | a2 | six-game |
|---|---|---|
| `probability_update` | 1,089 | 82 |
| **`official_result`** | **0** | **0** |
| **`anchor_seed`** | **0** | **0** |
| **`EXECUTION`** | **0** | **0** |

So the byte-identical `position` subtree proved only that an all-zero opening
state renders the same on both sides. Each chunk therefore ships its own Go↔
Python differential fuzz driving the API, and the diff harness now PRINTS what a
run did not drive.

## What went wrong / got stuck

- **§5.10's two ordering checks were written with a direction multiplier**, and
  the multiplier was inverted. It read as correct. The gate caught it on cycle 0
  of all three arms on its first run — which is what the gate is for.
- **A plant was masked by a second guard** in the position chunk: the
  unknown-security fill carried FIX tag 9383, so the venue-holding fold's own
  universe check raised first. ⭐ The rule this adds: *a plant that raises is only
  evidence if the raise came from the code under test.*
- **Go's package graph closes a cycle Python's module graph does not** —
  `venue → quotes → position → venue`. Cut with `position.SellOrder`, a five-field
  view of a Venue State Record order, with the state strings pinned from an
  external test package.

## Decisions made *(mirrored into [[market-maker/decisions]])*

1. **The Phase-2 gate needs a price-moving arm**, and the spec's named corpus
   cannot supply one.
2. **The gate compares checkpointed state as well as the book**, because the
   spec's five clauses cannot see an exponent.
3. **Package filing may differ from Python's where Go's import graph forces it**
   — the second instance, after the §3.2 gate.

## Questions opened / closed

- None opened. **N47 stands** (the §3.2.1 accept band vs the pair guard), and is
  in [[market-maker/go-port-findings]] as GP-3.

## Next

- **Phase 2's per-phase review**, then **Phase 3 — orchestration, runtime,
  converger**: ingestion, poller, the marketable guard, orchestration, runtime.
- ⚠ Phase 3 is where gate 0-b finally becomes evaluable — the FULL canonical
  state, all eighteen subtrees, tolerance list empty. Seven compare today.
