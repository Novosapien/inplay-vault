---
date: 2026-06-01
type: standup
status: extracted
extracted-to:
  - "[[digests/touchdowns-01-10-jun-2026]]"
---

## Post-Call Analysis

> Processed as part of the **[[digests/touchdowns-01-10-jun-2026|1–10 June touchdown sweep]]**.

| Finding | Destination | Action |
|---------|-------------|--------|
| Helmet realism — AI-generate realistic helmets for 163 teams with exact hex codes (Kevin supplying) | [[digests/touchdowns-01-10-jun-2026]] | Logged (build asset, no doc change) |
| Header lock vs scroll — leave scrolling for now; trader UX > advertiser > rest; sponsorships sold on exposure-minutes | Advertising (cross-cutting) via digest | Noted |
| "Territories" / page-ownership naming (gamecast, info centre, referral bank); Amex "owns the space" reference | Advertising (cross-cutting) via digest | Noted |
| Homepage takeovers (hue-of-red Coke background) idea | — | No action (exploratory) |
| Review tool / PWA working; goal = first app with onboarding + referrals + information stack | — | No action (build status) |
| Persona KYC back with Bowler/Matt | [[customer-onboarding/customer-onboarding]] | Superseded by 03-06 "signed" |
| Timeline — first app for download ~next week or two, latest 19 June; referral live before July 4; Father's Day bonus floated | — | No action (status; calendar already in [[referral/referral]]) |

---

**

Jun 1, 2026

## Meeting Jun 1, 2026 at 14:31 BST - Transcript

### 00:00:00

   
Brett StClair: Hello  
Edwin Johnson: Hey, hey.  
Brett StClair: everybody.  
Edwin Johnson: Hi,  
Kevin Murray: Hey guys,  
Edwin Johnson: Brett.  
Kevin Murray: how are you?  
Edwin Johnson: Hey, Kevin. What's up, Gary?  
Kevin Murray: Hey very  
Gary Anderson: Good morning everybody.  
Edwin Johnson: How are you all?  
Gary Anderson: Good.  
Kevin Murray: well.  
Edwin Johnson: Getting old,  
Kevin Murray: Yourself?  
Edwin Johnson: man.  
Max Kingaby: Hi, bro.  
Kevin Murray: Hey George. Hey Max.  
George Westbrook: How we  
Max Kingaby: Hey guys.  
Edwin Johnson: Hi, Max. Hi, George.  
Max Kingaby: Hey.  
Edwin Johnson: George,  
George Westbrook: doing?  
Edwin Johnson: another f****** home run, bro.  
Kevin Murray: Good.  
Brett StClair: She only knows.  
Edwin Johnson: just constantly hitting these home runs. The latest updates badass. Um couple just a couple of little tweaks.  
George Westbrook: Perfect.  
Edwin Johnson: Couple of the logos are are like black on or dark on dark. So it's like you can't see the Toyota or the Cash  
Kevin Murray: Good.  
George Westbrook: Okay.  
Edwin Johnson: App.  
George Westbrook: The Yeah, f****** thought I fixed them. The Toyota one cuz it's black. Yeah, it's black writing.  
   
 

### 00:01:16

   
George Westbrook: And I remember telling speaking to AI and saying, "Put it on a white background. It's not done  
Edwin Johnson: Yeah. So that those so just if the ads pop out,  
George Westbrook: it.  
Edwin Johnson: let me ask you a question because I actually have an in-person demo today which pretty exciting um at a big bank um who who is a huge sports advertiser here. Okay.  
Brett StClair: No.  
Edwin Johnson: And primarily in Chicago, but I'm hoping to push them to be like become a nationally recognized brand.  
Kevin Murray: Thank  
Edwin Johnson: Okay. And uh anyways on within the app it's so freaking great  
Kevin Murray: you.  
Edwin Johnson: man. They um you know do we think and this is me think it's a question not not a request. Do we think um are we capable of enhancing those helmets to be more realistic looking? Because if I had to if I had to say they look that that's a weak point. They look a little weak.  
George Westbrook: Yes, it is possible. It's just it it's not as So what we what have we done at the moment?  
   
 

### 00:02:19

   
George Westbrook: We've created like SVGs or vector graphics which is very easy to just replace the color. Um cuz I remember the one that you sent over those helmets look way better. But one of the things that we'd need to do is find a way to So what's there? 130 college teams and how many NFL?  
Edwin Johnson: 32 163.  
George Westbrook: 32. Yeah. So 163. We'd need to we'd need to generate 160 images. You use an AI um that would look exactly the same. Um which is doable, but it's not a it's not a hey Claude, can you can you just go and do this for me and it will take 20 minutes. I agree with it's something we definitely want to do before the before the launch. Um it's just it will take a bit bit of bit of working to make sure that it's right. Oh no, I think no we could do it.  
Edwin Johnson: Yeah.  
George Westbrook: We generate one and we add it as a reference image.  
Edwin Johnson: Yeah. I mean, I I struggled to make the helmets, too,  
   
 

### 00:03:12

   
George Westbrook: Yeah.  
Edwin Johnson: because every time I wanted to do it, they always want to throw in the logo, and I'm like, no logo, right? And then it's like,  
George Westbrook: Yeah.  
Edwin Johnson: okay, well, the colors, the you know, they for some reason, I think you guys told me last week, you know, once you get into like the weeds on these prompts, they can really put you into a spin cycle. So, it's like, you know, um Yeah. So, it took me a while to get those helmets right myself right where it's looked a little bit differently. Um, and we have to double check the colors, you know. So, when you're when you're talking to your your model,  
George Westbrook: Yeah.  
Edwin Johnson: please ask it to to make sure that the colors are exact because the blues like the blue from say Michigan uh University of Michigan is different than the blue from the University of Florida.  
George Westbrook: Yes. See, that's one thing with the colors as well is is making sure that they it might be difficult to  
Hasan Mohammed Ahmed: Yes.  
   
 

### 00:04:05

   
George Westbrook: make sure that they are like the exact hex code of that of that team. Unless unless we do it in a more traditional  
Hasan Mohammed Ahmed: Nightmare.  
George Westbrook: coding or vector graphics in a way we'll work something  
Edwin Johnson: Yeah. Yeah.  
Kevin Murray: Judge, just a quick one.  
George Westbrook: out.  
Kevin Murray: Would it help, say, if I went through and grabbed all of the colors of the teams and wrote the hex codes down to send to you?  
Edwin Johnson: Yeah.  
Kevin Murray: Would that be easier or is that just a pain in the ass?  
George Westbrook: Uh um no no that that's I think I think that's one of the process we went through or a AI went through. um it we just sent them out in parallel.  
Hasan Mohammed Ahmed: 360 days.  
George Westbrook: It's like for each of these 160 teams get the get the hex codes and then that's when the when it created  
Kevin Murray: Yeah.  
Hasan Mohammed Ahmed: The SVG.  
George Westbrook: the SVGs it should be the exact hex codes. Um but yeah we need the because I think from memory when you did it before Ein there was like the like the really nice like haloy gradient effect.  
   
 

### 00:04:59

   
George Westbrook: Um cuz what what so we need to work out how we can do that.  
Edwin Johnson: Yeah.  
George Westbrook: So I think it  
Edwin Johnson: I mean, I had I mean,  
George Westbrook: would  
Edwin Johnson: they're AI generated for me. It just took me like three hours to get it to look right, you know? And I mean,  
George Westbrook: Yeah.  
Edwin Johnson: it's a waste of time, right?  
Brett StClair: Yeah.  
Edwin Johnson: Like I mean there we I'm sure the agentic stuff can do it a little bit quicker but the more realistic the  
George Westbrook: Yeah.  
Edwin Johnson: helmets look it just looks like a richer experience right and you know we're trying to sell premium so we want to make sure we can sell premium the other question I had and this is for the group do we think that the um the advertisement tiles uh specifically at the top should the header remain as you scroll down throughout that let's say the homepage should that header of the Coca-Cola and welcome George always be at the top. So you you scroll underneath or do we like that it scrolls and disappears?  
   
 

### 00:05:53

   
George Westbrook: My personal opinion is it scrolls away because it's it's not on it's not on um sorry let me close this door  
Edwin Johnson: Yeah.  
George Westbrook: um it's not on it's not on desktop so like the real estate we've got is the bottom there's obviously the navbar which can't that can't go Um,  
Edwin Johnson: Right.  
George Westbrook: and then the top as well. And then let's say each one's 12.5%.  
Edwin Johnson: Fair.  
George Westbrook: That means we're only working with  
Edwin Johnson: All right. And then it kind of like diminishes any ads throughout the scroll process because you're getting double banged on  
George Westbrook: 75%.  
Edwin Johnson: the ad thing. Cool. So, and then I had a feeling you might suggest that. Do we think that um behind the ad specific tiles throughout the scroll, do we want to have um something like a a glow behind the tile that like stands out a bit? So like maybe like a a different kind of glow. I think on one of them there's um on the on the MX there was like a high u like a blue outline on on the MX tile which actually made it really look professional and stand out pretty nice.  
   
 

### 00:07:05

   
George Westbrook: Have a look the I'll I'll get my screen up now.  
Edwin Johnson: I can tell you Yeah.  
George Westbrook: Is it going to allow me to do  
Edwin Johnson: Um, I think it's I think it's under  
George Westbrook: this?  
Edwin Johnson: uh I mean you really did a great job though, bro. Like I mean let's not kid each other. It's awesome.  
George Westbrook: Wait. Can you Can you all see this?  
Edwin Johnson: Yeah. Yeah.  
George Westbrook: Yeah.  
Edwin Johnson: I'm on that same page right now, boss.  
George Westbrook: Um, yeah. So, is it was it was it this one you were talking about?  
Edwin Johnson: I think so.  
Kevin Murray: Yeah, it's on the trade page. Yeah.  
Edwin Johnson: Yeah, it's on the trade page. But for some reason, one I thought I maybe I'm maybe I'm going crazy. I thought the outline of this premium access every market day down uh keep going down on trade page. Yeah, right there. For some reason, I thought that had a different blue hue around it.  
   
 

### 00:07:59

   
George Westbrook: So, so like a kind of halo halo  
Edwin Johnson: Yeah. I mean, maybe it's You know what? probably in my haste,  
George Westbrook: effect.  
Edwin Johnson: it's probably the the fact that it has like a gradient behind it makes it stand out, right? Like it definitely pops off the page more than the  
George Westbrook: H there was one that I was thinking with the vis visa.  
Edwin Johnson: others.  
George Westbrook: I can't remember. I think I removed it. Um is this kind of it was it was this but it looked like a like an actual card.  
Edwin Johnson: Yeah.  
George Westbrook: I just restart this quickly.  
Edwin Johnson: It's really good though,  
George Westbrook: Um I need to need to restart  
Edwin Johnson: bro.  
Brett StClair: Um, I just want to add the I'm sorry,  
George Westbrook: this.  
Brett StClair: we're just helping Sky there got caught in a loop.  
Edwin Johnson: Like  
Brett StClair: Um, but I just want to check I go back to the header banners. Um, my commercial brain is saying it should  
Skye Capazorio: That's it.  
   
 

### 00:09:00

   
Skye Capazorio: Definitely. Sorry, just to jump in.  
Brett StClair: stay.  
Skye Capazorio: It definitely should stay and the content scroll like as you scroll that back like that brand at the top should stay there.  
Kevin Murray: My thinking with behind  
Skye Capazorio: I don't know Edwin if you disagree with that.  
Kevin Murray: this  
Skye Capazorio: I just think it it shows more perpetual presence for the brand in that space without it being intrusive.  
Edwin Johnson: What were we going to say?  
Kevin Murray: I was just going to say my thinking of when I was scrolling through it as well.  
Edwin Johnson: Keep  
Kevin Murray: Obviously on the homepage you've got the Coca-Cola at the top and the header and then as you're scrolling down then you've got that earn the $500 in play sponsored by Coca-Cola. So again you're seeing Coca-Cola again as you're going through. So that's why my thinking was to to just leave it there and then just scroll through because again as you as you're going up and down you're seeing again Coca-Cola scroll through again you can see it again. if the team if we're going to go with the the teams sorry the the brands that own that specific page.  
   
 

### 00:09:58

   
Kevin Murray: So just just my two  
George Westbrook: is all I think if this was let's just say it cuts off  
Kevin Murray: cents  
George Westbrook: here then we're only working with effectively between there and there for the user P to be able to do stuff.  
Edwin Johnson: Yeah. Yeah.  
Brett StClair: But that's probably  
Edwin Johnson: I I I think we I think we leave it scroll through for now.  
Skye Capazorio: Okay.  
George Westbrook: Um,  
Edwin Johnson: And if the if we get some push back from any marketers that they want it to remain at the top, we do because I tend to agree um that there's other like the cash app. I don't know that they want to share.  
Skye Capazorio: Excuse  
Edwin Johnson: If you go to the homepage, George, and you scroll down, I don't know that Cash App wants to share with the the overhang of Coca-Cola above them, you know. So,  
Skye Capazorio: me.  
Edwin Johnson: if if we are putting more into the body of the scroll, I think that it does diminish it a little bit. But I I asked the same question earlier, Scott.  
   
 

### 00:11:00

   
Skye Capazorio: So,  
George Westbrook: I need to fix this  
Skye Capazorio: one of the I'm just I'm just giving it from some of the feedback that I got last week.  
George Westbrook: page.  
Skye Capazorio: So, one of the things that comes up as being a prime real estate perception wise for advertisers is the ownership of that top banner and even um a level of of gantry Brett from you what we were talking about earlier today. Um, that goes that that goes down the sides. I'm not saying taking up a big block, George, before before it seems like I'm saying squish it. I'm I'm not saying actually change anything of where the information is at this point in time, but if you had that red halo for Coca-Cola, whoever else is the brand within that space, um, it leaves space for, you know, their a bit of their like in the case of Coca-Cola, a red ribbon or a white ribbon, the continuence of it. It's one of the most even though we're not doing programmatic it is one of the most um valuable spaces when it comes to programmatic and and from a um an advertiser perception perspective.  
   
 

### 00:12:05

   
Skye Capazorio: Um so that's that's the only reason why in terms of showing showing that added value that's that's in that space. But if if the consensus is that we don't want it there because we feel we can make up that brand presence more as you scroll down then that remains to be discussed.  
George Westbrook: What is that? The top.  
Edwin Johnson: Yeah.  
George Westbrook: I don't know if you meant the the top area or do you say the  
Skye Capazorio: No. So I I was I was just talking about the side as well as an extension.  
George Westbrook: side?  
Skye Capazorio: So almost like a an archway if you can imagine that. So currently where there is black down the sides there where your where your m where your  
Brett StClair: could be could be Coke bubbles as your  
Skye Capazorio: cursor is.  
Brett StClair: background, you know, or a cold glass of Coke as the background with it sitting on top.  
Skye Capazorio: Yeah.  
Brett StClair: Not an immediate, so let's not squirrel on this. Um, I can see George's squirrel brain going into gear there.  
   
 

### 00:13:04

   
George Westbrook: Uh  
Brett StClair: I think more immediate is Let's go to one of the other  
George Westbrook: it  
Brett StClair: pages, which is this.  
George Westbrook: Quick quick quick note quick note on that. It is if they are taking over because that's effectively them taking over the  
Brett StClair: Yeah.  
George Westbrook: whole page. We've got a way up how does it fit in with the current style and like if we've got these colors blah blah blah and then the background completely changes cuz do does anyone remember that app where you could like pretend to drink a beer from your phone. That that like that was what you meant,  
Edwin Johnson: Yeah.  
George Westbrook: wasn't it Brett? like that.  
Kevin Murray: Yep.  
George Westbrook: But that instead of it being beer, it's  
Brett StClair: what I don't care what the background is. I'm just saying the background could be a hue of red.  
George Westbrook: Coke.  
Brett StClair: Um, so it's called homepage takeovers where you there's areas around it that's integrated into the look and feel that kind of makes it work.  
   
 

### 00:14:01

   
Brett StClair: So I do agree with you. Home takeovers are an effort for everyone. Um, so if you're doing it, it's got to be high value.  
Edwin Johnson: Yeah. Here's here's the thing though.  
Brett StClair: Seriously.  
Edwin Johnson: Like I don't know, you know, see seemingly no one wants to pay for it, but they want to take it over, right? like it's like, you know, these these advertisers until we get like I guess closer to um making deals, you know, I think we try to keep it open for now, right? Like if we have to somehow like make the top cap stay if that's part of what they want and they're willing to pay for it. But um you know, every you know, you know how it goes. No one wants to give us any money. Everyone thinks it's b******* until it's time, but they know how we should do it anyway.  
Brett StClair: So, if we go to the discovery page versus the homepage, um, the homepage is slightly bigger, right? Because we've kind of double layered it.  
   
 

### 00:14:59

   
Brett StClair: So, it's a scary thought of locking a load.  
Edwin Johnson: Yeah,  
Brett StClair: I don't think we're going to necessarily have to double layer everything. So if you go into trade, maybe trade page or reward one of them. Yeah. Like that's not double layering. It's not as thick as the kind of homepage. And so locking loading.  
Edwin Johnson: sure.  
Brett StClair: So the what you want to do especially right now is to win credibility and to be able to use a metric like we promised x billion minutes. Well, you actually got X billion minutes of your own brand directly in front of it rather than scrolled through. So, your scrolled through experience when you're doing sponsorship is where I worry. If it was CPM, I would say scroll it up. You get an opportunity. CPM translates into CTC, which is clicks. So, if you get clicks, cost per click, um, fine. That model's fine. You scroll up. But I think you're doing sponsorships. You need to back the brand here.  
   
 

### 00:16:01

   
Brett StClair: Give them the minutes of exposure, right?  
Edwin Johnson: It's a good  
Brett StClair: You we're promising that we should be doing it. And then yes,  
Edwin Johnson: point.  
Brett StClair: we'll have other ad units that add to it. And so the engagement with the brand will be look, you get to lock and load them, but now you get all these other engaging volatility moments, uh, whatever moments that are really active. And so we're really bringing some engagement with your brand to our user and then you you're kicking off both metrics. Um and then at the end and you can go, yeah, you expected X, we killed it for you. That's the story we want right now. And I think so I'm I'm I'm on the side of George. Your I think the priority should go your trader needs the best experience. So top priority is is the experience. The second priority is the advertiser. The third priority is whatever else. Um, but in some cases we do have to sacrifice some user experience to make sure we hit the metric to blow them out of the park.  
   
 

### 00:17:09

   
Brett StClair: And it feels like, and I agree with Sky, it feels like that's that's something that we give away on a piece of real estate we could give away on to hit that mix.  
George Westbrook: So,  
Kevin Murray: Is there a way that Go ahead,  
George Westbrook: tighten this up and keep it there.  
Edwin Johnson: Okay.  
Kevin Murray: George.  
George Westbrook: That's that I was going to say. So,  
Kevin Murray: Sorry.  
George Westbrook: tighten this up a bit. Bring that up. Move that down. Make it a little bigger. So, it's similar to here.  
Brett StClair: Here we go. That's the one I was looking for. There we go. You see? Oh, have you done it already? Or was it already doing  
George Westbrook: Uh,  
Skye Capazorio: on the American Express one there is it it's the only one that stays static.  
Brett StClair: it?  
George Westbrook: this  
Skye Capazorio: at the top. I also think that they should it should be like and I don't know,  
Brett StClair: Thanks.  
Skye Capazorio: sorry before I got on if this was covered, but more like the American Express side where it looks like they own that space as opposed to just being the logo off to the side.  
   
 

### 00:18:08

   
Skye Capazorio: So like this is the American Express Gamecast.  
Brett StClair: Yeah,  
Skye Capazorio: Um,  
Brett StClair: works better,  
Skye Capazorio: yeah.  
Brett StClair: right?  
Skye Capazorio: So, it should be like the the Gatorade,  
George Westbrook: Okay.  
Skye Capazorio: whatever.  
Brett StClair: No.  
Edwin Johnson: Yeah, we can name these.  
George Westbrook: What time  
Edwin Johnson: We can name each of these um territories and then you know so the gamecast is a page right you have your information c center's a page referral bank what whatever we're going to do and we're going to have to work tightly on that sky to make sure that these Irish guys get what they need and Brett and team get what they need and you and I get what we need is by the way Troy is  
Skye Capazorio: Yeah.  
Edwin Johnson: Cody on the  
Troy McDonald Kane: No, he couldn't make it. He has two very sick children at home right now,  
Kevin Murray: No.  
Troy McDonald Kane: unfortunately.  
Edwin Johnson: Okay.  
Troy McDonald Kane: Yeah.  
Edwin Johnson: Okay.  
Brett StClair: He's probably just  
Edwin Johnson: I hope they are not hung over from  
   
 

### 00:19:01

   
Troy McDonald Kane: No,  
Edwin Johnson: Vegas.  
Troy McDonald Kane: he came home to strep and something else with his kids.  
Brett StClair: as  
Troy McDonald Kane: So, he's managing his kids with his wife this morning.  
Edwin Johnson: Okay.  
Troy McDonald Kane: Yeah.  
Edwin Johnson: All right. What else do you have, Brett?  
George Westbrook: Okay.  
Brett StClair: uh do a quick review the global site. Uh Sky, thank you very much. You've given a s*** ton of review and  
Edwin Johnson: That was  
Skye Capazorio: Sorry. Well, sorry, not sorry.  
Edwin Johnson: great.  
Skye Capazorio: But I think I think it's just will be great.  
Brett StClair: um  
Skye Capazorio: George, I went in and I saw Max that you were already making changes. So, and then I messaged George to say, "Let me know when it's done so I don't go over on the changes that you're working." So, when it's done, I can go back in. Um, I think it probably works if I wake up like early in the morning, review, crack out those changes to you, then you've got the day to do it and then we carry on doing  
   
 

### 00:19:58

   
George Westbrook: Yeah. Um,  
Skye Capazorio: it.  
George Westbrook: I smell of something I was going to say. Yeah, that was it. We did kind of like a internal one um today as well where it's just like right that looks wrong, that looks wrong, that looks wrong, blah blah blah. Just in our opinion. Um, so there'll be some other changes that you might not have said, but it's just in terms of like spacing of some of the headers that was a bit inconsistent. Some were like that fast spaced, some were like that. So just making that consistent. Um, the good thing if we make a change and you're like, why did you change that? We can always go back. So  
Skye Capazorio: look good.  
Brett StClair: Um, on that note,  
Max Kingaby: P bake.  
Brett StClair: um, we managed to get the review stuff working on a PWA. If you guys do want to give it a test because we have had some login issues, it's the same email that you would have registered on the when we first fired them out.  
   
 

### 00:20:58

   
Brett StClair: And if you don't remember your password,  
Skye Capazorio: Thank you.  
Brett StClair: please let us know and George can do a password reset um for you guys. Um so Sky, your password should be working on the PWA. We hit a couple of problems on the web which I think George and team are looking at at the moment to get that to work.  
George Westbrook: That's done.  
Brett StClair: Is it done? Eh, so want to test the website review.  
George Westbrook: Yeah.  
Brett StClair: So at least when you guys are browsing, you'll see a little green little tab just kind of on the right hand  
George Westbrook: See if I can get it up.  
Brett StClair: side that that's the review. Um, and the first couple of times just getting it in and logged in and all that stuff can feel a bit messy and using it the first time because suddenly there's blocks everywhere and you've got to pick what you want to do. I tend to use the scribble. So, I pick the scribble and I circle it pops up.  
   
 

### 00:21:55

   
Brett StClair: says what I want and then if it if the button isn't showing, which there's a problem with on Android, but I think it's working fine on iOS, then you can just go submit and it forwards it to the queue and we're able to do the work on it. Um, and it's just we just kind of want to encourage you guys each time to remember when you're there, you're going to see something that just goes like winds you up. You want to do a slow walk through,  
George Westbrook: Yeah. So,  
Brett StClair: George?  
George Westbrook: on on every page there's going to be this little green little green thing here.  
Brett StClair: Just about  
George Westbrook: Click that. It will ask you to log in.  
Brett StClair: there.  
Edwin Johnson: Yep.  
George Westbrook: I think Will I do it here? Yeah. And then  
Brett StClair: And by the way, the PWA, you can open it from your browser if you want on your desktop. Um, to also test. There we  
George Westbrook: and then what it does is it takes a screenshot of the page.  
   
 

### 00:22:57

   
Brett StClair: go.  
George Westbrook: If there's a specific component you want to click on, you can click on it, add a comment, or like Brett was saying, if you want to draw, you can be like this. The logo needs a white background or shape. It's just the same as before. um and then add the note. Click submit and then it will go into the go into the admin panel and then we'll be able to see okay that's feedback one that's feedback  
Brett StClair: Do you want to reshare the admin panel for everyone just so that they've got it again? Because we were talking about that a couple of weeks ago.  
George Westbrook: Hey,  
Brett StClair: So, I just want to make sure you've got all the links. Um because once we get into the habit, you'll be able to see other people's comments and reviews. Um and it really is quite a productive way to work and spot stuff. You might see someone wanting to change something and you want to jump in and go, "Whoa, I actually quite like it." Folding under or not folding under.  
   
 

### 00:24:15

   
Brett StClair: Um, and just so that when you're kind of using the platform, when you're using the PWA or um, on the website, you're feeling comfortable. You can spot something and instead of going, s***, I must remember X, Y, and Zed. Can literally just log it right then and there. Um, okay. Awesome. Um, good session with the tZERO guys. Thank you. That was valuable. We're actually really enjoying those sessions. Um, they're pretty rockstar team to be honest. Um, so it's really really good to be able to get into the reads with a lot of the APIs and all that kind of stuff. So, we're working and progressing that. Uh, a goal that we need to hit is we've got to get some version of an app out which has um onboarding, referrals and a information stack which we will will be the kind of homepage so they can browse and consume um sports radar data. Um, we've got all the information. We've loading it into the vault.  
   
 

### 00:25:39

   
Brett StClair: Actually, that's on my task. Sorry, George. I need to finish that off. I've started it. It's on my machine. Unless you jumped in. I hope you didn't.  
George Westbrook: Nothing.  
Brett StClair: Um, I'm working through that. So, that'll be uploaded this evening. Um,  
George Westbrook: Nothing.  
Brett StClair: and that was for the referral and for the IPO. But the key thing for us is referral right now. The ability to on board and then we'll get the inplay stuff plugged in properly and I mean not in place or trade off. That's the kind of goal,  
George Westbrook: Yeah. Yeah. The main thing is persona.  
Brett StClair: right?  
George Westbrook: Just getting that sorted. Okay. So, you speak to tZERO about what they what they need for us. So, we've got a onboarded user. Once that's done, then it'll be the referral stuff in the background. The sports radar um stuff as well. Um, so yeah, it should be should when I say quite soon, not tomorrow, um, but in the next few  
   
 

### 00:26:43

   
Edwin Johnson: Okay, great. Do we have everything we need,  
George Westbrook: weeks.  
Edwin Johnson: Troy, for our persona?  
Troy McDonald Kane: We're It's back in our hands. I think it's in Bowler's hands. I'll check in today.  
Edwin Johnson: Okay, cool.  
Kevin Murray: Yep.  
Troy McDonald Kane: Yep.  
Edwin Johnson: Okay.  
Troy McDonald Kane: Kevin, do you know for sure?  
Edwin Johnson: Um,  
Troy McDonald Kane: Is it back in Bogler's hands?  
Kevin Murray: We got it back on Friday and it was sent straight to Matt.  
Edwin Johnson: okay.  
Kevin Murray: So,  
Edwin Johnson: Okay.  
Kevin Murray: he's got it now.  
Edwin Johnson: Thank you.  
Troy McDonald Kane: Yeah.  
Edwin Johnson: And George, if I haven't logged in ever for that editing yet, um, I can I can just do it, right? Can cool.  
George Westbrook: I'll send you login details now.  
Edwin Johnson: Troy, I'm having trouble with my desktop email, too. I don't know. I got bumped out of my password. Now I'm locked up. I don't know what the hell's going on. Yeah, I can't input any password into the desktop computer now.  
   
 

### 00:27:30

   
Edwin Johnson: It's killing  
Troy McDonald Kane: Yeah, there's something going on. I don't know what it is.  
Edwin Johnson: me.  
Troy McDonald Kane: We'll have to I'll have to I'll have to take a look at your systems. I don't know why it keeps defaulting.  
Kevin Murray: Yeah, might just need to do a hard reset, I think. Edin,  
Edwin Johnson: I did that.  
Kevin Murray: stop.  
Edwin Johnson: I did that. It's still Microsoft isn't allowing me to input any passwords.  
Kevin Murray: Okay.  
Edwin Johnson: And it it actually closed me out. Like I like I don't even know what  
Troy McDonald Kane: It's probably trying to send you an authenticator push notification and it's getting timed out is what's  
Edwin Johnson: happened.  
Troy McDonald Kane: happening.  
Edwin Johnson: Why would that happen though? I have the email up, you know. I've  
Troy McDonald Kane: You have two factor authentication. So any when you when you reset and you relog in,  
Edwin Johnson: never  
Troy McDonald Kane: it's going to need a reacuthentication to make sure that you are who you are.  
   
 

### 00:28:17

   
Troy McDonald Kane: It's for security purposes.  
Edwin Johnson: Sure.  
Troy McDonald Kane: People can't hack your account essentially. So you should be happy with that because people can't hack your account,  
Edwin Johnson: Yeah, but I haven't been able to to to communicate for  
Troy McDonald Kane: including yourself. You can't even hack your own account.  
Edwin Johnson: Right. All right. We'll figure this out. Um All right. Cool. Um and then is there any So what what's do we have a hard like deadline that we want to have the first app out actual for download for the referral?  
Brett StClair: I think we in the next week or  
Edwin Johnson: and A's the first.  
Troy McDonald Kane: Yes. Yeah. With the latest being by the 19th of June,  
Brett StClair: two.  
Edwin Johnson: Okay.  
Troy McDonald Kane: we want to have it at least a week before the Fourth of July holiday so that the referral program can go live that week.  
Edwin Johnson: I actually think we need it before that, Troy, because I think we had a referral bonus for Father's Day.  
   
 

### 00:29:05

   
Troy McDonald Kane: Uh we well we do but we haven't even published anything for the referral program yet so it's not  
Edwin Johnson: I know, but we're going to I mean,  
Troy McDonald Kane: public.  
Edwin Johnson: this just give everyone kind of like a reality check. You know, we're two and a half months and you know,  
Troy McDonald Kane: Yeah.  
Edwin Johnson: we're on a razor sharp line in terms of timing, not just for technology, for ad sales, all I mean, it's just I mean, we're all insane for trying to do it. So, let's hope we, you know, we got to make it work one way or the other. Cool. Um, does anyone need anything else from me at the moment? Awesome. All right, friends. Have a wonderful day and we'll see you guys on Wednesday, not tomorrow.  
Brett StClair: Good  
Edwin Johnson: Thank you. If you need anything,  
Brett StClair: luck.  
Edwin Johnson: Brett, let me know. I'll let you know um how that meeting goes this afternoon with the bank.  
Brett StClair: There you can  
   
 

### 00:29:56

   
Edwin Johnson: And then um like we'll get this the pricing done. Skype, maybe work with Brett a little bit. We'll all be on the same page so we can all um and to just for clarity,  
Skye Capazorio: Yeah.  
Edwin Johnson: Brett and team are going to help us with ad sales. Okay. So, we're gonna we're going to just tackle this on as a as a group.  
Kevin Murray: Perfect.  
Edwin Johnson: And uh Kevin, happy anniversary.  
Brett StClair: Perfect.  
Edwin Johnson: And I heard you're trying to get American Airlines to buy  
Kevin Murray: I am. Yeah.  
Skye Capazorio: Okay.  
Edwin Johnson: space.  
Kevin Murray: And thank you very much. 11 years she's put up with me. So, uh, I must be doing something  
Edwin Johnson: For the record, after being with you for a year and a half,  
Kevin Murray: right.  
Brett StClair: Oops.  
Edwin Johnson: she's a saint. All right,  
Kevin Murray: Cheers.  
Edwin Johnson: friends. Have a wonderful day. We'll talk all soon.  
Troy McDonald Kane: All right.  
Edwin Johnson: Thank you.  
Kevin Murray: All right.  
George Westbrook: Perfect.  
Kevin Murray: Thanks guys.  
George Westbrook: Let's f******  
Skye Capazorio: Thanks so much everyone.  
George Westbrook: go.  
Kevin Murray: Talking go.  
Troy McDonald Kane: All right.  
Kevin Murray: Let's go. That's it.  
   
 

### Transcription ended after 00:30:56

  

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.

**