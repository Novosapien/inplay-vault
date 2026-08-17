---
description: "Weekly engineering record for the trading service, 09-16 August 2026: 56 commits taking it from a nine-person pilot to store scale"
service: inplay-trading-service
window: 2026-08-09 .. 2026-08-16
commits: 56
authors: { westy412: 7, Hxsan: 49 }
branches: { touched: 15, merged: 12, open: 0 }
---

# inplay-trading-service — week of 09–16 August 2026

> **Delivery:** [[delivery]] · **Week:** [[work-log-2026-08-16]]

## Headline

**The trading service moved from a pilot for nine people to a service that can carry the store population.**

- Hxsan wrote 49 of the 56 commits, so this was his service this week
- **Order updates ran minutes late** — the market maker flooded the shared event queue, so
  real users saw their own fills late
- **Prices on the screen ran up to forty minutes behind the venue** — the market feed
  committed one message at a time
- **Users could not buy at the market price** — the venue accepts limit orders only
- The team fixed all three. It also built the rules that decide who may trade, when they may
  trade, and how many shares exist.

## Scope

- **Window:** 2026-08-09 to 2026-08-16
- **Commits:** 56 (westy412 7, Hxsan 49)
- **Branches touched:** 15 — 12 merged, 0 still open. Three of the 15 are the mainline
  branches `origin/main`, `origin/dev` and `origin/prerelease`.
- **Busiest day:** 2026-08-14 (15 commits)

**The shape of this week**

- **Two feature branches only** survive on disk
- **11 of the 12 short-lived branches** merged and disappeared inside the window
- **Eleven commits** went straight onto `origin/dev` or `origin/prerelease`, with no feature
  branch at all
- **The "Branches" table** names those direct commits as workstreams, not as a branch
- **Promotion path** — `origin/dev` → `origin/main` up to 2026-08-13, then
  `origin/prerelease` → `origin/main` from 2026-08-14
- **Every commit in the window is reachable from `origin/main`**

## Themes

### The market maker starved the retail order feed, twice

**Why it matters** — a real user could not see their own fill for minutes.
The market maker's own traffic pushed every retail update to the back of one shared queue.

**Order-event flood repair** · `5327745` · `c6d8c27` · `42f4e8c` · direct on `origin/dev`, reached `origin/main`
- **Symptom** — on 2026-08-10 the app showed an order as placed and filled minutes after
  tZERO had really executed it
- **Cause** — the gateway publishes every account's order events on one `order.>` subject.
  One JetStream consumer folds all of them.
- **Cause** — the market maker drove 44 events a second into that consumer. Real users'
  order updates queued behind that.
- **Evidence** — a 2,000-event sample was 100 percent market-maker traffic. 47 percent of it
  was `ORDER_REPLACED` re-quotes.
- **Evidence** — the consumer pinned at `max_ack_pending=1000`, with a 14,775 message backlog
  and 7,370 redeliveries
- **Fix** — a house-agent filter keyed on the Zitadel sub, not on the `MM` ClOrdID prefix
  (`5327745`)
  - a prefix is a convention the bot chooses
  - a filter on the prefix would let any account mute its own order feed
- **Fix** — the first cut guarded the JetStream fold only. The core NATS handler is a second,
  independent copy of the same fold (`c6d8c27`).
  - it still published 150+ market-maker events a minute after the durable's backlog drained
    to zero
  - that is the dangerous shape of the bug. The metric everyone watches said "fixed" while
    the work continued.
- **Fix** — Hxsan then made the fold concurrent and partitioned it by ClOrdID (`42f4e8c`)
  - every event for one order still reaches the same worker, so the sequence per order is
    unchanged
  - the same commit raised `max_ack_pending` to 4000 and `ack_wait` to 60s

**`fix/house-account-push`** · merged `origin/prerelease`, then `origin/main`
- **Symptom** — the starvation came back on 2026-08-15. Retail cancel outcomes took 13 to 62
  seconds to reach the app.
- **Cause** — the market maker had moved to a second account, `385656921832584863`, which was
  not in `house_agent_subs`
- **Evidence** — in a five-minute sample, 1,493 of 1,500 personal order pushes went to that
  one sub
- **Fix** — westy412 fixed production with the `INPLAY_HOUSE_AGENT_SUBS` environment variable
  on `inplay-trading-worker`
- **Fix** — westy412 then made the code default match on `fix/house-account-push`

> The order itself was fine. It went out on the ephemeral fast path in about 15ms.
> Only the display lagged.

### The market fold ran forty minutes behind the venue

**Why it matters** — the price on the screen was up to forty minutes old.
A user cannot judge a trade against a stale price.

**`fix/market-fold-conflation`** · `6f15b06` · merged `origin/main` (`4875ead`)
- **Symptom** — on 2026-08-15 the headline prices, the board, P&L and alerts were all stale
  in live
- **Symptom** — the order book channel stayed real-time, so only part of the screen was wrong
- **Cause** — the `market.>` consumer committed once per message, inline in the NATS callback
- **Cause** — a live game produces about 100 quote and trade messages a second. The drain
  managed 25 to 50 a second.
- **Cause** — the backlog built up inside the process on core NATS, with no JetStream
  consumer, so no bus metric showed it
- **Evidence** — the `venue_quotes` rows ran about 40 minutes behind
- **Fix** — the callback now only merges each message into pending state
- **Fix** — `run_quote_fold` writes everything each 0.5s pass in one transaction, so database
  work scales with symbol count, not message rate
- **Fix** — quotes and snapshots conflate to newest-per-symbol. Trades do not conflate, so
  they queue losslessly.
  - the tape and the candles need every print
- **Fix** — `_upsert_quote` gained a monotonic `source_ts` guard, so an older message can
  never overwrite a newer price
- **Fix** — the commit adds the alarm the incident lacked. A fold pass that carries old
  messages logs the lag.
- **Fix** — the shared NATS client gained an `error_cb`, so slow-consumer drops are no longer
  silent
- **Evidence** — the commit adds 13 tests in `tests/test_quote_fold.py`

**Session volume, seed-only** · `1112652` · direct on `origin/prerelease`, the same evening
- **Symptom** — one ticker showed about 62k and about 300k in the same second
- **Cause** — two message kinds both wrote the session volume column, so the figure
  alternated between two independent running totals
- **Fix** — `_upsert_quote` gained a `seed_only` mode. The trade fold owns volume, and the
  snapshot may only fill the gap at cold open.

### Live prices now reach the whole screen, not part of it

**Why it matters** — three separate paths left the app with prices that disagreed with each
other. The `feat/data-sync` branch and `fix/previous-close-push` closed all three.

**`feat/data-sync`** · `58b28bf` · the deferred quote publish
- **Symptom** — a symbol that moved twice and then went quiet left every subscriber on the
  first of the two prices
- **Symptom** — that is the stale number users read off the order ticket
- **Cause** — the 1s publish gate capped pushes at one per symbol per second. It threw away
  every update that arrived inside a live window.
- **Cause** — the venue publishes on change, not on a clock
- **Fix** — a refused claim now defers. The gate marks the symbol dirty, and a sweeper
  publishes the settled row once the window clears.
- **Evidence** — worst-case push latency becomes about 1.25s, in place of unbounded staleness

**`feat/data-sync`** · `1338761` · the per-league board digest
- **Symptom** — the ticker tape, directory tiles and watchlist chips moved only on the app's
  60s cold refresh, beside an order book that runs at 4Hz
- **Cause** — those screens hold no Centrifugo subscription. About 170 symbols against a
  60-token cap would evict the screens a user actually trades on.
- **Fix** — a per-league board digest channel carries only the symbols changed since the last
  digest
- **Fix** — one subscription covers all 170 symbols at the fan-out cost of one
- **Fix** — the split is per league because NCAA opens secondary trading ten days before NFL.
  A single channel would leak NFL prices in that window.

**`fix/previous-close-push`** · `e81a0d1` · the derived previous close
- **Symptom** — the push path and the digest carried `previousClose: null`
- **Cause** — tZERO sends no previous-close price, so the day-change baseline comes from our
  own tape. That derivation reached the REST response only.
- **Fix** — a worker timer now writes the derived value into `venue_quotes`

**`fix/previous-close-push`** · `b4783dc` · digest redelivery
- **Symptom** — each lost digest froze those symbols until the next trade
- **Cause** — Centrifugo publishes timed out intermittently in production
- **Cause** — the digest counted a timed-out publish as delivered, and it had already drained
  its dirty set
- **Fix** — `_publish` now reports whether Centrifugo accepted the publish. The digest
  re-marks the symbols of a failed league.

> Both branches merged to `origin/prerelease` and reached `origin/main`.

### Market orders, built on a venue that has no market order

**Why it matters** — tZERO accepts `OrdType=2` limit orders only, with no IOC or FOK.
"Buy at market" is built in this service.

**`feat/synthetic-market-order`** · `6543e3c` · merged `origin/prerelease`
- **What** — the whole server side, dark behind `INPLAY_SYNTH_ENABLED`
- **What** — the market consumer already received `market.book.{sym}` and dropped it. The
  book now caches to Redis per symbol.
- **What** — `services/synth.py` walks the book. The limit is the price of the level at which
  cumulative displayed size covers the quantity.
- **What** — the walk never goes past the top of book plus or minus the 2 percent band
- **What** — a price inside the band with too little size returns `THIN_BOOK` and a
  `fillableQuantity`, so the app can offer what would fill
- **What** — a residual watchdog cancelled anything still resting after two seconds

**`feat/synthetic-market-order`** · `ec40984` · merged `origin/prerelease`
- **Symptom** — live testing killed the two-second cancel
- **Cause** — the market maker cancel/replaces continuously. An order that lands in the gap
  fills nothing in that instant.
- **Cause** — the market maker then re-quotes around the resting order rather than across it
- **Evidence** — Hxsan's own 1000-share AKRZ sell priced at 36.94 off a real book, was
  accepted, and lost all 1000 shares to the grace cancel
- **Fix** — the residual now rests for the day at the walked ceiling. That is the retail
  collar convention.

**`feat/synthetic-market-order`** · `eec457d` · merged `origin/prerelease`
- **Symptom** — the dry run complained that market orders "missed the market" and sat resting
  off-price
- **Fix** — the residual now *chases*. When the grace expires, the sweep re-walks the current
  book and cancel/replaces the residual at the new marketable price.
- **Fix** — the original band cap and buying power both bound the chase, and it runs once,
  not in a loop

> The branch merged three times into `origin/prerelease` across two days.
> Each merge followed live evidence.

### Who may trade, when they may trade, and with how much money

**Why it matters** — a nine-person pilot allowlist became real rules. Five commits went
straight onto `origin/dev` on 2026-08-11, plus the merged branch `feat/trader-lite-eligible`.

**IPO float v3** · `3664c27` · direct on `origin/dev`
- **What** — the share count changed first
- **What** — IPO Business Requirements v3 sets 1,000,000 shares per NCAA team and 900,000 per
  NFL team
- **What** — it retires both the flat 5,000,000 float and the 20 percent holdback
- **Why** — the holdback goes entirely. It was reserved as market-maker inventory, and the
  market maker does not work that way.
- **Why** — the market maker acquires inventory by trade. Withheld shares would shrink
  `reference_float` and distort every quoted price.
- **Where it landed** — `asset_shards` holds the purchasable pool, so `sql/022` re-seeds the
  shards, not just `assets`

**The `sql/022` guard** · `21f23e1` · direct on `origin/dev`
- **Symptom** — the migration's own guard aborted the first attempt on 31,962 order rows
- **Cause** — a read-only diagnostic showed those are venue orders, which never draw from the
  IPO shard pool
- **Fix** — Hxsan narrowed the guard to decremented shards and live holdings
- **Evidence** — the run applied to production on 2026-08-11

**Derived market phase and the placement gate** · `27ed3bb` · `5488ee0` · `2376f96` · direct on `origin/dev`
- **Symptom** — `assets.phase` was seeded `ipo` on every row and nothing ever advanced it
- **Fix** — the market phase became derived, not stored (`27ed3bb`). It comes from the
  per-league offering windows, in real `zoneinfo`.
- **What** — NCAA secondary opens 27 Aug and NFL opens 7 Sep
- **What** — the service models the ~11.5 hour intermission between the offering close and
  the secondary open as `closed`
- **Fix** — `execute_ipo_buy` then stopped reading the stale column (`5488ee0`)
- **Fix** — order placement became a gate on the `venue-trader` role, a tZERO account id and
  an open phase (`2376f96`)
  - the account is a gate condition, not decoration
  - an empty FIX Tag 1 makes tZERO book the order against the firm account, so two users
    could self-match on a real ATS

**`feat/trader-lite-eligible`** · `15bf865` · `a26da93` · merged `origin/dev`, then `origin/main`
- **Symptom** — every non-US user finished verification and then got 403 on assets, wallet,
  orders, holdings and alerts
- **Cause** — two-track KYC had shipped a `trader-lite` role that nothing accepted
- **Fix** — `trader-lite` became trading-eligible (`15bf865`)
- **Fix** — market data reads then opened to every signed-in tier, including `preview`
  (`a26da93`)

**`feat/market-data-phase-gate`** · `87652bf` · merged `origin/dev`, then `origin/main`
- **What** — the gate bounds market data reads in time as well as by tier
- **Why** — before secondary opens there is no market to look at, so withheld reads return
  empty rather than 403

**`feat/wallet-credit`** · `3f807f3` · merged `origin/dev`, then `origin/main`
- **What** — `POST /admin/wallet/credit` for the broker's end-of-day referral job
- **Why** — it is idempotent, because the call crosses a network
- **Why** — a double credit is silent, wrong and unrecoverable once the user has traded on it
- **Where it landed** — `wallet_credits.ref` is the receipt. The insert and the balance
  update share one transaction.

### The leaderboard grew two boards, a podium and a second scoring mode

**Why it matters** — the vault always specified two more boards, and v1 deferred them.
The client then asked for a board that ranks banked money.

**`feat/leaderboard-verticals`** · `925f97d` · `08cab5a` · merged `origin/dev`, then `origin/main`
- **What** — risk-adjusted is P&L divided by volatility
- **What** — comeback is equity minus minimum equity, ranked only when the trough fell below
  baseline plus top-up
- **Where it landed** — no migration was needed. `leaderboard_periods` and `equity_snapshots`
  already carried the columns.
- **What** — volatility uses Welford accumulators in Redis, not a per-user snapshot list that
  would grow to about 25,000 entries a season
- **What** — `08cab5a` mints group tokens for all nine boards in one response
- **Why** — a Centrifugo channel with no token falls back to the 30s poll

**`feat/group-podium-preview`** · `0a00031` · merged `origin/dev`, then `origin/main`
- **What** — each group tile carries the gameday top three and the caller's own score
- **Why** — both fields read the same board key as `my_rank` in the same request, so the
  caller's podium row and their standing cannot disagree

**`fix/join-summary-podium`** · `0b5683e` · merged `origin/dev`, then `origin/main`
- **Symptom** — a group joined by share code came back with an empty podium
- **Cause** — a second tile builder that the podium work missed
- **Fix** — the join response carries the podium too

**`feat/data-sync`** · `765e7f9` · `6124354` · `5534a1a` · realized mode and cadence
- **What** — on 2026-08-14 the client asked for boards that rank banked money
- **Fix** — a realized-P&L mode for all three boards behind `INPLAY_LB_REALIZED_MODE`, off by
  default (`765e7f9`)
- **Why** — it folds the orders fill log, not `venue_holdings.realised_pnl`, because the
  venue book starts empty and IPO shares never seed it
- **Fix** — `6124354` closed the last gap. Hydration re-derived scores from the equity
  function.
- **Why** — with realized mode on, every worker restart — that is, every deploy — would have
  overwritten the realized boards
- **Fix** — the same branch cut the board's cadence from five seconds to one (`5534a1a`)
- **Why** — the client had noticed a rank that held still beside a tape that ticked

## Branches

| Branch | Author | Commits | Merged into | Purpose |
|---|---|---|---|---|
| `feat/data-sync` | Hxsan | 10 | `origin/prerelease`, then `origin/main` | Quote publish sweeper, board digest, realized-P&L mode, replace buying-power check, 1s board cadence. |
| `feat/synthetic-market-order` | Hxsan | 3 | `origin/prerelease` (3 merges), then `origin/main` | Market orders priced by a book walk, because tZERO takes limit orders only. |
| `feat/leaderboard-verticals` | Hxsan | 3 | `origin/dev`, then `origin/main` | Risk-adjusted and comeback boards, plus group tokens for all nine boards. |
| `fix/previous-close-push` | Hxsan | 2 | `origin/prerelease`, then `origin/main` | Derived previous close written into the quote row; digest redelivery after a failed publish. |
| `feat/wallet-credit` | Hxsan | 2 | `origin/dev`, then `origin/main` | Idempotent additive wallet credit for the referral top-up. |
| `feat/trader-lite-eligible` | Hxsan | 2 | `origin/dev`, then `origin/main` | `trader-lite` becomes trading-eligible; market data opens to the `preview` tier. |
| `fix/market-fold-conflation` | westy412 | 1 | `origin/main` | Conflated market fold in one transaction per pass, plus monotonic quote rows. |
| `fix/house-account-push` | westy412 | 1 | `origin/prerelease`, then `origin/main` | The second market-maker account joins the house-agent filter. |
| `feat/market-data-phase-gate` | Hxsan | 1 | `origin/dev`, then `origin/main` | Market data reads are secondary-only, enforced per league on the server. |
| `fix/join-summary-podium` | Hxsan | 1 | `origin/dev`, then `origin/main` | The group join response carries the podium too. |
| `feat/group-podium-preview` | Hxsan | 1 | `origin/dev`, then `origin/main` | Group tiles carry the gameday podium and the caller's score. |
| `feat/order-book-tokens` | Hxsan, merged by westy412 | 0 in window | `origin/main` (PR #2, `0b9bff9`) | Older branch. Its commits date 2026-08-06, before the window. Only the merge falls inside. |

### Commits made directly on a mainline branch

Eleven commits carry no feature branch. They group into four workstreams.

| Workstream | Branch | Author | Commits | Files | Purpose |
|---|---|---|---|---|---|
| Order-event flood repair | `origin/dev` | Hxsan | 3 | `services/venue.py`, `config.py`, `tests/test_venue.py` | House-agent filter on both fold paths, then a partitioned concurrent fold. |
| IPO float v3 and the derived market phase | `origin/dev` | Hxsan | 5 | `sql/022_float_v3_per_league.sql`, `sql/diag_float_v3_precheck.sql`, `sql/002_seed_assets.sql`, `scripts/gen_asset_seed.py`, `services/market_phase.py`, `services/ipo_engine.py`, `routers/trading.py`, `api/auth.py`, `config.py` | Per-league float, retired holdback, phase derived from the offering windows, placement gate. |
| Leaderboard deploy record | `origin/dev` | Hxsan | 1 | `specs/2026-08-03-leaderboard-v1/progress.md` | Records the verticals rollout and the cross-revision rollover error. |
| Market-order band and session volume | `origin/prerelease` | Hxsan, westy412 | 2 | `routers/trading.py`, `schemas.py`, `services/market.py` | `/trading/config` serves the band; the snapshot seeds volume only. |

- **`origin/main`** — 12 merge and promote commits in the window, and no direct work
- **`origin/dev`** — a further 6 merge commits

## Notable fixes and incidents

**2026-08-10 — retail order updates queued behind market-maker churn**
- **Symptom** — the app showed an order as placed and filled minutes after tZERO executed it
- **Cause** — one `order.>` JetStream consumer folds every account's events, and the market
  maker drove 44 events a second into it
- **Fix** — filter house-agent subs before the fold, on both the JetStream path and the core
  NATS path
- **Fix** — then make the fold concurrent, partitioned by ClOrdID (`5327745`, `c6d8c27`,
  `42f4e8c`)
- **Evidence** — the commits cite measured production numbers: a 2,000-event sample, and a
  14,775 backlog that drained to zero in about 90 seconds
- **Evidence** — a test drives `_handle_message` directly and asserts that nothing reaches
  Centrifugo

**2026-08-15 — the same starvation returned on a second account**
- **Symptom** — retail cancel outcomes took 13 to 62 seconds to reach the app
- **Cause** — the market maker moved to account `385656921832584863`, which was not in
  `house_agent_subs`
- **Fix** — westy412 set the `INPLAY_HOUSE_AGENT_SUBS` environment variable in production the
  same day
- **Fix** — `7375841` then makes the code default match, so the next image deploy does not
  regress it
- **Known side effect, recorded in the commit** — `services/position.py` does not read this
  set
- **Known side effect** — a filtered sub's "ours" book freezes, so its `POSITION DIVERGENCE`
  log lines become permanent noise

**2026-08-15 — quote rows about 40 minutes behind the venue**
- **Symptom** — headline prices, the board, P&L and alerts stale in live, while the order
  book channel stayed real-time
- **Cause** — the market consumer committed per message inside the NATS callback, on core
  NATS, so no bus metric showed the backlog
- **Cause** — two queue-group members at different backlog depths had published
  non-monotonic timestamps
- **Fix** — the conflated fold (`6f15b06`), plus a monotonic `source_ts` guard
- **Evidence** — 13 new tests in `tests/test_quote_fold.py`
- **Evidence** — 16 `tests/test_venue.py` failures pre-exist on `main` in a fresh test
  database, from schema drift. The commit states they are unchanged by this work.

**2026-08-15 — Centrifugo publish timeouts froze the tape**
- **Symptom** — a symbol's price stopped moving on the tape until its next trade, or until
  the app's 60s cold refresh
- **Cause** — `_publish` is fail-open by design, with a 2s httpx timeout, so a timeout never
  raised
- **Cause** — the board digest counted the publish as delivered and had already drained its
  dirty set
- **Fix** — `_publish` returns whether Centrifugo accepted the publish (`b4783dc`)
- **Fix** — the digest re-marks the symbols of any league whose publish failed. A failed
  per-symbol publish defers to the quote sweeper.
- **Evidence** — 82 lines of new tests in `tests/test_board_digest_redelivery.py`

**2026-08-15 — session volume alternated between two totals**
- **Symptom** — about 62k and 300k for one ticker inside the same second
- **Symptom** — the app used "volume rose" as evidence that a trade had printed. The flap
  could fire the order book's print flash for a trade that never happened.
- **Fix** — the snapshot seeds volume and never overwrites it (`1112652`)
- **Evidence** — not yet proven correct. The commit states that the true session volume
  figure is still unknown.
- **Evidence** — it needs the two tZERO messages compared side by side in the gateway wire
  log

**2026-08-14 — `/orders/replace` reached the venue with no buying-power check**
- **Symptom** — none observed yet
- **Cause** — `require_capacity` appeared exactly once in `routers/trading.py`, inside
  `place_venue_order`
- **Cause** — a resting buy could be resized upward past the balance. The wallet would go
  negative when the bigger order filled.
- **Cause** — the app had just shipped order editing, which made the path reachable
- **Fix** — release the original's reservation, apply the replacement's, then judge capacity
  against that (`0467b1f`)
- **Fix** — the wallet is locked `FOR UPDATE` across check and publish
- **Evidence** — six tests. One of them pins the double-count that a naive fix introduces.

**2026-08-12 — a replayed wallet credit reported a zero grant**
- **Symptom** — found on the first live end-to-end run
- **Cause** — the credit and the `UEAR` both succeeded, and the caller's commit then failed
- **Cause** — the retry path would have closed the row with `applied_amount=0` against a
  wallet that had really moved
- **Cause** — the user would keep the credit for free and could redeem again
- **Fix** — the replay reads the original grant back from the receipt (`a22b0ed`)

**2026-08-11 — the `sql/022` guard aborted on the wrong signal**
- **Symptom** — the float migration refused to run, and reported 31,962 order rows
- **Cause** — the guard treated any row in `orders` as evidence that the IPO float had been
  consumed
- **Cause** — those rows are venue orders, and secondary trading never draws from the IPO
  shard pool
- **Fix** — a read-only diagnostic established the true state: 0 decremented shards, 0
  holdings (`21f23e1`)
- **Fix** — the guard now fails only on a decremented shard or a live holding
- **Evidence** — the commit argues that the guard was right to stop a production data change
  on a table nobody had looked at

## Still open

- **Nothing unmerged** — no branch is unmerged. Every commit in the window is reachable from
  `origin/main`.
- **On disk, and merged** — `fix/market-fold-conflation` and `fix/house-account-push` are the
  two feature branches still on disk. Both are merged.
- **Older, already merged** — `origin/feat/leaderboard-v1` (last commit 2026-08-04),
  `origin/feat/price-alerts` (2026-07-31) and `origin/feat/new-ncaa-teams` (2026-07-16)
- **Older, already merged** — those three carry no commits in the window, and are merged into
  all three mainline branches
- **Branch drift** — `origin/dev` is 28 commits behind `origin/main`. Its last commit is
  2026-08-13, because the team switched to `origin/prerelease` for the rest of the week.
- **Branch drift** — `origin/prerelease` is 3 commits behind `origin/main`. Neither is ahead.
- **Caveat** — no fetch was run for this report, so both drift figures describe the refs on
  disk

**Work the commits themselves record as unfinished**

- **Unproven** — which tZERO figure is the true session volume. `1112652` makes the column
  consistent, not proven correct.
- **Unproven** — it needs the two messages compared in the `inplay-fix-gateway-go` wire log
- **Unproven** — until then the figure holds yesterday's total across a session rollover,
  until the day's first print
- **Stopgap** — house egress needs its own gateway subject. Both house-agent filters are
  described in the commits as a consumer-side stopgap.
- **Stopgap** — the proper fix is a separate subject in the gateway
- **Known noise** — `services/position.py` does not read `house_agent_subs`. Filtered subs now
  log permanent `POSITION DIVERGENCE` noise.
- **Dark** — synthetic market orders. `synth_enabled` is `false` in the code default on
  `origin/main`, and `synth_residual_action` defaults to `chase`.
- **Off** — realized-P&L mode. `lb_realized_mode` is `false`.
- **Off, with a warning** — the commit warns the flag must only flip at a period boundary or
  after an `lb:*` wipe, because both modes score into the same verticals
- **Dated dependency** — `trader-lite` reaches the leaderboard endpoints. `15bf865` flags
  that non-US users will appear on the payout board until the separate global board ships.
- **Dated dependency** — the board is dark until secondary opens on 27 Aug
- **A decision to take** — the equity-snapshot retention proposal is not applied. It is a
  migration.
- **A decision to take** — `specs/2026-08-03-leaderboard-v1/proposals/equity-snapshot-retention.md`
  models about 43 GB a season at 50,000 traders, and proposes four accumulator columns
- **Still in use** — the `INPLAY_VENUE_PLACE_SUBS` map. It remains the only source of the
  settlement wallet while allocation is manual.
- **Still in use** — it is also the per-user phase bypass for internal testers

**One thing I could not determine**

- **Unknown** — whether the deploy of any of this week's work to production was verified end
  to end
- **Evidence** — the commits cite live observations and test counts, and
  `specs/2026-08-03-leaderboard-v1/progress.md` records the verticals deploy
- **Gap** — nothing in the repository records a deploy or a soak for the fold conflation, the
  board digest or the market-order chase

## Commit appendix

### `fix/market-fold-conflation`

`6f15b06` · `2026-08-15` · `westy412` · fix(market): conflate the fold — one transaction per pass, monotonic rows

### `fix/house-account-push`

`7375841` · `2026-08-15` · `westy412` · fix(venue): the second MM account joins the house-agent filter

### `fix/previous-close-push`

`b4783dc` · `2026-08-15` · `Hxsan` · fix(market): a timed-out publish no longer freezes the tape
`e81a0d1` · `2026-08-15` · `Hxsan` · feat(market): the previous-close roll - derived baseline lands in the quote row

### `feat/synthetic-market-order`

`eec457d` · `2026-08-15` · `Hxsan` · feat(venue): market orders chase the flicker instead of missing the market
`ec40984` · `2026-08-14` · `Hxsan` · feat(venue): a market order's residual rests for the day instead of cancelling
`6543e3c` · `2026-08-14` · `Hxsan` · feat(venue): synthetic market orders — server side complete, dark by default

### `feat/data-sync`

`e5ec4ed` · `2026-08-14` · `Hxsan` · feat(leaderboard): /config says how the boards score
`6124354` · `2026-08-14` · `Hxsan` · fix(leaderboard): hydration honours realized mode — deploys stop rewriting boards
`b2cedd8` · `2026-08-14` · `Hxsan` · test(leaderboard): the realized swap is proven at the engine, not just the math
`765e7f9` · `2026-08-14` · `Hxsan` · feat(leaderboard): realized-P&L mode for all three boards, off by default
`8652495` · `2026-08-14` · `Hxsan` · docs(session): previous_closes stops asserting that 6 of 170 symbols trade
`0467b1f` · `2026-08-14` · `Hxsan` · fix(venue): /orders/replace checks buying power before it reaches the venue
`1338761` · `2026-08-14` · `Hxsan` · feat(market): a board digest, so the tape stops being a minute behind the book
`58b28bf` · `2026-08-14` · `Hxsan` · fix(market): a quote deferred by the publish gate is no longer thrown away
`3493abc` · `2026-08-14` · `Hxsan` · docs(leaderboard): the engine header stops naming the old 5s cadence
`5534a1a` · `2026-08-14` · `Hxsan` · perf(leaderboard): the board advances every second, not every five

### `feat/market-data-phase-gate`

`87652bf` · `2026-08-13` · `Hxsan` · feat(venue): market data is secondary-only, enforced server-side

### `fix/join-summary-podium`

`0b5683e` · `2026-08-13` · `Hxsan` · fix(leaderboard): the join response carries the podium too

### `feat/group-podium-preview`

`0a00031` · `2026-08-12` · `Hxsan` · feat(leaderboard): group tiles carry the gameday podium + the caller's score

### `feat/wallet-credit`

`a22b0ed` · `2026-08-12` · `Hxsan` · fix(admin): a replayed wallet credit must report the ORIGINAL grant
`3f807f3` · `2026-08-12` · `Hxsan` · feat(admin): idempotent additive wallet credit for the referral top-up

### `feat/leaderboard-verticals`

`08cab5a` · `2026-08-12` · `Hxsan` · feat(leaderboard): mint group tokens for every live vertical
`6379942` · `2026-08-12` · `Hxsan` · docs(leaderboard): record the verticals build, and propose snapshot retention
`925f97d` · `2026-08-12` · `Hxsan` · feat(leaderboard): risk-adjusted and comeback boards

### `feat/trader-lite-eligible`

`a26da93` · `2026-08-11` · `Hxsan` · feat(auth): market data is readable by every signed-in tier, including preview
`15bf865` · `2026-08-11` · `Hxsan` · feat(auth): trader-lite is trading-eligible, same as trader

### `origin/prerelease` — direct commits

`1112652` · `2026-08-15` · `westy412` · fix(market): the snapshot only seeds volume, never overwrites it
`093710e` · `2026-08-15` · `Hxsan` · feat(config): /trading/config serves the market-order band

### `origin/dev` — direct commits

`4aab450` · `2026-08-12` · `Hxsan` · docs(leaderboard): deploy record for the verticals rollout
`5488ee0` · `2026-08-11` · `Hxsan` · fix(ipo): buys obey the derived phase, not the stale column
`2376f96` · `2026-08-11` · `Hxsan` · feat(venue): gate placement on role + account + phase
`27ed3bb` · `2026-08-11` · `Hxsan` · feat(phase): per-league market phase, derived from the offering windows
`21f23e1` · `2026-08-11` · `Hxsan` · fix(ipo): the float guard was checking the wrong signal
`3664c27` · `2026-08-11` · `Hxsan` · feat(ipo): per-league float, holdback retired (v3)
`42f4e8c` · `2026-08-10` · `Hxsan` · perf(venue): partitioned concurrent fold + raised JetStream ceilings
`c6d8c27` · `2026-08-10` · `Hxsan` · fix(venue): guard the CORE fold path too, not just JetStream
`5327745` · `2026-08-10` · `Hxsan` · fix(venue): drop house-agent order events before the fold

### `origin/dev` — merge commits

`8fb329b` · `2026-08-13` · `Hxsan` · Merge feat/market-data-phase-gate: market data is secondary-only
`8db2a76` · `2026-08-13` · `Hxsan` · Merge fix/join-summary-podium: join response carries the podium
`5ba9d2d` · `2026-08-12` · `Hxsan` · Merge feat/group-podium-preview: group tiles carry the gameday podium
`b305019` · `2026-08-12` · `Hxsan` · Merge feat/wallet-credit: idempotent additive wallet credit
`d0b537b` · `2026-08-12` · `Hxsan` · Merge feat/leaderboard-verticals: risk-adjusted + comeback boards
`67a6a9b` · `2026-08-11` · `Hxsan` · Merge feat/trader-lite-eligible: trader-lite trades, market data opens to preview

### `origin/main` — merge and promote commits

`4875ead` · `2026-08-15` · `westy412` · Merge fix/market-fold-conflation: conflated market fold + monotonic quote rows
`124b6af` · `2026-08-15` · `westy412` · Promote prerelease -> main: MM house filter + snapshot volume seed-only
`4db8f1f` · `2026-08-15` · `westy412` · Merge fix/house-account-push: the second MM account joins the house-agent filter
`ccf7f4e` · `2026-08-15` · `Hxsan` · Merge fix/previous-close-push: derived previous close + digest redelivery
`177e14e` · `2026-08-15` · `Hxsan` · Merge feat/synthetic-market-order: the chase
`571d116` · `2026-08-14` · `Hxsan` · Merge feat/synthetic-market-order: residual rests (retail collar convention)
`6b7fdfc` · `2026-08-14` · `Hxsan` · Merge feat/synthetic-market-order: server side, dark behind INPLAY_SYNTH_ENABLED
`ada634b` · `2026-08-14` · `Hxsan` · Merge feat/data-sync: quote sync, board digest, realized mode (off), replace BP check
`739cbeb` · `2026-08-13` · `Hxsan` · Promote dev -> main: market-data phase gate
`8c20d71` · `2026-08-13` · `Hxsan` · Promote dev -> main: join response carries the podium
`8ec4bf4` · `2026-08-12` · `Hxsan` · Promote dev -> main: podium preview, wallet credit, verticals, IPO float v3, venue gating
`0b9bff9` · `2026-08-10` · `westy412` · Merge pull request #2 from Novosapien/feat/order-book-tokens

Total: 56 commits — 27 on merged feature branches, 11 direct on a mainline branch, 18 merge
or promote commits.
