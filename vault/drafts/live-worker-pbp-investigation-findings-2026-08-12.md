---
description: "Findings from the live-worker play-by-play investigation — what gates capture, what is already fixed, three code defects found, and the plan for the Thursday 08-13 preseason games"
---

# Findings — the live worker and play-by-play capture

> **Date:** 2026-08-12. **Answers:** `live-worker-pbp-investigation-brief.md`.
> **Scope:** `inplay-sportradar-service`, GCP `inplay-497712`, Cloud Run worker
> pool `inplay-live-worker`. All probes below are read-only. **No deployed
> resource was changed.**

## Headline

Two of the brief's assumptions are now out of date, and three code defects are
new. In order of consequence:

1. **Sportradar Push entitlement is PROVEN.** The real feed accepted our
   production key and streamed. Gate 1 of the go-live runbook is closed.
2. **`LIVE_PUSH_BASE_URL` is already correct in production.** The brief and
   `CLAUDE.md` both say the prod worker is in simulation mode. It is not, and has
   not been since the Terraform apply. Production is in real-Sportradar mode.
3. **`LIVE_GAME_IDS` is the only remaining gate**, it is empty, and nothing
   alarms on that. This is confirmed.
4. **`GamePipeline.reconcile()` is never called.** The reconnect backfill is
   fully written and fully tested, but no production code path invokes it.
5. **The play-by-play cache poisons itself mid-game.** A 30-day TTL is applied to
   a play-by-play fetched while the game is still running.
6. **The boxscore cache can hide a live game for up to an hour.**

---

## 1. The gating model

`LIVE_GAME_IDS` is the only switch. The chain is short and has no discovery in it:

```
LIVE_GAME_IDS  →  settings.live.game_ids  →  Supervisor.game_ids()
               →  one GamePipeline per id (workers/live.py:139-149)
```

`Supervisor.game_ids()` returns the configured list verbatim. There is no
schedule lookup, no adoption, and no re-read: the list is read **once at process
boot**. A change therefore requires a new worker revision, which a Terraform
apply produces anyway.

**Who sets it, when:** `docs/first-game-golive-runbook.md` is the runbook and it
is specific — set `LIVE_GAME_IDS` in `terraform.prod.tfvars`, plan, apply, well
before kickoff, then watch worker logs → Redis blob → Centrifugo → device. The
runbook is marked "parked work" and names no owner and no clock time. That is the
gap: the procedure exists, the responsibility does not.

**Does anything alarm?** No. The project has 7 alert policies and 2 uptime checks
(listed live). Every one belongs to Centrifugo, Zitadel, or the trading broker.
**Nothing monitors this service or either worker pool.** An empty `LIVE_GAME_IDS`
on a game day is silent, and so is a worker that crashes at kickoff.

### Verified production state (read live, 2026-08-12)

| Item | Value |
|---|---|
| Image | `…/inplay-sportradar-api:f8c8aef85ca…` (= commit `f8c8aef`) |
| Revision | `inplay-live-worker-00014-b2x`, deployed 2026-08-11 13:23Z |
| Command | `python -m app.workers.live` |
| Instances | **2 active** (`manualInstanceCount: 2`, scalingMode manual) |
| `LIVE_GAME_IDS` | **present, empty** ⇒ idle |
| `LIVE_PUSH_BASE_URL` | **present, empty** ⇒ **real Sportradar** |
| `CENTRIFUGO_URL` | `http://10.0.3.12:8000` (internal ILB VIP) |
| `CENTRIFUGO_NAMESPACE` | `game` |

⚠ **Correct `CLAUDE.md`.** Its deployed-infrastructure section still warns that
`LIVE_PUSH_BASE_URL` is absent from the worker and that production is in
simulation mode. That warning is stale and now points the reader at the wrong
problem. `terraform.prod.tfvars` already carries `LIVE_PUSH_BASE_URL = ""`.

`inplay-live-worker-testing` is the deliberate mirror image:
`LIVE_PUSH_BASE_URL = https://playback.sportradar.com` ⇒ simulation. That split is
right and should stay.

## 2. Discovery for the live worker

The worker has none, and the Sportradar documentation says it may not need any.

From the Push Events reference: *"By default, a Push feed will provide all data
available for all in progress games."* The `match=sd:match:{id}` filter is
**optional**. One unfiltered subscription to
`…/nfl/official/production/stream/en/events/subscribe` therefore carries every
in-progress NFL game, and each envelope self-identifies through
`metadata.match` and `payload.game.id`.

That reframes the problem. Two designs are available:

**Design A — schedule-driven adoption (mirrors `inplay-mm-publisher`).** Poll the
season schedule, adopt any game in the 170-team universe, open one filtered push
connection per adopted game. Familiar, and reuses the mm-publisher's proven
shape. Costs N concurrent Sportradar connections for N simultaneous games, times
the instance count. Thursday alone would be 6 games × 2 instances = **12
concurrent push subscriptions**, and we do not know Sportradar's connection cap.

**Design B — one unfiltered stream, demultiplexed by game id.** One connection
per worker regardless of how many games are live. The worker learns about a game
the moment Sportradar sends its first event, so discovery becomes free and cannot
lag the schedule. `LIVE_GAME_IDS` becomes an optional allow-list rather than the
gate. Cost: the state machine and lease layers must be driven per learned game id
rather than per configured id, and every worker sees every game's bytes.

**Design B was chosen and is BUILT** — `feat/live-worker-discovery`, **PR #17**. It
removes the class of failure this investigation exists to explain: a game that
nobody remembered to type in cannot be missed. It is also the smaller operational
surface — one connection, one reconnect loop, one backoff — and it makes the
concurrency question above disappear.

The mm-publisher's UTC-date discovery edge noted in the brief (a game kicking off
at or after 00:00Z is adopted only at kickoff) applies to Design A only. Design B
has no equivalent, since it does not compute a date at all. **Thursday has three
games at or after 00:00Z**, so under Design A that edge would have bitten on
exactly the games in question.

### What PR #17 does

`app/workers/multiplex.py` fans one unfiltered stream out to a `GamePipeline` per
discovered game, created on first sight and dropped when the game ends.
**Everything downstream is unchanged** — same state machine, same Redis keys and
TTLs, same per-game lease, same fenced publisher — so a discovered game is
indistinguishable from a configured one. Both instances open the stream and see
every game; the per-game lease still decides which one publishes.

Discovery requires three conditions, all of them: `LIVE_DISCOVERY=true` (default),
no explicit `LIVE_GAME_IDS`, and the real SR feed. The third keeps the **testing**
worker idle, since the playback host is keyed by recording id and has no
unfiltered feed to subscribe to.

⚠ **This inverts what an empty `LIVE_GAME_IDS` means — from "idle" to "capture
everything" — and therefore changes the abort procedure.** Abort is now
`LIVE_DISCOVERY=false` or `worker_instances=0`. Clearing the game list no longer
stops the worker. The tfvars for both environments and the go-live runbook are
updated to say so.

Gates: `ruff` ✅, `mypy` ✅, **614 tests pass at 95.44% branch coverage**, 17 of them
new. What is *not* proven is the unfiltered stream carrying several concurrent
games — that needs a live game.

## 3. Push entitlement and preseason coverage — PROVEN

Live probe, 2026-08-12, production key, against Thursday's DET@CIN game id:

```
GET https://api.sportradar.com/nfl/official/production/stream/en/events/subscribe
      ?match=sd:match:d75404c4-fb21-4239-85e8-9fa8ce5283f5
→ 302  Location: https://push.prod.srsmtdelivery.com/stream/nfl/production?sessionId=…&token=…
→ 200  content-type: application/x-ndjson
       {"heartbeat":{"interval":5000}}   ×3 over 12s
```

- **Entitlement holds.** No 403. Gate 1 of the go-live runbook is closed.
- **The URL our code builds is the correct one.** `push_consumer.build_subscribe_url`
  produces exactly this path, and the `sd:match:{uuid}` filter format matches the
  Sportradar reference example.
- **The redirect + auth hop works**, which the runbook lists as never-executed.
- **Preseason is not rejected.** A preseason game id was accepted by the match
  filter. Full proof needs a live game, because a scheduled game yields heartbeats
  only — but there is no season-type gate visible anywhere in the product.
- The stream is `application/x-ndjson`. Our decoder handles both newline-delimited
  and concatenated objects, so this is fine.

## 4. Recovery after a miss

**The play-by-play itself is fully recoverable.** The 08-07 game that was missed
(CAR@ARI, `f112fe5a-d757-453f-8819-718dcddd52d3`) still returns its complete
play-by-play from the Sportradar REST feed: 600 KB, 4 periods, 183 events, final
33–30. Sportradar archives this the same way it archives the probabilities
timeline.

**The live-shaped blob is not recoverable after the fact.** `GET /sr/games/{id}/live`
(`services/live.py`) rebuilds a blob from REST only when the boxscore status is
`inprogress` or `halftime`. Once a game is final it raises 404 by design, and the
app falls back to the post-game boxscore view. So a missed game can be read as
play-by-play, but it cannot be replayed as a live experience, and nothing in the
app consumes a backfill today.

**A finding that matters more than the backfill question:** that same cold-miss
path means that *while a game is live*, `/live` already serves full play-by-play
built from REST, worker or no worker. The brief's statement that "NO play-by-play
flows to the app" is true of the **streaming** path only. A viewer opening a live
game gets plays; what they do not get is push updates, so the view is only as
fresh as their last request. Two defects below spoil even that fallback.

## 5. Detection — the "did we get it" check

The right ledger already exists and needs no new infrastructure.

When a game ends, `GamePipeline._end_game` writes the final blob with
`is_live=False`, which selects `LONG_FINITE` — **30 days** — for both
`sr:{league}:game:live:{id}` and `sr:{league}:game:live:seq:{id}`. So after a
captured game, those two keys persist for a month carrying the final status, the
full moments list, and the final `seq`. That is the exact analogue of the
`SR_PROBABILITIES` per-subject message count.

The check is therefore: **for every universe game whose kickoff has passed, assert
`sr:nfl:game:live:{id}` exists and its `seq` is greater than zero.** Absent ⇒ the
game was never streamed. Present with a low `seq` ⇒ streamed partially.

⚠ Note the trap: **during** a game the same key carries a 60-second TTL
(`GAME_LIVE = 60`). Mid-game presence proves capture is live *right now*; it is
not a historical record until the game goes final. A detector must not read the
key mid-game and conclude anything about the whole game.

Two gaps make this harder than it should be:

- **The worker does not log its game list usefully.** `workers/live.py` calls
  `logging.basicConfig` (stdlib), not the repo's structured JSON logger. So
  `logger.info("worker_starting", extra={"games": …})` reaches Cloud Logging as
  the bare string `INFO:__main__:worker_starting` — **the `games` list is
  dropped**. You cannot tell from the logs which games a worker adopted. Verified
  against the live logs.
- **Redis is VPC-private**, so a detector must run inside the VPC (a Cloud Run
  job) or go through an authenticated `/live` read.

## 6. Three code defects

### 6.1 `GamePipeline.reconcile()` is never called — reconnect backfill does not run

`grep -rn "\.reconcile(" src/` returns **nothing**. The method is written,
documented, and covered by `test_reconcile_e2e.py` and `test_game_pipeline.py`,
but `workers/live.py` runs only `pipeline.run()`, and `PushConsumer.run()`
absorbs reconnects **inside** its own loop and keeps yielding. The pipeline's
`async for` therefore never observes a reconnect boundary, so there is no moment
at which reconcile would fire.

**Effect:** when a push connection drops, plays that occurred during the gap are
lost permanently from the moments list. The score and clock self-heal, because
every payload carries a fresh `payload.game` summary — but the play-by-play list
keeps a hole for the rest of the game.

**Note for the runbook:** `first-game-golive-runbook.md` lists "REST
reconnect-backfill runs for the first time ever" as a known first-game risk. It
will not run at all. That line should change.

### 6.2 A mid-game play-by-play is cached for 30 days

`services/games.get_play_by_play` applies `ttls.GAME_PBP` = `LONG_FINITE` = 30
days **unconditionally**. Its docstring says "completed games only in Phase 1" —
but two live paths call it:

1. `Supervisor.build_pipeline`'s `backfill` closure (reconcile and finalize), and
2. `services/live.get_live_snapshot`'s cold-miss rebuild.

So the **first** call made while a game is in progress freezes a partial
play-by-play into Redis for a month. Every later reconcile, every later cold-miss
rebuild, and every post-game `GET /sr/games/{id}/pbp` then reads that truncated
copy — for 30 days, with no way to tell it is short.

**This is the more serious of the two cache defects**, because it survives the
game. Defect 6.1 currently masks half of it: with reconcile dead, only path 2
fires. But path 2 fires on *every* `/live` request whenever the worker is idle —
which is the exact condition we were in on 08-07.

**Worth checking against production:** if the app called `/live` for the 08-07
CAR@ARI game while it was in progress, `sr:nfl:game:pbp:f112fe5a-…` may right now
hold a truncated play-by-play that will serve until early September. Confirming
needs a `trader` bearer or in-VPC Redis access; neither was available in this
session.

### 6.3 A pre-kickoff boxscore can hide a live game for an hour

`get_boxscore` always caches with `ttls.game_box(is_final=False)` = `GAME_BOX_PRE`
= **1 hour**, and the code comment says so deliberately ("we can only know 'final'
after the fetch, so pick the conservative pre-game TTL"). But `services/live`
decides live-ness from that cached status. A single request in the hour before
kickoff caches `status="scheduled"`, and for up to an hour after kickoff every
`/live` cold miss then raises 404 — **the live view is unavailable during the
first quarter of the game it is for**.

With the worker running this is invisible: the worker's blob is present, so
`/live` never reaches the cold-miss branch. It only bites when the worker is idle,
which is precisely when the fallback is load-bearing. **The idle-worker fallback
is not a safe substitute for running the worker.**

---

## Thursday 2026-08-13 — the games

Pulled live from `…/nfl/official/production/v7/en/games/2026/PRE/schedule.json`.
All are NFL, so all are in the 170-team universe. **The brief lists five; there
are six** — ARI@LV was missing, and IND@NE is 23:30Z, not 23:00Z.

| Kickoff (UTC) | Match | Sportradar game id |
|---|---|---|
| 2026-08-13 23:00 | DET @ CIN | `d75404c4-fb21-4239-85e8-9fa8ce5283f5` |
| 2026-08-13 23:00 | GB @ PIT | `cedce52c-a5d5-4f58-a5fd-e3ecfeadbecf` |
| 2026-08-13 23:30 | IND @ NE | `6c9b817d-140c-4568-94b9-7f908b014686` |
| 2026-08-14 00:00 | ARI @ LV | `4fb56678-33e0-4c8f-8a17-6447ddb49fa9` |
| 2026-08-14 00:00 | LAC @ HOU | `45a00140-5e74-43d7-ba3a-e32d5b72a2df` |
| 2026-08-14 01:00 | TEN @ SF | `e715356e-bd9e-43cf-81b2-c7fa5ef142e9` |

Three more follow on 2026-08-14 at 23:00Z (MIA@WAS, TB@NYJ, DEN@ATL).

### The concurrency question — dissolved by PR #17

Under the old explicit-list model each instance opened one push connection **per
configured game**, so six games meant 12 concurrent Sportradar subscriptions
against an unknown connection limit. That was the largest unknown in a Thursday
go-live.

Discovery mode makes it **one connection per instance — two in total — regardless
of how many games are live.** The question no longer needs answering, and no
reduced game list is needed to manage it.

### Preseason schedule work in flight

`feat/preseason-schedule` (uncommitted, working tree) rewrites
`get_current_schedule` to derive the served week from **game status** rather than
Sportradar's `current_week` pointer, so the schedule can show upcoming preseason
fixtures before Sportradar advances its own pointer. That is the same universe of
games the live worker needs to adopt, and it is the natural feeder for Design A's
discovery. Keep the two changes separate for Thursday; converge them after.

---

## The Thursday decision

PR #17 is ready but **unreviewed and undeployed**. Two ways to take Thursday, and
this is a genuine judgement call rather than an obvious answer.

**Option 1 — deploy PR #17.** Every game on Thursday and every game after it is
captured with nothing to remember, on two connections. But it is new code on the
live path, merged and deployed within a day of the first-ever real-feed run. The
multi-game fan-out is unit-tested but has never seen a real stream.

**Option 2 — pin the games explicitly, deploy #17 after.** Set `LIVE_GAME_IDS` to
the six ids below on the code that is already running in production. That path is
the one the go-live runbook was written for and the one prod has been sitting on
since 08-11 — but it costs 12 concurrent Sportradar connections against an unknown
limit, and it is the manual step that failed on 08-07.

A middle option exists and is probably the best of the three: **deploy #17 and pin
`LIVE_GAME_IDS` to one or two games.** An explicit list still wins over discovery,
so this exercises the new code's deploy without relying on its fan-out, and keeps
connections at 2–4. Discovery then takes over for the 08-14 games once the first
real capture has been watched.

Whichever is chosen:

1. Apply via Terraform, **hours** before 23:00Z, not minutes. The worker reads its
   mode only at boot. Verify `0 to destroy`, no replacements, and no `allUsers`
   binding in the change set.
2. Watch in order: worker logs (`worker_starting mode=…`, then `game_discovered`)
   → Redis blob → Centrifugo → device.
3. Post-game, read `sr:nfl:game:live:{id}` for each game and record the final
   `seq`. That is the first entry in the capture ledger.
4. Capture the real push stream to a fixture. It is the first-ever real-feed
   capture and worth more than every simulation recording combined.

## After Thursday

1. Fix 6.2 first — it is the one that outlives the game. Give a non-final
   play-by-play a short TTL, the way `game_box` already switches on `is_final`.
2. Fix 6.3 with the same switch, so a live boxscore is not held for an hour.
3. Wire 6.1, or delete `reconcile()` and stop claiming a backfill exists.
4. Switch the worker to the repo's structured JSON logger. PR #17 works around the
   dropped `extra` dict by putting the mode and ids in the message string; the
   proper fix is the JSON logger the API already uses.
5. Build the capture detector against the 30-day final blob, and give it the
   project's first alert policy for this service.
6. Check whether `sr:nfl:game:pbp:f112fe5a-…` is holding a truncated play-by-play
   for the 08-07 game (defect 6.2). Needs a `trader` bearer or in-VPC Redis.

## Coordination

Hasan owns Centrifugo, Redis and the VPC. **None of this needs his approval** —
the worker pool is this repo's own deployable, and a worker publishing to
`game:{id}` adds a small load to a namespace built for it plus a few KB of Redis
per game. What is worth *telling* him, not asking:

- The worker will publish to Centrifugo for the first time. The worker → internal
  ILB VIP hop (`10.0.3.12:8000`) has never been exercised and is proven by that
  first publish.
- Memorystore is shared with Centrifugo under `allkeys-lru`. Live blobs are small
  and short-TTL, so the added pressure is negligible — but he asked to be told
  about anything that touches that instance.
