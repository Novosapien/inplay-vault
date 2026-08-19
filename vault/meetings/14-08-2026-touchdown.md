---
date: 2026-08-14
type: standup
description: "Friday touchdown, 14 August 2026: the debrief after the first live game night. Edwin's confidence crisis, the diagnosis that the fault is UI rather than back end, and the one-click trading model he demonstrated."
source: "Gemini meeting notes, Inplay - App - Touchdown"
scope:
  - "[[trading/trading]]"
  - "[[information-layer/sub-components/single-game-page/single-game-page]]"
  - "[[information-layer/sub-components/research-tab/research-tab]]"
  - "[[market-maker/market-maker]]"
  - "[[delivery/delivery]]"
status: extracted
extracted-to:
  - "[[trading/trading]]"
  - "[[trading/sub-components/order-entry/order-entry]]"
  - "[[information-layer/sub-components/single-game-page/single-game-page]]"
  - "[[information-layer/sub-components/research-tab/research-tab]]"
  - "[[market-maker/decisions]]"
  - "[[delivery/delivery]]"
  - "[[one-click-trading-requirements-aug-2026]]"
---

## Post-Call Analysis

~67 minutes, the morning after the first live game night, and the most consequential call in the record so far. Present: Edwin, Cody, Troy, Jared, Kevin, Gary (InPlay) and Brett, George, Max (Novosapien).

**Edwin opened by questioning whether the product can launch at all.** His words: the previous night was _"unquestionably the worst trading experience I've ever had in my life"_ and _"a failure pretty much at every touch point"_. He is due to put **$800,000 to $1,000,000 into marketing** and stated plainly that he cannot do so against what he saw. He put his own position at **$6.6 million invested**, summarised it as _"we don't have any users, we don't have any advertisers, we don't have technology that's comparable... I've got an idea and that's about it"_, and said he believes it is _"impossible to be ready by football season"_. He was explicit that this is not giving up, and equally explicit that he has to decide what more he is willing to fund.

Brett's counter, and the agreement that came out of it: this was the **first full end-to-end test ever attempted**, three months from a standing start, with the market maker and taker added as an unplanned three-week workstream. His ask was for **two more live runs before any decision is taken**, on the grounds that the call was being made too early. Edwin accepted the runs. The decision itself is deferred, not resolved.

**The diagnosis matters more than the reaction, and it is unusually clear.** Troy, who has the most venue experience in the room, placed the fault squarely away from the back end: tZERO confirmed their side operated as it should, with **3 million orders sent and an average latency of 1 millisecond**, and no degradation of the matching engine. His conclusion was that the harder part is already working and what remains is the interface and the data ingestion. George's version: the work needed sits on the tip of the iceberg rather than beneath it. That reframing is the single most useful output of the call, because it turns a crisis of confidence into a defined and largely front-end workload.

**What actually went wrong** is captured in the findings table and in [[one-click-trading-requirements-aug-2026]]. The through-line is that the app was built to protect a user from mistakes and the people testing it wanted to trade at speed. Confirmation steps, page transitions and screen takeovers each cost a second, and a trader losing a second loses the market. Cody counted five screens to get back to the game after a trade. Troy repeatedly _"missed the market"_ because the order book and the order ticket disagreed.

**Edwin then demonstrated his own prototype's trading model in detail**, which is the most concrete requirement set he has produced. It is extracted separately rather than summarised here, because it is a specification rather than feedback.

**Two reversals worth carrying forward.** Gamecast was **downgraded** by its strongest advocate: _"it's less important than you think... it gives you information, but doesn't give you a substantive edge to trade it."_ And the commercial position hardened: with no advertisers signed, Edwin now treats the **subscription as the only revenue path**, which makes the strategy lab the product rather than a feature.

| Finding | Destination | Action |
|---------|-------------|--------|
| Edwin questions whether launch is achievable; funding decision deferred pending two more runs | [[delivery/delivery]] | Recorded as the headline delivery risk |
| tZERO side clean: 3m orders, 1ms average latency, no engine degradation | [[market-maker/decisions]] | Recorded; reframes the fault as front-end |
| Fault located in UI, navigation and data ingestion, not the back end (Troy, George) | [[trading/trading]] | Update written |
| Trade confirmation returns to portfolio or IPO tiles instead of the game; five screens to get back | [[trading/trading]] | Defect, high priority |
| Order book out of sync with the order ticket; users missed the market repeatedly | [[trading/trading]] | Confirms Jared's written report |
| No market order, so some trades were not placeable at all | [[trading/sub-components/order-entry/order-entry]] | Synthetic market order promoted |
| Screens freezing, partly caused by hot fixes pushed mid-game | [[delivery/delivery]] | Process change agreed |
| Two app versions in circulation confusing testers | [[delivery/delivery]] | Process change agreed |
| Lag with six concurrent games; loading everything at once | [[frontend-performance]] | Optimisation in flight |
| IPO cards appearing during the run; switched off for the next | [[ipo-module/ipo-module]] | Done same morning |
| Favourites and watchlist not changeable; unclear how | [[information-layer/sub-components/discovery-home/discovery-home]] | Defect |
| Gamecast swipe inconsistent; card sequencing off | [[information-layer/sub-components/single-game-page/single-game-page]] | Defect |
| **One-click trading model demonstrated in full** | [[one-click-trading-requirements-aug-2026]] | Extracted as a requirement set |
| Gamecast downgraded: informative but not an edge | [[information-layer/sub-components/single-game-page/single-game-page]] | Priority reversal recorded |
| Subscription is now the only revenue path; strategy lab is the product | [[information-layer/sub-components/research-tab/research-tab]] | Update written |
| Strategy lab numbers: one rule across 138 teams ~$1.1m, profitable on 129; parameter sweep moves $93k to $1.3m | [[information-layer/sub-components/research-tab/research-tab]] | Recorded |
| Strategy lab confirmed number one priority after the trading experience | [[information-layer/sub-components/research-tab/research-tab]] | Priority recorded |
| Multi-year Sportradar history wanted, four to five seasons not one | [[integrations]] | Ask restated |
| Target user is the ~30% who trade actively, not the weekly visitor | [[audiences]] | Recorded, with George's counter |
| Granular feedback protocol agreed: screenshots and recordings, not "the app is slow" | [[delivery/delivery]] | Process change agreed |
| More runs: 14 and 15 Aug and beyond, described as actual runs not dry runs | [[delivery/delivery]] | Dates recorded |
| Confirmation that 22 Aug is the offering only; games start 29 Aug | — | Already recorded |

---

Aug 14, 2026

## **Inplay \- App \- Touchdown \- Transcript**

### **00:00:10**

**Brett StClair:** Good morning,

**Jared Sapirman:** Come

**Brett StClair:** Jared.

**Jared Sapirman:** on.

**Brett StClair:** I like your feedback. Thank you for that. Um, we think also you might be on an older version of the app on some of them, but I think your feedback was great. So, thank you.

**Jared Sapirman:** Yeah, I got a lot more where that came

**Brett StClair:** Good.

**Jared Sapirman:** from.

**Brett StClair:** Um, the more the better before you go live. Um, sooner the better as well.

**George Westbrook:** Hello.

**Brett StClair:** Hello everybody.

**Kevin Murray:** How's it going?

**George Westbrook:** Oh, good. How you

**Brett StClair:** Yeah.

**George Westbrook:** doing?

**Kevin Murray:** Exhausted.

**Brett StClair:** What have you been up to? You got a bit of a sweaty face there.

**Kevin Murray:** I'm in uh VA Las Vegas.

**George Westbrook:** Oh god. Did you Did you have to sell your soul last

**Kevin Murray:** No, no. I was I was actually very good. I was uh I was in bed by 1:00,

**George Westbrook:** night?

**Kevin Murray:** but uh Cody rang me at uh 5:00 this morning with the time difference, so I was like, "f\*\*\*." So,

### **00:01:22**

**Kevin Murray:** yeah, been awake an hour and a half earlier than I needed to be, but uh it's all right.

**George Westbrook:** That's That's not ideal.

**Kevin Murray:** So, yeah.

**George Westbrook:** Don't we were watching we were watching the games last night and just did not realize how many ads there are in American football games.

**Kevin Murray:** Yeah,

**George Westbrook:** Like compared to pre compared to Premier League,

**Kevin Murray:** it's

**George Westbrook:** it's like just so

**Kevin Murray:** Yeah, there's more ads than there is the f\*\*\*\*\*\*

**George Westbrook:** different.

**Kevin Murray:** game. You know what I mean? It's It's ridiculous.

**Brett StClair:** I really had that many ads.

**Kevin Murray:** And it And it's like stop start stop start. Like to be honest with you, it's I find it very annoying to watch compared to like the Premier

**Jared Sapirman:** That's cuz you use the socket.

**Kevin Murray:** League. I Yeah, I know. But that's what I mean. It's like when you watch the Premier League,

**Jared Sapirman:** Yeah.

**Kevin Murray:** it's 45 minutes of non-stop and then you have your 15 minute halfime and then you're back at it again.

### **00:02:17**

**Kevin Murray:** Where this is like every two seconds, it's like a break for something. So yeah.

**George Westbrook:** can just imagine like a Milw versus West Ham game and with If they started adding in adding in the brakes, I think that would Yeah, that would be

**Kevin Murray:** Oh yeah.

**George Westbrook:** chaos.

**Brett StClair:** Hello

**Kevin Murray:** Nuts.

**Brett StClair:** everybody.

**Cody Haugen:** Hello. Uh, Edwin, you're on mute.

**edwin's Presentation:** I ain't know it does that. Um, all right. Hey all. Um, I'm going to cut right to it. you know, um I'm not sure where everyone's heads that that was unquestionably the worst trading experience I've ever had in my life last night. I have actually um I don't know how to describe it other than it was a failure pretty much at every touch point that I could see. I don't know how the orders went, but it was it was horrible. Horrible. It's given me a a sleepless night completely. and I'm not sure what I want to do next. Okay.

### **00:03:33**

**edwin's Presentation:** I don't know that we can fix what needs to be fixed in time. Um, we'll talk about that a little bit, I guess. Um, yeah. I mean, it was just a f\*\*\*\*\*\* total disaster in my eyes.

**Brett StClair:** So, can I stop there?

**edwin's Presentation:** Yeah.

**Brett StClair:** I think what was delivered between T0 and um us was insane. Like what was actually delivered in the timeline was nuts. I've never experienced that. What I'd want from you guys is where do we need to improve it? So you guys have had the prototypes, the experience for a long time. If the experience is poor, let's change it. If it's a trading problem, then let's tweak those algorithms, right? If that's what it is, we got to tweak it. If it's speed, like we've already been seeing, the speed's actually not too bad. There a couple of tweaks we need to do. This is the first time we've run a full end to end test ever done in 3 months.

### **00:04:48**

**Brett StClair:** That's insane. Focus now is not give up. Poor performance, all that kind of stuff. Where is it bad? Work on it. Focus on the key points that need to be focused on. Get through it as quickly as we can. Ready for this afternoon's run. That's where we got to be. Do you agree?

**edwin's Presentation:** Uh who's that question to?

**Brett StClair:** Sorry.

**edwin's Presentation:** Who who you asking? Um I don't know how to answer that question. I um yeah, I would say that uh you know, I'm I'm probably you know, at least in in of the people I know, I may be the most tenacious person I know. So, I'm not a quitter and I don't give up at things. But I also have to look logically at where we're at and um what

**Brett StClair:** I don't think the changes are that big. I think we break them down cuz It's not helpful saying it's a poor trading experience. I think what's helpful is going where is it poor?

### **00:06:05**

**Brett StClair:** You know, like we've been breaking it down and we can actually identify the areas that need fixing. I thought Jared's feedback was really constructive. Let's get it focused. Remember, we've got this whole agentic consumption platform that can do the change. If it's a gap between where your prototype app is and that we need to get it up there, let's get those components, we iron them out and we be ready for the next run this evening. This is how technology works. Like when you're building technology from scratch at this scale across the ecosystems that we've built with the timings of things like market maker and market taker being thrown in as a last minute 3 weeks to get done.

**Cody Haugen:** Oops.

**Brett StClair:** What's been pulled off is close on a mira like a miracle and we still got three more days or two more days of testing. So, like I get it. You might feel a little bit down, but we've got to break it down and go, here are the areas that really need work.

### **00:07:09**

**Brett StClair:** Break it down and give the teams an opportunity to fix it. Throwing in the towel when really we're probably 2, three days of running and trying to fix and optimize, I think is crazy. like you've got something amazing. The technology that's been stacked and built is insane.

**edwin's Presentation:** Yeah,

**Brett StClair:** And it's like,

**edwin's Presentation:** I I I hear you. Let Let me interrupt you and I appreciate all that and you know you know some of it you know

**Brett StClair:** you know,

**edwin's Presentation:** uh is fair. Uh some of it is a little hyperbole. you know that this isn't my first rodeo with building tech stuff, Brett. Okay. Um, you know, my concern is that, you know, the group, you know, from a trading side, you know, uh, it wasn't great. Okay. Um, you know, the the the the freezing, the the cumbersomeness of it all. um you know that it's things not matching, things breaking. I've I've done dry runs before, okay? And and you know, I've built things that are far more sophisticated than what a market maker is, which is pretty basic s\*\*\* for what I've given and a market taker.

### **00:08:34**

**edwin's Presentation:** Pretty basic s\*\*\*. That's not that is not a high lift. Okay. So,

**Brett StClair:** It's unplanned on top of everything and we're

**edwin's Presentation:** sure. Let let me finish, please.

**Brett StClair:** extra hours and it's a bunch.

**edwin's Presentation:** Yeah.

**Brett StClair:** It's it's an algorithm. We tweak things.

**edwin's Presentation:** No, I understand.

**Brett StClair:** Half the time the market may buying things too fast because the range

**edwin's Presentation:** I'd like to let me let me know when I can finish. Okay. May I finish?

**Brett StClair:** Yep.

**edwin's Presentation:** Great. Um, cool. So, you know, we are scheduled to launch in a week and um, a week and a day. I'm also supposed to put about, you know, $800,000 or a million dollars into marketing. I cannot go to market with what we had last night. Okay. At all. It just it that would be the the I might as well just close now. So, you know, I'm not suggesting giving up anything.

### **00:09:36**

**edwin's Presentation:** What I'm suggesting is I don't know that we can be ready for football. I don't know that it's going to be ready in 3 weeks for football. Not for for what the market wants and is used to when it comes to trading this stuff. Bear with me one second. trying to make a little money on the in the market here. Um, but nonetheless,

**Brett StClair:** That's that's impressive.

**edwin's Presentation:** nonetheless, uh, what's

**Brett StClair:** That's impressive, Edwin.

**edwin's Presentation:** that?

**Brett StClair:** Sorry. Trading as you're dealing with all of this. Anyway,

**edwin's Presentation:** I've Well,

**Brett StClair:** but I'm also I'm not suggesting we get up.

**edwin's Presentation:** we've been Listen, Brett,

**Brett StClair:** I'm I'm fighting for the you give us more practice.

**edwin's Presentation:** since we Yeah. Yeah.

**Brett StClair:** Two more test runs.

**edwin's Presentation:** Yeah, I mean,

**Brett StClair:** I like

**edwin's Presentation:** sure, you you want test runs, you can have test runs. I listen, I I'm just trying to put forth a a practical um a practical expectation for the for the team.

### **00:10:43**

**edwin's Presentation:** Uh for the team because like, you know, what I'm willing to do in terms of spending money on where we're at is limited. Okay. I'm I'm you know it's it's not where we need it to be. Okay. I I I I don't know how to put it other than that. Um you know, I want to set the you know, the floor is just like, hey, it just didn't this was not great. I have to decide what I'm willing to do financially to push this forward for the football season in in my in my mind's eye. Um it's it's impossible to be ready by football season. That's that's what I believe. Okay. Thank you. All right. Just made some money Brett just for me.

**Brett StClair:** Nice. So I mean can we make a final decision on that? So, like I've gone through many many go lives and you know like again the difference is this one was the most insaneest timelines volume you know all of that kind of stuff but I think we're close and I'd rather let's have this discussion rather on a Monday morning, see where we land then and like things like we need to apply a lot of Jared's kind of feedback.

### **00:12:07**

**Brett StClair:** We really would like like what areas are not kind of performing well and then get some advice on how we can either broaden the market maker and how we can refocus. Troy, I think you had a bunch of really good recommendations in the previous call what we could be doing there. Let's give it a run. In my experience of getting technology to a point, doing these live runs and pushing stuff like we're doing last night was insane. We do it two more nights in a row. I think you're going to be very, very close to a really good platform. Now, I wouldn't have said that. I would be totally with you if we were using old school technology, old school way of doing things. I would have I would have actually been saying this three weeks ago. f\*\*\* it. We are never going to make this. But the setup that's running at the moment, I think we need two more two more test runs and I think we're there. And if we aren't, then let's make that call then.

### **00:13:06**

**Brett StClair:** I think we're just making the call too early. That that's my advice, Edwin. That's my frustration, right? Give it two more and then make the

**edwin's Presentation:** Yeah. Well,

**Brett StClair:** call.

**edwin's Presentation:** I mean, I'll be candid. I think we should have had some dry runs done with, you know, old data, you know, with the in the in the last few weeks. Um,

**Troy McDonald Kane:** Well, no.

**edwin's Presentation:** sure.

**Troy McDonald Kane:** I think there was some dry runs with the old data. The problem is the old data is it's too static. I think part of the optimization that had to happen last night was the ingestion of all of the sports radar data and the live market data off of TZ's platform at the same time. So I think I think where the trading experience just to chime in probably needs to be overhauled is not on the back end right now. It's some of the guey UI work. And what I would strongly encourage you to do is take what Edwin has done in his redesign and apply that wherever you can right now for the next dry run and for the ne and for Saturday's dry run.

### **00:14:09**

**Troy McDonald Kane:** Like it's it's not just the performance that was an issue. It was like my screen freezing when I tried to hit a button or I had to con and I know it's because you were pushing hot fixes through at the same time which is also not ideal because not everyone is synced at the same time with the same level of functionality. Um you had to take gateway offline at one point right to to reset it.

**edwin's Presentation:** Nothing.

**Troy McDonald Kane:** So, but it's more of just some some of the layout of the UI is just not intuitive. And like when I would hit trade, I would make a trade, it would bring me back to the IPO uh tiles, which was frustrating. When I was on the Gamecast, I I couldn't swipe the same way every time. So, I think where we should start.

**Brett StClair:** Let's gather all of that by the way because

**Troy McDonald Kane:** Yeah, I know. But I'm just I'm just summarizing what would be the next step for the Novo team would be to take the LA what what Edwin has kind of mocked up and emulate that to the best of your ability on the

### **00:15:06**

**edwin's Presentation:** Oops.

**Brett StClair:** Yes,

**Troy McDonald Kane:** current

**Brett StClair:** I'm totally in agreement with you on that.

**George Westbrook:** Because I think what we've got at the moment is the homepage and the team page. It I think it's where is

**edwin's Presentation:** Perfect.

**George Westbrook:** it. So this page and this

**Max Kingaby:** And is there a charge?

**George Westbrook:** Yes. Oh yeah, the homepage, the markets page, and then the team page.

**Troy McDonald Kane:** Okay. So,

**George Westbrook:** Is there

**Troy McDonald Kane:** this this has already been you guys have already been working on this this morning.

**George Westbrook:** it?

**Troy McDonald Kane:** Your

**George Westbrook:** Well, yeah,

**Troy McDonald Kane:** time.

**George Westbrook:** some of some of the stuff um some of the stuff has been added in um but not all of it. Not all of the not all of the reworks.

**Brett StClair:** So, have we got everything there? Is that the latest version that everyone needs to work off and that it's that's the version that's comfortable on cell and we've got the entire journey. Okay, George.

### **00:16:44**

**edwin's Presentation:** I have an updated one um I worked on last night.

**Brett StClair:** Yeah, let's get that. We're working off that and and give it a bash, right? because front ends are generally easier for us to manipulate unless it's, you know, massive on the database and and needing new screens and stuff, but like reshaping and all that kind of stuff. It's the same way like Edwin drawing up the prototypes is easier. This is also easier from that point of view. The hard part is that we pushing it real time, you know, as you guys are game playing and everyone has different versions. That's that that's where the balls up is. And so maybe what we do is we do we say we're not going to push any fixes until the end of the game. Then the next game we push all the fixes through. Everyone does a revamp, rejazz, and then next game run it through. Everyone we capture any bugs, errors, and we just need a way to people to send us those bugs and errors, right?

### **00:17:37**

**Brett StClair:** As quickly as we can. And then we apply them again the next game. We check it, but we don't do any pushes like we were doing last time through the game because we're just trying to fix as quickly as we possibly can. Does that sound like a plan?

**Troy McDonald Kane:** Yeah.

**edwin's Presentation:** Um I mean maybe um sure before

**Troy McDonald Kane:** Go ahead.

**edwin's Presentation:** before Kevin or Cody, do you have anything that you want to add? I mean, the only one who's on this. So, I don't know if the new guy, Vineth, if he's a DJ or not. He certainly looks like one. Um, but if we are going to be talking about trading it and betting it and all the rest of it, the only two people on the call that matter are me and Cody. I mean, the the rest everyone's going to do it like cursory testing,

**Kevin Murray:** Okay.

**edwin's Presentation:** did the order go through, whatever. But as far as like maybe Kevin a little bit because I seen him play slot machines, but at the end of the day, like we know what people f\*\*\*\*\*\* want.

### **00:18:31**

**edwin's Presentation:** Like we know exactly what that's supposed to look like. You know, I'm I'm literally clicking buttons here. I'm trying to make some money as we're having this conversation. So, um you know,

**Brett StClair:** every day.

**edwin's Presentation:** you know, Cody or Kevin,

**Brett StClair:** That's

**Cody Haugen:** Yes.

**edwin's Presentation:** you want to add anything?

**Cody Haugen:** So from Yeah. I mean I mean let's let's just start from a very high level.

**Kevin Murray:** Okay.

**Cody Haugen:** The I mean the first eight minutes of the game I felt like did go better. I mean, as expected for a first time live test run, right? Um, orders were being filled. Uh, I was able to get in play, but a a after that first quarter, I mean, it as we all saw it, the none of the prices were matching all of those certain things. I mean, we need the interface to reiterate what Troy and Edwin have said. We need that interface from the the actual button of clicking buy or sell to bring you right back to the price page or right back to that game page so that you are right back in the game.

### **00:19:32**

**Cody Haugen:** So, as I'm I mean I to to try and sell my long shares on the Packers after the you know after they scored and ran four plays and I wanted to get out to try and sell and then short them because Pittsburgh had already had a 20 yard uh uh catch. Then I wanted to short that on that drive. It was impossible based on the number of clicks and and like I said, I I don't know if it's because we were too deep in the forest to see the trees with this, but what we've designed is not what what is what is today and what we've built is not where we need to be from a interaction trading every play. It's just not functional enough. It's it's it's not I was I had to click through like five screens to get back to the the game. I had to trade. Trading took me to the portfolio. Portfolio. I had to go back home. Home home. I had to go back to the upcoming game or the live games to get back into live match tracker

### **00:20:33**

**George Westbrook:** Yeah.

**Cody Haugen:** view. All being said, what is factual information and has been proven at least from my brain is I treated it like a DGEN better last night. I tried to move as fast as humanly possible through it and place live trades as I would a live betting experience.

**edwin's Presentation:** Okay.

**Cody Haugen:** Now those five clicks X brought me back to the live match tracker. I watched the entire first half of the Packers and Steelers game through that live match tracker and I even had the game on my TV on the NFL network.

**edwin's Presentation:** Thank

**Cody Haugen:** And you know that what or why that is is because of what Edwin and I have been harping on is that live match tracker is

**edwin's Presentation:** you.

**Cody Haugen:** faster than TV. So if I see an update there, I'm going to keep my eyes glued to that because that's going to move that price and that's what I'm going to cash out and sell. So I I need to click that button. If that button goes through the trade confirmation,

### **00:21:26**

**Troy McDonald Kane:** Yeah.

**Cody Haugen:** needs to take me right back to that page

**George Westbrook:** Yeah, that was that was literally the one of the first fixes I tried to add.

**Cody Haugen:** with

**George Westbrook:** Um, I did exactly the same thing.

**Cody Haugen:** Yeah.

**George Westbrook:** I clicked buy. I was like, "Why is it taking me to the f\*\*\*\*\*\* trade page? I want to go back to the game." Um,

**Cody Haugen:** Yeah. Well, and and it's it's also extra wonky right now to a point we've already made that there is basically

**George Westbrook:** so

**Cody Haugen:** two versions of the app in there in the ether. it taking me to the IPOs during the tri run was just I

**George Westbrook:** yeah.

**Cody Haugen:** mean kicked me in the head while I was down at that point. I was like none of this even functioning right now or even a a point of of emphas emphasis.

**Troy McDonald Kane:** Yeah.

**Cody Haugen:** But yes, so that flow of that, like I said, I think we were too deep in the forest to see the trees, but from a I need to be able to sell along and short it within

### **00:22:23**

**George Westbrook:** So I

**Troy McDonald Kane:** And I want to be able I want to be able to go long one team and short another team within seconds,

**Cody Haugen:** seconds.

**Troy McDonald Kane:** too.

**George Westbrook:** think

**Troy McDonald Kane:** And that's what I was trying to do last night. And by the time I got there, the market moved away from where I wanted to trade. And that was part like that's why I kept saying on the earlier call, I kept missing the market. you know, there has to be a like it has to be, you know, two to three seconds at best, you know, or at worst, I should say, you know, that you'll be able to to swipe back and forth between um buy sell orders and the two teams that are playing against each other and like everyone's saying, like not have to leave that gamecast because I also was only watching the game during the game, you know, through the gamecast because I was watching two or three games at once and uh I didn't I couldn't figure out how to change my favorites.

### **00:23:10**

**Troy McDonald Kane:** I couldn't figure or watch list. I couldn't figure out how like it wasn't as intuitive it needs to be from what other apps that do the same thing are able like I because I would have like the other thing is the card sequencing was

**George Westbrook:** Found

**Troy McDonald Kane:** always off too on the slide and like we talked about earlier having all the college games in there made it a little messier but obviously that's how it's going to work in production. Um, is there a way to turn off the IPO cards for the next dry run and actually have emulate a

**George Westbrook:** it.

**Troy McDonald Kane:** full secondary trading post

**George Westbrook:** Yeah, lit literally that was one of well one of the things we've done this morning is turn that off because obviously at the moment

**Troy McDonald Kane:** IPO?

**George Westbrook:** we don't want to have loads of divergence between what's in the app store and what's there but we need to test it. So we switch that off. It's going to be like a full secondary trading experience.

### **00:24:02**

**George Westbrook:** Um then going to be reworking the pages, but I think a lot of the so there's the lag like where that's lagging just because it's the first time we've had what was it six games going at the same time and the way that we were loading some of the data is is kind of everything at once um give or take. So now we're working on optimizations to that. So, the clicking and the lag should be gone hopefully by tonight. It might be, it might not. Um, if not by tomorrow, um, there will be improvements in terms of UX and and UI in terms of as a trading experience. I think you said it best, Cody or Edwin, Edwin, um, traders. Um, we're not the DJ. So, that's where we're going to need both yourself, Edwin, and Cody to really like nail down. and when it's this is not working. Okay, we we need we need to know um because we we're not sitting there trading these live or betting on these live games and unfort what we don't know we don't know.

### **00:25:05**

**George Westbrook:** um is not to say we're we're not going to work it out at some point,

**edwin's Presentation:** I don't

**George Westbrook:** but by getting that tight feedback mechanism um with say like screenshots and

**edwin's Presentation:** know.

**George Westbrook:** and a bit of explanation about as to what it is that's when we can start churning through it and that that would be really really helpful for us like Jared your feedback was really really helpful um because it's like this is wrong this is what it should be blah blah blah um like we said we have moved quite quickly like I think poly and Cody was four years raised 30 million 85% of their team was engineers um and what it's it's three months all of us working together starting from ideulating requirements to getting it built um it's going to be s\*\*\* to start with um it's just now we know we can iterate a lot quicker two weeks is a lot of time a lot of the changes are UI um and app related and I know Edwin you hate me talking about the iceberg. But fortunately, the work that we need to do is on the tip.

### **00:26:08**

**George Westbrook:** It's not below it. When we had the call with T0, like I think the market maker yesterday, it was three three and a half million million

**Troy McDonald Kane:** million orders. Yeah.

**George Westbrook:** orders and

**Troy McDonald Kane:** And the average latency was uh 1 million.

**edwin's Presentation:** Say again. How many

**Troy McDonald Kane:** 3 million orders were sent last night and the latency was averaged at 1

**George Westbrook:** that

**edwin's Presentation:** orders?

**Troy McDonald Kane:** millisecond. That's really So everything it to to George's point, T0 confirmed everything operated on their end. that should have with no issue. Um, as far as order flow, uh, market data, latency was able to handle that many orders. There wasn't really any degregation of latency on the on the matching engine side. So it is about optimizing the data ingestion and making sure because that was obviously an issue that we keep saying is that the data is the data wasn't seen. thinking and that could just be again the fixes you're pushing out at the same time but um at least know everything on the back end is functional working that

### **00:27:05**

**George Westbrook:** I think it's

**Troy McDonald Kane:** is in my opinion the harder part um so um now we just have to optimize the UI and the data

**George Westbrook:** That's it. The only the only exposure to what's going on for for everyone is through the app. Um so if it looks as if like so if the data is not coming in quick enough, something's not something's not firing, then it looks as if it's all broken. The in from the app's perspective, there is the latency. I think there was one issue that that you sent through where you placed an order. It should have been at the top, but I think before the UI could even update was filled.

**edwin's Presentation:** Yeah, it didn't give me a fill though. It showed me as a working order.

**George Westbrook:** What was this on? So when you click say buy um it went through to the next and then it went on the order confirmation page working. Yeah, that cuz I I thought that in your in your thing it showed as when you confirm an order it should show working but rather you'd want it it updates cuz I thought we under the impression that when you click done then you go back to that page and then it's going to show if it's open and I think in the screenshot you sent it showed that it was filled but I don't know if that was the the correct Hold

### **00:28:27**

**edwin's Presentation:** I'm not sure when I placed the order um there was no uh I was top

**George Westbrook:** up.

**edwin's Presentation:** a book so the market maker quotes at a certain width and then if I want to jump in between the market maker I can place an order and I I did orders not necessarily be profitable you know I did orders that I wanted to see where the uh the platform would behave, you know, would they show me certain things and, you know, aggressive cancelling, aggressive bidding, all that stuff, you know, um because like you know, when you when you trade, okay, um you know, you don't want to have a lot of things in the way of trading. you know, you want to click a button for a buy and the order gets sent. And you know, I have it on this app that I've been playing with where you can just have oneclick trading where you take away the confirmation cuz like the way I trade right here as we're talking, I've made 347 trades since we've had this call. Okay.

### **00:29:35**

**George Westbrook:** So,

**edwin's Presentation:** So,

**George Westbrook:** so we need to cut out some of the confirmation.

**edwin's Presentation:** like I'm I'm No,

**George Westbrook:** Um cuz

**edwin's Presentation:** no, no, no. I mean, I'm just telling you like so when when if you're watching a game and you're going to be buying and selling

**George Westbrook:** I've

**edwin's Presentation:** the team, okay, and you you have to be able to stay on the same page where the buy sells live and you're watching, you click buy and it shows long and you're watching, you're nothing changes. You click sell and you're out like you know I can give you a demo but like you know the uh the um the the way actual people want to trade is they don't they don't go through a bunch of hoops to place them or to cancel them or to you know go back and forth. Similarly like I mean I had planned on doing this today. We'll see if I feel like it at later but basically um you I want to have like a game page a live page like we had you know all the games yesterday playing live and um when we do that I want to be able to um you know essentially have you know the team up there and the data.

### **00:30:43**

**edwin's Presentation:** I I'll show you but I mean I I'll be honest with you guys. I appreciate all the like we'll get him stuff and all that. I I I'm very concerned. So, you know, it's hard for me to want to put a lot of money towards everything right now knowing that like the way I look at is like after yesterday my my belief and my I could be wrong. Okay, this is my perspective. We don't have any users. We don't have any advertisers. We have we don't have technology that's comparable or that people are going to want to use. What do I have? Like what what you know what what am I actually doing here? You know, I I'm I'm I'm $6.6 million into this at this point. And oh, I've got an idea and that's about it. So, um yeah, it's just it's, you know, I got to decide what I want to do with the

**George Westbrook:** I think what we need is in terms of the trading experience um because I appreciate you saying it's bad is I think we just need every single thing note it get it sorted um like say for example here are you wanting just rather than you look are you looking at the screen Edwin

### **00:31:59**

**edwin's Presentation:** Uh, yes. Let me blow in real quick.

**George Westbrook:** Yeah.

**edwin's Presentation:** Yeah. So, there's too many clicks here, right?

**George Westbrook:** Okay.

**edwin's Presentation:** So, so,

**George Westbrook:** Cuz I thought what we've got that review confirm.

**edwin's Presentation:** so yeah. Yeah.

**George Westbrook:** We just want one

**edwin's Presentation:** So like here, well go back if you can. Okay,

**George Westbrook:** click.

**edwin's Presentation:** I'll show you what I mean. Okay, so uh go okay. So right here, right? Um what was happening last night is let's say I wanted to hit buy and I I would sell something. Okay, and then I want to cover it right away. And then as soon as I would like it it the like it wasn't matching my buy order to actual like prices. So, it put me back to a weird price and then I would have to type in the price. I would have to f\*\*\* around with that. Then I would have to type in the quantity and by the time I did all that, the trade had gone.

### **00:32:54**

**edwin's Presentation:** Okay. And I show you my screen for just a second. Let's see if mine even works. set my f\*\*\*\*\*\* clad. Let me see

**Jared Sapirman:** Edwin, I think that's because the uh the order book wasn't matching the

**edwin's Presentation:** here.

**Troy McDonald Kane:** That's right. It wasn't.

**Jared Sapirman:** quotes

**Troy McDonald Kane:** That was It was out of sync for a lot of the Midame. At least for me, it was where I would look at the order book and I would go to make a trade and the order and

**Jared Sapirman:** the whole time.

**George Westbrook:** Yeah,

**Troy McDonald Kane:** the trade ticket quotes were not synced. They were off.

**edwin's Presentation:** Right.

**George Westbrook:** that

**Troy McDonald Kane:** And then I go back order book and I'm like,

**George Westbrook:** was

**Troy McDonald Kane:** that's why I missed the market because order book was not synced with the order ticket.

**edwin's Presentation:** Correct. Yeah. Yeah.

**George Westbrook:** X now.

**edwin's Presentation:** I had say Okay, let me do let me figure out

### **00:33:34**

**Jared Sapirman:** And because there's no market order, you couldn't even actually buy that.

**Troy McDonald Kane:** Yeah.

**Jared Sapirman:** I I don't know where the market order is,

**edwin's Presentation:** how.

**Jared Sapirman:** but I think that's pretty

**George Westbrook:** there there at the moment there isn't there isn't a market order I think that

**Jared Sapirman:** imp

**George Westbrook:** was always on the let's get that added in it's just not been added in

**edwin's Presentation:** Can you fool see my screen?

**George Westbrook:** yet

**edwin's Presentation:** Cool.

**Troy McDonald Kane:** Yeah.

**edwin's Presentation:** All right. So, let me get through this real

**Kevin Murray:** Yeah.

**Jared Sapirman:** George, is that possible to add it

**edwin's Presentation:** quick.

**Jared Sapirman:** in?

**Troy McDonald Kane:** Weed will create a synthetic market order. T0 does not support market orders. Equity markets do not support market orders. They're all on the broker side.

**edwin's Presentation:** Okay. So,

**Troy McDonald Kane:** Yeah.

**edwin's Presentation:** I'm just going to go ahead and tell me when I can go go by.

**Troy McDonald Kane:** Go ahead.

**Jared Sapirman:** Okay.

**Troy McDonald Kane:** I'll go Edwin.

### **00:34:19**

**Troy McDonald Kane:** It's fine.

**edwin's Presentation:** Great. All right. So, George, you see here this live market here where it's like a bid offer.

**George Westbrook:** Mhm.

**edwin's Presentation:** What I've done here is I put a one-click trading. You see this box here? I can click that. So, if I don't have it on,

**George Westbrook:** Mhm.

**edwin's Presentation:** I click buy and I get the ticket and it gives me what I want there. Okay. The way that I have this set up is I I have multiple order types. You can do again it's a synthetic market order, but it's the public doesn't know what that means. So you just put market and that's basically you pick a price way above the bid ask and you fill it or you know or one way or the other. The other is you can join the bid, you can go to the mid or you can go to the ask. I'm going to show you what oneclick trading is. Okay. So like right now you see on the bottom let's trade a little bit bigger.

### **00:35:08**

**edwin's Presentation:** I hate 100 lots. So on the bottom it's like I got 70.6 whatever bottom left. You see that a th00and at market. Is it too small or can you see it? next to the buy button.

**George Westbrook:** Yeah.

**Brett StClair:** Oh yeah,

**edwin's Presentation:** Okay, cool. So, like right now I want to buy. Okay, I just put an order in. Now I'm long. Okay, and now I'm I'm I'm likely going to buy another one. I'm working that bad boy filled and now I'm I'm up money and I just want to hit I'm going to cancel that. Okay, really took a deep dive there. Wow, look at that. Um but let's say I want to hit flatten. Okay, so I'm long 2,000, but I want to get out. All I do is hit that button. Okay, and there I'm out. Now, let's say I want to get back in. I click again. I'm I'm constantly being able to buy and sell very quickly.

### **00:36:00**

**edwin's Presentation:** There's another order. Okay. So, if I want to if I want to sell or if I want to keep buying, you know, I got I'm I'm one click touching. Now, you can see I'm long 2,000. I'm going to click again. There. I'm now long 3,000. Okay. So, now I'm watching this thing trade. Whatever. I go to flatten. Give me some P\&L here. Some juice, please. And uh let's get a little green. Give me a little green. More than that. gave me a little taste, but not a not a big taste. Little more, please. Nope. Little. So, I'm going to just hit flatten there. And now I'm up money. So, that's how fast you got to be. You got to be able to like buy and sell very, very quickly, you know? Notice I don't have the the toggles up. It's not taking me anywhere.

### **00:36:52**

**edwin's Presentation:** And I'm just hitting buy or sell. And you know, the buyer and seller just f\*\*\*\*\*\*

**George Westbrook:** Yeah.

**edwin's Presentation:** loaded right here and it stays on Dallas. And so like and and it's loaded right now. So I can just hit buy right now. And look at the bottom. I'm long again. Okay. So I'm I'm back to being long. So even though I don't have to go to special spot, I've got the buy and sell ready to go at every time, every page. If I go to the team page, it's there. If I go to the company page, it's there. and my P\&L thrives uh you know survives each each layer because I want to be able to to constantly be trading the product especially if I'm like researching s\*\*\* or whatever you know it's it's that that that being able to you know go ahead and and knock that out is uh you know it's critical like I mean like I said I I you know I'm trading as we talk here and and you know it's I I'm not I'm making one click so like there's a ladder.

### **00:37:51**

**edwin's Presentation:** So, I'm trading the S\&P 500 right now and I'm trading a ladder and um like right now I just made four trades by four clicks of a button and now I'm in the market and I'm going to get those filled and I'm going to try to cover them. I'm filled and I'm going to try to buy them back and I am working them. So, one more.

**Brett StClair:** question.

**edwin's Presentation:** There we go.

**Brett StClair:** I'm quite curious to see how the game casting screen works in this environment because that's also important, right? To have the

**edwin's Presentation:** It is, but it's less important than you think. Okay, the gamecast is great if you're trying to understand things that you can't understand through

**Brett StClair:** similar

**edwin's Presentation:** TV, but like generally speaking, the price moves will be moving in line with Gamecast. So, Gamecast gives you information, but doesn't give you like a substantive substantive edge to trade it. The trading is the trading like it's it's you know it's not a golden ticket that you you're going to be a winning trader because you got gamecast.

### **00:38:55**

**edwin's Presentation:** You may become more informed. Okay. But the actual ual trading comes down to like whether or not you can buy and sell and and make money in the market. Okay, I just made a bunch of money. It went my way. Thank you, Lord. Thank God for that. So, um in the real market, not in this b\*\*\*\*\*\*\*. So, like that at the end of the day, like the trading aspect, this is the number one thing that matters, being able to trade incredibly quickly. If we go to the pro section and we go to a live game. Okay, notice I've got this on the bottom here. This buy sell. Let's go ahead and load up so we can trade thousands. Okay, so let's go back to the game. So here would be the live game we were watching last night. Let's buy 5,000. Okay, now we're long. Now I'm going to sell 5,000. Now I made 197 bucks there.

### **00:39:48**

**edwin's Presentation:** I'm going to buy another 3,000 there. Come on now. Get a little more. Went against us. Now we're up a little bit more. Keep going. Boom. Boom. Boom. Flat. And I sold one extra. Now I cover there. Now I'm up 1,800 bucks. That's how it's going to be. You see how it's like it's not clunky at all. You're watching the game cast. You're just buying and selling as the plays go on. Let's buy another,000. Sold. Now, now wait a minute.

**Brett StClair:** How would you switch?

**edwin's Presentation:** Now we're up 2,000. That's how fast it has to be.

**Brett StClair:** How would you switch teams like from here?

**edwin's Presentation:** You can swipe.

**Brett StClair:** Like how's your thinking?

**edwin's Presentation:** So, I've got it where you can swipe the the field and it'll go

**Brett StClair:** You swipe to field control. Oh, I see.

**edwin's Presentation:** to it goes to different live games.

### **00:40:28**

**Brett StClair:** And then it goes to different games. And then how do you pick the the the side you want to trade?

**edwin's Presentation:** Correct.

**Brett StClair:** I'm just curious on that.

**edwin's Presentation:** Look at the look at the top.

**Brett StClair:** Yeah.

**edwin's Presentation:** Um, okay. The top will tell you who you're trading.

**Brett StClair:** Yeah.

**edwin's Presentation:** So, if you want if you want to go that you you know you you they'll always start on the home team. So,

**Brett StClair:** Oh,

**edwin's Presentation:** there's Kansas City.

**Brett StClair:** there we go. Okay. Got it. Yeah. Yeah. Okay.

**edwin's Presentation:** Okay. Now, if you want to go back,

**Brett StClair:** So then that's how you know

**edwin's Presentation:** you just go to markets. You go to NFL.

**Brett StClair:** Yeah.

**edwin's Presentation:** What team you want? Like, okay, I want um Houston Texans. Now, you got the Texans. You go into Pro. You go to your explore live game, watch live. Now, you got the Texans.

### **00:41:12**

**Brett StClair:** Okay, I got

**edwin's Presentation:** So,

**Brett StClair:** it.

**edwin's Presentation:** you see like how the the the like the flow of making trades is simple. Right? Like because all I want to do is I want to watch the game and I want to buy in some and I want to do it in a way that's simple like that. The simpler the better, you know, and we've got all the detail down here. People can go in here, right? Like you go down here, you can look at the win probability versus the um the share price and you'll notice they deviate, you know? So that's where you can get some type of uh you know data down here. You can go down to the playbyplay. We can look at all these different things that are happening and we can pull that that that info in from Sport Radar. If you want to look at the game stats, you click here. and K. You don't know who's got more yards or who's who's out passing. You got all that s\*\*\*.

### **00:42:04**

**edwin's Presentation:** So, it's anything you want is within this little cockpit. But the most important thing people want is to be able to trade. That's it. So, let's go ahead and we'll sell another sell a thousand

**Brett StClair:** We're going to run with this. We're running with this. We got a better idea how it works now.

**edwin's Presentation:** here.

**Brett StClair:** I see exactly how you how you're working, right? It's slick. It's just like

**edwin's Presentation:** So,

**George Westbrook:** Yeah,

**edwin's Presentation:** there we go.

**George Westbrook:** cuz I think in terms of like

**edwin's Presentation:** We just made 1300 right there. You see that? Nothing happened.

**George Westbrook:** the

**edwin's Presentation:** Houston went up six to nothing. I shorted them because they didn't score a touchdown. We made 1300 bucks. So like that's that's how this should work. It should be as simple as possible, you know, because of buy and as soon as you enable the one-click trading,

**Brett StClair:** Is there one trading here as well?

**edwin's Presentation:** like if I go back here.

### **00:42:51**

**Brett StClair:** Right. You try to have it on every screen where you're going to enable it,

**edwin's Presentation:** Yeah.

**Brett StClair:** right?

**edwin's Presentation:** So the the trading's on everything, Brett.

**Brett StClair:** Yeah.

**edwin's Presentation:** It's always on.

**Brett StClair:** Sorry.

**edwin's Presentation:** So like now it I took off I took off the one-click trading.

**Brett StClair:** The one click trading.

**edwin's Presentation:** Okay.

**Brett StClair:** Yeah.

**edwin's Presentation:** And now here it comes up with a confirm. So some some guys don't I'm

**Brett StClair:** You confirm a hover over. Okay.

**edwin's Presentation:** sorry.

**Brett StClair:** It confirms a hover over rather than entire screen takeover. Okay. Got it.

**edwin's Presentation:** Yeah, it's a hover event.

**Brett StClair:** Got it.

**edwin's Presentation:** Then you just hit confirm. There you go. Now I bought 100\. Let's sell it.

**George Westbrook:** If you wanted to edit that order,

**edwin's Presentation:** Boom.

**Brett StClair:** Yeah.

**George Westbrook:** how would you do it if you're on the Gamecast?

**edwin's Presentation:** So that is a challenge, right? So number one, you can do it through here.

### **00:43:30**

**edwin's Presentation:** So you've got your position. Okay. Um and basically I've got to just sub submit market orders for demonstration. But you can say okay if I like ultimately we want to say if you're on the bid side, you want to work the bid. Okay. So you click and it will work only bid orders. And then um like here here's what I put in here, George. If I go to market, if I go to the bid price here and let's say I'm going to buy um see this price toggler, I'm moving the price down. So it's bid and I'm going to bid below. Okay. So now I've got a working order at 53.88, 50 cents lower than this.

**George Westbrook:** So if you if you so if you go to the game

**edwin's Presentation:** So that allows me to do the press.

**George Westbrook:** cast and what was it?

**edwin's Presentation:** Yeah.

**George Westbrook:** Is it the Browns versus the Texans? Getting the names right finally.

**edwin's Presentation:** Yes.

**George Westbrook:** So let's say here what you're on Texans.

### **00:44:28**

**George Westbrook:** Let's say you wanted to let's see how many clicks. So you want to grade the Browns. You don't want it to be a market order. You want it to be a limit order and you want to change the quantity. How would you how would what would the process look like from

**edwin's Presentation:** So, I would put the same thing that's in that market page in this area where it's your your Houston

**George Westbrook:** here?

**edwin's Presentation:** position. So, I would I would add it to the right side. I just haven't done that yet.

**George Westbrook:** Okay.

**edwin's Presentation:** Yeah. So,

**George Westbrook:** So the market so the the kind of order placing thing would be on both those

**edwin's Presentation:** the or yeah, you'd have the ability to do both,

**George Westbrook:** pages.

**edwin's Presentation:** right? Like you could do it on the market page because once you're in the gamecast and you're watching a game, you're not going to go to the markets page cuz you you're seeing the the Houston price here, right? You don't need a dynamic market book uh order book on this page.

### **00:45:23**

**edwin's Presentation:** You're just watching the game and this game's just about over.

**George Westbrook:** So could we have so iron cell buttons is linked linked to one team then so it allows the one-click trading but also rather than having let me just share so rather than clicking trade in in the current version There's a persistent buy and sell. Maybe we have a swipe if you want to go from one team to the next team. There's also a swipe up. So that rather than having that market with the call it the order input, the more complex market uh order input just wherever you are on any tab on any on any team on any game, you can click the buy and sell. You can go up and expand wherever you are into changing that. So if you wanted a limit at the um ask or you wanted it at the mid, you could do that um rather than having that that rolling. But I think the the one click trading I think I think that's where maybe where we've been going and where your your head's been going has diverged because we've always thought it was we let's fix the fat fingers.

### **00:46:37**

**George Westbrook:** Let's make sure that there's space for advertisers. Let's make sure that there's something that can be shared for users so that we can help for growth. But obviously now we know that we don't want that. What we want one click trading as much as possible. Um that that's really

**edwin's Presentation:** Well, again, listen, this is for the people who are going to be active traders.

**George Westbrook:** helpful.

**edwin's Presentation:** like you know some we had uh interns like well I don't like oneclick trading okay see you at the poor house um but uh you know

**George Westbrook:** Was that the poor house or the whole house?

**edwin's Presentation:** so we put the probably both one he's he's working at and the other one he's crying at. Um, but nonetheless, the uh, you know, the the one-click trading is, you know, the the the way people who want to try to be actively engaged, that's how they do

**Jared Sapirman:** George,

**edwin's Presentation:** it.

**Jared Sapirman:** is this oneclick trading something that we could put in the settings like under the more and then have that

### **00:47:39**

**George Westbrook:** Ex. Yeah.

**edwin's Presentation:** No,

**Jared Sapirman:** go throughout the entire

**edwin's Presentation:** I wouldn't do that, Jared. Please don't. I want it to be just like I have it here. Okay. It's real f\*\*\*\*\*\* simple, bro. One click trading here. One click trading off. That's what I want. I don't want it in the f\*\*\*\*\*\* more. None of that s\*\*\*. Okay.

**George Westbrook:** But does that change oneclick trading for all trading across the whole application? or does it only change it for this

**edwin's Presentation:** Correct. The the the whole

**George Westbrook:** team?

**edwin's Presentation:** application.

**George Westbrook:** I don't know where to put

**edwin's Presentation:** Dope. Yeah. So,

**George Westbrook:** that.

**edwin's Presentation:** the the idea is if someone's a one-clicker, they're going to want to click it once. That's it. If they're not, great. I mean, the people who are not going to be the, you know, one-click traders, they're not going to be active traders.

**George Westbrook:** But then I suppose this may be for a later point but maybe the one click traders initially are going to be 20 30%.

### **00:48:39**

**George Westbrook:** So I think we need to think about how we're going to transition people from starting out or not starting out but like halfway there to getting to that point. Um I think that oneclick training button that that's definitely going to help. Um so you can turn it on and turn it off.

**edwin's Presentation:** Well, we're going to have a a video that says, "Hey, you know, my goal is to have every one of these surfaces have a instructional video on it, you know, within the app and like on social media and all the YouTube b\*\*\*\*\*\*\* and everything else these these people like to to waste their f\*\*\*\*\*\* time on. Um, you know that we will give them everything they need because I've heard he for you know I've done a ton of these demos with you know non-traders. I've done a bunch. Okay. And uh you know, people are everyone's like, "Well, this is what people want." And it's like the next person's like, "I hate that." You know, it's just like everyone f\*\*\*\*\*\* knows that.

### **00:49:34**

**edwin's Presentation:** I know what people are going to use for trading. I trade for a living. I've been doing it for 30 years, okay? I I know what people are going to use. I've been gambling since I was in third grade. I know how people bet. Um, you know, I I know what they're going to want to do. Where we're going to make our money isn't on the fatties, the the the the like 50% who come on the app once a week. We're going to make our money on the the 30% of the people who are addicted to like the action and the the ability to trade like this on sports because like even on Kelsey and things like that, it's very, you know, problematic, you know. And then I'm going to give you I'm going to give you just one comment, George. I know you're like, Kel, she had 48,000 engineers and all the rest of it. These trading systems, they are commoditized, okay? There's no edge in the trading system.

### **00:50:28**

**edwin's Presentation:** Now, I've asked you guys to build a lot in a little bit of time, okay? And that I can respect, but you're capable of f\*\*\*\*\*\* doing it. So, and the whole team has done a good job up to this point, but at this point, I still have to decide if I want to if I want to continue putting money or or start putting money into the advertising on something that's not like what I want in the market. Cuz like if I went to market and again, obviously, it's a dry run. I'm not a f\*\*\*\*\*\* lunatic that last night like it's going to make me, you know, be like, "Oh my god, the sky is falling." I just I can tell you like I know how far we are away. Okay, so like, you know, I've been in this technology game. I've been burned by more f\*\*\*\*\*\* technologists than I could ever, you know, describe. Gary, are you on the f\*\*\*\*\*\* call?

**Gary Anderson:** Yes, sir. I am here.

**edwin's Presentation:** How much money did I lose with Ed Edwin Savu?

### **00:51:27**

**Gary Anderson:** Well, I don't know. You got to be I don't know, six mil or something. I know it's a lot. I know. I took a beating,

**edwin's Presentation:** Yeah.

**Gary Anderson:** too. So, yeah.

**edwin's Presentation:** So, we've been through this a couple of times. So, you know, I we just have to make sure we're in a position that we can win. And, you know, we're we're we you know, we'll we'll we'll come to some resolution here in in the next little bit of time. I just need to figure out what I want to do. But that's how this is how the app would function in my my mind's eye. You guys done looking at this

**George Westbrook:** Yeah, can you can you send all of over that as well? Um really really helpful.

**edwin's Presentation:** s\*\*\*.

**George Westbrook:** Um just yeah, it's two weeks before so we we'll be a in terms of UI most of that's going to be going to be possible. um like everything on the back end's working as expected.

### **00:52:21**

**George Westbrook:** UI isn't a good thing. Um obviously the best thing would be they would all work in um if there was

**edwin's Presentation:** Yeah. Well, I didn't show you. I don't know if I showed you this. Let me go back to this real quick. I'm gonna do it real fast.

**George Westbrook:** any

**edwin's Presentation:** Continue. Start broadcast. This is the uh the money maker. Sweet George.

**George Westbrook:** What? Oh,

**edwin's Presentation:** This is this this is the money maker.

**George Westbrook:** there.

**edwin's Presentation:** So, um this is the thing where you can type in any strategy you want and test whether it makes money. So, we'll just pick any random one. This one is sell after every home touchdown cover eight plays later.

**George Westbrook:** Uh, is is this the thing we spoke about ages ago with the getting the AI to create the

**edwin's Presentation:** Okay.

**George Westbrook:** strategy, run the strategy, doing it on schedules, things like that?

**edwin's Presentation:** Yes. Um I think it is.

**George Westbrook:** Oh, okay.

### **00:53:31**

**George Westbrook:** Yeah,

**edwin's Presentation:** So you can see

**George Westbrook:** I think we could think that's we we've got that all in the vault,

**edwin's Presentation:** here

**George Westbrook:** but with the UI stuff, that's going to be really helpful putting it into being able to visualize it.

**edwin's Presentation:** right. So like we don't have any advertisers. So the only way we can try to make money at this point is through the subscription. And we see prediction market users, anybody who's involved in taking risk on these games, using this potentially as a way to to to find a way to get a strategy. So, this particular one is the home team. So, I'm on the Florida Gator and the Florida Gator. Um, basically, where's Oh, here it is. I'm sorry. Um, we're going to So, we're going to We ran it on their rule set. Okay. So, the rule set for Florida uh Gators. Now, you can see here the net P\&L from this trade was amazing. They made 6,854 bucks, 20 trades.

### **00:54:28**

**edwin's Presentation:** The win rate 75% amazing. A small max draw down. The average win versus average loss. Great. And versus a buy and hold strategy, it made $7,000 more. Underneath here is every incident that happened. And if I click that button, which I'm not going to do, it'll take me to the replay, which allows me even more ability to find out, you know, you know, what other criteria happened around those plays that got me uh this positive feedback. But instead of just having it on one team, let's just run it off all 138\. Look at that thing makes um $1 million of uh it's always profitable. I don't know this 13 129 out of 138\. It should be now 32, but it'll show you each team's like profitability in this. It's pretty sick. You know what I mean? So, like if you want to go in here and you just want to type in different types of strategies, like for example, let's change this to like um four plays after. And right now, we're at a million one.

### **00:55:39**

**edwin's Presentation:** Let's run it. It only does 93,000. Okay. So, you can you can start to f\*\*\* around with all these different inputs. Let's go to 12, please. And I I built the criteria so that the the words go in there easily. And then if you wait 12 plays, it actually makes more 1.3 million. So this this is something people would pay for, right? And because like they can use it today in prediction markets. So you know we see well people will trade the game. Imagine people being able to do this strategy building during the course of the week. People may spend three, four, five, six hours come up with a strategy for this weekend's games and then if it it's if it's working they put it in the market like this is this is a badass strategy though this one here I mean yeah it's it's great so anyways so yeah that's I want to show you that

**George Westbrook:** But in terms of let's picture a world where trading experience with everything we've got is all

### **00:56:40**

**edwin's Presentation:** thing

**George Westbrook:** sorted. Would you say this this after is number one priority?

**edwin's Presentation:** uh that I'm sorry what Was that question?

**George Westbrook:** So let's if we imagine a world where everything that we've currently got on the app look field feels is working as close to perfectly as possible. Um, this would be the next thing that needs to be built, tested, and deployed.

**edwin's Presentation:** I mean, you know, yeah, I mean, yeah, I think so. I think there's a lot a lot to do there. I mean, that would be great. Um the um what can I do? Um, yeah, I mean that I'd like to sport radar data so I can start building the models around multiple years as opposed to just one year. So let's say that strategy worked for this year, I would like to be able to run it for the last four or five years and have different things that we could start to let people extrapolate. So the idea is like you know the more and more that people can get involved in building what they they think might be their own proprietary strategy and within that once you build the strategy you get to save it.

### **00:57:53**

**edwin's Presentation:** I put in 17 like samples that people can try and then they can build their own. And this is the same thing I've done with real trading by the way. You know, I've I've done the same, you know, thing where you you basically you can test how orders would behave um you know, in real market conditions.

**George Westbrook:** Okay. So I think yeah I I get that that's number one priority after what we need is I say list of feedback that we can get on to like now um Jared's really really helpful any screenshots really really helpful obviously got the got the prototype if we can have the the latest version that would be good um in terms of changes live I know we said let's not do any changes live only thing I'd like to say is is if we are doing changes live if we put the note in Slack say this is happening that's happening blah blah blah um and then you swipe up twice reload it and then confirm that the change is there um is that something we could potentially do because otherwise it's kind of we get one shot before there's no iteration in between times and effectively what what could turn into three attempts at different games to show iterations turns into one

### **00:59:21**

**edwin's Presentation:** Yeah.

**George Westbrook:** go

**edwin's Presentation:** I mean, why not? I mean, you know, I I'm not Yeah, I mean, sure. Yeah, we could do that.

**George Westbrook:** because I think I I think at the start like at the start the live game page it wasn't showing positions it wasn't

**edwin's Presentation:** I think

**George Westbrook:** showing it wasn't showing working orders it wasn't showing this it wasn't showing that um which was a fix that was pushed like I think it was slight piping issue where if it wasn't the data wasn't there it wouldn't show it as Um that was fixed before the start of the first game, albeit about 2 minutes before. So not f\*\*\*\*\*\* ideal timing. Um but things like that we can go bam done. Like you like you know, refresh. Is it there? No, it's not. Refresh again. Refresh again. Then we get that cadence a lot quicker cuz like I said, we got two weeks. We've got maybe let's have a look at the schedule. We got the 21st.

### **01:00:22**

**George Westbrook:** 21st is 21st. 20 22nd is when NCAA starts, isn't it?

**edwin's Presentation:** No, that's just the IPO.

**George Westbrook:** Oh, the IPO 29th.

**edwin's Presentation:** The actual games start on the 29th.

**George Westbrook:** Okay. So, yeah, we've got we've got tonight, tomorrow, we've got a lot of days to be able to do these to do these draw well, they're not dry runs anymore. Um, actual runs. Um, we know the sports radar playbyplay data is coming through. Um, it's just all data piping on the actual app. um and UI UX changes which is where we can iterate quick quickly like if it's like if it's say the market maker the the spreads too tight that's a it's not it's not a quick fix it can be done during the game

**edwin's Presentation:** Awesome.

**George Westbrook:** um but it means there's 10 minutes of downtime which means 10 minutes less of testing the UX of the testing um so that's where we maybe want to put things like UX oh I want to see the game the aim that's needs to be higher or this needs to happen blah blah

### **01:01:21**

**edwin's Presentation:** Sure.

**George Westbrook:** blah. That's where we can do it quickly. Um unfortunately we got a lot of games where we can test it.

**edwin's Presentation:** All right. Cool. All right. Anything else that we have at the moment?

**Cody Haugen:** Yeah, I mean I would like to clarify a point. Um, so George,

**edwin's Presentation:** Go ahead.

**Cody Haugen:** outside of this recording and all the feedback we've given and then all of the feedback that Edwin has in his um in the version that he's created, what other feedback I mean, do you need do you need us to write I mean recapture it all and and write it out in a word document? I will if that's needed, but it's here in the recording and it's what Edwin

**George Westbrook:** If yeah, if that's in its entirety, that's all we need.

**Cody Haugen:** Harris

**George Westbrook:** If there's any other stuff that's not been mentioned, um I think things like maybe some more granular feedback. So rather it being like the app's slow um it should what would be more helpful for us is when I click this button this happens it shows pending for 3 seconds um if it's like it goes to the wrong page which I know we there specific examples we got like you're on the game cast page you click trade it confirms it then goes back to the IPO page stuff like that's really helpful um because otherwise we're just clicking around every single page trying to find out If okay,

### **01:02:52**

**George Westbrook:** that didn't go where it was meant to go.

**Cody Haugen:** No, no, no. 100%. So, uh, we can definitely do a better job of that live where I can take screenshots or record my screen um like Jared did and and send that through. Um so that's that's good feedback for tonight. So I appreciate that. Um but yeah, I mean as far as the feedback right now, we've we've iterated it through the recording and Edwin has it in his uh example that uh format that he has sent over to you. So moving forward, yes, screenshots, video recordings, that type of thing will be will be done.

**George Westbrook:** Yeah.

**Cody Haugen:** Yep.

**George Westbrook:** Right. I think, correct me if I'm wrong, I think that's I think that's everything. And next run

**Cody Haugen:** Yeah.

**George Westbrook:** tonight.

**Cody Haugen:** Yep.

**edwin's Presentation:** All right, sounds good. Appreciate everyone's time. I got a bolt. Have a good day. If anyone needs me, reach out, please.

**Cody Haugen:** Yes.

**edwin's Presentation:** Thank you

**George Westbrook:** Let's f\*\*\*\*\*\*

**Kevin Murray:** Thanks.

**Cody Haugen:** Good.

**George Westbrook:** go.

**Brett StClair:** Thank you.

**Cody Haugen:** All right.

### **Transcription ended after 01:06:58**

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*