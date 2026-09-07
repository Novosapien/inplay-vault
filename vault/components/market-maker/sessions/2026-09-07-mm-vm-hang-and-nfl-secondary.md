---
description: "The 6–7 Sep maker outage — a KeyError crash, an auto-restart into a 13 GB journal replay, a 29-hour crawl, the reset, the fix, and the NFL open"
---

# 2026-09-07 — The maker VM hang: a crash, an auto-restart into a 13 GB replay, and the NFL secondary open

> **Who:** George + Claude session (inplay-vault, worktree `ops/2026-09-07-mm-vm-hang-and-nfl-secondary`)
> **Type:** live operations (incident) + build
> **Refs:** `inplay-market-maker` **PR #61** (`fix/malformed-replace-ack-drains`) ·
> [[market-maker/sessions/2026-08-18-the-cutover-and-the-vm-hang]] (the same shape) ·
> [[market-maker/sessions/2026-09-05-power-up-and-nfl-offering]] (the run this broke) ·
> gateway `/health` dead-man record · MM VM serial console
> **⚠ Ends with:** `mm-1` LIVE on **`supervised52` / CFG-0050**, **all 170 books** (PR #61 deployed), `Restart=no`;
> NFL secondary opened 09:30 ET with no maker until **12:24 ET**, when George's "the mm is not running" put it on the 32 NFL books.

## What we did

- **07:41 ET, the pre-open check found the NCAA market dark.** Gateway
  `/orders/mm` = 0; venue top of book across 340 symbols = 1 bid, 1 ask.
  The per-bot dead-man record for `mm-1`: `heartbeats: 0`,
  `last_fired_at: 2026-09-07T10:31:19Z`, `last_fire_cancels: 1476`,
  `latched: true`. The 32 IPO asks had expired on their GTD (0 × 900k) — that
  part was clean.
- **The MM VM was hung** — GCE RUNNING, SSH refused on 22, serial console
  emitting one Python traceback line every ~10 minutes, `systemctl: Transport
  endpoint is not connected` since 00:10Z. The 18-08 shape.
- **11:54:48Z instance reset (George: "get it up and running").** SSH back in
  10 s. `mm-1` was inactive (manual-start unit), so nothing replayed on boot.
- **11:56:47Z `mm-1` started on a fresh journal:** `supervised50`, **CFG-0048**,
  `MM_PRIOR_RUN_DIR=supervised49`, heal on, `MM_SECURITIES` unchanged at 138
  (env backup `/etc/mm-1/env.bak-cfg0047-pre-reset-0907`). Boot: replayed
  **1** event · heal DONE, 0 at venue · book standing **550 / 138**. Gateway
  at +75 s: 593 orders on 133 books, heartbeats 126, dead-man un-latched.
  At 12:25Z: 515 orders / 135 books, heartbeats 6,683, RSS 67 MB.
- **`Restart=no` on `mm-1`** (drop-in
  `/etc/systemd/system/mm-1.service.d/no-auto-restart.conf`, daemon-reload
  only — the running engine untouched). See Decisions.
- **The crash fixed in code — PR #61, merged `main@06c1735` and DEPLOYED
  13:26:18Z** (George: "merge it and get it going"): `_apply_replace` drains a
  replace ack that names no order instead of raising. 1,330 tests, ruff + mypy
  clean, three new tests. Cutover: stop 13:25:51Z → dead-man swept → VM
  checkout `mm-main-9aacef4` by bundle → **`supervised51` / CFG-0049 / prior
  `supervised50`** → replayed 1, heal 0, 548/138 standing; gateway 553 orders /
  138 books, heartbeats 21,349. Under a minute dark, 09:26 ET on a Monday.

## What we learned

- **The root cause is two defects stacked, and the second did the damage.**
  1. `2026-09-06 05:30:59Z` — `KeyError: 'orig_client_order_id'` at
     `src/mm/venue/engine.py:482` in `_apply_replace`: one `ORDER_REPLACED`
     on the shared MM namespace arrived without the field, read
     unconditionally **before** the alien check. Exit 1.
  2. `05:31:15Z` — systemd (`Restart=on-failure`, `RestartSec=15`) started
     it again, and that process **replayed `supervised49`**: *"anchor seed:
     NONE — this journal already holds 10,219,854 accepted events."* 13 GB
     on an 8 GB box. The VM crawled for 29 hours — through the whole NCAA
     Saturday — until the heartbeat died and the dead-man swept 1,476
     orders at 10:31Z on 7 Sep. NCAA then had **no maker at all** for 86
     minutes, and a glacial one for the 29 hours before that.
- **The 18-08 fix was procedural, not structural.** The pre-flight journal
  gate covers a human running a cutover; the boot healer makes a fresh
  journal safe. Neither touches an **automatic** restart, which replays
  whatever is on disk with no gate. `Restart=no` closes that.
- **The journal's growth is the underlying hazard.** `supervised49`: 11.84 M
  lines / 12.97 GB in 53 h (~6 GB/day). `supervised50`: **831 MB in its
  first 28 minutes**. Every replay of a journal this size fails on this box.
  Filed as **N80**; N70 already measured the ≥1 GB boot-walk problem for Go.
- **The dead-man did its job perfectly** — 1,476 cancels the instant the
  heartbeat stopped — which is exactly why "down" is the safe failure and the
  crawl is the dangerous one. This is the [[market-maker/decisions]] 01-09
  verdict ("the book must never be empty") violated from the other side: a
  book that is *stale* for a day is worse than one that is empty for ten
  seconds.
- **The reset recipe held for the third time** (18-08, 27-08, 07-09): reset →
  SSH in ~10–20 s → fresh journal + `MM_PRIOR_RUN_DIR` = previous → boots in
  one event. ⚠ It only works because `mm-1` is a manual-start unit.
- Not MM, recorded for the day's context: the 5 Sep NFL-offering broadcast
  exposed a notification-tap loop in the app (expo-router root remount on a
  cold-start `router.push`), fixed and shipped 6 Sep (`inplay-app` PR #27).

## What went wrong / got stuck

- **Nobody was watching the maker on Saturday.** The crawl ran 29 hours with
  1,476 orders resting and heartbeats still arriving — the dead-man cannot
  see a slow engine, only a dead one. `snt-halt-check` logged
  `maker=ABSENT(mm.state)` from 05:32Z on 6 Sep and nothing acted on it.
- `gcloud` reauth expired three times during the session; each venue check
  waited on George.
- The MM VM's SSH was refused for the whole hang; every read came from the
  serial console and the gateway's ops server.

## Decisions made *(mirror into [[market-maker/decisions]])*

- ✅ **`mm-1` does not auto-restart** (`Restart=no`, George 07-09, extending
  his 05-09 "manual starts only"). A crash leaves the engine DOWN; the
  dead-man sweeps the book in 10 s; a human starts it on a fresh journal.
- ✅ **Recovery on 138 NCAA books first; then 170 at 16:24Z.** The 27-08 ruling
  stood through the open; George's "the mm is not running" (12:18 ET, looking at
  NFL) was the go. NFL secondary traded maker-less 09:30–12:24 ET: one market
  order refused `NO_MARKET` (409) at 13:31Z, no fills seen.
- ✅ **The 170 inputs file is `/home/georgewestbrook/supervised-inputs-170.json`**
  (20 Aug) — George: "there is an input file for the NFL books"; found via the
  env backups' `MM_SUPERVISED_INPUTS` history. NFL rows are Edwin's 11 Aug
  numbers; NCAA rows identical to the 138 file.
- ✅ **The malformed-ack drain is the fix shape** (PR #61) — the same rule as
  the alien drain: no order id → no exposure → count, log, skip.

## Questions opened / closed *(mirror into [[market-maker/open-questions]])*

- **Opened N80:** the journal's growth rate (~6 GB/day steady, ~1.8 GB/h at
  boot) makes every replay unsurvivable on this box; what bounds it —
  checkpoint-based replay, rotation, or fewer journalled events?
- ⚠ Numbering: the unmerged `ops/2026-09-05-…` branch uses N78/N79 for the
  GTD-boundary and NATS-token items; `main` already holds a different N78
  (01-09). Whoever merges re-files, as with N56→N70.
- Open for George: **does the maker quote the 32 NFL books?** As of the open
  it does not.

## Next

1. ~~George's NFL call~~ — 170 since 16:24Z (CFG-0050 / `supervised52`). Watch
   the NFL books' first quotes against the IPO prices paid; IPTCRAMS has no
   Sportradar binding.
2. ~~Deploy PR #61~~ — done 13:26Z.
3. **N80** — decide how the journal is bounded before the next crash makes
   this note a fourth copy.
4. Wire `snt-halt-check`'s `maker=ABSENT` into an alert someone receives.
