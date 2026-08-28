---
description: "Rolling changelog — dated entries for every major vault update, from the vision workshop through SNT-1, IPO pricing v1.0 and the tZERO OMS Q&A"
---

# InPlay Trading Challenge -- What's New

> **Project:** [[index]]

## 2026-08-27: Two settled decisions reversed, in a call that was cut off

Digested [[27-08-2026-touchbase]], thirteen minutes on the morning secondary
trading opened. It was cut short by Troy for the tZERO go-live call, and Edwin's
parting words were that the conversation is very important and should resume. It
has not. Everything below is an instruction rather than a settled position, and
the vault records it that way.

**We built the offering the wrong way round.** George explained our structure,
where the market maker holds all the shares and the taker buys them. Edwin said
plainly: "so that's backwards." In a real offering the team company sells its own
shares, a broker dealer handles the sale, whatever does not sell rests in the
team's own treasury, and the market maker acts as selling agent holding real
inventory. He accepted what we built for the college run, calling it a good
simulation, and then gave a clear instruction for the next one: for the NFL, the
maker becomes the buyer. That is a structural change to the part of the system
that has just run a live offering, ten days before it runs the next one.

**Treasury is back.** It was retired on the twelfth of August, after the app had
already removed a field built for it. Edwin has now described it as a working
part of the structure, holding the unsold shares as a kind of securities bank
account. That makes it the second time a decision has been reversed and then
reversed back, and it is recorded as such.

**The bigger reversal is about price.** Since late July the agreed position has
been that the in-game price follows Sportradar's win probability directly, with
no model of our own. Edwin has now said the opposite: prices cannot be locked to
win probability. His example is the clearest explanation of his thinking we have
on record. An underdog wins seventy to nothing. The win probability reaches a
hundred percent, so a probability-locked price stops. But the market's view of
that team has changed completely, and the share should keep climbing. The price,
he says, should reflect what the market expects a share to be worth over time,
not just the chance of winning today.

**The catch is that the fix depends on the feed that is broken.** His mechanism
needs a team's expected wins to move after a game. George checked immediately
before the call: for college teams, expected wins is frozen, because the
Sportradar futures endpoint has been down for a fortnight. So the correction
depends on the input we do not have, which is the same input Saturday's pricing
needs.

**Worth noticing, because it is the first time.** Edwin asked for a control that
would let him adjust the market maker's spread during a live game, and then
withdrew the request himself before anyone started work, telling George to get
through the weekend first. Every previous late request in this record was
absorbed. This one was stood down by the person asking, and the vault now records
held asks alongside changed ones so that restraint is visible.

**Also confirmed:** trading volume is never shown publicly on any team, because
publishing it would tell users which team is about to receive the larger
off-field payout and turn the mechanic into a coordination game.

## 2026-08-26: The KYC layer comes off, and the draft closes tonight

Digested [[26-08-2026-touchdown]], 34 minutes on the final day of the NCAA IPO
draft. Edwin joined two thirds of the way through, having worked until four in the
morning, so Troy ran most of it. Lily was introduced to the client.

**The thing that was gating Thursday is done.** Hasan demoed the no-verification
path end to end: a person can now create an account and trade without an identity
document or a face scan. The call turned into a live design review of it and
produced four changes, all of which are worth having. The skip option is buried
below the fold and has to move to the top. The verify-or-not choice should be its
own screen straight after the email code, rather than hidden inside a verification
screen. The word "simulated" goes in front of "trading" everywhere, because
"start trading now" reads too much like a real brokerage account. And the term
"KYC" comes out of the interface entirely, replaced by "get verified" and "start
trading without verification".

**Worth flagging: there are now two different first screens.** The 17 August call
put a choice of three competitions on first open. This one puts a verify-or-not
fork straight after the email code. Nobody has reconciled them into one sequence,
and both are being built.

**The open has a time and a reason.** The draft closes at ten tonight and the buy
buttons lock. Secondary trading opens Thursday at half past nine Eastern. Troy
chose the morning deliberately rather than flipping it overnight, so the whole
team is online to test the open and confirm the locks came off. First games
Saturday, 138 teams live.

**The numbers.** 187 verified, 278 downloads. That gap of about ninety is exactly
what the no-verification path exists to convert. Edwin's caveat stands beside it:
the first batch is almost entirely their own networks. There is a prize pool for
week zero after all, at roughly three dollars per competitor, published Friday,
and there is no prize pool page in the app, so it goes out as a link to the
website.

**The largest risk is now a supplier.** The Sportradar futures endpoint is still
broken, and George put the consequence plainly: without it the market maker will
be far more volatile than it should be and might drop off altogether. Sportradar
have three engineers on it and promise a fix before Saturday, with money back if
they miss. That is not the same as a good first game day, so a fallback needs a
shape before then.

**Also:** the referral multiplier stays at five times until the end of the month,
so it covers the first game day, the app icon might be changeable without a store
review even though the name is not, and our warmed-up email outreach to marketers
still has not started because of bugs.

## 2026-08-24: The offering is live, and Thursday hangs on one piece of work

Digested [[24-08-2026-touchdown]], eighteen minutes, the shortest touchdown in the
record and deliberately so. Two days after the NCAA offering opened. **Edwin did
not join**, which makes it the first post-offering call with no client-principal
steer on it.

**The dates, and the shape of the risk.** The IPO window closes Wednesday, secondary
trading opens **Thursday 27 August**, and the first games are Saturday. The gap is
deliberate, so that anything wrong is not visible to everyone at once. Thursday is
gated on exactly one piece of work: **removing the KYC layer**, which Troy called
the highest priority and George sized at a day or two. Worth sitting with: the
thing standing between the product and its trading launch is not the market maker,
the venue or the data feed. It is a single piece of onboarding work, plus an
unverified question about whether tZERO have actually switched off their
eighteen-plus date-of-birth check.

**The headline defect was a build problem, and it carries a lesson.** Testers who
could not buy from the IPO page were still on the TestFlight beta rather than the
live App Store version. Jared reinstalled during the call and the problem vanished.
Troy: "we should have made that more explicit." The first question on any tester's
"the app is broken" report is now which build they are on. A separate buying-power
failure survived the reinstall and is still open, with a useful error message: open
orders and shorts are holding the play dollars, so the balance is held rather than
absent.

**A team sold out, and George already had the fix.** The Florida Atlantic Owls sold
out, so the public holds the entire float and the market maker has nothing to offer
in that book. Most of it was bought by the taker, so positions can be transferred
back to the maker. He called it not a huge issue, and he is probably right, with two
caveats: the transfer mechanism is one our own engineering log has questions about,
and nobody has yet counted how many other books are close to selling out.

**A correction worth having.** We had the shorting constraint backwards. Troy: there
is no limit on shorts in the simulation, the limit is in production. An extra million
shares per team is shortable and tZERO have turned the locate flag off. That takes
the venue out of the picture for now and leaves Edwin's own rules as the only thing
outstanding.

**And a genuine unblock.** There are only ten test tickers today, which is why the
market maker cannot be tested against live games. tZERO will supply a full replica of
all of them, so a change such as quoting five price levels instead of three can be
tried out during real games with no effect on users.

**Still escalating:** the Sport Radar college-football futures endpoint is still
broken, Cody has written twice with no reply, and his stand-in spreadsheet goes stale
in about five days. Also agreed: a daily report of every account that bought IPO
shares, and a freeze on app store listing changes until the app-store-optimisation
kickoff.

## 2026-08-17: The weekend was better, and the economics got sharper

Digested [[17-08-2026-touchdown]], five days before the offering. Calmer than
Friday and considerably more useful: Edwin spent most of it specifying fixes
rather than questioning the enterprise.

**He separated the two dates, and the second one is the real bar.** The offering
on the 22nd is survivable. Trading starts on the **29th**, and _"we still need
quite a bit of ground to cover before the 29th"_. Plan the polish against that.

**The commercial position, stated soberly rather than angrily.** Signups at 154,
fewer than a simulation he ran himself two years ago on a $25,000 spend. The venue
has moved from free to $20,000 a month for the simulation and $150,000 for
production, and the original deal gave them a share of advertising revenue that no
longer exists. He expects 5,000 to 10,000 users at best, a couple of hundred of
whom might convert, which puts acquisition near $4,000 a head. His conclusion:
this iteration is a loss.

**Two structural points worth more than the numbers.** More users currently makes
the economics worse, not better, because there is no way to monetise them and
every additional user is another person to pay out. And production needs
committed external market makers, or it needs $25 to $30 million of Edwin's own
capital across roughly fourteen teams, which he described as outside his zone.

**The market-maker retune is the most specific direction he has ever given.** His
diagnosis of the weekend was that the book was "like cement", too tight to the win
probability for anyone to trade around. The prescription: widen the spread to
eight to twelve ticks, cut the maker's resting size from around ten thousand to
between five hundred and three thousand, and let the taker cross with up to five
thousand through multiple price levels. The point is to knock out the touch so
real users resting near the top of book actually get filled.

**The subtlest request is the best one.** Sportradar's win probability lags the
score by up to ten seconds after a touchdown, which is an exploitable asymmetry:
users can see the score before the market does. His fix is to sample the score as
well, apply a dollar value per point, and move the price immediately as a
placeholder that lasts only until the next probability arrives. He is deriving the
per-point values from data going back to 1999 and will supply them this week. It
means the market maker now has to consume play-by-play, not just probabilities.

**Three things before Saturday:** a three-way competition choice on first open, a
deliberately thin buy-only offering page with the sell control locked and
explained, and a surface reduction across the app. On that last one Edwin was fair
about how the clutter arose: the app was built with many surfaces because the plan
assumed advertising inventory needing places to live, and with no advertisers that
rationale has gone.

## 2026-08-17: The night that nearly ended it, and the diagnosis that did not

Digested [[14-08-2026-touchdown]], the morning after the first live game night
and the most consequential call in the record.

**Edwin questioned whether the product can launch.** His words: the worst trading
experience he has had, a failure at every touch point. He is due to commit
$800,000 to $1,000,000 to marketing and said he cannot do it against what he saw.
He put his position at $6.6 million and said he believes it is impossible to be
ready for the football season. He was clear this is not quitting and equally
clear he has to decide what more he funds. **Two more live runs were agreed
before any decision. The funding question is deferred, not resolved**, and it
stays live at every weekly review until he closes it.

**The diagnosis is the part worth holding on to.** Troy placed the fault away
from the back end and had the venue's own numbers behind him: **3 million orders,
1 millisecond average latency, no degradation of the matching engine**. His
conclusion was that the harder part already works and what is left is the
interface and the data ingestion. George's framing, that the work sits on the tip
of the iceberg rather than beneath it, is what turned an existential question into
a defined front-end workload. Those are very different things to manage.

**What actually went wrong is coherent.** The app was built to protect people
from mistakes, with a confirmation step and page transitions that each cost about
a second. The people testing it were trading at speed, and a trader who loses a
second loses the market. Confirming a trade navigated away from the game, five
screens deep in Cody's case. The order book disagreed with the order ticket, so
Troy kept missing the market. And no market order existed, so some trades could
not be placed at all.

**Edwin then specified the fix rather than describing it.** He walked through his
own prototype's trading model while trading a real market on another monitor: a
one-click toggle on the trading surface itself and explicitly not in settings,
buy and sell on every page with position and P&L carried across, one-click
flatten, market and join-bid and mid and ask as one-tap choices, and a hover
confirmation rather than a screen takeover. Captured in
[[one-click-trading-requirements-aug-2026]], including the tension it creates with
the fat-finger guard he praised five weeks earlier.

**Two reversals.** **Gamecast was downgraded by its own strongest advocate**:
informative, but not an edge you can trade on. And with no advertisers signed,
**the subscription is now the only revenue path**, which makes the strategy lab
the product rather than a feature. He demonstrated it returning about $1.1 million
across 138 teams on a single rule, profitable on 129 of them, with one parameter
change moving the result from $93,000 to $1.3 million.

## 2026-08-14: The engine runs, and the front door is the problem

Digested the [[12-08-2026-touchdown]], filed the [[11-08-2026-icp-offer-workshop]]
as the source record for the advertising pack, and captured written
[[jared-trading-feedback-aug-2026|Jared's feedback from a real trading test run]].

**The market maker and taker are running continuously.** Twenty-four hours
across all 180 books, two-sided quotes on every one, roughly 1.2 million orders
in a day. The guard rails are working in live conditions: the venue's price band
rejects anything 30% out, and a journal divergence on one book quarantines that
book alone. One irritation to fix at source, the venue seeds stale resting
orders each morning and we currently walk the price up to clear them.

**The front door is now the risk, not the engine.** Edwin expects to lose half
or more of downloads at the sign-up wall and has watched family members refuse
outright. Part of that fear turned out to be a version confusion, since the
store build already starts with an email address and gates verification to cash
prizes, but the underlying point stands and was backed independently by Jared:
people download the app and do not know what they have downloaded. Edwin's four
questions for the first screen are recorded in
[[customer-onboarding/customer-onboarding]]. tZERO have also said the 18-plus
requirement can come off.

**Advertising works and Edwin does not like it.** The units serve in the store
build and are deliberately off in TestFlight so nobody clicks one by accident.
His reaction to the creative was that it would turn him off the app, so the
direction moves to a top or bottom video unit rather than in-content banners. A
former FIFA commercial lawyer is being engaged for direct brand deals, and
Edwin would rather run no advertising than fight ugly programmatic inventory.
The volatility-moment unit is now settled as direct-buy only, because a custom
unit of that shape cannot be filled programmatically.

**A date correction that changes the plan.** College football starts on 29
August, but no media outlet covers college football. The date that matters for
coverage and first impressions is **9 September**, the NFL opener.

**And one defect worth the attention.** A real trading session produced fourteen
items, three of which are the same problem: the price shown is not the price you
can transact at. P&L is permanently wrong, the chart drifts from the book, and
limit orders will fail in ways a retail user cannot diagnose. It is the
strongest argument yet for the market order landing before real users arrive.

## 2026-08-10: Five touchdowns digested, and a new Compliance section

Processed the 27 July → 7 August touchdown block ([[27-07-2026-touchdown]],
[[29-07-2026-touchdown]], [[31-07-2026-touchdown]], [[03-08-2026-touchdown]],
[[07-08-2026-touchdown]]). Three weeks of calls, two weeks from the IPO.

**A new [[compliance/compliance|Compliance]] section.** The regulatory
constraints had been scattered through meeting notes; they now have a home, with
[[compliance/regulatory-positioning]] (the securities-not-gambling argument, the
SEC filing and gun-jumping risk, Rule 255, the Kalshi litigation, state-by-state
exposure) and [[compliance/eligibility-and-age-gating]] (who may hold which
account and what they may win). Eight live build constraints are listed, from
"never say regulated by the SEC" to "non-KYC users only see under-18-safe ads".

**Onboarding is now three tiers, not one.** KYC was killing the funnel, and
international students can never qualify for cash anyway, so
[[customer-onboarding/customer-onboarding]] splits into **Trader Full** (US tax
resident, 18+, full KYC, cash prizes), **Trader Medium** (international, KYC'd,
no cash) and **Trader Light** (email only, 13+, no cash). Everyone can trade —
it is a simulator. One hard blocker: tZERO's onboarding API still demands a
DOB of 18+, so Trader Light cannot be allocated a wallet until they relax it.
Ahead of all three sits Edwin's non-negotiable **first-open explainer and fork
screen**, because today a referred user's first sight of the app is a stadium
picture that explains nothing.

**The IPO's market structure is settled.** [[ipo-module/ipo-module]] and
[[market-maker/market-maker]] both re-based: a **broker-dealer MPID** holds and
sells the whole **1,000,000-share-per-team** issuance, and the **taker algo
buys ≥600,000** of it with randomised sizing and timing, purely so that no team
visibly fails to sell. The maker never touches the primary. NCAA opens for five
days, NFL for two, and the load-balancing algo is dropped until the NBA in
October. Prices publish early via OTA and **freeze three days out**.

**The valuation chain is confirmed end to end.** The Sport Radar probabilities
contract amendment is signed at no extra cost and live in production, closing
the S1 blocker that had no input at all. We poll at **500ms in-game**; the RP
formula gained its missing term (the in-game leg is a **delta from the kickoff
probability**, not the raw probability). Edwin also settled a real design worry:
the MM dragging price back toward the reference price is not a bug, it is how
every market works.

**Trading works end to end** into tZERO, with fills, partial fills, shorts and
notifications ([[trading/trading]]). The **Android app is live**. AdMob is
serving, with an SSP ladder capped at three networks and **Kochava** picked as
the MMP. **Avalara** is chosen for W-9 handling; the payout processor is still
the open gap. The app has been restructured into Teams / League / Schedule /
Games tabs with a live order book on the team page.

**Flagged for focused sessions, not written here:** micro-challenges and private
leaderboards for universities and frats; the strategy **back-test lab**; and the
**analyst portal** that the empty Analyst tab needs.

## 2026-07-30: SNT-1 Synthetic Noise Taker

Edwin introduced a **second house agent** for the Challenge and sent a spec-quality reference implementation, now processed into the market-maker component: [[market-maker/systems/synthetic-noise-taker]] (code safe-copied to `sources/snt1_noise_taker.py`).

SNT-1 is a **taker-only, non-participant house account** that crosses the bid/ask with random sizes at random times, so **every team book shows real trading from IPO onward, even with no games on**. It is deliberately a **controlled loser**: the spread it pays is the subsidy that seeds an active secondary market. It earns no leaderboard credit, and its prints against the Market Maker carry no participant side, so they fall outside the $2.50 off-field volume split automatically (no spec change needed). The realism layer mimics retail disposition-effect profit-taking, conditioning only on its own cost basis so the flow stays uninformed.

Processed per the market-maker working guide: the [[market-maker/market-maker]] hub now lists two house agents (MM + SNT-1), with decisions, parameters (all proposed, two tuning levers flagged), open questions (E17/E18 for Edwin, N15/N16 for us: the ExchangeAdapter build and five production-hardening tasks), a session note, and glossary/learnings entries all updated. The main open item Edwin flagged is how SNT-1 interacts with the MM's quoting and inventory during the IPO Primary Mandate rounds.
## 2026-07-29: AdMob Ad-Unit IDs + Central ID Registry

Captured the AdMob ad-unit IDs and started a **central ID registry** for all ad-monetisation identifiers: [[ad-network-ids]] (source HTML safe-copied to `components/advertising/sources/`).

AdMob is fully populated: publisher `pub-2057484236798641`, the iOS and Android app IDs, and all eight ad units (three Native-advanced sizes, inline / MREC / strip, plus an inline Banner, mirrored per platform), along with the app-ads.txt line. The registry is a living doc: as SSP seat IDs and further ad-unit IDs are issued, they get added here so there is one place to query every publisher, app, ad-unit and SSP ID. Linked from [[advertising]] and the [[programmatic-media-playbook]].

## 2026-07-29: IPO Pricing Model v1.0

Edwin delivered the **IPO pricing model** for the 2026 season, now stored safely in the vault and processed: [[ipo-pricing-2026]] (source workbook safe-copied to `components/ipo-module/sources/`).

It sets the **listed IPO price for every tradeable team company**, all **32 NFL** and **138 NCAA** teams, from a clear formula: **IPO = $5.00 x E[Wins] + $2.50 x E[Ties] (NFL only) + $2.50/game x expected volume-capture share**. The on-field leg comes from devigged BetMGM win totals; the off-field leg from a Popularity Index (0.6 x brand + 0.4 x performance) with Bradley-Terry per-game capture. Prices range from about **$81 (LA Rams)** down to **$21 (Charlotte)**. The doc also captures the parameters, the methodology, and the author's caveats (notably the North Dakota State / Sacramento State non-universe pricing, and that supplying the exact 2026 schedule CSV will move NCAA prices by ~$1 to $2).

This fixes per-share IPO value; the remaining open variable is float size (shares issued per team), tracked in [[open-questions]]. The $5/win, $2.50/tie and $2.50/game accruals are the same [[earnings-report]] settlement mechanics, so the IPO price is the expected sum of every future earnings distribution.

## 2026-07-29: tZERO OMS Q&A + Risk Settings

Processed Rob Colucci's (tZERO) written answers from a QA testing session, plus the IPLY OMS risk-settings spreadsheet, into the vault ([[29-07-2026-tZERO-rob-qa]]; matrix in [[tzero-oms-risk-settings]]; digested into [[tzero]] §11).

**Fixed live in the session:** account-scoped position tracking (positions had been aggregating at the firm level because test accounts used TEST-environment credentials; the credential routing was corrected), and ticker `IPTCCONH` (was missing from OMS SIM, now created).

**Answered:** IPLY accounts carry positions overnight by default; bid/ask is driven by FIX orders with a market maker setting the market (no pre-set price list); UEPR/UEAR are enabled but there is no bulk position query, so EOD reconciliation needs a dedicated session. This also closes two 23-07 open items: the OMS has **Stop Wash Trades ON** (the self-match prevention the market maker needed), and the **risk-settings matrix** Rob owed has been delivered. The matrix's **limit-price-range tiers** give the market maker its OMS-level price band to reconcile against.

**Primary issuance:** the OMS can seed an IPO reference price, but tracking capital raised and shares remaining needs a **dedicated cap-table management tech stack**, which sits alongside the 23-07 direct-mint decision. Selecting that stack is a new open item.

## 2026-07-24: Meeting-Notes Batch Digested

Processed the 22 Jul touchdown, the 23 Jul tZERO weekly tech sync, the 24 Jul touchdown, Jared Sapirman's written app feedback, and two subscription/research source docs into the vault. (The 20 Jul touchdown and 23 Jul market-maker follow-up were already processed and are not repeated here; the market-maker component already owns that material.)

**Subscriptions priced.** Research and Watch/Pro-View at $49.99/mo each, bundled "Pro Trading Package" at $79.99/mo (ads still run on those surfaces). This resolves the long-open [[research-tab]] pricing question and supersedes the earlier tiered headline. See [[22-07-2026-touchdown]].

**IPO issuance decided.** Bypass the Matching Engine and mint tokens straight to investor wallets via tZERO's transfer-agent workspace (single-price, long-only primary raise); Novo needs minting access. The tZERO environment also splits into SIM (the current one) plus a new PROD, with production symbology decoupled from team names and a $1.20/share short fee. See [[23-07-2026-tZERO-weekly]].

**Also on 22 Jul:** a W9 tax-automation vendor jumps the backlog to be ready for the 29 Aug first games; education adds AI-clone persona videos and an in-app "how to use the app" piece; SSP onboarding is gated on the live App Store URL.

**Jared's feedback folded in** ([[jared-app-feedback-jul-2026]]): contact-permission referral invites, a ~2s cold-start target (down from ~4s), public usernames with anti-impersonation guardrails, and a social-layer direction (Groups & Leagues, influencer-hosted groups, richer streaks) plus a Dynamic Island presence, flagged for a focused session.

**Subscription pricing + research reports** ([[research-tab]]): two source docs fold in a four-tier pricing ladder (Free trial / Plus $24.99 / Pro $49.99 / Elite $79.99) and the first concrete pre-canned report catalog. The tier prices are a proposal under review, not locked: the strategy doc itself calls $29.99 the "optimal" Pro launch price and the middle tier is floated at $34.99–$39.99. Research/subscriptions are not a launch feature (target ~October), though the research piece is wanted within 1–2 weeks so influencers can talk about it.

**24 Jul touchdown** ([[24-07-2026-touchdown]]): ad serving moves to the live path (AdMob verifying now the App Store ID has landed, first SSP imminent, Google Tag Manager + an MMP decision); the Sport Radar feed-speed question is settled by necessity (custom Gamecast runs off the media feed since the betting feed is inaccessible, probabilities-API fixes being chased); trading infra is fully mapped and testable via historical-game simulations; payouts and tax forms get a delay-payout launch fallback; the KYC-less variant is parked to September; and a new guest-analyst "Analyst Prices" page was requested.

## 2026-05-17 — App Build Complete (Mock Data Phase)

The InPlay Trading Challenge mobile app now has all 20 screens built with full mock data. Every screen described in the vault sub-component specs is implemented, navigable, and styled to production standard. The app is ready for stakeholder review and user testing on-device via Expo Go or EAS builds.

### What's been built (May 12–17)

**Core Trading Screens**
- **Single Game Page** — the heart of the app. Head-to-head matchup, live match tracker (pre-game/live/post-game states), annotated price chart with time ranges, order book depth, embedded buy/sell, news feed, mini leaderboard widget
- **Portfolio** — all open positions with unrealised P&L, wallet balances, quick links to orders and history
- **Trade Confirmation Flow** — order entry → confirmation → placed screen → cancel order
- **Position Detail** — per-team position view with entry price, P&L, trade history

**Discovery & Research**
- **Discovery Feed** — horizontal game ticker, game cards with sparklines, NFL/NCAA filter, search with type-ahead across 163 teams
- **Team Page** — season price chart (candlestick), expandable season stats, division standings, schedule with results, injury report, player spotlight, team news, user's position P&L
- **Player Profile** — biographical data, position-specific stat tables, injury status, headline stats grid. Navigable from Team Page and Single Game Page
- **Full Results** — complete season game history per team
- **Full-Screen Chart** — expanded candlestick view (modal slide-up)

**Competition**
- **Leaderboard** — 3 verticals (Best P&L, Risk-Adjusted, Comeback) × 4 time horizons (Daily, Weekly, Monthly, Full Event). Gap-to-earn as the hero metric. Brand glow header (green = earning, red = not). Auto-scroll to user's position
- **Trader Profile** — public profile of other traders with performance stats

**Supporting Screens**
- **Dashboard (Home)** — wallet balances, ranking summary, proximity indicator, upcoming games
- **More tab** — Referral program (Get 1,000 / Give 500), Education hub, Settings
- **Wallet Details** — balance breakdown and transaction history

### Design System
- Dark mode default with full theme token system (colors, spacing, typography)
- Reusable component library: Card, FilterChips, SearchBar, StatusBadge, PriceIndicator, SectionHeader, ScreenGlow, GridBackground
- App-wide grid background at root layout level
- Standardised back gesture across all tab stacks
- Mobile-first — optimised for phone, consumer fintech aesthetic (not terminal UI)

### Mock Data Coverage
- 32 NFL teams + sample NCAA teams with realistic pricing
- 109 player profiles with position-appropriate stats
- 59 news items across team, game, and league categories
- Season candlestick data for historical charts
- Fake leaderboard with distinct data per vertical
- 8 trader profiles for leaderboard drill-down
- Order book depth data
- Portfolio with multiple open positions and P&L

### Product Documentation
- **[[product/pages/PAGES|App Pages]]** — complete screen map with descriptions and navigation flows (new)
- **Design system rules** added to CLAUDE.md — "change globally, not locally" principle
- **Sportradar data mapping** — confirmed all sub-component data requirements can be fulfilled by NFL/NCAA Player Profile, Team Roster, Game Summary, and Weekly Injuries endpoints

### Key Decisions
- No player images in app (requires separate NFLPA licensing) — jersey number badges used instead
- Player IDs are slug-based (`kc-patrick-mahomes`) for mock phase; will use Sportradar UUIDs in production
- Gap-to-earn is more prominent than rank number on leaderboard (per spec)
- 3 data points max per game card on Discovery (per spec)
- Bottom padding pattern (180px) on screens with floating trade button to clear tab bar

### What's Next
- Stakeholder review / on-device testing
- Backend integration planning (WebSocket for real-time prices, REST for user actions)
- State management library selection
- Authentication and KYC flow implementation

## 2026-05-14

- **Onboarding + Referral + Global Website extracted** from [[12-05-2026-onboarding-and-renewal-and-global-component]]
- **[[components/customer-onboarding/customer-onboarding|Customer Onboarding]]** — full 10-section component doc. Status `Collecting` → `Defined`. 5 sub-components surfaced: Discovery & App Acquisition, Registration+KYC, Wallet Provisioning, Holding State, Returning Login
  - Key decisions: registration and KYC happen as one step; tZERO owns auth credentials (SSO parked); cash wallet on tZERO chain (sidesteps store-of-value licensing); pre-funded wallet pool agreed in principle (pending tZERO cost); holding state UX is "gray out, never hide"
- **[[components/referral/referral|Referral]]** — full 10-section component doc merging vision content with new transcript. Status `Collecting` → `Defined`. 7 sub-components surfaced: Code Lifecycle, Share Surfaces, Bonus Campaigns, Cash Eligibility Tracking, Social Engagement Credits, Sponsor Redemption, Donor/Group Accounts (exploratory)
  - Key decisions: lifetime-stable codes; "Get 1,000 / Give 500" in orange on every surface; QR + dot card + t-shirt strategy; embedded-post QR mechanic; transparent eligibility checklist (no hidden T&Cs); cash eligibility rules owned here, surfaced at withdrawal moment
- **[[components/inplay-global-website/inplay-global-website|InPlay Global Website]]** — short summary + action list (design is in flight). Status `Collecting` → `In Design`
  - Multisport positioning locked; hero tagline "Trade sports as stocks. Buy, sell, hold — every play, every game, every season."; pages prioritised (Home / About / Advertising); Newsroom + Markets hidden; light-mode toggle to add
- **New component:** **[[components/withdrawal-flow/withdrawal-flow|Withdrawal Flow]]** (stub) — bank info + crypto wallet + 1099 captured at first withdrawal (not signup). Needs dedicated session
- **New cross-cutting concerns:**
  - **Analytics & Funnel Measurement** — end-to-end CTA tracking (social engagement → ad → install → onboard → first trade → referral conversion → LTV)
  - **Cybersecurity & Data-Handling Framework** — Troy flagged dedicated architecture session needed (PII from Persona, biometrics, location data, bank info)
- **[[audiences|Canonical audiences doc]]** created — 4 audiences (Crypto-Savvy Sports Trader, Analytical Fan / Armchair GM, Finance-Curious Student, Veteran Trader-Bettor). Brand-entity audience work merged with vision content. Audience #4 (Edwin's profile) added. Vision Section 2 refactored to link to canonical doc
- **Terminology fix:** "persona" now refers exclusively to the KYC vendor (Persona). User types are called "audiences"

## 2026-05-09

- **Information Layer fully documented** -- component doc with all 10 sections complete, plus 6 sub-components with entity journeys, acceptance criteria, data requirements, and dependencies
  - [[single-game-page]] -- the core convergence screen, 3 journeys defined
  - [[leaderboard]] -- 3 verticals, 4 time horizons, proximity alerts, 3 journeys defined
  - [[discovery-home]] -- app entry point, search, game cards, 3 journeys defined
  - [[team-page]] -- research dashboard, historical data, live enrichment, 3 journeys defined
  - [[game-day-overview]] -- multi-game monitoring, aggregate P&L, 3 journeys defined
  - [[research-tab]] -- placeholder only, 10 questions for next call
- **Sub-component template updated** -- entity journeys now split into 3a (isolated) and 3b (cross-component) with handoff points and integration contracts
- **Vault restructured** -- `content/` renamed to `vault/`, full directory skeleton in place for all 8 components + architecture
- **Component placeholders created** -- all 8 components have directories and entry-point docs with key elements from the vision workshop

## 2026-05-06

- **Vision document extracted** from 2-hour workshop session with Edwin, Cody, Troy, Skye
- **Component map created** -- 9 components identified, all in Collecting status
- **Three personas defined** -- Young Aspiring Trader, Sports-Passionate Casual, Experienced Trader
- **Cross-cutting concerns identified** -- Advertising, Push/CRM, Personal Dashboard
