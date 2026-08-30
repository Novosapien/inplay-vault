---
description: "Edwin's one-sided-book report traced to a 2h45m self-crossed Tar Heels book, and to George's cancel-first ordering rules that never left learnings.md"
---

# 2026-08-29b: the Tar Heels book crossed itself for 2h45m — and we already had the fix written down

> **Who:** George + Claude
> **Type:** live investigation (read-only) + one ruling
> **Refs:** [[market-maker/sessions/2026-08-29-ncaa-saturday-cadence-check]]
> (the cadence check that found it) · `R-Q09` `N12` `N41` `N75` ·
> `R-L03` · [[market-maker/learnings]] · `src/mm/venue/sync.py`
> `src/mm/venue/reconciler.py`
> **Trigger:** Edwin reported that some books showed asks and no bids.
> He named the North Carolina Tar Heels.

## What we did

Traced Edwin's report to a specific book, a specific mechanism and a
specific decision. Read-only throughout — `journalctl`, the gateway ops
endpoint, a 400 MB journal tail, and the repo. Nothing was changed and
nothing was deployed.

## What we learned

### ⭐ `IPTCNCTH` was self-crossed for 2 h 45 min, and recovered alone

| | |
|---|---|
| Window | **16:07Z → 18:52Z**, 29-08 |
| Ask side | **froze at 40.26 at 16:07Z** and never moved again |
| Bid side | kept repricing up, 40.30 → 40.63 |
| Book state | **bid above ask** for the whole window |
| Levels | asks grew **3 → 17**; bids stayed 4–7 |
| Real trading | 40.43–40.72 throughout — **$0.20–$0.45 above our stuck ask** |
| Recovery | **automatic.** The blocking touch moved. No hotfix, no operator |

`IPTCHFRG`, the other book in the same game, had the identical fault.
**Only live-game books are exposed** — they are the only ones whose
price moves fast enough to run into a resting third-party touch.

⚠ **The lopsided ask wall priced below the bids is what Edwin saw.**
"Asks and no bids" is the display of a crossed book whose offer side
is frozen and accumulating.

### The mechanism, end to end

1. A third-party bid rested at **40.40**.
2. Our target ask moved below it. The R-Q09 marketable guard refused —
   correctly: we price off our own valuation and never off the book, so
   without the guard every repost sweeps the touch (**$50,366 on
   09-08**).
3. ⚠ **The refusal holds back the WHOLE BOOK, not the offending side.**
   The guard's own alarm says it: *"no submit or replace has gone out
   for this book since"*. `MARKETABLE_GUARD_STALLED` fired **9 times**
   between 16:53Z and 18:52Z.
4. Both sides stopped updating. The stale orders stayed resting.
5. It cleared only when the third party's bid moved.

📝 **`[cancels-through]` did not save it.** George's 15-08 MED-3 ruling —
a refused book still sends its cancels — IS in the running tree. It did
not help, because the reconciler moves a stale order with a **replace**,
and the guard holds replaces. Cancels-through covers cancels, not the
cancel-half of a held replace.

### ⭐ THE REAL FINDING — we designed the fix in July and never shipped it

George's memory ("we decided cancel-first because the book looked
wrong") is **correct**, and the note exists. It is in
[[market-maker/learnings]], not [[market-maker/decisions]]:

> **Publish is a reconciler, not a send (George's push, refining the
> trilemma).** … executed under ordering rules: retreating side first
> (retreat can never cross), **cancels before creates at overlapping
> prices**, advancing side deepest-first with top-of-book last,
> **micro-barrier only on the specific orders an advance would cross**.

⚠ **It never left `learnings.md`.** It was never mirrored into
`decisions.md`, so **N12's flat post-first was never superseded**, and
`requirements.md` **R-L03** then codified the flat version — *"submits,
then replaces, then cancels"*, sourced to N12, ✅ test-backed. The
requirement locked in the design George had argued against.

The built reconciler is the flat version, one line
(`venue/reconciler.py:173`):

    return tuple(submits) + tuple(replaces) + tuple(cancels)

No retreating-side-first. No cancels-before-creates. No micro-barrier.

⭐ **And the last clause is exactly yesterday's fix.** *"Micro-barrier
only on the specific orders an advance would cross"* = refuse the
crossing ORDER, not the BOOK. The guard was built at book granularity
instead, for reasons that are real (`[atomic-book]`) but that the
micro-barrier design predates and answers.

### 📝 Edwin's standard vs Edwin's spoken ruling — both exist, and they conflict

- **Written:** PTS-001 §6.13.1 — *"locked or crossed markets SHALL NOT
  be published"* AND *"executable two-sided quotations SHALL be
  maintained unless trading is halted or suspended"*. Also §6.12
  (Validation), §7.2, §6.9.1.
- **Spoken (23-07, in `decisions.md`):** *"new orders are faster than
  cancels… on the first iteration, if we have to cross in order to make
  the adjustment in price, I don't care."* — **No cancel-first-wait
  gap**, confirmed by George the same day.

By the working guide's ground rule the spoken decision **outranks** the
standard, so post-first is governing and it is HIS. **What his tolerance
does not cover is the word `momentary`.** It licenses a price
adjustment, not a 2 h 45 min guard-frozen book. That gap is ours and it
was never recorded.

## What went wrong / got stuck

- ⚠ **I twice told George the wrong thing and corrected both.** First
  that the fix was easy ("refuse the order, not the book") — the code
  says that placement is **forced**, because submit ClOrdIDs mint BY
  POSITION and a partial send collides with ids the venue holds
  (`[atomic-book]`, "caught by test, a real collision"). Second that the
  06-08c conflict had "no defence" — the post-first design itself is
  Edwin's own call, so that was overstated.
- The gateway ops endpoint (`GET /orders/mm`) **has diverged from the
  engine**. All 9 `IPTCNCTH` orders it returned had no acknowledgement
  in 2 hours, at prices $3 from the engine's, while the engine sent
  60,891 acks for that book. `MM_BOOT_HEAL=on` reads that endpoint.
  Filed inside `N75`.
- The 06-08c conflict (tZERO's wash-trade blocking REJECTS self-crosses,
  which undermines post-first at the venue) was flagged with "the
  reconciler has a change coming either way". **The taker got its fix
  (wash guard, MM PR #29). The maker never did.**

## Decisions made *(mirrored into [[market-maker/decisions]])*

- ✅ **George, 30-08: PROMOTE the ordering rules from `learnings.md` to
  a decision.** They become the TARGET design for the reconciler,
  superseding N12's flat post-first. `R-L03` changes through the
  requirements addendum, never silently. **Not built, not scheduled** —
  R11 stands, and the granularity question (`N75`) is answered first.

## Questions opened / closed *(mirrored into [[market-maker/open-questions]])*

- **`N75` opened** — the guard refuses at BOOK granularity; George's
  micro-barrier refuses at ORDER granularity. Which, at what cost, and
  what does `[atomic-book]`'s positional ClOrdID minting really force?

## Next

1. **Answer `N75`** — cost the two options (cheap: extend
   `[cancels-through]` to the cancel-half of a held replace; deep: order
   granularity, which means non-positional ClOrdID minting and a fresh
   replay-equality proof).
2. Then return to the cadence work: **re-measure at peak** and rule
   `N74` (the publisher's hardcoded 1 s tick).
3. Ask Edwin nothing yet — the message George has covers it.
