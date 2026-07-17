---
type: source-feedback
received: 2026-07-17
author: Edwin Johnson
subject: Media plan / advertising forecast reviews (three rounds)
extracted-to:
  - "[[media-plan-forecast]]"
  - "[[assumptions-register]]"
---

Edwins feedback on the media planning and numbers for the Advertising forecasts

1st review:

I reviewed it. The deck is visually strong and the arithmetic largely ties, but the underlying inventory model is still too aggressive to use as the business-model base case.

The primary problem is not the $1.39 net eCPM. It is the 19.4 billion four-month impression forecast.

**Direct assessment**

| Category | Rating |
| ----- | ----- |
| Visual presentation | 9/10 |
| Arithmetic consistency | 8/10 |
| CPM/eCPM methodology | 6/10 |
| Inventory defensibility | 3/10 |
| Ready for tZERO/Hard Rock/investors | 5/10 |

It is currently a media-sales case, not a defendable financial forecast.

**1\. The deck is using upside inventory as its base**

The Highly Active cohort receives 18,200 impressions per user per month. That is approximately:

* 607 impressions per day  
* Approximately 700 impressions per game at six games per week  
* Roughly 230–240 impressions per active hour, depending on session length

That corresponds to the 15-second live-game rotation shown on Slide 1\.

We already determined:

* 60 opportunities per active hour: downside  
* 120: base  
* 240: upside ceiling

The deck therefore uses our upside frequency for 250,000 people—half the entire monthly audience—and assumes those users generate 94% of inventory.

That is not a suitable base case.

Google’s current guidance says refreshes should not occur more frequently than every 30 seconds; for mobile applications, 60 seconds is recommended. Refreshing inventory must be declared, and only viewable slots should refresh. [Google refresh guidance](https://support.google.com/admanager/answer/6286179).

A 15-second automatic refresh should be removed.

**2\. “Impressions” are actually eligible opportunities**

The 4.84 billion monthly figure is generated before:

* Fill  
* Viewability  
* Invalid traffic  
* SSP deductions  
* Channel adjustments

It should therefore be labeled:

Eligible ad opportunities

It is not 4.84 billion delivered, viewable or billable impressions.

The model needs this waterfall:

Eligible opportunities → served impressions → valid impressions → viewable/billable impressions → gross revenue → net InPlay revenue

Calling everything “impressions” makes the forecast look less rigorous than it is.

**3\. The 2,116-event count needs reconciliation**

The deck says the combined NFL/NCAA season includes 2,116 live events.

That appears to count team appearances rather than unique games. A physical game involving two Team Companies cannot automatically be treated as two independent live events unless:

* Each Team Company has a separate Gamecast;  
* Users can generate separate ad inventory on both; and  
* The model prevents the same user session from being counted twice.

If this is double-counting opposing teams in one physical game, inventory is overstated.

**4\. The time periods conflict**

The deck uses:

* 4.84 billion impressions per in-season month  
* 19.4 billion over a four-month challenge  
* 29 billion at a six-month August–February pace

But the existing football Challenge model uses 142 days—approximately 4.7 months.

We should model the actual daily Challenge period, not switch between four-month and six-month annualizations. The six-month figure can be an upside extension, not the headline.

**5\. The $4.50 blended programmatic CPM is unsupported by format mix**

Slide 2 uses:

* Banner: $1.50  
* Interstitial: $4.00  
* Native: $5.00  
* Rewarded video: $15.00  
* Blended programmatic CPM: $4.50

But it does not show the impression weighting that produces $4.50.

Using our provisional format mix:

| Format | Base share |
| ----- | ----- |
| Banner/display | 55% |
| Native/in-feed | 20% |
| Outstream video | 15% |
| Interstitial | 5% |
| Rewarded video | 5% |

The deck needs an outstream-video rate and a visible weighted-average formula.

Rewarded video should remain a small share because it requires an affirmative user choice. It cannot be used to inflate the blended CPM across ordinary display inventory.

**6\. The 35% first-party-data uplift should not be automatic**

The deck increases the $4.50 programmatic CPM to $6.09 because of KYC, teams, geography, age and behavior.

That is not defendable at launch.

Persona verification improves audience quality and reduces bot risk. It does not automatically cause programmatic buyers to pay 35% more.

Recommended treatment:

| Stage | Data uplift |
| ----- | ----- |
| Launch | 0% |
| Audience validated | 10% |
| PMP/direct demand established | 20% |
| Upside with demonstrated performance | 35% |

The uplift should depend on actual advertiser demand, not merely possession of first-party data.

**7\. The eCPM deductions are partly double-counted**

The deck applies:

* 60% fill  
* 78% viewability  
* 5% invalid traffic  
* 31% exchange cut  
* Channel mix  
* Another 20% sales commission

This produces the $1.39 net eCPM.

The problems:

* Fill belongs in the impression waterfall, not necessarily as an eCPM haircut.  
* Viewability should determine billable inventory and pricing—not always multiply revenue again.  
* The 31% exchange cut already represents programmatic selling friction.  
* A 20% sales commission should apply to directly sold inventory where a salesperson or representative earns it—not automatically to programmatic inventory after an SSP deduction.

The $1.39 result may be conservative, but the route used to reach it is conceptually messy.

**8\. The model does not include the current tZERO economics**

tZERO receives:

* 10% of Net Simulation Marketing Revenue  
* Capped at $1.75 million aggregate per month  
* No fixed event or monthly fee for the 2026 NFL/NCAA football challenge

The deck’s $26.8 million four-month InPlay net figure is therefore not actually InPlay’s final net revenue.

Before prizes:

* Reported net marketing revenue: $26.8 million  
* tZERO share at 10%: $2.68 million  
* InPlay after tZERO: $24.12 million

Assuming the revenue definition matches the proposed agreement.

**9\. Direct and territory revenue is not base-case revenue**

The deck includes:

* $600,000 direct-sold revenue  
* $300,000 territory revenue

Those amounts are not contracted. They should be:

* $0 in downside  
* Probability-weighted in base  
* Fully included only in upside

The tZERO fee waiver and revenue share are proposed economics—not evidence that tZERO has purchased a sponsorship territory.

**Recommended revised inventory cases**

Using the deck’s current inventory architecture but correcting the ad frequency:

| Case | Opportunities/hour | Monthly opportunities | 142-day opportunities |
| ----- | ----- | ----- | ----- |
| Downside | 60 | Approximately 1.21B | Approximately 5.73B |
| Base | 120 | Approximately 2.42B | Approximately 11.45B |
| Upside | 240 | 4.84B | Approximately 22.91B |

These are still subject to the audience ramp. They assume 500,000 MAU throughout the period, which will not be true if the Challenge begins near 10,000 users and grows toward one million unique registrations.

Therefore, even 11.45 billion is not the final base case. It must be multiplied by the monthly MAU ramp.

**Recommended CPM/eCPM structure**

Instead of one static $4.50 CPM:

| Stage | Gross blended CPM | Net realized eCPM target |
| ----- | ----- | ----- |
| Launch | $2.50 | $1.50–$1.75 |
| Early scale | $3.25 | $2.00–$2.25 |
| Validated audience | $4.25 | $2.75–$3.00 |
| Strong PMP/video mix | $5.50 | $3.75–$4.25 |

That reflects your position correctly: InPlay starts lower and levels up as the audience, inventory and advertiser evidence develop.

**Bottom line**

The $4.50 gross blended CPM is possible later in the Challenge. The $1.39 net realized eCPM is not unreasonable as an initial conservative result.

But the deck reaches $26.8 million by combining:

* 500,000 monthly active users from the beginning;  
* 240 impressions per active hour;  
* 15-second refresh;  
* Six games per week for half the audience;  
* A 35% first-party-data uplift;  
* Uncontracted direct sales.

That combination is not defensible.

The corrected model should use:

* A monthly audience ramp from roughly 10,000 toward the Year 1 target  
* 120 opportunities per hour in base  
* 30–60-second refresh rules  
* A visible format mix  
* A staged CPM/eCPM ramp  
* No automatic 35% data premium  
* $0 contracted sponsorship in base  
* tZERO’s 10% revenue share  
* The actual 142-day Challenge period

I would not use the current $26.8 million as the business-model base case without those corrections.

2nd Review:

**how do i model the prices for this screen to advertisers?**  
Worked for 2m 10s

Do not price the entire screen using one $3.25 CPM. That would materially underprice the video, Volatility Moments and direct sponsorship rights.

The screen needs five separate pricing models:

1. Standard programmatic display  
2. Private-marketplace and direct display/native  
3. Volatility Moments  
4. Scheduled field video  
5. Gamecast sponsorship rights

Digital video and live sports demand are growing rapidly, which supports pricing the field-video inventory separately and substantially above display. IAB projected $72 billion of U.S. digital video spending in 2025 and specifically identified live sports as a growth driver. [IAB Digital Video Report](https://www.iab.com/insights/video-ad-spend-report-2025/)

**Recommended launch rate card**

These are recommended InPlay prices, not contracted rates.

| Product | Advertiser rate card | Business-model realized price |
| ----- | ----- | ----- |
| Open-auction display | Not quoted directly | $3.25 CPM |
| PMP display/native | $8 CPM | $6–$6.50 CPM |
| Direct guaranteed display | $12 CPM | $8–$10 CPM |
| Native play-by-play unit | $15 CPM | $10–$12 CPM |
| Volatility Moment overlay | $25 CPM | $15–$18 CPM |
| Six-second field video | $30 CPM | $20–$24 CPM |
| Fifteen-second field video | $40 CPM | $27–$32 CPM |
| Thirty-second halftime video | $55 CPM | $35–$42 CPM |

The rate card is what sales quotes. The realized price is what the financial model should use after negotiated discounts.

**Standard display inventory**

Use the four-opportunities-per-minute model:

Qualified impressions=active minutes×4×fill×viewability×(1−IVT)

For a three-hour game:

180×4×60%×80%×95%=328.32

Therefore, each full three-hour user-game creates approximately 328 quality-adjusted display impressions.

**Channel-mix assumption**

Do not assume all inventory sells at the same CPM.

A defensible base mix after fill would be:

| Channel | Share of filled inventory | Gross CPM | Channel cost |
| ----- | ----- | ----- | ----- |
| Open auction | 80% | $3.25 | 31% |
| Private marketplace | 15% | $6.50 | 20% |
| Direct guaranteed | 5% | $10.00 | 15% sales cost |

That produces:

* Gross blended advertiser CPM: approximately **$4.08**  
* Net before tZERO: approximately **$3.00**  
* Net to InPlay after tZERO’s 10%: approximately **$2.70 per 1,000 quality-adjusted impressions**

This is how you can honestly show a gross CPM greater than $4 while still forecasting a lower net eCPM retained by InPlay.

**Volatility Moment pricing**

Use:

Revenue=user-game sessions×moments per game×viewability×(1−IVT)×1,000Volatility Moment CPM​

For the 250,000 highly active users:

* Six games per week  
* 16 weeks  
* 24 million user-game sessions  
* 20–30 Volatility Moments per game

That produces approximately 365–547 million quality-adjusted live Volatility Moment impressions.

At the modeled $15 CPM:

| Moments/game | Qualified impressions | Gross advertiser value |
| ----- | ----- | ----- |
| 20 | 364.8M | $5.47M |
| 25 | 456.0M | $6.84M |
| 30 | 547.2M | $8.21M |

A single sponsor is unlikely to commit $5–$8 million initially. Therefore, use one of these structures:

**Exclusive sponsor**

* Minimum guarantee: $1.5 million  
* Impression escalators  
* Maximum payment: $6 million  
* Category exclusivity  
* Live and replay branding  
* Full reporting

**Rotating sponsors**

Sell four 25% shares of voice:

* Initial price: $500,000–$750,000 each  
* Escalator to $1.5 million each  
* Maximum total Volatility Moment revenue: approximately $6 million

The base financial model should use the contracted minimum only. The CPM value determines the escalator.

**Field-video pricing**

Five video opportunities per game creates:

24 million user-games×5=120 million video opportunities

Model video through separate stages:

Completed views=opportunities×video fill×viewability×completion rate

Example base assumptions:

* 75% video fill  
* 90% viewability  
* 80% completion

120M×75%×90%×80%=64.8M completed views

At a blended realized video CPM of $28:

64.8M÷1,000×$28=$1.81M

That is the highly active segment alone.

**Sell video positions separately**

| Video position | Suggested opening package |
| ----- | ----- |
| Pregame | $500,000 minimum |
| Q1 and Q3 break package | $500,000 minimum |
| Halftime | $750,000 minimum |
| Postgame | $250,000 minimum |
| Complete game-break package | $1.5M–$2M minimum |

These minimums should include a defined quantity of completed views, followed by a CPM overage.

**Presented-by modules**

The Win Probability and Price Chart modules should be sold primarily as sponsorships.

**Win Probability sponsor**

* Opening floor: $500,000  
* Target after validation: $1 million  
* Maximum with escalators: $2 million

**Market Price sponsor**

* Opening floor: $500,000  
* Target after validation: $1 million  
* Maximum with escalators: $2 million

Each package should include:

* “Presented by” branding  
* Category exclusivity  
* A guaranteed quantity of qualified exposures  
* Programmatic backfill when the sponsor is absent  
* CPM overages after the guarantee

**Full Gamecast territory**

The entire Gamecast territory should not be sold as unlimited inventory for one fixed payment.

Use:

* $2 million guaranteed minimum  
* Category exclusivity  
* Naming/presenting rights  
* 20%–25% share of voice  
* Priority access to video and Volatility Moments  
* Impression escalators  
* Maximum payment of $9 million

One possible escalator:

| Qualified Gamecast exposure milestone | Cumulative advertiser payment |
| ----- | ----- |
| Contract execution | $2.0M |
| 250 million | $3.0M |
| 500 million | $4.0M |
| 1 billion | $5.5M |
| 2 billion | $7.0M |
| 4 billion | $9.0M cap |

The partner receives category exclusivity—not 100% ownership of every advertising impression. InPlay retains the remaining share of voice for programmatic and noncompeting advertisers.

**Financial-model structure**

Build one row for every product:

| Product | Inventory driver | Selling unit | Base realized price |
| ----- | ----- | ----- | ----- |
| Standard display | Active minutes × four | Quality-adjusted CPM | $3.25–$4.08 gross blend |
| Native play unit | Qualified native views | vCPM | $10 |
| Volatility Moments | Qualified moment exposures | vCPM | $15 |
| Six-second video | Completed views | CPM/CPCV | $22 |
| Fifteen-second video | Completed views | CPM/CPCV | $28 |
| Halftime video | Completed views | CPM/CPCV | $38 |
| Presented-by rights | Contract | Fixed fee plus overage | Event-specific |
| Gamecast territory | Contract | Minimum plus escalators | $2M–$9M |

Then show the revenue waterfall separately:

1. Gross advertiser spend  
2. Agency/sales commission  
3. Exchange and adtech costs  
4. Net Simulation Marketing Revenue  
5. tZERO’s 10%  
6. Revenue retained by InPlay

The key pricing rule is simple: **$3.25 belongs only to open-auction display. It should never be used to value Volatility Moments, field video or the exclusive Gamecast sponsorship.**

**how do i sell directly, i am having a lot of trouble?**  
Worked for 59s

You are having trouble because you are trying to sell a large, unfamiliar sponsorship before the audience exists. The buyer is being asked to believe:

* InPlay will launch on time.  
* Users will arrive.  
* Users will remain active for hours.  
* The ad inventory will work.  
* Measurement will be accepted.  
* The regulatory/sports-trading context will be brand-safe.  
* The projected impression volume will materialize.

That is too much risk for a cold buyer, especially weeks before launch.

The immediate solution is to stop leading with $2–$9 million territory packages. Sell a small, guaranteed, measurable pilot.

**What you should sell now**

Create one product:

InPlay NFL \+ NCAA Charter Advertiser Pilot

The offer should be:

* $50,000 initial commitment  
* Two- to four-week campaign  
* Guaranteed qualified impressions  
* Gamecast display  
* Volatility Moment exposure  
* Field-video exposure  
* Persona-verified audience  
* Age and geographic targeting  
* Campaign reporting  
* Full makegood if InPlay underdelivers  
* No long-term obligation  
* Option to convert into a season sponsorship

The makegood removes much of the audience-delivery risk. If you promise five million qualified impressions and deliver only three million, the remaining two million roll into the next NFL/NCAA period, NBA challenge or another competition.

Do not promise cash refunds unless absolutely necessary.

**Three packages**

Give buyers only three choices.

**Pilot — $50,000**

* Five million qualified display/native exposures  
* 250,000 Volatility Moment exposures  
* 100,000 completed or viewable video exposures  
* No exclusivity  
* Two- to four-week flight  
* Delivery guarantee and makegood

**Launch Partner — $150,000**

* Fifteen million qualified display/native exposures  
* One million Volatility Moment exposures  
* 500,000 completed or viewable video exposures  
* Rotation in one “presented by” module  
* Category conflict protection during the campaign  
* Four- to eight-week flight  
* Delivery guarantee and makegood

**Charter Partner — $300,000**

* Twenty-five million qualified display/native exposures  
* Two million Volatility Moment exposures  
* 2.5 million completed or viewable video exposures  
* Gamecast presenting-partner rotation  
* Category exclusivity during the campaign  
* Social and reporting integration  
* First negotiation right for the full-season territory  
* Delivery guarantee and makegood

These packages need to be reconciled against the final rate card before being issued, but this is the right commercial scale.

**Who you should contact**

Stop making the CMO your primary target. The CMO rarely buys individual digital media packages.

At brands, target:

* VP or Head of Media  
* Director of Digital Media  
* Director of Integrated Media  
* Director of Sports Marketing  
* Director of Brand Partnerships  
* Programmatic Media Lead  
* Director of Customer Acquisition

At agencies, target:

* Media Investment Director  
* Digital Investment Director  
* Programmatic Director  
* Sports Investment Lead  
* Group Director, Media  
* Client Investment Lead  
* Video Investment Director

Ask one direct question:

Are you responsible for digital sports and video media investment for this brand?

If the answer is no, ask who is.

**What you should say**

Do not lead with Sports Performance Securities, the corporate structure, the future production market or a $9 million sponsorship.

Lead with the media opportunity:

InPlay is launching a free NFL and college-football trading competition that puts verified users inside a live, interactive Gamecast for hours at a time. We are opening three measured charter-advertiser pilots across display, live-event sponsorship and scheduled video. The initial commitment is $50,000, delivery is guaranteed and any shortfall receives a full makegood. I would like to show you the experience and determine whether it fits one of your fall sports campaigns.

That is much easier to understand and approve.

**What the sales meeting should look like**

The first meeting should take 15–20 minutes.

1. Show the application immediately  
   Spend no more than 90 seconds introducing InPlay.  
2. Show the Gamecast screen  
   Demonstrate exactly where the brand appears.  
3. Show one Volatility Moment  
   Let the buyer see the five-second branded experience.  
4. Show the scheduled video takeover  
   Demonstrate pregame, quarter and halftime placement.  
5. Explain measurement  
   Verified users, viewability, video completion and reporting.  
6. Present one recommended package  
   Do not walk through ten territories.  
7. Ask for a decision process  
   “What would have to happen for your team to approve a $50,000 measured pilot?”

You need to get the objection into the open.

**Materials you are missing**

Before more outreach, you need a buyer-ready sales kit:

* One-page media overview  
* 60–90-second demonstration video  
* Annotated Gamecast inventory page  
* Three-package rate card  
* Audience and KYC summary  
* Measurement methodology  
* Brand-safety and moderation summary  
* Campaign calendar  
* Sample post-campaign report  
* Standard insertion order  
* Creative specifications  
* Makegood policy

A broad investor or Hard Rock business deck is not a media-sales package.

**Use Programmatic Guaranteed for media buyers**

Some agencies will not want to process a custom insertion order with an untested publisher. Once they agree to the campaign, offer to transact through their DSP using a Programmatic Guaranteed deal at an agreed CPM and impression quantity.

Programmatic Guaranteed supports a fixed CPM and guaranteed delivery; Preferred Deals can provide fixed-price access without guaranteed volume. [Google Ad Manager transaction types](https://support.google.com/admanager/answer/9248464), [Programmatic Direct features](https://support.google.com/admanager/answer/9345607?hl=en)

Use:

* Traditional insertion orders for naming rights, custom integrations and exclusivity.  
* Programmatic Guaranteed for standard display, native and video delivery.  
* Preferred Deals or PMP inventory for buyers who want access without a fixed commitment.

That makes InPlay easier for agencies to buy.

**Your sales representation problem**

You should not personally be the only seller.

Use two experienced independent media sellers who already know agency investment teams. Compensation should be based on collected revenue:

* 15% commission on direct business  
* Up to 20% for a completely new account  
* No commission on unpaid contracts  
* Limited or no monthly retainer  
* Defined account ownership  
* Ninety-day initial term

Katz may be able to help, but you need an explicit answer from them:

Will Katz actively represent this inventory, assign named sellers, provide a target-account list and commit to a launch sales schedule?

General interest is not a sales mandate.

Do not wait exclusively for Katz. Run independent sellers and founder-led selling simultaneously.

**Your immediate sales target**

Your prelaunch objective should not be one $2 million advertiser.

It should be:

* Three to five paying pilots  
* $250,000–$750,000 of contracted revenue  
* At least three advertiser categories  
* Live campaign data  
* A documented case study  
* A credible post-launch rate increase

Once you can show real users, actual hours, viewability, completion rates and verified delivery, the $1–$3 million conversations become materially easier.

**Thirty-day execution plan**  
**Days 1–3**

* Finish the media kit.  
* Produce the 90-second demo.  
* Finalize the three packages.  
* Complete the insertion order and makegood terms.  
* Build a sample reporting dashboard.

**Days 4–10**

* Build 100 target accounts.  
* Identify three relevant contacts per account.  
* Prioritize challenger brands and mid-market companies capable of approving $50,000 quickly.  
* Ask every investor, partner, advisor and university contact for media-buyer introductions.

**Days 11–20**

Daily founder targets:

* 20 personalized emails  
* 20 LinkedIn contacts  
* Five direct calls  
* Two demonstrations  
* One written proposal

Do not send the full deck before earning the meeting. Send the one-page media overview and demo.

**Days 21–30**

* Close pilots.  
* Obtain creative.  
* Create campaigns in the ad server.  
* Confirm measurement.  
* Produce launch case studies immediately after delivery begins.

The blunt answer is that major brands are unlikely to approve a multimillion-dollar direct sponsorship before InPlay proves its audience. A $50,000 guaranteed pilot is sellable. Close several of those, prove the product and then raise the price.

3rd Review:

**can i run 4 ads per minute on an ssp?**  
Worked for 35s

**Yes, you can technically generate four ad requests per minute through an SSP/mediation platform, but the compliant structure matters.**

**Recommended structure**

Use **four separately defined ad units**, each refreshing every 60 viewable seconds:

1. Gamecast upper-left display  
2. Gamecast lower-left native/display  
3. Win Probability slim unit  
4. Market Price slim unit

That produces:

4 ad units×1 refresh/minute=4 opportunities/minute

This is substantially more defensible than one banner refreshing every 15 seconds.

**AppLovin versus Google**

AppLovin MAX technically allows banner and MREC refresh intervals between 10 and 120 seconds. Therefore, its SDK can support a 15-second refresh. [AppLovin MAX advanced settings](https://developers.applovin.com/en/max/ios/overview/advanced-settings/)

But MAX is a mediation platform, not one single source of demand. The advertisements come from multiple demand partners, and each partner can have stricter rules.

Google demand requires declared time- or event-based mobile-app refreshes to remain visible for at least 30 seconds, with 60 seconds recommended. Google also states that longer refresh intervals are generally more desirable to buyers. [Google Ad Manager refresh rules](https://support.google.com/admanager/answer/6286179?hl=en)

Therefore:

* Four units refreshing every 60 seconds: **Yes**  
* Two units refreshing every 30 seconds: **Technically possible, but less desirable**  
* One unit refreshing every 15 seconds: **AppLovin may technically permit it, but do not build the model around it**  
* Four units refreshing every 15 seconds: **No—this would be 16 impressions per minute and would likely damage demand quality**

The strictest demand partner’s requirements should govern the placement.

**What four opportunities per minute really produces**

Four opportunities per minute does not mean four paid impressions.

| Stage | Per minute | Per three-hour game |
| ----- | ----- | ----- |
| Eligible ad requests | 4.000 | 720.00 |
| Filled at 60% | 2.400 | 432.00 |
| Viewable at 80% | 1.920 | 345.60 |
| After 5% IVT | **1.824** | **328.32** |

The business model should call 720 “eligible opportunities,” not billable impressions.

**Technical rules for InPlay**

Tell the development team:

* Create four unique ad-unit IDs.  
* Use a 60-second refresh for each.  
* Start the refresh timer only after the unit becomes viewable.  
* Stop refreshing when the application is backgrounded.  
* Stop refreshing if the placement is outside the viewport.  
* Pause refresh during field-video ads and Volatility Moment overlays.  
* Do not load multiple new ads when the user rapidly moves backward through plays.  
* Integrate Open Measurement for viewability and verification.  
* Track fill, latency and eCPM separately for each placement.  
* Allow individual placements to be disabled if they hurt performance or user experience.

Do not make a single network request that attempts to return four ads. Each placement needs its own auction and reporting.

**Questions AppLovin must answer in writing**

Before locking this into the forecast, ask AppLovin:

1. Does MAX permit four simultaneously visible banner/native/MREC units on this Gamecast screen?  
2. Can all four refresh every 60 seconds?  
3. Which mediated demand partners restrict multiple simultaneous placements?  
4. Will Google/AdMob demand participate in all four units?  
5. Does refresh occur only when the unit is viewable?  
6. Will four simultaneous auctions reduce fill or create auction competition between InPlay’s own placements?  
7. Are all four formats supported by OM SDK measurement?  
8. What eCPM and latency effects should InPlay expect from this configuration?  
9. Does MAX recommend staggering the four refreshes?  
10. Can direct-sold campaigns override the programmatic auction in individual units?

I would stagger the refreshes:

* Unit 1 at second 0  
* Unit 2 at second 15  
* Unit 3 at second 30  
* Unit 4 at second 45

Each unit still refreshes only once every 60 seconds, but the app avoids launching four auctions simultaneously.

**Conclusion:** four opportunities per minute is technically supportable and can remain in the inventory model. It should be implemented as four separately measured, 60-second viewable-refresh placements—not one rapidly refreshing banner.

Also:

My verdict: these are materially better than the prior deck, but neither is ready to become the business-model forecast.  
**What Brett improved**

* The model distinguishes eligible opportunities, served ads, valid traffic, viewability and billable impressions.  
* It uses average audience during the ramp—234,000—not 500,000 for the entire season.  
* Uncontracted direct sponsorship is excluded from the base.  
* tZERO’s 10% revenue share is included.  
* The $1.75 million monthly tZERO ceiling is identified.  
* The format blend producing a $3.98 rate-card CPM is mathematically correct.  
* The 142-day challenge is separated from a hypothetical six-month extension.

**Required corrections**

1. **The 240 case is described incorrectly.**

It says “15-second rotation.” That is not our intended architecture.

The correct description is:

Four independently served placements, each eligible for refresh approximately every 60 seconds, producing up to 240 eligible opportunities per active hour.

Base 120 can represent only two placements monetizing on average, or 50% inventory utilization. It should not be described as the fundamental Google-compliant limit.

2. **The calendar is inconsistent.**

The audience curve begins August 1 and ends around December 19, while the 142-day competition runs approximately August 22 through January 10\. January is missing. The launch period and competition period need separate dates.

3. **The CAC language is wrong.**

The deck shows:

* $25 paid-media CAC  
* $978,000 paid spend  
* Approximately 39,120 paid acquisitions  
* $1.96 “blended per user”

The $1.96 is not CAC. It is paid-media spend divided by ending users. Clean terminology should be:

* Paid-media CAC: $25  
* Fully loaded paid CAC: still to be calculated  
* Paid acquisition spend per ending verified user: approximately $2  
* Organic/referral share of acquisition: approximately 92%, not 98%, before considering churn

Fully loaded CAC must include paid media, creative/agency costs, referral rewards, promotional cash, affiliate payments, attribution and fraud expenses attributable to acquisition.

4. **The live-game inventory does not reconcile.**

At 120 opportunities per hour:

`6 games × 3 hours × 4.33 weeks × 120 = approximately 9,353 live-game opportunities per highly active user per month`

But the deck shows approximately 9,100 total opportunities across all surfaces, while Live Game accounts for only 42.9% of inventory. Those statements cannot all be true. We need Brett’s actual formula.

5. **Neither case models CPM leveling through the season.**

The base applies $2.50 across the entire challenge. The upside effectively applies $7.43 across the entire challenge. Our model should stage it—for example:

* Launch: $2.50  
* Early scale: $3.25  
* Validated audience: $4.25  
* Strong PMP/direct demand: $5.50+  
* First-party-data uplift only after it is demonstrated

That will produce a more credible central forecast between $3.29 million and $20.01 million.

6. **The upside changes too many assumptions simultaneously.**

It doubles inventory, nearly triples gross CPM and introduces direct sponsorship. That turns $3.29 million into $20.01 million, but it does not show which assumption drives the increase.

We need a sensitivity matrix separating:

* 120 versus 240 opportunities per hour  
* Low versus staged versus validated CPM  
* Audience downside/base/upside  
* Programmatic-only versus contracted direct sales  
7. **The 90% programmatic allocation is unexplained.**

If 10% is reserved for direct sales but remains unsold, does it receive programmatic backfill or generate nothing? That decision must be explicit.

8. **One upside figure is inconsistent.**

$20.01 million divided by 4.23 billion billable impressions equals approximately $4.73 net eCPM, not $4.66.

9. **The files are not actually editable models.**

Each slide is a single flattened PNG placed into PowerPoint. There is no embedded calculator, spreadsheet or editable chart data. Brett needs to deliver the source calculator and editable design file.

**Recommendation**

Use neither deck unchanged.

Keep 240 opportunities per hour as the full screen capacity, but build the base forecast using conservative delivery, fill, viewability and staged CPM assumptions. Treat 120 as a delivery/utilization case—not as a different technical architecture.

I would rate them:

* Base 120: **6.5/10** as an internal planning summary  
* Upside 240: **4.5/10** as a forecast, but **7/10** as a ceiling illustration

The next deliverable should be one integrated model with base, downside and upside controls—not two disconnected decks. The immediate request to Brett should be the editable calculator containing the audience, surface and revenue formulas.

