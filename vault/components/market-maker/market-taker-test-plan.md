---
description: "The taker's testing protocol — taker-isolated cases first, the maker's own plan second, then the joint phases, with SR game simulation as a named phase"
---

# Market Taker (SNT-1) — Test Protocol

> **Component:** [[market-maker/market-maker]] · **Requirements:**
> [[market-maker/market-taker-requirements]] · **The maker's plan:**
> [[market-maker/test-plan]] (its own protocol — deliberately separate).
> **Born:** 2026-08-11 (George: isolate the taker's testing first, the
> maker runs its own protocol, then bring them together; include SR
> game simulations for a live-game rehearsal — "not now, but in the
> protocol").

Status legend (same as the MM plan): ✅ passed · 🔄 ready to run ·
🔧 needs a build first · ⛔ blocked on someone else · ⏳ scheduled.

**The shape (George, 11-08):** three phases, strictly in order per
capability — a joint failure must never be the first time either bot
meets a case.

---

## Phase 1 · Taker ISOLATED

### TT1 — The suite — ✅ standing

670 tests on `main@5681767` (agent draws, gates, journal replay,
reconcile, schedule derivation), ruff + mypy-strict. Runs on every PR.

### TT2 — QA venue, own account, bounded runs — ✅ PASSED 10-08

Run 1 caught a true positive (T-S05 halt on the subject-ClOrdID bug);
run 2 clean: **67 sends, 67 fills, 0 rejects** across five books, both
sides, Edwin's size distribution. Evidence: requirements addendum
`2026-08-10c`.

### TT3 — Unattended soak (the deployed unit) — 🔄 RUNNING since 11-08

`snt-1.service` on the MM VM, `AUTO` state. Pass criteria: days of
clean journal; restarts resume position/budget/sequence; no reconcile
alarms; quiet books stay quiet (no orders while books are empty).
Watch: `journalctl -u snt-1` + `/var/lib/mm/snt3/journal.jsonl`.

### TT4 — Kill-switch and restart drills — ✅ DRILLED 11-08 (extend)

Halt → cancels → resume, journaled, on the live unit. Still owed as
drills: halt SURVIVES a restart (re-arm refused); a mid-window kill
(systemd stop with an order inside the 1.5 s cancel window) — confirm
the dead-man or the resting DAY order's fate matches the runbook.

### TT5 — Schedule-state proof on a REAL game — ⏳ 13-08 (the dry run)

The first live T-F07 proof: the game's two books go PRE_KICKOFF →
LIVE → POST unaided; derived marks land in the journal; arrival
intensity follows (×6 → ×75 → ×4); every other book stays OVERNIGHT.
Needs the MM engine up so the books exist to trade.

### TT6 — SR game SIMULATION drives the taker — 🔧 (George's ask, 11-08)

Simulate a live game on demand rather than wait for the calendar.
Two rungs, both reusing existing tools:

1. **Rig replay (no SR at all):** the A2 harness
   (`scripts/a2_replay_drill.py`, MM PR #13) replays the 1,089-reading
   Chiefs–Ravens capture over rig JetStream at recorded pace ÷ speed.
   Point a taker instance at the rig bus: states must walk
   OVERNIGHT → PRE_KICKOFF → LIVE → POST from the replayed readings.
   Build: a taker-side drill script (small); the harness exists.
2. **True SR simulation (the venue-facing rehearsal):** Sportradar's
   simulation library replays real recordings through the REAL API, so
   the publisher itself polls a "live" game and the production chain
   runs end to end. Needs the `.TEST` symbols provisioned (T10 — ten
   tickers chosen precisely for 17 playable replay games,
   [[market-maker/test-symbols]]) so the game maps to tradeable books.
   ⛔ on tZERO's `.TEST` provisioning; the replay side is proven
   (17/17 live-tested 08-08).

### TT7 — Failure drills — 🔧 partially proven

| Drill | Status | Note |
|---|---|---|
| Feed silence during LIVE → decay to OVERNIGHT | 🔧 | tested in unit; drill it on the rig replay (stop the feed mid-game) |
| Reconcile divergence → bot-wide halt | ✅ | happened live 10-08, true positive |
| Reject storm → book quiets | ✅ | built + seen (5-streak → 60 s) |
| NATS outage mid-session | 🔧 | expected: no orders (no books), clean resume |
| Journal-disk full / unwritable | 🔧 | expected: loud death, no silent trading |
| Venue band (LmtPerc) reject at the touch | 🔧 | T-O09's edge — untested |

### TT8 — Shorts (T-O10) on a zero-float book — 🔧 built 11-08, unrun

`SNT_SHORTS=1` on a book whose float is genuinely zero ON THE ACCOUNT
(the standard 5,000 float keeps the holding away from zero, so side 5
never fires there). **JETS is the natural candidate** once Rob resets
its band — the account holds zero JETS. Pass: the walk crosses zero
both ways with no order straddling; side 5 accepted by the venue on
this account (T16's entitlement question, answered behaviourally);
side 2 and side 5 never rest together; the venue's short reserve
(1,000 QA) never rejects inside our cap; T-S05 reconciles a NEGATIVE
venue position. Off by default everywhere else.

### TT9 — The LIVE rate at one print a second — ✅ PASSED LIVE 15-08 (the cap arm still unrun)

George's 15-08 ruling (20 s / 1 s / 20 s PRE/LIVE/POST). Before the
cutover, a rig run against the maker with two books pinned LIVE for
≥ 30 min. Pass: realised gap per book 1.0 s ± 5% (journal send stamps);
wash-guard skips ≤ ~15% of arrivals and no `Wash trades` rejects;
T-S05 silent (floats hold under the higher fill rate); the maker's
tick line shows no new `MISSED_SWEEPS`/`DRAIN_CAPPED` growth from the
extra acks; loss meter ≈ $5k/h/book at the QA spread; drift stays
inside the 1,500 cap most of the run (the cap WILL bind more often —
record how often, for the E41 round). Then a second run with
`SNT_MAX_ORDERS_PER_S=4` on five LIVE books: total sends ≈ 4/s, every
book still prints, `RATE CAP` lines on the log, no burst after a
30 s halt/resume. Statuses land in the requirements addendum.

✅ **The rig run was overtaken by production** — George deployed #40 at
17:00–17:04Z 15-08 and the first 76 min (SNT-CFG-0023/snt20, six books
LIVE on three preseason games) served as the verification, read-only:
**send gap 1.13–1.16 s** per LIVE book (target 1.0 s; ~11% of arrivals
skipped by the wash guard) · fill-gap p90 = mean × ln 10, so the gaps
stay **exponential — T-F01 intact** · **OVERNIGHT 394 s vs 400 s** ·
**zero rejects on 25,983 sends**, zero halts, zero reconcile alarms,
**zero resting orders (T-O03)** · buy fraction **49.6%**, clip **44 sh**
· **P(same side) 0.542** (the review's HIGH-2 band was 0.75–0.80) ·
cost **$2,507–2,601/hr per LIVE book** · **maker: zero `MISSED_SWEEPS`
in 9,505 ticks**. Full numbers in the build-deploy-log row and
[[market-maker/sessions/2026-08-15-taker-rate-verification]].
⚠ **Still owed:** the `SNT_MAX_ORDERS_PER_S` arm (never exercised —
the cap ships OFF, N44), and the inventory-headroom watch the run
opened (IPTCBEAR, float 1,056 vs the 1,500 cap — see the deploy log).

## Phase 2 · Maker ISOLATED — its own protocol

Lives in [[market-maker/test-plan]] (A/B/C cases + the 10-08c testing
audit's ranked additions). Not duplicated here. Gate to Phase 3: the
maker's A-cases green on the current binary (`main@5681767` — the next
run, `supervised10`/CFG-0009, picks up PRs #11+#13).

## Phase 3 · JOINT — maker and taker together

Strictly after both isolated phases are green for the capability under
test.

### TJ1 — Joint rig run — 🔧 (the 10-08c audit's next untested avenue)

Maker quoting + taker taking on the same rig loopback book. Pass:
the taker's prints stay inside the maker's spread; no reject churn;
both journals reconcile; the maker's skew responds to taker flow.

### TJ2 — Joint QA venue run — 🔄 after TJ1

Both bots, real venue, five QA books, poker OFF (the taker replaces
it as the noise source). Watch the dead-man coupling: the taker rides
the MM namespace, so an engine death sweeps taker orders too —
expected, fails safe (11-08 chat; cancels only).

### TJ3 — The `.TEST` dress rehearsal — ⛔ tZERO provisioning

The full stack on the ten `.TEST` symbols with an SR replay game
(TT6 rung 2 + the maker + the gamecast): the closest thing to a
season game that can run on demand, repeatably.

### TJ4 — Scale — 🔧

The 170-book shape (the audit's scale run) with the taker on its full
universe. Sizing questions (arrival rates × 170) get real here.

---

## Standing rules

- A finding in ANY phase files into
  [[market-maker/market-taker-requirements]] (addendum) or the MM's
  plan — this page carries statuses, the session notes carry the
  narrative.
- Isolation is per CAPABILITY, not per calendar: a new taker feature
  re-enters Phase 1 even after joint runs exist.
- Nothing in this protocol touches production books or real users;
  production entry stays gated on the compliance read (T-C01) and the
  IPLP classification (T-I02), independent of test results.
