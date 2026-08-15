---
description: "The as-built position page — net position, position ratio, pending exposure, the inventory skew and the reservation midpoint, plus the two external holes"
---

# Build — Position

> Part of [[market-maker/build/index|As Built]] · Code: `mm/position/` ·
> Spec: Ch 4.

Inventory into a skew: what we hold, how exposed we are, and how hard the
book leans to shed it.

## The equations

    NP  = OpeningPosition + Σ fills + CorporateAdjustments      §4.1
    PR  = NP ÷ ReferenceFloat                                   §4.3
    EP  = NP + pending buy exposure − pending sell exposure     §4.4
    EPR = clamp( EP ÷ ReferenceFloat, ±0.50 )                   §5.7.2
    IA  = −Clamp( PR × S, −M, +M )      S = $1.00 · M = $0.25   §4.5
    RM  = RP + IA                                               §4.6

- **Reference Float = issued − treasury**: 900,000 NFL · 1,000,000 NCAA
  (IPO Requirements v2, gospel). ⚠ N21: 18 rounds × 50,000 offers only
  900,000, so 100,000 NCAA shares per team never reach a window — issued
  or treasury changes every NCAA ratio by ~10 %.
- **Average cost and P&L (§4.2):** the three cases (add to a position,
  reduce it, cross through zero) are built and tested; realized and
  unrealized P&L follow.
- **RM is floored by §5.4's MEV machinery** — without the floor RM goes
  negative on extreme skews.

## Pending exposure — the timing rule

**Exposure begins at the DECISION to send.** Intent registers with the
Venue State Record BEFORE an instruction is published, because the
gateway never acknowledges that a message merely reached it (malformed
JSON is a silent drop) — register-first is the only order that never
understates exposure. Partially Filled orders count: their remainders
still rest (the spec's §4.4 state list omitted them; ours includes them,
recorded).

## The two known holes (both external)

- **E27 — the opening position has NO publisher.** §7.3 reserves
  `IPO_ALLOCATION` (the shape exists); nothing publishes it. The IPO runs
  on the primary plane and never touches the venue, so somebody at
  InPlay must tell us "you were allocated N shares of team X" before
  secondary opens. This is the ENTIRE day-one book — up to 85 M shares
  (~$4.26 bn) depending on E24's round-count answer. Until then the
  opening position is a construction argument.
- **N20 — the skew saturates before we start.** IA stops responding at
  25 % of float (PR × $1.00 clamped at $0.25); post-offering we hold
  50–100 %. Holding the whole float reads identically to holding a
  quarter of it — the skew is our only distribution tool and it is
  pinned. Reframed by George: distribution matters because a market with
  no shares in circulation is not a market, not because of risk.

## Deliberate properties

- **Inventory never prevents quoting** (§4.1) — we are the mandated
  buyer; ASMM-1's one-sided guard was rejected for exactly this reason.
- **EP is allowed in quantities and NOWHERE near a price** — the
  position-side modifier shapes SIZES (§5.7.2); prices lean only through
  IA's bounded ±$0.25. (E34 records the structural consequence: the
  crowd cannot move the price outside that band ahead of evidence.)
- `CORPORATE_ACTION` is built because the formula has it; expectation is
  it never fires (E28, with T12 on the venue side).

## What changes here next

[[market-maker/build/next|Next]]: E27's publisher (day-one blocker) ·
E24 (the mandate round count — $3.4 bn of ambiguity) · E26 (may the MM
short?) · N20/N21 answers.
