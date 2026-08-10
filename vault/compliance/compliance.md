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
