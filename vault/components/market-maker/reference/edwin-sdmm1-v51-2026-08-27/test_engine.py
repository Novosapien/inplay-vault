"""Acceptance suite for novo_engine v5. Every check is a property of the
model, not a snapshot of its output."""
import math
from statistics import NormalDist
import novo_engine as E
from novo_engine import League, Game

N = NormalDist()
PASS = []


def check(name, ok, detail=""):
    PASS.append(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name:<52} {detail}")


def fresh():
    return E.build_lsu()


def integrate(f, mu, sd, n=4001):
    """E[f(x)], x ~ N(mu, sd^2), midpoint rule on the probability scale."""
    return sum(f(mu + N.inv_cdf((q + 0.5) / n) * sd) for q in range(n)) / n


lg = fresh()
tg = lg.team_games("LSU")
base = lg.fair_value("LSU")

print("\nT1  CALIBRATION")
check("fair value at t=0 equals the published offer",
      abs(base.fair - 59.535) < 0.005, f"${base.fair:.4f}")
ps = [lg.win_prob(gi, ah)[0] for gi, _, ah in tg]
check("every per-game probability matches the feed",
      max(abs(a - b) for a, b in zip(ps, E.LSU_P_REF)) < 1e-9, f"sum {sum(ps):.4f}")
check("sigma equals the SIGMA_MKT convention",
      abs(base.sigma_remaining - 11.0) < 0.005, f"${base.sigma_remaining:.4f}")
sh = sum(lg.ad_share(gi, ah) for gi, _, ah in tg) / 12
check("mean marketing share equals the implied beta", abs(sh - 0.600) < 2e-3, f"{sh:.4f}")

print("\nT2  IDEMPOTENCE — the v4 bug that would have drifted all afternoon")
l2 = fresh()
l2.set_obs(0, wp_live=0.7, proj_margin=10.0, elapsed=0.3)
a = l2.fair_value("LSU").fair
for _ in range(200):
    l2.set_obs(0, wp_live=0.7, proj_margin=10.0, elapsed=0.3)
check("200 repeats of the same live tick", abs(l2.fair_value("LSU").fair - a) < 1e-12,
      f"drift ${l2.fair_value('LSU').fair - a:+.1e}   (v4: -$1.18 after ONE repeat)")
l2.set_injury("OPP6", "QB")
c = l2.fair_value("LSU").fair
for _ in range(200):
    l2.set_injury("OPP6", "QB")
check("200 repeats of the same injury", abs(l2.fair_value("LSU").fair - c) < 1e-12,
      f"drift ${l2.fair_value('LSU').fair - c:+.1e}")

print("\nT3  SPREADS — the weekly recalibration channel")
l2 = fresh()
gi, g, ah = tg[5]
mu0, v0 = l2._diff(gi)
p0 = l2.win_prob(gi, ah)[0]
b0 = l2.fair_value("LSU").fair
print(f"     week 6: model rating edge {mu0 if ah else -mu0:+.1f}, "
      f"our WP {p0:.3f}, uncertainty on the edge ±{math.sqrt(v0):.1f} pts")
l2.set_obs(gi, spread=mu0)          # board confirms the model exactly
mu1, v1 = l2._diff(gi)
check("a posted spread collapses that game's edge uncertainty",
      math.sqrt(v1) < 0.5 * math.sqrt(v0),
      f"±{math.sqrt(v0):.1f} -> ±{math.sqrt(v1):.1f} pts")
check("a confirming spread leaves the edge itself alone",
      abs(mu1 - mu0) < 1e-9, f"{mu0:+.3f} -> {mu1:+.3f}")

# martingale over the predictive of the posted spread
def price_given_spread(S):
    l3 = fresh()
    l3.set_obs(gi, spread=S)
    return l3.fair_value("LSU", discount=False).fair


pred_sd = math.sqrt(v0 + E.SIGMA_SPREAD ** 2)
em = integrate(price_given_spread, mu0, pred_sd, 801)
before = fresh().fair_value("LSU", discount=False).fair
check("E[price | spread posts] equals price before", abs(em - before) < 0.01,
      f"bias ${em - before:+.5f}")

# the wrong way: price the game straight off the raw spread
s_only = math.sqrt(l2.sg ** 2)
raw = integrate(lambda S: 5 * (1 - N.cdf(-S / s_only)), mu0, pred_sd, 801)
filt = 5 * fresh().win_prob(gi, ah)[0]
check("raw Phi(spread/sigma_g) is biased — filtering is not",
      abs(raw - filt) > 0.02,
      f"raw ${raw:.4f} vs correct ${filt:.4f}  (${raw-filt:+.4f} per game)")

print("\n     Weekly board posting, spreads matching the model:")
l3 = fresh()
print(f"     {'week':>5} {'sigma':>9} {'rating sd':>11}")
print(f"     {0:5d} {l3.fair_value('LSU').sigma_remaining:9.3f} "
      f"{l3.fair_value('LSU').rating_sd:11.3f}")
for k in range(0, 12):
    mu, _ = l3._diff(k)
    l3.set_obs(k, spread=mu)
    if k in (0, 2, 5, 8, 11):
        L = l3.fair_value("LSU")
        print(f"     {k+1:5d} {L.sigma_remaining:9.3f} {L.rating_sd:11.3f}")
check("posting the board collapses risk",
      l3.fair_value("LSU").sigma_remaining < 0.75 * base.sigma_remaining,
      f"sigma {base.sigma_remaining:.2f} -> {l3.fair_value('LSU').sigma_remaining:.2f}")
# A board that CONFIRMS the model is not a neutral path: LSU is favoured in all
# twelve, and collapsing the edge uncertainty pushes every p away from 0.5, so
# all twelve move up. The neutral statement is the expectation over the
# predictive of the spreads, which T3 already checks.
check("confirming spreads lift a team favoured everywhere",
      l3.fair_value("LSU").fair > base.fair,
      f"${base.fair:.3f} -> ${l3.fair_value('LSU').fair:.3f}; "
      f"E[wins] {sum(fresh().win_prob(gi, ah)[0] for gi, _, ah in tg):.2f} -> "
      f"{sum(l3.win_prob(gi, ah)[0] for gi, _, ah in tg):.2f}")

print("\nT4  MARTINGALE — results")
worst = 0.0
for k in range(4):
    l3 = fresh()
    for w in range(k):
        mu, _ = l3._diff(w)
        l3.set_obs(w, margin=mu)
    b = l3.fair_value("LSU", discount=False).fair
    mu, var = l3._diff(k)
    sd = math.sqrt(l3.sg ** 2 + var)

    def px(m, k=k, obs=dict(l3.obs)):
        l4 = fresh()
        for gi2, o in obs.items():
            l4.obs[gi2] = o
        l4.set_obs(k, margin=m)
        return l4.fair_value("LSU", discount=False).fair

    worst = max(worst, abs(integrate(px, mu, sd, 801) - b))
check("|E[V after the game] - V before|", worst < 0.01, f"worst ${worst:.5f}")

print("\nT5  MARTINGALE — the Tuesday ad print")
l3 = fresh()
gi0, g0, ah0 = tg[0]
l3.set_obs(gi0, margin=l3._diff(gi0)[0])
b = l3.fair_value("LSU", discount=False).fair
m, S, bm, bS, inj = l3._state()
i, j = (g0.home, g0.away)
mu_l = (bm[i] - bm[j]) + E.PHI_BRAND * ((m[i] + inj[i]) - (m[j] + inj[j]))
sd_l = math.sqrt(bS[i][i] + bS[j][j] - 2 * bS[i][j] + E.SIGMA_V ** 2)


def px_ad(x):
    l4 = fresh()
    l4.set_obs(gi0, margin=l4._diff(gi0)[0])
    l4.set_obs(gi0, ad_share=1 / (1 + math.exp(-x)))
    return l4.fair_value("LSU", discount=False).fair


check("|E[V after the print] - V before|",
      abs(integrate(px_ad, mu_l, sd_l, 801) - b) < 0.01,
      f"bias ${integrate(px_ad, mu_l, sd_l, 801) - b:+.5f}")
l4 = fresh()
r0 = l4.fair_value("LSU").rating
l4.set_obs(gi0, ad_share=0.85 if ah0 else 0.15)
check("an ad print never moves the on-field rating",
      abs(l4.fair_value("LSU").rating - r0) < 1e-12, "0.0 pts")

print("\nT6  OPPONENT NEWS")
l3 = fresh()
b0 = l3.fair_value("LSU").fair
gi5, g5, ah5 = tg[5]
opp = g5.away if ah5 else g5.home
p_b = l3.win_prob(gi5, ah5)[0]
l3.set_injury(opp, "QB")
check("opponent QB injury moves the price",
      l3.fair_value("LSU").fair - b0 > 0.2,
      f"${l3.fair_value('LSU').fair - b0:+.3f}  WP {p_b:.3f} -> {l3.win_prob(gi5, ah5)[0]:.3f}")
check("without touching LSU's own rating",
      abs(l3.fair_value("LSU").rating - base.rating) < 1e-12, "0.0 pts")
mv = []
for gi2, g2, ah2 in tg:
    l4 = fresh()
    v = l4.fair_value("LSU").fair
    l4.set_injury(g2.away if ah2 else g2.home, "QB")
    mv.append((abs(0.5 - l4.win_prob(gi2, ah2)[0]), l4.fair_value("LSU").fair - v))
mv.sort()
check("closest games reprice hardest", mv[0][1] > mv[-1][1] * 2.5,
      f"${mv[0][1]:+.3f} vs ${mv[-1][1]:+.3f}")
l4 = fresh()
l4.set_obs(gi5, spread=l4._diff(gi5)[0])       # board already hung the game
v = l4.fair_value("LSU").fair
l4.set_injury(opp, "QB")
check("an injury invalidates the stale spread it post-dates",
      l4.stale_spreads() == [gi5], f"game {gi5} flagged for re-posting")
# Net of two effects: the injury is worth +$0.76, but invalidating the spread
# gives back the certainty the board had provided on a game LSU was favoured
# in (-$0.62). Both are real; the sum is what the tape should print.
l5 = fresh(); l5.set_obs(gi5, spread=l5._diff(gi5)[0])
gain = mv[[round(x[1], 3) for x in mv].index(round(
    max(y[1] for y in mv if abs(y[1] - 0.759) < 0.01), 3))][1] if False else None
l6 = fresh(); l6.set_injury(opp, "QB")
inj_alone = l6.fair_value("LSU").fair - base.fair
cert = l5.fair_value("LSU").fair - base.fair
net = l4.fair_value("LSU").fair - v
check("and the injury prices correctly through it",
      net > 0 and abs(net - (inj_alone - cert)) < 1e-9,
      f"${net:+.3f} = injury ${inj_alone:+.3f} less lost certainty ${cert:+.3f}"
      f"   (unfixed: -$3.573, wrong sign)")

print("\nT7  SETTLEMENT — accrual, nothing paid until the season ends")
l3 = fresh()
w = 0
for k in range(12):
    at_home = l3.games[k].home == 0
    own = 10.0 if k % 3 else -10.0
    # Retention convention: each side's capture is printed from its OWN book.
    # LSU captures 0.6 every week; the opponent's capture is independent
    # (here 0.3 — the platform retains the 0.1 residual).
    if at_home:
        l3.set_obs(k, margin=own, ad_share=0.6, ad_share_away=0.3)
    else:
        l3.set_obs(k, margin=-own, ad_share=0.3, ad_share_away=0.6)
    w += 1 if own > 0 else 0
L = l3.fair_value("LSU", days=0.0)
check("P at settlement equals $5*W + A", abs(L.fair - (5 * w + 18.0)) < 1e-9,
      f"${L.fair:.4f} = 5x{w} + $18.000")
check("sigma at settlement is zero", L.sigma_remaining < 1e-12, "$0.00")

print("\nT8  IN-PLAY")
mx = 0.0
for el in [0.1, 0.5, 0.9]:
    for wp in [0.2, 0.5, 0.8]:
        l3 = fresh()
        l3.set_obs(0, wp_live=wp if l3.games[0].home == 0 else 1 - wp,
                   proj_margin=(wp - .5) * 40, elapsed=el)
        mx = max(mx, abs(l3.fair_value("LSU").live_game
                         - math.exp(-E.RATE * E.YEARS) * 5 * wp))
check("game leg equals $5 x WP_live exactly", mx < 1e-12, f"${mx:.1e}")
step = 0.0
for k in range(3):
    a_, b_ = fresh(), fresh()
    for w2 in range(k):
        for l_ in (a_, b_):
            l_.set_obs(w2, margin=l_._diff(w2)[0])
    a_.set_obs(k, wp_live=1.0, proj_margin=21.0, elapsed=1.0)
    b_.set_obs(k, margin=21.0)
    step = max(step, abs(a_.fair_value("LSU").fair - b_.fair_value("LSU").fair))
check("no price step at the final whistle", step < 0.02, f"${step:.4f}")

print("\nT9  NFL TIES")
nfl = League(["A", "B"], [Game(1, 0, 1)], "NFL")
p, pt = nfl.win_prob(0)
check("ties carry probability in the NFL", pt > 0.001, f"win {p:.4f}  tie {pt:.4f}")
ncaa = League(["A", "B"], [Game(1, 0, 1)], "NCAA")
check("no ties in NCAA", ncaa.win_prob(0)[1] == 0.0, "0.0000")

print("\nT10  PRODUCT BEHAVIOURS")
sp = lg.implied_spread(tg[0][0], tg[0][2])
ah0 = tg[0][2]


def after(own_margin):
    l3 = fresh()
    l3.set_obs(0, margin=own_margin if ah0 else -own_margin)
    return l3.fair_value("LSU").fair


b0 = base.fair
print(f"      (LSU is favoured by {sp:.1f} in week 1)")
check("price FALLS on an ugly win", after(2.0) < b0, f"${after(2.0)-b0:+.2f} winning by 2")
check("winning at the number is roughly neutral", abs(after(sp) - b0) < 1.5,
      f"${after(sp)-b0:+.2f}")
check("a big win moves it hard", after(sp + 30) - b0 > 4.0, f"${after(sp+30)-b0:+.2f}")
check("favourite asymmetry holds", abs(after(-7) - b0) > 1.5 * (after(sp + 30) - b0),
      f"win ${after(sp+30)-b0:+.2f} vs loss ${after(-7)-b0:+.2f}")
l_e = fresh(); l_e.set_obs(0, margin=(sp + 30) if ah0 else -(sp + 30))
early = l_e.fair_value("LSU").fair - b0
l_l = fresh()
for k in range(10):
    l_l.set_obs(k, margin=l_l._diff(k)[0])
v1 = l_l.fair_value("LSU").fair
ahk = l_l.games[10].home == 0
l_l.set_obs(10, margin=l_l._diff(10)[0] + (30 if ahk else -30))
check("early result outweighs the same result late",
      early > l_l.fair_value("LSU").fair - v1,
      f"week 1 ${early:+.2f} vs week 11 ${l_l.fair_value('LSU').fair - v1:+.2f}")

print(f"\n{'='*76}\n  {sum(PASS)}/{len(PASS)} passed\n{'='*76}")
