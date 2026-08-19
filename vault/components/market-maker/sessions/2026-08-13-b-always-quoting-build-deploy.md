---
description: "Always-quoting steps 1–3 built (bounded drain, N31 group commit, progress-aware heartbeat) and deployed the same night as supervised21/CFG-0020"
---

# 2026-08-13-b — the always-quoting build, steps 1–3, built and deployed

> **Type:** build + deploy session, ~00:30–01:30 UTC. George + Claude.
> George's calls: "let's do this" (the build) and "can't we just deploy
> it now" (the cutover, ahead of tonight's boundary and tomorrow's
> games). **Repo:** MM PRs #25 → #26 → #27, stacked on #24's branch.
> **VM:** `supervised21` / **CFG-0020**, journal
> `/var/lib/mm/supervised21/`, branch `always-quoting-deploy`
> (= `d5180eb`) by bundle.

## What we did

Built steps 1–3 of the 08-13 always-quoting ruling, in order, each with
its own stacked PR, then deployed all three:

1. **Bounded drain per tick (PR #25).** Both drains stop at a per-tick
   cap (`drain_max_readings_per_tick` 256 ·
   `drain_max_venue_per_tick` 512, 🟡 OURS); the leftover waits one
   tick. A capped tick logs `DRAIN_CAPPED` — an alarm, not a mode.
2. **N31 group commit (PR #26).** `Journal(group_commit=True)` defers
   per-append fsyncs; `run()` commits the whole tick in ONE fsync,
   before any await — nothing a tick produced leaves the process before
   its batch is on disk. ✂ §7.4's letter superseded (recorded in
   decisions). The ~579 events/s fsync ceiling stops binding.
3. **The progress-aware heartbeat (PR #27).** The beat certifies "ticks
   are completing"; it is WITHHELD once no tick completed within
   `heartbeat_stall_threshold_s` (5 s, 🟡 OURS) — a wedged engine's
   book gets pulled by the dead-man ~9 s after the wedge instead of
   never. `HEARTBEAT WITHHELD`/`RESUMED` log the transitions.

**716 tests** · ruff + mypy-strict clean at every step. Vault updated
per step (decisions, parameters, N31 closed, build/runtime +
build/event-core).

## The cutover (receipts)

1. ~01:14Z — taker HALTED on `snt.control.snt-1` (journalled
   `{"action": "halt"}`, "0 cancels out").
2. Maker SIGTERM → clean exit ("stopping after 16151 ticks").
3. The gateway's dead-man fired on the silence (1,608 cancels), then
   the explicit `gateway.orders.mm.cancel_all` followed (George's
   rule: never assume). Open orders → **28**, the known not-ours floor.
4. VM repo → `always-quoting-deploy` (`d5180eb`) via git bundle;
   `run_supervised21.sh` = the 20 script with journal `supervised21`
   and **CFG-0020**.
5. ~01:18Z — engine up: **1,594 instructions for 180 securities**,
   fresh journal, replayed 0.
6. ~01:21Z — taker RESUMED (journalled), filling within seconds
   (BYUC 182@62.21, AZSD 35@49.49).
7. Gateway after: **1,630 open orders · dead-man unlatched · beat
   126 ms fresh**.

## First production evidence (minutes in)

- **Group commit works as designed:** boot's ack burst journalled as
  `drained=121 … committed=122` — 122 lines, ONE fsync (was 122
  fsyncs). 12,161 events drained in the first ~370 ticks, zero
  `DRAIN_CAPPED`.
- ⭐ **`MISSED_SWEEPS` is GONE.** supervised20 logged it on every
  sweep tick (each sweep tick paid ~130 fsyncs ≈ 220+ ms and blew the
  0.625 s slot); supervised21 shows zero. The fsync ceiling was
  costing sweep cadence in normal running, not only on game days.

## What we learned

- The dead-man swept the book (1,608 cancels) BEFORE the explicit
  cancel_all landed — both paths ran; the explicit sweep remains the
  rule because the dead-man arms only when the book holds orders.
- The `/health` endpoint on the gateway (`localhost:8080`, X-Ops-Key)
  carries `open_orders` + the full dead-man state — the restart
  verification one-liner.
- The gateway HTTP binds VPC-only but is NOT reachable from the MM VM
  (`10.0.1.2:8080` → connection refused from there); go through the
  gateway VM's localhost.

## Open / carried

- Steps 4 (decoupled quote publication — its own design pass) and 5
  (the dead-man breaker) remain unbuilt.
- The drain-cap re-size after group commit (venue cap must RISE for
  Saturday's ~1,050 acks/tick) — measure engine time first.
- PRs #21/#22/#24/#25/#26/#27 all await George's review; the VM runs
  ahead of the merges (deliberate, George's call tonight).
- supervised20's journal → GCS archive when convenient (engine idle
  rule: the archive script refuses while trading — it will see the
  NEW engine trading, so archive 20's dir explicitly).

## Next

1. **03:59Z tonight** — the session clock's first live firing, now on
   supervised21 (monitor re-armed on `supervised21.log`).
2. **23:00Z today** — CIN–DET, PIT–GB, NE–IND: the first real live
   games, now with `committed=` visibility on the game-day load.
3. Step 4's design pass when the watches are quiet.

---

## Addendum 1 (11:3xZ) — the boundary VERDICT: PASS, and one finding

**The session clock's first live firing worked.** Read retroactively at
11:32Z (below on why):

- `SESSION close — 2026-08-12 ET` fired on schedule; **1,590 resting
  orders expired locally**; the closed window ran sweeps with
  `cycles=0` (the gate held). `SESSION open — 2026-08-13 ET` fired
  ~3 min later; the full universe cycled and the re-stand's acks
  drained over the following ticks in bounded batches.
- **Zero REJECTED, zero CONFLICT in the whole 71k-tick log. The 08-12
  phantom-cancel storm did not recur.** The journal carries exactly
  two SESSION_BOUNDARY events (idempotent, one per phase). No dead-man
  fires; the engine never stopped; the taker traded through the
  morning (fills across books, `.TEST` twins included).
- B1's overturn and T14's answer stand confirmed by a LIVE firing.

**The observation outage (a lesson, not an incident):** local gcloud
credentials expired at 03:54Z — five minutes before the close — and
every monitor poll through the window failed. The engine was
unaffected; the log held the verdict for the morning. ⚠ Rule for game
day: **refresh gcloud auth BEFORE an observation window, or arm the
watch on the VM itself** — a local watcher dies with local auth.

**The finding — `MISSED_SWEEPS` is back, and it names the next
bottleneck.** 8,197 of ~71k ticks (11.5%) missed a sweep slot: mostly
`=1`, but 1,335 ticks logged `≥2` — each a transient §3.5 confidence
deduction. The correlation is clean: missed ticks drain **p50 99 /
p90 178 acks** vs 24/88 overall (first miss: tick 317, `drained=180`).
With the fsync cost gone (`committed=181` in ONE fsync on that very
tick), the slip is **engine time on ack bursts** — ~0.5–1 ms per
drained event, exactly the post-group-commit constraint the build
predicted. The overnight dwell republishes books in synchronized
waves, so the acks arrive in ~100–200-event clumps. Feeds directly
into: the drain-cap re-size measurement · step 4 (decoupled quote
publication) · possibly de-phasing the dwell waves. Filed, not fixed —
quotes never stopped and no cap was hit.

**Health at 11:32Z:** tick 71,108 · RSS 190 MB (pruning holding) ·
journal 2.67 GB ≈ 72 events/s, the supervised17 rate.

---

## Addendum 2 (11:5xZ) — live-game watch prep: our side is READY

The path is hands-off by design; the prep was receipts, not actions.

**Tonight's slate (probabilities schedule, fetched live):**
`sr:sport_event:71548090` CIN–DET **23:00Z** ·
`sr:sport_event:71548092` PIT–GB **23:00Z** ·
`sr:sport_event:71548094` NE–IND **✂ 23:30Z** (the close note said
23:00Z — the schedule says 23:30Z). HOU–LAC 00:00Z and SF–TEN 01:00Z
sit on the 08-14 UTC schedule — adopted at the next 00:00Z discovery
pass, the known gap, unchanged.

**Receipts, our side:**

- **Maker:** `MM_READINGS=bus` bound at boot ("durable bound to
  SR_PROBABILITIES") · TEAM_BINDINGS verified for all ten teams
  (tonight's six + the late four) · boundary survived · group commit
  live. Nothing to do at kickoff.
- **Taker:** up since 08-12 22:39Z, `sr.probabilities.reading.>`
  subscribed (last-per-subject), **zero** "schedule feed unavailable"
  in 7 days. ⚠ Operating rule: **no taker restarts during games** —
  the boot-LIVE redelivery wrinkle (`fetched_at` fix still owed) only
  bites on a restart.
- **Publisher:** pool Ready · `MMPUB_POLL_LIVE_S=0.5` · the 00:00Z
  discovery pass ran and fetched today's schedule (200 OK). Adoption
  is not logged, so the FIRST verifiable receipt is the 15 s
  pre-kickoff poll onset at ~22:00Z — the watch reports it.
- **Stream:** SR_PROBABILITIES healthy (2,256 msgs retained,
  subjects `sr.probabilities.>`).

**The watch (the 03:59Z auth lesson applied):**

- **On the VM** (survives local auth death): `~/gameday13_watch.sh` →
  one line per minute into `~/gameday13.log` (stream seq · engine
  readings/min · alarm counts · tick · engine/taker liveness), running
  now through 04:35Z 08-14 — so it also covers tomorrow's 03:59Z
  boundary.
- **Locally**: a monitor from 21:50Z relays poll onset, reading-rate
  transitions, alarms, and publisher errors; its POLL_FAILED lines
  mean "reauth gcloud", never "the machine is sick".

**Still genuinely untested until tonight:** the publisher's live
polling loop during a real game — the one link with no prior
production run.

---

## Addendum 3 — the daily reference feed goes to its own session

George: Edwin sent material on how the daily report may be created —
analyse it in a DEDICATED session, design our side, **deploy nothing**.
Brief written: `vault/drafts/daily-reference-feed-analysis-brief.md`
(Edwin's 28-07 feed engine + the 08-09 EV handoff + N19/N23 gates).
Also from the same conversation: the daily file is two real numbers per
team — `expected_remaining_wins` sets the level, `sigma` sets the
width; the engine derives everything else. A false alarm on "the maker
stopped quoting" was checked to the metal: engine sweeping, 3,230 open
orders, MD cache fresh to the second, taker filling — all healthy at
12:43Z.

---

## Addendum 4 (13:xxZ) — ⭐ the panel's ACTIVE/DEFENSIVE flapping IS the missed-sweep bug (George's catch)

George asked whether the missed sweeps explain the market state showing
ACTIVE or DEFENSIVE. Confirmed in code, end to end:

1. `SweepScheduler` stamps `missed_intervals` on a late sweep; the
   orchestrator stores it **portfolio-wide** — one late sweep marks all
   180 books (`[one-counter]`, orchestration/engine.py:811).
2. `condition_status` (valuation/freshness.py:144–146): missed **1** →
   RP status WARNING · missed **≥2** → **DEGRADED**.
3. market_state/engine.py: WARNING → capped at **ACTIVE** (STABLE
   unreachable) · DEGRADED → **DEFENSIVE**.
4. Promotion needs the clean condition to hold for a DWELL — misses
   arrive every 2–7 ticks, so the climb keeps resetting.

With 11.5% of ticks late (1,335 at ≥2), the panel's flapping is the
ack-burst problem wearing its user-visible face. The machine is honest
— "my prices may be stale" — but the staleness is self-inflicted, so
today DEFENSIVE is noise, and on a game day it would mask a real
degradation. **George's ruling: fix this and redeploy** — the step-4
converger design (drafts/always-quoting-step4-design.md) + the
live-books-first priority George added in review.

---

## Addendum 5 (21:2xZ) — the evening: converger built+deployed, the DUAL-ENGINE incident, the 1.0 s ruling, the engine lock

The full story is in [[market-maker/decisions]] (08-13 evening entry);
the receipts:

- **The converger built** (MM PR #30, 721→724 tests): stage/converge
  with atomic books — the budget-splits-a-book defect was caught by
  test (positional ClOrdID minting collides on a re-diff; see
  `[atomic-book]`). Deployed first as supervised23/CFG-0022.
- **The dual-engine discovery:** the "fresh" supervised22 dir held a
  parallel session's 979 MB journal — two makers had run side by side
  17:53–20:27Z. That session then built the UNION
  (`deploy/g2-union-converger` — their state publishers + this
  converger) and ran it as supervised24. George's panel symptom ("no
  state snapshots on /mm") was the publisher dying in the crossfire.
- **George's evening rulings:** `sweep_max_interval_s` → **1.0 s**
  (restore absolute slack; ratio-tightening was capping every book at
  ACTIVE) · **the single-engine lock** ("make sure there are not 2
  market makers") · a full ghost-process sweep.
- **State at 21:20Z: supervised25 / CFG-0023** — union + tolerance +
  lock; fresh journal; 1,598 instructions / 180 books; **435 ticks,
  ZERO missed sweeps**; second-start REFUSED (lock proven live); taker
  resumed and filling; exactly one engine + one taker on the machine;
  watch on `supervised25.log`.
- ⚠ Standing facts for tonight: the taker restarted at 18:01Z (the
  parallel session) — the boot-LIVE redelivery wrinkle is armed if it
  restarts again near kickoff; `PUB_SHED` climbing is the publisher's
  shed counter (their metric to judge); the A2 drill's starvation
  check still fails at 10× compression (engine-time floor, queued).
- **Process lesson filed:** one session drives the VM at a time; the
  lock now enforces the machine half mechanically.

---

## Addendum 6 (23:4xZ) — FIRST LIVE GAMES: the path worked, then the spiral returned at live load, throttled mid-game

**The milestone first:** at 23:03Z the FULL chain ran on a real game for
the first time — SR → publisher → bus → engine reprice → venue → taker
fills on the game books (BENG/LION within seconds). Readings ramped to
~340/min across three live games.

**The publisher nearly missed the games** (filed for post-mortem with
the session that owns it): the production worker sat SILENT from its
00:00Z discovery until 22:26Z — the pre-kickoff scheduler never fired.
Two restarts failed ("user disabled instance" — new revisions lost the
manual instance count); the fix was one update carrying BOTH
`--instances=1` and an env bump (gen 7, 22:38Z). Polls then ran
perfectly (15 s, zero errors). ⚠ Unexplained: why the original
instance went quiet after midnight.

**The spiral returned at live load (23:05–23:40Z):** live redraw +
overnight churn pushed ticks past the 4 s beat window (asyncio cannot
preempt a synchronous tick); the dead-man fired **47 times**
(fire_count 89→136), each sweep cancelling the gateway's whole tracked
set; the venue rejected cancels for long-dead ids (**20k+
"DRAINED cancel-reject … untracked"**); the reject flood filled the
venue drain cap (512/tick pinned), which lengthened ticks further. The
"stable saturation" I rode from 23:06 was substantially this loop
wearing a calm face — the alarms (DRAIN_CAPPED every tick,
MISSED_SWEEPS 5–10) were real and I under-read them for ~30 min.

**The intervention (23:39–23:41Z, ~2 min dark):** halt taker → stop →
explicit cancel_all → **supervised27-era lever: `g2-throttle` branch,
`converge_max_instructions_per_tick` 256→**128** → **supervised26 /
CFG-0024** → resume. After: drains 39–161 (under cap), sent ~22–75,
beats **445 ms**, dead-man silent (the +7 fires were the cutover window
itself), 1,808 orders standing, taker filling live books again.

**What tonight proves for the build queue:** the 4 s dead-man window ×
synchronous ticks is the real fragility (N15's window/beat coupling +
step 4 phase B + the per-event engine cost measurement are all the same
fix); the gateway's cancel_all re-cancelling its full lifetime tracker
set turns every fire into a reject storm (a gateway-side item for
Hasan); and the throttle lever works as designed — stale-bounded, never
absent, live books first.

---

## SESSION CLOSED (08-15)

George ended the watch after the live slate; the session closes with
the machine running WITHOUT it: **supervised26 / CFG-0024** (throttled
converger build), taker active, the engine lock held — nothing on the
VM depends on this session. The 08-14 follow-ups this session queued
(the per-ack cost measurement, the dead-man window retune) were picked
up by parallel sessions — see the build pages (CB1: 9.893 ms/ack; the
window is 10 s since 00:19Z 08-14) and the 08-14 decisions.

**Open at close, owned elsewhere:** George's review/merge of MM PRs
#25/#26/#27/#30 (the VM runs ahead of the merges) · the publisher
post-mortem (silent 00:00→22:26Z) · the per-ack engine-cost work (the
Saturday gap) · the daily-reference-feed analysis (its own session,
brief in drafts/) · the Go-port question (language table given to
George 08-13; measurement-gated). The reference-price validator
(180/180 to the cent, addendum above) is ~50 lines against
`/quotes` + the inputs file — recreate from the description if wanted
in `scripts/`.
