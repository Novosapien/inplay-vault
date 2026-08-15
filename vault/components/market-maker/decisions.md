---
description: "Dated log of confirmed market-maker decisions and standard-doc supersessions — SNT-1 scope, v1 quote lifecycle, venue FIX facts and IPO-sheet economics"
---

# Market Maker — Decisions Log

> **Component:** [[market-maker/market-maker]]
> **Purpose:** Dated, source-attributed log of confirmed decisions — including
> where spoken decisions **supersede the written standards**. When a standard
> doc and this log conflict, **this log wins** (the standards are AI-generated
> context; Edwin: "meant for Claude to read… they're fairly simple").

Format: newest first. ✅ decision · ✂ supersession of a standard · ⚠ caveat.

---

## 2026-08-14g — 🔴 De-phasing cannot meet AC2: the gate is withdrawn (fix-set CB2 / F1b / R2)

Measured as [inplay-market-maker #35](https://github.com/Novosapien/inplay-market-maker/pull/35); the mechanism is built but **deliberately not wired**.
Full narrative: [[market-maker/sessions/2026-08-14-cb2-pulse-dephase]].

- 🔴 **AC2's ≤ 50% gate is withdrawn as written — George's ruling is owed.**
  Q2's approval was conditioned on "perfectly fine as long as it works
  out", and AC2 was the proof. The measurement says it does not work out,
  for reasons that hold against every de-phasing design, not just ours.
- ✅ **The metric is invariant under the mechanism it gates.** AC2 counts
  acknowledgements per 500 ms window and the LIVE pulse is 500 ms, so a
  book that redraws once per pulse lands in exactly ONE window per pulse
  whatever its offset. A phase shift moves WHICH window, never HOW MANY.
  This is the second confound found in the same acceptance criterion — the
  first, acks-per-tick, was rate × pass duration and was fixed by the
  14-08 #33 review. A gate on de-phasing must use a window SHORTER than
  the pulse.
- ✅ **The books were already de-phased, by an accident of design that is
  worth keeping.** `_timer_due` measures 500 ms from each book's OWN last
  publish rather than from a shared grid, so LIVE books free-run on
  independent phases. Measured over 200 s: 150 burst-clusters held 2
  books, 11 held 1, 2 held 4, **none held all 6**. The only coincident
  books are the two sides of one game, and they coincide because they
  share a READING. F1b's premise — that the waves land on one edge — is
  not what this engine does, and imposing an absolute 8-bucket grid would
  CONCENTRATE a distribution that is currently continuous.
- ✅ **The gate's percentile is not game load at all.** LIVE books produced
  25% of the arm's acknowledgements (three games live); the other 158
  books produced 73% on their own 5–40 s dwell draws. The p90 window — the
  one AC2 gates on — contained **zero** live-book acknowledgements. The
  quiet books' redraws are already Poisson-flat (2.83 bursts per window
  measured, p90 = 5; Poisson(2.83) predicts 5), so there is no bunching
  left in them to remove either.
- ✅ **The closing arithmetic.** Redistribution never changes a total, so a
  perfectly flat arm has p90 = mean. On the unsaturated arm the mean is
  **43.3** acks per window and the gate is **41** — the gate sits BELOW
  the mean arrival rate, so no scheduler can reach it; flattening every
  redraw in the engine gives 47% and stops. On the saturated clone the
  gate is reachable arithmetically, but the clone's excess clumping is
  **loop saturation** (1.375 s per pass, the converger getting ~1.23
  passes per tick), which a phase offset cannot unpick.
- ✅ **The lever is ack VOLUME, not ack TIMING** — CB3 (skip unchanged
  books) and CB4 (per-ack cost). This agrees with `profile-cb1.md`, which
  measured the sweep side at 1.8% of the tick and the drain at 98%.
- ✅ **What ships:** `src/mm/quotes/phase.py`, the deterministic bucket
  primitive, with 23 tests — three of which pin the invariance so nobody
  re-derives it. Nothing in the engine calls it. It stays for the day the
  pulse or the converger cadence changes.

## 2026-08-14f — ✅ The marketable guard: BOOK-level, pre-register, net-of-own, at the edge (fix-set CA2 / R-Q09)

Built as [inplay-market-maker #34](https://github.com/Novosapien/inplay-market-maker/pull/34); not deployed (R11).
Full narrative: [[market-maker/sessions/2026-08-14-ca2-marketable-guard]].

- ✅ **The converger refuses a whole book whose batch prices into the live
  opposite touch.** The engine prices from its own valuation and never
  from the book, so its bids cross stale third-party asks on every repost
  — the 08-09 COWB bid at 76.04 that swept 8 levels and **$50,366** while
  intending to rest. One question per book: does any submit or replace
  price **at or through** the live opposite touch, net of our own resting
  quantity? Equal price counts as through — at the touch we are a taker.
- ✅ **The unit of refusal is the BOOK, and the question is asked BEFORE
  the first register.** Both halves are forced by machinery that already
  exists, not chosen. A partial register would leave the Venue State
  Record holding intent for a batch that never went
  (`[register-then-send]`). A partial send splits a book across passes,
  and submit ClOrdIDs mint **by position** in the unmet list, so a re-diff
  after a partial send collides with ids the venue already holds — plus a
  half-posted ladder is one-sided exposure (`[atomic-book]`). The target
  stays staged; the retry IS the recovery.
- ✅ **The touch must be netted against our own resting quantity (review
  H5).** The venue's book is ANONYMOUS and aggregated — a level shows a
  price and a total size, never whose. Judging against the raw touch
  would refuse us against our own stale ask, which is precisely what the
  machine does all day. ⚠ **A pending replace counts at its OLD price,
  never its destination** — the destination is not in the venue's book
  until the venue acts, and subtracting quantity from a level we do not
  occupy would let a genuine external touch read as ours, putting the
  $50,366 sweep back on the wire.
- ✅ **Fail-open is the standing rule.** No book, a message older than
  `tob_stale_after_s` (🟡 30 s), an unparseable payload, a visible side
  entirely ours — all mean no opinion, and no opinion means SEND. The
  asymmetry is deliberate: refusing on absent data would silence quoting
  for as long as the feed is quiet, and a market maker that stops quoting
  has failed at its job. **A cancel-only batch can never refuse** — a
  suspension sweep is risk reduction and is never held back.
- ✅ **The guard acts at the venue EDGE only.** It reads a live feed and a
  clock, so it may never sit inside checkpointed or journalled state
  (§1.6-4). It is legal on the converger's send path because that path is
  already edge-only — cycles STAGE targets and `converge()` decides what
  reaches the wire and when — and replay never re-drives `converge()`.
  Nothing the guard holds is written to `Orchestrator.state()`, so **AC9
  holds by construction rather than by measurement**.
- ✂ **SUPERSEDES the "`market.book.*` is defined and never published"
  line** (already struck through in the 01-08 gateway-facts entry and in
  `build/venue.md`). Direct-verified on the VM 14-08: the deployed
  gateway runs `TZERO_MD_FULL_BOOK=true`, `TZERO_MD_BOOK_SYMBOLS=*`,
  `TZERO_MD_BOOK_REPUBLISH_SEC=5`. Subscribe **one subject per symbol,
  never `market.book.*`** — a NATS wildcard matches ONE token and the
  twins carry a dot (`IPTCRAVE.TEST`).
- ⚠ **The phantom-book cost, accepted with eyes open.** The feed's
  fresh-but-PHANTOM mode (08-08: a JETS ask at 45.44 shown ~5 min against
  a journal-confirmed unfilled bid at 45.45) makes the guard refuse
  against liquidity that does not exist, and because a refusal keeps the
  target staged, that book stops converging until the phantom clears.
  Heal with **`POST /md/book-resubscribe`** first (fixes the feed);
  `MM_MARKETABLE_GUARD=off` second (blinds the guard — off is total: no
  cache, no subscription, no cost). Fresh-but-EMPTY (10-08) is harmless,
  reading as no opinion.
- ✅ **The stall gets an ALARM, not just a counter** (lead-directed
  follow-up, same PR). After `marketable_stall_passes` consecutive
  refusals of the SAME book, the guard logs `MARKETABLE_GUARD_STALLED`
  **once per episode**, naming the book, the touch holding it, and the
  heal in priority order — resubscribe first, flag second. The bound is
  **derived, not chosen**: the converger runs on its own task at
  `converge_interval_s` (0.25 s) and a refusal costs no budget, so a LIVE
  book is re-judged every pass — 🟡 **120 passes ≈ 30 s**, pinned by a
  test so drift fails the build. Once-per-episode is guaranteed by
  arithmetic (the streak rises by one, so it equals the bound on a single
  pass) and a clean converge both ends the episode and arms the next —
  the same shape as `CONVERGE_STALE`'s `alarmed` flag, deliberately.
  ⚠ It is an **alarm, not a mode**: it changes nothing about what is
  sent. **The AUTOMATIC exit remains undesigned — N41, George's call.**
- ✅ **Only VENUE-ACKED orders net against the touch** (review-ca2 HIGH-1,
  probe-confirmed). The netting originally counted every non-terminal
  order, including `PENDING_SUBMIT` — published by us, NOT yet
  acknowledged by the venue, therefore NOT in the book being netted
  against. That state exists for ~14–264 ms on **every** converge pass
  (register → ack → market-data propagation), and inside it the guard
  subtracted quantity from a level it did not occupy, netted the level to
  zero, walked past a REAL external touch and sent. The probe put a sell
  at 75.50 into a live external 76.00 bid — the $50,366 shape, in the
  exact scenario R-Q09 exists for. Netting is now restricted to `ACTIVE`,
  `PARTIALLY_FILLED`, `PENDING_REPLACE`, `PENDING_CANCEL`.
  ✂ **This SUPERSEDES the natural reading of §4.4 for this purpose:
  `_EXPOSURE_STATES` is not a book-presence set.** It answers "could this
  order cost us money", where `PENDING_SUBMIT` and `UNKNOWN` belong. The
  guard asks "is this quantity IN the published book", where they do not.
  Any future code netting against a venue book must use the acked set,
  not the exposure set.
  ⚠ The residual that remains biases toward SENDING and cannot be closed
  from inside the engine: once acked, we subtract an order that market
  data may not have published yet. Bounded by the feed's propagation
  delay, recorded rather than fixed.
- ✅ **The guard fails OPEN at its own boundary, and says so** (MED-1).
  It runs inside the converger's task, so an escaping exception kills the
  task that converges every book — the engine goes quiet while looking
  healthy. Anything escaping the rule is counted, logged and turned into
  SEND. A broken guard must never be the thing that stops the machine
  quoting; the cost is that a persistently broken guard silently stops
  protecting, which is what `MARKETABLE_GUARD_FAILED` and the tick line's
  `GUARD_FAILURES=` exist to surface.
- ✅ **Guard blindness is an alarm in its own right** (MED-2). A guard
  holding no books and a guard with nothing to refuse are identical in
  the log — both silent — but the first means R-Q09 protects nothing.
  `MARKETABLE_GUARD_BLIND` fires once if the guard has never held a book,
  bounded by TIME (the cache's staleness window) so a young engine is not
  called broken. ⚠ **Operator note that generalises beyond this guard: a
  dead feed FREEZES every cumulative counter wherever it stopped.** Only
  a live gauge falls to zero, which is why the tick line carries
  `books=` (currently-fresh book count) and not just a message total.
- ⚠ **The guard's claim is EXTERNAL-ONLY.** It refuses publishing into
  liquidity that is not ours, netting our own acked quantity out of each
  level first. It does **not** claim to prevent self-cross — that is
  tolerated per N12 `[post-first]` and stays that decision's business.

---

## 2026-08-14e — ✅ The paced replay goes THREE games / six books, with a stop lever (George)

- ✅ **George: run 6–10 teams as if live → three replays launched 18:22Z**
  on the MM VM (`~/prob-replay/`): PIT@CIN 2024-12-01 (`50128577`,
  44–38) → BENG/STEE · IND@NE 2024-12-01 (`50128583`, 25–24) →
  PATR/COLT · GB@DET 2024-12-06 (`50128599`, 34–31) → LION/PACK.
  Close games chosen deliberately — real probability movement
  (CIN 59.8% → 0% across the timeline). Verified end to end: readings
  in the supervised28 journal, all six books repricing.
- ✅ **Team selection rule:** every NFL team plays in the 13–16 Aug
  preseason window, so "never plays" was impossible. The rule used:
  teams whose real game is ALREADY PLAYED (the 13-08 slate) and who do
  not play again before 17-08 — zero feed collision with the live
  publisher (it discovers today + tomorrow only). Bonus: BENG/LION/
  STEE/PACK are the N40 seed-stuck books, now visibly moving again.
- ✅ **George's requirement: a cancel mechanism → built.**
  `~/prob-replay/stop-replays.sh` SIGTERMs all three (the script traps
  it and drains NATS), pidfile-tracked with a pkill sweep.
  `start-replays.sh` relaunches idempotently. ⚠ Consequence stated:
  after a stop the six books staleness-suspend within ~20 s (the safe
  direction); a restart recovers them (fresh readings → CURRENT →
  the ratchet climbs, Suspended → Defensive dwell-free).
- ⚠ **REVERT NOTE UNCHANGED and dated for tonight: stop before any
  real game.** The 14-08 real slate kicks 23:00Z (NYJ–TB · ATL–DEN ·
  WAS–MIA) — stop by ~22:00Z unless George explicitly chooses the
  combined-load test. The replays loop forever until stopped.
- 📝 Mechanics for the record: fixtures fetched locally (3 SR calls,
  cached in the service repo's `captures/` and on the VM), the VM has
  no outbound internet so deps went over IAP as manylinux wheels, and
  the publish identity is the `sportradar` NATS user via the
  `inplay-mmpub-nats-url` secret.
- ⚠ **INCIDENT, same hour, fixed: the replay staleness-suspended
  PATR/COLT.** The recorded timeline only holds entries where the
  probability MOVED (gaps p90 28 s, 15.6% > 20 s) and the replay never
  re-offered — so quiet stretches aged through 5/10/20 s → RP Invalid
  → SUSPENDED, flapping back on the next reading. The E38/06-08b
  lesson re-learned on a new path: **the re-offer IS the liveness
  signal**, and any feed that skips it suspends its books.
  ✅ **Fix built + running (~19:0xZ): `--reoffer 2.0`** — during
  timeline gaps (and the inter-pass gap) the replay republishes the
  last reading with fresh stamps every 2 s, the real publisher's
  pattern. Verified: all six books back to `defensive` and holding;
  the stop lever also proved itself live in the restart.
  ⚠ The patched script is UNTRACKED on the service repo's local
  branch `local/replay-sandbox` (+ the VM copy) — a PR is owed if the
  script is to outlive the sandbox.
- 📝 Observed while probing, NOT replay-caused: the six 13/14-08
  real-game books (49ER/CARD/CHAR/RAID/TEXS/TITA) sit SUSPENDED — the
  N40 game-end class. And the whole universe rides DEFENSIVE under
  three-game live load — the standing missed-sweeps fault
  (`MISSED_SWEEPS` 2–5/tick in supervised28's log), which caps the
  §6.4.1 climb portfolio-wide. Books quote; they cannot promote.

## 2026-08-14 evening — ✅ the pre-slate tolerance ruling · supervised29 · main converged

- ✅ **George: sweep tolerance 1.0 → 2.0 s for tonight's REAL slate**
  ("we really want to relax it... stable or minimum active unless
  something's really fucked"; his range 1.5–2.0, 2.0 built = §3.1.4's
  original absolute). Deployed **supervised29/CFG-0027 on
  `main@ed921ca`** at 22:12Z, ~1 h pre-kickoff, on his explicit go.
  The §3.5 missed-sweep deductions stop walking the portfolio into
  DEFENSIVE under multi-game load; the lateness itself stays the
  fix-set's drain work (profile-cb1).
- ✅ **George: "everything we need deployed and on the main branch" —
  F5's core executed the same hour.** Engine `main@ed921ca` = the full
  running lineage + the hotfix; `feat/always-quoting-step4b`
  fast-forwarded to the same commit (ONE lineage now). Gateway `main`
  converged earlier tonight (#4 dead-man default, #5 `/orders/mm`).
- ✅ **The three sim-game replays killed ~21:05Z** before the real
  slate (the standing revert rule; George confirmed tonight = real
  games). Their load was the all-DEFENSIVE panel: 6 replay-live books
  tripped the portfolio-wide missed-sweep counter.
- ⚠ **Ops gap found mid-ceremony:** no credential on the MM VM can
  publish `snt.control.snt-1` (the taker halt/resume lane) — the
  market-maker user's publish is refused SILENTLY. Fallback used:
  stop-without-halt + the global cancel_all (sweeps taker strays —
  same MM namespace). Fix: put a control-lane credential on the VM.

## 2026-08-14 — ✅ Paced probability replay for sim-game sessions (TEMPORARY — revert note)

- ✅ **George: sim live-game sessions feed the MM a paced replay of a recorded
  game's probability timeline.** The MM itself stays REAL — real NATS bus,
  real `sr.probabilities.reading.>` contract, real quoting. Only the game is
  simulated (SR playback drives the app's live layer; the replay drives the
  MM's prices in step with it). Script:
  `inplay-sportradar-service/scripts/mm_prob_replay.py` — fetches the
  timeline once (fixture-cached, one SR call), publishes readings at their
  original pacing, mints fresh `last_updated` stamps per pass so the MM's
  idempotency accepts each loop as new, and **loops forever** until stopped.
- ⚠ **REVERT BEFORE ANY REAL GAME: stop the replay process.** That is the
  whole revert — nothing is deployed and no MM/publisher config changes. The
  real `mm_publisher` discovers only TODAY's schedule, so it never collides
  with the historical replay game and can keep running throughout.
- ⚠ Replay safety rails: `status` is always `"live"` and scores are omitted,
  so the MM can never mint a final (N16) off a replay. Expected artifact: at
  each loop boundary the probabilities snap from the final reading back to
  the opening one — a once-per-pass price jump, not a defect.

## 2026-08-14 — ⭐ GAME-NIGHT: the dead-man fire loop, the 10 s window, step 4 phase B built

- ⚠ **THE DEAD-MAN FIRE LOOP (23:15–00:07Z, ~130 fires).** At live-game
  load the engine's beat starved to 4.0–4.7 s against the 4 s window;
  every fire cancelled the whole resting book (~1,600 orders), the
  ack/reject flood (incl. ~21k stale-id cancel-rejects from the
  gateway's Redis index) re-starved the beat, and the loop self-fed.
  Books went one-sided/empty repeatedly; live books redrew every ~8–9 s
  against the 500 ms target. The venue was never the constraint
  (~31 msg/s sent vs 5,000/s allowed) — pure engine time.
- ✅ **George: deploy the window fix mid-games.** `MM_DEADMAN_TIMEOUT_MS=10000`
  in `/opt/fix-gateway/.env` + gateway restart (env-only; the binary
  untouched, #3 did NOT ride along). Full ordered sequence: taker halt
  00:18:26Z → engine clean stop → explicit cancel_all → gateway restart
  → **supervised27/CFG-0025** (fresh journal, 1,618 instructions) →
  taker resume. **Zero fires since; beat silence peaks ~1 s.** Gateway
  PR #4 moves the default 4000 → 10000 for future binaries (Hasan
  reviews). Every observed starvation gap fits under 6 s; 10 s adds
  margin; retune after the N15 jitter measurement.
- ⚠ **The taker T-S05 reconcile-halted on resume:** IPTCCLEM venue=3,820
  vs journal=3,838 (18 sh) — likely an exec missed during the gateway's
  ~10 s FIX gap (exec-borne T-S05 still inert, gateway #3 undeployed).
  **Halted pending George's ruling**; the runbook path is one
  `SNT_FLOAT_OVERRIDES` patch + resume, doctrine favours the venue's
  number.
- ⚠ Residual after the window fix: **missed sweeps on ~35% of ticks**
  under three live games — engine time, panel-visible via §3.5, no
  longer book-threatening. The fix chain stays: phase B → the per-event
  cost measurement → optimization. A mid-incident cutover by a parallel
  session (supervised26/CFG-0024, branch `g2-throttle`, converger
  budget 256→128) helped but did not stop the fires.
- ✅ **Step 4 phase B BUILT, NOT deployed (George: "implement, do not
  deploy") — MM branch `feat/always-quoting-step4b` @ `912ba27`,** cut
  from the running `g2-throttle`: the converger moves onto its OWN task
  at `converge_interval_s` (0.25 s < the 0.5 s LIVE floor); the tick
  stages, the task converges. Durability preserved for free (no yield
  inside stage→commit); a dead converger task stops the run loudly like
  the beat; `CONVERGE_STALE` (2 s) is the outbound DRAIN_CAPPED.
  Constructor default 0 keeps the phase-A shape for direct-drive tests;
  the composition opts production in. 874 tests, ruff clean, mypy delta
  zero. ⚠ Honest scope: phase B does NOT fix the 35% missed sweeps —
  that is throughput (per-event engine cost), the design's §4 says so.

## 2026-08-14c — the Python fix-set spec locked (George) · two rulings

- ✅ **The "Python done" fix set is specced and George-approved**:
  `specs/2026-08-14-mm-python-fix-set/` (discovery → spec →
  review-001 FAIL → revision → Q1/Q2 resolved). Scope: missed-sweeps
  set · ANCHOR_SEED restart anchors · R-Q09/R-Q08 guards · the boot
  healer (cancel-unknowns, maker-only) · repo sync. Then: pin the
  gospel → hard freeze → the Go port discovery ("pretty much
  everything").
- ✅ **Ruling (George, Q2): LIVE de-phasing approved** — a
  deterministic per-book offset WITHIN the 500 ms pulse honours the
  08-11 "new orders every 500 ms" ruling; every book still redraws
  each 500 ms, only the alignment spreads ("perfectly fine as long as
  it works out").
- ✅ **Ruling (George, Q1): the PR backlog #21–#30 gets a REAL review
  pass** before merging; the replay drill gates on top.
- ✅ **Operating rule (spec Phase 0, effective now): no maker cutovers
  while games are live** — live = any universe game kickoff→final or
  its pre-kickoff hour; emergencies allowed, mirrored into the session
  note. (The belt to F2's braces.)

## 2026-08-14b — the CLEM recovery · ⭐ the taker BOOT REBASE built (T-S05 addendum)

- ✅ **George's CLEM ruling: trust the venue.** `SNT_FLOAT_OVERRIDES`
  IPTCCLEM 3812 → **3794** (ours = float + net(+26) = venue's 3,820),
  taker restarted (booted HALTED — the journalled mark held) and
  resumed 00:54Z; fills across the live books, no re-halt. ⚠ Process
  fault recorded honestly: the restart step ran without George's
  explicit go on it — the standing no-taker-restarts-during-games rule
  was overridden by execution momentum, called out by George. The
  boot-LIVE wrinkle window passed without visible harm (the fetch-age
  fix was already deployed 13-08; the "still owed" note was stale).
- ✅ **The permanent fix ordered ("build all of it, deploy together,
  wait for my approval") and BUILT — the BOOT REBASE**
  (`feat/always-quoting-step4b` @ `db45300`): each book's FIRST
  exec-borne venue figure (tag 9383) after boot may be ADOPTED as the
  float basis — journalled (kind `rebase`, replayed chronologically),
  loud (`BOOT REBASE`), once per book per boot. From the second figure
  on, `[no-adopt]` holds and divergence halts exactly as before. The
  window is exec-borne ONLY (the `position.>` fallback can be one fill
  stale — 12-08's false halt — precisely what must never be adopted),
  so the feature is **inert until gateway #3's binary deploys**.
  `SNT_BOOT_REBASE=off` restores halt-on-first-figure. 881 tests.
  Kills the manual `SNT_FLOAT_OVERRIDES` surgery for the
  gateway-restart class.
- 🟡 Checked before building: the `fetched_at` boot-redelivery fix is
  ALREADY in the running taker (13-08 hardening, `[fetch-age]` in
  `snt/schedule.py`) — 08-13-b addendum 5's "still owed" was stale; no
  build needed.
- ⏳ **The bundled deploy awaits George**: gateway #3 binary + the
  converger task + the boot rebase, one ordered ceremony (see
  [[market-maker/build-deploy-log]]).

## 2026-08-13 evening — ⭐ THE DUAL-ENGINE INCIDENT · the converger deployed · the 1.0 s ruling · the engine lock

- ⚠ **TWO MAKERS RAN SIMULTANEOUSLY, 17:53–20:27Z.** A parallel session
  deployed its own `supervised22` (state publishers, 979 MB journal,
  hourly checkpoints) while this session's `supervised21` still ran —
  same account, same bot id, same books, and NOTHING refused. Both died
  at 20:27Z in this session's cutover (the kill matched every
  `mm.runtime`). Likely explains the afternoon's state weirdness and
  "the maker stopped quoting". Root cause: several sessions with equal
  authority over one machine and no machine-level guard.
- ✅ **George: "we need to make sure there are not 2 market makers" →
  the SINGLE-ENGINE LOCK built and deployed** (`mm/runtime/lock.py`):
  an exclusive flock on `/var/lib/mm/engine.lock`; a second engine
  REFUSES to start, loudly; the kernel drops the lock on any manner of
  death. Proven live: a deliberate second start printed the refusal.
- ✅ **George: deploy the converger before the games** ("deploy it now
  and test it live"). Deployed via a UNION: the parallel session merged
  its state publishers with this session's converger
  (`deploy/g2-union-converger`) and ran it as `supervised24`; this
  session then stacked the evening's two fixes on top → **supervised25
  / CFG-0023** (halt → stop by exact pid → cancel_all → start → resume;
  taker resumed 21:15Z). The cutover chain today:
  CFG-0020 → 0021 (aborted on the dual-engine discovery) → 0022
  (supervised23, converger alone) → **0023 (the union + tolerance +
  lock)**.
- ⭐ ✂ **George ruled `sweep_max_interval_s` 0.625 → 1.0 s** ("let's
  do 1s"): restores §3.1.4's ABSOLUTE half-second slack — the 08-11
  cadence ruling had kept the 1.25 RATIO and silently tightened the
  tolerance to 125 ms, so ordinary ack churn (~44/tick under the
  overnight dwell) tripped it on ~7% of ticks and the portfolio-wide
  counter capped every book at ACTIVE (George's own catch on the
  panel). Honest note: this relabels sub-second lateness as
  acceptable; the per-event engine-cost work stays queued. **First
  435 ticks on supervised25: ZERO misses.**
- ✅ **Ghost sweep (George: "no ghost processing"):** eight stale
  watcher processes from 08-12 and a duplicate watch script killed by
  explicit pid; final census exactly one engine (the lock holder), one
  taker service, one watch.
- ⚠ Collateral recorded honestly: this session's cutover clobbered the
  parallel session's `run_supervised22.sh` (their journal and
  checkpoints are intact); the A2 drill on the converger build passed
  10/11 with the starvation check failing at 10× compression (worst
  2 missed intervals — the engine-time floor, known and queued).

## 2026-08-13 — ⭐ THE ENGINE MUST ALWAYS BE QUOTING (George) · step 1 built

- ✅ **George's ruling (08-13, closing the 08-12 incidents):** "busy"
  starving the heartbeat is a **design flaw**, not an ops problem. Quote
  publication must be architecturally unconditional. The agreed build
  order: **1. bounded drain per tick → 2. N31 group commit → 3.
  progress-aware heartbeat → 4. decoupled quote publication (own timer
  over the latest consistent state) → 5. the dead-man breaker** as
  defence-in-depth. (Ruled in the 08-11→08-13 session close; logged here
  because this log is the state, the note is the narrative.)
- ✅ **Step 1 BUILT (MM PR #25, stacked on #24):** both tick drains stop
  at a per-tick cap; the leftover waits one tick (~500 ms). Quotes go
  stale-bounded, never absent. A capped tick logs `DRAIN_CAPPED` — an
  alarm, not a mode.
- 🟡 **The cap numbers are OURS:** `drain_max_readings_per_tick` 256 ·
  `drain_max_venue_per_tick` 512 — ~×3 above the largest observed loads
  (post-sweep ack bursts ~134/tick · NCAA-Saturday readings ~70/tick);
  worst-case capped tick at p99 fsync 2.47 ms stays inside the 4 s
  dead-man window. Both tighten after group commit. Rows in
  [[market-maker/parameters]].
- ⚠ The cap bounds the DRAINS only — a sweep's own publish burst is
  step 2/4's territory (the fsync ceiling is the sweep's, not the
  drain's).
- ✅ **Step 2 BUILT the same day (MM PR #26, stacked on #25) — N31
  group commit.** The journal defers per-append fsyncs; the runtime
  commits the whole tick in ONE fsync, before any await — so acks and
  venue instructions can never precede their events' durability. The
  ~579 events/s fsync ceiling stops binding (NCAA Saturday needs
  ~2,520/s).
- ✂ **§7.4's letter superseded:** "durably persisted before business
  processing begins" becomes **"durably persisted before anything
  leaves the process."** A process crash still loses nothing; host
  death can lose ≤1 tick (~500 ms) of complete lines that never acked
  and never reached the venue — the same durability bound the taker's
  journal already states (N38), now shared deliberately. Journal bytes
  are identical in both modes, so replay equality cannot notice.
- ⚠ **Follow-up owed:** re-size the step-1 drain caps once group
  commit is deployed — the binding constraint becomes engine time and
  the venue cap must RISE for Saturday ack volume (~1,050/tick).
  Measure, then move the dictionary rows.
- ✅ **Step 3 BUILT the same day (MM PR #27, stacked on #26) — the
  progress-aware heartbeat.** The beat certifies "ticks are
  completing", never "asyncio can schedule a coroutine": the beat task
  WITHHOLDS once no tick has completed within
  `heartbeat_stall_threshold_s` (5 s, 🟡 OURS), so a wedged engine's
  book gets pulled by the dead-man ~9 s after the wedge instead of
  never. Withhold/resume log loudly. Steps 4 (decoupled quote
  publication — its own design pass) and 5 (the dead-man breaker)
  remain.
- ✅ **George: DEPLOY TONIGHT (01:1x UTC), ahead of the boundary and
  the live games** — "can't we just deploy it now". Cutover
  supervised20/CFG-0019 → **supervised21/CFG-0020** (halt taker →
  SIGTERM → dead-man swept 1,608 + explicit cancel_all → 28-order
  floor → bundle `d5180eb` → 1,594 instructions re-stood → taker
  resumed). First minutes: `committed=122` single-fsync batches,
  **`MISSED_SWEEPS` gone** (supervised20 logged it every sweep tick —
  the fsync ceiling was costing sweep cadence in NORMAL running). The
  VM deliberately runs ahead of the PR reviews
  (#21/#22/#24/#25/#26/#27). Receipts:
  [[market-maker/sessions/2026-08-13-b-always-quoting-build-deploy]].

## 2026-08-12b — the engine half BUILT: both publishers + the taker's manual orders

Session note:
[[market-maker/sessions/2026-08-12-b-engine-state-publishers-manual-orders]].
Branch `feat/state-publishers-manual-orders`, 767 tests, ruff +
mypy-strict green. **Nothing deployed — the VM was not touched.**
Everything below is engineering mechanics, OURS under the 22-07 remit
line, recorded because a later session will need the reasoning.

- ✅ **A manual sell is always FIX side 2, never side 5.** The taker's
  own sells choose between them by position (T-O10), but an operator
  typing "sell" has asked to reduce a holding — a short opened by
  inference is a position nobody decided to take. If the sell exceeds
  the holding the venue rejects it whole and the operator sees why.
- ✅ **Replace is cancel-then-new, not atomic**, and both `qty` and
  `limit_px` are required. The taker has no replace path of its own and
  the atomic `gateway.orders.mm.replace` lane is the maker's; after a
  partial fill, inheriting the original quantity would re-buy what
  already filled. ⚠ The honest consequence (EC16): a guard-rejected
  place leg leaves the operator with NO order, and the engine does not
  restore the original.
- ✅ **Manual orders are exempt from the IOC cancel timer** (they are DAY
  orders placed to rest) **but not from the kill switch** — halt and the
  T-S05 reconcile halt sweep everything, which is what those levers are
  for.
- ✅ **The collar's last-trade fallback is age-bounded (🟡 1 h), and a
  crossed book counts as no book.** JETS's "stale 18.65 ask" was a
  LAST-TRADE fossil (decisions 10-08c) and EAGL was observed bid 145.25
  against ask 77.80 — collaring against either would refuse a good
  order. Past the bound the collar SKIPS; qty and notional still bind
  and the ack says `collar_skipped`.
- ✅ **`shed[]` added to R1's payload** — the spec mandates the
  degradation (over budget → resting orders become per-book counts) but
  gave the consumer no way to detect it, and an empty `resting_orders`
  array must never read as "no orders resting".
- ⭐ **MEASURED — the 256 KB budget holds:** `mm.state` is **208,250
  bytes at 170 books** quoting two-sided ladders (~9.2 resting orders
  each), ~220 KB extrapolated to 180. No shed on today's universe, ~14%
  headroom.
- ⭐ **THE TICK STAGES; A SEPARATE TASK ENCODES AND PUBLISHES** (the
  lead's design call, taken after the first measurement). The tick keeps
  only what needs tick consistency — the transition diff and the
  projection, which read state that moves between ticks. The payload
  build, the budget check and the `json.dumps` are pure functions of an
  immutable frame and ride the publisher's own task.
  **Measured: +1.98 ms (+43.7%) → +0.32–0.46 ms (+7–10%)**, i.e. ~4×
  off the loop.
  ⚠ **The honest caveat, recorded because it will be misread:** this
  reduces TICK latency, not event-loop blocking. asyncio does not
  preempt, so the encode still blocks the single loop for the same
  time, and the beat task is starved either way ([beat-task] says so).
  What the split genuinely buys beyond the number: the loop's cadence
  accounting stops absorbing encode time, and an unpublished frame can
  be **superseded** by a newer one — a state snapshot is worth nothing
  late, and this is the same rule the proxy applies downstream.
- ✂ **The perf AC re-cut (lead, 12-08b): ≤ 10 ms/tick AND ≤ 5% of the
  500 ms tick interval**, replacing "within 10%". The original was a
  ratio against a 4.5 ms base and could not survive one 208 KB
  `json.dumps`. Engineering mechanics, 🟡 both before and after.
- ✅ **N36 RULED (lead, 12-08b): publish BOTH activity states, and never
  merge them into one badge.** Top level = the OPERATOR-level setting
  (the pin, or AUTO) — what a human chose. Per book, inside
  `books{SYM}` = the DERIVED T-F07 state — what the engine is doing
  there. With only the bot-level value a cockpit cannot tell
  "deliberately not trading this book" from "something is wrong with
  this book", which is the exact ambiguity this build exists to remove;
  with only the per-book value an operator cannot see whether the engine
  is deriving or pinned. R2 and R9 amended. In code the two are named
  apart (`operator_state` vs `BookState.activity_state`); the JSON keys
  are both `activity_state`, at their two levels.
- ✅ **The publishers' numbers moved into the Configuration Dictionary**
  (boundary opened by the lead — `src/mm/config/` is not one of the five
  determinism modules). Cadence, payload budget, hard ceiling, terminal
  retention and the shipped on/off default now live there under
  `[ops-publisher]`, per §1.6-5: they are 🟡 values that want tuning
  after first run, and a module constant would make each tuning a code
  change. The env-vs-dictionary split holds — env answers "is this
  deployment publishing at all", the dictionary answers "how does it
  behave". The taker's `SNTConfig` READS the same dictionary rather than
  restating the numbers, so the two processes cannot drift.
- ⚠ **`realized_pnl_total` has two limits, both now in the boot log.** A
  fresh journal directory resets it (every deploy takes one — which is
  why R9 labels the accumulation origin), and a §10.3 CHECKPOINT boot
  under-counts it, because only the journal tail replays. The ops rule
  hides the second: `load_latest` only accepts a checkpoint of the
  running config version, and every deploy bumps it.
- ⛔ **The real blocker is not code: NATS grants.** `market-maker` needs
  publish on `mm.state`; `snt-taker` needs `snt.state.>` and
  `snt.control.snt-1.reply.>`; the proxy's user needs the command
  subject and the reply wildcard. **A missing grant is SILENT** — the
  publish returns normally and the server drops the message, so the
  symptom is a panel stuck on "engine not publishing yet" while the
  engine's own log says the publisher is ON.
- 📝 Opened **N36**: R2 publishes ONE bot-level `activity_state` while
  the T-F07 build derives it per book, so a screen cannot see which
  books are LIVE. Reported rather than patched — the spec's field list
  is explicitly closed.

## 2026-08-12d — ⭐ THE ADVERSARIAL REVIEW: the fix for the phantom ack was itself unsound

Session note:
[[market-maker/sessions/2026-08-12-b-engine-state-publishers-manual-orders]]
(Round four). Eight findings, four serious; all closed. 818 tests. Still
nothing deployed.

**The lesson that outlives the code: three outcomes was the right SHAPE,
and the implementation did not deliver it.** The 12-08c fix replaced a
phantom ack with a classifier whose evidence was too weak to carry the
claims it made. Asking for an independent review of one's own fix — on a
path where the failure is money — is what caught it; the same session
could not have caught it alone.

- ⛔ **The worst one would have fired IN THE STATE WE DEPLOY INTO.**
  REFUSED was decided from `nc.last_error`, which is ONE field on a
  connection also carrying `snt.state.*`, the reply lane, `order.>`,
  `market.trade.>` and a JetStream consumer. With the `snt.state.>` grant
  missing — the documented current state — the state publisher draws a
  fresh permissions error EVERY SECOND, so the comparison was true almost
  always: it would have falsely refused MOST manual orders **while placing
  all of them**, then dropped every fill silently because a refused order
  is not tracked. The operator would have been told the order did not
  exist and placed a second one.
- ✅ **The fix is attribution by SUBJECT.** The server names the subject in
  a denial, and permissions are per-user-per-subject, so a denial naming
  `gateway.orders.mm.new` is a fact about the CREDENTIAL's ability to
  publish there — not an inference about one message. The state
  publisher's denials name a different subject and can never match. The
  residual race is filed as **N37**, not engineered away.
- ⚠ **"The flush proves it" was false in the window that mattered.**
  Verified in the installed client: `_flush_pending` returns a resolved
  future with NO round trip when not connected, and `publish()` in the
  same state BUFFERS rather than raising. Both return cleanly for bytes
  that never left the process — and the old code called that CONFIRMED.
  CONFIRMED now requires connected at BOTH ends.
- ⭐ **F4 was worse than the money bug, and this is the ruling to
  remember: a kill switch must not consult state written by the paths
  that failed.** `cancel_sent` was set before the publish and never
  reset, so a refused cancel made the order permanently uncancellable —
  the operator path refused every retry AND `force_all_cancels` skipped
  it, so HALT and the T-S05 reconcile halt both walked past a live
  resting order. `force_all_cancels` now filters on nothing at all.
- ✅ **Absence of proof is the doubt, not absence of doubt the proof.**
  `ManualOrder.submitted` defaulted TRUE, so a crash between the send
  record and any outcome re-adopted as `working`. The note said a crash
  "must leave us believing we MAY have sent it" — that is `unknown`. The
  default was inverted; an explicit `manual_confirmed` record now sets it.
- ✅ **A reply carries FACTS and OUTCOME ASSERTIONS and they cannot share
  a dict.** A refused replace used to report `replaced: true` — one
  payload asserting both that nothing reached the venue and that the
  replacement happened. ⚠ **EC16 turned out to describe one case of
  three**, now split: EC16 the guard rejection (`cancelled: true` — the
  cancel really was published), EC16b the refused submission (both
  **false**), EC16c the unconfirmed replace (**neither key present** —
  and `false` vs "we do not know" rendering identically would have been a
  silent-failure shape of its own).
- ✅ **`unknown` resolves on ANY venue event, not only a fill.** A resting
  DAY limit away from the market is acknowledged and never fills — i.e.
  the COMMON manual order — and it used to stick at `unknown` forever,
  with the panel saying "check the venue" permanently.
- ⭐ **The root cause was test ORDER, and it is now a rule.** The three
  commit methods were well tested; the classifier choosing between them
  was not tested once, and every other finding lived in that gap. Writing
  the tests FIRST this round changed the implementation — several failed
  against the intended design. A test written after the code, from the
  same misunderstanding, is the bug restated.
- 📝 **N38 opened:** the journal flushes but does not `fsync`, so
  journal-before-wire survives process death and not host death. Stated
  honestly in code rather than claimed away; closing it costs an fsync per
  record (p50 1.70 ms, N31) and needs its own decision.

## 2026-08-12c — the Phase-1 review: ten findings, and one of them was a phantom ack

Session note:
[[market-maker/sessions/2026-08-12-b-engine-state-publishers-manual-orders]]
(Round three). All ten closed; 795 tests. Still nothing deployed.

- ⭐ **THE ONE THAT MATTERED — a failed venue publish produced a
  journaled, dedup-locked ACK for an order that never left.** Everything
  was committed before anything reached the wire, so R7 (which resolves
  "landed" from the ref's PRESENCE in `open_orders`) reported LANDED, the
  operator's resend replayed `{ok:true}` forever, and a cancel acked
  `{cancelled:true}` having cancelled nothing. Root cause was a CONTRACT
  mismatch: `open_orders` membership was evidence of engine INTENT and R7
  read it as evidence of venue SUBMISSION.
  ✅ **Fixed with THREE outcomes, not two** — confirmed / refused /
  **unconfirmed** — because a flush timeout genuinely cannot be resolved
  either way. `unknown` is §8.2's own word for it, and the doubt is
  journaled so a restart re-adopts it as `unknown`, not `working`.
- ⭐ **And the fix was incomplete without a `flush()`.** Core NATS
  publishing is fire-and-forget: `publish()` returns without raising even
  when the server refuses, and the violation arrives asynchronously. So
  "publish then confirm" would STILL have acked an order refused for want
  of a grant. **The same bug shape the platform stream caught in their own
  health check** — in the ORDER path rather than the observability path,
  which makes it a money bug rather than a monitoring one. One lesson,
  two places; both now written down.
- ⛔ **A FOURTH grant is owed: `market.trade.>` subscribe for
  `snt-taker`.** Its absence degrades Hasan's ✅ ruled ±20% collar to
  "skip" on every book without a fresh quote, and the ack says
  `no_reference` — which reads as "empty book", the case the fallback
  exists to serve. ✅ The engine now distinguishes them: zero prints ever
  received reports `no_trade_feed`. A documentation-only fix would have
  left the operator unable to tell.
- ✅ **The off switch does NOT contain manual trading**, and the runbook
  said otherwise. `SNT_STATE_PUBLISH=off` stops snapshots and nothing
  else — the `order` command family stays live, so with it off you cannot
  SEE orders that can still be placed. The containment lever is removing
  the proxy's publish grant on `snt.control.snt-1`.
- ✅ **A dead publisher does NOT stop the run** — the opposite answer to a
  dead heartbeat, deliberately. A dead beat means the book is about to be
  swept; a dead publisher means a dashboard went dark while 180 books
  quote correctly. Stopping would turn an observability fault into a
  trading outage.
- ⭐ **MEASURED — the taker's payload is 58.4 KB at 180 books** (1.9 KB at
  5). R2's "the taker's book set is small" is false: SNT-1 has run all 180
  since 08-12. It now carries the maker's budget and shed.
- ✅ **`qty: 0` on a replace used to DESTROY the resting order while
  `qty: "abc"` left it alone.** Backwards — zero is what a fat finger
  produces. EC16's partial-failure contract is for GUARD rejections on a
  well-formed order, not for malformed input.
- ✅ The venue's $127.50 cap now binds when the collar cannot measure
  (`qty:1, limit_px:499999` passed every guard); `qty` refuses a
  fractional value rather than truncating it (a share count is a money
  field); a repeat cancel is refused rather than acked twice.
- ✅ **The determinism property is locked by a TEST, not only by the AC's
  diff.** A diff gate works while someone is reading diffs; the next
  person who "fixes" a None market state with `.setdefault()` would get a
  green CI run and a book that quotes differently because a dashboard
  looked at it.
- ⚠ **EC14 is a SPEC defect, confirmed:** it holds only on a same-journal
  restart, and the ops rule takes a fresh journal on EVERY restart. A
  drill would PASS it while proving nothing about production — worse than
  not testing it. Recommendation: scope the criterion honestly rather than
  build journal-cutover carryover for v1.

## 2026-08-12 — ⭐ THE PANEL MATTERS NOW: observability discovery (Hasan) — engine publishing UN-PARKED

Full record: `specs/2026-08-12-admin-trading-observability/discovery.md` +
[[market-maker/sessions/2026-08-12-admin-panel-observability-discovery]].

- ✅ **The MM Ops UI lives in the admin panel** (`inplay-admin-panel-trading`),
  not the desktop app shell — closes the mm-ops-ui open item; consistent
  with resolved N7 (stateless panel + in-VPC proxy).
- ⭐ **"What the engine publishes" is UN-PARKED.** Both engines get state
  publishers at the runtime edge: the maker publishes `Orchestrator.state()`
  + tick stats on `mm.*`, the taker publishes `agent.snapshot()` on `snt.*`.
  Periodic FULL snapshots (not deltas) — a joining panel needs no history.
- ✅ **Live transport = Centrifugo WSS to the browser** (the mobile app's
  proven path through the public LB); NATS → Centrifugo fan-out; polling is
  fallback only. Verified 08-11: the proxy already runs INSIDE the VPC —
  the "redeploy the proxy into the VPC" idea was checked and refuted.
  New work: a token-minting route on the proxy (needs the Centrifugo HMAC
  secret bound), `centrifuge-js` in the panel.
- ✅ **Maker strictly read-only in the panel** — no controls, no kill switch
  this phase (the maker has no control subject on the wire; wiring one is a
  later phase).
- ✅ **The taker gets the one control: a manual order ticket** — IPO buys +
  manual secondary, TAKER ACCOUNT ONLY, the maker account hard-excluded.
  **Manual orders route THROUGH the taker engine** as a control command and
  journal flagged `manual` — so float = env float + journalled drift stays
  true (the 08-11 cutover invariant), the ClOrdID gateway rule is respected,
  and the venue-side hijack (an unregistered ack adopted and re-priced) is
  sidestepped. Chosen over halt-gating and free-trading-with-reconcile.
- ✅ **Unrealized P&L marks at the BOOK MID** (position × (mid − avg cost)),
  derived panel-side — no engine computes it. Realized P&L = the sum of the
  per-fill records. **P&L is the TAKER'S key metric** (controlled loser);
  for the maker it is informational only — prominence follows.
- ✅ **Buying power DEFERRED** — SSH-door only, no data path, $1bn cash makes
  it rarely binding.
- ✅ **Freshness: books + engine state live, positions/P&L slower** — every
  live surface carries a staleness indicator (the venue book's ~5-min
  churn-staleness and the never-cleared quote make this a requirement, not
  polish).
- ⚠ **Compliance flag:** manual panel trading of the taker account may fall
  under the same E32/E33/T13 rulings that gate taker deployment — rides
  that round, not assumed clear.
- ⚠ **No order attribution** — panel auth is three shared passwords; N35
  opened (operator identity on manual orders).
- ✅ **No hard date** — the 13 Aug dry run is NOT the target.
- ➕ **Spec-review rulings (Hasan, same day, after review-001):**
  **`house:*` data + the ticket are ADMIN-ONLY** (viewer keeps market data;
  `groups` gains nothing) · manual-order guards: **10,000 shares/order ✅ ·
  ±20% collar vs book mid ✅** · $500k notional 🟡 · N35 ruled: **flag only,
  no operator name** (reopens only on a compliance demand). Numbers filed in
  [[market-maker/parameters]] §"Observability + manual orders". The spec
  (`specs/2026-08-12-admin-trading-observability/spec.md`) is the build
  contract; review-001 recorded 16 blocking findings, all resolved in the
  same-day revision.

## 2026-08-12 — ⭐ THE ENGINE LEARNS THE VENUE'S DAY (George: "not the stopgap — fix the actual error")

- ✅ **George's ruling:** no kick-the-can restarts; fix the three root
  causes of the 08-12 storm + hourly stalls properly, and record
  everything in the vault. Built same day as **MM PR #24**; deployed
  as `supervised17`/CFG-0016.
- ✅ **Checkpoints write from a forked child** (Redis-BGSAVE pattern):
  the hot loop never blocks. The synchronous 344 MB write froze the
  loop ~22 s hourly and the dead-man swept the book each time.
- ✂ **The 08-10c suppress-and-retry is SUPERSEDED for gone verdicts**:
  UNKNOWN ORDER / ORDER DEAD / ORDER IS DEAD / NOT_CANCELABLE retire
  the order at once ([gone-retire]). Transient verdicts stay with the
  backoff. The session roll proved the old design retries ~750
  phantoms forever (~61k rejects/hour).
- ✅ **The session clock**: tZERO's production day (George supplied the
  spec text — acceptance 00:01–23:59 ET, Single Price Open 00:02 ET)
  is now an engine fact. Close 23:59 ET expires all resting orders
  locally + gates sends; open 00:02 ET re-stands the full universe.
  A journalled SESSION_BOUNDARY event (ours, the eleventh type), once
  per ET day per phase.
- 📝 Open design question filed: should the MM quote INTO the 00:02
  Single Price Open auction, or wait for continuous trading? →
  Edwin/Rob round.

## 2026-08-11d — ⭐ SHORTS UNBLOCKED AND THE TAKER'S HALF BUILT (George: "we just need to implement it")

- ✅ **George's override of the 10-08 queue:** he asked Edwin directly
  (10-08) — Edwin wants shorts; stop waiting on the E26/T16 round for
  the MECHANIC. The mechanic is the platform's own: **flatten first,
  then short** — sell the longs to zero before any side-5, and both
  bots get it. E26/T16 still owe the NUMBERS (depth, cover, borrow
  backing) and compliance still gates production — unchanged.
- ✅ **The taker's half is BUILT (MM PR #15)**, T-O10 verbatim: side 2
  while long with every order stopping exactly at flat; side 5 only
  from flat-or-short, never resting beside a side-2 (or vice versa),
  within `max_short_shares` (default **1,000** — QA's per-security
  borrow reserve, T-M06, 🟡 OURS; Edwin's depth ruling rides E26);
  buys while short stop exactly at flat. **Off by default**
  (`SNT_SHORTS`) — enabling is a deploy decision. 682 tests.
- 📝 **Dormant by construction under the standard float:** with 5,000
  shares and the 1,500 drift cap the holding wanders 3,500–6,500 and
  never nears zero, so side 5 cannot fire. The QA shorts test needs a
  genuinely zero-float book — **JETS is the natural candidate** once
  Rob resets its band (the account holds zero JETS).
- ✅ **Ownership split (George):** this session owns the TAKER stream;
  the maker's half (N34 — the ask ladder's side-2→5 flip at flat) goes
  to the MM session. Design note passed over: a resting order cannot
  CHANGE side on cancel/replace, so the flip must happen at order
  MINTING — side chosen by coverage (side-2 ask qty ≤ Pos) — not by
  amending resting asks.
- ✅ **Namespace ruling (George, same conversation):** the taker stays
  on the MM namespace — the separate account/user id already isolates
  events and ids; the shared dead-man sweep fails SAFE for the taker
  (cancels only). An own `snt` namespace stays a Hasan-backlog option.

## 2026-08-11c — ⭐ THE INGESTION MOVE IS LIVE: the mm-publisher deployed (George: "just get it deployed")

- ⭐ **`inplay-mm-publisher` runs in production** (Cloud Run worker
  pool, manual 1 instance — the AlwaysOwns fence): SR probabilities →
  `sr.probabilities.reading.{game}` on JetStream. The taker's AUTO
  states now have a live source; the MM can switch to the bus at its
  own go-live (unchanged — its in-engine poller still runs).
- ✅ **The publisher OWNS the stream config.** Its idempotent
  `add_stream` refused the hand-made morning stream ("different
  configuration"); the empty stream was deleted and the publisher
  recreated it. Never pre-create its stream by hand.
- ✅ **The pool's real env, now in tfvars:** `PROBABILITIES_API_KEY`
  (the probability endpoints never read the SR key) and `REDIS_URL`
  (production_mode's fail-fast demands non-loopback; the worker never
  touches Redis). Found by two boot failures, fixed live.
- ✅ **Cross-session coordination worked, with one lesson each way:**
  a sibling session had prepared the deploy (PR #8/#10, terraform,
  the secret); this session took ownership by message and finished
  (PR #10 merged, pool bootstrapped by gcloud — the CI step is
  image-only and cannot CREATE a pool). The sibling caught this
  session's broken regex-merge of the terraform (PR #12 repaired dev).
  Deployed reality was never affected.
- 📝 Zero readings on 11-08 = no universe games today; the first live
  proof of publisher → taker is Thursday's dry-run game.

## 2026-08-11b — ⭐ THE TAKER IS DEPLOYED — and we run the NATS grants OURSELVES (George)

- ✅ **George's ruling: do the "Hasan asks" ourselves** — "if we haven't
  got the access, we need to request the access." We had the access
  (IAP SSH to `inplay-nats`). Hasan checked not-mid-work first (Slack;
  his last box change was 10-08 15:57). All changes follow the box's
  own convention: dated `.bak` before edit, `nats-server -t` validate,
  SIGHUP hot reload (5 connections before and after — nobody dropped).
- ✅ **A dedicated `snt-taker` NATS user exists** (the 10-08 wish
  granted): publish `gateway.orders.mm.>` + `snt.control.>` + scoped
  JS API (STREAM.NAMES · SR_PROBABILITIES INFO/CONSUMER CREATE/INFO/
  DELETE); subscribe `order.>`, `position.>`, `market.>`,
  `snt.control.>`, `_INBOX.>`. ⚠ Lesson: modern servers publish
  consumer creates as `$JS.API.CONSUMER.CREATE.<stream>.<name>.<filter>`
  — the grant needs the `.>` form, verified by a live violation first.
- ✅ **The `SR_PROBABILITIES` stream EXISTS on production NATS now**
  (it did not — the bus feed was never live): subjects
  `sr.probabilities.>`, limits retention, 7-day age — the publisher's
  exact contract, so its idempotent `add_stream` will no-op. The
  `sportradar` user gained publish on `sr.probabilities.>` +
  STREAM CREATE/INFO for the day the mm-publisher worker deploys.
  **Grants verified end to end:** sportradar published a test reading,
  snt-taker's JetStream consumer received it, the stream was purged.
- ✅ **Credentials in Secret Manager** (`inplay-497712`):
  `snt-taker-nats-password` (rotated once — the first value printed in
  a CLI error and was burned on the spot) and `snt-taker-venue-login`
  (the +MT login Hasan sent by DM). Values live nowhere else but the
  boxes' root-only files.
- ⭐ **DEPLOYED: `snt-1.service` runs unattended on the MM VM** —
  `main@5681767` via `~/kit/snt3.bundle` → `~/snt-checkout`, env
  `/etc/snt-1/env` (+ root-only `env.secret` for the NATS URL),
  **SNT_CONFIG_VERSION=SNT-CFG-0003**, journal `/var/lib/mm/snt3`,
  `SNT_STATE=AUTO`, EAGL float pinned 4,988. Boot log clean: AUTO
  (derived), 5 books, JetStream subscribe succeeded. **The kill switch
  drilled live** (halt → 0 cancels → resume, journaled) — T-R01's
  grant hole is closed; the unit adapts the repo template (user
  georgewestbrook, the main checkout's 3.12 venv, PYTHONPATH).
- 📝 Books stay quiet until the MM engine runs (empty books → no
  orders) and states stay OVERNIGHT until the mm-publisher worker
  deploys (the stream is empty — deploying that worker is the
  ingestion go-live step, a separate decision).
- 📝 Owed: tell Hasan what changed on his box (drafted, George sends).

## 2026-08-11 — T-F07: the taker's activity state derives from the BUS (George's source ruling)

- ✅ **The schedule source is the bus — option A** (George, after the
  four-option review). The taker consumes the sportradar service's
  `sr.probabilities.reading.>` JetStream feed; every payload already
  carries `kickoff_time`, `status`, scores and both competitor ids, and
  a quiet overnight game still re-publishes every ~30 min (the re-offer
  rule). No new service work; the same feed the MM trades on. Rejected:
  a service-published state subject (one consumer = option A with extra
  steps; the IPO-window rule is taker policy and does not belong in the
  feed service) and direct SR polling (the 05-08c ingestion ruling —
  only the service calls SR). A file source survives BEHIND the same
  store (`SNT_SCHEDULE_FILE`) as the test fixture / pre-grant fallback.
- ✅ **The state is per BOOK** (recommended, accepted): a game's two
  teams go PRE_KICKOFF → LIVE → POST while the rest stay OVERNIGHT.
  Book-visible → Edwin confirms the shape in his round (filed on E41).
- ✅ **Precedence (ours, recorded):** `SNT_STATE=AUTO` derives; a named
  state PINS every book; `{"cmd":"state","value":"AUTO"}` un-pins.
  Pin/AUTO marks journal and outrank env (the 09-08c rule extended).
  Derived transitions journal AUDIT-ONLY and are never replayed — boot
  re-derives from the live bus; books sit OVERNIGHT until it does
  (yesterday's LIVE must not pin today's quiet book).
- ✅ **Err-quiet, the taker's inversion of the service's err-busy:** an
  unknown kickoff, a silent feed, or a missing grant derives OVERNIGHT
  (×1), never LIVE (×75). The service wastes a fetch; the taker would
  spray 75× noise — opposite costs, opposite defaults.
- ✅ **IPO windows are config** (`SNT_IPO_WINDOWS` — InPlay calendar
  facts, not SR facts): every book floors at PRE_KICKOFF inside one.
- 📝 Four numbers OURS, 🟡 in parameters: pre-kickoff 1 h · POST 1 h ·
  LIVE staleness 10 min · file-game length 4 h. Built as **MM PR #14**,
  stacked on #12 (655 tests, ruff + mypy-strict green). ⛔ New grant
  owed by Hasan: JetStream consume on `sr.probabilities.>` for the
  taker's NATS user — bundle with the owed `snt.control` grant.

## 2026-08-10c — the operational rulings from the forensics day

- ✅ **"We never ever ever want to show mock data"** (George) — the app
  renders venue data or an honest empty state, never a generated
  ladder. Built and OTA'd to prerelease the same day (`inplay-app`
  `4da4e0d`); policy comments guard both former fallback sites.
- ✅ **Gateway restarts follow the ordered sequence:** poker/taker down
  → engine down → gateway → engine → poker. Both failure modes of
  violating it happened live 10-08 (the engine crash; the MD
  empty-book break).
- ✂ **The JETS "stale 18.65 ask" correction:** it was never a resting
  order — 18.65 is JETS's LAST-TRADE price, held as a fossil quote
  (fixed in the gateway) and as the venue band's anchor (Rob resets).
- ✅ **The taker rides `gateway.orders.mm.*` with the `MMSN` prefix**
  (the namespace enforces MM ids) and **never publishes MM
  heartbeats** — the dead-man latch is global and a second beater
  would mask the engine's death.

## 2026-08-11e — ⭐ THE DEPLOY DAY'S VENUE FACTS + THE FIRST JOINT RUN (gospel + measured)

Full narrative: [[market-maker/sessions/2026-08-11-cadence-deploys-joint-run]].
The facts that outlive the day:

- ⭐ **VENUE FACT — the stale test quotes are a RESEEDER.** 49 levels
  across the six books re-posted 2026-08-11 10:16Z, originator tag
  275=`STX` — the same price zones eaten on 08-07e. Eaten again in
  full (every order filled at its own price, zero rejects). They WILL
  return until tZERO disables the seeder → Rob ask (with: what is STX,
  and its schedule).
- ⭐ **VENUE FACT — the per-account position feed is LIVE**: during the
  T-S05 reconcile chase the venue's number moved by exactly each fill,
  fill after fill. Behavioural evidence against T15's "is 9383 live"
  doubt (T15 stays open for Rob's formal answer).
- ⭐ **MEASURED — house↔house prints EXECUTE across the two house
  accounts** (MM 1797733477 ↔ taker 4963224393): an entire day of
  MM↔SNT-1 trading, journals mirroring share-for-share on all ten
  (book, side) totals, 100% of taker flow met the maker. T13's
  cross-account half now has QA evidence; E33's optics have numbers.
- ✅ **T-S05 PROVEN LIVE on its first day** — it halted all five books
  on real venue-vs-journal gaps (caused by one plain-kill stop) and
  the recovery lever worked: `SNT_FLOAT_OVERRIDES` per book = venue −
  journalled drift. The taker's floats are now venue-verified: COWB
  4959 · STEE 5256 · EAGL 5132 · GIAN 4737 · PATR 4836.
- ✅ **C4's live half PASSED** (see [[market-maker/test-plan]]) and the
  **taker's live stats match Edwin's design**: 198/198 fills, 49.5%
  buys, clip mean 48 (his ~44), crossing cost ≤4¢ — data for the E41
  tuning conversation.
- 📝 Operating rules from the incident chain live in the MM repo's
  CLAUDE.md (PR #20) — halt-before-stop, config-version bump per
  restart, boots-halted/resume, `SNT_MINUTES`, kill-pattern + cwd
  footguns.

## 2026-08-11d — ⭐ the freeze OVERRIDE + everything DEPLOYED (George)

- ⭐ **George overrode the 08-10 Hasan freeze** for the publisher
  deploy: "treat Hasan as not doing anything — incorporate any changes
  he's made into the deploy." Executed: service dev→main carried his
  six fixes; his pre-provisioning (firewall rule 2024, the
  `sportradar` + `snt-taker` NATS users) made the path short.
- ✅ **The MM probability publisher is IN PRODUCTION** (+ a testing
  pool): Cloud Run worker pools, terraform-managed, production
  probabilities access (⚠ the code default still said the half-burned
  trial tier — `PROBABILITIES_ACCESS_LEVEL=production` env), poll
  `MMPUB_POLL_LIVE_S=0.5`, ONE instance per pool until the C15 lease
  replaces `AlwaysOwns`.
- ✅ **The ingestion switch is ON** (MM PR #17, `MM_READINGS=bus`) and
  the pipe is proven: a captured reading published on the production
  JetStream reached the running engine and journalled. The `market-maker`
  NATS user carries the SR_PROBABILITIES consumer grants (nats.conf
  backed up on the VM before the edit).
- 📝 **The engine deploys by git BUNDLE over IAP scp** — the VM repo
  has no GitHub remote. supervised10 → 11 → 12 through the day; the
  per-deploy CFG bump + fresh journal rule held.

## 2026-08-11c — ✅ Edwin's ladder size profile STANDS: fattest at the touch (George, after challenge)

George read the live books' touch-heavy sizing as inverted from what he
expected ("you want the most orders at the best price... this seemed
atypical") and asked whether it was Edwin's design or an error. Review:
it is **Edwin's ASMM-1 design, implemented faithfully** (base 10,000 ×
0.72^level), and it is coherent for THIS MM's mandate — a liquidity-first,
non-profit-seeking maker whose flow is deliberately uninformed (retail +
SNT-1): size at the touch fills users near mid and earns the spread.
The inverted tree (thin at the touch, growing with depth) is the
risk-managing posture and matches empirical book shapes — a different
strategy, not a correction. **George: "let's stick with Edwin's design —
the key thing for him is two-sided liquidity, not profit-seeking."**

- ⚠ Process note, honest: the inversion was built AND merged (MM PR #19)
  on George's first message before his question landed; reverted the
  same hour (`b86ca83`), never deployed. The branch remains as a ready
  implementation if the ruling ever flips.
- 📝 Residual for the E31 round: does fattest-at-the-touch hold in LIVE,
  where a fat touch is pickoff-exposed between 500 ms updates?

---

## 2026-08-11b — ⭐ THE DWELL TABLE IS THE REPUBLISH CLOCK, every mode (George)

✅ Prompted by the cadence doc-sweep's finding: Edwin's 23-07 "non-live
re-quote every 30–60 s" was never superseded and never implemented —
non-live books only republished on a material change. George's ruling:
**every mode republishes a re-rolled book when its drawn dwell expires,
changed or not; materiality only publishes sooner.** His ranges:
**pre-game 5–20 s · post-game 5–20 s · overnight 20–40 s** (LIVE stays
0–0 on the 500 ms floor). ✂ Supersedes Edwin's ASMM-1 rows
(8–30/10–40/20–90) while implementing his 23-07 intent. Built + merged
(MM PR #18, 687 tests) and **deployed supervised11/CFG-0010**;
verified live: ~one re-roll per book per 20–30 s across the six books.

- ⭐ **C4's live half PASSED as a side effect:** JETS's LmtPerc rejects
  (the stale-18.65-ask blocker) retried 3–4× in 80 s — the backoff
  schedule, not sweep cadence. The other five books: zero rejects.
- 📝 Also proven this deploy: the pkill self-match footgun (a remote
  `pkill -f mm.runtime` kills its own SSH shell — bracket the pattern).

---

## 2026-08-11 — ⭐ THE LIVE CADENCE RULED: poll at 500 ms, NEW ORDERS every 500 ms, changed or not (George)

Two rulings in one conversation, closing our half of **E18**:

- ✅ **The in-game SR poll is 500 ms** (matching Edwin's 03-08 number).
  George: an unchanged successful fetch "is not no-data — it is
  confirmation" (the E38 principle, already built); the cadence buys
  reaction latency to the changes that DO happen. ✂ Supersedes the 2 s
  evidenced interim (SR's 4 s median gap). **Deployed** on both
  publisher pools (`MMPUB_POLL_LIVE_S=0.5`, service PR #15 — ⚠ service
  PR #14 was a mislabelled fmt-only merge, noted in #15).
- ✅ **In-game, the book publishes NEW ORDERS every 500 ms, changed or
  not** — chosen explicitly over the reaction-bound reading when both
  were put to him. Built as MM PR #16 (`feat/live-timer-quoting`,
  672 tests): tick 1.0 → 0.5 s · ✂ sweep 2.0 → 0.5 s (supersedes
  §3.1.4 — the sweep is the LIVE quote pulse) · ✂ the dwell table's
  LIVE row 3–12 s → **0–0** (Edwin's ASMM-1 row collapsed; every LIVE
  publish re-rolls the shape) · a LIVE cycle with an immaterial
  candidate still publishes once 500 ms have passed since the last
  publish. **LIVE only** — non-live states keep the §5.8 material +
  dwell gate, proven by test at the same offset.
- ✂ **R-Q03 ("the shape redraws never on the timer alone") is
  superseded for LIVE** — requirements addendum entry same day.
  **Rest-until-gone (R-L01) is deliberately untouched**: the 500 ms
  churn comes from re-rolled offsets MOVING rung prices, so orders
  genuinely cancel-replace; a same-price rung still rests.
- ⚠ **Flags carried:** the dwell collapse is book-visible → Edwin sees
  it in the E31/E17 round · at NCAA-Saturday scale (~60–80 live books)
  the ack volume makes **N31 group commit REQUIRED** · the IN-ENGINE
  poller still carries 2 s — it retires at the ingestion switch; do the
  switch (or bump it) before any live game.
- 📝 **E18 narrows to nothing on our side**: poll rate ruled, quote
  cadence ruled; what goes to Edwin is confirmation of the collapsed
  dwell and the visible-churn posture, not a question.

---

## 2026-08-10b — ⭐ THE TAKER'S ACCOUNT EXISTS (George)

✅ SNT-1 has its own account: **AccID `4963224393`**, login
`hasan.ahmed+MT@novosapien.ai` (created by Hasan; the credential is
held off-vault — never commit it). **T-I01 moves ⛔ → 🟡.**

**What it unblocks:** the shared-account hole closes — a deploy on this
account has its own `position.{userId}` stream and real per-account
sell-check semantics, so a QA run tests inventory behaviour, not just
wiring. **T-S05** (reconcile vs venue) becomes meaningful to build.

**➕ Same day, the user id RESOLVED (Zitadel lookup):** the taker's
platform user id is **`385656921832584863`**
(`hasan.ahmed+mt@novosapien.ai`, active). Cross-validated: the same
query returns `hasan.ahmed+mm@…` → `384925384799470102`, the MM's
known user id. The taker's full identity:
`SNT_USER_ID=385656921832584863` · `SNT_VENUE_ACCOUNT=4963224393` ·
position subject `position.385656921832584863`.

**Still owed before a deploy:**
- **Is this the IPLP (BD-prop) slot or a retail-class account?**
  Decides T-I02 (MPID on the tape) and the E33/T13 compliance posture.
- The credential belongs in Secret Manager at deploy time, not in env
  files in git.

---

## 2026-08-10 — ⭐ Edwin wants the taker to SHORT (George, relaying Edwin)

✅ **The requirement:** SNT-1 must be able to go short — long-only by
construction is not the end state. Recorded as intent; nothing is built
or changed yet.

✂ **Correction to the first filing of this entry (same day):** shorts
are NOT venue-gated — **the platform already shorts, live, via FIX
side 5.** Verified in code: the app maps side 5 (`venueOrders.ts`), the
gateway's NewOrderSingle sends it (`oe_adapter.go`, `SideSellShort=5`),
and the trading service charges full-notional collateral with a borrow
reserve of **1,000 shares/security on QA** (T-M06's "short reserve";
production capacity 5M/5M). The 08-09 sell rule (`sellable = Pos −
livS`, whole-order reject) governs **ordinary side-2 sells only** —
side 5 is a separate path with its own rules. The platform's model:
**flatten first, then short** — a mixed order is refused
(`SHORT_WHILE_LONG`), so long and short are exclusive states.

**What remains open before the taker shorts:**

- **T16 (Rob, narrowed)** — side-5 rules for the HOUSE/taker account:
  who backs the borrow reserve and its size per book; is
  short-while-long a VENUE reject or only a service-side check (SNT-1
  bypasses the trading service, so only venue-side checks bind it);
  margin on QA vs production.
- **E26 (Edwin, extended)** — the taker-side rules: when may it short,
  how deep (v2's float-wide short cap vs a per-bot cap), how it covers,
  and how the float/drift design (T-O08) reads once drift may go
  negative. The disclosure question (E33/T13) grows a leg: a HOUSE bot
  short against retail longs.

⚠ **Standing requirements affected, NOT yet changed:** T-O06 (side 2
only) and T-O08 (never goes short) stay as built until E26/T16 answer.
The build shape when they do: the sell gate extends — sell the long
via side 2 up to `Pos − livS`, then side 5 within the borrow cap. The
SNT runtime today maps only buy=1/sell=2.

✅ **The MM's own shorts (George, same conversation, settled after two
turns):** the market maker **CAN short, as a last-resort backstop** —
"usually never gonna happen but we're probably gonna need it." The
inventory floor (E27's opening position) makes flat rare; if it
happens, the ask ladder flips side 2 → side 5 at flat so the book
never goes one-sided. The flatten-first rule binds POSITION, not
resting orders (N34 option a + c). Edwin confirms in the E26 round.

✅ **The mechanism ruling (George, same day): never straddle zero.**
The taker clears its longs before it may short, and clears its shorts
before it may go long — no single order crosses zero, and side-5
orders never rest alongside a long or a live side-2 sell. Filed as
**T-O10** in the taker requirements. "Probably the maker as well"
(George) — but for the MM this is non-trivial: a two-sided quoter that
is FLAT must rest bids and asks at once, and a flat book's asks would
be side-5 shorts resting beside side-1 bids — strict order-level
exclusivity would forbid a flat MM from quoting asks at all. Filed as
**N34** (ours to design, with Edwin's E26 round).

---

## 2026-08-09c — the taker's hardening round: notional cap · kill switch · state lever · deploy artifacts

George: *"most of this looks like standard work… just get on with it"* —
with one carve-out: **T-S05 (reconciliation) is his to understand
before it is built.** Same branch (`feat/snt-1-float-and-sell-gate`);
628 tests, ruff + mypy-strict green. All routine calls below are OURS,
recorded here.

- ✅ **T-M03 — the per-order notional cap: $25,000, cut-not-skip.**
  Edwin named the cap but never a value; $25k halves the 400-share ×
  $127.50 worst case and a median order (~$2k) never feels it. Same
  posture as the sell gate: cut to fit, quiet below min size. 🟡 in
  parameters, ruling rides E32.
- ✅ **T-R01 — the kill switch is a NATS control subject, and it is
  JOURNALED.** `snt.control.{bot_id}`: halt stops new arrivals and
  cancels every live order at once; resume re-arms with redrawn
  schedules (no burst). Halt/resume marks replay at boot, so **a
  restart cannot silently re-arm a halted bot** — state that lives only
  in a running process dies with it (the MM's dead-man lesson).
- ✅ **T-F07's lever, not its requirement:** activity state is settable
  at runtime (`{"cmd":"state","value":"LIVE"}`), journaled, reschedules
  all arrivals on change (an OVERNIGHT draw can sit 40 min out; a
  switch to LIVE must not wait for it). **The journaled mark outranks
  the env boot default** — it is the later operator action; a fresh
  journal (new deploy) starts from env. T-F07 itself stays 🔴: nothing
  DERIVES the state from the schedule yet.
- ✅ **Deploy artifacts, no deploy:** `deploy/snt-1.service` +
  `snt-1.env.example` + `docs/SNT-RUNBOOK.md`. Operating rules inherit
  the MM's: bump `SNT_CONFIG_VERSION` + fresh journal dir per deploy,
  journal on the journal disk, **halt before stop** (a plain stop
  leaves an in-window order resting with nobody left to cancel it).
- ⭐ **The QA posture has a hole, now recorded in the runbook:** the
  venue's sell check is PER ACCOUNT, so on the shared MM account the
  taker's holding arithmetic is fiction and the MM's resting asks eat
  the taker's sellable quantity (and vice versa). **A QA run on the MM
  account is a wiring test, not an inventory test.** The clean run
  needs the IPLP account, or T-S05 first.
- 📝 **T-S05's input path exists after all:** the gateway publishes
  `position.{userId}` per symbol (size, cost basis) whenever tag 9383
  rides an execution report — found in the gateway source
  (`oe_adapter.go`, `nats_publisher.go`). The 08-09 caveat stands: 9383
  was observed not moving per fill, so whether it is a LIVE position is
  Rob's question (T15). Reconciliation gets built fail-safe against
  that unknown.

## 2026-08-09b — ⭐ SNT-1 PARTICIPATES IN THE IPO (George) — the float + the sell gate BUILT

George redirected the session: *"the market maker is already built — it's
the market taker that we need to be concerned with"*, then *"assume the
shares are not a problem… build what we can build according to the
documentation we've got, and the questions we ask after."* Branch
`feat/snt-1-float-and-sell-gate`; 620 tests green, ruff + mypy-strict
clean.

- ⭐ **THE RULING: the taker holds an IPO allocation before it trades.**
  SNT-1 participates in the IPO like any other holder, so it starts long.
  This is what makes its sells legal at all — the venue caps a sell at
  `Pos − livS` (decoded 08-09) and the taker's first sell from zero was
  always going to be rejected. No purchase, no seeding script, no
  opening trade of its own. The mechanism is unknown → **E39**.
- ✅ **The float is CONFIGURATION, not journaled state** (ours, recorded).
  `pos` keeps its meaning — net shares from own fills — and the holding
  is `float + pos`. So a journal replay can never double the float, and
  the journal schema does not change. The alternative (seed `pos` at
  boot) would have made every restart a correctness risk.
- ✅ **T-O08 needed no new inventory rule.** The soft cap and the
  disposition tilt both act on `pos`, and `pos` is drift from the float
  — so both already mean "return to the float". They flatten the drift;
  they never drain the float. ⚠ This corrects a claim I made to George
  mid-session — that the tilt would have to be switched off or it would
  sell the float away. It would not; it mean-reverts to the float.
- ✅ **The sell gate CUTS rather than skips** (ours, recorded). Over the
  bound the venue rejects the whole order, so the taker sends the
  smaller sell instead. Below the 5-share minimum there is nothing to
  cut to and the arrival passes quietly. Reasoning: order size is noise
  either way, whereas silence exactly when inventory is low would be
  informative — and T-F05 is the requirement the taker exists to protect.
- ✅ **`livS` is our own un-settled sells, counted at FULL quantity.**
  The IOC substitute leaves a marketable DAY order resting for up to
  1.5 s, so two arrivals inside that window would otherwise stack past
  the holding. A partially filled sell still counts whole, which
  over-counts — the safe direction, since the venue rejects whole.
- 📝 **Two numbers are OURS and unverified → E39:** the float size
  (**5,000/team**, 🟡 — sized so the holding wanders ~3,500–6,500
  against the 1,500 drift cap) and the float's **cost per share**
  (🔴 — unknown). While the cost is unknown the tilt keeps comparing mid
  against the VWAP of what the taker itself traded, not against the true
  cost of the holding. We did not invent a basis; which one to use is
  Edwin's call once the IPO price lands.
- ⚠ **The gate trusts our own arithmetic.** If the float is not
  verifiably on the account, the bound we compute is not the bound the
  venue applies. That is **T-S05** (reconcile, halt the book on
  divergence), still unbuilt, and it is now the taker's most valuable
  remaining item.
- 📝 **Not done, and deliberately: the MM's half.** R-Q08 (the ask
  ladder respecting `Pos − livS`) and R-Q09 (the stale-book crossing
  guard) are market-maker items and stay open. The 08-09b handover's
  build queue put R-Q09 first; George's ruling reorders it behind the
  taker.

## 2026-08-08c — T10 ANSWERED: permanent test symbols exist — real ticker + `.TEST` (Rob Colucci)

Direct from Rob (tZERO) to George, Slack, same day (venue facts, gospel).
**This closes the top item on the T-list.** Full registry, the ten symbols
and the replay games: [[market-maker/test-symbols]].

- ✅ **A test symbol is the real ticker plus a `.TEST` suffix.** Rob's own
  example: Baltimore Ravens → **`IPTCRAVE.TEST`**. Symbols go 8 → 13 chars;
  Rob asked about length, George confirmed no problem on the Novo side.
- ✅ **tZERO can track `.TEST` symbols separately and can create accounts
  that are only allowed to interact with them.** This is what makes them
  *permanent* rather than a pre-launch window — T10's "users must be
  blocked from trading them" caveat becomes a **venue-side entitlement**,
  not an app-side filter. The one-environment constraint stops biting.
- ✅ **Nothing changes on order routing** (Rob, same thread): the MPID is
  still driven by Account1 (FIX Tag 1); `Account1=1797733477` still hits
  an IPLM MPID. Restates `2026-08-07g`.
- ✅ **Ten teams requested** (George, same thread): BAL · BUF · DAL · DET ·
  GB · HOU · JAX · KC · PHI · WAS. Chosen by ONE criterion — the number of
  **Sportradar replay games playable between them**. Not brand, not market.
  A replay exercises a ticker *pair*, so a team with no in-set opponent is
  a dead symbol.
- 📝 **The selection, and the finding behind it:** Sportradar's simulation
  library is a fixed set of **102** NFL recordings, and only **46** carry
  BOTH the push `events` feed and the REST `pbp` feed. Every 2023 recording
  and 9 of 37 from 2024 have no push at all. `pbp` is not optional — push
  holds no state, so a disconnect recovers by pulling `pbp`. Exhaustive
  search over the 46 gives these ten a **17-game** matrix; an eleventh
  ticker buys only 1–2 more. All 17 live-tested 08-08: session + `pbp` 200
  + push connect, **17/17 pass**.
- ⚠ **Four of the ten four-letter codes are OURS, not tZERO's** — `LION`,
  `TEXA`, `JAGU`, `COMM` follow the observed `IPTC****` pattern but no
  source confirms them. RAVE/BILL/COWB/PACK/CHIE/EAGL are venue- or
  vault-attested. Nothing hardcodes the four until Rob returns them.
- ⚠ **The blocker that survives:** do the `.TEST` books get a `UEPR`
  reference price, or open empty? An empty book rejects everything ("No
  price available" — the `IPTCBILL` state). Same blocker as the other 163
  production books; see `LmtPerc reference` in [[market-maker/parameters]].
- 📝 For contrast, the seven already-minted symbols (EAGL · PATR · BILL ·
  GIAN · COWB · STEE · JETS) hold **one** push-capable head-to-head game
  between them. PATR, GIAN and STEE contribute zero at this set size.

## 2026-08-09 — ⭐ THE SELL RULE DECODED (live probe) · DONE_FOR_DAY never happens · the MM crosses the stale book

George: "is there a way to check the app state for my user ID… now you've
got the account ID, you can do the testing yourself." Probes run on
George's own user account (`380030896289412728` / venue account
`5120866205`, MPID IPLY) with his authorisation, alongside a research
sweep of the vendor specs.

- ⭐ **THE OVERSELL RULE — venue-verified, one message answers
  everything.** A side-2 sell for more than the sellable quantity is
  **rejected whole**. It does NOT fill up to the position and it does
  NOT open a short. The reject states the arithmetic:
  `FAILSRISK[5120866205]: You can SELL at most 50 shares of IPTCGIAN.
  Pos=100 livS=50`. So **sellable = Pos − livS**, where `livS` is the
  quantity already committed to LIVE RESTING SELLS. Control (sell 50 of
  100 held) accepted; test (sell 150 of 100 held) rejected.
- ✅ **This is a VENUE rule, not per-account config** (an earlier
  hypothesis, now retracted). The MM account's 07-08b reject —
  "You are not long IPTCBILL. There are NO shares to SELL" — is the
  same check at `Pos=0`. The negative positions seen on user accounts
  came from **side-5 (sell short) orders**, a different order type,
  behaving correctly.
- ✂ **Corrects three contradictory beliefs in the app code**
  (all pre-existing, none venue-sourced):
  `venueOrders.ts` — rejects whole + resting sells count as spoken-for
  → **CORRECT, now verified**; `OrderEntrySheet.tsx` — "the venue is
  free to fill only up to your position" → **WRONG**;
  `buying_power.py` — "undefined… could fill against inventory that is
  not the caller's" → the fear is unfounded, though its client-side
  refusal remains right behaviour.
- 📝 **SNT-1 consequence:** the sell gate is mandatory and must
  subtract LIVE RESTING SELLS, not merely compare to the position.
- ⚠ **DONE_FOR_DAY HAS NEVER HAPPENED — a recorded venue "fact" is
  wrong.** No `39=3` appears anywhere in the gateway's FIX log. Orders
  placed 08-08 00:31 survived TWO 23:59 ET boundaries and are still
  resting. This contradicts the 22-07 platform-doc adoption ("tZERO
  ends its session at 23:59 ET and every resting DAY order expires")
  and removes test **B1**'s premise. The MM's DONE_FOR_DAY state
  handling is harmless but has never fired. → new **T14**.
- ⚠ **The MM crosses the stale book on every repost — live, ongoing.**
  Its COWB bid at 76.04 was marketable against stale asks at
  54.35–55.05 and **swept all 8 levels: 920 shares, $50,366**, moving
  the position 100,930 → 101,850. The MM is TAKING liquidity while
  intending to rest passively. Cause: the venue book still carries
  third-party stale quotes far from Edwin's prices, and the engine
  prices off its own valuation, not the book. → build item.
- ⚠ **The engine ADOPTS any MM-prefixed order on its user id.** The
  gateway requires the `MM` prefix on `gateway.orders.mm.*`
  (`MM_PREFIX_REQUIRED`), but the engine's `_get_or_admit` path
  (built for restart recovery) admits an unregistered ack as ACTIVE —
  so the reconciler adopted a hand-sent probe order and cancel/replaced
  it 0.7 s later (85.00 → 76.31, 60,000 → 2,500 shares). **No manual
  probe on the MM user id is safe while the engine runs.**
- ✅ **The workaround (ours, recorded):** `gateway.orders.mm.new`
  validates only the ClOrdID PREFIX — `userId` and `account` ride in
  the payload. So a probe can use the MM transport with a different
  account's identity; its responses publish to `order.{thatUserId}.>`,
  which the engine does not subscribe to, so no adoption. This is how
  the probe ran. ⚠ Note the MM prefix makes such an order a target of
  the account-wide dead-man sweep.
- 📝 **The vendor OE spec does not document side 5 at all** — tag 54 is
  enumerated `1 = Buy, 2 = Sell` only, with no short-sale marking, no
  locate tag, and no occurrence of "short"/"borrow"/"locate". Side 5 is
  live-verified but vendor-undocumented. `OrdRejReason` (103) has no
  position-related value; the position rejects arrive as FAILSRISK text.

## 2026-08-08b — SNT-1 BUILT (George: "we start building it") — code complete, NOT deployed

MM PR #10 (merged, main `b42aa65`): Edwin's reference rebuilt
venue-hardened as `src/snt/` — own package beside `mm/`, own process,
own journal, identity all-env. 27 new tests; 609 total green.

- ✅ **Shape (autonomous, recorded):** same repo, separate package —
  process/account separation is what E33 needs, not repo separation;
  the wire contract, toolchain and deploy channel are shared and
  proven. Extractable later.
- ✅ **The IOC substitute:** marketable DAY + cancel after 1.5 s
  (tZERO has no IOC — E32). Rejects are first-class: a 5-streak
  quiets the book 60 s (interim until the reject-backoff build).
- ✅ **Restart safety:** an economic journal (fills/sends/session
  marks) replays position, basis and budget at boot; the send
  sequence resumes so a used ClOrdID is never re-minted. The RNG is
  seeded per process (config-version salt) and deliberately NOT
  persisted — replay reproduces economic state, not the future draw
  sequence (a noise bot's draws are not audit-relevant like the MM's
  quotes; noted in the code).
- ✅ **Two run postures, no code change:** QA on the MM account (the
  poker's door — self-crosses print, empty venue) vs production on
  the IPLP account when Rob assigns it. **Production stays blocked on
  E32 rulings + E33/T13 compliance** — building ≠ shipping.
- 📝 Parameters: Edwin's numbers filed 🟡 in the registry; the 8-tick
  spread gate filed 🔴 (never trades §5.2's Stable spread — E32).

## 2026-08-08 — ⭐ the double-post race found and fixed · poker v7 · the MD-view verdicts

George: "the book doesn't look like we expect — check the logs/replay,"
then "fix and deploy both," with a careful-impact review of anything
touching Hasan's service. Three causes found; two were ours, both fixed
and deployed (engine `dfa87f9`, CFG-0004, journal `supervised5`).

- ⭐ **ENGINE BUG — an in-flight replace left its destination
  unprotected (MM PR #9).** `register_replace` recorded PENDING_REPLACE
  at the OLD price only; the reconciler read the replace's destination
  as unmet during the ~250 ms in-flight window and pass 3 submitted a
  fresh order there; the venue confirmed both. Journal proof: replace
  → 77.74×5500 at 23:16:14.541, fresh submit 77.74×5500 at .598.
  **19 doubled price levels stood across the six books** (all four
  STEE ask levels 2× their draw) — real resting exposure, not optics.
  Fix: `VenueOrder.pending_price` — set on register, cleared on
  confirm/reject, carried by the checkpoint (**schema 2 → 3**), and
  counted as occupied by the reconciler. Pre-existing (supervised3's
  JETS had doubles); the trace missed it because it simulated settled
  venue states. Post-deploy: zero doubles.
- ✅ **The poker aimed at frozen prices (v7 deployed):** it read
  `q["bid"]/q["ask"]` off the message envelope — fields that do not
  exist in the quote schema — so every poke fell back to the static
  launch prices (COWB 99.7% miss; 1000-lots resting at fixed prices
  inside the spread — the fake 1-cent top). v7 aims from
  `market.book`. Post-deploy: **100% fill on all six books.**
- ✅ **market.quote's null sides are Hasan's DESIGN, not a bug** — the
  quote is a partial-update contract: null = "no change", consumers
  must merge with COALESCE; explicit `bestBidCleared`/`bestOfferCleared`
  flags mean "genuinely empty". Documented in his publisher; the Redis
  path already merges. Nothing to fix in his service; any consumer
  reading a single message naively (as poker v6 did) sees nulls.
- ⚠ **The market.book stream served a provably stale JETS book for
  ~5 min under churn** (23:09–23:14): the wire showed an ask at 45.44
  while a journal-confirmed poker bid at 45.45 rested unfilled —
  impossible on the real venue, so the published book was not the
  venue's. Not the crossed-book holdback (0 log hits). The feed is
  depth-0 snapshot-driven + a republish tick, so a stalled venue
  snapshot stream freezes the published book while republish keeps
  re-emitting it. Evidence handed to the Hasan message; his deployed
  binary (08-07 12:16Z) already carries all his 08-06 MD fixes.
- 📝 The visible ladder after both fixes: **monotone 69.7%** (5.8%
  original → 32–36% after the move-size fix alone → 69.7% now, vs the
  84% target ceiling). The remainder is the true E17 remnant — bites
  and kept generations.
- 📝 Restated for ops: every redeploy bumps `MM_CONFIG_VERSION` and
  takes a fresh journal dir until the boot-reconcile healer exists
  (dead-man sweeps while the engine is down never journal — an old
  journal replays phantom ACTIVE orders).

## 2026-08-12 — The maker and taker run live across every book — [[12-08-2026-touchdown]]

> First report of continuous operation against real books. George demonstrated
> the ops panel on the call.

- ✅ **Running 24 hours across all 180 books** (170 team companies plus the 10
  test tickers), showing **two-sided quotes on every one**. Roughly **1.2
  million orders** placed in a day between the maker and the taker. Business as
  usual cadence is slower than in-game by design.
- ✅ **Cadence for the live-game test is 500ms**, tightening toward **200ms as
  launch approaches**. George: "initially for the test we were aiming for 500
  milliseconds and then as time gets closer to launching get it down from 500 to
  200."
- ✅ **Taker cadence per market is roughly every 20 seconds.** It takes
  continuously across all markets, but any single book sees it far less often.
- ✅ **The price band rejects work as designed.** tZERO auto-rejects anything
  30% out either way, and every rejection is tracked in the journal.
- ⚠ **tZERO seeds stale resting orders at start of day.** After clearing the
  books they place resting orders at old prices. The workaround in use is to
  **walk the price up with a series of orders** (the Jets took about nine, from
  ~18 to ~40) and then let the maker churn through it. **tZERO can turn this
  off**, which is the cleaner fix and is now an ask.
- ✅ **Per-book quarantine confirmed in live operation.** A journal divergence
  on one book cancels that book's orders only; it does not stop the rest. The
  journal is the central source of truth, and divergence means halt and
  investigate.
- ✅ **Vocabulary fixed by Edwin, worth keeping consistent:** an **order** rests
  on the book; an **execution** or **trade** is when they cross. The 1.2 million
  figure is orders, not trades.

### The ops panel, and what Edwin asked for

- ✅ **Edwin gets a login to the admin panel.** Some sections are irrelevant to
  him (referral simulation, load testing); the maker, taker and market-data
  views are the point.
- ✅ **Requested additions for the taker view** (Edwin, agreed by George): not
  just its orders but its **positions**, whether it is long or short, the
  **average price** it is long or short from, and **realised and unrealised
  P&L**.
- ✅ **Manual orders for the taker** were semi-functional on the call and due
  to be finished the same day.

### An IPO requirement that is not the app's

- ⚠ **Edwin needs a desktop execution interface for the offering.** He has to
  place orders across 170 team companies, and doing that through the phone app
  means logging in and out repeatedly. He wants something he can click many
  times with a mouse. **Needed before the offering opens, with a couple of test
  orders put through first.** George: same infrastructure as the app, so the
  work is configuration rather than a new build.

## 2026-07-27 → 2026-08-07 — Touchdown block (Edwin + Troy + George) — [[27-07-2026-touchdown]] · [[31-07-2026-touchdown]] · [[03-08-2026-touchdown]] · [[07-08-2026-touchdown]]

> Four touchdowns that between them settle the **IPO market structure** the MM
> operates inside, and confirm the **valuation input chain end to end**. The
> 31-07 and 03-08 calls are effectively the MM design session that 23-07 never
> reached.

### Market structure — who holds the shares

- ✅ **Two distinct entities, two MPIDs, two wallets** (Troy, 31-07 + 03-08):
  - **InPlay Markets — the broker dealer.** Client-facing. Holds the entire
    primary issuance and posts it for sale. tZERO preloads **1,000,000 shares
    per team company** into this MPID plus effectively unlimited buying power,
    so there are no rejects. Analogous to the NYSE designated market maker
    holding shares to be sold to the public.
  - **InPlay Markets — the principal trading arm.** Non-client-facing. Runs
    **both** the maker algo and the taker algo. **One wallet, one MPID, one
    inventory, two execution styles.** Troy: "it's one firm, one company… you
    have a taker algo and you have a maker algo. It's the same inventory, it's
    just different actions in the market."
  - ✂ **Supersedes the 31-07 morning framing** of separate taker and maker
    wallets (Edwin said two, Troy corrected it on 03-08 and is configuring
    tZERO the corrected way). George had modelled it wrongly off the Friday
    call; resolved explicitly.
- ✅ **The MM never sells the primary issuance.** Edwin, 31-07, cutting George
  off: "the market maker is not going to open up and sell." The first sale is
  always the issuing company via the broker dealer. This holds the
  primary/secondary plane separation the MM has always had.

### The taker's IPO mandate

- ✅ **The taker is the largest IPO buyer of every team**, buying from the
  broker dealer during the primary window. Target **≥600,000 of the 1,000,000
  shares** per team (Edwin + Troy, 03-08).
- ✅ **Only the taker algo runs during the primary.** No passive/maker algo
  during the IPO window; maker and taker run in tandem only once secondary
  opens (Troy, 03-08).
- ✅ **Purchase pattern is randomised, not systematic** (Edwin, 31-07): Edwin
  supplies a **range of shares** and a **block of time**; the algo randomises
  both size and heartbeat inside them. Totals are ranges not exact figures —
  "it's not going to be 650,000 exact, it's going to range between 600 and
  650,000."
- ✂ **Not participation-weighted in v1.** George asked whether a heavily traded
  team should get more shares bought for liquidity; Edwin: "no, not at this for
  our first run. We're going to keep it very very simple." Rebalancing happens
  instead through **market operations once secondary opens**, deliberately as a
  further information event for users to trade on.
- ✅ **Rationale is failure avoidance, not liquidity optimisation.** With ~118
  signups, without the taker "there'll be teams that don't sell any shares
  whatsoever at an IPO. A complete failure of the IPO. We cannot have that for
  the simulation" (Edwin, 03-08).
- ✅ **Treasury holdback.** Float and public offering are two different numbers;
  a reserve is held back in treasury exactly as it would be in production.
  Modelled against a ~$75M cap (Troy). 1,000,000 issued per team for **both**
  NFL and NCAA, with the unsold remainder simply not sold (Edwin overriding the
  earlier 900k NFL / 1M NCAA split, 03-08).

### IPO windows

- ✅ **NCAA: one five-day window, all teams open at once.** NFL: two days.
- ✂ **The load-balancing algo is dropped for season 1** (Edwin, 31-07). Same
  application for both leagues, stretched over different window lengths.
  Deferred to the **NBA in October**. This closes the long-standing N6
  "load-balancing vs market-making" boundary question by removing one side of
  it for v1.

### Valuation inputs — now confirmed end to end

- ✅ **Sport Radar live probabilities contract amendment signed** (Cody + Troy,
  03-08), **no change in cost**, in the production account. The probabilities
  feed was always meant to be in the first contract. Resolves the S1 blocker.
- ✅ **The betting feed is NOT needed for this run.** It buys faster
  play-by-play only, and the gamecast already runs off the betting feeds via
  the Sport Radar live match tracker. Edwin: "we don't need anything over and
  above the gamecast and the live probability."
- ✅ **Probability is a separate poll, not in the play-by-play payload.**
  Confirmed by Cody 27-07 and re-confirmed 03-08. The play-by-play push gives
  the event ("five yards gained by the Chiefs") but never the probability
  change, so the MM polls the probabilities endpoint on its own clock.
- ✅ **Poll cadence: start at 500ms during games**, tune up or down from there
  (Edwin, 03-08). Outside games it still gets called, because the taker makes
  the market 24/7, but at a slower rate. ⚠ Note this is **finer than the 2s
  George proposed on 27-07** on API-quota grounds — quota stopped being the
  constraint once the contract was amended ("there's no limit on requests").
- ✅ **Next-game probabilities post ~15 minutes after the previous game ends**,
  and typically faster (Cody, 03-08). They are an extrapolation of the posted
  odds, so the moment the line posts, the probability can be pulled. Until
  then the prior feed value carries. Resolves S3's practical shape.
- ✅ **Reference-price formula restated and agreed** (George, 03-08):
  `RP = ((P(win now) − P(win at kickoff)) + E[remaining wins]) × $5 + off-field`.
  The in-game term is explicitly a **delta from the kickoff probability**, not
  the raw probability — this is the piece that was ambiguous on 29-07 and is
  now settled.
- ✅ **Graceful degradation is designed in, not bolted on.** If the probability
  is missing or stale, a reference price is still published from fallbacks, but
  bounded: "if it's too far from reality then it's not going to post something
  that could be destructive." Edwin's pro tip, accepted: **widen the bid/ask
  rather than cancel** when an input dies — "if I'm relying on say 20 inputs and
  one of them's down, my width of the bid ask automatically goes wide." Fills
  in N3's shape (Edwin decides policy, we implement).
- ✅ **Determinism reaffirmed** as a build property: a journal such that
  replaying the same inputs a year later reproduces the same output exactly
  (George, 03-08). Consistent with the working guide's day-one rule.

### Reference-price anchoring — Edwin's correction

- ✅ **The RP anchor is correct behaviour, not a bug.** George raised that
  because the MM provides most of the liquidity, its quotes will keep dragging
  price back to the reference price, which acts like an anchor. Edwin: "that's
  exactly how a real market works." A forced exit rips price away temporarily
  (**toxic flow**), the MM absorbs it, and the market returns toward fair value.
  "That's how every market in the world works." **No change needed.**
- ✅ **Underlying-vs-basis framing** (Edwin, 31-07): InPlay is the
  **underlying**; Kalshi and Polymarket trade **derivatives** of it, in binary
  outcome form. Real markets deviate from fair value for structural reasons
  (rates, expiries, deliverables) and InPlay's probability input is the
  aggregate of all such inputs for a team.
- ✅ **The proprietary price feed is a product.** Once live, back-test past
  seasons against actual share prices to learn which on-field and off-field
  events move fair value most. Edwin sees Kalshi, Polymarket and the
  sportsbooks licensing it — "it's not a probability feed, it's actually a
  price feed that they can translate into betting odds in real time." Recorded
  as strategy, not a v1 build item.

### Build status and Edwin's code

- ✅ **MM runs end to end** as of 03-08, on a single run: it takes the inputs
  and emits an order book. **No orders are produced yet.** Remaining work is
  connections, scheduling and deployment — "testing the connections… making
  sure if we need it to run every 200 milliseconds during a game, is it going
  to do that."
- ✅ **Edwin's Python cannot be used as-is** (George, 31-07). Components will be
  extracted — the volatility calculation named specifically — and the rest
  replaced. There is too much missing above and below it, plus the technical
  layer (200ms scheduling, cancel behaviour, state persistence). E4 closes as
  "received and assessed", not "adopted".
- ✅ **Edwin ran ~5,000 simulations per team across ~5 seasons** on the maker
  and taker (31-07). Calibration evidence, not code to lift.
- ✅ **Spread width comes from the volatility equation, not a lookup table**
  (George, 03-08) — a time-decaying volatility number feeds the width. Edwin
  did not confirm the ~20s half-life George floated; it stays 🔴.

### Dates

- ✂ **The 6 August dry run slipped.** George called it "looking unlikely" on
  31-07.
- ✅ **13 August is the new dry-run target** — a preseason game with live data,
  on TestFlight, with the InPlay team and friends and family trading it as if
  live (Troy, 31-07 + 03-08). Multiple team companies possible; several games
  that night.
- ✅ **The 13 August run is secondary trading only.** Troy: "we're not going to
  do a dry run of the IPO process… we just want to do a dry run of secondary
  trading during a game event." ⚠ **Edwin overrode the implication**: "I want
  one test run at least before" launch on the IPO too. So an IPO dry run is
  required, just not first.
- ✅ **Trading previously played games is an accepted fallback** for testing
  when no live game is available (Edwin, 31-07), alongside the SR simulation
  games already agreed 23-07.

## 2026-08-07h — ✂ the move pass adopts the fresh drawn size (George's ruling, BUILT + MERGED)

The ladder-shape trace's fix, ruled by George on the 07-08 findings
("the book shows no profile") and built next session as directed
(MM PR #8, merged — main `e0f2e45`):

- ✂ **Supersedes N10's "carries the remainder" wording for MOVES
  only.** A price move is still ONE cancel/replace (35=G), but the
  replace now sends `CumQty + level.quantity` — the moved order
  ADOPTS THE SIZE DRAWN FOR ITS NEW RANK — instead of
  `CumQty + LeavesQty` (the old remainder). The gateway's
  `quantity > CumQty` guard still holds by construction (a drawn
  level is ≥ 1; in practice ≥ 1,000 after round500).
- ✅ **Rest-until-gone for KEPT orders is unchanged** — a still-wanted
  price is never topped up. The E17 lifecycle question stays open;
  this narrows it to the kept-order generations, and Edwin sees the
  whole thing in the round (E17/E31).
- 📝 Why: the trace measured 95.7% of instructions carrying stale
  sizes under remainder-carry (a one-tick drift teleports the order
  falling off one end to the other end at its old size); the visible
  ladder was monotone 5.8% vs the target's 84%. Proven by test: the
  rotation fixtures (drift up/down) now assert a single replace at
  the new rank's draw, ladder non-increasing.

## 2026-08-07g — tZERO's MPID scheme lands (Rob Colucci): IPLM is the MM's tape identity

Direct from Rob (tZERO) to George, same day (venue facts, gospel):

- ✅ **SIM placeholder MPIDs:** **IPLM** = the MM account (1797733477)
  · **IPLP** = a future BD PROP account (assigned when it onboards —
  the SNT-1 / second-house-account slot, E33/T13's subject) · **IPLY**
  = retail (challenger) accounts, assigned at onboarding.
- ✅ **The MPID is DRIVEN BY Account1 (FIX Tag 1)** — "when we receive
  Account1=1797733477 it is hitting an IPLM MPID." Nothing changes on
  our side: the 06-08d fix already puts the account on every order,
  and we never send an MPID ourselves (tag 9251 is UAAR-side,
  add-only, not ours).
- 📝 Consequences worth carrying: the MM's prints and quotes are now
  ATTRIBUTABLE on the tape as IPLM vs IPLY retail flow — feeds the
  §5.5 public-book checks (ours-vs-others) and makes E33's house
  prints labelled house prints. When SNT-1's account onboards, telling
  Rob to cut IPLP over is the trigger to settle T13's cross-account
  wash question. George asked Rob whether MPID assignment interacts
  with the wash/self-trade settings or is purely the per-account 8985
  flags — answer pending.

## 2026-08-07f — ⭐ ALL SIX BOOKS LIVE, TWO-SIDED, AT EDWIN'S PRICES — after two more venue lessons

The continuous supervised run stands (engine `9ac909d`, CFG-0002,
journal `/var/lib/mm/supervised3`): EAGL 77.76/77.82 · PATR
79.76/79.82 · GIAN 61.08/61.13 · COWB 76.16/76.20 · STEE 66.32/66.36 ·
JETS 45.41/45.45 — every spread straddling its sheet price, 8–17k
shares per level. A 60-minute poker loop trades small clips against
our own inside so the books visibly update (George's ask).

**Two more real-venue lessons on the way, both fixed and merged:**
- ⭐ **A real fill event arrived with NO ids in its payload** — the
  gateway's local-publish quirk (recorded 02-08 for acks) proven on a
  fill — and the adapter's KeyError KILLED the engine; the dead-man
  swept the book (correctly — including the walk's anchors, which are
  MM-namespace orders). **Fix (PR #6):** fills use the subject
  fallback like acks; the venue drain gets the readings consumer's
  POISON rule — an untranslatable message is counted and skipped
  loudly; deliberate halts (busts, unmapped fills) stay fatal.
- ⭐ **The duplicate-id deadlock (PR #7):** ClOrdIDs mint
  deterministically over the config version; tZERO remembers ids per
  session; a redeploy on a WIPED journal re-mints the same ids → every
  order duplicate-rejects, and with no material change the reconciler
  resubmits the same ids forever. **Never wipe the journal against a
  session that remembers.** Fix: `MM_CONFIG_VERSION` env (§12.1's
  versioned configuration at run scale) — a new version re-mints every
  id (disjointness proven by test). This run is CFG-0002.
- 📝 The LmtPerc reference-refresh delay healed 4 of 6 books unaided
  (the reconciler's per-cycle retry IS an anchor-retry); the reject
  churn while waiting is the same backoff gap recorded 07-08d — the
  reject-backoff build item now covers three observed shapes:
  LmtPerc rejects, duplicate-id rejects, and empty-reference rejects.

## 2026-08-07e — ⭐ the book walk: LmtPerc DECODED, the stale quotes eaten, the books moved to Edwin's prices

George: "get the prices on the books, set the references to something
realistic, and run the engine so I can watch the book update live."
Executed as a scripted walk from the MM VM (real orders, MM account).

- ⭐ **LmtPerc decoded from full reject texts:** aggressive orders may
  cross at most **3%** through the opposite best (5% seen on STEE —
  per-symbol bands exist); passive orders must sit within **90%** of
  their own side's best. And the reference is **NOT the live book** —
  it is a SNAPSHOT that refreshes on a delay (minutes): we ate PATR's
  entire bid side and the check still said `BID(112.20)`; a COWB bid
  rejected against `ASK(53.90)` was ACCEPTED minutes later once the
  reference caught up. **Walk fast, anchor slow.**
- ✅ **The stale test quotes are GONE — eaten at their own prices**
  (aggressive-at-best = 0% through, always legal): all stale bids on
  the down-books (EAGL 8 levels/1,160 sh · PATR 9/1,170 · GIAN
  6/780 — sold from our seeded inventory) and all stale asks on the
  up-books (COWB 9/930 · STEE 8/800 · JETS 8/760 — bought, fake
  cash). The stale-order owner's account received the fills.
  ⚠ These are TRADES, not transfers — they are NOT in any MM journal
  (no engine was listening); position truth is Tag 9383 at next
  execution. Residue: EAGL/PATR/GIAN kept their stale ASKS (146+/
  112.95+/68.5+ — deep out of the money above Edwin's price,
  unreachable now by the 3% rule; harmless ghosts, noted).
- ✅ **Anchors at Edwin's prices** (10-share own orders, DAY): posted
  where the frozen reference allowed; the rest retried by a finisher
  script as the reference refreshes. JETS needs the recorded two-hop
  rung chain (the 90% passive band vs its ~18 reference).
- 📝 The never-empty rule held throughout — no book was left without a
  resting side (BILL's "No price available" state is the disease this
  avoids).

## 2026-08-07d — ⭐ FIRST RUN ON THE REAL VENUE: the machine quotes, the dead-man cleans up — and LmtPerc reveals a reject loop

The supervised test ran (George's go): `python -m mm.runtime` on the MM
VM, MM_MODE=supervised, 6 priced books (BILL parked), real identity,
production NATS, loopback confirmed OFF. Before the run: **the 7 books
were seeded ourselves** — 100,000/ticker via position-transfer, all
UPTa, basis at Edwin's prices, ledger in
`reference/position-transfer-ledger.md`; a side-2 sell then ACCEPTED
(yesterday's "not long" reject gone).

**What worked — the machine's first real-venue milestones:**
- 50 instructions stood for 6 securities; 64 orders ACCEPTED and
  RESTED — our bids visible on the venue book at $77.78/$77.76
  (IPTCEAGL), Edwin-priced, next to the stale $145 test quotes.
- 665 heartbeats at ~250 ms; the full boot/identity/account chain
  clean; no quarantine; journal + checkpoints on /var/lib/mm.
- ⭐ **The dead-man drill, live:** SIGTERM → beats stop → the gateway
  fired at +4 s and swept all 33 resting orders (`reason=deadman`).
  The venue book is clean. Exactly the designed cleanup.

**⭐ THE FINDING — a reject loop, two defects exposed at once:**
- **Venue reality:** the books carry STALE test quotes (EAGL ~$145,
  ~2× Edwin's $77.79; 110–180 sh/level), and LmtPerc measures
  aggressiveness against that reference — so every order of ours that
  would CROSS the stale book rejects as "Aggressive BUY/SELL LmtPrx".
  1,511 rejects vs 64 accepts. The passive side rested fine.
- **OURS, a real design gap: the reconciler has NO reject backoff.**
  A persistently-rejected level is re-wanted by every cycle and
  re-submitted at sweep cadence — ~16 msg/s of reject churn,
  indefinitely. Live-mode versions of this exist (venue bands, halts),
  so this is a REQUIRED pre-season fix, not test noise. Design note:
  rejects arrive as journalled order events, so a deterministic
  backoff keyed on them is replay-safe.
- The LmtPerc question for Hasan is now TWO-sided and sharper:
  (a) empty books reject everything ("No price available");
  (b) stale-referenced books reject fair-priced orders as aggressive.
  Ask: what sets the reference, the band width, per-account
  configurability — and clear the old test quotes off the 7 books
  (another user's orders; not ours to cancel).

**State after the run:** positions unchanged (nothing traded — the
"totalVolumeTraded 300" on the book snapshot was yesterday's probes,
cumulative), the account still holds the 700k seeded shares, no resting
orders. Supervised journal preserved at /var/lib/mm/supervised.

## 2026-08-07c — Hasan's trading-ops guide lands: we can seed OURSELVES · the LmtPerc mystery thins

Hasan's "Driving the Trading Stack with Claude Code" (07-08,
live-verified same day) — filed verbatim:
`reference/claude-trading-ops-guide-hasan-2026-08-07.md`. Gateway/venue
facts are gospel (22-07 filter). What it changes:

- ⭐ **The seeding dependency on Hasan DISSOLVES.** `POST
  /position-transfer` (35=UPT) is on the gateway VM's own HTTP server,
  reachable by IAP SSH — the same access we already use. Rules
  restated: `txfrQty` signed delta · `txfrCost` = TOTAL cost (not
  price), same sign, avg > 0 · replies `UPTa`/`UPTx` land in the
  journal, the 202 is only "sent" · **one-way** (negatives accepted
  then ignored) · **not idempotent** (a retry double-seeds) → keep a
  ClOrdID ledger (auto-ids prefix `T`). ⚠ `confirmTyp` is NOT a
  two-step commit — 1-then-2 produced TWO transfers (proven 05-08).
- ⭐ **The IPTCBILL "price" is a GHOST — a Redis quote is never
  cleared.** The guide states it exactly: a quote is only overwritten,
  never removed; when a venue snapshot comes back empty the gateway
  publishes nothing, so a dead symbol keeps its last price forever.
  BILL's $89.17 bid is stamped **2026-07-24** against an EMPTY venue
  book. So the panel's price and the venue's LmtPerc reference are
  DIFFERENT facts — the venue-side reference question for Hasan
  stands, but "check the timestamp" is now a rule for reading any
  quote.
- ✅ **UEAR (buying power / risk limits) is ours to drive too** — same
  SSH door. maxOrdRate default 100/s (⚠ the guide's own note: ~17×
  under MM full-ladder need — the 5,000 in Hasan's build guide was the
  MM namespace's configured value, not the IPLY default). UEPR stays
  dead (entitlement per MsgType).
- ✅ **Cancel/replace for non-app orders goes over NATS**
  (`gateway.orders.cancel` — a NEW clOrdId per cancel, orig in
  `origClOrdId`); the app path is ownership-gated. The admin proxy has
  no cancel route (Hasan's own "worth adding").
- ⚠ **Check the loopback toggle before trusting any order was
  simulated** (`GET /gateway/loopback`) — the OE session points at the
  live venue. Yesterday's probes filled for real (consistent with our
  record).
- 📝 Operational doors now in the record: the admin proxy (Cloud Run +
  bearer key from Secret Manager) for market data / orders / logs; SSH
  for buying power, transfers, raw journal. No secret values in docs —
  fetch at use, always.

## 2026-08-07b — ⭐ the probe run: wash-off VERIFIED · two new venue facts (gospel)

George: fire the MM-account probes now ("nobody's using production").
Run from the MM VM over production NATS with the `market-maker`
credential, real orders on the real gateway, account 1797733477.

- ⭐ **Wash-trade blocking OFF is VERIFIED for the MM account,
  behaviourally.** On IPTCEAGL: our BUY 100 @ 145.50 rested top of
  book (below the 146.00 ask — untouchable by construction), our SELL
  SHORT 100 @ 145.50 matched it — **both sides EXECUTED**. A
  self-cross PRINTS (it does not rest), which makes E33's compliance
  optics concrete: house self-prints on the tape. Net position flat;
  cancels correctly NOT_CANCELABLE after the fills. The user-account
  half (blocking ON) still needs Hasan's pilot accounts.
- ⭐ **NEW VENUE FACT 1 — side-2 sells require inventory.**
  `FAILSRISK[1797733477]: You are not long IPTCBILL. There are NO
  shares to SELL.` From a flat book, every side-2 ask REJECTS. Side 5
  (sell short) IS accepted from flat (proven — the EAGL short filled).
  ⚠ **Design-relevant: our transport sends side 2 for ALL sells**
  (`[side-codes]`: "the MM never sends 5 — E26"). On the real venue
  the entire ask side of a flat book would reject. The fork:
  (a) asks go side 5 from flat (stock-loan fee — economics, Edwin) or
  (b) seed inventory FIRST via E27's position-transfer, then side 2.
  **E26 + E27 are now launch-blocking mechanics, not product
  questions. Decide before the supervised run posts asks.**
- ⭐ **NEW VENUE FACT 2 — `LmtPerc: No price available` rejects orders
  on books without a reference price.** IPTCBILL (bid-only, no
  trades?) rejected a plain BUY on this risk check. 164 of our 170
  books are EMPTY — if a virgin book cannot take a first order, the
  MM cannot stand its book. → Ask Hasan: what feeds LmtPerc's
  reference (last trade? close? a settable per-symbol reference), how
  the first order lands on an empty symbol, and whether the check is
  configurable per account. **Blocking for everything beyond the 7
  populated tickers.**
- 📝 A real print now exists on IPTCEAGL at 145.50 (our self-trade,
  100 sh). Deliberate, George-directed, on the nobody-uses-it venue.

## 2026-08-07 — ⭐ the wash-trade conflict RESOLVES: blocking OFF for the MM account (unverified)

Hasan's side set wash-trade blocking PER ACCOUNT via 35=UEAR, 10/10
accepted: **MM account 1797733477 → 8985=0, blocking OFF · the 9 pilot
user accounts → 8985=1, blocking ON.** Only `account` and
`stopWashTrades` were sent — cash/DTBP/order-rate untouched; the MM
account sits outside INPLAY_VENUE_PLACE_SUBS, no overlap.

- ✅ **CONFLICT 1 from the 06-08c intake resolves in the flag-off
  direction.** N12's post-first re-quote design STANDS unchanged — no
  reconciler change needed. The user-account posture (blocking ON)
  matches the 23-07 rulebook line: users must not wash-trade.
- ⚠ **UNVERIFIED, stated plainly by Hasan's side:** UEARa means the
  message was ACCEPTED, not that the flag took effect — UEARa echoes
  only ClOrdID and Account, and no REST view exposes risk fields. The
  only proof is behavioural: rest an order on a user account, try to
  cross it from the same account (expect reject), then confirm the MM
  account still self-crosses. Offered by Hasan's side on request.
  **Do not treat as verified until that test runs.**
- ⚠ **New consequence, eyes open: with blocking OFF, the MM's
  momentary self-crosses can now EXECUTE as self-fills, not just
  rest.** Post-first on a price move can lift our own resting ask; the
  fill prints on the tape and the engine consumes both sides (net
  position unchanged, the spread paid to ourselves). Functionally
  handled; the COMPLIANCE optics of house self-prints on a
  FINRA-regulated ATS are exactly **E33** — keep it live with
  Troy/legal. The behavioural test will also show whether a self-cross
  executes or rests.
- 📝 T13's venue half is answered by mechanism (per-account
  `stopWashTrades` exists and is settable); the MM↔SNT-1 cross-account
  question inside T13 remains open — blocking is per-account
  self-cross, and whether tZERO relates two house accounts is untested.
- ✅ **Expected wins: Edwin's doc is the source for now (George,
  07-08).** The SR-sourcing question (SR futures carries NFL win
  totals — S10's on-file fallback — but not NCAA) is DEFERRED — ask
  later, alongside the Edwin round. Confirms the 28-07 design: Edwin
  publishes all 170; the engine's seam (the daily file /
  `ingest_reference_numbers`) makes any later source swap an upstream
  change only. Today's interim delivery is hand-carried: Edwin's IPO
  sheet → the reviewed supervised-inputs file, prices verified to the
  cent.

## 2026-08-06d — the wire-contract fixes, the quarantine, §10.3 checkpoints BUILT

Build session (MM `21dd7e1` → `43ba08d`, **534 → 561 tests**, ruff +
mypy strict clean, all commits LOCAL). The 06-08c intake's fixes and
the recorded checkpoint design, executed. Full narrative:
`sessions/2026-08-06-d-wire-fixes-quarantine-checkpoints.md`.

- ✅ **The four wire-contract fixes landed** exactly as designed 06-08c:
  `account` (FIX Tag 1) on every new order (cancel/replace carry no
  account field in the gateway's structs — verified in its source) ·
  identity rides env through `compose.Settings` (`MM_USER_ID` ·
  `MM_BOT_ID` · `MM_VENUE_ACCOUNT`; `mm_user_id`/`mm_bot_id` LEFT the
  dictionary; the reply subject follows the env user id) ·
  `venue_price_cap` $127.50 in the dictionary with the ladder ceiling
  floored at min(MEV, cap) — healthy MEV already sits at or under the
  cap, so the min() binds only on a WRONG input, where a capped ladder
  beats a stream of venue rejects · the heartbeat is `run()`'s own
  ~250 ms task; a dead beat task stops the run loudly. ⚠ Recorded
  honestly in `[beat-task]`: asyncio does not preempt — a synchronously
  blocking tick still starves the beat; that is what the N15 VM jitter
  measurement watches before the 4 s window tightens.
- ⭐ **NEW requirement (George): markets are independently failable.**
  One security's engine fault must not cost the other 169 books. Built
  as the per-security QUARANTINE at the orchestrator's cycle boundary:
  the faulted security's outcome becomes `BookSuspended("quarantined:
  …")` — the existing suspension sweep cancels its resting book — and
  its engines are never re-run. Deliberate boundaries BOTH ways
  (ours, tagged `[quarantine]`): event ingestion and the transport stay
  FATAL — a wire fault must kill the process so the dead-man sweeps.
  Replay-safe with no new event type (engines are pure functions of the
  event stream; proven by test). The log line shouts `QUARANTINED=n`.
- ✅ **§10.3 checkpoints BUILT to the recorded five-step design, and the
  deliverable PASSES:** on the real captured game, checkpoint-resume ≡
  never-stopped ≡ full-replay, byte-identical across all engines.
  Boot restores the newest valid checkpoint (schema, config and
  SHA-256 guards; rejects printed loudly) and replays only the journal
  tail; no valid file → full replay. Writer hourly at a tick boundary,
  local disk beside the journal, keep last 3.
  ⚠ **The proof caught a real gap mid-build:** tail replay must RE-ARM
  the acceptor's gate (sequence + seen keys) or a redelivered tail
  event after a checkpoint boot would be accepted twice. Fixed;
  the catch is exactly why the equality proof is the deliverable.
- ✅ **Dedup retention built:** seen keys prune on the accepted-time
  high-water mark past the one-week JetStream redelivery bound —
  §12.3's `event_idempotency_retention_s` slot is FILLED by the
  recorded 06-08c design (604,800 s), superseding the empty-slot
  posture. Duplicates deliberately never refresh a key's age (replay
  never sees duplicate lines — a refresh would fork live from replay).
  Checkpoint schema bumped to 2.
- 📝 The stale `[governor]` note in `compose.py` caught up with T2
  (50 → 5,000 msg/s); `parameters.md` rows 175–178 corrected the same
  day (the 06-08c supersession had not reached them).

## 2026-08-06c — ⭐ Hasan's build guide lands: T1/T2 ANSWERED, two design conflicts surfaced

George delivered Hasan's "Market Maker Bot — Build Guide" (05-08,
live-verified on the venue that day) plus the MM platform account's
credentials (stored locally, never in git). Filed verbatim:
`reference/mm-build-guide-hasan-2026-08-05.md` — venue/gateway facts are
gospel (22-07 filter); its bot-design suggestions are suggestions.
Also created this day: the MM VM (`infra-changes-2026-08-06-mm-vm.md`).

- ⭐ **T1 ANSWERED — the MM venue account EXISTS and is configured.**
  tZERO account **1797733477**: $1bn cash, $1bn day-trading buying
  power, position 0 everywhere, Agency capacity, uncapped open orders.
  Every order carries `account` (FIX Tag 1). The account 404s on
  tZERO's REST API (creation artifact, harmless — OMS-side everything
  works). ⚠ The buying-power check charges ~4.8 % over notional.
- ⭐ **T2 ANSWERED — the real rate limits:** gateway MM governor
  **5,000 msg/s (burst 2,000)** · tZERO `MaxOrdRate` **5,000/s** ·
  `MaxDupOrdRate` **200/s** (raised from the 20/s default for ladder
  churn). ✂ **Supersedes the recorded "50 msg/s placeholder"**
  everywhere it appears (parameters, build pages, `compose.py`'s
  [governor] note — the rig-drill caution stands only for old configs).
  The governor still REJECTS, never queues.
- ⚠ **CONFLICT 1 — wash-trade blocking vs N12 (design-changing).**
  tZERO's Stop Wash Trades is ON and REJECTS orders that cross our own
  resting orders. N12 (23-07) built the reconciler post-first with a
  momentary self-cross tolerated. **Incompatible as configured** —
  either the flag turns off (T13's conversation) or the re-quote path
  waits for cancels. Hasan says decide BEFORE finalising the diff
  engine. → Decide with Hasan/Troy; the reconciler has a change coming
  either way.
- ⚠ **CONFLICT 2 — the heartbeat is tick-tied; the guide wants it
  independent.** The gateway expects a beat ~every 200 ms and sweeps
  after 4 s of silence (latching; boot grace 30 s; arms only when it
  has something to protect). Our beat rides the 1 s tick INSIDE the
  loop — a tick that blocks 4 s (checkpoint write, GC, slow drain)
  would cost the whole book. → Move the beat to an independent task at
  ~200 ms (N15's number lands: window 4 s confirmed).
- ⚠ **NEW ASK for Hasan — NATS permissions for the readings path.**
  Since 05-08 every NATS user has its own scoped credential. The
  `market-maker` user may publish `gateway.orders.mm.>` and subscribe
  `order.> position.> market.> _INBOX.>` — **`sr.probabilities.>` is
  not in the list, and JetStream consumer API calls are not either.**
  The MM consumer and the sportradar publisher both need grants (or
  their own users). Without this the ingestion path cannot run on the
  real bus.
- ✅ **E27's venue mechanism is real:** inventory seeds via HTTP
  `POST 10.0.1.2:8080/position-transfer` — **one-way** (negatives
  accepted then silently ignored), **not idempotent** (each call is a
  delta), **no read-back** (position visible only via Tag 9383 on an
  execution report). Hasan's rule adopted: build a transfer LEDGER
  before seeding at scale. Who computes the allocation numbers is
  still E27's open half.
- ✅ **New venue facts:** 170 symbols exist (6 quoted two-sided in QA,
  164 empty — our resting orders ARE the book) · tick $0.01 · price
  cap/floor **$127.50 / 1 tick** (client sheet → parameters) · TIF
  DAY today, GTC pending, IOC/FOK unavailable · `market.snapshot/
  quote/trade/status.{symbol}` subjects exist (the §5.5 book feed's
  transport is appearing) · shorts are side 5 with a stock-loan fee ·
  venue price bands UNRECONCILED — the self-collar is ours (§5.4/MEV
  already built).
- ✅ **The wire contract is confirmed** against our build: MM prefix,
  ≤20 chars, no leading zeros, fresh id per cancel/replace — our
  minting complies. `userId` keys the reply subject; the real value
  replaces the wire test's `mm1` at composition time.
- 📝 The platform's RP/MOC/MOP streams still have no producers — our
  engine computes RP internally; nothing changes.

## 2026-08-06b — the MM-side consumer BUILT and DRILLED · ⭐ every fetch publishes

Build session, step-approved (MM `6a4904f` → `f4d3eac`, **512 → 534
tests**; service `0b936c8`, **575 → 577**; all LOCAL). Full narrative:
`sessions/2026-08-06-b-mm-consumer-built-drilled.md`.

- ⭐ **Every successful fetch publishes (George).** The publisher had a
  watermark (send only NEW readings) — which silently strips the "the
  source answered just now" signal and re-creates the quiet-is-not-dead
  halftime trap at the transport layer, and lets a final whose status
  flips after the last probability move never reach the MM at all. Now a
  fetch that finds nothing new re-offers the NEWEST reading under a
  fresh `Fetched-At`: the body is a §7.3 quiet duplicate, the header
  advances the observation age, and the re-offer's current status +
  scores close the finals gap and carry the post-game correction watch
  onto the wire path. **`Nats-Msg-Id` =
  `{game_id}:{last_updated}:{fetched_at}`** (George's composition): one
  publish ATTEMPT's identity — JetStream dedups client retries, never a
  deliberate re-offer.
- ✅ **The in-engine poller retires only AT GO-LIVE (George).** Nothing
  deleted now; the live composition switches to the bus when we push
  live. Loopback keeps the poller for the heartbeat.
- ✅ **The consumer half is built and proven end to end** on the local
  docker containers (`mm-nats` recreated with `-js`): adapter parity
  (1,089/1,089 file-vs-wire envelope equality, wire re-delivery of
  journalled history = all DUPLICATE) · finals minted MM-side on the
  poller's exact key basis (N16) · durable JetStream consumption with
  acks batched AFTER the tick (pop → journal → ack) · catch-up of
  pre-boot readings · a mid-run re-offer observed advancing the sweep's
  `observations` stamp while landing duplicate · restart with ZERO
  redelivery (135 events replayed from the journal instead).
- ✅ Ours, tagged in code: structural parity (both paths feed one
  envelope constructor — `_reading_envelope`, `result_envelope`) · the
  poison rule (a malformed message is acked away and counted, never
  redelivered forever) · durable `mm-engine`, deliver-all on first
  bind · both ends ENSURE the stream with one literal config (boot
  order free; drifted contract = loud boot failure) · the observation
  stamp is taken from `receive_time` BEFORE the accept verdict · the
  loopback team map is the real `TEAM_BINDINGS` now (synthetic `lb:*`
  retired) · `MM_SECURITIES` selects a drill's exact books.

## 2026-08-05c — all 170 bindings verified · ⭐ George's ingestion ruling

Build then live review (`06d6853` · `df6ae5b` · `46af364`, **500 → 512
tests**, commits deliberately LOCAL — George: do not push). Full
narrative: `sessions/2026-08-05-b-live-source-bindings-ingestion-ruling.md`.

- ⭐ **George's ingestion ruling: the sportradar SERVICE polls SR and
  publishes readings on NATS. The MM consumes the bus and never calls
  SR itself. The in-engine pull path must not go live.** This is the
  24-07 ingestion decision re-asserted (*"a dedicated MM poller at the
  edge… write-through push… the hot path never calls SR"*) — ⚠ **the
  build had DRIFTED from it** (01-08 poller, 04/05-08 runtime, today's
  HTTP source all absorbed polling into the engine), and stop-condition
  #2 never fired. George caught it in review. The seam contains the
  cost: `HttpSource` + the failure contract transplant to the service;
  valuation, quoting, journal, replay and the E38 liveness rules are
  untouched (the fetch stamp fits the message key on the push path —
  his design, recorded 05-08). **Process: the move is scoped in writing
  and approved before any build; before touching the sportradar
  service — git pull, verify local state, branch off `dev`.**
- ✅ **All 170 sr-id bindings verified and in code**
  (`mm/bindings.py::TEAM_BINDINGS`, validated at import). 163 exact
  schedule-name matches (14 trial-key calls, raws saved, `--from-raw`
  re-derives free) · 6 variants profile-confirmed on the core key
  (Texas A&M · Marshall · Middle Tennessee State · Sam Houston State ·
  UMass · Delaware) · the **LA Rams** via the NFL league uuid through
  the AF mappings bridge → **`sr:competitor:4387`**, profile-confirmed.
  **The bindings live-gate CLOSED; the ingestion-move gate replaced it.**
- ✅ **The seam's failure contract (ours):** `SourceUnavailable`, one
  exception for every cause — E38 needs exactly one fact, "did the
  source answer just now?". A failed fetch is skipped, never fatal,
  never a hot retry; `games_polled` means fetched successfully (it
  feeds the `observations` map). `source_fetch_timeout_s` = 1.5 s
  (Ch 12). Both transplant with the poller in the move.
- ⚠ **Serial fetches have a ceiling** (~35 live games outrun the tick) —
  noted in code; the move plus the S7 live-bulk endpoint is the answer.

## 2026-08-05b — tiers, the universe, the composition: the machine RUNS

Second half of the 04/05-08 stretch (`cf2bc10` · `7ac6787` · `0bd7f6f` ·
`db19e93` · `01b16c7`), **481 → 500 tests**. Full narrative:
`sessions/2026-08-05-composition-built-machine-runs.md`.

- ✅ **The slow poll tiers are George's numbers ("to be safe"):**
  OVERNIGHT **30 min** · POST_GAME **10 min through the 1 h window, then
  never**. The post-game watch re-offers the final each poll — identical
  is a quiet duplicate, a CHANGED score is a loud **CONFLICT** (§3.1.3
  wants a human, not an overwrite). The overnight tier doubles as the
  **N24 experiment**. PRE_KICKOFF stays **15 s, interim** — George has
  not picked from his 10–30 range.
- ✅ **The tier decision lives in the POLLER, from poller-local facts**
  (ours, recorded): the orchestrator's activity axis needs readings to
  know a game is live, which is circular for scheduling. The two
  derivations stay independent. `ensure_game` now carries the kickoff
  discovery always fetched, and a re-stamped kickoff reschedules at once.
- ✅ **The 170-security universe is tZERO's own ticker list, stored AS
  CODE** (`mm/universe.py`), validated at import against §2.5, refusing
  any hole. **The ticker IS the security id** — one name, no second
  namespace; the symbol map became identity. Floats via Ch 12 (900k
  NFL / 1M NCAA, v2 gospel). Four FCS programs sit inside the 138.
- ✅ **The composition** (`compose.py` + `__main__.py`,
  `python -m mm.runtime`): boot order promoted from the wire test —
  connect → beat → build → replay → stand the book → tick. **Live mode
  REFUSES to start and names its gates** (S1/S7 · sr-id bindings · N19):
  synthetic prices must never reach a real venue, so the gate is a
  raise, not a warning.
- ✅ **The drill passed both halves on the revived rig** — cold boot and
  restart-from-journal. ⚠ The restart **demonstrated the boot-reconcile
  gap live**: three dead-man-swept levels survived in the replayed
  record because their sweep events published into our absence. Parked
  with eyes open (the §3.1.4 healer + an ICD snapshot are the fixes;
  George: "we think about that more").
- ✂ **Defect fixed, spec-relevant:** `ingest_reference_numbers` never
  folded its record into the last-RP map, so **Edwin's daily step
  reached the book one event late** — a [no-smoothing] violation. The
  test now proves the ladder straddles the new price.
- ⭐ **George, end of session: the TRIAL KEY covers the build.** The live
  HTTP source and the sr-id bindings capture proceed WITHOUT waiting for
  S7 — one careful capture pass, not a loop (the trial quota was
  half-used in July). **T1 goes to Hasan directly**, carrying N30 and
  the 50 msg/s governor in the same conversation.
- 📝 Edwin's file: the 28-07 **structure is built** (field-for-field in
  `adapters/reference_feed.py`); only the delivery and his confirmation
  of that schema remain open (N19).

## 2026-08-05 — a quiet game is not a dead feed: the observation-age deviation

Built across 04/05-08 (`de33ebb` · `6a79c9f` · `48b648d`), corrected
twice by George before it settled. **The final rule, stated once:**

> **A successful fetch confirms the number. Only silence from the source
> suspends the book.** §3.3.1's live bands (5/10/20 s, values untouched,
> Edwin's) run on **OBSERVATION age** — time since our last successful
> fetch — wherever the liveness signal exists. Fetches landing every
> ~2 s → CURRENT, full status, full confidence, **through halftime and
> every stoppage**. Fetches silent 20 s → Invalid → suspend.

- ⭐ **The measurement that forced it** (real Chiefs–Ravens timeline,
  1,089 readings): SR sends **no heartbeat** — `last_updated` advances
  only when the number MOVES (98 % of entries change it). Gaps: median
  4 s · mean 16.3 s · p90 28 s · **max 2,862 s = halftime**. §3.3.1 as
  written suspends every book for all of halftime and on ~1 update in 6
  of a healthy game. Reading age cannot distinguish quiet from dead.
- ✂ **Supersedes the first cut recorded 04-08** ("old reading from a live
  source → Degraded"). George: a confirmed number is not a weaker form of
  fresh — the source is actively serving "the probability is still X",
  our copy matches it with zero lag, there is nothing to discount.
  **CURRENT, not Degraded.**
- ✅ **The plumbing: feed health rides the SWEEP** (`observations` map,
  game → last successful fetch time, journalled → replay reproduces the
  same suspensions). It cannot ride the probability key on the pull
  path: the poller re-fetches the whole timeline every ~2 s and §7.3
  dedup is what discards the 1,088 known readings — a fetch-time key
  component would re-mint the game's whole history every poll, and a
  fetch-time in the payload alone would CONFLICT-alarm every 2 s. ⚠ On
  the future SR-service push path the fetch stamp CAN live in the
  message key (one stamp per publish; redeliveries share it) — George's
  design, in its right home.
- ✅ **The liveness window = 20 s** (ours, Ch 12 `source_liveness_window_s`),
  deliberately §3.3.1's Invalid bound: "no successful observation for
  20 s" suspends on exactly the spec's timing, applied to the right fact.
- ⚠ **Deliberate residues:** pregame stays on reading age (no polling
  outside the pre-kickoff window → a frozen stamp would mis-suspend a
  healthy overnight book) · no-observation-ever → the spec's rule
  unchanged (nothing regresses before the producer runs live) · the
  Invalid+confirmed-live→Degraded rescue stays as a backstop only.
- 📅 **Edwin's half is E38:** confirm quote-through-halftime is the
  product he wants, and the 5/10/20 band values, measurement attached.
- Code markers: `[quiet-is-not-dead]` `[invalid-cost]` (freshness) ·
  `[liveness]` `[observation-age]` (orchestrator) · `[observations]`
  (runtime).

## 2026-08-04c — N28 and the runtime BUILT · the sweep is portfolio-wide

Build session (`2eaa27b` · `cd6cf21`), **443 → 463 tests** at this point
(474 by end of 05-08), ruff + `mypy --strict` clean.

- ✅ **N28 built: `VALUATION_SWEEP` is the tenth event type.** Key = the
  scheduled instant alone (a late sweep is still the sweep due then, so
  redeliveries dedupe and replay reproduces the sequence).
  `missed_intervals` is producer-stamped — recomputing it in the engine
  would need a clock read. §3.1.4's thresholds now actually reach §3.4
  status and §3.5 confidence: both were wired but nothing ever produced
  the number. ⚠ The type stays unblessed — §7.3 fixes nine. Ask with N23.
- ✂ **Correction to 03-08: the sweep is PORTFOLIO-WIDE, not
  per-security** (§3.1.4 + §2.5: complete recalculation of the full
  universe each sweep). One event per 2.0 s slot covers all 170 —
  **0.5 events/s, not 85** — so the emit-on-effect volume control is
  unnecessary and DROPPED. N28's row is corrected.
- ✅ **`mm/runtime/` built — the loop that owns the clocks, in one file.**
  Everything else stays a pure function of its events; `runtime/loop.py`
  is the single module that reads a clock, deliberately, so a second
  clock-reader cannot creep in unseen. The 1 s tick: beat FIRST (inside
  the poller — a slow source can never delay the dead-man), drain, due
  polls, due sweep. `SweepScheduler`: fixed slots (a late tick does not
  push later slots back) · a stall emits ONE sweep carrying the missed
  count, never a backlog (§3.1.4's own wording; a backlog would recompute
  identical universes and publish nothing per §3.1.5) · the first call
  anchors and owes nothing. `run()` cannot overlap ticks; a slow tick
  shortens the next wait rather than drifting.
- ⚠ **Boot order recorded in `[boot]`:** connect → beat → replay →
  reconcile → tick. Replay is synchronous inside the gateway's **30 s
  boot grace**, and the journal grows all season — which is exactly why
  §10.3 checkpoints are REQUIRED before the season (every deploy is a
  restart). Until then boot time is a number to watch.
- 📝 Still unwired in the runtime: **tiered polling** (one interval for
  every game today; the 03-08 tier table needs the 🔴 pre-kickoff number)
  and the **composition script** (transport → boot → reconcile → run; the
  wire test remains the prototype).

## 2026-08-04b — three items closed, nothing blocks the build

George's rulings at the end of the design thread.

- ✂ **No new database. Dropped (George).** It was proposed for the
  *panel* — so a person could query Edwin's file history and diff
  revisions. **The engine never needs it:** it reads the file, holds `T`
  in memory, and the journal records the event. **The bucket plus the
  journal covers everything we run.** Revisit only when the panel earns
  it. The bucket half of the 03-08 storage split stands unchanged.
- ✅ **Cloud NAT exists (George).** The MM VM can reach Sportradar. The
  concern raised on 03-08 is closed. **N30's remaining half is only the
  subnet layout**, which is a deployment-time question, not a blocker.
- ✅ **Secrets: Terraform surfaces them initially (George).** The panel
  handles updates later. Closes the "secrets" design item.
- 📝 **Supervised-test mode needs no design.** T10 is a fact, not a
  choice: tZERO gives us one environment for everything.
- ✅ **"What the engine publishes" is PARKED** until the panel matters.
  It is the contract between the engine and the panel — which subjects
  carry positions, prices and market states. Today nothing leaves the
  process except orders, so the only way to see what the MM did is to
  read the journal by hand. Not a blocker; nothing consumes it yet.
- ⭐ **Boot and death is NOT a separate design item — it is the runtime's
  boot sequence and shutdown.** Building `mm/runtime/` answers it.
- **Nothing blocks the build. Next: `mm/runtime/`.**

## 2026-08-04 — the 200 ms constraint is a CAPABILITY requirement (George)

Design session, continuing the deployment thread. George settled a
question this log had been treating as open, and the consequence is an
architecture constraint rather than a config value.

- ✅ **The machine must be BUILT CAPABLE of republishing every live
  security every 200 ms during games. George, agreed with Edwin.**
  Running slower is acceptable; being unable to run that fast is not.
  ⚠ **This is a capability requirement, not a cadence decision** — nothing
  in the design may assume slow. **Stop relitigating E18 as a build
  blocker**; E18 remains the question of what rate we actually choose.
  ⚠ Note the §5.8 tension is real and unchanged: §5.8 forbids
  republishing without material change, and SR's measured median update
  gap is 4 s, so a forced 200 ms republish is mostly the same prices with
  newly randomised quantities. That is a product choice for Edwin, not an
  engineering objection. **The build must support it either way.**
- ⭐ **Priced at the ceiling, THEN MEASURED** — NCAA Saturday, 35 games,
  70 hot securities, 6 orders each, full republish every 200 ms:

  | Limit | Estimated | **Measured 04-08** | Verdict |
  |---|---|---|---|
  | Engine compute | ~140 ms per pass | **6.30 ms** median, 9.53 ms worst (0.17 ms per event) | ✅ **FITS — 3 % of budget.** The estimate was **22× pessimistic** |
  | The journal | ~1,000–3,000 events/s | 35,637/s on a Mac — **not credible** | 🟡 **UNMEASURED.** See the caveat |
  | The venue | 2,100 msg/s vs a 50 msg/s gateway governor, `MaxOrdRate` unknown | not ours to measure | 🔴 **T2** |

  - ✂ **Correction: "Python cannot hold 200 ms on compute" is wrong.** The
    ~2 ms-per-reading figure was carried from a parameters note and did not
    survive measurement. Real cost is **0.17 ms per event**, so a full pass
    over 70 hot securities is **6.3 ms**. ⚠ That number excludes the sync
    driver's diff, payload serialisation, the NATS publish, inbound ack
    processing, and the §3.1.4 sweep over all 170 — it is the engine core
    only. But 22× headroom absorbs a great deal of unmeasured work.
  - ⚠ **The journal figure is invalid, not favourable.** On macOS
    `os.fsync()` does **not** force the drive to flush its write cache
    (that needs `F_FULLFSYNC`), so 0.028 ms per append measures the OS
    buffer rather than durability. On GCP persistent disk a real `fsync`
    is plausibly 10–30× slower; at 30× we would sit near 1,200 events/s
    against a 2,100/s need, i.e. **under**. **N31 stays open until the
    number comes off the real VM.**
  - 📉 **Consequence for the Go port: the performance argument is much
    weaker.** Concurrency for the I/O-heavy runtime and matching the
    gateway's language remain real reasons. *"Python is too slow to
    quote"* is not one.
  - Benchmark script kept in the session scratchpad; re-run it on the MM
    VM once N30 lands.

- ⚠ **NEW, and the most important finding: the journal is the throughput
  ceiling, not the engines.** `journal.py` flushes and `fsync`s on EVERY
  accepted event — that is what makes it durable before anything reacts
  (§7.4). An `fsync` on a GCP SSD is roughly 0.3–1 ms, so a single writer
  tops out near 1,000–3,000 events/s. The 200 ms ceiling sits exactly on
  that line. **Resolution: design group commit** — batch events arriving
  in the same moment into one `fsync`, with nothing counted as accepted
  until its batch is on disk. Durability semantics survive. Filed as
  **N31**. Far cheaper now than retrofitted, which is George's whole point.
- ✅ **Polling efficiency: press the S7 live-bulk endpoint.** George asked
  for a more efficient poll; the answer already exists as the *preferred*
  S7 ask — Sportradar's global AF probabilities v2 carries a live-bulk
  endpoint returning every live game in ONE call. On an NCAA Saturday that
  is 1 call instead of 35, i.e. ~0.5/s instead of ~17/s. Separate product,
  **Cody-gated** commercially. **Press it — it is now a capability
  prerequisite, not an optimisation.**
- ✅ **Quiet-day polling: keep polling, but N24 decides whether there is
  anything to poll.** The probabilities API is per-game and in-play, so
  with no game running SR has no probability for a team. Whether SR
  publishes **pregame** movement is **N24**, open — our one captured game's
  first reading sits exactly at kickoff. **Ours to measure in August.**
  What genuinely moves on a quiet day is Edwin's daily file and the
  off-field values.
- ✅ **Every deploy is a restart (George agreed) — so §10.3 checkpoints
  stop being optional.** Restart time is dominated by journal replay,
  which grows all season. Checkpoints bound it. They were parked on 02-08
  as "its own session"; that parking is now **promoted to required before
  the season**. ⚠ **A hot standby is not available** — two processes means
  two writers, which the journal forbids by design (`[second-writer]`).
- 📅 **Direction, PARKED — build the whole thing in Python, get it
  working, then port to Go** (George, 04-08). The port is real and still
  intended; it is simply **not this session's concern and changes nothing
  about what we build now**. ⚠ Two intermediate readings recorded earlier
  in this session are superseded: "Python carries season 1" and "real
  trading starts on Go, Python is only the oracle". **Everything is built
  in Python, in its entirety, and nothing moves off the Python critical
  path** — the VM, Cloud NAT, secrets, supervised-test mode, deployment
  and **N31** are all live Python items.
  - ⚠ **The hard part of a port is not writing Go — it is replay
    byte-equality.** Four hazards, recorded now so the port day is a
    checklist rather than a discovery:
    1. **Decimal arithmetic** — Go has no built-in decimal. Rounding mode
       and precision must match exactly or prices diverge at the penny.
    2. **Canonical JSON** — the payload hash is `sort_keys=True`,
       `separators=(",",":")`, `ensure_ascii=False`. Go's `encoding/json`
       escapes HTML by default, so every hash changes unless matched.
    3. **Map iteration order** — Python dicts are insertion-ordered, Go
       maps are deliberately randomised. Order-dependent iteration
       diverges *silently*, the worst failure mode.
    4. **Seeded randomness** — ✅ **already safe.** §5.7.3 seeds from
       **SHA-256**, not a language PRNG. Chosen for replay; it happens to
       pay for the port too.
  - ✅ **The mitigation already exists: differential replay** — the same
    journal through both implementations, compared byte-for-byte. Ch 8
    already proved two independent stacks emit byte-identical payload
    streams.
  - 📝 **Preserving Python's journals as a port oracle is NOT required**
    (George, explicit). The journal **format** is what must match.
  - 📝 The port-friendly hygiene (sort before iterating, pinned decimal
    contexts, canonical JSON) is **already required by §1.6-4's
    determinism rule** and is honoured in the code today. It is not new
    work and was not adopted because of Go.
- 📝 **Edwin's daily file — structure IS settled and built** (George could
  not recall; verified against the code). One JSON file, all 170 teams,
  06:00 ET daily, published even when unchanged. Per team:
  `expected_remaining_wins`, `sigma`, `games_remaining`, `effective_time`,
  `revision`, `is_correction`, `methodology_version`. Corrections resend
  the same `effective_time` with a bumped `revision`. It supplies **T**,
  the whole-season expected wins, from which the on-field leg is built —
  `$5 × (T − Σ p_ref + Σ x)`. Without T a team has no price and the code
  refuses to construct one. Reader: `src/mm/adapters/reference_feed.py`,
  which returns EVERY violation at once. **Open is the delivery on the day
  and the §7.3 event type (N19, N23) — not the schema.**

## 2026-08-03b — N29 answered · ⚠ the vault's VPC addresses are wrong

Same session, after George pointed at the right panel repo. Two findings,
one of which corrects the entry below.

- ✅ **N29 answered — the MM panel is `inplay-admin-panel-trading`**
  (`Novosapien/inplay-admin-panel-trading`, "QA test bench and
  monitoring", TypeScript, last pushed 30-07). **Not**
  `inplay-admin-panel`, which is the internal-operations panel where the
  vault and the CI assets are surfaced. Cloned locally 03-08.
  - It already carries the shape the MM needs: routes for `tzero`,
    `trading`, `market-data`, `health`, `vpc`, `test-bench`,
    `simulations`, `loadtest`, `resilience`; API routes for `gateway`,
    `nats`, `orders`, `positions`, `market`, `centrifugo`.
  - **The pattern is already built.** `proxy/` is a Python FastAPI
    service running INSIDE the VPC holding `nats_client.py`,
    `centrifugo_client.py`, `vpc_topology.py`. The Next.js routes sit
    outside and call it (`proxyFetch("/nats/monitor")`). So the MM panel
    is new pages plus new `proxy/main.py` endpoints — **no new
    deployment unit for monitoring**.
  - Stack: Next.js 16 · React 19 · Chakra + shadcn · deployed on Vercel
    (`ALLOWED_ORIGINS` names `inplay-admin-panel-trading.vercel.app`).
  - ⚠ **The panel queries no database.** Every route goes through the
    proxy, whose dependencies are `nats-py`, `redis`, `httpx` — no
    Postgres client. The one exception is `api/tzero`, which calls an
    `ONBOARDING_URL` service directly. Cloud SQL exists (PostgreSQL 15,
    database `inplay`, plus `inplay-trading-db` and `zitadel`) and the
    panel displays its **health**, but does not read from it.
  - ⚠ **Access control matters here.** This panel carries destructive
    controls — `/loadtest`, `/stress-test`, `/resilience`, and a
    `nats/purge` endpoint. The MM kill switch and
    `CONFIGURATION_ACTIVATION` would sit beside them. Roles exist (an
    `(auth)` group; commit `7eab0ad` "allow viewer role to see Market
    Data"). Confirm which role gates what before the MM control surface
    lands.
- ✂ **CORRECTION to 03-08 below: the VPC addresses in
  `vault/drafts/VPC Setup.md` do not match the live configuration.**
  `proxy/.env.example` is the deployed truth:

  | | `VPC Setup.md` (vault draft) | `proxy/.env.example` (live) |
  |---|---|---|
  | FIX gateway | `10.0.0.2` | `10.0.1.2` |
  | NATS | `10.0.0.3` | `10.0.2.2` |
  | Redis | — | `10.78.64.3` |
  | Cloud SQL | — | `10.78.65.3` |
  | Subnet | `10.0.0.0/24` | not a single /24 |

  So **`10.0.0.5` and `nats://10.0.0.3:4222` in the 03-08 entry are
  wrong** and have been struck there. The **shape** of N7 is unaffected —
  own VM, same subnet as NATS, one writer — only the addresses are
  unknown. This is the MM working mode's third stop condition (reality
  does not match the docs), so it is flagged rather than guessed.
  📅 **For Hasan, one message:** confirm the real subnet layout and the
  MM VM's address, alongside the Cloud NAT question.
- ⭐ **New fact worth carrying: Redis is already in the stack and already
  in the proxy** (`10.78.64.3`, TLS). For the MM's **live** projection
  that is a better home than Postgres, and it adds no dependency.
- ✂ **Refines 03-08's "projector → database → panel".** That was written
  before the panel's real data path was known, and it was too broad.
  Split it by question type:
  - **Live monitoring** (positions, market state, resting book, poll
    counters) — read live through the proxy, following the panel's
    existing grain. No projector, no SQL.
  - **Historical and relational** (Edwin's file rows, the accepted and
    rejected history, revision diffs) — still needs the bucket plus a
    queryable store, because a live read cannot answer "diff revision 1
    against revision 2". The bucket/database split stands **for the
    file**; it does not generalise to the whole MM state.

## 2026-08-03 — deployment architecture: N7 answered

Design session with George, no code. Settles where the machine runs, where
its data lives, and how the MM panel reads it. Full reasoning and the
three-clock addendum: `sessions/2026-08-03-deployment-architecture.md`.

- ⚠ **Correction to a standing assumption.** NATS does NOT run on the FIX
  gateway VM. Per `vault/drafts/VPC Setup.md`: gateway `10.0.0.2` (static
  public IP, tZERO-whitelisted) · NATS JetStream `10.0.0.3` (no public IP)
  · Centrifugo `10.0.0.4`, all in `inplay-subnet` (`10.0.0.0/24`,
  us-east4), inter-VM latency under 1 ms.
- ✅ **N7 answered — one stateful engine plus one stateless panel, joined
  by NATS.** They share no disk and never call each other.
  - **MM engine** — its own VM, `e2-medium`, in the same subnet as NATS.
    One writer. ⚠ **Address TBC — see the 03-08b correction below.**
  - **MM panel** — new pages in `inplay-admin-panel-trading` (N29), plus
    new endpoints in its in-VPC `proxy/`. No new deployment unit.
- ✅ **Not Cloud Run for the engine, and not the gateway VM.** The engine
  is one long-lived single-writer process with an fsync-per-event journal;
  `journal.py`'s `[second-writer]` note makes a second writer a stop
  condition, so scale-to-zero and container recycling are disqualifying.
  The gateway VM is the single point of failure that holds the whitelisted
  IP — adding load there buys nothing at under 1 ms.
- ⚠ **The MM VM needs Cloud NAT** (or its own public IP, which is worse).
  The poller calls Sportradar over the public internet; Private Google
  Access covers GCP APIs only. `VPC Setup.md:660` documents the fix and
  marks it as not yet created. **For Hasan — confirm before the VM exists.**
- ✅ **Restart posture: auto-restart with a rate limit** (systemd
  `Restart=always`, roughly 5 in 60 s then stay down), alarm on repeats.
  Journal replay makes restart safe. Between death and restart the
  gateway's 4 s dead-man clears the book, so no stale quotes rest.
- ✅ **The journal lives on a dedicated persistent disk**, never the boot
  disk, with hourly snapshots. §10.4's retention period is still an
  unfilled §12.3 slot (InPlay policy).
- ✅ **Edwin's daily file: the bucket stores the file, the database stores
  the parsed rows.** They are not the same data twice.
  - The **bucket** holds the file exactly as sent — the evidence.
    Rejected files land here too, with the reason in object metadata
    (N19's perpetuity ruling: a rejection is evidence).
  - The **database** holds the parsed rows — about 30,000 per season. The
    real questions are relational (T for one team on one date; revision 1
    against revision 2; every correction).
  - The row carries the object's path and hash. **The test of the split:
    the database can always be rebuilt from the bucket, and the bucket can
    never be rebuilt from the database.**
  - ⚠ The bucket is chosen for §10.4, **not for size** — the file is
    50–100 KB. A retention lock makes deletion impossible even for an
    administrator; a database row is editable and an `UPDATE` leaves no
    trace without audit triggers. Absent §10.4 one store would be simpler.
  - ⚠ **Do not apply the retention lock yet** — the period is unset and a
    lock is irreversible. Enable versioning now, lock when the number lands.
  - ⚠ **Write the object first, then the row.** An orphan object is
    harmless; a row pointing at a missing object is not.
  - **This also collapses the interim question:** Edwin drops the object
    now, the upload page writes the object later, and the engine watches
    the bucket either way. One path, built once.
- ✅ **The MM panel never reads the journal.** The journal is
  single-writer, fsync'd, replay-critical, and its format is internal. The
  engine publishes state to NATS; a projector writes that state to the
  database; the panel reads the database. This matches the 24-07 phasing
  (read-only first, the same APIs users get).
  - ⚠ **The panel is a projection, not the truth.** Expect it to lag the
    venue. Say so before someone reports the lag as a bug.
  - Phase 2 control runs the other way: the panel publishes
    `MANUAL_CONTROL` / `CONFIGURATION_ACTIVATION` to NATS and the engine
    journals it. Ch 6's kill switch already proves that path.
- ✅ **The §3.1.4 sweep scheduler is a PRODUCER, outside the deterministic
  core (ours, recorded).** The real constraint is not §7.3's type list: the
  orchestrator reads **no wall clock** (`[clock-stays-put]`) and §3.3's
  ages are differences of event timestamps (`[ages]`), so a clock-driven
  sweep has no legal `at`. Constraining sweeps to demotions does not help —
  a demotion changes the book as surely as a promotion.
  The scheduler therefore sits beside the poller, emits a journalled event,
  and the engine stays purely event-driven. Replay consumes the emitted
  events and never re-runs the scheduler.
  **Volume control: emit on effect, not on tick** — 170 securities at
  0.5/s would write 85 events per second and §10.4 keeps them all.
  Needs a tenth event type → **N28**, basis `security_id + scheduled_time`.
- 📅 **Still George's call: N29** — does the MM panel live in the existing
  admin panel, or in a new desktop app shell? Days against weeks.

## 2026-08-02b — George triages the open questions: eight closed, three slimmed

Housekeeping pass on [[market-maker/open-questions]] (resolved rows had
already moved below the fold earlier today). **64 open → 56 open.**

- ✂ **E4 closed** — the old simulation code is superseded by the 30-07
  ASMM-1 handoff package.
- ✂ **E6 closed** — week-zero mismatch openers are not a question: pricing
  rides SR probabilities + Edwin's T; a mismatch is just a lopsided number.
- ✂ **E7 closed** — "how strictly do the standards bind" was answered by
  the v1.3 spec adoption (24-07): the spec is the bar, deviations ride
  this log.
- ✅ **E8 resolved** — deliberate price-moving is "not in v1", agreed when
  filed.
- ✂ **E10 closed** — the v1.3 spec Ch 3 carries the full valuation math;
  the missing CTS-001 chapter is historical.
- ✅ **E16 resolved with a residual** — trading is continuous, no sessions
  or auctions; the one gap is the venue boundary. Hard fact: the FIX
  session runs **00:01–23:59 ET** (gateway config; DAY expiry at 23:59
  venue-verified). ⚠ George recalls **~30 min** of nightly downtime — the
  venue-side window's true length now rides **T9/T10** for the next T0
  call. Do not record the half hour as fact until T0 confirms.
- ✅ **E22 resolved** — shares outstanding are **900,000 NFL / 1,000,000
  NCAA** (IPO Requirements v2 §1.2/§5.1, gospel). The unoffered-100k
  question lives on as N21.
- ✅ **E23 resolved** — Edwin's price composition was answered in practice
  by the 28-07 email: his exact on-field formula is built and his unit
  tests pass; the off-field terms are §3.6's own build.
- 📝 **E18, E21, E24 slimmed to their single remaining asks** (E18's full
  refinement stays in the 31-07 entry; E24 now carries the leading
  reading — §4 governs per E20's ruling → Rounds 1–10 → 85 M max — one
  line from Edwin confirms it).
- ⭐ **E26 marked priority (George):** *is the MM itself ever going to
  short?* Ask in the Edwin round.

## 2026-08-02 — first contact: the wire test passes against the real gateway

The loopback wire test — George's precondition for any live attempt —
**passes all five phases** (heartbeat · post · move · kill switch ·
dead-man) against the real gateway binary in LOOPBACK_MODE over real NATS,
343 order events consumed on the passing run. Commits `abd8b2a` ·
`c477713` · `7b510ea`, 434 → 443 tests. Story page: "First contact" 📡.

- ✅ **The NATS transport exists** (`venue/nats_transport.py`) — one queue,
  one writer task, strict FIFO so post-first ordering survives onto the
  wire; a dead writer raises on the next publish, never silently.
  `nats-py` is the repo's first runtime dependency, confined to the edge.
- ⭐ **Three wire-only findings, each fixed where it belongs (gateway
  facts = gospel, 22-07 filter):**
  1. The gateway's LOCAL publish paths (loopback accepts; every cancel it
     resolves itself, dead-man and cancel_all sweeps included) put **no
     order id in the payload** — the subject `order.{user}.{clOrdId}` is
     the only name. The adapter falls back to the topic's last segment.
  2. The gateway's **eight publisher workers do not preserve timestamp
     order across subjects** — two acks for one security arrived 10 µs
     reversed and tripped the volatility engine's backward-clock guard.
     The orchestrator now floors each security's cycle clock at its
     high-water mark; deterministic on replay, absorbs only µs jitter.
  3. **cancel_all is a hammer, not a stop.** Fired alone, it swept 48
     orders and the live bot correctly treated the empty venue as
     divergence and REPOSTED. The stop is Ch 6's kill switch; the drill
     now proves suspend-then-sweep holds and nothing reposts.
- ✅ **Game discovery built** (`poller/discovery.py`) — the Sport Schedule
  endpoint on the SAME v1 product as the timeline (one S1 entitlement
  covers both) → the games touching our universe, membership via the
  valuation engine's own team map; replaced events skipped;
  `ensure_game()` idempotent.
- ✅ **§10.3 checkpoints deliberately deferred as a full session** —
  complete-state snapshots + integrity hashes + replay-from-checkpoint
  equality across eight engines is not a fill-in item. Recorded, not
  squeezed.
- 📅 **For Hasan:** the gateway Dockerfile pins golang:1.23 while go.mod
  requires ≥ 1.26 — the image no longer builds as committed (we built with
  an override). And the local publish paths omitting clOrdId (finding 1)
  are worth aligning with the real-venue path, which includes it.
- **Where this leaves the build: everything the venue side needs before
  live now exists and is wire-proven. What remains is permission —
  T1/T2, S1/S7 — and the unsent Edwin round E29–E37.**

## 2026-08-01c — the ungated tier lands: step 5 · Chapter 6 · Chapter 12

Third stretch of the day, autonomous integration mode. Three build commits
(`7c43131` · `2f21d81` · `2d3afd8`), **392 → 434 tests**, ruff + mypy strict
clean. Story page: "Permission to quote" 🚦.

- ✅ **The §3.2.1 sum check runs at the acceptor's door (§7.2's Business
  Validated stage), and rejections are audited.** A rejected event gets no
  Accepted Event Sequence and a `rejected` journal line carrying the
  reason. Because validation precedes dedup (spec order), a corrected
  resend under the same key is later accepted, and every re-delivery of a
  bad reading writes its own record. The engine's silent-drop branch now
  raises. Closes the last 27-07 review gap — the fix pass is complete.
- ✅ **Chapter 6 built.** §6.3 in §6.2's precedence; §6.4.1's promotion
  ceiling separate from the demotion floor (ordinary synchronizing demotes
  nothing but blocks the last climb to Stable); the tracker demotes
  instantly and promotes one rung per served 10 s dwell. **Suspended →
  Defensive is dwell-free (ours, recorded):** §6.4.1 names dwell conditions
  for the two upper climbs only, mirroring §3.4.1's first-rung grant — so a
  healthy security quotes on its first trigger rather than 10 s late.
  Dwell toward one rung never counts toward the next.
- ✅ **The kill switch is an event.** MANUAL_CONTROL (idempotency: Control
  Action ID) drives the global kill switch and per-security suspension —
  journalled, deduplicated, replay-identical. Payload shape is ours pending
  the ops UI; §6.3's "release requested but unapproved" middle state is an
  ops-UI workflow and does not exist yet.
- ✅ **The suspension sweep runs every suspended cycle, quiet by state
  (ours, recorded).** The flip-gated version had a hole: an order submitted
  just before the suspension is not yet cancellable, and when its ack
  landed the flip was spent — it rested through the suspension. Per-cycle
  sweeping cancels it on the ack's own cycle; already-cancelled orders are
  PENDING_CANCEL and never re-sent.
- ✅ **Edwin's four-state dwell table replaced the LIVE-only interim**,
  keyed on an activity axis (LIVE / PRE_KICKOFF / POST_GAME / OVERNIGHT)
  derived from the fixture rhythm — deliberately NOT §6.1's Market State,
  two axes both called "state". ⚠ The window boundaries (1 h before
  kickoff, 1 h after the final) are ours as interims under **N4**; the
  pre-hour mirrors §3.3.2's tightest band.
- ⚠ **The spec disagrees with itself on Recovery Ready → E37.** §6.3 maps
  Ready → Defensive; §6.4.1 permits the Defensive → Active climb with
  "Normal or Ready" — unreachable under the §6.3 row. Both implemented
  literally, the stricter wins; cannot bite until §10 recovery exists.
- ✅ **Chapter 12 built — the registry and the sweep.** Every configurable
  value lives in `mm/config/dictionary.py` with its status; §12.3's
  no-default parameters are None slots awaiting their named sources (T2,
  the ICD, InPlay policy); cross-parameter validation runs at construction.
  Fifteen modules alias their constants from it; the CONFIGURED-marker
  convention is retired and a test fails if it reappears. Deliberately
  absent: the superseded §5.2/§5.6/§5.7.1 tables, §9.2's 85 % (E20), and
  §3.6's unbuilt rows. Runtime activation/rollback stays unbuilt.
- ✅ **Active and Defensive quote identically for now** — their parameter
  widening is E31's per-state width floor; the slot exists in `width.py`
  and wires in one call-site when Edwin's values land. Suspension is the
  only enforceable state effect today, which §3.4's effects column already
  demanded.

## 2026-08-01b — Chapter 8 built in one run · two venue facts supersede the spec

First session under the autonomous integration mode, run as designed: four
commits (`56efd57` · `3b590cc` · `e7bdecb` · `4f12ab6`), 329 → 385 tests,
ruff + mypy strict clean, review at the chapter boundary. The gateway repo
was pulled first (6 new commits); two research agents mapped the gateway
contract and our integration surface before any code was written.

- ⭐ **tZERO recycles ExecIDs — §7.3's EXECUTION key is superseded (venue
  fact, gospel).** Proven by incident, not inference: on 29-07 the FIX
  gateway silently discarded both execution reports of a real filled order
  because ExecIDs 1658/1660 had been seen the previous day on a different
  symbol (gateway commit `e37cd3d`; the fill reached no part of the
  platform). Our key is now (venue, **client_order_id**, execution_id); a
  session gap-fill repeats both, so genuine retransmissions still dedupe.
- ✅ **DONE_FOR_DAY joins the §8.2 state table (venue fact).** tZERO ends
  its session at 23:59 ET and every resting DAY order expires as a distinct
  terminal state. Folding it into Cancelled would blind the morning repost.
- ⚠ **Time-in-force is DAY, and the consequence is book-visible → E36.**
  The book vanishes at 23:59 ET nightly and reposts after the boundary.
  GTC has no gap but leaves a dead bot's quotes resting with only the
  dead-man as cleanup. Built as DAY behind one CONFIGURED constant;
  Edwin's call which way it ships.
- ✅ **The reconciler implements rest-until-gone exactly as ruled (23-07,
  N10):** a still-wanted price is left alone, never topped up; a price move
  is one cancel/replace carrying the remainder (`CumQty + LeavesQty` — which
  satisfies the gateway's quantity-above-fills guard by construction);
  post-first ordering per N12. §8.3 honoured: no replace ever relies on
  keeping queue priority. §5.9 stays unbuilt — E17 decides the lifecycle.
  **✂ 07-08h: the remainder-carry on MOVES is superseded — a replace now
  adopts the new rank's drawn size (`CumQty + level.quantity`). Kept-order
  rest-until-gone stands.**
- ✅ **§4.4's PBE/PSE includes Partially Filled (ours, recorded).** The
  spec's state list omits it; a part-filled order's remainder still rests,
  and excluding it understates exposure. §4.4 and the Effective Position
  Ratio are now fed by real venue state — the last test-supplied quote
  input chain is gone.
- ✅ **Exposure begins at the decision to send.** Intent is registered with
  the Venue State Record BEFORE an instruction is published — the gateway
  never acks that a message reached it (malformed JSON is a silent drop),
  so register-first is the only order that never understates exposure.
- ✅ **ClOrdIDs mint deterministically** — MM prefix + 16 hex chars of a
  SHA-256 over pipe-joined context, the §5.7.3 seed scheme reused. 18 of
  the venue's 20 chars, no leading zero, no dots (the id becomes a NATS
  subject token and the gateway does not guard against a dot — we must).
- ✅ **The §7.5 audit chain closes.** cycle() and the Target Order Book now
  carry the triggering Accepted Event Sequence — event → RP → book is
  traceable end to end. §5.10 check 1 is real on every cycle (a
  StatusTracker status is always supplied).
- ✅ **Overnight books do not suspend (ours, recorded).** A security with no
  game live and none imminent reports its probability condition CURRENT —
  the input is not stale, it is not needed; the price rides T and the
  off-field values. Marking it Invalid would suspend all 170 books nightly
  against §2.5's 24 h/day evaluation. Daily-feed staleness is N23's
  question, unbuilt.
- 📅 **E27 movement from the gateway log:** the 35=UEPR position-seeding
  probe drew nothing on 28-07 — but tZERO switched that message family ON
  later the same day (35=UEAR now answers in 12–17 ms; buying power is
  settable per account over FIX). **Re-probe UEPR before declaring the
  venue-side seeding path dead.**
- ⚠ **Gateway facts worth keeping:** the MM rate governor REJECTS
  over-limit messages rather than queueing (deliberate — a stale order is
  worse than a refused one) · ~~`market.book.*` is defined and never
  published, do not build against it~~ ✎ **SUPERSEDED 14-08 (fix-set
  CA2): the depth feed is LIVE and load-bearing** — the deployed gateway
  env reads `TZERO_MD_FULL_BOOK=true` + `TZERO_MD_BOOK_SYMBOLS=*`
  (sudo-verified on the VM, 14-08); the taker's live trading gates every
  order on a fresh `market.book.{symbol}` and the R-Q09 marketable guard
  builds on the same feed. The 01-08 line described the pre-08-08 world ·
  JetStream durable publish is OFF by
  default (`NATS_JETSTREAM_PUBLISH=false`) — at-least-once is a deployment
  property to confirm at cert, not a code fact.

## 2026-08-01 — the working mode splits in two

- ✅ **Integration work is built autonomously; domain work stays step by step
  (George).** The step-by-step mode existed because the domain concepts were
  new and every piece needed his ruling. What remains — Ch 8 venue sync, the
  poller, Ch 12 config — is engineering mechanics under the 22-07 remit line,
  so Claude builds a full chapter per run: pieces committed separately,
  BUILD-LOG per step, tests green, review at the chapter boundary against
  one story-style explainer. **Three stop conditions survive:** anything
  book-visible (Edwin's remit) · anything contradicting this log · anywhere
  the gateway's real behaviour differs from its documentation. Recorded in
  the repo CLAUDE.md.
- 📅 **Estimate under the new mode: code-complete ~4–6 August** (was 10–12),
  leaving ~3 weeks to the 26 Aug deadline for QA against the real venue —
  which is only usable if **T1** and **S1/S7** land. The asks move in
  parallel now.

## 2026-07-31 — Chapter 5 built · §3.3–§3.5 built · the machine quotes

- ✅ **Chapter 5 is built, in the adoption spec's five pieces.**
  `volatility.py` (σ²) · `width.py` (γσ² + C) · `ladder.py` (§5.3/§5.4/§5.6)
  · `quantity.py` (§5.7) · `quotes/engine.py` (§5.8/§5.10/§7.5). **329
  tests**, ruff and mypy strict clean. Mechanisms only — every constant is
  🟡/🔴 pending E31. Deferred, externally gated: §5.5 (Ch 8) and §5.9 (E17).
  Headline proof: two fresh engines fed the same six events produce
  **byte-identical books, version chains and check reports**.
- ✅ **§3.3–§3.5 are built** — freshness bands, Reference Price Status with
  the §3.4.1 ratchet (demotions instant, promotions one rung per 10 s dwell,
  relapse resets), and Confidence with its status ceiling. §5.10's check 1
  is real whenever a status is supplied. **MEV** (§5.4's ceiling) computed
  in `reference_price.py` — the last test-supplied quote input gone.
- ⭐ **Materiality is judged BEFORE the §5.7.3 variation, on the held
  shape.** Final sizes are drawn with a fresh quote version, so they always
  differ — comparing them would republish every cycle. The comparison
  record stores pre-variation sizes; "a different possible random quantity
  is never a reason to publish" holds by construction.
- ✅ **The Quote Version increments only on publish**, and every seeded draw
  (shape, extra, dwell, sizes) is keyed on it — the whole replay result
  hangs on this. A held cycle consumes nothing.
- ✅ **N26 implemented as filed and closed.** §5.8's thresholds are the only
  publish trigger; an expired dwell only permits the next real publish to
  carry a fresh shape, at zero extra venue messages.
- ⭐ **An Invalid status gates the cycle BEFORE any state is touched —
  including σ² (George's dead-feed question).** A dead feed's frozen price
  reads as CALM to a volatility estimator and would tighten the book into
  the §2.3 danger case. Same-value-new-timestamp readings are accepted and
  reset the age — a feed confirming its number is alive; only silence
  decays trust.
- ⚠ **Cold starts are wide-when-ignorant, and that is book-visible → E31.**
  A new security's first σ² reads at the ceiling (V₀ = ceil ÷ H — the
  ceiling is on σ², not V, George's catch); a new StatusTracker starts
  Invalid and earns Degraded with its first valuation. Safe direction
  built, Edwin signs off the values.
- ✅ **The odd-tick side is a stateless seeded 50/50, not strict
  alternation** (ours under the remit line, tagged `[odd-side]`). Strict
  alternation needs "which side was it last time"; the hash bit achieves
  the same fairness with no state and full replay safety.
- 📅 **E18 refined into three separate numbers (George's challenge):** the
  poll rate (~2 s, matches SR's measured 4 s median), the reaction bound
  (~200 ms, costs nothing — the engine is event-driven), and §3.3's bands
  (break-detectors a healthy feed never trips). ⚠ Republishing every 200 ms
  to refresh the randomisation is explicitly forbidden by §5.8 and would
  cost queue position on every book 5×/second. **New question for Edwin:
  is 200 ms a reaction bound, or does he want the book visibly moving with
  no new information?** His RPV-2 instinct suggests the latter; his spec
  says the former.

## 2026-07-30b — a second market maker arrives · the Edwin call · a process fix

- ⭐ **Edwin will send spec-style documents with the equations, not code
  (agreed on the call, 30-07).** George raised it directly: three documents so
  far, each changing things, roughly a week spent understanding the first
  before the second moved it. Framed as *"we want to move fast, but this is
  not our area of expertise."* Edwin was fine with it and will rewrite the
  handoff package as a narrative document. **This is the most valuable outcome
  of the day** — more valuable to the timeline than any single algorithm change.
- ✅ **ASMM-1 is not a drop-in replacement, and Edwin accepts it.** His opening
  position was *"I think I've done the market maker for you… all you need to do
  is plug the code into T0."* The argument that landed, checkable in one line
  of each file: **`quote(now, rp, inventory)` takes the reference price and the
  share count as arguments**, and `RPV2.step(now, fair_value)` takes the fair
  value. Neither module computes either input. Our build computes both.
  Everything downstream — Chapter 3, the feed reader, the SR path, positions,
  the journal, replay — is untouched by his package.
- ⭐ **Adopt his width equation into Chapter 5.** `width = γσ² + (2/γ)ln(1+γ/k)`
  plus a seeded 0–3 tick extra. It replaces §5.2's lookup table, which is keyed
  on a state classifier **we never built** (N3's thresholds are still 🔴). His
  needs no classifier, no new inputs, works in an empty book, and cannot be
  gamed by posting orders — it reads only our own Reference Price. ⚠ The
  `(2/γ)ln(1+γ/k)` term is a **constant, 1.653 ticks**, because γ and k are
  constants. Compute it once at construction.
- ⭐ **Volatility scales the width, never the lean (George).** The width is a
  risk control, so volatility belongs in it. The lean is a **distribution**
  tool (29-07: §1.5 excludes profit, so the reason to shed inventory is that a
  market with no shares in circulation is not a market). Vol-scaling a
  distribution tool means pushing hardest to distribute during a live game and
  least overnight — backwards — and it reaches the cap sooner, so **it makes
  N20 worse**.
- ✅ **Keep our float denominator for the lean; his is wrong for us.** §4.3
  divides by the Reference Float, which answers *what share of this team do we
  own?* His divides by **4,000 shares**, which has no relationship to the
  security. Every extra share moves his lean ~22× further, so his cap arrives
  ~19× sooner: ours pins at 225,000 shares, his at **12,000**. §4.3–§4.6 stand
  as built; no change to `inventory.py`.
- ✂ **Reject his one-sided guard and his drawdown kill.** Past 6,000 shares in
  a live game ASMM-1 quotes **one side only**; §4.1 says the opposite —
  *inventory never prevents quoting* — and §4.1 is right precisely because we
  are the mandated buyer. Run as shipped there would be **no bid on any book**.
  A $25,000 mark-to-market kill on a book we are mandated to make is a market
  outage, not a risk control; §1.5 excludes profit, so drawdown is not a signal
  we should act on. The kill switch we need already exists (§6.3, operator-
  triggered, through the gateway's `cancel_all`).
- ✂ **Build none of RPV-1 / RPV-2, pending E30.** Three of its four additions
  are **invented movement**: a random OU trend worth up to **$0.80**, a
  continuous random walk, and event jumps. His own header states the purpose —
  *"the reference price sits still and the noise taker just chops around a
  fixed anchor… RPV-1 makes RP MOVE… so the whole market breathes."* That is a
  simulator. ⚠ The event jumps are a substitute for a probability feed **we
  already have**: `x_g` moves on every play, so adding them double-counts. And
  the fourth addition — RP responding to net order flow — is the compliance
  problem, because the house taker does most of the buying on day one.
- ⚠ **His width has no wide end.** The σ² ceiling of 400 caps it at ~10 ticks
  plus the random 3 — about **$0.13 on a $65 team, ever**. §5.2 Defensive is
  $0.40 and the indicated overnight spread is $2.50–$5.00. Worse: **a dead feed
  produces LOW volatility**, so the equation would quote tight into exactly the
  case §2.3 calls dangerous. **Recommendation: per-state width floors** off the
  §3.3/§3.4 freshness ladder, rather than raising the ceiling. → **E31**.
- ✅ **Take his ladder shape, keep our scale and our seeding.** Adopt the random
  level count (3–6), the random 1–4 tick step, and the geometric ×0.72 size
  decay — all of which remove further dependencies on the unbuilt classifier.
  ✂ Reject his 250-share base size (40× too small) and his `random.Random`
  jitter: **§5.7.3's seeded SHA-256 scheme is the fixture we reproduced
  byte-exact and the reason replay works.**
- ⚠ **His dwell timer must not drive a requote on its own (→ N26).** Redrawing
  the whole ladder every 3–12 s in a live game means cancel-and-repost with no
  new information, on 170 securities — a message-budget problem (T2 unanswered)
  and a lifecycle contradiction, since under rest-until-gone it wipes a
  partially-filled level for cosmetic reasons. **Rule: §5.8's material-change
  thresholds remain the gate; the dwell only defines when the shape is allowed
  to change.**
- ✂ **His port obligations, restated because they are the same three every
  time.** All `float` → §1.6-3 makes Decimal authoritative. `time.time()`
  inside the model → §10.3 requires bit-identical replay, so every `Δt` comes
  from event timestamps. `random.Random` → seeded SHA-256 only. Decimal has
  `.exp()` and `.ln()`, so step 2 of the volatility update needs no float.
- ⚠ **SNT-1 as written cannot run on tZERO.** Its entire order model is
  marketable **IOC**, and the venue supports **DAY / GTC / GTD only** —
  verified twice, the platform doc (22-07) and the OE FIX spec (23-07). The
  workaround (a marketable DAY order plus an immediate cancel) breaks SNT-1's
  own stated guarantee that it never posts resting liquidity. → **E32**.
- ⚠ **SNT-1's `max_spread_ticks_to_trade = 8` is narrower than our narrowest
  spread.** §5.2 Stable is $0.10 = 10 ticks. As configured it would never trade
  at all — least of all overnight, the state it was built for. Clean evidence
  the file was never reconciled against the MM spec. → **E32**.
- ⚠ **SNT-1 does not distribute the float, and it would hide that it doesn't.**
  Its flow is 50/50 and price-insensitive, so it defeats the only tool we have:
  a lean works by making our offer attractive, and a counterparty that ignores
  price does not respond. Volume would read healthy while **N20** is untouched.
- ⚠ **SNT-1 decides E17.** At LIVE intensity it crosses **~30,000 shares/hr per
  book** against a 10,000-share L1, and its sweeps cap at 3 ticks while our
  ladder spacing is $0.05 — so **every order lands on L1 only**. Under
  rest-until-gone the top level erodes to nothing over ~40 minutes and reloads
  only when fully consumed. §5.9's replenishment makes it a non-issue.
  **E17 stops being a preference and becomes a correctness question.**
- 🔴 **Two house accounts trading with each other, on a FINRA-regulated ATS.**
  On day one SNT-1's counterparty is overwhelmingly the MM. Common beneficial
  ownership on both sides is the definition of a wash trade, and the 23-07
  rulebook decision prohibits exactly this for users. Concrete: the OMS spec
  has per-account wash-trade blocking, so if T0 treats the two as related the
  prints are simply rejected. **Compliance read, not an engineering answer** —
  same class as S8. → **E33** + **T13**.
- ⚠ **The package disagrees with itself and with its own verification claim.**
  `HANDOFF.md` §3 says the flow impact is 10 ticks per 1,000 shares;
  `RPV2Config` says **6.0**. The package is described as clean-room verified.
- ⚠ **Two findings from his own results, worth reflecting back.** His §7 admits
  teams priced under ~$50 run **negative median MM P&L** — about half the
  universe. And his cohort economics put **retail participants at −$6,100 a
  session** to the house.
- ⚠ **Correction (George, 30-07): our day-one position is NOT a fixed 500,000
  shares a team.** The Mandate is *buy whatever participants do not*, so it
  depends on demand — more or less. 500,000 is the ceiling on the ten-round
  reading of **E24**, not an expectation. ✅ The argument against ASMM-1's
  scale does not rest on it: even a **90 % subscribed** offering leaves ~50,000
  shares a team, still **8×** his one-sided threshold and **4×** his lean cap.
- 📅 **Build status (George, 30-07): roughly halfway, and 80–90 % of the time
  so far has gone on understanding rather than writing.** Three documents, each
  superseding the last. The process fix at the top of this entry is the direct
  response.
- ⭐ **The market cannot move the price, and that is arithmetic (George, 30-07b
  → E34).** A normal market has several **profit-seeking** market makers each
  guessing fair value, and flow moves the price between them. We have **one**,
  explicitly **not** profit-seeking (§1.5), quoting a fixed spread around a
  **model** number. The quote is `RM = RP + IA` and §4.5 bounds `IA` to
  **±$0.25** — so that $0.50 band is the *entire* range in which market
  activity can move the price, **0.5% on a $50 share**. The Mandate pins us at
  the bottom of it on day one: **$0.00 of downward room, $0.25 upward, and only
  if participants buy our whole holding.**
  ⭐ **Corroborated independently: Edwin built RPV-2's invented price drift
  because he noticed his prices did not move.** Two routes, one finding. He
  fabricated movement; the real problem is that nothing real can create it.
  ⚠ **The product consequence is the one to lead with:** users watching prices
  move in the app would be watching our model, not a market — and a participant
  can never be right *early*, only right *at settlement*.
  **This reframes N20: it is not a distribution problem, it is the
  price-discovery problem**, and it is the root cause behind E30 and E35 too.
  Three ways out, of which (2) and (3) are the same fix: accept it as a
  fixed-odds product and stop calling it a market · raise `M` substantially ·
  distribute the float so participants set the price between themselves.
- ⚠ **Inventory is NOT a clean sentiment channel here (George's correction,
  30-07b).** I had argued flow reaches the price through inventory → lean. In a
  normal market maker that works, because accumulating costs money, so the
  markdown is an inference — *"flow is beating me, my price is wrong."* Ours has
  unlimited capital and is **required** to buy, so most of our position carries
  no information about whether our price is right. The mandated position is
  noise sitting on the signal, and it pins the lean before any voluntary flow
  can register.
- 🔴 **The Reference Price definition was reversed and nobody noticed (→ E35).**
  20-07: *"Reference Price = the mid between best bid and best ask."* The v1.3
  spec: the model value, `ROF + ΣGEV + RAV + EAV`. We built the spec's version.
  **The change is recorded nowhere as a decision.** Our recommendation is to
  keep the fair value pure — this security settles at a known number (§11.3), so
  sentiment does not change what a share pays, and chasing flow both destroys a
  correct participant's edge and creates an exploit. ⚠ But that recommendation
  only holds **if E34 is answered by distributing the float**, so the market has
  somewhere real to disagree.
- ✅ **The sentiment-in-RP blend was proposed and WITHDRAWN the same evening
  (30-07, review under Fable).** The idea: `RP = w × model + (1−w) ×
  participant-only price (§5.5)`, `w` falling as volume grows. Killed on three
  findings: (1) the model's forward leg is already **anchored to de-vigged
  sportsbook lines** — a far deeper crowd than our book will ever be, so the
  blend dilutes a strong crowd with a weak one; (2) **resting orders are free**,
  so a §5.5-driven mark is spoofable, and §4.2 marks every portfolio and the
  leaderboard at RP — with prizes attached, someone will; (3) **§2.3 is
  therefore deliberate and correct**, not an oversight. Season 1 collects the
  behavioural tape; any sentiment mechanism is a season-2 question argued from
  evidence. **E34 is asked as product intent only and blocks no build.**
- ⚠ **Two of the E34 claims were overstated and are corrected in the filing.**
  *"A participant can never be right early"* — false: the price moves on every
  result, probability and daily file, so being right pays as evidence lands.
  *"A wrong model is never corrected"* — false: banked results correct it at
  $5 a time, weekly. The true residual claim: **opinion ahead of evidence
  cannot be monetised, and the app shows a model tracking reality, not a crowd
  discovering it.**
- ✅ **The quote assembly is fixed (George, 30-07 evening):**
  `RP → + lean → centre (RM) → ± width/2 → L1 → ± step → ladder`. The lean
  moves the pair and never the gap; the odd tick alternates sides per draw.
  Chapter 5 builds this shape.
- ✅ **Distribution runs on size and depth, not price (George + review).** While
  the mandated position is large: more levels and much larger sizes on the
  offer, fewer and smaller on the bid. Both prices stay fair — no §2.3 issue,
  no §5.4 issue, works under any E34 answer. Needs three InPlay numbers
  (→ E31): the §5.7.3 quantity ceiling (15,000 binds first), the §5.7.2
  modifier range (1.5× is far too small), and §5.2's symmetric level counts
  relaxed.
- 🟡 **The split-position lean is proposed, not built.** `traded = NP −
  OpeningPosition`; sentiment lean on `traded` with a small cap, distribution
  lean on the mandated part with Edwin's cap. **Blocked on E27** — until the
  opening position has a publisher, `traded` cannot be computed. §4.5's
  single-position lean stands in the meantime.
- ▶ **Full rulings, area by area: [[market-maker/asmm1-adoption-spec]]** —
  including the new §0 assembly section.

## 2026-07-30, SNT-1 Synthetic Noise Taker added (Edwin email), [[market-maker/systems/synthetic-noise-taker]]

> Edwin delivered a spec-quality reference implementation (`sources/snt1_noise_taker.py`, ~349 lines) for a **second house agent**. Session note: `sessions/2026-07-30-snt1-noise-taker.md`.

- ✅ **A second house agent, SNT-1, is in scope.** A non-participant, taker-only house account that crosses the spread with random sizes at random times so every team book trades from IPO onward, including with no games on. It complements the MM (maker); SNT-1 is the taker.
- ✅ **Deliberately a controlled loser.** Its spread cost is the subsidy that seeds an active secondary market. Not trying to move price toward any target; flow is pure noise.
- ✅ **No off-field-split spec amendment needed.** SNT-1 prints against the MM carry zero participant sides, so they are excluded from the $2.50 off-field volume split under the existing >= 1-participant-side rule. `leaderboard_eligible = false`, so no leaderboard credit.
- ✅ **Design locked at v1.0** (all numbers in [[market-maker/parameters]], status 🟡): Poisson arrivals, log-normal sizes (5 to 400, median ~30), 50/50 direction, ~90% at-touch IOC (<= 50% of touch) / ~10% sweeps capped at 3 ticks through touch, intensity `base 9/hr x state x team_weight` (LIVE 75x), $100k per-team daily loss governor (metered cost-vs-mid), disposition-effect profit-take tilt (0.50 -> 0.65, losers ride at 50/50), 1,500-share inventory soft cap (80% flatten bias), taker-only, hard guards (no halted/locked/crossed/one-sided/RP-freeze/>8-tick books).
- ✅ **Account flags on the gateway:** `account_type = HOUSE_SYNTHETIC`, `leaderboard_eligible = false`, `participant_side = false`.
- ⚠ **Two levers to tune after real books:** `base_orders_per_hour` and the loss budget (Edwin).
- **Our side (not Edwin's):** implement the `ExchangeAdapter` against the matching engine, plus the five production-hardening tasks (kill switch + logging + per-order notional cap; persist pos/basis across restarts; periodic position reconciliation with halt-on-divergence; IOC limit enforcement as the impact cap; `activity_state()` mapping). See [[market-maker/open-questions]].

## 2026-07-30 — the spec filter · Chapter 4 built

- ⭐ **The spec's finance is authoritative; its engineering is AI scaffolding
  (George).** The v1.3 spec was written by a domain expert in finance who does
  not code, using AI. So: formulas, settlement, the skew mechanics, the
  de-vig, $5 a win — his own domain, defer to them. Event types, idempotency
  tables, journal design, replay architecture — generated, so **judge on
  merits rather than obeying**. ⚠ Judge, not ignore: some scaffolding has
  proved load-bearing. §7.3's per-game keying exposed the adapter bug that
  left half the universe unpriced, and §7.2's lifecycle ordering settled
  where rejection belongs. This filter is narrower than the 22-07
  platform-doc one and applies to the build spec itself.
- ✅ **Chapter 4 is built.** `position.py` (§4.1 net position, §4.2 average
  cost and P&L) · `inventory.py` (§4.3 float and ratio, §4.4 pending
  exposure, §4.5 the skew, §4.6 Reservation Midpoint) · `position/engine.py`
  (fills in, positions and skews out). **171 tests**, ruff and mypy strict
  clean.
- ⚠ **The Reservation Midpoint goes negative without §4.6's floor.** §4.6
  says RM "must remain within the price boundaries of §5.4" and that is
  load-bearing, not decoration: §5.4's floor is $0.01 and the skew reaches
  −$0.25, so `RP $0.10 + IA −$0.25 = −$0.15`. A team late in a losing season,
  priced near the floor, with us holding most of its float — not a contrived
  case. `reservation_midpoint()` clamps, and a clamped RM is worth noticing
  because it means the skew is asking for something the price cannot deliver.
- ✅ **The Position Ratio is deliberately NOT clamped to ±1.** v2 lets
  participants short the full float, so what can be sold to us is float plus
  short interest, and §4.1 imposes no inventory limit. A ratio above 1.0 is a
  state the spec permits (**E26**); clamping it would hide exactly the
  situation we would most want to see.
- ✅ **A fill for an untracked security RAISES**, deliberately the opposite of
  the valuation engine's silent skip. An unknown *team* is a legitimate §2.5
  boundary — NCAA sides play FCS schools with no Team Company. An unknown
  *fill* has no such story: we only receive execution reports for orders we
  placed, so it means the universe is wrong or we traded something we cannot
  price. Either way we hold inventory that never skews.
- ✂ **`IPO_ALLOCATION` and `CORPORATE_ACTION` are not built (George).** The
  opening position arrives as a constructor argument instead — same status as
  the RAV/EAV mocks, and replay still reproduces it. §7.3 reserves both event
  types but nothing sends either (**E27**, **E28**). Build them when we know
  what actually arrives rather than guessing. ⚠ I first argued the v2 dates
  force an overlap between the primary and the secondary; re-reading, §1.1 is
  clean and the overlap appears only from §2.1 + §5.2 together — drafting
  sloppiness, not intent. Conceded.
- ✅ **Realized P&L is emitted per fill and never accumulated.** A running
  total is derived state — the thing §2.5 prohibits, and the thing that caused
  the double-banking defect. A consumer sums the records; replay reproduces
  the total exactly.
- ⚠ **Average cost is a division, so it recurs.** `$23,000,000 ÷ 450,000`
  cannot be held exactly, so the unrealized P&L lands 5 x 10⁻²² from a round
  number. Not a defect — it is why §1.6-3 says round only where the algorithm
  says to. **Never compare an average cost against a hand-written literal.**
- ✅ **Comments move to a `# Notes` block at the end of each file (George).**
  Inline density was making the code unreadable. Short marked line inline,
  long form at the bottom keyed by a **named** marker — names survive edits,
  numbers drift. Nothing is deleted when a comment moves; it is relocated.
  Applied to all ten source files; repo `CLAUDE.md` rewritten so it holds.
  Tests are the exception — there the comment IS the statement of behaviour.
- ⭐ **Wins are conserved, and the feed does not conserve them (George).** 32
  NFL teams x 17 games = 272 games, so the 32 expected-win figures must sum to
  **272**. Real BetMGM lines sum to **275.00**; after the de-vig, **273.95**.
  The de-vig removes a third of the excess, but Edwin's rake works per team
  and nothing enforces the league total. Worth **$0.30 a share**,
  one-directional — every NFL name slightly high, never low — and we are the
  mandated buyer of the residual float, so ≈**$8.6 M**. **George's call
  (30-07): minor, park it as a question (N25) rather than act on it.**
  ⚠ NFL only — NCAA teams play FCS opponents outside the 170, so their wins
  legitimately exceed games ÷ 2.
- 🔴 **Two of §4.1's four inputs have no publisher.** Buys and sells arrive as
  fills and that path is built and QA'd. The **opening position** (**E27**)
  and **corporate adjustments** (**E28**) have nothing sending them. E27 is
  now the second-priority open question: v2 makes us the buyer of all
  remaining shares, so it is the entire day-one book.

## 2026-07-29b — the on-field leg built · the window is kickoff → the next T

- ✅ **The on-field leg is built.** `on_field_value()` in
  `mm/valuation/reference_price.py`, with `KickedOffGame`. 70 tests, ruff and
  mypy strict clean. Edwin's three stated unit tests plus four more: the
  in-play cancellation trap, the tie as half a win, two games netted, and the
  two sides of one game cancelling.
- ✂ **It supersedes §3.1.1's on-field terms** (`ROF + Σ GEV(g)`) with
  `$5 × (T − Σ p_ref(g) + Σ x_g)`. Authority: this log outranks the spec, and
  Edwin confirmed the formula on 28-07. **E23** — how his composition maps
  back to §3.1.1 — stays open. `RAV`/`EAV` are untouched.
- ⭐ **The adjustment window is kickoff → the next T, NOT kickoff → the final
  whistle (George's catch).** Verified with numbers: Chiefs T 11.6, p_ref
  0.566. They win, and if the adjustment stops at the whistle the price
  **drops $2.17 for winning**, then jumps back when the 06:00 file lands. A
  sawtooth every Sunday evening. Edwin's unit test (c) exists for exactly
  this: *"after the final whistle, it holds at banked-plus-expected until the
  next T arrives."*
- ✅ **Membership of G is a timestamp comparison, never a judgement.** Compare
  each game's kickoff time against T's `effective_time`:

  | Game | T holds it as | In G? |
  |---|---|---|
  | kicked off **before** T | a banked fact | no |
  | kicked off **after** T | a probability | **yes** |
  | not kicked off yet | a probability | no |

- ✅ **An upcoming game needs no adjustment** — it is already inside T, and
  T's guess is still the best one we have. This is why the adjustment starts
  at kickoff and not before.
- ✅ **A played game needs no probability** — `x` is the result: 1, 0.5 or 0.
  Only a game in play needs a live number. A loss moves the price **down** by
  `$5 × p_ref`, so a favourite losing costs more than an underdog losing.
- ✅ **With a healthy feed, G holds 0 or 1 games.** A team plays once every
  4–7 days and T lands daily. The set form Edwin required is purely the
  missed-file case — kept, because a missed file otherwise loses a real win
  from the price silently.
- 📅 **Kickoff time is now load-bearing.** The G membership test needs it, and
  the adapter currently discards it. **Fix-pass step 4 is a dependency of
  pricing, not a tidy-up.**
- ⚠ **Edwin's definition of `p_ref` disagrees with his own unit test (a), and
  we build the definition (George, 29-07b).** He defines `p_ref` as the
  pregame probability *"frozen at the moment T was ingested"* (06:00 ET), but
  test (a) requires the leg to equal `$5 × T` **at kickoff**, seven hours
  later, which only holds if `p_ref` is the closing number. Worked example:
  Chiefs T 11.6, 06:00 probability 0.566, kickoff 0.540 → the definition
  gives $57.87 and the test expects $58.00, a **13¢** gap. Freezing at
  kickoff instead leaves that 13¢ of pregame news out of the price until the
  next file. **Ruling (George): freeze AT KICKOFF — the closing pregame
  probability.** Edwin's own fallback clause already permits it, it makes his
  test (a) exact rather than approximate, and it needs no probability held
  from 06:00. The 13¢ of pregame drift stays inside T until the next file;
  that is the accepted cost. **Asked anyway → N22.** One line to change on
  his answer.
- ✅ **A tie is a terminal state, not a live probability (George).** Sportradar
  gives a two-way market and no tie probability exists (S6), so `x` is simply
  the live win probability while the game is in play, and becomes 1, 0.5 or 0
  once final. The 0.5 appears only at settlement. Do not blend a tie
  probability into the live number — there is no such number to blend.
- ✅ **Assume at least one T always exists (George).** T is required at
  construction rather than optional, so a "no price yet" state cannot occur.
  Edwin's rule already guarantees it operationally: a missing daily file is an
  alarm and we hold the last value.
- ✅ **A stale T is repairable, even weeks later.** Sportradar's timeline
  endpoint returns a game's whole history, so a pregame probability we failed
  to capture at kickoff can still be recovered.
- ✅ **Do not smooth on a new T** (reconfirmed). Edwin: *"a discontinuous
  repricing reflecting newly available information, not market-maker
  behavior."* Expect the new T to land near, but not exactly on, our adjusted
  number — his is the whole season rebuilt from his ratings, so other results
  moved it too. Widen quotes around the 06:00 window if we want cover.

## 2026-07-29 — IPO Requirements v2 · the gospel ruling · the deadline moves

- ✅ **Authority ruling (George): IPO Draft Business Requirements v2 (28-07)
  and `reference/season-win-totals-170.csv` are gospel.** Where either
  conflicts with an email, a spreadsheet or the IPO Supplement, they win. This
  settles three things immediately: **NFL float is 900,000** (not the 875,000
  in Edwin's email of the same day) · **§5.2.3 means NCAA**, 1,000,000 shares
  available for shorting · the **Washington Commanders DraftKings line
  stands**, so its IPO price is the price.
- 📅 **The deadline is secondary trading, not the season.** NCAA secondary
  opens **26 or 27 August** (v2 disagrees with itself — E25), NFL on
  **7 September**. The market maker must be quoting from the earlier date,
  about four weeks out. Every earlier plan assumed the season start.
- ✅ **The market maker buys ALL remaining shares, not 85%** (v2 §4). This
  **supersedes spec §9.2**'s `floor(0.85 × UnsoldShares)`. Closes E20.
- ✅ **InPlay Markets is the exclusive seller in the primary** (v2 §2). The
  market maker is a **buyer only** during the offering. Participants may buy
  only — no selling and no shorting until secondary opens.
- ⚠ **Shorting is new and unbounded** (v2 §1.2, §5.2). The full float may be
  sold short in the secondary market. So what can be sold to us is float
  **plus** short interest — 2,000,000 rather than 1,000,000 for an NCAA team.
  §4.3's Position Ratio can exceed 1.0, and §4.1 imposes no limit. → E26.
- ⭐ **The reason to distribute is liquidity, not profit or risk (George).**
  §1.5 excludes profit as a motive and the market maker has unlimited money,
  so the usual reason to shed inventory does not apply. The real reason is
  that **a market with no shares in circulation is not a market** —
  participants have nothing to trade with each other, and §3.6.3 excludes
  market-maker volume from the off-field value, so our own trading cannot
  feed the Popularity Index either. **That reframes the inventory skew as our
  distribution tool rather than our risk tool.**
- ⚠ **And the skew has no room left.** §4.5 caps it at $0.25, which binds once
  we hold 25% of the float. After the offering we hold 50–100%. Verified:
  holding the entire NFL float reads **identically** to holding a quarter of
  it. The only tool the spec gives us for the thing that actually matters is
  saturated from the first minute. → N20.
- ✅ **The fix pass is complete.** All four defects from the 27-07 review are
  fixed and merged (PRs #1, #2, #3). 63 tests. One new defect (#5, the
  `GameStatus` coverage flag) is recorded and open.
- ✅ **Nothing blocks the build.** The spec covers Chapters 3–8 in full. Only
  §5.9 replenishment is genuinely blocked, because **E17** is a mechanism
  question and not a value. Two data gaps — the schedule (§3.6, §2.5) and the
  live feed — do not stop us writing code today.

## 2026-07-28 — Edwin's answers to all six questions ([[standards/MM-edwin-answers-28-07|email]] + code + IPO Supplement)

- ✅ **Expected wins, not per-game probabilities — but never the raw posted
  line.** De-vig both sides, then `mean = line + σ_mkt × InvNorm(fair over)`.
  σ_mkt is a league constant: **2.7 NFL, 2.2 NCAA**. Worked example verified
  against his code to 4 dp.
- ✅ **`T` is whole-season** — banked wins included — which is exactly why the
  formula subtracts. The published feed field is the opposite: **remaining
  games only**. Both, deliberately; his definitions block governs.
- ✅ **Our double-count fix confirmed, and generalised.**
  `$5 × (T + Σ(x_g − p_ref(g)))` over **G, a set** of games kicked off since
  T's timestamp. A game **enters at kickoff and stays until a new T absorbs
  it** — so the adjustment survives the final whistle. Building it for a
  single live game (as I first did) loses the win until the next publication.
- ✂ **Do not smooth the mid** when a new T lands. *"The price change… is a
  discontinuous repricing reflecting newly available information, not
  market-maker behavior. Smoothing it would mean quoting a price you know is
  wrong."* Widen quotes around publication windows instead.
- ✅ **College is his, not Sportradar's** — MOV-capped Elo, calibrated weekly
  against SR's posted pregame probabilities; NFL raked so remaining-game
  probabilities sum exactly to the de-vigged sportsbook total. Published as a
  **daily 06:00 ET JSON file, all 170 teams every file**, heartbeat even when
  unchanged, **a missing file is an alarm**. `team_id` is Sportradar's
  competitor ID — no mapping table. **Closes S10.**
- ✅ **Ties: price the two-way market as proposed; settle at 0.5 → $2.50.**
  Closes S6. The ~0.4 % drag is a reserve, not a model.
- ✅ **IPO: `price = EV − discount`, and RP seeds at EV, not the listed
  price.** Frozen T-3, full precision, never revised. ⚠ The Supplement (§8,
  Open Item 10) had this **[OPEN]** and warned it gaps every discounted name
  1–3 % at the open with the MM as counterparty — the email decides it
  anyway, so that is now an *accepted* day-one exposure.
- ⚠ **Conflicts opened, not resolved:** **E20** §9.2's `floor(0.85 × Unsold)`
  vs the Supplement's MM Primary Mandate (buy *all* remaining, Rounds 1–10,
  up to 85 M shares) · **E21** his own two IPO implementations disagree on the
  tie leg, the Bradley-Terry inputs and the discount scaling, and the
  acceptance test is unrunnable without `teams_config.py` + `odds.csv` ·
  **E22** issued share count still missing, which blocks all of Chapter 4 ·
  **E23** his "retained earnings + on-field + ad accrual" composition vs
  §3.1.1's `ROF + ΣGEV + RAV + EAV`.
- ⚠ **His code is all `float`.** §1.6-3 makes Decimal authoritative, so
  `TeamPricer` and `validate_records()` must be **ported, not lifted**,
  despite the email's "lift it verbatim". Formulas port cleanly; only types
  change.
- 📅 **Dates now bind us:** NCAA freeze **19 Aug**, NCAA offering **22–28
  Aug**, NFL freeze **2 Sep**, NFL offering **5 Sep**.

## 2026-07-27/28 — Build review + the expected-wins insight (George + Claude)

- ✅ **A probability reading is a fact about a GAME, not a team — one event,
  both securities.** §7.3 keys a probability update on Source + Game +
  Provider Sequence with **no team component**, so per-team events collide:
  same key, different payload, and the acceptor correctly refuses the second
  as a conflicting duplicate. Proven on the real Chiefs–Ravens timeline —
  1,089 accepted, **1,089 conflicts, and the Ravens never priced at all**.
  The adapter now emits one side-neutral envelope per reading and the
  valuation engine fans it out. ⚠ **Spec tension to raise:** §3.2 describes
  a probability input record as carrying a single *Team Company ID*, while
  §7.3 keys the event per game. We implement the §7.3 shape because it is
  the normative table and the only one that works.
- ✅ **The pairs identity is a hard invariant, not a comment.**
  `GEV(home) + GEV(away) = $5.00 × (P_home + P_away + P_tie) = $5.00`,
  always. Enforced in the engine and checked **before** any state is
  written. Verified exact across 5,948 normalized triples, so a mismatch is
  never a rounding artefact — it means swapped sides or a broken §3.2.1
  repair. §2.3: wrong quotes are worse than no quotes, so it raises.
  (George's call: he asked for a belt-and-braces check; double-validating
  the *input* was measured to be a no-op — 0 disagreements over 1,001
  splits — so the check moved to the *output*, where it catches things
  double-validation never could.)
- ✅ **The universe map must be complete or we refuse to start.** A missing
  team entry was previously indistinguishable from a legitimate non-universe
  opponent (NCAA sides play FCS schools with no Team Company) — both simply
  produced no price, silently, forever. Construction now rejects any
  security the map cannot reach. (George spotted this.)
- ⭐ **RP needs expected WINS, not per-game probabilities.** Every win pays a
  flat $5, so `Σ GEV(g) = $5.00 × Σ P_win(g) = $5.00 × expected wins` — the
  per-fixture breakdown cancels out entirely. Collapses E19's requirement
  from ~2,400 game probabilities to **170 numbers**. (George's insight.)
  Sent to Edwin 28-07 as a proposal, not adopted unilaterally: it is
  arithmetically identical to §3.1.1 but not what §3.1.1 writes.
- ⚠ **Keep the three-term structure even though it collapses.**
  `W×$5 + p_live×$5 + tail×$5` is algebraically `$5 × T`, but the first two
  terms are *facts* and only the third is an estimate. Collapsing it makes
  the price track the bookmaker's opinion about games we already know the
  result of, and stops it hardening as the season resolves.
- ⚠ **The in-play cancellation trap (verified).** Season win totals are
  futures markets and are never repriced during a game. Subtracting the
  *current* live probability from a frozen whole-season total cancels the
  in-game movement exactly — the price sits at $60.00 whether the team is at
  60% or 90%. **Fix:** at kickoff the game leaves the tail carrying its
  *pre-game* probability, and the tail freezes for the game's duration.
- ✅ **HOW-IT-WORKS.md is the explainer, BUILD-LOG.md is the status.**
  Concepts in one, state in the other, and the boundary is stated in the
  file so they don't drift into each other and become untrustworthy.
- ✅ **`inplay-market-maker` now has a remote** —
  `Novosapien/inplay-market-maker`, private. Two days of work had existed on
  one disk.

## 2026-07-24 — Friday touchdown (Edwin + Cody + Troy + Kevin + Novo) — [[24-07-2026-touchdown]]

- ✅ **Probabilities ride SR's betting-side feed (Cody).** SR's licensed
  *media* data feeds power the gamecast; SR's own hosted match-tracker widget
  runs on *betting* data — faster, but the raw betting feeds are licensed to
  sportsbooks only and unavailable to InPlay. The **probabilities API is off
  the betting feed** and updates faster than media events — so the MM (which
  consumes the probability, not the event) is not disadvantaged: in-app users
  see events at the same moment the MM does. Edwin's ruling: use the fastest
  feed available for everything; must never lag the sportsbooks (S4
  mitigated). Cody lobbying SR for the betting feeds in parallel.
- ✅ **MM monitoring dashboard — phased, read-only first (Edwin ask).** An
  InPlay person monitors the market as we near production. Phase 1: see the
  backend working — positions/holdings ("how many shares it owns of PMX Y"),
  variables visible but static. Later: changeable variables for an active
  trade. Explicitly NOT about changing MM logic. George: the MM is just
  another user — the **same inventory/portfolio APIs that serve users serve
  the dashboard**. Feeds [[market-maker/systems/mm-ops-ui]].
- ✅ **SR entitlement channel agreed:** George emails the blocked
  products/versions to SR support + Scott + Cody (→ S7); Cody drives with
  Scott + David. Master-key model; call limits + versioning claimed moot at
  the real-time tier.
- ✅ **E19 reinforced:** Edwin re-affirmed he builds the remaining-season
  probability model internally ("I'll come up with a piece that you can
  pull"); weekly manual input via the MM platform floated. "We'll work that
  out over the next few days."
- ✅ **NCAA IPO prices in motion (E3):** Cody delivered the NCAA totals;
  Edwin pushing updated IPO prices into the app same day.
- ✅ **Trading launch anchor:** trading functionality live for **~Aug 22**
  (Troy: "we need to get this live for the 22nd"); the KYC-less academic
  variant is deliberately deprioritised behind it (needed ~first week of
  September).

## 2026-07-24 — Gateway: everything the MM needs is BUILT (Hasan, second report)

> Supersedes the earlier same-day entry. All five asks **plus both
> nice-to-haves** are built and deployed; what remains is a cert pass, not a
> build. Deployed code runs **ahead of the pushed `origin/main`** we fetched —
> build to the contract below and reconcile when the code lands.

- ✅ **Cancel (35=F) + cancel/replace (35=G) LIVE** (`33bf32a`), verified
  against **real tZERO QA**: cancel acked `150=4` solicited ~12 ms, replace
  acked `150=5` ~11 ms. Intake `gateway.orders.cancel`. The **caller mints
  the ClOrdID**; the gateway fills 55/54/38 from tracked state (35=F must
  carry the original OrderQty). Replace publishes `ORDER_REPLACED` on **both**
  the old and new subjects, so consumers keyed on either id stay consistent.
  GTD expiry inherited on replace unless overridden. `HandlInst(21)="1"` set
  on G — the venue requires it there while rejecting it on D (**verified in
  the OE spec, see below**).
- ✅ **Dead-man switch built + deployed, OFF** (`MM_ENABLED=false` **until our
  bot exists — we are now the gating item**). Needed an unlisted
  prerequisite: a **Redis open-order index**, because after a gateway restart
  the in-memory tracker is empty and 35=F can't be built without the original
  OrderQty. Shape: heartbeat silence **4 s** → rate-paced 35=F sweep,
  `Text(58)="deadman"`, **latched** (a bot down an hour produces one sweep,
  not one every 4 s), armed at boot so a restart rehydrating orphaned MM
  quotes is covered. Exercised end-to-end against the mock venue; **not yet
  against real tZERO** — cert item.
- ✅ **Tag 60 passthrough LIVE** (`e845721`): `source_timestamp` now carries
  tZERO's `TransactTime`, parsed across second/milli/micro variants, with the
  gateway clock as **fallback rather than the answer**. Unit-covered; not yet
  eyeballed on live venue traffic (cert item). → our envelope's
  `provider_event_time` is real for venue events.
- ✅ **Rejection NAK LIVE:** every validation failure on
  `gateway.orders.new` publishes `ORDER_REJECTED` with `local:true` + reason
  (`INVALID_CLORDID`, `UNKNOWN_SYMBOL`, `INVALID_SIDE`, `INVALID_QUANTITY`,
  `INVALID_PRICE`, the GTD/TIF family, `SESSION_DOWN`, `SEND_FAILED`).
  **No guess-by-timeout.** ⚠ Requests missing `userId`/`clOrdId` remain
  log-only — no subject exists to reply on.
- ✅ **MM namespace deployed (off):**
  `gateway.orders.mm.{new,cancel,replace,heartbeat,cancel_all}` on its own
  queue group, so MM churn can't starve retail intake. Token-bucket governor
  + **ClOrdID prefix partitioning enforced both ways** — MM traffic must
  carry the prefix, retail must not, else the dead-man's notion of "an MM
  order" isn't trustworthy. Gateway's NATS user already has
  `subscribe: ["gateway.>"]`; **only our bot's user needs an ACL change**.
- ✅ **At-least-once ON** for `order.*` / `position.*`: publish-with-ack,
  `Nats-Msg-Id` dedup, bounded retry, then a **Redis dead-letter rather than
  a drop**. Verified in production (0 retries, 0 dead-letters, core
  subscribers unaffected). **Market data deliberately stays on core NATS** —
  "a stale quote is worthless, a lost fill is a support ticket."
- ⚠ **Correction to our earlier note:** "the publisher drops on queue
  overflow" was accurate but incomplete — it also used fire-and-forget
  `nc.Publish`, so a message could be lost *without* the queue overflowing.
  The dropped counter never left zero; the real exposure was the un-acked
  publish.
- 🟡 **Remaining = cert pass, not build:** does tZERO accept `Text(58)` on
  35=F · pin the placeholder **50 msg/s governor** and **4 s dead-man
  window** against tZERO's session-throughput guidance · exercise the sweep
  against the live venue with a hand-rolled heartbeat publisher.

**Consequences for the MM build (new obligations on us):**

- ✅ **We must publish a heartbeat** on `gateway.orders.mm.heartbeat` faster
  than the dead-man window, or our own book gets swept. New requirement for
  the venue-sync engine (spec Ch 8).
- ✅ **Our ClOrdIDs must carry the MM prefix** (gateway convention) *and* obey
  the venue's ≤20 chars / no-leading-zeroes. **George 24-07: the ID scheme is
  fine** — 18 chars after the prefix is ample. Real constraint is that IDs be
  generated **deterministically**, so replay reproduces the same chain.
- ✅ **`cancel_all` is our kill-switch mechanism** — spec §6.3 (global kill
  switch → Suspended → "initiates cancellation of cancellable orders") now
  has a real implementation to call.
- ✅ **Duplicate fills are now possible by design** (at-least-once). Our
  §7.3 execution idempotency (venue + ExecID) moves from speculative to
  load-bearing.
- ✅ **Peak messaging is not a concern (George, 24-07)** — the 50 msg/s
  governor is Hasan's placeholder, not a venue limit; diff-based publishing
  is an optimisation, not a requirement.
- ✅ **Heartbeat cadence + dead-man window are OURS to set (George, 24-07)** —
  "we can update the code ourselves if we need." Decide from the real cycle
  timing once venue sync exists; don't inherit the 4 s placeholder by default.
- 🔴 **New ask:** NATS ACL for the MM bot's user (publish on
  `gateway.orders.mm.>`).

## 2026-07-24 — tZERO OE FIX spec re-verified (against the PDF, not memory)

- ✅ **ClOrdID = max 20 chars, NO LEADING ZEROES** — stated identically on
  35=D, 35=G and 35=F. ⚠ **Replace and cancel each carry TWO ids** —
  `ClOrdID` (new) + `OrigClOrdID` (superseded) — **each** capped at 20. Every
  replace mints a fresh id, so the chain is a sequence of ids, not one id.
- ✅ **`HandlInst(21)`: "Currently not supported" on 35=D · "Y — value is
  always 1" on 35=G.** Hasan's handling verified exactly.
- ⚠ **The OE spec contains NO rate-limit language whatsoever** (no msg/s,
  throughput, throttle or `MaxOrdRate`). **T2 is therefore unanswerable from
  documents** — `MaxOrdRate` is a per-account OMS configuration tZERO applies
  at account creation, so it must be asked **with T1**, in the same
  conversation.
- ✅ **MM data consumption (George):** the MM subscribes to the gateway's
  NATS streams (fills, positions, top-of-book, status) — no second tZERO
  session in v1; the dedicated MM FIX session stays a filed T0 ask. The MM
  subtracts its own resting orders from the feed to get the §5.5
  participant-only book.
- ✂ **Watchdog/supervision descoped from the MM (George, 24-07):** trade
  busting — and its detection — is tZERO's remit; consistent with the v1.3
  spec, whose six-engine pipeline has no supervision engine. Residual: T4
  keeps the ask to confirm T0 *detects* out-of-band trades, not just executes
  busts. The public trade stream remains consumed later only for §3.6
  off-field volume counting.

## 2026-07-24 — SR ingestion research (code + live API + SR docs via MCP)

> Question asked: could the MM ride SR's **push stream** (→ worker →
> Centrifugo) instead of polling, for lowest latency?

- ✂ **There is NO probabilities push feed — for any sport.** Verified four
  ways: the push message schema carries no probability field; 414 captured
  push messages across six fixtures contain zero matches for "prob"; the
  published live contract has none; and SR's own docs list the *only* push
  products as **Events, Statistics, Draft Picks, Draft Trades, Pulse** (NFL)
  and **Events, Statistics** (NCAA). Searching **every** SR spec for
  `subscribe` returns nothing outside the events streams.
  **Probabilities are REST-pull only. Full stop.**
- ⚠ **CORRECTION — probability update cadence.** Previously recorded (S5 +
  the 24-07 entry below) as *"per play, ~30–40 s"*. **That is wrong by an
  order of magnitude.** Measured from our own captured Chiefs–Ravens
  timeline: **median gap 4 s**, mean 11.5 s, p90 28 s; **64 % of updates
  within 5 s**; **1,089 updates across ~160 plays** (≈6–7 per play) because
  live win probability decays with the game clock, not only on plays; 1,070
  of 1,088 were genuine value changes, not restamps. **Consequence: a ~2 s
  poll is justified as *matching the median update interval*, not as
  oversampling. A 30 s poll would miss ~92 % of the movement.** (Caveat:
  `last_updated` is SR's own stamp and excludes network lag; the retro
  timeline is an upper bound on what a live poller can observe.)
- ✂ **Centrifugo is the wrong plane for pricing** (and carries no
  probabilities anyway): the `game` namespace runs **history OFF** →
  at-most-once with **no server-side recovery**; the documented recovery path
  is "re-fetch the snapshot and compare `seq`" — i.e. a fetch, which the MM
  hot path forbids. Plus per-user HS256 auth and a user-facing blast radius.
  **Centrifugo shows users the probability; the bus feeds the pricing.**
- ✂ **The SR service's Redis probability keys are unusable** — TTL
  cache-aside artefacts populated only when a user hits the API (3 min single
  / 30 min bulk), refreshed by nothing. Also: the SR service has **no
  internal bus at all** (no NATS, no Redis pub/sub) — Centrifugo HTTP publish
  + Redis writes are its only fan-out.
- ✅ **Poller architecture confirmed** (corroborates the 24-07 decision
  below): poller at the Approved-Data-Sources edge, ~2 s per live game,
  writes MM memory + publishes to the bus; hot path never fetches. Reuse the
  SR client + the **already-entitled, already-working** ID bridge as a
  library. Switch to the **v2 bulk live endpoint** the moment S7 lands (all
  live games in one call — ~0.5 QPS vs ~20 QPS peak per-game on an NCAA
  Saturday). ⚠ v1 has **no** bulk-live endpoint.
- 🔴 **Official results have no source today.** Nothing publishes "game X is
  final" onto any bus, and the §3.1.3 expected→realized swap depends on it.
  Scope it with the same poller — one worker, two publications. → N15.
- 🔴 **Two new risks raised (→ S8, S9):** SR's AF Probabilities docs state
  *"For media use only… prohibited for betting clients"*; and the SR
  service's own latency research puts Probabilities on the **media** tier
  (~5–15 s) which **contradicts Cody's 24-07 report** that it rides the
  betting feed. Both cannot be true, and which holds decides whether users
  can pick the MM off (S4).

## 2026-07-24 — MM build started (`inplay-market-maker`, Python)

> Working mode: step by step with George — each step states what we're
> writing, why, and which spec sections to read. Commits on `main`.

- ✅ **Foundations built + tested (48 tests, ruff + mypy --strict clean):**
  decimal policy rejecting floats at the door (§1.6-3) · the §5.7.3 quantity
  golden fixture reproduced byte-exact · event envelope (§7.1) with immutable
  records, canonical UTC-Z, payload hashing · idempotency keys (§7.3) ·
  append-only fsync'd journal + acceptor (§7.2/§7.4) with dedupe,
  conflict detection and restart recovery · Reference Price formula (§3.1) ·
  probability validation bands (§3.2) · valuation engine wiring.
- ✅ **Replay equality demonstrated on real data** (§10.3): the actual
  Chiefs–Ravens 2024 opener (1,089 SR probability points) priced end-to-end —
  kickoff $2.83 → final whistle $5.00, never outside $0–$5 — then rebuilt
  from the journal alone to an **identical** price stream.
- ✅ **SR adapter is a pure translator** — it never calls SR. Polling belongs
  to a separate (unbuilt) poller; the adapter takes parsed data, so file
  replay and live polling share one proven translation path.
- ⚠ **Two interim mappings, flagged in code:** `last_updated` stands in for
  the provider sequence SR doesn't supply (→ D-2; verified 1,089/1,089
  unique on real data, zero collisions) and `p_tie = 0` treats games as
  tie-impossible (→ S6). One line each to change on ruling.
- ⚠ **Float discipline extends to the border:** SR JSON is parsed with
  `parse_float=str`, so a binary float never exists anywhere in the pipeline.
  The live poller must use the same parse (not `response.json()`).

## 2026-07-24 — v1.3 Build Spec intake · tZERO confirmed · SR probability probe

> Sources: `InPlay_Market_Maker_Build_Specification_v1.3_FINAL.docx` (InPlay,
> "release-final for Novosapien"), mirrored at `standards/MM-build-spec-v1.3.docx`
> + `.html` rendering · live SR API probes (24-07, trial Probabilities key) ·
> codebase research on `inplay-sportradar-service` + `sportradar-futures`.

- ✂ **The v1.3 Consolidated Build Specification is the working baseline.**
  It declares itself the single authoritative engineering spec for MM v1 and
  supersedes the CTS/PTS standards for implementation. Adopted (George, 24-07)
  with one carve-out: the three spec-vs-call conflicts below are NOT silently
  adopted — they go to Edwin/InPlay as written blocking questions (E17–E19).
- ✅ **E11 answered — settlement:** `FSV = realized on-field + realized
  off-field` (§11.3). $5/win, $2.50/tie, $0/loss over the regular season only;
  postseason worthless. Longs receive FSV, shorts pay it, positions zero out.
- ✅ **E12 answered — NCAA in:** 170 securities (32 NFL + 138 NCAA D-I),
  evaluated 24 h/day (§2.5).
- ✅ **E1 answered:** $5.00/win both leagues + **new $2.50 tie value**
  (§3.1.2). InPlay-authored release-final doc = the sign-off.
- ✂ **Off-field redefined** (supersedes the 23-07 "popularity index ~$14–30"
  description): **$2.50 per-game pool split by counted trading volume** (§3.6);
  expected side from the BDI/VMI popularity blend; ceiling = games × $2.50.
  Confirms the sheet decode: NFL cap $85 + $42.50 = **$127.50**.
- ✅ **All pricing numbers landed (E5):** spreads $0.10/$0.20/$0.40 by state,
  levels 3/2/1, sizes 10k/7.5k/5k, skew S=$1.00 · cap M=$0.25 — most marked ▸
  proposed: mechanism mandatory, value pending InPlay approval (§12.2, Ch 14-A).
- ✅ **Skew denominator (E14):** Reference Float = issued − treasury (§4.3).
- ✅ **Venue = tZERO — confirmed by George (24-07)** (spec open item C-1
  answered on our side). The "Matching Engine ICD" is effectively the tZERO
  FIX specs mined 23-07 — C-2/C-3/C-4/C-9 already answered there; message-rate
  limits (C-7 = T2) stay open.
- ✅ **The reconciler is back:** §8.1 mandates venue sync by diffing the target
  book against the confirmed book and issuing minimal instructions — the
  shelved 22-07 reconciler design is now the required shape.
- ✅ **Replay harness first** (§1.6-4). The §5.7.3 SHA-256 golden fixture was
  reproduced locally, byte-exact (VF = 1.2433331614).
- ⚠ **Three conflicts held open — NOT adopted either way (→ E17–E19):**
  1. §5.9 fill replenishment (top up below 50 % after 15 s) vs Edwin's 23-07
     "rest until gone, no top-ups ever".
  2. §3.1.4 2.0 s sweep + 5 s-fresh-is-Current vs Edwin's "~200 ms — a
     second's too long".
  3. §1.5 excludes internally-generated probabilities vs Edwin's 23-07
     "InPlay produces remaining wins internally, weekly" — now with proof the
     spec's D-1 is unsatisfiable as written (see SR probe below).
- ✅ **SR probe results (trial key, 24-07):**
  - The standalone Probabilities product **works on the trial key** (200s) —
    the 403 story was key placement, not entitlement death. S1 downgraded;
    production key/quota still needed.
  - **2-way market only — no tie probability exists** in the product. The spec
    requires P_tie and forbids inferring it (§3.2.2). → S6.
  - **Rolling pricing:** NCAA 70 of ~1,700 games priced today; NFL priced via
    the **date-schedule endpoint** (12 games on 13-09) even though its seasons
    listing is empty. **Full-season Σ GEV(g) is NOT computable from SR
    alone.** Resolution options (→ E19): SR season win totals for the unpriced
    tail (NFL verified; NCAA absent per the 16-07 OC-Futures email), or
    InPlay-internal weekly (Edwin's original model, needs a §1.5 Change
    Order), or both.
  - **Live-bulk endpoint** (all live games, one call) exists in **global AF
    probabilities v2** — 403 on our key; separate product. Product ask → S7:
    v2 entitlement (~200k calls/mo, 0.5 QPS) or v1 quota bump (~2.5M/mo,
    ~20 QPS peak on an NCAA Saturday).
- ✅ **Probability ingestion architecture:** a dedicated MM poller at the
  spec's Approved-Data-Sources edge — reuses the SR client + ID bridge from
  `inplay-sportradar-service` **as a library**, write-through push (Redis +
  bus), never TTL cache-aside; the valuation/quoting hot path never calls SR.
  **Polling rate comes from the freshness bands (~2 s per live game), not the
  decision-cycle rate.** ⚠ The reason originally given here — "SR's number
  only moves per play (~30–40 s)" — is **WRONG and superseded by the 24-07 SR
  ingestion research above**: the measured median update gap is **4 s**. The
  ~2 s conclusion stands; the justification is "matches the median", not
  "oversamples".
- ✅ **Sportradar service facts (code-verified):** full-season schedules +
  results for all 170 teams work today on the core key; game replay works two
  ways (SR playback host streams real recorded games — no auth, real-time —
  and local JSONL fast-replay through the same pipeline). **S5 resolved.**
  Real SR Push (events stream) is itself an unconfirmed add-on entitlement.
- ✅ **Build start (George, 24-07):** begin now against mock + replay
  probability inputs — replay harness → valuation engine → position/quote/
  state engines. Venue sync and live data integrate later.

## 2026-07-23 — MM follow-up call (Edwin + Troy + team) — [[23-07-2026-market-maker-follow-up]]

> Not the planned deep-dive: **E11 (settlement) and E12 (NCAA) were never
> asked** — another MM call expected. George emailing the anchor doc to Edwin.
> Theme: **"really simple to start"** — augment over the next couple of months.

- ✂ **Quote lifecycle overturned — no top-ups, ever.** A partially-filled
  resting order is never refreshed; it rests until completely gone. On a
  price move: cancel the old level, post the **remaining** quantity at the
  new price. After a full fill at an unchanged price: reload at top of book.
  Supersedes the 22-07 amend-in-place recommendation (N12) and the
  top-up-replace mechanics (N10 → resolved).
- ✅ **Replace = cancel + new order at the back of the queue** — confirmed on
  the tZERO call and by Troy ("common practice on just about every matching
  engine"). Edwin: **"we don't care about that."** (T8.1 resolved; 35=G's
  only remaining value is message count.)
- ✅ **v1 crossing tolerance (confirmed by George 23-07):** post the new
  quotes without waiting for cancel confirmations; a **momentary self-cross
  during a price adjustment is acceptable** in v1. Edwin: "new orders are
  faster than cancels… on the first iteration, if we have to cross in order
  to make the adjustment in price, I don't care." No cancel-first-wait gap.
- ✅ **Cadence bifurcated by game state:** live games **~200ms per call**
  ("a second's too long") · non-live **every 30–60s** · **earnings windows**
  (Tue NFL / Wed NCAA): call all ~170 symbols for **~5 minutes**. Supersedes
  the flat all-teams-every-cycle framing.
- ✅ **Randomizer = quantities only** (especially top-of-book size, so the
  book doesn't read programmatic). **Price is purely algorithmic** — no
  price randomization. Narrows the 20-07 randomizer decision.
- ✅ **In-game price driver = Sport Radar live win probability, pulled
  directly.** No own event-weight algorithm in v1 ("you don't have to create
  it — you just pull Sport Radar's probability in"). E15 resolved;
  `event trigger weights` not needed v1.
- ✅ **Remaining-season wins produced internally by InPlay, weekly.** SR
  doesn't compute season win probability (futures aren't updated/tradeable);
  Edwin helping automate. E13 resolved.
- ✅ **Off-field = Edwin's popularity index** — ranked attendance/merch/
  popularity, valued **~$14–30 per team** (Dallas ~$30; Carolina/Arizona
  ~$14); **static at the start** and already inside the NFL IPO prices;
  changes with winning + star-player effects. E2 substantially resolved.
- ✅ **The Wednesday data drop:** every Wednesday InPlay delivers the updated
  off-field metric + remaining-game win probabilities; we plug them into the
  algo. New operational cadence.
- ✅ **Betting-feed parity requirement:** our probabilities must not lag
  DraftKings/FanDuel "or we're going to get picked off." Cody owns getting
  the feeds. (New Phase-0 item.)
- ✅ **User wash-trading policy = rulebook + surveillance, not tech (v1):**
  prohibited in the rulebook; order-query on high-volume accounts; removal
  from the event. Troy checking what self-match prevention tZERO employs (new
  T-item).
- ✅ **MM is a buyer at every IPO** — when buyers are short / to balance
  shares pushed into the market. Edwin: **"we're going to start with the
  IPO"** — sequencing signal; fuller session promised.
- ✅ **Testing via SR simulation games:** replay a past game in a ~4-hour
  window instead of waiting for preseason.
- ✅ **Edwin sending the original MM simulation Python files** ("functional,
  not a heavy lift") — E4 in motion.

## 2026-07-23 — tZERO Order Entry FIX spec v2.2 read (George + Claude, validated)

**Adopted — venue facts from the OE spec itself:**

- ✅ **FIX 4.2 only** (`BeginString` always FIX.4.2). Limit orders only
  (OrdType=2 is the sole value) — reconfirms 22-07. TIF = Day / GTC / GTD;
  GTC/GTD require `RoutingInst(9303)=DNRI`. Price field to 4 decimals (field
  precision — tick policy stays $0.01).
- ✅ **Order Replace Request (35=G) exists.** Symbol AND **Side must match the
  original order** — side is immutable; a bid can never become an offer.
- ✅ **Fills survive the replace chain:** Order Replaced carries `CumQty` +
  `AvgPx` forward. `OrderQty` on a replace = the new **total** for the chain;
  `LeavesQty = OrderQty − CumQty`. (Top-up to X resting = replace with
  `OrderQty = CumQty + X`.)
- ✅ **The fill-vs-cancel race has a defined reject:** Cancel/Replace Request
  Reject with `CxlRejReason 0 = "Too Late To Cancel"` (1 = unknown order).
- ✅ **Every execution report can carry `PosSIZ` / `PosCOST` / `PosRpnl` /
  `PosUpnl`** — venue-authoritative position + P&L per fill. Fields optional,
  so: our own event-sourced inventory stays primary; venue values used as a
  free cross-check (disagreement = bug alarm) + ops-UI P&L source.
- ✅ **No iceberg orders** — `MinQty`/`MaxFloor` "not supported on tZERO
  Matching Engine": displayed size = real size, always.
- ✅ **No `ExecInst`** — no post-only, no self-trade prevention at order
  entry. Our publish sequencing is the ONLY protection against executing
  against our own stale quotes.
- ✅ **Unsolicited cancels exist** (Order Cancelled has an unsolicited
  variant) — the reconciler must absorb venue-initiated cancels.
- ✅ **Execution Busted (ExecType=H)** confirmed at OE level; **Execution
  Corrected (ExecType=G)** also exists — a past fill's price/qty can be
  re-stated (either direction). Both reprocess through the same
  fill-reconciliation path. **Done for Day** message exists.
- ✅ `ClOrdID` ≤ 20 chars, **no leading zeroes**. Cancel/Replace *Pending*
  acks suppressed by default (request → silence → Replaced/Rejected).

**Adopted — our design consequences (validated 23-07):**

- ✅ Reconciler **never sends a replace with `OrderQty ≤ CumQty`** — where a
  shrink would go below what's filled, cancel + create fresh instead.
- ✅ Hot path is **push-only, memory-only**: FIX execution reports + bus RP
  push + in-memory state; per-cycle snapshot-at-start (atomic copy, live
  state keeps mutating, mid-cycle arrivals coalesce to next cycle); the
  append-only event log is disk-based, background-flushed, never blocks a
  cycle.
- ✅ **MM event log fully isolated from the production app database**
  (George, 23-07). It is not a transactional DB at all: one local append per
  cycle (few KB, sequential) → shipped asynchronously (log stream / object
  storage) → analysis store built from it later only if needed. The app never
  reads MM cycle records; the MM reads the log only at boot (state snapshot +
  tail replay for fast recovery). MM disk/log-shipping failure must never be
  able to touch the app (failure-domain isolation).

## 2026-07-22 — Share capacity + working process

- ✅ **Per team: 5,000,000 shares available for LONGS and 5,000,000 available
  for SHORTS** (learned 21-07, recorded by George 22-07). Supersedes the
  sheet's 875k float basis for capacity purposes; consistent with the IPO
  module's 5M float. ⚠ Consequences: the QA 1,000-share short reserve is a
  test config, not the product number; and **inventory-as-%-of-float maths
  (the skew gain λ) must be re-based** — 5M base vs 875k changes the
  effective gain ~5.7×. See [[market-maker/parameters]].
- ✅ **Working process established:** [[market-maker/working-guide]] +
  `sessions/` log + CLAUDE.md rule — any MM work starts by reading the guide,
  every session ends with a session note + working-doc updates.

## 2026-07-22 — Platform reality map (`trading-architecture.md` v1.0, live-verified)

> **Filter applied (George, 22-07): platform + venue facts from this doc are
> adopted as fact. Anything about the MM's own design (the `sdmm.py`
> prototype, its parameters, the "decided" 200 ms full-replace cadence,
> MM-as-user-account identity, the `gateway.orders.mm.*` seam) is treated as
> SUGGESTION ONLY — we design the MM from scratch. Those items live in
> open-questions as inputs, not here as decisions.**

**Adopted — venue facts (all test-verified, dates in source doc):**
- ✅ **Universe is 170 symbols: 32 NFL + 138 NCAA** (tickers `IPTC****`) —
  supersedes the standards' 163/131 count everywhere in this component.
- ✅ **tZERO has NO quote/mass-quote interface** — FIX schema is order-based
  only (D/F/G/8/9). Any MM is an order-based MM shaping the book with resting
  limit orders. (Closes T7.)
- ✅ **Limit orders only** (gateway hardcodes 40=2); **TIF = DAY / GTC / GTD
  only** — IOC and FOK do not exist in the venue spec.
- ✅ **No venue price band by default** — $0.01 and $1,000,000 limits both
  accepted verbatim. BUT the OMS Account/Position spec exposes a per-account
  collar (`LmtCents` + enforcement toggles) and wash-trade blocking — asks
  filed to enable on user accounts. Self-collar remains mandatory.
- ✅ **Shorts verified** (side=5): 1,000-share/security reserve ceiling,
  pre-trade enforced; stock-loan fee charged per short execution (absolute $,
  delivery not yet live on tZERO's side).
- ✅ **Session behaviour**: daily sequence reset 23:59 ET; resting DAY orders
  SURVIVE disconnects (cancel-on-disconnect empirically OFF) — a dead MM's
  stale quotes rest until end of day unless actively cancelled.
- ✅ **MM account mechanics exist in the OMS spec**: `UAAR` (create, with
  `MMType` + initial buying power), `UEPR` (seed per-symbol inventory),
  `UBT` (cash transfers). Entitlement ask filed. (T1 mechanism in hand.)
- ✅ **Our-side throughput is a non-issue**: Go gateway hot path measured
  ~460k orders/s/core. Binding constraint = tZERO's per-account
  `MaxOrdRate` + sustained-load authorization (ask filed). (Reframes T2.)

**Adopted — platform facts:**
- ✅ FIX gateway (Go) is live + battle-tested; two sessions (OE+MD); 170
  symbols subscribed; only 6 quoted two-sided in QA today.
- ✅ **Gateway gap #1: no outbound cancel (35=F) or cancel/replace (35=G)
  exists.** Cancel-system build committed 22-07 (owner Hasan) — includes an
  MM intake namespace, dead-man switch, Redis open-order index. Everything
  MM-shaped queues behind this build.
- ✅ Two trading planes: primary/IPO (internal, no venue) vs secondary (tZERO
  ATS). **The MM lives on the secondary plane only** — IPO fills never touch
  it.

**Adopted — economics (pending Edwin sign-off):**
- ✅ The client's real NFL IPO sheet exists and its economics decode to
  **`ESV = OffField + $5.00 × ExpectedWins`** — additive, arithmetic verified
  across all 32 rows. So **$/win = $5.00** (provisional). Float =
  **875,000/team**; price cap **$127.50**, floor 1 tick.
- ⚠ **Settlement definition** (what actually pays at season end) elevated to
  the single most important Edwin question.
- ⚠ **NCAA secondary-market scope for season 1 is OPEN** — the sheet covers
  32 of 170; NFL-only secondary is a live possibility.

**Noted as suggestions only (NOT adopted — MM is built from scratch):**
- The `sdmm.py` Phase-1 prototype and its Avellaneda-Stoikov formulation.
- Its proposed parameters (2-tick half-spread, λ 1500¢/100% float, 3
  levels/side, 6,000 sh/side, 2^k weights).
- The 200 ms full-per-team-cancel-replace cadence framing.
- MM identity as an individual user account.
- The `gateway.orders.mm.*` intake namespace (the platform's *offered* seam —
  our design may use it, but it doesn't bind the MM's architecture).

## 2026-07-20 — Market-maker Q&A (Edwin + Troy) — [[20-07-2026-touchdown]]

- ✅ **Scope: Novosapien builds CTS-001 and CTS-002** as well as PTS-001.
  George asked build-or-consume directly; Edwin: "We will build them." The
  matching engine / order book remain tZERO's.
- ✅ **Valuation formula given** (fills CTS-001's missing Section 3):
  `price = P(win this game)×$/win + E[remaining wins]×$/win + off-field`.
  Sport Radar live win probabilities are the input.
- ✂ **Unlimited capital — PTS-001 Ch 5 (Portfolio Allocation Engine)
  descoped.** Edwin: "The market maker will never have a limit on what it can
  do on capital"; buying power set to ~$100M–$100B. No finite pool, no
  zero-sum allocation. Per-team displayed-size config survives.
- ✅ **MM entity = ordinary participant + unlimited buying power + short-locate
  exemption.** tZERO to stand up the synthetic MM entity in QA (asked via the new
  Tue/Thu tZERO tech calls).
- ✅ **Limit orders only, including for the MM** — aggression via pricing
  through levels (bid 11 on a 7-at-8 market to sweep to 10).
- ✅ **Reference Price = the mid** between best bid and best ask.
- ✅ **Quoting = base spread ± per-side offsets around RP, with inventory
  skew** (long → offer drops toward RP to offload) — matches PTS-001 Ch 6.
- ✅ **Randomizer on quoted sizes** + occasional randomized **aggressive
  orders** that deliberately move price to exit inventory. ⚠ The aggressive
  behaviour goes beyond PTS-001's passive quoting — needs explicit bounds.
- ✅ **Cadence: cancel-replace ~5–10×/sec** intragame ("wipe the book and
  replace it"), plus event-triggered recompute. George's 200ms-baseline +
  event-trigger model approved by Troy for intragame.
- ✅ **Three liquidity sessions** — in-game / around-game / overnight
  (overnight deliberately wide, ~$2.5–5 spreads).
- ✅ **Markets truly isolated intragame**; each game a pairs trade; no
  rankings/tiebreaker effects; cross-game effects only between games.
- ✅ **Price band (~30%) + trade busting with tZERO** required for orderly
  markets — policy sessions "over the next couple of days."
- ✅ **NEW BUILD: synthetic market order** (app-side price-through) — before
  the first NFL game. Troy to help with logic. "A market order means whatever
  you get, you get" — no user-facing bounds.
- ✅ **NEW BUILD: MM ops desktop UI** — params, order lookup, positions, P&L;
  Kevin likely operates; sequenced last; first desktop surface of the app.
- ✅ **Priorities: challenge = stability first, profit last. Production =
  profit first** (if InPlay becomes its own MM — Edwin would open another
  company for it).
- ✅ **Terminology: "market state"** is Edwin's word for the condition/profile
  layer (not "market conditions").
- ⚠ **The standards are context, not constitution** — Edwin: "I meant it for
  Claude to read." Season-1 conformance bar to be signed off explicitly
  (Thursday 23-07).
- ✅ **tZERO cadence: two tech calls/week (Tue + Thu)** from this week.
- ✅ **Deep-dive booked: Thursday 23-07, 3–4pm London.**

## 2026-07-15 / 17-07 — Standups — [[15-07-2026-touchdown]] · [[17-07-2026-touchdown]]

- ✅ **IPO fill guarantee / float warehousing:** the MM warehouses unsold IPO
  float in max clips (~50k), guaranteeing ~35% (possibly up to 50%) of every
  float — the straw-buyer mechanism. (15-07)
- ✅ **Reference-price blend** (on-field probability + off-field) named as the
  price driver; **load-balancing algo vs market-making algo** distinction
  raised — boundary still unclear. (17-07)
- ✅ Randomized, non-uniform quote sizes flagged (book must not read as a
  machine). (17-07)

## 2026-07-17 (commit) — Standards received

- ✅ CTS-001 / CTS-002 / PTS-001 master drafts (PDFs dated 01–02 Jul) mirrored
  into [[standards/README|standards/]] via `feat/technical-standards`.
- ⚠ CTS-001's Section 3 (valuation mathematics) absent from the converted
  copy — referenced throughout, file ends at §2.33.

## 2026-07-21 — Structure decisions (this vault)

- ✅ Component named **market-maker**, umbrella over all three standards +
  new build items, with custom `systems/` + working-docs structure (this
  folder) instead of the standard component/sub-component pattern.
- ✅ Clarified I/O direction of the profile layer (condition/session in →
  spread/depth/refresh targets out) and the three-role bust model
  (participant / venue / operator) — see
  [[market-maker/systems/market-supervision]].
