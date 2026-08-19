---
description: "The Go port's venue record: byte-identical on both corpora, a four-seed differential fuzz built as Phase 1's gate, and a map-order bug the random fuzz could not reach"
---

# 2026-08-18 — the Go port, Phase 1 `venue-record`

> **Who:** Claude (`/general-implementation-builder`) + George
> **Type:** build
> **Refs:** `specs/2026-08-18-mm-go-port/` (spec.md · progress.md) ·
> `Novosapien/inplay-market-maker-go` PR #7 ·
> [[market-maker/build/venue]] · [[market-maker/sessions/2026-08-18-go-port-phase-0]]

## What we did

Ported the **Venue State Record** — `mm/venue/engine.py` and
`mm/venue/backoff.py` at the pin `fd193a4` — into `internal/venue`, and built
**Phase 1's gate**, the Go↔Python differential fuzz.

What is in it: the eleven order states including `DONE_FOR_DAY`; intent
registration before the send; the event fold over `EXECUTION` and the six ack
types; the replace pair; gone-retire; the drains; `expire_all`; the two
**derived** prune indexes; and the reject backoff **indexed by security**.

**What holds:**

- The `venue` subtree of the canonical state is **byte-identical to Python's on
  BOTH corpora** — 8,090 orders across 170 books on the six-game arm, 2,931
  across two on the a2 arm.
- A **four-seed × 800-step differential fuzz** reproduces
  `canonical(state())` **at every step**, plus every read's result, plus the
  errors: 4 seeds, ~200 order lifecycles each, ~460 events each, a checkpoint
  round trip every 97 steps, and injections for duplicate envelopes, reversed
  event times, orphan acks, foreign terminal acks and must-raise operations.
- `stampAndPrune` is **flat**: ~190 ns at 15,700 orders held, ~175 ns at
  750,000. A test asserts it, because the scan it replaced was 98.4% of the
  per-ack cost on the rig.
- `make gate` clean, `make diff` clean, identical hashes at GOMAXPROCS 1/2/8.

## What we learned

### ⭐ The two corpora drive almost none of the venue record

Both journals fold byte-identically through the new engine. Both also contain:

| | a2 | six-game |
|---|---:|---:|
| `EXECUTION` events | **0** | **0** |
| `ORDER_REJECTED` (the backoff's PRICE table) | **0** | **0** |
| `ORDER_DONE_FOR_DAY` | **0** | **0** |
| `CANCEL_REJECTED` | 172 | **0** |
| terminal PRUNES | **0** | **0** |

Zero prunes because both runs are shorter than the 300 s retention window — in
the chunk whose whole headline is the prune index. And three states are
unreachable by **any** fold, whatever the corpus: `pending_submit`,
`pending_replace` and `pending_cancel`. The reconciler registers intent at
converge time, converge is edge-only, replay never re-drives it and nothing
journals the registration — the same fact that keeps Pending Submit out of
PBE/PSE (N45).

`tools/diffreplay` now **prints that list on every run**, so a green fold can
never read as coverage it did not have.

### 🔴 A Go map's iteration order leaked into `Suppression`

The bug I shipped and the fuzz caught. Python's `Suppression` carries
`frozenset[Decimal]`, and **Decimal hashes by numeric value** — so
`Decimal("77.4")` and `Decimal("77.40")` are **two rows** of the backoff's table
(its keys are `str(price)`, so the checkpoint round-trips each spelling) and
**one member** of the set the reconciler reads.

Which spelling survives is decided by the walk order. CPython dicts iterate in
insertion order, so Python's answer is deterministic. My Go version ranged a
map, so the surviving spelling **changed run to run**.

⚠ Both spellings are reachable on the real machine: a registered order's price
is quantised to two places by the quoting engine, and an **admitted** order's
price is whatever the gateway's payload said — the six-game corpus carries
`"price": "77.4"`. Fixed with an insertion-ordered price table, and `restore()`
re-inserts in the checkpoint's sorted key order because that is what
`json.loads` hands Python.

### ⚠⚠ The random fuzz could NOT reach it — 3,200 steps said nothing

Catching that defect needs two orders, on one security and side, whose recorded
prices are numerically equal and differently spelled, both rejected, and both
still inside their backoff window at one read. With the string-keyed set planted
as a defect, **4 seeds × 800 random steps missed it every time.**

So the case is now a **scripted probe** every 61 steps rather than something
hoped for. Re-plant the defect and it fails at step 187.

This is invariant 6 doing its job: the question *"could this workload have
produced the failure?"* was asked, answered **no**, and the workload was
changed. Six planted defects in total, all caught, all at a low step index —
Pending Submit counted into exposure (step 12), `DONE_FOR_DAY` folded into
`CANCELLED` (18), gone-retire disabled (45), the heap ordered by id rather than
by parsed stamp (105), a normalised backoff key (136), the string-keyed set
(187).

### ⭐ The venue record does NOT want `ChunkedLog` — measured

A2 (`docs/checkpoint-design.md`) bound every engine in Phases 1–3, and named
the venue order record as the next table to reach that scale. Measured at two
scales, M5 Pro Mac, against the 500 ms tick budget:

| | 15,700 orders (today) | 750,000 (NCAA: 2,500 acks/s × 300 s) |
|---|---:|---:|
| **snapshot — copy the record** | **1.3 ms** | **83.7 ms** ✅ |
| `State()` — build the rendering | 6.7 ms | **516.1 ms** 🔴 |
| canonical encode | 24 ms | 1,084 ms |

**A plain deep copy is affordable here where it was not for the acceptor** —
83.7 ms against the acceptor tree's 792 ms at 380 MB. The reason is structural:
`VenueOrder` is an immutable **value** struct, so copying the two map levels
allocates nothing per order and clones no decimal.

⚠ The same run found the other half: **`State()` alone exceeds the whole tick
budget** at 516 ms, so "just render it on the tick" is ruled out as firmly as
the deep copy was for the acceptor. The tick hands over the raw record and the
writer goroutine renders it.

⚠ The cost is linear in `instruction rate × venue_terminal_retention_s`, and
reaches 500 ms at about **4.5 million** orders held — ~6× the NCAA target. That
retention window is the one dial that can move this decision.

### Two smaller things

- **Python's `datetime.fromisoformat` truncates to microseconds; Go's
  `RFC3339Nano` keeps nanoseconds.** `…54.2263721Z` parses as `…54.226372` in
  Python and as itself in Go, so the prune's cutoff would differ. Latent today
  (the runtime mints 3 digits, the gateway 6) and fixed anyway.
- **The engine's four diagnostic counters are not in `state()`, so a checkpoint
  restore resets them.** Faithful in both languages and correct — they are
  diagnostics, not state — but an operator reading `terminal_prunes` after a
  restore is reading a partial count. The fuzz's first run reported 0 prunes
  while 184 orders had visibly gone, which is how this surfaced.

## What went wrong / got stuck

- The first generator run crashed because my synthetic `ORDER_REPLACED` payload
  had no `client_order_id`. Python reads that field **before** branching on
  `ack_type`, so every ack payload carries it — the real gateway's replace
  events carry the *new* id there. Worth knowing: the field is not optional on
  any ack.
- I wrote the fuzz's coverage assertion (`refuse a seed that pruned nothing`)
  and it fired on a correct run, because the checkpoint round trip replaces the
  engine and resets its counters. The assertion was right; the reading was
  wrong.

## Decisions made *(mirror into [[market-maker/decisions]])*

1. **The venue record's checkpoint snapshot is a plain deep copy, not
   `ChunkedLog`** — decided by measurement, with `State()` barred from the
   tick and the break-even (~4.5M orders held) written down.
2. **The backoff's price table keeps INSERTION order.** Not a performance
   choice — it is what decides which spelling of a numerically equal price
   survives into the set the reconciler reads.
3. **Phase 1's differential fuzz was built WITH `venue-record`, not at the
   phase boundary**, because the gate's own words are "a differential fuzz over
   the venue record" — it certifies this chunk, and deferring it would have
   left the chunk resting on two corpora that drive almost none of it.
4. **`tools/diffreplay` takes `-securities`, and the universe is part of the
   target.** The a2 corpus ran over two books, the six-game corpus over 170.

## Questions opened / closed *(mirror into [[market-maker/open-questions]])*

- Nothing new opened.
- 🔴 **STILL OPEN — N46, needs George.** AC2 requires a rig session for the
  548.5 MB GATE corpus. It blocks no build work; Phase 1 continued without it.

## Next

- **Phase 1, chunk `reconciler`.** It needs `venue-record`'s state sets, which
  now exist. Read [[market-maker/build/venue]] first — rest-until-gone, the
  move pass carrying `cum_qty + level.quantity`, post-first ordering, the
  in-flight replace occupying its destination, and the boot healer that writes
  **no** engine state.
- ⚠ The reconciler's `_ACTIONABLE` is `{ACTIVE, PARTIALLY_FILLED}` and it is
  **not** the exposure set. Widening it to include `PENDING_SUBMIT` puts N45's
  divergence straight back, through `PENDING_CANCEL` instead.
- Then `transport`, then the phase gate — which the fuzz already covers for the
  record and must be extended across the reconciler.
- Answer N46.
