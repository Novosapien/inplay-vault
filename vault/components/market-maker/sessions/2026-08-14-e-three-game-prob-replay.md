---
description: "Three-game paced probability replay launched on the MM VM (six books live), the PATR/COLT staleness-suspension incident, and the re-offer fix"
---

# 2026-08-14 — three-game probability replay: launch, incident, re-offer fix

> **Who:** Claude (ops session) + George (rulings, live observation)
> **Type:** operational — the 2026-08-14 paced-replay decision, extended to
> three games / six books
> **Refs:** decisions 2026-08-14e · [[market-maker/build-deploy-log]] (the
> replay row) · `inplay-sportradar-service/scripts/mm_prob_replay.py`

## What we did

- **George asked for 6–10 teams quoting as if live.** Found three recorded
  games and launched three `mm_prob_replay.py` processes on the MM VM
  (`~/prob-replay/`, own venv, service `src/app` copy, fixtures cached):
  - PIT@CIN 2024-12-01 (`sr:sport_event:50128577`, 44–38) → BENG/STEE
  - IND@NE 2024-12-01 (`sr:sport_event:50128583`, 25–24) → PATR/COLT
  - GB@DET 2024-12-06 (`sr:sport_event:50128599`, 34–31) → LION/PACK
- **Team selection rule:** every NFL team plays in the 13–16 Aug preseason
  window, so the rule used was: teams whose real game is ALREADY PLAYED
  (the 13-08 slate) with no game before 17-08. Zero collision with the
  live publisher. Bonus: four of the six are the N40 seed-stuck books.
- **George required a cancel mechanism → built and drilled live:**
  `stop-replays.sh` (SIGTERM, pidfiles, pkill sweep) + `start-replays.sh`
  (idempotent). One restart cycle ran cleanly during the incident fix.
- **Verified end to end** at 18:23Z: readings in the supervised28 journal,
  all six books repricing.

## What we learned

- ⭐ **The re-offer IS the liveness signal — re-learned on a new path.**
  The recorded timeline only holds entries where the probability MOVED
  (median gap 4 s, p90 28 s, 15.6% > 20 s). The replay published entries
  at original pacing and nothing in between, so quiet stretches aged the
  observation through 5/10/20 s → RP Invalid → SUSPENDED. George saw it on
  the panel within the hour (PATR/COLT). Any feed that skips the re-offer
  suspends its books — same lesson as E38/06-08b, third appearance.
- **The VM has no outbound internet** — pip hangs silently. Dependencies
  travel as manylinux wheels over IAP scp (`~/replay-wheels/`), matching
  the git-bundle deploy convention.
- **The engine under three-game live load:** `MISSED_SWEEPS` 2–5/tick,
  occasional `DRAIN_CAPPED=venue`, `CONVERGE_BACKLOG` to ~36 — and the
  portfolio-wide counter caps every book at DEFENSIVE. The standing
  missed-sweeps fault, now reproducible on demand without a real slate —
  useful for the fix-set's CB1 measurement stream.
- The `mm.state` snapshot's book map key is `securities` (not `books`);
  probing it with the admin token from the VM works and answers "what
  does the engine believe" in one line.

## What went wrong / got stuck

- **The PATR/COLT staleness suspensions** (above) — fixed same hour:
  `--reoffer 2.0` republishes the last reading with fresh stamps every
  2 s during timeline gaps AND the inter-pass gap (a silent 30 s gap
  would otherwise suspend all six books once per pass). Verified: all six
  books back to `defensive` and holding.
- The first venv install failed silently (`pip | tail` swallowed the
  network hang); caught by the import proof failing, not by the install.
- Six OTHER books (49ER/CARD/CHAR/RAID/TEXS/TITA — last night's real
  games) sit SUSPENDED regardless of the replay: the N40 game-end class,
  observed while probing, untouched.

## Decisions made *(mirrored into [[market-maker/decisions]] 2026-08-14e)*

- Three games / six books, the selection rule, the cancel lever, the
  re-offer fix, the stop-before-real-games deadline.

## Questions opened / closed

- None opened. N40's evidence grew (the six real-game books suspended with
  the testing pool re-offering them — the re-open gap is engine-side, as
  filed).

## Next

- ✅ **STOPPED ~19:4xZ on George's instruction** — clean `replay_stopped`
  in all three logs, zero processes confirmed, well clear of the 23:00Z
  real slate. Honesty note: the processes were already down when the
  cancel ran (stopped minutes earlier by another hand — George via the
  `!` command, or a parallel session). The six books staleness-suspend
  ~20 s after the stop; expected and safe. Restart if ever wanted:
  `~/prob-replay/start-replays.sh`.
- The patched `mm_prob_replay.py` is UNTRACKED (`local/replay-sandbox` in
  the service repo + the VM copy) — open a PR if the script is to be kept.
- The replay's reproducible live load is ready-made input for the
  missed-sweeps measurement (fix-set CB1) — worth a deliberate run.
