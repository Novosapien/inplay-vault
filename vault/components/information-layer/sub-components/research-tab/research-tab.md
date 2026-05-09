# InPlay Trading Challenge -- Research Tab

> **Component:** [[information-layer]]
> **Date:** 2026-05-09
> **Status:** Collecting
> **Owner:** George Westbrook
> **Sources:** _[[meetings/08-05-2026-compoent-1]]_

---

## 1. What Does This Sub-Component Do?

**Functional purpose:**

The Research Tab is a planned sub-component for historical analysis and volatility research. It was discussed by Edwin and Cody as a monetisation lever: free during the simulation challenge to get users "conditioned" to rely on it, then subscription-gated in production trading.

Beyond the monetisation intent, almost nothing is defined about what this sub-component actually contains, what the user experience looks like, or what data it surfaces. **This needs a dedicated session before it can be documented.**

**What we know:**

- Free during simulation challenge, subscription-gated in production
- Users get "conditioned" to rely on it during the free challenge, then pay when transitioning to real trading
- Edwin and Cody see this as a key monetisation lever post-challenge
- Likely involves historical annotated charts (past game price movements with event annotations)
- Edwin mentioned it in the context of users being able to "forecast how much the market went down" and "build volatility strategies"
- Cody described it as "inplay research tab" and positioned it as something users would miss when it's no longer free

**What we don't know:**

- What is actually in the Research Tab? What does a user see and do?
- Is it historical charts for completed games? Predictive analytics? Pattern analysis?
- Does it include head-to-head research (which might overlap with Team Page)?
- Does it include Edwin's volatility pattern analysis (how much does a touchdown typically move the price)?
- Is there an InPlay proprietary analysis layer beyond raw data display?
- Is it a standalone page or a feature within Team Page / Single Game Page?
- Does it include any AI/automated analysis, or is it purely data display?
- What's the subscription model in production? Per-month? Per-feature? Tiered?

---

## Sections 2-8

**Not documented.** Insufficient information from existing sessions to define functional requirements, entity journeys, data requirements, or dependencies. These sections will be completed after a dedicated session with Edwin and Cody.

---

## Questions for Next Call

1. Walk us through what a user sees when they open the Research Tab. What's on the screen?
2. What can a user _do_ in the Research Tab? Is it read-only data, or can they interact (run queries, save reports, compare teams)?
3. How does this differ from what's already on the Team Page (historical stats, price chart, matchup data)?
4. Is there any predictive or forward-looking content, or is it purely historical?
5. Edwin mentioned users could "build volatility strategies" -- does the Research Tab provide tools for this, or is it just data that enables it?
6. Is this a separate page in the nav, or a tab/section within existing pages (Team Page, Single Game Page)?
7. What's the production subscription model? Per-month flat fee? Tiered access? Per-feature?
8. Are there any third-party data sources beyond Sport Radar and T0 that would feed into research?
9. Could this overlap with the Education component? (e.g., "here's how to read volatility patterns" could be education or research)
10. Who is the primary persona for this? The Experienced Trader seems obvious, but would the Sports-Passionate Casual use it too?

---

## Sub-Sub-Components

Unknown -- cannot assess decomposition until the scope is defined.
