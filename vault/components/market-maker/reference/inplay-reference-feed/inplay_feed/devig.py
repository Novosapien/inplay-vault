"""Item 1 of the spec email: sportsbook season win total -> de-vigged MEAN.

SIGMA CONVENTION (governs everywhere, matching engine.py's Parameters tab):
  - The de-vig mean extraction uses the MARKET-IMPLIED dispersion of season
    wins: SIGMA_MKT_NFL = 2.7, SIGMA_MKT_NCAA = 2.2. These are league
    constants, wider than pure game-by-game binomial dispersion because
    they carry parameter/team-quality uncertainty the market prices in.
  - The feed's published `sigma` field is a DIFFERENT object: the binomial
    dispersion of the remaining schedule, sqrt(sum p(1-p)) — see feed.py.
Do not interchange them.
"""

from __future__ import annotations

from statistics import NormalDist

SIGMA_MKT_NFL = 2.7
SIGMA_MKT_NCAA = 2.2


def american_to_prob(odds: float) -> float:
    """American odds -> implied probability (vig still included)."""
    return (-odds) / (-odds + 100) if odds < 0 else 100 / (odds + 100)


def devig_two_way(p_a: float, p_b: float) -> tuple[float, float]:
    """Proportional de-vig: scale both probs to sum to exactly 1."""
    s = p_a + p_b
    return p_a / s, p_b / s


def schedule_sigma(game_win_probs: list[float]) -> float:
    """Binomial dispersion of a win count: sqrt(sum p(1-p)).

    This feeds the feed's `sigma` FIELD only — never the de-vig step.
    """
    return sum(p * (1 - p) for p in game_win_probs) ** 0.5


def expected_wins(line: float, over_odds: float, under_odds: float,
                  sigma_mkt: float = SIGMA_MKT_NFL) -> float:
    """Sportsbook season win total -> de-vigged MEAN expected wins (T).

    line:       posted total, e.g. 9.5 (half-point lines assumed)
    over_odds:  American odds on the Over, e.g. -125
    under_odds: American odds on the Under, e.g. +105
    sigma_mkt:  market-implied season-wins dispersion —
                SIGMA_MKT_NFL (2.7) or SIGMA_MKT_NCAA (2.2)
    """
    p_over_fair, _ = devig_two_way(american_to_prob(over_odds),
                                   american_to_prob(under_odds))
    # The line is where P(wins > line) = fair over prob.
    # Normal approximation of the win count gives:
    z = NormalDist().inv_cdf(p_over_fair)
    return line + sigma_mkt * z
