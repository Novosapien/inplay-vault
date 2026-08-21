---
description: "The overnight friends-and-family session of 21 August 2026: what it proved, the crash and its ten-minute fix, and the exit-path failure that would have ruined the offering."
---

# Friends and family session, overnight 21 August 2026

> **Delivery:** [[delivery]] · **Source:** the session's own message log, pasted by Brett

The last rehearsal before the NCAA offering. Edwin, Troy, Cody, George and Hasan
on the app together on a live game.

## What it proved

The session did the job a rehearsal exists to do. It produced **one class of
problem that would have ruined the 22nd**, in front of six people rather than six
thousand, and it proved the over-the-air path works in both directions: a bug
reached testers at 00:41 and a fix reached them by about 00:44.

## The findings

| What happened | Detail | State |
|---|---|---|
| The app crashed on open | An over-the-air update carried a bug that stopped the app launching. Fixed in about ten minutes with a second push; testers had to fully close and reopen. The code cause was a timing hook sitting below an early return | Closed |
| **A trader could not exit** | Troy's sells were rejected at the market, above it and below it, and he could not get out of a position. His own reading: with no depth, an order that cannot fill in full is refused rather than filling what it can and cancelling the rest | ⚠ **Open** |
| The book had one level, sometimes one side | The maker was narrowed to price a single level and the taker's size raised closer to the maker's own. Troy saw one side of the book cleared; Edwin reported the bid missing for a while | ⚠ **Open** |
| Sell did not sell | Pressing sell opened an order ticket instead of placing a market sell. With one-click on, sell should sell | ⚠ **Open** |
| Down and distance unreadable | Reported 02:01, fixed 02:20, white on the score line and the field row | Closed |
| Watch page | Improved by an over-the-air update during the session | Closed |

## The one that matters

**A user must always be able to get out.** Three findings are the same problem
from different angles: the maker quotes one level by design, so the book is thin;
a market order into a thin book must fill what it can and cancel the remainder;
last night it was refused instead.

The trading service **already carries a residual sweep** that cancels the unfilled
remainder of a synthetic placement, so the intended behaviour exists in code. What
is not established is **why the venue refused these sells outright**. The most
likely explanation, and it needs confirming from the logged rejection text rather
than assuming, is the venue rule that a sell cannot exceed what the account can
prove it holds. That is the same rule [[change-requests-2026-08-18]] items 13 and
14 ask to remove, and Edwin has already raised it with Troy.

## The trade-off to hold in view

Wider and thinner quoting was asked for so prices move with the market rather than
sitting pinned to the win probability. That is a sound instinct and the cost
appeared the same night: less depth means more refused exits. Both cannot be
optimised four days out.

**Recommendation: keep the wider spread and make the exit path forgiving**, rather
than thicken the book again and lose the price movement that was the point of the
change.

## Note on over-the-air updates

They work, and they are a deploy straight to production with no review gate. That
is what let a crash reach testers at midnight. Treat every push as a release.
