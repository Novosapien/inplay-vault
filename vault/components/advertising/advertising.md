---
description: "Hub for advertising as a cross-cutting concern — the two revenue motions, direct-sold sponsorship vs programmatic SSP inventory, and its sub-component index"
---

# InPlay Trading Challenge — Advertising

> **Vision:** [[vision]]
> **Type:** Cross-cutting concern (not a standalone product component)
> **Date:** 2026-06-18
> **Status:** Collecting
> **Owner:** Edwin + Skye (commercial) + Brett (ad-tech / programmatic) + Max (creative units)
> **ID registry:** [[ad-network-ids]] is the central place for all ad-network account IDs, publisher IDs, app IDs, and ad-unit IDs (AdMob captured; SSP IDs added as issued).
> **Sources:** _[[meetings/22-05-2026-Advertising-first-meeting]], [[meetings/17-06-2026-touchdown]], [[27-07-2026-touchdown]], [[29-07-2026-touchdown]], [[31-07-2026-touchdown]], [[03-08-2026-touchdown]], [[07-08-2026-touchdown]]_
> **Updated:** 2026-08-10 — AdMob live and serving, SSP ladder set (AdMob + AppLovin MAX + one more, capped at three), Kochava chosen as MMP, rewarded-video unit proposed, and ad inventory now has to be gated by user tier.

---

## What This Is

Advertising is how InPlay monetises its inventory. It is a **cross-cutting concern**, not a screen or a flow: ad surfaces overlay the websites, the information layer, trading, referral, third space, and education. The canonical description of the commercial model (sponsorship territories, engagement-minute billing, packaging tiers, sales motion) lives in the **Advertising section of [[components/components#Cross-Cutting Concerns]]**. This directory exists to hold the **buildable sub-components** of the ad business as they get scoped.

There are two complementary revenue motions:

1. **Direct-sold sponsorships** — single-brand, season-long ownership of specific surfaces ("the trading challenge presented by [brand]"), sold by Skye's team. Served on day one as house ads/campaigns inside the mediator, and in **phase 2 via Kevel** for moment-based triggers (a brand owning touchdowns for a team). Rich, custom units; not standard IAB inventory.
2. **Programmatic / generalised inventory** — the rolling in-content ad units (banner, interstitial, native, video) filled by an **SSP portfolio** through an in-app auction. This is the always-on backfill that monetises every eyeball-minute the direct deals do not own. The operating model for this is the **[[sub-components/programmatic-media-playbook/programmatic-media-playbook]]**.

## Sub-Components

| Sub-Component | Overview | Status | Link |
|--------------|----------|--------|------|
| Programmatic Media Playbook | The SSP roster, the AppLovin MAX architecture, and the 1-human + AI-agent ad-ops operating model for the programmatic/generalised inventory | Reference | [[sub-components/programmatic-media-playbook/programmatic-media-playbook]] |
| AdMob Account & Ad Units | The live AdMob account (publisher ID, App IDs, app review status) and all 8 production ad-unit IDs, iOS + Android | Reference | [[admob-account]] |
| Unity LevelPlay Account | The LevelPlay SSP account: app keys per platform, ironSource platform IDs, registered store apps, ad units to follow | Reference | [[unity-levelplay-account]] |
| Vungle Account | The Vungle (Liftoff Monetize) SSP account: account ID, Android app ID, registered store apps, ad units to follow | Reference | [[vungle-account]] |

> **Note (18 June 2026):** Advertising was promoted from a pure cross-cutting note into this directory so the **programmatic media playbook** (Brett, 17-06) could be captured as a buildable sub-component. The specialist-sponsorship-territory detail still lives in [[components/components#Cross-Cutting Concerns]] and is the next candidate to extract into its own sub-component here.

---

## Update (27-07 → 07-08 touchdowns): AdMob live, and the SSP ladder

**AdMob is verified and serving.** Verification landed the morning of 27-07,
the first ad unit (native) was created, and by 31-07 there was a working
**ads lab page** inside the app showing every unit type against example
creative from the catalogue. Units click through to the advertiser's site and
back. Details in [[admob-account]].

**Why AdMob first, and the resubmission tax.** Every SSP integration requires
embedding serving code that is outside InPlay's control, plus a policy update,
which means **an app-store resubmission each time** — 24 to 48 hours, with the
app staying live and the new version swapped in. And an SSP can only be applied
for **once you have an app-store URL**, so it is chicken-and-egg. AdMob was
chosen because it turned around in 48 hours where the others take weeks and
want written submissions. Brett's sequencing: get AdMob in, prove it serves,
run test ads, then work the rest of the administration in parallel and
resubmit as each lands.

**The SSP ladder** _(Brett, 31-07)_:

| Network | Role | Status |
|---------|------|--------|
| **AdMob** | The volume. Majority of served impressions | ✅ Live |
| **AppLovin MAX** | Second network, minimum viable portfolio | 🟡 Two weeks chasing sign-on; warm intro being sought via Rich Ballance's son (Kevin) |
| **One more, TBD** | Third network within roughly a month | 🔴 Likely **Smart** (Brett's former boss is now their VP); trial applications to three others went unanswered ~two months ago |

**Cap of three in the first three months.** Beyond that it gets complicated
without a proportionate return. Brett on the category: _"these exchanges are
really, really, really, really slow"_ and the premium ones are fussy about
volume.

**Warning for the test period:** nobody may click the ads. It spikes CTR,
AdMob reads it as fraud, and the account gets banned. Standing instruction
while test units are live.

## Update (17-08): no advertisers, and the one format Edwin actually wants

**The commercial position, stated plainly.** No advertisers have signed. Edwin's
assessment of why the whole plan is where it is: the advertising revenue that
justified building at this pace _"at best was totally misunderstood, at worst it
was duplicitous information"_, and he is _"pretty furious about it"_. He also
named the consequence for outbound: getting users is hard to justify when there
is nothing to monetise them with, and _"the more people that sign up is the more
people I have to pay"_.

One relationship illustrates the problem better than any figure: InPlay has a
billionaire investor who owns a candy company, and the candy company will not
advertise.

**The programmatic creative got worse, not better.** Edwin's second look
produced plus-sized clothing models on his feed, which he attributed drily to
his own search history. It reinforces rather than changes the 12-08 position:
run it open to gather data, then tighten.

**The one format he has asked for rather than tolerated.** Video advertising
**over the field during breaks in play**: timeouts, television timeouts,
injuries, end of quarter, pre-game and post-game, with the buy and sell controls
still live underneath. He raised it himself, having floated it a couple of months
ago. It works because it **occupies dead time instead of competing with the
game**, which is the exact objection he had to in-content banners. If any
advertising format is worth designing properly for this product, it is this one.

⚠ **A structural note worth carrying.** Edwin was fair about how the app came to
have so many surfaces: it was built with plenty of them precisely because the
plan assumed advertising inventory needing places to live. With no advertisers,
that rationale has gone, and the surfaces became cost without benefit. The
17-08 surface reduction is the direct consequence. See
[[information-layer/sub-components/discovery-home/discovery-home]].

_Source: [[17-08-2026-touchdown]]._

## Update (12-08): serving in the store build, and Edwin does not like what he sees

**Where the units are.** The AdMob units are **live in the App Store build**,
curated, with age verification applied. They are **deliberately switched off in
TestFlight** so nobody on the team can click one by accident. Brett's reason is
worth repeating because the risk is existential rather than theoretical: every
SSP platform warns that a click-through rate above their threshold means an
instant ban, and it has taken months to get these networks to acknowledge,
verify and onboard. Further Google-ecosystem verifications arrived and are due
by September.

**The tuning trade-off, discovered by doing it.** Tightening the constraints on
what may serve drops the fill rate sharply and the platform warns you as it
happens. The decision taken was to **run relatively open for now and gather
data**, then tighten once there is evidence about what is actually coming
through.

**Edwin's reaction to the creative was blunt.** _"That ad looks horrible."_ He
found the in-content placement distracting enough that it would put him off the
app: _"in the belly of the context, it's very distracting and it would piss me
off. It would actually turn me off."_ Agreed direction: move to a **top or
bottom unit**, video only, rather than in-content banners. Brett: cheap to
change.

**A direct-sales route is opening.** A **former FIFA commercial lawyer**, just
finished representing FIFA on commercial deals, has approached Edwin and wants
to represent InPlay for brand deals. He is coming in inexpensively and named
contacts. Contract under review with counsel. Edwin's position, stated plainly:
_"I'd almost rather have no ad and wait for direct sales than fight those
programmatic banners."_

**The agreed compromise:** float programmatic in enough volume to test, measure
and check quality, then decide whether to increase it or pull it back. It is a
dial, not a switch, and the data has to come first. Note the tension with
[[sub-components/programmatic-media-playbook/programmatic-media-playbook]],
which assumes programmatic carries the always-on inventory: if direct sales
succeed, that model needs revisiting rather than quietly persisting.

⚠ **The volatility-moment unit cannot be programmatic.** Brett: a custom unit of
that shape is too difficult to slot into a programmatic auction, so it will have
to be a **direct buy**. That has been an open assumption in the packaging model
and is now settled.

_Source: [[12-08-2026-touchdown]]._

## Update (07-08): rewarded video for InPlay dollars

Edwin's UI prototype includes a **rewarded ad unit**: watch 30 seconds, earn
**100 InPlay dollars**, positioned at the bottom of the home surface as a
recovery mechanic — _"it's great because if you end up having a bad day, you
can go to that."_ This is the first ad format in the product with a **direct
economic exchange to the user**, and it overlaps the education reward mechanic
in [[education/education]] (100 InPlay coins on module completion). Not yet
scoped. _Source: [[07-08-2026-touchdown]]._

## ⚠ Constraint (03-08): ad inventory must be gated by user tier

With the [[customer-onboarding/customer-onboarding|three-tier onboarding
model]], a large share of users will be **not signed in or not KYC'd**, and
therefore possibly under 18. Those users may only be served **under-18-safe
inventory** — no alcohol, no gambling adjacency (George, 03-08). How that is
actually enforced per network is open (G4 in
[[compliance/eligibility-and-age-gating]]).

Brett's related warning (29-07) is the commercial half of the same problem: ad
serving wants identity. A not-logged-in user still generates an impression that
has to be served, tracked and pushed through the MMP, even if all they see is a
house banner pushing them toward KYC. _"You don't want to go, well, if you're
not logged in you're not going to get an ad served to you."_ See
[[customer-onboarding/customer-onboarding]] for the full note.

## Update (29-07): MMP direction — Kochava

**Kochava is the direction**, over AppsFlyer, following Brett's comparison
research. It is roughly **a fifth to a tenth of the price** and carries
everything else needed.

**The one gap:** Kochava has **no direct AdMob integration**, which matters
because AdMob is the network that is already live. Brett's read is that a
workaround is viable — _"it's a big gap, but it's a gap that's doable"_ — and
that a call with Kochava should establish the integration effort before
committing. His framing: _"it's a cheap option. I don't think you should be
going Rolls-Royce on this."_

**Commercial angle:** Jason at **Plexus Media** (the prospective marketing
agency) has a direct relationship with Kochava and is confident of beating
their standard rates, which are already good. Cody and Edwin took the
commercials up with him directly.

Supersedes the open AppsFlyer-vs-Kochava question from 24-07. Recorded as an
integration in [[integrations]]. _Source: [[29-07-2026-touchdown]]._
