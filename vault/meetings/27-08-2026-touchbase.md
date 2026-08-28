---
date: 2026-08-27
type: general
description: "Touchbase, 27 August 2026: Edwin reverses two settled positions, the IPO holding structure and price locked to win probability, in a call cut short by the tZERO go-live."
source: "Google Meet transcript, Touchbase Touchdown (13m 25s, ended early)"
scope:
  - "[[market-maker/market-maker]]"
  - "[[ipo-module/ipo-module]]"
  - "[[earnings-report/earnings-report]]"
status: partially-extracted
extracted-to:
  - "[[market-maker/decisions]]"
  - "[[market-maker/open-questions]]"
  - "[[market-maker/sessions/2026-08-27-touchbase-digest]]"
  - "[[ipo-module/ipo-module]]"
  - "[[earnings-report/earnings-report]]"
  - "[[delivery/requirement-changes]]"
---

## Post-Call Analysis

13 minutes, on the morning secondary trading opened. Present: Edwin, George,
Troy, Cody, Jared. **The call was cut short by Troy** for the tZERO call, which
he described as _"the final call before we go live with secondary trading"_.
Edwin's closing words were _"let's come back to this because this is very
important"_, and the conversation has not resumed.

⚠ **Status is `partially-extracted` deliberately.** Two of the biggest items on
this call were mid-explanation when it ended. Nothing here should be treated as
settled until the conversation is finished.

**This is the densest market-maker call since 17 August, and it reverses two
positions the vault records as settled.** Both reversals are Edwin's, both are
defensible, and both arrive three days before the first live games.

### 1. The IPO holding structure is backwards, and NFL changes

George described what we built: the **maker** held all the shares and placed the
sell orders, the **taker** bought. Edwin, flatly: _"So that's backwards."_

He then walked through the real structure. The team company sells its shares. A
broker dealer handles the sale, which is **InPlay Markets**, over tZERO's ATS.
They put up a million shares but sell only 600,000. **The unsold 400,000 do not
go to anyone: they sit in the team company's treasury.** His framing is worth
keeping: _"It's actually an asset like a bank account, but it's a securities
account… a securities bank account."_ The maker in this model is the **selling
agent** providing two-sided liquidity, and crucially _"they don't have to do the
short locates. So they're not getting short, they're just selling."_

He accepted the current build for now, _"it's okay for now. Good sim"_, and then
gave a direct instruction for the next offering:

> **"Right now for this instance, the taker is the buyer. But for the NFL, let's
> make it the maker be the buyer."**

⚠ **This is a structural change to the offering, ten days before the NFL
offering opens, and it lands on the module the last two touchdowns already
flagged as carrying open inventory questions.** See [[market-maker/decisions]]
and the new **E54** in [[market-maker/open-questions]].

**Troy disputed the terminology and took it offline.** He argued the group keeps
saying "maker" as though it is passive, when a market maker does _"both the
taking and the making including making the shares available"_, which is how a
company going public works with a designated market maker in equities. Reg A
means "designated" cannot be used, but _"liquidity provider"_ or _"selling
agent"_ can. He also said something that should not be lost: _"there's still a
little misunderstanding about how the accounts get created."_ Edwin agreed to
come back with cleaner language.

### 2. Treasury is real again

The vault's requirement-change register records the treasury holdback as
**retired** on 12 August, and notes the app removed a field it had built for it.
Edwin has now described treasury as an operating part of the structure, holding
the unsold 400,000 shares as a securities account.

**That makes it a re-reversal**, the second in the register after subscription
billing. It also gives **N21** (are the unoffered NCAA shares issued or
treasury?) a direction it has been waiting on since 29 July, which is the useful
half of the news.

### 3. The price must not be locked to win probability

The vault records a confirmed decision from 23 July: _"In-game price driver =
Sport Radar live win probability, pulled directly. No own event-weight algorithm
in v1."_ Edwin has now contradicted it directly: **_"the prices cannot be locked
to win probability."_**

His worked example is the clearest statement of the valuation model he has given.
A heavy underdog wins 70 to nothing. Win probability reaches 100%, so a
probability-locked price stops at $5. But the market's view of that team has
changed: _"Oh man, this team is amazing… they're going to win more games coming
up."_ The share should go to perhaps $10. His conclusion: **the per-game price
range should be roughly zero to $12**, and the price is _"based on the market's
expectancy of the value of that share over time"_, not on the probability alone.

George conceded the gap plainly: _"in practice that's not how it's working… at
the moment that's not being included in how the maker's pricing."_

**The mechanism he proposed in reply is the important part, and it is testable.**
Expected wins per season should **move after a game**: a 70 to nothing win raises
the team's expected wins, which feeds the price, and separately the next game's
win probability arrives from Sportradar. ⚠ **George then named the blocker:
NCAA expected wins is currently static**, which is the same broken Sportradar
futures endpoint already tracked as **S12**. So the correction Edwin wants
depends on the feed that has been down for a fortnight.

Edwin was mid-example, walking through North Carolina versus TCU (TCU favoured by
nine and a half, roughly a 270 to 275 moneyline, which he put at a win
probability in the high teens to low twenties), when the call ended.

### 4. Trading volume is never public

A firm instruction with a clear anti-gaming rationale. **No trading volume is
shown publicly on any team.** Edwin: _"We don't want someone to look at the
trading volume and say, oh well, they're at 2 million and this guy's at 200,000,
I'm going to buy this one because they're going to get 90% of the off-field."_
The off-field price stays _"a mystery until Tuesday"_.

The off-field mechanic itself was confirmed in one line by George and accepted:
trading volume during a game, allocated proportionally, $250, **excluding both
maker and taker activity**.

### 5. A scope addition that the client withdrew himself

Edwin asked whether he could act from the admin panel during a live game, to
**tighten or move the maker's bid-ask**, because the spread is standardised and
has not been tuned for late-game or game-specific variables. George said it might
be difficult. Edwin's initial reply was _"now is not the time to make anything
difficult"_, and then he reversed himself entirely:

> **"If there's any kind of change, then don't. Just make sure that the market
> maker's up. I don't want to make any changes whatsoever until we have this
> secondary market up and trading."**

And when George offered to look anyway: _"Before you do that, George, you got
enough on your plate. Let's just get through this weekend and make sure that
we're launched."_

**Worth recording as a positive.** This is the first in-window ask in the record
that the client withdrew on his own judgement. It goes in the requirement-change
register as a **held** item rather than a change.

| Finding | Destination | Action |
|---------|-------------|--------|
| **IPO holding structure is backwards; for NFL the maker becomes the buyer** | [[market-maker/decisions]], [[ipo-module/ipo-module]] | Decision + new E54 |
| Real structure: team company sells, InPlay Markets is the broker dealer, maker is selling agent | [[ipo-module/ipo-module]] | Recorded |
| Maker as seller does not need short locates | [[market-maker/decisions]] | Recorded |
| **Treasury is real: unsold shares sit in a team-company securities account** | [[ipo-module/ipo-module]], [[market-maker/open-questions]] | Re-reversal, N21 given direction |
| Troy disputes the terminology, will return with cleaner language; account creation misunderstood | [[market-maker/open-questions]] | New E55 |
| **Price must not be locked to win probability**, supersedes the 23-07 decision | [[market-maker/decisions]] | Supersession recorded |
| Per-game price range roughly zero to $12; price reflects expectancy over time | [[market-maker/decisions]] | Recorded |
| Expected wins must move after a game and feed the price | [[market-maker/decisions]], [[market-maker/open-questions]] | New N54 |
| **NCAA expected wins is static**, blocked on the same broken feed | [[market-maker/open-questions]] | S12 linked |
| **Trading volume never shown publicly**; off-field a mystery until Tuesday | [[earnings-report/earnings-report]] | Requirement written |
| Off-field: game trading volume, proportional, $250, excluding maker and taker | [[earnings-report/earnings-report]] | Confirmed |
| Admin-panel bid-ask control asked for, then **withdrawn by Edwin** | [[delivery/requirement-changes]] | Held, recorded |
| Credit terms from team companies to makers, to top off inventory | [[market-maker/open-questions]] | New E56, exploratory |
| Second maker implementation being tested in the background today and tomorrow | [[market-maker/plan]] | Recorded |
| Call ended early for the tZERO go-live call; conversation unfinished | Not applicable | Resume owed |

---

Aug 27, 2026

## **Touchbase Touchdown \- Transcript**

### **00:00:00**

**edwin:** That was very very

**George Westbrook:** Yeah. Okay.

**edwin:** good.

**George Westbrook:** Yeah, that's because we're what we're doing is testing another version of the maker. It will look, feel, act exactly the same. Um will just be a bit better. Um but that's that's in the that's in the background.

**edwin:** Okay.

**George Westbrook:** Um so testing that today and tomorrow. Um and then

**edwin:** And from my ad from my admin panel,

**George Westbrook:** hope Yeah.

**edwin:** I will be able to like if I'm I'm on a game and let's say I'm watching the game or I'm I'm, you know, watching how the flow of orders is going and I I want to execute, I can still execute in these live games. Correct.

**George Westbrook:** I think so. I'll need to double check. But why would you why would you want to do

**edwin:** So,

**George Westbrook:** that?

**edwin:** um there there may be a time where the acre maker um I like I don't want to say um because we have a standardized market maker bid offer with okay and we haven't really uh drilled it down

### **00:01:06**

**George Westbrook:** H.

**edwin:** for later in the game or variables related to the game. There may be a time or place where I may want to tighten it up

**George Westbrook:** Ah.

**edwin:** or move it.

**George Westbrook:** On on the maker.

**edwin:** Well, aren't I aren't I the shares I bought on the IPO? Aren't they all on the maker side?

**George Westbrook:** No, they're the

**edwin:** Okay, they're the taker.

**George Westbrook:** taker.

**edwin:** Okay, so the taker has all of these in that's who has the inventory right now.

**George Westbrook:** Yeah. So, we that's what we said. So, the the way the IPO work was the the maker held all the shares technically placed the sell orders.

**edwin:** Yeah.

**George Westbrook:** So,

**edwin:** So that's that's backwards.

**George Westbrook:** anything left anything

**edwin:** So that it's okay for now. Good sim. That's good. That when when you sell shares at an IPO, it's not the maker who has the shares. Okay. That it's actually the entity that is selling the shares. Right.

**George Westbrook:** Yeah.

**edwin:** Now the maker I guess we could say acted as the uh selling agent.

### **00:02:12**

**edwin:** Um but ultimately the makers who in in production if we if we top off these IPOs the maker is going to want to hold the inventory not the taker because the exchange can have a relationship where with the maker where some of this stuff um you know they may get

**George Westbrook:** Yes.

**edwin:** financing or special uh rates in order to uh to top off the inventory to ensure it's it's clean.

**George Westbrook:** Yeah. Because I I think what because I suppose that's where we painted the idea where it's the the treasury or what whatever the the entity sells the shares, then the taker, the users take some, and then the maker would take whatever was left over. So, we just thought what's simpler is the maker just owns all of them cuz it's sim. It plays.

**edwin:** Let let me let me let yeah for this let let me walk you through

**George Westbrook:** This is the sell orders and then the taker buys what it needs and the users and the maker has what's left

**edwin:** how yeah let me walk you through how it'll work in real because we're we've missed a step.

### **00:03:05**

**George Westbrook:** over.

**edwin:** So, um, the the the the company, the team sells the shares, okay? They go to a broker dealer who's going to handle the sale. That's going to be uh inplay markets, okay? And we're going to sell them by way of the T0 infrastructure, okay? Their ATS. So, um, ultimately they're going to sell they put up a million shares, but they're only going to sell 600,000. Great. um of the 400,000 those don't go to anyone. They sit in the treasury of the team company. It's actually an asset like a bank account, but it's a securities account. Think of the treasury as just like in this instance just a bank account for all the shares that haven't been sold because they're available in the market.

**George Westbrook:** Thanks.

**edwin:** The other 600,000 a value created. So that 400,000 that remain unsold, they actually are worth something.

**George Westbrook:** H

**edwin:** So it's just a securities bank account. Um so you know they put the shares onto the the platform. Um and inplay markets is basically the platform and then the the maker who is going to be providing two-sided liquidity buying and selling because they're going to potentially own some of them.

### **00:04:33**

**edwin:** They don't have to do the short locates. So they're not getting short, they're just selling. So, you know, I'm I'm trying to figure out a way that um I can extend credit terms from the team companies to the makers so that we can have an easy top off on the the the the amount of shares sold per team. So, I I haven't gotten that approved from regulatory and I'm still in the framework of what like you know how we could do that um without like violating any kind of regulatory laws or anything like that. So, um, but yeah, so right now for this instance, the taker is the buyer. Um, but for the NFL, let's make it the maker be the buyer.

**George Westbrook:** Okay,

**edwin:** Cool. Sorry,

**George Westbrook:** perfect.

**edwin:** Troy. Are you good with

**Troy McDonald Kane:** Yeah,

**edwin:** that?

**Troy McDonald Kane:** I'm still not I mean I still think we're we're not saying the right or using the right terms. I mean it's the same we'll we'll take it offline. I mean I think the we keep using the word maker because it's a passive activity but the market maker is actually doing both the taking and the making including making the shares available.

### **00:05:49**

**Troy McDonald Kane:** At least that's how it works in the equities markets now. So when a a company goes public, they have to work with the market maker to bring those shares to market as the exclusive or the designated market maker. Obviously these are reggg a so we can't say designate it but we can say liquidity provider we could say you know uh selling agent or whatever we want to call it but there's still I think there's still a little misunderstanding about how the accounts get created

**edwin:** Okay. Well, we'll we'll we'll go back on our side and come back to you with cleaner language. I mean, I I Yeah, we'll we'll make it work. Let's just make sure that um on my admin panel if if possible. Let's I want to make sure that I can do things if I want to tighten up bit ask.

**George Westbrook:** That that might be that might be difficult. I'll have a look that that yeah

**edwin:** Okay. Well, listen. Now is not the time to make anything difficult.

**George Westbrook:** that

### **00:06:48**

**edwin:** If there's any kind of change, then don't. Just make sure that the market makers up. Okay. I I don't want to make any changes whatsoever until we we have this,

**George Westbrook:** okay

**edwin:** you know, secondary market up and trading.

**George Westbrook:** I think there might be something I can do. We need to test it. I it might not be as big as I think it is. It's just we're changing a few things. We can test on the new one.

**edwin:** Yeah. You know what? Before you do that,

**George Westbrook:** Um,

**edwin:** George, you got enough on your plate. Let's just get through this weekend and and make sure that we're launched, right? You know, so

**George Westbrook:** perfect. Um, I think so. Yeah,

**edwin:** Okay.

**George Westbrook:** we got the the offfield performance. Got a good idea of that. It's I suppose it's just simple trading trading volume during a game. Allocate proportionally 250\. take out the maker the taker activity and obviously maker activity.

**edwin:** Yes. And just just to cover our basis here,

### **00:07:37**

**George Westbrook:** Um

**edwin:** we know that we're not going to show publicly any trading volume on any of these, right? So that's a mystery.

**George Westbrook:** yeah.

**edwin:** We don't want anyone to know what trading volume is because we don't want someone to look at the trading volume and say,

**George Westbrook:** Okay.

**edwin:** "Oh, well, they're at 2 million and this guy's at 200,000. I'm going to buy this one because they're going to get 10% 90% of the the trading volume uh the off field. We want that price to be a mystery until Tuesday.

**George Westbrook:** Yeah. Okay. And so the off-field performance that's during a game is effectively the previous one that's dictating the price. So the only thing during a game which is changing the price is the the only thing that's changing the price is the win probability and

**edwin:** No, no. I mean, we we still have the expectation.

**George Westbrook:** then

**edwin:** I mean, for these purposes, I I I don't want to confuse things, you know, in in reality,

**George Westbrook:** okay

**edwin:** the answer is no because it's not win probability.

### **00:08:50**

**edwin:** It's, you know, how big they win. Remember the price the prices cannot be locked to win probability. So, let me walk you through an example. So, win probability is what the bid offer during game could be for a period of time, but it's it's a reference point. If by chance a team wins, you know, 70 to nothing and they were an underdog, that team's that the value of that share should be higher than even $5. They the win probability will be 100%. But reality is the market's going to say,"Oh man, this team is amazing. They're not s\*\*\*." So they're going to win more games coming up. So maybe that share goes up $10. And that's what I keep saying is that the the range in price on a per game basis should be somewhere between, you know, zero and, you know, maybe $12. So it it's it's not just based on the win probability.

**George Westbrook:** H.

**edwin:** It's based on the market's expectancy of the value of that share over time. Right?

**George Westbrook:** Okay.

**edwin:** We've we we've gone through this a bunch.

### **00:10:02**

**edwin:** Are you following or

**George Westbrook:** Okay. Yeah. Yeah. I I know what you mean.

**edwin:** no?

**George Westbrook:** I just I'm in my head I'm thinking the how the price for the maker's currently working it out and the Yeah, I I'll have a look. I'll have a think and then come

**edwin:** Well, here look at it like this. Let me give you something to think about,

**George Westbrook:** back.

**edwin:** you know, consider what you what you do. Let's say a team wins this weekend. Okay, let's take the one game, North Carolina versus TCU. Cody, do you know the spread on the game?

**Cody Haugen:** Yeah, let me pull back up

**edwin:** Let him pull it up and I'm going to walk you through this real

**Cody Haugen:** here.

**George Westbrook:** because because I think I I I know what you mean.

**edwin:** quick.

**Jared Sapirman:** I still

**George Westbrook:** I think in in in practice that's not how it's it's working.

**Jared Sapirman:** Yeah.

**George Westbrook:** Um but I get conceptually what you mean in that if somebody wins big,

**edwin:** But um

### **00:10:49**

**George Westbrook:** it's going to have a big implication on what their future win probabilities are going to be,

**Cody Haugen:** Yeah.

**George Westbrook:** which is then going to have an influence on the price.

**edwin:** right so

**George Westbrook:** But I think at at the moment that's not being included in how the makers

**edwin:** right

**Cody Haugen:** TC is favored by nine and a

**edwin:** I understand but nine and a half that's so what's that

**George Westbrook:** pricing

**Cody Haugen:** half.

**edwin:** like a 280 money

**Cody Haugen:** Uh yeah, like 270\. Yeah,

**edwin:** Wow. Okay. All right. So,

**Cody Haugen:** 275\.

**edwin:** and that's going to put our probability at like uh you know uh low 20s, high teens.

**George Westbrook:** cuz cuz

**edwin:** Do we have a win probability on that game anywhere?

**George Westbrook:** I cuz

**Cody Haugen:** Let me look in the

**George Westbrook:** I think so where where I can see what you're saying working is so at

**Cody Haugen:** app.

**George Westbrook:** the start we got expected expected wins per season. um then the probability of that game cuz from sports radar we pretty much only get

### **00:11:46**

**edwin:** Correct.

**George Westbrook:** the win probability for the upcoming game um but not in the future.

**edwin:** Each game correct.

**George Westbrook:** says pretty much just that game.

**edwin:** away.

**George Westbrook:** So the expected wins per season I'd assume should change given the like so let's say one team wins 70 70 nil what should happen after the game is the expected wins per season goes up which is going to influence the price um and then obviously the win probability of the next

**edwin:** That's

**George Westbrook:** game one of the issues that we've got is the expected wins for NCAA at the moment

**edwin:** right.

**George Westbrook:** is static like I think I literally just checked before the call and we've only got 13

**edwin:** No, that's okay. That's okay because I'm going to walk you through on on how this will

**Troy McDonald Kane:** So,

**edwin:** work.

**Troy McDonald Kane:** sorry Edwin, I don't mean to cut you off, but we actually have a call with T0 right now. Is there any way that we can come back to this after that call?

**edwin:** Yeah, let's come back to this because this is very important.

**Troy McDonald Kane:** Yeah, that's why I didn't want So,

**edwin:** Okay.

**Troy McDonald Kane:** we'll be on that call right now. It'll probably only be like 10 or 15 minutes. It's the final call before we go live with secondary trading. Then we can jump back on this this

**edwin:** All right. Sounds good. We'll talk.

**Troy McDonald Kane:** group.

**George Westbrook:** Yeah.

**edwin:** Uh yeah, just let me know and uh I'll see you guys when you're ready.

**Troy McDonald Kane:** All right.

**edwin:** All right. See you.

**Troy McDonald Kane:** Thank you.

**edwin:** Bye. Thank you.

**George Westbrook:** Perfect.

**edwin:** But

**George Westbrook:** Close out of that call.

### **Transcription ended after 00:13:25**

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*