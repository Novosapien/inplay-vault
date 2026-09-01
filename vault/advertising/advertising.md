---
description: "The advertising section: outbound onboarding artefacts and their blockers, the marketing agency timeline, and the three in-app routes to revenue"
---

# Advertising

> **Vault:** [[index]]
> **Status:** Collecting
> **Date:** 2026-08-12
> **Sources:** [[07-08-2026-touchdown]], Edwin's three reviews of the advertising forecasts (July 2026), [[messaging-house]], [[website-punch-list]]

---

## About This Section

InPlay sells advertising and sponsorship inside The InPlay Challenge 2026. This section holds the three artefacts the Cold Outreach Workforce grounds on, authored 12 August 2026 in a working session with Edwin Johnson and Cody Haugen.

They form a dependency chain. The **offer** says what may be claimed. The **ICPs** say which companies to claim it to, and their tier weights are literally the rubric the workforce grades every lead against. The **buyer personas** say which humans inside those companies the message must land with. None of them is a brochure and no advertiser ever reads one.

**These are not yet loadable into the workforce.** Each document carries its own gaps list. The blocking items are collected below.

## Documents

| Document | Description | Status |
|----------|------------|--------|
| [[offer]] | The factual-claims universe. Seven sections, two component tracks, an honestly empty proof section | Draft v1 |
| [[icps]] | Three tiered ICP definitions. The tier weights are the workforce's lead-grading rubric | Draft v1 |
| [[buyer-personas]] | Six twelve-section personas, two per ICP, weighted to the economic buyer | Draft v1 |

A readable HTML rendering in the InPlay corporate identity lives on the shared drive at `clients/inplay/outbound-campaigns/`, alongside the script that regenerates it from these three files. The markdown here is the source of truth.

## What the session settled

- The offer routes as **media**, with two component tracks: sponsorship, covering title, premium pages and Gamecast field naming, and programmatic, covering the header unit, volatility moments and video interstitials.
- **Title sponsorship is not a separate mechanism.** The process is identical to premium pages, so it is the top scope of the sponsorship track rather than a track of its own.
- **Volatility moments are filled programmatically**, not sold as premium placement. At 20 to 25 a game there is more inventory than direct sales can fill.
- **2,200 games replaces 2,116.** Edwin confirmed the corrected count on 12 August. The old figure is still carried in [[vision]], the decks, the website copy and the media planner, and needs changing in all of them.
- **Betting, daily fantasy, sportsbook and casino are declined outright**, on every path including programmatic. A direct-only carve-out was raised and rejected, because the brand-safety claim is worth more than the revenue.
- **Audience is 18 to 55**, per [[audiences]]. No gender split is claimed in either direction, because none has been observed.
- **No audience number goes in front of an advertiser.** Sponsorship commits an exposure quantity instead, which needs no projection to sell.
- The [[messaging-house]] ban on "guaranteed" and "users" is scoped to prize and investor language. Advertiser-facing copy is exempt.

## Three facts that were in no earlier document

**The simulation multiplier.** The back test, simulation and strategy labs replay and simulate games, so an account holder may run one game many times before watching it live. Edwin's example was twenty simulations of a game before kickoff, giving twenty-one sessions rather than one. Inventory is therefore not bounded by the live-game count. Nothing in the media planner or in the advertising forecasts accounts for this, and it is the strongest claim in the offer. The multiplier itself is unmodelled.

**Title sponsorship reaches outside the app**, into InPlay's own outreach, marketing and landing pages. Nothing in the mechanism produces that and nobody owns it, so agents may not promise it yet.

**The Omnicom position.** The $60M expectation is not happening. The Omnicom and WPP relationships are live and real at $150K for a point of view and $250K to $500K for a full campaign, paused pending audience evidence. Those are two different facts and only the second one is usable.

## Blocking items

Nothing here may be loaded into the workforce until these close. Full per-document gaps lists sit at the foot of [[offer]], [[icps]] and [[buyer-personas]].

| # | Ask | Owner |
|---|-----|-------|
| 1 | The launch inventory map: which surfaces have live ad unit IDs at kickoff, and whether the field brand, volatility moment and video interstitial units exist | Cody |
| 2 | Is Open Measurement integrated, and which verification vendors will be accepted | Cody |
| 3 | The declared refresh interval per unit, and whether the timer starts on viewability | Cody |
| 4 | Definition of an exposure, served, viewable or completed, per format | Edwin and counsel |
| 5 | Whose numbers settle a delivery dispute | Edwin and counsel |
| 6 | Counsel sign-off on the makegood wording | Counsel |
| 7 | The rest of the advertiser category list: crypto, alcohol, cannabis, telehealth, VPN | Edwin |
| 8 | May agents state anything about legality. Default is silence | Edwin and counsel |
| 9 | The internal delivery model, so committed quantities stay inside real inventory | Cody and Novosapien |
| 10 | The simulation multiplier, modelled | Cody and Novosapien |

## The one honest weakness

Every first-person quote in [[buyer-personas]] was written by Novosapien, not captured from a real buyer. InPlay has closed no advertising deals, and Edwin and Cody asked for the personas to be built on assumptions so the session could finish. That is a legitimate starting point and it is stated at the top of the document rather than buried, but those quotes need replacing with real phrasing as soon as real calls happen. It is the one part that cannot be quietly corrected later.


## The marketing agency's timeline (28-08-2026)

Cody set out the agency's plan on the Friday touchdown. They are already in
TestFlight, and **reviewing the app and onboarding experience is explicitly part
of their scope**, not an extra.

| When | What happens |
|---|---|
| **Weeks 1 to 2** | Discovery. Reviewing the app and the onboarding experience, feeding back suggestions from a marketer's point of view |
| **Week 3** | **First ad tests.** Hooks and language only, **no graphics**, small spend, testing what resonates. Edwin's framing: _"even on their little $200 a day stuff"_ |
| **Weeks 3 to 4** | A spreadsheet of **suggested spend**, based on what the research found |
| **Week 5** | **The first real campaign** |

**Two things follow from this that matter more than the dates.**

**First, week three is the real deadline for onboarding, not Saturday.** Edwin
made the link himself: _"if we're spending money on advertising, we've got to
have people be able to sign up and not do the KYC."_ The buying-power gap found
on 28 August (see [[customer-onboarding/customer-onboarding]]) has to be
dependable before paid traffic arrives, not merely before the first game.

**Second, an access blocker is outstanding.** Brett asked Cody to chase the
agency for logins so they can be added to **tag manager, analytics and
Firebase**. Without those they cannot instrument anything they are about to
test, and Sebastian has not responded. Cody agreed to ping him.

_Source: [[28-08-2026-touchdown]]._

---

## ⭐ The three in-app revenue routes, and what is ready (01-09-2026)

Cody named them on the Monday touchdown, under open commercial pressure:
*"everyone from the team is stressed like right now we have three three options
towards towards revenue."* Inside the app, there are exactly three:

| # | Route | State on 1 September | Who decides next |
|---|---|---|---|
| 1 | **Programmatic ads on the pages** | ✅ **Configured and running.** Not optimised. Can be switched on immediately | InPlay say when |
| 2 | **Video ads over the field player and gamecast tracker** | ✅ **Built and verified.** Needs a short test pass before it goes live | Novosapien to test, then InPlay |
| 3 | **Subscriptions and packages** | 🔴 **Not scoped.** Needs a requirement session, booked for 2 September | Joint session |

Brett's exact words on the first two: *"we can be quick if you guys are happy we
just turn the ads on. We can turn them on because it's all configured
programmatics running. It's not optimized, but it's running. So, at least you can
start getting some revenues there."* And on the video: *"we've got it built out.
It's been verified. We need to get that in and just do run a couple of tests
first."*

⚠ **The decision on route 1 sits with InPlay and nothing is blocking it.** This
is worth stating plainly, because the ad stack was removed from the app build on
17 August and the removal was recorded as reversible. Switching it back on is a
choice, not a piece of work.

**Why the timing is this week rather than next quarter.** Paid advertising is
starting outside the Viral App Launch relationship, and Cody expects the traffic
to compound: *"you add that on the cascade that NFL IPOs and NFL regular season
are around the corner. This next weekend of college football is first real
games... we need to be able to monetize the users coming in."*

**Subscription scope belongs to the Research Tab**, where the tier ladder already
lives. It is recorded in
[[information-layer/sub-components/research-tab/research-tab]] rather than here,
because it is a product build with an App Store review attached, not an ad
placement.

_Source: [[01-09-2026-touchdown]]._
