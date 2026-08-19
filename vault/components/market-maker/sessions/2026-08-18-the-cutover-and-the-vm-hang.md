---
description: "The cutover to the pinned commit: the VM hung on a 3.5 GB journal replay, the taker was bricked by one torn line, and what the order book actually looks like"
---

# 2026-08-18 — the cutover, the VM hang, and the torn line

> **Who:** Claude + George
> **Type:** deploy + incident
> **Refs:** MM `main@fd193a4` (tag `mm-python-fix-set-complete`) ·
> [[market-maker/build-deploy-log]] ·
> [[market-maker/sessions/2026-08-17-mm-pre-port-close]]

## What we did

Merged the pre-port close (#52, #54, #56), pinned the gospel commit,
deployed it, hung the VM doing so, recovered, and later un-bricked the
taker from a corrupt journal line.

**Both bots are live on `fd193a4` and trading.**

## What shipped

| | |
|---|---|
| Gospel commit | **`fd193a4`**, tagged `mm-python-fix-set-complete` |
| Engine | `supervised41` / **CFG-0038** (fresh journal, version bumped with it) |
| Boot | `replayed 1 event` |
| Anchors | ⭐ `JOURNALLED 14 anchors from supervised40` |
| Boot heal | `DONE — 10 orders · cancelled 8 unknown · left 2 taker · ALARMED 0 · 19 ms` |
| Gate at the pin | 1,295 tests, ruff clean, mypy src clean — **run on the VM itself**, not only locally |

AC10 is restored: `main` and the running engine are the same commit again.

---

## ⛔ THE INCIDENT — a 3.5 GB journal replay hung the VM

**Cause: mine.** I chose to KEEP the journal on the cutover, because the
boot healer exists precisely to retire the fresh-journal ceremony. What I
never checked was whether **replaying** that journal fits in the box.

It did not. The journal had grown to **3.5 GB / 3.15 M events** — grown
*because* previous cutovers had been keeping it. On an n2-standard-2
(2 vCPU, 8 GB):

- 09:41 engine boots on `fd193a4`, starts replaying
- RSS reaches **3.9 GB**
- 09:53 systemd itself starts timing out (`dbus auth elapsed: 145,927 ms`)
- 10:08 `systemd-logind` cannot start; the **metadata server** times out
- SSH refuses entirely — no graceful path left
- 10:09 instance **reset**

### What made it survivable

- ⭐ **The dead-man swept the book from 1,588 orders to 10** the instant
  the old engine stopped. There was no exposure at any point — the failure
  mode was "not quoting", never "quoting wrongly".
- The taker was already stopped.
- 05:41 ET, **no games live** (R11 satisfied).

### The recovery, which is the path I should have taken first

Fresh journal `supervised41` + bumped `CFG-0038` + `MM_PRIOR_RUN_DIR=supervised40`:

- boots in **one event** instead of 3.15 M
- **`ANCHOR_SEED` carried the 14 kickoff anchors forward anyway** — the
  exact thing it was built for, so keeping the journal bought nothing
- the boot healer cleaned the venue side in 19 ms
- RSS **51 MB** instead of 3.9 GB

⚠ **THE RULE THIS EARNS: journal size is a pre-flight gate on every
cutover.** The healer makes keeping a journal *safe*; it says nothing
about whether replaying it *fits*. Check the size and the box before
choosing keep-vs-fresh. `ANCHOR_SEED` means a fresh journal costs almost
nothing, so the bar for keeping one should be high.

---

## ⛔ THE SECOND INCIDENT — one torn line bricked the taker

At **13:40:32** the taker's journal stopped mid-record:

```
{"kind": "send", "limit_px": "76.79", "qty": 8, "seq": 294157, "side": "sell"
```

One bad line out of 587,722 — and it was the **last** one. The taker
replays its whole journal on every start, `json.loads` throws on that
line, the process exits, systemd restarts it, and it fails again. It
crash-looped every ~6 seconds for hours. **It was not "shut down" — it
could not start.**

A clean `SIGTERM` finishes the line in flight. Only a hard kill leaves one
torn, so something killed it uncleanly at 13:40:32.

**Repair:** backed the journal up (`journal.jsonl.torn-backup-1620`),
dropped only the torn final line, verified all 587,721 remaining lines
parse, restarted. It booted clean — no halt, straight to `state=AUTO`.
Dropping it is correct: an incomplete write means the event never became
durable, so that `seq 294157` send never counted.

⚠ **THE GAP: a single torn final line permanently bricks the taker until a
human edits the file.** That is the normal consequence of any hard kill,
so it will happen again. `snt/journal.py`'s replay should tolerate and
truncate a torn FINAL line itself — mid-file corruption should still
raise. Small fix, and **the Go port inherits the same replay design**, so
it belongs in that brief too.

---

## What the order book actually looks like (George's question)

George reported lopsided books, wide spreads, and an empty Bengals book.
Investigated at the venue rather than from the engine's own claims. Three
findings, and **only the third is a real open item**:

**1. Lopsided depth is BY DESIGN.** `min_levels=3, max_levels=6`, drawn
per side per book. "6 bid levels and 3 ask levels" is in spec. 86 of 161
books were lopsided at one sample — expected, not a defect.

**2. Empty and thin books are CHURN.** The taker takes **~3.4 levels per
second** portfolio-wide; the maker reposts on a 500 ms pulse. Any snapshot
catches half-rebuilt ladders. Proven by re-sampling 45 s later:

| book | sample 1 | 45 s later |
|---|---|---|
| **IPTCBENG** | 0 bids, 2 asks | **2 bids, 2 asks** |
| IPTCAZWC | 0 bids, 2 asks | 2 bids, 2 asks |
| IPTCEMEA | 2 bids, 0 asks | 3 bids, 2 asks |

80 of 135 lopsided instances moved between the two samples. Portfolio-wide
the book was *rising*: 684 → 754 resting, 129 → 147 two-sided.

⚠ **The real consequence: the steady state is a permanently half-empty
book**, because the taker consumes faster than the maker rebuilds. That is
not a defect in either component — it is the two RATES being mismatched.
The lever is `SNT_INTERVAL_LIVE_S`, a deploy decision.

**3. 🔴 OPEN — eight books are persistently one-sided.**
No asks: **BEAR, MIWV, NTMG, RAID, VOLS**. No bids: **CINB, GOPH,
LION.TEST**. Across two samples 45 s apart, so not churn. **Unexplained.**

### The ask cap (W2) is CLEARED as a cause

Measured live: venue positions are **96,679 – 104,320 shares on every
book**, and `IPTCBEAR` — which shows no asks — holds **103,595**. Zero
books under 1,000 shares. The cap has ~100k of headroom against ~50k
ladders. All `ASK_CAP_*` alarms are zero. It is not binding anywhere.

Also ruled out for the stuck books: venue rejects (0), suspensions (0),
quarantine (0), missed sweeps (0).

### Two red herrings, recorded so nobody re-chases them

- **`refused=19,693` and climbing** is **ONE book** — IPTCPATR, refused
  every pass because our ask sits ~8 cents *below* a real bid at 73.18.
  The guard is correct; our PRICE is wrong. That is E31 (width/offsets),
  Edwin's, and it is the same class as the SAIN/JAGU note.
- **`PUB_SHED` at ~98%** is **pre-existing and by design** — the state
  publisher sheds `resting_orders` to fit the 262,144-byte budget, and has
  since at least 17-08 18:04. It means anything reading `mm.state` sees a
  thin picture, which is worth knowing when a dashboard looks wrong.

---

## What went wrong (process, not code)

- **I kept a 3.5 GB journal without checking it would replay.** The
  healer made it *safe*; it did not make it *possible*.
- **I told George "no rush" on a halted taker** that was not trading. It
  sat halted for an hour while we discussed it. The right framing was
  "it is not trading while we decide".
- **`pkill -f` killed my own SSH session twice**, because the pattern
  matched the command string carrying it. Use PIDs.
- **A background watcher reported success for a crash** — the runner
  touched its done-marker even though the job had died on an unrecognised
  flag. Watchers must check for a RESULT, not a marker. Third instance in
  two days of a completion signal that was not one.

## Decisions made *(mirror into [[market-maker/decisions]])*

1. ✅ **The gospel commit is `fd193a4`**, tagged. It is the Go port's
   reference commit.
2. ✅ **Journal size is a pre-flight gate on every cutover.**
3. ✅ Cutovers keep the journal only when it is small enough to replay;
   `ANCHOR_SEED` makes a fresh journal cheap.

## Questions opened / closed

- 🔴 **NEW — why are eight books persistently one-sided?** Inventory,
  rejects, suspensions and the ask cap are all ruled out.
- 🔴 **NEW — the maker/taker rate balance.** The taker eats faster than
  the maker rebuilds, so the book is structurally half-empty.
- 🔴 **NEW — the taker's replay must survive a torn final line.**
- ✅ **The AC8 rig drill is arguably moot** — the healer did it for real
  on 18-08, cancelling 1,645 orphans and leaving the taker's order alone.

## Next

The deep investigation into the order book: the eight stuck books first,
then the maker/taker rate balance — that second one is what makes the
whole book look wrong.
