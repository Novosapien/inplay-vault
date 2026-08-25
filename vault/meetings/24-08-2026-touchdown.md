---
date: 2026-08-24
type: standup
description: "Monday touchdown, 24 August 2026: two IPO defects separated, KYC removal as the gate on Thursday secondary trading, the first sold-out book and its position-transfer fix."
source: "Google Meet transcript, Inplay - App - Touchdown (18m 24s)"
scope:
  - "[[ipo-module/ipo-module]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[market-maker/market-maker]]"
  - "[[tzero]]"
  - "[[delivery/delivery]]"
status: extracted
extracted-to:
  - "[[ipo-module/ipo-module]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[compliance/eligibility-and-age-gating]]"
  - "[[market-maker/open-questions]]"
  - "[[market-maker/plan]]"
  - "[[market-maker/sessions/2026-08-24-touchdown-digest]]"
  - "[[app-store-accounts]]"
  - "[[tzero]]"
  - "[[delivery/delivery]]"
---

## Post-Call Analysis

18 minutes, the shortest touchdown in the record, and deliberately so: Troy
noted Brett _"wants these to be 15 minutes, not 30"_. Two days after the NCAA
offering opened on Saturday 22 August. **Edwin did not join** (Troy: _"Edwin will
not be joining the call this morning"_), which is worth noting because it makes
this the first post-offering call with no client-principal steer on it. Present:
Troy, Cody, Jared (InPlay) and George, Brett, Max, Hasan (Novosapien).

The tone was settled and the content operational. Troy closed with _"there's a
couple refinements we want to get done this week, but I think, you know, where
we're at, we've come a long way."_

**The offering produced two separate defects, and only one of them is solved.**
Jared reported that on the **IPO draft page** the teams were **locked**: he could
buy from the markets and trade pages but not from the IPO page itself, and the
same happened for a couple of his friends and some internal testers. Troy
identified the cause as the **TestFlight beta build** rather than the live App
Store build, adding _"we should have made that more explicit"_. Jared
reinstalled **during the call** and confirmed _"the whole problem with the IPO
page is gone"_. **The second defect survived the reinstall:** with **$80,000 of
buying power showing**, an order for a couple of thousand dollars still failed.
The error George read back is the useful part: **_"not enough buying power for
that order. Open orders and shorts holding play dollars."_** Jared owes a video
into the Novo Slack channel and Hasan is checking the account against the KYC
email. George's hypothesis for at least some cases: dry-run firepower that was
allocated and then removed, or older accounts.

Against that, the control group is clean. Cody's friends went through KYC over
the weekend and _"had no troubles at all"_, buying Alabama Crimson Tide shares;
Troy and two of his own friends tested successfully.

**Removing the KYC layer is the single gate on Thursday.** Troy: _"Let's focus on
removing the KYC layer right now. That's the highest priority right now is to get
that lifted as fast as possible."_ The sequence he set out: **the IPO window
closes Wednesday night, secondary trading starts Thursday, and there are no games
until Saturday.** The two-day gap is deliberate, _"in case anything was wrong, it
wasn't fully visible to the whole universe yet."_ George had already said the work
is _"not a turn it on"_ job but would be done _"over the next day or two"_.

**The IPO book was shared on screen, and it shows Edwin buying through the
taker.** George walked through it: shares offered, shares sold, and shares bought
by the public, where **the gap between sold and bought-by-public is what Edwin has
manually ordered through the taker**. That confirms the manual-execution behaviour
forecast on 17-08.

**One team has sold out, and George already has the fix.** The **Florida Atlantic
Owls** sold out, which leaves the maker _"nothing that it can do the two-sided
quotes for"_. He called it _"not a huge issue"_ because most of that stock was
bought by the taker, so the answer is a **position transfer from the taker back to
the maker** to restore the inventory it needs to quote both sides. Worth
recording as a real event rather than a crisis, and worth checking how many other
books are close.

**Troy corrected a shorting misunderstanding, and the correction matters.** George
had it backwards. Troy: _"There's no limit on the shorts in the simulation. There's
a limit on the shorts in production."_ An **additional million shares per team is
eligible for shorting**, so a million long and a million short. Edwin is trying to
**emulate the production constraint** by having the market maker acquire a portion
of the shares to loan out, but that is _"not a fully functional need right now
because T0 has bypassed that to allow up to 100% of shorts against the longs"_ by
**turning the locate flag off**. Troy: _"we'll have to confirm how that would
work"_, and it goes into the **tZERO call tomorrow**.

**New standing requirement: a daily IPO purchase report.** Troy asked whether
individual accounts can be identified. They cannot from the IPO book view George
shared, but he can produce a report: _"it would be good to get a daily report of
anyone that bought IPO shares throughout the process each day if possible."_

**The Sportradar college-football futures endpoint is still broken, and it is
holding up the market maker.** George needs it for expected wins. Cody chased
twice over the weekend after being told the bug would be fixed _"late Wednesday,
Thursday sometime"_, and got no reply either time: _"I'm getting very pissed off…
it's a product that we're paying for."_ He will phone Scott regardless; George
will re-check the endpoint. His workaround is a **CSV pulled from a different data
provider through a contact**, the same route used to get the IPO numbers, and it
**decays in about five days** because futures move with results: a team projected
five and nine that wins its first three games gets marked up.

**The test-ticker blocker is lifting, and George explained exactly why it
mattered.** Until now there were **only ten test tickers**, so replay testing was
possible but a **replica test during live games was not**. tZERO will provide a
**full replica of all the test tickers**, so a change such as _"a new maker so
that it's got five levels instead of three"_ can be tested **while live games are
running, with zero effect on any users**.

| Finding | Destination | Action |
|---------|-------------|--------|
| IPO draft page locked on the TestFlight build; live App Store build fixes it, confirmed live on the call | [[ipo-module/ipo-module]] | Update written |
| **Separate** buying-power failure survives the reinstall: "open orders and shorts holding play dollars" against $80k | [[ipo-module/ipo-module]] | Recorded, open, video owed |
| Control group clean: Cody's and Troy's testers bought without trouble | [[ipo-module/ipo-module]] | Recorded |
| No logo or name change; it triggers a new review. All store changes held until the Viral kickoff, tomorrow | [[app-store-accounts]] | Update written |
| **KYC layer removal is the highest priority.** IPO window closes Wednesday night, secondary opens Thursday, no games until Saturday | [[customer-onboarding/customer-onboarding]], [[compliance/eligibility-and-age-gating]], [[delivery/delivery]] | Update + G1 note |
| IPO book: the gap between sold and bought-by-public is Edwin buying manually through the taker | [[ipo-module/ipo-module]] | Recorded |
| **Florida Atlantic Owls sold out**; maker has no float to offer | [[market-maker/open-questions]], [[ipo-module/ipo-module]] | New N53 |
| **Fix already proposed: position transfer from the taker back to the maker** | [[market-maker/open-questions]] | Recorded inside N53 |
| Shorting corrected: **no limit in the simulation, a limit in production**; 1m extra shares per team shortable | [[market-maker/open-questions]], [[tzero]] | T16 and E26 updated |
| tZERO turned the **locate flag** off, allowing shorts to 100% of longs; confirm on tomorrow's tZERO call | [[market-maker/open-questions]], [[tzero]] | Recorded, unconfirmed |
| Edwin emulating the production short constraint by having the maker acquire stock to loan out | [[market-maker/open-questions]] | Recorded |
| **Daily report of every account that bought IPO shares**, George to build | [[ipo-module/ipo-module]], [[delivery/delivery]] | Requirement written |
| Sportradar NCAA futures endpoint still broken, chased twice with no reply; needed for expected wins | [[market-maker/open-questions]] | New S12 |
| CSV workaround from a second provider, decays in ~5 days as futures move with results | [[market-maker/open-questions]] | Recorded in S12 |
| **Only ten test tickers today**, so no replica test during live games; tZERO to supply a full replica | [[market-maker/open-questions]], [[market-maker/plan]] | T17 advanced |
| Closing objectives: IPO working for new users, NFL same process, Thursday secondary, SR dates, app iterations | [[delivery/delivery]] | Recorded |
| Brett wants touchdowns at 15 minutes, not 30 | Not applicable | No action |

---

Aug 24, 2026

## **Inplay \- App \- Touchdown \- Transcript**

### **00:00:06**

**Max Kingaby:** I have to the power to let people in.

**George Westbrook:** actually look

**Brett StClair:** Morning.

**Max Kingaby:** I know.

**George Westbrook:** like

**Brett StClair:** Morning.

**Cody Haugen:** Good

**George Westbrook:** f\*\*\*\*\*\*

**Cody Haugen:** morning.

**George Westbrook:** headphones. I can't hear anything. Have you got your head headphones in? What happens when you get to the age of 50? Right. Mine's working now. Technical difficulties.

**Cody Haugen:** As a tech company, it's always good

**George Westbrook:** Yeah.

**Troy McDonald Kane:** It's always someone that starts off with a tech issue.

**George Westbrook:** Love that. It's It's when you're like the first few calls somebody like,"Yeah, trust us to build this thing for you." How do you get your headphones to connect to Google Meet? Always happens.

**Cody Haugen:** Boys without

**George Westbrook:** It's Brett

**Troy McDonald Kane:** Um, Edwin will not be joining uh the call this morning,

**Cody Haugen:** fail.

**Troy McDonald Kane:** so we can get started whenever you guys want to kick us

**George Westbrook:** indoctrin.

**Troy McDonald Kane:** off.

**George Westbrook:** Sorry. There we go.

### **00:01:46**

**George Westbrook:** Um, yeah. So I suppose IPO from from your side how feelings I think the only thing that obviously we've seen is that non KYC um being an issue which is something which is not a turn turn it on. Um there's a bit of work going into it but we'll we'll be getting that done over the next day or two.

**Troy McDonald Kane:** There were some issues with Jared's account not being able to buy additional shares due to buying power, you know.

**Jared Sapirman:** Yep. Yeah,

**Troy McDonald Kane:** Yeah.

**Jared Sapirman:** there were quite a few issues with my account. Actually, I just talked to Ron. He also had a problem where on the IPO screen itself, you can't buy these teams. You in on the trade page, you can in the markets page, but when you go to the IPO page where it says uh IPO draft, I don't know if you can see right there, it's locked. So,

**George Westbrook:** Okay.

**Jared Sapirman:** you can't buy these from this page or

**George Westbrook:** Are these are these accounts of internal testers or are they like

### **00:02:47**

**Jared Sapirman:** or well,

**George Westbrook:** actual actual users?

**Jared Sapirman:** it work. Yeah, for a couple of my friends, yeah, they couldn't do it either.

**George Westbrook:** Okay.

**Jared Sapirman:** Um if this is also for Yeah. and a couple internal

**George Westbrook:** Okay, the internal testers that that makes sense.

**Jared Sapirman:** testers.

**George Westbrook:** Um because it's where where we've been say doing a dry run and we allocate fire power then we get rid of it. Um, even maybe some old users where they like so were these people that signed up like day of the IPO or late last

**Troy McDonald Kane:** The other the other thing too that they may not have done and I don't know if is you have to delete the

**George Westbrook:** week.

**Troy McDonald Kane:** test flight version and reddownload the the actual version that's live and sign in to through the account that you have that you did the initial setup for KYC. So if you're trying to do it through the test flight app,

**Jared Sapirman:** Okay.

**Troy McDonald Kane:** yeah, it wasn't wasn't going to work because that was the that's the beta version.

### **00:03:47**

**Troy McDonald Kane:** But if you so you had to delete that. We should have made that more explicit, but if anyone that was a tester, you had to delete it out of test flight and then redownload the version that had been approved by the app

**Jared Sapirman:** Okay.

**Cody Haugen:** Yeah,

**Troy McDonald Kane:** store.

**Cody Haugen:** because for what it's worth, the uh handful of buddies that I was able to uh wrestle away for maybe too many beers and and actually go through KYC this weekend, they had no troubles at

**Troy McDonald Kane:** Yeah,

**Cody Haugen:** all.

**George Westbrook:** Perfect. That's

**Troy McDonald Kane:** same with I was testing it a few times as well and uh and I I had two friends

**Cody Haugen:** Yeah.

**George Westbrook:** good.

**Troy McDonald Kane:** test it over the weekend

**Cody Haugen:** Yep. So,

**Troy McDonald Kane:** too.

**Cody Haugen:** they they uh bought themselves some shares of the the uh Alabama Crimson

**Troy McDonald Kane:** So Jared, I wonder were you trading through the test flight app or were you trading through the full

**Cody Haugen:** Tad

**Jared Sapirman:** potentially.

### **00:04:34**

**Troy McDonald Kane:** app?

**Jared Sapirman:** I'm going to redownload it and see if uh changes it.

**Troy McDonald Kane:** Yeah.

**Jared Sapirman:** And also another thing that we had talked about in the Slack um was changing the app

**Troy McDonald Kane:** Okay.

**Jared Sapirman:** logo and the app name if that's possible.

**George Westbrook:** It might that's not a a quick one because I think it's got a Hassan knows more than me more about this than me, but it's like new review. It might even be a new like whole app. I don't think it's that.

**Brett StClair:** It is.

**George Westbrook:** Um,

**Brett StClair:** I think it is.

**Cody Haugen:** Yeah, I would say let's let's hold off on making any app store changes until we have this call with Viral

**Brett StClair:** George.

**George Westbrook:** but

**Cody Haugen:** App. So, we've uh our kickoff call is tomorrow. Um part of our package with them is App Store optimization. So, let's let's not any Yeah,

**Brett StClair:** Yeah, let's take that.

**Cody Haugen:** let's take Yeah,

**George Westbrook:** stop jumping up and down, please.

**Cody Haugen:** let's not let's not jump off any cliffs quite yet.

### **00:05:29**

**Troy McDonald Kane:** Yeah. Yeah.

**Cody Haugen:** Um,

**Troy McDonald Kane:** Let's focus on removing the KYC layer right now.

**Cody Haugen:** yeah.

**Troy McDonald Kane:** That's the highest priority right now is to get that lifted as fast as possible.

**Cody Haugen:** Yep.

**Troy McDonald Kane:** Um because we're going to have obviously secondary trading starts Thursday. Uh the IPO window closes Wednesday night. We would really like that layer to not be there for secondary trading to kick off on

**George Westbrook:** Yeah.

**Troy McDonald Kane:** Thursday.

**George Westbrook:** Yeah.

**Troy McDonald Kane:** Even though there's not games until Saturday,

**George Westbrook:** I think

**Troy McDonald Kane:** we want to have we wanted to have a couple days again just so that in case anything was wrong, it wasn't fully visible to the whole universe

**Jared Sapirman:** Okay, so Troy,

**Troy McDonald Kane:** yet.

**Jared Sapirman:** I just re downloaded the app and the whole problem with the IPO page is gone,

**Troy McDonald Kane:** Okay.

**Jared Sapirman:** but my buying power is remains where I have 87

**Troy McDonald Kane:** Okay.

**Jared Sapirman:** $80,000 available and I'm trying to order maybe a couple thousand and I can't do it for Any team?

### **00:06:28**

**George Westbrook:** Are you able to join the call on your phone and then show us your screen if that's all right,

**Hasan Ahmed:** you join the call. That's right.

**George Westbrook:** please?

**Jared Sapirman:** Sure.

**Hasan Ahmed:** Yeah. Um and I was going to ask, are you able to give me the actual email you're the KYC with?

**Jared Sapirman:** Uh, yeah, I think it's my inplay email.

**Hasan Ahmed:** by email. Okay. Um,

**Jared Sapirman:** Yeah,

**Hasan Ahmed:** I'll I'll just check your account quickly and just make

**Jared Sapirman:** it is.

**Troy McDonald Kane:** I mean the good news is if there were and Cody or well maybe not Cody I guess Novo team how can we see who's actually traded the IPO shares

**George Westbrook:** So, let me I'll share this quickly. So what we've got here is basically like the IPO book. So obviously how many was offered. I mean that's pretty simple. It's the same for everyone. How many have been sold and then how many have been bought by the public. So obviously anything that's the difference between this number and that number is what's the what Edwin's gone in with the taker and manually manually ordered um everything along here is what's been bought by everything apart from the maker or Edwin.

### **00:07:56**

**George Westbrook:** Um, and then obviously anything that's remaining is there. Um, I think there's one team that is sold out,

**Troy McDonald Kane:** Ow.

**George Westbrook:** the Florida Atlantic Owls, which that's not necessarily the best thing because then the makers got nothing to Yeah,

**Troy McDonald Kane:** Yeah.

**George Westbrook:** the maker's then got nothing that it can do the two-sided quotes for that. So, thought thought about that. It's not a huge issue um because obviously most of those are going to have been bought by the taker. So what we can do is do a position transfer back to the maker so that it's got it's got that liquidity in order to provide to the

**Troy McDonald Kane:** Yeah. The other thing is well,

**George Westbrook:** market.

**Troy McDonald Kane:** you know, that that um an additional million shares per team is eligible for shorting. So, you'll have the million long and then you're going to have a million short. So, I think it's more um uh to synthesize what would how it could potentially work

**George Westbrook:** Yeah.

### **00:08:58**

**Troy McDonald Kane:** prod. But I don't I mean that's not going to limit someone from shorting the market because we're allowing shorting of up to 100% of the long shares.

**George Westbrook:** H did did Edwin say something about with I can't remember if it what call it was about with with the shorting not having those a million shares basically having not unlimited but a lot higher budget within the market in order to short

**Troy McDonald Kane:** I don't understand the question. I actually don't understand the question or what you're

**George Westbrook:** well.

**Troy McDonald Kane:** saying.

**George Westbrook:** So at the moment there's obviously a million shares for long, a million shares for short. Um, with the shorting I think he was saying like in a real market you can there's way more scope. There's not really a limit on the shorts or is I might just completely misreading what he might have

**Troy McDonald Kane:** No, it's the it's the other it's the other way around. There's no limit on the shorts in the simulation.

**George Westbrook:** said.

**Troy McDonald Kane:** There's a limit on the shorts in production.

### **00:09:54**

**Troy McDonald Kane:** So that's why he's trying to emulate what it would look like in production by the market maker acquiring a portion of

**George Westbrook:** Yeah.

**Troy McDonald Kane:** the shares to be able to loan out.

**George Westbrook:** Okay.

**Troy McDonald Kane:** But it's it's it's not a fully functional need right now because we've essentially T0 has bypass that to allow up to 100% of shorts uh against the

**George Westbrook:** Okay.

**Troy McDonald Kane:** longs.

**George Westbrook:** Okay. Yeah, that that I think. Yeah, that makes

**Troy McDonald Kane:** So we'll have to we'll have to confirm how that would work.

**George Westbrook:** sense.

**Troy McDonald Kane:** But my, you know, when we were testing it, I my understanding is it wasn't going to be a they had turned the locate flag off essentially.

**George Westbrook:** Okay.

**Troy McDonald Kane:** Um, but we cannot take that into our call with them tomorrow. Uh, but but George, can you see like how many people you can see how many people bought it?

**George Westbrook:** Um,

**Troy McDonald Kane:** Can you or that the public bought it, but are we able to say individual accounts of who bought it or how many people

### **00:10:48**

**George Westbrook:** let me have a look.

**Troy McDonald Kane:** participated.

**George Westbrook:** We'll be a we'll be able to find that out. Um maybe maybe not not like on that thing that I showed you.

**Troy McDonald Kane:** Okay.

**George Westbrook:** Um we can probably send over a

**Troy McDonald Kane:** Yeah,

**George Westbrook:** report.

**Troy McDonald Kane:** it would be good to get a daily report of anyone that bought IPO shares throughout the process each day if possible.

**George Westbrook:** Yeah. Yeah.

**Troy McDonald Kane:** Yeah.

**George Westbrook:** Yeah, we can. Yeah, I suppose for the Yeah, that's that that'll be fine. So like a list of people sorted. Yeah, I'll I'll get something I'll get something we could see for that.

**Troy McDonald Kane:** Okay.

**George Westbrook:** Um, and I think one of the one of the other things that we need is that that data from Sports Radar Cody for the the expected games

**Cody Haugen:** I ser Yeah,

**George Westbrook:** because

**Cody Haugen:** I seriously wrote them twice this weekend. Uh, George, and I'm getting very pissed off.

**George Westbrook:** it's like for the that's like really needed for the for the

### **00:11:49**

**Cody Haugen:** Yeah. Yeah.

**George Westbrook:** makeup.

**Cody Haugen:** For the wait because there's two outstanding issues. We're talking about the futures, right? For college football.

**George Westbrook:** Yeah. So just an endpoint that we keep on querying.

**Cody Haugen:** Yeah.

**George Westbrook:** Um

**Cody Haugen:** Yeah. They said they said that bug was supposed to be fixed like Thursday or something.

**George Westbrook:** the

**Cody Haugen:** So when I wrote them Friday, I expected like all go. I'll call Scott uh after this

**George Westbrook:** okay I'll just double check now to see well I'll note it

**Cody Haugen:** call.

**George Westbrook:** down to just check the the futures API for NCAA

**Cody Haugen:** Yeah, because Yeah, he said it should have been fixed like like late Wednesday, Thursday sometime. So that's Yeah, when I wrote them Friday, no one got back to me,

**George Westbrook:** Okay.

**Cody Haugen:** which again irritating the s\*\*\* out of me. But then Saturday wrote them again and they said I don't know. No, I don't think they replied to that one either. So I'll call Scott regardless after this.

### **00:12:46**

**George Westbrook:** I I I don't think I've checked since since Thursday.

**Cody Haugen:** Okay.

**George Westbrook:** Um so I'll I'll check. I'll have a check. it could be fixed. Um, if it is, great. If not, and if we make the worst case scenario that it's it's not, then we'll have a think what we can do. But it's it's one of those we don't want to do one thing and then it turns out it's fixed two weeks later and then we're having

**Cody Haugen:** Yeah. Right.

**George Westbrook:** to change it.

**Cody Haugen:** Well, and yeah, I mean it's a product that we're paying for. So, um I mean I have the solution.

**George Westbrook:** Yeah.

**Cody Haugen:** How we got the the IPOs, I went to a different data provider and a different buddy and said,"Give me the futures." And um so I have a CSV, but I mean those futures are basically going to be dead in less than a week, five days.

**George Westbrook:** So do they so they don't update throughout the season?

**Cody Haugen:** Well, no.

### **00:13:46**

**Cody Haugen:** I mean, they're going to be Yeah, basically, no. They're they are locked from like your futures. N I mean, yeah. In short, yes. Hypothetically, they could change a little bit. So, yeah. Okay. Because think of if a team comes out, right, they were projected, you know, five and nine or whatever it is and they win their first three games. Yeah. Like gonna up that. Um, and that's where you see the, you know, certain sleeper teams and Yeah. So, okay. I mean, check to see if it's fixed in short. Slack me if it's not. Um, or just call me, whatever. and then I'll call

**George Westbrook:** perfect. Um, yeah. And then that between now and now and the first game,

**Cody Haugen:** Scott.

**George Westbrook:** that's I think so, what's it called? KYC stuff or non KYC stuff. maker any iterations that we're picking up on the app as well. One other thing that I think I wasn't I wasn't here on Friday so apologies.

### **00:14:47**

**George Westbrook:** So that was f\*\*\*\*\*\* manic day moving stuff. But I think from what I understand T0 are going to provide us a full replica all the test tickers. Um, just so that we can have a proper test of the market maker even while the games are going on because the issue was before we only had 10 so we could do the replay um but we couldn't have like a replica test when there's actual live games um which I think is going to be is going to be important like let's say we want to test a new maker so that it's got five levels instead of three levels or one levels whatever we decide um we can test that while those live games are going on it's going to have zero effect on any users

**Cody Haugen:** Good.

**George Westbrook:** this.

**Cody Haugen:** Yeah.

**Jared Sapirman:** George, I tried sharing my screen and it wasn't

**George Westbrook:** So now you know our pain with Google.

**Jared Sapirman:** working.

**George Westbrook:** This is it.

**Troy McDonald Kane:** Yeah, but he took a video. Can you can put the video?

### **00:15:45**

**George Westbrook:** It

**Troy McDonald Kane:** Did you send the video in the Slack channel? Jared,

**Jared Sapirman:** Uh, yeah. Not in the one with Nova though.

**Troy McDonald Kane:** send send it to Novo because it shows what he's getting. Or if you want to take a fresh one now um too after or after this call and send it through the Slack so they can see what what you're clicking and what's happening.

**George Westbrook:** Oh, no. I think you did set you sent that one in, Troy. I think the not enough not enough buying power for that order. Open orders and shorts holding play dollars. That one.

**Troy McDonald Kane:** All right. Um, is there anything else we need to

**George Westbrook:** Um,

**Troy McDonald Kane:** cover?

**George Westbrook:** I think IPO for new users working. Um, so NFL, same thing, same process. So we should all be good there. Secondary opening on Thursday. That needs to be Yeah. And then dates from sports radar and then any any iterations on the app will will pick up.

### **00:17:03**

**George Westbrook:** I think I think that's everything unless anything else from your side.

**Troy McDonald Kane:** No,

**Cody Haugen:** Yeah.

**Troy McDonald Kane:** I think that's it.

**Cody Haugen:** Nothing else from my side, George. All right. Yeah, ping me if I gota I mean,

**George Westbrook:** Perfect.

**Cody Haugen:** and I'll call Scott regardless, but yeah, let me know if it's on because Yeah, they're got to move faster,

**George Westbrook:** Perfect. Are we going to finish early?

**Cody Haugen:** right?

**George Westbrook:** Are we Are we going to finish it early? What's going

**Troy McDonald Kane:** Yeah, we're going to finish early. But that's Brett's dream is to finish early.

**George Westbrook:** on?

**Troy McDonald Kane:** He wants these to be 15 minutes, not 30\. So

**Brett StClair:** I don't want to show off that I'm finishing

**George Westbrook:** Always finishes early.

**Brett StClair:** early.

**Troy McDonald Kane:** Yeah. Yeah. So, but uh no, we appreciate, you know, obviously there's a couple refinements we want to get done this week, but I think, you know, where we're at, we've come a long way. So, thank you again to the team.

**Cody Haugen:** Yes.

**Troy McDonald Kane:** Yeah.

**Brett StClair:** Thanks. Thank you. Thanks for

**Cody Haugen:** Absolutely. Yeah.

**Brett StClair:** the

**George Westbrook:** Yeah,

**Cody Haugen:** Let's f\*\*\*\*\*\* go,

**Troy McDonald Kane:** All right.

**George Westbrook:** let's f\*\*\*\*\*\*

**Cody Haugen:** George.

**George Westbrook:** go.

**Troy McDonald Kane:** All right. Have a good rest of the day.

**Cody Haugen:** Talk soon.

**George Westbrook:** Have a good one.

**Troy McDonald Kane:** All right. Bye.

### **Transcription ended after 00:18:24**

