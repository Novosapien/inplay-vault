# Build — Market State

> Part of [[market-maker/build/index|As Built]] · Code:
> `mm/market_state/engine.py` · Spec: Ch 6.

Permission to quote, per security: Stable · Active · Defensive ·
Suspended.

## The mechanism

- **§6.3's condition mapping walks in §6.2's precedence order** — the
  most severe applicable condition wins. Inputs: the venue connection
  axis (runtime-supplied via `set_venue_connection`), the sync axis
  (from the Venue State Record), freshness/status conditions, and manual
  controls.
- **The ratchet (§6.4):** demotions are INSTANT; promotions earn one
  rung per served **10 s dwell**. **Suspended → Defensive is dwell-free**
  (ours, recorded: §6.4.1 names dwell conditions for the two upper
  climbs only — a healthy security quotes on its first trigger, not 10 s
  late). Dwell toward one rung never counts toward the next. The
  **promotion ceiling** is separate from the demotion floor: ordinary
  synchronizing demotes nothing but blocks the last climb to Stable.
- **The kill switch is a journalled event** — `MANUAL_CONTROL`, keyed on
  Control Action ID: the global kill switch and per-security suspension
  dedup, replay identically, and drive the same path the wire test
  proved. (§6.3's "release requested but unapproved" middle state is an
  ops-UI workflow that does not exist yet.)
- **The suspended sweep runs EVERY suspended cycle, quiet by state.**
  The flip-gated version had a hole: an order submitted just before a
  suspension is not yet cancellable, and when its ack lands the flip is
  spent — it would rest through the suspension. Per-cycle sweeping
  cancels it on the ack's own cycle; already-cancelled orders are
  PENDING_CANCEL and never re-sent.

## Two axes, both called "state" — do not confuse them

Market state (this page) is §6.1's per-security permission ladder. The
**activity axis** (LIVE / PRE_KICKOFF / POST_GAME / OVERNIGHT) is a
separate derivation from the fixture rhythm that drives Edwin's
four-state dwell table and the poll tiers. The window boundaries (1 h
before kickoff, 1 h after the final) are interims under **N4**.

## Known edges

- **Active and Defensive quote identically today** — their parameter
  widening is E31's per-state width floor; the slot exists in `width.py`
  and wires in one call-site when Edwin's values land.
- **E37 — the spec disagrees with itself on Recovery Ready:** §6.3 maps
  Ready → Defensive; §6.4.1 permits the Defensive → Active climb with
  "Normal or Ready". Both implemented literally; the stricter wins.
  Cannot bite until §10 recovery exists.
- Promotions advance only on triggers; with the §3.1.4 sweep now built,
  quiet books climb on the sweep's cadence rather than waiting for a
  reading.

## What changes here next

[[market-maker/build/next|Next]]: E31's per-state values · §10 recovery
states (unbuilt) · the ops-UI kill-switch surface (with access control
first — the panel carries destructive endpoints).
