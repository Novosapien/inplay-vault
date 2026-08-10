---
description: "Transcript of the 2026-05-27 referral programme call — multiplier-event calendar and KYC cutoffs, PWA fallback for App Store risk, agentic follow/share checks"
---

**

May 27, 2026

## InPlay Referral programme - Transcript

### 00:00:00

   
InPlay: That's Sunday or Friday to Monday at 11:59. Any questions so  
Brett StClair: repeat myself just so that I've got this clear. Cody,  
InPlay: far?  
Brett StClair: and just correct me if I'm wrong. Events.  
George Westbrook: Okay,  
Brett StClair: Uh we've got 5 6 7 8 9 uh referral events,  
George Westbrook: I'll shut that.  
Brett StClair: a 1x referral.  
InPlay: Sorry, you keep cutting in and out, Brett, on your  
Brett StClair: Sorry,  
InPlay: sound.  
Brett StClair: I know what that is. Sorry, sorry, sorry. We're all having issues. Oh, that's weird.  
InPlay: I mean, now I can hear you,  
Brett StClair: Um,  
InPlay: but yeah, it was just coming in and out, so I I haven't really heard what you're trying to say.  
Max Kingaby: trying to get them. Okay.  
Brett StClair: there'll be every Wednesday you get a one and a half referral dollar.  
Max Kingaby: So,  
Brett StClair: So that's one and a half times the amount of referral dolls we usually get, which is usually a,000.  
InPlay: Yep. So it'  
Brett StClair: Um 1,500 uh beginning of summer  
InPlay: be  
   
 

### 00:01:07

   
Max Kingaby: uh, Father's  
Brett StClair: June,  
Max Kingaby: Day.  
Brett StClair: that's a $3,000 referral essentially.  
InPlay: 3,000. Correct.  
Brett StClair: Um and those will so from  
Max Kingaby: This will just be from the through  
Brett StClair: 0 hours  
Max Kingaby: to  
Brett StClair: 359,  
InPlay: Correct.  
Brett StClair: right?  
InPlay: Yes.  
Max Kingaby: 20.  
InPlay: Any any referral that uses their referral code has to go through the complete process KYC sign up all that good stuff just like any other user would by 2359 to get  
Brett StClair: and  
Max Kingaby: So that 259  
InPlay: counted.  
Brett StClair: 359.  
Max Kingaby: So, I'm just going to be really specific for  
InPlay: You're  
Brett StClair: um and  
Max Kingaby: is they have to  
InPlay: correct.  
Brett StClair: gotten to the point where we've issued that referral dollar. So, it's right at the end of the process. So, if they get to 23 59 uh 58 and they've they've registered, they've done their KYC, but they haven't got to the part where they can essentially close out the dollars. We we wouldn't have issued the wallets yet because they're not having  
   
 

### 00:02:17

   
Max Kingaby: It's not going to be a wallet. show you what it  
InPlay: Exactly. Right.  
Brett StClair: at a  
InPlay: You don't have to worry about issu issuing the referral dollars.  
Brett StClair: point.  
InPlay: What we need to do is be able to automate and track when the signups that came  
Max Kingaby: is.  
InPlay: in for each of those referral uh referrals and automate that process at those  
Brett StClair: Okay.  
InPlay: specific times. That's what we need to worry about. And then we can always go back.  
Max Kingaby: I'm  
InPlay: Oh, I was just going to say then we can go back and if we have all of that that ledger basically  
Max Kingaby: guiding  
InPlay: automated, then we can just top, you know, top off the referral dollars, the referral wallets once the wallets are created.  
Max Kingaby: colors. Colors. Uh,  
Brett StClair: Um, and then the two kind of all the others are running on a 24-hour basis. The only two that are running beyond a 24-hour basis are 4th of July, which is from Friday morning 0 hours to Sunday evening 235959 and Labor Day weekend, which is running from Friday 0 hours to Monday 2359.  
   
 

### 00:03:32

   
InPlay: Yeah,  
Brett StClair: Right.  
InPlay: let me just fact check something uh real quick. Okay, it works. Uh I just want to make point sure Fourth of July fell on a weekend. It works. It's a It's a Saturday this year. because it's not it's not the same day obviously every every year. So, um nope, we're good  
Max Kingaby: One one thing we might need to think about if 20 21st of  
InPlay: then.  
Max Kingaby: June is that I suppose That's that's a month. Um, two options are we have the version of or have a version of the app in the app store. If there's an approval,  
InPlay: Correct.  
Max Kingaby: then it might have to be a PWA with Persona linked to all of the backend systems that we have look branded exactly the same as it would be. It's just a PWA, which means that we do not need to worry about any Apple or Android approval process as a fallback. Oh, that's a good idea. which we can still do.  
Brett StClair: We  
Max Kingaby: We can probably because we're using React Native,  
   
 

### 00:04:37

   
Brett StClair: can  
Max Kingaby: we can we can have a web version. Um, so what PWA is is  
Brett StClair: essentially a mobile website that's rendered pretty much like a mobile app. Um, and it's a nice easy way to at least still promote a QR code or get or get the link somewhere. So when people click on it, they're not necessarily downloading the app, but they're still able to get through the referral process and get into the app. Um, if we are struggle to get the app launched by the of June with Apple and all that kind of stuff, it's just as a fallback. same same code base, same everything without the wrapper that is the app.  
Max Kingaby: It's just we kind of deploy the points of failure there is the first approval process doesn't happen by that  
InPlay: Yeah.  
Max Kingaby: time, then there could be the approval process happens and it's rejected and it goes into a review and then there's obviously it gets approved. It gets approved that's all good. Um and then it's what are the fallbacks at if that happens which is PWA which is fine we  
   
 

### 00:05:44

   
InPlay: Heat.  
Max Kingaby: can get that yeah deployed wherever whenever um we don't need to worry about an approval process. So at least yeah at least if because obviously 20 yeah  
Brett StClair: risk risk management on  
Max Kingaby: 21st of June is yeah the first one 3x referral dollars as  
Brett StClair: that.  
Max Kingaby: well. Okay,  
InPlay: Uh sidebar gentlemen, just because it's the first time we're hearing about PWA,  
Max Kingaby: happy  
InPlay: at least myself. Um can we do that for the advertising piece so that we can get something like on our phones that we can show anytime on an iPhone?  
Max Kingaby: we push the the prototype that way. So may thought maybe with that because I think with React Native it's client rendered. Um we might be better if we create a NexJS version which  
Brett StClair: We  
Max Kingaby: is server rendered. Um I need to look into it to double check. Um good idea Cody. We'll have a look and might require  
Brett StClair: and see if we can get the code rerendered.  
InPlay: Okay.  
   
 

### 00:06:52

   
Max Kingaby: like a a full rebuild but which could take couple of days maybe a little bit longer. Um have a look at it.  
Brett StClair: It's  
Max Kingaby: Yeah, have a look at it. If we can run it in the background as a rebuild. Makes sense. Um, we haven't heard anything back. No, it's still showing. I've reached out twice and there still it's just for a normal Apple developer account.  
Brett StClair: Oh,  
Max Kingaby: Anyway, that's Yeah, but that's a good idea, J.  
Brett StClair: ready.  
InPlay: Yeah. Um, okay. So then, uh, back to the referral stuff here. So then, um, outside of the referral events, we also want to tie to not the co-branded influence advertising we were talking about yesterday, just influencing the users to interact with our materials. So this could be following and liking or sharing posts. This could be uh completing our education modules. Um and then through this to be frank we haven't given it an an exact um referral number of what that is. Um but I mean hypothetically it could be anything if we think obviously this stuff is valuable enough.  
   
 

### 00:08:21

   
InPlay: Um, and so that's uh open open to the team here, but it could be Yeah. surveys, it could be education, it could be uh sharing and liking posts, it could be anything. Yeah. I mean, anything that we want to push. And this also could be live too, like you know, it could obviously we wanted to adapt to what we want to push our users to do. So if it's a weekly or monthly campaign for something that we want to push then yeah it needs to be adaptive I  
Brett StClair: Yeah, I agree with you.  
InPlay: guess.  
Brett StClair: And even for some of the stuff that it's difficult to get APIs into like a follow and share, we'll run an agentic um team that'll just as it sees it come through, we do a verification that the following share has happened.  
InPlay: So that perfect perfect segue there, Brett, because that leads me into the last point that I wanted to cover is if you could share with me and the the entire inplay team. How does the automation work from your side and what is capable?  
   
 

### 00:09:36

   
InPlay: because this is the first time we've really talked about capabilities from the Novo side of of what we can do because obviously we can all come up with great ideas but if it can't be executed on then it's just  
Brett StClair: correct.  
InPlay: wallpaper  
Brett StClair: So we think that there's so first of all like building this is going to be you know how we build at the moment and it's building a building into the app building it into a PWA just code but then there's a bunch of functions and features and this is why we were like hold on don't go with a company that's just going to build it and you're going to static kind of stuff. We think there's a bunch of work that can be done through agentic AI. So let me explain what a gentic AI is. Aentic AI is essentially clippets or clips of code that we host and this code has three things attached to it. The first one is it attaches to a large language model. So be it chatpt, claw, google. It attaches itself to a memory and it it attaches itself to a tooling.  
   
 

### 00:10:48

   
Brett StClair: And so we build these, we build thousands of these the whole time. In fact, we have agents that build these agents. And that clip of code um that's created is this new technology called an agent. So picture um if you want this agent to take over your machine and do something, it will take over your machine and take control of your browser and start going through your browser. if if there's a connection through an API to um say Instagram and it feels it can double check and go build the code to create a formal connection and then it monitors that connection, it'll do that. And so these are very intelligent pieces of code that we are going to train. So we build them, we train them, and they're able to do these tasks that one could never imagine before. And so an example of that is um you say to uh a follower please can you share like and CC a friend in it. So if you look at a lot of those campaigns what the advertiser often asks is please can you at us share but make sure we're included.  
   
 

### 00:12:04

   
Brett StClair: So we can actually go manually just double check if you have won something. We double check that you've shared it and you've included us. If you haven't, well then you're not going to win anything. That's how it kind of works. But what we can do with agents is we can say we'd like you to constantly monitor the inplay  
InPlay: right?  
Brett StClair: site. We'd like to also every time someone submits a referral if we're asking them to do a follow and a share, they need to submit their um their personal tag, right? Their Instagram code or address. Um they put it in there. We ask them to tag and play, but they might not. But we can then go check that they've done the post, that they've liked the post, that they've done something, and we literally, it's just one agent that goes off and checks that one person, okay, you have done it. It comes back to us, tells the database, that's all done. You can sign off on that referral.  
   
 

### 00:13:06

   
Brett StClair: Now, imagine the world before agents. Impossible to do with code.  
InPlay: Right.  
Brett StClair: The only way you could do it is manually go check.  
InPlay: Yeah, that's  
Brett StClair: And so it opens up this this world for you guys that you know in the beginning you're going  
InPlay: amazing.  
Brett StClair: to struggle to think of things. Don't worry. We also like ah what else could we do? But I mean if I look at our insurance clients um it goes and checks brokers emails. It reads the emails. It extracts uh insurance information. It goes and double checks that they've been sanctioned and tobed and feeder and and for that particular email that's been sent to it. It then goes and into their systems and goes, "Is that already registered? Is this a customer we can do business with?" It does all of that and within 30 seconds it comes back to the broker and goes, "You're all good to go. This is what we've understood. These are things that have passed. You're willing to move on.  
   
 

### 00:14:02

   
Brett StClair: You can move on and we can ensure this person  
InPlay: there. Yeah, that's simply amazing. Brad,  
Brett StClair: You just couldn't do that.  
InPlay: um my one concern or or question to you though is  
Brett StClair: So that's why you  
InPlay: I mean once again we hope to have three million,  
Brett StClair: go.  
InPlay: two, three million maybe more users on this platform. How scalable is that reading? because each person could have Instagram, Tik Tok, Facebook, and and so yeah. Okay. Simply put, that's that's all I  
Brett StClair: So, so picture like a little that snippet of code we hosted on something called a container which is very much  
InPlay: need.  
Brett StClair: like all the your microservices that we're going to build for you are going to be hosted on a container. These containers spawn up and they spawn to the millions per second real time and it goes away and does  
InPlay: Beautiful.  
Brett StClair: it gets it done individual work stream.  
InPlay: Yeah.  
Brett StClair: Don't worry about the scale. It does. It just does. Amazing.  
   
 

### 00:15:02

   
InPlay: Okay.  
Brett StClair: It's  
InPlay: Another idea just for uh uh as far as on your additional line there and to say out loud  
Brett StClair: mindblowing.  
InPlay: is um incentivizing someone to share their trade confirmation page. Um and build that into the share ecosystem of how we want to, you know, offer extra uh advertising value. um is when they share that page. Free value um to potentially a lot more  
Brett StClair: I like that. Oh, yes.  
InPlay: users.  
Brett StClair: Okay. Yeah, I remember that. Yes.  
InPlay: Yep.  
Brett StClair: I'm My brain's going to advertise a campaign error as your share ecosystem.  
InPlay: Um  
Brett StClair: Is Is that what you're talking about? Is that what you mean?  
InPlay: the the sharing the trade confirmation page. Sorry, say that again, Brad.  
Brett StClair: Oh, when you talk share ecosystem, do you mean that area where the advertiser can host their own kind of campaigns and you  
InPlay: No, separate. So on that trade confirmation page,  
Brett StClair: drive  
InPlay: so after you click trade by two clicks, you get that confirmation trade that comes up and then on that page, right, we were going to have the share buttons, uh message, email, Instagram, Tik Tok, whatever the main ones are.  
   
 

### 00:16:23

   
InPlay: and then uh one click that and it it it populates with you know that image or whatever and we connect those dots. If we are incentivizing people to share that trade confirmation page we can make that more of an ecosystem of a just a cultural thing within our app within our  
Brett StClair: That's very nice.  
InPlay: platform.  
Brett StClair: That's very nice. I like that.  
InPlay: Um yeah.  
Brett StClair: I really like that.  
InPlay: Um that concludes Cody's TED talk on the referral system. If anybody else has thoughts or um but that's my download there, folks.  
Edwin Johnson: Nice work.  
InPlay: Thank you.  
Brett StClair: I think it's good. I think it's clear.  
InPlay: Okay, let's get to work then.  
Brett StClair: I don't have any further questions. Thank you very much.  
InPlay: Yeah. Awesome. Well,  
Brett StClair: Um,  
InPlay: thank you guys for sticking around  
Brett StClair: that's awesome.  
Skye Capazorio: We're going to have we've got a 30 minute break now and then we've got the website  
InPlay: longer.  
Skye Capazorio: conversation after that.  
Brett StClair: Is that perfect? Is that perfect, Sky?  
Skye Capazorio: Yeah. Yeah, that's all  
Brett StClair: And we'll hop onto that call and then I can close this out,  
Skye Capazorio: good.  
Brett StClair: get it all published and get it into the  
Skye Capazorio: All good. All good.  
Brett StClair: vault.  
Skye Capazorio: Um Edwin, we've got the social sorry that social call with Georgia now. Um if you're okay to join that.  
Edwin Johnson: at 10:00 10 minutes.  
Skye Capazorio: Yeah.  
Brett StClair: Cheers,  
Edwin Johnson: Okay,  
Brett StClair: guys.  
Edwin Johnson: cool.  
Brett StClair: Thank you very much.  
Edwin Johnson: All right, have a great day all. Really appreciate your time today.  
InPlay: Thank you.  
Edwin Johnson: See you.  
Max Kingaby: And huff out.  
   
 

### Transcription ended after 00:18:13

  

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.

**