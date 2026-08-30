---
description: "Edwin's SDMM-1 v5.1 engine arrives, run and measured: it answers E52, our rebase is withdrawn, and George drops the injury channel"
---

# 2026-08-28: Edwin's engine lands — and the injury channel is dropped

> **Who:** George + Claude
> **Type:** analysis (of a delivered artefact) + one ruling
> **Refs:** `reference/edwin-sdmm1-v51-2026-08-27/` ·
> [[27-08-2026-mm-pricing-catchup]] ·
> [[market-maker/systems/expected-wins-pipeline]] · `E52` `E53`
> **Artifact:** "What Edwin sent" (claude.ai) — the decoded brief

## What we did

- Unpacked `novo_handoff_1.zip`, the formula Edwin promised on the 27-08
  call. Filed it at `reference/edwin-sdmm1-v51-2026-08-27/`.
- **Ran it, rather than only reading it.** All 31 acceptance tests pass.
  It reproduces LSU's published IPO of $59.535 to the penny.
- Measured four things nobody had measured: where the price move comes
  from, whether a win probability substitutes for a spread, how the engine
  scales to 170 teams, and how big the injury channel actually is.
- George ruled on the injury channel.

## What we learned

### The price formula is nearly ours; the engine underneath is not

His forward leg `5·ΣP(win)` IS our `$5 × T` — expected wins is the sum of
the per-game win probabilities. Same $5 win, $2.50 tie, $2.50 pool,
settlement identity, live leg, and no step at the whistle. All match.

What differs: we hold a frozen number. He holds a **rating in points per
team**, and every observation moves it by one Kalman step. That is the
whole difference, and it is the whole behaviour.

### It answers E52, and our proposal is withdrawn

| Event | Move |
|---|---|
| Loss by 7 | **−$12.54** |
| Ugly win (by 2 as a 28.5-pt favourite) | −$5.46 |
| Big win | +$6.51 |

Decomposed, the loss is only **−$4.53** from the game itself. The other
**−$7.14** is the remaining 11 games re-rating from 7.64 to 6.22 expected
wins. That is how a $5 game moves a price $12.54.

**Our weekly futures rebase is superseded. Withdrawn, not deferred.**

### ⭐ A win probability IS a spread

Verified on all 12 LSU games: `d = √(ς² + Var d) · Φ⁻¹(p)` reproduces the
engine's own edge exactly, and feeding the derived number gives an
identical price to feeding the real spread.

So his "primary channel", which we had listed as a feed we do not have,
**may already be arriving** as Sportradar's pregame win probability — the
same number we freeze as `p_ref`. Two unknowns remain: how far ahead SR
prices college games, and what observation noise their number deserves
against his 1.5-point bookmaker assumption.

### ⚠ The reference implementation does not scale

It rebuilds the entire posterior on every read. That is deliberate —
in-place updates double-apply, which cost $1.18 per repeated tick in his
v4, and the maker ticks many times a minute.

| Teams | Games | One rebuild |
|---|---|---|
| 13 (his demo) | 72 | 0.5 ms |
| 138 (our live book) | 828 | 364 ms |
| 170 (full league) | 1,020 | **652 ms** |

The cache clears on any new observation, and we poll live games every
500 ms. **A rebuild already exceeds the poll interval.**

**The fix, measured:** checkpoint the settled observations, replay only
the live games on top — **5.5 ms**, 130× faster, and it preserves his
idempotency exactly. It is the same checkpoint-plus-replay pattern our
journal already uses. Performance is explicitly out of his scope, so this
is ours either way.

### ⚠ Our prices sit ~2% above what shares were sold at

Measured across 132 matched college teams: our reference price runs a
**median +2.39%** over the listed IPO. His two "extra" legs — discounting
(−1.14%) and the risk charge (−0.87%) — total **−2.01%**, almost exactly
the gap.

They are not decoration. They are what reconciles the model to the price
people actually paid. Both are one line of arithmetic; both unwind to zero
by settlement.

⚠ One outlier in that check (Louisiana Monroe, −40%) is probably a
name-join error in my comparison, not a real discrepancy. Verify before
anyone quotes it.

## Decisions made *(mirrored into [[market-maker/decisions]])*

- ✅ **DROP the injury channel** (George). Measured, it is one scenario:

  | Injury | Move |
  |---|---|
  | Own QB, season-ending | **−$8.31** |
  | Own WR / DL | −$1.75 |
  | Own OL / RB | −$1.40 / −$1.18 |
  | Own kicker | −$0.62 |
  | Opponent's QB out | +$0.26 to +$0.77 |

  **Safe because** a QB injury still reaches the price through
  Sportradar's win probability — immediately during the game, and for
  later games as each gets its pregame number. Delayed, not lost.

  **A net simplification because** the stale-spread trap exists ONLY
  because an injury can post-date a posted spread. Dropping injuries
  removes the −$3.57 wrong-direction bug, the `stale_spreads()`
  invalidation logic, the timestamp requirement on the board feed, and a
  feed (position + severity) we do not have.

  ⚠ **Recorded cost — a product one, not a correctness one.** Edwin's
  09-08 Gamecast document made the star-QB case its headline (a major
  injury dropped a winning team's price in 26 of 26 tests), and it is the
  most dramatic moment in the product. Under this ruling the price drifts
  instead of reacting. The channel can be added later without changing
  anything else.

- 🟡 **§7 of the pipeline page is withdrawn**, not deleted — the reasoning
  trail stays.

## What went wrong / got stuck

- The complexity is real and it landed badly. We asked how to keep a daily
  number alive without Edwin operating a file. We received a complete
  pricing engine with discounting, a risk charge, a rating model and a
  spread channel. Most of it turns out to be either what we already had or
  one line of arithmetic — but that only became clear after measuring it.
- I described the update channels as "news", which read as press and
  headlines. It means new numbers arriving: score, live probability,
  pregame probability, and the weekly earnings figure. **Three of those
  four we already receive; the fourth we compute ourselves.**

## Questions opened / closed

- **E52 answered** — the tail re-rate is his rating engine, not our rebase.
- **E53 opened** — port his engine or keep ours. His takes our seed as its
  t-zero calibration, so this week's work is its input either way.

## Next

- **Nothing before Saturday.** The running engine prices Saturday
  correctly, and R11 forbids a cutover while games are live.
- George's call on E53.
- Cheap and independent of that call: fix the ~2% IPO gap.
- Still outstanding from 27-08: send Edwin `E51` (the popularity file and
  the earnings split rules) — the first earnings burst is days away.
