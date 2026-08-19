---
description: "Cross-cutting compliance hub: the regulatory posture InPlay trades under, and the constraints it puts on product, copy and eligibility."
---

# Compliance

> **Project:** [[index]]
> **Status:** Collecting _(opened 2026-08-10 from the 31-07 / 03-08 / 07-08 touchdowns)_

## Why this exists

Compliance is not a component. It is a **constraint layer that sits over every
component**: what the app may say, who may hold an account, which surfaces need
a disclosure, and which words trigger a filing problem. Until now these
constraints were scattered through meeting notes. They now live here.

The one-line posture, in Edwin's framing (31-07):

> InPlay is **not outcome-dependent**. A share's value is set by its **price**,
> which is an estimate of an operating company's on-field and off-field
> earnings. The result of a game informs that estimate; it does not settle the
> instrument. That distinction is the entire regulatory argument.

Everything in this section exists to protect that distinction.

## Documents

| Document | What it covers |
|----------|---------------|
| [[compliance/regulatory-positioning\|Regulatory positioning]] | The securities-not-gambling argument, the SEC offering circular, gun-jumping and Rule 255, the Kalshi litigation, state-by-state registration |
| [[compliance/eligibility-and-age-gating\|Eligibility and age gating]] | Who can hold which account tier, the 13+/18+ line, tax residency, and what each tier is allowed to see and win |

## Live constraints on the build

These are the compliance rules the product must satisfy **before launch**.
Each is sourced to the call it came from.

| # | Constraint | Bites on | Source |
|---|-----------|----------|--------|
| C1 | Never describe the offering as "regulated by the SEC". All such copy comes down | App copy, website, [[ipo-module/ipo-module]] | 07-08 |
| C2 | Always say **"simulated IPO"**, never a bare "IPO" | App copy, website, [[ipo-module/ipo-module]] | 07-08 |
| C3 | A **Regulation A testing-the-waters (Rule 255) disclaimer** must appear in the app | App surfaces | 07-08 |
| C4 | Cash payouts require full KYC **and** US tax residency **and** 18+ | [[customer-onboarding/customer-onboarding]], [[withdrawal-flow/withdrawal-flow]] | 03-08, 07-08 |
| C5 | Non-KYC accounts must only be served **under-18-safe ad inventory** (no alcohol etc.) | [[advertising/advertising]] | 03-08 |
| C6 | Team naming must not read as the real franchise (ticker/acronym convention instead) | [[trading/trading]], [[information-layer/information-layer]] | 27-07 |
| C7 | State-by-state rules apply; **California** needs extra geolocation disclaimers | Onboarding, app store listing | 03-08 |
| C8 | Marketing and disclosure obligations follow the **broker/financial-instrument** regime, not the gambling regime | All outbound copy | 03-08 |
| C9 | The **Messaging House lexicon** governs every word in public copy, app included. Always investors, shares, buy/sell/hold, earnings, market price. Never users, players, bettors, bets, picks, odds, win money, payout, cash out, risk-free, guaranteed, approved, or "own your team" | App, both sites, all outbound | Messaging House v2.0, 31-07 |
| C10 | Securities vocabulary **never appears on the Challenge site**. The only bridge between the Challenge and the offering is the "About InPlay" footer link | [[challenge-website/challenge-website]] | Punch List 1, C8 standing |
| C11 | **No named competitors and no legal conclusions** in public copy, including about InPlay's own legality beyond a factual description of the structure | All outbound | Messaging House v2.0 |
| C12 | **No performance promises or return expectations, ever.** No betting-shaped promotions: no deposit matches, no risk-free mechanics, no free-bet analogs. Brokerage-pattern mechanics (referral shares, fractional shares) are the approved shape | [[referral/referral]], all outbound | Messaging House v2.0 |

## The two governing documents (Edwin, 31-07-2026)

Two documents arrived from Edwin on 31 July and govern all public language. Both
live in `shared/clients/inplay/outbound-campaigns/`.

- **Messaging House v2.0** is the single source of truth for how InPlay talks
  about itself. Its own words: _"If copy conflicts with this document, this
  document wins."_ It carries the master idea (**Ownership, not outcomes**), the
  boilerplate, the three audience pillars, the proof-point bank, the lexicon
  above, seven **red lines**, the campaign phasing, and the voice rules. The
  news posture is explicit: nobody responds in real time to a regulator,
  journalist or platform inquiry; acknowledge, take details, route to counsel
  and the founder the same day.
- **Website Punch List 1 v1.3** is the 35-item work list against both sites,
  each item tagged by owner (`DEV`, `COUNSEL`, `EDWIN`, `POLICY`) and priority
  (P0 same day, P1 this week, P2 travels with the counsel package, P3 before
  kickoff). Largely implemented across 2 to 5 August; the P2 items wait on
  counsel. Tracked on the delivery flight plan, see [[delivery/delivery]].

> ⚠ **Live conflict.** The Messaging House bans **"play"** as the product verb
> and bans **"win money"** and **"payout"**. Punch List item C9 sets the
> approved Challenge phrasing as _"Free to enter. Fully simulated. No real money
> at risk."_ But the first-open tour Edwin demoed on 07-08 reads _"It's free to
> play"_ and _"real cash prizes if you're verified"_. One has to give before app
> copy freezes. Recommendation: follow Punch List C9, because it is the
> counsel-facing wording and the Messaging House is the governing document by
> its own terms. Needs a one-line ruling from Edwin.

## Owners

- **Edwin** owns the regulatory strategy and the relationship with counsel
  (Vogler, Marlin) and the SEC filing.
- **Novosapien** owns implementing the constraints in the app and flagging any
  new surface that touches them.
- No compliance copy ships without Edwin's legal review. The 03-08 call has a
  worked example: Edwin's first explainer story was **denied by legal the same
  morning** it was written.

## Open questions

See [[compliance/regulatory-positioning]] and
[[compliance/eligibility-and-age-gating]] for the live list. Cross-cutting
architecture questions stay in [[architecture/open-questions]].
