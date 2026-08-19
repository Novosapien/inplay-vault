---
date: 2026-06-10
type: standup
status: extracted
extracted-to:
  - "[[digests/touchdowns-01-10-jun-2026]]"
  - "[[trading/trading]]"
  - "[[architecture/open-questions]]"
  - "[[inplay-global-website/inplay-global-website]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[components/components]]"
description: "Transcript of the 2026-06-10 InPlay touchdown — guaranteed-prize-money compliance incident, website go-live review, Persona KYC demo, and tZERO wallet split"
---

## Post-Call Analysis

> Processed as part of the **[[digests/touchdowns-01-10-jun-2026|1–10 June touchdown sweep]]**.

| Finding | Destination | Action |
|---------|-------------|--------|
| **Compliance incident** — AI agent put "guaranteed prize money up to $25M" in the site legal footer; rule is "up to $25M", never "guaranteed" | [[inplay-global-website/inplay-global-website]] | Update block added |
| **Pre-deploy copy-review agent + counsel disclaimer review** (Marlin) | [[components/components]] (Cybersecurity & Data-Handling) | Control added |
| **tZERO wallet/buying-power split RESOLVED** — tZERO = trading wallet; InPlay = referral tracker + reload + **synthetic broker** for buying power; cash wallet TBD | [[architecture/open-questions]] / [[trading/trading]] | Q resolved + Trading note |
| **InPlay synthetic broker** (buying-power tracker) — BRs being written | [[architecture/open-questions]] / [[trading/trading]] | Row added; flagged for Friday |
| **Shorting mechanics** — short increases buying power; close-out/share-return triggers; hard on-chain | [[trading/trading]] / [[architecture/open-questions]] | Note + row added; Friday |
| Persona onboarding flow demoed — signup→KYC→pass/reject; ~2–3s face-scan callback; impl engineer ~8 weeks | [[customer-onboarding/customer-onboarding]] | Delivery note extended |
| Global Website published; mobile optimisation (outline font / clipped hero screenshot → stack/tilt) | [[inplay-global-website/inplay-global-website]] | Update block added |
| Careers page JDs AI-generated/high-level — Troy + Brian writing real ones | [[inplay-global-website/inplay-global-website]] | Noted in update block |
| Old WordPress site (GoDaddy) — Kevin needs DB access restored (one-field update) | — | No action (ops) |

---

**

Jun 10, 2026

## InPlay Digital TouchDown - Transcript

### 00:00:17

  

George Westbrook: already. I can't hear you, bro.

Hasan Mohammed Ahmed: Go.

George Westbrook: No.

Hasan Mohammed Ahmed: No.

George Westbrook: Hello.

Troy McDonald Kane: Hello.

Skye Capazorio: Bye.

George Westbrook: How we doing?

Troy McDonald Kane: Good. How are you,

George Westbrook: Good. Good. Good.

Troy McDonald Kane: George? Did you sleep last

George Westbrook: I did. I did. It's just a bit only a little bit later.

Troy McDonald Kane: night?

George Westbrook: I'm usually in here about that time anyway. I'm I'm a I'm a sad. Um is this is this is my my main home and I've just got another room where I sleep. Shut up,

Skye Capazorio: I love your your um content creator mic.

George Westbrook: Brett.

Skye Capazorio: Is that the result for the laptop bugging out?

George Westbrook: Yeah,

Skye Capazorio: Oh,

George Westbrook: it's

Skye Capazorio: Brett's also got one and now we can't hear you.

George Westbrook: it's it's all for show. We haven't actually got them turned on. It just to make us look a little bit more official.

  
  

### 00:01:25

  

Skye Capazorio: It's the new trend.

George Westbrook: Yeah, I think such a boomer. You can't get your mic to work.

Troy McDonald Kane: Uh, well, I just Admin just texted me asking if we were still meeting. I go,

Brett StClair: There we

Troy McDonald Kane: "Yeah." So,

Brett StClair: go.

Troy McDonald Kane: hopefully he's joining soon.

Max Kingaby: I assume they're all in the the sales

George Westbrook: All

Max Kingaby: conference.

George Westbrook: right.

Max Kingaby: I could hear you earlier. Can you guys hear Brett?

Skye Capazorio: No.

Troy McDonald Kane: No.

George Westbrook: Hello.

Troy McDonald Kane: You're on mute, Edmond. I think there you

edwin: Sorry about that. I'm on my phone. This f******

George Westbrook: Heat.

edwin: s***. Okay,

Troy McDonald Kane: are.

edwin: George, thank you for the uh fire uh the the Thank you for taking that s*** down last

George Westbrook: That's right.

Brett StClair: That's what I

edwin: night.

George Westbrook: Me, me and Hassan here, we were we saw the email and we were like,

Brett StClair: think.

George Westbrook: "Right, all systems

edwin: Yeah.

  
  

### 00:02:59

  

edwin: Well, that worked out really quickly.

George Westbrook: go."

edwin: I mean it's amazing execution on like you know saving saving a problem but we can't have those problems like that one that that particular one could cause me I don't even know what kind of

George Westbrook: Yeah.

edwin: exposure uh the moment that we put guaranteed 25 million I mean I could get sued by 50 states and I got to put out the 25 myself

George Westbrook: Yeah,

Brett StClair: Yeah.

George Westbrook: that was that was a that was a me issue.

edwin: right things

George Westbrook: I think it just in my head I think I was I can't it it was saw that you guys were

edwin: happen Yeah. Yeah.

George Westbrook: going to the thing I was like f*** it's not up. Let's just get it get it up. And then

edwin: Yeah.

George Westbrook: obviously

edwin: No, no, I I get it. And listen, I'm not angry or anything like that. I just, you know, moving forward, even if we're in a in a hyper speed,

George Westbrook: Yeah.

Brett StClair: Yeah.

edwin: you know, we we have a saying inside our company.

  
  

### 00:03:46

  

edwin: It's always protect the castle and protect me. And I want you guys to be an extension of that. I don't want to do anything that we could do that put me at risk.

Brett StClair: Yeah.

George Westbrook: Yeah.

edwin: Right.

George Westbrook: Yeah. So I think I think one thing we'll do

edwin: Cool.

George Westbrook: or one one thing that we'll do anything with copy out there we will we'll get an agent team that before we deploy anything it goes through it checks every single sensitive term does that review before we even put it out. Um, I mean ideally that's something we thought of before, but at least like I think me and Hassan looked it was it was up for about I think an hour an hour and a half maybe and in that time there was three or four click which I'm assuming

edwin: Yeah.

George Westbrook: was me, Hassan, yourself and somebody else from the

Troy McDonald Kane: and me. Yeah,

edwin: Yes.

Troy McDonald Kane: I was I was hitting refresh.

George Westbrook: team.

Troy McDonald Kane: I didn't look at the trading challenge page per se, but the one thing too I don't know, George, like we talked about last night, is that it looked like it was the trading challenge page was not the actual page that was staged and approved.

  
  

### 00:04:50

  

Troy McDonald Kane: It was much more in detail. Edwin said he was seeing like cash payout tables like Yeah.

Skye Capazorio: So,

George Westbrook: Let me have

edwin: Oh

Skye Capazorio: so basic I sorry Troy I figured Max and

Troy McDonald Kane: So I think there

edwin: yeah.

George Westbrook: the

Troy McDonald Kane: Yeah.

Skye Capazorio: I were on this morning just going through changes on that site where I think it actually popped in was in the footer policies is what is what I think was seen. So if you if you scroll down to the bottom of the website it was like cookie policy terms and conditions and it crept in over

George Westbrook: Was

Skye Capazorio: there.

edwin: No,

Troy McDonald Kane: Under terms and conditions.

edwin: it was when I clicked on the trading. Listen,

Troy McDonald Kane: Yes.

edwin: we don't need to like belabor the point.

George Westbrook: it

edwin: I clicked on trading challenge and then you know I I don't remember what I clicked um

Skye Capazorio: Okay.

edwin: but like an entire like per pri per place prize money and everything was listed.

  
  

### 00:05:40

  

edwin: The key thing was it was guaranteed prize money up to 25 million and we've never used that phrase here. We always have to use up to$ 25 million, right? So, it's just in in the event we need a legal out that if something happens, I only, you know, want to put in five and we don't get any advertisers, I don't want I don't want to be on the hook for

Skye Capazorio: Yeah.

edwin: 25play.com.

George Westbrook: Was it did because I'm trying to think was it did it look like this page or was it or did you access it via inplay global.com? Okay. Yeah,

Skye Capazorio: So,

George Westbrook: that would be that would be the main

Skye Capazorio: George,

Max Kingaby: It it was that it was it was that um page though because it been taken

Skye Capazorio: I I when

George Westbrook: one.

Max Kingaby: from the agent had taken it from your site then put it into the input global site.

George Westbrook: Oh,

Max Kingaby: Second was that leaderboard that not that leaderboard that price board

George Westbrook: okay.

Skye Capazorio: So, it wasn't on one of the main page navigations.

  
  

### 00:06:31

  

Skye Capazorio: I'm not saying that this mitigates it. I'm just saying that it wasn't on one of the main pages. So, Troy, when you clicked on trading challenge in the top navigation, it wasn't on that main page. It was when Max and I were looking through it this morning in the footer policies there's all the terms of use policy, cookies policy, all of that which are all general and it had literally t taken it from somewhere probably the learning repository and decided to add in a trading challenge rules policy essentially is what it seems it had done um which hadn't been there previously.

Troy McDonald Kane: Right. Okay. So, I I reviewed the the new staging of the website this morning again. The helmets look much better. Thank you. On the uh app shot. Um, what do we need to do a final review on so we can get this published this morning so that it's live for when these guys go to the conference today, which I think you guys are heading over there soon, aren't you, Edwin?

  
  

### 00:07:35

  

edwin: They're They're already open.

Troy McDonald Kane: Oh,

edwin: They They already went.

Troy McDonald Kane: they're already over there.

edwin: I'm going after Yeah.

Troy McDonald Kane: Yeah.

edwin: I'm going after this call.

Troy McDonald Kane: Yeah.

Brett StClair: Should we bring the page up for one quick?

George Westbrook: Thank

Brett StClair: Make sure that we've addressed where we think it is and that we're

Troy McDonald Kane: Yeah, I think that's right, Brett.

George Westbrook: you.

Troy McDonald Kane: Let's just do a quick review page by page to make sure we're aligned with what's on there.

Brett StClair: happy.

Troy McDonald Kane: I did I reviewed it on the train this morning. So, um, you know, more eyes the

edwin: Oh, that looks really nice.

Troy McDonald Kane: better.

George Westbrook: So first

Skye Capazorio: Oh,

George Westbrook: page.

edwin: Wow.

Skye Capazorio: Max, that Verizon thing has crept in again.

George Westbrook: That's that that was me.

Max Kingaby: Yeah,

George Westbrook: I'm

Max Kingaby: George.

Skye Capazorio: Oh, sorry.

George Westbrook: I'm

Skye Capazorio: I literally I feel like I'm going mad because I I've been sitting for like six hours this morning with

  
  

### 00:08:22

  

Max Kingaby: Yeah.

Skye Capazorio: Max going through eat and everything and that was one of the things that I was like please no brands.

Max Kingaby: Yeah. No. Um, I think L George had it up on his screen about 10 minutes ago and I think he's already prompted it.

Skye Capazorio: Um,

Max Kingaby: It's not on the live link yet.

George Westbrook: That was the first thing Max said to me as well, Sky. Really funny that you both said exactly the same

Skye Capazorio: sorry.

George Westbrook: thing.

Skye Capazorio: Because I've probably nagged him so much about

George Westbrook: Um, so yeah,

Skye Capazorio: it.

George Westbrook: Verizon, that's done. That will take 5 10 minutes.

edwin: Guys, so are you going to be the point person that signs off on any of this?

Skye Capazorio: Sorry. Say that again, Edwin.

edwin: Sorry, I'm eating like

Skye Capazorio: No, it's I've got a sinus infection.

edwin: usual.

Skye Capazorio: So, I've literally got like an echo reverb that's happening in my one ear at the

edwin: Yeah. Yeah. Yeah. Yeah. So,

Skye Capazorio: moment.

  
  

### 00:09:30

  

edwin: are you going to be the one who approves all of the changes and the push to to market? Then we need someone to be

Skye Capazorio: So I no sure so I've so basically I've shared this now

edwin: responsible.

Skye Capazorio: with with

edwin: Hold on one sec, Sky. Time out. Time out. Go ahead,

Brett StClair: Sorry,

Skye Capazorio: what

Brett StClair: I just I wouldn't you shouldn't be the reviewer because you

edwin: Brett.

Troy McDonald Kane: No, I'm I'm going to review I'm reviewing it and signing off on go

Brett StClair: and and and Max are doing Yeah.

Troy McDonald Kane: live.

Brett StClair: Yeah.

edwin: Okay, cool.

Brett StClair: Just because both of you are eyeballs on this and you're going to miss stuff.

edwin: Try

Troy McDonald Kane: Yeah.

Brett StClair: self.

Skye Capazorio: I I agree that there should always be a second person to review that are fresh eyes because I've literally spent like the last over over a week reviewing this every single day with Max making changes.

Troy McDonald Kane: Yeah.

George Westbrook: Sorry,

Max Kingaby: So George,

George Westbrook: don't

  
  

### 00:10:18

  

Max Kingaby: if you stop at that right at the bottom,

George Westbrook: hit

Max Kingaby: there was I think it's underneath legal a trading challenge link.

George Westbrook: that.

Max Kingaby: It was on that link all of the prize.

Skye Capazorio: Awesome.

Max Kingaby: Not so that's completely gone now.

edwin: Yeah.

George Westbrook: Then next page, our partners. I'll do this as well just so we double check.

edwin: Heat.

George Westbrook: there for that news room.

Brett StClair: Everyone is looking very Good.

edwin: I mean, the only one that's a little tough is the Brian Hardj mug shot. I mean, he's just like inmate 784.

Skye Capazorio: Christian.

edwin: I mean, it looks like he's running a tiny mob bus uh mob over there.

Troy McDonald Kane: That's That's what you want for running a finance is someone that looks like they're going to break your kneecaps.

edwin: Perfect. Yeah, this is nice.

George Westbrook: Where is locker

Troy McDonald Kane: Yeah,

George Westbrook: room?

Troy McDonald Kane: and we'll have um um Novo team, we'll have a a few more job postings for you to put on the website probably later this week.

  
  

### 00:12:12

  

Troy McDonald Kane: We're finalizing the descriptions for our go to market interns and a few other roles that we're looking to put out in the forum.

Skye Capazorio: This is also something just to um just to note Troy in terms of that what is sitting on the careers page it the AI has generated the actual job description that that is in there. So it's not um so that just probably needs a bit of a review. It's very high level. It's obviously not committing to a package or a location or anything like that. If we have an actual job description that we want to put like load up into here, um we can

Troy McDonald Kane: Yeah,

edwin: Who creates those job descriptions? You or Brian?

Troy McDonald Kane: Brian and I are doing them together.

edwin: Cool.

Troy McDonald Kane: Yeah.

edwin: Cool.

Troy McDonald Kane: And we've also got some input from other members of the team. based on the role like I've had Cody and Jared give some input as

edwin: Yeah.

Troy McDonald Kane: well.

George Westbrook: That's too

edwin: Okay.

  
  

### 00:13:24

  

George Westbrook: big.

edwin: What are you two f****** guys giggling about?

George Westbrook: I know. I said that's too

edwin: Oh,

George Westbrook: big.

edwin: well,

Brett StClair: This attention to detail is like

edwin: I thought I thought you were talking about me, George. So, I didn't think that was laughable.

Troy McDonald Kane: I I can only imagine what jokes were being said behind that comment as I I watch your faces laugh, Brett and Max.

edwin: I think you can pretty much figure that one

George Westbrook: It weren't made about Max.

Troy McDonald Kane: But

George Westbrook: Put it that way.

edwin: out.

George Westbrook: Right. So, yeah, this Yeah, I mean the word I've typed in in the finder guarant or the start of guarantee and it can't it's not picking up anything. So, um that that's the only way.

Skye Capazorio: But it says it does not guarant

George Westbrook: Yeah,

Skye Capazorio: Guarantee

George Westbrook: that's fine. It's not going to be in here, but just double check. No, that looks all

Brett StClair: Are all of the T's and C's um AI generated or are you guys comfortable with

  
  

### 00:14:52

  

George Westbrook: good.

Brett StClair: the actual T's and C's and policies and stuff like that?

edwin: I'm pretty sure it's generated by uh the AI. I haven't looked at anything yet.

Max Kingaby: So the way I generated them was I fed in the copy of the kind of available brand documents I had it to generate one. Um, but again, if you guys aren't happy with your own legal documentation that you want to add in there,

George Westbrook: You're right.

Max Kingaby: then an instant change.

edwin: Yeah. I mean the one that always rings that we have to do with any kind of financial product is this is not a guarantee you know that you can make money. There's past performance doesn't mean future benefit. You know, all all of those that you see every time you open up any kind of like financial app, you know, it's not an offer to sell securities at the moment, you know, anything like that, right?

George Westbrook: Bunch of

Brett StClair: There are a bunch of links there.

Skye Capazorio: Cuz

Brett StClair: Are we sure we need all those legal links?

  
  

### 00:15:59

  

George Westbrook: things.

edwin: Can I see it?

Brett StClair: Feels like there's a lot there.

Max Kingaby: They were just taken from the

edwin: May I see it

Brett StClair: Yeah.

Max Kingaby: copy.

Brett StClair: Just want to make sure that we aren't over cooking it.

edwin: again?

Brett StClair: Do you want to share again your screen?

George Westbrook: Oh.

Skye Capazorio: Troy, the previous site that was up, you said that there were no policies that were included with it. Is that is that correct

Troy McDonald Kane: It was just the boiler boilerplate statement that we have on our email signatures. That was it at the base.

Skye Capazorio: at the

Troy McDonald Kane: Yeah, we didn't have I mean,

Skye Capazorio: base?

Troy McDonald Kane: we probably don't need all of those right away uh until we can refine them, but I also don't know a lot of people that actually click on those on websites.

edwin: Yeah, but we still,

Troy McDonald Kane: So,

edwin: you know, who's going to click on them? Some f****** regulator. Okay.

Troy McDonald Kane: no,

edwin: And they're going to Yeah,

  
  

### 00:16:52

  

Troy McDonald Kane: that's why I'm saying we should take them off probably.

edwin: I agree.

Troy McDonald Kane: Yeah.

edwin: Um, let let Troy, why don't you send an email to Marlin, please?

Skye Capazorio: Um,

edwin: Don't send it to Vogler because he's taking like I I don't even know where Matt's at at the moment. I know he's got a kid, but guys disappeared on me. Um, send it over to Marlin. Marlin's engaged. I got the draft uh circular last night, which I'm going to review at some point today um for the uh NFL playoffs. So, look, it's looking

Troy McDonald Kane: Great. Um, yeah,

edwin: great.

Troy McDonald Kane: Sky or whoever, can you send me the copy that was used for all of the disclaimers on the bottom of the page under legal? We'll send them to our um, external council for review or refinement or get his opinion on what's needed right now versus what's needed when we launch the competition.

Skye Capazorio: Super. I think Max, if you could just PDF those, that would be helpful. Or Troy, do you want it in a word document for comment?

  
  

### 00:17:51

  

Troy McDonald Kane: No, in word so that we can mark it up. We can red line it up.

Skye Capazorio: Okay,

Troy McDonald Kane: Yeah,

Skye Capazorio: that's fine. Thank

Troy McDonald Kane: that'd be great. Yeah, thank

Skye Capazorio: you.

George Westbrook: Max, we need to make that smaller. Then push this up so that when they land,

Troy McDonald Kane: you.

George Westbrook: they can see everything. They don't have to scroll down.

Skye Capazorio: Um George my I know Max was

Max Kingaby: We changed it to make it bigger deliberately.

George Westbrook: Nice.

Skye Capazorio: um Max was also working on the deployment to mobile because the outline font if we can just use some time to talk about that. the outline font um is obviously uh uh it it it it literally overcrowds completely when it scales it and um and then another thing is that the image it just cuts the the image so I don't know how so like there for example we would need the f the mobile the screenshot to then fit in below that like it needs to

  
  

### 00:18:45

  

George Westbrook: Yes.

Skye Capazorio: then optimize In terms of that,

Brett StClair: Can we not set up uh separate rules once it reduces a certain resolution

George Westbrook: You

Brett StClair: size just on the images and we uh right position

George Westbrook: stupid.

Brett StClair: images when below uh 16 by9 whatever it is what are the pixels I can't see whatever they are that might be the way to do it.

George Westbrook: It is this is the the different devices which

Brett StClair: Yeah.

George Westbrook: 14 Pro Max. I mean I don't think that image in the back looks bad there. Um but I agree 100% agree with you with

Skye Capazorio: No,

George Westbrook: these.

Skye Capazorio: I don't think that that image at the top looks bad, but then it's cut off the the phone screenshot that is is

George Westbrook: Oh yeah yeah yeah.

Skye Capazorio: representative because that's on the Right. So, it needs to move that then um underneath or or make it smaller and move it next to trades for like it needs to find a space for it to go.

  
  

### 00:19:56

  

George Westbrook: Yeah. Yeah.

Skye Capazorio: Um and the same if you go all the way down to the bottom,

George Westbrook: I think it's maybe

Skye Capazorio: it's also cut off that screenshot. So, there you can see it on the on the left coming into it. So, that either needs to be like above the I would say probably above the title or below put me in play.

George Westbrook: Yeah. Okay. Mobile mobile mobile phone tra page football challenge page. Okay. Um right. So, there's that done. Oh, I think there was a this more relevant for Kevin, I think, around the old um the old website cuz I think he said he wasn't able to access it and basically we need to go into WordPress and the database there and just update one thing and then you can get access back cuz I think he was concerned that it was like completely wiped but all it is is with WordPress assuming you've hosted it with someone or somewhere and

Troy McDonald Kane: Yeah, it's with GoDaddy.

  
  

### 00:21:10

  

George Westbrook: Okay. Okay. Um, yeah. So,

Troy McDonald Kane: The finest the finest of domain

George Westbrook: we just need to hop on and change that.

Troy McDonald Kane: management.

George Westbrook: Yeah. Um, so there's that. There's the one thing we were kind of laughing about yesterday was Persona obviously sent set up the on boarding call.

Skye Capazorio: That's not

George Westbrook: Um, but we've already got it implemented into the um on boarding flow. So, it's sign up KYC, validate, send it back. if it's passed. If it hasn't, obviously reject it. Um, so that's correct if I'm wrong here, Hassan. That's working. We're happy that that's working.

Hasan Mohammed Ahmed: Um yeah,

Skye Capazorio: Okay.

Hasan Mohammed Ahmed: so at the moment everything is in place like I have done a few um what's called tests. Um I do have like the test of the video that I can also then send over for the onboarding flow. I still have

Brett StClair: Can I do a quick demo?

  
  

### 00:22:11

  

Hasan Mohammed Ahmed: it

Brett StClair: Are you able to do demo or am I throwing you in mid build somewhere?

Hasan Mohammed Ahmed: um at the moment is I'm still in building so I don't think I can do it live. If I can use the um video that I sent one um um uh yeah um let me screenshot this um actual video as well. So show you guys Um yeah. Um, is everyone a Yeah. Um, and so here's um what's called standard onboarding flow. Um, I cleaned up a bit since it's in like stages. Um, I might slow on the video a bit cuz I was doing a bit quick, but and so and so if you enter your um actual I mean like I think split up the actual onboarding flow. So it's a like I would say cuz it's a lot more like enjoyable than if if it's just like a standard form cuz so it's more I say interactive and so you would enter an email and then enter um a password as well.

  
  

### 00:23:45

  

Hasan Mohammed Ahmed: Um yeah and then over here like at this stage here you you would enter a code. Um so ideally um how like it would be um so if you didn't send the the um a QR code it should do like a deep link into here. So it should just um actually auto um I'm still um seeing if that's going to be the possible but ideally like it should be um if you just on the actual on boarding flow and then after this is going to be a as well. So yeah, this is just the the standard one. It has um it own like individual with names as well. So yeah,

edwin: Excuse

Hasan Mohammed Ahmed: his is all standardized like um ID. Um I mean like ignore the ID.

edwin: me.

Hasan Mohammed Ahmed: It's just like a placeholder as in like I did it slow so that it would always like pass and so that that's why I just uploaded like a almost random ID.

edwin: That's cool.

Hasan Mohammed Ahmed: So

  
  

### 00:25:12

  

George Westbrook: Go an

edwin: I mean, that's some You should have been a a model,

Hasan Mohammed Ahmed: smash

edwin: Hassan. I mean, you missed it.

Troy McDonald Kane: or or or a persona demo

Hasan Mohammed Ahmed: Sure.

edwin: I prefer the model. I mean, I don't think they make as much at

Troy McDonald Kane: actor.

edwin: Persona.

Hasan Mohammed Ahmed: Yeah. And so yeah, so that's the entire thing on boarding flow. Um so at this step um over here after like this and so after that is and done it is like pretty quick.

edwin: Yeah, that's

Hasan Mohammed Ahmed: And so as soon as you get um was going to scan your face,

edwin: awesome.

Hasan Mohammed Ahmed: it would um upload it onto I think API and then it will give you like a call back. And like I tested it, it's within about like um two three seconds maybe. It's extremely quick.

edwin: Wow.

Hasan Mohammed Ahmed: Yeah. And then after that it will have you the QR code. And so if you show like other people as well into

  
  

### 00:26:15

  

edwin: It's great

Hasan Mohammed Ahmed: that.

edwin: stuff.

George Westbrook: See,

Hasan Mohammed Ahmed: See I think

George Westbrook: I think the implementation engineer that's going to be there for the next eight weeks is going to be quite happy that

Troy McDonald Kane: Great.

Hasan Mohammed Ahmed: the

George Westbrook: it's is done.

edwin: Boys, I've got to jump. Girls, uh, boys and girl, I've got to jump. all have a great week. Uh right now the score is Miami one, Edwin one. I didn't lose last night. We're tied.

Skye Capazorio: Great

Troy McDonald Kane: All

edwin: Yeah. Well, tonight I'm going to go for him.

Troy McDonald Kane: right.

edwin: I try to be up two to one.

Skye Capazorio: stuff.

edwin: So, um anyways, thank you all for this. I really appreciate the attentiveness on that fire drill. Thank you very very much. Gave me a lot of confidence. So, um all have a great day. If anyone needs me, please reach out. We'll let you know um as soon as we're done with our meetings today how that

Hasan Mohammed Ahmed: Perfect.

  
  

### 00:27:04

  

edwin: went.

George Westbrook: Perfect.

Brett StClair: That's the f***

Skye Capazorio: Great.

George Westbrook: Let's f******

Troy McDonald Kane: Great.

George Westbrook: go.

Brett StClair: it up.

edwin: Thank you all.

Troy McDonald Kane: Thank

edwin: Bye now.

Hasan Mohammed Ahmed: That's

Brett StClair: Go.

Troy McDonald Kane: you.

Skye Capazorio: Um, Troy, just as next steps for for the website. Sorry, I see I don't know if George just dropped off the call at the same time.

Troy McDonald Kane: George just dropped. He's just like He was like,

Skye Capazorio: He was like, "Mike out.

Troy McDonald Kane: "I'm done. I'm going to bed.

Skye Capazorio: I'm done." Um, I just wanted to check, Troy. Okay. So, uh I've obviously shared on our teams group the latest link of what has been pushed there. But now, um so that we're all aligned about what next steps are. George, you're going to take all those policies off. There's obviously still the short link cut through. So, it's just the legal portion that's going to be taken out. Um Troy, are you able just to copy paste the disclaimer?

  
  

### 00:27:51

  

Skye Capazorio: I think we should still have our disclaimer that goes from our email signature um at the bottom.

Troy McDonald Kane: Yeah, I can uh I'll send that off to you guys or you can just pull it from an email I've sent in the past. But it's that's that's what was on the website before that we've been putting on our emails. It's just very

Skye Capazorio: Well, that's fine. And then,

Troy McDonald Kane: basic

Skye Capazorio: um, George, as soon as that's done, um, as soon as it's up updated on the preview link, if you can let us know, then Troy, if you want to just I'll also review it, but if you can give it the, um, the final go.

Troy McDonald Kane: final review.

Skye Capazorio: and then and then we can push that live. Um George will when we review it,

Troy McDonald Kane: Yeah.

Skye Capazorio: will we be able to review it with the mobile optimizations done to it too? My biggest concern surrounding this and this is what I I was saying I think I anyway um is that people most of the time especially in this scenario are going to probably look at this on their phone first than on a desktop, right?

  
  

### 00:28:54

  

Skye Capazorio: Um, and so I think if if that is the case, then I think what we need to do is make for for desktop just make it super thin on those outlines so that it doesn't bunch like it is design-wise for mobile. Um I don't know if we then optimize it. So there's like a bar that sits. So like where for example where it says um trade trade sports the stocks buy sell hold and all of that on the desktop it's currently the phone's to the right as a screenshot. Let's rather just create a block below it and put the screenshot in there. So it may look a little bit funny from a use of space on a desktop use but at least it's optimized for mobile. I don't know Troy if you agree with that.

Troy McDonald Kane: I'm sorry. Can you repeat that? I was reading something at the same

Skye Capazorio: Sorry. So, what I'm saying is I think that we should go onto the desktop and optimize it from the

  
  

### 00:29:41

  

Troy McDonald Kane: time.

Skye Capazorio: desktop to mobile because there seems to be an issue at the moment with the way that it is optimizing. And I think most people that are at this event are obviously not going to sit down and then go on to a desktop. They'll just look at they'll type in inplay global.com and go look at it on their phone. And so I think what we need to do is rather if we're having an issue with AI and the way that it's optimizing and resizing for mobile is to rather take the desktop and just design it for or or take this just take it design it in the space. So take the phone move it into a block picture below the statement. Um and I think it's actually really just those that's the main thing. It's just those screenshot pictures that need to need to show up. Um George, can you also scroll down there? I just want to check that those the graphs for outcome based and um and is is correct. Okay.

  
  

### 00:30:42

  

Skye Capazorio: Yeah. Okay. So, it's just basically scaled those down, which is fine. I would I would ideally make outcome um

George Westbrook: I think top and bottom rather than side to side.

Skye Capazorio: outcome and yeah, outcome and and fragmented one under the other so that it's you can read it better.

George Westbrook: Yeah.

Skye Capazorio: Um, and then I think that's that main page is the only page where there's a lot of that. Then the rest of the pages should be fine for now. Um, while we then sort out the visuals

George Westbrook: I'm literally getting these ch these changes to be like two minutes that they bigger and let me go

Skye Capazorio: So I I mean the you can make the phone smaller there.

George Westbrook: I'm

Skye Capazorio: I think that that could possibly work or alternatively bring it below to explore under explore the 2026 football challenge. But in an ultimate sense, it would actually go sorry it would actually go in between where every season ends and the

George Westbrook: Oh,

Skye Capazorio: first put me in play button.

  
  

### 00:32:03

  

Skye Capazorio: So it would go trade sports or stocks um buy sell hold every play every game phone image then

George Westbrook: my my only concern with that would be is if so Let's I know we said keep it smaller,

Skye Capazorio: buttons.

George Westbrook: but if it's that size, we put it underneath there, it finishes there, then a user has to scroll down for the for these

Skye Capazorio: Okay. So then that's fine. Just make it smaller.

George Westbrook: buttons.

Skye Capazorio: Then just make it smaller and maybe tilt it more at an angle next to like maybe it comes

George Westbrook: Yeah.

Skye Capazorio: more like overlaps from Trade Sports as stock so it feels like it's more put together as opposed to just popped

George Westbrook: Yeah. Let me give me one second. and he'll meet this quick.

Skye Capazorio: there.

George Westbrook: me chatting to the AI. So hopefully this should be top and bottom. Um yeah. Okay. So move that. So that top and bottom that tilted bit smaller in that top right and this cut down a bit more so the phone's visible.

  
  

### 00:33:26

  

Skye Capazorio: Yes.

George Westbrook: Then what are the other pages? Our partners.

Skye Capazorio: Temple covers.

George Westbrook: That looks all right. That's all right. That's okay. Then these font the fonts as well. It's all right. Crop that one. That one. Move it over a bit. That looks fine. And then get rid of the legal ones as well. Okay, perfect. And let's see what it's done here. Is that Is that a bit better for mobile?

Troy McDonald Kane: Yeah,

Skye Capazorio: Yeah.

Troy McDonald Kane: that looks a lot better.

George Westbrook: Um, and then even on on desktop it'll be like that.

Troy McDonald Kane: Yeah.

Skye Capazorio: Yeah,

George Westbrook: Yeah,

Skye Capazorio: I think that's much better.

George Westbrook: that

Skye Capazorio: Thanks,

Troy McDonald Kane: Yeah.

Skye Capazorio: George.

Troy McDonald Kane: I like it on an angle. It seems less flat and like you just plopped it

Skye Capazorio: And

Troy McDonald Kane: there.

George Westbrook: That doesn't hurt.

Skye Capazorio: that looks cool to you.

  
  

### 00:34:51

  

George Westbrook: It

Skye Capazorio: The stacking

George Westbrook: does. Oh, yeah. Yeah. Okay. Yeah. Yeah. the 3D the 3Dness. Okay. Yeah, I'll do that. Um, okay. So, yeah, that the other pages make that look a bit better. Just tighten up the space. Okay. Um, right. Get that sorted hopefully within the next half an hour. Um, right. Is there anything else? I suppose main priorities website done on boarding sports radar data statics done the live data tested um and done we can run back the simulations. Um, I think the only thing that we one of the things that we do need to think about I think this is more more for you Troy is the um the the wallets with tZERO in that who's holding the balance because in my opinion it it should definitely and I'm not sure if I misread what they were saying the other day. Um, I think I definitely think they should be holding the balance because just in terms of like obviously latency is key.

  
  

### 00:36:20

  

George Westbrook: Um, and if we're having to when they click trade, we have to do like a server side validation that they've got the the the budget and then we send it to them. If we send it to them, it's all in their own network. So, it'll be just a lot quicker. Um, but I suppose it's one is it is with them. Is that up for debate or is it more like a requirement that we have to do

Troy McDonald Kane: No, it's up for my understanding and we'll we can talk about this on Friday morning's call too is

George Westbrook: it?

Troy McDonald Kane: that they the trading wallet they'll own because that will be tied to the digital wallet but they're not going to you start tracking the referral wallet and I think we're still trying to figure out what the cash wallet

George Westbrook: Yeah.

Troy McDonald Kane: looks like. If that's them,

George Westbrook: Yeah.

Troy McDonald Kane: if that's a third party, I think that's up that's up for debate. But my understanding is that they would track the trading wallet.

  
  

### 00:37:14

  

Troy McDonald Kane: Let's just call it a trading wallet,

George Westbrook: Okay.

Troy McDonald Kane: a referral wallet, and a cash wallet. And so they'll they'll manage the trading wallet. You guys manage or track the or build the tracker for the referral wallet. And then we need to find a mechanism that allows us to put money back into the trading wallet from the referral

George Westbrook: Yeah, that's that's f because for some reason I thought they were suggesting that we have to calculate the buying

Troy McDonald Kane: wallet.

George Westbrook: power which obviously is constantly constantly changing um which one would be an expensive operation if we did it and two would just wouldn't make sense for us to be doing on our infrastructure because then every time we do that it's communicating with them and it's Yeah.

Troy McDonald Kane: Yeah. So, actually now I remember this. Okay. So, the the thing is that they don't they're not they're kind of only doing that in like a production like as a broker as if they were the broker.

  
  

### 00:38:13

  

Troy McDonald Kane: The broker is actually the one that tracks the buying power. So, we have to create this inplay market synthetic broker element. that tracks the buying power. Um, so let's let's it's up for discussion. Let's discuss it on Friday. Um, we we haven't even done the business requirements for that yet. I just gave them the business requirements for the primary offering, uh, which we're going to discuss on Friday as well. And then we have to I'm writing the business requirements for shorting. The one thing to note with shorting though is that when you do short, you actually get double the buy. You have to increase the buying power, not decrease the buying power because you have to be able to close out the short position through buying. So let's say you buy a 100,000 or you short 100,000. You're actually need 200,000 in buying power because you're actually receiving that 100,000 as funds because you're shorting it. You've sold it.

  
  

### 00:39:08

  

Troy McDonald Kane: So you have to be able to buy back into it and then they're if they go below so then that increases their buying power to 200K. But let's say it draw down draws down to 100K then it needs to trigger for them to return the shares. It's it's it's a little bit messier than it needs to be. I'm trying to find a more elegant way of doing it um at least for the simulation. You know shorting is not a concept that has really been built into um tokenization yet. uh that that's the problem. Like in a in a traditional market, it's a lot easier because there's locates and other mechanisms that support the shorting capability, but when it's on a blockchain, it's um you got to you got to figure out like if the shares are on reserve and all that.

George Westbrook: Yeah.

Troy McDonald Kane: So, let's let's discuss all this on Friday with

George Westbrook: Okay,

Troy McDonald Kane: them.

George Westbrook: perfect. Um, I think I think that's everything. Correct me if I'm wrong.

Troy McDonald Kane: Okay. No, but when uh you know,

George Westbrook: Anyone?

Troy McDonald Kane: I'll wait for you guys to let me know when it's time to final review the website so that we can try to get that out today.

George Westbrook: Perfect.

Troy McDonald Kane: All right. All right.

George Westbrook: Right,

Troy McDonald Kane: Thank you, gentlemen.

George Westbrook: let's f****** go.

Troy McDonald Kane: Let's f******

George Westbrook: I've said it at the right time now.

Troy McDonald Kane: go. I know. Every day. Every day. All right. Thanks, J.

George Westbrook: Speak to you soon.

Troy McDonald Kane: Bye.

George Westbrook: Have a good one.

  
  

### Transcription ended after 00:40:28

  

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.

**