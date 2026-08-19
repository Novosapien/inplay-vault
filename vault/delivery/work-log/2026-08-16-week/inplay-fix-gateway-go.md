---
description: "Weekly engineering record for the FIX gateway, 09-16 August 2026 — 17 commits, four permanent-wrong order states removed, and the 15 August disk-full outage"
service: inplay-fix-gateway-go
window: 2026-08-09 .. 2026-08-16
commits: 17
authors: { westy412: 15, Hxsan: 2 }
branches: { touched: 8, merged: 6, open: 1 }
---

# inplay-fix-gateway-go — week of 09–16 August 2026

> **Delivery:** [[delivery]] · **Week:** [[work-log-2026-08-16]]

## Headline

The FIX gateway is the connection between the InPlay platform and the tZERO venue. This
week the team removed four ways an order or a price could stay wrong for ever. The team also
put a key on the operations routes that move money. The gateway VM then filled its disk on
15 August and both venue sessions dropped. The market maker had no venue connection for about
one hour and forty minutes. The team archived the logs, installed a daily log rotation,
and wrote the storage rules into the repository so the same fault cannot repeat unseen.

## Scope

- **Window:** 2026-08-09 to 2026-08-16
- **Commits:** 17 (westy412 15, Hxsan 2)
- **Branches touched:** 8 — 6 merged into `origin/main`, 1 open, plus `origin/main` itself,
  which took two direct commits from Hxsan
- **Busiest day:** 2026-08-14 (5 commits)

Two notes on the count. First, `git log --since="2026-08-09"` returns 16, not 17, because
git reads a bare date at the current time of day. `0f72555` (09 August, 18:47 BST) drops out
of that result. The command `--since="2026-08-09 00:00:00"` returns the correct 17. Second,
a `fetch` was not permitted, so the remote refs on disk are from the last local fetch.

`inplay-fix-gateway` is a separate repository beside this one. It holds the earlier Python
FIX gateway, one commit on `main` dated 2026-05-22, and it was dormant through the window.

## Themes

### The disk-full incident and the storage rules

The gateway VM has a 19 GB root disk. Nobody had ever rotated the raw FIX wire log. It
reached 8.7 GB, `/var/log/syslog` reached 3.5 GB, and the disk hit 100% on 15 August. The
full sequence is under **Notable fixes and incidents** below.

The repair on the VM was operational work, but the team also wrote it down. `CLAUDE.md` now
records what writes to the disk and the rotation and archive arrangement. It also records
the rules that follow. One rule: a new file writer goes into the rotation config in the same
change. `deploy/vm/` holds reference copies of the five installed files, so a rebuilt VM
returns to the same state. The rotation runs once a day at 08:00 UTC, which is 04:00 EDT.
That slot is deliberate. The copy and the upload cost latency on the order path, so the
rotation must never overlap a live game. One exception stands: an hourly guard forces a
rotation at 85% disk use. A full disk kills both FIX sessions, so one blip in a game is the
lesser harm.

This work sits on `docs/claude-md-storage-incident`. The branch is **open**. It is the only
unmerged branch in the repository.

### Orders that could not clear

Two separate faults left an order in a state that nothing could clear.

tZERO answers a cancel of an order it has forgotten with `CxlRejReason=1`, UNKNOWN ORDER.
The gateway logged the reject but never changed the order state. The order therefore stayed
open in the tracker and in the Redis open-order index for ever. On 10 August one ClOrdID was
rejected six times in one day. The market-maker open-order gauge read 63 against a venue
that held none of them. Every dead-man sweep re-cancelled the same phantom orders.
`MarkGoneAtVenue` now sets CANCELLED and writes through, which drops the order from
`fix:orders:open` and `fix:orders:open:mm`. Hxsan wrote this on 10 August and pushed it
straight to `main` (`005fdd8`).

tZERO also suppresses the Pending Cancel/Replace acknowledgement. No event can resolve a
`35=F` or `35=G` that the venue never answers. The request registry therefore pinned the
order `REQUEST_IN_FLIGHT` until somebody restarted the gateway. Every later cancel or edit
of that order was then refused locally. In the app that read as an order stuck on
"Updating..." for ever. The adapter now sweeps the registry every 5 seconds and expires an
entry older than 30 seconds. It answers the requester with a local reject reason
`REQUEST_TIMEOUT`. This is `fix/request-registry-ttl`, merged to `origin/main` as PR #6.

### Market data: fossil prices and empty books

A depth-1 snapshot with an empty side published nothing at all, so `market:quote:{symbol}`
kept its last written price for ever. Two real examples are named in the commit: an IPTCBILL
bid from 24 July, and an IPTCJETS price of 18.65. A real QA purchase nearly cleared that
second price. The snapshot path now always publishes, and it carries a cleared flag for each
absent side.
`PublishQuote` deletes the cleared fields from Redis instead of only ever writing the fields
a message carried.

The same change added `POST /md/book-resubscribe`. After the session recovery on 10 August
the depth stream served fresh but empty books for about two hours. The venue held full
ladders at the same time. The only cure was a gateway restart. The new route closes and
reopens one book subscription, or every book subscription, without a restart. It reuses the
exact opening `MDReqID`, which is a venue rule. The change also rate-limited
the sequence-gap warning, which had logged one line per message for hours. All three fixes
are the single commit `20f7a0f` on `fix/md-book-resubscribe`, merged to `origin/main` as
PR #2.

Separately, `feat/test-symbols` registered the ten tZERO test symbols, for example
`IPTCRAVE.TEST`, so the market-data session subscribes to them and order validation accepts
them. The dot makes the `market.*` subject four tokens, so ordinary `market.quote.*`
subscribers do not see them. That is deliberate — they are internal only. Merged as PR #1.

### The ops routes and the execution report

Four changes alter what the market maker and the trading service see.

Hxsan put a key on the operations HTTP surface (`d9394f8`, direct to `main`). Until then the
only protection was that nothing could route to port 8080, because `inplay-vpc` carries no
firewall rules. The broker now needs a path in so it can set buying power for a new account.
`/buying-power`, `/position`, `/position-transfer` and `/restart` now require `X-Ops-Key`.
An empty `OPS_API_KEY` **disables** the mutating routes with 503; it does not open them.
Read-only routes (`GET /health`, `/logs`, `/quotes`, `/loopback`) stay open, so the admin
proxy keeps polling without a credential. Any route not on that open list is guarded by
default.

`phase0/orders-mm-ops-route` added `GET /orders/mm`, which serves the market-maker subset of
the open-order index. This is the seam the market-maker boot healer reads, so the engine can
diff the venue's resting book against its own record at boot. It is Phase 0c of the fix set
in `specs/2026-08-14-mm-python-fix-set`; the vault session note
`market-maker/sessions/2026-08-14-fix-set-phase0-team-start.md` holds the plan. The route is
key-gated, because it discloses the whole resting market-maker book. Merged as PR #5.

`fix/deadman-window-10s` raised the dead-man default from 4 seconds to 10 seconds. The
dead-man cancels the whole market-maker book when the engine's heartbeat goes silent for
longer than the window. The engine's heartbeat rides its asyncio event loop and starves to
about 4.7 seconds under live-game load. The 4-second window therefore swept a live book
about 130 times on the 13 August slate. A second fallback in `oe_adapter.go` still said 4
seconds, so a follow-up commit aligned it. Merged as PR #4.

`fix/exec-carries-possize` put tag 9383, the venue's post-fill position, onto the order event
as `posSize`. The figure rides the same execution report as the fill, so it cannot race the
fill and cannot be dropped on its own. The separate `position.>` publish can be dropped: one
was lost under churn on 12 August and false-halted the taker's reconciler. That publish is
unchanged. An absent 9383 stays absent, because a fabricated zero would read as flat, and
flat is a real position. Merged as PR #3.

## Branches

| Branch | Author | Commits | Merged into | Purpose |
|---|---|---|---|---|
| `origin/main` | Hxsan | 2 direct (+6 merges by westy412) | mainline | Hxsan pushed the UNKNOWN ORDER retire and the ops key straight to `main`. |
| `fix/deadman-window-10s` | westy412 | 2 | `origin/main` (PR #4) | Dead-man window default 4s to 10s, and the second fallback. |
| `docs/claude-md-storage-incident` | westy412 | 2 | **open** | `CLAUDE.md` storage section and `deploy/vm/` reference copies after the disk-full incident. |
| `fix/request-registry-ttl` | westy412 | 1 | `origin/main` (PR #6) | TTL on in-flight cancel/replace requests. |
| `phase0/orders-mm-ops-route` | westy412 | 1 | `origin/main` (PR #5) | `GET /orders/mm` for the market-maker boot healer. |
| `fix/exec-carries-possize` | westy412 | 1 | `origin/main` (PR #3) | Tag 9383 on the order event. |
| `fix/md-book-resubscribe` | westy412 | 1 | `origin/main` (PR #2) | Fossil-quote fix, book resubscribe route, gap-log rate limit. |
| `feat/test-symbols` | westy412 | 1 | `origin/main` (PR #1) | Register the ten venue test symbols. |

The branch ref for `fix/request-registry-ttl` no longer exists on disk; the branch is named
by merge commit `a41e540`. The local clone holds no `origin/` ref for
`docs/claude-md-storage-incident`, but the vault records it as gateway PR #7.

## Notable fixes and incidents

**Gateway VM disk full — 2026-08-15, 14:37Z to 16:31Z.**

- *Symptom.* The disk reached 100% at 14:37Z. The next quickfix logon at 14:38:16Z failed
  with `unable to write to file: .../store/FIX.4.2-FHINPLAY01-TZFIXORDQA.header: no space
  left on device`. The initiator's reconnect loop died. Both the order-entry session and the
  market-data session to tZERO were logged off from about 14:52Z. The gateway rejected every
  order locally with `SESSION_DOWN`. The market maker still reported all 180 books stable and
  kept quoting with no session to the venue. The venue held about 3,806 unmanaged resting
  market-maker orders. The app's books were frozen. Nothing alerted.
- *Root cause.* Nobody had ever rotated the raw FIX wire log. It grew to 8.7 GB on a 19 GB
  root disk, and `/var/log/syslog` added 3.5 GB. The quickfix store shares that disk, and
  quickfix cannot log on if it cannot write its store.
- *The fix on the VM.* The team streamed all four logs to
  `gs://inplay-fix-gateway-logs/2026-08-15-disk-full/` (1.8 GB compressed). The team then
  truncated them in place, vacuumed journald, and pruned old binaries. Disk use went from
  100% to 30%. George ruled archive, not delete: the wire log is the order audit trail. The
  gateway then needed a restart, because quickfix does not resume its logon loop after a
  store write failure. Both
  sessions logged on within 5 seconds. `cancel_all` swept 3,329 stale market-maker orders.
- *Prevention.* Rotation once a day at 08:00 UTC from `/etc/cron.d/fix-gateway-logrotate`,
  under `nice -n 19 ionice -c3`, with `copytruncate` because quickfix holds the files open.
  The configs live in `/etc/logrotate.fix-gateway.d/`, not `/etc/logrotate.d/`. The system
  timer fires at 00:00 UTC, which is 20:00 ET and prime game time. There is no size
  trigger. `ship-rotated-logs.sh` uploads each rotated file to
  `gs://inplay-fix-gateway-logs/<host>/<YYYY>/<MM>/` and deletes the local copy on success.
  An hourly guard forces a rotation at 85% disk use. A Cloud Monitoring alert, "VM root disk
  > 80% used" (policy `4198694945183575391`), fires before the guard does.
- *What was written down.* `CLAUDE.md` holds the storage section, the rules that follow, and
  the recovery procedure. `deploy/vm/README.md` lists the five installed files with their VM
  paths, their modes, and the commands that verify them. This is gateway PR #7, still open.
- *Recorded errors from the recovery.* The backup prune used a lexical sort and deleted the
  two newest rollback binaries. The TTL deploy therefore has no on-VM rollback binary until
  somebody rebuilds them. A background `cancel_all` loop also outlived its step and fired
  twice after the fresh engine was up. The vault build-deploy-log records both, not this repo.

**Permanent `REQUEST_IN_FLIGHT` — reported 2026-08-15.** An order stuck on "Updating..." in
the app was a cancel/replace request that tZERO never answered. See "Orders that could not
clear" above. Fixed by `42de015`. The vault records the deploy of `main@a41e540` on 15 August
at 02:47–02:51Z. That was a 4.5 minute outage in a post-slate window. The team verified both
sessions and 180 market-data symbols after it.

**Phantom open orders — measured 2026-08-10.** 63 orders that tZERO had forgotten stayed
open in the tracker and survived restarts through the Redis index. Fixed by `005fdd8`. The
commit records the deploy to the gateway VM on 10 August at 12:53. The next sweep retired
all 63 phantom orders and the market-maker open count went to zero.

**Dead-man swept a live book about 130 times — 13 August.** The 4-second window fired on
normal heartbeat jitter of 4.0 to 4.7 seconds. The env row `MM_DEADMAN_TIMEOUT_MS=10000` was
set on the VM on 14 August at 00:19Z. PR #4 moved the code default to match on the same day.
The commit says the team must retune the value after the N15 heartbeat-jitter measurement.

**A deploy-order trap, recorded and then cleared.** The body of `20f7a0f` carried a warning:
do not deploy from that branch. The running binary carried the UNKNOWN ORDER fix, and that
fix was not yet in `origin`. A deploy would have rolled it back. Hxsan pushed the source
(`005fdd8`) to `main` on the same day, directly after the PR #2 merge, so the trap closed.

## Still open

- **`docs/claude-md-storage-incident`** — 2 commits, last one 15 August. **In flight, not
  abandoned.** The vault records it as gateway PR #7, opened the same day as the incident.
  Nothing is left to build. It needs a review and a merge. Note that the branch is
  documentation and reference copies only; the arrangement it describes is already live on
  the VM.

No other branch is unmerged. `origin/feat/md-full-book`, `origin/fix/fix-session-timezone`
and `origin/feat/deadman-mm-jetstream` still exist as refs. Their tips are reachable from
`origin/main`. Their last commits are 07 August and 24 July, outside this window.

Known follow-ups that are not branches yet:

- `42de015` names one deliberately: an execution report for an in-flight request with an
  unexpected `execType` is still dropped and the registry entry stays. An eager clear would
  orphan a legitimate out-of-order acknowledgement, so this needs venue-spec work.
- The vault records a gateway fix that is not built. tZERO also answers a cancel of a dead
  order with `CxlRejReason=0` and the text `ORDER DEAD[DMA]`. The gateway only retires on
  reason 1. About 211 such phantom orders survived the 15 August restart.
- The vault records 317 phantom `PENDING_NEW` rows, all stamped 14:37:39Z, that never reached
  tZERO. They inflate the gauge and every sweep skips them as `NOT_CANCELABLE`.

## Commit appendix

**`docs/claude-md-storage-incident`**

`a812056` · `2026-08-15` · westy412 · docs+deploy/vm: rotation pinned to the 08:00 UTC quiet slot, never in a game window
`a6becf0` · `2026-08-15` · westy412 · docs: CLAUDE.md with the VM storage arrangement + reference copies of the log-rotation/GCS-shipping configs

**`fix/request-registry-ttl`**

`42de015` · `2026-08-15` · westy412 · fix(oe): TTL on in-flight cancel/replace requests — no more permanent REQUEST_IN_FLIGHT

**`phase0/orders-mm-ops-route`**

`be9a25e` · `2026-08-14` · westy412 · feat(ops): GET /orders/mm — the boot healer's seam

**`fix/deadman-window-10s`**

`8150e05` · `2026-08-14` · westy412 · fix(mm): align the oe_adapter dead-man fallback with the 10s default
`823cbbf` · `2026-08-14` · westy412 · fix(mm): dead-man window default 4s -> 10s

**`fix/exec-carries-possize`**

`701520d` · `2026-08-13` · westy412 · feat(oe): carry tag 9383 on the order event — the exec's own position

**`fix/md-book-resubscribe`**

`20f7a0f` · `2026-08-10` · westy412 · feat(md): fossil-quote fix, book resubscribe heal, gap-log rate limit

**`feat/test-symbols`**

`0f72555` · `2026-08-09` · westy412 · feat(config): register the 10 venue test symbols (real ticker + .TEST)

**`main`** (direct commits and merge commits)

`a41e540` · `2026-08-15` · westy412 · Merge pull request #6 from Novosapien/fix/request-registry-ttl
`8f678d4` · `2026-08-14` · westy412 · Merge pull request #5 from Novosapien/phase0/orders-mm-ops-route
`8c90f31` · `2026-08-14` · westy412 · Merge pull request #4 from Novosapien/fix/deadman-window-10s
`124991e` · `2026-08-13` · westy412 · Merge pull request #3 from Novosapien/fix/exec-carries-possize
`d9394f8` · `2026-08-12` · Hxsan · feat(ops): require X-Ops-Key on the mutating ops routes
`005fdd8` · `2026-08-10` · Hxsan · fix(oe): retire an order when the venue says UNKNOWN ORDER
`3e807ba` · `2026-08-10` · westy412 · Merge pull request #2 from Novosapien/fix/md-book-resubscribe
`98b2770` · `2026-08-10` · westy412 · Merge pull request #1 from Novosapien/feat/test-symbols
