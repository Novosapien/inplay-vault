---
description: "CB4's session: the ack drain was a scan costing 98.4% of every ack, removing it met AC4's miss gate, and a night of rig arms had measured the wrong tree"
---

# 2026-08-15 — CB4: the ack drain was a scan, not arithmetic

> **Who:** stream-b-cb4 then stream-b-cb4-r2 (AI sessions), team
> mm-python-fix-set. The first session died mid-arm on an API timeout;
> the second recovered the arms and found they were void.
> **Type:** build
> **Refs:** `specs/2026-08-14-mm-python-fix-set/` — spec F1c · R4/AC4 ·
> R9/AC9 · `profile-cb1.md` (the map) · `profile-cb4.md` (this result) ·
> MM branch `fix-set/cb4-drain-speed`

## What we did

CB1 measured that the venue ack drain is **98.1% of tick time at 9.893
ms per ack** and handed CB4 one instruction: run a function-level
profiler over that path, because CB1's own timers are stage-level and its
§9.1 says per-event attribution "wants a real profiler".

1. **Built the harness** (`scripts/cb4_ack_bench.py`). It stands the real
   170-book universe through the real composition, drives the book to a
   chosen depth, then feeds acks through the runtime's own drain body —
   `orchestrator.handle()` then `driver.stage()` — via the real gateway
   decode. A bench, not a baseline: the six-game workload stays what AC4
   is measured against.
2. **Found the cost.** One function, `VenueEngine._stamp_and_prune` — a
   full-dictionary scan on every venue event. (An early claim that it was
   **94.3%** of the ack path is withdrawn; see "What went wrong".)
3. **Replaced the scan with two derived indexes** and proved equivalence
   differentially against a verbatim copy of the old code.
4. **Ran the rig re-measurement** — the six-game workload at 1× and 10× on
   `cb1-profile-clone` (n2-standard-2), CB1's own durations and caps, plus
   a same-day pre-fix control arm.
5. 🛑 **Found that none of it had run the fix**, and threw the whole set
   away. Every arm imported the same engine source whichever tree it was
   launched from. See "What went wrong" — this is the session's most
   important finding and it is not about the market maker.
6. **Fixed the import, put provenance in the artefact**, and wrote
   `scripts/cb4_scan_cost.py` to size the prune reproducibly, because the
   ack bench structurally cannot.
7. **Re-ran the pairs back to back** — pre-fix then post-fix at 1× and
   10×, adjacent, idle box, provenance asserted per arm, with a
   `perf_counter` around `_stamp_and_prune` in both trees.
8. **Ran the R9 drill** on the post-fix arm's own 226 MB journal, and
   **STOPPED the rig** — verified `TERMINATED` at 18:18:23Z. It was
   started again 49 seconds later (the team lead, collecting the arms'
   `profile.json` while this session was quiet past its ETA — they held,
   read, and released). Rather than stop a box someone might be using, CB4
   installed a **load-based `cb4-watchdog.service`** (systemd, enabled,
   survives reboot) that powers it off after 30 minutes below 0.20 load.
   Deliberately load-based, not process-name-based: the first version
   keyed on CB4's own workload names and would have powered the box off
   under another stream's job. Escape hatch: `touch ~/cb4-hold`.
   ⚠ **Lesson: the shared account makes the audit log unattributable.**
   `gcloud compute operations list` gives the sequence of starts and stops
   and puts the same identity on all of them. Say in the channel when you
   start or stop the rig — that sentence is the only attribution we have.

## ⭐⭐ The result — AC4's miss gate is MET

Six-game workload, `cb1-profile-clone` (n2-standard-2, Python 3.12.13),
1×, 2,400 s, adjacent arms on an idle box:

| | pre-fix | post-fix |
|---|---|---|
| ms/ack p50 | 7.346 | **0.298** (24.6×) |
| ms/ack p90 | 9.299 | 0.586 |
| **missed-sweep ratio** | **28.755%** (693/2,410) | **0.000%** (0/4,777) |
| late ticks | 43.43% | **0.00%** |
| tick p50 | 411.85 ms | **32.31 ms** |
| **venue drain's share of tick** | **97.7%** | **47.5%** |
| DRAIN_CAPPED | 6 | 7 |

**AC4 wants < 0.5%. We measure 0.000%.** The 10× pair moves the same way
(3.953 → 0.254 ms/ack); it cannot discriminate on the gate because
pre-fix 10× already missed 0%.

**The probe settles the attribution on the rig, not on a bench:**
`_stamp_and_prune` was **7,225.8 µs per call = 98.4% of the per-ack
cost** pre-fix, and **6.72 µs = 2.3%** post-fix. **1,075×.**

⭐ **The venue drain is no longer the tick.** It was 96–98% of tick time
on every arm ever run against this engine; it is now under half.

**R9 PASSED at rig scale:** two independent folds of the post-fix run's
own journal — 226.0 MB, 224,876 events — agree byte for byte on 40,244,373
bytes of canonical state, and publish nothing.

🔴 **The one clause that does not pass: "zero DRAIN_CAPPED" (7 ticks).**
They are the boot re-stand, not game load — 1,598 standing instructions
against a 512 cap needs ≥4 ticks, `acks_per_tick` max is 512 while p99 is
130, and the count is 5–7 on **every arm ever run** while the miss ratio
moved 52% → 0%. A counter blind to a 24× change in per-ack cost is not
measuring load. **CB4 reads the clause as mis-specified rather than
failed; that is George's call, and CB4 proposes no dictionary row.**

## What we learned

### The cost was a full-universe scan on every single venue event

`_stamp_and_prune` walked every order in every book on every venue event,
re-parsing each terminal order's timestamp against the retention cutoff.

**What the engine actually holds**, reconstructed from the arms' own
journals (the engine's bookkeeping, not the ack payload — a replace ack's
`order_state` describes the NEW order, so reading it directly gets this
badly wrong): at 1× the run creates ~121,000 order records in 2,400 s,
**98.7% reach a terminal state**, and the dictionary settles at **~15,700
held, ~13,000 of them dead** and waiting out the 300 s retention window.
It plateaus, so retention works — but the scan re-parsed all ~13,000 dead
records on **every venue event**.

Timed on its own at that shape (`scripts/cb4_scan_cost.py`, one Mac):

| records held | terminal | pre-fix ms/call | post-fix ms/call |
|---|---|---|---|
| 1,500 | 0 | 0.0585 | 0.0002 |
| 9,400 | 7,802 | 0.9352 | 0.0003 |
| **15,700** | **13,031** | **1.6757** | **0.0003** |
| 31,000 | 25,730 | 3.4550 | 0.0003 |

Linear against flat. ⚠ **The terminal fraction is what makes it bite** —
the same 1,500 records cost 2.4× more at the rig's 83%-dead shape than
when they all rest. That is why a harness holding only resting orders
finds nothing.

⚠ An earlier claim that this function was **94.3% of the ack path** at
18,552 orders held is **withdrawn**: not reproducible from any committed
harness.

⚠ **There is no Decimal problem, and there never was.** The spec framed
CB4 as "Decimal churn, the ack fold, per-ack allocations". The ladder
build, the Decimal arithmetic, the gateway decode and the idempotency
bookkeeping together are under 5% of the path.

### ⭐ It grows with RUN LENGTH, not book depth — correcting CB1 §4.4

CB1 read its curve as "superlinear in resting-order count". It is
**linear in the total number of orders held**, and that total climbs
because terminal orders are RETAINED: `venue_terminal_retention_s` is
**300 s**, so a run sending ~57 instructions/s holds ~17,000 dead orders
and every ack re-parses all of them.

✎ **More precisely, and this matters for projecting:** the dictionary does
NOT grow without bound. It fills for the first ~300 s and then plateaus
(measured steady-window drift: +0.9%). What sets the plateau is the
**instruction rate**, because held ≈ rate × retention window. Run length
only matters until the window fills.

So the real variable is **records held**, and the two ways to move it are
the instruction rate and `venue_terminal_retention_s`. Measured mean held:
14,609 at 1× against 10,305 at 10× — the 1× arm is dearer per ack because
it sustains a higher instruction rate, not because it ran longer.

This explains CB1's three points **better than book depth does**: its 60 s
shakedown (1.455 ms/ack) had barely begun to fill the window; its 900 s
and 2,400 s arms (6.313 and 9.893) had filled it to different plateaus.
Same code, same machine, same workload.

It also explains **CB1-V's "book count drives ack volume, not game
count"**: more books means more converger instructions per second, means
a bigger retained dead set, means a slower ack.

⚠ **A measurement trap that outlives this fix:** any per-ack figure taken
from a run shorter than ~300 s understates the cost, because the
retention window has not filled.

### ⭐ The sibling had already learned this lesson

The acceptor's seen-key pruner (`[seen-retention]`,
`events/acceptor.py`) has used arrival-ordered deques with a head prune
**since the 08-12 incident where venue keys were 99.9% of a million-key
set**. The Venue State Record never got the same treatment and carried a
full scan until today. One lesson, learned once, not applied to the
sibling — worth a sweep of any other per-event pruner before the Go port
copies the shape across.

## What went wrong / got stuck

- **The first bench arm found nothing, and that was the useful result.**
  Sweeping the RESTING order count reproduced no curve at all — ms/ack sat
  flat at 0.13–0.24 from 170 to 1,492 resting orders. What gave it away
  was that the TOTAL dictionary size barely moved across those arms. The
  hypothesis inherited from CB1 was wrong, and testing it directly is what
  found the real variable.
- **A macOS tarball broke the suite on the clone.** AppleDouble `._*`
  sidecar files rode the `tar` across and `test_config.py` walks `src/`
  reading every file as UTF-8. Not a code fault; `find -name '._*'
  -delete` fixed it. Worth knowing for any future ship-to-rig.
- **The rig's progress log looked dead for ten minutes.** The workload
  driver's progress `print` has no `flush=True`, so those lines sit in the
  buffer until an engine print (which does flush) forces them out. Under
  CB1 the engine's constant alarms flushed it continuously; under the
  fixed engine it went quiet, and silence looked like a hang. Confirmed
  healthy by watching the journal grow instead.
- **The session died with the rig arms still running.** The 1× arm was due
  ~03:45Z and the 10× arm ~04:02Z; the session was lost to an API timeout
  at ~03:39Z, before either landed. The sentinel pattern held: the
  follow-up session found `cb4.done` and `before.done` both down and every
  arm complete on disk. Two commits were also unpushed
  (`cb4_replay_check.py` and a naming fix); recovered and pushed.

### 🛑 ⭐ THE BIG ONE — every arm measured the same engine, whichever tree it ran from

**CB4's entire first set of rig numbers was before vs before, and nothing
said so.**

`scripts/six_game_workload.py` put the repo ROOT on `sys.path`. The repo
is a `src/` layout, so `import mm` never resolved there and fell through
to the venv's editable install. Every venv on `cb1-profile-clone` had been
made by `cp -a` from `~/mm`, so every `.pth` still pointed at `~/mm/src`.
`~/mm-cb4/src` held the fix and **was never imported**. Proof, on the box:

```
mm      -> /home/georgewestbrook/mm/src/mm/__init__.py
mm-cb4  -> /home/georgewestbrook/mm/src/mm/__init__.py   ← the fixed tree
```

Nothing errored. The runs completed, printed a summary, and produced
numbers of an entirely believable magnitude. **The failure is silent and
its output is credible, which is the worst combination available.**

⚠ **Every anomaly that had been puzzled over dissolved at once**, and
none of them were real: the "same-day pair shows only 4%" (same code both
sides), the rig bench showing pre-fix ≈ post-fix (both resolved to one
module), and the 9.893 → 6.149 "improvement" (both pre-fix — that was the
box's own drift, the same drift the 10× cross-day pair showed at
6.313 vs 3.764 on identical code).

**What made it findable:** a `perf_counter` probe patched into the tree
under test emitted **zero** lines for ten minutes of a running arm. A
patched module that never prints is a patched module that never loaded.

**Fixed, and made unable to recur quietly:**
- `MM_REPO / "src"` goes on `sys.path` ahead of the root, in the workload,
  the bench and the replay drill — `[measure-this-tree]`.
- `profile.json` now carries `run.engine`: the `mm` package path that was
  loaded and whether the prune index is present. The summary prints both
  **beside the numbers they produced**, so the pair cannot be separated.
- The launcher asserts provenance per arm and aborts on a mismatch.

⚠ **This is a team-wide hazard, not a CB4 one.** Any stream that copied a
venv between trees has the same exposure — the `.pth` survives the copy,
so replacing the source changes the files and not what `import mm`
resolves to.

**Both sibling streams were checked and both are clean:**
- **CB1** ran from `~/mm`, the tree its own `.pth` points at. Safe.
- **CB2** never ran on the rig at all (there is no CB2 tree on that box).
  Its audit showed both arms ran on a Mac from its measurement worktree
  with `PYTHONPATH=src` winning over the `.pth`, proven two ways —
  `mm.__file__` directly, and a positive control stock code cannot
  produce (the ON arm's 24,144 converger passes against 7,642; that
  cadence override exists only in the measurement tree). **Its null
  conclusion stands.**

⭐ **The positive control is the transferable trick.** CB2 could prove its
arms differed because its ON arm produced an artefact the OFF build was
incapable of producing. CB4 had no such control, which is why an
all-pre-fix set looked normal for hours. **Where a change should leave a
visible fingerprint, assert on the fingerprint, not just on the timings.**

- **The bench cannot measure the function it was built for.**
  `cb4_ack_bench.py`'s timed window re-acknowledges orders that already
  rest, so every record is ACTIVE and the old scan's `continue` fires
  before the timestamp parse — the cost the index removes. It also caps
  near 1,550 records against the rig's ~15,700. Its published table
  (18,528 and 35,552 records held, a 28× win) **is not reproducible from
  the committed script** on either machine. `scripts/cb4_scan_cost.py` was
  written to size the function reproducibly instead.
- ⚠ **The rig lives in project `inplay-497712`, not the account default.**
  `gcloud compute` without `--project` reports the instance missing and
  the project empty — indistinguishable from a deleted rig. It had been
  left RUNNING since 14-08 17:47, ~12 h of idle billing, because the
  session that owed the STOP died first.
- ⚠ **Lesson for long rig arms:** the work outlived the session that
  started it, twice. The sentinel pattern is right, but collection has to
  be resumable by someone else — the launch must leave its output paths,
  sentinel names **and project** written down durably, not in a transcript.

## Decisions made *(mirror into [[market-maker/decisions]])*

- **The drain-cap ruling needs re-deriving, and CB4 proposes no
  dictionary row.** CB1's rule stands as a rule — `venue cap ≤ drain
  budget ÷ ms-per-ack` — but its arithmetic was computed at 9.893 ms/ack.
  The re-derivation belongs to the lead and George, not to this chunk.
- 🟡 **PROPOSED OPERATING RULE — a measurement must record what it
  measured.** Any run whose number gates a decision states, in its own
  artefact, which code it loaded and whether the change under test is
  present, and aborts if that does not match what was asked for. CB4 lost
  a night's arms to a silent import fallback that produced credible
  numbers for the wrong tree; no test, lint, type check or review could
  have caught it, because none of them run on the rig. **Provenance
  belongs in the artefact, not in the operator's memory of which
  directory they were in.**
- 🟡 **A before/after pair on `cb1-profile-clone` must be ADJACENT.** The
  same pre-fix code measured 6.313 ms/ack on 14-08 and 3.764 on 15-08 at
  10× — a 1.68× drift with no code change. Cross-day pairs on this rig are
  not admissible evidence; the arms must run back to back on an otherwise
  idle box. ⚠ This also means **the box must be left alone while an arm
  runs** — analysis scripts on the same 2 vCPUs corrupt the measurement.

## Questions opened / closed *(mirror into [[market-maker/open-questions]])*

- **Closed:** what in the ack path costs 9.893 ms. It is one function,
  named, measured and fixed.
- **Closed:** whether per-ack cost is superlinear in the resting book. It
  is not — it is linear in total orders held.
- **Opened then CLOSED by measurement:** `open_orders()` and
  `pending_exposure()` walk a security's whole order dict, terminal
  records included, on every ack — the same defect class, scaled down by
  170. Timed at the rig's per-book shape (~92 records, 83% dead) they cost
  **4.23 µs and 2.10 µs**. That is **under 0.5%** of the per-ack cost, not
  the ~15% first estimated. **Not worth a session.** ⚠ The lesson repeats
  the session's main one: the first estimate was arithmetic on iteration
  counts, and the measurement disagreed by more than 10×.

## Next

1. 🔴 **George's call on AC4's "zero DRAIN_CAPPED" clause.** The miss gate
   is met at 0.000%; the cap clause fails on a once-per-process boot
   transient. Either exempt the boot window, or re-stand the book under
   the cap across several ticks deliberately. **CB4 proposes no dictionary
   row.**
2. 🟡 **Re-take the drain-cap ruling with the new arithmetic.** At 0.298
   ms/ack p50 the rule gives cap ≤ 1,006; the 512 cap is now safe (153 ms
   worst case, was 3.76 s). The 1,050 NCAA figure is 4% short at p50 and
   ~2× short at p90 — a cap must survive p90, so CB4 still proposes no
   change, but the premise has moved.
3. ⭐ **Re-take the Go decision against these numbers.** One core goes from
   ~101 acks/s to ~1,700 (p90) – 3,400 (p50); NCAA Saturday's ~2,500/s now
   sits between them instead of 25× outside. Not a recommendation to stay
   on Python — the removal of the datum that made the answer look settled.
4. **The GATE inherits the measurement conventions** — provenance assert,
   same-day adjacent pairs, the ~4% noise floor, read the miss ratio with
   ms/ack and tick p50 (profile-cb4 §6).
5. **CB3 is now clearly not worth it for AC4** — it targets a sweep stage
   that was 1.8% of the tick when the drain was 98%; with the drain at
   47.5% and the miss ratio at zero, there is nothing for it to buy.
