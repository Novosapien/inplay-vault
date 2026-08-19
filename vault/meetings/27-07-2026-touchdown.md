---
date: 2026-07-27
type: standup
description: "Monday touchdown, 27 July 2026: AdMob verified and serving, the Sport Radar probability-polling problem, end-to-end trading demo, ticker naming, and the analyst prices page."
source: "Gemini meeting notes, Inplay - App - Touchdown"
scope:
  - "[[advertising/advertising]]"
  - "[[market-maker/market-maker]]"
  - "[[trading/trading]]"
  - "[[integrations]]"
  - "[[information-layer/sub-components/team-page/team-page]]"
  - "[[compliance/compliance]]"
status: extracted
extracted-to:
  - "[[advertising/advertising]]"
  - "[[market-maker/decisions]]"
  - "[[market-maker/parameters]]"
  - "[[market-maker/open-questions]]"
  - "[[trading/trading]]"
  - "[[integrations]]"
  - "[[frontend-deployment]]"
  - "[[compliance/compliance]]"
---

## Post-Call Analysis

~36-minute Monday touchdown, three weeks out. Present: Edwin, Cody, Troy, Kevin, Gary, Jared (InPlay) and Brett, George, Max, Hasan (Novosapien). Edwin opened by naming the three things that must land: the ad server, the market maker, and the rest of the app "ready for prime time".

The substance clustered in four places. **AdMob went live** that morning, first native unit created, and Brett explained the resubmission tax that comes with every future SSP. **Sport Radar's probability gap** surfaced properly for the first time: the fast push feed carries the play but not the probability change it caused, so probability has to be polled separately, and at the cadence the market maker wants that is 8 to 10 million calls a month. That opened the plan-B conversation about training an in-house model on NFLverse, which George judged impossible before launch and Edwin took away to attempt in rudimentary form. **Hasan demoed end-to-end trading** into tZERO with positions, executions and history. And Edwin asked for an **analyst prices page**, which George successfully argued down the priority list on the grounds that ads, trading and the market maker are the only non-negotiables.

One legal item: team companies cannot carry real franchise names, and Troy's acronym proposal (NYJ, Kalshi-style) was accepted.

Signups were reported at 101, against a stated need of 10,000.

| Finding | Destination | Action |
|---------|-------------|--------|
| AdMob verified, first native unit, resubmission-per-SSP constraint | [[advertising/advertising]] | Update written |
| Probability not in the play-by-play payload; poll cadence vs quota | [[market-maker/parameters]], [[integrations]] | Parameter row + integrations section |
| Own probability model on NFLverse as plan B; proprietary IP argument | [[market-maker/parameters]], [[integrations]] | Recorded, not a v1 build item |
| Trading end to end into tZERO; test-user gating | [[trading/trading]] | Update written |
| Ticker naming must not read as the real franchise; acronym convention | [[trading/trading]], [[compliance/compliance]] | Update + constraint C6 |
| Analyst prices page: weekly Wednesday submissions, needs a portal not email | [[information-layer/sub-components/team-page/team-page]] | Changelog entry, deprioritised |
| Priorities named: ads, trading, market maker are the non-negotiables | [[delivery/delivery]] | Folded into the delivery note |
| Signups ~101, mostly friends and family; fundraising context | — | No action |

---

Jul 27, 2026

## **Inplay \- App \- Touchdown \- Transcript**

### **00:00:04**

**George Westbrook:** Makes you look like you've got your head done in like the 80s.

**Max Kingaby:** I need some water to pat it down.

**George Westbrook:** Yeah.

**Max Kingaby:** It looks atrocious. Hello.

**George Westbrook:** Hello.

**Max Kingaby:** Yo.

**Cody Haugen:** Hello.

**George Westbrook:** How are we all doing?

**Cody Haugen:** Doing well. How you

**Kevin Murray:** Good. Good,

**George Westbrook:** Good, good, good.

**Cody Haugen:** doing?

**George Westbrook:** Everyone have a good

**Kevin Murray:** mate.

**George Westbrook:** weekend.

**Cody Haugen:** Yeah, not too bad.

**Gary Anderson:** You took my daughter to Disney. So, no, did not.

**George Westbrook:** Expensive weekend then.

**Gary Anderson:** Oh, yeah. It's budgeting.

**George Westbrook:** It makes me laugh. You go into Well, but we've only got the the Paris one in in Europe. Um, but you go in there, it's like, yeah, £60 for a like Woody out of Toy Story doll. It's like it's and then and then then you're going to go in and it's like, "Oh yeah, I want I want that one. I want that one. I want that one." Next thing you know,

### **00:01:11**

**George Westbrook:** 200 quid done on bloody cuddly toys.

**Gary Anderson:** Yeah, that are useless.

**Max Kingaby:** No,

**Gary Anderson:** Yeah.

**Max Kingaby:** George. I stopped wanting cuddling toys at about 10, but that's what you do at 25\. space issue.

**Brett StClair:** I'm wondering why he's still going there. I don't know why he went last week

**George Westbrook:** That's just my favorite place to go.

**Brett StClair:** either.

**Cody Haugen:** Yes.

**George Westbrook:** Spend Spend all the money I earn on cuddly toys.

**Brett StClair:** Now I'm worried. Hello everybody.

**Cody Haugen:** Good

**Kevin Murray:** How's it

**Cody Haugen:** morning.

**Brett StClair:** Yeah,

**Kevin Murray:** going?

**Brett StClair:** good. Um, the big question is, does George and his son understand Mark Makers yet?

**George Westbrook:** 50/50 code has been written. The understanding is enough that it's uh there's there's forward motion.

**Brett StClair:** Who's that? I missed the invite. There we go. Um, sure. Okay. Shall we get into it? Oh, no more. Is that everybody? Yes.

**Kevin Murray:** Nope.

**Brett StClair:** Hello everybody.

### **00:02:43**

**Edwin Johnson:** Hello.

**Cody Haugen:** Hello.

**Edwin Johnson:** Fine. Morning to you, sir.

**Brett StClair:** Good morning.

**Edwin Johnson:** Well, it's afternoon by you.

**Brett StClair:** It's uh 2:30. It's not too bad.

**Edwin Johnson:** investigate. All

**Brett StClair:** Um,

**Edwin Johnson:** right.

**Brett StClair:** everyone have a good weekend.

**Edwin Johnson:** Uh, I would say mine kind of sucked if I'm being honest.

**Brett StClair:** Was it a a weekend of doing

**Edwin Johnson:** Um, no.

**Brett StClair:** calculations?

**Edwin Johnson:** It's actually one I took a couple days off of work and um, you know, for whatever it is when you're in these startups when you're not working, you're thinking about working and um,

**Brett StClair:** Don't get away from it, right?

**Edwin Johnson:** never gets away from it. No, I just for whatever reason, I don't know what aligned in my life,

**Brett StClair:** Yeah.

**Edwin Johnson:** but this past week, I don't know, I spent like $50,000. I have no idea what it all went for. Yeah, it's just like, yeah, at some point we got to start figuring out how to make money instead of giving it out, you know, be great.

### **00:03:50**

**Brett StClair:** agreed. Well,

**Edwin Johnson:** So,

**Brett StClair:** you've got about three weeks.

**Edwin Johnson:** 3 weeks. Yeah, just about

**Brett StClair:** And I I like saying that because I like to see how many beads of sweat suddenly appear on George's

**Edwin Johnson:** just

**Brett StClair:** forehead.

**Edwin Johnson:** I'm more worried about the uh you know below the neckline sweat for George. That's things get serious.

**George Westbrook:** Got a fan on. But we don't sweat.

**Edwin Johnson:** I got you. I got you. Um Awesome. All right. So, listen. We've got, like you said, three weeks, tons to do. Is Troy on this call?

**Brett StClair:** Yeah,

**Edwin Johnson:** I don't see you.

**Kevin Murray:** Yep.

**Troy McDonald Kane:** I'm just off camera right now.

**Cody Haugen:** Mhm.

**Edwin Johnson:** Oh, okay.

**Brett StClair:** there's

**Edwin Johnson:** Cool. All right. Um, so listen, what do we have to do? We've got to get the ad server up. We've got to get the market maker done. Uh,

### **00:04:44**

**Brett StClair:** So

**Edwin Johnson:** we've got to get the rest of this app ready for prime time. So, I'll let you guys start. You want to start with the ad server? Go for

**Brett StClair:** yeah,

**Edwin Johnson:** it.

**Brett StClair:** so we've got ADM Mob up and running, verified. We got the verifications in this morning.

**Edwin Johnson:** Oh, congratulations.

**Brett StClair:** Um,

**Edwin Johnson:** That's

**Brett StClair:** so that's there. We've created the first ad unit, a dynamic ad.

**Edwin Johnson:** great.

**Brett StClair:** Um, oh, sorry, sorry, a native ad. So, we're going to just start each one, test it, make sure it's fine, that we've understood how it's working. Um, and uh, so we're just going through the config and the APKs. We probably to get it actually appearing in the app, we're going to have to tie it alongside a app release store cuz we've got to actually embed a bunch of serving code that's out of our control and resubmit with a bunch of policy kind of updates as well because as soon as you serving ads and there's a whole lot of rule changes.

### **00:05:43**

**Brett StClair:** Um so that's for the Apple app. Um the Android store is submitted and everything. We're waiting to hear back from them. As soon as uh the Android store is authorized, then we'll grab the Android store address and we'll set up the ad serving component on ADM Mob for Android and then we'll do the same process. We'll probably have to do a resubmission. So in that first couple of stages a bit kind of chicken and egg and then you kind of have to resubmit again because you need to get all the ad components up and running in that particular

**Edwin Johnson:** When when you resubmit,

**Brett StClair:** thing.

**Edwin Johnson:** is it an ownorous process to get back in?

**Brett StClair:** Anything between 24 and 48 hours.

**Edwin Johnson:** Oh, that's not

**Brett StClair:** M.

**Edwin Johnson:** bad.

**George Westbrook:** or or like what we did before. So it it it doesn't take it off the app store obviously.

**Brett StClair:** Yeah.

**George Westbrook:** Um it's just kind of like resubmitting

**Brett StClair:** And you wait and then it just swaps it out.

### **00:06:36**

**George Westbrook:** it.

**Brett StClair:** So it's still on the store. This is the next version. And we can't get away all the ads components. Every time we plug in a new SSP, um, we have to get it up and running. Uh, but you can only apply for the SSPs once you get your app store. um URL. So that's why the decision was ADM Mob. It's the quickest. It took 48 hours. Um the rest can take weeks and we have to do written submissions, all that kind of stuff. So I just figured get ADM Mob in. We know it's working. Run some ads into it, get some tests going. Um and then we start all the others because then we'll add the URLs and we can start just managing the administration process. as they come in, we'll resubmit again,

**Edwin Johnson:** That's

**Brett StClair:** get it out the door until we've got the right number of SSPs, you know, embedded into the actual apps. Um, so that's good.

### **00:07:34**

**Brett StClair:** So,

**Edwin Johnson:** okay.

**Brett StClair:** this week we'll be able to see ads starting to be served in it.

**Edwin Johnson:** Well,

**Brett StClair:** From there,

**Edwin Johnson:** that's it.

**Brett StClair:** it's all optimization and getting the networks properly engaged and getting the right formats running and all that kind of jazz.

**Edwin Johnson:** for our purposes though for us to try to close um you know if so basically I think I said this on the last call I'm trying to raise 40 million in August which will change the dynamic for for all of us quite a bit it'll take a lot of pressure off of me and then you know we could add the people we need or the services we need we can get a little bit more robust and at least our footing. Um and then the the the next wave would be like around March 30 and I would be at a much better valuation. So um you know the idea here is the more things that

**Brett StClair:** Nice.

**Edwin Johnson:** are actually done the more it's for whatever reason like you know I've been at this a long time.

### **00:08:31**

**Edwin Johnson:** I've been talking to people. I'm like oh yeah we're going to get an app. It's like no one believes you're going to have an app until you f\*\*\*\*\*\* see the app. I I I don't understand human beings.

**Brett StClair:** Few

**Edwin Johnson:** Like there's zero vision. And I'm I'm not a visionist, believe me. But like if someone's like, "Hey, I'm going to cut your lawn." I don't have to see him cut it for me to believe it. You know what I mean?

**Brett StClair:** lefties.

**Edwin Johnson:** It's it's a it's just it's it's a weird thing,

**Brett StClair:** I'm just

**Edwin Johnson:** you know, and you know, like whatever. I mean, we don't have great connections into like institutional capital. We have connections, but it's generally b\*\*\*\*\*\*\*, you know, like we talked to, you know, Goldman Sachs, but like all those guys are like you once it's built, you come to us, then we get and you don't need any money, then we'll give you the money, right? Then it's easier for them to raise.

### **00:09:19**

**Brett StClair:** Mad.

**Edwin Johnson:** Yeah.

**Brett StClair:** Mad.

**Edwin Johnson:** Um and I I did hear from uh Rafi Ashkenazi over the weekend. Uh so that was a positive. Um he thought we No,

**Brett StClair:** Who's that? Pong guy. Yeah.

**Edwin Johnson:** that's the um executive chairman of Hard Rock.

**Brett StClair:** Oh, hard rock. Okay.

**Edwin Johnson:** Yeah. Yeah. But there you're right because they're all connected to that that one dude.

**Brett StClair:** Yeah.

**Edwin Johnson:** And so um so that was a positive. and his his you know his note was congratulations on the app and you know I'll check in with my team on the the review cuz we gave him a bomb to look

**Brett StClair:** All

**Edwin Johnson:** at as you know uh that stuff we gave him last Monday was pretty pretty intense and then he said he thought we were pretty aggressive uh with our with our model which you know I always take aggressive as a compliment so that that was

**Brett StClair:** right.

**Edwin Johnson:** positive All right, moving on from ADM Mob.

### **00:10:16**

**Edwin Johnson:** What's next? What? How? George, I sent you those things last end of last week. Talk to

**George Westbrook:** Yeah. So progress is being made, code is being written.

**Edwin Johnson:** me.

**George Westbrook:** It's different to the the other way that we write a code. So for like front end, it's we can speak to the machine, we let it just do what it needs to do and then we validate after. With this, it's different. We need to check every single thing like this you could argue is one of the key parts. If we don't know how it works top to bottom um for the thing that is making the market then yeah this this whole thing doesn't really work. Um so it's a slower process than everything else and obviously for us it's going from zero to 100 in the space of a few weeks but we're getting there.

**Edwin Johnson:** Sure.

**George Westbrook:** Um so the understanding the the understanding is nearly there. Um now it's trying to work out the technical aspects.

### **00:11:11**

**George Westbrook:** So little things I think one of the one of the I wouldn't say it's a bump but is the so with the data feeds from sports radar the ones that get pushed to us the the quick ones let's call it um they don't include the probability change of the game. So if it will say five yards gained by the Chiefs, but it won't say what probability increase that is. So what we have to do is keep on polling the the end points to get back the probability. Um so one issue is basically it means that there would be around 8 to 10 million requests per month for that specific endpoint which is which is a lot. Um, and it's just going to chew through the quotota. So, I think there's another one that we've seen. It's a sports, it's still sports radar, but that should cut that to like 800,000 to a million. Um, and then should increase the the speed a bit. But the issue is we we need to balance how much do we call it?

### **00:12:17**

**George Westbrook:** Um, how quickly because obviously we don't want to leave it 5 10 seconds, but then again, we don't want to be calling it every 200 milliseconds. Um, so it would be balancing it so that say in game we're making a putting it pushing out new quotes every 200 milliseconds but when a game is on we're calling that probability endpoint every two seconds. So we're not we're not just wasting we're wasting sports radar things.

**Edwin Johnson:** Yeah.

**George Westbrook:** So if we do every two seconds about 8 to 10 million and then obviously if we were doing it every 200 milliseconds it's going to times that by 10 well 20 10 10 sorry so it' be 80

**Edwin Johnson:** Okay. Um,

**George Westbrook:** million

**Edwin Johnson:** Cody, is that right? We don't get the probability with that game

**Cody Haugen:** That is correct. Yeah,

**Edwin Johnson:** cast.

**Cody Haugen:** the gamecast is the hosted solution giving you the visualization of the data in the fastest way possible. The probab the probabilities is a separate endpoint that as like George said is a

### **00:13:15**

**Edwin Johnson:** Okay.

**Cody Haugen:** separate endpoint that's called in correlation with the data

**Edwin Johnson:** Uh, Troy,

**Cody Haugen:** updating

**Edwin Johnson:** do you know anybody who's like a badass quant that might be looking?

**Troy McDonald Kane:** Um, I can give it some thought, but they're going to be very

**Edwin Johnson:** So I found that running this company is anything but cheap.

**Troy McDonald Kane:** expensive.

**Edwin Johnson:** So very expensive is pretty much part for the course. Um okay.

**Brett StClair:** What the f\*\*\*?

**Edwin Johnson:** Um take a look because we may have to do something at after we certainly before production.

**Brett StClair:** is your thinking around the uh trying to get the uh calculation from um sports radar done on our side rather than waiting for sports radar and running a mult around that right is is that where your head

**Edwin Johnson:** Correct.

**Brett StClair:** space is going because I think that's also where George was going head

**Edwin Johnson:** Yeah. I mean,

**George Westbrook:** Yeah,

**Edwin Johnson:** maybe we can build a f\*\*\*\*\*\*

**Brett StClair:** space

**Edwin Johnson:** agent. That's a quantity.

**George Westbrook:** it so what this was this is one of the things I was looking into at the weekend is we we This is not a this is something that before launch I don't think would be possible.

### **00:14:39**

**George Westbrook:** Um is actually building our own model that would would do that. So I was looking in there's a there's a data set called NFL verse which has got every single basically all the data we need um about NFL games since 1999\. Um, and then what we could potentially do is train a more traditional machine learning model in order to give us those probabilities.

**Edwin Johnson:** Yeah, they don't have to be exact.

**George Westbrook:** Um so that yeah

**Edwin Johnson:** You know what I mean? In fact, the inexactness is probably going to be compelling for

**George Westbrook:** it

**Edwin Johnson:** traders.

**George Westbrook:** is because it it it's not it's not like a like loads of money that's going to like compare it to training an LLM for example. That's a lot of money. like that is a lot of money for this. It's just it's just outputting a probability change um or outputting a probability. So, it's not like it probably take I need to need to look at the data. Need to look at need to look at

### **00:15:42**

**Edwin Johnson:** Let me see what I Well, you do that.

**George Westbrook:** the

**Edwin Johnson:** Let me let me try to build something this week. But let let me just take a shot at it because like at the end of the day it's very um like

**George Westbrook:** Okay.

**Edwin Johnson:** it's not uh how do I say it's very systematic like you know the probabilities aren't going to go from like 80 to zero to 80 to 0 to 80\. It's always going to be like nudged and that nudged up or down is is what's tradable. And the fact is is if we're slightly hated on one side or the other. Like for example, if the game's 50/50, the score is 000 and the ball's at the 50 yard line. Um, you know, when you're in the fourth quarter and they move it to the 40 yard line, that's obviously going to make the probability different, right? And they move it to the 30, it's going to make it different. All those different things we can figure out. It's just um let let me see what I can do.

### **00:16:45**

**Edwin Johnson:** I may come up with a rudimentary model you might be able to use in the

**George Westbrook:** because I think so what we need to think is there's the there's the probability before and then as soon as the game

**Edwin Johnson:** interim.

**George Westbrook:** starts obviously every event's going to change that and then obviously given the score that So, we'd need to Yeah, if you you have a think, I'll have a think. And then by Fridays, hopefully we've got something that we can do. For the time being, we've got we've got a solution so that if nothing changes, um, we'll still be fine. Um, I just probably need to check two or two more things. Um,

**Edwin Johnson:** Cool.

**George Westbrook:** but there's progress being made on getting the algorithm, but then there's the the technical stuff outside it because obviously it's need to go every 200 milliseconds. Then there's the the cancel and replace. Um, but obviously we said we're going to push the orders then cancel them after and then it doesn't matter if there's crossing markets for a tiny

### **00:17:43**

**Edwin Johnson:** Yeah.

**George Westbrook:** bit.

**Edwin Johnson:** Hey Cody, what what's the deal with the calls? I mean, are do we have any flexibility on

**Cody Haugen:** So, yeah. So,

**Edwin Johnson:** calls?

**Cody Haugen:** that's what I was going to say is let me figure out the calls. They're not an issue. There should either be a push feed that we're that we need access to or or just need to switch as far as calls and if there's not a push feed then once again API calls are negligible. So that's just something that they need to move or put in the contract anyways the way it was supposed to be structured with the probability. So I have a call with Scott and uh David tomorrow. Um so if it's not figured out today over email, it'll be figured out tomorrow over the call. Um but the the contract is going to get rerouted, let's say. Um, and that needs to get into production. The calls need to be figured out. Um, so yeah, uh, all of that I'm not worried about it

### **00:18:36**

**Edwin Johnson:** I mean there is some value if we have our own internal proprietary methodology by the

**Cody Haugen:** 100%. Well, as you guys are talking about that,

**Edwin Johnson:** way.

**Cody Haugen:** yes, if we build our own, that's extremely valuable.

**Edwin Johnson:** Cool. Cool.

**Cody Haugen:** But so in the so in the interim,

**Edwin Johnson:** Okay.

**Cody Haugen:** George, I will figure out the API calls. we will have the API calls we need to get that done. Um, while you sort out building our own, building our own is valuable. Um, there was one other point I had going back a couple things. Yeah, it it left. Uh, I'll I'll let you know if it comes

**Edwin Johnson:** Cool. Cool. All right. Um,

**Cody Haugen:** back.

**Edwin Johnson:** what else do we have? I know you guys got a lot. So, I mean, I see fear in Max King of Bee's eyes.

**Brett StClair:** trading.

**Edwin Johnson:** A fear I haven't seen since before he left for Abiza.

**Brett StClair:** That's just a result of our visa.

### **00:19:26**

**Max Kingaby:** She's

**George Westbrook:** He's He's just had to put up his own uh death chair. So, he's he's absolutely

**Max Kingaby:** absolutely

**George Westbrook:** wiped.

**Edwin Johnson:** Max, how old are you? Can you imagine being 21,

**Max Kingaby:** 21\.

**Edwin Johnson:** Jared? Yeah.

**Jared Sapirman:** No.

**Edwin Johnson:** I mean, the fact that you came back alive means you're a lot smarter than I am.

**Brett StClair:** Don't have to

**Edwin Johnson:** So, have bless.

**Max Kingaby:** Well, I go again at the end of the month, so we'll see if I come back alive that

**Edwin Johnson:** Wow. Okay.

**Max Kingaby:** time.

**Edwin Johnson:** Good to know. Uncle Eddie's always got bail money for you. Don't worry.

**Max Kingaby:** Might have to take you up on that offer actually.

**Edwin Johnson:** No problem. No problem. Okay. Uh what's next?

**Brett StClair:** Should we talk trading?

**Edwin Johnson:** Yeah.

**Brett StClair:** Um, do you want to do you have any updates on that?

**Hasan Ahmed:** Um yeah, so at the moment I've just been trying out and then I'm just as in at the moment I'm just doing end to end trading and so it's going all the way through like into the T0 like it's giving us the execution back and then how it's handled inside the app.

### **00:20:42**

**Hasan Ahmed:** I could screen share how it looks right now because I changed the screen for it. Um

**Edwin Johnson:** Oops.

**Hasan Ahmed:** this Oh, there's everyone he see the screen and so yeah

**Brett StClair:** Yeah. Yeah.

**Hasan Ahmed:** um I mean so like I think cleaned up a bit and so like as in like it's a lot more like easier to actually understand and see see like if I was to like buy a share so at the moment I'm just doing doing it with a bunch of the test shares right now it would appear here and then it would have the um actually the entry value and then I think it's how much it's worth and then if you want to buy or sell it as well as in if you want to I mean if you want to buy like extra shares for it or if you want to as in if you want to also then sell it as well. Um as in at the moment I'm still like testing out and so like it's not going to be working right now but I'm just like cleaning up a few things.

### **00:21:49**

**Hasan Ahmed:** It will also show all of your actual executions that you you've also handled previously.

**Edwin Johnson:** That's

**Hasan Ahmed:** Um all at the bottom I think um if you from view all it has your actual like

**Edwin Johnson:** awesome.

**Hasan Ahmed:** trade history as well. And so here's all of your fields and then ads are also thrown in here as well.

**Edwin Johnson:** It's really great.

**Jared Sapirman:** Is there a way we could get access to this on test All

**Hasan Ahmed:** And so um

**Jared Sapirman:** right.

**Hasan Ahmed:** yeah um so so I have to add everyone as like a like approved lesson trader and so if you guys um find me your actual the emails for um the actual app and then I will like approve you as an actual test user and so then if you're looking by social shares like it will have the flow like already added in

**Edwin Johnson:** Cool.

**Cody Haugen:** Han, are you saying Hassan, you need us to give the Apple IDs again or the username from our sign up for the app?

**Hasan Ahmed:** Um, so it would be your um I mean I should think as in it will be your actual app and I think username and

### **00:23:02**

**Cody Haugen:** Okay. Because yeah, there's a couple people.

**Hasan Ahmed:** then Yeah.

**Cody Haugen:** Sorry. Go

**Hasan Ahmed:** Yeah. So cuz at the moment it's only in like the testing version.

**Cody Haugen:** ahead.

**Hasan Ahmed:** So only anyone who's like a like approved like a trader like it's not as cuz at the moment it's not really like exposed to anyone else. And so as soon as we get the closer to the trading I will add in like an card and so it's like if you want to be like a approved um actually the trader you need to sign here like it's included if you want to on board onto E0 and there's an extra step that you have to do. It's just entering your actual um your um I think actual name and then you're a like approved like trader. It will allocate you like a wallet and it would onboard you onto their system as well. And so at the moment it's gated right now until it's been actually been tested.

**Cody Haugen:** Yeah. No, no, no.

### **00:23:54**

**Cody Haugen:** That that that's totally fine.

**Hasan Ahmed:** Yeah.

**Cody Haugen:** Yeah. I was just going to say we're we're going to start to organize a smaller um like test group um with a few of our interns that are actually coming on board now. Um to start banging on this uh every page and and really start

**Hasan Ahmed:** Yeah.

**Cody Haugen:** to start to give us some feedback from obviously our prime demographic, our target demographic, whatever you want to call it, uh out of the gate demographic.

**Hasan Ahmed:** Yeah.

**Cody Haugen:** And so um I will get their their signups and get back to you.

**Hasan Ahmed:** Okay.

**Cody Haugen:** Thank

**Hasan Ahmed:** Yeah. I mean, I think that's everything on here for now.

**Cody Haugen:** you.

**Hasan Ahmed:** I mean, cuz at the moment, so um all of the actual shares I think static right now, like on the um actual the order book for T0 and so like if you want to buy or sell, like it's not going to go like up or down right now. But it's not until we as in I mean I think until we speak to them until we have the as in until we have the actual the order book set up properly and so I mean so every team has their actual allocated prices after that it should be fully working but at the moment it's only a small like amount of test teams.

### **00:25:14**

**Edwin Johnson:** Yeah, I I would say let's hold off on the inplay team jumping on that until Hassan gives us a green

**Hasan Ahmed:** Yeah.

**Edwin Johnson:** light.

**Hasan Ahmed:** Yeah.

**Edwin Johnson:** Cool.

**Cody Haugen:** Okay.

**Edwin Johnson:** Thanks, Hassan. That looks awesome. I like the Jets element next to it. So that's awesome.

**Hasan Ahmed:** Yeah.

**Edwin Johnson:** Um in the event that we might have to change that name um

**Cody Haugen:** Are you

**Edwin Johnson:** from New York Jets to say, you know, inplay New York Jets or something. Is that that's not a big lift,

**Hasan Ahmed:** And then no,

**Edwin Johnson:** right?

**Hasan Ahmed:** it's a small change like it's just a small um as in like it's just update on on um I think it's our config and so then it should update across the the app for all users.

**Edwin Johnson:** Yeah. Okay, cool.

**Hasan Ahmed:** Yeah.

**Edwin Johnson:** Um because we might group, we might want to look at the um the ticker for

**Brett StClair:** Let me turn

**Edwin Johnson:** these. I I I got to just run it one more time by Marlin.

### **00:26:06**

**Brett StClair:** up.

**Edwin Johnson:** How we're we're putting this out there. I don't want to I don't want to trip up a you know, an unnecessary legal thing I got to defend. Even though it's not the New York Jets, I don't want there to be a a concern and you know, people get f\*\*\*\*\* up looking at, oh,

**Troy McDonald Kane:** Yeah.

**Edwin Johnson:** I'm buying the Jets,

**Troy McDonald Kane:** Yeah. Edwin,

**Hasan Ahmed:** Yeah.

**Troy McDonald Kane:** can we can we do it similar at least for the the trading competition until we get

**Edwin Johnson:** right?

**Troy McDonald Kane:** more concise legal guidance? do it like Kelsey does it where they just do it an acronym and we do inplay like NYJ would be the example here also because we don't want the names to be too long either

**Edwin Johnson:** Yeah. Yeah.

**Troy McDonald Kane:** because when you start adding inplay in front of them it's going to get very long but if we do the acronyms inplay and an acronym then I think that's a good way Yes. model it out.

### **00:26:59**

**Troy McDonald Kane:** I don't know what anyone else thinks.

**Edwin Johnson:** I think that's perfect, Troy.

**Troy McDonald Kane:** Yeah.

**Edwin Johnson:** And you know, we could even shorten it, Troy, with just the I don't even know that we need to have the word inplay.

**Troy McDonald Kane:** Yeah. I mean, in some of our tickers, we were doing IPG for inplay global. I mean, yeah. But we can we can play around with it and see what it looks like aesthetically.

**Edwin Johnson:** Yeah. Okay, cool. Yeah, I just wanted to ask that. Awesome. It looks great. Awesome. All right,

**Brett StClair:** I think Then just um for you and Cody,

**Edwin Johnson:** what's next,

**Hasan Ahmed:** Yes.

**Edwin Johnson:** Brett?

**Brett StClair:** our uh Nova Sapion Limited group and all that kind of stuff and UTR's all landed on Friday. So what I've done is Cody, I've taken all your feedback on the proposal, the terms and conditions. I've applied all that. I've wrapped over a Nova Sapion look and feel.

### **00:27:55**

**Brett StClair:** Um, and then I've also added an SSP component to it. So, I'll get you guys that after this. I'm just doing one quick double check that, you know, it's all new branding, new,

**Edwin Johnson:** Sure.

**Brett StClair:** so I just it's occasionally spitting out a bit of rubbish. So, I'm just going through that just one last time. Um, and then at least you've got a revised proposal with the right with the terms and conditions and all that kind of stuff and a price point for the SSP stuff for

**Edwin Johnson:** Okay, great.

**Brett StClair:** you.

**Edwin Johnson:** All right. Anything else on your end, Troy?

**Troy McDonald Kane:** nothing

**Edwin Johnson:** Mr. Sinclair.

**Troy McDonald Kane:** today.

**Edwin Johnson:** Okay. And then uh George, the other thing that I wanted to add was that um obviously we want to try to get the NCAA overunder prices in uh I'm sorry, the stock prices in there as soon as possible. And if we could if we could add the a page for the uh

**George Westbrook:** Yeah.

**Edwin Johnson:** analyst in that team page, right?

### **00:28:58**

**Edwin Johnson:** We were talking about like you click on it, you discover the team, see the team's price, you click on it, then there's all that information. I'd love another page that was like analyst recommendations or analyst pricing.

**George Westbrook:** How would the analysts going to give you the information that they're they want to display?

**Edwin Johnson:** So I I'm thinking like on Wednesdays of each week there's a submission into inplay which we will submit over to Novo and then they will get populated sometime on

**George Westbrook:** Okay. And so once a week on a Wednesday,

**Edwin Johnson:** Wednesday.

**George Westbrook:** an analyst is going to put in Have you got a specific structure for their report?

**Edwin Johnson:** Not yet. I sent over a demo or a pro proposed layout. Um I'd love any feedback from anybody on that. Um not not Yeah,

**George Westbrook:** I don't think I saw that.

**Edwin Johnson:** not that big of a deal. I mean that this is more about that outreach because uh Cody and that gem of a guy Kevin Murray have been able to go out and get a couple of influencers who are going to be essentially analysts and talking about a price on their podcast and like you know we want to hit more people because our signups so far are pathetic.

### **00:30:21**

**Edwin Johnson:** Our signups are at less than 100\.

**Cody Haugen:** Over a 100 now this morning,

**Edwin Johnson:** Okay.

**Cody Haugen:** but negligible.

**Troy McDonald Kane:** Yeah.

**Cody Haugen:** 101\.

**Edwin Johnson:** Negligence 101\.

**Cody Haugen:** Yeah. Yeah.

**Edwin Johnson:** 101 Dalmatians of f\*\*\*\*\*\*.

**Cody Haugen:** Yeah.

**Edwin Johnson:** We need to uh like I mean on our own team like we're not hitting even enough of our friends and relatives to convert like you know aside from all the other b\*\*\*\*\*\*\* we've done. Um so we're going to have to make sure that we significantly ramp up those signups over the next couple weeks. That's our our main draw for inplay is we need we need 10,000 people signed up to trade and because this isn't going to work out well if we have

**Brett StClair:** Hold

**Edwin Johnson:** 300 people trading this

**Cody Haugen:** Yeah, exactly.

**Edwin Johnson:** cool um

**Cody Haugen:** Uh oh. So, so on that, George, um on that, George, so is it possible somewhere in the vault,

**Edwin Johnson:** Okay.

**Brett StClair:** on.

**Cody Haugen:** right? if or maybe it's not the vault.

### **00:31:20**

**Cody Haugen:** I'm just thinking the vault because it's already built. But like in somewhere in the vault, we give them a a login and it basically uploads as a CM, you know, into like a CMS and then you guys can draw from that. Basically, we're not going to I mean, it's starting with four, you know, or three guys, I guess, from preferred walk-on for college, but we're also going to add NFL. I mean probably at its peak you're looking at somewhere between six and 10 people potentially um as these right and

**Edwin Johnson:** various reports, six and 10 different reports.

**Cody Haugen:** actually at its peak that's just college football and NFL so at its peak for the trading challenge six to 10 different analyst reports then we had an NBA there's three to four more so it it does scale out um so we just have to think about that but is a CMS somewhere in the vault where they can upload it and then it's already digitized in a way for you guys to grab it and pull it into the app. Is that easier?

### **00:32:18**

**Cody Haugen:** As opposed to them sending us an email or some s\*\*\* like that and then forwarding.

**George Westbrook:** Yeah,

**Cody Haugen:** That sounds like an absolute

**George Westbrook:** that cuz that's that's what I was thinking is there's some way that we allow them to

**Cody Haugen:** mess.

**George Westbrook:** upload it. So it's not they send it in an email and we need let's say 10 fields and they put eight and then one of them's really really long. It's that would make it easier. It's not to say doing that is a two-day thing. Like it's still it's still a decent amount of work.

**Cody Haugen:** Right.

**George Westbrook:** Um it's not like the front end stuff. It's we build it, see what it looks like, blah blah blah, but it's that back end making sure that it's uploading at the right point. And I think in in terms of priorities for this week. I mean, we've got the the trading, the ads, and the market maker. Um, which is like they're obviously we all agree they are completely non-negotiables.

### **00:33:10**

**George Westbrook:** So, I think ideally if we just funnel all the effort into that,

**Edwin Johnson:** Correct.

**George Westbrook:** um, there's most likely going to be a bit of time before launch where it's just testing, testing, testing. And I feel like this is something like that that'd be good to slot in at that point in time. Um but I think for the time being it's just focus on ads trading and the market

**Cody Haugen:** 100% agree with you.

**Edwin Johnson:** Yeah, yeah, that's fair. I do want to get a date uh certain,

**George Westbrook:** maker.

**Edwin Johnson:** Cody,

**Cody Haugen:** It

**Edwin Johnson:** that we want to start talking with those guys and the other NFLs because timing wise for us to put it in

**Brett StClair:** That's

**Edwin Johnson:** there now, it really doesn't it it's important,

**Brett StClair:** it.

**Edwin Johnson:** but it's not that important. I mean, we can just put the inplay one in there, you know, we don't need to have multiple fields. we can just come up with a, you know, basic page. It's pretty simple. It's like, you know, underperform, neutral, overperform, and a target price, you know, and if you want, you could have a small blurb or something, but most people are just going to look at the target price and the underweight overweight.

### **00:34:10**

**Edwin Johnson:** It's not like they're going to do a full report on the Air Force Falcons college football team

**George Westbrook:** H.

**Edwin Johnson:** every single week,

**George Westbrook:** M.

**Edwin Johnson:** right? I mean, it's just something that people will be able to use and more importantly, it's an outreach for us because we do need we do need the user acquisition. We've got to get way more users. So, hopefully with the the timing of it, yeah, I mean, this week I would put that on hold, too. Um, but there is going to come a point over the next, I would say, three weeks,

**Brett StClair:** That's

**Edwin Johnson:** so a week before the the actual IPO, we we're going to want people to be able to uh get in the queue and submit orders to buy shares

**George Westbrook:** Yeah.

**Edwin Johnson:** in that in that IPO.

**Brett StClair:** everybody sent it.

**George Westbrook:** Yeah.

**Edwin Johnson:** Cool.

**George Westbrook:** Yeah.

**Edwin Johnson:** Awesome. Okay. Awesome. Anything else that we've got today?

**Brett StClair:** Absolutely.

**George Westbrook:** I think from our side I think that's

**Edwin Johnson:** I think if you're done, we're done.

**George Westbrook:** everything.

**Edwin Johnson:** Listen, we're we're real close. So, thank you again for all the hard work.

**Cody Haugen:** Let's

**Edwin Johnson:** You guys have been great. Inplay team, great week this week. Let's just keep going. Whatever we have to do, please don't leave any stone unturned.

**George Westbrook:** Let's f\*\*\*\*\*\*

**Troy McDonald Kane:** Absolutely.

**Kevin Murray:** Yep.

**Troy McDonald Kane:** Let's f\*\*\*\*\*\*

**Cody Haugen:** f\*\*\*\*\*\*

**Edwin Johnson:** Thank you.

**Kevin Murray:** f\*\*\*\*\*\*

**George Westbrook:** go.

**Troy McDonald Kane:** do

**Edwin Johnson:** All right,

**Cody Haugen:** go.

**Kevin Murray:** go.

**Edwin Johnson:** we'll look forward to seeing the paperwork too then, Brad. Okay.

**Brett StClair:** Cheers. Thanks, guys.

**Edwin Johnson:** Okay.

**Cody Haugen:** All right. Dark.

**Edwin Johnson:** Your planet.

**Brett StClair:** Catch you soon.

**George Westbrook:** Speak to you all soon.

### **Transcription ended after 00:35:46**

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*