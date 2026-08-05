---
date: 2026-06-17
type: standup
status: extracted
extracted-to:
  - "[[digests/touchdowns-12-17-jun-2026]]"
  - "[[advertising/advertising]]"
  - "[[advertising/sub-components/programmatic-media-playbook/programmatic-media-playbook]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[ipo-module/ipo-module]]"
  - "[[trading/trading]]"
  - "[[challenge-website/challenge-website]]"
  - "[[education/education]]"
  - "[[components/components]]"
  - "[[architecture/open-questions]]"
---

## Post-Call Analysis

> Processed as part of the **[[digests/touchdowns-12-17-jun-2026|12–17 June touchdown sweep]]**.
>
> This call's headline is Brett's **programmatic media playbook**, extracted into a full sub-component: [[advertising/sub-components/programmatic-media-playbook/programmatic-media-playbook]] (source artifact `Inplay Outreach/ssp-priority-stack.html`).

| Finding | Destination | Action |
|---------|-------------|--------|
| **Programmatic media playbook** — SSP roster (18 ranked), AppLovin MAX architecture, 1-human + 9-AI-agent ad-ops, KPIs, lifecycle | [[advertising/advertising]] + new sub-component | New component + sub-component created |
| **SSP-first stack** — AppLovin MAX (ad server + mediator) day one, Kevel phase 2, no GAM; 8–12 SSPs; anchors AppLovin/AdMob/Liftoff/PubMatic | [[components/components]] (Advertising) | Cross-cutting reframed |
| **AI-agent ad-ops** at ~20% margin; impression model (~5/min, ~25B+/season; video ~$3.58 eCPM) | [[components/components]] / [[architecture/open-questions]] | Note + open-question row |
| **Onboarding flow locked** — email code → Persona → IPO page; **Apple dev account = blocker**; wallet allocation day-before | [[customer-onboarding/customer-onboarding]] | Update note |
| **"IPO draft" naming** + "What is an IPO draft?" Education link; **inventory visibility** (hide shares-remaining + straw buyer) | [[ipo-module/ipo-module]] / [[education/education]] / [[architecture/open-questions]] | Update notes + open-question row |
| **Market maker** — internal MM for IPO fill + liquidity; dummy IPO + sim events to test | [[trading/trading]] / [[architecture/open-questions]] | Note + open-question row |
| **Prize pool $21M + $4M flex = "up to $25M"** | [[challenge-website/challenge-website]] | Update note |
| Education session scheduled for 18 June | [[education/education]] | Folded into Education update |

**

Jun 17, 2026

## InPlay Digital TouchDown - Transcript

### 00:00:10

  

Edwin Johnson: Morning

Skye Capazorio: All

Brett StClair: Hello everybody.

Cody Haugen: Hello

Skye Capazorio: right.

Edwin Johnson: all.

Brett StClair: Hello. Fire up. For some reason, it's not connecting. Yes, it's not working.

Edwin Johnson: What?

Brett StClair: Still not working. Is it? Just that um Edwin, I saw your email by the way to um kettle

Edwin Johnson: Julian.

Brett StClair: guys. Julian, I don't think they're going to be able to answer all of that, but you know how fortuitous this is.

Edwin Johnson: Yeah.

Brett StClair: Off the back of Cody's request, I was thinking about all the things you're going to need to learn and know about programmatic media. So I have dumped all my knowledge and everything I can find all the ratings gradings I pretty much answered about 99% of your questions what I can see on first hits in a

Edwin Johnson: really.

Brett StClair: programmatic playbook for you. How fortuitous is that?

Edwin Johnson: Okay,

Brett StClair: I just had a feeling you're going to be wanting to know all of that, right?

Cody Haugen: That That's amazing,

  
  

### 00:01:44

  

Edwin Johnson: that's great.

Cody Haugen: Brett.

Edwin Johnson: Yeah,

Cody Haugen: Thank you.

Edwin Johnson: the more that I can get my head around it, the better, right?

Brett StClair: Yeah, because Yeah, I'll just quickly whip it up before we jump in. Just got to find it quickly. Where did I put it? Is it here? Yeah. And so I'm just going to publish it and I'll share it with you guys afterwards. Um, but just thought you're jumping into a world here that is super complicated and there's going to be lots of terminologies. And so I've put together this programmatic playbook for you. in there. We've done some research, cross analyzed to your vaults, what the best SSPs that you should be connecting to, how to approach them, timings, all that different kind of stuff, right? Because there's a lot going on. An architecture of the type of technology, the operating models, and then I've built just like a bunch of cards. So, you can go have a look at the analysis on all the different SSPs.

  
  

### 00:02:55

  

Brett StClair: Um, here's a quick priority stack. Um, so if we're going SSP first, it might be worthwhile not going Keville right away and going with something like Apploven Max, who's an SSP and an ad server. And what you do is um, they literally allow you just to plug in all the other SSPs into them and they serve the ad directly. And when you start doing lots of direct buys, then you plug apploving into Kevl and then Keville will manage everything. Um, just a thought. I'm going to go check on pricing and all that kind of stuff, but I'm pretty sure it's a fraction of what a Keville is. Um then it kind of how I've kind of ranked everything for you guys was to get a sense of the ease of registration most important because some of these things can take three to four months to get registered on and you need traffic profiles you need to go through compliance you need to go through a whole lot of stuff inventory availability and then value and the premium nature um and so I've kind of built out this matrix for you um a bunch of these like ADM Mob, weirdly enough,

  
  

### 00:04:13

  

Edwin Johnson: Oh,

Brett StClair: ranked top and I think it's cuz it's mobile only. So that's great. I don't know if you guys know, I used to be the country manager of ADM Mob, so I know the guys backwards know all the people there. Um, bunch of my bosses ended up at Smato, um, Ad Colony, um, a whole lot of guys here and in Moby. Um, and so what I've tried to do is kind of also give you kind of a frame of reference. So when you've got all those questions and you want to learn about it, kind of deeper explanations. So I'm not going to go into everything. This is kind of bedtime reading. um kind of why would you go multiple

Edwin Johnson: I'm gonna read it. I'm gonna read it right after this call because this is important.

Brett StClair: exchanges yeah it talks about the optimal mixes it gives you the pros and cons of having too little too little too too much I try to lay out the architecture you know so when the the app fires off an ad slot what then happens how does it get loaded how does it then pull the different SSPs where does the SSP get its ads from?

  
  

### 00:05:24

  

Brett StClair: Well, it gets it from DSPs. So, you mentioned yesterday trade desk, Google, uh, Amazon's DSP, all those kind of guys. These are the guys where the the actual media buyers will buy from. Omnicom will buy from there. WPP will buy in there. That's their interface into this world. Our interface is the SSP, this the the sell side. DSP is the demand side. Um, and really to try and give you as much information as possible, some tips where I can, uh, give you a sense on on operating models, costings, traditional what it would usually cost, um, how everything kind of works through like we're suggesting you don't you don't hire people. We h we get one person and a aentic workforce running this. Um, what does that tech stack look like? Um, what do you measure? What is the point of an ADM MOPS ad ops? So, you need an ad ops, some kind of adops capability to run it. What are they trying to do?

  
  

### 00:06:27

  

Brett StClair: Well, they're trying to manage billions of ad units, right? And they're trying to get the most active value out of bidders, better fill rates. And then what I've tried to do is give you actual examples of what a KPI would look like for an adops team. Right? Step one, take an eCPM, push it up to as high as you can go. Take a net eCPM on uh homepage, push them up. Take your full rate, push it up. And then an explanation on how people do it. This part you probably don't need to go into too much detail.

Edwin Johnson: This is fantastic.

Brett StClair: This is really This is

Edwin Johnson: Jeez Louise, you and your little f****** AI team.

Brett StClair: the Yeah,

Edwin Johnson: You guys are amazing.

Brett StClair: it's a mixture of AI and also just making sure we tell you that you you understand like because AI just

Edwin Johnson: No,

Brett StClair: goes right and and so we just want to make sure everything's

Edwin Johnson: Tom.

Brett StClair: clear. We we've given you some ideas on how what the types of AI agents we're going to build the workforce to be able to manage it.

  
  

### 00:07:29

  

Brett StClair: Um, don't worry about that. Tooling stack, you don't need to worry about too much. How we'll integrate into Kevl in phase two because I just don't think you need to do Kevl right now because even if you have one premium placement, we can actually use house ads on max to fill it and that doesn't cost any money to serve those. So, you know, that's a bonus. Um,

Edwin Johnson: Right.

Brett StClair: then what I've tried to do is then list. So when you start thinking why why should we be going with this type of anchor stack why apploving you know what is the onboarding what are the commercials uh what are the net eCPMs that you can get from it what are the types of inventory that they support their strengths their weaknesses and I've essentially done it for pretty much the world's SSPs and then from the top we've ranked them all so a lot here I'm going to publish I'm going to send it to you afterwards, Cody. That's why I was very much like uh yes, we need to get cracking.

  
  

### 00:08:37

  

Cody Haugen: Yeah. No, this is amazing,

Brett StClair: But there's like I I need you guys to walk a journey with

Cody Haugen: Brett.

Brett StClair: me on on how to do it.

Cody Haugen: Yeah,

Brett StClair: And this is going to be the plan.

Cody Haugen: happy to

Brett StClair: So,

Edwin Johnson: So you're

Brett StClair: you see everything that says anchor, those are the ones that we need to get cracking in the next week.

Edwin Johnson: Yeah.

Brett StClair: It'll take about a week to get on boarded to do everything, but we need to do small little things like um we need to I I'll need to register with a uh uh call it a Novo at InPlay. So, we want to do this all on your domain. We want to make sure it's registered on your business. We want to make sure that all the payments go to your accounts. You'll see like different SSPs pay different terms. Some do immediately and immediately on SSP terms is at the end of the month. Some do end of the month plus 30 days.

  
  

### 00:09:27

  

Brett StClair: Some do end of the month plus 90 days. some actually have a poor reputation of even paying. Um, so you've got to like I've tried to grade it all on that. Um, and make sure they have the inventory, have the inventory type, have the type of eCPM, have MCP servers that we can connect into and do all that kind of work. So to answer your question yesterday, these are the four SSPs and then we'll use Apploving

Edwin Johnson: Cool.

Brett StClair: Max as our ad server initially. It'll be way cheaper than doing a

Edwin Johnson: Um, and then,

Brett StClair: kel.

Edwin Johnson: you know, as you're still trying to uh get your boy Wayne to whittle out some wood for us, um, he would buy through the through these uh ad places,

Brett StClair: Meeting's been set up.

Edwin Johnson: right?

Brett StClair: So he won't buy here. He'll buy a DSP level.

Edwin Johnson: at the uh the other one.

Brett StClair: Yeah. So where do we get DSPs? way I laid out the DSP world

  
  

### 00:10:24

  

Edwin Johnson: Yeah.

Brett StClair: uh further down the essentially the Amazon DSP, the uh Trade Desk DSP, the Google DV 360 DSP. Um and essentially what they are, they're like ad service from their site. So they'll run campaigns and then they're targeting they'll have audiences and then they target audiences. They can also target individual sites but remember there are a trillion websites you can target. So they go audience first and then a website to optimize. And so when we talking to any of Wayne's guys, they'll go what are they trying to achieve? What is the audience? and then they'll actually pick you out. And then when someone does a direct buy like that, we'll set the eCPM differently. Um, and so this is all about you start at a fill rate of 30%. Because I', in my life, I've never seen a fill rate start on a new site more than 30%. Then you're optimizing. So to give you a sense on optimizing, where did I just working through this? Working through it now.

  
  

### 00:11:45

  

Brett StClair: Oh, that's the priority stack. Um, there we go. Yeah. So, if you look at an optimize, what does an ad ops team do over here? Sorry, you can't really see the thing that he's put it there. Um, every 15 minutes you need to be going in checking your distribution tail, modifying the density curves. You check your SSP positions, see if they've got cap outs or if there's just no inventory or demand coming from their side, swap them out. You need a pre-warm, raise floors, do all that kind of basics. Um, and this is just every 15 minutes.

Edwin Johnson: And you're going to build AI agents to do

Brett StClair: We'll do a mixture of human and AI.

Edwin Johnson: that.

Brett StClair: So AI can probably So I'll tell you what AI can do. So I was like, how much can we make AI do everything? So what AI can do in the optimization side, it can do a decision loop every 15 minutes and it can play around with your flaws.

  
  

### 00:12:49

  

Brett StClair: So your flaws are saying I'm not going to take any other uh demand less than this price. Then you see your fill rate falling through the floor. Then you're like, "f*** it. No, no, no. I'll take for less." Then the fill rates come back up.

Edwin Johnson: Right.

Brett StClair: Why? Because demand's now coming. People are starting to run ad campaigns. So then you see you're getting a high fill rate. Then you go, "f*** it. I'm going to lift my floor again and then see if I can maintain a full rate at a higher rate. So, and it's like a trading desk, you know, you're like you're manipulating non-stop. So, AI can do that component, but like what it can't do are literally playing around with the actual direct SSP integration connections, monitoring, all that kind of output. It's a human kind of thing. There's no MCP servers and stuff. So, I've tried to kind of map it all out. We've just spent the today really putting it together for you guys.

  
  

### 00:13:40

  

Brett StClair: Try to make it digestible. Try to make it fun to read. I know it's and try to make it more like and it's just funny you sent that. It's not funny. You It's a brilliant coincidence because I'm glad you're thinking like that, Ed. Um, you have to know all that stuff.

Edwin Johnson: Sure.

Brett StClair: Um, I don't think the Keville guys might come back and answer two questions. they'll be like, "Yeah, your problem." Um, but at least you've got this information now.

Edwin Johnson: Okay.

Brett StClair: Cool. So, let's jump into it.

Edwin Johnson: Cool.

Cody Haugen: So sorry Brett one question before you before you move forward there. So um obviously Novo team is building the agentic AIS to help us out there.

Brett StClair: Yeah.

Cody Haugen: Um option A is we you know with existing team we learn how to do this the best of our capability. Um monitoring things every 15 minutes like obviously is a lot. Um, if we so choose to go option B,

  
  

### 00:14:35

  

Brett StClair: Now you need to build an

Cody Haugen: are you Yeah. Are you able to warm intro us into someone who has experience obviously

Brett StClair: Yeah.

Cody Haugen: with SSPs, some from someone from your previous life that specializes in this that we potentially could hire, contract with, I mean, whatever it may be to to optimize this at the highest level. I mean, if we're monitoring things and changing things every 15 minutes on a Sunday, I mean, there's a lot to be done,

Brett StClair: Yeah. So, there's a couple of ways we can handle it.

Cody Haugen: obviously.

Brett StClair: Um, just I think the very first time we started engaging, I was going to provide you guys with a full team, right? It was like three or four people to do this. Um, now we're going to do the majority with an agent workforce.

Cody Haugen: All

Brett StClair: We can provide you guys with a campaign manager, get them up to speed because this is like a full-time role.

Cody Haugen: right.

Brett StClair: This is not something you've got to hire somebody.

  
  

### 00:15:32

  

Cody Haugen: Yeah. Yeah. I mean at sport at sport radar it was a 10 to 15 person team.

Brett StClair: You've got to train them.

Cody Haugen: Yeah.

Brett StClair: Yeah. They're big, right? That's why like, you know, if you're running a million users,

Cody Haugen: Yeah.

Brett StClair: you're looking at between four and five on a team. That gets bloody expensive. Whereas we're going, hm, we got AI workforces. f*** it. Let's try do as much of the heavy lift with that and get that from four to five down

Cody Haugen: Yeah.

Brett StClair: to one person. And then we train them not necessarily, you know, you you these SSP guys are expensive. So you want to get uh someone who's open to learning how to use, report, and manage these AI workforces. Um, so we can do that for you guys. And so we've been I'm trying to work out costings. Um,

Cody Haugen: Yeah.

Brett StClair: can we do it within the 20%. That's kind of what's running through my mind.

  
  

### 00:16:27

  

Brett StClair: And so like in your inventory as you plug into these guys, everyone's taking a cut and you're going to see an end result. And it's like where is that? What's possible? What's not possible? And on a 20% cut, it means how much risk are we willing to carry getting a person on board for what period of time, how many impressions, all that kind of stuff. So all those numbers need to be run as well. Um because need to make sure that you're getting the impressions to cover the the costs of of someone like this. Um so whole lot of things we got to think about, but you're on the right course. This is not a It's hard. This stuff's hard. Eh, it's a different world. You know what? I'd probably trust an Edwin actually to figure out it with your trading background. Funny enough, it's that kind of

Edwin Johnson: You're the first guy that's ever trusted me, Brad.

Brett StClair: mind.

Edwin Johnson: I appreciate that.

  
  

### 00:17:23

  

Cody Haugen: That's

Brett StClair: I hope many women have trusted you, Edward.

Edwin Johnson: Mistakenly so.

Brett StClair: Um, so please have a read through it because it'll arm you guys up with the right knowledge that you need to know and let's have some further chats. Um,

Cody Haugen: Yeah, absolutely.

Brett StClair: and then what I'm going to start start the process if you can get me a

Cody Haugen: We'll do that today.

Brett StClair: nooinplay global.com email and I'll get it all registered up, get all the processes going because even an ADM mob um, even with my connections, right? I'm pretty sure two or three guys are still left in in the ADM Mob platform that I used to work with. Um, I could probably expediate it to 2 3 days. Um, so we want to get the process, we want to kind of get something up and running. A lot of the SSPs are going to be worse than the agencies. They're going to be show me your inventory figures first. And so that's why I've deprioritized them. And they are all the ones that are doing premium inventory.

  
  

### 00:18:30

  

Brett StClair: So, premium inventory means more brand friendly, uh, richer ad units, and what that does is it improves your full rate at a better eCPM. So, some of them can push the eCPMs all the way up to nearing $10, $11. So, everyone wants to get on there, but they're snooty little b******. Um, it it can take six months to earn favor and have proof points and everything with these more premium SSPs. Um, the probably the most premium SSP that I got contacts in is probably SmartOto. Um, and I know the VP of Europe and so he could probably fast track us in there. Um, but again, it's more of a plan. You need to have between eight and 12 SSPs. You need to segregate out your inventory. You need to have back full on certain SSPs. You can't have too many, otherwise you get too much latency pulling through. So you can picture an ad needs to be served in under 50 milliseconds. Nope, not served. Another SSP tries, another SSP tries, and then you start getting to like half a second a second to fill an ad unit, and that's just a fail.

  
  

### 00:19:40

  

Brett StClair: You you start your eCPM's tank. Um, so it's just getting all that balance right, getting all that configuration right. And remember, they're also running tech solutions. They're also breaking non-stop. They're doing real time on trillions of impressions literally a day.

Edwin Johnson: Sure.

Brett StClair: I mean, the scale of these guys, it's it's mind-blowing because they're servicing a whole planet um of inventory. So, it's just it's insane how big it

Edwin Johnson: And then when you're talking about this inventory,

Brett StClair: is.

Edwin Johnson: you know, there's different types, right? So you have video, you have Right. And um I think we want to try to have both because in our limited knowledge and research like we could get up to, you know, maybe $3.58 coming out of the box for video. Um

Brett StClair: You can even take like we should be in the mind of as you're going through and wanting the whole goal here is

Edwin Johnson: so

Brett StClair: full rate eCPM up and maintain that's the

Edwin Johnson: well, here's the thing, Brett.

  
  

### 00:20:40

  

Brett StClair: goal.

Edwin Johnson: I'll fill for cheap because I I don't like we did some modeling yesterday in terms of you know how many impressions per minute that a user can get. Okay. And we've we factored in around 20 if you're toggling around the different areas. And even if you're staying just on trade or just on chat, you know, 20 a minute is what we were factoring. You know, again,

Brett StClair: That sounds That sounds like a lot,

Edwin Johnson: not everyone only.

Brett StClair: by the way.

Edwin Johnson: Sure. Sure. Um,

Brett StClair: Like that sounds a lot on a minute basis.

Edwin Johnson: what sounds like a little to you? What sounds like a

Brett StClair: So, so what's happening in a minute is how you got to think about it.

Edwin Johnson: meaning

Brett StClair: So, what is a user doing? So, and and I've also been thinking about this going I think we need to be looking at inventory. A user goes onto the main kind of homepage. What are they doing?

  
  

### 00:21:36

  

Brett StClair: Well, the first thing they're going to do is spend some time reading what's on the homepage, right? They pause. They look, they might consume 10, 15 seconds. They're consuming one ad banner at the top. They scroll down to the next level. There's probably five, another 10 seconds where they're looking at it. They might be a little bit faster. They're getting to lesser information. They pass through one uh native ad unit. So, that's two ad units. They're into the 30 second, 40 second kind of space. They now get down to the bottom. They might click into another page yet. Maybe they're going to spend a minute on that first page. They've only seen two ad units. And so you've got to think about the user and how they browse through it and where the ad exposure comes from. And so like I've been thinking about it. I'm I'm also going to build a bit of a model because if we going to help you on the on the um programmatic side, need to make sure these like this is now these guys are pinpoint.

  
  

### 00:22:37

  

Brett StClair: There's no brush stroke stuff here.

Edwin Johnson: Well,

Brett StClair: You need to

Edwin Johnson: I I get it. I mean, what you just described on the homepage,

Brett StClair: get

Edwin Johnson: no one's going to take uh a minute to check their P&L, check their position, and look at two or three ads. That That's going to go much quicker because when you log into the app, Go

Brett StClair: Yeah. Can I sorry I just want to interrupt you.

Edwin Johnson: ahead.

Brett StClair: I want you to think about four different user types. So the difficulty we all have.

Edwin Johnson: I've got a few more than four.

Brett StClair: Okay.

Edwin Johnson: That's so my inside.

Brett StClair: Yeah. So that's good.

Edwin Johnson: Yeah. So,

Brett StClair: So like you and Cody are the super users,

Edwin Johnson: let's

Brett StClair: right? So you you've got to put yourself in that top 5%.

Edwin Johnson: sure.

Brett StClair: And uh Max is your freshman.

Edwin Johnson: So, are you suggesting that we should put another um territory for max a mirror

  
  

### 00:23:24

  

Brett StClair: He's going to very bit.

Edwin Johnson: page?

Brett StClair: Should we just call it

Edwin Johnson: Just the Max's mirror so he can see himself with an ad behind

Brett StClair: Max?

Edwin Johnson: it.

Max Kingaby: I mean, your user count would probably go up quite

Edwin Johnson: I I mean I would subscribe to that page,

Max Kingaby: quickly.

Edwin Johnson: Max. Gorgeous man.

Brett StClair: But yeah,

Edwin Johnson: Um No,

Brett StClair: so think of your users as intensity of

Edwin Johnson: I I understand what you're saying.

Brett StClair: usage.

Edwin Johnson: But so Cody and I are the only ones who are probably degenerate gamblers. If he was a trader, he'd be a degenerate trader.

Brett StClair: So,

Edwin Johnson: Okay.

Brett StClair: do we call do we label that trade degenerate?

Edwin Johnson: the kind of clients that we're going to have are going to be regens. Yes. That's that's a fact. Okay.

Brett StClair: That's

Cody Haugen: Exactly, Brad.

Edwin Johnson: And but

Cody Haugen: And I would say not only is it a fact,

Brett StClair: beautiful.

Cody Haugen: I'd say it's a majority of our

  
  

### 00:24:16

  

Edwin Johnson: Yes. And so what they're going to do is they're going to log in and hopefully we can get a splash page,

Cody Haugen: users.

Edwin Johnson: right? So what we'll have that homepage. So that's number one. Your title sponsor gets it. You get to the homepage. It'll take me about 3 seconds to check my positions and my P&L. And then the next button I'm going to hit is either discover so I can see the teams or trade. And I'm going to go right into trading. And when you make these trades, okay, you're going to go, you know, you you make a trade in, you make a trade out, bang, bang, bang. You now you have two trade confirmation pages, right? So let's take it let's cut ours in a quarter, okay? from 20 to five a minute which is I think very low. Okay, given how dynamic the pricing works. If this was a Instagram scroll, I would tend to agree with you more. But this is hyper intense.

  
  

### 00:25:15

  

Edwin Johnson: Okay, with the moment that there's actual money on the line, people behave really differently. Okay. So, um you know, based on that and and and frankly, we've we've lowered our user flow uh back and forth uh so to just 10,000 people actively trading a game, okay, for approximately say two two hours, two and a half hours. We've done one at three hours, but you know, let's do one at two hours. it still generates around $50 million even at half your rate. Okay. At 20 um even at a dollar whatever you said 47 or something is what I plugged in. You know we're expecting 25 billion plus impressions over the course of this this four

Brett StClair: Yeah.

Edwin Johnson: months. There's there's a lot of money at $147. Unless I'm missing how this whole uh scheme works. You know, we're we're going to be pushing at 10,000 massive numbers of impressions.

Brett StClair: Um, yeah, I I I agree. I think you are going to be hitting big impressions like part of me.

  
  

### 00:26:38

  

Brett StClair: Yeah, it's good to understand that, right? The kind of user behavior that's going to be important.

Edwin Johnson: Yeah. And so it look there there are going to be users who aren't going to be active traders. Let's say it's Max and Max doesn't trade a ton but he likes to go in and chitchat the other d******* in there and bang, you know, you're still getting quite a bit of of opportunity for people to stay engaged. The research part of this is going to be incredible as well. So like you know the trading is one aspect. I mean I know how I'm going to trade or I would trade it. I would be on every bid and every offer and I everything that happened in every game I would know, you know, like it happened to me, you know, in my life. It it's a great memory. Like I can still tell you trading days that I've had from 12 years ago pretty much the whole day, you know,

Brett StClair: No.

Edwin Johnson: and it's like you don't you remember that s***, especially if it was a big financial impact one way or the other.

  
  

### 00:27:32

  

Edwin Johnson: So that that that's the difference is it's like that the the the competition is what compels the eyeballs. If the money's there for them to earn, they're going to trade it. If it goes to like a fizzy wicket b******* nothing, you know, you get a a star, no one's going to trade it. But if there's actual cash and the cash is meaningful, people will stay and trade and they'll do it all day long.

Brett StClair: Yeah, I agree. I agree. So, on that note, do you guys want to see a demo?

Edwin Johnson: Yeah, f****** ain't got demo on my ass.

Brett StClair: It's always fun. Right now we're talking user experience. f*** it. Let's get into it. And on that note,

Edwin Johnson: Yes.

Brett StClair: I'd like to present

Hasan Mohammed Ahmed: Hello.

Edwin Johnson: There is Hassan's That group

Hasan Mohammed Ahmed: And my internet's playing up. Give me a second. Um, hello. Can everyone hear me and see? Yeah, cuz cuz I think right now I'm having a bit of like internet problems, but

  
  

### 00:28:59

  

Cody Haugen: Yeah, we can see it.

Hasan Mohammed Ahmed: so Okay, so um I'm going to start off with the actual onboarding flow and then how like it looks now as in cuz I think I mean I think like in a earlier I think touchdown it was like um I would say the quite the basic and so as you opened there um the the um um actually the app itself like this will be the like a starting screen and so like I mean I mean like I think it looks um um I mean I'll say like quite like enticing for like a user as

Edwin Johnson: I would say so I don't Yeah,

Hasan Mohammed Ahmed: the day.

Edwin Johnson: that I mean the only thing is we don't need baseball.

Hasan Mohammed Ahmed: So after this if you want to either create an account.

Edwin Johnson: Yeah, the the the two athletes that are baseball players or however many we need those out.

Hasan Mohammed Ahmed: Yeah.

Edwin Johnson: That's all. That may be instead of a baseball player,

Hasan Mohammed Ahmed: Okay.

Edwin Johnson: that may be me trying to collect on these SSPs with a bat.

  
  

### 00:30:00

  

Hasan Mohammed Ahmed: Yeah.

Edwin Johnson: They don't pay

Cody Haugen: Uh, do we want to make sure that that wording says I mean you're s***.

Edwin Johnson: up

Cody Haugen: Yeah.

Edwin Johnson: to

Cody Haugen: Up to 25 million just to just to make sure.

Hasan Mohammed Ahmed: Yeah. Yeah.

Edwin Johnson: It looks awesome though.

Cody Haugen: It looks great

Hasan Mohammed Ahmed: Sure. Yeah. And so yeah um after this if you want to create an account um I did add a few um extra steps in. So um this is the um standard that um I said the process that I should like um I mean um I said ages ago. So I'm just going to get quick sign in uh Phil. Um I don't have a code on me at the moment but so as soon as you create the like initial account like it will will actually email you uh a um actual code. And what I'll do is I'll get the actual email up as well just to show you guys. Um I might need to change how I share my screen.

  
  

### 00:31:15

  

Hasan Mohammed Ahmed: Um I do this if I share the screen here quickly. So, as soon as you are emo um um as you can see here like it will just like they hand you like a um actual code or if you want to click a button and so if you're on actual the phone like what you would do is like um after they click this and then it will um do the um actually the autofill. So for now I just uh copy this code in and then after that it will be the standard like the ID check. Um I think at the moment I will not do it. screen. There's an Oh, let me Oh, yeah. Let me switch back um a bit. Yeah. So, after you do the actual the email check, it will do the standard like ID check and stuff and then it will throw you into the app. Um I will not do that at the moment because it's like a bit long and I don't have like an camera on this, but I do have an account that's um that is already signed in. So let me get uh do that and so and so here um as you can see over here it will be be have a new um the IPO page.

  
  

### 00:32:54

  

Hasan Mohammed Ahmed: So um as you open it as a actually the new user that it will give you this

Edwin Johnson: Well, that's cool. f***. And you guys do really good work.

George Westbrook: So I think he's he's just had an issue with his network. So he's just just coming back now.

Edwin Johnson: Looks awesome.

Hasan Mohammed Ahmed: There we go. Okay. So, I just guess and so um cuz like it's like the basic like um I said the swiping. So if you want to think swipe to each team like it would be like quite simple and if you want to trade as well it's just I think swipe up or down. So I can also demonstrate that here and and and um I mean also like if you don't want to swipe and you want to use that individual as individual then buttons as well it's also there as an option but so if you want to swipe between each team and then on each um I'll say the card it would have um I'll say the basic stats and then if you want to click into it you can either think swipe up or down to view.

  
  

### 00:34:13

  

Hasan Mohammed Ahmed: So, if I swipe up and then we can see here like like it will have the more um I say that um I'll say like the um um actual um stats for um each individual team cuz I say at the moment it's all um um I say the placeholder in data. So like this that isn't actual data yet. Um yeah, and then also in here if you want to swipe um it's also possible and then also if you want to buy as well cuz I know for the actual IPO the um actual then price like is going to be like I think set price until the um IPO is over and so like this is unable edited and then if you want to change actual quantity as That's also

Edwin Johnson: Right. And on on the IPO,

Hasan Mohammed Ahmed: possible.

Edwin Johnson: there should only be a buy button. There's no sell button. Right. So, you got that perfect

Hasan Mohammed Ahmed: Yeah, you can change. Yeah. Yeah, it's only by.

  
  

### 00:35:15

  

Hasan Mohammed Ahmed: So like if I also go to the other view and so if you don't want to swipe and and if you just want a basic like view of each team like as a list, it's also possible here. You can sort I think um as an AFC NFC.

Edwin Johnson: Cool.

Hasan Mohammed Ahmed: And then if you go to NCAA as well, it has each of the um individual leagues.

Edwin Johnson: This is sick. Um,

Hasan Mohammed Ahmed: And then

Edwin Johnson: real quick, uh, just so it's noted for the the conversation, the term the draft board,

Hasan Mohammed Ahmed: yeah,

Edwin Johnson: I don't want it. It's too close to a fantasy draft.

Hasan Mohammed Ahmed: okay.

Edwin Johnson: We want to call that the IPO board or something like that.

Hasan Mohammed Ahmed: Yeah.

Edwin Johnson: Troy, you got anything a name?

Troy McDonald Kane: I mean, I wanted to call it the inplay draft,

Edwin Johnson: There you go.

Troy McDonald Kane: but you don't like the you don't like that the word draft at all

Edwin Johnson: Uh, well,

Troy McDonald Kane: or

  
  

### 00:36:01

  

Edwin Johnson: draft reminds me of fantasy, right? I mean, I'm lately my life is a fantasy gone wild.

Troy McDonald Kane: Yeah.

Edwin Johnson: Um, and not in a good way. Um, so I don't know, Cody, what do you think?

Kevin Murray: What about inplay IPO?

Edwin Johnson: I love I love inplay IPO. I mean, some people may not know what that means yet, right? But, you know, hopefully they'll they'll go through the learning part and figure it

Troy McDonald Kane: See, I think the reason why I like draft and I know where you're coming from with it being fantasy is that it drives more interest

Edwin Johnson: out.

Troy McDonald Kane: to pick up teams or buy into the initial offering. I think if I think a lot of people don't still understand what IPOs are or like what that actually means,

Edwin Johnson: No, I don't.

Troy McDonald Kane: but calling it a draft,

Edwin Johnson: Yeah.

Troy McDonald Kane: I think it it drives people to come in and want to buy into multiple teams, not just one. Like they are picking fantasy players.

  
  

### 00:36:59

  

Troy McDonald Kane: Like I I don't think that's a bad thing. I think that's a good thing because it's association to the type of demographic we're going

Edwin Johnson: Yeah. Cody, do you have any

Troy McDonald Kane: after.

Cody Haugen: Uh yeah,

Edwin Johnson: thoughts?

Cody Haugen: so I I I do like what Troyy's saying. I mean, the association to get them in, they quickly realize it's not a fantasy draft. Um and then they can learn from there. Uh which is a which is obviously the key is to get them in. Um if we're thinking or spitballing, sorry, just missed the beginning of that, but if we're spitballing on different names, um g give me some time. I'll figure out some or I'll come up with some other ideas.

Edwin Johnson: How about this? How about can we do this uh team uh Novo team? Uh I like the IPO draft. That can work provided to the right of where it says the IPO draft. There's a button that says what is an IPO draft?

  
  

### 00:37:54

  

Edwin Johnson: And they can click it and they could find out. They go right into the education center and we could have something written up on what the IPO draft is.

Troy McDonald Kane: I like that. No, I like that idea. It goes into the educational part of it,

Edwin Johnson: Thoughts.

Troy McDonald Kane: too, to help educate like what is an IPO, why people buy into IPOs, what you're getting when you put on a position in an IPO.

Edwin Johnson: Yeah. Okay. Is that doable team Novo?

Cody Haugen: Hey,

Edwin Johnson: Cool. All right. Yeah. Awesome.

Hasan Mohammed Ahmed: Yeah.

Edwin Johnson: Hassan,

Hasan Mohammed Ahmed: Yeah. And then um if

Edwin Johnson: this is this is sick, bro. This is really really

Hasan Mohammed Ahmed: I Yeah.

Cody Haugen: What's it called?

Edwin Johnson: good.

Hasan Mohammed Ahmed: I mean to be fair like I'll say at the moment it's only like an initial like hit on the um um um I'll say on the actual um on the actual IPO page and then like I will be adding to it and just to make it easier if you want to buy teams.

  
  

### 00:38:49

  

Hasan Mohammed Ahmed: So, I did add an extra thing here. If you want to swipe to buy and so if you want to quickly just go for your team, do that. Or if you scroll down,

Edwin Johnson: Yeah.

Hasan Mohammed Ahmed: let's say you want to buy one here or I mean you

Edwin Johnson: Hey, Troy. Yeah, Troy. Real quick,

Hasan Mohammed Ahmed: swipe

Edwin Johnson: as they're showing this,

Troy McDonald Kane: Yeah.

Edwin Johnson: do we need anything in there? And there's there's a question not not I'm I'm not saying um that

Troy McDonald Kane: Yeah.

Edwin Johnson: says how many shares are left

Troy McDonald Kane: Yes, we do. We need We need There to be a

Edwin Johnson: we or don't we because what if our IPO uh

Troy McDonald Kane: countdown.

Edwin Johnson: certain teams flop and we don't sell much. I'm going to have to create a straw buyer um that will come in and buy part of this stuff, right? like if if they're not available, then we're going to have to have the market maker buy, you know, some of the stuff that it can build an inventory with or something because I don't want to seem like, you know, um,

  
  

### 00:39:48

  

Troy McDonald Kane: Yeah.

Edwin Johnson: University of Arizona football team has zero IPO shares sold.

Troy McDonald Kane: Yeah, I see what you're saying. But I think it also you want there to be some countdown to what cuz we we don't want over buying of a partic a team as well. Well, if we go I mean, I know we're going to have the limit of 5 million, but I think

Edwin Johnson: Well, we're only going to sell 4 million of those shares. What might be interesting, Troy, is that we don't put any kind of like,

Troy McDonald Kane: it

Edwin Johnson: you know, uh, total that's available left. only as it gets close to being closed, there'll be like maybe we could have a trigger that says, you know, as soon as there's only, you know, 500,000 shares left, we have that posted or something, but we don't say how many are sold.

Troy McDonald Kane: Yeah.

Edwin Johnson: Um, just so that it doesn't look weak.

Troy McDonald Kane: Yeah.

Edwin Johnson: Any feedback from the team on that?

Cody Haugen: Yeah. I mean, what if you just showed it in percentages instead of actual numbers?

  
  

### 00:40:57

  

Edwin Johnson: No, because what if it's 0%. What I'm saying is as we get as we get close to the line,

Cody Haugen: Well,

Edwin Johnson: um, you know, and Brett, this is another thing I got to talk to you and George about, um, I have to start building my market maker. And, you know, we we got to figure out how to put that in, right? And, you know, there's going to be some wiggle that we need to do pretty quickly so that we can test some of this data. I'd like to do a like a at least one dummy IPO and then you know have the market maker operate for a couple you know events beforehand even if they're simulated events right we just want to know that the orders are being processed

Brett StClair: Yeah.

Edwin Johnson: properly

Brett StClair: Should we set up a another kind of component section to work it through, gather requirements, thrash out ideas, figure out how we can solve the problem?

Edwin Johnson: yes

Brett StClair: maybe take an a 90minut slot. Um I'll find some time in the diaries maybe Monday or Tuesday next week if that's cool.

  
  

### 00:42:00

  

Edwin Johnson: That's great. Yeah.

Brett StClair: Perfect.

Edwin Johnson: Every time I see your work, Hassan, George, Max, I'm I'm just It's so awesome and really really good

Brett StClair: It's good.

Edwin Johnson: stuff.

Brett StClair: Um have you got the referral still to go through there?

Hasan Mohammed Ahmed: Um I mean like I think spoke about like I mean I said ages ago. I mean I can also they show it here as well. Um, I quickly have it. And so if you go to like invite friends for example, like it will have you with the QR code

Brett StClair: Sorry.

Edwin Johnson: It's great.

Hasan Mohammed Ahmed: cuz I said like also be here too.

Brett StClair: Super simple,

Edwin Johnson: So this IP this IPO button um you know

Brett StClair: right?

Hasan Mohammed Ahmed: Yeah.

Edwin Johnson: the IPOs are going to happen you know once during the season. Do we are we sure we want the IPO button you like on that core

Brett StClair: This is going to be your pre-launch,

Edwin Johnson: bottom?

Brett StClair: right, version of the app.

  
  

### 00:43:06

  

Brett StClair: So,

George Westbrook: Sorry.

Brett StClair: all we're not going to show everything on that. Once it starts trading,

Hasan Mohammed Ahmed: What's station?

Brett StClair: that'll shift to your more section and then the standard format will click through because

Edwin Johnson: Oh wow. Awesome.

Brett StClair: you there's a whole lot of stuff we just don't want to show pre-launch,

Edwin Johnson: That's great.

Brett StClair: you know,

Edwin Johnson: Right. Right.

Brett StClair: like like we talking about the trade and all that stuff.

Edwin Johnson: Yeah. This is really good.

Brett StClair: So, um, we've got you've got the wallets set up, the trading wallets, ean, have you started looking at it? Who set that up there? I think it was Troy. Thank you. um uh for getting that arranged and we're going to start working on that next, right? Or I make an assumption you two.

George Westbrook: Yeah. No,

Brett StClair: Yeah.

George Westbrook: it will be. it the the thing is it's not as I know it seems like obviously an urgent thing but the actual process is it's something that we could we're not going to do this but in theory the day before the trading starts we just allocate an ID well the wallet ID to a user and then it's then it's done um we're not going to do that but it's cuz it's it's just feeding a bit of data to um tZERO and then they give us the wallet which we already have the IDs for cuz they've already been

  
  

### 00:44:21

  

George Westbrook: created. It's just a a quick allocation

Brett StClair: Can we get ready to push a version to the prototype

Troy McDonald Kane: What's

Brett StClair: space for the guys to play with on all your work? Is that possible, James?

Troy McDonald Kane: up?

George Westbrook: Yes, that probably by Monday.

Brett StClair: probably

George Westbrook: Monday or

Brett StClair: Monday.

George Westbrook: Tuesday.

Edwin Johnson: What is our target that we want to have this app in the store? When when are we hoping to have it

George Westbrook: It It's dependent on Wait,

Brett StClair: It's dependent on

Edwin Johnson: in

George Westbrook: I'll mute you quickly. Um it's it's dependent on when when we can with the Apple developer stuff. Um so as soon as that's done um then we can start getting the process in place and making sure that what well obviously bought before then we'll need to refine it make sure it's all all there. Um, so I think the biggest blocker at the moment is that Apple the Apple store because obviously like today we've got we've got a first version with a a week of iteration.

  
  

### 00:45:28

  

George Westbrook: Um, it's it should be good to

Edwin Johnson: Cool. I mean,

George Westbrook: go.

Edwin Johnson: in your mind's eye, what does that look like to you, George? Could it be end of

George Westbrook: Um,

Edwin Johnson: July?

George Westbrook: oh, 100% if if the Apple developer if the Apple developer stuff is there. I think one thing we've cuz obviously

Edwin Johnson: No, I meant that from a bad sign. I mean,

George Westbrook: there's Yeah,

Edwin Johnson: I think we want it to be up before July if possible.

Troy McDonald Kane: I mean,

George Westbrook: it's I think

Troy McDonald Kane: yeah, I think we want it up by the end of June if we can because we got to get the referral.

George Westbrook: it

Edwin Johnson: Yeah. Yeah, that's what I'm saying.

Troy McDonald Kane: Yeah.

George Westbrook: it's I think it's at the moment the biggest blocker is the Apple developer stuff.

Troy McDonald Kane: Yeah.

George Westbrook: Um because like like what what Hassan showed there, it's it it's functional. Um it's just linking it up,

Edwin Johnson: Cool.

  
  

### 00:46:11

  

George Westbrook: getting it deployed once we've got the approval from Apple developer and of the Google Play stuff. Um but obviously I think the majority of people it's going to be Apple probably like

Edwin Johnson: And cool.

George Westbrook: 70%.

Edwin Johnson: And then Sky on the copy, you're going to go through it all to make sure that I don't have any exposure, right?

Skye Capazorio: Yeah.

Edwin Johnson: Everything's got to be up to and all the rest of it.

Skye Capazorio: Yeah. So, for the trading challenge website, um Max and I have been working on that this week. Um and we just now the refinement just comes in and confirming like the prize pool and that stuff, the legal surrounding the trading challenge that we want um available on that page.

Edwin Johnson: Cool.

Skye Capazorio: Um and then

Edwin Johnson: I know we've re we've redone the um uh pricing for what we're going to distribute and we've come up I What was our total Cody, Troy, and Kev? What did we come up with yesterday? 21 mil.

Kevin Murray: Yeah. 21 million.

  
  

### 00:47:09

  

Edwin Johnson: 21 million which gives us four million in flex spending if the ads are coming in. Right? So, you know, the term up to 25 is something that we really want to focus on because we have a couple of thoughts around the holidays, around Thanksgiving games and then Christmas Day games where we might want to do some really cool

Skye Capazorio: Yeah.

Edwin Johnson: blowout stuff where people are with their families and hopefully by then we can really get a premium on those CPMs. Given the like, you know, what we've shown and the type of audience and the and the like, we we think we could do some really cool s*** there.

Skye Capazorio: Fantastic. Um, yeah, we just need the the details of that um so that we can put that on that section of the website. So, and we can the information that currently is sitting on that website even though it's not live says earn your earn your way up to um earn your part portion of 25 of up to 25 million. Um and then the prize pool area. Um we can also update that as that goes along.

  
  

### 00:48:10

  

Skye Capazorio: Um and and add things. So like if if for example the Christmas day event is not um confirmed now, we can put in a thing going special occasion special highlight event dates to be announced in the future for example. And then we can just put whatever the prize pool information is that we do have to date. Um, and then obviously linking to any legals that have been signed off on on your side from um Matt or or whoever is going to be dealing with the legals.

Edwin Johnson: Um, yes. Okay, cool. That sounds good.

George Westbrook: Perfect. I think I think that's I think I think that's everything for today.

Edwin Johnson: Okay.

George Westbrook: And then we've got the the education session on what tomorrow actually because I forget the bank holiday on Friday, isn't it? Right. Perfect.

Troy McDonald Kane: Yeah.

George Westbrook: Anything else from

Edwin Johnson: Awesome. No, no. Thank you all for your time today.

George Westbrook: anyone?

Edwin Johnson: Again, really blown away by the stuff. Yes. Please get out the baseball, guys, and make sure it says up, too.

Troy McDonald Kane: Heat.

Edwin Johnson: All right.

George Westbrook: Perfect.

Edwin Johnson: Thank you very much all. We will So, we're not meeting on Friday then?

George Westbrook: Um,

Troy McDonald Kane: No, we're meeting

George Westbrook: I think it

Brett StClair: So

Troy McDonald Kane: tomorrow.

George Westbrook: Yeah,

Edwin Johnson: Tomorrow.

Brett StClair: Nice

Edwin Johnson: Okay. Cool. All right. Wish everyone a great day. Thank you so much for your time.

George Westbrook: perfect. Let's f******

Brett StClair: talking.

George Westbrook: go.

Kevin Murray: So everyone,

Skye Capazorio: Thanks everyone.

Edwin Johnson: Bye now.

Kevin Murray: let's

Troy McDonald Kane: Thanks.

Brett StClair: Good job.

  
  

### Transcription ended after 00:49:44

  

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.

**