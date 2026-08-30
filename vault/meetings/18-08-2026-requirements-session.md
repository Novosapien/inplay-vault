---
date: 2026-08-18
type: general
status: raw
extracted-to:
scope:
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[ipo-module/ipo-module]]"
  - "[[trading/trading]]"
  - "[[market-maker/market-maker]]"
  - "[[advertising/advertising]]"
description: "Raw transcript of the 2026-08-18 requirements review — onboarding pathways, IPO notices, the order-book tile, top-of-book-only quoting, and ad inventory"
---
   **

Aug 18, 2026

## Review requirements - Transcript

### 00:00:00

  

Brett StClair: Oh, we need so we can

George Westbrook: Just Yeah.

edwin: Just don't please don't play it in court.

George Westbrook: Just

edwin: God, that chick sounds like a good time.

Brett StClair: load

edwin: Um,

George Westbrook: don't

edwin: anyways. Yeah. So, you know, a couple of things like, you know, when you when people download the app, the f*** you, b****. I mean, come on. Um, when you first download the app, the um you have to be greeted with that those pathways. It has to be, you know, it because otherwise people don't know what to do and so we need them to enroll in something either the private competition, the open competition or the overall and and cuz you know it that one's a non-negotiable and you've got the field. I mean we we've created something and I can you know put something together too if needed. you know, it's just basically three quadrants, you know, it could be like white or navy, white and orange, you know, public, private, money, whatever. And it's just click there and that gets you through to the app.

  
  

### 00:01:01

  

edwin: And, you know, once you click there, it's going to ask you for your email, your private ID or your your um uh you know, ID for uh the the verification. So, if people want to do the cash, that way these assholes who freak out and are like, "You're going to steal my ID." They can just go right to the public and then that they're not going to be, you know, intimidated to sign up. Cuz I actually have, and this is not a joke, people in my family who are they refuse to um sign up because they think their identity is going to get stolen. And you know,

Brett StClair: f***.

edwin: it's like, you know,

Brett StClair: Thank

edwin: you're I went to the PJ tour supertore.

Brett StClair: god.

edwin: I was traveling with Cody for a golf thing. And I don't know if I told you this, Cody. I bought a travel bag and the little trick behind the counter obviously stole my credit card info because he told me he was going to Vegas. When he was in Vegas, the guy racked up like 500 bucks in Only Fans charges.

  
  

### 00:02:03

  

Cody Haugen: in

edwin: So the credit Yeah.

George Westbrook: Are

edwin: So, the guy,

Cody Haugen: Vegas.

edwin: the credit card company called me back.

George Westbrook: you

edwin: They're like, "Listen, you've never purchased this before. Is this you?" And I was like, "No. Um,

Brett StClair: It's coming.

edwin: but can I can I have the links and let me check it out?" No. And then,

Cody Haugen: I mean, since I already paid for it.

edwin: you know,

George Westbrook: a paid for? Yeah.

edwin: let me do some investigative reporting here. Um,

Cody Haugen: Yeah.

edwin: but like people can steal your s***

Brett StClair: Yeah.

edwin: all the time, but for whatever reason, everyone's worked up about this. So, like that that one has to be the first thing you see when you download the app. Okay. Is that

George Westbrook: Yeah.

Cody Haugen: Is it Is it helpful to pull the list?

Brett StClair: Yeah.

George Westbrook: Yeah.

edwin: fair?

Brett StClair: Yeah. I think it's I think we should just quickly walk through it. I mean, I wanted to raise it's a risk, right?

  
  

### 00:02:45

  

Brett StClair: because it is a risk. Like we're doing these changes and so like if it's something else pushing it too

Cody Haugen: Yeah. Can Can you elaborate? Yeah.

Brett StClair: far.

Cody Haugen: Can you elaborate on that, Brett? Like I I understand we keep saying it's a risk.

Brett StClair: So,

Cody Haugen: Um.

Brett StClair: So,

Cody Haugen: But like what what is the risk

Brett StClair: a couple of things can so the easiest way

Cody Haugen: specifically?

Brett StClair: to do it is as you get closer to the period that we're going to cut off, what you want to be doing is less and less change in the code base. And so, even if it's humans or it's AI writing it, there's chances of mistakes. And so the problem with AI that AI I mean we've got all these agent work forces that are trying to retest and they manipulative and they're turning it and they're trying to make sure it's 100% perfect.

edwin: I love your AI.

Brett StClair: It can go wrong,

edwin: My description of the

Brett StClair: you know, that's how my brain is seeing it.

  
  

### 00:03:37

  

Brett StClair: Like lots of little Georgees f******

edwin: work.

Brett StClair: everywhere and the suns, you know, like f****** they just bred like m************ and they just all these and all that sort of s***,

George Westbrook: Yeah.

Brett StClair: right? But code can be broken and so the delicacy around code breaking in is it can break in a number of different ways. It can break where we get an error or it can break if it affects an algorithm or it affects a calculation or it does something that we just don't pick up because we've been testing. So all this other time we're testing continuously. We always just running through checking and running tests, running tests, running tests. And you won't believe how many times we do a change, whole lot of stuff is just different. You know, your call back screens fail and go to somewhere else. Those are the risks that happen. And so what you're trying to do as you go live is you're trying to iron that out. I that f****** flat iron, flat iron, flat.

  
  

### 00:04:34

  

Brett StClair: And every time we bring in new changes, we're opening that door again. I'm not saying it'll happen, but there's a chance of it happening. So risk is I mean you guys understand the the fundamentals of risk. I don't have to explain that but I think what I have to explain is what type of risk like and the type of

Cody Haugen: Right.

Brett StClair: risk is the code can break or can break your data or can break your backend or can break servers or can break the stuff. And so our jobs as technologists is make sure we we build stability because as we go closer and closer to launch there are people are going to take up on this product. Like in this room we believe one f****** thousand% this is a f****** brilliant idea and it's going to f****** kick off. Yeah, we need to do marketing and push this this but it's going to f****** kick off and there's going to be spikes. And so our jobs are to level it out, make sure it's smooth, because what we don't want is when you're running 10,000 users and something breaks or you spot there's been a mistake in the algorithm, it's probably okay in in the simulation, but if it was real trading and we expose you guys to millions of dollars of exposure, those are the kind of risks.

  
  

### 00:05:50

  

edwin: What's

Brett StClair: And so like I'll always be calling out risks.

edwin: this?

Brett StClair: That's my job, right? My job is the product owner, the guy kind of managing Where and how? what backlogs backlogs kind of look like. George's job is to shape and and get the designs right. A son's job is to make sure that we implementing, deploying, and managing all the backend infrastructure. Um, and then you've got Max who's making things pretty because Max is pretty. Um, and so it's that kind of risk. And so like I think you guys are putting yourself on,

Cody Haugen: Yeah,

Brett StClair: I'm going to highlight it. Don't don't get irritable with me or I know like you want to put

Cody Haugen: it's it's fair.

edwin: Too late.

Brett StClair: the guy,

edwin: Too late.

Brett StClair: right?

Cody Haugen: No,

Brett StClair: Someone's got to be

edwin: Listen,

Cody Haugen: it's it it is

edwin: I'm a risk taker, Brett.

Brett StClair: careful.

edwin: I I hear what you're saying and we we we read it loud and clear.

  
  

### 00:06:36

  

edwin: That said, I'll take the f****** risk cuz like we need Yeah.

Brett StClair: That's what I

edwin: When the people open it up, we we need a couple of things.

Brett StClair: think.

edwin: Number one, they have to know what to do, okay? they it has to be very very clear because otherwise you know I can say that probably 80% of my demonstrations people have been like I don't know what to do I'm on your app what do I do and they'll call me up and I'm like I don't I I you start trading it and they're like how where when you know like what is this and so you know we've made a lot of nice visual changes over the last few days so you know I think the things that we're looking to do are not about um adding like a huge workload. I think that you know I mean a login page is f****** simple. I mean that that's not a big deal. I mean George could whip that up while um Cody and Hassan are cleaning jerking each other. Um I I I don't see that as a big

  
  

### 00:07:34

  

Brett StClair: So, so but there is risk in it because we stepping into the authentication path and the

edwin: lift.

Brett StClair: authentication path is even in AI is really difficult. So I agree with you I think we can do it.

edwin: But it aren't we don't we already have the AI button like like the the authentication

George Westbrook: it.

Brett StClair: So as soon as you change workflows okay you might as well explain

edwin: button

George Westbrook: So is I think the look by that is easy but it's it's what happens behind the scenes. So like with the authentication it's so one what are they authenticating what KYC flow then if they're just doing the free competition then we got to make sure that there's the flag there then on every single page we've got to limit certain things for free users we've got to limit certain things

edwin: What do you have to

George Westbrook: for the so say for example on the

Brett StClair: So if if Yeah.

edwin: limit?

George Westbrook: on the free user on the leaderboards I think correct me if I'm wrong on any of this we said that the user is not going to be on the leaderboard So we need to make sure that in the back end when we're doing the calculations that they're not doing that when it comes to working out the payouts for example we're going to have to exclude those users.

  
  

### 00:08:42

  

George Westbrook: Whereas before it kind of was any single person trading is eligible for payouts and is going to be on the leaderboard. We have to change the logic.

edwin: But can't Yeah. Can't we just have like another leaderboard? Like we were talking about doing like privates. So it's basically you have three leaderboards two leaderboards. You have the authenticated one and then you have the public facing one that's just signed up with an

George Westbrook: We we we can we we can do that.

edwin: email.

George Westbrook: It's just it we've still got to change the back end like cuz whereas before it was kind of if somebody's trading they're going to be on the leaderboard. If somebody's trading they're going to be getting a payout.

edwin: Gotcha.

George Westbrook: Now we've kind of got to go if user is free then put them on this leaderboard

Brett StClair: And it's on every and you think of every single user journey.

George Westbrook: and don't do payouts.

Brett StClair: kind of flows one direction and what we're doing this is we're saying just check make sure they are that great confirm just check just check just check just check so it's a lot but we've been thinking and building and architecting it and so the way we've architectured it is so that you can do that because you guys bought up that you wanted multilayer and son and and and the team at at um persona you are thinking about how to layer this in. But I'm not saying we can't do it right now.

  
  

### 00:10:05

  

Brett StClair: So, let us do it. But know that the risk of that ripples throughout the entire app because it's every single user journey.

edwin: Okay.

Brett StClair: And I think it's all good, right? It's good for us to explain to you guys how it works and how the technology holds together. So, at least you also can see like when you're seeing a problem, you're like, "f****** hell, hold on. How did that slip through? that should not be going to under 18 and then we'll be like f*** we didn't pick up on that user journey we've got to go restitch it d and so the stuff where we architecturally are trying to be prepared for it and that we're building out the backends the front ends I agree with you they're easy um we're going to

edwin: You're not going to believe this. They're like an iceberg.

Brett StClair: highlight

George Westbrook: That's a really good That's a really good

Brett StClair: you know what we should No,

edwin: Thanks,

Brett StClair: no.

edwin: George. I heard it.

Brett StClair: What I'm going to do,

  
  

### 00:10:58

  

edwin: I heard it from this dude in

George Westbrook: analogy.

Cody Haugen: Oh

Brett StClair: I'm I'm going to do two I'm going to do two two boards.

Cody Haugen: god.

edwin: London.

Brett StClair: So, in office, we've got boards. We've got a board for Brett's s*** jokes. We've got a board for um Hasan being too gay.

edwin: Oh,

Brett StClair: Um what was the other board that we've got?

edwin: there.

Brett StClair: I can't remember. So, we've got a bunch of boards.

George Westbrook: Rabbit host.

Brett StClair: So, I'm going to create one where you can call out uh icebergs and we'll mark us off on iceberg comments. And I'm going to create one called technologists and I'm going to call you guys out on technologist calls and then we can see where it

edwin: It's good stuff right there,

Brett StClair: goes.

edwin: sir. They

Cody Haugen: Yeah, I What one thing that I I mean I do want to point out though is we have

edwin: um

Cody Haugen: 160 or so verified users on this. They IPO in four days and they start trading on the 29th.

  
  

### 00:11:51

  

Cody Haugen: That's not new information. I know we all know that. But of that 160, probably a hundred of them are friends and family. So call it we had 60 people as of right now. Yeah. So to the point of risk, I would say we have roughly I mean how many days until September

Brett StClair: sec.

Cody Haugen: 5th is our risk sort of adjusted uh play zone that we can really make and shake and f*** some s*** up because it's it's low risk. Um now granted, yes, we need to make it as soon as possible.

Brett StClair: just notify them you know say like we are going to be doing changes you're like us like Pioneer users

Cody Haugen: 100%. And and and and we can we can help with that, too.

Brett StClair: we

Cody Haugen: Like obviously there's push app notifications we can send out, but there's also we can send it out through the newsletter. We can, you know, do certain other things to communicate that to the users. That's a great idea, Brett.

  
  

### 00:12:46

  

Cody Haugen: Um, but I would say like yes, we want to get this ready as soon as possible, which is where these, you know, 25 or so odd things come from, but right now is the only time I think in this company's journey where we are going to be operating with as little risk as we have today. It is never going to be this low of risk ever

Brett StClair: Yeah,

Cody Haugen: again.

Brett StClair: that's a really really good point on that. Um, so can we go through this list?

Cody Haugen: Yeah.

Brett StClair: And I think the way to do this is one is we pretty much think it's okay and we should go for it. Two is we need to go and have a look at it. Uh, three is yeah, we can call this one. we're worried about it and and we just go through this and we go, "Yeah, yeah, yeah." And if there's anything that we don't understand what it's about, let's talk about it. Otherwise, let's whip it through and give it a like a one, two, three, one, two, three, one, two, three.

  
  

### 00:13:38

  

Brett StClair: And we get through it very,

Cody Haugen: Okay.

Brett StClair: very quickly. And then the focus is really make sure we bang out all the ones really quickly, the twos, then we'll manage. If if there are any threes, like I had a quick read through it. Like I don't I don't quite see it. It's just the volume, that's all.

Cody Haugen: Yeah. Yeah. So yeah, and I know we've brought this up before, but the no spinning wheel on login. I honestly like that screen is so short anyways and it's so fast that you can't even generally read what those little tidbits are on that screen. Is the spinning wheel just to remove that screen and you also remove said loading for that screen?

George Westbrook: I was I was going to say, do we just completely get rid of the screen and then it just loads up because it Yeah.

Cody Haugen: Yeah.

edwin: Yes.

Cody Haugen: Yeah. Just because it goes

edwin: Yes. I mean, some some of this is going to be reduction like,

  
  

### 00:14:23

  

George Westbrook: Okay.

edwin: you know,

Cody Haugen: That's what I'm

edwin: we're we're we're trying to simplify, not add, right?

Cody Haugen: saying.

edwin: Like I mean yeah there's a couple things that obviously you know for from a user standpoint like when I traded on Saturday I mean I I will give you this. I mean Thursday night I f****** didn't sleep and I was like I you know I was you know pretty much sure that this this business was going to be in big trouble because I didn't think there you could make the changes you made as quickly as you did and make it as functional as it was on Saturday. Um, Um cuz like I got to spend a bunch of money to market this s*** right now and I don't want to market it if the app experience is as difficult as like these lay people who are doing it are telling me, you know, I'm not telling you this from like what I what I think looks good or feels good or anything like that. I'm just telling you the feedback I'm getting and like I don't want to spend, you know, a million bucks to have a bunch of people download it and be like, "f*** this." You know what I mean?

  
  

### 00:15:24

  

edwin: So I want I want to try to make it as as clean and easy as possible. So, I would just get rid of that first

Cody Haugen: Yep, agreed. Because it goes too fast anyways.

edwin: page.

Cody Haugen: The the tidbits are nice, but you can't read the full thing anyways. Um, okay. So, that sounds like a negative one. So,

Brett StClair: It's a negative

Cody Haugen: all right. So, our our future three is now in play.

Brett StClair: one.

Cody Haugen: Um, okay. So, then we've already talked about the path at Nauseium, but that needs to be on the homepage.

Brett StClair: So,

Cody Haugen: Uh yeah,

Brett StClair: the path,

Cody Haugen: go ahead.

Brett StClair: let's put it as a two. So 2 to two, we just need to work through and just make we going to do it,

Cody Haugen: Okay.

Brett StClair: but we just got to make sure we're not going to break anything as we go through

Cody Haugen: Yeah. Number three is a variation of what we had before,

  
  

### 00:16:07

  

Brett StClair: it.

Cody Haugen: but there needs to be some sort of banner on that on the homepage somewhere that says like participate in the IPOs. They start on the 22nd.

edwin: I wouldn't even do Yeah, I wouldn't even put that in, Cody.

Cody Haugen: No, this one. Three.

edwin: I Yeah,

Cody Haugen: Is it gone

edwin: because I'm thinking about it by the time like I mean if you have like a popup or something that just

Cody Haugen: now?

edwin: says IPOs I guess on the 2 I would even do the 22nd. I would just say Yeah. Well, I guess I would I would just say IPOs on the 22nd and the 5th. Or is it the 5th?

Cody Haugen: Yes, Beth.

edwin: Yeah. And I would I would just basically do that. NCAA IPOs on the 22nd, NFL on the 20 around the 5th. So, and it could be a popup that happens one time they click and that's it because they're they're going to click on a team

Cody Haugen: Okay,

edwin: and the only thing they're going to be able to do is buy.

  
  

### 00:17:03

  

Cody Haugen: fair point.

edwin: There's going to be no marketing.

Cody Haugen: You you you you will be able to figure it out very quickly.

edwin: You would

Cody Haugen: You would hope. All right,

edwin: hope

Brett StClair: George,

Cody Haugen: so popup

Brett StClair: I'm not going to do the grading. I'm going to leave the grading to you once off because I'm going to be making assumptions, I realize, and you're going to probably be me under the table.

George Westbrook: He's got the glasses on. He's

Brett StClair: Yeah, I know. I've got to read like it's like I'm my eyes are bugged.

George Westbrook: focusing.

Brett StClair: Um, so what do you rank a three,

Cody Haugen: Yes.

edwin: Sure.

Brett StClair: George?

George Westbrook: popup. Is it a one-time popup?

Cody Haugen: Yep.

George Westbrook: Is it uh

edwin: One time. Pop it up or if you want to pop it up as we can.

George Westbrook: that

edwin: By the way, it only is going to last until the 5th and then that thing's gone, right? So, it's not going to last long.

  
  

### 00:17:52

  

George Westbrook: I personally I personally pop up should should be okay but I personally don't think it should be a popup. I think it should be something on the homepage um with the countdown.

edwin: Okay,

George Westbrook: But but feel free because I think it's people go to the homepage, they're going to be coming coming back,

edwin: done.

George Westbrook: they'll see something pop up. I know when I get a pop up, I go, "f*** off. Get out of here." Um and not everybody's like that. Um but I suppose home homepage is the router to the other pages. Um so every time we people are there

Brett StClair: It's not top of home page. It's not top of homepage. Always at top of homepage because right we got limited real estate there. Where do we want to be popping

edwin: Let me pull it up.

Brett StClair: it?

edwin: Give you some

Cody Haugen: Yeah, I would say closer to the bottom if possible because right now we have that homepage

edwin: cash.

George Westbrook: My

Cody Haugen: finally refined a little bit and there are some other notes in here to the homepage, All right.

  
  

### 00:18:52

  

edwin: Yeah. Um, you know, because it's only going to be for a short amount of time, I would put it underneath the ticker.

George Westbrook: So, do we do we want let's call it the the the prize selection or the

Brett StClair: Happy.

George Westbrook: challenge type selection then the IPO or IPO then the challenge selection because I suppose a user can't technically go in the IPO if they haven't selected the challenge that they want to

edwin: Yeah, I would do challenge first. So that the hierarchy go challenge, then go IPO notice, and then go your total equity.

George Westbrook: P.

edwin: And then the idea, George, for me is like once you click your layout, um, you know, we can add this later, but for now they just whatever they choose, that's the route they're in. So like you know people who want to play for fun maybe after a while they want to play for money. We got to give them a way to get back in. Okay.

George Westbrook: Huh.

edwin: But like right now we don't. We just need

Brett StClair: But you always put that on your personal page,

  
  

### 00:19:55

  

edwin: them.

Brett StClair: right? When you go to your personal section, you know what? You got all your settings and everything. I want to get back in. Could go there,

edwin: Yeah.

Brett StClair: right?

edwin: Yeah. We'll go there.

Brett StClair: Kind of lives there as a holding space until you want to turn them faster into a kind of

edwin: Good call.

Brett StClair: more playable space, right?

edwin: Yeah.

Cody Haugen: Okay. So, I heard that was a negative one as well from George. Great. Moving forward.

Brett StClair: You got to score otherwise Cody

Cody Haugen: Otherwise,

Brett StClair: school.

Cody Haugen: everything's a negative one.

George Westbrook: Yeah, it's it's like a like like a What's the scoreing again?

edwin: Okay.

Cody Haugen: George.

George Westbrook: one like Yeah, that's fine.

Brett StClair: So one is that we find two we need to investigate.

George Westbrook: Two.

Brett StClair: Three we're worried about it.

George Westbrook: One. That's a

Cody Haugen: Okay. Good, good, good, lad. Um, all right.

George Westbrook: one.

Cody Haugen: For um, so this is one of the rarities where it is moving and substantial.

  
  

### 00:20:51

  

Cody Haugen: So I expect some some push back here, but it was more or less to clean up that homepage. So, moving the news from the bottom of the homepage up to an icon that lives next to that little flame that counts your signin uh tracker. A little button up there just becomes the news icon. So, you click on that icon up at the top. It's a new page you would have to create,

Brett StClair: Oh,

Cody Haugen: but that's how you get to the news section. It doesn't live at the bottom of the homepage. Gives us more real estate on the homepage to to either make it shorter or or more

George Westbrook: one.

Cody Haugen: concise.

George Westbrook: That's That's a one.

Cody Haugen: Hell yeah,

George Westbrook: That's fine.

Cody Haugen: George. That's what I like to hear.

Brett StClair: George likes

George Westbrook: Is it is it's because it's like with

Cody Haugen: All right. Um, easy button. Um,

Brett StClair: give.

George Westbrook: that it's like just context that it's like everything's everything's there.

  
  

### 00:21:36

  

Cody Haugen: okay.

George Westbrook: All the back end stuff it's just the way in which we expose it is slightly different. So it's it's that's why we always say it's like anything that's touching the back end that's where we got to be careful. But front end stuff is fine. We've got the data we've got the infrastructure to serve that data. It's just a matter of manipulating it.

Cody Haugen: Cool. Okay. Um, number five, it might be um it might actually be the case because we're in the trading section of the app, but that ticker needs to then go back to to any new user coming in. That ticker only needs to show flat IPO prices, no net change across those because right now in ours,

George Westbrook: Come on.

Cody Haugen: it shows net change.

George Westbrook: Yeah, that's that's fine. That's the

Cody Haugen: So, so anybody coming in just sees those IPO flat prices,

George Westbrook: one

Cody Haugen: no changing price. Um, Gamecast on the homepage. Let's change that to name it live games.

  
  

### 00:22:41

  

Brett StClair: That's a three.

Cody Haugen: f****** text change.

edwin: f****** Brett's always by the way if you give me a change order Brett

George Westbrook: Yeah, but you it's the iceberg. You got to be careful of the

edwin: Yeah,

George Westbrook: iceberg.

edwin: there's only one iceberg. It's in Brett's pants.

Cody Haugen: Um, so then if your news icon,

Brett StClair: Watch it.

Cody Haugen: George, if your news icon is at the top, then that makes the um movers, today's movers,

George Westbrook: Come

Cody Haugen: the bottom of the page. So we're on seven right now. Today's So today's movers is the bottom of the homepage, and that's it. It makes that homepage really clean and concise.

edwin: If

Cody Haugen: Yep.

edwin: efficient

Cody Haugen: Well, considering you don't have to move anything,

George Westbrook: on.

Cody Haugen: it's a negative one because movers is already at the bottom of the page if we remove

Brett StClair: Yep.

Cody Haugen: news. Uh uh. Okay. So, um Oh, sorry. It Okay, maybe it is a one because the results section.

  
  

### 00:23:44

  

Cody Haugen: So, if you look in there, there's the live games and then there was the results right underneath live games. Move results to the bottom underneath today's movers.

George Westbrook: Okay. And then Yeah. And then a separate in a separate little

Brett StClair: Yum.

Cody Haugen: Yep. So

edwin: It'll just be underneath because what when you're trading,

Brett StClair: Yum.

edwin: you go to the live games,

George Westbrook: section.

edwin: you see live games and then you'll see,

Cody Haugen: if

edwin: oh, which one's moving and you're like, okay, I want to trade that one. You know what I mean? So, it's it's basically trying to get the the eyes so you don't have to scroll a number of spots to like, you know, find what you're looking

Cody Haugen: yep

edwin: for. George, you have a a pick where you go like this. I'll go, "Hey, um, you know, I think I want to go fly a kite today." And you're like, and it's very judgmental. And it's it's almost like I'm like, "Fine,

George Westbrook: That's like That's a That's a That's

  
  

### 00:24:36

  

edwin: I'll just I'll just go clean my bedroom.

Brett StClair: I'll

George Westbrook: a

edwin: Yeah.

George Westbrook: Yeah.

Brett StClair: thunderstorm.

edwin: What I love about the sound is he doesn't say much and he's he's mad magic that way.

Cody Haugen: He stays he stays on mute and smiles and giggles with us.

edwin: Okay.

Brett StClair: Yes.

Cody Haugen: Um, okay. So, nine is a one as well, George.

George Westbrook: Yeah. Uh yeah. Yeah. Yeah. Come

Cody Haugen: All right. 11.

George Westbrook: on.

Cody Haugen: Now, this is an ad across all the pages, but the buy and sell in the gamecast section. Take that. But that needs to be persistent across all pages. And the buy and sell buttons need to be a little bit wider, a little bit

edwin: Well,

George Westbrook: the So the

edwin: you know, we're not going to do it wider and bigger because we're going to keep that,

Cody Haugen: bigger.

edwin: you know, that that tab that you click.

George Westbrook: thing

edwin: The thing that that was tough for me is So, we're keeping it the way it is.

  
  

### 00:25:34

  

edwin: And by the way, the only place to add it would be the homepage because it's on markets and it's on trade. Oh, so it's got to go on a homepage and

Brett StClair: Yeah.

George Westbrook: Yeah,

edwin: ranks.

George Westbrook: because I think the the the issue with making it bigger is it's like I'm always thinking fat fingers. So, obviously you the first thing you think is the make the buttons bigger,

Cody Haugen: Yeah.

George Westbrook: but then it's the there's the thing in the middle where you click to open up the order sheet um so that you can then do the changes.

edwin: Yeah. Yeah. So,

Cody Haugen: There's

edwin: it's it's and I almost want to I want to where it says like the quantity and at, it's not um it's not clear that that brings up an order ticket. So, instead of it having the quantity and the word uh the the symbol at, I want it to say order. So then you'll go

George Westbrook: One one thing I'd say is that is if somebody's

edwin: ahead.

George Westbrook: in oneclick trading mode, they how like I How are they meant to know the quantity of what they're what they're

  
  

### 00:26:42

  

edwin: Yeah, that's fair. So if I take off one, let me go there real quick.

George Westbrook: placing?

edwin: This m*********** George with all the answers. If I take off one click trading.

Cody Haugen: There.

edwin: Okay.

Brett StClair: There's some con in Oh, I win this game. Okay. The atom. has got a little up arrow when you're on the game cast.

George Westbrook: Wait,

Brett StClair: It doesn't have it anywhere

edwin: Yeah. Yeah.

George Westbrook: wait.

edwin: So

Brett StClair: else.

George Westbrook: Have you Have you done the OTAA,

edwin: like

George Westbrook: Brad?

Brett StClair: I haven't closed the app. Sorry. Let me clear that. Sorry. I should know that by now.

edwin: George is like these old f****.

Brett StClair: Yeah, there we go.

George Westbrook: Right. The

Brett StClair: George, George,

George Westbrook: boomer.

Brett StClair: my boomer OTAA moment has been cleared. Now I've got an upside down button. What the f*** you talking about

George Westbrook: What do you mean?

Brett StClair: there?

George Westbrook: Are you holding your phone the right way

  
  

### 00:27:47

  

edwin: Good s***.

Brett StClair: Oh, I see. I didn't realize you could scroll across and pick the sides when you're in the market. So, it starts at KC 300 at NYG 300 at and you can scroll that across. Did you guys see that?

edwin: No. Where you at?

Brett StClair: So on that trade button

edwin: On trade button.

Brett StClair: here,

edwin: Yeah. Pick a team.

Brett StClair: you can scroll that team across at the bottom there.

edwin: I'm not sure. Hold on. Let me pull it up. Can you show me?

Cody Haugen: Oh s***. Oh s***.

Brett StClair: Do it again.

Cody Haugen: Yeah. Yeah.

edwin: I can't see it.

Cody Haugen: Down in those. Yeah.

edwin: Hold on.

Brett StClair: That's cool.

Cody Haugen: Yeah.

edwin: Yeah.

Brett StClair: So you see that So you can actually move it

edwin: Oh, that's sick.

Brett StClair: to other teams to trade with off one click just scrolling

George Westbrook: And so

Brett StClair: across. That could get really interesting over time when we load some algorithms in there to start understanding how you're

  
  

### 00:28:51

  

George Westbrook: the

Brett StClair: trading and what you probably want to trade and load that. That becomes quite a powerful little utility. Nice one, George. I like that.

George Westbrook: it's how it's sorted.

edwin: f****** George. That's

George Westbrook: how it's how it's sorted as well. So on the on when there's two teams on a page,

edwin: sick.

George Westbrook: we're making the assumption that they're going to be the two teams that a user is going to want to trade. Obviously, um not to say that it's always going to be that that's where they click up. Um but how it's sorted on the other pages and also in the let's call it the swipe

Brett StClair: to the

George Westbrook: thing when you open the order sheet is think last traded team is the first team that shows

Brett StClair: thing.

George Westbrook: up on like the markets the trade and then then it's your watch list um and then after that then goes to

Brett StClair: Oh,

George Westbrook: alphabetical

Brett StClair: so good. And then it keeps the two on the game.

  
  

### 00:29:46

  

Brett StClair: f***. See, that's what I was thinking about like that being a bit more intelligent. And you've actually done that already. f****** excellent.

edwin: You're really a smart little f***. Nice work.

Cody Haugen: So, so George f******

Brett StClair: s***.

Cody Haugen: love the love the functionality. We Well, I guess it's more me and Edwin's problem. Like, once again, that's not a button that's intuitive, though, that anybody's ever gonna f****** find. And no one's going to see the brilliance in that because they don't know that's what it

Brett StClair: button. Side arrow. Up

Cody Haugen: does.

Brett StClair: arrow.

George Westbrook: the the issue with the app like I agree with you.

edwin: We just need to do a demo.

George Westbrook: It's Yeah.

edwin: We just need to do a demo on the app. I mean, at the end of the day, this thing is powerful and there's a lot you can do. You're not just going to pick it up and start being like, "Okay, I know it all." you know, just they got to go through a little bit of a a thing to to get the maximum output because that that function that you got there is really

  
  

### 00:30:43

  

Brett StClair: Oh, you know what you could do every now and then?

edwin: cool.

Brett StClair: You just jiggle it.

George Westbrook: could do actually.

Brett StClair: You know how you do a jiggle on the thing that shows the animation?

Cody Haugen: Yeah, that that Yep.

Brett StClair: It's like

Cody Haugen: That catches someone's eye. That's not a bad

Brett StClair: like a little a little I mean I don't I don't I don't know how easy that is.

George Westbrook: Yeah.

Cody Haugen: idea.

Brett StClair: Now I'm Now I'm sounding like Edwin.

edwin: You lucky f***.

Cody Haugen: Um, I don't even know what number we're on.

Brett StClair: Uh we won uh

George Westbrook: Have it.

Cody Haugen: Yeah. 11. Yes. Um,

Brett StClair: 22

Cody Haugen: okay. So, we we got the buy and sell feature. Um, 13. Oh, yeah. We got to get rid of the word short and it pops up in the uh order thing. So once you click the 250 at it brings you into the order page.

edwin: Thank

Cody Haugen: It still says short there.

  
  

### 00:31:47

  

Cody Haugen: It needs to say uh

edwin: you.

George Westbrook: So the beha the behavior we've got at the moment is if you own it,

Cody Haugen: sell.

George Westbrook: it says sell. If you don't own it, it says short. So we just want we just want sell no short. But obviously still the short functionality.

Cody Haugen: I mean I I like the short function because I understand what shorting it means. But Edwin, you you said you didn't want it because you think that would be confusing to people.

edwin: I do.

Cody Haugen: Okay. I I think selling something that you don't own is a more confusing term.

edwin: Yeah.

Cody Haugen: I think most of my generation and younger knows what shorting a stock means.

edwin: So, this is So, no, I I got you, but like I'm in the market right now by accident. I clicked I bought some of this s***. Philadelphia Eagles. And by the way, the market taker just stuffed it right in my ass. I bought 7066s. He drove it down to 7051. Welcome to the show.

  
  

### 00:32:46

  

edwin: Um, this f****** prick. Um, but like I go to sell right now and I already have a position on and it's telling me I need to short. Okay. So, that we can't have. We just want the buy and sell. We don't want to have to go through the explanation. It's a layer we don't need. Now, at the bottom, it's saying short sale, 1235 of these shares open a short position. 88,000 Hasan may reject if the stock isn't available to borrow. For the simulation, we just want it out there. So like you we're going to agree that uh man I just lost some money. We're going to agree that all the shares are available to borrow at all times. We don't need to go through a formal locate for the simulation.

George Westbrook: Okay, we need I think we need to have a look um as to what what T0's limitations are there because I think we probably need to double check to see if there they've got limitations on sorting as well. like maybe there's a certain quantity. Um,

  
  

### 00:34:00

  

edwin: Yeah, I told Troy this morning, I don't want to hear that. Like I just said, make it all always available. And you know the way that we can do it because like in in real markets,

George Westbrook: yeah.

edwin: they claim all this s***, dude. That they you can be sure like shares of stock can be 150% short. Like there's circumstances where and and by the way like with the derivatives you can get synthetically short and that's why you see sometimes you see the market rip on these squeezes because people find out that the the short side's just overloaded because they expect this company to go down in value but like some prick finds out okay everyone's short and they can't you know they can't buy them back. Um so they're going to get f*****. The only way to to get out is to buy higher. Like the GameStop, do you remember the GameStop memes?

George Westbrook: Yeah. Yeah. Yeah.

edwin: That was exactly what happened because that Gabe Platkin was short, you know, a few billion dollars worth of this stock and they f****** rammed it, you know, hard up that guy.

  
  

### 00:35:02

  

edwin: And um, you know, it was just, you know, it was what it was. But yeah, like I'll give another example. I know these four lunatics who in 2008 they made it illegal to sell short in US for a period of time. I don't know if you remember that Cody, but it actually happened. We were in the midst of a like that that crazy 2008 depression and these

Cody Haugen: Yeah. Yeah.

edwin: four kids I you know they're option guys. So you can build a synthetic short with an option uh product, you know, by you know, you basically synthetically you're short by the the puts and the calls and you could sell calls, you can buy puts and essentially you have a you have a short position anyway. And they made like 400 million bucks these four guys and they're some of the worst human beings I've ever met. You know, like what they've done with their money,

George Westbrook: Thank you.

edwin: they actually their their company's called Hardight. They actually have a plane and then on the plane they have two dice double force.

  
  

### 00:36:01

  

edwin: So the heartates lives out.

Brett StClair: Okay.

edwin: They're horrible people though. They used to hire like prostitutes to come to like parties,

Brett StClair: f***.

edwin: right? And then they would offer them money to do like degrading things in front of the entire thing. So like one of the degrading things was like, you know, we want you to call your dad and tell him that like you're getting paid 50 grand. Like he need to do stuff. I they're like they're really horrible people.

George Westbrook: Jesus

edwin: Yeah, they're just terrible money.

George Westbrook: Christ.

Brett StClair: So, we do something similar to that.

edwin: It's

Brett StClair: We pay Hasan a salary to sit next to George. It's close enough.

George Westbrook: f******

edwin: Yeah, it's it's e equally degrading.

George Westbrook: hilarious.

edwin: I mean, the one that's you got that high flyer max a million that

Brett StClair: Anybody?

edwin: guy he's like more like max a thousand. Um but yeah. Okay. So, anyways, back to this. What are you What are you thinking? Where we at

Cody Haugen: Uh,

  
  

### 00:37:02

  

Brett StClair: Okay, that's a two.

Cody Haugen: we are at uh we're at Yeah,

Brett StClair: Number 13's a

edwin: next?

Cody Haugen: we're at 14.

Brett StClair: two.

Cody Haugen: Um Oh, sorry. You're saying 13's a two. Got it.

Brett StClair: Yeah.

Cody Haugen: Uh,

Brett StClair: 15's a two, you know.

Cody Haugen: okay. 14.

edwin: Oh, on 13 being a two. Um,

Brett StClair: Yeah.

edwin: the big priority on that one. I don't want it to be short.

Cody Haugen: Um,

Brett StClair: Yeah.

edwin: I don't And that that should be done with P 0 in conjunction.

Brett StClair: Yeah. It's a T thing.

edwin: And and by the way,

Brett StClair: Yeah.

edwin: it's okay because we still got till next Saturday for that to occur because no one's going to sell any shares yet because they can't sell them. They can only buy them storage

Brett StClair: That's

edwin: again.

Cody Haugen: okay.

edwin: I'm flying that kite.

George Westbrook: That's a That's a There's a M.

Brett StClair: cool.

George Westbrook: That's like a Yeah. Then there's a M.

  
  

### 00:37:51

  

edwin: That's a no.

George Westbrook: That's a That's a

edwin: That's a maybe.

George Westbrook: Yeah.

Cody Haugen: That's that's I got to think about it. Um and then so then 14 is more of a T0 thing.

George Westbrook: Yeah.

Cody Haugen: Um but yeah, the to Edwin's point, I think he just talked about this that there should not be a locate function on this and then therefore you can remove the page confirmation on that. It's for shortened.

edwin: Yeah, because if I go into like you know my interactive broker account. I want to short stocks. It doesn't have a short button. It just says sell. And then like the short happens behind the scenes. And now I know I'm short. And then on my statement, it'll tell me, hey, you're short 500 shares. Here's what you're paying every night to borrow the shares. And that's the cost. So there's no like intramarket intraarket description of it. It's just a buy or sell.

Brett StClair: Are you clear on that? Hey, George.

George Westbrook: the the just just the cell button.

  
  

### 00:38:57

  

George Westbrook: That's really I mean changing the 14

Brett StClair: my

George Westbrook: the that we need to check with T0.

Brett StClair: Yeah.

Hasan Ahmed: Um,

George Westbrook: Um but

Hasan Ahmed: not

edwin: We'll get that fixed before next Saturday, not this Saturday. Like in terms of like priorities,

Hasan Ahmed: tonight.

edwin: that one can wait till next week if need be, right? But we'll get T0 to do what we want cuz I, you know,

Cody Haugen: Yeah.

edwin: I got to pay T0 and I want to put up what I want to put up. I I don't want it to be, you know, it just needs to be this way. It's the best way and that's the way it has to be.

Cody Haugen: Yeah.

edwin: Cool.

Cody Haugen: Okay.

Brett StClair: 14 142 Cool.

Cody Haugen: Sorry.

edwin: Next.

Cody Haugen: Going ahead to 16 then. Yep.

Brett StClair: Yeah.

Cody Haugen: Um so underneath so this is in the gamecast underneath the field. Um you know move those volatility moments down or shrink them down and add a percentage change based on that team's daily stocks change because so what

  
  

### 00:39:57

  

edwin: No, no, no. Hold on.

Cody Haugen: we did I not explain that

edwin: Let Let me describe this. No.

Cody Haugen: right?

edwin: Let Let me do it real simple. So, George on the order book, okay, which is below the um uh big moments, you know, cursors and all that, and where it says market and game, I want the order book tile to be directly under the field. So, I want to see the bid ask. I want to see the last. And instead of the spread, we're just going to take the net change. And you can do that in a like a number, not a percentage, but it'll be like plus, you know, 2.87. So that means up $287 cents of inplay bucks. So we'll call it that. And then on where it says like if you go lower where you have the actual order book, um, we don't have to show the whole order book either. You know, we can show less. We can do just the top of book if it's if we can get that space. And then for this page, we'll only show top of book, the bid ask, the last, and the net change.

  
  

### 00:41:04

  

edwin: And that would go right underneath the game. Because what I want to do is when I'm trading, I want to see all the things in what without having to scroll that are necessary for me to buy and sell

Brett StClair: How do I get to the order book on the

edwin: it. It's right underneath where it says marketing game.

Brett StClair: app?

edwin: Go here. Go to the uh front. Go to your homepage, Brett,

Brett StClair: Yeah.

edwin: and then click where it says results and preseason one. Click on Seattle Dallas and it'll take you to the gamecast.

Brett StClair: Yeah. Yeah.

edwin: And right now we it's it's very luxurious in terms of spacing where where

Brett StClair: There it is. Yeah.

edwin: it says end game, that's where we want the order book. And we don't even have to call it the order book.

Brett StClair: Yeah.

edwin: You can just have the the title bid ask last spread. Perfect. And then you know down below like where you have the selection of um the the Seattle or Dallas. If Seattle's se selected, that's the order book that's up.

  
  

### 00:42:05

  

edwin: If you select Dallas, like you would with the orders, that's the order book that's up. So, you currently have it right now where you can choose to the right of it. Um, Seattle or Dallas. Uh, I would just I would I wouldn't have those. I wouldn't have order book. I would just have the bid ask last spread and then um the top of book um bid and the ask.

George Westbrook: with the quantities as

edwin: Yes, with the quantity. So just the the first line and best bid,

George Westbrook: well.

edwin: first line and best offer. Sorry Cody, I just wanted to help out there.

Cody Haugen: No, no, no. I I I misunderstood when I was I mean, we were I was I was live transcribing these fools earlier on a call,

edwin: Yeah.

Cody Haugen: so I'm glad.

edwin: Right. And then then on the tiles then next what we would do right underneath that

Cody Haugen: Yeah.

edwin: George we would go open orders and then recent fills and then we would have the in-game moments for us to toggle through.

  
  

### 00:43:10

  

edwin: And underneath that you'd have the market in game

George Westbrook: H. So, Gamecast then did ask last

edwin: that change not spread.

George Westbrook: Fred or that new number the the change the the change.

edwin: Yep.

George Westbrook: I think that change when it what change in the in what time

edwin: So there'll be a settlement every day. So it'll be from that.

George Westbrook: period

edwin: So when when we do like um I think they settle it for one minute. The the the exchange is open 24/7. So um but they're going to close down for one minute and then whatever those prices are, we have what's called settlement. And that settlement is is the is where it settles that day. So if you're long and it settles at, you know, $5 up, you made $5 that day.

Brett StClair: What's

edwin: And now from that settlement, then everyone the convention in the in the business is that settlements are where everything deres the next day from. So like you know settlements is a key piece because that's how the money in in production gets transferred. You know how much did you make, how much did you lose?

  
  

### 00:44:22

  

edwin: There has to be a time period where it settles and from settlement is where the next stage derives its value. up, down, or all around. f***.

George Westbrook: Okay. But yeah, I think we we get that we get that number through from T0, I think,

edwin: Yeah.

George Westbrook: with with every order. So that that's fine.

edwin: Yeah.

George Westbrook: And then it's just the delta in that that's the number that we have. And it's a number, not a percentage.

edwin: Correct.

Brett StClair: So that's a one, right?

George Westbrook: Um, one and a off.

Cody Haugen: Oh, now we're making up f******

edwin: Yeah.

Cody Haugen: numbers, George.

edwin: Yep. He's going to round that to two.

George Westbrook: I got

edwin: By the way,

Cody Haugen: He's definitely I mean, he only rounds up. Um, well,

George Westbrook: absolutely.

edwin: this

Cody Haugen: I'm gonna discount it to a one because that actually is 17 and or sorry, that is 16 and 17.

Brett StClair: 16.

Cody Haugen: So, it's actually two points in one.

Brett StClair: Yeah.

edwin: is down to 1.5.

  
  

### 00:45:18

  

Cody Haugen: Um

edwin: We get a win. They owe us.

George Westbrook: Yeah.

Cody Haugen: um so then we're at uh 18 actually. And so as you're scrolling, so what I found is I actually found myself putting on my degenerate hat. I had the Packers and the Steelers game on my TV in my living room and I was glued to the f****** app just as we thought. But I I wasn't drinking my own Kool-Aid. I was just trading it like I would live betting a game. And I the reason for that is because that data on the live match tracker is faster than the TV. So we need to keep that field frozen to the top of a scroll. So if I'm scrolling down to see the deeper order buck there, I need to see this field still because it got lost and then I'm scrolling back and forth and then it's like, "Oh s***, did I put that order in?" That type of thing.

edwin: Yeah. Like if you want to if you want to see the chart, you want to scroll down.

  
  

### 00:46:16

  

edwin: as long as that like you know you're uh cuz like as long as the field you don't even have to show the bid ask cuz technically okay let me look at this real

Brett StClair: So, are you guys not on the game cast going to horizontal mode?

edwin: quick

Cody Haugen: So the only So so Brett,

Brett StClair: You're keeping your upright.

Cody Haugen: yeah, we can we can move to that quickly after this. The watch the watch is great, but it needs the buy sell buttons. Right now it has the orange trade button. That doesn't work that because then it takes you to the order book. You place that order, it routes you all the way back. It needs to buy and sell so you can stay on that watch.

edwin: Yeah,

Cody Haugen: Troy actually said he used it on his iPad and it was sick.

edwin: he showed us.

Cody Haugen: Um,

edwin: So, it's pretty

Cody Haugen: it was very good. So, yes,

edwin: good.

Cody Haugen: that the the buy and sell button needs to be added there to that watch tab and then I'd be much happier with the watch

  
  

### 00:47:09

  

Brett StClair: and still short as well.

Cody Haugen: tab.

Brett StClair: So, we're going to take that to sell, right?

Cody Haugen: Yes.

Brett StClair: Yeah. And so so the I think the the issues around on the

Cody Haugen: Um,

Brett StClair: um watch page uh so you're talking about this page

George Westbrook: No, no, no.

Cody Haugen: yeah.

Brett StClair: eh

George Westbrook: Click watch above the

Cody Haugen: And then and then yeah, click watch at the top of the screen above the

George Westbrook: game.

Cody Haugen: field.

edwin: Yeah.

Brett StClair: yeah no sorry I mean when it's not turned to the side when you're not turning side you're talking about

Cody Haugen: That is it.

Brett StClair: this you're wanting that

Cody Haugen: That is the page that I'm talking about. Freeze the field to the top of the screen. Yep.

George Westbrook: that I think that we've got to think about that because if we do that the

Brett StClair: Yeah.

George Westbrook: amount of usable space on the screen is tiny.

Cody Haugen: Yeah, but like you're only scrolling down for a quick second and then you're back up again.

  
  

### 00:48:01

  

Cody Haugen: Anyways,

edwin: Yeah, this is the showstopper.

Cody Haugen: um

edwin: This is like it doesn't matter if we can freeze that top.

Brett StClair: George, it's kind of like you need a freeze from there,

edwin: Let me put it like this.

Brett StClair: right?

edwin: Yeah, like here.

Brett StClair: The whole component is actually till there.

edwin: Let let me

Brett StClair: So,

Cody Haugen: yes

Brett StClair: it's kind of like we need two components so that that slips under.

edwin: Here,

Brett StClair: Does that

edwin: let let me let me let me offer this. If we can freeze the field underneath where it says end game, okay? Like, or directly under the actual grass, like just whatever, you know, give yourself a little bit of padding so it doesn't look jank. Um and then you don't have to make the changes any other changes right now.

George Westbrook: I I one one good thing is I started working on this today before this call. So I can kind of show part of it and already

edwin: Oh, really? Are you showing it?

Cody Haugen: Oh, do I need to stop showing?

  
  

### 00:49:05

  

edwin: Let me see.

Cody Haugen: Oh, wow. We get Google Meets. You can multi-share screens.

George Westbrook: I mean this was my concern today is it's that's the scrollable then

Brett StClair: Go.

George Westbrook: thought do this so that you can collapse it if you want then change this to this was

edwin: Yeah. So that that's what I want right there.

George Westbrook: this is this is

edwin: That like I don't want to collapse that that yet. I mean because here's the thing. you're going to be like, if you're if you're looking at the market and you're trading, that's all you give a f***

Brett StClair: But you see the score goes up.

Cody Haugen: Yep.

Brett StClair: It holds the score.

edwin: about.

Brett StClair: The actual just field you can collapse temporarily and bring back down. And so you've got everything there. It's not folding the score up. So you still see the score, still see your trading points.

edwin: I I understand.

Brett StClair: It's just the field.

edwin: I I would like to feel up there if possible.

  
  

### 00:50:01

  

George Westbrook: So it it it will be up there.

Brett StClair: Okay.

George Westbrook: So like it will it's just I think and then and then when if the user

edwin: Oh yeah. So that's great.

George Westbrook: wants so every single time they come in the default's going to be this but if they want the option to go like that they can.

edwin: Okay, perfect. Yeah,

George Westbrook: Um and then this is new.

edwin: I mean this looks great. Click on J George.

George Westbrook: The identity.

edwin: Go back and click on market and then scroll again. Yeah, that's f****** good. Great.

George Westbrook: And then this this is new.

edwin: Is there a buy sell on the bottom?

George Westbrook: Where is it?

edwin: I can't see.

Cody Haugen: Yes, there

George Westbrook: Yeah. So it's this this is new as well,

Cody Haugen: is

edwin: Okay.

Brett StClair: Is is that a buy cell with an up arrow,

George Westbrook: which an up arrow.

Brett StClair: George?

George Westbrook: Yes. And then get rid of that. We buy and sell. But this is like all the like detailed playbyplay data.

  
  

### 00:50:56

  

edwin: Wait. Love.

George Westbrook: Um so in on a live game what will happen is when a new

edwin: love.

George Westbrook: moment so let's say it is this is the latest that that will be like glowing green that's the most recent play. Then when a new event comes up it comes in it pops up then that starts

edwin: That's

George Westbrook: glowing green as well. This is for an old

edwin: Yeah. And you can you can go to that with the um screen the this the

George Westbrook: game.

edwin: uh game cast up, right? Yeah.

George Westbrook: Yeah,

edwin: It's f******

George Westbrook: I I think potentially what we maybe what we do is we get rid of this

edwin: great.

George Westbrook: timeline for space on a live game.

Brett StClair: Do you go that for the

edwin: You're talking about the like the like big moments in the game.

George Westbrook: So, no. So, keep keep the moment,

Brett StClair: live

George Westbrook: but it's it cuz if we're like this is it's going to look pretty similar in a in a live game.

  
  

### 00:51:58

  

George Westbrook: Um, well, it isn't actually because we're going to add this in here. So, we're going to add this, the beard, the ass, the last, and then the percent the the amount change. So if we added that in

edwin: Yeah. Yeah, George.

George Westbrook: here

edwin: I'm actually thinking on the order book of just having you quote the top of book. No, no more book depth anywhere.

George Westbrook: anywhere at all.

edwin: Yeah, I'm thinking about it.

George Westbrook: Why?

edwin: Not not for today's change. Um, so we can not I only want you to quote the top of book moving forward and I want to make sure that we're a little bit wider. We'll go easy on the the um messaging.

George Westbrook: So even in the market maker changing that so it only quotes the top of the book and then a wider spread.

edwin: Yes.

George Westbrook: What why this is not that's not like a why I don't think we should do it. It's just more inquisitive.

edwin: So, um I think what like my experience on Saturday was like in the first quarter the book was so thick and the it it looked like no matter what happened in the game, the price wasn't going to move.

  
  

### 00:53:10

  

edwin: So, the playbyplay didn't give me any kind of like tradable event. Like they didn't catch a big pass and the market move 12 cents my way. So like it was like it was it wasn't it didn't really matter until like it was clear who's going to win the game that it started to move the prices. What what we want is to make sure that the prices are moving around um not just the win percentage but the so like the win percentage is is x but there should be some like distance from the share price versus the uh win probability because win probabilities are a function of math but the share price are a function of market participants and so like for example let's say you've got win probability go to 89%. He's like, "Oh, yeah. Well, that's clearly going to And but there's a segment of the people who say, "No, no, no. This is a value play. I know this team. They're going to f****** lose. So, I'm going to sell them at 89. I'm going to get priced and I'm going to sell enough that I move the price into some kind of distance away from the fair value.

  
  

### 00:54:15

  

edwin: That's why I got the taker in there so that he can push the prices in a way that makes

George Westbrook: which

edwin: the like opportunity appear for people who want to trade, you know, tight to win percentage. And the problem with the like if you're going to be a tight win percentage trader on this, the moment you get run over, it's massive. So like you you collect nickels but get steamrolled when it goes against you.

George Westbrook: with the with the maker being obviously initially going to be providing almost all the liquidity and I suppose going forward as well because it's anchored

edwin: Yeah.

George Westbrook: just on that fair value isn't it always just going to go back to that like no matter no matter

edwin: Well, in theory, yes. But like um we're going we're going to modify it once we're like next week a little bit so that there's a little

George Westbrook: Oh,

edwin: bit more eb and flow. And so I want you basically to have like a distribution level away from fair value that the market maker will reside before it resets. And that that reset's probably going to be around 20 cents 25

  
  

### 00:55:19

  

George Westbrook: so do do we want to base that

edwin: cents.

George Westbrook: on market participation? So if let's say the there's people who are they they think

Brett StClair: Yeah.

George Westbrook: one one team's more likely to win but we've got the win percentage and at the moment because this what it seems like it's doing somebody puts puts it in. They're not moving the market at all because the market makers always f****** pushing it back to that fair

edwin: Well, and the right and the market makers didn't put up 11,000,

George Westbrook: value.

edwin: right? But if we're if we're quoting 500 or 600 and like you trade through um and let's say you just want to sell a,000 and it's only 500 on the bid, then that bid becomes the offer. Okay. And maybe go get your coffee and maybe um we keep the market maker away from the fair value for a period of time like you know maybe we're like okay well until like you know something changes within the win probability. Maybe that has to move another five% or something before we recalibrate where the market maker is going to then repost its bid ask because we want to have some some jiggering in there.

  
  

### 00:56:32

  

edwin: for lack of a better word, some nuance where the prices were going to move just because of the market forces which are more akin to a real market. You know, it's funny, George. I went through all that data from MIT the 25 years, right?

George Westbrook: Yeah.

edwin: And I spent the day building all these different strategies that could find an edge. And it's f****** tough. Oh my god, is it tough? But I found three edges, okay? And they they're profitable. even giving up the edge at Kalshi by taking their if you're a taker you have to pay four times the cross rate of a maker and the only way to confirm on a back test that you get filled is by being a taker so you could say okay there were a thousand up I can do a thousand now so when people run back tests it's always a little bit fugazy but um in this case you could say I would I would have bought those thousand and so Claude told me he's like um yeah you shouldn't sell this um strategy developer, you should just trade the three strategies in Cal sheet.

  
  

### 00:57:36

  

edwin: You'll make more money. I was like, okay, cool. And it's interesting because having it all pegged to the win probability makes it um not a very fun walk because it's too rigid, especially in the beginning of the games like when it's like first quarter and things happen in that first quarter. the win probability has it won't change a ton but the market can and the market can change by the participants and we want to give them that flexibility to do that. Okay. And like you can still the market maker can quote but it can quote you know much lower than it's currently quoting so the bid ask isn't as tight.

George Westbrook: Okay,

edwin: Does that make sense to you or do you think that's b*******?

George Westbrook: I'm going to need to look back at the call and then read and read read it through again. But I think on the surface, yeah. Um, but I think with the Maker, I think we want to we want to limit like simpler changes are fine. Like let's say one level that's I think when we're adding in new things that's where that's where we probably want to be a bit more careful in my opinion.

  
  

### 00:58:48

  

edwin: Yeah.

George Westbrook: Um,

edwin: I I just want to go wider on the quotes.

George Westbrook: but that's it's it's

edwin: So, we should be able to

George Westbrook: a two, but in terms of the market, like I think anything touching the makers, two at minimum.

edwin: two. Yeah.

George Westbrook: Um,

edwin: Yeah.

George Westbrook: but in terms of in terms of what we're changing, there's there could be a lot worse that that that we could change.

edwin: Right.

George Westbrook: Um, like I said, it's just changing. Okay. What what would be the ranges that you would be looking for? So like let's say I'll get the numbers. I'll get the parameters. I'll send them over and then if you could say well this the base spread needs to be X instead of Y.

edwin: Yeah.

George Westbrook: Um and then if this happens then we'll do a bit of research as

edwin: Yeah. Yeah.

George Westbrook: well.

edwin: I mean, you you just tell me when. Obviously, this doesn't have to be done by Saturday, right? This is like next Saturday that we might want to modify because we just like that first couple games,

  
  

### 00:59:40

  

George Westbrook: H.

edwin: we want people to feel like the market's moving every single play, no matter what quarter, right? And now it's not going to move as much in the first quarter than it will in the fourth quarter. But like certain catches and you know stops or interceptions in the fourth quarter should be worth $2,3 maybe.

George Westbrook: Huh?

edwin: You know it should be the closer you get to the end of the game if it's close you know you can have a fumble be worth five bucks you know it could be nuts and that's where it gets really really exciting you know

George Westbrook: I think with I suppose you'll know more about this than than me Cody, but with the sports radar data is it when when it comes to like live

Cody Haugen: Y

George Westbrook: games like those win probabilities are they getting updated more frequently than let's say a preseason

edwin: What

George Westbrook: game?

Cody Haugen: um they shouldn't be it should be across the board but I mean when

edwin: happened?

Cody Haugen: they when they do these sort of product updates they will use the pre-season as test sort thing just like any other just like we are.

  
  

### 01:00:52

  

Cody Haugen: Which is unfortunate,

George Westbrook: Yeah.

Cody Haugen: but I've gotten screamed at for 15 plus years about it because they're like, "Well, we're testing our f******

George Westbrook: Damn.

Cody Haugen: product. Why are you testing yours?" It's like, "Well, because it's a live game. Just like you're testing your product with a live game. We're testing our product with a live game." So, unfortunately, they use um the preeason to test products just as well.

George Westbrook: That's if anything I view that as a positive because it's like there was I think there was one game there was 36 minutes where there wasn't a probability update and I'm thinking if that's what it's going to be like like in in prod then it that could be an issue but if if that's what I assumed like said A live game is a live game. You can only test it when when it's going on. You can do all the simulations you want, but I said, a live game's a live

Cody Haugen: Yeah. Um, yeah, they still owe us an answer on that,

  
  

### 01:01:38

  

George Westbrook: game

Cody Haugen: too. Support's really f****** pissing me off. So, um, we can talk about that offline, but uh, all right, back to our list.

George Westbrook: and the NC and the NCAA win totals as well.

Cody Haugen: Yeah. Yeah, exactly. They're f****** pissing me off. Um,

edwin: We don't have What's that?

Cody Haugen: no. I got them from a different data provider because I'm a scrappy

George Westbrook: Um,

edwin: Wow. Wow.

Cody Haugen: f****** f***, but Sport Radar is pissing me the f***

edwin: Jesus.

Cody Haugen: off right

edwin: They're terrible. I mean,

Cody Haugen: now.

edwin: they're really s******* on your face cuz they're like, "Where's our press release and all that other

Cody Haugen: Yeah, there's like Yeah, it's just pissed me off.

edwin: b*******?

Cody Haugen: Um, 19's a scrap, so 19, don't worry about it. We we figured we're going to keep it as designed as you guys have it now. Um 20 did did I you and Jared were going back and forth on this one so much Edwin I don't know where we fell.

  
  

### 01:02:35

  

Cody Haugen: Market orders being the default, not limit

edwin: Um, yeah, you can make them default.

Cody Haugen: orders.

edwin: I mean, there just should be a button that's like a box or something something. It's like market orders default oneclick trading, you know, click, click, boom. You can one click and hit a market order.

Cody Haugen: Yeah.

edwin: I mean,

Cody Haugen: Okay.

edwin: you know, by the way, no professional trader unless they're smoked ever uses a market order ever. Like the idea of I' I've been trading for so long, I have never used a market order ever.

Cody Haugen: That's crazy.

edwin: I've only I'll click a limit order,

Cody Haugen: Yeah.

edwin: but that's

Cody Haugen: Yeah.

edwin: it.

Cody Haugen: Um, okay. So, that's 20, George. So, adding a setting change, I guess.

edwin: And that's it,

Cody Haugen: Uh,

edwin: right? Do I have more or that's it?

Cody Haugen: no. There's five more.

edwin: f***.

Cody Haugen: Let's rattle through them quick. Um, I think it's about to storm up here.

edwin: Yep.

Cody Haugen: I got to go pick up Mia.

  
  

### 01:03:37

  

Cody Haugen: But, uh, 21. This one's actually pretty sweet. So, uh, the flatten button.

edwin: Oh,

Cody Haugen: Um, yeah. So,

edwin: yeah.

Cody Haugen: to add a flatten button to exit all positions on that specific,

edwin: Two buttons.

Cody Haugen: uh, game. And then there's a flatten all button that exits all current open positions across all teams.

George Westbrook: Oh,

edwin: And those

George Westbrook: that's that nuclear nuclear

Cody Haugen: Yes,

edwin: cross,

Cody Haugen: nuclear. I'm either making a s***

George Westbrook: button.

Cody Haugen: ton of money and I want to get out immediately or I'm getting f****** railroaded and I need to re-evaluate my

edwin: by the way,

Cody Haugen: life.

edwin: I've been in both situations. I've been and they've been horrible. Okay? like the when the so at a prop firm I worked at like the manager would walk by and be like you know are you down 100 grand and I'd be like yeah he's like get up and I'm like and I'd have to hit that flatten all button and I'd be like f****** c********* I need more time you know it'll come

  
  

### 01:04:36

  

Cody Haugen: So yeah, the flatten is just for all positions across that one game. Flatten all is all positions across all games.

George Westbrook: Definitely a two minimum.

Cody Haugen: Okay. Uh,

George Westbrook: Definitely two at minimum.

Cody Haugen: yep.

edwin: You're a f***.

Cody Haugen: And,

edwin: You're a

Cody Haugen: uh,

edwin: tent.

Cody Haugen: 22, um, the user to be able to go back to 100.

George Westbrook: Yeah.

Cody Haugen: So, if they're at 100 grand, they're trading, they lose 2,000, they need to be able to re-up to 100 given they have the trading reserve from the referrals. If they are flat, they can do that at any point. Not at 25,000 anymore.

George Westbrook: Okay. So with no positions, they can use their referral dollars and instantly get those referral dollars deposited into their

edwin: correct. It'll top them off up to 100 grand.

George Westbrook: account.

edwin: Never over 100

Cody Haugen: Yeah, but he brings up a good point,

edwin: grand

Cody Haugen: Edwin, though. Instantly or because we're not doing daily prizes or do you do instantly?

  
  

### 01:05:37

  

edwin: instantly. Let them f******

Cody Haugen: Okay.

edwin: run through it all.

George Westbrook: So it's in instantly is easier.

edwin: And they keep calling

Cody Haugen: Yeah, fair point.

edwin: people.

Cody Haugen: Okay,

George Westbrook: Instantly is is is easier.

Cody Haugen: great.

George Westbrook: It's it's still one and a half two or two but one and a half. Stick at that. Um, it could, but if anything, it's easier than the current referral mechanism. Um because then we've got we've got to

edwin: Yeah, it's cleaner, too.

Cody Haugen: It's

edwin: And we just want people to go through it that money anyway because I you know what we want

Cody Haugen: Yeah,

George Westbrook: check

edwin: for the marketing is we haven't talked about that is that Colin Cody the videos

Cody Haugen: the marketing. Oh, the the the videos the videos are not on the section because I already gave Brett and George that that run.

edwin: Okay, cool. Okay,

Cody Haugen: This is this is all new from this

edwin: cool. Yeah, because if we can get like these,

Cody Haugen: morning.

  
  

### 01:06:28

  

edwin: you know, people to watch the videos and stay on the screen. And that's why I don't want that like um gamecast to scroll,

Cody Haugen: That screen to go

edwin: you know,

Cody Haugen: away.

edwin: if the videos stay on during halftime, they can still scroll below, they can buy and sell, they can do whatever. We catch the the edge on those videos.

Cody Haugen: Yep.

edwin: Um the the money is way better and you know hopefully we can you know generate enough users to where it actually makes some sense so we can make a little bit of

Cody Haugen: Yeah, it it's it the video ad across the the field is in my opinion the lowest hanging

edwin: money.

Cody Haugen: fruit for our our revenue programmatically.

George Westbrook: When you say across the field, do you mean

Cody Haugen: Just cover it the cover the field up like it can't be in the live match

George Westbrook: like

Cody Haugen: tracker. Um, it just has to cover the live mash tracker.

edwin: It's an overlay

Cody Haugen: Yes. Yep. But it's still But it does need to be able to slide with the

  
  

### 01:07:20

  

George Westbrook: that's because it's

edwin: basically.

George Westbrook: that that's more difficult than it seems.

Cody Haugen: screen.

George Westbrook: So the slide not sliding with it that's fine but then we're going into like events event based ads. So it's kind of like at the instant that it's this event be at a timeout then show the ad serve

edwin: Yes, it's it's it's a lot, but you know what? We can get it done. It again,

George Westbrook: it.

edwin: not doesn't have to be done Saturday. Maybe even next Saturday. Don't wor like we'll get into it. Um I think Cody, you mentioned that Sport Radar does give you this the the notification that Yeah.

Cody Haugen: They do.

edwin: Yeah.

Cody Haugen: Yeah, we we already displayed in the text, George, in that live match tracker. It says timeouts, uh TV timeout, end of first quarter,

edwin: So,

Cody Haugen: halftime. So, we can trigger off of those and then that programmatically should just automatically send

George Westbrook: It's so it's not so much about getting the event,

Cody Haugen: it.

George Westbrook: but it's given that event, serving it, then it's I obviously it's doable.

  
  

### 01:08:24

  

George Westbrook: Um Brett,

Cody Haugen: Yeah.

George Westbrook: if I'm saying anything that's just wrong here, jump in. But it's doable. It's just personally I don't think that's a priority for like now. I think what in

Cody Haugen: I would I would give this a priority, George. I would realistically say this is a September 9th priority before the first NFL

George Westbrook: what

edwin: Yeah.

Cody Haugen: game.

edwin: Yeah.

Cody Haugen: That is what they because it,

Brett StClair: I think there's two different priorities, right? There's the priority we need to get done this week and then we can load the

Cody Haugen: right? Well, yeah,

Brett StClair: rest.

Cody Haugen: we're we're saying the video ad specifically that gives us or, you know, gives us all roughly, you know, three and a half weeks to get that video ad spectacular overlaid across that

George Westbrook: Okay.

Brett StClair: So um we've done some research what I mean I'm speaking for you here

Cody Haugen: field.

George Westbrook: It

Brett StClair: um around the video ad and looks like to be able to insert on the field is going to be diff difficult because of how you just want an overlay.

  
  

### 01:09:20

  

Cody Haugen: We don't want it We don't want it inserted in the field over the field.

Brett StClair: Hey okay let's do

Cody Haugen: Yep.

edwin: Yeah, cuz like you like you remember how you're like, "Oh, generally these videos are like they pop up over the whole screen, you I I don't know.

Brett StClair: Yeah.

edwin: I don't want to tell you how to do your business.

Brett StClair: Reward and takes it all

edwin: Yeah.

Cody Haugen: No. Yeah. Yeah. We just want the size of the field. So,

Brett StClair: over.

Cody Haugen: whatever that top third is,

edwin: Yeah.

Cody Haugen: freeze it so people can still scroll, but we we need to make sure that they see that full 30 secondond ad. We get premium CPM for it and uh and they can still buy and sell during that just like a TV commercial.

Brett StClair: Um, so your only challenge there is full rate. Full rate on video is is tough because a lot of the advertisers are are still

Cody Haugen: Yeah.

Brett StClair: adopting it as a as a kind of platform.

  
  

### 01:10:12

  

Brett StClair: And so we'll we've set from

edwin: Bill rate from the you from the style side or the user

Cody Haugen: from the cell side.

Brett StClair: the sell side the exchange providing the inventory that you need.

edwin: because that Phil like why do you say that B?

Cody Haugen: Yep.

edwin: Because we're too

Brett StClair: No, just generally. So if you take the ecosystem of video of of ad spend,

edwin: new.

Brett StClair: your videos are really really really small amount of ad spend in that total inventory ecosystem. And so what we've done is the way to do it is we've set up a uh native banner it's called but an expandable native banner and then we've dis removed all the so you can if we're

edwin: Sure.

Brett StClair: not getting enough video impressions we can have a overlay banner that can replace we're not getting enough revenue from it because rates down and we can

edwin: Yeah.

Brett StClair: switch it up to do that and so you can either load a full kind of animated GIF styled image or you can download they'll load a video in there and I've just we've configured it at the moment just to be video but as you do it that give you these warnings they go inventory is going to be difficult to fill and when they're doing

  
  

### 01:11:15

  

edwin: Yeah. Sure.

Brett StClair: that and we just got

edwin: Yeah. It's interest. interesting because like I know the the f****** uh ad mob b*******, you know,

Brett StClair: No.

edwin: they look at everything as like a a website that's selling like dog treats, but you know, this this particular a lot of people would want to advertise on sports related stuff, especially when you're talking NFL and NCAA. So like having a video played albeit even if it's like 20,000 people or 50,000 people it's it's still really premium and

Brett StClair: So it just depends advertiser ecosystem,

edwin: prime.

Brett StClair: right? So, if you've got an advertiser that's only bought 100,000 impressions on that video, targeting that audience you're grabbing after a small share, right? Um, and then what was the other thing? We've tried to keep it as open as possible for now. So, the way you want to do an issue

edwin: Okay.

Brett StClair: all that kind of stuff and then we start tweaking and that's that whole process doing all this

edwin: Yeah.

Brett StClair: tweaking and that's hectic.

  
  

### 01:12:21

  

Cody Haugen: Yep.

Brett StClair: But you you want to start as wide as possible. You want every advertiser, every SSP, every exchange, every DSP to be going, "Oh, f***. There's a new kid on the

Cody Haugen: Yep.

Brett StClair: block."

Cody Haugen: We'll get there. Um okay four four uh four four left here.

Brett StClair: What number did we get to?

edwin: Yep.

Cody Haugen: All right. Uh 23. The market data um section or module square piece, whatever you call those things at the bottom of the gamecast page can just be deleted. It's repetitive information.

George Westbrook: That's a three.

edwin: Or it can or it can just be

Cody Haugen: That's a free um All right.

George Westbrook: That's a

edwin: left.

Cody Haugen: 24.

George Westbrook: one.

Cody Haugen: Um, oh, in the markets tab, if you go to a college football or in markets tab, go to college football, click on any team and then if you click on games, anything past week one doesn't populate. It's uh it's a broken page. So, we need to It works for NFL.

  
  

### 01:13:26

  

Cody Haugen: It doesn't work for college football.

edwin: Just they show the first game upcoming, not any of the

Cody Haugen: Yep. So there's no other and then if you click in it's a broken screen and you actually have to it's a bit of a cumbersome to

edwin: rest.

Cody Haugen: even get back to a visible

George Westbrook: Oh yeah, didn't notice that.

Cody Haugen: page.

George Westbrook: No, that so it it does show. You've just got for some reason there's a bug in that when you click on it, it doesn't show. When you click onto team and then go back to games, it does show.

Cody Haugen: Oh, that's weird. Okay. Well,

George Westbrook: That is weird.

Cody Haugen: leave it to leave it to Jared to f****** He's He's like this what do you call them? The exterminators. He's looking for like a cockroach underneath a chair that's been sitting there for 40 years,

edwin: He's like an idiot savant.

Cody Haugen: guys.

edwin: If you take out the

Cody Haugen: But of course, that's that's his one piece of feedback.

  
  

### 01:14:16

  

edwin: savant

Cody Haugen: That's what he found. f****** crazy. Um Okay. Uh and then uh 25. Yeah, go

George Westbrook: I'm back on the NCAA. Something I just thought. So,

Cody Haugen: ahead.

George Westbrook: I didn't realize this, but so 170 teams tradable. What was it? 138 um 138.

edwin: 138

Cody Haugen: 138 college football, 32 in NFL.

George Westbrook: And uh is the is there so

Cody Haugen: Yep.

George Westbrook: could there be a situation where let's say I've got the let's say the the Wyoming Cowboys so currently assuming it's a tradable team is going to play an untradeable team.

edwin: Yes.

Cody Haugen: It could happen this first week.

edwin: Yes.

George Westbrook: Okay.

Cody Haugen: We week week zero definitely could happen. And that's why I said

George Westbrook: Okay.

edwin: There's going to be 22 games like that this year.

Cody Haugen: Yeah.

George Westbrook: Okay.

edwin: something like that.

George Westbrook: That's that's like a one and a half two to sort that out when it needs to be sorted.

edwin: 22.

George Westbrook: It's not like a it's just not a negotiable.

  
  

### 01:15:21

  

George Westbrook: It needs to be sorted out.

edwin: Yeah. I mean,

George Westbrook: We just need

edwin: it's it's it's one of those things where the the team playing, they just get 250. They get the whole like enchilada for the ad revenue. That's why like North Dakota State is ranked so high in price for IPO

George Westbrook: Okay,

edwin: because they play a lot of non-division one schools. They make a bunch of 250s just because they they play s*** teams or small teams. I shouldn't say s***.

George Westbrook: that's forot as well.

Brett StClair: which are the small teams like little people.

George Westbrook: It's the board.

Brett StClair: Stay away from my bomb. Stop it.

George Westbrook: That's a f****** That's a f******

Brett StClair: Put the f******

George Westbrook: s*** joke.

Brett StClair: down.

George Westbrook: Right. I need to remember to put the black the black pen black pen mark on

Brett StClair: No, no, no. Get a a a what's it?

George Westbrook: the

Brett StClair: Inplay think they're technologists and George thinks he's the Arctic iceberg all

Cody Haugen: Well, Hasan looks like he's in the Arctic right now,

  
  

### 01:16:26

  

Brett StClair: going

Cody Haugen: but uh

George Westbrook: We're literally next to each other and he's got f****** joggers and a hoodie on. I'm in shorts and a

Cody Haugen: Oh, yeah.

George Westbrook: t-shirt.

Cody Haugen: I'm I'm sitting

edwin: I believe uh Hasan doesn't have any knickers on.

Hasan Ahmed: I don't know.

George Westbrook: I've got them in my pocket.

Brett StClair: we need to get a bad bad joke for Edwin actually that's actually had rening a lot of good jokes there to be

edwin: Well, they're all because I'm raging.

Brett StClair: honest.

edwin: Um, Brett, I have a question. Why do you have that fancy background all that all white? You look like you're doing an interview for Netflix.

Brett StClair: That's the point.

Cody Haugen: It is a real background.

Brett StClair: And then I've got you see the

Cody Haugen: Oh, I thought that was a Yeah,

Brett StClair: shadow.

Cody Haugen: I thought that was a uh

Brett StClair: So I got lighting both side and then I've got a big lighting rig here that cross covers and gets a

edwin: Yeah.

Cody Haugen: virtual.

Brett StClair: shadow across my face.

  
  

### 01:17:18

  

Brett StClair: And then I've got a camera with a what's it? And then I do podcast and

edwin: Are you saying that the Brett that I've deposited in my spank bank is not the Brett I'm going to see

Brett StClair: s***.

edwin: in person?

Cody Haugen: No,

Brett StClair: Oh yeah.

Cody Haugen: that close.

Brett StClair: Oh yeah. This is This is the makeup. This is the f****** s***. You must see when I crawl out of Marvel

Cody Haugen: I mean,

Brett StClair: usually.

Cody Haugen: this is that's the room he's shooting his his feet pictures in.

Brett StClair: Yeah.

edwin: I

Cody Haugen: Those ghettos, man.

Brett StClair: My my only fans page f******

edwin: bet.

George Westbrook: Yes.

Cody Haugen: Yeah.

Brett StClair: studio.

Cody Haugen: Wow. Just don't get a black light in

Brett StClair: Edwin. Edwin, thanks for your $500,

Cody Haugen: there.

Brett StClair: bud.

edwin: You're welcome. It was money well spent. Let's just say there's a a massage.

Cody Haugen: Four.

edwin: massage uh person that's that's going hungry this week.

Brett StClair: That sounds perfectly well

  
  

### 01:18:08

  

edwin: All right.

Cody Haugen: All right,

edwin: What's next,

Brett StClair: fed.

Cody Haugen: last two. Um the the max button in the um trade order page.

edwin: Cody?

Cody Haugen: We can just remove that because it doesn't make any sense.

George Westbrook: good

Cody Haugen: Yeah,

George Westbrook: one

Cody Haugen: it's just it's factoring off of a a total it doesn't work. Let's just say that. Um,

George Westbrook: is because I think how it's calculated at the moment it's like given your buying power what is the max that you could

Cody Haugen: yes. Yes. Yep.

George Westbrook: Okay.

Cody Haugen: Um, 26. What is 26?

Brett StClair: Yeah.

Cody Haugen: Adding the trading Oh. Uh, so this was a Jared. He got really mad that we removed the referral section from the homepage. So maybe we add a trading reserve referral with your code on the homepage, very small at the bottom. and just move.

Brett StClair: Heat.

edwin: underneath the like past games or you know recent games or

Cody Haugen: Yeah. Yeah.

  
  

### 01:18:57

  

Cody Haugen: The very the very thing. So, when you scroll, you're on your homepage, scroll to the bottom,

edwin: whatever

Cody Haugen: you can see your referral code and and that's where you get to it because he apparently can't click on the account and go to referral and go to the actual referral page. I don't know.

edwin: by the way.

Brett StClair: Jenz's

edwin: And if it's three, I'm not playing. I'm like, good lord.

George Westbrook: Wait, how how old is Jared?

Cody Haugen: He's like,

edwin: Six.

Cody Haugen: is he 26?

Brett StClair: what is

Cody Haugen: Yeah.

edwin: No, I'm just saying six. No, he's 28.

Brett StClair: 26.

edwin: I mean, what I know is like if I was Jared's dad,

Cody Haugen: Oh,

edwin: I'd be spanking that little f***** daily.

Brett StClair: Is that in a good way or a bad

George Westbrook: I was going to

edwin: No, that this would be discipline.

Brett StClair: way?

edwin: Not Not the way I'd spank you,

George Westbrook: say

edwin: Brett. That would be seduction,

Cody Haugen: yeah.

edwin: Brett.

Cody Haugen: All

edwin: If we can get this thing off the round, we make some money, I'm gonna be spanking you with like uh stacks of hundreds and we're both going to be

  
  

### 01:19:50

  

Cody Haugen: right.

Brett StClair: and just find me find me a little person.

edwin: aroused.

Brett StClair: I'm going to throw him on a dot board after

George Westbrook: Huh?

Brett StClair: that.

edwin: Awesome.

Cody Haugen: You guys are in some weird s***,

edwin: Anything?

Cody Haugen: man.

edwin: Yeah. Well, it's late over there. We got to add to the fire. Uh we got to make sure George the Ripper has something to do on the way home.

Cody Haugen: Yeah,

edwin: Um is there anything else on this list?

George Westbrook: Any question?

Cody Haugen: that that was that that was the list. We went almost two hours, Jen. So, appreciate your

edwin: Yeah. Yeah. We really appreciate your time. Have a good rest of the night and then we can convene tomorrow.

Cody Haugen: time.

edwin: Give it a look seeie. Come back to us. A couple of those though we definitely need by Saturday. Okay. Please do your best and um if if not by Saturday, you know, sometime quickly thereafter.

Brett StClair: Who's going to

edwin: Please.

George Westbrook: Let's

  
  

### 01:20:46

  

Brett StClair: say?

Cody Haugen: Let's f******

George Westbrook: go.

Cody Haugen: go. Georgie boy.

edwin: Yes, please. I mean, we got to do something,

Brett StClair: Yeah.

edwin: but like I've come to the grips that this first event is going to be an absolute s*** show for me. I'm going to lose probably two million bucks. Um, but I believe that we can still make money out of it in the long run.

Brett StClair: I

Cody Haugen: And I'm a complete disbeliever that he's losing two million bucks.

edwin: So,

Cody Haugen: But this is our this is our beauty of our banter back and forth.

Brett StClair: think

Cody Haugen: I think we're gonna get the f****** users.

edwin: I we're going to have users,

Cody Haugen: I think they're gonna I think they're gonna stroll in.

edwin: but like we don't have any f******

Cody Haugen: Oh,

edwin: ads, you know?

Cody Haugen: we're gonna we're gonna get the programmatic going.

edwin: We

Brett StClair: I'll come. Okay.

Cody Haugen: Phil rate be damned. We're gonna get some good video CPMs and I'm going to get these f****** to start buying some f****** subscriptions.

  
  

### 01:21:34

  

Cody Haugen: We've got we've got pass and we're gonna do

edwin: Yeah. Yeah. I mean, I will tell you this that that strategy builder,

Brett StClair: Agree.

Cody Haugen: it.

edwin: you got to spend some time with that to get something that overcomes that ass spread. Uh cuz like just not for inplay stuff. So, one thing that we can sort of just give you guys a real quick update, Cody and I and Kevin thought, okay, look, the the strategy development tool, why don't we just take it to market for prediction markets right now because they don't have any historical data. What we can do is we can normalize the data with either sport radar or you know oddly enough that MIT thing we wouldn't use but we'd use the sport radar data and then we would create a bid ask based on the normal bid ask uh spread around you know plays during games and things like that. So we could basically have you know 20 years of historical data that people can run prediction market uh strategies on and find out what works. And you know when you go over 25 years worth the edges get you know there's there's times that they swing and they go for like two three years and other times where they don't make money.

  
  

### 01:22:44

  

edwin: So like you know it's it's very much like regular trading because you can have the greatest strategy in the world and the shelf life on most of them is like three months you know maybe especially if it's a fast one. I mean the stuff that I trade for me I've been trading for 30 years. Um, that's that's there's no the edge is in the trader. It's not in the like speed or that, but it's it's a very, you know, tightly, you know, it works. It always works. It just sucks that it's it's hard. Um, but like with strategy tools, so we were thinking, look, we went out and I built the strategies. Three of them I said were profitable despite the cross of the bid ask. Um, but it took me about 18 hours to find them. And then um you know so we were thinking about trying to sell something to the prediction market crowd because they already have a market. They're already like everyone's losing money on that thing. So why not try to give them something that they can actually use to be profitable.

  
  

### 01:23:44

  

edwin: If that if they would raise the contract value up to maybe five bucks versus a dollar, it would be a much different game. Then the tool in prediction markets would be very valuable.

Brett StClair: Interesting.

edwin: But it is what it is. So we might do that.

Brett StClair: Yeah.

edwin: We may spin up a a business in the next two, three weeks to just start selling to the prediction markets where they can, you know, use the tool that we're going to use for input but use it solely for prediction markets until we get enough users to come in. Maybe we can get we figured we would charge somewhere between um and basically it would work like this, George. You'd find the strategy. I built a dashboard and then you you would also be able to have it uh coded and then you could manage the trade from your your dashboard. So you find the edge you you basically put it into production and then it it waits for the signal signal happens does the trade and you can manage it all from a a dashboard. So you find it research it test it works bing put it in the market b makes money bing you see the profitability on your your thing. So that's what we were thinking in terms of getting some quick revenue. Other than that, you know,

Brett StClair: Sure.

edwin: I just got to I got to start spending a little bit more time in the market myself, which it's going to be a little bit of a change. Cool.

George Westbrook: See

edwin: All right. Well, listen, enjoy your night.

Brett StClair: Sure.

edwin: Thank you so much for the time. We'll chat with you all tomorrow.

Cody Haugen: All right. Thanks, J.

George Westbrook: you tomorrow.

Cody Haugen: We'll talk soon.

Hasan Ahmed: All right.

George Westbrook: Let's f******

edwin: Thank you all.

George Westbrook: go.

edwin: See you,

Cody Haugen: All right.

Hasan Ahmed: Just

edwin: boys.

Cody Haugen: See you.

  
  

### Transcription ended after 01:25:28

  

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.

**