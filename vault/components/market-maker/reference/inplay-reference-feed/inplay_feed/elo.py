"""Power-rating engine: Elo with margin-of-victory, home field, preseason regression.

This is the "every team carries a rating, updated after each result" piece
from item 3 of the spec email. Chess Elo, adapted for football:

  - Margin of victory matters, but is capped (mov_cap) so a 60-point
    blowout of a weak opponent doesn't distort.
  - The MOV multiplier is dampened when the favorite wins big (the
    autocorrelation damper), so strong teams can't inflate forever.
  - Home field is a fixed rating bump (hfa), skipped for neutral sites.
  - Preseason: ratings regress toward the team's group mean (conference
    for college, league for NFL) because rosters turn over.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class EloParams:
    k: float = 24.0                  # update step size
    hfa: float = 55.0                # home-field advantage, rating points
    mov_cap: int = 28                # cap on margin of victory, game points
    scale: float = 400.0             # rating points per factor-of-10 in odds
    preseason_regression: float = 0.35  # fraction pulled back to group mean
    base_rating: float = 1500.0


def win_prob(rating_diff: float, scale: float = 400.0) -> float:
    """Rating difference (home minus away, HFA included) -> home win prob."""
    return 1.0 / (1.0 + 10.0 ** (-rating_diff / scale))


class EloEngine:
    def __init__(self, params: EloParams | None = None):
        self.params = params or EloParams()
        self.ratings: dict[str, float] = {}

    # -- ratings ----------------------------------------------------------
    def get(self, team_id: str) -> float:
        return self.ratings.get(team_id, self.params.base_rating)

    def set(self, team_id: str, rating: float) -> None:
        self.ratings[team_id] = rating

    def preseason_reset(self, groups: dict[str, str]) -> None:
        """Regress every team toward its group mean.

        groups maps team_id -> group name (conference for NCAA, "NFL" for NFL).
        Teams not yet rated are seeded at base_rating first.
        """
        for team in groups:
            self.ratings.setdefault(team, self.params.base_rating)
        by_group: dict[str, list[str]] = {}
        for team, grp in groups.items():
            by_group.setdefault(grp, []).append(team)
        w = self.params.preseason_regression
        for grp, teams in by_group.items():
            mean = sum(self.ratings[t] for t in teams) / len(teams)
            for t in teams:
                self.ratings[t] = self.ratings[t] + w * (mean - self.ratings[t])

    # -- probabilities ----------------------------------------------------
    def rating_diff(self, home: str, away: str, neutral: bool = False) -> float:
        hfa = 0.0 if neutral else self.params.hfa
        return self.get(home) - self.get(away) + hfa

    def home_win_prob(self, home: str, away: str, neutral: bool = False) -> float:
        return win_prob(self.rating_diff(home, away, neutral), self.params.scale)

    # -- updates ----------------------------------------------------------
    def update(self, home: str, away: str, home_score: int, away_score: int,
               neutral: bool = False) -> float:
        """Apply one final result. Returns the rating delta given to the home team.

        Zero-sum: away team receives exactly -delta.
        """
        p_home = self.home_win_prob(home, away, neutral)
        margin = home_score - away_score
        if margin > 0:
            result = 1.0
        elif margin < 0:
            result = 0.0
        else:
            result = 0.5

        mov = min(abs(margin), self.params.mov_cap)
        mov_mult = math.log(mov + 1.0)

        # Autocorrelation damper (FiveThirtyEight-style): shrink the MOV
        # boost when the higher-rated team is the one winning big.
        raw_diff = self.get(home) - self.get(away)
        if result == 1.0:
            winner_edge = raw_diff
        elif result == 0.0:
            winner_edge = -raw_diff
        else:
            winner_edge = 0.0
        damper = 2.2 / (winner_edge * 0.001 + 2.2)
        damper = max(0.3, min(damper, 3.0))  # numerical guard rails

        delta = self.params.k * mov_mult * damper * (result - p_home)
        self.ratings[home] = self.get(home) + delta
        self.ratings[away] = self.get(away) - delta
        return delta
