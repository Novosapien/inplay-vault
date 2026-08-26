---
description: "E51 ported to the Go maker with the corpora pinned, then the Go venue leg made Python's: the resize pass removed and the inbound leg's silent drops found and fixed"
---

# 2026-08-26-b — The Go maker carries E51, and its venue leg becomes Python's

> **Who:** AI session (the Go side), resumed from the 21-08 handover.
> **Type:** build, local only. Nothing deployed. No VM touched.
> **Refs:** Go PR [#19](https://github.com/Novosapien/inplay-market-maker-go/pull/19) `feat/e51-parameters` → `feat/phase-3-ingestion` ·
> Python `main@f9eec8b` (the port target) ·
> [[market-maker/sessions/2026-08-21-go-maker-ladder-shape]] (the handover) ·
> [[market-maker/sessions/2026-08-20-widen-and-thin-parameter-round]] (E51) ·
> vault PR #41 (the 21-08 note, opened this session) · N65 · N66.

## What we did

1. **Opened vault PR #41** for the 21-08 session note — the handover's
   pending step.
2. **Re-read the world before the port.** Two facts had moved since the
   handover:
   - Gateway PR #28 (per-bot dead-man) merged 19:31Z and, per the parallel
     session, **deployed to both gateway VMs 19:39–19:40Z**. N66's live
     hazard is closed at the source. The rule stands: no Go maker run without
     George's explicit go.
   - Python `main` moved again today: `f9eec8b` (George, 20:11 BST) puts the
     rungs back to the **drawn 1–3**, superseding Edwin's 1/1. The handover's
     "levels 1/1" was stale by four hours. The port target is `f9eec8b`.
3. **Ported the E51 set to Go.** The shipped dictionary now carries:
   `min_width_ticks` 25 · levels **1–3** · `base_size` 550 · `min_quantity`
   100 · `material_qty_change` 50 · NEW `skew_reference_shares` 48,000 ·
   NEW width floors Defensive 50 / Overnight 100. Behaviour ported with the
   numbers: the per-state floor wired into the width (widest wins, applied
   after the extra), the lean's denominator moved off §4.3's float for the
   PRICE skew only (EPR keeps the float), and `PositionRecord` reports the
   applied lean beside the float-based ratio — exactly Python's
   `[skew-not-float]`.
4. **Kept the corpora honest.** Every certification target under `testdata/`
   is Python@fd193a4's output under fd193a4's numbers. A fold under the new
   dictionary disagrees on every drawn size — measured: the a2 corpus's
   `quotes` subtree diverges at byte 92, three asks where the pin has five.
   So the quote engine now takes a `Policy` at construction instead of
   package literals, `config.ReferencePin()` carries fd193a4's rows, and the
   differential harness resolves the dictionary from the corpus manifest's
   `commit` — it refuses a commit it cannot name. `make diff`: both corpora
   18/18 byte-identical, checkpoint arm and decay arm green.
5. **Tests.** 44 new: the Go half of Python's `test_edwin_20_08_parameters.py`
   (quotes + dictionary), the position engine's two denominators, the pin's
   registry, and one that proves the pin is load-bearing (the shipped
   dictionary must NOT reproduce the pinned corpus). `make gate` PASS.

## What we learned

- ⭐ **A dictionary value cannot be two values, and the corpora need two.**
  Python does not have this problem because it simply no longer reproduces
  fd193a4's corpora; the Go tree keeps them as the proof of the MACHINE. The
  pin is a test target, not an operator option: it fails `Validate()` on
  purpose (`SkewReferenceShares` 0), so `cmd/mm` cannot boot on it.
- ⭐ **The binding gate's `readFromDictionary` shape was already the answer.**
  Thirteen rows moved from AST-swept literals to "read off a
  `config.Configuration` parameter" — the gate's own end state, and the
  literal is gone rather than duplicated.
- ⚠ **N65 is NOT moot.** The handover expected `levels 1/1` to dissolve the
  monotonicity question. George's 26-08 ruling keeps 1–3 rungs, so the
  independent per-level ±25% draw still inverts adjacent rungs — and the
  step is now 550 × 0.72 against the same jitter, so the ~30% figure stands.
- ⚠ **Three lint findings blocked the gate, two of them from PR #18**
  (`real` shadows a predeclared identifier; an `err` shadow in the
  test-only test). Fixed in passing; noted in the PR.

## What went wrong / got stuck

- Two of my own test bugs on the first run: an envelope built from a Go map
  literal (the codec wants `codec.Number`), and a size band that forgot
  deeper rungs decay below the touch (314 = 550 × 0.72 × VF). Both fixed
  before the gate ran.
- `cmd/mm`'s opening-ladder test borrows its 18 from the run-loop parity
  harness, which folds Python@fd193a4. It now builds under the pin and says
  why; a second test asserts the SHIPPED ladder against its own policy
  (4–12 instructions for two books, no order above 688 shares).

## Decisions made *(mirror into [[market-maker/decisions]])*

- ✅ **The Go maker's shipped dictionary is Python `f9eec8b`'s** — E51 plus
  the 26-08 rung range. Not the handover's 1/1.
- ✅ **The corpora fold under the dictionary their manifest's commit names.**
  `config.DictionaryAtCommit` is the registry; an unknown commit is refused,
  never guessed. Regenerating a corpus means registering its commit first.
- ✅ **`SkewReferenceShares` 0 means "§4.3's float"** and is reserved for
  the pin — a shipped dictionary must be positive (Validate).

## Questions opened / closed *(mirror into [[market-maker/open-questions]])*

- **N65** — NOT moot after all (above). Still George + Edwin.
- **N66** — the gateway half is deployed (parallel session, 19:39Z). The
  engine half — `MM_BOT_ID=mm-test` in the test env — is config, not code.

## Next

1. **Review + merge the Go PR** (`feat/e51-parameters` → `feat/phase-3-ingestion`).
2. **Stand up the test-maker env** on `inplay-market-maker-go` per the 26-08
   census note: `MM_TEST_ONLY=on`, `MM_BOT_ID=mm-test`,
   `MM_VENUE_ACCOUNT=2559580864`, `MM_SECURITIES` = the 170 twins, own
   journal, own `MM_READINGS_DURABLE`. ⚠ 160 of the twins hold no shares —
   a position transfer is needed before a maker can offer them.
   ⚠⚠ No run without George's explicit go.
3. **Tell Edwin the rungs moved** (1/1 → 1–3, book-visible) — George's
   26-08 ruling, both engines.
4. **Decide N65 on evidence** once the 1–3 book has been watched live.
5. Longer term: regenerate the corpora at a current Python commit and retire
   `ReferencePin()` — register the commit in `pin.go` first.

---

# Part 2 — "just use the same process as the Python one"

> **Refs:** Go PR [#20](https://github.com/Novosapien/inplay-market-maker-go/pull/20) `feat/python-lifecycle` → `feat/phase-3-ingestion` ·
> commits `94a21b5` (resize pass removed) · `86ec89e` (the inbound leg) ·
> three parallel line-by-line comparisons against Python `main@f9eec8b`.

## What we did

George, after the E51 port: the parameters were never the whole story.
The Go maker, at the SAME 3–6 × 10,000 the Python maker ran supervised,
put **more than six orders a side** on a book, with a fat middle rung —
"it just seemed like the replacer wasn't working". His ruling: **copy the
Python process exactly.**

1. **Removed the 21-08 resize pass** (`94a21b5`). Between 21-08 and 26-08
   Go replaced a kept order whose size belonged to another rank. Python
   rests it until gone (N10), whatever rank it now sits at. Go now does the
   same — `ClearFirst`, `withinVariationBand`, the "pin the reference
   lifecycle" test helpers and `clear_first_test.go` are gone; the churn
   simulation's re-space case asserts Python's answer (three moves, nothing
   resized, silent next pass). ⚠ This reverses the 21-08 ruling and brings
   rank drift back exactly as Python has it; at 1–3 rungs × 550 the cost
   is 550-vs-285 at worst.
2. **Three parallel comparisons, file by file, against `f9eec8b`:** the
   venue state machine (`engine.py`/`engine.go`, `state`, `order`), the
   converger + marketable guard + backoff (`sync`, `backoff`, `tob_cache`,
   `writer`, `transport`), and the inbound translation + drain
   (`adapters/gateway`, `legs.go`, the tick). **Every engine and the
   translator itself is a faithful port** — every transition, state set,
   pending-price occupancy, examined cap, budget, guard verdict, backoff
   schedule and payload field checked and agreed.
3. **The divergences that CAN leave an order standing were all in Go's
   wrapper around the translator, and Python has none of them** — fixed in
   `86ec89e`:
   - Go **dropped every order-stream message** between the subscribe and
     the end of `Build` (minutes on a real journal). Python's
     `asyncio.Queue()` buffers from the subscribe and drains from the first
     tick.
   - Go's queue was a **4,096-deep channel that dropped on overflow**.
     Python's is unbounded.
   - Go **skipped every translation refusal** (a bust, an unknown verb, an
     unmodelled side) with a counter. Python halts on all but an unmapped
     fill.
   - Go printed the first poison message ever; Python prints every one.
4. **The inbound leg is now Python's shape:** the leg exists before the
   subscription and accepts raw bytes into an unbounded queue; `Build`
   binds the symbol map; translation runs on the tick in `Next()`; an
   alien fill is skipped loudly, poison is counted and printed every time,
   and a `GatewayTranslationError` halts the run — the `runtime.Source`
   contract now carries an error. The readings leg keeps its bounded queue
   because JetStream redelivers what it drops.

## What we learned

- ⭐ **A dropped ack is not a lost log line — it is an invisible resting
  order.** The record keeps a `PENDING_SUBMIT`/`PENDING_REPLACE` that
  OCCUPIES its price (so the price is never re-posted) and is never
  ACTIONABLE (so it is never cancelled), while the real order rests at the
  venue unknown to the diff. One extra order per affected level, for ever.
  That is the ">6 a side" shape, and the 21-08 resize could not have
  caused or cured it.
- ⭐ **The parity harnesses were blind to it by construction.** On a
  scripted timeline every ack arrives and none is refused, so
  `runloop-parity` and `gateway-parity` pass while the live wrapper drops.
  The proof of a port is not only that the engines agree; it is that
  every message reaches them.
- ⚠ **The boot window was the likeliest live trigger.** mm-2 restarted four
  times on 20/21-08 while the dead-man fired 21 times; every sweep ack and
  every previous-life fill that landed during a Go boot was discarded.
- ⚠ Two Go-only paths remain, both loud and both George's: the
  `MM_TEST_ONLY` wire guard refuses AFTER `RegisterSubmit` and aborts the
  pass (the process exits — the boot half should make it unreachable), and
  `sync.go` reads an empty venue symbol for an unmapped id where Python
  raises. Neither can leave a quiet extra order.
- ⚠ **Which build the VM ran is unknown.** `/usr/local/bin/mm-go` is "a
  21-Aug build"; two of that night's superseded attempts (the drawn-size
  trigger flood, the string-keyed doubled level) each produce extra orders
  on their own. Confirm the binary's commit before reading any old
  observation as evidence.

## Decisions made *(mirror into [[market-maker/decisions]])*

- ✅ **The Go maker follows Python's venue process exactly** (George
  26-08). No resize pass; rest-until-gone verbatim. Reverses the 21-08
  "resize is the behaviour" ruling.
- ✅ **The inbound leg buffers, never drops, and halts on a refusal** —
  Python's `[inbound-poison]` contract, now Go's.

## Questions opened / closed

- None numbered. N65 stands (depth stays, jitter inverts).

## Next (supersedes the list above where they differ)

1. **Merge order on `inplay-market-maker-go`:** #19 (E51) then
   `feat/python-lifecycle` — they touch the same runtime test files at
   different lines; rebase the second if git cannot merge them.
2. **Before any Go run:** read the commit of the VM's `/usr/local/bin/mm-go`
   and the `MM_CLORDID_PREFIX` in `/etc/mm-2/env`. A run with the prefix
   unset mints `MM` + 16 hex; a later run with `MMGO` treats those as the
   Python maker's and leaves them standing.
3. Then the test-maker env, with George's go.

### ✎ 21:46Z — deployed, not started (George: "merge them then put the binary on there")

- Go #19 and #20 merged → `feat/phase-3-ingestion@75ac263`. Linux binary
  built locally (go 1.26.5, `-trimpath`), sha `154cf8474840c036…`, uploaded
  and verified; installed as `/usr/local/bin/mm-go` on `inplay-market-maker-go`
  (backup `mm-go.bak-2e557cfb` = the 21-08 build, whose commit is still
  unknown).
- `/etc/mm-2/env` rewritten for the test maker (backup
  `env.bak-2026-08-26-cfg0047-mm2`): `mm-test` · `MM_TEST_ONLY=on` · account
  `2559580864` · `CFG-0048-GO` · fresh `go-run12` journal · all 170 twins ·
  new `supervised-inputs-170-twins.json` (each twin = its real ticker's row
  from the 180 file; the ten original twins already carried exactly that) ·
  boot heal off · `MMGO`. Everything else as mm-2 had it.
- Dry-run of the boot gates with a dead NATS URL: `mode=supervised
  config_version=CFG-0048-GO` then the NATS refusal — the sandbox lock and
  the mode check pass. **Service not started.** Entitlement is off the list
  (George: `MM_SECURITIES` + `MM_TEST_ONLY` gate it).
- ⚠ The last mm-2 run's shutdown line read `gateway 13992 seen/0 dropped/0
  untranslatable` — so run 11 lost nothing past the queue; the boot window
  (uncounted by design) remains the only inbound loss that run could have
  had. The proof is the first re-quote on this build.

### ✎ 21:48–21:56Z — started, validated, then swapped to the old shape on George's ask

- **21:48Z started** (George's go, after the walls were re-verified on the box:
  `MM_TEST_ONLY=on`, account 2559580864, 170 symbols all `.TEST`, boot heal
  off, bot `mm-test`). Boot: `TEST-ONLY MODE: 170 .TEST twins named`, 694
  opening instructions, composed in 14 ms.
- **The venue's own index, one minute in:** mm-test 712 ACCEPTED on 170 books,
  **zero on a real ticker**, per side 1 / 2 / 3 on 94 / 117 / 128 sides —
  never above 3. The 137 IPO asks (unattributed bucket) and snt-1's order
  untouched. **Eight minutes and many overnight re-spaces later:** 718 orders,
  max 3 a side, 0 duplicate same-side prices, no refusals, no poison. ⭐ The
  ">6 a side" shape did not recur on the #20 build.
- ⚠ The test account already holds shares (`pos_size` 100,000 on the twins
  with fills reported), so asks quote too.
- **"Cardinals and Falcons show no prices":** not the maker. AFFC.TEST rests
  3 bids / 3 asks (best 52.49 / 53.49) and CARD.TEST 1 / 1 at the venue, and
  BOTH gateways' `/quotes` carry a best bid and offer for all 170 twins. The
  gap is on the panel's quote path — the parallel session's symbol map.
- **George: "the old configuration, so I can validate how it looks — 1–3
  rungs is hard to judge."** Built `test/old-ladder-shape` (`b3d18b9`,
  NEVER merge): the pin's 3–6 × 10,000 / floor 1,000 / width 1 on the E51
  lean and floors. Deployed 21:53Z as `CFG-0049-GO-OLDSHAPE` with the
  journal KEPT so the record knew its 718 orders (there is no per-bot cancel
  on the gateway). Result: 1,526 orders, max 6 a side, 0 duplicates — but
  **413 old orders under 1,000 shares still rested**, every one at a price
  the new grid also wanted (AFFC.TEST's touch: the old 615 kept above a
  fresh 3,985). ⭐ That is rest-until-gone doing exactly what Python does,
  and the visible cost of removing the resize.
- **George: "make sure it clears the old resting orders."** 21:56Z: fresh
  journal `go-run13`, **`MM_BOOT_HEAL=on`**, `CFG-0050-GO-OLDSHAPE`. The
  healer is scoped by the prefix: it cancels only `MMGO` + 14 hex it does not
  know, reads `MMSN` as the taker's and `MM` + 16 hex (the Python maker, the
  137 IPO asks) as FOREIGN — checked in `healer.go` and against the live index
  before switching it on. Result: every old order gone (0 under 1,000), IPO
  asks 137 and snt-1 untouched, AFFC.TEST 8,309 / 7,435 / 7,402 decaying.
  ⚠ At 40 s four sides read 7–8 (post-first: new rungs land before the old
  cancel). **Settled by 21:58Z: three counts 20 s apart — 170 books, every
  side 3–6, none above 6, 0 duplicate prices, 0 refusals, the order count
  breathing 1,494–1,560 as ladders re-space.** The shape George knows, with
  the lifecycle holding.

**Decision (George, 26-08):** the TEST maker runs with the boot heal ON —
scoped by the `MMGO` prefix, it clears its own book on every restart. Never
with the prefix unset.

### ✎ 23:00–22:17Z — the resize comes back: rank drift on the old shape, by eye and by arithmetic

- George, three books on the old-shape run: **BENG.TEST rank 2 holding
  2,301** (a rank-2 draw is 5,400–9,000), **RAVE.TEST rank 5 holding 7,667**
  (a rank-1/2 size). "There is something fundamentally wrong with the way
  we're working it out." Per side ≤ 6 and 0 duplicates held — the LIFECYCLE
  was right; the SIZES were stale by rank. That is rank drift, the 21-08
  finding, back the moment the resize pass came out — and Python has it too
  (its 20-08 note: "the ladder sizes are stale by design"); one rung hid it.
- ✂ **The resize pass RETURNS** — Go PR #22 reverts `94a21b5` (only that
  commit; the inbound-leg fix `86ec89e` stands). Test build
  `test/old-ladder-shape-resize` (old shape + resize, NEVER merge) deployed
  22:14Z as `CFG-0051-GO-OLDSHAPE`, `go-run14`, the heal clearing 2,980
  (the old book plus its in-flight replaces).
- ⭐ **Measured, every rung against its rank's ±25% band (10,000 × 0.72ⁱ):**
  22:15:53Z 1,547 orders, 170 books, 3–6 a side, 0 duplicates, **0 rungs
  carrying another rank's size**, 10 outside their own band (replaces in
  flight); 22:16:53Z 1,562 orders, **0 another-rank, 2 outside own band**.
  BENG.TEST 12,469 / 8,465 / 4,491 / 3,078 / 3,317 · RAVE.TEST 9,842 / 5,752 /
  5,365 / 4,528 / 2,095 / 1,476.
- What remains is **N65 only**: BENG's 3,078 / 3,317 are both inside their
  bands and inverted by the independent per-rung draw (~6% of adjacent
  pairs). `feat/monotonic-ladder` (parked 21-08) removes it; both engines.

**Decisions (George, 26-08 evening):** the resize pass is the behaviour
after all — the day's "copy Python" ruling is narrowed to the inbound leg,
where Python was right and Go was dropping acks. Go PR #21 (the boot line
that described "no resize pass") is superseded and closed.
