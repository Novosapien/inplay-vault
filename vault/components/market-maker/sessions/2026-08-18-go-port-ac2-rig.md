---
description: "The AC2 rig session: replay equality proved on the real 548.5 MB corpus across two architectures, and a third instance of CB4's scan shape that only rig scale could see"
---

# 2026-08-18 — the Go port, AC2 on the rig

> **Who:** Claude (`/general-implementation-builder`) + George
> **Type:** measurement + build
> **Refs:** `specs/2026-08-18-mm-go-port/` · `Novosapien/inplay-market-maker-go`
> PR #8 · `docs/ac2-gate.md` · [[market-maker/build/venue]] ·
> [[market-maker/sessions/2026-08-18-go-port-venue-record]]

## What we did

Took the rig session N46 asked for and **closed AC2** — Phase 0's last open
acceptance criterion, and the only one the build could not meet from a laptop.

George's ruling: do it now, and fold on the rig as well as pulling the corpus
down.

1. **Found the rig.** `cb1-profile-clone` (project `inplay-497712`, zone
   `us-east4-a`, n2-standard-2) was **stopped, not deleted**, and its 50 GB disk
   still held the 16-08 GATE journal. N46 was never a capability gap — `gcloud`
   was already authenticated. It was flagged because starting a VM in the live
   project is billable and outward-facing, and because the handover's rule is
   that one session drives the VM.
2. **Folded the real corpus with Python at the pin, on two machines at once** —
   the rig and the dev Mac — and compared.
3. **Folded it with Go on both**, with the determinism stress on top.
4. **Chased a 44× gap** between the Go fold's rig-scale time and Phase 0's
   synthetic-journal figure, and found a real defect.
5. Stopped the VM and re-armed its idle watchdog.

## What it proved

**The corpus.** `~/gate-v2/v2-1x/journal/journal.jsonl`, written 2026-08-15 by
the `six-game-v2` workload (seed `20260814`): **548,523,635 B · 555,710 lines ·
551,939 accepted events**, sha256 `b187ae6d…55ed3959`.

**Python's reference agrees across two ARCHITECTURES.**

| arm | platform | fold | canonical bytes | publishes |
|---|---|---:|---:|---:|
| rig | linux-x86_64, n2-standard-2 | **1,505.6 s** | 102,953,252 | 0 |
| mac | darwin-arm64, M5 Pro | **603.8 s** | 102,953,252 | 0 |

Same sha256 `c9220465…3df6a6b`. R2a's "two independent folds must agree" rule,
satisfied across two machines rather than twice on one box — which proves the
fold is a function of the events **and** that the answer does not depend on the
hardware.

**Go matches it on both**, at one state hash
`8ca3ed3c…c055037c`, at GOMAXPROCS 1/2/8 on the Mac and 1/2 on the rig. That is
AC11's determinism stress at rig scale and across architectures, which is more
than AC11 asked for.

⚠ **1,505 s against ~107 s is NOT a speedup.** Python folds all **eighteen**
subtrees; Go folds **two**. The honest comparison arrives at gate 0-b, at the end
of Phase 3.

## What we learned

### ⭐ The rig is 2.5× slower than the dev Mac — measured twice

| | rig | mac | ratio |
|---|---:|---:|---:|
| Python, whole engine | 1,505.6 s | 603.8 s | **2.49×** |
| Go, acceptor + venue | ~107 s | ~43 s | **2.5×** |

Two workloads, two languages, one factor. **Every Mac measurement in the port
can now be read against `n2-standard-2` as a defensible estimate** — the decimal
benchmarks, A2's 792 ms deep copy, the venue record's 83.7 ms snapshot. ⚠ It
makes the estimate defensible; it does not retire the standing rule that a
capacity claim gets re-taken on the rig.

⚠ It also does not contradict the "this rig drifts ~1.7× day to day, ~31% within
a day" finding — that is about comparing rig arms to each other, and is why only
adjacent arms pair. This is a cross-machine ratio taken on one day.

### ⭐⭐ A THIRD instance of CB4's shape, and only rig scale could see it

The first rig-scale Go fold took **186 s per fold**, against the **4.25 s** Phase
0 measured on a synthesised journal of the same size. That gap was chased rather
than explained away.

**First, the obvious hypothesis was killed.** The harness holds all 551,939
envelopes in memory (3.7 GB peak), which looked like the cause. Measured:
streaming recovery **4.37 s** against materialising `Replay(0)` **4.64 s** —
holding every envelope costs **0.27 s**. Not it.

**Then the venue leg was profiled.** 161.81 s over 551,939 events:

```
   OpenOrders          116.41 s  50.60%   ← slices.partitionOrdered 20.9% alone
   PendingExposure      19.85 s   8.63%
```

**`record()` took its open-order COUNT from `len(open_orders(...))`, and
`open_orders` SORTS every ClOrdID in the book — on every venue event, to produce
a number that cannot depend on the order.**

That is **CB4's shape for the third time**: a per-event walk of every order held,
linear in the 300 s retention backlog, in a function whose result does not need
it. The port's spec already carries a "Do not transliterate" table naming
`_stamp_and_prune` and `RejectBackoff.suppression()` for exactly this class —
and nobody had swept the class for a third member.

⚠ **No workload short of rig scale makes it visible.** The two committed corpora
hold 8,090 and 2,931 orders; the GATE corpus holds **45,381**.

The fix is a count without the sort — identical by construction, since a count
cannot depend on iteration order. `open_orders` still sorts for its real
callers, the reconciler's diff and the boot healer. **161.81 s → 36.32 s,
4.45×**, with the same 546,584 records, 45,381 orders held and 228,659 prunes,
and byte-identity preserved everywhere.

### ⚠ What we deliberately did NOT fix

After the fix, **91% of the venue fold is still two full-book walks per event** —
`pending_exposure` 49.45% and the open-order count 41.82% — and **Python does
both of them too**. Per-security running counters would fix it.

They were not built, and the distinction is worth keeping:

- `len(sorted(x))` → `count(x)` introduces **no new state**. It is the fixed
  shape of a transliterated defect.
- Running sums are **new derived state with a maintenance obligation on every
  mutation path** — a design change, and the classic place for drift to hide.

Filed for the Phase-3 performance run with the numbers already in hand.

## What went wrong / got stuck

- 🔴 **`gcloud compute scp` silently truncated the 548 MB journal to 93,480,960
  bytes and exited 0.** Only the SHA-256 caught it. The working route is to gzip
  on the rig first (46 MB — it is JSON, 11.8×) and verify **both** the
  compressed and the decompressed hashes. ⚠ **"Silence is ambiguous" now has a
  fourth recorded disguise** in this project, after the block-buffered log, the
  notification that never fired, and the GC-thrashing process at 98% CPU.
- **The rig powered itself off mid-session** — `~/watchdog.sh`, 30 consecutive
  idle minutes, installed by the CB4 session because the box once idled ~12 h
  when the session that owed the stop died. It fired between the Python fold
  finishing and the Go run starting. Nothing was lost; the reference was already
  on disk. Escape hatch `touch ~/cb4-hold`, **removed again before leaving** so
  the mechanism is armed for whoever is next. ⭐ The watchdog did exactly its
  job — this is a note about how to work with it, not a complaint.
- **A 344-byte difference from the 16-08 run's reported canonical size**
  (102,952,908 against our 102,953,252) looked alarming for a moment. It is
  correct: `config_version` salts every §5.7.3 draw, that run used `CB4-REPLAY`
  and ours `AC2-GATE`, and the difference lands entirely in `quotes`. `acceptor`
  and `venue` are pure functions of the journal and are untouched by the salt.

## Decisions made *(mirror into [[market-maker/decisions]])*

1. **AC2 is closed as written**, on the real corpus, certified **once** — the
   548 MB journal is not committed, so hashes and provenance stand in for
   reproducibility. Every other target in the Go repo regenerates at the pin;
   this one cannot.
2. **The rig-to-Mac factor is 2.5×**, and it is the lens for every Mac number in
   the port.
3. **`record()`'s open-order count is ported WITHOUT the sort**, added to the
   spec's "Do not transliterate" table as its third named instance.
4. **The two remaining full-book walks stay**, because fixing them means new
   derived state and that needs its own chunk and its own review.

## Questions opened / closed *(mirror into [[market-maker/open-questions]])*

- ✅ **CLOSED — N46.** AC2 needed a rig session; the session was taken and AC2
  passes. Moved to the resolved table.
- Nothing new opened.

## Next

- **Phase 1, chunk `reconciler`.** Read [[market-maker/build/venue]] first.
- ⚠ When the reconciler lands, extend the differential fuzz across it — the
  phase gate is a fuzz over the venue leg, and today it covers the record only.
- ⚠ **Sweep the "Do not transliterate" class rather than its members.** Three
  instances of one scan shape have now been found, the third only at rig scale.
  Before Phase 2's engines are ported, ask of each: what does it walk, and how
  often?
