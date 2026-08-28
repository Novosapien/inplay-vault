---
date: 2026-08-26
type: standup
description: "Wednesday touchdown, 26 August 2026: the KYC-less onboarding demoed and reworked live, secondary trading set for Thursday 9:30 Eastern, and the Sportradar gap named as a market-maker risk."
source: "Google Meet transcript, Inplay - App - Touchdown (34m 14s)"
scope:
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[compliance/regulatory-positioning]]"
  - "[[ipo-module/ipo-module]]"
  - "[[market-maker/market-maker]]"
  - "[[referral/referral]]"
  - "[[delivery/delivery]]"
status: extracted
extracted-to:
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[compliance/regulatory-positioning]]"
  - "[[compliance/eligibility-and-age-gating]]"
  - "[[ipo-module/ipo-module]]"
  - "[[market-maker/open-questions]]"
  - "[[market-maker/plan]]"
  - "[[market-maker/sessions/2026-08-26-touchdown-digest]]"
  - "[[referral/referral]]"
  - "[[leaderboard]]"
  - "[[app-store-accounts]]"
  - "[[delivery/delivery]]"
---

## Post-Call Analysis

34 minutes on the **final day of the NCAA IPO**, with the window due to close at
**10pm that night**. Present: Troy, Cody, Kevin, Jared (InPlay) and George,
Brett, Hasan, Lily (Novosapien). **Edwin joined at roughly the 24-minute mark**,
having worked until 4am, so the first two thirds ran without him and Troy took
the decisions, explicitly flagging that he would take them back for Edwin's
sign-off. Lily was introduced to the client on this call.

**The KYC-less path is built, and the call turned into a live design review of
it.** Hasan demoed it end to end. The flow is unchanged until near the end:
date of birth, email, verification code, create account. Then the identity check
appears with a skip, and the user can trade without an ID document or a face
scan. **Four changes came out of the demo, and all four are worth holding:**

1. **The skip is buried.** _"I'll do it later"_ sits below the fold. Cody and Troy
   both want it at the top or as a popup. Troy's reasoning is the useful part:
   _"people will be like ugh because they don't even know that that's even an
   option at that point and they may just give up and not even scroll."_
2. **The fork should be its own screen, straight after the email code.** Cody
   pointed back at Edwin's own example: land on a page and **choose your route**,
   rather than discovering the choice buried inside a KYC screen. Kevin agreed,
   Troy agreed, Hasan confirmed it can work that way. This is the 17-08 "choose
   your competition" screen logic applied one level earlier, at verification.
3. **The word "simulated" goes in front of "trading" everywhere.** Cody:
   _"start trading now… that seems to me reads like regulatory brokerage account
   or maybe too close to it."_ Troy: _"Put simulated in there. Activate simulated
   trading."_ Kevin: _"pretty much just add simulated in before trading and pretty
   much everything should be good."_ **This is a compliance-driven copy rule, not
   a preference.**
4. **The term "KYC" comes out of the interface.** Troy: _"KYC is not a term that
   really resonates with everyone."_ After debating "identity verified", "ID
   verified" and "IDification", the group landed on the shortest version:
   **"get verified"** on one side and **"start trading without verification"** on
   the other, on the grounds that the age statement already makes it implicit.

**Three onboarding defects and asks, in increasing size.** The **date of birth
field puts day before month**, which is backwards for a US audience (Jared;
George: _"you Americans do it wrong. We'll change it."_). **SMS verification
instead of email** was asked for and is the more interesting one, because Jared
has the user research: people do not want to leave the app, and the Gmail
autofill prompt _"didn't pop up on mine. That didn't pop up on my friends
either."_ George: doable via **Twilio**, but _"not a done in a day"_. **Apple and
Google one-click sign-in** was asked for by Troy; George: doable, provider choice
needed, and Google's own verification is arduous, _"one of the things that we
can't speed up with AI."_ Both are recorded as future work, neither committed.

**The switch to secondary trading has a time on it: Thursday 27 August, 9:30
Eastern.** Troy chose the morning deliberately over flipping it at IPO close:
_"we should wait until the morning to do it because then we're all on and can
actively be looking at it in submitting orders"_, so there is **QA on the open**,
checking the locks actually came off. Two days before the first games, so little
trading is expected; the point is that people can test.

**The prize pool for week zero exists, and Troy had it wrong.** He assumed no cash
pool for the first week; **Edwin corrected him: _"No, we are."_** Sizing follows
the standing rule of thumb, **roughly three dollars per competitor**, against
**187 verified users** and **278 downloads**. To be decided within a day and
**published Friday**. ⚠ **There is no prize pool page in the app** (George), so
the announcement links to the website.

**The numbers, stated plainly.** 187 verified, 278 downloads, so **roughly 90 more
downloads than completed verifications**, which is exactly the gap the KYC-less
path is meant to close. Edwin's caveat: the first batch is _"primarily all of us
in our networks"_. The **interns started this week**, some already back on campus
working involvement fairs with scripts and content.

**The Sportradar gap is now a named market-maker risk, not just an annoyance.**
George: without that data _"the market maker is going to be way more volatile than
it needs to be. Like it might just drop off."_ He will keep testing and look at
workarounds before the first game day, and called it a risk in terms. Cody has
escalated: Sport Radar say it will be fixed _"absolutely before Saturday"_, with
**three engineers on a bug that has been open for a couple of weeks**, and if they
miss it **InPlay gets a credit on the bill**. Plan: pull the endpoint once or twice
a day, Cody pressures them again today.

**The app icon and name are still frozen, but the two were separated.** Hasan:
changing the **name** needs a fresh app store check, _"at least like a week"_.
Troy: the **icon** can probably change without a review since apps do it often,
and asked whether the icon alone can be simplified first. Cody held everything
until the Viral contract is settled; the kickoff happened on 25 August.

**Two commercial items are stalled.** The **warmed-up email outreach to marketers
has not started**: Brett reported a run of bugs after the reconfiguration, with
George and Vineth working through them. And the **Wayne introduction** in New York
has had no traction despite Brett nudging every second week.

| Finding | Destination | Action |
|---------|-------------|--------|
| KYC-less onboarding **built and demoed** end to end | [[customer-onboarding/customer-onboarding]] | Update written |
| The skip is below the fold; move it to the top or make it a popup | [[customer-onboarding/customer-onboarding]] | Requirement |
| **The fork becomes its own screen straight after the email code** | [[customer-onboarding/customer-onboarding]] | Requirement |
| **"Simulated" goes in front of "trading" everywhere**, a compliance copy rule | [[compliance/regulatory-positioning]], [[customer-onboarding/customer-onboarding]] | Rule recorded |
| **"KYC" comes out of the UI**: "get verified" and "start trading without verification" | [[customer-onboarding/customer-onboarding]] | Requirement |
| Date of birth field shows day before month; wrong for a US audience | [[customer-onboarding/customer-onboarding]] | Defect recorded |
| SMS verification via Twilio asked for; not a day's work | [[customer-onboarding/customer-onboarding]] | Future work |
| Apple and Google one-click sign-in asked for; provider choice and Google's own review | [[customer-onboarding/customer-onboarding]] | Future work |
| IPO window closes **22:00 Wed 26 Aug**; buttons lock | [[ipo-module/ipo-module]] | Recorded |
| **Secondary trading opens Thursday 27 Aug, 9:30 Eastern**, morning chosen for QA on the open | [[ipo-module/ipo-module]], [[delivery/delivery]] | Decision recorded |
| **Week-zero prize pool confirmed by Edwin**, ~$3 per competitor, published Friday | [[delivery/delivery]] | Recorded |
| **No prize pool page in the app**; announcement links to the website | [[leaderboard]] | Gap flagged |
| Comms: newsletter tomorrow and Friday, plus a push alert to the prize pool | [[delivery/delivery]] | Recorded |
| **187 verified, 278 downloads**; the ~90 gap is what KYC-less targets | [[delivery/delivery]] | Recorded |
| Interns live this week on campus with scripts | [[delivery/delivery]] | Recorded |
| **Sportradar gap will make the market maker over-volatile, possibly dropping off** | [[market-maker/open-questions]], [[market-maker/plan]] | S12 escalated |
| SR: three engineers, fix promised before Saturday, bill credit if missed | [[market-maker/open-questions]] | Recorded |
| Referral multiplier stays **5× to 30 August**, covering the first game day | [[referral/referral]] | Confirmed |
| App **icon** may change without review; the **name** needs one, about a week | [[app-store-accounts]] | Split recorded |
| Warmed-up marketer outreach **has not started**, blocked on bugs | [[delivery/delivery]] | Recorded |
| First-run step-by-step guide targeted for end of week | [[customer-onboarding/customer-onboarding]] | Recorded |
| Wayne introduction, no traction | Not applicable | No action |

---

Aug 26, 2026

## **Inplay \- App \- Touchdown \- Transcript**

### **00:00:32**

**Hasan Ahmed:** Hey baby.

**George Westbrook:** Head

**Brett StClair:** Is everyone in? Do I let everyone in?

**Hasan Ahmed:** Hey

**Brett StClair:** Hello.

**George Westbrook:** Oh,

**Brett StClair:** Hello.

**Cody Haugen:** There we go. Hello all.

**George Westbrook:** how we doing?

**Cody Haugen:** Oh, so busy, George.

**George Westbrook:** Good,

**Brett StClair:** f\*\*\*.

**George Westbrook:** busy, bad, busy, or just busy busy?

**Cody Haugen:** Uh, good busy um for the most part. But yeah, I'm looking at my schedule today and it's like I've got 45 minutes for 10 hours of calls. 45 minutes not on calls for 10 hours of calls.

**George Westbrook:** Well, at least you get to

**Cody Haugen:** Well,

**George Westbrook:** eat.

**Cody Haugen:** maybe yesterday was a uh was a pretzel and cheese dip lunch. So, but for Wisconsin night, that's like a dream.

**George Westbrook:** I suppos maybe one of the calls you're going to have to pretend your camera's broken for the first 10 minutes and your mic's not working. So, it's just then you accidentally turn it on and it's like,"Oh,

**Cody Haugen:** on on one of the podcast calls with Kevin.

### **00:01:57**

**George Westbrook:** s\*\*\*."

**Cody Haugen:** I'll just tell him to lead it. Yeah.

**George Westbrook:** That's a Yeah, one one way to do it,

**Cody Haugen:** Yeah.

**George Westbrook:** right?

**Cody Haugen:** Kevin was getting the lunch brought to him too yesterday, though. It's uh he's he's on just as many calls.

**George Westbrook:** That's not

**Cody Haugen:** No, it's it's a good problem. Like this this this podcast uh AI engine that we've worked with is generating just

**George Westbrook:** bad.

**Cody Haugen:** nothing but hundreds of leads and podcasts that we get to speak on. And we did another two last night and and you know intro calls all day. So no, it's it's good. It's really good. And we had a really good call last night. I was with uh the guys talking. We did our spiel and you know 15 and then they asked us to hang around for another 45 and talk football and talk shop. So yeah it was a good show.

**George Westbrook:** Nice.

**Brett StClair:** It's a nice medium. I really like podcasting.

### **00:02:56**

**Brett StClair:** I love listening to it.

**Cody Haugen:** Yeah.

**Brett StClair:** I love doing it. Threats. It's really really awesome, you know. And and you're in the person's head. It's such a special experience to be there, right? Oh,

**Cody Haugen:** Agreed.

**Brett StClair:** nice. Well done. Well, you must send us one of your podcasts so we can uh become

**Cody Haugen:** Yeah, they're Yeah. No, no,

**Brett StClair:** fan.

**Cody Haugen:** they're they're trickling in um as far as recordings and stuff. So, yeah, we'll have to share one over.

**Kevin Murray:** Yeah,

**Brett StClair:** Very very cool.

**Kevin Murray:** we'll start uh trying to get them all linked up onto the the socials and bits and pieces and YouTube and stuff as well once they once they come in.

**Brett StClair:** Very very cool. So, are most of them not live? Right. It's pre-recorded. They're not doing a live stream.

**Cody Haugen:** Uh, one last night was live. Um, but yes, I would say generally they are pre-recorded just because timing of their timing,

### **00:03:43**

**Brett StClair:** Okay.

**Cody Haugen:** our timing. Um, and then snip it in. But yeah, one last night was live. the the later

**George Westbrook:** I bet I bet the live ones are a bit bit more nerves than that one.

**Cody Haugen:** one.

**George Westbrook:** You're like,"s\*\*\*, this is this there's no undos on

**Cody Haugen:** No, no, no. There's no undos or or uh scrapping on any of

**George Westbrook:** this.

**Kevin Murray:** Yeah.

**Brett StClair:** So,

**Cody Haugen:** that.

**Brett StClair:** we forgot to introduce Lily last time. She's one of the new team members and apparently she might be related to me.

**Cody Haugen:** I couldn't guess what the names

**Kevin Murray:** Sorry to hear that. Lily,

**Brett StClair:** Sorry.

**Kevin Murray:** welcome

**Cody Haugen:** Welcome.

**Lily StClair:** Thank you.

**Cody Haugen:** Welcome to the Nice to meet you as well.

**Brett StClair:** Cool. Should we kick off or are we waiting for

**Cody Haugen:** Yeah, Troy, you're on

**Brett StClair:** Edwin?

**Troy McDonald Kane:** I've been on mute this whole time I've been talking.

**Cody Haugen:** mute.

**Troy McDonald Kane:** Uh we missed all my jokes.

### **00:04:46**

**Troy McDonald Kane:** So I I and I'm not going to repeat them,

**Brett StClair:** These guys are rude.

**Troy McDonald Kane:** but uh we should get started while we uh we wait for Edwin to join. Um so maybe a good place to start is where you guys are with re reducing or removing the KYC layer of the app.

**Brett StClair:** Oh, you have some.

**George Westbrook:** That's

**Brett StClair:** Do you want a demo? Time for a demo, ladies and

**Hasan Ahmed:** Yeah,

**Brett StClair:** gentlemen.

**Hasan Ahmed:** let me join on my phone. Um, are you are you using your AirPod mic? Yeah, I am. Oh,

**Brett StClair:** f\*\*\*. This is like the worst experience on your AirPod

**Hasan Ahmed:** yeah. Um,

**Brett StClair:** mics.

**Hasan Ahmed:** cool. Yeah,

**Troy McDonald Kane:** Thank

**Hasan Ahmed:** I'll start off on the actual onboarding page. Um, everything on here is pretty much the exact same except after you enter your like name, it will ask for like that's Yeah, Beth. So, you need to fill out your mic.

### **00:06:03**

**Hasan Ahmed:** Um, let me just your earbuds. I don't know. It's nothing. I'm

**Brett StClair:** Can Can someone write up a a son's f\*\*\*\*\*\*

**Hasan Ahmed:** just

**Brett StClair:** AirPod checkboard and every time we'll mark one down as a

**George Westbrook:** We're burning them.

**Kevin Murray:** Go a f\*\*\*. Can you

**Brett StClair:** failure?

**Kevin Murray:** pay?

**Brett StClair:** We have That's not That's not ears. That's probably the problem. That's why you

**Jared Sapirman:** There was feedback that I got on this screen specifically that uh the days first before the month

**Brett StClair:** gurgling.

**Jared Sapirman:** and it normally is flipped in the

**George Westbrook:** Yeah,

**Jared Sapirman:** US.

**George Westbrook:** you Americans do it wrong. We'll change it.

**Jared Sapirman:** Okay.

**Brett StClair:** I'd love to know why that's the case. I don't know

**Kevin Murray:** I don't know.

**Hasan Ahmed:** Um,

**Kevin Murray:** It took me a while to figure it out because I was always like day, month, and then year for

**Brett StClair:** who's

**Hasan Ahmed:** one

**Kevin Murray:** ages.

**Troy McDonald Kane:** I mean, do does the US do anything right these days?

### **00:07:12**

**Jared Sapirman:** Yeah, we don't have the metric system.

**Troy McDonald Kane:** I mean, we're we're not on the metric system.

**Jared Sapirman:** We

**Troy McDonald Kane:** We we reverse our birthdays.

**Jared Sapirman:** don't

**Troy McDonald Kane:** We drive on the wrong side of the street. So, yeah.

**Brett StClair:** Kevin must be a mess

**Hasan Ahmed:** Um

**Kevin Murray:** I'm

**Brett StClair:** there.

**Kevin Murray:** I'm

**Brett StClair:** He's blubbering.

**Hasan Ahmed:** yeah. Um hello.

**George Westbrook:** What?

**Hasan Ahmed:** Is this better? Yeah. Okay.

**Kevin Murray:** Yeah.

**Troy McDonald Kane:** Yes.

**Hasan Ahmed:** So um over here um you would enter your day of birth. So just put mine in quickly. Um, let me use a test email. Um, testing I mean as in the like entire thing on boarding flow is pretty much the exact same like except for a part um close to the like I'll say the end of it. So if I go through here, you enter your code like normal. Uh create account. Uh wait for this to come.

### **00:08:24**

**Hasan Ahmed:** There we go. And so as in so um I think at first like it will give you your entire KYC screen and if you and then if you don't want to do it and you want to skip past it say like I'll do this later and then it will ask you if you want to start trading now and then like it will just say I mean you like are able to actually think start trading but but you don't need to to actually handle the ID or like scan your face or anything. So on here like what you do is enter your enter your name. So, and then do you think open my trading account?

**Cody Haugen:** So, two things real quick. I think that I'll do it later might be too buried. Um, if we go back to Yeah, if we go back to Edwin's example,

**Hasan Ahmed:** Yeah.

**Cody Haugen:** right? It it brought you into the homepage and from the homepage you selected what route you wanted to go down. Um,

**Hasan Ahmed:** Yeah.

**Cody Haugen:** that that's my first bit of feedback and I'll let the team see if that's consensus or not.

### **00:09:28**

**Cody Haugen:** And then um second thing before you click that orange button uh do we need to add um simulated trading in that it said open or start trading now? Uh that seems to me reads like regulatory uh brokerage account or maybe two close to it.

**Troy McDonald Kane:** Right.

**Cody Haugen:** So like open your s or start simulated trading now or something like that just to make sure we're

**Hasan Ahmed:** H.

**Cody Haugen:** all covered there.

**Troy McDonald Kane:** Yeah, good points.

**Hasan Ahmed:** Yeah.

**Troy McDonald Kane:** Uh, Cody,

**Cody Haugen:** Yeah. Do you agree that that I'll do that later was kind of buried down

**Troy McDonald Kane:** yeah, I I was thinking it should be towards the top or like one of the first buttons that you see.

**Cody Haugen:** there?

**Troy McDonald Kane:** you shouldn't have to scroll because then people will be like gh because they don't even you have to scroll to see it and

**Hasan Ahmed:** Mhm.

**Troy McDonald Kane:** they don't even know that that's even an option at that point and they may just give up and not even scroll.

**Cody Haugen:** Yeah.

### **00:10:15**

**Hasan Ahmed:** Yeah.

**Troy McDonald Kane:** So it should be very obvious uh or or a popup or something that is easy to just skip if they want in the in the first

**Cody Haugen:** Hassan,

**Hasan Ahmed:** Okay.

**Cody Haugen:** what about this? Hassan, what about this?

**Troy McDonald Kane:** stage.

**Cody Haugen:** What if we added an orange button to the top of that that just said start simulating tra

**Hasan Ahmed:** Yeah.

**Cody Haugen:** start simulated trading now? You know, do KY or identity verification later if you want or something along those lines across the top with just a bright orange button. So like the way you have it now on the homepage that that's where the

**Hasan Ahmed:** Yeah.

**Cody Haugen:** landing should be, right? You have your two forks there and they can pick one of um in that.

**Hasan Ahmed:** Okay.

**Kevin Murray:** So after you Yeah, it's after you put your email in and then you get that confirmation code.

**Hasan Ahmed:** Yeah.

**Troy McDonald Kane:** Yeah.

**Cody Haugen:** Yeah.

**Kevin Murray:** Once you put that in and then click next, it should bring you to this page here now.

### **00:11:10**

**Kevin Murray:** And then you can pick either one of those is what I think anyway, but I'll revert back to the theme as

**Hasan Ahmed:** Okay.

**Troy McDonald Kane:** No, I agree.

**Hasan Ahmed:** I think

**Troy McDonald Kane:** If we can remove a couple hops because we want them to get to the screen so they can see the screen as soon as possible.

**Kevin Murray:** well.

**Hasan Ahmed:** Yeah.

**Troy McDonald Kane:** We understand to get a trading account, it's going to take a minute to get it permission, get the wallet set up and give them their buying power. So, that that that's fine. But, um, we want there to, you know,

**Hasan Ahmed:** Yeah.

**Troy McDonald Kane:** even waiting for the confirm to come in for the email sometimes is annoying, but it is a necessity, you know, because your email may not be refreshing fast

**Jared Sapirman:** And a question on that,

**Troy McDonald Kane:** enough.

**Hasan Ahmed:** Yeah.

**Jared Sapirman:** is there a way to do it where we do a cell phone instead phone number? because that's how multiple apps that I've interacted with recently have their verification process and it's much quicker.

### **00:11:59**

**Jared Sapirman:** than me having to go to check my email to then come back to put that code in. If I just have it pop up as a text message, it's easy to just put that right right into the uh the

**George Westbrook:** can be done,

**Hasan Ahmed:** can be done. But there's a taste.

**George Westbrook:** but there's a Oh,

**Jared Sapirman:** verification

**George Westbrook:** wait. Mute yourself. Yeah, it can be done, but there's a decent amount of work that goes into it because we have to not not ridiculous amounts, um, but enough where it's not a done in a day. We have to link to Twilio, um, set up the the organization, um, verify it, and then then get it sending. But it is possible. I agree with you. It's is quicker, um, and is better. So definitely an iteration or an improvement we can

**Jared Sapirman:** cuz that's other feedback that I've gotten where people are like multiple people who I've talked to about the

**George Westbrook:** add.

**Jared Sapirman:** onboarding process, they've said,"Ah, I don't want to have to exit out of my app, go open my email, take a picture, or remember that verification code, go back to the app, put that verification code in because it just pops up on their um on their messages, they can do what then that thing doesn't always come up um on I'm uh on on the keyboard for email.

### **00:13:14**

**Jared Sapirman:** That um button that you could press where it says from Gmail, that doesn't always pop up. That didn't pop up on mine. That didn't pop up on my friends either. With the message, it almost always does.

**Hasan Ahmed:** Okay.

**Troy McDonald Kane:** It could be a setting in the mail app maybe but uh but yeah that's fair Jared um is there also a way another piece of feedback you know that for the app store or from through the app store they can use their Gmail or their Apple or Google credentials like the oneclick option or is that another difficult like It doesn't have to be there right away, George, but I think over time it'd be good to get those buttons there because as you know, a large majority of apps now, it's like, you know, log in with an email or just log in with your Apple ID or your or your Apple account or your Google account

**George Westbrook:** H.

**Troy McDonald Kane:** and it's like a one-click like verification's much easier that way as well.

**George Westbrook:** Yeah.

### **00:14:10**

**Troy McDonald Kane:** It reduces a couple hops. Um, so if we could get that on the pipeline of getting integrated is I don't know what that looks like or how that works, but if you're already in the app stores, I would imagine that it should be easy to integrate those buttons,

**George Westbrook:** it. So, obviously 100% doable.

**Troy McDonald Kane:** but

**George Westbrook:** It's just we need to decide what providers blah blah blah. I've done the Google ones before and they are such a ball. It's just you got to do video. It's is it's think of it like what you do for the app store but just a really a lot more simple. So it's not as not as arduous, but there's still a process. It's it's one of the things that we can't speed up with AI. Um, so 100% once again doable. Just it's not a let's just add it.

**Troy McDonald Kane:** Yep. Yeah, we like I said, we can put it on the um the to-do list for the

### **00:15:05**

**Hasan Ahmed:** Um I mean I was going to show something as well.

**Troy McDonald Kane:** future.

**Hasan Ahmed:** So if you had to then skip this page and you were to skip this page and it go onto the homepage here like there's these options here like if you want to do it without the KYC or then if you want to go straight into the KYC and so then how I mean I was how I understand it is um after you enter your email and then it gets um actually as in after the actual email step like it should go straight Okay. And then on here if you do KYC.

**Cody Haugen:** Yes. Yes. Agreed. Yep. And then from here,

**Hasan Ahmed:** Okay.

**Cody Haugen:** you go back into that page you just showed us that this page.

**Hasan Ahmed:** Yeah. Like that. And then if you And then if you choose the other option,

**Cody Haugen:** Yep.

**Troy McDonald Kane:** Yeah.

**Cody Haugen:** Got it.

**Hasan Ahmed:** it will then give you this.

**Jared Sapirman:** Sure.

**Cody Haugen:** Yep.

### **00:15:54**

**Cody Haugen:** Perfect.

**Hasan Ahmed:** Yeah.

**Cody Haugen:** And then once again

**Troy McDonald Kane:** Put simulated in there. Activate simulated trading.

**Hasan Ahmed:** Yeah. Yeah.

**Kevin Murray:** Yeah,

**Hasan Ahmed:** Okay.

**Cody Haugen:** Y

**Kevin Murray:** pretty much just add simulated in before trading and it and pretty much everything should be

**Troy McDonald Kane:** Yep.

**George Westbrook:** Okay.

**Hasan Ahmed:** Okay.

**Kevin Murray:** good.

**Hasan Ahmed:** Um,

**Cody Haugen:** cool.

**Hasan Ahmed:** yeah.

**Cody Haugen:** Well,

**Jared Sapirman:** Troy,

**Cody Haugen:** we're

**Hasan Ahmed:** Um,

**Jared Sapirman:** I believe that something you said on this page was we're going to remove

**Cody Haugen:** almost

**Hasan Ahmed:** up

**Jared Sapirman:** slashchange the KYC moniker because most people don't understand

**Troy McDonald Kane:** Yeah. Or put put under Can we Yeah.

**Jared Sapirman:** that.

**Troy McDonald Kane:** So KYC is not a term that really resonates with everyone. So we can just I think uh get I can we change that to say

**Jared Sapirman:** Just leave it

**Troy McDonald Kane:** get identity verified instead of KYC.

**Jared Sapirman:** as

**Troy McDonald Kane:** So just replace KYC with identity or identification get identification ver verified.

### **00:16:47**

**Hasan Ahmed:** Okay. Yeah. Yeah. I mean, yeah. No, no, it's not an issue if you want to change the the wording.

**Troy McDonald Kane:** Yeah. And then and then on the other one just say start trading without

**Hasan Ahmed:** Yeah. Yeah.

**Troy McDonald Kane:** verification.

**Kevin Murray:** Yeah.

**Hasan Ahmed:** Okay, cool. Um yeah,

**George Westbrook:** Yeah.

**Hasan Ahmed:** I think that's

**Kevin Murray:** Would you Troy just a quick one?

**Troy McDonald Kane:** Okay.

**Kevin Murray:** Would you use like ID like in the US or not?

**Hasan Ahmed:** everything.

**Kevin Murray:** Or is like that's just more like a British thing cuz like instead of like identification just put like

**Jared Sapirman:** I think that's fine.

**Kevin Murray:** ID on it just to keep it a little bit shorter so it's

**Troy McDonald Kane:** Yeah,

**Jared Sapirman:** IDification.

**Troy McDonald Kane:** that's

**Jared Sapirman:** Get that make sense.

**Kevin Murray:** not all over the screen.

**Jared Sapirman:** You can put get IP.

**Kevin Murray:** get ID verified or not trading without ID sort of

**Troy McDonald Kane:** Yeah.

**Jared Sapirman:** Yeah,

### **00:17:33**

**Kevin Murray:** thing.

**Hasan Ahmed:** Yeah.

**Jared Sapirman:** that works.

**Cody Haugen:** Yeah, I think it makes

**Kevin Murray:** Okay,

**Cody Haugen:** sense.

**Troy McDonald Kane:** Yeah. Or even don't even need ID in there if you just say I mean the way you have it described get verified start

**Kevin Murray:** verified

**Jared Sapirman:** That's what I said originally.

**Troy McDonald Kane:** trading verif.

**Cody Haugen:** Thanks,

**Jared Sapirman:** I think that's the way to go.

**Troy McDonald Kane:** Yeah. So we don't even have to put ID in there because it says you need to be of these ages. So that's what you're doing the verification It's pretty implicit. So, yep. All right.

**Cody Haugen:** Yep.

**Troy McDonald Kane:** Cool.

**Hasan Ahmed:** Yes.

**Troy McDonald Kane:** Um, so we have the, uh, we're in the final day of the IPO draft for the NCAA teams. It is set to, um, go off at 10:00 tonight, right? I think, um, Novo team. Let me see what the clock says. Yeah, 12 hours left.

### **00:18:29**

**Troy McDonald Kane:** uh 11 minutes. So then at that time all the buttons just lock. Is that right? That have credentials.

**George Westbrook:** Yeah. And then just to is it are we waiting till tomorrow or as soon as that happens then secondary

**Troy McDonald Kane:** I was hoping Edwin was going to be on this call to kind of give that direction,

**George Westbrook:** starts.

**Troy McDonald Kane:** but right now let's just plan to unlock the buttons tomorrow morning. I mean, we're going to be two days before game day,

**George Westbrook:** Okay.

**Troy McDonald Kane:** so I don't know that there's going to be a lot of trading, but we at least want to give people the ability to buy and sell, test it out a little bit if they want before Saturday. Also, um Cody and Kevin, we should probably get uh email out if not uh tonight, first thing tomorrow morning before we transition to secondary trading announcing that we've moved into secondary trading and that the trading competition is open. But I assume at this point we're not doing a prize pool for week zero or week one.

### **00:19:23**

**Troy McDonald Kane:** This first week.

**Kevin Murray:** Don't think

**Troy McDonald Kane:** Yeah.

**Cody Haugen:** Yeah, I mean at this point based on the call yesterday,

**Troy McDonald Kane:** Okay.

**Kevin Murray:** so.

**Cody Haugen:** I would also assume

**Troy McDonald Kane:** Okay.

**Cody Haugen:** no.

**Troy McDonald Kane:** So, um I don't know if there's a way that we want to just articulate that that this first week is more of a like dry run trial

**George Westbrook:** Okay. All

**Troy McDonald Kane:** run before the cash prizes or not even mention it. But um we need to think about how we want to communicate that for tomorrow so people know that it's open for secondary trading and that the 138 teams will be live during their games on

**Cody Haugen:** Yeah,

**George Westbrook:** right.

**Cody Haugen:** I mean we could put in something catchy like use,

**Troy McDonald Kane:** Saturday

**Cody Haugen:** you know, use this week just like the college teams do to warm up and learn the

**Troy McDonald Kane:** and get your referral bank up.

**Cody Haugen:** buttons.

**Troy McDonald Kane:** That's what we should really be pushing.

**Cody Haugen:** Yeah.

### **00:20:06**

**Cody Haugen:** And get your tra tra Yeah.

**Troy McDonald Kane:** Get that referral bank up. Yeah.

**Cody Haugen:** Get your trading reserve up. Um, Hassan,

**Kevin Murray:** Yeah.

**Cody Haugen:** just real quick on that, can you send me an updated CSV list? Um, since we still uh need to update all the uh new names that have signed up for email when you get a job.

**Hasan Ahmed:** Um,

**Troy McDonald Kane:** And

**Hasan Ahmed:** hey Jared.

**George Westbrook:** I did

**Hasan Ahmed:** Yeah, I can send that over.

**Kevin Murray:** Cool.

**Cody Haugen:** Yeah, I appreciate it. Thank

**Troy McDonald Kane:** and Cody,

**Cody Haugen:** you.

**George Westbrook:** it.

**Troy McDonald Kane:** do we want to do any type of multiplier for Saturday since the first live game day?

**Cody Haugen:** Well, it's already 5x till the end of the

**Troy McDonald Kane:** Oh, it's still 5x. I thought that was going away at launched. So, it's still 5x going into game day.

**Kevin Murray:** Yeah,

**Cody Haugen:** Yeah.

**Kevin Murray:** till the end of the

**Troy McDonald Kane:** Oh,

**Cody Haugen:** The 30th.

### **00:20:46**

**Troy McDonald Kane:** till the end of the month. Okay. So, Monday. Okay,

**Cody Haugen:** Yep.

**Troy McDonald Kane:** great.

**Kevin Murray:** month.

**Cody Haugen:** Yep. So, we're covered there.

**Troy McDonald Kane:** All right.

**George Westbrook:** I think. What did you

**Troy McDonald Kane:** Were there any other onor issues that we've noticed over the last couple days that are new that we need to bring to the Novo team's attention?

**Kevin Murray:** No, the only thing I'd like to see is you know what how Edwin had it on when he was showing the the app there George you know where it was like doing the step by step to get into it if that's Yeah.

**George Westbrook:** Yeah, that's one thing on our list.

**Kevin Murray:** Okay. Perfect.

**George Westbrook:** Yeah,

**Kevin Murray:** Cool.

**George Westbrook:** but like a not a on the list later down the line. Like on a list.

**Kevin Murray:** So now it's next couple of weeks or whatever.

**George Westbrook:** Yeah. Yeah.

**Kevin Murray:** Yeah.

**George Westbrook:** Well, I mean,

**Kevin Murray:** As we move through All

### **00:21:24**

**George Westbrook:** ideally we want to get it get it there by the end of the week. Um,

**Kevin Murray:** right,

**George Westbrook:** I think for the for that just obviously a bit of testing.

**Kevin Murray:** cool.

**George Westbrook:** Um,

**Kevin Murray:** I wasn't sure how long this you say.

**George Westbrook:** but I think the only but

**Troy McDonald Kane:** Um,

**Kevin Murray:** So,

**George Westbrook:** I I I think the only thing that what where is that sports radar data,

**Troy McDonald Kane:** yep.

**George Westbrook:** Cody? Um,

**Cody Haugen:** Is it still up there,

**George Westbrook:** because it it it's there was a bit of improvement.

**Cody Haugen:** George?

**George Westbrook:** Um, but I'll test again straight after this. But the the issue with that is what what's going to happen is that the the market maker is going to be way more volatile than it needs to be. Like it might just drop off after um need to do some testing, but until that until we get that data, um, we don't know. We can we can do some I don't want to call them hacks, but maybe different ways of doing it.

### **00:22:16**

**George Westbrook:** But that's what we're going to be working on until before that first game day. Um, which obviously is is a risk. Um,

**Cody Haugen:** Yeah. I mean, they said it will be fixed um absolutely before Saturday.

**George Westbrook:** so

**Cody Haugen:** They have three, you know, three specific engineers trying to fix this bug that's been in there for a couple of weeks now. Um, and if they don't, then we're going to get a credit of some sort on our bill, but I'd rather obviously have the data and not run the risk. Um, okay. Well, yeah, just keep keep p uh pulling it, you know, once or twice a day. Um, I mean, what? Yeah, what is it? Wednesday now. So, yeah, I mean, keep pulling it once or twice a day just to see if they do have it fixed um before that. But um I will reach out to them uh again today just you know pressuring them saying obviously we're paying attention that it's not

**George Westbrook:** Yeah,

**Cody Haugen:** fixed.

### **00:23:15**

**George Westbrook:** that' be and I think I think apart from that there it's just buckle down the the hatches and prepare for um prepare for

**Cody Haugen:** Yeah.

**Troy McDonald Kane:** Yeah.

**George Westbrook:** secondary.

**Cody Haugen:** Yeah. I went Oh,

**Troy McDonald Kane:** and George and team I don't know if it makes sense that uh

**Cody Haugen:** there it is.

**edwin:** You

**Troy McDonald Kane:** you know we when we move to secondary trading we try to do some

**edwin:** know,

**Troy McDonald Kane:** beta testing right away or not beta testing QA testing way in the to make sure that the lock keys came off things like that um so we'll we'll be that's another reason why I think

**George Westbrook:** Come on.

**Troy McDonald Kane:** we should wait until the morning to do it because then we're all on and can actively be looking

**edwin:** the

**Troy McDonald Kane:** at it in submitting orders. Now,

**George Westbrook:** Yeah.

**Troy McDonald Kane:** the one thing I would recommend if possible we do and we'll take it back to make sure Edwin's okay with it is since I'm sorry.

**edwin:** I'm on now, Troy.

### **00:24:06**

**Troy McDonald Kane:** Oh, you're on now.

**edwin:** Yeah, I apologize. I worked till about 4:00 a.m.

**Troy McDonald Kane:** Okay.

**edwin:** here and literally just woke up.

**Troy McDonald Kane:** Uh,

**edwin:** So,

**Troy McDonald Kane:** no worries. Yeah.

**edwin:** apologies.

**Troy McDonald Kane:** Uh, we're just talking about so the couple quick updates for you Edwin is that the KYC layer has been reduced in its friction and there is a layer now to get in without verification. Um uh one question I follow that I don't I didn't hear Hassan is when will that be pushed out to the app store? What time?

**George Westbrook:** Um,

**Hasan Ahmed:** Um,

**George Westbrook:** is

**Hasan Ahmed:** is the order on there now?

**Troy McDonald Kane:** Okay.

**George Westbrook:** order.

**Troy McDonald Kane:** Um and I think that that's something Cody we should and Kevin we should um highlight in the in the email as well is that there is a path to not being verified to be able to trade and test it out. now. Um, but if we're not uh funding a cash pool for the first week of college games,

### **00:24:59**

**edwin:** No,

**Troy McDonald Kane:** uh Oh,

**edwin:** we are.

**Troy McDonald Kane:** we are.

**edwin:** Yeah, we're it's just going to be based on how many people.

**Troy McDonald Kane:** Okay.

**edwin:** I mean, uh, you know, we've got to figure out to, you know, today or tomorrow what we're going to be willing to pay, you know, with 200 users or 50 whatever we've got,

**George Westbrook:** You don't have

**edwin:** right?

**Troy McDonald Kane:** Yeah. Where are we at now, Cody?

**George Westbrook:** to

**Troy McDonald Kane:** And verified

**Cody Haugen:** and verify it. 187

**edwin:** Yeah. So maybe we get to 200, but like per 200 people, I've run pools at the merc bigger than 200 people. You know what I mean?

**Troy McDonald Kane:** Yeah. When are we going to publish the prize pool for Saturday?

**edwin:** Probably Friday.

**Troy McDonald Kane:** Okay.

**Cody Haugen:** So then yeah, it's probably backtoback newsletters then Kevin send one out tomorrow and send one out

**Kevin Murray:** Yeah.

**Cody Haugen:** Friday.

**Troy McDonald Kane:** Yeah. And it can also be a push alert,

**Kevin Murray:** Yeah.

### **00:25:54**

**Troy McDonald Kane:** right? Can we create a push alert through the app that points people to the prize pool so they know what what they're playing for?

**George Westbrook:** I don't I don't think we've got a page on the app for the actual prize pool yet. So, that might be something we need to add in.

**edwin:** It could be posted on the website or

**George Westbrook:** Um, okay.

**Troy McDonald Kane:** Yeah. even if it's just a link to the prize pool on the website,

**George Westbrook:** Yeah.

**edwin:** something.

**Troy McDonald Kane:** something like that, just to get them there. But so they know and then they more uh induced to trade and participate. I think even if it's a small price pool, Edwin, like even if we're talking about hundreds of dollars versus thousands of dollars, I think that that's still enough for the first test or first week of trading. Your thoughts

**edwin:** Yeah. Yeah. Yeah, I mean I right now I'm going with that same rule of thumb we had before,

**Troy McDonald Kane:** are

### **00:26:37**

**George Westbrook:** Yeah.

**edwin:** which was roughly for every competitor um that's involved would be like three bucks.

**Cody Haugen:** Yep.

**Troy McDonald Kane:** makes sense. Okay.

**George Westbrook:** Put it in.

**Troy McDonald Kane:** Um, Anything else that we need to uh to go over today? Um I know we have the Novo call set for tomorrow morning. I'm sorry, the the TZ Novo call set for tomorrow morning. Um I don't know if Brett if it makes and George if it makes sense for us also to just do another 30 minute call tomorrow um either before or after that. Well, it have to be just to like make sure we're all good for going into secondary. So Edwin, as of now, we're still planning to transition to secondary trading tomorrow morning at 9:30 Eastern, 8:30

**edwin:** Okay. Okay. That's exciting. I mean, you know, if as long as we have that second layer open,

**Troy McDonald Kane:** control.

**edwin:** then I consider it a win. Right now we're half halfway there because, you know, I I know we have whatever on that admin panel you gave me, George, we show like 300 something, you know, down I don't know if it's downloads or like emails or whatever we've captured.

### **00:28:00**

**edwin:** It's it's it's greater than the actual KYC number. Um, and you know, on on the intern front, when do we think the interns are going to start trying to push people into this? cuz I don't think we've gotten much of a splash in terms of people signing up since we've had Cam join or any of the

**Troy McDonald Kane:** They've started this week this week as some of them have already returned to campuses and are already starting to push

**edwin:** others.

**Troy McDonald Kane:** it and do you know uh involvement fairs and whatever first week kind of activities there are. So, uh, we have, uh, interns already pushing, um, signups.

**edwin:** Okay. because I don't think you need to be on campus to push. Right.

**Troy McDonald Kane:** Well, no,

**edwin:** Like if you know,

**Troy McDonald Kane:** they're all pushing through their friends and networks right now, but the ones that are on campus are already going out there and having conversations and and attending events,

**edwin:** right?

**Troy McDonald Kane:** promoting and play. We gave them scripts. We've armed them with,

### **00:28:54**

**edwin:** Okay.

**Troy McDonald Kane:** you know, uh, content to to talk about. Uh obviously the app being removing that KYC layer will really help them as well. Uh kind of show uh real quick how they can get on the

**edwin:** Right. Right. Okay. Okay.

**Troy McDonald Kane:** app.

**edwin:** Excellent. Good

**Cody Haugen:** Yeah, it's about a 100 more downloads um than KYC.

**edwin:** stuff.

**Cody Haugen:** 278 downloads. So 90 more

**edwin:** Okay. Well, that first batch of downloads primarily all of us in our networks, you know, out of that 150, you know, we we don't have much outside. Did Did you by any chance talk about these warmed up emails we were sending to marketers? Did we ever did we ever Go ahead.

**Cody Haugen:** That was Yeah, that was going to be my last point as well, Edwin.

**edwin:** You take it then.

**Cody Haugen:** Well, I was just gonna say Brett and I went back and forth just on one message,

**Brett StClair:** No.

**Cody Haugen:** but um Brett Uh when do we think that'll start now that you had to do the reconfig

### **00:30:03**

**Brett StClair:** Yeah, we just hit a bunch of bucks for some reason. It just hit a bunch of issues. So, George is working on it with Venez trying to iron it out as quickly as we can. Soon as we got that done, we'll be able to kick it off.

**edwin:** Okay. But it hasn't started,

**Brett StClair:** Hasn't started.

**edwin:** right?

**Brett StClair:** No, no. We hit a bunch of bugs.

**edwin:** Okay. Um, by chance, have you been able to reach out to Wayne to see if that other guy from New York that we talked to any any feedback?

**Brett StClair:** I've every second week I send him an email just nudging and seeing if I'm getting any traction.

**edwin:** Okay. Okay.

**Brett StClair:** Sorry, I'll stay on top of

**edwin:** Okay. Sounds good.

**Brett StClair:** that.

**edwin:** Okay. I don't have anything else other than apology for being

**Jared Sapirman:** Um,

**edwin:** late.

**Jared Sapirman:** I have one thing about the I know we had the viral app call yesterday, but um, something Edwin had brought up a couple times is the change of the app logo.

### **00:31:05**

**Jared Sapirman:** and the app name. Um, did we want to make a move on that or still wait more longer on this viral

**Cody Haugen:** No, wait. I'm actually one minute over to talk with Assam about the contract. So, um, let me jump to that. But yeah, I would hold off on anything until we get this sorted with viral

**edwin:** Yeah,

**Cody Haugen:** app.

**edwin:** I think we talked I well George or somebody came back to me and said that might that might be a bigger lift than we thought um internally. Is that fair? Is that fair,

**George Westbrook:** Yeah.

**edwin:** George?

**George Westbrook:** Yeah. Yeah,

**Brett StClair:** Yep.

**George Westbrook:** it's I I can't remember.

**edwin:** Okay.

**Troy McDonald Kane:** Great.

**George Westbrook:** I think you know better than me, Hassan.

**Hasan Ahmed:** need a

**George Westbrook:** It's either a completely new app review or a completely new submission.

**Hasan Ahmed:** complete

**edwin:** Wow. Wow. It changed the name, not the actual

**Hasan Ahmed:** um I believe if you want to update the actual the name you need to do a new um like app store

### **00:31:53**

**edwin:** logo.

**Hasan Ahmed:** check and so that might take I mean at least like a week or so I mean

**edwin:** Yeah.

**Hasan Ahmed:** I'll yeah see I can give it a look and

**George Westbrook:** Yeah, see Uh give

**Troy McDonald Kane:** Yeah, I I think the the the this the app icon can change without an app review because I know apps push that out pretty frequently. Um, but maybe the name needs more review because it is confusing if you search one name versus another name. But is there any way we can look at at least first getting the uh the icon change to be simpler?

**Hasan Ahmed:** Yeah.

**edwin:** Cool.

**Troy McDonald Kane:** Yeah.

**edwin:** All right. Who's Lily? It's a new person. Hi, Lily.

**Troy McDonald Kane:** Yes.

**Lily StClair:** Um,

**edwin:** What do you do?

**Lily StClair:** hi. I just graduated from Exit University. I'm not sure if you know that, but I've studied neuroscience and I'm just Yeah, I've started working in Nova Sapion.

**edwin:** Oh, congratulations. Good luck to you.

**Lily StClair:** Thank you so much.

### **00:32:55**

**Lily StClair:** Nice to meet you.

**George Westbrook:** H.

**edwin:** Awesome. Yeah. All right. Oh,

**George Westbrook:** She's a sin.

**edwin:** that's good.

**George Westbrook:** Sinclair as well.

**edwin:** She's a what player?

**George Westbrook:** A Sinclair.

**edwin:** Oh, is Oh, she's a Sinclair. Is that your daughter, Brett? Oh, gosh. Finally,

**George Westbrook:** Yeah.

**edwin:** we get to see the class of the the the the cream of the crop here.

**Brett StClair:** Just Thank

**edwin:** Oh, congratulations. Your dad's quite a quite quite a guy.

**Brett StClair:** you.

**edwin:** He's he's a very dynamic individual.

**Kevin Murray:** have to be very careful now what's being said on these

**edwin:** Yeah, things just changed. I mean, I think I think Brett's aces.

**Kevin Murray:** calls.

**edwin:** I mean, he's just great. No, your dad's a very nice fan and he's been working hard to help us,

**George Westbrook:** Yeah.

**edwin:** so we're greatly appreciative. Um, all right. Well, cool. I won't keep everyone have a good day and um yeah, if anything pops, please let me know. We'll do the same on our end.

**George Westbrook:** Perfect.

**Kevin Murray:** All right.

**George Westbrook:** Let's f\*\*\*\*\*\*

**Kevin Murray:** See you later,

**edwin:** Hey,

**George Westbrook:** go.

**Kevin Murray:** everyone.

**edwin:** thank you. Hey Cody, can I call you real quick on that uh viral app thing? Gone.

**Troy McDonald Kane:** I think he dropped already for that call.

**edwin:** Okay.

**Jared Sapirman:** Now you dropped.

**edwin:** Okay,

**Troy McDonald Kane:** Yeah.

**edwin:** cool. Thank you. Talk to you guys in a bit.

**Troy McDonald Kane:** All right. All right. This

**edwin:** I know.

### **Transcription ended after 00:34:14**

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*