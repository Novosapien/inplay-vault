---
description: "Weekly engineering record for the trading admin panel, 09-16 August 2026 — 117 commits, the maker and taker pages, and the rule that a surface must never state more than it can prove"
service: inplay-admin-panel-trading
window: 2026-08-09 .. 2026-08-16
commits: 117
authors: { westy412: 117, Hxsan: 0 }
branches: { touched: 27, merged: 27, open: 0 }
---

# inplay-admin-panel-trading — week of 09–16 August 2026

> **Delivery:** [[delivery]] · **Week:** [[work-log-2026-08-16]]

## Headline

The trading admin panel became the operator's live window onto both house engines. It gained
a maker page, a taker page, a manual order ticket and a pinned book rail. A new
NATS-to-Centrifugo pump inside the panel's own proxy feeds all four. Most of the week's effort
went into one rule: a surface must never state more than it can prove. The panel now says "the
engine is not publishing" instead of a confident zero. It also prefers the engine's own account
of what is live over a stale sports schedule.

## Scope

- **Window:** 2026-08-09 to 2026-08-16
- **Commits:** 117 (westy412 117)
- **Branches touched:** 27 — 27 merged, 0 still open
- **Busiest day:** 2026-08-12 (56 commits)

Every commit in the window has the git author `westy412`. There are no `Hxsan` commits and no
third-party commits. 89 of the 90 non-merge commits carry a `Co-Authored-By: Claude` trailer,
so most of this work is agent-assisted. The remaining 27 commits are pull-request merges into
`origin/main`.

## Themes

### 1. Engine truth outranks the schedule cache

The panel shows a Game chip beside each book. It answers one question: is this book's game
overnight, pre-kickoff, live or finished. The chip first read only the SportRadar cache, and
that source failed twice on consecutive nights.

On the night of 14 August the engine held game-bound books LIVE and filled orders on them.
Every Game chip on the panel read OVERNIGHT. The cause was a flushed SportRadar Redis cache.
The `21:16Z` and `20:45Z` redeploys removed `sr:{league}:teams:all` for both leagues, so the
`/game/board` join returned an empty map. The absence of the board outranked the presence of
the engine. `fix/game-chip-engine-truth` gave the chip an `engineState` prop from the taker's
per-book activity ladder, used whenever the board holds nothing.

The next day the same false OVERNIGHT returned on six live preseason books. The board had
recovered, and it now returned each team's SEPTEMBER season opener, because the cached REG
schedule holds no preseason games. A present-but-irrelevant fixture weeks away therefore beat
live engine truth. `fix/engine-live-outranks-schedule` made the precedence explicit and
commented. Board LIVE comes first. Engine LIVE or PRE_KICKOFF then outranks any board row,
then board pre or final, then the idle label. The branch also moved the maker page's inline
copy into a shared `useEngineActivity` hook, so the three surfaces that show a game phase agree.

Two earlier branches built this chip. `feat/game-status-board` added the Game column to the
market-data board and the `/game/board` join. `fix/pre-kickoff-window` stopped the chip from
styling any upcoming fixture as pre-game up to 45 days out. PRE-KICKOFF now applies only
inside the engine's own 60-minute window (`schedule_pre_kickoff_s = 3600`).
`feat/maker-game-phase` put the same chip on the maker's positions table. All four branches
reached `origin/main`.

### 2. The house cockpit — a live window on both engines

Before this week the panel had no view of the house accounts. `feat/trading-observability`
built one over 64 commits, and it is the largest branch of the week.

The proxy gained a pump (`proxy/house_pump.py`) that relays `mm.state` to `house:mm`,
`snt.state.>` to `house:snt.{botId}` and both accounts' order events to `house:fills`. The
panel gained a live-data layer (`src/lib/realtime/`) with one shared `centrifuge-js` client
and a ref-counted subscription registry keyed by channel. The house page opens exactly two
subscriptions whatever the row count; mids come from one shared 10 s REST quote poll.

The cockpit split into `/house/maker` and `/house/taker`, each with a health strip, metric
tiles and tabs. The taker's P&L is priced on `pos` — traded drift — never on `holding`,
because the float's cost basis is unknown. The commit records the worked example: pricing
`holding` instead would have shown +$544.50 where the truth is -$12. Unrealized P&L renders
"—" with a reason when there is no mid or the book is crossed, never NaN and never zero.

`feat/trading-observability` merged to `origin/main` as pull request #5.

### 3. Surfaces that worked before the engines published

The engines were under a deploy freeze all week, so `mm.state` and `snt.state` had no
publisher. The panel had to be useful anyway, and it had to stay honest about the gap.

The first answer was a fixtures mode. George deleted it rather than switched it off. An env
flag, a `NODE_ENV` check and a banner are all things that can be forgotten or mis-set. Invented
positions at a 1 s cadence look exactly like live ones. The house pages now say the engine is
not publishing and show nothing.

The second answer was to use the venue's own feeds. The pump replays the durable POSITIONS
JetStream stream and keeps the latest position per symbol per account. Positions and Holdings
therefore work with no engine change. The pump also accumulates a 500-event ring, a separate
200-execution ring and a reduced resting book per account, which seeds a cold browser. The
maker's Quotes tab rebuilds the resting ladder from accept, replace, cancel and execution
events. The taker's fallback became an order log, because the taker rests almost nothing.

The metric tiles were reworked twice after operator review. The first set was trader shorthand
and drew the response "I don't know what any of this is". Each tile now carries a plain-English
definition, a visible window under the value ("since 00:00" or "right now") and an ⓘ. The ⓘ
opens the full explanation inside the tile. `feat/maker-flow-tiles` later added the same daily
flow tally to the engine-snapshot strip. Those numbers vanished at the moment the engine came
alive and made them interesting. Branches: `feat/trading-observability`,
`fix/engine-view-design`, `fix/engine-tiles-and-sort`, `feat/maker-flow-tiles`. All merged to
`origin/main`.

### 4. The manual order ticket for the taker

`feat/trading-observability` added an admin-only `/manual-orders` page and the proxy routes
behind it. The ticket publishes R3 commands on `snt.control.snt-1` and waits for the engine's
reply. It never publishes on `gateway.orders.*`, because an order under an engine's userId
from outside the engine caused an observed venue-side hijack.

Four outcomes render four ways: ack, reject with the engine's own sentence, indeterminate, and
not-sent. Indeterminate blocks the resend until an `open_orders` snapshot stamped after the
send settles it. A resend reuses the original ref, so engine dedup replays the first reply.
The taker's `unknown` submission state is never folded into `working`.

Three follow-up branches improved the ticket for the operator. `feat/ticket-ux` replaced a
bare `<select>` of 180 tickers with a combobox that searches by team name. The same branch put
the live venue book beside the price field, with click-to-fill levels. `feat/ticket-quick-chips`
ported the app's quick-fill chips, where Max is `min(max_qty, floor(max_notional / px))` floored.
`feat/manual-history` added a command history panel, fed by a bounded 200-entry ring in the
proxy. The venue's order feed cannot say which taker orders were hand-placed, so the proxy is
the honest source. All merged to `origin/main`.

### 5. Maker and taker detail — pricing, liveness, flow and last trade

The engine team sent a brief on 13 August, and three branches implemented it display-only.

`feat/pricing-vs-quoting` put PRICING and QUOTING side by side on the maker's Quotes tab.
PRICING is the engine's own fair value, computed and invisible on the venue. QUOTING is that
price turned into a resting ladder. The reference price value is not on the wire, so the cell
says "not published" rather than improvising one from the order book.

`feat/maker-liveness-recipe` put a MAKER LIVE / LAGGING / DOWN banner on every trading page.
The verdict reads frame and tick clocks only, with the age computed server-side so browser
clock skew never enters it. A new `/api/house/liveness` returns about 200 bytes on a 3 s poll,
because the full frame is about 200 KB. The same branch fixed `/market/quotes` resilience. A
failed fetch used to replace the board with an empty map. The last good board now stands under
a "venue feed lagging" badge.

`feat/taker-last-trade` added a "Last trade" column to the taker's Positions table. The
execution ring could not serve it: 200 retained executions spanned six minutes across 66
books. The pump keeps a per-symbol map instead, served by `/house/last-trades/{account}`.
A book absent from the map reads "none in 42m", with the pump's watch horizon stated rather
than hidden. `fix/taker-dead-sort-chip` hid the Spread sort on the taker. The taker takes
liquidity and almost nothing rests, so the chip ranked nothing and fell through to book order.
All merged to `origin/main`.

### 6. Reading a 180-row table — filters, colour, render cost and access

`feat/positions-filters` added a control bar to both Positions tables: filters for league,
market state, game phase and "with a position", plus five sorts. Two rules carried over from
the week's defects. A filtered table says it is filtered, with a "showing 12 of 180 books"
line and a clear-filters link. An unknown value is never defaulted into a filter bucket. A
book with no activity reading is excluded from a phase filter rather than assumed OVERNIGHT.

`fix/state-colour-semantics` gave both state ladders one colour vocabulary in
`src/lib/state-style.ts`. A LIVE book was green on the maker and purple on the taker;
defensive was orange in one cell and amber in another. Green now means healthy or happening
now, amber approaching or mildly restricted, orange materially restricted, red stopped, muted
quiet or unknown. `feat/market-state-column` had earlier given market state its own column
with the engine's full cause ladder on click.

`perf/house-render` fixed a slow page. The maker page re-rendered on the 1 s engine snapshot
and on the 1 s clock tick. Each render rebuilt every row of two 180-row tables. Three changes
fixed it. Each row is now a memoised component that takes primitive props. Row-level clocks
arrive as a 5 s bucket. The Positions row shows the touch plus a resting count, instead of
every rung as a chip. No data is hidden.

On access: `feat/viewer-house-readonly` opened the house pages to the `viewer` role on
14 August, on George's instruction. Reads only — `/manual-orders` and every manual-order route
stay admin-only. The panel's allowlist and the proxy's allowlist moved in step. A panel list
wider than the proxy's turns a refusal into a mystery empty panel. The 12 August
"house is admin-only" ruling by Hasan is recorded in the code comments as relaxed by George,
so the comments cite both rulings. An earlier commit on `feat/trading-observability`
(`47edc34`) had extracted the role rules into `src/lib/role-access.ts` with 45 assertions. It
also made the sidebar read the same allowlists the middleware enforces. All merged to
`origin/main`.

## Branches

| Branch | Author | Commits | Merged into | Purpose |
|---|---|---|---|---|
| `feat/trading-observability` | westy412 | 64 | `origin/main` (PR #5) | The whole observability build: pump, live-data layer, house cockpit, manual ticket, pinned rail, role gating. |
| `feat/taker-last-trade` | westy412 | 1 | `origin/main` (PR #29) | Per-book "Last trade" column from a new per-symbol map in the pump. |
| `perf/house-render` | westy412 | 1 | `origin/main` (PR #28) | Stop the house pages re-rendering 180 rows twice a second. |
| `fix/state-colour-semantics` | westy412 | 1 | `origin/main` (PR #27) | One colour vocabulary for the activity and market-state ladders. |
| `fix/taker-dead-sort-chip` | westy412 | 1 | `origin/main` (PR #26) | Hide the Spread sort on the taker, where it ranks nothing. |
| `feat/positions-filters` | westy412 | 1 | `origin/main` (PR #25) | Filters and sorting on both Positions tables. |
| `fix/engine-live-outranks-schedule` | westy412 | 1 | `origin/main` (PR #24) | Engine LIVE beats a present-but-irrelevant schedule row. |
| `feat/maker-flow-tiles` | westy412 | 1 | `origin/main` (PR #23) | Today's order flow on the maker's engine tile strip. |
| `fix/game-chip-engine-truth` | westy412 | 1 | `origin/main` (PR #22) | Engine phase beats an empty SportRadar cache. |
| `feat/viewer-house-readonly` | westy412 | 1 | `origin/main` (PR #21) | House cockpit read-only for the `viewer` role. |
| `feat/maker-liveness-recipe` | westy412 | 1 | `origin/main` (PR #20) | Global maker liveness banner, shed truth, quote-fetch resilience. |
| `feat/pricing-vs-quoting` | westy412 | 1 | `origin/main` (PR #19) | Pricing and quoting side by side on the maker. |
| `fix/pre-kickoff-window` | westy412 | 1 | `origin/main` (PR #18) | PRE-KICKOFF only inside the engine's 60-minute window. |
| `feat/maker-game-phase` | westy412 | 1 | `origin/main` (PR #17) | A Game column on the maker's positions. |
| `feat/market-state-column` | westy412 | 1 | `origin/main` (PR #16) | A market-state column that explains its cause ladder. |
| `fix/engine-tiles-and-sort` | westy412 | 1 | `origin/main` (PR #15) | Plain-English engine tiles; league-order positions and holdings. |
| `fix/engine-view-design` | westy412 | 1 | `origin/main` (PR #14) | The engine's first live render gets the reviewed design. |
| `feat/manual-history` | westy412 | 1 | `origin/main` (PR #13) | Manual-order command history from a bounded proxy ring. |
| `fix/ticket-double-send` | westy412 | 1 | `origin/main` (PR #12) | Reset the ticket on resolve, to stop a duplicate order. |
| `feat/ticket-quick-chips` | westy412 | 1 | `origin/main` (PR #11) | Quantity and price quick-fill chips on the ticket. |
| `feat/ticket-ux` | westy412 | 1 | `origin/main` (PR #10) | Team-name search and a live book beside the price field. |
| `fix/positions-pull-consumer` | westy412 | 1 | `origin/main` (PR #9) | The POSITIONS replay stalled on flow control; rewritten as a pull consumer. |
| `fix/red-ladder-rescue` | westy412 | 1 | `origin/main` (PR #8) | Rescue-poll a red book before blaming the venue. |
| `fix/game-board-performance` | westy412 | 1 | `origin/main` (PR #7) | The game board took 41 s and returned nothing. |
| `feat/game-status-board` | westy412 | 1 | `origin/main` (PR #6) | A Game column on the market-data board. |
| `fix/book-test-symbols` | westy412 | 1 | `origin/main` (PR #4) | Accept `.TEST` symbols on `/market/book`. |
| `feat/test-symbols` | westy412 | 1 | `origin/main` (PR #3) | Accept and display the 10 venue test symbols. |

Every branch active in the window reached `origin/main`. This repo has one mainline branch and
no promotion chain, so there is no testing or prerelease state to report.

Three remote branches exist with no commits in the window and are already merged:
`origin/feat/is-test-flag` (tip 2026-07-01), `origin/feat/push-notifications-admin` (tip
2026-07-01) and `origin/scale-prep-auth-loadtest` (tip 2026-06-19).

## Notable fixes and incidents

**The proxy's NATS credentials had been wrong since 5 August** (`f9cf2e0`,
`feat/trading-observability`). `proxy/deploy.sh` bound the old shared `inplay-nats-token` to
both `NATS_PASSWORD` and `NATS_ADMIN_PASSWORD`. The 2026-08-05 rotation replaced that token
with per-service secrets, and this file was never updated. Every NATS connection from the
proxy failed with `Authorization Violation`, so `/orders/stream`, `/positions/stream`,
`/nats/*` and `/orders` had been broken since the rotation. The co-located Centrifugo bridge
was updated at the time; the proxy was missed. Verified on revision
`inplay-admin-proxy-00042-rqc`: both connections up, `/nats/streams` returns 200. A later
commit added `NATS_ROTATE_STAMP=20260805b`, which is the marker whose absence revealed the
miss.

**The POSITIONS replay stalled and both position tables rendered empty** (`b0afeed`,
`fix/positions-pull-consumer`). The consumer had delivered 2,824 messages and left 162,899
unprocessed. `nats-py` answers JetStream flow-control frames only on the callback delivery
path. The loop read through `next_msg()`, so the server paused at the flow-control window and
waited for a reply that never came. The loop's 30-second quiet rule then reported the
stall as "caught up". The first replay chunk was maker-heavy, which is why the maker page
looked fine and masked the defect. Rewritten as a pull consumer with batches of 200 and
`ack_policy none`. Verified on the deployed proxy: 165,828 messages replayed, 180 positions
per account, `caught_up` true.

**The derived maker book was full of ghost orders** (`743e65f`,
`feat/trading-observability`). Arizona Cardinals showed 15x17 levels against a 3-level venue
book, with derived bids above the venue's best bid. The FIX gateway emits every replace twice.
One copy goes on the new order's subject and one on the old one's. The payloads are identical
and the order of arrival is not guaranteed. Both reducers inserted under the subject id, so an old-subject copy that
landed second re-created the dead order at the new price. One ghost per replace, at about 50
replaces a second. Both reducers now insert under `newClOrdId`. A replay of the same 90 s
trace gave 4x5 and 3x2 levels, with the deepest book anywhere at 6x6.

**The mirrored collar guard was wrong by 100x** (`508c603`, `feat/trading-observability`).
`collar_pct` on the wire is a fraction: the engine holds `Decimal("0.20")` for the ruled ±20%
and publishes it unscaled. The panel divided by 100 again, giving a 0.2% threshold, so an
ordinary order 0.59% off mid tripped a guard breach. The engine still enforced correctly, so
nothing wrong reached the venue. The damage would have been operator trust. The panel would
have taught an operator to ignore the control. The one order genuinely 25% off mid would then
have looked like the fifty before it. The dev fixture carried the display form `20` and would
have re-certified the bug, so `c46c219` corrected the fixture too.

**A re-armed Send button placed a real duplicate order** (`24096f4`,
`fix/ticket-double-send`). The busy guard covered only the in-flight window. On resolve the
button re-enabled while the ticket still sat on the confirm step with the same draft. A second
click then minted a fresh ref, which the engine correctly treated as a new order. The
operator measured a real duplicate this way. The ticket now resets to the entry step on the
busy true-to-false edge.

**A token refresh would have dropped the whole WSS connection every hour** (`41096fd` and
`17fde29`, `feat/trading-observability`). Centrifugo requires a subscription token's `sub` to
equal the connection's. The connection-token route minted a fresh random `sub` on every
refresh. The failure is worse than a per-channel refusal: Centrifugo closes the whole
connection with code 3500. Every 3600 s expiry would have taken the ladder, the tape, the rail
and the house cockpit down together. It would have read as an unexplained transport
failure. The route now accepts and reuses a presented `sub`. It also validates the role segment
of that `sub` against the caller's server-side role.

**The game board took 41 seconds per call and returned nothing** (`ea42188`,
`fix/game-board-performance`). Redis SCAN walks the whole keyspace and the match pattern does
not index. The board ran that walk once per league at `count=200`, against a Redis shared
with production. One shared pass at `count=5000` plus a 20 s whole-body cache brought it to
2.9 s cold and 0.12 s cached. The board also returned empty in August. The only cached
schedule is the 2026 regular season, and its first game sat beyond the 14-day window.
The window is 45 days now.

**The pump-health parser had never matched the payload** (`6b87ba4`,
`feat/trading-observability`). `usePumpHealth` looked for `house_pump.subjects` as a map of
per-subject records. The proxy has never sent that; it sends two parallel maps keyed by
subject. The parser produced an empty map, which is indistinguishable from a pump with no
subscriptions. Every surface therefore fell through to a "cannot attribute" sentence, for the
whole life of the feature. The parser now reads the real shape and warns if neither key is
present.

**A one-sided quote update blanked the other side of a row** (`34683d0`,
`feat/trading-observability`). `market.quote` is a partial-update contract where null means
"no change". `coalesceQuote` honoured that across streamed messages, but it folded onto an
empty quote. Before the first update on the other side it therefore held a legitimate null
there. The page then wrote that whole object over the REST seed. Whichever side had not ticked
yet went blank, which is why it hit some teams and not others.

**A dead book kept showing depth** (`11a6c5e`, `feat/trading-observability`). The engines were
stopped and the venue books cleared, but pinned `.TEST` ladders still showed rungs. Centrifugo
retains nothing and the derived resting book was empty, so the pipeline was clean. The
mechanism is the gateway's skip rule: it never publishes an empty book, so a cleared book goes
silent rather than saying it is empty. The open tab kept its last frame under a 6px staleness
dot. A red book now fades to 35% and states that the rungs may no longer exist. A related
branch, `fix/red-ladder-rescue`, added a rescue poll first, so a wedged tab heals itself
before the panel blames the venue.

**Repeated defect, worth naming.** The false OVERNIGHT game chip was fixed on 14 August and
returned on 15 August through a different path. The first fix used engine truth only when the
board held nothing; the second made engine LIVE outrank any board row. The commit message for
`28c2068` describes it as "the same precedence defect as the night before, wearing a different
hat".

## Still open

Nothing. All 27 branches touched in the window merged into `origin/main`. There is no unmerged
work in this repository for this week.

Two things are finished in the panel but blocked outside it, and they are worth tracking:

- **The manual order ticket cannot be used yet.** The deployed taker understands only halt,
  resume and state on its control subject. The whole manual-order command family is engine
  code in engine PR #23 and is undeployed. `1d01cab` changed the disabled ticket's message to
  say exactly that. It also states what is not missing: the panel-side key is set and the bus
  grants are in.
- **Win probability is cut from this build.** The SportRadar Probabilities package is not
  entitled, so the stream is not on the bus. `6f524e7` removed it with no placeholder and no
  staleness badge, because a staleness badge implies a feed that runs late.

## Commit appendix

Grouped by branch, newest branch first. Each group ends with its merge commit into
`origin/main`.

### `feat/taker-last-trade` → PR #29

`1996a8d` · `2026-08-15` · `westy412` · panel+proxy: when each taker book last traded
`ced00d4` · `2026-08-15` · `westy412` · Merge pull request #29 from Novosapien/feat/taker-last-trade

### `perf/house-render` → PR #28

`e36565f` · `2026-08-15` · `westy412` · panel: stop the house pages re-rendering 180 rows twice a second
`d02591c` · `2026-08-15` · `westy412` · Merge pull request #28 from Novosapien/perf/house-render

### `fix/state-colour-semantics` → PR #27

`e9e78be` · `2026-08-15` · `westy412` · panel: one colour vocabulary for both state ladders
`c04e64a` · `2026-08-15` · `westy412` · Merge pull request #27 from Novosapien/fix/state-colour-semantics

### `fix/taker-dead-sort-chip` → PR #26

`b421fad` · `2026-08-15` · `westy412` · panel: hide the Spread sort on the taker — it ranked nothing
`bd8fb62` · `2026-08-15` · `westy412` · Merge pull request #26 from Novosapien/fix/taker-dead-sort-chip

### `feat/positions-filters` → PR #25

`95f7a15` · `2026-08-15` · `westy412` · panel: filters and sorting on both position tables
`87129c5` · `2026-08-15` · `westy412` · Merge pull request #25 from Novosapien/feat/positions-filters

### `fix/engine-live-outranks-schedule` → PR #24

`28c2068` · `2026-08-15` · `westy412` · panel: engine LIVE outranks a stale schedule row
`672d0ea` · `2026-08-15` · `westy412` · Merge pull request #24 from Novosapien/fix/engine-live-outranks-schedule

### `feat/maker-flow-tiles` → PR #23

`f6e8c1b` · `2026-08-15` · `westy412` · panel: today's order flow on the maker's engine strip
`6a80e2f` · `2026-08-15` · `westy412` · Merge pull request #23 from Novosapien/feat/maker-flow-tiles

### `fix/game-chip-engine-truth` → PR #22

`698e4f0` · `2026-08-15` · `westy412` · panel: the engine's phase outranks a dark SR cache
`d9d4713` · `2026-08-15` · `westy412` · Merge pull request #22 from Novosapien/fix/game-chip-engine-truth

### `feat/viewer-house-readonly` → PR #21

`2b8d7a2` · `2026-08-14` · `westy412` · panel+proxy: house cockpit read-only for viewer
`1e27928` · `2026-08-14` · `westy412` · Merge pull request #21 from Novosapien/feat/viewer-house-readonly

### `feat/maker-liveness-recipe` → PR #20

`ad8fda1` · `2026-08-14` · `westy412` · panel: the maker liveness recipe — global banner, shed truth, fetch resilience
`3cc832d` · `2026-08-14` · `westy412` · Merge pull request #20 from Novosapien/feat/maker-liveness-recipe

### `feat/pricing-vs-quoting` → PR #19

`0ea42f9` · `2026-08-14` · `westy412` · panel: pricing vs quoting, side by side on the maker
`68bd4af` · `2026-08-14` · `westy412` · Merge pull request #19 from Novosapien/feat/pricing-vs-quoting

### `fix/pre-kickoff-window` → PR #18

`7cc28f6` · `2026-08-13` · `westy412` · panel: PRE-KICKOFF only inside the engine's 60-minute window
`1f72848` · `2026-08-13` · `westy412` · Merge pull request #18 from Novosapien/fix/pre-kickoff-window

### `feat/maker-game-phase` → PR #17

`826e44b` · `2026-08-13` · `westy412` · panel: a Game column on the maker's positions — kickoff, LIVE, FINAL, OVERNIGHT
`eeb5803` · `2026-08-13` · `westy412` · Merge pull request #17 from Novosapien/feat/maker-game-phase

### `feat/market-state-column` → PR #16

`5afaa15` · `2026-08-13` · `westy412` · panel: a Market state column that explains its ladder
`1616efc` · `2026-08-13` · `westy412` · Merge pull request #16 from Novosapien/feat/market-state-column

### `fix/engine-tiles-and-sort` → PR #15

`e28543c` · `2026-08-13` · `westy412` · panel: engine tiles in plain English; league-order positions and holdings
`b79cf11` · `2026-08-13` · `westy412` · Merge pull request #15 from Novosapien/fix/engine-tiles-and-sort

### `fix/engine-view-design` → PR #14

`e84da82` · `2026-08-13` · `westy412` · panel: the engine's first live render gets the reviewed design
`59b92b6` · `2026-08-13` · `westy412` · Merge pull request #14 from Novosapien/fix/engine-view-design

### `feat/manual-history` → PR #13

`7c88c4d` · `2026-08-13` · `westy412` · panel+proxy: manual-order command history
`ab50683` · `2026-08-13` · `westy412` · Merge pull request #13 from Novosapien/feat/manual-history

### `fix/ticket-double-send` → PR #12

`24096f4` · `2026-08-13` · `westy412` · panel: leaving the confirm step is part of the send
`1d7f8eb` · `2026-08-13` · `westy412` · Merge pull request #12 from Novosapien/fix/ticket-double-send

### `feat/ticket-quick-chips` → PR #11

`bbdf9d1` · `2026-08-13` · `westy412` · panel: the app's quick-fill chips on the manual-order ticket
`0415b23` · `2026-08-13` · `westy412` · Merge pull request #11 from Novosapien/feat/ticket-quick-chips

### `feat/ticket-ux` → PR #10

`02354bb` · `2026-08-13` · `westy412` · panel: the ticket searches by team and prices against the live book
`4d5c771` · `2026-08-13` · `westy412` · Merge pull request #10 from Novosapien/feat/ticket-ux

### `fix/positions-pull-consumer` → PR #9

`b0afeed` · `2026-08-13` · `westy412` · proxy: the POSITIONS replay stalled on flow control — pull, don't push
`02f9df4` · `2026-08-13` · `westy412` · Merge pull request #9 from Novosapien/fix/positions-pull-consumer

### `fix/red-ladder-rescue` → PR #8

`16e09eb` · `2026-08-13` · `westy412` · panel: rescue-poll a red book instead of blaming the venue
`83c716a` · `2026-08-13` · `westy412` · Merge pull request #8 from Novosapien/fix/red-ladder-rescue

### `fix/game-board-performance` → PR #7

`ea42188` · `2026-08-13` · `westy412` · proxy: the game board took 41 seconds and showed nothing
`8548e19` · `2026-08-13` · `westy412` · Merge pull request #7 from Novosapien/fix/game-board-performance

### `feat/game-status-board` → PR #6

`06a3d8f` · `2026-08-13` · `westy412` · panel+proxy: a Game column on the market-data board
`71cfa59` · `2026-08-13` · `westy412` · Merge pull request #6 from Novosapien/feat/game-status-board

### `feat/trading-observability` → PR #5

`11a6c5e` · `2026-08-13` · `westy412` · panel: a dead book must not look alive
`1d01cab` · `2026-08-13` · `westy412` · panel: manual orders — name the real blocker
`a5ccc2a` · `2026-08-13` · `westy412` · panel: every tile says its window, and explains itself on a click
`7121607` · `2026-08-13` · `westy412` · panel+proxy: plain-English metric tiles, windowed to today
`b78e129` · `2026-08-13` · `westy412` · panel: taker order log, and metric tiles that work without the engine
`660dc31` · `2026-08-13` · `westy412` · panel+proxy: Positions and Holdings from the venue's own position stream
`743e65f` · `2026-08-13` · `westy412` · panel+proxy: the derived book was full of ghosts — every replace minted one
`db72d8a` · `2026-08-13` · `westy412` · panel+proxy: seed the house surfaces from the pump's accumulation
`f213828` · `2026-08-12` · `westy412` · panel: open the house pages on a tab that has data
`0328f28` · `2026-08-12` · `westy412` · panel: the drawer's depth bars grew the wrong way, and ten pins
`8c6541a` · `2026-08-12` · `westy412` · panel: read the drawer ladder from the centre out, and hold six pins
`34683d0` · `2026-08-12` · `westy412` · panel: a one-sided quote update was blanking the other side of the row
`4473cad` · `2026-08-12` · `westy412` · panel: league sort and filters, and stop the tables reshuffling under the cursor
`b3fa83d` · `2026-08-12` · `westy412` · panel: "Levels" was the order count, not the price levels
`bbe70de` · `2026-08-12` · `westy412` · panel: rebuild the maker's live quotes from the order feed
`a22f8b3` · `2026-08-12` · `westy412` · panel: the tape was calling a working market maker a wall of failures
`78011ea` · `2026-08-12` · `westy412` · panel: give Emotion a server-insertion registry, and stop the banner overclaiming
`6b87ba4` · `2026-08-12` · `westy412` · panel: fix the pump-health parser, which has never matched the payload
`d516111` · `2026-08-12` · `westy412` · panel: use the pump's other subjects as the control for a silent one
`820e8d2` · `2026-08-12` · `westy412` · panel: stop the house pages reporting a live engine as dead
`718d368` · `2026-08-12` · `westy412` · panel: delete the synthetic-data mode entirely
`c46c219` · `2026-08-12` · `westy412` · panel: make the dev fixtures match reality, and stop them lying
`70550ac` · `2026-08-12` · `westy412` · panel: full depth in the rail, and pin both chrome columns to the viewport
`4233b15` · `2026-08-12` · `westy412` · panel: split the cockpit per engine, add metrics and tabs
`c341eaa` · `2026-08-12` · `westy412` · panel+proxy: stream the symbol table, and say which transport is in use
`3db4cb7` · `2026-08-12` · `westy412` · panel: derive the house:fills fixture from the pump's source, not the spec
`67dd014` · `2026-08-12` · `westy412` · proxy: report publish_ok as null on every path, never false
`890abce` · `2026-08-12` · `westy412` · proxy: F2 connectivity guard on the refusal proof + subscribe-only grant check
`c58fe96` · `2026-08-12` · `westy412` · panel: the five mediums — each one an over-claim
`f1f83b7` · `2026-08-12` · `westy412` · panel: H6, H7, H8 — three surfaces that stated more than they knew
`31dc2ae` · `2026-08-12` · `westy412` · panel: one resolution rule for H4, H5 and C3 — never answer what the snapshot cannot
`b018dd7` · `2026-08-12` · `westy412` · proxy: Phase-2 review — 3 criticals, 2 highs, 6 mediums
`508c603` · `2026-08-12` · `westy412` · panel: Phase-2/3 review — C1, C2, C3
`ecefd2a` · `2026-08-12` · `westy412` · panel: cancelling an unknown row does not always clear it
`760f087` · `2026-08-12` · `westy412` · panel: announce the taker's shed on the cockpit, not just the maker's
`f14f280` · `2026-08-12` · `westy412` · panel: reconcile with engine's final contract; give submit_refused its action
`c7816b8` · `2026-08-12` · `westy412` · panel: the taker's shed contract — an absent order list is not an empty one
`ade299a` · `2026-08-12` · `westy412` · proxy: cover the engine's three submission outcomes + taker shed
`368ad91` · `2026-08-12` · `westy412` · panel: distinguish a non-binding collar from the ruled no-book fallback
`8f9c858` · `2026-08-12` · `westy412` · panel: make cancel read as the safe action on an unconfirmed row
`5076937` · `2026-08-12` · `westy412` · panel: the `unknown` submission state (EC18/EC19)
`34be335` · `2026-08-12` · `westy412` · panel: fix three criticals and three mediums from the Phase-1 review
`47edc34` · `2026-08-12` · `westy412` · panel: role gating sweep (R13) — extract the rules, prove them
`c4b587b` · `2026-08-12` · `westy412` · panel: house-agents cockpit (R9)
`0a5091c` · `2026-08-12` · `westy412` · panel: correct the game-resolution contract — switch on `state`, not status
`edcf264` · `2026-08-12` · `westy412` · proxy: refixture against the engine's final payloads (N36 + real shed)
`1899077` · `2026-08-12` · `westy412` · panel: manual taker order ticket (R12)
`6a1ca97` · `2026-08-12` · `westy412` · proxy: make the control-grant check real by reading last_error
`43c0cd9` · `2026-08-12` · `westy412` · proxy: game-context resolver, control-grant assertion, N36 fixture
`4312fe0` · `2026-08-12` · `westy412` · panel: live game context via the proxy resolver (R10)
`6f524e7` · `2026-08-12` · `westy412` · panel: drop win probability from the game context panel
`c84d25d` · `2026-08-12` · `westy412` · proxy: manual-order routes for the taker account (R7)
`bf3d328` · `2026-08-12` · `westy412` · panel: viewer allowlist — book depth + realtime tokens (WE9, pulled from #14)
`17fde29` · `2026-08-12` · `westy412` · panel: preserve the connection identity across a token refresh
`3e03af6` · `2026-08-12` · `westy412` · proxy: singleton always-on instance config for the pump (R5)
`6ede553` · `2026-08-12` · `westy412` · panel: market-data View page — ladder, venue tape, supply, sparkline (R10 part)
`41096fd` · `2026-08-12` · `westy412` · proxy: reusable connection sub + per-subject inbound clocks
`ac711f3` · `2026-08-12` · `westy412` · panel: pinned sidebar rail (R11) + env docs + honest upstream-silent flag
`ac90940` · `2026-08-12` · `westy412` · proxy: pump hardened against the measured frame + engine's real payloads
`be54243` · `2026-08-12` · `westy412` · panel: align the live-data layer to the verified node + amended contracts
`f9cf2e0` · `2026-08-12` · `westy412` · proxy: bind the per-service NATS credentials (fixes Authorization Violation)
`88ef064` · `2026-08-12` · `westy412` · panel: live-data layer — shared client, ref-counted registry, staleness (R8)
`ba96ded` · `2026-08-12` · `westy412` · proxy: NATS->Centrifugo house pump, disabled by default (R5)
`1a6e9d7` · `2026-08-12` · `westy412` · proxy: Centrifugo token routes + house state fallback (R6)
`1e4bac4` · `2026-08-13` · `westy412` · Merge pull request #5 from Novosapien/feat/trading-observability

### `fix/book-test-symbols` → PR #4

`89b4cc0` · `2026-08-10` · `westy412` · fix(proxy): accept .TEST symbols on /market/book
`c2dd38d` · `2026-08-10` · `westy412` · Merge pull request #4 from Novosapien/fix/book-test-symbols

### `feat/test-symbols` → PR #3

`2cb8cff` · `2026-08-09` · `westy412` · feat: accept and display the 10 venue test symbols (real ticker + .TEST)
`8c0d28c` · `2026-08-10` · `westy412` · Merge pull request #3 from Novosapien/feat/test-symbols
