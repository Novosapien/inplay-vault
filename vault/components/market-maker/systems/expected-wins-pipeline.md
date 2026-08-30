---
description: "Expected-wins pricing: seed once, then the zero-jump absorber — with §7 withdrawn and the injury channel dropped after Edwin's SDMM-1 v5.1 engine"
---

# Expected-Wins Pipeline — the pricing centre

> **Component:** [[market-maker/market-maker]] · **Status:** DESIGN, ruled
> 26-08 — build this week, ⚠ games live Saturday 29-08
> **Replaces:** [[market-maker/systems/daily-reference-feed]] (superseded —
> Edwin cannot operate a daily hand-off)
> **Ruling:** [[market-maker/decisions]] 26-08 ·
> [[market-maker/sessions/2026-08-26-expected-wins-pipeline]]
> **Closes:** N18 · N19 · N23 · N22's basis-drift residual ·
> **Opens:** E51 (off-field + earnings) · E52 (the tail re-rate) ·
> N73 (the market-data store)
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

> ⚠️ **§7 IS WITHDRAWN (28-08).** Edwin's SDMM-1 v5.1 engine
> (`reference/edwin-sdmm1-v51-2026-08-27/`) answers the forward re-rate
> properly — a per-team rating that every observation updates, giving a
> **−$12.54** loss against our absorber's −$4.53. The weekly futures
> rebase below is superseded and should not be built. Kept for the
> reasoning trail. See [[market-maker/decisions]] 28-08 and `E53`.
>
> ✅ **The injury channel is DROPPED** (George, 28-08). Measured, it is one
> scenario — a season-ending QB is −$8.31 and everything else is under $2.
> A QB injury still reaches the price through Sportradar's win
> probability, delayed rather than lost. Dropping it also removes the
> stale-spread trap, its −$3.57 wrong-direction bug, and the timestamp
> requirement on the board feed. ⚠ Cost is product theatre, not
> correctness — revisit if the app wants the moment.

## 7 · Rebase — the deferred layer, designed now ~~(WITHDRAWN 28-08)~~

Sportsbook futures reprice season totals mid-season. A fresh de-vig is a
**rebase**: legitimate market data, and the cheap form of the form re-rate.

    EXPECTED_WINS_REBASE:  E ← devig(new pull) − banked, shares re-split

Journalled like the seed. **Not built for Saturday.** A rebase moves every
price at once. Without it the far tail holds the seed's view.

⭐ **Cadence ruled 27-08 (George): HOURLY, pulled by us** — see
[[market-maker/parameters]]. One call returns the league, so 24 calls a day
is negligible, and frequent pulls make each price move small instead of
arriving as rare large jumps. Two rules make it safe:

1. **Record a change only when the line moves.** No heartbeat events — an
   hourly write of an unchanged number fills the journal with nothing.
2. **A new line and the banking of a result happen together.** A repriced
   season line ALREADY contains the result of the game just played. Take
   the new line while the game is still open in G and the win counts
   twice. This is Edwin's own rule (a game leaves G when a new T absorbs
   it), now load-bearing hourly.

No clash with live games: bookmakers do not move season lines during a
game (researched 27-07), so mid-game pulls return the same number. The line
moves after the whistle — exactly when the result should be banked.

⚠ **Source split.** Sportradar's futures product carries **NFL** season
totals. For the **138 college teams the endpoints exist but return no
data** (George, 27-08) — so they sit in §11's **"no source"** state and
hold their seeded view until Sportradar delivers. One code path covers
both; college starts working with no code change. ⚠ **Entitlement
unverified** — futures was checked on a July trial, and the August
contract amendment covered live probabilities, not futures.

⭐ **Promoted by the 27-08 call — the rebase is the answer to the forward
re-rate.** Edwin expects a bad loss to move a share "down 10 or $15". The
absorber alone gives −$4.53. A bookmaker cuts LSU's season win total after
that loss (8.5 → ~6.5); re-de-vig and expected wins fall ~2 wins, so the
price falls ~$10. **His number, from market data alone, with §1.5
intact** — no Elo engine, no internal probabilities. The only new
requirement is a **weekly** win-totals snapshot instead of one.

⚠ **Point spreads do not do this job.** Edwin proposed deriving win
probability from spreads, and wants InPlay-owned data rather than
Sportradar's. Spreads publish Sunday for the following week only, so they
re-rate one game at a time. A week-1 shock never reaches week 10. Spreads
are a good layer-2 source; they are not a tail re-rate. Both points ride
`E52`.

## 8 · Open rules (decide during the build)

- **`[unseen]` game** — never saw a pregame number: absorb at its flat
  share. One basis, no invented number. Needs the ruling recorded when
  implemented.
- **Schedule changes** — a game added: `E += share`; removed: `E −= its
  entry`. Journalled adjustments driven by the daily discovery.
- **NCAA snapshot provenance** — the July file's college rows have no
  confirmed source, and it carries two books where Edwin froze on BetMGM
  (E51 item b).

## 9 · The off-field mirror — earnings (27-08)

Off-field runs the same machine as §3–4, on a weekly cadence:

    on-field:   E   −= p_ref(g)  · banked += result    Δprice = $0 exactly
    off-field:  EAV −= expected  · RAV += actual       Δprice = actual − expected

The off-field jump is intended — it is the earnings surprise, applied in
the Tue/Wed ~07:30 burst window (the 23-07 ruling, parameters.md).

**The rule as recorded (Edwin's own docs, pending his confirm):** each
game has a $2.50-per-share pool, split between the TWO teams in that
fixture, pro-rata by trading volume. Per fixture, not a global pool.
Live volume never feeds the live price (circularity); volume surfaces
weekly only.

**Producer — George's ruling 27-08: WE compute the earnings report.**
The volume data is ours (every venue print, with its account). Edwin
defines the formula and blesses it; he audits the output; he runs no
weekly process. This removes the weekly hand-off — the daily-file
failure mode does not return at weekly cadence.

**House volume — George's ruling 27-08: included, under the symmetry
assumption.** SNT-1 runs on all books, both sides of every fixture, so
its volume cancels in a proportional split. ⚠ Recorded consequences:
house volume DILUTES the user signal toward an even split (early season,
taker volume dominates → earnings surprises compress toward zero — fails
safe), and the taker's random clip sizes put a noise floor under a
price-moving number. **Safeguard: the report computes BOTH columns —
with and without house accounts** — so the assumption is checked with
evidence, not asserted. Reversible at any time; the account tags exist
on every print.

**Schema questions riding E51** (pin before the first burst): pool shape
per-fixture vs global · volume in shares or dollars, and the window ·
the house-volume rule above, written down · denomination ($2.50 per
share per game, implied by his own EV numbers).

### 9.1 · Off-field accumulates, but the price must NOT rise

Off-field money sits in two buckets: **RAV** (earned so far) and **EAV**
(still expected). Each game moves a slice from EAV into RAV. The two
always sum to the same number, so the price does not move:

| Point in season | RAV | EAV | total |
|---|---|---|---|
| Start | $0 | $18 | $18 |
| Halfway | $9 | $9 | $18 |
| End | $18 | $0 | $18 |

The price moves **only** when a team earns more or less than expected.
That difference is the earnings surprise, and it is the entire purpose of
the weekly number.

⚠ **The bug this prevents.** Today RAV is `0.00` and EAV is frozen at the
full-season figure. Add realized money without draining EAV at the same
time and **every team's price climbs about $1.25 a game for nothing —
roughly $15 a share across a college season.** Both halves ship together,
or neither.

### 9.2 · ⚠ The live off-field numbers over-allocate the pools by ~9%

Measured on the 138 live NCAA records (27-08):

| Measure | Value |
|---|---|
| Off-field per team per game | min $0.955 · median $1.362 · max $2.302 |
| **Two average teams meet** | **$2.72** against a $2.50 pool |
| Two top teams meet | $4.61 |
| League expected off-field | **$2,254** |
| Money that exists (828 games × $2.50) | **$2,070** |
| **Over-allocation** | **~$184, about 9%** |

Worked case: Sacramento State earns $2.24 a game and North Dakota State
$2.30. Both are FCS, so the fixture can happen — and it would pay
**$4.54 out of a $2.50 pool**.

**Popularity is not the explanation.** Popularity correctly sets *who gets
more of the pool* — confirmed by Edwin on the 27-08 call (the Jets and
Giants "still could make a lion share… even if they stink") and visible in
the data: correlation between expected wins and off-field is only **0.729**,
and Sacramento State earns the second-highest off-field in the league on
4.61 expected wins. But popularity sets the **ratio**, never the **total**.
Two teams in one fixture must still sum to $2.50.

**The likely cause, with two independent pieces of evidence.** Edwin's
model appears to price each team's off-field from its own popularity and
never check that the fixture balances:

1. His Gamecast formula `offShare = 1.0 + pct × 0.5` reads only the team's
   own percentile and **never references the opponent** (§ the EV guide).
2. The live numbers sum to 109% of the available pools, above.

**Why it matters beyond tidiness.** Settlement pays what a team actually
earned, not what was projected. If EAV runs ~9% above the money that
exists, realized will land under expected week after week, and prices will
**drift down across the whole league** — a systematic bias that looks like
the model working while it is quietly wrong.

**The ask (E51 item d):** is the $2.50 split between the pair, or is each
team's number standalone? If it is a split, the projections need
normalising against the fixture list. Also: when a listed team plays an
opponent that is not a listed company, does it take the whole pool or only
its share? That would legitimately explain part of the excess.

**Generator change now (cheap):** EAV decays — `EAV = per-game share ×
games remaining`, recomputed each regenerate, replacing the sheet's
static season number.

## 10 · What the 27-08 call confirmed

[[27-08-2026-mm-pricing-catchup]] ·
[[market-maker/sessions/2026-08-27-edwin-pricing-call]]

**The seed verifies against numbers Edwin quoted live.** He worked LSU
through on the call:

| Quantity | Edwin, on the call | Our seed |
|---|---|---|
| IPO price | "$59 or 59.53" | 59.54 |
| Expected wins | "8.55" | 8.5452 |
| On-field baked in | "$42.75" | 42.73 |
| Reference price | — | 60.87 (his sheet's IPO EV: 60.874) |

**The absorber is his model.** Unprompted: "a win to LSU is not going to be
worth $5 more a share because part of that is already baked into the
price" — he put the move at 47 cents to $1.50 for a heavy favourite.
`$5 × (result − p_ref)` gives exactly that. §3–4 need no change.

**Off-field is confirmed both ways** — actual is trading volume, expected
is his popularity model. ⚠ But his spoken numbers (Dallas ~$30, Carolina
~$12–14) disagree with his own sheet (24.07, 19.22), which our seed used.
He offered the popularity file; `E51(d)` requests it.

**The gap: he expects the tail to re-rate at once** — see §7 above and
`E52`.

## 11 · Freshness — what "stale" means here (George, 27-08)

**A number is stale only if a newer one exists and we have not taken it.**
Age is not staleness. A July number is correct if nobody has published a
better one.

That gives three states per team, not two:

| State | Meaning | Alarm? |
|---|---|---|
| **Confirmed** | We reached the source. It gave the same number, or a new one we took. | No — fresh at any age |
| **No source** | We reached the source. It carries no market for this team. The number stands on its original provenance. | No — but show it as **unbacked** |
| **Broken** | We could not reach the source, or the pull failed. A newer number may exist and we are missing it. | **Yes — this is the only alarm** |

**The alarm sits on the pull, never on the age of the value.** This is the
same rule the live probability feed already runs (the E38 deviation): a
successful fetch CONFIRMS the number even when it has not moved, and time
counts from the last successful answer rather than the last change.

⚠ **The 138 college teams sit in "no source", and cannot leave it.** Their
July numbers did not come from Sportradar — Sportradar carries no college
season totals, so someone supplied them by hand. The source can never
confirm them. Display them as **unbacked, not stale**: calling them stale
implies a fault our side when there is none.

**Hold-last-value must be visible.** Today the college number is 16 days
old and nothing anywhere says so. Hold it indefinitely — there is no
alternative — but show its age and its state, so "the feed is broken" can
never look identical to "the line has not moved".

**Build consequence: one code path for all 170.** The pull runs hourly
against every team. NFL answers; college returns nothing today. When
Sportradar fixes the college endpoint it starts working with **no code
change**.

## 12 · Live state, measured 27-08 (read-only check)

| Fact | Value |
|---|---|
| Mode | `supervised` · readings off the bus · `CFG-0045` |
| Books quoted | **138 NCAA**. NFL is not in `MM_SECURITIES` |
| Inputs file | `/home/georgewestbrook/supervised-inputs-138-ncaa.json` |
| Journal | `/var/lib/mm/supervised47` (prior run carried, F2) |
| **`t_effective_time`** | **`2026-08-11T22:00:00Z` — static for 16 days** |
| Banked | `realized_on_field_total` and `realized_off_field` both `0.00` |
| Seed agreement | max ΔRP **$0.0061** across all 138 — verified |

⚠ **The consequence that sets the build order.** Saturday prices correctly
without the absorber, because the engine holds each finished game in G with
its result pinned. **The first regenerate of the inputs file WITHOUT
absorption drops every winning team by $5** — the file supplies a new T
while G still carries the game, so the win is removed and never banked.

**So the absorber and the file regenerate must ship together, or neither.**
Regenerating the file is not a safe independent step.

## 13 · Build list (plan.md 26-08)

1. Seed: Edwin's package on the July CSV + the played-games backfill →
   `EXPECTED_WINS_SEED` + bucket object.
2. The fold: seed + readings + results → E (moves 1–4).
3. The generator emitting the supervised-inputs file.
4. Regression: the §4 table · restart replay equality · the correction
   path.
