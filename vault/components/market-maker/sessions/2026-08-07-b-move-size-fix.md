# 2026-08-07-b — the reconciler move-size fix: built, deployed, observed live

> **Who:** Claude (autonomous session from the 07-08 handover; the fix
> itself was George's explicit ruling — option b on the ladder trace)
> **Type:** build + deploy + live observation
> **Refs:** decisions `2026-08-07h` · MM PR #8 (merged, main `e0f2e45`) ·
> the ladder-shape trace on [[market-maker/build/venue|Venue]] ·
> engine on the VM (journal `/var/lib/mm/supervised4`, CFG-0003)

## What we did

1. **The move-size fix, test-first (MM PR #8, merged):** the
   reconciler's move pass now sends `cum_qty + level.quantity` — a
   moved order adopts the size drawn for its new rank — instead of
   `cum_qty + leaves_qty` (the old remainder). The gateway's
   `quantity > CumQty` guard holds by construction (a drawn level is
   ≥ 1). Three new tests: the rewritten move test plus the trace's two
   rotation fixtures (one-tick drift up and down each produce ONE
   replace at the new rank's draw, ladder non-increasing). The
   fixtures failed on the old code exactly as the trace predicted.
   576 tests · ruff · mypy-strict green.
2. **The record:** decisions `07-08h` (✂ supersession of N10's
   "carries the remainder" wording — moves only; kept-order
   rest-until-gone stands) · the E17 row narrowed (move-scramble
   fixed; kept-order generations + no-top-ups remain) · build/venue
   and build/next updated.
3. **Redeploy to the VM** (bundle `mm-e0f2e45` via `inplay-mm-deploy`):
   SIGTERM to the old engine (dead-man swept its book as designed) ·
   fresh journal `/var/lib/mm/supervised4` + `MM_CONFIG_VERSION=CFG-0003`
   (the now-mandatory bump; `run_supervised4.sh`) · boot clean —
   58 instructions, six books two-sided at Edwin's prices, 346 accepts,
   **0 rejects**. The poker restarted (60-minute loop) to make the
   books drift.
4. **The live observation (under active poker fire, two 120 s windows,
   ~2,200 side-observations):** visible ladder monotone **32–36%** —
   up from the trace's **5.8%** before the fix (target ceiling 84%).
   Excluding the inside rank — where the poker's nibbles bite —
   **55.6%**. The snapshots read as clean decaying profiles; the
   remaining breaks sit at bitten inside levels and kept-generation
   mixes, i.e. the E17 remnant, not the move pass. No stale-size
   teleports observed.

## What we learned

- **A restart is a sweep-and-repost, and the replayed record would lie
  about it.** The dead-man sweeps on SIGTERM while the engine is down,
  so those cancels never journal — a restart on the OLD journal would
  replay phantom ACTIVE orders and the reconciler would stand no book
  (the parked boot-reconcile gap, met in practice). Fresh journal +
  CFG bump per restart is the discipline until the healer exists.
- **The LmtPerc reference now works FOR us:** with our own books the
  recent snapshot, a full repost at the same prices sails through —
  0 rejects on re-boot, against 1,511 on the first-ever run.
- `NOT_CANCELABLE` (145) and `REQUEST_IN_FLIGHT` (16) texts in the new
  journal are cancel-races against poker fills — expected churn, same
  family the reject-backoff build will quiet.

## Decisions made

- None new. Executed `07-08h` (ruled last session); its ✂ note and row
  updates recorded this session.

## Questions opened/closed

- E17 narrowed (see the row): the move-pass half of the book scramble
  is fixed and live; what remains for Edwin is kept-order generations
  and partial fills never topped up.

## Next

1. **The reject-backoff build** (TOP on [[market-maker/build/next|next]]
   — three live shapes: LmtPerc, duplicate-id, no-reference).
2. The Hasan message (ghost cleanup · LmtPerc reference · user-side
   wash · the infra file) · Rob's pending wash/MPID answer · the Edwin
   round (E17 remnant + E31 ladder shape).
3. systemd unit + N15 jitter recorder if the engine stays up · N31
   group commit (fsync measured ~579 events/s).
