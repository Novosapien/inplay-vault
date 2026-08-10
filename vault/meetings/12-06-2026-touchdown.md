---
date: 2026-06-12
type: standup
status: extracted
extracted-to:
  - "[[digests/touchdowns-12-17-jun-2026]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[trading/trading]]"
  - "[[challenge-website/challenge-website]]"
  - "[[inplay-global-website/inplay-global-website]]"
  - "[[education/education]]"
  - "[[components/components]]"
  - "[[architecture/open-questions]]"
description: "Transcript of the 2026-06-12 touchdown with extraction table — site analytics, tZERO real-time P&L, market-making kickoff, and AI education video plans"
---

## Post-Call Analysis

> Processed as part of the **[[digests/touchdowns-12-17-jun-2026|12–17 June touchdown sweep]]**.

| Finding | Destination | Action |
|---------|-------------|--------|
| Challenge Website rebuilt on a new template for **Google Analytics**; **Microsoft Clarity** heat-mapping to be added across sites | [[challenge-website/challenge-website]] / [[inplay-global-website/inplay-global-website]] / [[components/components]] (Analytics) | Update blocks + Analytics note |
| **tZERO real-time P&L** confirmed (resolves a buying-power concern) | [[trading/trading]] | Update note |
| **Market-making** kickoff — Kevin Murray (Head Execution Trader) leading, position-based not HFT | [[trading/trading]] / [[architecture/open-questions]] | Note + open-question row |
| **Persona effectively done**; tZERO wallet allocation = grab-from-pool; details call next week | [[customer-onboarding/customer-onboarding]] | Update note |
| **Education delivery debate** — TikTok + AI voice + code-gen animation + podcast; brand-owned modules | [[education/education]] | Update note |
| Press / media page signed off; main site needs app screenshots later | [[inplay-global-website/inplay-global-website]] | Update note |
| Launch referenced as **August 22nd** (College Football IPO) | [[ipo-module/ipo-module]] | Folded into 17-06 dates note |
| Payment-provider meetings (Pay.com and others), non-exclusive interest | — | Commercial; noted in digest triage only |
| Admin env-link consolidation; meeting cadence Mon/Wed/Fri | — | No action (status only) |

**

Jun 12, 2026

## InPlay Digital TouchDown - Transcript

### 00:00:22

  

George Westbrook: I can't use that. No.

Max Kingaby: Good day. Good day. Sorry it took so long to get you that link,

Skye Capazorio: Hi.

Max Kingaby: Sky.

Skye Capazorio: No worries. Is it up?

Max Kingaby: I that's a yeah completely new link.

Skye Capazorio: Is it a new link? Sorry. Is it a new

Max Kingaby: Um I had to rebuild the app on a different template so you can get all of the Google

Skye Capazorio: link?

Max Kingaby: Analytics analytics and whatnot.

George Westbrook: That's that's one thing I don't think we've talked about as well which could be quite handy for you Sky is there's this thing

Max Kingaby: Sorry.

George Westbrook: we have the ability Max could you mute please?

Max Kingaby: Give me

George Westbrook: Um

Skye Capazorio: Everybody has a curse. Your curse is free curse and

George Westbrook: It's f****** so annoy because we've worked out with the merge audio what um what happens is basically it turns off

Skye Capazorio: sound.

George Westbrook: everybody else's mic apart from one person's but we don't know which one it is.

  
  

### 00:01:13

  

George Westbrook: So sometimes it's really good,

Skye Capazorio: All right.

George Westbrook: sometimes it's really bad. Um so going back there's this thing that we can turn on called Microsoft clarity. So what that does is on the websites it will track every session of a user so that over time it will build up heat maps of say users are clicking here they're spending

Skye Capazorio: Sorry.

George Westbrook: a lot of that spending a lot of time on this section. So over time we can use that and be like right okay users are looking at this they're scrolling past that. So then it's it will help with identifying what is somebody actually looking at

Skye Capazorio: Yeah. Yeah.

George Westbrook: and is catching their eye.

Skye Capazorio: And like so it's providing or it's providing another solution to Google Analytics essentially on our with the heat mapping.

George Westbrook: Yeah. Yeah. It's it's it's

Skye Capazorio: It it sounds like it's a bit more than that. Like I used to use another another tool. I can't even remember what it was called like hotspot or hot plate or something along the lines of that to

  
  

### 00:02:02

  

George Westbrook: Yeah.

Skye Capazorio: look at the heat mapping in terms of where drop off was happening um and all of that sort of stuff in that obviously slightly different e-commerce related versus um but we could we could measure it according to um app download and all of that sort of stuff and that's something that working with Max this morning I was trying to implement multiple multiple occasions, just like the trading app, you're two clicks away from trading. The same thing for the challenge, like not wanting to try and bombard it, but that there's always the opportunity to depart from wherever you are to download. Um, similar kind of similar thinking on the prompting of

George Westbrook: Yeah.

Skye Capazorio: that.

George Westbrook: Yeah. But I thought Max Matt showed us this morning as well and that's that's looking that's looking good. The trading the trading one. Um

Skye Capazorio: Yeah, Troy, just for your site visibility, I've just shared it. Um,

George Westbrook: so

Skye Capazorio: I thought it would update on the link that I shared yesterday. Um, but Max said he had to move it over to another link.

  
  

### 00:03:10

  

Skye Capazorio: So, I've now shared the link like a minute ago to that team's group just to show you where um where it uh just the progress that's been made on it. Obviously, the prize pool and that sort of stuff is it hasn't been designed or anything because we need a lot of information to go in there. So, we've kind of focused on the first page, how to enter, and then the referral program is where we've gone and then uh we have we then we've got more time in the diaries the whole of next week to then refine the advertise with us. And then obviously the prize pool as soon as we get

Troy McDonald Kane: All

George Westbrook: Just realized one thing we need to add into the admin panel rather than us sharing links just an

Skye Capazorio: that

Troy McDonald Kane: right.

George Westbrook: easy way where obviously at the moment we've got the if you go into the admin panel you can click and it will go to

Skye Capazorio: I'm

George Westbrook: a version of the website um I think we need to add in one the ability for us to put the link in

  
  

### 00:03:57

  

Skye Capazorio: crazy.

George Westbrook: um and then you lot can just see production testing development and then see the different links rather than Yeah, it's a nightmare when you're looking back for a link and you're like, "s***, I'm looking at an email two weeks ago. Is this the right link or is it

Skye Capazorio: Yeah. All good. All good.

George Westbrook: Yeah.

Troy McDonald Kane: Um,

Kevin Murray: Yeah.

Troy McDonald Kane: the prize pool tab, the logo looks sharp. I don't know whose work that is, but nice. I like that a lot. Under the prize pool tab, there's a a different logo.

Skye Capazorio: Where?

Troy McDonald Kane: It looks It looks sharp is what I'm

Max Kingaby: Oh, that's that's one um I just prompted Gemini to make and it just came up with

Troy McDonald Kane: saying.

Max Kingaby: it.

George Westbrook: send can you send me that link max just have a look

Troy McDonald Kane: Yeah,

Skye Capazorio: Oh, the badging.

Troy McDonald Kane: the badge.

George Westbrook: quickly

Troy McDonald Kane: Yeah, the badging.

Max Kingaby: Yeah.

  
  

### 00:04:49

  

Troy McDonald Kane: Sorry.

Skye Capazorio: Well, sorry. I was like,

Troy McDonald Kane: Yeah.

Skye Capazorio: "Why have we changed the logo

Troy McDonald Kane: No,

Skye Capazorio: again?" All good.

George Westbrook: that's that's what I was thinking

Troy McDonald Kane: I should say the badge icon looks sharp. Yeah.

Skye Capazorio: Yeah. Um, so we we're just trying to get like the information in the right place and then we'll look to add more visuals, more icons, and all of that sort of stuff. We're just trying to get like the bulk. And the same goes for the I we'll make this the focus,

Troy McDonald Kane: Yeah.

Skye Capazorio: but once this is done, I'd like to go back to the main website that we have and and revisit then building out screenshots of the app, all of that sort of stuff into that space,

George Westbrook: All

Troy McDonald Kane: Makes sense.

Skye Capazorio: too.

Troy McDonald Kane: All right. Hey, Kevin.

George Westbrook: right.

Troy McDonald Kane: Um,

Kevin Murray: Hey, how are

Troy McDonald Kane: I'm glad to see you alive.

  
  

### 00:05:33

  

Kevin Murray: you?

Troy McDonald Kane: Um,

Skye Capazorio: Yeah, I was just gonna say

Troy McDonald Kane: I have not talked to Edund in a while. Is he alive?

George Westbrook: Yeah.

Troy McDonald Kane: Have you seen him, heard from him

Kevin Murray: The three of them were alive when I left them last night.

Troy McDonald Kane: last night or this

Kevin Murray: I like I have to Yeah. Oh, this morning.

Troy McDonald Kane: morning?

Kevin Murray: Technically this morning. Yes. H I had waved the white flag.

Skye Capazorio: at at 3:54 when I left them this

Kevin Murray: I was done.

Troy McDonald Kane: Oh, no.

Kevin Murray: Yeah, I waved the white flag.

Skye Capazorio: morning.

Kevin Murray: I I I couldn't go any longer. I was exhausted. I was like

George Westbrook: You're You're the representation for England over there.

Kevin Murray: full.

George Westbrook: Come on. I thought it was the Americans weren't weren't the ones who could hack

Skye Capazorio: No,

George Westbrook: it.

Skye Capazorio: like Cody has a liver.

Kevin Murray: No.

Skye Capazorio: I don't even know what Cody's liver is made from.

  
  

### 00:06:15

  

George Westbrook: Oh.

Skye Capazorio: It's made from like porous sponge material that just takes alcohol and just,

Kevin Murray: Yeah.

Skye Capazorio: you know, extrapolates it into energy cells in his body.

Kevin Murray: Yeah. And he drinks like a fish. I mean,

George Westbrook: Oh,

Kevin Murray: like, you think anyone you know, lads,

Skye Capazorio: Yeah.

Kevin Murray: that can fire drinks into them?

Max Kingaby: That's it.

Kevin Murray: Okay.

Max Kingaby: That's the challenge.

Kevin Murray: He's quick. He's

Troy McDonald Kane: Oh, Max is ready. Max is

Kevin Murray: quicker.

Max Kingaby: Sub in.

Troy McDonald Kane: ready.

Max Kingaby: Sub in.

Skye Capazorio: Max, I mean it. I wouldn't I wouldn't go down this I wouldn't go down this

George Westbrook: Matt,

Troy McDonald Kane: Max,

Kevin Murray: Yeah.

Skye Capazorio: road.

Troy McDonald Kane: he's like a 63 very big guy from Minnesota,

George Westbrook: should we talk about what you did at the Christmas thing?

Troy McDonald Kane: if that makes any sense.

Kevin Murray: Yeah.

Skye Capazorio: He's like he's very tall. He's like he's he's probably I think he's probably close to Brett's height.

  
  

### 00:06:54

  

Skye Capazorio: Like maybe a little bit shorter than Brett.

Max Kingaby: All

Skye Capazorio: And and he's just like he's just his his I don't know.

Max Kingaby: right.

Skye Capazorio: Like I said, I think his liver I don't know what it's made from. It's like supersonic sponge absorption. I don't

Kevin Murray: Yeah, the last two days have been very very good here. So,

Skye Capazorio: know.

Kevin Murray: um I I think Cody filled you in yesterday,

Troy McDonald Kane: Yes, he did. But if you want to just give like maybe a couple minute update to the Novo team and in Sky if she hasn't caught

Kevin Murray: Troy.

Troy McDonald Kane: up with any, you know, with Edwin just because uh I did catch up with Cody because I hadn't heard from Edin. I was like, I just want to check in and make sure everyone's

Kevin Murray: Yeah, we all survived. But um yeah, the so the guys had some really really good uh one-on-

Troy McDonald Kane: okay.

Kevin Murray: ons um meetings uh on the the first day.

  
  

### 00:07:39

  

Kevin Murray: Um and then yesterday we had a really good call with Pay.com. So they are a UK well they're owned by an Israeli guy uh but based out of the UK, but they're just coming over to the US now to make ideally make a big splash for them. Um during the pitch when we were going through it like the CEO absolutely loved it and in the middle of the meeting he pretty much facetimed two other billionaires to get them on the phone. He told Edwin you've got 12 seconds go to literally pitch them. Um it was it was unreal. Um so and then they went off then for like 45 minutes just shooting the s*** between the two of them. But it was really really good. So, good positive meetings over the weekend. Uh, some really good partnerships and connections that we've got to follow up on next week with regards to advertising partners as well as, you know, potentially some payment solutions as well. We've got at least I reckon there's probably three to four payment solutions companies that are are really interested.

  
  

### 00:08:44

  

Kevin Murray: So, we can either see if we can instead of making it exclusive, we could possibly just, you know, either bring two or three of them in to have different parts of it. But that's what was the main sort of area that was really

George Westbrook: Jesus.

Kevin Murray: engaging.

Skye Capazorio: And

Troy McDonald Kane: Did you guys go to Miami for dinner last night or no?

Skye Capazorio: the

Troy McDonald Kane: Yeah.

Kevin Murray: No.

Troy McDonald Kane: Okay.

Skye Capazorio: Sorry, I'm just having a giggle a giggle to myself. Who were the who were the besides the pay um the pay solutions, who else did you speak

Kevin Murray: Uh we Sorry.

Skye Capazorio: to?

Kevin Murray: Give me one second. playing this trying to get me out of here. Give me one sec.

Skye Capazorio: It's been kicked out of the lounge.

Max Kingaby: Right. When When's our version of this trick All

Troy McDonald Kane: I mean,

George Westbrook: I see now you can drink,

Troy McDonald Kane: we definitely got to get you guys over to the US probably.

  
  

### 00:09:39

  

George Westbrook: Max.

Troy McDonald Kane: I I definitely later than when we launch. It'd be great to have you guys here when we actually launch in August 22nd.

Max Kingaby: right.

Kevin Murray: Sorry.

George Westbrook: Hey.

Troy McDonald Kane: So, we're still working on what type of events we're going to plan around the launch and then a few viewing parties throughout the season. But, uh yeah, and then and then you can see but the thing is it's not just going out and drinking. It's going out and drinking and gambling at a casino.

George Westbrook: Oh no.

Troy McDonald Kane: There's a whole combination that go on.

Skye Capazorio: where there no clocks and the walls.

Troy McDonald Kane: It's not just about standing around drinking.

Skye Capazorio: You can't tell

Troy McDonald Kane: It's standing around drinking and playing craps in blackjack and whatever else these degenerates want

George Westbrook: Do they do they have simulation dollars as well?

Skye Capazorio: No,

Kevin Murray: No,

George Westbrook: Oh,

Troy McDonald Kane: to

George Westbrook: no.

Skye Capazorio: this is not a social

Kevin Murray: I I come out on top.

  
  

### 00:10:24

  

George Westbrook: No.

Kevin Murray: Like I um I went playing yesterday and and doing the slots with Cody.

Skye Capazorio: casino.

Kevin Murray: Um I hit 1,400 jackpot, so I was like, "Thank you very much. I'm out.

George Westbrook: f******

Troy McDonald Kane: Cody is magic on those slots. I've won thanks to Cody's advice on slots. Like I've never thought that was possible,

George Westbrook: that.

Troy McDonald Kane: but he has like this insights and these tricks where he knows he like has like this zen of knowing which machines are about to give out bonuses and then playing those machines and getting the bonuses and then maximizing the

Kevin Murray: Yeah,

Troy McDonald Kane: bonuses.

Kevin Murray: the first night he was up I think nearly two and a half thousand and then last night he was down when I left he was down a thousand.

Brett StClair: Oh, f***.

Kevin Murray: So Oh,

George Westbrook: He probably still in there

Kevin Murray: it wasn't that surprise me.

Troy McDonald Kane: He told me once he he made 30,000 on slots once.

George Westbrook: now.

Kevin Murray: Oh yeah, he's he's an absolute

  
  

### 00:11:16

  

Troy McDonald Kane: Yeah.

Kevin Murray: degenerate.

George Westbrook: Do you say he puts a thousand on

Troy McDonald Kane: Yeah. 30,000 US on slots once.

George Westbrook: one?

Troy McDonald Kane: Yeah.

Kevin Murray: Yeah.

Troy McDonald Kane: Yeah. He's magic. So, I think we have to go to Vegas is is what I'm saying. Uh for maps and George and Brett to to see the real Edwin.

Kevin Murray: Yeah.

Max Kingaby: I won't be complaining.

Brett StClair: I just think Max thinks he can outrink Cody. That's all I heard when he said

Troy McDonald Kane: I mean, Chicago's opening up a big brand new uh Hollywood casino,

Brett StClair: that's

Troy McDonald Kane: not Hollywood, but Hard Rock Casino in downtown Chicago. So, maybe that's will be open by the time we launch.

Brett StClair: beautiful.

Kevin Murray: Oh yeah.

George Westbrook: M Max is Max is all talk no walk when it comes to drinking.

Kevin Murray: Yeah.

Max Kingaby: Oh,

George Westbrook: We've had we've had two examples.

Max Kingaby: mate. Save it, Kermit. Save it.

  
  

### 00:12:02

  

Max Kingaby: And as well,

George Westbrook: You see?

Max Kingaby: if we're going down the poker route, I cleared out my 12-year-old brother about five over the course of the weekend. So, you're messing with a heavyweight over here, guys. Bacon.

Troy McDonald Kane: Um, all right. Is there anything else that we needed to touch base on today in today's standup just so that we can um cover that before we go into the weekend?

Brett StClair: Yeah.

George Westbrook: I think I think just going back to the the tZERO call because I think one of our one of our concerns going into it was what maybe the interpretation we got last week where we would be holding the buying power. We're a bit like a that might be because obviously the the amount the price and the actual value of their holdings both like you saying Troy realized and unrealized more the unrealized that's going to be changing so much that not panic but we were kind of like okay this is this is something that we might not have considered but the fact that they said that they're going to be handing that is that's

  
  

### 00:12:58

  

Troy McDonald Kane: Yeah,

George Westbrook: perfect.

Troy McDonald Kane: I was happy with the way I mean they're very thoughtful. I'm sure you guys see this around the workflows and then you know looking to build out some new mechanisms for us to be able to operate this. But I'm glad that you know it it and to your point it should sit there because it's going to have real time nancond calculations. So I'm glad they didn't really like I'm glad we all came to the same conclusion together without having to argue or or debate

George Westbrook: Yeah. Yeah. Um,

Troy McDonald Kane: it.

George Westbrook: so that was good. I think there was one as well which I think Edwin mentioned. I don't know if it was this week or last week was around the market making algorithm.

Troy McDonald Kane: All right. Yes.

George Westbrook: So it's I suppose it's because obviously at the m we're Yeah. So it's when when would when would we be looking to get get that in motion?

  
  

### 00:13:48

  

George Westbrook: Um

Troy McDonald Kane: probably next week at some point.

George Westbrook: and

Troy McDonald Kane: I got like next week we gota I gotta kind of lock him into a room and go through a bunch of stuff from this last week. But that's one of

George Westbrook: Okay.

Troy McDonald Kane: them.

George Westbrook: I need to I need to revise my uh my maths from uh undergraduate Just

Troy McDonald Kane: Yeah. Well, Kevin's going to be there to help because Kevin's help Kevin's kind of leading the ex he's going to be a head execution trader. So,

George Westbrook: start.

Troy McDonald Kane: you know, Kevin's going to help you with that as well. And then we may we may decide also maybe to bring in like a, you know, a computer science intern or someone that's more data science driven as well, just to kind of help with some of the research or post trade or anything like that. The good thing is we're not looking to trade high frequency. We're looking to trade more position based kind of reflective of opinion in the market that day and and put on size and and kind of let it ride

  
  

### 00:14:45

  

George Westbrook: I think one one just thought one thing that might be quite handy is before before we get into the

Troy McDonald Kane: essentially.

George Westbrook: the weeds of it if you could just send us over some like pointers of what we need to look at and research before um just so when we're going into it we're not asking stupid questions like what is that what is this blah blah

Gary Anderson: What's

George Westbrook: blah. So, we're going going in a bit more bit bit more informed more like a revision sheet as stupid as it sounds. Um, I suppose it wouldn't be revision, it'd be it'd be learning. Um, rather than obviously wasting your guys time for the first half an hour where we're just going, wait, what does this mean? What does that mean? Blah blah

Troy McDonald Kane: Yep.

George Westbrook: blah.

Troy McDonald Kane: That's good because Kevin's doing the same

Kevin Murray: I was I was about to say that I'm sort of learning it because it it's it's something I've never traded either before.

Troy McDonald Kane: thing.

Kevin Murray: So, I'm going through all that stuff at the moment.

  
  

### 00:15:30

  

Kevin Murray: So, I'll dig some stuff out as well and then share it with the

George Westbrook: Perfect.

Kevin Murray: group.

Troy McDonald Kane: Okay.

George Westbrook: Perfect. Um then so one thing which I don't think we spoke about for a while is the education aspect as well. Um we're under the impression that obviously we we're obviously we're serving the content but we're not necessarily producing it. Um, obviously that's potentially something that we want to we we want to start getting implemented even if it's just fake content for the time being. Um, maybe we just generate random stuff with with AI.

Kevin Murray: Wait,

George Westbrook: um just so we can get the look feel um going. And then once we got that nailed down in the background, getting the real real content

Kevin Murray: did you Sorry.

Skye Capazorio: So one of no so this is one of the things that because it's a list it's on

Kevin Murray: Go ahead,

George Westbrook: going

Kevin Murray: Sky.

Skye Capazorio: my like on my notes is just I suppose a question sitting next to it of how how we envisage the education working from from day one from what we had originally spoken and workshopped when we were in Chicago.

  
  

### 00:16:34

  

Skye Capazorio: It was going to be like almost Tik Tok real snippets essentially that that work that you got like little pieces of information. It was broken down in that sort of way that was also contextual to talking about you know having somebody that would take ownership of creation of that content. Um there's obviously a midline in that sense as you said George there's ways to create those videos in um with AI um to be more like text coming in and animation and and I suppose an element of like the doodle videos that Cody had worked on uh Troy and Kevin a while back. So like there different ways of us doing it that I think we just need to align on how we want to execute that first iteration or or what going forward because obviously if we need to start generating AI videos then we need to see like how that's going to work. George I don't know if you guys have the capability to do that.

George Westbrook: Yeah.

Skye Capazorio: We've been working with somebody to do far more advanced videos when it comes to that that require lots of iterations of prompting.

  
  

### 00:17:38

  

Skye Capazorio: If we're creating a hundred videos at that scale, I just don't see it being feasible at this point in time. So, we just need to find what we're doing what and how how we see that happening. So, that then we've got a this is how we're going to produce those

George Westbrook: Let me let let me show you something quickly that might with the AI videos. One way of doing it. I hope you can hear the Let me Let

Brett StClair: That's what I

George Westbrook: me Can you Can you all see this?

Brett StClair: said.

Kevin Murray: Yep.

George Westbrook: Um, can you can you hear that or not?

Troy McDonald Kane: No.

Kevin Murray: No.

Skye Capazorio: I can't hear anything.

George Westbrook: I'll explain it rather than me trying to fiddle around for two minutes. So, basically this, you know, it just looks like a slideshow. Um, add animations and things like that. but also on top of that generate the actual voice. So how this works will create the components or create the the iconography um and then create the transcript and then generate the voice with AI overlay it on top and then match it match it up perfectly.

  
  

### 00:18:58

  

George Westbrook: It's not a it's not an hour job per video. Um it's it's maybe an hour and a half, two hours, but maybe there's a potential way that we could generate one or two. Um nail that down and then start to generate them more at scale. Like I said, it's not a it's not a give us a give us a week and then it's then it's all done.

Skye Capazorio: So, am I right, George? Just so for clarity purposes, you're saying this is more as like a a carousel deck of of stuff with a voice over that goes as opposed to animation.

George Westbrook: Um you there's animation that you can do. Um so like this is kind of written in code. Um so the way the like so when it when it animates out so stuff like this we can use AI um to do that. It's just I wouldn't say we've we've tested how far it can go in terms of the animation, but I think a lot of like the AI companies now like the product demo videos they do, whereas before they're spending 2530 grand on a product demo video, they're generating it in a day with a couple hundred in tokens.

  
  

### 00:20:13

  

Skye Capazorio: Okay, cool. Um, I think let's let's see what we can do in that space. Um, I think it would be great to be able to visually see what is doable in that space to be able to show the team so that we can go is that is that okay? Is that what we want to do? Maybe we just write I don't know Kevin if you can share just like one of the you know like just something straightforward that we can create quickly look at how that

Kevin Murray: Yeah.

Skye Capazorio: renders and then see if that's if that's the direction that is you know wanted to be taken and then what the kind of I suppose the the cost to produce as in the you know the tokens and stuff like that that would be needed to produce that um an understanding of that at the scale that the education content that Kevin's built out needs to be to go live

Kevin Murray: So I'll just share this with you if can everyone see

Skye Capazorio: with

Kevin Murray: that?

George Westbrook: Yep.

  
  

### 00:21:14

  

Kevin Murray: Okay. So this is basically what was one of the uh beginner slides that I've done.

George Westbrook: This

Kevin Murray: So again creating different things and then ideally what I did was I just put like a video at the top and then based on the capital market information and structure behind it. Um obviously we have still to go through this with Troy and Edwin to to finalize it and make sure everything is what we need to do. And then uh with regards to that then you know as you get through it then you'll have like questions and stuff as well um and answers to be able to to complete before uh moving on to the next page. So like at the end like there's like a module quiz as well.

Skye Capazorio: So when So Kevin, if you can just scroll back quickly to where it says to where it said videos and then it went into capital markets.

Kevin Murray: Yeah. Yeah.

Skye Capazorio: Um it so is is it that the video explains everything that you're about to read and then you can read through it again if you want to.

  
  

### 00:22:11

  

Skye Capazorio: So you can watch the video and or read and then do the

Kevin Murray: Yeah. So like the video is probably going to be like more so like a like a highlight of what that what capital

Skye Capazorio: quiz.

Kevin Murray: markets is for argument sake. So it could be like a 30 second 40 second video and then obviously then there's more detailed information that they'd have to to read through if they wanted to or again they can just go click click on the the test to to pass

Skye Capazorio: Okay. Yeah.

Kevin Murray: it to and then get the 100 credits to move on to the next

Skye Capazorio: So almost like George,

Kevin Murray: module.

Skye Capazorio: I would say like it would read it would verbalize parts of this and then bring up like the more visual assets like primary versus secondary markets in the table um and hold that up and kind of go like a summary kind of verbalization going through each of the the rows. then SEC, FINRA, reggga, tier 2, ATS.

Kevin Murray: What?

Skye Capazorio: Um maybe those could just be like icons that then come up.

  
  

### 00:23:10

  

Skye Capazorio: So I don't know if maybe what's worth it is taking this just in module one let's just say capital markets and let's see what we can create visually out of out of the novoc sapen uh content creation and then and then put that forward in front of the team and see if that's you know if that's going to be viable with a

George Westbrook: I'm think one of the things I'm just one of the things I was thinking is so what the different methods of delivering this to a user. So there's pure text, then there's audio, and then there's visual, and then audio visual. So one potential thing that we could do is maybe more like a podcast route, not like not as the primary thing, um, but generating a podcast where there's two speakers. Um, they're having the conversation. Like I can think of like Joe Rogan. I mean, that's my go-to anyway. Um, so like the different because like I think it's I think it'd be good to progress over time.

Kevin Murray: Yep.

George Westbrook: Um, but taking final end state there could be the videos um like that one that I just showed you the pure pure text version the podcast and then even just uh where it just reads exactly what is on the page for the user.

  
  

### 00:24:27

  

Skye Capazorio: This

George Westbrook: Um because I suppose it's yeah when would somebody listen to a podcast like when they're walking to work or they're on the train. So it's getting more more of their time. I mean, one thing potentially be putting ads in the podcasts for the for for the thing. So like Yeah.

Skye Capazorio: Yeah. Yeah. Sorry. Carry

George Westbrook: So should like say where Yeah. Yeah,

Skye Capazorio: on.

George Westbrook: there's a podcast. It's 10 minutes. 20 seconds of that is ads sprinkled throughout like a 5second 5-second ad for Visa, 5second ad for Doritos, blah blah

Skye Capazorio: That was exactly the intention actually behind the the video content that was the brand in an

George Westbrook: blah.

Kevin Murray: What?

Skye Capazorio: ideal world. It was a brand that took ownership of the education module essentially and actually went and then produced this in their own visually and all of that. So they would own visual representation and all uh spoken ad breaks including the scrolling function. So the Tik Tok so they could use ambassadors of their own to do it or however they wanted to create that.

  
  

### 00:25:32

  

Skye Capazorio: So they took full ownership of this. Um it obviously depends on where we land from a sponsorship perspective

George Westbrook: Yeah. Yeah.

Skye Capazorio: um uh going forward um for for this specific one. But I think and obviously also like a podcast for example and I just want to make sure that we're on the same page about this. the podcast is you're gonna simulate that with AI voices as opposed to okay finding cool cool yeah I think that's absolutely the route that we wanted to go in terms

George Westbrook: Yeah.

Skye Capazorio: of accessibility of the content from the education side I think in its first iteration if we are going to create it until we've resolved sponsorship in this space um that would be

George Westbrook: I mean, now with AI,

Skye Capazorio: Right.

George Westbrook: you could do like programmatic voice ads. So like what I mean by let's say there's that 20 second break within the middle. Obviously usually with a podcast the cost to generate a voice is quite quite a lot but we could potentially programmatically add in that voice in the middle of that audio clip.

  
  

### 00:26:39

  

George Westbrook: I've Yeah, I've not really thought about that. Let's park that. Just throwing the idea out there. Otherwise we could squirrel squirrel on that.

Skye Capazorio: Yeah. Yeah. Yeah. And I think as as I think it's I think the the vision the intention of it going forward very similar actually to the chat function was that the chat function was also supposed to be built out that we could have a level of a broadcast desk that existed within that that was actually you know casted faces that then could be Coca-Cola branded in the background that they were then bringing you I I Brett you and I were joking about this over WhatsApp yesterday but where I was like Brett is you know bringing you the NFL recap of whatever like it. The whole concept was to be able to build out these content ownership spaces for brands that they could then have space in that absolutely you could either own it as a brand or you could even put in revshare advertising that then existed in it on those different modules.

  
  

### 00:27:32

  

Skye Capazorio: So um I think the vision's totally aligned. I think where we need to get to is what does version one look like, version two,

George Westbrook: Yeah.

Skye Capazorio: version three as we as we as we go along the process and as we kind of are building the plane while it's flying in terms of the bolts of sponsorships in that

George Westbrook: Yes.

Troy McDonald Kane: So,

Skye Capazorio: Okay.

Troy McDonald Kane: here's what here's what I would like to recommend. Um, so I know we have a couple other things that we want to tackle going into next week to get the referral, you know, app dropped um, you know, whenever as soon as we can. And I know we're still pending the app stores kind of verification, but Brett, next Friday, can we make our session an hour and make half of it a brainstorming session on the educational stuff? And then this week, Kevin and I will sit down and go through it so that we could at least get you a the first module that maybe we can beta test through this through this

  
  

### 00:28:33

  

George Westbrook: Yeah.

Troy McDonald Kane: process.

George Westbrook: Yeah, that'd be really good.

Brett StClair: Perfect.

George Westbrook: Um, which I think leads into the the next thing we we wanted to talk about was the start thinking about the well not start thinking but start getting done the pre-launch um version of the app. Um, so like what what are we going to include on there? Um, is it just going to be KYC and a holding page? not a holding page in terms of like what like a coming soon or we're gonna show data or are we gonna we're gonna do this and that like because obviously we've got the components there now

Brett StClair: Oh my god. He wants

George Westbrook: um it's what do we want to provide to the user as an experience before there's everything going on which I suppose could be a session in

Troy McDonald Kane: Yeah. Well,

George Westbrook: itself.

Troy McDonald Kane: we should make that the priority for Monday and we'll I'll make sure the team comes

Brett StClair: Take a

George Westbrook: Yeah.

Brett StClair: face.

  
  

### 00:29:31

  

Troy McDonald Kane: ready to talk through that on Monday so that we can solidify a plan on Monday.

George Westbrook: Yeah, let me just have a look at the calendar quickly cuz I can't imagine that's a half an hour and half an hour and

Troy McDonald Kane: I mean, we can do we should probably do an hour on Monday if we can.

George Westbrook: done.

Troy McDonald Kane: Now that we're doing these every other day, maybe next week we try to do the the three of them an hour each on what Monday because we next week's a big week for trying to finalize a few things. At least Monday and Friday I would do an hour and then maybe Wednesday we just do 30

George Westbrook: Um yeah.

Brett StClair: This is a

George Westbrook: Yeah.

Troy McDonald Kane: minutes

George Westbrook: And then Monday pre-launch,

Brett StClair: good

George Westbrook: Friday education. Um yeah.

Troy McDonald Kane: and then Wednesday just a midweek check in.

George Westbrook: Okay.

Troy McDonald Kane: Yeah.

George Westbrook: Yeah. Perfect. Um and then yeah,

Troy McDonald Kane: Okay.

George Westbrook: we might depending on what um if if if we get any information from that Abasheket guy um maybe set up a quick I mean it might just be a me me Hassan and Abashek call where it's just ironing out some details.

  
  

### 00:30:35

  

George Westbrook: Um, but I think we might need one next week, but I suppose it depends how far how far we get with the No, we it will be next week cuz I think like like I said earlier, the the on boarding stuff, I mean, Persona's and then punch me in the arm here if I say something wrong here, Hassan. Persona's pretty much done. Um, so it's which I mean I think I said this the other week which did really make us laugh where the time it took for them to send the on boarding call. Um, it's already already done, built and implemented which was quite nice.

Troy McDonald Kane: Yeah,

George Westbrook: Um and then KYC KYC

Kevin Murray: Awesome.

Troy McDonald Kane: cool.

George Westbrook: on tZERO side and wallet allocation which from what we said it's just there's a pool of IDs and we just grab one and allocate. Um so that should be touch wood pretty straightforward.

Troy McDonald Kane: Okay,

Kevin Murray: All right.

Troy McDonald Kane: great. I gotta I do have a hard stop. I got to jump to another call, but this has been another good productive week.

  
  

### 00:31:40

  

Troy McDonald Kane: The website looks great. Um, so thank you for getting that across the line this week. Um, and I know um I just signed off on the press and all that page being done. So that looks good. Thank you for getting that up and and integrated. So keep pushing along everyone. Hopefully you guys have a good weekend and we'll regroup in uh on Monday morning or Monday afternoon your time.

George Westbrook: Perfect.

Kevin Murray: All

George Westbrook: Who's Who's going to say it to sign

Troy McDonald Kane: You you have to say it now every time,

George Westbrook: off?

Kevin Murray: right.

Troy McDonald Kane: George. Just it's like the the way to end every meeting.

George Westbrook: Yeah,

Troy McDonald Kane: So,

George Westbrook: let's f******

Troy McDonald Kane: let's f******

George Westbrook: go.

Troy McDonald Kane: go.

Kevin Murray: All right. Have a good one, guys. Take care.

George Westbrook: b****,

Kevin Murray: Bye,

George Westbrook: you say never give up.

Kevin Murray: guys.

Brett StClair: the Go.

  
  

### Transcription ended after 00:32:27

  

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.

**