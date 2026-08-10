---
date: 2026-06-05
type: standup
status: extracted
extracted-to:
  - "[[digests/touchdowns-01-10-jun-2026]]"
  - "[[referral/referral]]"
  - "[[information-layer/information-layer]]"
  - "[[inplay-global-website/inplay-global-website]]"
  - "[[trading/trading]]"
  - "[[architecture/open-questions]]"
description: "Transcript of the 2026-06-05 touchdown call — referral system demo, live Sportradar data in the prototype, website redesign walkthrough, and in-app ad mockups"
---

## Post-Call Analysis

> Processed as part of the **[[digests/touchdowns-01-10-jun-2026|1–10 June touchdown sweep]]**.

| Finding | Destination | Action |
|---------|-------------|--------|
| Referral system demoed — lifetime-unique codes (~1B tested), QR page, referrer/referee table, KYC-gated crediting, preset boost windows | [[referral/referral]] | Changelog entry added |
| Cody's share flow — referral screen immediately post-KYC; one-click image-prepopulated social share (per-platform); own-code feedback loop; profile-page surface | [[referral/referral]] | Share Surfaces enriched |
| First-version app scope: referrals + wallet + signup + KYC (required) + some live data; not full in-app trading | [[customer-onboarding/customer-onboarding]] | Delivery note updated |
| Sport Radar data live in prototype; replay sim (week 10 2024) with real stats; demo data labelled | [[information-layer/information-layer]] | Touchdown note added |
| Demo strategy — demo on mock-data branch (production-like), not incomplete live-SR branch | [[information-layer/information-layer]] | Touchdown note added |
| Global Website redesign — exact deck copy, brand colours, imagery-last; hero, partners, team, football-challenge; outline font; CTA→form reason-routing to DLs | [[inplay-global-website/inplay-global-website]] | Update block + Page Map updated |
| App ad placements designed (Coca-Cola/Gatorade/etc.; MX banner across game screens); header lock vs scroll as advertiser options | Advertising (cross-cutting) via digest | Noted |
| tZERO homework — buying-power/referral-wallet operation + look/feel; NOVO-vs-tZERO responsibility split | [[architecture/open-questions]] | Row added |
| **Affiliate revenue (FanDuel-style rev-share); $25M operator raise at conference** | digest triage | New commercial lever — noted |
| **Multi-sport view-only re-raised** (one-email trial); George's focus concern vs Edwin's monetise-the-minutes | digest triage | May "not doing" stands; revisit v2.0 |
| Press release — Skye's tZERO draft + tZERO draft, merge for Tuesday | [[inplay-global-website/inplay-global-website]] | Noted in update block |

---

**

Jun 5, 2026

## InPlay Digital TouchDown - Transcript

### 00:00:00

   
Max Kingaby: How you doing?  
Edwin Johnson: Hey, what's up, Max?  
Max Kingaby: Nothing much. You well?  
Edwin Johnson: I'm hanging in there. Been a long f****** week, bro.  
Max Kingaby: I can I can imagine if it makes you feel any  
Edwin Johnson: I'm sure you had one,  
Max Kingaby: better.  
Edwin Johnson: too.  
Max Kingaby: Hello.  
Edwin Johnson: I'm sure you've had one, too. I We Everyone's fighting the same fight.  
Max Kingaby: Sorry.  
Edwin Johnson: We got to get up every day, make a little money, eat something good, hopefully find someone uh special to hug on.  
Max Kingaby: That's That's more of a challenge than you would probably imagine.  
Edwin Johnson: Not for you. For me, maybe you not for you. If I had your looks, oh my god, I'd own I'd own London and I'd have a I believe you call it a bevy of birds waiting to chirp.  
Max Kingaby: A bevy of birds. It sounds like the uh sounds like the life,  
Edwin Johnson: I mean,  
Brett StClair: Hello guys.  
Edwin Johnson: it sounds like the life I'm going for.  
Brett StClair: Sorry.  
   
 

### 00:01:10

   
Max Kingaby: eh?  
Edwin Johnson: What's up,  
Brett StClair: Hello. Hello.  
Edwin Johnson: Brett?  
Brett StClair: Everyone's coming now. Sorry, we all got caught up here.  
Edwin Johnson: You got  
Max Kingaby: That's  
Edwin Johnson: tZERO.  
Brett StClair: Uh tZERO call. Yeah, I think quite a bit got discussed and went through.  
Max Kingaby: Yeah.  
Brett StClair: So, it was a good session.  
Edwin Johnson: Was it a good call or did we have a fire?  
Cody Haugen: Uh,  
Brett StClair: Happy  
Troy McDonald Kane: No,  
Cody Haugen: no fires.  
Troy McDonald Kane: it was a good call. Good call. Good call. It was just, you know, going through we're we're in good shape for,  
Cody Haugen: Yeah.  
Troy McDonald Kane: you know, um the NOBO team has really gotten things up very quickly. So, uh it was more just now getting into all the final final finer details to ensure edge cases and test scenarios. So, um, one thing we need to take away for us to work on, um, is how we want the buying power, referral wallet, all of that to kind of operate and look and feel.  
   
 

### 00:02:07

   
Troy McDonald Kane: Um, you know, and how what part does the NOVO team do and what part does the tZERO team do? And that's the homework before next week's meeting.  
Edwin Johnson: All right, great. There they are. Kevin,  
Troy McDonald Kane: Yeah.  
Edwin Johnson: Gary, George E. Boy.  
George Westbrook: Hello. How are we all  
Hasan Mohammed Ahmed: Are you  
Edwin Johnson: It looks like the uh Well,  
George Westbrook: doing?  
Edwin Johnson: it was the inplay group was all the light blue boys and then we got the hammer coming in all black Kevin  
Hasan Mohammed Ahmed: doing  
Kevin Murray: Of  
Edwin Johnson: Murray. I mean,  
George Westbrook: Yeah. Did you you and Hassan have a chat about what to wear  
Edwin Johnson: if I was in Yeah.  
Troy McDonald Kane: I was about to say Yeah.  
George Westbrook: before?  
Edwin Johnson: If I if I had to guess before if I had to guess before Sky  
Kevin Murray: course, mate. Got to got to sync it  
Hasan Mohammed Ahmed: the Yeah.  
Troy McDonald Kane: Yeah.  
Edwin Johnson: gets on,  
Kevin Murray: up.  
   
 

### 00:02:41

   
Edwin Johnson: the two guys pulling the hose are going to be Kevin and Hassan and maybe Uncle Brett throws in with that black t-shirt.  
Cody Haugen: I mean, or they're ankles.  
Brett StClair: a roll.  
Cody Haugen: I'm not really  
Brett StClair: I I I heard that black makes you look thinner.  
Edwin Johnson: Yeah,  
Brett StClair: So that's how I  
Cody Haugen: sure.  
George Westbrook: that it doesn't for you,  
Edwin Johnson: I I've tried it.  
Brett StClair: roll.  
Kevin Murray: Me  
George Westbrook: bro.  
Edwin Johnson: I I I've tried it, Brett. I can tell you it doesn't work for  
Kevin Murray: too.  
Brett StClair: When I do that is the  
Edwin Johnson: all  
Brett StClair: giveaway.  
George Westbrook: You're gonna have to zoom out a fair bit more,  
Edwin Johnson: you young f******.  
George Westbrook: Brett.  
Edwin Johnson: Just wait till you get older. Just wait. It's a b****.  
Brett StClair: Uhhuh.  
Edwin Johnson: And I'm going to tell you something else. Everything hurts, too. And like it's just that you sneeze and you're out of commission for days,  
Max Kingaby: Really?  
Edwin Johnson: you know?  
   
 

### 00:03:26

   
Edwin Johnson: Like it's just an outrageous life that waits for you. It's it's it's not a lot of fun. It's fun, but it hurts. Keep that in mind. Us older guys, well, at least we've lived this long. A lot of people have thrown in the towel by this point, so f***  
Troy McDonald Kane: Oh  
Edwin Johnson: it.  
Troy McDonald Kane: jeez.  
Edwin Johnson: I don't mean to digress, but I mean, it's been a long week, right?  
Troy McDonald Kane: I also have to say Adwin, do you need a hug?  
Edwin Johnson: Yeah. I need a hug and a barrel a wheelbarrow full of cash. Speaking of which, Brad,  
Brett StClair: just  
Edwin Johnson: I'm going to head to the bank sometime today and uh send your payment so you guys will have your cash.  
Brett StClair: thank you.  
Edwin Johnson: Yep.  
Brett StClair: Um,  
Edwin Johnson: I need to make sure Hassan's got the hair product.  
Brett StClair: so I think that is  
Edwin Johnson: I don't want that s*** getting wild.  
George Westbrook: That's That's a hint to get a haircut.  
   
 

### 00:04:10

   
Brett StClair: looking fabulous.  
Edwin Johnson: I wouldn't touch that s*** if I were you,  
Troy McDonald Kane: No.  
Edwin Johnson: Hassan.  
George Westbrook: Had  
Edwin Johnson: No, I mean, if I'm flying into London,  
Brett StClair: Yeah.  
Troy McDonald Kane: Yeah.  
Edwin Johnson: I could see that at about 10,000 ft. I know where to go. Where is that? All right. So, um, who's in charge? Who's running the show?  
Brett StClair: I'll I'll kick it off.  
Edwin Johnson: Where we at?  
Brett StClair: Um, I think we've got a lot to demonstrate today. Um it's just so just giving us a little bit of time just so thank you the the test of just reducing the amount of catchups has given us time to just you know doing dev work you just need that focus period like hours and hours and hours so the team have done quite a bit um uh sun has absolutely smashed the tZERO integration got everything working got all the backend dashboards testing got all the scale kind of testing ready as well so that we can really push the integration and make sure that it's working at scale.  
   
 

### 00:05:06

   
Brett StClair: All of that's ready to go um and made a start on the referral wallet um and the back end of those uh parts of it. So, I think we'll start off with the son just walking through the referral wallet. Then we'll go on to uh Max and Sky have been hammering out the last final details and I think there's still some more today. I think they did a 5h hour stint together so they've gotten to know each other. Um and so that's looking good now. Um, still a couple of more changes, but Max will do a walk through on the website and then on top of that, um, Max has been working on the fidel the fidelity of the prototype app. Um, so he'll do a quick walk through on that and then while we're doing that, George, you might as well jump in and start talking through the sports data has is now linked up to that app. So, we've got a live connection in there and we're displaying sport radar data  
Edwin Johnson: Wow.  
Brett StClair: into the prototype right now.  
   
 

### 00:06:17

   
Brett StClair: Um, so all of that will be pushed this weekend.  
Edwin Johnson: That's  
Brett StClair: So, you guys have on that prototype PWA all the new stuff ready to go plus real data streaming into it. Um, and where it's demo data, it's highlighted as demo data. Cool.  
Edwin Johnson: just give you before you even start, let me just give you a quick update too on our end. Um, we're going to go to a sports conference next week.  
Brett StClair: Awesome.  
Edwin Johnson: Um, three of four of us, I don't forget how many, four of us are going to go. So, all of these assets we're going to try to put in front of people to buy ads next week.  
Brett StClair: Awesome. Awesome. Awesome. Awesome. Awesome. That's fantastic.  
Edwin Johnson: Cool. All right.  
Brett StClair: That's good timing because it Yeah, it's looking good. It's the first level of fidelity. So, like, you know, we start off really kind of like a blank screen and it's about just refining, you know, getting each image just perfected, each helmet smashed.  
   
 

### 00:07:15

   
Brett StClair: Go back to the homepage. You might as well start on the homepage, George. We can't hear you.  
Max Kingaby: You've also got the wrong Gatorade hero cuz that's  
George Westbrook: Just if you wait a second, Max,  
Max Kingaby: been  
George Westbrook: I was saying the this this is not the version that you've been working on.  
Brett StClair: Yeah.  
George Westbrook: It's another version. So that's why I say wait till wait till Max shows his one for the the UI the UI  
Brett StClair: Oh,  
George Westbrook: updates. Um so with the yeah with the live data obviously at the  
Brett StClair: okay.  
George Westbrook: moment there's no real games going on. So what we need to do is we we'll set a point in time and then we'll kind of keep that not looping but for that session that's where we'll set up the simulation. We'll get like the games that are going forward, games that are going back. So I think this at the moment is the end of the day on week 10 of 2024. Um, so obviously it's all showing us the the completed games.  
   
 

### 00:08:07

   
George Westbrook: Um, so these are all at that week 10 exactly the games that exactly the games that happened. Um, what's better this one? Um, so you're going to see less numbers because obviously some of these some of these things aren't actually linked up. Um, so it might not look as good as the other one because obviously now this is now this is real. Um, market data not too relevant. Um yeah, so some of these events we're still linking up. Um but like these scoring, the scoring drives, the stats. Um and then where because a lot of this information at the moment is static, the game day page, there's just not not as much going on. But all of this information here,  
Edwin Johnson: Very  
George Westbrook: apart from the pricing, is the information at that point in time. Um new bits of information added, so might need to be some tidy up tidy ups.  
Edwin Johnson: cool.  
George Westbrook: Um, anything that says demo is obviously still demo data. Same for this. This is at that point in time the actual um the actual standings, the actual results, the actual injury reports.  
   
 

### 00:09:21

   
George Westbrook: Then going to the key players. uh all the all the real stats. So,  
Edwin Johnson: Wow.  
George Westbrook: it's going to be it's going to look like it's taking one step back. Let's go 10 steps forward. Um so, that's where we got the question for next week is with the PWA. Um, in my opinion, I think what might be best is if we we show the fake data with the updated UI. So, it looks, feels, acts exactly like it's going to do in production. Um, rather than us having it like on the game day page, no events, no live  
Edwin Johnson: I agree with you, George.  
George Westbrook: games.  
Edwin Johnson: I think that because you know what I did was I actually made a couple of trades in my meetings and how quick because some people are like oh you know it's trading they don't understand you know you buy something for a thousand shares you sell it you know 20 cents higher for thousand shares you make 200 bucks they then it's like oh s*** people will be addicted to this  
   
 

### 00:10:27

   
George Westbrook: Um, so yeah, so we're still still working on getting in more of the static data. Won't take too long. Um, and then what we'll do is start testing out the live the live data. So when there is a game, when there is a moment that pops up, we'll just be running it on a simulation from sports radar provider simulation endpoint. So we'll get that all linked up. Um and then that's where it'll just be test test. Um both obviously human and AI testing.  
Edwin Johnson: I have a question for you, George. Would there be a solution here?  
George Westbrook: Um  
Edwin Johnson: I don't know that'll be in time or, you know, how how hard it would be, but let's say um you know, you have uh this football on and and we run the simulated live data on that. Um, but there's maybe there's a button underneath that's like other sports that you can click on where there's currently live baseball or live soccer or whatever that you know it shows that live data is coming in. You see what I mean?  
   
 

### 00:11:25

   
Edwin Johnson: So, it's like we can we can always say look our our football data is simulated because there's no football being played but we can show you how quickly the live data works with other sports. We can bring in baseball or  
George Westbrook: Um, Um, one I'm not sure if we have access to those APIs yet.  
Edwin Johnson: something.  
George Westbrook: Um,  
Cody Haugen: You could.  
George Westbrook: we do.  
Cody Haugen: No, you  
George Westbrook: Okay.  
Cody Haugen: could.  
George Westbrook: In part of me thinks in thinking about in terms of user experience, is there any point because I because  
Edwin Johnson: Yes. Um,  
Brett StClair: do it on a more button.  
George Westbrook: it's  
Edwin Johnson: let  
Brett StClair: So you go click more on one of those other screens and you go in there and it can just be a live data screen to show the samples,  
Edwin Johnson: let me let me tell you guys why. So,  
Brett StClair: right?  
Edwin Johnson: what are we really selling the advertisers? We're going to sell them that there's going to be engagement. So, what is our levels of engagement?  
   
 

### 00:12:16

   
Edwin Johnson: It's trading. It's research. It's looking at data. Um, it's also looking at all the other sports games, right? So, like even if we don't have a trading challenge for baseball, people who are are of this degenerate lifestyle like Cody and I, I'm bet I bet hockey last night. I bet, you know, baseball last night, you know, and if I have it on one app where maybe I'm trading on the challenge um for free, I still may be betting on other s*** and want this app to tell me, which, you know, the app that you're creating. By the way, this is possibly the best app in all of sports right now for consumption. the way that you have it aligned and the way that way that you add in the chat plus the ability to trade. There's nothing like this that exists. There's not a single point. You have so much robust data coming from Sport Radar. We don't have a competitor in terms of the the the user experience.  
   
 

### 00:13:13

   
Edwin Johnson: So, I want to try to I want to embellish and and and you know promote how how sticky this is outside of just a trading challenge.  
Cody Haugen: So, real quick, George, like I said, you could It takes me one email to get trial set up and real time activated. Not a lift from our side. So,  
Brett StClair: Yeah.  
Cody Haugen: I could get that done today if if this is something that's feasible for you guys.  
George Westbrook: I mean, it's definitely feasible. I think in my head I'm just thinking is it a matter of should we?  
Brett StClair: Yeah.  
George Westbrook: Because I appreciate what you're saying that like for an NFL experience we've got everything. You can get the data,  
Edwin Johnson: everything.  
George Westbrook: you can do the research, you can have the chat, you can get the trade and what like you said, what are we optimizing for user minutes on our our application?  
Max Kingaby: Enough.  
George Westbrook: um which NFL 100% we've got baseball we don't  
Max Kingaby: Nothing.  
George Westbrook: they can get the information um but like you said  
   
 

### 00:14:07

   
Edwin Johnson: right? Why don't we do this, George? Let Let me solve the issue. Let's just Cody,  
George Westbrook: you  
Edwin Johnson: we'll just tell them, you know, when we talk to anyone that we we're adding other sports. I mean, they'll understand it's live.  
Cody Haugen: Yeah. Yeah.  
Edwin Johnson: I don't want to create a bugaboo. I'm just, you know, as we,  
Cody Haugen: 100%.  
Edwin Johnson: you know, maybe it's in version 2.0, know a release later after we've launched the challenge, we bring in the NBA and the NHL and all the other sports data that we can have just to ensure that the the user experience is as as rounded off as  
George Westbrook: cuz cuz I think that like my only concern would be is if if you have this data,  
Edwin Johnson: possible.  
George Westbrook: you're going to be driving users off the application because it's this there's so much information um around not just NFL, say maybe football in the World Cup or baseball, but then like I said, they're going to want to take a they're going to want to take an action, which could be that bet, but that bet's not going to be with you.  
   
 

### 00:15:02

   
George Westbrook: So, you're driving them to say the betting platforms, whereas  
Edwin Johnson: But that's okay in a sense, George, because if they spend 10 minutes researching their bet on our app,  
George Westbrook: obviously  
Edwin Johnson: they go place their bet and then they come back because our data is live and it's up to date and they've got everything that great. You know, we still monetize those minutes. So even if they have to leave our app to go place the bet somewhere or you know trade on Kali and come back we still get them. Um and I do but before we roll we're going to go over time today Troy. So let's push our our meeting. I I don't want to I don't I don't want to take it too long but I want to update on uh the group on something else  
Brett StClair: Should  
Edwin Johnson: that's developing in the market that we need to be aware of. Okay. Cool.  
Brett StClair: we  
Edwin Johnson: So you see what I mean? See what I mean George? It's just like, yeah,  
   
 

### 00:15:47

   
Brett StClair: do  
Edwin Johnson: if they got to leave to make the bet and they come back, so  
Cody Haugen: And and simply simply put um we're going down to this it's a sports conference. Yes. But it is targeted towards uh operators next week and we're opening the floodgates to fill 25 million on whoever wants to get in outside of some some market segments like p*** or something like that. But if we set up an affiliate agreement with FanDuel and FanDuel wants to throw,  
George Westbrook: Yeah.  
Cody Haugen: you know, five or 10 million at this, we can set up an affiliate agreement, which we actually get paid revenue for um as well, just just like a Schwab account. So, um yeah. So, I mean, it's like if you leave to place the bet, but then they come back because our app's the best. Like Edwin's saying, there's there's multiple functionality behind it. Um just Yeah, we can table it, but that's that's kind of thought process behind it.  
George Westbrook: Okay. Yeah, I understand that. I understand that.  
   
 

### 00:16:47

   
George Westbrook: Um I said Max I think Max is dying to dying to of  
Edwin Johnson: No dying for Max.  
George Westbrook: his version.  
Edwin Johnson: Let's go, Max.  
Cody Haugen: Yeah.  
Max Kingaby: Uh press pressure is on.  
Edwin Johnson: See what's up.  
Max Kingaby: Um  
Edwin Johnson: By the way, that's a hell of a backdrop. Is that your real apartment?  
Max Kingaby: I wish this uh caser more mom and dad's  
Edwin Johnson: Oh, god damn. That's a the mom and dads are living nice very nice  
Max Kingaby: Thank you. Um I will first of all let's go through the website I think.  
Edwin Johnson: Nice.  
Max Kingaby: So, as Brett was saying at the start of the call, me, myself, and Sky, Sky and I um spent some time redesigning the website and getting what we feel is strong branding and brand colors across the whole  
Edwin Johnson: I mean, this looks awesome.  
Max Kingaby: site.  
Edwin Johnson: I mean, I think it's  
Max Kingaby: Yeah. Well, Sky came up and helped with most of the imagery,  
Edwin Johnson: incredible.  
Max Kingaby: so credit to her.  
   
 

### 00:17:53

   
Max Kingaby: Um, so this is our home hero page, and we've got generated image of two players facing off against each other. And what's quite important to mention is the whole site takes the exact copy from the deck that Sky made. I can't remember if she made that with you, Cody, as well, but all of the words from the deck are in the website. No additions, no, you know, no taking words and then changing them. It's the complete copy throughout. Um Oh, you go through. Uh Edwin, this comes straight from your deck. You've got each moment of the game. So turnover quarterback links limps off then he comes back on. So the price spikes. Um yeah and it's it's not quite there yet but compared to kind of where it was um it's been significant  
Edwin Johnson: Oh,  
Max Kingaby: improvement today. Um and it's just yeah with regards to branding I think it's getting much closer to  
Edwin Johnson: incredible.  
Max Kingaby: the final point now.  
Cody Haugen: Yeah,  
Edwin Johnson: Yeah,  
   
 

### 00:19:27

   
Cody Haugen: that  
Edwin Johnson: I do f I I love it. I do find the outline words for me uh a little hard to read.  
Cody Haugen: looks  
Edwin Johnson: I mean once I see it on the screen it might be a little bit easier but like you know the orange outline there the future it's hard for me to see that. Just as an FYI. I don't know about other people but I'm having trouble the band shift.  
Max Kingaby: Is that the color or  
Edwin Johnson: Yep.  
Brett StClair: Just need something more bold,  
Max Kingaby: the  
Brett StClair: right?  
Edwin Johnson: Yeah.  
Brett StClair: Something  
Edwin Johnson: It ju it's just I think the tightness of the the the letters um makes it it's a little bit blurry for me to see, but I'm looking I'm like uh I'm I'm two feet away from Let me wear my glasses. Let's see if this helps.  
Troy McDonald Kane: Yeah, I think maybe if you did a little bit thicker line and maybe brighter,  
Edwin Johnson: No.  
Troy McDonald Kane: it just looks dim like it relative to the rest of the or rest of the rest of the orange on the page.  
   
 

### 00:20:14

   
Edwin Johnson: Compared. Yeah.  
Max Kingaby: Cool.  
Edwin Johnson: the rest of the or the move with it is like okay that's really pops  
Troy McDonald Kane: It Yeah.  
Edwin Johnson: right  
Troy McDonald Kane: So if you can make the make it maybe bolder or thicker outline and then a little bit  
Edwin Johnson: thicker outline.  
Troy McDonald Kane: brighter I think then it  
Edwin Johnson: Yeah.  
Max Kingaby: Okay.  
Edwin Johnson: Yeah.  
Max Kingaby: And it's a similar theme throughout the whole website.  
Troy McDonald Kane: works.  
Edwin Johnson: Yeah.  
Cody Haugen: So,  
Max Kingaby: So one change it's across the whole thing as  
Edwin Johnson: Yeah. Yeah.  
Max Kingaby: well.  
Edwin Johnson: Cool.  
Brett StClair: Do you want All  
Edwin Johnson: Awesome. You want to go to the next page or you're you're in charge.  
Brett StClair: right.  
Edwin Johnson: You do your thing. What's next? Our  
Max Kingaby: This is all about partners and then it's a similar kind of effect along the side here for the  
Edwin Johnson: partners.  
Max Kingaby: numbering um partner with inplay. So once again I'll change that  
Edwin Johnson: Love  
   
 

### 00:21:02

   
Troy McDonald Kane: And then uh Max, real quick,  
Edwin Johnson: it.  
Troy McDonald Kane: let's we should map out where we want those signups to go as far as DLS.  
Max Kingaby: room.  
Troy McDonald Kane: So I if you give me a list of how many different points on the website can direct people to a signup page whether it's just sign up for general information sign up to advertise sign up to like yeah then I can direct that to the right DLS on the back you know from our side I can tell you what those emails are.  
Max Kingaby: So, so Troy, every page has a CTA button at the bottom and the homepage has two,  
Troy McDonald Kane: Yeah.  
Max Kingaby: one at the top and then as well one at the bottom. What happens is takes you to a form. Here's the form.  
Edwin Johnson: Sweet.  
Max Kingaby: And then depending on the reason why you're submitting interest, you can go I just want to be a user. I'm looking for advertising opportunities, media, etc. And then when Hassan puts that site live, he'll direct depending on what option is selected, he directs the um form to the appropriate team your  
   
 

### 00:22:05

   
Troy McDonald Kane: Okay, great.  
Max Kingaby: side.  
Troy McDonald Kane: I'll uh I'll take those categories and assign email distribution lists to  
Max Kingaby: Amazing.  
Troy McDonald Kane: them.  
Max Kingaby: Thank you. Um a bit about the team, everyone's beautiful photos.  
Edwin Johnson: Oh, go back. Let me see that. Let's see this fat little f***. Oh, yeah.  
Troy McDonald Kane: You don't know.  
Edwin Johnson: Jesus.  
Troy McDonald Kane: You You look pretty distinguished there. Uh Edwin,  
Cody Haugen: when  
Troy McDonald Kane: you  
Edwin Johnson: Listen, I I'll be honest with you.  
Cody Haugen: when  
Brett StClair: Good.  
Edwin Johnson: I look like someone I'd buy a casket from at a funeral home.  
Troy McDonald Kane: know,  
Cody Haugen: Well, I'll show you something trying to AI generate or update my headshot, Edwin. It kept combining my face with your face and it looked like a off child that came from both of us. I'll show you once we get together, but it was pretty funny. Um,  
Edwin Johnson: Is that what happens with the Eskimo  
Cody Haugen: so yeah,  
   
 

### 00:22:54

   
Edwin Johnson: twins?  
Cody Haugen: I guess Sky thought there should be some blood testing being  
Edwin Johnson: Oh man, Sky looks great. Yeah,  
Cody Haugen: done.  
Edwin Johnson: that's awesome. f****** Kevin Murray. Jesus Christ.  
Kevin Murray: Photoshop is amazing.  
Troy McDonald Kane: Yeah, these turned out great. Uh,  
Max Kingaby: Yeah.  
Troy McDonald Kane: very very nice.  
Edwin Johnson: Yeah,  
Max Kingaby: Awesome.  
Edwin Johnson: that's a great  
Brett StClair: What Trying to  
Max Kingaby: Um, bear in mind,  
Edwin Johnson: page.  
Max Kingaby: you notice there's not much imagery throughout the website. So, I've stripped the website clean of all imagery.  
Brett StClair: get  
Max Kingaby: That's what me and Sky did today. The whole point of that is because we really wanted to establish your text and copy and how that's going to look on the screen and then build the imagery around it. Which is why for now only the homepage has a few images on it because that's what we've been working through today. um images are to follow for the rest of the site. Um final page, the football challenge.  
   
 

### 00:23:51

   
Max Kingaby: So yeah,  
Brett StClair: Do you want to hit  
Cody Haugen: So minus that uh so minus that one edit of of darkening the the bold around those  
Max Kingaby: and  
Brett StClair: the  
Cody Haugen: letters. Let me put the squeeze on with the question is when do you see the team pushing this live?  
Edwin Johnson: Yeah,  
Cody Haugen: Before before next Tuesday.  
Brett StClair: I think we should  
Edwin Johnson: great. Um, can you  
Cody Haugen: I mean that that would be the that would be the press the press from from our side and the four people who  
Edwin Johnson: go?  
Cody Haugen: are heading down is if I sign you know if I swipe my dot card I don't want them  
Brett StClair: It's going down there.  
Cody Haugen: going to that that blank landing page I want them to see  
Brett StClair: Yeah.  
Edwin Johnson: Yeah.  
Max Kingaby: Yeah.  
Edwin Johnson: And the other thing, uh,  
Max Kingaby: Okay.  
Edwin Johnson: Troy,  
Cody Haugen: this  
Edwin Johnson: Sky sent over a press release for tZERO. Maybe we coordinate a press release around Tuesday, um, that we signed with tZERO  
   
 

### 00:24:40

   
Troy McDonald Kane: Wait. Uh,  
Edwin Johnson: or  
Troy McDonald Kane: she wrote up a press release because TZ is also writing up a press release.  
Brett StClair: Yeah.  
Edwin Johnson: Yeah, she wrote me up a draft. So yeah,  
Troy McDonald Kane: Okay. All right. Yeah,  
Edwin Johnson: I mean we'll we'll merge the two,  
Troy McDonald Kane: let's go. Let's go through it later. Yeah,  
Edwin Johnson: but and then we'll just try to time it as as best we  
Troy McDonald Kane: we can definitely get it out Tuesday.  
Edwin Johnson: can. Can you go back, Max? And Max, by the way, brilliant work, dude. I mean,  
Cody Haugen: Yeah,  
Edwin Johnson: just incredible.  
Cody Haugen: this is great. This is  
Edwin Johnson: Can you can you please go back to the team because I want to make sure the head shots.  
Cody Haugen: awesome.  
Max Kingaby: Hey.  
Edwin Johnson: So what I don't like about this is like go ahead. Okay, go down to the next. You see how I've got like a half body shot?  
   
 

### 00:25:16

   
Edwin Johnson: Troy's got like three a like three ace body shot co  
Max Kingaby: Yeah.  
Brett StClair: No,  
Edwin Johnson: Cody you have about same let's go to sky can can you make mine so it looks similar to those otherwise like Tony also has too much you see what I  
Max Kingaby: Yeah,  
Brett StClair: sorry.  
Edwin Johnson: mean it's like they should all be almost like a professional did them at the same like  
Max Kingaby: that's that's Yeah, agreed. That's that's one prompt.  
Edwin Johnson: distance  
Max Kingaby: I'll I'll get that fixed straight off this call. Um, and then the other thing I've been working on as well  
Edwin Johnson: and by the way let's let's take out that quote Tony that Anthony Tony  
Max Kingaby: was  
Edwin Johnson: verbillis just leave Anthony  
Cody Haugen: Yeah, that was going to be my note.  
Edwin Johnson: it's papo yeah  
Cody Haugen: It makes him seem like a like an underlying mobster or something  
Edwin Johnson: Anthony you know hooks verbillis Just if I  
Cody Haugen: like  
Max Kingaby: Sure. And then uh the other thing I've been working on is the design  
   
 

### 00:26:09

   
Edwin Johnson: can.  
Max Kingaby: side um to the app that George has built. I've been trying to kind of see how advertising could fit into the app and uh I've come up with some designs. Sorry that you can see everything behind.  
Edwin Johnson: Wow.  
Max Kingaby: Uh, so this is how Coca, this is obviously just the first bracket. Um, if you don't like it that it can easily be changed. But if we were to get Coca-Cola, there's what I thought was quite a cool hero for the homepage of your app.  
Edwin Johnson: It's incredible. Yeah.  
Max Kingaby: Uh, you go to the discovery page. You've got that Gatorade one's now slightly changed.  
Edwin Johnson: Oh, see now now we're talking f******  
Cody Haugen: Yeah, that's  
Edwin Johnson: M. That is awesome.  
Max Kingaby: Um,  
Cody Haugen: awesome.  
Max Kingaby: I have Pepsi down here as well. Let me just  
Edwin Johnson: Okay, these are starting to get like it's starting to pop down.  
Max Kingaby: see.  
Edwin Johnson: This is really  
Max Kingaby: Uh,  
Edwin Johnson: good.  
Max Kingaby: who do we have on here?  
   
 

### 00:27:19

   
Max Kingaby: Visa. Um,  
Kevin Murray: Yeah.  
Max Kingaby: Bud Light. I've also redesigned the actual look and feel buttons wise in this page.  
Edwin Johnson: Love  
Max Kingaby: That's what I'm going to be doing as well throughout the rest of the site, trying to just see what changes I can make to the buttons and the actual fill of the app. Um, here's the FedEx page.  
Edwin Johnson: Okay, this is f******  
Kevin Murray: Okay.  
Max Kingaby: So, so, as you can see, it's only kind of a few small changes that I've done.  
Edwin Johnson: gold.  
Max Kingaby: Um, but you can kind of see the direction we're looking to change it in. Um is MX?  
Edwin Johnson: So, did we um do we have the headers all consistency like this MX header  
Max Kingaby: Yeah.  
Edwin Johnson: stays? Do are they staying on the other slides as well or  
Brett StClair: I  
Max Kingaby: I I one will this page look the same as another page?  
Brett StClair: think  
Edwin Johnson: no?  
Max Kingaby: I we go here. Yeah.  
Brett StClair: so.  
Max Kingaby: See  
Brett StClair: You see how the header at the moment's being locked in um and the others aren't locked in. And basically to give you some options when you're talking to the guy to your advertisers, they can you can feel them out.  
   
 

### 00:28:33

   
Edwin Johnson: Yeah.  
Brett StClair: You know,  
Edwin Johnson: Yeah, that's great.  
Brett StClair: it's better to have it locked in or you happy if it scrolls through and it's a good kind of example, right?  
Edwin Johnson: Exactly.  
Brett StClair: My only worry with the bigger ad units although headers, hero headers is when they're bigger and you lock them in.  
Edwin Johnson: Yeah, you can't do that. I think it's too big.  
Brett StClair: Did you take too much screen time? Right. Screen guys. So, I've I think George and I have got a fixed a fixed stop, a hard stop on this. Um, is it okay if her son takes you through the referral stuff?  
Cody Haugen: Yeah,  
Edwin Johnson: Yes.  
Brett StClair: George, do you want  
Edwin Johnson: Beautiful work,  
Cody Haugen: absolutely.  
Brett StClair: to  
Kevin Murray: Mhm.  
Max Kingaby: Thank you guys.  
Edwin Johnson: Max.  
Max Kingaby: Appreciate it. And just so you know what my next prompt is to redesign the MX navbar  
George Westbrook: Right.  
Max Kingaby: to look a bit more like  
Edwin Johnson: Sweet. Yeah. Yeah,  
   
 

### 00:29:20

   
Max Kingaby: this.  
Edwin Johnson: that'll be great.  
Kevin Murray: Yeah.  
Edwin Johnson: Okay, how man,  
George Westbrook: Speak to you. Speak to you guys later.  
Cody Haugen: All right,  
Edwin Johnson: George. Hey,  
Kevin Murray: Take it easy  
George Westbrook: Have a good one.  
Cody Haugen: see you later.  
Edwin Johnson: have a great weekend.  
George Westbrook: Let's f****** go.  
Cody Haugen: Let's f******  
Edwin Johnson: Oh, boy. We need  
Troy McDonald Kane: Yep.  
Kevin Murray: question.  
Cody Haugen: go.  
Edwin Johnson: it.  
Hasan Mohammed Ahmed: Um hello hello. Um I'm going to share my screen. Um give me a second. Um so at the moment the the like entire thing on boarding stuff is like a bit isolated until I get everything in place everything like like hard hard like actually integrated. After that we'll actually add it into the app. But as of now, it's in the admin panel for for like just like a bit of testing and seeing how how like it works if you like apply a code. So I'll start off with a standard like sign up.  
   
 

### 00:30:11

   
Hasan Mohammed Ahmed: So, um, at the moment it's, um, I mean, because at the moment it's only going to be like a few, um, the actual fields and then until we have the, um, actual, um, as in like as soon as we have the like approval from like all of the um other other things stuff, then we'll extend onto it.  
Cody Haugen: I see.  
Hasan Mohammed Ahmed: Yeah. Yeah. The KYC and all that. we we like extend onto it and add like a few more fields.  
Cody Haugen: Yeah.  
Hasan Mohammed Ahmed: But so as of now I just do let's test test test and then for the code so how like I have it is like it's like a pre generated code. So for each user it will be like individual with each user.  
Kevin Murray: What  
Hasan Mohammed Ahmed: over there like it's not going to be anything overlap like I have already tested it for about like a billion  
Kevin Murray: happened?  
Hasan Mohammed Ahmed: users and it's all going to be individual like yeah and then I've also implemented a QR code um aspect of it the actual as in like this is only like a draft of the what's called the QR code um actual page like um I think we need to update it and make it a bit more cleaner and then add I mean a few more things onto it, but then as of now it's just like a um I said like a basic  
   
 

### 00:31:35

   
Cody Haugen: So that's what the user sees after they sign up.  
Hasan Mohammed Ahmed: page.  
Cody Haugen: That would be the next screen after, you know, they sign up KYC. That's the next screen they see.  
Hasan Mohammed Ahmed: I mean I mean like if it could be I mean I haven't um I mean I haven't really added it in yet but like it's a good point. I think like it should come up after like if you want to think show other people  
Cody Haugen: Yeah, it it should be the very next thing they see after they go through that. Um, and then the only other things that I would like to see added are the um the share buttons.  
Hasan Mohammed Ahmed: Okay. Yeah.  
Cody Haugen: So all the social um email or just uh  
Hasan Mohammed Ahmed: Yeah.  
Cody Haugen: messaging um Yep. So just the other share buttons on there.  
Hasan Mohammed Ahmed: Yeah.  
Cody Haugen: So it's a oneclick it populates basically if we can just basically share like this screen and that prepopulates in a in a in a Instagram message or a text message.  
   
 

### 00:32:26

   
Hasan Mohammed Ahmed: Yeah.  
Cody Haugen: So, it's not just text that says,  
Hasan Mohammed Ahmed: Yeah.  
Cody Haugen: "Hey, I've joined the Inplay Trading Challenge. You should, too." I mean, that's fine if that's all we can do, but I think we can do  
Hasan Mohammed Ahmed: Yeah. Yeah.  
Cody Haugen: better.  
Hasan Mohammed Ahmed: cuz like at the moment it's only I mean I mean I say like it's like a basic like um I say the implementation like we can extend onto it and then if you want to think tailor it for  
Cody Haugen: Yeah.  
Hasan Mohammed Ahmed: each like if you want to add it to each individual within platform so for for like Instagram it has a specific style for X it like it would have a style and then do like a bit of text maybe. Yeah like it's I mean I'll say it's all I say it's all I think easily impossible.  
Cody Haugen: Great.  
Hasan Mohammed Ahmed: So yeah.  
Edwin Johnson: Great stuff.  
Cody Haugen: Cool. Cool,  
Edwin Johnson: Nice  
Cody Haugen: man. That's awesome.  
   
 

### 00:33:10

   
Hasan Mohammed Ahmed: Yeah. And  
Cody Haugen: The the QR code is awesome,  
Edwin Johnson: work.  
Cody Haugen: too.  
Hasan Mohammed Ahmed: then  
Cody Haugen: Uh outside of the referral code because like multiple options and everything that that's  
Hasan Mohammed Ahmed: Yeah. Yeah.  
Cody Haugen: awesome.  
Hasan Mohammed Ahmed: I mean then like I do I mean like I do um as in I do like also then plan to add it into the um profile page as well. And so like after you can sign up if you want to go to it again and then you know open it up and then show people it's also possible like that.  
Cody Haugen: Love  
Hasan Mohammed Ahmed: So let me go back here.  
Cody Haugen: it.  
Hasan Mohammed Ahmed: So I mean let's say for example I'm a new user and this I'm use one of my example ones I used earlier. So if I get this code here I paste it in it will um create the user. Oh. Oh no man. Um I used that email already.  
   
 

### 00:33:57

   
Hasan Mohammed Ahmed: My bad. Uh should do some testing. Uh uh um uh let me try that again. So we do that if we create a user. So how like it would do it, it would then add it into the um actual I mean like it would install the individual user here as like a new entry and then it will add it into the actual um as into like a new table and so like it will track each individual um I mean each like individual like code use. So here we have where is it? Um over here and so and here's who um actually then gave it and here's who like used it as well. So yeah and then so for the actual the crediting it will only take so like it will only um actually the credit after you like approve on the here I see aspect and so at the moment it's only like like an an um I mean cuz at the moment it's only an actual an actual button but then once we have everything in place then you actually do the entire steps and then once that's all done.  
   
 

### 00:35:10

   
Hasan Mohammed Ahmed: So if I just simulate it here. So if you approve that then it will give you the um bonuses and stuff.  
Cody Haugen: And then once Yeah.  
Hasan Mohammed Ahmed: Yeah.  
Cody Haugen: And then so I'm just going back to it to make sure it's not a misstep.  
Hasan Mohammed Ahmed: Yeah.  
Cody Haugen: But so once that new user, right, like that new user used an existing referral code, people get paid their amount,  
Hasan Mohammed Ahmed: Yeah.  
Cody Haugen: but once they approve KYC, then that very next page they should see again is their own unique referral code.  
Hasan Mohammed Ahmed: Yeah.  
Cody Haugen: Just so we have that feedback loop.  
Hasan Mohammed Ahmed: I mean I mean um I could add that as well like that's also like a a a actual like extension onto what we have now.  
Cody Haugen: Yep.  
Hasan Mohammed Ahmed: So I mean I have to keep that in mind.  
Cody Haugen: Yeah, because if I if I take a sign,  
Hasan Mohammed Ahmed: Yeah.  
Cody Haugen: you know, if I take your code and I want the bonus,  
Hasan Mohammed Ahmed: Yeah.  
   
 

### 00:36:00

   
Cody Haugen: you want the bonus, I use it to sign up, but then I I want my own bonuses.  
Hasan Mohammed Ahmed: Yeah.  
Cody Haugen: So then that next page,  
Hasan Mohammed Ahmed: Yeah. Yeah.  
Cody Haugen: my you know, Cody's referral code.  
Hasan Mohammed Ahmed: Yeah. Yeah. Yeah.  
Cody Haugen: Yep.  
Hasan Mohammed Ahmed: Okay.  
Cody Haugen: Cool.  
Hasan Mohammed Ahmed: And then yeah, I think that's how it is. I mean, I might as well explain at the I mean there are also um I should boost as well and so on specifically days or like on like a specific like weekend. So like at the top here it's just um I cuz cuz at the moment it's like the kind of the preset. So before the actual start of the season, it will have these uh specific dates. If you if you want to add on to it, it's also possible and so  
Cody Haugen: Love it. Good work.  
Hasan Mohammed Ahmed: yeah,  
Edwin Johnson: It's nice work,  
Hasan Mohammed Ahmed: thank you.  
   
 

### 00:36:43

   
Edwin Johnson: Hassan.  
Hasan Mohammed Ahmed: Thank you.  
Cody Haugen: Yeah, it's it's not easy to build a whole referral system. So, I know this is awesome work,  
Hasan Mohammed Ahmed: Yeah.  
Edwin Johnson: Yeah, I mean the Max, you crushed it too today.  
Cody Haugen: dude.  
Edwin Johnson: Really fun to look at that. the app came to life with some of those images, you know, just when when do you think we can get a copy of that um to to start  
Max Kingaby: So, a copy of it um hopefully by early next week,  
Edwin Johnson: having  
Max Kingaby: But what I've given to Sky and I can share in this chat is a video I made that shows um shows you everything and how it works. Uh I'll just put that  
Cody Haugen: And then also while you're adding that Max,  
Max Kingaby: in  
Cody Haugen: I would just say send it via email as well so we can quickly find it in meetings.  
Edwin Johnson: I don't want to use the video uh coding the code the videos don't show as well.  
Cody Haugen: And so they I agree with you.  
   
 

### 00:37:40

   
Edwin Johnson: Um I'd rather use the existing UI like you know that whatever you  
Cody Haugen: Yeah.  
Edwin Johnson: guys call it I forget the so yeah um yeah the  
Cody Haugen: The PW Yep.  
Max Kingaby: Yeah. Okay. I will put  
Edwin Johnson: the sooner you you you can get that to us the better uh it it would be very helpful  
Max Kingaby: Yeah. Okay. Well,  
Troy McDonald Kane: Yeah. And the one other thing really quick,  
Max Kingaby: I  
Troy McDonald Kane: Max, too. Anything that you're sending to to Sky, can you start to send to Cody and I as well for review?  
Max Kingaby: Sure.  
Troy McDonald Kane: because it really I think we're slowing down the process a little bit by you starting with Sky and we haven't seen some of the the assets that you've created and sent to her yet.  
Max Kingaby: Okay. Yeah, totally fine.  
Troy McDonald Kane: Thank you.  
Max Kingaby: Um, I'll do tonight, this evening, wherever I get up to, um, in terms of UI design for the PWA, I will push all of the changes to George.  
   
 

### 00:38:35

   
Max Kingaby: Then when George comes in and gives you guys most updated version of the app, that will all be included. Um, and hopefully he'll do that over the weekend,  
Cody Haugen: Beautiful,  
Max Kingaby: so you'll have something to crack out next week and show all of the guys you're meeting at your sales conference.  
Cody Haugen: Max.  
Edwin Johnson: That's  
Cody Haugen: And confirming from a non tech guy, uh,  
Edwin Johnson: great.  
Cody Haugen: Ignoramus here that it'll be the same app that I have on my home screen, right? Like I don't have to redownload something to refresh it.  
Max Kingaby: Uh yeah, it should automatically update for  
Cody Haugen: Okay, great.  
Max Kingaby: you.  
Cody Haugen: I I just need to know if I do need to redownload something before Tuesday before I get in a meeting,  
Edwin Johnson: Oh,  
Cody Haugen: I'm like, "Well, f***. This isn't what I was looking  
Max Kingaby: No.  
Cody Haugen: for."  
Max Kingaby: And I'm sure sure George will give you a link just following up anyway. It'll probably be the same link,  
Cody Haugen: No.  
Max Kingaby: but I'm sure send it your way.  
   
 

### 00:39:26

   
Edwin Johnson: cool. And I have one last question for Hassan.  
Cody Haugen: Okay.  
Edwin Johnson: Um, T Hassan,  
Max Kingaby: Awesome.  
Edwin Johnson: do you feel that um the timing how do how do how do you feel timing  
Hasan Mohammed Ahmed: Yep.  
Edwin Johnson: wise? Do you feel like, you know, this referral piece is within, you know, the the goal line's close or are we still pretty far  
Hasan Mohammed Ahmed: Um I mean cuz at the moment I still need to do like a bit of work and and like a bit of  
Edwin Johnson: off?  
Hasan Mohammed Ahmed: tweaking. How I mean I mean like however like everything is like in place. So so all is is just trying to integrate into the actual thing the the um actual thing app itself.  
Edwin Johnson: Yeah. Well, because I'm basically trying to understand,  
Hasan Mohammed Ahmed: So  
Edwin Johnson: excuse me, when the app's going to be available for download, you know, forecast,  
Hasan Mohammed Ahmed: yeah, I mean because I think at the moment I'll have to speak to like I like I'll um have to speak to George  
   
 

### 00:40:13

   
Edwin Johnson: right?  
Hasan Mohammed Ahmed: as well because he needs to um have his um I mean has his actual changes as well and then after that um we'll try to give you a date.  
Edwin Johnson: Sounds great. Yeah. Um,  
Hasan Mohammed Ahmed: Yeah.  
Edwin Johnson: and and listen, we know that the app for download isn't going to be the actual inapp like Apple. It'll I think we're starting with referrals,  
Hasan Mohammed Ahmed: Thank  
Edwin Johnson: right, Cody and Troy?  
Cody Haugen: Yeah.  
Edwin Johnson: Like the first iteration doesn't have everything.  
Hasan Mohammed Ahmed: you.  
Cody Haugen: Yeah.  
Edwin Johnson: It just has the ability to get referrals,  
Troy McDonald Kane: and some data.  
Edwin Johnson: open up a wallet,  
Troy McDonald Kane: Yeah.  
Edwin Johnson: sign  
Cody Haugen: Oh, right. Right. Well,  
Edwin Johnson: up.  
Cody Haugen: it it does need some Yeah,  
Troy McDonald Kane: Yeah,  
Cody Haugen: it does need some data though, remember? Because we need some functionality.  
Edwin Johnson: Yeah. No, no. Will we have the KYC on the first iteration?  
Troy McDonald Kane: we we need it.  
   
 

### 00:40:58

   
Cody Haugen: We we need it.  
Troy McDonald Kane: Yeah.  
Cody Haugen: That's why I'm trying to Yeah,  
Troy McDonald Kane: Yeah.  
Hasan Mohammed Ahmed: Yeah.  
Cody Haugen: I'm trying to kick persona in the f****** ass. Kevin, we need to I know I pinged you off that, but or uh offline on that, but like Justin, like you were on our ass to sign the contract and now we haven't heard from you in two days.  
Kevin Murray: Yeah,  
Cody Haugen: Like be okay.  
Kevin Murray: I I picked him an email and a text this morning. Literally went.  
Cody Haugen: Beautiful. Yeah,  
Kevin Murray: So,  
Cody Haugen: we need we need to get the Novo guys those API docs.  
Kevin Murray: yep, I'm on  
Edwin Johnson: Sweet.  
Cody Haugen: Yep.  
Edwin Johnson: Okay.  
Max Kingaby: This is I've just just  
Cody Haugen: Yeah. Okay.  
Kevin Murray: it.  
Cody Haugen: So, yeah, Edwin Kyc needs to be in  
Max Kingaby: Yeah.  
Edwin Johnson: You just pushed this MX piece,  
Max Kingaby: Yeah. So,  
Edwin Johnson: Max.  
Max Kingaby: this is now the new banner that will come across all of the game screen.  
   
 

### 00:41:30

   
Cody Haugen: there.  
Edwin Johnson: Ah,  
Max Kingaby: So which one you could come up  
Edwin Johnson: so good. Yeah, so good. I mean, it's really, really good because when I look at this screen, guys,  
Max Kingaby: here?  
Hasan Mohammed Ahmed: Sorry.  
Edwin Johnson: I don't feel like I'm getting pounded in the face with an  
Troy McDonald Kane: No,  
Edwin Johnson: ad.  
Cody Haugen: Not at all.  
Kevin Murray: Oh yeah.  
Troy McDonald Kane: it's very elegant is the best way to describe it.  
Cody Haugen: Yes.  
Troy McDonald Kane: It is it's it's I'm sure you guys have all been on a lot of apps where it's like floating around  
Kevin Murray: Yeah.  
Edwin Johnson: Cool.  
Troy McDonald Kane: on the screen and following you and it's always annoying because it's then and then it overlaps with text sometimes. Like the way you guys have designed it is very elegant and very, you know, not in your face.  
Max Kingaby: Thank you  
Edwin Johnson: Awesome. Listen, you boys have a great weekend.  
Max Kingaby: guys.  
Cody Haugen: Yes.  
Edwin Johnson: Thank you so much for everything.  
Cody Haugen: Thank you guys.  
Troy McDonald Kane: Thank you.  
Cody Haugen: Really appreciate all your hard work.  
Edwin Johnson: Yeah.  
Kevin Murray: Great job,  
Edwin Johnson: Thank you very much.  
Kevin Murray: guys.  
Troy McDonald Kane: Cheers. Have a good weekend.  
Kevin Murray: Love them.  
Hasan Mohammed Ahmed: Yep.  
Cody Haugen: All right,  
Max Kingaby: You just  
Troy McDonald Kane: Bye.  
Cody Haugen: we'll talk to you.  
Edwin Johnson: We'll see you guys in a few.  
Cody Haugen: Bye bye.  
Hasan Mohammed Ahmed: Yep.  
   
 

### Transcription ended after 00:42:33

  

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.

**