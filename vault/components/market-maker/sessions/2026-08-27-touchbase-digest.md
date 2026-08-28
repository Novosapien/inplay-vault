---
description: "Digest of the 27-08 touchbase: the IPO holding structure reversed with the maker as NFL buyer, and the price unlocked from win probability, both left unfinished"
---

# 2026-08-27: the structure is backwards, and the price is not the probability

> **Who:** Claude (`/meeting-digest`) for Lily
> **Type:** call (digest of a touchbase, not a working session)
> **Refs:** [[27-08-2026-touchbase]] · [[market-maker/decisions]] 2026-08-27 ·
> [[market-maker/open-questions]] `E54` `E55` `E56` `N54` `S12` `N53` `N21` ·
> previous: [[market-maker/sessions/2026-08-26-touchdown-digest]]

## What we did

Digested a 13-minute touchbase held the morning secondary trading opened. It is
short, it is almost entirely market maker, and **it was cut off mid-sentence** by
Troy for the tZERO go-live call. Edwin: _"let's come back to this because this is
very important."_ It has not resumed.

## What we learned

- **We built the IPO holding structure backwards.** The maker holds the shares
  and rests the sell orders; the taker buys. Edwin: _"So that's backwards."_ In
  his structure the team company sells, InPlay Markets is the broker dealer, the
  unsold remainder rests in the team-company treasury, and the maker is the
  **selling agent** holding real inventory. **For the NFL offering, the maker
  becomes the buyer.**
- **He accepted the NCAA build as it stands.** _"It's okay for now. Good sim."_
  So this is not a fix-it-now item, it is a rebuild-before-5-September item.
- **Selling from inventory is not shorting.** _"They don't have to do the short
  locates. So they're not getting short, they're just selling."_ This quietly
  narrows `E26` and is the first clean answer to the `N53` sold-out problem: a
  maker that holds inventory does not need to short to offer.
- **Treasury is real again**, which re-reverses the 12-08 retirement and finally
  gives `N21` a direction after four weeks.
- **The price must not be locked to win probability**, which supersedes the
  ✅ 23-07 decision that Chapter 3 has been built on. Edwin's example: an
  underdog wins 70 to nothing, the probability hits 100% so a locked price stops
  at $5, but the share should reach perhaps $10 because the market's view of the
  team changed. Range roughly zero to $12 per game.
- **Edwin withdrew his own scope request.** He asked for live admin-panel control
  of the maker's spread, and then: _"If there's any kind of change, then don't...
  I don't want to make any changes whatsoever until we have this secondary market
  up and trading."_ Worth recording as the first time that has happened.

## What went wrong / got stuck

- ⚠ **`N54`'s proposed mechanism is blocked by `S12`.** Edwin wants expected
  wins to move after a game and feed the price. **NCAA expected wins is static
  today** because the Sport Radar futures endpoint has been down a fortnight.
  George checked it immediately before the call. So the correction Edwin wants
  depends on the input we do not have, and that is the same input Saturday's
  pricing needs.
- ⚠ **The magnitude is undefined.** Nothing says how far a 70 to nothing win
  should move expected wins. That number is Edwin's and it was not given before
  the call ended.
- ⚠ **`E54` cannot be specified yet.** Troy stopped the conversation on
  terminology, and more importantly said there is _"a little misunderstanding
  about how the accounts get created"_, which was never resolved. Until InPlay
  come back with the cleaner language and the account model, writing the NFL
  primary means guessing which entity holds what.
- **The pattern worth naming.** `E30`, `E34` and now `N54` are three separate
  arrivals at one gap: **our price moves only on evidence, and Edwin keeps asking
  for it to move on expectation.** Three times is not a coincidence, it is a
  design position we have not adopted. The resumed call should settle it as one
  question rather than a third time round.

## Decisions made *(mirrored into [[market-maker/decisions]])*

- ✂ The IPO holding structure is backwards; the maker becomes the NFL buyer.
- ✅ The maker as seller does not need short locates.
- ✂ Treasury is real, holding the unsold remainder.
- ✂ The price must not be locked to win probability.
- 🟡 Per-game price range roughly zero to $12, proposed, not a parameter row yet.

## Questions opened / closed *(mirrored into [[market-maker/open-questions]])*

- **Opened `E54`**, now the top item on the list: the holding structure and the
  NFL buyer, with four sub-questions owed before it can be built.
- **Opened `N54`**: unlocking the price from win probability, and its blockers.
- **Opened `E55`**: the cleaner language, and the unresolved account model.
- **Opened `E56`**: credit terms from team companies to makers, exploratory only.
- **`N53` narrowed** by the no-short-locate point: a maker with inventory can
  offer without shorting.
- **`N21` given direction** by treasury being real, though not yet closed.
- Nothing closed. The call ended before anything finished.

## Next

- **Get the conversation resumed, this week.** `E54` changes the module that runs
  the NFL offering in ten days, and it is half-explained.
- **Ask the three-times question once, properly:** should the price move on
  expectation as well as evidence? `E30`, `E34` and `N54` are the same question.
- **Do not start building `E54`** until `E55` lands. Guessing which entity holds
  what is how the current structure ended up backwards.
