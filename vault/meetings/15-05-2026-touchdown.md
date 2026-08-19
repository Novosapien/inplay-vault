---
description: "Transcript of the 2026-05-15 InPlay touchdown call — tZERO debrief and GCP direct connect, in-app feedback flow, website demos, and Sportradar data plans"
---

**

May 15, 2026

## InPlay Digital TouchDown - Transcript

### 00:00:00

   

 

### 00:01:20

   
Brett StClair: I really like their use of a distributed ledger.  
Troy McDonald Kane: that.  
Brett StClair: I mean, it's incredible where it's gone. Hey, like 5 years ago that kind of processing speed was unheard of. You could maybe do couple of hundred transactions a second. I mean, that's just insane. It's like like wow. Very impressive stuff. That was that was very very cool.  
Troy McDonald Kane: Yeah.  
Brett StClair: And the it's nice to see that they've also got the flexibility cuz you like this app's going to evolve fast and so you need a partner downstream as well that's  
Troy McDonald Kane: Heat.  
Brett StClair: adapting um quickly too and it's quite nice to see that they've got that flexibility. It's really nice. Really really nice.  
Troy McDonald Kane: Yeah, I don't know if you know the history of tZERO, but uh they were the first um special purpose ATS to get approved in the United States for tokenized assets uh many years ago. And so they've, you know, they were kind of one of the pioneers as well in how to bring um a digitalization element to, you know, equities and fixed income was what they were focused on.  
   
 

### 00:02:38

   
Brett StClair: very nice.  
Troy McDonald Kane: Uh ICENYSC is an investor in them and they uh they they have four primary, you know, offerings right now. you know, doesn't trade that much, but you know, they have about 30,000 active accounts that trade at any given time on their on their  
Brett StClair: Sure. I mean,  
Troy McDonald Kane: platform.  
Brett StClair: I quite like that they've got most of their kind of non ledger stuff up on GCP and have got a direct connect in play. Um, like I was dead serious about trying to leverage that direct connect. It can take time to get a direct connection even though it's with a serious data center in GCP through different partners and new accounts. These things take time and just can't remember the process but it is pretty easy connecting a GCP connection to a GCP connection and then leveraging and funneling through. Um, it's just getting the steps right cuz that could save 3 months just in application processes and that'll speed things up massively. So that direct connect is a real asset that they have into GCP.  
   
 

### 00:03:53

   
Brett StClair: Um, if we had done this in AWS and they needed a direct connect,  
Edwin Johnson: Were  
Brett StClair: you've got a threemonth application weight straight off the bat.  
Edwin Johnson: you pleased with that meeting today,  
Troy McDonald Kane: Yeah.  
Edwin Johnson: George Brent?  
George Westbrook: One thing that surprised me is the flexibility. It wasn't I was expecting no this has to be done this way.  
Edwin Johnson: outside.  
George Westbrook: No, this has to be done this way. And it was no, you want that? That's fine. We can do that. Oh, you want a million trades in one go? Yeah, fine. No queueing. It's fine. Just fire them at us. which was it was relieving because when when we've all been debating the architecture obviously without without having speak to them we had to obviously account for worst case scenario. Okay, what if it's only 25 me 25,000 messages a second. How are we going to handle that? But the fact they're like no just whatever you want we'll work with you is really really really  
   
 

### 00:04:46

   
Edwin Johnson: Yeah,  
George Westbrook: handy.  
Edwin Johnson: I mean Troy and I had a call with um Al who was on the call today and their CEO. Um I don't know if Troy, you've set the table for what an impact uh we are to them. It's a massive opportunity for tZERO to really push forth their their whole mantra of tokenization blockchain because they don't have any products that are are compelling enough to trade on the weekends yet. Like they're they're I don't know how I don't know anybody who's been more all in on us than them.  
Troy McDonald Kane: Yeah.  
Edwin Johnson: I mean, it's George. I think regardless of what they ask or what we ask, they're going to try to  
George Westbrook: Yeah. Yeah.  
Edwin Johnson: accommodate  
George Westbrook: Is I suppose that's the that was the only thing before the call when when when they said it was only 30,000 um active accounts. I was thinking 30,000 and then if somebody unmuted  
Max Kingaby: Tight th00and.  
George Westbrook: um 30,000 and we're going to be coming up them with millions over the next year.  
   
 

### 00:05:49

   
George Westbrook: Is that going to be an issue? But the fact that they seem so calm when we said million trades a second, three wallets, three million a million users, three three million wallets and they were like fine. And I think I spoke Troy what you brought up the other day about having to potentially wait days for the the trading account. I think we all thought, "Oh no, what are we going to do there?" And it's,  
Edwin Johnson: Right.  
George Westbrook: but they've obviously settled that concern um pretty pretty  
Edwin Johnson: Yeah. So, I mean that I think they're going to work with us to the best of their ability.  
George Westbrook: quickly.  
Edwin Johnson: I I mean they're they're incentivized and you know I talked to their CEO. I mean, they they may want to buy some equity in in play. Um, and and you know, that they're they're willing to commit some money towards advertising as well. Um, so that they're we're fully fully aligned and I I was very pleased with the call, but a lot of that techno garble geek stuff that you guys speak, I mean, it's just way over my head,  
   
 

### 00:06:48

   
George Westbrook: We just we just make it up,  
Edwin Johnson: you know what I mean?  
George Westbrook: Edin. We I was speaking to the TZ guys before. I was like, "Right, we're going to need to seem smart here, so let's just come up with some random words so that uh  
Edwin Johnson: Well, for what it's worth, you know, the TCPGB or whatever you guys are talking about, I was blown away. So, well, well done, George. It was a mission accomplished. And the app looked absolutely amazing. And um you know, I'm I'm a horrible person in a sense. I've been a trader for too long, you know, and on trading floor, Troy will attest, every person's the just disgusting people. We always swear and we're just on CO. And when I saw the app, I get so excited I resort back to, you know, f*** and all the rest of it. So, and I'm not really supposed to say that s*** in the house, but I try to get away with it, but I get in trouble. So, um, but yeah, I mean, it just looks awesome.  
   
 

### 00:07:42

   
Edwin Johnson: You guys are doing a great job.  
Troy McDonald Kane: Yeah.  
George Westbrook: Perfect.  
Troy McDonald Kane: One of the things that we when we talked to the TZ leadership yesterday, we talked about how great the app is coming along and they were like, we would love to get a look at that because our app is crap and we may want to leverage that for their app because they've been struggling to get both desktop and mobile app. They don't have a mobile app. They just have a a web-based app.  
Edwin Johnson: Weapons.  
Troy McDonald Kane: Yeah. They don't have anything that's as sophisticated as what we're building with you guys.  
George Westbrook: Yeah.  
Edwin Johnson: Yeah.  
Troy McDonald Kane: And so there might be an opportunity and uh which I think is is promising that when we go live in production that we can work to integrate the trading challenge app into a production app for their broker dealer that also our securities through their broker dealer and any of the other instruments that they have trading on their blockchains.  
   
 

### 00:08:32

   
George Westbrook: Yeah, cuz I could kind of tell from what some what they were saying about when we where we deploy the application, how we deploy the application that it was more web- based because effect what what we do is it's it's React Native. So it's native to the actual mobile. So effectively the server kind of runs on their phone. Um so it's each thing's a different connection. Obviously we'll have some things deployed. Um but yeah, like say when we the framework that we're using for it, we can quickly spin up a web version and then obviously down the line maybe a dedicated web version that's just super super focused on that. Um I suppose oh that was one update I kind of went I suppose yeah I'll do updates from from our side now um one of the updates so every first has everybody got the the inplay admin login  
Edwin Johnson: You know what,  
George Westbrook: now  
Edwin Johnson: George? I'm going to I had a full day yesterday. I haven't logged in yet, but I  
Troy McDonald Kane: Yes.  
   
 

### 00:09:26

   
George Westbrook: that no worries it's yeah sorry about the mess with authentication I was sat down with Sky the  
Cody Haugen: Yes.  
Edwin Johnson: will.  
George Westbrook: other day and basically it's because I sent you the old in there was something cached on the computer which meant that the invite was invalid. So I was like just create the passwords and send them to you and then that'll work. Um  
Cody Haugen: And we have sorted you just real quickly on that,  
George Westbrook: so  
Cody Haugen: George. we have sorted kind of the workflow of review and stuff. So um we'll work a daily timeline uh internally on the inplay  
George Westbrook: Mhm.  
Cody Haugen: side to consolidate and roll all feedback up and then I will be the submitter the one submitter approver. So anything anything you see with my name on it just take as already  
George Westbrook: Okay.  
Cody Haugen: consolidated uh feedback there.  
George Westbrook: Okay, perfect.  
Cody Haugen: Yep.  
George Westbrook: Oh, so I think my internet dropped there a second. Um, let me go back to that. So, new thing on the app, this ugly looking green button is not going to be in the actual application.  
   
 

### 00:10:34

   
George Westbrook: All it's for is similar to the website. It's just for feedback purposes. So, let's say you're on a page. Um, click that. It will probably prompt you to log in. So, just log in. Um then still trying to work on making sure because the balance is showing every single component and being able to click it and then obviously not making it look too crowded. So there might be sometimes where you're trying to click something and it it doesn't get the right thing initially maybe sometimes default to the drawing mechanism. Um but you can click on a component add add the note similar to the website uh and then with the shapes as well and add the note submit and then it's going to go into the admin panel for us all to see. Um, same thing. This is the internal version.  
Edwin Johnson: George, and when do you see yourself trying to implement more of these ads into  
George Westbrook: Um,  
Edwin Johnson: it?  
George Westbrook: the thought process is really going to start next week.  
   
 

### 00:12:02

   
George Westbrook: Um because the so with the some of the shortcomings with the with on the say team page for example what what what real value does that provide? We want to be seeing past performance maybe the ability to drill down more into games. It's just what the approach we've taken is let's get like the the highle pages. So these ones and then a little bit of nesting and then what we're going to focus on over the next week is let's get the rest of the pages not nailed but conceptually there.  
Edwin Johnson: Yeah.  
George Westbrook: Um so then we can take it as not a blank canvas where we're just plopping adverts in and rejig rejigging things around it. Um we'll get this in. We'll look at what's valuable in terms of advertising on certain pages and then how do we seamlessly link it in so it's not just like banner ad banner ad um um because  
Edwin Johnson: Yeah. Yeah. Yeah.  
George Westbrook: the other components that we we're going to be working on adding are obviously the third  
Edwin Johnson: Cool.  
   
 

### 00:13:06

   
George Westbrook: space so architecting that out as well um and the education and on boarding as well because on boarding we can we might test that in isolation to start with Um but then it's once we've got that going the Face ID so that when a user's logging in, we was researching that the other day. Um Face ID on the phone to login. But obviously for on boarding it needs to be needs to be done and then it's just setting up the markers. At what point do we capture the Face ID blah blah blah things like  
Edwin Johnson: Yeah.  
George Westbrook: that.  
Edwin Johnson: Um and and the my purpose for asking is selfishly. Um I want to try to sell as as soon as possible as much uh ads as I can.  
George Westbrook: H Yeah.  
Edwin Johnson: I actually got uh two two new meetings with two um sports agencies. um through some of my connects to uh yesterday. So, you know, be I want to be able to say like, hey, you know, I I just need a little demo something  
   
 

### 00:14:02

   
George Westbrook: Yeah. Yeah. Yeah. Because what one of the things working on as well is getting this.  
Edwin Johnson: some  
George Westbrook: So obviously at the moment it's just on my machine. Um, but making sure it's it's deployed somewhere so that wherever you are, you're able to access it um without having to publish it to the app store, download the app because like we said, if if if we publish it, they reject it. It then there's the whole back and forth process. So just finding a way that we get that app feel on your phone so that when you're in a meeting and they're like, "Oh, what's it going to look like?" You just go like that. Um uh and then I suppose the other things  
Edwin Johnson: Thank you.  
George Westbrook: from our side. So the Max maybe is it worth talking about the website the the landing page one?  
Max Kingaby: the paper.  
George Westbrook: Yeah.  
Max Kingaby: Yeah, sure. Um, I'm meant to be speaking to Sky about it this afternoon, kind of giving her the first overview of what I've built so far, but if everyone's got the time, I can share my screen and show you where my initial hit has got to.  
   
 

### 00:15:07

   
Max Kingaby: Um, just kind of bear in mind the wording and language right now hasn't been perfected. It's more just from a design point of view.  
Edwin Johnson: Cool.  
Max Kingaby: Um, hopefully me and Sky will have that sorted by this afternoon.  
Edwin Johnson: Wow. So  
Max Kingaby: So, yeah, very clear.  
Edwin Johnson: cool.  
Max Kingaby: There's a countdown. Obviously, we if Yeah, I've just put it as um August, but we can get more precise with dates as and when we get closer to the time. Um clear obvious photo of American footballer on a trading app. Um very simple website. Not really not a whole lot of stuff. Just very straight to the point trying to gauge interest. Uh got this image down here which I think I'm going to do a couple more changes to. Um it Sorry,  
Edwin Johnson: Is that Brett in a helmet?  
Max Kingaby: is that Brett in a helmet?  
Edwin Johnson: Is that right?  
Max Kingaby: 20 years younger and a bit better looking, but perhaps. Um, and then yeah, you just encourage the user to fill in the form.  
   
 

### 00:16:27

   
Max Kingaby: Um, yeah, it's just a very short, very simple website. I've also made some changes to the website I showed you guys the other day. Um, I I can try and launch that as well. Uh George, if if you've got anything to add your side whilst I try and launch that, feel free to. Might take a minute or two.  
George Westbrook: Um, let me think. Yeah. So, that's another thing we're doing as well is finalizing the what we're calling the inplay vault. Matt's probably don't show your screen. Nobody wants to see you clicking through all the uh the projects. Um yeah, so working through finalizing the vault so that you've all got something to read over the weekend if you didn't have anything planned. Um getting that nailed and then I say getting the changes on that. I mean I'm pretty confident that it's it's got what what we all discussed, but there's always there's always something that we might have missed, might have misinterpreted things like that. Um, like I said, we'll be getting the app deployed so that we can start collecting the the feedback on that as well.  
   
 

### 00:17:41

   
George Westbrook: And don't be afraid of hurting our feelings. Always just be be as brutal brutal as you want or feel. Um, because at the end of the day,  
Cody Haugen: agreed.  
George Westbrook: we both both parties want it to be as close to perfection as possible, if not perfect.  
Edwin Johnson: Sounds  
George Westbrook: And I think I think one one thing that we're going to critically think about next week is in terms of  
Edwin Johnson: great.  
George Westbrook: prioritization as well. So obviously ideal world we have everything um everything is perfect, everything's up and running um by August, but then having a sort of priorities list of okay, right, these these things are musthaves. If this is not there, there's no point us even releasing it down to, okay, this would be quite valuable for a user. Um, but if it's not there at launch, um, that that's not that's not vital. It's not to say that that thing right at the bottom won't be in at launch. It's just obviously tight tight deadlines. We we've got to be prioritizing certain things.  
   
 

### 00:18:47

   
George Westbrook: Um, and what what we're going to be doing as well from the start of next week is let's get some live data in there. Obviously with tZERO, there might be a little bit of a a wait for that once we've aligned on our side and their side. Um, but things like Sports Radar, I mean, after that call the other day, Cody, I mean, the documentation's amazing. Um, it's they've got the simulated stuff. So, there's there's no reason we can't be pulling in live data.  
Cody Haugen: There.  
George Westbrook: Um, but I think it's just conceptually first. We want to know like what's going to be on this page, what's going to be on that page before we start building out the microservices for fetching for fetching the real  
Edwin Johnson: So, George,  
George Westbrook: data.  
Cody Haugen: Does it  
Edwin Johnson: you're pleased with that uh interaction with sport radar  
George Westbrook: Yeah. Yeah.  
Edwin Johnson: then?  
George Westbrook: It's I mean I think before the call we we sat down like right let's think right what do we need to know look through the documentation the answers there.  
   
 

### 00:19:38

   
George Westbrook: Oh this other thing right do they do simulated simulated data? Yes that's there. It's kind of like you you kind of answered our questions already before this call with the documentation.  
Edwin Johnson: That's  
Cody Haugen: They do take a lot of Yeah, they do take a lot of pride in being self-service.  
George Westbrook: So,  
Edwin Johnson: great.  
Cody Haugen: Um, does it make sense, George, to schedule um I don't think we need, you know, 90inute modular meetings with potentially everyone on it. Obviously, whoever wants to join can join, but do we do we do more like shorter breakout sessions next week uh in those specific like within the page of what data points and kind of the structure of of what we want to show through the sport radar data or do you on the the other side of that coin,  
George Westbrook: No.  
Cody Haugen: would you rather just me explain that in a feedback bubble and go that route? I I just want to be efficient but also clear I guess on what kind of the vision I have or we have uh for these for these data points and how we want them  
   
 

### 00:20:40

   
George Westbrook: Yeah. Yeah, to I think a bit of both.  
Cody Haugen: shown  
George Westbrook: I think it would be valuable if we go through all of the kind of let's call it sports radar um related stuff related to games, things like that. We'll we'll we'll get some more pages sorted out, get it all refined, then we can sit down and be like, "Right, here's the pages we've got. What do we want to see on here? What do we want to see on here?" Um which is sometime sometimes what we do with our division  
Cody Haugen: Yep.  
George Westbrook: modules, components, subcomponents, things like that. Sometimes there's a need to do further workshops on certain subcomponents, sometimes there's not. Um, I mean, we've got obviously a lot of detail, but I think like you said, the sports radar data, um, that's something we really, really probably do need to maybe align on sometime next  
Cody Haugen: Yeah. No, sounds great. I mean, you you guys let me know.  
George Westbrook: week.  
Cody Haugen: I'm ready and available, you know, to walk through it.  
   
 

### 00:21:33

   
Cody Haugen: Um, it's just more from like the visualization packaging of it.  
George Westbrook: Hey  
Cody Haugen: Um, and and not so much like should we display this or not um or showcase this data point. It it's more like just how we package package it up. realization that I've seen from my experience is valuable or not valuable and that type of thing.  
George Westbrook: Yeah.  
Cody Haugen: So, um yeah, that that works great. And then as far as like phase two, when you say phase two, is that two weeks after launch? Is that a month after launch? Just so I can kind of understand as we start to frame uh you know formulate and prioritize things is so like I'm thinking a perfect example is that research tab, right? a user can go in and start to create like very defined reports and break down  
George Westbrook: H.  
Cody Haugen: different statistics, keeping them all within our app instead of going to different apps to to to do that research. Um,  
George Westbrook: Yeah.  
Cody Haugen: that I see is truly a phase two at this point.  
   
 

### 00:22:37

   
Cody Haugen: Um, but what does phase two I guess high level mean to you guys? We've never really established that.  
George Westbrook: Yeah, I I suppose it's one of those like like we me we don't don't want it to be like a big shabbam every month, two months where it's like here's this big release blah blah blah. I think obviously Brett mentioned about that sometimes do have to do some bigger releases.  
Cody Haugen: Yeah.  
George Westbrook: Ideally for us, like we've said, we don't want to be falling into that users having to wait a month for a feature. Like obviously once it's once it's out in the open, there's obviously the things that we think should be in phase two, but then obviously or phase 2, three, four. Um but also what what are the users saying? Um are they crying out for that research tab or are they crying out for the an expanded community section? Um, and one of the things I suppose we need to think about and integrate is the the product analytics. So there's obviously there's what users say they want and what they actually do.  
   
 

### 00:23:39

   
George Westbrook: Um, like how do they interact with it and like the things we're talking about like the the maps and things like that or the eye heat maps. Um, but also like the finger trails what because I suppose we're we're assuming what a user journey would look like. um they might be completely different. They might go discover tab, buy, then go off. They usually do that quite a lot. So maybe we need to make that experience a bit quicker. But the fa yeah the phases I wouldn't say there's kind of like a definitive timeline as it like this will be one month after launch, this will be two month. I suppose it's when we when we kind of sit down and scope it out that's that's when it becomes a bit more clear on the on the timelines.  
Cody Haugen: Great. No, that that makes sense. I mean, yeah, absolutely. User feedback is paramount. So, no m total sense. We can build what we think is awesome and it might not be  
   
 

### 00:24:31

   
George Westbrook: Yeah,  
Edwin Johnson: Yeah.  
Cody Haugen: awesome.  
Edwin Johnson: So the the only other thing that I would say we need to be somewhat considerate of  
George Westbrook: that's  
Edwin Johnson: is what the advertisers come back with.  
Cody Haugen: True. Yeah,  
Edwin Johnson: Right? So those would probably take precedence over the user if it's not like some big overhaul or something,  
Cody Haugen: absolutely.  
George Westbrook: Yeah.  
Edwin Johnson: right?  
George Westbrook: Yeah. Um, I'm trying to think what else. What else is there we got? Oh,  
Edwin Johnson: Cool.  
Max Kingaby: that server running if you  
George Westbrook: that's Yeah.  
Max Kingaby: Yeah. So, this is the main website that I showed you guys the other day. Um, have made quite a lot of the changes from the meeting. And once again, this needs to kind of go past Sky first, but just so you can kind of see what we're working with. Don't know if you guys remember this little animation we got at the start. then goes down and what you'll have is an animation of the app here.  
   
 

### 00:25:29

   
Max Kingaby: Um, and what we'll actually have is, as I said the other day,  
Edwin Johnson: Mhm.  
Max Kingaby: we'll have the actual app interface here. Um, this is just a mockup I've got. Um, what I've also done at the top is we had I think we had six different pages across the top of which you guys were saying some of them aren't necessary and all we needed was a home about and advertising. I've added an investor page. If you guys really don't want it,  
Edwin Johnson: Mhm.  
Max Kingaby: I can remove that. Um,  
Edwin Johnson: I like it.  
Max Kingaby: cool. Um, it's the about page. spinning basketball I thought was quite cool trying to add a few other sports in there. Um, this is what your investor page looks like. It's quite short, the investor page, so I can actually combine it with the advertising page if you guys would prefer that. It's totally up to you  
Edwin Johnson: I like the I like that it's standalone.  
Max Kingaby: guys.  
Edwin Johnson: Sometimes when I see a website with just a couple of buttons, I think b*******, you know.  
   
 

### 00:26:32

   
Max Kingaby: Well, there you go. I I'll I'll keep that in. Um advertising page. Quite a cool little animation there of multiple different sports balls coming out.  
George Westbrook: Um the baseball golf balls as  
Max Kingaby: Um  
George Westbrook: well.  
Cody Haugen: Yeah.  
Max Kingaby: yeah, George's pet peeves that is I I'll I'll try to change that. It's quite quite difficult. Um and then finally  
George Westbrook: Get that changed. And then finally,  
Max Kingaby: the partner with us page which is just a form to kind of register your interest um depending on who you are, your company, job title, etc. Um and then there is this option to view it all in a light mode. Um,  
Edwin Johnson: Mhm.  
Max Kingaby: but I need to configure this a bit better because it doesn't quite work across the whole website. But you can kind of see where we're going with it. Um, so  
Edwin Johnson: It's awesome. Yeah, it looks great.  
Max Kingaby: yeah,  
Edwin Johnson: Obviously, some of the copy we'll we'll work on, right?  
   
 

### 00:27:36

   
Edwin Johnson: like that. So, we're not the first regulated marketplace for sport. Those would be, you know, um Kouchy and Poly Market. We're the first uh regulated equity marketplace for sport. So, we're we're the first one who's ever come up with uh stocks, not not futures contracts.  
Max Kingaby: Okay, I appreciate that. I I'll add that in. Cheers,  
Edwin Johnson: Yep. Thank you.  
Max Kingaby: Evan.  
Edwin Johnson: Great work, Max. We really appreciate it.  
Max Kingaby: Thank you very much. Cheers.  
Cody Haugen: So then yeah, just one last clarifying point from my side.  
Edwin Johnson: Yep.  
Cody Haugen: So all of this George is going to be uploaded and started this weekend, early next week. So we should be really up, you know, really full speed ahead on that feedback loop say Tuesday, Wednesday, I mean sometime middle of next  
George Westbrook: the there's one there's like some ID verification aspect in order to get the  
Cody Haugen: week.  
George Westbrook: the app deployed. Um so I was sat there yesterday just refreshing my page like come on make is it done yet?  
   
 

### 00:28:42

   
George Westbrook: Is it done yet? That's that's the real only blocker on that. Um which unfortunately I can't control. Um if it's done this afternoon, I'll get it sorted over the weekend. Um if it if it's not, I'll obviously keep you guys in the loop. Um but like I said, the it's at the point now where we we need that feedback. It's it's yeah, like it's a priority for all of us so that that we're we're getting that iteration going as quick as possible.  
Cody Haugen: Yeah, exactly. So, yeah, just shoot me a note um or shoot the whole team a note uh when that's up and running or otherwise I can let the team know that we're we're ready to get rolling. But yeah, as soon as that's ready from from your side, just let me know.  
George Westbrook: Perfect. And Troy will be looking into the Slack stuff as well this weekend so that we're we're we're all linked up. Um because we're the the reason for the delay is we're currently on Rebel Labs Slack and then we're migrating everything over onto the Nova Sapion Slack.  
   
 

### 00:29:39

   
George Westbrook: And then I think I meant we'll use things Slack connect so that it's not you're joining our Slack or we're joining your Slack. We've just got channels that we can all see but then we've got the obviously the privacy within within each each workspace as well but we can obviously DM each other as well. Um so it's just just getting that sorted. It's the the issue we've got is a lot of our like agent auto fix and auto notification stuff linked onto the other one. So, it's just getting that getting that moved  
Troy McDonald Kane: Great. And then um for syncing with tZERO,  
Edwin Johnson: Great.  
George Westbrook: over.  
Troy McDonald Kane: does Friday mornings work or Friday afternoons work for you guys or do you want to do Thursdays? You know, is there a time slot? I think definitely at least, you know, until we get a beta out, it's good to to connect with them once a  
George Westbrook: Yeah.  
Troy McDonald Kane: week.  
George Westbrook: Yeah. To be fair, I think f Friday probably probably works.  
   
 

### 00:30:33

   
George Westbrook: Um,  
Troy McDonald Kane: Okay, great. Cool. Well, I'll get that cadence put on the calendar and we'll get that set up and we'll we'll reconvene with them next Friday.  
George Westbrook: yeah.  
Troy McDonald Kane: And uh you know, that's a great uh great path forward.  
Edwin Johnson: Yeah, and tackle everything I've already said. Really, the last couple weeks have been so much fun for us. I mean, we're having a ball and seeing the work you guys are doing, it's just awesome. We we very very grateful and  
George Westbrook: And it it's only going to get more fun as  
Edwin Johnson: excited. Yes, sir. All right. Great. Well, listen.  
George Westbrook: well.  
Edwin Johnson: You boys have a great weekend and we will look forward to catching up with you next week. If anything pops, please reach out.  
George Westbrook: Perfect.  
Troy McDonald Kane: Thank  
George Westbrook: And as we got to say,  
Edwin Johnson: Thank  
George Westbrook: end of every startup.  
Max Kingaby: Thanks.  
Edwin Johnson: you.  
George Westbrook: Let's f******  
Troy McDonald Kane: you.  
George Westbrook: go.  
Cody Haugen: Let's f****** go, George.  
Max Kingaby: Guys, have a good weekend.  
Cody Haugen: Have a good weekend.  
Max Kingaby: Did you say five?  
Cody Haugen: See you.  
Hasan Mohammed Ahmed: drinking guys too.  
   
 

### Transcription ended after 00:31:34

  

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.

**