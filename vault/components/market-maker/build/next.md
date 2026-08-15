---
description: "Build state at a glance — what is real, mocked or gated, and the sequenced queue of what the MM builds next"
---

# Build — What Is Real, and What Comes Next

> Part of [[market-maker/build/index|As Built]] · Sequencing:
> [[market-maker/plan]] · Blockers and owners:
> [[market-maker/open-questions]] · **In-flight pipeline state:
> [[market-maker/build-deploy-log]]** (check it before deploying
> anything). Rewritten 2026-08-14 to the post-first-live-games state.

## Real · mocked · gated

| Real and proven | Mocked / interim | Gated / unbuilt |
|---|---|---|
| Event core, journal, replay equality on a real game · §10.3 checkpoints equality-proven · **N31 group commit** (one fsync/tick, 08-13) | Off-field RAV/EAV (§3.6) — static inputs | Live mode (T1 · N19 · the go-live switch; S1 landed) |
| Valuation with Edwin's on-field leg · E38 observation-age freshness | `p_tie = 0` (S6 interim) | §5.5 public-book checks · §5.9 replenishment (E17) |
| Position/skew (Ch 4) · quoting chain (Ch 5) · market state (Ch 6) | Pre-kickoff tier 15 s (George's 10–30 range) | Ch 9 IPO · Ch 11 settlement · §10 recovery |
| Venue sync + reconciler + reject backoff + gone-retire, live-proven | E31 width values (mechanisms built, numbers Edwin's) | Opening-position publisher (E27) · the boot-reconcile healer (parked) |
| **The full bus path IN PRODUCTION** — publisher pools → JetStream → engine (`MM_READINGS=bus` since 08-11); universe filter fixed 13-08 | The always-quoting numbers — drain caps 256/512, converger 256→128 / 0.25 s, stall 5 s — 🟡 OURS, re-size after the measurement | **Always-quoting step 5** — the dead-man breaker |
| **Always-quoting steps 1–4 DEPLOYED** (bounded drains · group commit · progress-aware beat · converger phases A+B, 08-13/14) | Dead-man window 10 s — env row; the binary default rides gateway PR #4 (N15 retune stands) | Maker shorts (N34) · taker shorts ON (E26 depth rules · T16 · the JETS zero-float test) |
| The session clock (close 23:59 / open 00:02 ET), live-fired 08-13 | | The MM panel kill-switch surface (N29; access control first) |
| Per-security quarantine · **the single-engine lock**, proven live | | The daily reference feed pipeline (designed 13-08 — George's approval + the N23 blessing) |
| State publishers (`mm.state`/`snt.state`) + the taker's manual order ticket (four review rounds, 12-08) | | |
| **SNT-1 deployed and running** — AUTO states (T-F07 fetch-aged), wash guard, exec-borne T-S05 + boot rebase, floats venue-true | | |
| **The first live games ran the full chain 13-08** (SR → publisher → bus → engine → venue → taker fills) | | |

## What we build next

Each item names the build page it will change. **What we TEST next
lives in [[market-maker/test-plan]]**; in-flight rows and their exact
states live in [[market-maker/build-deploy-log]].

**Ours, unblocked — in rough order:**

1. **The missed-sweeps fix chain** (~35% of ticks miss a sweep slot
   under three live games — engine time per event):
   step 1 the instrumented per-stage/per-event cost measurement (A2
   replay at 10×, no live game needed; also sizes the drain-cap
   re-size owed since group commit) → step 2 the design fixes
   (de-phase the dwell waves; the incremental sweep — pure functions,
   skip an unchanged book) → step 3 Python hot-path work where the
   profile says it pays. ⚠ Honest ceiling: NCAA Saturday
   (~2,500 events/s) likely exceeds Python regardless — the Go
   decision reopens as a season-2/NCAA call. Changes
   [[market-maker/build/runtime|Runtime]] and
   [[market-maker/build/event-core|Event core]].
2. **The p_ref cutover rebase** (the 14-08 BENG/LION finding): a
   fresh-journal boot mid-game freezes `p_ref` at the CURRENT
   probability and erases the accumulated live move. George rules:
   carry kickoff freezes across cutovers (seed from the prior
   journal/checkpoint), and/or the operating rule — no maker cutovers
   while games are live. Changes
   [[market-maker/build/valuation|Valuation]].
3. **N40 — the game-end lifecycle**: the publisher retires an ended
   game ~1 h after the final, its confirmations stop, and a book still
   in the live-freshness regime suspends PERMANENTLY (no re-open
   path); two books escaped and quote pre-final prices. ➕ The
   service half is BUILT (PR #38 — never retire, overnight cadence
   forever; undeployed). Still needed: the engine-side post-final
   regime hand-off, plus the N39 fix (the mappings bridge + a loud
   `adopted=0`). Changes [[market-maker/build/ingestion|Ingestion]]
   and [[market-maker/build/market-state|Market state]].
4. **Always-quoting step 5 — the dead-man breaker** (defence in
   depth). Changes [[market-maker/build/runtime|Runtime]].
5. **Keep-one-alive under the reject backoff** (proven cascade: a
   reject storm suppresses every price on a side and the book closes
   one-sided): never suppress the best remaining postable level per
   side. Changes [[market-maker/build/venue|Venue]].
6. **The stale-book crossing guard (R-Q09)** — the engine's reposts
   take stale third-party liquidity ($50,366 measured once) — and
   **the sell gate (R-Q08)** — nothing subtracts live resting sells
   before an ask ladder (`sellable = Pos − livS`). Changes
   [[market-maker/build/venue|Venue]].
7. **Maker shorts (N34)** — the ask ladder's side-2→5 flip at MINTING
   (a resting order cannot change side on replace); the taker's half
   is merged and OFF. Changes [[market-maker/build/venue|Venue]] and
   [[market-maker/build/quoting|Quoting]].
8. **The review debt** — the VM deliberately runs ahead of review:
   MM PRs #21 · #22 · #24 · #25 · #26 · #27 · #30 OPEN while
   production runs their lineage (the wash-guard/boot-rebase branch
   split is CLOSED — `step4b-wash` @ `5b10d68` merges main into
   step4b and runs as the taker since SNT-CFG-0019). Service
   PR #37 (universe filter) OPEN — **the next service main deploy
   regresses the running hotfix until it merges**, and #37 is a FULL
   testing→main promotion (65 commits), not the one-hunk hotfix
   (which has no PR — see [[market-maker/build/ingestion|Ingestion]]).
   Gateway PR #4 (dead-man default) OPEN.
9. **Terminal-record pruning** — engine state grows ~70–90 MB/h at
   the 500 ms/180-book cadence. Changes
   [[market-maker/build/runtime|Runtime]].
10. **Protocol drills** TT4 (kill mid-window) · TT6 (rig replay of a
    full game); the A2 starvation check still fails at 10×
    compression (the engine-time floor — re-judge after the
    missed-sweeps chain).
11. **The daily reference feed build** — designed 13-08
    ([[market-maker/systems/daily-reference-feed]]); build gated on
    George's approval + the N23 event-type blessing. Changes
    [[market-maker/build/ingestion|Ingestion]].
12. Housekeeping owed: a systemd unit for the supervised engine
    (doubles as the N15 beat-jitter recorder) · the CI/CD audit
    (George, 06-08) · the boot-reconcile healer (parked with eyes
    open).

**Gated on others:**

- **Live mode itself** — T1 (the MM account) · N19 (Edwin's file
  transport; who does 06:00 until the upload page exists). S1's
  production allocation LANDED (the publisher polls
  `/production/v1`). Changes
  [[market-maker/build/infrastructure|Infrastructure]].
- **Off-field §3.6** — the RAV/EAV methodology (Edwin's world; E47
  may fill it if he confirms the Gamecast off-field method). Changes
  [[market-maker/build/valuation|Valuation]].
- **E31 values** — per-state width floors, the σ² bounds, the
  cold-start sign-off; the slots exist. Changes
  [[market-maker/build/quoting|Quoting]] and
  [[market-maker/build/market-state|Market state]].
- **§5.5 / §5.9** — the participant book feed and the E17 lifecycle
  ruling. Changes [[market-maker/build/quoting|Quoting]].
- **Ch 9 IPO allocation** (needs E27's publisher — the day-one book)
  and **Ch 11 settlement**. New pages when built.
- **Taker production posture** — E32 numbers · E33/T13 compliance ·
  the IPLP account class (T-I02) · shorts depth rules (E26/T16).
- **The Edwin round** — E29–E38, E47, N23/N28 blessings; several
  answers land directly in existing code slots.

**Direction, parked:** the Go port — everything stays Python through
season 1; differential replay (the same journal through both
implementations, byte-compared) is the port's certification tool. The
four port hazards are recorded in decisions 04-08; the 08-13 live
nights reopened the question for NCAA scale, decision parked at
season-2/NCAA.

**The landed history** (what shipped when, with coordinates) lives in
[[market-maker/build-deploy-log]]'s Landed table and the dated entries
in [[market-maker/decisions]] — this page stopped duplicating it on
14-08.
