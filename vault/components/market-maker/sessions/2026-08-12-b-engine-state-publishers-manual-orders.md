---
description: "Build session for the engine half of the observability spec — mm.state and snt.state publishers, the taker's P&L meter, and the manual-order command family"
---

# 2026-08-12b — the engines start publishing, and the taker takes orders by hand

> **Who:** Claude (`engine` stream of the `admin-trading-observability-impl`
> team) + the team lead
> **Type:** build
> **Refs:** `specs/2026-08-12-admin-trading-observability/spec.md` R1·R2·R3 ·
> MM branch `feat/state-publishers-manual-orders` (4 commits) ·
> [[market-maker/sessions/2026-08-12-admin-panel-observability-discovery]] ·
> [[market-maker/decisions]] 2026-08-12

## What we did

Built the engine half of the 12-08 observability spec. Four chunks, one
commit each, on `feat/state-publishers-manual-orders`. **767 tests green,
ruff + mypy-strict clean.** Nothing was deployed — the VM was not touched
at all; the output is code, tests, a runbook and a PR.

- **R1 — the maker publishes `mm.state`** every 2nd tick (~1 s at
  TICK_S 0.5), plus a flush within one tick of a kill switch, a new
  quarantine or a new suspension. Complete projection, never deltas: a
  panel joining mid-session renders from one message. Active books only
  (non-zero net OR resting orders OR state ≠ Stable).
- **R2 — the taker publishes `snt.state.snt-1`** every ~1 s from its OWN
  asyncio task, so a HALTED bot keeps publishing. Two pieces were real
  engine work rather than plumbing: an `avg_cost` / `realized_pnl_total`
  meter, and order-state tracking (`limit_px`, `leaves_qty`, `cum_qty`,
  lifecycle state) that did not exist at all.
- **R3 — the taker's control channel accepts manual orders.** Place,
  cancel and replace, guarded, journaled `manual`, replied to on
  `snt.control.snt-1.reply.{ref}`. Accepted while halted.
- **The redeploy runbook** (`deploy/OBSERVABILITY-REDEPLOY.md`).

## What we learned

- **The 256 KB payload budget holds, with about 14% to spare.** Measured
  on the full universe quoting two-sided ladders: **208,250 bytes at 170
  books** (~9.2 resting orders each), ~220 KB extrapolated to 180. The
  shed (orders → per-book counts) exists and is tested, but should not
  fire on today's book. A deeper ladder would change that.
- **The 10%-tick-latency acceptance criterion cannot be met, and it is
  measuring the wrong thing.** The publisher costs **+1.98 ms** on a
  **4.52 ms** tick — **+43.7%**, against a bound of 10%. But the tick
  INTERVAL is 500 ms, so the loop goes from 0.9% to 1.3% utilisation and
  the heartbeat is on its own task regardless. The irreducible cost is a
  208 KB `json.dumps` (0.67 ms) plus the projection and the payload
  build; 10% of 4.5 ms is less than one encode. Escalated to the lead as
  a spec-number question — an absolute bound is the honest AC.
- **`realized_pnl_total` has two honest limits**, both now documented and
  both visible in the boot log. A fresh journal directory resets it (and
  every deploy takes one), and a §10.3 checkpoint boot UNDER-counts it,
  because only the journal tail replays and the pre-checkpoint
  `PositionRecord`s never reach the edge. The ops rule hides the second —
  `load_latest` only accepts a checkpoint of the running config version,
  and every deploy bumps it — but a same-version restart would not.
- **The taker's `PendingOrder` really was a rename away from nothing.**
  It held no limit price, no leaves, no cum and no state, because the IOC
  substitute never needed them: it cancels the remainder after 1.5 s
  regardless of progress. The order-state fold is new tracking.
- **⛔ Neither publisher can work without a NATS grant that does not
  exist**, and a missing grant is SILENT — the publish returns normally
  and the server drops the message. `market-maker` needs `mm.state`;
  `snt-taker` needs `snt.state.>` and `snt.control.snt-1.reply.>`; the
  proxy's user needs the command subject and the reply wildcard. This is
  the deploy's real blocker and it is not code.
- The venue cancel path (`snt/runtime.py`) is sound and proven — the
  halt sweep and the IOC substitute both use it. Replace scopes cleanly
  on top of it as cancel-then-new.

## What went wrong / got stuck

- The first payload-size benchmark measured the garbage collector: the
  test transport KEPT every published payload, so 200 ticks built a 40 MB
  list. Fixed with a transport that encodes (the real cost) and forgets.
- The first tick-latency benchmark measured nothing at all — a bug in the
  bench clock (`replace(microsecond=0)` before adding 0.5 s) left it
  oscillating between two instants, so no sweep ever fell due and the
  "tick" was 0.003 ms. Real ticks need the sweep.
- The first cut of the publisher built the FULL projection every tick,
  just to diff for transitions. Replaced with a cheap
  `suspended_books` read; the projection now runs only on a publishing
  tick.

## Decisions made *(mirrored into [[market-maker/decisions]] 2026-08-12b)*

Engineering mechanics, ours under the 22-07 remit line, all recorded:

- **A manual sell is always FIX side 2**, never side 5. An operator
  asking to sell has asked to reduce a holding; a short opened by
  inference is a position nobody decided to take.
- **Replace is cancel-then-new, not atomic**, and both `qty` and
  `limit_px` are required — after a partial fill, inheriting the original
  quantity would re-buy what already filled.
- **Manual orders are exempt from the IOC cancel timer** (they are DAY
  orders placed to rest) but **NOT from the kill switch** (halt and the
  T-S05 reconcile halt sweep everything).
- **The collar's last-trade fallback is age-bounded** at 🟡 1 h, because
  JETS's 18.65 was a last-trade fossil. A crossed book counts as no book.
- **`shed` is one field added to R1's payload list** — the spec mandates
  the degradation but gave the consumer no way to detect it, and an empty
  `resting_orders` array must not read as "no orders resting".

## Questions opened / closed *(mirrored into [[market-maker/open-questions]])*

- Opened: **N36** — R2 publishes ONE bot-level `activity_state`, but the
  T-F07 build derives it PER BOOK. A screen cannot see which books are
  live. Reported to the lead rather than patched; one line and one spec
  decision.
- Flagged, not opened: the 10% tick-latency AC (above) and the
  `cancel_seq` id space, which is not journaled and therefore relies
  entirely on the per-restart `SNT_CONFIG_VERSION` bump for uniqueness.
  Recorded in the runbook.

## Round two — the lead's rulings, applied the same session

The PR went up, the lead reviewed, and five things came back. All applied.

- ⭐ **The encode moved OFF the tick.** The lead asked the right question:
  the projection plausibly needs tick consistency, a 208 KB `json.dumps`
  plainly does not. Now the tick STAGES an immutable frame and the
  publisher's own task encodes and publishes it.
  **+1.98 ms (+43.7%) → +0.32–0.46 ms (+7–10%).**
  ⚠ Recorded with the caveat, because it will be misread: this reduces
  TICK latency, not event-loop blocking — asyncio does not preempt, so
  the encode blocks the same loop for the same time, and the beat is
  starved either way. What it genuinely buys is that the loop's cadence
  accounting stops absorbing encode time, and an unpublished frame can be
  SUPERSEDED by a newer one rather than published late.
- ✂ **The perf AC re-cut** to ≤ 10 ms/tick AND ≤ 5% of the 500 ms
  interval. Measured 4.92 ms / 0.98%.
- ✅ **N36 ruled: publish BOTH activity states**, never merged into one
  badge — the operator's setting at the top, the derived per-book state
  inside each book. Named apart in code (`operator_state` vs
  `BookState.activity_state`) so the two cannot be confused at the call
  site.
- ✅ **The Configuration Dictionary boundary opened**, so the cadence, the
  budget, the ceiling, the retention and the shipped on/off default moved
  there per §1.6-5. The taker's config READS the same rows rather than
  restating them.
- ✅ **Exact `nats.conf` grant lines** written into the runbook as a
  prerequisite section, with the silent failure mode stated and a
  verify-by-subscribing step. `platform` independently found the same
  failure shape: the admin proxy sat unauthorised on NATS for a week
  after the 08-05 rotation, `Authorization Violation` on its own
  `/health`, nobody reading it. That precedent is now in the runbook.
- ⭐ **`platform` then found the sharper version of it, and it is now in
  the runbook too: a publish-based check is a LIE unless it inspects
  `last_error`.** Core NATS publishing is fire-and-forget — `publish()`
  returns without raising even when the server refuses, and the
  violation arrives asynchronously as `-ERR Permissions Violation`. They
  nearly shipped a health check whose green meant "we handed some bytes
  to a socket", which is worse than no check because it is trusted. The
  fix is `last_error` + `flush()` to force a round trip; subscribing
  avoids the trap entirely.
- ⚠ **And the caveat on their own green:** the proxy connects as the
  `admin` NATS user, which likely holds broad permissions, so its
  passing check says nothing about `market-maker` on `mm.state` or
  `snt-taker` on `snt.state.>`. Those two grants are still genuinely
  owed. Each user must be observed on its own subjects.
- 📝 **Drafted, NOT applied:** an addendum proposal for
  [[market-maker/market-taker-requirements]] —
  `drafts/2026-08-12-taker-requirements-addendum-PROPOSAL.md`. The lead
  and I agreed a builder should not amend a normative go-live list
  mid-task; the reasoning is captured, George makes the call on a written
  thing.

**Final:** 775 tests green, ruff + mypy-strict clean. Still nothing
deployed.

## Round three — the Phase-1 review, ten findings

A three-agent review confirmed the gated claims empirically (it rebuilt
the 170-book stack, hammered `observe()` and proved checkpoint state
byte-identical; both transport files SHA-match main) and then found ten
things. All closed.

**The one that mattered — F1, and it is the inverse of the failure this
build calls "where the money is real".** Everything was committed BEFORE
anything reached the wire: the order tracked, the ack journaled into the
dedup map, the reply handed back — and the caller published afterwards.
A failed publish therefore produced a journaled ack, a dedup-locked ref
and an `open_orders` entry for an order that never left. R7 resolves
"landed" from the ref's PRESENCE, so it reported LANDED; the resend
replayed `{ok:true}` forever; the entry sat at `working` for good; a
cancel acked `{cancelled:true}` having cancelled nothing.

The root cause was a CONTRACT mismatch, not an ordering slip:
`open_orders` membership was evidence of engine INTENT and R7 read it as
evidence of venue SUBMISSION. Fixed with three outcomes rather than two —
confirmed / refused / **unconfirmed** — because a flush timeout genuinely
cannot be resolved either way, and `unknown` is §8.2's own word for it.

⭐ **And the fix was incomplete without a `flush()`.** Core NATS
publishing is fire-and-forget: `publish()` returns without raising even
when the server refuses, and the violation arrives asynchronously. So
"publish then confirm" would STILL have acked an order refused for want
of a grant. This is the same bug shape `platform` caught in their own
health check — in the order path rather than the observability path,
which makes it a money bug rather than a monitoring one.

**The other nine:**

- **F4** — `market.trade.>` subscribe was missing from the grants block,
  and its absence degrades Hasan's RULED ±20% collar to "skip" on every
  book without a fresh quote, reporting `no_reference` — which reads as
  "empty book", the case the fallback exists to serve. Documentation
  could not fix that, because an operator cannot tell the two apart. The
  engine now can: zero prints ever received reports `no_trade_feed`.
- **F2** — `prune()`'s only caller lived inside `state_snapshot()`, so
  `SNT_STATE_PUBLISH=off` leaked settled orders for the process lifetime.
  What made it the wrong place is *when* it bites: the off switch is the
  ROLLBACK path, taken when something is already going wrong. Moved to
  the trading tick. The runbook's "behaves exactly as before" claim was
  false and is corrected — and it now says plainly that the off switch
  does NOT disable manual orders, so with the publisher off you cannot
  see orders that can still be placed.
- **F3** — the publish task had no watchdog. It has one now, with the
  OPPOSITE answer to the beat's: one loud line and the loop continues,
  because a dead publisher must never turn an observability fault into a
  trading outage. Counters ride the operator's tick line so zero frames
  since boot is visible rather than inferred from silence.
- **F5** — every snapshot was encoded TWICE (budget check, then the
  transport). 208 KB × 2 per second on the loop the split existed to
  protect; my own AC caveat understated the cost by 2×. One encode now.
- **F6** — the taker had no budget at all, and R2's "the taker's book set
  is small" is false: **58.4 KB at 180 books**, measured. Same shed now.
- **F7** — `qty: 0` on a replace DESTROYED the resting order while
  `qty: "abc"` left it alone. Backwards: zero is what a fat finger
  produces. Validation moved above the cancel leg.
- **F8** — nothing locked the determinism property in a test. The AC
  gates a diff, which works only while someone is reading diffs.
- **F10** — a default I claimed could not drift, drifting.
- **LOWs:** the $127.50 venue cap now binds when the collar skips
  (`qty:1, limit_px:499999` passed everything); `qty` refuses a
  fractional value instead of truncating; a repeat cancel is refused
  rather than acked twice; the failure log is rate-limited.

**EC14 is a SPEC defect, confirmed:** it holds only on a same-journal
restart, and the ops rule takes a fresh journal on every restart. A drill
would PASS it while proving nothing about production — worse than not
testing it. Recommended to the lead: scope the criterion honestly rather
than build journal-cutover carryover for v1.

**Final: 795 tests green, ruff + mypy-strict clean. Still nothing
deployed.**

## Drilling the states nobody can click

The lead asked how to make the Phase-4 drill's §3.4 runnable — EC18
(`submit_refused`) and EC19 (`submit_unconfirmed`), the two manual-order
outcomes no panel action can produce, and therefore the two most likely
to be wrong in production. His constraint: **nothing ships that can break
the order path in production.**

**Both are reachable operationally. No fault-injection hook was built.**

- **EC18** — remove the taker's publish grant on `gateway.orders.mm.>`,
  leaving its reply and state subjects intact. The engine publishes,
  flushes, reads the server's `-ERR Permissions Violation` and refuses.
  Genuine path, and it doubles as proof the flush is doing its job:
  without it the publish would look successful. ⚠ Halt FIRST, or the
  strategy's own orders fail silently at the same time and two faults
  read as one.
- **EC19** — `SNT_FLUSH_TIMEOUT_S`, now ordinary dictionary-backed config
  (default 2 s). Set it low: the publish still goes out, only the
  confirmation window closes first, so the engine reports honest doubt
  about an order that really did reach the venue. That is precisely what
  `unknown` means.

⭐ **The distinction that made option 1 possible where I expected to need
option 2:** a timeout can never stop an order being published — the
publish has already happened by the time the flush runs. A low value
makes the engine PESSIMISTIC; a fault hook would make it LIE. Pessimism
is safe in production, suppression is not, so the knob needs no
production gate and the drill needs no hazardous code.

⚠ **Rejected: the firewall route.** Dropping packets to NATS also
produces `unknown` — and starves the MAKER's heartbeat on the same host,
so the gateway's dead-man sweeps its entire book after 4 s. Documented in
the runbook as not to be used.

Both procedures are in `deploy/OBSERVABILITY-REDEPLOY.md` §3b, including
panel's check that proves the design: after a forced `unknown`, restart
and confirm the row is STILL `unknown` rather than promoted to `working`.

## Round four — the adversarial review: the fix was itself unsound

I asked for an independent review of the F1 fix, on the grounds that I
could not review code where I wrote both the bug and the cure. It came
back with eight findings, four serious. **Three outcomes was the right
shape; the implementation did not deliver it.** All closed; 818 tests.

**The worst one would have fired in the state we deploy into.** REFUSED
was decided from `nc.last_error` — ONE field on a connection that also
carries `snt.state.*`, the reply lane, `order.>`, `market.trade.>` and a
JetStream consumer. With the `snt.state.>` grant missing (the state my
own runbook documents as today's) the publisher draws a fresh permissions
error every second, so the comparison was true almost always: it would
have falsely refused MOST manual orders **while placing all of them**,
then dropped every fill silently because a refused order is not tracked.
Not a race — the normal case.

**The fix is attribution by subject**, and it is sound rather than clever:
permissions are per-user-per-subject, so a denial naming
`gateway.orders.mm.new` is a fact about the CREDENTIAL, whoever's message
drew it. Residual race filed as **N37** rather than engineered away.

**"The flush proves it" was false where it mattered.** Verified in the
installed client: `_flush_pending` returns a resolved future with NO round
trip when not connected, and `publish()` in the same state BUFFERS rather
than raising. Both return cleanly for bytes that never left — and the old
code called that CONFIRMED.

⭐ **F4 was worse than the money bug.** `cancel_sent` was set before the
publish and never reset, so a refused cancel made an order permanently
uncancellable — the operator path refused every retry AND
`force_all_cancels` skipped it, so HALT and the T-S05 reconcile halt both
walked past a live resting order. **A kill switch must not consult state
written by the paths that failed.** It now filters on nothing at all.

Also: `submitted` defaulted TRUE so a crashed send re-adopted as
`working` when the honest word was `unknown`; a refused replace reported
`replaced: true`; and `unknown` never resolved without a fill — which
stranded the COMMON case, a resting DAY limit that is acknowledged and
never fills.

⭐ **The root cause was test ORDER.** The three commit methods were well
tested and the classifier choosing between them was not tested once —
every other finding lived in that gap. Writing the tests FIRST this round
changed the implementation: several failed against my intended design.
**A test written after the code, from the same misunderstanding, is the
bug restated.** Platform hit the identical thing the same day: their
fixture carried `symbol` in the envelope, the opposite of the wire, so
their test asserted the wrong shape and passed while no house fill would
ever have rendered.

## Round five — the cross-stream catch, both directions

`platform` retracted a green they had given me: **all four NATS grants are
owed, theirs included.** The `admin` user does not hold the control-subject
permissions, and their own health check had reported otherwise.

⭐ **The finding that outlives it: the check I recommended to them was
still a false green.** Capture `last_error`, `flush()` to force the round
trip, compare — same server, same logic, **green without an `error_cb`
registered, real violation with one.** Neither of us has a verified
mechanism and neither of us guessed one; the runbook records the empirical
fact and demotes the check. Verify by SUBSCRIBING remains the standing
instruction because it observes the thing rather than inferring it from a
client-side field.

**Chasing their retraction found three things in our own code:**

- **The test fixture asserted a message shape the wire never produces.**
  nats-py's parser lower-cases the whole error message before anything
  sees it; the fixture used the server's mixed-case spelling. It passed —
  the regex carries IGNORECASE — but for the wrong reason. **This is
  platform's `symbol` fixture bug, in our repo, the same day.**
- **The SUBJECT is lower-cased too.** Every subject this engine publishes
  to is already lower case so nothing changes today, but a subject
  carrying a venue symbol would silently never match, and the failure
  would look exactly like "the denial never arrived". Both sides
  normalised, with a test that fails if either stops being.
- The engine already registers an `error_cb` — but only because the
  classifier rebuild needed denials to arrive at all, not because the
  hazard was understood.

📝 Confirmed outward for platform: nothing on the engine side reads the
envelope `symbol` for order events (the order handler reads `data`, the
book and trade caches take the symbol from the SUBJECT), so their
`symbol: null` bug does not reach us.

## What we learned, across five rounds

Every defect in this build was a **reasonable simplification that is
correct in the common case and silently wrong in the case that matters** —
the ack written before the wire, a passthrough dropping fields on a falsy
`ok`, a shed frame satisfying an absence test, a cancel that resolves in
one branch only, `last_error` read as if it were per-message, a publish
check that passes when the grant is missing. None was carelessness.

⭐ **Two sharper patterns underneath it:**

1. **A fixture built from the same assumption as the code makes the test
   assert the bug and pass.** It happened to platform (`symbol` in the
   envelope, the opposite of the wire — no house fill would ever have
   rendered while the counters climbed) and to us (a mixed-case error
   message the client never produces), on the same day, independently.
   The defence is building fixtures from the SOURCE — the gateway's Go,
   the client's parser — not from one's own reading.
2. **Nobody caught their own.** The Phase-1 review caught the phantom ack;
   the adversarial review caught the classifier; platform caught our flush
   coupling; we caught their probe; they caught our fixture. Every
   significant defect this build was found by someone other than its
   author. That is an argument for the review structure, not for
   individual care.

## Next

- **The NATS grants** — now four lines, not three: `market.trade.>`
  subscribe for `snt-taker` joined the list. They gate the whole Phase-4 drill and they are the
  one part of this work that nobody can do in code. Verify by
  SUBSCRIBING, never from the engine's own logs — the engine cannot tell
  a delivered publish from a refused one.
- George's call on the taker-requirements addendum proposal.
