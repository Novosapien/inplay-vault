# InPlay Trading Challenge — Vision

> **Client:** InPlay (Edwin Johnson, Kevin "Cody" Murray, Skye Capazorio)
> **Date:** 2026-05-06
> **Status:** Draft
> **Owner:** George Westbrook
> **Sources:** [[Meetings/06-05-2026-vision-workshop]]

---

## 1. What Are You Building?

**One-liner:** A simulated sports equity trading challenge where users trade team stocks during live NFL and college football seasons — no financial risk, real cash prizes.

**Detailed narrative:**

### The Asset Class

- InPlay creates actual public companies for each NFL and D1 college football team
  - Real corporate structure — board of directors, reporting obligations, corporate services managed by InPlay
  - 32 companies for NFL, additional for college football
- Each team company IPOs at a forward-looking price based on:
  - **On-field value:** projected wins × revenue value per win (e.g., 5 expected wins × $5 = $25/share)
  - **Off-field value:** expected marketing/advertising revenue driven by user engagement with that team's stock
- After IPO, shares move to a secondary market where buyers and sellers freely determine price
- At season end: companies close, perform a liquidating dividend — all earnings distributed to shareholders as cash
  - No tax at corporate level
  - Shareholders receive capital gains/losses treatment (losses are tax-deductible, unlike gambling)

### Core Mechanic: Path-Dependent Trading

- Trading is **path-dependent, not outcome-dependent**
- The price path during a live game creates hundreds to thousands of trading opportunities per play
- Examples of price movement:
  - Team wins but star player injured → share price drops despite the win
  - Team beats a strong opponent, rookie QB looks like a star → market prices shares at $8–9 instead of $5 per win
- Price driven by market forces (where buyers and sellers meet), not binary outcomes
- Nobody has to lose for someone else to win — if InPlay drives enough marketing revenue, every team's shares could increase even if they lost every game
- Single liquidity pool with single source pricing — InPlay becomes the reference price for the entire sports trading market

### The Trading Challenge (Simulation)

- Users receive 100,000 InPlay dollars on signup — no real money at risk
- Trade team stocks in real time during live games:
  - Buy, sell, go long, go short
  - Strategies: momentum, volatility, reverse momentum (providing liquidity when others sell), microstructure/flow trading, buy-and-hold (up to two or three weeks)
- Previous simulations: users traded 4 hours straight without logging off
- Season-long challenge with tiered prize pool: $5M–$25M total in real cash
- ~$200–250K distributed per day in prizes

### Competition Structure

- Three daily competition verticals:
  - **Best P&L** — who made the most money today (pays down to ~400 places, top prize ~$10K/day)
  - **Best risk-adjusted return** — smoothest upward P&L line (rewards disciplined risk management)
  - **Comeback trader of the day** — biggest recovery from deepest drawdown
- Leaderboards run across:
  - Daily, weekly, monthly, and full-season timeframes
- Major event days (e.g., Thanksgiving — 3 NFL games): $1.5–2M distributed, hundreds of thousands of potential winners
- Users always have something to compete for if they trade properly — not just a single winner-take-all

### Referral Wallet Mechanic

- Separate wallet from the active trading wallet
- Dual-sided referral: 1,000 InPlay dollars to referrer, 500 to referee (triggered on KYC completion)
- Referral wallet has no cap (influencer with 1,000 referrals could have $1M in referral wallet)
- Can only reload trading wallet back to 100,000 when it drops below 25,000
  - Can never exceed 100,000 in trading wallet
  - Creates safety net proportional to referral activity without unfair trading advantage
- Social media engagement earns InPlay dollars into referral wallet (following, commenting on InPlay social posts — LinkedIn, Facebook, Instagram, TikTok)
- Sponsor redemption: InPlay working with sponsors so users with large referral banks can use referral dollars for special offers with sponsors
- All referral balances reset to zero at end of season
- Summer pre-launch referral program:
  - Pre-sign up before August to build referral bank early
  - Bonus multiplier days (e.g., Fourth of July = 2,000 per referral instead of 1,000)
  - Leverages natural social gathering moments for viral growth

### Onboarding Flow

- Landing page or app store → download mobile app → sign up form → KYC via Persona
- KYC validates: age 18+, real identity, no bots, US citizenship (if required)
- On KYC approval:
  - 100,000 InPlay dollars credited to trading wallet
  - Auto-generated referral code tied to account
  - User can immediately share code via any channel

### In-App Surfaces

- **Personal dashboard (homepage):**
  - Current money, referral bank balance, rankings across all three verticals
  - Proximity indicators: "you're 112 places away from cashing"
  - Live schedule feed — upcoming games answering "when is my next opportunity to make money?"
  - College football plays 6 days a week, not just Saturdays

- **Game page (live):**
  - Live match tracker
  - Interactive price charts for both teams
  - Real-time stats
  - Trade execution interface

- **Team pages:**
  - Historical performance data
  - Upcoming matchups
  - Player stats
  - Team price chart
  - Powered by Sport Radar historical data

- **Favourites/following:**
  - Follow teams without holding shares
  - Blends fandom with trading
  - Scores, stats, game tracking
  - Increases time-in-app for advertising metrics

### Information Layer (Bloomberg Terminal-Style)

- **News feed:**
  - AP-style editorial newswire from Sport Radar
  - Player news, injuries, free agent signings, team news
  - InPlay proprietary market data news
- **Market data:**
  - Best bid, best offer, last traded price
  - Order book depth (how many orders at each price level)
- **Large block trade alerts:**
  - Anonymous: "a large block traded at this price at this time"
  - Pushed to socials and in-app feed
  - Creates market transparency and content

### Education Module

- Planned basic trading education — "what's a buy, what's a sell, momentum trading, how do you trade some volatility"
- Edwin: "at a 40,000 foot level. Not narrowed into any of the more granular detail"
- Full education on all facets for all traders, including people who "have no idea how to buy or sell yet"
- InPlay positioned as a financial literacy tool — skills transfer to traditional equity markets
- Edwin: "people may start trading on sports, but then they're like, 'Oh, I understand how equity markets work. I'm also going to trade on transport stocks or medical stocks'"
- Scope and delivery (in-app vs website) still to be defined

### Continuous Pricing Model

- Pricing doesn't shut down after a game — runs throughout the entire season
- Liquidity providers at all prices, for different reasons, at different stages of every game
- If a game doesn't go your way, you don't lose all your money — just some value
- Much easier to trade volatility compared to prediction markets
- Keeps users in the market rather than shutting them out after a single game result

### Community Layer ("The Third Space")

- Share executed trades (long/short positions)
- Strategy discussion and fandom chat
- Designed as stickiness and social proofing function — not the core product
- Enables organic education through peer learning
- Can create meme-stock-style herd dynamics (mirrors real equity market behaviour)
- InPlay provides marketplace infrastructure, does not curate or summarise community sentiment
  - Avoids liability from bad actors using sentiment manipulation

### Push Notifications & Communications

- CRM-driven outreach creating touchpoints outside active trading sessions
- Specifics of timing, content, and branding still being defined
- Potential for sponsor branding within push notifications

### Advertising Experience

- **Not static display — interactive, moment-based:**
  - Sponsors own specific games (e.g., Ohio State–Michigan)
  - Sponsors own volatility moments (touchdowns, interceptions)
  - Sponsors own specific pages or surfaces
- **Targeting capabilities:**
  - Geo-targeted (within 3 miles of a location)
  - Demographic-targeted (e.g., 25–35 year olds only)
  - Time-targeted (e.g., 30 minutes after game ends)
- **Vision:** Users associate brands with memorable trading moments
  - "I was offered Doritos during that touchdown"
  - "I got a Door Dash offer right as the game ended"
- This model doesn't exist anywhere else in sports media today
- Inventory model and packaging still being defined (tier structure vs. à la carte)

### Owned Media Layer (Future-State)

- Interviews with top traders
- Podcasts, broadcasting
- Content created from platform activity
- Distributed through InPlay's own channels
- Additional interaction points offered to advertisers

**Form factor:** Mobile app (primary). Web landing pages for the trading challenge and InPlay Global (secondary — registration funnel and brand presence). KYC and trading happen exclusively in the mobile app.

**Scope boundary:**
- **This IS:** The InPlay Trading Challenge — a simulated trading environment with no real money at risk, real cash prizes funded from a prize pool, running for the NFL/college football regular season.
- **This is NOT:** The production trading exchange (live trading with real money through broker partners and T0 as ATS). Production is the downstream destination; the challenge is the funnel into it.
- **This is NOT:** Sports betting. There are no odds, no bookmaker, no house edge. Users trade against each other on a secondary market, not against InPlay.
- **This is NOT:** A prediction market. Outcomes are not binary. Pricing is continuous across the season, path-dependent, and driven by market forces — not game outcomes alone.

---

## 2. Who Are You Building It For?

Edwin's overall target: "an 18 to 55 year old who loves sports and wants to try to make some money engaging with it." He explicitly resisted narrow segmentation: "I don't think it's just students. I don't think it's just graduates. I don't think it's people just with a college education." The three personas below are inferred groupings based on the different motivations and behaviours discussed — not hard segments from the transcript.

### Persona 1: The Young Aspiring Trader (18–25, inferred)

- **Demographics:**
  - College-aged — students and recent graduates
  - Includes international students (Taiwan, Vietnam, China, India seen at Ivy League campus tours)
  - US-based primarily, potentially global (pending regulatory confirmation)

- **Psychographic profile:**
  - Wants a career in finance or believes they can build wealth through trading
  - Sees trading as a skill to develop, not just a gamble
  - Familiar with meme stocks, Robinhood, phone-based risk-taking
  - Part of the generation that's comfortable with mobile-first financial products

- **Current behaviour:**
  - May sports bet casually
  - Follows sports closely
  - Doesn't have the capital to trade real markets
  - Edwin's own experience: "one guy told me if I had 50 grand, he'd let me trade with him. I didn't have 50 grand"

- **Motivations:**
  - Financial upside matters most to this group
  - Building real financial literacy — learning how equity markets work through sports they understand
  - Edwin: "the benefits over time to a younger person probably are a little bit greater than an older person"
  - Potential career pathway into finance

- **Needs:**
  - Zero cost to enter
  - Real emotional stakes without real financial risk
  - Basic education on trading mechanics (buy, sell, momentum, volatility)
  - Mobile-first experience available during evenings and weekends

- **Wants:**
  - Leaderboard recognition
  - Cash prizes
  - Transferable trading skills applicable to traditional markets
  - Community to learn from peers

- **Pain points with current alternatives:**
  - Can't access real markets without significant capital
  - Prediction markets and sports betting are structurally losing propositions (85% of retail lose money)
  - No risk-free way to develop trading skills with real emotional stakes
  - Traditional market simulators have no skin in the game — "you were completely disassociated"

- **Switching trigger:**
  - Free entry with real cash prize potential
  - Genuine skill development that transfers to traditional equity markets
  - An asset class they already understand (sports) with familiar trading infrastructure

---

### Persona 2: The Sports-Passionate Casual (25–45, inferred)

- **Demographics:**
  - Broad income and education range — truck drivers to office workers
  - Not necessarily finance-educated
  - Knows football deeply
  - Edwin: "I want to reach truck drivers who really know football and don't have a way to express that other than gambling"

- **Psychographic profile:**
  - Sports is identity — watches every game, has strong opinions on matchups and players
  - Currently channels sports knowledge into betting
  - May see themselves as sharp or "in the know" relative to casual fans
  - Wants a way to profit from what they know without feeling like they're gambling

- **Current behaviour:**
  - Sports betting (US lost $15B legally in 2025, much more illegally)
  - Some dabble in prediction markets but find them confusing or frustrating
  - Edwin on Polymarket: "you get liquidity at really s***** prices when you need it"
  - Spends significant time watching and analysing games already

- **Motivations:**
  - Wants to profit from sports knowledge without predatory bookmaker mechanics
  - Wants to feel ownership (shares vs bets)
  - Wants to be part of the action during games — evenings and weekends
  - Competitive drive — wants to prove their sports knowledge has real value
  - Edwin: "We want people who are losing money, betting on sports to come into play and I'm not going to risk my own money on sports this fall. I'm gonna compete here and try to learn a different skill on how to profit from the things I know and love"

- **Needs:**
  - Simple enough to start without trading background
  - Real-time engagement during live games
  - Ability to trade based on sports knowledge (not just financial technicals)
  - Fair playing field — not stacked against them like sports betting

- **Wants:**
  - Cash prizes for their sports expertise
  - Community validation — sharing winning trades
  - Sense of ownership and longer-term position management (buy and hold for days)
  - A nuanced way to express views (e.g., "this team will improve over weeks") rather than binary bets

- **Pain points with current alternatives:**
  - Betting is structurally a losing game (10–40¢ lines, 5–15% house hold)
  - Prediction markets have bad liquidity at critical moments, 6–8% round-turn cost, binary outcomes
  - When games go against you in prediction markets, can't exit without giving up massive edge
  - No way to express a nuanced, multi-day view on a team's trajectory

- **Switching trigger:**
  - No cost to enter, real cash prizes
  - Sports knowledge translates directly into a tradable edge
  - Path-dependent pricing means you don't lose everything when a game goes wrong
  - Available during the hours they're already watching football

---

### Persona 3: The Experienced Trader (40–55, inferred)

- **Demographics:**
  - Has traded before — traditional markets, options, futures
  - Sports fan
  - Edwin's own profile is the closest reference for this persona

- **Psychographic profile:**
  - Edwin: "is the money as important to a person my age? Probably not as someone who's young"
  - Drawn by novelty of a new asset class and the challenge
  - Values discipline and risk management — the risk-adjusted return vertical speaks directly to them

- **Current behaviour:**
  - Already trades traditional markets during market hours
  - May bet on sports separately
  - Understands risk management, order books, momentum, microstructure
  - Evenings and weekends are currently non-trading time

- **Motivations:**
  - Novelty of trading a transparent, real-time equity where you can watch your stock play on TV
  - Intellectual challenge of a new asset class with familiar mechanics
  - Leaderboard competition — proving skill against a large field
  - Edwin: "a first of its kind asset class focused on something people love"

- **Needs:**
  - Sophisticated trading infrastructure (order book, bid/ask, price charts)
  - Real-time market data and news feed
  - Ability to deploy complex strategies (momentum, volatility, reverse momentum, microstructure)
  - Fair market with single liquidity pool and transparent pricing

- **Wants:**
  - Recognition via risk-adjusted return leaderboard (rewards their disciplined approach)
  - Bloomberg Terminal-style data experience
  - Large block trade visibility
  - Potential pathway to production trading as a new income stream

- **Pain points with current alternatives:**
  - Traditional markets aren't available during evenings and weekends
  - Sports betting doesn't reward trading skill — it's binary against the house
  - Prediction markets lack continuous pricing model and proper market infrastructure
  - No existing product combines their trading expertise with their sports knowledge

- **Switching trigger:**
  - A genuinely new asset class with familiar trading mechanics — order books, bid/ask, continuous pricing
  - Applied to something they're passionate about
  - Available in hours when traditional markets are closed
  - The most transparent equity market in the world — "there's no other company that you could turn on your television and watch firsthand"

---

## 3. Why Are You Building It?

- **Business opportunity:**
  - Sports risk-taking market is enormous and accelerating:
    - Legal US sports betting: ~$130B/year
    - Prediction markets (Kalshi + Polymarket): $90B traded through April 2026 alone, expected $250B by year end
    - "Huge epidemic in US with younger people betting on sports, thinking that's a way to make money. It's not. 2025, US lost $15 billion in cash betting legally on sports, much more illegally"
  - 3 key states (California, Texas, Georgia) haven't legalized sports betting — ~1/3 of the US underserved
    - Prediction markets filled that gap but have structural problems (binary, bad liquidity, 85% losing)
  - Meme stock generation normalized phone-based risk-taking
  - Natural migration path: betting → prediction markets → equity-style trading (InPlay)
  - No one else occupies the "path-dependent sports equity" space — first mover
  - The trading challenge is simultaneously product AND marketing — Skye: "the product intersection and a marketing inflection point meet in the trading challenge... we're turning the product utility into that marketing promotion opportunity, which is rare"

- **Client's motivation:**
  - Edwin is a long-time trader — built this from deep personal trading experience
  - Personal dissatisfaction with existing simulators drove the challenge design — Edwin traded on a sim after work: "learned how to hit the buttons and click and look at things visually, but emotionally how I would react, you were completely disassociated. So in building this challenge, I wanted that to be different"
  - Control their own distribution channel rather than depending on brokerage partners (Robinhood, Webull, Schwab) — Edwin: "I don't believe that they're going to provide us with the value we expect from them in turning on their clients. They can turn on the clients, but if they don't make it aware for their clients that this exists, it's not going to have the same bite"
  - Edwin: "InPlay is a marketing platform with a very specific product that hits an amazingly large and juicy demographic for advertisers that they all clamored for"
  - Target: 1–5M active users in the challenge → 20–40% conversion to production trading
  - Edwin: "there'll be a number of people who decide to trade inplay stocks for a living and not other things"
  - Financial literacy — addresses youth gambling epidemic, teaches real equity market mechanics that transfer to traditional markets
  - Skye: "try before you buy" — the challenge gives free access to trial trading risk-free before committing to production
  - Skye: the simulator could become an "always on premium access opportunity into production trading" beyond just the seasonal challenge
  - Skye: potential to integrate into college syllabus as an education tool — "increasing financial fluency within a youth market in a fun and engaging way"
  - Share of wallet strategy — Skye: "one of our biggest things is looking at share of wallet and being very clear on how we migrate people from their [current spend] into ours"

- **Cost of inaction:**
  - Not explicitly discussed
  - Implied: prediction markets (Kalshi, Polymarket) are capturing the sports trading audience now — delay risks them becoming entrenched
  - NFL season timing creates a hard deadline — summer referral program and August launch are time-bound
  - ⚠️ **Gap:** Ask Edwin directly: "What happens if you don't launch this season?"

---

## 4. What Makes This Better Than the Alternatives?

### Sports Betting (DraftKings, FanDuel, Bet365, etc.)

- **What they do:**
  - Binary wagers against the house on game outcomes and spreads
  - Mobile apps for in-game live betting
  - Regulated state-by-state in the US

- **Market context:**
  - PASPA ruling (2018) opened up state-by-state legalization
  - Currently 40 states + Washington DC allow legalized sports betting
  - Requires expensive licenses: $10–20M per state + significant revenue share (New York is ~50–51%)
  - 3 key states still without legal sports betting: California, Texas, Georgia — roughly 1/3 of the US underserved
  - In Europe, 88–92% of all soccer bets are placed in-game (shows where behaviour is trending)
  - Revenue pattern is clockwork seasonal: peaks in fall (NFL/NCAA football), spikes at playoffs/Super Bowl/NCAA basketball tournament, virtually dead June/July

- **What works well:**
  - Culturally embedded — everyone understands it
  - Mobile-first, instant gratification
  - Huge existing market ($130B/year legal US wagering)
  - Live/in-game betting growing rapidly

- **What doesn't work:**
  - Standard "10-cent line" (house edge), grows to 40-cent line for live/in-play betting
  - Hold percentage: 5–15% of all wagering goes to the house
  - Predatory — structurally designed for users to lose
  - US bettors lost $15B in 2025 legally (much more illegally)
  - Very seasonal — dead in summer, highly concentrated around football
  - You bet against the house, not against the market — "it's you against the book, not the book against the world"
  - Zero-sum: losers pay winners

---

### Prediction Markets (Polymarket, Kalshi, FanDuel CME)

- **What they do:**
  - Binary contracts on event outcomes (sports, elections, etc.)
  - Contract value moves between $0 and $1 based on probability
  - Users trade contracts against each other via a marketplace

- **Market context:**
  - Enabled by second circuit court ruling interpreting the Commodity Exchange Act favourably
  - Started with elections — used as stepping stone to get into sports
  - 90% of all prediction market trading is now on sporting events
  - Available in CA, TX, GA where sports betting isn't legal — captures the underserved third
  - Aggregate volume: $90B between Kalshi and Polymarket through April 2026
  - Expected to reach $250B through the year (haven't hit football season yet)
  - Multiple platforms creating fragmented liquidity: Kalshi, Polymarket, FanDuel CME, plus upstarts

- **What works well:**
  - Cheaper than sports betting: 6–8% round-turn cost vs 10–40% edge
  - Novel — attracts the meme stock generation
  - Available where sports betting isn't
  - Trading against a market rather than against the house

- **What doesn't work:**
  - **Binary outcomes** — contract goes to $0 or $1, no nuance
  - **Single designated market maker** (Susquehanna for Kalshi):
    - Their job is to provide liquidity for buyers and sellers
    - When games become one-sided, they widen spreads dramatically or pull liquidity entirely
    - Users can't exit positions at reasonable prices when games go against them
    - "People just end up wearing the position and become buy and holders or sell and holders and wait for the outcome because what's the difference of two cents to them"
  - **85% of retail users losing money** — "which you would think you've got a 50/50 chance until you bring in the fees and the cost and the spread and the lack of liquidity when you need it"
  - **Fragmented liquidity** across platforms — problematic for price discovery
  - **No regulatory framework** like SEC — no insured accounts, no SIPC
  - **Poor support** — Edwin's personal experience: $900 went missing on Polymarket, 28 hours to get a response, 4 days to credit his account. "That's a huge problem."
  - **No financial literacy transfer** — "if you trade prediction markets, you don't actually learn how to trade futures. There's no benefit on the educational front"
  - **Zero-sum:** losers pay winners, same as betting
  - **No sense of ownership** — making bets vs owning shares feels fundamentally different

---

### Traditional Markets (Robinhood, Schwab, Webull)

- **What they do:**
  - Equity, options, and futures trading on conventional securities (stocks, ETFs, commodities)
  - Regulated by SEC, accounts insured by SIPC up to $500K
  - Established trading infrastructure: order books, continuous pricing, market data feeds, research tools

- **Market context:**
  - These platforms are InPlay's future brokerage partners for production trading (Robinhood, Webull, Schwab)
  - $150/customer acquisition cost — shows how valuable each active trader is to these platforms
  - GameStop/meme stock era (worth $11B despite "worth nothing") proved retail traders can move markets and created a generation comfortable with phone-based trading
  - Edwin: "the meme stock generation has created a whole new layer. People are very familiar with their phone. They like taking risk on their phone"

- **What doesn't work:**
  - **Capital barrier to entry:**
    - Edwin: "one guy told me if I had 50 grand, he'd let me trade with him. I didn't have 50 grand"
    - Had to work until he could find a backer to put up money
  - **Market hours don't overlap with real life:**
    - Traditional markets close before sports start (evenings/weekends)
    - No way to trade when you're actually engaged and watching content
  - **Opaque — can't watch your stock perform:**
    - Edwin: "there's no other company that you could turn on your television and watch firsthand and see, okay, how is my stock performing today?"
    - You can't see your investment performing in real time
  - **No connection to passion economy:**
    - Sports fans have deep domain knowledge but no financial instrument to express it
    - Traditional markets reward financial analysis, not sports expertise
  - **Simulators fail at building real skills:**
    - Edwin's experience: traded on sim for 2 hours after work — "learned how to hit the buttons and click and look at things visually, but emotionally how I would react, you were completely disassociated"
    - No stakes = no habit formation, no emotional development
  - **Intimidating for non-finance people:**
    - Steep learning curve
    - People who "really know football" have no way to express that knowledge in traditional markets

- **Relationship to InPlay:**
  - InPlay is the training ground that feeds users INTO traditional markets
  - "Every person who trades in this challenge will be a better trader afterwards"
  - InPlay mirrors the infrastructure (order books, continuous pricing, market data) but wraps it in an accessible, entertaining, sports-driven experience
  - Brokerage partners will pay $150/account for qualified referrals from InPlay production users

---

### InPlay's Structural Differentiation

- **Path-dependent, not outcome-dependent:**
  - Price path creates hundreds/thousands of opportunities per game
  - Don't lose everything when game goes wrong — just some value
  - Can express nuanced, multi-day views on team trajectories
  - Non-binary — continuous pricing across the entire season

- **Nobody has to lose for someone else to win:**
  - Equity model: value can be created (all shares go up if marketing revenue grows)
  - Sports betting and prediction markets are zero-sum — losers fund winners
  - InPlay: everyone can profit if the market grows

- **Single liquidity pool, single source pricing:**
  - Becomes THE reference price for sports equity globally
  - No fragmentation across platforms (vs. Kalshi/Polymarket/FanDuel all with separate liquidity)
  - Liquidity providers at all prices, all stages — easier to exit positions

- **SEC-regulated with SIPC insurance:**
  - Accounts insured up to $500,000
  - Real regulatory framework — prediction markets "don't have the regulatory framework that the SEC does"
  - Actual public companies with corporate governance

- **Financial literacy transfer:**
  - Teaches real equity market mechanics (order books, bid/ask, position management)
  - Prediction markets don't teach futures trading — "if you trade prediction markets, you don't actually learn how to trade futures"
  - Capital gains/losses tax treatment (losses tax-deductible, unlike gambling)

- **Timing and availability:**
  - Available evenings and weekends — when traditional markets are closed
  - When people are already watching and engaged with sports

- **Transparency:**
  - "The most transparent equity market in the world"
  - Can literally watch your stock perform on television in real time
  - No other asset class offers this

### Unfair Advantage

- Single source pricing — "we become the number one source for everyone to price everything else off of because this is the only single liquidity price." More users = more liquidity = stronger reference price
- SEC-regulated corporate structure with actual public companies — expensive and complex to replicate
- Sport Radar data licensing deal already in place
- Edwin: "it's a first of its kind asset class" — no one else is doing path-dependent sports equity

---

## 5. How Does It Make Money?

- **Revenue split (Trading Challenge):**
  - ~90% advertising and marketing
  - ~10% other (fees, IPO extraction, corporate services)
  - Edwin: "for the challenge, it would probably be 90% of the money comes from marketing and advertising"

- **Revenue split (Production — future state):**
  - ~70% advertising and marketing
  - ~30% other (transaction fees, data, referrals)
  - Edwin: "in our production level, I would call it 70/30 with 30 being the other stuff"

- **Revenue streams:**

  1. **Advertising & consumed minutes (primary):**
     - Target: at least 1M users engaged for at least 1 hour/week = ~1B minutes of consumption
     - Skye's team selling those consumed minutes to advertisers
     - Sports vertical that's otherwise untouchable for most businesses in terms of cost
     - Edwin: "while we're running an exchange, exchanges today make most of their money on data. They don't make it on exchange fees. And so, in lieu of us making money on data, where we aim to make money is in marketing and advertising"
     - Edwin: "InPlay is a marketing platform with a very specific product that hits an amazingly large and juicy demographic for advertisers"
     - Interactive moment-based ads (detailed in Section 1)
     - Social listening data as monetizable asset for advertisers/media buyers (Skye referenced Omnicom building products around this kind of data)
     - Advertising value differs between challenge and production users — Kevin: "We can sell different advertisements to the production users because they are a qualified actual trader. They are spending real money"

  2. **Brokerage referral fees:**
     - $150 per customer that opens an account with a brokerage partner
     - Qualifying deposit: $2,500
     - 500,000 referred accounts = $75M
     - Edwin: "I got a call yesterday from a group that will pay us 150 bucks per customer that opens an account"
     - Brokerage partners see $150 CAC as "very very cheap"

  3. **IPO extraction:**
     - InPlay Markets acts as manager of the ATS (through T0)
     - Extracts ~10% of money raised during IPOs
     - Also extracts fees for corporate services to team companies
     - Edwin: "we're going to extract roughly 10% of the money that's raised during the IPOs"

  4. **Corporate services:**
     - InPlay manages all corporate services for the 32+ team companies
     - Reporting, accounting, advertising sales, marketing
     - Revenue from these services — detail promised in a separate revenue model document

  5. **Data monetization (deferred to year 2+):**
     - Not charging for data in year one (challenge or production)
     - Cody built a platform for tiered market data access, historical data, backtesting
     - Will become a paid product in future years
     - Edwin: "in lieu of making that available for pay in year one we're going to hold off on that"

- **Who pays:**
  - Advertisers/sponsors pay for attention and consumed minutes (primary payer)
  - Brokerage partners pay for qualified user referrals
  - Users pay nothing for the trading challenge
  - In production: implied transaction fees but not detailed for challenge scope

- **Prize pool (cost, not revenue):**
  - $5M–$25M total prize pool for the season
  - ~$200–250K distributed per day
  - Funded by advertising revenue (implied, not explicitly stated)
  - ⚠️ **Gap:** Confirm funding source for prize pool — is it pre-funded by sponsors, or from general advertising revenue?

---

## 6. Constraints

- **Timeline:**
  - Mid-August launch — hard stop
  - Summer referral program needs to be live before launch to build pre-season user base
  - Payout schedule being finalized by InPlay team (Edwin + Cody)

- **Scope boundaries:**
  - Trading challenge covers NFL regular season only — not playoffs
  - NFL = 32 team companies (fixed)
  - College football D1 also in scope — plays 6 days a week (infrastructure must support this volume)
  - Challenge is simulation only — production trading is a separate future phase

- **Technology dependencies:**
  - T0 — ATS (Alternative Trading System) partner, manages the trading venue
  - Sport Radar — real-time in-game data + historical data for all D1 college and NFL games
  - Persona — KYC/identity verification (age, identity, bot prevention)
  - Brokerage partners (Robinhood, Webull, Schwab) — production trading accounts (future state)
  - Other vendors involved — Kevin referenced "coordination with some of the other vendors"

- **Legal / compliance:**
  - Age 18+ required
  - KYC for challenge: age verification, real identity, no bots, US citizenship validation (if US-only)
  - Global availability pending regulatory confirmation
  - KYC for production (future): accredited vs non-accredited investor validation on primary offering
  - Secondary offering: both accredited and non-accredited allowed without limitations
  - SEC regulatory framework applies to production
  - SIPC insurance up to $500K on production accounts
  - Fair access required — cannot gate production access based on challenge performance

- **Brand / design:**
  - App, trading challenge landing page, InPlay Global website, and socials must all feel cohesive — "look and feel and be very very connected" but not identical
  - Direction: white background, clean, focus on mockups, easy on the eyes
  - Wireframes already shared in Google Drive — existing design reference
  - Skye: "it needs to look like it's part of the same brand family"

- **Operational:**
  - Support during US peak sports hours (evenings/weekends US time = early morning UK time) — Kevin flagged this needs resolution and inclusion in terms of service
  - Brett: "What we build on the Rebel Novo side is essentially self-healing and self-support" — proposed approach but not yet defined
  - Contract review in progress with InPlay's internal counsel (delayed due to personal circumstances)

- **Non-negotiables:**
  - Trading challenge is free to enter — zero cost to user
  - Trading wallet capped at 100,000 (never exceeded via referrals)
  - Fair playing field — no user gets unfair trading advantage
  - InPlay does not provide trading advice or summarise community sentiment (liability avoidance)
  - No qualification gating — Edwin: "I would shy away from the qualification part... you have to provide fair access"
  - Referral trigger requires full KYC completion (not just signup)

---

## 7. What Exists Today?

- **Existing systems / platforms:**
  - Previous trading simulations have been run (users traded 4+ hours straight — real behavioural data exists) — ⚠️ unclear what platform/system these simulations were run on, need to clarify with Edwin
  - Cody built a market data platform with tiered access, historical data, and backtesting capability (deferred to year 2+ for monetization)
  - T0 partnership in place for ATS infrastructure
  - Sport Radar licensing deal in place for real-time + historical data
  - Persona selected for KYC

- **Existing user base:**
  - No live users yet
  - Ivy League campus tours completed — direct student engagement and feedback
  - Brokerage partner discussions active ($150/account offer already received)

- **Existing data / content:**
  - Behavioural data from previous simulations (engagement patterns, trading duration, user behaviour)
  - Sport Radar historical data access (all D1 college and NFL)

- **Previous work:**
  - Wireframes shared in Google Drive (game page reference included)
  - Landing page in active development (rough version, feedback mechanism due end of week)
  - InPlay Global website — conceptual design starting
  - Copy work in progress for landing page/flyer (Edwin, Skye, Cody collaborating)
  - Social strategy being developed (Skye + Brett strategy interview scheduled)
  - Payout schedule being finalized by Edwin + Cody

- **Existing branding / design language:**
  - Direction established: white background, clean, easy on the eyes, focus on mockups
  - Brand family cohesion required across all touchpoints
  - Full brand guidelines not yet defined
  - ⚠️ **Gap:** No established design system, colour palette, or component library shared yet

---

## 8. Risks

- **Abuse and gaming:**
  - Bot signups to farm referral wallets (mitigated by KYC via Persona)
  - Sentiment manipulation in the third space/community chat — Edwin flagged "I see some potential bad actors there"
  - Meme-stock herd behaviour — community momentum overtaking rational pricing (accepted as a feature that mirrors real markets, but could be exploited)
  - Influencers with massive referral banks (mitigated by 100K trading wallet cap)

- **Distribution and partnership risks:**
  - Brokerage partner dependency — Edwin concerned they won't promote InPlay effectively: "I don't believe that they're going to provide us with the value we expect from them in turning on their clients"
  - Referral wallet reset at end of season could cause dissatisfaction for users who built large banks but didn't use them all

- **Data and integrity risks:**
  - Accounting errors on user balances (Edwin's personal Polymarket experience — $900 went missing)
  - Sport Radar data feed reliability during live games (single dependency for real-time data)
  - ⚠️ **Gap:** What happens if Sport Radar has an outage during a live game?

- **Compliance and regulatory:**
  - Global availability still pending regulatory confirmation — could limit to US-only
  - Challenge operating in a novel regulatory space — not clearly sports betting, not clearly securities (for the simulation)
  - **Financial advice risk:** Any feature that summarises sentiment, suggests trades, recommends positions, or guides user decision-making could be construed as financial advice — requires appropriate licensing and disclaimers. Edwin was explicit about avoiding this: "I don't want to be the summarizer of the sentiment. I want users to make their own journey." This constraint must carry through to all AI-driven features, educational content, news feeds, and community aggregation
  - ⚠️ **Gap:** Has legal counsel confirmed the challenge doesn't require a sports betting license or specific state-by-state approval?

- **User experience risks:**
  - Users blowing out their trading wallet early and disengaging (mitigated by referral wallet reload)
  - Complexity barrier — users who don't understand trading mechanics may bounce quickly
  - Education module depth vs. "let the market tell us" approach — risk of under-serving beginners
  - Prize distribution concentration — if top traders dominate daily, casual users may feel locked out
  - ⚠️ **Gap:** What's the retention strategy for users who blow out and have no referral bank?

---

## Gaps — Questions for Next Call

### Section 1: What are you building?
- Education module — in-app or website-only? In scope for this build or handled separately?
- Off-field revenue component in the simulation — is it live/dynamic or simplified?
- "Always-on" simulator beyond the challenge — future-state or architect for it now?
- College football scope — all D1 games from day one, or a subset?

### Section 2: Who are you building it for?
- Gender split — relevant or deliberately not segmented?
- Global vs US-only — regulatory answer pending (was "finding out tomorrow")

### Section 4: What makes this better?
- Edwin's personal daily experience trading Polymarket, Kalshi, and betting — capture more detail on firsthand competitor UX

### Section 3: Why are you building it?
- Ask Edwin directly: "What happens if you don't launch this season?"

### Section 5: How does it make money?
- Confirm funding source for prize pool — pre-funded by sponsors or general advertising revenue?
- Detailed revenue model document promised by Edwin — request it
- Fee reduction for experienced challenge users transitioning to production — Edwin: "something we'd have to look at"
- Sponsor referral wallet redemption details — what offers, which sponsors?

### Section 6: Constraints
- Support hours model during US peak sports times — needs resolution and inclusion in terms of service
- Advertising inventory model — Skye: "right now it's not defined"
- CRM/push notification strategy — timing, content, branding all undefined
- Previous simulation platform — what system was used? Need to clarify with Edwin
- Payout schedule follow-up — Edwin promised "by next Friday"

### Section 7: What exists today?
- Design system / colour palette / component library — does one exist?
- Access to wireframes in Google Drive — need shared access

### Section 8: Risks
- Sport Radar outage scenario during live games — what's the fallback?
- Legal confirmation that challenge doesn't require sports betting license
- Retention strategy for users with zero referral bank who blow out

---
