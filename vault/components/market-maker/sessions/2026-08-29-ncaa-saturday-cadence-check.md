---
description: "Read-only production check on the first NCAA Saturday: the engine holds its 500 ms cadence with 92% headroom, Sportradar changes every 7 s, and one live book is frozen behind the marketable guard"
---

# 2026-08-29: the cadence check on the first NCAA Saturday

> **Who:** George + Claude
> **Type:** measurement (read-only production check)
> **Refs:** [[market-maker/parameters]] rows 221–229 ·
> [[market-maker/build/runtime]] · [[market-maker/build/ingestion]] ·
> `N41` `N55` · `inplay-sportradar-service/src/app/workers/mm_publisher/`
> **Window:** 2026-08-29 16:46Z–17:05Z · engine `supervised48` / `CFG-0046`

## What we did

George asked one question: does the maker run at a cadence that suits
live NCAA games? We measured the whole chain in production, read-only —
`ps`, `journalctl`, `gcloud ... describe`, and a 40 MB tail of the live
journal. No restart, no write, no config change.

The check ran during the noon-ET window of the first NCAA Saturday. The
maker quotes **138 NCAA books** and no NFL.

## What we learned

### ⭐ The engine meets its cadence, and Sportradar is the real limit

| Stage | Configured | Measured |
|---|---|---|
| SR → publisher poll (live game) | 0.5 s | **1.16 s** |
| **SR's own NCAA probability change** | — | **median 7 s** · mean 13 s · p90 25 s · max 153 s · min 2 s |
| Engine tick / valuation sweep | 0.5 s | 0.5 s, **`missed_intervals=0`** over 1,423 sweeps |
| Engine LIVE redraw | 0.5 s | holding; `cycles=138` on every tick |
| Converger | 0.25 s · 128 instr/pass | backlog 1–11 books of 138, clears |
| Engine CPU | 2 vCPU | **7.5% of one core**, load average 0.00 |

The source changes every 7 s at the median. The poll already oversamples
it about 6 times, and the redraw about 14 times. **The cadence question
is answered on the input side, not the engine side.**

Measured on `sr:sport_event:70894628` (kickoff 16:00Z): 1,040 reading
events carried only **55 distinct probabilities**. The rest are liveness
confirmations. No book suspended and no re-offer was withheld in 6 hours.

### ⚠ `MMPUB_POLL_LIVE_S=0.5` is set but cannot take effect

The env var IS on the `inplay-mm-publisher` worker pool. The loop cannot
honour it: `run_forever(..., tick_s: float = 1.0)` in
`inplay-sportradar-service/src/app/workers/mm_publisher/worker.py:477`
is a hardcoded default with no settings field and no env override. One
tick per second is the floor.

Measured: 513 fetches in 597 s on the live game = **one poll per
1.16 s**. [[market-maker/parameters]] row 221 records 500 ms as "ruled
08-11 · deployed". That is true of the env and false of the behaviour.

**Cost, measured rather than assumed: about 0.3 s of average detection
latency against a source that changes every 7 s.** Filed as `N55`, not
fixed — a publisher deploy mid-slate risks more than it buys.

### ⭐ The fetches ARE concurrent — the 14-08 serial-fetch worry is closed

`PublisherWorker.tick()` gathers every due game in one `asyncio.gather`.
The recorded fear that "the serial-fetch shape caps out near ~35 live
games" ([[market-maker/parameters]] row 240) no longer describes the
code. One round costs one SR round-trip, not N of them.

### ⚠ One live book is frozen: IPTCNCTH

`MARKETABLE_GUARD_STALLED` fired four times from 16:18Z, and 148
refusals landed in 30 minutes. Its sell target sits behind a touch at
40.39/40.40 x182 and **no submit or replace has left for that book
since**. `IPTCHFRG` did the same at 16:05Z and cleared.

This is `R-Q09` refusing and `N41` alarming, both as designed. The
effect is still a live NCAA book that does not reprice. The guard is
the only thing in the whole chain that broke cadence today.

### 📝 The dead games cost more polls than the live ones

`MMPUB_POLL_POST_GAME_S` is unset, so it takes the 2.0 s default — the
LIVE rate. 33 finished games from 27–29 Aug are fetched every 2 s. Of
11.4 SR fetches/s measured on the pool, about 14 calls in every 16 go to
games that will never move again. The behaviour is `N40`'s "never
retire" ruling working correctly; only the rate is wrong.

### ⚠ The testing pool polls production Sportradar

`inplay-mm-publisher-testing` fetched
`probabilities/production/v1/.../sr:sport_event:70894628/timeline.json`
at 17:02:35Z — the same live game as the production pool, seconds apart.
Duplicate quota spend. Whether it also publishes on the production
subject depends on the Redis fence, which we did not read.

### 📝 The load we measured is not the peak

83 games are tracked. **65 sit at the overnight tier** — today's later
kickoffs and tomorrow's. The 16:46–16:58Z window held ONE game with a
moving probability; by 17:05Z the live tier held 7. The evening slate is
the real test.

## What went wrong / got stuck

- Nothing broke. The recorded **~35% missed-sweeps fault did not
  reproduce** — zero missed intervals across 1,423 sweeps. ⚠ Do not
  read that as closed: the fault was measured at three live games under
  the pre-08-13 `sweep_max_interval_s`, and today's window held one to
  seven. Re-measure at peak.
- The first journal parse used the wrong schema and reported "0
  securities with readings". The journal wraps every event as
  `{"kind": ..., "record": {...}}`; the event type is
  `record.event_type`, and a probability reading carries `security_id:
  null` with the pair inside `payload`.

## Decisions made *(mirrored into [[market-maker/decisions]])*

- 📝 No decision. The session is a measurement. The one ruling it
  invites — whether to make `tick_s` settings-driven — is filed as
  `N55` for George.

## Questions opened / closed *(mirrored into [[market-maker/open-questions]])*

- **`N55` opened** — the publisher's 1 s tick makes every poll tier
  under 1 s unreachable, and `MMPUB_POLL_LIVE_S=0.5` is inert.

## Next

1. **Watch `IPTCNCTH`.** If the guard still refuses after the touch
   moves, the book needs an operator. It is the only broken cadence on
   the board.
2. **Re-measure at peak tonight** — missed sweeps, converger backlog,
   engine CPU, and the publisher's round time with ~30 games at the live
   tier. Today's numbers were taken at one to seven.
3. **Then rule `N55`**, out of hours: make `tick_s` a
   `MMPUB_TICK_S` setting, and set `MMPUB_POLL_POST_GAME_S` above the
   live rate so finished games stop dominating the round.
4. Ask whether `inplay-mm-publisher-testing` should hold a production
   Sportradar key at all.
