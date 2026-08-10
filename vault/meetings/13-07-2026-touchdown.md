---
date: 2026-07-13
type: standup
scope:
  - "[[information-layer/sub-components/research-tab/research-tab]]"
  - "[[education/education]]"
  - "[[components/components]]"
status: extracted
extracted-to:
  - "[[information-layer/sub-components/research-tab/research-tab]]"
  - "[[information-layer/sub-components/research-tab/changelog]]"
  - "[[information-layer/sub-components/single-game-page/single-game-page]]"
  - "[[education/education]]"
  - "[[components/components]]"
  - "[[advertising/sub-components/programmatic-media-playbook/programmatic-media-playbook]]"
  - "[[architecture/open-questions]]"
description: "Transcript and analysis of the 2026-07-13 touchdown call — education videos cut under 2 min, house ads, Watch Mode conceived, Research Tab demo, Hard Rock"
---

## Post-Call Analysis

> Monday touchdown (44 min). Three product threads: **education content verdict** (too long — sub-2-min regeneration + Troy/Kevin content re-slice), **house-ads strategy + IAB learnings**, and the birth of **Watch Mode** (Edwin's one-screen Gamecast + probability + price + trade ask). Plus a live demo of the **Research Tab v1 pre-canned reports**. Commercially: the Hard Rock meeting landed very well (follow-up requested). Priorities restated: **trading + ads are the two non-negotiables**.

| Finding | Destination | Action |
|---------|-------------|--------|
| **Research Tab v1 demoed** — weekly pre-canned SR roll-ups, sortable columns, click-in definitions; ladder refined to 4 steps (pre-canned → custom → LLM outlier layer → AI agent); resourcing follows usage metrics; SR-probability × tZERO-price cross-correlation is the "no other platform" differentiator; Cody sending report ideas | [[information-layer/sub-components/research-tab/research-tab]] | Updated §1 + changelog |
| **Education verdict** — modules too long / too much scrolling / blank filler panels (Jared); all videos to be regenerated **under 2 min**; Troy found 5–7 refinement areas (performance-security script, concept ordering); Troy+Kevin re-slicing source docs → **3–4× module count** expected; Skye: let post-launch metrics drive further cuts | [[education/education]] | Updated §2 rules + §3 |
| **Short-form / AI-UGC content** — deferred until post-launch metrics; three production routes mapped (AI video, creator collabs, AI UGC avatars ~$2/video); doubles as social-channel content; social agency search running | [[education/education]] | Updated §3 (parked v2 note) |
| **House-ads strategy** — run house ads day one to avoid the no-ads→ads flip; "What is InPlay?" hype-video unit + referral link; education re-entry video ad (Cody, 15/30s video CPM); Gamecast/Pepsi replay ad approved as-is; IAB aspect-ratio scaling confirmed | [[components/components]] Advertising + [[advertising/sub-components/programmatic-media-playbook/programmatic-media-playbook]] | Updated |
| **Watch Mode conceived** — Edwin: win probability + Gamecast + share price + trade on one screen; George proposed landscape "watch mode" | [[information-layer/sub-components/single-game-page/single-game-page]] §9 | Captured (with 15/17-07) |
| **App Store** — Apple in review; Play Store next: research gambling-classification avoidance (Apple = 70–80% of users) | [[architecture/open-questions]] | Row updated |
| **Priorities restated** — trading (tZERO QA env end-to-end + load testing + simulation) and ads (SSP setup, in-app serving to IAB standards) are the two non-negotiables; market-making algo call Wed; Brett to redo proposal with real numbers Fri | Post-call analysis | Noted — no doc change |
| **Hard Rock meeting** — went very well (head of sportsbook + COO attended; Rafi Ashkenazi champion; more info requested + follow-up; Edwin/Troy/Brian building detailed business model); potential trajectory-changer | — | Parked — commercial |
| Action items: outreach offer/messaging/ICPs (Skye+George, email warm-up in progress); education revision docs (Troy/Kevin → George); Brett↔Edwin SSP-timeline session; Cody pre-canned report ideas | — | Action items — tracked in transcript |

**

Inplay - Touchdown - July 13
VIEW RECORDING - 44 mins (No highlights): https://fathom.video/share/SyK6Vj3YPVM_tM4dSFkSq9gZGPisLxys

---

0:00 - George Westbrook (Novosapien)
  We don't have to do another massive review with Apple. I think the next step is the Play Store one, which I think we're in the process of getting sorted now.  I suppose while we wait for them, I suppose one thing, Skye, is on setting up the, what's it called, the outreach side of things as well.
  ACTION ITEM: Draft outreach offer, messaging, ICPs/personas; send to agents - WATCH: https://fathom.video/share/SyK6Vj3YPVM_tM4dSFkSq9gZGPisLxys?timestamp=14.9999  just getting the emails still warmed up, it's annoying that we have to wait for that, but we'll get the emails going and then it's getting the offer, getting the messaging and the ICPs and buyer persona sorted as well.  So we'll get that done this week, have a stab at them, send them over, because there's a specific format that we've got to follow for the agents so that they've got enough information and for targeting and things like that.

0:57 - Skye Capazorio (InPlay Global)
  Sounds good, sounds all good. Trying to think where else, because all the websites, they're up and running, aren't they?

1:04 - George Westbrook (Novosapien)
  Have we got any more iterations we need to make on the websites? I don't think so at this stage.

1:11 - Skye Capazorio (InPlay Global)
  think Edwin, Cody, Troy wanted the focus to be on the app and resources going to finalising that before going into the website.

1:23 - George Westbrook (Novosapien)
  Yeah, because that was one of our plans this weekend was to get the outreach stuff going. But then we, I think obviously that meeting with the hardware, wanted to make sure that the ads were all in there because they're, so they follow the IAB format.  we're double checking some of our understanding on that because obviously if somebody has some creative, obviously we can't really manipulate the size of it.  But there's, because initially when we were doing it, I thought it had to be the exact pixel dimension. So let's say if it was like 320 by 50, it would have had to have been that.  It turns out you can. It You can scale them up as long as the aspect ratio is the same, which was good to hear, because otherwise it was like you just had these weird little ad units around the app.  I suppose it might be worth going through, doing another run through the app, getting some feedback, maybe specifically on the ad units as well, because I think some of the things that are still outstanding is the education videos, just making sure they're under two minutes as well.  So I think we'll rerun them, make sure they're under two minutes. I see your eyes going, Jared, is two minutes still too long?  In my opinion, yes.

2:51 - Jared Sapirman (InPlay Global)
  I have to deal with everybody else on their opinions on that. In my opinion, yes.

2:58 - George Westbrook (Novosapien)
  In my opinion,

3:00 - Jared Sapirman (InPlay Global)
  I mean, I've told this to Troy and everybody else, in my opinion, it's not, you didn't create the education modules, but they're too long.  There's way too much scrolling. I mean, for example, like, module 14, I think, they have a trading journal, okay, and there's three separate panels of blankness.  What is the point of that?

3:30 - George Westbrook (Novosapien)
  Oh, this. Okay, so that's just as a, that's, that is a... And that's supposed to be what, what you would, you would consider a trading journal.  But, like, what is the point of that?

3:44 - Jared Sapirman (InPlay Global)
  Hmm.

3:45 - George Westbrook (Novosapien)
  You know? Because, because how they were, effectively, what happened when we created them, is it was kind of like, right, let's take the, call it the, source of truth document, which had loads and loads of detail, which is, which is good.  Because, It gives us the substance to work with. So I can imagine what it's done is it's put this in.  So we can get that cut down. I think it's just basically in terms of text content videos, to be fair, it might just be worse with the videos, regenerating them at two minutes.  Because I appreciate what you're saying, like two minutes still does seem quite long. But I suppose it's balancing that.  Like, obviously, most courses, it's like, I can imagine if this was done as a course with accreditation, so they wouldn't be five-minute videos, they wouldn't be 10-minute videos.  But obviously, the people that we're targeting, it's, yeah. Completely not, yeah, it's a completely different audience.

4:43 - Jared Sapirman (InPlay Global)
  Well, it's not a different audience. The audience who is doing this are going through those same courses where they would have long videos.  But the purpose of this app is not, well, I don't think a user of this app is going to be interested in going through.  That in this setting, because they do it in other things. Okay.

5:08 - Skye Capazorio (InPlay Global)
  think also, just to add to that, I think that ultimately, whatever gets launched with, I think, as with all product-led growth and growth hacking in a startup, needs to be looked at purely through metrics once it's launched.  So I think, Jared, I'm not disagreeing with what you're saying in terms of an audience's consumption, but I also see Edwin's viewpoint in terms of it.  But ultimately, the proof of it, and the appetite for it, either way, will be proofed out in the utility of the app and the data metrics that get gathered from that.  And then the app needs to be smartly augmented to cater towards that, to make sure that it keeps on engineering the user journey to incentivize greater utility of the app.  Yeah.

6:01 - George Westbrook (Novosapien)
  So I think it's one of like that short form, that's, call it TikTok style, which I think you mentioned ages and ages ago, Skye.  I mean, that, that would be amazing. It's just, how would we, I'm trying to think, how would we do that?

6:14 - Skye Capazorio (InPlay Global)
  To add to that, that the intention behind that was that somebody would own the content generation of that. That was, that, I mean, for InPlay to do that cost-wise and to have like creators in a TikTok style actually doing stuff, I mean, that would cost a fortune, right?  To do at the scale of obviously the volume of content that exists. And so the intention was to give that ownership up to somebody, a sponsor, an artistizer, to own and cross-collaborate with us on the production of it, but something that they could brand essentially in that, in that space.  But obviously, given the fact that there hasn't been that, that, Appetite for Sponsorship at this stage doesn't mean that that won't happen further down the line.  think once we've got an audience, and when I mean an audience, I don't mean like a possible audience, I mean actual users on the thing, using that to go to advertisers and sponsors and then say, this is the audience that you're tapping into.  These are the users you are tapping into that are in our environment and then augmenting it from there and utilizing the data exactly as we've said.  Like if people, if, you know, 80%, 75% of our market, of the users are going through all the modules and doing them at the time that they exist now, great.  If there's drop-off that happens, you know, 30 seconds into the video, great. It proves exactly what Jared is saying and needs to be augmented from there.  If it's going to be used as something that drives, that drives something. This is— This It always needs to come back to the reason why.  Like, why is it there? The why today is because the platform is helping to educate people in a way that InPlay feels is, you know, relevant and informative and in-depth enough.  But if the market that comes to it goes, not really interested because I either know or I don't want to consume content like that, both of those will be proofed out in the utility of the app.  And I think we need to not over-engineer it at this point in time because it will change when it goes live based on those data points.

8:40 - George Westbrook (Novosapien)
  Because I think one thing in terms of the actual creation is these style of videos, I mean, even call it the AI influencer ones, they're not too bad to create.  So it's kind of like obviously doing a full education module production with less. Bank of America, maybe before it was, got to map it out, make sure that they know where the placements are going to be, the voice, blah, blah, blah.  For us, it's just, there's a script. We match the script up to, they call it AI-generated code in here.  So if we wanted to put, I won't play there. So like, throughout here, we can litter their logo or their creative throughout the actual video.  And then let's say one month, it's Bank of America. Next month, it is Amex. It's just a quick switch out, change the transcript, click regenerate, and then it's done, which I suppose is a product to an advertiser.  I mean, it takes that pain away for them.

9:48 - Skye Capazorio (InPlay Global)
  I think, I think in doing advertising placements, I think we're like, there's two different things here, right? One is coming at it from the angle that Jared, the that Jared is expressing is the the  content creator side of things, which is very, I mean, he's not wrong in the way that people, especially that, like that generational segment absorbs content and information.  Everything is five tips, three steps, 10 minutes to do this, to, you know, learn everything sort of thing. It's everything's in bite-sized chunks and very short format because attention spans because of those short formats have been made much shorter, right?  So, naturally, that is how that goes. think the way that you're talking, George, now seems to me to be more impressions-based, more advertiser placement versus advertiser content ownership.  And they both can exist. I don't think that it's one or the other, right? But I think, actually, the advertiser placement portion impression route will happen most likely through the SSP link and stuff before the sponsorship.  Side of Things Happens, to have a content creator backing it.

11:04 - George Westbrook (Novosapien)
  With these videos, we wouldn't be able to do that with the SSPs because what we'd have to do is, obviously, I know you know this guy, but it's obviously at the point at which the user clicks it, then it fills it in.  We'd have to generate this video way in advance of anybody clicking on it, and every single user that goes in would see the same placement because the, let's say, 10,000 users click, and we do 10,000 generations of a video at the point at which they click that, one, the time, and two, the cost.

11:40 - Skye Capazorio (InPlay Global)
  100%, but that's, so I think we're, so what I was saying in terms of the SSP, maybe SSP isn't the right example of it, but like a DSP plug-in and direct sales and direct offers would be where that exists in that space.  So, yes, I hear what you're saying. No, it doesn't have the ability to generate multiple. Multiple impression-based surveying that happens, but it could be a direct sale to Bank of America, for example, in this iteration where it isn't a content creator-owned piece, but they are still owning the piece as a direct sale.

12:16 - George Westbrook (Novosapien)
  Because I think in terms of that short form as well, I think that could be, because I think with this sort of stuff where it's module-based, I think that's where I always feel like, well, the short form, it's not going to work because obviously it's an algorithm.  That's not going to show it one by one, blah, blah, blah. So you're not getting that linear learning path.  But like the quick tips, quick tricks, that's, I think, definitely something we could do, be it in this format without a person, or going out to content creators, getting them to create it, then we have it in our platform.  Or the third option, which is, which a lot of people do, is the AI UGC. So you create an AI avatar.  It looks, feels, acts like a real human. pops up on the page, and it's one of those, like, you could pop out hundreds of them a day, and I think it's at the point where when we're in maybe a thousand of those videos, let's say a thousand at two dollars a pop, about 20, 30 second videos, that's enough content where somebody's scrolling through, because I can't imagine they're going to spend hours and hours on Zoom scrolling on the in-play short form content, but I mean, it's got the capacity that it could do that anyway.  The only real bottleneck is ideas for the content, which AI can obviously help with as well.

13:34 - Skye Capazorio (InPlay Global)
  Yeah, I hear you. I think the thing is, behind that is also being able to utilize short form content to actually utilize that on the social channels as a content viewer within that space too.  So, not necessarily going through absolutely every module of learning, but using it as a snippet that is either AI UGC created or content creator collaboration created.  created that then lives on that space as a 30-second snippet or a 15-second snippet that then uses a viral hook to drive, uses that as a viral hook to drive people back into the app as an ongoing content.  Because ultimately, the social channels, now that there is a product, needs to be an ongoing content generation of all the things and all the features that live within that space, which I know Troy, think, Jared, I don't know if you are part of it, Troy and Kevin and Cody and stuff are looking for a social agency.  And I think, you know, I think, sure that they would, I'd be concerned, put it that way, if they didn't put forward doing all of that sort of stuff in that very micro absorption content, you know, it could be like Tips Tuesday or Tips Thursday or Yeah.  Friday or whatever the story is and it becomes part of a content series that feeds the actual TikTok, Instagram channels and YouTube even at a later stage.  100% that is absolutely needed and I'm sure and I hope that whoever the agency that is chosen within that would then go ahead, they would put that forward.

15:22 - George Westbrook (Novosapien)
  I suppose it might be worth talking to this, we need to think about as well as the agency potentially using that content workforce thing that we showed you because we're still in the development, obviously the TikTok and the Instagram stuff, but then it's obviously integrating in the video aspect as well.  So it's not just static images or infographics or parasails and things like that, like actual videos. for that, those AI influencer ones, yeah, there could be a place for that.  Absolutely.

15:54 - Skye Capazorio (InPlay Global)
  How was the Hard Rock meeting?

15:57 - George Westbrook (Novosapien)
  I see you guys are in now.

16:00 - Kevin Murray (InPlay Global)
  Yeah, it went very well. Edwin, you're on mute. Edwin, you're on mute.

16:15 - edwin
  Okay. Hi, George. Thank you very much for the weekend's deliveries. Brett, thank you, thank you, thank you. I don't know.  What do you guys think of that meeting? I thought it went really well. Obviously, they are continually engaged.

16:31 - Cody Haugen (InPlay Global)
  They want to see more information, which is always good, right? They're not ready to cut us off or say, we're done with this.  We demoed both apps. The second one, for whatever reason, my computer was running sluggishly slow, so I don't know what that was about, but I haven't closed all my other apps, but here we are.  Was that the PWA one or the pre-release? No, no, no, The IPL I did for my phone, so hopefully that was good.  Edwin, Kevin, Troy, that demoed well. Great. I thought you did fantastic.

17:06 - edwin
  And the F looks great, okay? I mean, it really, really looks great.

17:12 - Cody Haugen (InPlay Global)
  It's not a tough product to sell, which goes back to, once again, the Novo guys and how, what a great job you guys have done in such a short amount of Amazing.

17:23 - edwin
  And the weekend stuff, know, like getting that over to us over the weekend, you know, I know it's a pain in the , but it really is helpful when we have an 8 a.m.  meeting on Monday. You know, the thing is, this particular company, I mean, it could change the trajectory for us and Novo.  We work together, things like that, because they have, they, I mean, they're doing really well on sports betting side.  So, I think they're number four, Cody, right now. Yes, they are.

17:52 - Cody Haugen (InPlay Global)
  And I'd say they, because of their global ambitions, I think they could easily. They pass FanDuel and DraftKings in pretty short order.  They also have, not to mention, they also have all of Florida, and they're the only casino allowed in Florida right now.  Oh, really? Yeah.

18:13 - George Westbrook (Novosapien)
  I thought Florida would be rife with gambling. I thought it be everyone there.

18:18 - Cody Haugen (InPlay Global)
  They did an inclusive deal with the Seminole Tribe, and so no other sportsbook is allowed to be in Florida outside of Hard Rock.

18:27 - edwin
  Like, many years ago, the states, some states sold the gambling rights to the, or gifted the gambling rights to the Indian tribes for taking their land.  Oh, I think of all places where I learned that, I think it was South Park.

18:47 - Kevin Murray (InPlay Global)
  They gave us some liquor in the gambling rights, and it's like, .

18:51 - edwin
  Yeah, so in my neighborhood where I grew up, there was a bunch of guys from Chicago who actually were, you know, they were extorting.  Ring Con in San Diego, Indian Casino Reservation, and a bunch of guys from my neighborhood had to go to prison for it, you know, different day and age.  And here we are talking to, yeah, man, life's definitely a trip. But yeah, I thought it was an absolute home run meeting.  We had two new guys on, the head of the sports book, and then the chief operating officer for Hard Rock.  And then we, you know, obviously our big proponent in there is Rafi Ashkenazi, who's the executive co-chairman, I think, of that.  And he's, I mean, you could tell he's really excited, right? I mean, of all of them, even Edward got a little bit warmed up, you know, because those Aussies are, you know, they're tough to deal with, too.  Wait, did you say Aussies?

19:53 - George Westbrook (Novosapien)
  Aussies, yeah, he's Aussie. They're usually, they're usually, they're usually alright, the Aussies. I think they're like British people, just a bit more pissed all the time.  Yeah, mean, they're very short, like, their attention span's short.

20:10 - edwin
  Maybe it's from all the spiders and  like that. Yeah, just constantly like that, just looking around.

20:17 - George Westbrook (Novosapien)
  Looking around for a creepy crawly.
  ACTION ITEM: Schedule working session w/ Troy + Brian re: Hard Rock business model - WATCH: https://fathom.video/share/SyK6Vj3YPVM_tM4dSFkSq9gZGPisLxys?timestamp=1227.9999

20:24 - Cody Haugen (InPlay Global)
  Yeah, they asked for a bunch more information and want another follow-up after they digest. So, once again, it's always good when they're still interested and want more information.  So, they're not done with us.

20:38 - edwin
  Troy, we've got, so tomorrow, I'll sit with you and Brian. Maybe we can get Brian on there, that we can have him work out the business model in greater detail so I don't have to do it again.  Okay.

20:52 - Troy McDonald Kane
  Cool. What do you think of the meeting?

20:55 - edwin
  No, I thought it went well.

20:56 - Troy McDonald Kane
  Well, fact that any time a meeting goes over time, I know. Everyone's in a rush to get off. That's always a good sign, you know, where they were wanting to see more of the app.  They were had a lot of great questions. You know, I think that that Mike, I was the only one that's like, wait, what are you building here?  Like, that was the only thing that kind of, you know, was a little odd. But yeah, well, he probably didn't know what else going on.

21:22 - edwin
  No one actually caught him up. Well, that's what I'm saying.

21:25 - Troy McDonald Kane
  Like, why wasn't he caught up if he was on the call? That was it. Yeah. You know how the big dicks are.  They don't do any work.

21:31 - edwin
  They just show up. Yeah. Just show up.

21:34 - George Westbrook (Novosapien)
  And then everyone looks up their LinkedIn before and then, oh, , this guy's in the meeting.

21:38 - Troy McDonald Kane
  Yeah. That's right. We call that in my town, the Brett Sinclair.

21:46 - George Westbrook (Novosapien)
  Unfortunately, he's not on the call. So we can, we can chat about it now. The thing is, daughter's graduation is literally at, exactly at this time.  Oh, cool. Congratulations.

21:58 - edwin
  Yeah. So he's, he's an ex. I thought he had to go to Ibiza and find Max Kingaby.

22:06 - George Westbrook (Novosapien)
  Max wandered in this morning, just like, no one talk to me, I'm a broken man. Did he say it with his eyes or his lips?

22:18 - edwin
  Max was trying to find Max in Ibiza, to be honest.

22:22 - Max Kingaby
  Did you have a good time, Max?

22:25 - edwin
  Very, very, very, very, very good.

22:29 - Max Kingaby
  Wow, that smile just won't go away.

22:32 - George Westbrook (Novosapien)
  It came back, the first thing you said was, right, does anyone want to go in September?

22:37 - edwin
  Yes, I mean, the fact that Max was at Ibiza, like, going crazy, and I was at Walt Disney World, just, like, it's just not fair.  I should have been at it. But it's 19 pounds a flight.

22:53 - Max Kingaby
  I'm like, they're basically forcing me to go. Jesus Christ, what'd you fly on? EasyJet, it's just a low-cost line in the UK.  It's 19 pounds to fly. Yeah.

23:07 - edwin
  Holy . Exactly.

23:12 - Max Kingaby
  It costs me more than that if I want to go and see my parents at the weekend. My train ticket to work each day costs more.  Wow. I 20 pounds 60p to get to work every day. Really? Yeah. It puts a flight to Ibiza. Okay.  Well, easy to move.

23:29 - edwin
  All right, who's running this show? We're late, so apologies for that.

23:34 - George Westbrook (Novosapien)
  So one of the things we, or the things we were going over before was, so obviously apps in the app store, currently still in review, so hopefully we'll hear something next day or two.  We've obviously done many reviews ourselves, so very hopeful that it's going to get approved. So when we get that back, that'll be good.  The play store one, getting that. Finalized as well, get that sent off, but it's obviously Apple was more important.
  ACTION ITEM: Research Play Store gambling policy; prep submission to avoid gambling classification - WATCH: https://fathom.video/share/SyK6Vj3YPVM_tM4dSFkSq9gZGPisLxys?timestamp=1441.9999  can imagine like 70, 80% of users are all going to be on Apple. So I let's get that one bulletproof.  I think the Play Store, I think it's a bit more strict. So there's a bit more research we've got to go into to just make sure, especially with something, obviously we know it's not a gambling product, but it's just making sure that they know that.  And making sure that we don't, because I think it's as soon as they bucket it in with gambling, the amount of checks that go into it are much greater.  So just making sure that we avoid that. Then I suppose we spoke about the education aspect. So we're going to regenerate all of the videos so that they're under two minutes.  And then maybe rework some of the content, like I think one on this one, there's like these four trading journal things, which is, I think, like Jared said.  It's just a completely empty space. At most, it needs one of them. People are just going to be driven off of it.  The content will keep the same for the time being, so that when the reviews come back, then we'll iterate on the actual content, but we'll build the videos off of the, call it the source documents that we got sent over, which are really good because they're comprehensive.  Ben spoke about potentials of short-form content, but I think that'll be later down the line and how we could utilize AI to create it and come up with the ideas.  But I think for version one, have this here, see what the appetite's like, get the metrics. If it's not doing too well, mix it up.  If it's doing well, maybe double down and still add the short-form stuff, but at least there's the education capability in there.
  ACTION ITEM: Revise education modules; send to George; then George regenerates videos <2 min - WATCH: https://fathom.video/share/SyK6Vj3YPVM_tM4dSFkSq9gZGPisLxys?timestamp=1550.9999  And then I suppose...
  ACTION ITEM: Revise education modules; send to George; then George regenerates videos <2 min - WATCH: https://fathom.video/share/SyK6Vj3YPVM_tM4dSFkSq9gZGPisLxys?timestamp=1550.9999

25:59 - Troy McDonald Kane
  George. Real quick, George, real quick. On the education stuff, can you just give us today, because Kevin and I are going to sit down today.  I spent a lot of time on the education stuff this weekend. I must have watched those modules at least two or three times each.  And Jared watched them as well. And even Jared, what he was getting and I was getting were not even synced up.  And I know you're refining all that. But what I really took a lot of time to do this weekend is go through the content itself, not the videos.  And there are at least that I could find five to seven different areas that I think needs a little bit more refinement.  And then we do want to think about how to break it up more into smaller modules. So before you even do all that work, give us today to kind of work through it.  And then we'll come back to you with revised documents that you can use. I want to slice them up.  I want to create like there's probably going to be three or four X of the modules now because we're going to break up them in more subtopics.  And that's what I was trying to kind of outline. Okay, perfect. Yeah, because it was all this was, was like throwing something at the wall and seeing what sticks, not being refined at all.

27:10 - George Westbrook (Novosapien)
  So yeah, we'll wait till we got that and then we'll start on the refinements. Okay, yeah.

27:16 - Troy McDonald Kane
  mean, it's hopefully make it a lot easier when you do all that work and then we don't have to go back and iterate too many more times.  And I, you know, would like to take the opportunity to, because there's a couple areas where, you know, we've refined how we're our articulating certain concepts, especially on the performance security script, like that one will probably adjust again.  But even as you go through the modules, there's topics that get introduced in earlier modules that probably are in later modules that need to be explained in earlier modules because they give reference, like, so that's what I need to work with Kevin on today.  Okay.

27:54 - George Westbrook (Novosapien)
  For the next thing, the ad units as well. So Bye. So these, I think I mentioned an email, these are the IAB format.  So what we'll get when we plug into the SSP is these are the formats that this provider can serve.  They need to be in this aspect ratio and they need to look like this. So here's a, here's a, this, you won't be able to see this on the, um, test flight version.  Um, but there are more formats than this. Um, so it's just working out what do we want to show on the, call it the house ads.  Um, is what we've got at the moment sufficient? If not, what do we need to change? Maybe is it different units, different creative things like that?  Um, but I think it'd be definitely good when we, when the apps in the app store that we've got the, because I think we mentioned it last week that if we did what we did before, which was no ad units at all, be it house or the programmatic ones, when it gets to the point where we, we turn on ads.  And then the user experience has suddenly gone from no ads to now here's these loads of ads from random companies.  That might be a difficult transition. It might diminish it a bit. Whereas obviously if we've got house ads, they're still going to perceive them as ads.
  ACTION ITEM: Implement house ad: 'What is InPlay?' video unit; add referral link - WATCH: https://fathom.video/share/SyK6Vj3YPVM_tM4dSFkSq9gZGPisLxys?timestamp=1760.9999  It's just it's going to flip from obviously InPlay to Coca-Cola or Cash App or something like that. So I suppose it's any feedback on the current ad units that we've got.  So I mean, I love it.

29:31 - edwin
  The one thing I'd like is if possible, similar to how we have it on the trading app, if there was a way to click and see a video of InPlay or something, you know what I mean?  It's just so we can show that that video. Yeah. Is there? Yeah. OK, yeah, that's good. That's a good idea.

29:49 - George Westbrook (Novosapien)
  Maybe we could do for all of them or for some of them. Just I would say even one or two.  They don't have to be a lot.

29:58 - edwin
  Just so that we can show. That it exists. Okay. Yeah. not even existing. You know what I mean? Maybe the leaderboard one.  do leaderboard.

30:08 - George Westbrook (Novosapien)
  Leaderboard opens a splash page where they can see the video, click through, blah, blah, blah. And then we can do like a referral link in there as well.

30:17 - edwin
  No, what I mean to say is like on this particular page, like right there, you know how we said watch video for more content, right?  And you're in that referral bonus. It could be just something like this one, George. It doesn't even have to be a big deal.  Just how we had that separate page on the initial, you know what I mean, right? Yeah. Yeah. Yeah. You click, you go to the other page, you see the video, and then you can click off.

30:41 - George Westbrook (Novosapien)
  That's right.

30:41 - edwin
  And I would actually, like, I would say we should, and maybe we put in the, like the in-play video that Sky had.  The hype video, think, George, you guys have already from the website because it went up there.

30:54 - Skye Capazorio (InPlay Global)
  But if you need it again, just shout.

30:56 - George Westbrook (Novosapien)
  Okay, perfect. Yeah, maybe we could have another ad unit. What is InPlay? And then they can click on it and then it shows that video rather than it being like view leadable, then they click on some random video.
  ACTION ITEM: Evaluate education-module video ad on re-entry; propose approach to Cody - WATCH: https://fathom.video/share/SyK6Vj3YPVM_tM4dSFkSq9gZGPisLxys?timestamp=1864.9999

31:08 - edwin
  I wouldn't make it too difficult. I mean, you already have most of the parts. Yeah.

31:15 - Cody Haugen (InPlay Global)
  George, the other piece, thinking about raising that CPM or diversifying that CPM, are we still going to add potentially a video ad in the education module so that we can get, uh, you just made me think about it when you showed the inventory of ad units.  Um, let me have a think.

31:37 - George Westbrook (Novosapien)
  I mean, I can't, I can't see why we, we can't, I just need to, I just need to have a look.  Um, it doesn't have to be every module.

31:45 - Cody Haugen (InPlay Global)
  It could be every time you re-enter the education section, you just get one video, then you're in there. As long as you stay within the education module, you're not getting bombarded with more ads.  Yeah. It's just, if you leave that, go. trade, go back into the education module, it re-triggers a 15 or 30 second video, and that way we're able to get the video CPM, which is obviously much higher than any sort of display ads.

32:14 - George Westbrook (Novosapien)
  Okay, yeah, obviously you can get something like that.

32:17 - edwin
  I have a question, George, on the Gamecast ad, that Pepsi, is there, so I  love this, okay. When I was going through, and Cody gave a great demo of going back, so you look at a previous game, and you have all these listed, right, all these big plays, , is that cool.  Do we like the size of that and the orientation of that ad? I do. You do?

32:54 - Cody Haugen (InPlay Global)
  Yeah, I think it makes you focus, it's obviously right there in your face. But it's gone so fast anyways, I don't think it disrupts anything.  Yeah, I agree. Yeah, I agree as well.

33:10 - edwin
  Perfect. And we don't touch it. Because this, like, it's really cool. Now, George, when we were going down, there was a probability.  Where the heck was it? You got to click game. There you go. There you go. So, George, what I want to do is that game probability chart.
  ACTION ITEM: Design landscape 'Watch Mode' (Gamecast+Probability+Share price+Trade); then link market/probability data - WATCH: https://fathom.video/share/SyK6Vj3YPVM_tM4dSFkSq9gZGPisLxys?timestamp=2007.9999  I think we want to make that a little, well, strike that. I want you guys to think about this.  So, basically, I want to be able to, on one full screen, see the win probability, the game cast, and the share price of in-place of that particular team that you're watching.  Okay? So, basically, yeah. So, I want it to be, you know, where I could see the game, see the win probability.  And the share price all in one look-see. Because if I'm trading it, right, and let's say hypothetically, I click on, you know, something that happened in the second quarter, and I see the probability change, like click there, right, field goal happened, perfect.  Now the probability change, I'm going to want to look at what happened to the share price and the probability and the game cast.

34:25 - George Westbrook (Novosapien)
  So maybe what we have is a, let's call it like a watch, a watch mode, basically a mode where, because the issue, obviously, that is a lot of content to show on a screen.  It is. And what is somebody going to want to do? So ideally, they're going to want, so maybe it's, they go watch mode, they have to rotate their phone, so it's portrait, landscape instead of portrait.  The left-hand side is maybe fixed with the game cast, and then there's buttons to go through like this, and then on the right-hand side,  side. I can't rotate this, but there's- I'm with you.

35:04 - edwin
  You have a probability and then the stock chart with the ability to trade right from there, right? yeah. Is that doable?  Everything's doable.

35:17 - George Westbrook (Novosapien)
  It's just, I know that's like a  answer. But it's, yeah, what we'll do, we'll do, I don't think it'd be too much.  The only issue we'll have at the moment, because obviously this is, it's connected up to the trading. But it's not refined.  So that'll be the next step after this is going to be, obviously all this market data is, I mean, it's there, but there's, well, the components are there, but there's no data.  So once we've got the data, because whereas before what we had was, it was just completely fake data. So it looked and filled exactly like it was, but now we need to make sure that everything's mapped up.  So that that Like when they're at this moment in time, we can look back, what was the, what was the price for this team and this team?  What was the probability at this point in time? And then obviously checking what we have from Sports Radar at that point in time for this event, what was the probability linking it up?  Because that's where, which I suppose is one of the next points is the research module. That's where it's going to get ultra powerful.  Because at the moment, I think I might as well go to that. It's just taking a stab at some of the, is this going to load?  I don't know if the API's linked up. That's just basically doing a roll up of the, of some of the Sports Radar data.  But obviously we haven't got the, the prices linked into it. So it's, once we've got that, then these reports are going to be, right, this team in the fourth quarter when they're losing, this is the likelihood that they're going to win.  And given that team at that point in time, the price. That's usually fluctuates X amount in the last quarter, something like that, which obviously, like we said, no other platform, app, or software does that on the planet.

37:14 - edwin
  Exactly. I mean, every day it's more fun to have these calls because it really is awesome. I mean, yeah, you're doing a fantastic job.  So one thing's worth talking about is where we see the priorities.

37:33 - George Westbrook (Novosapien)
  Two big, two massive ones are trading and ads. So what we need to integrate, obviously, get all the, depending on what happens, the SSP stuff set up, but regardless, we need to make sure that the ability to serve is within the app, just making sure they're right locations, that we're making sure that we're sticking to the AIB standards, not just in ad formats, but the way that it's served and things like that.  And then the second one is trading. So on the call with T-Zero on Friday, yeah, it was Friday, just prepare and make sure that everything on the QA environment is running smoothly end-to-end, do lots of load testing so it's not like, oh, we've done five requests and they worked, let's go push this into production.  Making sure that it's battle-hardened, things scale up correctly, scale down correctly as well, so that we're not burning cash.  And then, like we said, get some sort of simulation going. And then once we've got that data set as well from those tests, then we can pipe in the real fake data into the app.  And then, obviously, given the trading, then there's the research module as well. I think the one other big thing is the market making algorithm, which I think we've got that call booked in on Wednesday.  Which would be good to go through.

39:05 - edwin
  Okay. Anything else? I think that's everything, unless anybody else has got anything.

39:13 - George Westbrook (Novosapien)
  So you just teased me with my research section, but you can't click into anything? Oh, wait, wait, wait. No, no, no.  These reports are just kind of random. The UI, I don't think it looks very good. But we're obviously limited by the fact that it's a phone screen.  mean, obviously these columns, so some of the issues with the columns, obviously, if this was all expanded out, it's going to be like the full width of this.  So it's just you click in, you can see what the columns mean. You can sort it by whatever you want.  Regression watch. So I suppose it's... So I suppose it's... If you could brainstorm some ideas for what research reports you want, because obviously this is like version one, which is pre-canned reports that are done on a weekly basis, let's just say, that maybe everyone can see or it's gated for some people.  Next step is the custom reports that a user can create, but still effectively like database roll-ups. And then the third layer is, which adds on to both of these two, is integrating like LLMs into it as well.  So it's not just, here you go, Mr. User or Mrs. User, have a look at this data. It's right, now the AI's analysed it and said, oh, this is an outlier, this is an outlier.  I've also noticed on this research report, blah, blah, blah, And then the step after that is AI Agent, which has got access to all these reports, all of the users.  They can ask questions and create reports from there. Obviously, varying degrees of technical complexity. And I suppose it's one of those things that, given the metrics from usage, that's where we pour the resources.
  ACTION ITEM: Share pre-canned research report ideas w/ George - WATCH: https://fathom.video/share/SyK6Vj3YPVM_tM4dSFkSq9gZGPisLxys?timestamp=2470.9999  But at least we've got a wide net to catch people. Yeah. No, I mean, this is already looking.

41:21 - Cody Haugen (InPlay Global)
  I think the functionality of it is great. Being able to filter on those columns, move that around. I will share with you some other sort of pre-canned reports that I've already given some thought to as well.  And then we can build and kind of brainstorm off of that as well. Yeah. Okay, perfect.

41:45 - George Westbrook (Novosapien)
  Who's going to say it? Nice work. It's time for Sky to say it.

41:52 - edwin
  Let's  go. Let's  go.

41:55 - George Westbrook (Novosapien)
  Finally.

42:00 - edwin
  Participate in it.

42:01 - Skye Capazorio (InPlay Global)
  When other people say it, I do participate in it. I'm just usually on mute. Oh, good to know.

42:07 - edwin
  George, so then my takeaway is I'm going to finish up the Market Maker stuff in anticipation of Wednesday, and then the SSP stuff.  We've got to figure out how long that's going to take. Yeah, yeah. We need that quickly.
  ACTION ITEM: Schedule working session w/ Brett re: SSP integration timeline - WATCH: https://fathom.video/share/SyK6Vj3YPVM_tM4dSFkSq9gZGPisLxys?timestamp=2544.9999

42:24 - George Westbrook (Novosapien)
  Yeah, that's more of Brett's remit in all honesty. It's probably better if it comes from him, because I'd probably make loads of mistakes on it.  So it's, yeah, maybe it's worth you and Brett having a sit down, having a chat around the SSP stuff.  But regardless of what happens on that front, obviously, we know that we need to have the ability to serve that.  It's just a matter of, obviously, which SSPs are we going to be using and how do we integrate. And yeah, making sure that we're getting as much money as possible.  Yeah, and when it's Friday, Brett's going to redo his proposal.

43:09 - Cody Haugen (InPlay Global)
  That proposal in the playbook that he sent over to us was like kind of quick back of a napkin math.  So he said on Friday, he's going to review that and send that to us to get actual numbers. And then I believe on Wednesday, he said he was going to share kind of an update on that front on Friday to us.  So, yeah, that was from Friday just because you weren't on that one. Yes. Okay, cool. All right. Well, if anyone needs anything, please reach out.

43:38 - edwin
  Otherwise, in play team, we got 10 minutes. We'll talk then. And, you know, thanks so much, team Novo. Fucker.  Yeah. Great job, guys.

43:50 - George Westbrook (Novosapien)
  Thanks for the help over the weekend, too. Appreciate it. No worries. Huge deal, George.

43:54 - edwin
  Thank you. Perfect. Let's  go. See you guys. Thanks, man. Bye-bye.