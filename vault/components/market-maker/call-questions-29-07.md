# Call questions — 29 July 2026

> **Component:** [[market-maker/market-maker]]
> **For:** the call with Edwin / InPlay today.
> **Sources:** Edwin's answers of 28-07 · his share-count email of 29-07 ·
> `InPlay_IPO_Pricing_2026.xlsx` · **IPO Draft Business Requirements v2
> (28 July)** · the IPO Supplement v1.3 · his code in `reference/`.

**Everything in sections 1 to 6 is open.** Answered items are at the bottom,
with their answers, so nobody raises them by mistake.

**The clock has moved.** Secondary trading, not the season, is now the
deadline.

```
NCAA secondary trading starts   26 or 27 August   ← 28 days
NFL  secondary trading starts   7 September
```

---

## 1 · The four that matter most

### 1.1 When must the market maker be quoting?

Requirements v2 says secondary trading starts on **26 August** in one place
and **27 August** in another. Either way it is four weeks away, and it is
much earlier than the season.

Also confirm what we must do in the **primary**. v2 says *"InPlay Markets
will be the exclusive seller of all initial offerings"*, and the market maker
buys what is left. Is that purchase executed by our engine, or by the
platform?

**Why it matters.** It sets our build order today.

### 1.2 Is the mandate 10 rounds, 16 rounds, or 18?

Requirements v2 gives all three.

| Section | Says |
|---|---|
| §2.2 | "MM completion sweep (Rounds **1-18**)" |
| §3 | "Rounds **1-16** (MM Primary Mandate in force)" |
| §4 | "for Rounds **1 through 10**… From Round 11, the mandate expires" |

Section 3 also disagrees with itself: the heading says 1-16, and the same
bullet ends *"Float equality through Round 10 is exact by construction."*

**Why it matters.** It sets our opening position, and the range is enormous.

```
10 rounds   85,000,000 shares    $4.26 bn
16 rounds  136,000,000 shares    $6.82 bn
18 rounds  153,000,000 shares    $7.67 bn
```

The document itself quotes $4.26 bn, which only holds for 10 rounds. But
18 × 50,000 = 900,000, which is exactly the NFL float. That suggests 18 is
intended and the others are leftovers.

### 1.3 Shorting is new. Please confirm the rules.

v2 allows the full float to be sold short in the secondary market. Neither
the build spec nor the IPO Supplement mentioned shorting.

Confirm three things:

- §5.2.3 says *"NFL team company has 1,000,000 shares available for
  shorting"* and §5.2.4 says *"NFL… 900,000"*. Both say NFL. We read 5.2.3 as
  NCAA. Correct?
- Is the cap on **total** short interest across all participants, or per
  participant?
- Can the market maker itself go short?

**Why it matters.** Shorting doubles what can be sold to us.

```
shares that can be sold to us  =  float + short interest
                               =  1,000,000 + 1,000,000  =  2,000,000
```

So our position can exceed the entire float, and the Position Ratio (§4.3)
can go above 1.0. The spec has no inventory limit — *"inventory never
prevents quoting"* (§4.1).

### 1.4 How do we sell the position down?

After the offering we hold a very large position. The spec gives us one tool:
when we hold a lot, we lower our prices to attract buyers. That is the
inventory skew.

**The tool is at its limit from the first minute and never moves.**

```
hold  250,000 shares  →  shade the price down 25 cents
hold  500,000 shares  →  shade the price down 25 cents
hold  900,000 shares  →  shade the price down 25 cents
```

Above a quarter of the float the cap binds and stays bound. Holding the
entire float looks the same as holding a quarter of it.

Twenty-five cents on a $50 share is half of one percent.

**Three things to ask:**

- Is there an expectation about how quickly we distribute?
- Should the cap `M` be larger during distribution?
- Or is distribution not the market maker's job?

---

## 2 · Numbers that disagree across documents

### 2.1 Is the NFL float 875,000 or 900,000?

| Source | NFL | NCAA |
|---|---|---|
| Your email, 29 July | **875,000** | 1,000,000 |
| Requirements v2, §1.2 and §5.1 | **900,000** | 1,000,000 |

NCAA agrees. NFL does not.

### 2.2 When does the NCAA offering end, and when does secondary start?

- §1.1 — offerings end **26 August** 10pm, secondary starts **27 August**.
- §2.1 — the offering runs to completion on **28 August** 10pm.
- §5.2 — secondary starts **26 August** 9:30am.

Taken together, secondary trading opens 12 hours before the primary closes.

### 2.3 Is the listed IPO price rounded to a penny, or full precision?

- **Your email:** *"at full precision — no rounding anywhere."*
- **The workbook Parameters sheet:** *"IPO price tick $0.01 — rounding
  increment for listed IPO price."*

All 170 listed prices in the workbook are exact pennies, so the workbook
rounds.

**Why it matters.** We must reproduce your price exactly on day one.

### 2.4 Is `inplay_feed/ipo.py` superseded by the workbook?

The workbook settles two differences between your files, and `engine.py` wins
both.

| | Workbook | `ipo.py` |
|---|---|---|
| NFL ties | **0.08 per team** → $0.20 | 0.4% of games → $0.17 |
| Discount | **normalised per league** | flat scale |

We want the workbook confirmed as the authority, so we stop reconciling three
sources.

### 2.5 Two smaller ones in v2

- **§2.2 says the NFL offering is 8 hours.** The table below it shows 5 hours
  on 5 September and 5 hours on 6 September. That is 10.
- **18 rounds × 50,000 = 900,000, but an NCAA team has 1,000,000 shares.**
  100,000 shares per team never reach a window.

### 2.6 Washington Commanders is priced off DraftKings.

```
NFL, Washington Commanders, 7.5, -125, 105, DraftKings
```

Every other team of the 170 is BetMGM, which is what your email specifies.
The price is frozen and never revised.

---

## 3 · Data we still need

### 3.1 Please send the 2026 schedule.

Two spec rules need it.

- §3.6 splits each game's $2.50 advertising pool between the two teams. We
  must know who plays whom.
- §2.5 counts regular-season games only. Without the schedule we cannot keep
  postseason games out of the price.

### 3.2 Will the daily feed carry real Sportradar competitor IDs?

The sample file uses placeholders such as `sr:competitor:nfl0`. Real IDs join
your feed to our live probability feed with no mapping table.

---

## 4 · What we build

### 4.1 Do we calculate expected wins, or read your number?

**Our de-vig already reproduces yours exactly.** Across all 170 teams the
largest difference is 8.88 × 10⁻¹⁶, which is floating-point noise.

No Sportradar product carries season win totals for college, so the 138
college teams must come from you. For the 32 NFL teams we can compute our own
from the sportsbook line.

We would like to run the NFL number as a check against yours.

### 4.2 We will build an upload page for the daily file. Are you content?

You upload the file. We validate it on screen. A bad file is rejected
immediately with the reason, so you can fix it at your desk. We keep every
file, including rejected ones, in perpetuity.

Confirm you can also automate the upload later against the same endpoint, so
a person is not needed every day at 06:00 ET.

---

## 5 · Two old ones, if there is time

### 5.1 Quote lifecycle — do orders top up, or rest until gone?

The spec refills an order once it is half eaten, after 15 seconds (§5.9). On
23 July you said orders rest until completely gone. This is **E17**.

### 5.2 Cadence — 2 seconds or 200 milliseconds?

The spec sweeps every 2.0 seconds (§3.1.4). On the call you said 200
milliseconds. This is **E18**.

Our measurement: Sportradar's probabilities move with a **4-second median**,
and in a live game **88%** of readings move the quote by at least one tick.

Both block Chapter 5.

---

## 6 · Already answered — do not raise these

| Question | Answer | Source |
|---|---|---|
| Send the IPO EV for each team | **Have it** — all 170, `reference/ipo-prices-170.csv` | IPO workbook |
| Send the listed price for each team | **Have it** — same file | IPO workbook |
| The 170-team list | **Have it** — 138 NCAAF + 32 NFL | `season-win-totals-170.csv` |
| Send `odds.csv` | **Have it** — the same file carries team, win total, over price, under price, book | as above |
| Send `teams_config.py` | **Not needed.** The workbook already carries Brand, Popularity, Avg Capture and out-of-universe games per team | IPO workbook |
| Which sigma? | **2.7 NFL · 2.2 NCAA** | workbook Parameters sheet |
| Do both sides of the over/under come priced? | **Yes.** All 170 rows carry both, and all 170 lines are half-point | `season-win-totals-170.csv` |
| Does the market maker buy 85% of unsold shares, or all? | **All of them.** *"the MM MUST purchase all shares of the allotment remaining after participant demand"* — this supersedes spec §9.2 | Requirements v2 §4 |
| Is the market maker the seller in the primary? | **No.** *"InPlay Markets will be the exclusive seller of all initial offerings."* We are a buyer only | Requirements v2 §2 |
| Can participants sell during the offering? | **No.** *"Participants may buy only… may not sell… may not short"* | Requirements v2 §2 |
| Shares per team | NCAA **1,000,000** confirmed. NFL is **disputed** — see 2.1 | email vs v2 |
