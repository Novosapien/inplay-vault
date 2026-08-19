---
description: "CB2's session: the pulse de-phase was measured before it was wired, and AC2's gate proved unreachable by any offset — so the mechanism ships unused"
---

# 2026-08-14 — CB2: the pulse de-phase, and why AC2 cannot be met by moving it

> **Who:** AI session (stream-b-cb2, restarted as -r2 after an API timeout)
> **Type:** build + measurement
> **Refs:** spec `2026-08-14-mm-python-fix-set` F1b / R2 / AC2 / Q2 ·
> `profile-cb1.md` · branch `fix-set/cb2-pulse-dephase` ·
> [[market-maker/build/runtime]] · [[market-maker/build/quoting]]

## What we did

Chunk CB2 asked for a deterministic per-book phase offset across the 500 ms
LIVE pulse, so that game-load republish waves stop landing on one edge. The
gate was AC2: the p90 of acknowledgements arriving per 500 ms of wall clock
must fall to half its baseline.

We built the deterministic half and then measured the premise before wiring
it in. The measurement says the mechanism cannot move the gate. We stopped
rather than ship a change that reads as progress and is not.

- Built `src/mm/quotes/phase.py` — a security id hashes to one of
  `live_phase_offset_buckets` (8) slots across the pulse. Deterministic on
  the security id alone, integer-microsecond grid, **23 tests** (three of
  them pin the invariance result, so nobody re-derives it).
- Ran the six-game workload at 1× for 2,400 s and decomposed the
  acknowledgement stream by book, by burst and by window width.
- Ran an ON/OFF A/B in a throwaway measurement worktree (`cb2/measure-rig`,
  never merged) — the ON arm releases LIVE books at their own phase slot from
  a converger at one bucket width (62.5 ms), which is the strongest
  de-phasing the machine can express.
- Shipped as [inplay-market-maker #35](https://github.com/Novosapien/inplay-market-maker/pull/35),
  based on CA2's branch. 1,009 tests (986 base + 23), ruff and mypy clean.

## What we learned

**1 · The metric is invariant under the mechanism.** AC2 counts acks per
500 ms window and the pulse is 500 ms. A LIVE book emits one burst per
pulse, so it falls in exactly one window per pulse whatever its offset is. A
phase offset moves *which* window, never *how many*. To see de-phasing at all
the measurement window must be shorter than the pulse.

This is the same class of defect the 14-08 review already caught once. The
original AC2 counted acks per *tick*, which is arrival rate × pass duration
and so moved with the loop's own slowness. The replacement removed that
confound and introduced a different one.

**2 · The books are already de-phased, and by design.** `_timer_due`
(`quotes/engine.py:161`) measures 500 ms from each book's OWN last publish,
not from a shared grid, so live books free-run on independent phases. Over
the last 200 s of the arm: 150 burst-clusters held 2 books, 11 held 1, 2 held
4, **none held all 6**. The only books that coincide are the two sides of one
game, and they coincide because they share a reading — not a pulse edge.
F1b's premise, that the waves land on one edge, is not what this engine does.
An absolute 8-bucket grid would *concentrate* a distribution that is
currently continuous.

**3 · The gate's own percentile is not game load.** Of 78,352 acks in the
904 s arm, LIVE books produced **25%**; the other 158 books produced 73% on
their 5–40 s dwell draws. The mean window holds 49.8 acks across only 4.2
distinct books. The p90 window — the one AC2 gates on — contained **no
live-book acknowledgements at all**.

**4 · The quiet books are already maximally spread.** Their 5,114 redraws
arrive as Poisson noise: 2.83 bursts per window measured, p90 = 5, and
Poisson(2.83) predicts p90 = 5 exactly. Independent arrivals are as flat as a
jittered schedule gets.

**5 · The closing arithmetic — the gate sits below the mean.** Redistribution
never changes a total, so a perfectly flat arm has p90 = mean. A gate set
below the mean is therefore unreachable by any scheduler, and that is what
AC2 asks for. Measured on the full 2,400 s six-game arm (224,034 acks,
4,829 windows), on every segment of it:

| Segment | hot books | LIVE share | mean/window | p90 | gate (50%) | verdict |
|---|---|---|---|---|---|---|
| whole arm | 12 | 33% | **46.4** | 90 | **45.0** | **impossible** |
| late (1,500–2,400 s) | 12 | 37% | **48.6** | 94 | **47.0** | **impossible** |
| peak (1,800–2,100 s) | 8 | 38% | **49.7** | 98 | **49.0** | **impossible** |

The LIVE share rises from 25% to 33–38% at full load, exactly as expected —
and the gate gets *harder*, not easier, because the mean rises with it.

⚠ The six-game workload never sustains twelve simultaneously-hot books: each
game's books go hot for 300–600 s and then quiet (a re-rolled ladder whose
diff comes out empty sends nothing). Peak concurrency is **8**. So the
"all-live tail" is a segment that does not exist in this workload as built,
and the peak segment above is the honest substitute.

On the saturated clone the gate is arithmetically reachable (mean 46.9,
gate 107) — but the clone's p90/mean ratio is 4.6 against this arm's 1.94,
and that excess is loop saturation (1.375 s per pass, the converger getting
~1.23 passes per tick), which a phase offset cannot unpick.

**The only lever that moves this metric is sending fewer acknowledgements,
not sending them at different times.** That is CB3 (skip unchanged books) and
CB4 (per-ack cost) — which is also what `profile-cb1.md` concluded when it
measured the sweep side at 1.8% of the tick and the drain at 98%.

**6 · THE A/B — the mechanism works and the gate cannot see it.** Two
2,400 s arms, same seed, same workload, one binary. The ON arm releases each
LIVE book at its own phase slot from a converger running at one bucket width
(62.5 ms) — the strongest de-phasing this machine can express.

*The mechanism engaged, and it is measurable:*

| Release clusters (LIVE books) | OFF | ON | change |
|---|---|---|---|
| clusters | 2,768 | 3,516 | **+27%** more, smaller releases |
| acks per cluster | 26.9 | 20.8 | **−23%** |
| books per cluster | 2.36 | 1.84 | **−22%** |
| single-book clusters | 385 | **1,648** | **4.3×** |
| 4-book clusters | 542 | 353 | −35% |

It did exactly what it was designed to do: split the coincident same-game
pairs, so a release is now usually one book instead of two.

*The AC2 gate metric did not move at all:*

| | OFF | ON |
|---|---|---|
| acks | 224,034 | 223,620 |
| mean / window | 46.39 | 46.30 |
| p50 | 44 | 44 |
| **p90 (the gate)** | **90** | **90** |
| p99 | 144 | 142 |

**p90 90 → 90. Zero.** Burst size fell 23% and the gate registered nothing,
because the window and the pulse are the same length. That is the invariance
argument confirmed by measurement rather than by reasoning, with a positive
control proving the code ran.

**7 · The 73% finding — the biggest ack-volume lever is not an engineering
chunk.** Two thirds of every acknowledgement the engine handles comes from
the **158 quiet books** redrawing on their own 5–20 / 5–20 / 20–40 s dwell
draws (measured on the full arm: 149,598 of 224,034 acks = **66.8%**, in
12,820 redraws of mean 11.7 acks, 2.65 per window). There are 158 of them
against at most 12 live ones, so the non-live republish cadence — one
dictionary row — is the largest volume lever in the machine. It is
**book-visible**, so it is Edwin's remit under the 22-07 line (George's
08-11b numbers, riding the E31/E17 flag round), not ours to move.

**The lever board, all measured on the same arm** (`scripts/cb2_dwell_lever.py`):

| Lever | mean arrival | p90 | AC2 needs −50% p90 |
|---|---|---|---|
| **de-phasing (CB2, measured A/B)** | −0.2% | **0%** (90 → 90) | ✗ |
| non-live dwell ×2 | −33.3% | −26.7% (90 → 66) | ✗ |
| non-live dwell ×4 | −50.0% | −40.0% (90 → 54) | ✗ |
| quiet books alone (LIVE silenced entirely) | — | 64 | the floor |

⚠✎ **15-08: these are `six-game-v1` numbers and the SHARE inverts on v2.** The feeder skew (review-002 HIGH) suppressed ~45% of the ack load, and it suppressed the GAME books' pulse redraws specifically — the quiet books never had game readings, so none of their volume was missing. Restoring it lands entirely on the live side: projected v2 is ~63% LIVE / ~37% quiet, against v1's measured 33/67. The quiet books' ABSOLUTE volume (149,598) is unchanged and the dwell row is still a real lever, but it is no longer the biggest one, and the dwell ×2/×4 p90 projections were derived on v1's distribution and need re-deriving. Arithmetic from the review's ~45%, not a measurement — the GATE's v2 arm settles it.

⚠ The dwell rows are an **upper bound on the saving**: a book that waits
twice as long has let its price move further, so its real reconciler diff
would be larger than the burst measured here. Even so, quadrupling the quiet
dwell — a large book-visible change — reaches only 40% off p90.

**8 · AC4's miss ratio is a MACHINE-SPEED result, not an engine result.**
Same code, same six-game workload, same 1× arm, no wire and no fills on
either side:

| Machine | miss ratio (AC4) | DRAIN_CAPPED | pass duration |
|---|---|---|---|
| clone, n2-standard-2 (production's shape) | **52.3%** | 4 | 1.375 s |
| this Mac (M-series), OFF arm | **0.12%** — 5 of 4,333 due-sweep ticks | 7 | 0.50 s |
| this Mac (M-series), ON arm | **0.11%** — 5 of 4,441 | 7 | 0.50 s |

AC4's target is < 0.5%, and the engine **already meets it** on hardware fast
enough — by a factor of four, at double production's game count. The 52.3% is
not a defect in the sweep, the converger or the pulse; it is the per-ack cost
against two Cascade Lake vCPUs. ⚠ AC4's second clause (zero DRAIN_CAPPED)
fails on both arms, and on this one the 7 capped ticks are the boot re-stand
hitting the 512 cap, not game load.

This is the strongest single datum for the CB4-before-CB3 re-order, and for
the Go argument generally.

## What went wrong / got stuck

- The first CB2 session died on an API timeout before committing anything.
  Its worktree was clean, so nothing was lost.
- `profile-cb1.md` §7 projected that de-phasing would cut the p90 to ~73 by
  re-quoting only 34% of books per pass. That model divided a 2.75-**pulse**
  pass by 8 **buckets** — different units. The doc flagged it 🟡 and said to
  re-derive if CB2's design differed. Re-derived here; it does not hold.
- A worktree sharing the main checkout's `.venv` imports `mm` from ANOTHER
  source tree, so tests and measurement arms silently exercise the wrong
  code. Every command in this session ran with `PYTHONPATH=src`. This is the
  same trap the 14-08 taker lesson records for the VM, and CB4's rig was hit
  by it for real (its arms imported `~/mm/src` whatever tree they launched
  from, because a copied venv's `.pth` beat a `sys.path.insert` of the repo
  ROOT — which does not resolve in a `src/` layout at all).
- **Both CB2 arms were checked against that failure rather than assumed
  clean** (lead-directed). `mm`, `mm.venue.sync` and `mm.quotes.phase` all
  resolve into the measurement worktree under the arms' own invocation. The
  negative control proves `PYTHONPATH=src` was load-bearing: without it,
  `mm` resolves to a DIFFERENT worktree that carries `phase.py` but not the
  patched `sync.py`, so the ON arm would silently have run without
  de-phasing. Independent proof from the recorded artefacts: the ON arm's
  `MM_CB2_CONVERGE_S=0.0625` override exists only in the measurement tree's
  `compose.py`, and `profile.json` shows **24,144 converger passes against
  the OFF arm's 7,642** (3.16×, mean 1.027 → 0.336 ms per pass) — so that
  arm provably ran the measurement code. Instructions sent were **136,872
  vs 136,935, 0.05% apart**: both arms did the same work and only the
  schedule differed, which is the ideal control for this experiment.

## Decisions made *(mirror into [[market-maker/decisions]])*

- ✅ **CB2 ships evidence, not a wired mechanism** — team lead, 14-08. The
  offset is not connected to the sweep or the converger. `quotes/phase.py`
  stays as the primitive for the day the pulse or the converger cadence
  changes. The lead's words: a mechanism proven inert must not ship looking
  like progress.
- ✅ **CB2's deliverable is the module + tests + the measurement tooling +
  this analysis.** PR #35, based on CA2's branch.
- 🔴 **AC2's ≤ 50% gate goes to George for withdrawal**, with the lead's
  backing. It is invariant to the mechanism it gates and, on an unsaturated
  engine, set below the mean arrival rate. It re-opens Q2's "works out"
  proof, so it is his call.
- ⚠ **Superseded on the way:** the lead first ruled Option A (release-side
  de-phasing at the converger, with a dictionary exception for
  `converge_interval_s` 0.25 → 0.0625). The (a)/(b) evidence — invariance,
  and the books already free-running — landed after that ruling and replaced
  it. Recorded because the reasoning is worth keeping: Option A would have
  been correct if the books had been phase-aligned.

## Questions opened / closed *(mirror into [[market-maker/open-questions]])*

- **Opened (N42):** does R2 survive at all, or does it fold into CB3/CB4 as
  "cut ack volume"? Needs George — AC2 was his "works out" proof for Q2.
- **Opened:** the non-live dwell cadence is the machine's biggest
  ack-volume lever and it is book-visible — Edwin's remit, one dictionary
  row, quantified here as reporting only.
- **Closed:** whether a within-pulse offset can move a per-500 ms-window
  count. It cannot; the window and the pulse are the same length.

## Next

- The lead takes ONE package to George: the AC2 withdrawal, the CB3/CB4
  re-order, and the lever board beside it — de-phasing (inert), the non-live
  dwell row (73% of volume, his and Edwin's call), and machine speed (AC4 is
  0.12% on a fast box against 52.3% on production's shape).
