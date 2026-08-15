---
description: "Fix-set chunk CA1: the ANCHOR_SEED build — a lenient prior-run reader and a journalled boot event carrying kickoff anchors, plus the review-f2 hardening"
---

# 2026-08-14 — CA1: kickoff anchors survive a fresh journal (ANCHOR_SEED)

> **Who:** Claude (stream-a-ca1, implementation teammate) + team-lead
> **Type:** build — chunk CA1 of `specs/2026-08-14-mm-python-fix-set` (F2)
> **Refs:** MM PR **#32** (base `phase0/fix-set-dictionary-batch`) ·
> spec R5 / AC5 / AC9 · review-001 H1 ·
> [[market-maker/sessions/2026-08-10-run-restart-crash-forensics|the p_ref forensics]] ·
> [[market-maker/build-deploy-log]] (the BENG/LION triage row)

## What we did

Built F2: kickoff anchors and finals now cross a fresh-journal restart as a
journalled `ANCHOR_SEED` event.

- **The lenient reader** — `src/mm/events/anchor_seed.py`, new. It takes the
  prior run's directory (`/var/lib/mm/<run>/`, holding `journal.jsonl` and
  `checkpoints/`), picks the newest checkpoint, verifies the **integrity hash
  only**, pulls `{game_id, kickoff_time, p_ref, x, p_tie, status, result}` out
  of the valuation state field by field, and then folds the prior journal's
  **TAIL** on top. Every degradation is named and printed; nothing raises.
- **The event** — `ANCHOR_SEED`, the twelfth type, ours. The composition
  mints exactly one and journals it FIRST into the new journal. From that
  point the anchors are an ordinary fact: replay reads them out of the
  journal and never touches the prior run again.
- **The application** — the valuation engine applies an anchor per game
  **only where no belief exists**, universe-filtered. `[late-arrival]` is
  unchanged as the explicit fallback for the two cases the seed cannot
  cover: no prior directory, and a game the prior run never saw.
- **The wiring** — `MM_PRIOR_RUN_DIR` reaches the existing `prior_run_dir`
  dictionary slot through `compose.Settings`, per the env-vs-dictionary
  split. Three gates decide whether a seed is minted: a prior directory must
  be named, this journal must be empty, and the prior directory must not BE
  this one. Every outcome prints one loud line.
- **25 tests** — the five R5 edges plus the main path, all on the incident's
  own fixture (IPTCBENG, p_ref 0.711, live 0.848). Suite **910**, ruff and
  mypy-strict clean.

## What we learned

- **`load_latest` would have failed silently, for ever.** Review H1 was
  right and the size of it is worth recording: the strict loader rejects on
  BOTH `config_version` and `schema_version`, and R-D06 bumps the config
  version on every single deploy. A seed built on that loader would have
  returned empty every time, on every deploy, with no error anywhere — the
  anchors would simply never have arrived and the book would have looked
  exactly as broken as it does today. A test now pins it: `load_latest`
  returns `None` on the same file the lenient reader reads in full.
- **The tail is not optional.** Checkpoints are hourly, so a kickoff
  routinely lands after the last one. A checkpoint-only seed would have
  carried a pregame belief and no anchor for exactly the games that matter.
- **The tail fold reuses the real engine.** Rather than re-deriving the
  freeze rules (pregame-tracks-x, the kickoff comparison, §3.2.1's
  normalized repair, the settled guard — each of which was a bug once), the
  reader folds the tail through a throwaway `ValuationEngine` built with THIS
  run's securities and team map. One copy of the rules, and the universe
  filter comes free.
- **The seed must carry `x`, not only `p_ref`.** The spec's field list names
  five; a belief cannot exist without `x`, and seeding `x = p_ref` would
  make the adjustment zero — which reproduces the exact bug being fixed
  until the next reading lands. Reported to the lead as a deliberate
  addition rather than a divergence.

## What went wrong / got stuck

- **The seed published a price, and that was nearly a live outage.** The
  first working version had `ANCHOR_SEED` publish a Reference Price like any
  other input. At boot its cycle ran, the quote engine recorded the ladder it
  produced as PUBLISHED — and replay discarded the instructions, as replay
  always does. `stand_the_book` then found nothing to change, so **the venue
  would have received an empty book** until a dwell expired. Caught by a test
  that asserted the standing ladder's mid rather than the Reference Price;
  the RP-level tests were all green while the book was empty.
  The fix: the seed writes state and publishes nothing (`[seed-silent]`).
  §3.1.5 publishes on real change, and at boot there is nothing to change
  from. The lesson generalises: **at boot, a test that checks the price is
  not checking the book.**
- **Two correct gates can hide each other.** The edge-(c) test (prior
  directory = this run's) first passed through the empty-journal gate
  instead, because the run being pointed at itself already had events. The
  test now uses an empty directory pointed at itself — the case that
  actually needs the gate: a wiped journal in a reused directory.

## Decisions made *(mirror into [[market-maker/decisions]])*

- **The seed is journalled at build and applied by `boot()`'s replay** —
  the composition hands it to the acceptor, not to the orchestrator. So the
  live path and the replay path are one path, and there is no second
  application whose equality has to be argued. The cost is a real ordering
  requirement: `build()` without `boot()` leaves a journalled seed that no
  engine has applied.
- **`ANCHOR_SEED` publishes no Reference Price** (above).
- **The seed is the weakest fact in the machine.** Anything the journal
  already knows outranks it, which is what makes "a fresher reading's
  kickoff_time beats the seed's" need no special case at all — the ordinary
  reading path replaces the belief and keeps the frozen `p_ref`.

## Questions opened / closed *(mirror into [[market-maker/open-questions]])*

- **N23/N28 (open, ours):** `ANCHOR_SEED` is the twelfth event type outside
  the spec's §7.3 table of nine. It joins `VALUATION_SWEEP` and
  `SESSION_BOUNDARY` in the blessing round, flagged in the code.
- **N22 (open, George):** the freeze-at-kickoff ruling is now HONOURED
  across cutovers rather than violated by every one. The operating half of
  the answer (R11, no maker cutovers while games are live) already landed in
  Phase 0; this is the carry-fix half George asked for alongside it.

## Next

- ~~Owed before this deploys: `MM_PRIOR_RUN_DIR` in the entrypoint's env table
  and the redeploy runbook~~ ✅ closed by the lead (commit 6ec78fa on the same
  branch).
- The lead's GATE chunk owns the full AC5 rig drill: a real SIGTERM mid-game
  and the published-mid-within-$0.02 measurement. CA1 proves the mechanics,
  not the rig.

---

## Addendum (same day) — the review pass: present is not parseable

A real review pass (**review-f2**, task #15) reproduced **four** ways a
hash-VALID prior run could stop the maker BOOTING. Every one of them is a
defect in the fix itself: the anchors exist to make a boot safer. All four
were reproduced first, then fixed, then re-reproduced green. Commit
**4a7c484**, PR #32 updated in place; **932 tests** (910 + 22), ruff and
mypy clean.

### What was wrong

1. **Presence is not parseability (HIGH).** The reader checked that
   `kickoff_time`, `x` and `status` were PRESENT, never that they PARSED.
   A hash-valid checkpoint carrying `status: "in_play"`, `result: "draw"`,
   `x: 1.5`, `x: "not-a-number"`, a nested `x`, or a status/result pair
   that disagree, passed that check, reached the strict apply path, and
   raised out through `compose.build()` — **the engine does not start**.
2. **`decimal.InvalidOperation` is not a `ValueError` (HIGH).** It inherits
   from `ArithmeticError`. The tail fold's except tuple was
   `(ValueError, KeyError, TypeError)`, so `p_home: "1.5"` (out of range)
   was skipped correctly while `p_home: "not-a-number"` or `null`
   (conversion failure) killed the boot. An asymmetry no reader of the code
   would guess, and the reason both fold guards now name `ArithmeticError`
   out loud.
3. **A typo burned the seed permanently (MED).** A seed can be minted ONCE
   per journal, because minting is what makes the journal non-empty. A
   typo'd `MM_PRIOR_RUN_DIR` minted an EMPTY seed from a directory that was
   not there — so the operator fixed the typo, restarted, and the
   empty-journal gate refused to re-mint, for ever, silently. The summary
   line said `JOURNALLED`, so it read as success.

### What changed

- `belief_from_anchor()` in `valuation/engine.py` is now the ONE place an
  anchor becomes typed. The reader validates a candidate by constructing
  the real `GameBelief` — same constructors, same range and enum rules,
  same status/result consistency check — so a bad game is noted and
  skipped while the rest of the checkpoint still seeds, and no second copy
  of those rules exists to drift.
- A missing prior directory is now a **FAILURE** that journals nothing and
  stays re-mintable. A directory that exists and yields no anchors still
  mints an honest empty seed — "there is no prior run" and "the prior run
  saw no games" are different facts. The boot line has a third verb
  (`FAILED`) so a misconfiguration can never read like the deliberate skip.
- `compose._seed_anchors` refuses to mint on any unexpected fault.

### What we learned

- **The rule the reviewer's LOW finding protects is the important one.**
  Validation must stay on the READ side, before the mint, because a
  journalled seed is replayed at EVERY future boot of that journal. Journal
  one entry that raises on apply and the engine can never start from that
  journal again — permanently, with only a hand-edit to clear it. Refusing
  to mint costs one boot of anchors; minting a doubtful payload costs the
  journal. So the catch-all refuses rather than repairs.
- **No such journal can already exist.** The pre-fix build raised inside
  `read_prior_anchors`, which runs BEFORE `acceptor.accept(seed)` — so it
  failed to start rather than journalling a bad seed. The damage was
  bounded to "the maker will not boot", never to a poisoned journal.
- **mypy earned its place in the gate.** The review pass skipped it; running
  it caught a shadowed local (`entry`) introduced by the fix itself.
- **"Hash-valid" is not "trusted".** The integrity hash proves the bytes are
  what was written. It says nothing about whether the values inside are ones
  this build can parse — a distinction that matters precisely because this
  reader is deliberately lenient about schema.

### Decisions made *(mirror into [[market-maker/decisions]])*

- **Read-side validation only, and refuse-don't-repair on the mint path.**
  Nothing unparseable may enter a journalled seed; anything unexpected
  means mint nothing and stay re-mintable.
- **A missing prior directory is an alarm, not a skip** — distinct verb,
  distinct report field, journal untouched.
