# 2026-07-27/28 — Build review · the expected-wins insight · Edwin messaged

> **Who:** George + Claude
> **Type:** code review / research / design
> **Refs:** `inplay-market-maker` PR #1 · [[market-maker/decisions]] (27/28-07) ·
> [[market-maker/open-questions]] (E19 rewritten, S10 new) ·
> [[market-maker/learnings]] (27/28-07)

## What we did

- **Reviewed the whole of the 24-07 build against the spec** with fresh eyes.
  Four confirmed defects, every one reproduced with real data rather than
  asserted. Details below.
- **Fixed the worst one** (one event per game, both teams priced) plus two
  guards George asked for. PR #1 open.
- **Created the remote** for `inplay-market-maker` —
  `Novosapien/inplay-market-maker`, private. It had been local-only for two
  days.
- **Wrote `docs/HOW-IT-WORKS.md`** — the missing explainer between the spec
  and the code, for anyone (George included) arriving cold.
- **Worked out that RP needs expected *wins*, not per-game probabilities**
  (George), then researched what that actually costs and traps.
- **Sent Edwin six questions**, grounded in what Sportradar can and cannot
  actually supply.

## The four defects

| | Defect | Evidence | State |
|---|---|---|---|
| 1 | **Only one team per game ever priced.** §7.3 keys a probability update per game with no team component; the adapter emitted one event per team. Same key, different payload → the second is a conflicting duplicate | Real game, both securities through one acceptor: **1,089 accepted, 1,089 conflicts, Ravens never priced.** 1,089 false integrity alarms per game | ✅ **Fixed** (PR #1) |
| 2 | **A corrected official result double-banks.** A correction is a new Results Version → new key → accepted → the payout is added a second time | Win corrected to loss leaves RP at **$5.00**, should be $0.00 | 🔴 Open — step 2 |
| 3 | **A late probability resurrects a finished game.** Nothing stops a finished game re-entering the unfinished set; realized and expected then both count | RP **$10.00 → $14.50** on a game already over | 🔴 Open — step 2 |
| 4 | **A torn journal line makes the system unbootable.** Crash mid-write leaves a partial trailing line; recovery dies on `json.loads` | `BOOT FAILED: JSONDecodeError` | 🔴 Open — step 3 |

Defects 2 and 3 share a root cause: the engine stores **computed answers**
(a game's expected value, a running banked total) rather than the
**inputs** that produce them. §2.5 forbids exactly this —
*"incremental valuation state is prohibited."* Fixing the storage shape
fixes both, plus config-change staleness, and yields the §3.1.4 Input
Snapshot for free.

Also found and not yet fixed: no §2.5 regular-season filter (SR sends
`stage.phase = "regular season"` and we discard it); §3.2's mandated input
fields dropped by the adapter (game status, competition, kickoff time); no
§7.2 rejection audit record (`KIND_REJECTED` is dead code); no retention
window on the seen-keys set.

**Record correction:** the recorded "mypy --strict clean" was `src` only.
`src` + `tests` had one error. Now genuinely clean over both.

## What we learned

Full list in [[market-maker/learnings]]. The two that matter most:

- **⭐ The per-game breakdown cancels out of the price.** Every win pays a
  flat $5, so `Σ GEV(g) = $5.00 × expected wins`. E19's requirement drops
  from ~2,400 game probabilities to **170 numbers**. The hard problem was
  an artefact of how §3.1.1 is written, not of what it needs. (George.)
- **The tests were shaped like the bug.** There *was* an away-side test; it
  built the envelopes and checked the flip, but never ran them through an
  acceptor. The suite proved the translation right and the architecture
  wrong.

## Research (two agents, web)

- Season win totals **close at kickoff and are re-posted weekly** as
  "adjusted" numbers, always **whole-season cumulative** — never a
  remaining-games market for the NFL. So banked wins must be subtracted.
- They are **never repriced during a game**. This confirms the cancellation
  trap: subtracting the live probability from a frozen total zeroes the
  in-game price movement exactly.
- The line is the **median**, not the mean. Converting needs a distribution
  assumption we have **not** validated — deliberately kept out of
  [[market-maker/parameters]] (George: "that's not something I approved").
- These lines are **biased at the extremes** — too high for strong teams,
  too low for weak ones, ~2 wins average error (Woodland & Woodland 2013).
- **NCAA win totals are published by all five books SR sources** (~130–138
  FBS teams) but are absent from SR's NCAAFB futures feed → **S10**.

⚠ Evidence quality: the in-play and cumulative findings are inferred from
industry practice and analyst transcripts, not sportsbook house rules.
Both are cheap to verify ourselves on the futures trial in August, same
trip as the S9 latency measurement.

## What went wrong / got stuck

- **I built all of step 1 without walking George through it**, after he had
  twice asked to go piece by piece. Stopped, offered to revert, and instead
  walked the written code through in pieces. The working mode is not
  "explain then build the lot" — it is one piece at a time, with agreement
  between each.
- **I put σ ≈ 2.0–2.5 forward as a parameter.** It came from a research
  agent that had itself flagged the whole method as unsourced. George
  caught it. It is an assumption inside an unadopted method, recorded as a
  note on E19 and nowhere near the parameters registry.
- **I told George the win-total line "is essentially the expected wins
  number."** It is the median. On a ~$57 share with a $0.10 spread, the
  typical gap is ~$0.60 — six times the whole spread.
- **I claimed "most submissions never reach an order."** Measured: **88%**
  of readings in a live game move the quote by at least a tick. Backwards.

## Decisions made *(mirrored into [[market-maker/decisions]])*

One event per game, both teams priced · the pairs identity as an enforced
invariant · the universe map must be complete or we refuse to start ·
expected wins rather than per-game probabilities (proposed to Edwin, not
adopted unilaterally) · keep the three-term RP structure even though it
collapses algebraically · HOW-IT-WORKS vs BUILD-LOG boundary · MM repo
remote created.

## Questions opened / closed

- **Opened: S10** — NCAA win totals missing from SR's futures feed though
  all five sourced books publish them. **138 of 170 securities.** Now top
  of the priority list; may close E19 outright.
- **E19 substantially rewritten** — the expected-wins collapse, the
  double-count, the cancellation trap and its fix, the median/mean caveat.
  Six-question message sent to Edwin 28-07.
- **Raised, not yet asked:** §3.2 describes a probability record per Team
  Company while §7.3 keys it per game; and §7.2 puts business validation
  *before* sequencing while the §3.2.1 sum check lives in Ch 3, *after*.
  Neither blocks — we implement the conforming shape — but both are §1.6-1
  gaps.

## Next

1. **Step 2 of the fix pass** — store ingredients, not answers. Carries
   defects 2 and 3, config staleness, and §2.5 conformance.
2. **Out-of-game pricing** (raised by George): the engine only knows about
   games it has seen a probability for, so a team with no live game prices
   at almost nothing. Needs the schedule, and is where E19's answer lands.
   Sits naturally beside step 2 — both are about what the engine holds.
3. Then steps 3–5: journal tolerance · the discarded adapter fields
   (regular-season filter first) · rejection audit records.
4. **Chase S10 with Cody + Scott** with the new evidence. It is the cheapest
   large win available.
