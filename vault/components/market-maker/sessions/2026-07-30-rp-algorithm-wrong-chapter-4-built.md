# 2026-07-30 — the Reference Price was wrong · Chapter 4 built

> **Who:** George + Claude
> **Type:** code review / build
> **Started:** 29-07 evening, ran through into the 30th
> **Refs:** `inplay-market-maker` branch `feat/position-engine` ·
> `standards/MM-build-spec-v1.3.html` §4 · `reference/inplay-reference-feed/` ·
> [[market-maker/decisions]] 29-07b + 30-07

## What we did

**George read the code and found the Reference Price used the wrong
algorithm.** That set the whole session. We fixed it in three pieces, then
built Chapter 4 in three more.

**Tests: 63 → 171.** ruff and `mypy --strict` clean throughout.

| | |
|---|---|
| on-field formula | `on_field_value()` + `KickedOffGame`, 7 tests |
| engine on the new leg | `T`, `effective_time`, the kickoff→next-T window |
| daily feed reader | `reference_feed.py`, validated on Edwin's own sample |
| §4.1 §4.2 | `position.py` — net position, average cost, P&L |
| §4.3–§4.6 | `inventory.py` — float, ratio, skew, Reservation Midpoint |
| Chapter 4 engine | `position/engine.py` — fills in, positions and skews out |

**Also:** swept the comment style across all ten source files — code at the
top, long-form reasoning in a `# Notes` block at the bottom, keyed by named
markers. George found the inline density unreadable. Repo `CLAUDE.md` rewritten
so it sticks.

**And a reference page** for Chapter 4's equations, every symbol defined
underneath, one team's numbers carried through:
`https://claude.ai/code/artifact/d9a53c9c-24e7-46e9-934e-325ff1c6947b`

## The Reference Price was wrong

`Σ GEV(g)` over *"games we happen to hold a probability for"* is not Edwin's
leg. It is why a team with no live game priced at roughly $0 instead of
roughly $63.75.

```
$5 × ( T − Σ p_ref(g) + Σ x_g )     over games kicked off since T
```

**Then George found the real trap, which is not in the formula but in the
window.** The obvious reading is "adjust while a game is live". Wrong by
$2.17: a game leaves G when a **new T absorbs it**, not at the final whistle.
Stop at the whistle and a Chiefs win *drops* the price by `$5 × (1 − 0.566)`
the moment they win, then returns it at 06:00 next morning. A sawtooth, on
winning. There is now a test that watches the whole boundary.

## What we learned

- **⭐ The spec's finance is authoritative; its engineering is AI scaffolding
  (George).** Formulas, settlement, skew mechanics, the de-vig — the author's
  own domain, so defer. Event types, idempotency tables, journal design —
  generated, so judge on merits. ⚠ Judge, not ignore: §7.3's per-game keying
  exposed the adapter bug that left half the universe unpriced, and §7.2's
  lifecycle ordering settled where rejection belongs.
- **⭐ Wins are conserved, and the feed does not conserve them.** 32 NFL teams
  x 17 games = 272 games, so the 32 expected-win figures must sum to 272. Real
  BetMGM lines sum to **275.00**; after the de-vig, **273.95**. The de-vig
  removes a third of the excess but nothing enforces the league total, because
  Edwin's rake works per team. Worth $0.30 a share, one-directional, ≈$8.6 M
  across the NFL float. **George's call: minor, park it as N25.**
- **Membership of G is a timestamp comparison, never a judgement.** Kicked off
  before T → banked, leave it. After T → still a guess inside T, swap it for
  reality. Not kicked off → T's guess is the best we have.
- **A played game needs no probability** — `x` is 1, 0.5 or 0. It still needs
  `p_ref`.
- **`p_ref` is not in Edwin's feed.** Verified against the sample. We capture
  Sportradar's last pregame reading ourselves.
- **The Reservation Midpoint goes negative without the §4.6 floor.** RP $0.10
  with the skew at −$0.25 gives −$0.15. A team late in a losing season, near
  the floor, with us holding most of its float. Not contrived. Found while
  writing the code, not by review.
- **A fill for an untracked security is an alarm, not a boundary.** Deliberately
  the opposite of the valuation engine's silent skip: an unknown *team* is a
  legitimate §2.5 case (FCS opponents), an unknown *fill* means we traded
  something we cannot price.
- **Average cost is a division, so it recurs.** `$23,000,000 ÷ 450,000` cannot
  be written exactly. Never compare it to a hand-written literal.
- **Two of §4.1's four inputs have no publisher** — the opening position
  (**E27**) and corporate adjustments (**E28**). George pushed on "how do we
  actually get this", which is what surfaced both.

## What went wrong

- **I dumped symbol soup on George** — NP, RF, PR, IA, RM with no definitions,
  laid out badly. Fixed by building the reference page with every symbol
  defined underneath its equation.
- **I used trading jargon without noticing** — "shade the quote", "the fill
  goes against the position". Both had to be unpicked.
- **I showed code that did not exist**, describing the position engine's event
  routing as though it were written. It was piece 3, unbuilt. George caught it.
- **I over-argued the IPO_ALLOCATION event**, claiming the v2 dates force an
  overlap between the primary and the secondary. Re-reading, §1.1 is clean and
  the overlap only appears from §2.1 + §5.2 together — almost certainly
  drafting sloppiness. Conceded, and the handler was dropped.
- **The comment-sweep agent went idle without reporting**, the same failure as
  the two on 27-07. Verified its work myself: every file grew, no spec section
  or open-question id was lost. One real gap found — §3.1.2 and §3.3 had
  vanished from `sportradar.py`, and that one was mine, not the agent's.

## Decisions *(mirrored into [[market-maker/decisions]])*

The spec filter (finance authoritative, engineering scaffolding) · the on-field
leg supersedes §3.1.1 · the window is kickoff→next-T · `p_ref` freezes at
kickoff (N22 interim) · a tie is a terminal state, not a live probability ·
`T` required rather than optional · publish-on-change (§3.1.5) · N25 parked ·
`IPO_ALLOCATION` and `CORPORATE_ACTION` not built · comments move to a Notes
block at the end of each file.

## Questions

- **Opened:** **E27** how we learn the opening position · **E28** do corporate
  actions ever happen · **T12** would the venue tell us · **N22** where `p_ref`
  comes from and when it freezes · **N23** no event type for the daily feed ·
  **N24** does SR publish pregame probability movement · **N25** NFL wins do
  not sum to 272.
- **Closed:** defect #5 (`GameStatus` read the wrong field) — fixed, though not
  the way the report said. `sport_event_status.status` is a *response*-level
  field, so a captured game carries one status for all 1,089 readings.
  Comparing each reading's own timestamp against `start_time` works for replay
  and live alike, with no clock read.
- **Re-prioritised:** **E27** to second, behind only the NCAA dates. v2 makes
  us the buyer of all remaining shares, so it is the entire day-one book, and
  nothing publishes it.

## Next

1. **Chapter 5, quote construction.** It consumes exactly what we just built —
   `RM` in, Target Order Book out. It is also the deadline item: quoting from
   ~26 August.
2. The poller, whenever Sportradar entitlement lands. Buildable against replay
   before that.
3. Outstanding in the fix pass: the regular-season filter (postseason games
   currently carry on-field value) and rejection audit records.
4. **Nothing is committed.** `feat/position-engine` has today's work uncommitted
   in the working tree.
