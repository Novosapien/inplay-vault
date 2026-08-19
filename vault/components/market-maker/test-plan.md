---
description: "The MM's live test matrix — game-lifecycle, venue-ops and failure-drill cases with a status, method and pass criteria per case"
---

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

> **The taker tests separately:** [[market-taker-test-plan]] (11-08,
> George's protocol — taker isolated, maker isolated (this page), then
> the joint phases TJ1–TJ4 recorded there).

---

## A · Game-lifecycle tests

### A1 — Normal operation (static supervised quoting) — ✅ PASSED 07/08-08

Six QA books two-sided at Edwin's prices on the real venue, poker-driven
drift, dead-man cleanup, restarts under config versions.
Findings fixed along the way: the move-size carry (PR #8), the
double-post race (PR #9), poker aiming (v7). Ladder monotone 69.7%
(84% is the target ceiling; the gap is the E17 remnant).
Evidence: decisions `2026-08-07d–f`, `2026-08-07h`, `2026-08-08`.

### A2 — In-game repricing — ⭐ STAGE 2 PASSED 08-12 00:52 (the synthetic game day, production bus + real venue, corr 0.989/−0.990, to-the-cent) · stage 1 passed 08-10c/11

**The big one.** Readings from a real game drive the valuation while
the engine quotes the venue books.

- **Method, stage 1 (rig):** `scripts/a2_replay_drill.py` (built 08-10c,
  on MM PR #13) — replays all 1,089 captured readings over the rig
  JetStream at recorded-pace ÷ `A2_SPEED`, re-offering the newest
  reading every 2 s through gaps (the live publisher's contract), while
  the full engine quotes the loopback gateway. Twelve checks judged at
  close. **120× smoke: 12/12 PASS** — every reading accepted ·
  never-empty on every ~1 s sample · zero doubled levels · zero
  rejects · wire-path beliefs ≡ file-path beliefs · two-sided uncrossed
  close · no sweep starvation · deterministic core replays
  byte-identically · settled venue book replays identically by value.
- **The 10× recorded run (completed 08-11 00:4x): 12/12 PASS** —
  1,782 never-empty samples over ~30 min, zero doubles, zero rejects,
  no sweep starvation; monotonicity closed at 100% (CHIE) / 62% (RAVE).
- **Findings (08-10c):** (1) the E17 remnant reproduces with NO fills —
  ladder monotonicity 50–100% purely from rest-until-gone generation
  mixing; (2) through-venue BYTE replay equality is not an invariant:
  `stand_the_book` is un-journalled and admitted orders carry the
  gateway's price string ("77.6" ≠ "77.60" canonically) — both named in
  the drill, closable if wanted; (3) the rig gateway remembers ClOrdIDs
  for its process life — the drill mints a fresh config version per run.
- **Method, stage 2 (live venue):** the same replay onto production
  NATS with the engine on the QA books. **The publisher is DEPLOYED
  (08-11, prod + testing pools, production probabilities access, both
  verified)** — see [[market-maker/build/infrastructure]]. What remains
  for stage 2: the MM-side go-live ingestion switch (the engine
  consumes the bus instead of its in-engine poller) on a QA run.
- **Pass criteria:** prices track the win-probability moves that
  Edwin's model implies, to the cent · width and cadence follow the
  LIVE tier · never-empty holds through the largest swing · no reject
  storm on fast repricing · zero doubled levels · the journal replays
  to identical state.
- **Watch tools:** `journal_open.py` (journal vs book), the
  monotonicity sampler, the poke hit-rate script — all on the VM.

✎ **STAGE 2 RESULT (08-12 00:17–00:52Z, the synthetic game day):**
all 1,089 Chiefs–Ravens readings replayed onto the PRODUCTION
`SR_PROBABILITIES` stream at 10× under a fresh game id
(`sr:sport_event:99990812`), maker `supervised15`/CFG-0014 on 180 real
venue books, taker at ×75 (551 CHIE/RAVE fills). **corr(p_home, CHIE
mid) = +0.989 / RAVE −0.990 over ~860 paired points; net moves match
Δp × $5/win to the cent** (+$2.18 vs +$2.17 implied). Re-offers deduped
as confirmations; no LmtPerc storm (the 348 in-game rejects are 95% the
KNOWN sell-gate gap, now measured under game load). Driver:
`~/synthetic_game_day.py` on the MM VM (fresh game id + stream purge +
Z-stamps are its contract — two silent-poison lessons, see the 08-11
full-book session note addenda 5–6). ⚠ Found on the way: the reading
poison counter surfaces nowhere — silent-poison build item.

### A3 — Pre-game → kickoff transition — ✅ PASSED 08-11/12 (rode the synthetic game day)

The market-state machine's tier flip: pre-kickoff cadence/width →
LIVE dwell (3–12 s seeded range) at kickoff.

- **Method:** start the A2 replay before the recorded kickoff.
- **Pass criteria:** books stand from static valuations before any
  reading arrives (cold start) · at kickoff the dwell/width tier
  changes visibly · no gap in the book at the transition.
- ✎ **08-11/12 result:** books stood from the supervised inputs all
  evening pre-game; the taker derived PRE_KICKOFF on the first
  not_started reading and LIVE at the kickoff second (23:32:30 run 1;
  00:17:38 run 3); no book gap at either transition.

### A4 — Post-game → overnight — ✅ state transition PASSED 08-12 · ⚠ the Edwin design gap stands

The final-whistle transition: post tier, then overnight tier.

- **Method:** run the A2 replay through the recorded final whistle.
- **Pass criteria:** the book widens/slows per the post and overnight
  tiers · quoting behavior at final is WHATEVER EDWIN RULES — pin the
  question first: keep quoting the settled-outcome price, or suspend?
  Settlement itself is Ch 11, unbuilt — this test covers the state
  transition only. → Edwin round.
- ✎ **08-12 result:** on the ended reading the taker flipped LIVE →
  POST (00:47:16) and the maker minted the OFFICIAL_RESULT exactly once
  (idempotent across 5 final re-offers), outcome home 27–20. What the
  maker QUOTES after a final remains the Edwin question.

### A5 — Halftime / quarter breaks — ✅ PASSED 08-12 (inside the synthetic game day)

Dwell-tier changes mid-game. Verified inside the A2 run; no separate
setup.

---

## B · Venue-ops tests

### B1 — The 23:59 ET session boundary — ✂ 08-12: THE PREMISE IS TRUE AFTER ALL — the roll WIPES the book, silently

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
- ✎ **08-12 OVERTURNED:** with ~750 orders resting across 180 books,
  the 00:01 ET boundary WIPED them all — no DONE_FOR_DAY, no message at
  all; every later cancel/replace drew `UNKNOWN ORDER`. The 08-09 run
  saw nothing because six mostly-idle books had little to lose. Fallout
  measured: an 8-hour phantom-cancel storm (~61k cancel-rejects/hour —
  the backoff's 60 s cap retries ~750 phantoms forever) + ~56 dead-man
  sweep/repost loops + MD subscriptions dead on some symbols (CHIE 8 h).
  Full record: [[market-maker/sessions/2026-08-12-session-roll-storm]].
  Fixes filed: engine-side UNKNOWN-ORDER retire (R-D05), a boundary
  strategy (self-sweep vs nightly restart), an MD boundary heal.
- ✎ **08-12 evening: the fixes are BUILT and DEPLOYED (MM PR #24,
  `supervised17`)** — gone-retire + the session clock (close 23:59 ET /
  open 00:02 ET, journalled) + fork-based checkpoints. **Tonight's
  boundary is the live re-run of this test**; pass = SESSION close/open
  in the log, no storm, books re-stand by ~00:03 ET. The MD boundary
  heal (gateway-side) is still owed — stale panel quotes may recur
  even if the engine passes.

### B2 — Venue halt / resume — ⛔ needs Hasan (or luck)

Security-status halts (market.status), SSR flags, circuit breakers.

- **Method:** ask Hasan to fire a halt on one QA ticker, or wait for a
  natural one.
- **Pass criteria:** the engine suspends the halted book (§6.4),
  sweeps it, leaves the other five alone (quarantine boundary), and
  recovers on resume.

### B3 — Scale beyond 7 books — ⭐ RUN 08-11: 169/170 STOOD, the empty-book gate is GONE

✎ 08-11 late, the full-book run (`supervised13`/CFG-0012, George's
ruled task 1): after seeding all 180 symbols (100k each, ledger) and
probing all 180 books clear, the engine stood **1,532 instructions
across 170 securities in one boot** — **169 of 170 books two-sided**.
⭐ **Every virgin book ACCEPTED its first ladder**: the 07-08
`LmtPerc: No price available` empty-book total-reject did NOT fire
(the venue behaviour has changed — parameters `LmtPerc reference` ✎).
The one failure is JETS (stale ~$18.65 reference, T20 — 46 rejects,
0 accepts, backoff keeping it quiet). ~9,400 wire messages in the
first ~4 min ≈ 38 msg/s, far inside the 5,000 msg/s governor; no
journal backpressure at this cadence (the N31 ceiling is a live-game
question, not a standing one). The taker joined on the same 170 books
(SNT-CFG-0008) and its first fills passed T-S05. ✎ Same night: the `.TEST` refusal was built away (MM PR #22 — twin
minting at composition) and `supervised14`/CFG-0013 stood **179 of
180 including all ten `.TEST` twins** (1,636 instructions); the first
`.TEST` print exists (`IPTCPACK.TEST` 6@71.66, house-to-house). ✎ Then
JETS was walked up (four cross-account prints, T20 closed ourselves) —
⭐ **ALL 180 OF 180 BOOKS STAND TWO-SIDED** (JETS 7 asks + 6 bids
accepted at close). B3's scale question is answered at full universe.

Historical framing (pre-08-11): 164 books were empty and
`LmtPerc: No price available` rejected the first order. Separately,
full-ladder message rates exceed the 100/s default `maxOrdRate`
(✂ superseded 05-08 — the governor is 5,000/s, burst 2,000).

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

### C4 — Reject-backoff under fire — ✅ PASSED LIVE 08-11 (supervised11)

**The live half landed unplanned:** JETS's standing LmtPerc blocker
(the stale 18.65 ask) made every JETS bid reject on supervised11 — and
each rejecting price retried only **3–4× in 80 s**, the backoff
schedule, not the old ~16 msg/s sweep-cadence churn. The other five
books ran clean. Pass criteria met on the real venue.

Three live shapes recorded: LmtPerc "aggressive", duplicate-ClOrdID,
no-reference — plus the 08-10 UNKNOWN ORDER cancel-loops (8 ids ×
18–124 rejects in 8 min on the diverged supervised5 boot). ⚠ Counting
note for any measurement: replace confirms and most cancel-rejects
arrive **2×** (the gateway's `[replace-pair]` delivery) — halve them.

- **Built:** `mm/venue/backoff.py` + reconciler suppression — submit
  rejects back off per (security, side, price); cancel/replace rejects
  per order; delay 2 s ×2 up to 60 s (🟡 in parameters); success is
  the only reset; state rides the checkpoint (schema 4); replay-safe
  by construction. 618 tests green.
- **Method (the live half):** re-create a persistent-reject book (a
  stale-referenced price does it) and measure the message rate.
- **Pass criteria:** the ~16 msg/s churn is gone; a rejecting level
  retries on the backoff schedule, not at sweep cadence; a halted
  divergence loop (the 08-10 shape) stays at the 60 s cap.

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
