---
date: 2026-06-15
type: standup
status: extracted
extracted-to:
  - "[[digests/touchdowns-12-17-jun-2026]]"
  - "[[information-layer/information-layer]]"
  - "[[ipo-module/ipo-module]]"
  - "[[earnings-report/earnings-report]]"
  - "[[components/components]]"
  - "[[architecture/open-questions]]"
description: "Transcript of the 2026-06-15 InPlay touchdown call — payment-provider debrief, zero-advertising crisis, pre-launch data preview, and earnings-report placement"
---

## Post-Call Analysis

> Processed as part of the **[[digests/touchdowns-12-17-jun-2026|12–17 June touchdown sweep]]**.
>
> ⚠️ **Parked (not extracted):** this call also contained an extended **strategic / contingency discussion** (advertising-commitment risk ahead of launch, a possible university-only fall challenge, and an investor conversation). Per the product owner, this was standup overflow that should not have happened in a sync; it is **not** written into the vision, components, or any changelog. Recorded here only so the conversation is traceable to this date. No graph impact.

| Finding | Destination | Action |
|---------|-------------|--------|
| **Pre-launch data preview** — SR historical data, grayed-out trading, IPO countdown (CFB ~22 Aug / NFL ~2 Sept); 2013-vs-1-year history debate | [[information-layer/information-layer]] / [[ipo-module/ipo-module]] | Update notes |
| **Title-sponsor splash screen** (2–3s on app open) | [[information-layer/information-layer]] / [[components/components]] (Advertising) | Update + cross-cutting note |
| **Synthetic off-field pricing** (ad-spend model) for the pre-launch IPO preview | [[ipo-module/ipo-module]] / [[earnings-report/earnings-report]] | Update note (preview input only) |
| **Earnings-report placement** — own page + embedded team-page box, trade button kept, ~15-min pre-release push | [[earnings-report/earnings-report]] | Update note |
| **AI brand-preview tool** (Max) — self-serve advertiser preview across ~10 units, goes in outreach emails | [[components/components]] (Advertising) | Cross-cutting note |
| **Advertiser KPI framework** — buyers prioritise CPA/CPM over engagement-minutes; IAB currency | [[components/components]] (Analytics) / [[architecture/open-questions]] | Note + open-question row |
| Strategic / contingency discussion (ads risk, university-only pivot, investor talk) | — | **Parked** per owner; no graph impact (see note above) |
| App feedback backlog (~20 items, ~4 weeks) | — | Status only |

**

Jun 15, 2026

## InPlay Digital TouchDown - Transcript

### 00:00:12

  

Skye Capazorio: Hello.

Kevin Murray: Morning, afternoon, how are

Edwin Johnson: Hello.

George Westbrook: I don't think your mic's working, bro.

Skye Capazorio: Yeah, George is like, "Yes, it's not

Kevin Murray: we

George Westbrook: I'm fine this time.

Skye Capazorio: me.

George Westbrook: It's actually work working as soon as I got into the call.

Edwin Johnson: How you been, George?

George Westbrook: Good, good, good,

Edwin Johnson: Haven't seen you in like a week.

George Westbrook: good

Edwin Johnson: Feels like I You're a different person.

George Westbrook: weekend.

Edwin Johnson: You're all grown up.

George Westbrook: No, I've actually had a shave for once. I'm not really not not really a shaving

Edwin Johnson: Thank you. Yeah. No, no,

George Westbrook: person.

Edwin Johnson: me neither. Um, but now we've got Max. His hair is grown out. Looks like he's over 21 now. It's a good

George Westbrook: Yeah, but when he opens his mouth, you can work out.

Edwin Johnson: day.

George Westbrook: No, this this guy is definitely

Max Kingaby: the most intelligent person on the call.

George Westbrook: That That was a good joke, Max.

  
  

### 00:01:06

  

George Westbrook: We've actually got We've actually got a tally for the amount of jokes, funny jokes Max makes. I think for the past two or three months,

Skye Capazorio: Okay.

George Westbrook: he's currently sat at two.

Edwin Johnson: Oh wow, that's way more than I

George Westbrook: Yeah.

Edwin Johnson: expected

George Westbrook: How were your weekends? Was it a bit big hangovers from last

Edwin Johnson: for me personally. Um I, you know,

George Westbrook: week?

Edwin Johnson: I I'm having trouble with travel.

Kevin Murray: No.

Edwin Johnson: I mean, I'm I'm it's not good for my body, obviously. you know, you have a little bit of fun or whatever, but um I've been having these crazy leg cramps in my sleep in Miami. I don't know what happened. Have you guys ever had that? It's unfreaking real.

Skye Capazorio: I

Edwin Johnson: It's like the hand of God or Satan, whoever you know you're dealing with that day, has a has a incred it's just it's it's almost impossible to walk, you know. So I um I had forgotten my passport and I don't have one of those real IDs to travel.

  
  

### 00:02:06

  

Edwin Johnson: So I don't know by the grace of God we got lucky. I didn't I was able to get on the flights. The last one I went as Kevin Murray and you know I you got this little old man you know clearly you know seen better days. I'm walking. So they took a lot of mercy on me. So that that that's my new vibe though. I'm going with the uh old man with a limp move. that turns out.

George Westbrook: Brett's doing that,

Skye Capazorio: Okay.

George Westbrook: but he hasn't got a choice.

Edwin Johnson: Well,

Brett StClair: I need to say

Edwin Johnson: I mean, it's tough because you know, Brett,

Brett StClair: that.

Edwin Johnson: I'll be honest with you, the son called me over the weekend and he told me, "Brett's not your real name." He said, "Your real name is Jerry Atric." Is that

Kevin Murray: What the

Edwin Johnson: true?

Brett StClair: I think we need a a board to keep count of Edwin jokes

Kevin Murray: heck?

Edwin Johnson: No, they're they're all um but I I'm I'm feeling a lot older.

  
  

### 00:02:59

  

Brett StClair: now.

Edwin Johnson: I feel like Brett's my son. That's how I

George Westbrook: Yeah.

Edwin Johnson: feel.

Brett StClair: You know,

George Westbrook: This

Brett StClair: I think we're like five years difference. You know that?

Edwin Johnson: I know. I mean, I I started early. What I can say I started early and I gave it a run. A good run.

Brett StClair: Beautiful.

Edwin Johnson: All right.

Skye Capazorio: Roy,

Edwin Johnson: So, what's

Skye Capazorio: you look like you've also had your hair done.

Edwin Johnson: our

Troy McDonald Kane: me.

Brett StClair: Which way?

Edwin Johnson: Oh,

Brett StClair: Oh, look at that.

Skye Capazorio: Troy

Edwin Johnson: wow.

Brett StClair: Here we go.

Troy McDonald Kane: This is the summer summer cut.

Brett StClair: Hey.

Edwin Johnson: Wow.

Troy McDonald Kane: Tight on the sides, long on top.

Edwin Johnson: It looks dark, too.

Troy McDonald Kane: Yeah,

Brett StClair: Oh.

Edwin Johnson: It looks like you mean business.

Troy McDonald Kane: I do mean business, Edwin. We have a very big week,

Edwin Johnson: That's good to know.

  
  

### 00:03:47

  

Troy McDonald Kane: so Every week seems to get

Edwin Johnson: Maybe the biggest week of our lives. Well, at least my life. That's, you know,

Troy McDonald Kane: bigger.

Edwin Johnson: and yesterday I think I fell asleep about 15 times, literally just like for five minutes, 10 minutes. I fell asleep in my garage behind the wheel.

Troy McDonald Kane: Oh

Edwin Johnson: That's that's that's how bad it's been.

Troy McDonald Kane: man.

Edwin Johnson: So, um stress, you know, plus the stress involved. So, I I haven't spoken to any of you guys since last Monday. Um you know, we obviously had an interesting week. Have are you guys all caught up on where we're at and what happened or you guys get a rundown for the most

Troy McDonald Kane: They got a little bit on Friday,

Max Kingaby: Kevin told

Edwin Johnson: part?

Troy McDonald Kane: but you may it'd be good for you to recap from your perspective because we heard it from Cody and and I'm sorry,

Edwin Johnson: Oh yeah, he's a liar.

Troy McDonald Kane: we heard it from Kevin,

  
  

### 00:04:37

  

Edwin Johnson: Oh, he's a bigger liar.

Troy McDonald Kane: not Cody.

Kevin Murray: Even

Edwin Johnson: Even worse. Well, I will say this. Kevin was amazing at the convention.

Skye Capazorio: Yes.

Kevin Murray: worse.

Edwin Johnson: I mean, they he and Tony, uh, Cody, everybody was was on really did a great job. And, uh, we were fortunate that we had this kind of layover on Friday. um not a layover in terms of different cities, but we had a little bit of time where the three of us were able to sit and kind of like strategize after what we found out from the week.

Skye Capazorio: I'm

Edwin Johnson: Um what we found out from the week was we're clearly a huge target for payment providers.

Skye Capazorio: getting

Edwin Johnson: Uh I would say massive target. Okay. Uh that that was that that was the overriding element. Cody had set up a meeting with this company called Kayafe which we all prepared for. Excuse me. That went pretty well. Um, you know, the gentleman who introduced us, uh, uh, it was, you know, an acquaintance of Cody who's works internally, uh, his boss was a complete stroke in my opinion.

  
  

### 00:05:40

  

Edwin Johnson: Uh, like a 35 to 42 year old like pretty boy, you know, got a great job. I don't pay attention to anybody guy. Um, but so for our first 20 minutes of a 45m minute conversation, maybe even a little bit longer, you know, this guy was totally disengaged, a complete uh f*** in my opinion. Uh, given that we had spent a lot of money and time to come down and see him. Uh, but at the last 20 minutes or so, it started to really hit home to him. And he actually asked a question or two, which was, you know, surprising because I I didn't think that guy could actually speak. Um, now the person that was internal that made that introduction, huge fan, uh, pretty well-known guy in the industry and definitely a savvy, experienced veteran, definitely sees the, you know, the benefit of it. So, that went pretty well. Um, I I don't hold a lot of hope in it. Uh, to be candid, I have I'm probably like a 25% uh, probably 5050. We have a follow-up call, but I'm probably 20% that there's anything here of substance.

  
  

### 00:06:57

  

Edwin Johnson: That's my read. Cody, what's

Cody Haugen: Well, you know me, I'm an eternal optimist,

Edwin Johnson: yours?

Cody Haugen: so I I like to uh think there was a little bit more behind that. Um, they spent the time with us. I mean, he didn't get up and walk away.

Edwin Johnson: I wish you would

Cody Haugen: Um I I I I feel like the meeting went went very well, as well as it could have. Um Terry, I caught up with him uh Thursday afternoon for like stogies and sips and uh he understands the the timing and the pressure. He's going to have a follow-up call with that stroke named Greg uh today. And uh and then he he basically said if I need to go above Greg, who is the head of North America, I will go to Alex. I always say Alex. I think it's actually Zach. Uh who's their their global head of gaming. And he said if I need to go above Greg to go to Alex, I will. Alex, Zach, whatever his name is.

  
  

### 00:07:56

  

Cody Haugen: Um I will. So I I I think we will get something. Now, if it's a my concern here, Edwin, is do and and what we talked about on Friday morning waiting to to take off is do we get these in the time that we need these? I think we do get engagement from them. Um, so that that's that's my read. That's my feedback on on Stay

Edwin Johnson: Cool. Yeah. Okay. Um then we'll move on to the next I would call it the next substantive meeting we had which

Cody Haugen: safe.

Edwin Johnson: was drum up out of nowhere by Kevin and Tony. Um that was with a company called Pay.com. Now, pay.com. Um, man, you sound hear that it sounds like a really a big name because it's like who who owns Pay.com? It's got to be a big big big entity, at least to me, right? Um, and you know, that particular group is interesting because they're very active outside the US. Um, they're they're Israeli backed and um they're backed by a pretty famous Israeli named Teddy Sagi.

  
  

### 00:09:05

  

Edwin Johnson: And I've known of Teddy Sagi before. um this call. I I uh never thought I'd ever speak to him uh during the meeting.

Skye Capazorio: Thanks.

Edwin Johnson: We actually did. Um so Kevin and uh Tony had met with their group the day prior and then they said, "Hey, sounds good. You should come back and meet our CEO." Which we did. We had about a half hour schedule that turned into about an hour and a half of, you know, gobetweens and whatnot. And uh that pitch went incredibly well, but I want to I want to temper the expectations. And this is at a conference. You know, conferences, you know, I I don't know I don't know what happens, but everyone almost like plays work, but they don't do anything. You know, there's a lot of discussions, but not a lot happens in my experience for me. Now, I'm not a seasoned veteran like Cody at a conference. Um, but I just find that most of the people who are there are like, but this particular guy being the CEO, he actually was someone who could do something.

  
  

### 00:10:09

  

Edwin Johnson: The the initial response was, "Of course, we'll do the payments." You know, that was kind of like a no-brainer. They want the payments. Um, I said, "One of our issues is we need the advertisement." And you know that's where you know he said look we we're not a BTOC um offering we're a B2B offering and that's the issue with the um uh marketing spend. However he said you know I pro provide proc uh payment processing for other companies one another one owned by that Teddy Sagi uh which is uh the ExpressVPN um and that's a big uh big company worldwide. Um, you know, he's he's a he's a very wealthy guy. He's got a color colorful background. Um, you know, some might say uniquely colorful. Um, and he he's probably, you know, one of the uh wealthiest people in Israel. Uh, so he's I don't know if he's worth, you know, five, 10 billion, whatever, but you know, whoever knows these things. Um, but so we got on the phone with Teddy Sagi right there.

  
  

### 00:11:18

  

Edwin Johnson: So he's like, "Look, tell him what's up." And, you know, I think this can can work for him. He just invested in prediction markets, 250 million bucks. Uh, this might be a great hedge for him, and it definitely has the ability to help out with his B TOC product. Um, and then right after we hung up that call, we, you know, I want you to picture this dude's holding his phone and he's got earpieces in, one in his ear. He put the other one in my ear. And then we called another billionaire who was uh a casino owner and the casino I I knew of these first two guys before that meeting um who ex expressed a lot of interest. Now if we open up the casino route for advertising this would be a this would be a no-brainer because by and large all of their customers are US-based.

Cody Haugen: Yeah. So,

Edwin Johnson: Okay.

Cody Haugen: for the just sorry to interrupt Edwin, but just a quick u piece of information there that's so important.

  
  

### 00:12:17

  

Cody Haugen: These are sweep stakes casinos that they own, not landbased traditional casinos. So, they're all trying to grab as many users as humanly possible before sweep stakes continues to get shut down on a state-by-state basis. So, like California's already said no sweeps. Uh there's a couple other states that have said no sweeps. Illinois is actually trying to run them out um to not great success, but but they are.

Skye Capazorio: Thank

Cody Haugen: So, these are all very user uh user focused acquisitions.

Skye Capazorio: you.

Cody Haugen: And so, that's why they're very excited about it.

Edwin Johnson: Yeah. Um and he's spending that dude spending like 10 million bucks a month on advertising and you know for them to spend a million or two of that with us. Um and actually the CEO of that paid.com said you know it I would try to convince him to do three with yours because of the direct you know uh I forget what he said but the you know interaction between uh the user a potential user and conversion to him.

  
  

### 00:13:20

  

Edwin Johnson: Um, and then we we you know then him and I he said, "Hey, let's have a coffee." We went for an hour, had a even more discussion, called another wealthy Israeli who um I forget what business he had, but he had another business. All the calls went like as good as they could have went and we'll see what happens. Um they're going to get back to us this week and see what they want to do. Um, so that was very very exciting, very positive. But, you know, again, with a healthy dose of reality, you know, I'm I'm at like a on that one, I'm probably at like a 5%. Maybe maybe 10. That's something will come of it. Um to to be to be honest. I don't know. What about you, Kevin or

Kevin Murray: Yeah,

Edwin Johnson: Cody?

Kevin Murray: I thought definitely with the the pay.com I think the 100% like we'll probably hear from I'll reach out and speak to Charles today. Uh he was the guy I spoke to um on the first day to set up the meeting.

  
  

### 00:14:18

  

Kevin Murray: again 100% be interested in in getting that but again it's trying to see if these other guys decide to to come on um and where they are but I do feel Tom who's the

Edwin Johnson: Yeah.

Kevin Murray: CEO that had the calls I don't think he would have reached out to all these people there and then while we're sat around this small little coffee table if he didn't think there was something to it

Edwin Johnson: No doubt. I mean and that that uh discussion did kind of lead way into like you know

Kevin Murray: So,

Edwin Johnson: in lie of him uh using advertising you know either pay.com investing or these other ones taking a piece of equity and we negotiated basically uh 30 million bucks for 20% of inplay uh was what we discussed I mean you know after the after the buzz wears off, you know, you're Does this sound realistic? And, you know, to me, I'm I won't say I'm pessimistic. I'm I'm realistic, which leads me to kind of where we're at. It's the 15th of June. I mean, I'm I'm having massive concerns about how we're going to get any advertisement before the um challenge at this point.

  
  

### 00:15:38

  

Edwin Johnson: Um, you know, it's just the the realist in me. We've got two months. I've been active over the weekend calling everybody I know and trying to work every angle we possibly can uh uh work and you know, we'll see at the end of this week how that works out. I think when when do I turn into a pumpkin, Cody? What what day are you telling me?

Cody Haugen: two more weeks.

Edwin Johnson: Two more weeks. So, we've got till the end of June to see what it is.

Cody Haugen: Yep. That that's been my my D-Day since we since we had to revamp and go direct. I I I'm I'm giving I'm giving Payafe. I mean, like I said, I pushed every button.

Edwin Johnson: No doubt.

Cody Haugen: I told Yeah.

Edwin Johnson: No doubt. This has nothing to do with us,

Cody Haugen: I told him,

Edwin Johnson: Cody.

Cody Haugen: "No, no,

Edwin Johnson: This has nothing to do with the offering.

Cody Haugen: no, no." Yeah.

Edwin Johnson: Nothing to do with us.

  
  

### 00:16:26

  

Cody Haugen: No, no.

Edwin Johnson: I mean,

Cody Haugen: I'm just saying that I expect to hear back from Terry this week.

Edwin Johnson: the meeting

Cody Haugen: I said even if it's a even if it's a no,

Edwin Johnson: Yeah.

Cody Haugen: we need a fast

Edwin Johnson: No, no, I understand that.

Cody Haugen: no.

Edwin Johnson: I'm saying even if like the the person that would make the decision that I understand would make the decision that Greg he's a

Cody Haugen: Yeah.

Edwin Johnson: no he wasn't engaged enough in my opinion but we'll

Cody Haugen: until Terry beats him down a little bit

Edwin Johnson: see maybe maybe

Cody Haugen: more.

Edwin Johnson: but uh the one green uh under or silver lining the person that works at Pay Safe that Cody knows asked if he could asked if he could invest

Cody Haugen: I I haven't gone back to him on that,

Skye Capazorio: That's

Cody Haugen: but yes,

Edwin Johnson: 100k.

Cody Haugen: he did he did have a serious conversation.

Skye Capazorio: funny.

Cody Haugen: It was just me and him smoking stogies in the lounge. And he said, "If this doesn't happen, I have 100k. Would you guys be interested?" And I said,

  
  

### 00:17:20

  

Cody Haugen: "I'll talk to Edund about it."

Edwin Johnson: Which the 100k isn't going to move the needle, but the I mean that tells you he's a believer. So,

Cody Haugen: Yeah.

Edwin Johnson: so yeah, I mean, so you know, my my concerns are are fraught with reality. Um, you know, I haven't decided what I want to do yet, but I mean, we may not run the the any trading challenge uh for the fall. Uh, it may be a bust. Okay. I mean, it's, you know, where where we where I thought we were at in terms of interest and ads and people, um, is not where we're at. So, um, you know, had I thought in April that by the mid June or towards the end of June, we're not going to have anybody, I mean, obviously, this is not a route I would have taken. I would have taken a different route. So, um, you know, Troy and I talked a little bit about maybe doing a universitywide only, um, with with, you know, so only, uh, colleges that have signed up.

  
  

### 00:18:28

  

Edwin Johnson: There might be something there. Um, but I have to, you know, take a real realistic look at like what I'm willing to do personally because if I'm footing the bill for all this, it just it's it's a big number. 25 million bucks, no advertisements. It's like that's a big number and I'm very very concerned about, you know, if I can be honest, you know, I'm I'm I'd rather just talk it through. You know, I did not expect us to have zero advertising at this point or zero commitment. I just it I don't I don't even know how it's possible. So, but it is what it is. And you know, we have to play reality, not uh you know, hopes and

Cody Haugen: I think yeah I think we we we give it two weeks.

Edwin Johnson: dreams.

Cody Haugen: We see where we land there and then I think we talk about what a five or even three like we talked about on Friday. Three is still a huge number, Edwin. I mean I think we still get a lot of people to come out of the woodwork for $3 million.

  
  

### 00:19:27

  

Cody Haugen: I I know you're footing the bill. I can't make that decision for you. But I think not running it is we we need the numbers to prove it at any level. And even with three, we get the numbers to prove it out. And then and then like I said, if the advertisers don't come on in the first month, we prove out the numbers. We can still get advertisers during the season. And we don't change our pricing because we were on a billion minutes anyways.

Skye Capazorio: What's happening?

Cody Haugen: They still pay full freight even if they miss a month because they never saw Yeah.

Edwin Johnson: I I I hear that.

Cody Haugen: They never saw the pricing to begin

Edwin Johnson: I hear that.

Cody Haugen: with.

Edwin Johnson: So you over the last year and a half a key component was the off-field revenue.

Cody Haugen: Yeah.

Edwin Johnson: How this works,

Skye Capazorio: Oops.

Edwin Johnson: right? That was based in the belief that there were going to be advertisers that were coming in.

Cody Haugen: Yeah.

  
  

### 00:20:14

  

Edwin Johnson: Now, like as I went through the offering circular as we get close to production launch, I mean, not having any advertisers is not doable, right? It's I I I mean, so, you know, I've got to I've got to figure out another kind of quasi pivot here, but um you know, right now we're in the lurch. You know, it is what it is. And you know, not zero advertising is not something that can happen. You know, even if I take a loss, I'll take a loss, but zero. I How do we get no one to f****** advertise on there? It's just it's it I'm I'm more than befuddled. So, that's that's the stark reality of things. Any questions from anybody? Cool. Okay. What's

George Westbrook: So I think when when we were all speaking on Friday,

Edwin Johnson: next?

George Westbrook: one of the things we were thinking is the kind of pre the pre-launch version of the application. So what what does that look like?

Skye Capazorio: Oh, f******

  
  

### 00:21:23

  

George Westbrook: What do we want to expose?

Skye Capazorio: s***.

George Westbrook: What do we not want to expose? Um, and sorry. Yeah, just in terms of obviously on boarding KYC, I mean that's obviously 100% needed. It's it's just what what does that experience look like before the IPOs have happened before users can actually trade. Um, so I suppose it's yeah, because there's there's everything from being able to check all the past data, blah blah blah, or is everything a bit more gated? Um, so I suppose it's just kind of throwing that up in the air and seeing what what is it we all think needs needs to be there on the pre-launch

Edwin Johnson: team. What do you guys

Troy McDonald Kane: So what?

Edwin Johnson: think?

Troy McDonald Kane: So 100% the KYC and the referral program, but we need something else, you know, there. And Cody and I and Kevin have talked about data. So Cody, what are your thoughts on what type of data? I mean, we talked about other sports, but we don't want to confuse potential participants around what's available in the training competition versus what's in the app pre-launch.

  
  

### 00:22:31

  

Cody Haugen: Yeah, I mean, we've talked about this before, but yeah, I guess to reiterate what I think is valuable, it's I think offseason additions and subtractions per team. Um, so key players leaving or coming to the team is extremely valuable. People will want to know about that before the IPO. um and why this team is valued at X or why this team, you know, was good last year but not good this year um so to speak.

Edwin Johnson: Tony,

Cody Haugen: Um obviously M

Edwin Johnson: can you can you bring in the totals for the

Cody Haugen: we we can bring in projections um for that.

Edwin Johnson: season.

Cody Haugen: Absolutely. So like you're saying win totals? Yep. Absolutely. I mean you can find that public sources.

Edwin Johnson: Yep.

Cody Haugen: Um, I would say it's probably not really released until probably after July. Um, but we could start to make our own. Um,

Troy McDonald Kane: Well, no. I think at least for this first iteration,

Cody Haugen: basically

Troy McDonald Kane: we need to focus on what we can get out of sports radar since the API is already plugged into the app versus introducing another element.

  
  

### 00:23:36

  

Troy McDonald Kane: Maybe in the second iteration we can think about that as we get closer to the IPOs,

Cody Haugen: Yeah.

Troy McDonald Kane: but right now we should What can we get out of Sports Radar's data offering that we can put in the app that would be interesting to potential

Cody Haugen: Yeah. So I think it's it's last year's so so yes going back to what we had talked about last year's

Troy McDonald Kane: users

Skye Capazorio: Okay.

Cody Haugen: data um in summary on a team basis of course um their additions and subtractions whether that be free agency or the draft all of that's in the API um and then um schedule data right like I mean just just simply put who are they going to play um and and so I think those three pieces allow people to

Troy McDonald Kane: Yeah.

Cody Haugen: do enough research search that they will actually interact with the app before there's actually live

George Westbrook: What else?

Skye Capazorio: Thanks.

Troy McDonald Kane: So Cody,

Edwin Johnson: Great.

Skye Capazorio: Can I just

Troy McDonald Kane: can we can we the Sports Radar offer the projected odds at the

  
  

### 00:24:23

  

Cody Haugen: data.

Edwin Johnson: Yes.

Troy McDonald Kane: beginning of last season and then where they ended and we can we map that side by side or is that too

Edwin Johnson: Yeah.

Troy McDonald Kane: much?

Edwin Johnson: He's saying they're not going to come out till July.

Troy McDonald Kane: No, no.

Edwin Johnson: I mean,

Troy McDonald Kane: I'm talking about last year's results to see where they started and where they finished.

Edwin Johnson: I think the totals

Cody Haugen: Yeah. Yeah. Yeah.

Troy McDonald Kane: So you can see like what the delta was between the start of the season and the end of the season for all 32. Well, actually we want to do it for the NCAA teams as well,

Cody Haugen: Yeah. Yeah. I mean,

Troy McDonald Kane: right?

Cody Haugen: we I would want to do it for everything that we're offering once it's a live app. Yeah.

Skye Capazorio: It's

Cody Haugen: Absolutely. So that they can see one to one what it looks like once it goes the season starts.

Troy McDonald Kane: Yeah.

Cody Haugen: Um and to answer your question in short, yes, absolutely true.

  
  

### 00:25:09

  

Cody Haugen: We can go back historical data back to 2013. So

Skye Capazorio: Just just a quick

Troy McDonald Kane: that could be like as a potential user especially on the college level.

Cody Haugen: yeah,

Skye Capazorio: question.

Troy McDonald Kane: I would like to see like where they were projected to be at the beginning of their season and where they ended up and get help me

Cody Haugen: it's

Troy McDonald Kane: think about strategy as these IPOs become available August

Edwin Johnson: the totals are out already,

Troy McDonald Kane: 22nd.

Edwin Johnson: Cody.

Cody Haugen: the the totals are are live.

George Westbrook: Sorry. When you say totals,

Cody Haugen: Okay.

Edwin Johnson: Yeah.

George Westbrook: what do you what do you

Cody Haugen: W win totals,

George Westbrook: mean?

Cody Haugen: George. So a team is projected nine and a half wins.

George Westbrook: Oh, okay.

Edwin Johnson: Yeah.

George Westbrook: So, so the like probabilities for what's going to happen in the season.

Cody Haugen: Right.

Edwin Johnson: Yeah. So, there's there's there's a betting market,

Cody Haugen: Yeah.

George Westbrook: Okay.

Edwin Johnson: what they call futures, okay, which will be like how many wins will the Buffalo Bills have?

  
  

### 00:25:50

  

Cody Haugen: Yeah.

Edwin Johnson: Right now, they're at 12.5 wins. That's what's expected. 12 and a half. So, you can bet over that or under that.

Cody Haugen: Yes.

Edwin Johnson: And that's a futures contract. You can't trade in and out of it or anything like that. It's just a it's how many are they going to win? So, that's been around for many, many years.

Skye Capazorio: George, just a quick question surrounding design of the app for this initial version of it. Do you envision that all it will have available on it is the what the actual utility is or would you still have certain buttons in place that are not active that has like a coming soon. So if somebody clicked on trades so that somebody has a visual understanding of what is still to come even though can't interface with it and it's not in a demo level but it's almost like a dummy holder of a page that has a coming

George Westbrook: Yeah.

Cody Haugen: Yeah. No, no,

Skye Capazorio: soon.

  
  

### 00:26:45

  

Cody Haugen: we talked about Yeah, we talked about graying stuff out,

George Westbrook: So

Cody Haugen: not making it invisible. Um, and then I think and then yeah,

Skye Capazorio: Yeah.

Cody Haugen: simply add a countdown, George, to IPO day. So, countdown to August, you know, 22nd for college football and September 2nd for

George Westbrook: yeah.

Edwin Johnson: Hey guys,

Cody Haugen: NFL.

Edwin Johnson: we we can do something with this now, Cody, where we could basically say, okay, here's the expected win total um at 12 and a half for say Buffalo Bills and then um I can write something in the next when are we hoping to get the app out?

Troy McDonald Kane: Well, so my we were hoping to get it for Father's Day, but without securing any advertisement, I would advocate we wait in another week after for Fourth of July and see if we can secure some advertising before the end of June. And if we move forward with this challenge because I don't want to drop the app if we change the go to market

Edwin Johnson: Yeah. Yeah, for sure.

  
  

### 00:27:40

  

Edwin Johnson: The um but what we can do with the Buffalo Bills is um or any of these,

Troy McDonald Kane: strategy.

Edwin Johnson: let's say it's 12 and a half wins, you come up with a $62.50 50 cent um onfield expectation and then we could come up with our own um off-field projection for each of these teams and we could have a targeted IPO price so people could start to sink their teeth into how that

Troy McDonald Kane: Yeah,

Edwin Johnson: works.

Troy McDonald Kane: I like that idea.

Kevin Murray: Mhm.

Troy McDonald Kane: And then it's changing constantly,

Cody Haugen: Absolutely.

Kevin Murray: Yeah.

Troy McDonald Kane: right? Because those aren't static,

George Westbrook: Yeah.

Troy McDonald Kane: right? It's changing all the time because then they can go on and see what the changes are and keeps them engaged on the

Edwin Johnson: They're not static. The onfield are not going to waver much.

Troy McDonald Kane: app.

Edwin Johnson: There would have to be a large bet in order to do that. So, this is basically the line in the sand that the casinos put out that

  
  

### 00:28:26

  

Troy McDonald Kane: Even going into preseason when they start playing and they don't

Edwin Johnson: you

Cody Haugen: Yeah, it it doesn't change like Okay, so I'll give you an example though.

Troy McDonald Kane: change

Cody Haugen: If Josh Jacobs, which I don't think happens because the courts move too slow, but he's facing five years in jail for his uh for his like five assault cases that came out in the last month. Uh starting running back for the Packers.

Skye Capazorio: That

Cody Haugen: Um,

Skye Capazorio: is

Cody Haugen: and so if if that happens where he was to miss a sizable part of the season because the appeal process went through or something like that or he goes to jail,

Skye Capazorio: awesome.

Cody Haugen: yes, the Packers uh will probably drop a half or a game. That's as much as it will drop though from the line in the sand that Edwin's talking about that they are true. They won't they won't adjust these like you'll never see more than a game swing.

Edwin Johnson: because the problem is the bookies, okay? If you move it too much, then you can lose both ways.

  
  

### 00:29:15

  

Troy McDonald Kane: Okay.

Edwin Johnson: So, I don't know if you guys read this, but over the over the NBA championship,

Cody Haugen: Exactly.

Edwin Johnson: the Pookies got f***** um because they had people who had bet the Knicks to win and then the odds were X and then they had people the on San Antonio to win the odds were X. They crossed when New York Knicks took over the and and became dominant and the bookies were gonna lose either way. It's it's a unique situation. You read about that, Cody?

Cody Haugen: Yes, I did. Yeah.

Edwin Johnson: Yeah.

Cody Haugen: Well,

Edwin Johnson: So they were they were they were and yeah it was it was most evident on

Cody Haugen: had Oh, sorry. Go.

Edwin Johnson: like Cal sheet. So the market makers were going to lose no matter what happened.

Cody Haugen: And then even ingame because they kept having the Knicks, you know, on such a big spread, people people were taking the Knicks plus six and a half and then they, you know,

Edwin Johnson: Yeah.

Cody Haugen: they came back and from a 29 point deficit and won.

  
  

### 00:30:15

  

Cody Haugen: But like you could take the Knicks and and at certain points in game take the Spurs. Yeah, it was it was a wild series to say the least. I would say a very edge case, but the

Edwin Johnson: Very much an edge case. Normally it's it's you know lock and load.

Cody Haugen: Knicks

Edwin Johnson: It's profitable. But on on the on Kelshi, the the market makers um were definite net net losers. Not on just like flow or anything like that, but like it didn't matter who won. The way that the the market swung uh affected them and they were going to lose either way. Just question

Troy McDonald Kane: Sig lost 10 million according to an article this morning on the 10 million on game four alone.

Edwin Johnson: 10.

Troy McDonald Kane: They lost 10 million on it.

Edwin Johnson: Yeah. Yeah.

Troy McDonald Kane: It was in the in the press this morning.

Edwin Johnson: Okay. Yeah.

Troy McDonald Kane: Yeah.

Edwin Johnson: I had read about this midweek last week that they were basically bucked no matter what.

  
  

### 00:30:56

  

Skye Capazorio: Okay.

Cody Haugen: Yeah.

Edwin Johnson: It was just question how much and I want to say that um uh Jeff uh

Troy McDonald Kane: Yeah.

Edwin Johnson: yes didn't want to disclose how much um at least at that time. So 10 million is huge hit but I don't think that's like that blow for them.

Troy McDonald Kane: No.

Edwin Johnson: That's a that's the other problem with these prediction markets is it's like in order to qualify to be a market maker, you have to have a bunch of money up. A swap dealer is different than a regular person. So there are there are not a lot of companies who can, you know, park a 100red or 200 million uh just for to meet the the the financial requirements to be a designated market maker in those products. Yeah. So you're going to get these cases where they're it's basically you against them and that's never good. So the breath of market participants make the market potentially if it's too thin um very volatile um and then the bid ass can get wide and you know the the actual quality of the product you're trading changes dramatically.

  
  

### 00:32:04

  

Edwin Johnson: You know back in the day like if you looked at our 30-year bond pit there were like 5,000 people standing in there and so the market could absorb a lot of loss or a lot of little guys could lose a little bit. Um, now these big firms that control pretty much all the flow, you know, if there's a massive out trade and they lose a lot of money, you you have systemic risk, you know, one of these firms can blow up. Um, Troy, you remember that one company, uh, who the f*** did they bust all those bond trades for in October? It was like Alustin, right?

Troy McDonald Kane: Alson or Ronin?

Edwin Johnson: Um,

Troy McDonald Kane: One of the two.

Edwin Johnson: not not Ronin. Ronin they took out.

Troy McDonald Kane: And it was Austin.

Edwin Johnson: f***. Yeah,

Troy McDonald Kane: Yeah.

Edwin Johnson: it was Austin. So basically they had a bunch of orders that were resting in the book and um a

Troy McDonald Kane: Yeah.

Edwin Johnson: comp I think it was China or somebody a a country had to get out of some trades and they just started ripping bids off and just blew out this company.

  
  

### 00:32:57

  

Edwin Johnson: Had those trades stood all would have bank been bankrupt which would have caused other companies

George Westbrook: Oops.

Edwin Johnson: to go bankrupt and you would have had this completely problematic situation in the bond market. Um, and you know the the exchange said we're going to bust the trades or make the trades as though they didn't happen which you know if you're on the wrong side of that you you get f***** too because you could get you're hedging against something that happened and they're like no that didn't happen. It was an error and because of that error people lose money. So anyways I don't want to digress the at the end of the day the breath of market participation is really important how how many how many different people taking on risk. Cool. Uh, yeah. So, I would I would definitely say we'd want to have some pricing model that shows the on expected onfield and then the synthetic expected off-field, but without any advertising. I don't even know. I don't even know what we put on there.

  
  

### 00:33:53

  

Edwin Johnson: I I don't even know how to put something on there. I didn't come up with something.

Troy McDonald Kane: I mean, we simulate we're sim well for for the simulation we we said 250 a week is at play for per game. I don't know if we want to try to model some formula or just split it 5050 for the IPOs to make it

Edwin Johnson: Yeah. I mean,

Troy McDonald Kane: simpler.

Edwin Johnson: it's not 50/50 though.

Troy McDonald Kane: Yeah.

Edwin Johnson: Then it looks like manufactured, you know. I'll I don't know. I'll come up with something.

Troy McDonald Kane: Yeah. There's we could do a formula where if they're rated higher in that game, they get 60% or like some model. We can easily come up with something

Edwin Johnson: I think it's let me come up with something. I think it's more about the like demographic and popularity of the team and the likelihood that they're going to trade more than it is the actual team's performance. Right?

George Westbrook: Is it off field performance in perfect world.

  
  

### 00:34:44

  

Edwin Johnson: We want to se separate it.

George Westbrook: What would be the method of calculation for that? Would it would it

Edwin Johnson: Well, yeah, it's total ad spend for the entire league divided by the games and then you put

George Westbrook: spend

Edwin Johnson: a certain amount on each team. So, or each game. So, let's say hypothetically there's a million dollars that's going to be spent per game. Uh there's 270 or yeah, 272 regular season games. So there's a ad spend of 272 million. So each game's worth a million bucks and then the team that actually has the most trades gets that percentage. So we're not going to publish trading volume until the earnings reports. That's that's the key, right? It's like we don't want to show volume until the earnings reports are are are coming out. So if you know Green Bay plays bears um and Green Bay has 80% of the people trading the Green Bay side of it, they get 80% of that million. So you get 800

  
  

### 00:35:50

  

George Westbrook: Okay. All right.

Edwin Johnson: grand

George Westbrook: Um, yeah. Then going back to, so going back to the they call it the pre-release version. So yeah, grade out areas just a matter of defining what we're going to have on those gradeout areas. Is it more just text/ educationbased for lack of a better term? It's like this is what you will be able to do here,

Skye Capazorio: Perfect.

George Westbrook: blah blah blah, maybe a video, something like that. And then obviously the the parts of the application that are going to be available to see. So obviously the sports radar data albeit not with a with live games and then we need to work out where the limit is like do we want them going back to 2013 or do we want it to just be last year's um maybe maybe it's somewhere in the middle where it's last two or three years. Um and then like we said I think it's narrowing down the the data that we want them to see. But obviously that's a lot of that's been recorded on

  
  

### 00:36:44

  

Cody Haugen: The the the problem with going back further, George,

George Westbrook: here.

Cody Haugen: is we have to then we have to match real sports data to real financial data, which we can do. Obviously, we have all the data of what happened. But like going back further in sports data to me has no value if you don't have the pricing data to compare it to. and and and and hypothetically if we do go this route and we do do the pricing data on a per game basis for every single team dating back however far we want to go back people can start

Skye Capazorio: Nobody escaped.

Cody Haugen: building models honestly on it and it is actually extremely valuable so I don't know Edwin maybe we do give that some thought um because then people actually

Skye Capazorio: Wait

Cody Haugen: have a real purpose to come in there and sit for hours before there's any live data because they're building models off of that historical sports data and financial data that we

Skye Capazorio: a second.

Cody Haugen: put behind it and and pair it to I

  
  

### 00:37:43

  

Edwin Johnson: Yeah. Yeah, it's gonna be the the the financial data is going to be synthetic.

Cody Haugen: mean well

Edwin Johnson: It's not going to be real, obviously. So, it's a

Cody Haugen: right but but what's what's real to somebody in a new product anyways it's it's

Edwin Johnson: little

Cody Haugen: whatever you put in front of them that's what's real I I I think

Edwin Johnson: Sure. Okay.

Cody Haugen: I mean I think there is it just obviously is more work on our side going back historically.

Edwin Johnson: Sorry.

Cody Haugen: But that that's the only way I see there's valuable going more than one year, George. So if we decide to do that,

George Westbrook: Okay.

Cody Haugen: maybe more than one year. If we don't, one year is all you

George Westbrook: Yeah. Yeah.

Cody Haugen: need.

George Westbrook: I think obviously in terms of time and complexity as well, like you said, top one year's one year is the easiest and it's the least complex.

Cody Haugen: Yeah.

George Westbrook: So I think at at a well minimum we say one year.

  
  

### 00:38:32

  

George Westbrook: um education as well. Um I think obviously that could be quite valuable. Um but then is it going to be ready? Potentially not. Potentially it could be. It doesn't really matter too much because correct me if I'm wrong here, Brett. We can just do an OTAA push because it's not updating anything anything native. Um so that's fine.

Skye Capazorio: Yeah,

George Westbrook: So education and then correct me if I'm wrong anyone here.

Skye Capazorio: I'm sorry.

George Westbrook: Education discover IPO preview. um KYC and on boarding referrals and then everything

Edwin Johnson: Sounds right.

Cody Haugen: You got

George Westbrook: else grayed out.

Edwin Johnson: Yeah, sounds right to me. Then during the gray out,

Cody Haugen: Yep.

George Westbrook: Um

Edwin Johnson: when do we want to turn the gray out off? Do we want to show the pre-season games live?

Cody Haugen: I I would

George Westbrook: uh I I didn't even think about that to be honest.

Cody Haugen: Yeah.

George Westbrook: that yeah that should be that should be that should be fine.

  
  

### 00:39:30

  

Skye Capazorio: It's

George Westbrook: Um it would but then in in my it wouldn't be grayed out.

Skye Capazorio: meant

George Westbrook: So it would be so if you can imagine that that that discover page if there's not a live game on it's going to look different to how it would be if there were live games on. Um and obviously that's not a manual thing. That's all managed via code. So it would just be right game's coming up or two hours before a game or the day before a game we show the let's call it the live or upcoming game cards when it's live it's the live game. Um, so yeah, preseason games as well. Preseason has that

Edwin Johnson: Then where where will the uh where will the earnings

Cody Haugen: Got that

George Westbrook: started

Edwin Johnson: pages be? In the in the more section, the three dots.

Skye Capazorio: It's

Edwin Johnson: It's going to have its own

George Westbrook: the so to be decided.

Edwin Johnson: page.

George Westbrook: Um, but I think one thing we could potentially maybe we take the trade button and that's currently in more until a user can actively trade and then that is replaced by like an IPO button or actually we just keep the trade button and then the only thing they can see is the

  
  

### 00:40:39

  

Edwin Johnson: Just keep the trade button.

George Westbrook: API.

Edwin Johnson: Yeah,

George Westbrook: Yeah.

Edwin Johnson: just keep the trade button because what what would be awesome is during the let's say you get on the app, you know, the earnings report comes out at, you know, 9:00 a.m. Central hypothetically, say, and you're on your app, you log in and then the earnings reports flash just like any kind of other economic number, but you've got that trade button right there and you can click on it and basically be ready to roll. And and so the moment that it hits, you hit trade, bang, bang, bang, you buy and sell. I mean, that part is going to be absolutely unbelievably fun and exciting to trade, you know, because you don't necessarily have to wait for the earnings report for it to come out. Like, some people speculate on what direction the market will go right before the earnings report and you'll say, "I'm going to buy them because I think the earnings report's going to be great." And then you're actually exiting because the market went your way.

  
  

### 00:41:34

  

Edwin Johnson: I that like even in real trading like the regular markets, the economic numbers are that little extra spice that make you real excited. It's a lot of fun.

George Westbrook: Okay. Yeah. So, keep it keep it on the trade page. Um, but the pages leaderboard. I mean, that's obviously going to

Edwin Johnson: No, George, I would I wouldn't keep the earnings report on it on the trade page.

George Westbrook: be

Edwin Johnson: I would say we want its own like it lives in the more section somewhere like by the education and all the referral bank it's there but I think we send a push notification that says earnings report in 15

George Westbrook: Yeah. And then I think Yeah.

Edwin Johnson: minutes

George Westbrook: a push notification and potentially at the top of the trade page or somewhere in the trade page when it's maybe the day of or the day before or whatever time period it pops up and goes. So, it's not a pop. It's like it's not static, but it's on the page. It's saying earnings reports in 30 minutes or like you said 15 minutes and then they can navigate to it from

  
  

### 00:42:35

  

Edwin Johnson: Yeah.

George Westbrook: the trade page or the homepage or wherever.

Edwin Johnson: Yeah. And they could click and they could click that countdown basically and go right to that

Troy McDonald Kane: Yeah, I think it should. So, I'm playing around with the app right now. I actually think where it should go,

Edwin Johnson: page.

Troy McDonald Kane: Edwin and George,

George Westbrook: Yeah.

Troy McDonald Kane: is under the discover page in addition to because when you click on the team companies, it gives you all the relevant information for that team. That's where the earnings report should sit for that team is on that page under the discover

Edwin Johnson: It's good idea.

Troy McDonald Kane: tab.

Cody Haugen: That's that's what we talked about before on the team page and then also have its own

Edwin Johnson: Great idea.

Troy McDonald Kane: You can trade off those pages,

Cody Haugen: page.

Troy McDonald Kane: but it sits there for the until the next one comes out the following week.

Skye Capazorio: It's

Cody Haugen: Yeah.

Edwin Johnson: Great idea,

Troy McDonald Kane: But to your

  
  

### 00:43:18

  

Edwin Johnson: Troy. If if whoever came up with that,

Troy McDonald Kane: Yeah.

Edwin Johnson: brilliant. Because then you don't have to toggle through different teams, right?

Troy McDonald Kane: Yeah.

Edwin Johnson: You know which which ones you're looking at. Really cool.

George Westbrook: So is that the only way that a user be able to navigate to the earnings report is going to the team which they want to see the earnings report for?

Troy McDonald Kane: I mean, I think so because that's how it works on other stock apps like

Edwin Johnson: I I would say no, George. I would push back.

George Westbrook: Anything?

Edwin Johnson: I would say we should have a earnings report page that that basically is the entire season's worth. So you can see historically how they've done. If you want to go and navigate to the, you know, earnings report page within the the more section, I think that should also be separate. It's another place for us, Troy, where we can brand because one thing that really stood out, Kevin was really uh, you know, slick.

  
  

### 00:44:11

  

Edwin Johnson: He basically took out the SoFi ad on that trade confirmation page, mocked up the pay.com, and the guy's eyes lit up when he saw it. It was really good.

Troy McDonald Kane: Yeah. So, looking at the discover page, like I'm on the Green Bay Packers one right now. You could have a a box for that week's earnings report. If you click on it, then it takes you to the other tab or the more tab that gives you a rundown of all the earnings reports for that team company in the season. And then people can just go to that tab to Edwin's point and just if they just want to research earnings reports and not look at the individual team.

George Westbrook: Yeah. Yeah. No. No. Yeah. I think Yeah. Cuz I didn't know if that was the only way,

Troy McDonald Kane: Yeah.

George Westbrook: but I think definitely by having both.

Troy McDonald Kane: Yeah. Yeah.

George Westbrook: Um Okay.

Troy McDonald Kane: Makes sense to have both.

  
  

### 00:45:07

  

George Westbrook: Okay.

Troy McDonald Kane: Yeah.

George Westbrook: Perfect.

Edwin Johnson: I mean, every time I look at this freaking app,

George Westbrook: Um

Edwin Johnson: it's just so good.

Troy McDonald Kane: I know.

Edwin Johnson: It's so good,

Troy McDonald Kane: Like,

George Westbrook: And it's only going to get

Edwin Johnson: man.

Troy McDonald Kane: well, when T when you guys are done with your integration into tZERO,

George Westbrook: better.

Troy McDonald Kane: we should do like a group simulated event on something where we can play around with it and kind of kick the tires and stress test it a little bit.

Edwin Johnson: I'll put up some cash so the you know we can do an internal uh where and you get a little bit of money. It' be fun. It's never fun without the money. You always got to have the money.

George Westbrook: I might put in I might put in a little version for me so that when I place a trade it just gives me 10 times the amount of money apart from a loss where it's 10% of

Skye Capazorio: That's

George Westbrook: it.

  
  

### 00:45:57

  

Edwin Johnson: When that goes through audit, George, not only when I find that out, not only will I shave your face, I'm going to shave that beautiful hair.

Skye Capazorio: stupid.

Edwin Johnson: Then

George Westbrook: I've done that once before and that's now it's making me even more scared.

Edwin Johnson: I'd also include the eyebrows just to make it a full full

George Westbrook: I have also done that before as

Edwin Johnson: on

Max Kingaby: If it makes you feel any better,

George Westbrook: well.

Max Kingaby: George, it can't get any worse.

Edwin Johnson: Oh man.

George Westbrook: Oh,

Edwin Johnson: Spoken from the pretty boy.

George Westbrook: definitely definitely getting that office BB gun.

Edwin Johnson: That's right. Awesome. All right.

George Westbrook: Right. I think I think that's I think that's all all we need.

Edwin Johnson: Cool.

George Westbrook: Um

Max Kingaby: Yeah.

Edwin Johnson: We got Brett with a finger up.

George Westbrook: Yeah.

Edwin Johnson: I don't know if that's a question or a statement.

Skye Capazorio: That's

Brett StClair: It's both. So, how do I do a statement and a question in one?

  
  

### 00:46:47

  

Edwin Johnson: Yes.

Brett StClair: Max, would you like to demonstrate your demo for the guys?

Skye Capazorio: okay.

Brett StClair: I think that's a statement and a

Max Kingaby: Yes.

Brett StClair: question.

Edwin Johnson: That was a question.

Brett StClair: Yeah.

Edwin Johnson: Would you like I mean that's that's a question.

Brett StClair: would you like?

Max Kingaby: Yeah.

Brett StClair: And then I have to phrase it as a statement. Please demo

Cody Haugen: Yeah.

Edwin Johnson: Well, when I was in Florida,

Max Kingaby: Um

Edwin Johnson: all these guys were calling me daddy,

Brett StClair: it.

Edwin Johnson: which was, oddly enough, very satisfying and erotic. Uh, which I enjoyed.

Cody Haugen: Daddy

Troy McDonald Kane: I can't I can't I'm

Edwin Johnson: You can't,

Max Kingaby: This

Edwin Johnson: Troy.

Cody Haugen: Warbucks.

Edwin Johnson: You can I mean,

Troy McDonald Kane: sorry.

Edwin Johnson: at one point,

Brett StClair: Since after we

Max Kingaby: is

Edwin Johnson: Kevin handed me a can a and I just started walking around. I looked like a little husky pimp from Chicago.

Brett StClair: So, so in South Africa all the youngsters call anyone older uncle and if you really are

  
  

### 00:47:40

  

Max Kingaby: good. And if you really

Brett StClair: respected you're called opp.

Max Kingaby: So

Brett StClair: So like which is

Skye Capazorio: OPA which means grandpa and

Brett StClair: grandad.

Edwin Johnson: Oh, good to know.

Max Kingaby: when

Skye Capazorio: Africans.

Edwin Johnson: Well, my brother uh has a grandson. When I probably 15 years ago, um I hadn't met this guy and he was a little guy and uh someone had a dog. I picked up the dog and this little kid goes, "Who's the grandpa with the dog?" And I was like, "Who's the retarded kid?" And it didn't go over well.

George Westbrook: You've heard that a few times, haven't you, Max?

Edwin Johnson: Love it.

Brett StClair: Shouldn't

Edwin Johnson: This is good stuff.

Max Kingaby: Yeah,

Edwin Johnson: If I wasn't fraught with peril,

Max Kingaby: that

Edwin Johnson: I would really be enjoying this conversation.

Max Kingaby: Um, let's try and make this a bit fun and a bit interactive. So, would one person, one in play person like to come up with a random company that's not in play.

  
  

### 00:48:47

  

Max Kingaby: It has to exist.

Edwin Johnson: an actual stock

Max Kingaby: Any company you can think of brand.

Edwin Johnson: company.

Max Kingaby: Yeah, preferably with a strong brand. So, for example, I did Malt teasers earlier.

Cody Haugen: Pepsi.

Max Kingaby: I hope so.

Edwin Johnson: Ah Yeah.

Skye Capazorio: Celsius.

Edwin Johnson: Celsius,

Cody Haugen: I I need a Pepsi.

Troy McDonald Kane: Rose.

Edwin Johnson: please.

Cody Haugen: I'm bone dry over

Edwin Johnson: Bry.

Cody Haugen: here.

Edwin Johnson: That's

Max Kingaby: So, Celsius, is that spelled like that? I

Cody Haugen: Yeah.

Edwin Johnson: rough.

Max Kingaby: think

Cody Haugen: Yes.

Skye Capazorio: Yeah.

Cody Haugen: Just Yeah. Just like the Yep. You got to go Celsius energy drink probably.

Max Kingaby: uh yeah,

Cody Haugen: Yep. Right

Max Kingaby: awesome. Okay. So,

Cody Haugen: there.

Skye Capazorio: Awesome.

Max Kingaby: last week I think it was Kevin needed George to add Play, was it Play.com as one of the advertising banners?

Edwin Johnson: Hey.

Cody Haugen: Hey

Max Kingaby: Um,

Kevin Murray: Yeah.

Max Kingaby: and obviously it was 3:30 our time,

  
  

### 00:49:39

  

Edwin Johnson: Yeah.

Max Kingaby: so George wasn't awake. But we have come up with a solution to get you to help

Edwin Johnson: What you do?

Max Kingaby: you guys with selling that includes the brand of the company you're working with. And just for any other brand who clicks on your website who wants to have a go, what what you do is for Celsius. So let's call this one Celsius. You save an image that represents the brand and then you take the brand's URL and then within what will be the website on the advertising page which Sky I know we haven't got on to yet but this was the idea behind it.

Skye Capazorio: There

Max Kingaby: You have this screen where you click here to advertise.

Skye Capazorio: is

Max Kingaby: You paste in your brand's URL, but that's optional because like some brands may not have a website, but we're hoping all the brands you guys are working with do. Copy the image. Generate banner.

Brett StClair: This is when you hope it works.

Max Kingaby: Yeah, I know.

Brett StClair: Yeah.

  
  

### 00:50:59

  

Max Kingaby: Fingers are crossed on the fingers on the mouse are really crossed right now.

Edwin Johnson: You know what always helps me, Max? When I go fingers crossed, toes crossed, legs open. and tend to be Oh,

Max Kingaby: And then you can envision what your brand will look like on the actual inplay app. Then you have the

Cody Haugen: Oh, that's that's sweet. Um,

Skye Capazorio: It's

Edwin Johnson: looking

Max Kingaby: option.

Kevin Murray: Yeah,

Cody Haugen: AI AI also uh put together its own little flavor because those the fruit

Kevin Murray: that's really good.

Edwin Johnson: awesome.

Troy McDonald Kane: Oh my gosh.

Cody Haugen: weren't wasn't in the original

Max Kingaby: Yeah, that's all within the prompt.

Skye Capazorio: okay.

Cody Haugen: picture.

Max Kingaby: It's kind of meant to make it come to life a bit more and fit the screen a bit better.

Cody Haugen: That's

Max Kingaby: Then you have the option to to download or if you're interested and want to talk to you

Cody Haugen: sweet.

Max Kingaby: guys, they say their name, company, and email address and then it sends it on to your sales team.

  
  

### 00:51:54

  

George Westbrook: I think one of the things you mentioned to me earlier as well,

Troy McDonald Kane: Yeah.

George Westbrook: Max, was that like imagine there's 10 different ad Sorry,

Max Kingaby: Imagine 10

George Westbrook: I'm just going to mute you, Max. Um, imagine there's like 10 different ad units that they can select across the whole application as well. page, maybe on the education, maybe on the chat. So then they can start to see what it would look like in in their world um on spec different areas of the application as

Edwin Johnson: I have a question for you, Georgie. Boy,

George Westbrook: well.

Edwin Johnson: on the home screen when we log in, the one thing that's not evident anywhere in the app is the title sponsor. There's other than I think on the first page might be like brought to you by Home Depot and very very small. Um and again this is for the group. It's a question not a request not a not a breath statement question. It's a real question. Um, do we see any value in the moment you log in that for, you know, 3 seconds or two seconds that screen is specifically the title sponsor that says, you know, welcome to the inplay trading challenge brought to you by Celsius and it dissolves and then you're right into the action.

  
  

### 00:53:14

  

Cody Haugen: Yeah,

Skye Capazorio: so splash screen

George Westbrook: Yeah.

Cody Haugen: I think yeah, I think this comes into a larger question to the Novo guys is and I haven't

Skye Capazorio: takeover.

Cody Haugen: really pushed on it because one, we've all been busier with other more important s***, but that's in our app feedback. George, that's been there for four weeks now. So, larger question to that point, yes, I agree with Edwin. We should have that for the title sponsor and what they would be paying, but when is that app feedback from that initial release going to be worked on and included into the app? There is probably 20 or so items.

George Westbrook: Yeah. Yeah. with this week because what we where is so where is initially it's with

Cody Haugen: Okay.

George Westbrook: the specifically with applications getting from let's call it 0 to 60 um not easy but um whereas the last few weeks it's pretty much

Cody Haugen: Yep.

George Westbrook: been websites is the front end stuff and then all the back end

Cody Haugen: Yeah.

George Westbrook: um so like say for example fix gateway up and running sports radar up and running um all the message buses things like that persona cuz it

  
  

### 00:54:20

  

Edwin Johnson: Yep.

Cody Haugen: Persona want this to be in Yeah.

Edwin Johnson: We know George here.

George Westbrook: was

Edwin Johnson: We know there's work on it.

Cody Haugen: Yeah.

Edwin Johnson: It's more of a question,

Cody Haugen: It it wasn't it wasn't Yeah,

George Westbrook: Yeah.

Edwin Johnson: not

Cody Haugen: it wasn't accusatory at all, George.

Edwin Johnson: complaint.

Cody Haugen: I know. And like we we threw the website and we were like,

George Westbrook: Yeah. Yeah.

Cody Haugen: "Get the website up in 24 hours, you know, like we need it."

George Westbrook: Yeah.

Edwin Johnson: I'm gonna tell you like as as little progress as we've made

Cody Haugen: So,

Skye Capazorio: Sorry.

Edwin Johnson: with advertising, we would have made less without the tools that we have because once people see

Cody Haugen: exactly. Exactly.

Edwin Johnson: the app, the app is incredible. I mean, it really is impacting. Okay. Um,

George Westbrook: Yeah.

Edwin Johnson: you know, the website's up, uh, also looks, you know, professional now. It's it doesn't look, you know, rinky dink. So you know all these things you know obviously take time.

  
  

### 00:55:08

  

Edwin Johnson: So there no no no no complaints whatsoever.

George Westbrook: Yeah. No. Yeah. it it was it was more in ter just in like what where where where we're thinking in terms of like the the phases of work. So it's like what this why obviously we wanted this conversation on Monday was this this is like the pre-launch app is I mean that needs to be done yesterday.

Skye Capazorio: Thank

George Westbrook: Um so it's get that get that sorted get that going and then if you imagine we got like

Skye Capazorio: you.

George Westbrook: another branch of work which is like the the production the production app um making sure that

Skye Capazorio: All

George Westbrook: we can go in and like when we want to do a simulation we we can do it um but now obviously that's starting to like say persona that's that bas a lot of the things are are close to completion not let's not say the word done um it's now it's flipping back into refinement mode for for for the application because I think there was more holistic changes we were making around like look and feel and then now like that's where these these little refinements are so so so important like like you

  
  

### 00:56:01

  

Cody Haugen: Yeah.

Skye Capazorio: right.

George Westbrook: said that splash page is it we need we need to definitely add that

Edwin Johnson: Yeah, by the way, Max, brilliant work on that.

George Westbrook: in

Edwin Johnson: I mean, that's incredible because like going into a meeting, being able to like, you know, upload an a website and a logo or whatever and be able to change it on the fly. Um, you know, because like for example, I reached out to the Wind Trust Bank. I haven't heard s*** back from that brick. Um, by the way, it was a an old f***. Oh, god. Disgusting. Um, anyways, you know, because they have multiple business lines, you know, uh, they would be great to be able to say, we hey, you know, here's your spot, but like you got 15 brands, buy one spot, integrate your 15 brands. I've been going back and forth with um, a guy from NextStar TV over the weekend. Um they're the largest TV in uh owner in in the US. Uh you know uh c like they own the CW and all these different TV stations and radio stations and they represent a s*** ton of brands.

  
  

### 00:57:08

  

Edwin Johnson: So, I'm hoping to get a presentation with him, uh, you know, today or tomorrow. Um, you know, but something like that, being able to like swap in all the different things that they have, it would be amazing, you know, for for for the first impression to see your different brands definitely elevates how they they envision people reacting with it. Like it the pay.com thing Kevin did was was awesome. So, Max taking upon whoever was responsible for that, the entire team, brilliant and thank you. so much. It's It's, you know, gives us a fighting chance

Cody Haugen: Yeah, I mean I think there's there's two pieces of value, right? It's we can do it for whatever conversation before the client even knows about it.

Edwin Johnson: anyway.

Cody Haugen: But Kevin, I was just thinking I think if we include that link in any of our brand uh outreach in the, you know, once we get the the email sorted out so we're not blasting domains. But um when we do that that large outreach again to the brands,

  
  

### 00:58:01

  

Skye Capazorio: Excuse

Cody Haugen: um including that link to say come in, you know, play around with our demo and show how your brand looks in in our in our demo

Edwin Johnson: Here's

Cody Haugen: site.

Kevin Murray: Yeah.

Cody Haugen: um allow them to, you know, kind of teach them how to fish and get them excited about playing around with something.

Skye Capazorio: me.

Cody Haugen: Yeah, I think it's I think that's a cool cool use case as

Kevin Murray: Yep.

Edwin Johnson: one other item I wanted to bring up. We haven't touched on this,

Cody Haugen: well.

Edwin Johnson: I don't think, yet, but I think it's going to be relevant to how we try to sell. So basically I think we need to profer what the KPIs are going to be for the advertiser user experience what we're actually going to track how they're going to be able to see it when we're going to release the information and if we don't get anybody how we're going to use that data to then you know put into a sales kit to say here's what we we had I don't know what we want to track totally above my pay afraid.

  
  

### 00:59:04

  

Edwin Johnson: I have no f******

Cody Haugen: Well,

Brett StClair: Yeah, I got

Cody Haugen: I think we have I think we have a good idea from the conversations of feedback

Edwin Johnson: clue.

Brett StClair: it.

Cody Haugen: from Sky and Brett, but I think it's also like the minutes per section that

Skye Capazorio: Okay.

Cody Haugen: you're sponsoring or selling, right? You want to know exactly what page they were living on and for how long. So that we could say that homepage actually might be worth a min of six and an upwards

Skye Capazorio: Okay.

Cody Haugen: of 12, whereas we think the I'm just saying something. The live match tracker is extreme value, but once we get these numbers, we actually see the live match tracker is probably a min of two or two and a half and it's a max of six.

Edwin Johnson: Yeah.

Cody Haugen: So I I think it's the the packages we want to sell and then I'll open this to Sky and Brett,

Edwin Johnson: Yeah.

Cody Haugen: but like I think it's what we want to sell and and what is that interaction with?

  
  

### 00:59:58

  

Edwin Johnson: Right.

Cody Haugen: So we have Okay,

Edwin Johnson: But here here's the problem.

Cody Haugen: go ahead.

Edwin Johnson: The problem that the feedback some of the feedback we got last week was that we may be touting minutes, but they're the they want impressions. They don't give a f*** about your minutes. They only care about impressions and how they're it fits in their their existing buyer kit. So,

Skye Capazorio: I think

Edwin Johnson: if we're going to come come to them and say,

Brett StClair: There we

Edwin Johnson: "Oh, yeah. Well, someone's trying to buy a car." We're like,

Skye Capazorio: this

Brett StClair: go.

Edwin Johnson: "No, you need an RV." Like, I'm buying a car, even if the RV is better, right? Or whatever.

Skye Capazorio: I think um Edwin ex there is thanks Kevin.

Kevin Murray: Sorry, I got to jump.

Skye Capazorio: uh that comes back to the two pages that I shared with you a few weeks back. Um I'll I can resend them to you that shows the benchmarking of the different things.

  
  

### 01:00:48

  

Skye Capazorio: So the um impressions etc etc. Um but then also what would need to be served from an impressions perspective and how that then backwards chains into what the CPM is and the cost break. We also spoke about this um and adjusting that numbers.

Edwin Johnson: I want but I I hear you, but I want it from an agency.

Skye Capazorio: Sure.

Edwin Johnson: I want it from a buyer. I don't want it from our end because like what we think we they want might not be what they

Skye Capazorio: That sure. So that that was filled that was filled in backwardly from the from the

Edwin Johnson: want.

Skye Capazorio: information that we had from Wayne and from um WPP from Rich um went into that. I was just putting it into a deck that was just easier or a page that was easier to understand on how that flow

Edwin Johnson: I hear you.

Skye Capazorio: worked

Edwin Johnson: Do we put a lot of weight in what Wayne and this other buck said though at this point? Are they the Are we

  
  

### 01:01:44

  

Skye Capazorio: in in terms of the the measurable me the metrics that the industry measures on.

Edwin Johnson: gonna

Skye Capazorio: Yes, I would say that um because that is that is a standardized requirement that they would then be offering to other clients of theirs that

Brett StClair: Thank you want the bet benchmark and how are we going to perform better?

Skye Capazorio: purchase

Brett StClair: That's the goal. We want to show how we're better on every single metric. And so they've given us those metrics. Um and now we need to make sure that whether we prove it with house ads, whether we prove it with an actual C advertiser, that's what these guys are looking for. The ultimate metric is cost per acquisition. That's what they will boil. Whatever metric we're offering, they're going to boil it down to that

Edwin Johnson: Okay.

Brett StClair: number.

Edwin Johnson: Okay. Are we comfortable? I mean, I I'll be I'm not comfortable, but if you guys are comfortable with th those two gentlemen's ideas, I mean, you know,

Brett StClair: It's industry standard.

  
  

### 01:02:44

  

Edwin Johnson: I'm not sure that we've gotten great information from them so far.

Brett StClair: So, it's Yeah,

Edwin Johnson: That's all.

Brett StClair: it's pretty much industry standard. It's like a currency um that all these guys work towards. It's called IAP. Um, it determines ad formats, measurable kind of outcomes and currency. And then there's metrics that you hit for each particular kind

Edwin Johnson: But I I hear that for a digital campaign for like f******

Brett StClair: of

Edwin Johnson: Google or something, but how's that play when you're looking at stadium signage at an NFL game? Like, how's that even possible?

Brett StClair: a whole another set of metrics for stadium signage,

Skye Capazorio: Okay.

Brett StClair: for billboards, uh for TV viewing rights, broadcasting, and everything. It's the currency that they'll operate in.

Skye Capazorio: Broadcast.

Edwin Johnson: Okay.

George Westbrook: I think one of the good things after that call we had with Keville was the fact that there's loads of

Brett StClair: One of the would like

George Westbrook: flexibility with the Keville platform. So whatever we want to build it as, whatever we want to track, how and then also we can build on top of their APIs to provide this information to either current or prospective clients as well.

  
  

### 01:03:54

  

George Westbrook: Um and then we had some ideas for interning tooling as well, but that's a that's another conversation,

Edwin Johnson: Okay, cool. Awesome.

George Westbrook: right? I think

Edwin Johnson: Anything else for me today?

Brett StClair: calendars have all been shuffled. Thanks, Troy.

Skye Capazorio: almost finished.

Edwin Johnson: Awesome.

Brett StClair: I've changed all the dates to accommodate the bank holidays.

Troy McDonald Kane: Great. Thank you.

Edwin Johnson: Does anybody need me for anything else? No. All right, I'm going to bolt. I'll see you fools later.

George Westbrook: Right.

Troy McDonald Kane: All right.

Edwin Johnson: Good luck.

George Westbrook: Let's f****** go.

Edwin Johnson: Thank you,

Troy McDonald Kane: There we go.

Edwin Johnson: George. I need it.

Troy McDonald Kane: There we go.

George Westbrook: Let's f******

Cody Haugen: That's

Edwin Johnson: Say a prayer for me,

George Westbrook: go.

Troy McDonald Kane: All right.

Edwin Johnson: please. I'm I'm doomed.

Skye Capazorio: Thanks.

Cody Haugen: all right. Talk

George Westbrook: Pressure makes diamonds.

Cody Haugen: soon.

George Westbrook: Pressure makes diamonds. Speak to you soon. Have a good one. Oh, wait.

Brett StClair: Wait,

Cody Haugen: All right.

George Westbrook: We It's been a bit

Brett StClair: what's guys?

Cody Haugen: All right.

Skye Capazorio: Thanks.

Cody Haugen: I believe.

Skye Capazorio: Bye.

Brett StClair: Yeah. Bye.

  
  

### Transcription ended after 01:04:58

  

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.

**