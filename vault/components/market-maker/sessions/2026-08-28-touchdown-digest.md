---
description: "Digest of the 28-08 touchdown: the reference-price delta model worked through with live numbers, and the end-of-game snap-back named the day before live games"
---

# 2026-08-28: the model gets its numbers, and the snap-back gets its name

> **Who:** Claude (`/meeting-digest`) for Lily
> **Type:** call (digest of a touchdown, not a working session)
> **Refs:** [[28-08-2026-touchdown]] · [[market-maker/decisions]] 2026-08-28 ·
> [[market-maker/open-questions]] `N55` `N56` `N57` `S13` `N54` `S12` ·
> previous: [[market-maker/sessions/2026-08-27-touchbase-digest]]

## What we did

Digested the Friday touchdown, 49 minutes, **the day before the first live NCAA
games**. It is the continuation of the 27-08 touchbase that was cut off, and it
is much more useful because Edwin stopped describing the model and worked it
through with live numbers.

## What we learned

- **The delta model, confirmed twice.** The kickoff win probability is **already
  inside expected wins**; the **change from that probability to the actual
  result** is what moves the share value. George stated it back, Edwin confirmed,
  George stated the caveat, Edwin confirmed again.
- **The numbers.** TCU against North Carolina: money line **-380**, win
  probability **77.3%**, payout $5, so the pre-game price is **0.773 × 5 = ~$3.86**
  and a win should carry it **toward $5**. Per-game season value at that
  probability: around **$1.14**.
- **Precision is explicitly not the goal.** _"There's no wrong or right answer. We
  just need it to be digestible by the market."_ The maker bids and asks around
  it. That lowers the bar on the reference price and **raises it on the spread**.
- **Edwin's model takes bid-offer pressure as a value input**, ELO-like, valuing
  the remaining season from record, fixtures and opponent strength.
- **Off-field volume definitions settled:** notional (effectively trade count),
  not dollar-weighted; game-to-game window; at least four days between games;
  Tuesday NFL and Wednesday college.
- **Injuries are out of scope for now**, deliberately, after George called that
  section of Edwin's document the part needing real work.

## What went wrong / got stuck

- 🔴 **`N55`, and it is visible tomorrow.** Because expected wins never moves, the
  price **snaps back to its opening level when a game ends**. George found it,
  Edwin rejected it flatly, and **the fix is the delta model, which is not built**.
  The first live games are 29 August, so the first weekend of real trading will
  show it. `S12` makes it certain rather than likely: NCAA expected wins is static
  anyway while the futures endpoint is down.
- ⚠ **`N56` is the load-bearing assumption and nobody has tested it.** The model
  assumes the kickoff probability is inside expected wins. **The two numbers come
  from different Sportradar feeds:** win probability is generated from live
  play-by-play, expected wins derives from an odds-comparison feed blending around
  30 sportsbooks. If the probability is not in there, the delta double-counts or
  under-counts **on every game**. This is testable against a completed game rather
  than a question to ask, and it should be tested before it is built on.
- ⚠ **A circularity nobody named on the call.** Edwin's model takes **our own
  book's bid-offer pressure** as an input to value, and the maker then quotes
  around the value that pressure produced. Raise it before it is built.
- ✂ **Off-field volume reversed a position taken the previous day.** On 27-08
  maker and taker were excluded; on 28-08 they are included, for presentation:
  _"I want to report more trading volume each week. I don't want to report 22
  trades."_ The cost is that the two house bots trade continuously, so the
  reported figure becomes mostly house activity, and the off-field allocation it
  drives is that much less connected to real participants. Recorded as `R17`.
- **`N57`:** journal replay adds latency, approach not chosen. Ours.
- **`S13`:** we cannot get live odds to derive a second probability, because that
  feed needs a sportsbook licence. Cody is working a precedent.

## Decisions made *(mirrored into [[market-maker/decisions]])*

- ⭐ The delta model: kickoff probability is in expected wins, the change to the
  result moves the price. Worked example recorded with live numbers.
- ✅ Precision is not the goal; digestibility is.
- ✅ Off-field volume definitions: notional, game to game, Tuesday and Wednesday.
- ✂ Maker and taker volume is now included, reversing 27-08.
- ⚠ Injuries out of scope for now.

## Questions opened / closed *(mirrored into [[market-maker/open-questions]])*

- **`N54` answered in mechanism** by the delta model, though not yet built.
- **Opened `N55`**: the end-of-game snap-back, live on the first game day.
- **Opened `N56`**: is the kickoff probability really inside expected wins.
- **Opened `N57`**: journal replay latency.
- **Opened `S13`**: live odds need a sportsbook licence.
- Nothing closed.

## Next

- **Test `N56` against a completed game before building anything on it.** Take a
  finished fixture, check whether pre-game expected wins moved by the amount the
  delta model predicts. This is a measurement, not a question for Edwin.
- **Decide what the first live weekend does about `N55`.** The snap-back will be
  visible and the fix will not be ready. Either say so in advance or accept that
  users see prices return to their opening level after every game.
- **Raise the circularity** in Edwin's model before it is built into anything.
