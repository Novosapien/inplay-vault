---
description: "The taker cutover: the two operating setups reconciled to one owner (snt-1.service, SNT-CFG-0007), floats recomputed at the halt, the nohup retired"
---

# 2026-08-11 (late) — the taker cutover: one owner, floats recomputed

> **Type:** live ops. Claude, from the 08-11 close handover.
> **Continues:** [[market-maker/sessions/2026-08-11-cadence-deploys-joint-run|the day's index]]
> §"Cross-session reconciliation owed" and
> [[market-maker/market-taker-requirements]] addendum 2026-08-11d.
> **VM state at close:** maker `supervised12` (CFG-0011) untouched ·
> taker `snt-1.service` ACTIVE, SNT-CFG-0007, journal `/var/lib/mm/snt4/`.

## What we did

1. **Read first** (per the working guide + the handover's instruction):
   the guide, the two 08-10c/08-11 session notes, the taker
   requirements addendum, the hub, `build/venue.md`,
   `trading-architecture.md` (tZERO + gateway facts), the newest
   decisions entries, and the MM repo CLAUDE.md operating rules.
2. **Surveyed the VM read-only.** Confirmed: the nohup taker running
   (PID 29081, boot 20:51:29Z, `~/snt-0811.env`, SNT-CFG-0006,
   PRE_KICKOFF pin) and `snt-1.service` enabled-but-dead since 13:48
   (SNT-CFG-0003, journal `snt3`, only EAGL float pinned). Both setups
   run the SAME code — `~/snt-checkout` @ `5681767` (PR #14) — so the
   delta was env only.
3. **Halt-before-stop.** Published `{"cmd":"halt"}` on
   `snt.control.snt-1` (python via the venv — no `nats` CLI needed),
   verified the journalled halt and `0 cancels out`, then killed the
   process by the ps-fields match (rule 4).
4. **Recomputed the floats at the halt.** The env floats were
   venue-verified at 20:51 but the taker kept trading under its
   PRE_KICKOFF pin — 342 sends by the halt. New float per book =
   env float + whole-journal drift (the T-S05 algebra; the whole-journal
   sum is correct because the recovery floats were chosen against the
   engine's replayed drift). Cross-checked against the journal's line-75
   reconcile record (PATR: 4868 venue at drift +32 → env 4836 ✓).
   Result: **COWB 4162 · STEE 5943 · EAGL 5565 · GIAN 4485 ·
   PATR 5039.**
5. **Cut over to the unit.** `/etc/snt-1/env` (dated `.bak` first):
   SNT-CFG-0003 → **SNT-CFG-0007** (above both prior id spaces),
   journal `snt3` → fresh `/var/lib/mm/snt4/`, the five reconciled
   floats. `SNT_MINUTES=0` and `SNT_STATE=AUTO` were already in the
   unit env. Renamed `~/snt-0811.env` → `.retired-20260811`. Started
   the unit: boot clean — replayed 0 (fresh journal → boots ARMED, no
   resume needed), 5 books at the new floats, state AUTO (derived),
   maker ticking undisturbed.

## What we learned

- **Floats are positions, not constants.** A float override is only
  true at the instant it was computed; any trading after that makes a
  copied-forward float stale. Every journal cutover must recompute
  float = env float + journalled drift, at a halt.
- The two shell layers of `gcloud compute ssh --command` mangle
  f-string braces — keep remote python plain.
- The nohup taker and the unit shared `~/snt-checkout` code; the
  reconciliation was pure env. Nothing needed a deploy.

## What went wrong / got stuck

- Nothing blocking. One rerun for the quoting mangle above.

## Decisions made

- None new — this executed the recorded 08-11d reconciliation order.
  CFG numbering continues from the highest of the two setups (0007).

## Questions opened/closed

- Closed: the 08-11d ⚠ two-setups hazard (requirements addendum
  2026-08-11e is the record).
- Watch (not a question): the first fill under SNT-CFG-0007 is the
  live T-S05 proof of the new floats. Fail direction is a safe halt;
  if it halts, patch `SNT_FLOAT_OVERRIDES` off the RECONCILE line and
  resume.

## Next

George's ruled order stands (the day-index note §Next): **1. the
full-book position-transfer seeding + the full-book MM run (B3 + the
LmtPerc empty-book experiment + N31 fsync)** · 2. the synthetic game
day · 3. C2 on supervised12's journal · 4. the externals round
(T17 · Rob: STX reseeder, JETS reference, T14/T15/T16 · Hasan: B2 ·
Edwin: E31/E17 + flags + the E41 data). Engine restarts: next is
`supervised13` + CFG bump + fresh journal dir.
