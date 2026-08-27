---
description: "The night the Go maker's ladder was found and fixed: E51 ported, the inbound leg's drops, the resize pass back, and tZERO's order-rate limit measured and paced"
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

### ✎ 22:19Z — the fast-dwell test reproduces the accumulation. This is the real defect.

George asked for a faster cycle so re-spaces are watchable. Test build
`test/old-ladder-shape-resize-fastdwell` (dwell 3–6 s in every non-live
state; NEVER merge) deployed as `CFG-0052-GO-FASTDWELL`, `go-run15`.

⭐⭐ **With a new version every 3–6 s the book over-fills, on the build that
has the inbound-leg fix AND the resize:**

| time | resting | wanted | max/side | dup prices | rungs at another rank's size |
|---|---|---|---|---|---|
| +40 s | 1,886 | 1,536 | **11** | 5 | 440 |
| +70 s | 1,678 | | 9 | 0 | 203 |
| +2–3 min | 1,686 → 1,773 → 1,769 | ~1,530 | 8–11 | 0–6 | ~250 |

A steady FLOAT of ~15% extra orders and ~14% of rungs mid-move — not a
climb, but the ">6 a side" and "wrong-size rung" shapes George saw on
20/21-08, reproduced on demand.

**Mechanism (from the code, both engines):** a version's replaces and
cancels are still in flight when the next diff runs. An in-flight order is
neither kept nor movable (one-in-flight), so the new rungs POST beside it
(post-first, N12); the extra is cancelled only when its ack lands and the
NEXT diff sees it. The float is cadence × in-flight time × books, and the
converger's 128-instruction budget per 0.25 s pass lengthens the in-flight
time when 170 books re-space together. ⚠ LIVE games redraw every 500 ms
(George 08-11) — faster than this test.

**So the inbound drops (26-08c) were real and are fixed, but they were not
the whole cause.** The whole cause is that quote versions are allowed to
OVERLAP on a book. The fix direction: a book whose last instructions are
still in flight (sync state Synchronizing) does not publish a new version —
versions never overlap, the resting book is always exactly one ladder. Both
engines; Python at one rung simply had almost nothing in flight.

⚠ Not built tonight. The test maker stays on the fast dwell for George to
watch, or goes back to the normal dwell — his call.

---

# Part 3 — "you build it now": the venue's order rate was the cause all along

> **Refs:** Go PR #23 (`feat/no-overlapping-versions`, four commits) · #22 ·
> test builds `test/fastdwell-nooverlap` (NEVER merge) · journals
> `go-run12`…`go-run20` on `inplay-market-maker-go`.

## What we did

George, 23:30, on the fast-dwell run: asks with no bid beside them, sides
of 7–9, "this would work fine on the Python one — it's not identical". And
the side note that mattered: **90 games at the weekend**.

1. **Built the no-overlap rule** (`quotes.Cycle` `venueBusy`, dictionary row
   `VenueSyncHoldMaxS`): a book whose orders are in flight holds its next
   version. Deployed on the fast dwell: **it did not fix it** — the hold cap
   fired 354 times in 2½ min. Books were "in flight" for more than 5 s.
2. **Measured instead of reasoning.** The engine ticks at 2/s and its inbound
   queue was empty (24 of 46,821 at stop) — the acks were not late in the
   engine. The gateway showed **245 orders PENDING_NEW** at one instant —
   sent, not yet answered by tZERO — churning, none stale. Then the journal:
   **"Exceeds Max Order Rate" — 6,005 new orders and 7,619 cancels/replaces
   refused in 2½ minutes, 29% of everything sent.** In every burst second
   the venue accepted exactly 100–101 new orders and refused the rest (358,
   450, 415…). Every boot blew it too: standing 170 books fires ~1,500
   instructions in 3 s, a third of the opening ladder was refused, and the
   reject backoff then sat on those prices — the E51 run had 10% rejects,
   the old-shape run 6%, ALL at boot; the books healed over the next passes,
   which is why they looked right after a minute.
3. ⭐ **This is the whole picture, and it is one cause with three faces.** A
   refused cancel is an order that keeps resting (the extra rungs). A
   refused replace is an order stuck at its old price and size (the
   wrong-rank rungs). A refused post is a missing rung (asks with no bid).
   Neither engine had an outbound limiter: the converger budget is 512/s,
   the gateway's governor 5,000/s, and the dictionary's
   `VenueMessageRateLimit` had sat 🔴 "T2 — ask tZERO" since July. Python at
   one rung and a 20–40 s dwell never approached it.
4. **Built the pacer** (`QueuedTransport.SetRateLimit`): order messages
   (new/cancel/replace) capped in any one-second window on the one writer
   every order crosses; the heartbeat and kill switch take a priority lane —
   never paced, never behind an order (a paced queue 1,500 deep is 15 s, and
   a heartbeat that waited that long is a dead-man sweep). Paced at 100:
   rejects 29% → 5%, every one in a second at exactly 100 — the venue's
   window is not ours. At 80: 1.4%, cancels weighing more than replaces. **At
   60: zero** over 23,619 acks.
5. **Derived the converger budget from the wire:** `ConvergeMaxInstructionsPerTick`
   128 → 15 (60/s × 0.25 s), pinned by Validate. At 128 the transport queue
   was ~15 s deep during a re-space wave, every pending "in flight" for the
   queue wait, and a 30 s hold cap fired 1,338 times in four minutes. With
   the budget at the wire's rate the backlog lives at the STAGE, where a
   stale version is superseded by the next instead of sent late.
   `VenueSyncHoldMaxS` 5 → 30 s.

## The result (23:56–00:00Z, fast dwell 3–6 s, old shape 3–6 × 10,000)

| sample | resting | wanted | per side | dups | rungs mid-move | rejects |
|---|---|---|---|---|---|---|
| +1 min (boot queue draining) | 1,667 | ~1,530 | 3–9 | 0 | 162 | |
| +2 min → +4 min, every sample | 1,501–1,566 | ~1,530 | **3–6, none above** | **0** | **1–3** | **0 of 23,619** |

Hold caps fired only in the boot minute. This is the shape George knows,
at four times the normal cadence, holding.

## What we learned

- ⭐⭐ **The venue's order rate is the ceiling everything sits under.** tZERO
  refuses past roughly 60–100 messages/s per session (rule not yet known:
  100 exactly in burst seconds; still refusing at a paced 80; clean at 60;
  cancels weigh more than replaces). This was open since July as T2 and
  nobody had the number. Tonight's journals have it.
- ⭐ **Every one of tonight's symptoms was downstream of it.** The inbound
  drops (26-08c) were real and are fixed; the resize (26-08d) is right; the
  no-overlap hold is right; none of them could hold a book clean while a
  third of the cancels were being refused.
- ⭐ **"Identical to Python" was true of the code and false of the load.**
  Same reconciler, same converger, same state machine — and a Go maker at
  six rungs on 170 books sends 6–10× what a Python maker at one rung did.
  The Python maker will meet the same wall the moment it runs depth at
  game cadence.
- ⚠ **The weekend (George's side note, and the real finding):** 90 games.
  At ~60 messages/s, a one-rung book costs ~2 messages per update; 80 live
  books redrawing every 500 ms need ~320/s — five times the venue's limit —
  before any depth. The plan's activity-tiered cadence is not a nice-to-have;
  it is the only way the maker fits. And T2 must be asked WITH these numbers.
- ⚠ Rate-limit rejects go through the reject backoff (2, 4, 8 … 60 s per
  price), which is the wrong tool for a rate limit: it makes a refused
  cancel rest longer. With pacing there are none; without it the backoff
  amplifies the damage.

## Decisions (George, 26-08 → 27-08)

- ✅ **The wire is paced to the venue's order rate** — `VenueMessageRateLimit`
  60 🟡 measured (was 🔴 T2), on the one writer; heartbeat and kill switch
  never paced.
- ✅ **The converger budget is derived**: rate × interval, pinned by Validate.
- ✅ **No overlapping versions**, hold cap 30 s.
- ✅ Go PR #22 (resize back) + #23 (the four commits) are the fix set, on
  top of #19 + #20.

## Next

1. Merge #22 then #23 into `feat/phase-3-ingestion`; close #21.
2. **Ask tZERO (T2) with the numbers**: 100/101 accepted in burst seconds,
   refusals at a paced 80 (cancels), clean at 60. What is the rule?
3. **The Python maker needs the same pacer** before it quotes depth at game
   cadence — it has the same 512/s budget and no limiter.
4. **Capacity plan for the weekend**: 60 msg/s ÷ (2 × rungs) books per
   second. Activity tiers, or fewer live books, or one rung — arithmetic,
   not judgement.
5. The test maker stays on the fast-dwell test build for George to watch
   (`CFG-0057-GO-PACED60`, `go-run20`). To return to a normal build: stop,
   restore `mm-go.bak-154cf847-e51` (E51 shape) or build #22+#23 on the
   phase branch, bump the version, fresh journal; the heal clears the book.

### ✎ 27-08 10:25Z — the UEAR, and a correction to Part 3

- **tZERO's MaxOrdRate is an ACCOUNT setting we can write ourselves.** The
  gateway's `POST /buying-power` sends a 35=UEAR (tag 8935 `maxOrdRate`,
  IPLY default **100/s**; tag 8936 `maxDupOrdRate`, default **20/s** per
  symbol-side for same-shaped orders — why a paced 80 still lost cancels).
  Sent on the test account 2559580864: `maxOrdRate 2000, maxDupOrdRate 200`
  → **`UEARa`** (accepted). No read-back exists; the proof is the next run.
- **Test build paced at 400/s** (`test/fastdwell-paced400`, `CFG-0058`,
  `go-run21`): 92,670 acks, **zero rate rejects**, busiest second 902.
  Remaining: 1.7% `UNKNOWN ORDER` on cancels (an orig already replaced —
  gone-retired, harmless) and transient double posts at 6× normal cadence
  (1–7 duplicate prices per sample, none persisting 12 s; sides of 7–8 on a
  handful of books at any instant — the post-first race).
- ⚠ **CORRECTION to Part 3.** The 20/21-08 journals (`go-run01`…`11`) carry
  **no "Exceeds Max Order Rate" at all.** Those runs were on the PRODUCTION
  account 1797733477, which evidently already carries a raised MaxOrdRate
  (who set it, when — ask Hasan; there is no read-back). Their rejects were
  **duplicate ClOrdIDs** (run02: 32% — the unbumped salt), **NOT_CANCELABLE**
  (run05: 683 — cancels refused = extra rungs) and FAILSRISK. So the wrong
  ladder of 20/21-08 was rank drift + dropped acks + those rejects. The rate
  limit was the TEST account's IPLY default, hit for the first time on 26-08.
  "The cause all along" in Part 3 overreached by one night; the pacer, the
  derived budget and the no-overlap rule stand on their own evidence.

**Next:** UEAR on the production account on George's word (2000/200), then
read production's effective rate the only way possible — a paced run and
the reject count — and set `VenueMessageRateLimit` from that.

### ✎ 27-08 12:00–12:10Z — the panel's twin cards are frozen; the venue book is right

George: "the Bears has sat there for ages — rank 2 bigger than rank 1, no
third bid, three asks." Measured at the venue at the same minute: Bears
4 bids / 4 asks (+1 pending each side), every rung in band; Bills 11,361 /
6,986 / 6,391 / 3,446 / 2,236 / 1,943, monotone — the card's 3,922 / 8,384
never existed at the venue. Across four samples 5 s apart, sides with rungs
from more than one grid: 6 / 11 / 0 / 5 of 340, none for 15 s. Uneven
sides (a re-space in flight): mean 1.2 books of 170, none over 4 s.

⚠ **The panel's book card polls `/api/market/book?symbol=` every 5 s and
the twins' depth does not reach it** — the "dot is a token" gotcha from the
26-08 census note (`market.book.*` does not match `IPTCBEAR.TEST`). The
card keeps its last successful draw (the yellow dot). A page reload shows
the venue's current book, then it freezes again. Panel/proxy fix, not the
maker's. Both gateways' `/quotes` stores carry honest timestamps: the
touch order is KEPT under rest-until-gone, so the best bid/offer genuinely
does not move.

Residual at 400/s: 1,535 cancels (13% of cancels) answered "UNKNOWN
ORDER" — already gone at the venue, gone-retired by the record. A
replace-lineage race under load; invisible at the normal cadence.
