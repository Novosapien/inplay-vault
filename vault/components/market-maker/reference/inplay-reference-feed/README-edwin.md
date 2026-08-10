# InPlay Reference Feed — engine + spec code

Everything in the "answers on all six" email, as running, tested Python.
Stdlib only — no dependencies except pytest for the tests.

## Map from the email to the code

| Email item | Module | What it does |
|---|---|---|
| 1 — win total math | `inplay_feed/devig.py` | American odds → de-vigged mean expected wins (T). Sigma convention: the de-vig step uses market-implied SIGMA_MKT (NFL 2.7, NCAA 2.2 — matching the engine.py Parameters tab); the feed's `sigma` field is schedule dispersion sqrt(Σp(1−p)). Different objects, never interchanged. Worked example is a test. |
| 2 — double count | `inplay_feed/pricing.py` | `TeamPricer` walks the full lifecycle: ingest T, kickoff, live updates, settlement, next T. The email's three unit tests (a)(b)(c) are in the test suite, plus a test proving the $63 bug can't happen. |
| 3 — the ratings | `inplay_feed/elo.py` | Power ratings: MOV-capped Elo with home field and preseason regression toward conference mean. |
| 3 — market anchor | `inplay_feed/calibration.py` | Weekly fit of the rating→probability curve against Sportradar's posted pregame probs, shrunk toward a prior so thin slates can't whipsaw it. |
| 3 — NFL consistency | `inplay_feed/rake.py` | Logit-space rake so NFL remaining-game probs sum *exactly* to the de-vigged sportsbook total. Probs stay in (0,1), ordering preserved. |
| 3 — the file | `inplay_feed/feed.py` | Record schema (field-for-field the email's) + `validate_records()`, the ingest rules. Run the same function on both ends. |
| 3/4 — publishing | `inplay_feed/publisher.py` | Daily file writes, refuses to publish an invalid file, correction reissues (same effective_time, bumped revision, `is_correction=true`, `_rN` filename). |
| fitting | `inplay_feed/backtest.py` | Walk-forward backtest (predict before update — every metric is out-of-sample) and coarse grid search for k / HFA / MOV cap. Scores log loss + Brier vs closing lines where available. |

## Run it

```
pip install pytest
python -m pytest tests/        # 25 tests — every guarantee in the email
python demo.py                 # end-to-end on synthetic data:
                               # fit → calibrate → rake → publish
```

`demo.py` writes `out/reference_feed_2026-08-29.json` — a valid sample
file with all 170 teams, in the exact production schema. Point your
ingestion at it today.

## What's synthetic vs. production

The engine, math, schema, validation, and publisher are production code.
Two inputs are stubbed and get swapped without touching anything else:

1. **Historical results** — `demo.py` simulates them; production loads
   5–10 seasons from the Sportradar backfill into the same row format
   (`{"season", "home", "away", "home_score", "away_score", "neutral"}`).
2. **The weekly Sportradar slate** — demo synthesizes pregame probs;
   production reads them off the live feed for the calibration step.

Division of labor stays as the email says: InPlay runs the fit,
calibration, rake, and publisher. novosapien consumes the file —
ingestion, hold-last-value, correction replacement, missing-file alarm —
and can reuse `validate_records()` and `TeamPricer` verbatim.
