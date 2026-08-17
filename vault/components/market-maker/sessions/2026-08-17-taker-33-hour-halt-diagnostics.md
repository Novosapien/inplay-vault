---
description: "Diagnostics for the taker's 33-hour silent halt: T-S05 fired correctly on a 28-share divergence, nothing alerted, and the bot-wide halt stopped 180 books — plus the self-healing design"
---

# 2026-08-17 — the 33-hour silent halt: diagnostics and the self-heal design

> **Who:** George + Claude · **Type:** incident diagnostics (read-only)
> **Severity:** the taker stopped trading for 33+ hours and nothing said so
> **Refs:** T-S05 · [[market-maker/market-taker-requirements]] · MM PR #44 ·
> decisions 2026-08-10b (T-S05 built) · 2026-08-14b (the boot rebase) ·
> [[market-maker/sessions/2026-08-15-taker-rate-verification]]

## 1 · What happened

| when | what |
|---|---|
| 15-08 23:38:06Z | Taker restarted (another session). `SNT-CFG-0025`, journal `snt22` **kept** — 0 boot rebases, i.e. the floats already matched the venue |
| 16-08 00:00 → 08:12 | Normal: 260–280 fills/min |
| 16-08 **08:17:13Z** | **`RECONCILE HALT — reconcile IPTCHOUC: venue=4467 ours=4439 (float=4902)`** · 682 cancels swept |
| 16-08 08:17:16Z | Last fill — in-flight orders settling |
| 16-08 08:17 → 17-08 07:46+ | **Silent. 33 hours. Nothing alerted.** |

**It did not crash and it did not hang.** The process stayed alive, the
NATS socket stayed `ESTAB` with zero queued bytes, and the state
publisher kept publishing throughout — a snapshot pulled at 07:46Z on
17-08 was 0 seconds old and read `halted: true`. A halted bot that keeps
publishing is the designed behaviour ([halted-is-not-silent], 12-08).

⚠ **A first, wrong diagnosis was given before the log was read back far
enough:** "hung on a dead socket, parked in `epoll_wait`". `epoll_wait`
is simply what an idle asyncio loop looks like; a halted taker sends
nothing, so it waits. The halt line was in the log the whole time.

## 2 · Why it halted — ROOT CAUSE FOUND: the gateway dropped a real fill

**IPTCHOUC: venue 4467, ours 4439 — the venue holds 28 shares MORE.**
The wire log identifies the missing fill exactly.

### 2.1 The lost fill, from the FIX wire (proof)

`MMSN2dec5d3406f347` — one of the five `CANCEL STUCK` orders on that
book, and the only one of exactly 28 shares. Its complete wire history
(`FIX.4.2-FHINPLAY01-TZFIXORDQA.messages.current.log`) is THREE
messages, no more:

| gateway log time | msg | content |
|---|---|---|
| 08:15:06.150 | `35=D` | our NewOrderSingle — `11=MMSN2dec5d3406f347 54=1 38=28 44=56.97 55=IPTCHOUC`, SendingTime **08:15:02.497** |
| 08:15:33.081 | `35=8` | the venue's ACK — `32=0`, SendingTime **08:15:06.467** |
| 08:15:33.445 | `35=8` | **THE FILL — `32=28` (LastShares) `31=56.97` (LastPx)**, SendingTime **08:15:06.467** |

**The arithmetic closes exactly:** float 4902 + pos −463 = **4439**
(ours). Add the unrecorded 28-share buy → **4467** = the venue's figure
to the share. The taker's journal contains no fill matching it.

### 2.2 Where it was lost — NOT NATS

NATS logged **zero** slow-consumer or dropped-message events all day
(retention reaches back to 05-28, so the window is covered). The loss is
upstream of the bus.

### 2.3 The mechanism — `oe_adapter.go:474`, a KNOWN open defect

```go
if pending := a.registry.GetByReq(clOrdID); pending != nil {
    switch {
    case pending.Kind == state.RequestCancel && execType == 4:  // cancel ack
    case pending.Kind == state.RequestReplace && execType == 5: // replace ack
    default:
        a.logger.Warn("exec report for in-flight request with unexpected execType", ...)
    }
    return nil          // ← THE FILL IS DROPPED HERE
}
```

**If ANY request is in flight for a ClOrdID, an execution report for
that order which is not the specific ack that request expects is logged
and discarded.** It never reaches `tracker.ApplyExecutionReport`, so it
is never published to NATS and the taker never learns of it.

This is the defect recorded as open in
sessions/2026-08-15-gateway-ttl-deploy: *"the gateway's known
unexpected-execType drop (registry-first resolution in
`handleExecutionReport`) — deliberately NOT bundled into #6 (an eager
Clear would orphan a legitimate out-of-order ack; needs venue-spec
work)."* It has now cost a 33-hour outage.

### 2.4 Why the precondition was met — the congestion made it certain

The IOC substitute cancels every order **1.5 s** after sending it. Under
normal latency (~12 ms round trip) the ack and any fill arrive long
before that cancel exists, so the registry is empty and the drop path is
never reached.

**Measured at the incident: the gateway was running 17.3 s mean,
27.0 s max behind the venue's own SendingTime on inbound messages.**
(18 samples across 08:15:3x — the same 27 s visible in the table above:
venue sent at 08:15:06.467, gateway processed at 08:15:33.)

At that lag **every** IOC order has its cancel in flight when its fill
is finally processed — so the drop path fires as a matter of course, not
as a rare race. Corroboration: **no `35=F` cancel was ever sent to the
venue** for this order (only the three messages above exist on the
wire), i.e. the taker's five cancels sat unresolved in the gateway's
request registry — exactly the `pending != nil` state.

### 2.5 The causal chain, end to end

1. **15-08 20:08 — `SNT_INTERVAL_OVERNIGHT_S` 400 s → 40 s** took the
   170 quiet books from ~0.44 to ~4.35 orders/s: an order-of-magnitude
   rise in gateway traffic. (Applied by this session at George's
   "very low limitations" instruction.)
2. The gateway falls **17–27 s behind** on inbound processing.
3. Every 1.5 s IOC cancel is therefore in flight when its fill lands.
4. `oe_adapter.go:474` **drops the fill**.
5. The taker's tally silently loses shares → divergence.
6. T-S05 halts, correctly.
7. Nothing alerts → 33 hours dark.

⚠ **Consequence not yet quantified: HOUC is only the FIRST book caught.**
The halt is bot-wide and fired on the first divergence detected, so other
books may carry unrecorded fills from the same window. Every book's float
needs re-basing against the venue before resuming — which the boot rebase
does automatically on a fresh journal.

⚠ Honest limit: the gateway's own `unexpected execType` warning for
08-16 cannot be read back — its journal retention starts 08-17 07:34.
The drop is proven by code, by the wire's three-message history, and by
the exact arithmetic; the warning line itself is inferred.

## 3 · Why it stayed dark for 33 hours — the actual defect

T-S05 is specified to require a human:

> *"the venue and our tally disagree; 682 cancels out, resume only after
> a human decides which number is real"*

That is correct as designed and was the right call in August when **T15
(is tag 9383 live and accurate?) was unconfirmed**. The failure is that
**a fail-safe requiring human action shipped with no way to tell a
human.** There is:

- no alert on `halted: true`,
- no alert on snapshot age,
- no alert on "no fills while books are open",
- and the taker deliberately never publishes MM heartbeats, so the
  gateway's dead-man cannot see it either ([no-heartbeat]).

**The signal was on the wire the entire time.** `snt.state.snt-1`
carries `halted` and `ts_ms`, published every ~1 s, and the admin panel
already renders it. Nothing reads it and shouts.

## 4 · The amplifier — the halt is BOT-WIDE

Edwin's requirement (T-S05) says divergence **halts that book**. The
10-08 build made it **bot-wide** on purpose, recorded at the time as
"stricter than the requirement; a divergence undermines trust in the
whole tally". That was a defensible call at **5 books**.

At **180 books it is the wrong trade**: a 28-share gap on one book
stopped trading on all 180 for 33 hours. Had the halt been per-book as
specified, 179 books would have carried on and the blast radius would
have been one ticker.

## 5 · What has changed since T-S05 was designed

The case for automatic recovery is much stronger now than in August:

1. **T15 has behavioural evidence.** 08-11: the venue's per-account
   figure moved by exactly each fill, fill after fill. 12-08: tag 9383
   verified live and share-accurate, twice.
2. **We already adopt the venue's number automatically — at boot.** The
   boot rebase (George, 14-08, from the CLEM halt) adopts each book's
   FIRST exec-borne figure after boot. On 15-08 it fired for **179 of
   180 books** and was correct every time.
3. **George has ruled "trust the venue" when asked** — the CLEM halt,
   14-08.
4. **The exec-borne figure cannot race.** Tag 9383 rides the SAME
   message as the fill, so it can neither arrive out of order nor
   half-arrive. This is exactly why the boot rebase is exec-borne only:
   the parallel `position.>` feed CAN be one fill stale, which caused
   the 12-08 false halt.

So the machine already trusts the venue automatically in the one place
it was allowed to. The proposal below extends that same trust, under
bounds, into the session.

## 6 · The fix — bounded self-healing

### 6.1 Change the blast radius (do this regardless)

**Halt the BOOK, not the bot** — i.e. implement T-S05 as written.
One diverging ticker quarantines one ticker. Alone, this turns a
180-book outage into a 1-book outage.

### 6.2 Auto-adopt small exec-borne divergences

On a divergence that survives the 5 s grace window **and whose figure is
exec-borne**:

| condition | action |
|---|---|
| \|delta\| ≤ `auto_rebase_max_shares` (🟡 proposed **500**, ~11 median clips) | **ADOPT** — pin the float so holding == venue, journal it loudly, keep trading |
| \|delta\| > that bound | **HALT that book** — a large gap is structural, not a lost message |
| figure came from the `position.>` fallback | **HALT that book** — never adopt a figure that can be stale (12-08) |

### 6.3 Rate-limit the self-heal, so a systematic fault cannot hide

- `auto_rebase_max_per_book_per_session` (🟡 proposed **3**). A book that
  keeps diverging has a real fault; escalate it to a book halt.
- A portfolio budget (🟡 proposed **20/session**). Broad message loss
  must surface as an incident, not be quietly absorbed 180 times.
- Every adoption is journalled (`kind: "rebase"`, already exists and
  already replays chronologically) so replay stays exact and the
  audit trail is complete.

### 6.4 Self-healing must never mean silent

Every auto-rebase and every halt raises an alarm. The distinction is
**who is woken**, not **whether it is recorded**.

## 7 · The alerting gap — cheapest fix, biggest win

Independent of any self-heal, and buildable today because the data
already exists:

1. **Alert on `snt.state.snt-1` showing `halted: true`.**
2. **Alert on snapshot age** > ~60 s (covers process death, which the
   halt path does not).
3. **Alert on "no fills for N minutes while books are open"** — catches
   the class where the bot believes it is trading and is not.

Any one of these turns 33 hours into under a minute.

## 8 · Related defects found in the same pass

- ⚠ **`CANCEL STUCK` floods the log — a bug shipped in MM PR #44.**
  **5,392 lines across 799 distinct orders** on 16-08, timestamps
  0.252 s apart (one per tick). The alarm was claimed to fire "once per
  order"; `stuck_orders` matches `cancel_attempts == threshold`, but
  `cancels_due` only increments every `cancel_retry_after_s` (2 s)
  against a 0.25 s tick, so it re-fires **every tick for ~8 ticks** per
  retry window. Fix: compare `>=` with a once-per-episode latch. The
  test passed only because it drove both on the same cadence.
- ⚠ **799 orders with unanswered cancels in one day** is itself the
  finding. The cancel re-arm (also PR #44) will keep re-cancelling
  orders the venue considers dead until the gateway retires `reason=0` +
  `ORDER DEAD` rows. **The owed gateway PR is now load-bearing**, not
  cosmetic.

## 9 · Immediate recovery (not executed — George's call)

1. **Rule IPTCHOUC.** Venue 4467 vs ours 4439. The 14-08 CLEM precedent
   is trust the venue → patch `SNT_FLOAT_OVERRIDES` and resume, or take
   a fresh journal and let the boot rebase adopt it.
2. Taker cutover: halt → stop → CFG bump + fresh journal (**create the
   directory first, `chown georgewestbrook:root`**) → floats → start →
   resume.
3. ⚠ Every restart drops all books to OVERNIGHT until the bus
   re-derives (~30 s). Avoid doing it inside a live game.

## 10 · Recommended order of work

| # | Item | Size | Why first |
|---|---|---|---|
| 1 | Alert on `halted` + snapshot age | hours | Turns 33 h into 60 s; data already published |
| 2 | Halt the book, not the bot | small | Turns a 180-book outage into 1 book |
| 3 | Fix the `CANCEL STUCK` flood | small | Log flood starves the loop (the 08-13 lesson) |
| 4 | **Gateway `oe_adapter.go:474` — stop dropping fills** | medium | **THE root cause.** A fill must never be discarded because a request is in flight; resolve it through the tracker and let the pending request settle on its own ack |
| 4b | Gateway `reason=0` retirement | small | The companion defect — dead orders never retire, so cancels re-fire for ever |
| 5 | Bounded auto-rebase (§6.2–6.4) | medium | The self-heal proper; needs the bounds ruled |
| 6 | Prove the lost message on IPTCHOUC | medium | Confirms the mechanism rather than assuming it |

## 11 · Open questions for George / Edwin

- **The three bounds** in §6.2–6.3 (500 shares · 3 per book · 20
  portfolio) are proposals with no source. They need a ruling.
- **T-S05 is an EDWIN requirement.** Weakening "halt on divergence" to
  "adopt within a bound" is a change to his safety rail and should go to
  him with the evidence in §5, not be made quietly.
- Does the per-book halt need a re-open path, per the standing rule that
  **a suspended book must never be a dead end** (George, 14-08, N40)?
