---
description: "The register of defects and gaps the Go port has found in the Python market maker — what each one is, its evidence, and who owns the fix"
---

# Go Port — Findings Register

> **Component:** [[market-maker/market-maker]]
> **Purpose:** ONE place for everything the Go port has found wrong with the
> **Python reference implementation**, so the list survives the port and can be
> worked through deliberately at the end rather than reconstructed from session
> notes.
> **Status:** open. Phases 0, 1 and 2 are ported and reviewed; Phase 3 is in
> progress. The register grows as the port continues.

---

## Why nothing here is fixed yet

Phases 0–4 of the port are a **faithful** port. The certification is a
differential replay against Python at the pinned commit `fd193a4`, so **any
behaviour change on either side breaks the zero-diff mandate** and the port
stops being provable. Every defect below is therefore:

1. **reproduced exactly** in Go, defect included;
2. **pinned by a test**, so neither side can drift or quietly "improve";
3. **recorded here**, to be fixed on purpose once the port is certified.

The one exception is `GP-1`, where reproducing the behaviour would mean
reproducing a hang. That divergence is deliberate and recorded in code.

⚠ **This register is the port's findings only.** Live issues found by
operating the maker — N40's game-end lifecycle, N41's phantom touch, N43's ask
cap — live in [[market-maker/open-questions]] and are not repeated here.

---

## A · Defects in the Python reference

### GP-1 · `NATSGatewayTransport.stop()` hangs for ever after the writer dies

| | |
|---|---|
| **Where** | `venue/nats_transport.py` — `flush()` |
| **What** | `flush()` is `asyncio.Queue.join()`, which waits for one `task_done()` per queued item. When the writer task dies mid-queue the remaining items never get one, so `join()` — and therefore `stop()` — never returns. |
| **Evidence** | Run against the pinned interpreter, not reasoned about: `join() HANGS after the writer dies — stop() would never return`. |
| **Severity** | 🔴 **Live.** A torn-down connection mid-publish is exactly when this happens, and exactly when shutdown matters. A hang is strictly worse than an error: the process cannot be stopped cleanly and systemd falls back to a kill. |
| **In Go** | ⚠ The ONE deliberate divergence in the whole port. Go returns the writer's death reason with the unsent count. Nothing about the difference is observable in canonical state. |
| **Fix** | Bound the flush (a timeout, or drain-and-count instead of `join()`), and surface the unsent count. Small, self-contained. |
| **Owner** | Maker team · found Go port PR #10, session [[market-maker/sessions/2026-08-18-go-port-phase-1]] |

### GP-2 · `_record` sorts the whole book on every venue event

| | |
|---|---|
| **Where** | `venue/engine.py` — `_record` taking its count from `len(open_orders(...))` |
| **What** | `open_orders` **sorts every ClOrdID in the book**, on every venue event, to produce a count that cannot depend on the order. |
| **Evidence** | Profiled on the real 551,939-event rig corpus: **50.6% of the entire venue fold**. Taking the count without the sort — identical by construction — is **161.81 s → 36.32 s, 4.45×**. |
| **Severity** | 🔴 **Live performance defect**, and it binds exactly where the port's whole justification sits (the ~6.3× gap to NCAA scale). |
| **Why nobody saw it** | The two committed corpora hold 8,090 and 2,931 orders; the rig corpus holds **45,381**. Only rig scale exhibits it. |
| **In Go** | Ported as `OpenOrderCount` — the count without the sort. `OpenOrders` still sorts, for the reconciler and the healer, which genuinely need the order. |
| **Fix** | One-line equivalent in Python: count without materialising a sorted list. |
| **Owner** | Maker team · found Go port PR #8, `docs/ac2-gate.md` |
| ⚠ **Sweep the CLASS** | This is the **third** instance of one scan shape (`_stamp_and_prune`, `RejectBackoff.suppression`, this). Ask of every hot function: *what does it walk, and how often?* |

### GP-3 · §3.2.1's tolerance band and the `[pairs]` guard contradict each other

| | |
|---|---|
| **Where** | `valuation/probability_validation.py` (the band) vs `valuation/engine.py::_on_probability` (the guard) |
| **What** | §3.2.1 **ACCEPTS** any win/tie/loss triple whose sum is within a millionth of 1 and uses the numbers **UNTOUCHED** — that is what the band is for. The guard then asserts `GEV(home) + GEV(away) == $5.00` **EXACTLY**, and `$5.00 × 1.0000005` is not `$5.00`. So a reading the gate deliberately tolerated **raises out of `process()`**, and `cycle()` has no `except` to catch it. |
| **Evidence** | Measured at the pin: **100%** of the accept band's non-exact sums raise, and **2.7%** of §3.2.1 **REPAIRS** raise too — the repair's own precision-28 residue, because `0.49/0.99 + 0.4/0.99` does not come back to exactly 1. |
| **Severity** | 🟠 **Latent, and only by luck.** Sportradar's two percentages sum to exactly 100 on **all 1,089 readings** of the captured game. That is a property of the **PROVIDER**, not of our code, and nothing checks it. `adapters/sportradar.py:93-94` reads SR's two numbers rather than deriving one from the other, so a provider that rounds differently, a schema change, or a second feed makes it live. |
| **In Go** | Reproduced exactly; `TestTheAcceptBandContradictsThePairGuard` pins it, and the differential fuzz drives it every 77 steps so neither side can quietly diverge. |
| **Fix** | ⚠ **A ruling, not a patch** — see `N47` in [[market-maker/open-questions]]. Three readings: tighten the accept band to exactly 1 · relax the guard to the band's tolerance · normalise inside the accept band too. Whichever is chosen, **both implementations change together**. |
| **Owner** | Edwin's number, George's ruling · found Go port PR #12, session [[market-maker/sessions/2026-08-19-go-port-valuation]] |

### GP-4 · The wire's JSON is not the journal's JSON

| | |
|---|---|
| **Where** | `venue/transport.py` (the wire) vs `events/checkpoint.py`'s canonical encoder (the journal) |
| **What** | `json.dumps` defaults to `ensure_ascii=True` on the gateway payloads; the canonical encoder uses `ensure_ascii=False`. One library, two call sites, two spellings of the same value. |
| **Severity** | 🟡 **Latent.** The venue account, bot id and user id all reach the wire from the **ENVIRONMENT**, so a non-ASCII value is a deployment away — and it would be spelled one way in a payload log and another in a journal line, which is the kind of difference that costs an hour during an incident. |
| **In Go** | The two encoders are deliberately separate and neither may be used for the other's job. Go's own `encoding/json` matches **neither** (it escapes `<`, `>`, `&`), so the wire encoder is hand-rolled. |
| **Fix** | Pick one spelling and use it in both places, or document the asymmetry at both call sites. Cheap either way. |
| **Owner** | Maker team · found Go port PR #10 |

### GP-5 · The `[exact-sum]` note is wrong where a §3.2.1 repair is involved

| | |
|---|---|
| **Where** | `valuation/reference_price.py` — the `[exact-sum]` note |
| **What** | The note reasons that Decimal addition at these magnitudes is exact, so the fold's order "cannot change the answer". True while the terms are **short**. A §3.2.1 repair produces a **28-significant-digit** probability, and two such terms round as soon as the running total reaches 1. |
| **Evidence** | A real window read out of the pinned engine: the sorted order gives `68.50635988904318442204161368`, and **four of the six orderings give `…367`**. |
| **Severity** | 🟢 **No behaviour defect** — both implementations already walk the games in sorted id order. It is the **reasoning** that is wrong, and a future edit that trusted the note could remove the sort. |
| **In Go** | `TestTheWindowIsSummedInSortedGameOrder` pins the real order-sensitive window. [[market-maker/build/valuation]] is corrected. |
| **Fix** | Correct the note in the Python source. |
| **Owner** | Maker team · found Go port PR #12 |

---

## B · Structural gaps the port inherits

These are not defects in the code; they are places where the machine cannot do
what a requirement asks, and the port cannot fix them either.

### GP-6 · A new T is not a journalled event, so replay produces different prices

| | |
|---|---|
| **What** | `ingest_reference_numbers` is a **method call**, not an event: §7.3 fixes the event types and none of them is a reference-numbers feed. T is a **price input**, and §10.3 requires replay to reproduce identical Reference Prices from the journal alone. |
| **Consequence** | Once a new T arrives, **replay silently produces different prices**, and §13.2's certification gate fails. Recorded in Python's own `[n23]` note; nothing has closed it. |
| **Port impact** | No journal can drive this path, so the differential fuzz certifies it through the API instead. It is named in the harness's coverage report as *unreachable by ANY fold*. |
| **Fix** | A journalled event type for the daily reference numbers. Natural basis: `source_id + effective_time + revision`, which matches Edwin's correction protocol exactly. |
| **Owner** | `N23` in [[market-maker/open-questions]] — needs the N23/N28 event-type blessing round |

### GP-7 · The committed corpora certify far less than they appear to

| | |
|---|---|
| **What** | Both journals are much weaker workloads than their size suggests. Measured, per subtree: |
| **venue** | 0 `EXECUTION`, 0 `ORDER_REJECTED` (so the backoff's price table is never written), 0 `ORDER_DONE_FOR_DAY`, 0 terminal prunes. The three pending states are unreachable by **any** fold. |
| **valuation** | 0 `OFFICIAL_RESULT`, 0 `ANCHOR_SEED` in either corpus — so settlement, the `[settled]` guard, `[correction]`, `[unseen]` and the whole F2 anchor seed are uncovered. |
| **position** | **0 `EXECUTION` events in either corpus.** Only a fill moves a position, so a byte-identical `position` subtree proves only that an all-zero opening state renders the same on both sides. |
| **Severity** | 🟠 It is not a defect, but any claim of the form *"the corpora prove X"* has to be checked against this. |
| **Mitigation** | `tools/diffreplay` now **prints, per run**, what the journal did not drive, per subtree. Each chunk ships its own Go↔Python differential fuzz driving the API. |
| **Owner** | Closed on the Go side; the Python side would benefit from the same coverage report |

---

### GP-11 · The journal's retention is shorter than its own input file's

| | |
|---|---|
| **What** | The journal is the system of record — §10.3 rebuilds all memory from it, and it is the record of every price the maker published. It lives on a separate `pd-ssd` (`inplay-market-maker-journal`, mounted `/var/lib/mm`) with an hourly snapshot schedule at **7-day retention**. Nothing carries it off the box: `grep -rn -i 'gcs|google.cloud|gs://' src/mm/` returns **nothing**. |
| **The inversion** | George's retention ruling for **Edwin's daily file** is *keep everything in perpetuity* (N19), stored bucket-first as evidence. The journal — the output that file feeds — has a **7-day horizon**. The record of what we quoted is kept for less time than the input that produced it, and §10.4 wants an audit trail of exactly the former. |
| **Also** | Up to one hour is unprotected against a disk-level loss. And the F2 anchor seed reads a LOCAL path (`prior_run_dir`, `runtime/compose.py:278-280`), so the kickoff-freeze carry depends on the prior run's directory still being on that disk — restoring a snapshot to read one directory is heavy for a boot-path dependency, and the seed is what stops a fresh-journal boot erasing an in-game move ($0.685/share on the BENG case). |
| **Severity** | 🟠 **Latent.** The separate-disk-plus-snapshot design is sound as far as it goes, and a VM rebuild does not lose the journal. This is a retention and reachability gap, not a data-loss bug. |
| **Port impact** | ⚠ **None, and deliberately none.** The Go port inherits this unchanged; reproducing it is CORRECT under the zero-diff mandate. Nothing here may be built into the Go runtime while the differential replay is the certification — see the register's rule 5 below. |
| **Fix** | Three options, in `N48`. Cheapest and most consistent with the 03-08 bucket/database split: ship each **closed** run directory to a bucket at rotation. ⚠ Whatever is chosen must not touch the fsync path — the N31 group commit is 2.4 ms and the venue drain is already 98% of the tick. |
| **Owner** | `N48` in [[market-maker/open-questions]] — George's ruling · found 19-08 during Go port Phase-3 preparation |

---

## C · Owed measurements and certification gaps

Not defects — work the port still owes, listed here so it is not lost.

| # | Item | Why it matters |
|---|---|---|
| **GP-8** | **R13's economics table must be re-derived on Go's own numbers, on `n2-standard-2`.** The published table was modelled from an unguarded `exp()`; `internal/decimal` evaluates at guard precision because apd's `Exp` is not correctly rounded, which costs about **15%** more per call. | The decay cache is a **requirement**, not an optimisation — the verdict is unchanged, but the numbers behind it are stale. AC23b already re-measures the hit rate on the rig; the per-call cost needs the same trip. |
| **GP-9** | **AC2 is certified ONCE and is not reproducible from `testdata/`.** The 548 MB gate corpus is a rig artefact and is not committed; only its hashes are. | A future change cannot re-run AC2 without another rig session. |
| **GP-10** | **The rig is 2.5× slower than the dev Mac**, measured twice independently (2.49× Python, 2.5× Go). | Every Mac number in the port is an ESTIMATE of rig behaviour through this factor. It does not retire the rule that a capacity claim is re-taken on `n2-standard-2`. |

---

## How to work this register

1. **GP-3 first** — it needs a ruling (N47) before any code moves, and the
   ruling changes both implementations.
2. **GP-1 and GP-2 next** — both are small, self-contained Python fixes with
   measured evidence, and GP-2 is worth real time at NCAA scale.
3. **GP-4 and GP-5** are tidy-ups; do them with whatever touches those files.
4. **GP-6** rides the N23/N28 event-type round.
5. ⚠ **Nothing in section A may be fixed in Python while the port's
   differential replay is the certification.** Fixing one side without the
   other turns a green gate red for the wrong reason. Land them as PAIRED
   changes after Phase 4, or in the Phase 5 spec where re-derivation is the
   point.
