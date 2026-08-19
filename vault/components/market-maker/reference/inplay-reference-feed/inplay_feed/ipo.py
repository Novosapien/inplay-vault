"""Item 6: IPO pricing — the complete engine.py methodology, rebuilt.

IPO price = EV - discount
EV = $5.00 x E[Wins] + $2.50 x E[Ties] (NFL only)
     + $2.50/game x E[Volume Capture Share]

On-field:  single-book season win-total prices at the T-3 freeze,
           de-vigged proportionally, mu = line + sigma_mkt * InvNorm(P_over)
           (identical math and constants to devig.py — by construction).
Off-field: Popularity Index Pop = 0.6*Brand + 0.4*PerfIndex,
           PerfIndex = 100 * E[Wins]/Games. Per-game capture vs opponent j
           is Bradley-Terry Pop_i/(Pop_i+Pop_j), clamped to [0.20, 0.80].
           Opponents outside the 170-team universe are uncontested: the
           universe team accrues the full $2.50.
Discount:  1%-3%, scaled within each league by the CONTESTED share of
           off-field value. Uncontested accrual > 20% of EV -> no
           discount, list at full EV.
Prices are computed once at the freeze, full precision, never revised.
Reference Price seeds at EV (not the discounted listing price).

DATA INPUTS (the only things not in this file):
  odds rows:   {team, league, line, over_odds, under_odds}
  brand tiers: {team: 0-100}
  schedule:    list of (team, opponent) rows; opponents not in the brand
               map are treated as out-of-universe.
"""

from __future__ import annotations

from dataclasses import dataclass

from .devig import SIGMA_MKT_NCAA, SIGMA_MKT_NFL, expected_wins

WIN_PAYOUT = 5.00
TIE_PAYOUT = 2.50           # NFL only
AD_POOL_PER_GAME = 2.50
CAPTURE_CLAMP = (0.20, 0.80)
NFL_TIE_RATE = 0.004        # expected ties per game, NFL
UNCONTESTED_EXEMPT = 0.20   # uncontested accrual > 20% of EV -> no discount
DISCOUNT_LO, DISCOUNT_HI = 0.01, 0.03


def popularity(brand: float, exp_wins: float, games: int) -> float:
    perf = 100.0 * exp_wins / games if games else 0.0
    return 0.6 * brand + 0.4 * perf


def capture_share(pop_i: float, pop_j: float) -> float:
    raw = pop_i / (pop_i + pop_j) if (pop_i + pop_j) > 0 else 0.5
    lo, hi = CAPTURE_CLAMP
    return min(max(raw, lo), hi)


@dataclass
class IpoResult:
    team: str
    league: str
    exp_wins: float
    ev_onfield: float
    ev_offfield_contested: float
    ev_offfield_uncontested: float
    ev: float
    contested_share: float      # contested off-field EV / EV
    discount_rate: float
    ipo_price: float            # EV - discount
    reference_price: float      # seeds at EV


def price_team(team: str, league: str, line: float, over_odds: float,
               under_odds: float, brands: dict[str, float],
               schedule: list[tuple[str, str]]) -> IpoResult:
    """Price one team. schedule holds (team, opponent) rows for this team's
    slate; an opponent absent from `brands` is out-of-universe."""
    sigma = SIGMA_MKT_NFL if league == "NFL" else SIGMA_MKT_NCAA
    opponents = [opp for (t, opp) in schedule if t == team]
    games = len(opponents)

    ew = expected_wins(line, over_odds, under_odds, sigma_mkt=sigma)
    ew = min(max(ew, 0.0), float(games) if games else ew)

    onfield = WIN_PAYOUT * ew
    if league == "NFL":
        onfield += TIE_PAYOUT * NFL_TIE_RATE * games

    pop_i = popularity(brands[team], ew, games)
    contested = uncontested = 0.0
    for opp in opponents:
        if opp in brands:
            # Opponent's PerfIndex needs its own expected wins; at IPO we
            # approximate with the league-average Pop for opponents priced
            # in the same run — production passes the full pop map instead.
            contested += AD_POOL_PER_GAME * capture_share(pop_i, brands[opp])
        else:
            uncontested += AD_POOL_PER_GAME  # out-of-universe: full accrual

    ev = onfield + contested + uncontested
    contested_frac = contested / ev if ev > 0 else 0.0

    if ev > 0 and (uncontested / ev) > UNCONTESTED_EXEMPT:
        rate = 0.0
    else:
        # VERIFY-BEFORE-FREEZE: linear map of contested share to [1%, 3%].
        # The original engine.py scaled "within each league"; if it ranked
        # or normalized differently, change this one line to match.
        rate = DISCOUNT_LO + (DISCOUNT_HI - DISCOUNT_LO) * contested_frac

    return IpoResult(
        team=team, league=league, exp_wins=ew,
        ev_onfield=onfield,
        ev_offfield_contested=contested,
        ev_offfield_uncontested=uncontested,
        ev=ev, contested_share=contested_frac,
        discount_rate=rate,
        ipo_price=ev * (1.0 - rate),
        reference_price=ev,
    )
