---
description: "The full-book seed: 173 position transfers (163 production + ten .TEST), all UPTa-verified — the MM account now holds 100k of every one of the 180 symbols"
---

# 2026-08-11 (late) — the full-book seed: 180 symbols, 173 transfers, zero rejects

> **Type:** live ops. Claude, continuing the handover's ruled task 1.
> **Continues:** [[market-maker/sessions/2026-08-11-taker-cutover]] (same
> working session — the taker cutover came first, then this).
> **The record:** [[market-maker/reference/position-transfer-ledger]]
> 2026-08-11 section — every ClOrdID, symbol, qty, cost, reply.

## What we did

1. **Built the seed plan.** The full symbol list is the gateway's
   180-symbol config (`inplay-fix-gateway-go`
   `internal/config/symbols.go`): the 170-ticker universe
   (`mm/universe.py`) + ten `.TEST` twins. Minus the seven seeded
   08-07 → **173 transfers**, 100,000 shares each, basis = the
   `Listed IPO` column of `reference/ipo-prices-170.csv` (a `.TEST`
   symbol carries its production twin's price). Total notional $877M.
2. **Joined names carefully.** The CSV uses short NCAA names
   ("Ohio State"), the universe uses full mascot names ("Ohio State
   Buckeyes"). Exact-first + explicit specials ("Miami Florida" →
   Hurricanes, "UL Monroe" → Louisiana Monroe Warhawks, "Florida
   International" → FIU Panthers, "Sam Houston State" → Bearkats,
   "North Carolina State" → NC State, "Southern Mississippi" →
   Southern Miss) + longest-name-first prefix matching, asserted as a
   170/170 bijection and eyeballed before use.
3. **Canary, then bulk.** One transfer (IPTCRAVE) sent alone: HTTP 202
   returns the T-prefix ClOrdID; the UPT/UPTa pair confirmed in the
   gateway journal (~35 s behind — the gateway paces UPTs onto the OE
   session behind live traffic). Then the remaining 172, sequential,
   0.3 s apart, halt-on-any-error, every response logged
   (`~/seed-log-20260811.jsonl` on the gateway VM).
4. **Verified one-for-one.** 173/173 `UPTa` replies joined by ClOrdID
   against the submissions — symbol, qty and cost all echo exactly.
   Zero `UPTx`. The ledger carries all 173 rows.

## What we learned

- ⭐ **The ten `.TEST` symbols are live at the OMS** — every one
  accepted a transfer with a `UPTa`. And the Texans test code is
  **`IPTCTEXS.TEST`** (matching the production ticker), not the
  `TEXA` guess — [[market-maker/test-symbols]] corrected, its open
  items 1 and 2 closed.
- `POST /position-transfer` returns HTTP 202 + the ClOrdID
  immediately; the venue reply only ever lands in the gateway log.
  Verification is a journal join, not a response check.
- The 08-07 and 08-11 seeds price from DIFFERENT sheets (Edwin's
  IPO sheet vs `ipo-prices-170.csv` — e.g. BILL $74.51 vs $77.27).
  The seven keep their 08-07 basis; flagged in the ledger.

## What went wrong / got stuck

- One local parse bug (a symbol-regex that clipped `IPTCCH49`) —
  caught by the bijection assert, fixed by joining on ClOrdID instead.
  No wire impact.

## Decisions made

- None new — executed George's ruled task 1 (the seeding half).
  Quantity (100k) and the basis source follow the handover + the
  08-07 convention.

## Questions opened/closed

- Closed: test-symbols items 1 (the four codes) and 2 (provisioning) —
  by the gateway config + the venue's own UPTa acks.
- Still open and now LOAD-BEARING: test-symbols item 5 / the LmtPerc
  empty-book question — the 174 newly seeded books have positions but
  EMPTY books ("No price available" rejects everything). The full-book
  run IS the planned experiment on exactly this.

## Next

The rest of ruled task 1: build the full supervised-inputs file from
`reference/ipo-prices-170.csv` (180 books incl. `.TEST`), then restart
the engine as **supervised13** (CFG bump + fresh journal dir) on the
full book — the B3 load test + the LmtPerc empty-book experiment + the
N31 fsync measurement in one. ⚠ The restart stops the currently
validated joint maker+taker run — confirm the timing with George/Hasan
before pulling supervised12.
