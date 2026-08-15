---
description: "The as-built valuation page — RP, Edwin's on-field leg, the F2 anchor seed that carries kickoff freezes across a fresh journal, and freshness/status/confidence"
---

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
  ⚠ **The mid-game rebase edge (found live 14-08, the BENG/LION
  triage) — ✅ FIXED by the ANCHOR_SEED, MM PR #32, not yet deployed.**
  On a FRESH-JOURNAL boot while a game is already in play, the engine
  has no kickoff anchor, so `[late-arrival]`
  (`mm/valuation/engine.py`) freezes `p_ref` at the CURRENT
  probability. Every fresh-journal cutover during a live game therefore
  ERASED the accumulated in-game move and snapped the book back toward
  seed — supervised27 froze BENG at 0.866 instead of the 23:03Z
  kickoff anchor 0.711 (live adjustment −$0.09 instead of +$0.69,
  $0.685 a share; up to $5 in the regular season). On a decided game
  (probability saturated) the book then looked frozen.
  George ruled BOTH halves: the operating rule (R11 — no maker
  cutovers while games are live, landed 14-08) and the carry fix. The
  carry fix is the **anchor seed** below. `[late-arrival]` is
  unchanged and is now the deliberate fallback, for the two cases the
  seed cannot cover — see **The anchor seed** below.
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

## The anchor seed (F2 — `mm/events/anchor_seed.py`)

⭐ **BUILT 14-08 (MM PR #32), not yet deployed.** How a kickoff freeze
crosses a fresh journal. A freeze is DERIVED state — it exists only
because the engine watched the game cross its kickoff — so a journal that
watched nothing can never re-derive it. The fix carries it as a FACT.

- **One journalled event.** At boot the composition reads the PRIOR run's
  directory once (`MM_PRIOR_RUN_DIR` → the `prior_run_dir` dictionary
  slot) and journals ONE `ANCHOR_SEED` FIRST. Everything after that is
  ordinary: replay reads the anchors out of the journal, and no boot ever
  reads the prior run twice. `ANCHOR_SEED` is the twelfth event type,
  ours — flagged for the N23/N28 blessing round with the sweep and the
  session boundary.
- **Two sources, deliberately** — the newest prior checkpoint, THEN the
  prior journal's tail folded on top. Checkpoints are hourly, so the
  kickoff itself routinely lands in the tail; a checkpoint-only seed
  would miss exactly the games that matter. The tail is folded through a
  throwaway `ValuationEngine` rather than a second copy of the freeze
  rules — one place for them, and the §2.5 universe filter comes free.
- ⚠ **NOT `load_latest`.** The strict checkpoint loader rejects on
  config_version AND schema_version, and R-D06 bumps the config version
  on every deploy — so a seed built on it would have returned empty every
  time, silently, for ever (review H1). The lenient reader verifies the
  integrity hash ONLY, extracts what parses, and names every degradation
  for the operator's log.
- ⚠ **Hash-valid is not trusted** (review-f2, 14-08). The integrity hash
  proves the bytes are what was written; it says nothing about whether
  the VALUES parse under this build. So every candidate game is proved by
  constructing the real `GameBelief` (`belief_from_anchor` — the one gate
  the reader and the apply path share) before it can enter the payload. A
  game that fails is noted and skipped; the rest of the checkpoint still
  seeds. Without that, `status: "in_play"` or `x: "not-a-number"` in a
  hash-valid prior run stopped the engine BOOTING — the opposite of what
  the anchors are for. The rule is read-side ONLY: a journalled seed is
  replayed at every future boot, so one that raises on apply would kill
  that journal permanently. On any unexpected fault the composition mints
  NOTHING and stays re-mintable.
- **A missing prior directory is an alarm, not a skip.** A seed can be
  minted once per journal (minting is what makes the journal non-empty),
  so a typo'd `MM_PRIOR_RUN_DIR` used to mint an empty seed and burn that
  one chance for ever. It now journals nothing, logs `FAILED`, and the
  corrected setting still seeds on the next boot. A directory that exists
  and holds no games still mints an honest empty seed.
- **The seed is the weakest fact in the machine.** It applies per game
  only where no belief exists, so anything the journal already knows
  outranks it — which is why a fresher reading's kickoff_time beats the
  seed's through the ordinary path, keeping the frozen `p_ref`. A game
  that FINISHED during the outage seeds its result, and `[settled]` then
  keeps it closed against a late reading.
- **It publishes no price.** Found the hard way while building: a
  publishing seed made the quote engine record a ladder that replay
  discarded, so the venue got an EMPTY book until a dwell expired. §3.1.5
  publishes on real change and at boot there is nothing to change from —
  the composition stands the book immediately afterwards.
- Three gates, each printing its reason: no prior directory · this
  journal is not empty · the prior directory IS this run's.

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
on p_ref (one line to change) · N23's event type for T · E38's blessing ·
the anchor seed's deploy (`MM_PRIOR_RUN_DIR` is owed to
`runtime/__main__.py`'s env table and the redeploy runbook first).
