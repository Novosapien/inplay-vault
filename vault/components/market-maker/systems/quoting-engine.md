# Quoting Engine (SDMM)

> **Component:** [[market-maker/market-maker]]
> **Standard:** [[standards/PTS-001-simulated-designated-market-maker-standard|PTS-001]] · guides: [[standards/PTS-001-plain-english-guide]] · [[standards/PTS-001-comprehensive-guide]]
> **Status:** Architecture known — pricing parameters owed (Thursday 23-07)
> **One-liner:** The bot. Turns a Reference Price + a profile into two-sided limit-order ladders resting in T0's book, refreshed ~5–10×/sec, skewed to shed inventory.
> **Companion:** [[market-maker/systems/decision-cycle-reference]] — every function in the cycle written out as concrete pseudocode with proposed default values.

---

## Purpose

Continuously provide realistic, two-sided, executable liquidity in every team
market. Not to predict prices — to build a tradable market *around* the price
it's given. Runs as one independent loop per team — the universe is **170
symbols (32 NFL + 138 NCAA)**, but **NCAA secondary scope for season 1 is an
open Edwin question (E12)** — the economics sheet covers NFL only. If NCAA
secondary is in, peak load is an NCAA Saturday (~30–40 concurrent games) and
cadence must be **activity-tiered**: in-play books at 5–10/sec, warm ~1/sec,
cold heartbeat-only. If NFL-only, the load story is trivial (≤16 games/week,
staggered).

**Plane note (22-07):** the MM lives on the **secondary plane only** (tZERO
ATS). IPOs fill on the internal primary plane and never touch it — the MM's
IPO role is limited to warehousing unsold float delivered to it afterwards.

## The Entity (in T0)

- A **synthetic market-maker entity inside T0** — technically the same as a
  user account, with two differences: effectively **unlimited buying power**
  (~$100M+, Edwin: "never a limit"), and **exemption from short-locate
  restrictions**. (Source: standup 2026-07-20)
- **Ask in flight:** T0 to stand up this entity in the **QA environment** so
  testing can start (Tue/Thu T0 calls).
- Whether it persists into production as one of many participants is
  undecided — depends on how the challenge goes and whether external MMs sign.
- **Portfolio capital allocation (PTS-001 Ch 5) is descoped** — unlimited
  capital removes the zero-sum budget machinery. What survives is per-team
  displayed-size configuration.

## The Decision Cycle (the control loop)

```
trigger (new RP · fill · state change · session change · ~200ms heartbeat)
  → assess   (order arrival, fill velocity, inventory position + velocity)
  → price    (reservation bid/offer around RP)
  → build    (ladders: N levels/side, spacing, sizes, randomization)
  → validate (never crossed, in bands, within limits)
  → publish  (cancel-replace into T0)
  → commit   (immutable record for replay)
```

- **Cancel-replace regime:** the MM constantly wipes and replaces its quotes —
  "liquidity lag". Baseline ~**5–10×/sec** plus **event-triggered
  recalculation** (touchdown → recompute now, then resume baseline). It does
  not wait to be traded against. (Source: standup 2026-07-20)
- Cycles never overlap; multiple triggers mid-cycle batch into the next one.

## Pricing

```
reservation bid   = RP − (base spread + inventory skew + activity adj + protection adj)
reservation offer = RP + (base spread + inventory skew + activity adj + protection adj)
```

- Offsets are per-side and **need not be symmetric** — skewing is the point.
- **Inventory skew** (the one mechanism to internalize): `skew = λ ×
  inventory% of float`. Long → bid backs away (accumulate less) and offer
  drops toward RP (shed inventory). Short → mirror image. Edwin's example: long
  heavy → lower the offer to/toward the reference price so buyers come in and
  it can offload. (Source: standup 2026-07-20)
- Control-engineering reading: a setpoint controller mean-reverting inventory
  to ~flat, with gain λ scheduled by regime (pricing profile).
- **Ladders:** N levels per side, spaced by the profile, budget spread across
  levels by normalized weights, most size near the top.
- **Randomizer:** quoted sizes randomized so the book doesn't read as a
  machine (no 500/500/500 lots) — bounded, *seeded* (replayable). Occasionally
  a randomized **aggressive order** deliberately moves the market: e.g. long
  50k wanting 10k → buy another 10k aggressively, rip the price higher, then
  sell the excess into the backfilled higher prices. (Source: standup
  2026-07-20 — this goes beyond the doc's passive quoting; needs its own
  bounds.)
- **Ticks:** bids round down, offers round up — rounding widens, never
  crosses.
- **Limit orders only** — everything stays a limit order, but a limit can
  **cross**: market 7 bid at 8, want filled to 10 → bid 11 and sweep 8, 9, 10.
  Market-order behaviour without a native market-order type. (Source: standup
  2026-07-20)

## Validation (before every publish)

Bid < offer everywhere · prices within bands · sizes ≥ 0 and within limits ·
best bid + best offer always present (unless halted) · randomization in
bounds · replayable. A failed market is reconstructed, never published broken;
repeated failure → forced defensive profile, still two-sided.

## Inventory Feedback

Fills against MM quotes come back from T0 as execution reports → inventory
changes → next cycle's skew. This closed loop is what keeps the maker from
accumulating a runaway position while never leaving the market.

## Determinism & Replay

Same inputs + version → identical quotes. No wall clocks, seeded randomness
only, event-sourced state. Record everything from day one; replay *tooling*
can come later (scope call for Thursday).

## Special Responsibilities

- **IPO fill guarantee / float warehousing:** the MM warehouses unsold IPO
  float in max clips (~50k), guaranteeing ~35% (possibly up to 50%) of every
  float is consumed — the straw-buyer mechanism from the 17-06 discussion.
  Mechanics with the T0 ledger open. (Source: standup 2026-07-15; see
  [[ipo-module/ipo-module]])
- **Load-balancing vs market-making algo split** (named 17-07) — boundary
  unclear, clarify Thursday.

## Open Items

Tracked in [[market-maker/open-questions]] / [[market-maker/parameters]]:
all pricing parameters (spreads, λ, ladder geometry, sizes), quote-replace
throughput ceiling on T0's FIX session, aggressive-order bounds, calibration
approach, week-zero policy.
