---
description: "Design for suspension recovery — what already re-opens a book automatically, the three gaps that do not, and the proposed backstop, manual lever and freshness carry"
---

# Suspension Recovery — every suspension needs a defined exit

> **Component:** [[market-maker/market-maker]] · **Status:** ⭐ DESIGN,
> nothing built · **Born:** George's requirement (14-08, restated 16-08
> after the settled-echo incident): *a suspended book must never be a
> dead end.*
> **Related:** [[market-maker/open-questions]] N40 (game-end lifecycle) ·
> N29 (the panel's control surface) · N40's policy half (NOT E11 —
> that resolved 24-07) ·
> [[market-maker/build/market-state|Market state]] ·
> [[market-maker/build/valuation|Valuation]]

---

## 1 · The finding that reshapes this work

**Auto-recovery already exists for input-driven suspension, and it is
not the gap.** Verified in code 16-08:

- `restriction()` (`market_state/engine.py`) is a **pure function of the
  CURRENT inputs**, recomputed on every cycle. It holds no memory of
  having suspended.
- `MarketStateTracker` demotes instantly and **leaves Suspended
  dwell-free** (`[start-suspended]`); only the upper rungs earn their
  10 s dwell.
- The orchestrator's `_suspended_securities` set is touched **only** by
  `MANUAL_CONTROL` — derived suspension never enters it.

So the moment a suspended book's inputs go healthy, it re-opens by
itself, with no operator action. That is why the 15-08 six books came
back the instant a fresh journal gave them a valid Reference Price.

**The 15-08 failure was therefore not a latch. It was an input that
could never recover** — the feed for a finished game stops for ever, so
RP Status stays Invalid for ever, so the book stays Suspended for ever.
The dead end was in the INPUT, not the state machine.

This matters for scope: we are not building a recovery mechanism. We
are closing the three cases where an input cannot recover on its own,
and adding the lever for when a human must decide.

## 2 · What already works — do not rebuild

| Suspension cause | Exit | Automatic? |
|---|---|---|
| RP Status Invalid (feed silence, recovered) | next healthy reading → CURRENT → restriction lifts | ✅ dwell-free |
| Venue disconnected | reconnect → `set_venue_connection()` | ✅ |
| Venue sync UNKNOWN order | reconciler resolves it | ✅ |
| Quarantine (engine fault) | ⚠ **NO exit — see gap 4** | ❌ |
| Manual kill switch / security suspension | `MANUAL_CONTROL` release | ⚠ no surface — gap 3 |
| Ladder cannot be two-sided in bounds | next cycle at a workable RP | ✅ |

## 3 · The gaps

### Gap 1 — an input that can never recover (the 15-08 class)

A finished game's feed stops; RP Status ages to Invalid; the book
suspends with nothing left that could ever un-suspend it.

**Largely closed at source** by the two 15-08 fixes: `[settled-freshness]`
(MM #45) keeps a finished book out of the live freshness regime
entirely, and `[final-is-receipt]` (MM #46) makes POST_GAME start at the
whistle. A finished book now reports CURRENT and never suspends.

**Residual:** the fixes work because the engine SAW the final. A game
that never finals — the duplicate-id case (`sr:sport_event:68385804`,
N39) polls at the live tier for ever and no `OFFICIAL_RESULT` is ever
minted. That book is still exposed.

**Proposed — the terminal backstop.** A book that has been Suspended on
`Reference Price Status is Invalid` for longer than
`suspension_alarm_s` **raises a loud, repeating operator alarm naming
the security, the reason and the age**. It does NOT auto-release:
quoting on an input we know is dead is the §2.3 danger case, and
wide-when-ignorant means silent, not wrong. The exit is the alarm plus
gap 3's lever.

- 🟡 `suspension_alarm_s` — proposed **300 s**. Ours; long enough that a
  normal recovery never fires it, short enough to catch a night.

### Gap 2 — derived state lost on a fresh journal

Suspension is derived, so a fresh-journal cutover forgets it — which is
how the 15-08 books "recovered" and also how played books re-quoted at
pre-final prices on 14-08. The same hole loses `final_time`: after the
23:37Z cutover the engine did not know the five finished games were
over until a re-offer re-minted each final (measured gap ~12 min,
15-08→16-08).

**Proposed — extend the anchor seed.** `ANCHOR_SEED` already carries
valuation beliefs across a fresh journal. Add the freshness facts it
needs to stop re-deriving a finished game as live: per security,
`final_time`, `settled_game_id`, and the `game_id` link.

- Same lenient-reader rules as the existing seed: prove every candidate
  before it enters the payload, name every degradation, mint nothing on
  an unexpected fault.
- The seed stays **the weakest fact in the machine** — applied only
  where the journal knows nothing.
- ⚠ Event-shape change → the N23/N28 blessing round, with the sweep and
  the session boundary.

### Gap 3 — no manual release lever

§6.3's manual conditions exist in the engine (`MANUAL_CONTROL`) and
nothing publishes them. An operator who sees the gap-1 alarm has no
button.

**Proposed:** the MM Ops UI's kill-switch surface (**N29**) grows a
per-security release beside it. ⚠ **Access control first** — the panel
already carries `/loadtest`, `/stress-test` and `nats/purge`; a release
lever sits in the same room. Roles exist; which role gates what is
unanswered.

### Gap 4 — quarantine has no exit at all

A quarantined security repeats `BookSuspended("quarantined: …")` for
every later event **without re-running its engines**, deliberately, so
the fault cannot recur. Nothing clears it short of a restart. This is
correct for a real engine fault and wrong for a transient one, and it
is not covered by anything above.

**Proposed:** leave the automatic behaviour exactly as it is (a
quarantine means we do not trust the engine for that book) and route
the exit through gap 3's manual lever plus a gap-1-style alarm. A
self-clearing quarantine would re-run a known-faulting cycle on live
money.

## 4 · What this does NOT decide

- **N40's policy half** — what a finished book should *deliberately* do
  (settlement pricing, freeze, reseed for the next fixture) is Edwin's
  and George's. This design only stops the ACCIDENTAL dead end.
  ✎ **Not E11.** E11 was RESOLVED 24-07 (v1.3 §11.3: `FSV = realized
  on-field + realized off-field`) and owes nothing. The N40 row's
  standing "the E11 call" phrasing is stale and was repeated here
  16-08; the open policy question is N40's own.
- **Whether a dead-feed book should quote at all.** Gap 1 deliberately
  keeps it silent and shouts. If Edwin wants a widened-but-live posture
  instead (his 03-08 "widen rather than cancel" instinct), that is a
  different answer and it is his to give.

## 5 · Build order, if approved

1. **The gap-1 alarm** — smallest, highest value, no event-shape change,
   no new surface. Catches every remaining class including N39's.
2. **The gap-2 anchor-seed extension** — needs the N23/N28 blessing.
3. **Journal the activity transition** — §6.4 already journals
   market-state changes; activity is not journalled, which is why
   proving POST_GAME on 16-08 needed a replay harness over 3.6 GB.
   Small, and it makes every future question of this shape a grep.
4. **Gap 3's lever** — gated on the panel's access-control answer.

## 6 · Open questions this raises

| # | Question | Owner |
|---|---|---|
| — | Is `suspension_alarm_s` = 300 s right? | George |
| — | Should a book suspended on a dead feed stay silent (proposed) or widen and quote (Edwin's 03-08 instinct)? | Edwin |
| — | Which panel role may release a suspension? | George + the panel's access control |
| — | Does the anchor seed's freshness extension need its own event type, or does it ride `ANCHOR_SEED`? | N23/N28 round |
