"""
SNT-1 — Synthetic Noise Taker, Reference Implementation v1.0
InPlay Football Trading Challenge

Purpose
-------
A non-participant house account that consumes liquidity (crosses the
bid/ask) to ensure trading action on every team book. It exists to
create realistic, exploitable noise flow — NOT to move price toward or
away from any target. It never earns leaderboard credit, and its prints
against the MM carry zero participant sides (excluded from the $2.50
off-field volume split per the existing >=1-participant-side rule).

Design principles (agreed with InPlay, Jul 2026)
------------------------------------------------
1. Arrivals are a Poisson process — no fixed schedule a participant
   could learn and front-run.
2. Sizes are log-normal, clipped to [min_size, max_size].
3. Direction is 50/50 i.i.d. (pure noise; flow is uninformative).
4. ~90% of orders are at-touch marketable IOC; ~10% are "sweeps"
   whose limit price is capped at max_impact_ticks through the touch.
   Nothing ever crosses deeper than that cap.
5. Expected cost per trade ~= half-spread x size. A per-team daily
   LOSS BUDGET governs activity: when the realized-loss estimate for a
   team-book hits its budget, SNT-1 goes quiet on that book until the
   next session.
6. Intensity scales with an activity state (PRE_KICKOFF / LIVE /
   POST / OVERNIGHT) and a per-team activity weight, so live games get
   more action and quiet books still get a heartbeat.
7. Hard guards: never trades a halted book, a locked/crossed book, an
   empty side, or during an RP re-anchor freeze window; never posts
   resting liquidity (taker only); inventory is soft-capped and mean-
   reverted so the account doesn't accumulate a directional book.

Integration
-----------
Implement ExchangeAdapter against the matching engine. Run one
NoiseTakerAgent per league (or one global — it is team-keyed
internally). Call agent.step(now) from your event loop, or run
agent.run() with a scheduler. All randomness flows through a single
seeded RNG for reproducible sims.

Account flags required on the gateway side:
  account_type = HOUSE_SYNTHETIC
  leaderboard_eligible = False
  participant_side = False        # for off-field volume counting
"""

from __future__ import annotations

import math
import random
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional


# ----------------------------------------------------------------------
# Market / venue interface (Novosapien implements this)
# ----------------------------------------------------------------------

class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"


class ActivityState(Enum):
    OVERNIGHT = "OVERNIGHT"
    PRE_KICKOFF = "PRE_KICKOFF"
    LIVE = "LIVE"
    POST = "POST"


@dataclass(frozen=True)
class TopOfBook:
    bid_px: Optional[float]
    bid_qty: int
    ask_px: Optional[float]
    ask_qty: int
    halted: bool
    rp_freeze: bool            # True during an RP re-anchor window

    @property
    def two_sided(self) -> bool:
        return self.bid_px is not None and self.ask_px is not None

    @property
    def locked_or_crossed(self) -> bool:
        return self.two_sided and self.bid_px >= self.ask_px  # type: ignore

    @property
    def spread(self) -> Optional[float]:
        if not self.two_sided:
            return None
        return self.ask_px - self.bid_px  # type: ignore


@dataclass(frozen=True)
class Fill:
    qty: int
    avg_px: float


class ExchangeAdapter(ABC):
    """Thin adapter over the matching engine, scoped to the SNT-1 account."""

    @abstractmethod
    def top_of_book(self, team_id: str) -> TopOfBook: ...

    @abstractmethod
    def activity_state(self, team_id: str) -> ActivityState: ...

    @abstractmethod
    def send_marketable_ioc(
        self, team_id: str, side: Side, qty: int, limit_px: float
    ) -> Optional[Fill]:
        """Marketable limit, IOC. Returns the fill (possibly partial) or None."""

    @abstractmethod
    def position(self, team_id: str) -> int:
        """Signed SNT-1 inventory (shares) per the engine's own books.
        Used for periodic reconciliation against the agent's internal
        tracking — not consulted on the trading path."""


# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

@dataclass
class SNTConfig:
    tick: float = 0.01

    # --- Arrival process (per team-book) ---------------------------------
    # Base rate = expected orders/hour in OVERNIGHT on a weight-1.0 team.
    base_orders_per_hour: float = 9.0
    state_multiplier: Dict[ActivityState, float] = field(default_factory=lambda: {
        ActivityState.OVERNIGHT: 1.0,
        ActivityState.PRE_KICKOFF: 6.0,
        ActivityState.LIVE: 75.0,
        ActivityState.POST: 4.0,
    })
    # Per-team activity weight in [0.25, 4.0]; supply from the EAV /
    # popularity model. Defaults to 1.0 for any team not listed.
    team_weight: Dict[str, float] = field(default_factory=dict)

    # --- Size distribution ----------------------------------------------
    size_lognorm_mu: float = 3.4       # median ~= e^3.4 ~= 30 shares
    size_lognorm_sigma: float = 0.9
    min_size: int = 5
    max_size: int = 400

    # --- Order style -----------------------------------------------------
    sweep_probability: float = 0.10    # else at-touch marketable IOC
    max_impact_ticks: int = 3          # sweep limit = touch +/- N ticks
    max_fraction_of_touch: float = 0.5 # at-touch qty <= 50% of displayed

    # --- Loss budget governor -------------------------------------------
    # Expected cost per trade ~ half-spread x qty; realized loss is
    # tracked as (fill vs mid at send). Budget is per team, per session.
    daily_loss_budget_per_team: float = 100_000.00   # dollars
    max_spread_ticks_to_trade: int = 8          # skip absurdly wide books

    # --- Inventory control ----------------------------------------------
    inventory_soft_cap: int = 1_500    # shares, absolute
    # Above the cap, direction is biased toward flattening:
    flatten_bias: float = 0.80         # P(trade reduces |inventory|)

    # --- Profit-taking realism (retail-style, objective-free) ------------
    # When inventory is in unrealized profit, the flatten direction gets a
    # mild stochastic tilt (contrarian supply into rallies / demand into
    # dips). Never a hard trigger, never conditions on anything but own
    # cost basis vs mid, and never overrides the 50/50 core when flat.
    profit_take_enabled: bool = True
    profit_take_bias_max: float = 0.65   # max P(flatten) when well in profit
    profit_take_full_ticks: float = 10.0 # profit/share (in ticks) for max tilt

    rng_seed: Optional[int] = 20260729


# ----------------------------------------------------------------------
# Agent
# ----------------------------------------------------------------------

@dataclass
class _BookState:
    next_arrival_ts: float = 0.0
    session_loss: float = 0.0
    trades: int = 0
    volume: int = 0
    pos: int = 0            # signed shares, tracked from own fills
    basis: float = 0.0      # VWAP cost basis of current position


class NoiseTakerAgent:
    def __init__(self, exchange: ExchangeAdapter, teams: list[str],
                 cfg: SNTConfig = SNTConfig()):
        self.x = exchange
        self.cfg = cfg
        self.rng = random.Random(cfg.rng_seed)
        self.state: Dict[str, _BookState] = {t: _BookState() for t in teams}

    # -- schedule ---------------------------------------------------------

    def _rate_per_sec(self, team_id: str) -> float:
        st = self.x.activity_state(team_id)
        w = self.cfg.team_weight.get(team_id, 1.0)
        per_hour = self.cfg.base_orders_per_hour * self.cfg.state_multiplier[st] * w
        return max(per_hour, 1e-9) / 3600.0

    def _schedule_next(self, team_id: str, now: float) -> None:
        lam = self._rate_per_sec(team_id)
        # Exponential inter-arrival => Poisson process; re-sampled each
        # trade so intensity changes (state transitions) take effect fast.
        self.state[team_id].next_arrival_ts = now + self.rng.expovariate(lam)

    def new_session(self) -> None:
        """Call at session open: resets loss budgets and schedules."""
        now = time.time()
        for t, s in self.state.items():
            s.session_loss = 0.0
            s.trades = 0
            s.volume = 0
            self._schedule_next(t, now)

    # -- sampling ---------------------------------------------------------

    def _sample_size(self) -> int:
        raw = self.rng.lognormvariate(self.cfg.size_lognorm_mu,
                                      self.cfg.size_lognorm_sigma)
        return int(min(max(raw, self.cfg.min_size), self.cfg.max_size))

    def _sample_side(self, team_id: str, s: _BookState, mid: float) -> Side:
        # Single source of truth: internally tracked s.pos. The adapter's
        # position() is for periodic reconciliation/alerting only — if it
        # diverges from s.pos, halt the book and investigate.
        inv = s.pos

        # Hard inventory control takes precedence over everything.
        if abs(inv) > self.cfg.inventory_soft_cap:
            flattening = Side.SELL if inv > 0 else Side.BUY
            if self.rng.random() < self.cfg.flatten_bias:
                return flattening

        # Retail-style profit-taking tilt: if our tracked position is in
        # unrealized profit, nudge P(flatten) above 0.5, scaled by profit
        # per share in ticks, capped at profit_take_bias_max. Losers get
        # NO tilt (they ride at 50/50) — mimics disposition-effect flow
        # and supplies contrarian liquidity into moves.
        if self.cfg.profit_take_enabled and s.pos != 0:
            pnl_per_share = (mid - s.basis) if s.pos > 0 else (s.basis - mid)
            if pnl_per_share > 0:
                profit_ticks = pnl_per_share / self.cfg.tick
                frac = min(profit_ticks / self.cfg.profit_take_full_ticks, 1.0)
                p_flatten = 0.5 + frac * (self.cfg.profit_take_bias_max - 0.5)
                flattening = Side.SELL if s.pos > 0 else Side.BUY
                opposite = Side.BUY if s.pos > 0 else Side.SELL
                return flattening if self.rng.random() < p_flatten else opposite

        return Side.BUY if self.rng.random() < 0.5 else Side.SELL

    # -- guards -----------------------------------------------------------

    def _tradeable(self, tob: TopOfBook) -> bool:
        if tob.halted or tob.rp_freeze:
            return False
        if not tob.two_sided or tob.locked_or_crossed:
            return False
        assert tob.spread is not None
        if tob.spread > self.cfg.max_spread_ticks_to_trade * self.cfg.tick:
            return False
        return True

    # -- core -------------------------------------------------------------

    def step(self, now: Optional[float] = None) -> None:
        """Fire at most one order per due team. Call frequently (>=1 Hz)."""
        now = time.time() if now is None else now
        for team_id, s in self.state.items():
            if now < s.next_arrival_ts:
                continue
            self._schedule_next(team_id, now)   # reschedule regardless
            if s.session_loss >= self.cfg.daily_loss_budget_per_team:
                continue                        # budget spent: stay quiet
            self._maybe_trade(team_id, s)

    def _maybe_trade(self, team_id: str, s: _BookState) -> None:
        tob = self.x.top_of_book(team_id)
        if not self._tradeable(tob):
            return

        mid = (tob.bid_px + tob.ask_px) / 2.0                    # type: ignore
        side = self._sample_side(team_id, s, mid)
        qty = self._sample_size()
        touch_qty = tob.ask_qty if side is Side.BUY else tob.bid_qty
        touch_px = tob.ask_px if side is Side.BUY else tob.bid_px  # type: ignore

        if self.rng.random() < self.cfg.sweep_probability:
            # Sweep: allowed to walk the book, but never deeper than
            # max_impact_ticks through the touch.
            impact = self.cfg.max_impact_ticks * self.cfg.tick
            limit_px = touch_px + impact if side is Side.BUY else touch_px - impact
        else:
            # At-touch: IOC at the touch, sized to a fraction of what is
            # displayed so we don't accidentally exhaust the level.
            qty = min(qty, max(int(touch_qty * self.cfg.max_fraction_of_touch),
                               self.cfg.min_size))
            limit_px = touch_px

        limit_px = round(limit_px / self.cfg.tick) * self.cfg.tick
        fill = self.x.send_marketable_ioc(team_id, side, qty, limit_px)
        if fill is None or fill.qty == 0:
            return

        # Realized "noise cost" vs mid at send — this is what the loss
        # budget meters. (Signed so an inside fill can credit back.)
        signed = 1 if side is Side.BUY else -1
        s.session_loss += signed * (fill.avg_px - mid) * fill.qty
        s.session_loss = max(s.session_loss, 0.0)
        s.trades += 1
        s.volume += fill.qty

        # Position / cost-basis accounting (for the profit-take tilt).
        signed_qty = fill.qty * signed
        new_pos = s.pos + signed_qty
        if s.pos == 0 or (s.pos > 0) == (signed_qty > 0):
            # Opening or adding: VWAP the basis.
            s.basis = ((s.basis * abs(s.pos) + fill.avg_px * fill.qty)
                       / max(abs(new_pos), 1))
        elif (new_pos > 0) != (s.pos > 0) and new_pos != 0:
            # Flipped through flat: basis resets to this fill.
            s.basis = fill.avg_px
        # Pure reduction: basis unchanged.
        s.pos = new_pos
        if s.pos == 0:
            s.basis = 0.0

    # -- telemetry --------------------------------------------------------

    def session_report(self) -> Dict[str, dict]:
        return {
            t: {"trades": s.trades, "volume": s.volume,
                "noise_cost": round(s.session_loss, 2),
                "budget_remaining": round(
                    max(self.cfg.daily_loss_budget_per_team - s.session_loss, 0.0), 2)}
            for t, s in self.state.items()
        }
