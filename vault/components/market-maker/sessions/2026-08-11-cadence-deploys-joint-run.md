---
description: "The deploy day: cadence rulings built+shipped, publisher+engine+taker live on production infra, books cleared, joint maker-taker run validated share-for-share"
---

# 2026-08-11 — the deploy day: cadence ruled, everything shipped, the first joint run

> **Type:** rulings + build + deploy + live ops. George + Claude.
> **Continues:** [[market-maker/sessions/2026-08-10-c-churn-forensics-reject-backoff|the 10c note]]
> (its Late additions 3–5 carry the same day's detail; this note is the
> day's own record and index).
> **Repo state at close:** MM main `b86ca83`+ (PRs #13, #11+residual,
> #16, #17, #18, #20 merged; #19 merged then REVERTED deliberately);
> sportradar-service main carries the publisher + worker pools (PRs
> #8–#15). All vault edits uncommitted on `docs/t0-plain-english-guide`.

## The rulings (George), all built and deployed same day

1. ⭐ **Live poll 500 ms** — an unchanged successful fetch is
   CONFIRMATION, not no-data (decisions 2026-08-11).
2. ⭐ **New orders every 500 ms in-game, changed or not** — chosen
   explicitly over the reaction-bound reading; tick/sweep 0.5 s, LIVE
   dwell 0 (decisions 2026-08-11; MM PR #16).
3. ⭐ **The dwell table is the republish clock in EVERY mode** —
   pre/post 5–20 s, overnight 20–40 s; closes the silent gap where
   Edwin's 23-07 "non-live 30–60 s" was never implemented (decisions
   2026-08-11b; MM PR #18).
4. ✅ **Edwin's ladder profile STANDS** (fattest at the touch) — George
   challenged it, reviewed it, kept it: "two-sided liquidity, not
   profit-seeking". The inversion was built+merged+reverted same hour
   (decisions 2026-08-11c; PR #19 revert `b86ca83`).
5. ⭐ **The Hasan freeze OVERRIDDEN** for the publisher deploy —
   "treat Hasan as not doing anything; incorporate his changes."

## Deployed to production infrastructure

- **The MM probability publisher** — Cloud Run worker pools
  `inplay-mm-publisher` (+ `-testing`), production probabilities
  access (the code default was still the half-burned trial),
  `MMPUB_POLL_LIVE_S=0.5`, terraform-managed. Hasan had
  PRE-provisioned the whole path (firewall 2024, the `sportradar` and
  `snt-taker` NATS users). Service PRs #8–#15; dev→main carried his
  six fixes.
- **The ingestion switch** (`MM_READINGS=bus`, MM PR #17) — the engine
  consumes the production JetStream; pipe proven end to end with a
  captured reading. NATS `market-maker` user gained the
  SR_PROBABILITIES consumer grants (conf backed up on the NATS VM).
- **The engine** — deployed by git bundle (the VM repo has no GitHub
  remote): supervised10 → 11 → 12 through the day; at close
  `supervised12`/CFG-0011, six books, all of today's merges aboard.
- **The taker** — first run on ITS OWN account `4963224393` with the
  `snt-taker` NATS user, continuous (`SNT_MINUTES=0`), per-book
  venue-verified floats (the T-S05 recovery — see below).

## Tests passed today

- **A2 stage 1**: 12/12 at 120× and 10× (the 1 s world), then
  re-gated **11/11 under the 500 ms cadence** after the drill learned
  to separate the E38 end-of-feed suspension and the benign ~1.2/s
  cancel-vs-ack race from defects. Drill: `scripts/a2_replay_drill.py`.
- **C4 live**: JETS's LmtPerc rejects retried 3–4× in 80 s on the real
  venue — the backoff schedule, not the old 16 msg/s churn.
- **The joint maker+taker run** (first ever, separate accounts): LIVE
  burst 20 fills/90 s; lifetime 198 sends → 198 fills, zero rejects;
  49.5% buys; clip mean 48 (Edwin's ~44); crossing cost ≤4¢;
  ⭐ **journals mirror share-for-share on all ten (book, side) totals.**

## Venue facts learned (gospel)

- ⭐ **The stale test quotes are a VENUE-SIDE RESEEDER** — 49 levels
  re-posted TODAY 10:16Z, originator tag 275=`STX`, same price zones
  eaten on 08-07e. Eaten again (all filled, zero rejects); recurs
  until Rob disables it.
- ⭐ **The venue position feed is LIVE** — it moved by exactly each
  fill during the reconcile chase (weighs on T15's doubt).
- ⭐ **House↔house prints EXECUTE across the two accounts** — 100% of
  taker flow met the maker, measured (T13's cross-account half, QA
  evidence; E33's optics now have numbers).
- **The depth feed can serve empty while the venue is full** (the
  08-10 flaw recurring); `POST /md/probe` is truth,
  `POST /md/book-resubscribe` is the heal, `GET /quotes` the cache.

## Incidents and their permanent records

The taker incident chain (boots-halted semantics · T-S05 firing on all
five books after a bad plain-kill stop · same-version RNG redraws ·
the `SNT_MINUTES=15` relic · kill-pattern and cwd footguns) → six
operating rules in the MM repo **CLAUDE.md** (PR #20) and the 10c
note's Late addition 5. T-S05's recovery lever proven:
`SNT_FLOAT_OVERRIDES` = venue − journalled drift per book.

## ⚠ Cross-session reconciliation owed (FIRST taker task next session) — ✅ DONE 08-11 late ([[market-maker/sessions/2026-08-11-taker-cutover|the cutover note]]): one owner, `snt-1.service` @ SNT-CFG-0007, floats recomputed at the halt, nohup retired

A parallel session (same day) built taker shorts (T-O10, PR #15),
T-F07 schedule-derived state (PR #14), and deployed the taker as
**`snt-1.service`** (systemd, enabled) — the process this session
TERM-killed at 13:48 while clearing the books, which is where the
T-S05 divergences began. Two operating setups now exist for one
account; the unit is enabled-but-inactive with STALE floats. Fold
tonight's venue-verified floats + `SNT_MINUTES=0` into the unit's env,
fresh journal + CFG bump, retire the nohup. A reboot meanwhile fails
safe (T-S05 halts the stale-float boot at its first fill). Full
detail: [[market-maker/market-taker-requirements]] addendum 2026-08-11d.

## Next (George's ruled order — the handover in-chat carries the detail)

1. **Full-book test**: position-transfer seeding of ALL tickers incl.
   the ten `.TEST` → run the MM on the full book (B3 load + the
   LmtPerc empty-book experiment + the N31 fsync measurement).
2. **Synthetic game day** over the production bus (A2-stage-2
   mechanics + A3/A4/A5 + taker ×75).
3. **C2** on supervised12's real journal.
4. Externals: T17 · Rob (STX seeder, JETS reference, T14/T15/T16) ·
   Hasan (B2) · the Edwin round.
