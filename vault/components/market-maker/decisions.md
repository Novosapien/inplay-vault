# Market Maker — Decisions Log

> **Component:** [[market-maker/market-maker]]
> **Purpose:** Dated, source-attributed log of confirmed decisions — including
> where spoken decisions **supersede the written standards**. When a standard
> doc and this log conflict, **this log wins** (the standards are AI-generated
> context; Edwin: "meant for Claude to read… they're fairly simple").

Format: newest first. ✅ decision · ✂ supersession of a standard · ⚠ caveat.

---

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
  worse than a refused one) · `market.book.*` is defined and never
  published, do not build against it · JetStream durable publish is OFF by
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
  the T0 call and by Troy ("common practice on just about every matching
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
  from the event. Troy checking what self-match prevention T0 employs (new
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
  matching engine / order book remain T0's.
- ✅ **Valuation formula given** (fills CTS-001's missing Section 3):
  `price = P(win this game)×$/win + E[remaining wins]×$/win + off-field`.
  Sport Radar live win probabilities are the input.
- ✂ **Unlimited capital — PTS-001 Ch 5 (Portfolio Allocation Engine)
  descoped.** Edwin: "The market maker will never have a limit on what it can
  do on capital"; buying power set to ~$100M–$100B. No finite pool, no
  zero-sum allocation. Per-team displayed-size config survives.
- ✅ **MM entity = ordinary participant + unlimited buying power + short-locate
  exemption.** T0 to stand up the synthetic MM entity in QA (asked via the new
  Tue/Thu T0 tech calls).
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
- ✅ **Price band (~30%) + trade busting with T0** required for orderly
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
- ✅ **T0 cadence: two tech calls/week (Tue + Thu)** from this week.
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
