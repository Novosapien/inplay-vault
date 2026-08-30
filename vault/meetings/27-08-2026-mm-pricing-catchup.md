---
date: 2026-08-27
type: call
status: extracted
extracted-to: "[[market-maker/sessions/2026-08-27-edwin-pricing-call]]"
description: "Transcript of the 27-08 pricing catch-up with Edwin: the LSU worked example, the win-premium mechanic, point-spread probabilities, off-field popularity, and market data as a product"
---

**

Aug 27, 2026

## Meeting Aug 27, 2026 at 15:07 BST - Transcript

### 00:00:01

  

George Westbrook: There we

edwin: is now taking. Cool.

George Westbrook: go.

edwin: Um, okay. So, the pricing of these teams, number one, also right now on the uh team companies for the NCAA, it's back to showing that there's a million shares available for each team.

George Westbrook: Okay, that's that's not the case in that it's that would just be like

Kevin Murray: That's

George Westbrook: UI saying that it's not actually

edwin: Okay. Cool. Cool.

Kevin Murray: Can I just jump in quickly?

George Westbrook: that

Kevin Murray: Troy did send an email to Rob yesterday saying it was a million shares.

edwin: Please.

Kevin Murray: Each team company for the NCA should be a million shares float uh outstanding and allowed up to a million shares to be shorted.

edwin: Thanks, Kevin.

George Westbrook: Yeah. Yeah.

edwin: But there was a there was some that you know like we bought a bunch and others bought a bunch over the weekend. They shouldn't it shouldn't have recycled any buys or sell you know buys into the IPO

George Westbrook: No, it should it should be like now it should be that all of those orders all the sell orders for the

  
  

### 00:01:04

  

edwin: already.

George Westbrook: for are all gone. Um, so any share just goes back to inventory and then that's what the maker's using to to quote

edwin: But I'm saying like right now if you go on to our app it shows like LSU has a million shares available. It should only show like 480,000 or 58 whatever that number

George Westbrook: I'll just message this

edwin: is

George Westbrook: out. Is this on the on the team page on the company's tab?

edwin: when you hit trade. Um Yep.

George Westbrook: Yeah.

edwin: and takes you to that IPO lot for NCAA.

George Westbrook: Okay. The IPO that should be gone. The IPO thing.

edwin: Well, oh yeah, those should be gone now,

George Westbrook: Yeah. Yeah. We Yeah, we'll we should be updated,

edwin: right?

George Westbrook: but we'll obviously it's not. So, we'll we'll we'll double check that. But the makers the makers running in the background um is is putting the quotes out. So,

edwin: Right. Okay, cool. All right. So, let's talk about this um this

  
  

### 00:02:21

  

George Westbrook: I

edwin: pricing.

George Westbrook: mean,

edwin: And we're going to talk about uh LSU to start because right now LSU's price uh for IPO went off at $59 or 59.53. Okay. Um and the the expected wins for that

George Westbrook: looks like

edwin: um team were exactly I think they were like 8.55 or

George Westbrook: Listen.

edwin: something. They were Yeah, 8.55 is their expected wins. So when we did the valuation, you know, we said, okay, well, 8.55 times $5, that's the onfield expected revenue, which is going to bring you to, you know, $42.75 is the baked into the price of the IPO. Okay, so we agree on that. Okay,

George Westbrook: Yeah.

edwin: cool. And then the balance is going to be the marketing portion, which is how much they make on the the the split between the 250. So, um, when LSU wins a game, okay, if if we're factoring in that each game that they are going to get revenue for is five bucks and they're only expected to win 8.55, obviously they're either going to win eight or nine or some other number.

  
  

### 00:03:59

  

edwin: It's never going to be like 0.55, but that's how the pricing works. So, um, a win to LSU is not going to be worth $5 more a share because part of that is already baked into the price, right?

George Westbrook: Yeah.

edwin: And so, you know, if if we were to take that the average win, um was, you know, whatever whatever the math is on it, um you know, $5 and you know, they they let's say hypothetically they win nine games, okay? And uh that would be 45. So over the course of the season,

George Westbrook: Yeah.

edwin: their earnings from winnings is only $2.25 more, right? Um, so if they lose a game, it has a massive impact on their price because a lot of the games that they play, they're favored by a lot. You know, maybe they'll be favored by 20 points. So how they win is some factor but the actual price of the

George Westbrook: s***.

edwin: share um itself should oscillate you know around if they're winning you know somewhere between you know uh you know 47 cents and maybe $1.50 for that win and then whatever the expectation is on the off field.

  
  

### 00:05:24

  

edwin: So, a a win may not move this share $5. It may only move it, you know, 90s or, you know, 50 cents,

George Westbrook: Yeah.

edwin: right? So, um I'm building you a formula that you can use um and you can take a look at it today that will hopefully clear up like how we can basically make the market around our fair value. And our fair fair fair value is the you know the price of the share for the season versus expected um wins and losses throughout the game. So like you know fell as you goes down 21 points to a team that they're favored to win on, you know, that they're going to lose a lot of value on that particular share for that period of time. Now, if they come back and win, you know, that's that's the exciting part is when there's this, you know, this price oscillation and, you know, who knows what can happen type thing.

George Westbrook: cuz I I think there's one thing that you said earlier which I can see how we can factor it or it would be factored in but then there's limitations um given what we got at the moment.

  
  

### 00:06:31

  

George Westbrook: So the the example you gave that if a team wins 70 nil so their price should increase more than just the so let's say they're an underdog um they were almost guaranteed

edwin: Yeah.

George Westbrook: to lose so then they've got zero of that $5 allocated to them just as with assumptions then they win 70 nil that they should get more than the $5 because that win is so big it's going to have implications

edwin: I found this b****.

George Westbrook: on the win probabilities for future games as well. So in a perfect world, what would happen is as soon as they win that game,

edwin: breath.

George Westbrook: Sports Radar updates the expected wins per season, which factors in the future probabilities because at the m there's different ideals. There's different ideals. One ideal is that they win 70 nil. That drastically changes the expected wins per season,

edwin: I think

George Westbrook: which drastically changes the price of that share. Second idea would be we have a win probability for each game um going out into the future and then they all independently change.

  
  

### 00:07:32

  

George Westbrook: Um both kind of have the same effect but what we what we don't know at the moment is how often is that expected wins going to change.

edwin: Yeah.

George Westbrook: Um so like if if if after a game it might be that let's say the

edwin: So,

George Westbrook: expected wins was eight win probability before the game was 0.5 but we obviously assume that that 0.5 for that the game that's just coming up is incorporated into that eight expected wins. Then obviously we work out the delta. Let's say it goes to 0.6. So then we just add um add that 0.1 * 5 onto the 8 * 5 to get the new price in game. Um but after um what what we can do is take the delta at the end of the game and kind of save it to that old expected wins. Um but then obviously in my head it will make sense that if they win that game and they win it by a certain margin against a certain team that should have an impact on their expected wins

  
  

### 00:08:31

  

edwin: that

George Westbrook: as well. So like let's say their next game was against a team that lost drastically and their win probability before the game was 0.5 of this up upcoming game. Now that should increase and the others decrease. Um,

edwin: speaking back.

George Westbrook: but we don't know that probability until just before the game. So up until the first the the 15 minutes before the game, there's not going to be that big implication on the price, which could mean

edwin: There there will be George, let me let me interrupt real quick because we can extrapolate what the point spreads are,

George Westbrook: that.

edwin: the like um you know they're going to win by 18 points or they're going to win by two. we can extrapolate those into a fair value um win percentage without getting the absolute win percentage.

George Westbrook: Okay.

edwin: So you know what I want to do is I want to try to I want to get our own data for this not reliant on sport radar. So you know a lot has to do with how many games are left too.

  
  

### 00:09:37

  

edwin: So it's like there's a decay like in the beginning of the season right then they win and they've got 11

George Westbrook: Yeah.

edwin: games left. That's different if they win at the end of the season. They got one game left, right? So, it doesn't have as much of an impact on future value because there's only one possible game. So, um,

George Westbrook: Yeah.

edwin: okay, let me, um, let me work on a few things this morning, uh, to to help us get to where we want to be on this because the data, you know,

George Westbrook: Mhm.

edwin: co Cody's going to want to resell this data, uh, you know, and we want to have our we I don't want to be reliant on any third party provider, uh, for some of the guts of what we're doing. we can use it as a reference point because like after after they play a game on Saturday and all the games are done, the point spreads come out like Sunday for the next week. So the win probability you can always back into

George Westbrook: Yeah.

edwin: them.

  
  

### 00:10:37

  

edwin: Cody, do you have any thoughts?

Cody Haugen: Um the larger thought not I guess more or less on the technical details of what you guys are talking about. Um the larger thought George is to to what Edwin said about us selling this data. um we need a way and and I know the data is starting to live somewhere but we're going to need it in a workable format that I mean secondary trading you know is obviously started that's our first proprietary market data set that we own um so we need a yeah we need a place to obviously start storing that and then a place that we can start working with that um and and start to combine it with the sports side of things with the finance side of things. So then we can start to Edwin's point creating our own projections,

George Westbrook: It's

Cody Haugen: our own probabilities and with the speed of the data of our market data. And I've said this before, but to reiterate it, we should be the fastest projection probability data in the world. And that's and that's not that's not a zero- sum game.

  
  

### 00:11:46

  

Cody Haugen: That's a lot of people would love that data because at to Edwin's point, you can back into a lot of things if you have that data. um can convert it to a lot of different things. and other industries like odds and spreads. Um, so it's it's it's a very cool uh hypothetical um at this point, but it's just a larger thought. We need access to our data and how you guys want to deliver that or structure that. We just need to figure out a way that we start this database and this this

George Westbrook: Yeah.

edwin: Yeah,

Cody Haugen: out

edwin: I mean we just want to be engineered so that you know we can access it and then any people who subscribe for any of our like um you know strategy builders they can subscribe you know when they pull the data it's available. So give that a think. I know that um you're getting a lot here at the end right before we get cooking,

George Westbrook: Yes.

edwin: but um the the key is the pricing. The pricing always has to be today's game uh the value of today's game relative to what's already banked or considered to be expected value and then what the forward-looking u potential is for the off-field and the onfield.

  
  

### 00:12:59

  

edwin: I mean, and and that that's what makes the market fun to trade because it's it's going to be volatile and there's

George Westbrook: What?

edwin: the edge itself is still um not very mature. So, like you know, you know, when you like if you're trading on say a traditional market like the 10-year note, that thing's been priced and sliced and diced by every f****** quant in the world. They know what fair value is on that 10-year note. So they know like if if you are working an edge there, let's say you're trying to buy it on the bid and you get filled and let's say you got filled uh you're at the end of the queue, meaning a whole bunch of people got filled before you and then finally you get filled. You know, the reality is you probably don't want them, you know, because someone's giving up an edge in a very mature seasoned market that nobody everyone works for that half-tick edge. That's how they make their living. So, if they're giving you the edge, you're going to get f*****. Um, and our product because it's so new, there is none of that which makes it for a very exciting and dynamic trading experience for the user because an edge that they get if they're working the bid and they want to get long for whatever reason.

  
  

### 00:14:19

  

edwin: It's not just the mechanics that that get them filled. It's, you know, no one's saying like, hey, if you get on the build, uh, the I'm sorry, if you get filled on the bid, that your trade's automatically bad because the bid ask is like there's no real defined pricing model to this yet that the market has narrowed in on and and really tightened up the bid ass spread. But that's we would call this a loose market, a fun market and one that has a lot of opportunity for anyone to make money in, not just like the high frequency traders and the professionals.

George Westbrook: Yeah.

Cody Haugen: Could I ask a question? Maybe just uh informational. Do you ever see it becoming a tight market just based on how the sport season to season so many different variables happen from week to week? It ever becoming like I don't think it could ever become that example that you gave of the 10-year note because there's way too many variables in and out from moving game to game

George Westbrook: All

edwin: Well, I would say I would say that there's far more v variables in the 10-year note.

  
  

### 00:15:19

  

Cody Haugen: lit.

edwin: Um,

Cody Haugen: Okay.

edwin: because you got a lot of different countries, you got war,

Cody Haugen: Oh, sure.

edwin: famine, f******

George Westbrook: right.

edwin: weather,

Cody Haugen: Yeah.

edwin: all those things happen and they can affect the the value of these these bonds. Um, but I do think it gets tighter as the season gets closer to

Cody Haugen: Sure. Yeah.

George Westbrook: s***.

Cody Haugen: Yeah. But like trying to build on a model of where the Bengals are projected and

edwin: ending.

Cody Haugen: finished this year versus when they IPO next year and where they can potentially finish. Like that's never going to be a

edwin: No, that's not going to be a thing. I I don't see that as multi-year like,

Cody Haugen: thing.

edwin: you know, build value. I'm investing in this team. they're going to carry me for the next four years. What I wanted and what I've designed is a reset. And to me, to me, because a reset makes sense. I mean, that the reset brings a lot more opinion.

Cody Haugen: Right.

  
  

### 00:16:17

  

edwin: And opinion means, you know, order flow and and, you know, people giving up edge to trade and like what what difference does it make if you want to get long and you got to cross a 10-cent edge, but you can get 50 cents out of the trade. People will pay the 10 cents if it makes sense to them. If if they if they know they're going to make 50,

Cody Haugen: Yeah.

edwin: they'll pay the 10 to make 50.

Cody Haugen: Every day

edwin: So,

Troy McDonald Kane: So Edwin, I have a quick question in the on the off game times.

edwin: um

Troy McDonald Kane: So when we're out of gameplay like today or you know, let's say we just played first week of games,

George Westbrook: What's

Troy McDonald Kane: we're in in between weeks and investors come in or participants come in and they say,

edwin: Yeah.

George Westbrook: that?

Troy McDonald Kane: you know, I want to I want to jump the price by $5 because I want to go, you know, to the ceiling of what they're going to capture the next week. How does the market maker algo adjust for that?

  
  

### 00:17:11

  

edwin: But see, Troy, I don't think they're like, if someone says,"Oh, they're going to make five bucks next week." That part of that five bucks is already priced into the IPO price. So, I don't think that comes into play unless they're like, you know, playing and they think an underdog's going to win and they're going to they're going to buy it,

Troy McDonald Kane: Well, yeah. Yeah, you we all understand that. I'm just saying like I'm just entering the competition today.

edwin: right?

Troy McDonald Kane: I had no idea how the IPOs worked. I have no idea what the valuation is today. I just know that they're playing for $5 of value that week plus off-field revenue. I I'm just trying to play like some edge cases of like how the algo would account if someone tries to drive the market up

George Westbrook: God.

Troy McDonald Kane: or down by a whole five dollars because they don't realize that it's partially priced into the price

George Westbrook: Ready?

Troy McDonald Kane: already.

edwin: Um,

George Westbrook: I think it would just it would just pull it just pull it back down because I think in the in the main

  
  

### 00:18:00

  

edwin: thank you.

George Westbrook: alos in the the maker it's all based all around that fair value and there's there's not much based on or I think anything on the what's actually happening in the market to for me and correct me if I'm wrong on anything on this Edwin but it always feels like let's say they're trying to push it that way the maker's always going to pull it back down um or the order's just not going to get filled

edwin: Well, um it's like traditional markets like if someone comes in, they puke a position, drives the market, you know, 10 ticks one way, um you know, the market's going to trade back to fair value. I mean the one order or one participant number one these guys are not going to have enough buying power to drive it that much at a h 100,000 to start you know maybe in 10 weeks they will they got a couple million maybe but um you know ultimately the market's going to correct itself I mean the market determines the prices if someone drives that price up five

George Westbrook: Facebook.

edwin: bucks I mean smart guys are going to sell the living s*** out of it and they're going to make money as a

  
  

### 00:19:10

  

Troy McDonald Kane: Yeah, I think it just goes back to what we were talking about yesterday with the with the financial report or the analyst reports.

edwin: So

Troy McDonald Kane: I think pricing stuff and earnings per share showing that it is partially baked into the share price based on the forward-looking statements.

George Westbrook: Where is it?

Troy McDonald Kane: Uh so that people understand like how to price that information into the security in between

edwin: yeah, I mean like on the on the LSU stuff.

Troy McDonald Kane: games.

edwin: Okay. Um, in the beginning of the season, the way that I've got the model, like if they make if they win the first couple of weeks, the share price for onfield only goes up like 47 cents a win cuz they're playing dog s***

George Westbrook: Thank you.

edwin: teams. So, they're they're they're heavily favored. you know, they don't make $5 extra per share because they beat like Jacksonville State who they're a 40point favorite on. Um, you know, they're going to make a little bit of of money because no, it's not a guarantee that they win every single game, right?

  
  

### 00:20:19

  

edwin: like I mean something can happen but um you know so the the actual you know move of the the of these games that they're expected to win is going to be less than way less than $5. Now, what's interesting is if they lose a game or two, that could be catastrophic to their price, right? So, like, you know, god forbid they lost to Jacksonville State, you know, on in the first game of the season, it's very very likely that that share could go down 10 or $15. Uh, sure.

George Westbrook: One one thing as well is the which I wouldn't say I'm clear on is it. So there's the actual off offfield earnings and then the expected off-field earnings. So the actual I can understand it's trading volume but what the expected how's that how's that worked

edwin: Yeah. So,

George Westbrook: out?

edwin: I built a thing for all the different teams in terms of popularity. Uh that was like socials, that was, you know, prime time games, you know, like for example, Dallas Cowboys. uh they were uh in the NFL they're expected to to you know earn like 30 bucks a a a share for offfield.

  
  

### 00:21:36

  

edwin: Okay. And um like Carolina is only supposed to, you know, earn like 12 bucks or 14 bucks or something. I can send you a copy of that um as well. So depending upon how popular the teams are um you know what market they're in.

George Westbrook: Yeah.

edwin: So like obviously New York Jets or New York Giants, they've got huge following in New York. We expect that a lot of people in New York will trade those teams. Um so even if they stink uh and they they lose every game, you know, hypothetically, they still could make a lion share of all the trading revenue uh you know, marketing trading revenue.

George Westbrook: Okay, that makes

edwin: Yeah.

George Westbrook: sense.

edwin: And so like and then you know the other thing that's interesting if you're a traitor of the product is let's say there's a team that sucks. Okay. Um but they drafted a quarterback this season who's going to you know he's on second string right now. The starter goes out. The the college star starts playing and he's amazing but the team sucks and they lose.

  
  

### 00:22:41

  

George Westbrook: It's

edwin: They have a terrible defense but the the the quarterback is starting to play really really well.

George Westbrook: right.

edwin: they score a ton of points and then a lot of fans start watching and trading that team as a result of a single player coming in. You could see a phenomenon where there'll be a lot of bid and a lot more um interest in that uh player and team, let's say Carolina perhaps, and all of a sudden they've got this like Michael Jordanesque football player on their team. Even though they lose, they still have a lot of people watching and trading it. it becomes very, you know, valuable for the off off-field stuff because most people trade that team no matter who they play. So there's there there's that dynamic as well. So I I think like a lot of people have asked me like,"Oh, are you going to do individual players?" And I've worked them through a couple examples where the individual player um can have a a strong impact without having to securitize that individual player.

George Westbrook: Okay. Okay, that will make sense.

  
  

### 00:23:45

  

George Westbrook: I hate to I've got to go to a dentist appointment. I got to cycle over there. Um,

edwin: f***.

George Westbrook: so yeah, it's f******

edwin: I don't feel better.

George Westbrook: annoying.

Troy McDonald Kane: One one quick question,

George Westbrook: What?

Troy McDonald Kane: George, before we jump off. Um. How quickly or what is the process for getting non uh verified users access to buying power to be able to trade.

George Westbrook: I'll check with Hassan, but that should be it shouldn't be too long. Like if if not already happening,

Troy McDonald Kane: Okay.

George Westbrook: if it's not happening already, have you noticed there's been some users that haven't been getting that?

Troy McDonald Kane: Yeah. So, I have a I have my son who I registered who has he still has his buy and sell buttons locked because he hasn't gone through KYC.

George Westbrook: Oh,

Troy McDonald Kane: And then I created a brand new account just to test the process to make sure that the layer was removed this morning.

George Westbrook: okay.

  
  

### 00:24:36

  

Troy McDonald Kane: And that still has the locks on it as

George Westbrook: Okay, that might we might just need to push that.

Troy McDonald Kane: well.

George Westbrook: I'll I'll literally speak to Hassan um as soon as I get off this, jump to the dentist, and then Well, well, I'm sure by the time I get back, Hassan, I'll have it sorted. Um, but I just need to speak to him to see see what the lift is on that.

Troy McDonald Kane: Yeah.

George Westbrook: But it's it's not going to be a a Monday thing. It will be like by the end of today or start of

Troy McDonald Kane: Okay.

George Westbrook: tomorrow.

Troy McDonald Kane: Yeah. Ideally before Saturday, I mean,

George Westbrook: Yeah.

Troy McDonald Kane: because we want to start really promoting it on Saturday.

George Westbrook: Yeah.

Troy McDonald Kane: Even though there's only eight games, we still want to give people an opportunity to try it out and submit orders and play around with it during a couple

George Westbrook: Yeah.

Troy McDonald Kane: games.

edwin: Yeah. And um we're still we're we've got our marketing group like starting.

  
  

### 00:25:21

  

edwin: So, you know, we're going to start getting out there and I'm I'm going to be spending uh quite a bit of money on marketing. So, I don't want to like, you know, we we have to have that up. You know, just give you one last thing before you go get that toothpulled.

Cody Haugen: Welcome.

edwin: Um well, we can talk about it later. I hope you're not driving a unicycle.

Troy McDonald Kane: All

edwin: I hope it's got two wheels.

George Westbrook: I I've not got the balance for that.

edwin: That makes sense. I'm sure Brett does. I'm sure Brett can do it and juggle a couple of beers at one time.

George Westbrook: Don't. Right.

edwin: Maybe not.

George Westbrook: So, I've got I've got to jump. I will Yeah,

edwin: All right,

George Westbrook: I'll speak speak to you in a bit.

edwin: we'll see you.

George Westbrook: Have a good one.

Troy McDonald Kane: right.

Kevin Murray: She has me.

Troy McDonald Kane: Thank you.

edwin: Thank you.

George Westbrook: Cheers.

Cody Haugen: See Fresh.

Troy McDonald Kane: All right.

edwin: You guys want to jump on real quick?

Troy McDonald Kane: Oh, they jumped off. They all just jumped off. But yeah, we should jump on real quick.

edwin: Yeah,

Troy McDonald Kane: I can send out a new link.

edwin: I got I got 10 minutes.

Troy McDonald Kane: All right, I'll jump I'll send out a new link.

edwin: Okay, cool. Bye.

Troy McDonald Kane: All right.

  
  

### Transcription ended after 00:26:28

  

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.

**