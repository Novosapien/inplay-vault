---
description: "Merge session — PR #23's eleven conflicts against main resolved: digest renumbering (E40–E46/T16–T18/N32–N33/S11), log unions, tZERO sweep adopted"
---

# 2026-08-10-b — the main merge: eleven conflicts, one numbering collision

> **Type:** housekeeping / merge session. Claude, from the 08-10 handover.
> **Docs touched:** decisions.md, open-questions.md, learnings.md,
> market-maker.md, plan.md, systems/synthetic-noise-taker.md (banner), plus
> five non-MM files and the 24-07 meeting note.
> **Repo state at close:** merge commit `d69becf` pushed; PR #23 MERGEABLE.

## What we did

1. Merged `origin/main` into `docs/t0-plain-english-guide` (no rebase — the
   branch was pushed and PR'd). Eleven files conflicted, as the handover
   predicted.
2. Applied the handover's per-file rules:
   - **decisions.md / learnings.md** — unioned in date order. Main's
     27-07 → 07-08 touchdown block and the 30-07 SNT-1 digest entry
     slotted in at their date positions. Nothing dropped.
   - **open-questions.md** — the branch numbering stays canon. The meeting
     digest (merged to main while the branch ran) had minted E17–E23,
     T12–T14, N15–N16 and S6 in collision with numbers the branch already
     used. The digest items are recorded as **E40–E46, T16–T18, N32–N33,
     S11**, with a numbering note at the top of the file. Main's newer
     resolutions (S1/S2/S3 resolved 03-08, E4 closed 31-07, N6 dissolved)
     folded into the resolved sections. The 10-08 priority reset sits above
     the 30-07b ordering, remapped; its E11/E12/E14 tail is flagged against
     the recorded spec-resolutions rather than silently adopted or dropped.
   - **market-maker.md / plan.md** — branch build-truth kept. Digest facts
     (13 Aug dry run, IPO market structure, Phase-0 clears) folded in.
     A merge note marks where the digest's "no orders sent yet" frame is
     overtaken by the 08-07 live run.
   - **Non-MM files** — main's digest side taken. Branch extras main
     lacked were re-added: the Withdrawal-Flow payouts note, the
     release-governance row, trading's 24-07 launch-target block, and the
     24-07 meeting note's MM extraction table + full transcript.
3. Adopted main's tZERO terminology in every kept hunk (quoted speech left
   as spoken).
4. Marked `systems/synthetic-noise-taker.md` (main's digest file) as a
   30-07 snapshot pointing at the live [[market-maker/systems/snt-1-noise-taker]]
   doc — both files exist post-merge; only one is truth.

## What we learned

- **Two doc pipelines minted numbers from the same counters.** The meeting
  digest on main and the MM working session on the branch both extended the
  E/T/N/S sequences, unaware of each other. The renumbering note in
  open-questions.md is the repair; the standing fix is that digests should
  check the branch (or the file's own max) before minting item numbers.
- Main's digest also re-raised items the branch had recorded as
  spec-resolved (E11/E12/E14). Flagged in place, not silently resolved
  either way — the next Edwin round should settle them.

## Questions opened/closed

- None opened for owners. The E11/E12/E14 flag above is a doc tension, not
  a new ask.

## Next

1. Merge PR #23 (branch is MERGEABLE/CLEAN).
2. Then the handover's carried queue: engine hardening (unknown-order
   cancel-reject must drain, not kill), the JETS 18.65 blocker, the no-mock
   OTA channel, supervised9 + CFG-0008 for the next run.
