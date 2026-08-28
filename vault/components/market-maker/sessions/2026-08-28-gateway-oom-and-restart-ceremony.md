---
description: "The FIX gateway OOM of 27-08, its root cause in the order tracker, and the restart ceremony error that cost mm-1 half its book on 28-08"
---

# 2026-08-28 — the gateway OOM, and the restart that broke the book

> **Who:** Claude session (inplay-vault-c9), George
> **Type:** incident / build
> **Refs:** gateway PR #29 · `inplay-fix-gateway-go@64dda79` · alert policies
> `14768873194610972375`, `4269185418752705984`

## What we did

- Traced the 27-08 outage end to end. The kernel OOM-killed `gateway-go` at
  **7.77 GB** on a 7.8 GB box with no swap, at 13:17:13. The VM then rebooted
  uncleanly.
- Proved the cause four independent ways: the kernel's per-process table, a
  live heap read through `/proc/<pid>/mem`, the retail gateway as a natural
  control, and a local reproduction with pprof.
- Deployed memory metrics and two alert policies to `inplay-fix-gateway-mm`.
- Shipped PR #29 — `strings.Clone` on `OrderID` and `ExecID`, plus the metric
  publisher into `deploy/vm/`.
- Ran the gateway cutover to `64dda79`. **Got the ceremony wrong, and cost
  mm-1 most of its book for about an hour.**
- Recovered with a fresh journal. Coverage returned to 138/138 in 77 seconds.

## What we learned

### The gateway leak

`OrderTracker.orders` and `.replaced`
(`internal/state/order_tracker.go:89-90`) have never evicted a row. The map was
written on 2026-06-02 and `git log -S` finds no `delete` in that file in its
whole history.

Each retained row also **pins its raw execution report**. `fix.ParseMessage`
splits the raw message with `strings.Split`, so every field aliases the backing
array of the whole message. `ApplyExecutionReport` stored two of those fields
on the row, which held the entire ~380-byte report for the life of the process.

- Live heap read: **194,767 complete FIX messages for 192,898 orders** — one
  whole retained message per order.
- The retail gateway runs the same binary, has published ten times more
  messages, and holds **62 orders and 21 MB after 26 hours**. The defect is
  market-maker replace volume only.
- Local rig, bytes per replace: unfixed ~1,597 · cloned 1,105 · cloned and
  evicted 228, with RSS flat over 600k replaces.

The same defect was fixed **in Redis** on 2026-08-20 with TTLs, after 935,575
of 1,510,596 hashes were untraded replace legs. The in-memory copy never got
the equivalent.

### The venue's own numbers

- tZERO reports `pos_size` **566,680** for `IPTCFRSB`, whose stated float is
  3,847. The taker's reconcile halt on 22-08 named the same symbol at
  venue=433,320 against its own 5,078. Nobody has ruled on it.
- `IPTCFAOW` is the **only symbol of 137 with zero house inventory**. Every ask
  is refused with `FAILSRISK … There are NO shares to SELL`, and it has been
  refused for over sixteen hours. Neither side then rests.

## What went wrong / got stuck

### 🔴 The restart ceremony error — read this before the next cutover

The plan said: send an explicit `cancel_all` from the maker, then confirm
`open_orders` reaches about zero. **I judged that stopping mm-1 and letting the
dead-man sweep achieved the same thing. It does not.**

The difference is whether the maker knows its book is gone.

1. `11:29:38` mm-1 stopped.
2. `11:29:50` the dead-man cancelled 1,082 of its orders — behind its back.
3. `11:35` mm-1 restarted, replayed its journal, and its replayed record still
   listed those 1,082 as resting.
4. It then tried to cancel orders that no longer existed — **5,164
   `UNKNOWN_ORDER` local rejects**, about 3.4 a second.
5. Its converger stalled on that reconciliation. `books` oscillated 86–115
   instead of holding at 138. Coverage fell from ~1,115 resting orders to 199
   and stayed there.

The maker's own boot line had already said so:

> `boot heal: NONE — MM_BOOT_HEAL=off. The engine boots on today's behaviour:
> a dead-man sweep during the outage leaves phantom orders in the replayed book`

**`MM_BOOT_HEAL=on` alone did not fix it.** The healer issued 706 cancels and
cleared that batch, but `MM_JOURNAL_PATH` was pinned to
`/var/lib/mm/supervised47/journal.jsonl`, so every restart replayed the same
journal and re-minted the phantoms.

**What fixed it:** a fresh journal directory, the prior directory kept for
anchor carry-over, and a bumped config version so new ClOrdIDs cannot collide
with the phantom ids.

```
MM_JOURNAL_PATH=/var/lib/mm/supervised48/journal.jsonl
MM_PRIOR_RUN_DIR=/var/lib/mm/supervised47
MM_CONFIG_VERSION=CFG-0046
```

Coverage went 1 symbol → **138/138 in 77 seconds**, rejects to zero.

### Other faults found and not yet fixed

- **Nothing watches quote coverage.** A maker quoting 65 of 138 symbols raises
  no alert. George found it by eye on the panel.
- **The maker logs no venue rejects.** `grep -ic reject` over its journal
  returns 0. `IPTCFAOW` failed every ask for sixteen hours in silence.
- **Cloud Monitoring notifies once per incident.** The taker's `snt/halted`
  alert fired on 22-08 and went silent for nearly six days while the condition
  stayed true.
- **`snt-1` has been halted since 2026-08-22 21:45Z** on a reconcile halt that
  says "resume only after a human decides which number is real". No human has.

## Decisions made *(mirror into [[market-maker/decisions]])*

- ✅ **2026-08-28a — a gateway cutover requires a fresh maker journal.**
- ✅ **2026-08-28b — `strings.Clone` ships; eviction does not, yet.**
- ⚠ **2026-08-28c — a dead-man sweep is not a substitute for `cancel_all`.**

## Questions opened / closed *(mirror into [[market-maker/open-questions]])*

- **Opened —** why does tZERO report a position 112× an instrument's float?
  (`IPTCFRSB`: venue 566,680, float 3,847.)
- **Opened —** who seeds house inventory, and why was `IPTCFAOW` missed?
- **Opened —** should the taker's reconcile halt auto-resolve, or fail loudly
  and repeatedly, instead of waiting silently for a human?
- **Open —** the terminal-row sweep design. Four independent reviews agreed the
  direction and blocked the plan as written. See
  `design-terminal-sweep` (scratchpad) for the required changes: port
  `stampAndPrune` from `inplay-market-maker-go`, exempt `CumQty > 0`, add a
  count ceiling, give it its own goroutine, add a runtime kill switch.
