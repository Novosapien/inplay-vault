---
date: 2026-08-07
type: standup
description: "Friday touchdown, 7 August 2026: the three trader tiers named, SEC language constraints imposed by legal, the app redesign walkthrough, the first-open tour and fork screen, and the analyst portal gap."
source: "Gemini meeting notes, Inplay - App - Touchdown"
scope:
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[compliance/compliance]]"
  - "[[information-layer/sub-components/team-page/team-page]]"
  - "[[information-layer/sub-components/discovery-home/discovery-home]]"
  - "[[market-maker/market-maker]]"
  - "[[advertising/advertising]]"
status: extracted
extracted-to:
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[compliance/eligibility-and-age-gating]]"
  - "[[compliance/regulatory-positioning]]"
  - "[[compliance/compliance]]"
  - "[[market-maker/open-questions]]"
  - "[[advertising/advertising]]"
  - "[[ipo-module/ipo-module]]"
  - "[[integrations]]"
---

## Post-Call Analysis

~43-minute Friday touchdown, two weeks from the IPO. Edwin had a hard stop and left halfway, after presenting his prototype from his phone.

**The three tiers were named**: Trader Full, Trader Medium and Trader Light, with Troy supplying the parallel legal framing of entertainment, educational and skill-based competition. One hard blocker surfaced: tZERO's onboarding API mandates a date of birth of 18 or over, so a Trader Light user cannot be allocated an account or wallet at all until they relax that field the way they relaxed the others.

**Legal imposed language constraints** after what Edwin called a barn burner with the legal team. Nothing may claim SEC regulation, everything must say "simulated IPO", and a Regulation A testing-the-waters disclaimer now sits in the app. The route through is Rule 255, which only requires an addendum to the offering circular provided the disclosures appear ahead of time.

**Edwin presented his UI prototype** and named one part of it non-negotiable: a first-open explainer, because today a referred user's first screen is a stadium image and a referral bank that explains nothing. Behind it sits the fork screen, which is where the tier choice becomes visible to the user. George's response drew the line he has been drawing all block: front-end changes are days, the back-test lab behind them is an iceberg and is not happening before launch.

**George then walked the redesigned app**: new Teams, League, Schedule and Games tabs, team-colour circles replacing helmets, dotted-texture headers, a live tZERO order book on the team page, and collapsible chrome. Two gaps came out of it, both raised by others: Jared noticed the key players shown for the Patriots are not key players, and the Analyst tab exists but is empty with no ingestion route.

| Finding | Destination | Action |
|---------|-------------|--------|
| Three tiers named: Trader Full, Medium, Light; Troy's legal framing | [[customer-onboarding/customer-onboarding]], [[compliance/eligibility-and-age-gating]] | Major update + compliance doc |
| tZERO onboarding API mandates 18+ DOB; blocks Trader Light entirely | [[compliance/eligibility-and-age-gating]] | G1, hard blocker |
| Persona now has two KYC paths, tax resident and non-tax-resident | [[integrations]] | Integration row updated |
| No SEC-regulation claims; always "simulated IPO"; Rule 255 disclaimer | [[compliance/regulatory-positioning]], [[ipo-module/ipo-module]] | Constraints C1 to C3 |
| First-open explainer carousel and fork screen; Edwin's non-negotiable | [[customer-onboarding/customer-onboarding]] | Update written |
| App restructured into Teams / League / Schedule / Games tabs | [[information-layer/sub-components/discovery-home/discovery-home]] | Changelog entry |
| Team page tabbed, live order book, collapsible chrome, colour circles | [[information-layer/sub-components/team-page/team-page]] | Changelog entry |
| Key players is a naive top-four pull; use the SR depth chart | [[market-maker/open-questions]] | New S6 |
| Analyst tab empty; needs a portal and database, not email | [[information-layer/sub-components/team-page/team-page]] | FLAGGED for a focused session |
| Ticker should be clickable and configurable, capped around 20 entries | [[information-layer/sub-components/discovery-home/discovery-home]] | Changelog entry |
| Rewarded video: watch 30s for 100 InPlay dollars | [[advertising/advertising]] | Update written |
| Back-test lab confirmed not before launch | [[information-layer/sub-components/research-tab/research-tab]] | FLAGGED |
| Taker requirements document owed by Edwin | [[market-maker/open-questions]] | New E19 |
| App-store age rating to be set at 13+ for parental controls | [[compliance/eligibility-and-age-gating]] | Recorded |
| Tickers from tZERO are the blocker on MM order testing | [[market-maker/open-questions]] | New T13 |
| Edwin's funding position and frustration | — | No action, business context |

---

Aug 7, 2026

## **Inplay \- App \- Touchdown \- Transcript**

### **00:00:13**

**Brett StClair:** Good morning

**Edwin Johnson:** Good

**Cody Haugen:** Good morning.

**Brett StClair:** everybody.

**Cody Haugen:** How you

**Edwin Johnson:** morning.

**George Westbrook:** That's so

**Max Kingaby:** Good. Handed.

**Cody Haugen:** doing?

**Edwin Johnson:** Awesome.

**Brett StClair:** A lot of good mornings all happened at once and it felt like my whole brain had exploded.

**Edwin Johnson:** Well, I'm glad your your brain didn't explode, Brett. We need a beautiful mind operating on full cylinders. George, you look like you had a pretty solid night of inplay work. I mean, I see it on your face.

**George Westbrook:** I did.

**Edwin Johnson:** King of bee,

**George Westbrook:** I'm ready and to go.

**Edwin Johnson:** how you doing? And we've got our boy Hasan. That's sweet. Look at the profile of Kingaby Brett's shoulder. That jawline looks like it was chis chiseled out of cheese. Very nice.

**Max Kingaby:** I Fresh.

**Edwin Johnson:** Yeah, if I was 21 and had your job and you know your looks, I might have turned out to be okay.

**Troy McDonald Kane:** Uh, I'm so convinced it's just an AI clone that's sitting there in the

### **00:01:21**

**Edwin Johnson:** Well, I I will agree with you on this sense,

**Troy McDonald Kane:** background.

**Edwin Johnson:** Troy. He's definitely wearing a wig.

**Brett StClair:** Yeah, we are working on trying to improve this clone. We've really mucked up quite a bit, you know, trying to get the revisions going.

**George Westbrook:** Yeah, it's what it what it says is the real issue.

**Max Kingaby:** Yeah,

**George Westbrook:** Like it's just says a load of s\*\*\*. It's just like we really need to retrain it.

**Max Kingaby:** it it's the output that's the

**George Westbrook:** It's

**Edwin Johnson:** Yeah,

**Max Kingaby:** problem.

**Edwin Johnson:** it's the only clone that quote goes to a visa every month.

**Max Kingaby:** Hey, so you've got to find yourself. Hey s\*\*\*.

**Edwin Johnson:** That's right. Good luck out there. Just remember, Uncle Eddie needs love, too. So, if you got a spare battery or two, I wouldn't mind charging it up. What are you do drinking?

**Max Kingaby:** Congratulations.

**George Westbrook:** Fresh orange juice.

**Edwin Johnson:** Oh,

**Max Kingaby:** Congratulations.

**Edwin Johnson:** I was hoping that the screwdriver or something.

### **00:02:10**

**George Westbrook:** Twinning.

**Brett StClair:** We quickly pop down to the local fresh orange juice

**Edwin Johnson:** Awesome. That's It's great. Um,

**Brett StClair:** provider.

**Edwin Johnson:** all right. So, let's get into it. Who's Who's running this thing today? I've got to I've got to stop at nine for me. So, you won't you won't get get much out of me today, but I'm I'm definitely with you

**Brett StClair:** Right.

**George Westbrook:** I suppose two two thing two things that so app updates we'll do them

**Edwin Johnson:** guys.

**George Westbrook:** after um I think two things are the so one's around the report the daily report and the expected wins as well which I'm assuming is going to come in from the daily report um or is that going to be sports radar?

**Edwin Johnson:** No, no, that'll come from us.

**George Westbrook:** Okay. So that I think it's just structure structure and way that you built the daily support and then once we've got

**Edwin Johnson:** Yeah.

**George Westbrook:** that then we can integrate that in and then I think

### **00:03:02**

**Edwin Johnson:** Yeah. Let me make a note here, George,

**George Westbrook:** it's

**Edwin Johnson:** because I actually owe you uh deliverables. I've had a a hellacious couple days, so please forgive me.

**George Westbrook:** all

**Edwin Johnson:** Um pricing

**George Westbrook:** right

**Edwin Johnson:** mechanism. Got it. Okay. Go ahead, George. Keep going.

**George Westbrook:** then the like so for the taker um if if in the same way that you did for the market maker would requirements requirements document if you could create one of them as well. Um haven't haven't even had a chance to look at it yet in all honesty. Um we've just been focused on the market maker which hopefully by today um once we get the tickers from T0 which that's we literally just spoke about it now so it's not as if they're delaying anything. Um, then we'll start then we'll start testing it, making orders, see that, test it out over over this weekend as well and early next week, ready for the test on the 13th. Um, and then while we're testing that, start working on the taker as well.

### **00:04:06**

**George Westbrook:** So, I suppose it's taker requirements and the daily report. Um, I think the next thing is KYC stuff. Um, so obviously we spoke about there's the students who they're not going to have not going to be a tax resident so they can't earn payouts but they can still do KYC if they've got if they've got another ID so they can be validated or we calling them pardon me. So trader full is over 18 persona KYC US tax resident so they qualify for everything.

**Edwin Johnson:** Mhm.

**George Westbrook:** trade a light which is the call it the student the international student so they've got an ID they can validate that they're over 18 they're going to go through the KYC and I think we kind of spoke about a third one um which I think we still need to validate stuff with um T0 is that there's no sign up to it is that something you

**Edwin Johnson:** No,

**George Westbrook:** still still want to do

**Edwin Johnson:** there there's a sign up to it. There's a they still have to provide an email, right?

### **00:05:14**

**Edwin Johnson:** So that but other than that, that's it.

**George Westbrook:** Yeah.

**Edwin Johnson:** And it's uh legally here in the US it's going to be we're going to have to take like an at station that they're 13 and up because if you're if you're

**George Westbrook:** Yeah.

**Edwin Johnson:** 13 and up you can do it. Um under 13\.

**George Westbrook:** Okay.

**Edwin Johnson:** Yeah. You

**George Westbrook:** Cuz in in order to trade a regulated security,

**Edwin Johnson:** can't.

**George Westbrook:** do you have to be over the age of 18?

**Edwin Johnson:** Yes.

**George Westbrook:** Is that going to impact them joining in the

**Edwin Johnson:** Um, well,

**George Westbrook:** challenge?

**Edwin Johnson:** they can do because so and we had a a kind of a barn burner yesterday with legal.

**George Westbrook:** Mhm.

**Edwin Johnson:** Uh now they're they're they're all worried about our our SEC filing getting compromised because we're referring to regulated and and securities and things like that. I just had a a very long conversation with the legal team um this morning and

**George Westbrook:** All

**Edwin Johnson:** um so we are going to move forward with um the the structure that we have.

### **00:06:14**

**Edwin Johnson:** We are going to try to um ensure that anything that talks about an IPO talks about a simulated IPO. Kudos to you on that Kevin. Well done. Um and then uh as far as the securities themselves, um we're not going to say anything about regul regulated by the SEC.

**George Westbrook:** right.

**Edwin Johnson:** All that has to come down. Um and that that uh I'm going to provide him with some updated materials this morning. Um for this uh it's called rule 255\. As long as we're compliant with that, then we would only have to make an addendum to the offering circular as like our marketing um quote. They call this trading challenge a test of waters which is legal and and compliant

**George Westbrook:** H.

**Edwin Johnson:** as long as we meet the criteria of the disclosures ahead of

**George Westbrook:** Okay. Cuz I think one we'd need to speak to T0.

**Edwin Johnson:** time.

**George Westbrook:** I I think they'd be able to do it because so B they've got their onboarding API which is set up for like a full KYC.

### **00:07:13**

**George Westbrook:** And if you imagine the proper API has got 10 or 20 fields. We've only got to fill in three. One of which is date of birth which has to be over 18\. Um so in its current format we couldn't give them an account because they're not over 18\. But I'm assuming because they've been able to turn off the other stuff, they can turn that one off as well. But we just need to double check that with them.

**Troy McDonald Kane:** No, I I think you're looking at it a little bit a little um I wouldn't I wouldn't look at it that way.

**George Westbrook:** Um

**Edwin Johnson:** Yeah.

**Troy McDonald Kane:** Everyone can get an account. It's a simulator. The only people that can get cash payouts are people that go through the full KYC and validate that they're 18 and over. So, I don't know that we need to over complicate the process. I think if I mean we can also validate or put age restriction on the app itself in the app store and say you have to be 13 and over to download the app.

### **00:08:03**

**Troy McDonald Kane:** Um so that if parents have rental controls on then they can avoid even getting the app but essentially everyone gets an account whether that account is eligible for cash payouts requires them to go through the KYC which we're validating not not T0 that's what the T0 question was in the earlier call

**George Westbrook:** with with that in order for us to in the current format to allocate somebody an account ID in T0 and allocate a wallet ID to that account we they would need to be over 18\. So that's that's just part of their API for on

**Troy McDonald Kane:** Why? Okay. We Oh, yeah.

**George Westbrook:** boarding.

**Troy McDonald Kane:** Then I guess I didn't realize they because we agreed that we what we agreed to because they're not using their I thought they weren't using their KYC API.

**George Westbrook:** It's it's so I think it's and Hassan might know better than me on this is it's so using their onboarding API which part of that includes like a kind of KYC um process which for the inplay when we basically speak to them um what they do is it goes down a different path so that it doesn't validate certain fields so say whereas before like a full KYC with 20 fields if it if it wasn't us every single field would have to be filled in and validated but as soon as we send

### **00:09:27**

**George Westbrook:** a request they only validate that we send three. Um, so the fact that they're turning those other ones off makes me think that they can turn off the the the date of birth one. Um, and then we'll we'll you we'll go through that same process that we're doing now, just not sending the date of birth as well. And then that would allow us to create them an account on T0 side and then allocate a wallet. And then we what we'll do we'll send a message in the slack group um and then get that conversation going um as well as the tickers and the we don't need to worry about the um accounts because we can do that I think. Well no we we we've done that for the market maker. And I think the next part is the unless there's any questions on any of that stuff.

**Edwin Johnson:** Um, I'm assuming you guys can work that out. Um, and it's it's it's fairly simple. We just need, like Troy said,

**George Westbrook:** Yeah.

**Edwin Johnson:** you know, when you if you're doing something that doesn't have a cash payout, the requirement to be 18 and up is is thrown out the window.

### **00:10:38**

**Edwin Johnson:** So, we just need to convey that because,

**George Westbrook:** Yeah.

**Edwin Johnson:** you know, the obvious is here. We're two weeks away from the IPO.

**George Westbrook:** Yeah.

**Edwin Johnson:** I mean, we we're we're up against

**George Westbrook:** Yeah.

**Edwin Johnson:** it.

**George Westbrook:** Um, yes. So, speak we'll speak to TZ about that. Get that sorted. I think we just went we No, we spoke to Persona about the because basically what we'll have whereas before we had one kind of KYC path, now we're going to have two different paths. Um so one for the tax citizen, one for the non- tax citizen and then obviously then we'll have this one which is the I'm not going to participate in the payouts or even the the yeah the three different so trader full, trader medium and trader light. The three different types of users who are trading

**Troy McDonald Kane:** Yeah, think think about it in these three categories. First level, entertainment purposes only. Second level, educational purposes. Third level, trading competition, skilled-based competition.

### **00:11:41**

**George Westbrook:** Yeah. Okay, perfect. Um, right now changes to the app. Let's have a look. Can everyone see this? Nothing new on this page,

**Kevin Murray:** Yep.

**Cody Haugen:** Yes.

**George Westbrook:** but the So, obviously me and you had that call, Edwin. Um, and obviously given that we there was some changes that that you obviously wanted to see. Wait, go back to I need to restart this quickly. Give me one second.

**Edwin Johnson:** Is that one of your 2500 little agents there doing its work?

**George Westbrook:** Got them all. Got them all squished up.

**Cody Haugen:** I really like that

**Edwin Johnson:** Kill

**Cody Haugen:** one.

**George Westbrook:** There we go.

**Edwin Johnson:** here.

**George Westbrook:** So, changed a fair bit. So now we've got these tabs here. So for the teams, the league, the schedule, and the games. Um searches up here at the top, similar to before, changed a tiny bit. So teams page first, the teams that you favored up here. Um then what's going to happen here is if there's a live game, there's going to be a live game that will show up here.

### **00:13:24**

**George Westbrook:** um obviously the next up games and then also the results along here. Um there's no market data yet, but it's going to show the the teams who are the top movers or the the along here going along or having the ability to scroll um ability to look into different divisions be it NFL, NCAA and I suppose one of the biggest changes which we've glossed over is the new icon because I think it was correct me if I'm wrong Edwin this was for kind of legal reasons having not using the helmets and rather having

**Edwin Johnson:** No, it it wasn't for the legal reasons.

**George Westbrook:** these.

**Edwin Johnson:** It was just for like the the helmets were um they were nice, but they were, you know, there were too many helmets on the pages. Like it was it for me it was a little distracting. So, um,

**George Westbrook:** Yeah.

**Edwin Johnson:** you know, I thought that we'd just go with the colors. Um, have you invested a lot of time in this right now on the

**George Westbrook:** Uh on the app.

### **00:14:21**

**Edwin Johnson:** app?

**George Westbrook:** Yes. Um why?

**Edwin Johnson:** Um,

**George Westbrook:** What's

**Edwin Johnson:** okay. Because my thought was we're going to hold off until I came back to you with my final uh product,

**George Westbrook:** that's fine.

**Edwin Johnson:** like you know.

**George Westbrook:** We can we we can change we can change it.

**Edwin Johnson:** Okay. Okay. Um, and I I want to I'm I'm going to do something real quick.

**George Westbrook:** Um

**Edwin Johnson:** Um, bear with me a second. Okay. I'm going to exit this call. What time is it? 8:46. Cool. I'm gonna exit this call and jump on from my phone. Okay.

**Cody Haugen:** Sounds good.

**Edwin Johnson:** Yep.

**George Westbrook:** You already

**Kevin Murray:** Oops.

**Cody Haugen:** You're on mute, Edwin.

**edwin's Presentation:** All right, here we go. Cool. Let me do this.

**Cody Haugen:** Yeah.

**edwin's Presentation:** I've learned how to share my screen so well lately. f\*\*\*. I thought I did.

**Cody Haugen:** You are a proficient sharer

### **00:15:47**

**edwin's Presentation:** f\*\*\*.

**Cody Haugen:** now.

**edwin's Presentation:** I was um Where is it on this team thing to share

**George Westbrook:** Okay.

**edwin's Presentation:** the screen?

**Cody Haugen:** Um, so yeah, you're on Google, on the phone,

**edwin's Presentation:** Well, you hit the three dots, I assume.

**Cody Haugen:** I would assume.

**edwin's Presentation:** There we There we go. Yeah. Continue. I got you. All right. Cool. Start that broadcast. Right.

**Cody Haugen:** Okay.

**edwin's Presentation:** Um, so bear with me a second here because this thing's going to get janky as f\*\*\*. So, this is how I have the opening. You download the app and this is your new homepage. Right now, our our current homepage, like the the first page you see is a stadium and then a referral bank. And you know,

**George Westbrook:** Mhm.

**edwin's Presentation:** my concern is that people don't know what this is, especially if they're getting a referral. So, I think that we we have to clearly state,

**George Westbrook:** H

**edwin's Presentation:** and again, this similar to the website, you know, trade sports for free, everything's listed here.

### **00:16:57**

**edwin's Presentation:** And then they're like, "Okay, well, what the f\*\*\* is this?" They move on to the next what you own. You own the company, not the bet. So, this is this is a an um an introduction to inplay, an introduction to what the team companies are. Again, very top level, just like, hey, here you go. And then you move on to here, you know, why it's different. So, um it gives you, you know, these four tabs to go through and then we move on to the last. And the last is your opportunity. Thank you, Troy Kane. And you start with $100,000 in play dollars. It's free to play. No deposit ever. Trade live games playbyplay. Um you can get real cash prizes if you're verified. And then give some uh qualification as far as who the f\*\*\* we are because we've got these partners. Okay. Then you get started and right at the the the opening I've got it where it basically explains what the what the widgets are or whatever you call these tiles are on the thing.

### **00:17:54**

**edwin's Presentation:** So that talks about your live tape. Okay, pretty simple. The tape's pretty cool. Cody gave me some tips on how to like scroll it and and uh you know go back. So well done Cody. Um this talks about like how you play and this is this is a critical fork. You basically have the left where you have no cash prizes. You got to be 18\. You can click with an email join. Uh you go to the right you get verified. Up at the top the browse all that'll be all your other events. So like schools and universities whatever. The third this is talks about your trading capital how much you've got what you can trade with you know that thing Hassan did that beautiful bar Hassan did and then for more clarification you know our goal would be to change it to like trading reserve. Now, obviously, we've got two weeks, so we understand like as we try to like get launched, I'm not looking for a rebuild, but but you know, a total well, I would love a total rebuild, but the problem is I think that with the amount of users we have, okay, we have 150 or some b\*\*\*\*\*\*\* like that.

### **00:19:03**

**edwin's Presentation:** And now we're going to talk about putting real money behind the marketing. My concern is that we market it and people get to the app and they don't know what to do and they don't sign up. Okay. And the last one then goes to your top movers of the day and you can trade those from a single click. So here's what the homepage actually looks like as I've envisioned it. Okay. You've got your ticker up at the top. It's a little bit bigger. I know George, you were concerned about the busy nature. Then you've got the introduction. You've got the uh the one that's flipping there uh not the scroll. That's going to be your favorites. And then you know like like I was saying, you click here, browse all. There's all your different competitions. Harvard, Indiana, blah blah blah. You want to join this, you click verify with uh persona. You want to join the no cash, you got to do it with an email.

### **00:19:54**

**edwin's Presentation:** Um, scroll down to here. You look at my positions. Um, you've got three hold, you know, there you've got Dallas, your long 620, Miami 480, you know, and those are collapsible. So, that's great. Um, there's your trading reserve. Here's your um your uh uh referral button and then you've got your sponsored and everything else. Now, once we get to the bottom, I've got this uh you know ad here that you basically can watch for 30 seconds. You get 100 inplay bucks for watching it. It's great because if you end up having a f\*\*\*\*\*\*, you know, you're having a bad day, you can go to that. So, um, and again,

**George Westbrook:** Hm.

**edwin's Presentation:** without getting into the weeds on this, if I click on one of the tabs up there, I'm going to skip this tour. There's a tall for a tour for every one of these, right? And I currently brought in a live market here, so people can actually trade from here. And if I wanted to, um, you know, I can just get into the market.

### **00:20:53**

**edwin's Presentation:** I'm a big trader, so I'm going to buy a,000. And there we go. We are long a,000. There's my P\&L down at the bottom. And basically, people can just start trading from this if they wanted to. I'm a Cannonballer, so I'll buy a couple more thousand. And now I'm down 600 bucks, 700 bucks. So, what's great about this single click, blah, blah, blah. Bottom left. You know, I love your buy, sell at the bottom, George. And then, um, you know, it keeps uh, you know, your your your, uh, share count and your P\&L down at the bottom left. One click button, flatten. hopefully get filled. Still working. You can see I've got a working order there. I can cancel that. It's great. Um, so I missed those and now we're getting run over. What's great also here I've got a chart built in. You can, you know, basically collapse that chart. Um, so yeah, so I know visually there's a lot going on here.

### **00:21:49**

**edwin's Presentation:** I think that from a a user position, it gets into it pretty quickly. you know, we've got this analyst tab. Talks about like why we say buy. Um, and then down here it talks about like, you know, how they earn money, you know, whether it's off the field or on the field. You've got all those. And the the key here, team is pretty self s\*\*\*. Sorry about that. Skip. Skip. We'll go to KC. Skip schedule. Talks about what they've earned, you know, year to date. They're six and four. And these are examples. So you can see like week seven they lost against Seattle but they still made a $163. We think that's fantastic. Um so yeah, you've got all this uh engagement there. And so we've got this now this disclaimer that regulation 8 testing the waters. I've been put that in there. So I've got a disclaimer. Um, and then the the money here is what I showed you the other day, George, which is the pro version, which allows people to go ahead and start trading and I'm sorry, watching and uh, you know, you can watch a live game.

### **00:23:01**

**edwin's Presentation:** You can do a live sim or you can do a replay. Um, I've built the model so that basically you can go I'll click on live sim. You go to three games if you want and this will simulate playbyplay. Um down here you'll see an audit trail of all the games. And it's just a randomized uh realworld football game. And if you wanted to test if you're going to be a buyer or seller here, um you can go ahead and you know just hit buy. We're long a th00and and then your P\&L. You can sit here and watch this game play by play and you can see what happens uh throughout it. You can also run it really quickly and if you wanted to um where is that button? I just want to hit next next or go four times speed. It'll just run through really really quickly. I also have a counter in here for us which is a programmatic. says how many uh video or how many things have been seen uh that game and uh those things are happening here.

### **00:24:04**

**edwin's Presentation:** If you look on the field, you know, it's just running really really quickly. Boy, we're having a bad day. We're long a thousand. We're down money again. So, um but anyways, this allows that user to go ahead and try to build strategies that we talked about um the other day, which we think is pretty cool. So, without getting into too much more of that, I'll go ahead and do that and I will stop sharing the screen. Thank

**George Westbrook:** I'll get this back up. Um,

**edwin's Presentation:** you.

**George Westbrook:** so I think the I think like what we said the other day, the back testing that that's really good. We need to add that in, but realistically I don't think that's going to be there before launch. Um, it's obviously the U the UI stuff is we go back to the the iceberg

**edwin's Presentation:** Yes.

**George Westbrook:** UI stuff, we can get that stood up in a couple of days. the backend stuff for that is where that iceberg gets very deep.

### **00:24:58**

**George Westbrook:** Um so I think before launch not really not really going to be

**edwin's Presentation:** Start.

**George Westbrook:** possible. Um but obviously UI changes um in terms of what we've already got 100% um we can get them in there. So I think given what you sent the other day made some changes to the team page as well. So it's got the got the market page. Um it depends on what you've actually got here. So if I just buy Yeah, let's buy that thing like what we had before the on the flow saying working change this got the

**edwin's Presentation:** You know what? I'm gonna get off my phone because it's hard for me to see this.

**George Westbrook:** order. Oh s\*\*\*.

**edwin's Presentation:** George.

**George Westbrook:** Yeah, forget this. It's on a quite a big

**edwin's Presentation:** Yeah, bear with me a sec. Just let someone let me back in,

**George Westbrook:** screen. Should we play a game of ice while we wait? Oh,

**Max Kingaby:** I spy someone who's unmuted with a crap chin.

### **00:25:59**

**George Westbrook:** you are muted and you got a crowd. So, are we all are you are you back in Edwin? Can you hear us?

**Cody Haugen:** Yeah, he's just muted.

**Edwin Johnson:** That f\*\*\*\*\*\* auto mute is so f\*\*\*\*\*\* annoying.

**George Westbrook:** Um let me make this a bit bigger. So yeah, team colors in the background. Um the what what we had in the order flow as well. Change that in play sharing. So with with these different ones um and then the so on the that's gone to the portfolio. So, I need to go back to Patriots.

**Edwin Johnson:** I do like the circles. I think they look great.

**George Westbrook:** Yeah, this is one of the things we're playing around with here is different different design ideas. Um, so I can send this over as well. But the the circles looked looked the best with like a little bit like an enamel gloss cuz when we did when we did it with these ones up here,

**Edwin Johnson:** Yeah.

**George Westbrook:** it just looked it just looked really bit too basic.

### **00:27:15**

**George Westbrook:** Um, so added a bit of textures in so it looks bit looks a bit nicer. Um, but yeah,

**Edwin Johnson:** Agreed.

**George Westbrook:** got the got the tabs here. So this is the this is the team page. This order book is actually live. This is what's currently on T0 at the moment. Um, obviously there's only one level at the moment, but live order book orders that are actually there for this ticker. Um, with this trade bar as well, um, because one of the things we've got now is obviously this is fixed. This is fixed. This is fixed. It can take up a lot of the screen. So, it's just collapsible. Um, where's the animation? There's an animation that goes with it that makes it look a bit cleaner.

**Edwin Johnson:** Yeah.

**George Westbrook:** Um, so it's just got that dollar sign. We could change it to a T if we wanted. Um, as a user, you can swipe between the pages as well. Um, I think it's helped to break up the information a bit more.

### **00:28:10**

**Edwin Johnson:** Hey, George.

**George Westbrook:** Um,

**Edwin Johnson:** I actually have to bolt. I got a a a important call right here at 9:00. Um the the thing that I think that we can do that's going to be no weight to your quote iceberg b\*\*\*\*\*\*\*

**George Westbrook:** yeah.

**Edwin Johnson:** example, which I hate it. Um is when the app is opened, we need the we need the torque basically of what the f\*\*\* they're looking at.

**George Westbrook:** Yeah.

**Edwin Johnson:** That that is a non-negotiable. We need to get that in as soon as possible.

**George Westbrook:** Yeah.

**Edwin Johnson:** So when someone downloads it, they know exactly what they've got. Um, and they need that fork which allows them to say,

**George Westbrook:** Yeah.

**Edwin Johnson:** "Hey, you want to trade for uh you don't want to give your f\*\*\*\*\*\* ID, b\*\*\*\*? Then you go ahead." Like these,

**George Westbrook:** Yeah.

**Edwin Johnson:** there's too many of these people are like, "They want to steal my thoughts, you know, f\*\*\* them." So,

**George Westbrook:** Yeah.

**Edwin Johnson:** I want those out. You know, we we've got we got to we need to make sure that the you open up the app,

### **00:28:53**

**George Westbrook:** Okay.

**Edwin Johnson:** it tells you something about Inplay similar to what we what I've put together here. I think this is great. I don't, you know, I'm again,

**George Westbrook:** Yeah.

**Edwin Johnson:** I value all the opinions on the call, but the people who matter most on this call in terms of how this app's going to use be used are going to be Cody and I. We're the only gems on the

**George Westbrook:** Yes. Yeah. And yeah, I think in terms of changes between now and launch,

**Edwin Johnson:** call.

**George Westbrook:** I know you hate the iceberg thing, but I'm going to still use it. Um, it's anything anything front end like if you're like change this, it needs to be square, change that, fine. Not simp simple, not easy, but we can get that done.

**Edwin Johnson:** No, we got you.

**George Westbrook:** But like the the back testing stuff is a lot of backend

**Edwin Johnson:** We got you 100%.

**George Westbrook:** work.

**Edwin Johnson:** And but you know, keep in mind like one of the things that we need to do, you know, we got f\*\*\*\*\* on this b\*\*\*\*\*\*\* advertising stream that was sold to me.

### **00:29:50**

**Edwin Johnson:** We have to figure out how to monetize some of this.

**George Westbrook:** Yeah.

**Edwin Johnson:** And Cody's point is we need to make sure that we're getting some type of subscription um money in. So that needs to move as quickly as possible into saying like here's what you're going to get for for

**George Westbrook:** Huh?

**Edwin Johnson:** signing up. Now that said, it has to be robust enough that people are going to pay for it and want to use it. So, you know, I I hear you. I hear you. Um, we just need we need a lot of labor over the next couple of weeks to get done. The next,

**George Westbrook:** Yeah.

**Edwin Johnson:** like I said, the next couple weeks are going to be tough, but you know, there's a giant reward at the end for all of us. So,

**George Westbrook:** Yeah. Yeah,

**Edwin Johnson:** You know,

**George Westbrook:** we'll

**Edwin Johnson:** but for me personally, like I'm putting up a lot of money this year or I'm sorry,

**George Westbrook:** do.

**Edwin Johnson:** this month, next month in October.

### **00:30:35**

**Edwin Johnson:** Like I'm not throwing f\*\*\*\*\*\* money into the the black hole of b\*\*\*\*\*\*\* anymore. I want f\*\*\*\*\*\* results and we have to have some f\*\*\*\*\*\*

**George Westbrook:** Yeah.

**Edwin Johnson:** revenue because like honestly like you know by the end of October I'm supposed to commit like five or six million and I've already put in6 million300 thou no like 6.5 million at this point like you know at some point I'm going to get I'm going to get frustrated and just say f\*\*\* this. Okay. And I'm not there, but it's definitely getting, you know, within my periphery that I need to have some view that we're going to get some f\*\*\*\*\*\* revenue back for what I'm putting. Otherwise,

**George Westbrook:** I think you

**Edwin Johnson:** yeah, I mean, I I'm a trader,

**George Westbrook:** Yeah.

**Edwin Johnson:** you know, right now. I've got a losing trade on and I'm holding on to it. I'm going to add to the position by putting more money into the marketing. And it's really um you know this is something that I would in my trading career I wouldn't do but you know if there's potential here to make a lot.

### **00:31:33**

**George Westbrook:** Yeah.

**Edwin Johnson:** So anyways I got to run all of you have a great weekend if George I'm available after like in about three hours if you need me.

**George Westbrook:** Yeah. Okay.

**Edwin Johnson:** Okay.

**George Westbrook:** Perfect. Yeah.

**Edwin Johnson:** Thank you.

**George Westbrook:** I'll drop I'll drop you a message.

**Edwin Johnson:** Thank you. Have a good day boys.

**George Westbrook:** Perfect.

**Max Kingaby:** Excellent.

**Troy McDonald Kane:** Thank you.

**Kevin Murray:** Nice.

**Max Kingaby:** So,

**George Westbrook:** So yeah.

**Max Kingaby:** yes.

**George Westbrook:** Oh, Max, mute yourself, please. Yeah. So, I suppose we just quickly go through some of the some of the other changes. So, yeah, we've got the market page. Um, the team page. So, just splitting up the information a bit more, whereas obviously before it was just here's f\*\*\*\*\*\* everything in one long page. Good luck finding anything. um and got a lot more got a lot more data going back in time as well whereas before like the season stats it just be 2025 um so we'll have some defaults so what I don't think it worked on this part but a lot of a lot of them it will be if there's data for 2026 show it if not show the previous year um so yeah season stats expandable out um the news moved down a some of the franchise data which I suppose is that really relevant there.

### **00:32:51**

**George Westbrook:** Um

**Cody Haugen:** It is from a a team company perspective when we're starting to talk about these as team companies like Edwin just

**George Westbrook:** h

**Cody Haugen:** showed. I I think it is it builds the like granted yes you're still only trading this season but

**George Westbrook:** Yeah.

**Cody Haugen:** it builds the allure of owning that team performance or the larger part of that though the fact is you only own this season. Um yeah so I mean is it valuable to your point?

**George Westbrook:** Yeah.

**Cody Haugen:** No. You're probably right but it does give the

**George Westbrook:** Yeah.

**Cody Haugen:** allure.

**George Westbrook:** I think I I think it's just a matter of where where we put it because like you said,

**Cody Haugen:** Sure.

**George Westbrook:** this is the this is the company page. Um which a bit like you said bit light on information.

**Cody Haugen:** Yep.

**George Westbrook:** So we could just move move

**Cody Haugen:** And I'm pretty sure Yeah,

**George Westbrook:** this.

**Cody Haugen:** I'm pretty sure he had that franchise information on the company page. I'm Yeah,

### **00:33:41**

**George Westbrook:** Okay,

**Cody Haugen:** I'm cool with that. That move. I think it Yeah,

**George Westbrook:** perfect.

**Cody Haugen:** it makes sense. It's like I went at

**George Westbrook:** And then yeah, the games. So it's got upcoming games obviously which are quite important.

**Cody Haugen:** it.

**George Westbrook:** Um the the results as well. So by season if you want to I think I still need to refine this. So say looking back this year or the previous year or by opponent. So then you can go in and see okay this is what's happened in the last few years. still probably few tiny refinements there but I think conceptually you can understand it's you want to see it by season or by um opponent um analyst there's nothing there at the moment um because obviously we've not got the like with the with the analyst reports that's what we need to think about is how is it how is it being consumed and updated um because not really an efficient way where it's just sent over via email and then we're plugging it into the app.

### **00:34:39**

**George Westbrook:** there's going to need to be maybe like a portal that an analyst would go into. The analyst would then upload their report which would then get added to the database and then be surfaced here. Um, which still need to think about how how we're going to do that. Um, I think yeah,

**Jared Sapirman:** George,

**George Westbrook:** so

**Jared Sapirman:** can you go back to the company page where there was the key

**George Westbrook:** the

**Jared Sapirman:** players?

**George Westbrook:** this one

**Jared Sapirman:** Yeah. So, a couple of these players are not key players at all for the

**George Westbrook:** Yeah. Yeah. So, that's that's one all this is doing at the moment,

**Jared Sapirman:** Patriots.

**George Westbrook:** I think, is just pulling in maybe the top four players. So, what we'd need to do is have a way of working out how do we define a key player? Um, and then looking at sports radar to see if is there a way that they do that.

**Cody Haugen:** Yeah.

**George Westbrook:** Um, I'm there's got to be a way where they've got like an impact an impact number for a player.

### **00:35:43**

**Cody Haugen:** No,

**George Westbrook:** Um,

**Cody Haugen:** that would be extremely subjective. Like always think of Sport Radar as facts. They they have made a billion dollars on selling facts.

**George Westbrook:** okay.

**Cody Haugen:** So anything subjective they well I I can't say all of their data. They do sell an insights product which is facts built with some sort of conceptualization. But the what they what you the closest thing you're going to get, George, that they will have is a depth chart. And so the the depth chart would tell you exactly this.

**Jared Sapirman:** Start us off.

**George Westbrook:** Okay.

**Cody Haugen:** You're going to take the first quarterback, you're going to take the first running back, you're going to take the first wide receiver, and then we're going to take some defensive player. There's always one on every team. Um there might be multiple on every, you know, on the defensive side of the ball. Um, you know, think Houston Texans. Now, CJ Stout is still their quarterback. That's important. Um, they still have Nico Collins as their wide receiver,

### **00:36:32**

**George Westbrook:** H.

**Cody Haugen:** but their defense is stacked and that's why they're going to make the Super Bowl if they make it. Um,

**George Westbrook:** Yeah.

**Cody Haugen:** so yeah, it's it's depth chart and then yeah, we'll have to figure out some sort of cadence for the defense if we add that because yes, it does there is two sides to the ball. Um, and it isn't both. So, uh, but yeah, the depth chart is going to be the closest thing you get to from sport

**George Westbrook:** Okay. Um,

**Cody Haugen:** radar.

**George Westbrook:** depth chart and then maybe think at a later point how we could have our own algorithm that does that. Let's not go down that rabbit hole.

**Cody Haugen:** No, no, no,

**George Westbrook:** Um, and then yeah, so this this top bar now, obviously that's a lot of space.

**Cody Haugen:** no.

**George Westbrook:** So as you scroll down, it's going to collapse down so that you can still navigate through the tabs, still see the ticker, um, but it's not taking up all that space. Um, we went through this one.

### **00:37:29**

**George Westbrook:** Let's go to the new page, the league. So it's just information around the league. So things like standings, leaders, um it's it's data you've all seen before. Um obviously just on a different tab. So I think we'll get this on the test flight version and then just get that feedback get that feedback in um the schedule. So filter by NFL, NCAA um and then the games which is what's happened previously. So, I always think schedule forward looking, games backwards looking. Um, and I think the So, we've I don't know if you can see it, but we've added like this little dotted texture to the back of it. Whereas before it was just like a plain color thing adds a bit more bit more like depth to it, bit more texture so that it doesn't look just like a block color. Um, I think if we look Here we can send this over as well and it's kind of like a pick sheet. It's like I like that, I don't like that, I like that, I don't like that.

### **00:38:43**

**George Westbrook:** Um, this was the one that we thought was the best at the moment. This kind of dotted texture. So thoughts on that in comparison to just like the normal one planish

**Cody Haugen:** Yeah, I like it. I mean, yeah, I have no qualms about

**George Westbrook:** Okay, perfect. Um,

**Cody Haugen:** it.

**George Westbrook:** and then one of the things we've changed as well is this kind of header on all the pages is that kind of dotted texture with these tabs rather than what we had before just so that there's consistency. So it's not like on one page it's one type of way to navigate between pages and the header looks one way. I think obviously before we had the just kind of like this background going all the way up. Um, so it kind of closes it in a bit more. Um, but obviously makes it easier to navigate rather than if you want to go to the new page, you got to go all the way up, look what tab you're on, and then click it.

### **00:39:42**

**George Westbrook:** Whereas now you can just I know it's not got the swiping. Um, but it's just segmented a bit more. So it's easier for users so they don't have to scroll all the way down, remember where something is. is they just click along. There's four or five elements on each tab. Um, and just makes it a bit

**Cody Haugen:** So, is there something we can do?

**George Westbrook:** easier.

**Cody Haugen:** I know Edwin still needs to send you his like final build of what he's been working on for the last call it week. Um, and and just go through like page by page, feature by feature and say, "Yeah, this one's lowhanging fruit. We can add this like something like the ticker, right? His ticker. I we we came up with the idea that it needs to be clickable, right? I want people to get trapped in that hamster wheel page to page to page to page and and prices and trading and everything, right? That ticker is I think that was one of the original ideas I had right of the of the hamster wheel is like you click on New York Giants, you get trapped in that hamster wheel, you go to their team page,

### **00:40:45**

**George Westbrook:** No.

**Cody Haugen:** you can trade them right there and then the the other one that I gave him was the sliding part. Like yours actually goes slower than the one he has. So I don't know if it's less of a thing, but let's say Dallas goes by and I'm like, "Oh s\*\*\*." You know, it catches my eye. I go back up to the right. I want to click on Dallas.

**George Westbrook:** Yes.

**Cody Haugen:** you don't have to wait for the full 32 because if this is showing all 32 NFL teams and then plus on a on a week where it's showing college football teams as well, I mean, you'll never get back to your team and for another 15 minutes. Um, you know, that's just too many teams.

**George Westbrook:** Yeah.

**Cody Haugen:** Um, but I know he built in some rules like it was top movers, your favorite teams, and live games. I think where three sort of levels of build on that ticker.

**George Westbrook:** Yeah.

**Cody Haugen:** So maybe it's never 160 whatever teams or 171 teams uh maybe it is um 170 teams sorry um and then uh you know maybe it's always at a max of 20 or something like

### **00:41:45**

**George Westbrook:** Yeah, I think yeah,

**Cody Haugen:** that.

**George Westbrook:** we could have a a setting in the settings. Um, could post about it that is just configure my ticker.

**Cody Haugen:** Yeah.

**George Westbrook:** Um, the only thing I'd say is the clicking because it's such a small element and it's moving. We might need to think about that and test it. But yeah, we'll get on to that. I hate to be rude, but we have got a hard stop at at quarter pass. So,

**Cody Haugen:** Yeah. No, no

**George Westbrook:** and I think the tax form stuff as well looking into

**Cody Haugen:** worries.

**George Westbrook:** um that's in progress. So, hopefully by next week, be it start or middle, we'll we'll have an update and new new version going to be published to the app store tonight as well. There'll be changes on test flight. Um, but the a bigger review will be doing and getting out tonight.

**Cody Haugen:** Great. Awesome. Thanks, George and team.

**George Westbrook:** Perfect.

**Cody Haugen:** Appreciate you guys.

**George Westbrook:** Have a good weekend and let's f\*\*\*\*\*\*

**Cody Haugen:** Have a good weekend.

**Kevin Murray:** Yes.

**George Westbrook:** go.

**Cody Haugen:** Yeah, let's f\*\*\*\*\*\* go.

**Kevin Murray:** Excuse

**Brett StClair:** Go guys.

**Cody Haugen:** Uh,

**George Westbrook:** Bye-bye.

### **Transcription ended after 00:42:46**

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*