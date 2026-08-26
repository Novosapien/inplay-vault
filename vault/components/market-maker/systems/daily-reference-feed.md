---
description: "SUPERSEDED 26-08 by the expected-wins pipeline — retained for its model analysis; the daily-file transport and ingestion design is dead"
---

# Daily Reference Feed — analysis and pipeline design

> ⚠️ **SUPERSEDED 2026-08-26.** George ruled Edwin cannot operate a daily
> hand-off, so the daily file is retired entirely. Expected wins now seed
> ONCE (`EXPECTED_WINS_SEED`) and are maintained by the absorber — the
> normative page is now
> **[[market-maker/systems/expected-wins-pipeline]]**; see also
> [[market-maker/decisions]] 26-08 and
> [[market-maker/sessions/2026-08-26-expected-wins-pipeline]]. This page's
> model analysis (§1) remains valid history; its transport and ingestion
> design is dead.

> **Component:** [[market-maker/market-maker]] · **Status:** DESIGN — nothing built, nothing deployed
> **Session:** [[market-maker/sessions/2026-08-13-c-reference-feed-analysis]] (the brief: `vault/drafts/daily-reference-feed-analysis-brief.md`)
> **Material analysed:** `reference/inplay-reference-feed/` (28-07) · `reference/edwin-handoff-2026-08-09/` (08-09) · `reference/sample_reference_feed_2026-08-29.json`
> **Prior work built on:** `standards/gamecast-ev-plain-english-guide.html` — the algebraic reconciliation of the two models. This page turns its findings into rulings-to-ask and a build plan.
> **Gates respected, not re-decided:** N19 (bucket + database, upload page later) · N23 (no §7.3 event type — raise, never invent) · E19 (Σ GEV = $5 × expected wins).

---

## 1 · The verdict on the two models (analysis question 2)

**One model, arriving twice. The 28-07 feed engine is normative for the daily file. The 08-09 Gamecast bundle is the app mock's pricing, and nothing in it describes how the daily file is created.**

The evidence, in order of weight:

1. **The 28-07 delivery is the file's methodology as running code.** Devig (`devig.py`, σ_mkt 2.7/2.2) → MOV-capped Elo (`elo.py`) → weekly calibration against SR pregame probabilities (`calibration.py`) → the NFL logit-space rake (`rake.py`) → schema + `validate_records()` (`feed.py`) → the publisher with the correction protocol (`publisher.py`). It is the direct implementation of the email that resolved **E19**, and its sample file validates clean against our built adapter (`mm/adapters/reference_feed.py`).
2. **The 08-09 bundle's resting layer (`seasonFair`) is the mock's stand-in for the missing daily file.** It computes an expected-wins substitute from the IPO price percentile plus the record (`e0 = 5.5 + pct·6.5`, blended with form) because a browser cannot call his daily engine. Verified in the JSX source (`InPlayHomeV1423-SOURCE.jsx:331`) — the transcription in the pricing docs is faithful. It consumes no bookmaker line, no Elo, no calibration — and no daily file.
3. **The live layer reduces to our built formula times a dial.** The plain-English guide's algebra: his `ΔC1 = 5·M·(wpLive − wpPre)` against our `Δ = $5·(x − p_ref)` — identical except the maturity multiplier `M`, and `M → 1` at the whistle, so both bank the same $5 on every result. The dial changes the path, never the destination.
4. **The mock-only additions do not belong in our engine.** The C2 live re-rate exists because the mock cannot fetch a fresh T mid-game — in production tomorrow's file re-rates the forward leg, and a live re-rate on top of T double-counts the next morning. The injury markdowns belong inside Edwin's engine (an injury changes T). The jitter/noise machinery (`ρ_game`, `rndOn/rndOff`, `ε`) is a third independent instance of the invented-movement instinct — logged as **E34 evidence**, and its §7 ties itself to the RPV-2 machinery that **E30** already holds at "build none of it".
5. **No decision adopts the Gamecast model.** The normative chain stands: the v1.3 spec Ch 3 as amended by E19 for pricing; the 28-07 engine for the file. decisions.md outranks any external document.

**The conflict that is Edwin's to resolve, not ours:** the 08-09 handoff calls `pFair` "the number your system needs to reproduce", and its spec §11 says the production market maker quotes around `P_fair`. That is a normative claim. Per the 22-07 stance (we ask, we do not propose) this is now **E47** in [[market-maker/open-questions]]: display model, or supersession? The same ask carries the maturity dial `M` (book-visible → his call), the unexplained **5.25 vs 5.00** forward coefficient, and the one genuinely new piece — the **off-field method** (`offShare = 1.0 + pct·0.5` against the $2.50 pool), which would fill our mocked RAV/EAV leg if he confirms it.

**Until E47 answers: build nothing from the 08-09 bundle into the MM. Proceed on the 28-07 chain.**

## 2 · Who produces the file (analysis question 1)

**Edwin/InPlay owns the methodology and remains the producer. We are the consumer, plus a cheap verifier. Running his engine ourselves is a break-glass contingency that needs a ruling, not a default.**

Could we run it mechanically? Mostly yes — and that is not the question:

- **NFL:** the devig needs only the posted season win-total line with both sides' odds. Verified obtainable (`season-win-totals-170.csv` carries both sides for all 170 lines — N18).
- **NCAA:** needs his full Elo stack — 5–10 seasons of historical results (the SR backfill, never pulled), the complete remaining schedule for all 170 teams, conference groupings for the preseason regression, and weekly SR pregame probabilities for calibration. Runnable, stdlib-only, but a real data-acquisition project.
- Either way his code is `float` throughout — anything we execute ports to Decimal (§1.6-3), as the adapter already did for validation.

What breaks if we become the producer:

1. **§1.5 bans internally generated probabilities.** E19's resolution made InPlay the producer precisely so the number stays InPlay's. If we run the fit, the MM prices from numbers we generated.
2. **The 22-07 remit line.** T is the price level — book-visible — so it is his algorithm and his numbers. The calibration judgement (k, HFA, MOV cap, prior weight, freeze timing) is methodology, versioned by HIS `methodology_version`.
3. **E47 makes "his maths" ambiguous** until he confirms which model is normative. You cannot faithfully run a methodology that is still two candidates.
4. The challenge dataset (the MM's job 3) is worth more when the forecast behind the price is independent of us.

What we SHOULD run:

- **The NFL devig as a verifier, not a producer.** On every accepted file, recompute the 32 NFL numbers from the current line and flag drift beyond a threshold (threshold 🔴 TBD — a parameters row exists). Cheap, catches a broken rake or a stale line on his side, and answers N18's cross-check half.
- **The contingency, surfaced for George:** if Edwin's production feed is not live by the NCAA secondary open (~26–27 Aug, E25), the options are (a) stay on the static seed / hold-last-value posture — live mode stays gated on N19 — or (b) run his engine as a break-glass producer **with his sign-off**, output marked by `methodology_version`. George's call, with Edwin. ⚠ **E43 movement:** the schema half of E43 is answered (28-07 delivery + sample, validated against our adapter). The open half is his **production stand-up** — as of 07-08 he had "not built the forward-looking gains model yet". Ask for the date.

## 3 · The ingestion design (analysis question 3)

The store is decided (N19, 03-08): the **bucket** holds every file byte-for-byte (rejected too, reason in object metadata; versioning on now, retention lock later; object first, then row); the **database** holds the parsed rows; the row carries the object path and hash. The design below is everything around that decision.

### 3.1 The shape — bus delivery, matching the 05-08c ingestion ruling

```
Edwin (interim: object drop / later: upload page)
        │
        ▼
┌──────────────────────┐    reject → bucket (reason in metadata) + alarm; never the bus
│ WATCHER / PUBLISHER  │    validate at the door (all violations at once)
│ (one worker, ours)   │    accept  → bucket object → DB row → JetStream publish
└──────────┬───────────┘
           ▼
   JetStream REFERENCE_FEED (durable, file carried whole + object path + SHA-256)
           │
           ▼
┌──────────────────────┐    pop → validate again (§7.2, [both-ends]) → journal ONE
│ MM ENGINE (consumer) │    event per accepted file → ack → fan out per security
└──────────────────────┘    → reprice, no smoothing
```

- **Why the bus and not an engine-side bucket watch:** the 03-08 note said "the engine watches the bucket either way", but the **05-08c ingestion ruling** landed after it — the MM consumes the bus and never calls an external source itself. A bucket poll is an external call plus a wall-clock schedule plus GCS credentials inside the engine; the bus path rides the exact machinery the SR path already drilled (durable consumer, pop → journal → ack, dedup on redelivery). The upload page needs a server-side component later anyway, and that component publishes after storing. **Recommendation, George approves.**
- **The worker's home:** the `mm_publisher` worker in the sportradar service repo is the pattern (one process, fail-open on source, fail-fast on NATS). This is not SR data, so the home is a small open detail — same repo beside `mm_publisher`, or the proxy. No new deployment unit is the goal. For Hasan with the bucket IAM.
- **The message:** the file rides whole (50–100 KB, well inside limits), headers carry the bucket object path, the SHA-256, and the received stamp. `Nats-Msg-Id` = `{source_id}:{effective_time}:{revision}` — redeliveries dedupe on the correction protocol's own identity.

### 3.2 The journalled event — N23's proposed shape (to ASK, not to build unblessed)

§7.3 fixes its event types and none is a reference-numbers feed; per §1.6-1 we raise rather than invent. The ask goes to InPlay **in the same round as N28's sweep-event blessing** (already paired there). The shape we propose:

- **One event per accepted FILE, not per team.** The file is accepted or rejected whole (`[whole-file]`), one snapshot, one G boundary. Per-team events would allow partial application and would collide with the N28 lesson (a reading is a fact about a game, not a team — this file is a fact about the whole universe).
- **Type name proposed:** `REFERENCE_NUMBERS`. **Idempotency basis:** `source_id + effective_time + revision` — exactly the correction protocol, so a correction is a new key, never a conflicting duplicate.
- **Payload:** the 170 parsed rows (exact-decimal strings) **plus** the bucket object path and SHA-256. The rows keep §10.3 replay self-sufficient from the journal alone; the pointer ties the journal to the §10.4 evidence.
- **Handler:** the acceptor admits the event; the valuation engine's `ingest_reference_numbers` becomes its consumer, fanned out per security; the orchestrator folds the new RP before the cycle (the 05-08 one-event-late defect fix stands).

### 3.3 Mid-session updates, corrections, and ordering

- A file can land at any time — a late 06:00 file, or a correction (`same effective_time`, bumped `revision`, `is_correction=true`). The engine ingests whenever the event arrives; G membership already keys on the `effective_time` boundary, so a correction replaces the statement about the same moment consistently.
- **Monotonic apply guard (new, ours):** apply a record set iff `(effective_time, revision)` exceeds the currently applied pair. A redelivered or late-arriving OLDER file journals (evidence) but does not regress T. The skip derives from journal order, so replay reproduces it exactly.
- **No smoothing** on the step (Edwin, twice recorded). Widening quotes around the 06:00 window stays his optional lever.

### 3.4 T is not the field — banked wins

`T = banked wins + expected_remaining_wins` (`[t-is-not-the-field]`). v1 computes banked from our own journalled `OFFICIAL_RESULT`s (N16 — we already mint them); banked is zero at the NCAA open, so nothing blocks launch. Cross-check on every file: the file's `games_remaining` against our schedule-derived count — a mismatch is an alarm, never silent trust. The cheaper permanent fix — one more published field — already rides the **N22** ask.

### 3.5 Stale-T posture — the mechanism ours, the numbers Edwin's

Hold-last-value plus alarm is his rule; **how long we may quote on a stale T is his number** (book-visible, the unsent question recorded in N19). The mechanism we design now, so the ask has a concrete shape:

- T-age is measured deterministically: the N28 sweep's `scheduled_time` minus the applied `effective_time` — no wall clock enters the engine.
- The same ladder shape as §3.3 freshness: **T-WARNING** (a missed 06:00 file → alarm, quote on), **T-DEGRADED** (widen / Defensive posture), **T-SUSPEND** (the book comes down). All three thresholds 🔴 TBD in [[market-maker/parameters]] — proposed rungs exist there purely to make the question concrete (~26 h / ~50 h / Edwin's call).

### 3.6 What `sigma` does — stated honestly

The feed's `sigma` (schedule dispersion √Σp(1−p)) is validated and stored, and **consumed by nothing today**: quote width runs on measured volatility (`st.vol.sigma_squared`, the E31/E44 family), not on the file. Any future use — e.g. a width floor scaled by schedule dispersion — is book-visible and Edwin's, alongside E31. The handover shorthand "sigma sets quote width" is design intent, not the build.

### 3.7 The upload page (phase 2 — the N29 panel pattern)

New pages + proxy endpoints on `inplay-admin-panel-trading`, no new deployment unit:

- **Proxy:** `POST /api/reference-feed` (validate → object → row → publish; the all-errors list returns to the screen), `GET /api/reference-feed/history` (files, revisions, rejections with reasons), `GET /api/reference-feed/current` (per-team T + age).
- **Panel page:** upload control with the validation report rendered whole (N19: Edwin fixes the file while still at his desk), the history table, a current-T view with the T-age tile.
- **The API path ships with the button** (N19's requirement) — the same authenticated endpoint lets Edwin automate later with no change on our side.
- **Validation parity:** the proxy runs the SAME rules as `mm/adapters/reference_feed.py`. Recommendation: a vendored copy plus shared golden fixtures (accept + every rejection class) proving parity in CI — a shared package is overhead for ~180 lines.
- **Operator identity:** consistent with N35's ruling — v1 attaches no name; the row flags the entry source (`upload-page` / `bucket-drop`); reopens only on a compliance demand.

### 3.8 The database rows

One table, rebuildable from the bucket (the N19 test): `source_id · effective_time · revision · team_id · league · expected_remaining_wins · sigma · games_remaining · methodology_version · object_path · object_sha256 · received_at · status (accepted/rejected) · reject_reasons`. Cloud SQL Postgres (already in the VPC). The panel reads the database, never the journal.

## 4 · The build plan (analysis question 4) — honestly sized

**The deadline that matters: NCAA secondary opens ~26–27 Aug (E25). Live mode refuses to start without file delivery (N19 gate). Phase 1 is ~one working week of build, so it fits — if the asks move now.**

### Phase 1 — the pipeline core (~5 working days)

| # | Work | Size | Blocked by |
|---|---|---|---|
| 1 | Bucket + object conventions (versioning on, no lock), IAM | ~½ day | Hasan (project, IAM) |
| 2 | Watcher/publisher worker: validate → bucket → row → publish; reject → bucket + alarm | 1–2 days | worker home (Hasan/George) |
| 3 | Engine: `REFERENCE_NUMBERS` event + consumer + monotonic apply + banked-wins wiring + tests | 2–3 days | **N23 blessing** (or George rules "build provisional, flagged" — the N28 precedent) |
| 4 | Stale-T ladder mechanism (values 🔴 await Edwin) | ~1 day | — |
| 5 | End-to-end drill on the rig: sample file, a correction file, a rejected file, a late file | ~½ day | 1–4 |

Interim delivery until the page exists: Edwin drops the object (needs a GCP identity + path — an ask that dies when the page ships) **or** our side uploads every morning. **The 06:00 hand is George's open call (N19).**

### Phase 2 — the upload page (2–4 days, panel-side)

Proxy endpoints + validation parity fixtures + the DB table + the panel page, per §3.7. Rides the N29/observability panel work; kills the GCP-identity ask.

### Phase 3 — verifier + contingency (optional, after E47/George)

- NFL devig cross-check on every accepted file (~1 day; drift threshold 🔴 TBD).
- Break-glass producer (running Edwin's engine): **deliberately not sized into the plan** — needs the SR historical backfill, all-170 schedules, conference groups, the Decimal port, and his sign-off. A week+ if ever ruled, plus calibration judgement that is not ours.

### The asks this plan depends on

| Ask | Owner | Carries |
|---|---|---|
| **E47** — Gamecast: display model or supersession? | Edwin | the M dial · 5.25 vs 5.00 · C2/injury home · the off-field method adoption |
| **N23** — bless the `REFERENCE_NUMBERS` event type | InPlay | rides the same round as N28's sweep blessing |
| **N22** — publish `p_ref` (and/or whole-season T / banked) per team | Edwin | kills the banked-wins seam |
| Stale-T thresholds | Edwin | §3.5's three rungs — with the mechanism attached |
| **E43** — production stand-up date for the daily feed | Edwin | phase-1 timing; the contingency decision |
| The 06:00 interim hand | George | N19's open half |
| Bucket project/IAM + worker home | Hasan | phase-1 items 1–2 |
