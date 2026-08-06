# Market Maker Bot — Build Guide (Hasan, 2026-08-05)

> **Provenance:** written by Hasan for the MM engineer; "everything here
> was verified on the live venue session today" (05-08). Received from
> George 06-08. Filed VERBATIM below the rule.
> **The 22-07 filter applies:** venue and gateway facts here are GOSPEL
> (live-verified). The bot-design suggestions (§13's shape, the 200 ms
> full re-anchor budget, the ClOrdID cycle-encoding idea) are SUGGESTIONS
> — our from-scratch design adopts or replaces each explicitly.
> **Intake:** decisions.md 2026-08-06c carries what this supersedes and
> the two design conflicts it surfaces (wash-trade vs N12 · the tick-tied
> heartbeat). Do not act on this document without reading that entry.

---

Market Maker Bot — Build Guide
For: the engineer building the InPlay market-maker bot As of: 2026-08-05. Everything here was verified on the live venue session today. Self-contained. You should not need to read any other document to start building.

1 · What you are building
An order-based market maker for InPlay's trading simulator, quoting on tZERO's ATS.

tZERO has no quote or mass-quote interface — there is no MassQuote message in their FIX schema. So a market maker here does not "publish quotes". It expresses its ladder as resting limit orders on tZERO's book and continuously re-prices them.

Your bot's output is therefore a diff: given a target ladder and your current resting orders, emit New (D) / Cancel (F) / Cancel-Replace (G) to close the gap. Prefer G over cancel-then-new — it halves message rate and avoids a naked no-quote window.

You do not touch FIX. You publish JSON to NATS. A Go gateway owns the FIX session, builds the wire messages, tracks order state, and publishes results back to NATS. Your entire interface is NATS subjects and JSON payloads.

your bot ──JSON/NATS──▶ FIX gateway ──FIX 4.2──▶ tZERO ATS
   ▲                    (VM 10.0.1.2)
   └──── order.{userId}.{clOrdId} ────┘
Scope note: this is a simulator. Capital is notional — the MM account is funded with $1bn precisely because it is not real money.

2 · Connection
NATS    nats://10.0.2.2:4222 — in-VPC only, not reachable from the internet
User    market-maker
Password    Secret Manager: inplay-nats-mm-token (project inplay-497712)
gcloud secrets versions access latest --secret=inplay-nats-mm-token --project=inplay-497712
Your credential is scoped and enforced. You can publish only to gateway.orders.mm.>, and subscribe only to order.>, position.>, market.>, _INBOX.>. Attempting anything else is a permissions violation, not a silent no-op.

Every NATS user was moved to its own password on 2026-08-05. If you see auth failures, note that Secret Manager values must be read without a trailing newline — that exact mistake broke three services earlier today.

3 · Subjects
You publish:

Subject    Purpose
gateway.orders.mm.new    New order (35=D)
gateway.orders.mm.cancel    Cancel (35=F)
gateway.orders.mm.replace    Cancel/Replace (35=G)
gateway.orders.mm.heartbeat    Liveness — mandatory, see §6
gateway.orders.mm.cancel_all    Panic sweep / clean shutdown
You subscribe:

Subject    Content
order.{userId}.{clOrdId}    Every result for that order — accept, fill, cancel, reject
position.{userId}    Position updates
market.snapshot.{symbol} · market.quote.{symbol} · market.trade.{symbol} · market.status.{symbol}    Venue market data
These are a separate queue group (gw-orders-mm) from the retail path, so your quote churn cannot starve user order intake.

4 · Wire contracts
Field names are exact — taken from the gateway's Go structs. Extra fields are ignored; missing required ones get you a reject.

New order → gateway.orders.mm.new
{
  "userId": "384925384799470102",
  "symbol": "IPTCCOWB",
  "side": 1,
  "quantity": 100,
  "price": 25.00,
  "clOrdId": "MM1c04a7",
  "account": "1797733477",
  "walletAddress": "",
  "timeInForce": 0,
  "expireTime": "",
  "botId": "mm-1"
}
Field    Notes
userId    Your bot's identity key. Determines the reply subject order.{userId}.{clOrdId}
symbol    See §8
side    1 buy · 2 sell · 5 sell short
quantity    Integer, > 0
price    Float. Limit only — tZERO has no market orders on this path
clOrdId    ≤20 chars, must start MM, no leading zeros. See §5
account    1797733477 — becomes FIX Tag 1
walletAddress    Optional. On-chain settlement address (Tag 9829). Omit unless told otherwise
timeInForce    0 DAY · 1 GTC · 3 IOC · 4 FOK · 6 GTD. Use 0 — see §8
expireTime    RFC 3339. Required only for GTD (6)
botId    Yours. Carried end-to-end; used by the dead-man switch
Cancel → gateway.orders.mm.cancel
{ "userId": "...", "clOrdId": "MM1c04a8", "origClOrdId": "MM1c04a7" }
clOrdId is a fresh id for the cancel request itself; origClOrdId is the order being cancelled. FIX 4.2 requires this chaining.

Replace → gateway.orders.mm.replace
{ "userId": "...", "clOrdId": "MM1c04a9", "origClOrdId": "MM1c04a7",
  "quantity": 150, "price": 25.50, "timeInForce": 0 }
Omit timeInForce to inherit the original's.

Heartbeat → gateway.orders.mm.heartbeat
{ "botId": "mm-1" }
Cancel-all → gateway.orders.mm.cancel_all
{ "botId": "mm-1", "reason": "clean shutdown" }
Explicitly does not latch the dead-man — a clean shutdown that later resumes heartbeating just carries on.

5 · ClOrdID rules — get these wrong and nothing works
Must start with MM. The gateway enforces the namespace by prefix. An MM order without it is rejected MM_PREFIX_REQUIRED. Conversely the retail path now rejects any MM-prefixed id with MM_PREFIX_RESERVED, so the prefix is genuinely reserved for you.
Maximum 20 characters.
No leading zeros (after the MM, the id must not begin 0).
Must be unique per request — including cancels and replaces, each of which needs its own fresh id.
Encode cycle and level into it. You will want to reconstruct "which re-quote cycle and which ladder level was this" from logs and replay. Something like MM{cycle36}{side}{level} works.

6 · The dead-man switch — read this before you write the main loop
A dead MM bot leaves stale quotes resting on tZERO until 23:59 ET. tZERO applies no cancel-on-disconnect (probe-verified), and FIX 4.2 has no mass-cancel. So the gateway enforces cleanup itself.

Contract:

Publish gateway.orders.mm.heartbeat every ~200ms.
If 4 seconds pass with no heartbeat, the gateway cancels every resting MM order and fires an ops alert.
It latches after firing — one sweep per outage, not one every 4s. A fresh heartbeat re-arms it.
Boot grace 30s: if the gateway restarts holding rehydrated MM orders, it waits 30s for you to reconnect before sweeping.
It only arms once it has something to protect (a heartbeat seen, or MM orders rehydrated at boot), so a gateway running with no bot does not fire against an empty book.
Practical consequence: your heartbeat must be on an independent timer, not tied to your quoting cycle. If your decision loop blocks for 4s — a slow feed, a GC pause, a synchronous DB call — your entire ladder gets cancelled.

Current config: MM_DEADMAN_TIMEOUT_MS=4000, MM_DEADMAN_BOOT_GRACE_MS=30000.

7 · Rate limits and your budget
The governor rejects; it does not queue. Exceed it and the order comes back RATE_LIMITED immediately. This is deliberate — for a market maker a stale quote is worse than a refused one. Do not build retry logic that assumes queuing.

Layer    Limit
Gateway MM governor    5,000 msg/s, burst 2,000
tZERO MaxOrdRate on the account    5,000/s
tZERO MaxDupOrdRate    200/s
Gateway raw capacity    ~460k orders/s/core — not your constraint
Budget math for 10 levels/side:

20 orders per team (10 bid + 10 ask)
× 5 cycles/s (200 ms cycle)
= 100 msg/s per live team
× 34 teams (17 concurrent games max)
= 3,400 msg/s peak
That is a worst case assuming every live team fully re-anchors every cycle. Headroom to the 5,000 governor is ~47%, good to about 25 concurrent games.

MaxDupOrdRate matters more than it looks. tZERO counts "duplicate" as same symbol + side + order type. Ten levels on one symbol-side per cycle is ~50/s — the platform default of 20/s would have clipped you, which is why it is raised to 200.

Prefer G (replace) over F+D: it halves your rate and avoids a window where you have no quote at that level.

8 · The venue — facts you need
Symbols    170 — 32 NFL + 138 NCAA. Only 6 are quoted two-sided in QA; 164 books are empty
Tick    $0.01
Order types    Limit only. No market orders
Time in force    DAY today. GTC pending. IOC/FOK unavailable
Session reset    23:59 ET daily — all resting orders expire. Sequence numbers reset automatically
Cancel on disconnect    None. Verified: a resting order survived a hard restart
Price bands at acceptance    Limits at $0.01 and $1,000,000 both rested verbatim (verified 2026-07-17). A later risk matrix says passive bands are ON — unreconciled, so do not rely on the venue to catch a bad price
Self-collar    Mandatory and yours. Nothing protects you from your own mispricing
Price cap / floor    $127.50 / 1 tick (client sheet)
Shorts    side 5. 1,000-share reserve per security, pre-trade enforced. Stock-loan fee per short execution
Matching    Price-time at tZERO. You never match internally — users cross against your resting orders
Capacity    Orders print as 47=A Agency. Known; not a problem for the simulator
Route    100=STX
Empty books are the normal case. 164 of 170 symbols have no other participants, so your resting orders are the book. That also means a marketable order can print at any resting price — another reason the self-collar is on you.

9 · The account — already configured
tZERO account 1797733477. Put this in the account field of every order.

Setting    Value    Status
Cash (CASHo)    $1,000,000,000    ✅ verified applied
Day-trading buying power (DTBPo)    $1,000,000,000    ✅ verified — a $125k order cleared
Margin multiple (DTMult)    1 (cash-equivalent)    set
MaxOrdRate    5,000/s    set
MaxDupOrdRate    200/s    set
Max open orders    uncapped    platform default
Position    0 on every symbol    ✅ verified
Capacity    Agency (47=A)    accepted as-is
Wash-trade blocking    ON    ⚠ see §11
One quirk to budget for: the buying-power check charges more than notional. A $25.00 × 1 buy was checked as Cost(26.20) — about a 4.8% buffer. At 170 symbols × 10 levels that compounds, so do not size against raw notional.

Account oddity, harmless: this account exists in tZERO's OMS but returns 404 from their REST API — an artifact of how it was created. Everything you need (orders, risk config, inventory) is OMS-side and works. Ignore the REST gap.

10 · Inventory — the biggest trap in this system
Offers need real inventory. You cannot quote a two-sided market from an empty position. The 1,000-share short reserve is explicitly not a substitute.

Seeding is not over NATS. It is an HTTP call to the gateway:

curl -XPOST http://10.0.1.2:8080/position-transfer \
  -H 'Content-Type: application/json' \
  -d '{"account":"1797733477","symbol":"IPTCCOWB",
       "txfrQty":1000,"txfrCost":25000.00,"confirmTyp":2}'
Constraints: txfrQty non-zero; txfrCost must share its sign; and txfrCost / txfrQty must be > 0.

Three properties that will hurt you
It is ONE-WAY. Positive transfers apply. Negative transfers are accepted (UPTa) and then silently do nothing — tested twice, with and without confirmTyp. You can add inventory; you cannot remove it. Reducing means selling in the market.
It is NOT idempotent. Each call is an independent signed delta. Two calls of +1 give you +2. confirmTyp does not sequence one transfer into two steps — that was tested and disproven.
There is no position read-back. The only way to read a position is Tag 9383 on an ExecutionReport, i.e. by placing an order.
Therefore: build a ClOrdID ledger before you seed anything at scale. A timeout-and-retry silently double-seeds and you cannot see that it happened. This already bit us at 1-share scale; at 170 symbols it would be unrecoverable without a record.

11 · Known conflicts and unfinished business
Wash-trade blocking vs your re-quote design. tZERO's Stop Wash Trades is ON, and it rejects orders that cross your own resting orders. Decision N12 says v1 posts new quotes without waiting for cancel confirmations, accepting a momentary self-cross. These are incompatible as configured. Either the flag gets turned off or the re-quote path waits. Raise it before you finalise your diff engine — it changes the design.

The reference price does not exist yet. Your quoting engine needs a fair price (RP = ESV, InPlay-sourced). The RP / MOC / MOP / lifecycle NATS streams are specified but have no producers. Fills work today; that is the only live input. You will need a stub RP source to develop against.

Parameters not yet decided (blocked on Edwin, not on the platform):

Level size and randomisation bounds — you cannot size a ladder without these
λ (inventory sensitivity) base value
The float denominator: 875,000 vs 5,000,000 — shifts effective inventory gain by ~5.7×
Randomisation applies to quantities only. Price is never randomised.

12 · Order lifecycle and rejects
Every result for an order arrives on order.{userId}.{clOrdId}.

Rejection reasons you will actually see:

Reason    Meaning
MM_PREFIX_REQUIRED    ClOrdID didn't start with MM on an MM subject
MM_PREFIX_RESERVED    An MM id was used on the retail path
NOT_MM_ORDER    You tried to cancel/replace an order that isn't yours
RATE_LIMITED    Governor refused it. Not queued — resend or drop
SESSION_DOWN    FIX session to tZERO is down
FAILSRISK[...]    tZERO risk check. Text explains, e.g. Cost(26.20) exceeds DTBP(0.00)
State machine: only orders in ACCEPTED or PARTIALLY_FILLED are cancelable or replaceable. The gateway rejects anything else locally without troubling the venue.

Partial fills rest until completely gone — no top-ups, no aging. On a price move, cancel the old level and post the remaining quantity at the new price. After a full fill at an unchanged price, reload at top of book.

Replace semantics: an updated order goes to the back of the queue at tZERO. That is standard for matching engines and has been accepted as fine.

13 · Suggested shape
┌─ heartbeat timer (200ms, INDEPENDENT thread) ──▶ mm.heartbeat
│
├─ event ingest ── fills (order.>) ─┐
│                  market data ─────┤
│                  RP feed (TODO) ──┤
│                                   ▼
│                          in-memory state
│                     (positions, resting orders, RP)
│                                   │
│                                   ▼
├─ decision cycle (200ms per team) ─▶ target ladder
│                                   │
│                                   ▼
│                          diff vs resting orders
│                     (only levels that moved ≥ 1 tick)
│                                   │
│                                   ▼
└──────────────────────────▶ D / F / G to mm.{new,cancel,replace}
Principles worth adopting from day one:

Determinism. Seeded randomness only, no wall clocks in logic, event-sourced state. Cheap now, brutal to retrofit.
Never read a database in the loop. Everything arrives pushed and lives in memory.
Emit only the diff. Only levels that moved ≥ 1 tick. A full re-anchor every cycle is the worst-case rate, not the operating rate.
Own the collar. Check every price against your own bounds before publishing. Nothing downstream will save you.

14 · Quick reference
NATS          nats://10.0.2.2:4222   user: market-maker
Secret        inplay-nats-mm-token   (project inplay-497712)
Publish       gateway.orders.mm.{new,cancel,replace,heartbeat,cancel_all}
Subscribe     order.>  position.>  market.>
Replies       order.{userId}.{clOrdId}

Account       1797733477      $1bn cash + DTBP
Rate          5,000 msg/s, burst 2,000 — REJECTS, never queues
Heartbeat     every 200ms — 4s silence cancels your entire book
ClOrdID       starts "MM", ≤20 chars, no leading zeros, unique per request
Side          1=buy  2=sell  5=short
TIF           0=DAY (use this)  1=GTC  3=IOC  4=FOK  6=GTD

Gateway HTTP  10.0.1.2:8080   /health  /logs  /position-transfer
Inventory     one-way, non-idempotent, no read-back — keep a ledger
Session       resting orders die 23:59 ET
Ask before you build around them: the wash-trade conflict (§11), and where your RP feed comes from. Both change the design.
