# Call questions — 29 July 2026

> **Component:** [[market-maker/market-maker]]
> **Authority (George, 29-07):** the **IPO Draft Business Requirements v2**
> (28 July) and `reference/season-win-totals-170.csv` are **gospel**. Where
> either disagrees with an email, a spreadsheet or the earlier Supplement,
> they win. What follows is only where **v2 disagrees with itself**, or where
> nothing covers the point at all.

**The deadline is secondary trading, not the season.**

```
NCAA secondary trading   26 or 27 August   ← 4 weeks away
NFL  secondary trading   7 September
```

---

## 1 · Where v2 contradicts itself

### 1.1 Is the market maker's mandate 10 rounds, 16, or 18?

**What the mandate is.** The offering runs in rounds. In each round every team
gets a one-minute window and 50,000 shares are made available. Participants
buy what they want. **At the close of the window the market maker must buy
every share they did not take** — that is the Primary Mandate. After the
mandate expires the market maker buys nothing more in the primary, and the
remaining rounds sell to participants only.

**The problem.** v2 gives three different answers for how many rounds the
mandate covers.

| Section | Says |
|---|---|
| §2.2 | "MM completion sweep (Rounds **1-18**)" |
| §3 | "Rounds **1-16** (MM Primary Mandate in force)" |
| §4 | "for Rounds **1 through 10**… From Round 11, the mandate expires" |

Section 3 also disagrees with itself — the heading says 1-16, then the same
bullet ends *"Float equality through Round 10 is exact by construction."*

**What it costs.** Rounds × 50,000 shares × 170 teams is our maximum opening
position.

```
10 rounds    85,000,000 shares    $4.26 bn
16 rounds   136,000,000 shares    $6.82 bn
18 rounds   153,000,000 shares    $7.67 bn
```

**Which looks right.** v2 itself quotes $4.26 bn, which only works for 10
rounds. But 18 × 50,000 = 900,000, which is **exactly** the NFL float. That is
unlikely to be a coincidence, so 18 looks intended and the 10 and 16 look like
leftovers from the earlier draft.

*Why it matters: this is our opening position. Every inventory rule in
Chapters 4 and 5 is calculated from it.*

### 1.2 When does NCAA secondary trading start — 26 or 27 August?

- §1.1 — *"Secondary Trading Start: August **27** at 9:30am ET"*
- §5.2 — *"Secondary trading begins: NCAA: August **26** at 9:30am ET"*

*Why it matters: this is the date the market maker must be quoting. It is the
hardest deadline we have, and it is four weeks away.*

### 1.3 When does the NCAA offering end — 26 or 28 August?

- §1.1 — *"Initial Offerings End: August **26** at 10pm ET"*
- §2.1 — *"running continuously to completion on August **28**, 2026 at
  10:00pm ET"*

Put §1.1 and §5.2 together and secondary trading opens at 9:30am on the 26th
while the primary is still running until 10pm the same day. That cannot be
intended.

*Why it matters: we need to know when the primary stops and the secondary
starts, and they must not overlap.*

### 1.4 NCAA teams have 1,000,000 shares, but only 900,000 are ever offered.

Eighteen rounds at 50,000 shares is 900,000. §5.1 says each NCAA team company
begins with **1,000,000 shares outstanding**.

So 100,000 shares per team — 13.8 million across the 138 teams — never reach
an offering window.

*Why it matters: §4.3 divides our holding by the float to get the Position
Ratio. We need to know whether those 100,000 shares count as issued, or as
treasury shares that sit outside the float.*

### 1.5 Is the NFL offering 8 hours or 10?

§2.2 says *"Total scheduled offering time: 8 hours"*. The table directly below
it shows 5 September 1:00–6:00 PM and 6 September 1:00–6:00 PM. That is five
hours plus five hours.

*Why it matters: small, but 18 rounds × 32 teams × 1 minute is 9.6 hours, which
fits 10 and does not fit 8.*

---

## 2 · Not covered anywhere

### 2.1 How are we meant to sell the position down?

**Why we must.** Not for profit — the spec excludes profit as a motive, and we
have unlimited money. The reason is that **a market with no shares in
circulation is not a market**. If we hold most of every team, participants have
nothing to trade with each other. And §3.6.3 says market-maker volume never
counts toward the off-field value, so our own trading does not help the
Popularity Index either.

**The one tool we have.** When we hold a lot, we shift both our prices down.
Lower prices discourage people selling to us and encourage them to buy from us.
The spec calls that shift the Inventory Adjustment.

**The tool is stuck.** The shift is our holding as a share of the float,
multiplied by $1.00, capped at 25 cents.

```
hold 25% of the float   →  shift down 25 cents   ← the cap
hold 50%                →  shift down 25 cents
hold 90%                →  shift down 25 cents
```

We cross 25% on day one and never come back under it while we are
distributing. So the number reads the same whether we hold 900,000 shares or
250,000. It gives no signal, and 25 cents on a $50 share is half of one
percent.

*Ask: should the cap be larger while we distribute? Is there an expectation of
how fast? Or is distribution not the market maker's job at all?*

### 2.2 Shorting — two things v2 does not say.

v2 allows the full float to be sold short in the secondary market. That was in
neither the build spec nor the Supplement.

- Is the cap on **total** short interest across all participants, or per
  participant?
- May the **market maker** go short?

**Why it matters.** Shorting means participants can sell us shares that do not
exist. So what can be sold to us is the float **plus** the short interest —
2,000,000 rather than 1,000,000. Our Position Ratio can then exceed 1.0, and
the spec has no inventory limit: *"inventory never prevents quoting"* (§4.1).

### 2.3 Is the listed IPO price rounded to a penny, or full precision?

- **Your email:** *"at full precision — no rounding anywhere."*
- **The workbook Parameters sheet:** *"IPO price tick $0.01 — rounding
  increment for listed IPO price."*

All 170 listed prices in the workbook are exact pennies, so the workbook
rounds.

*Why it matters: our Reference Price seeds at your EV and our first quotes are
built around it. A penny of disagreement is a penny of mispricing across 166
million shares.*

### 2.4 Is `inplay_feed/ipo.py` superseded by the workbook?

You sent the IPO calculation twice — as `engine.py` and as a Python module,
`inplay_feed/ipo.py`. They disagree in two places, and the workbook agrees with
`engine.py` both times.

| | Workbook and `engine.py` | `ipo.py` |
|---|---|---|
| NFL ties | 0.08 per team → **$0.20** a share | 0.4% of games → **$0.17** |
| Discount | normalised per league | flat scale |

*Why it matters: we want one authority. Otherwise every number has to be
checked against three sources.*

---

## 3 · Data we still need

### 3.1 Please send the 2026 schedule.

Two rules need it.

- **§3.6** gives every game a $2.50 advertising pool, split between the two
  teams. We cannot split it without knowing who plays whom.
- **§2.5** counts regular-season games only. Without the schedule we cannot
  keep postseason games out of the price.

### 3.2 Will the daily feed carry real Sportradar competitor IDs?

The sample file uses placeholders such as `sr:competitor:nfl0`.

*Why it matters: real IDs join your feed to our live probability feed directly.
Placeholders mean building and maintaining a mapping table.*

---

## 4 · What we build

### 4.1 Do we calculate expected wins, or read your number?

You sent the method and said to port it. Your daily feed already publishes the
answer for both leagues.

**What we know.** Our de-vig reproduces yours exactly — across all 170 teams
the largest difference is 8.88 × 10⁻¹⁶, which is floating-point noise. And no
Sportradar product carries season win totals for college, so the 138 college
numbers can only come from you.

*Ask: shall we compute the 32 NFL numbers ourselves as a check against yours?*

### 4.2 We will build an upload page for the daily file. Are you content?

You upload the file. We validate it on screen with the same checks your
publisher runs. A bad file is rejected immediately, with the reason, so you fix
it at your desk rather than hearing from us hours later. We keep every file,
including rejected ones, in perpetuity.

*Also confirm you can automate the upload later against the same endpoint, so a
person is not needed every day at 06:00 ET.*

---

## 5 · Two old ones, if there is time

### 5.1 Quote lifecycle — do orders top up, or rest until gone?

The spec refills an order once it is half eaten, after 15 seconds (§5.9). On
23 July you said orders rest until completely gone, with no top ups. **E17.**

### 5.2 Cadence — 2 seconds or 200 milliseconds?

The spec sweeps every 2.0 seconds and calls a 5-second-old probability current
(§3.1.4, §3.3.1). On the call you said 200 milliseconds.

Our own measurement of a real game: Sportradar's probabilities move with a
**4-second median**, and **88%** of readings move the quote by at least one
tick. **E18.**

*Both block Chapter 5, which we reach after Chapter 4.*

---

## 6 · Answered — do not raise

| Question | Answer | Source |
|---|---|---|
| Shares per team | **NFL 900,000 · NCAA 1,000,000** | v2 §1.2, §5.1 — supersedes the 875,000 in the email |
| Does the market maker buy 85% of unsold shares, or all? | **All of them** — supersedes spec §9.2 | v2 §4 |
| Who sells in the primary? | **InPlay Markets**, exclusively. We only buy | v2 §2 |
| Can participants sell or short during the offering? | **No.** Buy only | v2 §2 |
| §5.2.3 says NFL twice with different numbers | **5.2.3 means NCAA** — 1,000,000 | George, 29-07 |
| The IPO EV for each team | **Have it** — all 170 | `reference/ipo-prices-170.csv` |
| The listed price for each team | **Have it** — same file | as above |
| The 170-team list | **Have it** — 138 NCAAF + 32 NFL | `season-win-totals-170.csv` |
| `odds.csv` | **Have it** — the same file | as above |
| `teams_config.py` | **Not needed.** The workbook carries Brand, Popularity, Capture and out-of-universe games per team | IPO workbook |
| Which sigma? | **2.7 NFL · 2.2 NCAA** | workbook Parameters sheet |
| Do both sides of the over/under come priced? | **Yes**, all 170, and every line is half-point | `season-win-totals-170.csv` |
| Washington Commanders is priced off DraftKings | **Stands.** The CSV is gospel, so the price is the price | `season-win-totals-170.csv` |
