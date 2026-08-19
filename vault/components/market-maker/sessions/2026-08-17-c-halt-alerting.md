---
description: "The halt alerting built on 17-08 — both bots' state snapshots now page Cloud Monitoring, plus the finding that the maker runs with no supervisor at all"
---

# 2026-08-17c — the alerting, and the maker has no supervisor

> **Component:** [[market-maker/market-maker]] ·
> **Follows** [[market-maker/sessions/2026-08-17-b-recovery-and-the-40s-verdict]]
> (§7 item 1). Closes the gap that turned a four-minute glitch into a
> 50-hour outage.

---

## 1 · What we built

`snt-halt-check` on the market-maker VM: a systemd timer that runs every
60 s, reads BOTH bots' state snapshots off NATS, and writes them to Cloud
Monitoring as gauges. Three alert policies read those gauges and email
George and Hasan.

| Metric | Meaning |
|---|---|
| `custom.googleapis.com/snt/halted` | 1 = the taker is halted |
| `custom.googleapis.com/snt/snapshot_age_s` | wall age of its snapshot |
| `custom.googleapis.com/mm/kill_switch` | 1 = the maker's global kill switch |
| `custom.googleapis.com/mm/snapshot_age_s` | wall age of its snapshot |
| `custom.googleapis.com/mm/quarantined_books` | suspended book count |

| Alert policy | Fires on |
|---|---|
| **SNT-1 taker HALTED or not reporting** | `snt/halted > 0` for 5 min, **or no data** |
| **MM-1 maker DOWN or kill-switched** | `mm/kill_switch > 0` for 5 min, **or no data** |
| **SNT-1 taker snapshot STALE** | `snt/snapshot_age_s > 60` for 5 min |

**Silence pages.** The two liveness policies use
`EVALUATION_MISSING_DATA_ACTIVE`, so a dead bot, a dead VM or a broken
checker fires exactly like a halt does. The failure mode being fixed here
IS silence — a checker that can fail quietly would rebuild the same trap.

**It never touches the bots.** No restart, no resume. A halted taker must
stay halted until a human re-bases its floats (T-S05). Its NATS user is
read-only on the bus and it is read-only on the trading system.

Each policy carries a **runbook in its `documentation` field** — it
arrives in the alert email: what the alert means, the triage commands,
and, for the maker, a warning that restarting it is an event-sourced
cutover ceremony and not a command.

## 2 · ⚠ The finding: the maker runs with NO supervisor

George asked whether the maker and taker are on the same VM. They are —
and looking properly turned up something worse than a naming detail.

```
PID 252937   1-12:50   .venv/bin/python -m mm.runtime    ← the maker
PID 287446      42:59  .venv/bin/python -m snt.runtime   ← the taker
```

The taker is a systemd unit. **The maker is not a unit at all.** Its
PPID is 1 and its cgroup is `/user.slice/user-1001.slice/session-1153.scope`
— it was started by hand from a `screen`/SSH login session and orphaned
to init when that session ended. Consequences:

- **No `Restart=`.** It crashes, it stays dead.
- **No start on boot.** The VM reboots, the market maker is gone.
- **No `systemctl status`.** Its health is `ps` and nothing else.
- It survives only because nothing has killed it in 1 day 12 h.

Until today nothing would have noticed. The `MM-1 maker DOWN` policy now
would, within 5 minutes. **That is a detector, not a fix** — the process
still will not come back on its own.

⚠ This session did NOT fix it. Giving the engine a unit means restarting
it, and the engine is event-sourced: the restart has to carry its
journal, its checkpoint and the `ANCHOR_SEED` chain or it erases live
games' kickoff probabilities. That is the documented cutover ceremony,
scheduled, not casual. **Owed before the 29-08 slate.**

## 3 · Decisions and changes made

- ✅ **Both bots are covered, not just the taker** (George: "I swear the
  maker and the taker are on the same VM"). The first cut covered only
  the taker.
- ✅ **A new read-only NATS user, `mm-monitor`** (`publish: []`,
  `subscribe: ["mm.state", "snt.state.>"]`). A monitor should not hold a
  trading identity, and it must keep working when the taker's env is
  rewritten during a ceremony. Credential in Secret Manager as
  `inplay-nats-mm-monitor-url`, and root-only at
  `/etc/snt-halt-check/env` on the VM.
  ⚠ An earlier attempt widened `snt-taker`'s own subscribe list instead.
  That was **reverted** in the same session — the taker's credential is
  back to exactly what it was.
- ✅ **George added as a notification channel.** Previously every policy
  in the project emailed only Hasan.
  ⚠ **Two errors here, both corrected the same day.** First, this session
  claimed GCP would send a verification email that George had to click.
  It does not: `:sendVerificationCode` 404s for email channels, which are
  live the moment they are created. The claim was asserted without being
  checked, and George went looking for an email that was never coming.
  Second, the channel was created for `george.westbrook412@gmail.com` —
  taken from the session's account metadata rather than asked for — while
  George's working mailbox is `george.westbrook@novosapien.ai`. The first
  drill's alert was delivered to a mailbox he does not read. Both
  addresses are now attached, work mailbox for daytime triage and the
  personal one as the out-of-hours backstop: the 50-hour halt began on a
  Sunday morning.
- ✅ **The ops agent installed on the market-maker VM.**

## 4 · What we learned

- **⭐ `systemctl list-units` is not "what is running on this box".** The
  maker was invisible to it because it is not a unit. Earlier in the day
  this session told George "snt-1 is the only trading unit on the VM"
  while deciding a restart was safe. True as stated, wrong as understood.
  Use `ps -eo pid,ppid,etime,cmd` before believing a VM inventory.
- **⭐ The alert policy named for a VM did not cover it.** `VM root disk
  > 80% used (fix-gateway, market-maker, nats)` filters on
  `agent.googleapis.com/*` metrics, and the market-maker VM had **no ops
  agent installed** — no package, no unit files. Only centrifugo, the
  gateway and nats ever reported. The policy has claimed that VM since it
  was written and has never watched it, including through the 15-08
  full-disk incident. Now fixed. **A policy's NAME is not coverage;
  check that the series exists.**
- **The MM VM has no general internet egress.** No external IP, and its
  subnet is in none of the three Cloud NATs, so `dl.google.com` times out
  after 300 s. It reaches `*.googleapis.com` through Private Google
  Access, which is why writing metrics works. The agent was installed by
  side-loading the `.deb` over `scp` rather than by opening egress —
  giving a trading VM general internet access is a security posture
  change, not an install step.
- **⭐ "The alert fired" and "somebody was told" are two different
  claims.** The first drill proved the policy: Cloud Logging carries
  `ViolationOpenEventv1` at 12:40:55Z naming the policy and the threshold
  crossing, and `ViolationAutoResolveEventv1` at 12:46:24Z. It proved
  nothing about delivery — the notification went to an address George does
  not read, and searching his mailbox for `alerting-noreply@google.com`
  returned nothing at all. An alerting chain is only as good as its last
  hop, and that hop is the one nobody tests.
- **⚠ Project-wide, alerting has fired TWICE in 45 days** (Centrifugo
  13-08, this drill 17-08), so the notification path for Hasan's address —
  which every other policy in the project depends on — has never been
  confirmed to deliver either.
- **An untested alert is not an alert.** The halt policy was proven by
  injecting a synthetic `snt/halted=1` for 11 consecutive minutes against
  its 5-minute threshold, then letting it clear — without stopping the
  real taker. Hasan was temporarily removed from the policy during the
  drill so he was not paged by a test.

## 4b · Delivery PROVEN, and the real detection latency

Second drill, with all three channels attached:

| | |
|---|---|
| First aligned minute above threshold | 12:55:36Z |
| `ViolationOpenEventv1` | **13:03:37Z** |
| Email in George's inbox | **13:03:37Z** — same second, `INBOX`, not spam |

Sender `alerting-noreply@google.com`, subject
`[ALERT - No severity] snt/halted > 0 for 5 min (or no data) …`,
delivered to **`george.westbrook@novosapien.ai`**. The chain is proven end
to end: metric → policy → incident → email → inbox.

**⚠ The real detection latency is ~8 minutes, not the 5 the policy says.**
Measured twice: drill 1 took 8 min 22 s from first aligned violation to
incident, drill 2 took 8 min 1 s. The 5-minute `duration` is only part of
it — custom-metric ingestion and the evaluation cycle add roughly three
and a half minutes on top. Do not tighten `duration` to chase this; a
shorter window would fire on a single operator halt during a deploy
ceremony. **Against a 50-hour outage, 8 minutes is the win.** Expect it,
and do not treat a quiet 6 minutes after a halt as a broken alert.

Delivery to the email itself is instant once the incident opens, so the
whole latency is upstream of the notification.

## 5 · Runbook — the moving parts

| Thing | Where |
|---|---|
| Checker | `/usr/local/sbin/snt-halt-check` on `inplay-market-maker` |
| Timer / service | `snt-halt-check.timer` (60 s) → `snt-halt-check.service` |
| Interpreter | `/home/georgewestbrook/inplay-market-maker/.venv/bin/python` (needs `nats-py`) |
| Credential | `/etc/snt-halt-check/env` (0600 root) · Secret Manager `inplay-nats-mm-monitor-url` |
| NATS user | `mm-monitor`, read-only, in `/etc/nats/nats.conf` on `inplay-nats` |
| nats.conf backups | `.bak-2026-08-17-pre-sntstate-sub`, `.bak-2026-08-17-pre-mm-monitor` |

Check it by hand:
`sudo /home/georgewestbrook/inplay-market-maker/.venv/bin/python /usr/local/sbin/snt-halt-check`
→ `SNT_HALT_CHECK taker=OK maker=OK quarantined=0 …`

## 6 · Next

1. **Give the maker a systemd unit** (§2). Detector is in; the fix is
   not. Needs a scheduled cutover ceremony — journal, checkpoint,
   `ANCHOR_SEED`. Owed before 29-08.
2. ~~George: verify the notification email~~ — **withdrawn, no such step
   exists for email channels.** Superseded by: confirm the drill email
   actually arrived at `george.westbrook@novosapien.ai` and at Hasan's
   address. Until a human has seen one, delivery is unproven.
3. The `CANCEL STUCK` flood fix (`==` → `>=` plus a latch).
4. A `mm/quarantined_books` policy — the metric is live, but the
   threshold is a domain call (N40's "a suspended book must never be a
   dead end"). Needs George or Edwin.
