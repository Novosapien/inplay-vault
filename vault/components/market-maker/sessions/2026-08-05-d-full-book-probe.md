---
description: "Session note, 05-08 second probe stream: depth of book is available on the FIX v8 session we already run, so the MM never needs the IOI feed"
---

# 2026-08-05d — Full book: is depth available, and does the MM need IOI?

> **Who:** Hasan + Claude (build / probe session — second of the probe stream,
> follows `2026-08-05-c-oms-entitlement-probes`)
> **Re-labelled on merge:** filed on its own branch as `2026-08-05b`. Main had
> already used the `-b` slot for the live-source-bindings session, so this note
> takes `-d`. The order inside the probe stream is unchanged.
> **Type:** build / research — live probes against the tZERO MD session
> **Refs:** `inplay-fix-gateway-go` branch `feat/md-full-book` (`e742d7a`,
> `5f3fd7a`, `f231cde`) · tZERO FIX Market Data Spec v8 · tZERO IOI Market Data
> Spec v1.2 · [[market-maker/systems/quoting-engine]]

## What we did

- Started from a question about how the platform connects to market data and
  whether we use the IOI feed. Established that we do not, and that the answer
  matters for the MM: the quoting engine's ladders, supervision's band checks
  and the synthetic market order's "N levels through" all need depth.
- Built `POST /md/probe` on the FIX gateway — one MarketDataRequest with
  caller-chosen `MarketDepth`, `MDEntryTypes` and `AggregatedBook` — deployed
  it, and fired three probes at `IPTCGIAN`, the one symbol with a live
  two-sided book.
- Committed the previous session's already-deployed 35=UPT work, which was
  sitting uncommitted in the gateway tree (its own Next line asked for this).

## What we learned

- **Full Book is supported.** `MarketDepth=0` accepted, no reject. `IPTCGIAN`
  returned **8 price levels per side** in a single fragment (`268=20`,
  `893=Y`): bids 68.15 → 67.45, asks 68.50 → 69.20, sizes stepping 85 → 155.
  Depth is a one-field change on the session we already run, not a new
  integration.
  - The ladder's regularity — 0.10 price steps, +10 shares per rung — reads
    like tZERO's own test maker seeding the QA book, not organic flow.
- **Aggregation is real, but you have to ask for it.** Without `266`, each
  level carries `299` QuoteEntryID and no order count. With `266=Y`, `299`
  disappears and every level carries **`346=1` NumberOfOrders** instead. So
  queue-depth intelligence IS available on this feed — it is gated on
  requesting AggregatedBook, and `346=1` everywhere confirms the QA book
  currently holds exactly one order per level.
- **We have only ever asked for top of book.** `MarketDepth=1` is hardcoded in
  both gateways, so the platform has never seen depth — and nothing downstream
  is wired for it: `state/book_builder.go` is dead code written for the IOI
  N/C/R model, `market.book.{sym}` has a topic and no publisher, tag `893` is
  defined and never read, and the trading service drops book subjects.
- **OHLC is a split verdict.** Entry types 4/5/7/8 are accepted (no reject
  reason 8), but the venue answers **High and Low with real values, Open with
  an EMPTY entry** (`270=0.00`), and **Close not at all**.
- **PreviousClosingPx (9846) is not on this feed**, even when asking for
  everything — matching the spec's own field-exclusivity table (9846 is IOI
  v1.2 only). `venue_quotes.previous_close` can never populate from v8;
  derive it from our own tape (`venue_ticks`) instead.
- **IOI is not worth a second session for the MM.** Its only genuine
  advantages are 9846 and **9848 InitPrx** (reference price for
  not-yet-tradeable assets — relevant to E3 and the 138 NCAA symbols sitting
  at TBA). Everything else the MM needs is v8-only: `MDEntryID` and
  `DeleteReason` for busts (supervision, T4), Security Status for halts (T5),
  Trading Session Status for session boundaries (N4/E16), imbalance and
  theoretical opening price. IOI also permits only one client connection per
  session.

## What went wrong / got stuck

- **The first probe corrupted live price data**, and the failure is the design
  lesson. The reply was folded like any other snapshot, because a 35=W is a
  35=W. `handleSnapshot` flattens MDEntries into one bid and one ask by
  overwriting as it walks them — correct at depth 1 where exactly one of each
  arrives, wrong at depth 0 where the **outermost rung wins**. `IPTCGIAN`'s
  board showed best_bid 67.45 / best_offer 69.20 instead of 68.15 / 68.50.
  - Two more failures fell out of the same message: the empty `269=4`
    satisfied the `open != nil` publish gate, so `open_price` and
    `previous_close` were written as a real-looking `0.0000`; and `387`
    TotalVolumeTraded rides the message rather than the trade entry, so volume
    was overwritten to 0.
  - Fixed with an MDReqID prefix guard (`PROBE-`). Bid/offer/last self-healed
    on the next resubscribe; the residue was repaired with a one-row UPDATE.
  - **Depth-0 traffic on the top-of-book fold path does not degrade, it
    corrupts.** Routing by MDReqID is therefore a prerequisite of the
    full-book build, not a nicety — demonstrated rather than assumed.
- A claim was written into a code comment ("the reply is NOT folded") and
  acted on before it was checked. It was false, and the code proving it false
  had already been read. Trace the write path before firing at a live venue.

## Decisions made *(mirror into [[market-maker/decisions]])*

- ✅ Full book comes from the **existing v8 session** — not IOI, not a new one.
- ✅ Depth-0 and depth-1 traffic are **routed separately by MDReqID**; the
  top-of-book path that feeds the app's price board is never modified.
- ✅ Book state is **Redis + NATS only** — no Postgres migration.
- ✅ Full book ships **feature-flagged off**, with a symbol allow-list.
- ✅ Previous close is **derived from our own tape**, not chased on the feed.
- ✅ Request **`266=Y`** on any full-book subscription — it is what turns on
  `346` NumberOfOrders.

## Questions opened / closed *(mirror into [[market-maker/open-questions]])*

- **Opened T21** _(filed as T12; re-filed on merge)_ — does tZERO permit TWO concurrent subscriptions per symbol
  on one session (depth-1 + depth-0, distinguished only by MDReqID)? Decides
  whether full book is additive or a switch-over. The Phase-0 probe used
  `SubscriptionRequestType=0` (snapshot-only) deliberately, so it created no
  standing subscription and did not answer this.
- **Closed** — "can we get depth at all": yes, `MarketDepth=0`, 8 levels a side.
- **Closed** — "can we get per-level order counts": yes, gated on `266=Y`.
- **Closed** — "should the MM use the IOI feed": no. Only 9848 InitPrx is worth
  a follow-up question to tZERO, and it is one question, not a session.
- **N13** (book feed is for the watchdog and monitoring, not quoting) still
  stands, but with a measured caveat: depth exists, is 8 deep, and is cheap to
  take, so the constraint on using it is design preference rather than
  availability.

## Addendum, 2026-08-06 — the feed is live, and a real trade exercised it

- **Full book shipped and enabled for all 170 symbols.** Depth-0 subscriptions
  (`MDB-` prefix, `266=Y`) run alongside the 170 top-of-book ones; **164 symbols
  return depth**, the other handful being the same unknown tickers the quote
  feed already rejects. Published on `market.book.{sym}` → bridge →
  `market:book.{sym}`. Gated off production in the app; the ladder renders TBA
  there until secondary markets open.
- **Depth-0 incrementals have now been OBSERVED**, which no probe window managed.
  A real buy on IPTCGIAN produced exactly three:

  ```
  279=2 269=0 270=68.50 271=0        delete: the 68.50 offer, consumed
  279=2 269=1 270=68.60 271=0        delete: the 68.60 offer, consumed
  279=0 269=0 270=68.60 271=5 346=1  new bid: the residual resting order
  ```

  Zero anomalies, zero crossed books, and the ladder, the price board and the
  tape all agree (`68.60 × 5 / 68.70 × 105`, volume 150 → 330).
- **A depth-0 delete DOES carry its price.** The refusal branch was written
  because at `MarketDepth=1` the venue omits it and depth-0 behaviour could not
  be assumed. It does not omit it. The defensive path never fires — now measured
  rather than guessed.
- **The parser fix was load-bearing, not incidental.** Every one of those
  messages puts `279` before `269`. Under the old split-on-269 logic the first
  action would have been dropped and the rest shifted by one, so both deletes
  would have applied as New/Change and the consumed offers would still be
  sitting in the book. The ladder is correct *because* of that fix.
- **T21 is effectively answered.** Both subscriptions coexisted through a live
  trade: depth-0 delivered the incrementals above while depth-1 kept the price
  board current in the same window. tZERO adds rather than replaces.
- ⚠ **Own goal worth remembering:** the first probe reply was folded like an
  ordinary snapshot and wrote the OUTERMOST rungs of a depth-0 book to the app's
  price board (`67.45 / 69.20` against a real `68.15 / 68.50`). A code comment
  asserting "the reply is NOT folded" was written and acted on before it was
  checked, and the code disproving it had already been read. Routing by MDReqID
  is now the guard, and the lesson is the ordering: trace the write path before
  firing at a live venue, not after.

## Next

- Answer **T21** with one more probe: `SubscriptionRequestType=1` at depth 0
  alongside the live depth-1 subscription, then unsubscribe with `263=2`. It
  is safe to run now that the fold guard exists.
- Then **Phase 1**: rewrite `book_builder.go` for the v8 aggregated model —
  keyed by (side, price) with `MDUpdateAction` 0/1/2 — plus `LastFragment`
  reassembly and parser capture of `346`/`299`. Phase 1 does not depend on
  T21; only the Phase-2 wiring does.
- Delete `POST /md/probe` in the same change that lands Phase 2's real
  routing. It is localhost-only on a VM with no public IP, but it is a
  diagnostic and should not outlive its questions.
