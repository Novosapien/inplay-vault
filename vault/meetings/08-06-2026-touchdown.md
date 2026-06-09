---
date: 2026-06-08
type: standup
status: extracted
extracted-to:
  - "[[digests/touchdowns-01-08-jun-2026]]"
  - "[[information-layer/information-layer]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[inplay-global-website/inplay-global-website]]"
  - "[[architecture/open-questions]]"
---

## Post-Call Analysis

> Processed as part of the **[[digests/touchdowns-01-08-jun-2026|1–8 June touchdown sweep]]**.

| Finding | Destination | Action |
|---------|-------------|--------|
| **Internal creative tooling — CI-aware deck/creative skill + approved-image repository + ~1h training** | digest (cross-cutting) | New internal tooling — noted |
| **Agentic outreach at scale** (package messaging/imagery/email/deck per prospect) | digest (cross-cutting) | New internal tooling — noted |
| **Market-making algorithm** — Edwin wants to co-build over ~2 months | [[architecture/open-questions]] | Row added — flagged for own session |
| Onboarding flow built into app (placeholder KYC); awaiting Persona API keys | [[customer-onboarding/customer-onboarding]] | Delivery note updated |
| Persona speed validated (~99.5% AI-automated, seconds) | [[customer-onboarding/customer-onboarding]] | Delivery note updated |
| Sport Radar live (fixed 2025); moments → popup; ~18 moments/game validated; group by quarter | [[information-layer/information-layer]] | Touchdown note added |
| SR entity-ID join (play-by-play / AP / headshots / win-prob); injury AP context on player cards; win-prob under global AmFootball API | [[information-layer/information-layer]] | Touchdown note added |
| Team page — current + previous season only | [[information-layer/information-layer]] | Touchdown note added |
| Demo on mock-data branch (moving/production-like data) for the sales conference | [[information-layer/information-layer]] | Touchdown note added |
| Website published before Tuesday; outline font fixed, headshots cropped; **Career tab** (VP of Technology) | [[inplay-global-website/inplay-global-website]] | Update block + Page Map updated |
| Apple dev verification still pending (ticket raised); Google Play verification steps | [[customer-onboarding/customer-onboarding]] | Delivery note updated |

---

**

Jun 8, 2026

## InPlay Digital TouchDown - Transcript

### 00:00:01

  

George Westbrook: Ah, that even does it for mine as well. Wait, wait, wait, wait.

Brett StClair: Why is there an echo?

George Westbrook: Hear me.

Brett StClair: No.

George Westbrook: Hello. Hello.

Max Kingaby: retry.

George Westbrook: Hello.

Brett StClair: That's better.

Max Kingaby: He's nuts.

Brett StClair: This is where it's going to be interesting.

George Westbrook: Hello.

Brett StClair: Worked.

George Westbrook: Can anyone hear me?

Brett StClair: I'm going to let you run in.

Max Kingaby: No.

Brett StClair: You ready? People are coming in.

Max Kingaby: says no one

Brett StClair: Hello. Hello everybody.

Edwin Johnson: warning

Brett StClair: Morning.

Cody Haugen: Good

Edwin Johnson: off

Brett StClair: How?

Cody Haugen: morning.

Brett StClair: How was everyone's weekend?

Edwin Johnson: long.

Skye Capazorio: Hi everyone.

Cody Haugen: Good

Max Kingaby: Thank you.

Brett StClair: Good morning.

Troy McDonald Kane: Morning. Good

Cody Haugen: morning.

Brett StClair: Yeah, I

Edwin Johnson: Brett, did you Brett,

Brett StClair: suppose

Edwin Johnson: did you were you able to confirm that you made uh the wire got the money

Troy McDonald Kane: afternoon.

Edwin Johnson: properly?

Brett StClair: um I can confirm not yet, but that could be the UK side.

  
  

### 00:01:18

  

Edwin Johnson: Okay. Okay. Because I've got to confirm, but like with that trip XX you gave me on the last part of the routing, I just want to double check.

Brett StClair: Yeah,

Edwin Johnson: Okay.

Brett StClair: I think I gave you the trip XX last time. It's It's code.

Edwin Johnson: Okay.

Brett StClair: Yeah, it's

Edwin Johnson: Yeah. Yeah. Okay. It it seemed weird.

Brett StClair: XX

Edwin Johnson: I mean, generally when I think Triple X, I think Troy King.

Troy McDonald Kane: I don't know. I don't know how to I don't know how to take that.

Brett StClair: Troy.

Troy McDonald Kane: If that's

Edwin Johnson: It's a compliment.

Troy McDonald Kane: a

Edwin Johnson: I mean, I mean, I would have said Hassan, but I don't want to get beat up when I come to London. All right, George, thanks for getting me those uh assets right away over the weekend. Very helpful for what I was doing. I spent about six hours trying to build a team page in our deck for one of our people we're meeting.

  
  

### 00:02:08

  

Edwin Johnson: Um, and the AI is just absolutely horrendous.

George Westbrook: That's okay.

Edwin Johnson: I mean,

George Westbrook: Yeah.

Edwin Johnson: I I got to send there's one slide where it changed everyone's picture and it's unreal. It's I got to show that to everyone because it's like Sky, you look like I mean I look like I'm 78 years old.

Skye Capazorio: I look like the Cookie

Edwin Johnson: I mean,

Skye Capazorio: Monster.

Edwin Johnson: you look like, you know, like someone who might make a lot of money as a dominatrix.

Max Kingaby: Thanks.

George Westbrook: Hey,

Edwin Johnson: Let's put it that way.

Skye Capazorio: Oh,

Edwin Johnson: I mean,

Skye Capazorio: great.

Edwin Johnson: I think AI just went ham on

Skye Capazorio: I mean, that could be helpful. Maybe like,

Edwin Johnson: this.

Skye Capazorio: you know, we should put like hobbies underneath our names for the weekends and see if that's

George Westbrook: Did you put it in the prompt,

Edwin Johnson: Well, you know, I will tell you this.

Skye Capazorio: persuasive.

Edwin Johnson: I sent a resume once and you know they put like hobbies and I put you know long walks on the

  
  

### 00:02:47

  

George Westbrook: Edwin?

Edwin Johnson: beach, puppies and my safe word is like Oklahoma and I never heard back on that.

Troy McDonald Kane: What year was that?

Edwin Johnson: That was three weeks

Troy McDonald Kane: Just curious.

Brett StClair: Yeah.

Edwin Johnson: ago.

Brett StClair: George, did you say did you send

Skye Capazorio: I mean, if I read a CV like that, I'd actually have quite a giggle.

Brett StClair: Edmond?

Skye Capazorio: I'd think that the person had a great sense of humor,

Troy McDonald Kane: I agree.

Skye Capazorio: but

Troy McDonald Kane: I would want to at least interview them to

Skye Capazorio: 100%.

Troy McDonald Kane: understand

Edwin Johnson: Well, there you go. When When we're all out of work, start with the safe word.

Troy McDonald Kane: Oklahoma. Well, now I know what to say going forward.

Edwin Johnson: Yeah. Well, it's changed now. It's like my password. I got to update it.

Skye Capazorio: It's

Edwin Johnson: Now my safe word is Troy is awesome.

Troy McDonald Kane: That's right. Is awesome.

Edwin Johnson: Kevin, are you back?

  
  

### 00:03:46

  

Troy McDonald Kane: Oh

Kevin Murray: Yeah.

Edwin Johnson: Are you back for me?

Kevin Murray: Yeah.

Edwin Johnson: Cool. Cool.

Troy McDonald Kane: man.

Kevin Murray: Yeah.

Edwin Johnson: All right, boys. I'll let you run the show. Brett and the St. Clair crowd.

Brett StClair: Quick one, George. Did you say you sent Edwin a prompt, system prompt to help him with that stuff?

George Westbrook: No, no, it was the the actual

Brett StClair: Should we see if we can generate

George Westbrook: images.

Brett StClair: just for the team to be generating this kind of content a system prompt of some sort at a minimum or a skill that they can use where we've incorporated all the CI all the learnings and knowledge base just to help you

Edwin Johnson: Well,

Brett StClair: guys

Edwin Johnson: it's funny you say that because I spent 36 hours in the last three days on a deck.

George Westbrook: What's

Edwin Johnson: That's horrendous. All right. It's okay. I mean, the colors are It doesn't look

George Westbrook: that?

Cody Haugen: It's it's it's not horrendous.

  
  

### 00:04:36

  

Edwin Johnson: great.

Cody Haugen: You're being too hard on yourself again. Um, but the answer,

Edwin Johnson: Well,

Cody Haugen: Brett, is 100%. It should not fall on Edwin to spend any amount of time building a deck. I was about to tell him I'm gonna go old school and open PowerPoint and and just build a deck the old way, but uh if there is a quicker way that can have all of our information that a repository that we can draw on. Yes. Let's have the team use the technology as a friend, not a foe, and and build something that we could all spit out our own decks in a matter of short

Edwin Johnson: Yeah.

Cody Haugen: time.

Brett StClair: And then I'm thinking it's like an hour training session to teach you guys some best practice

George Westbrook: Hoodie.

Brett StClair: around it.

Skye Capazorio: Also,

Cody Haugen: Yeah.

Skye Capazorio: sorry, just to add so sorry, go ahead,

Edwin Johnson: Go ahead.

Skye Capazorio: Edwin. I was going to say that when Max and I were working through the website last week,

  
  

### 00:05:25

  

Edwin Johnson: No.

Skye Capazorio: um, one of the things obviously that he was doing was doing the images, rendering the images and then putting the images in and then asking it to overlay the copy over that. If we have a database of images that we that we all really like that so Edwin likes the ones with you know the the candlesticks and the train going up and the field at the base like Troy I know there it's in our the LinkedIn banners there's all those various different visuals if we have those as a standard repository of just a whole bunch of just images then those can easily I find correct me if I'm wrong that if I feed an example image into into GPT or whatever. It's better at taking that and creating a lookalike that runs through seamlessly if we if we have those elements as well as overlaying the

Edwin Johnson: That makes sense to me.

Skye Capazorio: information.

Edwin Johnson: I mean, we we So, over the last few days, what I've been doing is I've been attacking all these liquor brands around the country and all these different wine makers trying to like connect.

  
  

### 00:06:33

  

Edwin Johnson: And what I want to try to do is basically when I've gotten probably four responses who had some interest in, you know, having a conversation, whatever. Um, you know, we we probably need just like a standard like automatic like put their logo in however we're going to do it, you know, just ship it out. I used to be a uh I'll take it down memory lane real quick. I was a, you know, a very large illegal sports bookmaker in Chicago and I got in trouble in 1995, 31 years ago. And um after I got in trouble, I had to actually go into the real workforce. And because I had made all these like um betting journals that I would would distribute, I had to learn how to become a graphic designer really quick. Um, and so I went to work at this company, a sign company that that um, you know, could I work basically at night um, and I would design the the buildings are going to make with the sign so they could get a permit. Um, but yeah,

  
  

### 00:07:38

  

Troy McDonald Kane: Thanks.

Edwin Johnson: I mean, so basically what I found was I ended up being in charge of a program that did like 5,000 locations for an investment company called Edward Jones. And what I did was um you know kind of like what you're saying Sky we had the signs were in a repository and then we'd go I'd hire someone to go take a picture of a building then I would put the sign p the sign on the picture of the building make an image so I could take it to the whatever village or town to get a permit and then then they would get that permit approved I would have it build ship all that s***. Anyways, um so I have some experience with that. Um you know, not intentionally, just kind of as the way it goes. Um but I think we need to like, you know, whenever we would try to sell a company on something new, we'd always just incorporate their logo into whatever we were going to show them.

Skye Capazorio: Excellent.

Edwin Johnson: And then ultimately, like, you know, I got tired of that and I I started a company on my own.

  
  

### 00:08:33

  

Edwin Johnson: I would drive around at night and find signs that were not lit up. And then the next morning I would like either drop off a picture or an email of the that sign lit up with a picture. So I would basically, you know, put the logos on it as a sales piece and it always worked. Like I I actually made a ton of money doing that too.

Brett StClair: Yeah,

Edwin Johnson: Like I was I was on hard times after the big bust. So you know it it it I made a lot of money really quickly.

Brett StClair: nice.

Edwin Johnson: is um so anyways um so the more we can do that the other thing I wanted to ask the group the agentic team is um you know over the next two months I actually have to build a marketmaking algorithm okay and the marketmaking algorithm is I

Skye Capazorio: Okay.

Edwin Johnson: have one built um but it was built for the Xperry platform so some of the polls and things are going to be slightly different I would like to explore us building one together.

  
  

### 00:09:29

  

Edwin Johnson: Um, you know, uh, and and maybe we could,

Skye Capazorio: All

Edwin Johnson: you know, add that to the list of criteria.

Brett StClair: Beautiful.

Edwin Johnson: It's it'll be a fun exercise because if, by the way, that that the thing we're going to build, we could probably put in any market and actually make money.

Brett StClair: Yeah.

Edwin Johnson: It's interesting. Cool. All right. You're in charge,

Brett StClair: Yeah.

Edwin Johnson: Brett. What else?

Brett StClair: So,

Edwin Johnson: What do you got?

Brett StClair: um, if you're doing outreach like that,

Skye Capazorio: right.

Brett StClair: um, can I make it a yes that we're going to go and do the agentic outreach as well? So, what the agentic outreach will do is it can package stuff at scale.

Skye Capazorio: Okay.

Brett StClair: So, put the right messaging, put the right imagery, package in everything you need like that a lot better. Are you open to having a look at how that works? We'll do it with the agencies and you can see some of the output.

  
  

### 00:10:16

  

Edwin Johnson: really.

Brett StClair: We'll like tag you in so you can see how it actually pulls together. Um, and it does things like that. If we want to send it like a nicely formatted email with the logo on it kind of thing

Skye Capazorio: That's something.

Brett StClair: or an attach deck and tweak it, it can do that. Um, and it just does it at scale. So you don't have that, you know, wherever you do that repetitive human task. You know, it's nice to do the beginning by yourself to figure out is this a market? Is that the right thing? You know,

Skye Capazorio: I think

Brett StClair: this that thinking engaging the brain. Yeah. Yeah, that feels right. Okay, cool. Cool. I'm getting my messaging right.

Skye Capazorio: that's

Brett StClair: But it's another thing taking that learning, feeding it into the agentic stack and letting it double down for you.

Edwin Johnson: Oh. Okay. I mean, I'm down to try. I don't have a lot of confidence in it,

  
  

### 00:11:07

  

Brett StClair: Let's do it.

Edwin Johnson: but I am down to

Brett StClair: Yeah, I think that's the right approach.

Edwin Johnson: try.

Brett StClair: That's the perfect approach. Don't have the confidence. Let this engine go do it and let it surprise you. Um then George is it shouldn't be too much of an effort to get some kind of whether it's system prompt or a couple of skills to help the team with um their creative challenges. Especially if we create a repository of some sort of all the imagery that we're using.

George Westbrook: the the pulling in the images. Yes, that will be the getting the images and putting them in a place. Not so much. That's just a bit more manual. Okay, I want this image. I want that image. Um the visual style. Yeah, there's very very doable. I wouldn't say I wouldn't say easy in like it's a 20-minute job,

Skye Capazorio: That's

George Westbrook: but it's very very

Skye Capazorio: all.

Brett StClair: Okay, let's have a look at putting some time.

  
  

### 00:12:05

  

Brett StClair: It just helped like out of the thought of you,

George Westbrook: doable.

Brett StClair: Edwin, spending that much time on a deck. Um, it's not a good use of your time. So, let's let's make sure that we give you the tooling that gives you a far better conversion rate, right? and then the whole team can can use that.

Edwin Johnson: for sure.

Brett StClair: Um, we'll have a look at that. Max, you and I could probably look at putting that together.

Edwin Johnson: Cool.

Brett StClair: Awesome. Um, let's get into it. So, this week we want to get something up and running. Referrals with loginins or Thank you very much, Kev. Did you you sent through the um Persona APIs? Um Hassan, you'll get on to that and start uh testing,

Kevin Murray: Yeah.

Brett StClair: investigate, making sure we got access, plugging into the necessary admin dashboard and stuff.

George Westbrook: Yeah. So I'm

Hasan Mohammed Ahmed: Um yeah so um at the moment I'm just doing the whole entire I think onboarding flow.

  
  

### 00:13:05

  

Hasan Mohammed Ahmed: So it's until we we actually have the um API keys after that we can implement it into the the onboarding flow itself.

Brett StClair: So, we need API keys still. Hey, Kev, have you been able to get hold of that?

Kevin Murray: Okay,

Hasan Mohammed Ahmed: Yeah.

Kevin Murray: I'll chase that up

Brett StClair: Brilliant. Brilliant.

Kevin Murray: today.

Troy McDonald Kane: And then what do you need from I I saw your email around the the uh Google

Brett StClair: Um

Troy McDonald Kane: Play Store. What do you need from us? You need access to a inplay domain or ex I wanted to just wait for this call to find out exactly what we need to set up for you.

Brett StClair: So,

Hasan Mohammed Ahmed: So yeah,

Brett StClair: yeah, I'll go for

Hasan Mohammed Ahmed: so um on the Play Store um actual console um I forgot exactly where it

Brett StClair: it.

Hasan Mohammed Ahmed: was, but there actually are like a few things steps that um have be done and then after that we we can can actually upload like a test app and then see how it works on the actual um play store itself.

  
  

### 00:14:06

  

Hasan Mohammed Ahmed: Um so to um actually then do that I need to have um I mean I believe it's the owner um access as in I can't actually do anything only on um admin access. So,

Brett StClair: Do you want to talk Cody or Troy through it after this call?

Cody Haugen: Yeah.

Hasan Mohammed Ahmed: um,

Cody Haugen: So,

Hasan Mohammed Ahmed: yeah, sure. I can do

Cody Haugen: yeah, I mean it's it's it's verify your identity like as a human,

Hasan Mohammed Ahmed: that.

Cody Haugen: Troy. Uh verify our organization's website and then verify the phone numbers. That's the three things that I'm seeing on the the verification from the company side.

Troy McDonald Kane: Okay, we can we do it through the app development atplay global.com

Cody Haugen: Um, yeah, I think based on this identity, it has to be an actual document.

Troy McDonald Kane: email.

Cody Haugen: I don't know if that's driver's license, but we can we can figure that out.

Skye Capazorio: Exactly.

Cody Haugen: Um, but yeah, I can I can look into that and get you a list of exact things here.

  
  

### 00:15:06

  

Troy McDonald Kane: And then Apple called you yet,

Cody Haugen: Yeah.

Troy McDonald Kane: Edwin, for the app for the Apple store or gotten any verification contact from them?

Edwin Johnson: No, no, no, nothing from

Cody Haugen: He sounds okay.

Edwin Johnson: them.

Cody Haugen: Um I'll I'll write them a ticket in their little developer portal.

Troy McDonald Kane: Okay.

Cody Haugen: Um right now

Brett StClair: Um, and then George, you've had some more progress on sports radar. Do you want to take the guys through

George Westbrook: Yeah. So,

Brett StClair: it?

George Westbrook: I suppose we'll do I suppose there's three Yeah. three things. There's the sports radar data. Um, that's all that's all live. Sorting out some issues with that. I think I mentioned this last week. It's fixed to 2025 at the moment. So,

Skye Capazorio: I'm

George Westbrook: we actually see data, but it's got all the results from 2025.

Skye Capazorio: sorry.

George Westbrook: all of the moments for every single game that happened in 2025 linked up to a a popup.

  
  

### 00:16:03

  

George Westbrook: So, people go in, they can replay a game, they're going to see I I'll just pull this up rather than me explaining it. There we go. So, yeah, this is this is 2025. Obviously, these are all the completed ones. They haven't got the changes that Max has already put in.

Skye Capazorio: That's

George Westbrook: Um,

Skye Capazorio: what

George Westbrook: so you come to a game, can click on a moment, go through all of the moments that happened within that game.

Edwin Johnson: Oh man, that's f******

George Westbrook: Um, then is there anything here? No,

Edwin Johnson: awesome.

George Westbrook: this is the the market one. Um, so obviously all the moments are here as well. I think in terms of UX, we probably want to change this a bit because it's quite quite overwhelming.

Skye Capazorio: Okay.

George Westbrook: The scoring, the scoring drives, the the season.

Edwin Johnson: George, real quick. Sorry to interrupt you. George,

George Westbrook: That's

Edwin Johnson: do you know roughly Do you know roughly how many on average of those little dots occur per

  
  

### 00:17:03

  

George Westbrook: right.

Edwin Johnson: game?

George Westbrook: No, but I can.

Edwin Johnson: Nothing.

George Westbrook: So there there's varying degrees of granularity we can go into. Like I think this was one of the games I was looking at. At the moment eight there's 18 which is an okay amount. Um because I think it can go up to like 170 different moments which I mean obviously from the perspective of advertisers amazingund 170 different moments but a

Skye Capazorio: contact.

George Westbrook: user is not going to look through them and it's just in my opinion it's going to be diluted um where they're just not going to use

Skye Capazorio: Okay.

Edwin Johnson: No, that that 18 validate that I'm sorry to interrupt you.

George Westbrook: that.

Edwin Johnson: That 18 validates Cody's and my premise that there's roughly 15 to 20 per game, which is what we want to highlight on

George Westbrook: Yeah, I see that's 18.

Edwin Johnson: average.

Skye Capazorio: a question just about how those moment the brand ownership of those moments come up.

George Westbrook: That's

Skye Capazorio: Uh Cody, I think we spoke about this in terms of how that shows up and and the frequency.

  
  

### 00:18:04

  

Skye Capazorio: We're fine with the frequency that they will show up or how long they'll be on the screen to not overlap significantly to the point that you can't see then what's actually going on with the movement on the field.

Edwin Johnson: That won't happen because every that's impossible because even when they like say there's a

Cody Haugen: Yeah.

Skye Capazorio: Okay.

Brett StClair: Okay.

Edwin Johnson: turnover um it takes time for the team to line up. There's, you know, seconds in between they snap the next play.

Skye Capazorio: Yeah.

Edwin Johnson: You know,

Skye Capazorio: Oh, all good.

Edwin Johnson: that's Jeez

George Westbrook: Um then what else is there? The

Edwin Johnson: Louise.

Cody Haugen: uh going back George sorry just real quick a little feedback for you you know that where

George Westbrook: think.

Cody Haugen: it's had all those moments just in a line and how you said you wanted to clean it up yeah

George Westbrook: Yep.

Cody Haugen: just put them in quarters up so right above that it click first quarter second quarter third quarter fourth quarter and then it'll shorten it obviously and then the user can select which

  
  

### 00:18:56

  

Skye Capazorio: What's

Edwin Johnson: Cool.

George Westbrook: Yeah.

Skye Capazorio: that?

Cody Haugen: quarter.

George Westbrook: Okay. Yeah, that makes a lot of

Cody Haugen: Yeah, that's that's what they do in the the like hosted uh playbyplay uh

George Westbrook: sense.

Cody Haugen: widget and it it cleans it up real

Skye Capazorio: b****.

Edwin Johnson: Wow,

Cody Haugen: nice.

George Westbrook: Um,

Edwin Johnson: that's awesome.

George Westbrook: yeah, win probability as well. And then I think the team page has got a fair bit more detail as well. I think if we go back to this one.

Skye Capazorio: Okay.

George Westbrook: So yeah, all the seasons I think I mentioned this last week. All the season stats are there. The conferences, all of the results are now there as well. So you can look back at all of the results. And maybe we want to think,

Edwin Johnson: Only

George Westbrook: do we want to show say maybe 2024 as well or do we only want to show current season and previous season?

Cody Haugen: Yep. Only only one is

  
  

### 00:19:49

  

Edwin Johnson: one's

George Westbrook: Okay.

Cody Haugen: enough.

George Westbrook: um injury reports as well.

Edwin Johnson: enough.

George Westbrook: Like these are from week 10 of 2025, the actual injury reports. Once again, click into click into the

Cody Haugen: So, if idea on the injury report there, George, if you click into an injury,

George Westbrook: players.

Cody Haugen: um, is there something from the AP uh, editorial newswire that we licensed from Sport Radar that you can bring in as far as an article that says, you know, it's an ankle and he's questionable for two to four weeks, possibly back in the sixth week, something along those lines. uh just bringing in more context around that injury. Injuries are going to be huge thing people trade on like cannot minimize that

George Westbrook: Yeah. Yeah. Cuz I think the what what we'd need to check is when a news article comes

Cody Haugen: enough

George Westbrook: through, is it linked to a specific entity, be that a team or a player? I'm assuming it's linked to a team. Um,

  
  

### 00:20:49

  

Cody Haugen: it it will have both of those IDs. So yeah, so if you have Bo Nick's um player card,

George Westbrook: okay.

Cody Haugen: let's say if you clicked on Bon Knicks right there,

Skye Capazorio: I'm

Cody Haugen: Sport Radar's ID will be that Sport Radar ID will be the same ID across the AP

Skye Capazorio: sorry.

Cody Haugen: Newswe um his head shot if we ever brought in head shot. All the products that Sport Radar licenses all tie back to the Sport Radar ID.

George Westbrook: Can we put in the head shot? Is that Is that all good?

Cody Haugen: It's not it's not a product we have licensed, but yes, eventually yes,

George Westbrook: Okay,

Cody Haugen: we

George Westbrook: that was one thing as well.

Cody Haugen: could.

George Westbrook: The the in-game probabilities. Do we do we have the license for that at the moment?

Cody Haugen: Yeah. The win probabilities.

George Westbrook: Okay.

Cody Haugen: Yes.

George Westbrook: Yeah, because it's I'm not sure. I remember I was getting a um access deny or 403 error for that.

  
  

### 00:21:42

  

George Westbrook: So, I'll need to I need to double check that cuz that might just be

Cody Haugen: They are they are under the global American football API, not the NFL API, but those IDs will talk to each other.

George Westbrook: Okay.

Cody Haugen: So, just make sure you are looking in the same API and if you do have an issue, then copy me on an email to supportsportraar.com and we'll get it sorted.

George Westbrook: Okay, perfect. Um, I think Hassan,

Cody Haugen: We do currently, yeah, we we do have them in our contract.

George Westbrook: you've got cuz that's that's what I thought cuz I I remember I remember us

Skye Capazorio: That's

George Westbrook: talking about so when it was when it was getting denied. I think I was I was a bit bit confused.

Skye Capazorio: f******

George Westbrook: Um, do you want to bring up the referral and login stuff?

Edwin Johnson: before or while he does. George, when do you think you'll have the uh I forget what you guys call the the demo um with the updated ad placements?

Cody Haugen: everywhere.

George Westbrook: Um, you said you needed by Tuesday, didn't you?

  
  

### 00:22:39

  

Edwin Johnson: Yes,

Skye Capazorio: Okay.

Edwin Johnson: sir.

George Westbrook: Okay. So, um,

Brett StClair: You need to manually stitch those in. Hey, is that

George Westbrook: no, no.

Brett StClair: your

George Westbrook: So what what we'll do is so I'm on my branch, Max's on his branch for the ads.

Brett StClair: Yeah.

George Westbrook: will push the push Max's branch to main or have a separate deployment and then surface that

Skye Capazorio: It's not

George Westbrook: one in the URL because the issue I think we mentioned this last week is with with this one that I'm working on obviously it's on the the sports like the official sports radar API so it's going to look incomplete whereas we if we use the mock data it's going to look exactly like it would look

Skye Capazorio: That's

George Westbrook: in in like three or four months time um where it's got the in-game it's

Skye Capazorio: not

George Westbrook: got the price update It's got no demo demo data labels. Um, and obviously the updated ad units as well.

Edwin Johnson: I think that's the one we like,

Brett StClair: Perfect.

  
  

### 00:23:34

  

Edwin Johnson: right?

Cody Haugen: Yeah. Yeah. We We need to have moving data if we're going to be demoing

Brett StClair: Yeah.

Cody Haugen: it.

Hasan Mohammed Ahmed: Hello. Um yeah, is that a to see my screen?

Brett StClair: Yep.

Hasan Mohammed Ahmed: Yeah.

Cody Haugen: Yep.

Edwin Johnson: Yes.

Hasan Mohammed Ahmed: So for the like entire think onboarding um flow that that like I mean like I think had on the admin panel I did um implement it into the actual application itself.

Skye Capazorio: I don't see

Hasan Mohammed Ahmed: So I mean at the moment these are all like I mean like placeholders and so if nothing change the I mean the the the actual page and you know like add like extra stuff to it and make it like a bit nicer like yeah it's possible but so at the moment if we create account um I mean on here this is just a placeholder too. I'll just um enter some fake details. Uh just do this for now. And then over here then there is like an extra option for if you want to enter like an an actual code um for like example off of like a friend or something.

  
  

### 00:24:49

  

Hasan Mohammed Ahmed: And so yeah, if you go to create account um this might take a second. Let me check if it's loading. Yeah. And so um and so then over here like it'll be the actual ID check. Um at the moment it's only like a as in it's only like a placeholder. So like it's not like actually the functional yet. So until everything's in place. So then it will take you onto that screen and then you you do the whole ID check. And once you do that, so at the moment it will just take you through. So then once you do that and you're like approved,

Edwin Johnson: Cool.

Hasan Mohammed Ahmed: it will then show you a screen with your QR code as well. And so if you want other people to then scan the code and then if you want to copy it as well and then upload it onto like any other platforms um I mean ideally um I would add in like a few extra than deep links or like X um Instagram and so then if you think directly share it onto those um I mean external platforms is also the possible and then yeah so if you do this it should just like to enter the

  
  

### 00:25:51

  

Hasan Mohammed Ahmed: app and so yeah I um like it's an actual onboarding flow. So it's Yeah. So it's just like A to B to C is you know um quite straightforward on how everything flows through. Um

Edwin Johnson: That's really good.

Hasan Mohammed Ahmed: I

Edwin Johnson: How do how long do you think it would take a person to log in, you know, sign up?

Hasan Mohammed Ahmed: um I mean I think it's up to the um I think it's up to the actual

Edwin Johnson: Sure.

Hasan Mohammed Ahmed: like approval thing and so for the KYC um like it's up to that thing how long like it takes for them to approve it.

Edwin Johnson: Cody,

Hasan Mohammed Ahmed: And so that's the main hitch.

Edwin Johnson: how long do you think,

Hasan Mohammed Ahmed: Yeah.

Edwin Johnson: Kevin? Kevin,

Cody Haugen: Yeah.

Edwin Johnson: how long do we expect Persona to take to

Cody Haugen: So, it's it's automated.

Edwin Johnson: approve?

Cody Haugen: So, it's it's for a government ID, it's like 99.5% automated by AI.

Skye Capazorio: See you soon.

  
  

### 00:26:45

  

Cody Haugen: Um, and so it should be seconds for for for it

Edwin Johnson: Okay. Wow, that's awesome.

Cody Haugen: to approve because all Yeah,

Edwin Johnson: Yeah. Yeah.

Cody Haugen: it's Yeah.

Edwin Johnson: The photo.

Cody Haugen: the the photo in your in your face scan to make sure that it matches.

Edwin Johnson: Yep.

Cody Haugen: Yep.

Edwin Johnson: Really

Cody Haugen: So, like like I said before,

Edwin Johnson: cool.

Cody Haugen: when I've used Persona, um the the longest time in the signup process is walking from my couch to the kitchen to go get my ID. Like that's it. It literally takes,

Kevin Murray: Yeah.

Cody Haugen: you know, less than a a minute or

Kevin Murray: Yeah. Couple of seconds when we did the demo.

Edwin Johnson: Right.

Kevin Murray: It was really quick.

Edwin Johnson: That's great.

Cody Haugen: two.

Edwin Johnson: Cool. Nice work. On that welcome page, you're going to put something graphically, right? That's a little bit more dynamic.

Brett StClair: We let Max's s******* go solve the

Edwin Johnson: I mean, right now,

  
  

### 00:27:37

  

Hasan Mohammed Ahmed: Yeah.

Edwin Johnson: Max never looks sexier with that pouty little face on right now.

Brett StClair: problem.

Edwin Johnson: I mean, happy Monday, Max. I mean, what the f***? Um, all right. Yeah. No,

Max Kingaby: It's it's the it's the it's the makeup routine.

Edwin Johnson: great.

Hasan Mohammed Ahmed: It's the It's my

Skye Capazorio: I felt

Edwin Johnson: I see.

Skye Capazorio: like

Edwin Johnson: I see. Awesome.

Brett StClair: So

Edwin Johnson: All right.

Hasan Mohammed Ahmed: Actually,

Brett StClair: yeah.

Edwin Johnson: What What else you got for us today, Brett? Anything else?

Cody Haugen: I have a question.

Edwin Johnson: Go ahead.

Cody Haugen: Yeah. Uh website we still on

Brett StClair: Yeah.

Troy McDonald Kane: Yeah, I was about to say I looked at the updates over the weekend. Uh, and they look a lot better after our comments last week. So, thank you for getting that done. It's much bolder on the outline for the orange really stands out a lot better now. And the way you cropped the pictures looks good on the team page.

  
  

### 00:28:23

  

Troy McDonald Kane: So, I I mean, I think it's good to at least at this stage publish. I don't know if anyone else has any other feedback or edits that they want. Oh, the we need to make sure the career tab is at the top. It's the one thing I noticed wasn't there yet. uh so that we can start giving you job postings to put on there that we

Skye Capazorio: So Troy just to answer you Max and I I think we spent about 5 hours on Friday morning going through

Troy McDonald Kane: have

Skye Capazorio: making all those refinements like on the screen one to one and I've got another session with Max now um later this afternoon this evening our time um to continue that refinement um so if you can let us just do that round of refinement and then we'll share that and then um if we're happy with that to go live with that but then I still think I think there'll still be more refinements for us to make in the background but if we can publish it as that then I think that's that's

  
  

### 00:29:16

  

Troy McDonald Kane: Okay, great. And I can send you, if we haven't done already, the first job posting we have, which is for tech VP of technology to put on there. And then I did send them all the DLS for all of the groups on where they should be pointing to inplay global emails.

Skye Capazorio: do that. Thank

Edwin Johnson: Cool.

Skye Capazorio: you.

Edwin Johnson: Anything else today?

Troy McDonald Kane: Yeah.

Edwin Johnson: Awesome.

George Westbrook: I think that's

Edwin Johnson: Great work, everybody. Uh Brett, just when you can just confirm that you got the cash,

George Westbrook: everything.

Edwin Johnson: so I'm not worried about it.

Brett StClair: No worries.

Edwin Johnson: Okay.

Brett StClair: We'll let you know. Thank

Edwin Johnson: Yep. No problem.

Brett StClair: you.

Edwin Johnson: Look forward to seeing you guys on Yeah. Wednesday.

Brett StClair: Good luck with your show.

Edwin Johnson: Let's hope we're live.

Brett StClair: Good luck with the show,

Edwin Johnson: Um,

Brett StClair: guys.

Edwin Johnson: Cody, myself,

Cody Haugen: All

Edwin Johnson: Kevin, and Tony Berbillis are heading down tomorrow.

  
  

### 00:30:02

  

Edwin Johnson: And, uh, you know that Miami, you never win. Nobody wins. We take them on every time, but we never win. All right. Have have a wonderful day. Thank you so much. We'll look forward to talking soon.

Cody Haugen: right,

George Westbrook: So,

Max Kingaby: Hey guys,

Skye Capazorio: Thank

Cody Haugen: talk soon.

George Westbrook: who's who's going to say it as we end?

Max Kingaby: best f******

Hasan Mohammed Ahmed: going to say it as we end.

Max Kingaby: guy.

Cody Haugen: Yep. Let's f******

Edwin Johnson: Finally,

Cody Haugen: go.

George Westbrook: Let's f******

Hasan Mohammed Ahmed: Let's f******

Edwin Johnson: please.

Kevin Murray: Go.

George Westbrook: go.

Skye Capazorio: you.

Edwin Johnson: I need a good week.

Cody Haugen: Yeah.

Troy McDonald Kane: Maybe.

Edwin Johnson: Please.

Kevin Murray: We're going to win this weekend is what we're going to f******

Hasan Mohammed Ahmed: go.

Edwin Johnson: Sounds good.

Kevin Murray: do. All right, let's f******

Troy McDonald Kane: No.

George Westbrook: Yes.

Kevin Murray: go.

Edwin Johnson: See boys.

Kevin Murray: All right.

Edwin Johnson: See you.

Max Kingaby: Hey,

George Westbrook: Did you say

Max Kingaby: guys.

Hasan Mohammed Ahmed: is

Skye Capazorio: I

  
  

### Transcription ended after 00:30:37

  

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.

**