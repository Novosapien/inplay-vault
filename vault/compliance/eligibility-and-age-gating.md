---
description: "The three trader tiers and what each is legally permitted to do: the 13+/18+ line, KYC, US tax residency, cash-prize eligibility and ad-inventory gating."
---

# Eligibility and Age Gating

> **Section:** [[compliance/compliance]]
> **Product home:** [[customer-onboarding/customer-onboarding]] owns the
> journeys. This doc owns the **rules those journeys must satisfy**.

## Why the model changed

Until 03-08 there was one path: sign up, complete Persona KYC, trade. Two
problems forced a rethink, both raised on the 03-08 call:

1. **KYC is killing the funnel.** Edwin's own brother-in-law and sister-in-law
   reached the KYC step and stopped, having previously had their identities
   stolen. Signups sat at ~118 and were majority friends and family.
2. **International students cannot complete it.** Troy's university programme
   (DePaul curriculum, plus Harvard, Texas A&M and others) is full of students
   who are not US tax residents and so cannot receive a cash payout at all.

Edwin's conclusion, 03-08:

> "In order to qualify for any money payouts, you're going to have to fill out
> the KYC. That's a must. Now if you want to trade on the public forum, the one
> with no money, no rewards, you should be able to do that too."

The KYC-free tier is also a **funnel stage**, not a giveaway: free play →
KYC for cash → (eventually) a real brokerage account.

## The three tiers _(named 07-08)_

| Tier | Who | Verification | Can trade | Cash prizes | Leaderboard |
|------|-----|-------------|-----------|-------------|-------------|
| **Trader Full** | US tax resident, 18+ | Full Persona KYC | Yes | **Yes** | Yes |
| **Trader Medium** | International student / non-US-tax-resident, 18+ | Persona KYC (identity only, no tax residency) | Yes | No | Yes _(to confirm)_ |
| **Trader Light** | Anyone 13+ | Email only, plus a 13+ attestation | Yes | No | Micro-challenges only _(to confirm)_ |

Troy's framing of the same three tiers, by legal purpose (07-08):

1. **Entertainment purposes only**: Trader Light
2. **Educational purposes**: Trader Medium
3. **Skill-based trading competition**: Trader Full

That framing is deliberate: "skill-based competition" is the category InPlay
wants the cash-prize tier to sit in, and it ties back to the
[[compliance/regulatory-positioning|not-a-game-of-chance]] argument.

## The rules

- **13 is the floor.** Under-13s cannot hold any account (US law). The app
  takes an **attestation** that the user is 13 or over.
- **18 is the cash line.** Trading a regulated security requires 18+. Because
  the challenge is a simulator, everyone can trade; only **cash payouts**
  require 18+ verified. Troy, 07-08: "Everyone can get an account. It's a
  simulator. The only people that can get cash payouts are people that go
  through the full KYC and validate that they're 18 and over."
- **US tax residency gates payouts**, separately from age. It is what drives the
  W-9 requirement in [[withdrawal-flow/withdrawal-flow]].
- **InPlay validates KYC, not tZERO.** The verification decision sits on the
  InPlay side via Persona.
- **App-store age rating** should be set to 13+ so parental controls can block
  it upstream (Troy's suggestion, 07-08).
- **Ad inventory must be gated.** A non-signed-in or non-KYC user may only be
  served under-18-safe inventory. No alcohol, no gambling adjacency. George,
  03-08. This is a hard constraint on [[advertising/advertising]].

## Known blocker: the tZERO onboarding API _(07-08)_

tZERO's onboarding API is built for full KYC. InPlay only fills three of its
~20 fields, because tZERO already relaxes validation on the rest for InPlay's
requests. **Date of birth is still mandatory and must be 18+**, which blocks
account and wallet creation for Trader Light.

The ask: can tZERO turn off DOB validation the same way they turned off the
other fields? Without it, a Trader Light user cannot be allocated a tZERO
account ID and wallet ID, and therefore cannot trade at all.

Tracked as an open tZERO item; raised in the InPlay/Novo Slack channel.

## Open questions

| # | Question | Owner | Status |
|---|----------|-------|--------|
| G1 | Will tZERO relax the **18+ date-of-birth validation** on the onboarding API for the no-payout tiers? ➕ **14-08:** tZERO said they **will** remove the 18+ requirement. ➕ **24-08:** removing the KYC layer is now the **highest priority** (Troy), gating **secondary trading opening Thursday 27 August**; George sized it at one to two days. ⚠ The 24-08 call **never mentions the date-of-birth check**, so it stays open: **confirm it is actually switched off before treating Thursday as safe**. See [[24-08-2026-touchdown]] | tZERO | 🟡 **Agreed 14-08, removal unconfirmed; now on the Thursday critical path** |
| G2 | Do **Trader Medium** and **Trader Light** appear on the main leaderboard, or only on micro-challenge leaderboards? | Edwin / Troy | 🔴 Open |
| G3 | What exactly does the 13+ attestation look like, and is a bare checkbox sufficient in every state? | Edwin / legal | 🔴 Open |
| G4 | How is the under-18-safe ad inventory actually enforced at the SSP level, per network? | Novosapien, Brett | 🔴 Open |
| G5 | Can a Trader Light user upgrade in place to Trader Full without losing position history? | Novosapien / product | 🔴 Open |

## Sources

[[03-08-2026-touchdown]] · [[07-08-2026-touchdown]] · [[29-07-2026-touchdown]]
