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
| `MANUAL_CONTROL` | Control Action ID | The kill switch and per-security suspension |

## The journal

`events/journal.py`. Append-only JSONL; each line is
`{"kind": accepted|duplicate|conflict|rejected, "record": …}`. Flush +
fsync on every accepted event — that is what makes an event durable
BEFORE anything reacts to it (§7.4).

- **One writer, by design.** `[second-writer]` is a stop condition. This
  single fact shapes the infrastructure: the engine is one VM process
  (never Cloud Run, never a hot standby — two processes are two writers).
- ⚠ **N31 — the fsync is the throughput ceiling.** A single writer tops
  out near 1,000–3,000 events/s on a real disk; the 200 ms capability
  ceiling sits on that line. **Group commit is designed, not built**:
  batch same-moment events into ONE fsync, nothing accepted until its
  batch is on disk. Measure the real fsync on the VM first (the Mac
  number is invalid — macOS `fsync` does not flush the drive cache).

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

## What changes here next

[[market-maker/build/next|Next]]: §10.3 checkpoints (bound replay time —
required pre-season, every deploy is a restart) and N31 group commit.
