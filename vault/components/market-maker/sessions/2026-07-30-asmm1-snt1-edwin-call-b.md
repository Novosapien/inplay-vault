# 2026-07-30b — a second market maker arrives · the Edwin call · a process fix

> **Who:** George + Claude · call with Edwin
> **Type:** document intake / analysis / client call
> **Refs:** Edwin's SNT-1 email (30-07 am) · `inplay_algo_handoff_george.zip`
> (30-07, 14 files) · [[market-maker/asmm1-adoption-spec]] ·
> `call-questions-30-07.md`

## What we did

**Two new algorithms landed in one day**, both from Edwin, both as code.

1. **SNT-1** — a "Synthetic Noise Taker". A house account that crosses the
   spread at random so every book has activity from the IPO onward. ~350 lines.
2. **The handoff package** — 14 files, including **ASMM-1**, a complete
   Avellaneda-Stoikov market maker, plus RPV-1/RPV-2 (a reference-price layer),
   CFM-1, two harnesses, a calibration scaffold, and a 400-season Monte Carlo.

Read both. Analysed both against the v1.3 spec and our build. Produced
[[market-maker/asmm1-adoption-spec]] — six areas, a ruling on each — plus two
artefacts for the call.

**Then George called Edwin.**

## The call — what happened

**Edwin's opening position:** *"I think I've done the market maker for you, and I
think all you need to do is plug the code into T0 and it'll work."*

George explained why that is not the case, having checked first. The argument
that landed: **`quote(now, rp, inventory)` takes the reference price and the
share count as arguments.** His RPV-2 is the same — `step(now, fair_value)`. So
neither module computes either input. Our build is what computes both.

**Edwin accepted it.**

### The process fix — the most valuable outcome of the day

George asked for **short, concise, spec-style documents describing the
equations** — not code. He also raised the churn directly: three documents so
far, each changing things, roughly a week spent understanding the first before
the second arrived and moved it. Framed honestly — *"we want to move fast, but
this is not our area of expertise; give me a month and it'll be a lot better."*

**Edwin was fine with it**, and will rewrite the handoff package as a narrative
document that is easier to digest.

### What George also said

- SNT-1 is far less complex than the market maker — *"basically let's randomly
  buy and sell shares."*
- The market-maker change is an **improvement** and was acknowledged as one: the
  spread moves from a five-option lookup table to a real equation.

### Not asked, so still open

E29 (does ASMM-1 supersede §4.5/§5.2), E30 (is RPV-1 the published price or the
simulator), the compliance point on two house accounts, and the IOC problem.
These go into the next round — none of them are recorded as answered.

## What we learned

- **⭐ His two modules take the price and the position as arguments.** This is
  the whole rebuttal to "plug it in", and it is checkable in one line of each
  file. Everything downstream of it — Chapter 3, the feed reader, the SR path,
  positions, the journal, replay — is untouched by his package.
- **⭐ His width equation is genuinely better than ours, and we should take it.**
  §5.2 reads a spread off a table keyed on a state classifier **we never built**
  (N3's thresholds are still 🔴). His computes it from measured movement of our
  own reference price. No classifier, no new inputs, works in an empty book, and
  cannot be gamed by posting orders.
- **⭐ Volatility belongs on the width, not on the lean (George's framing,
  worked through).** The width is a risk control, so volatility belongs in it.
  The lean is a *distribution* tool (29-07). Vol-scaling a distribution tool
  means pushing hardest to distribute during a live game and least overnight —
  backwards — and it reaches the cap sooner, so it makes **N20 worse**.
- **His guards would break the market on morning one.** Past 6,000 shares in a
  live game ASMM-1 quotes **one-sided**. §4.1 says the opposite, and §4.1 is
  right for us because we are the mandated buyer. Run as shipped there would be
  no bid on any book.
- **His width has no wide end.** The σ² ceiling of 400 caps it at ~10 ticks
  plus the random 3 — about $0.13 on a $65 team, ever. §5.2 Defensive is $0.40
  and the indicated overnight spread is $2.50–$5.00. Worse: **a dead feed
  produces LOW volatility**, so the equation would quote tight into exactly the
  case §2.3 calls dangerous. Recommended per-state width floors rather than
  raising the ceiling.
- **Three of RPV-2's four additions are invented movement** — a random OU trend
  worth up to $0.80, a continuous random walk, and event jumps. His own header
  says why: *"the reference price sits still… RPV-1 makes RP MOVE… so the whole
  market breathes."* That is a simulator. And the event jumps are a substitute
  for a probability feed **we already have** — `x_g` already moves on every play,
  so adding them would double-count.
- **The fourth addition is the compliance problem.** RP would rise because
  someone bought, and on day one the house taker does most of the buying. One
  house account moves the published price; the other quotes against it.
- **tZERO has no IOC**, and SNT-1's entire order model is marketable IOC.
  Verified twice — the platform doc (22-07) and the OE FIX spec (23-07). The
  workaround (a marketable DAY order plus an immediate cancel) breaks SNT-1's
  own stated guarantee that it never posts resting liquidity.
- **SNT-1's `max_spread_ticks_to_trade = 8` is narrower than our narrowest
  spread.** §5.2 Stable is $0.10 = 10 ticks. So as configured it would never
  trade at all — least of all overnight, the state it was built for. Clean
  evidence the file was never reconciled against the MM spec.
- **SNT-1 does not distribute the float, and it hides that it doesn't.** Flow is
  50/50 and price-insensitive, so it defeats the only tool we have — a lean
  works by making our offer attractive, and a counterparty that ignores price
  does not respond. Volume would read healthy while N20 is untouched.
- **It also decides E17.** At LIVE intensity SNT-1 crosses ~30,000 shares/hr per
  book against a 10,000-share L1, and its sweeps cap at 3 ticks while our ladder
  spacing is $0.05 — so **every order lands on L1 only**. Under rest-until-gone
  the top level erodes to nothing over ~40 minutes and only reloads when fully
  consumed. §5.9's replenishment makes it a non-issue. E17 stops being a
  preference and becomes a correctness question.
- **His own results carry two things worth flagging back**: teams priced under
  $50 run negative MM P&L (about half the universe, his §7), and retail
  participants lose ~$6,100 a session to the house.
- **The package disagrees with itself**: `HANDOFF.md` §3 says the flow impact is
  10 ticks per 1,000 shares; `RPV2Config` says 6.0. The package is described as
  clean-room verified.

## What went wrong

- **I asserted a fixed 500,000-share day-one position.** George corrected it: the
  Mandate is *buy whatever participants do not*, so it depends on demand — it
  could be more or less. 500,000 is the ceiling on the ten-round reading of
  **E24**, not an expectation. Rewrote the argument to stand without it: even a
  90 % subscribed offering leaves ~50,000 shares a team, still 8× his one-sided
  threshold.
- **I buried the answer in length, repeatedly.** George had to ask three times
  for shorter output, and said plainly that the volume was making the work
  harder rather than easier. The useful pattern that emerged: verdict first,
  then the two or three reasons, then stop.
- **I used symbols and jargon without defining them** — σ, tick, lean, width,
  "measured against" — and each one had to be unpicked mid-call-prep. Same
  failure as 30-07a's symbol soup, less than a day later.

## Decisions *(mirrored into [[market-maker/decisions]])*

ASMM-1 is not a drop-in replacement, and Edwin accepts it · **Edwin sends
spec-style documents with the equations, not code** · adopt his width equation
into Chapter 5 · keep our float denominator for the lean · vol-scale the width
but never the lean · reject the one-sided guard and the drawdown kill · build
none of RPV-1/RPV-2 pending E30 · keep §5.7.3's seeded randomiser, take his
ladder shape.

## Questions

- **Opened:** **E29** does ASMM-1 supersede §4.5/§5.2 · **E30** is RPV-1 the
  published price or the simulator · **E31** γ, k, width bounds and per-state
  floors · **E32** SNT-1's order type, spread guard and short cap · **E33**
  SNT-1 compliance — two house accounts as each other's counterparty ·
  **N26** dwell redraw gated behind §5.8 · **N27** SNT-1 volume feeding the
  Popularity Index, and tagging house prints in the dataset · **T13** does
  tZERO's wash-trade blocking prevent MM↔SNT prints.
- **Sharpened:** **E17** — SNT-1's throughput makes the lifecycle question a
  correctness question, not a preference. **N20** — his design saturates 19×
  sooner than ours, so adopting it wholesale would make distribution worse.
- **Closed:** none.

## After the call — the structural question (George)

Working through whether market sentiment belongs in the Reference Price, George
arrived at the finding that reframes several others:

> A normal market has several **profit-seeking** market makers each guessing
> fair value, competing, with participant flow moving the price between them.
> We have **one**, explicitly not profit-seeking, quoting a fixed spread around
> a **model** number that changes daily. So the market maker sets the price and
> the market cannot disagree.

**It is arithmetic, not opinion.** `RM = RP + IA`, and §4.5 bounds `IA` to
±$0.25. That band is the entire range market activity can move the price —
**0.5% on a $50 share** — and the Mandate pins us at the bottom of it:
**$0.00 of downward room, $0.25 upward**, and only if participants buy our whole
holding.

⭐ **Edwin reached the same wall from the other side.** RPV-2's invented price
drift exists *because he noticed his prices did not move.* Two independent
routes, one finding. His answer was to fabricate movement.

⚠ **I had it wrong first.** I argued sentiment already reaches the price through
inventory → lean. George corrected it: that mechanism only works because a
normal market maker *loses money* by accumulating, which makes the markdown an
inference. Ours has unlimited capital and is required to buy, so most of the
position carries no information at all.

Filed as **E34** (the structural question) and **E35** (the Reference Price was
defined as the *market mid* on 20-07 and as the *model value* in the v1.3 spec —
an unremarked reversal). **N20 and E30 are now symptoms of E34.**

### And then the review reversed half of it (same evening, model switch to Fable)

George asked for a critical pass over the whole discussion. It found:

- **Two E34 claims were overstated** — a participant *can* be right early (paid
  as evidence lands weekly), and a wrong model *is* corrected (banked results,
  $5 at a time). Both corrected in the filing. The residual truth: opinion
  ahead of evidence cannot be monetised.
- **The blend proposal had a hole I missed:** resting orders are free, so a
  §5.5-driven mark is **spoofable**, and §4.2 marks the leaderboard at RP.
  Also: the model's forward leg already carries the **sportsbook crowd** via
  the de-vig — blending our thin book into it dilutes a strong crowd with a
  weak one. **Withdrawn.** §2.3 is judged deliberate and correct.
- **What survived:** E34 as a product-intent question · E35's reversal ·
  the §2.3 catch against RPV-2 · N20 · the SNT-1 blockers · and the cheapest
  idea of the evening, **distribution via size/depth asymmetry**, which works
  under any E34 answer.

Then George walked the quote assembly end-to-end and signed it off:
`RP → + lean → centre → ± width/2 → L1 → ± step → ladder`. Recorded in
decisions and as §0 of the adoption spec. The split-position lean (traded vs
mandated) is filed as a proposal, blocked on E27.

## Where the build stands

Roughly **halfway**, and George's honest read is that **80–90 % of the time so
far has gone on understanding rather than writing** — three documents, each
superseding the last. The process fix agreed on this call is the direct response
to that, and it is worth more to the timeline than any single algorithm change.

## Next

1. **Build Chapter 5** per [[market-maker/asmm1-adoption-spec]] — §0 assembly,
   then the build order: volatility number → width → ladder → guards. Nothing
   in it waits on Edwin. Still the deadline item: quoting from ~26 August.
2. **Send E29–E35 to Edwin** with the next round — E30 before any RPV work,
   E34/E35 as product-intent, E27 because the split-position lean waits on it.
3. Raise **E33 / T13** with Troy — two house accounts trading with each other
   is a compliance read, not an engineering one.
3. Raise **E33 / T13** with Troy — two house accounts trading with each other on
   a regulated venue is not an engineering decision.
4. Outstanding from 30-07a: the regular-season filter, rejection audit records,
   and `feat/position-engine` is **still uncommitted**.
