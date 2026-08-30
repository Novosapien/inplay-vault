---
description: "The register of Python engine changes made after the Go port's pin — what each one is, why it exists, and what the Go implementation owes before it can replace Python"
---

# Go Port — Divergence Backlog (Python → Go)

> **Component:** [[market-maker/market-maker]]
> **Purpose:** ONE place for every change made to the **Python** engine
> **after the port's pin**, so the Go implementation can be brought level
> deliberately instead of by archaeology. George's rule, 30-08: *"make a
> note of any divergences from the original Python one and the Go one, so
> when we have stabilised the Go one we can add in the new features we
> have added to the Python one."*
> **Direction:** this file is **Python → Go** — what Go OWES.
> Its sibling [[market-maker/go-port-findings]] runs the other way — what
> the port found WRONG in Python.
> **Born:** 2026-08-30.

## How this file works

1. **The pin is `fd193a4`** (tag `mm-python-fix-set-complete`), recorded
   in the Go repo's `README.md`. Everything in `src/mm` and `src/snt`
   after that commit is a divergence and belongs here.
2. **One row per change.** Name the commit, what it does, and whether Go
   must reproduce it, may skip it, or must decide.
3. **Add the row IN the session that makes the change.** A divergence
   recorded later is a divergence reconstructed from memory.
4. ⚠ **Differential replay cannot see these.** The harness compares the
   two implementations at the pin. A Python change after the pin makes
   the two diverge BY DESIGN, so the test suite goes quiet exactly where
   this register has to speak.
5. **Status:** 🔴 owed · 🟡 in progress · ✅ level · ✂ Go deliberately
   does not take it.

**Refresh the list with:**

    git -C inplay-market-maker log --oneline fd193a4..HEAD -- src/mm src/snt

---

## Owed

| Commit | Date | What it is | Go's obligation | Status |
|---|---|---|---|---|
| `68b76a8` | 20-08 | **Edwin's 20-08 parameter answers.** Dictionary rows only, no new mechanism: `min_width_ticks` 1 → **25** · `min_levels`/`max_levels` 3/6 → **1/1** · `base_size` 10,000 → **550** · `min_quantity` 1,000 → **100** · `material_qty_change` 500 → **50** · **NEW** `skew_reference_shares` 48,000 · **NEW** `defensive_width_floor_ticks` 50 and `overnight_width_floor_ticks` 100 | **MUST reproduce.** Values, not logic — but they change every quoted price, so a differential run against an un-updated Go engine mismatches on every book. ⚠ `min_levels`/`max_levels` is SUPERSEDED by `f9eec8b` below; take the final value, not this one | 🔴 owed |
| `76341d3` | 21-08 | **Alien traffic drains instead of killing the engine.** The 20-08 incident: mm-2 (the **Go** maker) quoted `.TEST` on the shared MM gateway, the gateway broadcast `ORDER_ACCEPTED` namespace-wide, mm-1 journalled it, could not resolve the security, raised `UnknownVenueOrder` and **crash-looped on replay at every boot** (journal `supervised43`, preserved; NRestarts=25, dead-man fired 21 times). The old rule assumed one writer per namespace | **MUST reproduce.** ⚠ **The Go maker CAUSED this incident** — running Go beside Python on one namespace re-creates it in the other direction. Reproduce before the next side-by-side run, not before cutover | 🔴 owed — **blocks shadow running** |
| `d162d8c` | 21-08 | **The alien drain's unenforced invariant, pinned by test.** The drain keys on RESOLVABILITY, so another writer's order on a symbol we quote IS admitted into the record, where the reconciler may cancel or reprice it. Safe only while the writers' universes stay disjoint, and **nothing enforces that**. Also marks the engine-level fill drain live | **MUST reproduce**, and inherit the open item with it: the structural fix is a per-writer `MM_USER_ID` (the gateway routes `order.{userID}.*`), queued behind Hasan's `HOUSE_EGRESS_SUBS` | 🔴 owed |
| `f9eec8b` | 26-08 | **Rungs go back to the drawn 1–3.** George, superseding Edwin's 20-08 "one rung, do not build the optionality" — the live one-rung book could not heal itself | **MUST reproduce**, and it OVERRIDES `68b76a8`'s `min_levels`/`max_levels` 1/1. Take 1–3 | 🔴 owed |
| **N75 — the guard's granularity** | ruled 30-08, **unbuilt** | George's 23-07 ordering rules, promoted out of [[market-maker/learnings]] on 30-08: retreating side first · cancels before creates at overlapping prices · advancing side deepest-first, top-of-book last · **micro-barrier only on the specific orders an advance would cross**. Replaces N12's flat post-first (`reconciler.py:173`). Forced by `IPTCNCTH` sitting **self-crossed 2 h 45 min** on 29-08 behind a whole-book guard refusal | **Decide, do not copy.** ⚠ The blocker is `[atomic-book]`: submit ClOrdIDs mint **BY POSITION** in the unmet list, so a partial send re-diffs onto ids the venue already holds. **Go is the cheaper place to change id identity** — it has no live journal to keep replay-equal with. If Go takes non-positional minting first, Python inherits the design rather than the other way round | 🟡 **open — George's call on where it lands first** |

## ✂ Deliberately not taken

| Change | Why Go does not take it |
|---|---|
| The SR probability publisher (`inplay-sportradar-service`, incl. **N74**'s `MMPUB_TICK_S`, PR #51) | Out of scope by decision (18-08): *"The SR publisher stays Python; the Go FIX gateway is untouched."* Not a divergence — a boundary |

## ⚠ Standing risks this register exists to hold

- **The pin moves only when George names a new one.** Until then every
  Python commit here widens the gap, and the differential harness cannot
  report it — it compares at the pin.
- **Two makers on one namespace is a live hazard, proven once**
  (`76341d3`). Any shadow run repeats the conditions.
- **`68b76a8` and `f9eec8b` conflict on one row.** Anyone porting them
  in commit order and stopping early ships the one-rung book George
  already withdrew.
