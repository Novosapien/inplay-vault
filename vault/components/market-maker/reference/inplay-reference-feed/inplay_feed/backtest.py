"""Walk-forward backtest: fit Elo parameters on history, score honestly.

Input: chronologically ordered game rows. Each row is a dict:
    {"season": 2023, "home": "sr:...", "away": "sr:...",
     "home_score": 27, "away_score": 20, "neutral": False,
     "closing_home_prob": 0.63}          # optional, for comparison
    plus "groups": passed separately for preseason regression.

The engine only ever predicts a game BEFORE updating on it, so every
metric is out-of-sample. Metrics: log loss and Brier score for the model,
and the same for closing lines where present — the model doesn't need to
beat closing lines, it needs to be close to them.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from itertools import product

from .elo import EloEngine, EloParams

_EPS = 1e-9


@dataclass
class BacktestResult:
    n_games: int
    log_loss: float
    brier: float
    closing_log_loss: float | None
    closing_brier: float | None


def _score(p: float, outcome: float) -> tuple[float, float]:
    p = min(max(p, _EPS), 1 - _EPS)
    ll = -(outcome * math.log(p) + (1 - outcome) * math.log(1 - p))
    br = (p - outcome) ** 2
    return ll, br


def run_backtest(games: list[dict], groups_by_season: dict[int, dict[str, str]],
                 params: EloParams, warmup_seasons: int = 1) -> BacktestResult:
    engine = EloEngine(params)
    seasons = sorted({g["season"] for g in games})
    warmup = set(seasons[:warmup_seasons])

    n = 0
    ll_sum = br_sum = 0.0
    cll_sum = cbr_sum = 0.0
    n_closing = 0
    current_season = None

    for g in games:
        if g["season"] != current_season:
            current_season = g["season"]
            engine.preseason_reset(groups_by_season.get(current_season, {}))

        p = engine.home_win_prob(g["home"], g["away"], g.get("neutral", False))
        margin = g["home_score"] - g["away_score"]
        outcome = 1.0 if margin > 0 else 0.0 if margin < 0 else 0.5

        if g["season"] not in warmup:
            ll, br = _score(p, outcome)
            ll_sum += ll
            br_sum += br
            n += 1
            cp = g.get("closing_home_prob")
            if cp is not None:
                cll, cbr = _score(cp, outcome)
                cll_sum += cll
                cbr_sum += cbr
                n_closing += 1

        engine.update(g["home"], g["away"], g["home_score"], g["away_score"],
                      g.get("neutral", False))

    return BacktestResult(
        n_games=n,
        log_loss=ll_sum / max(n, 1),
        brier=br_sum / max(n, 1),
        closing_log_loss=(cll_sum / n_closing) if n_closing else None,
        closing_brier=(cbr_sum / n_closing) if n_closing else None,
    )


def grid_search(games: list[dict], groups_by_season: dict[int, dict[str, str]],
                base: EloParams | None = None,
                k_grid=(16, 24, 32, 40), hfa_grid=(40, 55, 70),
                mov_grid=(21, 28, 35)) -> tuple[EloParams, BacktestResult]:
    """Fit k / hfa / mov_cap by out-of-sample log loss. Coarse by design —
    Elo is not sensitive enough to justify anything fancier."""
    base = base or EloParams()
    best_params, best_result = None, None
    for k, hfa, mov in product(k_grid, hfa_grid, mov_grid):
        p = replace(base, k=float(k), hfa=float(hfa), mov_cap=int(mov))
        r = run_backtest(games, groups_by_season, p)
        if best_result is None or r.log_loss < best_result.log_loss:
            best_params, best_result = p, r
    return best_params, best_result
