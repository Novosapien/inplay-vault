# 2026-07-29 — Edwin answers all six · IPO Requirements v2 · fix pass complete

> **Who:** George + Claude
> **Type:** document intake / code review / build
> **Refs:** [[standards/MM-edwin-answers-28-07|Edwin's email rendered]] ·
> `standards/InPlay IPO Draft Requirements v2 (July 28 2026).pdf` ·
> `standards/IPO_Pricing_Subscription_Supplement_v1.3.docx` ·
> `components/market-maker/reference/` · `call-questions-29-07.md` ·
> `inplay-market-maker` PRs #1 #2 #3

## What we did

**Finished the fix pass.** All four defects from the 27-07 review are fixed
and merged. 63 tests, ruff and mypy clean.

**Processed four rounds of incoming material** — Edwin's answers to all six
questions, his engine as code, the IPO pricing workbook, and the IPO Draft
Business Requirements v2.

**Worked through all six questions and answers with George**, one at a time,
in plain terms.

**Rewrote the call questions four times** as material arrived and closed
items off.

## The build — fix pass complete

| PR | Step | What it fixed |
|---|---|---|
| #1 | One event per game | Only one team of every game was ever priced. 1,089 accepted, 1,089 conflicts, the Ravens never priced |
| #2 | Store inputs, not answers | A corrected result double-banked; a late probability resurrected a finished game |
| #3 | Repair a torn journal tail | A half-written line stopped the system booting |

Also added: the **pairs identity** as a hard check ($5.00 exactly, verified
across 5,948 normalised triples), a **map completeness check**, and
**`GameStatus`**.

⚠ **One defect introduced and recorded.** `GameStatus` reads Sportradar's
`live` flag, which is a **coverage** indicator, not a progress indicator —
confirmed by Scott Boyd (SR, via Cody) and by our own fixture, where a 2024
game that ended still reads `live = true`. Fix goes in step 4.

## What Edwin answered

All six, in full, with code attached.

- **E19 resolved.** Daily 06:00 ET feed, all 170 teams, `expected_remaining_wins`.
  College comes from his own Elo engine; NFL is raked to the de-vigged
  sportsbook total.
- **S6 resolved.** Price the two-way market as proposed. A tie settles at 0.5,
  worth $2.50.
- **S10 closed.** We no longer need Sportradar to carry NCAA win totals.
- **Our double-count fix confirmed and generalised** — `G` is a set, and a
  game stays in it after the final whistle until a new `T` absorbs it.
- **Do not smooth the mid** when a new number lands.

## What we found in his code

Verified rather than accepted. **31 tests pass. The worked example reproduces
to four decimal places.** Then seven problems, raised under his own
invitation.

Three are his two IPO implementations disagreeing: the **tie leg** ($0.20 vs
$0.17), the **Bradley-Terry inputs** (Index vs Index, or Index vs raw Brand),
and the **discount scale** (ranked per league, or flat). The workbook later
settled all three in favour of `engine.py`.

Also: league naming inconsistent, everything is `float` so nothing can be
lifted verbatim under §1.6-3, the Supplement is missing §7, and his stated
acceptance test could not run.

## What the workbook gave us

`InPlay_IPO_Pricing_2026.xlsx` answered five questions at once. Extracted to
`reference/ipo-prices-170.csv`: **IPO EV and Listed price for all 170 teams**,
plus Brand, Popularity, Capture and out-of-universe games — which made
`teams_config.py` redundant as well as unnecessary.

**Our de-vig reproduces his exactly.** Largest difference across 170 teams:
**8.88 × 10⁻¹⁶**.

## What v2 changed

**The deadline moved.** Secondary trading, not the season.

```
NCAA secondary   26 or 27 August   ← four weeks
NFL  secondary   7 September
```

**And v2 contradicts itself in five places** — the mandate round count (10,
16 or 18, worth $3.4 bn of opening position), the NCAA dates (secondary would
open 12 hours before the primary closes), 100,000 unoffered NCAA shares per
team, and the NFL hours.

**Shorting is new**, and the full float may be sold short. So what can be sold
to us is float **plus** short interest.

## What we learned

- **⭐ The reason to distribute is liquidity, not profit or risk** (George).
  §1.5 excludes profit and we have unlimited money, so the usual reason to
  shed inventory does not apply. The real reason is that a market with no
  shares in circulation is not a market. **That reframes the inventory skew as
  a distribution tool.**
- **And the skew has no room.** It caps at 25 cents, which binds at 25% of the
  float. We will hold 50–100%. Holding the entire float reads identically to
  holding a quarter of it.
- **A silent skip and a silent failure can share a code path** — the universe
  map check.
- **Re-run the original reproduction, not just your own tests.** The first
  journal fix was wrong and only the original repro caught it: discarding a
  torn line at read time leaves it on disk, so the next append welds a good
  record onto a fragment.
- **"Not in the feed" and "does not exist" are different findings** — SR does
  not carry NCAA win totals, but the sportsbooks publish them.

## What went wrong

- **I built all of step 1 without walking George through it**, after he had
  twice asked to go piece by piece. Stopped and walked the written code
  through instead.
- **I put σ ≈ 2.0–2.5 forward as a parameter.** It came from a research agent
  that had itself flagged the method as unsourced. George caught it. The real
  value is 2.7 / 2.2, from the workbook.
- **I asked for `teams_config.py` when we did not need it.** George's
  challenge was right: brand scores feed the Popularity Index at IPO only.
- **I said the market maker faces one-sided sell flow on day one.** George
  corrected it — during the offering participants can only buy.
- **I over-trimmed the call questions**, then had to restore the context.
- Two research agents went idle without reporting. Did the work directly.

## Decisions *(mirrored into [[market-maker/decisions]])*

Gospel ruling (v2 + the 170-team CSV outrank emails and the Supplement) ·
the deadline is secondary trading · the MM buys all remaining shares,
superseding §9.2 · InPlay Markets is the exclusive primary seller ·
distribution is about liquidity, not profit · an upload page for the daily
file, with retention in perpetuity.

## Questions

- **Resolved:** E19 · E20 · S6 · S10 · N17.
- **Reduced:** E22 (shares outstanding known; issued-vs-treasury is now N21) ·
  N18 (both sides verified priced; compute-or-consume still open).
- **Opened:** E21 IPO implementation discrepancies · E23 price composition ·
  **E24** mandate round count · **E25** the NCAA dates · **E26** shorting
  rules · N19 upload page · **N20** the skew cannot distribute · **N21**
  unoffered NCAA shares.

## Next

1. **Chapter 4, the position engine.** Branch `feat/position-engine` is open.
   Nothing blocks it — we now have the float.
2. Then the feed reader, then Chapter 5.
3. **Nothing blocks the build.** Only §5.9 replenishment is genuinely waiting,
   because E17 is a mechanism question rather than a value. Two data gaps —
   the schedule and the live feed — do not stop code today.
4. The call questions are in `call-questions-29-07.md`, open items only.
