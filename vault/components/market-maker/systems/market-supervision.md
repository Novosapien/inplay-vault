# Market Supervision

> **Component:** [[market-maker/market-maker]]
> **Standard:** [[standards/CTS-002-market-operations-standard|CTS-002]] (orderly-markets requirements)
> **Status:** Policy TBD with T0 — mechanics exist on T0's side
> **One-liner:** The orderly-markets function: price bands, halts, and trade busting. Deliberately separate from the quoting engine — the MM is a counterparty and cannot be the judge of its own trades.

---

## Purpose

Keep prints sane and users trusting the market. Edwin: *"if everyone got
banged out on these market orders, you'd lose market participation really,
really quickly."* Regulatory framing: the exchange must maintain orderly
markets.

## The Three Tools (escalating)

| Tool | What it is | When |
|---|---|---|
| **Price band** | A corridor around the Reference Price (~±30%, exact number TBD). Orders priced outside it rejected at entry, and/or executions outside it disallowed | Continuous, preventive |
| **Halt** | Stop matching for one team (or all). Quotes go defensive/pulled; user orders queue or reject | Feed dead, valuation frozen, extreme volatility, operational failure |
| **Trade bust** | An already-executed trade at a clearly-wrong price is declared void; both sides' positions and cash reversed | Rare, after-the-fact — e.g. a crossing order filled at 85 on a 6–7 market |

Prevention ordering: tight order validation + entry bands should make busts a
rare last resort.

## Who Can Do What (clarified 21-07)

| Role | Can | Cannot |
|---|---|---|
| Participant (incl. our MM) | Cancel its own *unfilled* orders | Touch anyone else's orders; undo any *executed* trade — including its own |
| Venue (T0) | Void an executed trade — owns the book + trade record | Decide policy alone |
| Exchange operator (InPlay + us) | Decide *when* a trade qualifies for busting per agreed policy; instruct T0 | Reach into the book directly |

**Busting is not a market-maker power.** It's an operator + venue action:
Edwin — "as the exchange **or with T0** we have the ability to bust a trade or
say the trade didn't happen." Mechanically the bust is executed *by T0* and
arrives as an execution report reversing the fill for both counterparties —
our [[architecture/integrations/t0|T0 FIX docs]] already cover this
(`ExecType=H`, "Execution Busted", with position/P&L recalculation). The
plumbing exists; the policy and trigger don't yet.

## Why Separate From the SDMM

The quoting engine is a market participant — counterparty to most trades. It
cannot supervise executions it profited from (equal-access principle). So
supervision is its own function with read access to *all* executions, not just
the MM's.

## Build Shape (v1 proposal)

1. **Automated detector:** every execution checked against the band vs the RP
   at execution time → out-of-band fills flagged instantly.
2. **Human decision:** flag surfaces in the [[market-maker/systems/mm-ops-ui|MM Ops UI]]
   (Kevin) → bust triggered through the agreed T0 procedure.
3. **Halt control:** manual per-team halt/resume from the same UI, plus
   automatic defensive quoting via the market-state layer.

**Key question for the Tue/Thu T0 calls:** can T0 enforce bands natively in
the matching engine (reject out-of-band executions at source)? If yes, busts
become an edge case and the detector is mostly logging.

## Open Items

Tracked in [[market-maker/open-questions]]: band width (30%?), bust procedure
+ SLA with T0, halt semantics (who/what/how fast), native band enforcement,
whether band applies at order entry or execution or both.
