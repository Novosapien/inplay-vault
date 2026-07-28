"""
InPlay Football Trading Challenge — IPO Pricing Engine v1.0
============================================================
Prices all 32 NFL + 138 NCAA universe team companies at IPO as the expected
terminal (liquidating) distribution per share:

    IPO_i = P_WIN * E[Wins_i]
          + P_TIE * E[Ties_i]                      (NFL only)
          + POOL  * sum_over_games E[CaptureShare_i,g]

Per SDMM-1 / Consolidated Novosapien Spec v1.3:
  P_WIN = $5.00/share, P_TIE = $2.50/share, loss = $0 (retained-earnings accrual)
  POOL  = $2.50 per game, split pro rata by counted share volume, capture
          clamped to [0.20, 0.80]; games vs non-universe opponents pay the
          universe team the full $2.50 (Spec v1.2).

ON-FIELD MODEL
  Devig BetMGM season win-total prices (proportional method) -> P(over).
  Season wins ~ Normal(mu, sigma_league); the posted line L and devigged
  p_over identify mu:  mu = L + sigma * Phi^-1(p_over).
  sigma is the market-implied dispersion of season wins around the total
  (NFL 17g: 2.7; NCAA 12g: 2.2 — tunable).

OFF-FIELD MODEL (Popularity Index @ IPO)
  Pop_i = W_BRAND * Brand_i + W_PERF * PerfIndex_i
    Brand_i:    hand-assigned 0-100 fanbase/brand tier (Base Demand proxy)
    PerfIndex:  100 * E[Wins]/Games  (traders follow winners)
  Pairwise expected capture vs opponent j (Bradley-Terry with concentration
  gamma):  s_ij = Pop_i^g / (Pop_i^g + Pop_j^g), clamped to [CLAMP_LO, CLAMP_HI].
  Schedule approximation (no exact schedules yet):
    NFL:  6 division games vs the 3 named rivals (exact pairings), 11 games vs
          the uniform non-division field.
    NCAA: OU games vs non-universe (full pool); of the remainder, CONF_FRAC
          are vs uniform conference mates, rest vs uniform national field.
  Exact 2026 schedules can be supplied via --schedule CSV (team,opponent) and
  override the approximation entirely.
"""
import math
import numpy as np
import pandas as pd
from scipy.stats import norm
import teams_config as tc

# ------------------------------------------------------------------ parameters
P_WIN, P_TIE, POOL = 5.00, 2.50, 2.50
GAMES = {"NFL": 17, "NCAAF": 12}
SIGMA = {"NFL": 2.7, "NCAAF": 2.2}
E_TIES_NFL = 0.08            # expected ties per NFL team per season
W_BRAND, W_PERF = 0.60, 0.40
GAMMA = 1.0                  # Bradley-Terry concentration exponent
CLAMP_LO, CLAMP_HI = 0.20, 0.80
CONF_FRAC = {"P4": 9/11, "G5": 8/11}   # conf games / in-universe FBS games
P4 = {"SEC", "Big Ten", "Big 12", "ACC"}
# Listing-price layer (Supplement A v1.3): variable discount on the contested
# (model-driven) share of value; no discount where guaranteed accrual dominates.
DISC_MIN, DISC_MAX = 0.01, 0.03   # discount band
GUAR_THRESHOLD = 0.20             # guaranteed accrual share of EV above which d = 0
# Listed prices are FULL PRECISION — no rounding (per InPlay direction to novosapien).

# ------------------------------------------------------------------ on-field
def american_to_prob(o):
    return 100.0 / (o + 100.0) if o > 0 else -o / (-o + 100.0)

def devig(over, under):
    qo, qu = american_to_prob(over), american_to_prob(under)
    return qo / (qo + qu)

def expected_wins(line, p_over, sigma):
    return line + sigma * norm.ppf(p_over)

# ------------------------------------------------------------------ off-field
def capture(pi, pj):
    s = pi**GAMMA / (pi**GAMMA + pj**GAMMA)
    return min(max(s, CLAMP_LO), CLAMP_HI)

def build(odds_path="odds.csv", schedule_path=None):
    df = pd.read_csv(odds_path)
    df["p_over"] = [devig(o, u) for o, u in zip(df.over_price, df.under_price)]
    df["exp_wins"] = [expected_wins(l, p, SIGMA[lg])
                      for l, p, lg in zip(df.win_total, df.p_over, df.league)]
    df["games"] = df.league.map(GAMES)
    df["perf_index"] = 100.0 * df.exp_wins / df.games

    brand = {}
    for t in df.itertuples():
        src = tc.NFL_BRAND if t.league == "NFL" else tc.NCAA_BRAND
        if t.team not in src:
            raise KeyError(f"No brand score for {t.team}")
        brand[t.team] = src[t.team]
    df["brand"] = df.team.map(brand)
    df["pop"] = W_BRAND * df.brand + W_PERF * df.perf_index
    pop = dict(zip(df.team, df["pop"]))

    sched = None
    if schedule_path:
        sched = pd.read_csv(schedule_path)   # columns: team, opponent ('' = OOU)

    rows = []
    nfl = df[df.league == "NFL"]
    ncaa = df[df.league == "NCAAF"]
    div_of = {t: d for d, ts in tc.NFL_DIVISIONS.items() for t in ts}

    # ---------------- NFL
    nfl_teams = list(nfl.team)
    for t in nfl.itertuples():
        if sched is not None:
            opps = sched[sched.team == t.team].opponent.tolist()
            caps = [capture(pop[t.team], pop[o]) for o in opps]
            off = POOL * sum(caps)
            avg_cap = np.mean(caps)
        else:
            rivals = [x for x in tc.NFL_DIVISIONS[div_of[t.team]] if x != t.team]
            div_caps = [capture(pop[t.team], pop[r]) for r in rivals]  # x2 each
            field = [x for x in nfl_teams if x != t.team and x not in rivals]
            field_caps = [capture(pop[t.team], pop[o]) for o in field]
            e_div = np.mean(div_caps)
            e_field = np.mean(field_caps)
            avg_cap = (6 * e_div + 11 * e_field) / 17
            off = POOL * (6 * e_div + 11 * e_field)
        onf = P_WIN * t.exp_wins + P_TIE * E_TIES_NFL
        rows.append(dict(league="NFL", team=t.team, conf=div_of[t.team],
                         win_total=t.win_total, p_over=t.p_over,
                         exp_wins=t.exp_wins, brand=t.brand, pop=t.pop,
                         avg_capture=avg_cap, oou_games=0,
                         onfield_ev=onf, offfield_ev=off, ipo=onf + off))

    # ---------------- NCAA
    ncaa_teams = list(ncaa.team)
    for t in ncaa.itertuples():
        conf = tc.NCAA_CONF[t.team]
        oou = tc.OUT_OF_UNIVERSE_OVERRIDES.get(t.team, tc.DEFAULT_OUT_OF_UNIVERSE)
        if sched is not None:
            g = sched[sched.team == t.team]
            oou = g.opponent.isna().sum()
            caps = [capture(pop[t.team], pop[o]) for o in g.opponent.dropna()]
            off = POOL * (sum(caps) + oou * 1.0)
            avg_cap = np.mean(caps) if caps else np.nan
        else:
            in_univ = GAMES["NCAAF"] - oou
            mates = [x for x in ncaa_teams
                     if x != t.team and tc.NCAA_CONF[x] == conf]
            field = [x for x in ncaa_teams if x != t.team]
            e_conf = (np.mean([capture(pop[t.team], pop[m]) for m in mates])
                      if mates else np.nan)
            e_field = np.mean([capture(pop[t.team], pop[o]) for o in field])
            if conf in ("Independent", "FCS-Universe") or not mates:
                avg_cap = e_field
            else:
                cf = CONF_FRAC["P4"] if conf in P4 else CONF_FRAC["G5"]
                n_conf = min(round(cf * in_univ), in_univ)
                avg_cap = (n_conf * e_conf + (in_univ - n_conf) * e_field) / in_univ
            off = POOL * (in_univ * avg_cap + oou * 1.0)
        onf = P_WIN * t.exp_wins
        rows.append(dict(league="NCAAF", team=t.team, conf=conf,
                         win_total=t.win_total, p_over=t.p_over,
                         exp_wins=t.exp_wins, brand=t.brand, pop=t.pop,
                         avg_capture=avg_cap, oou_games=oou,
                         onfield_ev=onf, offfield_ev=off, ipo=onf + off))

    out = pd.DataFrame(rows)
    # --- listing-price layer ---
    out["guaranteed_ev"] = POOL * out.oou_games
    out["guar_share"] = out.guaranteed_ev / out.ipo
    out["contested_off_share"] = (out.offfield_ev - out.guaranteed_ev) / out.ipo
    disc = []
    for lg in ["NFL", "NCAAF"]:
        sub = out[out.league == lg]
        lo, hi = sub.contested_off_share.min(), sub.contested_off_share.max()
        u = (sub.contested_off_share - lo) / (hi - lo)
        d = DISC_MIN + (DISC_MAX - DISC_MIN) * u
        d = d.where(sub.guar_share <= GUAR_THRESHOLD, 0.0)   # no-discount rule
        disc.append(d)
    out["discount"] = pd.concat(disc)
    out["listed_price"] = out.ipo * (1.0 - out.discount)     # full precision, no rounding
    return out

if __name__ == "__main__":
    res = build()
    res.to_csv("ipo_prices.csv", index=False)
    for lg in ["NFL", "NCAAF"]:
        sub = res[res.league == lg].sort_values("ipo", ascending=False)
        print(f"\n=== {lg} ({len(sub)} teams) — top/bottom 8 ===")
        cols = ["team", "exp_wins", "avg_capture", "onfield_ev", "offfield_ev", "ipo", "discount", "listed_price"]
        print(sub[cols].head(8).to_string(index=False,
              float_format=lambda x: f"{x:,.2f}"))
        print("...")
        print(sub[cols].tail(8).to_string(index=False,
              float_format=lambda x: f"{x:,.2f}"))
    print(f"\nTeams priced: {len(res)}  (NFL {len(res[res.league=='NFL'])}, "
          f"NCAA {len(res[res.league=='NCAAF'])})")
