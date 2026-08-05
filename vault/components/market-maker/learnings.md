# Market Maker — Learnings

> **Component:** [[market-maker/market-maker]]
> **Purpose:** A running log of things we actually *understood* while working —
> concepts that clicked, traps caught, intuitions corrected. This is neither
> decisions ([[market-maker/decisions]]) nor questions
> ([[market-maker/open-questions]]) — it's understanding, kept so it doesn't
> have to be re-derived. Newest first. Add to it every session.

---

## 2026-07-30

- **A dead book is the real launch risk, and the fix is a house taker, not more makers.** SNT-1 exists because a real exchange with few users looks empty. The MM alone does not solve this: it posts liquidity, but liquidity nobody hits still reads as "no trading." SNT-1 manufactures the *taking* side so prints actually happen. Two house agents, opposite roles: maker (MM) and taker (SNT-1).
- **Noise is bought, not free.** SNT-1 is a deliberate controlled loser; its cost is literally the spread it crosses, metered against a $100k/team/session budget. That spread cost is the **subsidy that seeds the market** and is largely captured by the MM on the other side. The budget is a spend cap on that subsidy, not a P&L target.
- **Uninformed-by-construction is the safety property.** The realism (disposition-effect profit-taking) conditions only on SNT-1's own cost basis vs mid, never on book state or participant data. That is what keeps its flow noise rather than a signal participants could reverse-engineer or that could push price toward a target.
- **The off-field rule already handled this.** Because SNT-1 carries no participant side, its MM-facing prints fall outside the >= 1-participant-side off-field-volume rule automatically. A well-drawn rule needed no amendment for a new agent, worth remembering when the next house agent appears.

## 2026-07-23

- **The v1 lifecycle is simpler than everything we designed (23-07 call).**
  Rest-until-gone kills the top-up arithmetic, quote aging, replenishment,
  AND the amend-vs-cancel trilemma in one stroke: partially-filled orders
  just sit; price moves cancel-and-repost the remainder; full fills reload
  at top of book. The design surface that replaces all of it is
  **fill-response logic** — "if you get a fill, what do you do next" (N14).
  The 22-07 reconciler analysis is shelved, not wasted — it's the
  augment-later iteration.

- **Replace = back of the queue, everywhere.** Troy (ex-Citadel): standard
  on effectively every matching engine — an updated order is a new arrival.
  It's why real MMs invented queue tricks (partial packets etc.). Here it
  simply doesn't matter — Edwin: "we don't care about that" — because the
  MM isn't competing with other MMs for queue position.

- **v1 tolerates a momentary self-cross (Edwin + George).** "New orders are
  faster than cancels, believe it or not" — waiting for cancel confirmations
  before posting creates a gap Edwin explicitly doesn't want; a fleeting
  cross during a price adjustment is accepted on the first iteration. Wash
  blockers "can be used very predatorily" — policy for users is rulebook +
  order queries + removal, not venue tech (Troy checking tZERO's self-match
  prevention anyway, T11).

- **Edwin's ingestion model is pull, not push.** He talks in "calls" — we
  call Sport Radar on a schedule that bifurcates by game state (live ~200ms,
  non-live 30–60s, earnings burst). The hot-path principle survives
  unchanged: a poller writes memory, the quoting loop reads memory. Whether
  SR can actually serve that call shape is S5.

- **A trade print is a public receipt.** Every match is broadcast on the
  market-data feed — price, size, time, a unique trade ID. Busts appear on
  the same feed as public trade *deletes* (reason "Cancel/Bust").
  Consequence: the supervision watchdog runs entirely off the public feed —
  it sees every trade in every market, including user-vs-user trades the MM
  wasn't part of. No special access needed.

- **Aggregated book = queue position is invisible.** tZERO's feed shows only
  the total per price level (plus an order count) — never individual orders.
  We can never observe where our own order sits in the queue, so T8.1 (does
  an update keep queue position?) can only be answered by tZERO directly or by
  a two-account experiment in QA.

- **Opening auctions exist in the venue.** Some markets open by collecting
  orders without matching, computing one fair opening price from all of
  them, trading everyone at that price, then going continuous. tZERO's feed
  has the machinery (auction state, theoretical opening price). Whether OUR
  market uses one daily = T9 — it changes what the MM does at the open.

- **Match the store to the access pattern (why object storage).** The event
  log is written once, sequentially, and almost never read (boot tail +
  offline analysis). Object storage fits exactly: immutable, pennies/GB,
  zero servers, built for batch reads. Postgres would charge us for indexes,
  transactions, and vacuum we never use — and degrade as it grows. A log
  system (JetStream) is the *pipe*, not the archive. Write segments as
  columnar files and they're queryable later with no database at all.

- **The MM is event-rate bound — not CPU, not RAM.** Working state is
  per-TEAM (latest RP, ~a dozen own orders, inventory, capped counters) —
  a few MB total regardless of user count. Users add message RATE (fills,
  book updates flowing through), not resident state. The math is
  microseconds. The scarce resources are the venue's message allowance (T2)
  and round-trip latency — which is why every design argument lands on
  message budgets, not hardware. Guard: rolling windows as capped
  counters/ring buffers, never unbounded event lists.

- **The two FIX sessions fail differently.** Market-data subscriptions are
  wiped on disconnect (reconnect = re-logon with sequence reset,
  re-subscribe, fresh snapshot). Order-entry resting orders SURVIVE
  disconnect. Recovery flows must be designed separately — and the OE side
  is why the dead-man switch exists.

- **Snapshot-at-cycle-start kills the race (George's catch → confirmed
  design).** Live market state mutates continuously under pushed messages;
  each cycle takes an atomic copy and computes on the frozen snapshot;
  anything arriving mid-cycle lands in live state and coalesces into the next
  cycle. No locks in the hot path — and recording the snapshot is exactly
  what makes deterministic replay work.
- **RAM is bounded; only the disk grows.** Two stores, don't conflate:
  working state in memory (latest RP, ~a dozen live orders/team, inventory,
  seconds of rolling counters) is overwritten forever — bounded. The
  append-only event log grows on disk, background-flushed, never blocking a
  cycle. A season of record-everything is tens of GB of disk — trivial.
- **Order anatomy + the top-up.** OrderQty = chain total · CumQty = filled ·
  LeavesQty = still resting. Fills survive a replace (CumQty carries), so
  top-up to X resting = replace with OrderQty = CumQty + X — or add a sibling
  order of (X − leaves) at the same price. One order/one queue spot vs two of
  each; which is better hangs on T8.1 (queue position) + message budget.
- **The event log is write-only in operation.** One local sequential append
  per cycle (a few KB) — never a remote write inside the loop; durability
  ships asynchronously behind it. It's read in exactly two places: at boot
  (snapshot + tail replay to rebuild state) and offline (replay, audits,
  calibration, the challenge dataset). Nothing in the app reads it → it
  doesn't belong in the production database, or in any transactional DB
  at all.

- **The hot path never asks for anything.** All inputs arrive as pushes (FIX
  execution reports, bus RP, MD subscription); the cycle reads only local
  memory; the database is write-behind. A 50ms fetch anywhere in the loop
  would eat the 200ms budget — so there are no fetches.
- **The venue tells us our position on every fill** (PosSIZ/PosCOST/Rpnl/
  Upnl, optional fields) — our event-sourced inventory stays primary (needed
  between messages, deterministically); venue values = free drift alarm +
  ops-UI P&L source.
- **Users can cross; we can't.** An arriving order priced through the other
  side executes immediately (normal — synthetic MO relies on it). The
  never-crossed law binds only what RESTS — specifically the ladder we
  publish against ourselves.

## 2026-07-22

- **Reconciler reality-check (George pushing on complexity).** Three facts
  deflate it. (1) **Scale:** the ladder is N≈3–6 levels/side → ~6–12 orders
  per team per cycle — the diff is over a dozen orders, not a thousand; the
  1000→1200→1000 shape never happens per team (level count moves ±1–2 on
  profile flips). (2) **Side never flips:** 35=G cannot change Side — bids
  pair only with bids, offers with offers; two independent small lists.
  (3) **No persistent slot state:** pairing is recomputed fresh each cycle —
  sort live orders by price, sort target levels by price, zip, amend each
  pair, create/cancel the tail. Stateless per cycle. And the honest
  fallback: **full wipe-and-replace is a legitimate v1** — the reconciler is
  a message-budget optimization, and T2's MaxOrdRate answer (not taste)
  decides whether it's ever needed.

- **Publish is a reconciler, not a send (George's push, refining the
  trilemma).** Levels and quantities differ cycle-to-cycle, so no single
  strategy (cancel-first / post-first / amend-all) covers a real cycle. The
  correct shape: diff the target book against the believed-live book → a
  per-slot plan — AMEND if the slot persists, CANCEL if gone, CREATE if new,
  no-op if identical (zero messages) — executed under ordering rules:
  retreating side first (retreat can never cross), cancels before creates at
  overlapping prices, advancing side deepest-first with top-of-book last,
  micro-barrier only on the specific orders an advance would cross. Same
  shape as React's DOM diff or terraform plan/apply. The dominant in-game
  case (RP tick, N constant) is pure amends. Corollary: if the seeded jitter
  re-rolls every heartbeat, cosmetic cycles amend the whole book — jitter
  cadence is a message-budget choice, and it's book-visible → Edwin-adjacent
  (randomization bounds, E5).

- **The cancel-replace sequencing trilemma (George's framing).** Per cycle,
  old quotes must become new quotes. (A) cancel→confirm→post = a naked window
  with no MM quotes for ~a round-trip. (B) post-then-cancel = brief 2×
  displayed size AND the new bid can cross the stale offer → self-trade /
  wash-trade block. (C) amend in place via 35=G = atomic per order, no gap,
  no overlap — the venue spec has it; the gateway build (Hasan) adds it;
  only structure changes (adding/removing levels) still face A-vs-B. If
  forced to choose A or B, A (the gap) is safer: users' resting orders still
  populate the book during the window and the band caps sweep damage,
  whereas B risks integrity (self-cross) and double inventory. In ALL three,
  the fill-vs-cancel race (cancel returns "already filled") must be handled
  by the state machine. Feeds N10 + the T2 message budget (G halves
  message count vs cancel+new).

- **"Recalculate on every fill" sounds heavy — it isn't.** Every fill (any
  partial, any level, either side) queues a trigger because inventory moved
  and the skew is now wrong. But cycles never overlap and mid-cycle triggers
  coalesce into ONE next cycle — so a burst of 20 fills costs the running
  cycle plus one more, and the effective ceiling is the cycle rate
  (~5–10/sec in-game) regardless of fill rate. The math itself is
  microseconds; the real cost is the cancel-replace messaging (T2 budget).

- **EMERGENCY is not a quoting profile (George's catch).** The condition
  classifier conflates two different failure classes. **Input failures**
  (Sport Radar dead, valuation stale) — the order path still works, so the
  right response is quoting wide / around a frozen RP. **Actuation failures**
  (gateway or FIX session down) — we cannot post *anything*, so "widen the
  spread" is physically impossible; the only valid responses are out-of-band:
  the **dead-man switch** cancelling our resting quotes (part of Hasan's
  cancel build) and a **halt via supervision**. Made worse by the venue fact
  that resting DAY orders **survive disconnects** — without the switch, a dead
  MM leaves stale quotes resting in the book until 23:59 ET. The decision
  table must split `compute_ok` (can we think?) from `path_ok` (can we act?).

- **The classifier is boring by design.** MOC sits at Normal almost all the
  time. It's five if-statements checked in severity order, not a formula —
  its entire job is noticing the rare moments the inputs can't be trusted.

- **`feed_lag` is not free — it has to be constructed.** You only know how far
  behind you are if messages carry event timestamps (lag = our clock − event
  stamp, which needs clock sync) or by cadence expectation (in a live game,
  plays arrive every ~30–40s; silence beyond that is itself the signal).
  Which of these is available depends on how Sport Radar delivers (S3).

- **The standards' F(…)/G(…) notation is a trap.** They read as mathematical
  functions but are type signatures: the bracket list is an exhaustive
  *allowlist of what may be consulted* plus a purity contract; the bodies are
  lookups, decision tables, and threshold rules. The only real mathematics in
  the whole stack is the offset arithmetic (reservation prices) and the
  displayed-quantity formula. Present them as lookups/rules, never inline
  with prose as if they were equations.

- **The off-field term hides a contradiction (→ E2).** The earnings-report
  component says price impact of EST/ACT is *"market-determined, not a fixed
  function of the number"* — but the MM's ESV needs a mechanical OffField
  value at every moment, and the MM re-anchors the market at ESV. If the MM
  moves mechanically at the 7:30 release, the market never gets to
  "interpret" the surprise. Edwin has to resolve which number ESV holds
  between reports and whether it steps at release.

- **Most of the "deferred math" isn't math.** Across all engines the deferred
  items are: numbers for lookup tables, thresholds for decision rules, and a
  handful of arithmetic constants. The architecture is fully specified; the
  values aren't. That's why "we ask, we don't propose" is workable — the
  questions are enumerable.

- **The remit line.** *"If Edwin watched the book, could he tell the
  difference?"* Yes → his algorithm, his question (all numbers, thresholds,
  visible behaviour). No → engineering mechanics, ours (topology, transport,
  FIX plumbing, replay). Hybrids (like full-replace vs diff-publish) get both
  options put to Edwin with the observable consequences stated.
