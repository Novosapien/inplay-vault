# Build — Valuation

> Part of [[market-maker/build/index|As Built]] · Code: `mm/valuation/` ·
> Spec: Ch 3 · Superseded where noted by Edwin's 28-07 email
> ([[market-maker/decisions]] outranks the spec).

What a share is worth, right now, according to us. Everything downstream
is "quote around this number."

## The Reference Price (§3.1.1)

    RP = ROF + Σ GEV(g) + RAV + EAV

Realized on-field (money banked from finished games) + expected value of
unfinished games + realized and expected off-field. It is this simple
because settlement is: a share pays `FSV = realized on-field + realized
off-field` (§11.3), so RP is a live estimate of that number.

**✂ The on-field leg is SUPERSEDED** by Edwin's 28-07 formula
(`reference_price.py::on_field_value`):

    on-field = $5 × ( T − Σ p_ref(g) + Σ x_g )        over g ∈ G

- **T** — the whole-season expected wins, from Edwin's daily file.
  Without T a security has NO price: the code refuses to construct one
  (`[t-required]`).
- **G** — a SET of games: a game enters at kickoff and leaves when a new
  T absorbs it (so the adjustment survives the final whistle).
- **p_ref(g)** — the game's pregame win probability, frozen **at
  kickoff** (the closing pregame number — George's interim ruling, N22).
  Known consequence: pregame news between 06:00 and kickoff stays inside
  T until the next file (~13¢ on a plausible NFL example).
- **x_g** — the game's current probability (live), or its realized value
  once final (win 1 · tie 0.5 · loss 0).

Why this shape: a season win total already CONTAINS every game, so per-
game GEVs would double-count; and because every win pays a flat $5, the
per-fixture breakdown cancels — 170 numbers replace ~2,400 per-game
probabilities. The subtraction removes what T assumed about a kicked-off
game; the addition puts back what the game is actually doing.

**Mechanics that were bugs once (regression-guarded):**

- A new T reaches the book on ITS OWN event, never one event late
  (`[no-smoothing]` — "do not smooth the mid" is Edwin's own rule).
- The pair invariant: one reading prices BOTH teams, and the two on-field
  adjustments cancel — the pair's game values always sum to the game's
  full $5.00.

## Per-game expected value and settlement (§3.1.2, §3.1.3)

    GEV(g)   = P_win × $5.00 + P_tie × $2.50     (P_tie = 0 pending S6)
    realized:  win $5.00 · tie $2.50 · loss $0.00

S6 is resolved: SR's 2-way market has no tie; Edwin ruled "price the
two-way market exactly as proposed" — a tie settles at $2.50 (x = 0.5);
the ~0.4 % NFL drag is carried as a reserve, not modelled.

## Off-field (§3.6) — MOCKED

RAV/EAV arrive as static construction inputs. The methodology (the
popularity index, the $2.50-per-game pools, EST/ACT) is unbuilt and is
Edwin's world. ⚠ Known open tension (E2 residual, learnings): the
earnings component says price impact is "market-determined", but the MM
re-anchors the market at RP mechanically.

## Freshness → Status → Confidence (§3.3–§3.5, `freshness.py`)

The system that answers: is this price built from data fresh enough to
trust, and how loudly should we distrust it?

- ⭐ **The E38 deviation — live bands run on OBSERVATION age, not reading
  age.** Measured on the real game: SR sends no heartbeat —
  `last_updated` moves only when the number moves (98 % of entries);
  gaps run median 4 s · p90 28 s · **max 2,862 s = the whole of
  halftime**. The spec as written would suspend every book through
  halftime. **The rule as built (George): a successful fetch CONFIRMS
  the number.** Time since the last successful observation drives
  §3.3.1's bands — fetches landing every ~2 s → CURRENT, full status,
  through halftime and every stoppage; true silence ages through
  Warning >5 s · Degraded >10 s · **Invalid at 20 s → suspend**. On the
  bus path the observation is each message's `Fetched-At` (a duplicate
  re-offer IS a confirmation). Deliberate residues: pregame stays on
  reading age (§3.3.2 — permitted age from time-to-kickoff); a security
  with no observation EVER keeps the spec's rule. Band values are
  Edwin's, untouched — E38 carries the deviation to him with the
  measurement.
- **Status (§3.4):** one status per record, most restrictive condition
  controls. **Demotions instant; promotions earn one rung per served
  10 s dwell; a relapse resets the climb** (§3.4.1). **Invalid gates the
  quote cycle BEFORE any state is touched — including σ²**: a dead
  feed's frozen price reads as CALM to a volatility estimator and would
  tighten the book into §2.3's exact danger case.
- **Confidence (§3.5):** 0–100, deductions per condition, capped by the
  status. **Advisory — it never touches the price.**
- Overnight books do NOT suspend: a security with no game live reports
  its probability condition CURRENT — the input is not stale, it is not
  needed; the price rides T and the off-field values.

## What changes here next

[[market-maker/build/next|Next]]: off-field §3.6 (Edwin) · N22's ruling
on p_ref (one line to change) · N23's event type for T · E38's blessing.
