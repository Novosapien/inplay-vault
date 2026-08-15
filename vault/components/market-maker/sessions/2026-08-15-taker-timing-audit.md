---
description: "Audit of taker timing + the stale-price complaint: the rate arithmetic closes; the ~40 min trading-worker quote-fold backlog found, fixed and deployed"
---

# 2026-08-15 — the taker timing audit, and the stale-price bug found

> **Who:** Claude (handover from the 15-08 evening session) · **Type:** live
> forensics, READ-ONLY on every machine (nothing published, changed or
> restarted; probes ran as scripts under /tmp on the VMs)
> **Refs:** taker SNT-CFG-0025 / journal snt22 @ `main@0b9f601` ·
> trading-worker rev 00051-hqh · sessions/2026-08-15-taker-rate-verification
> (the prior measurement) · Jared's 14-08 item #6

## What we did

The handover left two open problems. One: the taker prints 37–50
fills/min per LIVE book against a 1 s target, and ~15% of the shortfall
was unexplained. Two: George sees last price vs mid gaps (~$1.10 CHIE,
~$1 RAMS) on every team, and the market data path checked out healthy.

1. Verified the running state (snt-1 active, CFG-0025, snt22, the env
   posture, code `0b9f601`).
2. Measured send and fill gaps per book two ways: a timed 104.6 s
   journal-growth window, and whole-run counts from journal + journald.
3. Walked the last hop to the screen through Centrifugo's history API
   (the app's own delivery), from the Centrifugo VM with the API key
   from Secret Manager.
4. Traced the stale data to its source in the trading service code and
   measured the backlog three times over 20 minutes.

## What we learned

### ⭐ THE COMPLAINT IS EXPLAINED — the trading worker's quote fold runs ~40 minutes behind

**The app's team-page prices come from the `market:board.{league}`
Centrifugo channel. At 20:53Z its newest publication carried quote rows
stamped 20:18 — 34.5 minutes stale. By 21:12Z the lag was 44 minutes
and still growing.** The channel publishes continuously (~1.7/s, offsets
advancing); the CONTENT is old. The `market:book.*` channels are
seconds-fresh — a different path. So the book display is right, the
team-page price is ~40 min old, and the gap between them grows with
price velocity. This is George's complaint, and it is Jared's 14-08
item #6 ("team-page prices contradict the order book, P&L always off")
— same root, P&L reads the same quote rows.

The mechanism, from `inplay-trading-service` `src/app/services/market.py`:

- The worker subscribes core NATS `market.>` (queue `trading-market`,
  nats-py cb). **No JetStream consumer exists for MARKET_DATA** —
  confirmed via the NATS monitoring endpoint (consumer_count=0). The
  backlog therefore lives INSIDE the worker process, invisible to every
  bus metric — which is why the earlier session found the market data
  path healthy.
- `_handle_message` folds each `market.quote`/`market.trade` with a
  full DB session: fold + commit + push, sequentially per message.
- Measured input during the games: **~103 DB-bound messages/s**
  (quote 94.9/s + trade 8.2/s; book 73.5/s more, cheap Redis path but
  the same single queue). Drain: 2 worker instances (min-scale 2,
  1 vCPU), far below input. The queue grows all game, then drains
  overnight when input collapses — so the symptom vanishes by morning
  and returns every game night.
- The taker's new 1 s LIVE rate did not cause the defect; it raised the
  input rate that exposes it. The board digest itself
  (`publish_board_digest_once`) is healthy — it faithfully publishes
  whatever the stale rows say.

⚠ Risks while the backlog stands: nats-py's default pending buffer is
512k msgs / 128 MiB per subscription. A deep backlog can hit the bytes
ceiling and then NEW messages drop silently (no error_cb is set). No
slow-consumer log line was found tonight, so drops are a risk, not an
observed fact. Dropped trades would leave holes in candles/volume.

⚠ NCAA Saturday multiplies the input by ~10×. The backlog would grow
minutes per minute.

**Fix shapes (trading-service, not MM):** conflate instead of folding
per message — keep newest quote per ticker and fold on an interval
(trades still need the tape, but they are 8% of the volume); or move
the fold to a JetStream consumer so lag is at least visible. **Emergency
lever tonight:** a worker restart discards the in-process backlog and
the next messages repopulate the rows fresh — at the cost of the
backlog window's candle/volume history.

### The taker rate arithmetic CLOSES — there is no unexplained residual

Steady state 20:20–20:50Z, per LIVE book (CHIE/SAIN/RAMS/JAGU):
fills 442–473 per 10 min = **1.27–1.35 s per fill = 44–47/min**.

The decomposition, all three factors measured tonight:

| factor | value | source |
|---|---|---|
| arrival gap | 1.012 s | proven in the prior session, and CHIE's send gap hit 1.03 s in the window |
| ÷ (1 − wash-guard skip) | ~0.87–0.90 | send gaps 1.03–1.43 s across the four books |
| ÷ fill ratio per LIVE book | **0.87–0.89** | journal: unfilled 10.9–12.9% per LIVE book |
| **predicted fill gap** | **≈ 1.32 s** | matches the measured 1.27–1.35 s |

The handover's "~94% fill" was the PORTFOLIO number — quiet books fill
~99% and mask the LIVE books' 87–89%. The unfilled remnants count
twice: they stretch fill gaps directly, and each remnant blocks the
reversing side (wash guard) for up to its terminal (~1.8 s) — which is
also why P(same side) rose to 0.571–0.595 tonight (was 0.542 on snt20).
An at-touch IOC misses when the touch moves in flight; a fast game
book misses more. Microstructure, not a defect.

**The 37/min low end was the 20:00–20:12 window**: a HALT at 20:05:43,
a RECONCILE HALT on IPTCAFFC at 20:08:05, and a restart booting at
20:12:47 — each restart drops every book to OVERNIGHT until the bus
re-derives. Fills ran 2.2–3.5 s gaps in that window. The handover's own
trap note ("restarts during a live game produce exactly the stale-price
symptom") applies.

### The rest of the checklist

- **`SNT_INTERVAL_OVERNIGHT_S=40` IS realised**: 431 quiet-book sends
  over 104.6 s across ~170 books = 41.3 s per book. ⚠ Trap: a top-N
  listing of quiet books shows 15–17 s gaps — that is the Poisson upper
  tail of 170 books, not the mean. Nearly a false defect.
- Levers if George wants a true 1 s PRINT rate on LIVE books: raise the
  LIVE rate to ~0.85 s to compensate the losses, raise
  `sweep_probability` (more marketable through the touch, fewer
  misses), or have the wash guard read `leaves_qty`. All book-visible →
  Edwin's E41 round.
- Games ended ~21:00Z; the four books' fills collapsed on cue (POST
  derivation worked).

## What went wrong / got stuck

- The DB last-hop leg is unreachable from the MM VM (private-IP Cloud
  SQL, TCP refused from that subnet, no psql). Centrifugo history
  substituted — and turned out to be the better probe, because it shows
  what the app actually receives.
- The trading API requires a Zitadel bearer token; the API leg went
  unchecked. It reads the same stale rows, so it adds nothing.

## Decisions made

- None. Read-only session; nothing deployed, nothing restarted.

## Questions opened / closed

- **Closed: the taker-rate residual.** The three measured factors
  multiply to the measured gap. No hidden loss path remains at tonight's
  scale.
- **Closed: the stale-price mystery** — the quote-fold backlog above.
  Filed as a build-deploy-log row (owner: trading service / platform).
- **Still open:** the skip-reason observability gap in
  `orders_this_tick` stands (nothing logs why an arrival died). Tonight
  it was closed by measurement instead; the counter PR is still worth
  building before NCAA scale.

## Next

1. ~~Show George the backlog finding~~ ✎ **DONE same night — and the fix
   is BUILT on George's go:
   [inplay-trading-service PR #3](https://github.com/Novosapien/inplay-trading-service/pull/3)**
   (the conflated fold + the monotonic `source_ts` guard + the lag alarm
   + the NATS error_cb; 13 new tests, suite parity with main). A second
   session independently reproduced the bug from the app side (23¢/18¢
   adrift, non-monotonic sourceTs churn) — both traces agree.
   ✎ **MERGED + DEPLOYED same night on George's "push it now"**
   (`main@4875ead`, image `market-fold-20260815`, worker 00053-df4 +
   api 00065-bl4, 21:44–21:46Z). **Verified: board sourceTs ~44 min →
   3–7 s**; boot lag warnings cleared in ~2 min, then zero warnings,
   zero exceptions. Rollback coordinate: `mm-filter-volume-20260815`.
2. The E41 packet gains tonight's numbers: per-LIVE-book fill ratio
   87–89%, P(same side) 0.571–0.595, and the 1 s print-rate levers.
3. Follow-ups NOT in PR #3: the POSITION DIVERGENCE error flood in the
   same worker, and the leaderboard engine's own `market.>` consumer if
   it shows the same per-message shape.
