# Quoting Engine (SDMM)

> **Component:** [[market-maker/market-maker]]
> **Standard:** [[standards/PTS-001-simulated-designated-market-maker-standard|PTS-001]] · guides: [[standards/PTS-001-plain-english-guide]] · [[standards/PTS-001-comprehensive-guide]]
> **Status:** v1 model set (23-07 MM call) — pricing numbers owed; fill-response logic (N14) to design
> **One-liner:** The bot. Turns a Reference Price + a profile into two-sided limit-order ladders resting in tZERO's book — refreshed ~200ms during live games, every 30–60s otherwise — skewed to shed inventory. v1 mantra (Edwin): "really simple to start."
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

## The Entity (in tZERO)

- A **synthetic market-maker entity inside tZERO** — technically the same as a
  user account, with two differences: effectively **unlimited buying power**
  (~$100M+, Edwin: "never a limit"), and **exemption from short-locate
  restrictions**. (Source: standup 2026-07-20)
- **Ask in flight:** tZERO to stand up this entity in the **QA environment** so
  testing can start (Tue/Thu tZERO calls).
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
  → publish  (cancel-replace into tZERO)
  → commit   (immutable record for replay)
```

- **Cadence bifurcated by game state (23-07):** live games ~**200ms per
  call** ("a second's too long") · non-live **every 30–60s** · **earnings
  windows** (Tue NFL / Wed NCAA): all ~170 symbols for ~5 minutes. Supersedes
  the flat 5–10×/sec framing — steady-state load is small.
- **v1 quote lifecycle (23-07, supersedes everything earlier):**
  - A partially-filled resting order is **never topped up** — it rests until
    completely gone (500 → 87 → 55 → 0).
  - **Price moves:** cancel the old level, post the **remaining** quantity at
    the new price.
  - **Full fill at unchanged price:** reload at top of book (randomized size).
  - **Publish is post-first:** don't wait for cancel confirmations; a
    momentary self-cross during an adjustment is acceptable in v1 (Edwin:
    "on the first iteration… I don't care"; George confirmed 23-07).
- **Fill-response logic is the open design surface (N14):** "if you get a
  fill, what do you do next?" — e.g. outside games, get filled at 6 → maybe
  leave the bid and let the ladder fill down rather than instantly re-quote.
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
- **Randomizer = quantities ONLY (narrowed 23-07):** price is purely
  algorithmic — no price randomization. Quoted sizes (especially top of
  book) randomized so the book doesn't read programmatic — bounded, *seeded*
  (replayable). The occasional randomized **aggressive order** Edwin
  described (deliberately moving price to exit inventory) remains
  out-of-scope for v1 pending bounds (E8).
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

Fills against MM quotes come back from tZERO as execution reports → inventory
changes → next cycle's skew. This closed loop is what keeps the maker from
accumulating a runaway position while never leaving the market.

## Determinism & Replay

Same inputs + version → identical quotes. No wall clocks, seeded randomness
only, event-sourced state. Record everything from day one; replay *tooling*
can come later (scope call for Thursday).

## Special Responsibilities

- **IPO buyer (firmed 23-07):** the MM buys at **every IPO** — when buyers
  are short, and to balance how many shares get pushed into the market.
  Edwin: **"we're going to start with the IPO"** — sequencing signal; fuller
  session promised. Earlier framing (float warehousing, max clips ~50k,
  ~35–50% guarantee) stands as the mechanism sketch; tZERO ledger mechanics
  open (T6). (See [[ipo-module/ipo-module]])
- **Load-balancing vs market-making algo split** (named 17-07) — boundary
  unclear, clarify Thursday.

## Open Items

Tracked in [[market-maker/open-questions]] / [[market-maker/parameters]]:
all pricing parameters (spreads, λ, ladder geometry, sizes), quote-replace
throughput ceiling on tZERO's FIX session, aggressive-order bounds, calibration
approach, week-zero policy.
