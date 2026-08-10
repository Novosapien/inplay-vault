---
date: 2026-07-31
type: standup
description: "Friday touchdown, 31 July 2026: Android store live, the primary-offering structure settled, reference-price anchoring explained, IPO price publication and the 3-day freeze, and the SSP roadmap."
source: "Gemini meeting notes, Inplay - App - Touchdown"
scope:
  - "[[market-maker/market-maker]]"
  - "[[ipo-module/ipo-module]]"
  - "[[advertising/advertising]]"
  - "[[frontend-deployment]]"
  - "[[compliance/compliance]]"
  - "[[delivery/delivery]]"
status: extracted
extracted-to:
  - "[[market-maker/decisions]]"
  - "[[market-maker/parameters]]"
  - "[[market-maker/open-questions]]"
  - "[[market-maker/plan]]"
  - "[[ipo-module/ipo-module]]"
  - "[[advertising/advertising]]"
  - "[[frontend-deployment]]"
  - "[[compliance/regulatory-positioning]]"
  - "[[delivery/delivery]]"
  - "[[integrations]]"
---

## Post-Call Analysis

~55-minute Friday touchdown, and the densest market-maker content since the 23-07 call. Effectively the MM design session that 23-07 never became.

**The primary offering's market structure was settled.** Troy walked through it: two MPIDs, one for InPlay Markets the broker dealer (holding and selling the entire issuance, preloaded by tZERO with a million shares per team and unlimited buying power) and one for the market-making arm. Edwin cut George off mid-explanation to make the key point, that the market maker never sells the primary. The taker buys, with randomised size and heartbeat, and deliberately not weighted by trading participation because v1 stays simple. The load-balancing algo was dropped entirely, deferred to the NBA in October.

**Edwin corrected a genuine design worry.** George had spotted that the MM's quotes keep dragging price back to the reference price, behaving like an anchor. Edwin confirmed it happens and that it is correct: toxic flow moves price temporarily, the market returns to fair value, and that is how every market works. He then extended it into the underlying-versus-basis framing, and from there into the argument that InPlay's price feed is itself a licensable data product.

**IPO price publication hit a tZERO constraint**: prices lock static once set, blocking simulated trading. The resolution is to publish now and freeze three days out. Edwin also asked for pre-IPO indication of interest, so users can queue orders against a visible shares-remaining bar before the window opens.

**Android went live** that day. Brett set out the SSP ladder and capped it at three networks in three months.

Edwin also read out the New York AG's complaint against Kalshi and explained why its "outcomes of the events" language is useful to InPlay, with an instruction not to name competitors in outbound social.

| Finding | Destination | Action |
|---------|-------------|--------|
| Two MPIDs: broker dealer sells, principal trading arm makes and takes | [[market-maker/decisions]], [[ipo-module/ipo-module]] | Decision block + IPO update |
| 1M shares per team; NCAA 5-day and NFL 2-day windows; load-balancing dropped | [[market-maker/parameters]], [[ipo-module/ipo-module]] | Parameters rebuilt, N6 dissolved |
| Taker buys with randomised size and heartbeat, not participation-weighted | [[market-maker/decisions]], [[market-maker/parameters]] | Decision + parameter rows |
| RP anchoring is correct behaviour; toxic flow and return to fair value | [[market-maker/decisions]] | Decision recorded |
| Underlying-vs-basis framing; price feed as a licensable product | [[market-maker/decisions]], [[integrations]] | Strategy recorded, not a v1 build item |
| Edwin's MM code unusable as-is; components to be extracted | [[market-maker/open-questions]] | E4 closed |
| IPO prices publish via OTA, freeze 3 days out; tZERO price lock | [[ipo-module/ipo-module]], [[market-maker/open-questions]] | Update + new T14 |
| Pre-IPO indication of interest and shares-remaining bar | [[ipo-module/ipo-module]] | Update written, scoping owed |
| 6 Aug dry run slipped; 13 Aug preseason game targeted | [[market-maker/plan]], [[delivery/delivery]] | Dates updated |
| Android app live in Google Play | [[frontend-deployment]] | Section added |
| SSP ladder: AdMob + AppLovin MAX + one more, capped at three | [[advertising/advertising]] | Update written |
| Do not click test ads; CTR spike reads as fraud to AdMob | [[advertising/advertising]] | Warning recorded |
| Estimation skill being built to produce the backlog agentically | [[delivery/delivery]] | Delivery note |
| NY AG v Kalshi; TRO denied; framing usable, do not name competitors | [[compliance/regulatory-positioning]] | New compliance doc |
| Fundraising target cut from $40m to $10 to 15m; Underdog DCM sale | — | No action, business context |

---

Jul 31, 2026

## **Inplay \- App \- Touchdown \- Transcript**

### **00:00:08**

**Max Kingaby:** Oh yo yo yo.

**Troy McDonald Kane:** Hello.

**Brett StClair:** Oh,

**Troy McDonald Kane:** Friday

**Brett StClair:** hey.

**George Westbrook:** Hey,

**Brett StClair:** Hey. It's Friday.

**George Westbrook:** it's Friday.

**Troy McDonald Kane:** and in uh in Chicago this weekend is is a big music festival called La Palooa.

**George Westbrook:** Yeah, I've heard of

**Troy McDonald Kane:** Yes. It's taken over. I was downtown yesterday. It took over the It started last night.

**George Westbrook:** that.

**Troy McDonald Kane:** It took over the entire city. It's like it's been a long time since I've seen downtown this busy. So, yeah, it made me actually think of Max. I'm like, where's Max? Why is he not in this crowd? It's like, you know, big M 4 day music fest in the heart of Chicago.

**Max Kingaby:** Now, now I know about it.

**George Westbrook:** No,

**Max Kingaby:** I'll be there for the next one.

**Troy McDonald Kane:** Yeah. Within play will be a sponsor. There you go.

### **00:01:00**

**Max Kingaby:** Hopefully. I play.

**George Westbrook:** it's

**Jared Sapirman:** It's in Millennium Park, right, Troy?

**Troy McDonald Kane:** Yeah. Yeah. Yeah. All right. Just waiting for Edwin, I think.

**Brett StClair:** So, good news on the Android store release still.

**Troy McDonald Kane:** Yeah, that's congrats team. Uh we'll have Kevin and we'll have to get the icon created for the website and everything. So that's exciting. It also for the first time makes me want to go buy an Android phone so I can try it on.

**Cody Haugen:** Uh,

**George Westbrook:** I still got

**Cody Haugen:** we are up in Android.

**Brett StClair:** Good

**Cody Haugen:** Is that what I'm gathering from that information?

**George Westbrook:** that.

**Troy McDonald Kane:** Yeah,

**Cody Haugen:** Oh,

**Troy McDonald Kane:** I got we're up. So,

**Cody Haugen:** awesome.

**Troy McDonald Kane:** yeah. Did you uh you're on the Slack the Novo Slack channel, right?

**Cody Haugen:** I am How did I miss that? Well, congratulations everybody. I see that now.

### **00:01:56**

**Troy McDonald Kane:** Great way to end the week, I'll tell you

**Cody Haugen:** Yeah. Congrats,

**Edwin Johnson:** What's that inplay?

**Cody Haugen:** David.

**Troy McDonald Kane:** that.

**Edwin Johnson:** No sapion.

**George Westbrook:** So

**Cody Haugen:** We're live in the Android

**Brett StClair:** Traditionally, to give you a sense on what would usually happen is you'd have a team of two or three people that would

**Cody Haugen:** store.

**Edwin Johnson:** Wow.

**Brett StClair:** build the PWA. You would have a team of about five or six people that would build the website and then you would have two people on the Android, two people on the iPhone store. That's just the absolute basics of minimum. If you were building this traditionally, mad, right?

**Edwin Johnson:** crazy.

**Brett StClair:** How different the world is now.

**Edwin Johnson:** I would say how good you guys are now.

**Cody Haugen:** I

**Troy McDonald Kane:** All

**Cody Haugen:** agree.

**Edwin Johnson:** I mean, screw the haters,

**Troy McDonald Kane:** right.

**Edwin Johnson:** right?

**Cody Haugen:** There's enough of them out there. We don't need to make more.

**Edwin Johnson:** Awesome.

**Brett StClair:** We talking about graduates coming out of college now.

### **00:02:55**

**Edwin Johnson:** f\*\*\*. Well, they're annoying, huh? Aren't they brutal?

**Brett StClair:** We don't want AI. Oh, f\*\*\*. Oops.

**Edwin Johnson:** I mean, I I I love Jared. Okay, Jared's on our team. You guys You haven't heard much from him because he's a silent but deadly type guy. Um the when we have to talk to him about his generation, my mind turns into mac and cheese because it's like, you know, they want everything for free. They don't want to do any work. They don't want to read. They want constant 10-second impulses that give them money and sex and whatever. It's just I want that, too. But man, it would be it's just hard to f\*\*\*\*\*\* deal with.

**Troy McDonald Kane:** I mean, I think besides Brett, the Novo team's all in the same generation as Jared.

**Max Kingaby:** Yeah. Yeah. I was about to say sounds awfully familiar.

**Troy McDonald Kane:** So,

**Max Kingaby:** E.

**Edwin Johnson:** But here's the difference. The difference is you guys work your f\*\*\*\*\*\* tail off.

### **00:04:03**

**Edwin Johnson:** All right? And you're always available. And you know, if it's midnight, George is f\*\*\*\*\*\* responding. Brett's responding. I know he's an old geyser like me, but the the the fact of the matter is there's just a different slant with certain people. Jared's putting in tons of hours each week, you know. So, I I wouldn't say that, you know, they're all the built the same, but yeah, I mean, like I think Dana White's got a great clip out there. He's like, the world's full of so many pussies right now. If you just apply a little bit of pressure, you can run the world, you know, because everyone's so soft, basically. So, we'll see how you turn out, Max. I'm I'm waiting for the next season. I'm going to

**George Westbrook:** Max is Max works hard,

**Edwin Johnson:** binge.

**George Westbrook:** but he's still a p\*\*\*\*.

**Edwin Johnson:** I mean, it kind of Go ahead,

**Max Kingaby:** and and

**Edwin Johnson:** Max.

**Kevin Murray:** Hope hopefully he gets plenty of it when he goes to IBA or wherever he's

### **00:04:55**

**Max Kingaby:** and not not with the state I was in

**George Westbrook:** I'm I'm fishing. I'm going to get a

**Kevin Murray:** going.

**Max Kingaby:** Kevin,

**George Westbrook:** bite.

**Max Kingaby:** but I'm also surrounded by pussies. I was going to say

**Edwin Johnson:** Yes.

**George Westbrook:** We got the bite.

**Troy McDonald Kane:** What do they say? It takes one to know one. Is that

**Edwin Johnson:** Whoa, man. It is just hot on a Friday here.

**Troy McDonald Kane:** the

**Max Kingaby:** Well,

**Edwin Johnson:** End of the month the right

**Max Kingaby:** hang hanging up, guys.

**Edwin Johnson:** way.

**George Westbrook:** You are You are what you eat.

**Edwin Johnson:** I think we have a female on this call. We may not want to I think we want to hit the brakes just a bit. Um,

**Skye Capazorio:** Nothing new.

**Edwin Johnson:** sorry about that,

**Skye Capazorio:** Nothing new.

**Edwin Johnson:** Gary.

**George Westbrook:** Yeah,

**Edwin Johnson:** Oh. Oh,

**George Westbrook:** Sky Sky knows Brett quite well.

**Edwin Johnson:** I didn't see you, Sky. I was talking about

### **00:05:34**

**George Westbrook:** So,

**Edwin Johnson:** Gary.

**Troy McDonald Kane:** Oh,

**Edwin Johnson:** All right. So, what are we talking about today,

**George Westbrook:** Oops.

**Edwin Johnson:** boys and

**Troy McDonald Kane:** well, I know I wanted to talk about the primary offering,

**Edwin Johnson:** friends?

**Troy McDonald Kane:** but I don't know, George,

**Brett StClair:** Yeah,

**Troy McDonald Kane:** you had other topics you needed to talk about before that.

**Brett StClair:** we can jump straight into that here, George. Yeah. The final

**George Westbrook:** I'm offering I'd say we start with that.

**Troy McDonald Kane:** Yeah.

**George Westbrook:** That would be that was on one of our

**Troy McDonald Kane:** Yeah. So, um I'll I'll um just update everyone on where we are with T0 and Edwin's kind

**George Westbrook:** lists.

**Troy McDonald Kane:** of um request for the primary offering. So, the NCAA teams will just all be open for primary offering for five days. Um, we'll have uh a million shares per team company available outstanding for the primary issuance. What you'll need to build in George to the marketmaking algo now is just a randomizer to kind of lift shares out of the primary offering throughout those five days.

### **00:06:39**

**Troy McDonald Kane:** Not systematically, but randomly, right, Edwin? Is that the the thought?

**Edwin Johnson:** That's a thought. I mean,

**Troy McDonald Kane:** Yeah.

**Edwin Johnson:** I think what we can do, and I've been giving this a little bit more thought, Ke team, and that is just for simplicity, I mean, I don't want to see George with gray hair anytime soon, um, or Hassan. The uh the thought is now in at least in my mind's eye that we ditch the load balancing algo for the NFL and NCAA and we just use the same application for both. We stretch the NCAA over five days. We sp stretch the NFL over two days and essentially um we'll let the uh market the market maker go in and purchase you know the first three or 400 share three or 400,000 shares of each team in a randomized way. Hit pause you know and maybe we could schedule so much per day roundabout and then you know they'll fill up the coffers for what we need in order to get enough liquidity out into the market so it's not dead.

### **00:07:44**

**Edwin Johnson:** And then um you know just keep it relatively simple for this iteration. We could do the load balance balancing for the NBA in October just to give us a little bit more

**George Westbrook:** I think I think we need to think about that because I think one of the approach that we said we were going to do

**Edwin Johnson:** time.

**George Westbrook:** with with T0 for the IPO because we're not using their process is effectively what what would be is the market maker would hold all of the shares um at the like say million million or 900,000 shares and then the the users well the market maker would open sell orders for all of them and then the

**Edwin Johnson:** Let me stop you right there, George.

**George Westbrook:** US

**Edwin Johnson:** The market maker is not going to open up and sell sell.

**Troy McDonald Kane:** It's the broker dealer.

**Edwin Johnson:** Okay.

**Troy McDonald Kane:** So, let me let me let me rephrase it a little bit what we talked about yesterday.

**Edwin Johnson:** Yeah.

**Troy McDonald Kane:** So, there's going to be at least for the simulation, there's going to be inplay markets with two divisions.

### **00:08:39**

**Troy McDonald Kane:** There's going to be the broker dealer side of the synthetic of of inplay markets which that is the the the side that will make the shares available and then there's the market making side of the broker dealer that will be able to to lift that. So think of it as client facing non-client facing essentially.

**George Westbrook:** So would that be two wallets as cuz I thought

**Troy McDonald Kane:** Yeah, two separate w two separate wallets.

**George Westbrook:** yesterday.

**Troy McDonald Kane:** It will also be two separate MPIDs because you need to differentiate the business lines. So there'll be the So that's what we were trying to talk about yesterday with T0 is that we'll have the synthetic broker

**George Westbrook:** Okay.

**Troy McDonald Kane:** dealer that is the uh the designated market maker that they call it on the NY exchange where they hold the shares to be sold to um the public and then we have inplay markets the market making arm that will then go in and and buy those shares you know randomly throughout the process.

**George Westbrook:** Okay. So, two wallets, one that holds all the shares, has the sell orders.

### **00:09:41**

**George Westbrook:** Um, the market maker then randomly buys those ones. Um, okay. And

**Troy McDonald Kane:** and Edwin the way that sorry real quick George one other quick note before we finish uh that workflow

**George Westbrook:** then

**Troy McDonald Kane:** is so what T0 is going to do is they're going to create uh an MPID for inplay markets the broker dealer and then it's going to preload a million shares in each of the teams and with essentially unlimited buying power as well.

**Edwin Johnson:** Mhm.

**George Westbrook:** s\*\*\*.

**Troy McDonald Kane:** So there's no issue with rejects or anything like that. And then um and then there'll be this second MPID that gets created that George will fit for the mark making

**Edwin Johnson:** Yeah, that makes total sense.

**Troy McDonald Kane:** algos,

**Edwin Johnson:** And this way we just keep it clean for the round. for this first round.

**Troy McDonald Kane:** right?

**Edwin Johnson:** Let's not complicate things and just get it done.

**Troy McDonald Kane:** Yeah.

**Edwin Johnson:** We we are not anticipating a ton of activity on the IPO. I mean, based on what we've gotten, signups, there just isn't enough right now for it to be, you know, anything other than a, you know, a necessary evil at this point in my mind.

### **00:10:43**

**Edwin Johnson:** You know, I have some hopes that we can get, you know, four or 5,000 signed up beforehand. You know, maybe 10 if we got really, really lucky. Um, but right now I think what do we sit at, Cody? Like 110\. 118\.

**Cody Haugen:** 118\.

**Edwin Johnson:** And so those 118 are not referring the way that we had hoped, at least in the preseason. You know, once they start losing money or an ability to trade, they'll start referring their balls off. So it definitely, you know, all of this pregame stuff is really hard to measure our impact because it's just there's nothing compelling to go on there right now other than if you want to read the news, do a little research. The news and research are great. You know, I was looking at different, you know, teams and players who's hurt yesterday. Pretty informative. Um, I think instead of us spending time on that IPO process, I think we should, um, at least for the football, okay, we should be focused on how to get some of the other things done, the market maker, the taker, the the subscription piece, because right now it looks like the subscription piece is going to be the only thing that's actually going to produce any money, potential money, and it's going to be, you know, poultry at That's at least to start.

### **00:12:01**

**Edwin Johnson:** Uh but hopefully it'll ramp up and you know we'll go from there.

**Troy McDonald Kane:** All

**George Westbrook:** There was with when you say random is it going to be kind of semi-

**Troy McDonald Kane:** right.

**George Westbrook:** random? So based on so let's say there's a

**Edwin Johnson:** I'll give you a range I'll give you a range of shares and then you're going to have a

**George Westbrook:** team

**Edwin Johnson:** randomizer and a randomizer is very easy to make you know it in there.

**George Westbrook:** Yeah.

**Edwin Johnson:** It's that's nothing. Um so we'll give it a time period. Okay. I'll give you blocks of times and then uh you know between say 500 and a,000 or 100 and 500 and you know it'll just clip along and it'll have a immeasurable heartbeat because the heartbeat will be randomized as well.

**George Westbrook:** But but would it be random based on participation? So let's say there's one team, there's loads of trading volume,

**Edwin Johnson:** No,

**George Westbrook:** it would still it wouldn't buy more shares of that to provide more liquidity.

### **00:12:55**

**Edwin Johnson:** not we're not at this at for our first run. We're going to keep it very very simple. We know where we want these teams because the totals are going to be also random.

**George Westbrook:** Okay.

**Edwin Johnson:** So, it's not going to be 650,000 exact. It's going to range between 600 and 650,000. And then once the secondary market opens up, we'll do market operations to get everyone balanced so that you know it it'll cause another bit of information and people to trade on you know before the season

**George Westbrook:** Okay.

**Edwin Johnson:** starts.

**George Westbrook:** So it's effectively it's because I suppose the market making it it is the market maker but it's not going to be the same algorithm. So effectively it's going to be kind of two market takers. one for let like secondaries open and one market taker which is going to allocate it to the um that's one thing we're going to have to think about with the the market taker as well actually so market taker for IPO process um but it's going to be allocated to the market makers wallet for the market taker

### **00:13:58**

**Edwin Johnson:** Yep.

**George Westbrook:** in normal trading what

**Edwin Johnson:** He's going to be its own wallet.

**George Westbrook:** Okay.

**Edwin Johnson:** He's going to be a basically think of him as just a random

**George Westbrook:** And that

**Troy McDonald Kane:** So wait,

**Edwin Johnson:** participant.

**Troy McDonald Kane:** you Edwin, you you envision two separate MPIDs for the taker and maker,

**George Westbrook:** Okay.

**Troy McDonald Kane:** not under the same MIDI. So you want a separate wallet or let me just say wallet. You want a separate wallet for the taker algo and a separate wallet for the maker. Okay,

**Edwin Johnson:** Yes.

**Troy McDonald Kane:** that's good. That that's good information to know. I'll make sure we set it up that way on T.

**Edwin Johnson:** Yeah. So, in all the tests I've been running on my stuff, the I'm trying to get the market maker in a position where it actually is profitable.

**Troy McDonald Kane:** Yeah.

**Edwin Johnson:** So, it actually the logic I the most recent logic I gave you, it actually manages its position.

### **00:14:45**

**George Westbrook:** H cuz that was that was one thing I was thinking I was looking through yesterday looking at the looking at the market making algo and I think it was the old reference price and how the old reference price is based purely on expected wins be the the figure published and the probability of that in game. Um, but it's not taking into account the actual market like where the market's going. So, if we kept that reference price, it's kind of like an anchor. So, the market might be moving it that way. um whatever for whatever reason, but because the market maker is the one providing the most amount of liquidity, the orders that it's or the quotes that it's going to be producing are always going to be smashing the market back to the reference price, which is based

**Edwin Johnson:** Yeah. So that's exactly how a real market works.

**George Westbrook:** on

**Edwin Johnson:** So you'll have a situation where let's say um I'm short the market and the actual fair value is a price of five. Okay?

### **00:15:40**

**Edwin Johnson:** and um I just have to get out because I'm I've breached my risk limits and I can't take any more pain up. And my clearing firm says to me, "You have to exit." And I just rip the market by covering my short by buying uh and I ripped the price up to 15\. That's not a new reference point. That's a that's a a price that's an an occurrence based on a market function that has to happen. The so the market maker takes a we call that like toxic flow for a second instantaneous toxic flow but then they make the market around the reference price and essentially it always the market always goes back towards fair value what the market calls fair value. That's how every market in the world works.

**George Westbrook:** But but say with um a normal a normal stock, how do you like obviously for us we've got kind of like a deterministic way to work out what we consider fair value, but I suppose in a real market For a market maker, there's not a deterministic way to calculate fair

### **00:16:44**

**Edwin Johnson:** I would say that every firm has a proprietary model that is some bastardization

**George Westbrook:** value.

**Edwin Johnson:** over someone else's proprietary model. It's pretty similar as far as how people value things. So like for example, if you were to look at a traditional market like S\&P futures, you know, they have an underlying called the spider ETF. Okay? And so they can deviate in price, but they can deviate in price for a number of reasons. Okay? So one is the actual 500 stocks you trade. The other one is the futures contract on the on the 500 stocks you trade. You would think they would move in lock step like this, but that's not how it works. Sometimes the spiders might be discounted based on interest rates or um any experies that are coming up. There's all kinds of things that can uh deviate the underlying or the basis of the spider versus the futures contract. Same thing is what I keep preaching about what we have within play is we have the underlying we have the spider contract.

### **00:17:45**

**Edwin Johnson:** So when all these poly markets and calcia are trading futures, they're trading a derivative essentially of what we're creating. They do it in a a binary outcome way, but um the difference is underlying versus basis. So when people look at fair value, they look at all those inputs, okay?

**George Westbrook:** Yeah.

**Edwin Johnson:** Uh current rate of cost of money, deliverables, when the contract's going to expire,

**George Westbrook:** And

**Edwin Johnson:** all that that stuff factors in. And ultimately, we all pretty much price it pretty close to the

**George Westbrook:** okay. Yeah.

**Edwin Johnson:** same

**George Westbrook:** So all those variables in a normal market have to be kind of assembled and put into the algorithm independently. But what we're using is the probability which is kind of the aggregate of all of that. Like so star quarterback gets injured that's going to drop the probability. somebody's on a good run gets the probability. So init okay so initially we're just going to use sports radar in order to determine that probability but in time with the plan B we consume the raw data points like injury performance

### **00:18:47**

**Edwin Johnson:** That's 100% accurate because that's then we have a proprietary feed, right?

**George Westbrook:** Okay.

**Edwin Johnson:** That becomes really valuable to us internally. And what we're going to do is we'll back test the last like whatever number of seasons against our share price once it's live. And we could internally start to digest what events on the field and off going to most frequently impact what we consider f fair value because there could be a deviation which then creates more and more trading opportunities because let's say Max has a valuation model that doesn't include you know um you know closing price or something. He only looks at opening price and opening range and that's his fair value for the day. uh we use something called a volume weighted average price or a VWAP model where you can tell where the concentration of of transactions has happened and if you deviate far from the VWAP then generally people say oh it's drifting too far away or otherwise so there's strategies that that fade things that drift too far away from a VWAP up or down because they look at the VWAP as like a magnet so similarly our price feeds our internal proprietary price feeds become very valuable for data sales, right?

### **00:20:02**

**Edwin Johnson:** So like I can see where Kelshi, Poly Market, all the sports books would want to license our proprietary data feed. It's not a probability feed. It's actually a price feed that they can translate into betting odds in real time.

**George Westbrook:** That was one thing I was looking at the other day is there's there's data already with every single event that's happened in NFL, every single result like freely available.

**Edwin Johnson:** Totally.

**George Westbrook:** Couple that with the proprietary stuff as well like the market data.

**Edwin Johnson:** Yeah. And that's where we're going to be able to like as we lay it overlay it on our share

**George Westbrook:** Okay.

**Edwin Johnson:** prices because that's going to also be like market reaction. So like you know we'll have here in the states let's say the uh the Fed or is going to cut rates or let's say they're actually going to raise rates because that's an environment we're going towards. And let's say the market says, okay, they're pricing it at 25 basis points, but they raise it 50 basis points or 75\. you it's always nice to model what that should be worth in terms of price.

### **00:21:04**

**Edwin Johnson:** So if like you're surprised by something that happens on the field, you know, a key injury in the first quarter is different than a key injury in the fourth quarter. So those, you know, you could say, oh, an injured quarterback should be worth 50 cents a a share. No, it it's determined by, you know, how late in the season, how late in the game, you know, what's the backup look like? All those different things we can funnel into the model and it can give us a lot of different valuations. Right?

**George Westbrook:** and their specific performance as

**Edwin Johnson:** There you go.

**George Westbrook:** well.

**Edwin Johnson:** There you go. So yeah, I mean there's a lot we can extrapolate from that, but like just for the ease because what what I want is I want to be able to start trading live. So George and I spoke yesterday on the phone all and the idea is I I worked on the market maker and taker. I know it's annoying. Um, but I did run about I want to say about 5,000 individual simulations per team for seasons.

### **00:22:03**

**Edwin Johnson:** Um, so it went five years back or whatever. And um you know I want to make sure our market maker is is acting correctly but I also want that taker in there because if if like one of the things I think that we're we're lacking okay when we when we have an opportunity to pitch the product to say a brand or a marketing firm is we can't actually show what it is. We can show the app and you you could say, "Oh, yeah, that looks cool and I see how there could be trading, but the moment you have someone start trading, it is where it changes because, you know, we could be on a pitch and we could be like, "Look, do you want to buy or sell right now?" We go into these markets and then we we need that market maker and taker to function so it'll look and resemble what's going to happen once we go live, right? And you know, it's kind of like how that Jim Mcool who's, by the way, an old cranky f\*\*\*. I mean, this guy's not a good time.

### **00:23:00**

**Edwin Johnson:** All right, he's like 68 years old, you know? I mean, you know, I I mean, he's a very nice man, but like he's, you know, he's not my target audience, but this guy was a total naysayer and then he got on and started trading. He's like, "Holy s\*\*\*, that's amazing." So, uh, you know, being able to have that experience, I think will change at least hopefully, you know, change some of our our our efforts to to raise money, um, through sales and, you know, maybe investment, you know, and a couple side notes. I'll just puke out my info as we go. Um, I don't like a straight line. I have not heard dick from those hard rock people. Nothing. After all that work, I mean, that's just u\*\*\*\*\*\*\*\* acceptable and unreal. um other than a guy reached out to me last Saturday, which you know now looks even worse because if he says he's going to check in with his team and I don't hear from someone for a week, man, it's just a terrible look.

### **00:23:56**

**Edwin Johnson:** So I have to write those guys off, okay? um and assume that are total b\*\*\*\*\*\*\*. You know, I we weren't with the Novo team last year. I think Sky was with me. Troy, Kevin, you remember those f\*\*\*\*\*\* guys? We signed the $30 million term sheet. They're now indicted for like fraud and all this other b\*\*\*\*\*\*\*. We have run up against so many strokes when it comes to f\*\*\*\*\*\* raising money. I'm sure there everyone does, but it seemingly, you know, we can't get a bonafide candidate to to participate. So, I'm I'm over the next two weeks, I'm going to just rack my my contact list and, you know, try to kind of ground swell maybe 10 or 15 million and then hopefully in October once we're running, we can raise a little bit more. I had hoped for 40 this month, but I don't see how that's happening. I mean, I can put in, you know, a little bit more myself and get us to whatever we need, but I would love 10 to 15 uh in this month at a minimum.

### **00:24:55**

**Edwin Johnson:** So, that's that. Um, George, after looking at that code um that I gave you, uh, now again, I I understand there's nuances connecting to sport radar and T0. Have you been able to like unit test that stuff at all or take a look at see if it looks like it can work? Because on my end, it's saying it should be able to work.

**George Westbrook:** it it won't work as is. Um but what we can do is take components out. Um, I think like I was mentioning yesterday, it's like there some of the good parts in there are I think it was the the calculating of the I think it was the volatility. There was a few there was a few things in there which we're going to pick out replace but we can't take the code as is because there's there's so much above it. There's so much below it um in order to get like the let's call it the market maker. And then there's the technical aspects as well, which is making sure that if it needs to run every 200 milliseconds, it's going to run every 200 milliseconds.

### **00:25:56**

**George Westbrook:** If it's going to need to cancel stuff,

**Edwin Johnson:** Right.

**George Westbrook:** it's going to cancel stuff. Um, making sure it's got the state stored in it as well. Um, it's some sometimes we have that when we're when we're writing code with AI is it will go,

**Edwin Johnson:** Okay.

**George Westbrook:** "Yeah, this is perfect. Just use it." And then when you try and use it, it's it's been a bit overzealous um in promising you the world.

**Edwin Johnson:** No, I I get that and I assume that there's going to be some um you know turbulence in integration. Um but if as long as some of that code is going to save you time and effort, you know, that's the goal because the sooner we can get the simulations up, the better. I know we had hoped for like what were we hoping for? August 6, first preseason game.

**George Westbrook:** Yeah,

**Edwin Johnson:** Yeah. I mean, if that's still a potential,

**Cody Haugen:** All

**Edwin Johnson:** it would be great.

**George Westbrook:** I mean at the moment that's looking unlikely.

### **00:26:43**

**Cody Haugen:** right.

**George Westbrook:** Um the the the difficulty we have is it's sometimes it's like pushing

**Edwin Johnson:** Okay.

**George Westbrook:** a like a snowball down a hill. Sometimes it starts really small and then it f\*\*\*\*\*\* snowballs and then it gets massive. and then it's fine. Um, other times we don't realize that we're at the start of push pushing it. Not the best analogy. Um, this is the difficulty especially with developing with with AI is some things that seem easy and they should be done overnight are things that take longer and other things you can get them stood up working functioning very very quickly. Um, which which I suppose is the one of the benefits working with us and one of the negatives is sometimes you're like f\*\*\*\*\*\*

**Edwin Johnson:** Right.

**George Westbrook:** hell this happened so quickly and then other times it's you did this thing in two days why is this taking two

**Edwin Johnson:** Understood.

**George Westbrook:** weeks

**Edwin Johnson:** Understood. We We're We're in your hands, Godfather. So, take take care.

**George Westbrook:** yeah it's progress is being made though um so I suppose the other the other aspects there's obviously there's the Play Store.

### **00:27:52**

**George Westbrook:** That's done. Um, trading. Well, pretty much, correct me if I'm wrong, like it's done. Um, or the ability to trade blah blah blah. We added in some notifications as well. Um, both in app and out of app. Let's say you place an order, close your phone, um, a notification is going to pop up when it's been filled. Whereas if you're in the app, it's going to it's not going to show the notification as like an Apple notification, but it's going to be an internal notification. Um, which is which is the standard standard way of doing that. Um, the the ads as well, ADM Mob's been integrated. Um, got some test ad units as well, which we're just trying to trying to get in there, trying to get them refined. So, I think it might be worth we we take you through that on on Monday. Um, what today Brett? I see Brett. Brett shaking his

**Troy McDonald Kane:** So, I'm looking at I'm looking at other possibilities that we could do uh dry runs.

### **00:28:46**

**George Westbrook:** head.

**Troy McDonald Kane:** So, the 13th is another possibility. So, that is a week from next Thursday. I mean, I I kind of can't believe we're already into August. Um and there's a couple games that night, too. So, we could actually potentially do multiple team companies if we wanted

**Edwin Johnson:** I I mean I think we also have the ability to trade some of those old games too,

**Troy McDonald Kane:** to.

**Edwin Johnson:** right?

**George Westbrook:** Yeah.

**Edwin Johnson:** So we don't just need to wait on a live game. I think we could trade, you

**Troy McDonald Kane:** Yeah,

**George Westbrook:** Yeah.

**Troy McDonald Kane:** but I think it would be better to I mean, yeah,

**Edwin Johnson:** know,

**Troy McDonald Kane:** if that's a that's the only option. Yeah, but I think it would be great to get live data pumping through a live game to see how

**Edwin Johnson:** 100%. I I think if we could do both though,

**Troy McDonald Kane:** Yeah.

**Edwin Johnson:** I mean, if it if we get,

### **00:29:33**

**Troy McDonald Kane:** Yeah.

**Edwin Johnson:** you know, we're at the point where George and King um Brett gives us the green light, we could start, you know, on a Wednesday morning trading stale data or, you know, I don't mean stale um you know,

**George Westbrook:** All

**Edwin Johnson:** previously played games. I think it'd be worthwhile to at least bang on it because I I do see a lot of value when people see a trade.

**George Westbrook:** right.

**Edwin Johnson:** And has anyone on this call ever traded any of my simulation? No. Right. It's it's f\*\*\*\*\*\* awesome.

**Kevin Murray:** Nope.

**Edwin Johnson:** I mean, it is it is really fun and it it's it's um like you'll be on for two hours, you'll think you're on for 10 minutes.

**Troy McDonald Kane:** Okay.

**Edwin Johnson:** I It just goes so fast and every single play it's just especially with money on the

**George Westbrook:** Hello.

**Edwin Johnson:** line, it's it's really really fun. It's I mean I don't like addictive but it's you know super addictive. So, and then you know what the other thing I was saying, George, with that taker I told Cody the goal here is obviously we have 247 trading, right?

### **00:30:36**

**Edwin Johnson:** That's our our our mantra. Well, if there's no market movement at 2 am on a Friday night, it's going to be annoying for people. They're going to log in. They're like, "Oh, prices aren't moving." The whole idea of the market taker is at least there's some flow that

**George Westbrook:** Oh,

**Edwin Johnson:** moves 24 hours a day. So even if you're laying in bed and there's no game being played, you can log in and take a look and be, oh yeah, and you know, it might move 50 cents a dollar. It could move, you know, based on what's happening with these uh the taker. We built in some, you know, some ability for this thing to just rip for whatever reason. Sometimes people need capital and they want to sell and liquidate so they can get money or they need to put money to work and they buy. Um it's very similar to when I trade overnight hours say in the bond market. The bond markets open from 7:30 in the morning uh central and they close at 2:00 p.m.

### **00:31:31**

**Edwin Johnson:** uh central. And what happens is um I still trade it from 2:00 p.m. to 400 pm and then I trade it from 5:00 p.m. all the way overnight until 7:30 a.m. And those are considered off hours. And there's still tons of things you can do um when the when the exchange is is not, you know, the the floor, call it when it was open wasn't open, you can still trade that s\*\*\*. So, I want the same experience here so that people don't need to have a game going on. And there was a big um deal today in New York that Queen Leticia James sued Kelshi and the governor came out and made a pretty rough statement on it. And I've been working with that statement about how they're like, "Yeah, the you know the what the heck is it? Bear with me. The the quote was I got it. So, they're they're worried about the underage um children betting. Okay. And um there's a phrase in here and this is their legal the phrase is actually their legal position.

### **00:32:49**

**Edwin Johnson:** It's something about like f\*\*\* I'm sorry guys. Please bear with me just a second. I apologize. And a number of states have sued, but New York suing is a different um it's a it's a different uh lawsuit than say uh Nevada. Okay. Because that that New York is going to be like second circuit. That's a that that's a big deal. And or I are they no DC second circuit. The circuit for New York is where a lot of um you know legal uh cases end up getting resolved. Like if you have something in like Northern California, everyone's like, "Oh, on appeal that s\*\*\*'s going to get overturned because it's so liberal." Or if you get something like heavy in the South, that's going to get uh overturned because it's like so, you know, conservative. But New York is is basically where a lot of precedent cases get set. So this them taking the initiative to sue them. Uh that earlier in the week they had tried to um or maybe it was early in the month tried to get a um temporary restraining order preventing New York from um stopping that based on the federal preeemption.

### **00:34:05**

**Edwin Johnson:** Okay. And then uh the judge actually denied that temporary restraining order which was a big deal which led the that green light for New York State to sue Kouchi um from from that. But basically at the end of the day this became like um that their their product is based on like the result of a game of you know they call it a game of chance the result of and it was like it was almost like I wrote it because it frames our product as the obvious solution which is not dependent on the outcome of a game. Right? And so and it it was it was it's so I've been working with this a little bit and I'll share some things later. That's that's a huge thing for us. The other thing is like uh Troy I don't know if you saw this um Underdog just bought a DCM to do market.

**Troy McDonald Kane:** I did see that. Yeah.

**Edwin Johnson:** They sold it like this week for $1.2 billion. They're not even f\*\*\*\*\*\* up.

### **00:35:07**

**Edwin Johnson:** Like they not not they're not they're not they're not anything. They're they're nobody. and they sold for a billion, too, which is crazy. And then here we are and we we're deal with d\*\*\*\*\*\*\*. So, I I'm I'm not sure what's going on with our fundraising, but it is definitely a frustrating run. So, um, again, by having this stuff run over the season and the way that we've structured the product with the off field, we have an operating company that's tradable and investable with multiple sources of revenue that is not outcome dependent in order for its value to be determined. So, you know, we always tout like, hey, you can win a game, but if the share price can go down, it doesn't mean it like the game in itself is not an absolute that gets someone money. It's an it's an idea that the market will say, "Oh, they won." And that wind means that they should get revenue but it's not forwardlooking and then as we are successful with ADM Mob and the others um you know on the field performance becomes less and less the dominant driver and then it becomes more about the predictability of the actual revenue from off the field.

### **00:36:18**

**Edwin Johnson:** Okay. So both of those things are important which leads me to my next question um

**Troy McDonald Kane:** I I'm sorry. I got to I I really have to jump.

**Edwin Johnson:** from them by the

**Troy McDonald Kane:** I'm late to this other call, but I'll I'll catch up with you all later. Thank you.

**Edwin Johnson:** way I mean let me guess he's interviewing

**Kevin Murray:** I f\*\*\*\*\*\*

**Edwin Johnson:** another intern uh we we are

**Kevin Murray:** no idea.

**Edwin Johnson:** interviewing interns at at a rapid pace. I'm going to be spending like $70,000 a month. I don't know what any of these kids are going to do. Um,

**George Westbrook:** Yeah.

**Edwin Johnson:** but we'll see what happens.

**George Westbrook:** Any of them any good that you've seen?

**Edwin Johnson:** I haven't seen any. Jared's been seeing them. Are any good,

**Jared Sapirman:** Yep. I mean,

**Edwin Johnson:** Jared?

**Jared Sapirman:** the one I'm working with is fantastic. I would love for you to meet him. We We could set up a call at any point.

### **00:37:04**

**Edwin Johnson:** Who Who is that directed to?

**Jared Sapirman:** You

**Edwin Johnson:** Oh, me. You know what? I got enough friends. I'm trying to cut some.

**Jared Sapirman:** Yeah.

**Edwin Johnson:** I'm thinking about dumping Brett here. I would never do that, sir.

**George Westbrook:** Thank

**Edwin Johnson:** That's a liquor talking.

**George Westbrook:** you.

**Edwin Johnson:** Um, all right. So, with ADM Mob, how many of these uh ad server programmatic places do you want to see us connected to over the next couple months?

**Brett StClair:** We are going to at a minimum be on apploving max. So they'll serve some they're going to be doing ad serving. Then majority is probably going to come from AdMob because the biggest volumes there. And then I'm going to try and get us into one other that'll be in the next month or so. Like even app loving it's been two weeks and I'm just chasing trying to

**Edwin Johnson:** Cool.

**Brett StClair:** get the sign on process. It's just slow. These exchanges are really really really really

### **00:38:07**

**Edwin Johnson:** So,

**Brett StClair:** slow.

**Edwin Johnson:** don't we know the the one guy who's friends with the owner of that app loving Kevin Kev?

**Brett StClair:** But I was thinking uh was it Kev?

**Edwin Johnson:** That that uh Rich's kid

**Brett StClair:** Yeah. if you can do a notes there to see

**Kevin Murray:** Rich. Yeah, Rich balances kids. Yeah, we can.

**Brett StClair:** if he if if he can do an intro for us then I can chase on that

**Edwin Johnson:** Okay.

**Kevin Murray:** Yeah.

**Brett StClair:** and then I've got three others that I'm trying to decide which is going to be quickest. I've got I did trial applications on them about two months ago and I didn't hear anything back. So I'm now going to go through my network see where I've got closest. I think it'll be SmartO. My old boss is now the VP of Smart, so I'm going to jump in and try work him a bit. Um, and see if we can get on to that list. These premium guys are a bit fussy.

### **00:38:57**

**Brett StClair:** No one car. It's the same cuz you know they're like we want volume we want this all that kind of jazz but I think maybe um what's it hurts can get me in there um and then I don't think we are going to go more in the first 3

**Edwin Johnson:** Okay.

**Brett StClair:** months than that only because it get really complicated

**Edwin Johnson:** Okay.

**Brett StClair:** um and then what I'm keen on you guys seeing what ads look like in the current ad placements because George at the moment has are very beautifully designed ads that are very aesthetic to the site,

**Edwin Johnson:** George is a beautiful human.

**Brett StClair:** but ads ad generally take give no f\*\*\*\* about the site and they some nasty s\*\*\* there. When I mean nasty, it's just like like I can't believe these people call themselves creatives. Um I don't know. So, were you able to get your your demo stuff running? Hey,

**Edwin Johnson:** Whip it out, George. Let's see what's

**Brett StClair:** the son.

**Edwin Johnson:** up.

**Brett StClair:** And then when once George is finished whipping it out, the son will share his

### **00:40:08**

**Max Kingaby:** Don't whip it out again,

**Brett StClair:** screen.

**Max Kingaby:** please.

**Edwin Johnson:** Are you guys going out for an end of the month celebration tonight?

**George Westbrook:** into

**Brett StClair:** We did a a bit of a lunch uh yesterday for her son's birthday.

**George Westbrook:** the

**Edwin Johnson:** Oh,

**Brett StClair:** Her son's turned 18\.

**Edwin Johnson:** how old have a boy? It's so so good to have that young blood.

**Brett StClair:** How old are you now?

**Edwin Johnson:** Happy

**Brett StClair:** 22\. You're 22,

**Edwin Johnson:** birthday,

**Brett StClair:** eh? 22\. 22?

**Kevin Murray:** Happy birthday,

**Brett StClair:** You're getting

**Kevin Murray:** mate.

**Edwin Johnson:** 22\.

**Kevin Murray:** You catching us

**Brett StClair:** old.

**Edwin Johnson:** I mean, you look at Max and f\*\*\*\*\*\* Hassan, 22, 21, living life.

**Kevin Murray:** up.

**Edwin Johnson:** I mean, could you imagine at that time, Brett, having a job like this where you can make a bunch of money, like an unbelievable future of your career and just

**George Westbrook:** I

**Brett StClair:** the security guard at Lord's cricket

**Edwin Johnson:** like I was running

**George Westbrook:** was

**Brett StClair:** ground.

**Edwin Johnson:** a large illegal sports empire.

### **00:41:05**

**Brett StClair:** I'd much rather have your

**Edwin Johnson:** Not not not when I got arrested.

**Brett StClair:** job.

**Edwin Johnson:** You will when we have our our drink. I'll tell you an amazing story around that whole Oh,

**Brett StClair:** Yeah.

**Edwin Johnson:** man. That was a very nerve-wracking time for

**George Westbrook:** Thank you. Caster.

**Edwin Johnson:** me.

**Brett StClair:** Oh, beautiful. Oh, you got it up and running. Nice.

**Hasan Ahmed:** Okay.

**Brett StClair:** Oh.

**Hasan Ahmed:** So, um everything in here is I think is all of the actual as these are all like example ads from from the like as an example catalog. So, um if you scroll through these are all of the ad types. Um

**Edwin Johnson:** What page are on there.

**Hasan Ahmed:** those

**Edwin Johnson:** Is it one of our pages? Uh, learn or something.

**Hasan Ahmed:** um I believe it's like a like internal and a testing page that

**Edwin Johnson:** Oh, okay.

**Hasan Ahmed:** only we can have placed them in the app

**Edwin Johnson:** Okay, cool.

**Hasan Ahmed:** but I think these are the individual thing formats for how they are going be in the app itself.

### **00:42:26**

**Hasan Ahmed:** And then I mean a few like I mean I mean actually a few of these ones but I mean these are the like adaptive ones which are a bit more I say that but like it's also an option if we are also then trying to go down the actual um

**Edwin Johnson:** Very

**Hasan Ahmed:** I mean yeah these ads if you want click into them,

**Edwin Johnson:** cool.

**Hasan Ahmed:** they will go to their um actual site. Um I don't know if it's going to open here, but I think um yeah, and then if you click on this part, it will go back to the app.

**Edwin Johnson:** Good luck.

**Hasan Ahmed:** Um,

**Edwin Johnson:** Love you, baby. Good luck. Thanks. See you in a bit. Oh, yeah. Love you.

**Brett StClair:** So I think the key thing is when we get it loaded into the

**Hasan Ahmed:** stop.

**Brett StClair:** actual app, you'll start to see,

**Hasan Ahmed:** Stop.

**Brett StClair:** you know, compared to, you know, these are this is just an ads lab area.

### **00:43:50**

**Brett StClair:** So we can start seeing what they're going to look like,

**Edwin Johnson:** Yeah.

**Brett StClair:** feel like, where we can use it, test it, all that kind of jazz. Um, so we're going to start placing them and you'll see they they really do disrupt.

**Hasan Ahmed:** There

**Brett StClair:** So you you're probably going to want to look at and get a feel, get a sense. When we do do that,

**Hasan Ahmed:** is

**Brett StClair:** it comes with a big big warning. Please do not click on the ads because what it'll do is

**Hasan Ahmed:** me.

**Edwin Johnson:** Okay.

**Brett StClair:** it'll spike your CTR rate and ADM Mob will think it's fraud and then they'll ban and block us. Um, so when we're running these early stages,

**Edwin Johnson:** Okay.

**Brett StClair:** please don't click on the ads. It's really tempting. I know some of the ads are tempting, you know, like George likes the extension product stuff and I keep telling him just ignore it, move on, but he keeps wanting to click on it. So like he's

### **00:44:39**

**Edwin Johnson:** I I I understand

**Brett StClair:** just

**Edwin Johnson:** why. Look at the face right now.

**Brett StClair:** I've never heard he's never had a non comeback.

**Edwin Johnson:** I mean, he looks like he's going to murder.

**Hasan Ahmed:** He's looking.

**Brett StClair:** He's looking for a marker to put some kind of mark against my name on one of our doors.

**Edwin Johnson:** Yeah. Please.

**Hasan Ahmed:** That'll

**Brett StClair:** That'll work.

**Edwin Johnson:** No, no murder yet, George.

**Hasan Ahmed:** work.

**Edwin Johnson:** Let's launch get some money so we can bail you out. That's awesome. Thanks, Han.

**Brett StClair:** Otherwise, I think that's it for now. I think we've got everything covered. We um Yeah, we're uh Cody, is Cody still here?

**Edwin Johnson:** No,

**Brett StClair:** Um no.

**Edwin Johnson:** Cody had to step off.

**Brett StClair:** Yeah, he stepped out. Um we are working on a skill to try

**Kevin Murray:** Nobody.

**Brett StClair:** get as best kind of guesstimate on timelines effort backlog based on the current cadence of it. It it's turning out to be quite difficult.

### **00:45:45**

**Brett StClair:** Um but we'll have something probably early next week. So at least you guys can start kind of going okay if I we want to do that next. This needs to be slotted in ahead of that rather than that. then you kind of get some kind of sense. But we're trying to get it to a point where we can run it agentically. Um instead of do what most project managers do in life, you kind of guess um on effort, duration, all that kind of jazz. We want to try to get as accurate as possible. So just looking at various ways to achieve that. So we'll probably have something early next week. Once we have something, we'll put down uh a nice kind of look and feel inplay style design, pop it into the uh vault and then you can kind of see and then when we make decisions, we can always then reshuffle that backlog accordingly and then you've always got a good sense of what's going to be delivered and see what has been delivered.

### **00:46:39**

**Brett StClair:** So like ticked off is the kind of thinking

**Edwin Johnson:** Cool. On the IPO stuff, I before we bolt, uh, quick question for you. When do you think you'll publish the NCAA prices?

**George Westbrook:** next push which will be I want to get to stuff in the next push. No, that'll be the IPO price is OTAA. So we just we need to do a bucket um a bucket for the a bucket of pushes for OTAA. We we should have enough now that we could Yeah.

**Edwin Johnson:** Kevin, this is genius

**George Westbrook:** Oh,

**Edwin Johnson:** works.

**George Westbrook:** I think actually I think the reason why we haven't done it already is because what we this Yeah, we forgot to mention this. So whereas before what we were doing is you see a number we just hardcode the number in ideally what we want is we want to pull that data from T0 but I think they were saying T0 said as soon as we set the IPO prices the prices are static there's like a lock on it so that then we can't do the simulated trading

### **00:47:51**

**Edwin Johnson:** Yeah, we Yeah, we don't want to do that. Why don't we load the prices up until 3 days before we're going to IP? IPO because 3 days is when we're going to lock in.

**George Westbrook:** And

**Edwin Johnson:** So come from now until IPO, you could have a lot of roster changes. Kids could get arrested and banned and hurt and coaches get fired. All kinds of s\*\*\* can go down, which would materially affect that stock price. So we want to make sure that we're going to we'll freeze the pricing three days ahead of time.

**George Westbrook:** Mhm.

**Edwin Johnson:** What what my goal would be is to have those prices out there. Okay? And then the ability for someone to say they can pre like say oh I want to buy a 100 shares of X and they can hit a button and then we can start to develop an in like that it'll say oh 48,000 shares already looking to be bought of you know Chicago Bears as and then it can change and so part of how we're going to um potentially if we can enable that how we would do it with the market maker is we could have the market maker start buying, you know, putting in orders to buy the IPO shares even before the window opens.

### **00:49:03**

**Edwin Johnson:** And we could show that on that bar that says shares available. You know, if there's a million shares outstanding, then 500,000 are bought. There's only in line to buy, there's only 500,000 left. You see that? That's going to that's going to at least give people something to do on the app right now. Um, so I could say to to a marketing company, hey, why don't we go in and pre- buy some shares of the New York Giants, and I'll show you how that anything that we can do to keep them um clicking something on the app and staying engaged other than, you know, news and and other stuff. Anything to do with trading that's going to get their mindset, you know, focused on that, that would be helpful. So, I don't know what that looks like on your end. I'm just telling you what my dreams are.

**George Westbrook:** Okay. Yeah, we we'll have a think and see what we can do

**Edwin Johnson:** Okay,

**George Westbrook:** there.

**Kevin Murray:** ask just quickly is the is it inplay challenge on the uh Google Play

### **00:49:52**

**Edwin Johnson:** cool.

**Kevin Murray:** Store is how it's coming up as well

**George Westbrook:** Um yeah,

**Kevin Murray:** or all right

**George Westbrook:** I can give you the link for it as well. Your mic's f\*\*\*\*\*.

**Hasan Ahmed:** Is it

**George Westbrook:** Yeah. Cuts

**Kevin Murray:** I could hear I could hear him from yours anyway,

**Hasan Ahmed:** okay?

**Kevin Murray:** George.

**George Westbrook:** out.

**Kevin Murray:** So, it's all thanks Hassan.

**George Westbrook:** Oh, there we go.

**Edwin Johnson:** Okay.

**George Westbrook:** Yeah,

**Kevin Murray:** Sweet.

**George Westbrook:** perfect. Um, you gonna say it? Yeah. Who's going to say it? I think that's

**Edwin Johnson:** Okay. I found that quote just just so you guys have it in your frame.

**George Westbrook:** everything.

**Edwin Johnson:** All right. The quote is, "The lawsuit alleges that Khi's prediction markets meet the legal definition of gambling because the outcomes of the events on which its users are betting are uncertain and outside the control of the better or hinge on a game of Chance. And so um that's it's

**Brett StClair:** That's terrible news for them.

### **00:51:05**

**Brett StClair:** Brilliant news for

**George Westbrook:** Oh,

**Edwin Johnson:** it is um so if I was a lawyer I would pick apart it athletics are not a game of

**Brett StClair:** you.

**Edwin Johnson:** chance. Athletics are a game of skill. So there that's a bad argument on their part number one.

**George Westbrook:** heat.

**Edwin Johnson:** Uh games of chance are like cards or dice. It's not it's not chance it's skill. And obviously the way that people get paid in that higher skilled players get more money, right? Uh so that I would attack that number one. But um the outcomes of events is the key phrase. Um because like we said our our whole mantra is we are not dependent on the outcome. We're dependent on the price back. That's what determines the value of the share not the outcome of the event. So, um, you know, obviously I've been working on this for a long time, but a quote like this by, uh, attorney general and governor is really powerful for us to use and frame.

### **00:51:59**

**Edwin Johnson:** Kevin, I think we might, and Jared, um, if No, he's still here. Um, if we want to try to frame some of our social outreach or things like that, we might want to not name anyone by name, but make comments or something like that in our own social about us being different without mentioning the other side, if that makes sense. We'll talk more about it offline, but um,

**Jared Sapirman:** Sounds like a good idea to

**Edwin Johnson:** anyways, thank you all for a great week,

**Kevin Murray:** Yeah.

**Edwin Johnson:** great month. Brett reviewing the contract at the lawyer.

**Jared Sapirman:** me.

**Edwin Johnson:** The lawyer's always our guy so f\*\*\*\*\*\* late. I mean, that's not a copout. Gary knows him. I mean,

**George Westbrook:** No, no, there's no

**Brett StClair:** on it.

**Kevin Murray:** Yeah.

**Edwin Johnson:** Jesus

**Brett StClair:** What I'm doing is I'm just running a set of statements on the Rebel Labs just to wrap up the Rebel Labs account and then I'm going to send you an invoice on the Novo Sapion account which

**Edwin Johnson:** and I'll have different account instructions on

### **00:52:47**

**Brett StClair:** will and I'm going to do it all in US dollars and I'm going to do it to a US dollar

**Edwin Johnson:** there.

**Brett StClair:** Revolute account. So,

**Edwin Johnson:** Yeah,

**Brett StClair:** at least it'll be a lot easier for you.

**Edwin Johnson:** I hated your your peg of 135\. I mean, that's some b\*\*\*\*\*\*\*. Trading 131 right now,

**Brett StClair:** What is it at 131 now?

**Edwin Johnson:** m\*\*\*\*\*\*\*\*\*\*\*.

**Brett StClair:** Oh, it was at 135 when I did it,

**Edwin Johnson:** I think so.

**Brett StClair:** but I can I can move it around.

**Edwin Johnson:** No, I'm I'm busting balls. We'll figure it out.

**Brett StClair:** Oh,

**Edwin Johnson:** We'll make it work.

**Brett StClair:** okay.

**Edwin Johnson:** Don't worry. I mean, we're not going to swivel over a couple grand every month.

**Brett StClair:** Yeah. Yeah. I wasn't I just kind of took the mean between X amount of weeks and thought,

**Edwin Johnson:** Awesome.

**Brett StClair:** okay, it's about there.

**Edwin Johnson:** Yeah. No,

**Brett StClair:** down.

**Edwin Johnson:** we're going to be fine. Um, we've operated great without a contract,

### **00:53:27**

**Brett StClair:** Yeah.

**Edwin Johnson:** so no issues.

**Brett StClair:** Yeah, I'm perfectly

**Edwin Johnson:** Okay, cool. Um, all right. Well, everyone enjoy your days and we will talk on Monday or over the weekend if anyone needs anything,

**Brett StClair:** fine.

**Edwin Johnson:** especially Hassan George or uh Max. If you need any love advice, Max, I know a guy who knows a guy.

**Brett StClair:** What's his name? A son.

**Edwin Johnson:** No, his name is Kevin Murray,

**Brett StClair:** Okay,

**Edwin Johnson:** which in Gaelic Yeah.

**Max Kingaby:** going to teach me the English the English tricks.

**Brett StClair:** that's good.

**Max Kingaby:** Heaven.

**Kevin Murray:** Dang,

**Edwin Johnson:** Yeah.

**Kevin Murray:** what's up?

**Edwin Johnson:** Gaelic Murray means panty dropper is what he told me. But it was his panty.

**Kevin Murray:** I've still got a few tricks up my sleeve.

**Edwin Johnson:** So

**Kevin Murray:** I'm sure I could uh teach

**Max Kingaby:** My phone's

**Kevin Murray:** you.

**Edwin Johnson:** dancy teeth.

**Max Kingaby:** hurt.

**Edwin Johnson:** All right, all have a great weekend. We'll talk soon. Um and Sky, I'm going to try you over the weekend. Okay.

**Skye Capazorio:** All good. Thanks.

**George Westbrook:** Perfect.

**Edwin Johnson:** Thank you all.

**Kevin Murray:** Have a good one everyone.

**Edwin Johnson:** Have a great day.

**Kevin Murray:** All right,

**George Westbrook:** Have a good one.

**Kevin Murray:** let's focus is

**George Westbrook:** Let's f\*\*\*\*\*\*

**Edwin Johnson:** Please,

**George Westbrook:** go off.

**Edwin Johnson:** George. Please.

### **Transcription ended after 00:54:39**

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*