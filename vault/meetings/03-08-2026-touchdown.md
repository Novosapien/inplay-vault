---
date: 2026-08-03
type: standup
description: "Monday touchdown, 3 August 2026: the 13 August dry run, Edwin's UI prototype, Sport Radar probabilities signed, maker and taker clarified onto one wallet, the Avalara tax path, and micro-challenges."
source: "Gemini meeting notes, Inplay - App - Touchdown"
scope:
  - "[[market-maker/market-maker]]"
  - "[[ipo-module/ipo-module]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[withdrawal-flow/withdrawal-flow]]"
  - "[[integrations]]"
  - "[[compliance/compliance]]"
  - "[[referral/referral]]"
status: extracted
extracted-to:
  - "[[market-maker/decisions]]"
  - "[[market-maker/parameters]]"
  - "[[market-maker/open-questions]]"
  - "[[market-maker/plan]]"
  - "[[ipo-module/ipo-module]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[withdrawal-flow/withdrawal-flow]]"
  - "[[integrations]]"
  - "[[compliance/eligibility-and-age-gating]]"
  - "[[compliance/regulatory-positioning]]"
  - "[[referral/referral]]"
  - "[[frontend-deployment]]"
---

## Post-Call Analysis

~60-minute Monday touchdown, the longest of the block and the one that changed the product model most.

**Onboarding split into tiers.** Edwin arrived off a 24-hour shift having rebuilt the app's UI himself with Claude across ~80 iterations, prompted, he was explicit, from the legal position rather than the design one. The substantive change underneath it was the decision to allow a **no-KYC public challenge**: email login, no cash prizes, 13+. The trigger was personal, his own brother-in-law and sister-in-law abandoning at the KYC step after a previous identity theft, plus Troy's point that international students can never qualify for cash anyway. Cody immediately extended it to fraternities, alumni associations and school-versus-school competitions, which is where micro-challenges came from.

**Maker and taker were clarified onto one wallet.** George had modelled Friday's call as two separate wallets and could not make it work. Troy corrected it: same entity, same MPID, same inventory, two execution styles, with the broker dealer holding the separate wallet.

**Sport Radar's probabilities contract is signed**, at no extra cost, in the production account, which closes the blocker that had left the pricing engine with no input. The betting feed was explicitly ruled out for this run. Poll cadence set at 500ms in-game.

**Avalara was chosen** for W-9 handling, with the middle of three equally priced integration paths: a one-line embed on an InPlay-branded page, a few hours of work. Payouts themselves remain unresolved and blocked on people rather than decisions.

Legal ran through the call throughout: gun-jumping risk, the SEC filing, 47 states of registrations, and California's geolocation requirements.

| Finding | Destination | Action |
|---------|-------------|--------|
| Three-tier user model: no-KYC public challenge, KYC'd cash tier, international | [[customer-onboarding/customer-onboarding]], [[compliance/eligibility-and-age-gating]] | Major update + new compliance doc |
| Maker and taker share one wallet and MPID; broker dealer is separate | [[market-maker/decisions]] | Supersession recorded explicitly |
| Taker buys 600k of 1M per team; treasury holdback; $75m cap modelling | [[market-maker/parameters]], [[ipo-module/ipo-module]] | Parameters + IPO update |
| Sport Radar probabilities amendment signed, in production, no cost change | [[integrations]], [[market-maker/open-questions]] | S1, S2, S3 resolved |
| Betting feed ruled out for this run; gamecast already runs off it | [[integrations]] | S4 re-scoped |
| Poll at 500ms in-game, slower but still polled overnight | [[market-maker/parameters]] | Parameter row |
| Next-game probabilities post ~15 min after the previous game ends | [[market-maker/parameters]], [[integrations]] | Recorded |
| RP formula restated with the kickoff-delta term; bounded fallbacks | [[market-maker/parameters]] | Parameter row |
| Widen the spread rather than cancel when an input dies | [[market-maker/parameters]] | Fills in N3's shape |
| MM runs end to end on one pass; no orders produced yet | [[market-maker/plan]] | Plan updated |
| Daily report structure owed by Edwin; codifiable not manual | [[market-maker/open-questions]] | New E20 |
| Avalara chosen; middle-ground embed integration path | [[withdrawal-flow/withdrawal-flow]], [[integrations]] | Update + integration row |
| Payout processor still unresolved; merchant application reassigned to Edwin | [[withdrawal-flow/withdrawal-flow]] | Gap recorded |
| Micro-challenges and private leaderboards for universities and frats | [[information-layer/sub-components/leaderboard/leaderboard]] | FLAGGED for a focused session |
| Back-test lab in Edwin's prototype; not before launch | [[information-layer/sub-components/research-tab/research-tab]] | FLAGGED, changelog entry |
| Gun jumping, SEC filing, 47 states, California geolocation | [[compliance/regulatory-positioning]] | New compliance doc |
| 13 Aug dry run, secondary only; Edwin requires an IPO test run too | [[market-maker/plan]], [[delivery/delivery]] | Dates updated |
| OTA bucketing before Apple review; no OTA during review | [[frontend-deployment]] | Section added |
| Referral bonus set to 5x for the rest of August | [[referral/referral]] | Update written |
| Ad inventory must be gated to under-18-safe for non-KYC users | [[advertising/advertising]], [[compliance/eligibility-and-age-gating]] | Constraint C5 |
| Android social blast produced 2 signups | [[frontend-deployment]] | Recorded honestly |

---

Aug 3, 2026

## **Inplay \- App \- Touchdown \- Transcript**

### **00:00:13**

**Max Kingaby:** What's the office like today, guys?

**George Westbrook:** still.

**Brett StClair:** told

**George Westbrook:** Hello.

**Troy McDonald Kane:** Good morning,

**Kevin Murray:** Hey

**Troy McDonald Kane:** afternoon.

**George Westbrook:** I think Brett and Brett and Max have found the uh the backgrounds for the uh

**Kevin Murray:** guys.

**Cody Haugen:** Hello.

**George Westbrook:** this unfortunately that's not what our office looks like.

**Max Kingaby:** I know cuz I'm in a coffee shop.

**George Westbrook:** Coffee shop. Shut up.

**Kevin Murray:** Yes.

**George Westbrook:** Max

**Kevin Murray:** Is it pissing down rain though? That's the only thing that could be true.

**George Westbrook:** it's actually 30° outside so where you

**Kevin Murray:** What is it?

**Max Kingaby:** might be where you are,

**George Westbrook:** are.

**Kevin Murray:** Jeez.

**George Westbrook:** Let me turn my blur off so that you can see the max is obviously not in a coffee

**Troy McDonald Kane:** God, you guys are way hotter than us today.

**George Westbrook:** shop.

**Troy McDonald Kane:** We're only 18 degrees today in Chicago.

**Brett StClair:** Why is it so cold?

**George Westbrook:** It's sunny old England for the past month and a bit

**Brett StClair:** Sure.

### **00:01:10**

**Troy McDonald Kane:** Yeah.

**George Westbrook:** actually.

**Brett StClair:** It's been 28 plus for the last month.

**George Westbrook:** Yeah,

**Brett StClair:** It's more like what?

**George Westbrook:** that's it. The only day that we did have rain was the only day that I've been playing golf. Typical. That's the reason I played awfully as well. Obviously.

**Troy McDonald Kane:** Sure. Yeah.

**George Westbrook:** Yeah.

**Troy McDonald Kane:** Excuses. Excuses.

**George Westbrook:** Yeah. It's just messing with my my setup. That's what it was.

**Brett StClair:** Um, did everyone have a good weekend?

**Kevin Murray:** Yeah, not

**Troy McDonald Kane:** Yeah.

**Kevin Murray:** bad.

**Brett StClair:** Are you wearing a

**Troy McDonald Kane:** Or here. It rained all day Saturday here, so uh kept people inside. But we actually we went to this thing called Medieval Times. I don't know if it's it's such an American thing where you go to this like 11th century like old tournament of like knights and jestering. Yeah. You get like a meal with no silverware.

### **00:02:14**

**Troy McDonald Kane:** You have to eat it with your hands.

**George Westbrook:** Please.

**Brett StClair:** I to one of those.

**Troy McDonald Kane:** Yeah.

**Brett StClair:** We've got one in South Africa called green sleeves.

**Troy McDonald Kane:** Yeah.

**Brett StClair:** Same thing you dress up, eat with your hands, they do a ceremony. Uh all that kind of stuff is really good.

**Troy McDonald Kane:** Yeah.

**Brett StClair:** It's a bit like um having dinner at Max's house.

**Troy McDonald Kane:** No silverware, having to eat chicken with your hands and Yeah. Yeah. All on dirty dishes probably. Yeah.

**Max Kingaby:** Especially when the mom's on A lot.

**Cody Haugen:** Maybe times is a good time though.

**Brett StClair:** Oh, funny.

**Troy McDonald Kane:** Anyone heard from Edwin this morning?

**Kevin Murray:** Nope.

**Troy McDonald Kane:** Yeah.

**Cody Haugen:** No.

**Troy McDonald Kane:** All right. Um,

**Brett StClair:** Just as George has an update on market

**Troy McDonald Kane:** well, while we wait for that,

**Brett StClair:** maker.

**Troy McDonald Kane:** can we I know he sent off a very long document of website changes.

### **00:03:14**

**Troy McDonald Kane:** So, um there there's probably going to be a few more after that iteration, but and I sent a couple more yesterday, but just wanted to um see if there's any questions off of that or feedback from the NOBO team. Yeah.

**Max Kingaby:** Me and George both picked it up.

**George Westbrook:** Don't break things at all.

**Brett StClair:** Max

**Max Kingaby:** So, we've both kind of come in today and my job now is to see what George has done and then compare it with mine, see which one, see what changes are most appropriate and then kind of push the most appropriate changes live. So, um, we should get that turned around with in by the end of the day. So,

**Troy McDonald Kane:** Great.

**Max Kingaby:** I'll have that over to you.

**Troy McDonald Kane:** Perfect. Appreciate it.

**Max Kingaby:** No worries.

**Troy McDonald Kane:** And then uh we did blast out on social media uh what was it? Saturday, Cody and Kevin, the Android app dropped which was nice. So hopefully that Where are we on signups?

### **00:04:14**

**Troy McDonald Kane:** Any uptick in signups, Cody, from that?

**Cody Haugen:** Yeah, you don't want to know. A whopping two. Um,

**Troy McDonald Kane:** Okay.

**Cody Haugen:** Max, uh, real quick on the on the websites though, um, can you just fact check? I don't know if there's like a fancy way to command F basically an entire website, but anyways, I'll give you the short and dirty is we just need to make sure that anywhere we're updating these referrals. Now, we're giving 5x referrals for the rest of August.

**Troy McDonald Kane:** Nothing.

**Cody Haugen:** Um because who cares? There's like a hundred people out there in the ether. Obviously, hopefully more, but uh we're just yeah going 5x the rest of August. So, anywhere there's a a schedule as far as like dates um or sort of any other bonus multipliers on the referral system, just make sure that we update it to to 5X, please.

**Max Kingaby:** Sure. No problem. I'll do that as well.

**Cody Haugen:** Cool. Thank

**Brett StClair:** I think it's you're going to need to update it on the internal system,

### **00:05:11**

**Cody Haugen:** you.

**Brett StClair:** right?

**George Westbrook:** I think that's done.

**Brett StClair:** But I mean for the entire august.

**George Westbrook:** Yeah.

**Brett StClair:** Okay.

**Cody Haugen:** Cool. Thank you

**Brett StClair:** The website stuff. Okay. Cool.

**George Westbrook:** Um,

**Cody Haugen:** guys.

**George Westbrook:** yes. Yeah. Websites getting on it. Um,

**Brett StClair:** Should we talk market maker or should we talk where we are with

**George Westbrook:** uh, I suppose trading is pretty much all there.

**Brett StClair:** trading

**Cody Haugen:** Great.

**George Westbrook:** um pretty much pretty much is leaving that gap where there's bound to be something when we're testing that's slightly not there or just adding that in. from what we see and feel free to jump in if I say anything out of pocket here and it's all it's all Yeah. Um like we'll look at the we'll look at the backend panel, see what the current quantities are. We can trade against it and it's everything's everything's checking out. Um I think the only thing is we're in the their QA environment at the moment.

### **00:06:15**

**George Westbrook:** So like the prices won't they'll change. Um, but you'll see like the price might not be the IPO price or it's it's all kind of test data, but test data coming from T0, not things that we're putting as test or mock data that's got no resemblance on what's actually happening behind the scenes.

**Troy McDonald Kane:** So, I updated the the TZ team over the weekend on what we talked about on Friday with the IPO windows and that we would I ideally like to push for the August 13th dry run. um on that preseason game. Um so I'll follow up with them today ahead of our call with them tomorrow morning, but uh that will be probably one of the main things we'll want to cover is when we can actually do the dry run.

**Kevin Murray:** Okay.

**George Westbrook:** And is that fair? Is that a dry run of the IPO process?

**Troy McDonald Kane:** No, we're not gonna we're not going to I we're not going to do that. We just want to do a dry run of secondary tradings during a game event.

### **00:07:19**

**Troy McDonald Kane:** And so, you know, try to get as many people from this group and our friends and family to kind of trade it as if it was live, you know. Um, you know, through the to the through the test flight app. Uh,

**George Westbrook:** Yeah. Yeah.

**Troy McDonald Kane:** yeah.

**George Westbrook:** I was going to say it had to be had to be the test flight one. Um yeah.

**Troy McDonald Kane:** Yeah.

**George Westbrook:** So we have a small focus group and then we just Morning

**Troy McDonald Kane:** Morning,

**Kevin Murray:** You're on

**Troy McDonald Kane:** Edwin.

**Kevin Murray:** mute.

**Edwin Johnson:** Hey all, um I just heard that we're not going to do a test run on the IPO. That's not correct. We're definitely doing some form of test run on the IPO.

**Troy McDonald Kane:** Not the first test run.

**Edwin Johnson:** Okay, but I want one test run at least before Yeah.

**Troy McDonald Kane:** Yeah.

**Edwin Johnson:** Yeah. Okay, cool.

**Troy McDonald Kane:** Okay.

**Edwin Johnson:** I apologize for being a little bit be uh late.

### **00:08:01**

**Troy McDonald Kane:** Yeah.

**Edwin Johnson:** I pulled a 24-hour shift, George, on the app. So, I've got some things to show. I don't know about this call, but maybe uh later or tomorrow

**George Westbrook:** Yeah. Okay.

**Edwin Johnson:** morning,

**George Westbrook:** Yeah, that works. And it is that what's that mean? like UI changes or Okay,

**Edwin Johnson:** you know. So basically, yeah, it's it's uh you know,

**George Westbrook:** perfect.

**Edwin Johnson:** my my goal was to try to like, you know, get us basically where, you know, we have an offering for the the subscription and we can bifurcate that experience. Going through it, I had to do a a number of um demos on Saturday. And um you know, the app looks great, but the actual like journey is a little bit like clunky to try to get to where you want to get quickly. And I think we've solved that.

**George Westbrook:** Yeah. Okay, perfect. Yeah, because that's the thing with the app now. Just these little refinements which some of them are little, Some of them are bigger.

### **00:09:02**

**George Westbrook:** Um, but it's yeah, that's cuz I think what we're what we're planning on doing is we're going to do an OTAA push, call it earlyish this week. Basically, the two things we need to do, we need to do all the OTAA pushes. Um, bucket everything into there and then do an app store review because we've got like say for the watch page,

**Brett StClair:** That's

**George Westbrook:** in order to get that on there, we need to do an Apple review. The ads we need to do an Apple review and there's a few other things that are going to require that. said we put everything that needs to be OTAA before that then do the Apple review because in that period where Apple's reviewing we don't want to be doing OTAA pushes. I think it's also we're not we're not able to um but it's going to complicate things so we want to get everything not everything in in its entirety and we never change it just anything we want to get into the app before that

**Edwin Johnson:** Sure.

**George Westbrook:** review which could be one day could be four days or could be a week.

### **00:09:55**

**George Westbrook:** um everything we want to get done before

**Edwin Johnson:** Sure. Yeah. Yeah. Um,

**George Westbrook:** that

**Edwin Johnson:** so basically Claude told me that all the code is written for the uh guey. I don't or the UI. Um, I don't know if that's true. We'll see. Um,

**George Westbrook:** for what?

**Edwin Johnson:** I asked it to for the changes I was prop I'm going to propose to make to the app.

**George Westbrook:** Sorry.

**Edwin Johnson:** Um, so the code you're shaking your head.

**George Westbrook:** Okay.

**Brett StClair:** Yeah.

**Edwin Johnson:** No,

**George Westbrook:** Yeah,

**Brett StClair:** So, yeah,

**Edwin Johnson:** Brett.

**Brett StClair:** it it's so we the agents that we have there's like two and a half thousand agents that break it down into these

**George Westbrook:** we

**Brett StClair:** microservices. And so, what Claude will do, it'll do a monolithic B and and it won't

**Edwin Johnson:** Mhm.

**Brett StClair:** work.

**George Westbrook:** could

**Brett StClair:** It so there's a reason why we break it into different agent workforces because it

**George Westbrook:** you

**Brett StClair:** hallucinates so much and so when it hallucinates it says yeah it's all working but it's got no context.

### **00:10:47**

**Brett StClair:** It doesn't understand where it's being hosted, how it's been deployed.

**Edwin Johnson:** Yeah.

**Brett StClair:** Almost

**Edwin Johnson:** Yeah. I I understand all that. Um you know, I did kind of like lay out the groundwork of what you know,

**Brett StClair:** keys

**Edwin Johnson:** my claude knows who you guys are at this point, you know, and knows what the like uh so it's not it's not built out of like nothing. um in terms of background now how this inter interacts with the microervices. We do need to be in a position though where this code, whatever we're building is, you know, changeable at times because we're going to have to constantly be able to improve that user experience to

**Brett StClair:** Yeah.

**Edwin Johnson:** the best of our

**George Westbrook:** Yeah,

**Brett StClair:** So,

**Edwin Johnson:** ability.

**Brett StClair:** I'll let you

**George Westbrook:** it is.

**Brett StClair:** go.

**George Westbrook:** It is all changeable. It's just I'm assuming this is what your claw's done. has maybe either gone on to the PWA, looked at the HTML and then is that is that what it's done or is it like what is it for

### **00:11:42**

**Edwin Johnson:** So yeah. Yeah.

**George Westbrook:** you.

**Edwin Johnson:** So basically what I've taken is I took uh as a benchmark uh to look at and then I said I want to build a new user interface. You know literally I probably spent 30 hours this weekend uh crafting it right. Um because my my main concerns was with Cody and that is how do we bifurcate what like someone if they want to buy a subscription and how is it valued you know how how how does it actually work and how do we differentiate the user experience the gated one versus the ungated one and

**Brett StClair:** Very

**Edwin Johnson:** um so basically I just said look you know I want to build this in uh

**Brett StClair:** helpful.

**Edwin Johnson:** for the user experience and I was like you know I it can't not like work I mean obviously there's going to be f\*\*\*\*\*\* bumps so I don't want to speak for it other than I can show you and then you know I asked about the weight of this code for UI because I was concerned that it's going to get heavy and it's going to become uh you know difficult to manage in terms of performance and um you know I've had it do a bunch of code reviews I don't know we'll see how it works but you know I I think my last version was like 81 or something uh so I I've I've iterated bunch on 80 81 versions over the course

### **00:12:51**

**George Westbrook:** 80 81 what? Sorry. Oh, okay.

**Edwin Johnson:** of the week um for for the for the UI the UI looks I mean it does look amazing and

**George Westbrook:** Okay.

**Edwin Johnson:** the functionality is amazing. It's it's basic it's a it's taken what you've done on the off the base but you know like for the um historical data you know I I put together what what I call like a test lab or you know background a back test lab we basically can say okay well if I would have bought here run it through the game how much would I have made or lost and that would be the basis for us to be able to say you know once we open up like let's say hypothetically we build a a raw database from 2025 because we don't have 2026 yet and we get all the information from sport radar and I put it in a position where we can start having users essentially build let's say two or three four or five criteria uh into a strategy and then they'd be able to back test it over a season or a month or a week and they'd be able to see if that strategy would have made or lost money.

### **00:13:54**

**Edwin Johnson:** So we'll come up with synthetic prices of shares, okay, based on the model on how I have it now, uh with the $2 and half dollars, you know, uh going split between the two volumes of the trading, then the $5 win. And I can go back in time and see what they were expected to win versus what they, you know, ended up. Like for example, the Kansas City Chiefs last year were expected to do very, very well and they didn't even make the playoffs. A number of teams really struggled. They had some injuries, other things. So those are really dynamic. uh use cases for us. The big thing is um you know I sent over the website changes. I've got the legal team uh like this week is a huge week for us legally. Uh we filed you know we did a a full batch file for the SEC last week. The language we have to be very very careful on now. Um, so like you know that uh you know that I've been pushed like more and more to like come up with those stories and like have like a kind of like a walk through what inplay is.

### **00:14:54**

**Edwin Johnson:** That first story got denied by legal this morning. They said no. So they're going to give me a version like Okay, maybe you can do but right now we we're susceptible to I forget what the word is. It is called we are uh there there's something about the way we promote um and condition investor interest in the securities while it remains unqualified gun jumping they call it unlawful gun jumping. So, I have to be be very careful on the messaging on that. And then we've got a whole shitload of things we got to file this week and like 47 states. We have we have a rough rough week for us. Um, so I just on the on the website, I want to make sure it's the same with the way we describe um, you know, these these these shares, you know, I put in a tab basically like, you know, you click in, you know, you open up, you go to your homepage and then let's say, you know, there's a small search says, you know, Dallas, you click on Dallas comes up, click, you go into it, and then there's basically like a, you know, a number of tabs in there.

### **00:16:05**

**Edwin Johnson:** One is about the actual company. So that's where like your IPO price will list. That's how the share flow will list. The QIP numbers, all things related to what production trading will be, we want to simulate to the best of our ability in this. So we can take it offline and do another call on

**George Westbrook:** Yeah, I was I was thinking maybe maybe later today what maybe we me me and you do um we have a

**Edwin Johnson:** that.

**George Westbrook:** call we go through that and I think what what would be quite good as well is maybe having a look to see how how you're using Claude um and then seeing if there's a way that we can get it in a because I think the issue is sometimes with claude it will go too far so it might it might start looking at databases it might start looking at this whereas what where I think you generating code could be good is maybe conceptually like I want this thing here that thing here and then making sure

**Edwin Johnson:** Yeah, that's all I've done, George.

### **00:16:55**

**Brett StClair:** That's

**Edwin Johnson:** That's all I've done on the on the visuals.

**George Westbrook:** okay Yeah.

**Edwin Johnson:** Now, it it actually is amazing because it functions.

**Brett StClair:** it.

**Edwin Johnson:** So, like, you know, while you do like a review of it,

**George Westbrook:** M.

**Edwin Johnson:** like you can hit the multiple tabs. It's not just a picture. And then if you want to go through historical stuff in the game, you can do that, too. I mean,

**George Westbrook:** Yeah.

**Edwin Johnson:** it's pretty f\*\*\*\*\*\* awesome. I'll be honest with you. I've shared a couple photos with the team and it it was it's it's for for a user trading experience. This is pretty

**George Westbrook:** Cuz I think Yeah.

**Edwin Johnson:** badass.

**George Westbrook:** Yeah. Yeah, I think we do a call then we have a look through because it' be good to understand how you're how you're working and how how you want to work and then maybe what we can do is we can go away and create some skills. Think of them like standard operating procedures so that sometimes you're not having to tell it to do the same thing again.

### **00:17:39**

**George Westbrook:** It's kind of like you click a forward slash and then type something and it's going to do exactly what you want every single time. It's going to output something. Um, we can maybe even link it up to your email so that rather than you having to copy paste stuff over, it's just going to either send it to could be on Slack, could be on email. Um, and maybe we have a channel. So that for those sorts of ideas, it just gets push pushed straight there, which should make it make it a bit

**Edwin Johnson:** Oh yeah. Yeah. And that's great.

**George Westbrook:** easier.

**Edwin Johnson:** So you know just and to circle back the prompting of this u enhanced UI was started from the legal because uh you know I I want to make sure that anything

**George Westbrook:** Okay.

**Edwin Johnson:** in there um frames as uh investment and security more than just trading. So, like if you look at if you look at I'm sorry, more than just like uh gamified uh trading or or what looks like, you know, I mean a regulator is always going to say we're gambling, you know, the the bad actors out there, but the the more and more things that we can put in to the app itself that differentiate us from gambling um is going to be very helpful.

### **00:18:47**

**George Westbrook:** Yeah.

**Edwin Johnson:** And so and even in so far as the disclosures and things like that, you know, when when you're a broker and you're someone who's conducting, you know, uh uh financial instrument trading, the requirements for disclosures are much different and even marketing are much different than a gambling product. So, we want to try to make sure that we stay in that lane because I don't want to get denied for the SEC offering circular because we had a, you know, a wrong misstep in phrasing, you know, and again, remember, there's going to be like one side of the aisle is looking to f\*\*\* us all day long and the other side, okay, whatever.

**George Westbrook:** Yeah.

**Edwin Johnson:** Um, but there there's always that a\*\*\*\*\*\* who wants to, you know, be be the guy. So, I just want to make sure we're buttoned up beyond belief before we get to the launch.

**George Westbrook:** M yeah yeah yeah um I suppose one thing market maker so

**Edwin Johnson:** Yeah,

**George Westbrook:** good good news on that so far is it's running end to end caveat that's only on like one run so there's still work to do making sure it's running on the right

### **00:19:43**

**Edwin Johnson:** Oh,

**George Westbrook:** schedules um making sure we deploy it link everything up so all a lot of the the code has been written Now it's just the testing phase. Not the testing in such as let's run orders through it, but testing the connections, testing, making sure if we need it to run every 200 milliseconds during a game, is it going to do that? How are we going to schedule that? Things like

**Edwin Johnson:** Yeah.

**George Westbrook:** that.

**Edwin Johnson:** So on that vein when you say end to end um are there orders being produced or

**George Westbrook:** No.

**Edwin Johnson:** no?

**George Westbrook:** So what what it would be is it would it would take in the inputs um and would spit out an order book.

**Edwin Johnson:** Okay. Will it produce reference price yet or a synthetic reference price?

**George Westbrook:** Um yeah yeah I think

**Edwin Johnson:** Okay, that's great.

**George Westbrook:** the only thing is and I think there's a few is the offfield offfield performance. Um might need to double check have a look through things like that but the onfield performance.

### **00:20:48**

**George Westbrook:** So one of one of the things we're going to do in terms of like the probabilities is like when we're fetching the data from sports radar is let's ideal situation is obviously we get the expected wins Um then we get the probability before the game and the probability during the game. So probability at the start of the game um or the current probability let's say there's a touchdown we get a new probability minus the probability at the start of the game to get the delta and then add that to the expected wins times by five plus the offfield performance and then that's constantly getting the reference price. But there's fallbacks in case let's say we didn't get the probability or there it was stale. We've got fallbacks so that a reference price is going to be published but if it's too far from reality then it's then it's not going to it's not going to pose something that could be destructive. Um cuz this one of the obviously the complexities in it is if something goes down what happens. Um if something's stale what happens.

### **00:21:53**

**George Westbrook:** And just making sure that there's that journal that means it's it's deterministic. So that even though let's say a year's time, we want to put in that exact those exact pieces of data. It's going to come out. It's going to show us exactly what

**Edwin Johnson:** Yeah. So I let me give you like a a pro tip.

**George Westbrook:** happened.

**Edwin Johnson:** So if I'm running a market maker and I'm relying on say 20 inputs and say one of them's down, my width of the bid asks automatically goes wide, right?

**George Westbrook:** Yeah.

**Edwin Johnson:** So I I don't necessarily cancel everything, but I might if I'm normally five prices wide or 10, then I go to like

**George Westbrook:** Yeah, I think because it's the new way we're calculate like because one of the the way we're calculating the spread or the

**Edwin Johnson:** 40

**George Westbrook:** width is that new equation, isn't it? So rather than it being like a lookup table, it's that equation with the volatility number which time decays. So if we fetch the probability and it's I think what's the half like 20 20 seconds I think.

### **00:22:53**

**George Westbrook:** So it's the Is that not all right?

**Edwin Johnson:** I don't know if that's right.

**George Westbrook:** Okay.

**Edwin Johnson:** I'm I'm Yeah,

**George Westbrook:** So I think what it it's

**Edwin Johnson:** I don't know. Real quick, let me ask you pause real quick. Cody,

**George Westbrook:** basic

**Edwin Johnson:** where are we at on the probability? Do we we have to work out a deal to get live probabilities throughout the game?

**Cody Haugen:** Done.

**Edwin Johnson:** Done. Okay, great.

**Cody Haugen:** Yeah. Troy Troy signed the amended contract. No changing cost.

**George Westbrook:** Is it is that the betting

**Cody Haugen:** All of that in our production account. Oh, no. No. Are you talking about the betting feeds, Edwin,

**George Westbrook:** one?

**Cody Haugen:** or are you talking about live probabilities?

**Edwin Johnson:** Well, the live probabilities is what we need to pump the market

**Cody Haugen:** So, the live live probabilities uh has it was supposed to be on the first contract anyway.

**Edwin Johnson:** maker.

**George Westbrook:** I think that's the one we got trial access to.

### **00:23:36**

**Cody Haugen:** So,

**George Westbrook:** This is the one without the data feed, isn't it?

**Cody Haugen:** yeah. So, so now the amendment uh Troy, right? Yeah, I believe you signed that amendment or did they not sign it yet?

**Troy McDonald Kane:** I haven't gotten it yet.

**Cody Haugen:** Okay, I'll follow up with Scott. It might have just because that was late Friday.

**George Westbrook:** That's

**Cody Haugen:** Um but uh yeah,

**Troy McDonald Kane:** Yeah.

**George Westbrook:** it.

**Cody Haugen:** the docyign team probably is just behind, but yes.

**Edwin Johnson:** And what do we need the betting feed four,

**Cody Haugen:** So the betting feed and probabilities feed are two separate feeds.

**Edwin Johnson:** right? So, as long as we have probability for price.

**Cody Haugen:** So

**Edwin Johnson:** Amazing. What will the betting feed give George additionally and team?

**Cody Haugen:** that would give us faster uh playby-play data.

**Edwin Johnson:** Okay. So, the game cast gets

**Cody Haugen:** No. Well,

**Edwin Johnson:** enhanced.

**Cody Haugen:** the gamecast is already running off those betting feeds if you use the sport radar live match

### **00:24:23**

**Edwin Johnson:** Yeah.

**Cody Haugen:** tracker.

**Edwin Johnson:** So, we don't need anything over and above the gamecast and the live probability.

**Cody Haugen:** Okay,

**Edwin Johnson:** That's it for this run for

**Cody Haugen:** then there you go. Yeah, for for this at least,

**Edwin Johnson:** sure.

**Cody Haugen:** I still want to keep the conversation going with Sport Radar just in case if the need ever comes up.

**Edwin Johnson:** Well,

**Cody Haugen:** We

**Edwin Johnson:** here's what I'll tell you. If they want to get a share of f\*\*\*\*\*\*

**Cody Haugen:** have

**Edwin Johnson:** profits, tell them to put out a f\*\*\*\*\*\* press release.

**Cody Haugen:** told them many times.

**Edwin Johnson:** Yeah.

**Cody Haugen:** Many a time.

**Edwin Johnson:** Yeah.

**George Westbrook:** because one quick question is with the so there's the difference so the playbyplay feeds I think this is correct that it doesn't include the probability in that payload like so for the market maker forget the the gamecast is But the so with the playby-play data at that

**Cody Haugen:** Right.

**George Westbrook:** specific feed which will feed to the market maker to do whatever it needs to do.

### **00:25:11**

**George Westbrook:** I don't think in the payload it includes the probability associated with it. So what we have to do is when we get that we need to fetch it. But what we're rather than fetching it at the time of that event happens because the speed it's going to affect the speed because an extra network request. What we'll constantly be doing during a game is fetching the probabilities every two seconds. Um because obviously say if we did it every 200 milliseconds that's 10 times as many requests a year than if it was every 2

**Edwin Johnson:** It doesn't the requests don't matter. Remember, there's no limit on

**George Westbrook:** seconds.

**Edwin Johnson:** requests.

**Cody Haugen:** I'm I'm not worried about the API call limits. It's it's more or less how fast that probabilities is updating. I would probably hit it uh once every second or half a second.

**Edwin Johnson:** Yeah,

**Cody Haugen:** George,

**George Westbrook:** Okay.

**Edwin Johnson:** let's start at 500 millies and then if we have to dial it up or down,

**Cody Haugen:** yeah, I I I Yeah,

### **00:26:01**

**Edwin Johnson:** we

**Cody Haugen:** because if if we're not if we if you're not getting returned,

**Edwin Johnson:** will

**Cody Haugen:** you know, any sort of data update, then obviously, yes, you're just spinning your tires in mud.

**Edwin Johnson:** Well, here, let let me let me let me stop you real quick, too. We only do do those calls during the games at that speed.

**Cody Haugen:** But

**Edwin Johnson:** Outside of games, we slow down to a second,

**George Westbrook:** Yeah.

**Edwin Johnson:** right? Two seconds, whatever.

**George Westbrook:** I I don't think we need outside.

**Edwin Johnson:** Probabilities aren't going to change as much in Thursday night at 2 am as they are during the game.

**George Westbrook:** Yeah. Yeah.

**Edwin Johnson:** So, we can

**George Westbrook:** I think outside the games it doesn't need to it doesn't need to be be a second.

**Edwin Johnson:** do

**Cody Haugen:** Right.

**George Westbrook:** I think um it

**Cody Haugen:** It doesn't even need to be

**Edwin Johnson:** well, no,

**Cody Haugen:** called.

**Edwin Johnson:** it does need to be called because there will be active market participation. The way that the market maker and taker is we want 24/7.

### **00:26:41**

**Cody Haugen:** Oh, right. Yes.

**Edwin Johnson:** You know, the markets will move. I mean,

**Cody Haugen:** Yes.

**Edwin Johnson:** it'll move at its own whatever, but the taker has its, you know, randomized strategy of what it's going to buy or sell. You know, you you'll be laying awake in bed Friday night, 3:00 a.m., can't sleep. Demons win. f\*\*\*

**George Westbrook:** Hm.

**Edwin Johnson:** that. You open up your app, you can start

**George Westbrook:** But with the with the probabilities, so I think with correct if I'm wrong here,

**Edwin Johnson:** trading.

**George Westbrook:** Cody, the probabilities for an upcoming game are not published until shortly before that game. Not shortly meaning minutes, meaning like it could be a day, it could be a week, could be a week

**Edwin Johnson:** It'd be be a week

**Cody Haugen:** What?

**George Westbrook:** before.

**Cody Haugen:** Yeah,

**Edwin Johnson:** before

**Cody Haugen:** it's it's it is before, but yeah, it's not published like continuously like they Yes, I I Scott replied with that uh from the probabilities team um in that email, George, that I forwarded to you.

### **00:27:40**

**Edwin Johnson:** Let me see.

**Cody Haugen:** Uh sure.

**Edwin Johnson:** Send it to me too, Cody. Let me see what he said,

**Cody Haugen:** Yeah, let me find it here with the technical

**Edwin Johnson:** please.

**Cody Haugen:** answer.

**George Westbrook:** Excellent.

**Cody Haugen:** Yeah. So, I guess he doesn't even really touch on exact time. I mean, this is specifically college football that we asked him on, George. Um, not NFL, but it does not say a specific time.

**Edwin Johnson:** Okay, Cody,

**Cody Haugen:** Uh,

**Edwin Johnson:** when do they put let's say okay game's over on Sunday,

**Cody Haugen:** yep.

**Edwin Johnson:** okay, and next week you're playing opponent XYZ. When does the line post at Sport Radar? How quickly after the game?

**Cody Haugen:** Oh, the data.

**Edwin Johnson:** Yeah. Yep.

**Cody Haugen:** You're saying within within 15 minutes they're closing

**Edwin Johnson:** I'm saying, okay, let me explain it. Okay.

**Cody Haugen:** the closing the data with the official tied to

**Edwin Johnson:** Right. So, it's going to be at no later than 15 minutes because the probabilities are just an an extrapolation

### **00:29:18**

**Cody Haugen:** official

**Edwin Johnson:** of what the odds are for the next game. So, if the game's, you know, a 35 point favorite, you can you can extrapolate that number down into a win probability very easily. Okay. So like if if the odds post at 15 minutes after the game, that's when the probability can feed can start being pulled. Until then, we would use the same feed that we had prior. So like that 15 minute wait period, we would just or whatever the wait period is, we

**Cody Haugen:** And it's typically faster than that 15 minutes.

**Edwin Johnson:** would

**Cody Haugen:** They just we always said 15 minutes to cover our asses.

**Edwin Johnson:** Yeah. But you know what I'm saying, right?

**Cody Haugen:** Yep.

**Edwin Johnson:** Cuz like a 3 favorite is,

**Cody Haugen:** Net.

**Edwin Johnson:** you know, a 65% chance winner. So, the numbers just instead of a point spread,

**Cody Haugen:** Yep.

**Edwin Johnson:** the odd the probabilities the odds of the game are actually factor in the probabilities.

**Cody Haugen:** Right.

**Edwin Johnson:** It's not tricky.

### **00:30:18**

**Edwin Johnson:** Cool.

**Cody Haugen:** Yep.

**Edwin Johnson:** Yeah. Um, okay. So, that's great news on the market maker. Um, go ahead, George. Back to you.

**George Westbrook:** Quick question on that is the that daily report that that's going to be submitted that I think is going to be consumed by the market maker. Do you have the structure for that?

**Edwin Johnson:** for my uh my internal to to the market maker. Not

**George Westbrook:** Okay.

**Edwin Johnson:** yet.

**George Westbrook:** Okay. Yeah. Cuz what what we're trying to work out is what's the best way to what's the best way to do that? Um cuz something in terms of phasing initially manual some sort of manual report which gets put into let's call it a market maker platform which then gets sent to the market maker. Um, but what' be good to understand is what are the sorts of things that you're going to be putting in there. Is it stuff that only you in your head is going to been able to put in there or is it something that we can codify and run on a schedule, consume the APIs,

### **00:31:22**

**Edwin Johnson:** No, we could.

**George Westbrook:** build it out?

**Edwin Johnson:** Yeah, we could codify it. Sure.

**George Westbrook:** Okay.

**Edwin Johnson:** Yeah. Yeah. It's it's it's not a what I feel like.

**George Westbrook:** Yeah.

**Edwin Johnson:** It's it's a math quote problem.

**George Westbrook:** Okay.

**Edwin Johnson:** I just haven't I haven't done the um you know the like forwardlooking gains model yet. I know what I want to look like. I just haven't done it.

**George Westbrook:** Okay. Okay. Yeah. And then we Yeah. Then once we got that, then we can incorporate that in. Um next thing is market taker as well. Um look through all that stuff again. And then once the market makers we're happy with where that's at, get the market market taker stuff started. Um, and then I can't remember, did we say that the market takers going to take part in the IPO or it's only going to be the market maker and

**Edwin Johnson:** No, the market taker is going to be the largest IPO buyer of every share of every

### **00:32:09**

**George Westbrook:** users

**Edwin Johnson:** team. So, I want the IPOs to be uh at least I think we what do we say, Troy? 600,000.

**Troy McDonald Kane:** We got at least 600,000. That's

**Edwin Johnson:** So, at least 600,000 shares out of the million shares for both.

**Troy McDonald Kane:** right.

**Edwin Johnson:** We're going to do the same. A million on the N uh NFL and a million on the uh um

**Troy McDonald Kane:** It's 900\.

**Edwin Johnson:** NC.

**Troy McDonald Kane:** It's 900 on the NFL, a million on the

**Edwin Johnson:** Yeah.

**George Westbrook:** And

**Edwin Johnson:** Well,

**Troy McDonald Kane:** NCAA.

**Edwin Johnson:** we're we're going to make it a million on both and then we're just not going to sell all of them.

**George Westbrook:** that's

**Edwin Johnson:** So, it's easy. Troy,

**Troy McDonald Kane:** Yeah, but it's not I thought we were modeling it against the 75 million

**Edwin Johnson:** we'll just Go ahead.

**Troy McDonald Kane:** cap.

**Edwin Johnson:** Yep. Let me finish. So,

**Troy McDonald Kane:** Okay.

**Edwin Johnson:** we're going to hold back a certain amount in reserve for treasury.

### **00:33:00**

**Edwin Johnson:** So the the float versus the public offering can be two different numbers. So it can be you know it could be worth 82 million but uh the the issuance but if you only sell 73 million you qual you know it's fine. So we want to hold back shares into the treasury similar to how we would for um production.

**George Westbrook:** So, sorry, with the So, the it's going to be the taker, not the maker, that's going to buy the majority of the shares.

**Edwin Johnson:** Correct.

**Troy McDonald Kane:** So here here's the way to look at it, George. It's two separate algorithms with two separate sets of uh requirements,

**George Westbrook:** Okay.

**Troy McDonald Kane:** but they're trading under inplay markets, the MPID, I guess. So, you just need to have an ALGO that's a taker algo and you have to have a maker ALGO.

**George Westbrook:** But in my own think so if the one that's meant to provide the liquidity doesn't hold the most amount of shares.

**Edwin Johnson:** No. So it does what?

**Troy McDonald Kane:** It's the same it can I let me let me it's the same entity but it's

### **00:34:04**

**Edwin Johnson:** Yeah.

**Troy McDonald Kane:** two separate functions think of it so that this is how all market making works it's one firm one company one but you have a taker algo and you have a maker algo it's the same inventories it's just different actions in the

**George Westbrook:** Okay. Okay.

**Troy McDonald Kane:** market

**George Westbrook:** So the t the taker is buying buying stuff and the maker is putting out the

**Troy McDonald Kane:** well no in the IPO So the taker is taking buying the shares from the seller which is

**George Westbrook:** Yeah.

**Troy McDonald Kane:** I which is going to be inplay markets the broker dealer the synthetic broker dealer when you operate in

**George Westbrook:** Mhm.

**Troy McDonald Kane:** secondary trading the maker and taker algos run in tandem under the same MPID there's just no maker algo happening during the or passive algo let's call it happening during the IPO it's only a take algo

**George Westbrook:** Okay. And the both those ALOS would have the same wallet because the Oh,

**Troy McDonald Kane:** Yes,

**George Westbrook:** okay. That's where I was getting confused because

### **00:35:03**

**Troy McDonald Kane:** same wallet, same buying power. It's just different execution styles.

**George Westbrook:** uh I that makes because I thought for some reason I thought

**Troy McDonald Kane:** Think of it.

**George Westbrook:** on Friday he was saying there's one wallet for the taker, one wallet for the maker. And I was thinking, well, how can the maker sell stuff or do stuff that the taker owns? And then if Okay, that makes sense

**Troy McDonald Kane:** Nope. There will be two wallets. There'll be the broker dealer wallet which will warehouse all the original shares.

**George Westbrook:** now.

**Troy McDonald Kane:** So I'm having T0 load every single team company up with all shares available to be sold into the IPO under inplay markets the broker dealer. That's one MPID, one entity. Then there's going to be what I'm calling inplay markets the principal trading arm which is going to be the make or taker of those securities. So they'll take in the IPO and then they'll make and take in secondary market back and forth based on the rules that we set

### **00:35:53**

**George Westbrook:** Okay.

**Troy McDonald Kane:** up.

**George Westbrook:** Okay.

**Edwin Johnson:** Think of it like this, Shorts. The first sale isn't done by the market maker and it's not done by the market taker. It's done by the company raising the money.

**George Westbrook:** Mhm.

**Edwin Johnson:** Now obviously we a simulation there's no we haven't taken it public yet but a company let's say uh the Chicago Bears inplay Chicago Bears they're going to go public. They need to raise money. They hire inplay markets to perform that service which is acting as a broker dealer in selling those securities to the public. now and to ensure that we have enough two-sided action and enough demand. We we don't our signups are horrendous right now. It's a it's a woeful at best. I mean, it's not it's a it's a failure to this point, disgustingly. So, so we need to have something that comes in and buys during the IPO. Otherwise, there'll be teams that don't sell any shares whatsoever at an IPO. A complete failure of the IPO.

### **00:36:52**

**George Westbrook:** Hey,

**Edwin Johnson:** we cannot have that for the simulation. So the taker will be the buyer of those securities and then you know he can manage that inventory in secondary operations. If they want to get the market taker flat and there's a lot of interest and people want to buy we can sell those into the market. Does that make

**George Westbrook:** Yeah,

**Edwin Johnson:** sense?

**George Westbrook:** I think yeah, what I'm going to do after this is look through all of the all of the documentation, do some research, make sure my understandings and obviously what we've said in this stand up as well. Um, and by tomorrow or the day after, I'll be I'll be an expert in this Touchwood.

**Edwin Johnson:** we know you will I so I have a couple of practical questions then um we need some dates we need some dates that we can go as targets now it's the third

**George Westbrook:** Yeah.

**Edwin Johnson:** we don't have much time so I know normally people give a lot of padding with dates I'd be careful

**George Westbrook:** Mhm.

**Edwin Johnson:** with the padding Okay, just try to let's just try to work through this.

### **00:37:56**

**Edwin Johnson:** Now, granted, we're going to have a bunch of bumps, right? And we're not going to try to like my my user interface are not meant to like add layers of complexity or work. It's actually for simplicity, but like the user journey that I had trouble on Saturday uh morning taking someone through how to buy and how to get to the to the page and all the other things. It was tricky and it took a long and so as much as we have to make sure the

**George Westbrook:** Yeah.

**Edwin Johnson:** market the the market maker the taker all this b\*\*\*\*\*\*\* is set up at the end of the day that end point or touch point for the user has to be easy and it has to be fun and otherwise we're going to spend all this time money effort energy to get them and then we're going to lose them. So, you know, as as important as everything is, you know, the the user experience and UI is going to be, you know, the most important, frankly.

**George Westbrook:** Is is a lot of the changes is that related to the trading experience or just everything and anything?

### **00:38:56**

**Edwin Johnson:** No, it's not everything and anything. It's a essentially it it's simplifi I'm trying to simplify what you go through and how you get there. So um you know it's uh you know if you look for a team uh you go to a team page and everything you're going to want to know about that team is on that page. You can buy and sell directly from that page. Every page has the same buy and sell. I did remove the floating orange and put just a block at the bottom um that has the same basically buy sell the teen price.

**George Westbrook:** Mhm.

**Edwin Johnson:** It's all basically loaded. Um, you know, I let me let me work with my team. I want to do a demo with them and get their blessings before I say, "Hey, this is the way I want it to be." And I want them to say in agreement, "Hey, we like it." And if we do, then we'd like to present it to you guys, you know, later today or tomorrow.

### **00:39:50**

**Edwin Johnson:** But, you know, when it comes to the timing and factoring, you know, I think we need to all be ready to like over the next three weeks, it's going to be ugly. Like, I mean, I'm telling you, like, you know, like I said, I mean, I I started Saturday morning at 3:00 a.m.

**George Westbrook:** Peace.

**Edwin Johnson:** and I I finished working on it yesterday at like 4:00 in the morning. So, I mean, I I just banged out as much as I possibly could. you know, I did, you know, stuff for the website. I did stuff for the the writing, um, for those blurb pieces. All those things are necessary in order for us to like make sure my ass is covered on a regulatory front, too. So,

**George Westbrook:** Is

**Edwin Johnson:** the closer we get to it, we just, you know,

**George Westbrook:** it?

**Edwin Johnson:** it's just going to be rough. So, I know you guys are AI amazing and uh, and we love that about you, but, you know, just let's try to make sure we can push as much as possible.

### **00:40:41**

**Edwin Johnson:** And if we need a little extra, you know, I know you guys are always there anyway, but like just in general, the next three weeks are going to be rough.

**George Westbrook:** Why we why we stocked up on these the uh the nicotine

**Edwin Johnson:** What do you got there? Oh,

**George Westbrook:** things?

**Edwin Johnson:** are those those Zin packs?

**George Westbrook:** Yeah. Yeah, pretty m pretty

**Edwin Johnson:** Oh, I thought those were like for getting boners.

**George Westbrook:** much.

**Edwin Johnson:** What is it? They're not.

**George Westbrook:** Yeah. No, for like nicotine.

**Edwin Johnson:** Oh, it's a nicotine.

**Cody Haugen:** Yeah. Yes.

**Edwin Johnson:** Oh,

**Cody Haugen:** Your nicotine p.

**George Westbrook:** Yeah.

**Troy McDonald Kane:** It's the modern version of Q is the way you should think about

**Cody Haugen:** Yes.

**Edwin Johnson:** okay. I thought it was a Viagra thing.

**Troy McDonald Kane:** it.

**George Westbrook:** Yeah. Well, you think every time I'm putting one in.

**Cody Haugen:** George

**George Westbrook:** Yeah. Putting one in during a call,

**Edwin Johnson:** You bone up.

**George Westbrook:** I want a

### **00:41:26**

**Edwin Johnson:** Yeah. I mean,

**George Westbrook:** boner.

**Cody Haugen:** walking around the office

**Edwin Johnson:** I hope you got one now, George.

**George Westbrook:** That's what I've got going on this screen.

**Cody Haugen:** with

**George Westbrook:** I've just got p\*\*\*\*\*\* in the background.

**Edwin Johnson:** I don't need it when I look at this rogues gallery. I mean, this is a lot of handsome faces. Um,

**Cody Haugen:** uh

**Edwin Johnson:** what questions you have for us?

**George Westbrook:** Um biggest one was that report for the market maker. Um got the thing through for the tax form.

**Edwin Johnson:** Yeah.

**George Westbrook:** So we'll look into that. See see see how long that's going to take. Um and then not many questions. The only other thing is Cody, I remember you saying about the kind of statuses for everything, what we're planning, working on getting that together. Um, if I'm being honest, I forgot about over the weekend. Um,

**Cody Haugen:** No worries.

**George Westbrook:** but we'll get something get something this week. Just kind of where we're at with stuff,

### **00:42:13**

**Cody Haugen:** Yeah.

**George Westbrook:** what needs to be done on the existing things, the new things, obviously, what needs to be done um and things like that.

**Cody Haugen:** Yeah. Just real quick on the tax thing. So, uh there's there's basically like choose your own path. Um there's three different sort of integration paths with Aera. All are the same price and all the and work as you go. So it's like zero dev time to a full you know one option is zero

**George Westbrook:** Okay.

**Cody Haugen:** dev time or you know an hour and then the third option is like a full integrated solution within the app. Uh I think we obviously move towards that but like after launch and like throughout the trading

**George Westbrook:** H.

**Cody Haugen:** challenge um is like a full SDK they never leave the app they fill out the W9 within the app. The middle ground I think is our solution.

**George Westbrook:** Yeah.

**Cody Haugen:** Um it's it's a simple embed code, one line of embed code. Um and so then it, you know, they go into their account section, they have their cash wallet there, it says, you know, five grand.

### **00:43:17**

**Cody Haugen:** They click withdraw. It just brings them to a different um screen within app um that says like to continue uh receiving your withdrawal amount, you know, click the link to fill out your W9 that you click that link in the app. It does have to in this middle middle ground sort of integration. It does take you out of that but that embed code we can put it on a landing page on our website and the design lives there. So it doesn't look like Avalera.

**George Westbrook:** Yeah.

**Cody Haugen:** It looks all like inplay. It's all our branding. It is our website that they land on but it doesn't have to be done within the app. So we just like hyperlink out of it. It takes them to the browser. They fill it out you know they make the withdrawal uh through the payment.

**George Westbrook:** Heat.

**Cody Haugen:** So, um, yeah, that that's what I would suggest, but let's talk about it more if we need to, but I was trying to simplify it as much for you guys that they they said this integration in

### **00:44:11**

**George Westbrook:** Perfect.

**Cody Haugen:** the in that middle ground that I just explained should be no longer than a couple hours, a few hours

**George Westbrook:** Okay. Yeah.

**Cody Haugen:** to

**George Westbrook:** All right. Perfect. Yeah, we'll look we'll look through the documentation for that. And I think that this I might shoot myself in the foot by saying this, but the their dev time is human dev time, not so it's yeah, we we'll have a look because it could like you said,

**Cody Haugen:** Exactly.

**George Westbrook:** it could be something that's days or maybe even a week or it could be something that an afternoon or a day's worth um could be done. So yeah, because I remember when we when we were putting that on the priorities, it was obviously trading, market maker, ads, and then the tax form. Um but one thing we need to think about is obviously payouts as well. Um because obviously at the moment we don't really have any visibility into what what platform and the dock.

**Edwin Johnson:** Yeah. Um, we're going to come back to you later because Brian's out this week,

### **00:45:04**

**Cody Haugen:** Yeah.

**George Westbrook:** So,

**Edwin Johnson:** right, Troy?

**Troy McDonald Kane:** till Thursday. Yeah,

**Edwin Johnson:** Till Thursday. Okay, cool. We'll come

**Troy McDonald Kane:** he's still he's still on if we need him for anything.

**Edwin Johnson:** back.

**Troy McDonald Kane:** He's just Yeah, he's just on vacation till Wednesday.

**Cody Haugen:** Heat.

**Edwin Johnson:** Cool. No more vacations before we launch. Okay. For

**Cody Haugen:** Yeah. Uh,

**Edwin Johnson:** anybody.

**Troy McDonald Kane:** So,

**Cody Haugen:** Edwin Charles is going to revamp that um is going to revamp that uh merchant application and send it to you.

**Edwin Johnson:** Okay,

**Cody Haugen:** They their their portal is built from like before 1999\.

**Edwin Johnson:** cool.

**Cody Haugen:** Um, you can't reassign the f\*\*\*\*\*\* application, which is the dumbest thing I've ever heard. So,

**Edwin Johnson:** That's

**Cody Haugen:** he's gonna completely cancel what Brian did, which was a couple sections, and just give it to you since you have all banking information anyways.

**Edwin Johnson:** Yep. Yeah, no problem. Um, so George Troy is a very intelligent man as you know.

### **00:45:53**

**Cody Haugen:** Okay.

**Edwin Johnson:** He's a former professor at Depal University and we are going to be in their curriculum this year and he's planning on going to talk to them and one of the things that he's told uh different professors is that we can bifurcate and create our own challenge for among those students. Right? So basically that it's would be a separate challenge um that would be specific to whatever group you know that has a password in or however we can we can assign it. Have you heard about that already or no?

**George Westbrook:** No, no.

**Troy McDonald Kane:** So this was the conversation George we had about creating different

**Edwin Johnson:** Okay.

**Troy McDonald Kane:** leaderboards.

**George Westbrook:** Yeah. So, I thought I how I read that was the around like the KYC stuff. So, if somebody was a if somebody wasn't a resident, um they weren't able to receive the tax thing, they could put in a uni code and then they could trade, but they couldn't be on a leaderboard and they couldn't win any

**Troy McDonald Kane:** right?

### **00:47:07**

**Troy McDonald Kane:** So we talked about where if we gave you a list of participants,

**Edwin Johnson:** Right.

**Troy McDonald Kane:** you would create a separate you can create a separate leaderboard just tracking those participants for that college or

**George Westbrook:** me.

**Troy McDonald Kane:** we also talked about doing it with potential frats or student organizations for inner competition. So it's just about and and these don't have to these are not part of the broader challenge.

**Edwin Johnson:** competition.

**Troy McDonald Kane:** These are going to be micro challenges or micro

**Edwin Johnson:** That's right.

**Troy McDonald Kane:** leaderboards.

**George Westbrook:** In all honesty,

**Edwin Johnson:** And and Okay,

**George Westbrook:** I don't I don't remember that.

**Troy McDonald Kane:** Okay.

**Edwin Johnson:** come on.

**George Westbrook:** Um,

**Edwin Johnson:** Well, let's talk about for a minute before we roll because here's the thing.

**Troy McDonald Kane:** Yeah.

**Edwin Johnson:** So, you know,

**George Westbrook:** yeah.

**Edwin Johnson:** I had dinner with some family on Saturday. Big bill, by the way, for me. not great. Lot of f\*\*\*\*\*\* lot of people showed up to that one. Um and you know my brother-in-law and sister-in-law were very close to they were going to sign up.

### **00:48:00**

**Edwin Johnson:** Um, and Then they got to the KYC and they've recently been hacked. Okay. And they had their identity stolen. And like, you know, he's a doctor and she's like a whatever big shock. And um so both of them didn't do that at KYC. And I'm like, "What the f\*\*\*?" You know, they're like, "Oh." I'm like, "It's safe." They're like, "You know, it took us blah blah blah to get out of it, right? Pain in the ass." So, um, you know, to Troy's point, there's there's something here like for the March Madness, okay? Uh, the big tournament, you can log on to CNBC or I'm sorry, CBS Sports and you can participate in the overall challenge. It's free. And then, uh, you know, if you're going to if you're going to win money, you got to fill out this thing. Um, but then if you're going to just say create a Novo inplay bracket challenge just among us, we can do that too. You can create your own and then people have their own pools and s\*\*\* like that.

### **00:49:00**

**Edwin Johnson:** So, um, that's a like ultra public facing one, which is what I think what we we we might want to consider how we structure this is in order to qualify for any money payouts, you're going to have to fill out the KYC. That's just that's a must. Now, if you want to trade on the public forum, the one with no money, no rewards, you should be able to do that, too. But you don't have to fill out the KYC because at the end of the day we can still monetize that okay to the about the more and more flow we get to the app right that to push the programmatic whatever fine so it's almost like we need a public facing challenge that has no KYC and then I think the barrier to people signing up is zero

**George Westbrook:** For that one, we would need a login. They would need to log in and sign up. Not maybe not necessarily KYC,

**Edwin Johnson:** 100% 100% and I would I would suggest doing the same thing because

**George Westbrook:** but

**Edwin Johnson:** that login gives us some something, right?

### **00:50:02**

**Edwin Johnson:** We get an email, right? They they're not just rolling up on our site and banging out and then gone in order to participate. You'd have to put up some kind of like identifier. Um because as we continue to go to the universities in the fall and if let's say we're going to go back to Harvard, we're going to want to have a Harvard challenge just for them. And you know this way um we can contribute some form of prizes to like that it may not be cash it may be something else that we give to the Harvard students or Texas\&M wherever the f\*\*\* we're going to end up right my so my thought is you know and again I'm spitballing here I'm not I'm not making a decree I'm asking the group in aggregate do we like having that model better because it's almost to me okay Just hear me out. Here's my last bit of sales. to me the free no KYC, no heavy info I can sign up, give an email, login. That's like the first funnel.

### **00:51:05**

**Edwin Johnson:** And then I start to like what I'm doing. I'm like, "Oh, f\*\*\*. I'm going to start trading for cash. I'll give them my KYC. Great. Oh, yeah. I'm doing great. I'm I'm almost winning money. f\*\*\*. The ch the the the actual market's coming up. I'll open up an account for a couple grand." So, I think we we add another layer of funnel by having this. Um because I do think that the KYC thing right in your face just to start out is putting people off before they get a taste of the app or anything. So my the way that I have this one designed in terms of UI is everything other than the pro version is accessible um to everyone who wants to look at it. They don't even have to, you know, if they d they download it, great, you know, and if they want to participate in the public challenge, then we'd have a the login. If they want to participate in these micro challenges like Troy's talking about, that would be great, too, right?

### **00:52:01**

**Edwin Johnson:** So, um, I'm not sure what workload that looks like. I'm not sure, you know, what that means. Can I please get some feedback from folks who either like or don't like this uh bot?

**Troy McDonald Kane:** No, I I mean I think it makes sense. I think the only thing we'll have to look into and the Novo team, please. How does that change any of the app and Android app review process?

**George Westbrook:** So I think in terms of I think in terms of the review it doesn't sound might punch me in a minute. Um it doesn't change too much. Um it's so what would we have to do in terms of ads? We would we would have to gate anything that is not assigned in or probably not even a KYC user to only show under 18 ads. It couldn't show we couldn't have the risk of showing them alcohol things like that. So that that would be one thing. Um obviously anything with the payouts they'd have to be KYC.

### **00:53:03**

**George Westbrook:** Um, it it it changes it changes stuff obviously within the app, but I don't think it would be an issue with the

**Troy McDonald Kane:** And are there any statebystate laws that complicates that as well?

**George Westbrook:** reviews.

**Troy McDonald Kane:** Because I know like California and a few others have their own unique flavor of rules on these apps based on functionality.

**Edwin Johnson:** I've been going through it over the weekend with Vogler and Marlin.

**Troy McDonald Kane:** Yeah. Okay.

**Edwin Johnson:** California is a tricky one. Um because basically we got to have some other like disclaimers that people give up

**Troy McDonald Kane:** Yeah.

**Edwin Johnson:** the GS uh or the geoloccation and all the other stuff that's different in uh state by state. So, we want to make sure that we're ahead of that. I have I have like full attention on legal this week. Like I said, they're investigating all the states just to make sure that I haven't f\*\*\*\*\* anything up. All the registration, all the bonds, I'll sign all those so everyone will be caught up to date.

### **00:53:59**

**Edwin Johnson:** So, I I just don't want have a a blind side because you know this New York State suing Kouchy on Friday is a massive deal because that one could have some

**George Westbrook:** Yeah.

**Edwin Johnson:** teeth and I I talked about this Friday briefly. It could have some teeth because the judge already did not give Kelshi the um restraining order to prevent uh the state from shutting down. What that basically means is on the surface the judge says it's unlikely that Koshi will win on the merits of its argument. Okay? And that allowed the green light for New York to then go ahead and pursue the full-on lawsuit. They would have never sued him if they didn't get like a positive signal from that initial judge's ruling. Um, again, this is going to go to the Supreme Court, but in the interim, like this this is a big deal and it's it's very po can be very powerful if we use it properly. The one thing we don't want to do is get like jammed up in Alabama, you know, that we didn't think of all the like, you know, whatevers.

### **00:55:03**

**Edwin Johnson:** And so, I just want to make sure everything that we have is is buttoned up as tight as possible. So, but any other thoughts on the public facing micro challenges? I mean, anybody hate it? Anybody like it?

**Cody Haugen:** No, I love it. Right. Um, we've talked about this across the alumni associations as well.

**Troy McDonald Kane:** Yeah.

**Cody Haugen:** You go to the tailgates, you get the frats. I mean, there's a there's a hundred different ways to do it. Um, specifically to to the trip down to Texas. Um, is they're going to be at the Texas Oklahoma game. If we can get the frats or other alumni associations signed up beforehand, I mean, you could create the school versus school for that game and we could be at the tailgate promoting it. I mean, there's there's endless possibilities, but yeah, I mean, it it absolutely needs to be a a function of the app to to like what Jason's been saying, of course, like and not to mention all of our international students that can't sign up uh through KYC.

### **00:56:04**

**Cody Haugen:** So, if you dial it back to just that, the students at all of these universities that we're at, there's your your reason right

**Edwin Johnson:** Yeah.

**George Westbrook:** H.

**Edwin Johnson:** I don't know if anyone's been to Harvard recently,

**Cody Haugen:** there.

**Edwin Johnson:** but it basically looks like Beijing, China. No, I'm not I'm not even kidding.

**Cody Haugen:** Yeah.

**Edwin Johnson:** It's

**Cody Haugen:** I mean, yeah. So, for the international students portion of us being in these curriculums and getting these students to trade it and all that stuff, like that's a reason by itself.

**Edwin Johnson:** Yeah. And by the way, George, I'm known to have a little bit of what they call yellow fever. Um, so and there's no cure for my FIFA. Brett Sinclair, did your dog died over the weekend? I have never seen you this serious in my life.

**Brett StClair:** She's sporting a bit of a hangover to be honest.

**Edwin Johnson:** Oh,

**George Westbrook:** Thank you.

**Edwin Johnson:** I like I like it. I like the honesty. I knew you'd come back to us,

### **00:56:58**

**George Westbrook:** Very

**Edwin Johnson:** Brad. Good to know. King Aabia, are you stretched out?

**Brett StClair:** Hopefully.

**Edwin Johnson:** Ready to go for a visa this uh later this month then?

**Max Kingaby:** very ready. Um excited. Refreshing myself and

**George Westbrook:** excited.

**Edwin Johnson:** Great. Well, let let's get a timely launch and we can somehow figure to get you a couple extra What are they?

**Max Kingaby:** preparing.

**Edwin Johnson:** What's the euros down there in pizza? Yeah. So maybe we can get you a couple extra euros.

**Max Kingaby:** Yes.

**Edwin Johnson:** Get yourself a new t-shirt to pick up some some

**George Westbrook:** Yes.

**Brett StClair:** It's not euros. It's getting it's getting on and begging as a currency,

**Edwin Johnson:** string.

**Brett StClair:** I

**Max Kingaby:** the or or the the special medicine you you give the lucky

**Brett StClair:** think.

**Max Kingaby:** ladies.

**Edwin Johnson:** Is that I mean well

**George Westbrook:** Red card.

**Troy McDonald Kane:** Red

**Edwin Johnson:** said.

**Max Kingaby:** Sorry.

**Edwin Johnson:** Um is it expensive in a visa like a night out?

### **00:57:50**

**Troy McDonald Kane:** car.

**Max Kingaby:** Yeah.

**Kevin Murray:** Yeah.

**George Westbrook:** Yes.

**Edwin Johnson:** How how much if you go falls to the wall?

**Max Kingaby:** Depends how good a night out you want to have.

**Edwin Johnson:** Falls to the

**Max Kingaby:** It's unlimited. I mean,

**Edwin Johnson:** wall.

**Max Kingaby:** you could you could, you know, my my friend's a stock broker and his desk could go and spend 100 grand a day,

**George Westbrook:** Yeah.

**Brett StClair:** That's

**Max Kingaby:** but if I'm out there,

**Edwin Johnson:** Wow.

**Max Kingaby:** probably be a grand a

**Edwin Johnson:** Do you know if that stock broker's hiring?

**Max Kingaby:** day.

**Edwin Johnson:** Because I know a guy.

**Max Kingaby:** Probably.

**Edwin Johnson:** Jared,

**Kevin Murray:** Please.

**Edwin Johnson:** you okay there? You look like you've got the just got busted for a

**Jared Sapirman:** wouldn't be the

**Edwin Johnson:** murder.

**Troy McDonald Kane:** Wow. All right. It's Monday morning, everyone.

**Brett StClair:** I'm gonna call this one, I think. Uh,

**Troy McDonald Kane:** Yeah.

**Brett StClair:** who's gonna say let's freaking go?

**Troy McDonald Kane:** This this all gets recorded, by the I just hope we all remember that.

### **00:58:47**

**Cody Haugen:** Yeah.

**Edwin Johnson:** Oh, f\*\*\*.

**Cody Haugen:** Yeah.

**Troy McDonald Kane:** Yeah.

**Edwin Johnson:** All my horrible stories. It's great.

**Max Kingaby:** I do not spike women for AI listening.

**George Westbrook:** I do not

**Troy McDonald Kane:** Yeah.

**Edwin Johnson:** someone.

**George Westbrook:** listen.

**Edwin Johnson:** If I ever get discovery in this, I'm gonna I'm gonna murder whoever reported this myself. I'll have

**Troy McDonald Kane:** Well,

**Edwin Johnson:** Jared.

**Troy McDonald Kane:** I'm an AI clone,

**Brett StClair:** That's

**Troy McDonald Kane:** so I'm actually not here and I'm not liable.

**Brett StClair:** me.

**Troy McDonald Kane:** So,

**Edwin Johnson:** Well, and Jared's process of murder is he starts with the ass and then he moves forward.

**Brett StClair:** Let's

**Cody Haugen:** I'm out. Let's f\*\*\*\*\*\*

**Troy McDonald Kane:** All right. Thank

**George Westbrook:** Let's f\*\*\*\*\*\*

**Brett StClair:** f\*\*\*\*\*\*

**George Westbrook:** go.

**Troy McDonald Kane:** you.

**Edwin Johnson:** George,

**Cody Haugen:** go.

**Edwin Johnson:** let me know when you want to talk about the uh app.

**Brett StClair:** go.

**George Westbrook:** Yes.

**Edwin Johnson:** Okay. Thank you all.

**Troy McDonald Kane:** Uh in play team,

**George Westbrook:** Perfect.

**Edwin Johnson:** Have a good

**Troy McDonald Kane:** can we jump on the team call for 15 minutes real quick,

**Edwin Johnson:** day.

**Troy McDonald Kane:** please? Uh I know we're way over it,

**Kevin Murray:** Yeah.

**Cody Haugen:** Yeah.

**Troy McDonald Kane:** but just 15 minutes I need. All right. Thank you.

**George Westbrook:** Perfect. Eggs.

**Edwin Johnson:** Yeah. Later on.

### **Transcription ended after 00:59:44**

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*