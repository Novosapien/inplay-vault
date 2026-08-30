---
description: "The MD feed was alive all along; 868 orders from the 13:30 SIGSEGV boot were stranded by a Redis LRU eviction of the order index, and swept by seeding it"
---

# 2026-08-20 (c) — The stranded book, and the market data feed that was alive

> **Who:** George + AI session.
> **Type:** live operations. No code changed. Production Redis written once, the MM gateway restarted once, a real venue swept.
> **Refs:** [[market-maker/sessions/2026-08-20-b-first-live-venue-run]] · N59 · N60 · N62 · gateway `internal/store/order_index.go` · `internal/adapter/oe_adapter.go`.
> **Ended with the venue clean: 3 retail orders resting, zero MM orders, MM gateway tracker 0.**

## What we did

- **Verified the box state from the handover.** `inplay-market-maker-go` still runs binary `376e17b8…`, `MM_READINGS_FROM_NEW` is absent, `MM_JOURNAL_PATH` is `go-run03`. Nothing was started.
- **Tested the market data feed instead of reading its timestamps.** `POST /md/probe` (a `35=V` snapshot request) on the retail gateway answered with a `35=W` in ~25 ms for IPTCBILL, then for all 180 books. The feed was alive. It had gone quiet at 17:12:20 because nothing traded after the sweep. ⚠ The MM gateway has `TZERO_MD_ENABLED=false`. The only MD session is `INPLAYQTSQA` on the retail box.
- **Took a full-book snapshot of every book at the venue.** 871 live orders on 95 books. **868 were the Go maker's 13:30:02 boot** — the SIGSEGV boot placed 868 orders in 1.3 s and died. All DAY orders, all on FHINPLAY02. The other 3 are retail bids of 100 shares. **Zero 900,000-share IPO orders anywhere.**
- **Traced why no tracker knew them.** Redis (`inplay-redis`, 1 GB BASIC, `allkeys-lru`) peaked at 1.02 GB around 14:00. The MM gateway logged **74,444 `order index write failed … OOM`** in that hour. Lifetime `evicted_keys` is 18.4 M. Resting-order hashes are the coldest keys, so LRU evicted them. The MM gateway's 15:53 restart logged `restoredOrders=0`. The 16:06 boot healer "fetched 0" because the index was empty, not the book. The 15:45 operator sweep and the 17:12 dead-man sweep read the same empty tracker. Order 1296 (IPTCCARD) became visible only because retail traded 100 shares against it at 17:33 and the gateway adopted it.
- **Checked for session crossover.** The retail gateway restarted at 13:18 with `MM_ENABLED=false` and sent no MM order after that. All 868 were FHINPLAY02's. The split holds.
- **Cleared them with the gateway's own machinery** (George approved, ~17:55Z). The mint is deterministic, so the 13:38 boot's 868 `Duplicate clOrdID` rejects in `go-run01/journal.jsonl` name every stranded order with symbol, side, quantity and price. Seeded 867 rows into `fix:order:*` + `fix:orders:open` + `fix:orders:open:mm` (Redis was at 99 MB, writable; the adopted order was already indexed). Restarted the MM gateway: `rehydrated … count=868`, `dead-man armed at boot restingMM=868`, fired at +30 s, **868 `35=F` → 868 `39=4` → 0 `35=9`**. Re-snapshot of all 180 books: the 3 retail orders only.

## What we learned

- ⭐ **The order index is the dead-man's memory, and it lives in an LRU cache that filled.** Resting orders are the coldest keys in Redis, so they are the first to go. After any OOM, the next gateway restart strands the whole book. This is N62, owner Hasan.
- **A quiet feed and a dead feed look identical from the panel.** The test is a snapshot request to the venue, not a comparison of two timestamps.
- The sweep's `stillResting=N` log line is read before the cancel acks land. It is a timing artifact (463 at 17:57:34, 0 seconds later), not a count of survivors.
- The gateway's `/logs` ring buffer holds 200 entries. Probe in batches of 20 and drain between batches.
- The gateway logs `REDIS_URL` with its password at INFO on every boot. Same hygiene problem as the 19-08 `OPS_API_KEY` print.

## What went wrong / got stuck

- The handover framed N59 as a dead publisher. Hours of the previous session went into that framing. One `35=V` settled it in 25 ms.
- The MD probes ran on the retail gateway, because that is where the MD session is. George's rule — the MM gateway is the maker's only session — held for order entry throughout. It cannot hold for market data until the MM gateway carries an MD session of its own.
- I used the retail gateway's ops key from its env file in-shell to call `/md/probe`. The key was never printed.

## Decisions made *(mirrored into [[market-maker/decisions]])*

- ✅ **Operator index seed + restart as the clearance path for tracker-less MM orders** (George, 20-08 ~17:55Z). The seed is the exact set the venue rejected as duplicates; a wrong row costs one `35=9`.
- ✅ **N59 is not a Saturday risk by the stated mechanism.** A full-book sweep does not blank market data.

## Questions opened / closed *(mirrored into [[market-maker/open-questions]])*

- **N59 closed** — the feed was alive.
- **N60 closed** — zero IPO orders at the venue. Whatever cancelled them, they are gone.
- **N62 opened** — the Redis order index under `allkeys-lru` is not durable. Owner Hasan.

## Next

1. **Check Redis before any gateway restart:** `used_memory` well under 1 GB, `SCARD fix:orders:open:mm` equal to the MM gateway's `/orders/mm` count. If they diverge, the tracker is already lying.
2. Deploy `5988827c…` (HEAD `53e7ac6`) to `inplay-market-maker-go`, set `MM_READINGS_FROM_NEW=on`, fresh `go-run04`, bump `MM_CONFIG_VERSION` to `CFG-0040-GO` (fresh journal → bump, R-D06), start, verify the boot line reads "starts at stream HEAD".
3. Then the quoting gate against the reference — does the Go ladder match Python's geometry.
