---
description: "Delivery hub for the InPlay app flight plan, the Novosapien/InPlay working agreement, with committed snapshots, structure conventions and key launch dates"
---

# Delivery · InPlay App Flight Plan

> **Status:** Living · updated per working session
> **Owner:** Novosapien (product owner: Brett StClair)
> **Live copy:** `shared/clients/inplay/flight-plans/inplay-app-flight-plan-{date}-{HHMM}.html` (a new timestamped file per build; prior versions stay as the audit trail)
> **Master:** `Programming/inplay/inplay-app-flight-plan/` (source + build script)
> **Companion:** [[requirement-changes|Requirement change register]], the citable record of settled requirements later changed
> **Internal only:** [[commercial-open-items|Commercial open items]], money promised in conversation with no written instrument behind it. Never goes in the flight plan
> **Latest change list:** [[change-requests-2026-08-18]], the 22 app requests received on 18 August, classified
> **Last rehearsal:** [[friends-and-family-2026-08-21]], the overnight session before the offering

The flight plan is the delivery working agreement between Novosapien and InPlay: what has shipped, what is committed, what capacity exists, and the live risks into each launch. It is produced with the `/novosapien-product-owner` skill from three reconciled sources: the build repositories, the partnership proposal, and this vault. This section holds the committed snapshots; each weekly review runs off the newest one.

## Snapshots

| Date | File | Headline state |
|------|------|----------------|
| 2026-09-02 (v2) | [flight-plans/2026-09-02-inplay-app-flight-plan.html](flight-plans/2026-09-02-inplay-app-flight-plan.html) | **The delivery wave splits into committed versus additional, and the two curves are almost the same shape.** Repos classified against the proposal: **committed** is the app, trading service, FIX gateway, Sportradar service and the onboarding and referral service; **additional** is the market maker and taker, the operations panel, the admin panel and API, the global and challenge websites, the CMS, media planner, presentation engine and teaser. The vault is excluded, since it records the work rather than being it. Totals: **1,640 committed changes against 802 additional**, so additional is **32.8%** of everything built. The finding: **51.4% of committed work and 50.9% of additional work both landed in the month before the offering.** The extra third of the programme was not spread into the quiet weeks of May and June, it piled into the same four weeks. Peak week beginning 10 August carried **322 committed plus 194 additional**. New prose makes the point that this is what 228% actually cost and where it was paid. Chart now draws stacked (committed at the base, additional riding on top) with the milestone labels **staggered onto three rows below the week labels**, each with its own connector, fixing the overlap that made them unreadable. Verified programmatically: no label collisions and nothing clips the viewBox |
| 2026-09-02 (late) | [flight-plans/2026-09-02-inplay-app-flight-plan.html](flight-plans/2026-09-02-inplay-app-flight-plan.html) | **New on Home, under the scorecard: a delivery wave showing when the work actually happened**, built from real commit data rather than assertion. Weekly non-merge commits across all 20 repositories, deduplicated, 6 May to 2 September, drawn as two waves (everything, and the mobile app) with a cumulative-share line and the critical month shaded. **It confirms the hypothesis and by more than expected: 51.9% of every engineering change in the programme landed in the single month before the offering** (22 Jul to 22 Aug), against 41.6% across the eleven weeks before it. **31.0% landed in the final fortnight, 13.9% in the final week alone.** The four busiest days in four months are 12, 13, 14 and 15 August, the live game nights. One week beginning 10 August carried **557 changes, a fifth of the whole programme**. App-only is less extreme but still heavy at 42.6% in the final month. The accompanying note separates the two causes deliberately: **discovery**, which is healthy and is what the three live nights were for, and **late requirement change**, which is the expensive half, with thirty settled requirements changing between 11 and 19 August. **The graph is now the argument for the NFL build freeze**, and it is why the two remaining items are logged for after the launch rather than squeezed in before it. Chart generator lives in `build.py` as `wave_svg()` with the weekly series embedded, so it regenerates rather than being redrawn |
| 2026-09-02 (evening) | [flight-plans/2026-09-02-inplay-app-flight-plan.html](flight-plans/2026-09-02-inplay-app-flight-plan.html) | **The two open items become committed post-NFL work rather than open defects.** Per Brett, and recorded as **agreed with InPlay**: the team reference-data sweep and the referral top-up threshold retirement are both **logged, sized and scheduled for the first working week after the NFL launch**. Neither affects trading, neither affects the offering, and neither holds the 5 September window, so the build definition stays frozen through the offering and the 7 September secondary open. Both move from "open, not started" to **Committed** and take **Q1 P1 slots S3 and S4**, so the commitment sits in the pipeline rather than in a backlog. The reference-data risk re-scores from Certain to Known, with the mitigation now agreed rather than proposed: one sweep of all 170 teams across the three places team identity is written, not twenty-two individual fixes. The Key Releases table is retitled "Logged for delivery after the NFL launch" and carries a note explaining why the two are shown at all: a plan that shows only green stops being useful the moment something genuinely slips. ⚠ **No citation exists in the meeting record for the InPlay agreement**; it is recorded on Brett's instruction and should be confirmed on the next call so the register carries a source |
| 2026-09-02 (pm) | [flight-plans/2026-09-02-inplay-app-flight-plan.html](flight-plans/2026-09-02-inplay-app-flight-plan.html) | **Two open defects added with verified status, both checked against the shipped code including unmerged branches and working copies.** ⚠ **Team reference data**: Jared's full list is 22 corrections across 21 teams, not the four captured on 28-08. Fourteen abbreviations, six colours in the wrong family, Notre Dame still in the ACC, and the BAMA label overflowing. **Nothing addresses any of them on any branch**, so the row reads open and not started, with the recommendation to sweep all 170 teams across the three places team identity is written rather than fix the reported 22. 🔴 **Referral top-up**: the 18 August decision (P6, any time while flat, instant, up to 100,000) is unbuilt. `RELOAD_THRESHOLD = 25_000` is still in two app files, and the deeper gap is cadence, since the 12 August mechanism runs end-of-day rather than instantly. Both appear on Key Releases under a new "Open defects, verified against the shipped code" table, on the module ledger against their components, and reference data enters the risk register at 9 as a credibility risk. Home reworded so the plan no longer claims the only open items are InPlay's |
| 2026-09-02 | [flight-plans/2026-09-02-inplay-app-flight-plan.html](flight-plans/2026-09-02-inplay-app-flight-plan.html) | **The launch board is clear, and the numbers move to 228% on 94%.** Every Novosapien delivery item carried into the first live game weekend is closed, so the board shows **95 green, 16 amber, none red**, and the amber is InPlay decisions or the advertising workstream parked by InPlay's own 17 August call. Four closures drive it: **buying power now provisions itself** (venue account at signup, role at verification, corridor holds for buying power, wallet balance refused as venue funds), the **reference pricing model** is built so a share holds the value the result gave it, the **win-probability feed and NCAA run together on the production worker** which retires the last supplier dependency, and **play-by-play rides the live stream** with the polled route as fallback. Also closed: a refused short names its real reason and reads as a sell, group joins open to any signed-in account, and the order verdict is fetched when a push never arrives. Delivered count **39 to 41**, additional-beyond-proposal **18 to 20**. Risk register retires three (accounts that cannot trade, the end-of-game snap-back, the Sportradar futures endpoint) and re-scores late requirement reversal down from high, because the client withdrew one ask himself and accepted the team's answer on another. **The NFL structure is now a decision risk rather than a build risk**, with the NCAA structure named as a working fallback. Must-land restructured so InPlay decisions are held separately from delivery |
| 2026-08-28 | [flight-plans/2026-08-28-inplay-app-flight-plan.html](flight-plans/2026-08-28-inplay-app-flight-plan.html) | **The market is open, and the plan now leads with delivered-versus-planned.** New headline card on Home carrying two bars against the July proposal and nothing else: **217% of the committed launch scope delivered** (39 deliverables against the 18 the proposal named), on **90% of the planned time** (day 114 of 126, 6 May to the 9 September kickoff), a rate of roughly **2.4×**. The count is shown in full on the Module Ledger so it can be argued with on specifics: 17 of 18 committed items delivered, 4 of the 6 the proposal deferred pulled forward, and 18 built that appear in no proposal. Records the **NCAA secondary open on 27 August 09:30 ET** and the **first live college game weekend**. Two new client-facing notes, deliberately placed below the fold: **Novosapien moves to best effort on the core platform**, with the five things that means spelled out; and **there is no support cover in place**, with the support and SLA programme (submitted 3 Aug) and the three education guides logged as delivered and awaiting InPlay's decision. Risk register re-scored: four retired (market maker missing the open, tZERO production readiness, launch load spikes, built-but-switched-off), and **the NFL holding-structure rebuild enters at number one** with the fallback named. Countdown re-anchored to the NFL offering |
| 2026-08-18 | [flight-plans/2026-08-18-inplay-app-flight-plan.html](flight-plans/2026-08-18-inplay-app-flight-plan.html) | **The overnight release and the 18 August change list.** Thirteen changes shipped between 13:00 on the 17th and 01:00 on the 18th across seven repositories, including the removal of the ad stack from the app and Discover becoming one Markets board. Advertising is off in the TestFlight build and reversible; the agreed replacement is an in-break video over the game tracker, unit at AdMob for verification. The board re-scored to 45 done, 29 in flight, 4 blocked. Market maker and taker both closed as delivered, and the taker added to the module ledger as an 18th component. A further **22 change requests arrived on 18 August**, the day after the freeze: seven change a settled requirement, two are venue rules rather than app choices. Held in [[change-requests-2026-08-18]] |
| 2026-08-17 (pm) | [flight-plans/2026-08-17-inplay-app-flight-plan.html](flight-plans/2026-08-17-inplay-app-flight-plan.html) | **The reversal claim is now counted and cited.** New [[requirement-changes\|requirement change register]]: 20 changes to settled requirements between 20 Jul and 17 Aug, each traced to where it was decided and where it changed. **11 reversals** (one a re-reversal), 1 descope, 4 late parameter changes, 4 genuine additions. Six fall in the last five days. Internal engineering corrections excluded deliberately, since the market-maker log alone carries 60 supersessions and counting those would make the figure meaningless. The Home note now carries the ten-row evidence table |
| 2026-08-17 | [flight-plans/2026-08-17-inplay-app-flight-plan.html](flight-plans/2026-08-17-inplay-app-flight-plan.html) | **Late requirement reversal enters the risk register at number one**, with a highlighted note on the Home page: the recent pattern has been reversal rather than addition, which costs the new work plus the finished work plus the tests that proved the old behaviour, and it landed in the same week the engines first met real games. Build definition frozen from 17 Aug. **Also built from the week's engineering work log.** Two live NFL preseason nights ran on **13 and 15 Aug**, not the 13/20/27 sequence the plan carried, and running them two days apart is why the fixes could be trusted. The market maker took a **six-part numbered fix programme** (keeps opening price across restart, refuses to cross a live market, self-repairs orders at boot, ~28x faster venue processing); the data feed took six publisher corrections and learned to find live games itself; four permanent-wrong states removed at the venue layer; **both front ends stopped inventing data**, which is the root of Jared's price-versus-book complaint. **One outage:** a disk filled on 15 Aug and the venue connection was lost for 1h40m, cause closed. **New structural finding:** the market maker starved the retail order feed twice. **New risk band: built but switched off**, covering synthetic market orders, the app's week of fixes, the data service's corrections and the engine's boot self-repair. The **20 Aug** rehearsal is now the go or no-go point; **27 Aug** is a hard deadline, not a rehearsal |
| 2026-08-13 | [flight-plans/2026-08-13-inplay-app-flight-plan.html](flight-plans/2026-08-13-inplay-app-flight-plan.html) | **Version 1.1 submitted to Apple on 12 Aug, waiting for review**, with the privacy blockers cleared, the store listing and reviewer notes rewritten and the age rating updated. A matching 1.1 build went to TestFlight, so external testers need Beta App Review first. The release backlog that dominated the 12 Aug plan is promoted and gone. **IPO windows now fixed to the minute** (NCAA 22 Aug 1:00pm to 26 Aug 10:00pm ET, secondary 27 Aug 9:30am; NFL 5 to 6 Sep, secondary 7 Sep), which closes E25. **Treasury holdback retired.** Referral Bank top-up built and deployed. New risk: a spec recommends **subscriptions through native store billing**, reversing the outside-provider assumption, and raising the classification question of what a subscription may sell |
| 2026-08-12 (pm) | [flight-plans/2026-08-12-inplay-app-flight-plan.html](flight-plans/2026-08-12-inplay-app-flight-plan.html) | **Full branch sweep across all 20 repositories, plus a new outbound-campaign band.** Headline: **276 finished commits sit off the main line**, 188 in the app alone, so the constraint is release, not build. Adds the **onboarding/KYC/referral service**, absent from every prior ledger. Corrects the tiers: **two are built** (US `trader`, international `trader-lite`), the email-only tier is **not**, and the tZERO date-of-birth blocker was solved by choosing a Persona template that captures DOB. New dated item: **split the payout leaderboard before 27 Aug**, since international users can now trade and therefore reach the cash board. 5x referral window ends **22 Aug**, not month end |
| 2026-08-12 | [flight-plans/2026-08-12-inplay-app-flight-plan.html](flight-plans/2026-08-12-inplay-app-flight-plan.html) | **Correction pass after George's review.** tZERO tickers and the maker/taker wallets already existed (they were listed as the top blocker); share counts corrected to **900k NFL / 1M NCAA**; **NFL IPO has no rounds**; tax forms moved to 5 Sep; the 200ms figure restated as the market maker's quote rhythm (200 to 500ms in play), not trade speed; **seven infrastructure tasks removed** as they came from internal drafts rather than agreed work; NBA downgraded to P3; research promoted to P1; App Store submission added as blocked on three must-fix items per Hassan's 11 Aug readiness report; new table showing every InPlay ask and its slot |
| 2026-08-10 | [flight-plans/2026-08-10-inplay-app-flight-plan.html](flight-plans/2026-08-10-inplay-app-flight-plan.html) | 12 days to the NCAA IPO. Now also folds in the 31-07 **Website Punch List 1** and **Messaging House v2.0**. Adds a live **countdown** to the IPO on every page, a **Countdown Board** (one cross-team must-land list: engine room, the three live-game proving runs on 13, 20 and 27 Aug, advertising on AdMob alone because AppLovin MAX has not responded, tax forms and payouts, identity and compliance, the scale ramp, and go to market), a **Backlog** page (60 items in three bands, sized and confidence-rated), and a **deliverable-bearing critical timeline** where every date states what must be finished by it. Evidence refreshed from all 21 repos |
| 2026-08-05 | [flight-plans/2026-08-05-inplay-app-flight-plan.html](flight-plans/2026-08-05-inplay-app-flight-plan.html) | 17 days to the NCAA IPO; launch mode active; trading path is the long pole |

## The Countdown Board (added 2026-08-10)

The flight plan now opens with a **live countdown to the NCAA IPO** (22 Aug,
1:00pm ET) on every page, and carries a **Countdown Board**: the single
cross-team list of everything that must land before it, grouped into seven
bands with an owner, a due date and a definition of done on every row.

1. **The trading engine room**: tickers, the two MPIDs, market maker complete
   and tested, market taker complete and tested, the offering engine.
2. **The three live-game proving runs**: 13, 20 and 27 Aug, each with what it
   proves. Deliberately three, not one: run 1 proves the wiring, run 2 proves
   concurrency with the market maker quoting, run 3 is the unattended dress
   rehearsal before real users trade on 29 Aug.
3. **Advertising and revenue**: live ads serve from AdMob **through the AppLovin
   MAX ad-serving layer**, across all ad units. AppLovin have not responded
   commercially despite repeated chasers, so their demand is not in the auction
   yet, which costs yield rather than function. The units ride the next App
   Store push; the **rewarded interstitial** has configuration issues and goes
   on the push after.
4. **Money out**: the Avalara W-9 embed, and the still-unresolved payment
   processor.
5. **Identity, eligibility and compliance**: the three trader tiers, tZERO's
   18+ date-of-birth block, the language sweep.
6. **Scale ramp**: the VMs. Measured, not guessed: the market maker journal
   sustains ~579 events/s against ~2,100 needed, so group commit is now
   required; Centrifugo (an e2-small) fans every tick to every user and its
   connection limit has never been measured.
7. **Go to market**: agency, referral multiplier, influencer analysts, campus,
   tailgate activations and PR, each with what delivery needs from it. Every
   campaign date is an infrastructure date.
9. **Outbound campaign**: the Cold Outreach Workforce that sells ad inventory to
   brands and agencies, distinct from the consumer go-to-market in band 7.
   Foundations (offer, ICPs, buyer personas) are authored and blocked on four
   InPlay answers; mailbox warming is under way but **the warmed-mailbox and
   LinkedIn list is not recorded anywhere** and is owed; then configure, launch
   ~1 Sep, measurement ~1 week later, first meaningful reporting ~1 week after
   that.
8. **Website and brand**: the remainder of **Website Punch List 1 v1.3** (the P2
   items travelling with the counsel package, the P3 pre-kickoff close-out, and
   the Insights section that must exist before Founder Memo No. 1), plus
   applying the **Messaging House v2.0** lexicon to the app, which has never
   been swept against it. Both documents are Edwin's, dated 31-07, and live in
   `shared/clients/inplay/outbound-campaigns/`. See [[compliance/compliance]].

## Two workstreams loaded into Q2 to Q4 (Brett, 12-08-2026)

Split deliberately, because they have different risk profiles and different
owners of the unknowns.

**InPlay Analyst.** Analyst reviews on team companies, from recruited human
analysts and from generated ones. Sequenced: the rating standard and its
compliance read (Q2 small), publication and attribution on top of the Q1
submission portal (Q2 medium), generated analysts with a review gate before
publication (Q3 large), track-record scoring of past calls against what the
price did (Q3 medium), alerts and a weekly digest (Q4 small).

⚠ The rating standard carries a **counsel gate**. A target price on a
securities-adjacent product sits close to investment advice, and the Messaging
House forbids performance promises. Settle the wording before anything is built
on it. See [[compliance/compliance]].

**Forecast, the AI playbooks.** A trader describes a playbook by typing or
speaking, the app generates it, and it runs against past games to show how it
would have performed. Sequenced: the historical price and event foundation plus
the database work (Q2 large, and the expensive substrate everything waits on),
the product shape and paywall decision (Q2 small), a voice-input research spike
(Q2 P2), the playbook builder (Q3 large), the backtest engine (Q3 large, which
absorbs the back-test lab Edwin prototyped in August), the learning layer (Q4
large, last because it needs a season of real prices), and playbooks running
live rather than only backwards (Q4 medium).

Q3 and Q4 entries are **loaded, not committed**: they firm at the respective
quarter reloads, per the year-ahead rule that commitments two quarters out are
fantasy.

**Outbound campaign dates pulled forward a week (Brett, 12-08).** Configure the
system Thursday **20 August**, campaign opens Tuesday **25 August**, measurement
in place ~**1 September**, first meaningful reporting ~**8 September**. Domain
authentication moves to the 20th and warming to the 25th to match. The upside is
that the first advertiser conversations happen while the market is live rather
than weeks after it opens. The exposure is that **mailbox warming cannot be
compressed by effort**: if it is not far enough along by the 25th, the honest
move is to open at lower volume rather than send anyway and spend the domain
reputation.

## 1 September: the app is locked out, and the tooling that would find it is switched off

A thirty-minute Monday touchdown, two days before the first week of college
football. Present: Cody, Troy, Jared, Kevin, Max (InPlay) and Brett, George,
Hasan, Lily (Novosapien). Edwin was absent. It ended early on purpose: Troy
cancelled the tZERO call that followed so the engineers could go and work the
outage.

**Two things dominate the week and they compound each other.**

### The app is locked out and nobody knows why

Jared was dropped mid-call. Cody had it from outside the team as well: *"I had a
few buddies text me this morning saying they were locked out. They can't retrieve
a password or a code. It's not sent to their email."* Both of them reproduced it.

The second half is the serious half. **Returning login fails, and the recovery
path fails with it**, so a locked-out user cannot get back in unaided. No cause
was identified on the call and nobody pretended otherwise. Brett named the
candidates and stopped: *"It could be a link to persona. It could be
authentication. It could be anything."* The live record is in
[[architecture/services/auth-service]].

The date is what makes it urgent. Cody: *"we have two really two days till more
trading happens, live games happen. Thursday is when week one kicks off and
they're both ranked games."* Troy added that the app is taking unprompted traffic
even off game days.

### The Claude account is suspended over an unpaid bill

This is the item that turns a bad morning into a slow week, and it is worth
recording exactly as it was said. Brett: *"we're just on manual mode at the
moment because our clause billing accounts have been suspended... it's going to
take us a little bit longer."*

The number and the ownership: *"I need to pay the Claude bill which is on our
side. It's our cost, but it is sitting at about $49,000, which I don't have a
spare $49,000 just to find to pay."* He is waiting on Edwin over payment.

**What it costs in delivery terms, in George's words:** *"usually it's say 10
people that would be doing it. Obviously, it's two to four of us with AI. So
there's going to be a bit more time on that now without the AI."* And,
unprompted: *"Feels like going back to stone tools."*

⚠ **Two things to keep separate.** The suspension did not cause the lockout. But
every step of finding the cause, and every fix after it, now runs at hand-coded
speed on a team sized for AI-assisted speed, in the week the first live college
games arrive. That is the delivery risk, and it is the honest headline for the
week.

### The commercial position: three routes to revenue, two of them ready

Cody put the pressure on the table without dressing it up: *"everyone from the
team is stressed like right now we have three three options towards revenue."*
Inside the app they are programmatic ads, video ads over the field player, and
subscriptions. **The first two are ready and the decision sits with InPlay:**
programmatic is configured and running, unoptimised but live, and the video unit
is built and verified pending a short test pass. Subscriptions need a
requirement session, booked for 2 September. Full record in
[[advertising/advertising]] and
[[information-layer/sub-components/research-tab/research-tab]].

Cody's timing on subscriptions, offered without being pushed: not expected in
September, early October acceptable.

### Brett named how the flight plan priorities were set, and asked to redo them

Recorded because it is candid and because it changes how the next plan should be
built. On Cody's list of asks: *"I think I've got most of that tracked in the
flight plan"*, then, on the priorities: *"because I just went, 'Hey, AI, what do
you think?' based on the conversations that we've had. So, let's give it the
right priorities."*

He asked for two sessions:

1. A **priority session**, loading Cody's list into the flight plan properly.
2. A **requirement session of about ninety minutes**, walking every user journey
   and mapping the components before any build. His reasoning: *"it gives it a
   way better chance if we do an hour and a half session work through in detail
   every single user journey kind of map it all out and then we load it up then
   it works really really well."*

### The Slack sweep is manual, and the client thought it was not

Troy raised it as an assumption InPlay have been operating on: *"I know we keep
sending you stuff one off in the Slack, so we assume that's being picked up by
AI."*

Brett corrected it honestly: *"I do that once a week. I take everything that's in
the chat and actually manually put it into the vault. So if we do find stuff that
we logged in the chat and it hasn't been picked up, it might be because of
that... it's just a manual, me remembering to do it at the moment."*

⚠ **This is a process gap with a client expectation attached to it.** Items sent
in Slack are being treated by the client as logged. They are logged weekly, by
memory. It should be fixed before the requirement sessions rather than after,
because those sessions will generate exactly this kind of traffic.

### The market maker got its first real client verdict, and it is about liquidity

Three days of live NCAA trading produced a coherent critique rather than a list
of complaints. Troy's rule: **a book must never be empty, not even for an
instant.** George confirmed the momentary gap is by design and named the venue
constraint behind it. George separately raised the structural gap himself: the
maker prices off the win probability alone and behaves the same whether a
thousand or ten thousand people are trading. Both are recorded in
[[market-maker/decisions]] and opened as `N77` and `N78`.

⚠ **The 20 August size cut is now being described back to us as a defect.** The
parameters are doing exactly what they were set to do, at the client's own ask.
Recorded in [[delivery/requirement-changes]] as `A11` and `A12`.

### Smaller items with owners

- **The website's www address is broken.** `inplayglobal.com` works,
  `www.inplayglobal.com` does not, and HubSpot looks responsible for the changed
  record. Cody authorised the fix on the call. See
  [[inplay-global-website/inplay-global-website]].
- **The agency's tester still has no TestFlight build**, and is double-blocked
  behind the outage.
- **The admin panel is being extended** so Cody can create groups and edit share
  codes himself rather than pinging Hasan across timezones.
- **The tZERO call was cancelled** with nothing outstanding on their side. Rob
  was away for an evangelist event.

## 28 August: the day before the first live games

A 49-minute Friday touchdown, the day before the first live NCAA games. Present:
Edwin, Troy, Cody, Jared, Kevin (InPlay) and George, Brett, Hasan, Lily
(Novosapien). It closed with Edwin asking who would be on standby for Saturday.
George: at least one of us.

**The valuation conversation that was cut short on Wednesday finished, and it
finished well.** Edwin stopped describing the pricing model and worked it through
with live numbers: TCU at a **77.3%** win probability against a $5 payout prices
at **$3.86**, and rising toward $5 if they win. The principle underneath it is
that a favourite's value is **already in the price before kickoff**, so what moves
the share is the difference between the expected result and the actual one. Full
record in [[market-maker/decisions]].

**⚠ One defect goes live tomorrow with no fix in place.** George found it and
named it plainly: because expected wins never updates, the price **rises during a
game and then drops back to where it started when the game ends**. Edwin: _"we
don't want anything dropping back down, that's not going to work."_ The fix is
the model above and it is not built. **Plan the first weekend around users seeing
it**, rather than being surprised by it on Monday.

**⚠ The more urgent problem is that some accounts cannot trade at all.** Troy
found two unverified accounts with no buying power, and his real worry is
everyone who signed up in the week since the verification wall came down,
_"expecting those locked feeds to come off now that we're open for secondary
trading."_ Allocating a trading account is still a manual step rather than an
automatic one. Hasan's estimates: **an hour to backfill everyone affected, a few
hours to fix the cause**. Edwin: _"that's a critical piece."_ This is the
operational bill for shipping the KYC-less path quickly, and it is a fair one.

**The home page is being reordered, prompted by outside feedback.** Edwin's
contact at Meta reported that new users find the app overwhelming on open. All
three InPlay voices agreed on the fix: **live games move up, the team IPO tile
moves down below the portfolio**. The reasoning generalises usefully: the offering
is a function the product needs, not a thing users enjoy. _"You buy them and then
you wait."_ ⚠ A defect surfaced alongside it: **college games are not appearing in
upcoming games at all**, the day before college games.

**A good exchange on the order ticket, worth recording as a pattern.** Edwin found
the quantity field sticky and proposed resetting it to zero. George, Jared and
Troy all disagreed with reasons, Troy settled it on the industry norm, and Edwin
took their answer. **The client proposed, the team pushed back, the better answer
won.** Detail in [[trading/trading]].

**The marketing agency now has a timeline**, and it changes what "ready" means.
Discovery in weeks one and two, **first ad tests in week three**, a spend plan in
weeks three and four, **the first real campaign in week five**. Edwin drew the
link himself: paid traffic is worthless if people cannot sign up and trade without
verification. **Week three, not Saturday, is the real deadline for the onboarding
fix.** See [[advertising/advertising]].

**The strategic conversation of the week, and it is about data.** Edwin thinks the
reference model _"might become the most valuable thing we create, that sports
books may want to buy from us"_, and Cody agreed it could _"replace a portion of a
billion dollar company's business."_ The argument is genuinely good: sportsbook
prices move on **flow rather than value**, because each book shades its line to
balance its own position, so polling ten books gives fragmented data rather than a
truer price. **InPlay is a single liquidity pool**, which makes its price a
cleaner signal. ⚠ The best version of it is blocked: deriving probabilities from
live odds needs a **sportsbook licence**. Cody is pursuing a precedent.

**Also:** off-field volume now includes house bot activity, reversing Wednesday's
position within about 24 hours (**R17**), the order ticket default reverts to a
configured setting (**R18**), injuries are deliberately out of scope for now, and
team reference data is wrong in at least a dozen places (Notre Dame's conference,
Louisiana Tech's colour, several abbreviations).

_Source: [[28-08-2026-touchdown]]._

## 26 August: the KYC layer comes off, and the last day of the draft

A 34-minute touchdown on the **final day of the NCAA IPO draft**. Edwin joined at
roughly the 24-minute mark, having worked until 4am, so Troy ran the first two
thirds and took decisions on the understanding he would confirm them. Lily was
introduced to the client on this call.

**The gate identified on 24 August is now open.** Hasan demoed the
no-verification path end to end and it works: a user can create an account and
trade **without an ID document or a face scan**. The call became a live design
review of it, producing four changes (the skip is buried, the fork should be its
own screen, "simulated" goes in front of "trading" everywhere, and "KYC" comes
out of the interface). Detail in
[[customer-onboarding/customer-onboarding]] and
[[compliance/regulatory-positioning]].

**The switch to secondary has a time and a reason.** The IPO window closes at
**22:00 on Wednesday 26 August**, when the buy buttons lock. **Secondary trading
opens Thursday 27 August at 09:30 Eastern.** Troy chose the morning over an
automatic flip at window close specifically so the team is online to **QA the
open**: _"then we're all on and can actively be looking at it in submitting
orders."_ First games **Saturday 29 August**, 138 teams live.

**The numbers, stated on the call.** **187 verified users, 278 downloads.** The
gap of roughly ninety is exactly what the KYC-less path is meant to convert.
Edwin's caveat is worth keeping next to the number: the first batch is
_"primarily all of us in our networks."_ The **interns started this week**, some
already back on campus running involvement fairs with scripts and content.

**There is a week-zero prize pool, and Troy had it wrong.** He assumed no cash
pool for the first week of college games. Edwin corrected him flatly: _"No, we
are."_ Sizing follows the standing rule of thumb of **roughly three dollars per
competitor**, decided within a day and **published Friday 28 August**. ⚠ **There
is no prize pool page in the app**, so it goes out by newsletter and a push alert
linking to the website. See [[leaderboard]].

**The comms plan for the open.** A newsletter tomorrow announcing secondary
trading and the competition being live, a second on Friday carrying the prize
pool, plus a push alert. Cody's framing for week zero: _"use this week just like
the college teams do to warm up and learn the buttons."_ Troy's is sharper and
should win: _"get your referral bank up. That's what we should really be
pushing."_ The **5× referral multiplier holds to 30 August**, so it covers the
first game day.

**⚠ The largest open risk is the Sport Radar futures endpoint, and it is a
supplier problem.** George named the consequence in terms: without that data
_"the market maker is going to be way more volatile than it needs to be. Like it
might just drop off."_ Sport Radar have **three engineers** on a bug open for a
couple of weeks and promise a fix **absolutely before Saturday**, with **a credit
on the bill** if they miss. George is pulling the endpoint daily and building a
fallback until first game day. Tracked as S12 in
[[market-maker/open-questions]]. A bill credit does not price a bad first game
day, so the fallback needs a shape before Saturday.

**Two commercial items are stalled, both ours.** The **warmed-up email outreach to
marketers has not started**: Brett reported a run of bugs after the
reconfiguration, with George and Vineth working through them. Edwin checked
directly and Brett confirmed it. Separately, the **Wayne introduction** in New York
has had no traction despite Brett nudging every second week.

_Source: [[26-08-2026-touchdown]]._

## 24 August: the offering is live, and Thursday hangs on one piece of work

An 18-minute touchdown, the shortest in the record and deliberately so (Troy:
Brett _"wants these to be 15 minutes, not 30"_), two days after the NCAA offering
opened. **Edwin did not join**, which makes it the first post-offering call with
no client-principal steer on it. Troy closed with _"there's a couple refinements
we want to get done this week, but I think, you know, where we're at, we've come a
long way."_

**The dates, as Troy set them out.** The **IPO window closes Wednesday 26 August**.
**Secondary trading opens Thursday 27 August.** The **first games are Saturday**.
The two-day gap is deliberate: _"we wanted to have a couple days again just so
that in case anything was wrong, it wasn't fully visible to the whole universe
yet."_

**Thursday is gated on exactly one piece of work: removing the KYC layer.** Troy
called it _"the highest priority right now"_; George had already described it as
_"not a turn it on"_ job but committed to _"the next day or two"_. Note the shape
of that risk. The thing standing between the product and its trading launch is
**not** the market maker, the venue or the data feed. It is a single piece of
onboarding work, plus the unverified question of whether tZERO have actually
switched off their 18-plus date-of-birth check (G1 in
[[compliance/eligibility-and-age-gating]]).

**The offering's headline defect was a build problem, and it is a lesson about
testers.** People who could not buy from the IPO page were on the **TestFlight
beta** rather than the **live App Store build**. Troy: _"we should have made that
more explicit."_ Jared reinstalled during the call and the IPO page problem
vanished. A **separate** buying-power failure survived the reinstall and is still
open. The operational takeaway: **the first question on any tester report is which
build they are on.**

**New standing requirement: a daily IPO purchase report.** Every account that
bought IPO shares, listed daily. George owns it. Small, but it is the first
reporting obligation this delivery has taken on that is about **oversight** rather
than product.

**One live problem, with a fix already proposed.** The **Florida Atlantic Owls
sold out**, so the market maker has no stock to offer in that book. George called
it _"not a huge issue"_ because most of it was bought by the taker, so positions
can be transferred back to the maker. Two things still to close: the transfer
mechanism is one the engineering log already questions, and **nobody has counted
how many other books are close to sold out**. See N53 in
[[market-maker/open-questions]].

**Still escalating, and this one is on a supplier.** The Sport Radar
college-football futures endpoint remains broken. Cody was promised a fix by
Thursday, wrote twice over the weekend and got **no reply either time**: _"it's a
product that we're paying for."_ He is phoning Scott; George is re-checking the
endpoint. The stand-in is a **CSV from a second provider through a contact**, and
it **decays in about five days** because futures move with results.

**Objectives as George listed them at the close:** the IPO is working for new
users, NFL follows the same process, secondary opens Thursday, the Sport Radar
dates land, and app iterations continue. _Source: [[24-08-2026-touchdown]]._

## 17 August: the commercial position, stated soberly

The tone recovered ("the weekend was better") and the economics got sharper. This
is the clearest account of the business position anyone has given, and it belongs
in the delivery record because it shapes what is worth building next.

| | |
|---|---|
| **Signups** | **154.** Edwin compared it unfavourably with a simulation he ran himself two years ago that drew 600 on a $25,000 spend |
| **Venue cost** | tZERO has moved from free to **$20,000/month minimum for the simulation** and **$150,000 for production**. The original structure gave them a share of advertising revenue, which no longer exists |
| **Expected users** | **5,000 to 10,000 at best**, of whom perhaps a couple of hundred convert to production |
| **Acquisition cost** | Around **$4,000 per customer** against a run cost of one to two million |
| **This iteration** | _"just going to be a complete loss for me"_ |
| **Production market making** | Without external market makers, **$25 to $30 million** of Edwin's own capital across ~14 teams. Outside his zone at present |

**Two structural points that matter more than the numbers.**

First, **more users currently makes the economics worse**: _"even if we had
50,000 people, we have absolutely zero way to monetize them at the moment. So the
more people that sign up is the more people I have to pay."_ That inverts the
normal growth argument and it should change how we talk about acquisition until
there is a monetisation path.

Second, the **29th is the real bar, not the 22nd**. Edwin separated them cleanly:
the offering is survivable, but _"we still need quite a bit of ground to cover
before the 29th"_ when trading actually starts. Plan the polish against the 29th.

**A process note to hold against the reversal position below.** Edwin asked
directly: _"I don't want to go back and forth a ton. If I say I want it this way,
just do it that way."_ That is reasonable and it is also the other half of the
same coin. The answer is not to argue it: it is to make the decision cheap to
record and expensive to reverse, which is what the frozen build definition and
the written displacement statements are for.

**Two commercial ideas raised, both worth keeping.** Approaching **prop trading
firms** for around $5,000 each for recruitment access to university participants,
framed as a goodwill gesture that also bolsters campus interest. And paying
participants on individual days through the start and into September, which needs
a structure before the offering.

**One testing constraint discovered by accident.** The weekend fixtures were
blowouts, so there was almost no price action and the trading experience could not
really be exercised. Edwin: _"they were actually quite boring to trade. You either
had the winner or you didn't."_ It is the argument for George's proposal to run
continuous simulation games on the test tickers rather than waiting for real
fixtures to cooperate.

## The 14 August debrief: the client questioned whether launch is achievable

Recorded plainly because it is the most significant delivery event in the record
and it is not resolved.

**What Edwin said.** The morning after the first live game night he opened with
_"unquestionably the worst trading experience I've ever had in my life"_ and
_"a failure pretty much at every touch point"_. He is due to commit **$800,000
to $1,000,000 to marketing** and stated he cannot do that against what he saw.
He put his own position at **$6.6 million invested**, summarised it as _"we don't
have any users, we don't have any advertisers, we don't have technology that's
comparable... I've got an idea and that's about it"_, and said he believes it is
_"impossible to be ready by football season"_. He was explicit that this is not
quitting, and equally explicit that he has to decide what more he funds.

**What was agreed.** Brett's counter was that this was the **first full
end-to-end test ever attempted**, three months from a standing start, with the
market maker and taker added as an unplanned three-week workstream, and that the
call was being made too early. The agreement: **two more live runs before any
decision**. Edwin accepted the runs. The funding decision is **deferred, not
resolved**, and it should be treated as live at every weekly review until he
closes it.

**Why the diagnosis matters more than the reaction.** Troy located the fault away
from the back end and had tZERO's numbers to support it: 3 million orders, 1
millisecond average latency, no engine degradation. His conclusion was that the
harder part already works and what remains is interface and data ingestion.
George's version, that the work sits on the tip of the iceberg rather than
beneath it, is what turned the conversation from an existential question into a
defined workload. **Hold on to that framing.** A crisis of confidence and a
front-end backlog are very different things to manage, and this is the second.

**Three process changes agreed on the call.**

1. **No pushing fixes mid-game, by default.** Hot fixes during the run caused
   freezes and left testers on different versions. Where a push is genuinely
   needed, it is announced in Slack, and the tester reloads and confirms the
   change is present before continuing. George negotiated this middle path rather
   than a blanket freeze, because a hard freeze turns three nights of iteration
   into one.
2. **Granular feedback, not impressions.** _"The app is slow"_ is not actionable.
   The agreed shape is: when I click this button, this happens, it showed pending
   for three seconds. Screenshots and screen recordings. Cody committed to
   recording his screen during runs, and Jared's written reports are the model.
3. **They are runs, not dry runs.** George's correction on the call. Every
   remaining night before the offering is a real rehearsal with real
   consequences.

**One thing to watch.** Edwin stated that on trading judgement he and Cody are
the only two opinions that count, and that the money comes from the roughly 30%
who trade actively rather than the weekly visitor. He is very likely right about
the revenue. George's counter is the product question: if active traders are 20
to 30% at the start, something has to carry the other 70% from arrival to
competence, and a toggle serves the expert immediately while doing nothing for
the newcomer. Both are true of different users. See
[[one-click-trading-requirements-aug-2026]].

## Requirement reversal: the position taken on 17-08-2026

Recorded because it is a standing position, not a one-off observation.

> **Counted and cited: [[requirement-changes|the requirement change register]].**
> Twenty recorded changes to settled requirements between 20 July and 17 August,
> each traced to where it was decided and where it changed: **11 reversals**, one
> of them a re-reversal, one descope, four late parameter changes and four late
> scope additions. Six of the twenty fall in the last five days of that window.
> The register deliberately excludes internal engineering corrections, of which
> the market-maker log alone carries sixty, because counting those would make the
> number useless.

**The distinction that matters.** Adding scope costs the new work. **Reversing a
settled requirement costs the new work, plus the work already finished, plus the
tests that proved the old behaviour was correct, plus the confidence in
everything built on top of it.** The second prices at several times the first,
and it does not present as a missing feature. It presents as a system nobody can
fully vouch for, which is far harder to see and far worse to launch on.

**What was settled and then changed in the three weeks to 17 August:** the
offering structure (rounds, then no rounds), the share counts, the treasury
holdback (specified, then retired), the subscription payment route (outside
provider, then native store billing), the account model (one path, then three
tiers, then two), and the app's home, team and discover surfaces across three
successive design sessions.

**The fair version, and it is the more persuasive one.** Every change is
defensible on its own and several genuinely improved the product. The direction
has largely been right. **The timing is the problem**, and it compounded: the
same two engineers absorbing the redesigns were the ones taking the system
through its first three live games. That is a direct cause of finished work sitting
unpromoted, which is the "built but switched off" band on the same report.

**The position.** Build definition frozen from 17 August. Every further ask gets
one of two answers: a slot after the offering, which is the default and the
recommendation, or a written statement of what it displaces and which risks it
raises. This applies to small asks as much as large ones, because five days out a
small change is still a change nobody has time to test. A standing requirements
session takes new ideas so nothing is lost.

**Holding the line is InPlay's call, not ours.** We can price the change and name
the consequence; we cannot decline the work.

## Tone rule: this document is client facing (Brett, 12-08-2026)

The flight plan goes in front of InPlay. It carries **delivery status, not the
work of assembling the plan**. Keep out of it:

- Meta-commentary about earlier versions, what a previous plan got wrong, or
  who corrected whom.
- Internal engineering hygiene: repository names, branch names, commit counts,
  promotion chains.
- Attribution of findings to internal reviews.

State the current position plainly and move on. Where something changed, change
it silently in the artefact and record the reasoning here in the vault instead.

## Two corrections from the 12-08 touchdown

**The commercial date is 9 September, not 29 August.** College football starts
on the 29th, but Cody's point settles it: _"no media outlet covers college
football. So us getting any sort of coverage or big blowout news, it's never
going to happen for a college football trading simulation. It will happen
NFL."_ Edwin agreed, adding that even betting behaviour does not reach full
swing until after the first NFL weekend. The NCAA opening still has to work,
and real users still trade it, but **the date that matters for coverage,
marketing spend and first impressions is the NFL opener**. Plan the polish
against it rather than against the 29th.

**Twice-weekly requirement sessions proposed (Brett).** Feedback is arriving
faster as more people use the app and will accelerate further. The proposal is
to use the two days without a standup for a requirements session: collect the
new asks, run them through the spec process, and come back with either an
over-the-air push or a store-push date and a backlog position. The framing
matters as much as the mechanism: half of running product development is
changing things, nobody gets it right first time, and the volume of change is a
sign of engagement rather than failure.

## How the plan is structured (stable conventions)

- **Home:** two-month flight-plan diagram + quarterly release plan + people.
- **Key Releases:** frozen build definition for the launch, ordered must-land list, a **live ranked risk register** (re-scored weekly, never a fixed template), decisions needed from InPlay with deadlines, and the rule that anything "explicitly not in this build" must name its landing slot in a later stage.
- **Next 8 Weeks:** week-by-week deliverables to the key dates, fading to monthly.
- **Quarter pages (4):** identical frame every quarter and band: P1 7 slots and P2 7 slots, each 3 large + 2 medium + 2 small; open slots shown inline; P3 planned-to-drop; a faded **P4 horizon** band (other sports back-plans, the FINRA live-production track).
- **Module Ledger:** all components reconciled repo-vs-proposal-vs-vault, with a soft origin column.

## Key dates it currently tracks

- 19 Aug: NCAA price freeze · 22 Aug: **NCAA IPO opens** · **26 Aug (Wed) IPO window closes · 27 Aug (Thu) 09:30 ET NCAA secondary trading opens** (time set 26-08; KYC layer now removed) · 29 Aug first games, 138 teams live · market maker quoting (E25 pending) · 5 to 6 Sep: NFL IPO · 7 Sep: NFL secondary · **3 Sep (Thu): college week one opens, two ranked games** · ~10 Sep: season kickoff · ~13 Jan 27: season close and settlement. ⚠ **Live from 1 Sep: the app is locked out with no identified cause, and Novosapien's AI tooling is suspended over an unpaid bill.**

## Delivery notes from the 27-07 → 07-08 touchdowns

**The four non-negotiables, in order.** Stated by George on 27-07 and held
across all five calls: **trading, market maker, ads**, then the **tax form**.
Everything else is explicitly deferred, including the analyst prices page and
the subscription features. George's argument, accepted by Edwin and Cody:
premium features are critical for revenue but the app **functions** without
them, whereas without trading and the market maker _"people can't use it."_
Edwin's counter-position, also accepted: not everything has to be live at
launch, _"if the subscriptions become available in week two of the NFL, so be
it."_

**Dry runs.**

| Date | What | Status |
|------|------|--------|
| 6 Aug | First dry run on a preseason game | ✂ Slipped, George called it "looking unlikely" on 31-07 |
| **13 Aug** | **Secondary-trading dry run** on a live preseason game, TestFlight, InPlay team plus friends and family. Several games that night, so multiple team companies possible | 🟡 Target |
| TBD | **IPO dry run.** The 13 Aug run is deliberately secondary-only; Edwin overrode the implication that there would be no IPO test at all, _"I want one test run at least before"_ | 🔴 Unscheduled |

Fallbacks if no live game is available: replay previously played games, or the
Sport Radar simulation games agreed 23-07.

**Estimation tooling (31-07).** Novosapien is building a skill to produce a
timeline, effort and backlog estimate **agentically**, from the actual cadence
of the work, rather than the traditional project-manager guess. Brett was
candid that it is proving difficult. Output: an InPlay-styled document in the
vault showing what has been delivered and what is queued, so the client can
re-prioritise against a visible backlog. This is the origin of the flight plan
above. Cody's ask that prompted it: _"I need daily insight into where the time
is being spent… it's not an attack, it's more just clarity."_

**⚠ Support and maintenance is an unfilled gap (Brett, 29-07).** There is no
support-and-maintenance contract, and Brett flagged it as the one thing missing
from InPlay's coverage, not for launch, but for when volumes rise. CTO-level
coverage is in place and a CIO is not needed at this size. The problem is that
conventional support means humans watching screens around the clock, which he
has built for mobile operators and banks and considers neither cost-effective
nor effective: _"you're trying to hire the most junior person, you're making
them do the shittiest thing, just monitoring."_ The proposal is to design it
**agentically** from the start rather than retrofit automation onto a human
rota. Method agreed: Brett lays out what conventional tiered support looks like,
then the group works out what can be automated. Deliberately **not** being
rushed before launch.

**Novosapien's own estimation caveat, worth keeping (George, 31-07).** On why
AI-assisted delivery dates are hard to give: _"sometimes it's like pushing a
snowball down a hill… other times we don't realise that we're at the start of
pushing it."_ Things that look easy can take two weeks; things that look hard
can be standing up overnight. This is the honest reason behind both the 6 Aug
slip and Cody's request for daily visibility.

Related: [[components]] · [[architecture]] · [[whats-new]] · [[compliance/compliance]]
