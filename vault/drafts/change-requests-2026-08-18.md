---
description: "The 22 app change requests received from InPlay on 18 August 2026, each classified as reversal, addition, layout or defect, with the ones that are not InPlay's to grant called out."
---

# Change requests, 18 August 2026

> **Delivery:** [[delivery]] · **Register:** [[requirement-changes]]
> **Received:** 18 August 2026, relayed by Brett. The wording reads as Edwin's
> and Cody's; attribution to be confirmed on the next call.
> **Context:** the build definition was frozen on 17 August. This list arrived
> the following day, four days before the NCAA offering opens on the 22nd.
> ✅ **Graded and dated on the 18 August call:** [[18-08-2026-requirements-review]].
> The classification below stands. The decisions and dates from that call are
> recorded at the foot of this document and outrank the recommendation section.

Numbering below is InPlay's own. The original list skips 8, 10, 12 and 15, and
several items were sent twice; duplicates are merged rather than counted twice.
**22 distinct requests.**

## What this list is, in one paragraph

Most of it is layout and naming, which is cheap and improves the product. Four
items are genuine new behaviour that has to be built and tested. Two items are
not InPlay's to grant, because they describe venue rules rather than app
choices. One item changes a settled trading default. Read in that order, the
list is affordable, but only if the four build items are dated honestly rather
than assumed into the 22nd.

## Classification

| Class | Count | What it costs |
|-------|------:|---------------|
| Layout, naming and copy | 12 | Front-end only. Hours each, no engine change |
| New behaviour to build | 4 | Real work: design, build, test |
| Reversal of a settled requirement | 3 | The new work, plus the finished work and its tests |
| Defect or performance | 1 | Fix, not change |
| **Not InPlay's to grant** | **2** | Venue rules. Needs tZERO, not a ticket |

## The requests

### Layout, naming and copy

| # | Request | Lands on | Note |
|---|---------|----------|------|
| 1 | No spinning wheel on login | [[customer-onboarding/customer-onboarding]] | Treated as a defect, see below |
| 3 | Participation in the IPO carries clear instruction on the start time | [[ipo-module/ipo-module]] | Copy plus a countdown surface. Cheap and it removes a real confusion four days out |
| 4 | News moves to an icon across the top of the screen, and that is where articles are read | [[information-layer/information-layer]] | Already agreed in principle on 17 August as part of reducing surfaces (register R13). This is the execution detail |
| 6 | Gamecast is renamed **Live Games** | [[information-layer/sub-components/single-game-page/single-game-page]] | Naming only. Worth doing before launch copy freezes |
| 7 | Today's movers moves to the bottom of the home screen | Home | Layout |
| 9 | Results moves to the bottom, today's movers comes up under live games | Home | Layout. Same edit as 7, stated twice |
| 16 | Volatility moments move down under the field, and carry a percentage change against the team's daily stock move | [[information-layer/sub-components/single-game-page/single-game-page]] | Layout plus one derived number the app already has the inputs for |
| 18 | The field stays frozen to the top of the scroll | Single game page | Layout |
| 23 | The market data section at the bottom of the game page is deleted | Single game page | Surface reduction, consistent with R13 |
| 25 | **Max** comes off the trade page selection | [[trading/sub-components/order-entry/order-entry]] | Removes the one-tap maximum size. Reduces fat-finger risk, which cuts the other way from removing confirmations (R9) |
| 26 | The trading reserve button goes to the bottom of the home screen, smaller than before, in the space the news block leaves | Home | Depends on 4 landing first |
| 24 | The NCAAFB games tab populates every game of the season | The data service and the Markets board | Listed as layout because the data exists, but see the caveat below |

⚠ **Caveat on 24.** The schedule the app reads is the regular-season feed. The
open item `/sr/winprob` takes no `season_type`, which is why preseason ids never
reached it and the app worked around it client-side. Populating a full NCAAFB
season is straightforward; making sure it stays correct across season types is
the part that has bitten twice already, on 14 and 15 August.

### New behaviour to build

| # | Request | Lands on | What it actually involves |
|---|---------|----------|---------------------------|
| 11 | The buy and sell controls are persistent across every page, and larger | [[trading/trading]] | Already specified in [[one-click-trading-requirements-aug-2026]] on 14 August. The Markets board and the Trade page got the shared bar on 17 August, so this is completion rather than a new start |
| 19 | Selecting a team at the top of the Live Games surface sets what the buy and sell controls trade | Single game page, order entry | The target-selection half of the one-click model. Needs a clear rule for what happens when the selected game is not live |
| 21 | A **flatten** button that exits every position on one team, and a **flatten all** that exits every open position across all teams | [[trading/trading]], market taker | Flatten per team is in the 14 August model. **Flatten all is new.** It is a multi-symbol liquidation path: partial fills, rejects, and what the user sees when only some legs close. This is the largest single item on the list |
| 22 | A user can move money into the trading reserve at any time, provided they are flat | [[withdrawal-flow/withdrawal-flow]], reserve accounting | New. Needs the flat test, the accounting entry and the rule for what happens mid-game. Interacts with the 100 IPD advertising reward, which credits the same reserve |

### Reversals of settled requirements

| # | Was | Becomes | Cost |
|---|-----|---------|------|
| 5 | The home ticker shows prices and their change, which Edwin described on 12 August as the thing that creates the excitement | The ticker shows IPO prices only, no net change | Small build, but it reverses a position argued for explicitly five days earlier |
| 17 | Full order-book depth, delivered on the team page after the gateway began publishing the whole book | Top of book only, expandable on demand | The depth work is finished and tested. This does not remove it, it hides it, so the cost is the display work plus the tests that proved depth |
| 20 | Limit is the default order type, with the synthetic market order behind a flag that is off | **Market becomes the default**, limit the alternative | The synthetic market order is built and merged. Making it the default means turning it on for every user, which was scheduled as a verified switch at the 20 August rehearsal, not as the standing default |

### Defect

| # | Request | Position |
|---|---------|----------|
| 1 | No spinning wheel on login | Logged as a defect rather than a change. Login already benefits from the 17 August work that made every screen transition instant; this needs reproducing before it can be sized |

### Not InPlay's to grant

| # | Request | Why it is not a ticket |
|---|---------|------------------------|
| 13 | Remove every use of the word **short**, make it **sell**, and remove any tZERO requirement to locate shares | The wording half is a copy change and is fine. **The locate is a venue rule, not an app choice.** The gateway caps a sell at what the account can prove it holds, and the venue rejects the whole order above it. Removing the language does not remove the rejection; it only removes the explanation the user gets when it happens. Needs a ruling from tZERO before the app pretends the constraint is gone |
| 14 | Remove the confirmation page that says shares are being located | Follows 13. Safe to remove **only** once 13 is settled with the venue. Removed on its own, a rejected sell becomes silent |

⚠ Both of these touch the short-while-long guard confirmed on 29 July and the
sell gate built into the taker. They are the two items on this list that can
produce a user-visible failure nobody can explain.

## Recommendation

**Before the 22nd, if InPlay want them:** 1, 3, 4, 6, 7, 9, 16, 18, 23, 25, 26
and the copy half of 13. All front-end, all testable in one pass on the 20
August rehearsal.

**After the offering:** 11 completion, 19, 21, 22, 24, and the reversals 5, 17
and 20. Each is either new behaviour or a change to something already proven,
and there is one live game left before real users trade.

**Needs a ruling, not a ticket:** the locate half of 13, and 14 with it.

The freeze is not a refusal. It is the difference between shipping these
deliberately and shipping them untested into the one window that cannot be
repeated.

---

## Decided on the call, 18 August

The list was graded live, item by item, on Brett's scale: **1 = go, 2 = look at
it first, 3 = worried**. Items that simplify by removing something were called
"negative one". Full record in [[18-08-2026-requirements-review]].

### The three dates

| Date | What lands |
|------|-----------|
| **22 August**, the offering | 1, 3, 4, 5, 6, 7, 9, 11, 16 and 17 merged, 18, 23, 24, 25, 26 |
| **29 August**, secondary opens | 13 and 14 (needs tZERO), 21 flatten and flatten all, 22 the reserve top-up, 2 the three login paths, the maker's wider quotes |
| **9 September**, first NFL game | The in-break video ad over the live match tracker |

### Corrections to this document, from the call

- **19 is scrapped.** Target selection already exists as the swipe on the trade
  bar, ordered last-traded, then watch list, then alphabetical. Keep as designed.
  The problem is that nobody knows it is there, which is discoverability rather
  than a build.
- **11 does not get bigger buttons.** Edwin was explicit: the tap target in the
  middle opens the order ticket, and a larger button eats it. Only Home and Ranks
  are missing the bar. Separate ask from the same item: the control should read
  **Order** rather than quantity and price, so it is obvious it opens a ticket.
- **16 and 17 merge into one change.** The order-book tile sits directly under
  the field and shows bid, ask, last and **net change in place of spread**, as a
  number rather than a percentage, derived from the daily settlement price tZERO
  returns with every order. Top of book only, with quantities. Below it: open
  orders, recent fills, in-game moments, then market and game.
- **22 retires the 25,000 threshold.** The top-up is **instant, up to 100,000,
  never above**, from referral dollars, with no position open.
- **24 is a bug, not a change.** The fixtures do populate: opening the team and
  returning to games shows them. The direct click is broken.
- **1 removes the screen rather than the spinner.**

### Added on the call, not on the original list

| Item | Position |
|------|----------|
| **Watch mode needs buy and sell** | The horizontal watch surface carries a trade button that routes the user away and back. It needs the same controls as everywhere else. Troy rated the surface highly on an iPad; this is what holds it back |
| **A tradable team playing an untradeable opponent** | Roughly 22 games this season, possibly one in week zero. George: not negotiable, one and a half to two |
| **The maker quotes too tightly** | Top of book only and wider spreads, with a tolerated distance from fair value of roughly 20 to 25 cents before the maker resets, possibly gated on win probability moving a further five percent. George: anything touching the maker is a two at minimum. He sends the current parameters, Edwin sets the new base spread |
| **In-app demo or an animated nudge** | Raised twice. The app is more capable than it is discoverable, and Edwin reports that 80 percent of the people he demonstrates to do not know what to do |

### The risk position, agreed rather than assumed

Brett set out why late change costs more near a launch. Edwin accepted it and
chose to proceed anyway, and Cody supplied the number that makes that reasonable:
**about 160 verified users, of whom roughly 100 are friends and family**, so real
exposure is about 60 people, and the window to 5 September is the lowest-risk
period the product will ever have. Agreed mitigation: tell those users what is
changing, by push and newsletter, as pioneer users.
