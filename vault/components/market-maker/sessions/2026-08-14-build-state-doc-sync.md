---
description: "Full build-state sync: every build/ page, the hub and infrastructure reconciled against the repos and the live VM, mid-flight with the CFG-0026 bundled deploy"
---

# 2026-08-14 — the build-state doc sync

> **Type:** documentation session (George: "update the build state so it
> is completely up to date"). Docs only — no VM writes, no code changes.
> Ran CONCURRENTLY with the engine session's bundled deploy and the
> gateway-watch session's forensics; coordinated by message with both.

## What we did

1. **Read the mandatory order** (hub → decisions → open-questions →
   parameters → requirements → plan → latest session notes), then
   reconciled every `build/` page against the repos and the live VM.
2. **Verified the ground truth directly**, not from the docs:
   - MM repo: `origin/main` @ `772e79c`; PRs #23/#28/#29 MERGED;
     PRs #21/#22/#24–#27/#30 still OPEN while production runs their
     lineage (`feat/always-quoting-step4b` @ `db45300`, 881 tests).
   - Gateway repo: `main` @ `124991e` (= PR #3, tag-9383); PR #4
     (dead-man default 10 s) OPEN — code default still 4000, the VM
     env carries 10000.
   - Service repo: `main` @ `f8c8aef` — PR #37 (universe filter) OPEN,
     so the next main deploy regresses the running hotfix.
   - Dictionary on the production branch: tick 0.5 · sweep 0.5/1.0 ·
     drains 256/512 · **converger default 128** (baked in from
     `g2-throttle` — not 256-with-override) · 0.25 s task · stall 5 s.
   - Live VM (read-only): caught the **CFG-0026 bundled deploy
     mid-ceremony** (taker SIGTERM 11:47:04Z, gateway restart
     11:48:54Z, empty `supervised28`/`snt15` dirs staged).
3. **Coordinated with the two live sessions:** the engine session
   confirmed the deploy LANDED 11:51Z and sent final coordinates
   (gateway `main@124991e` · engine supervised28/CFG-0026 @`db45300`,
   1,664 instr/180 books · taker SNT-CFG-0018/snt15 — superseded
   ~12:10Z by SNT-CFG-0019/snt16, see What we learned); it owns
   build-deploy-log/decisions/parameters and today's deploy session
   notes. The gateway-watch session filed
   **N40** (game-end lifecycle suspension) + its forensics note; its
   build-page references were folded in here.
4. **Updated the build state:**
   - `build/index.md` — 14-08 header; 0.5 s loop + converger + lock in
     the one-paragraph model; the main-vs-production-lineage divergence
     and open-PR debt; module map gains orchestration, lock, session
     clock, converger, state publishers, `.TEST` twins, `src/snt/`;
     key-numbers line re-cut to the current dictionary.
   - `build/next.md` — REWRITTEN to the post-first-live-games state:
     new real/mocked/gated table; the queue is now missed-sweeps chain
     → p_ref cutover rebase → N40 → step 5 → keep-one-alive →
     R-Q09/R-Q08 → N34 → review debt → pruning → drills → reference
     feed; landed history delegated to the build-deploy-log.
   - `build/runtime.md` — tick 0.5 s; sweep 0.5/1.0 s; new converger
     (phases A+B, deployed) and single-engine-lock sections; dead-man
     10 s; next-list refreshed.
   - `build/venue.md` — dead-man 10 s + the fire-loop's
     cancel-all-recancels-lifetime-set gateway item; the 13-08
     wash-flag ruling; `mm.state` deploy gate → deployed; next-list
     gains R-Q09/R-Q08/N34/keep-one-alive.
   - `build/market-state.md` — the 1.0 s tolerance ruling, the live-load
     ~35% residual, and N40's no-re-open-path edge.
   - `build/valuation.md` — the mid-game `p_ref` rebase edge (the
     BENG/LION triage) as a known deviation awaiting George's carry
     ruling.
   - `build/ingestion.md` — the universe-filter incident (never adopted
     a game until 13-08; PR #37/N39), two-publishers-one-bus, the
     Cloud Run `--instances=1` footgun, and N40.
   - `build/infrastructure.md` — status table re-cut to live
     coordinates (engine supervised28/CFG-0026 · taker
     SNT-CFG-0018/snt15 · gateway 10 s + `124991e` · publisher hotfix
     revisions); gateway VM row and engine-home heading corrected.
   - `build/event-core.md`, `build/quoting.md`, `build/position.md` —
     frontmatter added; quoting gains the 08-11c ladder-profile ruling.
   - Hub `market-maker.md` — status line rewritten to 14-08 (production
     running, first live games, fire loop → 10 s window, lock,
     always-quoting 1–4 deployed, standing faults); SNT-1 and Ops-UI
     system rows updated; every build page now carries `description:`
     frontmatter.

## What we learned

- **The VM outruns the vault by hours, reliably.** The build-deploy-log
  row read "waiting on George's go" while the ceremony was literally
  executing. The infrastructure page now says to read the log + the VM,
  and the deploy-state rows live ONLY in the log.
- **The converger budget is 128 by DEFAULT on the production lineage** —
  the vault recorded it as "256, with 128 deployed"; the branch baked
  the throttle in. (Flagged to the engine session for the parameters
  row it owns.)
- Cross-session messaging worked as designed: three sessions split one
  vault cleanly (deploy narrative / forensics / build state) with zero
  file collisions.
- ⚠ **A wash-guard regression alarm was raised here and CORRECTED by
  the engine session.** The explorers showed no branch carried both
  PR #29 and the boot rebase; my VM check read `~/inplay-market-maker`
  @ step4b and concluded the CFG-0018 taker lost the guard — but the
  taker IMPORTS from `~/snt-checkout` via PYTHONPATH (proven by
  `/proc/PID/environ`), which held `main@772e79c`: the guard never
  regressed; the boot rebase was the missing half. Resolution:
  **SNT-CFG-0019 (12:10Z)** runs `step4b-wash` @ `5b10d68` (main
  merged into step4b — both features, first binary with both).
  Runbook lesson recorded on the infrastructure page: the ExecStart
  venv path says nothing about the import tree; check
  `/proc/PID/environ`.
- ⚠ **Service PR #37 is not hotfix-sized**: its head IS the full
  `testing` tip (65 commits, +7544/−371) — merging it promotes ALL of
  testing to main. The genuine one-hunk fix
  (`hotfix/mm-publisher-universe-filter` @ `d877b26`) has NO PR.
  George should choose the merge path deliberately.
- Gateway PR #4 bumps `settings.go` only; a second hardcoded 4 s
  fallback survives at `oe_adapter.go:139` (bites only if the env
  value is ever ≤ 0).
- The repo-side `docs/BUILD-LOG.md` is stale (newest entry =
  always-quoting step 3; status table 06-08-era) — flagged on
  build/index; a code session should back-fill it.
- The two Explore subagents DID report, late; their findings produced
  the four flags above. Everything else they found matched the direct
  verification.

## What went wrong / got stuck

- Nothing blocking. One Edit missed on exact-whitespace match
  (re-anchored via grep); the first VM `ps` probe returned a mangled
  empty result that briefly read as "nothing running" — the systemd
  status check corrected it.

## Decisions made

- None. This session recorded other sessions' decisions; it made none
  of its own.

## Questions opened/closed

- None opened here (N40 was the gateway-watch session's). None closed.

## Next

1. ~~Fix the wash-guard regression~~ — MOOT: the alarm was false
   (see What we learned) and SNT-CFG-0019 (`step4b-wash` @ `5b10d68`,
   12:10Z) carries both features anyway.
2. **Merge the review debt before it bites:** the universe filter
   (choose the path: PR #37 = full testing promotion, or open a PR on
   the one-hunk `hotfix/…@d877b26`), gateway PR #4, MM PRs
   #21/#22/#24–#27/#30.
3. George's two standing rulings: the **p_ref carry across cutovers**
   (or no-cutovers-during-games) and the **missed-sweeps measurement
   slot** (step 1 of the fix chain).
4. **N40** needs an engine-side answer (post-final freshness hand-off /
   a re-open path) — the ten dark books recur every game night until.
5. The vault branch (now 6+ sessions of working docs) is still
   uncommitted — standing call with George.
