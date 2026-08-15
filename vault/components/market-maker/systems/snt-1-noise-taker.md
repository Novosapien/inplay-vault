# SNT-1 — the Synthetic Noise Taker (Edwin's "market taker")

> **Component:** [[market-maker/market-maker]] · **Status:** ⭐ BUILT
> 08-08 (MM PR #10, `src/snt/` — agent · pending · journal · runtime;
> 27 tests) — NOT deployed. Production blocked on E32 (mechanics
> rulings) + E33/T13 (compliance) + the IPLP account (Rob). QA can run
> on the MM account, env-only switch. Numbers: the SNT-1 section of
> [[market-maker/parameters]]. **What it must satisfy before it runs:
> [[market-maker/market-taker-requirements]].**
> **Source:** Edwin's email + reference code, filed verbatim in
> [[market-maker/reference/snt1-noise-taker-edwin-2026-07-30|reference]]
> (`snt1_noise_taker.py`). Received at the 30-07b intake; the full
> artifact reached the vault 08-08.
> **Not to confuse with:** [[market-maker/systems/synthetic-market-order]]
> (the app-side "buy at market" button — a different Edwin ask) and
> the **poker** (our throwaway QA tool on the MM VM — SNT-1-shaped in
> spirit, none of its design).

## What Edwin wants, in one paragraph

A second house account that randomly TAKES liquidity — crosses the
MM's spread with small random clips at random times — so every team
book prints real trades from IPO day onward, games or no games. It is
a deliberate, budgeted loser: its spread costs are the subsidy that
makes the secondary market look and feel alive. Its flow is certified
uninformative (50/50 i.i.d. direction), so nobody can read anything
from it, and its prints carry no participant side, so they stay out of
the off-field volume split.

## The design, distilled from the reference

- **Arrivals:** Poisson per team-book. Base 9 orders/hour, scaled by
  activity state (OVERNIGHT ×1 · PRE_KICKOFF ×6 · LIVE ×75 · POST ×4)
  and a per-team popularity weight (0.25–4.0). Nothing schedulable.
- **Sizes:** log-normal, 5–400 shares, median ~30 (~44 average).
- **Order style:** 90% at-touch marketable IOC, capped at half the
  displayed touch quantity; 10% "sweeps" capped at 3 ticks through the
  touch. Taker only — it never posts a resting order.
- **Loss governor:** $100,000 per team per day, metered as fill-vs-mid
  at send (spread subsidy, not marked P&L). ⚠ E32: at LIVE intensity
  it burns ~$1,500/hour, so the governor cannot bind;
  `base_orders_per_hour` is the only real lever.
- **Inventory:** internally tracked position + VWAP basis; a
  1,500-share soft cap with an 80% flatten bias above it.
- **Realism layer (new detail in the full artifact):** a
  disposition-effect profit-take tilt — in unrealized profit,
  P(flatten) rises from 0.50 toward 0.65 (full tilt at 10 ticks of
  profit); losers ride at 50/50. Conditions only on its own basis vs
  mid — no book state, no participant data.
- **Hard guards:** never trades halted, locked/crossed, one-sided, or
  RP-freeze books; never wider than 8 ticks.
- **Integration shape:** we implement a small `ExchangeAdapter`
  (top_of_book · activity_state · send_marketable_ioc · position) and
  drive `agent.step()` from an event loop. Seeded RNG throughout.
- **His hardening list for us:** kill switch + per-order notional cap ·
  persist pos/basis across restarts · periodic position reconciliation
  (halt the book on divergence) · the IOC limit is the real impact cap
  (a stale TOB snapshot is fine if the engine honors the limit) ·
  activity-state mapping for off-season and IPO windows.

## The venue-reality mapping (what the adapter must absorb)

The reference assumes an idealized matching engine. The recorded venue
facts change almost every interface point:

| Edwin assumes | tZERO reality | Consequence |
|---|---|---|
| Marketable IOC | No IOC — DAY/GTC/GTD only (verified twice; E32) | The adapter fakes IOC: marketable DAY + immediate cancel. Doubles the message count and CAN momentarily rest — the "never posts" guarantee needs re-wording with Edwin |
| `send_marketable_ioc` returns `Fill | None` synchronously | Async acks/fills over NATS; rejects are a first-class outcome | The adapter must correlate acks and surface REJECTS — in the reference a rejection is indistinguishable from "no fill" and the agent silently degrades (E32) |
| `max_spread_ticks_to_trade = 8` | Our narrowest spread is $0.10 = 10 ticks (§5.2 Stable) | As configured SNT-1 never trades at all. Config change, with Edwin (E32) |
| SELL from any state | Side-2 sells require inventory; side-5 shorts work from flat but the short reserve is 1,000/security (venue facts 07-08b) | The 1,500 soft cap exceeds the short reserve; SNT-1 needs seeded inventory (position-transfer, as we did for the MM) or an Edwin ruling on shorts (ties E26/E27) |
| Account flags `HOUSE_SYNTHETIC` / `leaderboard_eligible` / `participant_side` | Platform-side concepts, not tZERO's. tZERO's identity is the account + MPID | A second house account; Rob's **IPLP** MPID slot is reserved for exactly this (decisions 07-08g). The flags live in OUR platform layer |
| `top_of_book()` | `market.quote` is a partial-update contract; `market.book` can serve a stale book under churn (evidence 08-08) | Aim from `market.book` with a staleness gate on `source_timestamp` — Edwin's hardening point 4 covers the rest (the limit caps the damage) |
| `rp_freeze` windows | RPV is unadopted (E30: "build none of it" pending his answer) | The guard is a no-op for us unless RPV ships |
| `position()` reconciliation | Tag 9383 on executions + our journal | We already have the machinery; his "halt on divergence" matches our quarantine philosophy |

## The two real blockers (unchanged by the artifact)

1. **E32 — mechanics.** The four rows above marked E32. It cannot run
   as written; every one needs either an adapter workaround or an
   Edwin config ruling.
2. **E33/T13 — compliance.** On day one the MM holds most of every
   float, so SNT-1's counterparty is overwhelmingly the MM: two house
   accounts trading with each other on a FINRA-regulated ATS. The
   self-cross half is verified permissive for the MM account; the
   CROSS-account half (does tZERO relate two house accounts?) is open
   with Rob, and the compliance read (Troy + InPlay legal) is not an
   engineering call. **Nothing ships before this clears.**

## Relation to the poker

The poker proves the plumbing an SNT-1 adapter needs: NATS order path
with account + identity, book reading, cancel discipline, fill
tracking. It is NOT SNT-1: one account (the MM's own — the E33 optics
inverted), fixed 1,000 clips, biased streaks (deliberately informative
to exercise the MM's skew), no governor, no guards, 60-minute
lifespan. Treat it as the walking skeleton of the adapter, not an
early version of the agent.

## Build shape, if green-lit

Its own small service (not inside the MM engine — single-writer
journal, and E33 wants clean account separation), on its own account
with the IPLP MPID, talking to the gateway over the same NATS order
subjects the poker uses. Own journal for pos/basis persistence
(hardening point 2). Determinism discipline as per the house rule:
seeded RNG is already in the reference; keep the wall-clock scheduling
out of anything that must replay.

## ⭐ The ops surface (built 12-08b — spec R2/R3 of the observability spec)

The taker gained the panel's two hooks. Neither touches the trading
path: the agent, the sell gate, the tilt and the loss governor consume
exactly what they did before.

**The state snapshot — `snt.state.snt-1` (`snt/state.py`).** A complete
projection every ~1 s from its OWN asyncio task, so **a halted bot keeps
publishing** — the IPO cockpit case, where an operator places orders by
hand into a bot that is deliberately not trading. Publishing stops only
when the process dies, which is itself the signal (read off the
snapshot's age). Every configured book, keyed by full venue symbol.
Fields: `v · ts_ms · config_id · activity_state · halted · boot_ts_ms ·
journal_dir · guards{max_qty,max_notional,collar_pct} · books{SYM} ·
open_orders[]`.

- **`avg_cost` and `realized_pnl_total` are new** (`snt/pnl.py`), folded
  through `mm.position.position.apply_execution` — the maker's §4.2
  algebra, not a second implementation. They cover **traded drift
  (`pos`) only, never `holding`**: the float's cost per share is 🔴
  UNKNOWN (E39), and inventing a basis for the IPO allocation to make a
  screen look complete is exactly what §2.3 forbids.
- **`basis` and `avg_cost` are published together on purpose.** `basis`
  is the algo's own instrument (it feeds the disposition tilt and must
  keep behaving as Edwin's reference does); `avg_cost` is the reported
  number. The two agreeing is evidence both fold paths are whole.
- **`open_orders[]` is NEW tracking, not a rename.** `PendingOrder` held
  no limit price, no leaves, no cum and no state, because the IOC
  substitute never needed them — it cancels the remainder after 1.5 s
  regardless of progress. A terminal order now moves to a SECOND map and
  lingers 60 s for the screen; the trading path reads only the live map,
  so `live_fix_qty` can never count a filled sell against the venue's
  bound.
- ⭐ **TWO activity states, and they must never be merged** (N36, ruled
  12-08b). Top level = the OPERATOR-level setting: the pin, or `AUTO` —
  what a human chose. Per book, inside `books{SYM}` = the DERIVED T-F07
  state — what the engine is doing there. Bot-level alone cannot
  distinguish "deliberately not trading this book" from "something is
  wrong with this book"; per-book alone hides whether a human has
  pinned it.

**Manual orders (`snt/runtime.py`).** `{cmd:"order", action:
place|cancel|replace, ref, …}` on `snt.control.snt-1`, replied to on
`snt.control.snt-1.reply.{ref}`. Accepted while halted. The engine mints
the ClOrdID (MMSN prefix) off its own send sequence, journals the send
flagged `manual` with its ref, and submits through its own venue path —
never a proxy publishing to `gateway.orders.*`, which is what keeps the
journal whole, the float arithmetic true, and the 08-09 hijack (an
engine adopting and re-pricing a foreign order on its own userId)
impossible.

- **The maker is excluded structurally, not by a check.** No maker
  control subject exists on the wire and the command carries no account
  field. There is nothing to aim at one.
- **Guards** (engine-enforced, env-tunable, mirrored to the panel through
  `guards`): 10,000 shares ✅ · ±20% collar ✅ · $500k notional 🟡. The
  collar's reference falls back book mid → last trade → **skip**; the
  skip is load-bearing, because the halted-IPO case often has no book and
  a collar that refused an order for want of a reference would block the
  very trade the feature exists for. Skipping disables the COLLAR only.
- ⭐ **A manual order is only real once the publish reached the wire, and
  there are THREE outcomes because two would be a lie** (12-08d, after
  the adversarial review). CONFIRMED — the publish returned and a flush
  round trip came back clean on a connection that stayed up. REFUSED —
  `publish()` raised while connected, or the server refused a publish to
  the subject we sent on, attributed by SUBJECT because `last_error` is
  connection-global. UNCONFIRMED — everything else, tracked as `unknown`
  (§8.2's own word) because the bytes may yet arrive. The journal write
  still comes FIRST: believing we may have sent something we did not is
  recoverable; believing we did not send something the venue has is not.
- **A manual fill counts into pos/holding/float drift** — the 08-11
  invariant (float = env float + journalled drift) has to keep holding
  or T-S05 halts the book — but **never into `session_loss`**, live or on
  replay. `session_loss` stays a pure meter of the ALGO's noise cost; an
  operator buying 600,000 IPO shares by hand would otherwise blow the
  day's budget and silence a bot that had done nothing.
- **Replace is cancel-then-new, not atomic.** The taker has no replace
  path of its own and the atomic lane is the maker's. The cost is queue
  priority and a brief unrested window; the place leg re-runs the guards
  against the submission-time reference. If it is rejected the operator
  has NO order and the reply says so — the engine does not restore the
  original.
- **Dedup and resting manual orders survive a restart.** Every reply is
  journaled, so a resend re-publishes the SAME answer with the same
  ClOrdID; placed-minus-ended is re-adopted at boot as manual. Retention
  is the journal directory, which the ops rules rotate per deploy.

⛔ **Deploy gate:** the `snt-taker` NATS user needs publish on
`snt.state.>` and `snt.control.snt-1.reply.>`. A missing grant is silent.

## Open with Edwin (for the next round)

- The E32 config/mechanics rulings (IOC substitute wording · spread
  threshold vs §5.2 · short handling vs the 1,000 reserve).
- Whether the profit-take tilt survives the compliance read — it makes
  the "certified uninformative" claim weaker than 50/50 i.i.d. (the
  flow now conditions on its own P&L, which correlates with price
  direction).
- His own open question back to us: how SNT-1 interacts with the MM's
  quoting and Primary-Mandate inventory.
