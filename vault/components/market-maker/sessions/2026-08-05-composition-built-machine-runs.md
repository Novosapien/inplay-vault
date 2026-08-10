# 2026-08-05 — the composition lands: `python -m mm.runtime` and the machine RUNS

> **Who:** George + Claude
> **Type:** build session (the second half of the 04/05-08 stretch — the
> first half is `2026-08-04-runtime-built-liveness-deviation.md`)
> **Refs:** `inplay-market-maker` commits `cf2bc10` · `7ac6787` ·
> `db19e93` · `01b16c7` · `cf386cc` (BUILD-LOG) · **481 → 500 tests**

## What we did

1. **Tiered polling built, with George's slow tiers.** LIVE ~2 s ·
   PRE_KICKOFF 15 s (interim midpoint of his 10–30 range) · OVERNIGHT
   30 min · POST_GAME 10 min through the 1 h window, then never again.
   The tier decision lives in the POLLER from poller-local facts — the
   orchestrator's activity axis needs readings to know a game is live,
   which is circular for scheduling. The post-game watch re-offers the
   final: identical → quiet duplicate; a CHANGED score → **CONFLICT
   alarm** (§3.1.3 wants a human, not an overwrite). The overnight tier
   doubles as the **N24 experiment**.
2. **`mm/universe.py` — the 170 Team Companies from tZERO's own ticker
   list** (George supplied it; the first seven rows carried a live book
   snapshot). **The ticker IS the security id.** Validates §2.5's counts
   at import (32 NFL + 138 NCAA, unique, gospel floats 900k/1M now in
   Ch 12) and refuses a hole. Four FCS programs sit inside the 138 —
   the venue's list is the list.
3. **The runtime drains the venue's answers** — the tick consumes
   `order.mm1.>` to empty every pass, so a fill moves the book in the
   tick that delivered it. Discovery finally has a production caller
   (first tick, then daily; re-stamps moved kickoffs).
4. **The composition** — `compose.py` (every construction decision, one
   testable file) + `__main__.py`. Boot order promoted from the wire
   test: connect → beat → build → replay → stand the book → tick.
   Loopback runs the full 170 with synthetic T; **live mode REFUSES to
   start and names its gates** (S1/S7 · sr-id bindings · N19).
5. **The drill, against the revived rig: both halves PASS.** Cold boot —
   14 instructions stand the 2-security book, answers drained within two
   ticks, the sweep cycling every 2 s, clean SIGINT. Restart — 56-event
   journal replayed, book re-stood, loop resumed.

## What we learned

- ⚠ **Two real defects found by building:** `ingest_reference_numbers`
  never folded its record into the last-RP map — **Edwin's daily step
  reached the book one event late**, a [no-smoothing] violation (fixed;
  the test now proves the ladder straddles the new price). And a
  re-stamped kickoff did not reschedule an already-set next-due (fixed).
- ⚠ **The restart drill DEMONSTRATED the boot-reconcile gap live:** run 2
  re-stood with 11 instructions, not 14 — three levels the dead-man swept
  during our absence still sat in the replayed record, because those
  sweep events published into the gap. Passive convergence heals what
  trades; the systematic fixes are the §3.1.4 heartbeat-sweep healer
  (unbuilt) and a venue snapshot at boot (ICD — George: "we think about
  that more"). Parked with eyes open; the dead-man bounds the harm.
- **The gateway's 50 msg/s governor shapes rig drills:** a full
  1,020-order post would be mostly rejected. `MM_LIMIT_SECURITIES` caps
  the drill; the governor must rise for the 200 ms capability (Hasan).

## Decisions *(mirrored into decisions.md via the parameters/plan rows)*

Slow tiers are George's numbers ("to be safe") · the ticker is the
security id · live mode refuses rather than degrades · the trial key
covers the build (George, end of session): the live HTTP source and the
sr-id bindings capture can proceed WITHOUT waiting for S7 — one careful
capture pass, not a polling loop, because the trial quota was half-used
in July.

## Questions

- No new E/T/S/N items. George takes **T1 to Hasan** directly (with N30
  and the governor in the same conversation).

## Next

1. **The live HTTP source** (timeline + schedule behind the GameSource
   seam) + **the bindings capture** — buildable NOW on the trial key.
2. §10.3 checkpoints — its own session.
3. Send the Edwin round E29–E38 + N23/N28.
4. The 06:00 file hand-off — still George's call.
