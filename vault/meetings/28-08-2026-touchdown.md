---
date: 2026-08-28
type: standup
description: "Friday touchdown, 28 August 2026: the reference-price delta model worked through with numbers, the end-of-game price snap-back, and the buying-power gap found the day before the first live games."
source: "Google Meet transcript, Inplay - App - Touchdown (49m 40s)"
scope:
  - "[[market-maker/market-maker]]"
  - "[[earnings-report/earnings-report]]"
  - "[[trading/trading]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[information-layer/sub-components/discovery-home/discovery-home]]"
  - "[[delivery/delivery]]"
status: extracted
extracted-to:
  - "[[market-maker/decisions]]"
  - "[[market-maker/open-questions]]"
  - "[[market-maker/plan]]"
  - "[[market-maker/sessions/2026-08-28-touchdown-digest]]"
  - "[[earnings-report/earnings-report]]"
  - "[[trading/trading]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[information-layer/sub-components/discovery-home/discovery-home]]"
  - "[[compliance/regulatory-positioning]]"
  - "[[advertising/advertising]]"
  - "[[tzero]]"
  - "[[delivery/delivery]]"
  - "[[delivery/requirement-changes]]"
---

## Post-Call Analysis

49 minutes, **the day before the first live NCAA games**. Present: Edwin, Troy,
Cody, Jared, Kevin (InPlay) and George, Brett, Hasan, Lily (Novosapien). Max was
travelling. The call ran long, covered a demo, and closed with Edwin asking who
would be on standby for Saturday. George: at least one of us.

**This is the call the 27 August touchbase was cut off before finishing**, and it
is far more useful, because Edwin worked the pricing model through with real
numbers instead of describing it.

### 1. The reference price, finally worked through with numbers

Edwin sent a reference document the day before, covering the full remaining
season. George's read: the **injuries** part _"needs a decent amount of work"_,
and Edwin agreed to take it step by step, with injuries **out of scope for now**.

He described what he is building: not quite an ELO system but working like one,
and notably **it takes bid-offer pressure as an input to value**, so the price
is not only his opinion. His framing of its purpose: _"there's no wrong or right
answer. We just need it to be digestible by the market"_, because the maker bids
and asks around it.

**The problem he is solving, in his words:** _"we don't want the market or the
participants to think that oh they bought a team, the team won, they're entitled
to $5."_ Most of a favourite's value is **already in the price** before the game
starts.

**The worked example, which is the most valuable thing on this call.** Cody
supplied the live numbers for TCU against North Carolina: money line **-380**,
Sportradar win probability **77.3%**.

| Step | Value |
|---|---|
| Payout if the team wins | $5.00 |
| Win probability at kickoff | 77.3% |
| **Price before the game** | 0.773 × $5 = **~$3.86** |
| **If TCU wins** | the price should rise **from $3.86 toward $5** for on-field |
| Edwin's per-game value at this probability | around **$1.14** of season price |

**George stated the model back and Edwin confirmed it twice:** the kickoff win
probability is **already factored into expected wins**; the **change between the
kickoff probability and the actual result** is the increase or decrease in share
value. ⚠ **George immediately named the assumption it rests on:** that win
probabilities really are factored into expected wins. Expected wins and win
probability come from **different Sportradar feeds**, and different providers
give different expected wins. He called it a fair assumption; it is still an
assumption, and the whole model sits on it.

Edwin's own modelling goes further: _"currently LSU is three and three, and
they're down 14 points in the fourth quarter. What's their value with two minutes
left?"_ A 6 and 0 record gives a different price, with the remainder driven by
how many games are left and the strength of the opponents still to play.

### 2. The end-of-game snap-back, which is the real defect

George raised it plainly, and it is the concrete form of the problem the vault
has been circling since 17 August:

> _"Price goes up, changes during a game, and then at the end of the game,
> because the expected wins hasn't changed, it's just going to drop back down to
> what it was before."_

Edwin: _"we don't want anything dropping back down, that's not going to work."_
His delta model is the fix: the result moves expected wins, so the price ends the
game somewhere new rather than returning to where it started. ⚠ **The fix is not
built, and the first live games are tomorrow.** Recorded as **N55**.

George also flagged a mechanical cost: **replaying the journal to rebuild state
adds latency**, and the approach needs choosing.

### 3. Off-field volume: three answers, and one reverses yesterday

Four things were settled in quick succession, and one of them **reverses a
position taken on the 27th**.

- **Volume means the notional amount, effectively the number of trades.** Not
  dollar-weighted: _"we're not going to break it down into the actual dollar for
  dollar… keep it very simple."_
- **The window is game to game, not calendar.** _"As soon as the game's over,
  then that share's count till the next game is over."_ Games are always at least
  **four days apart** (Sunday then Thursday at the tightest).
- **Earnings release: Tuesdays for NFL, Wednesdays for college.** Reconfirmed.
- ⚠ **Maker and taker volume is now INCLUDED.** On 27 August Edwin accepted
  excluding both. Today, after George confirmed either filter is easy, he
  reversed it: _"Leave them both then. Leave the maker and the taker **because I
  want to report more trading volume each week. I don't want to report 22
  trades.**"_ Recorded as **R17**. The reason is presentational rather than
  mechanical, and it is worth stating what it costs: the two house bots trade
  continuously, so including them means the reported volume is **mostly house
  activity**, and the off-field allocation it drives is correspondingly less
  connected to real participant behaviour.

### 4. The order ticket, where the client's instinct was talked out of it

Edwin found the quantity field **sticky**: the last traded size persists, and
persists **across teams** (500 on Air Force stays 500 on Alabama). His concern is
real: _"people are going to mess it up the first couple times and if they do it on
size, it's going to be catastrophic."_ His fix was to **reset it to zero**.

**Three people talked him out of it, and they were right.** George: zero means
_"effectively no one-click trading"_. Jared: _"it would frustrate me if I was not
able to buy."_ **Troy settled it:** _"the default order size is what it always
goes back to. That's how it works on other trading softwares too."_ Jared:
_"That's how I do it on Weebull, Robinhood, thinkorswim."_

**Resolution: the order ticket reloads to the user's default order size.** The
setting already exists under More; it was built, then changed to last-order, and
now flips back. Recorded as **R18**, a re-reversal inside the app.

**Troy's larger ask, which is the better version of the same idea:** a **one-click
trading settings tab**, holding the presets a trading app normally has. _"At the
minimum you want quantity and then the ability to default to market on every
ticket."_ ⚠ **He named a defect while doing it:** order type is inconsistent,
_"sometimes market sticks, sometimes market doesn't"_, depending on which screen
the ticket is opened from.

**Quantity buttons become incremental.** George proposed that the preset chips add
rather than replace, so 100 then 25 gives 125. Edwin: _"Incremental."_ Jared
added that other apps also carry a **plus and minus stepper** at a configurable
increment.

Edwin also explained his own workflow, which is why the control matters to him: he
uses it to rest passive orders rather than pay the offer or hit the bid. _"I don't
want to give up an edge right away. I want to work it."_

### 5. The demo, and what Edwin wants changed

Hasan demoed the **first-run walkthrough**: it starts on account creation and can
be replayed from settings, then walks balance, upcoming games, the markets tab, a
team, the price chart, holdings, a **simulated practice buy and sell**, the
leaderboard, and groups.

| Change | Why |
|---|---|
| **Remove the dollar signs.** _"No reference to money."_ | Regulatory |
| **No percentages anywhere, show the net change in value** | Repeat instruction, previously given |
| Bug: the sell step's button is unreachable on some screens | Hasan: aspect ratios and accessibility zoom still to handle |
| Bug: back navigation does not return to the original screen after four or five steps | Spotted by Jared and Ronex, already in hand |
| Kevin: mention the default order size in the walkthrough | So users know the setting exists |

Edwin also could not change his own username. And he flagged, separately, that
**website language has to change for the regulators**, which he is handling.

### 6. The home page is reordered, and a defect surfaced with it

Edwin's contact at Meta sent feedback: **new users find the app overwhelming on
open**. George accepted simplification is needed while noting trading carries
inherent complexity, and floated then immediately withdrew the idea of different
app versions per user level.

**The agreed fix is an ordering change, and all three InPlay voices agreed.**
Edwin: the team IPO tile is _"overpowering"_, and the IPO itself is not the
engaging part: _"you buy them and then you wait"_ (his summary of Troy's point).
The excitement is trading during games.

- **Live and upcoming games move up**, directly under the simulated trading
  challenge header.
- **The team IPO tile moves down**, below the portfolio (Jared: _"substantially
  lower"_).
- ⚠ **Defect, the day before NCAA games: college games are not appearing in
  upcoming games at all, only NFL.**

### 7. Buying power is not reaching unverified accounts

**The most urgent operational item on the call.** Troy has **two unverified
accounts with no buying power**, one created weeks ago and one yesterday, and
asked how the 13-and-over tier gets enabled for trading.

Hasan explained the cause: getting a trading account is currently **an explicit
step** rather than an automatic one. He had planned to make onboarding allocate
buying power and register the account with tZERO automatically. The flow has to
wait for the account to move from tZERO's staging API onto their main system, and
timing that is _"a bit clunky at the moment."_

**Troy's real worry is not his two accounts:** _"I'm more worried about anyone
that may have signed up over the last week without going through the ID
verification, expecting those locked feeds to come off now that we're open for
secondary trading."_ In other words, the KYC-less path shipped and the accounts it
created may not be able to trade.

Hasan's estimate: a **backfill** to find and fix every account with no buying
power takes **half an hour to an hour**; the **underlying fix** takes **a few
hours**. Edwin: _"That's a critical piece."_ He tied it directly to marketing
spend: _"if we're spending money on advertising, we've got to have people be able
to sign up and not do the KYC."_

### 8. The marketing agency has a timeline

Cody set it out. The agency is already in TestFlight, and reviewing the onboarding
experience is explicitly part of their scope.

| When | What |
|---|---|
| Weeks 1 to 2 | Discovery: reviewing the app and the onboarding experience, feeding back suggestions |
| **Week 3** | First ad tests. **Hooks and language only, no graphics**, small spend, testing what resonates |
| Weeks 3 to 4 | A spreadsheet of suggested spend, based on the research |
| **Week 5** | The first real campaign |

Brett asked Cody to chase their logins so they can be added to **tag manager,
analytics and Firebase**; Sebastian has not responded.

### 9. Data as a product, and the licence that blocks the best version of it

The most strategically interesting exchange on the call, and it belongs on record
even though nothing is being built.

Edwin on the reference model: _"this is going to be key to our data sales… this
might become the most valuable thing we create, that sports books may want to buy
from us."_ Cody: _"this is how we could potentially replace a portion of a billion
dollar company's business."_

**The argument, which is genuinely good.** Sportsbook prices move on **flow**, not
value: a book shades its line to balance its own book, so FanDuel moves one way
while Hard Rock moves the other. Polling eight or ten books therefore gives
_"two smaller fragmented data sets"_, not a truer price. Edwin: _"you can move
lines with not that much money depending upon when you make those bets."_ **InPlay
is a single liquidity pool**, so its price is _"a truer source of a larger subset
of data."_ It is the same argument the product makes to users, applied to the data.

**Cody also explained the odds lifecycle**, which clarifies where our inputs come
from: Sportradar creates an **origination (consensus) line** and sells it to
sportsbooks worldwide; the large books blend it with their own data to make their
own line; those lines feed back to Sportradar, closing the loop. **Win probability
is completely separate** and is generated by Sportradar from live play-by-play
only, not from betting lines.

⚠ **The blocker.** Edwin noted you can back into a probability from live odds.
We cannot: live odds sit on the **betting feed**, and _"sportsbooks are the only
companies that are allowed to get it and you need a sportsbook license."_ Cody is
pursuing it, has found **a precedent involving a company operating under a
sportsbook licence**, and referenced Polymarket receiving the feed for
**matchmaking rather than resulting**. He owes a fact-check with David.

### 10. Team reference data is wrong in at least a dozen places

Jared's list, with more to come (_"there's probably 15 others"_):

| Team | Wrong | Should be |
|---|---|---|
| Notre Dame | Listed in the ACC | **Independent** |
| Louisiana Tech | Colour red | **Blue** |
| UConn | Abbreviated `UCN` | **`CONN`** |
| Charlotte | Abbreviated `CHAR` | **`CLT`** |

George: names came through, colours did not, and he will re-run the update. The
text is straightforward to fix. ⚠ Small individually, but this is the data on the
surfaces users see on the first live game day.

| Finding | Destination | Action |
|---------|-------------|--------|
| **Reference price = kickoff probability already in expected wins; the delta to the result moves the price** | [[market-maker/decisions]] | Decision recorded with the worked example |
| Worked example: TCU 77.3%, $5 payout, priced ~$3.86, rises toward $5 on a win | [[market-maker/decisions]] | Numbers recorded |
| Edwin building an ELO-like model taking **bid-offer pressure as a value input** | [[market-maker/decisions]] | Recorded |
| ⚠ The model assumes win probability is inside expected wins; different feeds, different providers | [[market-maker/open-questions]] | New N56 |
| **End-of-game snap-back: price returns to its start because expected wins never moves** | [[market-maker/open-questions]], [[market-maker/plan]] | New N55, live tomorrow |
| Injuries out of scope for now | [[market-maker/open-questions]] | Recorded in N56 |
| Journal replay adds latency, approach to be chosen | [[market-maker/open-questions]] | New N57 |
| Off-field volume = notional, effectively trade count, not dollar-weighted | [[earnings-report/earnings-report]] | Confirmed |
| Window is game to game; games at least four days apart | [[earnings-report/earnings-report]] | Confirmed |
| Earnings Tuesdays NFL, Wednesdays college | [[earnings-report/earnings-report]] | Reconfirmed |
| ⚠ **Maker and taker volume now INCLUDED**, reversing 27-08 | [[earnings-report/earnings-report]], [[requirement-changes]] | R17 |
| **Order ticket reloads to the default order size**, not last traded or zero | [[trading/trading]], [[requirement-changes]] | R18, re-reversal |
| Troy: a **one-click trading settings tab** with presets, at minimum quantity and default-to-market | [[trading/trading]] | Requirement |
| ⚠ Defect: order type inconsistent, market sticks on some screens and not others | [[trading/trading]] | Defect recorded |
| Quantity preset chips become **incremental**; plus and minus stepper asked for | [[trading/trading]] | Requirement |
| Walkthrough: **remove dollar signs, no reference to money** | [[compliance/regulatory-positioning]] | Rule extended |
| Walkthrough: **no percentages, net change in value only** | [[information-layer/sub-components/discovery-home/discovery-home]] | Repeat instruction |
| Walkthrough bugs: unreachable sell button, back navigation loses place | [[information-layer/sub-components/discovery-home/discovery-home]] | Defects recorded |
| Website language must change for the regulators (Edwin handling) | [[compliance/regulatory-positioning]] | Flagged |
| **Home page reorder: live games up, team IPO below the portfolio** | [[information-layer/sub-components/discovery-home/discovery-home]] | Requirement |
| ⚠ Defect: **college games missing from upcoming games**, only NFL showing | [[information-layer/sub-components/discovery-home/discovery-home]] | Defect, day before NCAA games |
| New users find the app overwhelming on open (Meta contact feedback) | [[information-layer/sub-components/discovery-home/discovery-home]] | Context recorded |
| ⚠ **Buying power not allocated to unverified accounts**; backfill 1h, fix a few hours | [[customer-onboarding/customer-onboarding]] | Critical, recorded |
| Trading-account allocation is an explicit step, should be automatic; tZERO staging-to-main timing clunky | [[customer-onboarding/customer-onboarding]], [[tzero]] | Recorded |
| Marketing agency: discovery wks 1-2, ad tests wk 3, spend plan wks 3-4, first campaign wk 5 | [[advertising/advertising]] | Timeline recorded |
| Agency logins owed for tag manager, analytics, Firebase | [[advertising/advertising]] | Chase recorded |
| **Data as a product**: single liquidity pool beats fragmented book polling | [[delivery/delivery]] | Strategy recorded |
| Odds lifecycle: Sportradar origination line, books blend, feed back | [[tzero]], [[market-maker/open-questions]] | Recorded |
| ⚠ **Live odds need a sportsbook licence**; Cody pursuing a precedent | [[market-maker/open-questions]] | New S13 |
| Team reference data wrong: conference, colours, abbreviations, ~15 more | [[information-layer/sub-components/team-page/team-page]] | Defect list recorded |
| At least one Novosapien engineer on standby Saturday | [[delivery/delivery]] | Recorded |

---

Aug 28, 2026

## **Inplay \- App \- Touchdown \- Transcript**

### **00:00:18**

**Brett StClair:** Hello.

**Jared Sapirman:** Morning or afternoon?

**Brett StClair:** I uh woke up a little bit later than normal, so I could actually maybe call it morning. Hello everybody. Oh, still two more. Jeez, sorry, that's me fast asleep. My apologies. Hello. Hello. Hello. Hello. Hello. Hello. Kevin looks surprised. What are you surprised about? Keep

**Cody Haugen:** Hey, good morning. Oh, we're all on mute.

**Brett StClair:** surprised that he's on mute.

**Cody Haugen:** Yeah,

**Brett StClair:** On mute.

**Cody Haugen:** he's like,"How does

**Kevin Murray:** Oh, I pressed the button like five times. The f\*\*\*\*\*\* thing wouldn't move.

**Cody Haugen:** work?

**Kevin Murray:** Come off. It's one of those mornings, I tell you. Is it too early for a drink?

**Brett StClair:** It's never too early for a drink. Never too early.

**Kevin Murray:** 5:00 somewhere in the world, isn't

**Cody Haugen:** Yeah,

**Brett StClair:** It's 5:00 somewhere indeed. Hello, Edmond.

**Kevin Murray:** it?

**Cody Haugen:** exactly.

**edwin:** I don't know if you could read my lips, but was wasn't real happy with the fact that I'm on mute every time I try to

### **00:01:51**

**Brett StClair:** Yeah,

**edwin:** join.

**Brett StClair:** f\*\*\*\*\*\*

**edwin:** It definitely it definitely was in the uh FU category. Good morning all.

**Cody Haugen:** Good

**edwin:** All right.

**Brett StClair:** boy.

**edwin:** Do we have everybody on that we

**Cody Haugen:** morning.

**Brett StClair:** Um,

**edwin:** need?

**Brett StClair:** let me have a

**George Westbrook:** He's joining.

**Brett StClair:** look.

**George Westbrook:** How we all

**edwin:** Good. Good.

**George Westbrook:** doing.

**edwin:** How about you? Are we ready for another?

**Brett StClair:** You got a demo coming now.

**edwin:** I got a demo.

**Brett StClair:** Demo time.

**edwin:** Oh, yeah. All right, let's see it.

**Brett StClair:** Mo time. This is where her son This is where her son puts on his s\*\*\*\*\*

**George Westbrook:** Give two seconds.

**Brett StClair:** earpiece. We all sit there going,"f\*\*\* sake, Sissan. Don't put on the s\*\*\*\*\* earpieces. Put on the ones we can hear you." And we go through that routine before we get to the demo.

**George Westbrook:** He's just he's just being a good boy and putting them in.

**edwin:** I got a lot of bad boys on my team.

### **00:03:01**

**edwin:** I don't have any good boys.

**Brett StClair:** Is it when you say that? Do you mean bad boys? Bad

**edwin:** Um,

**George Westbrook:** That was a s\*\*\*

**edwin:** not quite the criminal kind.

**Brett StClair:** boys.

**edwin:** I I was thinking uh more the naughty boys.

**George Westbrook:** joke.

**edwin:** Um, you know, you can't you can't hit your employees, which is unfortunate, but it would be great if you could.

**George Westbrook:** Oh god, Max Max would have so many black eyes if that was the case.

**edwin:** I was thinking more like a paddle.

**Brett StClair:** Oh

**edwin:** Yeah, I was thinking the bottom, not the top.

**George Westbrook:** Oh

**Brett StClair:** problem is then we have happy

**edwin:** Is KMBB down in Aiza already?

**Brett StClair:** Max.

**edwin:** Is he already down

**Brett StClair:** How's this for Max?

**edwin:** there?

**George Westbrook:** yeah.

**Brett StClair:** He gets on the plane and straight away two belter girls call him over and kick out the other people and he sits next to these two belter girls and he sends us a video of them and we're like

**edwin:** Oh, he for the record Max will never

### **00:04:00**

**Brett StClair:** only Max's

**edwin:** be seen again.

**Brett StClair:** world.

**edwin:** He's gonna he's gonna it's very likely Max is going to be like

**Brett StClair:** It's a lot

**edwin:** harvested for organs cuz I've seen Max.

**George Westbrook:** Hang

**edwin:** He's a handsome guy, but like you know two two at a time for Max.

**George Westbrook:** on.

**edwin:** I think that's that's tough.

**Brett StClair:** Juicy liver you got there, Max. What?

**edwin:** Sorry,

**Brett StClair:** Sorry.

**edwin:** I didn't mean to I didn't mean to take it dark on a Friday, but um I'm sure he's having a great

**Brett StClair:** Yeah. So,

**edwin:** time.

**Brett StClair:** should we jump in straight into a demo? Might as well. That's fun. So, are you ready? Sorry. Actually, we're just dumping you straight into

**Cody Haugen:** as he's frozen. Good. Good. Passover.

**Brett StClair:** it.

**George Westbrook:** He's back now. He's

**Hasan Ahmed:** He's back.

**Cody Haugen:** He's

**Hasan Ahmed:** Um, if you give me a second while I get up.

**George Westbrook:** back.

**Hasan Ahmed:** Um,

### **00:04:51**

**Cody Haugen:** back.

**Hasan Ahmed:** I was not prepared for it.

**edwin:** M those people aren't max I'm sorry it's

**Hasan Ahmed:** Um,

**Brett StClair:** Um,

**edwin:** on

**Brett StClair:** so then let's quickly talk market maker. George, are you happy where you landed with all the meetings yesterday?

**George Westbrook:** Yeah, I think with that document, Edwin, there's I think it's one that could be not problematic,

**edwin:** Sure.

**George Westbrook:** but needs a decent amount of work is the injuries one because then it's

**edwin:** Yeah. Yeah. I don't think Listen, I think that like we we take it step by step, right? So, I you know, I'm trying to build something internally here that's not it's not quite an ELO system, but it's going to work like an ELO system. um it's going to take in account like our our bid offer pressure and that's going to be a val an input

**George Westbrook:** H.

**edwin:** for value not just like you know my my opinion. So, um, my goal yesterday was to just give you something that's like a reference point that gives you the team the the rest of the season that you know all of the factors how you could just mathematically model it.

### **00:06:05**

**edwin:** Um because I you know the problem I think that we had was like we don't want we don't want the market or the participants to think that oh they bought a team the team won they're entitled to $5, right? it it's a market where most of the price of a favorite is already priced into the to the share price because of based on probability. So if someone's an 80% chance of winning the first game, you would just say okay well what's the payout? Five bucks. You'd say that price is worth $4. You know 80% of $5, right? And then like you as the game goes, let's say they go behind and you know now it goes from 80% down to 42%. It's not um it you know it has an impact on that game obviously but it could have an impact on other games. For example, if they lose to a s\*\*\* team or something like we discussed yesterday um that would have a material impact on the forward pricing of the model. Now the go the goal here isn't like we're not going to win a prize.

### **00:07:11**

**edwin:** for getting the best reference price because we're we're going to bid and ask around it. So, there's no wrong or right answer. We just need it to be digestible by the

**George Westbrook:** Yeah. Yeah, that makes sense.

**edwin:** market.

**George Westbrook:** I think the only other thing is so there's the expected offfield value which we we've already got the number, haven't it? it's already baked in. And then it's the the mechanism for going from actual sorry expected to actual and then updating. And then with the actual like we said it's based on the the trade is it volume or dollars traded as well for that game volume.

**edwin:** just volume.

**George Westbrook:** Okay.

**edwin:** It's going to be the notional amount which is the you know essentially how many trades. We're not going to break it down into the actual like dollar for dollar. You know, this traded 400,000, this trade at 401\. We're just going to say based on volume,

**George Westbrook:** Okay.

**edwin:** keep it very simple.

**George Westbrook:** And and over just the game period or a bit after the game and a bit

### **00:08:15**

**edwin:** Just that game.

**George Westbrook:** before.

**edwin:** Um, I would say from the week to week, so like you know,

**George Westbrook:** Oh, okay.

**edwin:** you know what I mean? The game's over that now. You know, as soon as the game's over, then that shares count till the next game is over.

**George Westbrook:** games is I don't know if it's the same as the Premier League, but sometimes there might be midweek games. So like a gap could be 5 days or it could be two

**edwin:** Yeah,

**George Westbrook:** days.

**edwin:** there well it they won't like it'll always be at least um four days. So you can play on Sunday and then you can play on Thursday, but it'll never be less than four days.

**George Westbrook:** Did we say earnings reports are going to be on Tuesdays or Wednesdays.

**edwin:** Yeah. Tuesday Tuesdays for NFL,

**George Westbrook:** So I suppose if it and then in that

**Kevin Murray:** Yeah.

**edwin:** Wednesdays for college.

**George Westbrook:** earnings report it's just going to be effectively that off off field presenting that off field.

**edwin:** Yeah.

**George Westbrook:** Um and the so obviously we'll get rid of the the what the maker does.

### **00:09:22**

**George Westbrook:** Um are we going to include the taker into that as well?

**edwin:** No, just no. The taker has Well, technically what's going Why don't you do this? Tell me what's going to be the easiest way for you to count.

**George Westbrook:** Um they're both kind of as easy as each other in terms of the volume. We can just like get all the trades then filter by ID and just remove maker and maker and taker activity. It's it's like a tiny tiny bit extra, but it's not enough where it's an issue really to be honest.

**edwin:** Uh, leave them both then. Leave the maker and the taker because I want to report more trading volume each week. I don't want to report 22 trades. I want to report,

**George Westbrook:** Yeah.

**edwin:** you know, couple of falls in or

**George Westbrook:** Okay. Um, I think the there's one other thing where I think it's

**edwin:** whatever.

**George Westbrook:** where we're rebuilding or replaying the journal, it's going to add some latency. I think we just need to I just need to look at what's the best way to way to do that.

### **00:10:36**

**George Westbrook:** If there's a will, there's a way.

**edwin:** Isn't that the truth?

**George Westbrook:** I think apart from that,

**edwin:** Sure.

**George Westbrook:** I'm just looking The injury channel not going to be in there at the moment. Volume in the week. Okay. Yeah, that's that's everything on that. I'm still still looking into it. So, um there's bound to be some more questions coming over.

**edwin:** And we can refine as you know as we you know continue through the journey.

**George Westbrook:** I think Hassan, you're up.

**Hasan Ahmed:** All right. Um,

**edwin:** I haven't seen you look this happy ever,

**Hasan Ahmed:** on to the always in a good mood.

**edwin:** son.

**Hasan Ahmed:** So, um, if you want to start the actual as in so um, how like it's going to work is as soon as you can create your like account, it will start the entire walk through. I mean, and then or if you want to go to the actual the settings and then start it through there as well. Like I mean like if you want a quick laugh and catch up, it's always there as an option.

### **00:11:44**

**Hasan Ahmed:** So if I click this as I mean I give you an intro and then explain how it's going to work.

**edwin:** Yeah. Well, on this page real quick,

**Hasan Ahmed:** So if you click show me.

**edwin:** Hassan, go back if you can.

**Hasan Ahmed:** Yeah.

**edwin:** Um, take out the the dollar sign.

**Hasan Ahmed:** Okay,

**edwin:** Okay. No, no reference to money. There's uh and uh for the record,

**Hasan Ahmed:** cool.

**edwin:** I know Kingaby is gone. I got to do a couple things. We got to make some changes on the website. I'm not detracting from your demo, but there's some language I have to remove or the the

**Hasan Ahmed:** Okay.

**edwin:** regulators. Cool. Keep going,

**Hasan Ahmed:** Yeah.

**edwin:** boss.

**Hasan Ahmed:** And then after you like click show me like it will explain your actual balance and then how it

**edwin:** Mhm.

**Hasan Ahmed:** works and then we go to and then like it will then show you your upcoming games. Um and then from that like it will scroll down it it will as in like it will ask you to then click on the actual markets tab and then like it will explain like each of the team and then like the actual the numbers and then how much and so then if there's like I think as in if there's like the price change it will explain that as well and

### **00:12:54**

**edwin:** Okay, on this one too,

**Hasan Ahmed:** then

**edwin:** I made this one before. We don't want to show any percentages. We just want to see the net change in value.

**Hasan Ahmed:** yeah Okay.

**edwin:** Okay,

**Hasan Ahmed:** Yeah.

**edwin:** cool.

**Hasan Ahmed:** Cool. And then if you click next and then it will ask you to have to tap on a team. I mean at the moment I think sculpt it to NCAA cuz like it's the the only legal page which actually has been trading open as in if you were to click NFL it would just have that placeholder page.

**edwin:** Yeah.

**Hasan Ahmed:** And so then on here if you click on that like it will explain the actual price chart. Um click next and then it'll explain your like your actual shares as well. Then we click that again and then it will ask you if you want to practice like ahead and buy and sell.

**edwin:** Mhm.

**Hasan Ahmed:** And so if you click act as a buy like it will explain like the actual quantity and then how much you would actually pay for it.

### **00:13:57**

**Hasan Ahmed:** And then if you click next as in like it's not going to be an actual buy or an actual sale. It's just going to be simulated. And so you're not actually going to be buying or selling anything.

**edwin:** Yes.

**Hasan Ahmed:** So click buy.

**edwin:** here. Yeah, I ran through that to that point and I I got stuck.

**Hasan Ahmed:** Yeah.

**edwin:** I couldn't hit the bottom because it was too low or

**Hasan Ahmed:** Yeah.

**edwin:** something.

**Hasan Ahmed:** I mean I mean I still need to tweak it a bit for aspect ratios for like certain phones are bigger and smaller and then people have the zoom as well like accessibility zoom and so I need to adjust for that too.

**edwin:** Yes. Yeah. Yeah.

**Hasan Ahmed:** And then if you do a cell,

**edwin:** Yeah.

**Hasan Ahmed:** it will ask you to do the exact same thing.

**edwin:** It was the cell that got me.

**Kevin Murray:** Yeah,

**edwin:** Yeah.

**Kevin Murray:** that's what I

**Hasan Ahmed:** Yeah.

**edwin:** Yeah.

**Hasan Ahmed:** Yeah. Um I'll tweet that as well.

**Kevin Murray:** got.

**edwin:** You go.

### **00:14:36**

**edwin:** Yes,

**Hasan Ahmed:** Um and then and then you click sell like it'll give you the the order ticket and

**edwin:** sir.

**Hasan Ahmed:** then after this it will take you on to the actual the leaderboards and then explain this as well a bit and then how

**edwin:** By the way, that HN whatever that is,

**Hasan Ahmed:** it Yeah.

**edwin:** that's actually me. I didn't know how to change my f\*\*\*\*\*\* ID. So, I don't know. That was like a code I put in.

**Hasan Ahmed:** Yeah.

**edwin:** Sand. know.

**Hasan Ahmed:** Yeah.

**edwin:** So,

**Hasan Ahmed:** Um I mean I mean if you want I mean I can update your actual username like if you if you really want

**edwin:** not great. I mean,

**Hasan Ahmed:** to.

**edwin:** that just looks like an Asian guy right there. We'll just leave it. That'll be my That'll be my page

**Hasan Ahmed:** Yeah.

**edwin:** name.

**Hasan Ahmed:** And yeah, after that like as in it was play like groups as well and then if you want join a group

**edwin:** Cool.

**Hasan Ahmed:** and then have your own like the private challenge for example and then

### **00:15:30**

**edwin:** Great.

**Hasan Ahmed:** Yeah.

**edwin:** All right. Cool. So, remove those dollar signs. Real quick, while you're on the app,

**Hasan Ahmed:** Yeah.

**edwin:** I want you to go somewhere for me, Hassan, because I want you to change something.

**Hasan Ahmed:** Yeah.

**edwin:** Okay.

**Hasan Ahmed:** Okay.

**edwin:** Go to um go to uh trade. Okay. And can just Yeah. Click on like I want to go. So, click on the Falcons here. Just click on them real quick. Where do I go? Oh, do I go to full team data to buy or sell? I click there.

**Hasan Ahmed:** Uh um like if you think click on that. Yeah.

**edwin:** Yeah,

**Hasan Ahmed:** Like it will take you to the actual team

**edwin:** this is where I want you to be. Yeah. Yeah.

**Hasan Ahmed:** page.

**edwin:** Okay. You see how it says Air Force to the left there? Uh on the bottom where it says buy,

**Hasan Ahmed:** Yeah.

**edwin:** sell. Um and then you got that then you have the like whatever like your your name's actually on it.

### **00:16:16**

**edwin:** I can't see that. I can't move that f\*\*\*\*\*\* thing. s\*\*\*. Okay. So, you know how you have the like little disc? That's Air Force AF, I assume. And then there's like a a number or something,

**Hasan Ahmed:** Yeah.

**edwin:** right? What what's right next to it in between that and the

**Hasan Ahmed:** Um,

**edwin:** buy?

**Hasan Ahmed:** like at the moment it's only 10 and then at the little arrow.

**edwin:** Yeah. So when you So like if I click buy right now or sell, I'm giving up the edge to So I'm paying the offer if I click buy and I'm selling the bid, hitting the bid if I if I click sell.

**Hasan Ahmed:** Yeah.

**edwin:** Okay. I mean, uh, that that thing to the left that in between the disc, I, like I said, I can't see it. I know it's normally like a number. Um,

**Hasan Ahmed:** Yeah.

**edwin:** that number is always sticky. So, if let's say I did 1,200 shares on my last trade, um, it's always loaded for 1,200.

**Hasan Ahmed:** Okay.

**edwin:** I think we need to make that loaded to zero after a trade's been done because people are going to get

### **00:17:12**

**Hasan Ahmed:** Right.

**edwin:** really pissed off,

**Hasan Ahmed:** Okay.

**edwin:** you know, doing it. So that that's been one hinky thing cuz it's it that's where I basically click to make myself buy on the bid and sell on the offer cuz I don't I don't want to I don't want to give up an an edge right away. I want I want to you see what I mean? I want I want to work it.

**Hasan Ahmed:** Yeah.

**edwin:** So if I want to place a a passive or resting order,

**Hasan Ahmed:** Yeah.

**edwin:** I got to click that button. And um it's it's slightly intuitive. Um, but like people are going to f\*\*\* it up the first couple times and if they do it on size, it's going to be catastrophic.

**George Westbrook:** If if we set it Oh,

**Hasan Ahmed:** If if we said it's all What?

**George Westbrook:** wait. Can you mute?

**edwin:** Go ahead.

**George Westbrook:** If we if we set it to zero, then there's effectively No one click

**edwin:** Well, um, yeah. I

**Jared Sapirman:** Yeah, I agree with George.

**George Westbrook:** trading.

### **00:18:07**

**Jared Sapirman:** I think the default order that you have in the settings is what should stay

**edwin:** mean,

**Jared Sapirman:** there because it I think it would frustrate a lot of people. It would frustrate me if I was not able to buy. If it was always zero and you always have to go click up because there is yeah effectively no one click trading in that in that

**George Westbrook:** because I think the two so it's purposeful that it's the last traded amount um

**Jared Sapirman:** regard.

**George Westbrook:** which is smart but it's annoying because

**edwin:** Well, let let me ask you this. I hear you. But like let's say, you know,

**George Westbrook:** you

**edwin:** let's say I want to I want to do whatever 500 on Air Force, but then I click over to Alabama. It's still loaded at 500\.

**George Westbrook:** could we could have that What Jared said is there's like a default order amount. Um we I was going to say we could have a default one for buy, default one for sell, but it needs to just be one number.

**edwin:** I just have one.

### **00:19:08**

**edwin:** Yeah.

**Jared Sapirman:** Yeah.

**George Westbrook:** Um we could set we could just at the moment just set it to 100\.

**edwin:** One number.

**George Westbrook:** Um and then look to add it into the settings. So we could we so we could have like a trading settings amount.

**Jared Sapirman:** Well,

**George Westbrook:** Um

**Jared Sapirman:** isn't that there in more already, George? If you click on more, Hassan, isn't there a trading default uh size? I thought we had that. Yeah, default order size right there.

**George Westbrook:** Not going to that's that's not going to I think we added that and then changed it to the last order. So we'll just we'll flip that back.

**edwin:** I mean, I don't know if I want you to flip it back then, but can I get some input from anybody else on this call, please?

**Troy McDonald Kane:** I think it should be the default order size is what it always goes back

**Cody Haugen:** Yeah.

**Troy McDonald Kane:** to.

**Jared Sapirman:** Yeah, that's how it's been. That's how it is.

**Troy McDonald Kane:** That's how it works on other trading softwares too.

### **00:20:08**

**Troy McDonald Kane:** There you put your default order size and it always goes to that.

**Jared Sapirman:** Yep.

**Troy McDonald Kane:** So you can set it at 20, 50, 100, whatever it is. But it's order ticket should always autoload with whatever your default settings are.

**Jared Sapirman:** That's how I do it on Weeble, Robin Hood,

**edwin:** Okay.

**Jared Sapirman:** Thinker Sweet.

**Troy McDonald Kane:** Yeah.

**Jared Sapirman:** That's how I've always done

**Troy McDonald Kane:** Yeah.

**Kevin Murray:** Hassan as well maybe in the the walk through that you've got there maybe have something there where it

**edwin:** Oh.

**Kevin Murray:** says like default size as well just to make people aware that it

**Hasan Ahmed:** Yeah.

**Jared Sapirman:** Yeah, go ahead.

**Kevin Murray:** in that setting well just to give so you're covering all bases

**Hasan Ahmed:** Yeah.

**edwin:** Mhm. Yeah. Okay. I I think that's right.

**Troy McDonald Kane:** Yeah,

**edwin:** Cool. I mean

**Troy McDonald Kane:** I think in the settings there should almost be like a one-click trading like tab that you set all your one-click trading settings.

**Kevin Murray:** Hi.

**Troy McDonald Kane:** Like you want it to always be market.

### **00:21:04**

**Troy McDonald Kane:** You want it to be 100 lot standard size. Like there should be somewhere where you set because that's also very common on trading software is you put in a lot of presets in your so that it's always pre-populating your order tickets.

**Jared Sapirman:** Yep.

**Troy McDonald Kane:** So at the minimum you want quantity and then the ability to default to market on every ticket. So that because it is not consistent either depending on how you're clicking it from what screen. Sometimes market sticks, sometimes market

**George Westbrook:** One quick thing I was thinking about or we were thinking about was on the

**Troy McDonald Kane:** doesn't

**George Westbrook:** quantities. You see where it's got the the 2500 250 is do we want it so that you click that and it goes to that quantity or you click it and

**edwin:** Yeah.

**George Westbrook:** every time you click it it increments it by that amount. So if you wanted to do 125, you click 100, then

**edwin:** Increments.

**George Westbrook:** 25\.

**edwin:** Incremental. You want to be

**Jared Sapirman:** So they have that as trading settings too in in other trading apps that I've used where they have a a default not only just a default order but a default incremental growth button too.

### **00:22:10**

**Jared Sapirman:** So, you would click an I don't know a plus or a minus at some point on the

**George Westbrook:** and

**Jared Sapirman:** quantity. There isn't that right now, but it it would go up by a 100 shares each time you click that plus shares each time you click the minus.

**George Westbrook:** okay. Yeah, that that makes sense.

**edwin:** Oh, nice walk through outside.

**Jared Sapirman:** Um,

**edwin:** That was great.

**Jared Sapirman:** one one issue that I had yesterday with the walkth through is I don't know if Troy sent this over. Did Troy, did you send that over? The thing that Ronex sent over to you?

**Troy McDonald Kane:** What are you talking about?

**Jared Sapirman:** um where if you go to a different screen, so I think it's like four or five clicks through a walkthrough and then you click back, it doesn't go back to the original screen.

**Hasan Ahmed:** Yeah. Um I think spotted that as well like as I was like playing around with it. It's when you So when you click show me next.

**Jared Sapirman:** Yeah.

### **00:23:15**

**Jared Sapirman:** You go past forward, forward, go to the markets page,

**Hasan Ahmed:** Yeah. After you click this and then Yeah.

**Jared Sapirman:** and then if you go back then it doesn't Yeah.

**Hasan Ahmed:** Yeah. Yeah. Um I mean think I think update that. I mean, I already inspired it earlier like I think I think about I think 20 minutes ago.

**edwin:** Cool.

**Hasan Ahmed:** So, I'll get that

**Jared Sapirman:** Okay.

**Hasan Ahmed:** fixed.

**edwin:** And then George,

**Hasan Ahmed:** Yeah.

**edwin:** I sent you over a couple of uh screenshots from my buddy who works at uh that Facebook

**Hasan Ahmed:** Yeah.

**edwin:** Meta.

**George Westbrook:** Yeah.

**edwin:** Um you know, we're still kind of in a limbo of like when people open it up, you know, it's overwhelming to them evidently. I mean, you can read his messages. is I don't want to reread them but the um you know the thoughts are how do we how do we

**George Westbrook:** Hey,

**edwin:** simplify the the you know the onboarding I mean to to a degree I mean for me it's relatively I like I f\*\*\*\*\*\* understand it I mean but that's me you

### **00:24:19**

**George Westbrook:** I think I'm just look at the homepage now.

**edwin:** know

**George Westbrook:** points that yeah it's difficult cuz it's not as if it's a like I appreciate what they're saying and obviously it does need to be simplified. It's just difficult when it's something like trading which is there's obviously a lot of underlying knowledge that's needed. Um it's I'm not suggesting we do this but I'm not suggesting we do this but it's almost like we need different versions of the app for different user levels. Definitely not suggesting we do that because it because it's like say some someone like people

**edwin:** No, no.

**George Westbrook:** on this call where you traded before

**edwin:** So, like when when you look at this homepage, George, here's what I see. The first thing I see is an EIPO.

**George Westbrook:** need.

**edwin:** like you know that the NFL IPO is coming up on the 5th. Um it's it's pretty dominant obviously and if you're going to open up for this weekend for the NCAA um you know there's nothing really on here other than live games or whatever that's like like it it the team IPO thing is overpowering in my opinion.

### **00:25:31**

**edwin:** Um and you can click that and then let's see what I click it. when okay takes me to my favorites and then I'm there but the IPO is like you know it's a function that we need so that these are actual securities like the IPO you know uh it's not that exciting you know Troy said it best he's like you buy them and then you wait so that there's not much to do after you buy them it's it's you know the excitement comes from when you trade them during the games

**Troy McDonald Kane:** Yeah, I think um putting putting a a tile above that that has upcoming games.

**edwin:** Um,

**Troy McDonald Kane:** Like I also noticed that that the college games are not showing up in co, you know, uh upcoming games. It's only the NFL games for some reason. But that's what you should see the first when you when you log in is okay what game like yeah that live games that should be moved up so that that's actually the first thing you see because then you can start clicking on live games and seeing what it all

### **00:26:30**

**edwin:** Mhm.

**Troy McDonald Kane:** looks like in trading. The other thing Hassan is that if it's not a a verified account it's it's I still don't have buying power uh on two accounts that were not verified. One that was created a couple weeks ago and one that was created yesterday. So, how long does it take for buying power to get allocated to an account that's not verified and one that's verified?

**Hasan Ahmed:** Um, as in Um like are these like accounts that are like they on boarded like as in terms of like the teaser on boarded but they are not

**edwin:** Thank you.

**Troy McDonald Kane:** I well I don't they're they're the the the first layer with the the

**Hasan Ahmed:** KYC.

**Troy McDonald Kane:** the 13 and over layer like how do we get the 13 and over layer enabled for

**edwin:** This

**Hasan Ahmed:** Yeah.

**Troy McDonald Kane:** trading?

**Hasan Ahmed:** Um as in cuz like I mean cuz I I mean how I think added in earlier was that it's like a explicit step. So you have to get a trading account like I mean actually I mean actually allocated.

### **00:27:25**

**George Westbrook:** Sorry.

**Hasan Ahmed:** So like I was planning on um having it as like a sort of like automatic step and so after you on board it will allocate your buying power and then on board you onto T0.

**edwin:** Well, can you just have it done After they give you their email and it's been

**Hasan Ahmed:** Yeah. Yeah. So, like I need to do then do that cuz at the moment if I go into an account that Let me quickly switch over to

**edwin:** verified

**Hasan Ahmed:** one. Um I'm just I'm just going through the flow

**George Westbrook:** I'm just I'm just going through the flow now.

**Hasan Ahmed:** now. I didn't create anyone that was released. Um.

**edwin:** Cody. Well, he does that. The the marketing company's going to also look at the app experience,

**Hasan Ahmed:** Uh,

**edwin:** right? and come back to

**Cody Haugen:** Yeah, absolutely. That's a big portion of their stuff.

**edwin:** us.

**Cody Haugen:** Uh I added them to the test flight because um they needed exactly that. So onboarding experience, all all of that, they're going to offer suggestions from from their point of view.

### **00:28:49**

**edwin:** Cool. When do they start placing ads? Do you know?

**Cody Haugen:** uh the first the first campaign you're talking about.

**edwin:** Yeah. the first

**Cody Haugen:** Um because well the first test is going to start in the first two weeks.

**edwin:** test.

**Cody Haugen:** That's when they start testing the hooks and the uh and like the language,

**edwin:** Mhm.

**Cody Haugen:** but it's no graphics. It's just words basically that they're testing to see what resonates. Um and then uh but then like the first actual real campaign

**edwin:** Mhm.

**Cody Haugen:** starts week five.

**edwin:** No, that's not what I'm asking. I'm asking when are they going to start testing ads to to see what we're going to do. like when when will people start seeing that in plays out there even on their b\*\*\*\*\*\*\* little you know $200 a day stuff?

**Cody Haugen:** uh week three.

**edwin:** Okay, week three because we want to make we want to make sure that this is

**Hasan Ahmed:** That's a new account.

**Cody Haugen:** So

**Hasan Ahmed:** Yeah. Um

**edwin:** functioning properly ASAP because you know if we're spending money on advertising and all the rest of it, we've got to have people be able to sign up and not do the KYC.

### **00:29:52**

**Hasan Ahmed:** Yeah, check them.

**Cody Haugen:** Yeah, the weeks one and two are this, you know, onboarding whatever. Um, and then all of their discovery,

**edwin:** Mhm.

**Cody Haugen:** so looking at the app, that type of thing. Week three is when they start testing the the hooks and doing, you know, all that beta testing behind the scenes. Um, and then yeah, week five is like the first real campaign. So that's so weeks three after weeks three and four is when they're going to give us that spreadsheet of suggested spend based on what they found in the research.

**Brett StClair:** Cody, can you give them a nudge just so we can get their login so we can add them to tag manager, analytics, all that kind of stuff? Firebase so that they can put their hooks in.

**Cody Haugen:** Uh, absolutely.

**Brett StClair:** Thank you.

**Cody Haugen:** Sebastian hasn't gotten back to you guys. Obviously not. Um, yeah,

**Brett StClair:** Thanks,

**Cody Haugen:** I will ping him.

**Brett StClair:** dude.

**Hasan Ahmed:** um I mean in terms of the actual the buying power um so I mean at the moment how it is is as soon as it on boards onto the T0 like it needs to go from their think staging API onto

### **00:31:00**

**George Westbrook:** Sorry.

**Hasan Ahmed:** their MS and so if you're going to allocate anything buying power you need to as in you need to sort of and time it as soon as it's on the like MS. And so I think the actual auto like allocation like it's a bit clunky at the moment. I need to iron it out a bit. And so um Troy if you give me those like the two accounts will be a bit like have nothing buying power. I like as in like I I mean I will like actually um allocate the actual buying power to it and then I'll get the auto like allocation sorted out as in like I think I know like a way to get it more like concrete except I need to do a bit more research on

**Troy McDonald Kane:** Yeah,

**Hasan Ahmed:** it.

**Troy McDonald Kane:** I'll send them to I'm more worried about anyone that may have signed up over the last week um without going through the ID verification, you know, expecting those locked feeds to come off uh Saturday or even now that we're we're open for

### **00:31:56**

**Hasan Ahmed:** Yeah.

**Troy McDonald Kane:** secondary

**Hasan Ahmed:** Yeah.

**Troy McDonald Kane:** trading.

**Hasan Ahmed:** I mean um I think like at the moment I can do like a back field and then like check anyone else who like also has no bang power allocated

**edwin:** How

**Hasan Ahmed:** and uh probably about probably about I think um I said half

**edwin:** long?

**Hasan Ahmed:** an hour to an hour like it should be eating pretty quick.

**edwin:** Okay. Okay. Cuz that that that

**George Westbrook:** allocate.

**Hasan Ahmed:** That's to allocate that's to allocate the buying power.

**George Westbrook:** That's to allocate the buying power.

**Hasan Ahmed:** The fix might take a little bit longer.

**George Westbrook:** The fix might take a little bit longer.

**Hasan Ahmed:** Yeah.

**edwin:** How long could it fix

**Hasan Ahmed:** Um,

**edwin:** roughly?

**Hasan Ahmed:** I would say probably a few hours cuz I do have a like idea like in mind and it I believe it should work.

**edwin:** Okay. Okay. That's a critical piece. So,

**Hasan Ahmed:** Yeah.

**edwin:** um doing sooner or better. Um, I agree with Troy though. I think we need to move the uh live games up above the Steam IPO.

### **00:33:03**

**edwin:** Just put them like what? Right underneath simulated trading

**Troy McDonald Kane:** Yeah.

**edwin:** challenge.

**Jared Sapirman:** I think the team IPO should go below the uh portfolio too to be quite

**Troy McDonald Kane:** Okay.

**Jared Sapirman:** honest.

**edwin:** Yeah. I mean it's it's just it's very dominant.

**Jared Sapirman:** And yeah, like what are people doing? They're buying something to then wait for a while. Like you said, Edwin, it's not there's not that's not going to keep people on the app, the IPO itself. So I think that should be lower,

**edwin:** No.

**Jared Sapirman:** substantially lower.

**edwin:** Yeah, I I agree. Okay. Okay. Can you fix those, please?

**George Westbrook:** Yep. So, we got the buying power stuff, move the home page, and upcoming games for NCAA and the walkthrough stuff as

**edwin:** Right. And then Yes sir.

**George Westbrook:** well.

**edwin:** And then what about the market maker? So where do you think we are with the market

**George Westbrook:** is it's going to be going to be quoting the games.

**edwin:** maker?

**George Westbrook:** It's just that that kind of not having it reset after having that tiny bit of memory.

### **00:34:14**

**George Westbrook:** But when I say reset, it's more like price goes up changes during a game and then at the end of the game because the expected wins hasn't changed, it's just going to drop back down to what it was before or that the reference price is going to be the same.

**edwin:** Well, I mean c can't you so when we talk about pricing it like if um you know it's f\*\*\* because that's we don't want anything dropping back down or that's that's that's not going to work. They I'll explain this to you in a way that'll work. So, like I said, there's no game that's played that's 100% probability a team's going to win. Okay? It might be 99.99, but it's never 100 until it's over. So even if even if like you know most of these teams that are playing this weekend green puff you know

**George Westbrook:** Yeah.

**edwin:** they're that what the first game is TCU North Carolina and we said the spread was like 9 and

**Cody Haugen:** Correct.

**edwin:** a half and the money line \- 10 and a half TCU and the money line 9

### **00:35:26**

**Cody Haugen:** Minus was money line was 380 and we had

**edwin:** 380

**Cody Haugen:** 77.3% win probability.

**edwin:** right so George with a $5 value. Okay. If you take 77.3 \* 5 bucks or, you know, 773, it's going to give you roughly $3 um and like86. Okay, that's what it's priced at at the moment. So if they win the game TCU, the price should go up somewhere between 3.86 to $5 for onfield. You follow what I mean? So do you understand what I'm trying to

**George Westbrook:** Yeah.

**edwin:** say?

**George Westbrook:** So you're saying correct me if I'm wrong. There's the the start win probability which is already we make the assumptions it's already

**edwin:** Mhm.

**George Westbrook:** in factored into the expected wins. we have the end result.

**edwin:** Correct.

**George Westbrook:** The change in that is either the increase or decrease of that share

**edwin:** Mhm.

**George Westbrook:** value.

**edwin:** Correct.

**George Westbrook:** That's with one big assumption though, which is that the it's it's that that is the case in

**edwin:** So

**George Westbrook:** that in those expected wins, the win probabilities are factored in. It I think it's a fair assumption.

### **00:36:50**

**George Westbrook:** Um, but it could be diff like different data providers might provide different things. Obviously, it's it's sports radar data. I think correct me if I'm wrong on this, Cody. The win probabilities that doesn't come from say the same betting feed as the expected expected wins does. And then obviously I think with Sports Radar, they provide different expected wins from different different providers.

**Cody Haugen:** Correct.

**edwin:** What do you mean by that? I don't follow that.

**Cody Haugen:** So,

**edwin:** Different expected wins by different providers. There there's there's it's a math equation here.

**Cody Haugen:** uh,

**edwin:** It's not this isn't a um Go ahead. Go ahead. But what what's it? What do you

**George Westbrook:** Well,

**Cody Haugen:** so,

**George Westbrook:** I

**Cody Haugen:** so their odds comparison feed is pulled in from different sports books.

**George Westbrook:** think

**Cody Haugen:** they work with,

**edwin:** say?

**Cody Haugen:** you know, I think in the odds comparison feed, they pull in like 30 of the top sports books around the world. So there is a multitude of answers in that odds comparison feed for win uh totals, projected win totals for each

### **00:37:52**

**edwin:** Sure. Sure.

**Cody Haugen:** team.

**edwin:** But I I mean the the probabilities are generated by sport radar, not the books.

**Cody Haugen:** Oh, right. Yeah. Yeah. So the probabilities feed to George's point is a separate feed and it is the probabilities is generated by sport radar.

**edwin:** Right. And so are the money the money lines. Yeah.

**Cody Haugen:** Now money lines are coming from the sports books direct connections with sport radar as

**edwin:** So, DraftKings makes their money line,

**Cody Haugen:** well.

**edwin:** FanDuel makes their money line, Arrock makes their money line. And and what then Sport Radar takes those and blends

**Cody Haugen:** No. So what I mean really quick what happens is sport radar will create a origination line.

**edwin:** them.

**Cody Haugen:** They'll sell it to all of the the sports books around the world. The big guys have their own live trading team. They will take that sport radar data plus their data and mix it to make the Hard Rock line, the the Win line, the FanDuel, the DraftKings. Then FanDuel, all of those books give it back to Sport Radar, which closes the feedback loop, and that's what creates the life cycle of odds.

### **00:38:58**

**Cody Haugen:** And then sport radar. that's out live odds off of that. So sport radar is the origination line and and or what you would say is the consensus line. So if you're looking at the consensus, I would also use that synonymously as the origination line.

**edwin:** Are all the books using the consensus line then for their live betting feeds?

**Cody Haugen:** They are t that's what they're starting with.

**edwin:** Yeah.

**Cody Haugen:** So then that cycle Yeah.

**edwin:** No, I I get that. I get

**Cody Haugen:** Yeah. So then the cycle continues through their live odds.

**edwin:** that.

**Cody Haugen:** Sport Radar will pitch out a live odd. They'll take that back in live trade it and then keep going.

**edwin:** And then they move their internal lines based on flow and the rest of

**Cody Haugen:** They're of course and they're users and and they need to balance their own book,

**edwin:** it.

**Cody Haugen:** you know, Hard Rock versus FanDuel.

**edwin:** Mhm. Yeah.

**George Westbrook:** and I'd assume the win probability from sports radar is obviously got nothing to do with the the

### **00:39:52**

**edwin:** Okay.

**Cody Haugen:** completely separate.

**George Westbrook:** betting line.

**Cody Haugen:** Yeah,

**George Westbrook:** It's it it's all based on

**Cody Haugen:** completely separate. Yeah.

**George Westbrook:** Yeah.

**Cody Haugen:** Yeah. That is that is just based on live playbyplay and what's happening in the game.

**edwin:** Yeah. Um because we can back into probability if we have live lines.

**George Westbrook:** I don't know if I know what you mean by that.

**Cody Haugen:** If if we have the live odds,

**edwin:** Um,

**Cody Haugen:** we can use the live odds to back into a win probability.

**George Westbrook:** Okay.

**Cody Haugen:** George,

**George Westbrook:** I don't think we we I don't think we have access to the live odds.

**Cody Haugen:** well, it's it's right now it's the media.

**edwin:** so

**Cody Haugen:** It's not the betting feeds that sports books get because sports books are the only companies that are allowed to get it and you need a sports book license. I'm still fighting that good fight with Sport Radar and we've made some progress that they have a precedent set with a a company that is still under a sportsbook license yada yada yada.

### **00:41:07**

**Cody Haugen:** But yes, there is a precedent similar set that I'm trying to exploit and make a case

**edwin:** Right. Well,

**Cody Haugen:** for that we are

**edwin:** I mean, they've got to be given the Talian Poly Market something.

**Cody Haugen:** um they're giving them uh well so they're not using it for

**edwin:** Media

**Cody Haugen:** resulting. They're using it for matchmaking which is obviously what we'd be using it for. Yeah, I'd have to fact check with David what actually is in their contract.

**edwin:** Mhm. Interesting. Okay. Yeah. So, the way that I I when I'm looking at this, George, I'm saying that every game there's some value that can be gained if you win or lose, right? So, like if it's it's if if it's a 77% value that you know ECU is going to beat North Carolina, then you know in in my math that it should be worth somewhere around a $1.14 in terms of their um or up to 114 in terms of their uh price for the season because every game's going to have some form of like, you know, probability that's factored in to get these totals.

### **00:42:25**

**edwin:** the total of like let's say LSU at 9.55, you can't win half a game and you certainly can't win.55 of a game. So, you know, I I was modeling this stuff all around like the probabilities of of each game, right? And then there's an assumption based on like you know historical I would imagine you know that LSU is going to be able to beat Jacksonville State or like you know some smaller school and that those lines even though they're not out yet will likely be um you know 20 or 30 points because like the model I

**Troy McDonald Kane:** I don't care.

**edwin:** built yesterday I was playing with it where you could basically say okay currently LSU is three and three, you know, and they're down 14 points in the fourth quarter. What's their value with two minutes left to go? And I started to get within, you know, a reasonable amount for a reference point. And then if they were like six and0, it was a different price. And um then the rest was based on how many games were available and then who, you know, that strength of what who they were going to play left.

### **00:43:37**

**edwin:** So, um I mean for the first weekend, we're going to have to deal with what what's what. But this this is going to be something that, you know, as soon as everything else gets off my f\*\*\*\*\*\* plate, I'd like to work on um this because this is going to be key to our data sales. Um you know,

**George Westbrook:** Yeah.

**edwin:** I'll probably this might become the most valuable thing we create um that sports books may want to buy from us as well.

**Cody Haugen:** 100% agreed. This is Yeah. Yeah. This is how we could potentially replace a portion of a billion dollar company's

**George Westbrook:** Yes.

**Cody Haugen:** business in a large

**edwin:** Because like where where they suffer like you know there's some benefit to getting the polling from you know eight or 10 books but eight or 10 books who are lopsided on the same way they're going to shade their lines. uh you know, if let's say the public comes out and they're betting the living s\*\*\* out of, you know, uh LSU, um and then everyone, you know, they're all these sharps are hitting them all at the same time because they think they got a weak line, then that line across the board is going to change where the actual value of the marketplace um might Not.

### **00:44:59**

**edwin:** Because believe it or not on the sports betting you can move lines with not that much money depending upon when you make those bets.

**Cody Haugen:** Yeah,

**edwin:** I guess the same thing would apply in market.

**Cody Haugen:** it comes it comes back to the same

**edwin:** I

**Cody Haugen:** uh unique prepping or uh selling proposition that we have for single liquidity.

**edwin:** guess

**Cody Haugen:** They're fragmented. So like what Edwin is saying is FanDuel will move to balance their book where hardline or hard rock sorry will could move the other direction. So it's it even pulling it in, you're not getting a large data set. You're getting two smaller fragmented data sets. Since we are a single liquidity pool, all of those people being in one, we actually are a truer source of a larger subset of data. So just like we we sell to our users as a as a proposition of coming to us as a single liquidity pool and not having to go to those different places, the data sets and buying our data sets is also the same selling proposition.

### **00:46:01**

**Cody Haugen:** Does that make sense?

**edwin:** Yeah.

**Cody Haugen:** Yeah.

**edwin:** All right. Well, we can we can argue about this later.

**Cody Haugen:** I was gonna say I can pick it up uh later.

**edwin:** Um I

**Cody Haugen:** I gota I'm pretty late to this call here so I got to jump.

**edwin:** Yeah, Steve. Okay. Um All right. Uh what else? Anything else for

**Jared Sapirman:** I have one other thing. Um, George,

**edwin:** today?

**Jared Sapirman:** I don't know if Cody sent you the uh feedback I had on a lot of the different codes and anagrams and the colors of the different teams that

**George Westbrook:** Yeah.

**Jared Sapirman:** are wrong. He

**George Westbrook:** Yeah. Got the got the the names.

**Jared Sapirman:** did

**George Westbrook:** Um I don't think we got anything through the colors. I'll double check. Um but we can rerun that again. The the the team updating is the the text updating is pretty easy. So we'll get on to that.

**Jared Sapirman:** Okay.

**edwin:** What team was wrong

**Jared Sapirman:** Oh, a lot.

### **00:46:57**

**Jared Sapirman:** I I can tell you Notre Dame,

**edwin:** here?

**Jared Sapirman:** it said Notre Dame was uh a part of the ACC, which they are not. They're independent. Louisiana Tech, their color is red when they're actually blue. um Yukon, their um moniker or anagram was UC N on the app, which it's not. It's actually co-n um Charlotte is not right. It's CLT going on the app. It's C H A R. There's probably 15 others.

**edwin:** Okay. Okay. Well, those are detailed things you can figure out.

**George Westbrook:** Yeah.

**edwin:** All right.

**George Westbrook:** Yeah, they'll be they'll they'll relatively easy to

**edwin:** Awesome. Sure. Sure.

**George Westbrook:** fix.

**edwin:** Okay. Um, anything else from Novo side for us?

**George Westbrook:** I think that's I think that's everything.

**edwin:** Cool.

**Brett StClair:** Yeah.

**Troy McDonald Kane:** Yeah.

**edwin:** Anything from inlay side?

**Troy McDonald Kane:** No,

**edwin:** Great.

**Troy McDonald Kane:** just getting the trading uh layers better or which I That was what you'll work on

**edwin:** Okay, cool. Well, I'm wishing all of you a great great weekend and thank you very much for the hard work.

### **00:48:00**

**Troy McDonald Kane:** today.

**edwin:** Um, we'll see. Tomorrow is going to be an interesting day. So, that's going to be a lot of fun. Um, in the event that there's any kind of um problem,

**Brett StClair:** Let's

**edwin:** will anyone be around?

**Jared Sapirman:** I

**George Westbrook:** And yeah, there'll be I think there'll be one at least one of us on

**edwin:** No. Cool.

**George Westbrook:** standby.

**edwin:** I mean, I'm not anticipating problems,

**Brett StClair:** see.

**Jared Sapirman:** Oh,

**edwin:** but you never know. Cool. Awesome. All right. Well, I think uh I think Lily should say at this point, right?

**Brett StClair:** Let's f\*\*\*\*\*\* go.

**edwin:** There you go.

**George Westbrook:** You got to shout.

**edwin:** All right.

**George Westbrook:** You got to shout it, Lily.

**edwin:** All Listen,

**George Westbrook:** You got to shout. Let's f\*\*\*\*\*\*

**Brett StClair:** Johnson.

**George Westbrook:** go.

**Brett StClair:** You on

**George Westbrook:** You're on mute.

**edwin:** I shouted at I I've shouted at women uh once and that was a mistake.

**George Westbrook:** You're on mute.

**Brett StClair:** mute.

**edwin:** I've never done it again.

**Lily StClair:** I'm not sure what I'm supposed to say.

**George Westbrook:** Let's f\*\*\*\*\*\*

**edwin:** No,

**George Westbrook:** go. That's what you got to say.

**Lily StClair:** Okay,

**edwin:** you Thank you.

**Lily StClair:** let's f\*\*\*\*\*\*

**George Westbrook:** Let's f\*\*\*\*\*\*

**Lily StClair:** go.

**edwin:** That that that's what we needed.

**Brett StClair:** Love it.

**George Westbrook:** go.

**edwin:** We needed that special touch. Um thank you, Lily. Have a good weekend all. If anyone needs anything, let me know. And um we will all chat later.

**George Westbrook:** Thanks. Have a good one.

**edwin:** Thank you.

### **Transcription ended after 00:49:40**

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*