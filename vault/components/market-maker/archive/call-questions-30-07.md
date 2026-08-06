# Call questions — 30 July 2026 (read-on-the-call version)

> **Component:** [[market-maker/market-maker]]
> Plain-language version of [[market-maker/call-questions-29-07]], in priority
> order, plus the three items raised on 30-07 that are not in that file.
> **Gospel:** IPO Draft Business Requirements v2 (28-07) and
> `reference/season-win-totals-170.csv`.

**The deadline is secondary trading, not the season.**

```
NCAA secondary   26 or 27 August   ← 4 weeks
NFL  secondary   7 September
```

---

## The five that matter

### 1 · Which date must we be quoting from — 26 or 27 August?

v2 says three different things. One reading has normal trading opening at
9:30am on the 26th while the IPO is still selling until 10pm the same day.

**Why we ask:** it is the date we must be live. Four weeks away, and it is the
hardest deadline we have.

### 2 · Who tells us what we own on morning one?

Shares change hands in two separate places. The IPO happens inside InPlay's
own system and never reaches tZERO. Normal trading happens on tZERO, and that
is the only place we can see.

So when we ask the venue "what do we own?", it says nothing — it never saw the
IPO. The shares are real; the record of them sits with InPlay.

**And it does not fix itself.** Once trading starts we can query our position,
but the venue counts from zero and only adds what we trade on the venue. If
nobody seeds the IPO number, every position we read is wrong by the amount we
were allocated — forever, not just on day one. And that number decides every
price we post.

**Two answers, either is fine:**

1. You send us a file when the IPO closes — team, share count, average price.
   The spec already reserves the slot for it (`IPO_ALLOCATION`); nobody
   produces it.
2. Or you give us read access to your allocation records and we pull it.

**Ask:** *"How do we learn our allocation per team, and by when?"*

### 3 · How many rounds does the mandate cover — 10, 16 or 18?

v2 says 1-18 in one place, 1-16 in another, 1-10 in a third.

```
10 rounds    85 M shares    $4.26 bn
16 rounds   136 M shares    $6.82 bn
18 rounds   153 M shares    $7.67 bn
```

**Why we ask:** that is our opening position, and $3.4bn of spread. Every
inventory rule is calculated from it.

### 4 · How are we meant to sell the position down?

**What we do.** We quote two prices on every team, all day: one we buy at, one
we sell at.

**The problem.** We must buy every share participants do not take, so we end
up owning 50–100% of every team. That is bad because **if we hold nearly all
the shares, participants have nothing to trade with each other.** A market with
one owner is not a market.

**The one tool we have.** When we hold a lot, we move both prices down. Our
sell price gets cheaper, so buying from us is attractive. Our buy price gets
worse, so selling to us is not. Shares flow out. That is the whole mechanism.

**The tool is stuck.** The shift is capped at 25 cents, and the cap binds at
25% ownership.

```
hold 25%    →  shift down 25 cents   ← cap
hold 50%    →  shift down 25 cents
hold 100%   →  shift down 25 cents
```

We pass 25% on day one and never come back. So holding every share looks
identical to holding a quarter. And 25 cents on a $50 share is half of one
percent — it persuades nobody.

**Ask:** *"Raise the cap while we distribute, tell us the pace you expect, or
tell us distribution is not our job. Which?"*

**If pushed:** this is not about profit. v2 excludes profit as a motive and we
have unlimited funds. It is about liquidity. It also helps them — their
Popularity Index counts volume, and the rules say our volume never counts, so
shares parked with us do nothing for their product either.

### 5 · Shorting — two things v2 does not say

Is the cap on **total** short interest, or **per participant**? And may the
market maker itself go short?

**Why we ask:** shorting lets participants sell us shares that do not exist. So
what can be sold to us is the float **plus** the short interest — 2,000,000
rather than 1,000,000 — and v2 sets no limit on how much we absorb.

---

## Then, if there is time

### 6 · Which IPO calculation is authoritative?

The workbook and `engine.py` agree. `inplay_feed/ipo.py` differs on the tie leg
($0.20 vs $0.17) and the discount scale. **We want one source, not three.**

### 7 · The 100,000 unoffered NCAA shares — issued, or treasury?

Each NCAA team has 1,000,000 shares but only 900,000 are ever offered. That is
13.8 M shares across 138 teams. It shifts every NCAA position calculation by
about 10%.

### 8 · Where does the pregame win probability come from?

Your on-field formula needs it for every game, frozen when we take your daily
number. **It is not in your feed.** Is it our Sportradar number, or do you
publish it?

### 9 · Is the listed IPO price rounded to a penny, or full precision?

Your email says no rounding. The workbook says a $0.01 tick, and all 170 prices
are exact pennies.

### 10 · Do corporate actions ever happen, and who publishes one?

The formula carries the term and nothing publishes it. We expect it never
fires. **But a silent share issuance would corrupt every position with nothing
detecting it.**

### 11 · May we move the price on purpose to shed stock, and inside what bounds?

You raised this once and we parked it. If the skew cannot distribute (item 4),
this is the alternative.

### 12 · Is the market simply on, all day?

The spec implies 24 hours, no sessions, no auctions — but never says it. NCAA
plays six days a week, so we also need each team's overnight boundary.

### 13 · Who declares a game final?

Nothing publishes it, and swapping expected results for real ones depends on
it.

### 14 · How do you want week-zero college mismatches priced?

NCAA opens in four weeks and the openers are lopsided.

---

## Data we still need

- **The 2026 schedule.** We cannot split the $2.50 advertising pool without
  knowing who plays whom, and we cannot keep postseason games out of the price.
- **Real Sportradar competitor IDs** in the daily feed, not
  `sr:competitor:nfl0`. Placeholders mean we build and maintain a mapping table.

## Confirms — quick yes or no

- **The upload page.** We build it: your file validated on screen, rejected
  immediately with the reason, every file kept. And you can automate against
  the same endpoint later.
- **Expected wins.** Shall we compute the 32 NFL numbers ourselves as a check
  against yours?
- **Quote lifecycle.** Orders rest until completely gone, no top-ups — as you
  said on 23 July, against the spec's refill?
- **Cadence.** 200 milliseconds, not the spec's 2 seconds? Our measurement of a
  real game shows probabilities move on a 4-second median.
- **Version control.** Will there be a v3, and when? Until then, is what you
  say today authoritative over the PDF? And confirm the change-freeze date — we
  have assumed 19 August.
