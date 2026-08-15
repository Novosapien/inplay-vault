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
  §5.2 Defensive's $0.40 and the indicated overnight $2.50–$5.00. The
  per-state width FLOOR slot exists (`state_floor_ticks`, one call-site
  to wire) awaiting Edwin's E31 values.

## 3 · The ladder (`ladder.py`)

    levels = 3–6 · step = 1–4 ticks       drawn, seeded (two draws)
    bid₁ = ⌊RM − bid_off·tick⌋            round DOWN (outward)
    ask₁ = ⌈RM + ask_off·tick⌉            round UP (outward)
    walk outward by step · every price in [$0.01, MEV] · dedupe

Rounding is always OUTWARD — a rounding error may widen the book, never
cross it. A book that cannot be two-sided inside the bounds returns
**Suspended — a typed result, not an exception** (a normal state the
cycle handles).

## 4 · Quantities (`quantity.py` + `variation.py`)

    base_i = 10,000 × 0.72^i              i = 0 at the inside
    buy    = base × (1 − EPR)             long → show less buying
    sell   = base × (1 + EPR)             long → show more selling
    pre    = round500( base × modifier )  halfway rounds DOWN
    final  = clamp( round500( pre × VF ), 1,000, 15,000 )

- The geometric ×0.72 decay is Edwin's (adopted); the 10,000 base is
  ours (his 250 was 40× too small for the mandate's inventory).
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
- ⚠ The 15,000 ceiling binds exactly where distribution needs room
  (N20's other face).

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
