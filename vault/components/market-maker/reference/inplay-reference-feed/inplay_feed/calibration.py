"""Weekly calibration: anchor our rating->probability curve to Sportradar.

Each week, for the games where Sportradar posts a pregame win probability,
we know our rating differential AND the market's probability. We fit the
logistic scale so our curve reproduces the market's probs as closely as
possible (minimum log loss), then shrink toward the prior scale so a
small slate can't whipsaw the curve.

This is what guarantees the published expected-wins numbers can't drift
systematically away from the live feed the market maker prices from.
"""

from __future__ import annotations

import math

from .elo import win_prob

_EPS = 1e-9


def log_loss(scale: float, diffs: list[float], target_probs: list[float]) -> float:
    """Cross-entropy between the market's probs and ours at a given scale."""
    total = 0.0
    for d, q in zip(diffs, target_probs):
        p = min(max(win_prob(d, scale), _EPS), 1 - _EPS)
        total += -(q * math.log(p) + (1 - q) * math.log(1 - p))
    return total / max(len(diffs), 1)


def fit_scale(diffs: list[float], target_probs: list[float],
              lo: float = 150.0, hi: float = 1200.0, iters: int = 60) -> float:
    """1-D golden-section search for the scale minimizing log loss."""
    gr = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    c = b - gr * (b - a)
    d = a + gr * (b - a)
    fc, fd = log_loss(c, diffs, target_probs), log_loss(d, diffs, target_probs)
    for _ in range(iters):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - gr * (b - a)
            fc = log_loss(c, diffs, target_probs)
        else:
            a, c, fc = c, d, fd
            d = a + gr * (b - a)
            fd = log_loss(d, diffs, target_probs)
    return (a + b) / 2


def calibrated_scale(diffs: list[float], target_probs: list[float],
                     prior_scale: float = 400.0, prior_weight: int = 30) -> float:
    """Fit, then shrink toward the prior by observation count.

    With n observed games the result is (n*fitted + w*prior) / (n + w),
    so one thin Tuesday slate cannot move the curve much, while a full
    college Saturday (dozens of games) mostly speaks for itself.
    """
    n = len(diffs)
    if n == 0:
        return prior_scale
    fitted = fit_scale(diffs, target_probs)
    return (n * fitted + prior_weight * prior_scale) / (n + prior_weight)
