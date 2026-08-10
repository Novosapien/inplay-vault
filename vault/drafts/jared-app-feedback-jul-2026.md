---
type: source-feedback
received: 2026-07-24
author: Jared Sapirman
subject: Additional app feedback (6 items)
extracted-to:
  - "[[referral/referral]]"
  - "[[third-space]]"
  - "[[frontend-performance]]"
  - "[[trader-profile]]"
description: "Jared Sapirman's Jul 2026 app feedback — six items from referral contact invites to groups, cold-start speed and public usernames, each routed to a vault doc"
---

# Jared Sapirman, Additional App Feedback (Jul 2026)

> **Up:** [[components]] · [[index]]
> **Type:** source-feedback
> **Received:** 2026-07-24 from Jared Sapirman
> **Source file:** `Additional App Feedback.docx`

This is a written feedback document with six numbered items. Each is captured faithfully below (lightly paraphrased, specifics and figures preserved) with a note on where it was routed. Per digest doctrine these were folded into existing homes as additive, sourced notes; genuinely new features are flagged as candidates for a focused session rather than fully specced here.

---

## 1. Contact Permissions and Referral Invites

Enable contact permissions so users can invite people from their address book directly through the referral program. To maximise opt-in, the app should request contact access **only at the moment a user taps "Invite Friends,"** preceded by a **branded priming screen** explaining the benefit of sharing contacts. Priming screens of this kind have lifted comparable iOS permission opt-ins by **20 to 40 percentage points**. On **iOS 18+**, the flow should be built around Apple's **limited contact picker** and per-contact **Access Button**, since full address-book access is no longer the default user behaviour.

**Routed to:** [[referral/referral]] (Share Surfaces / Code Lifecycle). Reinforces the bulk-contact-referral ask also raised in the 22 Jul touchdown.

---

## 2. Groups and Leagues (Social Layer)

A social component is critical to retention. If a full chat feature is not feasible right now, that is acceptable, but there must be **some social mechanism that lets users compare performance with friends** and drives usage through friendly competition. The recommended approach is **groups or leagues**: friends and people who know each other join a shared group and compete against one another, similar to a fantasy football league.

In addition, offer **influencer-hosted groups**, where trading influencers bring their audiences into the app and those communities compete against each other, with prizes attached. **GameStock** currently operates this model successfully, with **creator-hosted tournaments** serving as a primary acquisition and engagement channel.

**Routed to:** [[third-space]] as feature direction / candidate sub-component(s). Depends on public usernames (item 6). Flagged as a candidate new sub-component (possibly a component) for a focused session, see below.

---

## 3. App Launch Time

Current **cold-start time is nearly 4 seconds**, versus **Kalshi and Polymarket, which each load in 2 seconds or less**. For context, **39% of top-100 apps cold-launch in under 2 seconds and 73% within 3 seconds**; InPlay currently falls outside both bands. Launch time should be treated as a product priority, with a **target of approximately 2 seconds**.

**Routed to:** [[frontend-performance]] as a performance target/requirement.

---

## 4. Streak Experience

A **separate document** outlining the full set of streak-system changes to improve engagement and retention is being prepared. The two core changes:

1. The reward should be a **base multiplier that increases over time**, rather than a flat number of InPlay Dollars.
2. Extending a streak should be a **celebrated moment with meaningful animation**, rather than a plain screen stating that the streak has continued.

Full details to follow in the dedicated streak document.

**Routed to:** [[third-space]] as engagement feature direction / candidate. Flagged: fuller streak-system spec to follow, candidate for its own session/component.

---

## 5. Dynamic Island Presence

When users leave the InPlay app, the app should **maintain a presence in the iPhone's Dynamic Island**, similar to Spotify or Webull. This could display a **live stock price or the InPlay logo**, and **tapping it returns the user directly to the app**. This keeps InPlay visible and one tap away even after the user has moved on.

**Routed to:** captured here only, no clean existing home. **Flagged as a new app-shell / engagement candidate** for the orchestrator to note in components.md cross-cutting. No new component created here.

---

## 6. Public Usernames

Jared does not currently see a place to create a username. If none exists, **every user should be able to create their own public username**, with guardrails: **filtering for vulgar or offensive names** and **protections against impersonating other users or public figures**. Public usernames are **foundational to the social features** in items 2 and 4.

**Routed to:** [[trader-profile]] (public identity, vulgarity filter + impersonation guardrails). Cross-referenced from [[third-space]] as the foundation for Groups & Leagues.

---

## Routing Summary

| Item | Home | Nature |
|------|------|--------|
| 1 Contact-permission invites | [[referral/referral]] | Additive to existing component |
| 2 Groups & Leagues + influencer groups | [[third-space]] | Candidate sub-component / new component, flag |
| 3 Cold-start ~4s → ~2s target | [[frontend-performance]] | New performance target |
| 4 Streak experience | [[third-space]] | Candidate; fuller doc to follow |
| 5 Dynamic Island presence | (this doc) | New app-shell/engagement candidate, flag |
| 6 Public usernames | [[trader-profile]] | Additive; foundational to social |
