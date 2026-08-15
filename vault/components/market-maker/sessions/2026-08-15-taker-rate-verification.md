---
description: "Live verification of the deployed 1 s LIVE taker rate: the rate lands, both review HIGHs measure mild, and one real finding — a book can spend its float before the soft cap engages"
---

# 2026-08-15 — verifying the taker's new LIVE rate against the logs

> **Who:** George + Claude · **Type:** live forensics, READ-ONLY (nothing
> published, changed or restarted on any machine)
> **Refs:** MM #40 (`main@7ca9d76`) · taker SNT-CFG-0023 / journal snt20 ·
> engine supervised32/CFG-0030 · build-deploy-log (#40 row + the new
> finding row) · taker requirements addendum 2026-08-15b · TT9 ·
> decisions 2026-08-15e (the ruling this verifies)

## What we did

George's ask after the deploy: *look in the market taker logs, see if
it's working as expected.* Read-only pass over the taker service log,
its journal, the `snt.state.snt-1` snapshot and the maker's own log.

1. **Confirmed what is actually running** before judging anything:
   `snt-checkout` @ `mm-main-7ca9d76` (the #40 merge) — checked by the
   PYTHONPATH the process imports, not the unit file (the 14-08 lesson)
   — **SNT-CFG-0023, journal `/var/lib/mm/snt20`, up 17:03:53Z**, AUTO,
   no `SNT_INTERVAL_*` / `SNT_TICK_S` / `SNT_MAX_ORDERS_PER_S` in the
   env, so the ruled defaults are in force.
2. **Measured the realised rate** two independent ways: fill timestamps
   from journald (a 3,600 s window) and send counts from the journal
   (the whole 4,560 s run).
3. **Tested the two HIGHs** the pre-merge review had predicted, against
   the tape rather than against reasoning.
4. **Checked the maker** over the same window (supervised32's tick
   lines and alarm counts) and compared with supervised30's tail.
5. **Read the ops snapshot** an operator/Edwin sees (`snt.state.snt-1`,
   88 KB, 180 books) for holdings, P&L and open orders.

## What we learned

### The rate lands, and the arrival-clock fix is proven at both ends

| | target | realised |
|---|---|---|
| LIVE, per book (sends) | 1.00 s | **1.13–1.16 s** |
| LIVE, per book (fills) | — | mean 1.16–1.25 s · median 0.77–0.88 · p90 2.6–2.8 |
| OVERNIGHT, per book | 400 s | **394 s** |
| portfolio | — | 5.70 sends/s · 24,534 fills in 76 min |

- **The 13% gap between the 1.0 s arrival draw and the 1.13 s send is
  the wash guard**, not the clock: ~11% of arrivals are skipped because
  an own remnant is resting on the opposite side. Designed behaviour
  (T-F01 survives a thinned stream).
- ⭐ **The gaps are still exponential** — LIVE fill p90 / mean = 2.30 =
  ln 10, which is the exponential identity. The faster rate has not
  turned Poisson arrivals into a metronome, which was the property most
  at risk (T-F01).
- **OVERNIGHT at 394 s against a 400 s target** is the arrival clock
  measured where the old tick-residual bias was smallest, and **LIVE at
  1.13 s** is it where the bias was worst (the old code would have run
  ~1.27 s before any wash-guard skips). Both ends behave.

### Both pre-merge HIGHs are real in kind and small in size

| | review predicted | measured |
|---|---|---|
| HIGH-1 realised gap | 1.51–1.63 s | **1.13–1.16 s** |
| HIGH-1 wash-guard skip | 33–39% | **~11%** |
| HIGH-2 P(same side) | 0.75–0.80 | **0.542** (per book 0.528–0.553) |
| HIGH-2 longest same-side run | 25–35 | **14–18** |

- **The arithmetic was right; one input was wrong.** Both HIGHs assume
  a remnant rests 1.5–1.8 s (the IOC cancel window). Against a deep
  maker book the taker's marketable orders terminate near-instantly —
  **94.4% fill, and zero genuinely resting orders at the sample
  instant** (316 filled + 13 cancelled, all inside the 60 s screen
  linger). The 1 s interval therefore overlaps a live remnant far less
  often than the worst case, so the guard bites ~11% of arrivals rather
  than a third of them.
- The residual directionality is measurable (0.542 vs 0.500) and worth
  showing Edwin in the E41 round, but it is not a shape that reads off
  the tape.

### Health

- **Zero rejects on 25,983 sends.** Zero halts, zero T-S05 reconcile
  alarms, zero `RATE CAP` lines (the cap is off), no errors.
- Buy fraction **49.6%** portfolio; clip mean **44 sh** — Edwin's
  reference distribution, unchanged by the rate.
- Crossing cost **$2,507–2,601/hr per LIVE book** ($19,307 across six
  books in 76 min) → **~$8,900 over a 3.5 h game against the $100k/day
  budget**, so the governor still cannot bind (T-M04 stands).
- 179 of 180 books **boot-rebased** at 17:03 (fresh journal against env
  floats that are now far from venue truth — adoptions up to ±1,984
  sh). The rebase doing exactly its job, and a reminder that
  `SNT_FLOAT_OVERRIDES` in `/etc/snt-1/env` is stale by design now.
- **The maker is unhurt: supervised32 has ZERO `MISSED_SWEEPS` in
  9,505 ticks**, 3 `DRAIN_CAPPED`. Its drain is 88.9 events/tick and
  sent 53.1 against 16.9/16.9 in supervised30's pre-game tail — but
  that window also has three live games, so the rise is not
  taker-attributable and should not be quoted as such.

### ⚠ The one real finding — a book can spend its float before the cap engages

**The soft cap measures the wrong quantity for a thin book.** The
1,500-share cap (with its 80% flatten bias) is applied to `pos`, the
DRIFT from the float; the sell gate is applied to `holding` = float +
pos. Where the venue-true float is **under** 1,500, holding hits zero
before the drift cap is ever reached, so the inventory control never
fires:

- **IPTCBEAR**: the boot rebase adopted the venue's real position,
  **float 1,056** (the journal thought 3,372). At 18:2xZ pos was −763,
  so **holding 293 sh** — about seven median clips from the sell gate
  going quiet and the book turning **buy-only**.
- Buy-only flow on a bot that exists to be uninformative is a T-F02
  problem. It is self-correcting (buys rebuild the holding) but visible
  while it lasts. **Not yet materialised** — BEAR's per-10-min buy
  share is still 45–55%, indistinguishable from BILL's.
- **The rate exposed this, it did not cause it.** Drift now reaches
  ±1,000 in about an hour; at 5.3 s it took the better part of a day.
- Exposure today is **1 book of 180** (float min 1,056 · p10 3,127 ·
  median 4,782) but **11 books sit under 2,500** and every game night
  compounds the drift.

## What went wrong / got stuck

- Nothing on the machines (read-only throughout).
- I nearly reported a false defect: my first probe of the state
  snapshot used guessed key names (`realized_pnl`) and printed `None`
  for the P&L Edwin asked for on 12-08. The real keys
  (`realized_pnl_total`, per book) are populated — **the P&L publishes
  fine.** Read the schema before calling something missing.

## Decisions made

- None. This session ruled nothing and changed nothing.

## Questions opened / closed

- **Closed in practice:** the pre-merge review's HIGH-1 and HIGH-2 —
  both measured, both far inside the tolerable range. Recorded in the
  #40 deploy-log row and the requirements addendum rather than as new
  questions.
- **Opened (filed on E39, touching T-M05/T-O08):** should the drift cap
  be relative to the float (`min(1500, k × float)`), or should the
  flatten bias key on `holding` instead of `pos`, or should thin books
  be re-seeded — now answerable with venue-true float numbers.
- **Still open, unchanged:** N44 (the portfolio cap value) — untested,
  the cap has never been switched on.

## Next

1. **Watch IPTCBEAR on the next game night.** If it prints buy-only for
   a stretch, that is the float-vs-cap finding materialising; the
   cheapest immediate lever is a float re-seed on the thin books.
2. **Exercise the cap arm of TT9** (`SNT_MAX_ORDERS_PER_S=4`) in a
   quiet slot — it is the one part of #40 that has never run.
3. **Edwin's E41 round** with the measured numbers in hand: the four
   intervals, P(same side) 0.542, the clip/buy distributions, and the
   thin-float question (E39).
4. George rules **N44** before a Sunday-sized slate — today's six LIVE
   books cost the maker nothing measurable, twenty would be a different
   test.
