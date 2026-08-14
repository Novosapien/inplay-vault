---
date: 2026-08-12
type: standup
description: "Wednesday touchdown, 12 August 2026: maker and taker running live across all books, the IPO execution interface Edwin needs, ads live in the store build, and the KYC wall as the biggest conversion problem."
source: "Gemini meeting notes, Inplay - App - Touchdown"
scope:
  - "[[market-maker/market-maker]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[advertising/advertising]]"
  - "[[ipo-module/ipo-module]]"
  - "[[information-layer/sub-components/research-tab/research-tab]]"
status: extracted
extracted-to:
  - "[[market-maker/decisions]]"
  - "[[market-maker/open-questions]]"
  - "[[market-maker/parameters]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[advertising/advertising]]"
  - "[[ipo-module/ipo-module]]"
  - "[[information-layer/sub-components/research-tab/research-tab]]"
  - "[[information-layer/sub-components/team-page/team-page]]"
  - "[[delivery/delivery]]"
---

## Post-Call Analysis

~61-minute Wednesday touchdown, ten days before the offering opens. Present: Edwin, Cody, Troy, Jared, Gary (InPlay) and Brett, George, Max, Hasan (Novosapien). The most substantive engineering-status call of the block, and the first where the market maker and taker are reported running continuously against real books.

Three threads dominated. **The engine room is live**: maker and taker have run for 24 hours across all 180 books including the 10 test tickers, two-sided quotes on every one, roughly 1.2 million orders in a day. George set out the guard rails, the tZERO price band, the per-book journal quarantine, and the stale-price workaround at start of day. Edwin corrected the vocabulary in passing, which is worth keeping: an order rests, an execution is when they cross.

**The app's front door is the problem, not its engine.** Edwin's feedback, backed independently by Jared, is that people download the app and do not know what they have downloaded. He put a number on it: he expects to lose half or more at the sign-up wall, and named two family members who refused KYC outright. Troy then demonstrated that the store build already starts with email only and gates KYC to cash prizes, so part of the fear is a TestFlight-versus-store confusion rather than a live defect. The four questions Edwin wants answered on first open are recorded below.

**Advertising is working and Edwin does not like it.** The units serve, the piping is proven, and his reaction to the creative was that it would turn him off the app. He is engaging a former FIFA commercial lawyer for direct brand deals and would rather run no advertising than fight ugly programmatic inventory.

One timeline correction worth carrying into every plan: college football starts on 29 August but, as Cody put it, no media outlet covers college football. The date that matters commercially is **9 September**, the NFL opener.

| Finding | Destination | Action |
|---------|-------------|--------|
| Maker and taker live across all 180 books, 24 hours, ~1.2m orders | [[market-maker/decisions]] | Decision block written |
| Cadence 500ms for testing, tightening toward 200ms for launch | [[market-maker/parameters]] | Parameter row |
| tZERO seeds stale resting orders at start of day; walk-the-price workaround | [[market-maker/decisions]], [[market-maker/open-questions]] | Recorded + new tZERO ask |
| Price band rejects at 30% out, tracked in the journal | [[market-maker/parameters]] | Confirmed |
| Per-book quarantine confirmed in operation | [[market-maker/decisions]] | Confirmed |
| Ops cockpit going to Edwin; needs taker positions, average price, realised and unrealised P&L | [[market-maker/systems/mm-ops-ui]] | Requirement recorded |
| Edwin needs a desktop execution interface for the IPO across 170 teams | [[ipo-module/ipo-module]] | New requirement, dated |
| Probabilities polled not pushed, polling ramps when a game is detected | [[market-maker/parameters]] | Reconfirmed |
| Ads live in the store build, off in TestFlight to avoid click fraud | [[advertising/advertising]] | Update written |
| Tightening ad constraints drops fill rate sharply; running open to gather data | [[advertising/advertising]] | Recorded |
| Edwin prefers direct sales over programmatic; FIFA commercial lawyer engaged | [[advertising/advertising]] | Direction recorded |
| KYC wall estimated to cost 50%+ of downloads | [[customer-onboarding/customer-onboarding]] | Major update |
| Store build already email-only with KYC gated to cash prizes | [[customer-onboarding/customer-onboarding]] | Corrects the fear |
| tZERO say the 18+ requirement can be removed | [[customer-onboarding/customer-onboarding]] | Blocker closing |
| First-open walkthrough named the key blocker by Jared and George | [[customer-onboarding/customer-onboarding]] | Reinforced |
| Strategy lab described as a home run; research seen as the weekday stickiness | [[information-layer/sub-components/research-tab/research-tab]] | Changelog entry |
| Edwin wants Sportradar historical play-by-play, news and depth charts | [[information-layer/sub-components/research-tab/research-tab]] | New ask, routed |
| Analyst reports: the hard part is structured ingestion, not display | [[information-layer/sub-components/team-page/team-page]] | Interim static outlook proposed |
| Back-testing confirmed not before launch | [[information-layer/sub-components/research-tab/research-tab]] | Confirmed |
| Ticker should show IPO price with an IPO label rather than blank data | [[information-layer/sub-components/discovery-home/discovery-home]] | Changelog entry |
| Real commercial D-Day is 9 September, not 29 August | [[delivery/delivery]] | Timeline note |
| Twice-weekly requirement sessions proposed on non-standup days | [[delivery/delivery]] | Cadence proposal |
| Interns to be assigned to analyst content (Troy) | — | Action item |
| Persona meeting held later the same day | — | No action |

---

Aug 12, 2026

## **Inplay \- App \- Touchdown \- Transcript**

### **00:00:09**

**Brett StClair:** Look at those jokers at in play global.

**Inplay Global:** Oh man. I can't see our

**Jared Sapirman:** Cody,

**Inplay Global:** friends.

**Jared Sapirman:** what are those boxes back there?

**Brett StClair:** What are those boxes?

**Inplay Global:** Huh?

**Jared Sapirman:** What are the boxes behind you, Cody?

**Inplay Global:** Yes.

**Jared Sapirman:** Computers.

**Inplay Global:** Bingo. Why do you care?

**Jared Sapirman:** Just It's a new thing. I've never seen those there before.

**Inplay Global:** This is bagels.

**Jared Sapirman:** So,

**Inplay Global:** Bagels. Coca-Cola.

**Brett StClair:** pizza.

**Jared Sapirman:** No, it's

**Inplay Global:** He's probably stuck on

**Jared Sapirman:** not

**Inplay Global:** the

**George Westbrook:** Hello.

**Brett StClair:** Um, George Sun, did you guys manage to sort Car's uh password change request?

**George Westbrook:** In the process of doing so.

**Brett StClair:** Okay, sweet.

**George Westbrook:** Starting with two seconds.

**Inplay Global:** Hey.

**Brett StClair:** Cool.

**Gary Anderson:** I'm not sure what happened. It uh asked me to log on and then it wouldn't take my password and I did a password reset and it wouldn't take my new password. So, I don't know what's going on.

### **00:01:37**

**Brett StClair:** The other guys are looking into it. I just heard them in the background going into the database double checking seeing it works.

**Gary Anderson:** Okay.

**Brett StClair:** Hello

**Inplay Global:** Hello there.

**edwin:** Yo yo,

**Brett StClair:** God is

**edwin:** can you guys hear me?

**Inplay Global:** Yeah.

**edwin:** I can't hear you.

**Brett StClair:** no.

**Inplay Global:** Yeah. I don't know about the sugar notes or whatever. Fake sugars in there. No, but I have we bought a pack and I've been drinking le. So really, I guess I'm just going after a carbon engine. Yeah. Those ones spark on the bread. Yeah, I think like the the strawberry the best, but they're all pretty. Yeah,

**edwin:** Thanks. Yo, can you guys hear me at Okay.

**Brett StClair:** Yeah,

**Inplay Global:** yeah.

**George Westbrook:** Yes.

**edwin:** I couldn't hear you on that last run. All right. Here we go.

**Inplay Global:** Yeah.

**George Westbrook:** How we doing?

**Brett StClair:** Shall we do it? Um,

**edwin:** How are you doing?

**George Westbrook:** Good. Good.

### **00:03:10**

**Brett StClair:** good.

**George Westbrook:** Good.

**edwin:** Nice.

**Brett StClair:** Good.

**George Westbrook:** Nice warm day in the UK

**edwin:** All right.

**George Westbrook:** today.

**Brett StClair:** and and a solar

**edwin:** That's good to know.

**Brett StClair:** eclipse.

**Inplay Global:** Oh, that's right. I forgot. Yeah. Complete solar eclipse.

**Brett StClair:** Complete solar eclipse. So fun and

**Inplay Global:** and immed. And all the planets are aligned.

**Brett StClair:** games.

**Inplay Global:** Maybe this is how we

**edwin:** Wow.

**Inplay Global:** go.

**Brett StClair:** the guy on the corner of uh a region in Oxford Street. He might be on a thing with his campaigning on his uh the end of the world

**edwin:** Thank you.

**Brett StClair:** is

**edwin:** That's all good stuff to know.

**Brett StClair:** um

**edwin:** I'm going to put that in the the memoirs. Awesome. All right. Who's running today?

**Brett StClair:** so yeah let's let me let me run with it.

**edwin:** Brett, George, Troy. Who's taking the

**Brett StClair:** So,

**edwin:** lead?

**Brett StClair:** let's talk outbound reach. Uh, Edwin, um, Cody, thank you very much for your time yesterday.

### **00:04:18**

**Brett StClair:** What I've managed to do is I just work through every single um offer, all the ICPS, all the personas, generated a first draft on it.

**George Westbrook:** She

**Brett StClair:** It's large.

**George Westbrook:** wants

**Brett StClair:** I've sent you guys HTML and then I realized actually probably want to see a PDF version, port you the PDF version. Don't stress about going through it in detail. It's a shitload there.

**George Westbrook:** Jesus.

**Brett StClair:** Like we think about every possible angle. We break it all out. We're trying to train an engine to do this. Um but what if I can ask you both just a quick skim just in case you pick out something f\*\*\* why are we targeting those kind of personas or you know what, f\*\*\* it. I don't want to be talking to those guys like that. You know, this is a much stronger kind of offer. I think we've got something that's good enough.

**edwin:** Cool.

**Brett StClair:** Bearing in mind that as the agents are going out, they're trying to learn from the engagement.

### **00:05:08**

**George Westbrook:** That's

**Brett StClair:** Are they getting any engagement? If they are, why are they getting the engagement? If they're doing that, let's see if we can update things.

**George Westbrook:** wrong.

**Brett StClair:** Um, so it you kind of want to start it somewhere and let it figure it out. Um, is the

**edwin:** Yeah, I I looked at it already to to a little bit of a degree.

**Brett StClair:** way

**edwin:** Not a large degree, but a little bit. So, I'll come back to it.

**Brett StClair:** there's a lot there.

**edwin:** It's a

**Brett StClair:** Um,

**edwin:** lot.

**Brett StClair:** but it needs that kind of dump of information and then it guides it and gets it going. Once you guys just give me a thumbs up, then we'll start the config process and and training certain bots and stuff. Um,

**edwin:** Sounds good.

**Brett StClair:** then Cody, I'm going to send you a backlog and product owner plan. I know you were looking to find something. I want it. I don't know if I'm overkilling. it and everything.

### **00:05:59**

**Brett StClair:** I'd love just some of your feedback to make sure that I'm articulating what you're looking for. Right. What I've tried to do is go here's a headline story, next column. Um, here's a plan for launch, next column, what does the 8 weeks after launch look like, etc., etc., etc. So, you can start slotting stuff in. Um, and just keeping I think it's also we use it internally the the action points, you know, the next month. So we on top of absolutely everything. Um so I'm kind of exposing that a bit. Um so if it does feel like a lot, don't stress. Um then what it's also done is it might have picked up a bunch of stuff on uh team in play, but that's from meetings and from the vault where it's going, hey, I I don't know if we've spoken about this. Uh can we get some confirmation? If you do pick up on any of that, let me know and I'll do the various updates on it. And if it's picked up stuff that's just, yeah, it was a conversation like two months ago.

### **00:07:01**

**Brett StClair:** The s\*\*\* isn't happening. Park it. I'll also do a tidy up. So, we'll need to do a tidy up. Once I think you are happy and I'm happy, then I think uh we should just send it to the team so everyone can kind of keep track of this. Um, and it'll be

**Inplay Global:** Yeah. Great.

**Brett StClair:** good

**Inplay Global:** Do you envision this being a I mean a living breathing document? Right. Yeah. Okay. Great.

**Brett StClair:** changes every every day. It'll change.

**George Westbrook:** Okay.

**Brett StClair:** So, as we upload all our meetings and stuff,

**Inplay Global:** Yeah.

**Brett StClair:** any email correspondence, it goes into the vault and then I'll run the product owner uh bots against it. It'll regenerate and uh then I think we should look at it like on the Friday standup. Just go, okay, cool. Where are we with this?

**Inplay Global:** Yeah.

**Brett StClair:** Just you mean you don't want to overkill it because there's a lot um you don't need to be going into that

### **00:07:44**

**Inplay Global:** Yeah.

**Brett StClair:** kind of detail. Um but it's detail we deal with every single day to make sure things are executed.

**Inplay Global:** Yep. No, that's

**edwin:** What did What's the date that you expect us to start trying to put something out there?

**Brett StClair:** as in putting um messaging

**George Westbrook:** That's

**edwin:** Yeah. Being able to be like,

**Brett StClair:** or

**edwin:** you know, into the ad mob or whatever. When do you foresee putting stuff out there?

**Brett StClair:** um I think if you look at the test app you will see all the ADM mob ads are starting to um showcase hey son we've got it in this version here so we've We've inserted all the ADM Mob ads, we've curated it, we've put all the age verification, all that kind of stuff. Um, and please try not to click on the ads because we don't want it to think that we're trying to dupe the CTR. So, have a look at some of the ads that are coming through. That's currently what's in there. Um, SSP that's being pulled through that it's thinking that's right.

### **00:08:45**

**Brett StClair:** And then we've got a bunch of config that we'll need to So as soon as we go

**edwin:** I don't I don't see anything other than the inplay.

**Brett StClair:** live

**edwin:** play yet. So, is that what I'm looking for?

**George Westbrook:** on on the test flight one. I think we've turned off the ads just in case if I'm wrong on any of this, Hassan. and we've turned them off so that nobody can accidentally click it. Um, you know, even even myself sometimes you're going along, you accidentally click on something and it's their thresholds pretty low before they start going, "What the f\*\*\* are you doing? Stop clicking the ads, blah blah blah," and then they ban you. So on the test flight, we turned it off. But I think Hassan, could you join on your phone and then just show the ones in in your version?

**Hasan Ahmed:** Um

**Inplay Global:** I saw him briefly on the train for like a split second, then you guys pushed out that other update and turned them off. So, they're they're there or at least in the other version,

### **00:09:27**

**Hasan Ahmed:** yeah.

**Brett StClair:** Yeah,

**Inplay Global:** they're there.

**Brett StClair:** it's so high risk. Every time we started going into the SSP platforms, every one of them were warning, if your CTE goes over, we will ban you instantly. No one touch anything.

**Inplay Global:** All

**Brett StClair:** Um,

**Inplay Global:** right.

**Brett StClair:** last thing we need, it's taken so long to get these SSPs to acknowledge, verify, on board, accept, plus verify. We've been having to do a whole lot more verifications across the uh Google ecosystem um that I saw come in yesterday. That needs to be done by September. Um, they just don't make it easy. So, you just got to be super careful with the ads. It's fine your end users using clicking on them, but that's

**edwin:** sounds good. Um, okay. So, we will see if we we get any of those ads. Um, all right. Uh, I'm sorry. Let me let me explain my phone real quick. has had to execute a trade. Um I Okay, go ahead, Hassan. Can you scroll again,

### **00:10:41**

**Hasan Ahmed:** Um so um on this actual version it will be on the actual app

**edwin:** please?

**Hasan Ahmed:** store version and so then if anyone installs the actual app uh through the the actual app store they um are going to have like the real ads. So, if you scroll down on the homepage, like it's over here as an actual ad through the ADM Mob.

**edwin:** Okay, man. That ad looks horrible. Jesus.

**Hasan Ahmed:** Um,

**edwin:** I mean, it looks like, you know, one of those things like when you're like on a like kitten website or something and they're

**George Westbrook:** What's up?

**Brett StClair:** So over time we can tweak but as we tweak it starts giving you warnings

**edwin:** like

**Brett StClair:** potential fill rates drop to a maximum of and so we were playing around with some of the constraints and restrictions and all that kind of stuff and it can drop really quickly if you go too heavy on what you don't want or do want. And so we spend a bit of time rather going f\*\*\* it, we'll take a little bit more. And then, you know, as we see what's kind of coming through, then we decide, you know, is those the kind of ads that we're comfortable with?

### **00:11:51**

**Brett StClair:** Okay, we can tweak it down or tweak it up. Um, but right now, let's just let it flow. Let's get some data through it.

**George Westbrook:** Perfect.

**edwin:** Okay, Jake. What are our thoughts about um Oh, well, let's just continue. You You go ahead. Start start running start going on your next agenda, Brett, if you have stuff.

**Brett StClair:** Yeah. So, um I think the next agenda is are we comfortable with the launch dates? Um teams are starting to acclimatize to a later evening. Um getting up a little bit later and earlier just to make sure everyone's on form. Um do we need to do any syncing up with the TZ team?

**George Westbrook:** No, no. It's pretty much it's business as usual for them.

**Brett StClair:** Happy.

**George Westbrook:** It's just we So, this one of the things we'll be testing today, making sure it So, it's the feeds that are coming through. We know we've got the connection. It's one of those things we can only really test it when there is a live game.

### **00:12:53**

**George Westbrook:** Um,

**Brett StClair:** That's

**George Westbrook:** so worst case tomorrow it's let's say we missed the first game, let's say we miss the second game,

**Brett StClair:** what

**George Westbrook:** there's one at two o'clock in the morning. Um, well 2:00 in the morning our side. So in between that time. So there's one at 12, one at 1, um, and one at 2:00. So we've got three goes tomorrow. Um, for I think the main thing we want to get out tomorrow is is the sports radar data coming through.

**edwin:** I

**George Westbrook:** What would be the best thing in the world is is the sports radar data coming through and is the maker adapting to that

**edwin:** just

**George Westbrook:** accordingly. The way that the makers set up is it's not dependent on the data feed

**Brett StClair:** Wait,

**George Westbrook:** from SP sports radar in terms of the push the push feed because we don't get any probabilities on that. So all it does is it polls when it sees there's a game. It then sets a timer and then ramps up the polling so that it's a lot quicker.

### **00:13:47**

**George Westbrook:** Um rather than because the playby-play data only includes the plays, not the probabilities.

**Brett StClair:** That

**George Westbrook:** So when we know that the game's starting, we ramp up the polling. So any little change we're going to be picking up. If it fails, like it it doesn't matter. We just keep on requesting. Um if it keeps on failing, then the performance is degraded, blah blah blah. Um

**edwin:** Hey Tony, I thought we pay we're paying for the live

**George Westbrook:** but but

**Inplay Global:** We

**edwin:** probability.

**Brett StClair:** It's a bit

**Inplay Global:** are

**George Westbrook:** that's live probability in that we have to request to fetch the data rather than it being a like the with the playbyplay data that's kind of like we go to them hello sports radar give us all your data and just push it to us. Um, with the live probabilities, we have to we have to go to them and request it, but we just request it like very very very frequently.

**Inplay Global:** That's 100% the right setup,

**George Westbrook:** Perfect. Um,

### **00:14:40**

**Inplay Global:** George.

**George Westbrook:** yeah. So, and then I suppose going to the actual maker.

**Brett StClair:** Yes.

**George Westbrook:** Um, we've got well, it was running, it's been running for the last 24 hours across all the allund 180 books because there's 10 test tickers. is Um, so that's been running, that's been turning out orders. We've updated our admin panel as well, which we'll give you access to to see as well. Can everyone see my screen?

**Brett StClair:** Yeah, I was about to say share screen. Let's have a look at that, baby.

**Inplay Global:** Yeah, now we can

**George Westbrook:** So,

**Inplay Global:** George

**Brett StClair:** Zoom in a bit. I don't like saying it. I like I'm

**George Westbrook:** So, it's what we've got here is all the all of the

**Brett StClair:** just

**George Westbrook:** tickers all showing two-sided quotes um or two-sided markets. Um the market m because it's like the business as usual. It's not updating as frequently as it would be during a game.

**Brett StClair:** Awesome.

**George Westbrook:** Um but we'll be testing today when it is a game.

### **00:15:54**

**George Westbrook:** Is it is it updating quick enough? I think it's that every two to 500 milliseconds. I think initially for the test we were aiming for 500 milliseconds and then as time gets closer to launching get it down from 500 to 200 milliseconds. Um and then yeah like cuz the trading the trading's working really well. I mean the maker and the taker I think how many orders have they done in the last Yeah. So today there's been close to 1.2 two million orders done um through the maker and the

**Brett StClair:** Yes.

**edwin:** orders.

**George Westbrook:** taker um um

**edwin:** Orders or trades?

**Brett StClair:** Who is it?

**George Westbrook:** orders I think let's have a

**edwin:** Do you know how many times the tra the maker crossed the bid ask of the 1.2 million

**George Westbrook:** look

**edwin:** quotes?

**George Westbrook:** I think it might be let me

**Brett StClair:** Good

**George Westbrook:** cuz I think the the taker at the moment is not running as so it's there it's constantly taking stuff off

**Brett StClair:** evening.

**George Westbrook:** all of the markets but obviously per market it's not I think it's like every I want to say 20

### **00:17:17**

**Brett StClair:** I'm

**George Westbrook:** seconds. Um,

**Brett StClair:** not

**George Westbrook:** these were rejected. So, some one of sometimes when we see them get rejected is because T0 got stuff running and then the price is within if a if it's out by 30%. Either way, then it automatically gets rejected.

**edwin:** Yeah. The price span. So,

**George Westbrook:** Um

**edwin:** so just so our vernacular is the same, an order is just an order on the book. Okay. That we call an order a resting order.

**George Westbrook:** yeah.

**edwin:** You know, an execution or a trade is when they cross.

**Brett StClair:** Yeah.

**George Westbrook:** Yeah.

**edwin:** Are they crossing at all? Has there been any trait?

**George Westbrook:** Yes. So these are I think we call them order order execution.

**Brett StClair:** Yes.

**George Westbrook:** So these are all so the accepted the field ones. We need to add some more filter in here. So one of the things we're adding into this part here which isn't it's semifunctional but will be by the end of today is the first the manual orders for the taker.

### **00:18:23**

**George Westbrook:** Um,

**Brett StClair:** I'm dead.

**George Westbrook:** and then this kind of cockpit. Um, basically we're just it's just going to be able to see more in in detail into what's happening in both the maker and the

**edwin:** Okay.

**George Westbrook:** taker.

**edwin:** Um, but as you speak, as you've been running the market maker, what we need, so we need the taker to show like all the positions it has, right? So, it's got to have like not just its orders,

**George Westbrook:** Yes.

**edwin:** but we need to know like what is it long or short or whatever. Then we actually need to know the average price that they're long or short from.

**Brett StClair:** Yeah.

**George Westbrook:** Yeah.

**edwin:** And then we have to know the you know theoretical P\&L on those realized and

**George Westbrook:** Is this Is this

**edwin:** unrealized.

**George Westbrook:** Yeah.

**Brett StClair:** some of those.

**George Westbrook:** Okay. Yeah.

**Brett StClair:** Okay.

**George Westbrook:** We'll get we'll get we'll get that all added in. Um, and then what we'll do is we'll send this over to you with a with a login. Some of this stuff you're not going to need to need to see like the referral simulation or the load testing stuff.

### **00:19:28**

**George Westbrook:** Um, but some of this stuff up here I think would be would be relevant. And obviously the market data stuff as

**edwin:** Cool.

**George Westbrook:** well.

**edwin:** And then like for me to execute those orders on the IPOs, I need some kind of like execution or I do it through the app underneath the like uh the app's going to be kind of a pain in the ass. It would be better if I had something that I could click multiple times with a mouse cuz logging in and out

**George Westbrook:** Yeah.

**edwin:** of 170 teams on the phone is going to be

**George Westbrook:** Yeah. Yeah. This. So, this thing,

**edwin:** cumbersome.

**George Westbrook:** this thing here is where it will be. Um, so let me see if it's I haven't actually tested this part yet.

**edwin:** Okay, I can see I'm getting old. George, my screen's tiny.

**George Westbrook:** Let's have a look. And then is one of the things what we still need to work out is so is the we've got the journal for the both the maker and the taker.

### **00:20:28**

**George Westbrook:** And if sometimes it if it's if it's not tracked in the journal, then it's like, f\*\*\*, something's gone wrong. Shut it all down. Send us a notification and investigate. um because that that journal is that central source of truth. So that if if that diverges at all um something's gone wrong. Um but I think we've got it per per book.

**edwin:** There we

**George Westbrook:** So it's it's not as if if one if one book there's something not in the journal,

**edwin:** go.

**George Westbrook:** it's going to not it's not going to shut down everything. Um, but what it will do is the maker if there's an issue on one of the books, it's going to cancel all of the orders for that specific book so that it's not let's say it's random. There's a lot of guard rails in that it's it's obvious there's the bands. So, if price price bands, so if it's 30% above or 30% below, they're autorejected by T0 um tracked in the journal.

**edwin:** Sure.

**George Westbrook:** Um, and then also if there's some internal issues like the performance is slightly degraded or it's not quoting.

### **00:21:33**

**edwin:** Sure. We shouldn't be quoting 30% outside the ban though,

**George Westbrook:** Yeah,

**edwin:** right? I mean, it's a Go

**George Westbrook:** it is I think in the last well the tests over

**edwin:** ahead.

**George Westbrook:** the last 3 days there's not been the only times it would happen is when so T0 at the start of the day they they clear the books then they have something on their side which places resting orders on old prices. Um, but we've got we've got a workar around that we're doing at the moment, but we know that they can just turn that off. But all we do if that happens is I think it's with with the jets. So, we'll just place loads of orders to walk the price up. I think it takes like nine and then then we can start placing placing the orders. So, we can walk the price up from I think it's like 18 to 40 then get the market maker churning through it.

**edwin:** Okay. Okay. Just uh keep me posted on that one, okay? Because it's pretty important.

### **00:22:30**

**George Westbrook:** Yes.

**edwin:** Yeah. Okay. Cool. um before the IPO next Saturday um for the beginning of

**George Westbrook:** Yeah.

**edwin:** it, we should probably have I should probably have access to that um exe executable uh interface and we should probably

**George Westbrook:** Yeah.

**edwin:** test one at least a couple orders to make sure they go

**George Westbrook:** 100%.

**edwin:** through.

**George Westbrook:** Yeah. it what we'll do we'll we'll do loads of testing our side. Um I say it's using exactly the same infrastructure that's on the app. So it will just be minor little config issues maybe related to the journal. Um but we'll we'll sort them out as soon as they're sorted we'll send it over then we can then we can then you can test it out. Um, I suppose as well once you've sent it over, if there's anything else that you'd want to see on that admin panel that that that I just showed, just let let us know because it's all all it really is is just consuming the data and all of the behemoth of infrastructure below

### **00:23:33**

**edwin:** Okay. Okay.

**George Westbrook:** it.

**edwin:** Where? Um All right. What's next, Brett? I'll let you keep going.

**Brett StClair:** So, next up is let's just talk about the updates in the app that you were sending through. Um, we've completed pretty much all of them. Hey, George.

**George Westbrook:** Uh like probably 70 80%

**Brett StClair:** Um, what's wrong?

**edwin:** In terms of what I saw today when I downloaded test flight. You think that 70 to 80% of my changes are in in

**George Westbrook:** No. So in some of our internal so stuff like the um I think like we mentioned last week like the

**Brett StClair:** Thanks.

**edwin:** there.

**George Westbrook:** back testing the the analyst reports and stuff like that that's the back testing unfortunately

**Brett StClair:** Yep.

**George Westbrook:** I don't think that's going to be ready before launch. um the analyst reports as well is the the hard part about that is not viewing the data, it's getting that data. So, we'd need like a little mini platform that an analyst can view into can view then can put in the data in a structured way because we can't really have it where it would need to be like this is paragraph about X, please put in information because we need it all to to match up and be structured.

### **00:24:45**

**edwin:** No, I I get that. Um, you know, we have we have people and we have a bunch of people who seemingly don't have a lot of s\*\*\* to do. So, we can we can assign tasks to people um to to provide the the reports need be. I mean, Troy, what are your thoughts about putting like a couple of these interns on it?

**Inplay Global:** Yeah, that's exactly what I was thinking.

**edwin:** Okay. Do we have anybody that like you you think is like uh smart and and numbers wise that you

**Inplay Global:** Yeah,

**edwin:** like?

**Inplay Global:** probably uh Ambath and Ronic probably would be my two top picks right now. So, Harvard and

**edwin:** Okay.

**Inplay Global:** Northwestern.

**edwin:** Okay. Um, all right. Cool. Well, we will uh let let's chat about that on our next

**Inplay Global:** Okay.

**George Westbrook:** What what we could do is just and this would be touchwood pretty easy is having

**edwin:** meeting.

**George Westbrook:** a a market uh start of season analyst outlook which for the first maybe two or three weeks stays there and that's static and in that we can that's pretty simple.

### **00:25:51**

**Brett StClair:** All

**edwin:** Mhm.

**George Westbrook:** we just get the information and just put it in the app.

**edwin:** Yeah.

**George Westbrook:** Um it's going forward when let's say there's an analyst report every week or every two weeks.

**Brett StClair:** right.

**George Westbrook:** That's where we'd need the call it platform in order for them to log in, put it in blah blah blah,

**Brett StClair:** Uhoh.

**George Westbrook:** which is which is a lot more is a lot larger uplift.

**edwin:** Understood. Understood. Um, remember the actual games don't start until August 29th, at least in college football. And then I think what we're like 10 days later, 12 days later, Cody 9\.

**Inplay Global:** Yeah. September

**edwin:** Yeah. Yeah. Okay, cool.

**Inplay Global:** 9th

**edwin:** Um, so what's it? Yeah, it's 11 days later. Okay. Um,

**Brett StClair:** book sign up and verification quickly.

**edwin:** say

**Brett StClair:** We've got sign up and verification.

**edwin:** again.

**Brett StClair:** We've got a meeting um with Persona later on today.

**edwin:** Okay. And you know, from what I saw, I downloaded the app and uh or you know, updated the app.

### **00:26:56**

**edwin:** Um, we're still in a in tricky spot here because first thing I got hit with was the KYC and you know we're we're about we're trying to get these influencers and things like that Brett you recommended and you know I don't want to do a lot of outreach okay that's going to have a bunch of people get to the app and say f\*\*\* this I'm not going to put up my my ID until I know what the hell I'm doing.

**Inplay Global:** Okay.

**edwin:** Uh because you know a lot of a lot of these referrals are like hey you know I've got a brother and

**Inplay Global:** Oh,

**edwin:** he's like I'm like go get me 20 people and he's like he calls 20 people no one knows what inplay

**Inplay Global:** thanks.

**edwin:** is. They just download as a favor or a referral to get that that bonus or whatever whatever and then they get to that that that first thing it's just like give us your ID. And I'm telling you from my like what I'm getting in feedback people are like I'm not comfortable. I actually have two family members who won't do it.

### **00:27:54**

**edwin:** And I'm like, they're like, I had my identity stolen. It's like f\*\*\*\*\*\* retarded. Um,

**George Westbrook:** Are you here?

**Inplay Global:** you guys are going.

**edwin:** you

**Inplay Global:** So, so Edwin, real quick and and Novo team,

**edwin:** know,

**Inplay Global:** keep me honest here because I tested this last night. It's not there anymore. So, I actually registered my son last night without having to go through KYC. So, I'm not sure what where the out trade is on that.

**edwin:** I know the the persona

**Inplay Global:** I think I think we're still well I think that that because there's there's the test flight app that is obviously has a lot of other features but I actually went on a different device downloaded the trading challenge app and it said you know create an account. I created an account with my son's email and my son and that's it. It went right into the app.

**edwin:** Oh, really?

**Inplay Global:** It didn't require me to go to and then well no because you're on the test flight

**edwin:** Yeah. Then I'm using the wrong s\*\*\* cuz I'm

### **00:28:49**

**Inplay Global:** version of it and also if you log out and log back in it does

**edwin:** I'm

**Inplay Global:** change as well. So I think it's just there's a there's a lot of things that are being adjusted in parallel right now. But I did test last night with my son and it

**edwin:** okay.

**Inplay Global:** worked.

**edwin:** Okay. Well, I'll do it after the call and see what's up.

**Inplay Global:** Yeah.

**George Westbrook:** I think T0 are working on or have sorted out the 18 plus. So we spoke to T0 yesterday.

**Brett StClair:** That's it.

**George Westbrook:** They said it shouldn't be an issue removing the over 18 thing. Um, and obviously we do we only do the over 18 check for somebody who's going to be receiving payouts. And then the KYC flow, we've got the part of it is are you a US tax resident? Are you not? Um, and the over 18 stuff. If they if they are um over 18, then it's going to ask them do you want to participate in the challenge.

### **00:29:46**

**George Westbrook:** There we go. Hannah's getting it up.

**Inplay Global:** Right.

**Brett StClair:** So yeah,

**George Westbrook:** So yeah,

**Brett StClair:** it's

**George Westbrook:** this is what this is what if you go back to Hassan and then go to the page. That gets to

**Hasan Ahmed:** Um,

**Inplay Global:** But I haven't done I haven't done the QC verification yet.

**George Westbrook:** that.

**Inplay Global:** It's saying do it to enter the challenge. So I wish I could show you what I'm seeing right now, but um let me see if I can show it on the camera. So I This is my son's account. You can see it says get verified through KYC to end challenge. So that's what it's now showing on the app that you can download from the app store, not the test flight app. Did you know that Novo team that that's what it looks

**edwin:** Mhm.

**Inplay Global:** like

**Hasan Ahmed:** Um yeah. Yeah. So I actually updated the actual the KY flow and so that

**Inplay Global:** 100% starts with no cash prizes open verified to get cash prizes?

### **00:30:41**

**Hasan Ahmed:** um

**Inplay Global:** get KYC verified. Then it goes through tells you how the process works. Then it's through persona and then it starts the verification. That's exactly Yeah. All I had to do is put in an email.

**edwin:** All

**Inplay Global:** Yeah. Which is what we want, right? We want some spam and email. Yeah. That's all I had to put in. So it looks like it's working there for the for new downloads on the app store. Okay. Yeah. Amazing.

**edwin:** right. Well, we'll take a look and we'll we'll come back to you. I I clearly f\*\*\*\*\* that up.

**Inplay Global:** No, no,

**edwin:** So,

**Inplay Global:** it's because there's the te the problem the problem with the app store is that if you're accessing it through the test flight, you have to delete the test flight version and then go back to the app store, redownload the live version. It it's a little bit wonky because we're between two worlds right now. We're in the test flight world with has the trading capability and then the live version which doesn't have the trading capability.

### **00:31:45**

**edwin:** Okay. And in terms of the um the nuance of the app,

**George Westbrook:** 6

**edwin:** the the stuff that I've sent over and the demo I gave Brett and uh Maximillion yesterday, you know, obviously everyone's got too much on their plate. Um, you know, the one thing that's sticking out, I did a couple demos last night and um that strategy lab that I showed you Brett and Max yesterday is a a f\*\*\*\*\*\* home run. Like people are like, "Holy s\*\*\*." And and and frankly, we think that that one will,

**George Westbrook:** Oh

**edwin:** you know, people trade a game and, you know, maybe they'll spend an hour or two trading that game,

**George Westbrook:** no.

**edwin:** but we think the research pieces might get them even stickier during the week.

**Brett StClair:** Thank you.

**edwin:** You know, we we could see someone spending a few hours a week just building different strategies.

**George Westbrook:** Damn.

**edwin:** Um, Brett, what is your thought on like, you know, the way that I have the ad ads on on my version native into the

**George Westbrook:** Okay.

**edwin:** app embedded in versus the

### **00:32:48**

**George Westbrook:** Okay.

**edwin:** banners?

**Brett StClair:** Um, so firstly, I really like the demo that you showed us and we need to do a bit of thinking about how we're going to run the algorithms and build all that out. And I think it's worthwhile doing a requirement session and let's get that properly articulated otherwise I know we're going to miss stuff. Um and and then we can also draw from your designs. Um when it comes to the ad units, you you can start getting a sense of what the ad units look like. So, um,

**edwin:** They're big. They're really

**Brett StClair:** they're they're big, right? And and so it's about what we need to test is when it's side

**edwin:** big.

**Brett StClair:** on, maybe we can slip it in. when it's upright, I'm I'm not sure it's going to be able to, you know, um the the problem with the kind of volatility ad unit post is even on the version that we had,

**George Westbrook:** See you back.

**Brett StClair:** it's going to have to be a direct buy because it's so difficult to slot in a custom ad unit like that.

### **00:33:57**

**edwin:** Yeah.

**Brett StClair:** Um so,

**edwin:** So, let let me interrupt real quick just for a second.

**Brett StClair:** so yeah,

**edwin:** So,

**Brett StClair:** it might be easier to do a top or bottom ad unit on around

**edwin:** I I Yeah. I in the belly of the the context, it's very distracting and it's like it would piss me off. Um I it would actually turn me off.

**Brett StClair:** And we can change that.

**edwin:** Um yeah.

**Brett StClair:** That's super easy,

**edwin:** So, you know, I on last Friday,

**Brett StClair:** right?

**edwin:** one of the a lawyer from FIFA called me up. He just finished his time. He was doing commercial deals for FIFA and you know, so we we had a couple conversations and I'm going to engage him. He's actually coming in very inexpensive on the box,

**Brett StClair:** Nice.

**edwin:** but um you know he wants to represent us for commercial deals for brands

**Brett StClair:** Nice.

**edwin:** and um you know I'd almost would rather have no ad

**Brett StClair:** f\*\*\*.

**edwin:** um and wait for direct sales than like fighting those programmatic banners like maybe on the bottom where we do video only

### **00:35:01**

**Brett StClair:** I'm with you. Maybe float the programmatic ads where we can test and get volume and check the quality and then

**edwin:** something.

**Brett StClair:** if we feeling comfortable we want to make more cash out, we float more in. But like the ad unit say

**edwin:** It's It's just It's really ugly and it's really frustrating.

**Brett StClair:** horrible

**edwin:** I mean, just looking at him pissed me off, you know what I mean? I was like, "f\*\*\* this." You know? Um, but you I'd like to see what this dude can do over the next couple weeks. Um, you know, he said he's got a bunch of contacts. Um, he named them and uh, you know, it was it was interesting. So, I'm going to uh I got an another f\*\*\*\*\*\*

**George Westbrook:** Oh

**edwin:** contract to look at today of his.

**George Westbrook:** yeah.

**edwin:** Um, so hopefully, you know, I can get Vogler and Marlin to sign off on that today. if he they can then we can get moving. And you know, we still are tackling your contract. So, um, which we'll probably need a separate call, uh, to to go over that contract because there's a couple questions I

### **00:36:07**

**Brett StClair:** Yeah. Yeah.

**edwin:** have.

**Brett StClair:** I mean, I've tried to keep it super simple, right? It's just like terms and conditions and really what's in there is more deliverables

**edwin:** Yep.

**Brett StClair:** than anything.

**edwin:** Abs. Absolutely. Um, okay, cool. So, you know, I think from a structure standpoint, um, you know, we're in this like Frankensteinish app.

**George Westbrook:** Hey,

**edwin:** I mean, Hassan, you've done a really good job putting it together, okay? So, don't take my changes as something that's personal um at all.

**George Westbrook:** good.

**edwin:** You know, we're we're very encouraged by what you've done and George and Max, everybody. But, um in terms of what like a priority is for us, right? So, the first thing, you know, it's kind of that chicken egg b\*\*\*\*\*\*\* where it's like we got to get customers before anyone takes us serious with brands, but like we can't um, you know, get the customers, you know, without me spending more money on advertising and things like that. And then if we get them to the water and the water tastes like s\*\*\*, they're not going to drink it.

### **00:37:11**

**edwin:** So, you know, our value proposition to downloaders and people are engaged in the app, it's pretty important and it's got to look and feel seamless. And, you know,

**George Westbrook:** How you

**edwin:** when aside from like the strategy builder and things like that,

**George Westbrook:** want?

**edwin:** just the, you know, the the process of of when you download the app, what it looks like, where do I go, you know, the four pillars to me are always like, what did I just download? How does it work? what's the difference from the rest of the market if that's a market thing and then how do I benefit like what's what's in it for me type thing right and those are the four things I think we need to have like when someone opens this thing for the first time cuz you know I don't know about the

**George Westbrook:** What's

**edwin:** rest of you and I'll take feedback but like when you refer people to download the app and you know are you giving them like a half hour or an hour of what inplay is because we don't have time for that you The referrals have to be like really easy and be like, "Hey, download this app.

### **00:38:12**

**George Westbrook:** good?

**edwin:** It's awesome. You can create." Boom. That should be the description. And then the app in and of itself should give them that that journey that gives them the comfort of like, "Okay, this will be fun." And uh, you know, it's not threatening to me and I, you know, I I can use this. And then from there, we can have the like, you know, the strategy builders and the rest. But, you know, does anyone else have any thoughts on this?

**George Westbrook:** Is your main main concern that the walk through not being there at the moment?

**edwin:** No, I wouldn't say that.

**George Westbrook:** Then

**edwin:** I would say like um I'd have to first of all I I have to download the app like uh Troy did to come back to you with with realistic feedback. But the the ones that already have downloaded the app have just been like, you know, I don't know what to do here. It's is telling me to refer people and I don't even know what what I'm referring for cuz they haven't been downloaded on what this actually is.

### **00:39:07**

**edwin:** So our,

**George Westbrook:** Yeah.

**edwin:** you know, I think as a group on the inplay side, we were uh shortsighted in how we were thinking everyone would know at least a portion of what it was before they downloaded. And therefore, they were kind of like, you know, hey, this is trading. It's relatively simple. And what's simple to us might, you know, be much different to somebody else is my concern.

**Inplay Global:** I

**edwin:** Um because like let's say well let's say we put up like you know 500k over

**Inplay Global:** think

**edwin:** the next two weeks to advertise and and to get people here and let's say you know that gets us 50,000 people who go to

**Inplay Global:** it's

**edwin:** download like what are we going to lose because they don't know like they may download but that's it. You know what I mean? just it to me it needs to be much more aligned with with what I've proposed than what what we have now.

**George Westbrook:** It in terms of what what aspects like the homepage, the the other pages,

**edwin:** Yes. So when you open the app, you know,

### **00:40:10**

**George Westbrook:** the

**edwin:** I think number one, you need to be like, you know, you need a user needs to be able to like, okay, I'm trading. What am I trading? like it's people don't know what a sports security is and and and still cumbersome for people to digest trade sports as stocks cuz they're like what does that mean? I mean, the words are simple and we've simplified it for years trying to to make it so the fatties out there can be like, "Okay, I get this." But, um, you know, I still am getting, at least the feedback I'm getting, okay? Like, you know, the feedback I'm getting from people who download are still like, I don't know what to do. And I'm like, okay. And maybe that's just society today. I I mean, you know, or maybe it's my my small sample that's, you know, uh deranged or something. Um, you know, Jared, how has it been going for you for for you pushing

**Jared Sapirman:** No, no, you're right. You're 100% right.

**edwin:** it?

**Jared Sapirman:** Everything that you showed me on the pre the app that you've created makes it make a lot more sense.

### **00:41:14**

**Jared Sapirman:** So, I just downloaded the app on my brother's phone and you have to create an account before you can do anything. And

**Inplay Global:** Yeah. Yeah,

**Jared Sapirman:** then

**Inplay Global:** that's still just but just an email. There's no ID creation or anything like that.

**Jared Sapirman:** is there a way we can circumvent that? So you can go through what the the Inplay app does,

**edwin:** The app

**Jared Sapirman:** what the app does, and then have it.

**edwin:** is

**Jared Sapirman:** So you don't right away it's like, okay, you download the app, you open the app, boom, create an account before anything. You don't even know what you're down, what you're doing, what you're creating an account for.

**George Westbrook:** Got

**Jared Sapirman:** Is there a way that we can use that process that Edwin showed me where it show says trade sports of stocks. This is not a prediction market. explaining what it is go through that walk through first,

**George Westbrook:** the walk But the walk through is the key

**Jared Sapirman:** then have the commiss to create an account because that would

### **00:42:03**

**George Westbrook:** blocker.

**edwin:** I'm sorry,

**George Westbrook:** It I don't know if my mic's working.

**Jared Sapirman:** be

**edwin:** George.

**George Westbrook:** So Jared, the walk through is that is that what you're saying at the start?

**edwin:** So,

**George Westbrook:** Okay.

**edwin:** I also I also like this.

**Jared Sapirman:** Yes.

**George Westbrook:** Yeah.

**edwin:** So the other thing again and again I'm not drinking my own Kool-Aid but when I designed the homepage okay the homepage gives information that a user may want that they don't have to sign up for so like the ticker you know and the ticker you know it just has prices. Okay, you'll notice on our homepage, we don't show any team scores. We don't have like a scrolling ticker of team scores on there. So, it it's meant to entice people to say, "Oh, interesting." And then they have the ability to select like which which thing they want to compete

**George Westbrook:** So with the with the team scores is we don't we don't have that data in P

**edwin:** in.

**George Westbrook:** 0 at the moment. So what we what the way the app's set up is if there's no

### **00:43:05**

**edwin:** We don't Right.

**George Westbrook:** data

**edwin:** We don't want teams. I'm saying, Pardon me.

**George Westbrook:** so did I say team scores I meant team prices.

**edwin:** Yeah. Yeah. Okay. Yeah. Because there are no team prices yet,

**George Westbrook:** Yeah. Yeah.

**edwin:** right?

**George Westbrook:** So it's is so what with the way it is is we don't necessarily want to show blank data.

**edwin:** Yeah. So, I wouldn't show blank data.

**George Westbrook:** So if like say with the tickers it it the tickers would show only come on when

**edwin:** I

**George Westbrook:** that price change is happening just so from a user's perspective in the same way they're like okay there's a ticker uh they're showing

**edwin:** Yeah, I I follow you. Well,

**George Westbrook:** 0%.

**edwin:** here's what I would put in lie of the the actual price. I would put up, you know, the IPO price and a little note that says IPO, right?

**George Westbrook:** Yeah.

**edwin:** And so that way when a ticker is going by, you're looking up and say, oh, you know, University of Akran's like 58 bucks a share and you know, University of Texas El Paso is $62.33 a share.

### **00:43:50**

**George Westbrook:** Perfect.

**edwin:** So that scrolling ticker and on the version I I have an update but I don't want I don't want to vary it George and team you know that's not the goal. The goal is to like, you know, if we're if we're moving towards getting users, I my gut tells me this user journey has to be simplified and we actually have to give them like a come on to like, you know, they get there, they see the ticker moving, oh, there's excitement and the prices and whatever are up, whether it be IPO or or live trading, you know, it it doesn't give them anything of benefit other than within the inplay world. So those prices don't mean anything on Kelshi or prediction markets um or betting um maybe the the change in prices they could figure out but like you know it it would be in in my opinion okay I think we need a clean like uh entry and then the homepage you know where they can sign up has Something. that's visually stim stimulating other than just a wall cuz like when I went to sign up this morning, you know, I tried to sign up with a different email and my f\*\*\*\*\*\* ID wasn't being taken.

### **00:45:11**

**edwin:** It was really annoying. It took me about 20 minutes before I quit. And you know, I took the front and the back of the ID. It still didn't take. I did it about three times and I said, "f\*\*\* it." And then I just went back and logged in on my own and then had the update. But I, you know, getting hit with a wall, I think, is is is tough. That I mean, my guess is we're going to lose 50% or more just by that wall.

**Inplay Global:** What's this?

**edwin:** Whether it's an email, whether it's KYC, whatever. If that's the first thing you see, I'm I'm I mean, people are telling me they're not doing it.

**Brett StClair:** So, this is all really good news, by the way, and the feedback's fantastic. And so what you're going to find is as we go closer and closer and more and more users come on board, this feedback mechanism is so crucial to constantly update the app. So we've got the first version up. What I want to suggest is that we actually put in a session like maybe twice a week where we can go uh a bit like we do with the user requirements.

### **00:46:14**

**George Westbrook:** You can

**Brett StClair:** What are those changes that we need to get in? What are those new changes?

**George Westbrook:** follow

**Brett StClair:** Because they're going to come faster and faster. By the way, you're going to speak to more people. people going to go f\*\*\*\*\*\* that sucks. Now I want to see that. No, I'd like to try this instead. Oh, I've got a better idea. This is blocking this. It's only going to come faster. And so this world is fast, right? Usually in the past you'd have to wait two weeks, a month to get it scheduled in.

**George Westbrook:** Stop.

**Brett StClair:** But what I'm going to suggest is maybe we do a standup in the two days that we're not doing a standup where we do um new ideas, new concepts. We do like a requirement session.

**George Westbrook:** Please

**Brett StClair:** We go through it. We grab your ideas in the design kind of prototype that you've built,

**George Westbrook:** go.

**Brett StClair:** Edwin. We take that, we put it all together, we can push it through our engines, get it through our spec engines, and then depending on whether it's an OTAA push, we can get that out fairly quickly.

### **00:47:04**

**Brett StClair:** If it's not an OTAA push and we got to push to store,

**George Westbrook:** Excuse

**Brett StClair:** then we we'll be able to tell you when we're going to push to store and how we're going to load that backlog and get out the door. But this is good, right? It's going to keep coming. And when you're running product development,

**George Westbrook:** me.

**Brett StClair:** half of it is you're always changing. You're always changing. You're trying to tweak. You're trying to refine. You're trying to reshape a button. Push it slightly to the left. No one's ever going to get it perfect on first hit. You're going to be changing the whole time.

**edwin:** No,

**Brett StClair:** So, this is really, really good. I don't want you guys to get depressed about it. If that needs to change,

**edwin:** I I don't I don't think anyone's depressed.

**Brett StClair:** we change. Let's go.

**edwin:** I mean,

**Brett StClair:** Let's

**edwin:** I think, you know, I'm I'm not depressed.

**Brett StClair:** go.

### **00:47:39**

**edwin:** I'm just like, god f\*\*\*\*\*\* damn, I need some breaks in my life.

**Brett StClair:** And we pivot, right?

**George Westbrook:** Stop.

**Brett StClair:** And we pivot. And we pivot. And we keep trying.

**edwin:** Um,

**Brett StClair:** and we want to get the data and we want to make sure it's there because remember in theory code is cheap.

**George Westbrook:** She's

**Brett StClair:** It's it's getting the requirement articulate requirement getting into a spec and then pushing it through the system. There's only a couple of caveats in Some of the stuff we've just got to also get out the door. And so what we got to do is find a 10% slot where we go these are the kind of new changes that we can quickly squeeze in. Why are we pushing all the other stuff out the door? And and then we prioritize, right? This is important like to take away that barrier. I hear you.

**edwin:** Yeah.

**Brett StClair:** I'm I'm aching at the thought of someone going through that. Right. f\*\*\*. I get that.

### **00:48:22**

**George Westbrook:** I didn't know that.

**Brett StClair:** I know that feeling. Right.

**edwin:** Right.

**Brett StClair:** That's obviously a priority.

**edwin:** Because you know Cody,

**Brett StClair:** What where do we do a shuffle?

**edwin:** on our deal with Sport Radar,

**George Westbrook:** Is

**edwin:** do we have historical data playbyplay?

**Inplay Global:** Yes, it's all included in that real time

**edwin:** Cool.

**George Westbrook:** it?

**edwin:** So, um,

**Inplay Global:** data.

**edwin:** one thing I'd like to do, um, for my app, okay, for as I'm developing my version and improving it, um, I need access to that, uh, sport radar historical data, and I want to go back a number of years and basically run playbyplay on all the games and then really enhance that strategy lab. Okay? because we have to essentially assign a synthetic price um to the the to the team share. So I basically we'll run like a remodel of let's say the last 5 years of you know NCAA and NFL football and then we'll take play by play. Um we'll run them just like we would have had we IPOed them 5 years ago and then we we we see the price action throughout and then we put that stigma to it.

### **00:49:29**

**edwin:** I mean, what I told Brett yesterday, George, was, you know, it's it's very interesting, okay? Like, if if if we have this like strategy development tool, okay, embedded into the app, they may there, well, there will be users that that use that for other purposes other than inplay. in particular, you know, if let's say hypothetically you're going to trade Khi, okay, and you want to know that any time that there's a play that happens on the field greater than 20 yards, um what would historically a price have done after that play and we can recreate that, okay, with an inplay pricing model. And then you could say, okay, um, you know, every time there's a a play over 20 yards, should I buy that team or should I sell it or how how should I approach it? And then what is that actual move worth in terms of risk? Because like if I if I'm trading Kelshi, say, and um, you know, they the team makes a great catch and it's 25 plus yards goes in the other team's territory and you can put all this criteria in the model that I have, right?

### **00:50:42**

**edwin:** And then you say, "Okay, that happens. If I buy here, what happens next over all the teams, all the games to pricing?" And it says,

**George Westbrook:** Yeah.

**edwin:** "Okay, well, generally the price goes up 28 cents." Okay. Well, if that's the case, you can you can Um, basically you can price the 28 cent move on in play into a probability move

**George Westbrook:** She's

**edwin:** on Kelshi. So then all of a sudden you say every time that they make any any any team or any um company on Cal or strike that any team on Kelshi that completes a play 20 plus yards in the opposing team's uh uh field um I'm going to make money because I'm going to buy every single time and every single time over all these litmus tests and all these back tests it shows that I it's a winning strategy no matter what. Okay. And the way that this works or like is very similar to how I trade, you know, I I built something similar to this which which would um allow me to see orders. Okay? So like um you not I don't want to go down a rabbit hole,

### **00:51:48**

**George Westbrook:** Okay.

**edwin:** but bear with me a second. But let's say I want to know what the the stock market does from 8:30 a.m. Central to 8:33 a.m. Central. And in particular, when a certain number of criteria happen, the the market opens lower than the pre previous close, you have more orders on the sell side at the top of book than the buy side. and um you know I'm going to use those two say inputs and then I'm going to say I'm going to sell the best bid price there and then my software would would run through enormous amounts of test and it would give me like the next number of like ticks and let's say I ran it for like a 20 tick you know outcome and then I could basically test and say yeah if I do this 72% of the time I win 28% of the time I lose my worst draw down is three grand. Um, my highest win is, you know, 4,200, but net net, if I had done this over the last year, I'm going to make $400,000. And that's how I build

### **00:53:00**

**George Westbrook:** I I think like like the strategy thing fantastic idea with along with

**edwin:** strategies.

**George Westbrook:** the research stuff that that Cody Cody mentioned as well then using the AI stuff unfortunately it's it is a it is a heavy lift like I think it's it's important to

**Inplay Global:** Nothing.

**George Westbrook:** make a distinction between an app a prototype and then a clickable HTML

**edwin:** No,

**George Westbrook:** document.

**edwin:** no, of of course.

**George Westbrook:** Um,

**edwin:** Of of course, you

**George Westbrook:** so it's cuz I I think because with the with like the Claude stuff,

**edwin:** know.

**George Westbrook:** I think where it's really helpful for us is conceptualizing some of the ideas you've got. So like say click um we see the back testing blah blah blah.

**Brett StClair:** That's okay.

**George Westbrook:** But in terms of actually getting that to work with real data, managing websocket connections for up to a million users, making sure that the data is streamed within 20 milliseconds via a messaging bus, scaling up all the VMs and stuff like that, it's that I know you hate this uh analogy, but the iceberg.

### **00:53:59**

**George Westbrook:** That's like the the tip tip tip of the iceberg. Um I think for for us, like I said, it's really helpful to understand those ideas, but it's we'll need a session to understand. Okay. Um I'm already thinking in my head how we'd get that data, how we'd work it out, and I can I can see how we would do it because like you said, the sports radar data is there. We just need to we just need to think about how we're how we're going to do it. I think concepts in terms of the HTML slideshow things that you're doing are really helpful and then in terms of equations and then requirements once we've got that I think after launch that should be a priority. Um, but I think it's like for it's like we said before, it's the the ads, the trading, the market maker. Market maker nearly there, the taker nearly there, the trading is is there. Um, and ads although not where we probably want them in terms of a visual as aspect,

**Brett StClair:** Yeah.

### **00:54:59**

**George Westbrook:** um, the the piping is there. Um, and obviously the IPO linking into all of that as well is I mean because we've got the the simplified version I say all that confidence is there but I suppose it's what is it is it this time is it this time next week the IPO opens the 20 no sorry 22nd.

**edwin:** next Saturday. Yeah. No, no. I I understand.

**George Westbrook:** Yeah.

**edwin:** I I know the the the amount of work that's on the plate, and I I I get that. You know, when you look at something pretty, you know, there sausage has to be made behind the scenes.

**George Westbrook:** Excuse

**edwin:** I I get all that. Um but I don't know if you know this, but Brett has 25 mini agents over there hustling their little their ass off,

**George Westbrook:** me.

**edwin:** right?

**Brett StClair:** I call them Matthew 1, Matthew 2, Matthew 3\. I got late. I got bored of that.

**edwin:** For what the for the record, I hate the name Matthew.

**Brett StClair:** Hey.

**edwin:** I've never met a Matthew that hasn't been a complete f\*\*\* in my life.

### **00:55:55**

**Brett StClair:** Well, he does

**edwin:** Yeah. Well, I mean,

**Brett StClair:** f\*\*\*.

**Max Kingaby:** Wait till you realize Brett's son's called Matthew.

**edwin:** oh, sorry. Yeah. Well, I mean, we could call him Matt then or M dog or something. Every Matthew I've ever experienced that works,

**Brett StClair:** I think he calls himself big dog.

**edwin:** too. The other name that's s\*\*\* is Declan. No one ever meets a good Declan.

**George Westbrook:** Best name's George, I'd say. Worst name's Max.

**edwin:** Fair. Um, all right. Well, on on the app stuff, you know, we're going to we're going to just keep, you know, iterating on it. But what I would would like to do um in in anticipation of um you know,

**George Westbrook:** H

**edwin:** we still like the the IPO launch, we're going to be ready for that. Okay. I know we'll figure out a way. Um we don't launch trading until the 29th and it's college. Okay. And that's still like pre-Labor Day weekend. In my experience, Cody, talk to me if I'm wrong at your time at Fort Radar.

### **00:56:56**

**edwin:** That still doesn't mean that everyone's in through the full swing of betting yet. It's generally after that first NFL weekend is when it really starts, which would be around September 12th. Is that right,

**Inplay Global:** 100 100% right. And I was talking to Troy yesterday.

**edwin:** Cody?

**Inplay Global:** No, no media outlet covers college football. So like us getting any sort of coverage or like big blowout news about us or anything. Uh it's never going to happen for running a college football training simulation. it will happen NFL. So realistically everyone should I mean yes we need to get things up and running

**edwin:** No.

**Inplay Global:** for the people who are trading college football but really DDay is September 9th

**edwin:** Cool. Um, so yeah. All right. Excellent. Um, so we do in what's today the 12th.

**Inplay Global:** 12

**edwin:** So we think we have a month to actually do part of the app and once you get this taker and

**George Westbrook:** Go.

**edwin:** maker humming and we have the rest um what I'd like to do to help is I'd like to get access to that data.

### **00:58:04**

**Inplay Global:** Yeah.

**edwin:** Okay. So like I want the data put somewhere that I can point to that I could start working with because I want to assign an IPO price to each team. I want to sign a price to each team and then I want to start building the strategy tool around that and I want to like you know basically it's a language model like our own little mini

**Inplay Global:** Heat.

**edwin:** one where you basically you know you just type in what you want hey anytime the home teams this

**Brett StClair:** We've got the H.

**edwin:** orders

**Brett StClair:** We can forward it to you, right? That shouldn't be a problem.

**edwin:** There.

**Brett StClair:** Just send through the APIs and it should be able to consume.

**George Westbrook:** Uh it depends if it's market data, market maker data or sports radar data.

**Brett StClair:** No, no, I'm radar, right?

**edwin:** Yeah,

**Brett StClair:** Yeah.

**edwin:** sports radar data.

**George Westbrook:** Yeah.

**edwin:** What I need from sports radar is a couple things. I need the news. I want the news because I want to I want to put this in in a couple of different spots so I can actually see it.

### **00:59:03**

**edwin:** Um, and then I want to visualize I need the uh the team rosters. Um, does Cody does Sport Radar offer like a um starting lineup?

**Inplay Global:** Dev

**edwin:** Yep. Chart.

**Inplay Global:** charts.

**edwin:** Okay. I'll I'll put this all together and send an email what I need from Sport Radar and then um yeah, we want to we want to work with some of historical data that we can start pulling and finding out like what we're going to do with that like how we're how I'm going to actually how here how I would use it to start researching trade ideas around that. And um you know when I showed the FIFA lawyer that you know his he's tight with DraftKings you know basically he's like we need to sell your company to DraftKings because they actually need this desperately right now.

**Brett StClair:** Guys, I need to drop.

**edwin:** like see

**Brett StClair:** Um, I've got a hard stop. Um,

**edwin:** you.

**Inplay Global:** I

**Brett StClair:** everyone good? George, I need you in this hard stop as

**Inplay Global:** believe

**George Westbrook:** Yeah.

**edwin:** All right. Yeah. Why don't we we'll just continue here.

**Brett StClair:** well.

**edwin:** I'll give you a list of items I want from Sport Radar. I just might need help with how to pull them.

**Inplay Global:** uh Novo team,

**edwin:** Okay.

**Inplay Global:** can we do another sink tomorrow um at 2:30 uh London time just to kind of coordinate the final logistics for the dry run in the evening or sometime in the late morning our time.

**George Westbrook:** Perfect.

**Brett StClair:** Yeah, I'll drop something in the

**Inplay Global:** Okay.

**edwin:** Awesome.

**Inplay Global:** Yeah.

**Brett StClair:** diaries.

**Inplay Global:** Uh just not two uh London time, but 2:30 or anytime after probably would work.

**Brett StClair:** Perfect.

**Inplay Global:** All right.

**edwin:** Thank you so much all. We will talk soon.

**Brett StClair:** Thanks.

**Inplay Global:** All right.

**George Westbrook:** Let's f\*\*\*\*\*\*

**edwin:** Great work.

**Inplay Global:** Thank you.

**George Westbrook:** go.

**edwin:** Thank you, Georgie Boy.

**Inplay Global:** problem.

**edwin:** Butter.

**Inplay Global:** Yeah.

### **Transcription ended after 01:00:56**

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*