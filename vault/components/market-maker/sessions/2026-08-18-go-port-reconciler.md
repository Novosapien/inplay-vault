---
description: "Porting the reconciler and the boot healer, and the discovery that a random fuzz missed four known defects including the one that doubled 19 live levels"
---

# 2026-08-18 — the Go port, Phase 1 `reconciler`

> **Who:** Claude (`/general-implementation-builder`) + George
> **Type:** build
> **Refs:** `specs/2026-08-18-mm-go-port/` · Go repo PR #9 ·
> [[market-maker/build/venue]] ·
> [[market-maker/sessions/2026-08-18-go-port-venue-record]]

## What we did

Ported `venue/reconciler.py` at the pin: the four-pass diff (keep → move →
post → cancel), post-first ordering, deterministic ClOrdID minting,
`cancel_everything`, and the **boot healer** with its eight verdicts.

Extended Phase 1's gate — the Go↔Python differential fuzz — across all of it.
Each seed now drives about **60 reconciles** against synthetic Target Order
Books, plus the sweep, the healer over a deliberately hostile index, and both
ClOrdID functions. Every result is compared byte for byte, including the
healer's own reason strings.

**Nineteen planted defects, all caught** — the move carrying the old remainder
(07-08h), an in-flight replace not occupying its destination (08-08),
`_ACTIONABLE` widened to `PENDING_SUBMIT` (N45), cancel-before-post (N12), the
taker's ids no longer recognised, and fourteen more.

## What we learned

### ⚠⚠ Four of those nineteen were MISSED first time

**This is the finding, not a footnote.** Each defect was planted, watched to
pass over **4 seeds × 800 steps**, and only then closed:

| the case | why the random draw missed it |
|---|---|
| two spellings of one price | two orders, one book and side, numerically equal prices spelled differently, both rejected, both suppressed at one read |
| an in-flight replace's **destination** as a wanted level | the ladder reused resting prices and never `pending_price` |
| a reconcile while a cancel target is suppressed | it had to hit the same book inside a 2–60 s window |
| a ladder asking for a price the venue **just** rejected | one value in ~1,000 the generator can mint, on the right side, in the window |

⚠ **The second of those is the 08-08 defect** — the one that put 19 doubled
levels across the six QA books live. The fuzz was driving replaces, and reading
`pending_price` back, and still could not see it, because the target ladder had
no reason to ask for that particular price.

Three of the four are now **queued**: a reject or a cancel-reject schedules the
reconcile that must observe its own suppression. The fourth is scripted.

**The rule this establishes:** a random fuzz is not automatically a covering
fuzz. The only way to know is to plant each known defect and watch whether the
fuzz passes. The vault already holds the defect list — nobody had turned it into
a coverage checklist.

### ⚠ A BAD PROBE passed, and looked like coverage

My first attempt at testing send order reordered three independent append
statements. That changes nothing — the three instruction lists are separate
fields — so it "passed", and a less careful reading would have filed it as
proof that post-first was tested.

⭐ Chasing why surfaced a real design flaw. Python returns **one ordered tuple**,
so post-first is carried by the data. The Go version had three buckets, which
moved that contract into the caller's head — where contracts go to be
forgotten. `Instructions.All()` now reconstructs the sequence, the fuzz compares
it, and a genuine reorder fails at step 12.

**A probe that passes is only evidence if the probe is known to bite.**

## Decisions made *(mirror into [[market-maker/decisions]])*

1. **Post-first belongs in the data, not in a convention.** The Go reconciler
   exposes the ordered sequence, and that is what the runtime sends.
2. **A reject queues the reconcile that must observe its suppression.** The
   backoff's two tables are only tested if something asks again while the
   window is open, and randomness does not reliably arrange that.
3. **Every defect in the vault's history is a coverage requirement.** Before a
   chunk's gate is called clean, each recorded defect of that subsystem gets
   planted and the fuzz must catch it.

## Questions opened / closed

- Nothing opened, nothing closed.

## Next

- **Phase 1, chunk `transport`** — the last of the three. One queue, one writer
  task, strict FIFO, because **post-first ordering survives onto the wire only
  if the transport preserves it**. Plus `account` (FIX Tag 1) on NEW only, the
  price-as-JSON-float rule, and the poison-versus-fatal boundary.
- Then Phase 1's gate is complete and Phase 2 begins.
