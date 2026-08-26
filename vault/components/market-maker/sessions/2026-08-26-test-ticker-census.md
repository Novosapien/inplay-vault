---
description: "A census of the .TEST twins on 26 Aug: every source still shows the original ten, so the panel work for new twins waits on a list"
---

# 2026-08-26 — The `.TEST` ticker census

> **Who:** AI session, from the 26 Aug handover.
> **Type:** research. No code changed, no deploys.
> **Refs:** [[market-maker/test-symbols]] · panel `src/lib/symbols.ts` ·
> gateway `internal/config/symbols.go` · MM `src/mm/universe.py`.

## What we did

The handover said new `.TEST` tickers had been added since the ten of
2026-08-08, and the next task was panel features for them. The first step
was to enumerate the new twins. Every source was checked:

| Source | `.TEST` count | Note |
|---|---|---|
| Retail gateway `inplay-fix-gateway` — live `/quotes` | 10 | 180 symbols total |
| MM gateway `inplay-fix-gateway-mm` — live `/quotes` | 10 | 180 symbols total |
| Proxy `/market/quotes` (what the panel reads) | 10 | 180 symbols total |
| Gateway config `symbols.go` on `origin/main` | 10 | the `registerTest` loop, unchanged since `0f72555` |
| Panel `src/lib/symbols.ts` on `main` | 10 | 180 keys; zero diff against the live feed |
| MM `universe.py` | — | mints a twin of any known ticker on demand; no list |
| [[market-maker/reference/position-transfer-ledger]] | 10 | last twin rows are the 20 Aug top-ups to 900,000 |
| Slack (Hasan DM, tZERO channels) after 19 Aug | 10 | Hasan's 21 Aug note: "180 vs 180, nothing on either side alone" |
| Gmail, last 14 days | 0 mentions | — |

The ten are the same everywhere: BILL, CHIE, COMM, COWB, EAGL, JAGU, LION,
PACK, RAVE, TEXS.

## What we learned

- No new `.TEST` twin exists on either gateway, in any repo, or in any
  channel as of 2026-08-26 04:00Z. The premise of the next task does not
  hold yet.
- A new twin needs three edits before the panel can show it: the gateway
  `registerTest` list (both VMs), the panel `SYMBOLS` and `CONFERENCE`
  maps, and a venue position transfer. The MM engine needs none — it mints
  twins on demand.
- The gateway rejects a symbol that is not in its config (`IsValidSymbol`),
  so the engine's mint-on-demand does not reach the venue without the
  gateway edit.

## What went wrong / got stuck

- Blocked on the list of new twins. The panel feature cannot be specified
  without it.

## Decisions made

- None.

## Questions opened / closed

- Opened (N, George): which `.TEST` tickers are new, and where does the
  list live? If tZERO provisioned them, the gateway config and the panel
  map both need the same edit.

## Next

- Get the list of new twins from George or Rob Colucci. Then add them to
  the gateway `registerTest` list and the panel maps in the same change,
  and spec the panel feature against the real set.
