# Build — What Is Real, and What Comes Next

> Part of [[market-maker/build/index|As Built]] · Sequencing:
> [[market-maker/plan]] · Blockers and owners:
> [[market-maker/open-questions]].

## Real · mocked · gated

| Real and proven | Mocked / interim | Gated / unbuilt |
|---|---|---|
| Event core, journal, replay equality on a real game | Off-field RAV/EAV (§3.6) — static inputs | Live mode (S1/S7 · the go-live switch · N19) |
| Valuation with Edwin's on-field leg (his unit tests pass) | `p_tie = 0` (S6 interim) | §10.3 checkpoints (required pre-season) |
| Position/skew (Ch 4) · quoting chain (Ch 5) · market state (Ch 6) | Pre-kickoff tier 15 s (George's 10–30 range) | §5.5 public-book checks · §5.9 replenishment (E17) |
| Venue sync, wire-proven vs the real gateway | E31 width values (mechanisms built, numbers Edwin's) | Ch 9 IPO · Ch 11 settlement · §10 recovery |
| The full bus path, drilled end to end 06-08 | Loopback's synthetic T | Opening-position publisher (E27) · boot-reconcile healer |

## What we build next

Each item names the build page it will change.

**Ours, unblocked:**

- ✅ **DONE 06-08d — the wire-contract alignment from Hasan's guide:**
  `account` (FIX Tag 1) on every new order · identity via env through
  `compose.py::Settings` (`MM_VENUE_ACCOUNT` · `MM_USER_ID` ·
  `MM_BOT_ID`; the reply subject follows the env user id;
  `mm_user_id`/`mm_bot_id` left the dictionary) · `venue_price_cap`
  $127.50 in the dictionary, the ladder ceiling floored at min(MEV,
  cap) · the heartbeat on its own ~250 ms task (N15's pairing — the
  4 s window retunes AFTER the VM jitter measurement). MM commits
  `21dd7e1` → `3c2368f`, 534 → 540 tests. The env-vs-dictionary split
  is recorded on [[market-maker/build/venue|Venue]] and
  [[market-maker/build/runtime|Runtime]]; the NATS credential
  (Secret Manager → env at deploy, never files, never git) lands with
  the deploy.

- **The go-live ingestion switch** (at push-live — George, 06-08b): the
  live composition consumes the bus, the poller keeps only the
  heartbeat, `LIVE_GATES`' ingestion entry closes. Changes
  [[market-maker/build/ingestion|Ingestion]] and
  [[market-maker/build/runtime|Runtime]]. Gate: re-run the docker drill
  against the live wiring.
- **§10.3 checkpoints** (required pre-season — every deploy is a
  restart): complete-state snapshots + integrity hashes +
  replay-from-checkpoint equality across the engines. A session-sized
  build. Changes [[market-maker/build/event-core|Event core]] and
  [[market-maker/build/runtime|Runtime]].
  **Design agreed with George 06-08b:** five steps — per-engine
  `state()`/`restore()` · canonical file format (sorted-keys JSON,
  sequence + config version + schema version + SHA-256; schema mismatch
  falls back to full replay, loud) · hourly writer at a tick boundary
  (atomic temp+rename, keep the last few) · boot loads the newest valid
  checkpoint then replays the tail · the equality proof on the real
  captured game is the deliverable. **Storage:** local persistent disk
  beside the journal (boot never depends on the network); the journal
  disk's hourly GCP snapshots are the external copy (⚠ not provisioned
  yet — the VM does not exist; lands with deployment). **Companion
  item — dedup retention:** the acceptor's seen-keys memory grows
  ~43k/day (sweeps) → ~0.5 GB/season; prune keys older than the
  redelivery bound (one week, JetStream's retention), deterministically
  — driven by EVENT timestamps inside event processing, never a wall
  clock, so replay reproduces the same pruned set.
- **N31 group commit**: batch same-moment events into one fsync; nothing
  accepted until its batch is on disk. Measure the real fsync on the VM
  first. Changes [[market-maker/build/event-core|Event core]].
- **The CI/CD audit** (George, 06-08): testing + prod deploys for the
  sportradar API and workers incl. the publisher's slot, and the MM
  engine's deploy story. Fills
  [[market-maker/build/infrastructure|Infrastructure]]'s thin row.
- **The boot-reconcile healer** (parked with eyes open): dead-man-swept
  levels surviving a replayed record; the §3.1.4 healer + an ICD
  snapshot. Changes [[market-maker/build/venue|Venue]] and
  [[market-maker/build/runtime|Runtime]].

**Gated on others:**

- **Live mode itself** — S1/S7 (SR production allocation) · T1 (the MM
  account) · N19 (Edwin's file transport: bucket + upload page; who does
  06:00 until the page exists). Changes
  [[market-maker/build/infrastructure|Infrastructure]]'s status table.
- **Off-field §3.6** — the RAV/EAV methodology (Edwin's world). Changes
  [[market-maker/build/valuation|Valuation]].
- **E31 values** — per-state width floors, the σ² bounds, the cold-start
  sign-off; the slots exist. Changes
  [[market-maker/build/quoting|Quoting]] and
  [[market-maker/build/market-state|Market state]].
- **§5.5 / §5.9** — the public-book checks (need the participant book
  feed) and fill replenishment (E17 decides the lifecycle). Changes
  [[market-maker/build/quoting|Quoting]].
- **Ch 9 IPO allocation** (needs E27's publisher — the day-one book) and
  **Ch 11 settlement**. New pages when built.
- **The MM panel pages + the kill-switch surface** (N29's shape; access
  control first). Changes
  [[market-maker/build/infrastructure|Infrastructure]].
- **The Edwin round E29–E38 + N23/N28** — not build items, but several
  answers land directly in existing code slots.

**Direction, parked:** the Go port — everything stays Python through
season 1; differential replay (the same journal through both
implementations, compared byte-for-byte) is the port's certification
tool. The four port hazards are recorded in decisions 04-08.
