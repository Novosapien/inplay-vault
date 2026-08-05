---
date: 2026-07-20
type: standup
scope:
  - "[[market-maker/market-maker]]"
  - "[[trading/trading]]"
  - "[[information-layer/sub-components/single-game-page/single-game-page]]"
status: extracted
extracted-to:
  - "[[market-maker/market-maker]]"
  - "[[trading/trading]]"
  - "[[components/components]]"
  - "[[vision]]"
  - "[[architecture/open-questions]]"
  - "[[information-layer/sub-components/single-game-page/single-game-page]]"
---

## Post-Call Analysis

75-minute Monday touchdown. Edwin present for the first ~35 minutes for a market-maker mechanics Q&A (his prep doc — the "market banker" workbook — also went to the Hard Rock / Israeli investor groups today); Troy carried the rest of the MM detail after he left. Second half: Watch page UX + ads, watchlist vs favourites, week focus.

| Finding | Destination | Action |
|---------|-------------|--------|
| Market maker mechanics resolved: resting-liquidity bot in tZERO's book (users match each other directly), **market state** terminology, unlimited buying power, short-locate exemption, reference-price ± offsets + skew, randomizer, limit-order crossing, cancel-replace ~5–10×/sec, three liquidity sessions, subjective/learned event triggers | [[market-maker/market-maker]] | **New component created** (promoted from candidate trading sub-component — user-directed); backfilled into [[components/components]] + [[vision]] |
| CTS1/CTS2 price engines — **InPlay builds them**, not consumed from tZERO; price drivers = today's-game probability + all-other-games + off-field revenue | [[market-maker/market-maker]] | Captured in component doc §2 |
| Markets truly isolated per team (pairs-trading frame); rankings/tiebreakers don't feed pricing | [[market-maker/market-maker]] | Captured in component doc §2 |
| Synthetic market order re-scoped: **before first NFL game** (was post-MVP); price-through approach, Troy to help write logic | [[trading/trading]] | §2 business rule + §9 post-MVP list amended |
| Price band (~30% TBD) + quote-bust authority with tZERO | [[market-maker/market-maker]] + [[trading/trading]] | Captured both sides; detail deferred to coming sessions |
| tZERO cadence: tech calls now 2×/week (Tue/Thu); tZERO asked to stand up synthetic MM entity in QA | [[market-maker/market-maker]] + [[trading/trading]] update block | Captured |
| MM ops UI = desktop version of the app, MM-first; Kevin likely operator | [[market-maker/market-maker]] | Captured in component doc §2 |
| MM deep-dive moved to **Thu 23-07, 3–4pm London**; George mapping remaining PTS/CTS docs; Edwin's old trigger script to be located; week-zero NCAA valuation question for Edwin | [[market-maker/market-maker]] §4 + [[architecture/open-questions]] | Next-steps captured; MM open-question rows updated |
| Watch page: scrollable right-hand graph stack + interlaced ads (~6–8 positions), team-selector ordering (playing → favourites → alphabetical), trade-sheet scroll-through built, intern app reviews starting | [[information-layer/sub-components/single-game-page/single-game-page]] | §9 Watch Mode 20-07 block + changelog entry |
| Watchlist vs favourites (Jared feedback) — multiple watchlists vs single favourites, positions use case | [[architecture/open-questions]] | New open-question row (raised 20-07) |
| Notification types named: system / personalized / campaign-based — this-week focus | [[components/components]] Push/CRM | Bullet added |
| App Store: Apple silent since 15-07; Hasan escalating for expedited review; approval a this-week priority | [[architecture/open-questions]] | App Store row updated |
| Sportradar futures API broken — 403 on wanted endpoint, only 8/32 NFL win totals, no probabilities returned; George emailed endpoints detail (re-sending reply-all to Cody); Cody chasing David/Scott + topping up probabilities-API trial quota (45% used). FanDuel shows NCAA win totals, so upstream data exists | — | Action item — Cody owns the chase |
| SSP sequencing: AdMob first, then AppLovin (AdMob loaded into AppLovin as mediator/ad server) | — | No action — consistent with 13–17 Jul AppLovin MAX decision |
| Investor deck + workbook approved by Edwin, out to Hard Rock + Israeli investor groups today; Max building an app to automate the deck-workbook workflow for Edwin | — | No action (status) |
| Week focus: trade backend (once tZERO hands over), notifications, app approval, first SSP live | — | No action (status) |

---

Jul 20, 2026

## Inplay - App - Touchdown - Transcript

### 00:00:08

  

George Westbrook: Start the market. Just going to add the funny me as an alien.

Brett StClair: Do it.

Max Kingaby: We're all giving ourselves effects to

Brett StClair: Hello. Come on, do it, George.

George Westbrook: Hello.

Brett StClair: I was trying to tee you up there. George was trying to show off that he's finally learned

Skye Capazorio: Oh, Max,

Brett StClair: to

Skye Capazorio: look at that

Max Kingaby: Been grinding it out.

Skye Capazorio: hair.

Max Kingaby: Delicious.

Brett StClair: Are you trying to find it,

Cody Haugen: You trying to find the

Brett StClair: George? Have you forgotten where it

George Westbrook: No, I'm going to leave leave the the alien for

Brett StClair: is?

Skye Capazorio: Were you going to put it

George Westbrook: today.

Skye Capazorio: like ears on? Oh, the sun is a

George Westbrook: Don't we we I think we we did we did a virtual stand up with all

Kevin Murray: Excuse

Skye Capazorio: sloth.

George Westbrook: between all of us and I think for about 10 minutes all we were doing was just playing around with the like one person was an alien the other person was like a a pig or something.

  
  

### 00:01:26

  

George Westbrook: It was really it was quite it was strange how amusing we found it and for how long. I think by the end of it Brett was like I work with

Kevin Murray: me.

George Westbrook: f***************. Right. Are you

Max Kingaby: Yeah, you got the old man Rap.

George Westbrook: going

Brett StClair: It's terrible. This is the one that George had and it really bothered the hell out of me because as he spoke it'd be

George Westbrook: now?

Brett StClair: yes. So as I'm speaking it's all cool with my

George Westbrook: Gary's going to think, "What the f***

Troy McDonald Kane: that just made Monday.

George Westbrook: have I just walked into? Now, now the fun part is seeing Brett trying to turn it off.

Brett StClair: I know it is terrible. Hey, I just I' just got to figure out how to turn it off. How the f*** do I turn this off? What's this wavy hair? I max. How do I get rid of that wavy hair?

Kevin Murray: f****** hell,

  
  

### 00:02:34

  

Cody Haugen: You've uh have have you seen the video, Brett,

Kevin Murray: Max.

Troy McDonald Kane: Man,

Cody Haugen: of the guy? He's a he's a attorney and he's it's like back from COVID,

Brett StClair: Yeah.

Cody Haugen: but so they're show up on the Zoom and he's trying to represent himself and he's a cat. like,

Brett StClair: He's not

Cody Haugen: I can't turn it off. My daughter put it on for a project or something. He's like, I'm I'm here though. I promise I'm not a cat. And the judge's like, we know you're not a cat. Just

Brett StClair: This is far better. This is my French song.

Cody Haugen: ridiculous.

Brett StClair: Claire, I don't know why I'm finding it so much fun. I got so irritated last week when you guys were doing it. Okay, so guys, how was everyone's weekends? Was it good?

Cody Haugen: Yeah. Busy. Very very

Troy McDonald Kane: Yeah.

Brett StClair: Yeah,

Kevin Murray: Yeah.

Brett StClair: it's been a busy weekend.

  
  

### 00:03:30

  

Brett StClair: Hey, um,

Cody Haugen: busy.

Troy McDonald Kane: Were you up late watching the game yesterday?

Brett StClair: come on,

Troy McDonald Kane: Yeah.

Brett StClair: Spain.

George Westbrook: Scrap very

Brett StClair: So, we got to watch England beat Argentina in the rugby on the Saturday evening.

George Westbrook: strong.

Brett StClair: Yes. And then we got to watch Spain beat Argentina on the Sunday. Yes.

Edwin Johnson: I don't know how you had time to watch the games while you were doing all this work for me over the weekend.

Brett StClair: Yeah. And you know I'm instructing nothing at all. I'm not saying work Lord work.

Edwin Johnson: It's amazing, right? When we combine the couple of clouds, how good it

Brett StClair: It's coming right. Right. Um Max is putting together more of an app for you guys so that we're taking all the learnings.

Edwin Johnson: gets.

Brett StClair: everything you're sending me, I'm sending him. So, you can run it through and test. And then you'll instead of having to prompt it, you'll actually have an app that you can load your decks into and it'll do a better job, but it's still a bit of

  
  

### 00:04:30

  

Edwin Johnson: That's great. Um, listen, I have uh an emergency popped up.

Brett StClair: a

Edwin Johnson: I got to go downtown and deal with the situation. Um, I had to have Matt fly in uh Troy and team. So, I'm going to be out of pocket at 9:00 for the day, but I need everyone to to hammer away on on this because we have to send this out to the hard rock peeps today.

Troy McDonald Kane: Yeah, understood.

Cody Haugen: Yep.

Brett StClair: is this the market banker we need to hammer out

Edwin Johnson: Awesome.

Kevin Murray: Yep.

Edwin Johnson: Oh, it is.

Brett StClair: today

Edwin Johnson: But unfortunately today your boyfriend here is gone. But I can't make it tomorrow. Today's just uh

Brett StClair: person I have to explain to my wife who I'm messaging late at night to

George Westbrook: Yeah.

Edwin Johnson: you're like listen,

George Westbrook: Is that what is that why you're taking pictures in the toilet as well?

Brett StClair: Especially

Edwin Johnson: you know, well very aggressive on a Monday.

Troy McDonald Kane: Oh,

Edwin Johnson: George I was gonna say started with a little

  
  

### 00:05:21

  

Troy McDonald Kane: you missed it. You missed the first five minutes.

Edwin Johnson: poetry. You know, amazing how many things ran with deck.

Brett StClair: if you're a Kiwi, you're from New Zealand.

Edwin Johnson: That's right.

Brett StClair: I like my large deck.

Edwin Johnson: That's right.

Brett StClair: I like to polish it.

Edwin Johnson: Yeah, indeed he does. By the way, you know who's like continuously up my gulo is your boy Julian and Snot

George Westbrook: Oh Yeah,

Edwin Johnson: rot.

George Westbrook: keep on seeing emails coming through from him.

Brett StClair: Do you want me to manage it?

George Westbrook: Any status updates?

Brett StClair: I can manage it.

Edwin Johnson: Can you manage it for me?

Brett StClair: I'll manage.

Edwin Johnson: cuz I'm literally in a I'm I am so irritated at

Brett StClair: I'll manage it.

Edwin Johnson: the moment I could literally choke people through screens, but I may have a chance to do it in person. So, we'll see what happens.

Brett StClair: Who's Matt?

Edwin Johnson: I'm sorry.

Troy McDonald Kane: He's our chief legal

Brett StClair: Did you say you

  
  

### 00:06:13

  

Edwin Johnson: Oh, Matt Voggler.

Troy McDonald Kane: officer.

Brett StClair: met?

Edwin Johnson: He's uh one of our uh well uh he's a young guy that was my lawyer for he was at a bigger firm and about it's a long time now about 12 years ago. Um I said listen leave the law firm and I'll back you and you become your own law firm but I'm your I'm your number one client always.

Brett StClair: Nice.

Edwin Johnson: So, well, we're very, very close, but he just had a baby and he's really behind on a number of things that have caused me a lot of discomfort.

Brett StClair: Yeah. So, I know that feeling, right? O having a baby and a discomfort.

Edwin Johnson: Yeah, I mean, yeah, I'm pretty frustrated.

Brett StClair: Oh,

Edwin Johnson: So, uh, but we we're going to take care of some stuff today. Um, okay, cool. Listen, the uh the work on the deck, I think looks and you know, it's it's beautiful,

Brett StClair: it's

Edwin Johnson: right? And when you see the accompanying uh workbook, uh I made just a couple of tweaks in terms of like the titles and s*** like that that just didn't make a ton of sense uh of sense.

  
  

### 00:07:19

  

Edwin Johnson: But I think we're in a position where we can send this to the Israeli mob and the hardrack guys and frankly any other investor who's uh institutional is going to ask for things like this. I don't know if anyone's had a chance to look at the workbook itself, but it's

Brett StClair: It's

Troy McDonald Kane: Yeah.

Edwin Johnson: comprehensive.

Troy McDonald Kane: I haven't se I've only seen what you've sent.

Brett StClair: comprehensive.

Troy McDonald Kane: I haven't seen the final product,

Kevin Murray: Yeah.

Troy McDonald Kane: which would be great to see. I've only seen your your documents that you sent to create the document.

Edwin Johnson: Oh,

Kevin Murray: All right.

Edwin Johnson: okay. Well, let me let me send this out to the group right now because I'll forget otherwise. Um,

Brett StClair: And then a related question. Everyone see Ganesha's

George Westbrook: Yeah,

Brett StClair: post.

George Westbrook: I think that sounds on it.

Edwin Johnson: How are we doing on that Apple store

Troy McDonald Kane: Jesus.

George Westbrook: I don't I don't think they've replied yet.

  
  

### 00:08:11

  

Edwin Johnson: b*******?

Brett StClair: Okay.

George Westbrook: So,

Brett StClair: Thank

George Westbrook: we've we've sent our response and they're Yeah, I think it was last Have a look.

Brett StClair: you.

George Westbrook: Still connect.

Cody Haugen: I don't know if it still lives in the same process, George, but if I go into that developer portal um and I don't know, raise hell with either another email or submit another ticket or tell them to call us,

Edwin Johnson: Hello.

Cody Haugen: is that worthwhile or

George Westbrook: Uh I think Hassan you

Cody Haugen: Or is that is that the same portal that you guys Yeah.

Troy McDonald Kane: That's the same portal. Hassan has access to it. So,

George Westbrook: Yeah.

Cody Haugen: All right.

Hasan Ahmed: Yeah.

Troy McDonald Kane: yeah.

Cody Haugen: Yeah. Okay.

Hasan Ahmed: Um,

George Westbrook: Um I mean as far as study

Hasan Ahmed: I mean like as far as I know like I believe if it's like extremely urgent you you are able to like speak to them as in like if we want it like ASAP like we we we are able to let them push through and ask them are they able to let them check it ASAP and so um I mean I'm I

  
  

### 00:09:14

  

Troy McDonald Kane: Yeah.

Hasan Ahmed: mean I'm unsure how to do that but I will have a look and see if I can try to get them to

George Westbrook: try to go.

Hasan Ahmed: just check it through ASAP so we can can actually get the app out as soon as possible.

Cody Haugen: Yeah, appreciate

George Westbrook: Yeah, I think they said Yeah,

Kevin Murray: Go kick some doors down.

Cody Haugen: it.

George Westbrook: they get your uh get your baseball bat. Um, I think yeah,

Brett StClair: Is

George Westbrook: because I think they it was last well the 15th at 2:30 and then we sent we sent our

Brett StClair: it?

Troy McDonald Kane: Yeah.

George Westbrook: response like 45 minutes later and they're still not they're still not back.

Troy McDonald Kane: Yeah.

George Westbrook: So, let's get the baseball bats

Edwin Johnson: Yeah,

George Westbrook: out.

Edwin Johnson: that boy. I wish it was like that again.

Cody Haugen: Yeah.

Edwin Johnson: You know,

George Westbrook: Yeah, go to go to Certino and not start knocking on the doors. I doubt they'll be working there though.

  
  

### 00:09:58

  

Troy McDonald Kane: See

Edwin Johnson: you know,

Cody Haugen: Heat.

Edwin Johnson: when I grew up, George, there was a time and a place here in Chicago that if you had a you had a beef with someone, nobody sued anyone. Like you you just you handled it,

George Westbrook: Yeah,

Edwin Johnson: you know? It's like it's crazy.

Troy McDonald Kane: that?

Edwin Johnson: That's not That's different. I mean,

George Westbrook: it's the gypsies over here still do the same

Edwin Johnson: I I grew up in an era Yeah. an an error here in my neighborhoods.

George Westbrook: thing.

Brett StClair: Amen.

Edwin Johnson: Like there were two car bombings where like guys got out of line, got blown up, killed.

George Westbrook: I suppose that's what that's one way to sort it

Edwin Johnson: Yeah. Yeah. I don't know if you know this. I don't want to digress, but real quick, funny no interesting story.

George Westbrook: out.

Edwin Johnson: I live in a suburb called Hinsdale, which is a a pretty nice suburb west of Chicago.

Brett StClair: Okay.

Edwin Johnson: um uh the fir I would say one of the first not it's it's about 12 miles away from downtown and it it it is a nice area um but there was a guy who was um he's running a a trucking business that was being like shaken down by local

  
  

### 00:11:02

  

Edwin Johnson: uh like figures like that you know bad guys and uh well whatever maybe not so bad some bad things but not so bad people um anyways this particular guy um he started he got a subpoena from the government about his uh

Brett StClair: Yeah.

Edwin Johnson: his billing and uh he that he lived maybe three or four blocks away from me. This is in I think in like 1987 or something. I don't remember the exact year. Anyways, he drove uh on the on-ramp to get on the to the highway and as soon as he did um they they hit a a button and and blew him up.

Brett StClair: What the

Edwin Johnson: And um interestingly like prior his wife and daughter or his wife and son were in the

Brett StClair: heck?

Edwin Johnson: car and um but you know in where I grew up some of the guys who were involved in that I knew who they were and then odd the the funny part is the son who lived even though he got close to getting blown up too I actually met uh he's a friend of a friend of mine.

  
  

### 00:12:01

  

Edwin Johnson: The mom got remarried. He has a whole different name and it just he told me the story and I got the chills. I was like, "Oh s***, crazy." Yeah. Really, really interesting. But nonetheless, um all right, so here we go. Um we have Man, do we have a lot to do quick.

Brett StClair: I can make it.

Edwin Johnson: Um,

Brett StClair: Do we do do do do do do do do do do do do do do do do do do do do do do do do do do do do do do do do do do do do do do do do do do we do do we want to rather get George and the son to ask the questions so we focus it down on what we want what we understand if you can update us and we go from there and we quickly smash us out is that a

Edwin Johnson: yes.

Brett StClair: a master

Edwin Johnson: Perfect. Perfect.

George Westbrook: I uh I think yeah I think

Edwin Johnson: You got me for about 15 minutes.

  
  

### 00:12:37

  

Edwin Johnson: So,

Brett StClair: approach

Edwin Johnson: whatever I can trouble with, the boys got you.

George Westbrook: it' be preliminary questions before a bigger a bigger session um because it's just yeah understanding because I I think we've we've got a better understanding of where it fits into it. So what we thought before was it was something that sits in between the user and tZERO and effectively the user speaks to the market maker blah blah blah. Obviously now we're aware that it's not that but this is our current understanding. So a user places a places a trade or places an order um that goes to tZERO. tZERO has an order book which has all of the orders. The market maker acts as like a a bot which would be placing orders, buy, sell orders um into the order book within um within tZERO which has their matching algorithm which is going to match

Edwin Johnson: Correct.

George Westbrook: up match up the orders. Um,

Edwin Johnson: Correct.

George Westbrook: I've got this I'll share this part of my screen cuz this is

Edwin Johnson: So, the market makers just as you share,

  
  

### 00:13:40

  

George Westbrook: just

Edwin Johnson: they post what's called resting liquidity. Okay. They're going to they're going to put orders that are going to be passively in the market for people to hit

George Westbrook: Mhm. Yeah.

Edwin Johnson: bids and offers, right?

George Westbrook: as well as as well as so a let's imagine there there isn't a market maker obviously then that would be I buy I place a buy order Hassan places a sell order if they match then they would get consumed or filled um and then with the market maker it's doing that same thing but obviously just at a higher frequency with algorithms behind it in order to do it but there is a possibility that if I placed a buy order and Hassan placed a sell order, they match, they would get consumed. It doesn't have to be the market maker.

Edwin Johnson: That's

George Westbrook: Market makers. Okay. And then obviously part of the market maker is there's the So there's these two things,

Edwin Johnson: correct.

George Westbrook: the valuation system and the is it the market conditions.

  
  

### 00:14:40

  

George Westbrook: Um, one of the things we're not not too sure is how is the the market conditions um worked out because I'm aware. So the market conditions they do the the spread and it's like five five other variables isn't it which then determines the like the pricing levels, the the amount of orders that there's there's still some things we need I think I need

Edwin Johnson: Correct.

George Westbrook: to look through.

Edwin Johnson: You got a great handle.

George Westbrook: Um,

Edwin Johnson: But it's actually called market state. So like what the Yeah,

George Westbrook: market state and then the market state determines the the orders that

Edwin Johnson: market state. So

George Westbrook: the market maker's going to send to tZERO's order book,

Edwin Johnson: you

George Westbrook: which then will be available for the users order to match against. And I suppose also the the market makers orders to match against what a user might do. So let's say if the market maker is like right I want to sell the user wants to buy it's going to match against that then that get then that asset gets allocated to the market makers portfolio.

  
  

### 00:15:41

  

Edwin Johnson: if the market maker is on one side of the order. Yes. Yeah. And the market maker has the nice part about the simulation or skill-based competition is the market

George Westbrook: Okay.

Edwin Johnson: maker, we're not risking any of our own capital yet. So the market maker we can start to see what the like risk tolerance is and any kind of market data to

George Westbrook: Yeah.

Edwin Johnson: model how tight we want the bid at spread spread to be and how deep in terms of

George Westbrook: H

Edwin Johnson: order quantity want we want to rest above and below the fair value price that we're going to we're going to determine a

George Westbrook: is the is the buying power of the market maker fixed at the start or can it fluctuate? like are you going to inject more capital into the market maker given certain market conditions?

Edwin Johnson: The market maker will never have a limit on what it can do on

George Westbrook: Okay.

Troy McDonald Kane: Yeah,

Edwin Johnson: capital.

Troy McDonald Kane: she almost set the capital buying power to like like $100 million or something like

  
  

### 00:16:33

  

George Westbrook: Okay.

Troy McDonald Kane: that. So there Yeah.

Edwin Johnson: 100 billion probably

George Westbrook: Yeah. So,

Troy McDonald Kane: Yeah.

George Westbrook: it's effectively effectively limitless and it's there to maintain the two-sided liquidity

Troy McDonald Kane: Yeah.

George Westbrook: in the market so that there's always a potential to buy and always a potential to sell from a users's perspective.

Edwin Johnson: That's

George Westbrook: Okay.

Troy McDonald Kane: And when we meet with tZERO tomorrow,

Edwin Johnson: correct.

George Westbrook: Um

Troy McDonald Kane: so we're now doing two a week with tZERO for tech calls starting this week.

George Westbrook: Mhm.

Troy McDonald Kane: So we have we're doing these calls Monday, Wednesday, Friday, and then we're doing the tZERO calls on Tuesdays and Thursdays. We need to have them set up this synthetic market maker entity uh with that buying power so you guys can start to maybe test that in the QA

George Westbrook: is what's what's the difference between a user and a synthetic market maker as a like

Edwin Johnson: Yes.

Troy McDonald Kane: environment

George Westbrook: an entity technically is it because part of my head I'm thinking surely it's just exactly the same it's just the amount of capital it's got is close to limitless

  
  

### 00:17:38

  

Edwin Johnson: Correct.

Troy McDonald Kane: that in in a production world they don't have to locate shorts. They get an exemption for that because they're designate, you know, they're providing liquidity designated market maker. So that's the other big nuance is that they they don't have as many of the shorting restrictions as they in a production

George Westbrook: H.

Troy McDonald Kane: environment they would if they were not a designated market maker.

George Westbrook: Hm.

Edwin Johnson: I also and If we're talking about production, they also tend to get favorable um risk risk control too because you know for example that you know if we offer subs

Troy McDonald Kane: Christ.

Edwin Johnson: membership subscriptions and we know that these people have to put up $5 million in an account for us to be a a subscribed member. You know that they have another buffer of risk capital. So we, you know, market the the the clearing entity tends to give the market maker favorable treatment on their money, more risk for

George Westbrook: Would the synthetic market maker exist in the production environment as well,

  
  

### 00:18:34

  

Edwin Johnson: less.

George Westbrook: but it would rather it be one of many participants

Edwin Johnson: We're going to see how that goes. We're going to see how the simulation goes for football and basketball and then we're going to come back.

George Westbrook: or

Edwin Johnson: I mean, at the end of the day, if we don't get the market makers to sign on at the terms we want them to sign on, then we're going to do it ourselves and and we'll open up another company and become the market maker. The thing about marketers is they generally don't lose

George Westbrook: then

Edwin Johnson: money out of

George Westbrook: because that's I remember looking at this that there's the the hierarchy of things that they want and then

Edwin Johnson: ever.

George Westbrook: profit seeking is right at the bottom. Would that change in would that change in production and that profit is going to be higher up the hierarchy because obviously at the moment it's maintain stable market conditions two-sided liquidity blah blah blah um but I can imagine

Edwin Johnson: Yeah, I mean it goes to the top.

  
  

### 00:19:34

  

Edwin Johnson: I mean, if we're going to be the market maker, profitability is first. So then, you know, once we have the data,

George Westbrook: Yeah.

Edwin Johnson: we can model how aggressive we want to market make, meaning how tight we want the bid ass spreads to be at certain periods throughout the game. Um because like for example, you know, if the game's a blowout and um you know, it's already a foregone conclusion, the spreads may get a little bit wider from the buy side and the sell side. If it's a very close game, um the buy and sell uh tightness should be, you know, closer than something that's a little bit more of a predetermined outcome.

George Westbrook: with I think I think I know the answer to this but I'm gonna ask it anyway and I think it might be a stupid question So the middle. So you got the you got the bid, you got the ask, you've got that middle price. Is that the reference price or whatever it's called?

Edwin Johnson: It is.

George Westbrook: The reference price.

Kevin Murray: Thanks.

  
  

### 00:20:26

  

George Westbrook: Is the is the distance between the bid and the

Edwin Johnson: Yeah.

George Westbrook: ask always equal um either side or is it sometimes it skews?

Edwin Johnson: Sometimes it's skewed because like for example in a in a production environment if let's say you buy a whole bunch of shares and um you want to you you know it's kind of like being a bookmaker. You want to be as balanced as possible. You don't want to have, you know, too much directional risk because your business is capturing the spread between the bid ask

George Westbrook: H.

Edwin Johnson: in a perfect world. I mean, it doesn't always work like that, obviously, but if you're long a bunch of shares, okay, let's say you're generally two ticks below the reference price on the bid and two ticks below the reference price on the off or above the reference price on the offer. And let's say that you're long a ton, you're probably going to make uh your offer at the reference price. We'll lower it so buyers can come in and you can offload some of those shares that you're

  
  

### 00:21:27

  

George Westbrook: And then that part of the algorithm is the bid offset and the so you have the base spread and then

Edwin Johnson: long.

George Westbrook: I suppose it's base spread plus and minus on the reference price and then the bid offset and the ask offset and then that's what determines how far right or far or how

Edwin Johnson: Correct.

George Westbrook: close it is on the the left.

Edwin Johnson: That's right. And one of the things that I I want to do is offer um this is what I've done in the past when I've been

George Westbrook: Okay.

Edwin Johnson: a market maker is a randomizer. So the randomizer will be um a condition that the market maker can be in where you modify the number of shares that you're going to bid for and offer for randomly. So there's no rhyme or reason. And then occasionally, let's say that you were to get um again in that example where you're really long. Uh let's say you're long, you know, 50,000 shares and you only want to be long 10,000. Um on something like that, um we would, you know, randomize a market order.

  
  

### 00:22:29

  

Edwin Johnson: Um that odd, oddly enough, would buy more, but would push the price higher so you can offload the 40,000 shares at a higher price. So let's say, for example, you're you're long an extra uh 50,000 shares and you only want to be long 10,000. What what I would do um would be, you know, I would buy another 10,000 at the market and I wouldn't rest. I would just go market order and I'd rip the market higher and then all the prices that backfill after I ripped the my market higher.

Kevin Murray: Thank

Edwin Johnson: That's where I sell my my now my new 50,000 I want to get out of.

Kevin Murray: you.

Edwin Johnson: So, it's, you know, you can you can move the market to your favor by buying a whole bunch because you want to exit at a higher price with the

George Westbrook: And and so a you a user can only do limit orders,

Edwin Johnson: 40,000.

George Westbrook: but would the designated would the market maker be able to do um market orders as

Edwin Johnson: No, we'll put the we'll keep everything at a limit order,

  
  

### 00:23:27

  

George Westbrook: well?

Edwin Johnson: but a limit order in function you can still cross. So, let's say the market seven bit at 8. If you want to fill, you know, all the way up to 10, you you put an order to buy 11s.

George Westbrook: you. Yeah. And then it's always going to be filled. Okay.

Edwin Johnson: So, you get eight,

George Westbrook: Yeah. Okay,

Edwin Johnson: nine,

George Westbrook: that makes

Edwin Johnson: 10. Yeah.

George Westbrook: sense.

Troy McDonald Kane: Yeah, one thing we should talk about at some point is how do we create our own market order type on the

Edwin Johnson: 11.

Troy McDonald Kane: app so that it can be synthetically mar like we still have to talk through that a little bit because there's a little concern that people will go and put in a price and miss the market, frustrate it. But if there's a way for us to create a function, a synthetic market order on the app that just guarantees they get filled essentially um when they place the

George Westbrook: could there's a cancel.

  
  

### 00:24:17

  

George Westbrook: You can cancel an order,

Troy McDonald Kane: order

George Westbrook: can't you? Yeah. So one potential thing is is like time bounded. So where a user places an order and then we go a certain certain amount below like let's say let's say if they want to Yeah. So they they place a synthetic market order um at that price and then what we do is every like 5 seconds if the order hasn't been filled we cancel the order and then move the the price down or up so that it's going to get filled at some point. Um it's just obviously in like really volatile markets I can imagine that price increase or decrease could mean that it might need to be that should be fine.

Edwin Johnson: Yeah, I mean the user we don't want the user experience to be frustrating. That might be something we need before our first game or at least before the first NFL game is

George Westbrook: Um,

Edwin Johnson: a synthetic market order, Troy.

Troy McDonald Kane: Yeah.

Edwin Johnson: And it can be something that that bids through.

  
  

### 00:25:17

  

Edwin Johnson: It's pretty I I mean I imagine it's pretty simple if the market six bit at seven you could just say a market

Troy McDonald Kane: Yeah.

Edwin Johnson: order prices through five prices you know so you instead of like you know buying sevens you buy twelves it's going to fill you at the best price anyway

George Westbrook: What? When you say like six bid seven, what does that what does that

Edwin Johnson: it means that the buyers are are at six.

George Westbrook: mean?

Edwin Johnson: So the bid is the the best bid price is price is six and the offer the lowest offer price is seven. So when we we quote a market it's always you know bid ask 67 67 market goes up 8

George Westbrook: Okay.

Edwin Johnson: n 89 you know 10 11 and it's basically just you're always quoting two. There's no like there's no single price when you're talking about a market.

George Westbrook: Yeah.

Edwin Johnson: There's a bid and an ask. You can have a last traded price but that's that's kind of irrelevant. It's what the bid and the ask is.

  
  

### 00:26:12

  

Edwin Johnson: So on the on the synthetic market order, Troy, we could just have it priced through

George Westbrook: Yeah.

Troy McDonald Kane: Yeah, I think that's and that's how CME does it. That's how other exchanges do it.

Edwin Johnson: it.

Troy McDonald Kane: That's how brokers typically do it because believe it or not in equities market orders don't really exist. The brokers create synthetic market orders that that trade through the market. And so let's say it I don't even I don't even take the price right now. Let's say I want to put in a sell market order. We have to take that bid price and then we subtract so many price levels at

Edwin Johnson: All

Troy McDonald Kane: that point.

Edwin Johnson: right.

Troy McDonald Kane: So it's guarantees it will it will match through. And I can help you write that logic for sure.

George Westbrook: So could it be when you do a market order, do you have a kind of upper bound? Found. So if you want to buy you just go I want to buy at the market price but if it go if

  
  

### 00:27:00

  

Edwin Johnson: No,

George Westbrook: if in between now when I click

Edwin Johnson: no, no.

George Westbrook: buy.

Edwin Johnson: A market order means whatever you get, you

Troy McDonald Kane: Yeah.

George Westbrook: Okay.

Edwin Johnson: get.

Troy McDonald Kane: Until you're exhausted or there's no

George Westbrook: Okay.

Troy McDonald Kane: market.

George Westbrook: Okay. Um, and

Edwin Johnson: We should talk about the trading ban. So, Troy, too.

Troy McDonald Kane: Yeah.

Edwin Johnson: So like the only way that so let's say you place a market order and that market order

George Westbrook: then

Edwin Johnson: is you know it's 67 again six bit at seven and you get filled at a price of 85 you know likely that would be outside of our price band okay which would be a 30% or whatever we're going to come up with correction and we would as the exchange or with tZERO we have a ability to quote bust a trade or say the trade didn't happen. So our our we have to maintain orderly markets, you know, for regulatory purposes because if everyone got banged out on these market orders, you know, you'd lose market participation really really quickly.

  
  

### 00:28:04

  

Edwin Johnson: Okay? So we'll we'll talk about that uh you know over the next couple of days. Just bear with me today. You know, today's going to be a b**** for me. So I'm I'm going to be in about another two three minutes.

George Westbrook: And one one last thing is the this the CTS1 and CTS2 are they are they things that

Edwin Johnson: two. Yep.

George Westbrook: are they things that we would have to build as well or is they are they things that we would consume from tZERO.

Edwin Johnson: We will build them.

George Westbrook: Okay.

Edwin Johnson: Yeah. So, it's going to they're fairly simple. Okay. There's a lot of like I didn't mean to make that thing like I meant it for Claude to read it, not for everyone else to read it other than get kind of like a peripheral. But basically there's two main price drivers and that's going to be your probability for this exact game that is happening at the moment. And then the probability of all the other games combined come up with a price.

  
  

### 00:28:59

  

Edwin Johnson: We add that together. That's your onfield revenue. And then you add in the off-field revenue that we we've created between the onfield, you know, today's game plus all the rest of the games combined plus the off- field. That's going to be your share price. And that share price, okay, again, is going to be moving off field is going to also be, you know, it's not guaranteed every game. So, that's another one that's interpretive, which makes this a great market to trade because nothing is like ironclad like, hey, you know, it's $2 next game for this team off field. We don't know yet. And that that makes the market really really dynamic for trading.

George Westbrook: and and in terms of so what's called it 170 odd teams um

Edwin Johnson: Yep.

George Westbrook: there would there would effectively be for each of those teams the calculations happening and then the ones that would act as larger inputs above would be the ones for the whole

Kevin Murray: Oops.

George Westbrook: market. Holistically.

Edwin Johnson: I don't know with them.

  
  

### 00:29:59

  

Edwin Johnson: So restate that, George. I didn't

George Westbrook: So there's obviously going to be well not obviously um so for

Edwin Johnson: follow.

George Westbrook: each team there's going to be some calculations done to work out the market state of that team in addition to the market state for the whole market.

Edwin Johnson: Yep.

George Westbrook: So then in a in a calculation

Edwin Johnson: I I wouldn't call it a market state for each team.

George Westbrook: for

Edwin Johnson: I would say for each market because each team's going to have their own market. when you have the two teams playing, you know, it's like Dallas Cowboys versus Chicago Bears.

George Westbrook: H.

Edwin Johnson: There's going to be a share price for the Chicago Bears and a share price for Dallas Cowboys. And the interesting part about this is like when you're trading it, if it was just a single like security, you could either go long or short the one issue. So like like for example, if I try to buy the Bears, but I miss them, well, I could still sell the Cowboys if I wanted to if I was trading that intraame.

  
  

### 00:30:55

  

Edwin Johnson: So, I've got four outlets there, you know, for each

George Westbrook: And then does the the let's say the

Edwin Johnson: hand.

George Westbrook: market state for the Cowboys that's going f****** Crazy. Um, is that going to affect things that happen in like the the bears?

Edwin Johnson: No,

George Westbrook: Okay. So,

Edwin Johnson: no.

George Westbrook: all independent isolated markets that are

Edwin Johnson: Correct.

George Westbrook: Okay.

Edwin Johnson: Correct.

George Westbrook: Okay.

Edwin Johnson: which is again if you just isolate another really cool trading um input that people could look at is if the team that they're playing goes a****** uh there may be some edge that you can grab from the bearish trying to identify when that team's liquidity dries up

Kevin Murray: Yes.

Edwin Johnson: or someone rips it or sells it. You know, you could do could do a lot of interesting stuff.

George Westbrook: Yeah. And I suppose because the because the amount of money that the market maker has is effectively infinite, it can afford to do that because it's not limited by capital. So it doesn't matter if it's absolutely crazy on one because it's not like a normal company where it's got a fixed amount of money that it can put into the market.

  
  

### 00:32:05

  

Edwin Johnson: Well, you'd be surprised, Troy can tell you stories how much money the market makers put towards even traditional stocks. I mean, Troy worked at this, you know, I think the largest market making company in the world at Citadel Securities,

Troy McDonald Kane: Yeah,

Edwin Johnson: served the biggest, right?

Troy McDonald Kane: they're the largest. Yeah.

Edwin Johnson: Yeah.

Troy McDonald Kane: Mhm.

Edwin Johnson: And what do you guys like roughly make a

Troy McDonald Kane: Uh last year they made 12 billion,

Edwin Johnson: year?

Troy McDonald Kane: I think. Yeah.

George Westbrook: Not bad.

Troy McDonald Kane: Um I mean Jane Street's the king of the castle. They made like 20ome billion last year, but they're they they trade a lot of diverse stuff. They trade a lot of equities, but they also trade a lot of mainly ETFs. They're like one of the biggest ETF market making firms out there. We're sitting mostly single.

Edwin Johnson: And they're also somewhat controversial. They've been in a little bit of trouble in India and other places for,

  
  

### 00:32:51

  

Troy McDonald Kane: Yeah.

Edwin Johnson: you know, market tactics.

Troy McDonald Kane: Yeah. Bye.

Kevin Murray: Let's

Troy McDonald Kane: It used to be Citadel was the most profitable market maker out there and Jane has deanth thrown them. But when I say largest, I mean the largest breath. They make in the most markets. They make in 37 countries. They make every symbol almost every asset class now.

Kevin Murray: go.

Troy McDonald Kane: Uh and they deploy billions of dollars of capital in the market every day.

Edwin Johnson: So there's your

George Westbrook: Hence why they I think like the juniors the juniors come in are getting paid ridiculous

Edwin Johnson: limit.

Troy McDonald Kane: Yeah. I mean interns get like 250 for the summer US.

George Westbrook: money

Troy McDonald Kane: Yeah.

Edwin Johnson: You know anyone that can hire me?

George Westbrook: that

Max Kingaby: went there and then he got arrested. He's still in prison.

Troy McDonald Kane: Gelber.

Edwin Johnson: What's

Max Kingaby: He started a company. Is it what?

  
  

### 00:33:44

  

George Westbrook: Let me mute

Max Kingaby: What was the company he started?

Edwin Johnson: that?

Max Kingaby: Curly brown hair. Huh? No one can hear you. Why? George is saying no one can hear me. Can everyone hear me?

Troy McDonald Kane: We can hear

Max Kingaby: Yeah. There's a guy uh curly brown hair.

Kevin Murray: Yeah.

Troy McDonald Kane: you.

Max Kingaby: Um he started sorry uh he's he's

Edwin Johnson: Oh, curly brown hair. H hair. Sure.

Max Kingaby: still in prison now but he like afforded billions of dollars and he he went to James Street before he started up his business. I'm trying to remember what it's called.

Troy McDonald Kane: Oh,

George Westbrook: Silicon Valley

Troy McDonald Kane: the crypto. Yeah.

George Westbrook: Bank.

Edwin Johnson: He did a market maker as well.

Max Kingaby: What's the second street?

Edwin Johnson: They just hit all the losses.

Kevin Murray: Is it f***?

Edwin Johnson: Like it ain't I mean that he was a brilliant guy, but they were dumb as f*** when it came to market making cuz that like it's it's basically a printing of money unless you're you know mildly retarded because they're giving you edge.

  
  

### 00:34:42

  

Edwin Johnson: every trade you get an edge if you want it. Okay, you got to manage it. But like it's it's not rocket science by the way to be a market maker. You you don't have to be really that smart.

Troy McDonald Kane: All

Edwin Johnson: You need technology and capital. It's about it. So, um all right, anybody? I'm I guess I'm out. I'm going to wish everyone a great day. My team, I'll be back in touch when I'm back.

Troy McDonald Kane: right. Good

George Westbrook: have a good

Kevin Murray: Sounds

Edwin Johnson: Thank you.

Troy McDonald Kane: luck.

Skye Capazorio: Good luck.

Edwin Johnson: Thank you very much.

George Westbrook: day.

Edwin Johnson: See you guys.

Cody Haugen: All right.

Kevin Murray: good.

Brett StClair: Hello.

Troy McDonald Kane: Any

George Westbrook: Um, so I suppose rest of the

Troy McDonald Kane: other any I mean I might be able to answer a few more questions if you have you know

Brett StClair: Good.

Troy McDonald Kane: around market structure uh not how to for that document that Edwin wrote but

  
  

### 00:35:29

  

George Westbrook: So I think I think I think what we need to do is it's I think I we were under the impression that it was that the PT whatever the PTS01 um but we need to have a look through the the other ones the more foundational ones because I was reading it and then I was looking basically we took that document and then built a built something that was a bit easier to understand. Um and then we need to go back do the same for the other ones and then then map it map it all out. But um it's Yeah, it it's a lot. It's a lot. But yeah, especially coming from not that background. But we'll get we'll get something

Brett StClair: George,

George Westbrook: sorted.

Brett StClair: do you see this is a automated kind of bot that's firing non-stop? Is is this how it's going to operate?

Troy McDonald Kane: Yeah,

George Westbrook: Yeah.

Troy McDonald Kane: I mean all the market making firms out there run full blackbox algos when their liquidity

Brett StClair: Right.

Troy McDonald Kane: is it's really it's just a set of conditions in the market.

  
  

### 00:36:24

  

Troy McDonald Kane: what if statements when they widen and tighten their spreads, they have most market making firms have obligations to get the incentives that Edwin talked about. So, um you know, they're required to make a certain width, size up, certain percent of the day. Um and then they, you know, there's usually a setter and then other market makers are leaners. And so it's, you know, whether or not, you know, what we're trying to create is we're trying to be the setter of the market as the market maker to to drive

Brett StClair: falling.

Troy McDonald Kane: trading decisions one way or another, but also have to be somewhat market neutral. Uh because you're making both sides at the same time.

Brett StClair: And so it's calling the API and deciding what it's going to be trading on, right? It isn't waiting on signals from

Troy McDonald Kane: It's it's feeding everything off market data.

Brett StClair: zero.

Troy McDonald Kane: It's going to feed off of the tZERO market data. It's going to feed off of the sports radar data,

  
  

### 00:37:20

  

Brett StClair: So it's all coming in and then it makes a decision real time what it's going to make a bid or

Troy McDonald Kane: right?

Brett StClair: trade.

Troy McDonald Kane: Like let's say the Bears score a touchdown buy.

Brett StClair: Now buy on the bears.

Troy McDonald Kane: Bears have a turnover sell. like there it's as it's as simple as that to a certain extent,

Brett StClair: Okay.

Troy McDonald Kane: but it's also where you want the like your bid um uh spread to be like you want to be tight, wide, like it's I was watching the spreads on Kelsey last night for the World Cup game. It was crazy how wide they were. Just crazy. I mean,

Brett StClair: There's a lot of transactions happening simultaneously. So, we need to think of this as an application that's kind of going,

Troy McDonald Kane: yeah.

Brett StClair: I'm building on that game, that game, that game, and this way, and it's

Troy McDonald Kane: Well,

Brett StClair: okay.

Troy McDonald Kane: really you're only looking at you got to look think of it.

  
  

### 00:38:05

  

George Westbrook: H.

Troy McDonald Kane: There's this concept in the equities world called pairs trading. And what that means is you're trading two stocks against each other.

Brett StClair: Yeah.

Troy McDonald Kane: That's essentially every game every week is those two stocks, those two team companies are trading against each other because it's based on the probability that they're going to capture that $5 in revenue. So, let's say it's the Bears versus the Packers. That's a pairs trade essentially where participants will probably be trading both team companies at the same time, not just one singularly based on the back and forth correlation of the probability that they're going to win that game and they're going to earn $5 in revenue capture. They don't care about the other 30 teams that are being played that week. They just care about that one trade for that week.

George Westbrook: H.

Troy McDonald Kane: Where in the broader equities world, signals can come from all different places like it could come from hundreds of

George Westbrook: The Yeah. Whereas this is only

  
  

### 00:39:01

  

Troy McDonald Kane: symbols,

Brett StClair: So,

Troy McDonald Kane: you know.

George Westbrook: Yeah.

Brett StClair: what happens if what happens if someone's trying to sell some shares

Troy McDonald Kane: Yeah.

Brett StClair: and the market maker the algorithm doesn't pick up on that and it can't

Troy McDonald Kane: No, they will.

George Westbrook: It it is

Brett StClair: sell.

Troy McDonald Kane: That's passive. It's already known that they're out there in their

Brett StClair: Now,

Troy McDonald Kane: markets.

Brett StClair: I'm just saying the algorithm doesn't fire or doesn't kick in or fails

George Westbrook: because the market there's there's

Troy McDonald Kane: It's constantly what we say kids are replacing their quotes.

George Westbrook: going to be orders from users as well.

Brett StClair: or

Troy McDonald Kane: It's constantly recalibrating the quotes, moving them. They're not waiting to be traded before they change their markets. They're moving the markets based on the action of the game or the action of the market. So again,

George Westbrook: All

Troy McDonald Kane: maybe a better analogy is that the Bears score a touchdown,

  
  

### 00:39:38

  

George Westbrook: right.

Troy McDonald Kane: I'm going to move my bid offer up. Bears get a turn a turnover,

Brett StClair: Yeah.

Troy McDonald Kane: I'm going to move my bid offer down because the momentum is reversed.

Brett StClair: Okay.

Troy McDonald Kane: Yeah.

George Westbrook: H

Troy McDonald Kane: But you're always making two-sided quotes,

Brett StClair: Yeah. This is

Troy McDonald Kane: but you're moving that up and down like like a like a slider.

Brett StClair: quite

Troy McDonald Kane: Yeah,

George Westbrook: So,

Troy McDonald Kane: we call it a liquidity lag in the business.

George Westbrook: so then every Yeah.

Troy McDonald Kane: So, it's it's

George Westbrook: So,

Troy McDonald Kane: Yeah.

George Westbrook: then there's going to be the quotes that the market maker puts out and then when it recomputes it, it's going to cancel all of the other ones and then it's constantly cancelling,

Troy McDonald Kane: Yeah. It a cancel replace.

George Westbrook: canceling.

Troy McDonald Kane: They just wipe the book and replace it with updated quotes.

George Westbrook: What's a what's a typical like time period in which it would do it?

  
  

### 00:40:26

  

George Westbrook: Obviously, I think I looked at something where it was saying that the time period is variable, but if there was a range, is it like five times a second or five times a

Troy McDonald Kane: Oh, it's definitely going to be by second,

George Westbrook: minute?

Troy McDonald Kane: not by minute. Uh, it's gonna it's probably it's probably going to be five to 10 times per second. Like, we're dealing in milliseconds here, if not microsconds. I don't I mean it again this is all new. I mean I know there were simulators that Edwin did before but you know think about every time there's an uh a volatility moment that we're calling them like that's going to change the the price discovery of the

George Westbrook: does. So,

Troy McDonald Kane: market.

George Westbrook: as well as being on call like a let's just say the standard one without anything else is um five times every second. So 200 200 milliseconds is like the refresh rate but given an event that happens we'd have a

Troy McDonald Kane: All right.

  
  

### 00:41:22

  

George Westbrook: trigger being like so if no event do it every 200 milliseconds if event recalculate now and then publish new and then go back to the every 200 milliseconds.

Troy McDonald Kane: I think intragame that probably works. I think we also have to think about how the algos work outside of games because and I were talking about that a little bit last week.

George Westbrook: Yeah.

Troy McDonald Kane: You know, do we like we don't want tight markets like overnight when nothing's happening. Even in a simulated environment, we may go wide and just say, "Okay, the spread's $5 wide." Let everyone decide if they want to close it out themselves. The market. at least is telling you where the market is, you know, two and a or maybe two and a half wide. I don't know. But we need to talk through kind of what that quoting liquidity looks like during games and outside of games or around games. Like there's probably going to be three different sessions that change the liquidity profile.

  
  

### 00:42:18

  

George Westbrook: So I suppose like the two main inputs are the market state and the game state or games state because then then I suppose I suppose there's no playoffs so it doesn't matter but I was

Troy McDonald Kane: Yeah.

George Westbrook: going to say let's say it's one team's playing another team and then in another in another like so let's say you've got first and second are playing in a game and then third and fourth are playing in a game the impact of third scoring might have an impact on the second team's price is That's something that would be factored factored in because then I suppose then you have like a part of the equation which is like given the current um position of this team and the implication of this score on the teams above or below it how does that impact on the price? Because as I was thinking, they're they're kind of isolated markets, but given the interlinkness of one team's performance to another, are they actually

Troy McDonald Kane: they are isolated. So even though let's say it's the Vikings and the Lions are playing over here and the Packers and the Bears are

  
  

### 00:43:16

  

George Westbrook: isolated?

Troy McDonald Kane: playing over here. No matter what happens in each of the games should not impact the pricing of that game during the game. Now, once the games have concluded, let's say the Bears then play the Lions the next week and the Lions won, it could change the price because of the that. But intraame, it shouldn't affect the pricing discovery. Outside of the games, it will because then it it I don't I

George Westbrook: But yeah,

Troy McDonald Kane: Yeah.

George Westbrook: but then I think like if

Kevin Murray: Oops.

George Westbrook: Yeah, that example I gave where it's like the the teams that are very close to each other. Um obviously so if one team scores the probability of the other team winning goes down um in the same way that let's say in that other game if one team scores in in the NFL do you have like like so in Premier League you have goal difference. So like if if my team Tottenham was playing and Arsenal were playing in different games um if we both win um but are if we both win and then we're on equal points um then it's determined by the goal difference who's higher up in the table.

  
  

### 00:44:44

  

George Westbrook: Is there a similar concept in NFL?

Troy McDonald Kane: There is, but not that that quantitatively. Like there are there are tiebreaker rules on rankings, but that's just for rankings. That shouldn't play into the pricing of these securities. And then and then when we get to the playoffs,

George Westbrook: Oh

Troy McDonald Kane: it's rare that two two games are being played at the same time because then they try to space them out

George Westbrook: yeah. Is that Yeah, because the earnings Okay,

Troy McDonald Kane: more.

George Westbrook: I think I get what you mean now. The ear the earnings is not linked to their position. It's earned to It's linked to onfield and off-field

Troy McDonald Kane: It's literally their onfield revenue capture each week.

George Westbrook: performance.

Troy McDonald Kane: It's the rankings only matter if they get into the playoffs.

George Westbrook: Yeah.

Troy McDonald Kane: And since we're we're not carrying this into the playoffs,

George Westbrook: Okay.

Troy McDonald Kane: the rankings actually shouldn't play too much into that.

George Westbrook: Okay,

Troy McDonald Kane: Did you

  
  

### 00:45:27

  

George Westbrook: I I get what you

Cody Haugen: Yeah, that that's exactly correct. Yeah, the the rankings are never like point differentials in football,

George Westbrook: mean.

Troy McDonald Kane: have

Cody Haugen: George. It's always how the the wins and losses and then they'll go by conference or by division first and then they'll go by conference. So, it's always wins over X team and in this division or this conference. So the tiebreers are always wins, losses, and ties. It's never points for or

Troy McDonald Kane: Yeah.

George Westbrook: Okay. Yeah. And then Yeah,

Cody Haugen: against.

George Westbrook: because I think that's where I was confusing where I was thinking is the the user is going to trade for the position on the table that they're not, but they're not. It's for the onfield and off-field performance. Onfield, if they win, they get points, lose, that they get less money. And then the off-field performance as well. Okay. Yeah, that makes sense. They are truly isolated.

Troy McDonald Kane: It should make it easier for you to do the the algos because you don't have to worry about too many things outside of that.

  
  

### 00:46:16

  

Cody Haugen: Yeah.

Troy McDonald Kane: That's why I was trying to use the analogy of pairs trading.

George Westbrook: Yeah.

Troy McDonald Kane: Just think of these all as pairs trading each week where you're just trading against the two symbols based on the probability of capturing that $5 on field revenue.

George Westbrook: Okay. And oh, f****** forgot what question I was going to ask. Um,

Brett StClair: Thank

George Westbrook: that's what I was going to ask.

Brett StClair: you.

George Westbrook: The So is there a given an event like a so like a touchdown versus a sack? Is there like an a set impact on price that would happen when or a set impact on the market maker when it's one event compared to another event or is it just positive and negative and then the amount of positive things in a because I can imagine like a if you sack somebody that's positive but it's not as positive as if you've just scored a

Troy McDonald Kane: Yeah,

George Westbrook: touchdown.

Troy McDonald Kane: I mean those are all good. This is what makes this kind of a little bit of an art versus a science because investor sentiment is what drives that if it's if if it's material or not is that it depends on where the stack comes.

  
  

### 00:47:30

  

Troy McDonald Kane: Is it on the fourth down? Is it on the third down? Is it are they where are they on the feet? Like there's so many other criteria that could determine, but everyone may have a different opinion of that. I may say, "Oh, that was a great play." You know, I may I may sell or buy based on that play. Other investors may say, "It's not material." You know, let's say it's just the first down and they get sacked. It's like not as material as if it was the third down and they got sacked.

George Westbrook: Okay. So, and then Oh, no. So, the only

Troy McDonald Kane: possibly like but but it there's so many other factors that can play into that's impact the probability of the win or not. Cody,

George Westbrook: Yeah.

Troy McDonald Kane: you would know more from the sports radar data how like is there a way for us to find like standard let's call them standard triggers that would deem like actionable,

  
  

### 00:48:18

  

Cody Haugen: I mean, no. Yeah, they're not going to because it's all subjective just like just like like I mean,

Troy McDonald Kane: right? It's all subjective, right?

Cody Haugen: yes, they are all factual things that happen, but it's it's us determining what's a big play. Is it a 20 yard run or is it a 25 yard run? like what what do you determine a big pass at 25 yards or 40 yards?

Troy McDonald Kane: Yeah.

Cody Haugen: I mean, we went through this exercise when we created some content years ago at Sport Radar and we came up with like 40 qualifying data points that determined either like a big play or an actionable item that we would showcase through this content that was automatically generated. Excuse me. And uh but it's but it's all subjective. So it's like yeah, George, you might say no, a 20-yard run is a big enough thing. That's that's 20 yards down the field. That's 20% of the field. Uh of 100 yards, it's a first down. But once again, to choice point, does that happen in the first quarter?

  
  

### 00:49:15

  

Cody Haugen: Is that the fourth quarter? Uh are you behind by 30 points?

Troy McDonald Kane: Yeah. What's the score on the board at that time?

Cody Haugen: Does the run does the 20 yard run is it garbage time and it means jack s***

Troy McDonald Kane: Right.

Cody Haugen: anyways? Like so it there's so many things. I guess my question to you, Troy, just confirming because I know I've asked this question a hundred times, but we are not determining that price though. The market determines that place based on all of those

George Westbrook: Yeah. The

Troy McDonald Kane: True,

Cody Haugen: factors.

Troy McDonald Kane: but the market maker still needs to rebalance based on those triggers because then like it's true to a point like the market makers are the setters and

Cody Haugen: Okay.

Troy McDonald Kane: and then everyone else can decide if they want to take that market, tighten that market, take the market in a different way. That's the sentiment that comes in. But the market maker still has to have some criteria for that bid offer with.

  
  

### 00:50:04

  

Troy McDonald Kane: And I know actually Edwin probably had a um and Kevin,

Cody Haugen: Mhm.

Troy McDonald Kane: you may know this, like he had to have had a set of triggers when he did the simulated modeling when you guys did that two years ago. We just have to find what that was because he was able to make that two-sided liquidity during those simulated games when you

Cody Haugen: Yeah.

Troy McDonald Kane: guys Were you part of that, Kevin? I can't remember.

Kevin Murray: No, I joined the company just after. Uh,

Troy McDonald Kane: Yeah.

Kevin Murray: but I I I do reckon he's probably got a full script of of what it is.

Troy McDonald Kane: Yeah.

Kevin Murray: I don't know as well, just throwing out there,

Troy McDonald Kane: Yeah.

Kevin Murray: whether it will come into the fact of volume as well, how many people are trading it,

Troy McDonald Kane: Yeah.

Kevin Murray: where the market making.

Troy McDonald Kane: I mean the supply demand imbalances is that's that's exactly right.

Kevin Murray: It's

Troy McDonald Kane: The volume uh the demand for volume is going to be one of the criteria as well.

  
  

### 00:50:47

  

Brett StClair: What?

Kevin Murray: Yeah.

George Westbrook: So with the with the events

Brett StClair: 3.

George Westbrook: so we kind of answered this question.

Troy McDonald Kane: I also like how Edwin's like, "Market making so easy." No,

George Westbrook: Hey.

Troy McDonald Kane: it's actually not. Otherwise, everybody would be doing it. Like, it's not. It's easy in his head because he's done it his entire career. But actually, market making is not easy because you have to take into account hundreds of permutations of what's going to

Kevin Murray: Yeah.

Troy McDonald Kane: happen off of every single trigger, off of every single actionable event. And then you gota you got to determine what your liquidity profile changes are going to be based on that so you don't get run over or

George Westbrook: Okay.

Troy McDonald Kane: you take losses and you find that edge. like I he like simplifies it sometimes and then he overengineers it in other regards like I don't

George Westbrook: So, so is the I think this is what you were were asking Cody.

  
  

### 00:51:32

  

Troy McDonald Kane: quite

George Westbrook: I just want to from my understanding. So, an event happens a touchdown. So, that's going to impact what how users trade and is the market maker going to because where I said there's the events as inputs to the market maker and the market data. Is it that there's no event data because that event happening influences the market which changes the market state which then the market maker consumes in order to spit out the new quotes or is it market data comes in and the event comes in there is some kind of categorization or number that is associated with that event which I think will probably be another custom equation which is another input all into to the other equations which then determines the

Troy McDonald Kane: Yes, in theory. So, think of it this way,

George Westbrook: price.

Troy McDonald Kane: like the an actionable moment happens, you're going to see the rest of the investors out there make a decision off of that. If they decide they want to sell, you're going to see this this demand of volume on the buy side that you need to be.

  
  

### 00:52:49

  

Troy McDonald Kane: Now, as a market maker, mean, all right, everyone's trying to sell right now. I'm going to start moving my quotes down because the market is is dictating the demand wants the market to move down or if they score a touchdown, then the market's going to start to to progress up. So, it's also reading, it's not just reading the triggers, it's reading like what the behavior of the rest of the investors are doing at off that moment and then adjusting based off of that.

George Westbrook: H and then I suppose in time the so initially it's a guess this event means it's let's just a touchdown is 0.5 for this number it's a guess but then what we can do over time is we can look at at that point that that event happens the market does this which means instead of it being 0.5 it should be

Troy McDonald Kane: That's right. That's that's exactly how why market makers do it so well because they build these predictive

George Westbrook: 04

Troy McDonald Kane: models to anticipate what it's going to do based on whatever information is in the market at that time.

  
  

### 00:53:47

  

George Westbrook: and then and then you and then you can go if there's a then you can take three

Cody Haugen: Yeah.

George Westbrook: events like let's imagine there's a touchdown here um or not a touchdown Basic. basically from let's say if somebody rushes 20 yards then they get sacked five yards and then rush 30 yards in previous previously that always usually leads to a touchdown so the market maker can assume that there's going to be a touchdown so then it can change prices

Troy McDonald Kane: Yeah. And and and and Cody,

George Westbrook: accordingly

Troy McDonald Kane: would sports radar data give us that probability like those type of forecastings at

Cody Haugen: Well, yeah.

Troy McDonald Kane: all?

Cody Haugen: So, I mean, we do have the live probabilities. Um,

Troy McDonald Kane: Yeah.

Cody Haugen: and how forward thinking those are is based off of historical data that dates back to, I think, 2000, early 2000s. Um, so there's like 20 years of historical data um that that Sport Radar uses off of those probabilities. Um so yeah I mean in now it's just whether you trust their

  
  

### 00:54:47

  

Kevin Murray: f******

Cody Haugen: permutations or like so there's two things George that Eglund has keep or mentioned in the past

George Westbrook: Yeah.

Cody Haugen: though that this also like we're going to learn as you're alluding to right the data is going to learn the data sets get larger and we're going to be able to learn from that but that's also why the simula or the trading challenge is so important so that we can take this to the market once we go into production and show market makers what is actually possible. and how to frame this thing. So, I mean, I I see it, Troy, as like I know we don't obviously want to just get burned and and we won't because Edwin obviously has experience in this and that type of thing, but like the first few weeks it might be kind of volatile on both sides. Like, I mean,

Troy McDonald Kane: Oh, I think it will be

Cody Haugen: we don't want to Yeah. until this this algorithm learns from itself.

Troy McDonald Kane: 100%.

Cody Haugen: Because once again, what we're seeing or what we're talking about right now is like, yeah, a touchdown in the first quarter is valued at potentially X, but then three weeks down the road of it learning from that is like people can score on the opening drive and then teams don't score the rest of the game.

  
  

### 00:55:54

  

Cody Haugen: So, is that touchdown first quarter really that valuable or not?

George Westbrook: Yeah.

Cody Haugen: because it's it learns that there's three more quarters in the game and there's a lot of game left and all of those things. So, yeah, I mean it's it's going to learn to what you're saying, George. I'm just reiterating it in a different way, but I think it's going to be very volatile and the first, you know, couple weeks of games

Troy McDonald Kane: Unless it's like a complete blowout,

Cody Haugen: here.

Troy McDonald Kane: which there are a couple of those games in the college series that where they play really easy teams in the beginning of the season,

Cody Haugen: Yeah.

Troy McDonald Kane: but

Cody Haugen: And and that's another thing that maybe we table that I thought about is how much value we do give that week zero of college football to this algorithm. Like maybe we do because yeah it's going to be like you know University of Alabama playing the like brothers of the sisters and poor type s***. Like it's the the blind and deaf or something like it's crazy.

  
  

### 00:56:46

  

Troy McDonald Kane: Yeah. Yeah.

Cody Haugen: Like they play some pretty low to get a win and you know basically make themselves look good for the rest of

Troy McDonald Kane: Yeah. Yeah.

Cody Haugen: this.

Troy McDonald Kane: And try their playbooks out. Yeah.

Cody Haugen: Yeah. So it's like Yeah. So, we that was something I was thinking about as far as to ask Edwin like how does he value this week zero of college football, but yeah, it's going to be

Troy McDonald Kane: Um,

Cody Haugen: interesting.

Troy McDonald Kane: okay. Um, Brett, did we want to put more time on tomorrow with Edwin to go through any more of this or do you want to take a couple days to work through it and maybe we do Thursday instead or what's your thought?

George Westbrook: Couple of days

Troy McDonald Kane: Yeah. So, why don't we do Thursday? We can do that same time slot that works um the the 3 to 4

George Westbrook: be

Troy McDonald Kane: London time,

Cody Haugen: All right, since it seems like we're tableabling this, George, I'm going to ask you my favorite question of the last few days.

  
  

### 00:57:34

  

Troy McDonald Kane: right?

Cody Haugen: Did we figure out the futures for Edwin? Since he's all other stuff,

George Westbrook: I sent the sent I sent a

Cody Haugen: let's make him happy and get him the futures today if we can.

George Westbrook: response back to sports radar um bas Yeah.

Cody Haugen: Oh, you did? Okay.

George Westbrook: Yeah. Cuz I think I sent uh I tested it tested it tested it and it was just it nothing was nothing was coming up like the end points were being hit. it was returning things, but it was not returning the probabilities.

Cody Haugen: Yeah.

George Westbrook: I sent them a long email, all the end points, what we were getting, what we weren't getting. Um, and they've just said, "Uh, okay, we'll look into it. We'll get back to you."

Cody Haugen: Okay. So, yeah, keep me if you could keep me copied on those. Not that I again I don't need to play middleman,

George Westbrook: Yeah, I swear I did.

Cody Haugen: but then at least I can give them a kick in the ass.

  
  

### 00:58:23

  

Cody Haugen: So you don't have to worry about following up on that.

George Westbrook: Yeah.

Cody Haugen: Like you be the fact guy, I'll be the chaser guy. Um and make sure I'll chase him down. As long as you provide the facts, then I can be like, "Well, what the f***? It's been two days or whatever." Because

George Westbrook: Uh, let me have a look cuz I swear.

Cody Haugen: once again, I can call David or Scott in two seconds and be like, "Boys,

George Westbrook: Yeah.

Cody Haugen: what's going on?

George Westbrook: Oh, yeah. I'll forward you this email. For some reason, I did. I know what I've done. I've clicked reply instead of reply all.

Cody Haugen: Uh, no worries.

George Westbrook: Go.

Cody Haugen: Because yeah, I didn't know if you even replied. I just saw that they said they were looking into something. I was like, well, George must have replied, but okay, cool. Yeah, because it's still giving us a 403. Like, we're not authorized.

George Westbrook: Yeah,

Cody Haugen: We are.

  
  

### 00:59:10

  

George Westbrook: it's it's I think some of them some of them what was it it said here? It it's basically it allows for most of them but not the one that we want. And then it was like sometime you might have there might be certain book makers that aren't allowed or are allowed. Um, and I think it's even the NFL ones. Only eight eight probabilities uh or eight win totals are coming through out of the 32. Um, so it's yeah, I'm not I'm not too sure why. Um, I mean, I was doing it. Claude was having a good old look through and it was like, yeah, this is just it's just not not

Cody Haugen: Yeah,

George Westbrook: there.

Cody Haugen: because they I mean they are it's it's it's interesting but they are at the sport radar is at the uh the the the standard of the sports books, right? like the the web hooks are tied to the sports books. Yes, sport radar is selling the the raw data to the sports books. The sports books put that into their algorithms, spit out futures, come back to Sport Radar, and that's how the circle of what they call the life cycle of odds is built.

  
  

### 01:00:13

  

Cody Haugen: Um, so yeah, they are at the, you know, mercy of of what the sports books are actually sending back in. Um, but yeah,

George Westbrook: H

Cody Haugen: you would think that there's futures out there because I mean I think I can FanDuel right now and bet

George Westbrook: I think I think there's two the the probabilities API as well.

Cody Haugen: them.

George Westbrook: I think we're on a trial for that and I think we've I think we've used 45% of the quotota on that and then in testing

Cody Haugen: Yeah, that that uh don't worry about.

George Westbrook: you

Cody Haugen: I'll get us more calls. That's fine. Um, I'm just trying to see if FanDuel has them, if there are futures right now for NCA football. Uh, view all. No, see, right now in FanDuel, all they have is uh who's going to win the Heisman. So,

George Westbrook: That's Yeah,

Cody Haugen: maybe maybe So,

George Westbrook: that's that was one of the ones that came up as well.

Cody Haugen: you you did see that? Yeah.

  
  

### 01:01:12

  

Cody Haugen: I have Yep. National Championship.

George Westbrook: Yeah.

Cody Haugen: You can pick that. College football. Oh, no, no, no, no, no. Sorry. I got it right here. Win totals. So, it is it is there. Okay. Uh in FanDuel and Sport Radar powers FanDuel. So, it's something that we're just not seeing or something. So, I'll I'll chase it up right after this call.

George Westbrook: Okay, perfect. Um, I think apart from that, there was the a few of those iterations that we mentioned last week been added in. Off the top of my head, I can't really remember what they are in all honesty. Um, the only one most notable one is on the watch page, the scrolly part on the right hand side with the ad units in between and then the ad unit to the left hand side as well. But I think the rather than me just I'll just show it quickly. Um, but I think we need to think how the the UX is going to work on there.

  
  

### 01:02:10

  

George Westbrook: Uh, So like this this ad unit here. I mean I just squish one in.

Cody Haugen: Yep.

George Westbrook: Um but I suppose it's just to show the positions that they can be not having the the scrubber. And then this is quite nice cuz that's obviously when a user is holding their phone. Um there's going to be one finger each side of the screen. So closest right hand the trade one. This is this has changed now. So you can scroll through. Um and then

Cody Haugen: Just as long as the first two on the default of the scroll. It's not alphabetical. It's the teams that are playing.

George Westbrook: yeah,

Cody Haugen: Yeah.

George Westbrook: so how we've how we've got it. I think this is one of the things I So the order in which this is going to be and it should be like this on other pages as well is you you click on it. The first two are going to be the team the two teams that are playing and then

  
  

### 01:03:11

  

Cody Haugen: Okay,

George Westbrook: after that it's going to be your favorite teams.

Cody Haugen: great.

George Westbrook: It didn't do that part but so yeah I think it's because I haven't got any favorite teams.

Cody Haugen: Love that.

George Westbrook: So it's always going to be first two that are playing then your favorite teams then alphabetical. One of the things we do want to think is No, I've got I got it. So, it be first two favorites, is this team that's playing NFL? If it is, then let's put the NFL teams to swipe across and then let's go to the NCAA. If it's an NCAA game, NCAA after the favorites. But I think in all honesty, after the favorites and the teams playing, people are just going to search cuz I know I would I couldn't be asked to scroll through 130

Cody Haugen: I 100 100% agree.

George Westbrook: teams.

Cody Haugen: I'm not doing that. I'm I'm giving it maybe four to five swipes before I get like, where the f*** is this? All right, I'm just gonna type it in.

  
  

### 01:04:02

  

George Westbrook: Yeah.

Cody Haugen: No, I agree.

George Westbrook: Um that

Cody Haugen: Uh the other the other thing that uh I don't think Jared's on this call. Um, but uh that he has brought up in other feedback is watch lists. And I guess from a a trade I mean Troy, you can maybe explain this better than me,

George Westbrook: Yeah.

Cody Haugen: but it's not quite your favorites list. It's just a separate watch list. Like you might have your favorite teams, but then you might also have like, you know, a s*** team might be on your watch list because you're shorting them.

George Westbrook: Yeah.

Cody Haugen: I don't Am I explaining that? What's the difference between a favorite and a watch list again, Troy? Like I get it from a high level, but I don't understand why you have

Troy McDonald Kane: I think it's more semantics to be honest with you KO on this because a watch

Cody Haugen: Okay.

George Westbrook: I

Troy McDonald Kane: list is just whatever you want to watch.

Cody Haugen: Okay.

George Westbrook: I

  
  

### 01:04:50

  

Troy McDonald Kane: Like when you do when you go to a stock app you have a watch list. Everywhere else it's a favorites list. It's literally the in my opinion it's the same thing. I don't know.

George Westbrook: I think there I think they could be slightly

Cody Haugen: Okay.

Troy McDonald Kane: I actually don't know what difference this would be personally except you could have multiple watch lists I think is the

George Westbrook: different.

Troy McDonald Kane: differentiator. So you could have like a Big 10 watch list. You could have you know or you could have you know power conference watch lists if you want to watch who's playing you know at one. I I mean I think it's it's just where you classify it. I think that the difference actually Cody is maybe the difference is you only have one favorites list but you can have multiple watch you can create multiple watch

Cody Haugen: Got

George Westbrook: I I think potentially with because I suppose it's on like a sports app

  
  

### 01:05:30

  

Cody Haugen: it.

Troy McDonald Kane: list

George Westbrook: you're never going to like there's nothing exist before where you can trade and then also al also on maybe trading apps you're not really going to have anything to do with sports maybe I don't know maybe that was a bad statement but I'm thinking favorites is here's the teams that I want to get information about Oh, let me get this. So Like on the on the discover page, you'd have your teams that you want information about. So this would be a bit more personalized. And then on the trade page, you might have a watch list of teams that you don't really give a s*** about the news about them. But then I suppose you probably would actually if you're trading them. So they are kind of on the

Cody Haugen: Yeah, I would

Troy McDonald Kane: I mean, typically like there there's another reason why people use watch list and that's their o anything they have a position

George Westbrook: same

Cody Haugen: say

Troy McDonald Kane: on. So then they can see what teams they have a position on assuming they hold positions long term.

  
  

### 01:06:30

  

Troy McDonald Kane: And so you know you can leverage watch list for that too. But again, it's it's really more of the trainability of what people are used to versus, you know, some people are used to just having a favorites list. Some people have a watch list. I think watch watch list is a more trading term where everywhere else favorites

George Westbrook: Yeah.

Troy McDonald Kane: kind of thing because like all my sports app is just favorites,

George Westbrook: Okay.

Troy McDonald Kane: but then if you go to a stock app,

George Westbrook: Yeah.

Troy McDonald Kane: it's watch lists. So,

George Westbrook: I think what one of the other things and then we got to think what we want to add here. Obviously there's no open position so this doesn't really or no P&L but is now this is like scrollable so we can add multiple things along here obviously interlace ads in between them um so that there's

Cody Haugen: See, I think I Yeah, I think that does function really easily and quick because you can just swipe up and down.

  
  

### 01:07:14

  

George Westbrook: more

Cody Haugen: I did know Edwin on the last call said he did not want that, but um I I don't know. Let's show it to him. I mean, I think I think it's I think it's fast enough that you're

Troy McDonald Kane: I I agree.

Cody Haugen: you're

Troy McDonald Kane: I agree, Cody. I think it if you have it gives you more positions to put stuff

Cody Haugen: Well,

Troy McDonald Kane: there.

Cody Haugen: that and and I don't think it's overwhelming either.

George Westbrook: Yeah.

Cody Haugen: It's just your thumb is right there on that side of the screen and you just swipe up and

Troy McDonald Kane: It's not.

George Westbrook: Yeah.

Troy McDonald Kane: And now we had a we have a couple interns starting.

George Westbrook: Both can

Cody Haugen: down.

Troy McDonald Kane: They're going to start doing app reviews and they're they're going to the target demographic.

George Westbrook: Okay.

Troy McDonald Kane: So, it'll be good for their feedback to start funneling in this

George Westbrook: Yeah. Yeah, because I think in terms of obviously one ad placement,

  
  

### 01:07:56

  

Troy McDonald Kane: week.

George Westbrook: I think if it was just just those two graphs there, there's literally zero space to put ads between them. You can't really put any ads here um on this side um because it's it's so then it just leaves maybe one ad unit.

Cody Haugen: right?

George Westbrook: Whereas obviously with this, let's say there's six different graphs, there could be six six to eight different ads in there as well. And I think the thing we have got to work out is obviously here there's space for ads here. maybe along the bottom as well. Um,

Cody Haugen: Yeah. And I mean I think this is a position or something like you know win probability presented to uh

Brett StClair: This is

George Westbrook: but

Cody Haugen: presented by you know so and so if you're actually in the you know

Brett StClair: what

George Westbrook: yeah.

Cody Haugen: clicking into that graph and and that type of thing.

George Westbrook: Yeah.

Cody Haugen: But um I mean once again George it looks f****** sweet. I mean I I I I we're we're definitely not taking steps backwards.

  
  

### 01:08:52

  

Cody Haugen: this thing. Every time you show it, it just looks this much better.

Troy McDonald Kane: Yeah, it's just getting better and better.

Cody Haugen: Like every time I think it can't get better because of what we've already created, like it gets better. So, no, I think it's all positive ads and how it looks and flows. It's It's great,

Brett StClair: George, just on the tower banners.

Cody Haugen: man.

Brett StClair: I don't think those are custom or IB.

George Westbrook: the they are.

Brett StClair: They are.

George Westbrook: Yeah.

Brett StClair: That'll fit that width.

George Westbrook: So with the with

Brett StClair: There might be tower that are for desktop,

George Westbrook: the I think

Brett StClair: but I can't imagine their tower for mobile.

George Westbrook: with I need to double double double check but with so IAB used to be exact pixel sizes. So it used to be like 396 by 36 and it had to be that pixel size whereas I think they changed it a few years ago. Now it's aspect ratio so that you can show an ad unit um and you can scale it you can scale it up and down as long as the proportions remain exactly the same.

  
  

### 01:09:56

  

Brett StClair: must be up to a point, right? Because you could end up scaling it into a non-usable ad unit,

George Westbrook: Yeah.

Brett StClair: right?

George Westbrook: Yeah.

Brett StClair: Well, we'll we'll test it with real ad units

George Westbrook: Yeah.

Brett StClair: soon.

George Westbrook: Um cuz I think in terms of the the trading like watch stuff like that is we need to nail the the back end trading stuff once tZERO have got everything over to us and then and then the trade pages that's where that's where we'll start iterating on that because obviously we we did the first hit where we didn't really know anything. Um now it's let's get what's actually going to be there um on a different version which people can get their hands on.

Troy McDonald Kane: All

George Westbrook: But I think apart from that, I can't I can't think of can't think of anything

Brett StClair: I think it's just the focus this week, right?

George Westbrook: else.

Brett StClair: Focus trade focus notifications,

Troy McDonald Kane: right.

Brett StClair: different types of notifications that'll be pushed, system notifications, uh personalized notification and campaignbased notification and how we're going to run and push that.

  
  

### 01:11:05

  

Brett StClair: Um the market maker I just

Troy McDonald Kane: and getting to approve our app would be phenomenal this

Brett StClair: there'll be an inter what? Oh yeah approval. Yeah.

George Westbrook: Yeah.

Troy McDonald Kane: week.

George Westbrook: Yeah.

Brett StClair: Get that through. Um and ads and getting at least one of the SSPs up and running. Um I think the the perfect one I think we'll definitely get ADM Mob going and then the next focus is get apploving going on it. We'll load ADM Mob into Apploving. So Apploving is actually more of a ad server in the space.

Cody Haugen: Amazing.

Brett StClair: Um and then you can load different SSPs into that and it has its own SSP. It's quite nice. It's pretty cool. Um yeah, I think that's that's the focus, right? It's just on the market maker. Are we going to have a different interface? Are we going to run that interface off the admin side? We're going to have some face like I'm assuming dashboard, how it's performing,

  
  

### 01:12:07

  

George Westbrook: Interface.

Brett StClair: that kind of

Troy McDonald Kane: Yeah, we're going to have to create um a UI for the market maker that we can set

Brett StClair: stuff.

Troy McDonald Kane: parameters, modify, modern, moderate orders, stuff like that, which Kevin might be running. So, yeah. Um,

George Westbrook: I think that might be another little mini

Brett StClair: We got a giveaway.

Troy McDonald Kane: yeah, that's going to have to be that.

George Westbrook: workshop.

Troy McDonald Kane: But that one I'm less worried about because that and that should always come at the end anyway when you have all the the backend stuff done and then you can create this. I mean, it's actually gonna actually when I I take it back, it's it's all we really need is a desktop app version of the app, which I assume we're going to have, right?

George Westbrook: of the of of this app.

Troy McDonald Kane: Yeah. Of the Gallenge app because that's he just think of the market maker as any other participant in the trading challenge.

George Westbrook: Um,

Troy McDonald Kane: It just has far more capabilities because it's going to have unlimited buying power and it's going to have the ability to quote two-sided markets.

  
  

### 01:13:15

  

Troy McDonald Kane: But we could the UI doesn't have to change any more than what we're already building for everybody else. We just have to add a couple new components in there to monitor what we're

George Westbrook: but is the the market maker is that mainly just for monitoring and updates?

Troy McDonald Kane: doing.

George Westbrook: It's two parameters every once in a while.

Brett StClair: Yeah, because we've got the admin dashboard and I can see it being used more as a desktop version.

George Westbrook: Oh,

Brett StClair: The admin dashboard is built for desktop and we don't quite have a desktop version yet. we've we haven't started anything on the desktop version of it. Um,

Troy McDonald Kane: So,

Brett StClair: so you've got

Troy McDonald Kane: this it might be a good idea to we we'll we'll create the desktop version for the market maker first. We may not even have to roll it out to other participants right away, but we can we can use the desktop version to be for the market maker operations.

Brett StClair: It's going to be seriously rough though.

  
  

### 01:14:12

  

Brett StClair: Um, just to let you guys know,

Troy McDonald Kane: Yeah. All right. So, he's

Brett StClair: the

Troy McDonald Kane: good.

George Westbrook: So does this.

Troy McDonald Kane: Yeah. And again, we can refine it as we go through the trading challenge. It's I think basic functionality is we need to be able to set parameters of the algos and have order lookup and know what our positions in P&L are. And a lot of the same functions that you have in the app. It's just building it into a desktop version and giving us more

George Westbrook: Okay.

Troy McDonald Kane: control.

George Westbrook: Okay.

Brett StClair: I'm excited.

George Westbrook: I think

Brett StClair: Happy days.

George Westbrook: that's

Brett StClair: We don't uh George will definitely be loading this session in soon for the market maker, Right. There's so much

George Westbrook: Yeah. Think I need to buy I think I buy need to buy more nicotine

Brett StClair: in

George Westbrook: pouches.

Troy McDonald Kane: or find another vice.

George Westbrook: Yeah.

Cody Haugen: No, buddy.

Brett StClair: is a

Cody Haugen: Stick with the keeps us it keeps us operating at maximum

Brett StClair: zombie.

Cody Haugen: capacity.

George Westbrook: Yeah.

Cody Haugen: All right. Well,

George Westbrook: Right.

Troy McDonald Kane: All

Brett StClair: That's it.

George Westbrook: Who's Who's going to say it?

Cody Haugen: let's let's f******

Troy McDonald Kane: right.

George Westbrook: Who's going to say it?

Cody Haugen: go, baby. It's been too long.

Troy McDonald Kane: All right.

George Westbrook: Speak to you soon.

Kevin Murray: All right,

George Westbrook: Have a good one.

Kevin Murray: have a good one, guys. Take it easy.

Troy McDonald Kane: Right.

Brett StClair: Yes.

Troy McDonald Kane: Yep.

Brett StClair: Touch out.

  
  

### Transcription ended after 01:15:39

  

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.

**