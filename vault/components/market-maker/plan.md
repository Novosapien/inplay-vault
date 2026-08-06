# Market Maker — Build Plan

> **Component:** [[market-maker/market-maker]]
> **Status:** Draft — phases + dependencies; dates only where anchored
> **Timeline anchors:** launch mid-August (hard stop, [[vision]]) · NCAA IPOs
> ~20 Aug · first NFL game ~09 Sep ([[ipo-module/ipo-module]]) · synthetic
> market order needed **before first NFL game** (Edwin)

> ⚠ Reality check (raised 20-07): the full stack — valuation + market state +
> quoting + supervision + synthetic market orders — landed ~a month before
> launch. The plan below is deliberately a minimum-slice ladder: every phase
> produces something testable in QA, and scope bends before dates do.

---

> **Update 23-07 (MM follow-up call):** v1 got dramatically simpler — quote
> lifecycle is rest-until-gone (no top-ups, no aging), publish is post-first
> with momentary self-cross tolerated, randomizer is quantities-only, and the
> in-game price driver is SR's live probability pulled directly (no event
> weights). Cadence is bifurcated: live ~200ms · non-live 30–60s · earnings
> windows all-symbols ~5 min — so steady-state load collapses. New inputs:
> the **Wednesday data drop** (off-field index + remaining-game
> probabilities, InPlay-produced) and Edwin's original Python files.
> **Sequencing signal: Edwin wants to "start with the IPO"** (MM as IPO
> buyer) — fuller session promised. Testing: SR **simulation games** (replay
> a past game in ~4h) instead of waiting for preseason. E11 + E12 still
> unasked — another MM call expected.

> **Update 24-07 (v1.3 spec + build start):** the **v1.3 Build Spec is the
> baseline** ([[market-maker/decisions]]) — E11/E12/E1/E5/E14 answered; the
> open blocking questions are **E17–E19 + S6/S7**. **Build started (George):**
> new repo **`inplay-market-maker`**, **Python**, we build everything.
> Working mode: **step by step with George** — every step states what we're
> writing, why, and which spec sections to read. Order per spec §1.6-4:
> replay harness first; valuation on mock/replay inputs; venue sync (tZERO)
> and live SR data integrate later. The phases below predate the spec and
> are being re-cut collaboratively as the build proceeds.

> **Update 24-07 (Friday touchdown):** **new timeline anchor — trading
> functionality live for ~Aug 22** (Troy). S4 betting-feed parity partially
> mitigated: the probabilities API rides SR's betting-side feed (faster than
> the media feeds; the MM consumes probabilities directly). SR entitlement
> channel agreed (George's email → SR support + Scott + Cody). MM ops UI
> phasing set: read-only positions dashboard first, via the same APIs users
> get ([[market-maker/systems/mm-ops-ui]]). Testing reaffirmed: replay a past
> game (e.g. Chiefs–Ravens), runnable multiple times a day — check both the
> user's view and the MM's side.

> **Update 06-08b (the ingestion move, MM side: the consumer BUILT +
> DRILLED):** the MM consumes the bus end to end — reading + finals
> adapters (structural parity with the file path, proven 1,089/1,089 on
> the real capture), the JetStream durable consumer seam (acks batched
> AFTER the tick: pop → journal → ack), the runtime drain (a duplicate
> re-offer still advances the observation stamp — E38 on the wire), and
> the composition (`python -m mm.runtime` binds the durable; loopback
> now routes via the real `TEAM_BINDINGS`). **512 → 534 tests.**
> ⭐ **George's ruling, service side (`0b936c8`): every successful fetch
> publishes** — the re-offer is the liveness signal; msg-id =
> `{game_id}:{last_updated}:{fetched_at}`. Closes the halftime trap at
> the transport layer AND the finals-after-last-reading gap.
> ⭐ **The end-to-end drill PASSED on local docker** (`mm-nats` now runs
> `-js`): pre-boot catch-up · live delivery · duplicate-advances-stamp ·
> MM-minted final · restart with zero redelivery.
> **Parked (George): the poller retires only at GO-LIVE** — the live
> composition switches to the bus then, and the `LIVE_GATES` ingestion
> entry closes then. **Next: session close done; then the Edwin round /
> §10.3 checkpoints / the CI/CD audit at end of implementation.**
>
> **Update 06-08 (the ingestion move, service side: the publisher BUILT):**
> `inplay-sportradar-service` branch `feat/mm-probability-publisher` (off
> updated dev; all local, unpushed): the MM probability publisher — tier
> scheduler (the vault's numbers) · float-free fetch (`parse_float=str`
> end to end) · lease-fenced worker loop · **JetStream delivery** (Hasan
> confirmed, then **validated on the production server**: 10 GB store,
> 5 streams live; the publisher refuses to start without it; msg-id
> dedup on the reading's identity). 547 → 575 tests. Payload carries the
> `live` flag for §7.3 hash parity with the MM's file path.
> **Next (NEW session): the MM-side consumer** — JetStream durable sub →
> the runtime's drain path, observation age from `Fetched-At`, finals
> MM-side; then the in-engine poller retires. Rig chore: `mm-nats`
> needs `-js`. 📌 George (06-08): END-OF-IMPLEMENTATION CI/CD AUDIT —
> testing + prod deploys for the sportradar API and workers.
>
> **Update 05-08c (all 170 bindings verified · ⭐ the ingestion ruling):**
> The live `HttpSource` + the seam's failure contract landed (**500 →
> 512 tests**), the bindings were captured in one careful pass and
> verified to all 170 (163 exact · 6 profile-confirmed · the Rams via
> the mappings bridge → `sr:competitor:4387`), and
> `mm/bindings.py::TEAM_BINDINGS` closed the bindings live-gate.
> ⭐ **Then George's ruling re-cut the live path: the sportradar SERVICE
> polls SR and publishes readings on NATS — the MM consumes the bus and
> never calls SR itself.** The build had drifted from the 24-07
> ingestion decision (polling absorbed into the engine across 01-08 →
> 05-08); stop-condition #2 never fired; George caught it in review.
> The seam contains the cost — `HttpSource` and the failure contract
> transplant to the service; nothing in valuation/quoting/replay moves.
> ⚠ The 05-08b/c MM commits are LOCAL and stay unpushed (George).
> **Next: (1) the ingestion-move scope, one page, George approves BEFORE
> any build** (service work: git pull → verify local → branch off `dev`)
> **→ (2) §10.3 checkpoints → (3) the Edwin round E29–E38 + N23/N28.**
>
> **Update 05-08b (the COMPOSITION lands — the machine RUNS):**
> `python -m mm.runtime` boots, stands its book against the real gateway,
> ticks, drains, sweeps, and dies cleanly — **the drill passed both
> halves** (cold boot + restart-from-journal) on the revived rig.
> Built this stretch: **tiered polling** (LIVE 2 s · PRE_KICKOFF 15 s
> interim · OVERNIGHT 30 min · POST_GAME 10 min through the window, then
> never — the slow tiers are George's numbers, and the post-game watch
> turns a corrected score into a loud CONFLICT) · **`mm/universe.py`**
> (the 170 from tZERO's own ticker list; the ticker IS the security id;
> §2.5-validated at import) · the tick **drains** `order.mm1.>` to empty
> (a fill moves the book in its own tick) · discovery's first production
> caller · **live mode refuses to start and names its gates**.
> Two defects found by building: Edwin's daily step reached the book one
> event late (fixed — [no-smoothing]); a moved kickoff slept out its old
> schedule (fixed). ⚠ The restart drill demonstrated the boot-reconcile
> gap live: three dead-man-swept levels survived in the replayed record —
> parked with eyes open (the §3.1.4 healer + an ICD snapshot are the
> fixes). **443 → 500 tests.**
> ⭐ **George, end of session: the TRIAL KEY covers the build** — so the
> live HTTP source and the sr-id bindings capture proceed WITHOUT S7
> (one careful capture, not a loop; the trial quota was half-used in
> July). **T1 goes to Hasan directly** (with N30 + the governor).
> **Next: the live source + bindings → §10.3 checkpoints → the Edwin
> round E29–E38.**
>
> **Update 04/05-08 (the RUNTIME lands · quiet ≠ dead):** **N28 built** —
> `VALUATION_SWEEP` is the tenth event type, minted by the new
> **`mm/runtime/`** loop (1 s tick: beat → drain → due polls → due
> sweep; fixed slots; a stall emits ONE sweep with the missed count).
> ✂ The sweep is **portfolio-wide** (0.5 events/s — the 03-08 "85/s +
> emit-on-effect" note was a per-security misreading, dropped).
> ⭐ **The observation-age deviation (E38):** SR sends no heartbeat and
> halftime is a measured **2,862 s** gap, so §3.3.1 as written suspends
> every book through halftime. Built instead (George, corrected to final
> form 05-08): **a successful fetch confirms the number** — the live
> bands run on time-since-last-successful-fetch; fetches landing →
> CURRENT at full status through every stoppage; **20 s of true silence
> suspends**. Feed health rides the sweep's journalled `observations`
> map, so replay reproduces the same suspensions. Band values untouched
> — E38 takes the intent + values to Edwin with the measurement.
> Also this stretch: the **200 ms capability ruling** (build capable,
> choose the rate later; compute measured at 6.3 ms per 70-security pass
> — 22× better than estimated; the journal fsync ceiling is **N31**,
> unmeasurable off the Mac) · Python-then-Go **parked** (everything in
> Python now) · no new database · secrets via Terraform · Cloud NAT
> exists. **443 → 474 tests.**
> **Next: tiered polling** (needs the 🔴 pre-kickoff number) → the
> composition script → §10.3 checkpoints (its own session) → **send the
> Edwin round E29–E38 + N23/N28**.
>
> **Update 03-08 (DEPLOYMENT ARCHITECTURE — N7 answered):** design
> session, no code. The machine's shape is settled: **one stateful engine
> plus one stateless panel, joined by NATS.** The MM engine gets its own
> VM in the same subnet as NATS — not Cloud Run (single-writer journal),
> not the gateway VM (that host is the SPOF holding the whitelisted IP).
> ⚠ **Addresses TBC: the vault's `VPC Setup.md` does not match the live
> config** (gateway `10.0.1.2`, NATS `10.0.2.2`) → **N30**, for Hasan.
> Auto-restart with a rate limit;
> journal on a dedicated persistent disk with hourly snapshots. Edwin's
> daily file: **the bucket holds the file, the database holds the parsed
> rows**, the row carries the object's hash — which collapses the
> interim/end-state split, because the upload page later writes the same
> object the engine already watches. **The panel never reads the journal**
> — the engine publishes to NATS, a projector writes the database, the
> panel reads the database. The **three runtime clocks** are specified in
> `parameters.md` (1 s tick · tiered SR polls · the §3.1.4 sweep).
> ⚠ **The §3.1.4 sweep is the hard part of the runtime build** — the
> orchestrator reads no wall clock, so a clock-driven sweep has no legal
> `at`. Resolved by making the scheduler a **producer** outside the
> deterministic core; needs a tenth event type (**N28**, ask with N23).
> **N29 ✅ answered (03-08b): the MM panel is
> `Novosapien/inplay-admin-panel-trading`** — the trading QA/monitoring
> panel, not the internal-operations `inplay-admin-panel`. It already
> runs an in-VPC Python `proxy/` that speaks NATS, so the MM panel is
> **new pages plus new proxy endpoints, no new deployment unit**.
> ⚠ It queries no database, so live monitoring reads live and only the
> file history needs a store; **Redis is already in the proxy** and is the
> better home for the live projection.
> **New/changed: N7 ✅ resolved · N29 ✅ resolved · N19 store decided, the
> 06:00 hand-off still open · N28 + N30 opened.** ⚠ **For Hasan, one
> message: the real VPC layout (N30) and Cloud NAT** for the MM VM to
> reach Sportradar (`VPC Setup.md:660`).
> **Next: the panel-side build** (bucket · file-history store · ingest
> handler · proxy endpoints · MM pages), then `mm/runtime/`.
>
> **Update 02-08 (FIRST CONTACT — the loopback wire test passes):** the
> real NATS transport is built and the whole stack ran against the real
> gateway binary (LOOPBACK_MODE + MM namespace + dead-man live, in
> docker) — all five phases pass: heartbeat, post, move, the kill
> switch, the dead-man sweep. Three wire-only findings fixed (topic-named
> events · cross-subject timestamp jitter → per-security cycle-clock
> floor · cancel_all reposts unless the bot's own Ch 6 kill switch
> engages first). Game discovery built (schedule → game list, same S1
> entitlement as the timeline). §10.3 checkpoints deferred as a full
> session, recorded. 434 → 443 tests. **The venue side is build-complete
> for live; the remaining blockers are permissions (T1/T2 · S1/S7) and
> the unsent Edwin round E29–E37.**
>
> **Update 01-08c (the ungated tier LANDS — step 5 · Ch 6 · Ch 12):** third
> stretch of the day. Rejection audit records close the fix pass (§3.2.1 at
> the acceptor's door, §7.2's order honoured). **Chapter 6 built** — the
> four states wired into every cycle: instant demotions, one earned rung
> per 10 s dwell (Suspended→Defensive free), the kill switch as a
> journalled MANUAL_CONTROL event, the suspended sweep per cycle, Edwin's
> four-row dwell table on a derived activity axis (1 h windows = N4
> interims). **Chapter 12 built** — every configurable value in one
> validated registry, the CONFIGURED convention retired and test-enforced,
> §12.3 slots awaiting T2/ICD/policy. New: **E37** (§6.3 vs §6.4.1 on
> Recovery Ready — spec defect, low urgency). 392 → 434 tests.
> **Remaining ungated:** the NATS adapter + loopback wire test (before any
> live attempt) · §10.3 checkpoints · poller game discovery. Everything
> else gates on T1/T2 · S1/S7 · the unsent Edwin round E29–E37.
>
> **Update 01-08b (the POLLER built · N16 closed):** one worker, three
> publications — probabilities, official results, the gateway heartbeat.
> The poller holds no seen-state (the acceptor's idempotency is the
> memory, restart-proven); the real Chiefs–Ravens game flows FileSource →
> all engines → gateway payloads and its final whistle publishes the
> result. Validated against SR's OpenAPI specs: the v1 product we use
> matches exactly; ⚠ the S7-gated v2 product nests timeline entries under
> `market` — switching is a one-function adapter change, never silent.
> 385 → 392 tests. **Remaining:** fix-pass step 5 · Ch 12 sweep · the NATS
> adapter + loopback wire test (deferred by George) · live HTTP source
> (S1/S7).
>
> **Update 01-08 (Chapter 8 BUILT — the loop closes):** first session under
> the autonomous integration mode, run as designed: the whole chapter in one
> run, four commits, 329 → 385 tests, review at the chapter boundary.
> The machine now runs **event → priced → positioned → quoted → diffed
> against the venue's confirmed book → gateway-shaped instructions out**,
> with fills and acks flowing back through the real adapter path into
> §4.4's pending exposure. Replay reproduces byte-identical books THROUGH
> the venue leg, and two independent stacks emit byte-identical payload
> streams. Venue facts folded in from the gateway pull (6 new commits):
> **tZERO recycles ExecIDs** (EXECUTION key superseded), DONE_FOR_DAY is
> real, no cancel-on-disconnect, UEPR possibly re-enabled (→ E27 re-probe).
> New Edwin question: **E36** (DAY vs GTC — the nightly book gap).
> **Remaining before live:** the NATS adapter (one Protocol method, gated
> on T1's ACL) · the poller · Ch 12 config sweep · §5.5/checks 5+12 (needs
> the participant book feed) · checkpoints (§10.3).
>
> **Update 31-07 (Chapter 5 BUILT · §3.3–§3.5 BUILT · the machine quotes):**
> All five pieces of the re-cut Chapter 5 landed in one session — volatility
> → width → ladder → quantities → the assembly — plus §3.3–§3.5 (freshness,
> RP Status with the recovery ratchet, Confidence) and the §5.4 MEV formula.
> **171 → 329 tests**, ruff + mypy strict clean; both repos committed and
> clean. A Reference Price in → a validated, versioned Target Order Book
> out, and replay reproduces the whole chain byte-identically. Deferred,
> externally gated: §5.5 (needs Ch 8) · §5.9 (E17). **N26 closed — built as
> filed.** New for Edwin: the E18 refinement (reaction bound vs visible
> churn) and E31's cold-start addition.
> **Next: Chapter 8 — venue sync + the orchestration** (the wiring that runs
> event → Ch 3 → Ch 4 → Ch 5 in production rather than in tests), then the
> poller (buildable against replay now), then the Ch 12 config sweep. The
> thinking half is done; what remains is integration — where the unknowns
> are operational (S1/S7 entitlement, T1 permissions, **E27 the day-one
> book**), not intellectual.
>
> **Update 30-07b (two new algorithms · the process fix · Chapter 5 re-cut):**
> Edwin sent **SNT-1** (a house noise taker) and a **14-file handoff package**
> containing **ASMM-1**, a complete Avellaneda-Stoikov market maker, plus
> RPV-1/RPV-2. On the call he accepted it is **not** a drop-in replacement —
> his `quote()` takes the reference price and the position as **arguments**, so
> it sits on top of our build rather than instead of it.
> **Agreed process fix, and the most valuable outcome of the day: Edwin now
> sends spec-style documents with the equations, not code.** George raised the
> churn directly — three documents, each superseding the last, with roughly a
> week spent understanding the first. He delivered the first narrative document
> the same day.
> **Chapter 5 is re-cut, not delayed** — see [[market-maker/asmm1-adoption-spec]]
> for the ruling on each of the six areas. Net effect on the schedule: the
> **state classifier is no longer needed** (his volatility number replaces it,
> and N3's thresholds were never built), which removes work. Build order:
> **volatility number → width → ladder → guards**. `inventory.py` needs **no
> change**; Chapter 3 needs **no change** and is blocked on **E30** either way.
> ⚠ **Neither new algorithm can run as sent.** ASMM-1 quotes one-sided past
> 6,000 shares, which on day one means no bid on any book. SNT-1's order model
> is IOC, which tZERO does not support, and its 8-tick spread guard is narrower
> than our narrowest spread. Both are Edwin questions (**E32**), not blockers on
> our build.
> 📅 **Status (George): roughly halfway, and 80–90% of the time so far has gone
> on understanding rather than writing.**
>
> **Update 30-07 (Chapter 4 done, Chapter 5 next):** the on-field correction
> is complete in all three pieces, and **Chapter 4 is built** — `position.py`
> (§4.1, §4.2), `inventory.py` (§4.3–§4.6) and `position/engine.py`. **171
> tests**, ruff and mypy strict clean. Built today: the Reference Price now
> follows Edwin's leg, the daily feed reader parses and validates his file,
> and the position engine turns fills into positions and skews.
> **Next: Chapter 5, quote construction.** It consumes exactly what now
> exists — `RM` in, Target Order Book out — and it is the deadline item,
> because the market maker must quote from ~26 August. After it: the poller
> (gated on SR entitlement for live use, buildable against replay now), then
> Chapter 6 market state and Chapter 8 venue sync.
> ⚠ Two Chapter 4 inputs have no publisher: the **opening position**
> (**E27**, now second priority — it is the entire day-one book) and
> **corporate adjustments** (**E28**, expected never to fire).

> **Update 29-07b (build sequence changed):** the position engine (Ch 4) was
> next. George found that the Reference Price used the wrong on-field
> algorithm — `Σ GEV(g)` over "games we happen to hold a probability for"
> rather than Edwin's `$5 × (T − Σ p_ref + Σ x)`. That correction now runs
> first, in three pieces: **(1) the formula** ✅ built ·
> **(2) the engine state** — T, its `effective_time`, and the kickoff→next-T
> window · **(3) the feed reader** — Edwin's daily 06:00 ET file, which
> supplies T. Piece 3 also needs the adapter to stop discarding kickoff time
> (fix-pass step 4), because the G membership test compares kickoff against
> `effective_time`. **Chapter 4 follows.** It is not blocked either way — it
> takes RP as an argument and never looks inside it.

## Phase 0 — Unblock (now, parallel)

The build can't start in earnest until these move; none are code.

- [ ] **Sport Radar probabilities feed fixed** (S1/S2) — the valuation
  engine's primary input. Cody chasing.
- [ ] **Synthetic MM entity in T0 QA** (T1) — asked 20-07, Tue/Thu calls.
- [ ] **Thursday 23-07 deep-dive** — extract E1–E10 (the numbers, the trigger
  script, conformance bar). Bring [[market-maker/parameters]] as the agenda:
  every 🔴 row is a question.
- [ ] **T0 throughput + bands answers** (T2–T5).
- [x] **Gateway cancel system (35=F/35=G)** — ✅ **DONE 24-07 (Hasan):** live,
  QA-passed 7/7 against real tZERO, ~11 ms round trips. Follow-ons in
  progress: dead-man switch · TransactTime pass-through · rejection NAK ·
  at-least-once delivery.
- [ ] **E11 settlement definition + E12 NCAA scope** from Edwin — E11 anchors
  the valuation semantics, E12 decides the load profile and book count.
- [ ] Draft the **merged profile table** (N2) structure — values are Edwin's.
- [ ] **Verify Sport Radar fit (S5):** live win probability readable ~every
  200ms per live game, quota to match, + simulation games for testing.
- [ ] **Betting-feed parity (S4)** — probabilities must not lag
  DraftKings/FanDuel; Cody owns.
- [ ] **Wednesday data-drop pipeline** — agree format/delivery for the weekly
  off-field index + remaining-game probabilities (InPlay → us).
- [ ] **Edwin's Python files** — receive + read the original MM simulation
  code (E4, in motion).

## Phase 1 — Valuation engine walking skeleton

Goal: a live ESV per team in QA, driven by real Sport Radar data.

- Ingest win probabilities + season win totals; compute
  `on-field = P(win)×$/win + E[remaining]×$/win` with a placeholder $/win.
- Static off-field seed (wire the earnings engine later — E2).
- Event-driven recompute on game events; event-sourced lineage from day one.
- Publish ESV → RP on the bus (N1; NATS topic per team fits the existing
  [[architecture/architecture]]).
- **Exit test:** replay a recorded past game; ESV moves per play,
  deterministically, twice identically.

## Phase 2 — Quoting engine, one team, QA

Goal: the SDMM quoting a single team's book against the QA entity.

- Decision cycle loop (trigger → price → build → validate → publish → commit).
- Reservation prices with base spread + inventory skew (λ); ladder N levels;
  static sizes; tick conformance; never-crossed validation.
- Cancel-replace via the MM's own FIX OE session; fills → inventory feedback.
- **Exit test:** trade against it manually in QA; watch it skew after eating
  inventory; confirm cadence sustainable (T2).

## Phase 3 — All teams + sessions + state

Goal: 32 NFL books live simultaneously with session-aware behaviour.

- Market-state layer: condition classifier (simple thresholds), merged profile
  table, session state machine off the fixture schedule.
- Frozen-RP failure mode wired end-to-end (kill the feed mid-test).
- Randomizer (seeded) on sizes; profile-driven gain scheduling.
- Scale target: **32 NFL books minimum; up to 170 (32 NFL + 138 NCAA) if E12
  lands NCAA-in.** ⚠ NCAA IPOs run ~20 Aug on the *primary* plane
  (internal — no MM involvement); whether NCAA gets a *secondary* market in
  season 1 is the open Edwin question that decides the load profile.
- If NCAA-in: peak day is an NCAA Saturday (~30–40 concurrent games → 60–80
  hot books) and **activity-tiered cadence is a requirement** (hot 5–10/sec,
  warm ~1/sec, cold heartbeat-only). If NFL-only: load is trivial.
- **Exit test:** a full simulated peak day in QA — concurrent games, staggered
  windows, pre-game → live (event storm) → post-game → overnight widening.

## Phase 4 — Supervision + synthetic market order

Goal: orderly markets + the user-facing "market" button. **Gate: before first
NFL game.**

- Band checks at order entry (app-side) + out-of-band execution detector;
  bust workflow per the T0 procedure (T4); manual halt/resume.
- Synthetic market order in the Trading Service (N levels through, Troy's
  logic) — designed together with the band so N can't sweep outside it.
- **Exit test:** deliberately fat-finger in QA; detector flags; bust reverses
  positions via ExecType=H.

## Phase 5 — Ops UI + calibration (through the season)

- MM ops desktop surface (Kevin's workshop first — see
  [[market-maker/systems/mm-ops-ui]]): params, orders, positions/P&L,
  supervision flags.
- Calibration loop: trigger weights vs observed market reaction; Edwin's old
  script as seed; expect volatile first weeks (accepted 20-07).
- Aggressive-order behaviour (E8) only after bounds agreed — not in v1.

## Workstream split (proposal)

Valuation engine and quoting engine are separable workstreams after Phase 1's
RP contract is fixed — they meet at one bus topic. Supervision + synthetic
market order ride the existing Trading Service / FIX GW work. Ops UI last.

## Standing cadence

- **Mon/Wed/Fri:** internal touchdowns.
- **Tue/Thu:** T0 tech calls (entity, throughput, bands, busts).
- **Thu 23-07:** Edwin deep-dive — parameters + conformance sign-off.
- After every session: update [[market-maker/decisions]],
  [[market-maker/open-questions]], [[market-maker/parameters]].
