---
description: "Edwin's 18-08 maker asks become a parameter round, sent 20-08 — asks 1 to 3 are inert alone, and RPV-2 turns out to be his own July design"
---

# 2026-08-20 — Widen and thin: Edwin's asks become a parameter round

> **Who:** George + AI session.
> **Type:** design / research (no code changed).
> **Refs:** [[18-08-2026-requirements-session]] · `standards/MM-build-spec-v1.3.html` §3.6 ·
> `asmm1-adoption-spec.md` · E30 · E31 · E34 · N20.
> **Sent to Edwin 20-08** — the ten questions are now live with him.

## What we did

Turned Edwin's 18-08 call asks into a parameter round he can sign off, and sent it.

Two documents, both published as artifacts:

- **Spread and Depth** — the as-built reference: the five-stage chain
  (RP → RM → σ² → width → ladder), every symbol defined under the line that
  uses it, and each labelled Constant / Variable / Derived / Drawn.
- **Wider and Thinner** — the Edwin-facing page: his asks in his own words, a
  parameter table with a blank column for his numbers, and ten questions.

**Edwin's four asks, from the transcript:**

1. Top of book only — *"no more book depth anywhere"*.
2. Wider quotes — *"the bid ask isn't as tight"*.
3. ~550 shares, not 11,000 — *"if we're quoting 500 or 600… that bid becomes the offer"*.
4. A distribution level away from fair value, *"around 20 cents 25 cents"*.

**We added a fifth ask, ours:** raise the inventory lean. See below — without it
asks 1 to 3 change nothing.

**George's counter on ask 1:** rungs go to **1–3 drawn**, not 1. The size cut does
the work (three rungs at 550 = 1,231 shares a side against 30,739, a 96% cut;
one rung is 98%), and 1–3 keeps §5.2's stress ladder and the shape variation.
Recorded as a counter in the document, with *"if you still want one, say so"*.

## What we learned

⭐ **Asks 1 to 3 are inert on their own, and the arithmetic says so.** Edwin's own
worked example: a participant sells 1,000 into a 550-share bid and 550 fills. On
our next cycle RP has not moved, and 550 shares against a 900,000 float moves
`IA` by **$0.0006** — six hundredths of one tick. We re-post the same bid and buy
the rest. Thinning the book and widening the spread do nothing without something
that makes the price move and stay moved.

⭐ **RPV-2 is Edwin's own July design, and we declined it.** `rpv2_flow_responsive.py`
in the ASMM-1 package already moves the price with flow: **6 ticks per 1,000 net
shares** (`RPV2Config`) or **10** (`HANDOFF.md` §3) — the conflict is E30, still
open. Our 30-07 ruling was *build none of it*, because three of its four terms
invented movement and the fourth moved **RP**, which SNT-1 would then drive.
**Ask 4 is that fourth term alone, moving the QUOTE instead of RP** — which
answers our own objection: RP, settlement and the leaderboard are untouched.
So the impact coefficient already exists; Edwin owes us 6-vs-10, not a new number.

⭐ **E34 predicted this exactly.** George, 30-07: *"can the market move the price at
all?"* The note already recorded that Edwin built RPV-2's drift because he
noticed his prices did not move. Two routes, one finding — and he has now hit it
live in a real first quarter.

**Trades move the price; resting orders must not.** The 30-07 analysis withdrew a
§5.5 book-derived blend as **spoofable**: a resting order is free, and §4.2 marks
every portfolio and the leaderboard at RP, so there is a direct payoff to posting
and pulling. A trade costs money, so it is credible. The drift therefore reads
**executions only**. Our own fills are journalled already, so ask 4 needs no new
data. Participant-to-participant trades should count too and we cannot see them —
we receive `market.book.{symbol}` (depth), not a trade feed → **T23**.

**Off-field (§3.6) is fully specified and entirely unbuilt.** Seven subsections,
exact formulas — per-game $2.50 pool, volume-share realisation, and a popularity
model blending IPO demand into traded volume over four weekly publications.
No BDI, VMI, capture share or publication exists in code. `realized_off_field`
and `expected_off_field` are reviewed constants in
`docs/supervised-inputs-2026-08-07.json` ($18.31–$30.82 expected, $0.00 realized).
Two external inputs missing: `IPOEligibleOrderShares` (no publisher, E27 family)
and counted participant volume (§5.5). **Not a day-one blocker** — the frozen
values carry the right magnitude at listing — but the error grows all season.

**§3.6.6 is a Bounded Reflexivity Prohibition**, and it matters for ask 4:
trading may reach **RP** only through §3.6, weekly and capped. The drift moves the
QUOTE, so it does not engage §3.6.6 — worth stating before anyone raises it.

## What went wrong / got stuck

⚠ **The band was described as a deadband on fair value, and George rejected it.**
The first reading was "stop following RP until it has moved 25 cents". That is a
**lag mechanism**: with no trading at all we would quote a stale price while the
game moved, and anyone watching the win probability would pick us off. George:
*"this doesn't seem good… the market's gonna move a lot quicker than us."*

**The correct reading** — from Edwin's own words, *"a distribution level away from
fair value that the market maker will **reside**"* — measures the gap between OUR
QUOTE and CURRENT fair value:

    centre = RP + drift        drift bounded to ±$0.25

We track fair value continuously and carry an offset on top. No trading → drift
zero → we quote at fair value → never stale.

⚠ **His two numbers were wrongly merged into one.** The claim that 25 cents and
"5% win probability" were the same rule (5% × $5.00 = $0.25) was arithmetic
coincidence dressed as a finding. They are **two different objects**: 25 cents
**bounds** the drift, and a 5% probability move **clears** it.

⚠ **`skew_reference_shares` was published in the wrong form.** 12,000 is Edwin's
**saturation point**, not the denominator. Saturation is `M ÷ S × D` = 0.25 × D,
so a 12,000 saturation needs **D = 48,000**. The effect table was right
throughout (550 sh → 1.1 ticks); only the parameter row was wrong. Also flagged:
12,000 was fitted to his 250-share book (48 rungs to saturation); at 550 a rung
it is 22, so scale-matched it is nearer 26,400. Framed for Edwin as *"how many
rungs before we are fully leaned over?"*

⚠ **Two smaller corrections.** The untradable-opponent rule (full $2.50 to the
universe team) was called unrecorded — it is **spec §3.6.1**, only missing from
`parameters.md`. And `state_floor_ticks` was justified as *"now required because
depth was the last stress signal"* — true only at one rung; at 1–3 the real
reason stands on its own (the equation cannot exceed $0.15, and a stale feed
makes it quote **tighter**).

⚠ **Incremental edits put a contradiction into a document about to be sent.**
One note argued that two separate $0.25 limits meeting was *"the correct shape"*;
a later note proposed **one** combined limit. Both shipped. Caught only by
reading the rendered page end to end, along with a duplicated section and a
headline stat that counted the lean but not the drift. **A document that
accumulates edits must be re-read whole before it leaves.**

⚠ **Artifact URLs were lost twice to account switches.** Three accounts saw three
different artifact sets; the first `Spread and Depth` URL is unrecoverable. Local
files are the source of truth; artifacts are disposable.

## Decisions made *(mirrored into [[market-maker/decisions]])*

- ✅ **Rungs go to 1–3 drawn, not 1** (George) — a counter to ask 1, sent as one.
- ✅ **The drift reads EXECUTIONS only**, never resting orders — spoofability.
- ✅ **One combined $0.25 bound** on the total gap from fair value, covering the
  lean and the drift together — put to Edwin for confirmation.
- ✅ **Nothing is built until Edwin answers.** No code changed this session.

## Questions opened / closed *(mirrored into [[market-maker/open-questions]])*

- **E51 opened** — the 18-08 parameter round: ten questions, sent 20-08.
- **T23 opened** — does tZERO publish a participant trade feed?
- **E30 annotated** — revived in a narrower, better form (quote not RP); the
  6-vs-10 impact conflict is now load-bearing rather than parked.
- **E31 annotated** — the width numbers ride the same round.
- **N20 / E34** — both now have Edwin's own live corroboration.

## Next

**Wait for Edwin's ten answers.** Nothing should be built before they land — the
impact number, the one-limit ruling and the rung call each change what gets
written. Two items are ours and can move meanwhile:

1. Ask tZERO for a participant trade feed (**T23**).
2. Settle the deploy window — Edwin said "next Saturday" (29-08), which is a live
   NCAA Saturday, and **R11 forbids a maker cutover during live games**. Ship
   before NCAA secondary opens, or take a Sunday morning.
