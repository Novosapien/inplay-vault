---
description: "Session note: digesting the 27-07 to 07-08 touchdown block into the market-maker docs. IPO market structure settled, valuation inputs confirmed, E11/E12 still unasked."
---

# 2026-08-10, Touchdown block 27-07 → 07-08 digested

> **Type:** digest session (no build work)
> **Sources:** [[27-07-2026-touchdown]] · [[29-07-2026-touchdown]] ·
> [[31-07-2026-touchdown]] · [[03-08-2026-touchdown]] ·
> [[07-08-2026-touchdown]]
> **Previous session:** `2026-07-30-snt1-noise-taker.md`

## What we did

Processed five touchdown transcripts covering 27 July to 7 August. Four of them
carry market-maker content; 31-07 and 03-08 are substantial enough to count as
the MM design session that the 23-07 call never became.

Updated [[market-maker/decisions]] (one new dated block),
[[market-maker/open-questions]] (five resolutions, eight new items),
[[market-maker/parameters]] (a rebuilt IPO warehousing section plus six new
valuation rows), and [[market-maker/plan]] (Phase 0 largely cleared, dry-run
dates added).

## What we learned

**The IPO market structure is now settled, and it is not what the docs said.**
The 15-07 model had the MM warehousing unsold float in ~50k clips. That is gone.
There are two MPIDs:

- **InPlay Markets, the broker dealer**: client-facing, holds the entire
  1,000,000-share-per-team issuance, posts it for sale, unlimited buying power,
  preloaded by tZERO. This is the seller. The MM never sells the primary.
- **InPlay Markets, the principal trading arm**: non-client-facing, runs the
  maker algo and the taker algo off **one wallet, one MPID, one inventory**.

The taker is the primary's biggest buyer, ≥600k of the 1M per team, with
randomised size and heartbeat inside Edwin-supplied ranges. Its purpose is
failure avoidance, not liquidity shaping: with ~118 signups, without it some
teams would sell zero shares and the IPO would visibly fail.

**Edwin corrected a real design worry.** George had spotted that because the MM
supplies most liquidity, its quotes keep dragging price back to the reference
price, which behaves like an anchor. He was right that it happens and wrong that
it is a problem. Edwin: "that's exactly how a real market works." Forced exits
rip price away temporarily (toxic flow), the MM absorbs it, price returns to
fair value. No change needed. Worth remembering as the shape of question to ask
Edwin: describe the observed behaviour, let him tell you whether it is a bug.

**The valuation input chain is confirmed end to end.** The Sport Radar
probabilities contract amendment is signed at no extra cost and live in the
production account. Probability never rides in the play-by-play payload, so we
poll, 500ms in-game to start. Next-game probabilities post ~15 minutes after
the previous game ends, because they are an extrapolation of the odds line.

**The RP formula now has its missing term.** `RP = ((P(win now) − P(win at
kickoff)) + E[remaining wins]) × $5 + off-field`. The in-game term is a **delta
from kickoff**, not the raw probability. That ambiguity had been sitting
unnoticed since 20-07.

**Edwin's stale-input policy is "widen, don't cancel."** Twenty inputs, one
dies, the bid/ask goes wide rather than the book going dark. That fills in the
shape of N3, which we had as pure TBD.

## What went wrong / got stuck

**We wrote the wallet structure down wrong for two days.** On 31-07 Edwin said
two separate wallets for taker and maker; George modelled it that way and could
not make it work ("how can the maker sell stuff that the taker owns?"). On 03-08
Troy corrected it: same wallet, same MPID, two execution styles, and it is the
**broker dealer** that has the separate wallet. Recorded as an explicit
supersession rather than a silent fix.

**E11 (settlement definition) and E12 (NCAA secondary scope) are still
unasked** after three further calls. These have been top-of-agenda since 22-07.
E11 in particular collapses the whole pricing engine into "a live estimate of
the settlement number" if answered. They keep losing to whatever is on fire.

**The 6 August dry run slipped**, called "looking unlikely" on 31-07. George's
own framing of why is worth keeping: AI-assisted development is a snowball down
a hill, sometimes it starts small and compounds fast, sometimes you don't
realise you're still at the top of the hill. Some things land overnight, others
take two weeks, and which is which is not predictable up front.

**Tickers are the hard blocker.** No order testing can start until tZERO issue
them, and the 13 Aug dry run depends on that testing.

## Decisions made

Mirrored into [[market-maker/decisions]] under the 27-07 → 07-08 block: two
MPIDs and their roles · taker as primary buyer with a ≥600k target · randomised
not participation-weighted · load-balancing algo dropped for v1 · 1M issuance
both leagues · treasury holdback · NCAA 5-day / NFL 2-day windows · price freeze
3 days pre-IPO · SR contract signed · 500ms poll · RP formula with kickoff delta
· widen-don't-cancel · RP anchoring confirmed correct · Edwin's code assessed
not adopted · 13 Aug dry run, secondary only, IPO test still required.

## Questions opened / closed

**Closed:** S1 (probabilities API) · S2 (quota) · S3 (poll vs push) · E4
(Edwin's code) · N6 (load-balancing vs market-making boundary, dissolved).

**Opened:** E19 taker requirements doc · E20 daily-report schema · E21
volatility half-life · E22 taker share range and time blocks · E23 post-primary
market operations · S6 key-player definition · T12 the two MPIDs · T13 tickers ·
T14 IPO price lock vs simulated trading.

**Re-scoped:** S4, the betting feed was ruled out for this run, so no faster
path has been bought and probability lag is now purely SR's odds-ingestion
speed.

## Next

Chase **T13 (tickers)**: it blocks the 13 Aug dry run and everything behind it.
Then **T12 (the two MPIDs)** with Troy, and put **E19/E20/E22** to Edwin in
writing, since he acknowledged owing them on 07-08 ("I actually owe you
deliverables"). Ask **E11 and E12** at the same time; they have now survived
four calls unasked.
