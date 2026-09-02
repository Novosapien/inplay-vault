---
date: 2026-09-01
type: standup
description: "Monday touchdown, 1 September 2026: an app-wide lockout with no known cause, the AI tooling suspended, three revenue routes, and the never-empty-book rule."
source: "Google Meet transcript, Inplay - App - Touchdown (30m 06s)"
scope:
  - "[[architecture/services/auth-service]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[inplay-global-website/inplay-global-website]]"
  - "[[advertising/advertising]]"
  - "[[information-layer/sub-components/research-tab/research-tab]]"
  - "[[market-maker/market-maker]]"
  - "[[referral/referral]]"
  - "[[delivery/delivery]]"
status: extracted
extracted-to:
  - "[[architecture/services/auth-service]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[inplay-global-website/inplay-global-website]]"
  - "[[advertising/advertising]]"
  - "[[information-layer/sub-components/research-tab/research-tab]]"
  - "[[market-maker/decisions]]"
  - "[[market-maker/open-questions]]"
  - "[[market-maker/parameters]]"
  - "[[market-maker/plan]]"
  - "[[market-maker/sessions/2026-09-01-touchdown-digest]]"
  - "[[referral/referral]]"
  - "[[architecture/frontend/app-store-accounts]]"
  - "[[delivery/delivery]]"
  - "[[delivery/requirement-changes]]"
---

## Post-Call Analysis

Thirty minutes, on transfer deadline day, two days before the first week of
college football. Present: Cody, Troy, Jared, Kevin, Max (InPlay) and Brett,
George, Hasan, Lily (Novosapien). Edwin was absent. The call was cut short
deliberately: Troy cancelled the tZERO call that followed it so the engineers
could go and work on the outage.

**Two things dominate this call and they compound each other.** The app is
locked out for everybody, nobody knows why, and the tooling that would normally
find the cause has been switched off over an unpaid bill.

### 1. The app is locked out, and nothing points at a cause yet

Jared, mid-call: *"I got kicked out of the app. Is that supposed to happen?"*
It was not. Cody had already seen it from outside the team: *"I had a few
buddies text me this morning saying they were locked out. They can't retrieve a
password or a code. It's not sent to their email."* He and Jared both
reproduced it. So the failure is not just sessions dropping, it is the recovery
path failing too: no password reset, no code, nothing arriving by email.

**No cause was identified on the call, and nobody pretended otherwise.** Brett
listed the candidates and stopped there: *"It could be a link to persona. It
could be authentication. It could be anything."* George said the same. The
honest position at the end of the call is that this is unlocated, the team is
reading code by hand to find it, and there is no estimate.

The scale matters more than usual because of the date. Cody: *"we have two
really two days till more trading happens, live games happen. Thursday is when
week one kicks off and they're both ranked games."* And Troy noted the app is
picking up unprompted traffic even off game days: *"we never know who might try
to log on to it... we are getting active enga more active engagement even
though it's not a game day."*

### 2. The Claude account is suspended over an unpaid bill, and that is why the fix is slow

This is the thing that turns a bad morning into a slow week. Brett, plainly:
*"we're just on manual mode at the moment because our clause billing accounts
have been suspended... it's going to take us a little bit longer."*

The number: *"I need to pay the Claude bill which is on our side. It's our
cost, but it is sitting at about $49,000, which I don't have a spare $49,000
just to find to pay."* He is waiting on Edwin over payment.

**What it costs, in George's words:** *"usually it's say 10 10 people that
would be doing it. Obviously, it's two two to four of us with with AI. So
there's going to be a bit more time on that now without the AI."* And,
unprompted: *"Feels like going back to stone tools."*

Two things are worth separating. The lockout is **not** caused by the
suspension. But every step of diagnosing it, and every fix after it, now runs
at hand-coded speed on a team sized for AI-assisted speed, and the first live
college week starts in two days.

### 3. The website's www address stopped working, and HubSpot looks responsible

Typing `inplayglobal.com` works. Typing `www.inplayglobal.com` does not. A
saved bookmark works; typing it fresh does not. Jared confirmed it used to
work: *"I've been able to type in probably month ago www.inplay global and that
did not come up."* Troy dated the break: *"something's broke been broken over
the last week or so."*

George's diagnosis, and he was careful to mark it as a diagnosis: *"it looks
like the HubSpot something to do with HubSpot has changed the DNS for www...
I think the www c name's been changed."* Neither side has touched DNS. Cody and
Kevin confirmed only the social accounts were connected through HubSpot, never
the website, and that the Viral App Launch agency has the advertising logins
but **not** GoDaddy.

**Cody authorised the fix on the call:** Brett asked *"You guys are fine if we
break that and bring it back to normal"*, and Cody answered *"Yes, please."*

### 4. Three routes to revenue, and two of them are ready now

Cody put the commercial pressure on the table without dressing it up:
*"everyone from the team is stressed like right now we have three three options
towards towards revenue."* Inside the app, they are:

1. **Programmatic ads** on the pages.
2. **Video ads** over the field player and the gamecast tracker.
3. **Subscriptions and packages.**

Brett's read on readiness, which is the useful half:

- **Programmatic can be switched on now.** *"we can be quick if you guys are
  happy we just turn the ads on. We can turn them on because it's all
  configured programmatics running. It's not optimized, but it's running. So,
  at least you can start getting some revenues there."*
- **The video ad is built and verified**, and needs a short test pass: *"we've
  got it built out. It's been verified. We need to get that in and just do run
  a couple of tests first."*
- **Subscriptions need a requirement session.** Not a build task yet.

The reason the ads matter this week and not next quarter: paid advertising is
starting outside the Viral App Launch relationship, the first real college
games land on Thursday, and the NFL offering and season follow. Cody:
*"all of these things are going to start to cascade... we need to be able to
monetize the users coming in."*

### 5. What a subscription build actually contains

George laid the scope out before anyone committed to a date, and it is larger
than a paywall:

- **What is gated**, free versus paid, which he thinks is roughly understood
  already but not written down.
- **Payment through Apple**, taking the 30% cut. This was already the standing
  assumption.
- ⚠ **Another App Store review.** *"as soon as you change big things like
  payments that's when we're going to need the app store review."* That is a
  submission and a wait, on top of the build.
- **The app changes that go with it**: gating for free users, access for paid
  ones, and *"how we can motivate people throughout the app to make those
  subscriptions and it not just be something that's hidden away."*
- Brett added the commercial plumbing: *"There's billing, there's onboarding,
  there's upselling, cross-selling."*

**Cody's timing, offered without being pushed:** *"I didn't expect them or us
to get to them in September, but I would like them as soon as possible. So, if
that means, you know, beginning of October, then great."* He also asked for the
research function and tools *"in there as soon as possible"*.

### 6. Brett named how the flight plan priorities were set, and asked to redo them

This is a candid one and worth recording as said. On Cody's list of asks:
*"I think I've got most of that tracked in the flight plan"*, then, on how the
priorities got there: *"because I just went, 'Hey, AI, what do you think?'
based on the conversations that we've had. So, let's give it the right
priorities."*

He asked for two sessions:

1. A **priority session** to load Cody's list into the flight plan properly.
2. A **requirement session**, about an hour and a half, walking every user
   journey and mapping the components before any build. His reasoning:
   *"it gives it a way better chance if we do an hour and a half session work
   through in detail every single user journey kind of map it all out and then
   we load it up then it works really really well."*

Tomorrow's call (2 September) becomes the subscription design session.

### 7. Troy's rule: a book must never be empty, even for an instant

This is the most consequential engineering item on the call, and it came as a
principle rather than a bug report. Troy: *"there should never be a moment
where there's not a bid an offer. Now the bid and offers can widen and tighten.
But what I saw was that whenever you were re-calibrating, you would wipe out all
three levels and then you had like a split second of no bid or offer."*

His ask is **consistent three levels**, and a recalibration that widens and then
tightens rather than clearing: *"if you're recalibrating, it should be widen
out, tighten in kind of criteria."* His reason is structural, and he is right
about it: *"there's no other market makers there that can support that
liquidity. We are the... So, we almost have to operate as like two or three
market makers at once because there's no one else leaning on us or we're not
leaning on anyone else."*

**George confirmed the gap is by design, not a defect**, and named the venue
constraint: *"with T0 you can't do a replace in place. It has to be a cancel and
then a replace. So we need to work out how are we going to do it where it's
either topping up or it's clearance."* He offered two directions: a better
design, or make it fast enough that the gap does not matter.

### 8. Phantom liquidity, and why market orders do not fill

Both Troy and Jared hit the same thing independently. Jared: *"there was not
actually a single time where I had an order of more than I would say 50,000
that fully filled."*

Troy's account is the precise one, and it names the mechanism: *"what's
happening is if others are hitting the same market at the same time also the
market maker is resetting the bid offer. What I noticed as I was doing that is
that it would get a partial fill and then the book would reset. So in that
reset in that cancel replace the liquidity is actually more **phantom
liquidity** because it's not there and it's in the process of being cancel
replaced and so the order can't go through the book because the book is being
reset."*

He also named the frequency as a suspect, while explicitly leaving the call to
Edwin: *"I still think the market maker's updating too frequently. But that's
Edwin's discretion. He wants it set a certain way because I missed the market so
many times because every time I was going to hit the market or lift the market
the market maker algo was resetting."*

Troy did not propose a fix and said so: *"I don't know if we need to go larger
quantities, we need to go to depth of five. I don't know yet."*

### 9. The size squash, stated from the other side of the screen

George gave the history in one breath, and it is the clearest client-facing
statement of what the 20 August cut did:

> *"before... it was minimum three levels, maximum six levels with everything
> in tranches of 500 with a bit of randomization in with the maximum amount of
> quantity being 10 to 15,000. Then I think everyone wanted it squashed right
> down. So I think the max quantity per side is between 500 to I need to double
> check that."*

And the consequence, said plainly: *"getting a thousand filled on a market
order is pretty much not going to happen unless it's coming from other people
apart from the market maker."*

Jared pushed on whether an order should walk the book through the deeper
levels, which is the right question. Troy's answer is that it would, if the
levels stayed still, and they do not.

### 10. The maker prices off probability alone, and George says that is the gap

This is George diagnosing his own machine, and it is the most useful sentence
of the call for the next build phase:

> *"the maker needs more variables in order to determine levels and quantity
> because it needs to take into account maybe trading volumes during the game.
> And then expanding out maybe the quantity based on the number of participants
> in the market. Whereas at the moment it is this is the bounds for quantity.
> These are the levels. The quantity is random within certain bounds. The levels
> are almost completely random."*

And the design position that follows from it: *"it's not taking into account
participation in the market when building the actual market... it's purely
based on certain aspects that are coming from sports radar which are more
deterministic, like this is the win probability. But there could be a thousand
users or 10,000 users, the market maker's still going to be functioning in more
or less the same way, by design."*

He agreed it needs improving and put the decision where it belongs: *"I suppose
it's just up to Edwin as to what he sees fit."*

**The scale case that makes it urgent** came from Jared, and it is a real game:
Hawaii against Stanford at the weekend, where Stanford led by a lot, Hawaii
came back, and Stanford won it in the last minute. His point: that is the game
everybody would have been trading, the price moved hard, and the experience
would have degraded exactly when it mattered most, while the quiet games ran
fine.

### 11. UNCC had no bid, and George traced it to a rule rather than a fault

Cody, on the weekend: *"we were heavy UNCC. So there was no bid on UNCC for a
while, but when it was working, I was going on both sides relatively
seamlessly."* Edwin hit the same book.

George's read, offered as unfinished: *"there was a criteria in one of the
constitutional documents which was basically like if this happens then do that.
Which I think we need to loosen a bit. But rather than me giving a half-arsed
answer as to what we should do, properly going to investigate it."* He noted the
one saving grace: *"it kind of fortunately only does it for one market and not
the whole market."*

⚠ This is the same shape as the North Carolina book on 29 August: a guard that
refuses correctly against a real touch and holds one book while it does. It
belongs with N75 and N76, not on its own.

### 12. Two smaller items with owners

- **TestFlight access for the agency.** Jared: Dimmitri from Viral App Launch
  still has nothing. Kevin and Hasan are working it, and it is blocked behind
  the app working at all.
- **Admin panel for share codes and groups.** Hasan will extend the trading
  admin panel so Cody can create and edit groups and edit share codes himself.
  Cody has no access to that panel today, only Edwin does. His reason is a good
  one: *"I would like to ping you less and be able to sort on our time zone."*

### 13. Slack items only reach the vault when Brett remembers

Troy raised it as an assumption the client has been making: *"I know we keep
sending you stuff one off in the Slack, so we assume that's being picked up by
AI."*

Brett corrected it honestly: *"I do that once a week. I take everything that's
in the chat and actually manually put it into the vault. So if we do find stuff
that we logged in the chat and it hasn't been picked up, it might be because of
that... it's just a manual, me remembering to do it at the moment."*

That is a process gap with a client expectation attached to it, and it is worth
fixing before the requirement sessions rather than after.

### 14. The tZERO call was cancelled, and for the right reason

Troy cancelled the same-day tZERO call so the team could work the outage, after
checking there was nothing outstanding. George confirmed there was not: *"there's
no issues we've had with their side and usually if there's something urgent,
Rob's on it straight away."* Rob was away last week and this week for an
evangelist event.

---

## Findings

| Finding | Destination | Action |
|---------|-------------|--------|
| ⚠ **App-wide lockout: login fails, password and code emails do not arrive** | [[architecture/services/auth-service]], [[customer-onboarding/customer-onboarding]] | Live incident recorded, cause unknown |
| ⚠ **Claude account suspended over a $49,000 unpaid bill; engineering on manual mode** | [[delivery/delivery]] | Delivery risk recorded |
| ⚠ `www.inplayglobal.com` broken, bare domain fine; HubSpot changed the www record | [[inplay-global-website/inplay-global-website]] | Defect recorded, fix authorised by Cody |
| Three in-app revenue routes named: page ads, video ads, subscriptions | [[advertising/advertising]] | Recorded |
| **Programmatic ads configured and running**, switchable on InPlay's say-so | [[advertising/advertising]] | Recorded, decision owed by InPlay |
| **Video ad over the field player built and verified**, needs a test pass | [[advertising/advertising]] | Recorded |
| Subscription scope: gating, Apple 30%, **another App Store review**, upsell placement | [[information-layer/sub-components/research-tab/research-tab]] | Scope recorded, session booked for 2 Sep |
| Subscription timing: not expected in September, early October acceptable | [[information-layer/sub-components/research-tab/research-tab]] | Recorded |
| Flight plan priorities were AI-drafted; priority session and 90-minute requirement session asked for | [[delivery/delivery]] | Recorded |
| ⭐ **A book must never be empty, even for an instant; recalibrate by widening then tightening** | [[market-maker/decisions]], [[market-maker/open-questions]] | New N77 |
| Cancel-replace produces **phantom liquidity**; market orders partially fill then the book resets | [[market-maker/open-questions]] | Recorded in N77 |
| Maker update frequency questioned by Troy, left explicitly to Edwin | [[market-maker/open-questions]] | Recorded in N77 |
| Sizes squashed from 10,000 to 15,000 down to about 550; a 1,000-share order cannot fill from the maker | [[market-maker/parameters]], [[delivery/requirement-changes]] | Consequence recorded, A11 |
| ⭐ **The maker needs participation inputs: in-game trading volume and number of participants** | [[market-maker/open-questions]], [[market-maker/plan]] | New N78 |
| UNCC had no bid; George traces it to a rule that needs loosening | [[market-maker/open-questions]] | Recorded against N75 and N76 |
| Scale case: Hawaii against Stanford, the game everyone would have traded | [[market-maker/open-questions]] | Recorded in N78 |
| Admin panel to be extended so Cody can create groups and edit share codes | [[referral/referral]] | Requirement recorded |
| Viral App Launch tester still has no TestFlight access | [[architecture/frontend/app-store-accounts]] | Blocked behind the outage |
| Slack items reach the vault only via a manual weekly sweep | [[delivery/delivery]] | Process gap recorded |
| tZERO call cancelled to free the team; nothing outstanding on their side | [[delivery/delivery]] | Recorded |

---

Sep 1, 2026

## **Inplay \- App \- Touchdown \- Transcript**

### **00:00:22**

**Kevin Murray:** newsroom where it's a hive of activity on

**Brett StClair:** Is there a hype of activity around the

**Kevin Murray:** a transfer deadline day.

**Brett StClair:** football?

**Kevin Murray:** f\*\*\*\*\*\* glued to the glued to the Sky Sports. I am so do

**George Westbrook:** I hate Everton at the moment.

**Cody Haugen:** Okay.

**George Westbrook:** Bloody selling selling that guy to City

**Kevin Murray:** I the the shot.

**George Westbrook:** instead.

**Brett StClair:** Come on you spurs.

**Kevin Murray:** I don't know.

**George Westbrook:** Is it Is it come on you?

**Brett StClair:** Is it come on you yet?

**Kevin Murray:** I know.

**Brett StClair:** Say

**George Westbrook:** Yeah.

**Kevin Murray:** What's going on with Richie? How come he he's not allowed to

**George Westbrook:** I know.

**Kevin Murray:** leave?

**George Westbrook:** I' I'd have thought we'd have we'd have got rid of him.

**Kevin Murray:** I think the only know something like 2 million pounds or something before they can sell because he won't leave cuz he hasn't asked to leave so he's entitled to 2 million as if he hasn't got enough

**George Westbrook:** Oh yeah.

**Kevin Murray:** money. Do you know what I mean?

### **00:01:12**

**George Westbrook:** Don't I think it's Well, because we we were looking for obviously gakpo,

**Brett StClair:** Why would he

**George Westbrook:** but why would he want to leave Liverpool if they don't want to sell him?

**Brett StClair:** want

**George Westbrook:** And why and obviously City wanted him. Um and then your guy and Oh,

**Brett StClair:** and then your guy?

**George Westbrook:** perhaps in your way.

**Brett StClair:** Sorry.

**George Westbrook:** Sorry.

**Brett StClair:** Sing.

**George Westbrook:** And then it's in in day or whatever his name is. I I'd not really seen him play to be honest,

**Troy McDonald Kane:** I

**George Westbrook:** but everybody's ranting and raving about him. And then obviously City comes in and like Yeah, we'll have

**Kevin Murray:** Yeah, I think it was something maybe to they did a deal there.

**George Westbrook:** him.

**Kevin Murray:** it was an extra 5 million. So, they've paid 65 million for him. And then maybe they'll probably cover more of Greish's uh wages or something because we were meant to be paying 90% of it.

**George Westbrook:** Yeah.

**Kevin Murray:** So, we'll wait and see.

### **00:01:56**

**Kevin Murray:** But yeah.

**George Westbrook:** Don't I can imagine there's going to be a fair bit that is going to

**Brett StClair:** I can imagine.

**Kevin Murray:** Oh, yeah. It's going to be insane the next couple of hours for sure.

**George Westbrook:** happen.

**Kevin Murray:** But I won't digress too much on the good old football.

**George Westbrook:** Proper football.

**Brett StClair:** probably um we're having a look at the login

**George Westbrook:** Um, we're having a look at the result in

**Brett StClair:** problems. Is that better? Can you guys hear me?

**Kevin Murray:** Yep.

**Brett StClair:** Yeah.

**Kevin Murray:** Well, I'm

**Brett StClair:** Okay. It sounds like it's being muted.

**Kevin Murray:** glad

**Brett StClair:** Um we're just on manual mode at the moment because our clause billing accounts have been suspended. Um so it's going to take us a little bit longer um to have a look at it. But uh I think we picked up another issue on your website as well. So I don't know if these are correlated or issues. If you go to ww um Inplay global eh yeah are you seeing the same

### **00:02:51**

**Cody Haugen:** Yeah, I just checked this. Um,

**Brett StClair:** problem on yeah there there's some we don't know what's causing

**Kevin Murray:** Yeah.

**Brett StClair:** That's We are just when I say manual mode,

**Cody Haugen:** I am not Yeah,

**Brett StClair:** we're going through stuff manually.

**Cody Haugen:** Brett, I am not on our homepage. I see our normal homepage

**Brett StClair:** So go ww and then type it

**Cody Haugen:** here. Uh,

**Brett StClair:** out.

**Cody Haugen:** okay. Sorry. They're

**Troy McDonald Kane:** I think the problem is the problem is Brett some browsers correct for it and some

**Cody Haugen:** saying

**Troy McDonald Kane:** browsers don't. So if you do www.inplay global half the time I do that it takes it away and sends me to the right page and half the time it

**Brett StClair:** takes it away.

**Troy McDonald Kane:** doesn't.

**George Westbrook:** it when I think when we had it set up before it would always take you to the right page. I think I'm not sure what's happening now.

**Troy McDonald Kane:** Something broke recently.

**Brett StClair:** Do you reckon it's a maybe it's not correlated?

### **00:03:44**

**George Westbrook:** It's not I think it was a it looks like the

**Brett StClair:** Um,

**Troy McDonald Kane:** Yeah.

**Brett StClair:** I think I

**George Westbrook:** HubSpot something to do with HubSpot has changed the DNS for www do because

**Brett StClair:** mean

**George Westbrook:** usually what you do is you'll have the you'll set up a redirect. So either the www do redirect to the normal one so that if you typed it in without

**Brett StClair:** to the north. So that type it's going to bring

**George Westbrook:** it's going to redirect to the www do or vice versa.

**Cody Haugen:** So yeah, I mean as far as HubSpot's concerned, unless you guys have started on any integrations, it's not connected to our web page though. Like there's no formal connection that that Kevin and I have done from any of our I mean I guess our socials were connected but nothing to the actual homepage.

**George Westbrook:** Could it be something to do with the viral viral app launch, guys? I don't know if they've had access to what was it, GoDaddy.

**Cody Haugen:** Uh they do not have access to GoDaddy.

### **00:04:43**

**Cody Haugen:** They do have access to the advertising um the advertising login um meta Google and and all of those

**Brett StClair:** No, I don't think that'll cause it.

**Cody Haugen:** things. Um but

**Brett StClair:** Unless we just stumbled onto something that was already there.

**Kevin Murray:** If I click on the link for Inplay Global that I've got saved on my desktop,

**Cody Haugen:** yeah,

**Kevin Murray:** it takes me straight to the website and it's perfect exactly how it was. But if I type it in, then it brings up the same issue you guys have

**Jared Sapirman:** Yeah, that was not always a problem because I've been able to type in probably month ago uh

**Kevin Murray:** got.

**Jared Sapirman:** www.inplay global and that did not come up.

**Troy McDonald Kane:** Yeah,

**Brett StClair:** and it doesn't.

**Troy McDonald Kane:** that's what I was saying. It would correct. It would correct for it.

**Brett StClair:** Okay.

**Troy McDonald Kane:** So, something's broke been broken over the last week or so.

**Brett StClair:** Yeah.

**George Westbrook:** Yeah.

**Brett StClair:** Yeah.

**George Westbrook:** And I know we've not touched the DNS.

### **00:05:29**

**Brett StClair:** I know. DNS. Um,

**George Westbrook:** Um,

**Brett StClair:** well, let's go into the DNS manually and see what we can do to fix it. See um Hasan,

**Kevin Murray:** Even if you just type in inplay global.com,

**Brett StClair:** do you want to have a look on the call?

**Kevin Murray:** it brings you straight to the actual web page properly. So it's only when you www.in

**Cody Haugen:** Yes.

**Brett StClair:** Galaxy.

**Kevin Murray:** start

**Cody Haugen:** Yeah. The HTTP prelude does work.

**Brett StClair:** Um.

**Cody Haugen:** It's the WW for whatever reason.

**Brett StClair:** Um. Yeah. So, we're just on a bit of a slow mode. Just we're going to be checking stuff manually, so bear with us. Um, Cody, I've seen your list. I think I've got most of that tracked in the flight plan. I think what we need to do is do a session to do two things.

**Cody Haugen:** Yeah.

**Brett StClair:** A loaded into the flight plan correctly. Um, because I just went,"Hey, AI, what do you think?" based on the conversations that we've had.

### **00:06:28**

**Brett StClair:** So, let's give it the right priorities.

**Cody Haugen:** All right.

**Brett StClair:** And then a couple of them, let's do an actual requirement session where we lay out the components, get it mapped out correctly so that we give AI better fighting chance than what we've been trying to do to date because we're just trying to go as fast as we could. And so I think it gives it a way better chance if we do an hour and a half session work through in detail every single user journey kind of map it all out and then we load it up then it works really really well. You know things like the um analyst um what else? Let me just bring up your list.

**Jared Sapirman:** I got kicked out of the app. Is that supposed to happen?

**Brett StClair:** Yeah, that's what we looking we're looking at at the moment. Not sure what that reason is. Um, but we I've got to talk to Edwin because I need to pay the Claude bill which is on our side. It's our cost, but it is sitting at about $49,000, which I don't have a spare $49,000 just to find to pay.

### **00:07:34**

**Brett StClair:** So, I just need to chat to him, see how he's going on the payment. Um, and then I can get that paid off. But it doesn't stop us from working because we just snap into normal software engineering mode. Do you see how excited George and Hasan Vineth and everybody

**George Westbrook:** Feels like going back to f\*\*\*\*\*\*

**Brett StClair:** is?

**George Westbrook:** stone tools.

**Troy McDonald Kane:** So, are we locked out of the app because you guys are locked out of

**Brett StClair:** No, I don't think so.

**Troy McDonald Kane:** Claude?

**Brett StClair:** Trying to figure the problem out is going to be a manual thing though. So, we're just sifting through the code to figure it out. Now all our agents are sitting in Claude locked out.

**Troy McDonald Kane:** Okay.

**Brett StClair:** So we can't we can't code with Claude is our

**Cody Haugen:** Yeah, because it is a it is a wider issue.

**Brett StClair:** problem.

**George Westbrook:** Sure.

**Cody Haugen:** I had a few buddies text me this morning saying they were locked out. They can't retrieve a password or a code.

### **00:08:25**

**Cody Haugen:** It's not sent to their email.

**Jared Sapirman:** Yeah,

**Cody Haugen:** And then same,

**Jared Sapirman:** I just tried that I could get it.

**Cody Haugen:** yeah, I did too. So, yeah, it does seem to be everyone.

**Brett StClair:** Okay,

**George Westbrook:** Okay.

**Brett StClair:** we're going to look at it. There's so many different things.

**Cody Haugen:** Brett

**Brett StClair:** It could be it could be a link to persona.

**George Westbrook:** could be authentication could be

**Brett StClair:** It could be authentication. It could be anything.

**George Westbrook:** anything.

**Brett StClair:** So,

**George Westbrook:** So leave it with that and

**Brett StClair:** leave it with us and we will try unstitch this. Um,

**George Westbrook:** usually

**Brett StClair:** usually we let Claude do it and then we come up with a solution quickly and we fix it quickly. But we're just going to have to unpick this by hand quickly. 30\.

**George Westbrook:** Just check just check the reason the the website's doing that and it's it is something to do with HubSpot which I'm yeah we've we've not

**Cody Haugen:** Okay.

**Brett StClair:** Yeah.

### **00:09:13**

**George Westbrook:** done anything with HubSpot so I don't know I'm not sure what's happened

**Brett StClair:** So question

**Cody Haugen:** I don't either.

**Brett StClair:** is, how long haven't we put this up for?

**Cody Haugen:** Hasn't done anything and Kevin,

**Brett StClair:** Yeah.

**George Westbrook:** question.

**Cody Haugen:** did you when you were connecting something maybe connect something else or something? It was just socials,

**Kevin Murray:** No, it's just the socials, but I again I link those directly through Instagram,

**Cody Haugen:** right?

**Kevin Murray:** Facebook, Tik Tok X, so nothing went through the

**George Westbrook:** And yeah,

**Kevin Murray:** website.

**George Westbrook:** I can't imagine they'd in order for them to get access to but they wouldn't have access to the DNS any of the any of the socials.

**Kevin Murray:** No.

**George Westbrook:** So it it h I think it'd have to be something done in in HubSpot. But I'm I'm just trying to think how that how that could have happened. Um USS Data Center.

**Brett StClair:** I've got some ideas on what the domain kind of coding could be. The codes that you need. Is there a wam?

### **00:10:15**

**George Westbrook:** name. I think so.

**Brett StClair:** I think I think I think

**George Westbrook:** I think I think the w.c name's been changed. Connecting a website or subdomain to a HubSpot account. You guys are

**Brett StClair:** You guys are fine if we break that and bring it back to normal.

**Cody Haugen:** Yes,

**Brett StClair:** Yeah, let's do that.

**Cody Haugen:** please.

**Brett StClair:** Um, so Cody, can I set up some time in your guys diaries to do requirement sessions on the kind of two big ones? Let me just pull it up

**Cody Haugen:** Yeah,

**Brett StClair:** now.

**Cody Haugen:** I mean whatever whatever we need to do as soon as possible, Brett, because like I mean as as Edwin and I have well and everyone right um everyone from the team is stressed like right now we have three three options towards towards revenue now we're starting to pivot expand however you want to say it to other conversations as we continue to work on our own but through the app. It's really three options. It's the programmatic ads on the pages like we had.

### **00:11:22**

**Cody Haugen:** Um it's the video ads that live over this the the field player. Um the gamecast tracker um and it is um subscriptions and those packages. Those are really our three inapp strategies towards revenue. So whatever we need to do to move that

**Brett StClair:** So I think the the ads the ads would we can be quick if you guys are happy we just turn the ads on. We can turn them on um because it's all configured programmatics running. It's not optimized, but it's running. So, at least you can start getting some revenues there. Um, then the video ad, we've got it built out. It's been verified. We need to get that in and just do run a couple of tests first. Make sure that's working and then we can get that up and running pretty quickly. And then the subscription ones. Let's do a proper requirement session there. Hey, George.

**George Westbrook:** Yeah.

**Brett StClair:** Yeah.

**George Westbrook:** Yeah.

**Brett StClair:** Yeah.

**George Westbrook:** Because first I suppose it's

### **00:12:17**

**Brett StClair:** There's billing, there's onboarding, there's upselling,

**George Westbrook:** Yeah.

**Brett StClair:** cross-elling, all that s\*\*\*. Yeah.

**George Westbrook:** Yeah.

**Brett StClair:** Yeah.

**George Westbrook:** It seems like what's what's being gated?

**Brett StClair:** We type.

**George Westbrook:** Let me mute you back. Sorry. Sorry. Um what's what's being gated, which I I think we we've got a decent decent idea already, but I think just nailing that down. But then there then there's all the other stuff like sorting out how the payment's going to be processed which I think we spoke about before just through Apple take the 30% hit. Um but then there's obviously integrating that into it and then doing another app store review. Um because as soon as you change big things like payments that's when that's when we're going to need the app store review. And then there's obviously the app changes that go along with that. So making sure that they are gated off for free users and paid users have got access. Um and then how that changes the experience as well and how we can motivate people throughout the app to make those subscriptions and it not just be something that's that's hidden away.

### **00:13:18**

**Cody Haugen:** Yeah. Okay. No, that makes sense. Um, like I said, happy to do that. The the the programmatic why and and I'm happy to hear that it's moving forward and ready to go. The reason why it is is because or such a big deal is we are starting to do not through viral app launch but through others uh sort of paid advertising. So I mean through all of this as it should uh numbers should start to tick up relatively quickly. Now you add that on the cascade that NFL IPOs and NFL regular season are around the corner. This uh next weekend of college football is first real games. all of these things are going to start to cascade in what we all hope to be a successful sort of snowballing effect. Um, and so yeah, we we need to be able to monetize the users coming in. So the the the programmatic ads definitely, the video programmatic ads definitely, and then we'll figure out the subscriptions through a through a call um and start to spin those up.

### **00:14:21**

**Cody Haugen:** I mean, honestly, I didn't expect them or us to get to them in September, but I would like them as soon as possible. So, if that means, you know, beginning of October, then great. Um, but yeah, I mean, we want to make sure that there's that research function and those tools in there as soon as possible. Cool.

**George Westbrook:** Happy.

**Brett StClair:** Just having a quick pick to pee to see where we had next eight weeks. I think it was in there. So, yeah.

**Jared Sapirman:** We also need to meet on the test plate.

**Brett StClair:** Yeah. The goal was to get it in, by the way.

**Cody Haugen:** Yeah.

**Brett StClair:** Sorry. Sorry, Jar.

**Jared Sapirman:** Dimmitri has to go on the test flight. Obviously, the app's not working right now, but once the app's working, Dimmitri from the viral app launch has not gotten anything

**Cody Haugen:** Yeah, I was I was just paying Kevin and Hassan on

**Jared Sapirman:** right.

**Kevin Murray:** Yeah, I I was dealing with that yesterday,

**Jared Sapirman:** Okay,

**Kevin Murray:** Jared.

### **00:15:16**

**Cody Haugen:** that.

**Kevin Murray:** So,

**Jared Sapirman:** it's all good.

**Kevin Murray:** Han and Han and I are trying to sort it out for

**Jared Sapirman:** Okay.

**Kevin Murray:** Vlad. One quick question.

**Brett StClair:** Cody,

**George Westbrook:** Um,

**Kevin Murray:** I've emails from Fathom.

**Brett StClair:** it's the subscription. Sorry.

**Kevin Murray:** I get emails from Fathom from you guys wanting to join to access for like recordings. Is that a load of b\*\*\*\*\*\*\*

**Brett StClair:** No,

**Kevin Murray:** or what is it?

**Brett StClair:** no,

**George Westbrook:** no.

**Brett StClair:** we're running a test. Our apologies.

**George Westbrook:** Apologies.

**Kevin Murray:** No. No. I just wanted to know what it was.

**Brett StClair:** Um,

**George Westbrook:** Um she's trying

**Kevin Murray:** I didn't know whether it was spam or whatever

**Brett StClair:** did you see Lily putting her hand up?

**Kevin Murray:** cuz

**George Westbrook:** to go down

**Brett StClair:** She's trying to automate it so it goes from here straight in without any manual oversight.

**George Westbrook:** without and fill in

**Kevin Murray:** So, shall I just ignore those emails then as well?

**Brett StClair:** So you and fill in your credit card details to that one

### **00:15:58**

**Kevin Murray:** Yeah.

**Cody Haugen:** Yeah,

**George Westbrook:** your

**Cody Haugen:** exactly.

**Kevin Murray:** Sounds I'll send you a million bucks as well,

**Brett StClair:** link.

**Kevin Murray:** Brett, from from my Nigerian father.

**George Westbrook:** I had I had a prince the other day that was promising me wealth.

**Brett StClair:** part.

**George Westbrook:** Apparent I'm just in the process to get a million uh million pounds.

**Kevin Murray:** Oh yeah,

**George Westbrook:** So hopefully that lands.

**Kevin Murray:** it was it was left by the third uncle of the right toe or

**George Westbrook:** Yeah. Apparently I was apparently I was related to

**Max Kingaby:** George George,

**Kevin Murray:** something.

**Max Kingaby:** have you been um going to the same guy for joke classes that Brett goes to?

**George Westbrook:** him. Byebye.

**Cody Haugen:** Um, yeah. So, what uh moving in um so yes, thank you for covering my topics. What what else is there gentlemen that uh we want to touch on?

**George Westbrook:** So I suppose it's the main thing for us is investigating what's going on with the app, but that's going to take a a decent amount time more.

### **00:17:00**

**George Westbrook:** Um, obvious yeah, usually it's say 10 10 people that would be doing it. Obviously, it's two two two to four of us with with AI. So, it's going to there's going to be a bit more time on that um now without the AI, but once we've got answers on that, we'll we'll get that over, start working on the fixes, but once again, obviously, that's going to that's going to take more time as well. Um but we'll we'll keep you guys updated on that. Um I think I

**Cody Haugen:** Yeah, we have two really two days till more trading happens,

**George Westbrook:** think

**Cody Haugen:** live games happen. Thursday is when week one kicks off and they're both ranked games. Um, at least one team is ranked in the top 25 in both those games. So, um, yeah, I mean, obviously, right, everything is always as fast as possible, but that's re realistically what we're up against. Um, is, uh, Thursday has two games and then Friday and then into the weekend for week one.

**George Westbrook:** How how was the experience at the weekend.

### **00:18:03**

**Cody Haugen:** um the the trading when it was flowing correctly. Um I was I mean the the no bid I know we went back and forth. Edwin and I had the same problem. We were heavy UNCC. Um so there was there was no bid on UNCC for a while, but um when it was working, I was going on both sides relatively seamlessly. Um so I thought that was good for that game.

**George Westbrook:** I I think the I'm still well still investigating. The issue with that was there was a there was a criteria in one of the I think Edwin called them like the constitutional documents which was basically like if this if X happens then do Y. Um which I think we need to loosen a bit. Um but rather than me giving a halfass answer as to what we what I think we should do properly going to investigate it. Um because given that it kind of fortunately only does it for one market and not the whole market. um well it one market instead of all the markets.

### **00:19:03**

**George Westbrook:** So I think there might need to be some loosening loosening that we need to do there. But like I said a further investigation um and then yeah then get get something what potential solution for

**Troy McDonald Kane:** So the the what needs to be smoothed out a little bit,

**George Westbrook:** that.

**Troy McDonald Kane:** George, too, is that there should never be a moment where there's not a bid an offer. Now the bid and offers can widen and tighten.

**George Westbrook:** Yeah.

**Troy McDonald Kane:** But what I saw or was observing is that whenever you were re-calibrating, you would wipe out all three levels and then you had like a split second of no bid or offer. And I know both Jared and I had experiences with the market order functionality where it's

**George Westbrook:** Yes.

**Troy McDonald Kane:** not the liquidity is not there by the time the market order is in flight and it's not completely filled or you know which is not the obviously user experience that we want.

**George Westbrook:** Yeah.

**Troy McDonald Kane:** We need to smooth it out so that there's a consistent three levels.

### **00:19:58**

**Troy McDonald Kane:** And you know, if you're widening out, if you're recalibrating, it should be widen out, tighten in kind of criteria because there's no other market makers there that that can support that liquidity. We are the So, we almost have to operate as like two or three market makers at once because um there's no

**George Westbrook:** Yeah.

**Troy McDonald Kane:** one else leaning on us or we're not leaning on anyone else. So, we can take that offline,

**George Westbrook:** H.

**Troy McDonald Kane:** but right now the priority is definitely we got to get the app back up and running. Um, there's obviously still a few um things that we brought to your attention last week that still need to be kind of uh retailered on the app as far as, you know, how the tiles look, the information flow, things like that. Um, I know we keep sending you stuff one off in the in the in the Slack, so we assume that's being picked up by AI.

**George Westbrook:** Yeah.

**Troy McDonald Kane:** Yeah.

**George Westbrook:** Yeah. I think the the so I think with the momentary the momentary where there's not there's not anything and it gets wiped that's that is by design at the moment um is not an error because I think

### **00:21:00**

**Troy McDonald Kane:** It's

**George Westbrook:** with with T0 you can't do like a a replace in place. It has to be a cancel and then a replace. So we need to work out how are we going to do it where it's either topping up or it's it's clearance. So so it like you said that there's always something on there at one time. Um but yeah, unfortunately at the moment that is that is by design. So there's two options are work out a better design um or make it so fast that that's not even the case or have there's always a

**Troy McDonald Kane:** Okay.

**George Westbrook:** solution

**Troy McDonald Kane:** And then my other other thing to note is do we need this T0 call today or can we cancel it so you guys have more time to work on this stuff? Is there anything outstanding you needed to get from them today from today's call? because otherwise I'm just going to have them cancel today because um you guys have a lot of stuff you need to figure out

### **00:21:56**

**George Westbrook:** Yeah, I I think I think that would be best.

**Troy McDonald Kane:** today.

**George Westbrook:** I mean, there's no no issues we've had with with their side and usually if there's if there's something urgent, Rob's Rob's on it straight away.

**Troy McDonald Kane:** Yeah,

**George Westbrook:** So,

**Brett StClair:** And I don't think Rob's on the call. What is it?

**Troy McDonald Kane:** Evangelist isn't this week.

**Brett StClair:** Evangelist.

**George Westbrook:** Oh,

**Troy McDonald Kane:** So he sent out a note.

**George Westbrook:** okay.

**Troy McDonald Kane:** Rob wasn't last week, but yeah. So, as long as you guys are getting what you need from them, I'll just tell them that we can cancel this morning's call and then you guys are freed up to go get this app back up and running because uh we never know who might try to log on to it and

**George Westbrook:** Yeah.

**Troy McDonald Kane:** and check whatever. So, we are getting active enga more active engagement even though it's not a game day.

**Jared Sapirman:** And to piggy back off of what Troy said in regards to market orders, there was not actually a single time where I had a an order of more than I would say 50,000 that fully filled.

### **00:22:51**

**Jared Sapirman:** That would never happen.

**Troy McDonald Kane:** Well, there's never there's never that much liquidity at that.

**Jared Sapirman:** Uh

**George Westbrook:** Yeah, that's that's

**Troy McDonald Kane:** Why? Like they're only doing like couple hundreds lot.

**George Westbrook:** right.

**Troy McDonald Kane:** If you look at the liquidity pool, it's never it's never big enough to sustain a 50,000

**Jared Sapirman:** I see that I well it was only well

**Troy McDonald Kane:** lot.

**Jared Sapirman:** $50,000 but it was only but um even

**Troy McDonald Kane:** Oh. Yeah.

**Jared Sapirman:** still at like a

**Troy McDonald Kane:** How many shares was that?

**George Westbrook:** But babe,

**Jared Sapirman:** thousand

**Troy McDonald Kane:** Yeah.

**George Westbrook:** yeah,

**Troy McDonald Kane:** That even a thousand's too much. Like that's what we're saying.

**George Westbrook:** that's

**Troy McDonald Kane:** Like it's the liquidity profiles are not large enough to support that type of uh order size right

**George Westbrook:** cuz we we did have the so whereas before I think this was the first dry run,

**Troy McDonald Kane:** now.

**George Westbrook:** it was minimum three levels, maximum maximum six levels with everything in tranches of 500 with a bit of randomization in with the maximum amount of quantity being 10 10 to 15,000.

### **00:23:46**

**George Westbrook:** Then I think everyone wanted it squashed right down. So I think the max quantity per side is between 500 to I need to double check that. Um, so getting a a th00and filled on a market order is pretty much not not going to happen unless it's it's coming from other people apart from the market

**Jared Sapirman:** But can't you make it so that it would go through the bids or go through the asks?

**George Westbrook:** maker.

**Jared Sapirman:** If I buy at the ask and there's only 500 at the ask, there's got to there's other levels normally and it could it could just by I thought

**George Westbrook:** Sometimes

**Jared Sapirman:** Troy you said that it was up to 30% that it would go up

**Troy McDonald Kane:** Yeah, but what's happening is if others are hitting the same market at the same time also the market makers

**Jared Sapirman:** to

**Troy McDonald Kane:** is resetting the bid offer. What I noticed as I was doing that is that it would get a partial fill and then the book would reset. So in that reset in that cancel replace the liquidity is actually more phantom liquidity because it's not there and it's in the process of being cancel replaced and so the order can't be can't go through the book because the book is being reset.

### **00:24:51**

**Troy McDonald Kane:** I still think the market makers updating too frequently. Um but that's that's Edwin's discretion. He wants it set a certain way because it I missed the market so many times because every time I was going to hit the market or lift the market the market maker algo was resetting. So that you know there was no liquidity there to fill because in that moment the liquidity was being reset. So I don't know if we need to go larger quantities, we need to go to depth of five. I I don't know yet because if we we do have, you know, tens of thousands of users and they're all trying to go after the same market, which is very probable because there's going to be times where that's the only game people care about and want to trade. And if there's not enough liquidity to sustain the ability to trade, then it's going to degrade the user experience

**Jared Sapirman:** significantly. Yeah.

**George Westbrook:** Yeah.

**Jared Sapirman:** Especially like my thought is on in a game where it was like the Hawaii game uh the

### **00:25:40**

**Troy McDonald Kane:** dramatically.

**Jared Sapirman:** Hawaii versus Stanford game where Stanford was up by a lot. Then Hawaii made a massive comeback and there was drastic price movement where a lot of people would probably be trading that and then Stanford ended up beating Hawaii in the last minute where so there massive volatility, massive movement. I could see so many people trading that specific game where the other games were not even remotely close. That game, the trading experience would be degraded significantly because so many people would be on it and they wouldn't be able to get

**George Westbrook:** Yeah, the the maker needs more variables in in order to

**Jared Sapirman:** filled.

**George Westbrook:** determine levels and quantity because exactly like you said it needs to take into account trade maybe trading volumes during the game. Um and then expanding out maybe the quantity based on the number of participants in the market. Um whereas at the moment it is this is the bounce for quantity. These are the levels. The quantity is random within certain bounds. The levels are almost completely random.

### **00:26:53**

**George Westbrook:** Um, so it's like you said, it's not it's it's not taking into account participation in the market when building the actual market is purely based on certain aspects that are coming from sports radar which are more like determinist like this is the this is the win probability but there could be a thousand users or 10,000 users the market maker still going to be still still going to be functioning in more or less the same way by design by design so I I agree that things do need to be improved there um I suppose it's just up to up to Edwin as to what what he he sees fit.

**Jared Sapirman:** Okay.

**Troy McDonald Kane:** Okay. Okay. Um, anything else? I know you guys have to go and get this. I know we have another call tomorrow. I don't know if we need to make that an hour, Brett, tomorrow.

**Brett StClair:** Yeah, let's finish off the um subscription services.

**George Westbrook:** Yeah.

**Troy McDonald Kane:** Um,

**Brett StClair:** Do like a design session on that.

### **00:27:55**

**George Westbrook:** On that.

**Brett StClair:** Um just on the chat group,

**George Westbrook:** Um just on the chat for

**Brett StClair:** I do that once a week. I take everything that's in the chat and actually manually put it into the vault. So if we do find stuff that we logged in the chat and it hasn't been picked up, it might be because of that. So, I'll see if I can do it more frequently. Um, it's just a manual, me remembering to do it at the moment. So, if you are seeing stuff that's missed, my apologies.

**Kevin Murray:** All right,

**Cody Haugen:** Yeah,

**George Westbrook:** Boom.

**Cody Haugen:** sorry.

**Brett StClair:** Cool.

**Cody Haugen:** I have one one other thing.

**Troy McDonald Kane:** Okay.

**Cody Haugen:** Uh, Hasan,

**Kevin Murray:** cool.

**Cody Haugen:** and and we can take this offline. Just I just wanted to mention it real quick. You keep saying uh that you're going to edit uh the admin panel so that I can change like some of these websites and stuff like that. Is that just the inplay hyphen admin panel that I'm going to like we went to

### **00:28:49**

**Hasan Ahmed:** Yeah.

**Cody Haugen:** for the feedback and the vault and that type of thing? Is that going to just be like another section you're going to add in there for us?

**Hasan Ahmed:** Um I mean I think it's going to be on the I think trading admin panel. I just need to um like extend onto it. And so if you want to edit groups uh then create groups and like edit the share codes as well. Like I just need to add that as extra functionality onto that and then

**Cody Haugen:** Okay, that no. Yeah, that that would be amazing.

**Hasan Ahmed:** Yeah.

**Cody Haugen:** That sounds great. I don't believe I have access to that. I think Edwin's the only one that has access to that.

**Troy McDonald Kane:** That's

**Cody Haugen:** Um,

**Hasan Ahmed:** Yeah.

**Troy McDonald Kane:** right.

**Cody Haugen:** so yeah, just a a quick point, but yeah. Okay, sounds good. Thank you very much.

**Hasan Ahmed:** Yeah.

**Cody Haugen:** Yeah, because I would like to ping you less and be able to sort on our time zone as opposed to you got enough to work on. Cool. That's it from my side.

**George Westbrook:** Perfect. Right.

**Cody Haugen:** All right.

**Brett StClair:** Right.

**George Westbrook:** I think I think that's everything.

**Kevin Murray:** Perfect.

**Brett StClair:** Have a

**Cody Haugen:** All right.

**George Westbrook:** Have a good one.

**Kevin Murray:** Right.

**George Westbrook:** Speak to you.

**Cody Haugen:** Sounds Y.

**Brett StClair:** good

**George Westbrook:** Speak to you tomorrow.

**Cody Haugen:** Thanks,

**Kevin Murray:** Have a good one.

**Cody Haugen:** guys.

**George Westbrook:** Cheers.

**Cody Haugen:** Thanks.

**Hasan Ahmed:** Get messages.

**George Westbrook:** The right.

**Hasan Ahmed:** Because

### **Transcription ended after 00:30:06**

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*