# Position-Transfer Ledger — account 1797733477

> **Purpose:** the endpoint is one-way and NOT idempotent, and the venue
> has no position read-back — so this ledger is the only complete record
> of what was seeded (Hasan's rule, trading-ops guide §7). Every
> transfer, ever, goes here. A retry after a timeout is FORBIDDEN until
> the gateway journal has been checked against this table.

## 2026-08-07 — the supervised-test seed (George's direction; run by Claude)

100,000 shares per ticker, cost basis at Edwin's IPO-sheet prices.
All seven accepted (`UPTa`, gateway journal 16:57:28–16:57:34 UTC, FIX
seq 3126–3132). Verified behaviourally: a side-2 sell on IPTCEAGL —
"not long"-rejected the day before — was ACCEPTED then cancelled
(MMSEEDVER1).

| ClOrdID | Symbol | txfrQty | txfrCost | Basis | Reply |
|---|---|---|---|---|---|
| Thl4l1s77qa | IPTCEAGL | +100,000 | $7,779,000 | $77.79 | UPTa |
| Thl4l1st6a4 | IPTCPATR | +100,000 | $7,979,000 | $79.79 | UPTa |
| Thl4l1tf32v | IPTCBILL | +100,000 | $7,451,000 | $74.51 | UPTa |
| Thl4l1u0ytj | IPTCGIAN | +100,000 | $6,110,000 | $61.10 | UPTa |
| Thl4l1umuyx | IPTCCOWB | +100,000 | $7,618,000 | $76.18 | UPTa |
| Thl4l1v8rii | IPTCSTEE | +100,000 | $6,634,000 | $66.34 | UPTa |
| Thl4l1vunmo | IPTCJETS | +100,000 | $4,543,000 | $45.43 | UPTa |

**Running position per this ledger:** 100,000 of each of the seven.
(Plus the two 07-08 wash-probe fills on IPTCEAGL, +100/−100 = net 0.)
