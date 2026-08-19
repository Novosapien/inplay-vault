---
description: "Weekly engineering record for the InPlay mobile app, 09-16 August 2026 — 292 commits across 21 branches, the end of fabricated prices, store version 1.1, and the move to live worker data"
service: inplay-app
window: 2026-08-09 .. 2026-08-16
commits: 292
authors: { westy412: 109, Hxsan: 181, Claude Code: 2 }
branches: { touched: 21, merged: 20, open: 1 }
---

# inplay-app — week of 09–16 August 2026

> **Delivery:** [[delivery]] · **Week:** [[work-log-2026-08-16]]

## Headline

The app stopped showing numbers it had invented. A price, an order book, a chart or a
day change now comes from the venue, or the screen says it has no data. The team also made
the app faster and shipped version 1.1 to the App Store. The app now reads the live game
worker directly, so a kickoff, a score and a win probability arrive in seconds instead of
a minute. Most of this work sits on `prerelease` and has not reached users yet.

## Scope

- **Window:** 2026-08-09 to 2026-08-16
- **Commits:** 292 (westy412 109, Hxsan 181, Claude Code 2 — see the note below)
- **Branches touched:** 21 — 20 merged, 1 still open
- **Busiest day:** 2026-08-14 (78 commits)

Three counting notes, all checked:

1. **Use explicit times in the git command.** A bare `--since="2026-08-09"` resolves to
   2026-08-09 at the current time of day, not to midnight. Run at 19:30, it silently drops
   every commit made before 19:30 on 09 August. That is 18 commits here — all westy412,
   all on `feat/home-rework`, all between 15:59 and 18:42. The correct form is:

   ```
   git log --all --since="2026-08-09 00:00:00" --until="2026-08-17 00:00:00"
   ```

   The bare form returns 274. The correct form returns **292**. This file uses 292.
2. The two `Claude Code` commits are agent checkpoints of `.claude/RESUME.md`. They live
   on `refs/claude/*`, not on any branch. They belong to westy412's work `(agent commit)`.
3. This repository is live. The snapshot is 2026-08-16 19:54 BST, with `prerelease` at
   `00cbc9c`. One commit landed while this file was written.

## Themes

### 1. No fabricated prices anywhere

The app carried a simulated price engine from before the venue existed. It filled gaps
with invented numbers. A tester could see a fake `$20-80` price above a real order book.
A chart could draw a year of trades that never happened. A team page showed a
"Season High/Low" that nobody had set. That is a data-integrity problem, not a cosmetic one.

westy412 deleted the simulated price engine on `fix/no-fabricated-prices` (`9bdf1fb`).
The `LivePriceProvider` now serves venue quotes only. No feed means no prices, not demo
prices. He removed the fabricated position sparkline, the non-venue team-page fallback,
and the stale "Demo" badges. Earlier in the week he removed every generated order-book
ladder on `feat/home-rework` (`51af564`), so an empty ladder reads as
`No live order book available`. Hxsan removed the mock candle generator on
`fix/order-history-and-chart-migration` (`6e5a6a5`). It fabricated about 347 daily bars
that started the previous September. That is why charts folded back on themselves.

Hxsan then fixed the opposite failure. `TBA` meant two different things. 164 of 170 symbols
carried no previous close, so `TBA` was the default state of nearly every row on the board
(`6416a93`, on `feat/data-sync`). A flat day change now reads `0.00%` with no arrow and a
neutral colour, from one rule in `lib/format.dayChangePercent`. He also fixed a push that
wiped the day-change baseline on the symbols that actually trade
(`bd09e77`, `fix/tape-day-change-baseline`).

`fix/no-fabricated-prices`, `feat/data-sync` and `fix/tape-day-change-baseline` reached
`origin/prerelease` only. `feat/home-rework` reached `origin/main`.

### 2. Venue trading became reliable

Testers reported orders that vanished, taps that did nothing, and a limit price that
climbed under the thumb. Several of these are the kind of fault that ends in a user
selling the same shares twice.

westy412 fixed the order lifecycle on `prerelease`. A placed order stopped vanishing, and
positions now heal inside a session (`1a3395a`). A tZERO reject with `CxlRejReason=0` no
longer deletes a live order (`d0e3940`). The reducer had treated that catch-all code as
proof of a fill. westy412 confirmed the fault live on an `IPTCBUCC` short. A dropped iOS
sheet present no longer freezes every trade tap (`4bf5bdd`). The limit price is now frozen
and seeded from the last traded price (`ff00387`). `Max` now mirrors the server's projected
position, so the server no longer refuses the size the app proposed (`2d90015`). He also
exposed the built-but-hidden edit sheet, so open orders can be edited on all five surfaces
that show them (`e4ed039`).

Hxsan built the trading features. `feat/synthetic-market-order` added the MKT chip, which
sends `order_type='market'` with no price and lets the server walk the book (`aaaf0e5`).
`feat/sell-availability` states and enforces the sell bound on both order sheets
(`7fa0df9`). Two pending sells of 25 against 100 held no longer leave the user guessing.
`feat/data-sync` settled a real divergence. The quote feed and the depth feed are two
separate tZERO subscriptions that can legitimately disagree. Every surface picked one ad
hoc. `hooks/useTopOfBook` now makes the precedence one rule (`8b8cd74`).

All four branches reached `origin/prerelease` only.

### 3. The app got faster, and one fix was reverted

The app lagged on tab switches and scrolls. Hxsan profiled it and worked through
`fix-lag`. The root cause was whole-tree work unrelated to what was on screen.

`18d7669` coalesced quote ticks into one flush per 250ms. It also made channel
subscriptions follow what is on screen, not the first 60 rows of the board. `7ca292c` made a
price tick re-render only the rows showing that symbol. `ccdf6b7` paused ticks and polls
on blurred tabs. `370c922` gave each Discover panel its own scroller, so the schedule
finally virtualizes. A 60-game NCAA Saturday now mounts a screenful of rows, not all of
them. `0967655` enabled the React Compiler (486/486 components compile).

One change was reverted. `7821f78` set `freezeOnBlur` on the tab navigator and all five
nested stacks. Prerelease then reported tabs that intermittently stopped painting, because
`react-freeze` suspends a subtree and React 19 on the New Architecture can lose its
effects. Hxsan removed all six sites (`5e1b947`) and kept the memoisation half.

**This revert has not reached `origin/main`.** `7821f78` is on `origin/main`,
`origin/dev` and `origin/testing`. `5e1b947` is on `origin/prerelease` only. See
"Notable fixes" below.

### 4. Live game data now comes from the worker

The app polled `/sr/games/{id}/live` every 60 seconds, so a game could sit on screen as
"upcoming" for up to a minute after kickoff. The app has held a Centrifugo connection
since Phase 2, and the game page already streamed the same deltas.

westy412 subscribed the live candidates to their game channels, so the first publication
on a channel is itself the "live now" signal (`f8d8222`). He kept the 60-second poll as
the cold-open read and the safety net. He fixed a screen left open across kickoff
(`b7282d6`) and the final whistle (`1a1a3bf`). He fixed a socket drop that permanently
shortened the game page's moments rail (`0095a2c`). He added the worker's live win
probability to every card (`6844177`, `3fcf371`). He added a possession ball and the full
SR play-by-play feed (`ee619ba`). He rebuilt the landscape watch screen as a full trading
surface (`2ce92c2`, `438ccc6`). He also collapsed about 30 game-page requests into one
`/sr/games/{id}/aggregate` call (`814f921`).

All of this sits on `prerelease` and is not on `origin/main`.

### 5. Store 1.1, KYC tiers and the market-phase gate

Hxsan shipped version 1.1 through the promotion chain on 2026-08-12. `feat/store-1.1`
(`077f435`) cleared two iOS privacy-manifest blockers: `NSPrivacyTrackingDomains` was
empty while `NSPrivacyTracking` was true, and `NSPrivacyCollectedDataTypes` was missing
`ProductInteraction` and `SensitiveInfo`. That change is native and needed a full
`eas build`. Version 1.0.2 moved to 1.1, which moves the OTA runtime fence.

`feat/role-tiers` made KYC skippable, so a user can explore before verification
(`43ecac9`). `feat/referral-topup` replaced a mock wallet top-up that moved money only in
React state (`d6688b4`). That branch is flag-gated off, because the crediting scheduler
does not exist yet. `feat/leaderboard-verticals` and `feat/ranks-v2` turned the risk-adjusted and
comeback boards from a hardcoded "coming soon" card into real server-driven boards
(`2867b4e`, `3f0501f`).

Hxsan also replaced two build-channel switches with a per-league market phase served on
`/trading/config` (`3cbe980`, `a7d3107`). NCAA secondary opens 27 August and NFL opens
7 September, so a single global switch cannot be correct for ten days. About 90 call
sites now pass the instrument's league.

All these branches reached `origin/main`.

### 6. Home rebuilt to Edwin's mock, plus schedule and the season rollover

Edwin handed over a front-end mock of the app on 2026-08-08. The mock's home page is
trader-first: your money, your teams, the movers. The app's home page was games-first: the
day's slate. westy412 wrote the merge plan on 2026-08-09 and committed it to `inplay-vault`
(`ab0165b`, `vault/components/information-layer/sub-components/discovery-home/home-rework-plan.md`).
That file holds the 13-block list, the mock-to-component mapping, and the work order. It is
the written brief for this workstream, and it names the three open questions that were still
open when the build started.

The build was an iterated design response, not one pass. westy412 wrote 18 commits on
09 August alone, all on `feat/home-rework`. He built a first pass of the whole page
(`c381c07`), then reworked the header twice. `46c0eff` is "v2" and dropped the 372px
stadium hero. `68fec97` is "v3" and returned to a traditional header in George's block
order. Six more commits tuned the header insets and the ticker edge. One of them is marked
"George-approved" (`6331173`). He redesigned and restacked the IPO countdown three times,
across `ba35179`, `ee58c71`, `745c85c` and `9fa7c94`.

The rest of the plan landed later in the week. On 2026-08-15 westy412 extracted the
Discover movers rail into `components/market/TopMoversRail.tsx` and mounted it on Home as
"Today's Movers" (`2bd6564`, `91346fd`). That is block 7 of the plan, and the commit says
so. He then hid three cards behind `HOME_PROMO_CARDS_ENABLED` (`1b4c26c`). Two of
them are plan blocks that had already been built: `CompetitionsCard` (block 4) and
`IpoDriveCard` (block 9). The flag hides the way in and leaves the cards, routes and data
in the bundle, so one environment variable restores them.

On `feat/preseason-labels` he made the schedule read all three season phases, so August no
longer claims "No results yet" with three preseason weeks played (`fd5da17`). He added a
Home results row (`49c7cee`) and a `PRE`/`POST` week label derived from `season_type`
(`58f6822`). Hxsan fixed the IPO cards, which showed `TBA` for every last-season record
once the server's season resolver rolled to 2026 (`b382ac3`).

`feat/home-rework` and `feat/preseason-labels` reached `origin/main`. The Today's Movers
and promo-card work sits on `prerelease`.

## Branches

| Branch | Author | Commits | Merged into | Purpose |
|---|---|---|---|---|
| `prerelease` | westy412 76 / Hxsan 117 | 193 | partly `origin/main` (to 2026-08-13) | The shared integration branch. Both authors commit to it directly. |
| `feat/home-rework` | westy412 | 20 | `origin/main` | Home rebuilt to Edwin's 08 Aug mock, header iterated v1–v3; venue-only order book. All 18 of the 09 Aug commits are here. |
| promotion chain (`origin/dev`, `origin/testing`, `origin/main`) | Hxsan | 15 | `origin/main` | Six promotion runs and the iOS build-number syncs (builds 34–39). |
| `feat/data-sync` | Hxsan | 14 | `origin/prerelease` | One top-of-book rule, live charts, board digest, the modal-dismissal gate. |
| `feat/sell-availability` | Hxsan | 9 | `origin/prerelease` | Sell bounds stated and enforced; both order sheets share one layout. |
| `fix/prod-polish` | Hxsan | 8 | `origin/main` | Honest pre-market surfaces, ET countdowns, Company tab offering data. |
| `feat/synthetic-market-order` | Hxsan | 4 | `origin/prerelease` | The MKT chip — market orders from the ticket. |
| `fix/no-fabricated-prices` | westy412 | 4 | `origin/prerelease` | Delete the simulated price engine; edit open orders; NCAA symbol fixes. |
| `feat/ranks-v2` | Hxsan | 4 | `origin/main` | Field-rails standing hero, Discover drawer chrome, Groups as a race. |
| `feat/preseason-labels` | westy412 | 3 | `origin/main` | Preseason labels, all season phases, Home results row. |
| `feat/pending-orders-on-position` | Hxsan | 2 | `origin/prerelease` | Open orders render on their position card. |
| `feat/leaderboard-verticals` | Hxsan | 2 | `origin/main` | Risk-adjusted and comeback boards, exposed by server config. |
| `fix/tape-day-change-baseline` | Hxsan | 1 | `origin/prerelease` | A pushed quote keeps the day-change baseline. |
| `fix/ranks-note-placement` | Hxsan | 1 | `origin/prerelease` | The realized-scoring note moves above the stats. |
| `feat/chart-intraday-ranges` | Hxsan | 1 | `origin/prerelease` | 15m and 1h lead the season tabs; 3M and 1Y move to settings. |
| `feat/store-1.1` | Hxsan | 1 | `origin/main` | iOS privacy-manifest blockers cleared; version 1.1. |
| `feat/referral-topup` | Hxsan | 1 | `origin/main` | Server-backed wallet top-up, flag-gated off. |
| `feat/role-tiers` | Hxsan | 1 | `origin/main` | KYC becomes skippable; tier plumbing. |
| `local/live-replay-sandbox` | westy412 | 3 | **open** | Local replay sandbox. The same three changes were re-committed on `prerelease`. |
| `refs/stash` | westy412 | 3 | **not a branch** | One stash entry: the live-game swipe pager, marked sluggish. |
| `refs/claude/*` | Claude Code `(agent commit)` | 2 | **not a branch** | Two rate-limit checkpoints of `.claude/RESUME.md`. |

Nine further refs carry commits in the window but hold **no work of their own**:
`feat/games-year-dropdown`, `fix/order-history-and-chart-migration`, `fix-lag`,
`fix/live-reseed`, `feat/live-winprob-cards`, `chore/home-hide-promo-cards`,
`feat/home-top-movers`, `trading-ui-changes` and `origin/prerelease`. Each one is a
pointer left at a position on the shared `prerelease` line. Their commits are counted once,
under `prerelease`. The theme text still names them, because they label the work.

## Notable fixes and incidents

**`freezeOnBlur` is on `origin/main` and its revert is not.** `7821f78` set
`freezeOnBlur` on the tab navigator and five nested stacks. It reached `origin/main` on
2026-08-13 in the promote `2d40c4e`. On 2026-08-14 Hxsan removed all six sites in
`5e1b947`, because prerelease testers hit tabs that intermittently stopped painting: state
intact, navigator moved, screen never painted. `react-freeze` 1.0.4 suspends a subtree by
throwing a promise, and on React 19.1 with the New Architecture a suspended tree can lose
its effects. `5e1b947` is on `origin/prerelease` only. **The App Store build therefore
carries the fault.** Verified against the original repro on Metro; a device soak is still
needed before `freezeOnBlur` returns.

**A missing ATT native module took the whole app down.** `expo-tracking-transparency` was
the only eager import of an optional native module. On a binary built without it the
import threw at `app/_layout.tsx` module load. The root layout never mounted and every
screen blanked with `useAuth must be used within an AuthProvider`. Hxsan moved the require
into `initAds`' existing `try` (`f33ff8e`). `tsc --noEmit` clean.

**Trade taps died after a sheet closed.** Presenting an iOS Modal while a sibling modal is
still dismissing silently no-ops. The edit and cancel sheets added two new native modals.
"Close the cancel sheet, tap Cover" then left `sheetOpen` true with nothing on screen.
Every later tap was a no-op until a remount. Hxsan added a settle-then-flush gate
(`4f8864d`); westy412 extended it to the order sheet's own dismissal and made `openTrade`
self-heal (`4bf5bdd`).

**A venue reject deleted a live order.** tZERO overloads `CxlRejReason=0` as a catch-all
for its risk stack. The cause lives only in the Tag 58 text. The reducer treated reason 0
as proof of a fill: it removed the row and flashed a green "already filled". A short whose
resize failed the borrow re-check vanished until a cold start. westy412 fixed the reducer
and added tests (`d0e3940`). Confirmed live on 2026-08-15.

**A placed order vanished and the share count did not move.** The open-order merge kept a
local row only when the row post-dated the request. A snapshot that had not yet published
the new order therefore deleted it. westy412 moved the decision into a pure
`mergeOpenOrderSnapshot` under the Node harness, keyed on the app-minted ClOrdID with a
30-second window (`1a3395a`). Positions also gained an in-session self-heal.

**Charts drew a year of trades that never happened.** Both chart surfaces fed
`getSeasonCandles()`. That mock generator anchored to 1 September of the previous year.
In August it fabricated about 347 daily bars. Its day-grid re-stamp then made timestamps
run 10am, 11am, 10am. Hxsan dropped the prop (`6e5a6a5`). The same commit fixed a filled
order that never reached the Orders tab until a remount.

**Every IPO countdown ran about 13 hours fast.** `new Date(2026, 7, 22)` builds midnight
in the device's timezone. The offering opens 1:00pm ET, and a tester in London hit zero at
7pm ET the day before. Hxsan pinned all six countdowns to the real ET instants from the
requirements document (`4fdbbdf`, `2dd04f3`).

**Every last-season record read `TBA`.** The IPO cards called `useStandings(league)` with
no year. The server's season resolver had rolled to 2026, which has not kicked off, and
returned 170 rows of `0-0-0`. Nothing errored and nothing was missing. Hxsan added
`useCompletedStandings`, which asks whether any team has a season worth reporting
(`b382ac3`). This will recur every August unless the predicate matches the question.

**The limit price climbed under the user's thumb.** A hotfix. While pegged, an effect
rewrote the limit field on every book tick. westy412 removed the peg-follow effect; the
field now seeds once from the last traded price (`ff00387`).

## Cross-service dependencies

The app changed shape this week because three other services changed. These links matter
for the roll-up.

**`inplay-sportradar-service` (the worker).** The app now depends on the worker for live
state. `f8d8222` subscribes live candidates to their game channels and treats the first
publication as the "live now" signal. `6844177` and `3fcf371` read a new optional
`homeWinProb` on the delta snapshot; the commit says that feed is "live on testing".
`1a1a3bf` treats the worker's terminal snapshot as the authoritative end signal, and adds
SR's single-l `"canceled"` spelling. `814f921` follows service change `f2dff19` on testing:
`GET /sr/games/{id}/aggregate` and `season_type=ALL` on `/sr/schedule`. `ee619ba` reads
the `pbp` endpoint and `possessionAlias`. One open ask sits with the service team:
`/sr/winprob` takes no `season_type`, so preseason ids never reach it. `5efe7bd` fills that
gap client-side, capped at 20 probes, and retires itself when the endpoint learns
`season_type`.

**`inplay-trading-service`.** `fc63509` and `dc5a22f` are explicit pointers. A cleared
account that saw a generated ladder means one of two things. The service refused the
book-channel token, or it served a both-sides-null quote. The fix lives on branch
`feat/order-book-tokens` (`1d6def7`), PR #2. Do not patch the app fallback. `3cbe980` and
`a7d3107` depend on the per-league market phase the service serves on `/trading/config`.
`5de4af6` depends on `marketOrderBandPct` on the same endpoint — the app had hardcoded 2%
while the server band moved to 30. `aaaf0e5` depends on `order_type='market'`, and on the
server's `THIN_BOOK` / `fillableQuantity` response. `ef6b820` depends on the per-league
board digest. `58bbb92` records that the digest contract is now 1s.

**One open server-side gap.** `bd09e77` records that `previousClose` is derived server-side
and patched into the REST cold open only. Both push payloads are built from `venue_quotes`
rows where `previous_close` is NULL. The app now merges rather than replaces, but the push
payloads still carry no baseline.

**`inplay-fix-gateway-go`.** `d0e3940` states that the gateway half of the reject fix ships
separately, with the next gateway deploy. That half is a TTL on the request registry, plus
the "stuck Updating…" case. `845e376` notes the gateway already publishes
`market.trade.{symbol}`. Per-print pulse fidelity would need a `market:trades.{ticker}`
channel that carries the FIX aggressor side.

**Market maker.** `18d7669` sizes its 250ms coalescing against the market maker's 2s sweep,
and states the change reaches nothing on the market-maker side. `97be786` records that
order pushes ran minutes behind under the market-maker push flood, which left the ticket on
a stale side. `4595209` and `4f2c859` follow the IPO float v3 migration. That migration
went to production on 2026-08-11: NCAA 1,000,000 and NFL 900,000. It also retired the
holdback, because the market maker holds inventory by trading.

**`inplay-vault`.** The home rework implements a written plan that lives in the vault, not
in this repository: `ab0165b`, `vault/components/information-layer/sub-components/discovery-home/home-rework-plan.md`.
Two of its blocks are now hidden behind a flag (see Theme 6). Its section 7 names the next
queued workstream — Gamecast — and states that Gamecast is blocked on the pricing engine.
The pricing engine must publish the per-play decomposition of Edwin's `snap()` contract.

**Not yet deployable.** `d6688b4` (`feat/referral-topup`) is flag-gated off. Its config file
lists the deploy order. Flipped before the scheduler exists, a user would get a pending
top-up that nothing ever credits. `ebca840` depends on tZERO: the venue currently returns a
500 on a successful account create, so a real activation may report `pending`.

## Still open

- **`local/live-replay-sandbox`** — 3 commits by westy412, last on 2026-08-13. It looks
  **superseded, not abandoned**. All three changes exist again on `prerelease` under the
  same subjects (`da13f24`, `05abb38`, `931766e`). The branch is a local replay sandbox and
  is not on any remote.
- **The stash entry `caf06e3`** — "live-game swipe pager (works; sluggish — needs perf
  pass + swipe surface on gamecast card)", saved 2026-08-14. It is **in flight**, and the
  commit message states what remains.
- **Three open questions from the home-rework plan.** The plan (`ab0165b` in `inplay-vault`)
  lists them and no commit this week answers them. Does the backend hold the daily streak
  and the favourite teams? Which side implements which block, westy412's or Hxsan's? Has
  Edwin signed off the block order, and must anything on the current home survive that the
  mock drops? Two blocks also diverged from the plan. Block 3 wanted a greeting card
  carrying the streak; the streak went into the app bar instead (`417ffff`), and Home has
  no separate greeting card. Block 8 wanted a watchlist; `9fa7c94` **removed** the watchlist
  rail from Home. Neither divergence is recorded in the vault plan.
- **The promotion chain stopped on 2026-08-13.** 143 of the 292 commits in the window sit
  on `prerelease` and have not reached `origin/main`. `origin/dev`, `origin/testing` and
  `origin/main` all last moved on 2026-08-13. Everything in Themes 1, 2, 3 and 4 dated
  2026-08-14 or later is **not in a user's hands**. This includes the `freezeOnBlur`
  revert.

## Things this file does not settle

- Seven duplicate commit pairs exist. Each pair has an identical subject and different
  SHAs: `4da4e0d`/`51af564`, `fc63509`/`dc5a22f`, `da13f24`/`4570861`, `05abb38`/`0e6258d`,
  `931766e`/`059c06b`, `343a787`/`fdcd794`, plus three copies of
  `feat(education): gate the Learning Center off behind one flag`. These are cherry-picks
  or rebases across the two `prerelease` lines. Each is counted once. I did not work out
  which copy is canonical.
- The `.claude/worktrees/house-ads`, `.claude/worktrees/max-edits` and
  `.claude/worktrees/pwa` worktrees received **no commits in the window**. Their branch
  tips date from 2026-07-11, 2026-06-09 and 2026-05-29. The prompt listed
  `feature/house-ads`, `max-edits` and `worktree-pwa` as active; they were not.

## Commit appendix

Grouped by branch, newest branch first. 292 commits, every one listed once.

### `prerelease` (193)

`00cbc9c` · `2026-08-16` · westy412 · feat(live): fold the worker's real timeouts into the scoreboard dots
`48f4d12` · `2026-08-16` · westy412 · fix(game): the trade bar's spare width goes to Buy/Sell, not the qty chip
`438ccc6` · `2026-08-16` · westy412 · feat(watch): play-by-play joins the watch rail - and the rail learns to loop
`1ddebad` · `2026-08-16` · westy412 · fix(game): the win-prob curve routes team colors through the chart-color guard
`ee619ba` · `2026-08-16` · westy412 · feat(game): possession ball + the full play-by-play feed lands on the game page
`9b55fb5` · `2026-08-15` · westy412 · feat(currency): simulated amounts render bare - the struck-P mark comes off
`931e286` · `2026-08-15` · westy412 · fix(discover): the ticker grouping loosens a touch after validation
`51112ef` · `2026-08-15` · westy412 · fix(discover): the ticker row closes the dead air between symbol, price, and change
`3152639` · `2026-08-15` · westy412 · fix(discover): ticker prices read in white, not gray
`46e6e14` · `2026-08-15` · westy412 · feat(currency): the dollar sign gives way to the InPlay-dollar mark
`dca99e8` · `2026-08-15` · westy412 · fix(nav): a Home mover opens on the Home stack, and a parked tab always resets
`44f9ca2` · `2026-08-15` · westy412 · fix(trading): the wash-trade reject copy now states the venue's real rule
`97be786` · `2026-08-15` · westy412 · fix(trading): a resting market order says so, and a stale side heals itself
`1a3395a` · `2026-08-15` · westy412 · fix(trading): a placed order stops vanishing, and positions heal in-session
`9d99073` · `2026-08-15` · westy412 · feat(watch): the landscape screen fits its safe area, and the ads come off
`8dfd367` · `2026-08-15` · westy412 · fix(live): a burst means a moment just happened, and nothing else
`38db9c1` · `2026-08-15` · westy412 · fix(winprob): a near-black team can no longer vanish from the bar
`6704b02` · `2026-08-15` · westy412 · fix(gamecast): the midfield mark sits on the 50, not below it
`91346fd` · `2026-08-15` · westy412 · feat(home): Today's Movers reads as a vertical list, under the games card
`2ce92c2` · `2026-08-15` · westy412 · feat(watch): the watch screen becomes a full trading surface
`2bd6564` · `2026-08-15` · westy412 · feat(home): Today's Movers — the Discover rail, extracted and mounted on Home
`845e376` · `2026-08-15` · westy412 · feat(book): the top of book pulses when a taker takes it
`1b4c26c` · `2026-08-15` · westy412 · chore(home): hide the three promo cards, and the ad slot the Learning Center left orphaned
`3fcf371` · `2026-08-15` · westy412 · feat(live): win probability moves in-game on every card, and the label stays one line
`320afbd` · `2026-08-15` · Hxsan · Merge feat/sell-availability: sell bounds said + enforced, order sheets unified
`0095a2c` · `2026-08-15` · westy412 · fix(live): a socket drop no longer loses the game page's moments — reseed on resubscribe
`6f09ecf` · `2026-08-15` · westy412 · Merge remote-tracking branch 'origin/prerelease' into prerelease
`3c5282f` · `2026-08-15` · Hxsan · Merge fix/tape-day-change-baseline: pushes keep the day-change baseline
`a6d6dcf` · `2026-08-15` · Hxsan · Merge feat/pending-orders-on-position: orders live on their position cards
`95dd6b4` · `2026-08-15` · westy412 · fix(trading): the edit/cancel sheets get the same present-race guards as the order sheet
`d0e3940` · `2026-08-15` · westy412 · fix(trading): a venue "too late" reject no longer deletes a live order
`a180835` · `2026-08-15` · westy412 · feat(portfolio): My Positions allocation row, mirrored onto the Trade stack
`4bf5bdd` · `2026-08-15` · westy412 · fix(trading): a dropped sheet present can no longer freeze every trade tap
`b7672a7` · `2026-08-15` · Hxsan · fix(watch): the order form scrolls; Buy/Sell stays pinned and reachable
`ff00387` · `2026-08-15` · westy412 · fix(trading): the limit price is frozen — seeded from last, never follows the book
`167682a` · `2026-08-14` · westy412 · feat(chrome): one HeaderBar for every tab — extracted from HomeHeader
`0ad14a7` · `2026-08-14` · westy412 · Merge remote-tracking branch 'origin/prerelease' into prerelease
`c556db0` · `2026-08-14` · westy412 · feat(trading): sheet search page, one-click toggle placement, greyed switcher
`4c8b5b4` · `2026-08-14` · Hxsan · Merge feat/data-sync: live charts + the modal-dismissal gate
`c4079d8` · `2026-08-14` · westy412 · fix(trading): the trade FAB returns everywhere a screen has no bar of its own
`1bc0168` · `2026-08-14` · westy412 · feat(team): trade bar is persistent; Market tab leads with the book and hides nothing
`8887616` · `2026-08-14` · westy412 · feat(team): the sticky trade bar trades like the game page's matchup bar
`63a8274` · `2026-08-14` · Hxsan · Merge feat/synthetic-market-order: MKT orders from the ticket
`2ed0f2c` · `2026-08-14` · westy412 · fix(nav): buy-flow exits return to their origin; cross-tab dead-ends removed
`2dce80d` · `2026-08-14` · Hxsan · Merge fix/ranks-note-placement
`4037d1e` · `2026-08-14` · Hxsan · Merge feat/data-sync: realized-scoring note on Ranks
`5ef304f` · `2026-08-14` · Hxsan · Merge feat/data-sync: data streams synced, steppers, confirm lock, board digest
`a9264b1` · `2026-08-14` · westy412 · feat(trading): one-click trading, the matchup trade bar, and in-place cancel
`a073180` · `2026-08-14` · westy412 · feat(realtime): game channels can ride a separate sim Centrifugo
`2d90015` · `2026-08-14` · westy412 · fix(trading): Max mirrors the server's position projection; error copy says what to do
`fe32a2a` · `2026-08-14` · westy412 · Merge branch 'fix/no-fabricated-prices' into prerelease
`995046e` · `2026-08-14` · Hxsan · fix(trading): a stalled placement can no longer strand the ticket on "Placing…"
`370c922` · `2026-08-14` · Hxsan · perf(discover): panels own their scrollers; the schedule finally virtualizes
`3dc55f0` · `2026-08-14` · Hxsan · perf(home): the IPO drive countdown stops ticking on a blurred tab
`ae00ee1` · `2026-08-14` · Hxsan · perf(discover): every visited sub-tab stays mounted — warm-cache switches stop remounting
`f33ff8e` · `2026-08-14` · Hxsan · fix(ads): a missing ATT native module can no longer take down the root layout
`9a8b147` · `2026-08-14` · Hxsan · fix(nav): the Trade tab's stack root is the portfolio now
`de9c4fb` · `2026-08-14` · Hxsan · docs: the tech-stack table stops claiming FlashList
`0967655` · `2026-08-14` · Hxsan · perf(compiler): enable the React Compiler (Expo SDK 54, experiments.reactCompiler)
`f4149cb` · `2026-08-14` · Hxsan · perf(discover): the Teams panel survives sub-tab switches; deferred mounts hold their height
`ccdf6b7` · `2026-08-14` · Hxsan · perf(background): blurred tabs stop ticking and polling
`41b28da` · `2026-08-14` · Hxsan · perf(chrome): games-strip cards memoised, ScreenGlow context value stabilised
`6ec39db` · `2026-08-14` · Hxsan · perf(ranks): both leaderboard lists get windowing and stable render callbacks
`ad4db51` · `2026-08-14` · Hxsan · perf(schedule): one groupByDay, stable game identities, memoised rows
`515045a` · `2026-08-14` · Hxsan · perf(monogram): memoised, with a per-team palette cache
`6b8c393` · `2026-08-14` · Hxsan · perf(rows): portfolio, watchlist, and directory rows read their own symbol
`b99a10d` · `2026-08-14` · Hxsan · perf(home): the dashboard's money math is memoised and its game tiles are components
`4ec28c5` · `2026-08-14` · Hxsan · perf(ticker): one trading subscription per strip, per-symbol wakes, paused on blur
`0569126` · `2026-08-14` · Hxsan · perf(trading): the context invalidates on held prices, not on every board flush
`7ca292c` · `2026-08-14` · Hxsan · perf(prices): a price tick re-renders the rows showing that symbol, nothing else
`7a04e26` · `2026-08-14` · Hxsan · perf(nav): the tab bar derives its route from state and memoises its buttons
`e9827cb` · `2026-08-14` · Hxsan · perf(feedback): a FeedbackTarget holds no router subscription and registers once
`7ebff9e` · `2026-08-14` · Hxsan · perf(nav): the root layout holds no router subscription
`f0dbe35` · `2026-08-14` · westy412 · feat(trading): the order sheet streams live quotes and pegs the limit to the book
`25a337b` · `2026-08-14` · westy412 · feat(trading): the Trade tab exits the IPO takeover and lands on the portfolio
`6844177` · `2026-08-14` · westy412 · feat(live): the win-prob bar moves in-game when the worker sends it
`672a680` · `2026-08-14` · westy412 · fix(trading): review order survives a missing quote; no dead-end fallback
`e6234ae` · `2026-08-14` · westy412 · tweak(game): player stats leaders card shows five rows
`34d1109` · `2026-08-14` · westy412 · feat(game): player stats leaders card drills into a scoped full-list page
`2b2fc62` · `2026-08-14` · westy412 · feat(ticker): the tape shows favourites and games near their kickoff
`b8e1d71` · `2026-08-14` · westy412 · feat(game): per-player stat lines under the game stats
`452479d` · `2026-08-14` · westy412 · feat(game): live game stats lead the Game tab, events counter retired
`6b4f5b8` · `2026-08-14` · westy412 · feat(trading): empty ladder slots read as slots; card counts levels below
`fdcc321` · `2026-08-14` · westy412 · fix(trading): the order book card is a fixed six-row ladder
`086393f` · `2026-08-14` · westy412 · fix(nav): Open Orders and Fills resolve from a game opened on Home
`2e3d6e7` · `2026-08-14` · westy412 · fix(home): a live game no longer also sits in the Upcoming row
`5e1b947` · `2026-08-14` · Hxsan · fix(nav): drop freezeOnBlur — tabs intermittently stopped painting
`da13f24` · `2026-08-13` · westy412 · feat(game): Open Orders gets a scoped Game Orders page, like Game Fills
`05abb38` · `2026-08-13` · westy412 · feat(game): the Market tab trades like the portfolio, and shows nothing demo
`931766e` · `2026-08-13` · westy412 · fix(trading): the receipt's Done returns to the screen the buy started on
`cbe5162` · `2026-08-13` · Hxsan · Merge remote-tracking branch 'origin/prerelease' into prerelease
`15dcea5` · `2026-08-13` · Hxsan · Merge feat/chart-intraday-ranges: 15m/1h season tabs, 3M/1Y behind settings
`1a1a3bf` · `2026-08-13` · westy412 · fix(live): game end unlocks the post-game data and drops the LIVE badge
`b7282d6` · `2026-08-13` · westy412 · fix(live): a screen left open across kickoff now notices the game
`8a076ef` · `2026-08-13` · westy412 · fix(trading): the simulator can reach the Market tab again
`6e5a6a5` · `2026-08-13` · Hxsan · fix(trading): fills reach order history live; charts read venue data, not mock
`f8d8222` · `2026-08-13` · westy412 · feat(live): kickoff shows up instantly, not within a minute
`11cc704` · `2026-08-13` · westy412 · feat(game): depth chart unit is a dropdown, teams read away-at-home
`e156d66` · `2026-08-13` · westy412 · feat(game): depth chart above the injury report, one block per position
`814f921` · `2026-08-13` · westy412 · perf(sr): one aggregate request for the game page, one for a season year
`9898156` · `2026-08-13` · westy412 · fix(discover): the Schedule and Games tabs can show a live game
`bb3833c` · `2026-08-13` · westy412 · fix(home): live games come from the worker, not the cached feed
`5efe7bd` · `2026-08-13` · westy412 · feat(schedule): fill the win-probability gap the bulk slate leaves
`314038c` · `2026-08-13` · westy412 · fix(schedule): win probabilities land with the first paint
`77bad08` · `2026-08-13` · westy412 · Merge remote-tracking branch 'origin/prerelease' into feat/games-year-dropdown
`f347327` · `2026-08-13` · westy412 · perf(schedule): stop requesting season phases that cannot answer
`87e158e` · `2026-08-13` · westy412 · feat(discover): the season filter is a dropdown, not a chip row
`39fa1fb` · `2026-08-13` · Hxsan · perf(discover): stop tab switches mounting on the transition frame
`7821f78` · `2026-08-13` · Hxsan · perf(nav): freeze off-screen screens, memoise the hot paths
`18d7669` · `2026-08-13` · Hxsan · perf(prices): coalesce quote ticks, subscribe on demand, stop the tape resetting
`f2273a5` · `2026-08-13` · Hxsan · build: ios buildNumber 39 (prerelease build bcf46ba3)
`4768720` · `2026-08-13` · Hxsan · sync: buildNumber 38 from main
`4136176` · `2026-08-13` · Hxsan · Merge origin/main into prerelease: reconcile the split P&L fix
`f5a2b77` · `2026-08-13` · Hxsan · refactor(trading): derive the Trade button's reserve from the button itself
`343a787` · `2026-08-13` · Hxsan · fix(ranks): pinned self-card P&L no longer hides under the Trade button
`81b4759` · `2026-08-13` · westy412 · Merge feat/preseason-labels: preseason labels, full-phase schedules, home results row
`ee14290` · `2026-08-13` · Hxsan · feat(ranks): the group board wears the global board's chrome
`6788341` · `2026-08-13` · Hxsan · fix(ranks): swipe every board state, unbound the glow, trophy watermark
`0b2286b` · `2026-08-13` · Hxsan · Merge feat/ranks-v2: field rails, Discover drawer chrome, Groups as a race
`4716112` · `2026-08-12` · Hxsan · promote: testing -> main (pinned self-card P&L + handover)
`be1407d` · `2026-08-12` · Hxsan · promote: dev -> testing (pinned self-card P&L + handover)
`8ed1791` · `2026-08-12` · Hxsan · promote: prerelease -> dev (pinned self-card P&L + handover)
`2c35bdb` · `2026-08-12` · Hxsan · promote: fix/prod-polish -> prerelease (pinned self-card P&L + handover)
`fdcd794` · `2026-08-12` · Hxsan · fix(ranks): pinned self-card P&L no longer hides under the Trade button
`8bde4c1` · `2026-08-12` · Hxsan · promote: testing -> main (countdown ET instants)
`b54118f` · `2026-08-12` · Hxsan · promote: dev -> testing (countdown ET instants)
`0f5c9c1` · `2026-08-12` · Hxsan · promote: prerelease -> dev (countdown ET instants)
`bd2e241` · `2026-08-12` · Hxsan · promote: fix/prod-polish -> prerelease (countdown ET instants)
`1cc0008` · `2026-08-12` · Hxsan · promote: testing -> main (IPO countdown times)
`c6364d1` · `2026-08-12` · Hxsan · promote: dev -> testing (IPO countdown times)
`b18265e` · `2026-08-12` · Hxsan · promote: prerelease -> dev (IPO countdown times)
`8bf8a5c` · `2026-08-12` · Hxsan · promote: fix/prod-polish -> prerelease (IPO countdown times)
`b22fba5` · `2026-08-12` · Hxsan · chore: buildNumber 37 (eas build auto-increment — prerelease 1.1 tester build)
`ec5cdac` · `2026-08-12` · Hxsan · sync: buildNumber 36 from main
`5730d64` · `2026-08-12` · Hxsan · sync: buildNumber 36 from main
`65211c7` · `2026-08-12` · Hxsan · sync: buildNumber 36 from main
`10b84a6` · `2026-08-12` · Hxsan · chore: buildNumber 36 (eas build auto-increment — production 1.1 store build)
`cd67bcc` · `2026-08-12` · Hxsan · promote: testing -> main (Company tab row cleanup)
`671e79f` · `2026-08-12` · Hxsan · promote: dev -> testing (Company tab row cleanup)
`aa7c2f4` · `2026-08-12` · Hxsan · promote: prerelease -> dev (Company tab row cleanup)
`f83456c` · `2026-08-12` · Hxsan · promote: fix/prod-polish -> prerelease (Company tab row cleanup)
`47f816b` · `2026-08-12` · Hxsan · promote: testing -> main (Company tab real offering data)
`7b02520` · `2026-08-12` · Hxsan · promote: dev -> testing (Company tab real offering data)
`ab1699a` · `2026-08-12` · Hxsan · promote: prerelease -> dev (Company tab real offering data)
`bc52665` · `2026-08-12` · Hxsan · promote: fix/prod-polish -> prerelease (Company tab real offering data)
`c4d078d` · `2026-08-12` · Hxsan · promote: testing -> main (Market tab card inset)
`36af147` · `2026-08-12` · Hxsan · promote: dev -> testing (Market tab card inset)
`c8e47ef` · `2026-08-12` · Hxsan · promote: prerelease -> dev (Market tab card inset)
`155efca` · `2026-08-12` · Hxsan · promote: fix/prod-polish -> prerelease (Market tab card inset)
`9c2b8ab` · `2026-08-12` · Hxsan · promote: testing -> main (ad card + pre-market TBA fixes)
`2fc0b23` · `2026-08-12` · Hxsan · promote: dev -> testing (ad card + pre-market TBA fixes)
`0e4104c` · `2026-08-12` · Hxsan · promote: prerelease -> dev (ad card + pre-market TBA fixes)
`4a36c98` · `2026-08-12` · Hxsan · Merge fix/prod-polish: honest pre-market surfaces + full-bleed ad cards
`9892dcf` · `2026-08-12` · Hxsan · chore: buildNumber 35 (eas build auto-increment — prerelease 1.1 tester build)
`8de5be9` · `2026-08-12` · Hxsan · sync: buildNumber 34 from main
`e1fec47` · `2026-08-12` · Hxsan · sync: buildNumber 34 from main
`03b1167` · `2026-08-12` · Hxsan · sync: buildNumber 34 from main
`51fca28` · `2026-08-12` · Hxsan · chore: buildNumber 34 (eas build auto-increment — production 1.1 store build)
`785f92a` · `2026-08-12` · Hxsan · promote: testing -> main (store 1.1 — privacy manifest fixes, version 1.1, referral top-up dark)
`185b1ca` · `2026-08-12` · Hxsan · promote: dev -> testing (store 1.1 submission candidate)
`318afc9` · `2026-08-12` · Hxsan · promote: prerelease -> dev (store 1.1: privacy manifest, referral top-up, ranks verticals)
`056909b` · `2026-08-12` · Hxsan · docs(store): refresh the readiness report against live ASC + pod-tree evidence
`65e4881` · `2026-08-12` · Hxsan · Merge feat/store-1.1: privacy-manifest fixes + version 1.1
`b8975c1` · `2026-08-12` · Hxsan · Merge feat/referral-topup: server-backed wallet top-up, flag-gated
`da4026a` · `2026-08-12` · Hxsan · Merge feat/leaderboard-verticals: risk-adjusted + comeback boards
`b382ac3` · `2026-08-12` · Hxsan · fix(ipo): last-season record went TBA when the 2026 season rolled over
`4595209` · `2026-08-12` · Hxsan · fix(ipo): float is per league — NCAA 1M, NFL 900k
`71f6a69` · `2026-08-11` · Hxsan · feat: price tape for preview users, secondary-open on internal builds, slimmer pick-teams
`140b79f` · `2026-08-11` · Hxsan · fix(trading): the Trade button follows the market, not the account
`9bea994` · `2026-08-11` · Hxsan · feat(home): drop the standalone verify card, the competitions card carries it now
`939aa71` · `2026-08-11` · Hxsan · feat(home,ranks): one KYC action on the competitions card; Ranks on for internal builds
`163b842` · `2026-08-11` · Hxsan · feat(kyc): capture the trading-account signature during verification
`e4ae8e8` · `2026-08-11` · Hxsan · docs: iOS App Store readiness report for the next production build
`5399ff8` · `2026-08-11` · Hxsan · copy(kyc): title the step by what it gives you, and say trading is what it gives
`6de9f6e` · `2026-08-11` · Hxsan · feat(education): gate the Learning Center off on prerelease too
`dc61db5` · `2026-08-11` · Hxsan · feat(education): gate the Learning Center off behind one flag
`3bda023` · `2026-08-11` · Hxsan · Merge origin/prerelease: home rework + venue-only order book
`199525e` · `2026-08-11` · Hxsan · docs: record the per-league price gate and the four prerelease fixes
`173aa07` · `2026-08-11` · Hxsan · fix: four signup and Ranks-tab defects Hasan hit on prerelease
`1fe5ec6` · `2026-08-11` · westy412 · Merge branch 'feat/home-rework' into prerelease
`a7d3107` · `2026-08-11` · Hxsan · feat(phase): gate market prices per league, on the secondary open dates
`3cbe980` · `2026-08-11` · Hxsan · feat(phase): gate the order book and day change on the served market phase
`9d13d25` · `2026-08-11` · Hxsan · fix(kyc): show the verified state instead of stranding on "pending"
`ff9d56c` · `2026-08-11` · Hxsan · feat(kyc): choose your track before verifying
`0030422` · `2026-08-11` · Hxsan · fix(kyc): drop the X, match card margins, stop the transition dissolving
`7e8d4a2` · `2026-08-11` · Hxsan · feat(kyc): a way back into verification, from Home and the More hub
`ab1aec2` · `2026-08-11` · Hxsan · docs: record the IPO float v3 migration and what it turned up
`ebca840` · `2026-08-11` · Hxsan · feat(tzero): in-app trading-account activation
`c1770d6` · `2026-08-11` · Hxsan · Merge feat/role-tiers: skippable KYC + tier plumbing
`05794fe` · `2026-08-10` · Hxsan · feat(education): gate the Learning Center off behind one flag
`a851854` · `2026-08-10` · Hxsan · feat(education): gate the Learning Center off behind one flag
`4da4e0d` · `2026-08-10` · westy412 · feat(orderbook): venue data only — remove every generated-ladder fallback
`fc63509` · `2026-08-10` · westy412 · docs(orderbook): demo-ladder fallback is not the bug — pointer to the trading-service fix

### `feat/home-rework` (20)

`51af564` · `2026-08-10` · westy412 · feat(orderbook): venue data only — remove every generated-ladder fallback
`dc5a22f` · `2026-08-10` · westy412 · docs(orderbook): demo-ladder fallback is not the bug — pointer to the trading-service fix
`42e0d30` · `2026-08-09` · westy412 · feat(home): education card above the news feed (ads re-slotted between neighbours)
`9fa7c94` · `2026-08-09` · westy412 · feat(home): drop watchlist rail + referral bank card; IPO timings restacked as rows
`ba35179` · `2026-08-09` · westy412 · feat(home): IPO countdown redesigned — NCAA left, NFL right, dark strip on the orange card
`ee58c71` · `2026-08-09` · westy412 · feat(home): live IPO countdown on the Team IPO card
`745c85c` · `2026-08-09` · westy412 · feat(home): IPO drive moved directly under the challenge card (the mock's IPO slot)
`1349745` · `2026-08-09` · westy412 · copy(home): cash-track fine print — 'US tax residents only', Persona mention dropped
`df8fb84` · `2026-08-09` · westy412 · feat(home): competitions card rebuilt to Edwin's join fork — under the referral hero, mocked buttons
`6331173` · `2026-08-09` · westy412 · fix(home): header top gap dialed in — streak pill floats clear of the dynamic island (George-approved)
`ef9d853` · `2026-08-09` · westy412 · fix(home): symmetric header insets — gap from the notch equals gap to the ticker
`f0637c8` · `2026-08-09` · westy412 · fix(home): ticker flush to the header edge — optional style prop on MarketTicker zeroes its 2px trailing margin
`417ffff` · `2026-08-09` · westy412 · feat(home): streak flame in the app bar; ticker bottom edge = header bottom edge
`3bc70e8` · `2026-08-09` · westy412 · feat(home): Edwin-style app-bar header — logo, search, notifications, education quick-link
`71df675` · `2026-08-09` · westy412 · fix(home): breathing room under the header ticker — the gap the tab strip provides on Discover/Trade
`4d99481` · `2026-08-09` · westy412 · feat(home): header drawer chrome — same surface as Discover/Trade
`68fec97` · `2026-08-09` · westy412 · feat(home): v3 — traditional header + George's block order
`46c0eff` · `2026-08-09` · westy412 · feat(home): v2 — drop the 372px stadium hero for the static compact stadium bar
`c381c07` · `2026-08-09` · westy412 · feat(home): first pass of the Edwin-mock home rework — market ticker, competitions card, watchlist rail, top movers
`4ae200f` · `2026-08-09` · westy412 · wip: live-sim session fixes — equity formatting on home, period labels + replay date on game page, clock interpolation off, Centrifugo channel fix, scrub/watch tweaks

### promotion chain — `origin/dev`, `origin/testing`, `origin/main` (15)

`2d40c4e` · `2026-08-13` · Hxsan · promote: testing -> main (freezeOnBlur, memoised hot paths, deferred tab mount)
`7f525cd` · `2026-08-13` · Hxsan · promote: dev -> testing (freezeOnBlur, memoised hot paths, deferred tab mount)
`b731bd8` · `2026-08-13` · Hxsan · promote: prerelease -> dev (freezeOnBlur, memoised hot paths, deferred tab mount)
`2aea7ab` · `2026-08-13` · Hxsan · promote: testing -> main (price tick coalescing, tape reset fix)
`bc5e5fb` · `2026-08-13` · Hxsan · promote: dev -> testing (price tick coalescing, tape reset fix)
`b02b72c` · `2026-08-13` · Hxsan · promote: prerelease -> dev (price tick coalescing, tape reset fix)
`11f9630` · `2026-08-13` · Hxsan · sync: buildNumber 39 from prerelease
`64372cc` · `2026-08-13` · Hxsan · sync: buildNumber 39 from prerelease
`7ca4a20` · `2026-08-13` · Hxsan · sync: buildNumber 39 from prerelease
`e449809` · `2026-08-13` · Hxsan · sync: buildNumber 38 from main
`a8c129f` · `2026-08-13` · Hxsan · sync: buildNumber 38 from main
`c606079` · `2026-08-13` · Hxsan · build: ios buildNumber 38 (production build 51d70677)
`7990588` · `2026-08-13` · Hxsan · promote: testing -> main (Ranks v2, market-data gate, P&L reconciliation)
`26af493` · `2026-08-13` · Hxsan · promote: dev -> testing (Ranks v2, market-data gate, P&L reconciliation)
`a8d472c` · `2026-08-13` · Hxsan · promote: prerelease -> dev (Ranks v2, market-data gate, P&L reconciliation)

### `feat/data-sync` (14)

`4f8864d` · `2026-08-14` · Hxsan · fix(trading): a Buy tap after closing the cancel/edit sheet can no longer die
`22020b3` · `2026-08-14` · Hxsan · fix(charts): the chart moves with the tape instead of freezing at cold open
`8fb331b` · `2026-08-14` · Hxsan · feat(ranks): one line under the title when the boards rank realized P&L
`91a342a` · `2026-08-14` · Hxsan · Merge prerelease into feat/data-sync: one-click trading priced off the ladder
`3438511` · `2026-08-14` · Hxsan · docs(prices): every team trades now — the scarcity that justified TBA is gone
`711c2e3` · `2026-08-14` · Hxsan · perf(prices): the digest made two latent bugs constant — fix both
`9cc3ae9` · `2026-08-14` · Hxsan · fix(game): the Market Data card reads the same feed as the ladder beneath it
`d902a1d` · `2026-08-14` · Hxsan · feat(trading): the price steppers flank the field instead of sharing it
`063ebff` · `2026-08-14` · Hxsan · Merge prerelease into feat/data-sync: no-fabricated-prices + our sync work
`ef6b820` · `2026-08-14` · Hxsan · feat(prices): passive surfaces subscribe to the board digest
`6416a93` · `2026-08-14` · Hxsan · fix(prices): a flat day change reads 0.00%, not TBA — on every surface
`7584f2b` · `2026-08-14` · Hxsan · feat(trading): the limit price steps by tap, and locks the moment you confirm
`8b8cd74` · `2026-08-14` · Hxsan · feat(trading): one top-of-book rule, so the ticket and the ladder agree
`58bbb92` · `2026-08-14` · Hxsan · docs(leaderboard): the digest contract says 1s, because the server now does

### `feat/sell-availability` (9)

`5de4af6` · `2026-08-15` · Hxsan · feat(trading): server-owned band copy, bolder chips, edit block twins the ticket
`e3a75c1` · `2026-08-15` · Hxsan · copy(trading): the MKT chip reads Mkt
`302cd0b` · `2026-08-15` · Hxsan · style(trading): steppers slim to 32pt; shells shed padding - the price wins the width
`8e085b7` · `2026-08-15` · Hxsan · style(trading): the divider line becomes split panels
`b63d33d` · `2026-08-15` · Hxsan · style(theme): borderStrong token; the sheets' column divider takes it
`53eb56c` · `2026-08-15` · Hxsan · style(trading): steppers take the input shell's profile; edit-sheet shell matches the ticket
`f31564e` · `2026-08-15` · Hxsan · style(trading): chip pills on both sides, hairline divider between the halves
`71e760c` · `2026-08-15` · Hxsan · feat(trading): edit sheet gets Bid/Mid/Ask; Mid returns to the ticket; fields align
`7fa0df9` · `2026-08-15` · Hxsan · feat(trading): sell availability is said and enforced on both order sheets

### `fix/prod-polish` (8)

`f8fdb0b` · `2026-08-12` · Hxsan · docs: handover — store submission, referral top-up, countdown fixes
`2dd04f3` · `2026-08-12` · Hxsan · fix(countdowns): every timer targets the real ET instant
`4fdbbdf` · `2026-08-12` · Hxsan · fix(ipo): countdowns target 1:00pm ET, not midnight local
`0ed09da` · `2026-08-12` · Hxsan · fix(team): drop Company rows with nothing distinct to say
`4f2c859` · `2026-08-12` · Hxsan · fix(team): Company tab shows the real offering, not TBA
`0d21d33` · `2026-08-12` · Hxsan · fix(team): inset the Market tab placeholder to match sibling tabs
`07ed9e2` · `2026-08-12` · Hxsan · style(ads): align house card type with the paid card
`89146d2` · `2026-08-12` · Hxsan · fix(ui): honest pre-market surfaces + full-bleed ad card

### `feat/synthetic-market-order` (4)

`4da6101` · `2026-08-14` · Hxsan · copy(trading): the MKT explainers match the resting residual
`67d4a35` · `2026-08-14` · Hxsan · fix(trading): the ticket stops re-rendering on every book frame
`b8dc7fe` · `2026-08-14` · Hxsan · sync prerelease (ranks note placement)
`aaaf0e5` · `2026-08-14` · Hxsan · feat(trading): the MKT chip — synthetic market orders from the ticket

### `fix/no-fabricated-prices` (4)

`fb683af` · `2026-08-14` · westy412 · fix(trading): Max on a short accounts for the stock-loan fee reservation
`5a8ae95` · `2026-08-14` · westy412 · fix(data): correct NCAA symbols and the 2026 Pac-12 realignment
`e4ed039` · `2026-08-14` · westy412 · feat(trading): open orders can be edited, everywhere they are shown
`9bdf1fb` · `2026-08-14` · westy412 · fix(prices): no fabricated prices anywhere — no data renders as no data

### `feat/ranks-v2` (4)

`3ae9479` · `2026-08-13` · Hxsan · docs: subscriptions via native store billing spec
`ea66f96` · `2026-08-12` · Hxsan · feat(ranks): Discover drawer chrome + Groups as a race, not a rank badge
`3f0501f` · `2026-08-12` · Hxsan · feat(ranks): field-rails standing hero
`190d92b` · `2026-08-12` · Hxsan · feat(ranks): carry the group podium preview through the app data layer

### `feat/preseason-labels` (3)

`fd5da17` · `2026-08-13` · westy412 · feat(schedule,home): all season phases in schedules, restyled result tiles
`49c7cee` · `2026-08-12` · westy412 · feat(home): show the most recent completed week's results
`58f6822` · `2026-08-12` · westy412 · feat(schedule): label preseason games and disambiguate week numbers

### `local/live-replay-sandbox` (3) — open

`4570861` · `2026-08-13` · westy412 · feat(game): Open Orders gets a scoped Game Orders page, like Game Fills
`0e6258d` · `2026-08-13` · westy412 · feat(game): the Market tab trades like the portfolio, and shows nothing demo
`059c06b` · `2026-08-13` · westy412 · fix(trading): the receipt's Done returns to the screen the buy started on

### `refs/stash` (3)

`caf06e3` · `2026-08-14` · westy412 · On prerelease: wip: live-game swipe pager (works; sluggish — needs perf pass + swipe surface on gamecast card)
`8353a07` · `2026-08-14` · westy412 · index on prerelease: 1bc0168 feat(team): trade bar is persistent
`32834cf` · `2026-08-14` · westy412 · untracked files on prerelease: 1bc0168 feat(team): trade bar is persistent

### `feat/pending-orders-on-position` (2)

`9e2e8bb` · `2026-08-15` · Hxsan · fix(trading): a stolen touch can no longer leave the price stepper repeating
`e2919f5` · `2026-08-15` · Hxsan · Show pending orders on their position card in the portfolio

### `feat/leaderboard-verticals` (2)

`5b4be45` · `2026-08-12` · Hxsan · feat(ranks): all three verticals on the group board too
`2867b4e` · `2026-08-12` · Hxsan · feat(ranks): wire the risk-adjusted and comeback boards

### `refs/claude/*` (2) — agent commits

`d0831ff` · `2026-08-15` · Claude Code `(agent commit)` · WIP: Claude Code rate-limit checkpoint (310cb77c)
`73341b6` · `2026-08-15` · Claude Code `(agent commit)` · WIP: Claude Code rate-limit checkpoint (5f1697f7)

### Single-commit branches (6)

`bd09e77` · `2026-08-15` · Hxsan · `fix/tape-day-change-baseline` · fix(prices): a pushed quote no longer wipes the day-change baseline
`bdd7923` · `2026-08-14` · Hxsan · `fix/ranks-note-placement` · fix(ranks): the realized-scoring note centers above the where-you-sit stats
`348cd33` · `2026-08-13` · Hxsan · `feat/chart-intraday-ranges` · feat(charts): lead the season tabs with 15m and 1h, move 3M/1Y to settings
`077f435` · `2026-08-12` · Hxsan · `feat/store-1.1` · fix(ios): clear both privacy-manifest blockers; version 1.1 for submission
`d6688b4` · `2026-08-12` · Hxsan · `feat/referral-topup` · feat(referral): real wallet top-up — confirm, pending state, flag-gated
`43ecac9` · `2026-08-11` · Hxsan · `feat/role-tiers` · feat(kyc): make verification skippable so users can explore first
