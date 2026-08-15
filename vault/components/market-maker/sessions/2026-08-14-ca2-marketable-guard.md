---
description: "Fix-set chunk CA2 (F3/R-Q09): the flagged, pre-flight, net-of-own marketable guard at the converger, plus the verified market.book feed coverage"
---

# 2026-08-14 — CA2: the marketable guard at the converger (F3 / R-Q09)

> **Component:** [[market-maker/market-maker]] · **Chunk:** CA2 of the
> fix-set (`specs/2026-08-14-mm-python-fix-set`) · **Branch:**
> `fix-set/ca2-marketable-guard` · **PR:**
> [inplay-market-maker #34](https://github.com/Novosapien/inplay-market-maker/pull/34)
> (base `fix-set/ca1-anchor-seed` — stacked) · **Nothing deployed (R11).**

## What we did

Built R-Q09: the engine must never publish a book whose own batch prices
into the live venue touch.

The defect is the one from 08-09. The engine prices from its own
valuation and never from the book, so its bids can be marketable against
stale third-party asks on every repost. A COWB bid at 76.04 swept 8
levels, 920 shares, **$50,366** — the market maker taking liquidity while
intending to rest.

The fix is one question per book, asked between the reconciler's diff and
the **first register**: does any submit or replace price at or through
the live opposite touch, net of our own resting quantity? Yes means the
whole batch waits — nothing registered, nothing sent, the target left
staged for the next pass. Equal price counts as through, because at the
touch we are a taker.

Four pieces:

1. `src/mm/venue/tob_cache.py` (new). `TOBCache` holds the last
   `market.book.{symbol}` per symbol with its receive time, mirroring the
   taker's `_BookCache`. `MarketableGuard` is the rule. `subscribe_books`
   opens one subject per symbol.
2. `src/mm/venue/sync.py`. The pre-flight call before the first register,
   and the `refused` counter.
3. `src/mm/runtime/compose.py`. Construction behind the flag, and
   `Stack.tob_cache`.
4. `src/mm/runtime/__main__.py`. The subscription, the
   `MM_MARKETABLE_GUARD` row in the operator env table, and `refused=` on
   the tick line beside `MISSED_SWEEPS=`.

34 new tests. 966 total (base 932), ruff and mypy clean, replay equality
green.

## What we learned

**The `market.book` feed is live and load-bearing — the vault said the
opposite.** The step-1 coverage check was the spec's own first task, and
the answer changes a standing fact. The deployed gateway runs:

| Setting | Deployed value |
|---|---|
| `TZERO_MD_FULL_BOOK` | `true` |
| `TZERO_MD_BOOK_SYMBOLS` | `*` (every symbol) |
| `TZERO_MD_BOOK_REPUBLISH_SEC` | `5` |

So every symbol publishes on change plus a 5 s republish of each
non-empty book. The old line — "`market.book.*` is defined and never
published, do not build against it" — described the pre-08-08 world. It
is now struck through in both [[market-maker/decisions|decisions.md]] and
[[market-maker/build/venue|build/venue.md]]. The taker has been gating
every order on this feed for days; the guard reads the same one.

**Subscribe per symbol, never `market.book.*`.** A NATS wildcard matches
ONE token and this venue's twins carry a dot (`IPTCRAVE.TEST`), so a
wildcard silently misses them. The taker already subscribes this way.

**The venue's book is anonymous, so the touch must be netted (review
H5).** A level shows a price and a total size, never whose. Judging a new
bid against the raw ask touch would refuse us against ourselves — and the
commonest case of that is exactly what the machine does all day:
repricing a stale ask while posting a bid that crosses where the stale
ask still sits. Each level is netted against our own resting quantity;
a level that nets to zero or less is skipped for the next one down.

**A pending replace counts at its OLD price, never its destination.** The
destination is recorded on the order (`pending_price`, the 08-08
double-post fix) but it is not in the venue's book until the venue acts.
Subtracting quantity from a level we do not occupy is the one error with
teeth — it would let a genuine external touch read as ours and put the
$50,366 sweep straight back on the wire.

**The placement is forced, not chosen.** Between the diff and the first
register is the only seat that keeps both existing invariants. A partial
register would leave the Venue State Record holding intent for a batch
that never went (`[register-then-send]`). A partial send splits a book
across passes, and submit ClOrdIDs mint by POSITION in the unmet list, so
a re-diff after a partial send collides with ids the venue already holds
— plus a half-posted ladder is one-sided exposure (`[atomic-book]`).

**Ingest must not parse.** At 180 books the feed is hundreds of messages
a second arriving on the client's IO task — the same task the heartbeat
rides. CB1's profile says tick time is the scarce resource (the venue ack
drain is 98.1% of it). So the callback does one dict write of the raw
bytes plus a receive time, and the JSON is decoded only when the
converger actually asks for that book, memoised per message. A book
nobody quotes costs a dict write. The guard itself is O(instructions) per
book per pass — both touches computed once, then one comparison per
instruction. **No per-ack work anywhere**, per CA1's standing lesson.

## What went wrong / got stuck

**The first CA2 worker died on an API timeout at ~21:29Z mid-build.** The
work survived as uncommitted changes in the worktree — a new
`tob_cache.py`, edits to `sync.py`, `compose.py` and `__main__.py`, and
the test file. This session recovered it rather than rebuilding: the
diffs were read, kept, rebased onto the base branch's new commit
(`4a7c484`, the review-f2 anchor-reader hardening), and finished.

The rebase produced **one conflict, in `compose.py`, and it was purely
additive** — the base had added an `[anchor-seed-remintable]` note in the
same Notes block where the guard's `[marketable-guard]` note went. Both
were kept. Nothing else in the recovered work needed changing to apply.

**The recovered work did not pass the gates as found.** Four ruff errors
(unsorted `__slots__`, a useless `return None`, an unused unpacked test
variable) and two mypy errors, both real:

- `instruction.price` on the `SubmitOrder | ReplaceOrder | CancelOrder`
  union. The side lookup was in a helper, so mypy could not narrow the
  type through it. Restructured into an inline `isinstance` chain, which
  narrows properly and reads better; the helper is gone.
- The `_Subscriber` Protocol did not structurally match nats-py's real
  `Client.subscribe`, which takes `queue` **between** the subject and the
  callback. `cb` is now keyword-only in the Protocol, which is how the
  call site passes it anyway.

**One stale number was carried into the code notes from the brief**: a
"15 s republish". The verified deployed value is 5 s
(`TZERO_MD_BOOK_REPUBLISH_SEC=5`). Corrected.

## The honest cost — recorded because it WILL be seen

Fail-open is the standing rule. No book, a message older than
`tob_stale_after_s` (🟡 30 s), an unparseable payload, a visible side
entirely ours — all mean no opinion, and no opinion means SEND. The
asymmetry is deliberate: refusing on absent data would silence quoting
for as long as the feed is quiet, and a market maker that stops quoting
has failed at its job.

But the depth feed has two proven failure modes and the guard inherits
both:

- **Fresh-but-EMPTY** (10-08 — the feed served empty books while the
  venue held full ladders). Reads as no opinion, so the guard is simply
  absent. Fail-open, as designed. Harmless.
- **Fresh-but-PHANTOM** (08-08 — a JETS ask at 45.44 shown for ~5 min
  while a journal-confirmed bid at 45.45 rested unfilled). **This one
  bites.** The guard refuses against a touch that does not exist, and
  because a refusal keeps the target STAGED, that book stops converging
  until the phantom clears.

Two levers for the phantom case: `MM_MARKETABLE_GUARD=off` retires the
guard entirely without a code deploy, and **`POST /md/book-resubscribe`**
on the gateway is the feed's own heal. An operator hitting a stuck book
should reach for the resubscribe first — it fixes the feed rather than
blinding the guard.

Logging is rate-limited for the same family of reason. A phantom book
would refuse every pass, twice a second, on every book it touches, and
the 08-13 fire loop proved a log flood starves the heartbeat and feeds
itself. A security's first refusal prints, then every fiftieth, carrying
`repeats=` so the silence between is not read as the problem going away.
Each `MARKETABLE_REFUSED` line names the price we were about to publish
AND the touch that refused it, with the net-of-own quantity — a phantom
is diagnosable from one line, without a second tool.

## Decisions made

- **The guard acts at the venue EDGE only, never inside checkpointed
  state.** It reads a live feed and a clock, so it cannot live in the
  deterministic core (§1.6-4). It is legal on the converger's send path
  because that path is already edge-only: cycles STAGE targets and
  `converge()` decides what reaches the wire and when. Replay never
  re-drives `converge()`. Nothing the guard holds is written to
  `Orchestrator.state()` — the cache lives on the composition, the
  counters on the guard and the driver, and the checkpoint's five members
  never see them. **AC9 holds by construction, not by measurement**, and
  a test asserts it.
- **The unit of refusal is the BOOK, not the instruction**, and it is
  decided before the first register. See "the placement is forced" above.
- **A cancel-only batch can never refuse.** A suspension sweep is risk
  reduction and is never held back.
- **`MM_MARKETABLE_GUARD=off` is total** — no cache, no guard, no
  subscription, no comparison, no cost. Restart-applied, like
  `MM_STATE_PUBLISH`.
- The staleness bound is the dictionary's `tob_stale_after_s` (🟡 30 s,
  the taker's own number). No literal in the code.

## Questions opened / closed

- ✅ **CLOSED — does the deployed gateway publish books for the MM
  universe?** Yes. `TZERO_MD_FULL_BOOK=true`, `TZERO_MD_BOOK_SYMBOLS=*`,
  `TZERO_MD_BOOK_REPUBLISH_SEC=5`, direct-verified on the VM 14-08. The
  guard would have been permanently "no opinion" had this gone the other
  way, so it was the spec's first task. It is a GO.
- 🟡 **OPEN — the phantom-book interaction is untested against a real
  phantom.** The failure mode is reasoned from the 08-08 incident, not
  reproduced. The mitigations exist (the flag, the resubscribe route);
  what is missing is a live observation of the guard meeting a phantom.
  Watch `MARKETABLE_REFUSED` lines on the first live night.
- 🟡 **OPEN — `tob_stale_after_s` is 🟡, inherited from the taker.** 30 s
  was set on the taker's 08-08 evidence, not measured for the maker. With
  a 5 s republish, 30 s tolerates six missed republishes before the guard
  goes quiet. Nobody has argued that number for the maker's side.

## Addendum — the stall alarm (lead-directed, same session, same PR)

The lead accepted CA2, approved the `__main__.py` deviation, confirmed
the drill reading, and ruled one cheap follow-up onto N41: **the stall
needs a LOUD signal, not just a climbing counter.**

Built as `MARKETABLE_GUARD_STALLED`. After `marketable_stall_passes`
consecutive refusals of the SAME book, the guard logs once per episode.
The line names the book, the side and price we are trying to publish,
the touch holding it with its net-of-own quantity, and **the heal in
priority order** — `POST /md/book-resubscribe` first because the feed is
the likelier fault, `MM_MARKETABLE_GUARD=off` second. The operator
reading it at 3am did not write the guard.

**The bound is derived, not chosen.** The converger runs on its own task
at `converge_interval_s` (**0.25 s**), and a refusal costs no budget, so
a LIVE book is re-judged every pass. 30 s ÷ 0.25 s = **120 passes**. Long
enough that a fast market crossing our staged price for a few passes
stays quiet; short enough that a stuck book is heard about inside half a
minute. A test pins `passes × cadence == 30.0`, so moving either number
fails the build rather than silently drifting from the comment.

**Once per episode, guaranteed by arithmetic rather than a flag.** The
streak rises by exactly one per refusal, so it equals the bound on a
single pass. A clean converge clears the streak, which both ends the
episode and arms the next. This is deliberately the same shape as
`CONVERGE_STALE`'s `alarmed` flag in `runtime/loop.py` — there was
already a precedent in this codebase for a once-per-episode outbound
alarm, and matching it was cheaper than inventing a second idiom.

Two honest notes recorded in the code:

- **This is the one place `tob_cache.py` prints** rather than returning a
  line for the driver to print. The episode lives in the guard's own
  streak and nothing else can see it cross. It is also forced: `sync.py`
  is frozen for CB2 (see below).
- **The alarm changes nothing about what is sent.** It is an alarm, not a
  mode, exactly like `converge_staleness_alarm_s`. The automatic exit
  stays undesigned and stays N41.

⚠ **A dictionary one-row exception**, explicitly approved by the lead:
`marketable_stall_passes` in `mm/config/dictionary.py`, 🟡 OURS, with the
derivation in the comment and a validation predicate. `parameters.md`
carries its row.

⚠ **`venue/sync.py` is now frozen for me** — CB2 stacks on this branch
and will edit it. The alarm sits entirely in `tob_cache.py`,
`compose.py`, `dictionary.py` and the tests. Nothing in `sync.py` moved,
so CB2 rebases onto an unchanged file.

Gates after the follow-up: **972 tests** (966 + 6), ruff and mypy clean.

## Addendum 2 — the phase review, and the HIGH it found

The #34 phase review traced placement, atomicity and determinism clean,
and found **one probe-confirmed HIGH plus three MED and three LOW**. Six
are fixed in the same PR.

### HIGH-1 — the guard was netting orders that were not in the book

The netting counted every non-terminal order, which silently included
**`PENDING_SUBMIT`** — an order we have published but the venue has NOT
acknowledged, and therefore one that is not in the book we are netting
against.

Every converge pass creates that state for **~14–264 ms** (register →
ack → market-data propagation). On a fast move the guard subtracted
quantity from a level it did not occupy, the level netted to zero, the
walk stepped **past a real external touch**, and the batch went. The
reviewer's probe sent a sell at 75.50 into a live external 76.00 bid:
**the $50,366 shape, in the exact scenario R-Q09 exists for.** The guard
was failing at its one job in the window it most needed to work.

The fix nets only what the venue has acked — `ACTIVE`,
`PARTIALLY_FILLED`, `PENDING_REPLACE`, `PENDING_CANCEL`.

**The lesson worth keeping: §4.4's exposure set is not a book-presence
set.** `_EXPOSURE_STATES` answers *"could this order cost us money"*, and
`PENDING_SUBMIT` and `UNKNOWN` rightly belong to it. The guard asks a
different question — *"is this quantity IN the published book"* — and for
that question those two states are exactly the wrong answer. Two
plausible-looking questions about the same orders, with different
answers; reaching for the existing set would have been the natural move
and would have kept the bug.

The error the fix LEAVES is the safe one: where the venue has published
our order but our record has not caught up, we now under-subtract, count
our own liquidity as external, and refuse a book we could have sent — one
wasted pass, recovered by the retry.

⚠ **The opposite residual stays open and is recorded, not fixed:** once
acked, we subtract an order that market data may not have published yet,
which over-subtracts and biases toward SENDING. It is bounded by the
feed's propagation delay rather than the whole ack round trip, and
nothing in this process can know the book better than the book does.

### MED-1 — the guard could kill the converge task

The guard runs INSIDE the converger's task, so an escaping exception does
not fail one book: it kills the task that converges **every** book, and
the engine goes quiet while looking healthy. Two probes reached it —
`data` arriving as a LIST (`AttributeError`, outside the parse's except
tuple) and a **single-level NaN price**, which slips past the parse
precisely because sorting one level never compares it, then raises at the
comparison.

`refuses()` is now a boundary; the rule moved to `_verdict()`. Anything
escaping is counted, logged, and turned into SEND.

**A test caught a second-order version of the same mistake:** the failure
handler itself called `self._symbols.get(...)` and could throw. A handler
that runs *because* something threw may not touch the machinery that
might have thrown. It now uses only the security id.

### MED-2 — a blind guard looked exactly like a quiet one

A guard holding no books and a guard with nothing to refuse are
identical in the log: both silent. The first means R-Q09 protects
nothing, and that is not hypothetical — the subscription lives in
`__main__`, so a stack built without it reads "no book" for ever.

`MARKETABLE_GUARD_BLIND` now alarms once if the guard has never held a
book. The bound is **time** (the cache's own staleness window, reused so
there is no second number), because the feed republishes on a timer and a
young engine that has not been told anything yet is not blind.

The tick line gains **`books=`**, a LIVE gauge. This is the part worth
remembering: *a dead feed freezes every cumulative counter wherever it
stopped*, so `messages` looks healthy forever while nothing arrives.
Only a gauge falls to zero.

### The rest

- **LOW-1** — one refused subject must not cost the other 179;
  `subscribe_books` and `__main__` both survive and say so loudly. An
  unguarded engine still quotes; an engine that will not boot does not.
- **LOW-2** — the warm-cache boot test: a phantom touch at boot holds the
  WHOLE opening ladder, staged, and stands once it clears. Asserted on
  the instruction stream, per `[seed-silent]`.
- **LOW-3** — the test client's `cb` is keyword-only, like the real one.
- **Scope recorded in the PR:** the guard's claim is **external-only**.
  It does not claim to prevent self-cross — tolerated per N12
  `[post-first]`, and that decision's business, not this guard's.

### Not done, and why

- **MED-4** (cap books EXAMINED per refusing pass, bounding full-universe
  rediff CPU) belongs in `converge()`, and `venue/sync.py` is frozen
  while CB2 stacks on this branch. Flagged to the lead with a proposed
  patch rather than risking a collision — it is a CPU bound, not a
  correctness fix. ⚠ Whoever takes it should note the fairness trap: the
  converger's cursor only advances on SERVED books, so a persistent set
  of refusing books at the head of the rotation can starve the ones
  behind them, and a naive cap makes that worse rather than better.
- **MED-3** (whether a refusal should still let the batch's CANCELS
  through) is George's call on batch semantics — untouched.

Gates after the fixes: **986 tests** (932 + 54), ruff and mypy clean,
replay equality green.

## Next

**F5 real-review pass on PR #34** before it joins the merge train. Then,
whenever the fix-set reaches a live night, the watch is now one line
rather than a trend: any **`MARKETABLE_GUARD_STALLED`** in the log is a
book that has published nothing for ~30 s. Reach for
`POST /md/book-resubscribe` first, `MM_MARKETABLE_GUARD=off` second. A
climbing `refused=` with no stall line is the guard working normally.

**Still owed on N41: the automatic exit** — a forced send after N
refusals, a cross-check of the touch against our own journal-confirmed
resting orders (a phantom contradicts a live unfilled order at a better
price), or auto-firing the resubscribe on a streak. George's call.
