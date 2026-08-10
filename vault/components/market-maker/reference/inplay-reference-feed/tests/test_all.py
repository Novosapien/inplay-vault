"""Every guarantee made in the spec email, as a failing-loudly test."""

import math

import pytest

from inplay_feed.calibration import calibrated_scale
from inplay_feed.devig import american_to_prob, expected_wins
from inplay_feed.elo import EloEngine, EloParams, win_prob
from inplay_feed.feed import build_record, validate_records
from inplay_feed.pricing import TeamPricer, share_price
from inplay_feed.publisher import ValidationError, publish, publish_correction
from inplay_feed.rake import rake_to_total


# ---------------------------------------------------------------- item 1
class TestDevig:
    def test_symmetric_juice_returns_the_line(self):
        # Email unit test 1: -110 both sides -> exactly the line.
        assert expected_wins(9.5, -110, -110) == pytest.approx(9.5, abs=1e-12)

    def test_heavier_over_juice_lifts_the_mean(self):
        # Email unit test 2: heavier Over juice -> mean above the line.
        assert expected_wins(9.5, -125, +105) > 9.5

    def test_worked_example_from_the_email(self):
        # line 9.5, Over -125, Under +105, sigma_mkt 2.7 -> 9.72 wins, $48.60
        t = expected_wins(9.5, -125, +105)
        assert t == pytest.approx(9.72, abs=0.005)
        assert 5 * t == pytest.approx(48.60, abs=0.03)

    def test_ncaa_sigma_variant(self):
        # Same odds under NCAA sigma_mkt 2.2 -> 9.679 wins
        from inplay_feed.devig import SIGMA_MKT_NCAA
        t = expected_wins(9.5, -125, +105, sigma_mkt=SIGMA_MKT_NCAA)
        assert t == pytest.approx(9.6792, abs=0.001)

    def test_american_odds_conversion(self):
        assert american_to_prob(-125) == pytest.approx(125 / 225)
        assert american_to_prob(+105) == pytest.approx(100 / 205)

    def test_schedule_sigma_is_binomial_dispersion(self):
        from inplay_feed.devig import schedule_sigma
        assert schedule_sigma([0.5, 0.5]) == pytest.approx((0.5,)[0] ** 0.5)


# ---------------------------------------------------------------- item 2
class TestPricing:
    def test_a_price_equals_5T_at_first_kickoff_after_fresh_total(self):
        p = TeamPricer()
        p.ingest_total(12.0)
        p.game_kickoff("g1", p_ref=0.60)   # x starts at p_ref
        assert p.price() == pytest.approx(5 * 12.0)

    def test_b_price_moves_5_dollars_per_unit_of_live_prob(self):
        p = TeamPricer()
        p.ingest_total(12.0)
        p.game_kickoff("g1", p_ref=0.60)
        base = p.price()
        p.live_update("g1", 0.70)
        assert p.price() - base == pytest.approx(5 * 0.10)

    def test_c_holds_banked_plus_expected_until_next_total(self):
        p = TeamPricer()
        p.ingest_total(12.0)
        p.game_kickoff("g1", p_ref=0.60)
        p.settle("g1", 1.0)
        # Win banked: 12 - 0.6 + 1 = 12.4 -> $62. Holds until new T.
        assert p.price() == pytest.approx(5 * 12.4)
        p.ingest_total(12.4)               # next total arrives, G resets
        assert p.price() == pytest.approx(5 * 12.4)

    def test_georges_63_dollar_bug_does_not_happen(self):
        # 4-1 team, total 12, playing at 60%: correct answer is $60 flat
        # at kickoff (the total already contains this game), not $63.
        assert share_price(T=12.0, ref_probs=[0.60], x_values=[0.60]) == 60.0

    def test_tie_settles_at_half_win(self):
        p = TeamPricer()
        p.ingest_total(8.0)
        p.game_kickoff("g1", p_ref=0.50)
        p.settle("g1", 0.5)
        assert p.price() == pytest.approx(5 * 8.0)  # 8 - 0.5 + 0.5

    def test_g_is_a_set_multiple_games_net_out(self):
        # College Saturday case: two games since the last total.
        p = TeamPricer()
        p.ingest_total(9.0)
        p.game_kickoff("g1", p_ref=0.70)
        p.settle("g1", 0.0)                # upset loss
        p.game_kickoff("g2", p_ref=0.55)
        p.live_update("g2", 0.80)
        assert p.price() == pytest.approx(5 * (9.0 - 0.70 + 0.0 - 0.55 + 0.80))


# ---------------------------------------------------------------- item 3
class TestRake:
    def test_sum_hits_target_exactly(self):
        probs = [0.2, 0.5, 0.5, 0.8, 0.65]
        raked = rake_to_total(probs, 3.1)
        assert sum(raked) == pytest.approx(3.1, abs=1e-8)

    def test_probs_stay_inside_unit_interval_and_ordered(self):
        probs = [0.05, 0.4, 0.6, 0.95]
        raked = rake_to_total(probs, 2.9)
        assert all(0 < p < 1 for p in raked)
        assert raked == sorted(raked)

    def test_impossible_targets_raise(self):
        with pytest.raises(ValueError):
            rake_to_total([0.5, 0.5], 2.0)
        with pytest.raises(ValueError):
            rake_to_total([0.5, 0.5], 0.0)


class TestElo:
    def test_updates_are_zero_sum(self):
        e = EloEngine()
        e.update("A", "B", 27, 20)
        assert e.get("A") + e.get("B") == pytest.approx(2 * 1500.0)

    def test_winner_gains(self):
        e = EloEngine()
        e.update("A", "B", 27, 20)
        assert e.get("A") > 1500.0 > e.get("B")

    def test_mov_cap_binds(self):
        e1, e2 = EloEngine(), EloEngine()
        e1.update("A", "B", 48, 20)   # margin 28 (at cap)
        e2.update("A", "B", 80, 20)   # margin 60 (over cap)
        assert e1.get("A") == pytest.approx(e2.get("A"))

    def test_preseason_regression_pulls_toward_group_mean(self):
        e = EloEngine(EloParams(preseason_regression=0.5))
        e.set("A", 1700.0)
        e.set("B", 1300.0)
        e.preseason_reset({"A": "X", "B": "X"})
        assert e.get("A") == pytest.approx(1600.0)
        assert e.get("B") == pytest.approx(1400.0)

    def test_upset_moves_more_than_expected_win(self):
        e = EloEngine()
        e.set("Fav", 1650.0)
        e.set("Dog", 1350.0)
        before = e.get("Dog")
        e.update("Dog", "Fav", 24, 21)     # dog upsets at home
        upset_gain = e.get("Dog") - before
        e2 = EloEngine()
        e2.set("Fav", 1650.0)
        e2.set("Dog", 1350.0)
        e2.update("Fav", "Dog", 24, 21)    # favorite wins as expected
        expected_gain = e2.get("Fav") - 1650.0
        assert upset_gain > expected_gain


class TestCalibration:
    def test_recovers_true_scale_with_enough_games(self):
        true_scale = 300.0
        diffs = [d for d in range(-400, 401, 10)]
        target = [win_prob(d, true_scale) for d in diffs]
        s = calibrated_scale(diffs, target, prior_scale=400.0, prior_weight=1)
        assert s == pytest.approx(true_scale, rel=0.02)

    def test_empty_slate_returns_prior(self):
        assert calibrated_scale([], [], prior_scale=400.0) == 400.0


class TestFeedAndPublisher:
    def _records(self, n=3):
        return [build_record(f"sr:competitor:{i}", "NCAA",
                             "2026-08-29T10:00:00Z", [0.6, 0.4, 0.7])
                for i in range(n)]

    def test_build_record_math(self):
        r = build_record("t", "NFL", "2026-08-29T10:00:00Z", [0.6, 0.4])
        assert r.expected_remaining_wins == pytest.approx(1.0)
        assert r.sigma == pytest.approx(math.sqrt(0.6 * 0.4 * 2))
        assert r.games_remaining == 2

    def test_validation_catches_bounds_and_count(self):
        recs = [r.to_dict() for r in self._records(3)]
        recs[0]["expected_remaining_wins"] = 99.0
        errs = validate_records(recs, expected_team_count=4)
        assert any("outside" in e for e in errs)
        assert any("expected 4 teams" in e for e in errs)

    def test_publisher_refuses_bad_file(self, tmp_path):
        recs = self._records(3)
        recs[0].expected_remaining_wins = 99.0
        with pytest.raises(ValidationError):
            publish(recs, tmp_path, "2026-08-29", expected_team_count=3)

    def test_correction_reissue_semantics(self, tmp_path):
        recs = self._records(3)
        publish(recs, tmp_path, "2026-08-29", expected_team_count=3)
        path = publish_correction(self._records(3), tmp_path, "2026-08-29",
                                  expected_team_count=3, revision=2)
        assert path.name == "reference_feed_2026-08-29_r2.json"
        import json
        payload = json.loads(path.read_text())
        assert all(r["is_correction"] and r["revision"] == 2
                   for r in payload["records"])


# ---------------------------------------------------------------- item 6
class TestIpo:
    BRANDS = {"A": 80.0, "B": 60.0, "C": 40.0}
    SCHED = [("A", "B"), ("A", "C"), ("A", "FCS-X")]  # FCS-X out of universe

    def _price(self):
        from inplay_feed.ipo import price_team
        return price_team("A", "NCAA", 2.5, -110, -110, self.BRANDS, self.SCHED)

    def test_reference_price_seeds_at_ev_not_listed(self):
        r = self._price()
        assert r.reference_price == pytest.approx(r.ev)
        assert r.ipo_price <= r.ev

    def test_out_of_universe_pays_full_pool(self):
        r = self._price()
        assert r.ev_offfield_uncontested == pytest.approx(2.50)

    def test_capture_is_clamped(self):
        from inplay_feed.ipo import capture_share
        assert capture_share(99.0, 1.0) == 0.80
        assert capture_share(1.0, 99.0) == 0.20

    def test_uncontested_exemption_zeroes_discount(self):
        r = self._price()
        if r.ev_offfield_uncontested / r.ev > 0.20:
            assert r.discount_rate == 0.0

    def test_nfl_gets_tie_leg(self):
        from inplay_feed.ipo import price_team
        sched = [("A", "B")] * 17
        r = price_team("A", "NFL", 9.5, -110, -110, self.BRANDS, sched)
        assert r.ev_onfield == pytest.approx(5 * 9.5 + 2.5 * 0.004 * 17)
