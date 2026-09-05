---
description: "Triage of the 23:23Z 'book down 4+ min' alert — Auburn and Baylor dark 9 min at their game's end because the publisher's re-offer guard held while SR sat on the final"
---

# 2026-09-05 (b) — Auburn and Baylor dark for nine minutes at the final

> **Who:** Claude session (inplay-vault), George
> **Type:** ops / triage (read-only — nothing restarted, nothing changed on the machine)
> **Refs:** Cloud Monitoring policy `MM-1 book SUSPENDED too long` (`6304727655840835723`) ·
> `deploy/SNT-HALT-CHECK.md` · `inplay-sportradar-service/src/app/workers/mm_publisher/worker.py`
> (`_reoffer_would_mislead`) · `src/mm/valuation/freshness.py` · [[market-maker/open-questions]] N40 → **N80**
> **⚠ Ends with:** both books back, two-sided, at settlement prices. Nothing to recover. A policy question opened (N80).

## What we did

- **The alert.** `mm/suspended_oldest_age_s > 240` fired **23:23:53Z** (value 320.9 s) and
  resolved **23:28:24Z**. George saw the email and asked what was down.
- **Which books.** The checker line (`journalctl -u snt-halt-check`) read `suspended=2
  oldest=IPTCAUBT@0s` at 23:15:14Z and climbed to `@511s` at 23:23:45Z; the next run
  (23:24:50Z) read `suspended=0`. The second book was **`IPTCBAYB`** — same game.
  Auburn (home, `sr:competitor:4294`) v Baylor (away, `sr:competitor:4359`),
  `sr:sport_event:70894758`, kickoff 19:30Z. Bindings: `src/mm/bindings.py`.
- **Why they suspended — the engine side.** The journal's `valuation_sweep` events carry
  a per-game `observations` clock (the last SUCCESSFUL source observation). For this game
  it advanced every few seconds until **23:14:00.448Z**, then froze. 20 s later
  (`source_liveness_window_s`) the Reference Price went Invalid and `restriction()`
  returned SUSPENDED for both books. It moved again at **23:23:33.6Z** and both books
  re-opened dwell-free (auto-recovery, as designed — no human release).
- **Why the clock froze — the publisher side.** SR never stopped answering: the
  `inplay-mm-publisher` worker pool fetched the game's `timeline.json` every ~5 s with
  HTTP 200 straight through the window. What stopped was the **re-offer**. From
  **23:14:07Z to 23:23:20Z** the pool logged `mm_publisher_reoffer_withheld` on every
  tick (130 warnings). `_reoffer_would_mislead` needs three facts at once: the newest
  reading's scoreline differs from the game's current scoreline · the book is undecided
  (not saturated) · the reading is older than `stale_reoffer_grace_s` (120 s). The newest
  reading was from **23:05:56Z** (p_home 0.907). The score moved at ~23:14Z; SR never
  priced it. The guard refused to swear that number was fresh, so the MM heard silence.
- **What ended it.** SR flipped the game's status to ended/closed at **23:23:11Z**. The
  publisher marked the final, the engine accepted `official_result` (outcome home —
  Auburn won), the first settled reading (p_home = 1) landed at 23:23:33Z, `live=False`,
  both books re-opened at settlement prices.
- **Now (23:35Z):** AUBT stable 51.25 / 51.51 (647 / 607) · BAYB stable 43.25 / 43.53
  (540 / 640) · 138/138 quoting (114 stable, 24 active) · no alarms · kill switch off.
- **Same shape earlier the same day.** The 03:23:06Z alert (resolved 03:30:22Z) reads
  `suspended=2 oldest=IPTCMISP@0s` from 03:15:14Z, ≥ 11 min; the pool logged 13–67
  withheld re-offers a minute from 03:13Z to 03:25Z. Not examined further. Two dark
  windows in one Saturday; the NFL slate on Sunday will produce the same.

## What we learned

- ⭐ **The guard that refuses to lie makes a dark window exactly as long as the source's
  status lag.** The 15-08 withhold (N40 fix set) chose "dark" over "quote a pre-score
  probability". Its 120 s grace assumed SR re-prices a score within seconds (worst
  measured 90 s). At a game's LAST score SR never re-prices at all — it moves the status
  to closed, and today that took **9 minutes**. Every book ends its game through this
  window unless the last probability was already saturated. Availability lost at the
  moment of most interest, by design. Whether that is the right trade is a policy call —
  **N80**.
- **Timeline of a suspension in five commands.** (1) `journalctl -u snt-halt-check` →
  which book, how long. (2) `mm.state` on NATS (read-only `mm-monitor` cred in
  `/etc/snt-halt-check/env`) → its state now, `last_reading_ts_ms`, `live`.
  (3) `src/mm/bindings.py` → ticker ↔ `sr:competitor`; the journal's
  `probability_update` events key on `game_id` + team ids, NEVER on the ticker (a grep
  for `IPTCAUBT` finds only venue events). (4) the journal's `valuation_sweep`
  `observations[game_id]` → the exact second the source went quiet and came back.
  (5) Cloud Logging `resource.type="cloud_run_worker_pool"
  resource.labels.worker_pool_name="inplay-mm-publisher"` → the publisher's own words.
  The engine journals **no market-state transition event**; the checker's gauge and the
  sweep clock are the only record of a suspension.
- The checker unit exits 1 on every run while the taker is OFF (`taker=ABSENT`). It still
  writes every gauge; the `Failed to start` journal noise is cosmetic. Worth a
  `--taker-optional` flag some day.
- Detection latency held at the documented ~8 min: the policy fired 33 s AFTER the books
  had recovered. The 240 s threshold is not the limiter; ingestion + evaluation is.

## What went wrong / got stuck

- First journal pass grepped the ticker and found only venue acks — 20 minutes to learn
  that readings carry team ids. Recorded above so the next triage starts at step 3.
- `journalctl --since 2026-09-05T23:05` fails to parse; it wants `"2026-09-05 23:05"`.
- [[market-maker/open-questions]] carries **duplicate numbers**: N75, N77 and N78 each
  exist twice (the 01-09 rows and the 05-09 rows both used them). Not re-filed here;
  the new item takes **N80** to stay clear.

## Decisions made *(mirror into [[market-maker/decisions]])*

- None. Read-only session.

## Questions opened / closed *(mirror into [[market-maker/open-questions]])*

- **Opened N80 — the end-of-game dark window.** The re-offer guard + SR's status lag =
  every undecided book goes dark from (last score + 120 s) until SR marks the game
  closed (9 min today, ×2). Options for George / Edwin: accept it; synthesise the final
  from SR's status clock (period 4, clock 0:00 — beware overtime); re-offer the
  pre-score reading under a DEGRADED grade the engine would have to learn; or lengthen
  nothing and alert earlier. Sits under E11 (settlement definition) and N40.
- N40 gains a fourth observed shape (cross-referenced in its row).

## Next

- George's call on **N80** before Sunday's NFL finals — or accept the window knowingly.
- The 05-09 note's list still stands: Sunday 22:00 ET confirm the GTD expiry cleared
  the 32 NFL asks (`cancel_orders.py` as the belt) → the second power-down in order;
  rotate `inplay-nats-mm-token` + redact the boot line (N79); merge `feat/ipo-nfl-offering`.
