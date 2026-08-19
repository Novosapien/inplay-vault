---
description: "Building the IPO test rig, and the afternoon that overturned three recorded tZERO facts and destroyed 99,663 maker shares"
---

# 2026-08-19 — the IPO test rig: scripts, a gateway read path, a panel page

> **Who:** George + Claude
> **Type:** build
> **Refs:** `inplay-fix-gateway-go` **PR #20** (deployed) ·
> `inplay-admin-panel-trading` **PR #32** ·
> `inplay-market-maker/scripts/ipo/` ·
> [[market-maker/build-deploy-log]] · [[ipo-module/ipo-module]]

## What we did

George is testing the IPO process. The shape he set: the **maker account** holds
the float and rests sell orders at the listed price, test users subscribe through
the matching engine, and Edwin buys on behalf of the taker from the admin panel.

Built three things.

**1 · The venue scripts** (`inplay-market-maker/scripts/ipo/`)

| script | what it does |
|---|---|
| `prices.py` | builds the ticker → price file from the vault model or from `teams.ts` |
| `allocate.py` | one 35=UPT position transfer per team, through the gateway's ops endpoint |
| `rest_orders.py` | one limit sell per team on `gateway.orders.mm.new`, side 2, TIF DAY |
| `cancel_orders.py` | precise cancels from the run ledger, or one global `cancel_all` |

Quantities come from `mm.universe` (900,000 NFL · 1,000,000 NCAA), never a flag.
Every step keeps a JSONL ledger and resumes off the **intent**, not the success —
see the UPT properties below.

**2 · `GET /positions/house` on the gateway** — PR #20, **deployed 19-08 ~12:20Z**.
Aggregates the tracker's MM orders per bot and symbol: ordered, sold, resting,
notional, avg price, and the venue's own tag 9383 figure. `OrderTracker.GetMM`
includes terminal orders; `SetPosition` stores 9383/9384, which the gateway used
to publish and then discard.

**3 · The IPO book page** in the admin panel — PR #32, not deployed. A proxy
passthrough carrying `X-Ops-Key`, an admin-only API route, and the page.

## What we learned

### ⭐ The IPO already has an execution path, and it is not the venue

`inplay-trading-service/src/app/services/ipo_engine.py` is a complete float
manager: `execute_ipo_buy` decrements a sharded float, debits the wallet, upserts
the holding and writes a fill marked `settlement_status="simulated"`. It never
calls the venue. `routers/trading.py:879` refuses venue placement unless the phase
is `LIVE`.

⚠ **The first reading of this was wrong** — it looked like a conflict with
George's plan. It is not. The two legs are independent: app users buy through the
internal engine, and the taker's manual orders reach tZERO through
panel → proxy → NATS → taker engine → gateway. The trading service is not in that
path, so the phase gate cannot see it. The plan stands.

`services/market_phase.py` also carries **IPO Draft Business Requirements v3
(1 Aug 2026)** — a document newer than the v2 the vault treats as gospel. Its
windows: NCAA 22 Aug 13:00 ET → 26 Aug 22:00 ET, secondary 27 Aug 09:30; NFL
5 Sep 13:00 → 6 Sep 22:00, secondary 7 Sep 09:30.

### ⚠⚠ The dead-man switch will cancel the whole offering

`internal/adapter/deadman.go` sweeps every resting MM order when the maker
heartbeat stops. It arms two ways, and **both can happen by accident inside an
offering window**:

- a heartbeat is seen — start the maker engine once and it arms; stop it and the
  sweep runs `MM_DEADMAN_TIMEOUT_MS` later (10s)
- the gateway **restarts** and rehydrates the orders — `ArmForBoot` sweeps after
  `MM_DEADMAN_BOOT_GRACE_MS` (30s)

There is no off flag: `DeadManTimeout <= 0` falls back to 10s in `oe_adapter.go`.
Before a window, raise both env values past the window length and freeze gateway
deploys.

### ⚠ 35=UPT is one-way, and not idempotent

From `server.go`'s own probe record: UPT applies a **signed delta**, positive
transfers apply, and **negative transfers are accepted (UPTa) but never move the
position** — tried with and without ConfirmTyp, measured 2026-08-05. The reply
goes to the gateway's FIX log, never to the caller, so a timeout proves nothing.
**There is no scripted reversal today.** The absolute-set message is UEPR
(`POST /position`), which drew no reply on 28-07 and was read as disabled — but
tZERO switched that family on later the same day, which is what **E27** already
says to re-probe.

### ⭐ The venue only reports a position ON A FILL

Tag 9383 rides the execution report. This FIX session has no Request For
Positions, so before the first trade the venue has told us nothing. The endpoint
returns `pos_size: null` and the page renders a dash — never a zero.

### ⚠ Live coordinates contradict two recorded facts

Read off the gateway's own book, 19-08:

| | recorded | live |
|---|---|---|
| maker bot id | `sdmm-1` (env example) | **`mm-1`** |
| accounts | "one wallet, one MPID, one inventory" (decisions 03-08) | maker **1797733477** · taker **4963224393** — **separate** |

## What went wrong / got stuck

- ⚠ **A secret was printed into the session.** A read-only pre-deploy check
  `cat`-ed `/opt/fix-gateway/.env` with a redaction pattern that did not match,
  so `OPS_API_KEY` reached the terminal transcript. Nothing was written to a
  file, a commit or a PR. **Rotate it.**
- **The build-deploy-log was stale and nearly caused a bad deploy.** It said the
  running gateway was `main@a41e540` (15-08). The VM was actually running a
  binary deployed **19-08 00:03Z**, and `/health` reports `role: mono` — a field
  that only exists in PR #19, merged 20 minutes earlier. Had the log been
  believed, the deploy would have looked like it shipped 30 commits of
  passengers. It shipped one endpoint.
- The maker and taker do **not** run on the gateway VM. Only
  `fix-gateway.service` is there, so their state could not be verified from that
  host.
- `TestEndToEnd` in the gateway's `e2e/` fails on `main` — pre-existing, unrelated.

## Decisions made *(mirror into [[market-maker/decisions]])*

- ✅ **The maker account sells the primary for this test.** A deliberate
  substitution for the broker-dealer MPID (T16, not stood up). It reverses the
  31-07 "the market maker is not going to open up and sell" for the TEST only.
- ✅ **900,000 NFL · 1,000,000 NCAA** — George reaffirmed after the 03-08 record
  (1M both) was flagged. The built systems already agree: `dictionary.py:96` and
  the trading service's `FLOAT_BY_LEAGUE`, both sourced to **v3 §1.2/§3.1**.
- ✅ **No rounds.** One open window, resting sell orders, users subscribe.
- ✅ **The matching engine, not the 23-07 direct-mint path**, for the venue leg.
- ✅ **The IPO panel view is a NEW PAGE** (`/ipo`), admin-only.

## Questions opened / closed *(mirror into [[market-maker/open-questions]])*

- ➕ **E27 moves.** "How does the market maker learn its opening position" now has
  a read path for the venue side: `GET /positions/house`. The publisher for an
  `IPO_ALLOCATION` event is still missing.
- 🔴 **NEW — are the maker and taker on one account or two?** Live says two. The
  03-08 decision says one. Whichever is right, 166.8 M shares get seeded into one
  of them.
- 🔴 **NEW — is there any reversal for a position transfer?** Re-probe UEPR. One
  message answers it.
- 🔴 **Which price set does the app actually charge?** The vault model and
  `teams.ts` agree on 137 of 170 tickers and differ on 33, by up to $21.59.
  `assets.ipo_ask_price` in the trading-service database is the truth and was not
  read this session.

## Next

- Probe UEPR (`POST /position`). It decides whether the allocation is reversible,
  and therefore whether the first run may use real books or must use the ten
  `.TEST` twins.


---

# Addendum — the afternoon: what the venue actually does

> Hasan measured tZERO's position mechanics against the session wire log
> 17:20–17:42 UTC. **Three things this vault recorded were wrong**, and one
> probe from this session turns out to have destroyed real stock.
> Decisions: [[market-maker/decisions]] 2026-08-19e.

## ⚠⚠ The incident — a "no-op" probe cost the maker 99,663 shares

At 16:24:35Z I sent `POST /position {"account":"1797733477",
"symbol":"IPTCJAGU.TEST","qto":0,"eto":0}` to test whether UEPR was alive. The
route's own documentation calls that a no-op — but the full sentence is *"a
no-op — qto=0, eto=0 **on a symbol the account has never traded**"*. The maker
had traded it and held **101,665 shares**. `Qto` is an absolute opening
quantity, so the probe set the opening balance to zero: `9383` read **2,002** at
17:40Z. **99,663 shares gone.**

Trading did not do it — exactly one execution report exists on that
account+symbol in the window, and it is the probe order itself; the MM had been
dark since its dead-man latched at 13:35.

⭐ **What actually went wrong, and it is not "UEPR is dangerous":**

1. The no-op was **conditional** and I treated the condition as scenery.
2. I picked `IPTCJAGU.TEST` as "least likely to matter" — a guess standing in
   for a check.
3. I had spent the previous hour concluding **a position could not be read**,
   and acted on an account whose contents I had just declared unknowable. The
   right move at that moment was to stop, not to probe.
4. The read path existed the whole time.

## What was wrong in the record

| The record said | Measured 19-08 |
|---|---|
| UEPR is not enabled (28-07, and re-probed by me the same afternoon) | **`UEPRa` in 8 ms.** Every earlier probe sent `Qto=0` on a **zero-opening** account — a genuine no-op, so silence proved nothing either way |
| There is no undo for a seeded position | **UEPR is the undo.** `9381 Qto` is ABSOLUTE (four sends, four exact hits: 0→9, 3→12, −12→−3, −9→0), so it is idempotent and safe to retry |
| Tag 9383 arrives only on a fill | **It rides ANY execution report**, plain `39=0` accept included. One 1-share GTD order priced to rest reads any account |
| (mine, twice) Request For Positions either isn't on this session, or we simply never built it | **It exists in NEITHER spec.** Nothing to entitle, nothing to build our side. The order IS the read |
| `9387 TxfrCost` is a total | **The venue behaves as a PRICE PER SHARE** — 7 sh @ 7.00 → basis 49.00; 2 sh @ 3.00 → basis +6.00 |
| One wallet, one MPID, one inventory (03-08) | **Two accounts, one MPID.** Maker `1797733477`, taker `4963224393`, both IPLM. Positions are **per account** |

## ⚠⚠ The one that would have been worse than the incident

`scripts/ipo/allocate.py` was sending `txfrCost = quantity × price` — the total.
If 9387 is a per-share price, the Eagles line alone books a basis of
900,000 × $65,592,000, across all 170 lines, and **UPT cannot be undone**. The
05-08 probe used 1 share at 1.00, the single quantity where a total and a price
are the same number, which is why it stood for two weeks.

`--cost-unit` is now **required with no default**. The unit is measured on IPLY
and **unconfirmed on IPLM**, where the maker lives.

## What this unblocks

- **N49 closed** — two accounts, so the maker at `1797733477` is the seed target
  and the taker gets nothing from it.
- **N50 closed** — the seed IS reversible, via UEPR.
- **N53 opened** — the TxfrCost unit, which blocks the real seed.
- **E27's read side** — a position can be read on demand for the cost of one
  resting order. The `IPO_ALLOCATION` publisher is still missing.

## Next

1. **George's call on the 99,663 shares:** restore exactly, re-seed at a
   defensible basis, or leave flat. The old basis was $2.5 M/share on an
   instrument that last traded at $63.88 — almost certainly N53's unit error at
   an earlier seed, so an exact restore restores nonsense.
2. **Settle N53 on IPLM** — one transfer, distinctive quantity, distinctive
   price, throwaway symbol, read back with a 1-share resting order.
3. **Seed ONE team and verify** count and basis before the other 169.
