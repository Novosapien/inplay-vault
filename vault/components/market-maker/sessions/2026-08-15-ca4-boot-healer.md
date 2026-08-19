---
description: "CA4: the boot healer — the venue's real MM book diffed against the record, cancel-unknowns only, and the cutover-shape rule it forces"
---

# 2026-08-15 — CA4: the boot healer (F4 / R8 / R-D05)

> **Component:** [[market-maker/market-maker]] · **Branch:**
> `fix-set/ca4-boot-healer` · **PR:** MM
> [#42](https://github.com/Novosapien/inplay-market-maker/pull/42)
> (base `fix-set/ca3-ask-cap`) · **Who:** AI session (stream-a-ca4),
> fix-set team · **Type:** build

## What we did

Built the boot healer: at boot, after the journal replay and BEFORE the
book stands, the engine reads the gateway's own MM order index and diffs
it against the Venue State Record.

- **The seam** is the gateway's `GET /orders/mm` — its PR #5, wrapping
  `LoadOpenMMOrders`, the same set the dead-man scans. ✎ It is LIVE:
  it rode the TTL binary into production as `main@a41e540` at 02:49Z
  today, which corrects the chunk brief's "not yet deployed".
- **The client** (`src/mm/adapters/gateway_ops.py`) is one bounded
  stdlib GET that never raises. Unset URL, 404, 401, 503, refused,
  timeout, non-JSON, wrong shape, a body past the 16 MB cap — each
  returns a reason a human can act on, and the engine boots on today's
  behaviour.
- **The rule** (`plan_boot_heal`, `venue/reconciler.py`) is pure. Ours
  and unknown → cancel, one loud line each. `MMSN…` (the taker) → never
  touched. `MM`-prefixed but not our scheme → LEFT resting and alarmed.
  Anything else → never touched. An unreadable entry → skipped and
  alarmed.
- 1,102 tests (1,065 + 37), ruff + mypy-strict clean. Seed §R8's seven
  cases are asserted at the VENUE INSTRUCTION STREAM, including the
  zero-heal case, which asserts nothing was published at all.

This closes [[market-maker/requirements|R-D05]] and retires **R-D06's
fresh-journal-per-deploy rule for the MAKER**. The old ceremony stays
documented as the rollback, in the engine repo's
`deploy/OBSERVABILITY-REDEPLOY.md`.

## What we learned

**1. The cutover now has TWO shapes, and mixing them is the trap.** With
the journal surviving a deploy, the config version must NOT be bumped:
`load_latest` only accepts a checkpoint written under the RUNNING config
version, so a bump rejects every checkpoint and the boot replays a
journal that now grows without bound. And the reverse still holds — a
FRESH journal must bump the version, because a fresh journal restarts
each book's quote-version counter at 1, the reconciler re-mints ClOrdIDs
the venue already remembers, and every order duplicate-rejects (the
07-08 lesson). **The journal and the config version move together.** The
runbook's §2.2 is now a two-shape table:

| | A — heal (the new default) | B — fresh journal (the rollback) |
|---|---|---|
| journal path | unchanged | new directory |
| config version | unchanged | +1 |
| `MM_BOOT_HEAL` | on | off |
| `MM_PRIOR_RUN_DIR` | not needed | the previous run's directory |

**2. The ownership boundary is the ClOrdID scheme, and nothing else.**
`MM` + 16 lowercase hex is a SHA-256 tail; the taker mints `MMSN` + 14
hex, which fails the hex test on its SECOND character. Both are 18 chars
and both start with `MM`, so the boundary looked fragile until it was
written down — it is not, and a test now feeds the taker's own
`mint_id` to the classifier rather than a copy of the scheme. We
deliberately do NOT also gate on the entry's `user_id`/`bot_id`: the id
is already the strongest proof available, while an index that stopped
populating `user_id` would silently heal nothing. Adding that gate could
only add a failure mode.

**3. "Known to the record" had to be chosen, not inherited — the
exposure-set lesson for the THIRD time in one build.** The answer is
non-terminal orders only, i.e. `open_orders`. Not §4.4's
`_EXPOSURE_STATES` (that answers "could this cost us money"), not the
reconciler's `_ACTIONABLE` pair (that would draw a second cancel for an
order already leaving), and not "any id the record holds" — a
TERMINAL-in-record order that the venue still shows OPEN would then rest
for ever, because the reconciler only ever sees `open_orders` and the
record drops the row at the 300 s retention window.

**4. The healer must write NO engine state, and that turned a spec
sentence into a design decision.** See below.

## What went wrong / got stuck

**The spec's "retire locally" cannot be built as written.** R8 and the
chunk brief both say a known-but-absent order is "retired locally". A
local retire writes boot-time state out of an HTTP snapshot, and replay
has neither the gateway nor the snapshot — so the same journal would
rebuild a DIFFERENT venue book and AC9's settled-book claim breaks on
the very next drill.

It is built as a CANCEL instead: the healer sends one, and the venue's
own answer (`ORDER DEAD` / `UNKNOWN ORDER`) retires the order through
the existing journalled `[gone-retire]` path. Same outcome, journalled,
replay-identical — and strictly safer, because the index is a SNAPSHOT
whose own route documents that the caller owns staleness. An order
submitted microseconds before the call can be missing from it, and
retiring on that evidence would forget a REAL resting order and repost
the level — the 19-doubled-levels defect from 07-08. A cancel gets the
truth back either way. Flagged to the lead before building, and
**APPROVED by the lead the same day as the design** — "strictly better
than the spec's local retire"; the lead carries the ✎ into `spec.md`.

**A test that proved nothing, caught by mutation.** The first version of
"the healer writes no engine state" listed every record order in the
index, so it never exercised the absent branch — a healer mutated to
retire locally passed it. Fixed to cancel in both directions; the
mutation now fails it.

**A real-socket test poisoned three unrelated tests.** An in-process
HTTP server makes the process multi-threaded for the rest of the
session, and `write_checkpoint_detached`'s fork then emits a
`DeprecationWarning` on the forked-checkpoint tests — a warning that
reads exactly like "CA4 broke checkpointing". The real-socket proof was
moved OUT of the suite and run standalone (success in 7.9 ms, headers
really sent, the 404 arm, the byte cap). Worth remembering: a test can
change process-global state that no assertion of its own touches.

## Decisions made *(mirror into [[market-maker/decisions]])*

- The healer writes no engine state; every consequence enters through a
  journalled venue event. Known-but-absent is proved dead with a cancel,
  never assumed dead.
- "Known to the record" is the non-terminal set (`open_orders`),
  explicitly chosen.
- Ownership is the ClOrdID scheme alone; the universe does NOT narrow it
  — an own-scheme order on a book this run does not quote is still ours
  and still unmanaged, so it comes down, with its symbol named in the
  log.
- The journal and the config version move together (the two cutover
  shapes above).

## Questions opened / closed *(mirror into [[market-maker/open-questions]])*

- **Opened (for the GATE, not an external):** the heal's RETURN traffic
  is one venue event per cancel. A boot after a dead-man sweep can
  cancel the whole record (~1,660 orders on today's universe), and those
  answers arrive as acks against the runtime's 512-per-tick drain cap.
  At CB1's pre-CB4 9.893 ms/ack that is ~5 s of drain in one tick, which
  is the beat-stall threshold; at CB4's post-fix cost it is not close.
  The GATE's drill should read the heal's own numbers off the boot log
  and confirm the beat holds.
- **Closed:** R-D05 (a boot reconciles the venue's truth against the
  record) — built, tested, not deployed.

## Addendum — review-ca4 came back: two HIGHs, both misconfiguration-triggered

The reviewer's verdict on the design was clean (the ownership boundary
survived 25 hostile id variants, the fail-open survived 26 poison
inputs). The two HIGHs were both about the CLIENT, both probe-verified,
and both had a whole-book blast radius. **1,119 tests** (1,102 + 17);
every probe shape is now a test.

**HIGH-1 — absent is not null, and the difference is a whole book.** A
200 carrying `{"status":"ok","count":40}` — no `orders` key at all —
read as "the venue holds no MM orders", which is exactly the input that
makes the healer plan a cancel for the ENTIRE record. A sentinel now
separates ABSENT (a shape error → no heal) from an EXPLICIT null (Go's
nil slice → genuinely empty → acted on), and the `count` field the
client was discarding is cross-checked against the list it came with.
⭐ **The general lesson, worth carrying:** where the DESTRUCTIVE reading
and the "no data" reading are the same value, they have to be told apart
at the PARSE — no downstream check can recover the distinction.

**HIGH-2 — `timeout=` is per socket operation, not a budget.** A server
trickling one byte at a time never trips it; the probe ran **19.09 s at
timeout=0.5**, synchronously, on the event loop, inside the gateway's
30 s boot grace. Bounded twice now: the body is read in chunks with the
wall clock tested between them (this ends the WORK), and the whole read
runs in a worker thread under `asyncio.wait_for` (this ends the WAIT,
because a thread cannot be cancelled). The runbook's "a sixth of the
boot grace" is a property of the code now rather than a hope about it.
✎ Precision on the blast radius: during BOOT the engine's beat task has
not started yet, so what this protects at boot is the 30 s GRACE; beat
starvation is the same hazard anywhere else.

**MED-1** the opener refuses 3xx (a 302 had walked the `X-Ops-Key` to
another path) · **MED-2** a publish that dies mid-heal reports
**PARTIAL** with sent-of-planned, because "the engine boots on today's
behaviour" is a lie about a part-healed book · **MED-3** a NaN timeout
parsed fine and made every deadline comparison False — refused by name ·
**LOW-1** an id listed twice is cancelled once (two identical cancels
mint the same request id) · **LOW-2** the runbook's sample numbers are
marked illustrative.

⭐ **One finding the suite made, not the review.** `build_opener()`
installs a default `ProxyHandler`, and constructing it calls
`getproxies()` — on macOS that reaches into SystemConfiguration and
leaves the process multi-threaded, enough that a later `os.fork()`
raises 3.12's DeprecationWarning. **This engine forks for every §10.3
checkpoint**, so an import-time system lookup that makes the process
fork-hostile is a real cost. Passing an EMPTY `ProxyHandler` removes the
lookup — and stops an `http_proxy` in the environment routing an
ops-key'd request through a third party, which is MED-1's shape again.
The boot read's worker thread is retired on every path for the same fork
reason. The trail started as three DeprecationWarnings on unrelated
checkpoint tests; the honest read of a warning on someone else's test
was worth the twenty minutes.

## Next

- F5's review pass on PR #42 (the "prove it dead" deviation is ruled —
  approved by the lead 15-08, ✎ into `spec.md` is the lead's).
- The GATE owns AC8's remaining half: the rig drill with planted orders,
  the season-scale (≥1 GB) boot timing, and one real-VM cutover WITHOUT
  a fresh journal — boot clean, book stands, taker unaffected, no
  reconcile halts in the first 30 minutes.
