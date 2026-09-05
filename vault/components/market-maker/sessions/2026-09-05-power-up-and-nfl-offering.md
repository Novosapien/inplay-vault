---
description: "The 5 Sep power-up after the 1 Sep shutdown, the NFL offering rested while the NCAA maker runs, and the venue's price-band anchor trap found on the way"
---

# 2026-09-05 — Power-up, and the NFL offering rested beside a live maker

> **Who:** Claude session (inplay-vault), George
> **Type:** ops / build
> **Refs:** Hasan's `POWER_DOWN_RUNBOOK.html` + `FINAL_STATE.md` (local-only) ·
> `inplay-market-maker@feat/ipo-nfl-offering` (`98eeaea`, `4545ac6`) ·
> gateway per-bot dead-man `4b2d723` · [[market-maker/reference/ipo-seeding-runbook]]
> **⚠ Ends with:** the NFL offering RESTING (32 × 900,000, GTD `2026-09-07T02:00:00Z`),
> mm-1 quoting 138 NCAA books on `supervised49`/**CFG-0047**, snt-1 OFF.

## What we did

- **Power-up (00:01–00:12Z).** Hasan's runbook, in order: both Cloud SQL
  primaries → NATS and Centrifugo MIGs → the 7 Cloud Run services at their
  exact pre-shutdown values → 15 alert policies → 8 scheduler jobs → both FIX
  gateways. Every value matched `pre-shutdown-state-2026-09-01.txt`. Manual
  SQL backups of both primaries taken (none had run since 30-08).
- **The MM VM.** `mm-1` was `enabled` and auto-started on the 1 Sep journal.
  Stopped after 14 s, sent nothing. `snt-1` runs on the same VM (not the Go
  VM) and booted `state=AUTO`. Both stopped and `disabled`; George: taker off
  for Saturday.
- **The venue before anything:** `POST /md/probe` on all 32 NFL books →
  `entries=0`. MM gateway `open_orders 0`.
- **Prices read from the trading DB** (`assets.ipo_ask_price`, via a read-only
  `python -c` on the `inplay-trading-migrate` job). All 32 NFL prices differ
  from the 20-08 price file. `float_remaining` 900,000 on every NFL row.
- **The offering, with the maker STOPPED, under a distinct identity**
  (`userId ipo-nfl-user`, `botId ipo-nfl`, account 1797733477):
  1. 32 × UEPR `Qto=0` → 32 × `UEPRa`.
  2. 32 one-share reads at half price → every `9383=0`.
  3. 32 × UEPR `Qto=900000` → 32 × `UEPRa`.
  4. 32 asks at the IPO price → **32 rejects** (the anchor trap, below).
  5. Recovery on IPTCEAGL, then the other 31: a 1-share SELL hop at 0.9 × IPO
     (accepted, `9383=900000` — the position check), ~4 min for the anchor,
     cancel the hop, rest the ask within 3 s → **32 × `39=0`, leaves 900,000,
     `9383=900000`**. 28,800,000 shares, $1,836,063,000 notional.
- **The maker (00:49Z).** Fresh journal `supervised49`, prior `supervised48`,
  **CFG-0047**, heal on, `MM_SECURITIES` = 138 NCAA. 138/138 quoting in
  90 s, 714 orders, 0 NFL symbols, 0 adoptions, 0 unknown-order rejects. The
  32 `ipo-nfl` asks untouched. Unit left `disabled` — manual starts only.
- **Scripts:** `set_position.py` (UEPR, `--only` required, NCAA refused),
  `read_positions.py` (`--side buy|sell`, `--parse`), `cancel_reads.py`,
  README §5 with the recipe and the trap.

## What we learned

- **Three mechanics make an offering safe beside a running maker.** Adoption
  is by `userId`, which the gateway uses only for routing (R-V08,
  `oe_adapter.go`). The dead-man is per `botId`; a bot with no heartbeat arms
  only on a gateway restart. `cancel_all` is global. So: distinct userId,
  distinct botId, no `cancel_all`, no gateway restart for the window.
- **⭐ The anchor trap.** On an empty book the venue's price-band anchor
  follows the last resting order, per side, with a refresh measured at
  ≤ 3.5 min. The half-price reads set the sell-side anchor; every ask at the
  IPO price was refused `Passive SELL … more than 85 percent ABOVE the
  ASK(38.90)`. The buy side is judged against the stored 20-08 ask (72.88):
  a bid near the IPO price is *Aggressive BUY … 3 percent ABOVE the ASK*. A
  1-share **passive SELL** inside the band moves the sell-side anchor.
- **A resting hop counts against sellable.** `sellable = Pos − livS`; with a
  1-share sell live the 900,000 ask is refused `You can SELL at most 899999`.
  Cancel the hop, then rest — the anchor lags long enough.
- **UEPRa carries no 9383.** The position reads back only on an order's
  execution report. The hop's accept is the cheapest read.
- **`Qto=0` on a symbol seeded by UPT gives `Qt=0`.** The 20-08 activity did
  not survive; `Qto = 900,000 − 0` was the whole set.
- The venue never queues the asks' visibility: George saw the 32 read bids
  within a minute. Reads before a window, never during — the runbook was right.

## What went wrong / got stuck

- The offering took four attempts (IPO-01 rejected ×32, IPO-02 rejected,
  IPO-03 oversell, IPO-04 oversell after a bad cancel payload, IPO-05 live).
  Each burned a run tag; none rested twice.
- `mm-1` and `snt-1` were both `enabled`. A VM start is not a ceremony; the
  plan said to check `is-enabled` and it was needed.
- **A secret reached the transcript.** The maker's boot line logs
  `nats=nats://market-maker:<token>@10.0.2.2:4222`; a journal grep pulled it.
  It was already in the VM journal. Rotate `inplay-nats-mm-token` after the
  window and redact the boot line (**N79**).
- `set -e` plus `systemctl is-enabled` (exit 1 on "disabled") aborted the
  first start attempt silently. Caught on the next check.

## Decisions made *(mirror into [[market-maker/decisions]])*

- ✅ **2026-09-05a — an offering may rest beside a running maker** under a
  distinct `userId` and `botId`, never `cancel_all`, no gateway restart.
- ✅ **2026-09-05b — the anchor hop is the way to rest an offering on an
  empty book** until tZERO sets an IPO Reference Price for us (T-item).
- ✅ **2026-09-05c — `mm-1` and `snt-1` stay `disabled`.** Manual starts only.
- ✅ **2026-09-05d — the taker is OFF for Saturday 6 Sep** (George).
- ✅ **2026-09-05e — CFG-0047 / `supervised49`** is the live maker.

## Questions opened / closed *(mirror into [[market-maker/open-questions]])*

- **Opened T — tZERO IPO Reference Price.** Rob (29-07) said the OMS can set
  one via the Previous Close. Ask for it before the next offering.
- **Opened N77 — `snt-1` booted `AUTO`.** The 22-08 reconcile halt: resolved
  after 29-08, or not persisted across a restart?
- **Opened N78 — GTD across 00:01 ET.** Unproven. The 32 asks answer it at
  05:05 BST 6 Sep: `GET /orders/mm` → 32 rows under `ipo-nfl`.
- **Opened N79 — the maker's boot line prints the NATS token.**
- **Closed §6.2 of the runbook (N51)** — `assets.ipo_ask_price` read; it is
  the price the venue asks now carry.

## Next

- **05:05 BST 6 Sep:** the N78 check. If the asks are gone, re-rest from the
  ledger with a new run tag, hop first.
- Sunday 22:00 ET: confirm the GTD expiry cleared the 32; `cancel_orders.py`
  as the belt. Then the second power-down in the plan's order (offering gone →
  `mm-1` stop → dead-man → `cancel_all` → SQL backup → Hasan's runbook).
- Rotate `inplay-nats-mm-token`; redact the maker's boot line.
- Merge `feat/ipo-nfl-offering`; the VM worktree `~/mm-ipo` carries it.
