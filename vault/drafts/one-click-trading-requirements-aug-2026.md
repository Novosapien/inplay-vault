---
description: "Edwin's one-click trading model, demonstrated live on 14 August 2026: the toggle, the persistent trade bar, flatten, the order types and the confirmation pattern, with the design principle behind them."
---

# One-click trading: Edwin's demonstrated model

> **Source:** [[14-08-2026-touchdown]], demonstrated live from his own prototype
> **Lands on:** [[trading/trading]] · [[trading/sub-components/order-entry/order-entry]] · [[information-layer/sub-components/single-game-page/single-game-page]]
> **Status:** requirement set, not yet specced or estimated

Extracted separately from the meeting digest because it is a specification
rather than feedback. Edwin walked through it screen by screen while trading a
real market on another monitor, which is worth knowing: the model is what he
himself does for a living, not a guess at what a user might want.

## The principle underneath it

The app was built to protect a user from mistakes. The people testing it wanted
to trade at speed. Those two goals fight, and every confirmation step, page
transition and screen takeover costs about a second. **A trader who loses a
second loses the market**, which is exactly what Troy reported: he kept
_"missing the market"_ because by the time he had navigated, the price had gone.

Edwin's summary of what a trading surface owes its user: _"the most important
thing people want is to be able to trade. That's it."_ Everything below follows
from that.

⚠ **This inverts an earlier design intent, deliberately.** The persistent trade
bar and the confirmation step were introduced partly as a **fat-finger guard**
after Edwin praised that behaviour on 29 July, and partly to leave room for
advertising and share prompts. George named the divergence on the call: the team
optimised for safety and shareability, and the requirement is now speed. Both
readings came from Edwin, five weeks apart. That is worth stating plainly rather
than quietly reversing.

## The model

**1. A one-click toggle, on the trading surface itself.**
A visible switch that turns the confirmation step off. When Jared suggested
putting it in settings, Edwin refused explicitly: _"No, I wouldn't do that,
Jared. Please don't. I want it to be just like I have it here. One click trading
here. One click trading off. That's what I want. I don't want it in the more."_
The toggle changes behaviour **application-wide**, not per team or per screen.

**2. Buy and sell on every page, always loaded.**
Team page, company page, Gamecast, research. The trade controls do not move and
do not have to be summoned. Position size and P&L **carry across every layer**,
so the user never loses sight of where they stand while navigating.

**3. Flatten, in one click.**
A single control that closes the whole position regardless of size. Edwin used
it repeatedly in the demo: long 2,000, one click, flat. This is the exit
equivalent of one-click entry and it matters more, because exits are when people
panic.

**4. Order types, in the user's language.**
- **Market**, which is the synthetic market order underneath. Edwin was clear
  about the naming: _"it's a synthetic market order, but the public doesn't know
  what that means. So you just put market."_
- **Join the bid**, **mid**, and **ask** as one-tap choices.
- A **price toggler** to step a limit price up or down from the touch, so a user
  can bid below the market without typing.
- Working orders visible and cancellable from the same surface.

**5. Confirmation as a hover, not a takeover.**
With one-click off, the confirmation appears as an overlay on the same screen
rather than a new page. Nothing navigates. The user confirms and stays exactly
where they were.

**6. Never navigate away after a trade.**
The defect that caused most of the frustration: confirming a trade moved the
user to the portfolio, or worse to the IPO tiles. Cody counted **five screens**
to get back to the game he was trading. After a trade the user stays on the
game.

**7. Swipe between live games.**
Swiping the field moves to the next live game. The header states which team is
being traded, and it defaults to the home team. Switching to a team not currently
in play is done through the markets list rather than the swipe.

## What sits beneath it, and is not yet designed

Edwin acknowledged one gap when George pressed him. Editing an existing order
from the Gamecast is unresolved: he showed it working from the position panel,
and said the fuller order controls would need to be added to the right-hand side
of the game surface, which he had not built yet. **So the model covers place and
flatten well, and amend less well.** That is the open question to close before
this is specced.

## The disagreement worth preserving

Edwin's position is that the revenue comes from active traders, not casual
visitors: _"where we're going to make our money isn't the 50% who come on the
app once a week. We're going to make our money on the 30% of the people who are
addicted to the action."_ He also stated that on trading judgement, he and Cody
are the only two opinions that count.

George's counter, which is the product question rather than the trading one: if
one-click traders are only twenty or thirty percent at the start, **something has
to carry the other seventy percent from arrival to competence**. A toggle serves
the expert immediately; it does nothing for the person who does not yet know
they want it. Edwin's answer was instructional video on every surface, in the app
and on social.

Both are right about different users, and the plan needs to hold both. Recorded
here because it is the kind of tension that gets resolved by whoever writes the
ticket unless it is written down first.
