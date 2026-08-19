---
description: "Live forensics 15-08: N40 suspensions on the 14-08 slate confirmed, then the gateway disk-full incident — both FIX sessions down, logs archived to GCS, rotation installed"
---

# 2026-08-15-b — N40 suspension investigation, live (the 14-08 slate's six books)

> **Who:** AI session (investigation, read-only on the machine)
> **Type:** research / live forensics
> **Refs:** open-questions N40 · build-deploy-log #38 row · supervised29/supervised30 journals on the MM VM

## What we did

- George reported the six 14-08-slate books suspended after their games ended:
  COMM, BUCC, JETS, DOLP, BRON, FALC (WAS–MIA · NYJ–TB · ATL–DEN).
- Verified live via `mm.state` (admin NATS user): exactly 6 of 180 books
  `suspended` under supervised29/CFG-0027. Last readings: JETS/BUCC
  02:07:03Z · COMM/DOLP 02:08:01Z · BRON/FALC 02:09:53Z — game end. No
  readings after; books staleness-suspended ~20 s later. **This is the N40
  game-end class, exactly the 13-08 pattern.** The #38 publisher fix
  (keep-polling) is on the TESTING pool only; production still runs the
  retire-at-game-end code.
- **Mid-investigation, a parallel session cut the machine over:** supervised29
  stopped after 19,607 ticks (~02:48Z); **supervised30/CFG-0028** booted
  02:50:47Z (same code `deploy-ed921ca`, fresh journal
  `/var/lib/mm/supervised30`), taker journal snt17 02:51Z. The fresh journal
  drops the derived suspensions — all 180 books re-quote, the played six at
  their stale pre-final RPs (the N40 "quoting while bound game closed" shape).
- Chased George's second report (app shows COMM one-sided, panel two-sided):
  the venue book IS one-sided — **tZERO's risk check rejects every COMM sell**:
  `FAILSRISK[1797733477]: Aggressive SELL LmtPrx(58.15) is more than 3 percent
  BELOW the BID(60.80)`. Since the 02:50Z boot: COMM sell rejects 78 ·
  DOLP buy rejects 74 · BUCC sell rejects 4. The engine's stale RP sits >3%
  through the informed touch on those sides, so only the safe side rests.
  The app (venue book) is right; the panel renders the engine's view.

## What we learned

- The venue's 3% aggressive-price band is currently the only guard between
  the fresh-journal engine and informed post-game flow. It blocks the worst
  sides (COMM sells, DOLP buys) but anything within 3% of the touch still
  rests at pre-final prices.
- Suspension timing reconfirmed to the second: last reading + ~20 s
  (the live 5/10/20 s regime), per pair, three games.
- Under supervised30 the six books show `live: false` with the old reading
  stamps — occasional `readings=1` ticks are the old publisher's settle-watch
  re-offers (original stamps) inside its 1 h post-game window; after ~03:10Z
  the feed goes silent for good on this slate.

## What went wrong / got stuck

- **UNEXPLAINED, needs its own follow-up:** 02:42–02:47Z (before the
  cutover, supervised29 era) the four books JETS/DOLP/COMM/BUCC were the
  BUSIEST books on the venue (162–268 acks each in 4.4 min, above every
  active book) with ORDER_ACCEPTED / ORDER_REPLACED / ORDER_CANCELLED churn
  — while supervised29's own `mm.state` reported them `suspended` with a
  fossil resting list (JETS: 2 partially-filled sells at 45.27/46.92) that
  never moved across samples. BRON/FALC were properly dark. Either
  supervised29 quoted books its market state called suspended, or a second
  order source ran on the maker account (dual-engine shape). The churn ids
  were MM-prefixed and replace-heavy (maker-style). Not resolved.
- supervised29's realized P&L on COMM last night: **−$13,025** (net short
  5,252 at game end). Worth a look in the P&L review.
- The `/nats/monitor` proxy endpoint returns empty objects; NATS connz not
  reachable from the VM either (monitoring port closed) — could not list
  connections to attribute the churn.

## Decisions made

- None (investigation only; nothing deployed or changed by this session).

## Questions opened / closed

- N40: reconfirmed live, addendum appended to the row (15-08).
- New follow-up owed (logged in the N40 addendum): the 02:42–47Z churn
  attribution. ✎ Correction after reading the current build-deploy-log:
  the supervised30 cutover WAS logged — it is the gateway TTL deploy
  ceremony (Landed, 15-08 02:47–02:51Z, George's explicit go). The churn
  window (02:42:48–02:47:10Z) ends where that ceremony begins, so part of
  the tail may be ceremony traffic — but ORDER_ACCEPTED/REPLACED on four
  suspended books before 02:47 is still unexplained.
- **George's ask (15-08): "put a build deploy thing for this so that we can
  fix it" → done.** The #38 row is re-cut as QUEUED FOR PRODUCTION (path:
  clean PR → main, then a prod release of the publisher pool; the #37 trap
  stands) and a new row holds the engine-side N40 game-end lifecycle work.
  Both still sit behind the 14-08 deploy freeze — the lift must be explicit.

## Addendum 15-08 ~15:40Z → 17:10Z — the disk-full incident (same session)

George asked how the books were doing. They were not: **both FIX sessions to
tZERO had been down since ~14:52Z.** Root cause: the gateway VM's 19 GB root
disk hit 100% at 14:37Z — the FIX wire log (8.7 GB, never rotated) plus
syslog (3.5 GB). quickfix's 14:38:16Z logon failed writing its store header
and its reconnect loop died. Since then the gateway locally rejects every
order (`SESSION_DOWN`), the engine reports 180 stable books while quoting
into a void, and ~3,806 MM resting orders sit at the venue unmanaged.

Actions, in George's order ("we don't want to just clear the logs — take
them off the disk so this does not happen again"):

1. Created `gs://inplay-fix-gateway-logs` (us-east4), granted the VM's SA
   `objectAdmin`; streamed all four logs gzip → bucket (1.8 GB gz), verified
   the archive decompresses (FIX log from 29-05); THEN truncated in place,
   pruned old binary backups, vacuumed journald. Disk 100% → 30%.
2. Installed and PROVED (forced rotation → gz → GCS → local delete):
   `/etc/logrotate.d/fix-gateway` (daily/500 MB, copytruncate) · rsyslog
   re-cut the same way · `/usr/local/sbin/ship-rotated-logs.sh` as the
   `lastaction` hook (postrotate runs BEFORE compression — first attempt
   shipped nothing from `data/log`) · hourly `logrotate` cron so the caps
   bite intra-day.
3. Cloud Monitoring alert "VM root disk > 80%" (policy `4198694945183575391`,
   metric device is `/dev/sda1`, NOT `/dev/root`) → security-alerts email.
4. Gateway repo **PR #7**: `CLAUDE.md` with the storage section George asked
   for + `deploy/vm/` reference copies of the four VM files.

**Mistake, owned:** the binary-backup prune used `ls | sort | head -n -2`,
which is lexical — it deleted the two NEWEST backups
(`gateway-go.bak-124991e-pre-ttl`, the TTL rollback, and `bak-005fdd8`) and
kept older ones. Both rebuild from git; recorded in the build-deploy-log row.

**George's latency ruling (added ~16:10Z): rotation must NEVER run in a
game window.** Re-cut: no size trigger; the two configs moved OUT of
`/etc/logrotate.d/` (the system timer fires 00:00 UTC = 20:00 ET, prime
game time) into `/etc/logrotate.fix-gateway.d/`, run once daily at 08:00 UTC
(04:00 EDT / 03:00 EST — never a game, clear of the 00:01 ET session reset)
under `nice -n 19 ionice -c3` with their own state file. The one exception
is `/etc/cron.hourly/fix-gateway-disk-guard`: ≥ 85% used → force a rotation
now (a full disk kills both sessions; one blip mid-game is the lesser harm).
The 80% email alert fires first. Steady-state latency cost: none. Proper
follow-up: size-based non-blocking rotation inside `wireLogFactory` (Go).
PR #7 + `deploy/vm/` reference copies updated to match.

**RECOVERY CEREMONY 16:19–16:31Z (George: "redeploy the gateway? Or
restart with these changes").** Emergency cutover — no game live (only the
two stuck duplicate-id games from last night, settled 1/0), and the maker was
not quoting anyway. Sequence held: taker halt (journalled; 0 cancels out —
the session was dead) → `snt-1` stop → engine SIGTERM clean stop, tick
95,430 → `systemctl restart fix-gateway` (binary unchanged) → **both
sessions logged on in 5 s**, logon 14 ms, 180 MD symbols → `cancel_all`
swept **3,329** stale MM orders; every venue book verified empty →
engine **supervised31/CFG-0029** (fresh journal, replayed 0, 1,580
instructions / 180 books) → taker **SNT-CFG-0021 / snt18** (booted AUTO,
filling; boot rebase adopted venue truth on EAGL/SCGC/HOUC/SACS/ARKR…).
Verified: two-sided books at fresh prices (COMM 58.06/58.12, JETS
46.66/46.72, EAGL, BRON), dead-man armed/unlatched, MM open ~1,573 rising.

- **317 gateway-side phantom orders** (`PENDING_NEW`, all stamped
  14:37:39Z — the second the disk filled). They never reached tZERO but the
  tracker holds them and sweeps skip them `NOT_CANCELABLE`. Zero risk;
  gauge inflation; fix belongs with the reason-0 phantom PR.
- Ceremony fault, owned: the taker's FIRST start ran on the OLD env (a
  `sed` with `#` delimiters failed silently). It replayed snt17 and booted
  HALTED on the journalled halt, traded nothing, was stopped within
  seconds, env patched by python, restarted clean on CFG-0021/snt18.
  Lesson: patch env files with a script that ASSERTS the old line exists.
- **Second ceremony fault, owned — worse than the first:** the `cancel_all`
  loop (5 rounds × 35 s, break at < 300 open) was launched from an SSH
  command that hit the tool's 300 s timeout and moved to the BACKGROUND;
  I proceeded to start the engine without killing it. Its health poll from
  the MM VM intermittently returned empty (JSON error → the break test
  never fired), so rounds 4 and 5 fired at **16:28:21Z and 16:31:07Z — after
  the fresh engine was up — and swept its new book twice** (`cancels_sent`
  3,329 → 6,868). The engine took the unsolicited cancels and re-stood
  each time (two `CONVERGE_STALE` bursts, 16 then 88 securities dirty > 2 s,
  then backlog back to ~3); by 16:38Z: **1,617 resting, 180/180 two-sided,
  all `stable`, no alarms**, gateway gauge 1,935 = 1,617 + the 317 phantoms.
  No fills lost that we know of; the taker was resuming during round 4, so
  a few of its IOCs may have met an empty book. Lessons, both for the
  runbook: (a) a sweep loop must be a FOREGROUND step with an explicit exit
  before the engine starts — never let it outlive the step; (b) the
  gateway's `open_orders` gauge includes phantoms, so "< N" is a bad exit
  test — poll `stillResting` minus known phantoms, or just run a fixed
  number of rounds and stop.

## Next

- Rebuild the two deleted rollback binaries from `main@124991e` / `005fdd8`.
- Gateway follow-up PR: age out `PENDING_NEW` rows on a dead session (with
  the reason-0 retirement) so the 317 phantoms clear.
- Merge gateway PR #7 (docs + `deploy/vm/`).
- Deploy #38 (publisher keep-polling) to the PRODUCTION pool — the testing
  pool already proved it. Until then every game night re-creates this.
- The engine-side N40 work (game-end transition, settlement pricing, re-open
  policy) remains the real fix; the fresh-journal restart "recovery" quotes
  stale prices and leans on the venue's 3% band.
- Attribute the 02:42–47Z churn (dual-engine check: gateway logs by session,
  or ack-vs-tick correlation on the supervised29 journal).
