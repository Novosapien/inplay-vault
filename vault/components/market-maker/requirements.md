# Market Maker — Requirements

> **Component:** [[market-maker/market-maker]]
> **Purpose:** The normative list — what MUST be true for this machine to
> run in production. Not narrative (that is
> [[market-maker/decisions]]), not as-built (that is
> [[market-maker/build/index|build/]]), not numbers
> ([[market-maker/parameters]]). Each requirement carries a source, a
> status, and how it is verified.
> **Born:** 2026-08-09 (George: "we create our own requirements doc, and
> an addendum for anything we need to change").

**How to change this document.** Do not silently edit a requirement.
Add a dated entry to the **Addendum** at the top, then edit the
requirement in place and mark it ✎. The addendum is the audit trail; the
list below is always the current truth.

**Status:** ✅ met and verified · 🟡 met, unverified · 🔴 not met ·
⛔ blocked externally · ✎ changed (see addendum)

**Source:** `VENUE` = observed on the real venue (gospel) ·
`EDWIN` = his ruling · `GEORGE` = his ruling · `OURS` = our engineering
decision, recorded · `SPEC` = the v1.3 build spec.

---

## Addendum — changes to these requirements

### 2026-08-09 — the sell rule (first entry, from the live probe)

- **ADDED R-V07** (sellable = Pos − livS). Discovered by live probe;
  no vendor document states it. Makes R-Q08 (ask-side bound) a
  correctness requirement rather than an assumption.
- **ADDED R-V08** (no manual orders on the MM user id while the engine
  runs) after the engine adopted a hand-sent probe order.
- **WEAKENED R-L05** (DONE_FOR_DAY) from a venue fact to unverified:
  no `39=3` has ever been observed. See T14.
- **ADDED R-Q09** (do not cross the live book) after the engine swept
  stale asks for $50,366 while intending to rest.

---

## V · The venue contract

What tZERO requires of us. Everything here is `VENUE` unless noted —
these are gospel under the 22-07 filter and are not ours to change.

| # | Requirement | Source | Status | Verified by |
|---|---|---|---|---|
| R-V01 | Every new order carries the account (FIX tag 1) | VENUE | ✅ | live 07-08 |
| R-V02 | ClOrdIDs are unique per session, ≤ 20 chars, no leading zero, no dots. A repeat is duplicate-rejected forever | VENUE | ✅ | live 07-08 (the deadlock) |
| R-V03 | A redeploy must mint fresh ClOrdIDs — the venue remembers ids across our restarts | VENUE | ✅ | `MM_CONFIG_VERSION`, PR #7 |
| R-V04 | One in-flight request per order; a second is `REQUEST_IN_FLIGHT` | VENUE | ✅ | reconciler `[one-in-flight]` |
| R-V05 | Time in force is DAY/GTC/GTD only — **there is no IOC** | VENUE | ✅ | spec + live |
| R-V06 | Orders obey LmtPerc bands, which are **per-symbol**: passive ≤ 80–90% above the ask, aggressive ≤ 3–5% below the bid | VENUE | ✅ | live 08-07, 08-09 |
| R-V07 | **A side-2 sell may not exceed `Pos − livS`** (position minus quantity already committed to live resting sells). Over that the venue rejects the WHOLE order — it never part-fills and never opens a short | VENUE | ✅ ✎ | live probe 08-09 |
| R-V08 | **No manual order may use the MM's user id while the engine runs** — the engine admits unregistered acks as ACTIVE and adopts them. Probes use a different identity on the MM transport | OURS | ✅ ✎ | live 08-09 |
| R-V09 | The MM never sends side 5 (sell short) | EDWIN (E26) | 🟡 | by construction |
| R-V10 | The dead-man switch sweeps the book when heartbeats stop | VENUE | ✅ | drilled live 07-08 |
| R-V11 | Order rate stays within the account's `MaxOrdRate` | VENUE | 🔴 | not enforced in code — see B3 |

## L · Lifecycle

| # | Requirement | Source | Status | Verified by |
|---|---|---|---|---|
| R-L01 | An order at a still-wanted price is left alone — never topped up (rest-until-gone) | EDWIN (N10) | ✅ | test |
| R-L02 | A price move is ONE cancel-replace that adopts the new rank's drawn size | GEORGE (07-08h) | ✅ | PR #8, live 32→70% monotone |
| R-L03 | Instructions are post-first: submits, then replaces, then cancels | N12 | ✅ | test |
| R-L04 | No replace relies on keeping queue priority | SPEC §8.3 | ✅ | by construction |
| R-L05 | DONE_FOR_DAY is a distinct terminal state | SPEC/22-07 | 🟡 ✎ | **never observed — see T14** |
| R-L06 | An in-flight replace occupies its destination price — no double-post | OURS | ✅ | PR #9, zero doubles live |
| R-L07 | Entering Suspended publishes an empty book and cancels what is cancellable | SPEC §6.4 | ✅ | test |
| R-L08 | §5.9 replenishment — **undecided** | EDWIN (E17) | ⛔ | open question |

## Q · Quoting

| # | Requirement | Source | Status | Verified by |
|---|---|---|---|---|
| R-Q01 | A book is never left without a resting side | GEORGE | ✅ | live 07-08 |
| R-Q02 | Spreads follow the state tiers (Stable/Active/Defensive) | SPEC §5.2 | 🟡 | values are Edwin's, E31 |
| R-Q03 | The shape redraws only on a §5.8-material change with an expired dwell — never on the timer alone | OURS (N26) | ✅ | test |
| R-Q04 | Prices are capped at min(MEV, venue cap $127.50) | VENUE | ✅ | built 06-08d |
| R-Q05 | The ladder is non-increasing from the inside outward | GEORGE | 🟡 | 70% live; gap is E17 |
| R-Q06 | Quantities are drawn per rank, seeded and reproducible | OURS | ✅ | test |
| R-Q07 | Skew distributes inventory across the ladder | SPEC Ch 4 | 🟡 | N20 open |
| R-Q08 | **The ask ladder respects `Pos − livS`** — it may not offer more than it holds minus what it already offers | VENUE (R-V07) | 🔴 ✎ | **not built** — sizes the ask side, couples to E27 |
| R-Q09 | **A published order must not be marketable against the live book** — the MM rests, it does not take | OURS | 🔴 ✎ | **not built** — swept $50,366 on 08-09 |

## D · Determinism and recovery

| # | Requirement | Source | Status | Verified by |
|---|---|---|---|---|
| R-D01 | Seeded randomness only — no wall clocks in decision paths | OURS | ✅ | test |
| R-D02 | Event-sourced: state derives from the journal, replay is exact | OURS | ✅ | equality proof on a real game |
| R-D03 | Checkpoint resume ≡ never-stopped ≡ full replay | SPEC §10.3 | ✅ | proof 06-08d; re-run on live data = C2 |
| R-D04 | Duplicate events are idempotent; the dedup window covers the redelivery bound | SPEC §12.3 | ✅ | built 06-08d |
| R-D05 | A boot reconciles the venue's truth against the record | SPEC §3.1.4 | 🔴 | healer unbuilt — C1 |
| R-D06 | Every deploy bumps the config version and takes a fresh journal (until R-D05 exists) | OURS | ✅ | operational rule |

## R · Risk and safety

| # | Requirement | Source | Status | Verified by |
|---|---|---|---|---|
| R-R01 | One security's fault suspends only that book | GEORGE | ✅ | built 06-08d |
| R-R02 | Untranslatable inbound is poison — counted and skipped; deliberate halts stay fatal | OURS | ✅ | PR #6, live |
| R-R03 | A persistently rejected level backs off deterministically | OURS | 🔴 | **not built** — C4, top of next |
| R-R04 | Exposure counts pending states (PBE/PSE) including Partially Filled | SPEC §4.4 | ✅ | test |
| R-R05 | A kill switch takes the whole machine down on demand | OURS | 🟡 | dead-man exists; operator surface is N29 |
| R-R06 | Stale inputs suspend the affected book | SPEC §6.4 | 🟡 | built; C3 unverified live |

## S · SNT-1 (the noise taker)

| # | Requirement | Source | Status | Verified by |
|---|---|---|---|---|
| R-S01 | Runs on its own account with its own tape identity (IPLP) | OURS/E33 | ⛔ | account not assigned |
| R-S02 | Flow is uninformative — 50/50 direction, Poisson arrivals | EDWIN | ✅ | test |
| R-S03 | Taker only — never rests deliberately | EDWIN | 🟡 | the IOC substitute can rest briefly |
| R-S04 | Impact is capped at 3 ticks through the touch | EDWIN | ✅ | test |
| R-S05 | A per-book daily loss budget silences the book when spent | EDWIN | ✅ | test |
| R-S06 | Position, basis and budget survive a restart | EDWIN | ✅ | journal replay test |
| R-S07 | **Sells respect `Pos − livS`** | VENUE (R-V07) | 🔴 ✎ | **not built** — mandatory |
| R-S08 | Runs from a seeded float and never goes short | OURS | 🔴 | baseline change not built |
| R-S09 | Rejects are first-class — a rejecting book goes quiet | OURS | ✅ | test |

## X · External gates (not ours to satisfy)

| # | Gate | Owner | Blocks |
|---|---|---|---|
| X-01 | The LmtPerc reference on empty books | Hasan | the other 163 books (B3) |
| X-02 | Opening position at IPO | Edwin (E27) | day-one book, and now the ask-side size (R-Q08) |
| X-03 | Quote lifecycle — top-up vs rest-until-gone | Edwin (E17) | R-L08, R-Q05 |
| X-04 | Two house accounts as counterparties | Troy / legal (E33, T13) | SNT-1 shipping |
| X-05 | Session roll — does DAY ever expire? | Rob (T14) | R-L05, E36 |
| X-06 | Live-mode gates: SR allocation, MM account, file transport | S1/S7/T1/N19 | go-live |
