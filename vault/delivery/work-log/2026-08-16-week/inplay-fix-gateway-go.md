---
description: "Weekly engineering record for the FIX gateway, 09-16 August 2026: 17 commits, four permanent-wrong order states removed, and one outage"
service: inplay-fix-gateway-go
window: 2026-08-09 .. 2026-08-16
commits: 17
authors: { westy412: 15, Hxsan: 2 }
branches: { touched: 8, merged: 6, open: 1 }
---

# inplay-fix-gateway-go — week of 09–16 August 2026

> **Delivery:** [[delivery]] · **Week:** [[work-log-2026-08-16]]

## Headline

**The team removed four ways an order or a price could stay wrong for ever.**

- The FIX gateway is the connection between the InPlay platform and the tZERO venue
- The team also put a key on the operations routes that move money
- The gateway VM then filled its disk on 15 August, and both venue sessions dropped
- The market maker had no venue connection for about one hour and forty minutes
- The team archived the logs, installed a daily log rotation, and wrote the storage rules into
  the repository, so the same fault cannot repeat unseen

## Scope

- **Window:** 2026-08-09 to 2026-08-16
- **Commits:** 17 (westy412 15, Hxsan 2)
- **Branches touched:** 8 — 6 merged into `origin/main`, 1 open, plus `origin/main` itself,
  which took two direct commits from Hxsan
- **Busiest day:** 2026-08-14 (5 commits)

**Two notes on the count**

- **The count command** — `git log --since="2026-08-09"` returns 16, not 17. Git reads a bare
  date at the current time of day
  - `0f72555` (09 August, 18:47 BST) drops out of that result
  - the command `--since="2026-08-09 00:00:00"` returns the correct 17
- **The remote refs** — a `fetch` was not permitted, so the remote refs on disk are from the
  last local fetch

**The sibling repository**

- `inplay-fix-gateway` is a separate repository beside this one
- It holds the earlier Python FIX gateway, one commit on `main` dated 2026-05-22
- It was dormant through the window

## Themes

### The disk-full incident and the storage rules

**Why it matters** — a full disk stops both FIX sessions. The gateway then has no venue
connection, so the platform has no venue connection.

- **The disk** — the gateway VM has a 19 GB root disk. Nobody had ever rotated the raw FIX
  wire log
- **The growth** — the wire log reached 8.7 GB, `/var/log/syslog` reached 3.5 GB, and the disk
  hit 100% on 15 August

**`docs/claude-md-storage-incident`** · `a812056`, `a6becf0` · **open**
- **What** — `CLAUDE.md` now records what writes to the disk, the rotation and archive
  arrangement, and the rules that follow
- **What** — one rule: a new file writer goes into the rotation config in the same change
- **What** — the rotation runs once a day at 08:00 UTC, which is 04:00 EDT
- **What** — one exception stands: an hourly guard forces a rotation at 85% disk use
- **Why** — the repair on the VM was operational work. The team also wrote it down
- **Why** — the copy and the upload cost latency on the order path, so the rotation must never
  overlap a live game
- **Why** — a full disk kills both FIX sessions, so one blip in a game is the lesser harm
- **Where it landed** — `deploy/vm/` holds reference copies of the five installed files, so a
  rebuilt VM returns to the same state

> The branch is **open**. It is the only unmerged branch in the repository. The full sequence
> of the incident is under **Notable fixes and incidents** below.

### Orders that could not clear

**Why it matters** — an order in a state that nothing can clear is a phantom. The gauge, the
sweeps and the app then all act on a book the venue does not hold.

Two separate faults left an order in a state that nothing could clear.

**UNKNOWN ORDER never retired the order** · `005fdd8` · direct to `main`, Hxsan, 10 August
- **Symptom** — the market-maker open-order gauge read 63 against a venue that held none of
  them. Every dead-man sweep re-cancelled the same phantom orders
- **Cause** — tZERO answers a cancel of an order it has forgotten with `CxlRejReason=1`,
  UNKNOWN ORDER. The gateway logged the reject but never changed the order state
- **Cause** — the order therefore stayed open in the tracker and in the Redis open-order index
  for ever
- **Fix** — `MarkGoneAtVenue` now sets CANCELLED and writes through, which drops the order from
  `fix:orders:open` and `fix:orders:open:mm`
- **Evidence** — on 10 August one ClOrdID was rejected six times in one day

**`fix/request-registry-ttl`** · `42de015` · merged `origin/main`, PR #6
- **Symptom** — in the app that read as an order stuck on "Updating..." for ever
- **Symptom** — the request registry pinned the order `REQUEST_IN_FLIGHT` until somebody
  restarted the gateway. Every later cancel or edit of that order was then refused locally
- **Cause** — tZERO also suppresses the Pending Cancel/Replace acknowledgement. No event can
  resolve a `35=F` or `35=G` that the venue never answers
- **Fix** — the adapter now sweeps the registry every 5 seconds, and expires an entry older
  than 30 seconds
- **Fix** — it answers the requester with a local reject reason `REQUEST_TIMEOUT`

### Market data: fossil prices and empty books

**Why it matters** — a price that never changes is still a price. A buyer can clear at a figure
the venue abandoned weeks ago.

**`fix/md-book-resubscribe`** · `20f7a0f` · merged `origin/main`, PR #2 · three fixes, one commit
- **Symptom, fossil quote** — a depth-1 snapshot with an empty side published nothing at all,
  so `market:quote:{symbol}` kept its last written price for ever
- **Symptom, empty books** — after the session recovery on 10 August the depth stream served
  fresh but empty books for about two hours. The venue held full ladders at the same time
- **Symptom, empty books** — the only cure was a gateway restart
- **Symptom, gap log** — the sequence-gap warning had logged one line per message for hours
- **Fix, fossil quote** — the snapshot path now always publishes, and it carries a cleared flag
  for each absent side
- **Fix, fossil quote** — `PublishQuote` deletes the cleared fields from Redis, instead of only
  ever writing the fields a message carried
- **Fix, empty books** — `POST /md/book-resubscribe` closes and reopens one book subscription,
  or every book subscription, without a restart
- **Fix, empty books** — the route reuses the exact opening `MDReqID`, which is a venue rule
- **Fix, gap log** — the change also rate-limited that warning
- **Evidence** — the commit names two real examples: an IPTCBILL bid from 24 July, and an
  IPTCJETS price of 18.65. A real QA purchase nearly cleared that second price

**`feat/test-symbols`** · `0f72555` · merged `origin/main`, PR #1
- **What** — registered the ten tZERO test symbols, for example `IPTCRAVE.TEST`
- **Why** — the market-data session subscribes to them, and order validation accepts them
- **Why** — the dot makes the `market.*` subject four tokens, so ordinary `market.quote.*`
  subscribers do not see them. That is deliberate — they are internal only

### The ops routes and the execution report

**Why it matters** — four changes alter what the market maker and the trading service see. One
of them guards the routes that move money.

**Ops key on the operations HTTP surface** · `d9394f8` · direct to `main`, Hxsan
- **What** — `/buying-power`, `/position`, `/position-transfer` and `/restart` now require
  `X-Ops-Key`
- **What** — an empty `OPS_API_KEY` **disables** the mutating routes with 503. It does not open
  them
- **What** — read-only routes (`GET /health`, `/logs`, `/quotes`, `/loopback`) stay open, so
  the admin proxy keeps polling without a credential
- **What** — any route not on that open list is guarded by default
- **Why** — until then the only protection was that nothing could route to port 8080, because
  `inplay-vpc` carries no firewall rules
- **Why** — the broker now needs a path in, so it can set buying power for a new account

**`phase0/orders-mm-ops-route`** · `be9a25e` · merged `origin/main`, PR #5
- **What** — `GET /orders/mm` serves the market-maker subset of the open-order index
- **Why** — this is the seam the market-maker boot healer reads. The engine can diff the
  venue's resting book against its own record at boot
- **Why** — the route is key-gated, because it discloses the whole resting market-maker book
- **Where it landed** — Phase 0c of the fix set in `specs/2026-08-14-mm-python-fix-set`
- **Where it landed** — the vault session note
  `market-maker/sessions/2026-08-14-fix-set-phase0-team-start.md` holds the plan

**`fix/deadman-window-10s`** · `823cbbf`, `8150e05` · merged `origin/main`, PR #4
- **Symptom** — the 4-second window swept a live book about 130 times on the 13 August slate
- **Cause** — the dead-man cancels the whole market-maker book when the engine's heartbeat goes
  silent for longer than the window
- **Cause** — the engine's heartbeat rides its asyncio event loop, and starves to about
  4.7 seconds under live-game load
- **Fix** — the dead-man default rose from 4 seconds to 10 seconds
- **Fix** — a second fallback in `oe_adapter.go` still said 4 seconds, so a follow-up commit
  aligned it

**`fix/exec-carries-possize`** · `701520d` · merged `origin/main`, PR #3
- **What** — tag 9383, the venue's post-fill position, now rides the order event as `posSize`
- **Why** — the figure rides the same execution report as the fill, so it cannot race the fill,
  and it cannot be dropped on its own
- **Why** — the separate `position.>` publish can be dropped. One was lost under churn on
  12 August and false-halted the taker's reconciler
- **Where it landed** — that publish is unchanged
- **Where it landed** — an absent 9383 stays absent, because a fabricated zero would read as
  flat, and flat is a real position

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

- **`fix/request-registry-ttl`** — the branch ref no longer exists on disk. The branch is named
  by merge commit `a41e540`
- **`docs/claude-md-storage-incident`** — the local clone holds no `origin/` ref for it. The
  vault records it as gateway PR #7

## Notable fixes and incidents

**Gateway VM disk full — 2026-08-15, 14:37Z to 16:31Z**
- **Symptom** — the initiator's reconnect loop died. The gateway rejected every order locally
  with `SESSION_DOWN`
- **Symptom** — the market maker still reported all 180 books stable, and kept quoting with no
  session to the venue
- **Symptom** — the venue held about 3,806 unmanaged resting market-maker orders. The app's
  books were frozen
- **Symptom** — nothing alerted
- **Timeline**
  - 14:37Z — the disk reached 100%
  - 14:38:16Z — the next quickfix logon failed with `unable to write to file: .../store/FIX.4.2-FHINPLAY01-TZFIXORDQA.header: no space left on device`
  - about 14:52Z — both the order-entry session and the market-data session to tZERO were
    logged off
- **Cause** — nobody had ever rotated the raw FIX wire log. It grew to 8.7 GB on a 19 GB root
  disk, and `/var/log/syslog` added 3.5 GB
- **Cause** — the quickfix store shares that disk, and quickfix cannot log on if it cannot
  write its store
- **Fix** — the team streamed all four logs to
  `gs://inplay-fix-gateway-logs/2026-08-15-disk-full/` (1.8 GB compressed)
- **Fix** — the team then truncated them in place, vacuumed journald, and pruned old binaries.
  Disk use went from 100% to 30%
- **Fix** — George ruled archive, not delete: the wire log is the order audit trail
- **Fix** — the gateway then needed a restart, because quickfix does not resume its logon loop
  after a store write failure
- **Fix** — both sessions logged on within 5 seconds. `cancel_all` swept 3,329 stale
  market-maker orders
- **Prevention** — rotation once a day at 08:00 UTC from `/etc/cron.d/fix-gateway-logrotate`,
  under `nice -n 19 ionice -c3`, with `copytruncate` because quickfix holds the files open
- **Prevention** — the configs live in `/etc/logrotate.fix-gateway.d/`, not `/etc/logrotate.d/`
- **Prevention** — the system timer fires at 00:00 UTC, which is 20:00 ET and prime game time.
  There is no size trigger
- **Prevention** — `ship-rotated-logs.sh` uploads each rotated file to
  `gs://inplay-fix-gateway-logs/<host>/<YYYY>/<MM>/`, and deletes the local copy on success
- **Prevention** — an hourly guard forces a rotation at 85% disk use
- **Prevention** — a Cloud Monitoring alert, "VM root disk > 80% used" (policy `4198694945183575391`), fires before the guard does
- **Written down** — `CLAUDE.md` holds the storage section, the rules that follow, and the
  recovery procedure
- **Written down** — `deploy/vm/README.md` lists the five installed files with their VM paths,
  their modes, and the commands that verify them. This is gateway PR #7, still open
- **Recorded errors** — the backup prune used a lexical sort, and deleted the two newest
  rollback binaries
- **Recorded errors** — the TTL deploy therefore has no on-VM rollback binary until somebody
  rebuilds them
- **Recorded errors** — a background `cancel_all` loop also outlived its step, and fired twice
  after the fresh engine was up
- **Recorded errors** — the vault build-deploy-log records both, not this repo

**Permanent `REQUEST_IN_FLIGHT` — reported 2026-08-15**
- **Symptom** — an order stuck on "Updating..." in the app was a cancel/replace request that
  tZERO never answered
- **Cause** — see "Orders that could not clear" above
- **Fix** — `42de015`
- **Evidence** — the vault records the deploy of `main@a41e540` on 15 August at 02:47–02:51Z.
  That was a 4.5 minute outage in a post-slate window
- **Evidence** — the team verified both sessions and 180 market-data symbols after it

**Phantom open orders — measured 2026-08-10**
- **Symptom** — 63 orders that tZERO had forgotten stayed open in the tracker. They survived
  restarts through the Redis index
- **Fix** — `005fdd8`
- **Evidence** — the commit records the deploy to the gateway VM on 10 August at 12:53
- **Evidence** — the next sweep retired all 63 phantom orders, and the market-maker open count
  went to zero

**Dead-man swept a live book about 130 times — 13 August**
- **Cause** — the 4-second window fired on normal heartbeat jitter of 4.0 to 4.7 seconds
- **Fix** — the env row `MM_DEADMAN_TIMEOUT_MS=10000` was set on the VM on 14 August at 00:19Z
- **Fix** — PR #4 moved the code default to match on the same day

> The commit says the team must retune the value after the N15 heartbeat-jitter measurement.

**A deploy-order trap, recorded and then cleared**
- **Symptom** — the body of `20f7a0f` carried a warning: do not deploy from that branch
- **Cause** — the running binary carried the UNKNOWN ORDER fix, and that fix was not yet in
  `origin`. A deploy would have rolled it back
- **Fix** — Hxsan pushed the source (`005fdd8`) to `main` on the same day, directly after the
  PR #2 merge, so the trap closed

## Still open

- **In flight, not abandoned** — `docs/claude-md-storage-incident`, 2 commits, last one
  15 August
  - the vault records it as gateway PR #7, opened the same day as the incident
  - nothing is left to build. It needs a review and a merge
  - the branch is documentation and reference copies only
  - the arrangement it describes is already live on the VM
- **No other branch is unmerged** — `origin/feat/md-full-book`, `origin/fix/fix-session-timezone`
  and `origin/feat/deadman-mm-jetstream` still exist as refs
  - their tips are reachable from `origin/main`
  - their last commits are 07 August and 24 July, outside this window

**Known follow-ups that are not branches yet**

- **Deliberate, named in the commit** — `42de015` still drops an execution report for an
  in-flight request with an unexpected `execType`, and the registry entry stays
  - an eager clear would orphan a legitimate out-of-order acknowledgement
  - this needs venue-spec work
- **Recorded in the vault, not built** — tZERO also answers a cancel of a dead order with
  `CxlRejReason=0` and the text `ORDER DEAD[DMA]`
  - the gateway only retires on reason 1
  - about 211 such phantom orders survived the 15 August restart
- **Recorded in the vault** — 317 phantom `PENDING_NEW` rows, all stamped 14:37:39Z, never
  reached tZERO
  - they inflate the gauge
  - every sweep skips them as `NOT_CANCELABLE`

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
