---
description: "Weekly engineering record for the Sportradar service, 09-16 August 2026: 82 commits, six publisher fixes, and the first two live game nights"
service: inplay-sportradar-service
window: 2026-08-09 .. 2026-08-16
commits: 82
authors: { westy412: 80, Hxsan: 2 }
branches: { touched: 32, merged: 24, open: 5 }
---

# inplay-sportradar-service — week of 09–16 August 2026

> **Delivery:** [[delivery]] · **Week:** [[work-log-2026-08-16]]

## Headline

**Most of the week's work is correctness under live fire.**

- This service is the only part of InPlay that talks to Sportradar
- This week it started to feed the market maker for real
- It survived the first live NFL preseason games on 13 and 15 August
- Ten separate faults were found on real game nights. Each was fixed the same night or
  the next day.
- The service also learned to find live games by itself, instead of a hand-typed game id

## Scope

- **Window:** 2026-08-09 to 2026-08-16
- **Commits:** 82 (westy412 80, Hxsan 2)
- **Branches touched:** 32 — 3 mainline (`main`, `dev`, `testing`) plus 29 working
  branches. Of those 29, 24 merged and 5 are still open.
- **Busiest day:** 2026-08-13 (29 commits)
- **Quiet days:** no commits landed on 09 or 10 August. The week's work starts on
  11 August.

**The repository was live while this log was written.**

- A new branch, `feat/live-timeouts`, appeared during the analysis
- It carries one commit dated 16 August (`0d7d64f`). It is counted and described below.
- A later commit could arrive after this file is written
- The main worktree also holds uncommitted changes to six files
- It also holds an untracked `captures/` directory and `scripts/mm_prob_replay.py`
- Uncommitted work is outside this log's scope

**Where the work landed.**

- `origin/main` has not moved since 11 August. Its tip is `f8c8aef`.
- Everything after that date sits on `origin/dev` and `origin/testing`, which are both at
  `f822ced`
- The 13 and 15 August game nights ran entirely in the testing environment, by George's
  decision (`3acf734`)
- So "merged" in the table below almost always means `origin/dev` and `origin/testing`,
  not production

**A note on remotes.**

- This log reads the refs on disk
- The shared context forbids `git fetch`, so a remote ref could be behind GitHub
- Nothing in the history suggested that, but the reader should know the constraint

---

## What the market-maker publisher is

- Several branches this week start with `mm-`. They all mean one thing.
- The market maker (`inplay-market-maker`) prices 170 team securities
- It needs a live win probability for every game
- Sportradar sells that number. Only this service holds the Sportradar key, the retry
  rules and the 170-team map.
- So this service polls Sportradar and pushes each probability reading onto a NATS
  message bus
- The market maker reads the bus and never calls Sportradar itself
- **The publisher** — the part that does this is a separate worker process,
  `app.workers.mm_publisher`. This document calls it the publisher.
- **Its design** — `docs/mm-probability-publisher.md`

Two facts about the publisher explain most of this week's fixes:

1. **A reading is identified by its timestamp.** The market maker de-duplicates on that
   stamp, so one timestamp must carry exactly one message.
2. **Silence is a signal.** The market maker judges whether a price is fresh from the
   time of the last successful fetch.
   - If the publisher stops sending for a game, the market maker suspends that game's
     book
   - That is correct when the feed is genuinely dead
   - It is wrong when the publisher simply stopped for a bad reason

---

## Themes

### 1. The publisher reached production, then took six correctness fixes

**Why it matters** — the publisher is the market maker's only source of a live win
probability. A wrong reading becomes a wrong price.

**`feat/mm-probability-publisher`** · merge `89e8456` · merged `origin/main`
- **What** — the publisher's code, written on 6 August, reached `origin/main` on
  11 August

**`feat/mm-publisher-deploy`** · `c7a7018` · merged `origin/main`
- **What** — on 11 August, the same day, the publisher got its own Cloud Run worker pool
  and a third deploy step

**`fix/terraform-stitch`** · `99e551b`, `b7c6f18` · merged `origin/dev`, `origin/testing`
- **Symptom** — the Terraform file was broken. The new pool was missing
  `PROBABILITIES_API_KEY` and `REDIS_URL`.
- **Cause** — two parallel merges had left the Terraform file broken
- **Fix** — three infrastructure repairs: two on this branch, and `7138750` directly on
  `dev`

**`feat/live-poll-500ms-real`** · `488d35c` · merged `origin/dev`, `origin/testing`
- **What** — the live poll rate drops to 500 ms
- **Why** — George ruled the rate down

> The branch before it, `feat/live-poll-500ms`, carries a formatting-only commit. See
> **Notable fixes**.

**Then the games started, and the publisher was wrong in six ways.**

**Fix 1 of 6 — `testing-local`** · `daf5604` · merged `origin/dev`, `origin/testing`
- **Symptom** — it adopted no games at all: zero adopted, zero polls, zero readings on
  the bus
- **Cause** — the universe filter compared Sportradar's own competitor ids
  (`sr:competitor:NNNN`) against the league feed's GUIDs
- **Cause** — the two id schemes can never match, so discovery filtered out every game
- **Fix** — an unrecognised Sportradar id now errs on the side of adoption
- **Fix** — the market maker's own bindings decide what it prices
- **Evidence** — George found this live on 13 August, 30 minutes before the first
  preseason slate

> **This one fix exists as three identical patches.**
> - `daf5604` on `testing-local` — the only one on a mainline branch
> - `d877b26` on `hotfix/mm-publisher-universe-filter` — cut from the deployed production
>   SHA, so the API and live worker would not roll forward on game night
> - `da08336` on `fix/mm-publisher-latency`

**Fix 2 of 6 — `fix/mm-discover-tomorrow`** · `66d120b` · merged `origin/dev`,
`origin/testing`
- **Symptom** — prime-time games were discovered at kickoff
- **Symptom** — the pre-kickoff hour the market maker prices its opening book from was
  lost every time
- **Cause** — discovery fetched only today's UTC schedule, but a 20:00 ET game kicks off
  at or after 00:00 UTC
- **Cause** — such a game lives on tomorrow's schedule date, so the publisher found it at
  the date rollover, which is its own kickoff
- **Fix** — fetch both dates on every discovery pass
- **Where it landed** — PR #33

**Fix 3 of 6 — `fix/mm-publisher-latency`** · `434f8c8` · merged `origin/dev`,
`origin/testing`
- **Symptom** — a round of polls took 3.5 seconds instead of 2
- **Cause** — the publisher fetched due games one at a time, at about 0.7 s per
  Sportradar round trip, so four live games stretched every game's real cadence
- **Cause** — it also adopted a CFL fixture that Sportradar never finalled, which sat on
  the live tier forever and burned a fetch slot every round
- **Fix** — the fetches now run concurrently
- **Fix** — discovery drops any fixture that declares a competition other than NFL or
  NCAA
- **Evidence** — the commit records that the remaining lag is Sportradar's own ~10 s
  model latency, which is not reachable from this side
- **Where it landed** — PR #39

**Fix 4 of 6 — `fix/mm-reading-collisions`** · `0ff4fa5` · merged `origin/dev`,
`origin/testing`
- **Symptom** — a second's first reading reached the market maker, not its last
- **Cause** — Sportradar stamps readings to the second, and issues several distinct
  readings inside one second
- **Cause** — the publisher iterated Sportradar's raw order, so it published the first
  reading of each second and dropped every later revision
- **Fix** — collapse each second to its last reading, and publish in stamp order
- **Evidence** — measured across three live games on 15 August: 131 of 1,638 readings
  shared a second with an earlier one
- **Evidence** — the widest such pair was 8.5 probability points apart
- **Evidence** — replayed against the real CAR@BUF timeline, the new path is correct for
  726 of 726 seconds. The old path was superseded on 68.

**Fix 5 of 6 — `fix/mm-reading-collisions`** · `1bf9b2f` · merged `origin/dev`,
`origin/testing`
- **Symptom** — the liveness re-offer kept dead prices alive
- **Cause** — the publisher re-sends the last reading during quiet spells, so the market
  maker's freshness clock keeps ticking
- **Fix** — withhold the re-offer when the reading's scoreline differs from the current
  one **and** the reading is older than `MMPUB_STALE_REOFFER_GRACE_S` (default 120 s)
- **Fix** — both conditions are needed, because either alone is normal
- **Fix** — a withheld re-offer logs a warning
- **Evidence** — on 15 August Sportradar stopped pricing CLE@CHI for 36 minutes mid-game
- **Evidence** — its last reading was computed at 10-7 while the game stood 10-10
- **Evidence** — the market maker held a live book at 46.3% with no signal that anything
  was wrong

**Fix 6 of 6 — `fix/mm-reading-collisions`** · `743b174` · merged `origin/dev`,
`origin/testing`
- **Symptom** — that guard then suspended healthy books
- **Symptom** — CAR@BUF sat at 98.4% for its last 38 minutes, and the new guard suspended
  its book for 20.4% of the game, for nothing
- **Cause** — Sportradar records a probability change only when it exceeds 0.1%, so a
  decided game legitimately stops moving
- **Fix** — skip the withhold when either side of the two-way market is at or beyond
  `MMPUB_DECIDED_PROBABILITY_PCT` (default 98)
- **Evidence** — replayed on the same three games: CLE@CHI suspension fell from 24.7% to
  18.5%
- **Evidence** — MIN@NYG stayed at 0%. CAR@BUF fell from 20.4% to 0%.

> All three `fix/mm-reading-collisions` commits merged via PR #40 (`f822ced`,
> 16 August).

### 2. A finished game must keep reporting

**Why it matters** — the market maker reads silence as a dead feed. A finished game that
stops reporting loses its book.

**`testing-keep-polling`** · `d492dcb` · merged `origin/dev`, `origin/testing`
- **Symptom** — ten books went dark on 14 August, into permanent suspension
- **Cause** — when a game ends, the publisher used to stop polling one hour later
- **Cause** — the market maker judges freshness from successful observations, so that
  silence starved every finished game's book
- **Cause** — the 600 s correction watch before that was also too slow
- **Cause** — it made each book suspend, cancel and re-stand once per poll, against the
  market maker's ~20 s freshness fuse
- **Fix** — the post-game settle watch now polls at the live rate, so no gap is wide
  enough for the fuse to see
- **Fix** — the settle window default doubles to 2 hours, so it outlasts the market
  maker's own activity flip
- **Fix** — past that window the publisher polls at the overnight rate forever, and never
  returns "done"
- **Evidence** — Sportradar serves closed timelines indefinitely, and George ruled that
  quota is not a constraint

> - `fix/mm-publisher-post-game-keep-polling` (`751efb6`) carries the identical patch and
>   is **not merged**
> - `d492dcb` is the one that reached `origin/dev` and `origin/testing`
> - The commit notes that the matching engine-side game-end work stays with the market
>   maker's own N40 item

### 3. The live worker finds its own games, and survives failure

**Why it matters** — a game nobody typed in was a game nobody captured. That is what
happened to the 7 August preseason game.

- **The live worker** (`app.workers.live`) is the other worker in this service
- It reads Sportradar's Push stream and turns it into the play-by-play the app shows
- Until this week it needed `LIVE_GAME_IDS` — a hand-typed list

**`feat/live-worker-discovery`** · `6358bb3` · merged `origin/dev`, `origin/testing`
- **What** — the worker finds live games itself. The hand-typed list is gone.
- **Why** — Sportradar's Push feed sends every in-progress game on one unfiltered
  subscription, and each envelope names its own game
- **Where it landed** — a new `app/workers/multiplex.py` fans that one connection out to
  a pipeline per game, created on first sight

> - Everything downstream is unchanged. An explicit `LIVE_GAME_IDS` still wins.
> - The commit records that this inverts the meaning of an empty list, from "idle" to
>   "capture everything", and updates the runbook's abort step.
> - It also records two defects found but deliberately not fixed there. Both were fixed
>   later in the week — see theme 5 and `fix/reconnect-reconcile` below.

**`feat/live-worker-discovery`** · `d327bee` · merged `origin/dev`, `origin/testing`
- **What** — a rehearsal of the fan-out against two real recorded games, replayed
  interleaved on one stream
- **Evidence** — the strongest assertion is that the interleaved result is
  byte-identical to the NFL game run alone

**`feat/live-worker-discovery`** · `8d066ef` · merged `origin/dev`, `origin/testing`
- **What** — `scripts/watch_live.py` reads each link of the chain separately: the raw
  Sportradar stream, the Centrifugo channel, and the API's own `/live` blob
- **Why** — a game-day operator can then tell which link broke

**`fix/reconnect-reconcile`** · `6a44c89` · merged `origin/dev`, `origin/testing`
- **Symptom** — a dropped connection left a permanent hole in the play list
- **Cause** — Sportradar Push has no replay, so plays that happen while the socket is
  down are gone forever unless a REST catch-up runs
- **Cause** — `GamePipeline.reconcile` implemented that catch-up correctly and had an
  end-to-end test, but **nothing ever called it**
- **Cause** — the push consumer absorbed reconnects inside its own loop, so no code ever
  saw a reconnect boundary
- **Fix** — the consumer announces reconnects, and awaits a hook before the first message
  of any later connection
- **Evidence** — the new tests target the wiring, not the catch-up logic, because a
  behavioural test of the catch-up passed throughout

**`fix/live-worker-hardening`** · `4df15bf` · merged `origin/dev`, `origin/testing`
- **What** — lands every confirmed critical and high finding from an adversarial review,
  run the night before the first real games
- **Symptom** — one bad message killed all games. The process still looked healthy to
  Cloud Run.
- **Symptom** — both instances wrote the Redis blob, although only one was allowed to
  publish
- **Symptom** — a restarted worker republished from sequence 1. That permanently froze
  every viewer's screen until they force-quit the app.
- **Symptom** — a game found by discovery could never end, because Sportradar Push sends
  no status flip
- **Fix** — all four faults are closed. An idle sweep now runs a REST end-check on any
  adopted game quiet for 3 minutes.

**`fix/live-worker-hardening`** · `8047d74` · merged `origin/dev`, `origin/testing`
- **What** — `scripts/validate_live_worker.py` attacks the real binary against a local
  fake Sportradar, including a hard `SIGKILL` mid-game and a restart
- **Evidence** — result: 17 of 17
- **Note** — it is a manual tool, not CI

> Both `fix/live-worker-hardening` commits merged via PR #29.

**Game-day tooling, not shipped code.**

**`chore/gameday-2026-08-13`** · `ce06fa9`, `56ada7c` · merged `origin/dev`,
`origin/testing`
- **What** — a raw-feed recorder added to `watch_live.py`, so the night's data survives
  even if every deployed component fails
- **Why** — the parsed model loses data when it is written: 25 keys in, 11 out on a real
  fixture
- **Fix** — `PushStreamDecoder` gained `feed_with_raw()`, and the recorder writes the
  verbatim wire dict
- **Note** — the branch added a game-day plan document, then deleted it in `56ada7c` on
  George's call. The recorder and the decoder fix stayed.

**`chore/testing-real-feed`** · `3acf734` · merged `origin/dev`, `origin/testing`
- **What** — Terraform only. It pointed the testing worker at the real Sportradar feed,
  turned discovery on, and raised the worker to two instances.

**`local/replay-sandbox`** · **open**
- **What** — a local worktree. It is **not merged**.

**In flight on 16 August.**

**`feat/live-timeouts`** · `0d7d64f` · **open**
- **What** — `homeTimeoutsRemaining` and `awayTimeoutsRemaining` on the live snapshot and
  on the `op:tick` delta
- **Why** — Sportradar sends `remaining_timeouts` on every push message, in the same
  `payload.game.summary` block the worker already reads
- **Why** — so this needs no timeout counting, no Redis persistence and no boxscore poll
- **Why** — the app-side scoping had assumed all three
- **Evidence** — a replay of the recorded feeds proves it: 197 NFL and 79 NCAA deltas
  carry timeouts on every one, with zero nulls
- **Note** — the fields are optional, so the contract version stays at 1
- **Note** — they are retained from the previous snapshot when a partial header omits
  them, and never defaulted to 3
- **Where it landed** — nowhere. The branch is **open** and sits on top of
  `local/replay-sandbox`.

### 4. Win-probability readings reach the app, not only the market maker

**Why it matters** — one entitled Sportradar fetch can serve two consumers. The app then
shows the same reading the market maker prices from.

**`testing` direct commit** · `7f30fc4` · on `testing`
- **What** — the live worker gains an optional feed
- **What** — the feed tails the publisher's readings on NATS, and maps each Sportradar
  event id to its league game
- **What** — it publishes `homeWinProb` on the existing `game:{id}` channel as an
  `op:tick` delta
- **Note** — the feed is off unless `LIVE_WINPROB_NATS_URL` is set. With it empty the
  worker behaves exactly as before.

**`testing` direct commit** · `fa0a6d3` · on `testing`
- **What** — wires the environment into the testing deploy

**`fix/winprob-feed-hardening`** · `6e6e5ec` · merged `testing` (`952d8be`), then
`origin/dev` and `origin/testing`
- **Symptom** — on go-live, 15 August, it did not work
- **Symptom** — the feed idled behind a healthy-looking `winprob_feed_subscribed` log
  line, and the app's win-probability bar stayed at its pre-game value
- **Cause** — the service's NATS user held publish rights on `sr.probabilities.>` but no
  subscribe grant, so the server refused the subscription
- **Cause** — the `nats.py` client reports that refusal on an asynchronous error
  callback. It still returns a subscription object that looks alive.
- **Fix** — wire the error callback into the read loop, so any server error tears the
  connection down and the retry loop re-logs the cause
- **Fix** — log every applied reading and every unmapped event
- **Fix** — redact the NATS credential from the log, and record the required grant

> **The grant itself is not a repository change.**
> - A person applied it by hand on the `inplay-nats` host by `SIGHUP`
> - The backup is at `nats.conf.bak-winprob-sub-20260815`
> - That is a live-host change

### 5. Cache lifetimes derived from the fetched game

**Why it matters** — a wrong cache lifetime freezes a partial play list for a month, or
hides a live game behind a 404.

- The service caches Sportradar responses in Redis
- A cache lifetime had to be chosen before the fetch
- Whether a game is final is a property of the response
- That mismatch produced three faults, none of which is visible in a response body

**`fix/live-cache-ttls`** · `c0d4114` · merged `origin/dev`, `origin/testing`
- **Symptom** — the first read taken during a game froze a partial play list for a month
- **Cause** — `get_play_by_play` applied the 30-day archival lifetime unconditionally,
  and two live paths call it mid-game
- **Symptom** — `/live` returned 404 well into the game it exists to cover
- **Cause** — `get_boxscore` always used the one-hour pre-game lifetime, and the `/live`
  endpoint decides liveness from that cached status
- **Fix** — `get_or_set` accepts a lifetime that is a function of the fetched value,
  resolved once on the leader before write-back
- **Fix** — play-by-play: 30 days when final, 30 s otherwise
- **Fix** — boxscore: 30 days when final, 30 s when live or past kickoff, one hour when
  scheduled
- **Fix** — the scheduled case is clamped, so the key cannot outlive kickoff
- **Fix** — the same commit removes a duplicated `LIVE_STATUSES` set that existed
  byte-identical in two files

**`fix/final-settling-ttls`** · `b8b5560` · merged `origin/dev`, `origin/testing`
- **Symptom** — the same bug class on `/statistics`, plus a step the first fix missed
- **Cause** — a game that has just gone final is not immutable. Sportradar pushes stat
  and scoring corrections after the whistle.
- **Fix** — final blobs within 12 hours of kickoff now re-check every 15 minutes, before
  they graduate to the 30-day archival lifetime
- **Evidence** — cost is at most one Sportradar call per blob per 15 minutes per
  instance, and only while someone reads it
- **Where it landed** — PR #35

### 6. The app-facing API: preseason schedule, the game page, and access roles

**Why it matters** — the app's Discover tabs, team page and game page all read this API.
A schedule the API cannot express is a screen the user cannot see.

**`feat/preseason-schedule`** · `ffea38f` · merged `origin/dev`, `origin/testing`
- **Symptom** — during the 2026 preseason, `GET /sr/games` served one closed game and
  nothing upcoming
- **Cause** — it followed Sportradar's `current_week` pointer, and Sportradar advances
  that pointer only once the next week's games are published
- **Fix** — derive the served week: take the most recent week holding a result, and union
  it with the next week holding unplayed games
- **Fix** — the derivation rolls PRE → REG → PST, and then into the next published season
  year

**`feat/preseason-schedule`** · `dd70e80` · merged `origin/dev`, `origin/testing`
- **Fix** — `limit` becomes nullable, so an omitted page size serves the whole union
- **Cause** — without that change, an NCAA union of about 284 games filled page 1 with
  last week's finals
- **Cause** — every app call site calls `useGames(league)` bare and never follows the
  cursor, so those fixtures would never have been seen
- **Note** — this is a public OpenAPI contract change, and the parameter description says
  so

**`feat/preseason-schedule`** · `cc99cbe` · merged `origin/dev`, `origin/testing`
- **Fix** — `season_type` becomes expressible, and week 0 becomes reachable

**`feat/preseason-schedule`** · `80be12f` · merged `origin/dev`, `origin/testing`
- **Fix** — adds an `SR_SEASON_TYPE` override
- **Fix** — returns a typed 404 for NCAA preseason, because NCAA football has no
  preseason and a 502 would be retried forever
- **Fix** — retires the `schedule_current_week` cache key

**`feat/preseason-schedule`** · `7510f4a` · merged `origin/dev`, `origin/testing`
- **What** — completes the edge-case matrix
- **What** — adds a `conftest` guard that fails any test escaping to live Sportradar

**`feat/schedule-multi-phase`** · `6bf8ec7` · merged `origin/dev`, `origin/testing`
- **Symptom** — the app's team page made 18 requests where 6 were needed, which starved
  the page's other calls of connections
- **Fix** — `/sr/schedule` serves a whole season year in one request
- **Fix** — phases are fetched concurrently and merged in calendar order
- **Note** — an omitted `season_type` still means REG, deliberately

**`fix/unpublished-phase-empty`** · `597033e` · merged `origin/dev`, `origin/testing`
- **Symptom** — the night the preseason build reached the testing app, both Discover tabs
  hung
- **Cause** — the app asked for NCAA 2026 `season_type=PST`, a postseason Sportradar has
  not published
- **Cause** — the service turned Sportradar's 404 into a 502, and the app treats 5xx as
  transient and retried in a loop
- **Fix** — an unpublished phase is now an empty page
- **Fix** — a genuine 5xx, 429 or timeout still propagates

**`feat/game-aggregate`** · `856190a` · merged `origin/dev`, `origin/testing`
- **What** — `GET /sr/games/{id}/aggregate` answers a game page in one call, instead of
  about 30 requests
- **Symptom** — all 14 depth-chart calls on the testing game page returned 404
- **Cause** — the default context was hardcoded to REG week 1
- **Fix** — the same commit fixes depth charts
- **Fix** — it also moves the win-probability bulk fallback onto the derived `/sr/games`
  union, so the fallback prices preseason games

**`feat/role-tiers`** · `ecf3332` · merged `origin/main`
- **Author** — Hasan's two commits are `feat/role-tiers` (`ecf3332`)
- **Where it landed** — the only work that reached `origin/main` after 11 August
- **Symptom** — the `trader` role gated both reading sports data and trading, so an
  unverified user could not see a team page or a chart
- **Fix** — this service's edge now answers only "may you read sports data"
- **Fix** — it accepts three tiers: `preview`, `trader-lite` and `trader`
- **Fix** — trading eligibility moves to the trading service
- **Note** — `trader` keeps its exact key and meaning, so no user needs a re-grant

---

## Branches

Merged branches reached `origin/dev` and `origin/testing` unless the row says otherwise.
`origin/main` last moved on 11 August.

| Branch | Author | Commits | Merged into | Purpose |
|---|---|---|---|---|
| `feat/preseason-schedule` | westy412 | 5 | `origin/dev`, `origin/testing` | Derive the served schedule week from game status; make season type expressible. |
| `feat/live-worker-discovery` | westy412 | 3 | `origin/dev`, `origin/testing` | Find live games from one unfiltered Sportradar Push stream. |
| `fix/mm-reading-collisions` | westy412 | 3 | `origin/dev`, `origin/testing` | Publish a second's last reading; withhold the re-offer on a stale undecided book. |
| `fix/terraform-stitch` | westy412 | 3 | `origin/dev`, `origin/testing` | Repair the double-merged Terraform; align the two publisher pools. |
| `fix/live-worker-hardening` | westy412 | 2 | `origin/dev`, `origin/testing` | Land the pre-go-live review findings; add the live-fire harness. |
| `chore/gameday-2026-08-13` | westy412 | 2 | `origin/dev`, `origin/testing` | Record the raw push feed verbatim. The plan doc was added, then deleted. |
| `merge/testing-into-dev` | westy412 | 2 | `origin/dev`, `origin/testing` | Reconcile the win-probability bulk fallback into `dev`. |
| `fix/mm-publisher-latency` | westy412 | 2 | `origin/dev`, `origin/testing` | Concurrent timeline fetches; drop non-NFL/NCAA fixtures at discovery. |
| `merge/main-into-dev` | westy412 | 2 | `origin/main`, `origin/dev`, `origin/testing` | Reconcile the parallel NCAA/season fixes with the publisher infrastructure. |
| `feat/mm-publisher-deploy` | westy412 | 1 | `origin/main`, `origin/dev`, `origin/testing` | The publisher's Cloud Run worker pool and the third deploy step. |
| `feat/mm-probability-publisher` | westy412 | 1 (merge only) | `origin/main`, `origin/dev`, `origin/testing` | **Older branch.** Code written 6 Aug; merged into `dev` on 11 Aug. |
| `feat/role-tiers` | Hxsan | 1 | `origin/main`, `origin/dev`, `origin/testing` | Split data access from trading eligibility. |
| `feat/live-poll-500ms` | westy412 | 1 | `origin/dev`, `origin/testing` | Labelled 500 ms, but the commit is formatting only. See Notable fixes. |
| `feat/live-poll-500ms-real` | westy412 | 1 | `origin/dev`, `origin/testing` | The real 500 ms live poll rate on both pools. |
| `fix/live-cache-ttls` | westy412 | 1 | `origin/dev`, `origin/testing` | Derive play-by-play and boxscore cache lifetimes from the fetched game. |
| `fix/reconnect-reconcile` | westy412 | 1 | `origin/dev`, `origin/testing` | Actually call the REST catch-up when the push socket drops. |
| `fix/unpublished-phase-empty` | westy412 | 1 | `origin/dev`, `origin/testing` | An unpublished season phase is an empty page, not a 502. |
| `chore/testing-real-feed` | westy412 | 1 | `origin/dev`, `origin/testing` | Point the testing worker at the real Sportradar feed for go-live. |
| `feat/game-aggregate` | westy412 | 1 | `origin/dev`, `origin/testing` | One-call game page; depth-chart and preseason win-probability fixes. |
| `fix/mm-discover-tomorrow` | westy412 | 1 | `origin/dev`, `origin/testing` | Discover tomorrow's UTC date, restoring the pre-kickoff ramp. |
| `fix/final-settling-ttls` | westy412 | 1 | `origin/dev`, `origin/testing` | A freshly final game settles for 12 h before it archives. |
| `testing-local` | westy412 | 1 | `origin/dev`, `origin/testing` | The universe-filter fix that actually landed. Same patch as the hotfix branch. |
| `testing-keep-polling` | westy412 | 1 | `origin/dev`, `origin/testing` | The keep-polling fix that actually landed. Same patch as the `fix/` branch. |
| `testing-promote` | westy412 | 1 (merge only) | `origin/dev`, `origin/testing` | Promote the publisher latency fixes from `dev` to `testing`. |
| `testing` | westy412 | 2 direct + 9 merges | mainline | The win-probability feed and its testing deploy were committed here directly. |
| `dev` | westy412 | 1 direct + 23 merges | mainline | Integration branch. `7138750` was committed here directly. |
| `main` | Hxsan, westy412 | 2 merges | mainline | Last moved 11 Aug at `f8c8aef`. |
| `hotfix/mm-publisher-universe-filter` | westy412 | 1 | **open** | Same patch as `testing-local`. Cut from the deployed production SHA. |
| `fix/mm-publisher-post-game-keep-polling` | westy412 | 1 | **open** | Same patch as `testing-keep-polling`. |
| `local/replay-sandbox` | westy412 | 1 | **open** | Local worktree. Same patch as `7f30fc4` on `testing`. |
| `feat/schedule-multi-phase` | westy412 | 2 | **partly** — `6bf8ec7` reached `origin/dev` and `origin/testing`; tip `b0e16f9` is open | Serve a whole season year in one request. |
| `feat/live-timeouts` | westy412 | 1 | **open** | Carry timeouts remaining on the live snapshot and delta. New on 16 Aug. |

- **`feat/ipo-data-domains` and `feat/ipo-data-domains-pr-a`** were named as candidates in
  the brief
- Both branches last moved on 3 and 4 July 2026
- Neither has a commit in this window, so there is no IPO data-domains work to report

---

## Notable fixes and incidents

**The universe filter adopted nothing (13 August)**
- **Symptom** — zero games adopted, zero polls, zero readings on the bus, 30 minutes
  before the first real preseason slate
- **Cause** — the probabilities schedule keys competitors on `sr:competitor:NNNN`.
  `TEAM_SYMBOLS` keys on league-feed GUIDs.
- **Cause** — the membership test could never match
- **Fix** — an unrecognised Sportradar id now errs on the side of adoption
- **Evidence** — the commit records that the fault was found live. It does not record a
  post-fix measurement.
- **Note** — the branch was cut from the deployed production SHA `f8c8aef`, not from
  `main`, so the API and live worker would not roll forward on game night
- **Landed as** — `daf5604`

**The market maker held a live book on a dead probability (15 August)**
- **Symptom** — Sportradar stopped pricing CLE@CHI for 36 minutes mid-game
- **Symptom** — its last reading was computed at 10-7 while the game stood 10-10
- **Symptom** — the market maker showed home 46.3% and no signal that anything was wrong
- **Cause** — the publisher's liveness re-offer refreshes the market maker's freshness
  clock
- **Cause** — it defeated the market maker's own dead-feed protection at the exact moment
  that protection was needed
- **Fix** — withhold the re-offer on a stale reading whose scoreline no longer matches
- **Evidence** — replayed against the real CLE@CHI outage: re-offers continue for the
  first 2 minutes, then withhold from 5 minutes on
- **Landed as** — `1bf9b2f`, corrected by `743b174`

**Ten finished games' books went dark (14 August)**
- **Symptom** — every finished game's book entered permanent suspension
- **Cause** — the publisher's poll clock returned "done for good" one hour after a game
  ended, and the market maker reads that silence as a dead feed
- **Fix** — poll a finished game at the live rate for 2 hours, then at the overnight rate
  forever
- **Evidence** — the commit cites the market maker vault's N40 forensics. It does not
  claim a live re-test.
- **Landed as** — `d492dcb`

**Both Discover tabs hung in the testing app (13 August)**
- **Symptom** — both Discover tabs sat on their spinners
- **Cause** — the app asked for NCAA 2026 `season_type=PST`, which Sportradar has not
  published, and the service returned a 502
- **Cause** — the app retried the 5xx in a loop
- **Fix** — an unpublished phase returns an empty page
- **Evidence** — the commit states the exact stuck request now returns
  `{"data":[],"has_more":false}` in 0.5 s against live Sportradar
- **Landed as** — `597033e`

**The win-probability feed was silently refused (15 August)**
- **Symptom** — the app's win-probability bar stayed at its pre-game value while the
  worker logged a healthy `winprob_feed_subscribed` line
- **Cause** — the NATS user had publish but not subscribe rights
- **Cause** — `nats.py` reports a refused subscription only on an asynchronous callback
  that was not wired up
- **Fix** — wire the error callback into the read loop, and log every applied reading
- **Fix** — grant subscribe on the NATS host
- **Landed as** — `6e6e5ec`

> **Caveat — the NATS grant is not in this repository.**
> - A person applied it by hand with `SIGHUP` on the `inplay-nats` host
> - The backup is at `nats.conf.bak-winprob-sub-20260815`

**A reconnect feature that was never called**
- **Symptom** — every dropped socket left a permanent hole in the play list
- **Cause** — `GamePipeline.reconcile` existed, was covered by an end-to-end test, and no
  production path ever invoked it
- **Evidence** — `grep -rn "\.reconcile(" src/` returned nothing. Every test passed.
- **Landed as** — `6a44c89`

**A commit whose subject does not match its diff**
- **Symptom** — `e0204cf` on `feat/live-poll-500ms` is titled "LIVE poll at 500 ms"
- **Cause** — its diff is whitespace alignment in `terraform.prod.tfvars` only
- **Fix** — the real change is `488d35c` on `feat/live-poll-500ms-real`, which sets
  `MMPUB_POLL_LIVE_S = "0.5"` on both the production and testing pools
- **Evidence** — `488d35c`'s own body says so
- **Note** — both branches merged, so the setting is in place

**Four fixes exist as duplicate patches on several branches**
- **Evidence** — verified by `git patch-id`, these pairs and triples are byte-identical:
  - `d877b26` = `daf5604` = `da08336`
  - `751efb6` = `d492dcb`
  - `7f30fc4` = `0cecdd7`
  - `b0e16f9` = `597033e`
- **Note** — this is a working pattern, not a contradiction. The fix was cut against the
  deployed SHA for a live hotfix, and re-applied on a mainline-based branch.
- **Note** — no fix was reverted and reapplied this week

---

## Still open

- **Five branches are unmerged.**
- Four of them are duplicates of a patch that reached a mainline branch, confirmed by
  `git patch-id`, so no work is lost there
- The fifth, `feat/live-timeouts`, is genuinely new and in flight

| Branch | Last commit | State | What is left |
|---|---|---|---|
| `feat/live-timeouts` | 2026-08-16 (`0d7d64f`) | **In flight.** | New work, created on 16 August while this log was written. It is the checked-out branch in the main worktree, has no remote ref, and is based on `local/replay-sandbox` rather than a mainline branch. It needs rebasing onto `dev` and a PR. |
| `hotfix/mm-publisher-universe-filter` | 2026-08-13 (`d877b26`) | **Superseded, safe to delete.** | Identical to `daf5604`, which is on `origin/dev` and `origin/testing`. It was cut from the deployed production SHA for a game-night hotfix. |
| `fix/mm-publisher-post-game-keep-polling` | 2026-08-14 (`751efb6`) | **Superseded, safe to delete.** | Identical to `d492dcb`, which is on `origin/dev` and `origin/testing`. |
| `local/replay-sandbox` | 2026-08-14 (`0cecdd7`) | **Local sandbox.** | It has no remote ref. Its one commit is identical to `7f30fc4` on `testing`. Nothing is pending on the commit itself, but `feat/live-timeouts` now branches off it. |
| `feat/schedule-multi-phase` | 2026-08-13 (`b0e16f9`) | **Partly merged.** | `6bf8ec7` merged via PR #24. The tip `b0e16f9` did not, but it is identical to `597033e`, which merged via PR #26. Nothing is pending. |

**The wider gap is `origin/main`.**

- Every change from 12 August onward sits on `origin/dev` and `origin/testing` only
- That covers the live worker discovery and hardening, and all six publisher correctness
  fixes
- It also covers the cache-lifetime work, the whole preseason schedule change and the
  win-probability feed
- The gap was deliberate for the 13 August go-live, which ran entirely in testing
- It is a decision to revisit, not a fault

**Twelve other directories are worktrees of this one repository.**

- Nine are under `/private/tmp/claude-501/`. They hold branches that were worked on in
  parallel and are all merged.
- The main path itself is on `feat/live-timeouts`
- Three worktrees are siblings of the main path:
  - `inplay-sportradar-hotfix` (`hotfix/mm-publisher-universe-filter`)
  - `inplay-sportradar-testing-fix` (`testing-local`)
  - `inplay-sportradar-winprob` (`fix/winprob-feed-hardening`)

---

## Commit appendix

All 82 commits in the window. Merge commits appear under the branch they were made on.

### `feat/live-timeouts` (1) — open

`0d7d64f` · `2026-08-16` · `westy412` · feat(live): the snapshot carries timeouts remaining, straight off the push header

### `fix/mm-reading-collisions` (3)

`743b174` · `2026-08-15` · `westy412` · fix(mm-publisher): the stale-reoffer withhold applies only to an UNDECIDED book
`1bf9b2f` · `2026-08-15` · `westy412` · fix(mm-publisher): withhold the liveness re-offer once the game moves past the reading
`0ff4fa5` · `2026-08-15` · `westy412` · fix(mm-publisher): a second's LAST reading reaches the MM, not its first

### `fix/winprob-feed-hardening` (1)

`6e6e5ec` · `2026-08-15` · `westy412` · fix(live): the win-prob feed surfaces a refused NATS subscription instead of parking

### `fix/mm-publisher-latency` (2)

`434f8c8` · `2026-08-15` · `westy412` · fix(mm-publisher): concurrent timeline fetches + competition gate on discovery
`da08336` · `2026-08-13` · `westy412` · fix(mm-publisher): universe filter never matched SR-native ids — every game silently unadopted

### `testing-promote` (1)

`1f84d28` · `2026-08-15` · `westy412` · Merge dev into testing: mm-publisher latency fixes (PR #39)

### `testing-keep-polling` (1)

`d492dcb` · `2026-08-14` · `westy412` · fix(mm-publisher): never retire a finished game — settle watch at live rate, then overnight confirmations forever

### `fix/mm-publisher-post-game-keep-polling` (1) — open

`751efb6` · `2026-08-14` · `westy412` · fix(mm-publisher): never retire a finished game — settle watch at live rate, then overnight confirmations forever

### `local/replay-sandbox` (1) — open

`0cecdd7` · `2026-08-14` · `westy412` · feat(live): fold the mm_publisher's win-prob readings into game deltas

### `testing-local` (1)

`daf5604` · `2026-08-13` · `westy412` · fix(mm-publisher): universe filter never matched SR-native ids — every game silently unadopted

### `hotfix/mm-publisher-universe-filter` (1) — open

`d877b26` · `2026-08-13` · `westy412` · fix(mm-publisher): universe filter never matched SR-native ids — every game silently unadopted

### `fix/final-settling-ttls` (1)

`b8b5560` · `2026-08-13` · `westy412` · fix(cache): a freshly final game settles before it archives; stats TTL is value-derived

### `fix/mm-discover-tomorrow` (1)

`66d120b` · `2026-08-13` · `westy412` · fix(mm-publisher): discover tomorrow's UTC date too — restore the midnight ramp

### `feat/game-aggregate` (1)

`856190a` · `2026-08-13` · `westy412` · feat(games): game-page aggregate + multi-year schedule; fix depth charts and the winprob preseason gap

### `fix/live-worker-hardening` (2)

`8047d74` · `2026-08-13` · `westy412` · test(worker): live-fire validation harness — the real binary, attacked
`4df15bf` · `2026-08-13` · `westy412` · fix(worker): harden the live path against the pre-go-live review findings

### `chore/testing-real-feed` (1)

`3acf734` · `2026-08-13` · `westy412` · chore(testing): flip the testing worker to the real SR feed with discovery on

### `fix/unpublished-phase-empty` (1)

`597033e` · `2026-08-13` · `westy412` · fix(schedule): an unpublished season phase is an empty page, not a 502

### `feat/schedule-multi-phase` (2) — tip open

`b0e16f9` · `2026-08-13` · `westy412` · fix(schedule): an unpublished season phase is an empty page, not a 502
`6bf8ec7` · `2026-08-13` · `westy412` · feat(schedule): serve a whole season year in one request

### `fix/reconnect-reconcile` (1)

`6a44c89` · `2026-08-13` · `westy412` · fix(worker): actually run the reconnect catch-up when the push stream drops

### `chore/gameday-2026-08-13` (2)

`56ada7c` · `2026-08-12` · `westy412` · chore: drop the game-day plan doc — it lives in the session, not the repo
`ce06fa9` · `2026-08-12` · `westy412` · feat(gameday): record the raw push feed, and a plan for 2026-08-13

### `fix/live-cache-ttls` (1)

`c0d4114` · `2026-08-12` · `westy412` · fix(cache): derive game TTLs from the fetched game, not a guess before it

### `merge/testing-into-dev` (2)

`006eec8` · `2026-08-12` · `westy412` · style: adopt datetime.UTC in the merged winprob fallback
`e72f00a` · `2026-08-12` · `westy412` · Merge origin/testing into dev: reconcile the winprob bulk fallback

### `feat/preseason-schedule` (5)

`7510f4a` · `2026-08-12` · `westy412` · test(schedule): complete the edge-case matrix and enforce no-live-SR
`80be12f` · `2026-08-12` · `westy412` · feat(schedule): SR_SEASON_TYPE override, NCAA preseason guard, per-week keys
`cc99cbe` · `2026-08-12` · `westy412` · feat(schedule): make season type expressible, and week 0 reachable
`dd70e80` · `2026-08-12` · `westy412` · feat(schedule): serve the whole union on page 1 by default
`ffea38f` · `2026-08-12` · `westy412` · feat(schedule): derive the served week from game status, both leagues

### `feat/live-worker-discovery` (3)

`d327bee` · `2026-08-12` · `westy412` · test(worker): rehearse discovery against two REAL recorded games
`8d066ef` · `2026-08-12` · `westy412` · feat(scripts): add watch_live.py — see which link of the live chain is flowing
`6358bb3` · `2026-08-12` · `westy412` · feat(worker): discover live games from one unfiltered SR Push stream

### `feat/role-tiers` (1) — Hxsan

`ecf3332` · `2026-08-11` · `Hxsan` · feat(auth): split data access from trading eligibility (role tiers)

### `feat/live-poll-500ms-real` (1)

`488d35c` · `2026-08-11` · `westy412` · feat(infra): LIVE poll at 500 ms — George's 08-11 ruling, matching Edwin's 03-08 number

### `feat/live-poll-500ms` (1)

`e0204cf` · `2026-08-11` · `westy412` · feat(infra): LIVE poll at 500 ms — George's 08-11 ruling, matching Edwin's 03-08 number *(formatting only; see Notable fixes)*

### `fix/terraform-stitch` (3)

`78ef4b5` · `2026-08-11` · `westy412` · Merge origin/dev: reconcile the parallel publisher-env fixes (keep both sessions' comments)
`b7c6f18` · `2026-08-11` · `westy412` · fix(infra): align the publisher pools — production probabilities access + the product key + redis
`99e551b` · `2026-08-11` · `westy412` · fix(infra): repair the double-merge terraform — close the publisher pool resource, dedupe the cache-warming blocks

### `merge/main-into-dev` (2)

`74e708a` · `2026-08-11` · `westy412` · Merge origin/main into dev: reconcile the parallel NCAA/season fixes + cache warming with the MM publisher infra
`7e0329e` · `2026-08-11` · `westy412` · Merge origin/main into dev: union the terraform (publisher pool + cache warming), take main's season docstrings

### `feat/mm-publisher-deploy` (1)

`c7a7018` · `2026-08-11` · `westy412` · feat(infra): the MM publisher worker pool — terraform + the third deploy step

### `testing` — direct commits (2)

`fa0a6d3` · `2026-08-15` · `westy412` · chore(infra): wire the live win-prob feed env into the testing deploy
`7f30fc4` · `2026-08-14` · `westy412` · feat(live): fold the mm_publisher's win-prob readings into game deltas

### `dev` — direct commit (1)

`7138750` · `2026-08-11` · `westy412` · fix(infra): the publisher pool needs PROBABILITIES_API_KEY + REDIS_URL

### `testing` — merge commits (9)

`952d8be` · `2026-08-15` · `westy412` · Merge fix/winprob-feed-hardening into testing: the win-prob feed surfaces a refused NATS subscription
`6b444e4` · `2026-08-13` · `westy412` · Merge pull request #36 from Novosapien/dev
`261632c` · `2026-08-13` · `westy412` · Merge pull request #34 from Novosapien/dev
`f2dff19` · `2026-08-13` · `westy412` · Merge pull request #32 from Novosapien/dev
`ebfcc18` · `2026-08-13` · `westy412` · Merge pull request #30 from Novosapien/dev
`fd1bf9b` · `2026-08-13` · `westy412` · Merge pull request #28 from Novosapien/dev
`efce8af` · `2026-08-13` · `westy412` · Merge pull request #25 from Novosapien/dev
`17f3ffe` · `2026-08-12` · `westy412` · Merge pull request #20 from Novosapien/dev
`9f2a640` · `2026-08-11` · `westy412` · Merge remote-tracking branch 'origin/dev' into testing

### `dev` — merge commits (23)

`f822ced` · `2026-08-16` · `westy412` · Merge pull request #40 from Novosapien/fix/mm-reading-collisions
`8764a46` · `2026-08-15` · `westy412` · Merge pull request #39 from Novosapien/fix/mm-publisher-latency
`dae35c6` · `2026-08-13` · `westy412` · Merge pull request #35 from Novosapien/fix/final-settling-ttls
`5a97d14` · `2026-08-13` · `westy412` · Merge pull request #33 from Novosapien/fix/mm-discover-tomorrow
`0754d36` · `2026-08-13` · `westy412` · Merge pull request #31 from Novosapien/feat/game-aggregate
`173b2c8` · `2026-08-13` · `westy412` · Merge pull request #29 from Novosapien/fix/live-worker-hardening
`f8191bc` · `2026-08-13` · `westy412` · Merge pull request #26 from Novosapien/fix/unpublished-phase-empty
`637dde6` · `2026-08-13` · `westy412` · Merge pull request #27 from Novosapien/chore/testing-real-feed
`87a5abc` · `2026-08-13` · `westy412` · Merge pull request #23 from Novosapien/fix/reconnect-reconcile
`ffe5a57` · `2026-08-13` · `westy412` · Merge pull request #22 from Novosapien/chore/gameday-2026-08-13
`e3d2441` · `2026-08-13` · `westy412` · Merge pull request #21 from Novosapien/fix/live-cache-ttls
`efddc40` · `2026-08-13` · `westy412` · Merge pull request #24 from Novosapien/feat/schedule-multi-phase
`b5893b7` · `2026-08-12` · `westy412` · Merge pull request #19 from Novosapien/merge/testing-into-dev
`29a14f7` · `2026-08-12` · `westy412` · Merge pull request #18 from Novosapien/feat/preseason-schedule
`416f1d7` · `2026-08-12` · `westy412` · Merge pull request #17 from Novosapien/feat/live-worker-discovery
`a9c85ff` · `2026-08-12` · `westy412` · Merge origin/main into dev: reconcile the 2026-08-11 drift (role tiers)
`3a88cbb` · `2026-08-11` · `westy412` · Merge pull request #15 from Novosapien/feat/live-poll-500ms-real
`d48122a` · `2026-08-11` · `westy412` · Merge pull request #14 from Novosapien/feat/live-poll-500ms
`d32f788` · `2026-08-11` · `westy412` · Merge pull request #13 from Novosapien/fix/terraform-stitch
`a0370a8` · `2026-08-11` · `westy412` · Merge pull request #12 from Novosapien/fix/terraform-stitch
`8a31490` · `2026-08-11` · `westy412` · Merge pull request #11 from Novosapien/merge/main-into-dev
`7078736` · `2026-08-11` · `westy412` · Merge pull request #9 from Novosapien/feat/mm-publisher-deploy
`89e8456` · `2026-08-11` · `westy412` · Merge pull request #8 from Novosapien/feat/mm-probability-publisher

### `main` — merge commits (2)

`f8c8aef` · `2026-08-11` · `Hxsan` · Merge pull request #16 from Novosapien/feat/role-tiers
`0f75097` · `2026-08-11` · `westy412` · Merge pull request #10 from Novosapien/dev
