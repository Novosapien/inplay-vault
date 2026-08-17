---
date: 2026-08-17
type: standup
description: "Monday touchdown, 17 August 2026: the weekend was better, but the commercial position hardened. Precise market-maker parameter changes, score-based interim pricing, and the pre-offering surface reduction."
source: "Gemini meeting notes, Inplay - App - Touchdown"
scope:
  - "[[market-maker/market-maker]]"
  - "[[ipo-module/ipo-module]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[information-layer/sub-components/discovery-home/discovery-home]]"
  - "[[advertising/advertising]]"
  - "[[delivery/delivery]]"
status: extracted
extracted-to:
  - "[[market-maker/decisions]]"
  - "[[market-maker/parameters]]"
  - "[[market-maker/open-questions]]"
  - "[[ipo-module/ipo-module]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[information-layer/sub-components/discovery-home/discovery-home]]"
  - "[[information-layer/sub-components/single-game-page/single-game-page]]"
  - "[[advertising/advertising]]"
  - "[[compliance/regulatory-positioning]]"
  - "[[delivery/delivery]]"
---

## Post-Call Analysis

~45 minutes, five days before the offering. Present: Edwin, Cody, Troy, Jared, Kevin, Gary (InPlay) and Brett, George, Max (Novosapien). Markedly calmer than Friday, and far more useful: Edwin opened with _"the weekend was better"_ and then spent most of the call specifying fixes rather than questioning the enterprise.

He remains unresolved on launch readiness, _"I don't know that we're in a place to launch yet"_, and separates the two dates cleanly: the offering on the 22nd is survivable, but _"we still need quite a bit of ground to cover before the 29th"_ when trading actually starts. **Treat the 29th as the real bar, not the 22nd.**

**The commercial picture hardened, and it is the most important thing in this call.** Signups stand at **154**, which he compared unfavourably with a simulation he ran himself two years ago that drew 600 on a $25,000 spend. The tZERO commercials have moved from free to a **$20,000 per month minimum platform fee for the simulation and $150,000 for production**, and the original structure gave tZERO a share of advertising revenue, which no longer exists to share. His own projection is **5,000 to 10,000 users at best**, of whom perhaps a couple of hundred convert to production, which against a run cost of one to two million puts customer acquisition around **$4,000 a head**. His conclusion, stated soberly rather than angrily: _"this iteration is just going to be a complete loss for me."_

Two structural points fall out of that and both need holding. First, **more users currently makes the economics worse, not better**: _"even if we had 50,000 people, we have absolutely zero way to monetize them at the moment. So the more people that sign up is the more people I have to pay."_ Second, **production needs external market makers or it needs Edwin's balance sheet**: without committed market makers he would have to make markets himself on roughly 14 teams, at a capital requirement he put at **$25 to $30 million**, which he described as outside his zone.

He was direct about the cause: the advertising revenue that justified building at this pace _"at best was totally misunderstood, at worst it was duplicitous information"_, and he is _"pretty furious about it"_. Recorded because it is the root of the current position, not as blame to be actioned.

**The market-maker changes are specific, quantified and the most valuable engineering output of the call.** Edwin's diagnosis of Saturday: the book was _"like cement"_, too tight to the win probability, with no room for a two-way market. He compared it to trading the ten-year note, where an edge is a miracle and you do not want it when you get it. His prescription is in the decisions log and the parameters registry: widen the spread, shrink the maker's resting size, and materially increase the taker's size and willingness to cross multiple levels. The logic is worth keeping in his words: _"if you buy 30 into an 11,000 lot it doesn't mean anything. But if you bought 11,000 into a 30 lot, the market's going to be crazy."_

**The subtlest and most interesting request is score-based interim pricing.** Sportradar's win probability lags the score, sometimes by ten seconds after a touchdown, and Edwin identified that as an exploitable asymmetry: _"everyone can buy on scores and then they'll have an unfair advantage... stale data is a death knell."_ His fix is to sample the score as well as the probability, assign a dollar value per point, and move the reference price immediately on a score change as a **placeholder that survives only until the next probability arrives**. He accepts it will be imperfect and rather likes the consequence: a visible mispricing is itself a trading event. He is deriving the per-point values from NFLverse data going back to 1999 and will supply them this week. **Consequence for us: the market maker now has to consume play-by-play, not just probabilities.**

Also of note: the Gamecast was **praised on speed**, displaying several seconds ahead of television in Edwin's case, which is worth recording alongside Friday's downgrade of its trading edge. The two are compatible: fast and informative, but not an edge.

| Finding | Destination | Action |
|---------|-------------|--------|
| Signups at 154; below a self-run simulation two years ago | [[delivery/delivery]] | Recorded |
| tZERO commercials: $20k/month simulation, $150k production; ad-revenue share now moot | [[delivery/delivery]], [[tzero]] | Recorded |
| Projection 5,000 to 10,000 users; ~$4,000 customer acquisition; iteration a loss | [[delivery/delivery]] | Recorded |
| More users currently worsens economics, since there is no monetisation | [[delivery/delivery]] | Recorded as the core structural problem |
| Production needs external market makers or ~$25 to $30m of Edwin's capital for ~14 teams | [[market-maker/market-maker]], [[delivery/delivery]] | New, significant |
| **Widen the maker spread to 8 to 12 ticks** | [[market-maker/parameters]] | Parameter change |
| **Reduce maker resting size to 500 to 3,000** from ~10,000 | [[market-maker/parameters]] | Parameter change |
| **Increase taker size to up to 5,000 and let it cross multiple levels** | [[market-maker/parameters]] | Parameter change |
| Intra-game price swing should reach ~$1.50 to $8 per share, not a couple of dollars | [[market-maker/parameters]] | Target recorded |
| **Score-based interim pricing** between probability updates, per-point dollar values owed by Edwin | [[market-maker/decisions]], [[market-maker/open-questions]] | New requirement + new open item |
| Market maker must now consume play-by-play (quarter and score) | [[market-maker/decisions]] | Scope addition |
| Post-game oscillation risk if expected wins do not update promptly | [[market-maker/open-questions]] | Raised by George, accepted as tolerable |
| Continuous simulation games on the test tickers so live trading is always testable | [[market-maker/plan]] | Testing improvement |
| Three-way choice on first open: free 13+, private competitions, prize competition | [[customer-onboarding/customer-onboarding]] | Requirement, before 22 Aug |
| IPO page per team: shares available, buy only, sell button locked with an explanation | [[ipo-module/ipo-module]] | Requirement, before 22 Aug |
| Edwin will manually buy the majority of each team's shares at the offering | [[ipo-module/ipo-module]] | Confirms the execution-interface need |
| Surface reduction: money first, live games, news behind an icon, drop the discover page | [[information-layer/sub-components/discovery-home/discovery-home]] | Requirement |
| Remove the floating orange trade button everywhere | [[trading/trading]] | Requirement |
| Permanent scroll-under header on the game page | [[information-layer/sub-components/single-game-page/single-game-page]] | Requirement |
| Gamecast validated on speed, several seconds ahead of TV | [[information-layer/sub-components/single-game-page/single-game-page]] | Recorded |
| Testing-the-waters disclosure: info button plus the intro page, not every surface | [[compliance/regulatory-positioning]] | Decision |
| Video advertising over the field during timeouts, with trading still live below | [[advertising/advertising]] | Idea recorded |
| Prop-trading firms approached for ~$5k trader-recruitment access at universities | [[delivery/delivery]] | Idea recorded |
| Edwin: "if I say I want it this way, just do it that way" | [[delivery/delivery]] | Recorded against the reversal position |
| Weekend games were blowouts, so price action was flat and the test was limited | [[delivery/delivery]] | Recorded |

---

Aug 17, 2026

## **Inplay \- App \- Touchdown \- Transcript**

### **00:00:39**

**George Westbrook:** Good morning. How are we all

**Jared Sapirman:** Morning.

**George Westbrook:** doing?

**Cody Haugen:** Hello there. Sorry, one

**Brett StClair:** Hello everybody.

**Cody Haugen:** second.

**Brett StClair:** Freddy, did you have a haircut?

**Cody Haugen:** Sorry, Brad. Was that to me?

**Brett StClair:** Yeah. Do you have a

**Cody Haugen:** Uh, yeah. Yeah, I got a haircut what,

**Brett StClair:** haircut?

**Cody Haugen:** like a week ago, maybe a little longer than that. I just still wear my hat a lot. But, uh, we have a a podcast interview after this, so I figured I'd spritz up a little bit.

**Brett StClair:** Nice. Who's the interview

**Cody Haugen:** Um,

**Max Kingaby:** Nice.

**Cody Haugen:** kind of a weird dude,

**Brett StClair:** with?

**Cody Haugen:** so we'll see how it goes.

**George Westbrook:** Sorry, Max.

**Cody Haugen:** is uh it is it is not with

**George Westbrook:** Is it

**Cody Haugen:** uh not with Max Million here. Um he he comes from a place that he just uh it's called stadium BS, but he comes from a place that uh sports betting and prediction markets are extremely predatory.

### **00:01:48**

**Cody Haugen:** Um and so he wants to talk to us on why we're different.

**Brett StClair:** Nice. That's very cool.

**Cody Haugen:** Yep. So,

**Brett StClair:** Oh,

**Cody Haugen:** yeah.

**Brett StClair:** hello.

**edwin:** Hey, they're all.

**Kevin Murray:** ever.

**Brett StClair:** You're breaking up quite a bit, Edwin.

**edwin:** How about now?

**Cody Haugen:** Much better.

**edwin:** Okay, I'll try to take the metal plates out of my head.

**Brett StClair:** Are you wearing like a tinfoil

**edwin:** No,

**Brett StClair:** hat?

**edwin:** I mean I'm right now, Brad. I'm staying away from all sharp objects.

**Brett StClair:** Please tell me he's nowhere near a bridge. Somebody

**edwin:** You know, right now I'm so husky. If I jump off the bridge, it's likely I'm going to bounce back up. So, I I got to I got to cut some weight to make that work for me. It's all um stress uh stress uh related fun.

**Brett StClair:** Are you a stress?

**edwin:** Yeah. Yeah.

**Brett StClair:** Are you stress also?

**edwin:** Yes. Um, all right. So, let's get right into it. Um, the weekend was better.

### **00:03:08**

**edwin:** Um, better. I would say that, um, you know, we're we're in a weird spot. We're launching Saturday,

**Max Kingaby:** Perfect.

**edwin:** so I don't know that we're in a place to launch yet. Um, hopefully we are. the uh the actual trading app itself. We still need quite a bit of ground to cover before the 29th. Um user-wise, we're laughable. 154 uh signups at this point. That tends to associate with no outward facing advertising. However, you know, at this point, outward fa outward facing advertising to get users to come in is going to be very very tricky given that we have no um advertisers that have signed on um to the platform. So,

**Max Kingaby:** Sorry.

**edwin:** uh this uh I actually had more signups for the simulation I ran a couple years ago. I think I had 600\. Um that that ran on on mine and I put up 25K. So that that was disappointing. Um yeah, so you know, essentially we have uh we've got ourselves a pickle here. Uh we need the app to be far more like click, you know, click by sell by cell.

### **00:04:40**

**edwin:** Um, the orientation of the the pages needs to have a a pretty quick, you know, doover or like modification even in the existing app. Maybe we can reduce some of the surfaces that people can click to just so they don't get confused. Um, but you know, the one thing I would say is that, you know, we've I put forth a couple of times of of what we want the app to look and feel like because in actuality, you know, as I look at this over the weekend, and I'll take anyone's feedback from it, please. You know, our differentiation, you can forget the fact that we're a stock. You can can, you know, forget the fact that it goes on multiple games. You can forget all that s\*\*\*. At the end of the day, the way that the structure works in my eyes is that, you know, you're able to trade in and out, in and out, in and out, multiple times a game. And that's the experience that we offer that other ones can't. You can do it on, let's say, a prediction market, but you can't do it for profit.

### **00:05:44**

**edwin:** Um, given their structure and the constraints of a zero being floor and a dollar being ceiling, there's just not enough room for the share prices to move. Um, so you know on on the on the production side. You know, the number one thing we need right now is we need market makers who are going to commit to our production launch. And if we don't have market makers, then I'm going to have to be the market maker on say 14 teams. and cap requirement on that it's probably going to be around 25 to 30 million that I'll need up for that which is outside my uh my zone at the moment. Um so yeah I mean I don't know anybody have any feedback on uh any of those points?

**George Westbrook:** I think in terms of in terms of like the actual app cutting down the surfaces is fine. I think we just that's that can be done by this weekend. Um I think like we from our side we're getting a better idea now of what what the experience you're picturing in terms of that in and out trading in and out clicking from a lot of where it is removing that friction of the reviewing blah blah blah.

### **00:07:06**

**George Westbrook:** Um so updating that's going to be fine. I think what was really pleasing for us was all the back end stuff's holding up really like really well. I think even TZ said like on the Friday alone where obviously didn't no the Thursday where it didn't go as well as expected um that was pretty much all appide um which looks to be almost resolved now um I think T0 saying it was like 3 million 3 million orders throughout that day um and then Friday Friday and Saturday were were good as well on the app services like we said if we keep that tight iteration loop then by the end of the will have something that I think everyone will be a lot more happy

**edwin:** Great. Yeah, the um yeah,

**George Westbrook:** with.

**edwin:** Troy and I are talking to T0 later this afternoon um about our deal terms. we have somehow morphed from being uh a free uh deal to start with to now it's going to run maybe 150,000 I think something like that

**Brett StClair:** Is that a

**edwin:** um for us uh no not a month there and yes

### **00:08:10**

**Brett StClair:** month?

**edwin:** ultimately a month so I think the total Troy where are we at numbers wise with those guys are we

**Troy McDonald Kane:** Well, the the minimum guarantee is the 20k a month platinum platform fee is what we the minimum were required that they want us to to start paying,

**edwin:** Right.

**Troy McDonald Kane:** but it was uncertain if that was for prod or for the trading competition. That was actually one of my questions I wanted to go over with them today.

**edwin:** Yeah, that's for sim. The tra the production is 150\.

**Troy McDonald Kane:** All right. Yeah.

**edwin:** So productions 150 because I think the first iteration they were going to make like based on the ad revenue they want a piece of that as well. So, um, with no ad revenue, that's going to change that that discussion uh mightily. So um yeah, we'll see. So let's say this thing cost uh you know 100 to 150,000 to run with 150 current signups and um the referral program isn't working at all uh yet. We'll see if it happens once we get on campus or if we put any of these interns into work.

### **00:09:25**

**edwin:** um you know we're going to end up somewhere between my guess is 5,000 to 10,000 tops users. So I don't see like you know a lot of users and with that little bit amount of users there's not going to be a lot of ad revenue even if we were to put in programmatic. So this this iteration is just going to be a complete loss for me. Um looking at it soberly and so you know what what can we gain out of it? I'm not sure. You know we we'd have to brainstorm on that. But ultimately this is just a I mean we're going to lose money on it and un it's unfortunate in the leadup we were hoping to make a little bit of money. Um, and I'm not sure, you know, of that 5 and 10,000 that we hope to get for trading, how many actually turn into production. You know, maybe a couple hundred. So, you know, if this ends up costing me, you know, a million dollars to run, maybe two. The if we had 500 users, call it $4,000 to acquire a customer, not really great return on that.

### **00:10:39**

**edwin:** Um, yeah. Did someone have something to say?

**Brett StClair:** I think I have a squeaky table in front of

**edwin:** Okay.

**Brett StClair:** me.

**edwin:** I just assume that was Max. Um,

**Brett StClair:** He's in

**Max Kingaby:** I I I don't want to be squeaking on Brett's table.

**Brett StClair:** Spain.

**edwin:** the last one didn't make it at the end. Um, yeah. So, you know, ultimately before this Saturday, here's what has to happen. We have to uh reconfigure the end. Like when you download the app, we have to have the three items there to choose from. It's got to be really simple, George. It's got to be like choose your competition, you know, free, 13 plus, whatever, you know, badges and all that b\*\*\*\*\*\*\*. then the like private competitions and then the um then the uh overall you know Jared hopefully will have some success with some of these frats and

**George Westbrook:** Sorry.

**edwin:** and otherwise and Kevin maybe some of these you know influencers that we've reached out to they can come back with uh some numbers but you know is anyone seeing it any differently than me with clear Nice.

### **00:11:59**

**edwin:** That

**George Westbrook:** I think in term in terms of the IPO,

**edwin:** b\*\*\*\*\*\*\*.

**George Westbrook:** I agree. Obviously, it's coming on it's coming on Friday. There's there's always a chance that 10,000 100,000 people could sign up, but obviously the likelihood is is is low. Um, but I suppose it's it's not over just because there's low subscription to the IPI. like we said, how we've got it, the market maker is going to be having all of that stock. So, as and when people flood to it, we're going to be able to to deal with it. Um, so yeah, I'd agree with you on this week, maybe even over the next month. Um, but it's not to say that's not going to change in the coming

**edwin:** No, I I understand that.

**George Westbrook:** months.

**edwin:** I'm just talking about right now, right? Like, and the other thing is like even if we had 50,000 people, we have absolutely zero way to monetize them at the moment. So, we we're we're not going to make any money. So, the more people that sign up is the more people I have to pay.

### **00:12:59**

**edwin:** So, I don't I don't really, you know, want 50,000 if it just means I have to pay out more money, right? Like at at the end of the day, this is basically just a free-for-all um based on our current

**George Westbrook:** Sorry.

**edwin:** structure. the um you know that programmatic that we had in there. I had like I don't know Cody said it was something related to my search history, but there was like a bunch of plus-sized female models came on my my f\*\*\*\*\*\* app and I was like good good lord,

**George Westbrook:** So, how many of them did you click on and buy stuff from?

**edwin:** you know. You told me not to click,

**George Westbrook:** Like 50%. Oh, yeah.

**edwin:** so I didn't click.

**George Westbrook:** Yeah, actually. Yeah. Yeah. Forget about

**edwin:** Yeah. I mean, but I I wasn't I think they were modeling clothing.

**George Westbrook:** that.

**edwin:** I don't know that they were modeling themselves. Otherwise, I would have probably bought a couple. But, um, yeah. So, I mean, from the inplay side, has anybody got anything they want to add?

### **00:13:57**

**edwin:** All right, great. Well, it looks like we're off to a f\*\*\*\*\*\* shiny start on Monday. Um, okay. So, uh, George, I guess that the the the quick quick and dirty here is for the IPOs, we also need a page that basically says if you want to buy shares, you have to just click the offer. Um, so I don't know how you want to do that, but you know, the IPO has to just be an offer, you know, where someone's like whatever, there's a million shares available and that's it. It's it's just selling, right?

**Brett StClair:** supposed.

**edwin:** So maybe it's just a page or something for each team. You click on a team, it goes to a page, it has, you know, the amount of shares available and you can click buy and that's it. Because you can't sell them, you can only buy them.

**George Westbrook:** Yeah,

**edwin:** Does that make sense or is that

**George Westbrook:** I think what we were I think what we were thinking is is you we just turn off the sell button.

**edwin:** tricky?

**George Westbrook:** So the the sell button will be there.

### **00:14:53**

**Brett StClair:** How do you feel?

**George Westbrook:** Um, well, two options. no sell button at all or the sell button's there and it shows us locked and then what we can do is when a user

**Brett StClair:** Eating.

**George Westbrook:** clicks the sell button we can have a popup that will say as this is the only the IPO process um you cannot sell if you want to sell trade on the secondary market there um just so that they're getting

**edwin:** Yeah, that's perfect cuz I don't want to get a bunch of calls. I mean, out of this 150 people,

**George Westbrook:** Okay.

**edwin:** I think, you know, a hundred are friends and family anyway. So, like, I'm going to be getting calls from f\*\*\*\*\*\* Kevin's uncle. Like, I can't sell my shares. I don't want to get any calls.

**George Westbrook:** Yes, I suppose it's it it's that and then the walk through at the start as well. So when users come on, I think it's probably best we do that once we've got the like all of the UI elements as close to nailed as we can get rather than building it, then it changes and then we're then we're going back and forth.

### **00:15:50**

**George Westbrook:** Um, so I think UI improvements, I think we've got a there's a few things we'll need to do with the maker and the taker and the the gateway this week as well.

**edwin:** Well,

**George Westbrook:** Um,

**edwin:** on the maker front, we need to widen out the maker. It's too tight.

**George Westbrook:** okay.

**edwin:** Okay. Cuz like, you know, the the prices are not moving enough away from the win percentage to to make it

**Brett StClair:** I love your

**George Westbrook:** Yeah.

**Brett StClair:** music.

**edwin:** realistic.

**George Westbrook:** That was that was a point actually I think we were talking about today which is one one issue that I think we foresee is that so with the refresh rate on sports radar data. So we've got both the win percentage and the expected games. So, but obviously before the game it's just expected wins. Um, that's fine. We assume that's valid data. During the game, we've obviously got the win probability, which sometimes is good, sometimes can be a little bit slow. Um, so hence why, let's say there's a touchdown, it might take 10 seconds before it reacts, but then also after the game,

### **00:16:53**

**edwin:** Yeah.

**George Westbrook:** we don't know and we what the expected wins might not change instantly after the game. So what could mean let's say at the start of the game it's six and a half during the game win probability

**edwin:** Heat.

**George Westbrook:** going up and down price follows up in accordance with that then after the game if the expected wins don't increase straight away the price is just going to drop back down to the the price that it was before the game and then it's going to oscillate

**edwin:** Yeah. So the Yeah. So it's price should always be like um adding in you know that that like whatever that um percentage of a win would be.

**Brett StClair:** Where?

**edwin:** So let's say like hypothetically you're expecting 12 wins,

**George Westbrook:** Oh, yeah.

**edwin:** right? And um yeah.

**George Westbrook:** I get what you mean.

**edwin:** Yeah. So a win is worth like 12 divided by 17,

**George Westbrook:** Yeah.

**edwin:** right? So it's like something like that's worth um or 17 divided by 12\. I always get them backwards. So a win might not be worth five bucks.

### **00:17:56**

**edwin:** It might be worth like, you know, $4.8 or something on the pure math, but the market sentiment sentiment, you know, a win, you know, and the swing within the game should be right now we're swinging only a couple bucks. The w the swing should be much greater. So, the swing should be anywhere between, you know, um let's say a $150 and say $8.

**Brett StClair:** Okay.

**edwin:** That's how much the price should be

**George Westbrook:** Okay. Yeah. Because I think one thing we need to is that daily report as well is automating that.

**edwin:** moving.

**George Westbrook:** But the more of a factor on I suppose the the NCAA the ELO ratings um and the offfield performance as well. or we could change I suppose yeah offfield performance um so I think it's just looking through that getting that built getting that implemented I suppose you and I get I get what you're saying about the prices after the game now because it's just start win probability if they win one minus start win probability times that by five and then that gives you the price after then you just add that to the expected wins before to

### **00:19:09**

**edwin:** Well,

**George Westbrook:** get that new

**edwin:** it's not it's no it's so like if that win hypothetically let let me walk you through and

**George Westbrook:** Nice.

**edwin:** we we can talk about this math. We don't need everyone on it but on the call for this but basically let's say a team is favored um by seven points to win. Okay. So the win probability when they start the game is not 50/50.

**George Westbrook:** Yeah.

**edwin:** Maybe it's like 8020\. So if you take the win probability times the pro uh the the $5 revenue you'd have $4. So it'd be $5 time. 08\. Now, if they actually won, the the gain in the seasonal would be 0.2 time five or another dollar. And if they actually lost,

**George Westbrook:** Yeah.

**edwin:** their drop would be $4.80 cuz they were expected to win. You follow what I

**George Westbrook:** Yeah. Yeah. Yeah. That's Yeah. That's I get that.

**edwin:** mean?

**George Westbrook:** Um, and then we just have to save that, use that until because I'm assuming what would happen is is there might be a slight discrepancy between what sports radar tell us and that.

### **00:20:15**

**George Westbrook:** So, let's say we've we've got that number. Let's say it went from 6.5 expected wins to 6.7. Um, and then Sports Radar might come out with a number given that performance, it's now 6.9. So then there'll be a jump with that as well because we've got our calculation and then when we get the new daily report from pardon me from sports radar data that might change given the assumption that we made before which I suppose is fine. Um it's just there might be that sudden movement in the market

**edwin:** Right. Right.

**George Westbrook:** maker.

**edwin:** And listen, movement's okay cuz this this is simulation. Well, there is no like we didn't do it close enough right enough. We want the prices to move. That's all I care about. So, if the prices can move and people can transact, that's all we want for this particular um circumstance. We want to be relatively close, but we don't it doesn't have to be, you know, dollar for dollar, penny for penny. The thing about the um delayed win percentage quotes.

### **00:21:21**

**edwin:** So what we need to consider okay is part of our win percentage um uh f\*\*\* let's say you know you're quoting around win percentage your bid offer but let's say hypothetically um the score is 1010 okay and and uh sport radar updates the prices much f uh the scores much faster than win probability because they actually have to compute to do it. So what I want to add on is a compute to our win probability. Our last like let's say our market maker win probability. Um so we convert it and you're I want you to pull from the score. And so if the score changes, okay, I want our our market maker to move the instant the score changes, not wait for the win probability, okay? Because we're not going to the stale data is is a death no. We can't have that. We can't have the market makers sit and wait because everyone can buy on scores and then they'll have an unfair advantage, an unrealistic advantage. So, we want to um you know, and by the way, we you know, maybe we take our own win probability.

### **00:22:36**

**edwin:** I don't know eventually. But I would I would sample the win probability and the score. And for the market maker, there's two questions. Is the win probability the same? Yes. Great. Is the score the same? Yes. Great. market make at that price. Then then then you have the next scenario where it's like market maker samples is it um is a win probability the same? Yes. Is the score the same? No. And if you say oh well the other team scored is up, you know, by seven points. We can put a um a dollar value to each point, you know, a seven or a three or whatever it may be. and that can move the you know the the um the market makers uh fair value price. So you should be calling both price and um or I'm sorry score and win probability. Does that make sense?

**George Westbrook:** It may it makes sense but in practice that might be quite difficult

**edwin:** Tell me why.

**George Westbrook:** um because so I suppose there's so many variables in terms of right when a team scores um there maybe their past performance maybe any current injuries or the

### **00:23:45**

**edwin:** No, we don't have to do that. Not for this. So, I I would almost I would almost look at it like this.

**George Westbrook:** Okay.

**edwin:** And you can do it on old data if you want. Like you take a sport radar, you know, historical game or something and just run it. I mean I I've got historical data on win probabilities right now going back to 1999 that I've been working with over the weekend.

**George Westbrook:** it. Oh, is that the the NFL verse data set?

**edwin:** Okay.

**George Westbrook:** I think I saw

**edwin:** Yes. Yes.

**George Westbrook:** that.

**edwin:** And um you know for our for our strategy lab development and what we're going to try to offer within the app um I want to be able to start building off of that data now so you don't have to and then we can just give you what we want after it's done. And then so they they um they settle all their data at the end of the night or you know when it's all over. So they don't have live win probability.

### **00:24:37**

**edwin:** So that's not where we can pull from. But you can basically say this George like you know win probability is 80%. And then let's say you know they go up by seven points. Does that mean and it's in the first quarter whatever does that mean the win probability goes to 100? No. it might go to 83 points, you know, or whatever. And then let's say the other team scores it. Does that mean it's 5050? No. It might go down to 73\. Um, and then as you get closer to the end of the game, the scores matter more. So like if we if the sport radar data shows a touchdown on the favorite, you know, they may go to 95%. And we don't need to be accurate for more than 10 seconds. We just need to change Right? Because as soon as that next sample of win probability, you're going to have the market maker recalibrate directly of that. So, it's a placeholder when you get stale data. And it actually would be kind of cool because it would be a trading event that's like,

### **00:25:37**

**George Westbrook:** Okay.

**edwin:** "Oh, f\*\*\*. The market mispriced this." You know what I

**George Westbrook:** Yeah. Okay. So, yeah,

**edwin:** mean?

**George Westbrook:** we'll have let's say win probability then the team scores. We keep on pulling the probability. If it's not been updated and the score is updated, then we we do a correction. As soon as the win probability has been updated, then we take that as gospel. Okay. I think we just I think all we need Yeah,

**edwin:** You

**George Westbrook:** I think we just need to assign a a an offset on the price

**edwin:** should

**George Westbrook:** or an offset on the probability given a certain point differential.

**edwin:** right. And I I can work on that. I maybe I'll have something for you later this week. Uh yeah, I mean I'm I'm going to pull all this data and I can tell you like um you know what the what a

**George Westbrook:** Okay.

**edwin:** win probably like what a touchdown's worth in the fourth quarter. Generally speaking, we can, you know, have an average differentiation and it literally only has to sit there until you get the next live win probability,

### **00:26:47**

**George Westbrook:** Okay. Then we're going to have to get the market maker to start consuming the playby-play data as well. So it'll be Yeah.

**edwin:** right?

**George Westbrook:** Okay. So yeah, playby-play data. Then I have to take the quarter. that and the score. Okay. Yeah, cuz it's not going to affect the taker because the taker is just random. Um what sort of random?

**edwin:** Yeah. Yeah. And I think what in terms of like size,

**George Westbrook:** Um

**edwin:** we're resting too much size. Um the book is too thick. So like if if the maker like um on the market maker,

**George Westbrook:** okay.

**edwin:** you know, we don't want to be 10,000 up, you know, we want to be,

**George Westbrook:** Yeah.

**edwin:** you know, maybe like, you know, 500 to 3,000

**George Westbrook:** Okay.

**edwin:** up.

**George Westbrook:** So, narrow the smaller quantities and the takers eating more because I think the take I think the takers at the moment it's completely random between like three

**edwin:** Correct.

**George Westbrook:** to 30 to 400\. So if we reduce that down to 500 to 3,000,

### **00:27:50**

**edwin:** Yeah.

**George Westbrook:** say it's random between like 300, the takers randomize between 300 to

**edwin:** Let me let me let me work you through. So basically I want to reduce the market maker size and I want to increase the taker size because I want

**George Westbrook:** Okay.

**edwin:** the bid ass to be knocked out. Okay? So, if people are resting on the bid top of book or second position and the taker comes in and he's going to sell 5,000, we want people to rest on the top of book or near the top of book to get fills. So, think of it like reduced market maker,

**George Westbrook:** Okay.

**edwin:** increase taker because otherwise the effect of the taker is very minimal. We, you know, they don't do anything. If you buy 30 into a 11,000 lot,

**George Westbrook:** Yeah. Yeah. Yeah.

**edwin:** it doesn't mean s\*\*\*. But if you bought a 11,000 into a 30 lot, like the market's going to be like

**George Westbrook:** Okay, that makes sense. Yeah.

**edwin:** crazy.

**George Westbrook:** And then it's the Yeah, cuz then the the the maker red does it books obviously on a timely cadence as well.

### **00:29:04**

**George Westbrook:** I think it's 2 to 500 milliseconds, but then also the when a quote has been filled and then also when there's a new win probability as well.

**edwin:** Right. Right.

**George Westbrook:** So then it would just be more

**edwin:** And so yeah. Yeah. So we want the the maker to be wider in terms of bit ass width.

**George Westbrook:** Yeah.

**edwin:** So somewhere around you know 8 to 12 ticks I think we want. And then we want to have the taker um at times willing to cross that you know for you know up to say 5,000 lots and they should be mark like our version of a market order where they could go through multiple prices not just

**George Westbrook:** Okay.

**edwin:** One.

**George Westbrook:** I I think Yeah, that makes sense. And I think one other thing I was going to say as well is in terms of testing, what I think we're going to do is on the test tickers, test tickers. um is have like live games always going on. So basically like on a just repeating and repeating. We'll have some of the simulation games on the test tickers and have it on some part of the app that only we can see.

### **00:30:15**

**George Westbrook:** So we can always be testing live trading. So it's not like let's just wait for a game and then test live trading. It's still going to work for the live games.

**edwin:** Yeah.

**George Westbrook:** Um just we've always got stuff going on.

**edwin:** Right. Right. The only thing I'm going to ask and you know you and Hasan staying up late, we really really appreciate it. Sincerely, um, believe me, we we on the on the user interface stuff. I don't want to go back and forth a ton. Like if if I say I want it this way, just f\*\*\*\*\*\* do it that way. Okay. What? like just you know we're not asking for you to have the strategy builder up before Saturday or anything like that. We're just saying in terms of like the user flow um you know the the buying and selling has to be as seamless as possible and it has to be as as quick as possible right like where you can go back and forth and back and forth. I mean these games over the the weekend there were a lot of blowouts so there weren't there wasn't any kind of like nailbiters at the end where like you could see prices flip you know from one side to the other.

### **00:31:20**

**edwin:** What's with the with the price move movement between say a dollar and you know maybe $8.5 is what a win or loss could do. You know you'll start to see the market be topsyturvy you know at key parts of the game. So the ability to make three or five or $6 a share is there on on on the playbyplay especially if the games are close. So we need to make sure that that experience is available otherwise it's uh defeats the

**George Westbrook:** Yeah,

**edwin:** purpose.

**George Westbrook:** that that makes a lot of sense. Um I think in terms of the the trade but so obviously get rid of that yellow orange trade button everywhere.

**edwin:** Yep.

**George Westbrook:** Um the obviously oneclick trading I'm assuming that's working a lot better.

**edwin:** it is,

**George Westbrook:** Um,

**edwin:** but the user has to select the one click, right? So, we want them to just be able to say, I'm g choose it because you could have fat fingers or whatever and you buy and sell and get worked up because you didn't

**George Westbrook:** yeah.

**edwin:** mean to. But, um, yeah, I mean, the the we're going to simplify this to the best of our ability over the next week uh before secondary get uh trading gets started on the 29th.

### **00:32:29**

**edwin:** Um, and you know, we'll go from there. But um you know our team Kevin, you're still on, right?

**Jared Sapirman:** He's

**edwin:** Okay. Troy,

**Jared Sapirman:** not

**edwin:** are you on?

**Troy McDonald Kane:** Yes, I

**edwin:** Okay, cool. Uh Kevin or I'm sorry,

**Troy McDonald Kane:** am.

**edwin:** Troy and Jared. Um we're going to have to think about how we want to pay people on these individual days for um start and then through September. Hopefully by September we'll have some additional people. Maybe an advertiser or two will put up some money, you know. Um I thought about this, Troy. Uh just talking out loud here. Um you know, maybe we go to some of the prop trading companies and see if any of them want to do anything five grand or something uh for traders uh like for recruitment. maybe they get a line into some you know potential traders that participate this on the university level so we can um you know have that as uh part of the offering you know there's most of these firms have so much f\*\*\*\*\*\* money and I know they all have their own hiring process but it might be a interesting goodwill gesture for them and see if we can't bolster some of the university u interest so we can talk about that later but that's a thought I had over the weekend Um, all right.

### **00:33:51**

**edwin:** Cool. Anything else? Any questions for me.

**Jared Sapirman:** Ed, I have a question. Um, something that you put on your uh mockup app was testing the waters

**edwin:** Yep.

**Jared Sapirman:** on a lot of screens. Is that something that's necessary in the actual app?

**edwin:** Uh, yes, but not in its current form.

**Jared Sapirman:** Okay.

**edwin:** Uh, we basically need to have that disclosure with a info button on it and it can pop up and it'll basically have that whole thing. But um for SEC regulatory um just relief uh that whole testing the waters thing has to be you know front and center on

**Troy McDonald Kane:** So, Edwin, is it possible that it just sits in the terms and conditions and when people first sign up for the app,

**edwin:** everything.

**Troy McDonald Kane:** they just click, they accept terms and conditions when we know 99% of people don't even read it just to cover our asses?

**edwin:** Um, yes. But we might like on the intro page, Troy, like when people choose their selection, what they're going to trade on, I may I may want to also have it there just to say it was there,

### **00:34:49**

**Troy McDonald Kane:** Right.

**edwin:** right? And that way, you know, it's not in on every surface.

**Troy McDonald Kane:** Yes.

**edwin:** But, um, you know, I did like the Gamecast experience surface. Um, George, but I like as we go over the next week and a half, like, you know, please be as flexible as you can on how that user interface works, cuz as good as the Game Cast is, um,

**George Westbrook:** Yeah.

**edwin:** and by the way, the Gamecast worked really well terms of speed, we're getting that displayed in some cases multiple seconds faster than TV in my case. Uh, very very uh, exciting. So, that that part was great. Um but like in terms of the orientation that um we can do a lot better um you know e and again I'm not talking about adding all the bells and whistles.

**George Westbrook:** Hm.

**edwin:** I'm just talking about the like the buy sell mechanics, the seeing of the fill, um you know the working orders, all that stuff. My P\&L a flatten button. uh because right now it's cumbersome when I like let's say you know I'm trading one team and I sell, you know, 1,500 uh shares of uh one team, then I go to my next team, my my gun is already loaded for another 1,500.

### **00:36:09**

**edwin:** So, it's like, you know, those types of things. I got to click on that, then I got to change the amount, and by the time I do that, the bid ask may have changed. In our case, the bid ask were was the market maker was like cement like there was no trade around because it was too thick. it was too tight to the um you know win probability. There wasn't enough like synthetic give up on both sides for it to have that two-way market flow. It basically was like trading the the 10-year note right now, which is like 3,000 up. If you get an edge, it's a miracle. And if you got that edge, you really don't want it. You know, it's like it's it's akin to a very developed market. So, we're going to we're going to lower those volumes at quote. We're going to widen up the spread. We're going to increase the takers um willingness to go outside and and cross for size. And then um yeah, I mean, I think that should change quite a bit. The Saturday games, like I said, they didn't have a lot of dynamic nature to them.

### **00:37:13**

**edwin:** They were actually quite boring to trade. You either had the winner or you didn't. Uh so they didn't trade, you know, enough back and forth to where uh it was it was viable for us to show the difference between us and prediction markets. The the prediction markets trade is basically what we had on on the games on Saturday. A team was winning. There was no real change in the probability uh at all. It just drifted and then if you're on the wrong side, you lost. Um it it was funny on one of the games I had the wrong side and I tried to exit and I had like 1300 or 1500\. I forget how many but I actually I hit the bid and um I uh I had like maybe maybe I got 500 done or something and then it's it I f\*\*\*\*\*\* missed them and then the market did drift away from me another three bucks. So that, you know, that miss cost me like three grand um on that. So, and that's that's realistic trading. That part's really good. Um but the actual user experience we've got to make sure is, you know, really, you know, we'll just re reduce surface, clean it up, make it streamline, simple to understand, and then we can, you know, add as we need to over the course of the season.

### **00:38:38**

**edwin:** Um, but in play, our team has a, you know, herculean effort ahead of us to start to monetize something. Um, you know, because otherwise this is just me throwing money away and and I don't want to do it anymore. I I want a clear path to like us launching, us being, you know, Maybe maybe not profitable, but to have some revenue, not to beat the dead horse, but you know, we're in this position cuz we are promised advertising revenue. That advertising revenue f\*\*\*\*\*\* was at best totally misunderstood. At worst, it was, you know, duplicitous information. But, you know, I'm I'm still wrestling with how to manage that that problem. So, you know, realistically, none of us would be down the road we are right now because we would have not have moved forward developing an app without a place to have the app be monetized. Um, you know, it's just it's it's unfortunate that that happened, but this is where we're at and I'm pretty furious about it to be honest. Um, yeah. So, that's that's where I'm at. We we need we need to make sure that the when someone downloads the app they get a clear selection of the three places they can trade private public or for for prizes.

### **00:40:00**

**edwin:** Okay. And then we have to say something about like hey this upcoming I IPO for the NCAA you know click buy to buy shares whatever that means.

**George Westbrook:** Yeah.

**edwin:** I don't know what that means but it can be a onepage just whatever. And then people could search up their teams and then we have to have the share lots available, a million shares available on each team. Then I'm gonna manually go in and I'm gonna buy the majority of those and then we'll have the secondary market up and running

**George Westbrook:** Okay.

**edwin:** the following weekend. And over the next week and a half, we can try to clean up the app to the best of our ability. Is that a fair plan?

**George Westbrook:** Yeah. And in in terms of in terms of cleaning up the app, is it on that discover page basically get rid of everything apart from having just the teams as the market? Maybe we we're going to need a section for live game so that people can easily get onto there, but cut out the cut out the league

### **00:40:55**

**edwin:** Yeah. On that. Yeah. On that front page when you get in,

**George Westbrook:** stuff.

**edwin:** it's good that you see your money first. Okay. And then you have the gamecast section. And we could just turn that into live games instead of gamecast. we just put live and then when people click on those it takes them to the gamecast and they're

**George Westbrook:** Yeah.

**edwin:** tradable. Um on the discover I'm not sure that we even need a discover page when we have the um search uh glass up at the top. Um,

**George Westbrook:** Yeah.

**edwin:** and I I would put a an icon up at that top bar uh for news and then have the news all in there so that these surfaces become really like thin in terms of how deep they got to scroll and you know it's basically just yeah what you see is what you get and then if you you know want

**Jared Sapirman:** Yeah.

**edwin:** more information you can click that top. I think the headers on the on the gamecast page need to be permanent. Uh so like uh if if I see like we'll come up with something in the next day or two that basically is a a header head header that you can scroll under.

### **00:42:01**

**edwin:** Um that that will work and then uh you know our our rankings and I don't know that we need a whole lot else. I mean we'll our team will go through and come back to you but realistic realistically I think we

**George Westbrook:** Okay.

**edwin:** just make this you know UI light make it effective simple and uh you know hopefully that experience gets us what we need to

**George Westbrook:** Okay,

**edwin:** get

**George Westbrook:** perfect.

**Jared Sapirman:** Yeah, Edwin, the simpler the better. I totally agree with it's it's the simpler the better.

**edwin:** what's that I'm sorry

**Jared Sapirman:** What you said I completely agree with.

**George Westbrook:** Um,

**Jared Sapirman:** It's very it's there's still a good amount of fat that we can cut I think from uh

**edwin:** Okay.

**Jared Sapirman:** the UI currently there that a lot of people won't use and it won't it will just detract from um their understanding of the

**edwin:** Well, I mean, in in like fairness to the fact,

**Jared Sapirman:** app

**edwin:** you know, what we were trying to build was an app that had a lot of stickiness because when we first started building it, we thought we were going to have ad spaces and services.

### **00:43:05**

**edwin:** we need to have multiple you know programmatic or whatever spend on and we need to make sure that there were enough places for these advertisers to promote their product. Um I don't see that happening right right now. We don't have any advertisers. I mean one thought I had George and team was um you know similar to how

**Troy McDonald Kane:** Thanks.

**edwin:** you like watch a game you know on the gamecast screen itself um if there's a pause in action whether it be a timeout TV timeout injury whatever end of the quarter um pregame after the game to have maybe you know we had talked about this a couple months ago maybe have some video that that goes over the field during the time of a timeout. Um, you can still trade. So, the market down at the bottom, you'd still have your buy, sell, but the actual, you know, commercial, if you will, is going during, uh, the times that the game is not going. And then, um, yeah, I still got to figure out how to sell something, you know, to somebody who want to buy it.

### **00:44:11**

**edwin:** I mean, what's crazy is we've got a billionaire investor who owns a candy company. We can't get the candy company to to uh advertise you know, we got all these relationships and, you know, everyone just sucks. So, it's just been a a horrible start to August. And hopefully, uh, as people come back to work, maybe maybe, you know, we can get some advertisers in September or, October to help offset some of the costs that we're going to be facing. Okie do.

**George Westbrook:** Perfect. I think I say busy week ahead, but let's f\*\*\*\*\*\*

**edwin:** Yep. Thank you, Big George.

**George Westbrook:** go.

**edwin:** And again, I do sincerely appreciate you staying up that late. I know you're a real f\*\*\*\*\*\*

**George Westbrook:** No worries.

**edwin:** night owl. You're like um George the Ripper, you trolling b\*\*\*\*\*\* that night. Um, so, but we we appreciate it. We're going to knock this out and uh we just need a successful uh IPO on Saturday. All right. Thank you, boys.

**George Westbrook:** Perfect.

**edwin:** All who need to talk to me, I'm going to be available in about 45 minutes.

**Jared Sapirman:** Sounds good.

**edwin:** All right. Have a good day all.

**George Westbrook:** Perfect.

**edwin:** Thank you so much.

**George Westbrook:** Have a good one.

**edwin:** See you.

**Max Kingaby:** Cheers guys.

**edwin:** I know.

### **Transcription ended after 00:45:26**

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*