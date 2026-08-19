---
description: "Stub component doc for the withdrawal flow — known decisions (bank/crypto/1099 capture at first withdrawal, W9 automation by 29 Aug) plus open questions"
---

# InPlay Trading Challenge — Withdrawal Flow

> **Vision:** [[vision]]
> **Audiences:** [[audiences]]
> **Date:** 2026-05-14
> **Status:** Stub
> **Sources:** _[[12-05-2026-onboarding-and-renewal-and-global-component]], [[22-07-2026-touchdown]], [[03-08-2026-touchdown]], [[07-08-2026-touchdown]]_
> **Updated:** 2026-08-10 — **Avalara** selected for W-9 with the middle-ground embed path; payout processor still unresolved; payout eligibility now restricted to the Trader Full tier.

---

## Summary

Surfaced as a separate component during the 12-06-2026 onboarding extraction. The decision: **bank info, crypto wallet linking, and 1099 tax info are captured at first withdrawal — not at signup.** This kept onboarding lean and pushed the heavier compliance lift to the moment the user is converting InPlay$ to real cash.

This component is **not yet documented** — a dedicated session with InPlay is required to flesh it out. Stub created so cross-component references in [[components/customer-onboarding/customer-onboarding]] and [[components/referral/referral]] resolve correctly.

---

## What we know

- **Trigger:** user requests their first withdrawal of real cash
- **Captures at this point:**
  - Bank information (US users)
  - Crypto wallet address (global users, Coinbase or similar — referenced via Iris conversation)
  - 1099 tax information (US users)
  - **W9 automation (22-07):** cash-prize withdrawals over a threshold auto-trigger a W9 form via a dedicated tax-automation vendor (see below)
- **Pattern reference:** Cody — _"I've dealt with that. I was going to treat it the same way I've dealt with high stakes fantasy is you fill in all that information once you request a withdrawal."_
- **Cash wallet hosting:** on tZERO chain (decided in onboarding call to sidestep store-of-value licensing exposure)
- **Eligibility verdict:** received from [[components/referral/referral]] — user must satisfy Referral's cash eligibility rules (e.g., 10 referrals + location-on + other rules TBD) before withdrawal proceeds
- **Eligibility surfacing:** if any requirements are unmet, the withdrawal flow shows a transparent checklist — never a hidden T&C (Skye principle)
- **Tax automation / W9 (22-07):** a new **tax-automation vendor** is being added so that when a user **wins a cash prize and withdraws over a threshold amount**, an automation **triggers a W9 form** fill. Two vendors were in conversation as of 21-07. This **jumped ahead of HubSpot** in the backlog. It **must be ready by 29 Aug** (first games): a winner could withdraw cash that night. Edwin notes settlement is 29 Aug even if the payment lands 30 Aug, i.e. within the first 24 hours of games ending. (Source: [[22-07-2026-touchdown]])
- **Payouts + tax forms are the "blind spot" pre-launch (24-07):** George flagged **payouts, tax forms, and notifications** as the last structural pre-launch additions, with payouts/tax forms the least-defined. **Agreed launch fallback:** if the payment-provider deal is **not signed/integrated by launch**, still show **qualified winners and their amounts** and simply **delay the actual pay-out** by a couple of weeks. Not being able to pay out is **far less bad** than not having trading/market-maker. Edwin: a manual **interim** (Zelle / wire / "whatever") is acceptable to start; the **payment processor is becoming a bugaboo** and the exact method "really doesn't matter" for the interim. (Source: [[24-07-2026-touchdown]]) See [[integrations]] (Pay.com + redundant processor, vendor selection 23-07).

- **Tax vendor selected — Avalara — and the integration path chosen (03-08).**
  Cody brought back three integration options, **all the same price**, and the
  **middle one is the decision**:

  | Option | Shape | Verdict |
  |---|---|---|
  | Zero dev | Off-the-shelf, user leaves the product entirely | Rejected |
  | **Middle ground** | **A single line of embed code** on an InPlay-branded landing page on the website. The user clicks withdraw in-app, hits a screen saying "to continue receiving your withdrawal amount, fill out your W-9", and is hyperlinked out to the browser. **It looks entirely like InPlay, not Avalara**, because the design lives on our page | ✅ **Chosen** |
  | Full SDK | W-9 completed **inside** the app, user never leaves | Deferred to post-launch, during the trading challenge |

  Avalara estimate the middle option at **no longer than a few hours** of work.
  George's caveat, wry: _"their dev time is human dev time."_ Novosapien to read
  the documentation. Cody deliberately simplified the choice to protect the
  build: _"I was trying to simplify it as much for you guys."_
  (Source: [[03-08-2026-touchdown]])
- **⚠ Payouts remain the unresolved half (03-08).** The tax form now has a path;
  the **payment provider does not**. George: _"at the moment we don't really
  have any visibility into what platform."_ Progress is blocked on people, not
  decisions — Brian was on vacation until the Wednesday, and the merchant
  application had to be **reassigned to Edwin** because the provider's portal
  (_"built from like before 1999"_) does not allow an application to be
  transferred between people. Charles is rebuilding and resending it.
- **Eligibility is now tier-based (03-08 / 07-08).** Only **Trader Full** users
  (18+, full Persona KYC, **US tax resident**) can receive a cash payout at all.
  Trader Medium (international students) and Trader Light (email-only) can
  trade and compete but never withdraw. This is what makes the W-9 requirement
  tractable: everyone reaching this flow is by definition a US tax resident.
  Rules in [[compliance/eligibility-and-age-gating]]; journeys in
  [[customer-onboarding/customer-onboarding]].

---

## What we don't know

- Withdrawal UX flow — screens, fields, validation, error states
- Minimum withdrawal threshold
- Withdrawal frequency limits
- Holding periods / clearance windows
- KYC re-verification at withdrawal — required or not?
- Crypto wallet linking UX (Coinbase integration mechanics)
- Tax handling: 1099 capture, year-end reporting, withholding rules
- The **withdrawal threshold value** that triggers the W9 automation (TBD as of 22-07)
- ~~Which tax-automation vendor~~ **✅ ANSWERED 03-08: Avalara**, middle-ground embed integration. Still open: the exact **withdrawal threshold** that triggers the W-9, and whether the hyperlink-out step hurts completion enough to justify pulling the full SDK forward
- **Which payment provider processes the actual payout** — still open, and now the biggest gap in this component
- FX exposure / conversion handling for non-USD users
- Failure modes — what if the bank rejects, what if Coinbase wallet is invalid, etc.
- Audit / fraud review workflow for high-value withdrawals
- Customer support routing for withdrawal issues

---

## Open Questions for Next Call (InPlay team)

This component needs a dedicated session. Key starting questions:

- Full UX walk-through — how should the withdrawal screen look and feel?
- Bank info capture — fields, validation, third-party integration (Plaid? direct?)
- Crypto wallet — Coinbase as primary? Others supported? Same KYC re-flow or piggyback on Persona?
- 1099 capture flow — TaxJar-style integration, or first-party?
- Minimum withdrawal, frequency, holding periods?
- Eligibility verdict handoff from Referral — interface contract
- Failure & dispute flows — including the bad-experience precedent Edwin's $900 Polymarket incident represents (28 hours to first response, 4 days to credit)
- Cybersecurity for bank + 1099 data — coordinate with the cross-cutting Cybersecurity & Data-Handling Framework
- tZERO cash-wallet → bank/crypto wire mechanics

---

## Cross-references

- **[[components/customer-onboarding/customer-onboarding]]** — establishes the user identity + cash wallet that this flow operates on
- **[[components/referral/referral]]** — supplies the eligibility verdict and the transparent checklist UX
- **tZERO** — hosts the cash wallet; payout mechanics depend on tZERO capability
