# Call questions — 29 July 2026

> **Component:** [[market-maker/market-maker]]
> **Authority (George, 29-07):** the **IPO Draft Business Requirements v2**
> (28 July) and `reference/season-win-totals-170.csv` are **gospel**. Where
> either disagrees with an email, a spreadsheet or the earlier Supplement,
> they win. Questions below are only where **v2 disagrees with itself**, or
> where nothing covers the point at all.

**The deadline is secondary trading, not the season.**

```
NCAA secondary trading   26 or 27 August   ← 4 weeks
NFL  secondary trading   7 September
```

---

## 1 · Where v2 contradicts itself

**1.1 Is the mandate 10 rounds, 16 or 18?**
v2 says all three: §2.2 says 1-18, §3 says 1-16, §4 says 1-10.
*Our opening position is 85 M, 136 M or 153 M shares. That is $4.26 bn to $7.67 bn.*

**1.2 When does NCAA secondary trading start — 26 or 27 August?**
§1.1 says the 27th. §5.2 says the 26th at 9:30am.
*This is the date the market maker must be quoting.*

**1.3 When does the NCAA offering end — 26 or 28 August?**
§1.1 says the 26th at 10pm. §2.1 says the 28th at 10pm.
*As written, secondary trading opens 12 hours before the primary closes.*

**1.4 NCAA teams have 1,000,000 shares, but 18 rounds only offer 900,000.**
What happens to the last 100,000 per team?

**1.5 The NFL offering is 8 hours in the text and 5 + 5 in the table.**
Which is right?

---

## 2 · Not covered anywhere

**2.1 How do we sell the position down?**
We will start holding most of every team. Participants need shares in
circulation or there is no market, and market-maker volume does not count
toward the off-field value (§3.6.3). Our only tool is the inventory skew, and
it is capped at 25 cents — a cap we pass on day one and never come back
under.
*Should the cap be larger while we distribute? Or is distribution not our job?*

**2.2 Shorting — two things v2 does not say.**
Is the cap on total short interest across all participants, or per
participant? And may the market maker itself go short?

**2.3 Is the listed IPO price rounded to a penny?**
The workbook rounds — all 170 prices are exact pennies. Your email says full
precision, no rounding.
*We must reproduce your price exactly on day one.*

**2.4 Is `inplay_feed/ipo.py` superseded by the workbook?**
The workbook and `engine.py` agree on ties ($0.20) and on the discount method.
`ipo.py` disagrees on both.
*We want one authority, so we stop reconciling three sources.*

---

## 3 · Data we need

**3.1 The 2026 schedule.**
§3.6 splits each game's advertising pool between the two teams, so we must
know who plays whom. §2.5 counts regular-season games only.

**3.2 Will the daily feed carry real Sportradar competitor IDs?**
The sample file uses placeholders like `sr:competitor:nfl0`. Real IDs mean no
mapping table.

---

## 4 · What we build

**4.1 Do we calculate expected wins, or read your number?**
Our de-vig already reproduces yours exactly across all 170 teams. College must
come from you, because no Sportradar product carries season win totals. We
would like to compute the 32 NFL numbers as a check.

**4.2 We will build an upload page for the daily file. Are you content?**
You upload, we validate on screen, a bad file is rejected immediately with the
reason. We keep every file in perpetuity. Confirm you can automate the upload
later against the same endpoint.

---

## 5 · Two old ones, if there is time

**5.1 Quote lifecycle — do orders top up, or rest until gone?**
The spec refills after 15 seconds (§5.9). On 23 July you said rest until gone.
**E17.**

**5.2 Cadence — 2 seconds or 200 milliseconds?**
The spec says 2 seconds (§3.1.4). You said 200 milliseconds.
Our measurement: a 4-second median, and 88% of readings move the quote.
**E18.**

---

## 6 · Answered — do not raise

| Question | Answer | Source |
|---|---|---|
| Shares per team | **NFL 900,000 · NCAA 1,000,000** | v2 §1.2, §5.1 — gospel, supersedes the 875,000 in the email |
| Does the market maker buy 85% of unsold shares, or all? | **All of them** — supersedes spec §9.2 | v2 §4 |
| Who sells in the primary? | **InPlay Markets**, exclusively. We only buy | v2 §2 |
| Can participants sell or short during the offering? | **No.** Buy only | v2 §2 |
| §5.2.3 says NFL twice with different numbers | **5.2.3 means NCAA** — 1,000,000 | George, 29-07 |
| The IPO EV for each team | **Have it** — all 170 | `reference/ipo-prices-170.csv` |
| The listed price for each team | **Have it** — same file | as above |
| The 170-team list | **Have it** — 138 NCAAF + 32 NFL | `season-win-totals-170.csv` — gospel |
| `odds.csv` | **Have it** — the same file | as above |
| `teams_config.py` | **Not needed.** The workbook carries Brand, Popularity, Capture and out-of-universe games | IPO workbook |
| Which sigma? | **2.7 NFL · 2.2 NCAA** | workbook Parameters sheet |
| Do both sides of the over/under come priced? | **Yes**, all 170. All lines are half-point | `season-win-totals-170.csv` |
| Washington Commanders is priced off DraftKings | **Stands.** The CSV is gospel, so the price is the price | `season-win-totals-170.csv` |
