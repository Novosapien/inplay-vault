---
description: "Digest of the 24-08 touchdown for the market maker: the shorting constraint corrected, the test-ticker replica, and the first sold-out book with its position-transfer fix"
---

# 2026-08-24: the shorting correction, the replica, and the first book with no float

> **Who:** Claude (`/meeting-digest`) for Lily
> **Type:** call (digest of a touchdown, not a working session)
> **Refs:** [[24-08-2026-touchdown]] · [[market-maker/open-questions]] `T16` `T17`
> `E26` `N50` `N53` `S12` · [[market-maker/plan]]

## What we did

Digested the Monday touchdown of 24 August, 18 minutes, the first since the NCAA
offering opened on Saturday 22 August. **Edwin did not join.** Four of the call's
items touch the market maker; the rest is IPO distribution, KYC and app-store
business.

## What we learned

- **The shorting constraint runs the opposite way to our assumption.** Troy,
  correcting George on the call: _"There's no limit on the shorts in the
  simulation. There's a limit on the shorts in production."_ An **additional
  1,000,000 shares per team is eligible for shorting**, so a million long and a
  million short. **tZERO have turned the locate flag off**, allowing shorts of up
  to **100% of the longs**. Edwin is separately emulating the production
  constraint by having the maker acquire stock **to loan out**, which Troy called
  _"not a fully functional need right now"_. Goes to the tZERO call on **25-08**
  to confirm.
- **The test-ticker constraint has a number on it: ten.** That is why replay
  testing works but a replica test during live games does not. tZERO will supply
  **a full replica of all the test tickers**, so a maker quoting **five levels
  instead of three** can be tested against live games with **zero effect on
  users**.
- **A book has already sold out.** The **Florida Atlantic Owls**, so the public
  holds the entire float and the maker has nothing to offer there.
- **George's fix for it is a position transfer.** Most of that stock was bought by
  **the taker**, so transfer positions back to the maker and it has inventory to
  quote with. He does not treat it as a crisis.
- **Dates:** IPO window closes **Wednesday 26 August**, secondary opens
  **Thursday 27 August**, no games until **Saturday**. The gap is deliberate.
  Thursday is gated on the KYC-layer removal, not on us.

## What went wrong / got stuck

- **The sold-out fix rides on the mechanism `N50` questions.** Position transfer
  is `35=UPT`, which applies a **signed delta and is not idempotent**. If we get
  the size wrong on a live book it is not obviously reversible. Prove it on a test
  ticker before running it on FAU.
- **Nobody has counted the near-misses.** One sold-out book is an incident. If
  twenty books are within a few thousand shares of sold out, it is a launch
  condition and the position-transfer plan needs to be a procedure, not a
  one-off.
- **`S12`: the Sport Radar NCAA futures endpoint is still down**, and this one
  lands on us, because George needs it for **expected wins**. Cody chased twice
  over the weekend after being promised a fix by Thursday and got no reply either
  time. His stand-in CSV comes from a second provider and **decays in about five
  days**, because futures move with results.
- ⚠ **`S10` reads too confidently in hindsight.** It was closed 28-07 as
  superseded by Edwin's own daily feed. George is nonetheless asking Sport Radar
  for NCAA futures data, so the closure covered Edwin's need, not ours. `S12` is
  filed separately rather than reopening it.

## Decisions made *(mirror into [[market-maker/decisions]])*

- **None.** Every market-maker item from this call is a correction, a status
  change or an open question, so `decisions.md` is deliberately untouched.

## Questions opened / closed *(mirror into [[market-maker/open-questions]])*

- **Opened `N53`**: a sold-out book leaves the maker with no float to offer.
  Records George's position-transfer fix and the two things to close before
  Thursday.
- **Opened `S12`**: the NCAA futures endpoint, escalating, workaround expiring.
- **`T16` and `E26` corrected**, not merely updated: the venue is **not** the
  near-term short constraint. Edwin's rules are now the only thing outstanding.
- **`T17` advanced** to 🟡, with the full replica promised. Stays open until it
  lands and an order goes through it.

## Next

- **Prove the position transfer on a test ticker**, then size it for the Florida
  Atlantic Owls. Read `N50` first.
- **Count how many other NCAA books are near sold out**, before Thursday.
