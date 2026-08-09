# Market Taker (SNT-1) — Requirements

> **Component:** [[market-maker/market-maker]] · **System:**
> [[market-maker/systems/snt-1-noise-taker]] · **Code:**
> `inplay-market-maker/src/snt/`
> **Purpose:** The normative list for the market taker — what MUST be
> true before it runs against real books. Edwin's reference is the
> design source ([[market-maker/reference/snt1-noise-taker-edwin-2026-07-30|filed here]]);
> this document is what we are actually accountable for building.
> **Born:** 2026-08-09 (George).

**How to change this document.** Do not silently edit a requirement.
Add a dated entry to the **Addendum**, then edit the requirement in
place and mark it ✎. The addendum is the audit trail; the list is
always current truth.

**Status:** ✅ built and tested · 🟡 built, unverified against the venue ·
🔴 not built · ⛔ blocked externally · ✎ changed (see addendum)

**Source:** `EDWIN` = his reference or email · `VENUE` = observed on the
real venue (not ours to change) · `GEORGE` = his ruling ·
`OURS` = our engineering decision, recorded · `COMPLIANCE` = pending a
legal/compliance read, not an engineering call.

---

## Addendum — changes to these requirements

### 2026-08-09 — created, and the sell rule folded in

- Created from Edwin's reference plus the venue facts learned 07-08 and
  08-08. Baseline status: the agent, the IOC substitute, the journal and
  the wiring are built (MM PR #10); the inventory requirements are not.
- **T-O07 / T-O08 added** from the live probe: a sell may not exceed
  `Pos − livS`, and the taker runs from a seeded float so it never goes
  short. Neither is in the built code.
- **T-O03 weakened to 🟡** — "never rests" cannot be literally true on a
  venue with no IOC; the substitute rests for up to the cancel window.
  Needs Edwin to re-word the guarantee.

---

## I · Identity and account

| # | Requirement | Source | Status | Note |
|---|---|---|---|---|
| T-I01 | Runs on its OWN venue account, separate from the market maker | EDWIN/OURS | ⛔ | account not yet assigned |
| T-I02 | Carries its own tape identity — MPID **IPLP** | VENUE (Rob, 07-08g) | ⛔ | Rob cuts it over when the account onboards |
| T-I03 | Flagged `account_type = HOUSE_SYNTHETIC`, `leaderboard_eligible = false`, `participant_side = false` | EDWIN | 🔴 | platform-side concepts, not tZERO's — ours to implement |
| T-I04 | Identity is configuration, never code — one variable moves it between accounts | OURS | ✅ | `SNT_*` env, PR #10 |
| T-I05 | Runs as its own process, not inside the MM engine | OURS | ✅ | single-writer journal + E33 separation |

## F · Flow character — the reason it exists

Its entire purpose is trading activity that carries **no information**.
Every requirement here protects that property.

| # | Requirement | Source | Status | Note |
|---|---|---|---|---|
| T-F01 | Arrivals are Poisson — no schedule a participant can learn or front-run | EDWIN | ✅ | seeded, tested |
| T-F02 | Direction is 50/50 at its core | EDWIN | ✅ | tested |
| T-F03 | Sizes are log-normal, clipped 5–400 shares | EDWIN | ✅ | tested |
| T-F04 | Intensity scales by activity state and per-team weight | EDWIN | 🟡 | state is configured, not derived; weights stub at 1.0 |
| T-F05 | It NEVER conditions on book state, other participants, or any external signal | EDWIN | ✅ | reads only its own basis |
| T-F06 | The disposition (profit) tilt is the ONLY departure from pure noise, and it conditions solely on own cost basis | EDWIN | ✅ ⚠ | **flagged to compliance** — it makes flow weakly correlated with price |
| T-F07 | Activity state maps correctly — off-season/overnight → OVERNIGHT, IPO windows → PRE_KICKOFF at minimum | EDWIN | 🔴 | currently a static env value |

## O · Order mechanics

| # | Requirement | Source | Status | Note |
|---|---|---|---|---|
| T-O01 | 90% of orders sit AT the touch | EDWIN | ✅ | tested |
| T-O02 | At-touch size ≤ half the displayed quantity — never exhaust a level | EDWIN | ✅ | tested |
| T-O03 | Taker only — never posts resting liquidity | EDWIN | 🟡 ✎ | **cannot be literally true**: with no IOC, the substitute rests up to the cancel window. Edwin to re-word |
| T-O04 | Sweeps (10%) are capped at 3 ticks through the touch | EDWIN | ✅ | the real impact cap |
| T-O05 | The IOC substitute is a marketable DAY order plus a cancel after a short window | OURS (E32) | ✅ | tZERO has no IOC |
| T-O06 | Sends side 2 only — never side 5 (sell short) | OURS (E26) | ✅ | by construction |
| T-O07 | **A sell never exceeds `Pos − livS`** — position minus quantity already committed to live resting sells | VENUE | 🔴 ✎ | **not built.** The venue rejects the whole order over this |
| T-O08 | **Runs from a seeded float and never goes short** — the inventory rule measures drift from the float baseline, not from zero | OURS | 🔴 ✎ | **not built.** Makes T-O06/T-O07 safe by construction |
| T-O09 | Respects the per-symbol LmtPerc bands | VENUE | 🟡 | inherits from pricing at the touch; untested at the edges |
| T-O10 | Never trades a halted, locked, crossed, one-sided, or too-wide book | EDWIN | ✅ | tested |
| T-O11 | The spread gate must be wider than the narrowest production spread | EDWIN (E32) | 🔴 | **8 ticks < §5.2 Stable's 10** — as configured it would never trade. Needs his ruling |
| T-O12 | Never acts on a stale book snapshot | OURS | ✅ | 30 s gate, from the 08-08 MD evidence |

## M · Money control

| # | Requirement | Source | Status | Note |
|---|---|---|---|---|
| T-M01 | A per-team, per-session loss budget silences the book when spent | EDWIN | ✅ | tested |
| T-M02 | The budget meters fill-vs-mid-at-send, floored at zero | EDWIN | ✅ | spread subsidy, not marked P&L |
| T-M03 | There is a per-order notional cap | EDWIN | 🔴 | his hardening point 1 — not built |
| T-M04 | Intensity, not the budget, is the real spend lever | EDWIN (E32) | 🟡 | at LIVE it burns ~$1.5k/hr against a $100k budget — the governor cannot bind |
| T-M05 | Inventory is soft-capped and mean-reverted so no directional book accumulates | EDWIN | ✅ | 1,500-share cap, 80% flatten bias |
| T-M06 | The soft cap must not conflict with venue reserves | VENUE | 🟡 | 1,500 vs the QA rig's 1,000 short reserve; production capacity is 5M/5M |

## S · State, recovery, determinism

| # | Requirement | Source | Status | Note |
|---|---|---|---|---|
| T-S01 | Position and basis survive a restart | EDWIN | ✅ | journal replay, tested |
| T-S02 | The session loss budget survives a restart | OURS | ✅ | else a restart re-arms a spent budget |
| T-S03 | The send counter survives — a restart never re-mints a used ClOrdID | VENUE | ✅ | the 07-08 duplicate deadlock |
| T-S04 | Internal position is the source of truth on the trading path | EDWIN | ✅ | by construction |
| T-S05 | Internal position is periodically reconciled against the venue; divergence HALTS that book | EDWIN | 🔴 | his hardening point 3 — not built |
| T-S06 | Seeded randomness and an injected clock — no wall clock in decisions | OURS | ✅ | tested |
| T-S07 | Every deploy bumps the config version | OURS | ✅ | new id space per deploy |

## R · Safety

| # | Requirement | Source | Status | Note |
|---|---|---|---|---|
| T-R01 | A kill switch stops it immediately | EDWIN | 🔴 | his hardening point 1 — process stop only today |
| T-R02 | Rejects are first-class — a persistently rejecting book goes quiet | OURS | ✅ | Edwin's reference cannot see rejects at all |
| T-R03 | Every action is logged and auditable | EDWIN | 🟡 | journal covers economics; ops logging is thin |
| T-R04 | It cannot interfere with the market maker's orders or state | OURS | ✅ | separate process, account, journal, id prefix |

## C · Compliance — not engineering calls

| # | Requirement | Source | Status | Note |
|---|---|---|---|---|
| T-C01 | Two house accounts trading with each other is cleared by compliance | COMPLIANCE (E33) | ⛔ | Troy + InPlay legal. **Nothing ships before this** |
| T-C02 | tZERO does not treat the two house accounts as related (wash blocking) | VENUE (T13) | ⛔ | cross-account half open with Rob |
| T-C03 | Its prints earn no leaderboard credit | EDWIN | 🔴 | platform-side |
| T-C04 | Its prints are excluded from the off-field volume split | EDWIN | 🔴 | platform-side; ≥1-participant-side rule |
| T-C05 | The profit tilt is disclosed in the compliance read | OURS | 🟡 | filed on E32; weakens the "certified uninformative" claim |

## X · External gates

| # | Gate | Owner | Blocks |
|---|---|---|---|
| X-T1 | The second house account + IPLP MPID | Rob / tZERO | T-I01, T-I02 — everything |
| X-T2 | E32 rulings: the spread gate, the IOC re-wording, the inventory cap | Edwin | T-O03, T-O11, T-M06 |
| X-T3 | The compliance read | Troy / legal | T-C01 — shipping |
| X-T4 | Per-team popularity weights | Edwin (EAV model) | T-F04 |

---

## Where it stands

Built and tested: the brain, the IOC substitute, the journal, the
wiring, the reject guard — MM PR #10, 27 tests.

**Not built, and all of it inventory-shaped:** T-O07 (the sell bound),
T-O08 (the seeded float), T-S05 (position reconciliation), T-M03 (the
notional cap), T-R01 (the kill switch), T-F07 (activity-state mapping).
The first two are correctness — without them the taker rejects on its
own sells the first time it tries to trade down a book.

**Blocked, and not by us:** the account, Edwin's config rulings, and
the compliance read.
