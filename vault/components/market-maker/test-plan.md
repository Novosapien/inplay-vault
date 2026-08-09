# Market Maker — Live Test Plan

> **Component:** [[market-maker/market-maker]]
> **Purpose:** The test cases that take the MM from "quotes standing"
> (proven 07-08) to season-ready. Each case has a status, a method, and
> pass criteria. Update the status here after every run; the session
> note carries the narrative.
> **Born:** 2026-08-08 (George: "we need different test cases — normal,
> in-game, pre and post game").
> **Securities:** [[market-maker/test-symbols]] — the ten permanent `.TEST`
> symbols (tZERO, 08-08) and the 17 Sportradar replay games that drive
> them. A2 below takes its game feed from that page.

Status legend: ✅ passed · 🔄 ready to run · 🔧 needs a build first ·
⛔ blocked on someone else.

---

## A · Game-lifecycle tests

### A1 — Normal operation (static supervised quoting) — ✅ PASSED 07/08-08

Six QA books two-sided at Edwin's prices on the real venue, poker-driven
drift, dead-man cleanup, restarts under config versions.
Findings fixed along the way: the move-size carry (PR #8), the
double-post race (PR #9), poker aiming (v7). Ladder monotone 69.7%
(84% is the target ceiling; the gap is the E17 remnant).
Evidence: decisions `2026-08-07d–f`, `2026-08-07h`, `2026-08-08`.

### A2 — In-game repricing — 🔄 ready (rig) / ⛔ live bus (publisher undeployed)

**The big one.** Readings from a real game drive the valuation while
the engine quotes the venue books.

- **Method, stage 1 (rig):** replay the captured real game through the
  docker rig bus at real-time pace, then at 10×. The engine runs with
  supervised identity but readings-driven valuation. No live-venue risk.
- **Method, stage 2 (live venue):** the same replay onto production
  NATS with the engine on the QA books. Needs the sportradar-service
  MM probability publisher deployed — `feat/mm-probability-publisher`
  is still a local branch (flagged since 06-08).
- **Pass criteria:** prices track the win-probability moves that
  Edwin's model implies, to the cent · width and cadence follow the
  LIVE tier · never-empty holds through the largest swing · no reject
  storm on fast repricing · zero doubled levels · the journal replays
  to identical state.
- **Watch tools:** `journal_open.py` (journal vs book), the
  monotonicity sampler, the poke hit-rate script — all on the VM.

### A3 — Pre-game → kickoff transition — 🔄 ready (rides A2)

The market-state machine's tier flip: pre-kickoff cadence/width →
LIVE dwell (3–12 s seeded range) at kickoff.

- **Method:** start the A2 replay before the recorded kickoff.
- **Pass criteria:** books stand from static valuations before any
  reading arrives (cold start) · at kickoff the dwell/width tier
  changes visibly · no gap in the book at the transition.

### A4 — Post-game → overnight — 🔄 ready (rides A2) · ⚠ design gap first

The final-whistle transition: post tier, then overnight tier.

- **Method:** run the A2 replay through the recorded final whistle.
- **Pass criteria:** the book widens/slows per the post and overnight
  tiers · quoting behavior at final is WHATEVER EDWIN RULES — pin the
  question first: keep quoting the settled-outcome price, or suspend?
  Settlement itself is Ch 11, unbuilt — this test covers the state
  transition only. → Edwin round.

### A5 — Halftime / quarter breaks — 🔄 ready (rides A2)

Dwell-tier changes mid-game. Verified inside the A2 run; no separate
setup.

---

## B · Venue-ops tests

### B1 — The 23:59 ET session boundary — ⚠ RUN 08-09: THE PREMISE IS FALSE

The premise was that tZERO ends its session at 23:59 ET and every
resting DAY order expires as DONE_FOR_DAY (adopted 22-07 from the
platform doc).

- **What happened:** the engine ran unattended from 08-08 through
  08-09, across TWO 23:59 ET boundaries. **No `39=3` DONE_FOR_DAY
  exists anywhere in the gateway's FIX log**, the engine journalled
  none, and orders placed 08-08 00:31 are STILL RESTING.
- **Verdict:** the venue fact is wrong, or the QA venue does not run a
  session roll. The MM's DONE_FOR_DAY handling is harmless but dead
  code. → **T14** (ask tZERO: is there a session roll, does DAY expire,
  and does the QA environment differ from production?).
- **Still open from the original test:** what the engine does at a real
  roll, if one ever occurs — untestable until T14 answers.

### B2 — Venue halt / resume — ⛔ needs Hasan (or luck)

Security-status halts (market.status), SSR flags, circuit breakers.

- **Method:** ask Hasan to fire a halt on one QA ticker, or wait for a
  natural one.
- **Pass criteria:** the engine suspends the halted book (§6.4),
  sweeps it, leaves the other five alone (quarantine boundary), and
  recovers on resume.

### B3 — Scale beyond 7 books — ⛔ LmtPerc answer · 🔧 N31 first

164 books are empty and `LmtPerc: No price available` rejects the
first order (blocking, with Hasan). Separately, full-ladder message
rates exceed the 100/s default `maxOrdRate`.

- **Method:** once LmtPerc is answered, stand 20 → 50 → 170 books
  stepwise; measure fsync (N31 group commit — ~579 events/s measured,
  under the ~2t requirement) and gateway order rates (UEAR raise).
- **Pass criteria:** all books stand within the message budget · no
  journal backpressure · reject-backoff (see C4) keeps any rejecting
  book quiet.

---

## C · Failure drills on the real venue

### C1 — Restart on the OLD journal (the boot-reconcile gap) — 🔧 healer unbuilt

Every restart so far sidesteps the gap (fresh journal + CFG bump)
because dead-man sweeps while the engine is down never journal — an
old journal replays phantom ACTIVE orders and the reconciler stands no
book.

- **Method:** deliberate restart on the old journal against the swept
  venue; observe the phantom set; then build the §3.1.4 healer (ICD
  snapshot / order-status reconcile at boot) and re-run.
- **Pass criteria (post-healer):** boot detects swept orders, corrects
  the record, reposts the book, and the journal stays replay-true.

### C2 — Checkpoint resume on a live day's journal — 🔄 ready

The §10.3 equality proof ran on the captured game. Re-run it on a real
venue day's journal (supervised5 or later).

- **Method:** copy the day's journal + checkpoints off the VM; replay
  checkpoint-resume vs full-replay locally; compare state hashes.
- **Pass criteria:** byte-identical state, including the venue record
  with `pending_price` (schema 3).

### C3 — Readings-feed loss mid-game — 🔄 ready (rides A2, rig stage)

Kill the replay feed mid-game; restore it after the freshness window.

- **Pass criteria:** the stale book suspends and sweeps (§6.4) · the
  other books keep quoting (per-security quarantine) · recovery
  republishes within one cycle of fresh readings · wire faults stay
  fatal (poison vs fatal boundary holds).

### C4 — Reject-backoff under fire — 🔧 build first (TOP of [[market-maker/build/next|next]])

Three live shapes recorded: LmtPerc "aggressive", duplicate-ClOrdID,
no-reference. 751 CANCEL_REJECTED in 30 min of poker churn is the same
family.

- **Method:** after the build, re-create a persistent-reject book (a
  stale-referenced price does it) and measure the message rate.
- **Pass criteria:** deterministic, replay-safe backoff — the
  ~16 msg/s churn is gone; a rejecting level retries on the backoff
  schedule, not at sweep cadence.

### C5 — Malformed inbound (poison) — ✅ passed live 07-08, 🔄 fuzz later

The no-id fill killed the engine once (fixed, PR #6: subject fallback
+ poison drain). A deliberate fuzz pass over the drain (truncated
payloads, wrong types, unknown subjects) is cheap insurance before
season.

---

## D · Blocked externally (not ours to schedule)

- **User-side wash verification** (blocking ON) — Hasan's pilot
  accounts.
- **The 163 empty books** — the LmtPerc reference answer (gates B3).
- **IPO → secondary day-one book** — E27's opening-position publisher,
  then Ch 9.
- **MD-view trust** — the market.book staleness evidence is with the
  Hasan message; until gated/alerted, judge the engine from the
  journal, not the panel.

---

## Suggested order

1. **B1 tonight** (zero effort — the engine is already running).
2. **A2 stage 1 on the rig** (biggest coverage, no live risk), with
   A3/A4/A5/C3 riding the same replay.
3. **C2** on the supervised5 journal.
4. **C4** after the reject-backoff build; then **A2 stage 2** on the
   live bus once the publisher deploys.
5. **C1** when the healer is scheduled; **B2/B3/D** as the external
   answers land.
