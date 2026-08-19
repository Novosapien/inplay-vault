---
description: "Investigation brief for a new session: does the sportradar live worker capture play-by-play for real games, who flips LIVE_GAME_IDS, and what must be true by the next preseason game"
---

# Investigation brief — the live worker and play-by-play capture

> **For:** a fresh session, working in `inplay-sportradar-service` (+ GCP
> project `inplay-497712`). **From:** the 2026-08-11 MM night session
> (George/Hasan). **Trigger:** the 08-06 ET preseason game
> (Cardinals–Panthers) happened and we do not believe ANY of our systems
> streamed its play-by-play. The market maker's path is NOT the concern —
> see "what is already known" below. The app's live-game path is.

## The question, in one line

How do we GUARANTEE that when a real NFL game happens, the app's
play-by-play/live-game stream captures it — and how do we know, after
the fact, whether we did?

## What is already known (verified 2026-08-11 night — do not re-derive)

1. **The MM probabilities path is fine and separate.** The
   `inplay-mm-publisher` worker pool (Cloud Run, deployed 08-11) PULLS
   SR's standalone Probabilities product: daily discovery from
   `GET /probabilities/production/v1/en/sports/sr:sport:16/schedules/{date}/schedule.json`
   (key: Secret Manager `inplay-probabilities-api-key`), adopts any game
   touching the 170-team universe, polls each at 15 s pre-kickoff /
   500 ms live, publishes to JetStream `SR_PROBABILITIES`. Verified live:
   the schedule lists NFL Preseason (Thursday 08-13 23:00Z: CIN–DET,
   PIT–GB, NE–IND), and the missed 08-07 game's timeline holds 1,293
   readings — SR archives, so missed probability data is recoverable on
   demand. ⚠ One known edge, worth fixing while you are in there:
   discovery runs once per UTC date, so a game kicking off at/after
   00:00Z (8pm ET or later) is adopted only AT kickoff — discover
   today+tomorrow each pass to restore the pre-kickoff ramp.
2. **The live worker is IDLE by configuration.** Cloud Run worker pool
   `inplay-live-worker` (+ `-testing`), 2 instances, Redis-lease
   failover: SR Push v7 → per-game state machine (monotonic `seq`,
   Redis snapshot) → Centrifugo `game:game:{gameId}`. Its `LIVE_GAME_IDS`
   env is EMPTY ("flip at season" — trading-architecture.md §3.8). With
   it empty, NO play-by-play flows to the app, regardless of what SR
   sends. This is why the 08-07 preseason game produced nothing.
3. The platform doc for the surrounding architecture is
   `trading-architecture.md` (Downloads copy on George's machine; §3.8
   is the SR service). The service repo is
   `~/Programming/inPlay/inplay-sportradar-service`.

## What to investigate

1. **The gating model.** Is `LIVE_GAME_IDS` the only switch? Read the
   live worker's config and consumer code. Who is meant to set it, when,
   and per what runbook? Does anything alarm when it is empty on a game
   day?
2. **Discovery for the live worker.** The mm-publisher discovers games
   automatically; the live worker does not. Should it? Propose (and, if
   cheap, build) schedule-driven discovery so the worker adopts universe
   games without a manual flip — or a deliberate decision that manual
   gating stays, with a written runbook + alarm instead.
3. **Push entitlement and preseason coverage.** Confirm our SR Push v7
   subscription actually carries preseason games (the probabilities
   product does; push is a different entitlement). A short live probe
   during Thursday's 23:00Z games settles it.
4. **Recovery after a miss.** SR Push holds no state; the documented
   recovery is pulling the REST `pbp` feed (see the t0 integrations doc
   §5 pattern). Confirm: can we backfill a missed game's play-by-play
   after the fact, the way the probabilities timeline could be
   backfilled? What would the app do with a backfill, if anything?
5. **Detection.** Build the "did we get it" check: something that, for
   each universe game on the schedule, verifies the game stream flowed
   (Centrifugo `game:game:{id}` published / Redis snapshot exists) and
   alarms when it did not. The MM side's equivalent ledger is the
   `SR_PROBABILITIES` message count per game subject.
6. **Thursday 08-13.** Whatever the long-term answer, make Thursday
   work: three universe preseason games at 23:00Z (CIN–DET, PIT–GB,
   NE–IND) + two more crossing midnight UTC (HOU–LAC 00:00Z, SF–TEN
   01:00Z on 08-14). If the flip stays manual, the deliverable includes
   WHO sets `LIVE_GAME_IDS`, to WHAT values, and WHEN.

## Constraints and courtesies

- Hasan owns the platform side of this service historically —
  coordinate before changing deployed pools (the 08-11 sessions changed
  his boxes under George's explicit ruling; get the same ruling or his
  ack for live-worker changes).
- The MM night session left `inplay-mm-publisher` untouched and
  running; do not restart pools casually — the C15 Redis lease is
  unbuilt, so each pool runs exactly 1 publishing instance.
- Record findings + changes in this vault (a session note beside this
  brief, or the platform docs), and if service code changes: PR to
  `inplay-sportradar-service` per its conventions.
