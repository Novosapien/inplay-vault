---
description: "Delivery hub for the InPlay app flight plan, the Novosapien/InPlay working agreement, with committed snapshots, structure conventions and key launch dates"
---

# Delivery · InPlay App Flight Plan

> **Status:** Living · updated per working session
> **Owner:** Novosapien (product owner: Brett StClair)
> **Live copy:** `shared/clients/inplay/flight-plans/inplay-app-flight-plan-{date}-{HHMM}.html` (a new timestamped file per build; prior versions stay as the audit trail)
> **Master:** `Programming/inplay/inplay-app-flight-plan/` (source + build script)
> **Companion:** [[requirement-changes|Requirement change register]], the citable record of settled requirements later changed

The flight plan is the delivery working agreement between Novosapien and InPlay: what has shipped, what is committed, what capacity exists, and the live risks into each launch. It is produced with the `/novosapien-product-owner` skill from three reconciled sources: the build repositories, the partnership proposal, and this vault. This section holds the committed snapshots; each weekly review runs off the newest one.

## Snapshots

| Date | File | Headline state |
|------|------|----------------|
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
through its first two live games. That is a direct cause of finished work sitting
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

- 19 Aug: NCAA price freeze · 22 Aug: **NCAA IPO opens** · 26 to 27 Aug: NCAA secondary + market maker quoting (E25 pending) · 5 to 6 Sep: NFL IPO · 7 Sep: NFL secondary · ~10 Sep: season kickoff · ~13 Jan 27: season close and settlement.

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
