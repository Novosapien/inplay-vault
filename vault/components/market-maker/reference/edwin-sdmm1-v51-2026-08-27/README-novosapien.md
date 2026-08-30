---
description: "Provenance and verified findings for Edwin's SDMM-1 v5.1 handoff — what it is, what we measured, and the rulings it triggered"
---

# SDMM-1 v5.1 — Edwin's handoff, 27 August 2026

> **Source:** `novo_handoff_1.zip`, sent 27-08 after the pricing call
> ([[27-08-2026-mm-pricing-catchup]]). This is the formula he promised
> live on that call.
> **Filed unchanged.** `README.txt` is his. This file is ours.
> **Analysis:** [[market-maker/sessions/2026-08-28-sdmm1-v51-injury-dropped]]
> · [[market-maker/decisions]] 28-08 · `E52` `E53`

## What is here

| File | What |
|---|---|
| `novo_engine.py` | The engine, 476 lines, standard library only |
| `test_engine.py` | 31 acceptance tests. His rule: a port is correct when all 31 pass |
| `reference-spec.html` | The specification |
| `README.txt` | His run instructions |

    python3 novo_engine.py    # prints the LSU calibration, $59.5350
    python3 test_engine.py    # 31 tests, ~30s

## Verified by us, 28-08

- **All 31 tests pass.** The engine reproduces LSU's published IPO of
  **$59.535 to the penny**.
- **A loss is −$12.54**, of which only −$4.53 is the game played; −$7.14
  is the other 11 games re-rating 7.64 → 6.22 expected wins.
- **A win probability converts to a spread exactly** —
  `d = √(ς² + Var d)·Φ⁻¹(p)` matched the engine's own edge on all 12 LSU
  games, and gave an identical price.
- **It does not scale as written.** One rebuild: 0.5 ms at his 13-team
  demo, 364 ms at our 138 books, **652 ms at 170** — against a 500 ms live
  poll. Fix: checkpoint the settled observations, replay only live games —
  **5.5 ms measured**.
- **Our prices run a median +2.39% above the listed IPO**; his discounting
  (−1.14%) plus risk charge (−0.87%) is −2.01%, almost exactly the gap.

## Rulings it triggered

- ✅ **The injury channel is dropped** (George, 28-08). Measured, it is one
  scenario: a season-ending QB is −$8.31, everything else under $2.
- 🟡 **Our weekly futures rebase is withdrawn** — superseded by his rating
  engine.
- 🔴 **`E53` — port his engine or keep ours** is George's open call.

## Caveats on our reading

- We ran the code. **We did not audit the mathematics.** The martingale
  claim is tested to under a penny, which is strong evidence, not a proof
  we checked.
- He marks most constants **(est)** and says final estimation "awaits the
  freeze file and game history".
