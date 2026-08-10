---
date: 2026-07-15
type: standup
scope:
  - "[[information-layer/sub-components/single-game-page/single-game-page]]"
  - "[[ipo-module/ipo-module]]"
  - "[[components/components]]"
status: extracted
extracted-to:
  - "[[information-layer/sub-components/single-game-page/single-game-page]]"
  - "[[information-layer/sub-components/single-game-page/changelog]]"
  - "[[ipo-module/ipo-module]]"
  - "[[earnings-report/sub-components/off-field-earnings-engine/off-field-earnings-engine]]"
  - "[[components/components]]"
  - "[[advertising/sub-components/programmatic-media-playbook/programmatic-media-playbook]]"
  - "[[architecture/open-questions]]"
description: "Transcript of the 2026-07-15 InPlay touchdown call — Watch Mode 3D stadium demo, all-138 D1 IPO scope, media-plan calculator, and the Hard Rock fundraise"
---

## Post-Call Analysis

> Wednesday touchdown (66 min). The **Watch Mode demo** stole the call — custom-built 3D stadium (no SR module → owned IP, white-label potential), instant premium-pricing debate ($4.99/mo floated, parked by Edwin: CPM model first). **IPO scope decision** (all ~138 D1 schools; MM warehouses 35–50% of float) and a full walkthrough of **Brett's media-plan forecast calculator**. Apple review came back with a single (wrong) age-verification objection. Commercial context: offering circular filed, Hard Rock/pay.com raise conversations ($30–50M ask), next 5–6 weeks "rough", launch bonus promised.

| Finding | Destination | Action |
|---------|-------------|--------|
| **Watch Mode demoed** — fully custom 3D stadium Gamecast (no SR match-tracker module): owned IP, white-label/resale potential (Cody → Hard Rock); premium debate: $4.99/mo (Cody), 5-min free (Kevin), first-day-free (Troy), free-first (Jared); Troy: premium payers expect no ads; Edwin parked payment — monetize engagement first | [[information-layer/sub-components/single-game-page/single-game-page]] §9 + [[architecture/open-questions]] | New §9 + open-question row |
| **IPO scope confirmed** — ALL ~138 D1 schools (Edwin overruled power-conference cut); MM buys unsold float in ~50k max clips, warehouses 35% (maybe 50%) → resolves unsold-share open item; Aug 22 IPO deadline | [[ipo-module/ipo-module]] | Business rules + edge case updated |
| ⚠️ **Float sizing conflict** — Edwin cited ~1M shares/NCAA team + 875k/NFL team vs documented 5M float | [[ipo-module/ipo-module]] + [[architecture/open-questions]] | Flagged — needs confirmation |
| **Off-field corner cases** — tradable vs non-tradable opponent → 100% of pool to tradable team; bye weeks → no allocation | [[earnings-report/sub-components/off-field-earnings-engine/off-field-earnings-engine]] | Edge cases resolved |
| **Media-plan calculator walkthrough** — page × persona bottom-up (degenerate/starter/returning), 30% fill, $1.47 blended floor, KYC 1.15×/team-follow 1.1× uplifts, 90/5/5 split, CTR-first (complementary advertisers only), 20s→15s rotation testing, agentic bidding every 5 min; audience-mix barbell correction (Cody); SSPs demand live accounts (demo traffic gets cut) | [[advertising/sub-components/programmatic-media-playbook/programmatic-media-playbook]] + [[components/components]] Advertising | New dated section + bullet |
| **Apple review** — single objection (age verification/parental controls), wrong on their side: Persona KYC blocks under-18s; response sent | [[architecture/open-questions]] | Row updated |
| **Fundraise / commercial** — offering circular filed; Hard Rock/pay.com qualifying questions ("how much, what for"); $30–50M ask; individual investors (Rafi, Teddy, Rahm) likely; NBA trading challenge planned late Oct; launch bonus for Novo team; next 5–6 weeks rough | — | Parked — commercial |
| **Engagement-decay debate** — Troy: participation decays when users fall out of prize contention (fantasy-sports analogy); Edwin's counter: last simulation (~600 users) averaged 45+ min engagement incl. non-contenders; comeback-trader leaderboard is the existing mitigation | Post-call analysis | Noted — watch post-launch metrics |

**

Jul 15, 2026

## Inplay - App - Touchdown - Transcript

### 00:00:08

  

Brett StClair: Hello,

Max Kingaby: Good day.

Brett StClair: Troy.

Max Kingaby: Good day.

Brett StClair: I'm guessing the password for your Apple account goes to you. Is that your telephone number? I mean, Troy,

Troy McDonald Kane: I'm sorry.

Brett StClair: did I say George?

Troy McDonald Kane: What?

Brett StClair: The Apple developer account, the two-factor authentications, does that does that go to your telephone number?

Troy McDonald Kane: Yeah, I think I sent it to Hassan this morning when I got the text or see not I can send it give it

Brett StClair: Okay. Yeah,

Troy McDonald Kane: to you or you can regenerate it and I can give it to you. Yeah.

Brett StClair: I I'll I'll I'll regenerate it because I'm trying to we we set everything up on a dummy account on one of our accounts so I can just test all the SSPs and everything.

Troy McDonald Kane: Yeah.

Brett StClair: and I'm setting up on your accounts. And of course, it worked fine on our test developer URLs, but you don't have a URL yet because you haven't been accepted into the store.

  
  

### 00:01:01

  

Troy McDonald Kane: Oh, great.

Brett StClair: I was trying to see if there was a way I could hack a developer URL on it and see if I can bypass that, but they all want your developer URL, so we got to wait until that comes installed. But I'm using a a hack one that we've got to just bypass and check all the SSP settings to make sure that we'll be able to meet all that. Anyway, sorry guys, I'm taking up everyone else's time. How's everybody?

Troy McDonald Kane: How are

Brett StClair: Yeah, good, good.

Troy McDonald Kane: you?

Brett StClair: I had a very interesting week with my daughter's graduation which ended up in her breaking up with her long-term boyfriend who is living with us. So, he f***** up there. So,

edw: Oh,

Troy McDonald Kane: Sounds like your own reality show that

edw: wow.

Brett StClair: it was it was it was like housewives of

Troy McDonald Kane: you're

Brett StClair: Miami.

edw: Where do you live, Brad? You live in the suburbs of London.

Brett StClair: I live in to the kind of like commuter belt a place called Sari and there's a

  
  

### 00:02:08

  

edw: Oh yeah, sorry. You Yeah.

Brett StClair: little a little village called Cobb.

edw: Yeah.

Brett StClair: It's actually the home of the Chelsea football ground.

edw: Wow.

George Westbrook: The training, not the football.

edw: Okay.

Brett StClair: Oh,

George Westbrook: Not football.

Brett StClair: the training ground. Sorry. Yeah, the training ground from

edw: Are you uh foresee So your daughter graduated from

George Westbrook: Yeah.

edw: college?

Brett StClair: uni. Yeah. Yeah. from Exodity University,

edw: Wow.

Brett StClair: did a her neuroscience degree and uh got a dissertation a distinction for her dissertation about um uh how friendly LLMs are towards emotions, human emotions. So she mixed in neuroscience with large language models to understand how ready the world is for emotions. And I'm like, "Baby,

edw: Wow.

Brett StClair: now I introduce you to all my friends at Google and you will land a job there.

edw: That's great.

Brett StClair: Oh, so thank you.

edw: Congrats.

Brett StClair: That was super super

edw: I mean, that breakup makes me feel like when uh when uh Troy doesn't treat me

  
  

### 00:03:03

  

Brett StClair: special.

edw: right. Breakups are hard. And well, good luck with that.

Brett StClair: That was very funny. Next morning with a So he his parents flew up from South Africa. She happened to be dating a South African.

edw: Um,

Brett StClair: They all flew up and they had all just landed and we all meant to go for lunch together and it was super awkward because he he had f***** up and she was dealing with it and then we all went to lunch together in the world's most awkward lunch yesterday.

edw: I mean, the thing is, you know, dudes are always f****** up. I mean, if I looked at my Good

Brett StClair: All all the dads went,

edw: Lord,

Brett StClair: "At least it's not us. That's awful

edw: totally. I mean, I think the only person that's has ever not f*****

Brett StClair: then.

edw: up is George W. Westbrook.

George Westbrook: Oh, unfortunately I've got a mouth. Um, that that that does a a lot of the off offputtingness, I think,

edw: sticks and stones,

George Westbrook: as well as other things.

  
  

### 00:04:17

  

edw: you know, tell them.

George Westbrook: Yeah.

edw: Um, well, we've I'm sorry we missed you on Monday. It's been a a whirlwind with me back here. Um,

Brett StClair: Sounds

edw: so just I'm going to take a give the group in my group an update on kind of where I'm at because I started work

Brett StClair: good.

edw: yesterday at 3:00 am and I finished at 1:00 a.m.

Brett StClair: My goodness.

edw: in a 22-hour banger. Um,

Brett StClair: Jesus.

edw: and Jared, we're going to finish our call as soon as I catch a break, but it does look like we have all the things ready. I don't know if the uh offering circular got filed last night or it will be today but it will be done by I think today 5:00 pm today. So Eastern so that is really really exciting for all of us right so it changed the dynamic um I also had a call with uh the pay.com CEO who's basically the point person for all these Israeli mobsters and their money and all this stuff with Hard Rock and everything else.

Brett StClair: All

  
  

### 00:05:15

  

edw: So that went really really well. You basically they've come back and said, "How much do you want to raise and what are you going to do with the money?" So th those are

Brett StClair: right.

edw: really good um uh qualifying questions. Um so uh sorry, my wife. Yes. Um, anyways, so you know, they've they've dropped some bombs on me in terms of deliverables. So, right now I'm I'm I had to get the offering circular done. That's done. They've asked for a full business model um and and they want it to be as quote as detailed or granular as possible. I don't know if you guys remember Edward Hartman. He's like the more detail the better. So, um that's that. I'm I'm going to be working with Troy and Brian to help me with some of the the staffing and s*** like that. Um so that's for Hard Rock. And then Tom asked me for the you know distribution of how how they're going to put the money to work. He also did say to me group that he said um it's probably going to come from them individually as well.

  
  

### 00:06:27

  

edw: So, uh, it's not just the companies. So, like he specifically said Rafie has told him that he wants to put in money on his own and so has Teddy. So, they're probably going to come in as a group and then Rahm also individually. It may be in addition to the company. So, those are all incredible positives. So, just I'm a fully transparent guy, everyone. So, I don't I don't I don't like to f*** around, you know. So, basically, I told them 30 to 50 million is what we'd like. Um, and I said with 50 million, you know, I can basically turn this into a $2 billion company within the next 12 months. And he actually disagreed. He said it'll probably be worth four. So, um, there they will not Yeah.

Brett StClair: We said 100 will be welcome. Thank you.

edw: Well, I mean, look, the the the idea here is we need to launch. Like, we just whatever has to happen, we have to launch. And we have a like I'm looking at a f*** ton of work still and I got to finish the IP stuff with the patent lawyers and that's so like I I'm I was supposed to be in the office yesterday.

  
  

### 00:07:34

  

edw: Not a chance. Supposed to be in today. Not a chance. Um so for me I'm just I'm worn down a bit. Okay. Work-wise, not complaining, but I am worried about the deliverables. So like you know team-wise just George, you were you you're amazing on the weekends. you're giving us stuff that really helped for the hard rock. I got that uh information to him on Sunday. Brett, you two that the deck was fantastic. Um I mean really really good. Uh and I mean I mean the whole team, right? You're the only two pictures I can see. So I'm including Max. I know he's got a f****** ego on him. Uh so yeah, Max too and Hassan. Um, but all all those things, you know, I know it's weekends and it's tight, but just for the next five or six weeks,

George Westbrook: She's curious.

edw: it's probably going to be a little bit tough. Okay. And like, you know, we launch, you know, what I plan on doing um for the Novo team, you know, we have an agreement.

  
  

### 00:08:34

  

edw: We still don't have an agreement, but we have an agreement. So, the monthlies that I pay, um, you know, I'm going to allocate an additional bonus for our launch, okay? Um, because I want the team to know how much we appreciate. We couldn't be here without you. We need you. Um, but the next five or six weeks are going to be f****** rough. I mean, they just are. And you know I I want to be very clear that it's You know, I can't not have you. All right? Like, if I can't have you, no. Or if I can't have you, I'll make it like this. Everyone will. So, um, whatever we've got to do on that front. Uh, we're working hard on the SSP side, right, Brett? You're trying to get us together with what we're going to need to do. We need to get that ad server situated. Um, I met a group uh a husband wife through one of my buddies. The wife used to work at Publicist. She's got contacts there and at Omnicom that they've pitched to.

  
  

### 00:09:34

  

edw: I offered them a commission to go pitch it. Um, and then she ca they came back yesterday with a number of questions that Cody and Kevin answered. Um, so will they deliver anything? God f****** knows. Who knows? But the more and more I've done my research on this and looked hard um you know with this programmatic side I mean if we sell out 14 days in advance um you know nothing further we're going to we can come out really cheap and then we can just augment because that KFC and that nonbot determination though and then overlay football I mean we should get a much higher CPM than that 147 especially if we can integrate some of these ads, right? And um you know, if we're delivering the volume, this is one of the things that Hard Rock was talking about. Uh well, I hate strike that the the Rafi Ashkenazi like he indicated that that's a model that he's really excited about was the the ad revenue because, you know, if we drive the impressions the way that we think we can and if we get that level of engagement that we think we can, you know, I actually see a potential for a blended rate somewhere between, you know, four and maybe $6 as opposed to, you know, one and a half to three and a half.

  
  

### 00:10:58

  

edw: And I I've looked at a lot of different campaigns. I see what people are paying. You know, obviously we're not going to get that day one, but maybe come October, we're getting it. And you know, Troy and I spoke, you know, briefly and the team spoke briefly about I think we need to plan on having the NBA trading challenge right on the followup. So that starts late October. And now we've gotten, you know, some some realworld KPIs that we can tout and we've got revenue coming in. will have cap more capital because whether or not these guys come in or not, um I've been talking to my uh my other billionaire investor and I'm sweet talking her because she's a uh you know I'm I'm working on raising some additional capital, but my my concerning is like five or 10 million right now. I mean, even if I put in five or 10, that's going to be like, you know, kind of pissing in the ocean a bit and we actually need some real cash and because to market these things out the way we need to, you know, social media, all the other b*******, like we're going to have to spend.

  
  

### 00:12:11

  

edw: Um, so that's kind of where I'm at. I'm just I'm I'm running out of daylight every day. So I'm I'm hoping that after today I'll be able to come in the office, see you tomorrow, Troy, or you're not in tomorrow.

Troy McDonald Kane: No, I am no everything to tomorrow.

edw: Okay, then I'll see.

Troy McDonald Kane: So, we'll be in the office everyone

edw: Yeah. Yeah. So,

Troy McDonald Kane: tomorrow.

edw: we'll knock this out. Um and then hope hopefully I'll have that uh business model completed by Friday for the Hard Rock guys. It's it's tough. Uh because we have to make a lot of assumptions. We got to pull a lot of data because we only get one shot to look like we're credible with them. And that at the end of the day, we're actually auditioning not just for Hard Rock. Rafy's like going back to all the rest of them and saying like, "Hey, these guys are legit. If we give b*******, they're gonna be like, right?" So, we need to make sure that our our stuff is really to uh Mr. Cody and um we we will get that ready.

  
  

### 00:13:08

  

edw: So, I don't want to continue to dribble on. Um yeah, so that's that's kind of like where where I'm at. Um I also been working on the market maker stuff for our next call uh to ensure that we've got the two pieces a load balancing algo um and then the market making Troy uh on the allocation side for the the off-field revenue for the trading challenge. You know, I ran into a corner case where some FBS1 schools are going to play non-FBS schools and then how would I allocate that $2.50 or just going to give the entire 250 to the to the team that has shares available because you can't trade Kevin Murray State against Ohio State because there is no offering for them.

Troy McDonald Kane: Yeah. One thing we wanted to talk to you about which we don't have to go too deep into right now and and just hear me out for a second is because we are coming up on the August 22nd deadline for the IPOs. Do we still want to do the full scope of 138 or whatever the number is now of the the D1 schools or do we just do the power conferences for the trading challenge?

  
  

### 00:14:23

  

edw: No, I want them

Troy McDonald Kane: Okay.

edw: all.

Troy McDonald Kane: And you're not worried about like no demand for those bottom teams at all from

edw: Yeah, I'm I'm I'm ve very worried about it,

Troy McDonald Kane: the

edw: but the market maker is going to inventory up to 35% of all the shares for each team. Oh, what what I've written here in I've got I've got a lot to share to the Novo team.

Troy McDonald Kane: Okay.

edw: I know we're going to talk about it so Agenta can pick it up, but basically I want to make sure that um you know it'll buy it in the like the max increments, you know. So let's say hypothetically you're going through there's no Q established for say Air Force and you know right now it looks like there's a million shares to be available for NCAA football teams and 875,000 shares for the NFL. But in the event that any of those don't get picked up on say round one, then the market maker will buy 50,000 of those shares or whatever the max clip is. Okay? So, if there's no bid for, you know, Baylor, it'll buy 50,000.

  
  

### 00:15:27

  

edw: And then I'll just warehouse those and we'll we'll get out at least 35 I may raise that actually. We'll get out at 35 to 50% of every share that's offered at the IPO will be uh consumed either by the public or by the market maker. Cool. Yeah. Yeah. So, actually, I don't want to get into the market maker,

Troy McDonald Kane: Okay.

edw: but Yeah. So, a couple of corner cases like that and then like what do we do on by weeks? You know, if there's revenue established, what do we do with that? Um, some thoughts, you know, I just said f*** it. They don't get anything, you know, we'll just take that ad revenue because a lot of this is going to be like a preamble into the uh production level trading anyway. So, it it's been it's been a f****** mental trip for me. I'm getting too old. I'm going from simulation to production to offering circular to f****** patent s***. I'm just like, man, I should have stayed in school and you know, I was a real funny guy in the classroom and now I'm paying for it.

  
  

### 00:16:32

  

edw: So, all right, next. All right, who's in charge? Let's roll.

George Westbrook: suppose one thing there's a few few changes to the app as well. Um I think one one thing as well literally just before the call we got some feedback from Apple. So there's one one iteration we've got to make which we looked at it before it's a mistake on their part. It was something around age verification and that there needs to be parental controls because there might be people under a certain age using it which obviously we're which we put in the application. Um it's KYCed somebody under the age of 18 will not be able to access it. So we'll just manage the communications with them get the iteration submitted may kind of maybe politely politely tell them you're f****** wrong. look at what we wrote. Um, but the good thing is that's the only thing. Um, so that should be relatively quick

edw: Wow,

George Westbrook: turnaround.

edw: that's great. I mean, I think

Troy McDonald Kane: I'm I'm glad that's the only thing that's wrong because they were right that is on their side and easy to resolve because we using

  
  

### 00:17:30

  

edw: we

Troy McDonald Kane: a proper KYC uh interface.

George Westbrook: Yeah.

Troy McDonald Kane: But yeah, I thought it was hopefully I'm glad it's not anything else that's going to take time

George Westbrook: Yeah.

Troy McDonald Kane: to

George Westbrook: I mean,

edw: Yeah.

George Westbrook: Hassan's face when when he saw the email was like, "What the f*** are they talking about?" like blah blah like the age verification controls. They've got to be f****** 18 to use it.

edw: Does this sound actually swear?

George Westbrook: Uh yeah, he's got he's got potty mouth if you want to hear him.

Troy McDonald Kane: Yes. The tagline at the end of the meeting. Now we'll we'll to say

George Westbrook: Yeah.

edw: Yeah. Well, I mean, I thought he just mouthed it.

Troy McDonald Kane: it.

edw: I didn't hear any actual words. All right, that's great

George Westbrook: Um the um then just a few quick

edw: news.

George Westbrook: changes. Um where can we all see this? It's loading in.

edw: Oh, I see Garrett.

George Westbrook: Um,

Troy McDonald Kane: Wow.

  
  

### 00:18:27

  

edw: Oh.

George Westbrook: so one of the things we changed Yeah.

Troy McDonald Kane: So much better.

edw: Uh-huh.

Troy McDonald Kane: Look at that. You You just got Edwin really aroused

George Westbrook: it because it the thing

edw: f***.

Troy McDonald Kane: probably.

edw: Oh my god. That's so f******

George Westbrook: was was looking at it because spent

edw: good.

George Westbrook: a we spent a bit of time ages ago trying to get a 3D stadium with all the ads and stuff like that and we ran into a dead end because we were trying to get it fully animated things like that and then we realized it was left there in this kind of s*** 2D whatever it was before. So now at least it's going to show obviously the plays um where the the gains and losses are, where the ball is, and obviously when an event actually happens um that's going to update as well. And then there's the the watch mode which is still refining. Um but same thing, the events are still going to pop up. Every time there's event, you're going to see the current price or what the price was at that point in time for this team or this

  
  

### 00:19:26

  

edw: f***. This this this is so this is such a valuable piece, George.

George Westbrook: team.

edw: You've got to figure out how to that this section needs to be sponsored by somebody or we've got to have an ad in here. This This is way too f****** valuable because I mean, Cody, this is the only way you're gonna f****** use this app now.

Cody Haugen: 100,000 million%.

edw: This is it, guys.

Cody Haugen: Holy s***.

edw: This is f******

Cody Haugen: This is sweet, guys. This is f****** sweet.

edw: it.

Cody Haugen: My my and my my instant thing is you're not getting the watch zone unless you're paying us another

Troy McDonald Kane: Yeah.

Cody Haugen: monthly subscription fee. This is that powerful.

Kevin Murray: 100%.

edw: Yeah.

Kevin Murray: Is

edw: I mean, this is it.

Cody Haugen: Th this is if if you want the watch feature, it's another $4.99 a

Kevin Murray: that

Troy McDonald Kane: Yeah.

Cody Haugen: month.

Troy McDonald Kane: I'm imagining this on my iPad like phone

Cody Haugen: Holy s***. This is a

Troy McDonald Kane: up like Yeah.

  
  

### 00:20:17

  

George Westbrook: with more more widgets and and yeah,

Cody Haugen: sweet.

Troy McDonald Kane: Right. Exactly.

George Westbrook: like the It's It's

Troy McDonald Kane: The pro version of what else you just came out with like you can like

Cody Haugen: Yeah, we're we're we're charging for this, guys.

edw: Cool.

Kevin Murray: I was going to say,

Troy McDonald Kane: Yeah.

Cody Haugen: Most definitely.

George Westbrook: Yeah.

Kevin Murray: is there a way we could use this or have it like this for like say 5 minutes where they can use it for free and then it pops up then they have to pay for it.

edw: I

Kevin Murray: something like that where the

Skye Capazorio: You definitely want a premium route to to do this to pri premium.

edw: think

Kevin Murray: premium

Skye Capazorio: So like free and then you have a premium to extend That

edw: f***.

George Westbrook: H.

Kevin Murray: just an idea I don't know if that's or just going straight to the premium

George Westbrook: Yeah.

Jared Sapirman: That sounds like a good idea to me, Kevin.

Troy McDonald Kane: or or a day a day free like not you know because usually it's like you get the first day free.

  
  

### 00:20:59

  

Troy McDonald Kane: If you like it, subscribe because you're you're going to want more than just five minutes.

Kevin Murray: Yeah.

Troy McDonald Kane: But that's a great idea, Kevin,

edw: Great idea,

Troy McDonald Kane: to give people Yeah.

edw: guys. Kevin, it's fantastic. Troy, I like your version even better. You know,

Troy McDonald Kane: Yeah.

edw: this I I mean,

Kevin Murray: Yeah.

edw: this is incredible for for for trading and and watching and interacting. This is going to be 90% of the time people will be right here

Troy McDonald Kane: during games.

Cody Haugen: 100.

Troy McDonald Kane: Yeah.

Cody Haugen: Yeah.

Troy McDonald Kane: Yeah.

Cody Haugen: George, can I ask a quick question on where we are as far as IP of this?

edw: like

Cody Haugen: Is this now completely rebuilt just powering off of Sport Radar real-time data or are you guys still using the live mass tracker module from Sport Radar?

George Westbrook: I think I don't really think any like this is All completely completely

Cody Haugen: f*** yeah, that's the answer I wanted because we could white label the s***

George Westbrook: custom.

  
  

### 00:21:50

  

Cody Haugen: out of this as well if we want to and resell this you well to

edw: No. Yeah. No.

Cody Haugen: our partners Edmond is what I'm thinking.

edw: Yeah. Fair.

Cody Haugen: I'm not saying that to everybody,

edw: So,

Cody Haugen: but if Hard Rock wanted to put something in their app,

edw: you see Yeah.

Kevin Murray: Oops.

edw: You Yeah.

Cody Haugen: we can white label this watch solution to them.

edw: Do you see right underneath the score 100? We've got that gap of space. It's a night. Yeah. Right underneath that all that blue. It's very very relaxing and spatial, but that has room for like, you know, even if it's a little bit on the smaller side. I mean, th this is this is premium s***, man. This will be it.

George Westbrook: that one thing this scrubbing mechanism as well. So if you want to skip through that's not working multiple uh how it should work is when you go along yeah like that you can go through different events and then say the chart as well you can go through write this event there that event there blah blah for each team the candles

  
  

### 00:22:57

  

edw: Jared, what's your take on

Jared Sapirman: I think it's good.

George Westbrook: Hello.

Jared Sapirman: uh on the field the MIA was in the wrong

edw: this.

Jared Sapirman: direction. Uh the the letters like that's that's written

George Westbrook: Yeah. Yeah.

edw: Yeah,

Jared Sapirman: incorrectly.

edw: I think um I thought those were just dummy uh for for visuals. Okay, but for forget that for a second. What's your take on this?

Jared Sapirman: Yeah, I think it's good.

edw: You're a big shark guy and a big landscape

Jared Sapirman: I definitely agree with Kevin. I agree with Kevin that this should be free for some time because honestly,

edw: guy.

Jared Sapirman: nobody's going to pay for this unless they experience it first.

edw: Yeah, it's probably right. But f***, it's good. And that's good.

George Westbrook: and then the win win probabilities as well. So, it's just cuz obviously like if this was desktop um or iPad, obviously there's there's ways we can have like ads would be a lot easier to see on here and the way in which we'd be able to have multiple different things.

  
  

### 00:24:03

  

George Westbrook: Obviously, we're limited a bit by phone,

edw: Yeah.

George Westbrook: but then there could be a way where let's say down this right hand side you can scroll up or scroll down and you can see you can see other other graphs for example and then maybe there's an ad unit in each of them as they scroll up or scroll down.

edw: Heat.

George Westbrook: And then this is kind of maybe more more fixed.

edw: Like, so let let me ask a group this because I'm trying to model our our projections for

George Westbrook: Um

edw: the CPM s***. You know, you're looking at this, Cody, and you're you're you're trading your balls off, right? And you're like, "Okay, whatever." Um, how many impressions are we going to get a minute in this kind of thing? Because like I'm telling you, if if I had this to trade on on these products, I wouldn't use anything else. This is where I would be. Literally 90 95% of my time would be right here because all I care about are the probabilities, the prices, and then what's happening on the field.

  
  

### 00:25:06

  

Cody Haugen: agree with that sentiment, but you're still going to switch to other games. So to get to other games, you're going to go through three other screens, back to this screen,

edw: Sure.

Cody Haugen: three other screens, back to this screen, or you know, one other screen, back to the screen. So you are still going to be cycling through the app, but once

edw: But let's say let's say Cody, real quick, let me let me just finish this and then I agree with you on that. Let's say you're going to just trade this game, okay? And you're going to be on here for three hours,

Cody Haugen: Okay.

edw: okay? What how many impressions are we going to be able to push through in three hours if you're just literally watching and trading this particular game?

Cody Haugen: Yeah.

edw: I know you guys use the term spammy.

Cody Haugen: I mean

edw: Um, but like George Brett, what do you think? I mean, what what's an acceptable amount of of things that we could put in there?

Cody Haugen: Well, so let me just

George Westbrook: I think one of

  
  

### 00:26:01

  

Troy McDonald Kane: The one thing I will say though is if we're charging a premium for it,

Cody Haugen: something

Troy McDonald Kane: there's going to be less desire to see advertising or plugs on it. Just want to point that out that it may deter people if they do pay for it to cancel it

edw: All

Troy McDonald Kane: because part of paying for premium services on apps is to not see ads or get popups or have

edw: right. Well, well,

Troy McDonald Kane: to watch.

edw: let's take the pay out for now. Let's just talk about the CPM model because like right now it, you know,

Troy McDonald Kane: Okay.

edw: getting five bucks a month from, you know, 50,000 people, it's juicy, but it doesn't validate our premise, which is we're we're trying to monetize engagement. So, let's just talk about the the the the impression side. What can we do in terms of that volumewise before it starts being spammy?

Jared Sapirman: Edmond,

edw: I mean,

Jared Sapirman: quick thought,

edw: go ahead.

Jared Sapirman: quick thought. Um,

edw: Yeah.

Jared Sapirman: how about if we for everybody we have ads and then the paid feature is getting rid of the ads.

  
  

### 00:26:58

  

Jared Sapirman: ads on there. There's quite a few apps that do do that.

edw: I don't I want to stay away from that this first iteration. I I hear you because I one of the questions that the Omnicon from US came back with

Jared Sapirman: Okay.

edw: was can people pay to have the ads off throughout the entire app experience? And right now I don't want to do that because like it's not worth it to us. I think we can monetize it for like this isn't a one-off event. We're trying to build like value for our marketing partners and brands that they're like, "Hey, this is more powerful than advertising at a stadium." You know, we'll pay a premium to be involved in, you know, football, basketball, baseball, whatever, whatever the f*** we got. You know what I mean? I'm trying to get it where we're building our our our value by having the the users engage with the the apps. Sky,

Troy McDonald Kane: So with that said,

edw: what do you think?

Troy McDonald Kane: sorry,

edw: Go ahead.

Troy McDonald Kane: go ahead.

  
  

### 00:27:57

  

edw: Go ahead,

Cody Haugen: I'm

Troy McDonald Kane: Yeah, sorry. With that said,

edw: Troy.

Troy McDonald Kane: do we want to think about this differently for the trading competition versus production and

edw: I don't know.

Troy McDonald Kane: like

edw: I don't know. I think we got to let the market tell us, right?

Troy McDonald Kane: having

edw: Like if our CPM prices don't increase over the course of the challenge, then I think we move to a pay uh for certain functions of the app of maybe higher price. But, you know, I here's the here's the answer to the question I want though. I want to know how many ads per minute do we think are reasonable for if someone's on this particular screen for 3 hours?

Brett StClair: I can give you a sense on that.

edw: Yes, sir.

Brett StClair: And so impressions is all about brand and it's about recognition. And so a lot of guys try and convert their impression ratios to like GRPs, which is how you measure TV audiences. How long did they see the ad? So it's about how many times have you seen the ad?

  
  

### 00:28:58

  

Brett StClair: How long have you seen the ad? And so I wouldn't think of the world as how many ads per minute. Because if you're thinking how many ads per minute, think about it from the advertisers's experience. They're going f*** on that screen and I get 3 seconds. I think the way we need to be thinking about it is every single thing we do with an ad unit will have an impact on a data point that'll have an impact on your CPM. And so that could be fill rate, could be your click-through rate, could be your CPM. Those your three kind of core data points you need to be very very careful. And so my advice would be we start off with uh 20 seconds. Load an ad in rotate. see get some data for a week on that particular page then shorten it bring it down to 15 seconds let's monitor let's see how it's impacting the CPM the CTR because if we impact the CTR so the CTR is not so important for For us,

  
  

### 00:29:59

  

edw: Let's see here.

Brett StClair: CTR means um click-through rate. So, an advertiser, the CTR is what counts,

edw: Okay.

Brett StClair: especially in the world of programmatic because it's performance. And so, performance is saying, "I'm only going to pay for the click. I don't care about the impression." And so, we're measuring everything as CPM, but in reality, a lot of the actual monetary value is going to come from a CTR. And so, we actually want to encourage the person to click an ad. Yes, it's going to go out of our space, but you're going to have happy advertisers.

edw: Right.

Brett StClair: They're going to go, "f*** yeah, this is a great platform. You know, I'm converting customers. I'm making money." And the big test for us is, so they click on the ad, are they coming back? That's going to be the big If they click an ad, never ever come back. And so um an example of that would be um a competitor. You've allowed competitors onto your space. They're clicking on an ad.

  
  

### 00:30:53

  

Brett StClair: They're going, "f****** hell, this this is a way better app than in play. I'm never going back to it. That is a poorly managed inventory. And so we make sure we never have competitors that put us at risk there. But if it's a complimentary advertiser, so advertisers where you know what, it's for uh I don't know uh what's the stuff George Ve all the

George Westbrook: Zin or Vello these

edw: cocaine.

George Westbrook: things.

Brett StClair: kids have.

edw: Cocaine.

George Westbrook: No, no,

Brett StClair: And they put the bag underneath their li and it's it's like tobacco,

George Westbrook: no.

Brett StClair: right?

edw: Oh.

Brett StClair: And it's ve and and it's a little packet of tobacco and yeah, that's that could be really complimentary. Young men, everyone likes a bit of ve great. They see an ad for a discount, boom, they'll be right back 100%. They're just going to top up on their val and then they straight back into those are complimentary advertisers on a great CTR. Now, if you're shortening it where then the user is not getting a chance to see that special because you're trying to rotate as many ads through.

  
  

### 00:31:56

  

Brett StClair: The problem is, yeah, you might be getting an impression, but you're not getting a valuable impression. Your impressions start to de decline, right? Because the advertisers over time will go, "Yeah, not really great audience that because no one's actually buying my product." And so, it's finding that time. So, as we do this about optimizing

edw: Let me ask you this then, Brett. Like when we talked about the programmatic spend and they're like, "Oh, it's a buck 42 or whatever the f*** it was, 47, I don't remember." Um,

Brett StClair: average.

edw: yeah. Per thousand, right? So that's like how many impressions per thousand?

Brett StClair: No.

edw: Um, you know, like Viral Nation tried charging me a nickel for every uh like they had 20 million impressions. They wanted like $1.2 million.

Brett StClair: Right?

edw: That's what they they were talking about. So like I mean that that wasn't great math for me, right?

Brett StClair: Doesn't make sense. Right? So this is also the problem with impressions. It'll start at 147. That's your kind of CPM.

  
  

### 00:33:03

  

Brett StClair: And then you get effective CPM. That's what publishers actually want because the ad serving, the guys serving the ads, the programmatic guys are taking a slice of that. Everyone's taking a slice. So if we say only took traffic from the ADM mob, they might be actually selling it at $2.50, 50, but they're taking a cut of 32% by the time you see it. Then there's other ad serving fees. There's spillage, there's unserved ads,

edw: Mhm.

Brett StClair: there's um spam, there's all these kind of things that no way at it that keeps going down. You got serving fees and all these kind of things. And so you get an effective CPM that's usually quite low because your fill rate is never at 100%. And so this is what the SSP, the the expert in a specialist in doing this every day. Their jobs are to be monitoring this every 15 minutes going, "Okay, where are we on this? I'm going to ramp this up. I'm going to load a different ad unit here.

  
  

### 00:34:00

  

Brett StClair: I'm going to price up my algorithm. I'm going to put a lower." So they're kind of like market making it a bit,

edw: Yeah, I get it.

Brett StClair: right?

edw: Those

Brett StClair: Trying to load the price. And you know, there's a lot of demand, so they're going to push that price up automatically.

edw: are

Brett StClair: And so the proposal I wanted to talk to you today about is it's part human and part AI. And so the human part is helping us set it up, get all the traction, get all the configs. It's a heavy heavy lift working with these guys. I mean, like I've just been trying to do with demo accounts to see how much work it is to get these guys going because it's all manual. But then we're looking at the world going, you know, we build out a bunch of agents for you guys that are literally bidding and moving the ceiling and the floor pricing based on demand and everything every single day. That's one agent that's doing it at like every 5 minutes.

  
  

### 00:34:47

  

edw: Okay. Yeah.

Brett StClair: Because the reality in programmatic media buying, if humans doing it, they're doing it once a day. But we want to optimize the f******

edw: Right.

Brett StClair: s*** out of this. And it could be duration that we're seeing in the ads. We look at every single ad unit on every single page. We might flip an ad unit to a different type of ad unit. We might flip it to a different type of advertiser. We're going to constrain it because all of a sudden we're seeing too many, I don't know, um, alcohol ads coming through. Bad example. And those are coming in really, really s***** CPM. But we want car ads. And we seeing that the demand on car ads is pumping. BMW, Mercedes, it's that time of year. They're flipping on all their card ads. We're going to gun after that revenue. And so how we're going to do it is we're going to frame the audience slightly differently. We're going to put in a slightly richer ad unit that we usually have a standard banner.

  
  

### 00:35:39

  

Brett StClair: No, f*** it. We're going to have a fold down banner to attract that in the beginning. I'm going to see how we stimulate that ECPM. So it's exactly like a marketplace. And so we're saying put a human in it and then we wrap some aentic to really light this thing up.

edw: Understood. Okay. I mean, that all makes sense. It it scares me in a lot of ways. Um number one for my

Brett StClair: That's why like we we take the 147 by the way and the 147 is they look at

edw: purpose

Brett StClair: us and they go that's what your average is going to be and they've seen it again and again again and again again but they're looking at a

edw: is that post Yeah.

Brett StClair: global level they they haven't added on the multipliers they haven't done like you said

edw: Yeah.

Brett StClair: yeah

edw: Is that post um like ADM mob rake?

Brett StClair: uh that's what the advertiser play the CPM So remember that that's

edw: Yeah. So then our Yeah,

Brett StClair: before.

  
  

### 00:36:28

  

edw: before so you know couple things. So like I as I was explaining that Viral Nation their um CPM was cost they provided was

Brett StClair: Yeah.

edw: like 50 bucks per CPM, right? So it's a it's a very big number and I you know I thought that was outrageous but then so

Brett StClair: Yeah. But like you guys shouldn't be looking at a $50 CPM. You want to be going CTR.

edw: so

Brett StClair: You want a click price. CPC. This is called cost per click. That's what you guys want because you want to pay only for your click.

edw: let's say hypothetically do we want that model for inplay

Brett StClair: That's a way better way to optimize. You will be getting a blended model of that coming through the in order to attract the audience. And so the point of having a a demand side specialist is they'll look at how much traffic's coming through CTR. If you have really strong CTR, by the way, means you're getting a high CPM.

edw: Yeah,

Brett StClair: If you're getting a really low CTR,

  
  

### 00:37:24

  

edw: I get it.

Brett StClair: your CPM's through the floor. It's going to be s***. And so then it's going to be like, f*** it. How much brand spend? So, it's called brand spend. Pure CPM is called brand spend. That's where someone's come in, they said, I'm not interested in the clickthrough rate. I want to secure myself an certain amount of time in front of an audience. And Coca-Cola is famous for brand spin. They'll be like, "I just want everyone to know it's happiness. It's happiness. That's all I give a f*** about. They must see red everywhere and f****** happiness." And that's their brand strategy. And it works for them, right? The big brands,

edw: No,

Brett StClair: you can actually see a dip in their sales when they cut

edw: no question. So, here's a couple things. Okay,

Brett StClair: brand.

edw: so the click-through rate on our product might be lower because of the interaction that they have with the market, right? So,

Brett StClair: Yeah.

  
  

### 00:38:12

  

edw: it may not be uh I don't think we can call it apples to apples, right? Like I I don't think it's like a website. We're like, "Oh, yeah. You want to buy some f****** like bandscaping tools?" And you're like, "Yeah, I'll buy that s***." I don't have anything taking my attention away from like, but we're we we're more about the I think the the promotion and the awareness

Brett StClair: No, it's not.

edw: unless it's slow than the click for is my my gut number one.

Brett StClair: We'll figure it out through the data. Our goals are to get you the highest possible CPM.

edw: So,

Brett StClair: To get you the CPM

edw: and how do we mark how do we market though to the SSP or the ADM

Brett StClair: up,

edw: Mob clients and and whomever? Like how how do we market inplay as a new spot for them to buy?

Brett StClair: you don't performance,

edw: You

Brett StClair: performance, performance, performance. So, this is where I am at the moment. I'm not trying to get you guys on.

  
  

### 00:39:05

  

Brett StClair: I've registered a couple of testers.

edw: know,

Brett StClair: We've been running some ad units on the literally on our own accounts. But again, we're starting to see that dry up because they very quickly go, "Oh, this is the demi demo s*****. We're not filtering ads there." So, they cut you off quickly. They want live accounts. So, as soon as we're live, we need to be taking that, banging it into all of those different platforms. They want data points. So volume and performance and so word go we do that once you start and so what I've spent five years of my career on the publisher side um helping publishers all over the world get the most optimum eCPM and what happens is as the network or the exchange you see the volume and you're like we're fuggling we're fuggling we're struggling to fill that inventory. And so what they do is they take note and they have a look at the inventory. They look at that type of audience because they're actually interested in your audience, less so your product in the beginning.

  
  

### 00:40:07

  

Brett StClair: Then they go, "Okay, we're going to get this in front of our advertisers." And so we kind of jumped the we jumped ahead of that whole conversation, getting some conversations going globally with them because we know this is a great product. We know this is going to be a f****** great product where these brands are going to want to be like, "We know it. We can see it. They know it. But we just don't have the data points to prove it to them.

edw: Right. Well, I mean,

Brett StClair: But and then we switch more and more to direct.

edw: like,

Brett StClair: You kind of shift because then you start building the relationships with the guys and you start

edw: so we're g we're going to modify our goal is to modify away from programmatic into more direct

Brett StClair: shifting.

edw: relationship because I look at like, you know, a billboard at the at the stadium.

Brett StClair: Yeah.

edw: It's like I can't click through that f****** thing, you know? I just look at it and say, "Okay." And most of the sports ads are kind of like that.

  
  

### 00:40:58

  

edw: I don't imagine there's a ton of clickth through during games while they're being

Brett StClair: Yeah, I mean I actually know the stadium world quite well through rugby.

edw: played.

Brett StClair: Um like Lion sponsorship, big Lions fan. I know all the media guys, Mega Pro and all those guys. That sponsorship, you know what that sponsorship is? It's a sales sponsorship. So it's about say uh Vodto phone um they'll buy out all of that. Yeah. So they get their brand everywhere. When they bring their top clients into the box and entertain the s*** out of them and blow them up and wow them up and while they're in there all they're experiencing is Vodafone, Vodafone, Vodafone. It's low down the funnel, right? It's not necess then they'll sell it. Yeah, it's branded and you know the audience sees it a bit. No, it's actually a sales comes out of sales marketing budget. The guys who've got banners and everything, they've got full-on hospitality. They've got all these sales people working the s*** out of it.

  
  

### 00:41:58

  

Brett StClair: This is all about close the deal over a bunch of drinks, getting the customers hammered, and we see it like the whole time. And so, yes, they're not getting the clicks, but my god, it's impressive when you're being sold to in that environment,

edw: No,

Brett StClair: right? So,

edw: no,

Brett StClair: it's lower down the

edw: no. So, Brett,

Brett StClair: sales

edw: how do how do how do we prepare this business model or Hard Rock given that we've got a lot of different levers to pull here? How do how do I do this?

Brett StClair: So, I've been working on your modeling and so this modeling is going to bring out a whole lot of stuff for you and I need to add later screenshots.

edw: Okay.

Brett StClair: So, this is a bit old, but I'm trying to work out a whole bunch of stuff here. So, these all the data parameters they're going to help you with your business model. And so what we need to do is we need to sit down and go homepage. I can run the model and update all these these images a bit better.

  
  

### 00:42:59

  

Brett StClair: Um we've got the degenerate. What is the degenerate? What type of person? What do we think they're going to do? All that kind of stuff. We think they're going to generate 250 page impressions a week. We think we can serve five ads on that page. So that's saying how much time how many ads are they most likely going to see. Scrolling down the starter, they're a little bit less. They're kind of they're in three to six sessions per week. They're active 12 to 21 days per month. So I'm trying to figure out who that user is. So if you guys can help me with that, then all the way down to a max who's a complete nobody in life. Oh, wait. Sorry. I meant I mean the max. um the returning,

edw: is the max. Yeah. Yeah. I

Brett StClair: right?

edw: love

Brett StClair: And and so they're entry level and they're doing 30 impressions at six at five ads.

  
  

### 00:43:52

  

Brett StClair: And so I've tried to do that. You see how I'm starting the bottom up and I'm working it upwards.

edw: Yeah.

Brett StClair: And then I'm so glad you've done so try to map all the pages and then go into So I've put in a well, how much of your audience is degenerate, but you guys reckon it's going to be higher. Great. We'll put up that percentage of degenerates. Now, I'm going to share this with you so you can also play with this and put in your numbers and put in your

edw: Yeah,

Brett StClair: figures.

edw: that'll help me a

Brett StClair: And if you don't like the numbers on the homepages,

edw: lot.

Brett StClair: we put them up either here or we put them up on each page or we put them down until we get a number. And then what I've done is I've tried to start working out what are the revenues, each of the breakdowns, what do they or who's taking what at each cut. Then you go on to how many live events. I've tried to put in every single parameter.

  
  

### 00:44:43

  

Brett StClair: Um um start off with a 90% programmatic, 5% direct,

George Westbrook: Yes.

Brett StClair: 5% territory. Um how what are the price points? and 47 on blended CPM. fill rates at 30%, you know, all that kind of stuff, even to the point where you've got an uplift. So, if it's KYC verified, you know, you're going to get an uplift of 1.15. Uh, if it's teams followed, uh, so anyone who's following a particular team, they'll get an uplift of 1.1. So, what that's doing is upload uplifting the value of the inventory. So, I'm trying to bring in absolutely everything. Then you go to the top and then you start going how many users will I have at 200,000 at 5 million. What happens if I have an aggressive figure? Why is my eCPM so low? Break it out and then you can start seeing okay so there is an uplift. We can tell you what all the uplift figures are there. All the uplifts and what the direct caps and everything look like.

  
  

### 00:45:53

  

Brett StClair: Remember, these are the figures that we're going to continuously be manipulating,

edw: Mhm.

Brett StClair: massaging to keep upping it. My suggestion on this is you want I've tried to do as worst case scenario on this. I know that's that's not your style, but let me be the pessimist in this and then you be the optimist and then I think we're going to land in a really really good place. I put in your viewability, IVTs, progs, you name it. absolutely everything until what you get to your blended CPM and you can have a look at all the data. If we spend a bit of time here, we'll have the exact figures on what we think the impressions are from a bottom up point of view. We'll have the exact data. We can then make some assumptions on what we think the actual eCPM growth. That's why I'm happy you've been looking at it and been getting more data points because I'm with you. I don't think the 147 is our worst case scenario. That's what they're coming to us as a industry and they're saying you should be on average because everyone else is there at 147 like that.

  
  

### 00:46:58

  

Brett StClair: You're going to get more than that. What does that actually look like in actual ad revenues? But with a really, really, really good baseline, not worked out per minute. The problem with per minutes is the industry's tried to do it for years.

edw: Doesn't

Brett StClair: It just it doesn't work this way. You build it up.

edw: work.

Brett StClair: I mean I mean some cases I'm over cooking it. I think I'm overcooking it here. Live games, but maybe not. I'm saying the degenerate will spend four they'll generate 460 page impressions and they'll see about 20 ads per page impression on watching game days per week. That feels reasonable to me to be honest.

edw: That seems low to me to be

Brett StClair: That's what I thought cuz I thought and then part of me is like am I overcooking it?

edw: honest.

Brett StClair: Well, I don't know. How long would you spend on a game day? Especially this new game day screen.

edw: Yeah.

Brett StClair: Maybe it's a thousand,

  
  

### 00:47:48

  

edw: I mean,

Brett StClair: right?

edw: realistically, you're going to spend, you know, like if you're trading a game, you're going to spend two and a half hours of that game in. app right now.

Brett StClair: Yeah. So

edw: Like and I will like I'll trade or bet I'll start betting on Saturday at

Brett StClair: then

edw: 11:00 a.m. I will I will be active until 1000 p.m. So I'll go for 11 hours straight and I trade or bet a lot of games. So it's like you know I I mean and there but obviously it sounds crazy but it's some of the funnest time of your life. I mean, is are those lost Saturdays gambling and betting on the football games, right,

Cody Haugen: Yeah, absolutely. I mean, I'm also thinking like I mean with the international games,

edw: Cody?

Cody Haugen: you can do that on a Sunday now, too. uh where international game starts at 7:00 a.m. and you're betting slashtrading on our platform until 1000 p.m. when the Sunday night football game

edw: Yeah.

Brett StClair: So,

edw: Yeah.

Brett StClair: even like I think I've got the audience mixes wrong.

  
  

### 00:48:47

  

Cody Haugen: ends.

Brett StClair: I've just taken what a traditional media company would see from a super user point of view and overlaid it.

Cody Haugen: Yeah,

Brett StClair: Again,

Cody Haugen: I mean that's that's the biggest I think that's the biggest edit from the highest Yeah.

Brett StClair: that's going to be huge impact.

Cody Haugen: from the highest level that adjusts these numbers is the degenerate number is going to be I don't think there's going to be like this middle ground user. I think it's you're going to we're going to get these degenerates and we're going to get these very new kind of sort of hey this is new. This isn't betting. It's not a prediction market. It is trading. I'm a trader but I've never sports gambled before. That type of thing. So I think it's going to be one end or the other at least to start. But I think those numbers are the the high level that we can change. Do you want to do you want to set up time for us three uh or whoever from the team tomorrow morning to go through

  
  

### 00:49:40

  

Brett StClair: Yeah. Yeah.

Cody Haugen: this? Do you want to send it to us?

edw: Yeah.

Cody Haugen: Have Edwin and I take a spin through

Brett StClair: You can have a spin through it. But I think do a spin through, play around.

Cody Haugen: um

Brett StClair: I've every every acronym you can click on, it'll tell you what it is. Every calculation, it'll take you to where the parameter is. So you can actually see, you know, like why the f*** is that feeling so low? Why is that feeling so high? And it'll give you all the justifications on how to do it. So I've tried to make everything clickable. The models have been run and run and run and run and run. I can't see how we're going to get the models more optimized. Now it's about getting the right data inputs. Um, and like when I run some of the models, you're getting billions, you know, right? And that's just with my numbers. And so like I I think you're feeling right.

  
  

### 00:50:29

  

Brett StClair: I think what we got to get right is the eCPMs because the eCPM is after everything. And the reason why the eCPM is coming so low at the moment. So eCPM is effective CPM and effective CPM is coming low because I've got your fill rate at 30%. your film rate will be low in the first month.

edw: of

Brett StClair: You just no matter what you do, as you say, you want to tell everyone about it. We've got to get the data to these engines as quickly as we can.

edw: There's

Brett StClair: And we'll be testing as many of these exchanges is seeing which one's going to adopt us as quickly as possible. Run with one and then start feeding some inventory to another to give it information. And that's how you kind of get these guys excited. But at least then you can play with these numbers. And these are all industry calculations. I mean, I've gone through Sky also helped me with some of the calcs. It was slightly wrong on on the seasons because when you divide it by the months, it doesn't come out right.

  
  

### 00:51:26

  

Brett StClair: But essentially what it's doing is it's saying you start off with a spike kind of grows a little bit. It clusters there's some some narrow part and it kind of works everything out. So you can't just divide it by x amount of months. Um the season calculations are working out right now. I've run a bunch of tests on them. Um but the big things are what is the audience makeup? What do we think that's going to be like? What are the number of page impressions that we think we're going to get?

edw: Got it.

Brett StClair: What this thing doesn't have is the ability to save. I'm not running it on a database. So, I'm running it in the model. And so, that's why I have a play.

edw: Mhm.

Brett StClair: You can hit a reset button. You can put numbers everywhere. You can save it, but it just saves it on your screen. If you close out of it, those numbers are gone.

edw: Real quick, Jared, what's your take on this um user journey?

  
  

### 00:52:22

  

edw: Uh you're a trader. You're not Are you a sports guy or no?

Jared Sapirman: Am I a sports guy, Edwin?

edw: Yeah. Do you like I mean do you like football?

Jared Sapirman: Yes,

edw: Do you bet on it and s***

Jared Sapirman: I have.

edw: like that?

Jared Sapirman: But I don't bet I would say a lot. But I mean, I'm always watching sports no matter what.

edw: Okay. So,

Jared Sapirman: Yeah.

edw: what's your take on on how how long someone's engaged on a Saturday and Sunday with football, your

Jared Sapirman: Um I would say a good amount.

edw: age

Jared Sapirman: probably not as much as you, but it and it also depends on what teams are playing, right? Uh if there's great games that are going on, there's I think there's a lot more factors than just like, oh, it's a it's a Saturday. Oh, it's a Sunday. I'm going to watch all day. If there's like marquee games, I'll be there for that. If there's a team that I'm interested in, I'll be there for

  
  

### 00:53:11

  

edw: Yeah, I'm not asking about the watching pattern.

Jared Sapirman: that.

edw: I'm I'm more interested in how people will trade it. Like I don't give a f*** if like Pee-Wee Herman's playing, you know, Arnold Schwarzenegger. It's gonna that game's going to get blown out. If I can make money in it, I'm gonna I'm gonna trade it or bet it or whatever. So, you know, the the the actual the big title games for me, they're generally harder to to bet. The lines are really tight. Um, so I look for softer schedule for me to to actually be effective in.

Jared Sapirman: Yeah, that's yeah, betting is not my area.

Cody Haugen: Same.

edw: All right, let's talk about trading.

Jared Sapirman: I would

edw: How do you how do you see people your age engaging with this app or younger? Um, do you see them being, you know, multiple hours a day out during game day or do you see them being like click and you know what do you guys do? Go your

Jared Sapirman: No, no, I can see it happening. Yeah, there's definitely going to be certain days where people will spend a good amount of maybe an hour or two hours on

  
  

### 00:54:07

  

edw: feelings.

Jared Sapirman: it. Um, there are also going to be others where they don't. Um, especially like I I think that once there are like or when there are close games in the fourth quarter, once people experience trading those types of games, that's going to be very addictive and interesting

edw: Right. But the fundamental here,

Jared Sapirman: to

edw: the underlying is we're trying to reward people for trading with cash. Right?

Jared Sapirman: Yeah.

edw: So the better they trade, the more they trade, the more money they make, the better all that stuff is, they can actually earn money. So, at at at the crux of our our offering is, hey, there's a pot of gold here. You got to go trade for it. We're giving you the the application to trade on for free. You get to trade it for free. Everything you get to do is for free. Go get some money. Um, to me, that reduces all the I hate the word now everyone use it, but the friction um for someone to get involved with it because it's doesn't cost anything.

  
  

### 00:55:18

  

edw: And ultimately, if you're watching games for entertainment, you're going to do whatever. But if you're engaging with inplay because you're trying to make money and you're trying to learn how to trade and you're trying to enjoy the game in a different way, it's a whole different experience than saying, you know, Ohio State's playing Michigan. I want to watch it. But, you know, my my my belief is that people are going to say, well, f***, I can make money doing this. Instead of betting or trading on Kouchi, I'm going to come to play because it doesn't cost me anything. And you know, by the way, every play the prices are moving. So, I'm gonna stick around here and I'm gonna try to make some cash. That's what that's what my mind

Jared Sapirman: Yeah, I can see that. It's just the attention spans in my age group are lower,

edw: says.

Jared Sapirman: right? And and me and younger are lower. Um, but I can see that happening 100% where they spend a lot of time. But as I said, I think I've told said this before, there's going to be notifications that move them off the app, then they come back there.

  
  

### 00:56:18

  

Jared Sapirman: It's I don't think it's going to be a like hour straight on the app. There may be a couple of things where people's attention goes somewhere else for a few minutes here and there, a text message, whatever, and then comes back.

Troy McDonald Kane: The other thing to note that I'm I'm thinking through when you made that kind of ex example, Edwin, is what happens when you're let's say you're halfway through the game and you know, you're you have no chance of being in the top 400 or whatever the prize allocation level is. And then they just say, "All right, I'm done. Um, there's no way I'm going to make any or like compete for this pool of capital today.

Brett StClair: Wow.

Troy McDonald Kane: I'm going to walk away, come back another day.

edw: Well, that's why we tried to do the the comeback trader,

Troy McDonald Kane: So,

edw: right?

Troy McDonald Kane: yeah. But I mean, even then, like I feel like um the younger age demographics are quick to give up.

edw: Sure.

Troy McDonald Kane: Um because if they don't see a path to like I think more serious traders definitely will be like, "Yeah, I can recover this." But I think,

  
  

### 00:57:20

  

Troy McDonald Kane: you know, when we're talking about tens of hundred, tens of thousands to hundreds of thousands of users, I feel like there's going to be a decay of participation throughout the game based on where you are in that rankings in in the leaderboards for each of the categories because, you know, the comeback trader of the day will have a separate leaderboard so you'll know if you're in contention or not.

edw: Yeah. I I you know, we'll we'll see how it's all borne out. You know, I I I don't necessarily agree with that. Um to I I get your point. I mean, it's a valid point. I just,

Brett StClair: It's

edw: you know, it for guys who don't gamble or don't trade it or, you know, aren't involved with it, like your perspective is going to be different than the people who actually do

Troy McDonald Kane: Yeah, but that's not the demographic we're talking about here,

edw: it.

Troy McDonald Kane: aren't we? Talking about 18 to 22 year olds mostly in the first iteration

edw: Um, I don't know about mostly.

  
  

### 00:58:14

  

edw: I would say that our demographic

Troy McDonald Kane: in the first couple months that we go live with this in the trading challenge.

edw: I mean maybe I mean I'm hoping we get a lot more adults in there to be honest. Um but I mean maybe I'm doing a poor job of describing it. Cody, what's your take?

Cody Haugen: I mean, you know, my take. I I think it is absolutely going to be an an engaging product. I understand what what Troy and and Jared are saying.

Brett StClair: It's

Cody Haugen: I mean, we will just based on our marketing, unless we start doing a lot more social media marketing to other demographics. Troy is right though. In this first iteration of the first couple months, all of our marketing efforts and uh user uh acquisition efforts have been towards colleges. So they are going to be 18 to 22 at least initially until we start doing more marketing efforts outside of that.

edw: Yeah.

Cody Haugen: Um I I just think if you offer any person whether it doesn't matter what age they are, if you do something and you have the chance to earn substantial amount of money, you're going to do that.

  
  

### 00:59:22

  

Cody Haugen: I mean, it's a tale as old as

Troy McDonald Kane: We don't disagree with that.

Cody Haugen: time.

Troy McDonald Kane: It's for how long though? That's the That's the question on the table.

Cody Haugen: Well, yeah, but the money is the question. You have to do it long to be substantially good at it to earn that money.

Troy McDonald Kane: I look at like fantasy sports as a better example than gambling because that's what I have the the most exposure

Cody Haugen: So,

Troy McDonald Kane: to. Like in fantasy sports if I feel like I have no shot of winning anymore or I feel like I I just kind of give up on those days. Like if I you know I look at my fantasy my league I'm like there's no way I'm going to win this week. I stop caring that week.

edw: Thank

Troy McDonald Kane: Even if I had even if I had the chance to earn money.

Cody Haugen: Yeah.

Troy McDonald Kane: I'm like, I'm not going to spend my time engaging in something that I don't have an opportunity to get a

  
  

### 00:59:57

  

edw: you.

Troy McDonald Kane: return on.

Cody Haugen: You can't trade that player mid game though, Troy.

Troy McDonald Kane: It's not about the player, it's about my team. Then I'm not going to go watch the other games that my players are on because my team just got blown out because one player

Cody Haugen: Yeah,

Troy McDonald Kane: caused

Cody Haugen: but you're but if you're trading one stock that you're getting bombed out on, you can go trade a different game at any point. Like if if your

Troy McDonald Kane: But the P&L is not off one game.

Cody Haugen: fantasy of course,

Troy McDonald Kane: It's off the entire

Cody Haugen: but your but your opportunity to trade a different game is substantially more

Troy McDonald Kane: day.

edw: right?

Cody Haugen: like your fantasy team, right? Like if your if your player is like you said doing bad, it's tanked your day. You can't trade that player or insert another player like you could with

edw: or a shortcut

Cody Haugen: our or short that player, but you couldn't insert a different player mid lineup because he's already played and he's

  
  

### 01:00:52

  

edw: player.

Cody Haugen: locked like you could insert a different game on our platform to go make that back or make your day better.

edw: Here's what I can tell

Cody Haugen: Well,

Troy McDonald Kane: I I disagree with that. I just want to make sure we're we're setting I feel like sometimes we're setting very high expectations here and

edw: you.

Troy McDonald Kane: we I just want to make sure that we're thinking through all the scenarios of what the actual proper viewership from a number and minutes perspective is and we're not just like black and white calculating this Come

edw: I don't think anyone's doing that.

Troy McDonald Kane: on.

edw: Um, what I would tell the group is what I've seen from our simulation run last time. Um granted it's a subset. Okay, it's like 600 people total. Um that like the average user was engagement was over 45 minutes and there was only there was a number of them who traded even though they weren't necessarily close to winning. There was only one person that made the money right that I distributed to and they still trended in. So but it it could have been the novelty too for that particular week that they had never seen it.

  
  

### 01:02:08

  

edw: Um, we'll find out, you know, we'll find out s soon enough how many people are going to use it and how many people are going to stay engaged. My issue too is when I hear like not a not a shot at Jared per se, but the younger age group clearly doesn't want to work. They don't want to invest any time. They don't want to read. They want free everything. They want the money. And then they want to be able to like like dilly around. I I don't even understand who the f*** these people are to be honest. Like that there's no responsibility to do anything. Everything seemingly is just like given to them and they got a safe animal near them to make it better in case they don't have a good day. Soap. Like, yeah. I mean, sure. I mean, I think there are going to be people who want to trade all the time and people who don't. We We'll find out soon enough how it works out. All right. What's Let's move on. What's next?

  
  

### 01:03:16

  

Cody Haugen: You're into your elgo call

Brett StClair: when I'll go call.

Cody Haugen: now.

edw: Yeah,

Brett StClair: I'm just wondering if we've got enough time. Shall we make a hit at it for 25 minutes and see where we get? So, just

edw: we're not going to get far in 25 minutes. What I propose for the algo call,

Brett StClair: some

edw: let me um let me pull together a I think we we should reschedu it either for tomorrow or Friday. Um I want to I want to have some time to run out to the bank today. I want to send you your money. uh by the way today.

Brett StClair: Thank you.

edw: So I just haven't had a chance to get to the bank.

Brett StClair: Thank

edw: I have a limit on what I can wire from my phone uh daily.

Brett StClair: you.

edw: So um I want to do that. I I would say let me come up with like a a a narrative description of the uh of the load balancing algorithm and then the market making algorithm because the market maker is going to buy some of the shares that aren't offered.

  
  

### 01:04:14

  

edw: um I'm sorry that aren't sold during the IPO so we at least have enough subscription for these shares to be tradable in the secondary market. Um I would say you know I could use a day more to have this construct anyway if if you could please allocate the time for

Brett StClair: Perfect.

edw: me.

Brett StClair: I'll reschedule for you.

Troy McDonald Kane: My recommendation is we do that Monday, Brett, if possible,

Brett StClair: Monday. Yeah.

Troy McDonald Kane: because I think we have a lot of stuff we need to get through today through Friday that I think will help make that a more productive

edw: Abs,

Brett StClair: Yeah.

Troy McDonald Kane: conversation on Monday.

Brett StClair: Perfect.

edw: absolutely.

Troy McDonald Kane: Yeah.

Brett StClair: Res

edw: Absolutely. Um, okay, cool. Um, and then Brett, when can you share that uh page so that we could start? I want to be able to start modeling for that.

Cody Haugen: I send it.

edw: Uh,

Brett StClair: in your in your darling.

Cody Haugen: I send it to you. We have it.

edw: we have it.

  
  

### 01:05:02

  

Cody Haugen: Yep,

Brett StClair: Yeah.

Cody Haugen: we have

edw: All right. Cool. Thank you.

Cody Haugen: it.

Brett StClair: Um, perfect. I've moved the input and I've put uh something in your diaries for CPN planning tomorrow

edw: Okay. Is there anything that anyone needs from me at the

Brett StClair: morning.

edw: moment? Okay. I'm going to sign off.

Brett StClair: Thank you.

edw: I'm

George Westbrook: Who's going to say it?

Brett StClair: Oh.

Troy McDonald Kane: I thought his son was today.

Brett StClair: Oh.

Troy McDonald Kane: Yeah.

edw: Yeah.

George Westbrook: Come on. Scream it.

Hasan Ahmed: Let's f****** go.

edw: Wow. That was beautifully done. All right,

Cody Haugen: Love it.

edw: cool.

George Westbrook: Speak to you soon.

edw: Um, all right.

Cody Haugen: All right.

Brett StClair: Awesome

edw: If if anyone needs anything,

George Westbrook: Have a good one.

Skye Capazorio: I'm

Brett StClair: guys.

edw: let me know and I will talk to you all soon. Okay.

Brett StClair: Wonderful.

Troy McDonald Kane: All right.

Kevin Murray: Thanks.

Brett StClair: Cheers guys.

Kevin Murray: Bye.

Troy McDonald Kane: Yes.

Brett StClair: Thank you.

edw: Thank you all.

George Westbrook: Epic.

Brett StClair: Cha chow.

George Westbrook: Bye-bye.

  
  

### Transcription ended after 01:06:01

  

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.

**