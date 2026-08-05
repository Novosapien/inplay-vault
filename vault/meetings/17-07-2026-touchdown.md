---
date: 2026-07-17
type: standup
scope:
  - "[[information-layer/sub-components/single-game-page/single-game-page]]"
  - "[[components/components]]"
  - "[[architecture/open-questions]]"
status: extracted
extracted-to:
  - "[[information-layer/sub-components/single-game-page/single-game-page]]"
  - "[[information-layer/sub-components/single-game-page/changelog]]"
  - "[[ipo-module/ipo-module]]"
  - "[[earnings-report/sub-components/off-field-earnings-engine/off-field-earnings-engine]]"
  - "[[education/education]]"
  - "[[components/components]]"
  - "[[advertising/sub-components/programmatic-media-playbook/programmatic-media-playbook]]"
  - "[[architecture/open-questions]]"
description: "Transcript of the 2026-07-17 InPlay touchdown — AppLovin MAX as ad server, Kevel on hold, Edwin's market-maker reference-price mechanics, and Watch Mode fixes"
---

## Post-Call Analysis

> Friday touchdown (48 min). Two decision-heavy threads: **ad serving** (AppLovin MAX confirmed as ad server, Kevel on hold, Google's 30s minimum refresh kills the 15s rotation plan, watch-screen targets ~720 impressions/game, $50k–250k direct pilot construct) and the **market-maker mechanics finally revealed** (reference price = today's-game probability + season-long probability price + off-field projection, quoted around with randomization; deep-dive moved to Mon 20-07). Watch Mode iterated (slider killed, P&L on-screen, trade sheet swipes both teams). Education's 16 sub-2-min modules shipped. Cadence: Tue/Thu tZERO standups added — daily standups until launch. Timeline anchor: trading opens Aug 29; Edwin commits $1M Aug + $2M Sept marketing, +$1–2M prize money.

| Finding | Destination | Action |
|---------|-------------|--------|
| **Market-maker mechanics** — reference price = blend(today's-game probability price, per-game win probabilities over remaining games × $5) + off-field projection (Cowboys ≈$30 vs Carolina ≈$14); bid-below/ask-above with randomization factor (no machine-pattern 500-lots); load-balancing + market-making as two algos; Edwin writing layman narrative; Novo insists on understanding before building; deep-dive Mon 20-07 | [[architecture/open-questions]] | MM rows updated |
| **Ad-server decision** — AppLovin MAX as ad server + SSP adapters; Kevel formally on hold until first direct deal (1–2 wk setup; "holding pattern, not blow-off"); MAX cost comes off ad-serving fees (no upfront budget) | [[components/components]] Advertising + [[advertising/sub-components/programmatic-media-playbook/programmatic-media-playbook]] | Updated |
| **Ad-load rules** — Google 30s minimum refresh kills 15s plan; Edwin target ~720 impressions/game on watch screen; field-overlay transparent logo + 30s stoppage-only videos in field outline; trading-page CTR expected low (clicks at halftime/other pages); $50k–250k 2–4-wk pilot with earn-out guarantee; first 2 weeks maybe 90% ad-revenue distribution to users (vs 65%) | Same as above | Updated |
| **Watch Mode iteration** — slider killed (OS-gesture conflict), click-through stays; net position + per-game P&L + global P&L on-screen; trade sheet must swipe both teams; expandable event cards = direct-sale ad space; landscape trade layout redesign | [[information-layer/sub-components/single-game-page/single-game-page]] §9 | Updated |
| **Education shipped** — 16 updated modules live, all videos under 2 min; next review pass + Troy/Kevin revised docs pending | [[education/education]] | Noted in §2 |
| **Timeline** — secondary trading opens Aug 29 post-IPO (pre-season dead zone UX needs thought); ~10k users targeted at IPO launch | [[ipo-module/ipo-module]] | Business rules updated |
| **Process** — Tue/Thu tZERO standups added at 4pm London (daily standups to launch); interns Cam + Claybornne alpha-testing page-by-page; dual TestFlight builds planned (IPO + trading); tZERO visibility via Chris's platform | Post-call analysis | Noted — no doc change |
| **Marketing commitment** — Edwin: $1M Aug + $2M Sept user acquisition, +$1–2M prize money; break-even on season one = win if acquisition funnel clicks; NBA challenge late Oct | — | Parked — commercial |
| Futures API (Cody's) — win-probability endpoint returns unauthorized on trial tier; escalating via Scott/support | Post-call analysis | Action item |

**

Jul 17, 2026

## Inplay - App - Touchdown - Transcript

### 00:00:15

  

Jared Sapirman: All

Cody Haugen: Hello.

Brett StClair: I know there might be the gravel one.

Edwin Johnson: Hey

Cody Haugen: Hello.

Brett StClair: Uh Troy,

Jared Sapirman: right.

Edwin Johnson: y'all.

Brett StClair: I tend to ask some of the sillier questions because sometimes we look at the files and connections and we're like, "What are we posting? We can't see the whole stitching together." And then we're like,

Troy McDonald Kane: Yeah, they're not they're not silly or there's no wrong questions,

Brett StClair: "s***.

Troy McDonald Kane: bad questions, dumb questions because you guys are learning trading alongside, you know, uh, building out this app. So, I I I could tell by the question what you guys were were trying to lean on. So, that's why I wanted to explain. We just got off with the Novo,

Brett StClair: Did

Troy McDonald Kane: I'm sorry, with the TZ tech team um going through some of the next iterations of

Brett StClair: I?

Troy McDonald Kane: the uh development for the app for trading. Yeah.

Edwin Johnson: Great.

Troy McDonald Kane: And I know um George and Hassan will be on shortly.

  
  

### 00:01:10

  

Jared Sapirman: Great.

Troy McDonald Kane: They had to do one more setup with uh tZERO and then they'll be on.

Edwin Johnson: All right, cool.

Troy McDonald Kane: Um while we're waiting for them, Brett, I do after that call. What I would like to recommend going forward until we launch is right now we have our Monday, Wednesday, Friday standups. I'm going to recommend that we do Tuesday, Thursdays as tZERO standups. So then every other day we're we have a standup.

Brett StClair: Doing the same

Troy McDonald Kane: Yeah. Okay. Uh, and then does 4 uh 400 p.m. London time work for you guys because that's the time we have on the books now with them. So, they don't have to move their calendars around, but we already have a standing meeting at that time.

Brett StClair: Yeah, that's perfect.

Troy McDonald Kane: Okay.

Brett StClair: Tuesday.

Troy McDonald Kane: Then I'll just have evangelists add you four to those meetings going forward and anyone else on this call

Brett StClair: Yeah.

Troy McDonald Kane: that needs to be part of it.

  
  

### 00:02:06

  

Brett StClair: Yeah, I think that works.

Troy McDonald Kane: Great. All right.

Brett StClair: Um yeah, just this is where all the focus is right that we get the

Troy McDonald Kane: Yep.

Brett StClair: trading components up and running. But there's just so many it's like individual file calls individual and so

Troy McDonald Kane: Down.

Brett StClair: we were like s*** we're not seeing in this file call the response that we're expecting to come back and then it's oh no it's in another set of APIs or another process and we okay let's have a look at that one no it's not there and yeah and then we started thinking about the market maker stuff and we're like h so will the order book how does We can't picture the market maker structure technically.

Troy McDonald Kane: Yeah. Well, we haven't done the market maker yet.

Brett StClair: So I think what you explained was actually really helpful for us because we're its own API and

Troy McDonald Kane: Yeah. Yeah.

Brett StClair: Oh, there we

Troy McDonald Kane: Yeah, we'll uh Monday we'll go through all of that finally,

  
  

### 00:02:59

  

Brett StClair: go.

Troy McDonald Kane: but uh at least you guys are are moving along as much as you can. So, we're they were at the main question when was just how the how the market maker is going to interact with uh the trading competition. So, I went through that and how the quotes would be provided and and used as uh triggers or uh prices to lean on.

Edwin Johnson: I'm sorry. Then give me one second.

Troy McDonald Kane: No, no, it's fine.

Edwin Johnson: No, say that one more time.

Troy McDonald Kane: You don't have you didn't have to hear any of that.

Edwin Johnson: The last sentence. I I just You know how I am.

Brett StClair: Oh yeah.

Edwin Johnson: I can't

Troy McDonald Kane: Just how how the market making is going to work on the trading competition with you as the market maker and how the two-sided markets will be there and then others will lean or or improve those quotes based on their their information.

Edwin Johnson: That's right. That's right. All right.

  
  

### 00:03:48

  

Troy McDonald Kane: Yeah.

Edwin Johnson: Cool. Um, yeah. I mean, like we said on the call on Wednesday, it's just going to be balls to the wall. I know everyone, you know, we had a little bit of a session yesterday, but, uh, you know, we we still got so much to cover.

Brett StClair: really great.

Edwin Johnson: I mean,

Brett StClair: Thanks a

Edwin Johnson: we can do it, but it's going to, you know, it's not going to be able to be done without helping each other. So, unfortunately, it's just the next five weeks are going to be be rough. So, you just try to be as, you know, accommodative as possible with us, Brett and Max. You know, you're always there for us. We know that. Um, yeah.

Brett StClair: in the same we'll push the hours and burn the candle light as they say,

Edwin Johnson: So,

Brett StClair: right? Um,

Edwin Johnson: yeah.

Brett StClair: just a quick one.

Edwin Johnson: All

Brett StClair: I I regenerated your plan and what I added in was an extra

  
  

### 00:04:32

  

Edwin Johnson: right.

Brett StClair: component which was a growth plan that I loaded up front and said make something aggressive based on the kind of the assumptions you were making in the conversation load that up and then allow the media planner to kind of select where that growth finishes rather. So we kind of go ah we want it to finish at 500 what's required what is achievable what's not achievable in that time and then map it to a revenue stream and then have like a kind of moderate plan all the way up to a high plan which is really based on ad units served.

Edwin Johnson: Totally.

Brett StClair: So you had a 120 and a 240 and I kind of gave you two options and I figured I'd give you two decks on either one. I'm just in the process. It takes three four hours of working through and testing models. when I

Edwin Johnson: Before you do that, Brett,

Brett StClair: get

Edwin Johnson: that so I did a little research on app loving and mob mob

Brett StClair: at

Edwin Johnson: something mob ad mob and then the Google um

  
  

### 00:05:33

  

Brett StClair: mobile.

Edwin Johnson: rules and they basically they're tricky. Okay, so like getting four placements one every 15 seconds is not going to work the way that we want. Okay, we're going to need to do it differently.

Brett StClair: Rex

Edwin Johnson: And so basically I'm trying to create I wanted to have it ready for the call but I I don't basically um you know we want to on refresh rate on the trading portion of this. A couple things are missing. We're missing like the net position and the P&L for that game. You're going to need to see those. But, um, you know, I think like we need to embed like sell a logo for the field with like a

Brett StClair: Yes.

Edwin Johnson: transparent logo kind of like we did with the Red Bull. Um, you I've been trying to come up with different things that we could do. maybe a short-term pilot program where maybe it's like 50 grand uh and it

Brett StClair: Of course.

Edwin Johnson: lasts for two weeks and we earn out the 50 grand and if we don't earn it out then obviously they get whatever is not earned out back.

  
  

### 00:06:34

  

Edwin Johnson: Um and then you know basically I like I have four uh uh quadrants where we can or I'm sorry one in strike that four ads that are embedded into the horizontal screen but the ads are not like um the same right. So like you'll have the f****** egg,

Brett StClair: Yeah, you got like a banner unit,

Edwin Johnson: man,

Brett StClair: you got a volatility unit, and you got an

Edwin Johnson: right? So the the volatility unit we've got there,

Brett StClair: onfield.

Edwin Johnson: right? And then we've got the video before the game, after the first quarter, second quarter, third quarter, after the game. So we can we can embed those into where the field is, right? So the video will show, you know, within the the outline of the the field, but they don't go while like plays going on, right? like it's only during like known breaks in action and we could do those for 30 seconds and those you know based on a little bit of research if you look at finance and

Brett StClair: Yeah.

Edwin Johnson: sports obviously this is not day one but we could ramp up to a pretty good CPM for those types of things right and especially if we we get the

  
  

### 00:07:41

  

Brett StClair: Thank you very very much.

Edwin Johnson: criteria I think we just got it like I'm sorry

Brett StClair: No, that's George screaming how happy he is to get the connectivity to the

Edwin Johnson: Oh,

Brett StClair: space Chris has set up for him.

Edwin Johnson: I thought George got his first

Brett StClair: Yeah, he does that.

Edwin Johnson: date.

Brett StClair: It's random spurt of outburst of passion. Welcome,

Edwin Johnson: No doubt. No

Brett StClair: George.

George Westbrook: What what did I just random outburst of?

Edwin Johnson: doubt.

Brett StClair: We're talking about your date earlier on.

George Westbrook: Oh yeah.

Brett StClair: Um, just on the note on the ad units, um, I mean, I've been looking at all the different ad unit types and just trying to figure out what would load into a volatility moment. Your volatility moment is a two three second flash up and uh and the shape of it and the distribution of it whether it's on widescreen or horizontal is going to impact the type of ad unit and I don't know if this SSPs are going to be able to serve that type of ad unit.

  
  

### 00:08:50

  

Brett StClair: So we just got to be aware of those kind of things as well.

Edwin Johnson: Yeah. And you know, I think what we do there on some of those if If we don't go through the SSP for those and we just try to direct sell those, we can still run them, right? So, um, man, I I thought I had a good lead on that Gallow Lines. What happened last night, man? I I end up this this woman was like, "Hey, can we move over to WhatsApp?" And it get turned into a situation and I'm like what the f***, man? Really?

Brett StClair: Jesus.

Edwin Johnson: Like it I mean it was I I don't know what's going on. I think I'm I think there's a campaign to try to f*** with me right now going out there. Um you know, we received a a like a s*** Facebook post purportedly about me yesterday. We've got that Wikipedia thing came out where there's like a, you know, some guy. That guy's legit though, right?

  
  

### 00:10:01

  

Troy McDonald Kane: John Lotheian. Yeah. No, he's Yeah,

Edwin Johnson: Troy.

Troy McDonald Kane: he's you call legit is like he has a very large following and has been reporting on the industry for two decades almost. So,

Edwin Johnson: Yeah. Somehow someway though, I made it on his radar that he wrote a like a bio on me and the guy.

Troy McDonald Kane: yeah.

Edwin Johnson: It's a very long bio. It's not a smear piece, but it's definitely I like to be in the shadows more than I, you know what I mean? So, um, you know, I don't know that I don't know what happened that situation last night, but it turned into like a felt like one of those honeypot traps looking at camera,

Brett StClair: Where's the candle camera? That kind of thing.

Edwin Johnson: but like I mean there was Yeah, I don't know what the f***** going on. Anyways, maybe we can try to re, you know, sell those um specially uh because I think those in in particular, even if we try to dump them like for a small amount, but we go for like two weeks worth, right?

  
  

### 00:10:56

  

Edwin Johnson: And it's like, you know, we we just don't go for the whole competition, you know, we just try to continue to resell. So I I I've been thinking about like you know trying to lower like just for the pilot for the first say two to four weeks have the minimum spend like 50 grand and then have the max spend like 250 and then let's try to build it up you know we and for maybe for the first two weeks guys we distribute 90% of the ad revenue so that the user base gets enough juice as opposed to 65%. So, I've been trying to play with a couple models in my mind, but you know,

Brett StClair: Yeah,

Edwin Johnson: we we'll we'll see. So, I do appreciate that though, Brett. Those definitely help. Um, but it certainly

Brett StClair: I'll run your next set of recommendations on it on a separate kind of path so you can see the difference between

Edwin Johnson: Yeah. Before you do,

Brett StClair: everything.

Edwin Johnson: I got one more set that I'm going to send you, which is going to be um the rules like as like as it stands at

  
  

### 00:11:50

  

George Westbrook: Okay.

Brett StClair: Okay.

Edwin Johnson: the moment. So, like if we somehow bid four different like uh ads within the trading horizontal, right? You know, maybe it's above the game, maybe it's, you know, lower left, the the the probability chart sponsored by the price chart sponsored by. Um, and if we rotate them, not like every minute they all flash different, but like 15 seconds, 30, 45, it becomes like just this uh rolling refresh. Um, that seems to stick because then each one's on for a minute.

Brett StClair: on the card.

Edwin Johnson: So according according to what's

Cody Haugen: It also keeps eyes.

Brett StClair: Yeah.

Edwin Johnson: that?

Cody Haugen: I said it also keeps the eyes refreshed if they're all flashing at different times while you're watching the game.

Edwin Johnson: Yeah. Well, I don't know. We're going to flash him, but certainly they hopefully

Cody Haugen: Well, the the the rotation, not flash, but like if you're changing from a Coke to a uh whatever the f***.

Edwin Johnson: Yeah.

Cody Haugen: Yeah, I think you get what I'm saying.

  
  

### 00:12:57

  

Edwin Johnson: Yeah. So that might be easier on the eyes, but like I mean I thought we could do one every 15 seconds because that seemed like a short amount of time, but based on Google they'll they don't want it less than 30

Cody Haugen: Yeah, I saw

Brett StClair: Yeah. Yeah.

Edwin Johnson: seconds.

Brett StClair: I had a feeling it was going to be longer.

Cody Haugen: that.

Brett StClair: It's again it goes down to that conversion, right? um they want it there for a longer time because they're trying to get the click through.

Edwin Johnson: Yeah, for sure.

Brett StClair: Um and there's always a metric. So 30 seconds does feel kind of right for

Edwin Johnson: Yeah. So, I mean on our trading app,

Brett StClair: me.

Edwin Johnson: we might have talked about this yesterday internally. On the trading app, I don't see a lot of clickth through. On on the trading page, like the horizontal trading page, I do not see a lot of clickthrough. On other parts of the app, I see a lot of clickth through.

  
  

### 00:13:51

  

Edwin Johnson: But if you're focused on a game and you're you're trading it back and forth, unless it's like halftime and you're ready to eat a sandwich or something, you know, you probably click on something then. And then it probably has high clickth through to be

Brett StClair: Yeah, we'll see how it lands,

Edwin Johnson: honest.

Brett StClair: right? It's your premium ad inventory space from a volume point of view. Like it was quite interesting running those charts, right? to see how it compared both from the page point of view compared to other pages and from the audience point of view. Um, it generates a lot of impressions. So, we do want to kind of make sure it's not degradating your overall CTR and just got to figure that

Edwin Johnson: Yeah.

Brett StClair: out.

Edwin Johnson: Okay. Um All right. What What's next?

Brett StClair: Um, from our side. George, we we haven't got any updates at the moment, right? Uh no, apart from the

George Westbrook: the education that's been updated um with all the 16 new modules.

  
  

### 00:14:58

  

George Westbrook: was every video under 2 minutes. Um, so once we get that pushed, if we have another review of that and then once we get the the updated modules as well, we'll get through that as well. Um, I think one of the biggest things for us at the moment is all the the trading market making stuff which which which we still need to still need to tackle. Um, because it's I think the key things that we we've got, I said there's three um well, the two main ones are ads and trading. um which non-negotiables, they need to be f****** nailed. One's the core experience, the other one's the method of generating revenue. So, if there's two buckets we want to be putting as much in, it's it's them. Um ads, same thing. It's what SSPs set up, get them linked in, get the test ad units in. I mean, we've already got the spaces in in the app. We can add some more, do some more testing. um education as well getting that that's there's not loads that needs to be done there.

  
  

### 00:16:01

  

George Westbrook: Um unless it needs to be ripped completely down, but I don't I don't personally think it does. Um and then but then when it comes to trading, it's obviously well after we have the call around the market making um then I think we'll get a lot more clarity. Um it's it's for us it's kind of where does it sit? How does it work? not in terms of the actual algorithm but what's the from that point at which the user clicks the button um where the market m market algorithm is where where does it sit how does it work um and interacting with t0 as well but we had a that quick five 10 minutes that we had with Chris got access to this platform that they've got which has given us a lot more visibility um is just making sure that we've got that obviously it all.

Edwin Johnson: Cool. Cool. Um, yeah. And you know the more and more we think about it like you know that 10,000 we're gaining

George Westbrook: Now,

Edwin Johnson: for hoping to have for like IPO launch I mean we can always iterate during the first couple weeks of the competition to get this thing going but like you said the core dem or the core structure has to be the trading experience has to be amazing and the ad experience has to be amazing.

  
  

### 00:17:22

  

Edwin Johnson: you know, thought that that's where our bread's going to get buttered and where we're going to be determined to be successful or not, at least at first glance.

George Westbrook: Yeah.

Edwin Johnson: So, um,

George Westbrook: about the store name the Oh,

Edwin Johnson: cool.

George Westbrook: what the the app store? Yeah. Yeah. So, it was just uh it just a quick message that we sent back to them because it's to do with age controls. They were like, you need age controls and we've put in the application. Well, nobody under the age of 18 is even going to be able to get into the app. Um, so that's ridiculous. Waiting for a response from them on that Play Store as Well, that's that's getting submitted soon. Um, but obviously like we said, Apple 70 80% of the users are going to be on Apple. Um, so that's the that's the main one we want. We're we're concerned not concerned as in but where we're where the effort is. Um cuz I think it's Yeah.

  
  

### 00:18:16

  

Troy McDonald Kane: Now,

George Westbrook: And

Troy McDonald Kane: in the in the when you when you went back with the age verification,

George Westbrook: it

Troy McDonald Kane: did they do they know that we're leveraging Persona for that, which is a very reputable KYC platform out

George Westbrook: Yeah,

Troy McDonald Kane: there?

George Westbrook: I think in the me correct if I'm wrong. Um in the message we we we put that it is I think it probably was in it was in the it was in the

Troy McDonald Kane: Okay. Yeah.

George Westbrook: application as well, wasn't it? Yeah. They as I should have tagged as easy as it tells you that it's authorized.

Troy McDonald Kane: Yeah.

George Westbrook: They should they should have it's stuff they should have already known if they looked through the f****** application properly.

Troy McDonald Kane: Yeah.

George Westbrook: Um but I suppose it's Apple, isn't it? They've got probably millions of these.

Troy McDonald Kane: Yeah. And they like to do them man like human manually versus automated too.

George Westbrook: Yeah.

  
  

### 00:19:00

  

Troy McDonald Kane: So you know

George Westbrook: Yeah. So it's yeah that's the ads just getting them connected up education on that the and then the watch page as well that's one thing where we'll be adding improvements like we were saying the other day one obviously the ad units are going to be that going to need to be in there where are they going to sit and then also having more functionality in there as well like we said with the maybe on the right hand side swiping up and down to see different graph views um so it's a bit more interactive. Um, but just brainstorming what what we could add there. The futures thing as well. Um, the API Kodi, we were testing it and it just kept on coming back saying unauthorized. Do some more today. Send over to Scott what we were doing just to see if it's a an us issue or a them issue. Um when we were researching it was saying that for the trial version you weren't able to access the um the win like so we could it wasn't as if we didn't have access like we could access let's say there was 10 endpoints we could access eight eight or nine of them but the one that we actually wanted it was saying it was unauthorized.

  
  

### 00:20:15

  

Cody Haugen: Yeah. Yeah. I mean that that should be cleaned up really easily through support. Um makes me feel better though of why I wasn't able to pull it. I was like I'm pretty this the right way. Um two things to your point,

George Westbrook: Yeah.

Cody Haugen: George. Uh just quick feedback on the uh new money maker page which is the watch page. Um it it uh the slider button down at the bottom.

George Westbrook: Mhm.

Cody Haugen: um when you're using that to slide through the volatility moments. Um you know what button I'm talking about that you were showing?

George Westbrook: Yeah. The the Yeah.

Edwin Johnson: Yep.

Cody Haugen: Yeah. Either way,

George Westbrook: Yeah.

Cody Haugen: maybe it's because I have a fatter thumb than most, but it because it's so close to the bottom of the screen, it moves the entire app like you're trying to close the app. You know what I'm saying?

George Westbrook: Oh

Cody Haugen: When you're dragging it like nine out of ten times like I have to be very slow and deliberate with it

  
  

### 00:21:02

  

George Westbrook: yeah.

Cody Haugen: if I want to slide at all more than just click through one at a time. Um and then uh so I don't know if we want

Edwin Johnson: I would lose the slider.

Cody Haugen: to that's what I was thinking I would do.

Edwin Johnson: I would just go with the button.

Cody Haugen: That was going to be my suggestion is just keep the click through one by one.

George Westbrook: H.

Edwin Johnson: Yeah, I think that that's the best. I mean, yeah, I I would lose that.

George Westbrook: Okay.

Edwin Johnson: And then we have a little bit of room potentially for the um I want to be able to see my like net position while I'm trading on this screen for this game. So if I'm long or short one of these two teams, I want to know that. I want to know whether I'm up or down money on this particular game, you know, so I trade that and then I want to know um you know maybe you know my global P&L for the day or something or total somewhere in there, right?

  
  

### 00:22:00

  

Edwin Johnson: So, um, yeah, and then we've got to figure out how to manage the the advertisement in here in a way that's, uh, going to comply with the, you know, rules on these SSPs that we still get. I still want to try to start with 720 impressions per minute. No, per hour.

Cody Haugen: Yeah. Per

Edwin Johnson: Per hour on these, right?

Cody Haugen: hour.

Edwin Johnson: So like if we have four refreshing every minute that's 240 uh per hour and so 720 per game that that that would be good. I mean, I think I think we need that number to get into, you know, that that lynch pin to start us off because if we can if we can show any traction whatsoever, I'm I'm pretty sure we'll we'll get that uh the original CPM rate up, right, Brett? Like the more we show the higher we can deliver that number you know because if we can get it where we're our cut is a buck 50 net I mean we can do really well with this I mean anywhere between you know 20 and 30

  
  

### 00:23:11

  

Cody Haugen: Yeah.

Edwin Johnson: million

Cody Haugen: Yeah. George, I have one more edit for you on that page if you I don't know if you want to pull it up quick just so I can kind of talk you through what I was seeing.

George Westbrook: Just a quick one. Make us fall.

Brett StClair: setting up. Um Keville, uh see he's chasing you. Um my gut on this is we should be going with the SSP ad server. Um uh Max loving the apploving one. Use that as the ad server. Then we plug in SSPs into that for now.

Edwin Johnson: Yeah.

Brett StClair: and

Edwin Johnson: What will I budget for that Brett?

Brett StClair: then

Edwin Johnson: What do I need to to put aside for that applo uh ad server roughly?

Brett StClair: it'll come it'll come off. So, we've actually calculated it into the ad serving fees depending on who it is. So, it'll actually come off the ad serving. So, you know, when I've got the eCPM, I've actually factored it in there.

  
  

### 00:24:10

  

Edwin Johnson: Okay. So,

Brett StClair: And you don't have,

Edwin Johnson: I don't have to put up like half a million bucks.

Brett StClair: you shouldn't have to um what I can see of it, it's the same as ADM.

Edwin Johnson: Okay.

Brett StClair: They take a deduction off the top and then each of the SSPs take a deduction off the top. Um, unless there's some premium services that I just haven't got to, it shouldn't be a problem. The Keville is different. They're an actual ad server. They're only doing the ad serving component. They're not providing anything else. So, they charge a set fee. I think they become important to be able to serve those custom ads and do direct buys and that. So, I I think we should rather put them in a bit of a hold and say, "Listen, we're just trying to get everything going. We're going to load uh and we just tell them it's ADM Mob for now. We're going to get it up and running as soon as we get our first deal.

  
  

### 00:25:04

  

Brett StClair: They become really important when you want to do your direct buys and you want to do your custom units. You it's it's the only way you're going to be able to serve it at the scale you need to be able to serve it.

Edwin Johnson: Yeah.

Brett StClair: And I think because they're more on a, you know, have to have a set budget and set set fee. Um, you probably don't want to start that until we know that we're getting direct deals, right? Soon as we get direct deals,

Edwin Johnson: Yeah,

Brett StClair: it's very quick to set up. By the way, it's one or two weeks, config, test,

Edwin Johnson: cool.

Brett StClair: setup campaigns, fire it out. And so, like, I don't think we blow them off. I think we put them on a holding pattern.

Edwin Johnson: Yeah. Okay, I'll respond.

Brett StClair: and and he should be comfortable with it. He's I can see what he's doing. He's hitting his end of quarter target. So, he's he's under

Edwin Johnson: Yeah.

  
  

### 00:25:57

  

Edwin Johnson: So that uh Okay, cool. Thank you for that.

Brett StClair: pressure.

Edwin Johnson: I will respond to him uh today. Um the slider I would lose um that. And then George with I I won't say this is short. Um, but it looks like there's still some real estate that we're not using within the phone. Is that true?

Brett StClair: Um, I'd say here here. But every on

George Westbrook: This is, let's say, some of them don't have the island. Um, some of them do. So, really, I'd say it's here, here, and here. Um,

Edwin Johnson: Yeah,

George Westbrook: and maybe with no slider. Um

Edwin Johnson: maybe we can put that the P&L in position there right by trade,

George Westbrook: h

Edwin Johnson: you know.

Brett StClair: Yeah.

George Westbrook: I was thinking here like so it could be let's imagine there's five different five of these. So you as a user You can scroll, you can scroll down and then let's say like your P&L comes up all your positions in this game and in between each one is an ad unit.

  
  

### 00:27:09

  

George Westbrook: So like in between here and here there'd be an ad unit. As you scroll down there'd be another ad unit above it in between the next one. So it's kind of like an infinite infinite scrolling

Edwin Johnson: Yeah,

George Westbrook: thing.

Edwin Johnson: I don't know if I love that. Um, I was thinking, you know, we sell placement on the field again. We we we get somebody for the middle of that field,

George Westbrook: Mhm.

Edwin Johnson: you know, a a somewhat transparent overlay. Okay. And then, you know, within that that field box, that's where we're going to play the videos before the game, first, second quarter, third, uh, first, second, third, and fourth quarter, and halftime. Um, and then above the field, there's room for something. Yeah, somewhere there. And then maybe on the charts um you know we can have the more native where it's presented by you know that that that that period of time is present by Wow. That's f****** cool. I didn't see this.

Brett StClair: And then it's time to be

  
  

### 00:28:15

  

George Westbrook: It'd be like for each of the Oh, let me go back. That's a bug. Um, so for each of these, so on, imagine there's five. They can click and expand in. Um, and then in each of the expandable Oh, I know it's cuz I'm clicking the wrong button, that's why. Um, so in each of these, obviously, there's a lot of space. So then there's the these would be more direct. So like similar to the inplay popup when there's an event um this could be direct sales direct space as well. Um and then like user is scroll see this one then

Edwin Johnson: Yes.

George Westbrook: add unit here each time they click into

Cody Haugen: Yeah.

George Westbrook: one

Cody Haugen: So the uh the second just feedback piece before I forget to give it to you George is when you're on this if you're on IUB who whatever team you have selected if you click trade you can only trade that one team. So click trade once. Yeah, right there it it looks exactly the same screen as we have for the IPL.

  
  

### 00:29:22

  

Cody Haugen: Yep. You can't swipe to the other team. Just want to let you quick note there. So,

Brett StClair: Yeah,

Cody Haugen: yeah, make sure we can swipe to to both teams in that game and back and forth. Yeah, like you don't want to you don't want to spend time typing it

George Westbrook: Yep.

Brett StClair: I think this

Cody Haugen: in.

George Westbrook: I think we need to just change how this is laid out as well because this looks I mean it looks good on when it's there.

Cody Haugen: Yeah. When it's when it's Yeah.

Edwin Johnson: portrait.

Cody Haugen: When it's vertical.

George Westbrook: Yeah. It's just Yeah, because in the how we could have this. Maybe

Edwin Johnson: You know what, Cody, I don't know if you've clicked on these charts while he's doing that.

George Westbrook: it's

Edwin Johnson: When you expand the chart and you click and it's basically like shows all the different candlesticks and

Cody Haugen: Yep. Yeah,

Edwin Johnson: there's a little button on there,

Cody Haugen: I was Yeah.

  
  

### 00:30:12

  

Edwin Johnson: you click on it, it says what happened even in

Cody Haugen: No, no, I was playing with it yesterday.

Edwin Johnson: this

Cody Haugen: That's awesome for the uh for the chart traders out there, right

Edwin Johnson: Troy. We really need someone like going page by page on all this because like I don't have time right

Cody Haugen: Jared?

Edwin Johnson: now.

Troy McDonald Kane: Yeah.

Edwin Johnson: I mean, can is it some we can put uh any of our misfits in?

Troy McDonald Kane: Which misfits?

Edwin Johnson: I mean, we got a

Troy McDonald Kane: Yeah. Um I mean so we just added so well that that's what I was about to say.

Jared Sapirman: I think

Edwin Johnson: bunch

Troy McDonald Kane: We have the two our first two interns.

Jared Sapirman: intern

Troy McDonald Kane: So Cam and um Claybornne have gotten access to the test flight.

Edwin Johnson: of

Troy McDonald Kane: So uh Cam starts Monday. We can have Cam be one of the alpha testers on this. So um and have him going through it.

Edwin Johnson: Okay.

  
  

### 00:31:10

  

Troy McDonald Kane: I'll I'll check in with him today to see if he had gotten access to it because I know Hassan sent access rights to him and to to to uh to

Brett StClair: And it's even by even

George Westbrook: tiniest things that are that are broken.

Troy McDonald Kane: Clyborn.

George Westbrook: Like say for example, one of them which keeps on annoying me is I accidentally keep on clicking that button instead of

Cody Haugen: Yeah, I did the first five times,

George Westbrook: the

Cody Haugen: George. Yeah,

Brett StClair: Yeah, I

Cody Haugen: instead of minimize on the right side.

Brett StClair: think

Troy McDonald Kane: Yeah,

Cody Haugen: Yeah.

Troy McDonald Kane: we'll have them do extensive QAing of this click by click, page by page, inch by inch.

Edwin Johnson: Okay, cool. Yeah, because we definitely need

Troy McDonald Kane: Yeah.

George Westbrook: cuz I think it's like we said initially it's getting for for everything getting to that first 80% like that it's that

Edwin Johnson: that.

George Westbrook: last 20% which takes up 80% of the

Troy McDonald Kane: Yeah. And then Cody and Jared, I feel like you two both should be trying to spend as much time on it as I know we're all managing multiple priorities right now, but Cody, since you're a a active gambler and Jared, you traded.

  
  

### 00:32:20

  

Troy McDonald Kane: It's about getting your feedback on the functionality and does it keep the engagement levels high.

Cody Haugen: Yep. Absolutely. Already doing

Troy McDonald Kane: Yeah.

Jared Sapirman: Yeah, same. It'll be a lot more um effective for me once I see the how the trading functionality

Cody Haugen: it.

Troy McDonald Kane: So

Jared Sapirman: works because I can't trade on here yet.

Troy McDonald Kane: well, not on the test flight version.

Jared Sapirman: Yeah.

George Westbrook: the

Troy McDonald Kane: The test flight version is for the IPOs only.

Jared Sapirman: Yeah.

George Westbrook: the the PWA version.

Troy McDonald Kane: Yeah.

George Westbrook: I think that there's that will have the what what is currently the trading flow. Have a look. Um yeah, if we send that if we send that over um then that's just the current trading flow. I think we need to see if we might need to promote an old version or redeploy an old version. Um so it's not going to look or feel ex like this at all. Um, it might even be easier if we just turn on the trading function for this one.

  
  

### 00:33:41

  

George Westbrook: We'll have a think.

Cody Haugen: Cool.

George Westbrook: Um, and get something sorted. We can do two. We can do we can do two we can do two different versions, can't we? In test flight. Yeah. So, I think better it will be, pardon me, two different versions in test flight. um one IPO, other one trade inversion. Um and then that will that will give a better handle of what the UX is going to look like post IPO

Troy McDonald Kane: Yeah, I like that a lot because then we can also uh not only QA it but then we can demo

George Westbrook: IPO.

Edwin Johnson: Yeah.

Troy McDonald Kane: it better.

Edwin Johnson: And remember that the actual trading other than the IPO doesn't begin until August 29th. So the the the actual application, no one's going to be able to trade. Well, strike that. That's not true. after we close the IPO, they can trade it, but there'll be no there'll be no onfield like, you know, stuff happening. So, I mean,

  
  

### 00:34:44

  

George Westbrook: Yeah.

Edwin Johnson: we could we could not have the trade. That's not good. Let we'll think on that, too. I mean, um you know, thing is with Cody, like Cody's got a tough thing. Kevin and Cody got to start helping me with ad sales,

George Westbrook: Hat.

Edwin Johnson: too, because we're gonna have to really grab this thing by the balls and f****** run because we're in trouble on this one. You know,

Kevin Murray: Yeah.

Edwin Johnson: if we don't have enough capital to distribute daily, all the people we pay for to come to the app are going to lose interest real quick. So, we've got to make sure that once we get them, we got to offer them enough juice for them to stay. Okay? I think people will do it for a little bit of time with a little less money but ultimately this

Brett StClair: Oh s***.

Edwin Johnson: comes down to they want to come they want to be able to earn something tangible and that's you know exciting otherwise no matter how good the app is no how matter how good the ads are it's not going to work so you know I told the team yesterday I'll put in a million bucks for August uh advertising to acquire users two million bucks September is that what we agreed

  
  

### 00:35:51

  

Troy McDonald Kane: Yes,

Cody Haugen: Yes.

Troy McDonald Kane: that's what we agreed on yesterday.

Edwin Johnson: total of three for that. And then um you know I'll put in maybe another one or two for uh prize money to ensure that that initial start we get some. But you know I personally I'm I'm getting out on my skis a bit here and I want to make sure that like I'm seeing something that I'm not just pissing money away. All right, cool. Um All right. So,

Cody Haugen: Absolutely.

Edwin Johnson: what what's what's how do we leave this call? Other than wishing everyone a great weekend, what are the to-dos that we have to do? Brett, I owe you a couple more inputs potentially from the, you know, for this particular uh what are you calling it? Like the uh media plan.

George Westbrook: Medic.

Edwin Johnson: Yep. And then you're going to try to get me some PDFs and

Brett StClair: Yeah. So,

Edwin Johnson: then Okay,

Brett StClair: I I'll do it as PowerPoint so you can at least edit it as well if you don't like something in

  
  

### 00:36:52

  

Edwin Johnson: cool. That that helps. And then for Sweet Mac Kingab,

Brett StClair: Yeah.

Edwin Johnson: um, is he the the you're the power point like you're the deck guy now.

Brett StClair: He's going to be I need to hand him back over all the skilled and algorithms now.

Edwin Johnson: All right. Sweet.

Brett StClair: Uh he doesn't know how much I've

Edwin Johnson: Um, and yeah,

Max Kingaby: I'll catch up.

Edwin Johnson: so basically here's what I've got.

Brett StClair: changed.

Edwin Johnson: I've got about a 30page document that describes our business model. It's going to have all of our projections for hiring and costs. Okay. And we're going to try to map out what we think this is going to do for the initial, you know, simulation. You know, again, if we can break even on this one to losing a little bit of money, it's a massive win. Okay? Because that then we start to have customer acquisitions. We can turn them on to production and we can roll right into the NBA trading simulation in October.

  
  

### 00:37:49

  

Edwin Johnson: So, you know, while we're doing this for, you know, August launch and September launch, we're going to have another one late October. And by that time, people should be aware of what this is, and we should be able to command a lot more money for the, you know, marketing pieces. Hopefully, we'll get some direct buys and then, you know, we can enhance all of that, uh, prize pool. So, you know, as as of you know, as much as I had hoped we'd make some money, even if we lose a little little bit, but we got that customer acquisition funnel clicking, it should be okay.

George Westbrook: Then

Brett StClair: Yeah,

Edwin Johnson: Okay. So, I owe you a few things, Brett, and I no matter what,

Brett StClair: agreed.

Edwin Johnson: I'm leaving my house at 10:30 to go to Chase Bank,

George Westbrook: Thank

Edwin Johnson: and then you're going to be on standby if there's an issue. Um,

George Westbrook: you.

Edwin Johnson: and I'll have that taken care of. And then, uh, Cody, maybe we can talk about this this landscape on how we want this to look, um, for trading.

  
  

### 00:38:55

  

Edwin Johnson: And then P&L, Troy, Kevin, Jared, Let's really focus on that maybe over the next hour so we can get those over to George and Keem and then uh

Troy McDonald Kane: Yeah, we have a team huddle in 20 minutes, so maybe we can take that into that.

Edwin Johnson: Perfect.

Troy McDonald Kane: Yeah.

Edwin Johnson: Cool. Um All right. Is there anything that anyone else needs from me at the

Troy McDonald Kane: Yeah.

Brett StClair: I think They

Edwin Johnson: moment?

George Westbrook: anything would be is before the market making call on Wednesday if there's anything that you think would be good for us to know before going into it as long as as well as obviously the documents you sent over before send them over and we'll we'll we'll make sure to have a thorough look through is

Troy McDonald Kane: What?

Edwin Johnson: I I'll ask the the like one of Claude or something give me a layman's description of what I wrote. Okay. So that it's like readable. Okay. Because I I thought we were going to walk through it and you could just basically put that s***

  
  

### 00:39:41

  

Troy McDonald Kane: Yeah.

Edwin Johnson: into a gentic and then it would start to like grab it. Right. I that my goal is never to be like,

Brett StClair: s***.

Edwin Johnson: "Oh, you know, this is so tough to understand." Not even close. I I just want

George Westbrook: is like this with with anything we build.

Brett StClair: cuz it's

Edwin Johnson: Yeah.

George Westbrook: It's it's it's not here you go just build it because like we we want to understand it because it's as much as Agent KI is very good everything we build we make sure that we understand because it's just it's uncomfortable for us knowing that we've we've built something and we're we're not necessarily sure on the mechanism behind it. It's It's not to say that with that we couldn't just pump it into AI, but it wouldn't feel comfortable for us knowing that we built you something and we're kind of like, "Yeah, I think it works."

Edwin Johnson: Right. No, I I get that. I mean, and there's going to be mistakes,

George Westbrook: Um,

  
  

### 00:40:40

  

Edwin Johnson: okay? And and we we all need to realize that there's going to be hiccups.

Brett StClair: Huh?

Edwin Johnson: We just hope that they're not critical. Okay? So, um,

Brett StClair: Yeah.

Edwin Johnson: like there's probably a couple pointer cases on the market making I haven't even dreamt of yet on this simulation because like no one's ever had a 247 stock market in the history of the world. So, this is we we're doing a whole lot of firsts here and trying to market that. Um,

George Westbrook: Hollywood.

Edwin Johnson: yeah, it's tricky because basically, you know, at the end of the day, there's two prices you need. you need uh you need to take in like okay what's prob like we're gonna just call it probability probability for today's game and then how do you measure that about probability over how many games are left. So basically, you know, you look at today's game, there's like an 80% probability a team's going to win and that payout's five bucks and we don't know what the onfield is, but we know like uh I'm sorry, the off field is yet, but we'll have some idea based on that criteria I created for the off-field projected revenue.

  
  

### 00:41:48

  

Edwin Johnson: You know, like I don't know if you saw, but like Dallas Cowboys, very popular team, they're expected to make 30 bucks off field. And a team like Carolina is only expected to make like 14 or So, you know, just in terms of like attendance, jersey sales, you know, people watching the games, all that s***, I baked all that into like projecting how to make the off-field, uh, you know, revenue component, uh, with enough disparity that it's tradable because we don't want to just be 5050, right? So, um, but basically, you know, so you're the market maker is going to reference the the current probability price as one input. It's going to reference another price that we're going to create, which is the probability over all the games left. So, if the first game of the year, they got 16 games left. Each of those games will have a probability measured to it and then it'll have a value and then that value is going to be extrapolated over those 16 games. And then we're going to times that times five and that's going to be our long-term price.

  
  

### 00:42:53

  

Edwin Johnson: Um, and then we we we merge the two, right? So, it it's it's not as difficult as the paperwork made it.

George Westbrook: Okay.

Edwin Johnson: Um, you know, I've I thought you guys could just like, you know, put a PDF in like in there would get it. Um, but it it's it's okay. We'll we'll walk through. It's going to be a lot it's going to be a lot less sticky than we think. But like Troy, you know, we also have to think about these corner cases because there's going to be a bunch. You know,

Troy McDonald Kane: I know.

Edwin Johnson: we we came up with one the other day, which is like when a team that's has uh shares available plays another

Troy McDonald Kane: Yeah.

Edwin Johnson: team that's a like a lower team that doesn't have shares, how do we distribute the off-field revenue, right? We just got to give all of it to the team that's tradable. We can't give any because there's no no allocation that we can give them. So, that that's a component.

  
  

### 00:43:46

  

Edwin Johnson: So when we do the pricing, you know, if there's let's say I think there's 180 games like that over the of the 2100 like you have to already factor that 100% of that 250 for offfield revenues go to that team anyway. So that goes into the mix, right? So it's like probability probability for the season and then off-field revenue raise and then all that gets compiled. Then we have a reference price and the market maker basically says I'm going to bid below and I'm going to bid above and I'm I'm going to instruct I want to instruct it to have certain criteria which is a randomization factor so it doesn't look like a like a you know a machine is putting 500 lots 500 500 500 um you know we're going to have some different techniques in there that I've I've used to to add variability variability to the markets interpretation of what they're trading against and who they're trading against. So, it it it it's a lot it's much easier than the paperwork sounds for for what we're doing in a simulation.

  
  

### 00:44:51

  

Edwin Johnson: Okay.

George Westbrook: Mhm.

Edwin Johnson: Production is going to be a little bit tougher.

Brett StClair: Yeah.

George Westbrook: My weekend sorted then.

Edwin Johnson: Yeah. Oh, well, and I'll I'll have I'll I'll send something over within the next hour or two. I just want to I like my my life like all my s***

George Westbrook: Okay.

Edwin Johnson: is uh like I haven't left my office other than to go downtown yesterday and that was a nightmare. I don't know if you guys saw but we're in smoke. Like it's like is Gary on the call? Not on today. Oh yeah. It's like Gary's screen full time.

Kevin Murray: No.

Edwin Johnson: Seriously,

George Westbrook: Shut.

Edwin Johnson: Chicago was the unhealthiest air in the world yesterday.

Brett StClair: What?

Edwin Johnson: Like I think they said like at over 300.

Cody Haugen: Yeah.

Brett StClair: Jesus.

Edwin Johnson: It's terrible and dangerous.

Troy McDonald Kane: Yeah.

Edwin Johnson: We were at like 7 something. The rating like 750 or something. And we all walked out.

  
  

### 00:45:49

  

Edwin Johnson: I took the Uber down and I had to take the train back. By the way, I had a real issue on the train with the f****** guy collecting the money. He comes up, I go, I need to buy a ticket. The guy gets all worked up. I'm like, "What the f***, dude?" Like, "What's your problem?" He's like, "It's five bucks more." I'm like, "Okay." You know, so he's like, "But I'm not going to charge you because you you don't take the train, right?" And I'm like, "No." So, um, you know, he, you know, he gave me the ticket and I paid him. It was $5.50, so I I just gained 20. I said, "Go get yourself a beer and learn how to relax a little bit." f*** you, dude. So, yeah, the train's off for me. No more train,

Cody Haugen: You're one

Edwin Johnson: please.

Troy McDonald Kane: I mean, you you do have your personal Uber driver on this call that's happy to pick you up and take you home

  
  

### 00:46:33

  

Cody Haugen: try.

Troy McDonald Kane: whenever you want. So,

Edwin Johnson: The problem is I got to listen to his tail of love. That's the cost of the drive. All right. All right. Um All right. We know what we got to owe. I owe you Brett. I owe you George. Let me do this. And then I don't owe Max s***. And I don't owe uh Hassan anything. Right. All right. Cool. All right. And then we'll see each other on the next 10 minutes, the rest of us. Uh and then Brett, I'm going to be over there in about an hour and 10 minutes. And then you're going to be ready on the phone if there's an issue on your end. Okay.

Brett StClair: Perfect. Perfect.

Edwin Johnson: Okay, thank you all. Have a great weekend.

Brett StClair: He's going

Edwin Johnson: We'll talk soon.

Kevin Murray: Thanks everyone.

Skye Capazorio: Thanks all.

Edwin Johnson: See you.

Troy McDonald Kane: Thank

Brett StClair: to

Cody Haugen: Let's f****** go, George.

Brett StClair: That was beautiful.

  
  

### Transcription ended after 00:47:49

  

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.

**