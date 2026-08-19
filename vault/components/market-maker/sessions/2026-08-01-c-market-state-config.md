# 2026-08-01c — step 5 · Chapter 6 · Chapter 12: the ungated tier lands

> **Who:** Claude, autonomous integration mode (third stretch of 01-08)
> **Type:** build session
> **Refs:** `inplay-market-maker` commits `7c43131` · `2f21d81` · `2d3afd8`
> (+ docs) · story page "Permission to quote" 🚦 · E37 opened

## What we did

The whole remaining ungated tier, in the handover's order. **392 → 434
tests**, ruff and `mypy --strict` clean throughout.

1. **Fix-pass step 5 — rejection audit records** (`7c43131`). The §3.2.1
   sum check moved to the acceptor's door as §7.2's Business Validated
   stage (`events/business_validation.py`); `KIND_REJECTED` finally gets
   written, with the reason; no sequence for rejected events; the
   valuation engine's silent-drop branch now raises. The fix pass from the
   27-07 review is complete.
2. **Chapter 6 — Market State** (`2f21d81`). `mm/market_state/engine.py`:
   the §6.3 mapping in §6.2's precedence, the §6.4.1 promotion ceiling as
   a separate function (synchronizing demotes nothing, blocks only the
   climb to Stable), the §6.4 tracker mirroring `StatusTracker`. Wired
   into every cycle; check 2 real; MANUAL_CONTROL events drive the kill
   switch; the sync axis reads off the Venue State Record; the connection
   axis is the runtime's (`set_venue_connection`, CONNECTED by
   construction until the NATS adapter). Edwin's four-row dwell table
   replaced the LIVE-only interim, keyed on a derived activity axis.
3. **Chapter 12 — the Configuration Dictionary** (`2d3afd8`). One
   registry, per-field statuses, §12.3 None-slots, cross-parameter
   validation at construction reporting all problems at once. Fifteen
   modules swept; the CONFIGURED convention retired and enforced retired
   by `test_config.py`; repo CLAUDE.md updated.

## What we learned

- **The §6.4.1 dwell list omits Suspended → Defensive** — the same shape
  as §3.4.1's Invalid → Degraded first-rung grant. Reading it literally
  (first rung free, upper rungs earned) makes boot behaviour sensible: a
  healthy security quotes Defensive on its first trigger.
- **The flip-gated suspension sweep had a real hole**: an order submitted
  just before a suspension is not yet cancellable, and by the time its ack
  landed the flip was consumed — it would have rested through the
  suspension. Sweeping every suspended cycle is quiet by state
  (PENDING_CANCEL is not re-cancelled) and closes it.
- **"Continuously for the dwell" needs care at promotion time**: the next
  rung's clock may only start when conditions already permit that rung —
  otherwise time served under worse conditions counts toward a better
  state. Caught while writing the tracker tests.
- **The spec disagrees with itself on Recovery Ready** (§6.3 Ready →
  Defensive vs §6.4.1 "Normal or Ready") → **E37**, low urgency, cannot
  bite until §10 exists.

## What went wrong

- First tracker draft started every security Suspended with a full dwell
  to Defensive — broke half the integration tests and, on reflection, the
  spec's own §3.4.1 parallel. Re-read §6.4.1, corrected to the free first
  rung before commit.
- A test released the kill switch 30 s after the last reading and expected
  requoting — the live feed was legitimately Invalid by then. The machine
  was right; the test moved its clock.

## Decisions *(mirrored into decisions.md 01-08c)*

Sum check at the door, rejections audited, re-rejection per delivery ·
Suspended→Defensive dwell-free · kill switch as a journalled event ·
suspended sweep per cycle, quiet by state · dwell table on the activity
axis with 1 h N4-interim windows · Ch 12 registry with the superseded rows
deliberately absent · Active/Defensive parameter widening waits on E31.

## Questions

- **Opened: E37** — §6.3 vs §6.4.1 on Recovery Ready (spec defect).
- **N4** gained built interims (the two 1 h windows), tagged in the
  Configuration Dictionary.

## Next

1. **The NATS adapter + loopback wire test** (deferred by George 01-08) —
   before any live attempt; needs no T1 (gateway LOOPBACK_MODE).
2. **§10.3 checkpoints** (boot re-reads the whole journal) and **poller
   game discovery** (schedule → game list).
3. Send the Edwin round: **E29–E37** + the E18 refinement (still unsent).
4. Re-probe **UEPR** on the next T0 call (with T1/T2).
