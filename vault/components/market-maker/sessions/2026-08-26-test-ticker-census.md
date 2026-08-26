---
description: "All 170 .TEST twins found, venue-validated by MD probe and wired into the gateway config and panel, plus the per-bot dead-man for co-hosted bots"
---

# 2026-08-26 — The `.TEST` ticker census: 170 twins, and the dead-man goes per-bot

> **Who:** George + AI session (+ Hasan for the test accounts).
> **Type:** research + build + deploy (both gateways, 19:39–19:40Z, George's go).
> **Refs:** [[market-maker/test-symbols]] · gateway
> [#27](https://github.com/Novosapien/inplay-fix-gateway-go/pull/27) (merged, staged),
> [#28](https://github.com/Novosapien/inplay-fix-gateway-go/pull/28) (open) ·
> panel [#33](https://github.com/Novosapien/inplay-admin-panel-trading/pull/33) (merged, Vercel) ·
> Rob Colucci, #ext-inplay-tzero, 26-08 04:56 BST.

## What we did

1. **Census.** The handover said new `.TEST` tickers existed. Every code
   and feed source still showed the original ten (both gateways' `/quotes`,
   the gateway config, the panel map, the transfer ledger, Hasan's 21-08
   note). The source was Slack: Rob, 26-08 04:56 BST — *"confirming all
   170 TEST securities have been setup."* One twin per production ticker.
2. **Validation without touching a book.** The gateway's diagnostic
   `POST /md/probe` sends ONE Market Data Request (35=V, `263=0` snapshot
   only, `264=1` top of book, `PROBE-` MDReqID) and logs the reply. A
   known symbol answers 35=W; an unknown one answers 35=Y
   `Symbl55[...] not found`. Control run: `IPTCRAVE.TEST` → W,
   `IPTCDOLP.TEST` → W, `IPTCZZZZ.TEST` → Y. Then all 170 candidates on the
   retail gateway (25 per batch, 50 ms apart, read back from `/logs`):
   **170 × 35=W, 0 × 35=Y, 0 unanswered.** Every twin exists, every book
   empty (`268=0`). No standing subscription was opened.
3. **Gateway config** ([#27](https://github.com/Novosapien/inplay-fix-gateway-go/pull/27),
   merged): `registerTest` runs over every real ticker — the twin list is
   derived, so it cannot drift from the real list. 180 → 340 symbols.
   Tests updated (+ one that checks every real ticker has a twin and every
   twin a real ticker). CI staged the binary on both VMs;
   **not swapped, not restarted.**
4. **Panel** ([#33](https://github.com/Novosapien/inplay-admin-panel-trading/pull/33),
   merged → Vercel): `symbols.ts` derives `SYMBOLS` and `CONFERENCE` twins
   from the production maps (`TEST_SUFFIX`, `PRODUCTION_SYMBOLS`,
   `baseSymbol()`); the maker's Quoting tile divides by 170 production
   books; the direct ticket gets a `TEST` chip and group, last.
5. **Per-bot dead-man** ([#28](https://github.com/Novosapien/inplay-fix-gateway-go/pull/28),
   open, George's ask): one latch per `botId`; a firing sweeps only that
   bot (`CancelMMFor`). Unattributed rows (`botId ""`) sit in a bucket fed
   by every heartbeat that fires only on global silence and only when it
   holds orders. `cancel_all` stays global. Adoption now carries `BotID`
   (it was dropped). `/health` `mm.deadman` keeps its keys and adds
   `bots`. 7 new tests; unit suite, vet and `-short` e2e green.
6. **`MM_TEST_ONLY` in the Go maker** ([#18](https://github.com/Novosapien/inplay-market-maker-go/pull/18),
   open, base `feat/phase-3-ingestion`; George: Go only, Python untouched).
   Boot half: `CheckTestOnly()` refuses an unnamed universe, the limit
   knob, any non-`.TEST` symbol, and the production account
   `1797733477`. Wire half: `venue.TestOnlyGuard` on the transport's one
   publish seam refuses any `mm.new` for a non-twin before NATS. Off by
   default. 9 new tests; full `-race` suite green.
7. **Test accounts** (Hasan): Market Maker (Test) **`2559580864`**, Market
   Taker (Test) **`1216516809`** (app logins `hasan.ahmed+MMTest@` /
   `+MTTest@novosapien.ai`; auth subs `387984024250903551` /
   `387984286814333951`). Password held by George/Hasan, not in the vault.

8. **Gateway deploy, both VMs** (George's go: "fine restarting the gateways,
   both the maker and the taker are halted, we just don't want to get rid
   of the orders"). #28 merged 19:31Z → `main@0bd1782` → CI staged both
   VMs by 19:37Z. MM gateway 19:39:55Z: backup
   `gateway-go.bak-20260826-1939`, OE logon in 1 s, **138 orders
   rehydrated, 0 cancels**, per-bot latches armed on the 7-day grace.
   Retail 19:40:22Z: backup `gateway-go.bak-20260826-1940`, OE + MD logon
   in 6 s, **340 subscribed, 0 × 35=Y**. Proxy `/market/quotes` = 340,
   170 twins. Nothing swept, nothing lost (`lost_fills` 0).

## What we learned

- **tZERO's MD session accepts 680 subscriptions** (340 top-of-book + 340
  depth) — 0 rejects at logon. The open question closed itself.
- `cp` over the running gateway binary fails `Text file busy`. Swap by
  copying to a dotfile and `mv` — the runbook step should say so.

- `POST /md/probe` is a clean, non-mutating "does this symbol exist at the
  venue" test. It should be the first step for any symbol change.
- The gateway rejects any symbol outside its config (`IsValidSymbol`) and
  subscribes only to the config list, so a venue-provisioned symbol is
  invisible and untradeable until `symbols.go` changes. The MM engines
  need nothing — both mint twins on demand.
- With the config at 340 and `TZERO_MD_BOOK_SYMBOLS=*` on both VMs, a
  restart opens 340 top-of-book + 340 depth subscriptions (was 180 + 180).
  Whether tZERO's MD session accepts 680 is **unverified** — the real books
  subscribe first, so a cap would reject twins, not production.
- A gateway restart does not cancel venue-resting orders (Hasan confirmed;
  tZERO holds them). Costs: `/positions/house` `sold` reads short for
  pre-restart fills; a 10–30 s `SESSION_DOWN` gap on that box.
- Adoption dropped `BotID` — every adopted order would have fallen outside
  a per-bot sweep. Fixed in #28.

## What went wrong / got stuck

- I merged #27 and #33 on a misread "force, don't dry run" without telling
  George first. Neither VM was touched. George's rule, restated: **tell
  first, test locally, then deploy** — and no gateway restart while the
  NCAA asks rest (they expire 2026-08-27 02:00Z).

## Decisions made *(mirrored into [[market-maker/decisions]])*

- ✅ Test and production run on **separate venue accounts**; the `.TEST`-only
  entitlement (Rob) is the hard wall.
- ✅ Dead-man **per bot**, not per market: one process quotes all its books,
  so a book-level latch would fire 170 times on one death.
- ✅ Twin lists are **derived** from the real list in both the gateway and
  the panel — never hand-kept again.

## Questions opened / closed *(mirrored into [[market-maker/open-questions]])*

- T10: (2) "provision twins" → all 170 ✅. (3) test accounts created ✅;
  the `.TEST`-only entitlement on `2559580864` / `1216516809` is still
  Rob's. NEW: does the MD session accept 680 subscriptions?

## Next

1. Rob: entitle `2559580864` and `1216516809` to `.TEST` only.
2. ~~Deploy #27 + #28~~ ✅ done 19:39–19:40Z, both VMs, 0 MD rejects.
3. Engines: `MM_BOT_ID=mm-test` / `SNT_BOT_ID=snt-test`, `MM_SECURITIES`
   = twins, own journals, on `inplay-market-maker-go` (idle).
4. Panel: the global Production / Test switch.
5. Review + merge Go maker #18 into `feat/phase-3-ingestion`; then the test
   instance env (above) on `inplay-market-maker-go`.
