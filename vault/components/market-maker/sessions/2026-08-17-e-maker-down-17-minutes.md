---
description: "The maker ran for 17 minutes with no market after a gateway ceremony stopped it and nothing restarted it — the recovery, and the systemd unit that was always owed"
---

# 2026-08-17e — the maker was stopped and nobody noticed for 9 minutes

> **Component:** [[market-maker/market-maker]] · **Type:** live incident
> Follows [[market-maker/sessions/2026-08-17-c-halt-alerting]], which built
> the alert that caught this.

---

## 1 · What happened

Hasan's 16:29Z gateway deploy ran the ordered ceremony and stopped the
engine. **The restart step never took.** The engine has no supervisor, so
nothing brought it back.

| time | event |
|---|---|
| 16:29:30 | engine stops. Last write to `supervised35/journal.jsonl` |
| 16:29–16:46 | **no market.** Taker fills fall from ~300/min to 9 in 3 min |
| 16:38:47 | **`MM-1 maker DOWN` fires** — 9 min 17 s after death |
| 16:41:54 | taker halted (ordered sequence) |
| 16:46:09 | engine up, book standing, taker resumed |

**17 minutes with no quotes on any book.** This morning the same class of
failure — a bot stopped, nothing watching — ran for **50 hours**. The
alert built earlier the same day closed that to nine minutes on its first
real test, and it fired unprompted.

⚠ Even so, a human guessed it before the page was read. The alert is the
floor, not the ceiling.

## 2 · The recovery

Fresh journal was REQUIRED, not optional: the gateway's dead-man sweep
fired 3,187 cancels while the engine was down, and those never reach the
engine's journal — replaying `supervised35` would re-stand phantom ACTIVE
orders. That is the case `deploy/OBSERVABILITY-REDEPLOY.md` §2.2 exists
for.

```
CFG-0032 -> CFG-0033
journal  supervised35 -> supervised36
MM_PRIOR_RUN_DIR = supervised35   (carries the anchors, F2)
code unchanged at mm-main-d2b2fb5
```

Result:

```
anchor seed: JOURNALLED 14 anchors from supervised35 (checkpoint seq 6964985 + 0 tail)
state publisher: ON — journal supervised36 · realized P&L accumulated from the whole journal
book standing: 1552 instructions for 180 securities
```

14 anchors carried, and it booted on FULL replay — so `realized_pnl_total`
is correct rather than the tail-only case.

## 3 · ⭐ The boot looked hung and was not

For ~3 minutes the process sat at **99.8% CPU, state R, one thread**, with
three lines of log and a 0-byte journal. It was working:

```
fd 10 -> /var/lib/mm/supervised35/journal.jsonl   pos 5,301,444,608 / 8,022,795,949
```

It was folding the **8 GB** prior journal to carry the anchors. The
checkpoints existed but were written under CFG-0032, and `load_latest`
only accepts a checkpoint under the RUNNING config version — which the
ceremony had just bumped. So a full fold is the documented, expected
consequence of the version bump.

**Diagnose a "hung" engine with `/proc/PID/fdinfo`, not by watching the
log.** A read position against a file size answers in one command what a
silent log cannot.

⚠ **This cost grows.** `supervised35` reached 8 GB in about a day, and the
fold sits in the middle of every recovery. The cheapest moment to run the
next ceremony is always the earliest one, because the fold is over the
CURRENT run's journal.

## 4 · Fixed in this session

- ✅ **The maker now has a systemd unit** (`mm-1.service`): `Restart=on-failure`,
  `RestartSec=15`, `StartLimitBurst=5` in 600 s so a crash loop cannot
  hammer the venue with book re-stands, `WantedBy=multi-user.target` so a
  reboot brings it back. Env split `/etc/mm-1/env` + `/etc/mm-1/env.secret`
  (0600), built from the RUNNING process rather than reconstructed.
  **Installed and enabled, deliberately NOT started** — the engine is live
  under `setsid` and must not be double-started. It takes over at the next
  ceremony, so it costs no extra restart.
  ⚠ `on-failure`, never `always`: a deliberate stop during a cutover must
  stay stopped.
- ✅ **The engine now runs under `setsid`**, not a `screen` session
  orphaned to PID 1. A dropped shell can no longer kill it.
- ✅ **`snt-halt-check` gets `SuccessExitStatus=1`.** It exits 1 when a bot
  does not answer — the check RAN and wrote the metrics that paged us, so
  systemd marking the unit "failed" on exactly the runs that matter was
  backwards, and it buried the real failures (2 = no credential, 3 = metric
  write).

## 5 · What this says about the ceremony

The ordered sequence is correct and was followed on the way down. It
failed on the way up, silently, because **nothing verifies that the thing
you stopped came back**. A ceremony that ends without asserting its own
end state is a checklist, not a procedure.

The alert is now that assertion, at ~9 minutes. A `systemctl is-active`
at the end of the cutover would be faster and free.

## 6 · Next

1. PR #15 (gateway identity fallback) needs a ceremonied bounce. Run it
   SOON — `supervised36` is small now, so the anchor fold is near-instant.
2. Start the engine via `mm-1.service` on that bounce. Bump to CFG-0034 /
   `supervised37`, `MM_PRIOR_RUN_DIR=supervised36`.
3. The four orphaned gateway orders still page on every fill until #15
   lands.
