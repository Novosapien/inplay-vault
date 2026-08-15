---
description: "PROPOSAL, not applied — a draft addendum entry adding manual-order and observability requirements to the market taker's go-live list, awaiting George's approval"
---

# PROPOSAL — taker requirements addendum for manual orders + the state publisher

> ⚠ **THIS IS NOT APPLIED.** [[market-maker/market-taker-requirements]] is
> unchanged. That document's own rule is that it changes only through a
> dated addendum entry, and a builder should not amend a normative go-live
> list mid-task. This is the draft, written while the reasoning was fresh,
> **awaiting George's approval**.
>
> **Who:** Claude (`engine` stream) · **Date drafted:** 2026-08-12 ·
> **Decided by:** the team lead, who asked for it as a proposal rather
> than an edit
> **Source:** the R2/R3 build —
> [[market-maker/sessions/2026-08-12-b-engine-state-publishers-manual-orders]]
> · [[market-maker/decisions]] 2026-08-12 and 2026-08-12b

## Why an addendum is arguably owed

The taker gained a capability it did not have when the requirements list
was written on 09-08: **a human can now place, cancel and replace orders
through it**. The list is "what MUST be true before it runs against real
books", and manual trading is a second way for the taker to reach the
venue. Everything below is either already built and tested or already
ruled — none of it is new design. The question for George is only whether
these belong in the normative list at all, or whether they stay in
`decisions.md` and the spec.

**The honest argument against adding them:** manual orders are an OPS
surface, not taker behaviour, and the list is about the algo. If George
takes that view, nothing here is lost — the properties are tested and
recorded either way.

## Proposed addendum entry

> **2026-08-12 — manual orders and the state publisher (spec R2/R3).**
> The taker gains an operator-driven order path through its control
> channel and a state snapshot on the bus. New rows T-O11, T-M07, T-S08,
> T-S09, T-R05, T-R06; T-R03 tightened.

## Proposed new rows

### O · Order behaviour

| # | Requirement | Source | Status | Notes |
|---|---|---|---|---|
| T-O11 | A manual sell is an ORDINARY sell (FIX side 2), never a short | OURS | ✅ | an operator asking to sell has asked to reduce a holding; a short opened by inference is a position nobody decided to take. Over the holding, the venue rejects whole (T-O07) and the operator sees why |

### M · Money and limits

| # | Requirement | Source | Status | Notes |
|---|---|---|---|---|
| T-M07 | Manual orders are guarded before they reach the venue, and the guards are the ones an operator is shown | GEORGE (Hasan 12-08) | ✅ | engine-enforced: 10,000 shares/order ✅ · ±20% collar ✅ · $500k notional 🟡. Env-tunable, and the panel MIRRORS the live values from `snt.state.guards` — never hardcoded, or a tuned guard would silently disagree with the screen |
| T-M08 | The collar never blocks an order it cannot measure | OURS | ✅ | reference falls back book mid → last trade (age-bounded, 🟡 1 h) → skip. A crossed book counts as no book. Skipping disables the COLLAR only; qty and notional still bind and the ack says `collar_skipped`. The IPO place-while-halted case usually has no book at all |

### S · State, recovery, determinism

| # | Requirement | Source | Status | Notes |
|---|---|---|---|---|
| T-S08 | Manual fills move position, holding and float drift, but NEVER the session-loss budget | GEORGE (spec 12-08) | ✅ | the float invariant (float = env float + journalled drift) must keep holding or T-S05 halts the book. `session_loss` stays a pure meter of the ALGO's noise cost — an operator buying 600,000 IPO shares by hand would otherwise spend the day's budget and silence a bot that had done nothing. The exemption is carried on the journal record, so replay reapplies it |
| T-S09 | A resting manual order survives a restart, and a resent command never places a second order | OURS (spec R3) | ✅ | placed-minus-ended is re-adopted as manual at boot (not cancelled, not orphaned); every reply is journaled so a duplicate `ref` re-publishes the original answer with the same ClOrdID. Retention is the journal directory, which the ops rules rotate per deploy |

### R · Safety

| # | Requirement | Source | Status | Notes |
|---|---|---|---|---|
| T-R05 | The strategy loop never cancels or reprices a manual order — and the kill switch always does | OURS | ✅ | manual orders are exempt from the IOC cancel timer (they are DAY orders placed to rest) but NOT from halt or the T-S05 reconcile halt. A kill switch that spared an order would not be a kill switch |
| T-R06 | The maker cannot be traded by hand | GEORGE (12-08) | ✅ | structural, not a check: no maker control subject exists on the wire and the command carries no account field. There is nothing to aim at the maker |

### Tightened

| # | Change | Why |
|---|---|---|
| T-R03 | "Every action is logged and auditable" — 🟡 → 🟡, note extended: manual orders now journal their send, their ref, their ClOrdID, their fills and their terminal state, and every reply is journaled. Ops logging for the ALGO's own actions is still thin, which is why the row does not go ✅ | the manual path is the one a regulator would ask about first (E33/T13), and it is now the best-audited path in the taker — worth recording that the gap is elsewhere |

## What this proposal deliberately does NOT claim

- **It does not claim compliance clearance.** T-C01/T-C02 are unchanged
  and still ⛔. Manual panel trading of the taker account rides the same
  E32/E33/T13 round (decisions 12-08); building it is not shipping it.
- **It does not add an operator-identity row.** N35 is ruled: v1 flags
  the order `manual` and attaches no name. A requirement row would
  misrepresent that as an open obligation.
- **It does not touch T-O06/T-O08.** Those govern the ALGO's sells and
  shorts and are unaffected by an operator's order.
