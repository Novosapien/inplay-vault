# 2026-08-07 — THE LIVE-VENUE DAY: first real quotes, six books at Edwin's prices

> **Who:** George + Claude (George directing throughout — "nobody's
> using production"; probes, seeding and the walk all his calls)
> **Type:** live venue operations + build-on-findings, one long chat
> session spanning 06-08d's continuation through this note
> **Refs:** decisions `2026-08-07` b–g · MM PRs #6, #7 (merged) · the
> transfer ledger · Hasan's trading-ops guide (filed) · the
> ladder-shape trace (agent run, findings on
> [[market-maker/build/venue|Venue]]). Engine + poker running on the
> VM at session close (journal `/var/lib/mm/supervised3`, CFG-0002).

## What we did

1. **Wash-trade verified by real self-cross** (MM account, wash OFF):
   both sides EXECUTED — self-crosses PRINT. User-account half still
   needs Hasan's pilot accounts.
2. **Two venue facts from probe one:** side-2 sells need inventory
   (side-5 shorts work from flat) · `LmtPerc: No price available` on
   empty books (BILL's disease — gates the 163 empty books).
3. **Seeded 100k × 7 tickers ourselves** via position-transfer (Hasan's
   ops guide made it self-serve): all UPTa, basis at Edwin's prices,
   ledger in `reference/position-transfer-ledger.md`.
4. **Supervised run 1:** 64 orders rested (passive halves only) — the
   stale test quotes made every crossing half "aggressive" under
   LmtPerc (3%/90% bands, delayed-snapshot reference — all decoded
   from full reject texts). The engine's reject-repost loop observed
   (~16 msg/s). The dead-man drill happened LIVE: SIGTERM → swept in
   4 s, book clean.
5. **The book walk:** ate every stale quote in the way (at their own
   prices — 0% through is always legal), anchored all six books at
   Edwin's prices with the never-empty rule; the frozen reference's
   refresh delay handled by patient retries.
6. **Two live crashes, two merged fixes:** a real fill with NO payload
   ids killed the engine → PR #6 (subject fallback for fills; POISON
   drain — untranslatable inbound counted and skipped, deliberate
   halts stay fatal) · a journal wipe re-minted identical ClOrdIDs
   into tZERO's session memory → duplicate-reject deadlock → PR #7
   (`MM_CONFIG_VERSION`; never wipe a journal against a session that
   remembers).
7. **⭐ ALL SIX BOOKS LIVE, TWO-SIDED, AT EDWIN'S SHEET PRICES** —
   spreads straddling every target, 8–17k/level. The poker (v6:
   ~0.8 s nibbles of 1,000, biased streaks, self-cancelling misses)
   keeps the books visibly trading. Book seq >126k by session close.
8. **Rob (tZERO) intake:** MPIDs — IPLM (MM, driven by Account1) /
   IPLY (retail) / IPLP (future BD-prop = the SNT-1 slot). No engine
   change; his wash/MPID-interplay answer pending.
9. **The ladder-shape trace** (George: "the book shows no profile") —
   agent-run simulation on the real code. THE CAUSE: the reconciler's
   move pass carries the OLD order's quantity to the NEW price
   (95.7% of instructions carried stale sizes; visible ladder
   monotone 5.8% vs the target's 84%). Variation is innocent. Full
   findings on [[market-maker/build/venue|Venue]].

## What we learned

- **The venue teaches at order-one speed.** Five real lessons in one
  day (inventory-gated sells, empty-book lock, frozen references,
  no-id fills, id memory) — none visible from loopback.
- **The equality/robustness disciplines paid out live:** the dead-man
  swept exactly as drilled; the poison rule was designed the day it
  was needed.
- **The book the users see is not the book the engine intends** — the
  reconciler's size-carrying move scrambles the profile. George's
  "this looks wrong" instinct found a real, measurable defect.
- **pkill -f on a pattern that appears later in the same SSH command
  kills the session** — cost four SSH sessions before it stuck: stops
  and starts go in SEPARATE ssh invocations.

## Decisions *(the record: decisions.md 2026-08-07 b–g)*

- George: fire the probes now · seed ourselves · walk the books ·
  poker cadence/nibble tuning · **fix the reconciler move-size line
  NEXT SESSION** (option b — fresh drawn size on a move; re-words
  N10's "carries the remainder"; Edwin sees it in the round).
- Deferred: SR-sourced expected wins (Edwin's doc is the source for
  now) · the ghost cleanup + LmtPerc reference + user-side wash → the
  Hasan message.

## What's open / next

1. **The reconciler move-size fix** (George's ruling, next session):
   `quantity = cum_qty + level.quantity` in the move pass + tests +
   the N10 supersession note — then watch the live book hold its
   profile.
2. **The reject-backoff build** (three shapes seen live).
3. N31 group commit · systemd unit + N15 jitter recorder (if the
   engine stays up) · BILL + the 163 books await the LmtPerc answer.
4. The Hasan message (ghosts, LmtPerc, wash user-half, infra file) ·
   Rob's pending answer · the Edwin round (now + E17 lifecycle,
   E31 ladder shape incl. George's tree preference).
