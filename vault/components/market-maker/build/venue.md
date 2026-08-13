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

## ⭐ The sell rule (venue-verified 08-09) — sellable = Pos − livS

A side-2 sell is checked against **the position minus the quantity
already committed to live resting sells**. Over that, the venue rejects
the WHOLE order — it never part-fills to the limit, and it never opens
a short (that needs side 5, which we do not send — E26).

```
FAILSRISK[5120866205]: You can SELL at most 50 shares of IPTCGIAN. Pos=100 livS=50
```

Consequences for this machine:
- The ladder's ask side is bounded by inventory **and by its own
  resting asks**. A repost that adds an ask while earlier asks still
  rest can trip the check even though the position looks sufficient.
- The `Pos=0` case is the familiar "You are not long … There are NO
  shares to SELL" (07-08b) — the same rule, not a separate one.
- ⚠ **Not yet enforced in the reconciler.** §5.9/E17 aside, nothing in
  `quotes/` or `venue/` subtracts live resting sells before drawing an
  ask ladder. Build item.

## ⚠ The engine crosses the stale book on every repost (live 08-09)

The QA books still carry third-party stale quotes far from Edwin's
prices. The engine prices from its own valuation, not from the book, so
its bids can be marketable against those stale asks. Observed: a COWB
bid at 76.04 swept 8 stale levels — **920 shares, $50,366**, position
100,930 → 101,850. The MM is TAKING liquidity while intending to rest.
It recurs on every repost, so it is an inventory-accumulation risk, not
a one-off. Related to §5.5's unbuilt public-book checks.

## ⚠ The engine adopts any MM-prefixed order on its user id

`_get_or_admit` (built so a restart can recover orders it did not
register) admits an unregistered ack as ACTIVE — so the reconciler
treats a hand-sent MM-prefixed order as its own and moves it. Observed
08-09: a probe order was cancel/replaced 0.7 s later (85.00 → 76.31,
60,000 → 2,500). **No manual probe on the MM user id is safe while the
engine runs.** Workaround for probes: `gateway.orders.mm.new` validates
only the ClOrdID prefix, so a different `userId`/`account` in the
payload routes the responses to that user's subject, invisible to the
engine.

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
- **An in-flight replace occupies its DESTINATION price**
  (`VenueOrder.pending_price`, 08-08, MM PR #9): with only the old
  price occupied, the destination read as unmet during the ~250 ms
  in-flight window and pass 3 double-posted it — 19 doubled levels
  measured live across the six QA books. The field rides the
  checkpoint (schema 3).
- §5.9 replenishment is deliberately unbuilt — it IS the E17 conflict.
- **Gone-retire (08-12, MM PR #24):** a cancel-reject whose verdict
  names a DEAD order — `UNKNOWN ORDER`, `ORDER DEAD[DMA]`,
  `ORDER IS DEAD`, `NOT_CANCELABLE` — RETIRES the order (CANCELLED,
  leaves 0) instead of restoring-and-suppressing; the next diff reposts
  the level. ✂ Supersedes the backoff's suppress-and-retry for those
  verdicts (the 08-12 session-roll storm: ~750 phantoms at the 60 s cap
  = ~61k rejects/hour for 8 h). Transient verdicts (REQUEST_IN_FLIGHT,
  SESSION_DOWN, "Too late to cancel") stay with the backoff. Counter:
  `gone_retires`. Also new: `expire_all()` — the session clock's close
  (see [[market-maker/build/runtime|Runtime]]) expires every
  non-terminal order to DONE_FOR_DAY and resets the backoff.
- **The reject backoff (R-R03/C4, built 08-10c — MM PR #13,
  `venue/backoff.py`):** the venue's NOs feed two event-sourced tables
  while acks apply — submit rejects key on (security, side, price);
  cancel/replace rejects key on the resting order's id (the gateway's
  CANCEL_REJECTED names `origClOrdId`). The diff then simply does not
  ask again inside the schedule: a suppressed price leaves `wanted`
  (no submit, no replace INTO it), a suppressed cancel target leaves
  `movable` (no replace, no cancel; `cancel_everything` skips it too).
  Schedule min(2 s × 2^(n-1), 60 s), values 🟡 in
  [[market-maker/parameters]]; **success is the only reset** (an accept
  or confirmed replace at the price clears it; a terminal order drops
  its cancel entry), so a level that keeps rejecting escalates toward
  the cap instead of oscillating. Expiry is priced with the triggering
  event's own time, threaded runtime → sync → diff — no clock, so
  replay reproduces identical suppressions. The tables ride the venue
  engine's checkpoint (**schema 3 → 4**). ⚠ The gateway's 2× duplicate
  delivery of cancel-rejects double-bumps a count — one extra rung,
  deterministic, accepted. ⚠ Live half of C4 (recreate a rejecting
  book, measure the rate) still owed.

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

## ⭐ The state snapshot — `mm.state` (`venue/state.py`, built 12-08b)

The engine's observability output (spec R1 of the 12-08 admin trading
observability spec). One COMPLETE projection of the engine's state,
published about once a second, so a panel that joins mid-session — or
reconnects after a dropped socket — renders correctly from ONE message.
Never deltas: there is no history to replay and no sequence to reconcile.

- **`mm.state` is OURS, not the gateway's.** The gateway owns
  `gateway.orders.mm.*` and publishes `order.{userId}.{clOrdId}`; nothing
  is added to that namespace. In particular this is NOT the heartbeat
  subject — the dead-man is one global latch and a second beater would
  mask the engine's death (decisions 10-08c). It shares the heartbeat's
  TRANSPORT (one connection, one writer queue) and never its subject.
- **Fields:** `v · ts_ms · config_version · boot_ts_ms · journal_dir ·
  global_kill_switch · quarantined[] · missed_sweeps · tick{…} ·
  universe{total,active} · shed[] · securities{SYM}`. Per book:
  `net · avg_cost · realized_pnl_total · market_state · freshness ·
  resting_orders[]`.
- **Active books only:** non-zero net OR resting orders OR market state ≠
  Stable. ⚠ Straight after boot EVERY book reads active — a
  MarketStateTracker starts Suspended until its first cycle — which is
  correct and is also the payload's worst case.
- **The projection is not `Orchestrator.state()`.** That is the §10.3
  checkpoint's complete deterministic memory, an order of magnitude
  larger and shaped for `restore()`.
- **Money crosses as a JSON number, quantized to 6 dp first** (the same
  reasoning as `[price-wire]`: the consumer is a browser). Average cost
  is a division and routinely recurring, so an unquantized Decimal would
  print 28 digits of precision the number does not have.
- **The budget has a DEFINED shed, announced in the payload.** Over
  256 KB (🟡): stage one drops the per-book `resting_orders[]` arrays and
  keeps `resting_order_count`; stage two empties `securities`. `shed[]`
  names what went — without it an empty array would read as "no orders
  resting". Stage two exists only so NATS's 1 MB `max_payload` can never
  be hit, because a publish above it is REFUSED and the feed would stop
  silently. **Measured: 208,250 bytes at 170 books** — no shed on today's
  universe.
- ⛔ **Deploy gate: the `market-maker` NATS user needs publish on
  `mm.state`.** Its grants were written for `gateway.orders.mm.>` alone,
  and a missing grant is SILENT — the publish returns normally and the
  server drops the message.

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
- ✅ **The reject-backoff gap — CLOSED 08-10c** (was: re-submits at
  cycle cadence, ~16 msg/s; shapes seen live: LmtPerc, duplicate-id,
  no-reference, UNKNOWN ORDER cancel-loops). Built as the reconciler's
  suppression input — see "The reject backoff" above. Live C4 run owed.

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
