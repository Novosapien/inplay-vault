---
description: "The Go maker's ladder shape: rank drift found and fixed on the fourth attempt, the alien drain and MMGO prefix ported, and three live failures in between"
---

# 2026-08-21 — The Go maker's ladder shape, and three ways I broke it

> **Who:** George + AI session (the Go side), overnight 20→21 Aug.
> **Type:** build + live operations on `mm-2`. Six commits, four live runs.
> **Refs:** Go PR #17 `feat/phase-3-ingestion` — `46c9538` `506216f` `8cebdde` `667b181`
> (and `2a55d74`, `fa3dfc2`, both superseded) ·
> [[market-maker/sessions/2026-08-20-e-e51-deploy-and-alien-drain]] (the Python side of the same night) ·
> N10 · N62 · N63 · N64.
> **⚠ Ended with `mm-2` stopped and its orders cleared. Nothing of ours rests at the venue.**

## What we did

Chased one complaint from George — *"the shape is still fucked"* — to its cause,
through three failed fixes and one that worked. Also ported the Python maker's
alien drain and took our ClOrdIDs out of its healer's reach.

## What we learned

### ⭐ The defect is RANK DRIFT, and George described the mechanism before we measured it

His words: *"n plus one is being added and then when it reaches n plus two it
keeps n+1 and gets rid of n."* Traced on `IPTCJAGU.TEST`, eight samples five
seconds apart:

```
samples 1–7   63.85/11002 63.83/11939 63.81/8428 63.79/4747 63.77/3443 63.75/2564
              (2-cent grid, unchanged for 35 s)
sample 8      63.83/11939 63.79/4747 63.75/2564 63.71/4069 63.67/2620
              +2 added  −3 removed  3 KEPT AT THE SAME PRICE  0 mutated
```

The ladder re-spaced from a 2-cent to a 4-cent grid. Three orders sat on prices
the NEW ladder also wanted, so §8.1 pass 1 (rest-until-gone, N10) kept them
untouched — each still carrying the size drawn for the rank it was BORN at.
`63.75` was rank 6 (2,564); in the new ladder it is rank 3, where the draw is
~5,500, and the level below it posted fresh at 4,069. Hence bigger-as-you-go-out.

⭐ **The arithmetic that proves version mixing.** Sizes are `10,000 × 0.72^i`
varied by `VF ∈ [0.75, 1.25]`, so within ONE quote version a step can only fall
in `[0.432, 1.20]`. Live steps reached **2.16**. Nothing one version drew can do
that.

### ⭐ The trigger must be the RANK BASIS, never the drawn size

`quantity.go` already said so — *"materiality is judged BEFORE variation. Final
sizes are freshly drawn each version, so comparing them would republish every
cycle"* — and the second attempt ignored it and did exactly that.
`Level.PreVariation` now carries the rank's basis, and a resting size is honest
for the rank it sits at when it falls in `[0.75 × pre, 1.25 × pre]`.

### ⚠ The remaining inversions are the SPEC's, not a bug

With rank drift fixed, ~30% of ladders still show a small inversion. §5.7.3 draws
the ±25% variation **independently per level** against a 0.72 decay step, so
adjacent rungs flip whenever the jitter ratio exceeds 1.389 — about 6% per pair.
A sweep of 8 securities × 40 versions × 2 sides × 3–6 levels finds **541 inverted
steps**. Python at the pin does the same; it never shows because `mm-1` quotes
one rung a side. **N65.**

### ⭐ tZERO was blameless throughout

The one time it was worth asking: every message was answered correctly and
immediately — 389 new → 389 acks, 157 replaces → 157, 550 cancels → 550, zero
rejects, zero cancel-rejects. Every failure that night was ours.

## What went wrong

### 1 · ⚠⚠ Attempt one took the books dark

Cancel the level, post it next pass. Sizes are re-drawn every version, so every
order mismatched every version and every book spent a whole pass empty: **72 to
97 of 180 books quoting**, 11 of 164 quoting in all ten samples. George saw it on
the panel before the measurement finished.

### 2 · ⚠⚠ Attempt two reintroduced the 08-08 doubled level

The held-level lookup was keyed on `Price.String()`. `"63.80"` and `"63.8"` are
numerically equal and render differently, so an order failed to match its own
level and a SECOND order went out at a price the first held. **4 doubled levels
across 60 ladders.**

### 3 · ⚠⚠ Attempt three flooded the venue

Triggering on the drawn size republished every level every version: **246 orders
across 10 books**, 109 prices posted as NEW more than once, 389 news and 550
cancels in three minutes.

### 4 · ⚠ Every unit test passed through all three

⭐ **The lesson: every test asserted on ONE reconcile call.** Both live failures
are properties of MANY calls. The fix ships with a closed-loop churn simulation
that drives the reconciler against a venue that applies what it is told —
a stable ladder must go silent, a re-space must settle in one version, a walking
ladder must never inflate. Restoring the old trigger fails it with *"got 5
instructions — this is the 20-08 flood"*.

### 5 · ⚠ I reported success from two cherry-picked books

Sampled `IPTCBILL` and `IPTCCHIE`, saw clean ladders, and said it was working
while the Texans, Commanders and Jaguars were visibly broken on George's screen.
The aggregate statistic was fine; the books he was looking at were not.

## Decisions made *(mirror into [[market-maker/decisions]])*

- ✅ **The resize is the BEHAVIOUR, not an environment variable** (George). A
  defect fix does not sit behind a switch. `MM_REQUOTE_CLEAR_FIRST` was removed;
  the parity harnesses pin the reference lifecycle themselves and say why.
- ✅ **Our ClOrdID prefix is `MMGO` + 14 hex.** It keeps the `MM` the gateway's
  namespace check demands, and fails the Python healer's `MM` + 16-hex test on
  the `G` — so we read as FOREIGN and its boot healer leaves our book alone.
  ⚠ A wholly non-MM prefix is impossible: `namespaceReason` refuses it with
  `MM_PREFIX_REQUIRED`.

## Questions opened *(mirror into [[market-maker/open-questions]])*

- **N65** — §5.7.3's per-level variation breaks ladder monotonicity in ~30% of
  ladders. A monotonic ordering of the same seeded draws fixes it and is written
  but NOT committed; it fails three Phase-2 gate tests and needs the same
  explicit pinning. ⚠ Moot if the Go maker adopts Edwin's `levels 1/1`.
- **N66** — the gateway's dead-man is one latch for the whole MM namespace, so
  either engine's silence sweeps every MM order including the resting IPO
  offering. Go PR #28 (`feat/deadman-per-bot`) addresses it.

## Next

1. ⚠⚠ **Do not start `mm-2` until PR #28 is merged AND running on the MM
   gateway.** The IPO offering rests in the same namespace on 137 real books; a
   10-second heartbeat gap sweeps it. Ticker scoping does not protect against
   this — the sandbox lock stops us placing bad orders, not our silence
   cancelling someone else's.
2. Port Edwin's 20-08 parameters to Go (`levels 1/1`, `base_size 550`,
   `min_quantity 100`, `min_width_ticks 25`). Go still runs the pin's
   `3–6 / 10,000 / 1,000`, and at one rung a side N65 disappears.
3. Then decide N65 on the evidence.
