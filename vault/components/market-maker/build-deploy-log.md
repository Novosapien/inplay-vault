---
description: "The cross-session working log: every in-flight change, where it is (built / merged / deployed / verified), and who or what it waits on"
---

# Market Maker & Taker — Build/Deploy Log

> **Component:** [[market-maker/market-maker]] · **Born:** 2026-08-13
> (George: one log of what is being done, where it is, and its
> implementation and deployment state).

## How to use this file — read before editing

1. **This is the WORKING LOG, not the narrative.** Session notes carry
   the why; this file carries the CURRENT STATE of every change moving
   through the pipeline: `building → PR open → merged → deployed →
   verified live`. If you build, merge, or deploy anything, update its
   row in the SAME session — a stale row here misleads every parallel
   session.
2. **One row per change.** Name the repo and PR. State the CODE state
   and the DEPLOY state separately — merged ≠ running (the recurring
   binary/repo-divergence lesson). Name what the change waits on.
3. **Deployed rows carry the running coordinates** (config version /
   journal / commit) so the next session can verify instead of trust.
4. **Move finished rows to "Landed" — never delete them.** The log is
   also the record of what shipped when.
5. **Check this file before deploying anything** — another session may
   hold an in-flight change on the same component. The taker's env on
   the VM outruns the vault regularly; the row states the last KNOWN
   coordinates and when they were read.

## In flight

| Change | Repo / PR | Code state | Deploy state | Waits on |
|---|---|---|---|---|
| **Gateway forwards tag 9383 on exec events** (`posSize` — activates the taker's exec-borne T-S05) | `inplay-fix-gateway-go` **#3** | ✅ merged (`main` incl. the X-Ops-Key hardening) | 🔴 NOT deployed — running binary is 10-08's (`005fdd8`-era) | **Fold into the next natural gateway/engine restart** (ordered sequence: taker down → engine down → gateway → engine → taker). No dedicated ceremony — George, 13-08. Until then the taker reconciles on the `position.>` fallback (fails safe) |
| **Step 4 phase B — the converger on its own task** (`converge_interval_s` 0.25 s · `CONVERGE_STALE` 2 s · dead task = loud stop) | `inplay-market-maker` `feat/always-quoting-step4b` @`912ba27` (cut from the VM's running `g2-throttle`; pushed) | ✅ built — 874 tests, ruff clean, mypy delta zero | 🔴 **NOT deployed — George's explicit instruction** ("implement, do not deploy") | The bundled deploy (below); honest scope: does NOT fix the ~35% missed sweeps (per-event engine cost — measure first) |
| **Taker boot rebase** (T-S05 addendum: FIRST exec-borne figure per book after boot may be adopted, journalled `rebase`, loud; mid-session [no-adopt] holds; `SNT_BOOT_REBASE=off` reverts) | same branch @`db45300` | ✅ built — 881 tests, ruff clean, mypy delta zero | 🔴 NOT deployed | The bundled deploy; **inert until gateway #3's binary runs** (the window is tag-9383-borne only) |
| **THE BUNDLED DEPLOY (awaiting George's approval):** gateway #3 binary + MM converger task + taker boot rebase, one ordered ceremony | gateway `main` binary · MM/taker `feat/always-quoting-step4b` | all ✅ built | 🔴 waiting | George's go + a window (post-games, pre-03:59Z roll, or tomorrow daylight). Sequence: taker halt→stop → engine stop → gateway binary swap+restart → engine start (CFG-0026, fresh journal) → taker full runbook (new binary, CFG bump, fresh journal, floats from the RUNNING env) → resume |
| ~~**Taker T-S05 reconcile halt — IPTCCLEM**~~ ✅ **RESOLVED 00:54Z** (George's ruling: trust the venue) | — (operational) | — | `SNT_FLOAT_OVERRIDES` CLEM 3812→3794 (`env.bak-clem` kept), taker restarted (booted halted, mark held) + resumed; filling, no re-halt | — (the permanent fix is the boot-rebase row above) |
| **No price updates for IPTCBENG (Bengals) + IPTCLION (Lions)** — reported by George in the 14-08 live test: the app shows no quote movement for these two while other symbols move | — (operational, not code) | — | ⚠ untriaged | **MM-session triage** (app session was told NOT to touch the VM). App side is RULED OUT: the app-session audit (14-08) verified the full chain — app slug `cin`/`det` → ticker `IPTCBENG`/`IPTCLION` → trading-service asset seed rows → MM `universe.py` rows → `bindings.json` (sr:competitor:4416 / 4419) all present and consistent, and the app's 60 s cold refresh re-reads the WHOLE `/trading/quotes` board, so a static price on screen means the `venue_quotes` DB row itself is not changing. **George's read (14-08): the LIVE WIN PROBABILITIES for these two are the suspect** — check the win-prob path for their games specifically (publisher polling → `SR_PROBABILITIES` stream → engine binding sr:competitor:4416 / 4419 → freshness marks) |
| **MISSED-SWEEPS FIX, step 1 — the engine-cost measurement** (~half a day): an instrumented run breaking tick time down per stage (readings drain · venue drain · 180 cycles · converge · encode) and per event, on the rig via the A2 replay at 10× — no live game needed. Output: ms-per-ack, ms-per-cycle, the real binding stage. Also sizes the drain-cap re-size owed since group commit (venue cap must RISE toward ~1,050 acks/tick) | `inplay-market-maker` — instrumentation branch off the deploy lineage | 🔴 not built | — | A quiet slot; nothing external. **Prerequisite for steps 2–3 — measure before optimizing** |
| **MISSED-SWEEPS FIX, step 2 — the design fixes** (1–2 sessions, language-agnostic — a Go engine would want both): (a) **de-phase the dwell waves** — jitter republish schedules so acks stop arriving in 100–200-event clumps; (b) **the incremental sweep** — a book whose inputs are unchanged since the last sweep provably yields the identical output (pure functions), so skip recomputing it; §3.1.4 semantics preserved, replay equality re-proven by the A2 drill. (b) is the big win and touches the machine's heart — reviewed, not rushed | `inplay-market-maker` | 🔴 not built | — | Step 1's numbers (they say whether (a), (b) or both pay) |
| **MISSED-SWEEPS FIX, step 3 — Python speed work** (1–2 sessions, dies with any Go port): hot-path optimization ONLY where step 1's profile says it pays (ack fold, Decimal churn); optionally a faster VM core (single-thread bound). Target: NFL-scale miss rate ~0% | `inplay-market-maker` / VM sizing | 🔴 not built | — | Step 1's profile. ⚠ Honest ceiling: NCAA Saturday (~2,500 events/s) likely exceeds Python regardless — that is **the Go decision** (weeks-scale rewrite + re-proving replay equality; parked 04-08, tonight's evidence reopens it as a season-2/NCAA call) |
| **Taker shorts** (side 5, T-O10, off by default) | `inplay-market-maker` **#15** | ✅ merged | ✅ in the running binary; feature **OFF** (`SNT_SHORTS` unset) | QA test (TT8) needs a zero-float book — JETS after Rob resets its band; E26 (depth rules), T16 (entitlement) |
| **Maker shorts** (N34 — ask ladder side-flip at minting) | `inplay-market-maker` | 🔴 not built | — | The MM session (handed over 11-08, vault decisions 2026-08-11d) |
| **Vault docs branch** | `inplay-vault` `docs/t0-plain-english-guide` | ⚠ 5 sessions of working docs UNCOMMITTED | — | George's go to commit + push |
| **Protocol drills TT4 (kill mid-window) · TT6 (rig replay of a full game)** | — | 🔴 not run | — | A quiet slot; no externals |

## Landed (most recent first)

| Change | Repo / PR | Live since | Coordinates / proof |
|---|---|---|---|
| **Dead-man window 4 s → 10 s** — ends the game-night fire loop (~130 sweeps at silence 4.0–4.7 s) | env row on the gateway VM · default bump in `inplay-fix-gateway-go` **#4** (OPEN, Hasan) | 14-08 00:19Z | `MM_DEADMAN_TIMEOUT_MS=10000` in `/opt/fix-gateway/.env`; binary UNCHANGED (#3 still undeployed). Ordered sequence honoured; engine now **supervised27/CFG-0025** (fresh journal, 1,618 instr); zero fires since, beat silence ~1 s peak. Decisions 2026-08-14 |
| **Publisher universe-filter hotfix** — `sr:competitor:` ids pass discovery; the publisher adopts and polls games for the first time ever | `inplay-sportradar-service` — hotfix branch (prod) + `testing` cherry-pick + **PR #37 → main (OPEN — merge or the next main deploy regresses it)** | 13-08 ~22:38Z (prod) · ~22:44Z (testing) | Prod pool: `hotfix/mm-publisher-universe-filter` @`d877b26` (cut from running SHA `f8c8aef`), run 31750593932. Testing pool: `testing@daf5604`, run 31751010981. Both verified polling `71548090/92/94` at 15 s; testing also covers the 08-14 late slate. Session 2026-08-13-e |
| **Wash guard** — never send against an own resting IOC remnant | MM **#29** | 13-08 18:01Z | Taker `SNT-CFG-0017`, journal `snt14`, `main@772e79c`. 46 fills/2 min post-cutover, zero alarms. Venue wash flag stays ON (ruling 13-08) |
| **T-F07 fetch-age freshness** — staleness prices `Fetched-At`, not delivery | MM **#28** | 13-08 13:15Z | In the running binary since CFG-0014. Kills restart-re-derives-LIVE (3 occurrences 11/12-08) |
| **Exec-borne T-S05 (taker half)** — prefers the exec's own 9383 | MM **#28** | 13-08 13:15Z | In the binary; **primary path INERT until gateway #3 deploys** — fallback = today's proven behaviour |
| Taker unattended deploy + AUTO states + NATS grants + Secret Manager | MM #12/#14 | 11-08 | `snt-1.service` on the MM VM; `snt-taker` NATS user; stream `SR_PROBABILITIES` |
| mm-publisher worker (the taker's schedule feed) | sportradar-service #8/#10 | 11-08 | Cloud Run pool `inplay-mm-publisher`, 1 instance; the publisher owns the stream config |
| Reject backoff + cancel-reject drain (engine) | MM #11/#13 | in `main` 11-08 | Engine picks them up per its own runs (operating session's coordinates) |

## Standing facts a deployer must know

- Every taker deploy: **halt → stop → new binary → CFG bump + fresh
  journal + floats recomputed from the RUNNING env + journal drift →
  start.** Floats are positions, not constants.
- Gateway restarts follow the ordered sequence, always.
- Merged ≠ deployed, on every repo — check the running coordinates.
- The operating session cuts the taker's env frequently (CFG-0013 →
  0016 in one afternoon, 13-08); read `/etc/snt-1/env`, never assume.
