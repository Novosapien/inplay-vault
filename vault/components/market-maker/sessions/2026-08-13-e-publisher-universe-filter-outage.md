---
description: "The publisher never adopted a game: the universe filter compared sr:competitor ids to GUID keys. Hotfixed on production + testing 20 min before kickoff"
---

# 2026-08-13-e — the publisher's universe filter never matched, found 40 min before kickoff

> **Type:** live incident + hotfix deploy. George + Claude.
> **Trigger:** George: the admin trading panel still shows OVERNIGHT for
> the preseason games kicking off in ~40 minutes (23:00Z CIN–DET and
> PIT–GB, 23:30Z NE–IND).
> **Repo:** `inplay-sportradar-service` — hotfix branch off the deployed
> production SHA + a cherry-pick onto `testing` + **PR #37** into main.

## What we did

1. Traced the OVERNIGHT symptom down the chain: panel → taker/maker
   activity states → readings on the bus → the mm-publisher. The VM
   watch (`~/gameday13.log`) showed **`seq=2907` frozen and
   `readings/min=0` since at least 11:47Z** — the stream had accepted
   nothing all day.
2. Production `inplay-mm-publisher` logs for 24 h held exactly two
   lines: the 00:00:01Z discovery fetch. Zero timeline polls all day.
   A pool restart (env-nonce revision) re-ran discovery — schedule now
   carried all three games — and STILL produced zero polls. So the
   filter, not the schedule.
3. **Root cause, confirmed in code:** `PublisherWorker`'s universe
   filter tests `team_id in TEAM_SYMBOLS`. The probabilities schedule
   keys competitors on SR-NATIVE ids (`sr:competitor:4416`);
   `TEAM_SYMBOLS` keys on league-feed GUIDs (`ad4ae08f-…`). The test
   can never be true → **every game ever discovered was silently
   dropped**: zero adopted, zero polls, zero readings. The publisher
   has never fed the bus a real game; tonight was the first time it
   mattered ("genuinely untested until tonight" — 08-13-b addendum 2).
4. **The hotfix (one line):** an `sr:competitor:` id passes the filter
   — adopt the fixture and let the MM's own bindings decide what it
   prices. A wasted poll beats a dead feed (the service's own err-busy
   doctrine).
5. **Deployed twice, deliberately differently:**
   - **production:** branch `hotfix/mm-publisher-universe-filter` cut
     from `f8c8aef` — the exact SHA production ran — so the API and
     live worker redeployed byte-identical on game night. Dispatch run
     31750593932, landed ~22:38Z.
   - **testing** (George: the test runs on the testing services): the
     same commit cherry-picked onto the `testing` head Hasan deployed
     at 20:26Z (`daf5604`), push-triggered run 31751010981, landed
     ~22:44Z. NOT the production branch — that would have downgraded
     Hasan's testing API/worker.
6. **Verified live, both pools:** timeline polls for `71548090/92/94`
   every 15 s (PRE_KICKOFF tier) with `mm_publisher_tick` reports;
   testing additionally polls the 08-14 late slate (`71548102/104/106`,
   HOU–LAC and SF–TEN) because it carries the discover-tomorrow fix.
7. **PR #37** folds the fix into main so the next main deploy does not
   regress it. 17/19 pass (17 on the old head, 19 on testing's).

## What we learned

- **The filter bug was invisible for a month because "quiet" is a
  legal state.** "Zero readings today = no universe games" (08-11) was
  read as the correct quiet state; adoption is not logged, and the
  first verifiable receipt was defined as the 22:00Z poll onset — which
  never came. An `adopted=0` on a day with games should be an ALARM.
- **SR posts NO pregame probabilities for these preseason games** —
  timelines were empty at 22:37Z. So OVERNIGHT-until-kickoff is partly
  DESIGNED behaviour (err-quiet without a reading): expect the panel to
  jump OVERNIGHT → LIVE at the first posted probability, with no
  visible PRE_KICKOFF tonight. The maker's activity axis has the same
  dependency ("needs readings to know a game is live" — parameters,
  tier-decision row).
- **Two publishers now feed one bus** (testing shares the
  `inplay-mmpub-nats-url` secret). Duplicates are tolerated by design
  (idempotent readings; re-offers are liveness confirmations), so this
  is redundancy — and the ONLY pre-kickoff ramp for the 00:00Z/01:00Z
  games, which production's older image cannot discover until midnight.
- A second session (rev `00005`, 22:26Z) restarted the pool in
  parallel under the same account — the one-session-drives lesson now
  has a Cloud Run instance.
- Cloud Run "Shutting down user disabled instance" lines belong to the
  PREVIOUS revision's instance; the pool-level `lastModifier` is
  overwritten by every update — audit logs, not pool state, say who
  did what.

## What went wrong / got stuck

- ~25 minutes went to the restart theory (schedule-empty-at-midnight)
  before the zero-polls-after-restart receipt killed it. The filter
  was four greps away the whole time.
- First test run failed spuriously: the shared venv's editable install
  resolved the MAIN repo's newer module, not the hotfix worktree's —
  `PYTHONPATH` to the worktree's `src` fixed it.

## Decisions made

- Hotfix now, both environments, smallest possible diff, cut from the
  running SHAs — George's implicit go under the 20-minute clock; the
  deploy held for his explicit confirm mid-flight.
- The venue-side proper fix (mappings bridge in discovery) is filed as
  **N39**, not slipped into the hotfix.

## Questions opened/closed

- **N39 opened:** wire the GUID ↔ sr-native mappings bridge
  (`services/probabilities_identity.py`) into publisher discovery so
  the universe filter actually filters; make `adopted=0` on a
  game-day schedule loud.

## Next

1. Watch the first posted probability tonight: seq advances on
   `~/gameday13.log`, taker books flip LIVE, maker prices the games.
2. Merge PR #37 (main), then the follow-on N39.
3. The build-deploy-log rows this session added.

---

## Addendum (23:0x–23:2xZ) — the flip PROVEN live, and the "not running" scare was the panel

- **The chain worked at kickoff:** seq 2,907 → 4,380+ with a 358/min
  burst at 23:10Z as SR posted its first probabilities. The books
  skipped PRE_KICKOFF and went straight to LIVE — as predicted (SR had
  no pregame probabilities; err-quiet held until the first reading).
- **George's mid-game "the maker is not running": FALSE, proven three
  ways** — engine ticking (13,386+), 180/180 books cycling with ~13–14
  resting orders each (`resting_order_count`, all `defensive` from the
  known missed-sweep demotion), `mm.state` publishing every ~1 s
  (subscribed with the admin NATS user, frame fresh, CFG-0023), the
  proxy pump POSTing frames into Centrifugo the same second.
- **The two real, panel-side causes:** (1) the snapshot was in SHED
  mode — `shed=["resting_orders"]`, game-load frames outgrew the
  256 KB budget, so ladders arrive as counts; any view keyed on
  ladders shows empty books. The engine's shed frame is
  contract-correct (field omitted, count present). (2) the proxy's
  `/market/quotes` drew 10 s upstream timeouts → 502 at 23:02/23:11/
  23:12 — an empty venue-book view on each failure.
- **Panel changes specced for the panel owner** (not built): a maker
  liveness banner (frame age + tick age) on every trading page; a
  shed headline summing `resting_order_count` — a row must never read
  "not quoting" while a count exists; keep-last-good + a lagging badge
  on `/market/quotes` failures.
- **Engine follow-up filed by observation:** the 256 KB snapshot
  budget binds under game load (shed is the steady state during
  games) — re-size or trim rides the existing always-quoting/step-4
  workstream, post-freeze.
- **15-08 verification:** the fix survived the 14-08 redeploys — the
  testing pool's running commit `d492dcb` descends from the
  cherry-pick. PR #37 remains OPEN and main (at `f8c8aef`) does NOT
  carry the fix: the next main → production publisher deploy regresses
  it until #37 (or its re-apply) merges. Flagged in the
  build-deploy-log Landed row.
