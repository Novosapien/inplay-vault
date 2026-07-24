---
date: 2026-07-24
type: standup
scope:
  - "[[market-maker/market-maker]]"
  - "[[trading/trading]]"
  - "[[information-layer/sub-components/single-game-page/single-game-page]]"
  - "[[information-layer/sub-components/team-page/team-page]]"
  - "[[components/components]]"
status: extracted
extracted-to:
  - "[[market-maker/decisions]]"
  - "[[market-maker/open-questions]]"
  - "[[market-maker/plan]]"
  - "[[market-maker/systems/mm-ops-ui]]"
  - "[[trading/trading]]"
  - "[[information-layer/sub-components/single-game-page/single-game-page]]"
  - "[[information-layer/sub-components/team-page/team-page]]"
  - "[[components/components]]"
  - "[[architecture/open-questions]]"
---

## Post-Call Analysis

Friday touchdown, ~51 min. Edwin + Cody + Troy + Kevin (InPlay) with the Novo team. Same day as the v1.3 MM spec intake — Edwin's "doc last night" is that spec (George reviewing, questions owed by Monday). Big threads: gamecast/probability feed speed, SR entitlements, trading-launch focus (~Aug 22), MM dashboard, and a new analyst-prices/subscriptions surface.

| Finding | Destination | Action |
|---------|-------------|--------|
| Probabilities API rides SR's **betting-side feed** (faster than the licensed media feeds powering the gamecast; raw betting feeds are sportsbook-only, unavailable). MM consumes probability directly → in-app parity between users and MM. Edwin: use the fastest feed, must never lag. Cody lobbying SR for betting feeds | [[market-maker/decisions]] + [[market-maker/open-questions]] S4 + [[information-layer/sub-components/single-game-page/single-game-page]] | Decision logged; S4 downgraded to mitigated; feed-source block added to §9 |
| SR entitlement route: George emails blocked products/versions (probabilities in production, v2 live-bulk 403, quotas) to **support + Scott + Cody**; Cody drives with Scott + David. Master-key model — call limits + versioning claimed moot | [[market-maker/open-questions]] S7/S2/S1 | S7 channel recorded; S2 folded into the email |
| MM monitoring dashboard (Edwin): phased — read-only positions/holdings first, variables static; MM = just another user → reuse user inventory APIs | [[market-maker/systems/mm-ops-ui]] + [[market-maker/decisions]] | Phasing section added |
| Remaining-season probabilities: Edwin re-affirmed internal weekly model ("I'll come up with a piece you can pull"); George offered SR-derived calc; weekly manual input floated | [[market-maker/open-questions]] E19 | 24-07 call evidence appended (E19 stays open) |
| NCAA IPO prices: Cody delivered totals; Edwin pushing prices into the app today | [[market-maker/open-questions]] E3 | Status → in motion |
| Trading: infra map complete 23-07, small items left (cancel, cancel-replace); launch non-negotiable, **live for ~Aug 22**; replay-based simulation testing (Chiefs–Ravens), multiple runs/day | [[trading/trading]] + [[market-maker/plan]] | Update block + timeline anchor added |
| Launch remainder: notifications, tax forms, payouts. Payment provider unsigned — worst case delayed payouts with visible owed amounts; interim Zelle/wire acceptable | [[components/components]] Withdrawal Flow row | Row updated |
| Release governance (Brett): scope freeze near launch; app-store push vs capped OTA → staged, scheduled releases | [[architecture/open-questions]] | Standing-policy row added |
| KYC-less app variant for academic competition — needed ~first week of Sept, below trading in priority; Apple-review lift being scoped | [[architecture/open-questions]] | New row |
| First SSP: app store ID landed → AdMob verification underway (24–48h); Android + other SSPs queue behind store IDs | [[components/components]] Advertising | Status bullet added |
| Google Tag Manager (Hasan) — one container, all tags; share setup with Cody. MMP question: Kochava (Plexus agency) vs AppsFlyer — Brett reviewing | [[components/components]] Analytics | Bullets added |
| **Analyst-prices swipeable on team pages** + subscription packages (Cody sending; ~$39.99 mid-tier, ~$2M/mo math; research inserted "next week or two"); Preferred Walk-Ons onboard (~200k reach); Edwin sample Monday | [[information-layer/sub-components/team-page/team-page]] | **Flagged for focused session** — placeholder section added, not specced |
| Cody roadmap/bandwidth-visibility ask → Brett + George to build a vault release/cadence dashboard | — | Action item — Brett + George |
| Status only: 37 first-time downloads Wed 22-07 (83 approved KYCs, up from 64 — some downloads pre-KYC'd); newsletter out today; Omnicom two-pager owed to John (Brett); T0 calls Tue/Thu (already recorded 20-07); Edwin's doc = the v1.3 MM spec (already extracted same day) | — | No action |

---

**

## Inplay - App - Touchdown - Transcript

### 00:00:00

  

Brett StClair: I can't I'll call you.

Max Kingaby: TW.

Brett StClair: Hello everybody. Sorry we're late.

Max Kingaby: Sorry guys.

Brett StClair: It was Max behaving like a child again.

Edwin Johnson: Thank God.

Max Kingaby: Can't help myself.

Edwin Johnson: It's good to see that young spirit.

Cody Haugen: Well,

Edwin Johnson: Max,

Max Kingaby: I called Brett twat on a client call.

Edwin Johnson: is it just a dynamic duo today?

Max Kingaby: So for them I called Brett a twat on a client call.

Edwin Johnson: I'm sorry.

Max Kingaby: It's an alltime high.

Edwin Johnson: Did you describe the twat in question at all? All right.

Max Kingaby: I think I think I found it funny.

Edwin Johnson: Where'd your boy George? Is he out? Boy George. Get that.

Brett StClair: You just

Max Kingaby: He's just hopped to L after the last call, but he'll be back shortly.

Edwin Johnson: Sweet. Sweet. All right. Great.

Brett StClair: Yeah.

Edwin Johnson: All right. So, uh, thank you for today. Another week. Hey, Brett.

  
  

### 00:00:58

  

Edwin Johnson: Quick question for you. Um, did to a couple of them actually. Did you send that info over to that d****** from Omnicom US,

Brett StClair: Send enough.

Edwin Johnson: John?

Brett StClair: I'm going to send it off.

Edwin Johnson: Okay, please. Um, also, where are we at with the um, uh, ad server? Like, I think we're running out of time to get that thing hooked

Brett StClair: So,

Edwin Johnson: up.

Brett StClair: we've got the ADM Mob verifications are in progress right now.

Edwin Johnson: Cool.

Brett StClair: Um, our problem is we had to wait till we get an app store ID which we got yesterday. So, as soon as we got that, Troy and I worked through the various signins and authentications last

Edwin Johnson: Sweet.

Brett StClair: night. Um, and so that's kicked off. So, we've got 24 hours, 48 hours of ADM Mob and then at least we've got one SSP that's going to be serving. And then once the Android store goes live, we'll grab that and we'll go through the same process.

  
  

### 00:01:52

  

Brett StClair: So, at least we get ADM Mob firing in. Then, we'll carry on with all the other guys because they also all need the app store ids and URLs. So, there's and they're just different timelines.

Edwin Johnson: Okay, cool. Okay,

Brett StClair: But,

Edwin Johnson: so we're

Brett StClair: I just want to make sure as soon as possible we can serve that from an SSP so we can get the data sets coming

Edwin Johnson: cool.

Brett StClair: through.

Edwin Johnson: Yeah. Yeah. Any anything will help. I think my my cause

Brett StClair: Yeah. Yeah. Yeah. Exactly. Um, also just thinking about your MMPs and analytics and all those kind of tags. Her son's got it on his list of things to do to add something called a tag manager. So, a tag manager kind of creates this pocket. We install it once and then you can drop as many tags as you want, no matter what you want to track.

Cody Haugen: Is that going to be Is that going to be Google Brett?

  
  

### 00:02:39

  

Brett StClair: So, it's a Google Tag Manager and then you can buy many different types of tag manager,

Cody Haugen: Yeah.

Brett StClair: but it's free, the Google one. And then you just load it up with Google Analytics, you can add um HubSpot analytics, you can add NMMP, you can add Facebook analytics, drop cookies, whatever tag you want in there. But we just got to get it in and published.

Cody Haugen: Yeah. No, that's great. It came up in uh a couple of these other conversations that we're setting up with other

Brett StClair: Um

Cody Haugen: um marketing ventures as far as creating content uh with some of these companies and and some other things as far as some uh influencers and that type of thing to be able to tag all of our content appropriately um to track that.

Brett StClair: yeah.

Cody Haugen: So that's good. Um, so if you can share with me once that's all set up, then I can disseminate through the through the other platforms and and other folks. Um, and then the other thing that came up on the MMP side is uh potentially might be working with uh an agency uh called Plexus.

  
  

### 00:03:42

  

Cody Haugen: Um, long story short is he uses Coachaba. Um, and so I didn't know if you had heard of that or um,

Brett StClair: How do you spell it? Coaba maybe

Cody Haugen: it's K haba.

Brett StClair: a I know apps

Cody Haugen: Basically said like it's either apps flyier or coachaba.

Brett StClair: flyer.

Cody Haugen: Okay.

Brett StClair: Um, ok yeah

Cody Haugen: Yeah. Ko cava.

Brett StClair: um the number one absol

Cody Haugen: Who funny

Brett StClair: USP on Kava is we're Appsfly's number one alternative that's the USP

Cody Haugen: not the USP is they are not absol Yeah. would you know typically lead with a stronger typically lead with a stronger sales pitch than that.

Brett StClair: Brilliant. Brilliant.

Cody Haugen: Uh we are not our competitor. Um if you don't mind just giving it a few minutes of review uh today and just letting me know what you think. Um he uses Coachaba already, so we're still waiting on his proposal. We're not in in bed with him quite yet. Um but obviously we're going to review that and and whatever.

  
  

### 00:05:02

  

Cody Haugen: So if we could tie because he already uses Coachaba, tie everything together um for simplicity sake using the same platform. That's the only reason why I suggested it. But yeah, if you could review it and give me some some honest feedback on it, that'd be

Brett StClair: Perfect.

Edwin Johnson: Yeah, Hassan, thanks for the work last night,

Cody Haugen: great.

Edwin Johnson: too, by the way. Our our night. I mean, we really appreciate that. All right, dramatic pause.

Troy McDonald Kane: Yeah,

Hasan Ahmed: building up tension.

Troy McDonald Kane: Brett,

Hasan Ahmed: Yes.

Troy McDonald Kane: you got to buy Hassan new headphones, man. You got to get him like some super Yeah.

Edwin Johnson: Get him the Get him the big ones.

Troy McDonald Kane: Or get him like one of those like uh headsets he just wears like he's a, you know, answering uh 1800 phone numbers, you know.

Edwin Johnson: I think we all just learned a valuable lesson from Tan. the art of seduction.

Cody Haugen: I mean, I was I was sitting in Spence waiting

  
  

### 00:06:05

  

Troy McDonald Kane: I love

Edwin Johnson: I was too I'm like I was like, "Thank you." And he it looked like his face he was going to just be like,

Troy McDonald Kane: you.

Cody Haugen: for

George Westbrook: I

Edwin Johnson: "You know what? You're welcome." But no, he wasn't going to give it to us. He's like, "You wait. You wait until I'm ready." Good for you,

George Westbrook: Yeah, I I definitely think I'd seduce more people if I just stopped

Edwin Johnson: son.

George Westbrook: talking.

Cody Haugen: me too, George. That's our problem.

George Westbrook: Yeah.

Edwin Johnson: I for me,

Cody Haugen: Too much.

Edwin Johnson: George, I'd seduce more if I didn't even show up.

Hasan Ahmed: Just just an online online relation,

George Westbrook: Just just an online online relationship.

Hasan Ahmed: is

Edwin Johnson: I just I get like um Well,

Cody Haugen: indeed.

Edwin Johnson: I could use Hassan's head shot. I could use yours. I wouldn't use King of Beasts because that just they would require too much, you know, maintenance. Maybe a Troy, but uh yeah, just throw the head shot up there and let that do the work.

  
  

### 00:06:55

  

Edwin Johnson: All right. So, we've had a hell of a week, you

Kevin Murray: Yeah.

Brett StClair: Can we talk a little bit about I want to start bringing a little bit of structure into requirements

Edwin Johnson: know.

Brett StClair: coming through and managing the deployment. And the reason why is as we near our production line or production launch, the more change that happens nearing that period, the more risk we're adding into the code base. And so you'll see us going to be pushing back on a lot of stuff saying just we just need to get it up and running. and the key features and functions delivered and then after that we'll carry on building and delivering going into a cadence.

Edwin Johnson: Yep.

Brett StClair: So the first step is that the second step is when it comes to deploying now we've got to be careful. So the couple of reasons you we've got in place something called CI/CD or you probably heard of DevOps and so DevOps and CI/CD is a very structured testing ensuring the quality and the release cycle but it's now going to an app store and two things happen in an app store.

  
  

### 00:08:01

  

Brett StClair: You can either push where we have to do an actual app store push. We try to avoid that but some cases we can't get around it. It's the certain types of code changes insist that we have to do that. Other cases, we can do something called OTAA or over the air. When we do an OTAA, it sounds like we've got lots of flexibility just to keep pushing, but they actually cap you. They cap you at how much you can push. Um, and then you need to do a whole lot of other stuff and we start risking things. So what you'll probably see us do is we're going to start scheduling stuff into those caps and filling that bucket and going yes great we can take it yes we can do it but the release is going to have to be staged in and so it'll be for those two reasons. First one risk. Second one, it's about just filling and making use that we're not blowing now the production criteria that are being governed by each of the app stores through those Two.

  
  

### 00:08:59

  

Brett StClair: verticals. I just want to as we go through this also kind of take you guys on the path and some of the learnings and some of the challenges that we're now going to hit in these production scenes. Is everyone cool with that? Any

Edwin Johnson: I think we're all in

Cody Haugen: Yeah.

Brett StClair: questions?

Cody Haugen: No, I mean that that sounds good. I appreciate you sharing that with us.

Edwin Johnson: agreement.

Cody Haugen: I mean, I do feel targeted personally since I'm the one bringing all the requests to George,

Brett StClair: No, no,

Cody Haugen: but I'm okay.

Brett StClair: no. Don't ever feel Keep bringing it. Keep bringing it.

Cody Haugen: Yeah,

Brett StClair: We'll we'll figure out how to do it and backlog and and and then we'll f******

Cody Haugen: of course. Yeah.

Brett StClair: target you. No, I'm kidding. No,

Cody Haugen: Fair.

Brett StClair: but keep bringing it. I just like if if we don't share with you how we're going to manage it, you guys going to sometimes go,

  
  

### 00:09:34

  

Cody Haugen: Fair.

Brett StClair: "Yeah, but you go like this is this now you're stalling for two weeks." And we're like, "Oh." So, I just want to take you on the journey and I'll remind you guys again and again because I don't expect you to remember all these things. Um but the main thing is risk and compliance.

Cody Haugen: No. Fair and fair.

Brett StClair: Perfect.

Edwin Johnson: George, did you get Yep.

Brett StClair: But keep the ideas coming.

Edwin Johnson: George, did you get my uh doc last night? Did you have a chance to look at

George Westbrook: Yes. Yeah.

Edwin Johnson: it?

George Westbrook: Yeah. Look looking through it. I think there's a there's a few things where I think that was one thing with the if you give me until Monday. Any questions I have, I'll drop them over either over the weekend or on Monday.

Edwin Johnson: No

George Westbrook: Um I think it was around probabilities.

Edwin Johnson: problem.

George Westbrook: No, that wasn't I solved that one. There'll be a few questions.

  
  

### 00:10:27

  

Edwin Johnson: Yeah, no problem.

George Westbrook: I'll send them through.

Edwin Johnson: I mean, the sick part is I spent the entire whatever getting that ready. the document that uh was created by the the the uh AI b*******. The um the first one was 650 pages long. Like I'll get murdered if I try to bring this through.

George Westbrook: I was I was glad you didn't send me that

Edwin Johnson: Yeah. No,

George Westbrook: one.

Edwin Johnson: I mean it's just and a lot of it's you know they tend to be redundant like going over and it's like you know I read through it and I'm like Jesus Christ how many times you going to say the same thing? Um, and you know, I was able to callull it down to I think what was it like 30 I'm

George Westbrook: Yeah.

Edwin Johnson: hopeful that that's close. Um,

George Westbrook: Yeah.

Edwin Johnson: and now that we Cody got me the totals for the NCAA football teams. Um, I'd like to get those updated today. Uh, so we can actually put them into the app, the actual IPO prices.

  
  

### 00:11:25

  

George Westbrook: Yeah.

Edwin Johnson: People can start looking at it, you know, and be like, "Oh, f***. Okay, I want to buy this team or

George Westbrook: Yeah, because that that's one of the the issues that we we we sometimes have with like AI generated documents is it's like if

Edwin Johnson: whatever.

George Westbrook: we're working on maybe we started on version one and now we're working on version three, sometimes it will just automatically change things that we need to keep from version one and then it will overwrite them in version three. And if we're not we're not looking through it then it sometimes overwrites it. It sometimes makes an assumption. So that's why we always like you said it created 650 documents. pages. The same thing happens to us. It's like yeah hundreds of pages of documents is which something that could be done in

Edwin Johnson: Yeah. No, no, no question. There is a trick that I I gathered where I I learned it through Claude which it helped on that

George Westbrook: 10

Edwin Johnson: document because I've been working with both chat GPT and Claude on both because I have pretty significant databases.

  
  

### 00:12:20

  

Edwin Johnson: My chat GP goes back since inauguration. It has everything from inplay that I've ever done on there.

George Westbrook: Right.

Edwin Johnson: And I'm pretty I'm pretty diligent about like updating it each week. If I have a s***** meeting, I'll type in, "Hey, remember this f****** guy or whatever." And it it actually really does. Okay. So, um, but if I freeze a paragraph, then it won't touch it on the on the later iterations. So, like I'm like freeze this paragraph until the doc's done. So, if I I find something that I like, then it tends to stick. Um, cool. So, u I hope to push out those NCAA uh football IPO prices today at some

George Westbrook: Okay, perfect. Yeah, cuz Sports Radar, they weren't I I don't know what was happening there cuz like I say when I was testing I thought it was going absolutely mental.

Edwin Johnson: point.

George Westbrook: I'm like it's it's meant to be there.

Cody Haugen: Yeah, you you and me both. Yeah, it's it's broken for all clients.

  
  

### 00:13:13

  

George Westbrook: Um

Cody Haugen: So, it's a larger issue. They're working on some elaborate fix, but uh yeah, we figured out a

Edwin Johnson: And then and then we need to we do need an answer on that speed of the

Cody Haugen: work. Yeah. Yeah. So, George, this I mean this is a question for you,

Edwin Johnson: gamecast.

Cody Haugen: right? So, you guys developed that new gamecast. I I know we talked about it a couple weeks ago, but just to reiterate the exact answer, the game cast now that you have built, the prettyl looking one, let's call it, um, is running off of the the data feeds that we have licensed,

George Westbrook: Mhm.

Cody Haugen: which are technically called media data feeds.

George Westbrook: Yep.

Cody Haugen: That is that correct?

George Westbrook: Yeah. So we've got the so for old games, so not currently live, it's just a normal API request where it's going to just fetch the information. Pretty simple. The the in-game ones.

Cody Haugen: Yep.

George Westbrook: So it's a it's like a mix of both.

  
  

### 00:14:08

  

George Westbrook: So like what will happen is is when let's say it's the second quarter, um the user clicks onto the page, it's going to fetch all the old data. So all of the events that have happened from before that point in time. then it's going to be streaming in as the events happen. We need to work out when it's that as the events happen, what is the actual delta between it happening in real life and us receiving

Kevin Murray: Let's

George Westbrook: it. There's really not much we can do to control that. Um it's when sports radar sends it to us. Um maybe what we I need to look through the API to see if it gives you the time it happened and the time

Kevin Murray: go.

George Westbrook: that the events delivered. Um, I'd need to work that out.

Cody Haugen: Well, let me give you the let let me give you the answers here,

George Westbrook: Um.

Edwin Johnson: That's Yeah.

Cody Haugen: George. So, so, so the live match tracker that we have licensed Let's call it the ugly one.

  
  

### 00:15:01

  

Cody Haugen: Uh the ugly one is it the backend runs off of bedding data actually. That's why that data is so much faster than our actual raw data feeds.

George Westbrook: Yeah.

Cody Haugen: They're two separate feeds built for two different use cases. Um and so that is the the issue is if we use the ugly one, which we've talked about yesterday, aesthetics aside, we need the speed. Um yeah, go ahead.

George Westbrook: But I'd argue that surely the match tracker that they've built like so how I'd imagine they've built it is just so it's an iframe it's just bit HTML um for the UI which is plugging into the APIs that we would be able to access anyway is

Cody Haugen: We can't but but we can't access those APIs because we are not a licensed sports

George Westbrook: that

Cody Haugen: book. So they only sell those betting feeds to licensed sports books to date. Like no Yeah. No one else in any industry has them.

George Westbrook: Okay.

Cody Haugen: uh is a long story. It's a story for another day.

  
  

### 00:16:03

  

Cody Haugen: But so if we use the prettier version and those medias,

George Westbrook: Yeah.

Cody Haugen: we are losing speed.

George Westbrook: But one thing is would so if we use the live match tracker it's only going to update the UI but it's not going to ping us the request.

Cody Haugen: Correct.

George Westbrook: So so we'd need the the thing that we need the speed for is let's say the market maker um where it needs to know the instant that event happens the market's going to the market's going to potentially move. We'd need to know and we'd need to access that through the API. I think I'd need to double check, but if you're saying that the a we can't access the APIs, we'd have to use the data feed for the for yeah, the the the med media API,

Cody Haugen: media.

George Westbrook: sorry, those APIs to tell the MA market maker, right, do this, do that. And then I might argue then would we want to use the match tracker because then the match tracker is going to be faster than the market maker which means that users in the market can take actions quicker than the market maker can.

  
  

### 00:17:11

  

George Westbrook: Whereas if we limit both that they're both using the same feed. So the instant the event comes to the app because we're using the custom one it's going to reach the market maker at the same time. So even though they might be watching it on the TV and it happens maybe three seconds faster, users that are just in the app, they're just using the app to consume this game, they're going to see it the same time that the market makers going to see it.

Cody Haugen: You're not wrong in that assumption that if they're on the app, yes, the your match tracker would be updating at the same time the market maker has access to that

Edwin Johnson: Yeah, I think what what in a long-winded way,

Cody Haugen: data.

Edwin Johnson: we need to use the fastest speed.

George Westbrook: Yeah.

Edwin Johnson: What whatever it looks like. Um Yeah,

Cody Haugen: The raw data feed you're saying? Yes.

Edwin Johnson: Because that whatever is powering the gamecast, the the big thing is, you know, we this has to run like similar to how like the betting markets are going to work.

  
  

### 00:18:10

  

Edwin Johnson: We can't be lag laggered by a second or two because any anyone in there is going to get frustrated and they're going to get picked off, right? And then you're going to be like, "f*** this." You know, it's too slow. It's too too much latency. So the number one thing here is we have to focus on is that whatever is on that gamecast feed that comes in that's the feed we want to use for the visual. So it's it will be faster than television and then obviously whatever we get in that that um probability the probabilities are off that feed Cody.

Cody Haugen: The probabilities are off the betting feed.

Edwin Johnson: Yeah. Yeah.

Cody Haugen: You're saying those update faster?

Edwin Johnson: So, we're going to be So, we're Yeah. Yeah. Yeah.

Cody Haugen: Yes.

Edwin Johnson: We're gonna be call Yeah.

George Westbrook: and is that the probabilities API?

Edwin Johnson: And we're going to be calling that.

George Westbrook: Okay.

Edwin Johnson: Yeah. We're good,

Cody Haugen: Yes.

Edwin Johnson: George. We're not going to have to build an

  
  

### 00:19:01

  

George Westbrook: Ah, okay. That's fine. market maker will be fine then because the so the market maker is not consuming the event it's

Edwin Johnson: extra

George Westbrook: consuming the probability and if the probability is faster then we just consume that directly because then I suppose it updates the yeah the probability comes in when there's an event and then that updates the ESV which is what the market maker uses to create the

Edwin Johnson: That's right. So the mark the the think of the probability is always going to be the like the the most um valid uh signal for the reference point because whatever happened on the field the probabilities are going to show

George Westbrook: H.

Edwin Johnson: first. Okay. So if there's a fumble or a touchdown or whatever it may be, it'll be extrapolated into the probability and then we extrapolate that probability into the price factoring in all the other things that we have to factor in other than the probability of that

George Westbrook: How how are we calculating the probabilities for the win?

Edwin Johnson: game.

George Westbrook: Because I think in in the document or something when I was looking through earlier, it's anything apart from that specific game.

  
  

### 00:20:11

  

Edwin Johnson: Yeah.

George Westbrook: The probabilities are going to have to be calculated internally for the rest of the season,

Edwin Johnson: Y that's right.

George Westbrook: for the rest of the games.

Edwin Johnson: So we're going to we're going to have u uh essentially there'll be a probability feed or um we can create a custom one. It's basically you know let's say hypothetically uh you know you look three games out and there's a 42% probability that the team's going to win that game. You would take 42% times $5. That would be $210. That would be one input for that game. And you basically have the percentages going out the rest of the season.

George Westbrook: I don't think I don't think sports radar, correct me if I'm wrong here, Cody, like let's say it's week one um and there's 20 weeks. I don't know if they give you probability of that team winning in week 20. So it would be the over

Edwin Johnson: I don't believe they do. Yeah, I don't believe they do. We'll create a custom similar to how I was talking about giving you the um like the

  
  

### 00:21:04

  

George Westbrook: under.

Edwin Johnson: weekly um internally at Inplay. will come up with a I'll come up with a a piece that you can pull for the you know it'll be it'll expect the next number of games out and I I'll I'll build that model in tournament

George Westbrook: Okay, I'll have a look at the for the call it onfield performance the data that we get from sports radar and then how we can use that to calculate a probability for the rest of the season rather than it being a a once a week or once a game thing where you have to input the probability that we think I just that could maybe be something similar for the off-field performance but I think there probably is going to have to be some like manual maybe it's a in the market making platform every Tuesday Um there's the you've got to put in the the onfield offfield performance figures.

Edwin Johnson: Yeah, I mean we we'll work we'll work that out over the next few days. I mean we'll we'll get that. Um that's not my daunting catch.

  
  

### 00:22:09

  

Cody Haugen: Yeah.

George Westbrook: Okay.

Edwin Johnson: tell you something. I need to make sure that we have that fastest speed no matter

Cody Haugen: Yeah. So, yeah. So, I spoke with uh sport radar folks yesterday on the phone.

Edwin Johnson: what.

Cody Haugen: Um I'm setting up a call as soon as possible, hopefully early next week. But I'll continue to push on basically proving why we are even better than a regulated sports uh sports betting market. Uh we are more we are more regulated than a sports betting market.

George Westbrook: Hey,

Cody Haugen: We are more regulated than a prediction market. So I'll keep fighting the good fight and do that lobbying for us to get the betting feeds in parallel.

George Westbrook: heat.

Cody Haugen: But it seems like we have at least a solution in the in the interim.

George Westbrook: I think I remember there's two I think two things regarding sports radar APIs as well is the probabilities API is currently not available in the production environment. Well, so like with sports rad they got the development production.

  
  

### 00:23:05

  

George Westbrook: Um it's not currently in the production one and we got like a um we've got like a thousand quotota limit for the month. Um and then also I think there was um it was something around fetching the probabilities as well. Um I think maybe we might need one called global American football probabilities v2. Um let's see a different sports package from the one our trial key unlocks. Yeah, the current one we got is probabilities v1 and v2's got a bulk probability endpoint. So why we would want that is it's basically the number of queries we'd have to make. So if we if we did it on the current one, the amount of queries is something like 2.5 million a month or down to a million a

Edwin Johnson: Yeah,

George Westbrook: month.

Edwin Johnson: I remember I ran into this same problem when I was doing Yeah, we need unlimited calls on the

Cody Haugen: Yeah. So the way yeah the way the calls work now is a API yes the API calls are in there on

Edwin Johnson: probability.

  
  

### 00:24:03

  

George Westbrook: But

Cody Haugen: the userfacing side but they've reshaped their APAs even before I left. They basically mean nothing. Um,

George Westbrook: hey,

Cody Haugen: and and it truly is more of an unlimited perspective at the at the real time levels. Tro or Troy, sorry. Sorry, Troy. George, can you summarize uh that in an email or send that to support uh because yeah, I'm seeing what you're saying. Probabilities is on our contract that should be in the production level. Um but and and the versioning doesn't necessarily matter either now that they've moved to this whole like one API key to control all like it used to be every product had its own API key and it was just very cumbersome from a client perspective and so now you run with one master API key that forks into all these products. Um, and so getting one, back to my point about API calls not really mattering. Um, but two, um, the versioning doesn't matter

George Westbrook: it.

Cody Haugen: either.

George Westbrook: So I so some of the times when we try and query with that master API key, we get like a not not authenticated.

  
  

### 00:25:16

  

Cody Haugen: Yeah.

George Westbrook: So that's where it's not been allocated to the the sports radar account. And so one of them was that global American football's probabilities. And why that might be useful is one obviously the amount of requests we want to make. So I think what it does is it batches all of the probabilities. So rather than us doing 170 calls or yeah 170 calls,

Cody Haugen: Right.

George Westbrook: it's one call and then we're doing one call every 200 milliseconds during a game rather

Cody Haugen: Yeah.

George Westbrook: than maybe 170. Obviously I know we probably wouldn't do 170 during a game because for different markets they're not going to be going at that refresh rate. Um but I think it was Let me have a look. It's somewhere up here.

Cody Haugen: Well,

George Westbrook: Oh,

Cody Haugen: so, so yeah, I mean the long and short, George,

George Westbrook: nice.

Cody Haugen: I I hear what you're saying. Let's summarize in an email. Let's send it to support Scott and me. I will work with Scott and David to make sure that it's all aligned.

  
  

### 00:26:15

  

George Westbrook: Yep.

Cody Haugen: So yeah, I just need to email from you exactly what versions products that you're seeing that aren't allowing us in and then I'll handle it from the commercial side and we'll get it

Edwin Johnson: By the way, Cody,

Cody Haugen: all one

Edwin Johnson: how long is our contract with Sport Radar?

George Westbrook: Okay.

Edwin Johnson: Yeah.

Cody Haugen: year.

Edwin Johnson: Well, do you think they'll f*** us in year two?

Cody Haugen: I mean, no,

Edwin Johnson: Okay,

Cody Haugen: but I mean, yeah,

Edwin Johnson: maybe.

Cody Haugen: they're they're going to try and increase rates and I'm going to tell them to f*** off and then we're going to agree to some sort of reasonable increase and then we're all happy and

George Westbrook: Stick.

Cody Haugen: move along forward.

Edwin Johnson: Nice.

Cody Haugen: I mean what what is going to happen is is just a natural price increase over this time. So, by the time we get to year two, it's not going to be a huge increase because we're going to add, you know, 10 sports or six sports over the next

Edwin Johnson: Yeah.

  
  

### 00:27:12

  

Edwin Johnson: I was just concerned that if they do a,

Cody Haugen: year.

Edwin Johnson: you know, a deal with the prediction markets that the prediction markets say, "Hey, we don't want InPlate to have access to these feeds.

Cody Haugen: Yeah. I mean, they would never do an exclusive deal. I mean, they work with 900 sports books around the world. FanDuel, Bet 365 could have said that 30 years ago and and they would never do that. They I mean,

Edwin Johnson: Right.

Cody Haugen: they it's funny because they are obviously headquartered in Switzerland, but they actually that's their mantra internally is like they are the Switzerland of everything. They don't choose heads. Um,

Edwin Johnson: Cool.

Cody Haugen: but what we can examine just a quick offshoot and we can take this on offline but is as we add sports or get more comfortable with a long-term relationship with

George Westbrook: Yes.

Cody Haugen: any providers but specifically Sport Radar, we can use adding sports and the betting feeds as leverage in a longer term contract if we so choose.

Edwin Johnson: Okay, cool,

  
  

### 00:28:10

  

Cody Haugen: That that's how I would look at it as far as leverage with them.

Edwin Johnson: cool,

Cody Haugen: Those are those are going to be the levers that they care about.

Edwin Johnson: cool. And Brett, did you send that two pager over to John? Sweet.

George Westbrook: brought to you right

Edwin Johnson: Yeah, f*** that guy. Um,

George Westbrook: now.

Cody Haugen: Hey, send him over that information, but also on the same lane. f***

Edwin Johnson: well,

Cody Haugen: him.

Edwin Johnson: he didn't reach out to us, did he?

Cody Haugen: No, that's crazy.

Edwin Johnson: I mean, I guess people have so much money they don't want anymore, you know. Unfort I I wish that was my case, but it's not. Um, all right, cool. What else do we have today?

George Westbrook: I think one of the only things from our side is just that we're looking into the KYC,

Edwin Johnson: Detroit.

George Westbrook: no KYC versions of the app, seeing the lift lift on that, if it would require a new um Apple review because I agree that's it's a it's it's a good idea.

  
  

### 00:29:06

  

George Westbrook: Um, it's just how how feasible in the time that we've got left to get something built, pushed, tested in the hands of

Edwin Johnson: Yeah. I don't and frankly I don't think it needs to like be the highest priority.

George Westbrook: users.

Edwin Johnson: I think right now we the highest priority is making sure we're ready to launch. Um because I don't think scalewise,

George Westbrook: Yeah.

Edwin Johnson: you know, well maybe I'm wrong, but we're going to put some money into marketing over the next month and we'll hopefully drive some. Is there any way to find out how many downloads have actually happened so far?

George Westbrook: Yes.

Troy McDonald Kane: and one thing I will say, George, is we we we don't really need it until September, the first or the second week of September,

George Westbrook: Okay.

Troy McDonald Kane: because that's when the first academic presentation gets done. So, uh, you have, you know, more. you have a whole month to figure it out. But I I agree with Edwin. The priority is to get the trading functionality pushed out by because we need to test that and we need

  
  

### 00:30:01

  

George Westbrook: Okay.

Troy McDonald Kane: to get this live for the 22nd and then we can continue on trying to find a different way to log in for uh for the academic portion of the

George Westbrook: Huh.

Troy McDonald Kane: competition.

Cody Haugen: Oh, did that T0 call happen this morning? Me and Kevin were sitting on there for like seven minutes. It was just us.

Troy McDonald Kane: It was moved to yesterday.

Cody Haugen: Oh

Troy McDonald Kane: It's It's no longer on It's no longer on Fridays.

Cody Haugen: my.

Troy McDonald Kane: It's Tuesday, Thursdays. So, we're doing Novo calls Monday, Wednesday, Friday, and we're doing T0ero calls Tuesday and

Cody Haugen: Okay.

Troy McDonald Kane: Thursday.

Cody Haugen: I still have an invite for today.

Troy McDonald Kane: Yeah.

Cody Haugen: Okay. No, no worries.

Kevin Murray: Yeah.

Cody Haugen: Yeah,

Troy McDonald Kane: Maybe maybe because it was forwarded to you,

Cody Haugen: I was just wondering if

Troy McDonald Kane: it didn't come off your calendar.

Cody Haugen: potentially for

Troy McDonald Kane: Um Yeah. But yeah, there's no more Friday TZ calls there.

  
  

### 00:30:51

  

Cody Haugen: sure

Kevin Murray: Heat.

Troy McDonald Kane: They should be now Thursday's T0 calls.

Cody Haugen: and I and I do I don't have the Thursday call.

Troy McDonald Kane: Let me see if evangelist didn't do it right. Let's see.

Kevin Murray: Yeah, I've still got

Troy McDonald Kane: No,

Cody Haugen: Yeah,

Troy McDonald Kane: it is.

Cody Haugen: we we can take it all the time,

Troy McDonald Kane: All

Cody Haugen: but yeah, I I don't see a Thursday.

Kevin Murray: a

Cody Haugen: I have a

Troy McDonald Kane: right.

Cody Haugen: Friday. Yeah. So, I mean, I guess where opening to that just generally to the Novo guys, like I mean, I feel like the last couple calls have been productive, right? We've sorted some stuff out. How do we feel? because I feel like that obviously is paramount to the app and paramount to our product is the trading infrastructure but it is also holding up moving to really a lot of other things to get ready for the launch. So yeah,

George Westbrook: Yeah.

Cody Haugen: where do we feel I don't know a ballpark percentage of of where do we feel on on getting that finalized or or you know ready for launch.

  
  

### 00:31:58

  

George Westbrook: Well, it's a non-negotiable that it's going to be ready for launch.

Cody Haugen: Right. Exact.

George Westbrook: Um,

Cody Haugen: Well, exactly

George Westbrook: it it's just it is some of the stuff we're waiting we were waiting on T0

Cody Haugen: right.

George Westbrook: um because it was like one API would be working then they're linking one thing to another thing. So, we've mapped out yesterday um every single component of the trading infrastructure. Where are we at with all of it? Um, what do we need to do? We've got a list of things we need to do. They're like tiny tiny little things like I think have a look on the list. It's things like adding in the cancel feature. Um, adding in the cancel and request feature. So, it's very simple to do. It's just things that we've we've left and it's tightly integrated into the market maker as well. So, obviously the market maker is going to be the thing the thing trading. Um, and like we said, when it comes to actually testing,

  
  

### 00:32:44

  

Cody Haugen: Yeah.

George Westbrook: doing the simulations, we don't need to wait until there's actually a a live game in order to do that because we can say, "Right, let's pick a game that happened Um, last year and let's run the run a simulation based off of that and then we'll set it up in a way on a version

Edwin Johnson: Okay.

George Westbrook: of the app where it's like right it's going to be what was the one that I was using recently or today the the Chiefs versus the Ravens um actually remembered their names um

Edwin Johnson: Nice.

Cody Haugen: Hey,

George Westbrook: the

Cody Haugen: you're you're growing right before my

Edwin Johnson: You're becoming a real revolutionary

Cody Haugen: eyes.

George Westbrook: yeah learn everything new every day I think I've got two teams in my brain at the moment and

Edwin Johnson: church.

George Westbrook: the Giants.

Cody Haugen: There you

George Westbrook: Um, and yeah, so we could say this game,

Cody Haugen: go.

George Westbrook: right? Let's run it. Let's see how it's working. Is everything looking good in our our end from a user's perspective?

  
  

### 00:33:41

  

George Westbrook: How's it looking on the market makers side? Was this working? Was it was it not? Um, and then we can run that multiple times a day if

Edwin Johnson: Cool. I got a question for you on the market maker.

George Westbrook: needed.

Edwin Johnson: Um, can we also have a dashboard? What I'd like to do is have, you know, we're going to have someone from InPlay monitoring uh the the dashboard of of the market. I I want to know like bills and things like that as we get closer, you know, get through. I want to make sure that we're we're running it as close to production as possible so that

George Westbrook: Yeah.

Edwin Johnson: Yeah.

George Westbrook: Yeah. We need we we probably need to take a phased approach to that. I think it's first it's priorities is the market maker is is it like from what we can see

Edwin Johnson: Total total.

George Westbrook: on the back end is it working given that it's obviously that the data is going to be there it's going to be stored

  
  

### 00:34:28

  

Edwin Johnson: Yeah.

George Westbrook: and then first it'll be the representation of that data so maybe some of the variables are static we can't change them but you can see the data next step maybe there's variables we want to change for a um

Edwin Johnson: Yeah. No, I'm not talking about changing the logic of the market maker.

George Westbrook: active trade

Edwin Johnson: I'm just saying like, you know, knowing how many shares it owns of PMX Y and blah blah

George Westbrook: Yeah. Yeah. Yeah. Because it like like we've said,

Edwin Johnson: blah.

George Westbrook: the market maker is just effectively another user. So the same APIs that we'd use to show a user their um their inventory would be the same ones that we'd use for the for the market

Edwin Johnson: Okay,

George Westbrook: maker.

Edwin Johnson: that'll work to start. Um, awesome. What What else do we have, George?

George Westbrook: He's

Brett StClair: Boost up the um where your we can monitor who's registered etc.

Edwin Johnson: Oh yes. Did you get a total

Brett StClair: and put some sex six sexier dashboards on and growth

  
  

### 00:35:26

  

Edwin Johnson: count?

Brett StClair: dashboards and link in the analytics and link the app store numbers through so you can get a more complete version of how things are tracking.

Edwin Johnson: That's awesome.

Brett StClair: Um so that's going to be worked on as well. Um,

Edwin Johnson: Yeah.

Brett StClair: I think the count uh last I saw was 130. That's the

George Westbrook: the logged in. So I think it was so there's a delay in the days. So on on the Wednesday the 22nd there was 37 first time downloads. Um, so we don't know, we don't know for yesterday and we don't obviously know for today

Edwin Johnson: Okay,

George Westbrook: yet.

Edwin Johnson: cool. Yeah, if you get a if you get a count over the weekend, if you could just shoot an email or something,

George Westbrook: Yeah,

Edwin Johnson: that would be awesome.

George Westbrook: I think there's Can everyone log in to App Store Connect and actually like I think you can see it on your side as well. I think if it's

Edwin Johnson: If I actually go to the app store, you're

  
  

### 00:36:30

  

George Westbrook: on to this to this link and

Edwin Johnson: saying

George Westbrook: then log in

Cody Haugen: George.

George Westbrook: with

Cody Haugen: Yeah, George, give me that uh that number again you just said. What was the download?

George Westbrook: 30 37 first time downloads.

Cody Haugen: All right. And we had 64 before and now we have 83 approved KYC's. So,

George Westbrook: Okay.

Cody Haugen: so of that 37, what is that? 19 um have gone through the KYC.

George Westbrook: But it could be I think it could be that maybe some of those downloads are people that have already been KYCed.

Cody Haugen: Ah, fair.

George Westbrook: So like let's Yeah.

Cody Haugen: Yeah. Yeah, fair point. Because that's us, right? Like technically we downloaded it,

George Westbrook: Yeah.

Cody Haugen: but all of us had already gone through the KYC. Fair point.

Troy McDonald Kane: Yeah.

George Westbrook: Yeah.

Troy McDonald Kane: And three of my family members had already gone through the KYC too that downloaded it.

Cody Haugen: Yeah,

Troy McDonald Kane: So, yeah.

  
  

### 00:37:27

  

Cody Haugen: a bunch of mine as well that I had sent. So, no, that's that's a great point actually. So above that, if we take that into account,

Troy McDonald Kane: Yeah.

Cody Haugen: because that actually makes the number sound better, um it is 19 officially new people potentially.

Edwin Johnson: Uh yeah, we we need uh Foxcon more than that, but yeah,

Cody Haugen: No,

Edwin Johnson: it's a good

Cody Haugen: I I I I understand for sure that that those numbers still don't work,

Edwin Johnson: start.

Cody Haugen: but trying to put some lipstick on a peg.

Troy McDonald Kane: The newsletter is going out today,

Edwin Johnson: Yep.

Troy McDonald Kane: right?

Cody Haugen: Yes,

Troy McDonald Kane: Yeah.

Cody Haugen: correct.

Troy McDonald Kane: That will hopefully re-engage or remind people to sign up that haven't already from the last

Edwin Johnson: Oh, this is cool, George. Thank you.

Troy McDonald Kane: update.

Edwin Johnson: Yeah, this

Cody Haugen: Uh, Hassan, have you sent have you had a chance, I'm sorry,

Edwin Johnson: works.

Cody Haugen: to send over that updated CSV file because I've seen probably another 25 registrations come over email.

  
  

### 00:38:20

  

Cody Haugen: Um,

Hasan Ahmed: Um yeah um I'm doing the actual the export now. So then I'll Yeah. Yeah. Um I will probably get they handed over after the call. So yeah.

Edwin Johnson: f***.

Cody Haugen: Thank

Edwin Johnson: I don't know. I Somehow I can't see anybody now.

Cody Haugen: you.

Edwin Johnson: That's funny. There we go. Yeah. All right. Cool. Um, thanks George.

George Westbrook: Well,

Edwin Johnson: That'll work.

George Westbrook: I think I think that's everything from our side. Is there anything else you want to want to talk

Edwin Johnson: No, other than we need to get the the that d******, John,

George Westbrook: Oh,

Edwin Johnson: and then the SSP stuff um or ad server, whatever we got to do there. You're killing it on the market making that the app looks great. Um, are there any other uh new additions that you're doing before um the the launch that are going to be, you know, structural structural or significant on the app? Or is this what we're taking this one to market

  
  

### 00:39:36

  

George Westbrook: two the Oh, notifications. Yeah. Um, notifications,

Edwin Johnson: notification? Yep.

George Westbrook: tax forms, payouts. With payouts, we I say we don't we that's where we're a bit blind at the moment. And same with the with the the tax forms. Um, I suppose worst worst worst case scenario is users can see what they might be getting paid out and they might have to wait a couple of weeks in order to get the payouts into them. If let's say by launch payment providers um deals not signed or it's not integrated, they still be able to receive the payouts. we'll have we'll have the users that have qualified for it um and the amounts and we can just delay the actual paying out. Um so that's worst case scenario because obviously not having trading and not having the market maker is way way worse than not having the ability to get paid out.

Edwin Johnson: Yeah, I mean we can come up with a solution if we have to too, like an intern solution.

George Westbrook: Yeah.

  
  

### 00:40:41

  

Edwin Johnson: The payment processor is starting to become a bugaboo of mine. You know, every everybody's got to have a custom payment, you know. I just I'll zel or wire or do whatever just in the inim. It really doesn't matter. Yeah. It's like Yeah.

George Westbrook: Yeah.

Edwin Johnson: Okay, cool. All right. Um, anything on our end? Troy, Cody,

Cody Haugen: Yeah, I I'll throw I'll throw one thing out there just as we're talking about backlog and roadmap.

Edwin Johnson: Jared,

Cody Haugen: George, is there is there something you guys have already created as far as like I mean just something visually to look at so that I'm not looking at just my list in my notebook, but we can stagger it out months. Okay, these two kind of overlap because we do have some some bandwidth here. Okay, this just in case if we come up with a f****** sweet feature, right? I got to know what's getting pushed and what's getting updated and what are

George Westbrook: Yeah.

Cody Haugen: those what are those, you know, risks of of pushing something.

  
  

### 00:41:38

  

Cody Haugen: I I I outside of I need a better I guess the the the ask is I need a better

George Westbrook: H.

Cody Haugen: insight into your guys's bandwidth or Well,

Edwin Johnson: like a a timeline or

George Westbrook: Yeah.

Cody Haugen: right.

Edwin Johnson: something.

Cody Haugen: I I need to see what they're like currently working on versus what their bandwidth is versus, you know, like we we I just have no idea right now. right now we're just saying like, "Hey guys, work on this feature." And then you're like, "Sweet. Yeah, it's done." And we move on. So like it's it's great. We're all We got We got to this point. But as we continue to evolve and work, I see Brett getting real excited over here.

George Westbrook: really excited.

Brett StClair: of other

George Westbrook: really impress.

Cody Haugen: He's been waiting for this ask for like

Brett StClair: stuff.

Cody Haugen: months.

Brett StClair: As the product matures, right, you got to figure out the cadence. And so you've got a vault. And what I'm going to do is I'm going to work with George and we'll build out something in the vault, whether it be a dashboard that will kind of track how we're releasing, what we're releasing, what our kind of cadence is that kind of gives you this kind of feeling.

  
  

### 00:42:46

  

Brett StClair: Until we launch, it's going to be flat out and we'll pick up stuff and try jam it in and do everything we can.

Cody Haugen: Right.

Brett StClair: Um, but as we go forward, yeah, I really like that. And if we can automate it and it's, you know, we're doing these meetings, we're loading everything into the vault where we analyze everything before goes in the vault. We do our standards in the morning, we break down all the different tasks and see what we can do. We update that and then you can kind of see, okay, that's what's being slotted in. This is where capacity falls. And then you can also then make the calls and go, don't want that now. Hold it. I want to shut it shove this in.

Cody Haugen: Right.

Brett StClair: Push those out.

Cody Haugen: Yeah.

Brett StClair: Happy to take that. you know and allows you to do that kind of planning.

Cody Haugen: Yeah.

Brett StClair: So you we enable you with the right product ownership kind of tooling. So I think that's a great

  
  

### 00:43:30

  

Edwin Johnson: That's

Cody Haugen: Exactly. Yep. Yeah. It's just like,

Brett StClair: idea.

Cody Haugen: you know, where does, you know, research in subscriptions fall?

Edwin Johnson: Okay.

Cody Haugen: You know, like we have no idea except me and George just passing back ideas right now.

George Westbrook: That's

Cody Haugen: Yeah.

George Westbrook: good.

Cody Haugen: It's it's falling off a cliff. We're actually not doing it. Uh we're selling chocolates. Um no, like yeah, like where does that fall, right? Like it's obviously not for the launch as we just

Edwin Johnson: By the way, if we were selling chocolates,

Cody Haugen: discussed.

Edwin Johnson: we'd have more than 37.

Cody Haugen: Probably there's there's enough chocolate lovers out there, me included. Um so yeah, it's just like yeah,

Edwin Johnson: Yeah.

Cody Haugen: obviously not for launch, but like is that September? Is that October? Right. Like and it is October. I disagree with that.

George Westbrook: Hey.

Cody Haugen: Let's have a conversation. It needs to

Edwin Johnson: Yeah.

  
  

### 00:44:15

  

Edwin Johnson: I mean, to your to your point, Cody, we're going to have to insert that research piece in in the next week or two because we want

Cody Haugen: be

Edwin Johnson: these um um influencers to be able to to start talking about we've we do you want to talk really briefly? I know we're over on time. Uh do you want to talk Kevin really briefly on what we've got with those campus kids?

Kevin Murray: Yes. So they're uh what we're doing for we've got the AI clones that are going to be we're

Edwin Johnson: No, not the clones.

Kevin Murray: gonna I'll prefer to walk on.

Edwin Johnson: See uh

Cody Haugen: prefer.

Kevin Murray: Sorry. Yeah.

Edwin Johnson: that

Kevin Murray: So yes,

Cody Haugen: Yep.

Kevin Murray: so these guys have got a podcast that they're going to be going out doing. They did like a a six-h hour one uh last week just on the SEC teams. So they're really excited. to come on board as well um to be able to start dedicating it, you know, 30 minutes, an hour just on in play.

  
  

### 00:45:07

  

Kevin Murray: So, they'll be able to talk through all of the stuff. Then that way we can then grab that content and then chop it all up and then fire it out as well. But um yeah, they're going to do like an analyst piece on their um NCAA teams as well, which is really cool. So, Cody and I are still working on someone for the NFL, but uh yeah, that's that's pretty cool.

Edwin Johnson: Yeah. So, you know, remember we talked about trying to get these guest analysts who are going to give prices if they have a forum to distribute that information and prices. I don't know how many how many preferred walk-ons. What's their social media base?

Kevin Murray: uh I think it's 200,000 I

Edwin Johnson: That's great.

Cody Haugen: Yeah,

Kevin Murray: believe

Cody Haugen: it was like uh the number of views because they're heavy streams and then they've the thing about preferred walk-on is they're only about two months old after being separated from PFF. They used to be under the PFF flag and so they have just started their socials two months ago.

  
  

### 00:46:01

  

Cody Haugen: They have just started all this YouTube streaming, you know, generally two months or more. It was maybe like four or five months actually. Two months. Yeah. But anyways, it's relatively new. They were all under the PFF flag up until that point. So, they are growing substantially. Um, and and really booming it out. Um but yeah,

Edwin Johnson: right?

Cody Haugen: views and and users, they've they've got a pretty good reach in the degenerate college very focused college uh focal

Edwin Johnson: Yeah. So that that that page, you know, when you click on a team and you swipe,

Cody Haugen: point

Edwin Johnson: you see the schedule and all that s***. Well, I want to have one more swipeable, which is like analyst uh prices, you know, different analysts. We'll have one. We'll have we'll have guests in there. We're going to try to get as like four or five of them, like I said, and that way they can distribute. But they're willing to start really quickly.

  
  

### 00:46:53

  

Edwin Johnson: So, I want to try to get that page up. I'll I'll have a sample for you by Monday.

George Westbrook: Okay. Yeah, we need to think about how we do that. Oh, wait. Mute yourself, Max. Yeah,

Max Kingaby: It was me.

George Westbrook: we need to think about how we do that.

Edwin Johnson: What's up next?

George Westbrook: Yeah, we need to think about how we're going to do that because obviously it's every week they're going to have to upload something and then we're going to need to where are they uploading it to?

Edwin Johnson: Mhm.

George Westbrook: How are we going to consume it? How are we going to serve it? Things like that. Um,

Edwin Johnson: Yeah.

Cody Haugen: As you're thinking about this,

George Westbrook: how are we going to label the

Cody Haugen: George. Yeah, as you're thinking about this, George,

George Westbrook: data?

Cody Haugen: I I need to send you the subscription packages and pricing and everything that I'm thinking about um as well. So, you can that'll start to formulate how we should shape this and what we're going to charge for it, of course.

  
  

### 00:47:41

  

Cody Haugen: But from their specific point with these analysts, I would think specifically for college, it's going to be like short video clips almost of the top 25. anything outside the top 25. So, think the next 110 teams is going to be like a two to three cents blurb. on this week's pricing and this week's matchup.

Edwin Johnson: So you envision

Cody Haugen: I would love video. And if we can't put video in the app,

Edwin Johnson: video.

Cody Haugen: then we'll use the video that they're going to create in our socials across our content. So, if it can't live within the app, George, fine. We'll we'll use it in other ways. But when we talked to them yesterday, they're going to create either a separate show for us or give us like a 30 minute 45minut time slot every week in their stream to then so that we can take that 45 minute time slot and chop it up into 30 second minute um content pieces specifically for that team and then we use it out and push it out however we feel is the

  
  

### 00:48:40

  

Edwin Johnson: Yeah. And so just to give you guys just a taste of what the DGEN pool means. So like when you're talking about this kind of focus on the sport, the level of detail these people go into, these are hardcore fans. So the conversion of this group versus like, you know, John Q public is probably, you know, multiples higher with this core group than we'll ever get in the public. Okay? So like, you know, if they have 200,000 followers, I would be very shocked if we don't get a 100,000 of them to sign up.

George Westbrook: H.

Edwin Johnson: Cody, what's your thought?

Cody Haugen: No, that's 100% right. Yeah. I mean, the Dens are the people who

Edwin Johnson: Right. And you know,

Cody Haugen: pay.

Edwin Johnson: we we don't need a ton in in this first iteration. You know, we we're aiming for 500,000 if total. And half of those being dens, we we can make good

Cody Haugen: Yeah. Based on the math we did yesterday,

Edwin Johnson: money.

  
  

### 00:49:44

  

Cody Haugen: what that math netted out to 2 million a month in subscription costs

Kevin Murray: Yeah, Max, just to answer your question,

Edwin Johnson: So

Kevin Murray: yes, we have looked at the Clipper stuff as well.

Cody Haugen: revenue.

Kevin Murray: It's on the list to uh to do as well.

Edwin Johnson: cool.

Kevin Murray: Thanks,

Max Kingaby: Nice. I think it'd be really interesting.

Kevin Murray: mate.

Edwin Johnson: Awesome.

Cody Haugen: I'll I'll send over what I got, George.

Kevin Murray: Appreciate it.

Cody Haugen: At this point, it's still uh I would say always a work in progress and will continue to be even after we launch, right? If we see something's not working, we're gonna have to be agile and move. Maybe the the middle package uh you know is $39.99. Maybe it's $34.99 and that hits harder. Um, but I I'll send over what I have so you can start to digest it, start to come up with your sweet ideas that you come up with and and we'll just ping pong back and

Edwin Johnson: You really do.

Cody Haugen: forth because yeah, it it it does need to be it does need to be obviously I've given it a s***

Edwin Johnson: Cool.

Cody Haugen: ton of thought, but it I would like outside opinion as well and especially because you guys are building the app that has a big component of what we can do.

Edwin Johnson: Um, all right. Well,

George Westbrook: Okay,

Edwin Johnson: listen. Oh, have a great weekend. Let's f****** go, please. And,

George Westbrook: let's f******

Edwin Johnson: um,

George Westbrook: go.

Edwin Johnson: we got less than a month before this is all going to happen.

Cody Haugen: Yeah.

Edwin Johnson: bless our our souls if we don't. Right. So, good luck all.

Troy McDonald Kane: Yeah.

Edwin Johnson: Thanks for the great work uh in play team and uh Novos. We'll talk to you guys on Monday. Available if anyone needs anything. Okay.

Cody Haugen: Okay.

George Westbrook: Perfect.

Troy McDonald Kane: All right.

Kevin Murray: Thank you.

George Westbrook: Speak to you soon.

Edwin Johnson: Take guys.

Cody Haugen: All right. See everybody.

  
  

### Transcription ended after 00:51:21

  

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.

**