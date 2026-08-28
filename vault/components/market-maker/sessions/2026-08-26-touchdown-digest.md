---
description: "Digest of the 26-08 touchdown for the market maker: secondary opens Thursday 09:30 Eastern, and the Sportradar gap becomes the largest risk to the first game day"
---

# 2026-08-26: the open has a time, and the data gap has a consequence

> **Who:** Claude (`/meeting-digest`) for Lily
> **Type:** call (digest of a touchdown, not a working session)
> **Refs:** [[26-08-2026-touchdown]] · [[market-maker/open-questions]] `S12` ·
> [[market-maker/plan]] · previous: [[market-maker/sessions/2026-08-24-touchdown-digest]]

## What we did

Digested the Wednesday touchdown of 26 August, 34 minutes, held on the **final day
of the NCAA IPO draft**. Most of the call is onboarding and comms. Two items land
on the market maker, and one of them is the biggest risk on the board.

## What we learned

- **The open has a time.** The IPO window closes **22:00 on Wednesday 26 August**
  and **secondary trading opens Thursday 27 August at 09:30 Eastern**. Troy chose
  the morning over an automatic flip at window close so the team is online to
  **QA the open** and confirm the locks came off. First games **Saturday 29
  August**, 138 teams live.
- **The Sport Radar gap has a named consequence.** George: without that data
  _"the market maker is going to be way more volatile than it needs to be. Like it
  might just drop off."_ That is a market-quality failure, not a missing nice to
  have, and it lands on the first live game day.
- **Escalation state on `S12`.** Sport Radar have **three engineers** on a bug open
  for a couple of weeks and say it will be fixed **absolutely before Saturday**;
  if they miss, InPlay gets **a credit on the bill**. George pulls the endpoint
  **once or twice a day**; Cody pressured them again on the 26th.
- **George is building a fallback.** _"I don't want to call them hacks, but maybe
  different ways of doing it."_ That work runs until the first game day.

## What went wrong / got stuck

- **`S12` is now the largest open risk to 29 August**, and it is owned by a third
  party whose last promise (a fix by Thursday 20-08) was missed with no reply to
  two chases. A credit on the bill does not price a bad first game day.
- ⚠ **The fallback has no shape yet.** _"Different ways of doing it"_ is not a
  plan, and the deadline is three days out. **Next session should make the
  fallback explicit**: what the maker uses for expected wins if the endpoint is
  still dead on Saturday morning, and who decides to switch to it.

## Decisions made *(mirror into [[market-maker/decisions]])*

- **None from this call for the MM.** The secondary-open time is a delivery
  decision, recorded in [[market-maker/plan]] and [[ipo-module/ipo-module]].

## Questions opened / closed *(mirror into [[market-maker/open-questions]])*

- **`S12` escalated**, not merely updated: the consequence is now stated, the
  deadline is the first game day, and the owner is a supplier who has already
  missed once.
- Nothing closed. `N53` (the sold-out book and its position transfer) and `T17`
  (the test-ticker replica) went unmentioned on this call, so both stand where
  the 24-08 note left them.

## Next

- **Give the Sport Radar fallback a shape before Saturday.** What does the maker
  price on if the endpoint is still dead, and who makes the call to use it?
- **Chase `N53` and `T17`**, neither of which moved this week, and secondary opens
  tomorrow.
