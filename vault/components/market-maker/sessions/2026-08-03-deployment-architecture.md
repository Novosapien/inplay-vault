# 2026-08-03 — deployment architecture: where the machine runs

> **Who:** George + Claude
> **Type:** design session (no code)
> **Refs:** N7 · N19 · N23 · `vault/drafts/VPC Setup.md` · the 02-08 wire test

## What we did

Settled how the market maker is deployed, where its data lives, and how
the MM panel reads it. No code changed. The session answers **N7** and
adds the runtime clock model that `mm/runtime/` will implement.

## What we learned

- **The handover's premise was wrong.** NATS does not run on the gateway
  VM. Per `VPC Setup.md`: FIX gateway `10.0.0.2` (static public IP,
  tZERO-whitelisted) · NATS JetStream `10.0.0.3` (no public IP) ·
  Centrifugo `10.0.0.4`. All sit in `inplay-subnet` (`10.0.0.0/24`,
  us-east4). Inter-VM latency is under 1 ms. So "co-locate on the trading
  VM" means a **third VM in the same subnet**, not a process on the
  gateway.
- ⚠ **The MM VM needs Cloud NAT.** The poller calls Sportradar over the
  public internet. A `--no-address` VM reaches GCP APIs through Private
  Google Access, but it cannot reach `api.sportradar.com`.
  `VPC Setup.md:660` documents Cloud NAT as the fix and marks it as not
  yet created. Confirm with Hasan before the MM VM exists.
- **The engine reads no wall clock.** `[clock-stays-put]` in
  `orchestration/engine.py`: every cycle's `at` comes from the triggering
  envelope. `[ages]`: §3.3's ages are differences of event timestamps.
  Replay equality rests on this, not on §7.3's type list. A clock-driven
  sweep therefore has no legal `at` — which is the real §3.1.4 problem.
- **Outbound venue instructions are not journalled.** The journal holds
  accepted inbound events only; `Orchestrator.replay()` re-runs those
  through fresh engines. So a book change with no event behind it cannot
  be reproduced.
- **The file is small.** Edwin's daily file is roughly 50–100 KB, about
  18 MB per season. Size is not an argument for a bucket. §10.4 is.

## Decisions *(mirrored into decisions.md 03-08)*

Own VM at `10.0.0.5` · auto-restart with a rate limit · journal on a
dedicated persistent disk with hourly snapshots · the file to the bucket
and the parsed rows to the database · the panel never reads the journal ·
the sweep scheduler is a producer outside the deterministic core.

## What went wrong

Nothing broke. One prose correction: the first pass of this design was
written outside ASD-STE100 and George asked for it again in the standard.

## Questions

- **N7 resolved** — one stateful engine plus one stateless panel, joined
  by NATS.
- **N19 half-resolved** — the store is the bucket. Who puts the file
  there at 06:00 ET, until the upload page exists, is still open.
- **N28 opened** — the §3.1.4 sweep needs a tenth event type. Same class
  as N23; ask both together.
- **N29 opened** — does the MM panel live in the existing admin panel, or
  in a new desktop app shell?

## Next

1. **George's call on N29** — it decides whether the panel is days or
   weeks of work.
2. **Build `mm/runtime/`** — the three clocks below, once N28 has a
   provisional event type.
3. Ask N28 + N23 as one question in the Edwin round (E29–E37, still
   unsent).

---

## Addendum — how the machine actually runs: the three clocks

The engine is event-driven. A book updates when an accepted fact
arrives, never on a timer (§5.8 forbids republishing without material
change). So "every 200 ms" and "every 4–5 s" are not one loop speed.
They are three separate clocks the runtime owns.

### 1 · The heartbeat tick — 1 s, fixed, unconditional

The loop's base rate. On every tick, in order:

1. `beat()` — the gateway sweeps our book after 4 s of silence.
2. Drain inbound order events.
3. Run whatever else is due.

This is already the poller's shape.

### 2 · The input poll scheduler — per game, tiered

Tiered by the activity axis already derived per security (LIVE ·
PRE_KICKOFF · POST_GAME · OVERNIGHT).

| Situation | SR poll | Why |
|---|---|---|
| LIVE game | ~2 s per game | E18's evidenced rate. SR's median update gap is 4 s, so a 200 ms poll re-reads unchanged values |
| PRE_KICKOFF (≤ 1 h) | ~10–30 s | Lines move before kickoff. The number is a CONFIGURED interim to add |
| POST_GAME / OVERNIGHT | None — daily schedule discovery only | The price rides T and off-field |
| Earnings window (Tue/Wed ~07:30) | Edwin's daily file → burst-evaluate all 170 | The 23-07 ruling. The file is the input |

**Load check.** The worst case is an NCAA Saturday: 30–40 live games →
15–20 SR calls per second. That is the S7 quota ask. Engine compute is
about 2 ms per reading. The ceiling is venue messages (T2's
`MaxOrdRate`), never CPU.

### 3 · The §3.1.4 sweep — 2.0 s per security — UNBUILT

This is what makes "it runs every 2 s" true when no event arrives. A
per-security evaluation pulse. It ages freshness (missed-sweep
counting), advances market-state promotions on quiet books, and lets the
reconciler heal stale levels. Without it, a quiet book re-evaluates only
when something happens to it — the known "quiet books climb late" gap.

**The replay problem, and its resolution.** A sweep is clock-driven and
§7.3 defines no sweep type. The constraint is tighter than that: the
orchestrator reads no wall clock, so a sweep has no legal `at`.
Constraining sweeps to demotions does not help, because a demotion
changes the book as surely as a promotion.

**Resolution (ours, 03-08):** the sweep scheduler is a **producer**,
outside the deterministic core, beside the poller. It emits a journalled
event and the engine stays purely event-driven. Replay consumes the
emitted events and never re-runs the scheduler — the same relationship
the poller already has.

To control volume, the scheduler **emits on effect, not on tick**. It
ticks at 2.0 s in memory and journals only when a sweep would change
something. 170 securities at 0.5/s would otherwise write 85 events per
second, and §10.4 says keep them all.

Open: the tenth event type and its name → **N28**. Basis
`security_id + scheduled_time`, which deduplicates for free.

### Where 200 ms fits

It is a reaction bound, not a timer. An accepted reading reaches a
published book in single-digit milliseconds in process, measured on the
real-game tests. The 200 ms budget is spent waiting for SR's feed, not
for us.

⚠ If Edwin's E18 answer is "I want the book visibly churning sub-second
with no new information", that is a §5.8 change order plus a T2
prerequisite. It is a different machine, priced accordingly. That is
why the E18 ask is phrased the way it is.

### SOP summary

One process. One asyncio loop. A 1 s tick: beat → drain → due polls →
due sweeps. Discovery runs daily. Edwin's file is watched at 06:00 ET.
Boot order is heartbeat before reconcile. The kill switch is a
`MANUAL_CONTROL` event first, and the gateway's `cancel_all` second.
