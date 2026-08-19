---
description: "Handover for the taker's 33-hour halt: recovery ceremony, the gateway fill-drop fix (Go), the taker self-heal work (Python), the alerting gap, and everything else left open on 17-08"
---

# HANDOVER — 2026-08-17 — taker recovery + the fixes on both sides

> **For:** a fresh session (or two — one per repo). Read this, then
> [[market-maker/working-guide]], then
> [[market-maker/sessions/2026-08-17-taker-33-hour-halt-diagnostics]]
> (the full diagnostics), then [[market-maker/build-deploy-log]].
> **State of the machine as of 07:50Z 17-08:** the taker is HALTED and has
> been since 08:17Z 16-08. Nothing else is broken. Nothing is in flight.

> ## ✅ DONE + ⛔ PARTLY CORRECTED — 17-08 11:0xZ
>
> - **§1 recovery: DONE.** Taker live on `SNT-CFG-0027`, journal
>   `/var/lib/mm/snt24`, `OVERNIGHT=40`. (Recovered at 10:44Z on
>   CFG-0026/snt23/120 s, then moved to 40 s once the measurement below
>   cleared it.)
> - **§4 is WRONG and withdrawn.** The 40 s rate did not congest the
>   gateway. Measured over the full wire log: **0.02–0.04 s mean inbound
>   lag in every hour**, 286 msg/s at 0.04 s in the busiest hour, and
>   **6 lost fills in 230,847 (0.0026%)**. The cause was a FIX session
>   break at ~08:13 recovered by a `ResendRequest` at 08:17:16.
> - **§2 stands but is re-scoped** — a rare-event fix for session
>   recovery, and the exact discard path is not proven.
> - Evidence:
>   [[market-maker/sessions/2026-08-17-b-recovery-and-the-40s-verdict]].

---

## 0 · The one-paragraph story

⛔ **Corrected 17-08 — the version below blames the rate; the measurement
does not.** The taker halted itself at 08:17:13Z on 16-08 on a 28-share
divergence on IPTCHOUC (T-S05, correct behaviour, a TRUE positive) and
then sat halted for 33+ hours because nothing alerts on a halt. The FIX
session to tZERO broke at ~08:13 and recovered at 08:17:16 with a
`ResendRequest`; in that flush the gateway discarded a real 28-share fill
that had reached it. The halt fired three seconds before the resend
completed. Chain: session break → resend flush → fill arrives under an
in-flight cancel → gateway discards it → divergence → correct halt → no
alert → dark for a day and a half.

~~Root cause: under the congestion the taker's new rate caused (gateway
17–27 s behind the venue) the 1.5 s IOC cancel was in flight for
effectively every fill, so the drop path fired routinely.~~ **Withdrawn:
no congestion exists in the record.**

---

## 1 · Recovery — do this first (taker, ops, ~20 min)

**Do NOT just patch HOUC's float and resume.** HOUC was the FIRST book
caught; under 27 s of lag the drop path was firing across many books, so
other floats are wrong too. A fresh journal makes the boot rebase
re-base every book against the venue automatically (it did 179/180
correctly on 15-08).

```
1. Confirm nobody else is on the VM  (build-deploy-log; ListAgents)
2. taker is already halted — skip the halt step
3. sudo systemctl stop snt-1
4. sudo cp /etc/snt-1/env /etc/snt-1/env.bak-2026-08-17-cfg0025
5. edit /etc/snt-1/env:
     SNT_CONFIG_VERSION=SNT-CFG-0026        (bump — rule 2, RNG salt)
     SNT_JOURNAL_PATH=/var/lib/mm/snt23/journal.jsonl
     SNT_INTERVAL_OVERNIGHT_S=120           (was 40 — see §4; back to a
                                             rate the gateway can carry
                                             until the Go fix lands)
6. sudo mkdir -p /var/lib/mm/snt23 && sudo chown georgewestbrook:root /var/lib/mm/snt23
   ⚠ /var/lib/mm is root-owned; skipping this crash-loops the unit
     (PermissionError, 15 restarts) — happened 15-08
7. sudo systemctl start snt-1
8. verify:  pid=$(systemctl show snt-1 -p MainPID --value)
            sudo tr '\0' '\n' </proc/$pid/environ | grep SNT_   (the env
            the PROCESS has, not the file — the unit file is a decoy)
            journalctl -u snt-1 -o cat | grep -c "BOOT REBASE"  (expect
            many — that is the floats correcting)
9. it boots HALTED (the halt is journalled)?  NO — fresh journal, so it
   boots armed. If it halts again within a minute, read the RECONCILE
   line: that book's figure came from position.> (not exec-borne), which
   the rebase deliberately refuses. Patch that one float from the halt
   line's numbers and resume.
```

VM: `inplay-market-maker`, project `inplay-497712`, zone `us-east4-a`,
`--tunnel-through-iap`. Code root is `~/snt-checkout/src` via PYTHONPATH,
currently `main@0b9f601`. Halt/resume: `nats pub snt.control.snt-1
'{"cmd":"halt"}'` from `inplay-nats` as `admin` (password in Secret
Manager `inplay-nats-admin-token`).

⚠ Every restart drops all books to OVERNIGHT until the bus re-derives
(~30 s). Do it outside a live game.

---

## 2 · THE GO FIX — `inplay-fix-gateway-go` (root cause)

**File:** `internal/adapter/oe_adapter.go`, `handleExecutionReport`,
~line 474.

**Defect:**
```go
if pending := a.registry.GetByReq(clOrdID); pending != nil {
    switch {
    case pending.Kind == state.RequestCancel  && execType == 4: a.resolveCancel(...)
    case pending.Kind == state.RequestReplace && execType == 5: a.resolveReplace(...)
    default:
        a.logger.Warn("exec report for in-flight request with unexpected execType", ...)
    }
    return nil    // ← a FILL (execType 1/2, LastShares>0) is discarded here
}
order := a.tracker.ApplyExecutionReport(...)   // never reached
```

**Fix shape (proposed — not built):** the early `return nil` is the bug.
A report that is not the pending request's ack must still fall through
to `tracker.ApplyExecutionReport` and be published. Do NOT clear the
pending request on the way through — the other session's 15-08 concern
("an eager Clear would orphan a legitimate out-of-order ack") is right;
leave it, and let its own ack (or the 30 s TTL from PR #6) settle it.
Concretely: keep the switch for the two ack cases, then **remove the
`return nil` and continue** to the tracker for everything else, so a
fill under a pending cancel is processed like any fill.

**Test to add:** NewOrderSingle → cancel request registered (in flight)
→ fill report (`150=1`/`2`, `32>0`) arrives → assert the fill is applied
to the tracker AND published on `order.>` with `posSize`, AND the pending
cancel is still registered. Then the cancel's own `150=4` arrives →
assert it resolves. Also the mirror: replace in flight + fill.

**Evidence to reproduce from:** FIX wire log
`/opt/fix-gateway/data/log/FIX.4.2-FHINPLAY01-TZFIXORDQA.messages.current.log`
on `inplay-fix-gateway`, `grep -a MMSN2dec5d3406f347` — three messages:
35=D, 35=8 ack (`32=0`), 35=8 fill (`32=28 31=56.97`). No 35=F ever
sent. The `unexpected execType` warning line for 08-16 is gone (journal
retention starts 08-17 07:34), but the wire + arithmetic prove it.

**Companion defect, same file, also owed:** tZERO answers a cancel of a
dead order with `CxlRejReason=0` + text `ORDER DEAD`; the gateway
retires tracker rows only on `reason=1` (UNKNOWN_ORDER). Dead rows
re-cancel for ever. Symmetric with the `MarkGoneAtVenue` reason-1 path,
gated on the ORDER DEAD text. Owed since sessions/2026-08-15-gateway-ttl-
deploy. **799 taker orders had unanswered cancels on 16-08** — this is
why.

**Deploy:** the gateway ordered ceremony (taker halt/stop → engine clean
stop → cancel_all → binary swap → engine → taker), documented in
`deploy/OBSERVABILITY-REDEPLOY.md` in the MM repo. Post-slate window.
Owner: Hasan's repo — his review.

---

## 3 · THE PYTHON FIXES — `inplay-market-maker`, `src/snt/`

In priority order. Details in the diagnostics doc §6–§8.

### 3.1 Alert on the halt (hours — do first)
`snt.state.snt-1` publishes `halted` and `ts_ms` every ~1 s and the
admin panel already renders it. Nothing reads it and shouts. Cheapest:
an external checker (cron on the MM VM, or the panel) that pages on
`halted: true` or snapshot age > 60 s. Do NOT use systemd `WatchdogSec`
to auto-restart on halt — a halted bot must stay halted until re-based.

### 3.2 Halt the BOOK, not the bot (small)
`snt/reconcile.py` keys per book already; the halt was made bot-wide on
10-08 by choice ("stricter than the requirement"). Edwin's T-S05 says
per-book. Make divergence quarantine one ticker; the other 179 keep
trading. Interacts with N40's rule "a suspended book must never be a
dead end" — give it a re-open path (the auto-rebase in 3.4, or manual).

### 3.3 Fix the `CANCEL STUCK` flood — a bug shipped in PR #44 (small)
5,392 lines / 799 orders on 16-08, one per 0.25 s tick. `stuck_orders`
matches `cancel_attempts == threshold` but `cancels_due` only increments
every 2 s, so it re-fires ~8 ticks per retry window. Fix: `>=` plus a
once-per-episode latch on the `PendingOrder`. The test passed because it
drove both on the same cadence — add a test that ticks at 0.25 s.
⚠ Log floods starve the loop (the 08-13 lesson).

### 3.4 Bounded self-heal — auto-adopt small exec-borne divergences (medium, needs rulings)
On a divergence surviving the 5 s grace, **if the figure is exec-borne
(tag 9383 on the exec report)**: |Δ| ≤ 🟡 500 sh → ADOPT (pin float,
journal `kind: "rebase"`, keep trading); |Δ| > 500 → halt that book;
figure from `position.>` fallback → halt that book (can be one fill
stale — the 12-08 false halt). Rate limits: 🟡 3 per book per session,
🟡 20 portfolio per session; over → escalate to halt. Every adoption
alarms. Justification: the boot rebase already does exactly this at boot
(179/180 correct on 15-08); T15 has behavioural evidence; George ruled
"trust the venue" on CLEM 14-08. **T-S05 is EDWIN's requirement — take
the change to him with the evidence, don't do it quietly.**

### 3.5 Instrument skip reasons in `orders_this_tick` (small, deferred)
Still unbuilt; the rate residual was closed by measurement instead.
Worth it before NCAA scale.

---

## 4 · The rate posture — what to run until the Go fix lands

Currently in `/etc/snt-1/env` (SNT-CFG-0025): `SNT_LOSS_BUDGET=0` ·
`SNT_MAX_SPREAD_TICKS=40` · `SNT_INTERVAL_OVERNIGHT_S=40` ·
`SNT_MAX_ORDERS_PER_S=0`. LIVE is one print/s (PR #40, George's ruling).

⛔ ~~**The 40 s overnight rate is what pushed the gateway 27 s behind.**
Recommend 120 s until §2 lands.~~ **WITHDRAWN, 17-08.** The rate is
cleared and George ruled it stays at **40 s**. Measured over the full
wire log, per minute: mean inbound lag 0.02–0.04 s in EVERY hour at
40 s; 286 msg/s at 0.04 s mean in the busiest hour; 6 lost fills in
230,847. The 27 s figure was sampled inside a minute carrying 36
messages during a dead session — it is the age of a post-outage flush,
not a lag level.

The measurement method is worth keeping: inbound lag = gateway log time
− FIX tag 52 SendingTime, bucketed **per minute alongside the message
count**. Reading the lag without the denominator is what produced the
wrong answer.

**Live now:** `SNT-CFG-0027` · journal `/var/lib/mm/snt24` ·
`SNT_LOSS_BUDGET=0` · `SNT_MAX_SPREAD_TICKS=40` ·
`SNT_INTERVAL_OVERNIGHT_S=40` · `SNT_MAX_ORDERS_PER_S=0`.

The Sunday-slate / NCAA-Saturday load questions (trading worker at
min 2 / max 6, 1 vCPU; ~60 LIVE books ≈ 175 events/s ≈ 14 instances,
over both the Cloud Run cap and the DB connection budget) remain open and
dated: **29-08**.

---

## 5 · Also open, not urgent

- **The trading worker's quote fold** runs ~40 min behind in games
  (`inplay-trading-service` `market.py:377`, one DB commit per message,
  sequential). Diagnosed by another session 15-08; fix is conflate-the-
  fold or a JetStream consumer. This is Jared's #6/#13/#14. Also
  `nats-py` drops silently at its 128 MiB pending ceiling with no
  `error_cb` — register one.
- **Thin floats:** IPTCBEAR reached 293 sh, PANT 36 on 15-08 — a book
  can spend its float before the 1,500 drift cap engages. E39 (Edwin);
  or shorts (E26/T16).
- **E41 round with Edwin:** the four intervals, P(same side) 0.57–0.60
  at the new rate, the 1 s print target levers (interval ~0.85 s /
  sweep_probability / guard reading `leaves_qty`).
- **N44 closed** (no portfolio cap, George); mechanism dormant.
- **Vault:** every session's edits are uncommitted in the shared tree on
  `docs/t0-plain-english-guide`. Someone commits `-A` and sweeps them all.

---

## 6 · Traps (all cost real time this weekend)

- **Multiple sessions drive this VM.** Two collided on 15-08 inside one
  minute. Read the build-deploy-log, name ONE driver, and don't message
  other sessions unless George says to.
- The taker's code root is `~/snt-checkout/src` (PYTHONPATH), not the
  venv path in ExecStart. Verify with `/proc/PID/environ`.
- `journalctl --since "-2min"` misparses → false "it stopped" alarm.
  Use absolute times.
- The `admin` NATS user cannot subscribe to `market.>`/`order.>`; use
  the taker's credential from `/etc/snt-1/env.secret` in a `nats-py`
  script.
- **A quiet taker with `epoll_wait` and an ESTAB socket is HALTED, not
  hung** — read the log back to the `RECONCILE HALT` line before
  diagnosing.
- State snapshot keys: `realized_pnl_total` is per book, not top level.
- New journal dir needs mkdir + chown before start.
- Every restart drops books to OVERNIGHT ~30 s — not during a game.
- 94% fill is the PORTFOLIO number; LIVE books fill 87–89% of IOCs.

---

## 7 · What landed this weekend (for orientation)

- MM #40 (LIVE 1 print/s, arrival-clock fix, env-tunable rates) —
  merged + deployed 15-08.
- MM #44 (wedge fix: cancel re-arm + age-bounded wash guard;
  `SNT_LOSS_BUDGET`; `SNT_MAX_SPREAD_TICKS`) — merged `0b9f601`, running.
  ⚠ carries the §3.3 flood bug.
- Trading worker scaled min 2 / max 6, 1 vCPU, 1 GiB (revision
  `00051-hqh`).
- Taker env posture SNT-CFG-0025 (§4).
- The wedge (a lost cancel silences one side of a book) — found, fixed,
  live evidence PANT/BILL 15-08.
- The 33-hour halt — diagnosed to the wire; this handover.
