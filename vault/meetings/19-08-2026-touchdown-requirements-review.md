---
description: "The 19 August touchdown: the maker's spread method left open between George and Edwin, the evening IPO rehearsal plan, and shares-remaining returning as a public-facing display."
date: 2026-08-19
type: standup
status: digested
attendees: [Brett StClair, George Westbrook, Hasan Ahmed, Max Kingaby, Vineth Siriwardana, Edwin Johnson, Cody Haugen, Troy Kane]
duration: 8m
source: "Inplay - App - Touchdown - requirements review – 2026_08_19 14_31 BST – Notes by Gemini"
---

# Touchdown, 19 August 2026

> **Delivery:** [[delivery]] · **The change list:** [[change-requests-2026-08-18]]
> **Previous:** [[18-08-2026-requirements-review]]

Eight minutes, the day after the requirements review and three days before the
offering. Notes only, no full transcript, so quotes are the note-taker's
paraphrase rather than verbatim.

## The four findings

### 1. The maker's spread method is open between George and Edwin

George proposed a **scaling factor on the spread calculation: three for smaller
spreads, two for larger**, as the way to reach the wider quotes agreed the
previous evening. Edwin's counter is a different starting point rather than a
different number: **aim at a realistic level of liquidity and let the equation
follow**, instead of optimising the equation and accepting whatever liquidity it
produces.

Neither position was settled. They agreed to take ten minutes on it that evening,
before the next live game. Recorded as **N46** in
[[market-maker/open-questions]].

This matters more than a parameter argument sounds: it decides whether the maker
is tuned against a formula or against how the book feels to a trader, and the
answer sets how every later change to the maker gets argued.

### 2. The evening IPO rehearsal, and how it runs

George set out the method: **turn the market maker off**, allocate shares, create
the sell orders, and verify the offering inside the app. Edwin runs the buy side
from the admin panel as the taker.

What the rehearsal has to prove:

- the IPO card appears
- shares can be bought
- **selling is blocked**, which is the property that makes the primary window a
  primary window
- the allocation figures move as expected

Framed explicitly as preparation for the NFL offering rather than as the NCAA
dress rehearsal on its own.

### 3. Shares remaining becomes a public-facing display

⚠ **This reverses a position of Edwin's own.** The plan of record had
**shares-remaining hidden until near the close**, at his instruction. He now wants
it visible to buyers, with the example he gave being 500,000 remaining out of a
1,000,000 total.

The awkward part is technical, and it is not obvious from the ask. As of 19 August
the offering is **venue-backed**: an IPO buy is a real venue order resting against
the market maker's ask, and the database float's sold-out and remaining counters
were explicitly stopped from gating those buys, because the maker's book is the
inventory and the float describes something nothing draws from. **So the number
this display needs no longer has an obvious source.** It has to be derived from
the venue side, or the float has to be kept in step with it deliberately.

Recorded in [[requirement-changes]] as a reversal, and it needs a decision before
it is built rather than a best guess in the UI.

### 4. Iceberg orders

George raised iceberg order types, where a large order is worked in smaller
visible slices. Edwin's answer was about detection rather than support: **they
already have software that spots them immediately, and such orders show in blue**
so the team can see them.

No build ask attached. Logged because it is the first time order-concealment has
come up, and if a house engine is going to meet iceberg behaviour on the venue,
the maker's assumptions about what it can see in the book are worth checking.

## The grading, revisited

The 18 August review scored every change one to three. This call records some
items being **moved to a four in the background** after the implementation work
landed, with an acknowledged debate about the labelling. The scale as agreed had
only three points, so a four is either a new tier or a shorthand for done.
**Worth clarifying on the next call before the numbers appear in a report and
mean different things to different people.**

## Actions

| Who | What |
|-----|------|
| Brett | Circulate the updated flight plan |
| Edwin and George | Ten minutes on the maker's spread method, that evening |
| Edwin and George | Run the IPO rehearsal with the maker disabled |
| Edwin | Calls to Jared, Troy and the wider InPlay team |
