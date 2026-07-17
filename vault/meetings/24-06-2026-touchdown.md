---
date: 2026-06-24
type: standup
status: extracted
extracted-to:
  - "[[digests/touchdowns-18-29-jun-2026]]"
  - "[[referral/referral]]"
  - "[[challenge-website/challenge-website]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[trading/trading]]"
  - "[[architecture/open-questions]]"
---

## Post-Call Analysis

> Standup. Processed in the **[[digests/touchdowns-18-29-jun-2026|18–29 June touchdown sweep]]**.

| Finding | Destination | Action |
|---------|-------------|--------|
| **Prize model → participation-gated payouts** (Sat/Sun dailies + Tue weekly ~$25k/day; ~3 criteria; referrals NOT a hard gate; referral leaderboard + separate prize; multiplier/badging) | [[referral/referral]] + [[architecture/open-questions]] | Changelog row + open-question flagged |
| **Referral program LIVE via challenge website + KYC** (launch ~July 4; 600 signups emailed) | [[referral/referral]], [[challenge-website/challenge-website]], [[customer-onboarding/customer-onboarding]] | Noted |
| App-store status (Apple moving / $99 fee; Android Play verification stuck — owner access) | [[customer-onboarding/customer-onboarding]] | Update block |
| T0 daily buying-power file (referral→trading moves; no intraday rebalance) | [[trading/trading]] | Update block |
| B2B/B2C email infra (3 mailboxes/domain, redirects, warm-up) + interns (60-70 on-campus) + social revamp | [[components/components]] (Push/CRM) | Note added |
| Impression-forecast calculator due next touchdown | [[components/components]] (Advertising) | Status |
| Payments (Mastercard/Anna, Goldman, pay.com dead) | — | Parked — commercial |

**

Jun 24, 2026

## InPlay Digital TouchDown - Transcript

### 00:00:06

  

Brett StClair: two minutes.

Cody Haugen: Good morning folks.

Brett StClair: Everybody gives me a double chin when I sit you over here like

George Westbrook: Hello.

Cody Haugen: Hello.

Max Kingaby: Not just Yeah,

George Westbrook: Not just there,

Brett StClair: this.

Max Kingaby: not just a chat.

George Westbrook: Brett.

Brett StClair: And I can't even grow a beard to cover it. Like I have like toughs of hair here. A little bit there. A long piece out of my mole. It's

George Westbrook: When I get a haircut next time,

Brett StClair: beautiful.

George Westbrook: I'll tell him to put it in a bag so he can stick it stick it there.

Brett StClair: I don't want your hair. I want a sunset.

Cody Haugen: Yeah, there you

Brett StClair: Then I'm going to look like I've got kickass beer.

Cody Haugen: go.

Brett StClair: Morning. Morning. Hello.

Cody Haugen: Yeah,

Brett StClair: How's it going?

Cody Haugen: I'm muted, sir.

Troy McDonald Kane: Yeah.

Cody Haugen: Edwin.

Edwin Johnson: very nice to see you all today.

Brett StClair: It is 35 degrees here in London, gentlemen.

  
  

### 00:01:11

  

Edwin Johnson: I heard it's quite lonely.

Brett StClair: It is like walking through a furnace because

Troy McDonald Kane: Wow.

Edwin Johnson: So,

Brett StClair: it's

Edwin Johnson: I know I'm not a weatherman, but the hell that I'm going through,

Brett StClair: horrendous.

Edwin Johnson: I'm sending your way.

George Westbrook: Is that what the thunderstorms were the other

Brett StClair: Earth.

Edwin Johnson: Yes, I had a thunderstorm yesterday during the day on our team

George Westbrook: night?

Edwin Johnson: meetings.

Brett StClair: Did you? Was it a hot hot

Edwin Johnson: I did it.

Cody Haugen: Thanks.

Edwin Johnson: It's very frustrating.

Brett StClair: one?

Edwin Johnson: I um Yeah. Yeah. I've been I I think I slept about 45 minutes last night trying to figure out a way out of this uh conundrum we're in, which is, you know, obviously with the advertising not being there, there's no support. You know, what what am I really going to do here? Because,

Brett StClair: Where's your head

Edwin Johnson: you know,

Brett StClair: landing?

Edwin Johnson: uh it's tricky. It's tricky, you know, because, you know, one thing I've I've, you know, haven't done is, you know, if I had said spent the last four and a half years trading, I probably probably would have made around $50 million trading because these markets are very good for me and my style.

  
  

### 00:02:28

  

Edwin Johnson: So, um, yeah, I mean, it's, uh, definitely, uh, you know, a big bet on this company and wanted to make it work. I mean, the team and I spoke about like, you know, maybe we're going to start trading, you know, I'll start trading a little bit here because with uh, with our darling Mr. Trump in office, he makes for very good predictable trading. Um, yes,

Brett StClair: That's Yeah.

Edwin Johnson: in particular for this the the style of trade that I've employed since I began. uh you know being able to make uh some money. Um, you know, the question is with this this competition like how's it how does it make sense for for inplay you know because you know realistically so I think we we have a disconnect um and I when I say we I'm going to include myself and Cody and I would say even to a limited degree I'd put Troy on my side maybe not as deep because Troy is not a degenerate at least in the trading and gambling side.

Kevin Murray: Right.

Edwin Johnson: I've seen him otherwise.

  
  

### 00:03:35

  

Edwin Johnson: He's pretty good. Um, and then Kevin, are you a gambler, Kev? You Yeah, you're the high limit guy. I forgot.

Kevin Murray: High limits in and out though.

Edwin Johnson: Yeah.

Kevin Murray: Once I make my money, I'm out.

Edwin Johnson: Yes.

Kevin Murray: Gone like a

Edwin Johnson: Um,

Kevin Murray: sniper.

Edwin Johnson: I I think where we where we land is think for for Kevin or for myself and Cody, we're still struggling where people don't see that a lot of the carpets already been worn for us. Meaning, it's hard it's hard not to be able to say there's going to be interest in trading this product when you look at the growth of gambling here. And then you say well you look at the growth of prediction markets here in particular on sports okay because the reason the calcium and poly market are valued high is not because they you can trade on an election or whether or not you know someone's you know some other b*******. It's all based on the sports. You know 90% of all their volume is on sports.

  
  

### 00:04:33

  

Edwin Johnson: The headline they get headlines for like you know will this happen or otherwise but all all their real volume's in sports. And so, you know, when when we say, "Okay, well, how are you going to get users and and you don't have any users yet?" And I'm like, "Well, it's not football season yet." And um I I I don't I I struggled with the disconnect of saying like, "Hey, here's what we have. Here's when we're going to offer it." And you know, I think I sent on the call yesterday. I might have to the to the guy that we spoke to. Um John, um by the way, side note, not impressed with John. I I wasn't really He didn't wow me. Um nice enough guy, but he didn't blow me away. Um but I, you know, I because he he knows people who gamble or whatever, and he's like, "Oh, there's a lot of everyone's gambling." He said, you know, if you remember his quote, I said, "Well, what if you remove the one like friction item that stops most people from gambling, which is risking their own money?" And,

  
  

### 00:05:32

  

Edwin Johnson: you know, then then he's like, "Oh, well, that yeah, that could be, you know, different, right?" So it's like when I when I take the g the gambling angle, the trading angle, the sports angle, meaning like football here, again, I know you guys are from UK and South Africa and whatnot, but football is pretty big here, you know, and then you say, uh, by the way,

Brett StClair: What?

Edwin Johnson: you can do this for free and you have a chance to actually earn money. When people are like, well, you've got to build your audience. I'm like, are you f****** stupid or what? Like I mean how like how how do you not see like it it's people becoming aware, right? So I can see like hey how are you going to make people know but if if you're saying like um well there's not going to be an audience for this and I'm not saying anyone on this call individually. I'm just saying as an aggregate what I'm struggling to to to again reconcile with is like are you kidding me?

  
  

### 00:06:27

  

Edwin Johnson: Like how do you not see this? H how is it not like hitting you in the face like holy s***? you know, we we may have millions of people who sign up here provided that they know about it, right? And then, you

George Westbrook: a quick when cuz I was I obviously wasn't on that When he was when he was

Edwin Johnson: know,

George Westbrook: saying you haven't got an audience, was he referring to the fact that those people aren't there or that they're not within

Edwin Johnson: he didn't

George Westbrook: the play

Edwin Johnson: um I he didn't come out and say that specifically,

George Westbrook: ecosystem?

Edwin Johnson: George. I mean, I think there's always a healthy um like this is b******* that most people have whenever they have a conversation. Um, you know, you could tell he wasn't like a tremendous gambler or trader because when we showed the app, he didn't gau like I mean Troy said like last weekend when he's showing people at barbecues the app like if you've gambled or traded, you look at this app that's been created and you're like,

  
  

### 00:07:20

  

George Westbrook: H.

Brett StClair: Yeah.

Edwin Johnson: "Holy f***." I mean, I can see myself on this thing. And maybe not just for the training,

George Westbrook: Hm.

Edwin Johnson: you know, not just for the training, maybe it's for the for the the the sports data and for the the chat and and more from like you can get consumer sentiment from the s chat like, you know,

Brett StClair: Cool.

Edwin Johnson: I mean, you can you can see, oh, where the markets is and market maybe um in opinion wise and if it's too bloated, you might be able to fade it or something. But like one thing that over the last five years I've been thinking about, it's like, oh f***, man. It's like I told people five years ago that people were going to want to trade sports and everyone looked at me like I was insane. No one believed me. And then the Cali and Poly market came out and now everyone's like, "Holy s***, you can trade sports." It's like you can trade s***. Um I mean it's it's a terrible trade.

  
  

### 00:08:11

  

Edwin Johnson: So, I'm I'm still still of the ilk of like, you know, even with our 600ish signups or 500 signups that we have from the from the trading challenge, you know, if half of those people refer 50 people, you know, we're looking at 13 to 14,000 potential signups, right? And then once people get paid, then those signups really start to blossom. So, you know, where my head's landing at, Brett, I think I'm an idiot. Um, I'm very uh humiliated and and a little bit um disappointed in myself that I haven't been more keen on where we're at truly at with the potential ad revenue because that was, you know, I should have definitely had my eye on the ball. I mean, at the end of the day, all failures fall on me. They don't fall on any individual um but me. and it's very very frustrating. Um so, uh you know, where are we at today? Where's my head at? The best thing I could come up with overnight was this. Um you know, we still move forward with the challenge.

  
  

### 00:09:20

  

Edwin Johnson: We still move forward with the $25 million up to, but we had a we had a line. And that lines based on the number of competitors. Okay? And that would also be the number of competitors for the overall season and and for the dailies. Okay? So, for example, you know, if we get um you know, and the way that I looked at this too is, you know, part of part of it is like a customer acquisition cost, right? So, like if we got our $25 million payout and we somehow cobble that together and then we're going to distribute it um and we end up getting 500,000 users, who wouldn't pay 50 bucks for a customer acquisition into a trading environment like that? You know,

Brett StClair: Excellent.

Edwin Johnson: Interactive Brokers is paying like 225, right? And if we can get that partly offset by advertisers, fantastic, right? If if it's fully offset, amazing. But if it's partially offset, pretty good.

George Westbrook: What the

Edwin Johnson: So you Yeah.

George Westbrook: f***?

  
  

### 00:10:30

  

Edwin Johnson: I mean, my my thoughts are we have to like get a little bit creative in terms of how we're going to do the distribution. The other thing that I thought about was maybe and again I I don't have this I don't have an answer yet but maybe um we use the daily participation uh for the first month. We don't do any cash payouts the first month uh for dailies and we use those as qualifiers for the monthlong pool. So you have to you have to trade at least you know four days a week or three days a week.

Brett StClair: like prove yourself do your education

Edwin Johnson: You got to be on the Bingo.

Brett StClair: study if I can get there you got to qualify for this fact that's

Edwin Johnson: You qualify for it. Okay. And then if you qualify for it, maybe the first month, you know, we give out like not just one,

Brett StClair: Nice.

Edwin Johnson: but if we do that, then we can b basically get some runway that we could go back to brands with and maybe squeeze them a bit and say, "Hey, look at our traction. Here's how many people signed up.

  
  

### 00:11:32

  

Edwin Johnson: Here's how many people engaged. here's how long they engage for, what's it worth to do it for the next three months to you? And this is only going to grow right after we do the prize distribution. And maybe we can push those signups that way, right? So maybe no initial payments and then maybe for the first month um there's not just one winner. May maybe we we count it as you know learn you know learn how to trade markets in the first month instead of one trader getting like you know a 100red grand maybe we have five traders get a 100red grand and so now we're now now it becomes a little bit more doable and then we figure out just a different prize schedule for that month and we try to keep it under you know under a million bucks and then try to go from

Brett StClair: Start slower but make it look officially bigger,

George Westbrook: Hey,

Edwin Johnson: there,

Brett StClair: more exciting. People can track a map and go. It's a real thing, but you've got protection.

  
  

### 00:12:32

  

Edwin Johnson: right?

Brett StClair: So, if people don't qualify, then you're keeping it down. You're de-risking.

Cody Haugen: And yeah,

Edwin Johnson: Yeah.

Brett StClair: You actually the risk into the model.

Cody Haugen: I absolutely love that.

Brett StClair: f***. I like that.

George Westbrook: Hey, the

Edwin Johnson: So one one last thing I would add and then to qualify you'd have to trade

Cody Haugen: That's

George Westbrook: one

Edwin Johnson: at least like say you know you'd have to be logged in for at least you know 30 or 45 minutes a days that you're logged in three times a week you'd have to make and execute at least you know five trades and you'd also in that month have to refer at least 50 people That's my

Brett StClair: There we go.

Edwin Johnson: That's

Brett StClair: This is the kind of pivoting.

Edwin Johnson: what

Brett StClair: That's This is it. This is it. I like that.

Edwin Johnson: George, what were you gonna

Brett StClair: You forcing

Edwin Johnson: say?

George Westbrook: It was about the the first month potentially not doing payouts

  
  

### 00:13:20

  

Brett StClair: it

George Westbrook: is

Edwin Johnson: Daily daily

Brett StClair: daily. Oh yeah.

George Westbrook: yeah I think I I personally

Edwin Johnson: pants.

George Westbrook: think there should be some daily payout but the amount should be a lot smaller maybe distrib ute wider um because I think me and Brett were talking about earlier like initially like it's a network effect. So the bottom nodes of the graph is where it all spans out from and we want to activate as many of those nodes as possible. Um, I mean, I know when I was in university, if I won a hundred quid, I'd be f****** over the moon. If I won $1,000, I'd be like, I think there was a bet I put on and I won three grand off £3. Every single one of my mates knew about that. Um, they were all so jealous, but obviously it was just normal sports betting, so there wasn't really an incentive for them to do it, and there wasn't an incentive for me to do it. But by allowing a uni student just to win, maybe it's 50 50 people that win a small amount each day, they're gonna be like, "f***, oh, that's the hook." Whereas if it like in my head,

  
  

### 00:14:31

  

George Westbrook: I'd think if I was a uni student, I'm going out on the piss all the time, I've got lectures, I've got to wait a month before I'd win.

Brett StClair: Quit drinking

George Westbrook: Would I stay around? I I don't know.

Brett StClair: money.

George Westbrook: But like $50 or 50 quid for me, I mean, all be I was in Newcastle, so I could have probably gone out for a tenner. Um, but like $50 is the the difference between me having a a cheap night or a good night.

Brett StClair: 50 quid a month.

George Westbrook: Um, and it's going to it's going to make a especially obviously considering that we're going to be targeting the colleges colleges first where their attention span's really small and my only concern would be if it's waiting a month are they going to are they just going to churn? Um, but I think it's a fantastic idea about the ramp up because then it's like as users, they're going to think, right, so if I if I refer more people, I'm getting these I'm getting these inplay dollars, which means that if I f*** it up, I can restart.

  
  

### 00:15:21

  

George Westbrook: And the more people I get, then the bigger the prize pool's going to get. Um, and there might just be that month delay. Um, if there's no payout, that's that's just what I think.

Edwin Johnson: No, it's a great call. I mean, the other thing is like could you imagine if Cody won like five grand that f*****

Cody Haugen: Yeah.

Edwin Johnson: would be kneede in,

Kevin Murray: Even

Edwin Johnson: you know, whouses and liquor and we have to have another 5k for

Brett StClair: I missed.

Edwin Johnson: rehab.

Cody Haugen: Yeah, that's that's probably true. What about something in the middle of of just weekly?

George Westbrook: H.

Cody Haugen: So you still have your same KPIs, Edwin, where they still have to make the same daily trades. They still have to be engaged daily for a set amount of time. So you can still use the same exact KPIs, but you just expand it to four four payments over the week. A week flies by like no one's business. I mean, to go from Thursday, a Thursday night football game back to Thursday night,

  
  

### 00:16:09

  

George Westbrook: Yeah.

Cody Haugen: it seems like it happens in two days, not a week.

Edwin Johnson: Well, let's ask the voice of reason. Troy, what are you thinking?

Troy McDonald Kane: I mean, I agree with George and Cody and was going to say the same thing.

Cody Haugen: Uh

Troy McDonald Kane: I think weekly, we start with weekly prizes because the concentration is really going to be on Saturdays and Sundays as the season ticks over. So I think doing weeklies that end on Tuesday. So they go through Monday Night Football and Tuesday resets. We do that for the month August and September. So we take it through September. Uh and then we hopefully we'll have enough data to show advertisers that okay now we can rebalance the payout. This is what I was kind of saying the other day. If we just publish the first months and we just do monthly schedules based on like you said level of participation is really key because it doesn't make sense to pay out a lot of money if there's not a lot of participation.

  
  

### 00:17:11

  

Troy McDonald Kane: I think keeping it agile so that we have optionality to change it based on criteria. I mean I think George hit it on the nail like the first iteration is really getting these college students. It doesn't have to be a lot of money. doesn't have to be $100,000. It could be $1,000. It could be $50. But we can maximize the distribution. I think that's how we get the network effect of the referrals. My only concern that I want to highlight is that we don't want to make too many requirements that it becomes cumbersome to keep going and people just give up because oh, I got to spend this much time every day. I got to make like keeping track of the criteria might be a little problematic. To George's point, there's a lot of ADD within Gen Z college students right now. I think we should max three criteria no

George Westbrook: Maybe,

Kevin Murray: I was going to say guys as well,

  
  

### 00:18:02

  

Troy McDonald Kane: more.

Kevin Murray: the only criteria I think we should do is the 50 referrals.

George Westbrook: maybe.

Kevin Murray: You have to refer 50 people in order to go through because that that's worth its weight in gold rather than trade for so many minutes, I think.

Troy McDonald Kane: I actually I actually think it's the opposite. I think the big hurdle that may deter people is that there is a 50 referral. Not like there is a lot of like anti like uh anxiety about

George Westbrook: Hat.

Troy McDonald Kane: referrals for some people like having to go solicit referrals with friends like 50 is also a big number you know I think it's actually we we we get more if we maximize time on the app number of trades because that's what advertisers are actually going to care about

Edwin Johnson: But they want to know that user account

Troy McDonald Kane: more correct yeah I think the referral just stays as the referral you get the referral credits That's the driver for the referral program. But I think the criteria should be minutes on the app, number of trades per day or per week to qualify.

  
  

### 00:19:02

  

Troy McDonald Kane: And maybe a third criteria like you have to watch some of the education or something that to that effect to really show advertisers the the the you know the dynamic of the user base. I don't think the number will be as important through the referrals as it is engagement on the app.

George Westbrook: m Maybe there's one thing we could do whereas it's rather than it being like if you do this you get the full payout. If you don't do it you don't get it. Maybe it's somewhere in between where it's like let's say there's those five steps that we might want the user to complete. Um and they can see right you're going to get £1,000 payout this week and then here are the five steps that you can do to multiply that payout so that it can get up to say 1,500. And maybe there's a we could even do a prize thing for the amount of referrals somebody does. Just a pure here's money for referrals.

Brett StClair: do badging.

George Westbrook: Um, so it could

  
  

### 00:19:57

  

Edwin Johnson: Where are

Brett StClair: You could badge,

Troy McDonald Kane: Yeah, I like the idea of a leaderboard for referrals with a different carrot.

Brett StClair: by the way.

George Westbrook: be

Edwin Johnson: you?

Troy McDonald Kane: Like we could still for referrals that first four to six weeks because that's going to be the critical base as students are returning to campus. Also, it's remember not all campuses come back in August. They actually are sequenced starting mid August to end of September with the last schools coming in that last week of September. So that six weeks from launch of August 22nd through September is really our core base of how do we get the engagement on the universities to to maximize that? And I think we have to keep that in mind that until it's fully in, which is really not till the end of September,

George Westbrook: What?

Troy McDonald Kane: it's going to be a staged growth kind of out. But I like the idea of a separate leaderboard for referrals with a se separate prize like top three referrals for that month get a thousand bucks each or something like or two one five something like that to really that way.

  
  

### 00:20:57

  

Edwin Johnson: cuz f***.

Troy McDonald Kane: Yeah.

Edwin Johnson: Excuse me.

Cody Haugen: Bless

Edwin Johnson: Brett, if believe it or not, that was a cough. I mean, if if you you know how it is when you stay up all night,

Cody Haugen: you.

Edwin Johnson: you're like kind of buzzed on like lack of sleep. Um, you know, Brett, you had thrown out a number of 500,000 users. That's compelling. Um, you know, I think we should definitely put the payout at up to, but you know, we can't pay out $25 million if we've got, you know, 4,000 people who are training at any, right? Like it has to be based on participation criteria and levels. What do you really think? Like you know that Well, number one, do did you think the guy yesterday got it or no? No. Yeah, you're muted.

Brett StClair: No, no, he didn't.

Edwin Johnson: Cool.

Brett StClair: And it it's from where he's coming from. So that's kind of where it's hard, right? I keep using the analogy of me as the techie.

  
  

### 00:22:17

  

Brett StClair: As a techie, I just want to talk acronyms and talk tech and wall in just love technology.

Edwin Johnson: Help

Brett StClair: So if you sit in an office with no one else around and it's the four of us, we are just g geek geeking out, right? And I can imagine it's when you guys all get together,

Edwin Johnson: me.

Brett StClair: you're geeking out about trading and betting and sports. And in order for us to exist outside of our office in the real world, we have to layman's terms how we talk about our tech. Uh because turns out, f*** 99% of the people just aren't as excited about technology as we are. f***. And that's my biggest life lesson. And I think we're seeing it here. like it seems obvious, but the problem is the buyers, the advertisers, the they'll see the potential. And I think people can hook on things they can relate to, they're all sports fans. And I think that's where I get most excited is as long as we can get the positioning for the buyers to go, you're a sports fan.

  
  

### 00:23:20

  

Brett StClair: Yes. Well, then this is the f****** craziest s*** you'll ever see in your life. Oh, wait, you're a better. Then we come at the angle going, "f*** it.

Edwin Johnson: Yeah.

Brett StClair: This is why you're gonna see you're a trader." Okay. And we're going to come in that angle. You see what I we find where their lowhanging relative kind of conversation point. And I don't think he had it didn't seem like he was a massive sports fan. Didn't seem like he was a better and he wasn't a trader.

Edwin Johnson: No. Um, it's interesting because he's in sports marketing, right? Like I mean it it's it's tough to um you know I I wouldn't Oh, here let let me put it like this. You do you remember that Who Wants to be a Millionaire show and then you'd say, "Oh,

Brett StClair: We we still have it still

Edwin Johnson: okay cool." And then you have the 50/50 lifeline.

Brett StClair: on.

Edwin Johnson: And then you also have the phone a friend. I would not call that guy.

  
  

### 00:24:19

  

Brett StClair: No. No. I think the the excited sports person is his boss. the CEO. So, I want to get some facetime with him. So, his CEO didn't have

Edwin Johnson: He um yeah, I don't know if you heard him say though, but I mean he got it enough to say that,

Brett StClair: time.

Edwin Johnson: you know, I know someone who might want to invest in this company. So there there was some I mean I don't believe any of that but like I there was some of that. He um he he he definitely um I don't know, Troy, what do you think of him like in terms of him receiving our

Troy McDonald Kane: I I mean I I agree. I don't think it landed with him.

Edwin Johnson: message?

Troy McDonald Kane: I I was a little surprised that he did cover the space because he just seemed not as jazzed or excited about the opportunity as some of these other uh potential partners that we've pitched to. I feel like he was there out of a sense of obligation, not a sense of actually genuine interest in what we're doing at

  
  

### 00:25:16

  

Edwin Johnson: Yeah. Yeah. I mean,

Troy McDonald Kane: InPplay.

Edwin Johnson: so like we have this like dichotomy where we talk to people who are like whatevers and then we talk to these Israelis who know the space really really well and you know they're basically jumping over their shoes to get to meetings with us because they they see the potential. I mean you you know not everyone can

Brett StClair: They're in the gaming space. They're going f*** insane.

Edwin Johnson: Yes.

Brett StClair: f***.

Edwin Johnson: Is that fair,

Troy McDonald Kane: Oh, 100%.

Brett StClair: No,

Troy McDonald Kane: Yeah.

Brett StClair: I'm not

Troy McDonald Kane: I mean,

Edwin Johnson: Troy?

Troy McDonald Kane: from what I heard of how they engaged with you at the conference to the follow-up conversations that we've already had with them,

Brett StClair: surprised.

Troy McDonald Kane: like they they put stuff in motion within minutes, not hours or days or weeks. Like that that just shows that shows the genuine interest in what we're doing where yesterday it was like you could almost tell like he didn't want to be there.

  
  

### 00:26:11

  

Troy McDonald Kane: like he like and then when Wayne dropped off, I think it even got flatter because at least Wayne was trying to inject some like enthusiasm into the

Edwin Johnson: Abs. Absolutely.

Troy McDonald Kane: conversation.

Edwin Johnson: So you know listen that's one particular person but you know my question is in that sense should we should we

Brett StClair: Okay.

Edwin Johnson: try other angles within Omnicom here because that that's just one guy and and like he works at a company that's part of the brand.

Brett StClair: The

Edwin Johnson: It's not even an indiv like that's not Omnicom. He's like at some other brand, right? Like you know

Brett StClair: We're going to keep hitting up as many different angles in up,

Edwin Johnson: so

Brett StClair: down, left, right. So, we're working that. Um, that is the strongest channel. It's their key marketing, sports, all their majority of their media spend goes through there. But as he said, he's got to now pitch to all the different brands from a marketing point of

Edwin Johnson: I mean, here's the scary part though, Brit, having that guy pitch for us.

  
  

### 00:27:16

  

Brett StClair: view.

Edwin Johnson: I mean, f******. I mean, like, you might as well just, you know, shoot the horse now and yourself because there's no chance that guy's gonna, you know, get anything across the line. I mean,

Brett StClair: Oops.

Edwin Johnson: he I don't think he could sell anything to be honest. And he's only been there a short little bit of time. That guy's a nobody at that place. I I looked him up, you know, a bit and um he's he's he's been there a year and a half and I can't imagine like he has a lot of loyal brand unless he brought brands, who knows? Um but yeah, I mean,

Brett StClair: Surprisingly disappointing.

Edwin Johnson: yeah, it it was very frustrating. You know, we had we had, you know, expectations that there was that we all believed we were much farther along with with these conversations and that they were were leading to bonafide advertisement um interest and you know, well, I think Wayne gets it. I mean, he definitely got it. Okay.

  
  

### 00:28:19

  

Edwin Johnson: The guy was not prepped, you know, yesterday. He was like, and that was I was a little bit surprised he hadn't heard about us before, you know. He's like, "Well, I did look at some things." I'm like, "Well, f***. I would have sent you a few, you know, nudes or something to get you jazzed up if that's what it takes." I mean, because clearly sports is not his area of excitement for a guy who sells sports advertising. Yeah. Very, very, very rough. So, um, that's where my head's at right now. I'm trying to figure out, you know, alternative ways to make this work. I do think that we have to put a threshold on how many users versus how much payout and hopefully that can also motivate the audience to push it. And

Brett StClair: we get a big enough audience with a big enough impression and user and we can prove it

Edwin Johnson: then

Brett StClair: right and I I don't mean prove it to anybody I mean purely from the create the impressions the SSP can fill it and so but it's just not going to be filling it at the 8 to12 CPM ratio that's the problem.

  
  

### 00:29:29

  

Edwin Johnson: Yeah.

Brett StClair: So,

Edwin Johnson: Yeah,

Brett StClair: so the inventory is not working effectively for what it should be working for.

Edwin Johnson: I get that.

Brett StClair: That makes sense,

Edwin Johnson: No,

Brett StClair: right?

Edwin Johnson: no, I get that. I mean, I do think at some point during the challenge,

Brett StClair: No.

Edwin Johnson: it could be provided that we're not pre like if we sell it out for 7 to 14 days, that gives us two runs, Troy, Cody, and Kevin, that we can, you know, essentially, you know, knock this out. I mean, if you think about it, we we haven't marketed this at all and our social media is putrid. We actually lost social media followers in the last month with with them.

Troy McDonald Kane: We lost.

Edwin Johnson: We lost three users. We have to revamp social media because the how we're going to connect with these kids are going to it has to be through that.

Troy McDonald Kane: Yeah, we're have to probably maybe outsource it to a professional agency at this point

Edwin Johnson: So

  
  

### 00:30:23

  

Troy McDonald Kane: that has pages that with distribution and,

Edwin Johnson: yeah.

Troy McDonald Kane: you know, can

Edwin Johnson: Yeah.

Troy McDonald Kane: leverage

Edwin Johnson: Because I mean the the other thing is we think we've got whatever signups and you know we'll see how many of those actually follow through but we can actually say organically we've got this number of signups through through our efforts right and the way that our model works with referrals that that number is worth some multiple it might not be a hundred it might not be 50 but it's going to be worth some multiple because there will be folks who do push the referrals we do have a few of the interns starting July one Troy is

Cody Haugen: Yep.

Troy McDonald Kane: Um July we we're referring to after the World Cup.

Edwin Johnson: two.

Troy McDonald Kane: So the week of July 19th is when the first intern will start.

Edwin Johnson: Cool. And so we we our goal is to have 60 to 70 onampus interns that we're going to pay

Troy McDonald Kane: Yep.

Edwin Johnson: to help promote the product and they get paid, you know, based on how well they recruit and get signups.

  
  

### 00:31:21

  

Edwin Johnson: So that we think that can be very valuable. Um, I just in terms of of us having time for that prize pool. I'm I'm with you, George. I think we have to pay something out every day. I I I mean, it could be, you know, dimminimous, but even 50 bucks is 50 bucks. Maybe it's like, you know, you you you trade, you know, may maybe we pay out, you know, 500 spots, 25 grand a day or something. Or maybe, I mean, again, just talking out loud here, maybe we limit it to game day and we

Troy McDonald Kane: I was just what if we just did Saturdays and Sundays for the dailies and then the we

Edwin Johnson: can

Troy McDonald Kane: do a weekly as well for the full week. So we have three payouts per week. one for Saturday for college football day, one for Sunday for big football day, and then one on Tuesday for the entire previous

Edwin Johnson: Yeah, maybe we distribute 25 grand each day.

Troy McDonald Kane: week.

  
  

### 00:32:18

  

Edwin Johnson: So, I'm at 200 a month.

George Westbrook: Oh,

Edwin Johnson: Not terrible. It gets us something going. I mean,

Troy McDonald Kane: Yeah.

Edwin Johnson: it it fills George's cup, fills our cup, but you know, there's got to be a way to figure this out. It just it's

George Westbrook: hey.

Edwin Johnson: maddening.

George Westbrook: There's always a

Brett StClair: The

George Westbrook: way.

Edwin Johnson: It's a startup talker right there,

Brett StClair: question have you finished the did you finish the

Edwin Johnson: George.

Brett StClair: referral on the web Han? Is that calling together and the KYC from the website?

Hasan Mohammed Ahmed: Um

Brett StClair: Did I see that right? Sorry. Just thinking as you referring and pushing it through for your request,

Hasan Mohammed Ahmed: um Yeah, cuz I think

Troy McDonald Kane: Yeah. Yeah. I was I saw the email when I woke up this morning.

Brett StClair: right?

Hasan Mohammed Ahmed: everything.

Troy McDonald Kane: My plan is to test it this morning and and bring you guys back any feedback, but it from what the email said, it sounds like it's in good shape.

  
  

### 00:33:13

  

Hasan Mohammed Ahmed: Yeah.

Troy McDonald Kane: So, you know, Edwin and Cody, we can take this in our next meeting, but we uh we now have the ability to run the referral program through the trading competition website. it, you know, as we go through the approval process. So,

Cody Haugen: Amazing.

Troy McDonald Kane: we potentially can launch the referral program next week going into Fourth of July

Edwin Johnson: Wow, that's

Troy McDonald Kane: weekend.

Cody Haugen: Yep.

George Westbrook: It's KYC as well.

Cody Haugen: Amazing.

George Westbrook: So, it's obviously a fully KYC

Edwin Johnson: great.

Brett StClair: Hey,

Troy McDonald Kane: Yeah.

Cody Haugen: Yeah. So,

George Westbrook: user.

Cody Haugen: the only thing we missed in in pushing it out is just downloading the app. Um, yeah. No, no, that's great. and and we can send out um George I I'm gonna I mean I'm going to I know you're advising against it, but I'm sending these 600 emails Monday or Tuesday next week. I I have I have like we have to like we have to get out to those 600 people as soon as

  
  

### 00:34:03

  

Troy McDonald Kane: Yeah, I would like to target Tuesday since it's the last day of June uh for it to go out going into the

Cody Haugen: possible.

Troy McDonald Kane: holiday weekend to so we should target the the newsletter the first distribution announcing the referral program being live. Tuesday would be my

George Westbrook: with the with the other emails.

Troy McDonald Kane: preference.

George Westbrook: Um,

Edwin Johnson: Okay.

George Westbrook: what we what we I don't know if you saw the email the other day,

Brett StClair: Please.

George Westbrook: I think it was I don't know if it was that one is for like the cold outreach, let's call it B to B2B outreach.

Cody Haugen: need to be

George Westbrook: Um,

Cody Haugen: out.

George Westbrook: that's that's where we'd need the the three emails per domain with a real name. Um once the all the warm-up infrastructurees done, I've just got to log in and then I'll get that then I'll get that firing.

Cody Haugen: So the ones that we have sent over, you want actual names at

George Westbrook: Yeah.

Edwin Johnson: Can we make up a person that's just like an,

  
  

### 00:34:55

  

Cody Haugen: getinplaytradingchallenge.com.

George Westbrook: Yeah.

Edwin Johnson: you know, an avatar that

George Westbrook: I wouldn't because what like say if I get a cold email and it's something I'm

Edwin Johnson: you

George Westbrook: actually interested in um I'll look up the person's name, I'll look up the company and then if it's if I can't see anything I'm like what the f***

Brett StClair: Um,

George Westbrook: is this? I don't know what this is. Um so it's if it's real people um and then what we need to do as

Edwin Johnson: Right.

George Westbrook: well is set up the domain redirect. So if they typed in, let's say it's getinplaytradingchallenge.com, obviously that's not the real domain at the moment. It redirect to the trading challenge page and then that's that that's two 3 weeks and then they can all fire

Cody Haugen: Is that is that the same as sorry for the I think dumb question,

George Westbrook: out.

Cody Haugen: but is that the same as setting up an alias for for an email or do we actually have to register these

George Westbrook: have to have to like register them and then they'd be like as if they're paid well not as if

  
  

### 00:35:53

  

Cody Haugen: emails?

George Westbrook: they are paid paid users but I think was it Microsoft is like8 or nine eight or nine pounds maybe a bit more actually

Brett StClair: Perfect.

George Westbrook: um so yeah paying for the user license um and then we'll link that up to the warm up the warm up will get going and then at the point at which you want to start sending cold outbound outreach to new prospects prospects of B2B. Um, that's that's what we'd that's what we'd use as well as LinkedIn obviously.

Cody Haugen: Yeah. Okay. Sounds good. Yeah. We'll we'll we'll chat on

George Westbrook: Uh,

Troy McDonald Kane: Yeah,

Cody Haugen: it.

Troy McDonald Kane: let's uh let's come into our call on Friday with a call like a a plan of action

George Westbrook: perfect.

Cody Haugen: Yeah.

Troy McDonald Kane: because again uh ideally it would be great to get this first newsletter distribution note out uh next.

Cody Haugen: Well, the new Yeah, that newsletter is going out.

Troy McDonald Kane: Yeah.

Cody Haugen: Uh, for sure. And we'll we'll send it from I mean, we can send it from your Inplay Global, my Inplay Global, Kevin's, and we can divide the 600 into 200 a piece and send it out that way.

  
  

### 00:37:08

  

Cody Haugen: Um, but that's going out. But for the B2B, he's saying we got to warm it up and make those names.

Troy McDonald Kane: I understand B2B for sure.

Cody Haugen: Yeah. Yep. and and that also needs to get going.

Troy McDonald Kane: Yeah,

Cody Haugen: But um yeah.

Troy McDonald Kane: but we got to get B to C off next

Cody Haugen: Yep. B TOC is definitely going out. Has

Troy McDonald Kane: week.

George Westbrook: Let me let me do some research tonight on the B TOC one and

Brett StClair: Come on.

Cody Haugen: to

George Westbrook: then I'll let you know what I find.

Brett StClair: Hold it.

George Westbrook: I appreciate what you're saying. They need to go out next week. Um, but the B B TOC ones are a bit different to B2B in that you can if they're transactional emails instead of marketing. Um, especially with a sign up as well. I just need to do some more research on

Cody Haugen: Yeah. And and and in in that research, George,

  
  

### 00:37:52

  

George Westbrook: that.

Cody Haugen: something specific that I'd like you to look into for me is that these 600 people have already signed up through our through our form. Like these are all form signups. They're all students or people who have come to the website, signed up, and agreed to consent. So, so does that make a difference of of landing in a spam or an inbox if you've already given your information? I think it absolutely should. But what does a dumbass computer say about that? You know, like like I already gave my information. I want to connect with this company. It should not go to spam. But what does an automated system think about that?

George Westbrook: H M yeah I think off the top of my head it's in it's the engagement that happens with that email that's sent be it a link click or u

Cody Haugen: Yeah.

George Westbrook: yeah so it's is it's the engagement but like so say for example password reset emails um like people use different a they will use aliases for this um because I

  
  

### 00:38:52

  

Brett StClair: There you go.

George Westbrook: won't go into detail they'll use an alias they'll send it 95% of the time when they send that email, somebody's clicking on it. So, high engagement on the email. Um, and then that's why they wouldn't go to spam. It's obviously like the cold outreach ones. 99% of them pe people don't even open.

Cody Haugen: Yeah, but these people will because they've already signed up.

George Westbrook: Yeah.

Cody Haugen: They're they're waiting for Implate to send them something positive.

Brett StClair: Yeah.

George Westbrook: Yeah. Yeah.

Brett StClair: Yeah.

George Westbrook: That's that's in in that case is

Cody Haugen: Let's Yeah, let's just look into it. I I mean obviously I know a computer is ones and zeros, but it there's got to be some complexity to it.

George Westbrook: Yeah. Yeah, there is. It's just uh Anyway, we'll go down a rabbit hole.

Cody Haugen: Yeah.

George Westbrook: I'll research when I got it.

Cody Haugen: Yeah.

George Westbrook: I'll send it over.

Cody Haugen: All right. Cool. Yeah.

  
  

### 00:39:43

  

Cody Haugen: Thank you, George. Appreciate

Brett StClair: Especially

George Westbrook: I'll write that write that on my hand.

Cody Haugen: it.

George Westbrook: That is that's you know when it's a high priority thing when it's it's not in it's not in Siri. It's it's on my hand.

Edwin Johnson: That's not good, George. People are going to think you're tatted up. That beautiful face and body. I think it's destroyed by the

George Westbrook: email research.

Edwin Johnson: ink.

Brett StClair: when it's nice and sweaty and it's going to rub off somewhere as you're doing that

George Westbrook: Ah s***. Yeah, I need to actually write it down

Brett StClair: right.

Edwin Johnson: That's true.

George Westbrook: somewhere.

Edwin Johnson: When is your heat wave supposed to be over?

Brett StClair: Another week I think.

Edwin Johnson: I saw like Paris had the hottest temperatures in history.

Troy McDonald Kane: can't be

George Westbrook: my ch Tuesday next

Troy McDonald Kane: good.

George Westbrook: week.

Edwin Johnson: And you guys don't have like air conditioning, right? It's just a hot box everywhere.

George Westbrook: We do in the we do in the offices.

  
  

### 00:40:43

  

Brett StClair: I can see.

Edwin Johnson: What about at home?

George Westbrook: Nice.

Max Kingaby: I bought one for myself.

Edwin Johnson: f***.

Kevin Murray: No

Brett StClair: Yeah.

Edwin Johnson: And you got one, Max? Oh,

George Westbrook: back a little f******

Max Kingaby: Yeah.

George Westbrook: D.

Edwin Johnson: that's I can't see that.

George Westbrook: I can't can't sleep if it's too

Kevin Murray: f******

George Westbrook: hot.

Kevin Murray: his head all got ruined.

Edwin Johnson: George,

George Westbrook: Bob already does that for him,

Edwin Johnson: once this is George, once this is all done, we're going to take the the inplay crew and the Novo crew and we're going to go to a

George Westbrook: Kevin.

Edwin Johnson: luxury resort and just get absolutely f***** up. And we're going to run the air so low.

Brett StClair: Okay.

Edwin Johnson: Max is going to be we're in a f****** winter.

Max Kingaby: I want to take code at Texas. Hold him. I've been practicing.

Brett StClair: You don't hold.

George Westbrook: Yeah,

Max Kingaby: money's on.

George Westbrook: I I just

Brett StClair: It's not about holding a

  
  

### 00:41:32

  

Edwin Johnson: Well,

Max Kingaby: I'll leave that to

George Westbrook: hope

Edwin Johnson: the reason Cody always Cody always wears a hat is because he plays strip poker.

Brett StClair: Texan.

Edwin Johnson: So,

Cody Haugen: I I I do have some uh some neck ties underneath here. You just can't see them. I got a few articles that I can lose before we uh really get down to it. Uh exciting news. Um Anna from Mastercard uh just scheduled Monday.

Edwin Johnson: That's

Cody Haugen: So yeah, Troy and Kevin, sorry. I was texting with Edwin late last night as Anna from Mastercard was getting back to me finally from

Edwin Johnson: great.

Cody Haugen: SBC reach out. Um f*** pay. Terry, I don't know. Whatever. He didn't get back to me, but Anna from Mastercard.

Troy McDonald Kane: They're dead to me.

Cody Haugen: Uh Yeah.

Troy McDonald Kane: It's either pay.com or others like pay is dead to

Cody Haugen: Yep.

Troy McDonald Kane: me.

Cody Haugen: Exactly. Dead to pretty much all of us. Um and so um yeah,

  
  

### 00:42:19

  

Troy McDonald Kane: Yeah.

Cody Haugen: so Anna from Mastercard came back and wrote a very long email for being Mastercard, I thought. um and had some really good questions and some very high level of in of intrigue into our regulatory uh background and how we differentiate from a lot of the turmoil that is happening around prediction markets and sports betting. Um and so yeah uh she just scheduled a call for Monday. So I'm not going to make that interview on Monday. Uh, Troy, we we'll figure out a Yeah.

Troy McDonald Kane: reschedule. I actually like to be on that call on Monday if possible as well. So, we'll res that interview.

Cody Haugen: Yeah.

Troy McDonald Kane: It's not

Cody Haugen: Yeah. Absolutely.

Troy McDonald Kane: critical.

Cody Haugen: We'll we'll get the people on.

Edwin Johnson: and I I'm talking to Goldman Sachs later today, too.

Cody Haugen: Awesome.

Kevin Murray: Yeah,

Edwin Johnson: And then we've got the uh the Israelis

Brett StClair: Nice.

Edwin Johnson: tomorrow.

Cody Haugen: Yep.

Kevin Murray: perfect.

Cody Haugen: Lots of pokers in fire still.

  
  

### 00:43:17

  

Brett StClair: Um,

Kevin Murray: Yep.

Brett StClair: I just wanted to check something with you on the Android verification on the store. Is that moving forward? No.

Troy McDonald Kane: I'm

Brett StClair: On the Android Play Store is Is that moving forward?

Troy McDonald Kane: Sorry.

Brett StClair: Cuz we were hopping on today and I see it. I thought it would have been cleared and authorized. Um I don't know if you stuck or if there's stuck somewhere there because I might have some contacts in the Android or Play Store to try and move that.

Cody Haugen: All

Troy McDonald Kane: Yeah, I'll into it. I am um I am processing the app. So,

Cody Haugen: right.

Troy McDonald Kane: I'll I'll check into the Android store today. The Apple store is actually moving along again. So, we got the like we got we figured out where everything was sitting.

Brett StClair: Bless

Troy McDonald Kane: We got that processed earlier this week. I'm paying the uh annual app developer payment which is

  
  

### 00:44:13

  

Brett StClair: feet.

Troy McDonald Kane: FYI when it's 99 bucks a for the year.

Edwin Johnson: Wow, that's

Troy McDonald Kane: Well,

Edwin Johnson: deep.

Troy McDonald Kane: I think I think it's kind of silly to be that you have to even pay anything to be in the freaking store,

Brett StClair: All right.

Troy McDonald Kane: but whatever. Um yeah.

Edwin Johnson: I was going to say buy two at this rate.

Troy McDonald Kane: Uh so uh so that's moving along. So hopefully that should then allow us to now drop whatever else we need in the app store. I'll look into the Android store this morning and see what's I know there was like some they needed us to verify our website or you know some some other criteria that hasn't been fulfilled yet. But uh I'll look into what the outstanding requirements are today.

Cody Haugen: Yeah, Hassan, because you're actually uh well, you're all in there. I added all of you guys like I don't know a month ago when Brett sent that original email.

Brett StClair: Yeah.

Cody Haugen: Is that something you guys can help us verify because you're admins in the website as far as or I

  
  

### 00:44:58

  

Brett StClair: Yeah.

Cody Haugen: guess let us specifically Troy and I specifically know what you guys need. But um if there is help there, if you can go in from the developer side and and and give us a a push or a help helping hand.

Hasan Mohammed Ahmed: I mean like I think checked it over and believe you have to have the actual um I think it's like the owner access and so because I believe um admin access isn't actually high enough and so like update any of those actual steps

Cody Haugen: Got it. No, that makes sense this time. Okay.

Brett StClair: on the website authorization. Do we need to drop a tag or anything? Do you know to help um Cody with that?

Hasan Mohammed Ahmed: I'm on short. How you can check that?

Brett StClair: Yeah, let's just double check that. So, Cody, yeah, on the website sometimes it is a tag drop and it speeds it up because there's usually three different

Cody Haugen: Okay. Yeah, there was Yeah,

Brett StClair: ways.

Cody Haugen: it was it was the website, Troy, and there was one other piece.

  
  

### 00:46:08

  

Cody Haugen: Um, let me pull it up right now.

Troy McDonald Kane: All right. Um, and uh, I just,

Brett StClair: What's

Troy McDonald Kane: if you couldn't tell, I was doing the verification process while we were talking five minutes ago,

Brett StClair: this?

Troy McDonald Kane: so that worked. Uh, it says it's spinning. It says verifying you. This usually takes a minute. Keep this tab open. It's been a minute. I'm not sure if it's stuck somewhere on the back end.

George Westbrook: Yeah.

Hasan Mohammed Ahmed: Yeah,

George Westbrook: because I'm sorry.

Brett StClair: Come

Hasan Mohammed Ahmed: cuz I'm still think organizing it now to see see if it actually works cuz

Brett StClair: on.

Hasan Mohammed Ahmed: like as in like we only accept like and so then as in as in like if we want to um actually test it. We aren't like able to. So like that's why I just asked like if you can have a check. So thank

George Westbrook: I think I think you were cutting out a bit Hassan there.

  
  

### 00:47:00

  

George Westbrook: B I think I knew basically we've set it up so that it's only US

Brett StClair: Thank

George Westbrook: IDs.

Brett StClair: you.

George Westbrook: Um obviously we we haven't got any US IDs. So we when we have been testing it before we've just been passing the making making sure that it passes um testing everything around that up until that last point where it is just put the US ID

Troy McDonald Kane: Okay. Yeah, that's the point that we're at. So,

George Westbrook: in

Troy McDonald Kane: you have me as a beta to see how it works, but uh I I mean I was able to scan my ID, scan my selfie, and that all went through perfectly. So, that that worked great. So, great.

Brett StClair: Um,

Cody Haugen: Just real quick on Google,

George Westbrook: Perfect.

Cody Haugen: it's verifying the organ uh organization's website and phone numbers are the last two

Brett StClair: yeah.

Cody Haugen: pieces sitting in that uh portal.

Troy McDonald Kane: All right, I will try to handle those today.

Cody Haugen: Um,

  
  

### 00:47:54

  

Brett StClair: if you need hand with the

Cody Haugen: they're both under that. Yeah,

Brett StClair: website.

Cody Haugen: they're both under you, Troy, because you were the uh person we signed up from the

Troy McDonald Kane: Yeah. Yeah. Well, we've added other users to the Android store,

Cody Haugen: company.

Troy McDonald Kane: right?

Brett StClair: Yeah.

Troy McDonald Kane: So the Novo team should have the ability to go in there and do things in the app and the in

Cody Haugen: Well, two things for the app.

Troy McDonald Kane: the Oh yeah.

Cody Haugen: I don't know if they can verify your phone number though for you.

George Westbrook: Perfect.

Troy McDonald Kane: But

Cody Haugen: Yeah. Once once they're in in the app of Yeah.

Troy McDonald Kane: yeah.

Cody Haugen: then they can push out the app and features and and other things. Yes.

Troy McDonald Kane: All right.

George Westbrook: I think I think Is that everything? I think so.

Brett StClair: Um just on a T0 um do we want

Kevin Murray: Yeah.

Brett StClair: to set up a call with the guys today just to talk through like I'm worried that what we'd like to start doing next week is start doing real trades and getting the full on boarding.

  
  

### 00:48:50

  

Brett StClair: And there seems to be it feels like a disconnect between the lightweight API and changing the existing API for the onboarding. And we want to make sure that that's all integrated when we launch the preame pre-launch app. need to make sure that's all tied up and working well. And I we're just talking about it today that in the Slack chat there's a bit of a miscommunication. I'm just thinking let's jump on a call today, get that agreed and tidied up and make sure there isn't any inconsistencies. I just don't want the T0 thing to be a week delay between each decision. And as soon as we spot something, we just get on top of it. Is it okay if we do a recharge, Troy, and and sort out get on a call with

Troy McDonald Kane: Yeah. No, they said to Yeah, please reach out. They said reach out at any time. uh for Friday's session,

Brett StClair: them?

Troy McDonald Kane: the plan is to go through the short selling requirements again and uh have a triple check of what the primary offering is going to look like between their API and how you're displaying it on your on the app.

  
  

### 00:50:04

  

Troy McDonald Kane: So those are the two primary topics for Friday's call. So you should get anything else out of the way

Brett StClair: Let's get in there.

Troy McDonald Kane: before.

Brett StClair: Okay. Yeah, because I think if we can get that done and in the bag,

Troy McDonald Kane: Yeah.

Brett StClair: then we've got everything on the pre-launch app and now it's just package it all up,

Troy McDonald Kane: Yeah.

Brett StClair: get it on to uh what's an APK and push it to the stores.

Troy McDonald Kane: Evangelist will be your key key person to talk to. He's the project manager for this.

Brett StClair: And he's quite the evangelist.

Edwin Johnson: TMD is Mr. Preacher. George, I saw you put the um or TS on or Max,

Troy McDonald Kane: Yeah.

Edwin Johnson: somebody put the welcome screen on. Um appreciate that.

Troy McDonald Kane: Yeah.

Cody Haugen: Who's

Troy McDonald Kane: Looks

Cody Haugen: that?

Troy McDonald Kane: great.

Edwin Johnson: On the I have one request.

Max Kingaby: Oh, the app. Is that on the app?

  
  

### 00:50:54

  

Edwin Johnson: Is that you?

Max Kingaby: Yeah.

Edwin Johnson: Kings beat.

Max Kingaby: Yeah.

George Westbrook: Yeah,

Edwin Johnson: Is it king of be or kings beat?

Max Kingaby: Yeah.

Edwin Johnson: King a beat.

George Westbrook: we just call him wine cut to be honest.

Max Kingaby: Yeah.

Edwin Johnson: I prefer Kings beat. If I If I'm being honest, I prefer Kings

Max Kingaby: George, say it again.

Edwin Johnson: beat.

Max Kingaby: Someone other than Brett might laugh.

Brett StClair: We all

Troy McDonald Kane: Wait.

Brett StClair: love.

Edwin Johnson: What's yours?

Max Kingaby: I

George Westbrook: I said we we don't call him king.

Max Kingaby: said,

George Westbrook: We just call him

Edwin Johnson: Oh,

George Westbrook: wanker.

Max Kingaby: "Thanks,

Edwin Johnson: so I I got a very quick before we go because generally I'm yelling on these calls

Max Kingaby: Cody.

Edwin Johnson: or piss pissing people off. Let me give you a quick story about being a wanker. Um, so about a year and a half ago, my I took my family over to Europe and we were taking the high-speed train from Paris to uh London and there was some crazy Asian dude who was like on me like he wouldn't give me space, right?

  
  

### 00:51:49

  

Edwin Johnson: So, you know, we were in we were in the the train. I'm putting the bags in the thing and this guy's hovering over me and I turn around and I'm like, whoa, you know, back the f******, guy. Right. And and I he was invading my space. He clearly didn't speak English. So I turn around again and he's even f****** closer and I like go back. I'm like, "Holy f***." Like, you know, it looks like I'm going to get shaved or something. And I hit my head on the rail of the the the thing. I I actually gave myself a concussion. Okay. So now I'm like, we're taking the train over there. I'm all f***** up. and we get to the hotel and we're staying at a really nice hotel in um uh what's it nightsbridge you know so this this really really great hotel and you know obviously you they're like it's a very formal pl formal place whatever and um you know it was hot and it was hot because I was sweating from this concussion and you know I called down I'm like hey you know this

  
  

### 00:52:45

  

George Westbrook: Okay.

Edwin Johnson: the air is not going the right way. I need I need temperature control. They're like, "Sir, um it's working on our end." I'm like, "Well, it's not f****** working on my end, right?" And um the next thing I know, I call again now. Now I'm getting pissed off, right? And I got a bad temper. So I'm like, "m***********." You know, I start losing my s*** and I'm like, "I'm telling you, it's f****** hot in here." So then they send up a guy and he must have opened up the air conditioner from I don't know, from the North Pole. this m***********. He he it ends up going from like 70 degrees in there into like 50 like instantly. And so, um, my wife's like, "Hey, you know, it's too cold in here." And I'm like, "Yeah, it's starting to get cold." And she goes, "Well, if you didn't call down, you know, those guys down in the room, they're probably saying, "Blast that wanker." You know,

  
  

### 00:53:40

  

George Westbrook: Who is

Edwin Johnson: and so my so now this this funny story is like whenever I do something stupid, my wife's like,

George Westbrook: this?

Edwin Johnson: "Blast that wanker." Right? But it was so bad. Evidently, I went off so bad that I was eating breakfast the next morning and the manager of the hotel came over to my breakfast table and was like, "Are you okay?" And I was like, I you know, I pro I I I'd say I probably lost my temper or something. Um, but you know, but I was staying at like the Mandarin Oriental in in Nightsbridge, you know, and it's like I don't think people say swear words or cuss words in there.

Brett StClair: Let's see where it is.

Edwin Johnson: So you know they're basically they were not not happy uh with me there much time but

Brett StClair: It's uh I'm picturing you in peak hour tube where people are heaving and

Edwin Johnson: whatever

Brett StClair: crushing people onto it and yesterday was like that on the tube and it's must be about 42° C and you got people just squeezing in and you going like and you got to be comfortable with like six people's bodies breathing and sweating all over you and I'm still haven't

  
  

### 00:54:44

  

Edwin Johnson: absolutely No,

Brett StClair: got my head around that.

Edwin Johnson: I mean I wish you guys great success, you know, doing getting through that. Um, Mr. Kingabby on that uh if you're handling that like splash entry once we get to the second page I don't want it to be duplicative where it says welcome back George like you know so on the on the splash it says welcome back George. um you know and then on the next page it also says that you know maybe there's something else we can put in there like you know good trading or I don't know it's anything other than the duplication because I do want to walk through um as many brands as like I'm still going to punt like punch around every corner I can get and pitch everybody I got like I'm I'm not a quitter and I'm

Brett StClair: Good evening.

Edwin Johnson: not I'm not saying we're doomed. I'm just saying I'm doomed.

Cody Haugen: Um, last piece from my side. I just clicked around all of the different uh trading challenges.

  
  

### 00:55:39

  

Cody Haugen: I just That's f****** hot.

Brett StClair: photo from my wife while she's

Cody Haugen: Yeah. Yeah.

Edwin Johnson: Wow,

Brett StClair: driving.

Cody Haugen: Yeah. That's like almost 100 degrees or over 100 degrees.

Edwin Johnson: it's

Brett StClair: Yeah. I don't know what it

Edwin Johnson: over.

Cody Haugen: Um, yeah. Sorry. So,

Brett StClair: is.

Cody Haugen: I just clicked around the trading challenge page and the homepage. Where did we lose our uh little magic tool to input any brand into our little advertising? And I'm not seeing it anywhere. Can someone just shoot me a link to that

Skye Capazorio: It's on the challenge website,

Cody Haugen: again?

Skye Capazorio: Cody. It needs to transfer onto the inplay one. Uh because the challenge site hasn't gone

Cody Haugen: Yeah.

Brett StClair: No,

Cody Haugen: Yeah.

Brett StClair: I'm not going

Skye Capazorio: live,

Cody Haugen: I cl I clicked on your link that you sent in uh in uh

Brett StClair: to

Skye Capazorio: the other day.

Cody Haugen: in in yeah in the teams and it's nowhere to be found on

  
  

### 00:56:26

  

Skye Capazorio: Oh, then it should be on there. Max,

Cody Haugen: there.

Skye Capazorio: do you know do you know what's happened to the advertising page? Because it was it was on there when we were reviewing it.

Cody Haugen: Uhhuh.

Max Kingaby: um on the trading challenge

Cody Haugen: Yeah. on that on that advertising where that cool little tool you guys gave us last week that we could like upload

Max Kingaby: site.

Skye Capazorio: Yes.

Edwin Johnson: image.

Cody Haugen: any uh image and company web page and then it would like basically put their logo in uh the screenshot of the apps the app pages. I I want to do that for Mastercard so we're ready for

Max Kingaby: Uh yeah, good.

Cody Haugen: Monday.

Max Kingaby: That's a good point. I've just gone on and it's not there. Um I'll look into that and fix that for you ASAP.

Cody Haugen: Cool. Thank you, buddy.

Max Kingaby: Sorry.

Cody Haugen: Uh yeah, just shoot me a link when uh when it's up and fixed.

Max Kingaby: Hold it.

Cody Haugen: Cool.

  
  

### 00:57:15

  

Edwin Johnson: All right.

Cody Haugen: Thank you.

Edwin Johnson: Anything else for us talking?

George Westbrook: Who's going to say

Cody Haugen: Let's f****** go.

Edwin Johnson: I'll say it.

George Westbrook: it?

Cody Haugen: You say it.

Edwin Johnson: It's time to f****** go.

Cody Haugen: There we go.

Edwin Johnson: Thank you all for your time today.

Kevin Murray: All right,

George Westbrook: Right.

Kevin Murray: have a good one,

Edwin Johnson: Um Brett and uh Sky,

Kevin Murray: guys.

Edwin Johnson: if you have any thoughts or whatever on the advertising front, please reach out. Um you know, and by the way, we're just trying to keep open dialogue so you guys know exactly where we're at. You know,

Brett StClair: Yeah.

Edwin Johnson: we're not cry babies. We're just like for business purposes, it's probably best to know where everyone stands.

Skye Capazorio: Can I just ask a quick question?

Edwin Johnson: Okay.

Skye Capazorio: the modeling that you were working on in terms of the various different ad units,

Brett StClair: agree.

Skye Capazorio: the the different premium pricing, the uh cost per view, all of that sort of stuff.

  
  

### 00:58:05

  

Skye Capazorio: I know I think last week you said two weeks. Uh do we have a a date in mind for next week to review what that looks like?

Brett StClair: I get it ready for next week's standup uh touchdown.

Skye Capazorio: Okay. Okay. Great.

Brett StClair: I'm going have to work it out.

Skye Capazorio: Thank you.

Edwin Johnson: And I'm sorry,

Brett StClair: No worries.

Edwin Johnson: could you refresh me real quick? What is that? Um uh what what is that

Brett StClair: Uh trying to work out what a

Edwin Johnson: for?

Brett StClair: forecasted impression basis would be based on all the different user types and all that kind of stuff. um and to break away from the minute to impression conversion ratio and try use the metrics that industry kind of standards go to and then I want to sit with you guys and go okay you guys are the degenerates how much time all you'll be doing how will you use it and then translate that into clicks and impressions and really give us an accurate kind of forecast on

  
  

### 00:59:05

  

Edwin Johnson: Yes. Yeah.

Brett StClair: that.

Edwin Johnson: So I and and just to to make Cody and I feel better, it's not just for Dens. Remember,

Brett StClair: Yes. Yeah. Yeah.

Edwin Johnson: we've got an we do have an investor who became a DGEN that Schwab

Brett StClair: Yeah.

Edwin Johnson: guy who's an a cananker sold conservative f***.

Brett StClair: Yeah.

Edwin Johnson: You know what I mean? It's like like this guy lives at a country club. You know what I'm saying? like he's not he's not

Brett StClair: George.

Cody Haugen: He's not covering our cloth. Let's just say that much.

Brett StClair: George.

Cody Haugen: No. Um, and then sorry, one last thing on the brain is uh just waiting for you guys to schedule that research

Edwin Johnson: no

Cody Haugen: module.

Brett StClair: Yes, thank

Cody Haugen: Yes, Brett. Thank you.

Brett StClair: you.

Edwin Johnson: way that was very British. I felt like I was watching like Nodding Hill right there.

Cody Haugen: Uh, I'm ready when you are, Brett. When Whenever Whenever you decide is the right time, I'm ready.

Edwin Johnson: The heat got to him,

Cody Haugen: Exactly.

Edwin Johnson: Cody.

Cody Haugen: We're we're we're getting fried out here.

Edwin Johnson: Cool. Awesome. All right. Well,

Cody Haugen: Cool.

Edwin Johnson: all have a great day. Thank you. Please stay cool. We'll talk soon.

Cody Haugen: All right.

George Westbrook: Thank you.

Troy McDonald Kane: Hey.

Cody Haugen: Thanks, everybody.

Brett StClair: Thanks guys.

Skye Capazorio: Thanks.

Cody Haugen: Yeah.

Edwin Johnson: Thanks all.

Skye Capazorio: Bye.

  
  

### Transcription ended after 01:00:28

  

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.

**