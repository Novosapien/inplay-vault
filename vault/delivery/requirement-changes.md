---
description: "Citable register of settled requirements that were later changed, each traced to where it was decided and where it changed, with the change classified so the count is honest."
---

# Requirement change register

> **Delivery:** [[delivery]]
> **Opened:** 2026-08-17, at Brett's request, so the claim that late change has
> been reversal rather than addition can be counted and checked rather than
> asserted.

## Why this exists, and the rule that keeps it honest

The flight plan states that late requirement reversal is the largest single risk
to the launch. That is a serious claim about a client's behaviour, so it needs to
be countable and every entry needs to point at where the original decision was
recorded and where it changed.

**The rule.** Only changes to **requirements that were previously settled and
recorded** appear here. Internal engineering corrections do not, however numerous
they are. For scale: the market-maker decisions log alone carries **60
supersession markers**, and the overwhelming majority are George correcting a
reading of the specification or refining his own earlier note. Counting those
would inflate this register to the point of being useless in a conversation.
Every row below is a **product requirement** that InPlay had settled and then
changed.

## Classification

| Class | Meaning | What it costs |
|-------|---------|--------------|
| **Reversal** | A settled requirement replaced by something incompatible with it | The new work, plus the finished work, plus the tests that proved the old behaviour |
| **Re-reversal** | Changed back toward a position previously abandoned | As above, twice, and the second time nobody trusts the decision |
| **Descope** | Removed entirely | Cheapest of the four. Sunk cost only |
| **Late parameter change** | The requirement stands; the numbers behind it change on a built system | Retune and re-verify. Real, but bounded |
| **Late scope addition** | Genuinely new, not a reversal | The new work only. The honest kind of change |

## The count

| Class | Count |
|-------|------:|
| Reversal | **10** |
| Re-reversal | **1** |
| Descope | **1** |
| Late parameter change | **4** |
| Late scope addition | **4** |
| **Total recorded changes to settled requirements** | **20** |

All twenty fall inside roughly **four weeks**, between 20 July and 17 August, and
the last five days of that window carry six of them. For context, the offering
opens on 22 August and trading starts on 29 August.

---

## Reversals

| # | The requirement | Where it was settled | What it became | Where it changed | Note |
|---|-----------------|---------------------|----------------|------------------|------|
| R1 | **The offering runs as timed rounds**, described as 18 one-minute rounds per day | InPlay's own Requirements v2, carried as E24 in [[ipo-module/ipo-module]] and into the 05-08 flight plan | The window simply opens for a few days. **No rounds at all** | George's review of the 10-08 plan, 12 August | Two documents of InPlay's own disagreed on 10, 16 or 18 rounds before the concept was dropped |
| R2 | **5,000,000 share float per team**, with a 20% holdback | [[ipo-module/ipo-module]], 26-05 component session | 1,000,000 per team on both leagues | [[03-08-2026-touchdown]], Edwin overriding Troy on the call | |
| R3 | **1,000,000 per team on both leagues** | [[03-08-2026-touchdown]] | **900,000 NFL, 1,000,000 NCAA** | George, 12 August; confirmed in the app on 12 August | Changed twice inside ten days |
| R4 | **20% of float held back for shorting**, later a treasury reserve modelled against a $75m cap | [[ipo-module/ipo-module]] 26-05, restated [[03-08-2026-touchdown]] | **The holdback is retired. Treasury does not exist** | Requirements v3, reflected in the app 12 August | The app had to drop a field it had already built |
| R5 | **Subscriptions billed in-app**, accepting the store fee rather than a browser bounce-out | [[research-tab]] changelog, 26-06 component session | **A third-party provider, not app-store billing** | [[29-07-2026-touchdown]] | See R6: this then reversed again |
| R6 | **A third-party payment provider** | [[29-07-2026-touchdown]] | **Native store billing** (Apple IAP and Play Billing) | Build spec dated 07-08, committed 13 August | **Re-reversal.** Back to the 26-06 position after five weeks. Adds two external dependencies that cannot be engineered around |
| R7 | **One onboarding path**: sign up, Persona KYC, trade | [[customer-onboarding/customer-onboarding]], the component as built | **Three account tiers** | [[03-08-2026-touchdown]] | |
| R8 | **Three account tiers** | [[03-08-2026-touchdown]], named 07-08 | **Two tiers built**, the email-only tier does not exist; the third door returns as a competition choice | Built 11 August; [[17-08-2026-touchdown]] | Changed twice inside two weeks |
| R9 | **A confirmation step as a fat-finger guard.** Edwin praised the pre-loaded exit explicitly: _"this is fantastic for teaching how to trade"_ | [[29-07-2026-touchdown]] | **Remove the confirmations. One-click trading** | [[14-08-2026-touchdown]], model in [[one-click-trading-requirements-aug-2026]] | George named the divergence on the call. Both positions are Edwin's, sixteen days apart |
| R10 | **Watch Mode and the Gamecast are the differentiator**, the premium surface, priced at $49.99/mo | [[architecture/open-questions]] 22-07, [[research-tab]] | _"It's less important than you think... it doesn't give you a substantive edge to trade it"_ | [[14-08-2026-touchdown]] | Downgraded by its own strongest advocate |
| R11 | **Programmatic advertising is the always-on inventory**, the backfill that monetises every eyeball-minute direct deals do not own | [[advertising/advertising]] and the [[programmatic-media-playbook]] | _"I'd almost rather have no ad and wait for direct sales than fight those programmatic banners"_ | [[12-08-2026-touchdown]] | The playbook's central assumption is now in question |
| R12 | **In-game price moves on win probability alone.** Edwin was explicit that no own event model was needed: _"you don't have to create it, you just pull Sport Radar's probability in"_ | E15, resolved on the 23-07 MM call, recorded in [[market-maker/open-questions]] | **Probability plus score.** A per-point offset moves the price immediately when the score changes | [[17-08-2026-touchdown]] | Adds a data dependency: the market maker must now consume play-by-play, not just probabilities |
| R13 | **A rich app with many surfaces**, built that way deliberately to carry advertising inventory. Edwin confirmed the reasoning on the call | [[advertising/advertising]], the app as built | **Reduce the surfaces.** Money first, live games, news behind an icon, question whether discover needs to exist | [[17-08-2026-touchdown]] | Edwin was fair about the cause: the rationale was advertising revenue that never arrived |
| R14 | **The testing-the-waters disclosure on most surfaces**, as Edwin's own prototype had it | Edwin's prototype, the 07-08 disclaimer work | **An info button plus the competition-selection screen.** Not every surface | [[17-08-2026-touchdown]], recorded in [[compliance/regulatory-positioning]] | The lightest of the reversals, and it improves the product |

Rows R1 to R14 contain **11 distinct reversals** of settled requirements, one of
which (R6) is a re-reversal, plus two rows (R3 and R8) that are second changes to
requirements already changed once.

## Descope

| # | The requirement | Where it was settled | What happened | Where it changed |
|---|-----------------|---------------------|---------------|------------------|
| D1 | **A load-balancing algorithm alongside the market-making algorithm**, the boundary between them tracked as open question N6 | Raised 17-07, carried in [[market-maker/open-questions]] | **Dropped entirely for season 1.** Deferred to the NBA in October | [[31-07-2026-touchdown]] |

## Late parameter changes

These are not reversals. The requirement stands and the numbers behind it moved,
on a system already built and running. Recorded because they still cost a retune
and a re-verification, and because all four arrived five days before the
offering.

| # | Parameter | Was | Became | Where |
|---|-----------|-----|--------|-------|
| P1 | Maker spread | Built tight, described by Edwin as _"like cement"_ | **8 to 12 ticks** | [[17-08-2026-touchdown]] |
| P2 | Maker resting size | Around 10,000 per level | **500 to 3,000** | [[17-08-2026-touchdown]] |
| P3 | Taker size | SNT-1 v1.0 reference: 5 to 400, median about 30 (30-07). Re-cut to 20/400/20 on 15-08 | **Up to 5,000, crossing multiple price levels** | [[17-08-2026-touchdown]] |
| P4 | Target intra-game price swing | Not previously specified; observed at a couple of dollars | **Roughly $1.50 to $8 per share** | [[17-08-2026-touchdown]] |

## Late scope additions

The honest kind of change: genuinely new, and priced as new work rather than as
rework. Recorded for completeness so the register is not only a list of
grievances.

| # | The addition | Where | Note |
|---|--------------|-------|------|
| A1 | **A desktop execution interface** for the offering, so Edwin can place orders across 170 teams without using the phone app | [[12-08-2026-touchdown]] | Needed before 22 August. It is how the offering gets absorbed at all |
| A2 | **The full one-click trading model**: persistent controls on every page, one-click flatten, order types, hover confirmation | [[14-08-2026-touchdown]], [[one-click-trading-requirements-aug-2026]] | Overlaps R9, which is the reversal half of the same change |
| A3 | **Split the payout leaderboard** so international users do not appear on a cash-prize board they cannot win | Consequence of the 11-08 tier work | **The only hard dated deadline in the engineering record: 27 August** |
| A4 | **Pre-offering indication of interest**, queued orders against a shares-remaining bar | [[31-07-2026-touchdown]] | Scoping owed, never started |

---

## What the register is for

Three things, and none of them is blame.

**To make the claim checkable.** "Most of the recent change has been reversal" is
an assertion. Twenty rows with two citations each is evidence, and it can be
argued with on the specifics rather than the sentiment.

**To price the next one honestly.** When the next change arrives, this is the
reference for what class it falls into and therefore what it costs. A late scope
addition costs the new work. A reversal costs the new work plus the finished work
plus the tests. That is the difference between a day and a week, and it is not
obvious from the outside.

**To be fair about direction versus timing.** Several of these improved the
product. R14 is straightforwardly better. R13 is a sensible response to
advertising revenue that never arrived, and Edwin said as much himself. The
problem this register documents is **not that the decisions were wrong. It is
that they were taken after the work was built**, inside the four weeks before a
launch, by the same two engineers who were simultaneously taking the system
through its first live games.

## Maintaining it

Add a row when a settled requirement changes, with both citations, at the point
it is agreed rather than later. If a change cannot be classified against the table
above, that is usually a sign the original requirement was never actually settled,
which is a different and cheaper problem worth knowing about.
