---
description: "The project to-do list — open IA, leaderboard, data and integration questions, each linked to its component doc"
---

# InPlay Trading Challenge -- To-Dos

> **Project:** [[index]]

## Information Layer

- [ ] Resolve IA question: is [[game-day-overview]] a separate page or a tab within [[discovery-home]]?
- [ ] Define the [[research-tab]] -- needs dedicated session with Edwin and Cody
- [ ] Determine news feed placement -- where does the SR newswire appear? [[discovery-home]]? [[team-page]]? Both?
- [ ] Determine order book depth display -- how much Bloomberg-style data on mobile? Full book or top of book? ([[single-game-page]])
- [ ] Define "comeback trader" metric for [[leaderboard]] -- biggest absolute swing? percentage? recovery from negative?
- [ ] Define "risk-adjusted return" plain-English label for [[leaderboard]] -- can't use "Sharpe ratio" in UI
- [ ] Sport Radar client setup call -- logo toggle decision, widget customisation, ad placement within match tracker
- [ ] Define featured games selection criteria for [[discovery-home]] -- editorial? algorithmic? advertiser-driven?
- [ ] Determine whether [[team-page]] includes player-level data or team-level only
- [ ] Define leaderboard payout structure -- how many places pay out per vertical per time horizon?
- [ ] Define proximity alert thresholds for [[leaderboard]]
- [ ] Resolve daily leaderboard reset timing -- games spanning midnight ([[leaderboard]])

## Architecture

- [ ] Data source matrix: map what comes from Sport Radar, what from tZERO, what InPlay stores internally
- [ ] Define the cross-correlation data store ("mem store" per Brett) for volatility annotations
- [ ] Tech stack decisions -- not started

## Other Components

- [ ] Schedule Trading component deep-dive session
- [ ] Schedule remaining component sessions (Onboarding, Referral, Third Space, Education, Websites)

## 2026-08-13 — from the preseason go-live session (George)

- [ ] **Testing Market Maker, on testing tickers.** Tonight the testing
  mm-publisher publishes real-game probability readings onto the ONE shared NATS
  bus, relying on the MM's idempotency to absorb duplicates. That is fine for
  dual-publishing identical facts, but it means there is no way to test MM-side
  changes in isolation: a testing MM would consume the same subjects as
  production. Wanted: a testing MM instance that trades only a TESTING ticker
  universe (its own symbols, its own subjects — e.g. a `test.` subject prefix on
  the readings stream), so the whole probabilities→MM→pricing path can be
  exercised without touching production tickers. Pairs with the existing C15
  lease gap (each pool runs exactly 1 publishing instance) and the noted tfvars
  drift (mm-publisher-testing points at prod Redis).
- [ ] After tonight: scale `inplay-mm-publisher-testing` back to 0 AND set
  `mm_publisher_instances = 0` in terraform.testing.tfvars (they currently
  disagree: tfvars says 1, live was 0, tonight it runs 1 deliberately).
