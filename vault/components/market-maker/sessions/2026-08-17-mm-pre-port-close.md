---
description: "The pre-port close session: the ask cap reads the venue's own position, the reject tables get an index, and the boot healer's live evidence"
---

# 2026-08-17 — the pre-port close: W1, W2, W4 (W3 measuring)

> **Who:** Claude (implementation) + George
> **Type:** build
> **Refs:** `specs/2026-08-17-mm-pre-port-close/BRIEF.md` · MM
> [#52](https://github.com/Novosapien/inplay-market-maker/pull/52) (W2) ·
> [#54](https://github.com/Novosapien/inplay-market-maker/pull/54) (W4) ·
> [[market-maker/build-deploy-log]]

## What we did

Took the four W-items of the pre-port close. Two are built and in review,
one is measuring on the rig, one turned out to be half-done already.

| Item | State |
|---|---|
| **W1** boot healer switched on | ⚠ config ALREADY LIVE (another session); classifier proven read-only; the drill's own question answered; the boot log is NOT durable |
| **W2** ask cap reads the venue | ✅ built, PR #52 |
| **W3** the second drain cost | ✅ **ANSWERED — not a scan**, PR #56 |
| **W4** the reject blind spot | ✅ built, PR #54 |

## What we learned

### The brief's baseline was stale before the session started

`main` had moved five commits past the brief's `0b9f601` — PRs #45, #46,
#49, #50, #51, all landed 15–17 Aug by a parallel session. Live is
**supervised40 / CFG-0037 on `main@87cb35f`**, booted 21:28Z. The vault's
build-deploy-log records **none** of CFG-0029→0037 or supervised34→40.
`main` moved again *during* the session (to `1bf4479`, #50).

The engine is healthy on it: **zero missed sweeps** in the run.

### W2 — the venue has been publishing the number all along

The measurement came before the build, and it settled everything:

| Question | Answer |
|---|---|
| Does `posSize` (tag 9383) reach the MAKER? | **212/212 exec reports — 100%** |
| Per-symbol, or firm-wide? | **Per symbol** — 140 distinct securities |
| Does it track our own fills? | **133/133 deltas exact**, zero mismatches |
| Shared with the taker? | **No** — maker acct `1797733477`, taker `4963224393` |
| What does the venue say we hold? | **59,277 – 106,225 shares per book** |

⭐ **The account holds ~100,000 shares a book, and `opening_position_shares`
is a 0 stub.** R-Q08 has been failing open against a real holding all along.
E27 was never the blocker it looked like — the number was on the wire.

Then, driven through the new adapter and fold, against **180 real captured
production exec reports**: 180/180 carried the figure, and the fold agreed
with the venue's own latest number on **all 119 securities, zero
mismatches**.

⭐ **And activating the cap changes nothing today.** Against the live order
book: **0 of 119** books would have their ask side emptied, **0 of 119**
would have their ladder resized. The tightest book (IPTCEAGL) offers 52.6%
of its holding; p50 is 25.9%. It is a rail that only engages when a book
gets thin — which is exactly the state the 15-08 IPTCBEAR finding predicted.

### W4 — the finding is the blind spot, not the cost

`RejectBackoff.suppression()` filtered the whole portfolio's tables to
answer a per-security question, at 4 Hz. **The six-game rig structurally
cannot see it** — the synthetic venue never rejects, so both tables are
empty for the entire run. Production agrees while it is healthy:
supervised40's first 37 minutes had **0 order rejects and 11 cancel
rejects**. The function is free until it is not.

Measured, changed, re-measured on adjacent arms in one process:

| entries | 0 | 1,000 | 4,000 | 8,000 | 16,000 |
|---|---|---|---|---|---|
| flat | 0.027 | 1.707 | 4.498 | 8.634 | **29.066** |
| indexed | 0.029 | 0.222 | 0.504 | 1.022 | **1.546** |

At the production ceiling: **3.762 → 0.429 ms/pass, 8.8×**. The 16,000
column is the **15-08 disk-full incident**, where a dead FIX session locally
rejected every order at ~500 per book — the old shape spent **11.63%** of
every converge interval on this scan at precisely the moment the venue was
in trouble.

### W1 — the healer is configured, and the ownership boundary holds on real ids

`MM_GATEWAY_OPS_URL` and `MM_GATEWAY_OPS_KEY` were **already set on the
running engine** by the parallel session. Verified independently from the
MM VM: the route answers **200** with a well-formed `count` + `orders` body.

The real classifier (`plan_boot_heal`) was then run **read-only over the
live 1,588-entry index**:

- **1,587 ours** (`MM` + 16 hex) · **1 taker** (`MMSN`) · **0 ambiguous,
  0 foreign, 0 malformed**

⭐ The `MM` vs `MMSN` boundary — the one the design said "reads thin until
written down" — is **proven correct on production ids**, and the taker's
single order is classified TAKER and never touched.

Two arms of the plan:

- record EMPTY (a fresh journal) → **1,587 cancels planned** — the ceiling
- record knows them → **0 cancels**

⭐ **And that answers the drill's own open question.** The build-deploy-log
warned that a boot cancelling the whole record puts one venue event per
cancel against the 512-per-tick drain cap, "which at CB1's pre-CB4
9.893 ms/ack is ~5 s in one tick, i.e. the beat-stall threshold". On the
measured numbers:

- 1,587 cancels ÷ 512 cap = **4 ticks**
- at CB4's **0.298 ms/ack**: 512 × 0.298 = **153 ms** per tick — inside the
  500 ms tick, 473 ms of drain in total
- at CB1's pre-CB4 **9.893 ms/ack**: 512 × 9.893 = **5.07 s in one tick** —
  past the beat-stall threshold

**CB4 is what makes the healer safe to switch on.** Before the prune fix it
would have stalled the beat and armed the dead-man on its own boot.

### W3 — the residual is WORK, not an algorithm

Two adjacent rig arms, one variable (book count):

| probe | 170 books | 85 books |
|---|---|---|
| acks | 65,792 | 55,268 |
| **ms/ack** | **0.6980** | **0.8114** |
| `1c_cycles` share | 58.3% | **58.5%** |
| `2_stage` share | 0.2% | **0.2%** |

⭐ **Halving the portfolio did not halve per-ack cost — it RAISED it**, and
the composition did not move at all. An O(portfolio) scan inside the drain
would have done the opposite on both counts. There is no scan to find.

The brief's first question is settled: **`sync.stage` is 0.2% of the
drain**. It is all `orchestrator.handle` — ~91% `_process_accepted`, of
which ~58% is `_drive_cycles`, the quoting recomputation itself.

⭐ **Why this is the answer the Go port needed.** An algorithmic scan would
have been INHERITED by the port — same shape, faster language, same wall at
NCAA scale. Work-bound cost converts directly into headroom instead. **The
port is justified, measured.**

⚠ Caveats that must travel with the numbers: the absolutes are NOT
comparable to `gate-v2-results.md` (a 300 s arm at 10× has only ~90 s at
full six-game load, because `PRE_ROLL_S` is 60 WALL seconds and the stagger
runs to 1,500 recorded); and the 6.5× curve itself was NOT reproduced — it
came from the v1→v2 workload step. Full record: `w3-drain-verdict.md`.

## What went wrong / got stuck

- 🔴 **The engine's boot log is not durable, so W1 cannot be verified as
  written.** The running engine's stdout is a **socket**
  (`/proc/303211/fd/1 -> socket:[933655]`), not a file — supervised37–40
  have no log on disk where supervised27–36 all do. W1's verification step
  is literally "verify in the boot log: `boot heal: DONE — …`", and that
  line is **unrecoverable for this boot**. It is a ceremony regression (the
  `> ~/supervisedNN.log 2>&1` redirect was dropped), not a code defect —
  and it is rule 1 ("any job over a few minutes emits a heartbeat, or it is
  not observable") biting the deploy that was meant to close AC8.
- ⚠ **The AC8 rig drill was never run, and the live cutover happened
  anyway.** The brief says do the drill BEFORE the live cutover. That
  ordering was violated by the 21:28Z cutover.
- ⚠ **The copied-venv trap is still live on the rig**: `~/mm-cb4/.venv`
  imports `mm` from `~/mm/src` — a different tree. The CB4 lesson is
  written down but the rig was never cleaned. This session built a fresh
  `~/w3` with its own venv and asserted provenance before measuring.
- **The 85-book arm crashed instantly on an unrecognised `--books` flag** —
  my probe never had one (it lives on `six_game_workload.py`). Worse, the
  runner touched its done-marker anyway, so the background watcher reported
  "both arms landed" when one had died in the same second it started. The
  watcher now checks the LOG for a result, not just the marker. Second
  instance in this session of a completion signal that was not one.
- **I killed my own SSH session twice with `pkill -f`** — the pattern
  matched the `--command` string carrying it. Use PIDs.
- **`--speed` does not scale ack load.** Two local arms at 1× and 10× came
  out at 0.1169 and 0.1206 ms/ack — nearly identical. `--speed` scales the
  READING replay, and ack volume is driven by book count, not game count
  (CB2 already found this: the 158 quiet books produce most of the acks).
  Worse, superlinearity is a **saturation** effect, and this Mac is ~4× the
  rig and never saturates. W3 has to run on the rig, at 1,800 s. An hour
  was spent learning that the fast machine cannot see the defect.

## Decisions made *(mirrored into [[market-maker/decisions]])*

1. ✅ **George, 17-08: the ask cap reads its position FROM THE VENUE — do
   not wait for Edwin's E27.**
2. ✅ **The maker takes the LATEST exec-borne figure, not the first** — a
   deliberate deviation from the taker's boot rebase the brief said to copy.
   The taker adopts once because it defends its own authoritative tally; the
   ask cap keeps no tally, so the venue's most recent answer is strictly the
   best evidence. Riding the EXECUTION envelope the journal already stores
   makes replay reproduce the fold BY CONSTRUCTION — no new event type, and
   no "since boot" notion a replay cannot see.
3. ✅ **`0` from the venue BINDS; `None` does not.** E27's stub conflated
   the two, and that conflation is the entire reason R-Q08 sat dark.
4. ✅ **`MM_ASK_CAP_VENUE=off`** is the operator's lever — the cap is
   book-visible, so it needs one without a code change.

## Questions opened / closed *(mirrored into [[market-maker/open-questions]])*

- **N43 rider 1 (sequencing)** — ✅ satisfied: `pending_quantity` shipped
  with the fix set and is already live, so supplying the position is no
  longer the same deploy that introduces it.
- **N43 rider 3 (kept rungs exceed the bound)** — ✅ measured moot today: no
  book is anywhere near its bound (worst is 52.6% of holding).
- **N43 rider 2 (`[post-first]` ordering)** — 🔴 **STILL OPEN and it is the
  one that gates activation.** New sells go out before the cancels of orders
  livS counts reclaimable, so a fully-offered book can still be rejected at
  submit. Decide cancel-first-for-over-committed-sell-books vs
  accept-residual-rejects.
- 🔴 **NEW — the maker's livS is OURS; the venue's is the ACCOUNT's.** A
  resting sell our record does not know about makes the bound generous, and
  R-V07 can still reject at submit. This is exactly what the F4 boot healer
  closes at boot, so **the ask cap and the healer are load-bearing for each
  other and should stay switched on together.**
- 🔴 **NEW — the engine's boot log must be durable.** Without it AC8 cannot
  be verified on any cutover, this one included.

## Next

George rules on: (1) the `[post-first]` rider, the last gate on activating
the ask cap · (2) whether the boot-log redirect goes into the runbook as a
mandatory ceremony step · (3) reviewing #52 and #54. Then **W3's rig arms
land** → the drain answer → the completion promise, the gospel pin, the hard
freeze, and the Go port discovery.
