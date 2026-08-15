---
description: "The taker LIVE rate: the 5.3 s was the design number, George rules one print a second, the arrival-clock bias fixed, portfolio cap built OFF (MM #40)"
---

# 2026-08-15 — the taker's LIVE rate: one print a second (MM PR #40)

> **Who:** George + Claude (a fresh session, briefed on maker + taker first)
> **Type:** feedback → feasibility → ruling → build
> **Refs:** MM PR #40 `feat/snt-live-rate` (off `main@2c74886`) ·
> decisions 2026-08-15e · parameters (SNT-1 rows) · open-questions E41,
> **N44 (new)** · taker requirements addendum 2026-08-15 · taker test
> plan TT9 · build-deploy-log row · systems/snt-1-noise-taker ·
> learnings 2026-08-15c

## What we did

1. **Familiarised with the maker + taker** per the working guide (hub,
   decisions, open-questions, parameters, requirements, plan, latest
   notes, build-deploy-log, the taker's own docs and `src/snt/`).
   Two background readers distilled decisions.md and open-questions +
   parameters; both confirmed the taker picture.
2. **Traced the feedback.** Edwin (via George): the taker "does not seem
   to be running quick enough during live games — it crosses every
   ~5.3 s". That is `base_orders_per_hour` 9 × LIVE ×75 = 675/h = 5.33 s:
   **Edwin's own v1.0 numbers, not a fault** (his 30-07 smoke test said
   "~1 order every 5 seconds per book"). E41 already named
   `base_orders_per_hour` as his lever to tune on real books.
3. **Feasibility + implications, given to George** (the assessment is
   in the chat and summarised in decisions 2026-08-15e): cheap to change
   (one config row + a loop fix); money never binds (spread mostly
   house→house); inventory drift grows √N so the 1,500 cap binds more;
   wash-guard skips ~10% at 1/s; the maker's LIVE 500 ms re-roll stays
   ahead of the taker so no L1 erosion; **maker load — every taker fill
   is one exec ack (~10 ms under live load, CB1)** — NFL night +5%,
   Sunday slate +20%, NCAA Saturday >50%; message budget irrelevant
   (5,000/s governor).
4. **George's ruling: one print per book every 20 s PRE_KICKOFF · 1 s
   LIVE · 20 s POST; OVERNIGHT untouched.** Multipliers 20/400/20 (were
   6/75/4). Book-visible → filed 🟡 GEORGE; Edwin confirms in the E41
   round.
5. **Built MM PR #40** in a fresh worktree off `main`:
   - `snt/config.py`: the ruled multipliers (`[rate-ruling]`); the rates
     env-tunable as INTERVALS `SNT_INTERVAL_{OVERNIGHT,PRE_KICKOFF,LIVE,
     POST}_S` (`[rate-env]`); `tick_s` 0.25 (`SNT_TICK_S`, `[tick]`);
     `max_orders_per_s` 0 = off (`SNT_MAX_ORDERS_PER_S`, `[portfolio-cap]`).
   - `snt/agent.py`: **`schedule_after_arrival`** — the served arrival
     reschedules from its own instant, clamped to one tick of backlog
     (`[arrival-clock]`); `schedule` (from now) stays for state changes
     and resume.
   - `snt/runtime.py`: the loop routes served arrivals through the new
     clock; tick from config; the portfolio cap (token bucket, drop +
     reschedule, rotating scan start, `RATE CAP` log, `capped=` on the
     done line).
   - Docs: BUILD-LOG session entry, `deploy/snt-1.env.example` rows,
     runbook section, schedule.py comments refreshed.
   - **896 tests (885 + 11), ruff + mypy-strict clean.** Nothing merged,
     nothing deployed (the 14-08 freeze).
6. Vault: decisions 2026-08-15e · parameters (three new SNT rows + the
   ruled multipliers) · E41 addendum + **N44** (the cap is George's
   call) · taker requirements addendum (T-F04 ✎, T-F01 hardened) ·
   TT9 in the taker test plan · build-deploy-log row · the SNT-1
   system doc's rate line · learnings 2026-08-15c.

## What we learned

- ⭐ **The arrival clock was biased long, and the bias grows with the
  rate.** The loop serves one arrival per book per tick and rescheduled
  from the TICK's time, so every gap carried ~half a tick. Measured on
  the agent (200,000 s, seeded, 0.5 s tick): 5.575 s realised for
  Edwin's 5.333 s (+4.5%, invisible), **1.268 s for a 1 s target
  (+27%)**, and the shape drifts toward "one every tick" as λ·Δt → 1
  (T-F01's "no learnable schedule" would have quietly eroded). Fixed:
  1.057 s at 0.5 s, **1.012 s at the 0.25 s tick now shipped**.
- The taker's tick body costs **0.039 ms at 180 books** — halving the
  tick is free even on the maker-saturated VM.
- The 5.3 s figure being the design number, not a bug — check the
  configured value before treating a complaint as a defect.
- **A per-book rate is a portfolio load**: 1 s per book × the books
  live at once, each print an ack the maker drains. State the portfolio
  number beside every per-book ruling (learnings 2026-08-15c).
- **Cap by thinning, not queueing** — a deferring cap turns Poisson into
  a metronome; drop-and-reschedule keeps it Poisson.
- Repo mechanics: the shared `.venv` imports the MAIN checkout's `src`;
  a worktree must run with `PYTHONPATH=src` or its tests silently test
  the wrong tree (the first run "passed" 211/211 against old code).

## What went wrong / got stuck

- First test run passed against the wrong source tree (above) — caught
  by the ratio test that should have failed. `PYTHONPATH=src` from then
  on.
- Two statistical tests needed tolerance widening (10,000 draws → ~1%
  sampling error) and one exact-float assertion loosened; no logic
  changes.

## Decisions made *(mirrored into [[market-maker/decisions]] 2026-08-15e)*

- ✅ George: LIVE one print a second per book; PRE_KICKOFF 20 s; POST
  20 s; OVERNIGHT untouched. Book-visible, Edwin confirms (E41).
- ✅ Rates env-tunable as intervals; the taker tick 0.25 s (🟡 ours).
- ✅ The portfolio cap exists and ships OFF — capping the ruled rate is
  George's call (N44).

## Questions opened / closed *(mirrored into [[market-maker/open-questions]])*

- Opened **N44**: should the taker's TOTAL arrival rate be capped, and
  at what — the Sunday-slate / NCAA-Saturday maker-load arithmetic;
  options (a) OFF until CB4, (b) ~10/s, (c) slate-aware LIVE interval
  (not built). Needs an answer before the first NFL Sunday at 1 s and
  before NCAA 29-08.
- E41 addendum: LIVE/PRE/POST ruled by George; Edwin to confirm the
  four intervals with the E31 batch; OVERNIGHT (which also covers
  weekday daytime) and the `team_weight` feed remain his.

## Next

1. **Review + George's merge go on MM #40**, then the taker cutover on
   the freeze lift in a quiet slot: halt → stop → `SNT-CFG-0021` +
   fresh journal → floats from the RUNNING env + snt17 drift → start
   (the running taker still fires every 5.3 s in LIVE until then).
2. **TT9 rig run first** (two books pinned LIVE ≥ 30 min: realised gap,
   wash-guard skip fraction, T-S05 silent, maker tick unhurt; then the
   cap at 4/s on five books).
3. George rules **N44** before the first Sunday slate at 1 s.
4. Edwin round: the four intervals + the ungridded sizes + E31.
5. Vault branch `docs/t0-plain-english-guide` — still uncommitted across
   sessions; George's go to commit + push.
