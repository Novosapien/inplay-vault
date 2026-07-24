# InPlay Trading Challenge — Withdrawal Flow

> **Vision:** [[vision]]
> **Audiences:** [[audiences]]
> **Date:** 2026-05-14
> **Status:** Stub
> **Sources:** _[[12-05-2026-onboarding-and-renewal-and-global-component]], [[22-07-2026-touchdown]]_

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
- **Cash wallet hosting:** on T0 chain (decided in onboarding call to sidestep store-of-value licensing exposure)
- **Eligibility verdict:** received from [[components/referral/referral]] — user must satisfy Referral's cash eligibility rules (e.g., 10 referrals + location-on + other rules TBD) before withdrawal proceeds
- **Eligibility surfacing:** if any requirements are unmet, the withdrawal flow shows a transparent checklist — never a hidden T&C (Skye principle)
- **Tax automation / W9 (22-07):** a new **tax-automation vendor** is being added so that when a user **wins a cash prize and withdraws over a threshold amount**, an automation **triggers a W9 form** fill. Two vendors were in conversation as of 21-07. This **jumped ahead of HubSpot** in the backlog. It **must be ready by 29 Aug** (first games): a winner could withdraw cash that night. Edwin notes settlement is 29 Aug even if the payment lands 30 Aug, i.e. within the first 24 hours of games ending. (Source: [[22-07-2026-touchdown]])
- **Payouts + tax forms are the "blind spot" pre-launch (24-07):** George flagged **payouts, tax forms, and notifications** as the last structural pre-launch additions, with payouts/tax forms the least-defined. **Agreed launch fallback:** if the payment-provider deal is **not signed/integrated by launch**, still show **qualified winners and their amounts** and simply **delay the actual pay-out** by a couple of weeks. Not being able to pay out is **far less bad** than not having trading/market-maker. Edwin: a manual **interim** (Zelle / wire / "whatever") is acceptable to start; the **payment processor is becoming a bugaboo** and the exact method "really doesn't matter" for the interim. (Source: [[24-07-2026-touchdown]]) See [[integrations]] (Pay.com + redundant processor, vendor selection 23-07).

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
- **Which tax-automation vendor** (two in evaluation as of 22-07) and its integration mechanics; must be live by 29 Aug
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
- T0 cash-wallet → bank/crypto wire mechanics

---

## Cross-references

- **[[components/customer-onboarding/customer-onboarding]]** — establishes the user identity + cash wallet that this flow operates on
- **[[components/referral/referral]]** — supplies the eligibility verdict and the transparent checklist UX
- **T0** — hosts the cash wallet; payout mechanics depend on T0 capability
