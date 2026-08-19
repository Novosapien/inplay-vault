---
description: "CA2 follow-on: George's cancels-through-refusal ruling and the examined-books cap, plus the LIVE-class starvation gap the cap exposed"
---

# 2026-08-15 — CA2b: finishing the refusal path (MED-3 + MED-4)

> **Component:** [[market-maker/market-maker]] · **Branch:**
> `fix-set/ca2b-refusal-path` · **PR:**
> [inplay-market-maker #37](https://github.com/Novosapien/inplay-market-maker/pull/37)
> (base `fix-set/ca2-marketable-guard` — stacked on #34) · **Nothing
> deployed (R11).** Narrative for the guard itself:
> [[market-maker/sessions/2026-08-14-ca2-marketable-guard]].

## What we did

One `sync.py` pass covering both halves of R-Q09's refusal path — the two
items deliberately left out of #34.

1. **George's MED-3 ruling: a refused book still sends its CANCELS.**
2. **MED-4's examined-books cap**, plus the fairness fix the cap makes
   mandatory.

994 tests (986 + 8), ruff and mypy clean, replay equality green.

## What we learned

**Risk reduction must never wait on risk addition.** The case that forced
George's ruling is a falling market: our resting bid is stale and due for
cancel, and its replacement prices through the live ask. The guard refuses
the replacement — correctly — and under #34's whole-batch rule the
**stale bid stayed resting**. That is the order most likely to be hit in a
falling market, and it was being held on the venue because the guard
disliked its successor. The batch is no longer all-or-nothing: submits and
replaces wait, cancels go.

**The cancels-only subset does not weaken `[atomic-book]`, because that
invariant has two halves and neither is reachable.** Worth writing down,
because "we are sending part of a book" reads alarming until the halves
are named:

- The *half-posted ladder* half is about **adding** one side without the
  other. A cancel adds nothing; exposure only ever shrinks during a
  refusal.
- The *ClOrdID collision* half is about submit ids minting **by position**
  in the unmet list, so a re-diff after a partial send collides. A
  cancel's id mints from the **original order's id**
  (`CXL-{client_order_id}`), never from a position — so it is stable
  across re-diffs, and re-minting one would produce the *identical* id
  rather than a colliding one.

**And the cancels cannot storm**, because `register_cancel` moves the
order to `PENDING_CANCEL` while the reconciler's `_ACTIONABLE` is
`{ACTIVE, PARTIALLY_FILLED}` — the re-diff ignores an order already
leaving. They go exactly once per set. All three properties already
existed; the ruling only needed them pointed at.

**A budget that measures the wrong thing bounds nothing.** The converger's
instruction budget cannot bound a *refused* book: the guard answers AFTER
the diff, and the book then sends nothing — so it costs a whole
`reconcile_book` and spends no budget at all. A phantom touch holding many
books therefore re-diffs all of them every pass, for ever. The fix is a
second bound on a different unit: books EXAMINED, not instructions sent.

**The cap creates a starvation bug unless the rotation changes with it.**
This is the part worth remembering. The round-robin advanced only on
**served** books. Add a cap and a wall of persistent refusers at the head
of the rotation is re-examined every pass, hits the cap, breaks — and the
books behind them are never reached *at all*. Being refused now counts as
progress through the rotation, even though it is not progress on the book.

**The gap nobody had named: the LIVE class had no rotation whatsoever.**
The tests found it, not the review. The general lesson is the useful part:

> A work list that drains itself needs no fairness mechanism. The moment
> an item can stay on the list without being completed, it does.

Served books leave `_targets`, so a static alphabetical order over LIVE
books drained itself and fairness was free. A *refused* book stays — so
the same starvation applied to LIVE, and the fixture books are LIVE, which
is exactly why the first draft's tests failed. LIVE now rotates on its own
cursor.

## What went wrong / got stuck

**The first cancels tests asserted nothing.** They passed a refusal
through the converger and expected cancels, and got an empty list — the
reconciler prefers **REPLACE** over cancel-plus-submit, so a book that
merely reprices yields no cancels at all. A probe across six probability
pairs produced 16 replaces and 2 submits every time and **zero cancels**.
Cancels only appear for orders *surplus* to the wanted prices, so the
tests now manufacture that surplus (`rest_surplus_orders`) — which is also
the honest shape of the falling-market case: stale bids resting under a
book that no longer wants them.

**A passing test is not a proving test.** Both starvation tests passed on
the first green run, and one of them passed for the wrong reason — the
book that moved the cursor was being *served*, not refused, so it would
have passed against the old code too. A mutation check (revert the
refusal-branch cursor increment, re-run) is what exposed it. The test now
makes every book refuse, so the cursor can only move through the refusal
path, and **both** starvation tests fail under the mutation.

**The new worktree had no venv** — `uv sync --group dev` rebuilds it.
Worth knowing for the next worktree-per-stream chunk.

## Decisions made

Mirrored into [[market-maker/decisions]] as **2026-08-15b**:

- A refused book still sends its cancels (George's MED-3 ruling), with the
  three safety properties recorded.
- ✎ This **amends** the 14-08f line "a refusal costs no budget" — a
  refusal that carries cancels now spends budget for them.
- A converger pass is bounded twice: instructions SENT and books
  EXAMINED. Budgeted passes only.
- Being refused counts as progress through the rotation; the LIVE class
  now rotates too.

## Questions opened / closed

- ✅ **CLOSED — MED-3**: George ruled cancels-through. Built.
- ✅ **CLOSED — MED-4**: built, with the fairness fix it requires.
- 🟡 **OPEN — the second dictionary row.** `marketable_stall_passes` was
  an explicitly granted one-row exception; I took the same latitude for
  `converge_max_books_examined_per_pass` because it is a real throughput
  lever and belongs beside `converge_max_instructions_per_tick`. Flagged
  to the lead — a module constant instead is a one-line change.
- 🟡 **STILL OPEN — N41's automatic exit.** Unchanged by this session.
  Cancels-through *reduces* the phantom's cost (a stalled book at least
  sheds its stale orders now) but the submits still wait indefinitely.

## Addendum — the Phase-3 review found the SAME bug in a third class

The review reproduced a HIGH in the examined cap: **it starved the
converger through suspends**, the one class with no cursor.

Suspends run FIRST (`[converge-priority]`), they re-stage on every
`BookSuspended` cycle, and a suspend with nothing left to cancel yields
**zero instructions**. So a portfolio with ~100 suspended books spent the
whole cap on them, at the same alphabetical break point, every pass, and
**no live book ever converged** — not late, never.

**This is the third time the same shape appeared in one chunk.** `rest`
had a rotation. `live` did not, and I found that one. `suspends` cannot
have one, and neither the reviewer nor I checked it until the cap made it
reachable. The lesson written in this vault two commits earlier is
precisely the one that predicts it:

> A work list that drains itself needs no fairness mechanism. The moment
> an item can stay on the list without being completed, it does.

A suspend re-stages every cycle, so it *behaves* like it stays, even
though each individual target is deleted. Writing the lesson down was not
enough to make me apply it to the next class along — worth remembering
about lessons in general.

**Why exemption rather than the alternatives.** A cursor cannot fix this
class: rotating risk reduction spreads the delay around instead of
removing it. And of the two shapes the reviewer offered, I rejected
"charge only instruction-yielding targets" — the cost the cap exists to
bound is the **diff**, which is already paid by the time the yield is
known, and a book whose target happens to match the venue diffs in full
and yields nothing. Charging on output would under-bound exactly the work
the cap is meant to bound.

Exempting suspends is right on its own terms: risk reduction is never
rationed here (the guard already refuses to hold back a cancels-only
batch), and a suspend is self-draining — it converges and is deleted
unconditionally, so it can never acquire the stay-dirty-without-progress
shape the cap was written for.

⚠ **Recorded, not fixed:** a zero-instruction suspend still costs one
`_suppression()` call, and that is a scan of the **whole portfolio's**
reject table (`backoff.py:113`). Not this cap's to fix — it is on the
per-event-scan list given to the lead, where it is the strongest MM hit.

Also in this pass: **LOW-2** (the `sec in rest/live` membership tests read
frozensets now — consulted once per security on a 4 Hz walk, and `in` on a
list is a scan) and **LOW-4** (the `[suspend-exempt]` note).

Three new tests, all mutation-verified. ⚠ I could not run the reviewer's
own `repro.py` — it lives in their session's scratchpad, not mine — so the
evidence here is my own reproduction of the same shape at the fixture's
scale, failing under mutation with the identical symptom.

The reviewer also verified clean: cancels-exactly-once, the CXL-id
stability argument, and the compat-flush exemption; and judged the
refusal-cancel budget exhaustion self-limiting.

Gates after this pass: **997 tests** (994 + 3), ruff and mypy clean,
replay equality green.

## Next

**Review pass on #37**, then it joins the merge train behind #34. The
merge order is the lead's: #34 first, then #37.
