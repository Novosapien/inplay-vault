# Synthetic Noise Taker (SNT-1)

> **Component:** [[market-maker/market-maker]]
> **Status:** Reference implementation v1.0 delivered by Edwin (2026-07-30). Spec-quality Python; our side is the `ExchangeAdapter` + production hardening.
> **Owner:** Edwin (design) / George + Novosapien (implementation)
> **Source:** email from Edwin, 30-07-2026; reference code safe-copied to `sources/snt1_noise_taker.py` (~349 lines).
> **Reading order:** this sits alongside the [[market-maker/systems/quoting-engine|Quoting Engine (SDMM)]]; both are house agents on the secondary plane. Read [[market-maker/working-guide]] first.

---

## What it is

SNT-1 is a **second house agent** for the Challenge, alongside the Market Maker. It is a **non-participant house account that consumes liquidity**: it crosses the bid/ask with random sizes at random times so **every team book shows real trading action from IPO onward, including when no games are being played.**

Where the MM **posts** resting liquidity (maker), SNT-1 only **takes** it (taker-only, never posts). The two are complementary: the MM makes the market, SNT-1 trades against it (and against users) so the book is never dead.

## Why it exists (the problem)

A brand-new exchange with real books but few users looks empty, which kills the very engagement the Challenge needs. SNT-1 manufactures **realistic, exploitable noise flow** so the secondary market feels alive from day one.

It is **deliberately a controlled loser**: its spread costs (it crosses the spread, so it pays it) are the **subsidy that seeds an active secondary market**. It is not trying to move price toward any target; the flow is pure noise, uninformative by design.

- It **never earns leaderboard credit** (`leaderboard_eligible = false`).
- Its prints **against the MM carry zero participant sides**, so they are **excluded from the $2.50 off-field volume split** under the existing **>= 1-participant-side rule** (see [[earnings-report/earnings-report]]). Edwin: no spec amendment needed there.

## Design (v1.0)

Every number below is in [[market-maker/parameters]] with a status. All randomness flows through one seeded RNG for reproducible sims (determinism, per the working-guide ground rules).

- **Arrivals:** a **Poisson process** (exponential inter-arrivals), re-sampled each trade so intensity changes take effect fast. Nothing schedulable or front-runnable.
- **Sizes:** **log-normal**, clipped to **5 to 400 shares** (median ~30).
- **Direction:** **50/50 i.i.d.** (pure noise).
- **Order style:** **~90% at-touch marketable IOC** (sized to at most **50% of displayed touch qty** so it does not exhaust a level); **~10% sweeps**, whose limit is **hard-capped at 3 ticks through the touch**. Nothing ever crosses deeper than that cap.
- **Intensity:** `rate = base_orders_per_hour x state_multiplier x team_weight`. Base **9 orders/hr** per weight-1.0 team in OVERNIGHT; multipliers OVERNIGHT 1x, PRE_KICKOFF 6x, **LIVE 75x**, POST 4x. Per-team `team_weight` (0.25 to 4.0) is fed from the **EAV / popularity model** (the same popularity index behind valuation).
- **Loss governor:** a **per-team daily loss budget of $100,000**, metered as **cost-vs-mid-at-send** (this meters **spread subsidy, not marked P&L**). When a book hits its budget, SNT-1 goes quiet on that book until the next session.
- **Realism layer, disposition-effect profit-taking:** when its tracked position is in **unrealized profit**, `P(flatten)` tilts from 0.50 up to a **0.65 ceiling** (full tilt at **10 ticks** of profit per share). **Losers ride at 50/50** (no tilt) until the **1,500-share inventory soft cap** kicks in (then **80% flatten bias**). It conditions **only on its own cost basis vs mid**, never on book state or participant data, so it supplies contrarian liquidity into moves without being informed flow.
- **Hard guards:** never trades a **halted**, **locked/crossed**, or **one-sided** book; never during an **RP re-anchor freeze** window; never when the spread is **wider than 8 ticks**; **taker-only** (never posts resting liquidity).

## Integration (our side)

SNT-1 is engine-agnostic: it drives through a thin **`ExchangeAdapter`** interface that Novosapien implements against tZERO's matching engine (see [[tzero]]). One `NoiseTakerAgent` per league (or one global; it is team-keyed internally). Drive `agent.step(now)` from the event loop.

`ExchangeAdapter` methods to implement:

| Method | Purpose |
|--------|---------|
| `top_of_book(team_id)` | Current TOB: bid/ask px + qty, `halted`, `rp_freeze` |
| `activity_state(team_id)` | OVERNIGHT / PRE_KICKOFF / LIVE / POST |
| `send_marketable_ioc(team_id, side, qty, limit_px)` | Marketable limit, IOC; returns the (possibly partial) fill or None |
| `position(team_id)` | Signed SNT-1 inventory per the engine's books, **reconciliation only, never on the trading path** |

**Account flags required on the gateway:** `account_type = HOUSE_SYNTHETIC`; `leaderboard_eligible = false`; `participant_side = false` (the last drives the off-field volume exclusion above).

**`activity_state()` mapping (minimum):** off-season / overnight -> OVERNIGHT; IPO windows -> PRE_KICKOFF at minimum.

## Production hardening (our side, from Edwin)

1. **Kill switch + logging + per-order notional cap** on the SNT-1 account.
2. **Persist pos/basis across restarts** (otherwise the profit tilt resets to flat).
3. **Periodic reconciliation** of the agent's internal position vs the engine's books; **on divergence, halt the book.** Internal tracking is the source of truth on the trading path; `position()` is reconciliation-only.
4. **IOC limit enforcement is the real impact cap**, the agent's TOB snapshot can be stale by send time, which is fine as long as the engine honours the limit.
5. **`activity_state()` mapping** as above.

## Interaction with the Market Maker

Most SNT-1 prints will be **against the MM's resting quotes**, so SNT-1's spread cost is largely the MM's spread capture, and its flow is what makes the MM's book look traded. Edwin explicitly flagged **how SNT-1 interacts with the MM's quoting and inventory during the Primary Mandate rounds** (the IPO completion-sweep rounds where the MM absorbs unsold float) as the main open question, see [[market-maker/open-questions]]. Both agents respect the same guards (halts, RP re-anchor freezes, price bands from [[market-maker/systems/market-supervision|supervision]]).

## Smoke test + tuning

Edwin smoke-tested against a fake engine: at **LIVE intensity ~1 order every 5 seconds per book, ~44 shares average**, well inside budget. The **two levers expected to tune after seeing real books** are **`base_orders_per_hour`** and the **loss budget**.
