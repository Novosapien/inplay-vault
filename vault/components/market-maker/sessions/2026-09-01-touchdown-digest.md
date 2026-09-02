---
description: "Session note for the 1 September touchdown digest: the never-empty-book rule, phantom liquidity from cancel-replace, and the ask for participation inputs."
---

# 2026-09-01 · the Monday touchdown digest

> **Who:** Lily (Novosapien) with Claude · call attendees Cody, Troy, Jared,
> Kevin, Max (InPlay) and Brett, George, Hasan, Lily (Novosapien). Edwin absent
> **Type:** call digest
> **Refs:** [[01-09-2026-touchdown]] · [[market-maker/decisions]] 2026-09-01 ·
> `N77` `N78` opened · `N75` addendum · [[market-maker/parameters]] ·
> [[market-maker/plan]]

## What we did

- Digested the 30-minute Monday touchdown, the first one after three days of
  real NCAA trading and two days before college week one.
- Opened **`N77`** (a book must never be empty) and **`N78`** (the maker cannot
  see its own market), and added the `UNCC` no-bid report to **`N75`** rather
  than opening a third item for the same mechanism.
- Recorded the client-visible consequence of the 20 August size squash against
  `base_size` and `levels_range` in [[market-maker/parameters]].
- Logged the two non-MM items that gate everything else this week: the app-wide
  lockout and the suspended AI tooling.

## What we learned

- **Troy argued the single-maker case as a design constraint for the first
  time.** *"there's no other market makers there that can support that
  liquidity... we almost have to operate as like two or three market makers at
  once because there's no one else leaning on us."* That reframes the never-empty
  ask from a preference into a structural requirement.
- **The client has independently arrived at `N75`.** What George settled on
  30 August from the reconciler's side, Troy described from the screen: the
  book clears, the market order is in flight, and the fill is not there.
- **George diagnosed his own machine unprompted**, and it is the most useful
  sentence of the call: the maker prices off Sportradar's probability alone, so
  *"there could be a thousand users or 10,000 users, the market maker's still
  going to be functioning in more or less the same way, by design."*
- **The word "phantom" now means two different things in this vault.** `N41` is
  the market-data feed showing a touch that does not exist. Troy's phantom is
  the ordinary cancel-replace window working exactly as built. They must not be
  merged.
- **Jared gave us a real scale case, not a hypothetical:** Hawaii against
  Stanford, where the price moved hard and everybody would have been in the same
  book, while the quiet games ran fine.

## What went wrong / got stuck

- **Nothing on this list can be worked this week.** The app is locked out for
  every user with no identified cause, and the AI tooling that would normally
  find it is suspended over an unpaid bill, so the whole team is reading code by
  hand. Troy cancelled the same-day tZERO call to free them up.
- **`UNCC` was reported by the client, not caught by us.** The 29 August Tar
  Heels freeze had the same mechanism and produced `MARKETABLE_GUARD_STALLED`
  nine times, so the alarm exists. It did not reach anyone before Cody did.
- **The size squash landed back on us as a defect report.** The parameters are
  doing exactly what they were set to do on 20 August, at the client's own ask.
  Worth stating plainly when `N78` goes to Edwin, because sizing off
  participation is the honest answer to it and re-raising the old numbers is not.

## Decisions made *(mirrored into [[market-maker/decisions]] 2026-09-01)*

- ✅ George confirmed the momentary empty book is **by design, not a fault**, and
  named the venue constraint: tZERO has no replace-in-place, so a move is cancel
  then replace. Two directions offered, neither chosen: a topping-up design, or
  fast enough that the gap stops mattering.
- 📝 No ruling on `N77` or `N78`. Both are asks awaiting Edwin, who was absent.

## Questions opened / closed *(mirrored into [[market-maker/open-questions]])*

- **Opened `N77`** the never-empty book. Settle it **with** `N75`, not beside it:
  the 23-07 ordering rules are the design that answers it. What `N77` adds is an
  explicit never-empty invariant, which is stronger than "do not self-cross" and
  does not obviously fall out of the ordering rules on its own.
- **Opened `N78`** participation inputs for sizing. Two candidates, both ours
  already: in-game traded volume and participant count. ⚠ Determinism is the
  design constraint, not an afterthought.
- **`N75` gains a second book** and a second reporter: `UNCC`, five days after
  `IPTCNCTH`.
- ⚠ **Priority list reset**, with a line above it saying nothing moves until
  the app is back up.

## Next

- **Nothing on the maker until the lockout is closed.** When it is: put `N77`
  and `N75` to George as one question, because they have one answer, and take
  `N78` to Edwin as a sizing ask with the Hawaii-Stanford game as the case.
