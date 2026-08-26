---
description: "The as-built quoting page — σ², width, the ladder, quantities and variation, and the publish-or-hold gate with the LIVE 500 ms carve-out"
---

# Build — Quoting

> Part of [[market-maker/build/index|As Built]] · Code: `mm/quotes/` ·
> Spec: Ch 5, RE-CUT by the ASMM-1 adoption
> ([[market-maker/asmm1-adoption-spec]], 30-07b): Edwin's
> volatility-driven width replaced §5.2's spread table (whose state
> classifier was never built). §5.3/§5.4/§5.6's price rules survive
> unchanged.

RM in, a validated Target Order Book out. Five pieces, in pipeline order.

## 1 · σ² — the volatility number (`volatility.py`)

One exponentially-decayed variance rate per security:

    r  = |RP − RP_prev| ÷ tick             the move, in ticks
    V ← V · exp(−ln2 · Δt ÷ h)             decay; half-life h = 20 s
    v  = r² ÷ Δt                           what this move implies
    V ← v  if v > V   else  ½V + ½v        asymmetric blend
    σ² = clamp(V · H, 0.05, 400)           horizon H = 30 s; ticks²

- `V` is a RATE (ticks²/second); `σ²` is ticks² over the horizon.
  Confusing the two is the easiest mistake in this module.
- The blend is deliberately asymmetric: spikes land whole, calm decays
  gradually — a ratchet, like §3.4's.
- **Cold start: the first σ² reads at the CEILING** (V₀ = ceil ÷ H — the
  ceiling is on σ², not V). Wide-when-ignorant is the safe direction;
  book-visible on day one, so Edwin's sign-off rides E31.
- A dead feed produces LOW volatility — which is why Invalid status gates
  the cycle BEFORE σ² ever updates (see
  [[market-maker/build/valuation|Valuation]]).

## 2 · Width (`width.py`)

    risk_width  = γ·σ² + C            γ = 0.02 · k = 1.2
                                      C = (2/γ)·ln(1 + γ/k) ≈ 1.653 ticks
    price_scale = clamp(RP ÷ $65, 0.6, 1.6)
    width       = ceil( clamp(risk_width, min, max) + extra·price_scale )
    bid_off     = ⌊width ÷ 2⌋ · ask_off = width − bid_off

- C is a CONSTANT (γ and k are constants) — computed once; a new γ must
  recompute it.
- The extra (0–3 ticks) is seeded from the §5.7.3 hash — never
  `random.Random` — ADDED, never max'd, and only IT scales with price.
  The odd tick's side is a stateless seeded 50/50 from the same draw.
- ⚠ **The equation has no wide end**: the σ² ceiling caps width at
  ~10 ticks + the extra — about $0.13 on a $65 team, ever — against
  §5.2 Defensive's $0.40 and the indicated overnight $2.50–$5.00.
  ⭐ **Filled 20-08 (E51 answer 6):** `state_floor_ticks` is wired in
  both engines — Defensive **50**, Overnight **100**, the WIDEST wins,
  applied AFTER the extra so a floor is exact. 100 sits above
  `max_width_ticks` 60 on purpose: the cap bounds what volatility may
  justify; a floor is a refusal to be tight while blind.
- ⭐ **`min_width_ticks` is 25 since 20-08** (E51 answer 1, was 1): a
  $0.25 baseline that leaves 12 postable prices a side. It binds BEFORE
  the extra, so the realised spread is 25–30 ticks. `k` untouched.

## 3 · The ladder (`ladder.py`)

    levels = 1–3 · step = 1–4 ticks       drawn, seeded (two draws)
    bid₁ = ⌊RM − bid_off·tick⌋            round DOWN (outward)
    ask₁ = ⌈RM + ask_off·tick⌉            round UP (outward)
    walk outward by step · every price in [$0.01, MEV] · dedupe

- ✂ **1–3 rungs since 26-08** (George, Python `f9eec8b` · Go
  `feat/e51-parameters`), superseding Edwin's 20-08 "one rung, do not
  build the optionality": the live one-rung book showed a bitten rung
  stays bitten (floor + N10 + unbuilt §5.9). Was 3–6 at the pin.
  ⚠ Book-visible — Edwin to be told.

Rounding is always OUTWARD — a rounding error may widen the book, never
cross it. A book that cannot be two-sided inside the bounds returns
**Suspended — a typed result, not an exception** (a normal state the
cycle handles).

## 4 · Quantities (`quantity.py` + `variation.py`)

    base_i = 550 × 0.72^i                 i = 0 at the inside
    buy    = base × (1 − EPR)             long → show less buying
    sell   = base × (1 + EPR)             long → show more selling
    pre    = round( base × modifier )     to the nearest share
    final  = clamp( round( pre × VF ), 100, 15,000 )

- ✂ **550 at the touch since 20-08** (E51 answer 3, was our 10,000): a
  participant selling 1,000 into a 550 bid leaves 450 as their own
  offer, so the market moves. The 100 minimum (George 20-08, was
  §5.7.3's 1,000) is a backstop — the touch draws 412–688 and the old
  floor clamped every draw straight back up. `material_qty_change` is
  50 (was 500) for the same reason.
- The geometric ×0.72 decay is Edwin's (adopted).
- ⭐ **In Go these rows are a `Policy` read off the dictionary at
  construction, not package literals** — because every corpus under
  `testdata/` is Python@fd193a4's output and needs the pin's 10,000 /
  3–6 / 1,000. `config.ReferencePin()` holds them; the differential
  harness resolves the dictionary from the corpus manifest's commit.
  ✅ **The touch-heavy profile STANDS** (George, 08-11c, after his own
  challenge from the live books): fattest-at-the-touch is Edwin's
  deliberate design for a liquidity-first, non-profit-seeking maker.
  The inverted tree (thin at the touch) was built, merged and REVERTED
  the same hour (MM PR #19, revert `b86ca83`, never deployed); the
  branch remains ready if the ruling ever flips. Residual for E31:
  does fattest-at-the-touch hold in LIVE, where a fat touch is
  pickoff-exposed between 500 ms updates?
- **VF is §5.7.3's seeded variation** — SHA-256 over named context,
  byte-exact against the spec's golden fixture, keyed on the Quote
  Version so replay reproduces every draw.
- ✂ **The quantity grid is DROPPED since 15-08 (`qty_increment` 1, was
  §5.7.3's 500)** — MM #36, decisions 2026-08-15, not merged/deployed
  under the freeze. On the 500 grid every size ended in 000 or 500 and
  the book read as machine blocks; George's ruling: ANY visible grid
  reads as an inactive book, so sizes are raw integers (12,433 ·
  8,617 · …), like a book carrying partial-fill remainders. The
  rounding step survives in code — one row restores any grid. The §5.8
  materiality threshold stays 500 sh, so the finer basis can only
  publish LESS often. Book-visible → Edwin round.
- ⚠ The 15,000 ceiling binds exactly where distribution needs room
  (N20's other face).

### 4b · The ask cap — what we may legally sell (R-Q08 / R-V07)

    capacity = holding − livS
    holding  = opening position + net position (§4.1)
    livS     = committed sell quantity the next pass cannot reclaim

The ask ladder is **RESIZED** into that bound, never rejected — tZERO
refuses a sell over `Pos − livS` as a WHOLE order, so an unbounded ladder
loses the entire ask side of a book rather than one rung. Levels are paid
inside-out (the touch keeps its shares); each capped quantity is FLOORED
to the 500 increment; a level that cannot reach the 1,000 minimum is
DROPPED, because §5.10 rejects a sub-minimum level and a failed check
blocks the whole book.

- **livS EXCLUDES `ACTIVE` and `PARTIALLY_FILLED`.** Those are the
  reconciler's `_ACTIONABLE` set — the ladder REPLACES them
  (rest-until-gone keeps a still-wanted rung, a moved price replaces it),
  so counting them would double-count the ask side against itself and
  make a fully-offered book empty and re-offer on alternate passes. It
  counts `PENDING_SUBMIT` / `PENDING_REPLACE` / `PENDING_CANCEL` /
  `UNKNOWN`, a replace at **max(old remaining, new remaining)**. ⚠
  Deliberately NOT §4.4's `_EXPOSURE_STATES` — a different question,
  pinned apart by test.
  - ⚠ **Both operands must be REMAINING shares** (review MED-1, 08-15).
    `pending_quantity` is a FIX TOTAL — "CumQty + the rank's draw",
    because the gateway requires a replace quantity above CumQty — while
    `leaves_qty` is what remains. Comparing the two directly counts the
    filled shares twice: once in livS, once through the journalled net
    position those same fills already reduced. A 10,000-share sell with
    6,000 filled, being repriced, contributed 10,000 to livS instead of
    4,000 and cost the book 6,000 shares of capacity. It bit hardest on
    the books that are actually trading. The destination is now counted
    at `pending_quantity − cum_qty`.
- **A capacity ≤ 0 empties the ask side; the bids are untouched.** ✂ A
  documented one-sided state: R-Q01 yields to R-V07, because no ask we
  could post would survive the venue. Announced once per episode
  (`ASK_CAP_NEGATIVE`), never per cycle.
  - 📟 **Operator: `ASK_CAP_NEGATIVE` re-fires once per affected book after
    a restart, and that is deliberate.** The edge flag `_cap_alarmed` is
    in-memory and is deliberately NOT checkpointed — keeping it out of
    engine state is part of what makes the cap replay-identical (AC9). So
    a restart with the bound still negative re-announces every affected
    book once. A burst of `ASK_CAP_NEGATIVE` lines straight after a boot
    is the expected shape, not a new incident. Read it as a census of the
    books that are still short, and escalate only if the same book keeps
    re-firing WITHOUT a restart, which would mean the bound is flapping.
- 🔴 **Inert today.** `opening_position_shares` is 0 (🟡/E27) and 0 means
  UNKNOWN, not "we hold nothing", so the bound **fails open** and says so
  at boot (`ASK_CAP_UNBOUNDED`). Enforcing it at the stub would take every
  book bid-only — R-V07's `Pos` is the VENUE's position and our journal
  starts at 0 (the 14-08 IPTCJETS −197 case). One real number turns it on.
  George's call — N42.
- The bound lands AFTER §5.8's decision and every §5.7.3 draw, on the
  final quantities only, so it changes no price, no version and no
  checkpointed field — AC9 by construction, exactly like R-Q09's guard.
- ⚠ Sizing is only half of R-V07. The venue applies the rule per order at
  SUBMIT time, so the converger must also never land new sells on top of
  old ones it is about to cancel. Not built — `venue/sync.py`.
- ✅ **The bound now survives the reconciler** (review-002 HIGH, 08-15).
  A mint-time cap governs an INTENTION; R-V07 measures what SETTLES.
  Rest-until-gone keeps a standing rung at its OWN size and a pass-2
  replace adopts the new rank's size, so the settled ask side reached
  **27,000 sh against an 18,000 sh holding**. The cap now RESERVES the
  rungs the reconciler will keep — at `max(resting, target)`, from
  `resting_ask_quantities` over the `_ACTIONABLE` states — before it
  sizes the levels that will actually be sent. A grid test asserts
  settled commitment ≤ capacity across five prices and five bounds.
  - ⚠ **Residual, open:** if the KEPT rungs alone exceed the bound, no
    target fixes it — only a cancel does, and cancelling a still-wanted
    rung is N10's to revisit. Cannot bite while the cap is dark; must
    close before N43 activation.
- ⚠ **The bound binds the TARGET, not the standing book.** Rest-until-gone
  (N10) keeps a resting order at a still-wanted price at its OWN quantity
  — never topped up, never trimmed — so a book legally offered at a larger
  holding can sit ABOVE a bound that has since tightened; the cap declines
  to add to it but will not bring it down. No venue rule is broken (R-V07
  applies per order at submit, and that order was accepted when sent).
  Trimming would mean cancelling a still-wanted rung — Edwin's ruling,
  not the cap's call. Pinned by test so it stays visible.

## 5 · Publish or hold (`quotes/engine.py`, §5.8 · §5.10 · §7.5)

- **Material change is the publish trigger** (§5.8): IA moved
  ≥ $0.005, or a quantity basis moved ≥ 500 shares. **Materiality is
  judged on the PRE-variation shape** — final sizes are freshly drawn
  each version, so comparing them would republish every cycle.
  ✂ **LIVE carve-out (George 08-11, `[live-timer]`, MM PR #16): in-game
  an immaterial cycle still publishes once 500 ms have passed since the
  last publish** — "new orders every 500 ms, changed or not". The sweep
  runs at the same 0.5 s (✂ §3.1.4's 2.0 s) and is the quote pulse;
  the tick is 0.5 s. Non-live states keep the pure §5.8 gate, proven by
  test at the same offset.
- **The ASMM-1 dwell only PERMITS a reshape** (N26): an expired dwell
  changes nothing by itself — the new shape rides the next
  justified publish, at zero extra venue messages. ✂ **The LIVE dwell
  row is 0–0 (George 08-11, was Edwin's 3–12 s)**: every LIVE publish
  re-rolls the shape, so re-rolled offsets move rung prices and the
  reconciler genuinely replaces orders — rest-until-gone survives for
  the rare same-price rung. Book-visible: Edwin sees the collapse in
  the E31/E17 round.
- **The Quote Version increments only on publish**; a held cycle
  consumes nothing (every seeded draw hangs off the version — this is
  what makes replay exact).
- **The §5.10 check battery runs every cycle** (sixteen checks; 1/5/12
  record their status — 5 and 12 are UNAVAILABLE pending the §5.5
  participant-book feed). The triggering Accepted Event Sequence is
  threaded through `cycle()` onto the Target Order Book (§7.5) — event →
  RP → book is traceable end to end.
- Headline proof: two fresh engines fed the same six events produce
  **byte-identical books, version chains and check reports**.

## What changes here next

[[market-maker/build/next|Next]]: E31 (width floors, σ² bounds, cold
start — Edwin's values into existing slots) · §5.5 public-book checks
(needs the participant book feed) · §5.9 replenishment (E17 decides the
lifecycle) · E18's one remaining ask (reaction bound vs visible churn).
