---
date: 2026-07-29
type: standup
description: "Wednesday touchdown, 29 July 2026: Kochava chosen as MMP, the support-and-maintenance gap, Brett's KYC-funnel warning, subscriptions as the near-term revenue, and a second trading demo."
source: "Gemini meeting notes, Inplay - App - Touchdown"
scope:
  - "[[advertising/advertising]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[trading/trading]]"
  - "[[information-layer/sub-components/research-tab/research-tab]]"
  - "[[delivery/delivery]]"
  - "[[integrations]]"
status: extracted
extracted-to:
  - "[[advertising/advertising]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[trading/trading]]"
  - "[[delivery/delivery]]"
  - "[[integrations]]"
  - "[[referral/referral]]"
---

## Post-Call Analysis

~51-minute Wednesday touchdown. The most strategically candid call of the block: Edwin laid out the money position openly, including that the $60m of pre-bought Omnicom ad space he had planned against evaporated to zero, and that he has funded roughly $6.5m himself with $7 to $10m more needed before launch.

Four substantive threads. **Kochava is the MMP direction** over AppsFlyer, at a fifth to a tenth of the price, with one real gap (no direct AdMob integration) that Brett judged workable. **Brett raised a long-term KYC warning** drawn from Google's post-acquisition login problem: a mixed population of logged-out, logged-in and KYC'd users complicates ad serving, house ads, impression tracking and upsell, and the hard part is moving anyone up a tier once they are comfortable. Edwin's answer, that sports-betting accounts let you see everything until you take risk, is effectively the model the 03-08 call formalised. **Subscriptions were named as the near-term revenue**, because programmatic takes six to nine months to ramp by which point the challenge is over, and crucially they do not have to ship at launch. And George set out the priority logic that held for the rest of the block: premium features are revenue-critical but the app functions without them.

Brett also flagged the missing **support and maintenance contract**, arguing it should be designed agentically rather than as humans watching screens.

Hasan demoed trading again, with Edwin giving trading-desk feedback (a max-quantity button, praise for the pre-loaded exit as a fat-finger guard) and Jared catching an inverted-arrow bug.

| Finding | Destination | Action |
|---------|-------------|--------|
| Kochava over AppsFlyer; no direct AdMob integration; Plexus relationship | [[advertising/advertising]], [[integrations]] | Update + integration row |
| KYC funnel warning: mixed audiences break ad targeting and upsell | [[customer-onboarding/customer-onboarding]], [[advertising/advertising]] | Recorded as a known future cost |
| Subscriptions are the near-term revenue; can land week 2 of NFL | [[information-layer/sub-components/research-tab/research-tab]] | Changelog entry |
| Payment provider will not be app-store IAP; needs integration and gating | [[information-layer/sub-components/research-tab/research-tab]] | Reverses the 26-06 in-app-payment decision |
| Trading end to end confirmed with Rob; fill notifications in-app and push | [[trading/trading]] | Update written |
| Cannot short while long; tZERO tracks the borrow in separate wallets | [[trading/trading]] | Update written |
| Buy/sell arrows inverted on the open-order screen | [[trading/trading]] | Bug logged |
| QA data is tZERO replay of real historical games, not random | [[trading/trading]] | Update written |
| Support and maintenance gap; agentic monitoring proposal | [[delivery/delivery]] | Delivery note |
| Referrals not converting pre-launch; expected to kick in on drawdown | [[referral/referral]] | Note added |
| NCAA IPO simplified to a five-day window | [[ipo-module/ipo-module]] | Confirmed and expanded 31-07 |
| Fundraising position, Hard Rock silence, Omnicom reversal | — | No action, business context |

---

Jul 29, 2026

## **Inplay \- App \- Touchdown \- Transcript**

### **00:00:09**

**Brett StClair:** Hello peoples.

**Cody Haugen:** Hey Brad, how you doing?

**Brett StClair:** Okay.

**Gary Anderson:** Morning.

**George Westbrook:** Morning.

**Troy McDonald Kane:** Hello.

**Brett StClair:** So Cody, I just did a very general analysis on it. Ran a whole lot of research agents, did the comparisons and I think it all, you know,

**Cody Haugen:** No.

**Brett StClair:** is dependent on um the budget and trying to work down both players to see what your fair value is. I think we can work with the ADM Mob stuff. It's just not a standard

**Cody Haugen:** Okay. because that's what I when I was looking at your your list, I was like, well, if that's the one that's integrated already and Coachaba doesn't handle that,

**Brett StClair:** integration.

**Cody Haugen:** well, that's a big f\*\*\* you and I guess we can't work with them. But no, if it's something where we can, it's not a direct integration, but we can work around it potentially. I mean, Coachava is like, you know, a fifth of the price. Yeah. of the price. Um,

**Brett StClair:** Well,

### **00:01:21**

**Cody Haugen:** so it might

**Brett StClair:** I think that's probably a worthwhile let's let's have a call with them and just understand because they can integrate.

**Cody Haugen:** be

**Brett StClair:** We just need to understand what the effort is to

**Cody Haugen:** well. So, so also the benefit here, Brett,

**Brett StClair:** integrate.

**Cody Haugen:** is uh Jason of Plexus Media, the potential marketing agency that we're going to be working with, um, has direct relationships with Coachava to the Yeah.

**Brett StClair:** Oh, awesome.

**Cody Haugen:** to the point where he's mentioned a couple times that he is pretty confident he can negotiate a better rate for us um even than their kind of standard rates. So um we're right well right yeah it's like a tenth of the price.

**Brett StClair:** And they're already a good rate, by the

**Cody Haugen:** So,

**Brett StClair:** way.

**Cody Haugen:** um, so yeah, uh, Edwin and I are speaking with him right after this call, um, on the commercials, um, because there's just some things that obviously we fundamentally disagree on, which is pretty standard on any sort of negotiation. But um so yeah, we'll we'll we'll talk about that with him and and see what his take uh is on that level of confidence on the negotiation.

### **00:02:30**

**Brett StClair:** Awesome. Good. Okay. So, I'm glad I managed to I just suddenly realized last night I was like,

**Cody Haugen:** But no,

**Brett StClair:** "Oh, f\*\*\*. I haven't got that to you." I have

**Cody Haugen:** no, I I appre I appreciate putting it all together.

**Brett StClair:** agents.

**Cody Haugen:** No, no worries. I appreciate putting it together. Um so from that level just uh as we're waiting quickly for Edwin to join is um other than that though Coachaba would be a suitable a suitable Vex. um based on this about everything that you've looked at.

**Brett StClair:** Yeah, it's got everything else,

**Cody Haugen:** Okay.

**Brett StClair:** right? Um,

**Cody Haugen:** Yes.

**Brett StClair:** it's but you know, it's a cheap option. I don't think you should be going Rolls-Royce on this,

**Cody Haugen:** No.

**Brett StClair:** right?

**Cody Haugen:** No. And and

**Brett StClair:** After after that analysis, my brain went to Katala rather than the other one.

**Cody Haugen:** certainly.

**Brett StClair:** And then we figure out how we integrate what's needed. That's the only little gap.

### **00:03:22**

**Brett StClair:** And yes, it's a big gap, but it's it's a gap that's

**Cody Haugen:** Okay. Good.

**Brett StClair:** doable.

**Cody Haugen:** All right, then I will. Yeah, I I appreciate all that feedback and appreciate your uh your time putting it in for me. So, I will talk about that with Jason and Eden uh after this call.

**Brett StClair:** No worries. No worries, dude.

**Troy McDonald Kane:** and uh where are we with the Android store approval?

**Cody Haugen:** Cool.

**Troy McDonald Kane:** Do we know

**Hasan Ahmed:** um at the moment is still um I think still being checked right now. If I'd like to play still console right now just to have a

**Cody Haugen:** Yeah, believe it or not, Hassan, there's a lot of uh Android f\*\*\*\* out there in the world still these days. I thought it was a lot less, but they're coming out of the woodworks and I'm getting surprised by them daily of people saying, "Where's the Android?"

**Brett StClair:** I used I used to be Android,

**Cody Haugen:** Uh,

**Hasan Ahmed:** I used to be doing all

### **00:04:16**

**Brett StClair:** but even I've moved away from Android onto Apple

**George Westbrook:** Even I was going to say I thought it was just boomers like Brett

**Brett StClair:** now.

**Cody Haugen:** which uh well I was I I actually expected to say

**Hasan Ahmed:** this position.

**George Westbrook:** that use Android.

**Cody Haugen:** you were on Android because your team Google so hard. So um but yeah, it is surprisingly coming up and being like a weird thing now that I did not expect to be a thing. But um yeah, apparently there's a lot of Android users out there still. So um wherever Yeah. Wherever we could get a a solid update on that, that would be

**Brett StClair:** So, Cody, as the ex uh country director of Android for emerging

**Cody Haugen:** great.

**Brett StClair:** markets, I'm surprised you're saying still, come on, man. This is a growing product. What the f\*\*\*? It's just in the Americas, right? Jesus.

**Cody Haugen:** Yeah. I mean, sure. I mean,

**Brett StClair:** Lots of $50 handsets out

**Cody Haugen:** they do they do ship all their they do ship all their, you know, uh, old devices to, you know, developing countries.

### **00:05:13**

**Cody Haugen:** So, I guess there's millions and hundreds of millions of devices living out there.

**Brett StClair:** Hello

**Cody Haugen:** So, you're on you're on mute,

**Troy McDonald Kane:** I think I will join.

**Brett StClair:** everyone.

**Troy McDonald Kane:** Yeah.

**Cody Haugen:** buddy.

**Edwin Johnson:** I don't know if you could read my lips, but I said, "f\*\*\* you. I hate that f\*\*\*\*\*\* mut." Um, all right. Sorry for being late. It's been a been a great uh great uh morning so far. Um, where are we at? Brett, real quick before we get into it, I got your contract. I will review it ASAP and then um you know we'll We'll go from there. Just on a cursory before I get into it and we we'll talk about it offline. I So I'm I'm paying for the ad server guy and then part of the AI portion. Am I also paying a commission?

**Brett StClair:** taken that out. Yeah,

**Edwin Johnson:** Got it.

**Brett StClair:** I've just made it a services component cuz I saw that come up and I was like

### **00:06:25**

**Edwin Johnson:** Okay. Because I

**Brett StClair:** actually it's either or. You got to pick either or, right?

**Edwin Johnson:** Okay,

**Brett StClair:** It's either a commission or but there's so much build that we have to do with the agent guys.

**Edwin Johnson:** cool.

**Brett StClair:** So that's why I pulled that out cuz it's not going to be possible,

**Edwin Johnson:** Yeah. Yeah. Okay, cool. We'll we'll work on uh you know like key key

**Brett StClair:** right?

**Edwin Johnson:** things that happen. You know obviously we're we're in bed with you guys and as we go we want to make sure that you guys are incentivized to continue to give us that same great service that George Hassan even Cam when he shows up it's good. So I mean we're we're you know Troy and I spoke yesterday about you know having you guys on Um, specifically with Hassan, George, you and Max being available when we have questions, even off hours for you has taken a load off of us having to to fire out getting a CTO or someone like that to help us, right?

### **00:07:24**

**Edwin Johnson:** So, we're leaning on you in that way and it's saving me at the double dip.

**Brett StClair:** Yeah, we've got enough of a coverage from a CTO point of view and I think you you're small enough to not worry about from a CIO. So CIO worries about the running of the technology, the running of your desktops, your emails and all that stuff. You don't really need that. CTO, we've got enough coverage to cover you with experience. The one thing that is missing out of your suite, and I'm not too worried about it for launch, um, it's when the numbers go up, and that's a support and maintenance contract, and how we need to do it. And what I've what I started working on last night was describing it for you what a typical kind of support and maintenance looks feels like because I think we need to actually think about this and go how do we apply an agentic AI view onto this on monitoring and so we do it differently because you you're usual it's humans monitoring stuff 24 hours 7 days a week um it's having humans on call It's um I built many of these support and maintenance things.

### **00:08:35**

**Brett StClair:** And the thing what mainly for mobile operators and banks and what most people want to see, they want to walk into a room, there's three or four people staring at a bank of f\*\*\*\*\*\* screens and it's just not cost effective, right? Cuz you're trying to hire the most junior person.

**Edwin Johnson:** No.

**Brett StClair:** You're making do the shittiest thing just monitoring. And so like I don't know. I just needed to sit down with you guys and let's brainstorm some ideas. And so what I figured was if I lay out kind of how traditional support and maintenance would work and then we kind of go, well, what could we automate? Let's throw a whole bunch of ideas together to figure this out because when the numbers are small, we can probably pick up on it as it is. When the numbers start rolling in, you've got to be dealing with this in tears, right? Because you're going to have support requests that go, "Uh, I can't log in. Uh calling a Y forgotten my password but I've forgotten my my account for my

### **00:09:33**

**Edwin Johnson:** That's me basically.

**Brett StClair:** password.

**Edwin Johnson:** Yes. Same face by the way.

**Troy McDonald Kane:** It is. He's probably reset his password 20 times since

**Edwin Johnson:** All right, Troy. No names need to be disclosed here.

**Troy McDonald Kane:** I

**Edwin Johnson:** All right.

**Brett StClair:** Sorry that no if I'd known it was you I wouldn't have like been so ridiculous about

**Edwin Johnson:** Jesus Christ. No. No. Actually,

**Brett StClair:** it but never does it

**Edwin Johnson:** I feel like I looked in the mirror and I saw the end of me. So, Amen.

**George Westbrook:** Brett never does it either.

**Brett StClair:** either.

**George Westbrook:** He's he's never forgot a single

**Edwin Johnson:** Well, I mean to be honest with you,

**Brett StClair:** or I'll often do

**George Westbrook:** password.

**Edwin Johnson:** George, why do we need so many? Can't we just like look at the retina eyeball or something?

**Brett StClair:** it.

**Edwin Johnson:** Like at this point, it's a b\*\*\*\*\*\*\*.

**George Westbrook:** Same password for everything.

**Edwin Johnson:** Yeah.

**Brett StClair:** So I just want

**Edwin Johnson:** I mean, what scares me about the the maintenance and the help desk and s\*\*\*,

### **00:10:11**

**Brett StClair:** to

**Edwin Johnson:** you know, last week when I had my lawyer flew in, you know, we we went into court and I wanted to file an emergency motion to get a restraining order against this lunatic and we heard a guy, well,

**Brett StClair:** Yeah.

**Edwin Johnson:** actually it was a girl talking to the judge and it was she was a prosay litigant and she might have been the dumbest human being I've ever heard in my life. She was um the uh dashboard for her MercedesBenz AMG went out and she was suing the car dealer, not the manufacturer, the car dealer for selling her defaulty thing. Obviously, it was like a fuse or something. And she was like, you know, I I'm not going to do it justice. She was like the MercedesBenz AMG funeral or no, a casket on wheels. And I was like,

**Brett StClair:** Oh my god.

**Edwin Johnson:** and that was a tough cell even for me.

**Brett StClair:** Yeah. So, I just want to talk you guys through it and the various levels and where we can use tech,

### **00:11:09**

**Edwin Johnson:** Yeah.

**Brett StClair:** but there's going to have to be some human element in blend and it's going to be a bit more of a problem when you've got your numbers up. So, let's not rush into it. Let's get this done, right? But I figured by setting the scene,

**Edwin Johnson:** Cool.

**Brett StClair:** giving you some experiences that I've lived through and then let's thrash something out and figure out the most cost effective way to do

**Edwin Johnson:** Cool. Yeah, we'll work together. I mean,

**Brett StClair:** this.

**Edwin Johnson:** we're totally aligned in terms of the goals and the the commercials won't get into the way. Like, we'll figure out a way to make it everyone makes a little bit of money and has a good time. So, okay. All right. Um, what's next? You got anything to show me other than Max's visa itinerary? yellow shot at noon,

**Brett StClair:** is up.

**Edwin Johnson:** you

**Brett StClair:** Well, the way to see Max's IBA itinerary is you got to be in the office when we are all vibing and his playlist comes out.

### **00:12:09**

**Edwin Johnson:** He strikes me as a real Barry Manalo type guy. But they don't know who that is.

**Brett StClair:** It's names I've never heard of it. What are some of their names that you listen

**George Westbrook:** times the

**Edwin Johnson:** Yeah.

**Max Kingaby:** Today we we had uh Postper on the

**George Westbrook:** use.

**Edwin Johnson:** Prosper. Okay.

**Max Kingaby:** DJ.

**Edwin Johnson:** Max, have you ever heard of this dynamic duo switch disco?

**Max Kingaby:** No.

**George Westbrook:** She

**Max Kingaby:** Should I

**Edwin Johnson:** They're they're they're a mashup crew from London.

**Max Kingaby:** have

**George Westbrook:** died.

**Edwin Johnson:** If you ever are in my office, that's what's playing. They give you like three 15 seconds of a song and then the next song's, you know, another one, right? I I like the mashups,

**George Westbrook:** like ADHD

**Edwin Johnson:** but Yeah.

**George Westbrook:** music.

**Edwin Johnson:** Yeah. Kevin is just, you know, straight p\*\*\* theme music.

**George Westbrook:** Just listen. Yeah. Listen listening to a plumber that's going in who the woman doesn't have any money to play.

### **00:13:02**

**George Westbrook:** Is that is that is that

**Edwin Johnson:** That's it. How can I work off this

**Brett StClair:** Yeah.

**George Westbrook:** Yeah.

**Kevin Murray:** Sounds about right.

**Brett StClair:** So before before we jump in,

**Edwin Johnson:** debt?

**George Westbrook:** something,

**Brett StClair:** something was niggling on my mind and you know me,

**George Westbrook:** you know.

**Brett StClair:** I just want to share it and get you guys thoughts on it and views on it. KYC customer Like I just want I want to bring some red lights to it. I need you guys just to think about it and happy to go either way. I think the solutions that you guys are thinking of are really good. But I do want you guys to think just put your minds in a longer term play. And I come from a world of Google. I've lived through a world where um all a lot of the acquisitions they had had no login. People just went to it and then they had to move very quickly to a logged in world because of the likes of Facebook and all these media owners are adding so much more value from a data point of view to their inventory and audience.

### **00:14:15**

**Brett StClair:** And it took Google about two years to figure out how to get everyone onto like a single login. like you you know you take your Google ID, you can log on to YouTube, you can log and then work out the different layers of the different types of audiences and how they wanted to service them across different use cases, user journeys and it was mad. It was like um I've never seen so much human engineering resource put in a project and projects were all delayed and they're trying to sort this problem out. After living through that experience, I just want to you guys just to where this half an hour think of what your world looks like when you've got a mixture of challenge audiences. real live audiences. Um, not logged in audiences in in the challenge, logged in audiences, KY logged in and KYC audiences, and then how you're wanting to convert and upsell them. And so, it starts getting a little bit complicated. It's it's manageable through the technology from a user journey. But I just want you guys to be thinking about how do I move it from one to the other to the other because you can use house ads.

### **00:15:34**

**Brett StClair:** But you need to be very careful with house ads because now you need to be understanding that type of audience layer coming in and if they're not logged in, it's quite difficult and the information that we need to feed to the ad serving engines because you don't want to go well I'm just going to if you're not logged in you're not going to get an ad served to you. You're just going to see a banner. That's important impressions. Whether it's a banner that's trying to force you to go KYC, that still needs to be an ad service. You still need to track. You still need that information. You still need to push it through the NMP. And so, right now, it's a Yes, that sounds like a great idea. where we've got this challenge of a KYC loggedin user which by the way you your product that's the hardest user to get. So you're always going to have that as a constant challenge within your business. Um is it easier rolling them in bit by bit?

### **00:16:35**

**Brett StClair:** Probably. Are you kneejerking um because of the current audience base and the current stats you've got which are small to try and get something in place? Is that knee-jerk? Which to me makes kind of sense right now where you guys are why why I think it makes sense. Like if I was was listening to George and all your conversations, I was like, "Yeah, I think it's probably a good thing." But the long-term approach suddenly becomes challenging um around ad serving around impressions around conversions around upselling around pulling them up to a KYC and I want to add one last bit is once you have the audiences coming through is that difficulty as difficult as one expects so like a Robin Hood that is the challenge they have to get someone KY if they let them off the hook, would they ever be able to get someone KYC or would you have this everlasting audience that sits there just grabbing information?

**Edwin Johnson:** Yeah.

**Brett StClair:** Um, you're going to have So,

**Edwin Johnson:** So let let me Yeah.

**Brett StClair:** I just want you to think a little bit longer term about it and then and if you're comfortable, then we're

### **00:17:48**

**Edwin Johnson:** Let let me give you one perspective related to that.

**Brett StClair:** comfortable.

**Edwin Johnson:** Okay. is so right now if I log on to one of my sports betting accounts um that I uh haven't funded yet or you know I have the fund or something. Um, I can look at pretty much everything they offer, but the moment I want to take action and take risk, I have to, you know, provide them the bank information, give send the bank, all that and the KYC stuff. Um, so we look at slightly differently in terms of how the layers work.

**Brett StClair:** Okay.

**Edwin Johnson:** So, we don't I'm I don't understand the programmatic game at all. Okay? I I'm just we're in a situation now where like I've just did the budget for the rest of the year and it looks like we're going to have to spend somewhere between seven and $10 million. Okay. And you know all of our investment leads have gone cold. No one's reached out since Saturday which is not a good sign. So, we have to assume that um I have to fund the rest of this for the next four months just to get to launch, right?

### **00:18:57**

**Edwin Johnson:** And then a launch it's going to be another, you know, probably four or five million just to ensure that we can launch the production amount. So, we're starting to get into like significant number,

**Brett StClair:** I speak.

**Edwin Johnson:** right? So, big big money. Right now we only have a hundred signups and I would say 60% or 55% no probably 65% are all friends or family.

**Brett StClair:** I was about to say we're we're at a barbecue with Troy.

**Edwin Johnson:** Yeah. And that's not great.

**Brett StClair:** Yeah.

**Edwin Johnson:** Now we haven't done a ton of marketing but all of our efforts for the fall or spring campaign there's been no conversion. nothing of substance, right? And so, you know, the 35 or 40 grand I spent to send the team all over the country has provided me with with I think we have how many did we say, Cody? 30\. I think we're like $1,500 of conversion.

**Cody Haugen:** 32

**Edwin Johnson:** Not Not great, right? You're you're not going to you're not going to have a business with that.

### **00:19:58**

**Cody Haugen:** 32

**Brett StClair:** At least at least you got the data point now,

**Edwin Johnson:** Um,

**Brett StClair:** right? That's the only thing you can take out of that is now you know what the data point and doing that kind of hands-on

**Edwin Johnson:** I mean, well,

**Brett StClair:** acquisition.

**Edwin Johnson:** I think it's I don't think it's fair because we didn't have the app up at the time. If we had the app up at the time, I think a lot more people would have downloaded the app at that instant. Now, converting them into the KYC. Well, I do understand your position, but I think what where where our head's at right now is we can't look at the ads that are going to help there. It's going to be a minimal amount of money that we make from the ad serving. I mean, not even enough to cover the cash dist distributions,

**Brett StClair:** Yeah. Yeah. Right now. Yeah.

**Edwin Johnson:** right? Uh cash payments. So, that $10 million does not include paying out winners.

### **00:20:52**

**Edwin Johnson:** That's just to to to market operate and whatever. So a a pretty big number. If we add in let's say a minimum of another five, I mean it's going to be we're right around 20, you know, and at some point it becomes, you know, where we're on thin ice. So Cody's uh idea about having the subscriptions and access to the trading tool and the you know information the AI generated uh abilities all the things we talked about those become relatively critical uh to us and I would say that we're going to need those relatively quickly to be part of this environment otherwise you we we're going to need a lot more runway and a lot more money. And you know, I'll figure out a way to make it work. I always do. But, uh, at the end of the day, I'm starting to get into where, you know, if I'm trying to raise 40 million and I want to give up like 22% of company for that and we're on, you know, fumes and we don't have a lot of, you know, light at the tunnel, I'm not going to be able to do a deal at 22%.

### **00:22:11**

**Edwin Johnson:** Right? I'm going to have to do a deal far worse for me. And this is generally where founders get f\*\*\*\*\*. And I want to be very careful not to get f\*\*\*\*\*.

**George Westbrook:** One one quick thing with the outreach. Um, is it worth so need to raise money? Two ways of raising money. Raise it or do direct sales and I suppose which one's more more crucial. Um,

**Edwin Johnson:** I mean, the direct sales is more crucial,

**George Westbrook:** maybe raise it.

**Edwin Johnson:** George, because then you actually have you have a track record of money,

**George Westbrook:** Okay.

**Edwin Johnson:** but we haven't been able to get anyone to respond to emails. Like, we can't sell advertising. our entire um you know where where we decided to hit the pedal was we understood that Omnicom was pre- buying roughly $60 million worth of ad space is what we were told in April and May okay so for us you know we said okay all systems go you know in the last three or four months I've had to put in like a million two you know just to keep things own self, right?

### **00:23:21**

**Edwin Johnson:** And you know, had I had I known the actual state of the advertising, I probably wouldn't have made some of those decisions. That said, we're here now, so it's not we can't look back and cry. But, you know, I certainly wouldn't have said, "Let's let's rush into a trading challenge and let's let's cram the summer trying to build an app and do all these things in such short order if I didn't believe that we had the um re some revenue right coming." And you know when it come when we went to 60 to zero I mean that was a pretty uh tough uh thing sobering effect for our entire team. You know, we had planned on that. I mean, is that fair

**Cody Haugen:** Yeah. Uh can I can I just kind of summarize here uh because Edwin and I have talked about

**Edwin Johnson:** team?

**Cody Haugen:** this uh at great length over the past week or so, but I I think I mean our our our if if the research is not ready for launch, which George, you and I have talked about at Nauseium as well, we still need that that roadmap uh or backlog feature from Brett.

### **00:24:32**

**Cody Haugen:** Um, and and something like I said, I I I need daily insight into where the time is being spent. And I know you guys are working non-stop. I get that. It's not a it's not an attack. It's more just clarity sort of point of view.

**George Westbrook:** Yeah.

**Cody Haugen:** um and where those features fall because at this point the our nut to to help you know as Edwin is saying is the the subscriptions whether that be on the research function whether that be on the watch tab and how we can make that a true paid subscription feature with multiple games and you know it's your it's your war room it's all of these things in one page it's the AI companion app it's all these things that we want to build into the subscription features. That's going to help us offset a lot of this cost that Edwin's putting in at least on our hopefully conservative projections brings him net zero. Um, and then any programmatic over the time and any sort of extra uh fill we can get on subscriptions is cherry on top.

### **00:25:39**

**Cody Haugen:** But that that's really where we need to to head in parallel with the the programmatic stuff. But the programmatic stuff, as we've all talked about, takes six to nine months to really get up and running. Um, by that point, this challenge is done and the basketball challenge is halfway done. So, um, it's just not a realistic revenue generator to the to the level that we need it to be. So, we're looking at the cards that we have in our hand right now, and it's it's premium subscriptions while still parallel getting the the SSP set up and and running. Um, but yeah, that's that's kind of where we're at. So, a couple things that we just need from you guys to to understand where we're at and where that that timing falls because if it's not ready for launch, is it ready in the first couple weeks? Can we push it out in another launch then? Is it ready in the first month? you know what what are we looking at? Um because right now I don't think we still have that nailed

### **00:26:42**

**George Westbrook:** Yeah.

**Cody Haugen:** down.

**George Westbrook:** No, I agree. We don't cuz for us we've kind of got blinders on um with ads cuz like I think

**Cody Haugen:** Exactly.

**George Westbrook:** it's the kind of four non-negotiables are obviously ads but more importantly trading market maker trading market maker top top top top top priority. So we have got blinders on. So that that is all we are focusing on. Good news with the trading. Had a call with um Hassan had a call with Rob yesterday. Did the end to end testing. Me and Hassan were like little children playing around with it last night. I was like, "Oh, you buy that and then I'll sell that and then does it work out?" "Yeah, it works out." "Oh, f\*\*\*\*\*\* come on. Come on." Um yeah.

**Edwin Johnson:** That's

**George Westbrook:** And it's Yeah.

**Edwin Johnson:** awesome.

**George Westbrook:** It's it. So trading is is is pretty much there. Obviously, it's not going to be perfect now, but hence why we've been putting all our eggs in that basket for a bit.

### **00:27:36**

**George Westbrook:** Market Maker still working all that through, making good progress now. We've got trading sorted. It's just a matter of getting the because obviously trading and market maker very tightly interlin. Um there'll be good proc good progress over there. And then now that trading sorted, next thing is going to be ads. Then after that, like we spoke about Cody, is that tax form? Um, which we're still we we might need to do a session on that like what does that entail? What external things need to happen? What internal things are going to happen? But I suppose it's for us it's it's what what do we need to get for done for the launch, which is a completely non-negotiable. Um, and maybe I'm right, maybe I'm wrong on this, but with like the premium things, it's obviously critical for revenue. Um but in terms of the app actually functioning it's not um compare that to the market maker or the trading without that it's yeah it's just it people can't use it. Um so I suppose that's where we're thinking about the priorities is what is completely non-negotiable in terms of functionality.

### **00:28:46**

**George Westbrook:** Um, obviously appreciate what you're saying about the the revenue from the premium research, but in terms of functionality, it's we've got, let's call it a V1 of all of them. Maybe the research does need more improvement for it to be considered a true V1. Um, but like some of the complexities that come in with the um, let's call them premium features are are we going to use the the app store for managing payments? Well, I think like you were saying, we're probably there's going to be another payment provider. So, we're going to need to integrate that, make sure that that's bulletproof, hardened, especially when it's coming to like real real real money. Um, which like with that we we're not entirely sure on the platform yet. We haven't integrated it. We haven't started planning. Then what we'll have to do is in the actual application is gate things off. So it's it it's it's there's some complexities in there which if we started working on them now in parallel or scoping them out is going to interfere with the non-negotiables.

### **00:29:50**

**Edwin Johnson:** We understand. So I I would look at it like this, George. as much as like so we've modified our our IPO for the NCAA uh football, right? We made that much easier to uh run just open for the five days. You you've read that from Troy, right?

**George Westbrook:** Yeah.

**Edwin Johnson:** Yeah.

**Troy McDonald Kane:** Yeah. And the T0 confirmed this morning uh that they received and reviewed the specs and we're going to

**George Westbrook:** Yeah.

**Edwin Johnson:** So,

**Troy McDonald Kane:** review it as a team all the TZ the Novo team and the inplay team tomorrow.

**George Westbrook:** Perfect. I I did have some questions around that,

**Edwin Johnson:** great.

**Troy McDonald Kane:** Yeah.

**George Westbrook:** so I'll save them for tomorrow.

**Edwin Johnson:** Cool. Yeah. So basically, you know, we can we can modify. I mean, we've got 106 users, so whatever even even as we roll out and, you know,

**George Westbrook:** Yeah.

**Edwin Johnson:** Troy hands uh puts his campus uh group to work and you know, hopefully we're going to get you know, 50,000 you know, signups from that alone, right?

### **00:30:48**

**Edwin Johnson:** And and hopefully then there's some referral although the referrals aren't working the way that I thought they would. that no one's referring anyone to get more trading money and it might be because they haven't lost any trading money yet. You know, a lot of it has to do with the fact that it's still weeks out and it doesn't feel real yet. Kind of similar to how people responded to we're going to build an app versus here's our app. It's like night and day.

**Troy McDonald Kane:** Yeah, Adam, real quick on that.

**Edwin Johnson:** Um

**Troy McDonald Kane:** We we interviewed a candidate yesterday from OSU and he says that he thinks the referral program is smart and he thinks it will be more utilized when the competition starts. As people draw down,

**Edwin Johnson:** Yeah.

**Troy McDonald Kane:** they'll go out and get referrals to build it back up. He actually thinks it's a really good model and he thinks it will play well on the OSU

**Edwin Johnson:** Yeah.

**Troy McDonald Kane:** campus.

**Edwin Johnson:** Um, yeah. I I I I agree with him.

### **00:31:38**

**Edwin Johnson:** I think that but all things have to be moving which goes to my point George which is I don't think we have to have

**Troy McDonald Kane:** Yeah.

**Edwin Johnson:** a everything's got to be up before the launch in order for us to benefit from it. Even the subscriptions right like we can if the subscriptions become a week available in week two of the

**George Westbrook:** H.

**Edwin Johnson:** NFL so be it. I mean, there's only so many hours in the day and so much we can do without like shooting ourselves in the foot along the way, you know, to we just have to assume that like this initial run we're going to get f\*\*\*\*\* on. I mean, I I'm resigned. I'm getting f\*\*\*\*\* here. And, you know, it's it's on me at the end of the day because I trusted that we had ads sold and we didn't. You know, that was total bub kiss. So, um, you know, we can we can point fingers at, you know, who's responsible for that, but at the end of the day, it's I'm in charge of the company.

### **00:32:31**

**Edwin Johnson:** So, it's always on me. Um, and you know, hopefully I won't make that same mistake again.

**George Westbrook:** I think I think Hassan you've got a demo of the trading haven't you?

**Edwin Johnson:** Let's see if it's not make me happy.

**George Westbrook:** I think because it's so what we what we what we will do is get that new test light version but we wanted to make sure that like there was a few UI changes um so Uh, the the some of the interns can start ripping it apart. Um there's still a few minor things. Um but we'll get that we'll get something out in test flight um soon. We just need Yeah, we just need to sort that out. Um you are ready, aren't you?

**Hasan Ahmed:** Oh yeah, let me share my

**George Westbrook:** Yes.

**Hasan Ahmed:** screen. Okay. Um, so yeah. Um, so at first I think I'll speak about a few of the um actual tweaks I made onto the actual homepage. So as soon as you um are as soon as you actually then go I mean cuz like as soon as you you are on the actual app if you then scroll down you actually have your your I mean cuz as in it's your actual wallet with like all of the specific details.

### **00:33:57**

**Hasan Ahmed:** So like invested as in like I did as in like I I um also added in this extra bar as well and so it's a lot more as in as in so as as in so it's easier you to actually understand and also to read it.

**Edwin Johnson:** Yeah, that's

**Hasan Ahmed:** Um so if you click through here it should also they take you here.

**Edwin Johnson:** great.

**Hasan Ahmed:** So I will execute a few trades just as um we were for an example. So let's say for example I want to buy um um I choose um let's say the Cowboys here. Um for the quantity uh let's do let's say 10 shares. Um and then over here if you want to um like the autofill it for like 25 100 um the 250 as well and then also like adjust the actual offer as well. But there's also these options. Um so I'll keep 25 and then if you want to do the expiration date as well.

**Edwin Johnson:** Mhm.

**Hasan Ahmed:** So this opens up as an extra menu.

### **00:35:03**

**Hasan Ahmed:** can either do this one for as so it's until the end of the um I mean so so yeah I think it's until you close it like explicitly and then this is until like a certain day and so it could be a day it could be 3 days it could be

**Edwin Johnson:** session.

**Hasan Ahmed:** a week and so at the moment I just do think day duration so if I buy this like it will give you your actual details and then all of the specifics

**Edwin Johnson:** Cool.

**Hasan Ahmed:** about And then if you place the order, it should do the order placed and then it'll give you an overview. And then if you want to think share, this is all I think at the moment. Like if you want to think share it, it's not like entirely built yet. So if you click share, it's not going to go anywhere right now. But I add that in.

**Edwin Johnson:** Yeah,

**Hasan Ahmed:** Um,

**Edwin Johnson:** Max,

**Hasan Ahmed:** so then if you click Yeah.

**Edwin Johnson:** I'm sorry. Hassan, one quick question.

### **00:35:54**

**Edwin Johnson:** Sorry to interrupt you. Um, this looks again f\*\*\*\*\*\* amazing. Um, when we have an order and let's say you want to put in an order, can you go through that sequence again where you're like, "Oh, I'm going to place a buy order." And then we go to the quantities.

**Hasan Ahmed:** Uh, sure.

**Edwin Johnson:** Yes, sir. Cool.

**Hasan Ahmed:** Yeah.

**Edwin Johnson:** And see how it says uh 25, 100, and 250\. Um,

**Hasan Ahmed:** Yeah.

**Edwin Johnson:** and you can put your cursor on that 100 right now, right? And put in 14 or whatever you want.

**Hasan Ahmed:** Um, yeah. Yeah. So, like it can be a custom.

**Edwin Johnson:** Okay,

**Hasan Ahmed:** So, let's say I want to do like a 27 shares for

**Edwin Johnson:** cool. Yeah. Yeah. Is there any space uh that we can squeeze in that someone you could say

**Hasan Ahmed:** example.

**Edwin Johnson:** max like what's the max you can buy? Because sometimes when I'm trading quickly I'm and I want to get an edge, right?

### **00:36:46**

**Hasan Ahmed:** Yeah.

**Edwin Johnson:** I'm just going to say I don't want to do the math in my head or like get out a calculator know how many shares I can buy that it will just compute the maximum shares

**Hasan Ahmed:** Um I think at the moment I can add that in I mean as an extra option like under the actual

**Edwin Johnson:** later.

**Hasan Ahmed:** quantity. So yeah.

**Edwin Johnson:** Just keep that in mind.

**Hasan Ahmed:** Yeah.

**George Westbrook:** And is that max given your buying power?

**Hasan Ahmed:** I'm assuming.

**Edwin Johnson:** Yes, sir.

**Hasan Ahmed:** Yeah.

**Kevin Murray:** Yep.

**Hasan Ahmed:** So yeah. Um so I'm going to place this trade at the actual offer. If I check the actual price right now, the offer price is 11320\. So, let me buy that. Uh,

**Edwin Johnson:** Yep.

**Hasan Ahmed:** I think they should fill according to the actual bid size. Just check that quickly. And um, yeah. So, like it's been as an over here like it will be automatically filled cuz there's like available the bids for the sh.

### **00:37:43**

**Edwin Johnson:** on the offer side. You are a buyer, right?

**Hasan Ahmed:** Yeah. Um yeah so as in so this is the actual overview of

**Edwin Johnson:** Cool.

**Hasan Ahmed:** each as in each share that you you actually buy. So if I buy another stock for example let's do New York Giants let's do

**Edwin Johnson:** Hassan, let me interrupt real quick again.

**Hasan Ahmed:** 10\.

**Edwin Johnson:** So, apologies. So, you're along there and then automatically you have the cell exit.

**Hasan Ahmed:** Sure.

**Edwin Johnson:** So, that you that to get out of that position, you already have it ready to go. That's

**Hasan Ahmed:** Yeah. So that and then if you click sell like it will

**Edwin Johnson:** safe.

**Hasan Ahmed:** auto as in cuz like it will auto add how much you own for that

**Edwin Johnson:** Yeah. So, what that does Yeah, that's awesome. So basically there's this um you know fat finger phenomenon that like you can like if

**Hasan Ahmed:** share.

**Edwin Johnson:** you're long a lot of times people things start to go bad or good and they freak out instead of hitting the

### **00:38:36**

**Hasan Ahmed:** Yeah.

**Edwin Johnson:** sell button they hit buy again and the next thing you know they're like they're they're double double stuffed and uh you know this is fantastic for um teaching how to trade.

**Hasan Ahmed:** Yeah.

**Edwin Johnson:** Don't you think,

**Troy McDonald Kane:** Yeah.

**Edwin Johnson:** Trey?

**Troy McDonald Kane:** The other thing we're going to have to figure out is a synthetic marker. I know we keep talking about that.

**Hasan Ahmed:** Yeah.

**Edwin Johnson:** I mean, my suggestion is part of the video I would say buy through the offer. You know, like we're going to create a um a video of how to use the app

**Hasan Ahmed:** Please.

**Edwin Johnson:** and you know, we can do something like that in the interim if the market order isn't going to be available. I mean, we still have till the 29th is the first actual college football game.

**Troy McDonald Kane:** right? That's when secondary trading starts. That's when the trading functionality is going to be needed because before that it's just the IPO cards.

**Edwin Johnson:** That's right. Yeah, this looks awesome.

### **00:39:32**

**Edwin Johnson:** And when can we start playing with

**Troy McDonald Kane:** Yeah.

**Edwin Johnson:** this?

**Hasan Ahmed:** Um I mean I think at the moment I'm going to do like a new actual build and then I'm going to add in the actual the test like ad units into that build as well and so then it'll be like a whole

**Edwin Johnson:** Okay.

**Hasan Ahmed:** package. I think I have already onboarded everyone. Um I think I on boarded everyone's emails. And so then as soon as you actually And so as soon as you actually um um I think as soon as you're actually on the um the um app like it should have like a trade button and so if you want to buy so like it should be

**Edwin Johnson:** Cool.

**Hasan Ahmed:** available. Um so on here as well I'm going to demonstrate a cell for example. So I have 27\. I place that. I think it should automatically fill if there's I for that. And then as as in after you actually place a trade, it will update your actual bar as well here.

### **00:40:35**

**Hasan Ahmed:** So uh and let me cancel this order because it's not in the limit. But so um I think I should also let me see if I can do things shorting as well in this. So let's say for example in the Cowboys if I want anything short them let's do 100 shares as in like it will give you like a message as well on how like a short works here and

**Edwin Johnson:** That's

**Hasan Ahmed:** then after you place a short so that's going to

**Edwin Johnson:** awesome.

**Hasan Ahmed:** be that should place properly. Yeah. And then they sell order as in that it was only like partial fill cuz there wasn't like enough left but like it did do I think 70 shares like out of the like 100 orders and then up here.

**Edwin Johnson:** Yeah. And you got 30 left.

**Hasan Ahmed:** Yeah. As in I think for the actual orders you unable to do while trading.

**Edwin Johnson:** Yeah.

**Hasan Ahmed:** So let's say for example I want to cover this and I still have a partial fill.

### **00:41:41**

**Hasan Ahmed:** It's open. So if I want to do this, if like I tried to cover it, like it would tell me that like I still have um actual orders that are resting.

**Edwin Johnson:** Mhm.

**Hasan Ahmed:** And so if I want to actually since if I want to cover it, I need to close. Oh, wait. I just buy up. Okay. I mean I mean I think um he did. Yeah. I mean, I think I think George, he just had bought up the shares that were still available on the

**Edwin Johnson:** Nice work, George.

**Hasan Ahmed:** short.

**Edwin Johnson:** I like the fact that George is up money and Hassan's down money. We can't hear you, George.

**George Westbrook:** If you mute quickly with with shorting,

**Edwin Johnson:** There you

**George Westbrook:** are we going to allow a user to short a stock that they already own or do they have to

**Edwin Johnson:** go.

**George Westbrook:** sell

**Troy McDonald Kane:** So that's a good T0 had a similar question.

**George Westbrook:** first?

**Troy McDonald Kane:** It it's not really logical to short before you have to sell off your existing inventory if you're long.

### **00:42:53**

**Troy McDonald Kane:** Short only exists if you're not long any positions. And so because Edwin, the way that T0 is tracking shorts is we're not doing two coins like a long coin or a short coin,

**Edwin Johnson:** Sure.

**Troy McDonald Kane:** but they are tracking them in separate wallets to track the outstanding shares that are shorted essentially. Like that's the borrow.

**Edwin Johnson:** Yeah. Okay,

**Troy McDonald Kane:** Yeah,

**Edwin Johnson:** cool. Yeah. I mean, you don't get short if you're already long.

**Troy McDonald Kane:** that's right.

**Edwin Johnson:** You got to you got to exit.

**Troy McDonald Kane:** Yeah.

**Edwin Johnson:** And then to be short, you got to be flat.

**Troy McDonald Kane:** Yeah.

**George Westbrook:** H.

**Hasan Ahmed:** Excuse

**George Westbrook:** Okay.

**Edwin Johnson:** It actually reminds me when I first opened an account and they were like, "We got to test trade to make sure it clears." And this a\*\*\*\*\*\*

**Hasan Ahmed:** me.

**Edwin Johnson:** from the clearing firm kept going, "Buy one." And I I bought one. And then he's like, "Sell it." And I was I was I lost like 500 bucks.

### **00:43:41**

**Edwin Johnson:** And I'm like, "Hey, f\*\*\* nuts. Can you at least tell me to sell one first so I can make money back?" It was funny.

**George Westbrook:** Yeah.

**Edwin Johnson:** So I looked at Hassan's thing and reminded me of that. Um, yeah, this would be great to to screw around with and definitely use as a demo because it's the the data is still like just random data, right,

**George Westbrook:** Um, some of it is, but most of it's not,

**Edwin Johnson:** George?

**George Westbrook:** I don't think.

**Hasan Ahmed:** Um I think everything here is actually the market data um through um I think

**George Westbrook:** Now,

**Hasan Ahmed:** it's the yeah if I See if I will

**Edwin Johnson:** Like historically,

**Hasan Ahmed:** try.

**Edwin Johnson:** is it historical? Did it

**George Westbrook:** So, so I think in the QA environment,

**Hasan Ahmed:** So

**George Westbrook:** they've got like a they've got some prices already kind of set. Um, so this is like rather than it being we put in that number and we just randomly change it up and down, this is coming through from the actual market data on T0 side.

### **00:44:36**

**Hasan Ahmed:** 0\.

**Edwin Johnson:** Um, okay. Gotcha. Okay. Very cool. And Troy, we think those are just random numbers, correct? They're not using historical data from

**Troy McDonald Kane:** uh T0.

**Edwin Johnson:** team. Yeah.

**Troy McDonald Kane:** They're pumping in whatever ever they're getting. Yeah. It's all fake data.

**Edwin Johnson:** sport radar and it's in Cody. So then it's just like random

**Troy McDonald Kane:** Yeah.

**Cody Haugen:** Well,

**Edwin Johnson:** prices.

**Cody Haugen:** yeah. I mean, it would just be historical data that they would I mean, there's no games going on,

**Troy McDonald Kane:** Yeah.

**Cody Haugen:** so it'd have to be historical data.

**Troy McDonald Kane:** It's all replay. It's replay data.

**Edwin Johnson:** Gotcha. I mean,

**Cody Haugen:** Yeah.

**Edwin Johnson:** we're making the prices.

**Troy McDonald Kane:** Yeah.

**Edwin Johnson:** They're not making the prices.

**Troy McDonald Kane:** Correct.

**Cody Haugen:** Oh, right.

**Troy McDonald Kane:** Exactly.

**Cody Haugen:** Yeah. So,

**Troy McDonald Kane:** Yeah.

**Cody Haugen:** that's I I guess that's where I was confused.

### **00:45:24**

**Edwin Johnson:** Okay.

**Cody Haugen:** Um, but yes, if they're running off a replay, I mean, Sport Radar has real games that have happened in the past that they are replaying in real time. So, it is a real game.

**Edwin Johnson:** Indeed.

**Cody Haugen:** Yeah. Yeah.

**Edwin Johnson:** Yeah.

**Cody Haugen:** That that did happen and real stats. It's just

**Edwin Johnson:** Gotcha.

**Cody Haugen:** historical.

**Edwin Johnson:** Okay, cool. All right, Cody Bolt, and then I'll see you on the next one.

**Cody Haugen:** Okay, sounds good. Thanks everybody.

**Edwin Johnson:** All right. All right. Is there anything that's needed from us at the moment?

**George Westbrook:** Uh, I don't think so.

**Hasan Ahmed:** Maybe a few questions.

**George Westbrook:** There's going to be a few questions maybe around the market maker which I think most should get covered tomorrow in the T0 call. Um, but apart from that,

**Edwin Johnson:** Did the information I provided you help

**George Westbrook:** yeah. Yeah, there's a few there's a few things I'm still double checking.

**Edwin Johnson:** you?

**George Westbrook:** Um, but no, it did really help cuz it the like what you were saying about like devigging the expected wins.

### **00:46:21**

**George Westbrook:** That's that's really that's really helpful. Um,

**Edwin Johnson:** Right?

**George Westbrook:** and yeah,

**Edwin Johnson:** Because like a total could be like 10 and a half,

**George Westbrook:** look.

**Edwin Johnson:** but the odds are like minus 160\. So it's not 10 and a half.

**George Westbrook:** Yeah.

**Edwin Johnson:** It's like if you were extravagant, it's more like 10.9 or something or 10.85,

**George Westbrook:** Yeah. and and yeah because and then with the because that's one of the things when I was looking at I was like wait so there's the expected games for the season then there's

**Edwin Johnson:** right?

**George Westbrook:** this game which has a probability at the start and then a probability ongoing so where does that get accounted but obviously we've worked that out

**Edwin Johnson:** Yeah. Okay.

**George Westbrook:** now

**Edwin Johnson:** Cool. All right. If there's anything else you need from me, let me know on that front. Okay. And if you want me to be on the TZ call tomorrow,

**George Westbrook:** okay

**Edwin Johnson:** I can do that as well.

**George Westbrook:** lovely

### **00:47:08**

**Jared Sapirman:** George, quick note. Um, can you go back to that? Can you go back to that open order screen?

**Edwin Johnson:** It's Housean's running that

**Jared Sapirman:** Oh, on. Yeah, the buy and sell arrows are the opposite

**Troy McDonald Kane:** Oh

**Jared Sapirman:** direction as to what I've seen on other uh trading applications.

**Hasan Ahmed:** Oh

**Troy McDonald Kane:** yeah.

**Jared Sapirman:** So, that's confusing.

**Edwin Johnson:** man.

**Hasan Ahmed:** yeah.

**Edwin Johnson:** How did Can you see that? Jesus. I My eyes I can't even see

**George Westbrook:** See,

**Edwin Johnson:** that.

**George Westbrook:** that doesn't see I would have thought I I mean I've not looked up a trading

**Troy McDonald Kane:** The reason why is because when you buy,

**George Westbrook:** app.

**Troy McDonald Kane:** you want the market to go up. When you sell, you want the market to go down.

**George Westbrook:** Uh,

**Troy McDonald Kane:** So that's why the arrows go the opposite

**George Westbrook:** see? Oh, cuz I think the buy comes to you.

**Troy McDonald Kane:** direction.

**George Westbrook:** Sell it goes away from you like the actual asset.

### **00:47:53**

**Edwin Johnson:** Yeah,

**George Westbrook:** But flip them. Okay.

**Troy McDonald Kane:** Yeah.

**Edwin Johnson:** the genius. Is I mean, flip the genius. Georgia genius. That's his first time that you've shown anything other than geniusness.

**George Westbrook:** Don't know. I'm going to have to I'm going to have to look myself in the mirror

**Edwin Johnson:** Yeah.

**George Westbrook:** now.

**Edwin Johnson:** Well,

**Troy McDonald Kane:** I mean,

**Edwin Johnson:** don't

**Troy McDonald Kane:** you all are going to be professional traders by the time quant traders by the time we're done with this project.

**Edwin Johnson:** have

**George Westbrook:** Yeah.

**Troy McDonald Kane:** And I know we might just go start a trading firm at this point and just trade

**Edwin Johnson:** We're all going to end up scrapping this and just run.

**Troy McDonald Kane:** all these new sports contracts that get launched because we know all the inside points

**George Westbrook:** Huh? Yeah.

**Troy McDonald Kane:** now.

**Edwin Johnson:** Well, we have a model

**George Westbrook:** I mean,

**Troy McDonald Kane:** That's right.

**George Westbrook:** yeah. About a week and a half, two weeks ago,

### **00:48:31**

**Troy McDonald Kane:** Yeah.

**George Westbrook:** I knew f\*\*\*

**Edwin Johnson:** comprising

**George Westbrook:** all about market making and uh now uh

**Troy McDonald Kane:** Who will be the next save? Well, Sesuana will be the next sports market maker.

**George Westbrook:** Yeah.

**Edwin Johnson:** that might not that might not be that far from reality. I mean, because I definitely got to start trading. I mean, I wanted to like trade in July, but it's really thin in there at the moment. The volumes are s\*\*\* for me. Um,

**Troy McDonald Kane:** You don't want to go trade the 24/7 gold contract.

**Edwin Johnson:** so, not really.

**Troy McDonald Kane:** Edwin

**Edwin Johnson:** Not really. Uh, CME come out today. They're going to do uh options and futures on sports, but they're so f\*\*\*\*\* up. I mean, they're they're not actually a competitor to us.

**Troy McDonald Kane:** It's sports indexes and it's probably starting with the NHL. So, not football, not what most people care about right

**Edwin Johnson:** I mean,

**Troy McDonald Kane:** now.

**Edwin Johnson:** whose idea was Oh, Terry likes coffee.

### **00:49:32**

**Edwin Johnson:** That's

**Troy McDonald Kane:** He's that's that's exactly why.

**Edwin Johnson:** why.

**Troy McDonald Kane:** You got it. Yeah. I was talking to someone about it yesterday and they're like Terry is like the like he would go out and party with the Blackhawks when they won the Stanley Cups.

**Edwin Johnson:** Oh, I know.

**Troy McDonald Kane:** Like that's how connected he is to hockey just like Vinnie Viola is. It's just crazy.

**Edwin Johnson:** Yeah. Well, they both have kids who play hockey.

**Troy McDonald Kane:** That's right. Yeah.

**Edwin Johnson:** Crazy. Okay. Um well, is is there anything else that you need for me,

**Troy McDonald Kane:** Yeah.

**Edwin Johnson:** Brett, other than I will get to the contract and have legal review it? Um I do have an update. The full package for the SEC uh there would go go uh back and forth last night. I think it goes in today. So, I should have that stamped copy for Jim Angel and the rest. And uh that's a great thing.

**Troy McDonald Kane:** That's great to hear. Awesome.

**Edwin Johnson:** Okay. All right. Have a great day all. We'll talk soon.

**Troy McDonald Kane:** All right.

**George Westbrook:** Perfect.

**Troy McDonald Kane:** Thank you.

**George Westbrook:** Let's f\*\*\*\*\*\*

**Edwin Johnson:** Thank you.

**Troy McDonald Kane:** Let's f\*\*\*\*\*\*

**Edwin Johnson:** Thank you,

**George Westbrook:** go.

**Edwin Johnson:** George.

**Troy McDonald Kane:** go.

**Max Kingaby:** J.

**Edwin Johnson:** Please. Please.

**Brett StClair:** Bye.

**Hasan Ahmed:** Nice.

**George Westbrook:** Speak to you soon.

**Brett StClair:** Cheers.

### **Transcription ended after 00:50:37**

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*