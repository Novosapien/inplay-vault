# 2026-08-09 — the sell rule decoded, and three findings the engine handed us

> **Who:** George + Claude (George directing: research the T0 docs ·
> probe it live · "you can use the other gateway channels" · file it)
> **Type:** documentation research → live probe → findings
> **Refs:** decisions `2026-08-09` · parameters (venue risk + bands) ·
> [[market-maker/build/venue|Venue]] · [[market-maker/test-plan]] B1 ·
> open-questions T14/T15 · the SNT-1 walkthrough artifact

## What we did

1. **Researched every tZERO document we hold** (agent sweep: vault,
   both gateway repos, trading service, vendor PDFs) for the oversell
   question. Verdict: **NOT DOCUMENTED**. The vendor OE spec does not
   even enumerate side 5 — tag 54 is `1 = Buy, 2 = Sell`, with no
   short-sale marking, no locate tag, and no `OrdRejReason` value for a
   position failure.
2. **Found three contradictory beliefs about it inside our own app** —
   `venueOrders.ts` (rejects whole, resting sells count),
   `OrderEntrySheet.tsx` (fills up to the position),
   `buying_power.py` (undefined, refuse client-side). None cited a
   venue source.
3. **Probed it live.** First attempt on the MM account failed twice
   over (below). Second attempt used George's own user account, at his
   direction, and answered both questions in a single reject.
4. **Filed everything**: decisions, parameters, venue build page,
   test-plan B1, T14/T15.

## ⭐ What we learned — the sell rule

```
FAILSRISK[5120866205]: You can SELL at most 50 shares of IPTCGIAN. Pos=100 livS=50
```

- **sellable = Pos − livS** — the position minus the quantity already
  committed to LIVE RESTING SELLS. The venue prints its own arithmetic.
- Over that, the order is **rejected WHOLE**. Never part-filled to the
  limit; never converted into a short.
- Control (sell 50 of 100 held) accepted · test (sell 150 of 100 held)
  rejected. Both non-marketable, both cancelled, position unchanged.
- It is a **venue rule, not per-account config** — an earlier
  hypothesis, retracted. The MM's 07-08b "You are not long" reject is
  the same check at `Pos=0`. The negative positions on user accounts
  came from side-5 short orders behaving correctly.

## The other three findings

- ⚠ **DONE_FOR_DAY has never happened.** No `39=3` in the entire
  gateway FIX log; orders from 08-08 00:31 survived two 23:59 ET
  boundaries and still rest. An adopted 22-07 "venue fact" is
  contradicted, and test B1 loses its premise → T14.
- ⚠ **The engine crosses the stale book on every repost.** A COWB bid
  at 76.04 was marketable against stale asks at 54.35–55.05 and swept
  8 levels: **920 shares, $50,366**. The MM is taking liquidity while
  intending to rest. Live and recurring.
- ⚠ **The engine adopts any MM-prefixed order on its user id** —
  `_get_or_admit` admits an unregistered ack as ACTIVE, so the
  reconciler cancel/replaced a hand-sent probe 0.7 s later. No manual
  probe on the MM user id is safe while the engine runs.

## What went wrong / got stuck

- **The first probe cost $50,366 of unintended trading.** Not the probe
  order itself — it woke the engine after 38 hours of quiet, and the
  engine's next repost swept the stale book. Lesson: on these books,
  *any* engine cycle can trade.
- **A demonstration order filled unintentionally.** George placed a buy
  at limit 148 to reveal his user id; the stale ask at 146 was inside
  the limit, so it executed — 100 shares, $14,600. My instruction
  ("well below the market") was too vague for a book carrying stale
  quotes at double fair value.
- **Two false claims made and retracted mid-session**, both from
  over-reading greps: "those sells are all side 2" (they included side
  5) and "this is per-account configuration" (it is a venue rule). The
  position field `9383` does not move per fill in the log, so
  co-occurrence there proves nothing — only the controlled probe did.
- The `market-maker` NATS credential is correctly scoped to
  `gateway.orders.mm.*` and refused the general user-order subject.
  George's route through the MM subject with a different identity in
  the payload is what unblocked it.

## Decisions made

All in decisions `2026-08-09`. Autonomous and recorded: the probe
transport workaround (MM subject + foreign identity in the payload).

## Questions opened/closed

- **Opened:** T14 (is there a session roll at all?) · T15 (which risk
  toggle governs the sell check, and its per-account values).
- **Closed:** the oversell question itself — answered by observation.
- **Unchanged:** E32/E33/T13 for SNT-1; the IPLP account still pending.

## Next

1. **The stale-book crossing** — the engine is taking liquidity it
   means to offer. Top of [[market-maker/build/next|next]].
2. **The sell gate** — `Pos − livS` for the MM's ladder and
   (mandatory) for SNT-1.
3. **The replace churn** — ~40/minute with nothing moving; diagnose
   before the reject-backoff build.
4. The Hasan message · Rob's round (now + T14, T15) · the Edwin round.
