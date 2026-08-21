---
description: "The Go port's Phase 0: the event core built and proven byte-identical to Python, plus three spec defects the build found and the checkpoint design a measurement decided"
---

# 2026-08-18 — the Go port, Phase 0

> **Who:** Claude (`/general-implementation-builder`) + George
> **Type:** build
> **Refs:** `specs/2026-08-18-mm-go-port/` (spec.md · progress.md) ·
> new repo **`Novosapien/inplay-market-maker-go`**, PRs #1–#6 ·
> `specs/2026-08-17-mm-pre-port-close/GO-PORT-HANDOVER.md` ·
> [[market-maker/build/event-core]]

## What we did

Built **all seven Phase-0 chunks** of the Go port and proved the event core
byte-identical to Python on both reference corpora.

| Chunk | PR | What it produced |
|---|---|---|
| `repo-scaffold` | #1 | The A3 layout, the pinned toolchain gates, CI |
| `reference-artefacts` | #2 | Every certification target, generated at the pin |
| `decimal-parity` | #3 | `internal/decimal` — the apd wrapper |
| `canonical-json` | #4 | `internal/codec` — the byte-equal encoder |
| `event-core` | #5 | `internal/events` — envelope, keys, journal, acceptor, checkpoints |
| `diff-harness` + `checkpoint-design` | #6 | `tools/diffreplay` and A2, measured |

**What holds:**

- The acceptor's fold is **byte-identical to Python's on BOTH corpora** —
  7,443 and 14,975 seen keys, each with its hash and its event time.
- **22,471 journal lines** re-emitted byte-identically (AC4), and **22,471
  payload hashes** recomputed and matched.
- **Checkpoint-resume ≡ never-stopped fold** at sequence 3,722 (R2c).
- 2,285/2,285 decimal vectors and 200,000/200,000 transcendental sweep rows
  (AC3); identical state hashes at GOMAXPROCS 1, 2 and 8 (AC11); 7.4M fuzz
  executions; the toolchain gate clean (AC15).

## What we learned

### ⭐ apd's `Ln` and `Exp` are NOT correctly rounded — the spike's headline was a sampling artefact

`spike-decimal/RESULTS.md` reported *"221/221 numeric parity … including every
transcendental"*. That rested on **one** `ln` vector and **28** `exp` vectors.
The 2,285-vector conformance suite's 229 `exp` vectors passed too.

A sweep of **100,000 draws from each function's real engine domain** found it
at once:

| | disagree with libmpdec in the last digit |
|---|---|
| `ln` | **1.480%** |
| `exp` | **0.056%** — about one in 1,800 |

Both are fatal: the width feeds the ladder, the ladder's prices are compared
**as strings**, and `variance_rate` reaches the checkpoint as one. At one in
1,800, `exp` would have surfaced in Phase 2 as an unreproducible *quote*
divergence rather than as a decimal bug.

Fixed with Ziv's strategy — evaluate at 28+5 guard digits, escalate to 80 when
the discarded tail sits within 2 ULP of the rounding boundary, and panic
rather than guess. **200,000/200,000 now match.** 1,536 boundary rows are
committed as a regression fixture.

⚠ **Consequence for R13:** the guard costs about **15% on `exp`** and 12% on
`ln`. The decay cache is more load-bearing than the spec models it, not less,
and the economics table needs re-deriving on Go's own numbers.

### ⭐ A deep copy is ALSO too slow — which decides A2

Measured at **380 MB of canonical state**, against the tick's 500 ms budget:

| strategy | on-tick cost | |
|---|---:|---|
| deep copy the state tree | **792 ms** | 🔴 1.6× OVER |
| canonical encode | 1,964 ms | 🔴 3.9× over |
| **chunked snapshot** | **1.6 µs** | ✅ |

Encoding off the tick is obvious. **That a deep copy is also too slow is
not**, and it removes the "copy on the tick, serialise later" option entirely.
Discovering it in Phase 4 would have meant rewriting every engine's state
representation with the port otherwise finished.

`internal/events.ChunkedLog` gives an O(chunks) snapshot — and it is cheap for
**this engine's data specifically**, because the seen table is append-mostly
with head-pruning, so at most two chunks are touched per snapshot generation.
`docs/checkpoint-design.md` writes down what that binds on Phases 1–3.

### The time spelling in checkpointed state is Python's, not Go's

The journal carries `"…34.223Z"`. The checkpointed seen-key table carries
`"…34.223000+00:00"` — `datetime.isoformat()`: six fraction digits always,
**none at all** for a whole second, and a `+00:00` zone. Go's `RFC3339Nano`
writes a `Z` and **trims trailing zeros**. All 7,443 entries would have been
wrong, and it would have read as an unexplained checkpoint diff.

### Go and CPython disagree on JSON in five places, and only one has a switch

`\b` and `\f` have **no option at all** in `encoding/json`; U+2028/U+2029 are
always escaped. Hence a hand-rolled encoder rather than post-processing the
one whose output is the contract.

## What went wrong / got stuck

- **Three spec defects, all found by building** — see Decisions below. Each
  was resolvable from stated intent, so each was fixed in the spec rather
  than escalated.
- **A guard-cost figure was quoted from a 3,000-iteration benchmark**, which
  is noise rather than a measurement. It read ~50%; steady state gives ~15%.
  Corrected in the code, the commit and the PR body. The same shape as the
  measurement failures the pre-port work kept finding.
- **A test of mine asserted a §3.2.1-repaired probability triple sums to
  exactly 1.** It does not — `0.49/0.99 + 0.1/0.99 + 0.4/0.99` is
  `0.9999…9` at precision 28, **in both languages**. An assertion of a clean 1
  would have failed a *correct* port. The values are now pinned to CPython's.
- **The pinned worktree went dirty** because its virtualenv sat inside it, and
  the artefact generator correctly refused to certify from it. The venv now
  lives outside.

## Decisions made *(mirror into [[market-maker/decisions]])*

1. **The R2a target was stale and is replaced.** `scripts/a2-run/state-replay.json`
   (1,903,026 B) was committed at `29ae86d` on 11-08. `terminal_at`,
   `pending_quantity` and `settled_game_id` (schema 7) all landed after it,
   and the quoting engine moved. Folding at the pin correctly yields
   **2,091,275 B**. Chasing the old number would have bent the Go port to
   reproduce a four-day-old Python. ⚠ `state-live.json` was **not** retired —
   R2b's three byte-legs still hold at the pin.
2. **The Phase-0 gate is split into 0-a and 0-b.** It required byte-identity
   on the FULL canonical state, which has eighteen subtrees; Phase 0 builds
   **one**. 0-a is every subtree the phase owns (holds now), 0-b is the full
   state at the end of **Phase 3**. Nothing relaxed — the tolerance list is
   still empty.
3. **apd is used only behind `internal/decimal`'s guard-digit wrapper.** Raw
   apd is not a parity-safe decimal for this engine.
4. **The checkpoint snapshot is O(chunks), not O(entries)**, and every
   engine's state representation in Phases 1–3 must satisfy that.
5. **Module path `github.com/Novosapien/inplay-market-maker-go`.** The
   gateway's `github.com/InPlaySports/…` points at an organisation that
   returns 404 — the path never resolved, so it was not copied.
6. **`inplay-fix-contracts` stays deferred** (spec Q4). Structs vendored by
   hand, exactly as Python does; the drift risk is recorded, not closed.

## Questions opened / closed *(mirror into [[market-maker/open-questions]])*

- **CLOSED:** may the Go repo be created? George approved 18-08 — private,
  `main`, under `Novosapien`.
- **CLOSED:** are the ≥2,000 decimal vectors owed? No — 2,285 already existed
  at the pin in `scripts/go-conformance-vectors.json`, regenerating
  byte-identically. The spike's 221 were its sample, not the suite.
- 🔴 **OPEN — needs George.** **AC2 requires a rig session.** It names the
  548.5 MB / 551,939-event GATE corpus, which is a **rig artefact** in neither
  repo, and "one session drives the VM". The *harness* half is proved locally:
  a synthesised, structurally-real 544.4 MB journal folds in **4.25 s**
  (129,773 events/s), 239 MB heap, **0.6% of wall clock in GC** — so the
  spec's "tune `GOGC`" worry is answered rather than deferred. Only the corpus
  is missing. **Options: take a VM session now, or defer AC2 to the Phase-3
  performance run, which is on the rig anyway.**

## Next

- **Phase 1 — `venue-record`.** Read [[market-maker/build/venue]] before
  porting it, and `docs/checkpoint-design.md` first: the venue order record is
  the next table to reach 380 MB scale, and A2's constraint on its state
  representation is already decided.
- ⚠ **Name which of the FIVE order/position state-set questions you are
  answering before writing any venue code.** Reaching for a nearby one caused
  two HIGHs, and the worst sent a sell through a real external bid ($50,366).
- Answer the AC2 question above.
