# InPlay — Live Gamecast Share-Pricing Spec (v3)

**Purpose.** Replace the win-probability-driven live price with a **value model**: the
share price is the expected value of everything the share still has a claim to. Win
probability becomes an *input*, never the price itself. This is what lets the price
**decouple from WP and the scoreboard** — e.g. a team is winning but (a) its star QB goes
down, or (b) it only squeaks past a weak opponent, and the share *falls*, because the rest
of the season just got worse.

Everything below is proposed defaults. Dials you'll want to red-line are marked **[DIAL]**.

> **v2 (Edwin):** a win banks **exactly $5 per share — absolute, always.** The "worth more/less"
> lives **entirely in Component 2 (forward EV re-rate), never in the banked win.**
>
> **v3 (Edwin's red-line, Aug 8) — the governing principle is VARIABILITY.** Market pricing is an
> art; the model should breathe, not tick deterministically. Specifically: the noise band varies
> by game with **trading volume** (thin volume → prices drift more; heavy volume → tends toward
> efficient — a tendency, not an absolute); the forward re-rate strength varies and a star injury
> can **torpedo** a season's value (the Aaron Rodgers / Jets 2023 case — season value gutted on
> one snap); star values are **derived** (no hand-set table — see Appendix A); a lost star hits
> **off-field too**, variably; and the pregame disclosure **collapses base + remaining into one
> "Season value" line** so the current-game pieces stand out — kept visually clean.

---

## 1. Core principle

At any instant `t` during a game, for the share of team **H** (opponent **O**):

```
P_fair(t)  =  Base_H
            + C1(t)      current-game win premium        (fast — moves every play; win banks a fixed $5)
            + C2(t)      remaining-games on-field EV      (re-rates live — opponent quality, performance, injury)
            + C3         current-game off-field EV        (locked during the game)
            + C4(t)      remaining-games off-field EV     (injury-sensitive only)

P_mkt(t)   =  P_fair(t)  +  ε(t)     traded price = fair value + market noise  (§7)
```

- **`Base_H`** — structural/franchise value independent of any single game's outcome (brand,
  enterprise value, banked results already realized). Large and slow.
- **`C1`** is the only component that moves play-to-play. `C2`/`C4` re-rate slowly except on
  injuries or a decisive result. `C3` is fixed once the game starts. `Base + C2 + C3 + C4`
  form the **floor** the price oscillates above.
- At **kickoff** the four components sum to the **`seasonFair(H)` anchor** we already compute,
  so there's no discontinuity at kickoff. The live price then moves as the *revisions*.

Reconciliation (kickoff price == anchor exactly):

```
P_fair(t) = seasonFair(H)                    // the anchor, = the four components at t=0
          + C1(t)                            // 0 at kickoff, by construction
          + ( C2(t) − C2(0) )                // live re-rate of remaining on-field EV
          + ( C4(t) − C4(0) )                // live re-rate of remaining off-field EV
```

`C1(0)=0`; `C2(0)/C4(0)` are the pregame expectations already inside `seasonFair`. The price
starts on the anchor and moves only as the game changes the picture.

---

## 2. Component 1 — current-game win premium `C1(t)`  (win = a fixed $5)

The value the share gains/loses from **this game's** result, relative to the pregame
expectation already priced in (so `C1` starts at 0 and is the *revision*).

```
C1(t) = WinRev · M(t) · ( WP_live(t) − WP_pre )        WinRev = $5.00  (FIXED — absolute banked value of a win)
```

- **`WinRev` = $5.00, fixed.** A win banks exactly $5; a loss banks $0 in win revenue. There
  is **no** opponent-quality or performance multiplier on the win itself. *(The "worth more/
  less" intuition lives in Component 2.)*
- **`WP_live(t)`** — live win probability of H (engine output; blends the pregame prior and the
  score-driven WP).
- **`WP_pre` = `WP_live(0)`** — pregame win probability (the number we disclose, §8).
- **`M(t)` — maturity/leverage weight** = how much a WP swing moves price yet. **Time-decay
  dial (§ agreed):**
  ```
  M(t) = M0 + (1 − M0) · τ^p          τ = 1 − gameSecondsRemaining/3600   (0→1 over the game)
  ```
  **[DIAL]** `M0 = 0.35`, `p = 1.5` (convex → late game dominates).
  - Early: `M ≈ 0.35` → a WP swing still moves price, but muted (a Q1 conversion moves cents —
    **not zero**).
  - Late: `M → 1` → WP swings move at full weight.
  - **Closeness needs no separate term** — it rides in through `WP_live`: a tied-Q4 conversion
    swings WP hard *and* `M≈1`; a Q4-blowout play barely moves WP so `C1` barely moves.

**Convergence (banks the absolute $5):**
- Win: `WP_live→1`, `M→1` → `C1 → $5·(1 − WP_pre)`. The share gains the *unpriced* portion of
  the win; the **total accumulated earnings rise by exactly $5** (the rest was already in the
  pre-kick price).
- Loss: `WP_live→0`, `M→1` → `C1 → −$5·WP_pre`. The priced-in win premium evaporates; $0 win
  revenue banks.

So the **banked number is absolute ($5 / $0)**; the **price move** is the surprise portion
relative to what was already priced. That reconciles "the actual number earned is absolute"
with "the price moved by less/more than $5."

---

## 3. Component 2 — remaining-games on-field EV `C2(t)`  (all quality/performance lives here)

The forward value of win premiums for every game **after** this one. **This is where opponent
quality and in-game performance re-rate the price** — an upset marks the team up, an
unconvincing win marks it down.

```
C2(t) = g_rem_after · winRate_fwd(t) · WinRev            WinRev = $5 (same fixed win value)

winRate_fwd(t) = clamp( winRate_base · ReRate(t) · InjuryMult_on(t),  0.05, 0.95 )
ReRate(t)      = 1 + ρ_game · perfSignal(t)              performance re-rate, ReRate ∈ [0.80, 1.25]
```

- **`g_rem_after`** = games left after this one (17-game NFL season). The "how many games left"
  lever: with 9 games left a live re-rate moves `C2` far more than with 1 left. A late-season
  squeak-by barely dents `C2`; an early-season one moves it a lot.
- **`winRate_base`** = pregame forward win rate (from `seasonFair`/`pRem`).
- **`ReRate(t)` — live, opponent-adjusted performance re-rate. VARIABLE (Edwin):** `ρ_game` is
  drawn per game around a base **[DIAL]** `ρ ≈ 0.15 ± jitter`, so identical box scores re-rate
  differently game to game — market judgment, not a fixed function. *(The performance re-rate is
  bounded modestly; the INJURY path below is where a season can be torpedoed — it is NOT held to
  this clamp.)*
  ```
  perfSignal(t) = clamp( dom_actual(t) − dom_expected,  −1, +1 )
  dom_actual(t) = margin_H(t) / 21                       // live scoreboard dominance
  dom_expected  = (WP_pre − 0.5) · k                     // how much H was expected to dominate  [DIAL] k = 1.5
  ```
  - **Beat a strong team** (H was a dog, `dom_expected < 0`) while leading → `perfSignal`
    strongly positive → forward win rate revised **up** → `C2` up. *This is the "upset is worth
    more" effect — realized as forward EV, not as a bigger banked win.*
  - **Squeak by a weak team** (H heavily favored, `dom_expected` high) with a thin margin →
    `perfSignal` **negative** → forward win rate revised **down** → `C2` **down**. *Exactly the
    scenario: the market infers the remaining games should be forecast lower.*
- **`InjuryMult_on(t)`** — starts at 1.0; an injury knocks it down (§6). The other way `C2`
  craters — enough to drop a **winning** team's share.

---

## 4. Components 3 & 4 — off-field EV (projection only; never live volume)

Off-field revenue = **$2.50/game** split pro-rata by share volume. **No team's live trading
volume is disclosed intra-game — volume is reported only on the Friday report.** So the live
price uses the **projected** off-field capture, never realized live volume — which keeps these
a calm floor and removes the circularity of volume feeding price.

```
offShare_H = projected fraction of the $2.50 pool H captures per game   (brand/volume model)
C3 = offShare_H                                   // current game — LOCKED once kickoff happens
C4(t) = g_rem_after · offShare_H · InjuryMult_off(t)
```

**[DIAL]** `offShare_H` ≈ $1.00–$1.90 (brand-weighted; today's `seasonFair` `offShare` 1.0–1.5).
`C3` does not move during the game. `C4` moves **only** on injury (a lost star reduces
attention/merch/ticket premium for the rest of the season) at a muted rate (§6).

**UI audit requirement:** no live per-team volume number anywhere in the gamecast (cockpit, L2
book, "traded today", inventory). Volume surfaces only in the Friday report.

---

## 5. Worked examples — the behaviors this must produce

Share 54.0, `g_rem_after = 8`, `winRate_base = 0.58`, `WinRev = $5` → `C2(0) = 8·0.58·5 ≈ 23.2`.

**(a) Big upset — win worth *more* than $5 to the market (via forward EV).** H a 30% dog
(`WP_pre = 0.30`) beats a strong team. Bank: `C1 → 5·(1−0.30) = +3.5` (**accumulated earnings
+$5 absolute**; $3.5 of it was unpriced). Forward re-rate: `perfSignal` strongly positive →
`winRate_fwd 0.58→0.66` → `ΔC2 = 8·0.08·5 = +3.2`. **Total price move ≈ +6.7** (`ΔC1 +3.5` +
`ΔC2 +3.2`). The win itself banked exactly $5; the market valued it "above $5" only because it
re-rated the rest of the season **up**. ✔

**(b) Favorite squeaks by a cellar team — price *falls* despite a win.** H an 80% favorite
(`WP_pre = 0.80`) wins by 2 over a weak team. Bank: `C1 → 5·(1−0.80) = +1.0` (**still $5
absolute banked**; only $1 unpriced). Forward re-rate: expected to dominate, didn't →
`perfSignal` negative → `winRate_fwd 0.65→0.60` → `ΔC2 = 8·(−0.05)·5 = −2.0`. **Total ≈ −1.0 —
share drops even though H won and banked $5.** ✔  *(The banked win is absolute; the forward
markdown exceeds the unpriced premium.)*

**(c) Injury drops a winning team.** Team leads 14–3 late Q3, star QB carted off
(season-ending, elite tier). `InjuryMult_on → 0.72` → `ΔC2 ≈ −6.5`; small `C1`/`C4` effects.
**Net ≈ −7 while winning.** Same mechanism as (b) — Component 2 craters. ✔

**(d) Time leverage — same play, different clock.** Tie-game 3rd-and-long conversion.
- **Q1** (`WP 0.50→0.53`, `M≈0.36`): `ΔC1 = 5·0.36·0.03 ≈ +0.05` → +~cents. Real but small.
- **Q4 @2:00** (`WP 0.50→0.62`, `M≈0.95`): `ΔC1 = 5·0.95·0.12 ≈ +0.57` → +~0.6. ~10× the leverage. ✔

---

## 6. Injury model — severity × position × per-team star value (two-sided)

Injuries already generate (~1.3/game) but are cosmetic. Upgrade each to draw a **position**, a
**severity**, and resolve a **price impact** = `posWeight · starValue · severityFrac`, applied
to the forward components.

### Position weights (fraction of team on-field value lost if out for the season) **[DIAL]**

| Position | Weight |
|---|---|
| QB | 0.35 |
| WR1 / edge / LT / CB1 | 0.09 each |
| RB1 / WR2 / DT / S | 0.05 each |
| TE / LB / interior OL | 0.03 each |
| depth / other | 0.01 |

### Per-team star value — the "Mahomes vs Carolina's QB" point

Each team carries a **star-value multiplier by position**, so losing KC's QB reprices far
harder than a bottom team's. **Derived, not hand-entered** (defensible mock default, `[DIAL]`):

```
starValue_QB(team) = 0.6 + 1.2 · seasonFairPct(team)      // ~0.6 (bottom) → ~1.8 (top)
```

Elite-QB franchises already sit atop the brand/performance/`seasonFair` model, so this ranks them
correctly for free. **Resolved (Edwin): DERIVED — no hand-set override table.** The full 32-team
result is **Appendix A** (KC 1.57 vs CAR 0.83 — Mahomes reprices ~1.9× harder, with zero tuning).
Production swaps in a real player-value feed behind the same interface.

### Severity distribution (per injury event) **[DIAL]**

| Tier | Prob | severityFrac | Narration |
|---|---|---|---|
| Minor | 65% | 0.00–0.05 | "questionable — returns" |
| Moderate | 25% | 0.10–0.30 | "out for the game" |
| Major | 10% | 0.50–1.00 | "carted off — season" |

### Applying the shock — VARIABLE, and a star can torpedo a season (Edwin)

```
hit            = posWeight · starValue · severityFrac        // fraction of team value lost
InjuryMult_on  = clamp( 1 − hit · η_on · rndOn ,  0.40, 1.0 )     η_on  ≈ 0.6 ± jitter   [DIAL]
InjuryMult_off = clamp( 1 − hit · η_off · rndOff,  0.55, 1.0 )    η_off ≈ 0.30 ± jitter  [DIAL]
```

The injury path is **not** held to the modest performance-re-rate clamp — an elite QB lost for the
season can drive `InjuryMult_on` toward its ~0.40 floor, i.e. **cut remaining on-field value ~40–60%
in one snap** (the Rodgers/Jets 2023 archetype). `rndOn/rndOff` are per-event random draws so the
same injury doesn't reprice identically twice — market art, not a lookup. **Off-field is hit too
(Edwin)**, variably and more stickily than on-field (`η_off` < `η_on`; higher floor). A **major**
injury to H's own key player also drops `WP_live` (H is worse now). Minor injuries → ~0 impact.

### Two-sided
If **O**'s star goes down: O's `C2/C4` fall (O's share drops); H's `WP_live` rises (easier win →
H's `C1` up); if H and O meet again, H's `winRate_fwd` ticks up. One event, opposite moves on
the two instruments.

---

## 7. Fair value vs traded price — the market-noise band (your answer: **B**)

The **traded** price is not the model number; it floats around fair value on supply/demand, so
there are exploitable mispricings — the "prosecute value" edge.

```
P_mkt(t) = P_fair(t) + ε(t)
dε = −θ·ε·dt + σ·dW      plus event kicks: on a key play / injury, ε += shock (crowd over/under-reacts, then decays)
```

**Resolved (Edwin): the band is VARIABLE per game, keyed on trading volume.** Thin-volume games
drift more (looser, less efficient); heavy-volume games tend toward efficient pricing — *a
tendency, not an absolute*, so even a liquid game can dislocate on a shock.

```
σ_game(t) = σ0 · volFactor(t) · (1 + jitter)
volFactor(t) = clamp( (Vref / V_live(t))^q , loFac, hiFac )     // low volume → big factor → wide band
```
**[DIAL]** `σ0 ≈ 1.0` IPD (price-scaled so the % band is uniform across the $14–118 ladder),
`q ≈ 0.5`, `volFactor ∈ [0.6, 2.2]`, plus per-game `jitter` (±20%) so no two games behave
identically. Reversion `θ` also eases with volume (thin books mean-revert slower). Event kicks
(key plays, injuries) inject a transient over/under-reaction that decays back.

**Volume is an INTERNAL pricing input, never a displayed number.** The engine / market-maker
uses `V_live` to set the band; the user never sees a per-team volume figure intra-game — it
surfaces only in the **Friday report** (§4). No contradiction: volume *drives* price, it just
isn't *disclosed* until Friday.

In production the market-maker (`rpv2_flow_responsive` RP-vol machinery) quotes around `P_fair`
with this volume-scaled vol; in the mock we simulate `ε` and a synthetic `V_live` directly.

---

## 8. Pregame disclosure — the "Opening Line" card (UI)

Shown on the pre-kick gamecast state (the "Watch Live" splash becomes a teaching surface).
**Discloses everything.**

**Layout (mobile, 375pt):**

1. **Pregame Win Probability** — a single split bar, both teams, team colors, big + legible:
   `DAL 62% ▓▓▓▓▓▓▓░░░░ 38% DET`. Eyebrow `PREGAME WIN PROBABILITY`. Sides sum to 100%.
2. **Opening price decomposition** — a labeled **stacked horizontal bar** + a compact table so
   the user sees *why* the share opens where it does:

   | Component | Value |
   |---|---|
   | Season value *(base + remaining games, on- & off-field)* | 51.30 |
   | This game — win premium (WP × $5) | 3.10 |
   | This game — off-field | 1.30 |
   | **Opening price** | **55.70** |

   **Resolved (Edwin): collapse base + remaining into ONE "Season value" line** so the two
   *current-game* pieces stand out — the parts a trader actually moves during the game. Keep the
   interface clean: three rows + total, not five. (A tap on "Season value" can expand the
   breakdown for the curious, but the default is the clean three-row view.) The current-game win
   premium is `WP_pre × $5` — the *expected* value of a $5 win; it settles to $5 (win) or $0 (loss).
3. Explainer: *"A win is worth $5. What moves the share by more or less is the market re-rating
   the rest of the season. Watch each piece move as the game plays."*

Tokens: `C.panel` card, mono numerals, a 3-segment stacked bar — muted (Season value) / orange
(win premium) / teal (off-field). Type ≥ 10px floor. Clean over complete.

---

## 9. Live value readout (UI) — making "WP ≠ price" visible

The broadcast block's Price + WP bar stays (big tradeable **`P_mkt`** orange, **`WP`** blue)
and gains:

- **Value-breakdown strip** (collapsible): the four components' current values **and per-play
  deltas**, so a price jump shows which piece moved — `Win premium +0.6 · Remaining +0.3 · Off-field —`.
- **Re-rate / injury event cards** — a distinct card when Component 2 moves materially:
  `★ INJURY · DAL QB (season) — remaining-season value −6.5`, or `▼ UNCONVINCING — forward EV −2.0`,
  colored as down-events even while the team leads. The decoupling made legible.
- **Fair-value overlay (Pro toggle)** — a faint `P_fair` line beside traded `P_mkt` on the
  chart, exposing the mispricing gap (Bloomberg-style edge). Off by default.
- **WP-vs-price divergence cue** — first time price and WP move opposite, a one-time subtle
  callout: *"Price can move against win probability — that's the rest of the season repricing."*

---

## 10. Calibration defaults (the red-line table)

| Symbol | Meaning | Default | Notes |
|---|---|---|---|
| `WinRev` | banked value of a win | **$5.00 fixed** | absolute; never floats |
| `M0` | early-game leverage floor | 0.35 | Q1 still moves |
| `p` | maturity curve exponent | 1.5 | convex, late-dominant |
| `ρ` | live forward re-rate strength | 0.15 | `C2` sensitivity (quality + performance) |
| `k` | expected-dominance scale | 1.5 | squeak-by / upset threshold |
| `ρ_game` | live re-rate strength (VARIABLE) | 0.15 ± jitter | performance clamp [0.80,1.25]; injury path exempt |
| position weights | injury value by position | table §6 | QB = 0.35 |
| `starValue_QB` | per-team QB value | 0.6 + 1.2·pct | + optional elite override |
| severity dist | 65/25/10 minor/mod/major | table §6 | major = the shock |
| `η_on, η_off` | injury → on/off-field conversion (VARIABLE) | ~0.6 / ~0.30 ± jitter | on-field floor 0.40, off-field 0.55 |
| `offShare_H` | projected off-field / game | $1.00–1.90 | never live volume |
| `σ0, volFactor, θ` | noise band (VOLUME-LINKED, VARIABLE) | σ0≈1.0 · [0.6,2.2] | thin volume drifts more; volume is internal, Friday-only display |

---

## 11. Engine integration (both engines, when you approve)

- Replace the live price line (`price = base + banked + lgLive(wp) + offfield`) with the
  `P_fair` decomposition **+ `ε` noise** → `P_mkt`, in **both** the store engine and
  `lgSimulate` (identical, so live and replay match).
- The whistle bank = a **fixed $5** win revenue into `Base_H` (win) or $0 (loss), **plus** the
  live `C2/C4` re-rate persisting; reconcile with the existing `seasonFair` between-game
  revision so there's no double-count. Confirm the banked win is exactly $5, always.
- Upgrade the injury event to carry `{position, severity}` and emit the two-sided shock.
- `snap()` gains `{c1,c2,c3,c4,pFair,pMkt,wpPre}` so the UI renders disclosure + live strip
  without recomputing.
- Both instruments (H and O) reprice off the same play (mirror on the win-premium axis;
  independent on the injury/forward axis).

---

## 12. Red-line — RESOLVED (Edwin, Aug 8)

1. **Noise band** → **variable, volume-linked.** Thin volume drifts more; heavy volume tends
   efficient (tendency, not absolute). Volume is an internal input, never displayed intra-game
   (Friday-only). *(§7)*
2. **Forward re-rate** → **variable per game** (`ρ_game`); the **injury path can torpedo a season**
   and is exempt from the modest performance clamp (Rodgers/Jets). *(§3, §6)*
3. **Star values** → **derived**, no hand-set override. See **Appendix A**. *(§6)*
4. **Off-field injury** → **yes, off-field is hit too, variably** (`η_off`, stickier than on-field).
   *(§4, §6)*
5. **Disclosure** → **collapse base + remaining into one clean "Season value" line**; current-game
   pieces stand out; three rows + total. *(§8)*

**Remaining before code:** final numeric feel-tuning (the `σ0`/`volFactor`/`ρ`/`η` centers +
jitter widths — best dialed by watching live games, not on paper), then wire into both engines.
Nothing structural is open.

---

## Appendix A — Derived per-team QB star value (all 32 NFL)

`starValue_QB(team) = 0.6 + 1.2 · seasonFairPct(team)`, where `seasonFairPct` = the team's IPO-price
percentile within the league (the existing brand/performance/price model). Pure derivation, no hand
tuning. Sanity: **KC 1.57 vs CAR 0.83** — Mahomes reprices ~1.9× harder than Carolina's QB.

| Tier | Teams (QB value) |
|---|---|
| Elite (≥1.55) | LAR 1.80 · BAL 1.76 · BUF 1.72 · DET 1.68 · SEA 1.65 · SF 1.61 · KC 1.57 |
| Strong (1.25–1.54) | PHI 1.53 · NE 1.49 · CIN 1.45 · GB 1.41 · HOU 1.34 · DEN 1.34 · DAL 1.30 · LAC 1.26 |
| Mid (1.00–1.24) | CHI 1.22 · JAX 1.18 · MIN 1.14 · PIT 1.10 · TB 1.06 · NO 1.03 |
| Lower (<1.00) | IND 0.99 · NYG 0.95 · WAS 0.91 · ATL 0.87 · CAR 0.83 · TEN 0.79 · LV 0.75 · CLE 0.72 · NYJ 0.68 · MIA 0.64 · ARI 0.60 |

**Eyeball note:** because this is pure 2026 price-percentile, a team that is *cheap this season*
gets a *low* QB value — e.g. **NYJ 0.68**. That is correct for current pricing (the Rodgers
"torpedo" magnitude comes from the loose injury clamp × severity, not from NYJ's tier being high).
If any specific team's QB looks mispriced to you, that one team is the case for a targeted override
— but the derivation stands on its own for all 32. Position weights (QB 0.35, etc.) are in §6.
