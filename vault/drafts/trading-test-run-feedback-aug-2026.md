---
description: "Written defect and UX feedback from a real trading test run, August 2026: fourteen items, several of them launch-critical, with the price-versus-order-book mismatch the most serious."
---

# Trading Test Run, written feedback

> **Received:** 14 August 2026, via the shared meeting-notes folder
> **Type:** written feedback from a hands-on trading session, not a meeting
> **Routed to:** [[trading/trading]] · [[information-layer/sub-components/team-page/team-page]] · [[information-layer/sub-components/leaderboard/leaderboard]] · [[market-maker/market-maker]]
> **Related:** [[jared-app-feedback-jul-2026]], the same shape of artefact from July

Fourteen items from someone trading the app properly rather than clicking
through it. Recorded in full because several are launch-critical and the list
arrived nine days before the offering opens.

## The three that matter most

**1. Displayed prices contradict the order book, so P&L is always wrong.**
The price at the top of the team page disagrees with what the order book says
is actually buyable and sellable. The consequence is not cosmetic: profit and
loss is permanently off, and the price shown when a user tries to buy is not
the price they can transact at. Reported twice in the same note, once at the
top and once at the bottom, which is a fair signal of how much it grated.

**2. It compounds into the missing market order.** Because the quoted price is
not the book price, a limit order will frequently not fill, and the user has no
way of understanding why. The reporter's conclusion is the important part:
this makes a market order *more* necessary, not less, because retail users
will not diagnose an unfilled limit. The synthetic market order is already
specified (see [[market-maker/systems/synthetic-market-order]]) and this is the
clearest argument yet for it landing before real users arrive.

**3. Max buy is rejected when buying power is sufficient.** Attempting to buy
the largest quantity the balance allows returns insufficient buying power. It
still fails around $1,000 below the limit. Edwin asked for a max button on
27 July; this is that feature failing before it exists properly.

## The full list

| # | Item | Lands on |
|---|------|----------|
| 1 | No market order anywhere, and it is what most retail traders reach for first | [[trading/sub-components/order-entry/order-entry]] |
| 2 | Open orders are hard to find | [[trading/sub-components/order-status/order-status]] |
| 3 | No default order size setting; every ticket starts generic | [[trading/sub-components/order-entry/order-entry]] |
| 4 | Finding your positions is tough | [[trading/sub-components/portfolio-view/portfolio-view]] |
| 5 | Bid and ask sometimes render blank | [[information-layer/sub-components/team-page/team-page]] |
| 6 | **Team-page prices contradict the order book; P&L always off** | [[information-layer/sub-components/team-page/team-page]] |
| 7 | An open order can only be cancelled, not modified | [[trading/sub-components/order-status/order-status]] |
| 8 | **Max buy rejected despite sufficient buying power** | [[trading/sub-components/order-entry/order-entry]] |
| 9 | Six wrong team acronyms: IUB should be IU, UKY should be UK, CINB should be CIN or CINN, HOUC should be HOU, NTX should be UNT, TAMU is correct | [[ipo-module/ipo-module]] data |
| 10 | Conference mapping is last season's; the Pac-12 reshuffle is not reflected and only two teams show against it | [[integrations]] (Sportradar reference data) |
| 11 | Leaderboard takes at least five seconds to update | [[information-layer/sub-components/leaderboard/leaderboard]] |
| 12 | **App broke after rotating to landscape and back**; tab presses did nothing. Videos to follow | [[frontend-performance]] |
| 13 | Chart is not in sync with the order book, moving back and forth independently | [[information-layer/sub-components/team-page/team-page]] |
| 14 | Buy price is not the order-book price, so limit orders will not fill and users will not know why | [[trading/trading]], [[market-maker/systems/synthetic-market-order]] |

## Why this matters more than its length suggests

Items 6, 13 and 14 are the same underlying problem seen from three angles: the
app is showing one price and transacting at another. On a product whose entire
premise is that a price is the thing you own, a price the user cannot trust is
not a defect in a screen, it is a defect in the proposition.

Items 9 and 10 are reference-data quality rather than engineering, and they are
cheap to fix, but they are also the kind of thing a knowledgeable American
sports fan notices instantly and reads as carelessness.

Item 12 is the only one that is a straightforward crash, and it needs the
promised videos to reproduce.
