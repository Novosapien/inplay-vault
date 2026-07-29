# Call questions — 29 July 2026

> **Component:** [[market-maker/market-maker]]
> **For:** the call with Edwin / InPlay today.
> **Sources:** Edwin's answers of 28-07 ([[standards/MM-edwin-answers-28-07|email]]) ·
> the IPO Supplement v1.3 · his code in `reference/` ·
> `reference/InPlay_IPO_Pricing_2026.xlsx` · his share-count email of 29-07.

**Updated 29-07.** The IPO workbook arrived and answered five of the original
questions. Those are listed at the bottom so nobody raises them by mistake.

**The clock:** today is 29 July. The NCAA price freeze is **19 August**, in 21
days. The NCAA offering opens **22 August**, in 24 days.

---

## Ask this one first

### 1. Does the market maker need to be live for the offering on 22 August?

The IPO Supplement gives the market maker a **Primary Mandate**. For rounds 1
to 10 it must buy every share left after participant demand.

**Why it matters.** If the answer is yes, our build order changes today. If
the platform executes the mandate instead, we have until the season starts.
This question changes more than any other on the list.

---

## The IPO block — prices freeze on 19 August

### 2. Is the listed price rounded to a penny, or full precision?

Your two sources disagree.

- **Your email:** *"at full precision — no rounding anywhere."*
- **The workbook Parameters sheet:** *"IPO price tick $0.01 — rounding
  increment for listed IPO price."*

All 170 listed prices in the workbook are exact pennies. So the workbook
rounds.

**Why it matters.** We must reproduce your prices exactly on day one. A penny
either way is a penny of day-one mispricing on 166 million shares.

### 3. Is `inplay_feed/ipo.py` superseded by the workbook?

The workbook settles two of the three differences we found, and `engine.py`
wins both.

| | Workbook Parameters sheet | `ipo.py` |
|---|---|---|
| NFL ties | **0.08 per team** → $0.20 a share | 0.4% of games → $0.17 |
| Discount | **normalised contested share, per league** | flat scale |

**Why it matters.** We want to be sure the workbook is the authority and the
Python rebuild is a reference only. Then we stop reconciling three sources.

### 4. Washington Commanders is priced off DraftKings. Every other team is BetMGM.

```
NFL, Washington Commanders, 7.5, -125, 105, DraftKings
```

Your email specifies single-book BetMGM at the freeze.

**Why it matters.** One row out of 170 breaks the rule. Either the line is an
error or the rule has an exception. The price is frozen and never revised.

### 5. Confirm the day-one gap is intended, and that you are content with it.

```
value of all shares at IPO EV        $8.45 bn
value at the listed price            $8.27 bn
the discount                         $180.7 m   (2.14%)
```

The Reference Price starts at **EV**. Participants buy at the **listed
price**. So on day one every subscriber can sell to us at a profit.

We do not lose money on this — we bought at the discount too. But the flow is
one-sided, and it lands on top of the position the Primary Mandate already
gives us.

Your own Supplement §8 raised this and left it **[OPEN]**. The email decided
EV. We only want it confirmed, not reopened.

---

## The float and the offering

### 6. Does the market maker buy 85% of the unsold shares, or all of them?

Two documents give two answers.

- **Spec §9.2:** `floor(0.85 × unsold shares)`.
- **IPO Supplement §5:** **all** remaining shares, rounds 1 to 10, exempt
  from the per-participant cap.

Your own Open Item 9 marks this unresolved.

**Why it matters.** This is the market maker's opening position. Every
inventory rule in Chapters 4 and 5 works from it.

### 7. Can you walk us through the offering process?

We have read the Supplement. We would rather hear it once. Windows, rounds,
the water line, and where the market maker sits in each.

**Why it matters.** The share counts you sent (875,000 NFL, 1,000,000 NCAA)
against the Supplement's 50,000 per round for 10 rounds means most of the
float sells **after** the mandate expires. We want to be sure we read that
correctly.

---

## Data we still need

### 8. Please send the 2026 schedule.

**Why it matters.** Two spec rules need it.

- §3.6 splits each game's $2.50 advertising pool between the two teams. We
  must know who plays whom.
- §2.5 counts regular-season games only. Without the schedule we cannot keep
  postseason games out of the price.

### 9. Confirm the daily feed will carry real Sportradar competitor IDs.

The sample file uses placeholders such as `sr:competitor:nfl0`.

**Why it matters.** Real IDs join your feed to our live probability feed with
no mapping table.

---

## What we build

### 10. Do we calculate expected wins, or do we read your number?

**Our de-vig already reproduces yours exactly.** Across all 170 teams the
largest difference is 8.88 × 10⁻¹⁶, which is floating-point noise. The
method, both sigma values and the margin removal all agree.

**What we have confirmed:** no Sportradar product carries season win totals
for college. So the 138 college teams must come from you. For the 32 NFL
teams we can compute our own from the sportsbook line.

**Why it matters.** It decides whether we build a reader or a calculator. We
would like to run the NFL number as a check against yours.

### 11. We will build an upload page for the daily file.

You upload the file. We validate it on screen. A bad file is rejected
immediately, with the reason, so you can fix it while you are still at your
desk. We keep every file, including rejected ones, in perpetuity.

Confirm you are content. Also confirm you can automate the upload later
against the same endpoint, so a person is not needed every day at 06:00 ET.

---

## Two old ones, if there is time

### 12. Quote lifecycle — do orders top up, or rest until gone?

The spec refills an order once it is half eaten, after 15 seconds (§5.9). On
23 July you said orders rest until completely gone, with no top ups. This is
**E17**, still unresolved.

### 13. Cadence — 2 seconds or 200 milliseconds?

The spec sweeps every 2.0 seconds and calls a 5-second-old probability
current (§3.1.4, §3.3.1). On the call you said 200 milliseconds, and that a
second is too long. This is **E18**, still unresolved.

Our own measurement: Sportradar's probabilities move with a **4-second
median**, and in a live game **88%** of readings move the quote by at least
one tick.

Both questions block Chapter 5, which we reach after Chapter 4.

---

## Answered — do not raise these

| Was | Now |
|---|---|
| Send the IPO EV per team | **Have it.** `reference/ipo-prices-170.csv`, all 170 |
| Send the listed price per team | **Have it.** Same file |
| How many shares per team? | **875,000 NFL · 1,000,000 NCAA** (email, 29-07). Different per league. **166,000,000 shares in total.** ⚠ Our own note of 5 million was wrong; 875,000 was the NFL figure all along |
| The 170-team list | **Have it.** `reference/season-win-totals-170.csv` — 138 NCAAF, 32 NFL |
| `odds.csv` | **Have it.** The same file: team, win total, over price, under price, book |
| `teams_config.py` | **Not needed, and now redundant.** The workbook carries Brand, Popularity, Avg Capture and OOU Games per team |
| Do both sides of the over/under come priced? | **Yes.** All 170 rows carry both, and all 170 lines are half-point |
| Which sigma? | **2.7 NFL, 2.2 NCAA** — confirmed on the Parameters sheet |
