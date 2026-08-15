---
description: "The as-built event-core page — the envelope, the acceptor, idempotency keys, the journal with group commit, replay, checkpoints and the F2 anchor reader"
---

# Build — The Event Core

> Part of [[market-maker/build/index|As Built]] · Code: `mm/events/` ·
> Spec: §7.1–§7.5, §1.6-3, §1.6-4.

Everything the machine knows arrived as an event. This page is the spine
every other page hangs off.

## The envelope (§7.1)

`events/envelope.py`. Every input is an `EventEnvelope`: event type, a
deterministic event id, the idempotency key, provider/receive times, the
payload, and a canonical payload hash. Two properties are load-bearing:

- **Floats are rejected at construction** — §1.6-3. The constructor walks
  the payload recursively; a binary float anywhere (however nested)
  raises. Every number in the machine is `decimal.Decimal` or an exact
  string. At the borders, JSON is parsed with `parse_float=str`, so a
  float never exists even momentarily.
- **The payload hash is canonical** — `sort_keys=True`, compact
  separators, `ensure_ascii=False`. The hash is what §7.3 conflict
  detection compares, so any code that builds "the same" payload must
  produce the same bytes. (This is also a named Go-port hazard: Go's
  `encoding/json` escapes HTML by default.)

## The acceptor (§7.2–§7.4)

`events/acceptor.py` + `events/business_validation.py`. The pipeline
order is fixed and the order matters:

    validate (Business Validated) → dedup → journal → sequence

- **Validation before dedup** (spec order): a rejected event gets NO
  Accepted Event Sequence and a `rejected` journal line carrying the
  reason — so a corrected resend under the SAME key is later accepted,
  and every re-delivery of a bad reading writes its own audit record.
  The §3.2.1 probability sum check runs here, at the door.
- **Dedup (§7.3):** same key + same hash → `DUPLICATE` (quiet, no
  downstream effect). Same key + **different** hash → `CONFLICT` — a
  data-integrity alarm: somebody upstream is lying or broken. The
  conflicting submission is journalled as a `conflict` line and
  surfaced; it never reaches an engine.
- **Seen-key retention (built 06-08d):** keys older than JetStream's
  one-week redelivery bound are pruned — nothing can redeliver them, so
  remembering them buys nothing (~43k keys/day of sweeps → ~0.5 GB per
  season unpruned). The pruning clock is the `accepted_time` high-water
  mark read from the events themselves, never a wall clock, so live
  processing, recovery, tail replay and a checkpoint restore all
  converge on the SAME pruned set. Duplicates deliberately do NOT
  refresh a key's age (replay never sees duplicate lines). §12.3's
  `event_idempotency_retention_s` slot is filled by the recorded
  06-08c design — 604,800 s.
- **Sequence (§7.4):** accepted events get the next Accepted Event
  Sequence. A restart continues the sequence and still dedups —
  proven by test.

## The idempotency keys (§7.3)

`events/idempotency.py`. The load-bearing bases:

| Event | Key basis | Note |
|---|---|---|
| `PROBABILITY_UPDATE` | source · game · `last_updated` | `last_updated` stands in for the provider sequence SR lacks (D-2; verified unique across 1,089 real readings). Keyed per GAME, never per team — two per-team events would share a key with different contents and false-CONFLICT |
| `OFFICIAL_RESULT` | source · game · result version | Always version `1`; a §3.1.3 correction is version 2 — a genuinely new fact, not an overwrite |
| `EXECUTION` | venue · **client order id** · exec id | ✂ Supersedes the spec's key. tZERO RECYCLES ExecIDs — proven by incident (a real fill silently dropped because its ExecID was seen the previous day on another symbol) |
| `VALUATION_SWEEP` | the scheduled instant alone | A late sweep is still the sweep due then; redeliveries dedup |
| `ANCHOR_SEED` | prior run dir · this run dir | ⭐ 14-08, ours (F2). The CROSSING is the fact — exactly one per new journal. Deliberately NOT keyed on time: a second seed would re-apply stale anchors over a journal that has since learned better |
| `MANUAL_CONTROL` | Control Action ID | The kill switch and per-security suspension |

## The journal

`events/journal.py`. Append-only JSONL; each line is
`{"kind": accepted|duplicate|conflict|rejected, "record": …}`. Every
line is flushed at once; durability comes per append in the default
mode, or per TICK under group commit (below).

- **One writer, by design.** `[second-writer]` is a stop condition. This
  single fact shapes the infrastructure: the engine is one VM process
  (never Cloud Run, never a hot standby — two processes are two writers).
- ⭐ **N31 group commit — BUILT 08-13 (MM PR #26).** The measured VM disk
  does ~579 fsyncs/s (p50 1.70 ms) against the ~2,520 events/s an NCAA
  Saturday arrives at, so per-event fsync was the machine's binding
  ceiling. `Journal(path, group_commit=True)` defers each append's
  fsync; `commit()` makes the whole batch durable in ONE. The runtime
  commits once per tick, before ANY await — asyncio cannot preempt, so
  nothing a tick produced (acks, venue instructions) leaves the process
  before its batch is on disk. ✂ Supersedes §7.4's "before business
  processing" with "before anything leaves the process" (decisions
  08-13). Crash honesty: a process crash loses nothing (flush hands
  lines to the OS); HOST death can lose ≤1 tick of complete,
  never-externalized lines — the same bound the taker's journal states
  (N38). Journal bytes are identical in both modes (test-pinned), so
  replay equality cannot notice. The batch size rides the log line
  (`committed=n`).

## Determinism and replay (§1.6-4, §10.3)

- No engine reads a wall clock (`mm/runtime/` is the single exception —
  see [[market-maker/build/runtime|Runtime]]). §3.3's ages are
  differences of event timestamps.
- No map-iteration-order dependence; sorted before iterating where order
  could leak.
- No unseeded randomness: every draw is a SHA-256 over pipe-joined named
  context (§5.7.3) — which also makes the draws survive a language port.
- `acceptor.replay()` rebuilds all state from the journal; replay skips
  duplicate/conflict/rejected audit lines. **Replay equality is proven on
  a real captured game**, through the venue leg, byte-identically.

## Checkpoints (§10.3 — BUILT 06-08d)

`events/checkpoint.py` + `state()`/`restore()` on every engine, both
trackers, and the orchestrator's aggregate. Boot becomes
restore-plus-tail instead of replay-everything — the journal grows all
season and every deploy is a restart.

- **The state:** the machine's COMPLETE deterministic memory as
  JSON-safe primitives (Decimals as strings, datetimes ISO, enums as
  values). The venue-connection axis stays out — the runtime supplies
  it live.
- **The file:** one canonical spelling (the payload hash's own
  sort-keys discipline), SHA-256 over the state, schema + config
  versions checked separately so a reject names WHICH guard failed;
  temp + fsync + rename atomic writes; keep-last-3 retention;
  newest-valid pick with every reject named. A config-version change
  deliberately invalidates checkpoints.
- **The boot:** the composition picks the newest valid file BEFORE
  constructing the acceptor (the full-journal scan is skipped),
  `restore()` supplies the memory, and only the journal tail past the
  checkpoint's sequence replays. No valid file → full replay — always
  correct, only slower. ⚠ Tail replay also RE-ARMS the acceptor's gate
  (sequence + seen keys) — without that fold, a redelivered tail event
  after a checkpoint boot would be accepted twice; the equality proof
  caught exactly this while building.
- **The proof (the deliverable):** on the real captured game, a machine
  that checkpoints mid-game through the real file path, dies, restores
  and replays the tail is byte-for-byte the machine that never stopped
  — identical cycle outcomes on every tail event, identical complete
  state at the final whistle, and equal to a from-scratch full replay
  (`tests/test_checkpoint_replay_equality.py`).
- **The writer:** hourly (the dictionary's `checkpoint_interval_s`), at
  a tick boundary, on the LOCAL disk beside the journal (boot never
  depends on the network; the journal disk's hourly GCP snapshots are
  the external copy). The write is synchronous — one of the stalls the
  N15 beat-jitter measurement watches.

## The anchor seed's second reader (F2 — BUILT 14-08, MM PR #32)

⚠ **`load_latest` is the WRONG loader for a PRIOR run**, and a fix built
on it would have failed silently for ever. It rejects on config_version
AND schema_version — deliberately, for its own job ("state produced under
other numbers must not seed a machine running these") — and R-D06 bumps
the config version on every deploy. Pointed at the previous run, it
therefore returns empty EVERY time, with no error anywhere (review H1).

So F2 has its own reader, `events/anchor_seed.py`, and the split is the
point: `load_latest` decides whether THIS run's own memory may be
restored wholesale, and is right to be strict; the anchor reader lifts
five fields per game out of ANOTHER run's memory, and is right to be
lenient. It verifies the integrity hash only, extracts field by field,
tolerates an unknown or older shape, reads the prior journal read-only
(never through `Journal`, which opens for append and would repair another
run's torn tail), and names every degradation for the operator. Nothing
in it raises — the fallback is a wrong-but-survivable price, and a crash
at boot is not. Full mechanism on
[[market-maker/build/valuation|Valuation]].

⚠ **"Nothing in it raises" took a second pass to be true** (review-f2,
14-08). The first build checked that a checkpoint field was PRESENT, not
that it PARSED, so a hash-valid prior run carrying `status: "in_play"` or
`x: "not-a-number"` stopped the engine BOOTING. Two lessons the next
lenient reader should inherit: validate by CONSTRUCTING the real typed
value (one gate, no second copy of the rules to drift), and remember that
`decimal.InvalidOperation` inherits from **`ArithmeticError`, not
`ValueError`** — an except tuple without it skips an out-of-range
probability while a malformed one kills the process.

## What changes here next

[[market-maker/build/next|Next]]: ~~N31 group commit~~ built 08-13
(MM PR #26) — next here: the game-day `committed=` observation and the
drain-cap re-size once engine time is the binding constraint.
~~§10.3 checkpoints~~ built 06-08d, equality-proven.
