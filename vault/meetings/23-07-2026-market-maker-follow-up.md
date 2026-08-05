---
date: 2026-07-23
type: general
scope:
  - "[[market-maker/market-maker]]"
  - "[[customer-onboarding/customer-onboarding]]"
  - "[[referral/referral]]"
status: extracted
extracted-to:
  - "[[market-maker/decisions]]"
  - "[[market-maker/open-questions]]"
  - "[[market-maker/parameters]]"
  - "[[market-maker/plan]]"
  - "[[market-maker/learnings]]"
---

## Post-Call Analysis

46-minute multi-topic call ("Follow up with Market Maker"). App launched on the Apple App Store the night before — first ~10 minutes are launch status. Edwin arrived late; the middle ~30 minutes are a market-maker working session that materially simplified the quoting design and resolved three valuation open questions. Final segment (after George dropped): KYC objection handling. ⚠ This was **not** the planned deep-dive agenda — E11 (settlement definition) and E12 (NCAA scope) were never asked; Edwin: "we didn't get a ton done on the market making" — another MM call expected.

> ✅ **Extraction complete 23-07** (same-day session, George + Claude). All MM findings written to the destinations listed below. Finding #11 (v1 crossing tolerance) confirmed by George: post-first, momentary self-cross tolerated in v1. Session note covers the working session. Other-findings rows (#18–23) NOT extracted here — they belong to app/onboarding components.

### Market Maker findings

| # | Finding | Destination | Action |
|---|---------|-------------|--------|
| 1 | **Quote lifecycle overturned:** partially-filled resting orders are never topped up — they rest until fully gone. On price move: cancel the old level, post remaining qty at the new price. After a full fill at unchanged price: reload at top of book | [[market-maker/decisions]] · [[market-maker/open-questions]] N10/N12 · [[market-maker/learnings]] | ✂ Supersedes the update-in-place recommendation and the 23-07 top-up replace mechanics |
| 2 | **Cadence bifurcated by game state:** live games ~200ms/call ("a second's too long"); non-live every 30–60s; earnings windows call all ~170 for ~5 min (Tue NFL / Wed NCAA) | [[market-maker/decisions]] · [[market-maker/parameters]] · [[market-maker/plan]] | Revises the all-teams-every-cycle framing |
| 3 | **Fill-response logic is a design item** — "if you get a fill, what do you do next" (e.g. off-game, leave the bid and fill down through the ladder) | [[market-maker/open-questions]] | New N-item |
| 4 | **Randomizer = quantities only** — price purely algorithmic; top-of-book size randomized so the book doesn't read programmatic | [[market-maker/decisions]] · [[market-maker/parameters]] | Narrows the 20-07 randomizer decision |
| 5 | **In-game price driver = Sport Radar live win probability, pulled directly** — no own event-weight algorithm in v1 | [[market-maker/open-questions]] E15 · [[market-maker/parameters]] | E15 resolved; `event trigger weights` not needed v1 |
| 6 | **Remaining-season wins produced internally by InPlay, weekly** — SR doesn't compute season win probability (futures aren't tradeable/updated); Edwin helping automate | [[market-maker/open-questions]] E13 · [[market-maker/parameters]] | E13 method resolved |
| 7 | **Off-field = Edwin's popularity-index value** (~$14–30 range; Dallas ~$30, Carolina/Arizona ~$14), static at start, already in the NFL IPO prices | [[market-maker/open-questions]] E2 · [[market-maker/parameters]] | E2 substantially resolved |
| 8 | **Weekly Wednesday data drop:** Edwin/InPlay deliver the updated off-field metric + remaining-game win probabilities every Wednesday, plugged into the algo | [[market-maker/decisions]] · [[market-maker/parameters]] | New operational cadence |
| 9 | **Betting-feed parity requirement** — probabilities must not lag DraftKings/FanDuel or the MM gets picked off; Cody owns getting the feeds | [[market-maker/open-questions]] · [[market-maker/plan]] Phase 0 | New item, InPlay-owned |
| 10 | **Queue position answered (T8.1):** replace = cancel + new order at the back of the queue (tZERO call earlier that day + Troy: standard on every matching engine); Edwin: "we don't care about that" | [[market-maker/open-questions]] T8 | T8.1 resolved |
| 11 | ⚠ **v1 crossing tolerance:** Edwin — "on the first iteration, if we have to cross in order to make the adjustment in price, I don't care"; use cancel-replace. Exact sequencing he rejected is ambiguous in the transcript | [[market-maker/decisions]] | Pending George's confirmation of the reading |
| 12 | **User wash-trading policy:** rulebook prohibition + order-query on high-volume accounts + removal from event; Troy checking what self-match prevention tZERO employs | [[market-maker/systems/market-supervision]] · [[market-maker/open-questions]] | New T-item |
| 13 | **IPO buyer role firmed + sequencing signal:** MM buys at every IPO when buyers are short / to balance shares pushed into the market; Edwin wants to "start with the IPO"; fuller session promised | [[market-maker/decisions]] · [[market-maker/plan]] | To capture |
| 14 | **Edwin sending the original MM simulation Python files** ("functional, not a heavy lift") | [[market-maker/open-questions]] E4 | In motion |
| 15 | **Testing via SR simulation games** — replay a past game in a ~4-hour window instead of waiting for preseason | [[market-maker/plan]] | Testing approach |
| 16 | **v1 simplicity mandate** — "really simple to start", augment over the next couple of months | [[market-maker/decisions]] | Tone-setting for v1 scope |
| 17 | E11 + E12 never asked; George emailing the anchor doc to Edwin for review; another MM call expected | `sessions/` note | Session note to write at extraction |

### Other findings

| # | Finding | Destination | Action |
|---|---------|-------------|--------|
| 18 | **App live on the Apple App Store** as "InPlay Challenge" (now first search result); OTA updates rolling: education videos <2 min, IPO prices in, colors updated, **house ads live in app**, NCAA placeholder-data bug being fixed | [[whats-new]] · [[components]] Advertising | Milestone + one-line house-ads note |
| 19 | **5x referral launch-week bonus live**; team leaning yes on repeating it for the Android launch | [[referral/referral]] | Bonus Campaigns update |
| 20 | Google Play listing pending screenshots + a frozen build (Hasan → hand back to Troy) | — | Action item |
| 21 | **Non-US / no-KYC app variant exploration** — international students need access without KYC; "function that forks off" idea; George assessing feasibility | [[customer-onboarding/customer-onboarding]] | Component update + open question |
| 22 | **KYC objection handling:** users uncomfortable giving ID → "Why is this required?" popup/tab at the Persona step (bullet points or AI-clone explainer); messaging: reputable third party, legal/IRS requirement, W9 only for winners; Jared researching how other apps approach it; monetizable no-KYC layer floated | [[customer-onboarding/customer-onboarding]] | Registration+KYC update |
| 23 | ASO research (Cody — Apple keywords vs Kalshi/Polymarket, Brett sync offline); newsletter + socials going out; repost to stories (Skye) | — | No action |

---

## Follow up with Market Maker - 2026/07/23 14:32 BST – Transcript

# Attendees

Brett StClair, Cody Haugen, Edwin Johnson, Gary Anderson, George Westbrook, Hasan Ahmed, Jared Sapirman, Kevin Murray, Max Kingaby, Skye Capazorio, Troy McDonald Kane

# Transcript

Brett StClair: Hello everybody.

Cody Haugen: Good morning.

Troy McDonald Kane: Yeah.

George Westbrook: How we all doing?

Kevin Murray: How are you?

George Westbrook: Good. Don't I've been yesterday when the app came out, I was looking on the app store and I was like, where is it? I was like, what's going on? I thought it's live, but obviously it's not US-based. So, did And…

Kevin Murray: Yeah, even when we looked up in play global, we couldn't find it. So obviously then I think it was Troy that said it's inplay challenge. So we managed and

George Westbrook: then when you type in inplay challenge, is it the first one that comes up?

Troy McDonald Kane: It is It wasn't yesterday. When I typed it in today, it was the first thing to pop up.

George Westbrook: Okay. Yeah.

Troy McDonald Kane: Yesterday was third or fourth down, but I'm sure it will take a few days for the algorithm readjust, but I mean majority of people are going to be directed to it from a QR code or…

Troy McDonald Kane: from a link, but at least it did this morning when I checked because my understanding, Hassan, no updates have been pushed out yet. Is that right?

Cody Haugen: No, son.

Cody Haugen: You can speak to it. I'm sorry.

Hasan Ahmed: At the moment I'm doing a few actually the OTAA pushes cuz it was quite an old build and so there's quite a lot of changes and then I'm slowly pushing them out now as in terms of the IPO prices.

Hasan Ahmed: There was a slight thing bug with NCAA as in cuz it has placeholder data but I'm taking that now and then everything else is also in there. So, I'm not sure of all the specific changes, but I think education is updated.

Cody Haugen: Yep. I'm looking through it now.

Hasan Ahmed: Yeah.

Cody Haugen: Learning center module one.

Hasan Ahmed: Okay. Yeah,…

George Westbrook: Yeah, I've got the list for us to check again.

Hasan Ahmed: I've got the

George Westbrook: side. That's this.

Cody Haugen: Yeah, the education the video is still a minute 45. I can't remember what it started at. Is it a minute 45 the first version? I can't remember what that

George Westbrook: I think first version some of them were 5 minutes. So now they're all under two minutes.

Cody Haugen: Okay, then education is updated.

Cody Haugen: The IPO prices are in there and the colors are updated. the…

George Westbrook: House ads.

George Westbrook: Are they in there?

Cody Haugen: what yeah,…

George Westbrook: The h house ads fence.

Cody Haugen: that's right. The house ads are in there. Great work everybody. appreciate that help late night and getting that pushed through this morning. Hassan and George and Max and everybody Yeah.

Troy McDonald Kane: Yeah.

Troy McDonald Kane: There it is. All Great. Awesome. So, we should be good then, Cody, to send out the newsletter and get the socials, updated today.

Cody Haugen: Yeah. I just I mean

George Westbrook: Five extra referral was live as well,…

George Westbrook: wasn't it? Yeah. if you go to the home page, you should be read that.

Skye Capazorio: Kevin, on the social side, just when you do it, I would suggest that you repost obviously whatever the post is, repost it to stories because that will then make sure that the followers get to see it in a higher quantity.

Kevin Murray: Yep. Perfect.

Kevin Murray: Yeah, I've got all the different posts as well and…

Skye Capazorio: And…

Kevin Murray: different sizes for the different platforms.

Skye Capazorio: 

Skye Capazorio: okay, Amazing.

Cody Haugen: Yeah,…

Cody Haugen: I see that bonus launch week 5x is on.

George Westbrook: Let's f*** go.

Cody Haugen: Yeah, I love it, Absolutely.

Kevin Murray: That's just one thing I was thinking about there this morning obviously for that that's for Apple…

Kevin Murray: but for the Android when that eventually pumps out should we do 5x for that one as Yeah.

Troy McDonald Kane: Yeah. Yeah.

Troy McDonald Kane: And then on that Hassan, I was looking at the Google Play console and it looks like they're just waiting for us to put information to get it listed.

Hasan Ahmed: I think at the moment I just need to dash with the screenshots and…

Hasan Ahmed: then I build for it and then I can hand it off. It's just cuz there have been a lot of updates and so I need to choose as a specific actual build and so I don't want to do one and then we make more updates and then Yeah. Okay.

Troy McDonald Kane: Okay.

Troy McDonald Kane: Let me know when you want to hand it back over to me and we'll complete that. Thank you.

George Westbrook: I think…

Troy McDonald Kane: Great work.

George Westbrook: what else is There's 5x referrals done. And then it's just thinking about the non- US citizen version and…

Kevin Murray: I have done.

### 00:05:00

George Westbrook: the no KYC version as well to see how feasible and how quick that is to do.

Edwin Johnson: What's up, Paul? Sorry I'm late.

George Westbrook: How we doing?

Edwin Johnson: I'm doing good. It's been a morning, so appreciate that. all right.

Troy McDonald Kane: and updated.

Edwin Johnson: So, the app is released. I mean, what the f***?

Cody Haugen: and updated.

Cody Haugen: What the f***?

Edwin Johnson: And Who's responsible for that update?

Cody Haugen: And updated.

Edwin Johnson: Hassan the beautiful. f***.

Cody Haugen: Everyone was working late.

Edwin Johnson: Amazing. Thank you so much. I mean, I don't know if you guys are excited, Brett. You look like you're ready to cry. I don't know if that's joy or sadness, but nah.

Brett StClair: I know how much effort's involved in the market. That's what keeps me up at night.

George Westbrook: All right.

Edwin Johnson: Nah, the market maker is not that hard.

Edwin Johnson: It's really not. We go.

Brett StClair: I think concept of delivering technology will happen through stuff today…

Edwin Johnson: Will you sure?

George Westbrook: The architectures.

Brett StClair: our thinking what we think and how it needs to grow. we think I'm hoping the architecture is like so we just a bit worried it is the thing that's keeping George and…

Edwin Johnson: Yeah. I wouldn't put a ton of sweat into worry on this one. This one it's going to be much easier than you expect. it's a rinse and n

Brett StClair: I more so George he's written about 15 algorithms and approaches and architectures on our glass windows. You probably see shitloads of oros.

George Westbrook: because it's not so much the algorithm…

George Westbrook: because I agree with you Edwin obviously it is what it is like it's an algorithm it's the stuff around it like consuming the data then the speed at which we need to do it and…

George Westbrook: then taking into account latency it's moving forward I think it's just initially for all of us looking at it it was a new thing and we're like h

Edwin Johnson: I get it.

Edwin Johnson: I get it sounds so glamorous market making. it's a blue collar way to make a lot of money. it's not like one market maker is better than the other. I mean, they all price the same things basically. One's generally faster and the other one can handle more inventory,…

Edwin Johnson: I mean, what do you think, Give your McDonald key.

Troy McDonald Kane: I mean,…

Troy McDonald Kane: one thing I will say, and I was saying this to the Novo team the other day, is that the formula is like you're a trader, Edwin, so in your mind, it's easy. But when you have to build it from the back end, it's actually not easy because there's a lot of edge cases that you have to account for. There's a lot of components. And I remember at Citadel the quant researchers would be like why can't you build it this way? And it's like it can't work that way. The exchange doesn't operate that way just because you simulated it that way it's not going to react that way. So I think that's why you don't see dozens of market making firms being created every year is that the technology on the back end actually is the hard part. Yeah.

Edwin Johnson: For our use case though, I don't think it says …

Troy McDonald Kane: No, I mean in this environment it's not latency is not a factor and there shouldn't be too many edge cases here.

Edwin Johnson: no. But,…

Troy McDonald Kane: Yeah. It's my formal name so it's real. Yeah.

Edwin Johnson: boy was I excited when I got the news from Troy McDonald game. I love that McDonald's, by the way. I hope you own a piece of that company. It does It is real.** Hey, that's a great name. Jesus. I mean, George, I don't want to go down a rabbit hole. But if you were going to start making pornography, I think you'd have to have that name as an actor. Sure. Much better than a Gary Anderson.

Gary Anderson: Complain everybody.

Edwin Johnson: Yeah. …

George Westbrook: Yeah, maybe we do a vote at the end.

Gary Anderson: That's like Bill Smith,…

George Westbrook: Who's got the most

Gary Anderson: .

Edwin Johnson: I know Brett Sinclair is the lover of all. I mean, that's the best. I mean, Edwin Johnson,…

Troy McDonald Kane: Hello.

Edwin Johnson: 

Edwin Johnson: they're like, "Cue the black guys." And I'm like, but that's So, all right. Is there anything we need to catch up before we get into the market Thank you.

Cody Haugen: I guess just real quick offline, Brett, if you could catch up with me on Apple optimization. I've been doing some digging and if that's valuable. It seems pretty lowhanging fruit. as far as the cost of it and the app in the app store and actually advertising it and getting it all the keywords basically eventually trying to steal search optimization away from Kelshy and…

### 00:10:00

Cody Haugen: Poly Market and s* like that within the app store.

Brett StClair: within the app store.

Brett StClair: Yeah. Yeah,…

Cody Haugen: Yeah, I've been doing some research on it last night and others and I don't know. I just want your input on it. Cool.

Brett StClair: we can grab some time. So, we got a bit of a fix a hard stop at the end of this.

Brett StClair: But we can pick up probably an hour later after that.

Edwin Johnson: Okay, cool.

Brett StClair: That's okay. Someone's coming into the office.

Edwin Johnson: No problem. Anybody important?

Brett StClair: George's No, I'm kidding. No, no, that she's not important. George, he hates it when I don't do mom jokes.

George Westbrook: I'm ready to throw something.

Brett StClair: Should we get into the market?

Edwin Johnson: Okay, cool. Yes.

Brett StClair: I'll pop some in your diary, Cody.

George Westbrook: So I suppose there we've got so back…

George Westbrook: what are we doing first it's understand the algorithm what's happening at each stage where we're seeing some of the complexity is the technical architecture so obviously this is something it's not like every 10 seconds or every minute or even every five seconds that this is happening. It's across all 160 teams simultaneously taking in all of the market state for all of them and then doing that and then cancelling orders then replacing orders because I think one thing we learned from tZERO today which is a bit annoying and I don't know if this is how it would typically function in the market is that obviously every time there is a new cycle let's call it for the market maker all of the old orders need to be cancelled and then recreated with the new orders that the market maker

George Westbrook: One of the ways that we were thinking about doing it is updating in place. So, let's say there was a 500 500 bid at $6. and it was partially filled, so 250 were filled. the new market maker says, "Right, we're going to do a new quote for 500 at six again." so what we would do is take the 250 that is not filled and then basically take the difference between what's been filled, what's not been filled, and then get it back up to 500.

Edwin Johnson: Let me stop you right there. So, that's more complicated than it needs to be.

Kevin Murray: S*. Oops.

Edwin Johnson: We're going to make it really simple to start and we can augment the market maker, as we iterate over the next couple months. It's going to be very very simple. first I think we're going to start with the IPO when I discuss how I want to do that because Mark Maker is going to be a buyer at the IPO for every team in the event that we don't have any buyers or we're trying to balance up how many shares get pushed into the market so we have an even balance. So, we'll talk about the idea in a second, but firstly in this example, if you're bidding for 500 at six, and your 500 if you're 500 bid for six is you get partially filled and…

George Westbrook: So you Okay.

Edwin Johnson: you're never going to refresh that bid until it's completely gone. So, you leave the resting order of 500. it trades down. they hit the bid. You've got, 100 left, 87 left, 55 left. You just leave it until it's gone. And then once it's not gone, okay, let's say, for example, you were, resting 500. Now it traded all the way down to 27 lots at six. But now the update says you got to go to the next best bid is going to be eight.

Edwin Johnson: Okay, we're going to randomize that front lot order first best of bid So, we're gonna essentially move up and we're going to cancel the top of book bid at 6 and now we're going to be, resting 382 at 8. So, we don't have to do any we're not refreshing at a price just because we want to keep a bid at six if they're sold for example okay and we do the call and we get the call and says okay we should be at top of book six and we get filled and the next call says top of book six we can reload at that top of book or if the price changes which is going to be more likely than not then we'll reload Mode it the next time.

Edwin Johnson: top of book. We'll just use a randomizer…

### 00:15:00

Edwin Johnson: which is very basic by the way. That's not hard to do, so that the numbers don't look like it's programmatic into who's at the top of book. Okay. Correct.

George Westbrook: and…

George Westbrook: the randomization would come in both price and quantity. so the price is a thing that's purely algorithmic with no randomization with the bid offset base spread blah blah blah it's the quantities that are going to be randomized is

Edwin Johnson: We're going to get the reference price but the quantity of resting orders. That's correct. That's right. And then when you're doing the calls, okay, so let's break it down again. when we do calls for updates, you're not going to have to do all 170 every minute of every day. We're going to lower the Come on, m***********.

Edwin Johnson: We're going to lower that burden. So, we're only going to do calls for games that are being played instant. so if there's a schedule, we'll put in the schedule. 49ers play the Chicago Bears on Thursday night.

George Westbrook: Okay.

Edwin Johnson: You're going to be updating that call all, the entire game. But when games are not being played, we can do the call every minute or 30 seconds or, it's okay. So, we don't have to burn so much. Because, if we get filled, okay, we'll get a fill and then we'll write some logic based on if you get a fill, what do you do next? So, if the game's not being played, and you're 500 bid at six and you get filled at six, and says, " you should still be bid at six, but we've got bids at five, four, and three." we may just leave that and see if we get filled all the way up. So, we can work through that logic.

Edwin Johnson: We don't have to call every game every second like that, Just the ones that are being played because that's where you're going to see the majority of the trading action. during the earnings reports, we will have to call all of them for about five minutes.

Edwin Johnson: That's about it. And then once that's done, the number's over and it's awesome.

George Westbrook: And that would be the so and…

Edwin Johnson: Tuesday for NFL, Wednesday for NCAA football.

George Westbrook: the not in game that would be the MIP market operating profile.

Edwin Johnson: Yeah. I mean, is that what I wrote? The MOP?

George Westbrook: Yeah. Yeah.

Edwin Johnson: Yeah. I mean, I've tried to make it more for a lay person, so I've written more here, and we'll go through that next, but don't fret about too many of the calls and the over 170 symbols being called every second.

Edwin Johnson: We can bifurcate it to just when the games are being played and lessen the load at least in the beginning,…

George Westbrook: Okay. Yeah,…

Edwin Johnson: If we feel that we need to do more, in late September or whenever we can augment.

George Westbrook: because I suppose that was where we saw it before if it was five times a second. So every 200 milliseconds is the schedule for doing let's say a run of the market maker across all 170. And then there's the other triggers which are new reference price game event blah blah blah and the other ones that was

Edwin Johnson: You don't have to reference the The game events are always going to be like we're going to get the reference prices and…

Edwin Johnson: they're already going to compute all things that happen in those games. So the probability factor that we're going to pull from sport radar, okay, and that'll work in the beginning. We can augment again later, the probability for the game for the games that are being played.

George Westbrook: Mhm. So yeah,…

Edwin Johnson: They're going to be your first source for that game's value. And then we're going to add on the rest of the season's value and the potential field revenue. Yes.

George Westbrook: the ESV is onfield plus Onfield is expected. So before a game, let me look all of the games of the season expected win rate times by is it 5 per win? $5 per win.

George Westbrook: And then when an ingame, so then let's say we're game. When an event happens, that's most likely going to change the win probability of that team or the two teams in that session, which would require a new ESV to be calculated. And then the market maker run, it would copy over the ESV as the reference price,…

George Westbrook: then do that. So it's okay. That's So we'd have a schedule of let's say every minute during game and on top of the trigger based recalculation. Okay. Okay.

Edwin Johnson: You're probably going to be closer to every 200 milliseconds during games per call.

Edwin Johnson: Yeah, a second's too long.

### 00:20:00

George Westbrook: Okay. And then Yeah.

George Westbrook: Right.

Edwin Johnson: and Cody,…

George Westbrook: Sylvester. So,…

Edwin Johnson: we got to figure out, we got to make sure that we're getting those betting feeds, whatever we got to do to get those so that we are on par with the DraftKings and FanDuels. That's a critical piece because the probability cannot lag. Otherwise, we're going to get picked off on the market maker. It's too easy for people to make money.

George Westbrook: I suppose we'd need to create a win during a game.

George Westbrook: we'd need to create some sort of algorithm to count the potential win probability based off of the available data. So let's say there was sports radar just to start.

Edwin Johnson: No, you don't have to create it.

Edwin Johnson: You just pull sport radars probability in. That's what we're going to use to start.

George Westbrook: So it' just be one call with one number

Edwin Johnson: 

Edwin Johnson: And one column with one number plus our rest of the season outlook.

George Westbrook: in. Yeah.

Edwin Johnson: Okay, and the off field metrics. So I'll write the formula. Okay, it's fairly simple. Okay, and it changes game by game, Because when you're trading options, they converge towards the date. So this works the same way. when there's 17 games available, you'll have more opportunity. But if there's only one game available, that reference price versus this game is going to have the most impact.

Edwin Johnson: There's no other games that are possible to affect the price of that share. So, as you get closer to the end of the season, it's going to be very close to the probability of that single game outcome for onfield plus what we do with offfield.

George Westbrook: And at the moment,…

George Westbrook: what's the way that we're going to let's say when we start it's everything that we've got today. What's going to be the mechanism to calculate the off field?

Edwin Johnson: I don't know if I shared this yet, but basically we have a popularity index, how many people go to the games, how many people buy s*** from different companies, and we ranked them, and I gave an off-field value to the professional teams. I think it's incorporated in those NFL prices that are up for IPO. And there's a pretty big variance with off-field.

Edwin Johnson: The off-field I think was on the low end 14 bucksish and…

George Westbrook: And is that static or…

Edwin Johnson: on the high end around 30 bucks. So Dallas I think was 30 and I think Carolina or some I don't remember the other team maybe Arizona somebody had around 14 bucks of off-field revenue allocated towards the projection.

George Westbrook: how much would it change during the season if it's not?

Edwin Johnson: It's going to change and it's going to change for a couple of reasons. It's going to change generally speaking if a to win. more people start to bet on. The only other thing that happens is when the team has either traded for or drafted a star player because even if they sink, people want to watch them. if people want to watch them, then they may start to trade that side of the team and increase their popularity. So, the Chicago Bears have been pretty s**. but we have a really good quarterback now and we've done better than we have recently and…

Edwin Johnson: he's relatively popular here. So even before they started to win, people were starting to take notice that he was a good player. And so the awareness and whatnot comes in.

George Westbrook: So I suppose with so initially offfield is going to static,…

George Westbrook: but in time what we're going to need to do is have a way for an event happening,…

George Westbrook: not an outofgame event. So, let's say somebody's injured, somebody's transferred, blah blah blah. Because would sports radar if somebody drafts a new player or somebody's injured change the win probability for the season automatically? Yeah.

Edwin Johnson: Correct. Yes.

Edwin Johnson: They don't calculate the win probability for the season. They're going to calculate the win probability for a game. they may have what's called overunders,…

George Westbrook: Good night.

Edwin Johnson: which we're trying to get from them for college football. Those can change, but generally speaking, that's not a target that gets traded or bet on intra season. It's generally like they call them futures, which is I think the Bears are going to win more than seven and a half games or less And you can bet on one of those sides. The problem is you cannot trade those throughout the season. and it becomes a singleshot bet and so they don't generally update the win probability or totals of a season. That's something we will do internally and I can help with that we can automate the process but we'll have our own weekly essentially balance and then we can modify what the market maker sees and how it starts to bid ask and that variability is going to be exciting because it'll create great change.

### 00:25:00

Edwin Johnson: Later, Max and I keep it real.

Max Kingaby: We'll see you guys in a bit. Have a good rest of your day.

Edwin Johnson: Thank You two,…

George Westbrook: Yes.

Edwin Johnson: does that make sense George? Yes,…

George Westbrook: So, each game is going to have a probability of one person winning and another person winning. But if let's say the Giants were playing the Bears and the Giants star quarterback gets injured, the win probability would change or it wouldn't change?

Edwin Johnson: of course it'll change. Especially if it's …

George Westbrook: It would change. Okay. If it's not in game,…

Edwin Johnson: here, let me write that wrong. If the Giants are winning 35 to nothing in the fourth quarter with two minutes left and the quarterback gets hurt, the win probability is not going to get hurt. I'm sorry, the win probability is not going to change. If it's early in the game and the score is 000, the win probability is going to have a magnificent change. So, a lot has to do with the time left in a game, the time decay.

George Westbrook: if it's outside of a game happening and…

Edwin Johnson: If it's outside of a game happening, then it'll affect the future game.

George Westbrook: Okay. Yeah.

Edwin Johnson: Yeah. Yeah,…

George Westbrook: That's good.

George Westbrook: So what one of the things we probably need to do is how that would work out how that would affect the off-field performance.

Edwin Johnson: I mean the off-field stuff I'd probably just say, "Look, we'll probably have a day before the games start, maybe on Wednesday, where I provide an updated field metric that we can just simply plug into the ALGO and that it's updated weekly. We can handle that number for you." So, we can provide Okay.

George Westbrook: Okay, perfect.

Edwin Johnson: And then, we can also more likely than not provide the rest of the season probability win total. also, so the thing that the market maker is going to do is going to take that input the other off-field input that we'll give on a Wednesday. The win probabilities for each of the remaining games, we can give that on Wednesday. And then you're calling the live probabilities during game and then you're adding these other components into it to make the price. Yeah. Boy,…

George Westbrook: Okay. …

George Westbrook: what's the one triggers?

Edwin Johnson: do you got anything on that? You upset with that? You like that?

Troy McDonald Kane: No, it makes sense.

Troy McDonald Kane: Yeah, I would chime in if I disagreed. Yeah.

Edwin Johnson: Okay, cool. Thank you.

George Westbrook: I think somebody said did you have an old for one of the previous simulations did you have a script that you were using for that would you be able to send that over when you got a second…

Edwin Johnson: Yes. …

George Westbrook: if that's right one other thing as well is I'm assuming obviously we talked about the cancel and…

Edwin Johnson: yes. Let me do that. Let me see if I can find Market Maker. let me see.

George Westbrook: replace mechanics. I'm assuming we'd need to monitor when the market maker creates a new set of quotes,…

George Westbrook: if some of those quotes are the market's crossing that it would cancel the ones that were crossing the previous ones. Is that fair to say?

Edwin Johnson: Say that again.

Edwin Johnson: I got confused on that. Try one more time.

George Westbrook: So in order to avoid crossing markets, if the market makers not automatically cancelling all of its old quotes and the ones that were previous and not filled are staying there, if it was to submit new quotes and…

George Westbrook: some of those old quotes would mean that the markets would cross, it would automatically cancel those old quotes and only publish the new ones.

Edwin Johnson: Yeah,…

Edwin Johnson: I mean look we call that wash trading at times it's almost unavoidable okay because generally new orders are faster than cancels believe it or not so yeah I mean a lot of my life got messed up by wash blockers. So, yeah, it's a technique. but on the first iteration If we have to cross in order to make the adjustment in price,…

### 00:30:00

Edwin Johnson: I don't care.

George Westbrook: Because one thing we could do…

George Westbrook: which once again is a design decision is instead of so in order to do that cancel and then replace we'd have to so market maker runs outputs the new quotes we can either post the new quotes first and then cancel the old ones after and then it be crossing or cancel the old ones first, wait till we receive confirmation that they've been cancelled and then post the new ones, but then that would mean in one market maybe there's less quotes that are needing for a few milliseconds. Which one out of those cases would you say is better or worse?

Edwin Johnson: I'm sorry. I got distracted trying to get your thing here.

Edwin Johnson: I have a fatal flaw. I can't multitask at all. And everyone gets very frustrated with me. So, please forgive me. One more time. And I just want to get you this market maker file, but go ahead, sir. wash. Yep.

George Westbrook: So with the cancelling of old orders and…

George Westbrook: the potential problem of it being crossing markets, two approaches are one, so the market maker

George Westbrook: create those fresh quotes are sitting there ready to be submitted to the order book. we can either post them to the order book and then they'd be potentially crossing markets from the old quotes that haven't been cancelled yet and…

George Westbrook: the new quotes that are sitting there. Or we could flip it so that when the quotes are ready, we first have to cancel the quotes that would cause a crossing of the market then post. And you don't want that.

Edwin Johnson: Yeah, I don't want that.

Edwin Johnson: Yeah, I don't. So, Troy and George, reach out to tZERO and find out if they support an order type court called cancel replace.

George Westbrook: They do one of the not issues cancel and replace would mean that let's say there's 100 items in the queue. there's an order that's at number 10.

George Westbrook: If we do cancel and replace rather than replacing…

George Westbrook: where it is they said they don't natively support it.

Edwin Johnson: Yeah, we don't care about that.

George Westbrook: So effectively behind the scenes it is first a cancel and then a new order that goes to the back of the queue.

Troy McDonald Kane: Yeah. And that and…

George Westbrook: Okay.

Troy McDonald Kane: and by the way, George, that's common practice on just about every match engine. So that's not unique to tZERO. So yeah,…

George Westbrook: 

George Westbrook: Yeah. I think I was battling with Claude about that last night and I was like but then

Troy McDonald Kane: so that's where the matching logic tends to, …

Troy McDonald Kane: be a little backwards maybe,…

Edwin Johnson: Vulnerable. what's interesting about that order type is it actually creates two functions.

Troy McDonald Kane: I guess. but yeah,

Troy McDonald Kane: And the intent is that is because it's an updated order, it has to move to the back of the queue.

Troy McDonald Kane: Yeah. Yeah.

Edwin Johnson: …

Edwin Johnson: if people are doing really low latency and they're leaning on an order book, which we're not having, but just for knowledge, it's a technique you can do to jam the market, the OC because if I do let's say I'm bid for fives and everyone joins my bid for fives and sell I bid because I want to sell. then they join me and I cancel and I sell simultaneously.

Edwin Johnson: They don't get an update that the order has been cancelled till they've been filled on the sale.

George Westbrook: I Yeah,…

Edwin Johnson: So it's a trick that's Unbelievable.

George Westbrook: I think I'm Yeah.

Troy McDonald Kane: And there's another trick…

Troy McDonald Kane: which I will not spend too much time on, but what the other trick that these market makers will do is that they will do impartial packets. So they'll send parts of the information to raise action first and then they'll follow up with completed information once they get their queue placement. there's the amount of what we would call shenanigans that happens. I won't stress you out on it but it's not at play here yet.

Troy McDonald Kane: It will when people start getting API access.

George Westbrook: Did you say it was self wash or self

Troy McDonald Kane: But one thing I need to check in on Edwin is…

Troy McDonald Kane: what type of self-match prevention tZERO employs if we want to block wash trading.

Edwin Johnson: Yeah, I think that we're going to have it in the rule book that we're going to say it's not acceptable.

Edwin Johnson: And then if we see someone with high volume, we'll just run an order query on it and…

Edwin Johnson: see if they're blocking. And if they are, then we're going to take them out of the event.

Troy McDonald Kane: It's called selfmatch prevention.

George Westbrook: Cuz I think self.

Edwin Johnson: Cool. Yes.

Troy McDonald Kane: And there are mechanisms that matching engines utilize to mitigate wash trading. It's usually an in feature.

### 00:35:00

Troy McDonald Kane: So you have to set it,…

Troy McDonald Kane: but a lot of exchanges require you to set it in their policies because the regulators have very strong opinions about wash trading because they think it's tied to moneyaundering or they think it's tied to manipulative trading practices.

Edwin Johnson: If it's used…

Edwin Johnson: if it's used the right way…

Troy McDonald Kane: If it's used the right way, it can be very Yeah.

Edwin Johnson: 

Edwin Johnson: if it's used the right way. it's not bad if wash blockers can be used very predatorily like they can be brutal.

George Westbrook: Yeah, because I definitely remember talking about this to Claude yesterday. So pix don't respect whether Self trade prevention instructions would normally live. It's not currently supported. MS account spec. Yes, there's a per account wash trade block toggle and asks were already filed to enable it on the user account. Okay, I'll look into that. okay.

George Westbrook: I think what might be hand is if I send this over to you, Edwin, and if you just have a quick skim through to see if any of this that we've got in here is a load of bollocks or it's

Edwin Johnson: Can you email it to me?

George Westbrook: Yeah. and then because this is one of the things we're using kind of like an anchor to understand as well as the other documents you sent and…

Edwin Johnson: Cool.

George Westbrook: it's really really helpful. and then along with this we'll be mapping out the more technical stuff. but I think we were saying on the tZERO call that what we can do is with Sports Radar, they provide the simulation games that we can use.

George Westbrook: So rather than having to wait for an actual game to happen, and then testing the market makers thing in real time, for the preseason game, what we can do is just set a 4hour period…

George Westbrook: where we're like, this game that happened a year ago, what we're going to do is we're going to just simulate it on that and see how it functions.

Edwin Johnson: Okay.

George Westbrook: Perfect. I think me and I've got to hop off onto that call that Brett and Max were on. I think what will happen is ll away. We'll have a further investigate,…

George Westbrook: get some stuff tested and almost certainly probably going to require maybe another call at some point. if that's all good and then yeah, we'll get going.

Edwin Johnson: 100%. Yeah.

Edwin Johnson: And I send me what you can. I'm going to get you the Python files from the original market maker that we used in that simulation.

George Westbrook: Mhm. Yeah.

Edwin Johnson: Again, it was functional. It was not a heavy lift for the purposes of this, Okay, You guys bolt. Hey, inplay team, can we stay on for two seconds?

Kevin Murray: Yeah.

Troy McDonald Kane: Yeah. Yeah.

Edwin Johnson: right, cool. All right,…

George Westbrook: Perfect. Right.

Edwin Johnson: see this.

George Westbrook: Speak to you.

Hasan Ahmed: to Speak to you guys tonight.

George Westbrook: Speak to you guys tomorrow.

Edwin Johnson: Thanks, Really appreciate that work last night.

Edwin Johnson: George, too.

Hasan Ahmed: Let's f*** go.

George Westbrook: Let's f*** go.

Edwin Johnson: Got a boy.

Hasan Ahmed: Let's go.

Edwin Johnson: You, Okay,…

Hasan Ahmed: I see.

Edwin Johnson: yeah, I got a question for you. I've had a number of people come back and be like, I'm uncomfortable giving my ID. I'm like, if you want cash, people got to know who the f*** you are. people aren't weird.

Troy McDonald Kane: they've never signed up for a or a trading account. I mean this is not an unreasonable ask if you want to your point Edwin to enter a trading competition that gives out cash prizes. absolutely.

Edwin Johnson: I mean, I don't think it's legal for us not to know who we're sending it to,…

Troy McDonald Kane: It definitely is not legal to Yeah.

Edwin Johnson: I mean, you talk about money laundering and…

Edwin Johnson: be like, " yeah, Kevin from, Omaha, he's* moving weed and s*** and it's very strange."

Skye Capazorio: It's an audit trail requirement,…

Skye Capazorio: too. if anybody ever wants to audit the competition and where it went and who the money went to and stuff like that, they've got to be those checks in places. But I think a lot of people are just sensitized to that on a global scale because of all the various conversations that are going on globally about, people control and movement control and therefore, it's a huge thing in the UK at the moment.

Edwin Johnson: Yeah. Wait,…

Kevin Murray: Yeah. But my thing as well is …

Troy McDonald Kane: I mean what I would sorry real quick…

Kevin Murray: if you go ahead

Troy McDonald Kane: what I would say I don't know who these people are. they're probably of a certain age. But what I would say is that just say that Persona is a wellreputable KYC platform that is trusted by dozens…

### 00:40:00

Edwin Johnson: wait. Yeah.

Troy McDonald Kane: if not hundreds of online trading apps, sports apps. if that gives them any reassurance that it's not like we're storing it.

Troy McDonald Kane: It's an independent party that is reputable that provides these services to everyone that does a trading app or some sports betting app.

Edwin Johnson: Yeah. I mean, I think that there's going to be to Jason's point yesterday, I think there's going to be this layer of d******* where they're going to take my DNA. we've all met that guy, …

Troy McDonald Kane: I don't know a sports betting app that you don't put an ID in to get access.

Edwin Johnson: what I'm saying? No, you can't. You can't.

Troy McDonald Kane: So, it's or a brokerage account as well,…

Edwin Johnson: You got to put your banking information when you go to bedding app,…

Troy McDonald Kane: Yeah. And your social security number. We're not asking for social security numbers.

Gary Anderson: 

Troy McDonald Kane: We're asking for date of birth and addresses. That's it.

Cody Haugen: Not yet.

Edwin Johnson: right? Yeah,…

Cody Haugen: If you actually want the money, yes, we will get that.

Troy McDonald Kane: Yeah. Then they'll get a W9 form that they have to fill out.

Cody Haugen: Yeah. Yeah.

Troy McDonald Kane: But yeah.

Cody Haugen: I mean, I don't know. I see it as more of an outlier in our user base than the masses.

Troy McDonald Kane: Yeah. Yeah.

Cody Haugen: The masses are going to what you guys just said. They're going to be used to it. They've done it before.

Cody Haugen: We can't make any adjustments. So, yeah.

Edwin Johnson: no, no, no, no, no, no.

Cody Haugen: So I mean I think it's and…

Edwin Johnson: 

Edwin Johnson: I'm not saying that. to Jason's point there may be a layer that we can monetize of these** who don't want to do the full commitment. Kevin, what were we gonna Kevin?

Cody Haugen: and we will. Yes. So

Edwin Johnson: 

Edwin Johnson: What were we gonna say? Yeah. Right. Right.

Kevin Murray: Yeah. No,…

Kevin Murray: what I was going to say is obviously with all the brokerage accounts and anything like that, you always have to put in your info. What another thing I was thinking of is we can use those AI clones. to maybe educate some people that, you're going to be going through Persona, who's a third party KYC company, similar to how you would do when you set up any of your brokerage accounts or betting gambling accounts, just to make it real f*** simple that people are understanding it that we're in play global are not storing your data. Do you know and…

Cody Haugen: Dude, these clones,…

Kevin Murray: you've got to do it as exactly? Yeah.

Cody Haugen: dude, they're going to do so much for us. These clones are going to do so much for us is what I said. Yeah. It's not a bad recommendation there,…

Gary Anderson: If we can do a …

Gary Anderson: where you go to put in the information if we can do a little tab that says why is this required and you hit it and the clone comes up and it explains that none of the funds could be distributed without this information. that's required by the IRS real briefly and then I think that might go a ways to put some people at ease. I don't know but it might be something we can just do simply

Edwin Johnson: Yeah. Yeah.

Cody Haugen: Gary. If…

Edwin Johnson: Gary from the smoke.

Cody Haugen: if put it in the smoke coming out,…

Edwin Johnson: Smoke is coming in,…

Cody Haugen: baby. I mean,…

Edwin Johnson: baby. …

Cody Haugen: if not a video, you're right. It should be a simple popup with, …

Kevin Murray: Look, disclaimer.

Kevin Murray: Come on.

Cody Haugen: just bullet points of why it's required.

Edwin Johnson: yeah, I think that's a good idea,…

Cody Haugen: Yeah.

Edwin Johnson: Okay, all right. we didn't get a ton done on the market making, but I think these guys will come around. I think that, when you look at the whole thing overall, I'm sure it's like daunting. they don't know what the f*** you're doing. But, when you put it into application, it's not that hard. So, Jared, without getting into the safety animals, I'm interested to know, will kids your age have problems giving the KYC information to get cash?

Jared Sapirman: potentially, but I'm also looking into different apps that do this currently as a research project to see how they approach it because they're

Troy McDonald Kane: But Here's the thing. Treat it production. they're all giving their** information to go on Kelshi. I don't care.

Edwin Johnson: Hey,

Troy McDonald Kane: They're going to give their information. We have to have it. we can talk about …

Troy McDonald Kane: why people don't feel sensitive to do that. But the reality is if you want to go and trade on something or get some cash payout, KYC is the standard in the industry.

Cody Haugen: Yeah, I did talk to Yeah,…

Troy McDonald Kane: not prohibiting hundreds of people signing up for Kelchi every day or hundreds of thousands of people signing up for Kelshi

Cody Haugen: exactly. Millions with the World Cup. Edwin and everyone else. on that George call yesterday though I did bring it up to him and a couple different variations of we need the code for the international students

Cody Haugen: and he said that was actually easier than the web app. But the web app is known by George and team now after yesterday's call that we do need a variation of someone needs to be able to get into the app without KYC whether that's a web app or a different version of the app that not a different version but a function that forks off basically.

### 00:45:00

Kevin Murray: Perfect. Yeah.

Cody Haugen: He's given it a thought and was going to come back to us. So we are absolutely

Troy McDonald Kane: Okay, real quick.

Troy McDonald Kane: I want to just stop the conversation because we're on the Novos which is being recorded and we have a team huddle in a little bit. So,'s I would recommend we just pick up these topics in our team huddle.

Edwin Johnson: Okay, sounds good.

Troy McDonald Kane: right.

Edwin Johnson: Novo listeners,…

Troy McDonald Kane: All right.

Edwin Johnson: congratulations on getting the app done,…

Edwin Johnson: It's out there and it's ready to party.

Troy McDonald Kane: Yeah. Give it to all your friends.

Troy McDonald Kane: We got the newsletter going out. We'll talk through that in a little bit.

Cody Haugen: Yeah.

Edwin Johnson: right, sounds good. Thank you,…

Troy McDonald Kane: All right.

Edwin Johnson: Troy. See you guys.

Kevin Murray: Thank you. Bye.

Gary Anderson: s***.

### Meeting ended after 00:46:02 👋

This editable transcript was computer generated and might contain errors. People can also change the text after it was created.

  
**