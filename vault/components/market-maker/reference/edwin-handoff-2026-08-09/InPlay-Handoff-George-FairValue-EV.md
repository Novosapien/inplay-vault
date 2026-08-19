# InPlay Global — Engineering Handoff: Fair-Value (EV) Pricing

**To:** George Westbrook / novosapien
**From:** Edwin Johnson
**Re:** How the mock computes a share's **current fair value** (the "final EV") — the number your system needs to reproduce.
**Status:** built and node-verified in the mock (`makeLiveGame` store engine + `lgSimulate` pure engine, identical math).

---

## 0. What this document is

This is the pricing spec for **one thing**: how we arrive at a share's **fair value / expected value (EV)** at any moment. It is not the market-maker spec and it doesn't cover order matching or spread policy — it's the theoretical value everything else is priced around.

There are two layers. Get the first one exactly right and the second one falls out of it:

1. **Resting EV** — a team's fair value when no game is live. This is `seasonFair(team)`. It's the number a share is "worth" between games.
2. **Live EV** — during a game, the resting value is re-priced play-by-play by four in-game components. This is `lgValuePrice(...)`.

The governing principle throughout: **price tracks value, not win probability.** Win probability is only an *input* to one component. This is why a team's share can fall while it's winning (see §2.4).

All dollar figures are per share, in InPlay Dollars.

---

## 1. Layer 1 — Resting EV: `seasonFair(team)`

A share is a claim on a team-company's season revenue. Its fair value is the **IPO price adjusted by the revision in expected season revenue** since the IPO. If results and the remaining schedule now imply more revenue than the IPO assumed, the share is worth more than IPO; if less, less.

### 1.1 Inputs
- `px` — the team's **static IPO price** (from the canonical IPO sheet; NFL range **35.66 (ARI) → 81.20 (LAR)**).
- Results to date — wins and **banked revenue** so far this season.
- Remaining schedule — games left.

### 1.2 Revenue primitives
- **Win revenue = $5.00 per win** (canonical, absolute — see §2.2).
- **Off-field = $2.50 per game**, split between the two teams pro-rata by share volume. A team's per-game off-field share is brand-weighted:

```
pct       = clamp( (px − 35.66) / (81.20 − 35.66), 0, 1 )   // price percentile within the league
offShare  = 1.0 + pct * 0.5                                  // this team's per-game off-field ≈ 1.0–1.9
```

### 1.3 The formula (exact, as coded)

```
pct        = clamp((px − 35.66) / (81.20 − 35.66), 0, 1)
e0         = 5.5 + pct * 6.5           // preseason expected wins implied by the IPO price
offShare   = 1.0 + pct * 0.5           // per-game off-field share

// results to date (in the mock these come from schedSim wks 1–11;
// in production they are ACTUAL results):
wins, played, banked   // banked = Σ (win ? $5 : 0) + off-field earned to date
remGames   = 17 − played

pRem       = clamp( (e0 + 2*wins) / (17 + 2*played), 0.08, 0.85 )   // fwd win rate: prior blended with form
expRemWins = remGames * pRem
expRemRev  = remGames * (pRem * 5.25 + offShare)   // expected remaining revenue
pre        = e0 * 5.25 + 17 * offShare             // revenue the IPO price already assumed

fair       = clamp( px + (banked + expRemRev) − pre , 14, 118 )
```

Read it as: **`fair = IPO price + (revenue we now expect this season) − (revenue the IPO price already priced in)`.**

> Note on `5.25`: the season model uses **5.25** as the revenue coefficient per *expected* win (the $5 win plus a small blend), while a *realized, banked* win is exactly **$5.00**. Keep both: 5.00 for banked results, 5.25 for the forward expectation term.

### 1.4 Worked example — Kansas City (mock data)

```
seasonFair("KC") → { fair: 68.93, wins: 6, losses: 4, banked: 43.94,
                     expRemWins: 4.3, expRemRev: 32.75, remGames: 7 }
```

KC's shares rest at **68.93** (up from a lower IPO because a 6–4 start + a favorable remaining slate imply more revenue than the IPO assumed).

`seasonFair` returns `{ fair, wins, losses, banked, expRemWins, expRemRev, remGames }`. Cross-section sanity in the mock: `corr(wins, fair) ≈ 0.96` (a 9–1 team prices near 90; a 1–10 team near 17).

**This `fair` is the "final EV" for a team with no live game — the value your system should carry as the resting fair price.**

---

## 2. Layer 2 — Live EV: re-pricing during a game

When a game is live, the resting value (the **anchor** = `clamp(seasonFair.fair, 24, 96)`) is re-priced every play by four components. The live fair value is:

```
pFair = anchor + banked + C1 + (C2 − C2₀) + (C4 − C4₀) + offCur
```

- `anchor` — the resting EV from §1 (already contains season-to-date + expected remaining).
- `banked` — **intra-session** banking only, from prior games in a multi-game stretch. **0 for a standalone live game.** (Do **not** add season banked here — it's already in the anchor.)
- `C1` — current-game win premium.
- `C2 − C2₀` — change in remaining-games EV (the live re-rate).
- `C4 − C4₀` — change in remaining off-field EV (injury-driven).
- `offCur` — this game's off-field.

### 2.1 The per-game constants (`gv`)

Computed once at kickoff from `seasonFair(home)`:

```
anchor      = clamp(seasonFair(home).fair, 24, 96)
wpPre       = 1 / (1 + e^(−pregameZ))                 // disclosed opening win prob (0..1)
winRateBase = clamp(expRemWins / remGames, 0.08, 0.85)
gRemAfter   = max(1, remGames − 1)                    // games left AFTER this one
offShare    = 1.0 + pct * 0.5
```

(`rhoJit`, `liq` are variability knobs — see §2.5 / §3.)

### 2.2 C1 — current-game win premium (a win banks **exactly $5**)

```
M       = 0.35 + 0.65 * clamp(1 − timeLeftSecs/3600, 0, 1)^1.5   // maturity / time-decay leverage
cgWin   = 5 * ( wpPre + M * (wpLive − wpPre) )                   // expected $ from this game's win, 0..5
C1      = cgWin − 5 * 0.5                                        // centered so kickoff is continuous
```

- **The win is worth $5, absolute.** It never floats on opponent quality. At the whistle `cgWin → $5` on a win (from `wpPre`), `→ $0` on a loss.
- `M` is the **time-decay dial**: 0.35 at kickoff (Q1 plays still move price, just muted) → ~1.0 late. A tie game in the last two minutes has `M ≈ 0.97` *and* a hair-trigger `wpLive`, so late swings move price hard; a Q1 first down barely moves it. Maturity values: kickoff **0.35**, halftime **0.58**, two-minute **0.97**.
- `wpLive` is the live win probability (0..1). **This is the only place WP enters the price.**

### 2.3 C2 — remaining-games EV (this is where re-rating lives)

```
domActual   = clamp((homeS − oppS) / 21, −1, 1)          // scoreboard dominance
domExpected = (wpPre − 0.5) * 1.5                         // what a team of this strength "should" show
perf        = clamp(domActual − domExpected, −1, 1)       // opponent-adjusted over/under-performance
reRate      = clamp(1 + 0.15 * rhoJit * perf, 0.80, 1.25)

C2₀ = gRemAfter * winRateBase * 5                         // remaining EV at kickoff
C2  = gRemAfter * (winRateBase * reRate * injOn) * 5      // re-rated live (injOn from §2.6)
```

**All opponent-quality re-rating lives here, not in the banked win.** Beating a strong team (or dominating a weak one *more* than expected) lifts `perf` → `reRate` up → C2 up → the remaining season is worth more. Squeaking past a cellar team pushes `perf` negative → C2 down.

### 2.4 The consequence: total price move ≠ the banked win

- **Upset:** win banks $5 **and** C2 re-rates up → total gain **> $5**.
- **Favorite squeaks by a weak team:** win banks $5 **but** C2 re-rates down → net can be **flat or negative**.
- **Star injury while leading:** C2 craters (§2.6) → **price falls even though the team is winning.**

Verified in the mock: a **major injury to a leading team dropped its share price in 26/26 test cases (100%)** — the behavior WP-based pricing can never produce.

### 2.5 C4 / offCur — off-field EV

```
C4₀    = gRemAfter * offShare
C4     = C4₀ * injOff        // remaining off-field, injury-sensitive (a lost star hurts the brand too)
offCur = offShare            // this game's off-field
```

Off-field is a **projection only** — it never keys off live intra-game volume (that would make price circular). Volume is disclosed on the weekly Friday report, never per-team live.

### 2.6 Injury model (impact formula — the part that ports)

The mock *draws* random injuries; in production they come from a real feed. Either way, the **impact** is:

```
hit    = posWeight * starValue * severityFrac        // fraction of team value lost

injOn  = clamp( injOn  * (1 − hit * 0.60 * rnd(0.7,1.3)), 0.40, 1 )   // on-field markdown → C2
injOff = clamp( injOff * (1 − hit * 0.30 * rnd(0.7,1.3)), 0.55, 1 )   // off-field markdown → C4
// major injury also drags wpLive down (own star) / up (opponent's star)
```

- **Two-sided:** your own star down marks *you* down and helps the opponent's WP; the opponent's star down helps you.
- **Per-team star value** — Mahomes ≫ a cellar QB — is **derived from IPO-price percentile**, no hand table:

```
starValue = 0.6 + 1.2 * pct       // 0.6 (bottom of league) → 1.8 (top).  KC-QB ≈ 1.61, CAR-QB ≈ 1.10
```

- **Position weights** (`posWeight`): QB 0.35 ≫ WR / DE / CB 0.09 ≫ LT / OL 0.06 ≫ RB / S 0.05 ≫ LB / TE 0.03.
- **Severity** distribution: 65% minor `[0, 0.05]`, 25% moderate `[0.10, 0.30]`, 10% major `[0.50, 1.0]`.
- Effect scales: an elite-QB season-ender can cut remaining on-field value ~40–60% in one snap.

### 2.7 The exact reconciliation identity

The disclosed 3-way decomposition sums to the fair value exactly:

```
pFair  =  seasonVal  +  cgWin  +  offCur
          (base + remaining)   (this game's win premium)   (this game's off-field)
```

Worked (KC, opening WP 0.62): `seasonVal 65.93 + cgWin 3.10 + offCur 1.42 = 70.45 = pFair`. Use this identity as your unit test — if these three don't sum to `pFair`, something's wrong.

---

## 3. The traded price (context only — not the EV)

The mock's **traded** price is `pFair + ε`, where `ε` is a mean-reverting, volume-scaled noise term (thin liquidity drifts wider). In the sim this manufactures the mispricing a trader prosecutes; **in production, real order flow replaces `ε` entirely.** The point for you: **`pFair` (this document) is the anchor; the traded print is not the fair value.** Everything downstream should be built around `pFair`, not the last print.

For reference, the sim's noise (tunable, will be discarded in prod):

```
volFac = clamp(1 / liq, 0.6, 2.2)                 // liq ~ per-game liquidity, rand(0.5,1.5)
ε      = ε * 0.80 + rand(−0.95, 0.95) * volFac    // mean-reverting
if (key play) ε += rand(−1.3, 1.3) * volFac       // event over/under-reaction
traded = clamp(pFair + ε, 14, 118)
```

---

## 4. Production data inputs

To compute `pFair` live for a real game, the model needs, per play:
- **Live win probability** `wpLive` (0..1) — from the Sportradar feed. *(This is the historical-replay backfill still owed.)*
- **Live score** and **time remaining** (for `M` and `domActual`).
- **Pregame opening WP** `wpPre` — set at kickoff.
- **Injury events** (player + position + severity) — feeds the §2.6 impact.
- **Static inputs:** IPO price (`px`), the team's results-to-date and remaining schedule (for `seasonFair`).

Clamps to respect: `anchor ∈ [24, 96]`, final price `∈ [14, 118]`, `winRateBase ∈ [0.08, 0.85]`, `reRate ∈ [0.80, 1.25]`, `injOn ∈ [0.40, 1]`, `injOff ∈ [0.55, 1]`.

---

## 5. Where it lives in the mock (to port)

All in `InPlayHomeV1423.jsx` (assembled: `InPlayApp-ASSEMBLED.jsx`):
- `seasonFair(mono)` — Layer 1 (resting EV). Memoized.
- `lgPct`, `lgStarValue`, `LG_POSW`, `lgDrawInjury`, `lgMaturity` — helpers.
- `lgValuePrice(gv, wpLive, homeS, oppS, pool, timeLeftSecs)` — Layer 2. Returns `{ pFair, cgWin, offCur, seasonVal, c1, c2, c2_0, dC2, c4, dC4 }`.
- `gv` constants are built in `seedGame` (store engine) and the per-game loop in `lgSimulate` (pure engine) — **identical math in both**, so port from either.
- Every play carries `wpPre` and the full `vp` breakdown; `snap()` exposes `wpPre`, `pFair`, `vp`.

Full narrative spec (with the design rationale and all red-line decisions): **`InPlay-Gamecast-Pricing-Spec.md`** (v3).

---

## 6. Open items
- **Sportradar WP backfill** for historical game-week replay (owed from your side).
- The noise/`ε` layer (§3) is sim-only and will be replaced by real order flow — don't port it as pricing.
- `rhoJit` / `liq` / injury magnitudes are variability **knobs**, still being feel-tuned; the **structure** above is stable.
