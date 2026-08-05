# 2026-07-22 — MM workstream foundation: standards → understanding → structure → process

> **Who:** George + Claude
> **Type:** research / design / process — the foundation session for the whole MM workstream
> **Span:** one continuous working session across 20–22 July (touchdown processing → standards deep-dive → component build → platform-doc reconciliation → process setup)
> **Refs:** [[20-07-2026-touchdown]] · [[standards/README|CTS-001 / CTS-002 / PTS-001]] · `trading-architecture.md` (platform team, 21-07 upd. 22-07) · PR pending (everything below is uncommitted on `digest/touchdowns-13-17-jul`)

---

## Why this session happened

The three technical standards (CTS-001 valuation, CTS-002 market operations,
PTS-001 the SDMM) landed on us ~a month before launch, written in dense
pseudo-legal style, with the initial assumption that they described someone
else's system. This session took us from "what even is this?" to: confirmed
scope, a complete plain-English knowledge base, a structured vault component,
concrete pseudocode with proposed defaults, a feasibility estimate, and a
working process for the build. It is the foundation everything after builds on.

---

## What we did

### 1 · Understood the standards (and built the tools to keep understanding them)

- Read all three standards end-to-end. Established the core model: **value ≠
  price** — a valuation engine computes ESV, market ops publishes it as the
  Reference Price, the SDMM quotes two-sided ladders around it, tZERO matches.
  The SDMM is a **feedback control loop** (inventory skew = setpoint
  controller; pricing profiles = gain scheduling) — George's mech-eng
  background maps directly onto it.
- **Built the plain-English guides**: [[standards/CTS-001-plain-english-guide]]
  and [[standards/CTS-002-plain-english-guide]] (markdown + styled HTML
  renderings), matching the existing PTS-001 guide format. Each includes a
  20-07-touchdown supersession section and a quirks register.
- **Built the interactive machine map**: `standards/sdmm-machine.html` — every
  engine and equation clickable, every symbol defined in a "where" panel
  (context-aware: `F` = refresh multiplier in one equation, classification
  function in another). v2 reconciled against the touchdown: ✓ confirmed
  flags, ✂ descoped Ch5, the green Touchdown Reconciliation card.
- **Discovered CTS-001 §3 is missing**: the vault copy ends at §2.33 — the
  formal valuation math is referenced throughout and absent. (Later
  substantially filled by Edwin's spoken formula + the sheet decode.)

### 2 · Processed the 20-07 touchdown (the session that changed everything)

Full detail in [[market-maker/decisions]]. Headlines:

- **Scope settled:** George asked build-or-consume; Edwin: **"We will build
  them."** All three standards are Novosapien builds. The docs themselves were
  "meant for Claude to read… fairly simple" — context, not constitution.
- **The valuation formula, spoken:** `price = P(win this game)×$/win +
  E[remaining wins]×$/win + off-field`. Sport Radar live win probabilities are
  the input.
- **Capital unlimited** (~$100M–$100B buying power) → **PTS-001 Ch5 (portfolio
  allocation) descoped** — the zero-sum budget machinery is gone.
- MM = ordinary participant posting **resting liquidity**; limit orders only
  (aggression = pricing through levels); cancel-replace ~5–10×/sec +
  event-triggered recompute; three liquidity sessions (in-game / around-game /
  overnight-wide); markets truly isolated intragame (each game a pairs trade).
- New build items surfaced: **synthetic market order** (before first NFL
  game), **trading bands (~30%) + quote busting** with tZERO, **MM ops desktop
  UI** (Kevin), find **Edwin's old simulation trigger script**.

### 3 · Built the vault component (custom structure)

[[market-maker/market-maker]] — deliberately NOT the standard
component/sub-component pattern: `systems/` (one doc per buildable system:
valuation engine, market state, quoting engine, supervision, synthetic MO,
ops UI) + living working docs (decisions · open-questions · parameters · plan
· glossary). Restructured the existing 20-07 digest hub without losing any
sourced content.

### 4 · Answered the hard conceptual questions (now baked into the docs)

- **Why "republish" ESV as RP if identical?** Publication management, not
  math: gating by lifecycle state, timestamp/version stamping, the
  frozen-price failure mode, and the trust boundary (`RP = ESV` is a *ban* on
  downstream adjustment).
- **Why don't the equations define their operations?** They're **type
  signatures wearing math notation** — the argument list is the law (an
  exhaustive allowlist of what may be consulted) + a purity contract. Bodies
  are lookup tables, threshold rules, and small arithmetic. The only real math
  lives in PTS-001 Ch6.
- **MOP inputs vs outputs:** condition + session in → spread/depth/refresh
  targets out. One layer's outputs are the next layer's inputs (caught by
  George as a wording error in the guide — fixed).
- **What a quotation actually is:** the MM's resting limit orders, both
  sides, all levels; the 8-element Executable Quotation is the record of the
  whole posted ladder + lifecycle metadata. The order book = everyone's
  orders merged by the venue.
- **Bands / halts / busts and who can bust:** three-role model — participants
  cancel their own unfilled orders only; the **venue** (tZERO) voids executed
  trades (`ExecType=H` plumbing already in our FIX docs); the **operator**
  decides when per policy. Busting is NOT an MM power → implies a separate
  **market-supervision** function (conflict of interest: the MM can't judge
  trades it's counterparty to).

### 5 · Wrote the machine out concretely

[[market-maker/systems/decision-cycle-reference]] — **every function in one
decision cycle as runnable pseudocode**: the pure-function loop, trigger
coalescing, assessment windows, the condition classifier, the profile lookup
table, the executable-market constructor, offsets → reservation prices →
ladder → sizes (with a worked example), validation, publish, commit/replay,
fill handling. **~22 proposed constants, every one marked 🟡** — deliberately
drafted by us so Edwin reviews instead of authors. This doubles as the
Thursday agenda.

### 6 · Sized the build

- **Complexity: medium as software** — the 20-07 call deleted the hard parts
  (real capital risk, portfolio allocation, profit pressure). The bar is
  *realism + un-gameability*, not profitability. Hard 20%: FIX integration
  under load, exploitability (stale-quote sniping = #1 prize-integrity
  threat), calibration tail.
- **Estimate:** ~4–6 engineer-weeks build effort with Claude-Code-heavy
  development; **5–8 weeks calendar** (dependency-gated: tZERO access, SR feed,
  Edwin's numbers), one primary builder. **2–3 weeks to a tradeable QA thin
  slice is feasible (~60–70%)** with hard preconditions and an explicit cut
  list — and the mid-August window demands roughly that anyway.
- **Topology recommendation (ours, 21-07):** MM must NOT share the users' FIX
  session/process (identity, failure-domain isolation, control); embed the
  FIX session in the MM service; Drop Copy → supervision.

### 7 · Reconciled against platform reality (`trading-architecture.md`)

The platform team's live-verified map arrived — a day ahead of our vault in
places. **George set the filter: platform + venue facts = gospel; anything
about the MM's own design (their `sdmm.py` prototype, params, 200 ms
full-replace cadence, MM-as-user identity, `gateway.orders.mm.*` seam) =
suggestions only — we build the MM from scratch.** Reconciliation applied
under that filter (decisions 22-07 entries, E1→🟡, T1/T2 reframed, T7
resolved, new E11/E12/N9, parameters updated, plan updated).

Adopted facts, headlines:

- **Universe = 170 symbols (32 NFL + 138 NCAA)** — corrected from 163/131 in
  four places.
- **$/win = $5.00 decoded** from the client's real NFL sheet
  (`ESV = OffField + $5.00 × E[wins]`, verified all 32 rows) — E1 → sign-off.
- **No mass-quote interface on tZERO** — order-based MM by necessity (T7 ✅).
- **Gateway has no outbound cancel/replace (35=F/G)** — the #1 prerequisite;
  build committed (Hasan). TIF = DAY/GTC/GTD only; limit-only; no default
  price bands (per-account collar exists in OMS spec, asks filed); resting
  orders survive disconnects; MM account mechanics = `UAAR`/`UEPR`/`UBT`.
- **Our-side throughput is a non-issue** (~460k orders/s/core measured);
  binding constraint = tZERO's per-account `MaxOrdRate`.
- Their independently-proposed MM params **converge with ours** (2-tick
  spread, 3-tick spacing, ~3–4 levels) — corroboration, logged as
  suggestions.

### 8 · New fact: share capacity

**5,000,000 shares available for longs AND 5,000,000 for shorts, per team**
(learned 21-07). Consequences: QA's 1,000-share short reserve is test config;
and the **λ denominator question** — skew is %-of-float, and 5M vs the
sheet's 875k changes the effective gain ~5.7×. Flagged 🔴 in parameters.

### 9 · Stood up the working process

[[market-maker/working-guide]] (mandatory reading order · ground rules ·
session loop) + `sessions/` with TEMPLATE + **CLAUDE.md rule**: any MM work
must read the guide first. This note is the first artifact of that process.

---

## What we learned (the distilled insights)

1. **The machine is simpler than its documents.** 80 pages of ceremony
   compress to: one pricing formula, one feedback loop, a handful of lookup
   tables, and ~22 numbers. The standards' value is the interface discipline
   (argument lists as law, determinism, replay), not the prose.
2. **The argument list is the law.** Every "undefined function" is a
   dependency allowlist + purity contract. This makes the system unusually
   testable and unusually AI-buildable.
3. **The spoken word outranks the written standard.** Twice now a call has
   descoped or corrected the docs (Ch5, capital, cadence). Hence
   decisions.md-wins and this session log.
4. **Two teams are converging independently on the same design** — platform's
   prototype params ≈ ours without coordination. Good sign for the design;
   also a warning that coordination (the 22-07 filter, N9) matters.
5. **The real risks are not the math:** tZERO rate limits, the SR probabilities
   feed, stale-quote exploitability, and the calendar.

## What went wrong / got stuck

- **The vault drifted a full day behind the platform team** — they'd made
  decisions (cadence, identity, seam) we learned about only by reading their
  doc. The sessions process exists because of this.
- **Symbol counts were wrong everywhere** (163/131 vs real 170/138) — the
  standards don't match the deployed universe; trust the venue.
- **CTS-001 §3 (the valuation math) was never delivered** — worked around via
  Edwin's formula + the sheet decode, but the PDF should still be requested.
- **Float ambiguity bit us twice** (875k sheet vs 5M capacity) — unresolved
  denominators are dangerous when a feedback gain depends on them.
- Momentary scare that the whole engagement had silently doubled in scope —
  resolved into the correct framing: it did grow (we build all three
  standards), but the growth is bounded and mostly arithmetic + integration.

## Decisions made *(all mirrored into [[market-maker/decisions]])*

20-07 batch (scope, formula, capital, mechanics, sessions, new build items) ·
22-07 batch (platform facts adopted, MM suggestions quarantined, 5M/5M
capacity, working process). Plus structural: custom component layout;
component named `market-maker`; decision-cycle defaults drafted as proposals.

## Questions opened / closed *(state in [[market-maker/open-questions]])*

- **Closed:** T7 (no mass-quote → order-based MM).
- **Reframed to 🟡:** E1 ($5.00 decoded, sign-off), E3 (NFL RP₀ sheet), T1
  (mechanism in hand, entitlement pending), T2 (venue config question).
- **Opened:** **E11 settlement definition** (the most important product
  question), **E12 NCAA secondary scope** (decides the load profile), N9
  (adopt-or-redesign each platform-doc MM suggestion), λ-denominator
  reconcile.

## Artifacts produced this session

| Artifact | Path |
|---|---|
| CTS-001 plain-English guide (md + html) | `vault/standards/CTS-001-plain-english-guide.{md,html}` |
| CTS-002 plain-English guide (md + html) | `vault/standards/CTS-002-plain-english-guide.{md,html}` |
| Interactive machine map (clickable equations) | `vault/standards/sdmm-machine.html` |
| Component hub + 7 systems docs | `vault/components/market-maker/` + `systems/` |
| Decision-cycle pseudocode + proposed defaults | `systems/decision-cycle-reference.md` |
| Working docs (decisions · open-questions · parameters · plan · glossary) | `vault/components/market-maker/` |
| Working guide + sessions process + CLAUDE.md rule | `working-guide.md` · `sessions/` · `CLAUDE.md` |
| 20-07 touchdown transcript in vault | `vault/meetings/20-07-2026-touchdown.md` |

**⚠ ALL of it is uncommitted** on `digest/touchdowns-13-17-jul` — branch + PR
is overdue and should happen before Thursday.

## Next

1. **Commit + PR everything** (before Thursday, so the team can read it).
2. **Thursday 23-07 deep-dive prep:** walk in with [[market-maker/parameters]]
   (every 🔴/🟡 row is a question), **E11 + E12 at the top**, the
   decision-cycle reference as the defaults-for-sign-off document.
3. **Start the from-scratch design pass** (N9 adopt-or-redesign calls + N7
   topology) so Thursday's answers land into a design, not a vacuum.
4. Keep chasing Phase-0 blockers: SR probabilities feed, tZERO QA MM account,
   gateway cancel-system build (Hasan).
