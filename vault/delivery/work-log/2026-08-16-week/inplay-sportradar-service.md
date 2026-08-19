---
description: "Weekly engineering record for the Sportradar service, 09-16 August 2026 — 82 commits, six market-maker publisher fixes, and the first two live NFL preseason game nights"
service: inplay-sportradar-service
window: 2026-08-09 .. 2026-08-16
commits: 82
authors: { westy412: 80, Hxsan: 2 }
branches: { touched: 32, merged: 24, open: 5 }
---

# inplay-sportradar-service — week of 09–16 August 2026

> **Delivery:** [[delivery]] · **Week:** [[work-log-2026-08-16]]

## Headline

This service is the only part of InPlay that talks to Sportradar. This week it started
to feed the market maker for real, and then survived the first live NFL preseason games
on 13, 14 and 15 August. Most of the week's work is correctness under live fire. Ten
separate faults were found on real game nights. Each was fixed the same night or the
next day. The service also learned to find live games by itself, instead of waiting for
a person to type in a game id.

## Scope

- **Window:** 2026-08-09 to 2026-08-16
- **Commits:** 82 (westy412 80, Hxsan 2)
- **Branches touched:** 32 — 3 mainline (`main`, `dev`, `testing`) plus 29 working
  branches. Of those 29, 24 merged and 5 are still open.
- **Busiest day:** 2026-08-13 (29 commits)

No commits landed on 09 or 10 August. The week's work starts on 11 August.

**The repository was live while this log was written.** A new branch, `feat/live-timeouts`,
appeared during the analysis with one commit dated 16 August (`0d7d64f`). It is counted
and described below. A later commit could arrive after this file is written. The main
worktree also holds uncommitted changes to six files, plus an untracked `captures/`
directory and `scripts/mm_prob_replay.py`. Uncommitted work is outside this log's scope.

**Where the work landed.** `origin/main` has not moved since 11 August. Its tip is
`f8c8aef`. Everything after that date sits on `origin/dev` and `origin/testing`, which
are both at `f822ced`. The 13, 14 and 15 August game nights ran entirely in the testing
environment, by George's decision (`3acf734`). So "merged" in the table below almost
always means `origin/dev` and `origin/testing`, not production.

**A note on remotes.** This log reads the refs on disk. The shared context forbids
`git fetch`, so a remote ref could be behind GitHub. Nothing in the history suggested
that, but the reader should know the constraint.

---

## What the market-maker publisher is

Several branches this week start with `mm-`. They all mean one thing.

The market maker (`inplay-market-maker`) prices 170 team securities. It needs a live
win probability for every game. Sportradar sells that number, but only this service
holds the Sportradar key, the retry rules and the 170-team map. So this service polls
Sportradar and pushes each probability reading onto a NATS message bus. The market
maker reads the bus and never calls Sportradar itself.

The part that does this is a separate worker process, `app.workers.mm_publisher`. This
document calls it **the publisher**. Its design is in `docs/mm-probability-publisher.md`.

Two facts about the publisher explain most of this week's fixes:

1. **A reading is identified by its timestamp.** The market maker de-duplicates on that
   stamp, so one timestamp must carry exactly one message.
2. **Silence is a signal.** The market maker judges whether a price is fresh from the
   time of the last successful fetch. If the publisher stops sending for a game, the
   market maker suspends that game's book. That is correct when the feed is genuinely
   dead. It is wrong when the publisher simply stopped for a bad reason.

---

## Themes

### 1. The publisher reached production, then took six correctness fixes

The publisher's code was written on 6 August. It reached `origin/main` on 11 August
through `feat/mm-probability-publisher` (merge `89e8456`). The same day it got its own
Cloud Run worker pool and a third deploy step, on `feat/mm-publisher-deploy`
(`c7a7018`). Three infrastructure repairs followed. Two parallel merges had
left the Terraform file broken, and the new pool was missing `PROBABILITIES_API_KEY` and
`REDIS_URL`. Those repairs are on `fix/terraform-stitch` (`99e551b`, `b7c6f18`) and
directly on `dev` (`7138750`). George also ruled the live poll rate down to 500 ms. That change is on
`feat/live-poll-500ms-real` (`488d35c`) — see the note under **Notable fixes** about
the branch before it.

Then the games started, and the publisher was wrong in six ways.

**It adopted no games at all.** The universe filter compared Sportradar's own
competitor ids (`sr:competitor:NNNN`) against the league feed's GUIDs. The two id
schemes can never match, so discovery filtered out every game: zero adopted, zero polls,
zero readings on the bus. George found this live on 13 August, 30 minutes before the
first preseason slate. The fix makes an unrecognised Sportradar id err on the side of
adoption, and lets the market maker's own bindings decide what it prices. This one fix
exists as three identical patches on three branches:

- `hotfix/mm-publisher-universe-filter` (`d877b26`). It was cut from the deployed
  production SHA, so the API and live worker would not roll forward on game night.
- `testing-local` (`daf5604`). This is the one that reached `origin/dev` and
  `origin/testing`.
- `fix/mm-publisher-latency` (`da08336`).

Only `daf5604` is on a mainline branch.

**Prime-time games were discovered at kickoff.** Discovery fetched only today's UTC
schedule. A game at 20:00 ET kicks off at or after 00:00 UTC. It therefore lives
on tomorrow's schedule date. The publisher found it at the date rollover, which is its
own kickoff. The pre-kickoff hour that the market maker prices its opening book from was lost every
time. `fix/mm-discover-tomorrow` (`66d120b`) fetches both dates on every discovery
pass. Merged to `origin/dev` and `origin/testing` via PR #33.

**A round of polls took 3.5 seconds instead of 2.** The publisher fetched due games one
at a time, at about 0.7 s per Sportradar round trip. Four live games therefore stretched
every game's real cadence. It also adopted a CFL fixture that Sportradar never
finalled, which sat on the live tier forever and burned a fetch slot every round. Both
are fixed on `fix/mm-publisher-latency` (`434f8c8`): the fetches now run concurrently,
and discovery drops any fixture that declares a competition other than NFL or NCAA.
Merged via PR #39. The commit records that the remaining lag is Sportradar's own
~10 s model latency, which is not reachable from this side.

**A second's first reading reached the market maker, not its last.** Sportradar stamps
readings to the second and issues several distinct readings inside one second. Measured
across three live games on 15 August: 131 of 1,638 readings shared a second with an
earlier one, and the widest such pair was 8.5 probability points apart. The publisher
iterated Sportradar's raw order, so it published the first reading of each second and
dropped every later revision. `fix/mm-reading-collisions` (`0ff4fa5`) collapses each
second to its last reading and publishes in stamp order. Replayed against the real
CAR@BUF timeline, the new path is correct for 726 of 726 seconds; the old path was
superseded on 68.

**The liveness re-offer kept dead prices alive.** The publisher re-sends the last
reading during quiet spells, so the market maker's freshness clock keeps ticking. On
15 August Sportradar stopped pricing CLE@CHI for 36 minutes mid-game. Its last reading
was computed at 10-7 while the game stood 10-10. The market maker held a live book at
46.3% with no signal that anything was wrong. `fix/mm-reading-collisions` (`1bf9b2f`)
withholds the re-offer when the reading's scoreline differs from the current one **and**
the reading is older than `MMPUB_STALE_REOFFER_GRACE_S` (default 120 s). Both
conditions are needed, because either alone is normal. A withheld re-offer logs a
warning.

**That guard then suspended healthy books.** Sportradar records a probability change
only when it exceeds 0.1%, so a decided game legitimately stops moving. CAR@BUF sat at
98.4% for its last 38 minutes and the new guard suspended its book for 20.4% of the
game, for nothing. `743b174` skips the withhold when either side of the two-way market
is at or beyond `MMPUB_DECIDED_PROBABILITY_PCT` (default 98). Replayed on the same three
games: CLE@CHI suspension fell from 24.7% to 18.5%, MIN@NYG stayed at 0%, CAR@BUF fell
from 20.4% to 0%. All three commits merged via PR #40 (`f822ced`, 16 August).

### 2. A finished game must keep reporting

When a game ends, the publisher used to stop polling one hour later. The market maker
judges freshness from successful observations, so that silence starved every finished
game's book into permanent suspension. Ten books went dark on 14 August. The 600 s
correction watch before that was also too slow. It made each book suspend, cancel and
re-stand once per poll, against the market maker's ~20 s freshness fuse.

`fix/mm-publisher-post-game-keep-polling` (`751efb6`) changes three things. The
post-game settle watch now polls at the live rate, so no gap is wide enough for the fuse
to see. The settle window default doubles to 2 hours, so it outlasts the market maker's
own activity flip. Past that window the publisher polls at the overnight rate forever
and never returns "done". Sportradar serves closed timelines indefinitely, and George
ruled that quota is not a constraint.

The branch `fix/mm-publisher-post-game-keep-polling` is **not merged**. The identical
patch on `testing-keep-polling` (`d492dcb`) is the one that reached `origin/dev` and
`origin/testing`. The commit notes that the matching engine-side game-end work stays
with the market maker's own N40 item.

### 3. The live worker finds its own games, and survives failure

The live worker (`app.workers.live`) is the other worker in this service. It reads
Sportradar's Push stream and turns it into the play-by-play the app shows. Until this
week it needed `LIVE_GAME_IDS` — a hand-typed list. A game nobody typed in was a game
nobody captured, which is what happened to the 7 August preseason game.

`feat/live-worker-discovery` (`6358bb3`) removes the list. Sportradar's Push feed sends
every in-progress game on one unfiltered subscription, and each envelope names its own
game. A new `app/workers/multiplex.py` fans that one connection out to a pipeline per
game, created on first sight. Everything downstream is unchanged. An explicit
`LIVE_GAME_IDS` still wins. The commit records that this inverts the meaning of an empty
list, from "idle" to "capture everything", and updates the runbook's abort step. It also
records two defects found but deliberately not fixed there — both were fixed later in
the week (see theme 5 and `fix/reconnect-reconcile` below).

`d327bee` rehearses the fan-out against two real recorded games replayed interleaved on
one stream. The strongest assertion is that the interleaved result is byte-identical to
running the NFL game alone. `8d066ef` adds `scripts/watch_live.py`. It reads each link of
the chain separately: the raw Sportradar stream, the Centrifugo channel, and the API's
own `/live` blob. A game-day operator can then tell which link broke.

`fix/reconnect-reconcile` (`6a44c89`) fixes a feature that did not exist. Sportradar
Push has no replay, so plays that happen while the socket is down are gone forever
unless a REST catch-up runs. `GamePipeline.reconcile` implemented that catch-up
correctly and was covered by an end-to-end test, but **nothing ever called it**. The
push consumer absorbed reconnects inside its own loop, so no code ever saw a reconnect
boundary. A dropped connection therefore left a permanent hole in the play list. The fix
makes the consumer announce reconnects and awaits a hook before the first message of any
later connection. The new tests target the wiring, not the catch-up logic, because a
behavioural test of the catch-up passed throughout.

`fix/live-worker-hardening` (`4df15bf`) lands every confirmed critical and high finding
from an adversarial review run the night before the first real games. It fixes four
faults:

- One bad message killed all games. The process still looked healthy to Cloud Run.
- Both instances wrote the Redis blob, although only one was allowed to publish.
- A restarted worker republished from sequence 1. That permanently froze every viewer's
  screen until they force-quit the app.
- A game found by discovery could never end, because Sportradar Push sends no status
  flip. An idle sweep now runs a REST end-check on any adopted game quiet for 3 minutes.

`8047d74` adds `scripts/validate_live_worker.py`, which attacks the real binary against
a local fake Sportradar, including a hard `SIGKILL` mid-game and a restart. Result:
17 of 17. It is a manual tool, not CI. Both merged via PR #29.

**Game-day tooling, not shipped code.** `chore/gameday-2026-08-13` (`ce06fa9`) added a
raw-feed recorder to `watch_live.py`, so the night's data survives even if every
deployed component fails. Getting that right needed a real change to
`PushStreamDecoder`. Writing the parsed model loses data — 25 keys in, 11 out on a real
fixture. So the decoder gained `feed_with_raw()`, and the recorder writes the verbatim
wire dict. The same branch added a game-day plan document and then deleted it in the
next commit (`56ada7c`) on George's call. The recorder and the decoder fix stayed.
`chore/testing-real-feed` (`3acf734`) is Terraform only: it pointed the testing worker
at the real Sportradar feed, turned discovery on, and raised the worker to two
instances. `local/replay-sandbox` is a local worktree and is **not merged**.

**In flight on 16 August.** `feat/live-timeouts` (`0d7d64f`) adds
`homeTimeoutsRemaining` and `awayTimeoutsRemaining` to the live snapshot and to the
`op:tick` delta. Sportradar sends `remaining_timeouts` on every push message. It sits in
the same `payload.game.summary` block the worker already reads. So this needs no timeout
counting, no Redis persistence and no boxscore poll — all three of which the app-side
scoping had assumed. Replaying the recorded feeds proves it: 197 NFL and 79 NCAA deltas carry
timeouts on every one, with zero nulls. The fields are optional, so the contract version
stays at 1. They are retained from the previous snapshot when a partial header omits
them, and never defaulted to 3. The branch is **open** and sits on top of
`local/replay-sandbox`.

### 4. Win-probability readings reach the app, not only the market maker

One entitled Sportradar fetch can serve two consumers. `7f30fc4` (committed directly on
`testing`) gives the live worker an optional feed. The feed tails the publisher's
readings on NATS and maps each Sportradar event id to its league game. It then publishes
`homeWinProb` on the existing `game:{id}` channel as an `op:tick` delta. The feed is off
unless
`LIVE_WINPROB_NATS_URL` is set; with it empty the worker behaves exactly as before.
`fa0a6d3` wires the environment into the testing deploy.

On go-live, 15 August, it did not work. The service's NATS user held publish rights on
`sr.probabilities.>` but no subscribe grant, so the server refused the subscription.
The `nats.py` client reports that refusal on an asynchronous error callback. It still
returns a subscription object that looks alive. So the feed idled behind a
healthy-looking `winprob_feed_subscribed` log line, and the app's win-probability bar
stayed at its pre-game value. `fix/winprob-feed-hardening` (`6e6e5ec`) wires the error callback into
the read loop so any server error tears the connection down and the retry loop re-logs
the cause. It also logs every applied reading and every unmapped event, redacts the NATS
credential from the log, and records the required grant. The grant itself was applied by
hand on the `inplay-nats` host by `SIGHUP`, with a backup at
`nats.conf.bak-winprob-sub-20260815`. That is a live-host change, not a repository
change. Merged into `testing` (`952d8be`) and then into `origin/dev` and
`origin/testing`.

### 5. Cache lifetimes derived from the fetched game

The service caches Sportradar responses in Redis. A cache lifetime had to be chosen
before the fetch, but whether a game is final is a property of the response. That
mismatch produced three faults, none of which is visible in a response body.

`fix/live-cache-ttls` (`c0d4114`) found two. `get_play_by_play` applied the 30-day
archival lifetime unconditionally, and two live paths call it mid-game. So the first
read taken during a game froze a partial play list for a month. `get_boxscore` always
used the one-hour pre-game lifetime, and the `/live` endpoint decides liveness from that
cached status. So `/live` returned 404 well into the game it exists to cover. The fix
lets `get_or_set` accept a lifetime that is a function of the fetched value, resolved
once on the leader before write-back. Lifetimes are now derived:

- Play-by-play: 30 days when final, 30 s otherwise.
- Boxscore: 30 days when final, 30 s when live or past kickoff, one hour when scheduled.
  The scheduled case is clamped, so the key cannot outlive kickoff.

The same commit removes a duplicated `LIVE_STATUSES` set that existed byte-identical in two
files.

`fix/final-settling-ttls` (`b8b5560`) closes the same bug class on `/statistics`, and
adds a step the first fix missed. A game that has just gone final is not immutable:
Sportradar pushes stat and scoring corrections after the whistle. Final blobs within
12 hours of kickoff now re-check every 15 minutes before they graduate to the 30-day
archival lifetime. Cost is at most one Sportradar call per blob per 15 minutes per
instance, and only while someone reads it. Merged via PR #35.

### 6. The app-facing API: preseason schedule, the game page, and access roles

`GET /sr/games` followed Sportradar's `current_week` pointer, and Sportradar advances
that pointer only once the next week's games are published. During the 2026 preseason
that served one closed game and nothing upcoming. `feat/preseason-schedule` (`ffea38f`)
derives the served week instead. It takes the most recent week holding a result, and
unions it with the next week holding unplayed games. The derivation rolls PRE → REG →
PST, and then into the next published season year.

`dd70e80` makes `limit` nullable, so an omitted page size serves the whole union.
Without that change, an NCAA union of about 284 games filled page 1 with last week's
finals. Every app call site calls `useGames(league)` bare and never follows the cursor,
so those fixtures would never have been seen. This is a public OpenAPI contract change
and the parameter description says so. `cc99cbe` makes `season_type` expressible and week 0 reachable.
`80be12f` adds an `SR_SEASON_TYPE` override, returns a typed 404 for NCAA preseason
(NCAA football has no preseason, so a 502 would be retried forever), and retires the
`schedule_current_week` cache key. `7510f4a` completes the edge-case matrix and adds a
`conftest` guard that fails any test escaping to live Sportradar.

`feat/schedule-multi-phase` (`6bf8ec7`) lets `/sr/schedule` serve a whole season year in
one request. The app's team page was making 18 requests where 6 were needed, which
starved the page's other calls of connections. Phases are fetched concurrently and
merged in calendar order. Omitting `season_type` still means REG, deliberately.

`fix/unpublished-phase-empty` (`597033e`) fixes an incident: the night the preseason
build reached the testing app, both Discover tabs hung. The app asked for NCAA 2026
`season_type=PST`, a postseason Sportradar has not published, and the service turned
Sportradar's 404 into a 502. The app treats 5xx as transient and retried in a loop. An
unpublished phase is now an empty page. A genuine 5xx, 429 or timeout still propagates.

`feat/game-aggregate` (`856190a`) adds `GET /sr/games/{id}/aggregate`, which answers a
game page in one call instead of about 30 requests. The same commit fixes depth charts:
all 14 calls on the testing game page returned 404, because the default context was
hardcoded to REG week 1. It also moves the win-probability bulk fallback onto the
derived `/sr/games` union, so the fallback prices preseason games.

Hasan's two commits are `feat/role-tiers` (`ecf3332`), the only work that reached
`origin/main` after 11 August. The `trader` role previously gated both reading sports
data and trading, so an unverified user could not see a team page or a chart. This
service's edge now answers only "may you read sports data" and accepts three tiers:
`preview`, `trader-lite` and `trader`. Trading eligibility moves to the trading service.
`trader` keeps its exact key and meaning, so no user needs a re-grant.

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

`feat/ipo-data-domains` and `feat/ipo-data-domains-pr-a` were named as candidates in
the brief. Both branches last moved on 3 and 4 July 2026. Neither has a commit in this
window, so there is no IPO data-domains work to report.

---

## Notable fixes and incidents

**The universe filter adopted nothing (13 August).**
*Symptom:* zero games adopted, zero polls, zero readings on the bus, 30 minutes before
the first real preseason slate. *Root cause:* the probabilities schedule keys
competitors on `sr:competitor:NNNN`; `TEAM_SYMBOLS` keys on league-feed GUIDs. The
membership test could never match. *Fix:* an unrecognised Sportradar id now errs on the
side of adoption. *Verification:* the commit records that the fault was found live. The
branch was cut from the deployed production SHA `f8c8aef`, not from `main`, so the API
and live worker would not roll forward on game night. The commit does not record a
post-fix measurement. *Landed as:* `daf5604`.

**The market maker held a live book on a dead probability (15 August).**
*Symptom:* Sportradar stopped pricing CLE@CHI for 36 minutes mid-game. Its last reading
was computed at 10-7 while the game stood 10-10. The market maker showed home 46.3% and
no signal that anything was wrong. *Root cause:* the publisher's liveness re-offer
refreshes the market maker's freshness clock, so it defeated the market maker's own
dead-feed protection at the exact moment that protection was needed. *Fix:* withhold the
re-offer on a stale reading whose scoreline no longer matches. *Verification:* replayed
against the real CLE@CHI outage — re-offers continue for the first 2 minutes, then
withhold from 5 minutes on. *Landed as:* `1bf9b2f`, corrected by `743b174`.

**Ten finished games' books went dark (14 August).**
*Symptom:* every finished game's book entered permanent suspension. *Root cause:* the
publisher's poll clock returned "done for good" one hour after a game ended, and the
market maker reads that silence as a dead feed. *Fix:* poll a finished game at the live
rate for 2 hours, then at the overnight rate forever. *Verification:* the commit cites
the market maker vault's N40 forensics; it does not claim a live re-test. *Landed as:*
`d492dcb`.

**Both Discover tabs hung in the testing app (13 August).**
*Symptom:* both Discover tabs sat on their spinners. *Root cause:* the app asked for
NCAA 2026 `season_type=PST`, which Sportradar has not published, and the service
returned a 502. The app retried the 5xx in a loop. *Fix:* an unpublished phase returns
an empty page. *Verification:* the commit states the exact stuck request now returns
`{"data":[],"has_more":false}` in 0.5 s against live Sportradar. *Landed as:* `597033e`.

**The win-probability feed was silently refused (15 August).**
*Symptom:* the app's win-probability bar stayed at its pre-game value while the worker
logged a healthy `winprob_feed_subscribed` line. *Root cause:* the NATS user had publish
but not subscribe rights, and `nats.py` reports a refused subscription only on an
asynchronous callback that was not wired up. *Fix:* wire the error callback into the
read loop, log every applied reading, and grant subscribe on the NATS host. *Landed as:*
`6e6e5ec`. **Caveat:** the NATS grant was applied by hand with `SIGHUP` on the
`inplay-nats` host, with a backup at `nats.conf.bak-winprob-sub-20260815`. It is not in
this repository.

**A reconnect feature that was never called.**
`GamePipeline.reconcile` existed, was covered by an end-to-end test, and no production
path ever invoked it. `grep -rn "\.reconcile(" src/` returned nothing. Every test
passed. Every dropped socket left a permanent hole in the play list. *Landed as:*
`6a44c89`.

**A commit whose subject does not match its diff.**
`e0204cf` on `feat/live-poll-500ms` is titled "LIVE poll at 500 ms" and its diff is
whitespace alignment in `terraform.prod.tfvars` only. The real change is `488d35c` on
`feat/live-poll-500ms-real`, which sets `MMPUB_POLL_LIVE_S = "0.5"` on both the
production and testing pools. `488d35c`'s own body says so. Both branches merged, so the
setting is in place.

**Four fixes exist as duplicate patches on several branches.** Verified by `git
patch-id`, these pairs and triples are byte-identical:
`d877b26` = `daf5604` = `da08336`; `751efb6` = `d492dcb`; `7f30fc4` = `0cecdd7`;
`b0e16f9` = `597033e`. This is a working pattern, not a contradiction: the fix was cut
against the deployed SHA for a live hotfix and re-applied on a mainline-based branch.
No fix was reverted and reapplied this week.

---

## Still open

Five branches are unmerged. Four of them are duplicates of a patch that reached a
mainline branch, confirmed by `git patch-id`, so no work is lost there. The fifth,
`feat/live-timeouts`, is genuinely new and in flight.

| Branch | Last commit | State | What is left |
|---|---|---|---|
| `feat/live-timeouts` | 2026-08-16 (`0d7d64f`) | **In flight.** | New work, created on 16 August while this log was written. It is the checked-out branch in the main worktree, has no remote ref, and is based on `local/replay-sandbox` rather than a mainline branch. It needs rebasing onto `dev` and a PR. |
| `hotfix/mm-publisher-universe-filter` | 2026-08-13 (`d877b26`) | **Superseded, safe to delete.** | Identical to `daf5604`, which is on `origin/dev` and `origin/testing`. It was cut from the deployed production SHA for a game-night hotfix. |
| `fix/mm-publisher-post-game-keep-polling` | 2026-08-14 (`751efb6`) | **Superseded, safe to delete.** | Identical to `d492dcb`, which is on `origin/dev` and `origin/testing`. |
| `local/replay-sandbox` | 2026-08-14 (`0cecdd7`) | **Local sandbox.** | It has no remote ref. Its one commit is identical to `7f30fc4` on `testing`. Nothing is pending on the commit itself, but `feat/live-timeouts` now branches off it. |
| `feat/schedule-multi-phase` | 2026-08-13 (`b0e16f9`) | **Partly merged.** | `6bf8ec7` merged via PR #24. The tip `b0e16f9` did not, but it is identical to `597033e`, which merged via PR #26. Nothing is pending. |

**The wider gap is `origin/main`.** Every change from 12 August onward sits on
`origin/dev` and `origin/testing` only. That covers the live worker discovery and
hardening, all six publisher correctness fixes, the cache-lifetime work, the whole
preseason schedule change and the win-probability feed. The gap was deliberate for the
13 August go-live, which ran entirely in testing. It is a decision to revisit, not a
fault.

Twelve other directories are worktrees of this one repository. Nine are under
`/private/tmp/claude-501/`. They hold branches that were worked on in parallel and are
all merged. The main path itself is on `feat/live-timeouts`. Three worktrees are
siblings of the main path:
`inplay-sportradar-hotfix` (`hotfix/mm-publisher-universe-filter`),
`inplay-sportradar-testing-fix` (`testing-local`) and
`inplay-sportradar-winprob` (`fix/winprob-feed-hardening`).

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
</content>
</invoke>
