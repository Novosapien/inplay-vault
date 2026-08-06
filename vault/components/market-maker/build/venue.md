# Build — Venue

> Part of [[market-maker/build/index|As Built]] · Code: `mm/venue/` ·
> Spec: Ch 8 · Wire-proven 02-08 (the five-phase loopback test against
> the real gateway binary: heartbeat · post · move · kill switch ·
> dead-man).

The Target Order Book onto tZERO's real one, and the venue's answers
back.

## The Venue State Record (`venue/engine.py`)

Every order's lifecycle state, including **`DONE_FOR_DAY`** — a venue
fact the spec's §8.2 table lacked: tZERO ends its session at 23:59 ET
and every resting DAY order expires there as a distinct terminal state
(folding it into Cancelled would blind the morning repost). The record
feeds §4.4's pending exposure (PBE/PSE), Partially Filled remainders
included.

## The reconciler (`venue/reconciler.py`)

Implements **rest-until-gone** exactly as ruled (Edwin 23-07, N10):

- A still-wanted price is LEFT ALONE — never topped up.
- A price move is ONE cancel-replace carrying the remainder
  (`CumQty + LeavesQty`, which satisfies the gateway's
  quantity-above-fills guard by construction).
- New levels post FIRST, then cancels (N12 — post-first ordering; a
  momentary self-cross during adjustment is tolerated for v1).
- **No replace ever relies on keeping queue priority** (§8.3 — tZERO
  sends amends to the back of the queue).
- §5.9 replenishment is deliberately unbuilt — it IS the E17 conflict.

## Sync (`venue/sync.py`)

- **Register intent BEFORE publish.** The gateway never acks that a
  message merely reached it, so registering first is the only order that
  never understates exposure.
- **ClOrdIDs mint deterministically:** `MM` + 16 hex chars of a SHA-256
  over pipe-joined context (the §5.7.3 seed scheme reused). 18 of the
  venue's 20 chars, no leading zero, **no dots** — the id becomes a NATS
  subject token and the gateway does not guard against a dot, so we
  must.

## The transport (`venue/nats_transport.py` · `venue/transport.py`)

- One queue, ONE writer task, strict FIFO — post-first ordering survives
  onto the wire (a task per publish would interleave). Serialization
  happens at the call site so a bad payload fails with the caller on the
  stack. A dead writer raises on the next publish — never silent.
- **Time-in-force is DAY** behind one constant (E36, Edwin's call): the
  book vanishes nightly at 23:59 ET and reposts after the boundary;
  GTC's alternative is a dead bot's quotes resting with only the
  dead-man as cleanup. Self-cleaning is the built default.

## Gateway facts (gospel under the 22-07 filter)

- **The dead-man:** the gateway sweeps our resting book after **4 s** of
  heartbeat silence (N15 — the window is ours to tune); the **30 s boot
  grace** covers synchronous journal replay at boot.
- **The MM governor: 5,000 msg/s, burst 2,000** (Hasan's guide 05-08 —
  ✂ supersedes the 50 msg/s placeholder recorded earlier; local rig
  containers may still run old configs). Over-limit messages are
  **REJECTED, never queued**. T2 is ANSWERED: tZERO `MaxOrdRate`
  5,000/s · `MaxDupOrdRate` 200/s (duplicate = same symbol + side +
  type). The venue account is **1797733477** ($1bn cash + DTBP; the
  buying-power check charges ~4.8 % over notional; every order carries
  `account` = FIX Tag 1). ⚠ Wash-trade blocking is ON and rejects
  self-crosses — in open conflict with N12's post-first design (see
  decisions 06-08c; the reconciler has a change coming either way).
- **tZERO recycles ExecIDs** — proven by incident: a real fill was
  silently dropped because its ExecID had been seen the previous day on
  another symbol. Our EXECUTION key uses the client order id (see
  [[market-maker/build/event-core|Event core]]).
- **`cancel_all` is a hammer, not a stop:** fired alone, the live bot
  correctly treats the emptied venue as divergence and REPOSTS. The stop
  is Ch 6's kill switch — suspend, THEN sweep.
- The gateway's eight publisher workers do not preserve timestamp order
  across subjects — the orchestrator floors each security's cycle clock
  at its high-water mark (deterministic on replay, absorbs µs jitter).
- No cancel-on-disconnect at the venue (probe-verified); `market.book.*`
  is defined but never published — do not build against it.

## What changes here next

[[market-maker/build/next|Next]]: the boot-reconcile healer (dead-man-
swept levels surviving a replayed record — parked with eyes open) · E36
(DAY vs GTC, Edwin) · T1/T2 (the account and the real rate limit) · the
§5.5 participant book feed.
