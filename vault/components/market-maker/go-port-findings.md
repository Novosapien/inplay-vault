---
description: "The register of defects and gaps the Go port has found in the Python market maker — what each one is, its evidence, and who owns the fix"
---

# Go Port — Findings Register

> **Component:** [[market-maker/market-maker]]
> **Purpose:** ONE place for everything the Go port has found wrong with the
> **Python reference implementation**, so the list survives the port and can be
> worked through deliberately at the end rather than reconstructed from session
> notes.
> **Status:** open. Phases 0, 1, 2 and **3** are ported and reviewed; Phase 4
> is next. ⭐ **Gate 0-b passes as of 19-08** — all eighteen subtrees
> byte-identical on both corpora. The register grows as the port continues.

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

⚠⚠ **And it records defects in PYTHON, not defects in the Go port.** The port
finds plenty of its own — a mis-transcribed literal, a name doing two jobs, a
`select` that races where Python's sequential checks could not. Those belong in
the port's Drift Log, and putting one here would wrongly accuse the reference.
Before adding an entry, confirm the pinned Python actually has the defect.

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
| **Owner** | ✅ **RULED 19-08 — George: "prices being a millionth off is fine."** Option (b): **relax the pair guard to the accept band's own tolerance.** Concretely, `pair_total != WIN_VALUE` becomes `abs(pair_total − WIN_VALUE) > WIN_VALUE × sum_accept_tolerance` — a tolerance of **$5.00 × 1e-6 = $0.000005**, half a thousandth of a cent. ⭐ **It changes no stated behaviour**, only an over-tight assertion: the guard exists to catch swapped sides and a badly broken repair, and neither can hide inside a millionth. ⚠⚠ **NOT IMPLEMENTED YET, AND THAT IS DELIBERATE.** Phases 0–4 of the Go port are a FAITHFUL port certified by differential replay against the pin, so changing either engine now breaks the zero-diff mandate — Go would stop raising where Python raises, and the valuation fuzz drives that case every 77 steps. **The change lands at Phase 5, in BOTH engines together.** Found Go port PR #12, session [[market-maker/sessions/2026-08-19-go-port-valuation]]; ruled 19-08 |

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

### GP-15 · 🔴 `anchor_seed.py`'s reader RAISES, against its own "NEVER raises" docstring

| | |
|---|---|
| **What** | `read_prior_anchors` exists so that a boot **cannot** die because a prior run left a bad file. Its docstring says it never raises. It does. `_accepted_lines` catches `(JSONDecodeError, KeyError, TypeError)` — but a prior journal line whose `record` is a **string** makes `dict(record["record"])` a **`ValueError`**, which is not in that tuple. The exception escapes `read_prior_anchors` entirely and **kills the boot**. |
| **⚠ Why this one is worse than its severity suggests** | It is the exact failure the module was written to prevent. Every other failure path in the reader returns "no seed" and logs loudly; this one takes the process down. And the input that triggers it is **a file the reader itself declares untrusted** — the whole reason it hash-verifies a checkpoint and constructs the real typed value before believing anything. |
| **Reachability** | One malformed line in one prior run's journal. The reader runs on **every** boot that finds a prior run directory. |
| **Evidence** | `internal/runtime/anchor_seed.go` + `testdata/anchor-seed/` in the Go port. ⭐ The raise is recorded **IN the artefact** as `python_raised`, not in a code comment, and the raise **count is asserted as a floor AND a ceiling** — so a NEW hole in the reference fails the Go gate rather than passing unnoticed. 43 prior-run directories, each itself a planted defect, including a checkpoint that is a directory, three where the newest must win, a corrupt newest that must fall back, a torn crash tail, a tampered payload, and a chain (a prior run that was itself seeded). |
| **Severity** | 🔴 **Boot-fatal, live.** |
| **Fix** | Add `ValueError` to the caught tuple — or catch `Exception` in a reader whose contract is that it never raises. ⚠ Go is **deliberately lenient** here rather than bug-compatible, because the spec's wording specifies the contract (*"every failure path returns 'no seed', loudly logged"*) rather than the implementation. That divergence is recorded in the code. |
| **Owner** | 🔵 **Ours** · found 19-08, Go port Phase 4's `boot-features` chunk |

---

### GP-16 · 🔴 A large journal walks the boot past the gateway's 30 s dead-man grace

| | |
|---|---|
| **What** | The maker sends its **first heartbeat before it builds anything**, so the beat itself is fast. But between that beat and the run loop starting the beat task, **exactly one heartbeat has gone out** — and the work in between is a full journal replay. On a **1,073,742,282-byte** journal (1,093,132 lines, 1,090,732 events) the whole boot takes **1 m 03.334 s**. The gateway's grace is **30 s**. |
| **The numbers** | First heartbeat **+8.157 ms** — the AC8 clause passes by four orders of magnitude. Whole boot **1 m 03.334 s** on the dev Mac, which runs ~2.5× faster than `n2-standard-2`, so the rig reads **≈ 2 m 38 s**. |
| **⚠ Why it is reachable rather than theoretical** | A checkpoint boot is fast, so this looks like an edge case. It is not: **R-D06 bumps `MM_CONFIG_VERSION` on every deploy**, and `LoadLatest` only accepts a checkpoint of the running version — **so a deploy always boots on a FULL replay.** That is precisely when the journal is largest. `build/runtime.md` puts growth at ~70–90 MB/h at 180 books, which makes 1 GB a **12–14 hour game day**. |
| **Evidence** | Measured in the Go port's `boot-features` chunk on a synthesised 1 GB journal. The test **logs the number rather than asserting a pass**, so the exposure is visible on every run instead of being encoded as acceptable. ⭐ A design correction came out of the same work: `Boot` first took a ready-made stack, which would have spent the entire grace inside `build()` — it now takes a `Build func()` and the ordering test asserts `beat` → `build` → `replay`. |
| **Severity** | 🔴 **Live in the running Python bot.** The Go port reproduces the shape faithfully; Python's entry point has the identical ordering. This is not a port defect. |
| **⚠ Re-measured 19-08 in `deploy`, and the number MOVED — upward** | Same test, same synthesised journal, on the same Mac: **1 m 12.786 s**, against `boot-features`' 1 m 03.334 s. Read the 9 s as **ambient load on a shared dev box, not a regression** — nothing between the two runs touched the boot path. It matters only because it says the Mac figure is a soft one: the rig estimate should be read as **≈ 2 m 38 s to 3 m**, not as a point value. |
| **⚠⚠ AND ONE FIX MADE IT SLIGHTLY WORSE, DELIBERATELY** | `deploy` changed `events.FromMap` to validate on every journal read, matching Python's `__post_init__` — Go was **silently trusting a journal line whose payload no longer matched its hash, where Python's boot REFUSES it**, a replay-equality divergence under R2a. Validating re-hashes every payload, and the boot reads the journal **twice** (the recovery scan and the replay). Isolated cost **+1.762 µs/event** → **≈ +3.8 s at 1 GB on the Mac, ≈ +9.6 s on the rig**, about **+5%**. The whole-boot runs after the change were **1 m 12.625 s and 1 m 15.164 s** — a 2.5 s spread between two identical runs, so the end-to-end measurement is **consistent with +5% and not precise enough to confirm it**. Working: the Go port's `docs/payload-hash.md`. ⚠ **Whoever fixes this grace must budget for that 5%**, and must not reach for reverting the validation to buy it back: the boot is already ~6× over the grace, so 5% changes no decision, and the divergence it closes is a correctness one. |
| **⭐ THE CHECKPOINT MITIGATION NOW EXISTS IN GO, AND IT IS WORTH ~2x** | Until 19-08 the Go maker **never wrote a checkpoint** — `runtime.Options.Checkpoint` was unset, so `events.WriteCheckpoint` had no production caller while every boot called `LoadLatest`. So on the one path an operator is told to use, Go had **no mitigation where Python has one**, which was a divergence from the pin rather than a faithful port. That is closed: `cmd/mm` writes one, capture synchronous and write detached. ⚠⚠ **But the mitigation is far weaker than "replays only the tail" implies, in BOTH engines.** Measured at 1 GB (1,078,365,723 B / 1,095,584 lines): scan-plus-replay **18.858 s cold** against **9.545 s with a checkpoint** — folding 4,980 events instead of 1,093,175. A boot makes TWO full passes and a checkpoint removes only the **recovery scan**; the replay still reads and validates every line before filtering by sequence (`acceptor.go:303`, and `acceptor.py:191` is identical). **A shorter fold saves almost nothing next to reading a gigabyte.** ⚠ So "restart without bumping the version" halves the boot — it does not rescue it. |
| **Fix** | ⚠ **Not available inside a zero-diff phase** — any change to the boot ordering is a behaviour change. Options for Phase 5 or for ops: beat during the replay rather than only before it; widen the grace; make a deploy able to load the prior version's checkpoint; **or make `Replay` filter by sequence BEFORE it parses**, which the measurement above says is where the remaining time is. **George's to route.** |
| **Owner** | 🔴 **George's** · found 19-08, Go port Phase 4's `boot-features` chunk · re-measured in `deploy` |

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
| **Owner** | ✅ **RULED 19-08 — George chose option (1): ship each closed run directory to a bucket at rotation.** Closes the retention inversion, the anchor seed's local-path dependency and the missing cloud path. ⚠ The one-hour window is **ACCEPTED, not closed** — continuous shipping was rejected as invasive. 🔨 **BUILT 19-08** in the Go port's `internal/runtime/rotation.go`, and ⚠⚠ **it is a deliberate DIVERGENCE from the reference**, confined to a path a fold cannot observe: it only ever READS a directory the engine has finished with, so no journalled state and no canonical comparison can see it. It ships at BOOT rather than at shutdown, because the PRIOR run's directory is the one that is definitively closed and shutdown-shipping sends nothing after a crash, an OOM or a kill -9 |

---

### GP-12 · 🔴 apd cannot represent the numbers CPython stores, and the a2 corpus needs them

| | |
|---|---|
| **Where** | `github.com/cockroachdb/apd/v3` — `decimal.go:71`, `MaxExponent = 100000` (and `MinExponent = -MaxExponent`), a HARD package-level cap independent of the Context's own bounds |
| **What** | CPython's decimal context runs to `Emin/Emax = ±999999`. apd stops at `±100000`. Any value outside that band **does not exist in apd** — it is not a rounding difference and no wrapper closes it. |
| **Evidence** | Folding the a2 journal through the whole machine, Python's `variance_rate` for `IPTCCHIE` is `4.385597164977966123725114636E-916199`. Go cannot hold it: `decimal mul: exponent out of range`, even for `1 × tiny`. ⚠ **`variance_rate` is a CHECKPOINTED STRING**, so the value reaches canonical state directly — this is not an intermediate. |
| **Why the corpus reaches it** | The a2 journal spans **60,871,126 seconds** — nearly two years. Its probability readings carry the captured **2024** game's own timestamps while its venue events and sweeps carry the **2026** replay's. The decay factor over that Δt is `exp(−2.1 × 10⁶)`. |
| **Severity** | 🟠 **Blocks gate 0-b on the a2 corpus; almost certainly harmless in production.** In a live run consecutive events are seconds apart, so Δt never approaches this. The two-year span is an ARTEFACT of how the corpus was assembled, not an operating condition. |
| **Found alongside** | ⭐ A **separate, genuinely dangerous apd defect that IS fixed**: `Context.Exp` works only while `\|x\| ≤ 23 × precision` and refuses to bump precision past 1000, so past `\|x\| = 22,977` it returns **ZERO** where Python returns the real value (`exp(−34657.359…)` → `0E-1000031` vs `3.163856671530324185927899991E-15052`). Fixed in `internal/decimal` by range reduction (`x = n·ln10 + r`, so `exp(x) = exp(r) × 10ⁿ`, a pure exponent shift); 4,000 vectors from the pin, 2,495 of them past the cliff, all exact. |
| **The ruling needed** | Three readings, and it is **George's**: (a) accept that gate 0-b is certified on the six-game corpus and NOT on a2, recording a2's four affected subtrees as a known limit; (b) rebuild the a2 corpus so its readings and venue events share one timeline, which removes the two-year Δt and is arguably what the corpus should always have been; (c) carry a scaled representation inside `internal/decimal` so extreme exponents survive — real work, and it changes the port's most load-bearing package. ⭐ **(b) is the cheap one and probably right**, because the Δt it removes is not a thing the engine can ever see in production. |
| **Owner** | ✅ **CLOSED 19-08 — George ruled (b): rebuild the a2 corpus on one timeline.** `testdata/generators/a2_corpus_rebuild.py` drives the real capture through `six_game_workload.run_profile`, whose `feed_game` already rewrites every stamp onto the run's own clock — which is why the six-game corpus never had the gap. The rebuilt corpus spans **212.6 s** and **all eighteen subtrees now match on both corpora, so gate 0-b passes.** |
| **⚠ The trade George took** | At 120× the capture's real ~16-second reading cadence becomes 0.13 s, so **every reading lands in §3.3.1's Current band** and the a2 arm no longer exercises Warning, Degraded, Invalid, the §3.4.1 promotion dwell, or the §3.5 deductions. He took it with those numbers in front of him. The mitigation is real: the RETIRED corpus did not exercise them either — two-year-old readings are Invalid on all of them — and `testdata/valuation-fuzz/` drives that surface directly through the API. |
| **⚠⚠ The LIMIT is not closed, only the CONDITION** | apd still stops at ±100000 and always will. The operational fact that follows: **a security whose Reference Price goes quiet for 76.9 days leaves apd's range.** The decay is `exp(−ln2·Δt÷20)`, so the rate crosses `1e-100000` at `Δt = 100000·ln10·20÷ln2 = 6,643,856 s`; the retired corpus's gap was **nine times** past it. That is far outside any real session — but *"we never go quiet that long"* is the REASON it is safe, and the reason now lives beside the limit in `internal/decimal/exponent_limit_test.go`: four tests on the exact numbers, naming the boundary on both sides and computing the 76.9-day budget rather than asserting it. |

---

### GP-13 · 🔴 The six-game reference is folded under a config version its own journal does not carry

| | |
|---|---|
| **Where** | `scripts/go_reference_checkpoint.py` — `REPLAY_CONFIG_VERSION = "GO-REFERENCE"`, used by `_replay_to_state()` to fold the reference it commits |
| **What** | The generator writes a matched pair — `journal.jsonl` and `state.canonical` — but folds the state under **its own** config version, not the one the RUN that produced the journal used. The run mints `CB1{epoch}` (`six_game_workload.run_profile`) and stamps it into every record. So the committed journal says `CB11787049727` and the committed reference is Python's fold under `GO-REFERENCE`. |
| **Why it is a trap and not a footnote** | The config version **SALTS every §5.7.3 draw**. Reading it off the journal's records is the natural thing for any consumer to do, and it is the wrong answer. A fold under the wrong one reproduces every price that does not depend on a draw and gets every drawn one wrong — so the result reads as *nearly correct* rather than as obviously broken. |
| **Evidence** | The Go port fell into it for the length of a whole chunk. `tools/diffreplay` folded under `CB11787049727` and got 13 of 18 subtrees byte-identical, with `quotes` differing in `extra_ticks`, `ask_carries_odd`, the drawn `shape`, every price that followed one, and `quote_number` running ahead on 3 of 12 securities — because a changed book changes whether a cycle publishes at all. It was carried as **"a σ²/width divergence in `quotes`"**. |
| **What it cost** | A decay-cache investigation (exonerated — folding with the cache off is byte-identical, which incidentally re-confirmed AC23a on a venue-bearing corpus for the first time), a marketable-guard investigation (exonerated — Python's own run logs `MARKETABLE_GUARD_BLIND`, so it refuses nothing either), a determinism check (three runs, identical, so not map order), and a bisection harness over 15,000 events. The bisection is what exposed it: folding the journal with **Python** at the version the harness was passing made the two AGREE, which can only mean the committed reference was folded under something else. |
| **⭐ And documentation did not prevent it** | `testdata/README.md` already stated `GO-REFERENCE` in as many words, and the `-config-version` flag's own help text already warned about this exact failure mode. Neither helped. |
| **Severity** | 🟠 **No production impact whatsoever** — it is a property of a certification artefact, not of the engine. But it is a live trap for every future consumer of that pair, and it wastes the most expensive kind of time: the kind spent looking for a bug that is not there. |
| **Fix** | Two halves. On the Go side, done: `assertReferenceIsForThisJournal` REFUSES unless the manifest beside the reference agrees with the config version being used, and unless the manifest's `journal_sha256` and `canonical_state_sha256` match the two files being compared — four planted defects prove it, including the exact one that was carried. On the Python side, owed: the generator should fold under the version the run actually used, or state loudly in the artefact itself that it does not. |
| **The transferable rule** | **A setting that is part of a certification target must be ENFORCED against that target's own manifest, not documented beside it.** The other settings of this shape are `-securities` (the a2 corpus's universe) and the pin itself. |
| **Owner** | 🔵 **Ours** — the Python-side half is a one-line change to the generator, to be made when the pin next moves · found 19-08, Go port Phase 3 |

---

### GP-14 · 🟠 Three documents give three different values for `sweep_max_interval_s`

| | |
|---|---|
| **What** | The sweep's cadence and its missed-interval tolerance have moved three times, and the places that record them have not moved together. |
| **The four sources** | `dictionary.py` — **0.5 / 2.0**, the shipped values, with a comment block that records all three rulings correctly. `loop.py:43-44` — comments reading `# ✅ §3.1.4 — 2.0 s` and `# ✅ §3.1.4 — 2.5 s`, which are §3.1.4's ORIGINAL numbers and predate every ruling. `build/runtime.md` — **1.0 s** for the max interval, which was George's 08-13 evening ruling and never picked up his **14-08** relaxation to 2.0. `parameters.md` row 35 — **2.0 s · 2.5 s ✅ E18**, superseded by its own row 223 further down the same table. |
| **⚠ Why the `loop.py` comments are the worst of the four** | They carry the **✅ marker**, which under the vault's own ground rule means *confirmed*. A reader checking a number against the code finds a confirmed-looking value that the code beside it does not use. |
| **Evidence** | `testdata/generators/runtime_producers.py` was written with 2.0 / 2.5 hard-coded — taken from `loop.py`'s comments and corroborated by `build/runtime.md` — and its own provenance assertion refused to run, naming the shipped 0.5 / 2.0. The generator now READS the dictionary and records what it read, and its step plan is written in MULTIPLES of the cadence, so a fourth ruling regenerates the artefact instead of silently invalidating it. |
| **Severity** | 🟠 **No behavioural defect** — the code reads the dictionary and the dictionary is right. It is a documentation-integrity defect, and the risk is entirely to whoever trusts the wrong copy. The value decides when a sweep counts as MISSED, which drives §3.4 status and §3.5 confidence across all 170 books. |
| **Fix** | Delete the numbers from `loop.py`'s comments and point at the dictionary; update `build/runtime.md` with the 14-08 ruling; retire `parameters.md` row 35 in favour of row 223. ⚠ None of it touches behaviour, so none of it is blocked by the zero-diff mandate. |
| **Owner** | 🔵 **Ours** · found 19-08, Go port Phase 3's `runtime` chunk |

---

## C · Owed measurements and certification gaps

Not defects — work the port still owes, listed here so it is not lost.

| # | Item | Why it matters |
|---|---|---|
| **GP-8** | **R13's economics table must be re-derived on Go's own numbers, on `n2-standard-2`.** The published table was modelled from an unguarded `exp()`; `internal/decimal` evaluates at guard precision because apd's `Exp` is not correctly rounded, which costs about **15%** more per call. | The decay cache is a **requirement**, not an optimisation — the verdict is unchanged, but the numbers behind it are stale. ✅ **AC23b's hit rate is MEASURED, 19-08: 82.39%** on the venue-bearing arm (3,856 lookups, 3,177 hits, 679 distinct Δt keys, zero evictions) against a ≥80% bar — and the rate is machine-independent, so that half needs no rig. ⚠ The **per-call cost** still does. ⭐ Worth knowing while reading this row: **Python has no decay cache at all** — `grep -rn 'DecayCache\|decay_cache'` over `src/`, `scripts/` and `tests/` at the pin returns nothing. R13 is a Go-side ADDITION, which is why AC23a (byte-identical with the cache ON and OFF) is the stricter of the two acceptance criteria: the cache may exist only because it cannot be observed. |
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
