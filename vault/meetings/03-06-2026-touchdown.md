---
date: 2026-06-03
type: standup
status: extracted
extracted-to:
  - "[[digests/touchdowns-01-08-jun-2026]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[trading/trading]]"
---

## Post-Call Analysis

> Processed as part of the **[[digests/touchdowns-01-08-jun-2026|1–8 June touchdown sweep]]**.

| Finding | Destination | Action |
|---------|-------------|--------|
| **Persona contract SIGNED**; implementation on intro to their tech engineer | [[customer-onboarding/customer-onboarding]] | Delivery note updated |
| Apple dev account reset to start (Edwin/Troy signatory step); Google Play set up | [[customer-onboarding/customer-onboarding]] | Delivery note updated |
| Referral mechanisms / QR built, tested in isolation; auth-framework decision pending (links to Persona) | [[referral/referral]] / [[customer-onboarding/customer-onboarding]] | Captured (fuller detail from 05-06 demo) |
| VPC stood up (locked down, secure, connected to T0); FIX gateway rebuilt for concurrency; Hassan load-testing | [[trading/trading]] | Architecture note updated |
| Sport Radar API soon linked to app (live vs mock data) | [[information-layer/information-layer]] | Captured (confirmed live in 05-06) |
| Booster = too early (order-management/ad-ops for scale); Kevel still needed for sponsorship serving | Advertising (cross-cutting) via digest | Noted |
| Challenge-website content session proposed (terms, rulebook, prize pool, how-it-works; repurpose flyer) | [[challenge-website/challenge-website]] | Flagged — own session |
| Feedback ownership split: app→Cody, global website→Skye, challenge website→build out | — | No action (process) |
| Cody to review the vault/content repository (exec decisions being made from it) | — | No action (process) |

---

**

Jun 3, 2026

## InPlay Digital TouchDown - Transcript

### 00:00:00

   
Max Kingaby: Afternoon guys.  
Kevin Murray: How's it  
Skye Capazorio: Hi  
Max Kingaby: Hello. Good.  
Kevin Murray: going?  
Max Kingaby: How's it going for you  
Skye Capazorio: everyone.  
Max Kingaby: guys?  
Gary Anderson: Morning everybody.  
Kevin Murray: Not bad at all.  
Max Kingaby: Morning.  
Kevin Murray: Morning.  
Edwin Johnson: Hello. How is  
Max Kingaby: Morning.  
Kevin Murray: Yeah.  
Edwin Johnson: everybody?  
Kevin Murray: Good.  
Skye Capazorio: Max, I've started going through.  
Max Kingaby: Awesome.  
Skye Capazorio: You'll you you'll start to see feedback elements coming through on the website um on the changes that you sent through to me today.  
Max Kingaby: Awesome. Thank you, Skye. I've been also editing the page now looks exactly like the live site as well.  
Skye Capazorio: It's not it's not reflecting on my end that way just so that you're aware. So I don't know if  
Max Kingaby: That's  
Edwin Johnson: I can't hear you, Max.  
Max Kingaby: you hear me now?  
Edwin Johnson: Yes. That must be one hell of a building you guys are  
George Westbrook: Go  
Edwin Johnson: in.  
Skye Capazorio: Yeah.  
Brett StClair: just  
Edwin Johnson: Sound proof  
   
 

### 00:01:57

   
George Westbrook: the new new office.  
Brett StClair: just  
George Westbrook: So it's this new merged audio is how you  
Edwin Johnson: booth.  
Brett StClair: kind of unmmerge your silence then link up and then it doesn't pick us up and we can all have our mics on.  
Skye Capazorio: Fire.  
Brett StClair: It's clever tech until it doesn't work. Which  
Max Kingaby: And I do.  
Edwin Johnson: Okay.  
Cody Haugen: Yeah, now we can't hear  
Brett StClair: website?  
Cody Haugen: you. Nothing, Brett.  
George Westbrook: singing the closes of Google for weeks and weeks and weeks.  
Max Kingaby: Okay.  
Skye Capazorio: I'm  
Brett StClair: I'm following the This  
George Westbrook: So I suppose I was just thinking some of the some of the things we'll go through today. Um obviously the websites um the app and the advertising as well. um some of the back end some of the backend stuff we've been doing which we're making really good progress on um most notably referrals and then obviously we've got I think the Keville call next week which is correct me if I'm wrong Brett about the ad serving and then obviously maybe we do a quick update on the the booster booster demo we did as well and HubSpot as well Cody I saw that come  
   
 

### 00:04:13

   
Brett StClair: Can you guys hear me? Okay,  
Cody Haugen: Yes, we can hear you now. Uh the only one I'll add there,  
George Westbrook: Yes.  
Brett StClair: now  
Cody Haugen: George, if you want another ball in the air, that's also the other piece to launching this app is persona is signed. So we will so we will kick off that implementation as soon as we get that um  
George Westbrook: Perfect.  
Cody Haugen: intro from sales guy to uh tech engineer implementation strategist whoever they intro us to. Um but yeah, we're we're connecting connecting  
George Westbrook: Perfect.  
Brett StClair: Is this blood?  
George Westbrook: Yeah, I suppose if we start with the the kind of on boarding referral thing.  
Cody Haugen: dots.  
George Westbrook: Um, with the the actual on boarding, we we haven't started that because obviously we we're waiting on the persona stuff, but we thought right, let's just go straight to the referrals. Um, so we've been building the mechanisms for that, testing the QR codes. It's not integrated into the application yet because we wanted to test it in isolation and we've got the codes generated.  
   
 

### 00:05:09

   
George Westbrook: We're just working on the the back end stuff so that when a user shows that QR code or sends the link, it allocates the funds to or allocates the referral to their account and then in the referee um it's going to have that record against them so that they're going to get those those dollars deposited into their referral account. And then now we got the persona stuff working.  
Cody Haugen: Great.  
George Westbrook: Um that kind of whole on boarding flow. Um we've put a bit of head space into it but not done the work on it yet but we know we need to get authentication sorted um because there's obviously the KYC with persona but we obviously need to manage the actual authentication of the user into the application carrying that across all of the backend services and obviously the front end stuff. So that yeah good progress been made on that just deciding on the framework to use for the authentication then that will link nicely with Persona and then I think on Friday um we'll have a quick discussion with T0 about the the onboarding on their aspect but they've got they've got quite good API docs so we we we can get a lot of visibility into  
   
 

### 00:06:23

   
Skye Capazorio: Did we Um, just I just want to bring it up because Brett, I mentioned this to you this morning when we met. Cody, your issues that are being had with Apple and the Apple account. What can you clarify? I know yesterday we were talking about that you were struggling to get hold of them or get or get something from  
Cody Haugen: No.  
Skye Capazorio: them.  
Cody Haugen: So, I mean it's it's so Yeah. I mean, long story short to the Bretton team, um they kicked us back to the beginning because we we went through the process like I don't know, six months ago, but never actually fully completed it. And so, they kicked us back to the beginning. So, now we're waiting on uh uh for them to email or call Edwin to approve Troy as a company signatory to sign that developer agreement. Um and then once that is complete, then I can add you into the Apple account. So, LA last time we did this, it took about 48 to 72 hours um to get you add or to get the call or email, whatever they did with Edwin.  
   
 

### 00:07:29

   
Cody Haugen: I I don't even know what they did last time, but um so yeah,  
Skye Capazorio: It's  
Cody Haugen: that that's where we're at right now. Um Google has been added. Um I don't know if you guys have had a check on that, but I added you guys yesterday.  
Skye Capazorio: so easy.  
Cody Haugen: Um, so or two days ago, whenever you sent that email. So, we're good there. Um, so that's where Apple and Google set.  
George Westbrook: Okay, perfect. Yeah, I remember seeing the the Google one come through. Um,  
Cody Haugen: Yep.  
George Westbrook: so get that get that all linked up as well.  
Cody Haugen: Yep. Exactly. Um, so yeah, we're just we're just waiting on Apple to to call or email Edwin to verify that. Um, yeah. So that should answer any questions where we  
George Westbrook: Okay, perfect. Then the I suppose let's talk about the back end.  
Cody Haugen: set  
George Westbrook: Some of the backend stuff we do we've been doing before we go on to the the websites front end stuff.  
   
 

### 00:08:24

   
George Westbrook: So one of the things we've been getting on is actually obviously connecting to the engine. um to T0 making sure our infrastructure is sorted out. We've got all the VPC set up so it's all locked down. It's all secure. It's all connected to T0. Um and we've rebuilt the gateway as well uh or the fixed gateway for managing that connection um so that the concurrent well the amount of requests it can handle at one time is like ridiculous. So Hassan was doing a bit of load testing as well. Um and it's looking pretty good. It's like very fast. Room for improvement, but as a starting point is it yeah is really really good. Um the sports radar data uh the API as well making making good progress on that. soon to be linked up, still building it out, but soon to be linked up to the actual application. Um, and then we'll start seeing some live data, so it's not like just random mock data. Um and then yeah the referrals on boarding on boarding covered referrals covered um the trading gateway the sports radar and then maybe we tag on the advertising at the end.  
   
 

### 00:09:50

   
George Westbrook: Um and then the updates for the websites I suppose sky you and you and Max have been having conversations on that haven't you? Is it that's making good progress I think isn't  
Skye Capazorio: Yeah,  
George Westbrook: it?  
Skye Capazorio: I think the So there's I think we were we've now I've now got the version that has the copy as we had supplied it.  
George Westbrook: Mhm.  
Skye Capazorio: So I'm busy going through that. the visual side of it needs quite a bit of work so that it has so it pulls  
George Westbrook: Yeah.  
Skye Capazorio: through the visual elements of that deck um into it because right now it's not it's not like that. So it needs to pull the visual elements of the um the current the the current holding page essentially into it um and and adding and building that out. Um, so I'm busy reviewing in terms of the content on there, but I saw that um, uh, a lot of the bios have been loaded. I know I've just sent you Brett Brett Vitma's, um, bio and, uh, and and, um, headshot.  
   
 

### 00:10:57

   
Skye Capazorio: Uh, so I think you have everything except uh, Brett, you Brett, Brett Sinclair, Brett to send that to me and add that. Um, and then I think that then completes all the bios that we need on there.  
Max Kingaby: Sorry. As in, are we having Brett and Cla as in Brett? Are you going on the  
George Westbrook: Yeah.  
Brett StClair: is suggesting it. I just need to have a think about it.  
Max Kingaby: website?  
Brett StClair: I'm just in the middle. I was talking to Sky about it this morning in this exit with Teraflow. So, I got to be careful. The guy's threatening to pull the deal and all this kind of stuff. So, I'm just But I'll talk to you guys about it afterwards. Um  
George Westbrook: one one thing as well the three kind of feedback elements we got at the moment are obviously the global website the challenge website and the actual application um obviously appreciate Sky if that's all currently sitting with you that's quite a lot so is there maybe a way that we could have one person reviewing each of those things so that we  
   
 

### 00:12:03

   
Skye Capazorio: The app's not sitting with me. So the app sitting with Cody to provide that feedback.  
Brett StClair: Yeah.  
Skye Capazorio: The global the website is with me based on what Max Jade with me today.  
George Westbrook: Okay.  
Skye Capazorio: I'm reviewing that to get feedback to you today. Um and then the talent website we're going to have to that needs to then be built out um from a content perspective.  
George Westbrook: Okay.  
Brett StClair: Can I suggest for the challenge website we do a hour hour and a half interview session um that captures that requirement as quickly as we can um and then we do the rebuild off the back of that. I think it'll just help the flow so that we don't have so much backwards and forwards getting that baseline and then push through. Is everyone okay if we do that?  
Skye Capazorio: Yeah, sure. I also think that there's there's a lot of we could probably outline what needs to go on the challenge website ahead of that to go into that call, but then I think there there's just chunks of information in there that need to be rounded out as in the actual detail that goes into that information into those sections.  
   
 

### 00:13:07

   
Skye Capazorio: Is that that's right,  
Cody Haugen: Yeah, like yeah, like we talked about in Chicago,  
Skye Capazorio: Cody?  
Cody Haugen: like uh we need the terms of service um basically the rules of the on there.  
Brett StClair: No  
Cody Haugen: We need probably or we definitely need the prize pool um definitions  
Edwin Johnson: Wait.  
Brett StClair: one  
Cody Haugen: loaded on there. Um I I can't I can't remember all the details we talked about in Chicago a few weeks ago,  
Brett StClair: needs something.  
Cody Haugen: but I know those were definitely two of them um in there. And then the look and feel of it. Didn't we decide on just like basically repurposing the flyer as kind of the look and  
Skye Capazorio: Yeah. So that's that's less I'm I'm less concerned about the look the look of it.  
Cody Haugen: design?  
Skye Capazorio: I think it's more just defining the first batch.  
Brett StClair: So,  
Skye Capazorio: What is the what are the kind of headline content pieces we want which we can get ahead of  
Cody Haugen: Yes.  
Skye Capazorio: time and then knowing that there's going to be epsom laurum copy that sits in there for the time being until that's rounded  
   
 

### 00:14:04

   
Cody Haugen: Yeah, great. Yeah, I mean I I think I mean terms of service and rulebook are the two I remember.  
Skye Capazorio: out.  
Cody Haugen: Um or sorry, the rule book and prize pool are the two I remember. Um how it works I think was one of them. But yeah, we can get all that to you guys. We we we already gave that some thought.  
George Westbrook: Perfect. Um,  
Brett StClair: Seven.  
George Westbrook: and then the the app as well. Um, I suppose that's that's a key one, just getting the the feedback  
Cody Haugen: So feedback as far as initial feedback I mean so first off guys I mean I do want to say it  
George Westbrook: on  
Brett StClair: Hello.  
Cody Haugen: looks amazing. So like once again you guys have captured our initial definitions and things. So great work.  
Brett StClair: Yeah.  
Cody Haugen: I mean it's I think from now or here so I've already uploaded the initial round of feedback. Um, but I think generally speaking, it's we're just talking like es and flows now of where things are placed, functionality of where the thumbs can reach and really getting into like the nitty-gritty of looks and feels,  
   
 

### 00:15:02

   
George Westbrook: Huh?  
Cody Haugen: but um the overall, you know, concept and what's what it's actually showing, uh, everyone is blown away by it. So,  
George Westbrook: Huh?  
Cody Haugen: I mean, just great job. I mean, it's the best app I've ever seen, and I've seen thousands,  
Brett StClair: We had an idea, by the way.  
Edwin Johnson: Hey, Cody,  
Brett StClair: Um,  
Edwin Johnson: let me interrupt real quick. Brett, do you find it amazing?  
Brett StClair: yeah.  
Edwin Johnson: It's the best app with the best product and we can't get anyone to f******  
Cody Haugen: please.  
Edwin Johnson: advertise on it because I find it pretty f****** disgusting.  
Cody Haugen: It's pretty disgusting indeed. But that is based on what we just talked about. I mean,  
Edwin Johnson: No,  
Cody Haugen: Yeah.  
Edwin Johnson: I got it. I got it.  
Cody Haugen: Yeah.  
Edwin Johnson: Go ahead,  
Brett StClair: um so Apple and Android all these guys launch and it's not for now it's  
Edwin Johnson: Brett.  
George Westbrook: f***.  
Brett StClair: for a year's time uh design app of the year and you know who won it this  
   
 

### 00:15:59

   
Skye Capazorio: Is  
Brett StClair: year  
Skye Capazorio: that  
Edwin Johnson: Brad St.  
Brett StClair: NBA.  
Cody Haugen: Yeah.  
Edwin Johnson: Clair.  
Cody Haugen: And their and their app is juvenile at  
Brett StClair: So if you've had a look at the MBA app,  
Cody Haugen: best.  
Brett StClair: have a look at it. It won the design Apple app of the year  
Cody Haugen: It sounds like It sounds like one of those award shows where you pay to get  
Brett StClair: essentially.  
Skye Capazorio: Yeah,  
Cody Haugen: nominated.  
Skye Capazorio: I there's a lot of that.  
George Westbrook: Yeah.  
Skye Capazorio: I mean, I'm not I'm not Yeah. discrediting elements of it, but it's also Yeah. highly reliant on the cohort of apps that were supplied as well as who was the highest bidder for for the award.  
Cody Haugen: Yeah. But yeah, so so that's the app feedback's in the admin portal.  
Brett StClair: I  
Cody Haugen: Yep. Um so yeah,  
Brett StClair: mean  
George Westbrook: Perfect.  
Cody Haugen: let's let's run with that first uh boost. There's probably 15 to 20 things in there uh that I uploaded already.  
   
 

### 00:16:53

   
Cody Haugen: Um, and then we can see those reflections and and then go from  
Brett StClair: sir  
George Westbrook: Perfect. Yeah,  
Cody Haugen: there.  
George Westbrook: because I think I remember one of the ones was the helmets which Yeah.  
Brett StClair: and  
George Westbrook: in the process of getting that sorted.  
Cody Haugen: Yep.  
Skye Capazorio: Okay.  
Cody Haugen: The colors to the helmets. Yeah. Yep. And I know Kevin sent over some hex codes uh to you guys as far as primary secondary.  
George Westbrook: Yeah.  
Skye Capazorio: Oops.  
Brett StClair: three  
Cody Haugen: Ke Kevin,  
Kevin Murray: I'm still fixing some of the um ones from the NCAA,  
Cody Haugen: did you send  
Kevin Murray: but the NFL ones are complete and you'll have that by the end of your time today for you  
George Westbrook: Perfect. Perfect.  
Kevin Murray: guys.  
George Westbrook: We don't sleep. Coffee, cap,  
Brett StClair: was  
George Westbrook: caffeine, and uh nicotine.  
Cody Haugen: Sounds like my type of day.  
George Westbrook: Um so yeah, that's all. Yeah, all the build stuff. Um is it worth talking about booster Brett?  
   
 

### 00:17:45

   
George Westbrook: What what came out that that call?  
Brett StClair: I think boost is too early to be honest. Um, it was an order management system and it's kind of when you hitting a greater scale of advertisers. Um so I think it's you know managing 10 advertisers at the moment can be  
Skye Capazorio: Okay.  
Brett StClair: done manually. Um um interesting meeting good meeting good kind of insight  
Skye Capazorio: It's  
Brett StClair: as to how to manage the scale of what these guys expect from a a data and and audit and all that kind of point of view but it just feels too early. Sky do you any do you have any views on that?  
Skye Capazorio: Yeah, I think that they built for for further down the line.  
Brett StClair: I  
Skye Capazorio: and I wouldn't bring them on to manage to manage 10 sponsors. Um in that in that space I think that that absolutely can be done  
Brett StClair: see  
Skye Capazorio: manually. Um I think when we need to start automating that the bill back and all of that sort of stuff is when we start entering into that conversation with them about how that gets served and managed  
   
 

### 00:18:52

   
Brett StClair: he next week is going to be  
Skye Capazorio: and I think I think as I think the convers sorry sorry Brad I think the conversation with Keville next week will be probably quite similar in that regard but it's good to see and have visibility of what that looks like.  
Brett StClair: I don't think so. Um because serving ads or serving the placements and getting the metrics and getting all the reporting that's you want an ad server there. You need some kind of ad server.  
Skye Capazorio: is. So they also going to take ownership of the reporting side of  
George Westbrook: Let's  
Brett StClair: So what your ad server does is it'll place the sponsorship.  
Skye Capazorio: things.  
George Westbrook: go.  
Brett StClair: It'll allow them to rotate uh campaigns. So don't think of the ad server as you know just the programmatic stuff. It manages how it was served, who it was served to, um what pages are being served, what kind of campaigns are being served. So if they rotate, if you just if we keep it static like it is at the moment,  
   
 

### 00:19:49

   
Skye Capazorio: That's  
Brett StClair: fine. But I promise you the guys will want to run different messaging,  
Skye Capazorio: f******  
Brett StClair: different concepts. They'll want all the audits. They'll want to know what was reached, minutes achieved, all that kind of  
George Westbrook: Correct me if I'm wrong as well, Brett.  
Brett StClair: stuff.  
George Westbrook: Even even if with the sponsorship, say if it's build by impressions, we'd need like a Kevl in there to be able to track that.  
Brett StClair: Correct. Correct.  
George Westbrook: Okay.  
Skye Capazorio: So that's what I'm saying.  
Brett StClair: Now the reason why I'm looking at KVL it it supports  
Skye Capazorio: They tracking then the reporting mechanism.  
Brett StClair: sponsorships.  
Skye Capazorio: Okay.  
Brett StClair: Yeah. Otherwise it's building an ad server out ourselves which I just  
Skye Capazorio: Yeah.  
Brett StClair: it's a big job.  
Edwin Johnson: I wouldn't build anything until we actually have advertisers. I mean, because I mean,  
Brett StClair: Right.  
Edwin Johnson: it it looks like the number one advertiser for the inplay trading challenge is going to be me. I don't need an ad server.  
   
 

### 00:20:53

   
Brett StClair: You just place it and we'll put a photo of your  
George Westbrook: Yeah.  
Edwin Johnson: I have a better picture.  
George Westbrook: Everywhere.  
Brett StClair: face.  
Edwin Johnson: I have a better picture than my face that I'd like to  
George Westbrook: Just  
Edwin Johnson: show.  
Brett StClair: Um, anything else that we need to talk about? Oh, Cody, uh, if you're doing the reviews and everything for the app, I just want to make sure you've got access to the content repository where we capturing all the meetings um, for each of the components. I'd love it if someone can give that a review because we're pulling a lot of the app build  
Skye Capazorio: Is  
Brett StClair: out of those meetings and the vault.  
Cody Haugen: Yeah, the vault.  
Brett StClair: Yeah. Um, and I I'm I'm making some decisions when it's not sure.  
George Westbrook: Yeah.  
Cody Haugen: Yeah.  
Brett StClair: George is making some decisions when he's not sure. And I'm hoping I've made the right decision, but it's probably worthwhile getting your eyeballs onto that to make sure that some of the right decisions have been  
   
 

### 00:21:54

   
Cody Haugen: Yeah. No, I will I will certainly review um that I mean for the sake of time I mean I  
Brett StClair: made.  
Cody Haugen: think yes some executive dis you know decisions do need to be made and then let's review the product that comes out of it because right like as we've talked about iterating on the product is is quick and and fast whereas going back and forth I I don't know I yeah I I'll review it um to make sure that there's any sort of uh discrepancies uh are are are cleared up.  
Edwin Johnson: Cool.  
Cody Haugen: Yeah,  
Brett StClair: Yeah.  
Cody Haugen: I'm just I'm just trying to keep us Yeah,  
Brett StClair: Just it's Yeah.  
Cody Haugen: I'm just trying to keep us lean and  
Brett StClair: Yeah. Yeah. Yeah. Um I mean it's not major.  
Cody Haugen: mean.  
Brett StClair: Just do a quick whip  
Edwin Johnson: Real real quick. Sorry to interrupt you, Brett. Apologie. Um, I'm supposed to have a call with uh somebody here on this group at 9:00.  
Brett StClair: through.  
   
 

### 00:22:49

   
Edwin Johnson: I need to postpone that call um at least 45 minutes, maybe an hour. Is that doable? whoever I'm supposed to talk  
Skye Capazorio: Yeah,  
Edwin Johnson: to.  
Skye Capazorio: that was the the lead gen call that's with Troy, Cody, Brett, myself, and you and we can move it.  
Edwin Johnson: Okay, I need to move it. At least for me.  
Cody Haugen: Yeah.  
Skye Capazorio: That's  
Brett StClair: No,  
Edwin Johnson: You guys should have without me.  
Brett StClair: no, I think Yeah,  
Edwin Johnson: That's fine,  
Skye Capazorio: fine.  
Brett StClair: I was about to say why don't we just let's do the call because we still need to get the work done and then  
Edwin Johnson: too.  
Brett StClair: Edwin we can do a call later in the day whenever it suits you.  
Edwin Johnson: Sounds good. All right, all have a great day. Thank you so much.  
Cody Haugen: All right.  
Max Kingaby: Uh,  
Cody Haugen: Talk to you  
Brett StClair: Thanks everybody.  
Max Kingaby: I just wanted to say I redeployed the websites,  
Cody Haugen: later.  
Max Kingaby: guys. So, if you want to take another look when you get a chance,  
Skye Capazorio: Oops.  
Max Kingaby: it should have the  
Brett StClair: Yeah.  
Max Kingaby: updates.  
George Westbrook: Perfect.  
Skye Capazorio: Great. Thanks so much, Max. I'll I'll put in the feedback there now.  
Cody Haugen: All  
Skye Capazorio: Well, I'll go I'll start going through it now to give you all the feedback.  
Max Kingaby: Awesome. Thank you guys.  
George Westbrook: Let's f******  
Max Kingaby: See you.  
George Westbrook: go.  
Skye Capazorio: Okay.  
Max Kingaby: Let's go.  
Cody Haugen: right.  
Brett StClair: Let's go.  
Troy McDonald Kane: Thanks.  
Cody Haugen: All right. Thanks,  
Brett StClair: Thank you.  
   
 

### Transcription ended after 00:24:05

  

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.

**