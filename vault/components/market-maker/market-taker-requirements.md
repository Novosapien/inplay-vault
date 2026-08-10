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

### 2026-08-09c — the notional cap, the kill switch, and the state lever BUILT

- **T-M03 moves 🔴 → 🟡.** The cap cuts the order to fit (same posture
  as the sell gate); below the minimum size it stays quiet. The value —
  **$25,000/order** — is OURS, Edwin never gave one; filed 🟡 in
  [[market-maker/parameters]], his ruling rides E32.
- **T-R01 moves 🔴 → 🟡.** A kill switch on NATS
  (`snt.control.{bot_id}`): halt stops new orders AND cancels every live
  order, resume re-arms with redrawn schedules. **Both are journaled, so
  a restart cannot silently re-arm a halted bot** — the MM's dead-man
  lesson applied.
- **T-F07 stays 🔴, but the note changes:** activity state is now
  operator-settable at runtime (`{"cmd":"state","value":"LIVE"}`,
  journaled, outranks the env boot default). The REQUIREMENT — the state
  derived correctly from the schedule — is still not built; what exists
  is the lever an operator pulls by hand.
- **Deployment artifacts exist:** `deploy/snt-1.service`,
  `deploy/snt-1.env.example`, `docs/SNT-RUNBOOK.md` in the MM repo.
  Nothing is deployed. ⚠ The runbook records the **shared-account
  caveat**: on the MM account (the QA posture) the venue's per-account
  sell check makes the taker's inventory arithmetic wrong in both
  directions, so a QA run there tests wiring, not inventory behaviour.

### 2026-08-09b — the float and the sell gate BUILT

- **T-O07 and T-O08 move 🔴 → 🟡** (built, unverified against the venue).
  Both landed together, because neither is safe alone: the gate needs
  inventory behind it, and the float needs the gate to stop it being
  spent. Code: `snt/agent.py`, `snt/pending.py`, `snt/runtime.py`;
  11 new tests, 620 green.
- **George's ruling that made it buildable: SNT-1 participates in the
  IPO, so it already holds shares when it starts.** No purchase, no
  seeding script, no opening trade of its own.
- **The float is CONFIGURATION, not journaled state.** `pos` keeps its
  meaning — net shares from own fills — so a journal replay can never
  double the float, and the journal schema does not change. Holding =
  float + pos.
- **T-O08 needed no new inventory rule.** The soft cap and the profit
  tilt already act on `pos`, and `pos` is drift from the float, so both
  already mean "return to the float". They flatten the drift; they never
  drain the float.
- **The float size (5,000/team) and the float's cost are OURS and
  UNVERIFIED** — filed 🟡 and 🔴 in [[market-maker/parameters]] under
  new question **E39**. The cost matters: while it is unknown the
  disposition tilt keeps comparing mid against the VWAP of what the
  taker itself traded, not against the true cost of the holding. We did
  not invent a basis.
- ⚠ **The gate trusts our own arithmetic.** If the float is not actually
  on the account, the bound we compute is not the bound the venue
  applies. That is **T-S05**, still 🔴.

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
| T-F07 | Activity state maps correctly — off-season/overnight → OVERNIGHT, IPO windows → PRE_KICKOFF at minimum | EDWIN | 🔴 ✎ | operator-settable at runtime 09-08 (journaled control command); the DERIVATION from the schedule is still not built |

## O · Order mechanics

| # | Requirement | Source | Status | Note |
|---|---|---|---|---|
| T-O01 | 90% of orders sit AT the touch | EDWIN | ✅ | tested |
| T-O02 | At-touch size ≤ half the displayed quantity — never exhaust a level | EDWIN | ✅ | tested |
| T-O03 | Taker only — never posts resting liquidity | EDWIN | 🟡 ✎ | **cannot be literally true**: with no IOC, the substitute rests up to the cancel window. Edwin to re-word |
| T-O04 | Sweeps (10%) are capped at 3 ticks through the touch | EDWIN | ✅ | the real impact cap |
| T-O05 | The IOC substitute is a marketable DAY order plus a cancel after a short window | OURS (E32) | ✅ | tZERO has no IOC |
| T-O06 | Sends side 2 only — never side 5 (sell short) | OURS (E26) | ✅ | by construction |
| T-O07 | **A sell never exceeds `Pos − livS`** — position minus quantity already committed to live resting sells | VENUE | 🟡 ✎ | **built 09-08.** Cuts the sell to what is sellable; below the 5-share minimum it stays quiet. `livS` is our own un-settled sells, counted at full quantity (conservative) |
| T-O08 | **Runs from a seeded float and never goes short** — the inventory rule measures drift from the float baseline, not from zero | OURS | 🟡 ✎ | **built 09-08.** The float is config, not journaled state; `pos` stays drift, so the soft cap and the tilt already measure from the float. Size + cost are assumptions — **E39** |
| T-O09 | Respects the per-symbol LmtPerc bands | VENUE | 🟡 | inherits from pricing at the touch; untested at the edges |
| T-O10 | Never trades a halted, locked, crossed, one-sided, or too-wide book | EDWIN | ✅ | tested |
| T-O11 | The spread gate must be wider than the narrowest production spread | EDWIN (E32) | 🔴 | **8 ticks < §5.2 Stable's 10** — as configured it would never trade. Needs his ruling |
| T-O12 | Never acts on a stale book snapshot | OURS | ✅ | 30 s gate, from the 08-08 MD evidence |

## M · Money control

| # | Requirement | Source | Status | Note |
|---|---|---|---|---|
| T-M01 | A per-team, per-session loss budget silences the book when spent | EDWIN | ✅ | tested |
| T-M02 | The budget meters fill-vs-mid-at-send, floored at zero | EDWIN | ✅ | spread subsidy, not marked P&L |
| T-M03 | There is a per-order notional cap | EDWIN | 🟡 ✎ | **built 09-08** — cuts the order to fit under $25,000 (our number, E32); below min size it stays quiet |
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
| T-R01 | A kill switch stops it immediately | EDWIN | 🟡 ✎ | **built 09-08** — `snt.control.{bot_id}`: halt stops new orders + cancels every live order, journaled so a restart stays halted |
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
wiring, the reject guard — MM PR #10, 27 tests. **Plus the float and the
sell gate — 09-08, 11 tests** (T-O07, T-O08).

**The two correctness items are closed.** Before them the taker rejected
on its own sells the first time it tried to trade a book down. It now
holds an IPO float and cuts every sell to what the venue will accept.
Both are 🟡, not ✅ — nothing has run against a real book yet.

**Built 09-08c:** T-M03 (the notional cap) and T-R01 (the kill switch),
both 🟡. Deployment artifacts exist (`deploy/`, `docs/SNT-RUNBOOK.md`);
nothing is deployed.

**Still not built:** **T-S05 (position reconciliation) — now the single
most important item.** The sell gate computes its bound from our own
arithmetic, so a float that is not actually on the account produces a
bound the venue does not share. The gateway already publishes
`position.{userId}` per symbol from tag 9383, so the input path exists —
but 9383 was observed NOT moving per fill (08-09), so whether it is a
live position is a Rob question (T15). Also open: T-F07's real
derivation, and the shared-account caveat that makes a QA run on the MM
account a wiring test only.

**Blocked, and not by us:** the account, Edwin's config rulings, and
the compliance read.
