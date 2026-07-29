# Call questions — 29 July 2026

> **Component:** [[market-maker/market-maker]]
> **For:** the call with Edwin / InPlay today.
> **Source:** Edwin's answers of 28-07 ([[standards/MM-edwin-answers-28-07|email]]),
> the IPO Supplement v1.3, and his code in `reference/`.

Ordered by what decides the most. Each question states what to ask, then why
it matters.

**The clock:** today is 29 July. The NCAA price freeze is **19 August**, in
21 days. The NCAA offering opens **22 August**, in 24 days.

---

## Ask this one first

### 1. Does the market maker need to be live for the offering on 22 August?

The IPO Supplement gives the market maker a **Primary Mandate**. For rounds 1
to 10 the market maker must buy every share left after participant demand.

**Why it matters.** If the answer is yes, our build order changes today. If
the platform executes the mandate instead, we have until the season starts.
This question changes more than any other on the list.

---

## The IPO block — the prices freeze on 19 August

### 2. Which numbers are final? Is the tie leg 20 cents or 17 cents?

Your two files disagree three ways.

| | `engine.py` | `inplay_feed/ipo.py` |
|---|---|---|
| Tie value per NFL share | **$0.20** (0.08 ties per season) | **$0.17** (0.4% of 17 games) |
| Popularity comparison | Index against Index → 0.5000 | Index against raw Brand → 0.4975 |
| Discount scale | ranked within each league | flat scale |

Your email agrees with `ipo.py` on ties. You call `engine.py` authoritative.
Your own comment in `ipo.py` predicted the discount difference.

**Why it matters.** The IPO price is frozen and never revised. It should not
depend on which file was run.

### 3. Please send the IPO EV for each of the 170 teams.

**Why it matters.** You ruled that the Reference Price seeds at **EV**, not
at the listed price. So our opening price must equal your number exactly. We
do not need to rebuild your engine. We need its output.

### 4. Please send the listed price for each team.

**Why it matters.** The listed price is what participants paid. We need both
numbers to know the size of the day-one gap.

### 5. Which sportsbook did you freeze on?

The spreadsheet carries both **BetMGM** and **DraftKings**. Your email says
single-book BetMGM.

**Why it matters.** The two books post different lines. The choice changes
every IPO price.

---

## The float — three numbers, and they do not agree

### 6. How many shares exist per team in total?

We hold three different figures and none is confirmed.

| Figure | Source |
|---|---|
| **5,000,000** | our own notes |
| **875,000** | a spreadsheet |
| **500,000** | the IPO Supplement — but this is the *guaranteed primary float after Round 10*, not the issued count |

**Why it matters.** §4.3 needs Reference Float, which is issued shares minus
treasury shares. Without it there is no Position Ratio. Without a Position
Ratio there is no inventory skew, and the market maker cannot quote at all.
This blocks all of Chapter 4.

Our own note says the 5 million against 875 thousand gap changes the skew by
about 5.7 times.

### 7. How much of the float does the market maker end up holding?

Two documents give two answers.

- **Spec §9.2:** the market maker buys `floor(0.85 × unsold shares)`.
- **IPO Supplement §5:** the market maker buys **all** remaining shares, for
  rounds 1 to 10, and is exempt from the per-participant cap.

The Supplement states the consequence itself: a maximum opening inventory of
**85 million shares, about $4.26 billion**. Your own Open Item 9 marks the
conflict unresolved.

**Why it matters.** This is the market maker's opening position. Every
inventory rule in Chapters 4 and 5 works from it.

### 8. Can you walk us through the offering process?

We have read the Supplement, but we would rather hear it once. Windows,
rounds, the water line, and where the market maker sits in each.

---

## Data we still need

### 9. Please send the 2026 schedule.

**Why it matters.** Two spec rules need it.

- §3.6 splits each game's $2.50 advertising pool between the two teams. We
  must know who plays whom.
- §2.5 counts regular-season games only. Without the schedule we cannot keep
  postseason games out of the price.

### 10. Confirm the daily feed will carry real Sportradar competitor IDs.

The sample file uses placeholders such as `sr:competitor:nfl0`.

**Why it matters.** Real IDs join your feed to our live probability feed with
no mapping table. That is a real saving, and we want to be sure of it.

---

## What we build

### 11. Do we calculate expected wins, or do we read your number?

You sent the de-vig method and said to port it. Your feed already publishes
`expected_remaining_wins` for both leagues.

**What we have confirmed:** no Sportradar product carries season win totals
for college. So the 138 college teams must come from you. For the 32 NFL
teams we could calculate our own from the sportsbook line and compare it with
yours.

**Why it matters.** It decides whether we build a reader or a calculator. We
would like to run the NFL check, because your own two files already disagree.

### 12. We will build an upload page for the daily file.

You upload the file. We validate it on screen. A bad file is rejected
immediately, with the reason, so you can fix it while you are still at your
desk. We keep every file, including rejected ones, in perpetuity.

Confirm you are content. Also confirm you can automate the upload later
against the same endpoint, so a person is not needed every day at 06:00 ET.

---

## Two old ones, if there is time

### 13. Quote lifecycle — do orders top up, or rest until gone?

The spec refills an order once it is half eaten, after 15 seconds (§5.9). On
the call of 23 July you said orders rest until completely gone, with no top
ups. This is **E17**, still unresolved.

### 14. Cadence — 2 seconds or 200 milliseconds?

The spec sweeps every 2.0 seconds and calls a 5-second-old probability
current (§3.1.4, §3.3.1). On the call you said 200 milliseconds, and that a
second is too long. This is **E18**, still unresolved.

Our own measurement: Sportradar's probabilities move with a **4-second
median**. In a live game **88%** of readings move the quote by at least one
tick.

Both questions block Chapter 5, which we reach after Chapter 4.

---

## What we no longer need to ask

Recorded so we do not raise them by mistake.

- **The 170-team list.** We have it — `reference/season-win-totals-170.csv`,
  138 NCAAF and 32 NFL.
- **`odds.csv`.** The same file is it: team, win total, over price, under
  price, per book.
- **`teams_config.py`.** Not needed. Brand scores feed the Popularity Index
  at IPO only; in season §3.6.5 replaces them with the Base Demand Index from
  real IPO demand. Conferences were only used to guess schedules, and we are
  asking for the real schedule instead. Out-of-universe games are derivable,
  because we now hold the 170 names.
- **Whether both sides of the over/under are priced.** They are. All 170 rows
  carry both prices, and all 170 lines are half-point, so the whole-number
  problem does not arise in this snapshot.
