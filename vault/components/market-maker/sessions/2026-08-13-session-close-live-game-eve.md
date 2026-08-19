---
description: "The closing note for the 08-11→08-13 marathon: full-market operation, the synthetic game day pass, three incidents fixed, the always-quoting ruling, and live-game-eve state"
---

# 2026-08-13 — session close: the machine runs the full market; tomorrow it meets a real game

> **Type:** the closing index for one continuous working session,
> 08-11 evening → 08-13 ~01:00 UTC. George + Claude.
> **The period's notes, in order:**
> [[market-maker/sessions/2026-08-11-taker-cutover]] ·
> [[market-maker/sessions/2026-08-11-full-book-seed]] ·
> [[market-maker/sessions/2026-08-11-full-book-joint-run]] (addenda 1–7) ·
> [[market-maker/sessions/2026-08-12-session-roll-storm]] (addenda 1–7).
> This note records what those do not: the closing rulings, the cadence
> calibration, the replay-probability clarification, and live-game-eve
> state. **Repo state:** MM PRs #21, #22, #24 open;
> `feat/session-boundary` deployed by bundle (two commits). **Vault:**
> all edits uncommitted on `docs/t0-plain-english-guide`.

## The arc, in one paragraph

The session took the machine from six QA books to the FULL market: all
180 symbols seeded on both accounts, `.TEST` twins built into the
engine, JETS's dead anchor walked up by hand, and maker + taker trading
house-to-house on every book. The synthetic game day then PASSED to the
cent (A2 stage 2 + A3/A4/A5). Production then taught three lessons —
the venue's silent nightly book wipe, the checkpoint stall-sweep, and
the sweep/repost spiral — and the first two are fixed and deployed
(PR #24); the third produced the session's standing ruling. Storage got
a durable home. Tomorrow the machine meets its first real live games.

## What the earlier notes already carry (index)

- **The taker:** cutover to one owner (`snt-1.service`), rule 7 (floats
  are positions), T-S05 field-proven ×3, the 20-hour undetected halt
  (our miss — health checks must read the last control action), the
  fetched_at staleness defect (top taker build item).
- **The market:** the 173+175 position-transfer seeds (ledger receipts),
  PR #22 `.TEST` twins, the JETS anchor walk (T20 closed ourselves; the
  anchor FOLLOWS prints, ~3–5 min refresh), the empty-book LmtPerc gate
  proven GONE, the STX reseeder's daily ~10:15Z schedule (T19).
- **The synthetic game day:** corr +0.989/−0.990, ±$2.17 to the cent,
  full lifecycle derived, official result minted once; the three-run
  harness lessons (fresh game id · purge · Z-stamps · the invisible
  poison counter).
- **The incidents:** the 23:59 ET session roll (B1 overturned, T14
  answered-by-observation), the 8-hour phantom storm, the hourly
  checkpoint stall-sweeps, the VATH false-positive forensics (no fill
  was ever lost; a position message was), the 4-minute sweep/repost
  spiral (my gzip triggered it; the loop is a real defect).
- **The fixes (PR #24, 702 tests):** fork checkpoints (3 clean hourly
  writes since) · gone-retire · the session clock (close 23:59 ET /
  open 00:02 ET) · terminal-order pruning + scoped dedup retention
  (schema 6) · the GCS journal archive (`gs://inplay-mm-journals`,
  17 runs, 8×) · the hardened archive script (refuses while trading).
- **The cleanup:** orphan orders from retired config versions swept via
  `cancel_all` (George's call); the stale-orphan hazard named — a
  restart without cancel_all leaves invisible orders resting.

## What this note adds

### ⭐ George's ruling: the engine must ALWAYS be quoting

"Busy" starving the heartbeat is a design flaw, not an ops problem.
The architecture must make quote publication unconditional. The agreed
build order (not yet built):

1. **Bounded drain per tick** — no tick may process an unbounded
   backlog; starvation becomes structurally impossible.
2. **N31 group commit** — batch the fsyncs. This is not hardening; it
   is THE gap to a game day (see the calibration below).
3. **Progress-aware heartbeat** — the beat means "the loop advances",
   not "the loop is idle"; the dead-man then fires on death only.
4. **The deeper split (own design pass):** quote publication on its own
   timer over the latest consistent state — ingestion lag makes quotes
   stale, never absent.
5. The dead-man breaker (paced re-stand after a sweep, alarm on the
   second sweep) as defence-in-depth behind all of the above.

### ✂ The cadence calibration (correcting this session's own claim)

The 24-hour run did NOT republish books at 500 ms. Measured on
supervised17 (17,161 s):

- The tick loop held **1.91 ticks/s vs the 2.0 target** — the engine
  EVALUATES 180 books every 500 ms. That part is proven.
- Books REPUBLISHED on the overnight dwell: 26.5 real replaces/s ≈ one
  full 6-level book every **~41 s**. Only CHIE/RAVE ever ran at the
  500 ms LIVE cadence, for ~30 min of synthetic game.
- Journal load ran at **70 events/s ≈ 12% of the ~579/s fsync ceiling**.
- A real NCAA Saturday (~70 LIVE books) needs **~2,520 events/s ≈ 435%
  of the ceiling**. Tomorrow's ~6 live books fit comfortably; Saturday
  does not. **Group commit is the difference.**

### The replay-probability clarification (for future dress rehearsals)

The playback service (the 17 `.TEST` recordings) carries play-by-play
ONLY — no probabilities. The Probabilities API returns a finished
game's timeline as one archive, not a progressive feed. So in ANY
replay, WE are the probability feed: `~/synthetic_game_day.py` fetches
the archive once and re-publishes it paced. A joint app+MM dress
rehearsal therefore needs the playback session and our driver started
together and time-aligned to one synthetic kickoff — a real test case,
not yet filed in the test plan.

### Live-game-eve facts (13 Aug, tonight/tomorrow)

- The slate: **CIN–DET, PIT–GB, NE–IND at 23:00Z** (all universe
  games), HOU–LAC 00:00Z and SF–TEN 01:00Z crossing UTC midnight.
- The publisher discovers them from the probabilities schedule endpoint
  (probed live with our production key; the missed 08-07 game returned
  1,293 readings — the entitlement covers preseason).
- The MM path is hands-off: publisher polls (15 s pre-kickoff, 500 ms
  live) → `SR_PROBABILITIES` → the engine reprices → the taker derives
  its states. ⚠ The ONE untested link: the publisher's live polling
  loop during a real game.
- ⚠ The UTC-midnight discovery gap: the two late games are adopted only
  at the 00:00Z discovery pass — LIVE polling starts at kickoff but the
  pre-kickoff ramp is lost. Known, filed with the sportradar session.
- ⚠ The app's play-by-play path stays gated (`LIVE_GAME_IDS` empty) —
  the parallel session owns that
  (`vault/drafts/live-worker-pbp-investigation-brief.md`).
- JetStream retention facts (Hasan + verified): SR_PROBABILITIES 7 d ·
  ORDERS 24 h · POSITIONS 24 h · MARKET_DATA 1 h. The bus is not an
  archive; the journal (+ GCS) is.

## State at close (01:0x UTC)

| Thing | State |
|---|---|
| Maker | `supervised20` / CFG-0019, 180 books, journal `/var/lib/mm/supervised20/`, carries PR #24 + #22 + pruning (schema 6) |
| Taker | `snt-1.service`, SNT-CFG-0013, journal `snt10`, 180 books, AUTO |
| Books | 180/180 two-sided on a cleared venue book; COWB carries the STX reseeder's junk (not ours) |
| Tonight | The session clock's first live firing at 23:59 ET — monitor armed on `supervised20.log` |
| Archive | `gs://inplay-mm-journals` — all 17 runs; local copies NOT yet swept (George's call pending) |

## Next (the standing queue)

1. **Watch tonight's boundary** (SESSION close/open lines, no storm).
2. **Tomorrow's live games** — the first real end-to-end run.
3. The always-quoting build (bounded drain → group commit → heartbeat).
4. The taker's `fetched_at` fix + T-S05 compare-source fix.
5. C2 on supervised12's archived journal · the Edwin round (+ the new
   Single-Price-Open question) · Rob (T19 reseeder) · Hasan (B2, the
   NATS change notes owed).
6. Housekeeping: commit the vault branch · merge PRs #21/#22/#24 ·
   sweep archived local journals · the repo CLAUDE.md rule additions
   (rule 7 refinement, the health-check rule) once the checkout frees.
