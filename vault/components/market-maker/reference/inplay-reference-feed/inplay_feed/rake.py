"""NFL consistency step: rake remaining-game probs to a target sum.

For the 32 NFL teams, the published number must equal the de-vigged
sportsbook total by construction. The model supplies the game-by-game
shape; this module rescales those probs so their sum hits the target
exactly, while keeping every prob strictly inside (0, 1).

Method: shift every prob by a constant in logit space and bisect on the
shift until the sum matches. A logit shift preserves ordering, keeps
probs in (0, 1), and moves near-50% games more than near-certain ones,
which is the behavior you want from a rake.
"""

from __future__ import annotations

import math

_EPS = 1e-9


def _logit(p: float) -> float:
    p = min(max(p, _EPS), 1 - _EPS)
    return math.log(p / (1 - p))


def _sigmoid(x: float) -> float:
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    e = math.exp(x)
    return e / (1.0 + e)


def rake_to_total(probs: list[float], target: float,
                  tol: float = 1e-10, max_iter: int = 200) -> list[float]:
    """Return probs shifted in logit space so they sum to target.

    target must lie strictly between 0 and len(probs); values at or past
    the boundary have no valid probability vector and raise ValueError.
    """
    n = len(probs)
    if n == 0:
        if abs(target) < 1e-9:
            return []
        raise ValueError("no games to rake but nonzero target")
    if not (0.0 < target < float(n)):
        raise ValueError(f"target {target} outside (0, {n})")

    logits = [_logit(p) for p in probs]

    def total(shift: float) -> float:
        return sum(_sigmoid(l + shift) for l in logits)

    lo, hi = -50.0, 50.0  # sigmoid saturates far before these bounds
    for _ in range(max_iter):
        mid = (lo + hi) / 2
        if total(mid) < target:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    shift = (lo + hi) / 2
    return [_sigmoid(l + shift) for l in logits]
