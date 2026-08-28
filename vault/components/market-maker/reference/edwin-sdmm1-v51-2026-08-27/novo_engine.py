"""
novo_engine.py — SDMM-1 season value function. v5.

CHANGES FROM v4

1. STATE IS REPLAYABLE. v4 applied each Kalman update in place, so calling
   record() twice with the same tick applied it twice -- $1.18 of drift from
   one repeated live tick, and injuries compounded the same way. The maker
   ticks a live game many times a minute, so this was fatal. v5 stores
   observations and rebuilds the posterior from the prior on every read.
   Idempotent by construction; there is no update path that can be applied
   twice.

2. POSTED SPREADS ARE THE PRIMARY RATING CHANNEL. A spread observes the same
   rating difference a final margin observes, but with roughly 1.5 points of
   noise instead of 15 -- a hundred times the information per observation.
   Weekly recalibration off the board is therefore the dominant input and
   results are secondary. It needs no special case: a spread goes through the
   same Kalman step as everything else, which is what keeps the martingale
   exact.

   What does NOT work is pricing a game directly off the raw spread as
   Phi(S/sigma_g). That double-counts the spread's own error and leaves a bias
   of 2*SIGMA_SPREAD^2 in the denominator. Filtering the spread and then
   pricing off the posterior is exact. See test T3.

THE MODEL

    r ~ N(m, S)                        team ratings, in points
    d_g = r_i - r_j + H                expected margin of game g
    margin_g = d_g + eps               eps ~ N(0, SIGMA_G^2)
    spread_g = d_g + eta               eta ~ N(0, SIGMA_SPREAD^2)
    P(win_g) = Phi( d_g / sqrt(SIGMA_G^2 + Var d_g) )

Everything is linear in the state, so every update is an exact Kalman step and
fair value is a martingale in closed form:

    d|F ~ N(mu,V), update -> N(mu',V'),  mu' ~ N(mu, V-V')
    E[ Phi(mu'/sqrt(s2+V')) ] = Phi( mu/sqrt(s2+V'+(V-V')) ) = Phi( mu/sqrt(s2+V) )

SETTLEMENT (accrual; nothing is paid out until the regular season ends)

    V_T = $5*wins + $2.50*ties (NFL only) + marketing dollars captured

Dependencies: standard library only.
"""

from __future__ import annotations
from dataclasses import dataclass, replace
from statistics import NormalDist
import math

N = NormalDist()
Phi = N.cdf
Phi_inv = N.inv_cdf

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
WIN_VALUE = 5.00
TIE_VALUE = 2.50            # NFL only
AD_POOL   = 2.50
RATE      = 0.04
YEARS     = 105 / 365

SIGMA_G      = {"NCAA": 15.0, "NFL": 12.5}   # residual margin sd, points
HOME_ADV     = {"NCAA": 2.5,  "NFL": 1.8}
SIGMA_MKT    = {"NCAA": 2.2,  "NFL": 2.7}    # season-win sd convention
TIE_BAND     = {"NCAA": 0.0,  "NFL": 0.5}
SIGMA_SPREAD = 1.5          # how far a posted spread sits from the true edge

SIGMA_V   = 0.35            # weekly ad-share noise, logits
PHI_BRAND = 0.020           # logits of brand per rating point
CAP_LO, CAP_HI = 0.20, 0.80 # Supplement A clamp on per-game capture

# RETENTION (per Edwin, Aug 27): the $2.50/game pool is NOT fully distributed.
# Each team's capture is measured against the field (0.6 brand + 0.4
# performance, clamped 20-80%); the two captures in a game need not sum to 1,
# and the platform retains the residual. On the NFL reconstruction sheet the
# league-wide retention is $243.30 of the $680 notional (35.8%). So there is
# no pairwise adding-up identity to enforce -- the invariant is instead that
# capture_i + capture_j <= some bound consistent with retention >= 0.

INJURY_PTS = {"QB": 7.0, "RB": 1.0, "WR": 1.5, "OL": 1.2,
              "DL": 1.5, "LB": 1.0, "DB": 1.2, "K": 0.5}
INJURY_VAR = 4.0


@dataclass
class Game:
    week: int
    home: int
    away: int
    neutral: bool = False


@dataclass(frozen=True)
class Obs:
    """What the market knows about one game. Immutable and replayable."""
    spread: float | None = None      # posted spread as EXPECTED MARGIN, home persp.
    margin: float | None = None      # final margin, home perspective
    wp_live: float | None = None     # live win prob, home perspective
    proj_margin: float | None = None
    elapsed: float = 0.0
    ad_share: float | None = None    # home team's printed capture of its $2.50
    ad_share_away: float | None = None  # away team's printed capture (need not be 1-home)

    @property
    def final(self):
        return self.margin is not None

    @property
    def live(self):
        return self.wp_live is not None and self.margin is None


@dataclass(frozen=True)
class Injury:
    team: int
    position: str = "QB"
    severity: float = 1.0


@dataclass
class Legs:
    banked_wins: float
    banked_ties: float
    banked_marketing: float
    live_game: float
    forward_wins: float
    forward_marketing: float
    risk_charge: float
    rating: float
    rating_sd: float
    sigma_remaining: float

    @property
    def fair(self):
        return (self.banked_wins + self.banked_ties + self.banked_marketing
                + self.live_game + self.forward_wins + self.forward_marketing
                + self.risk_charge)


class League:
    """Shared rating state. All mutation goes through set_obs / set_injury,
    which record intent; the posterior is rebuilt from the prior on read."""

    def __init__(self, names, schedule, league="NCAA", rating_sd=6.0, brand_sd=0.35):
        self.names = list(names)
        self.idx = {n: i for i, n in enumerate(self.names)}
        self.games = list(schedule)
        self.lg = league
        self.sg = SIGMA_G[league]
        self.h = HOME_ADV[league]
        self.tie_band = TIE_BAND[league]
        n = len(self.names)

        self.m0 = [0.0] * n
        self.S0 = [[rating_sd ** 2 if i == j else 0.0 for j in range(n)] for i in range(n)]
        self.bm0 = [0.0] * n
        self.bS0 = [[brand_sd ** 2 if i == j else 0.0 for j in range(n)] for i in range(n)]

        self.obs: dict[int, Obs] = {}
        self.injuries: list[Injury] = []
        self.rate = RATE
        self.rp = 0.0
        self._gross0 = 0.0
        self._sigma0 = 1.0
        self._cache = None

    # -- intent ------------------------------------------------------------
    def set_obs(self, gi: int, **kw):
        """Replace what is known about game gi. Idempotent: sending the same
        live tick twice leaves the state identical."""
        self.obs[gi] = replace(self.obs.get(gi, Obs()), **kw)
        self._cache = None

    def clear_obs(self, gi: int):
        self.obs.pop(gi, None)
        self._cache = None

    def set_injury(self, team, position="QB", severity=1.0):
        """One active injury per team; re-sending the same one is a no-op."""
        i = self.idx[team] if isinstance(team, str) else team
        self.injuries = [x for x in self.injuries if x.team != i]
        if severity > 0:
            self.injuries.append(Injury(i, position, severity))
        self._cache = None

    def stale_spreads(self):
        """Games whose posted spread is no longer usable because injury news
        landed after it. The operator should re-post these."""
        hurt = {x.team for x in self.injuries}
        return sorted(gi for gi, o in self.obs.items()
                      if o.spread is not None and o.margin is None and not o.live
                      and (self.games[gi].home in hurt or self.games[gi].away in hurt))

    def clear_injuries(self):
        self.injuries = []
        self._cache = None

    # -- posterior ---------------------------------------------------------
    def _state(self):
        if self._cache is not None:
            return self._cache
        n = len(self.names)
        m, S = list(self.m0), [r[:] for r in self.S0]
        bm, bS = list(self.bm0), [r[:] for r in self.bS0]
        inj = [0.0] * n
        for x in self.injuries:
            inj[x.team] -= INJURY_PTS.get(x.position, 1.0) * x.severity
            S[x.team][x.team] += INJURY_VAR * x.severity

        def kal(M, C, gi, y, var_obs, ratings, offset=0.0):
            g = self.games[gi]
            i, j = g.home, g.away
            mu = M[i] - M[j] + offset
            if ratings:
                mu += inj[i] - inj[j]
                if not g.neutral:
                    mu += self.h
            var = C[i][i] + C[j][j] - 2 * C[i][j]
            Sd = var + var_obs
            if Sd <= 0:
                return
            c = [C[k][i] - C[k][j] for k in range(n)]
            nu = y - mu
            for k in range(n):
                M[k] += c[k] * nu / Sd
            for a in range(n):
                for b in range(a, n):
                    d = c[a] * c[b] / Sd
                    C[a][b] -= d
                    C[b][a] = C[a][b]

        # A posted spread already reflects whatever the board knew when it
        # was hung. If an injury lands AFTER that, the spread is stale: the
        # real book takes the game down and re-posts. Filtering the stale
        # number against an injured rating makes the update fight the injury
        # -- measured at -$3.57 on a week-6 QB, in the wrong direction. So an
        # injury invalidates posted spreads for that team's unplayed games.
        hurt = {x.team for x in self.injuries}
        stale = {gi for gi, o in self.obs.items()
                 if o.spread is not None and o.margin is None and not o.live
                 and (self.games[gi].home in hurt or self.games[gi].away in hurt)}

        # Ratings. A game contributes exactly ONE observation: the final
        # margin if it exists, else the live projection, else a live spread.
        # Order is irrelevant for a linear-Gaussian filter.
        for gi in sorted(self.obs):
            o = self.obs[gi]
            if o.margin is not None:
                kal(m, S, gi, o.margin, self.sg ** 2, True)
            elif o.live and o.proj_margin is not None and o.elapsed > 0:
                kal(m, S, gi, o.proj_margin, self.sg ** 2 / o.elapsed, True)
            elif o.spread is not None and gi not in stale:
                kal(m, S, gi, o.spread, SIGMA_SPREAD ** 2, True)
        # Brand runs its own filter. An ad print never touches a rating.
        for gi in sorted(self.obs):
            o = self.obs[gi]
            if o.ad_share is not None:
                v = min(1 - 1e-9, max(1e-9, o.ad_share))
                g = self.games[gi]
                # The mean of the observed logit share includes the rating
                # tilt, so the innovation must be measured against it too.
                # Comparing against the brand difference alone left the update
                # wrong by up to 0.57 logits on a lopsided matchup.
                tilt = PHI_BRAND * ((m[g.home] + inj[g.home])
                                    - (m[g.away] + inj[g.away]))
                kal(bm, bS, gi, math.log(v / (1 - v)), SIGMA_V ** 2, False,
                    offset=tilt)

        self._cache = (m, S, bm, bS, inj)
        return self._cache

    # -- probabilities -----------------------------------------------------
    def _diff(self, gi):
        m, S, _, _, inj = self._state()
        g = self.games[gi]
        i, j = g.home, g.away
        mu = (m[i] + inj[i]) - (m[j] + inj[j]) + (0.0 if g.neutral else self.h)
        return mu, max(S[i][i] + S[j][j] - 2 * S[i][j], 0.0)

    def win_prob(self, gi, home=True):
        mu, var = self._diff(gi)
        s = math.sqrt(self.sg ** 2 + var)
        b = self.tie_band
        ph = 1.0 - Phi((b - mu) / s)
        pa = Phi((-b - mu) / s)
        pt = max(0.0, 1.0 - ph - pa)
        return (ph, pt) if home else (pa, pt)

    def implied_spread(self, gi, home=True):
        mu, _ = self._diff(gi)
        return mu if home else -mu

    def ad_share(self, gi, home=True):
        m, S, bm, bS, inj = self._state()
        g = self.games[gi]
        i, j = (g.home, g.away) if home else (g.away, g.home)
        dr = (m[i] + inj[i]) - (m[j] + inj[j])
        vr = max(S[i][i] + S[j][j] - 2 * S[i][j], 0.0)
        mu = (bm[i] - bm[j]) + PHI_BRAND * dr
        var = (bS[i][i] + bS[j][j] - 2 * bS[i][j]) + SIGMA_V ** 2 + PHI_BRAND ** 2 * vr
        raw = 1.0 / (1.0 + math.exp(-mu / math.sqrt(1.0 + math.pi * var / 8.0)))
        # Supplement A: capture is the team's own take of the game's $2.50,
        # clamped; the opponent's capture is computed from THEIR book, not as
        # 1 - ours. The platform retains whatever the two captures leave.
        return min(CAP_HI, max(CAP_LO, raw))

    def team_games(self, team):
        i = self.idx[team] if isinstance(team, str) else team
        return [(gi, g, g.home == i) for gi, g in enumerate(self.games)
                if i in (g.home, g.away)]

    # -- risk --------------------------------------------------------------
    def sigma_remaining(self, team):
        """Var(W) = sum p(1-p) + [(sum a)^2 - sum a^2] * Var(own rating)

        The diagonal already carries rating uncertainty, because p integrates
        it. The off-diagonal is the covariance every remaining game shares
        through this team's own rating; opponents differ game to game, so they
        contribute no cross terms.
        """
        i = self.idx[team] if isinstance(team, str) else team
        _, S, _, _, _ = self._state()
        var, a = 0.0, []
        for gi, g, at_home in self.team_games(i):
            o = self.obs.get(gi)
            if o and o.final:
                continue
            if o and o.live:
                wp = o.wp_live if at_home else 1.0 - o.wp_live
                var += WIN_VALUE ** 2 * wp * (1 - wp)
                continue
            mu, v = self._diff(gi)
            s = math.sqrt(self.sg ** 2 + v)
            p, _ = self.win_prob(gi, at_home)
            var += WIN_VALUE ** 2 * p * (1 - p)
            a.append(WIN_VALUE * math.exp(-0.5 * (mu / s) ** 2) / (s * math.sqrt(2 * math.pi)))
        cov = (sum(a) ** 2 - sum(x * x for x in a)) * S[i][i]
        return math.sqrt(max(var + cov, 0.0))

    # -- value -------------------------------------------------------------
    def fair_value(self, team, days=None, discount=True) -> Legs:
        i = self.idx[team] if isinstance(team, str) else team
        m, S, _, _, inj = self._state()
        d = days if days is not None else YEARS * 365
        df = math.exp(-self.rate * d / 365.0) if discount else 1.0
        tie = TIE_VALUE if self.lg == "NFL" else 0.0
        bw = bt = bm_ = lv = fw = fm = 0.0
        for gi, g, at_home in self.team_games(i):
            o = self.obs.get(gi)
            if o and o.final:
                mg = o.margin if at_home else -o.margin
                bw += WIN_VALUE if mg > self.tie_band else 0.0
                bt += tie if abs(mg) <= self.tie_band else 0.0
            elif o and o.live:
                lv += WIN_VALUE * (o.wp_live if at_home else 1.0 - o.wp_live)
            else:
                p, pt = self.win_prob(gi, at_home)
                fw += WIN_VALUE * p + tie * pt
            if o and o.ad_share is not None:
                # the Tuesday print reports each team's own captured dollars;
                # ad_share here is stored from THIS team's perspective
                bm_ += AD_POOL * (o.ad_share if at_home else (o.ad_share_away
                                  if o.ad_share_away is not None else o.ad_share))
            else:
                fm += AD_POOL * self.ad_share(gi, at_home)
        sig = self.sigma_remaining(i)
        rc = -self.rp * self._gross0 * sig / self._sigma0 if (discount and self._gross0) else 0.0
        return Legs(df * bw, df * bt, df * bm_, df * lv, df * fw, df * fm, df * rc,
                    m[i] + inj[i], math.sqrt(S[i][i]), sig)

    def quote(self, team, touch=0.25):
        f = self.fair_value(team).fair
        return round(f - touch / 2, 4), round(f + touch / 2, 4)


# ---------------------------------------------------------------------------
# Calibration
# ---------------------------------------------------------------------------
def calibrate(lg: League, team, ipo, expected_wins, p_ref, mean_share):
    i = lg.idx[team]
    tg = lg.team_games(team)

    def set_opponents(sd):
        n = len(lg.m0)
        for k in range(n):
            for q in range(n):
                lg.S0[k][q] = sd ** 2 if k == q else 0.0
        s = math.sqrt(lg.sg ** 2 + 2 * sd ** 2)
        for (gi, g, at_home), p in zip(tg, p_ref):
            e = s * Phi_inv(p)                       # required edge, our view
            hf = 0.0 if g.neutral else (lg.h if at_home else -lg.h)
            opp = g.away if at_home else g.home
            lg.m0[opp] = lg.m0[i] + hf - e
        lg._cache = None

    def season_sigma(sd):
        set_opponents(sd)
        var, a = 0.0, []
        for gi, g, at_home in tg:
            mu, v = lg._diff(gi)
            s = math.sqrt(lg.sg ** 2 + v)
            p, _ = lg.win_prob(gi, at_home)
            var += p * (1 - p)
            a.append(math.exp(-0.5 * (mu / s) ** 2) / (s * math.sqrt(2 * math.pi)))
        return math.sqrt(max(var + (sum(a) ** 2 - sum(x * x for x in a)) * sd ** 2, 0.0))

    lo, hi = 0.1, 30.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if season_sigma(mid) < SIGMA_MKT[lg.lg]:
            lo = mid
        else:
            hi = mid
    set_opponents(0.5 * (lo + hi))

    lo2, hi2 = -8.0, 8.0
    for _ in range(90):
        mid = 0.5 * (lo2 + hi2)
        lg.bm0[i] = mid
        lg._cache = None
        if sum(lg.ad_share(gi, ah) for gi, _, ah in tg) / len(tg) < mean_share:
            lo2 = mid
        else:
            hi2 = mid
    lg.bm0[i] = 0.5 * (lo2 + hi2)
    lg._cache = None

    lg._gross0 = lg.fair_value(team, discount=False).fair
    lg._sigma0 = lg.sigma_remaining(team)
    lg.rp = 1.0 - (ipo / math.exp(-RATE * YEARS)) / lg._gross0
    return lg


LSU_P_REF = [0.9300, 0.8800, 0.7100, 0.6200, 0.8000, 0.5500,
             0.6600, 0.8600, 0.5800, 0.7500, 0.6800, 0.5300]
LSU_HOME = [True, True, False, False, True, False,
            True, True, False, True, False, False]
LSU_BRAND = [0.30, -0.25, 0.05, 0.15, -0.40, 0.10,
             -0.05, -0.60, 0.22, -0.15, 0.02, -0.10]


def build_lsu(ipo=59.535, expected_wins=8.55) -> League:
    names = ["LSU"] + [f"OPP{k+1}" for k in range(12)]
    sched = [Game(k + 1, 0 if LSU_HOME[k] else k + 1, k + 1 if LSU_HOME[k] else 0)
             for k in range(12)]
    lo, hi = -6.0, 6.0
    for _ in range(90):
        mid = 0.5 * (lo + hi)
        t = sum(1 / (1 + math.exp(-(math.log(x / (1 - x)) + mid))) for x in LSU_P_REF)
        if t < expected_wins:
            lo = mid
        else:
            hi = mid
    sh = 0.5 * (lo + hi)
    p = [1 / (1 + math.exp(-(math.log(x / (1 - x)) + sh))) for x in LSU_P_REF]
    lg = League(names, sched, "NCAA")
    for k in range(12):
        lg.bm0[k + 1] = LSU_BRAND[k]
    return calibrate(lg, "LSU", ipo, expected_wins, p, 0.600)


if __name__ == "__main__":
    lg = build_lsu()
    L = lg.fair_value("LSU")
    print(f"rating sd       {L.rating_sd:.3f} pts")
    print(f"gross E[V]      ${lg._gross0:.4f}")
    print(f"risk premium    {lg.rp*100:.3f}%")
    print(f"IPO             ${L.fair:.4f}   (published $59.535)")
    print(f"sigma           ${L.sigma_remaining:.4f}   (convention "
          f"${WIN_VALUE*SIGMA_MKT['NCAA']:.2f})")
    print("implied spreads " +
          " ".join(f"{lg.implied_spread(gi, ah):+.1f}" for gi, _, ah in lg.team_games("LSU")))
