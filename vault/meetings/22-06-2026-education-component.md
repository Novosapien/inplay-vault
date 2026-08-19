---
date: 2026-06-22
type: component-session
scope:
  - "[[education/education]]"
status: extracted
extracted-to:
  - "[[education/education]]"
  - "[[components/components]]"
  - "[[vision]]"
  - "[[architecture/open-questions]]"
description: "Transcript and extraction table for the 2026-06-22 InPlay education component call — 36-module card-based redesign, rewards, badges and the paid research tab"
---

## Post-Call Analysis

> Focused **component deep-dive on [[education/education|Education]]**. This session reset the launch design of the component, so the extraction is a substantial rewrite of the education doc rather than an append.

| Finding | Destination | Action |
|---------|-------------|--------|
| **Format reversed** — TikTok 15-sec reels dropped for launch; now **card-based UI + slideshow / whiteboard videos with voiceover + text + quiz** | [[education/education]] §1-3 | Rewritten (reels noted as possible v2) |
| **36 modules across 3 tiers** (Beginner 16, Intermediate 10, Expert 10), replacing "12-15 modules" | [[education/education]] §1-2 | Rewritten |
| **Non-sequential access** — jump to any module; only reward sequencing matters | [[education/education]] §2 | Rewritten |
| **Progress display** — completed modules grayed but visible (revisitable), resume to point in course | [[education/education]] §2 (Progress Tracking) | Rewritten |
| **Reward = 100 InPlay coins (referral credits) per module**, earn-once | [[education/education]] §2 (Reward Integration) | Added |
| **In-module glossary** (swipe right at module end) | [[education/education]] §2 | Added |
| **Certification & Badges** — profile "Certs" section, tiered certs, clickable badge entry points | [[education/education]] | New 8th sub-component |
| **AI Chatbot deferred to Phase 2**; Phase 1 ships no in-app chatbot | [[education/education]] (AI Chatbot Support) | Status → Phase 2 / deferred |
| **Sponsorship = slide-group level** (not whole-module exclusive); skippable pre-video CPM ads; rotating sponsor splash screen (backlog) | [[education/education]] (Sponsor Ownership Layer) + [[advertising/advertising]] | Updated |
| **Production pipeline** — AI-generated slideshow/whiteboard, pilot 1-2 modules then replicate; condensed text for all 36 first; hosted on YouTube channel | [[education/education]] §4 | Updated |
| **Website FAQ + disclaimers** separate from Education, legal review (Brian) before publish; OG/social card metadata | [[education/education]] (Education-on-Website) | Updated |
| **Premium Sport Radar data resale + paid AI companion + tiered pricing** | [[architecture/open-questions]] → flag for **Research Tab** session | Out of Education scope; flagged |
| Status reflects a dedicated deep-dive | [[education/education]] / [[components/components]] / [[vision]] | Status: **Defined (updated 22-06)** |

**

Jun 22, 2026

## InPlay Digital - Component Education - Transcript

### 00:00:11

  

Max Kingaby: Yes.

Inplay Global: Oh, yes. I mean, when you drink, you feel like you're sleeping, but you're actually not. No, you never reach that red sleep. Get that drunk sleep.

Edwin Johnson: What's up, boys?

Inplay Global: It's the camera's all weird. It's tilted down. Oh,

Edwin Johnson: Looking at Brian's lap.

Inplay Global: wow. It is Monday.

Edwin Johnson: Oh, there's Kevin. A dream come true.

Inplay Global: Why is it just focused on something? I don't know. I think it's maybe because you're talking.

Edwin Johnson: What's up,

Inplay Global: There we

Edwin Johnson: Novo team?

Brett StClair: There we go.

George Westbrook: Are we doing it?

Brett StClair: Hello.

Inplay Global: go.

Edwin Johnson: Before Sky gets on, Brett,

Brett StClair: Hello.

Edwin Johnson: you look like you uh were given a very pleasurable weekend. You've got that after.

Brett StClair: I had my oats in the

Edwin Johnson: Okay. Well, if you're selling any kind of like pills that get that to happen,

Brett StClair: morning.

Edwin Johnson: I'm a buyer.

George Westbrook: I think the one he used this weekend was blue.

  
  

### 00:01:12

  

George Westbrook: I think that's what he was saying.

Edwin Johnson: A big pill.

Inplay Global: Blue pillow. Oh, blue

Edwin Johnson: The problem is, George, someone has to teach them it goes in the mouth

Inplay Global: pillow.

Edwin Johnson: first.

Brett StClair: They're not supposed

Inplay Global: This is how we're starting. Okay.

Brett StClair: to.

George Westbrook: Start the week off with a

Edwin Johnson: We got two Listen,

George Westbrook: bang.

Edwin Johnson: we got two months left. Today is June 22nd.

Inplay Global: That's right. That is

George Westbrook: Let's f******

Edwin Johnson: f******

Brett StClair: Did anyone notice her son her son got a haircut for this

George Westbrook: go.

Edwin Johnson: autan.

Inplay Global: fast.

Brett StClair: occasion?

Edwin Johnson: I don't want you to touch that pillow again. You got beautiful hair. I don't want it gone.

Hasan Mohammed Ahmed: Yeah.

Edwin Johnson: All

Hasan Mohammed Ahmed: I mean, to be fair, it's getting really hot here,

Edwin Johnson: right.

Hasan Mohammed Ahmed: so had to trim it down a bit.

George Westbrook: That's

Hasan Mohammed Ahmed: A little bit, you know.

  
  

### 00:01:58

  

Edwin Johnson: You know,

George Westbrook: it.

Edwin Johnson: I've read on the internet that a little glistening of sweat is what the um will make you very attractive to people. So, just a little glisten. That's what Matt Max told me. Anyways, I mean Max has a little website. It's, you know, how to be like me and I I follow it religiously

George Westbrook: You're the only one.

Max Kingaby: Yeah,

George Westbrook: There's only one subscriber and they keep reviewing that

Max Kingaby: there's only one subscriber and they keep reviewing that page.

Edwin Johnson: because if the thing is,

Max Kingaby: Who that was?

George Westbrook: page.

Edwin Johnson: Max, if I can't have you, no one will.

Inplay Global: What the f***? Oh gosh. One

Brett StClair: Oh man. So I clearly clearly Edwin you also got your oats by the sounds of

Inplay Global: subscribe.

Edwin Johnson: No, I've been working all weekend.

Brett StClair: it.

Edwin Johnson: I I'm so sick of this company and this b*******. I just I'm delirious to be honest with you. I spent the weekend writing the uh uh offering circular for the regulators.

  
  

### 00:02:51

  

Inplay Global: Be awesome.

Edwin Johnson: We need to get that submitted ASAP. So, um, pretty pretty interesting weekend, though. We we've had a couple of things happen.

Brett StClair: No.

Edwin Johnson: I don't know if you're aware. Did, uh, Kevin, did you tell this group that you basically got us some, um, like directors and s*** like that of some famous movies that we're talking to?

Inplay Global: No, I haven't spoken to anyone. Just yourself.

Edwin Johnson: Oh, okay. Do you want to give a quick update? That's interesting.

Inplay Global: Yes. So, I was speaking to um a guy last week and then uh gave him the pitch on what we're doing and he was like, "Hold on there." He said, "I need to get someone on the call." and he brought this guy uh Tom in for a call and he's produced he was one of the main directors for the Fast and the Furious franchise. So I spoke to him and then sent him the deck and sent him all our info. So hopefully to hear back from him uh later today or tomorrow

  
  

### 00:03:45

  

Edwin Johnson: Yeah. Oddly enough, that group has a small investment.

Inplay Global: with

Edwin Johnson: Well, I don't know how small. It could be large. They have an investment group. They also did the Avengers, too. That Captain America stuff. That's not my, you know, I'm I'm just into, you know, other kinds of movies. uh you know less than you

Brett StClair: Max Kimovk king.com

Edwin Johnson: know that you know something along those lines. Yeah. And you know it's more of a it's more of a journey than a movie with Max King.

Brett StClair: phone.

Edwin Johnson: It's his his a young man's awakening to the world. Um so we'll see.

Max Kingaby: What chapter are you on,

George Westbrook: Watch out for you.

Max Kingaby: Edwin?

Edwin Johnson: I'm sorry.

Max Kingaby: What chapter are you

George Westbrook: Watch your

Edwin Johnson: Well,

Max Kingaby: on?

Edwin Johnson: I can't get out of chapter one because it's a real tearjerker.

George Westbrook: team.

Max Kingaby: Wait till you get to chapter five.

Edwin Johnson: Oh,

  
  

### 00:04:31

  

Max Kingaby: It's the good stuff.

Edwin Johnson: the tales of erotica. I saw that. I gotta build up some stamina for that though, Max. Um, yeah, we we also had a a really interesting conversation with um the pay.com people, which which was uh uh you know, very interesting. So, they brought us that Hard Rock Digital. um and Hard Rock Digital. Oddly enough, the the executive chairman said that, you know, he had come up with a concept very similar uh to what we have. Okay. Uh you know, a lot of people have thought about ways to do this. So, it's not, you know, that's not that uh earthshattering, but interestingly enough, um that was a very very good conversation. Are you familiar with um this company called Playtech at all? You ever heard of Playtech? No. They're a UK company. They basically started in the late 90s. They They're probably older than Max, but they they sell a lot of It's gaming platform, right,

Inplay Global: Yes. So they they tie in for a tier one operator or sports book.

  
  

### 00:05:34

  

Edwin Johnson: Cody?

Inplay Global: There's everything that we're trying to do times 10, right? KYC, CRM, player management, all of that type of stuff. And a sports book, if they have enough money and they want to launch fast enough, they'll go to these platform providers that have all of the partnerships already rolled into one. And then it's a white label service that they just sell to operator after

Edwin Johnson: Yeah. So, the founder of that company is a guy named Teddy Sige.

Inplay Global: operator.

Edwin Johnson: You ever hear of him in the UK? Okay. He's a wealthy Israeli. You've heard of him, right, Max?

Max Kingaby: Yes.

George Westbrook: Yeah,

Max Kingaby: Does he own the market?

George Westbrook: I have

Max Kingaby: I'm pretty sure he does.

Edwin Johnson: Yes,

George Westbrook: the

Edwin Johnson: he does.

Max Kingaby: Yes.

Edwin Johnson: Yeah. Yeah. So,

Max Kingaby: feel so proud of myself and

Edwin Johnson: he was a Yeah. No, he was also dating Bar Raphaeli, too, for a while. So, I mean, based on the pictures I saw, he's probably got a lot of money based on pictures.

  
  

### 00:06:40

  

Edwin Johnson: Um, anyways,

Inplay Global: Okay.

Edwin Johnson: he um he was the founder of Playtech and he took that company public. When we met with the Pay.com people in Florida, they they basically the CEO and I did three calls with one earpiece in his ear and my one earpiece in mine and we call three billionaire friends of his or business partners of his and they're all somehow uh affiliated with this Teddy Sige. Okay. There's uh what what's the name of that casino sweep stakes? Cody Crown

Inplay Global: Oh yeah yeah yeah. Crown Casino and then

Edwin Johnson: Chumba. Yeah.

George Westbrook: Hey,

Edwin Johnson: So the guy So I spoke to Teddy Sige,

Inplay Global: Jumba

Edwin Johnson: the founder and owner of those two sweep stakes casinos and one other gentleman. And they're all from they're all within this realm of this really wealthy Israeli guy. Um so you know we pitched them down in Florida, Florida. And then um last week this uh gentleman from Hard Rock Digital really liked what we talked about.

  
  

### 00:07:43

  

Edwin Johnson: We were scheduled for I think 45 minutes, maybe an hour, but we definitely went over and um you know they he saw a lot of opportunities for Hard Rock Digital to partner with us in some way. They have 8 million uh loyalty members and all these different things, right, that they'd like to bring into the mix. He really understood the model pretty well. Um, yeah. And then after that call, I got a I got a text and said that uh Teddy Sigis CEO and I are going to do a call tomorrow. So interesting. Um there could be some real momentum here. He also owns something called ExpressVPN. Okay. And ExpressVPN.

Brett StClair: I like

Edwin Johnson: Yep. Um there, you know,

Brett StClair: this.

Edwin Johnson: that's a business to consumer product and it might be, you know, right up the alley of advertising with us here. So, couple of couple of good things. I got a I got a meeting with Goldman Sachs on Wednesday as well. So, um we'll see how that goes.

  
  

### 00:08:44

  

Edwin Johnson: You know, we're pushing everything we can here. I reached out to a company called Cats Media. I had a little go uh back and forth and then another um Navastar,

Brett StClair: No.

Edwin Johnson: which owns a bunch of television stations. So, I've had some go between back and forth with them. And then obviously tomorrow we're going to talk to your pretty boy Wayne. We're going to dirty him up a little bit and then um see if we can't make some magic happen there because I'd

Brett StClair: Yeah.

Edwin Johnson: really I'd really like to get some momentum over these next two months.

Brett StClair: I

Edwin Johnson: I'm worried, you know, I'm really worried that you know this this we've bit off a lot we could chew,

Brett StClair: agree.

Edwin Johnson: you know, a lot to chew financially. I want to make sure that we're not in soup.

Brett StClair: Yeah,

Edwin Johnson: Okay. So, that's our our update from

Brett StClair: good. Well done. Well

Inplay Global: Well, I got to pick up one more for you as well.

  
  

### 00:09:36

  

Inplay Global: Uh, or two more. So, yeah,

Edwin Johnson: last.

Brett StClair: done.

Inplay Global: Terry is going to give me a call this afternoon. He's meeting with the head of North America this morning and the head of global gaming um for Paysafe um just for the rest of the group. Um, so we also met down with them at SBC in Florida. Um, so they are meeting about us specifically. So good, bad, and different. I'll have an update from Terry uh later this afternoon. And then also speaking with a uh another one of a sport radar, but uh he's ran a couple uh advertising companies.

Edwin Johnson: Cool.

Inplay Global: So, I'm going to chat with him, see if there's uh other things we can do around the SSP or help us get set uh all that set up and moving in the right direction.

Edwin Johnson: And then did you ever hear back from that curling league

Inplay Global: Uh Nick,

Edwin Johnson: guy?

Inplay Global: uh no, he's he's busy closing his round, but he said he'll get back to me this week.

  
  

### 00:10:34

  

Edwin Johnson: Cool.

Inplay Global: Rock League, the new curling league in Canada. He's he's an old buddy, but yeah, he's launching his own curling league. This his new venture.

Edwin Johnson: And away we go. So, I mean, uh, we're we're pounding it. We've got everyone doing all we can. Uh, we're we need to get some ads.

Inplay Global: Yeah.

Edwin Johnson: Now, I will say I if you're gonna do a demo on the app updates, it's pretty f****** badass, George, because I was planning with it over the weekend, Max Hassan. Really cool s***. Um the ads are awesome. You know, there's the now you click through on Door Dash or whatever. I'll let I won't steal your thunder, but I was definitely active looking at it this weekend. Um and then I got a question for you. Like if we're going to do a demo, okay, and let's say we're on a Zoom like this or Teams, um it's really cumbersome to just bring up the app because you can't see it. How how is it is it a lift at all to have like a robust desktop version or is that something that you can just be like, "Hey, AI, make it desktop and then we get it." So,

  
  

### 00:11:43

  

George Westbrook: um desk.

Edwin Johnson: you know what I'm saying?

George Westbrook: There's ways to Yeah.

Edwin Johnson: It's like you want to be able to share your

Inplay Global: or web based or web-

Edwin Johnson: screen

Inplay Global: based or you know that the app that can be accessed through a URL or through a web

Edwin Johnson: cuz when we do it on the web now, George,

Inplay Global: browser

Edwin Johnson: it looks like the space and gapping it just it's not great for for our

George Westbrook: Yeah. Let me let me show you something quickly that makes the that sort the spacing out.

Edwin Johnson: purpose.

Brett StClair: Yeah,

George Westbrook: Let me just

Brett StClair: I was about to say if you drag your browser smaller, it'll size to the browser landscape,

Edwin Johnson: Oh,

Brett StClair: which might be a a nice easy start.

Edwin Johnson: really?

Brett StClair: Yeah, I'll show you. Let's Are you pulling it up,

George Westbrook: Yeah,

Brett StClair: George?

George Westbrook: I'm just trying to get the

Edwin Johnson: That's

Brett StClair: Oh, there's

Inplay Global: And while you do that, two quick updates from my side.

  
  

### 00:12:25

  

George Westbrook: URL.

Inplay Global: So I I have a call a follow up with Zero Hash this week too about potentially being an advertiser who's the

Brett StClair: something.

Inplay Global: stable coin that TZ uses. And then uh I was showing the app off a lot over the weekend because I went to two barbecues on Saturday and everyone agrees it's one of the best things they've ever seen in the sports space and they would use it pretty pretty aggressively.

Brett StClair: Superb.

Inplay Global: Like one one guy's like I wouldn't put this down all day on Sunday. Yeah.

Edwin Johnson: I mean, isn't it crazy, Troy?

Inplay Global: Literally he literally said I would watch games I don't care about just to use this app.

Brett StClair: Beautiful.

Edwin Johnson: Isn't it crazy that validation, you know, and I think we're also missing something too,

George Westbrook: H.

Edwin Johnson: Brett? Like I, you know, we talk about all these engagement minutes and how many games there are. We forget it's 142 consecutive days. People are going to trade this s*** when the games aren't playing.

  
  

### 00:13:22

  

Edwin Johnson: They're going to be engaged.

Brett StClair: Okay.

Edwin Johnson: I mean,

Inplay Global: Yeah,

Edwin Johnson: that's a that's 142 day. That's a lot of

Inplay Global: went.

Edwin Johnson: days.

Brett StClair: George, I think I have it. Do you have

George Westbrook: So yeah. Yeah. Can you can you all see this here?

Brett StClair: it?

Edwin Johnson: Yeah.

George Westbrook: So, one option is you right click and then go to this thing that says inspect and then usually it will pop up like this. So, if I just Yeah.

Edwin Johnson: No, it was it was right the first time. Yeah.

George Westbrook: So if you if you go inspect then it might pop up like this and then if you go up to the top

Edwin Johnson: Okay,

George Westbrook: where it says dimensions and then click a mobile one and

Edwin Johnson: that's cool.

George Westbrook: then command plus actually know you can and then zoom it

Edwin Johnson: Yeah.

George Westbrook: in and then you use it here like you would on your

Edwin Johnson: Okay, that that's perfect.

  
  

### 00:14:19

  

George Westbrook: phone.

Inplay Global: Yeah,

Edwin Johnson: That's perfect. So,

Inplay Global: great

Edwin Johnson: for our next couple calls, guys, we should have this ready to go like

Inplay Global: sitting on your one of your tabs on the side somewhere.

Edwin Johnson: that.

Inplay Global: Always always accessible.

Edwin Johnson: You know, because Troy,

George Westbrook: One thing you could do

Edwin Johnson: when you were giving your demo, did you show anybody like did you make any

George Westbrook: actually

Inplay Global: Yeah, I made a trade and I showed the gamecast and how it showed the touchdown.

Edwin Johnson: trades?

Inplay Global: I showed the chart. It was I mean like the the guys were kind of geeking over it. So, um and actually one one woman too was kind of like this is awesome. She's like I would play I would use this for my fantasy football is what she said.

Edwin Johnson: Yeah.

Inplay Global: Yeah. I told you I'm not crazy because they would watch the games that their fantasy football players are tied to and not have to watch the game on TV.

  
  

### 00:15:11

  

Inplay Global: They would watch it through our app. Yeah.

George Westbrook: One thing you could do as

Inplay Global: Ended up being like non-stop talking work on Saturday because like,

Brett StClair: What's

George Westbrook: Oh,

Inplay Global: well, what's going on with the job? I'm like, well, let me show you what's going on. What's the job? Yeah. A lot. Yeah, it is. It's most Yeah.

George Westbrook: one one thing you

Edwin Johnson: Did you say you're not crazy,

Inplay Global: Uh,

Edwin Johnson: Cody?

Inplay Global: no.

George Westbrook: could

Inplay Global: Because Troy just validated what I've been saying for months that some the woman he was

Edwin Johnson: Okay.

Inplay Global: talking to said she would watch the games and use it for fantasy and not even necessarily trade it, but would use the app for research and watching the games through the live match tracker. And I said, finally, I'm I'm validated on what I've been saying for months at a time.

Edwin Johnson: What kind of fantasies is this woman having?

Inplay Global: That's perfect. Kind of she wants Cody in it.

  
  

### 00:16:00

  

Edwin Johnson: Well, Cody,

Inplay Global: kind of

Edwin Johnson: Cody, this is bizarre. I had a dream uh last night that you and I went to my high school reunion

Inplay Global: fancy

Edwin Johnson: and um you were helping me get dressed so I look cool. f****** weird as Yeah.

Inplay Global: like put your pants on kind of get dressed or like we went down in a

Edwin Johnson: Like I mean he was kind of laying it out for me and he's like you got to put this cumber bun on and I

Inplay Global: row.

Edwin Johnson: Okay.

Inplay Global: Oh, if it's You've made a couple of my dreams as well. We'll leave it at that.

Edwin Johnson: Yeah, everybody likes those old pervert dreams.

George Westbrook: But one quick thing as well with

Edwin Johnson: Those are the best.

George Westbrook: demos is if you want to what you could do when you're on the call is join on your phone as well. Um,

Edwin Johnson: Oh, that's

George Westbrook: so I'm sharing sharing the screen here and then

Edwin Johnson: cool.

George Westbrook: then you can go on to it.

  
  

### 00:16:57

  

Edwin Johnson: Sweet.

George Westbrook: It's just not as it's a little bit

Edwin Johnson: Sure.

George Westbrook: jumpy.

Inplay Global: And the link hasn't changed. Correct,

Edwin Johnson: Sure.

Inplay Global: George. It's the same link as the last one.

George Westbrook: Yes. Yeah. The same link and then the the updates get get pushed to that one.

Inplay Global: Yeah.

George Westbrook: We should leave from here now. There we

Edwin Johnson: Cool. All right. Well, Nova, we'll let you take over. You're running this show today.

George Westbrook: go.

Brett StClair: So education, who's got one? Not me. So I'm going to hand over to someone who has.

Inplay Global: All right, Kevin.

Brett StClair: So um yeah.

Inplay Global: So Kevin, you want to show what you started with? Yeah.

Brett StClair: Do you guys want to jump in with some of your ideas and what you're looking to create and then we'll walk through

Inplay Global: log on your computer. Just make sure you mute

Brett StClair: experience?

Inplay Global: your Kevin's pulling it up,

  
  

### 00:17:58

  

George Westbrook: Because I think one of the things we need to think as well is in terms of like phasing like obviously end state

Inplay Global: folks.

George Westbrook: but then what are what we going to get done for when it's when it's launched or even in the pre-launch app as well. Um, thinking about what's needed at pre-launch, if anything at all. Um, which obviously I think there probably should be some stuff. Um, and then what do we need for launch and then what is the the golden goose? What is the the best example of what we want the education to look like?

Brett StClair: There we go.

Inplay Global: Okay, zoom in on

Edwin Johnson: Thanks, Brad. I can't see it either.

Inplay Global: You see that?

Brett StClair: Uh, at the bottom you'll see a slider. It's on 69% George's favorite number.

Inplay Global: default. There it is.

George Westbrook: Wait.

Inplay Global: 69. Yeah. Now you should be able. Okay. So, yeah, pretty much now with the education I went through with Brett as well uh last week.

  
  

### 00:19:48

  

Inplay Global: Um so, both of us have sort of confirmed this that's all working and makes sense for for everyone. Um, but so again, this is the education one for the new users. So, anyone that's never traded stocks before. So, again, this one can be uploaded uh George as well to your AI um and then we can go through. But what we're looking at here then is obviously 16 modules uh with then 16 video lessons that we will create. Um and then we did it with earn 100 uh inplay coins for every module that you complete. So you can either do it two ways. You can either watch the video and then just scroll down and take the quiz or again if you want to read through everything you can do. I think having the two options of the education stuff will be very valuable because again some people might just glance over it um as well and then obviously then there's there's an intermediate level and then an expert level as well. So, do you want me to click through all the pages or do you want

  
  

### 00:20:57

  

George Westbrook: Yeah, it'd be it'd be it'd be good to have a look at what what they look like because just working out if we'd need to condense any

Inplay Global: to?

George Westbrook: of them down for like mobile mobile reading.

Inplay Global: Yeah.

George Westbrook: Okay. Because I think yeah, what we could what we could do is use it use all of this as a as a base and then because I think we we probably have to condense some aspects down. Um, and obviously the quizzes they they'll be they'll be fine. Um,

Inplay Global: Yeah.

George Westbrook: and obviously I'm assuming the vid the videos they they they don't they don't exist yet. Is that is that Yeah.

Inplay Global: No,

George Westbrook: Okay.

Inplay Global: that's probably the next step of, you know,

George Westbrook: Um

Inplay Global: are we looking are you guys able to create them with the AI or do should we create them uh based on the summary of what each chapter is? Um, that's probably just a another question just to figure out what's what's what,

George Westbrook: yeah.

  
  

### 00:22:03

  

Inplay Global: you know, what would be easier as

George Westbrook: Yeah. Yeah.

Inplay Global: well.

George Westbrook: We need to like I said it's with AI it's definitely possible. It's just a matter of how long how long does it take and what's the what's the quality going to come out come out like? Um I suppose depending on the style of the video as well. Is it is it more like a a slideshow um with voice over the top or is it like full AI avatars presenting and doing loads of stuff? That's obviously a bit more bit more

Inplay Global: Yeah, because that's one thing.

George Westbrook: difficult.

Inplay Global: Do we want sponsors as well? I mean, videos, you know, brought to you. It's it's a it's an open piece. I mean the education module for the likes of what we said Kaplan and yeah other companies that have corresponding stock education modules

Edwin Johnson: I actually think in this case less is more.

Inplay Global: and marks dig all of them but nothing

Edwin Johnson: George, where is it?

  
  

### 00:23:02

  

Inplay Global: back yet.

Edwin Johnson: I'm sorry. I didn't hear

Inplay Global: Sorry, I I was just telling Troy I reached out to Kaplan not marks um

Edwin Johnson: you.

Inplay Global: STC as well and they they do all of the securities um education content and haven't heard back yet on any of them.

Edwin Johnson: Yeah. Yeah.

Inplay Global: You should to the CFA Institute as well.

Edwin Johnson: Yeah.

Inplay Global: The CFA Institute does a level one curriculum at the college level that this could potentially play into.

Edwin Johnson: Okay. So, George, what I was saying in terms of the slide or how this is going to be presented on the video, in my mind's eye, I think less is more here. I do think like, you know, like almost like a PowerPoint slideshow, you know, where the words are on the background, you know, there there isn't much more to it. No distraction like this. there's an offer and you know we might be able to to Kevin or K's point I forget who said it just now um you know have each particular slide group sponsored by somebody.

  
  

### 00:24:04

  

Edwin Johnson: Anybody else have feedback on that? That's just my mind's

Inplay Global: No, I agree. I think you want it to be very concise and direct and not

Edwin Johnson: eye.

Inplay Global: over like overdone. So either like similar to like the whiteboard videos where it's being whiteboarded out with the concepts as if you were watching a Yeah. live class or just powerpoints or a combination of the two. Yeah. Because I was thinking as well like all of these videos could then live on the YouTube channel as well, right? 100%. So that should be where they're warehouse and then leveraged for all purposes. Yeah.

George Westbrook: Yeah.

Inplay Global: The other piece with the video there um is we are thinking about as far as you know building that programmatic stack is having a a skippable skippable video not being forced to watch a 30 second video before these modules but um having something that we can trigger a video CPM against as

Edwin Johnson: Where do you see the updated app? There's some cool stuff on there, Cody,

  
  

### 00:25:12

  

Inplay Global: Thank

Edwin Johnson: that they they put in over the weekend, over the last three days.

Inplay Global: Okay. Uh, I'll check it

Edwin Johnson: Well, I think Are you guys going to demo what's been new

Inplay Global: out.

George Westbrook: Um yeah. Yeah.

Edwin Johnson: later?

George Westbrook: At the end I think we'll we'll get Max to whip it up and go through some of the

Edwin Johnson: Sounds cool. Yeah. Yeah,

George Westbrook: changes.

Edwin Johnson: it looks really cool.

Inplay Global: So George, would this be helpful then if I just share these documents with you as

George Westbrook: Yeah. Yeah. So I think what let's have a think.

Inplay Global: well?

George Westbrook: So get the yeah we'll get the documents we'll make a condensed version um which we'll just start building against um then obviously we'll send send that condensed version over over to you guys to have like a little play with that this is right, this is wrong, blah blah blah. Um but just as long as we've got a base that we can start building the UI and the UX off of.

  
  

### 00:26:09

  

George Westbrook: Um I think phase one would be let's just get a text version. Um, phase one meaning in the next couple of weeks, probably closer to a week and a half. Um, then have a look at the videos as well. We need to do some um, how many modules are there? 16.

Inplay Global: 16 modules in the beginner. Um,

George Westbrook: Okay.

Inplay Global: and then I believe Then the expert guide, there's 10 modules in that one. And in the intermediate, there's 10 modules as

George Westbrook: Okay. So, yeah. So, we need to think of how we could create those videos at scale.

Inplay Global: well.

George Westbrook: So, what we probably need to do is a bit of a bit of a test to see how long is it taking to create each video and then iterate and then make sure that it's done. Um, because if that's going to be a two or two or three week job to get that done. Um, obviously I think there's there's other more important stuff that that we can be cracking on with before launch.

  
  

### 00:27:21

  

George Westbrook: Um, and then a fate like once we've once we've got the production app going then focus on the videos. But that's just a matter of us testing because it it it could be a relatively short exercise, maybe like a week or two. Um but it could take could take longer. So we we need to test that and then see if that's what we're thinking. Um cuz what is the process? We need to generate the voice, generate all of the let's call them slides, but they'll be moving and then all of the text on there as well. Um cuz they might come out and they might just be s*** to be honest. Um, and it's obviously it's rather it's better to do nothing than put something out there that's a load of s*** that that's going to give people a bad impression. Um, and I think one of the one of the things we spoke about I think in the component when we did that very first education component thing was that Tik Tok style um scrolling. I think that might be too much for for launch um going in that direction whereas more of like a traditional education aspect where there's some text, there's some videos, there's a quiz um it's going to provide the value um and give them that structure as well where it's like right you start here, you go here and then there's obviously that mechanism where they're going to get those inplay dollars as well.

  
  

### 00:28:42

  

Edwin Johnson: I agree. And maybe we maybe uh Kevin, can you send it over to me? I'd like to review all that, too. And then um maybe we just do one or two slides. So you don't do the first 16 and we all agree that this is the way that we like it or don't like it and we modify from

George Westbrook: Yeah.

Edwin Johnson: there. So we just do a real Is that cool?

George Westbrook: Yeah. Yeah. Yeah. So I think what it be is get let's say all 16 modules on the beginner there in

Inplay Global: Yeah.

George Westbrook: their condensed format but not validated content. um just in terms of like looking at the UI, see what it might look like in one or two with videos and the quiz. Um just so we all of the UI and UX components are built, tested, and iterated and we've got say one page or one module that is done to completion. Once we're happy with that, replicate for all of the other modules so that there's the full set for for launch.

  
  

### 00:29:36

  

George Westbrook: Um,

Edwin Johnson: Cool.

Inplay Global: Okay, I've just sent that to everyone now. So, everyone on the call should have those documents,

George Westbrook: perfect.

Inplay Global: those word documents for each of the files to review.

Edwin Johnson: Cool.

George Westbrook: Let's have a look. Okay, so what do we need to do? We need to get the condensed text version. Yeah, I think got a good understanding of what we need to do. Um, I'm trying to think what else is there on the education because like we're not doing the crazy Tik Tok ideas um to start with. Um, it's just that testing and generating of the videos is the only point of contention potentially. Um, we'll find a way. Um, I can't think of anything else on the education. I thought I don't think we need the full hour to be honest. Brett's Brett's got his hand up. The voice of

Brett StClair: the voice of reason.

George Westbrook: reason.

Brett StClair: The end user clicks on the um navigation bar, goes to education.

  
  

### 00:30:42

  

Brett StClair: Can we just thrash out how we see that looking? Are we going to have kind of cards and then you kind of go down and then cards are in sections and or are we going to swipe left? I know you the Tik Tok for me is always swipe down. Swipe down. Swipe down. But I'm just picturing a card. You click into the card. Card opens up the course. Course plays. Turn your phone to the side. You watch through the course. Great. That's really awesome. You get to the end. Pops up the other way. You complete the survey. Oh, not the survey, the questionnaire. Yeah. Da da da. You pass. Awesome. You earn your referral credits, right?

George Westbrook: That That's one. Is it referral credits or is it actual inplay dollars?

Inplay Global: referral

George Westbrook: Okay.

Brett StClair: So, you earn your referral credits.

Inplay Global: credit.

Brett StClair: Then it says to you, "Do you want to go to your next course?" Great.

  
  

### 00:31:42

  

Brett StClair: You go to the next course. Same thing happens. Turn your phone to the side. You watch it. Flips back. You answer the questions. You go next. You earn. There's a page that says, "Hey, congrats. You've earned it. You're now five of six on the way there. You get to the final one. You start it. You turn it. You get halfway. You stop. You move on. You try to do something else. You go back to the education page. You no longer see the courses that you've already done. Where do they go? We've got the next course, which should be the course that you're halfway through. It takes you to the point of where you were in the course. You continue. You answer the questions. You then say, "Great. Thank you. I'm done." It then says, "Well done. You finished the whole section.

  
  

### 00:32:33

  

Brett StClair: You are now certified. You are a whatever. You're a entrylevel superhero. Awesome. Awesome. Actions we could drive off that a little store in your education folder of badges that you've earned. Or um goes to a social media clip. So you can go great. Can I post this on my social media? I'm now a a investor pro at inplay blah blah blah. kind of post your certificate or does it initiate I don't know or we just keep a store what's everyone's thinking about that as you complete each um

Inplay Global: I like a lot of what you just said. The only thing that I would change, I guess,

Brett StClair: course.

Inplay Global: from my perspective is don't get rid of the courses they complete. Maybe just gray them out or something and and you highlight the one you're currently on and forward. um just because you complete quizzes and stuff all the time, but if I want to go back and remind myself what is a security and that was module two and I'm on eight, you know,

  
  

### 00:33:43

  

Brett StClair: Remember we fold it up.

Inplay Global: you never want to close out the education piece just like Yeah.

Brett StClair: You complete it.

Inplay Global: So,

Brett StClair: It folds up kind of thing.

Inplay Global: yeah, you can't uh Yeah, collapsible maybe. Yeah. Yeah. Um, obviously you can't get more referral dollars for going back and completing the same video or something,

Brett StClair: Yeah.

Inplay Global: but um, you could go back and still retain or see the information

George Westbrook: Do we want to allow a user who hasn't completed module one to be able to look at module 10,

Inplay Global: again.

George Westbrook: for example, or does it have to be in order to do 10, you have to do all of the ones before?

Brett StClair: Thank

Edwin Johnson: No, I think you want anyone to be able to go wherever they want.

Brett StClair: you.

Edwin Johnson: No, no, no

George Westbrook: Okay. Do

Edwin Johnson: limit.

Inplay Global: if they do them all referral cash they'll get right but yeah so if they think it's easy

George Westbrook: you

Brett StClair: Never mind.

  
  

### 00:34:30

  

Inplay Global: and they can get swing through it or just jump right to the test then they'll probably do it and we like chunks

George Westbrook: do we want

Inplay Global: in it's like they can do it as multiple times maybe maybe yeah I don't think we want to govern that but yeah but then once they earn it they earn it back So, no. Yeah, I see what you say. No,

Brett StClair: You got me.

Inplay Global: once once you've captured it, that's why I like the idea of graying it out. Yeah, that way you can always go back and reference it, but it's no longer part of the sequence, right? Cool.

George Westbrook: Do do we want to have like a glossery of terms like a quick like definitions

Edwin Johnson: Good coffee

George Westbrook: thing?

Inplay Global: Yeah, it hurts.

Edwin Johnson: 100%.

Inplay Global: Yeah.

George Westbrook: Okay.

Inplay Global: And one of the things I also have prep doing some work on is as part of the education stuff is refining the FAQ that we need to put back on our website like that standard like just basic questions about what is a reggae security how is in play regulated like those type of questions that's also going to be outside of the education component we want to have like a broad base of FAQs on our website that just answers key questions about who and what is inflate Yeah,

  
  

### 00:35:44

  

Edwin Johnson: Yeah,

Inplay Global: on each of those modules I

Edwin Johnson: that one. Sorry to interrupt you, Kevin. On that one,

Inplay Global: did.

Edwin Johnson: I want to be a little bit careful because the sauce we we want to be careful how we uh, you know, serve the sauce.

Inplay Global: Oh, it's going to go reg.

Edwin Johnson: Get into the

Inplay Global: Yeah,

Edwin Johnson: meat.

Inplay Global: absolutely. We will have legal review it before it gets

Edwin Johnson: Who the f*****

Inplay Global: published.

Edwin Johnson: illegal? I haven't talked to a lawyer in a long

Brett StClair: That should

Edwin Johnson: time.

Inplay Global: Uh I mean at this point it's Brian and I, I guess.

Brett StClair: be

Inplay Global: Yeah. Um,

Edwin Johnson: Okay.

Inplay Global: yeah, because I also spent some time on the weekend going through the disclaimers we need to be putting back on the website as well that I was going to send to Marlin to review.

Edwin Johnson: You did talk to Matt though on Friday, right?

Inplay Global: Yes. Very quickly.

  
  

### 00:36:29

  

Inplay Global: And I got my action items and now I he'll he said once it's back in queue to let him know and he'll chase it down. It's for the app

Edwin Johnson: Okay.

Brett StClair: the

Inplay Global: and from sorry Brian we'll take this into our huddle later.

Edwin Johnson: Okay.

Brett StClair: Yeah.

Inplay Global: Yeah just quickly as well at the end of each of those uh education pieces there is a glossery for on the if you slide right to the

George Westbrook: Oh,

Brett StClair: Yes.

Inplay Global: end.

Edwin Johnson: Cool.

George Westbrook: okay.

Brett StClair: Then as you clock up your certifications, I think we need a section on your profile page that sayserts and we have

Inplay Global: Oh,

Brett StClair: little custom badges for each of these as you collect them. And maybe they're all gray and then as you collect each one so it doesn't look like you've got the smattering. You've actually got an order that you're trying to hit and you can see which ones you've done or not done. And if you click on one of those that are gray,

  
  

### 00:37:24

  

Inplay Global: heat.

Brett StClair: it takes you to the exact course and then you can pick up from there and do that course. Right? So you've got multiple points of entry to the courses as well.

Inplay Global: I like that. Yeah, I like that a lot. People love badges for whatever reason.

Brett StClair: Yeah.

Inplay Global: Everyone likes smart they are.

Brett StClair: Uh

Inplay Global: Yeah, I think there's an instant gratification to it once you actually achieve it, too.

Edwin Johnson: Awesome.

Brett StClair: Happy. I think that's everything.

Inplay Global: Go. So, uh, before we jump Oh, I have one. Sorry. I have one more thing. Sorry, Cody. No, no, you go ahead.

George Westbrook: Yeah.

Inplay Global: Mine's not on education. So, not on education on the website. So, the new website when you put the URL in like a LinkedIn post or a social media post, it's coming up with a picture. Have you heard you you know what I'm talking about? A picture icon that looks nothing like inplay.

  
  

### 00:38:26

  

Inplay Global: It looks like some mapping chart.

George Westbrook: s***.

Inplay Global: Is there a way to get it so that the inplay logo or some inplay icon shows up when that

Brett StClair: Yeah. What's that? It's called social.

Inplay Global: Yeah.

George Westbrook: I think OG

Brett StClair: What is it called? OG image, right? Yeah. And I think there's a lot more we can add to that.

George Westbrook: image.

Brett StClair: We can actually package up. So when you put it in there, it pulls up like a social card these days where it's a little description plus the what's it

Inplay Global: Yeah.

Brett StClair: plus the right image that you want and your logo kind of thing.

Inplay Global: Yeah.

Brett StClair: Um she Yeah, we didn't think of that. Um but it's not a difficult thing to

George Westbrook: I don't know where that

Brett StClair: do.

Inplay Global: Because we tried to do a LinkedIn post last week and it when we put in the website the new website in I think

George Westbrook: came.

Inplay Global: this is the first time we've done this.

  
  

### 00:39:12

  

Inplay Global: The icon came up like as the image looked really weird.

Brett StClair: Yeah.

Inplay Global: So we didn't wrap it. We didn't post the web the link.

Brett StClair: Okay.

Inplay Global: So,

Brett StClair: Oh, yeah. Look at that.

Inplay Global: sorry.

Brett StClair: Yeah.

Inplay Global: I just want to make sure I brought that up before the end of the call this week for the

Edwin Johnson: Good night, Troy.

Inplay Global: day.

Edwin Johnson: Good

Brett StClair: Yeah. That's good catch.

Edwin Johnson: night.

Inplay Global: Um, my piece is on the the research module. Um, we use every tool in our tool belt to generate revenue here. Um Edwin and I have talked about or the whole team has talked about um potentially charging for premium data points and that research section that I've wireframed. I know George you had very real feedback and concerns on that on what that does as far as timelines and moving stuff around. So, I don't know if you want to if we want to schedule a different uh component call or module call to talk through that or if 15 minutes is enough.

  
  

### 00:40:15

  

Brett StClair: Yeah. Let's do we do we have enough time to do it now? We probably do.

Inplay Global: Now,

Brett StClair: Hey, because I'm just thinking about Yeah.

Edwin Johnson: I I'd prefer we schedule another time.

Brett StClair: Get it done properly because it's quite a So, we're just thinking about there's billing mechanisms, how we do the billing mechanisms, there's the usage, there's the overlay, it's the experience, it's the co-pilot view to it. And how do we

George Westbrook: Just the overall functionality as well is uh

Edwin Johnson: What do you guys think of this this uh plan?

George Westbrook: Yeah.

Edwin Johnson: You think it's a good

Brett StClair: I think it's very cool. It's nice.

Edwin Johnson: plan?

Brett StClair: I think it's really like I think it's a really powerful feature, right? Imagine getting anything you want on any of that data. f***. The problem we're going to have is getting the right guardrails in place. You you don't want to be caught in this. So, two things. You don't want people to then burn LLM tokens.

  
  

### 00:41:15

  

Brett StClair: So, that's going to be one of the things. How do we constrain it a bit? People going, "Ah, now I want to do" and it goes away and you get

George Westbrook: H.

Brett StClair: slaughtered on LLM tokens. We're going to need to put some guardrails there to stop that. And then we are going to need to make sure that from a compliance point of view, the kind of um feedback that you're getting isn't stepping the line in your advisory kind of space if it's going, you know, because people will push the boundary, right, with L&M it'll start with, I want to know who's injured. I want to know why they're injured. I want to know the chances of them winning. I want to know how I should be bidding. You know, it'll the conversation will go there anyway. And so it's we got to think about the traps that we got to put in play to catch, buy back, and then push them to their own decision- making. So that's I think also why George, let's rather spend a bit more time, right, trying to work through some of the use cases that people are going to work through because it's super powerful, right?

  
  

### 00:42:18

  

Brett StClair: But you don't

Edwin Johnson: Well, I will tell you in personal experience,

Brett StClair: want

Edwin Johnson: I built a overunder model for NBA basketball in chat and

Brett StClair: Yeah.

Edwin Johnson: um it was really effective and then it it like it started telling me that I was um violating the policy as it couldn't give me the results anymore and I'm

Brett StClair: Nice

Edwin Johnson: like but you had given it to me the last you know it was like we shouldn't have given you the information. It was the most bizarre conversation I had with an LLM in my life but it was very

Brett StClair: content rights.

Edwin Johnson: effective.

Brett StClair: You've stumbled into a content rights blocker and it's gone. We haven't paid for this content. Oops. Get the f*** out of here.

George Westbrook: Okay.

Edwin Johnson: Yeah, it was it was Yeah.

Brett StClair: But you paid for it, right?

Edwin Johnson: I mean it was interesting because like in that particular model I built I'm like you know what are the key things for overunders on

Brett StClair: So

  
  

### 00:43:10

  

Edwin Johnson: you know NBA and obviously they looked at the referees and then they looked at the likelihood teams were going to start shooting the ball within the first five seconds of go crossing half court and the more shots they took the more likelihood there would either they'd make it or miss and the other team would fast break and get you know go for points on the other side and it was I I mean it was about 80% accurate when I used Obviously that's I had a very short um um uh you know subset to look at but pretty

Brett StClair: As a product owner, the part I like most about this capability,

Edwin Johnson: interesting

Brett StClair: this is a direct tap into your trader vein on stuff they want. This is your feature list. This is your cuz you're going to see stuff coming up and up and again and you go you do a Sam

Inplay Global: Yeah.

Brett StClair: Alman that's a good idea build into your feature string. That's what's so powerful about

Edwin Johnson: Yeah, I'm I'm wondering out loud here if we need to have the

  
  

### 00:44:10

  

Inplay Global: Heat.

Brett StClair: it.

Edwin Johnson: um AI function built into the app. I don't know that we do to start with. Um, you know, c certainly I think that um the premium data, Cody,

Brett StClair: Oh,

Edwin Johnson: correct me if I'm wrong, what we're getting from Sport Radar that we're pushing out is data that would normally cost some kind of money to a user, right? Like,

Inplay Global: Correct.

Edwin Johnson: and that number would be what

Inplay Global: I mean,

Edwin Johnson: roughly?

Brett StClair: heat.

Inplay Global: if you're looking at real-time data, anywhere between 10 and $20,000 a month across a couple

Edwin Johnson: Okay, perfect. So what what I would say is like maybe for ease maybe we just say you know they query

Inplay Global: weeks

Edwin Johnson: the stuff on our our our app and they take whatever result in into whatever LLM they're using and let them figure it out on their own. We'll give them the data. We don't need to give them the the Q function in ours. You know it might be easier for us to stomach at least on day one.

  
  

### 00:45:15

  

Edwin Johnson: Um because you know I'd always been against charging for the um

Brett StClair: Sorry.

Edwin Johnson: access to the data because I want to give the first taste free for the whole season and then once we go to production people get comfortable with it. But being that we're kind of in this soup with the advertisement model um we're behind. So, I mean, you know, it could become a very big revenue provider for us to help us offset some of these, you know, payout

Inplay Global: Absolutely. Yeah, I agree with you on the AI chatbot could be a phase two um sort of feature

Edwin Johnson: costs.

Inplay Global: ad and then also that's when we take it from 14.99 to 19.99 if you want your AI companion. Some people say for

Edwin Johnson: Well, I mean, look, I'm I'm paying a hundred bucks or 200 bucks a month for chat. I pay whatever hundred bucks a year. I don't know what I pay for Claude, but I'm paying all these things anyway. I mean, if you've got a a true sport one, Cody,

  
  

### 00:46:11

  

Inplay Global: Yeah,

Edwin Johnson: you might be able to go from $14.99 to $49.99 or

Inplay Global: absolutely. 100%. So,

Edwin Johnson: more.

Inplay Global: I think it's a it's a great feature add-on for phase two um post launch that we can we can trigger a substantial price increase. Um I know I've sent it over a few times.

George Westbrook: Huh?

Inplay Global: Phase one can really just be that that research portal that I've sent over in wireframe that has our pre-anned reports that we build out. You know, your top five offenses versus top five defenses. What does that equate to in stats per game? And then so you have those pre-anned reports and then the ability and this is where people really get addicted to this stuff is creating your own reports. So maybe we limit to five stat categories or something that we can get this out for for a launch. So it doesn't have to be over complicated. We can always iterate on it later. But they can they can build out their own reports with say five stat categories and you can save said report.

  
  

### 00:47:14

  

Inplay Global: So, it's, you know, top scoring offenses in the first half when they're on the road.

Edwin Johnson: day game versus night game.

Inplay Global: What? Yeah. And you save that report that's in your portal.

Edwin Johnson: Yeah.

Inplay Global: That's what you're paying for. And then the real- time data is flowing into this every week and updating it. And that's building your trading model. That's that's what you like to trade off of. Or maybe you're like, I really like to short teams in the first half. that suck and then I buy them at halftime because they come back and they, you know, make it interesting or something like that. And that's a model and you save these reports and that's what people will pay for. Sorry, I get excited about this. I know I'm yelling. Jasmine like a tier based that if they if they pay like say 99 cents or what they only get like three reports. I love it. They got Absolutely. You know, you get 10 reports in it.

  
  

### 00:48:08

  

Inplay Global: It's $29.99. I mean, we said we were gonna make this a a different modular recording, but now we're getting lot of No, it's a great idea.

George Westbrook: We've got seeds for the next one.

Brett StClair: Yeah.

Inplay Global: Yeah. Yeah. Yeah. Exactly. Lots of seeds. I mean, this is a product I've had in my head for like the last seven years. It's just Sport Radar never took BTOC approach. They always wanted to say B2B. So, yeah, I've got lots of ideas.

Brett StClair: Um, when you said you before it goes into the app, how were you envisioning it? Was it like an MCP server? Is am I misunderstanding that?

Edwin Johnson: Who are you

Inplay Global: before. Yeah,

Brett StClair: You guys mentioned that maybe first phase isn't in the app or do you mean it was in the app?

Edwin Johnson: asking?

Brett StClair: I'm not I'm

Inplay Global: the AI portion is not in the app,

Brett StClair: not

Inplay Global: but the research portal lives in the

  
  

### 00:48:58

  

Brett StClair: Oh,

Inplay Global: app.

Brett StClair: I see the research with the Okay. Okay. Sorry. Sorry. Yeah.

Inplay Global: But but the the AI companion uh sort of feature lives outside of the app for

Brett StClair: Yeah.

Inplay Global: phase one. Let them use what they're already paying for. We just give them the data sets and then phase two we build in the

Brett StClair: So there is a technology called MCP servers.

Inplay Global: companion

Brett StClair: You could open an MCP server on your side and they log in with their credentials and then they crunch using their LLMs and consume their set of data. Might be a short-term hack. I don't know.

George Westbrook: Need to see need to see if Sports Radar have a policy against that because

Inplay Global: Well, my other concern is then you li you limit yourself getting the higher premium when you add it in phase two. You're you're going to be fighting against the MCP service that you've created.

Brett StClair: Yeah.

George Westbrook: And I think it's too much to give away for free because it's it's very very very

  
  

### 00:49:59

  

Brett StClair: Yeah.

George Westbrook: difficult to charge for an MCP server at the moment. I mean, you can validate and invalidate the API key if they've paid or not. Um but it's yeah it's quite

Brett StClair: Yeah. No, no, no. That's pushing it too far. Yeah. Yeah. Yeah.

Edwin Johnson: I like how you think though, Brett.

George Westbrook: Yeah.

Edwin Johnson: Before we do both on the call,

Brett StClair: Oh,

Edwin Johnson: do we have a little time for Max Kingsby to show us uh the updates on the

Brett StClair: max kingsby.com.

Edwin Johnson: app?

Brett StClair: Kingabe. I always say Kingsby as well. King of Sorry, man.

Edwin Johnson: I mean,

Brett StClair: Max.

Edwin Johnson: I misspelled his name on Only Fans for a couple years.

Brett StClair: Uh, it's a problem.

Max Kingaby: Don't worry,

George Westbrook: All right.

Edwin Johnson: I I thought I thought he was Max Queen's

Max Kingaby: I've only been working.

Inplay Global: Okay.

Max Kingaby: Um,

Edwin Johnson: name.

Max Kingaby: yeah, I'll give everyone a quick walk through.

  
  

### 00:50:52

  

Max Kingaby: I mean, the app will look very similar to what everyone's already seen, but I'll kind of show the specific changes that I've made in the past couple of days. Can everyone see that?

Brett StClair: Yep.

Max Kingaby: Cool.

Inplay Global: Yeah.

Brett StClair: That ball's looking better.

Max Kingaby: Yeah.

Edwin Johnson: Yeah.

Max Kingaby: So, starting first of all, navbar.

Brett StClair: All

Max Kingaby: Um, I've made the icons bolder and actually made it a floating navbar instead

Brett StClair: right.

Inplay Global: So,

Max Kingaby: of a concrete navbar that's attached to the bottom of the screen. Um, a small change which you guys might not have noticed is the actual helmets themselves.

Edwin Johnson: I noticed.

Max Kingaby: Well, hey. Um, all of the helmets have now been updated to include the new style, which doesn't have any of the ugly white backgrounding around them. Um, a big one with the ads,

Inplay Global: What?

Max Kingaby: each ad now has a popup page. So, you click in to Cash App and it comes up with a Cash App popup page,

Inplay Global: That's

  
  

### 00:51:59

  

Max Kingaby: which you can then Yeah. which you can then one day get started and go to their website

Inplay Global: nice.

Max Kingaby: or watch a video and earn a um cash reward. Once the video is up, you then have the opportunity to leave this page and win the reward, but you have to watch the whole length of however long the advertisement video is going to be.

Edwin Johnson: That's brilliant, by the way.

Max Kingaby: Uh,

Edwin Johnson: I think that's

Max Kingaby: thank you.

Edwin Johnson: amazing.

Max Kingaby: Um, another thing is all advertising banners at the top of the page now stay there no matter where you scroll on the screen. So,

Inplay Global: That's awesome.

Max Kingaby: it'll always be there.

Edwin Johnson: And you can click through that one as

Inplay Global: Yep.

Max Kingaby: Yeah. Click through. Here you go.

Edwin Johnson: well.

Max Kingaby: Door Dash. Um,

Inplay Global: Brilliant.

Max Kingaby: once again, you can watch in video or inquirer.

Inplay Global: No one has said this is not a

Max Kingaby: Then with the live game cast, I've slightly updated the Pepsi banner.

  
  

### 00:52:57

  

Inplay Global: Yeah.

Brett StClair: Hey,

Max Kingaby: So,

Brett StClair: are you

Max Kingaby: it will now there'll be an animation and it'll bring you into the

Edwin Johnson: Love.

Max Kingaby: game.

Edwin Johnson: Beautiful.

Max Kingaby: Um,

Inplay Global: Yes.

Max Kingaby: most of the changes I'm making now are just kind of UX changes. Ah, small one up here. This card used to be actually it wasn't a card previously. It was just a floating search bar um and an option to select all NFL or NCAA. I've made that now a card so it fits in a bit better with the rest of the app. Um trade

Brett StClair: cards are rendering really really well.

Max Kingaby: page

Brett StClair: Really sits nicely. It's like proper material design kind of feel to it.

Max Kingaby: all the buy and sell buttons are now in a slightly more highlighted bold color to encourage the user to click on them.

Edwin Johnson: That's right.

Max Kingaby: Wow.

Edwin Johnson: Love that change, by the

Max Kingaby: Thank you.

Edwin Johnson: way.

Max Kingaby: Uh we've added design as a sponsor and then we've also added a Pringles option down below.

  
  

### 00:54:13

  

Max Kingaby: Um yeah, and then I'm going through and editing this final more page in a bit more detail now as we speak. Um I really like the idea of as profile pictures being able to select a helmet. Do people like that or is that a big night?

George Westbrook: It might be a bit confusing because if you if the mute yourself,

Edwin Johnson: I

Inplay Global: I mean, one thing they do in fantasy is they let you pick your own logo icon that you want

George Westbrook: Max

Edwin Johnson: mean,

Inplay Global: to have in color scheme. Yeah. Yeah. And color

Edwin Johnson: can you bring in a photo?

Max Kingaby: Yeah,

Inplay Global: scheme.

Max Kingaby: that's what I was thinking.

Edwin Johnson: Can you bring in a photo?

Inplay Global: Yeah.

Max Kingaby: We we can give the option for that.

Inplay Global: They usually

George Westbrook: Yeah.

Inplay Global: propose.

Max Kingaby: Yeah.

Edwin Johnson: I mean, I think the photos are cool because, you know, people like to be out

Inplay Global: Yeah.

Max Kingaby: I.e. like a photo of themsself or that dog or

  
  

### 00:55:13

  

Edwin Johnson: there

Inplay Global: Not not necessarily a photo of himself. Like I don't know for Yahoo Fantasy.

Max Kingaby: something.

Inplay Global: I have like this this crazy uh Kirby enthusiasm. Yeah. Picture. So you can just like upload a picture from the internet. Yeah.

Max Kingaby: Yeah. Um yeah,

Inplay Global: As a honey badger.

Max Kingaby: I can do no problem. Um we'll have to just put a little page up here to kind of say edit photo. Um you can probably also give yourself a little bio. this up to you guys. Um, make it feel a bit more personalized, I suppose.

Inplay Global: out

Max Kingaby: Trading expert and enthusiast of the balls.

Inplay Global: here.

Max Kingaby: Don't know like that. Um, and I think that pretty much sums up all of the changes I've made. We still need to update the supporting information. So, the FAQs, contact us, terms and condition pages, but ah,

Edwin Johnson: right?

Max Kingaby: the 3D stadium Don't show that.

Edwin Johnson: Oh,

  
  

### 00:56:15

  

Max Kingaby: Oh, don't don't show the 3D stadium.

Edwin Johnson: f***.

Max Kingaby: Apparently, that's not that

Edwin Johnson: You f******

Max Kingaby: thing.

Edwin Johnson: tease. That looked awesome, by the way.

Max Kingaby: Sorry.

George Westbrook: That's that that was something that I mute you again, Max. the that that was something I think we put four or five days into it, but it wasn't it was going to take longer than that. Um it's that picture there was just a placeholder picture. Um it's definitely something in time that we can add in. That's a placeholder, so don't base anything off that, but it's like the animations across. It's a bit more 3D. Um, and then the potential when there's sponsors to add the sponsorship onto the actual stadium as well,

Edwin Johnson: s***.

George Westbrook: cuz I think like we were saying ages ago, it's the eyeballs are going to be on on that game page when it's a game day. Um, and then utilizing as much space as that in a natural way for

Edwin Johnson: Yeah. looks awesome.

  
  

### 00:57:17

  

Edwin Johnson: You know,

George Westbrook: advertising.

Edwin Johnson: I don't want to state the obvious again, but what this team has put together in seven f****** weeks is amazing.

George Westbrook: has been seven weeks. I don't

Edwin Johnson: I know it feels like seven years, but I mean, it's only been seven weeks,

George Westbrook: know.

Edwin Johnson: plus the websites and plus all the other things. In terms of output, I mean, it's it's staggering. It's hard to believe you're you're able to do that stuff, guys. So, you know, very impressed. You should be proud of yourselves. I'm excited to be part of it. Um, yeah, I mean, it just looks incredible. We need a little thing, couple of things of good luck this week, you know, so hopefully tomorrow's a great day for us overall and um, you know, we'll see what happens. But, you know, should be really pleased with with the effort. Keep your head down, keep going. But I mean, it's it's hard not to be in awe of what's been accomplished in seven

  
  

### 00:58:16

  

George Westbrook: Thank you.

Brett StClair: thinking about that delivery date.

Max Kingaby: Thanks. said,

Edwin Johnson: weeks.

Brett StClair: Um, we need to get the pregame up and running this week and out the door. So, that's going to be a focus. I just wanted to check, Troy, did Apple get back to you at all yet?

Inplay Global: Yeah. So, Apple finally got back to us, sent said they had sent a web form to our legal contact. I called our legal contact on Friday. He said he has not gotten anything. He looked at his spam. He looked at his multiple emails that he has, you know, both his law firm and the inplay. So then I went back to them and said, "We haven't gotten it, but here's who did it, who was it sent to, here's who it should have been sent to, and we created, you know, legal atplay global.com so that multiple people can see when it comes

Brett StClair: Nice.

Inplay Global: through." Yeah.

Brett StClair: Okay. Awesome. Awesome. Awesome.

  
  

### 00:59:10

  

Brett StClair: Awesome. Because that's going to be

Inplay Global: Oh, I'm It's my today is like I'm going to be on it if they don't respond with couple hours.

Brett StClair: the

Inplay Global: I'm gonna be on it until we get this form and then I'm going to be on our lawyer to get it done.

George Westbrook: Yeah.

Inplay Global: so that we can move along because this is the next stage to our approval to be able to drop it at the

Brett StClair: what we want to do is create a separate branch on the pre-launch.

Inplay Global: store.

George Westbrook: Come on.

Brett StClair: So, it only has pre-launch features and functions on it. and we'll work to refine and perfect that. And then in parallel is to then carry on building the production um with all the capabilities and pre-launch will have to have uh wallet creation. It'll have to have um IPO listings, IPO buy. So when we switch that on, let's not rely on making sure we've got the full app there. Let's make sure that the pre-launch has that.

  
  

### 01:00:02

  

Brett StClair: Um I'm just a bit worried that Let's see. Let's see what the tZERO guys come up with just on that API. Let's just make sure that that API is available. Then we can launch with it even, you know, by the end of the week. Otherwise, we can always drip feed. So, which has got an idea to kind of just, you know, simulate the end points for now. But as soon as we do turn on, at a minimum, we're going to need to make sure that those those abilities are there.

Inplay Global: Yeah, I think we need to come up with a little bit of a backup plan in the event that we want the pro the referral program to go live for Fourth of July weekend, which I think we absolutely should try to drive for that if through the web and not through the app at a

Brett StClair: Yeah.

Inplay Global: minimum so that we can drop that by Monday or at the latest of next week so that people go into the Fourth of July weekend here in the class trying to drive up referrals to get on the weight lists.

  
  

### 01:01:01

  

Brett StClair: Yeah. Yeah. I agree.

Inplay Global: So, yeah, big

Brett StClair: Big we can

Edwin Johnson: quick question for you.

Inplay Global: week.

Edwin Johnson: Um, Max King,

Brett StClair: build.

Edwin Johnson: Kingsby, um, on the when and I guess George and Hassan, I guess Brett, too. f*** it. Uh, the whole crew. Um, I don't want anyone to feel left out. when you hit the inplay um icon on the phone and it brings you into the app and it says

Inplay Global: Awesome.

Edwin Johnson: welcome back George. Um how difficult will it be to have a you know a just

Brett StClair: His

Edwin Johnson: before that happens basically like picture you know inplay trading challenge brought to you by whomever and that dissolves within two seconds or whatever you know whatever is acceptable.

George Westbrook: on the backlog.

Max Kingaby: on the backlog.

George Westbrook: So,

Max Kingaby: So,

Edwin Johnson: Okay,

George Westbrook: yeah,

Max Kingaby: yeah.

George Westbrook: we'll we'll get that added in.

Brett StClair: name is

Edwin Johnson: cool.

George Westbrook: Uh yeah. Yeah, Max.

  
  

### 01:02:03

  

George Westbrook: Um yeah, so splash page then we're iterating well not iterating working through the feedback on the app as well.

Edwin Johnson: Cool.

George Westbrook: Um I think like we were saying before it's we get to a point where we think we can start adding the feedback in and then we've got like say the education module that's coming in and we want to get the net new stuff done before we go into like right we've got everything here let's iterate iterate

Edwin Johnson: Yep. What I mean, look, you know,

George Westbrook: iterate

Edwin Johnson: you you guys are doing fantastic, so I know you'll figure it out in terms of,

Brett StClair: This

Edwin Johnson: you know, timing and whatnot. It's just something that I don't think we need it today, obviously. Um, but as we get further maybe with some of these advertising discussions, you know, one thing we might be able to talk to advertisers about, Brad, is that we're we're you know, going to include something for uh if you sign quickly, we'll uh we could put you on that front page and maybe we you know,

  
  

### 01:02:51

  

George Westbrook: Yeah.

Edwin Johnson: it's a rotating logos or something like that so it's not just a single person or a single company every

George Westbrook: Yeah.

Edwin Johnson: time. Maybe there's a way that we could bas, you know, spin it up so everyone gets equal uh equal exposure on the entry.

Brett StClair: This

Edwin Johnson: Cool. Awesome. Well, thank you. Is there anything else for me today?

Brett StClair: is

George Westbrook: I think I think that's

Inplay Global: Yep.

Edwin Johnson: Okay.

George Westbrook: everything.

Edwin Johnson: I wish everyone a great day.

Inplay Global: Yeah.

Edwin Johnson: Um great week. Fingers crossed. We need some We need some good luck. Okay.

George Westbrook: I think we need somebody else to say let's f****** go at the end of this one.

Inplay Global: No, it's doesn't work.

George Westbrook: Who? I I can't be the only one. I'll do

Edwin Johnson: I'm gonna have to I'm gonna have to request the mystical beast known as Gary Anderson. He's in that fog.

George Westbrook: it.

Edwin Johnson: They know he's got some kind of potion being created over

  
  

### 01:03:44

  

Gary Anderson: That's right.

Edwin Johnson: there.

Gary Anderson: That's how it is here in Florida.

Inplay Global: smoke.

Gary Anderson: We're in the uh in the Everglades. We're in the swamp. So, but let's f******

Edwin Johnson: Wow.

Gary Anderson: go. Let's do it. Let's f******

Edwin Johnson: There we go.

Gary Anderson: go.

Brett StClair: Please hear that again.

George Westbrook: Yes.

Max Kingaby: Let's

Edwin Johnson: There we go.

Inplay Global: Yeah.

Edwin Johnson: The mystic is spoken.

Gary Anderson: George is like it.

Edwin Johnson: There you go.

Max Kingaby: go.

Edwin Johnson: And Gary,

Gary Anderson: All right,

Inplay Global: All

Edwin Johnson: we're going to get you an inplay robe for these calls,

Gary Anderson: guys.

Edwin Johnson: too, because I think something with cloak cloak.

Gary Anderson: Rogue, that would be all right.

Edwin Johnson: That's right. All right. Well, thank you all for your time today. If anyone needs anything, please reach out.

Inplay Global: right.

George Westbrook: Perfect.

Edwin Johnson: Thank you all.

Inplay Global: All right.

Edwin Johnson: See you guys.

George Westbrook: I said you say have a good one.

Hasan Mohammed Ahmed: side.

Inplay Global: I freaking out.

Hasan Mohammed Ahmed: Cheers.

Edwin Johnson: Bye.

  
  

### Transcription ended after 01:04:26

  

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.

**