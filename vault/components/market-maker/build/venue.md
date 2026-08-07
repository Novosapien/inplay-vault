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

## ⭐ Why the visible book scrambles (traced 07-08, simulation on the real code)

George watched the live QA books and saw no size profile. The trace
(agent run, real `reconcile_book` + `quantity_ladder`, 400-publish
random walk) found the cause is NOT the ±25% variation:

- **The engine's fresh target ladder is non-increasing 84% of the
  time** (6 levels; ties, not inversions, are what variation mostly
  produces — round500 collapses overlap bands onto shared values).
- **The venue's resting ladder is non-increasing only 5.8% of the
  time.** The profile dies in the reconciler's MOVE pass: a replace
  carries the OLD order's quantity (`cum_qty + leaves_qty`) to the NEW
  price, paired by rank — on a one-tick drift the order falling off
  one end TELEPORTS to the other end with its old size (a 10,500
  top-of-book order lands on the deepest rung). **95.7% of simulated
  instructions carried a stale size**; in steady state submits are
  zero, so a fresh drawn size almost never reaches the wire. Shape
  redraws at dwell expiry then make the scramble permanent; partial
  fills never topped up (E17) add bite marks.
- Also true: the clean 10,000/7,200/5,184 decay never exists even
  fresh — round500 flattens it to 10,000/7,000/5,000/3,500/2,500/2,000
  before variation.

**RESOLVED — option (b) ruled by George and BUILT (07-08h, MM PR #8,
main `e0f2e45`):** the move pass now carries `cum_qty + level.quantity`
(the fresh drawn size for the new rank) instead of the old remainder.
Fixes the ~96% of stale-size carriers, cancels nothing, keeps the
lifecycle; the ✂ supersession of N10's "carrying the remainder"
wording is recorded in decisions 07-08h. Option (a) — full
cancel-and-repost — was rejected (~4× message volume, reverses
rest-until-gone). What the fix does NOT touch stays on E17: kept
orders at still-wanted prices keep their old sizes, and partial fills
are never topped up. **Live confirmation (same day, redeploy
CFG-0003):** under active poker fire the visible ladder measured
32–36% monotone (5.8% before; 55.6% excluding the bitten inside
rank) — the residual scramble is the E17 remnant.

## The reconciler (`venue/reconciler.py`)

Implements **rest-until-gone** as ruled (Edwin 23-07, N10; move-size
superseded 07-08h):

- A still-wanted price is LEFT ALONE — never topped up.
- A price move is ONE cancel-replace that ADOPTS THE NEW RANK'S DRAWN
  SIZE (`CumQty + level.quantity` — George 07-08h, superseding the
  remainder-carry; satisfies the gateway's quantity-above-fills guard
  by construction, a drawn level being ≥ 1,000).
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
- **Every new order carries `account` (FIX Tag 1)** — the 06-08b
  wire-contract gap, CLOSED 06-08d. Cancel and replace carry no account
  field in the gateway's structs (verified in its source), so none is
  sent there.
- **Identity rides env, not the dictionary** (the env-vs-dictionary
  split, George 06-08b): `MMIdentity` (user id · bot id · venue
  account) is built by `compose.py::Settings` from `MM_USER_ID` /
  `MM_BOT_ID` / `MM_VENUE_ACCOUNT` and passed explicitly to the sync
  driver and every payload builder. The inbound reply subject
  (`order.{user}.>`) follows the env user id. The loopback default's
  account is the string `"loopback"` — deliberately not a real account,
  so a placeholder can never pass for `1797733477`.
- **The ladder ceiling floors at min(MEV, $127.50)** — the venue's hard
  cap (client sheet, live-verified in Hasan's guide) REJECTS rather
  than clamps, so a wrong MEV input must produce a capped ladder, not a
  stream of rejects. `venue_price_cap` lives in the Configuration
  Dictionary; the floor needs no twin (`minimum_price` is already one
  tick). See `[venue-cap]` in `orchestration/engine.py`.
- **Time-in-force is DAY** behind one constant (E36, Edwin's call): the
  book vanishes nightly at 23:59 ET and reposts after the boundary;
  GTC's alternative is a dead bot's quotes resting with only the
  dead-man as cleanup. Self-cleaning is the built default.
- **The heartbeat is the runtime's own ~250 ms task** since 06-08d —
  see [[market-maker/build/runtime|Runtime]]; N15's window stays 4 s
  until the VM jitter measurement.

## Venue risk facts learned LIVE (07-08 — the first real-venue day)

- **LmtPerc, decoded from reject texts:** an AGGRESSIVE order (one that
  crosses) may price at most **3%** through the opposite side's best
  (5% observed on one symbol — per-symbol bands exist); a PASSIVE
  order must sit within **90%** of its own side's best. The reference
  is a **SNAPSHOT that refreshes on a delay of minutes**, not the live
  book — orders can reject against a book state that no longer exists.
  An empty book (both sides) rejects everything: "No price available"
  (IPTCBILL's state; how the first order ever lands on a virgin symbol
  is the open Hasan question that gates the other 163 books).
- **tZERO remembers ClOrdIDs per session.** A redeploy that re-mints
  the same deterministic ids duplicate-rejects every order — and with
  no material change the reconciler resubmits the same ids forever
  (deadlock, seen live). Rules: NEVER wipe the journal against a
  session that remembers; a re-minting redeploy runs under a new
  `MM_CONFIG_VERSION` (every id re-mints; proven disjoint by test).
- **MPIDs (Rob Colucci, 07-08):** driven entirely by Account1 (FIX
  Tag 1) — our account 1797733477 → **IPLM**; retail → IPLY; a future
  BD-prop account → IPLP. We never send an MPID. The MM's prints are
  attributable on the tape.
- **The reject-backoff gap (build item, top priority):** the
  reconciler re-wants and re-submits a persistently-rejected level at
  cycle cadence — ~16 msg/s of churn observed. Three reject shapes
  seen live: LmtPerc, duplicate-id, no-reference.

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

[[market-maker/build/next|Next]]: the wash-trade-vs-N12 decision (the
reconciler has a change coming either way — decide with Hasan before
any venue drill) · the boot-reconcile healer (dead-man-swept levels
surviving a replayed record — parked with eyes open) · E36 (DAY vs
GTC, Edwin) · the §5.5 participant book feed. ~~T1/T2~~ answered
05-08; the wire-contract alignment they triggered landed 06-08d.
