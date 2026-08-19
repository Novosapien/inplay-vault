---
description: "Phase 3 of the Go port: four chunks land, gate 0-b runs for the first time, and the decimal library turns out unable to hold a number CPython stores"
---

# 2026-08-19 — the Go port, Phase 3, and the limit of the decimal library

> **Who:** Claude (`/general-implementation-builder`) + George
> **Type:** build
> **Refs:** `specs/2026-08-18-mm-go-port/` · Go repo PRs #16, #17 ·
> [[market-maker/go-port-findings|GP-12]] · `N52` ·
> [[market-maker/build/ingestion]] · [[market-maker/build/runtime]]

## What we did

First we closed Phase 2's per-phase review. Then we built four of Phase 3's
five chunks.

| chunk | what it covers |
|---|---|
| ingestion | the Sportradar adapter and the two-front-doors contract |
| poller | the pull path, the tier table, discovery, N16's final |
| marketable-guard | R-Q09's TOB cache and the refusal |
| orchestration | per-security cycles, the quarantine, the whole-machine fold |

**Gate 0-b now runs.** The fold drives the real Orchestrator, so all eighteen
subtrees come out of one `State()` call. Thirteen reproduce byte-identically on
both corpora.

## What we learned

### 🔴 The decimal library cannot hold a number CPython stores

The `apd` library caps the exponent at **±100000**. CPython reaches **±999999**.

On the a2 corpus Python stores this `variance_rate`:

    4.385597164977966123725114636E-916199

⚠ That field is a **checkpointed string**. The value reaches the saved state
directly. `apd` cannot hold it at all.

The corpus reaches the number because the a2 journal spans **60,871,126
seconds**, about two years. Its probability readings carry the captured 2024
game's timestamps. Its venue events and sweeps carry the 2026 replay's.

⭐ A live engine never sees such a gap. Real events arrive seconds apart. The
gap is a fault in how we built the corpus.

**This needs a ruling — `N52`.** Three options. The cheap one is to rebuild the
a2 corpus on one timeline.

### 🔴 apd returns zero where Python returns a real number

`Exp` works only while `|x|` is at most 22,977. Above that it returns **zero**.

    exp(-34657.359…)   python  3.163856671530324185927899991E-15052
                       apd     0E-1000031

This is a wrong answer, not a rounding difference, and it sits in the numeric
core. The real corpus drives it.

We fixed it. The calculation splits into `exp(x) = exp(r) × 10ⁿ`. The `10ⁿ` part
moves the exponent only, so it adds no rounding. 4,000 values from the pin now
match Python exactly. 2,495 of them are above the old limit.

⚠ This is the **third** `apd` defect, after the `Ln`/`Exp` rounding and
`to_integral_value`. The class was known. Nobody had swept the domain to its
edge.

### ⭐ A wrong ladder tie-break, found by Phase 2's review

CPython's `max` and `min` return their **first** argument on a tie.
`ladder.py` passes the price first, so a price equal to a bound keeps the
**price's** spelling. Go took the bound's.

    RM 4.995, MEV "5"   python  asks ["5.00"]
                        go      asks ["5"]

Prices reach the wire as strings, so that is a gate failure. It was latent only
because every MEV today carries exponent −2. `maximum_price` is a plain
parameter, and **Phase 3's orchestrator is what starts supplying it** — so it
would have gone live exactly when the port could no longer see it.

## What went wrong / got stuck

- **`ConditionInputs` needs its constructor.** Two fields belong to unbuilt
  chapters. Their healthy values are `true` and `Normal`, not Go's zero values.
  A struct literal made every book read as "not trading". **All 4,756 cycles
  suspended.** The symptom read as "the cycle never runs" rather than "one input
  is wrong".
- **The config version seeds every §5.7.3 draw**, and the fold hardcoded it.
  Every price that needs no draw stayed right. Every drawn price went wrong.
  ⚠ A nearly correct result is the worst shape a defect can take.
- ⭐⭐ **Nine fixtures could not see the defect they existed to catch.** Two
  floors were declared and never asserted, and the data violated both. An
  ordering case did not discriminate. A tick replay drove two games, where map
  order is invisible. A stub always reported the session open. **Every one was
  found by planting a defect. None by reading the code.**

## Decisions made *(mirrored into [[market-maker/decisions]])*

1. **A gate lists what it PROVES, never what currently passes.** Five subtrees
   stay outside the `built` list with the real fault named against each.
2. **The config version is a setting**, like the security universe. The fold now
   requires it.
3. **`internal/decimal` reduces the range for `exp`** rather than inheriting
   apd's limit.

## Questions opened / closed

- ⭐ **`N52` opened** — the decimal library's exponent limit. George rules.
- `N48` stands (the journal's retention).

## Next

1. **George rules on `N52`.** It decides whether gate 0-b can pass on a2.
2. Close the `quotes` divergence on the six-game corpus. The first prices
   reproduce exactly, then drift one tick.
3. Build `runtime`, Phase 3's last chunk. ⚠ The marketable guard's wiring lands
   there, and Phase 1's differential fuzz must re-run after it.
