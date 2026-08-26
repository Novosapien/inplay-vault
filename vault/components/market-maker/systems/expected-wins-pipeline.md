---
description: "The normative page for expected-wins pricing: seed once from de-vigged win totals, then the zero-jump absorber — equations, lifecycle, generator design, rebase"
---

# Expected-Wins Pipeline — the pricing centre

> **Component:** [[market-maker/market-maker]] · **Status:** DESIGN, ruled
> 26-08 — build this week, ⚠ games live Saturday 29-08
> **Replaces:** [[market-maker/systems/daily-reference-feed]] (superseded —
> Edwin cannot operate a daily hand-off)
> **Ruling:** [[market-maker/decisions]] 26-08 ·
> [[market-maker/sessions/2026-08-26-expected-wins-pipeline]]
> **Closes:** N18 · N19 · N23 · N22's basis-drift residual · **Opens:** E51
> **Background:** [[standards/gamecast-ev-plain-english-guide]] (the proof
> that the Gamecast is the same model) · `reference/inplay-reference-feed/`
> (Edwin's engine as code, 25 tests) · `reference/season-win-totals-170.csv`

This page is the single home for how a security's on-field price number is
produced. The session notes narrate; this page states. Update it whenever
the machine changes.

---

## 1 · The price, and the one term this page owns

    RP        =  on_field + RAV + EAV                       (1)
    on_field  =  $5 × ( T − Σ p_ref(g) + Σ x_g )   over G   (2)
    T         =  banked + expected wins remaining           (3)

- `banked` — realized wins to date, win-units (win 1 · tie 0.5 · loss 0).
- `expected wins remaining` — this page's subject. Call it **E** below.
- `G` — games kicked off since the last absorption, each carrying its
  frozen kickoff probability `p_ref(g)` and live probability `x_g`.
- RAV/EAV — off-field, still mocked, still Edwin's (E51 item d).

**No external feed supplies E after the seed.** Every change to E is one
of the four moves in §3.

## 2 · The seed — once, ever

Run **Edwin's own package** (`reference/inplay-reference-feed/`: `devig.py`
→ `rake.py` → `feed.py` validation) on the July snapshot
(`season-win-totals-170.csv`, both prices verified for all 170 rows):

    q_o = implied(P_over)    q_u = implied(P_under)         (4)
    p_o = q_o / (q_o + q_u)                                 (5)
    E   = line + σ_mkt × Φ⁻¹(p_o)      σ_mkt 2.7 NFL · 2.2 NCAA ✅ (6)

Then the **backfill**: games already played before go-live are inside the
July totals as expectations. Absorb each once at seed time — subtract its
share (§3), add its result (finals from the SR schedule, which carries
scores). After the backfill, `banked` is honest and E covers exactly the
games still to play.

The output is one journalled event:

    EXPECTED_WINS_SEED {
      snapshot: { path, sha256 },        // object in the bucket (03-08 ruling)
      teams: { ticker: E, … }            // all 170 · keys sorted · decimals as strings
    }

One event, dictionary payload — the `ANCHOR_SEED` shape. This is the only
event type the pipeline adds (the N23 answer).

## 3 · The four moves — everything E ever does

| # | Move | Rule | Price effect |
|---|---|---|---|
| 1 | **Swap** — SR prices a pregame game | the game's entry follows SR's pregame number: `E += p_SR − share` | `$5 × Δ` — real information, spread pre-kickoff |
| 2 | **Freeze** — kickoff | the tracked number freezes as `p_ref(g)`; game enters G | $0 — continuous by construction |
| 3 | **Live** — during the game | `x_g` moves with SR's live probability (G-term, not E) | `$5 × Δx` per reading |
| 4 | **Absorb** — after the final | `E −= p_ref(g)` · `banked += x_g` · `g` leaves G | **exactly $0.00** (§4) |

The whole season in one line:

    new expected wins = old + (result − kickoff probability)          (7)

— with the live form of (7) replacing the result by the live probability.

**The one-basis rule (kills N22's residual):** the number absorbed out of
E must be the number E carried for that game. The swap→freeze→absorb chain
guarantees it: one number, tracked, frozen, subtracted.

**The flat split (the share):** a game SR has not yet priced carries
`share = E ÷ games remaining` as scaffolding. The shares sum to E, and SR
replaces each share before its kickoff (SR prices every game 1–2 weeks
out), so no game is ever absorbed on an invented number and E ends the
season at **exactly zero**:

    E_final = seed + Σ(p_SR − share) − Σ p_SR = seed − Σ share = 0    (8)

⚠ Known lumpiness: a mismatch game swapping from a flat share to ~0.95
moves ~$1.25 across its pre-kickoff window. Real information, but visible.

## 4 · The absorber's zero-jump proof — the regression anchor

    before:  contribution(g) = $5 × ( p_ref(g) + x_g − p_ref(g) ) = $5·x_g
    after:   contribution(g) = $5 × ( x_g from banked )           = $5·x_g
                                                        Δprice = $0.00  ∎

| Moment | banked | E | G-term | on-field |
|---|---|---|---|---|
| Win, final | 0 | 8.40 | +(1 − 0.62) | $5 × 8.78 = 43.90 |
| Win, absorbed | 1 | 7.78 | — | $5 × 8.78 = 43.90 ✓ |
| Loss, final | 0 | 8.40 | +(0 − 0.62) | $5 × 7.78 = 38.90 |
| Loss, absorbed | 0 | 7.78 | — | $5 × 7.78 = 38.90 ✓ |

Consequences: the 06:00 sawtooth (`[t-is-not-the-field]`) cannot occur,
and absorption can fire on result acceptance — there is nothing to batch.

Corrections: a changed result is already a loud CONFLICT (§3.1.3). After
absorption the fix is a reversing entry — `absorb(g)⁻¹` then `absorb(g)`
with the new x. The ledger is append-only.

## 5 · Durability — the journal is the store

E is **derived state**: the seed event, folded with events the journal
already records (pregame readings, kickoff freezes, `OFFICIAL_RESULT`).
A restart replays the journal and lands on the same number byte-for-byte.
Nothing else to back up; nothing external to re-deliver.

## 6 · The generator — how it reaches the engine without touching it

George's constraint (26-08): **do not touch the running Python engine.**
The engine already boots from the supervised-inputs file (per ticker:
`expected_season_wins`, `t_effective_time`, `realized_on_field_total`,
`games_remaining`, `scheduled_games`, off-field). So the pipeline ships as
an **external generator**:

    Edwin's package + July CSV + SR finals  →  generator  →  supervised-inputs file  →  engine, unchanged

- Absorption lands at each regenerate + restart. Between restarts the
  G-term prices every game correctly anyway — the file cadence is
  operational hygiene, not pricing correctness.
- The Go port internalises the fold later as another subtree to match.
- The reference-feed adapter (`validate_records()`) survives as the
  door-validation seam only.

## 7 · Rebase — the deferred layer, designed now

Sportsbook futures reprice season totals mid-season (SR sells no such
product — the per-game path is move 1 and needs nothing). A fresh de-vig
mid-season is a **rebase**: legitimate market data, and the cheap form of
the form re-rate.

    EXPECTED_WINS_REBASE:  E ← devig(new snapshot) − banked, shares re-split

Journalled like the seed, snapshot in the bucket. **Not built for
Saturday.** A rebase moves every price at once, so it ships only after the
E51 conversation. Without it the far tail holds the seed's view — a
quality gap, not a correctness gap.

## 8 · Open rules (decide during the build)

- **`[unseen]` game** — never saw a pregame number: absorb at its flat
  share. One basis, no invented number. Needs the ruling recorded when
  implemented.
- **Schedule changes** — a game added: `E += share`; removed: `E −= its
  entry`. Journalled adjustments driven by the daily discovery.
- **NCAA snapshot provenance** — the July file's college rows have no
  confirmed source, and it carries two books where Edwin froze on BetMGM
  (E51 item b).

## 9 · Build list (plan.md 26-08)

1. Seed: Edwin's package on the July CSV + the played-games backfill →
   `EXPECTED_WINS_SEED` + bucket object.
2. The fold: seed + readings + results → E (moves 1–4).
3. The generator emitting the supervised-inputs file.
4. Regression: the §4 table · restart replay equality · the correction
   path.
