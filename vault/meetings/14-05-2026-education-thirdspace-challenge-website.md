**

May 14, 2026

## Modules 6 and 7 - Inplay Simulator App - Transcript

### 00:00:00

   


### 00:01:57

   
Brett StClair: And we're going to base it kind of on the look and feel that we've got.  
Skye Capazorio: Yeah.  
Brett StClair: We're going to strip it down,  
Cody Haugen: Don't pick  
Brett StClair: get it out, published. Um, Kev, thanks very much for running with that. um his son manages all the production and deployment and all that kind of stuff. So he's the guy who's going to need access to your domains.  
Skye Capazorio: See  
Brett StClair: He'll run the push through that and we just build like a mini CI/CD pipeline um as soon as  
Skye Capazorio: that?  
Brett StClair: they're ready. I think these build like a temporary one just to make sure that we've getting ready while we get the final design nailed out and we will spend some time with you Sky just to review first before we push it to the official site.  
Skye Capazorio: Sure, that's fine. I would I would also like to share the link obviously with um with the team the team here  
Brett StClair: Okay,  
Skye Capazorio: for for review.  
Brett StClair: cool.  
Skye Capazorio: It's just the holding page so it it doesn't I think we're just going with bare minimum coming soon um buy sell hold etc the logo and then obviously the form so that we can carry on data capturing while we're still having the college um presentations over the next few days.  
   
 

### 00:03:04

   
Brett StClair: So this um form must be specifically for sign up for university.  
Skye Capazorio: Um  
Brett StClair: Hey  
Skye Capazorio: uh no so currently what we have is a form that has um various different entry points. I think it's like name, first name, last name, optional um mobile, email address and then we do ask whether like the name of your business or college um in terms of that input. So it's it's a bit more generic than that because it obviously opens itself up but the main spaces that people  
Brett StClair: Okay.  
Skye Capazorio: are being driven to sign up is from the college presentations and we just need to make sure uh just Troy Kevin while just so that nothing falls apart in this that the QR  
Brett StClair: Good job.  
Skye Capazorio: code Troy that you show um on your presentations we just need to test that it's linking back to make sure that none of the linking elements have broken in this transfer of just the holding page. of the main website and that the data  
Cody Haugen: Yeah. So that QR  
Skye Capazorio: is still being captured in the same place that it has been  
   
 

### 00:04:03

   
Brett StClair: It's  
Cody Haugen: Yeah.  
Skye Capazorio: before.  
Cody Haugen: The QR code goes directly to the put me in page on our current website and then once that's completed, it then flows through to the email and then goes into the Excel sheet.  
Skye Capazorio: Yeah.  
Brett StClair: the worst.  
Skye Capazorio: So, what I'm saying now is that um there's obviously not going to be an inplay form to go to.  
Cody Haugen: Yeah.  
Skye Capazorio: it's going to sit on this holding page because we're basically going to take down the current website as it is have the form available there. That's why I'm saying we need to make sure that the QR code link um is then going that it's going to still we put whatever update the URL in the back end of that QR code that's being used at the presentations um and then make sure that the data flow is linking as you said Kevin email and into the Excel sheet  
Cody Haugen: Sounds good.  
Skye Capazorio: but I would I would like that to be live tomorrow if we can just get consensus from everyone because then it allows us to start doing the pre-posting on social media before the hype video and then leading into the the main website which I will also then share um Edwin across our group um to get by to get alignment but those posts are very straightforward like something exciting is coming soon buy um hold etc. So, it's just more the tease of what's happening than definitive social  
   
 

### 00:05:40

   
Brett StClair: Um,  
Skye Capazorio: posts.  
Brett StClair: we're going to store the data into a database and we're going to push an email to you. So, at least it's being stored in a database and we'll give you access to that database. But we can also do an extract into a spreadsheet if that's easy easier for you guys. Just let us  
Cody Haugen: Well, we are uh in the midst of figuring out CRM strategy and locking that down.  
Brett StClair: know.  
Cody Haugen: So there will be an integration either into HubSpot or Vtigger pretty soon  
Skye Capazorio: Okay.  
Brett StClair: Okay, cool.  
Cody Haugen: so that we can that we can automate our email workflows on welcome email once they  
Brett StClair: Perfect.  
Cody Haugen: sign up, promotional emails, all that fun  
Brett StClair: Perfect. Perfect. Okay, we'll just do like a temporary store.  
Cody Haugen: stuff.  
Brett StClair: We're just going to bang it into Air Table. store it there for you and then push that through to HubSpot once you guys are ready.  
Cody Haugen: Perfect.  
Brett StClair: Um just a quick one just the landing page needs to cater for university students coming through and also an advertiser coming through.  
   
 

### 00:06:43

   
Brett StClair: Is that correct?  
Skye Capazorio: Um,  
Brett StClair: They come speak  
Skye Capazorio: I mean, yes,  
Brett StClair: to  
Skye Capazorio: I don't I don't I don't think that there's harm in having, you know, either one. I just don't want it to become messy and and complicated in terms of that. So maybe we can just add a field that's you know says whether you're you know a exactly but the  
Brett StClair: advertise. Okay,  
Skye Capazorio: but the anticipation is that the main website then is up towards the end of next week that then would have the  
Brett StClair: that's  
Skye Capazorio: advertiser section on it anyway.  
Brett StClair: So, so Sky, sorry Max here on the side. Press laptop. Um the the purpose of this landing page is for  
Skye Capazorio: Okay.  
Brett StClair: you guys to understand I suppose captivate  
Skye Capazorio: No. Okay. Hold on. Let me just like let me I'll just put a draw a line under it.  
Brett StClair: interest.  
Skye Capazorio: We're we're taking the current website that exists that you are modeling off to build the main website.  
   
 

### 00:07:42

   
Skye Capazorio: So like all the information that exists there the is not in our brand guidelines and it's obviously well it's part of the old brand guidelines. So there's a complete disconnect of that and we want to start getting things posted on social media, but we don't want to have the link in the bio from social media that then is going to somebody's going to click on it and then go to the current main website that is green and black and all of that sort of stuff. And the feeling is that the positioning on that, the wording on that isn't 100% right. So, as a short-term fix so that we can get going on posting on social media is to take down that main site, put this holding site that's in the new brand colors and just has the bare minimum coming soon um with what I shared in the email and the form capture so that at least that function is still capable of continuing until the main website is ready to go live. Does that make sense?  
Brett StClair: Yes. Yes.  
   
 

### 00:08:38

   
Brett StClair: Have you? Yeah. Okay. Yeah. I I'll knock something up and get I I've already been building something,  
Skye Capazorio: Cool.  
Brett StClair: but I just want to kind of know the direction of it. So, from what I've understood from this so far, I'll get you something pretty soon after this call and then you kind of let me know where it  
Skye Capazorio: Great.  
Brett StClair: sits.  
Skye Capazorio: Thank you.  
Brett StClair: Okie dokie. We enter our final module sprint. Um what are we going to be covering in this module today is going to be the third space education and then I think we should take the last portion of it to review the global oh sorry the challenge website and then we're going to do a separate session for those sections that essentially run all the way across like advertising. It's going to touch absolutely everything. Is that right, George? Did I get that right? My favorite George a muted  
George Westbrook: shut up. If if we get time as well,  
   
 

### 00:09:44

   
Brett StClair: one.  
George Westbrook: maybe talking about the the payout mechanism um if I know I know we briefly touched on it um and just in terms of obviously mechanism and then actually how we how we want it to flow as well.  
Brett StClair: So, what should we do first?  
George Westbrook: Oh, I think you're on mute.  
Cody Haugen: You're  
Brett StClair: You're on mute.  
Cody Haugen: on.  
Edwin Johnson: Sorry about that. Pulling a real George over here.  
Brett StClair: Yeah.  
Edwin Johnson: Um, somebody's got a lot of background over there. I don't know who's got it, but okay. Then then it's acceptable from you, Brett. I mean, that's about it, though. Um, no, Cody and I don't line on the payment uh schedules for all that, George. So,  
George Westbrook: Okay.  
Edwin Johnson: we we we probably need till uh at least close of business Monday, may maybe Tuesday in order to come back with with what that looks  
George Westbrook: Okay, that's fine. Yeah, that's so then I suppose today it's Yeah,  
Edwin Johnson: like.  
George Westbrook: education.  
   
 

### 00:11:07

   
George Westbrook: I think maybe if we do education first then the third space and then challenge challenge website at the end.  
Edwin Johnson: Yes, sir. Okay, cool.  
George Westbrook: Perfect. So I suppose yeah the education component um I suppose one of the things we need to think is what do we overall want it to look like best case scenario and then what is just essential um and I suppose if we just replay it back as I know we've obviously talked about the education a little bit um but how do you see users using it is it like we said is it is there a little bit of it everywhere there's also the dedicated page what information do they need to Get out and things like  
Edwin Johnson: Yeah. Um, you know,  
George Westbrook: that.  
Edwin Johnson: it it probably needs to start pretty basic. You know, how to click buy, how to click sell, you know, why you'd want to go long, the determinate, you know, the the language being long or short. Um my view is if we have these modules and again it may not work for the MVP but if we can compensate people for going through the education modules uh with some of those referral dollars or that can money can go in that referral bank.  
   
 

### 00:12:22

   
Edwin Johnson: I think it might add a little bit more gravitas to how many people go to the education portal or part of this and then um certainly would help um bolster Sky efforts um and and Cody's efforts to sell advertising around the uh education center. Uh if they're incentivized to do it, they're more likely not going to. Um, so yeah, I mean essentially it it you it would have to run the gamut. You know, you you you you can buy at an IPO. You know, what's an IPO? What does that look like? We can we can have uh you know, starting from scratch, download, you've got a 100,000 of uh inplay coins or whatever we're calling them to trade with, you know, risk management, all all the things that are necessary to actually engage with trading on a day-to-day basis. I think would be very helpful, but I would like to curb it at like maybe the top 12 modules or something, right? May maybe 15. And I'm not the right person to ask because I've been doing it so long.  
   
 

### 00:13:33

   
Edwin Johnson: I I I'm not a fair person. We We actually need to talk to someone who's really probably not a trader, you know, and how do we prepare them, you know?  
Brett StClair: Do we we see it as a separate icon, separate page, right? So when you need education,  
Edwin Johnson: So,  
Brett StClair: you go into it and then we kind of um you need a video distribution platform. it might be quickly quick quickest and easiest to load it onto a YouTube platform. So you can also distribute through your channels and then you pull it through and you can remove all the YouTube kind of iconography so you you don't really know it's YouTube. Um and so you're playing it through there. You're pulling the same content through there. We have like a showcase top reel where you slide across, you know, it doesn't autoplay in some of the contents. You can get bit of a highlights reel. Then you go down into different modules where you can click into it. You open it, turn your phone to the side, and you just do like a play through as you complete it.  
   
 

### 00:14:36

   
Brett StClair: We can add it to your lead kind of like your status. You've done x amount of courses, you're at this stage of the course. So, we want to always keep track how far you are with your courses. Um, so when you come back and you haven't, you know, you're bit stuck, haven't been on the platform for a while, you want to pick up where you left off. It starts with that last video that you've watched, you can see all the others are played. Are we thinking that kind of style?  
Edwin Johnson: I mean that sounds wonderful to me.  
Skye Capazorio: I so one of the considerations that I have around this space is um making it very uh what I don't know if this is the right word but like natively digestible by the audience that's going to be in there and making it very much like a scroll like literally like scroll real scrolling um essentially within that making it very very short in in each of them  
George Westbrook: Hey,  
Skye Capazorio: like I would aim for the you know the kind of reel to be uh 15 seconds max um in each of in each of those modules to not make it long- winded and make it in the way that this audience is used to consuming educational content.  
   
 

### 00:15:48

   
Skye Capazorio: Um, and and and so that it has a similar sort of feel to Tik Tok, to Instagram in that sort of way as opposed to like a stop, press play, YouTube, like find that sort of stuff. Um, obviously then being able to go somebody's watched that full reel to be able to then take that and and and qualify the points within the, you know, referral wallet. um is I you know I'm not sure how that how that works in terms of that um but but I would say the feel that I would want coming out of that is that that sort of feel. It should feel like you are consuming information like Tik Tok. I don't know Cody what you think in terms of  
Cody Haugen: I think it's brilliant.  
Skye Capazorio: that.  
Cody Haugen: Yeah. No, I think that's exactly how the short form should be or the educational content should be. Um, very digestible, very quick. Uh, and then  
Edwin Johnson: And sorry to interrupt, Cody. If these hype videos work out,  
Cody Haugen: go  
   
 

### 00:16:50

   
Edwin Johnson: then maybe we just go right back to them to create the educational  
Skye Capazorio: Yeah.  
Edwin Johnson: videos.  
Skye Capazorio: And I've also I've actually been talking to him about other stuff like other formats of stuff. So, um like AI overlap. So, and I don't know, I'm sure most of of us have seen the videos where there's like a content creator that's pointing to stuff like there's them in the like corner of the screen and they're like, "So, you point to this button and then you click this and no no no, he has the capability of AI generating that even in that sort of style content. Um, so there many ways that we can do it as opposed to them being these very sort of polished education videos. I I want from my perspective they should feel no different to when you would scroll if you're going through a Tik Tok feed. And so we want to try and embed that. Obviously creating brandability, but I also see this as an avenue of a space that could potentially be bought by another brand um to own and co-create with them that they own the education module around  
   
 

### 00:17:53

   
Brett StClair: Imagine in your third space.  
Skye Capazorio: that.  
Brett StClair: Guys have just finished watching. We love it so much. We posted on our third space, right? Because you don't want them necessarily sharing outside. But getting them into the third space, guys, you should have seen this latest one. And I agree. You can start making personalities in the space, right? That was really cool. Have you seen how brilliant that is?  
Skye Capazorio: Yeah.  
Brett StClair: and keep it lightweight so it's not one of those Udemy style kill me forces,  
Skye Capazorio: Yeah.  
Brett StClair: right?  
Cody Haugen: I've got a quick question guys as well.  
Skye Capazorio: Yeah.  
Cody Haugen: Is it possible then after you've gone through the videos and then you maybe answer like two or three questions on the content that you've seen in order to then get your stars money or something like that. So you're actually retaining what you're watching as  
George Westbrook: Yeah. Yeah, that's a good idea.  
Skye Capazorio: Yeah.  
Brett StClair: It's a great idea.  
Cody Haugen: well.  
   
 

### 00:18:43

   
Brett StClair: Yeah. And it also helps us tag once they finish, right? Instead of having watch the point of the video, we just like, "Oh, at the end you filled that in. Great. That's where you are." It's a nice way to do it there, George.  
George Westbrook: Yeah,  
Skye Capazorio: Okay.  
George Westbrook: I'm just I'm just trying to think of the like MVP thinking, the the technical complexity for that Tik Tok scrolling because all I think is every single scroll a new video has to be loaded in. Um, and we can't we we can't obviously preload all the videos on the user's device. Um, that would be way way way way way too much. And then I'd need to go away and do some more research, but my instincts are telling me it for an MVP having the the Tik Tok feel might might be quite a lot cons.  
Skye Capazorio: Just explain to me why. Sorry, George. I don't I don't understand  
Brett StClair: George, I think I think we could leverage the YouTube shorts infrastructure. I'm pretty sure.  
   
 

### 00:19:44

   
Brett StClair: So,  
Skye Capazorio: technically.  
Brett StClair: what I was suggesting by loading onto YouTube, it's all there, but it has all the serving capabilities. So, you just capitalize on that. So, you don't have to worry about pushing and serving and storing and hope We run it all through YouTube. You got the YouTube as your distribution channel anyway.  
George Westbrook: Okay.  
Brett StClair: So people can still come and learn even if they're not on the system, can be part of your drive. But then we're pulling that in and then we leverage their for example shorts their shorts infrastructure to swipe up.  
George Westbrook: H  
Brett StClair: We check what's available on the API,  
Skye Capazorio: Can I can I just ask another question about that? So like you know where you go on an e-commerce site or any website like very often brands will they used to have like an actual like um social feed that comes through at the bottom. So whatever's being posted on Instagram is reflecting on the website. Is there no way of us maybe creating the content that sits on a a private um Instagram channel that then pulls directly into there and has that or a private, you know, Tik Tok.  
   
 

### 00:20:44

   
Skye Capazorio: I don't know. Maybe that's another way to consider. I leave it to you to research.  
Brett StClair: Yeah,  
Skye Capazorio: I think you get the idea of what we want to  
Brett StClair: let us have a look. I'm just really familiar with YouTube.  
Skye Capazorio: do.  
Brett StClair: Used to run it for two years. So, that's where I'm leading to.  
Skye Capazorio: Yeah.  
Brett StClair: That's the only reason why I know a lot about it.  
George Westbrook: Hey.  
Skye Capazorio: I think it's just we want the the feel, right? I understand that there's a technical question that needs to be answered and I think that it's that also as we're saying answering like three questions that's on that specific education module very quickly then becomes like a maybe it's like a multiple choice thing, a multiple choice scroll that happens that somebody can you know answer in terms of that. So then it like looks like it's scrolling to the next and it's like a poll that you vote on and then it moves to the next video, etc., etc. Maybe that's one way of resolving it.  
   
 

### 00:21:34

   
George Westbrook: It's say I've literally just as we've been speaking been having a look into it and it's not as it's not as complex as I thought it was.  
Skye Capazorio: Okay, cool.  
George Westbrook: Um okay,  
Skye Capazorio: Great.  
Brett StClair: If we leverage someone else's capability,  
George Westbrook: good.  
Brett StClair: I think we're okay.  
George Westbrook: Yeah.  
Brett StClair: It's just the APIs and what we can do.  
George Westbrook: Yeah. Yeah. Um yeah. Yeah. And there's libraries already pre-built that we can use and leverage. Um, okay. One of the things I'm thinking is so if it's module based so when forget how we refer to modules but like a typical learning module how do you envisionage like a a scrolling experience in that or is it the scrolling experience is just kind of  
Skye Capazorio: empty.  
George Westbrook: randomly generated um and users just scroll through find stuff or for each module there's a certain specific set of clips maybe accompanied with some text because I know some people do like text some people like videos and things like  
Skye Capazorio: Yeah.  
   
 

### 00:22:26

   
George Westbrook: Huh?  
Skye Capazorio: Um, it's a good  
Brett StClair: You could get to the end of a scroll.  
Skye Capazorio: question.  
Brett StClair: When you finish up the module, it stops, snaps out of a scroll, goes into something a bit more formal,  
Skye Capazorio: Well, couldn't it have that you press like start education journey, let's just call it, at the top. You click on that, it opens up the first module. You scroll through it, answer the polls and stuff, and then it gets to the bottom and it says, "Move on to part two." And at the end of each one, it prompts you to move on to the next one. And maybe as you do that, there can be a little celebration that happens on the screen because you've now earned X amount of cash into your referral wallet  
Brett StClair: So that concept, you know, when you like a video,  
Skye Capazorio: that  
Brett StClair: whatever, you're the first to like or you're the hundth to like or my absolute favorite, you're the 67th to like  
Skye Capazorio: terrible. Terrible. Terrible.  
   
 

### 00:23:29

   
Cody Haugen: Dad joke.  
Brett StClair: confetti off the screen and literally on 67 the 67th screen does this  
Edwin Johnson: By  
Skye Capazorio: Yeah.  
Brett StClair: little  
George Westbrook: Brett. Brett the Boomer.  
Skye Capazorio: I mean, I know that like that that um 67  
Edwin Johnson: the way, great shot, George. That was a great  
Skye Capazorio: is 67 is is hitting a cord at the  
Brett StClair: kills me. That's all he does to me.  
Edwin Johnson: job.  
Skye Capazorio: moment with like my sevenyear-old. So, I'm not quite sure it's a it's going to I I don't know if it's past the audience that we're talking to now, but uh we can certainly look at that as an  
Cody Haugen: Yeah.  
Skye Capazorio: option.  
Cody Haugen: Can I can I just interject real quick with a duality duality of what we're creating for the education is that all of that repository is able to be acted on or learned from um an AI chatbot that's going to hopefully the way I'm looking at this predominantly handle like 75 or 85 or more of our first level support questions.  
   
 

### 00:24:31

   
Skye Capazorio: What?  
Cody Haugen: So whatever this repository is, this AI chatbot that I was going to ask if you guys could build it, I assume you can. Otherwise,  
Skye Capazorio: Yeah.  
Cody Haugen: HubSpot does offer a support tool, but we need this repository to be accessed by a uh support AI tool that can learn and and reshowcase all this information.  
George Westbrook: Yeah. Yeah. The G giving it the information is yeah very very very doable. Um we might if if we might need another we we might need to do some thinking about that and then do maybe another module discussion on how you envisionage AI from within the platform because don't don't get don't get us started on that because we'll go we'll go down rabbit  
Skye Capazorio: Is  
George Westbrook: holes.  
Cody Haugen: I I don't I don't want to digress. I just wanted to make it known that this repository does need to be acted on in other  
Skye Capazorio: it?  
George Westbrook: Yeah.  
Cody Haugen: places.  
George Westbrook: So, so from from what I'm getting, you want it to be video first and do you envisage any text content as well?  
   
 

### 00:25:39

   
Cody Haugen: I'd say less tax is better.  
George Westbrook: Like not users not even having the option or they have the option but  
Cody Haugen: I I don't see  
George Westbrook: it's  
Skye Capazorio: I mean, I I I see it literally being created in a way that is like potentially with  
Cody Haugen: the  
Skye Capazorio: subtitles of the video that's being explained like like you would do in in Tik Tok and Instagram. Um, but I don't see it as like like paragraph sentences about the  
Cody Haugen: Yeah. Stand stand alone.  
Skye Capazorio: about the things.  
Edwin Johnson: I agree with that,  
Skye Capazorio: Yeah.  
Edwin Johnson: Scott. I I like that.  
Cody Haugen: Yes.  
Skye Capazorio: I think we're trying to make the information assimilated by them in a way that feels 100% natural to how they assimilate content and information learning and news.  
George Westbrook: My push back would be who who learns a lot from Tik Tok and Instagram res.  
Skye Capazorio: Me I do  
George Westbrook: I'd say I I can't in my head I'm like I like I get the 60-second 60-second clips, but if it's  
   
 

### 00:26:44

   
Brett StClair: how I learned how to spell.  
George Westbrook: a  
Brett StClair: It's how I learned how to use cord code.  
George Westbrook: Yeah, I've seen you use Claw Code Max.  
Brett StClair: f***.  
George Westbrook: That was a joke. He's very  
Skye Capazorio: Um um I I mean for short snippet  
George Westbrook: good.  
Skye Capazorio: learning absolutely I think for remember George like from my perspective this is these are not like this is not like each thing is an hourong module. mod. Each video is not an hourong module. It's like snackable information. So, it's very short and sharp.  
George Westbrook: H.  
Skye Capazorio: It doesn't it's not like Yeah, I I don't think that it's it's drawn out. And I think it's in each of those kind of phases. Um almost like an infotainment element. I think that's what we're trying to hybridize here,  
George Westbrook: What is it?  
Skye Capazorio: if that makes  
George Westbrook: Yeah, because one of the things that's going into my head,  
Skye Capazorio: sense.  
George Westbrook: I think Brett ages ago did that the product demo video similar to what I think this guy that you were talking about, Sky.  
   
 

### 00:27:46

   
George Westbrook: Um, where you can use AI to write the code to do the video and then the you create the transcript. You send the transcript up to an AI voice generation service. You overlay it on top of the video. And why I'm thinking that is if let's say you have module module one which is about whatever um if you create the videos in a certain way and an advertiser sponsors it it'd be very difficult to switch out advertisers whereas if it's done in  
Skye Capazorio: Yeah. So, I can I can I can cut that out immediately.  
George Westbrook: H.  
Skye Capazorio: So we're not looking to change advertisers in the space on a almost programmatic impression basis. I'm talking about like uh literally the content being created. Let's just say it's Coca-Cola.  
George Westbrook: Mhm.  
Skye Capazorio: They are embedded in it as if it was something that they would put on their own channel. It's not changing out the advertiser.  
George Westbrook: Mhm.  
Skye Capazorio: That would be a space that we would offer to one advertiser to essentially take ownership of the education module.  
   
 

### 00:28:50

   
George Westbrook: Okay.  
Skye Capazorio: So it wouldn't work like an impression thing where we're trying to change that if that makes  
George Westbrook: Yeah, it was I wasn't I wasn't thinking of it in ter like in programmatic where it's like it could be changing every day,  
Skye Capazorio: sense.  
George Westbrook: but maybe even on like monthlong monthlong bases. Um where they they they buy the space for a month. Obviously, every time there's a new one, they'd have to regenerate the videos. Whereas with AI, we could have it done programmatically, meaning in code. So that a new advertiser comes in, one one month it's Coca-Cola logo, next month it's a Budwiser logo, and then we just run a script. It creates the videos, puts it in the CMS, and then then loads  
Skye Capazorio: Yeah. So, I get what you're saying.  
George Westbrook: in  
Skye Capazorio: Where I see this slightly differently is that embedment embedding within content from an actual like experience perspective is a very high value property when it comes to advertisers. So even let's just say I'm trying to think of a a a brand that would be that would so let's just say we take an energy drink or something like that they would they would the opportunity exists here for them to actually go and  
   
 

### 00:29:52

   
George Westbrook: Mhm.  
Skye Capazorio: create the content in this space in a way that is almost brandowned by them that lives in our ecosystem. So we're saying we have an opportunity to educate people about how you go through the trading process in short um social style content base with polls that brand could take over ownership in terms of actually creating that content themselves. that that is probably the first place that I would start is giving them the opportunity to go each education module has to we'd obviously collaborate on what needs to be included in from a scripting perspective and the actual education portion of it but there's a lot that could be taken on from an ownership perspective of a brand directly in that so I get what you're saying about that and maybe that is something that we look to do in the future but I would say for this I would definitely want to sell that as a space that a brand could own holistically and also they take ownership potentially of of creating that content and embedding their brand and their  
Edwin Johnson: You know, it's actually it's actually very valuable with our partnership with tZERO because  
   
 

### 00:31:02

   
Skye Capazorio: style.  
Edwin Johnson: if you ask a lot of people what tokenization is today,  
Skye Capazorio: Yeah.  
Edwin Johnson: they don't have a clue. And if you talk to them what uh you know a blockchain ledger is, a lot of them still don't have a clue. Um so but by us using both of those within this uh environment um you know again helping people learn the way finance is moving. It's not just about our trading challenge but you know the New York Stock Exchange and NASDAQ are all moving towards tokenization. So this we could get in front of it. So as you saw an ad it would be pretty valuable to someone uh I would imagine.  
George Westbrook: Okay.  
Skye Capazorio: It could even be a space where like a brand has their own content creators that they collaborate with always on that that work with them to actually create these pieces of content and education  
Edwin Johnson: Yeah.  
George Westbrook: And do do you do you see that do you see that more as in your education module or something  
Skye Capazorio: modules.  
   
 

### 00:32:04

   
George Westbrook: That sits more in the third  
Skye Capazorio: I think it sits in our education module.  
George Westbrook: space.  
Skye Capazorio: I think we need to be I I think we need to be clear about the two things in terms of the third space. The third space by my definition is where people get to it's a social space for them to be able to communicate their thoughts on what they, you know, they think is going on and and be reactive to what's going on with Teams. It's a social community like like WhatsApp essentially or a chat room for them to be able to converse on what's going on. In a future version of this, I see this being able to build into various different uh potential Discord channels that they would each own  
George Westbrook: Hey, thank you.  
Skye Capazorio: that live that are embedded within our space and then could even, you know, they they could take ownership. So, you could get like um top traders or influencer content creator traders actually being able to own their own channel within that that they are using as almost like a broadcast channel to to talk about what it is that's going.  
   
 

### 00:33:05

   
Skye Capazorio: But that's a future state in this. This is purely just the third space for me right now in this current thing is a chat space that people are having conversations and making comments about what what's happening real time and stuff like that. I think Brett I I can't I think you did it on um on on the on the lovable app um example that you did. I think there was a thing that said that that it was like somebody was like, "Oh, this team's on fire. this is so great and then somebody writes um wait they're just about to tank this is going to be the worst loss you know so it's it's that sort of stuff it's team banter that is probably the best way the education modules I see as being separate to this I don't see those as as being this social engagement yes there is an opportunity to take that and go I finished I shared I've done this module and now I've got the extra cash but it needs to be functional from an education content  
Edwin Johnson: Makes sense to  
   
 

### 00:34:03

   
Skye Capazorio: stream.  
Brett StClair: So let's get into the third space while we're here,  
Edwin Johnson: me.  
Brett StClair: right? Um are we happy about the education? I think there's pretty there's a lot we can do on education like you can extend it out into as Cody you're suggesting using AI into the app into recommendations. You can have different modes if you're junior you know  
Skye Capazorio: Thank you.  
Brett StClair: inexperienced you can have these kind of help guides. you know, you're not too sure, we see you haven't done a trade yet, notification, boom, come learn how to do a trade.  
Skye Capazorio: What's  
Brett StClair: I think those will be future phases because it just requires more deeper kind of integration and thinking  
Skye Capazorio: up?  
Brett StClair: and machine learning kind of attributes there. Are we happy with where we landing the moment? It's a destination Tik Tok style uh with poll like kind of bit of a poll feeling so that we can test to see if they've actually learned anything and we break it up into components and then we'll think about and and then against  
   
 

### 00:35:07

   
Skye Capazorio: And the reward.  
Edwin Johnson: Hey, Troy. Troy,  
Brett StClair: it. Yeah.  
Edwin Johnson: do you have anything that is not resonating well with you with this  
Skye Capazorio: Lord,  
Edwin Johnson: model?  
Cody Haugen: No, it's it's not. It all makes sense. I think when we get closer to launch in production,  
George Westbrook: What is  
Cody Haugen: be able to partner with uh other vehicles for getting  
Skye Capazorio: let's  
George Westbrook: that?  
Cody Haugen: education out like, you know, Tasty Live does their their their 16 hours of broadcast. we could talk about them getting a series on their broadcast of explaining how to trade and price performance securities. So  
Edwin Johnson: You know who you should consider, Troy,  
Cody Haugen: I  
Edwin Johnson: is that Kaplan University. They sell all that b******* when you got to take the exams and all that.  
Cody Haugen: Yeah,  
Edwin Johnson: Their whole business is selling educational materials that they would be a a  
Cody Haugen: 100%.  
Edwin Johnson: great sponsor for education. Just  
Cody Haugen: The the other one which I just sent to Kevin and Cody is Investopedia as  
   
 

### 00:36:00

   
Skye Capazorio: Yeah.  
Edwin Johnson: got  
Cody Haugen: well has lots of already staged educational resources  
Skye Capazorio: Oops.  
Cody Haugen: on how to invest like all the different market structure terminology and encyclopedia. Also, SIBO has a a institute, an education institute. Again, a lot of great ideas on how to package content and education.  
Skye Capazorio: That's 10  
Cody Haugen: You know, that's how they've educated uh retail for options.  
Skye Capazorio: seconds.  
Cody Haugen: So if we can take some of that and leverage their approach,  
Edwin Johnson: Kev,  
Cody Haugen: um I  
Edwin Johnson: can you can you spend some time on those sites and get give us some  
Cody Haugen: think  
Edwin Johnson: feedback?  
Cody Haugen: Yeah, sure. Yeah. But I think this is a great starting point because this is what we need for the trading challenge.  
Edwin Johnson: Cool.  
Cody Haugen: But I'm also starting to think about okay, how do we transition that into when we go into production and you know we we're going after prot traders or just general uh you know  
George Westbrook: See  
Cody Haugen: investors.  
Skye Capazorio: I I think the absolutely and I think where we can partner within that space  
   
 

### 00:37:00

   
George Westbrook: you.  
Edwin Johnson: Okay.  
Skye Capazorio: and and leverage that. So, exactly as you were saying, Troy, where there are spaces that already do that and then they create custom content that's specifically linked to in place production trading that actually gets housed on their site and our site and becomes an opportunity for them to drive other education modules for their brand essentially and their product offering outside of that is once again exactly one of those scenarios that can that that of of um an advertiser. And I also think Cody's idea further down the line of meeting the trader where they're at um in their knowledge base and stuff like that and almost customizing their education journey would be incredible.  
Cody Haugen: Yes.  
Edwin Johnson: Great. Okay.  
Brett StClair: Okay. So, let's park it. I want to move on to third space. And so, third space gets a little bit more integrated,  
George Westbrook: Let me  
Brett StClair: right? We'll have a space where the chat rooms are. You can go into particular chat rooms and then it's thinking about how do we pull those chats into the right pages so that you get those kind of engagements.  
   
 

### 00:38:24

   
Brett StClair: Do we put filters on when we see people talking about the bears? Is that the bears? Is the bears a team? Sorry.  
Edwin Johnson: Yeah. Oh, yeah.  
Brett StClair: We've got couple  
Edwin Johnson: In fact, in college, there's also the Golden  
Brett StClair: of  
Edwin Johnson: Bears.  
George Westbrook: We're going to have to do some revision on the teams, I think.  
Brett StClair: I think we all need to start making NFL and NBA our most watched. I've actually been to an NFL game at Tottenham Spurs Stadium. It was the most insane experience of my life. Like this is why people do this.  
Edwin Johnson: by the way that's no it's uh that's that's why we're I'm  
Brett StClair: It's just fun. It's insane.  
Edwin Johnson: trying to push so we can get access to the UK for the trading challenge because the huge  
Brett StClair: sold out.  
Edwin Johnson: appetite  
Brett StClair: Huge. Huge. I couldn't believe it. And it's what a 70,000 seater. We can't even do that in rugby.  
   
 

### 00:39:12

   
Brett StClair: Fill a 70,000 seater. Um has to be an international game  
Edwin Johnson: Really?  
Brett StClair: otherwise bad. So let's talk a little bit about it. How do you guys see it kind of? And I want us to start kind of a core area, right? We we've got to drive the users to find a chat room, create a chat room. Um, what we thinking of in the initial thinking was we're going to leverage an open source platform. And there's a couple out there. I think in the proposal I've put a platform we reviewed, but I can't remember the name of it. It was quite dynamic. So open source instead of reinventing the wheel here, it's been done a thousand times over. It's called the headless. So, I've double checked it's a headless platform, so we can layer our own head on it with our own interface. Um, and you can do some really sexy stuff with it. And I think it just makes it way faster, easier, and it reduces risk.  
   
 

### 00:40:10

   
Brett StClair: Um, and you get all these amazing features with it without having to build it from  
Cody Haugen: So start.  
Skye Capazorio: Do do we No,  
Brett StClair: scratch.  
Cody Haugen: Oh, sorry. Go ahead,  
Skye Capazorio: I just wanted to ask do we are we able to uh do we get the  
Cody Haugen: Sky.  
Skye Capazorio: the conversation like is there is there a place that we can store that conversation? The reason I'm asking is because I think long term it's potentially a very valuable space for us to be able to record what people are saying because it it it lends itself for us to be able to start packaging thematic narratives that we are able to sell from a data perspective. Um,  
Brett StClair: So all that data is yours. Um, it's all open source. We'll set up all the database. It'll link it through however you want to manage that data.  
Skye Capazorio: okay.  
Brett StClair: The conversations. The challenge with chat is it's fractured and so it brings a whole another set of kind of concerns and then if stuff goes viral,  
   
 

### 00:41:05

   
George Westbrook: Jesus.  
Brett StClair: one chat can generate hundreds of thousands of impressions. And so we really want a mechanism to kind of manage that workload if that goes crazy. What we got to be thinking about is where do you want those chats exposed in  
Cody Haugen: Yeah.  
Brett StClair: game like a natural  
Cody Haugen: Yeah. So, let me maybe just to kick it off from a creative perspective and then everyone can tear it apart  
Skye Capazorio: Okay.  
Cody Haugen: or come up with other ideas. But where I originally thought of this or planned for the chats to be involved would be uh specifically on the game page once again to your point Brett to limit  
Edwin Johnson: What's the game page to code?  
Skye Capazorio: Yeah.  
Cody Haugen: the uh the the matchup page.  
Edwin Johnson: Describe the  
Skye Capazorio: speech. Speech.  
Edwin Johnson: game.  
Cody Haugen: So two teams you go there you see the live match tracker to limit the at least  
Skye Capazorio: Speech.  
Cody Haugen: limit to an extent the number of people in one chat at a time. to your point, Brett, a chat could go insane very quickly.  
   
 

### 00:42:10

   
Cody Haugen: And so, at least you only have people focused on that game, two teams going back and forth. You know, I'm I'm long the Bears, while I'm long the Packers, I'm actually shorting the Bears. It's just that community rivalry back and forth in that game. Um, and then secondarily in a favorites page. So, the ability to favorite the Packers because I'm a Packers fan or favorite the Cowboys or favorite your your long positions. Um, those type of teams. So, then you're in a community of like-minded folk that you can share information back and forth. Oh, did you see that the Packers signed uh a free agent this week? Oh, no, I didn't see that. Oh, well that really makes their defensive line a top 10 uh defensive line in the league now. And now they're starting to share ideas and generate more interest to make a trade or uh decisions being made shared organically.  
Skye Capazorio: Good night.  
Cody Haugen: So favorites favorites page or a community team page uh team matchup page or game page.  
   
 

### 00:43:16

   
Cody Haugen: Um, and then lastly, I had thought of like a private chat. And once again, in production, this would be a paid feature, but in the simulation, it's let's get them hooked on as much cool s*** as possible. And so, it's a private chat that has an AI layer on it that loads in the repository of sport radar statistics and I can ask it, well, what are the packers? So, in in in combination and maybe it lives on the research tab that I uploaded into that uh data dump um where you can make reports and such like that, but this is just more of a natural way to get short form answers back. When was the last time the Packers threw for 300 yards? Okay, it can quickly analyze historical data and spit back an answer.  
George Westbrook: Yeah.  
Cody Haugen: So much more natural language processing back and forth with the chat tool um as opposed to the research.  
Brett StClair: Think about the learning statistic.  
Cody Haugen: Yeah, exactly. A good old client of mine that does this extremely well that we can model after is called Statmuse and they built an entire business uh off, you'll love this Brett, off the Google Accelerator program and now they're massive.  
   
 

### 00:44:32

   
Cody Haugen: uh they actually have an investment from Google, but they built an entire business off short form answers that run off NLP and how people interact with that is amazing. They get millions and tens of millions of queries every month because Google and Amazon Alexa actually default to stat news for sports questions that are multiple levels deep. So not just what is the score but when is the last time this happened on such and such day you know in this weather type or something like that. So those are the three forms without going down too much of a rabbit hole. Those are the three forms that I originally had come up with where a chat function would live and breathe.  
Brett StClair: Just one of the things we need to also put some thinking hats on is um moderation. Um and so when you open up chats, you do open yourself up to some exposure around abuse. Um, and so making sure that your policies are well articulated and um, got to decide if it's you're moderating it, which I would not suggest, it's going to be a nightmare, or set up something like uh, userbased moderation.  
   
 

### 00:45:51

   
Brett StClair: So when someone can lodge and put an appeal that it's, you know, violated your policies blah blah blah, and then you investigate, you can put like a layer of AI on that, too. kind of helped scale that a bit. But that's the only downside of chat. Bad words. Hey, you have bad words. Well, it's how we got to think about how we also manage them. So, if someone's swearing, you know, like I'm guessing it's perfectly fine to swear on the platform, right? Um, you've agegated, great. Um, but if there is continuous racial slur, yeah, you know, is that part of your policy? Are you comfortable with that, you know, you probably want to take action. So, but do you want to ban them outright or do you want to fire a warning? Like, you don't want to be telling people, you know, because there's bias. There's bias in everything. And so you've got to watch the freedom speech kind of scenarios like what are you managing? Um and just it need it it requires a bit of thought.  
   
 

### 00:47:00

   
Brett StClair: I wouldn't take it lightly because when you do open up the channels, promise you we like I'm currently in Teraflow, we're running about 400,000 messages an hour and it's a fairly controlled environment and still can't believe what goes on in there and it goes very quickly and these guys are managing maybe 600,000 000 users a month and that volume of chat comes through and they're an e-commerce kind of environment with the ability to chat and engage with their kind of communities. So,  
Cody Haugen: I Yeah,  
Brett StClair: it's just put a damp need to think about it.  
Cody Haugen: I mean it seems you seems like have a Yeah,  
Brett StClair: Make sure you're ready.  
Cody Haugen: sorry B. It seems like you have a good handle on at least scale to what we're trying to initially get off the ground with which hopefully we start August with a half million or more. So I mean I would I would heavily lean on your expertise as far as the moderating. I have given it some thought. But I don't have any good answers at this point.  
   
 

### 00:48:10

   
Cody Haugen: Um outside of like do we appoint someone kind of the zar of that team's chat. Um and they we we vet that person. We take that you know they take that very seriously as like kind of that badge of honor that they are the zar of that team. Um but then once again you're you're turning it back to the public facing sort of thing. So you remove in play from it. Um, but yeah, so so like I said, I've given it some highlevel thought, but I would like to we can maybe take it offline and kind of bounce around some ideas to bring back to the  
Brett StClair: Yeah,  
Cody Haugen: team.  
Brett StClair: I think it's a mixture of technical solutions plus kind of exposure and how to manage exposure.  
Cody Haugen: Yep.  
George Westbrook: One thing I'm thinking is how how do you how are we going to split up the users into groups because I think even team team based that that could be problematic. cuz I suppose if a team's playing then a lot of people or two teams are playing then a lot of people might want to join that chat and it's going to be very burst based and then if let's just say there's even 10,000 people um in a chat wanting to message it's just it it's like those when you're watching those illegal streams of like sports games and there's the chat down the side it's just loads and loads of random random messages and it's it doesn't it doesn't provide value.  
   
 

### 00:49:38

   
George Westbrook: Um, but then again, you don't want to fence off some users because they're not this, but then you don't want to have private groups because then you're not getting general consensus. It's Yeah, I'm  
Cody Haugen: So that's why I wanted it down as much as possible because there was a stage where I was not paying for any  
George Westbrook: just  
Cody Haugen: sports and yeah I I mirror I mirrored it off of that experience that that chat lives on those illegal streams and it's just I mean you can't even read a sentence before it's gone. So, so more yeah, like I said, more thought uh I have original ideas, but I would like yeah the team to give it more thought or you guys to give it more thought on how we break this out because yeah, that's that serves no value at  
George Westbrook: What is what is the value that you want the user or the users to get out  
Cody Haugen: all.  
George Westbrook: of I'll say this chat but I suppose there's chats in different situations cuz in my head I'm thinking right game day chat that's a communic communication about the game.  
   
 

### 00:50:38

   
George Westbrook: And then the other parts thinking more more Reddit style where it's maybe longer horizon  
Cody Haugen: Yeah,  
George Westbrook: conversations.  
Cody Haugen: I I think if it's a if it's a team focused like favorites chat like you just said, I think it's more longer vision, longer term type type chat, uh where maybe that chat lives. And then the game chat, yeah, is more s***-talking for lack of a better term. um razing up the other team and but it's also you know inter you know it is about your team as well or the other team um and then the private chat is really just whatever research you want to do and to be clear game chats would end as soon as the game ended. We have established that fact at least the chats will not live on on the game page longer than the game is actually being  
George Westbrook: cuz I'm trying to think is there so there's obviously the  
Cody Haugen: played.  
George Westbrook: leaderboard for like the the PNL now um comeback trader of the day and things like that. Is there a way of potentially having like some sort of community ranking?  
   
 

### 00:51:59

   
George Westbrook: No, because I was going to say then their messages hold more weight, maybe they're more persistent, things like that, but then you're not treating all users equal with the messages and then it's not promoting a back and forward discussion between all users as equal. I need to think more about that. I've I've got the idea, but I can't really articulate it.  
Cody Haugen: Yeah.  
Edwin Johnson: I'm not a big so like I don't I don't have anything to say here other than I basically look for something that's funny and makes me laugh and then I go on. You know what I mean? So it's like that's about it.  
George Westbrook: I suppose in the game day chat we can make it quite like fun where there like s*** talking is like one of the main aims. Let's say there's a big thing and there's maybe you can send certain gifts or do something  
Skye Capazorio: That's what I wanted to ask.  
George Westbrook: to other users on another team.  
Skye Capazorio: Are we going to allow like gifts, memes, things like that that people can like will they be able to post that sort of stuff within there?  
   
 

### 00:53:04

   
George Westbrook: potentially and put like an 8020 80 yes 20 no on the potentially um because it it it depends on the choice of what chat infrastructure we use. So without without doing the research I could say yes 100%. Um but we we'd have to decide decide on that. But I think especially for the game day chat, that is really important because like you said, Cody, it's mainly going to be about s*** talking. Nobody's going to be like, "Oh, I've seen this price move blah blah blah." And they did this like,  
Cody Haugen: Yeah.  
George Westbrook: "Oh, we've made 10 yards. Yeah, have that."  
Cody Haugen: Yeah.  
George Westbrook: Um  
Brett StClair: So I think also what's important is and we actually haven't we should uh this is probably across the board scenario is uh like a management back end and we'll need to plug the chat kind of kind of management and controls and flows and stats into that back end as well or  
George Westbrook: Do you mean in for internal use?  
Brett StClair: internal use. Yeah. Yeah.  
   
 

### 00:54:18

   
Brett StClair: Yeah. Yeah. Yeah. So, the teams can monitor stats and stuff and there'll be a whole lot of stuff where we probably want to launch kind  
Edwin Johnson: Excuse  
George Westbrook: Okay.  
Brett StClair: of campaign ideas into it and notifications. will need a kind of backend dashboard so you can load notifications in or integrate it into a RAM of some sort.  
Edwin Johnson: me.  
Brett StClair: And there's all that component that we need to think about. Just bring it in there so we capture it on the documentation. Um, one quick clarification. The game day page is not called game day. It's called  
George Westbrook: It's part of the information. So, it's a subm module within the information component or  
Brett StClair: I mean the landing page when two teams are playing against each other.  
George Westbrook: module.  
Brett StClair: What do you guys want to call that?  
George Westbrook: I think it was the game day page. Correct me if I'm wrong, anyone.  
Cody Haugen: Yeah, I  
Brett StClair: I got the sense you guys didn't want to call it that.  
   
 

### 00:55:25

   
Brett StClair: You wanted to call it something else.  
Cody Haugen: guess  
Brett StClair: Info get game information or did I mis misunderstand that? Okay.  
Cody Haugen: I I didn't to be honest,  
Brett StClair: Okay.  
Cody Haugen: I didn't know we named it anything specific up to this point. I would I would vote, you know, matchup page, game day page, game information page. I I think we can still dial that  
Brett StClair: Okay.  
Cody Haugen: in.  
Brett StClair: Yeah, we're going to get to a point where we're going to get need to get terminologies bedded down and uh sometimes it develops organically like component and  
Cody Haugen: Yeah.  
Brett StClair: module. Okay, I think we've got enough on this one. Shall we do the last component? Um, and then I want to talk about like an approach to do the advertising and advertising units after that if we've got five minutes left just so we can tee up that and get those workshops up and running. Um, I'm going to ask you George to take control here.  
George Westbrook: for the challenge website.  
   
 

### 00:56:35

   
Brett StClair: Challenge website here.  
George Westbrook: Okay. Um, let me get it  
Brett StClair: I was saying to Max,  
George Westbrook: up.  
Brett StClair: you're gonna come up set her all up. And he's what? I don't have access to it. And I realize you built it.  
George Westbrook: Let's I suppose if we things like styling look and can you all see this as well?  
Cody Haugen: Uh, now we can  
George Westbrook: Perfect. Um yes I think like little design iterations like the eyes for example um what what would be best if we capture that in the admin panel. I suppose it's more like holistic like what does each page need to do? What pages are needed? What is the design look and feel? um more more more generally. Um so I suppose the pages pages we've got up here at the moment of the home, how it works, the prizes and then the leaderboard which will be like a real time real time leaderboard of what what's actually going on. Um and then obviously an FAQ as well.  
   
 

### 00:57:43

   
George Westbrook: Um so those overall pages, do they work? Is there anything else you'd want to add?  
Edwin Johnson: I can't think of anything off the top of my head right now.  
Skye Capazorio: Yeah. Neither can  
George Westbrook: cuz I suppose it's how how for for this website how meaty meaty do you want it  
Skye Capazorio: I.  
George Westbrook: just as bare minimum for them to be able to get get the information and just get onto the app as soon as possible.  
Edwin Johnson: I would say that's the best path.  
Skye Capazorio: Yeah, this is this is yeah, this is information not getting into like all the details of the various different things. I think it's about getting getting them ultimately to understand it so that they download the  
Edwin Johnson: Yeah,  
George Westbrook: Okay.  
Edwin Johnson: this is a support page more than a,  
Skye Capazorio: app.  
George Westbrook: Yeah.  
Edwin Johnson: you know, destination page. I I in my mind's eye.  
George Westbrook: So, so you see this more as like support for users when they've got an issue and they want to go to check how it works  
   
 

### 00:58:45

   
Edwin Johnson: No, no, no,  
George Westbrook: or  
Edwin Johnson: no, no. I mean, as far as awareness,  
Skye Capazorio: No.  
Edwin Johnson: support to say, okay, you know, hey,  
George Westbrook: Okay.  
Edwin Johnson: what is this? Oh, I'm gonna look it up on the internet or whatever beforehand.  
George Westbrook: Okay.  
Edwin Johnson: Not not for technical support of any kind.  
George Westbrook: Yeah. Okay. Yeah, that I don't Yeah, I was I got a bit confused on that.  
Edwin Johnson: Yes,  
George Westbrook: Um that's all right.  
Edwin Johnson: sorry about that.  
Skye Capazorio: I and just to add George,  
Brett StClair: That was the  
Skye Capazorio: just like in the context of our conversation about the overall page,  
George Westbrook: Um,  
Skye Capazorio: I know we want to have this as a another a separate URL, but I was having a think about that potentially having just the homepage portion of this as a tab in the main website that somebody then can click to and when they go there it takes them to this. I don't know.  
George Westbrook: it's a re like a redirect.  
   
 

### 00:59:31

   
Skye Capazorio: We just need to think about that.  
George Westbrook: So it could two yeah cuz I suppose two two options we  
Skye Capazorio: Yeah. Yes.  
Cody Haugen: s***.  
George Westbrook: could have is there's global website separate domain separate URL blah blah completely isolated in terms of deployment and then this on a separate URL in play trading challenge blah blah blah they can click on a button on the homepage or a tab on the homepage and it will redirect them to this URL or we could have everything sat under one one URL and it's ability to route. But I suppose what I'd I'd favor first option because for things like SEO um custom tags for all of this um obviously you can do it for the other pages  
Skye Capazorio: Yeah.  
George Westbrook: but I suppose if they're slightly isolated you can kind of this one is ultra focused on a certain thing whereas the other one is ultra focused and they can still navigate between um there just might be an extra  
Skye Capazorio: Yeah.  
George Westbrook: one one second of waiting.  
Skye Capazorio: Yeah. I I do think that I do think that the I I agree with you.  
   
 

### 01:00:35

   
Skye Capazorio: I think that they should be separated for all the reasons that we've spoken about, but I do think that the main website should list like and we'll probably build this over time, right? So, it would be like challenges and then over time we would have multiple challenges there.  
George Westbrook: Yeah.  
Skye Capazorio: So then you would click on it and be able to go out to each of those for the time being it would then just take you to this one. Um but also we might also have like simultaneous challenges happening at the same time also. So we just need to but I do still think that there should be a place for a highle thing even if people are clicking through from there to the outside website there should be a tab in the main website that talks to challenges.  
George Westbrook: Okay.  
Skye Capazorio: Even if it's actually high level it doesn't even have to say this specific challenge. It could go um you know it could talk about the whole experience that a challenge gives you the chance  
George Westbrook: Um,  
   
 

### 01:01:32

   
Skye Capazorio: to try and play out you know at no risk and there's amazing rewards and prizes and etc etc and then somebody can go current challenges and then they click or past challenges or  
George Westbrook: I suppose as well for the for the homepage,  
Skye Capazorio: whatever  
George Westbrook: what are the main things you want to get out of that homepage? Um,  
Skye Capazorio: we that's busy being so I I I can't answer that right now.  
George Westbrook: is  
Skye Capazorio: I know Edwin is working across more refining the information that that exists within that  
George Westbrook: it  
Skye Capazorio: space. I think we should be, as he said, we should be using our websites to help inform people, but ultimately pushing as much traffic to the apps, you know, in to the app for the challenge for production trading. um in terms of that and then you know I don't I don't see the website becoming the central content hub for inplay like it would be for formula 1 for example you know where people are being driven to the website and that's got uh you know loads of content that's constantly being refreshed within that space  
   
 

### 01:02:43

   
George Westbrook: And so that one were you referring to the the global homepage or the the challenge homepage?  
Skye Capazorio: well both I suppose on a certain level because they we're trying to keep it the challenger's purpose is to SEO obviously and ranking but ultimately to provide people with enough information that they  
George Westbrook: Okay.  
Skye Capazorio: they download to move as opposed to inundating them with information like it's almost like we want them to go and explore more on the app. We don't want to give them everything that is capable and possible within the app on the website.  
Edwin Johnson: Yeah. So,  
George Westbrook: H  
Edwin Johnson: I look at it like this, like the advertisers are not going to go download the app to find out what this is all about first that Sky reaches out to. So, I wanted this to be like kind of a placeholder. So, it's like, hey, what the f***** going on? Okay,  
Skye Capazorio: Yeah.  
Edwin Johnson: they they got this up. Great. I also think you can um like our our our lead advertisers should be on this page as well.  
   
 

### 01:03:36

   
Edwin Johnson: It gives them um you know exposure but also legitimizes us as a  
Skye Capazorio: Okay.  
Edwin Johnson: competition. So if we do get some marquee names up there, I think that would be very  
Skye Capazorio: Yeah,  
Edwin Johnson: helpful.  
Skye Capazorio: Edwin, do you see that being like almost like we could we could have a ticker that goes up at the top almost that goes our partners? Like obviously the trading challenge when we have a name, title, partner of the actual trading challenge, they would be embedded in the logo and all of that sort of stuff. But maybe there's a ticker at the top that we can keep adding to.  
Cody Haugen: Okay.  
Skye Capazorio: I think that would be that would be good.  
Edwin Johnson: 100%.  
George Westbrook: I suppose it's how much information if any at all like say obviously the leaderboard stuff from the actual real data. Um, so do you want any matchbased stuff? Any any leaderboard based stuff or it is literally just no  
Edwin Johnson: I I don't think so,  
Skye Capazorio: What's  
Edwin Johnson: George. I don't think so.  
   
 

### 01:04:31

   
Edwin Johnson: And I'll tell you why. We want to push people to that app,  
George Westbrook: leaderboard?  
Edwin Johnson: right? I I think we'd rather have them like get their information from the app. the more times are on the app, the better it is for our advertising metrics because I don't think we're going to make any, you know, measurable headway by people going to the website to see what's  
Cody Haugen: think I agree 100%. Yeah.  
Edwin Johnson: up.  
Cody Haugen: Yeah. I mean, the website's really the core is going to be, you know, how do you get to the app,  
Skye Capazorio: Christmas.  
Cody Haugen: right? That's that's the point of the website. And then we want as much of the engagement through the app as possible. Whether it's a desktop app or a mobile app, the app is the  
George Westbrook: H  
Cody Haugen: key.  
George Westbrook: because part of me is thinking And if there's a user who knows what it is, perfect. They know what it is. They want to download it straight away.  
   
 

### 01:05:27

   
George Westbrook: But if there's somebody who's maybe just stumbled across it, maybe they do a bit of discovery. Are they going to read it all? Maybe. Do we need to provide something more in terms of value on the website? Um, or we just going to like stick with the strip it down just get to the app? Because I suppose it's for people that know what they want to do that's fine. They'll go in, they'll click, they download the app.  
Cody Haugen: Could  
George Westbrook: But somebody who's maybe on the bottom portion of that user conversion, is there more value that needs to be  
Cody Haugen: we house the education then just on the website?  
George Westbrook: provided?  
Cody Haugen: I was just about to say that I think that's that's a good place for educa like some of the education not all of it because we want to have again a way to get people to the app but I like very very high level you know some explainer videos some educational content or the hype video uh you know newsletters like things like that I think is  
   
 

### 01:06:24

   
George Westbrook: cuz and I suppose like more of like a progressive disclosure. So like they can see all let's say there's 12 modules they can see all 12 modules they start clicking through number one and as it gets to halfway through number one it could say if you want to carry on with this go to the app. Um maybe let's let's take the leaderboard. They're scrolling through. They want to see I don't think the leaderboard's a good example. Um it it could be in terms of the money like they can see, okay, this person, he's done XYZ and he's going to be paid out this amount tomorrow. Um the live the live matches, that's one where I think that's that's just going to have to be out. Um because otherwise they're just going to stay they're just going to stay on the website. Um unless there's certain mechanisms where no I think yeah I think the live match tracker that's got to be that's got to be in the app.  
Cody Haugen: We don't want any of that on the on the landing page.  
   
 

### 01:07:18

   
George Westbrook: Um  
Cody Haugen: It's too high value.  
George Westbrook: okay that's made it that makes it a lot clearer. And with the like kind of overall design direction um I don't know if you had a chance to look through it. Where where is it  
Skye Capazorio: I think just to answer that. So, at the moment, um,  
George Westbrook: sitting?  
Skye Capazorio: we are just finalizing a, um, a flyer, an information flyer that's going to go out. Um, and that I think will form a a a substantial portion of the baseline for what the challenge website will be. Um, I think that's probably the first point of departure and I know I know Edwin's working on that. So, as soon as we get that, we'll then um we're going to just give it over to a designer purely just to color correct it, put the right logos in, all of that sort of stuff. And then from there, we'll be able to hand that over to you with then additional content outlines of what we would like to be in the challenge website um across the the different pages.  
   
 

### 01:08:28

   
Skye Capazorio: So, if you can just hang on a tick for us on that and then we'll get you that because I I I don't see it being like a complete overhaul,  
George Westbrook: Yeah.  
Skye Capazorio: but I definitely think they're going to be um adjustments and changes that need to need to happen from what it was what it was originally replicated off the back end  
Edwin Johnson: Just so we have consistency,  
Skye Capazorio: of.  
Edwin Johnson: George,  
George Westbrook: Yeah. Yeah. Yeah. That Yeah, that makes a lot of sense.  
Edwin Johnson: around  
George Westbrook: Right. Do you put a you put a question in, didn't  
Brett StClair: Are you happy with the logos SVG?  
George Westbrook: you?  
Brett StClair: I just figured while I was doing it at all your inplay logos as well and got them all on transparent, not transparent and all that kind of stuff and then threw together quick CI for you.  
Skye Capazorio: Yeah. So,  
Brett StClair: That was I just wasn't sure.  
Skye Capazorio: I need we need to go we need to go through that. Um uh but once again I also I need Yeah.  
   
 

### 01:09:22

   
Skye Capazorio: I need to go through that and then we just need to see what we need to refine like we're doing with the flyer. Okay,  
Brett StClair: Okay, let's finish off with the last piece um for the advertising.  
Skye Capazorio: super  
Brett StClair: How we're going to approach this is we are going to tie that to the prototype. And so the prototype is getting to a stage where we can get to at least like a 0.1, not a 0.01. um in that we're going to take all this feedback, right, and then we're going to roll it through into the prototype and get us to some space. We're going to start identifying some initial holds of where ads could go and then I think we need to do a session working through the prototypes, going through what the ads look like, what they're going to do, all that kind of stuff. And then we can start refining those. And then there'll be more the sessions after that will be more like a this is what we've got us refine but we also uh can we load I don't think we can load the the prototype app onto your review.  
   
 

### 01:10:28

   
Brett StClair: Hey George I don't think we  
George Westbrook: We It's a different Oh,  
Brett StClair: can  
George Westbrook: do you mean the feed?  
Skye Capazorio: What's  
George Westbrook: I I need to work that one out because there's the first giving everybody because it's it's not like a  
Skye Capazorio: next?  
George Westbrook: web app where you can just post it to your URL. Um, so we'll get that sorted hopefully.  
Cody Haugen: Oops.  
George Westbrook: Just waiting on a review from Apple for a a certain account thing we need to do. It's not for the app store. Um, it's Apple's just very funny with even deploying something for testing. Um, so we're just getting that get that testing. then you can have all have the app on on your phone to click around with and then need to look to  
Brett StClair: Person.  
Skye Capazorio: Hi  
George Westbrook: integrate the that the sim similar maybe not the same um feedback thing that we've got  
Skye Capazorio: there.  
George Westbrook: for the challenge website I'm pretty sure we can get get it done um it's just the slight unknown um but I thought we'll get we'll get the prototype stood up deployed and  
   
 

### 01:11:20

   
Edwin Johnson: What is that?  
George Westbrook: then then get the feedback going and then it will be iterate iterate iterate  
Edwin Johnson: I mean only a few of us need access to the prototype as soon as possible so we can you know start a sale sales process.  
George Westbrook: H.  
Skye Capazorio: Oh,  
Edwin Johnson: The one thing I would tell you, oh god damn, sorry about that.  
George Westbrook: Yeah.  
Edwin Johnson: Um, about the ads is, you know, when you think about where to where to put them in, the the key here is we're selling the the the premier moments in sport. That's where the advertisers going to get the most value. That's where we're going to get the most money. That's where the user is going to have the most unique experience. We're literally selling those key moments. Okay.  
Skye Capazorio: Yeah.  
Edwin Johnson: But for the the marquee dollars, it's, you know, a big play happens. Who put the money behind that? You know, who who's do  
Skye Capazorio: Yeah. What another thing Edwin I just wanted to add post Cody and my catch up yesterday surrounding this that we're also going to  
   
 

### 01:12:18

   
Edwin Johnson: that?  
Skye Capazorio: be working on over the next week to help also input and and inform that is that the way that the way that we are probably going to package the  
George Westbrook: This  
Skye Capazorio: selling of this is on a on a game by games.  
George Westbrook: is  
Skye Capazorio: So you'll so you'll be able to purchase a se a selection of games that you want to be adjacent to essentially as a brand. And so think about it through that lens that somebody is purchasing to be adjacent to that game and layering exactly what Edwin said, the moments that matter in those games specifically and where their brand can show up and activate. And that we're going to be billing the clients with advertisers based on minutes of engagement. And that's not necessarily minutes of engagement where they are like clicking on the actual brand to see what's going on there, but in those interfaces whether they are seeing a matchup that's happening and then being able to then click into one of the teams and go onto the team page and stuff like that and then interact within that space.  
   
 

### 01:13:29

   
Skye Capazorio: Just think of it through that lens is that's how we think is going to be the best way to package it with an overarching tier then being above that which is then rather interfacing more I would say from the trading aspect of the of the user. So that's the other layer. So ownership of the trading challenge um the the the more the more specific to the user spaces like the P&L like the education modules all of that sort of stuff. are kind of split into those two layers. Does that make  
Edwin Johnson: It does. Let me give you a little advice though.  
Skye Capazorio: sense?  
Edwin Johnson: I because I thought about this as well in terms of selling the individual games. You really need to package them in the blocks, you know, right? Like  
Skye Capazorio: 100 billion%. We're not going to say to somebody you're allowed to choose one game. No, that is not going to be the case at all.  
Edwin Johnson: because we're going to need support for that. Like the games that don't have a lot of,  
   
 

### 01:14:23

   
Skye Capazorio: 100%.  
Edwin Johnson: you know, expected  
Skye Capazorio: Yeah, I agree 100 billion% Edwin.  
Edwin Johnson: viewership.  
Skye Capazorio: Sorry I I wasn't clear on that. That is the intention that we'll be doing that. It was more just making reference to what the spaces are that we're giving to the advertisers and how we're segmenting  
Edwin Johnson: Yeah. And just so the Rebel Lab soon to be new name team,  
Skye Capazorio: that.  
Edwin Johnson: um Cody and Sky, do you see this then as you know with 2,100 games that there's like a minimum of 200 games or whatever it may be?  
Cody Haugen: Yes,  
Edwin Johnson: Right.  
Cody Haugen: there's a minimum on these block packages that people need to and based on guys  
Skye Capazorio: Yes.  
Cody Haugen: tiering idea. Maybe at the high level the minimum is three. At the lesser games the minimum is 15. Something like that. So it is scalable so that we make sure all games are chewed  
Edwin Johnson: Yeah. Yeah. And then obviously like the placement's really important for each game.  
   
 

### 01:15:17

   
Cody Haugen: up.  
Edwin Johnson: So you got a second here. Okay. And then as we were discussing last week, just to reiterate now,  
Skye Capazorio: Yeah.  
Edwin Johnson: there may be games that actually on paper don't look that exciting, but for our user base will be very exciting, especially if it's, let's say, the final game of the night.  
Cody Haugen: Mhm.  
Edwin Johnson: And that that is the difference between them caching and not caching. Um, you may see a lot of activity that otherwise you wouldn't if not for the inplay challenge.  
Skye Capazorio: And this is part of what we'll also build into the sales deck, Edwin, is exactly the narrative surrounding that. Like what are the what are the benefits of being adjacent to a tier one team, a tier two t a tier one game, a tier two game, and a tier three game.  
Edwin Johnson: Yeah.  
Skye Capazorio: Um and and and putting the information in there aligned to that.  
Edwin Johnson: And right and then there's tier one days versus tier 2 days. Right. So like Thursday night football may not be that big to people but Sunday football is much bigger.  
   
 

### 01:16:23

   
Cody Haugen: So,  
Skye Capazorio: Yeah.  
Cody Haugen: Sunday night football game,  
Edwin Johnson: And obviously  
Cody Haugen: it should be the pinnacle of what we sell because it's a whole day of a lot of games and that's the last game to cash.  
Edwin Johnson: Yeah. Yeah. You would think so, Cody. And now with Thanksgiving, they have the Bears playing Detroit. Um I don't know if you saw a schedule. Uh but that that's those are two great markets for us to really push the challenge on. You know, I did you see any other teams on on Thanksgiving, Cody?  
Cody Haugen: Uh I have not uh looked at I know the full schedule rolls out at uh I think 400 pm  
Skye Capazorio: This is awesome.  
Cody Haugen: Eastern.  
Edwin Johnson: Okay,  
Cody Haugen: Yeah.  
Edwin Johnson: Brett, you strike me as more of a Golden Bear guy. California golden.  
Cody Haugen: Um the the last piece of uh focus I want to add to this  
Edwin Johnson: Yeah.  
Cody Haugen: is something I've I've given a lot of thought to and shared with Edwin too.  
   
 

### 01:17:15

   
Cody Haugen: It's part of our education journey. Uh Kevin is that not every good team matchup of let's say you know the Rams are going to the Super Bowl or projected and so are the Bears.  
Skye Capazorio: What's  
Cody Haugen: And so that hypothetically is a good game to watch because they're two Super Bowl contenders.  
Skye Capazorio: that?  
Cody Haugen: Well, typically Super Bowl contenders have very good defenses. Very good defenses lead to very little scoring. And so that as far as a uh a high volatil or a high volatile game with a lot of trading probably won't happen.  
Skye Capazorio: There's  
Cody Haugen: So something we have to educate our advertisers and our users in doing is to  
Skye Capazorio: just  
Cody Haugen: actually probably go down the funnel and so that those lower tier games where it's  
George Westbrook: It's not  
Cody Haugen: Jacksonville who's one and six versus the Dolphins who are also one and six is actually probably a better game to trade because their defenses suck and so the game is probably 35 to 21.  
Edwin Johnson: Well, well, you're hitting on a really good point, Cody, which is um the monetization is about the user experience.  
   
 

### 01:18:22

   
Edwin Johnson: It's not necessarily about the quality of the competition of of the the the gameplay itself,  
Cody Haugen: Right.  
Edwin Johnson: but the actual user competition on our platform because, you know, otherwise like a lot of these like s*** teams and like buy foregone games, they don't get great viewership on those. You know, some of them are less than 100,000.  
Cody Haugen: That's where that's where the NFL is going to love us because the viewers on a Jacksonville game are always bad and they're gonna like, you're bringing millions of new eyeballs to a Jacksonville versus Dolphins game.  
Skye Capazorio: I don't know about that.  
Edwin Johnson: Yeah.  
Cody Haugen: This is amazing. So, yeah. Uh, so real quick,  
Edwin Johnson: Yeah.  
Cody Haugen: I don't know if anyone saw, but this year there's going to be a Thanksgiving Eve game between the Packers and the Chiefs.  
Edwin Johnson: Oh man, that's a great game.  
Cody Haugen: One, it's a Wednesday night game, so that's great because it's midweek on a Wednesday, but and then plus the three Thanksgiving games that which they just announced.  
Edwin Johnson: Yeah. So, Troy, what we should do when we start to build out the pricing,  
   
 

### 01:19:21

   
Cody Haugen: So,  
Edwin Johnson: you know, we have a big belief that the Thanksgiving games because families will all there's not much else to watch, you know, here in the States. So, a lot of people just have football running in the background and if the the people are around their families and they're trading,  
Cody Haugen: right.  
Edwin Johnson: we think that's an amazing way. So, especially if we up the challenge uh for like a mini challenge within challenge for Thanksgiving Day and maybe we, you know, maybe we're we're going to out of that 25 million bucks, maybe we have those three games we give away a million each uh during those games. So, people people can try to make, you know, maybe maybe we give, you know, a million dollars to the best trader that for each game that day.  
Cody Haugen: Yeah, here's the other here's the other thing that that I just found out as well. It's only being streamed on Netflix.  
Edwin Johnson: Oh man.  
Cody Haugen: Yeah,  
Edwin Johnson: So that we got to talk to  
Cody Haugen: they did that game.  
   
 

### 01:20:21

   
Cody Haugen: Yeah,  
Edwin Johnson: Netflix.  
Cody Haugen: they did that for the Christmas Day game last year. Where  
Skye Capazorio: That's Omnicom. That's Omnicom.  
Cody Haugen: is  
Skye Capazorio: Just so you  
Edwin Johnson: We've got to talk to them because they they've had to pay over a hundred million for those  
Skye Capazorio: know.  
Edwin Johnson: rights.  
Skye Capazorio: Yeah. Yeah.  
Edwin Johnson: And if if they if they have a repeat of last year where nobody watched those games because both  
Cody Haugen: easy?  
Edwin Johnson: the teams like the Kansas City and Dallas, they were like they had injuries, people were out of the playoffs, they they had a putrid viewership. Um this would be a an amazing way for them to ensure they're going to have people watching no matter  
George Westbrook: Let's  
Edwin Johnson: what.  
Skye Capazorio: Yeah,  
Cody Haugen: in LA because it was and the Packers,  
Skye Capazorio: absolutely.  
Cody Haugen: not the Chiefs. Rams and the Packers. Rams and the Packers, not the Chiefs. Oh, I love the NFL. And it's in LA. It's at the stadium.  
   
 

### 01:21:08

   
Edwin Johnson: Cool. Yeah,  
George Westbrook: go.  
Edwin Johnson: that's great. Yeah.  
Cody Haugen: Yeah,  
Edwin Johnson: So, when we build out the pay schedule,  
Cody Haugen: they're they're trying to move up the schedule.  
Edwin Johnson: George, we're we're going to have these special events. And then there's always like there's these rivalry games like Ohio State Michigan will likely have something special for that game as well, you know? So things like that that are every year it's just like doesn't matter how good the teams are, they hate each other so much and the fans go crazy for it. You know, it's I'm sure it's like that way in in uh your soccer, whatever European football, you know,  
George Westbrook: proper  
Edwin Johnson: where Yeah. I mean, we just hate the other team so much.  
George Westbrook: football.  
Edwin Johnson: You don't care what the score,  
Cody Haugen: What?  
Edwin Johnson: what the records are. You just want to win that game.  
George Westbrook: Yeah. Yeah. What one thing I was thinking in terms of the advertising  
Edwin Johnson: Yes.  
   
 

### 01:21:56

   
George Westbrook: on the game moments. Let me just let me just get something up because otherwise this is not going to make sense for trying to explain it because where the advertisers can get the like maybe the best bang for their buck. This is a very raw page so ignore it. Um, so imagine there's the this is the game day page. There's the option to go live, blah blah blah. Um, and then in the timeline, every time they go back to a specific time, that ad can maybe repop or maybe so then it's cuz  
Edwin Johnson: Oh yeah.  
Cody Haugen: That's  
Edwin Johnson: f******  
George Westbrook: I'm because it's like I just think if I was the  
Edwin Johnson: brilliant. Brilliant.  
Cody Haugen: awesome.  
Edwin Johnson: George.  
George Westbrook: advertiser, so you'd have to assume you're only getting the bang for your buck if the user is on the page when that moment happens. And if they're not on the page, they're not going to see it. But obviously with something like this where they can they can replay it.  
   
 

### 01:22:51

   
George Westbrook: So there's a there's a 12 yard rush and then there's a specific thing that comes up for that and every time somebody goes back to that. One thing to think of e as well is for past performance. So if a user goes to a past game maybe six weeks ago, maybe the ads stay on that page as well. So let's say this was this wasn't live. This was 6 weeks ago. um when they click back through it again, they're still going to see the ad, which maybe is going to drive up the perceived value from the advertiser because it's not like this transient moment that comes and goes, flashes up. If you're there, brilliant, you saw it. If you weren't,  
Edwin Johnson: you missed  
George Westbrook: you're not going to see it come up again.  
Edwin Johnson: it.  
George Westbrook: Um whereas this, it's kind of it's living there every single time a user goes back to the page.  
Edwin Johnson: And why those in-game moments are so important is because that's where your price changes are going to happen.  
   
 

### 01:23:44

   
Edwin Johnson: So, if you're looking at like you're going to trade it, you're going to be like, "Oh man, this thing just dropped three bucks. What the f*** happened?" and you click on that and you're like, "Oh, yeah." Like a key player got hurt or something.  
George Westbrook: Yeah.  
Edwin Johnson: That's different than like a drop touchdown pass. You know what I mean? That's really brilliant.  
George Westbrook: Yeah.  
Edwin Johnson: That That's incredible. Great idea, bro. That's awesome.  
George Westbrook: Um, yes. Yes. So, so like like we said, I think it was yesterday, we'll get we'll get this stood up to a certain point and then it will be right now let's switch to advertising mode. Obviously, we'll still be making iterations to the look, the feel, the UI for the things that aren't ads. But obviously now we've got once we've got something stood up, it's like, okay, what's going to interfere? What's not going to interfere? What pages would we want something? What pages wouldn't we want something?  
   
 

### 01:24:35

   
George Westbrook: How do we want it represented? And things like that.  
Edwin Johnson: cool. I mean, it's really good. I think these module sessions have been incredibly uh valuable overall just in I mean obviously with the output but just in terms of everyone being on the same page as far as what's going on because the idea flow uh from from all sides are really really good. So really thank you very  
Brett StClair: On that note, we're done with the modules. So, now it's time for us to focus on getting subm modules out, get those prototypes out, get the advertising bits going, and we're going to be pushing for our first prop. Um, so we give us tomorrow to wrap up the the documentation. Hopefully George's bane of his life for some reason that authentication module may have given you some form of relief um be able to get you onto the system if you can spend the weekend perusing it. See if you can pick up anything. Don't don't do it's a lot. It's a lot.  
   
 

### 01:25:48

   
Brett StClair: So George, myself and Max and the son read this the whole time. And this is I'd probably be far rather be reading a Harry Potter than going through  
George Westbrook: His  
Brett StClair: the detail that these cover, but it's really really  
Edwin Johnson: The question, the real question is,  
Brett StClair: important.  
Edwin Johnson: would you be rather reading the Bible?  
Brett StClair: Yes. Um  
Edwin Johnson: Given your past history of sins,  
Brett StClair: I  
Edwin Johnson: I find that to be incredible.  
George Westbrook: his hands burn as soon as He touches a  
Edwin Johnson: Oh,  
Cody Haugen: Is  
Brett StClair: got if you believe If you believe Dan Brown and the St.  
Edwin Johnson: the sizzle.  
Cody Haugen: that  
Edwin Johnson: He's got the sizzle.  
George Westbrook: Bible.  
Brett StClair: Clair clan, you guys are talking about great papa Jesus to me. You  
Edwin Johnson: Yeah. I mean,  
Brett StClair: know,  
Edwin Johnson: I think your name is a perfect name for any kind of like uh like perverted villain in any movie. You know who's behind this? Brett Sinclair.  
Brett StClair: I like that.  
   
 

### 01:26:45

   
Brett StClair: Have you seen you seen the Avengers?  
George Westbrook: Yeah.  
Brett StClair: So the Avengers is famous kind of spy movie or spy series in the  
Edwin Johnson: I Yes.  
Brett StClair: 70s loved it with Roger Mo and I can't remember the American  
Cody Haugen: Good enough.  
George Westbrook: Oh.  
Brett StClair: guy and uh they were Sinclair and his name was Brett Sinclair not Sinclair  
Edwin Johnson: Yeah,  
Brett StClair: but and so I was named after the Avengers. So if you meet anyone in this country who's in their late 70s, especially ladies, they go, "You have a dishy  
George Westbrook: I I think I think anyone I think anyone who's not a  
Brett StClair: name.  
Edwin Johnson: that's awesome.  
Cody Haugen: This is all the  
George Westbrook: boomer when you said Avengers did not think of the 70s spy show.  
Cody Haugen: rest.  
George Westbrook: I think we were all thinking superheroes. I was I was like spies in Avengers.  
Brett StClair: Wait.  
George Westbrook: What What was he talking about?  
Edwin Johnson: You know, we get old, George. It happens. We start remembering what we want to remember.  
Brett StClair: No.  
Edwin Johnson: Fair enough. What a great day. Again, thank you all for this. If you need anything else, please reach out. Um, and then I will have the flyer done  
Cody Haugen: Yeah.  
George Westbrook: Perfect.  
Cody Haugen: If nothing, Edwin, it'll help the AI train a higher level of thinking. Yeah. everyone.  
Skye Capazorio: Thanks everyone.  
Edwin Johnson: Hey,  
Brett StClair: Thank you everybody. Touch.  
Edwin Johnson: finally.  
   
 

### Transcription ended after 01:30:56

  

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.

**