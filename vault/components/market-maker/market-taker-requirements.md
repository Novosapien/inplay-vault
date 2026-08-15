---
description: "The market taker's normative go-live list — identity, flow, order, money, state and compliance requirements with statuses and a dated addendum"
---

# Market Taker (SNT-1) — Requirements

> **Component:** [[market-maker/market-maker]] · **System:**
> [[market-maker/systems/snt-1-noise-taker]] · **Code:**
> `inplay-market-maker/src/snt/`
> **Purpose:** The normative list for the market taker — what MUST be
> true before it runs against real books. Edwin's reference is the
> design source ([[market-maker/reference/snt1-noise-taker-edwin-2026-07-30|filed here]]);
> this document is what we are actually accountable for building.
> **Testing:** [[market-taker-test-plan]] — the taker's own protocol
> (isolated → joint), born 11-08.
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

### 2026-08-13 — the 12-08 build items BUILT (MM PR #28 + gateway PR #3)

- **T-F07's staleness clock now prices the reading's `fetched_at`**
  (the Fetched-At header — the publisher's fetch instant), never the
  delivery time: skew-clamped, never regressing, no header = no
  freshness, and a redelivered final no longer reopens POST. The
  restart-re-derives-LIVE class is closed.
- **T-S05's comparison source corrected as the 12-08 entry asked:**
  gateway PR #3 forwards the exec report's own tag 9383 as `posSize`;
  the reconciler prefers it (same message as the fill — cannot race,
  cannot half-arrive) and demotes `position.>` to a fallback for books
  that never saw an exec-borne figure. Never fails quiet against an
  old gateway. Awaits: George merges #28, Hasan reviews #3; both ride
  the next deploys. The +31 VATH float patch stays with the operating
  session's next cutover. Session:
  [[market-maker/sessions/2026-08-13-taker-hardening]].

### 2026-08-12 — ⭐ T-S05's first production-class catch (a lost exec report), and the night's hardening

- ⭐ **T-S05 caught a real MESSAGE loss — ✂ corrected 08-12 afternoon:
  the lost message was a POSITION update, not a fill.** Wire forensics:
  all 26 VATH fills journalled 1:1; the triggering exec's own
  `9383=4416` AGREED with the journal to the share; the companion
  `position.>` message was dropped at the churn-storm peak, so the
  reconciler halted against a one-fill-stale venue figure. Positions
  never actually diverged. The rail's fail direction (halt) was right;
  its comparison source needs fixing: **T-S05 should reconcile against
  the exec report's OWN 9383 tag (same message as the fill — cannot
  race, cannot half-arrive), not the parallel position feed.** Build
  item. ⚠ Residue: the recovery adopted the stale 4447 — **snt8's VATH
  float is +31 high** (true base 4416); patch at the next cutover.
  Fresh T15 evidence: 9383 live and share-accurate, twice.
- 📝 Rule-7 refinement (→ MM repo CLAUDE.md next session): recompute
  floats from the RUNNING env (`/etc/snt-1/env` or its dated `.bak`),
  never a convenience file — a stale base fails T-S05 within seconds
  (demonstrated, CFG-0010).
- ✅ The `snt-taker` NATS user now publishes `$JS.FC.SR_PROBABILITIES.>`
  (JetStream flow control) — without it the T-F07 schedule feed could
  stall mid-game (fail-quiet). Fixed on the box, dated `.bak`.
- 🔴 **Top taker build item: the T-F07 staleness clock must price the
  reading's `fetched_at`, not its delivery time** — every restart
  re-derives LIVE from retained messages for 10 minutes (three
  demonstrations on 08-11/12).
- State at close: SNT-CFG-0011, journal `snt8`, 180 books, floats
  venue-reconciled.

### 2026-08-11e — ✅ the two operating setups RECONCILED: one owner, `snt-1.service`

- ✅ **The 08-11d reconciliation is DONE** (session:
  [[market-maker/sessions/2026-08-11-taker-cutover]]). The running nohup
  taker was halted on the control channel (halt journalled, 0 cancels
  out), then killed by a ps-fields match. The unit env
  (`/etc/snt-1/env`, dated `.bak` kept) now carries: **SNT-CFG-0007** ·
  fresh journal `/var/lib/mm/snt4/` · `SNT_MINUTES=0` ·
  `SNT_STATE=AUTO` · the reconciled floats. `~/snt-0811.env` renamed
  `.retired-20260811`. The unit boots armed on the fresh journal:
  5 books, AUTO (derived), maker undisturbed.
- ⭐ **The floats moved — the 20:51 env values were stale by 21:28.**
  The nohup taker kept trading under its PRE_KICKOFF pin, so the new
  floats = env floats + whole-journal drift at the halt (the T-S05
  algebra, cross-checked against the journal's line-75 reconcile
  record): **COWB 4162 · STEE 5943 · EAGL 5565 · GIAN 4485 ·
  PATR 5039.** Lesson: floats are positions, not constants — recompute
  at every journal cutover, never copy them forward.
- ⚠ Residual: the first fill under SNT-CFG-0007 is the live T-S05 proof
  of the new floats. Fail direction is a safe halt (boots-halted →
  explicit resume after a float patch).

### 2026-08-11d — the joint-run day: T-S05 proven ×5, floats venue-verified, ⚠ TWO operating setups now exist

- ⭐ **T-S05 PROVEN LIVE on all five books** — the reconciler halted on
  real venue-vs-journal gaps (an in-flight fill lost to a plain-kill
  stop; the session's own systemd unit was TERM-killed at 13:48 during
  the books-clearing, which is where the divergence began). Recovery
  lever worked as designed: `SNT_FLOAT_OVERRIDES` per book = venue −
  journalled drift. **Venue-verified floats (account 4963224393):
  COWB 4959 · STEE 5256 · EAGL 5132 · GIAN 4737 · PATR 4836.**
- ✅ **First full validated day against the maker:** 198/198 fills,
  zero rejects · 49.5% buys · clip mean 48 · crossing cost ≤4¢ ·
  drift inside the cap · **journals mirror the maker share-for-share**
  (T13 cross-account evidence; E33 numbers). LIVE-intensity test:
  20 fills/90 s, clean, reverted.
- ✅ T-R01's full lever set exercised live: halt, resume, and the
  state pin (`LIVE` → `PRE_KICKOFF`).
- ⚠ **RECONCILE THE TWO OPERATING SETUPS (next session, first taker
  task)** — ✅ **DONE, see 2026-08-11e above:** the 08-11b systemd deploy (`snt-1.service`, ENABLED but
  inactive since 13:48; journal `/var/lib/mm/snt3`, SNT-CFG-0003,
  STALE float EAGL 4988, `SNT_STATE=AUTO`) vs tonight's hand-run
  (`~/snt-0811.env`, journal `snt-0811`, SNT-CFG-0006, the
  venue-verified floats above, PRE_KICKOFF pin, RUNNING). One owner:
  fold tonight's floats + `SNT_MINUTES=0` into the unit's env, point
  it at a fresh journal (or adopt snt-0811's), bump the CFG, retire
  the nohup. A reboot today would start the unit on stale floats —
  T-S05 halts it at the first fill, so the hazard fails safe.
- 📝 Operating rules from tonight's incident chain: MM repo CLAUDE.md
  (halt-before-stop · CFG bump per restart · boots-halted → resume ·
  `SNT_MINUTES` · kill-pattern/cwd footguns).

### 2026-08-11c — SHORTS BUILT (T-O10), the 10-08 change-flag resolved

- **George's override** (he asked Edwin 10-08 — Edwin wants shorts;
  the mechanic is the platform's flatten-first-then-short): build now,
  numbers follow. **MM PR #15**, off by default (`SNT_SHORTS`).
- **T-O06 ✎:** "side 2 only" is superseded — side 2 while long, side 5
  from flat-or-short when enabled, never both resting.
- **T-O08 ✎:** "never goes short" is superseded — runs from the float
  and may short within `max_short_shares` (default 1,000 = QA's borrow
  reserve, 🟡 OURS; E26 rules the real depth/cover).
- **T-O10 (never straddle zero) 🔴 → 🟡:** built verbatim; a 400-order
  walk test crosses zero both ways without one order straddling.
- ⚠ Dormant under the standard float (holding never nears zero); the
  QA test needs a zero-float book — JETS once Rob resets its band.
  Side-5 entitlement on account `4963224393` is untested (T16).
- The maker's half (N34) is handed to the MM session with the design
  note: the side flip happens at order MINTING (a replace cannot
  change side), chosen by coverage.

### 2026-08-11b — DEPLOYED: unattended systemd on the MM VM, own NATS credential

- **The taker runs as `snt-1.service`** on the MM VM: `main@5681767`,
  `SNT-CFG-0003`, journal `/var/lib/mm/snt3`, `SNT_STATE=AUTO`, EAGL
  float pinned 4,988. No more hand-run bounded sessions.
- **The 10-08c grant hole is CLOSED — by us, on George's ruling** (do
  the Hasan asks ourselves): a dedicated `snt-taker` NATS user carries
  the kill-switch subjects and a SCOPED JetStream consume on the new
  `SR_PROBABILITIES` stream. **T-R01 drilled live on the deployed
  unit** (halt → resume, journaled). Credentials in Secret Manager
  (`snt-taker-nats-password`, `snt-taker-venue-login`).
- The stream is EMPTY until the sportradar service's mm-publisher
  worker deploys (its publish grant is ready) — so AUTO derives
  OVERNIGHT, the correct quiet default. Books are also empty while the
  MM engine is stopped, so the bot rests. Full detail:
  [[market-maker/decisions]] 2026-08-11b.

### 2026-08-11 — T-F07 BUILT: the state derives from the schedule (MM PR #14)

- **T-F07 moves 🔴 → 🟡.** George's source ruling (option A): the taker
  consumes the bus — the sportradar service's
  `sr.probabilities.reading.>` JetStream feed, whose every payload
  carries `kickoff_time`, `status`, scores and both competitor ids.
  Game → ticker via `mm/bindings.py::TEAM_BINDINGS` (the shared table;
  a runtime dependency on the bus, never on the MM process).
- **The state is per BOOK now, not per bot** — the two teams in a game
  go PRE_KICKOFF → LIVE → POST; the rest stay OVERNIGHT. Book-visible,
  so Edwin confirms the shape in his round (filed on E41).
- **Precedence:** `SNT_STATE=AUTO` derives; a named state PINS every
  book; `{"cmd":"state","value":"AUTO"}` un-pins. Pin/AUTO marks stay
  journaled and outrank env. Derived transitions journal audit-only —
  boot re-derives from the live bus, books sit OVERNIGHT until it does.
- **Fail direction is QUIET everywhere:** unknown kickoff, silent feed,
  missing grant → OVERNIGHT (×1), never LIVE (×75).
- **IPO windows are config** (`SNT_IPO_WINDOWS`, InPlay calendar facts —
  not SR facts): inside a window every book floors at PRE_KICKOFF.
- **Four numbers are OURS, filed 🟡 in [[market-maker/parameters]]:**
  pre-kickoff window 1 h · POST window 1 h · LIVE staleness bound
  10 min · file-game length 4 h. `SNT_SCHEDULE_FILE` is the fallback
  source (tests, pre-grant dry runs) behind the same store.
- ⛔ **New grant owed (Hasan):** JetStream consume on
  `sr.probabilities.>` for the taker's NATS user — bundle with the owed
  `snt.control.{bot_id}` grant. 655 tests green; PR #14, stacked on #12.

### 2026-08-10c — FIRST LIVE RUNS: T-S05's first catch was a true positive

- **Run 1:** one fill, then `RECONCILE HALT venue=4988 ours=5000` — the
  bot was blind to its own fills (the gateway carries the ClOrdID only
  in the order SUBJECT; the taker read the body). T-S05 caught it on
  trade one. Fixed (`with_subject_order_id`, commit `0570bf5`).
- **Run 2:** clean — fills folding both ways across the five books,
  reconciler silent (= verifying every fill). **T-O01–T-O08, T-M03 and
  T-S05 have now RUN against the venue** on the taker's own account.
- Wire facts learned: the gateway REQUIRES the `MM` ClOrdID prefix on
  `gateway.orders.mm.*` → the taker mints **`MMSN` + 14 hex**
  (`20f6a51`); riding that namespace puts its orders under the global
  dead-man sweep, and the taker must NEVER publish MM heartbeats (the
  latch is global — a second beater would mask the engine's death).
- ⛔ **`snt.control.{bot_id}` is not granted** to the NATS user — the
  kill switch (T-R01) is DEAD in QA runs until Hasan adds the grant
  (ideally a dedicated NATS user for the taker). Process kill is the
  interim stop.
- The float is env-tunable (`SNT_FLOAT_SHARES`, `SNT_FLOAT_OVERRIDES`)
  so the operator pins it to the account's verifiable reality — which
  T-S05 enforces.

### 2026-08-10b — T-S05 BUILT · the base committed · the taker's identity complete

- **T-S05 moves 🔴 → 🟡.** George approved after the plain-terms
  explanation ("we can consume this from the venue, which is tZERO").
  `snt/reconcile.py` + runtime wiring: `position.{userId}` in, compare
  against `holding()`, mismatch surviving 5 s → the journaled halt with
  both numbers. Never adopts the venue figure (T15). One deliberate
  deviation: the halt is BOT-WIDE, not per-book — stricter than the
  requirement; a divergence undermines trust in the whole tally.
  10 tests; 638 green.
- **The 09-08 work is now COMMITTED and the branch pushed**
  (`feat/snt-1-float-and-sell-gate`: `7e2b54d` the float + gate +
  hardening, `2de7775` T-S05).
- **T-I01 identity complete** (see the row): user id
  `385656921832584863` · account `4963224393`.
- **➕ Same day: the float is REAL.** George's call — seeded via the
  gateway's `35=UPT` position-transfer path (Hasan's "second
  inventory-seeding path", one-way, non-idempotent): **5,000 shares on
  each of the five live tickers** (EAGL/PATR/GIAN/COWB/STEE — JETS
  excluded, its book is band-blocked), cost basis at the mid at
  transfer (EAGL 389,025 · PATR 398,975 · GIAN 305,475 · COWB 380,900
  · STEE 331,725). All five venue-accepted (`UPTa`). This resolves
  E39's mechanism-for-QA and matches the built default
  `float_shares=5000`, so T-S05 boots clean. E39's PRODUCTION answers
  (real allocation size, Edwin's cost-basis ruling for the tilt) stay
  open. **PR #12 opened** for the whole taker branch.

### 2026-08-10 — Edwin wants the taker to SHORT (change requested, venue-gated)

- George, relaying Edwin: **SNT-1 must be able to go short.** Nothing is
  changed in the list yet.
- **The venue path EXISTS (corrected same day):** the platform already
  shorts live via **FIX side 5** — the app maps it, the gateway sends
  it, the service layer charges full-notional collateral with a
  **1,000 shares/security borrow reserve on QA** (T-M06). The 08-09
  sell rule (`Pos − livS`, whole-order reject) governs side-2 sells
  only. The platform's model is **flatten first, then short** — long
  and short are exclusive states.
- **T-O06 (side 2 only) and T-O08 (never goes short) are change-flagged
  ✎⛔:** they stay TRUE of the built code until **E26** (Edwin's
  taker-side rules: when, how deep, how covered) and **T16** (the
  house-account side-5 specifics: borrow backing, venue-vs-service
  checks — SNT-1 bypasses the service, so only venue checks bind it)
  come back. Do not build ahead of either.
- Design note for when it unblocks: the sell gate extends rather than
  inverts — side 2 up to `Pos − livS`, then side 5 within the borrow
  cap; drift already tolerates negative internally. The SNT runtime
  today maps only buy=1/sell=2. The risk work (depth, cover,
  disclosure E33/T13) is the real substance.
- **➕ Same day, George's mechanism ruling → new requirement T-O10:**
  the taker **never straddles zero** — longs cleared before any short,
  shorts cleared before any long, no single order crossing zero.
  Probably the maker too — that half is **N34** (two-sided quoting
  makes strict order-level exclusivity non-trivial for the MM).

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
| T-I01 | Runs on its OWN venue account, separate from the market maker | EDWIN/OURS | 🟡 ✎ | **Identity COMPLETE (10-08): user id `385656921832584863` · venue account `4963224393` · login `hasan.ahmed+MT@novosapien.ai`** (Hasan-created; credential held off-vault; user id from the Zitadel lookup, cross-validated against the MM's). Still owed: is this the **IPLP** slot or a retail-class account (decides T-I02 and the E33/T13 posture) |
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
| T-F04 | Intensity scales by activity state and per-team weight | EDWIN | 🟡 ✎ | state DERIVED per book since 11-08 (T-F07); weights still stub at 1.0 (E41 feed) |
| T-F05 | It NEVER conditions on book state, other participants, or any external signal | EDWIN | ✅ | reads only its own basis |
| T-F06 | The disposition (profit) tilt is the ONLY departure from pure noise, and it conditions solely on own cost basis | EDWIN | ✅ ⚠ | **flagged to compliance** — it makes flow weakly correlated with price |
| T-F07 | Activity state maps correctly — off-season/overnight → OVERNIGHT, IPO windows → PRE_KICKOFF at minimum | EDWIN | 🟡 ✎ | **built 11-08** (PR #14): derived PER BOOK from the sportradar bus (`sr.probabilities.reading.>` — kickoff/status/teams in every payload); IPO windows via `SNT_IPO_WINDOWS` floor books at PRE_KICKOFF; operator pin + AUTO un-pin, journaled. Err-quiet: any gap derives OVERNIGHT. Grant LIVE 11-08b (snt-taker user, verified end to end); real derivation waits on the mm-publisher worker deploy — the stream is empty until then |

## O · Order mechanics

| # | Requirement | Source | Status | Note |
|---|---|---|---|---|
| T-O01 | 90% of orders sit AT the touch | EDWIN | ✅ | tested |
| T-O02 | At-touch size ≤ half the displayed quantity — never exhaust a level | EDWIN | ✅ | tested |
| T-O03 | Taker only — never posts resting liquidity | EDWIN | 🟡 ✎ | **cannot be literally true**: with no IOC, the substitute rests up to the cancel window. Edwin to re-word |
| T-O04 | Sweeps (10%) are capped at 3 ticks through the touch | EDWIN | ✅ | the real impact cap |
| T-O05 | The IOC substitute is a marketable DAY order plus a cancel after a short window | OURS (E32) | ✅ | tZERO has no IOC |
| T-O06 | Sells side 2 while long; side 5 only from flat-or-short, when enabled | OURS ✎ (11-08) | 🟡 | **superseded 11-08** (PR #15): shorts built under T-O10, `SNT_SHORTS`-gated, off by default. Side-5 entitlement on the taker's account untested (T16) |
| T-O07 | **A sell never exceeds `Pos − livS`** — position minus quantity already committed to live resting sells | VENUE | 🟡 ✎ | **built 09-08.** Cuts the sell to what is sellable; below the 5-share minimum it stays quiet. `livS` is our own un-settled sells, counted at full quantity (conservative) |
| T-O08 | **Runs from a seeded float; may short within the cap when enabled** — the inventory rule measures drift from the float baseline, not from zero | OURS ✎ (11-08) | 🟡 | **built 09-08; "never goes short" superseded 11-08** (PR #15). The float is config, not journaled state; the soft cap and tilt measure from the float unchanged. Size + cost stay E39; short depth rides E26 |
| T-O09 | Respects the per-symbol LmtPerc bands | VENUE | 🟡 | inherits from pricing at the touch; untested at the edges |
| T-O10 | **Never straddles zero** — clears longs before any short, clears shorts before any long. A single order never crosses zero; side 5 rests only when flat with no live side-2 sells; while short, buys only reduce toward flat | GEORGE (10-08) | 🟡 ✎ | **built 11-08** (PR #15), verbatim; walk-tested across zero both ways. Unrun against the venue; dormant under the standard float (see addendum) |
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
| T-S05 | Internal position is periodically reconciled against the venue; divergence HALTS that book | EDWIN | 🟡 ✎ | **built 10-08** (`snt/reconcile.py`, George approved after the plain-terms explanation). Listens on `position.{userId}` (tag 9383); a mismatch surviving the grace window (5 s) fires the SAME journaled halt as the kill switch, both numbers printed, live orders swept. The venue's figure is NEVER adopted (T15 unconfirmed). Halt is bot-wide, stricter than the row asks. Unrun against the venue |
| T-S06 | Seeded randomness and an injected clock — no wall clock in decisions | OURS | ✅ | tested |
| T-S07 | Every deploy bumps the config version | OURS | ✅ | new id space per deploy |

## R · Safety

| # | Requirement | Source | Status | Note |
|---|---|---|---|---|
| T-R01 | A kill switch stops it immediately | EDWIN | ✅ ✎ | **built 09-08, grant live + drilled on the deployed unit 11-08** (halt → resume, journaled; the snt-taker NATS user carries both sides of `snt.control.>`) |
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

**Built 10-08:** T-S05 (position reconciliation) — and its first live
act was a true positive (the subject-ClOrdID fix). The taker then ran
clean: 67/67 fills on its own account. **Built 11-08:** T-F07's real
derivation (per-book state from the sportradar bus, PR #14) — unrun
against the venue, and live use waits on the JetStream grant.

**Still open:** the T15 question that bounds T-S05's trust (is tag 9383
live — Rob), the E41 weight feed (T-F04's stub), and the shorts build
(T-O10 + side-5) queued behind E26 + T16.

**Blocked, and not by us:** the account, Edwin's config rulings, and
the compliance read.
