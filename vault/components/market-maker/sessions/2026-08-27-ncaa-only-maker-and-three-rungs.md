---
description: "The maker returns after the offering: NCAA-only universe, three rungs restored, dead-man timers back to 10s/30s — and the MM gateway VM I hung with a log read"
---

# 2026-08-27 — The maker returns: NCAA only, three rungs, and a VM I hung

> **Who:** George + AI session.
> **Type:** live operations. Two maker cutovers, one gateway restart, one
> instance reset.
> **Refs:** [[market-maker/sessions/2026-08-26-test-ticker-census]] ·
> MM `main@f9eec8b` · gateway `main@0bd1782` ·
> `deploy/OBSERVABILITY-REDEPLOY.md` §2.
> **⚠ Ends with the maker LIVE on 138 NCAA books, the taker STILL HALTED.**

---

## What we did

### 1 · The offering closed itself

All 138 NCAA asks expired at 02:00Z on their own GTD `expireTime`. The
venue showed no offer and no bid on any NCAA book at 13:20Z. George asked
to cancel them; nothing needed a cancel. The MM gateway tracker still
listed 137 of them as open — the gateway's view, not the venue's. The
runbook records that exact trap.

### 2 · ⛔ I HUNG THE MM GATEWAY VM

**Cause: mine.** The taker's float table is wrong on every book, so I
went to read the venue positions out of the wire logs. I ran the read ON
`inplay-fix-gateway-mm` — a live trading VM with 2 vCPU and 8 GB. The
first job read whole log segments into memory. The second ran
`zcat | grep` pipelines with no `nice`.

- 12:52Z the VM stopped answering SSH, ping and port 8080, from inside
  the VPC as well as outside. GCE still reported RUNNING.
- The MM gateway holds FHINPLAY02 and the whole MM namespace, so the
  direct ticket died and `mm-test` lost its venue path.
- 13:24:55Z instance reset (George's go). SSH answered 20 s later. The
  gateway logged on at 13:25:06Z and rehydrated 2,154 orders. It sent
  zero cancels. No venue order was lost.

**The lesson, and it is not a new one** (the 18 Aug hang has the same
shape): never run a heavy read on a trading VM. The logs ship to
`gs://inplay-fix-gateway-logs/inplay-fix-gateway-mm/2026/08/` — pull them
and read them on a laptop. ⚠ The 22–26 Aug shipped segments are ~0 MB, so
the IPO-week fills exist only in the VM's own log files. A single
`nice`d, one-file `grep` is the way to read them.

### 3 · The maker, NCAA only (CFG-0044)

George: secondary trading and the maker run on the NCAA teams only. Two
edits, not one — the engine refuses a reviewed-inputs file that names a
ticker outside `MM_SECURITIES`:

| Setting | Value |
|---|---|
| `MM_SECURITIES` | the 138 NCAA tickers (was 170) |
| `MM_SUPERVISED_INPUTS` | `supervised-inputs-138-ncaa.json` (built from the 170 file) |
| `MM_CONFIG_VERSION` | `CFG-0044` |
| `MM_JOURNAL_PATH` | `/var/lib/mm/supervised46/journal.jsonl` |
| `MM_PRIOR_RUN_DIR` | `/var/lib/mm/supervised45` |
| `MM_BOOT_HEAL` | `off` — shape B |

Shape B, because the universe changed. Started 13:28:44Z. 138 books
quoting inside a minute, 275 accepts, 20 rejects in the first minute.
The rejects self-limit: 4 are IPTCFAOW "not long, NO shares to SELL",
the rest are first-tick aggressive-price rejects while the marketable
guard has no book yet.

### 4 · The dead-man timers came home, and the per-bot latch proved itself

The offering posture left both timers at **7 days**. Restored to the
dictionary values in `/opt/fix-gateway/.env`:

```
MM_DEADMAN_TIMEOUT_MS=10000
MM_DEADMAN_BOOT_GRACE_MS=30000
```

⭐ **The per-bot dead-man (gateway PR #28, deployed 26-08) did exactly
what it was built for, on its first real firing.** After the restart:

| Bot | Heartbeats | Outcome |
|---|---|---|
| `mm-1` | beating | **untouched** — book kept |
| `mm-test` | silent since the hang | swept, 2,134 cancels |
| `snt-1` | never beats by design | swept, 1 cancel |
| `""` (unattributed) | fed by `mm-1` | not fired |

The old global latch would have taken all three together, including the
live maker's book. ⚠ `snt-1` never publishes MM heartbeats (it must not —
a second beater would mask the engine's death), so **the taker's resting
orders are swept whenever every bot goes quiet**. Its one order
(IPTCTXLH buy 398,523 @ 62) went with the sweep.

### 5 · Three rungs (CFG-0045)

George asked for min 1 / max 3. The change was already on `main` as
`f9eec8b` from a parallel session; the VM ran `76341d3`, two commits
behind. Shipped by git bundle (the VM checkout has no GitHub remote).

| | before | after |
|---|---|---|
| `min_levels` | 1 | 1 |
| `max_levels` | **1** | **3** |
| `min_step_ticks` / `max_step_ticks` | inert | 1 / 4, live again |

Second cutover, same shape B: `CFG-0045`, journal `supervised47`, prior
`supervised46`.

**The sequence, and step 1 is the one nobody would guess:**

1. Restore the dead-man timers FIRST. Shape B relies on the sweep to
   clear the old book when the engine stops. At 7 days there is no
   sweep, and the new engine would post beside its own orphans.
2. `systemctl stop mm-1` → the sweep took 275 orders in ~9 s.
3. Ship the bundle, `git checkout`, apply the env delta, start.
4. Verify.

**Result at 14:03Z:** 561 resting orders over 138 books. Levels per side:
**86 books at 1, 92 at 2, 97 at 3** — the drawn 1–3 range, working. 137
of 138 books two-sided at the venue. IPTCFAOW is bid-only, correctly: the
account holds no FAOW shares and the ask cap binds at zero. No NFL book
and no twin carries a maker quote.

**Downtime: 13:57:28Z → 13:59:31Z, about two minutes.** One minute of it
was mine: the first bundle fetch named the ref `f9eec8b` when the bundle
carries `refs/remotes/origin/main`.

---

## What we learned

- A `git bundle` made with `A..origin/main` carries the ref
  `refs/remotes/origin/main`. Fetch that name, then check it out.
- `POST /md/probe` and the shipped GCS logs answer nearly every question
  about the venue without touching a live VM.
- The gateway's `/orders/mm` record uses `bot_id`, while the NATS payload
  and `/health` use `botId`. Both appear in one system.

---

## What went wrong / got stuck

- **The VM hang, §2.** Mine, avoidable, and the second time this shape
  has cost a reset.
- 17 `.TEST` orders sit in `PENDING_NEW` on the gateway from the hang.
  They belong to `mm-test`. `POST /orders/mm/prune` retires that shape.

---

## Decisions made *(mirror into [[market-maker/decisions]])*

- ✅ **The maker quotes NCAA only.** 138 books. The 32 NFL books carry no
  maker quote until George says otherwise.
- ✅ **Three rungs a side, drawn 1–3** — George, superseding Edwin's 20-08
  "one rung a side, do not build the optionality" (E51 answer 2).
  ⚠ Book-visible. Edwin has not been told yet.
- ✅ **Dead-man timers return to 10 s / 30 s** the moment an engine runs.
  The 7-day offering posture is over.

---

## Questions opened / closed

- Opened (N, George): the taker's floats. `SNT_FLOAT_OVERRIDES` is wrong
  on all 180 books — Hasan's 21-08 flatten zeroed the taker's venue
  positions and the IPO buys then landed on it. The journal's `rebase`
  records show a venue reading of 0 against every float. The taker cannot
  resume until the table is rebuilt from the venue.
- Opened: tell Edwin the rung count moved from 1 to 3.

---

## Next

1. Rebuild `SNT_FLOAT_OVERRIDES` for the 138 NCAA books from the venue's
   own figures. Read the wire logs OFF the VM.
2. Then resume the taker: fresh `SNT_CONFIG_VERSION`, fresh journal,
   `{"cmd":"resume"}` on `snt.control.snt-1`.
3. Tell Edwin about the three rungs.
4. `mm-test` is silent and its book is swept. Its owner decides whether it
   returns.
