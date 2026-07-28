# Market Maker — Learnings

> **Component:** [[market-maker/market-maker]]
> **Purpose:** A running log of things we actually *understood* while working —
> concepts that clicked, traps caught, intuitions corrected. This is neither
> decisions ([[market-maker/decisions]]) nor questions
> ([[market-maker/open-questions]]) — it's understanding, kept so it doesn't
> have to be re-derived. Newest first. Add to it every session.

---

## 2026-07-27/28 — reviewing our own build, and the wins insight

- **The tests were shaped like the bug.** Every test ran one side of a game
  at a time, so the head-on collision between two per-team events sharing a
  game-level idempotency key never occurred in the suite. There *was* an
  away-side test — it built the envelopes and checked the probabilities were
  flipped, but never put them through an acceptor. A passing suite proved
  the translation right and the architecture wrong. **Ask what shape the
  tests are, not just whether they pass.**

- **Storing answers instead of ingredients is the root of a whole bug
  class.** The engine kept each game's computed expected value and a running
  banked total, not the probabilities and results that produced them. From
  that single choice came: a corrected official result double-banking (a
  win corrected to a loss still reads $5.00), a finished game resurrecting
  when a late probability arrives ($10.00 → $14.50 on a game already over),
  and configured values that could change without any stored price
  noticing. §2.5 says it in one line — *"incremental valuation state is
  prohibited"* — and it turns out to be a bug-prevention rule, not an
  aesthetic one.

- **A silent skip and a silent failure can be the same code path.** The
  engine dropped unknown teams deliberately, because NCAA sides play FCS
  schools with no Team Company. That correct behaviour made a *missing map
  entry* invisible: an unmapped Chiefs would have looked exactly like a
  legitimate FCS opponent, priced never, alarmed never. Whenever "ignore
  this" is correct for one reason, check what else it now hides.

- **Belt-and-braces belongs on the output, not the input.** George asked for
  a second validation pass as a safety net. Measured, the same triple
  validated from either side can't disagree — 0 differences over 1,001
  splits, because addition commutes. The check that *does* earn its place
  is on the result: the two teams' expected values must sum to exactly
  $5.00. That catches swapped sides, broken repairs and a wrong payout
  constant, none of which double-validation would see. **The instinct was
  right and the mechanism was wrong — worth separating those.**

- **⭐ The per-game breakdown cancels out of the price.** Because every win
  pays a flat $5, the sum of per-game win probabilities and the total
  expected wins are the same number times five. Nine months of "we need a
  probability for all ~2,400 games" turns into "we need 170 numbers." The
  hard problem was an artefact of how the formula is written, not of what
  the formula needs. (George.)

- **A betting line is not a forecast.** The over/under is set where the money
  balances, which makes it the *median* outcome, not the mean — a different
  number, and worth up to a few dollars a share on a ~$57 share when our
  whole spread is $0.10. And these particular lines are known to be biased:
  too high for very strong teams, too low for very weak ones, missing final
  records by ~2 wins on average (Woodland & Woodland 2013). Using market
  data is fine; **using it without knowing what object it is** is not.

- **A frozen input can cancel a live one exactly.** Season win totals don't
  move during a game. Subtract the current live probability from one and the
  in-game price movement vanishes completely — $60.00 at 60%, $60.00 at 90%.
  It would have looked like a working system with a dead price. Whenever
  two terms are derived from overlapping information and one is stale, check
  whether the update is being subtracted from itself.

- **"Not in the feed" and "doesn't exist" are different findings.** Our
  16-07 pull proved SR's NCAAFB futures feed has no win totals. A research
  agent then reported the market is near-universal across all five books SR
  already sources, and concluded our evidence must be wrong. Both were
  right — the market exists, SR just isn't carrying it. That distinction
  turns an impossible ask into a coverage complaint, and it's the difference
  between building a model for 138 teams and sending an email.

## 2026-07-24 (b) — build day + ingestion research

- **Measure the feed; don't reason about it.** We recorded twice that SR
  probabilities move "per play, ~30–40 s" — plausible, repeated, and wrong by
  an order of magnitude. Counting gaps in our own captured game gave a
  **4 s median**, because win probability decays with the game *clock*, not
  only on plays (~6–7 updates per play). The 2 s conclusion survived, but the
  *reason* inverted — 2 s matches the median rather than oversampling. Any
  claim about a feed's behaviour should come with the measurement.

- **"Is there a push feed?" is answerable definitively, and worth answering.**
  Four independent checks (schema, 414 captured messages, published contract,
  vendor docs) beat one plausible assumption. Answer: SR has no probabilities
  push product for **any** sport — pull only. Knowing that is worth more than
  a faster guess, because it closes an architecture debate permanently.

- **Fan-out planes have contracts; pick the one whose contract you need.**
  Centrifugo is at-most-once, history off, recovery-by-refetch — perfect for
  showing a phone the score, disqualifying for a price input whose recovery
  path must never be "go fetch something". Backend-to-backend belongs on the
  durable bus. Same layer, same data, wrong contract.

- **A cache is not a feed.** The SR service's Redis probability keys look
  like a free push source and are actually TTL cache-aside artefacts, written
  only when a *user* happens to hit the API and refreshed by nothing. "The
  data is in Redis" says nothing about whether it's current.

- **Placeholders travel as facts unless you label them.** A "50 msg/s"
  governor from a colleague's message became, in my head, "our budget" — and
  briefly promoted diff-publishing from optimisation to requirement. It was a
  placeholder; the venue spec contains **no rate language at all**. Check
  where a number came from before designing against it.

- **Verify a vendor claim against the vendor's own document.** Two minutes
  with the tZERO PDF confirmed ClOrdID ≤20/no-leading-zeroes, revealed that
  replace and cancel each carry **two** such ids, and confirmed the odd
  `HandlInst` asymmetry (banned on new orders, mandatory on replaces). It
  also proved a negative — no rate limits documented — which redirected T2
  from "read the spec" to "ask tZERO with T1".

- **Golden fixtures are cheap certainty.** The spec shipped one worked
  example for the quantity seed; reproducing it byte-exact before writing
  anything else validated both the document's precision and our reading of
  it. Do this first with any spec that ships fixtures.

- **Keep the translator pure and the fetcher separate.** The SR adapter takes
  parsed data and returns envelopes — no network, no clock. So a captured
  game is a deterministic test input *and* the live poller inherits an
  already-proven translation path. The messy part (retries, quota, timing)
  stays quarantined in the part that can't be unit-tested anyway.

- **Enforce invariants at the border, not in the middle.** Floats are refused
  by the money/probability constructors, by the payload hasher, *and* by
  parsing SR's JSON with `parse_float=str`. Three chokepoints mean no code
  path downstream has to remember the rule.

## 2026-07-24

- **A written spec can overturn call decisions — the protocol held.** The
  v1.3 Build Spec contradicted three things Edwin said five days earlier
  (lifecycle, cadence, probability source). Because the rule is "surface
  every conflict, never silently adopt", they became E17–E19 instead of
  silent rewrites. The doc is the baseline; the conflicts stay visible.

- **"Priced" = probabilities published, and SR prices rolling.** A game can
  be scheduled without being priced; SR attaches probabilities as games
  approach (NCAA: 70 of ~1,700 today). Consequence: full-season Σ GEV(g) is
  impossible from SR alone — and since Σ P_win(g) ≡ expected remaining wins,
  the fix is a source swap for the unpriced tail (SR win-total futures, or
  InPlay-internal weekly — Edwin's original model), not a formula change.

- **Polling rate ≠ cycle rate.** The probability only moves per play
  (~30–40 s). The decision cycle reads memory at any speed; the poller polls
  at the freshness band (~2 s per live game). Edwin's 200 ms and the spec's
  2 s stop being a fight about polling — the remaining question is purely
  how fast the *cycle* must react (E18).

- **Derive the quota ask, don't guess it.** Freshness band × concurrent live
  games × season = the number: per-game polling on the current product ≈
  2.5M calls/mo at ~20 QPS peak; the v2 product's live-bulk endpoint (all
  live games, one call) ≈ 200k/mo at 0.5 QPS. The product choice IS the
  quota ask (S7).

- **Probe the real API before trusting any requirement on it.** Thirty
  minutes with the trial key found: no tie probability exists (spec requires
  it, forbids inferring it → S6), NFL's seasons listing is empty but the
  date-schedule endpoint prices it fine, and 403 means per-product
  entitlement, not a broken API.

- **Verify golden fixtures on arrival.** The spec's SHA-256 quantity-seed
  fixture was reproduced locally before adopting anything else in the doc —
  cheap, and it certifies both the doc's precision and our reading of it.

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
  order queries + removal, not venue tech (Troy checking T0's self-match
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
  an update keep queue position?) can only be answered by T0 directly or by
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
