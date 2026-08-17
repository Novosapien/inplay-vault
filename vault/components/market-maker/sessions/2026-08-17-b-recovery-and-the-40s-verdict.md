---
description: "The taker recovery on 17-08 and the measurement that cleared the 40 s overnight rate — the gateway was never congested, and only 6 fills in 230,847 were lost"
---

# 2026-08-17b — the recovery, and the measurement that cleared 40 s

> **Component:** [[market-maker/market-maker]] ·
> **Supersedes the root cause in**
> [[market-maker/sessions/2026-08-17-taker-33-hour-halt-diagnostics]] and in
> [[market-maker/sessions/2026-08-17-handover-taker-recovery-and-fixes]].
> **Read the correction in §3 before you act on either of those documents.**

---

## 1 · What we did

**Recovered the taker.** It had been halted 50 hours (since 08:17:13Z on
16-08). The §1 ceremony from the handover, run at 10:44Z:

- `SNT-CFG-0026`, fresh journal `/var/lib/mm/snt23`, `OVERNIGHT=120`
- 177 books re-based against the venue at boot, 546 fills in the first
  minutes, zero halts, zero `CANCEL STUCK`.

**Then measured the gateway**, because George asked the right question:
*work out why 40 s did not work*, rather than accept 120 s as a guess.

Two passes over the 4.6 GB FIX wire log
(`FIX.4.2-FHINPLAY01-TZFIXORDQA.messages.current.log`, 15-08 16:19 →
17-08 10:45), per minute:

1. message count by type, plus inbound lag (gateway log time − tag 52
   `SendingTime`) — 2,549 minutes;
2. taker fills on the wire (`11=MMSN*`, `150=1|2`, `32>0`) per hour,
   against the taker's own logged fill lines per hour.

**Then set the rate back to 40 s** on the evidence — `SNT-CFG-0027`,
journal `/var/lib/mm/snt24`, at 11:0xZ. Live, no halts.

## 2 · What we learned

### 40 s was never the problem

| | measured |
|---|---|
| Inbound lag, every hour at 40 s | **avg 0.02–0.04 s** |
| Busiest hour (15-08 21:00, Sunday slate) | **286 msg/s, avg lag 0.04 s, max 1.2 s** |
| Overnight hours at 40 s | ~100–200 msg/s, avg lag 0.02–0.03 s |
| Taker fills received, 15-08 21:00 → 16-08 08:00 | **230,841 of 230,847 — 0.0026% loss** |
| Minutes with inbound lag > 2 s, in 12 h | **4** — all inside one event |

The gateway carried the 40 s rate for 20 hours with 20 ms of lag, and
carried 286 msg/s during the live slate. There is no congestion in the
record.

### What actually broke, 16-08

1. **08:13** — the FIX session to tZERO breaks. Traffic collapses in
   BOTH directions: our own outbound new orders fall from ~740/min to
   2/min. This is the tell that it is a session break, not load — load
   does not stop us sending.
2. **08:13–08:16** — the pipe is dead (1,478 → 44 → 36 → 8 msg/min).
   tZERO's messages queue; when they are finally read they are logged up
   to **27 s** after their `SendingTime`.
3. **08:17:13** — the reconciler halts on IPTCHOUC, `venue=4467
   ours=4439`, exactly 28 shares short.
4. **08:17:16** — quickfix completes a `ResendRequest`, resending our
   messages 698142–698168. The halt fired **three seconds before the
   recovery flushed**.

The HOUC order on the wire, end to end:

```
08:15:06.150  35=D  buy 28 IPTCHOUC @56.97   (stamped 08:15:02.497 — 3.6 s late OUT)
08:15:33.081  35=8  ack   32=0               (stamped 08:15:06.467 — 27 s late IN)
08:15:33.445  35=8  FILL  32=28 31=56.97 9383=4502   (same 27 s)
```

**The fill reached the gateway and never reached the taker.** The halt
was a TRUE positive — those 28 shares were genuinely gone.

### The frequency

One disruptive event in the 12-hour run. The other traffic collapse in
the window, 16-08 03:59, is the **daily venue session roll** (seen again
cleanly at 03:59–04:01Z on 17-08: `Session reset` → `Disconnected` →
`connection refused` → logon at 04:01:30). The scheduled roll cost zero
fills — it is graceful. The 08:13 break was not.

## 3 · ⚠ The correction — what the earlier documents get wrong

The 17-08 diagnostics doc and the handover both state: *the taker's new
rate congested the gateway (17–27 s behind), so the drop path at
`oe_adapter.go:474` fired routinely across many books.* **The measurement
does not support this.**

- **"17–27 s behind" was a stall artefact.** The 27 s reading comes from
  a minute carrying **36 messages**. It is the age of messages flushed
  after a 4-minute outage, not a standing congestion level. The same
  metric in a 6,200-message minute reads 0.02 s.
- **"Fired routinely across many books" is contradicted by the fill
  count.** Six lost fills in 230,847, four of them inside the stall.
- **The 177 boot rebases are NOT evidence of lost fills.** Every one of
  the 177 `BOOT REBASE` lines has `journal=` exactly equal to that
  book's `SNT_FLOAT_OVERRIDES` value. With a fresh journal the taker
  starts from the stale 15-08 seed and adopts the venue's CURRENT
  position after a night of trading. Large differences are expected and
  mean nothing about correctness. (This session made that mistake too,
  mid-session, and had to withdraw it.)

**What survives from the earlier diagnosis:** the fill genuinely reached
the gateway and genuinely never reached the taker. That much is proven
on the wire.

**What is NOT proven:** that `oe_adapter.go:474` is the specific line
that discarded it. The gateway's app log for 16-08 has aged out of
journald, so the discard was reconstructed, not observed. The dedup
paths at `oe_adapter.go:497–517` (`CheckSeqNum` on a resend,
`CheckContentKey` on a recycled ExecID) can also discard an execution
report, and a resend window is exactly where they are most likely to
misfire. **:474 is the leading candidate, not a finding.**

## 4 · What went wrong / got stuck

- I asserted "162 books re-based — the drop path was firing almost
  everywhere" from the rebase count, before checking what the rebase
  figure actually is. It is the env override. Withdrawn within the hour
  by testing it (177/177 matched the override exactly), but it was the
  same class of error the earlier diagnosis made: reading a number
  without establishing what produces it.
- The gateway app log for the incident window is gone. journald
  retention on `inplay-fix-gateway` starts 17-08. Only the FIX wire log
  and the 8 KB session event log survive, and the event log retains only
  the tail of the resend burst.

## 5 · Decisions made

- ✅ **OVERNIGHT stays 40 s** (George, on the measurement). 120 s was a
  provisional floor for one hour and is withdrawn.
- ✅ **The recovery ran on the fresh-journal ceremony**, not a HOUC float
  patch (George).
- ✂ **The session-gap grace idea is dropped.** Proposed mid-session, then
  killed by the evidence: the fill was not late in transit, it was
  discarded, so no taker-side wait recovers it.

## 6 · Questions opened / closed

- **Closed:** "why did 40 s not work" — it did work. The rate is cleared.
- **Opened:** what broke the FIX session at 08:13 on 16-08? Not
  recoverable from retained logs. Needs the gateway's app log retention
  extended before the next occurrence.
- **Opened:** which gateway path actually discarded the fill — `:474` or
  a dedup path? Needs a counter per discard path (see Next).

## 7 · Next

1. **§3.1 alerting** — unchanged in priority and now the clear top item.
   A 4-minute glitch became 50 hours dark because nothing reads
   `snt.state.snt-1`.
2. **Gateway observability before the gateway fix** — a counter and a
   WARN on every path that discards an execution report (`:474` default
   branch, both dedup paths), plus journald retention on
   `inplay-fix-gateway` long enough to survive a weekend. Without these
   the next incident is reconstructed again.
3. **The `:474` fix** — still correct, but re-scoped: a rare-event fix
   whose real exposure is session recovery, not steady-state load.
   Hasan's review.
4. **§3.3 `CANCEL STUCK` flood** — unchanged (`==` should be `>=` plus a
   latch).
