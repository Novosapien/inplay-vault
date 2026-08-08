# SNT-1 — the Synthetic Noise Taker (Edwin's "market taker")

> **Component:** [[market-maker/market-maker]] · **Status:** ⭐ BUILT
> 08-08 (MM PR #10, `src/snt/` — agent · pending · journal · runtime;
> 27 tests) — NOT deployed. Production blocked on E32 (mechanics
> rulings) + E33/T13 (compliance) + the IPLP account (Rob). QA can run
> on the MM account, env-only switch. Numbers: the SNT-1 section of
> [[market-maker/parameters]].
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

## Open with Edwin (for the next round)

- The E32 config/mechanics rulings (IOC substitute wording · spread
  threshold vs §5.2 · short handling vs the 1,000 reserve).
- Whether the profit-take tilt survives the compliance read — it makes
  the "certified uninformative" claim weaker than 50/50 i.i.d. (the
  flow now conditions on its own P&L, which correlates with price
  direction).
- His own open question back to us: how SNT-1 interacts with the MM's
  quoting and Primary-Mandate inventory.
