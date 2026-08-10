# SNT-1 — Edwin's email + reference implementation (filed verbatim)

> **Received:** ~2026-07-30 (the 30-07b intake — "two new algorithms in
> one day"; the RNG seed in the file is 20260729). Filed 2026-08-08 when
> George forwarded the full artifact into the working session.
> **Status:** reference only. The concept outline and the venue-reality
> mapping live in [[market-maker/systems/snt-1-noise-taker]]. The
> blockers are E32 (mechanics) and E33/T13 (compliance) in
> [[market-maker/open-questions]]. Nothing here is adopted by filing.

---

## The email

Subject: SNT-1 — Synthetic Noise Taker: reference implementation attached

George,

Now that the Market Maker build is underway, we're adding one more house agent to the Challenge: SNT-1, a Synthetic Noise Taker. Reference implementation is attached (snt1_noise_taker.py, ~350 lines, Python). It's spec-quality code — you implement the small ExchangeAdapter interface against your matching engine and drive agent.step() from your event loop.

WHAT IT IS
A non-participant house account that consumes liquidity — crosses the bid/ask with random sizes at random times — so every team book has real trading action from IPO onward, including with no games being played. It is deliberately a controlled loser: its spread costs are the subsidy that seeds an active secondary market. It never earns leaderboard credit, and its prints against the MM carry zero participant sides, so they're excluded from the off-field volume split under the existing >=1-participant-side rule. No spec amendment needed there.

DESIGN (all in the file header, briefly):
- Poisson arrivals, log-normal sizes (5–400 shares, median ~30), 50/50 direction. Nothing schedulable or front-runnable.
- 90% at-touch marketable IOC (capped at half displayed touch qty); 10% sweeps, hard-capped at 3 ticks through the touch.
- Intensity scales by activity state (base 9 orders/hr per weight-1.0 team; LIVE = 75x) and a per-team weight we'll feed from our popularity model.
- Per-team daily loss governor: $100,000, metered as cost-vs-mid-at-send. Note this meters spread subsidy, not marked P&L.
- Realism layer: disposition-effect profit-taking. When its tracked position is in unrealized profit, P(flatten) tilts from 0.50 up to a 0.65 ceiling (full tilt at 10 ticks of profit). Losers ride at 50/50 until the 1,500-share inventory soft cap kicks in (80% flatten bias). Conditions only on its own cost basis vs mid — no book state, no participant data.
- Hard guards: never trades halted, locked/crossed, or one-sided books, never during RP re-anchor freezes, never wider than 8 ticks, taker-only (never posts).

ACCOUNT FLAGS NEEDED ON YOUR GATEWAY
account_type = HOUSE_SYNTHETIC; leaderboard_eligible = false; participant_side = false.

YOUR SIDE FOR PRODUCTION HARDENING
1. Kill switch + logging + per-order notional cap on the SNT-1 account.
2. Persist pos/basis across restarts (the profit tilt resets to flat otherwise).
3. Periodic reconciliation of the agent's internal position vs the engine's books — on divergence, halt the book. Internal tracking is the source of truth on the trading path; your position() is reconciliation-only.
4. IOC limit enforcement is the real impact cap — the agent's TOB snapshot can be stale by send time, which is fine as long as the engine honors the limit.
5. activity_state() mapping: off-season/overnight -> OVERNIGHT, IPO windows -> PRE_KICKOFF at minimum.

We smoke-tested against a fake engine: at LIVE intensity it prints roughly an order every 5 seconds per book, ~44 shares average, well inside budget. The two levers we expect to tune after seeing real books are base_orders_per_hour and the loss budget.

Happy to walk through it on a call. Questions welcome — especially anything about how this interacts with the MM's quoting or inventory from the Primary Mandate rounds.

Edwin

## The attached file

The reference implementation is filed unmodified beside this note:
`snt1_noise_taker.py`.
