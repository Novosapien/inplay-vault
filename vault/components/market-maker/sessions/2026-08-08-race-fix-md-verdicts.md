# 2026-08-08 — "the book doesn't look right": the double-post race, poker v7, and the MD verdicts

> **Who:** George + Claude (George: check the logs/replay · fix and
> deploy both · review impact on Hasan's service carefully)
> **Type:** live forensics → build → deploy → verify
> **Refs:** decisions `2026-08-08` · MM PR #9 (merged, `dfa87f9`) ·
> engine CFG-0004, journal `/var/lib/mm/supervised5` · poker v7 ·
> the MD evidence for the Hasan message

## What we did

1. **Journal forensics on George's "the book shows no profile":** built
   journal→open-order reconstruction and diffed it against the live
   `market.book` stream per book. Five books matched the engine's
   intent; the mismatches decomposed into three separate causes.
2. **⭐ Found and fixed the double-post race (MM PR #9):**
   `register_replace` kept PENDING_REPLACE at the OLD price, so the
   reconciler read the in-flight replace's destination as unmet and
   pass 3 submitted there too — proven at 57 ms resolution in the
   journal; 19 doubled levels stood across the six books (real
   exposure). Fix: `VenueOrder.pending_price` occupies the
   destination; checkpoint schema 2 → 3. Race fixtures fail on the old
   code; 582 tests, ruff, mypy green.
3. **Fixed the poker (v7):** v6 read `q["bid"]`/`q["ask"]` — fields
   that do not exist in the quote schema — and poked the static launch
   prices forever (COWB 99.7% miss; stray 1000-lots inside the
   spread). v7 aims from `market.book` tops.
4. **Reviewed Hasan's service before touching anything (George's
   caution — right):** the local Go checkout was BEHIND; on current
   main the one-sided `market.quote` is a documented partial-update
   contract (null = no change; COALESCE; `bestBidCleared` flags), and
   the Redis path merges. NOT a bug; nothing pushed. The deployed
   binary (08-07 12:16Z) already carries his 08-06 MD fixes.
5. **Proved a real MD-side issue for the Hasan message:** the JETS
   `market.book` was stale for ~5 min under our churn — the wire
   showed an ask at 45.44 while a journal-confirmed poker bid at 45.45
   rested unfilled (impossible on a real matching book). Not the
   crossed-book holdback (0 log hits). The depth feed is snapshot-driven
   + republish tick: a stalled venue snapshot stream freezes the
   published book while the republisher keeps re-emitting it.
6. **Deployed both fixes** (dead-man sweep on stop; fresh journal
   `supervised5`; CFG-0004 — the mandatory bump) and verified live:
   zero doubles after 30 min of churn · poker 100% fill on all six
   books (369/369) · **ladder monotone 69.7%** (5.8% original →
   32–36% after move-size alone → 69.7% now; 84% is the target
   ceiling — the rest is true E17: bites + kept generations).

## What we learned

- **The visible book had FOUR overlapping distortions** (move-size
  carry · double-posts · poker static-aim pollution · MD staleness).
  Only journal-vs-wire diffing separated them; watching the panel
  could not have.
- **A pure-function trace cannot catch in-flight races** — the
  double-post lived in the ~250 ms between register and ack, which the
  simulated venue settled instantly.
- **Check the deployed version AND the current source before
  diagnosing someone else's service** — the stale local checkout
  produced a wrong first diagnosis of the quote nulls; George's
  "review carefully" caught it.
- The crossed-pair test (a journal-confirmed resting order vs the
  published opposite side) is a clean, reusable proof of MD staleness.

## Decisions made

- Recorded in decisions `2026-08-08` (the race fix + deploy, poker v7,
  the two MD verdicts, the redeploy discipline restated).

## Questions opened/closed

- Nothing new for Edwin. The Hasan message gains two MD items: the
  book-staleness evidence (his design call how to gate/alert) and a
  heads-up that naive `market.quote` consumers see partial documents.

## Next

1. **The reject-backoff build** (unchanged TOP — 751 CANCEL_REJECTED
   in 30 min of poker churn is the same family).
2. The Hasan message (now: ghosts · LmtPerc reference · user-side wash
   · infra file · the two MD items) · Rob's pending answer · the Edwin
   round (E17 remnant + E31).
3. systemd unit + N15 jitter recorder · N31 group commit.
