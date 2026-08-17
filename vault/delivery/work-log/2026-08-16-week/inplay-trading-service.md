---
description: "Weekly engineering record for the trading service, 09-16 August 2026 — 56 commits, mostly Hasan's, taking the service from a nine-person pilot to store scale"
service: inplay-trading-service
window: 2026-08-09 .. 2026-08-16
commits: 56
authors: { westy412: 7, Hxsan: 49 }
branches: { touched: 15, merged: 12, open: 0 }
---

# inplay-trading-service — week of 09–16 August 2026

> **Delivery:** [[delivery]] · **Week:** [[work-log-2026-08-16]]

## Headline

The trading service moved from a pilot for nine people to a service that can carry the
store population. Hxsan wrote 49 of the 56 commits, so this was his service this week.
Three problems dominated the week. Real users saw their own order updates minutes late,
because the market maker flooded the shared event queue. Prices on the screen ran up to
forty minutes behind the venue, because the market feed committed one message at a time.
Users could not buy at the market price, because the venue accepts limit orders only. The
team fixed all three, and also built the rules that decide who may trade, when they may
trade, and how many shares exist.

## Scope

- **Window:** 2026-08-09 to 2026-08-16
- **Commits:** 56 (westy412 7, Hxsan 49)
- **Branches touched:** 15 — 12 merged, 0 still open. Three of the 15 are the mainline
  branches `origin/main`, `origin/dev` and `origin/prerelease`.
- **Busiest day:** 2026-08-14 (15 commits)

Note the shape of this week. Only two feature branches survive on disk, and 11 of the 12
short-lived branches merged and disappeared inside the window. Eleven commits went
straight onto `origin/dev` or `origin/prerelease` with no feature branch at all. The
"Branches" table names those direct commits as workstreams, not as a branch.

The promotion path ran `origin/dev` → `origin/main` up to 2026-08-13, then
`origin/prerelease` → `origin/main` from 2026-08-14. Every commit in the window is
reachable from `origin/main`.

## Themes

### The market maker starved the retail order feed, twice

The gateway publishes every account's order events on one `order.>` subject, and one
JetStream consumer folds all of them. On 2026-08-10 the market maker drove 44 events a
second into that consumer. A 2,000-event sample was 100 percent market-maker traffic, and
47 percent of it was `ORDER_REPLACED` re-quotes. The consumer pinned at
`max_ack_pending=1000` with a 14,775 message backlog and 7,370 redeliveries. Real users'
order updates queued behind that. The app showed an order as placed and filled minutes
after tZERO had really executed it. The order itself was fine: it went out on the
ephemeral fast path in about 15ms. Only the display lagged.

Hxsan added a house-agent filter keyed on the Zitadel sub, not on the `MM` ClOrdID prefix
(`5327745`). A prefix is a convention the bot chooses. A filter on the prefix would let any
account mute its own order feed. The first cut guarded the JetStream fold only. The core
NATS handler is a second, independent copy of the same fold. It still published 150+
market-maker events a minute after the durable's backlog drained to zero (`c6d8c27`). That
is the dangerous shape of the bug: the metric everyone watches said "fixed" while the work
continued. Hxsan then made the fold concurrent and partitioned it by ClOrdID. Every event for
one order still reaches the same worker, so the sequence per order is unchanged. The same
commit raised `max_ack_pending` to 4000 and `ack_wait` to 60s (`42f4e8c`). All three commits went straight onto `origin/dev` and reached `origin/main`.

The starvation came back on 2026-08-15. The market maker had moved to a second account,
`385656921832584863`, which was not in `house_agent_subs`. In a five-minute sample, 1,493
of 1,500 personal order pushes went to that one sub. Retail cancel outcomes took 13 to 62
seconds to reach the app. westy412 fixed production with the `INPLAY_HOUSE_AGENT_SUBS`
environment variable on `inplay-trading-worker`. westy412 then made the code default match
on `fix/house-account-push`, which merged to `origin/prerelease` and reached `origin/main`.

### The market fold ran forty minutes behind the venue

On 2026-08-15 the headline prices, the board, P&L and alerts were all stale in live, while
the order book channel stayed real-time. The `market.>` consumer committed once per
message, inline in the NATS callback. A live game produces about 100 quote and trade
messages a second, and the drain managed 25 to 50 a second. The backlog built up inside
the process on core NATS, with no JetStream consumer, so no bus metric showed it. The
`venue_quotes` rows ran about 40 minutes behind.

westy412 rewrote the fold on `fix/market-fold-conflation` (`6f15b06`). The callback now
only merges each message into pending state. `run_quote_fold` writes everything each 0.5s
pass in one transaction, so database work scales with symbol count, not message rate.
Quotes and snapshots conflate to newest-per-symbol. Trades do not conflate, because the
tape and the candles need every print, so they queue losslessly. `_upsert_quote` also
gained a monotonic `source_ts` guard, so an older message can never overwrite a newer
price. The commit also adds the alarm the incident lacked. A fold pass that carries old
messages logs the lag, and the shared NATS client gained an `error_cb`, so slow-consumer
drops are no longer silent. The commit adds 13 tests in `tests/test_quote_fold.py`. It
merged to `origin/main` (`4875ead`).

A related fix landed on `origin/prerelease` the same evening (`1112652`). Two message kinds
both wrote the session volume column, so the figure alternated between two independent
running totals. One ticker showed about 62k and about 300k in the same second.
`_upsert_quote` gained a `seed_only` mode: the trade fold owns volume, and the snapshot may
only fill the gap at cold open.

### Live prices now reach the whole screen, not part of it

Three separate paths left the app with prices that disagreed with each other. The
`feat/data-sync` branch and `fix/previous-close-push` closed all three.

The 1s publish gate capped pushes at one per symbol per second. It threw away every update
that arrived inside a live window. The venue publishes on change, not on a clock. So a
symbol that moved twice and then went quiet left every subscriber on the first of the two
prices. That is the stale number users read off the order ticket. A refused claim now
defers instead: the gate marks the symbol dirty, and a sweeper publishes the settled row
once the window clears (`58b28bf`). Worst-case push latency becomes about 1.25s, in place
of unbounded staleness.

The ticker tape, directory tiles and watchlist chips hold no Centrifugo subscription. About
170 symbols against a 60-token cap would evict the screens a user actually trades on. They
moved only on the app's 60s cold refresh, beside an order book that runs at 4Hz. Hxsan
added a per-league board digest channel that carries only the symbols changed since the
last digest (`1338761`). One subscription covers all 170 symbols at the fan-out cost of
one. The split is per league because NCAA opens secondary trading ten days before NFL. A
single channel would leak NFL prices in that window.

tZERO sends no previous-close price, so the day-change baseline comes from our own tape.
That derivation reached the REST response only, so the push path and the digest carried
`previousClose: null` (`e81a0d1`). A worker timer now writes the derived value into
`venue_quotes`. Last, Centrifugo publishes timed out intermittently in production. The
digest counted a timed-out publish as delivered, and it had already drained its dirty set.
Each lost digest froze those symbols until the next trade (`b4783dc`). `_publish` now
reports whether Centrifugo accepted the publish, and the digest re-marks the symbols of a
failed league. Both branches merged to `origin/prerelease` and reached `origin/main`.

### Market orders, built on a venue that has no market order

tZERO accepts `OrdType=2` limit orders only, with no IOC or FOK, so "buy at market" is
built in this service. `feat/synthetic-market-order` merged three times into
`origin/prerelease` across two days, and each merge followed live evidence.

The first merge (`6543e3c`) added the whole server side, dark behind `INPLAY_SYNTH_ENABLED`.
The market consumer already received `market.book.{sym}` and dropped it, so the book now
caches to Redis per symbol. `services/synth.py` walks the book. The limit is the price of
the level at which cumulative displayed size covers the quantity. The walk never goes past
the top of book plus or minus the 2 percent band. A price inside the band with too little
size returns `THIN_BOOK` and a `fillableQuantity`, so the app can offer what would fill. A
residual watchdog cancelled anything still resting after two seconds.

Live testing killed the two-second cancel. The market maker cancel/replaces continuously.
An order that lands in the gap fills nothing in that instant. The market maker then
re-quotes around the resting order rather than across it. Hxsan's own 1000-share AKRZ sell
priced at 36.94 off a real book, was accepted, and lost all 1000 shares to the grace
cancel. The second merge made the residual rest for the day at the walked ceiling
(`ec40984`). That is the retail collar convention. The dry run then complained that market
orders "missed the market" and sat resting off-price. The third merge made the residual
*chase*. When the grace expires, the sweep re-walks the current book and cancel/replaces
the residual at the new marketable price (`eec457d`). The original band cap and buying
power both bound the chase, and it runs once, not in a loop.

### Who may trade, when they may trade, and with how much money

Five commits went straight onto `origin/dev` on 2026-08-11, plus the merged branch
`feat/trader-lite-eligible`. Together they replaced a nine-person pilot allowlist with real
rules.

The share count changed first. IPO Business Requirements v3 sets 1,000,000 shares per NCAA
team and 900,000 per NFL team. It retires both the flat 5,000,000 float and the 20 percent
holdback (`3664c27`). The holdback goes entirely, because it was reserved as market-maker
inventory and the market maker does not work that way. The market maker acquires inventory
by trade, and withheld shares would shrink `reference_float` and distort every quoted price.
`asset_shards` holds the purchasable pool, so `sql/022` re-seeds the shards, not just
`assets`. The migration's own guard aborted the first attempt on 31,962 order rows
(`21f23e1`). A read-only diagnostic showed those are venue orders, which never draw from the
IPO shard pool. Hxsan narrowed the guard to decremented shards and live holdings. The run
applied to production on 2026-08-11.

The market phase became derived, not stored (`27ed3bb`). `assets.phase` was seeded `ipo` on
every row and nothing ever advanced it. The phase now comes from the per-league offering
windows, in real `zoneinfo`. NCAA secondary opens 27 Aug and NFL opens 7 Sep. The service
models the ~11.5 hour intermission between the offering close and the secondary open as
`closed`. `execute_ipo_buy` then stopped reading the stale column (`5488ee0`). Order
placement became a gate on the `venue-trader` role, a tZERO account id and an open phase
(`2376f96`). The account is a gate condition, not decoration. An empty FIX Tag 1 makes
tZERO book the order against the firm account, so two users could self-match on a real ATS.

Two-track KYC had shipped a `trader-lite` role that nothing accepted. Every non-US user
finished verification and then got 403 on assets, wallet, orders, holdings and alerts
(`15bf865`). Market data reads then opened to every signed-in tier, including `preview`
(`a26da93`). `feat/market-data-phase-gate` bounded that in time as well as by tier
(`87652bf`). Before secondary opens there is no market to look at, so withheld reads return
empty rather than 403.

`feat/wallet-credit` added `POST /admin/wallet/credit` for the broker's end-of-day referral
job (`3f807f3`). It is idempotent, because the call crosses a network. A double credit is
silent, wrong and unrecoverable once the user has traded on it. `wallet_credits.ref` is the
receipt, and the insert and the balance update share one transaction.

### The leaderboard grew two boards, a podium and a second scoring mode

`feat/leaderboard-verticals` added the two boards the vault always specified and v1
deferred (`925f97d`). Risk-adjusted is P&L divided by volatility. Comeback is equity minus
minimum equity, ranked only when the trough fell below baseline plus top-up. No migration
was needed, because `leaderboard_periods` and `equity_snapshots` already carried the
columns. Volatility uses Welford accumulators in Redis, not a per-user snapshot list that
would grow to about 25,000 entries a season. `08cab5a` mints group tokens for all nine
boards in one response, because a Centrifugo channel with no token falls back to the 30s
poll.

`feat/group-podium-preview` put the gameday top three and the caller's own score on each
group tile (`0a00031`). Both fields read the same board key as `my_rank` in the same
request, so the caller's podium row and their standing cannot disagree.
`fix/join-summary-podium` then found the second tile builder that the podium work missed:
a group joined by share code came back with an empty podium (`0b5683e`).

On 2026-08-14 the client asked for boards that rank banked money. `feat/data-sync` added a
realized-P&L mode for all three boards behind `INPLAY_LB_REALIZED_MODE`, off by default
(`765e7f9`). It folds the orders fill log, not `venue_holdings.realised_pnl`, because the
venue book starts empty and IPO shares never seed it. `6124354` closed the last gap.
Hydration re-derived scores from the equity function. With realized mode on, every worker
restart — that is, every deploy — would have overwritten the realized boards. The same
branch also cut the board's cadence from five seconds to one (`5534a1a`). The client had
noticed a rank that held still beside a tape that ticked.

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

`origin/main` carries 12 merge and promote commits in the window and no direct work.
`origin/dev` carries a further 6 merge commits.

## Notable fixes and incidents

**2026-08-10 — retail order updates queued behind market-maker churn.** Symptom: the app
showed an order as placed and filled minutes after tZERO executed it. Root cause: one
`order.>` JetStream consumer folds every account's events, and the market maker drove 44
events a second into it. Fix: filter house-agent subs before the fold, on both the
JetStream path and the core NATS path. Then make the fold concurrent, partitioned by
ClOrdID (`5327745`, `c6d8c27`, `42f4e8c`). Verification: the commits cite measured
production numbers — a 2,000-event sample, and a 14,775 backlog that drained to zero in
about 90 seconds. A test drives `_handle_message` directly and asserts that nothing reaches
Centrifugo.

**2026-08-15 — the same starvation returned on a second account.** Symptom: retail cancel
outcomes took 13 to 62 seconds to reach the app. Root cause: the market maker moved to
account `385656921832584863`, which was not in `house_agent_subs`. Fix: westy412 set the
`INPLAY_HOUSE_AGENT_SUBS` environment variable in production the same day. `7375841` then
makes the code default match, so the next image deploy does not regress it. Known side
effect, recorded in the commit: `services/position.py` does not read this set. A filtered
sub's "ours" book freezes, so its `POSITION DIVERGENCE` log lines become permanent noise.

**2026-08-15 — quote rows about 40 minutes behind the venue.** Symptom: headline prices,
the board, P&L and alerts stale in live, while the order book channel stayed real-time.
Root cause: the market consumer committed per message inside the NATS callback, on core
NATS, so no bus metric showed the backlog. Fix: the conflated fold (`6f15b06`), plus a
monotonic `source_ts` guard, because two queue-group members at different backlog depths
had published non-monotonic timestamps. Verification: 13 new tests in
`tests/test_quote_fold.py`. The commit states that 16 `tests/test_venue.py` failures
pre-exist on `main` in a fresh test database, from schema drift, and are unchanged by this
work.

**2026-08-15 — Centrifugo publish timeouts froze the tape.** Symptom: a symbol's price
stopped moving on the tape until its next trade, or until the app's 60s cold refresh. Root
cause: `_publish` is fail-open by design, with a 2s httpx timeout, so a timeout never
raised. The board digest counted the publish as delivered and had already drained its dirty
set. Fix (`b4783dc`): `_publish` returns whether Centrifugo accepted the publish. The digest
re-marks the symbols of any league whose publish failed, and a failed per-symbol publish
defers to the quote sweeper. Verification: 82 lines of new tests in
`tests/test_board_digest_redelivery.py`.

**2026-08-15 — session volume alternated between two totals.** Symptom: about 62k and 300k
for one ticker inside the same second. The app used "volume rose" as evidence that a trade
had printed. The flap could fire the order book's print flash for a trade that never
happened. Fix: the snapshot seeds volume and never overwrites it (`1112652`). Not yet
proven correct: the commit states that the true session volume figure is still unknown. It
needs the two tZERO messages compared side by side in the gateway wire log.

**2026-08-14 — `/orders/replace` reached the venue with no buying-power check.** Symptom:
none observed yet. Root cause: `require_capacity` appeared exactly once in
`routers/trading.py`, inside `place_venue_order`. A resting buy could be resized upward
past the balance. The wallet would go negative when the bigger order filled. The app had
just shipped order editing, which made the path reachable. Fix (`0467b1f`): release the
original's reservation, apply the replacement's, then judge capacity against that. The
wallet is locked `FOR UPDATE` across check and publish. Verification: six tests. One of
them pins the double-count that a naive fix introduces.

**2026-08-12 — a replayed wallet credit reported a zero grant.** Symptom: found on the
first live end-to-end run. The credit and the `UEAR` both succeeded, and the caller's commit
then failed. The retry path would have closed the row with `applied_amount=0` against a
wallet that had really moved. The user would keep the credit for free and could redeem
again. Fix (`a22b0ed`): the replay reads the original grant back from the receipt.

**2026-08-11 — the `sql/022` guard aborted on the wrong signal.** Symptom: the float
migration refused to run, and reported 31,962 order rows. Root cause: the guard treated any
row in `orders` as evidence that the IPO float had been consumed. Those rows are venue
orders, and secondary trading never draws from the IPO shard pool. Fix (`21f23e1`): a
read-only diagnostic established the true state — 0 decremented shards, 0 holdings. The
guard now fails only on a decremented shard or a live holding. The commit argues that the
guard was right to stop a production data change on a table nobody had looked at.

## Still open

No branch is unmerged. Every commit in the window is reachable from `origin/main`, and the
two feature branches still on disk, `fix/market-fold-conflation` and
`fix/house-account-push`, are both merged.

Three older remote branches carry no commits in the window and are already merged into all
three mainline branches: `origin/feat/leaderboard-v1` (last commit 2026-08-04),
`origin/feat/price-alerts` (2026-07-31) and `origin/feat/new-ncaa-teams` (2026-07-16).

Branch drift to note. `origin/dev` is 28 commits behind `origin/main` and its last commit
is 2026-08-13, because the team switched to `origin/prerelease` for the rest of the week.
`origin/prerelease` is 3 commits behind `origin/main`. Neither is ahead. No fetch was run
for this report, so both figures describe the refs on disk.

Work the commits themselves record as unfinished:

- **Which tZERO figure is the true session volume.** `1112652` makes the column consistent,
  not proven correct. It needs the two messages compared in the `inplay-fix-gateway-go`
  wire log. Until then the figure holds yesterday's total across a session rollover, until
  the day's first print.
- **House egress needs its own gateway subject.** Both house-agent filters are described in
  the commits as a consumer-side stopgap. The proper fix is a separate subject in the
  gateway.
- **`services/position.py` does not read `house_agent_subs`.** Filtered subs now log
  permanent `POSITION DIVERGENCE` noise.
- **Synthetic market orders are dark.** `synth_enabled` is `false` in the code default on
  `origin/main`. `synth_residual_action` defaults to `chase`.
- **Realized-P&L mode is off.** `lb_realized_mode` is `false`. The commit warns the flag
  must only flip at a period boundary or after an `lb:*` wipe, because both modes score
  into the same verticals.
- **`trader-lite` reaches the leaderboard endpoints.** `15bf865` flags this: non-US users
  will appear on the payout board until the separate global board ships. The board is dark
  until secondary opens on 27 Aug, so that is a dated dependency.
- **The equity-snapshot retention proposal is not applied.** `specs/2026-08-03-leaderboard-v1/proposals/equity-snapshot-retention.md`
  models about 43 GB a season at 50,000 traders and proposes four accumulator columns. It
  is a migration, so it is a decision to take.
- **The `INPLAY_VENUE_PLACE_SUBS` map is still in use.** It remains the only source of the
  settlement wallet while allocation is manual. It is also the per-user phase bypass for
  internal testers.

One thing I could not determine: whether the deploy of any of this week's work to
production was verified end to end. The commits cite live observations and test counts, and
`specs/2026-08-03-leaderboard-v1/progress.md` records the verticals deploy. Nothing in the
repository records a deploy or a soak for the fold conflation, the board digest or the
market-order chase.

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
