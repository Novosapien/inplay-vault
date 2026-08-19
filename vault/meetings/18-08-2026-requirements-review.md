---
description: "The 18 August requirements review: InPlay and Novosapien graded all 26 change requests one to three, scrapped one, and set which land by 22 August, which by 29 August, and which by 9 September."
date: 2026-08-18
type: general
status: digested
attendees: [Brett StClair, George Westbrook, Hasan Ahmed, Edwin Johnson, Cody Haugen]
duration: 1h25m
source: "Review requirements – 2026_08_18 21_01 BST – Notes by Gemini"
---

# Requirements review, 18 August 2026

> **Delivery:** [[delivery]] · **The list:** [[change-requests-2026-08-18]]
> **Register:** [[requirement-changes]]

The call that turned a list of 26 asks into a graded, dated plan. Every item was
scored live by George against a scale Brett set at the top: **1 = go, 2 = look at
it first, 3 = worried about it.** Items that make the app simpler by removing
something were called "negative one" in the room.

## The frame both sides agreed

**Brett stated the risk plainly and it was accepted rather than argued.** As a
launch date approaches, the safe move is less change in the code base, not more:
code breaks in ways that do not announce themselves, an algorithm or a callback
quietly goes wrong, and the cost of that rises with every user on the system.
Edwin's answer: _"I'll take the f\*\*\*ing risk"_, because a user who opens the app
and does not know what to do is a certainty, while a regression is a probability.

**Cody supplied the number that makes that trade defensible.** There are roughly
**160 verified users, of whom about 100 are friends and family**, so the real
exposure today is about 60 people. His framing: the window to **5 September** is
the lowest-risk period this company will ever have, so if change is going to be
made, now is when it costs least.

**Agreed mitigation:** tell the existing users. Push notification and newsletter,
framed as pioneer users, so changes land as participation rather than breakage.

## The gradings

| # | Request | Grade | What was actually decided |
|---|---------|-------|---------------------------|
| 1 | No spinning wheel on login | Negative one | Delete the splash screen entirely rather than speed it up. Nobody can read the tips at that speed |
| 2 | Login paths: private, free, cash | **2** | Agreed in principle, three quadrants on first open, but it ripples through every user journey. See below |
| 3 | IPO start-time instruction | 1 | Not a popup. A homepage element **under the ticker** with a countdown. Order on the page: challenge selection, then the IPO notice, then total equity. It retires itself after 5 September |
| 4 | News moves to a top icon | 1 | Frees the homepage. New page behind the icon |
| 5 | Ticker shows IPO prices only | 1 | Flat IPO prices, no net change, for a user arriving before trading opens |
| 6 | Gamecast renamed **Live Games** | 1 | Text change |
| 7 | Today's movers to the bottom | Negative one | Falls out of removing news |
| 9 | Results below today's movers | 1 | Live games, then movers, then results. Edwin's reasoning: a trader looks at what is live, then what is moving, and should not have to scroll past finished games to find it |
| 11 | Persistent buy and sell | 1, with a correction | **Not bigger.** Edwin: keep the sizing as it is, because the tap target in the middle opens the order ticket and a bigger button eats it. Only Home and Ranks are missing the bar; Markets and Trade already have it. Separate ask: the control that reads quantity and price should read **Order**, so it is obvious it opens a ticket |
| 13 | Remove the word short | **2** | Edwin's top priority on the list. Today it reads sell if you own it and short if you do not. It should always read sell, with the short behaviour unchanged underneath. Needs tZERO. Due **29 August**, not the 22nd |
| 14 | Remove the locate confirmation | **2** | Follows 13, same tZERO dependency, same date |
| 16, 17 | Order book under the field | 1.5, called a 1 | Merged into one change. Bid, ask, last and **net change in place of spread**, as a number not a percentage. Top of book only, with quantities. No title needed. The team selected below drives which book shows. Under it: open orders, recent fills, in-game moments, then market and game |
| 18 | Freeze the field to the top of the scroll | Accepted | George had already started it that day and demoed it live. Default is the frozen field, collapsible by choice. Edwin: _"this is the showstopper"_ |
| 19 | Target selection from the top of the game surface | **Scrapped** | Already exists as the swipe. Keep as designed |
| 20 | Market orders as the default | 1 | With a settings control to change it. Edwin, against his own instinct: no professional trader uses a market order, but retail expects one |
| 21 | Flatten and flatten all | **2 minimum** | George: the nuclear button. Flatten closes every position on one game, flatten all closes everything across every team |
| 22 | Top up the trading reserve while flat | 1.5 to 2 | **Instantly, up to 100,000, never above it**, from referral dollars, with no position open. This retires the previous 25,000 threshold. George: instant is easier than the current mechanism |
| 23 | Delete the market data block | 1 | Repetitive with the new order-book tile above it |
| 24 | NCAAFB games tab beyond week one | Bug, not a change | It does populate: opening the team and returning to games shows it. The direct click is broken |
| 25 | Remove Max from the trade page | 1 | It computes off buying power and the number it produces does not make sense |
| 26 | Referral code on the homepage | 1 | Small block at the very bottom, Jared's ask after the referral section was removed |

## What item 2 actually costs, in George's words

The three-door front screen is easy. What sits behind it is not. Every free user
has to be flagged, and then **every page has to know what a free user may not
do**. The payout and leaderboard logic assumed the opposite: anyone trading is on
the leaderboard and anyone trading is eligible for a payout. That has to become
conditional per user.

Edwin's simplification, accepted: **two leaderboards**, one for verified users and
one for the email-only public. That is cleaner than filtering one board.

Brett's addition, accepted: a user who picks the free door must be able to change
their mind later, and the place for that is their **account section**, as a
holding space that converts them when they are ready.

## Decisions beyond the list

**The market maker quotes too tightly, and Edwin wants it looser.** His experience
trading the live game: the book was so thick that nothing in the play-by-play
moved the price, so there was no tradable event until the outcome was obvious. He
wants **top of book only, wider spreads**, and a **distance from fair value of
roughly 20 to 25 cents** that the maker tolerates before it resets, possibly gated
on win probability moving a further five percent. The point is that price should
move because participants move it, not only because the probability model does.
George's position: anything touching the maker is **a two at minimum**, he will
send the current parameters, and Edwin sets the new base spread against them.
**Target is 29 August, not the 22nd.**

**Watch mode needs the trade controls.** The horizontal watch surface carries an
orange trade button that routes the user away to the order book and back again.
It needs the same buy and sell controls as everywhere else. Troy used it on an
iPad and rated it highly; this is the one thing holding it back.

**A tradable team will play an untradeable opponent.** George raised it, Edwin
confirmed: roughly **22 such games this season**, and week zero could carry one.
The app has to handle a game where only one side has a listed company. George
sized it at one and a half to two and called it non-negotiable rather than
optional. It is also why North Dakota State prices high in the offering: they
play a lot of non-division-one opponents and take the whole result.

**The video ad is specified and dated.** Overlay across the live match tracker,
never inside the field, **top third**, triggered off the Sportradar play-by-play
signals the app already renders: TV timeout, end of quarter, halftime. Thirty
seconds, not skippable, buy and sell live underneath it throughout. Cody's date:
**9 September, before the first NFL game**, not this Saturday. Brett's caution:
video fill is the hard part, so the unit is configured as an expandable native
banner that can serve video or fall back to an animated image when video demand
is thin.

**Sportradar is a live problem, not a background one.** One game ran **36 minutes
without a win-probability update**. Support has not answered, and Cody has sourced
the NCAA win totals from a different provider rather than wait. Preseason is when
Sportradar tests its own product, which is part of the explanation and none of the
comfort.

## Two things worth carrying forward

**Discoverability is now the product problem, not capability.** The trade bar
already switches teams by swipe, ordered last-traded, then watch list, then
alphabetical. Brett and Edwin both found it during the call and neither knew it
existed. Cody's point stands: nobody will find it. Ideas raised: an animated
nudge on the control, and an in-app demo. Edwin: _"80% of my demonstrations,
people say I don't know what to do."_

**Edwin's own expectation for the first event is low and he said so.** He expects
to lose around two million on the opening and called it a likely mess, while
holding that the business works in the long run. Cody disagreed with the number.
Recorded because it sets what "success" means on the 22nd: not a flawless
offering, but one that does not lose users.

## Not delivery, but worth knowing

Edwin and Cody are considering a **separate product for prediction-market
traders**: the strategy development tool, fed with normalised Sportradar history,
sold to people trading Kalshi who have no historical data of their own. Edwin
built three profitable strategies from 25 years of data in about eighteen hours
of work. They may spin it up within two to three weeks. It is not on this
delivery plan, and it competes for the same attention.
