---
description: "Edwin's E51 parameter set and George's 26-08 rung range ported to the Go maker, with the fd193a4 corpora kept valid through a pinned dictionary"
---

# 2026-08-26-b — The Go maker carries E51, and the corpora keep the pin

> **Who:** AI session (the Go side), resumed from the 21-08 handover.
> **Type:** build, local only. Nothing deployed. No VM touched.
> **Refs:** Go PR `feat/e51-parameters` → `feat/phase-3-ingestion` ·
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
