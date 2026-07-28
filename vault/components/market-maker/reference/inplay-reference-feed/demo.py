"""End-to-end demo on synthetic data: proves the whole pipeline runs.

Simulates two leagues with known "true" team strengths, plays two seasons
of history, fits Elo parameters by grid search, calibrates the probability
curve against a synthetic Sportradar slate, rakes the NFL to de-vigged
totals, and publishes a valid sample feed file.

Run:  python demo.py
"""

from __future__ import annotations

import random

from inplay_feed.backtest import grid_search
from inplay_feed.calibration import calibrated_scale
from inplay_feed.devig import expected_wins
from inplay_feed.elo import EloEngine, win_prob
from inplay_feed.feed import build_record
from inplay_feed.publisher import publish

random.seed(7)

# --- synthetic universe --------------------------------------------------
NFL = [f"sr:competitor:nfl{i}" for i in range(32)]
NCAA = [f"sr:competitor:cfb{i}" for i in range(138)]
TRUE = {t: random.gauss(1500, 110) for t in NFL + NCAA}
GROUPS = {**{t: "NFL" for t in NFL},
          **{t: f"CONF{(i % 10)}" for i, t in enumerate(NCAA)}}


def simulate_game(home, away):
    p = win_prob(TRUE[home] - TRUE[away] + 55)
    home_wins = random.random() < p
    margin = max(1, round(abs(random.gauss(10, 8))))
    return (margin, 0) if home_wins else (0, margin)


def simulate_season(season, teams, n_rounds):
    games = []
    for _ in range(n_rounds):
        order = random.sample(teams, len(teams))
        for h, a in zip(order[::2], order[1::2]):
            hs, as_ = simulate_game(h, a)
            games.append({"season": season, "home": h, "away": a,
                          "home_score": 20 + hs, "away_score": 20 + as_})
    return games


def main():
    # 1. history + parameter fit
    history = []
    for season in (2024, 2025):
        history += simulate_season(season, NFL, 17)
        history += simulate_season(season, NCAA, 12)
    groups_by_season = {2024: GROUPS, 2025: GROUPS}
    params, result = grid_search(history, groups_by_season)
    print(f"fit: k={params.k} hfa={params.hfa} mov_cap={params.mov_cap} "
          f"| oos log_loss={result.log_loss:.4f} brier={result.brier:.4f} "
          f"({result.n_games} games)")

    # 2. ratings entering the new season
    engine = EloEngine(params)
    for g in sorted(history, key=lambda g: g["season"]):
        engine.update(g["home"], g["away"], g["home_score"], g["away_score"])
    engine.preseason_reset(GROUPS)

    # 3. calibrate the curve to a synthetic Sportradar slate
    slate = random.sample(NCAA, 40)
    diffs, market = [], []
    for h, a in zip(slate[::2], slate[1::2]):
        diffs.append(engine.rating_diff(h, a))
        market.append(min(max(win_prob(TRUE[h] - TRUE[a] + 55)
                              + random.gauss(0, 0.02), 0.02), 0.98))
    scale = calibrated_scale(diffs, market, prior_scale=params.scale)
    print(f"calibrated scale: {scale:.1f} (prior {params.scale})")

    # 4. build records; NFL raked to de-vigged totals
    records = []
    eff = "2026-08-29T10:00:00Z"
    for t in NFL:
        opps = random.sample([x for x in NFL if x != t], 17)
        probs = [win_prob(engine.rating_diff(t, o), scale) for o in opps]
        line = round(sum(probs) * 2) / 2
        line = line + 0.5 if line == int(line) else line   # half-point line
        target = expected_wins(line, -118, -104)  # sigma_mkt NFL default 2.7
        target = min(max(target, 0.01), len(probs) - 0.01)
        from inplay_feed.rake import rake_to_total
        probs = rake_to_total(probs, target)
        records.append(build_record(t, "NFL", eff, probs))
    for t in NCAA:
        opps = random.sample([x for x in NCAA if x != t], 12)
        probs = [win_prob(engine.rating_diff(t, o), scale) for o in opps]
        records.append(build_record(t, "NCAA", eff, probs))

    # 5. publish
    path = publish(records, "out", "2026-08-29", expected_team_count=170)
    print(f"published {path} ({len(records)} teams)")


if __name__ == "__main__":
    main()
