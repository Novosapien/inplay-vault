# 2026-08-09b — HANDOVER: state of the machine, and where the next session starts

> **Type:** handover — read this, then the working guide's §1 order.
> **Covers:** 07-08 through 09-08. Written to be the single entry point
> for the next session, human or AI.

---

## 1 · Where everything is

| Repo | Branch | Head | State |
|---|---|---|---|
| `inplay-market-maker` | `main` | `b42aa65` | clean · 609 tests · ruff + mypy-strict green · **pushed** |
| `inplay-vault` | `docs/t0-plain-english-guide` | `cce3d41` | clean · **not pushed** (no ruling to push it) |
| `inplay-sportradar-service` | `feat/mm-probability-publisher` | — | local only, **unpushed** — carries the publisher half of the readings contract. Flagged four times now; it gates test A2 stage 2 |

**Live right now:** the MM engine runs on the VM `inplay-market-maker`
(10.0.2.3), supervised mode, **CFG-0004**, journal
`/var/lib/mm/supervised5`, engine `dfa87f9`. Up ~15 hours. The poker has
finished. **SNT-1 is built but NOT deployed anywhere.**

⚠ **The engine is doing something undesirable while it runs** — see §4.

---

## 2 · What was built and merged

| PR | What | Effect |
|---|---|---|
| #8 | Move-size fix — a moved order adopts its new rank's drawn size | Visible ladder monotone 5.8% → 32–36% |
| #9 | An in-flight replace occupies its destination price | 19 doubled levels → zero |
| #10 | **SNT-1**, venue-hardened from Edwin's reference | New `src/snt/`, 27 tests, undeployed |

Combined effect on the live book: monotone **69.7%** (84% is the target
ceiling; the remainder is the E17 remnant — bites and kept generations).

---

## 3 · ⭐ The finding that changes the build — the sell rule

Live probe, 08-09, on George's own account with his authorisation:

```
FAILSRISK[5120866205]: You can SELL at most 50 shares of IPTCGIAN. Pos=100 livS=50
```

- **sellable = Pos − livS** — position minus quantity already committed
  to LIVE RESTING SELLS.
- Over that, the venue **rejects the WHOLE order**. Never part-fills,
  never opens a short.
- It is a **venue rule, not per-account config**. The MM's "You are not
  long" reject is the same check at `Pos = 0`.
- No vendor document states any of this. The OE spec does not even
  enumerate side 5.

**Why it matters:** the ask side of any ladder is inventory-bounded,
which couples ladder sizing to **E27** (the opening position). And for
SNT-1 it is correctness — without the gate, it rejects on its own sells
the first time it trades a book down.

---

## 4 · ⚠ Three live problems, none of them fixed

1. **The engine crosses the stale book on every repost.** Its bids are
   marketable against third-party stale asks left on the QA books. Once
   measured: a COWB bid at 76.04 swept 8 levels — **920 shares,
   $50,366**, position 100,930 → 101,850. The MM is TAKING liquidity
   while intending to rest. Recurs on every cycle. **This is the most
   urgent item.**
2. **Replace churn with no new information** — ~40 replaces/minute for
   15 hours with the poker stopped and inputs static: 35,982
   ORDER_REPLACED and 9,156 CANCEL_REJECTED since boot. Nothing should
   be moving. Diagnose before the reject-backoff build.
3. **The engine adopts any MM-prefixed order on its user id** —
   `_get_or_admit` admits an unregistered ack as ACTIVE, so the
   reconciler cancel/replaced a hand-sent probe 0.7 s later. **No manual
   order on the MM user id is safe while the engine runs.** Probes must
   use a different identity on the MM transport (that is what worked).

---

## 5 · Corrections to things previously recorded as true

- **DONE_FOR_DAY never happens.** No `39=3` anywhere in the gateway FIX
  log; orders from 08-08 00:31 survived two 23:59 ET boundaries and
  still rest. The 22-07 adopted "venue fact" is contradicted, test **B1**
  loses its premise, and **E36**'s "book vanishes nightly" worry
  evaporates unless production differs → **T14**.
- **The app holds three contradictory beliefs about oversell.**
  `venueOrders.ts` correct (now verified) · `OrderEntrySheet.tsx` wrong
  ("fills up to your position") · `buying_power.py` over-cautious but
  its client-side refusal is right behaviour.
- **Two claims made and retracted mid-session** (mine, both from
  over-reading greps): "those sells are all side 2" — they included
  side 5; "this is per-account configuration" — it is a venue rule.
  Tag `9383` does not move per fill in the log, so co-occurrence there
  proves nothing. Only the controlled probe settled it.

---

## 6 · New documents — the ones that change how sessions work

- **[[market-maker/requirements]]** — the MM's normative go-live list.
  ⚠ **George has an open decision: keep it, or let the taker doc stand
  alone?**
- **[[market-maker/market-taker-requirements]]** — SNT-1's normative
  list, 44 requirements. **This is the build document for the next
  phase.**
- **[[market-maker/test-plan]]** — 14 live test cases. B1 now records a
  falsified premise rather than a result.
- Both requirements docs change ONLY through their dated addendum —
  never edit a requirement silently.

---

## 7 · Where the next session starts

**Build, in this order:**

1. **The stale-book crossing guard** (R-Q09) — the engine must not
   publish an order that is marketable against the live book. It is
   live and moving money right now.
2. **The sell gate** (R-Q08 / T-O07) — `Pos − livS` for the MM ladder,
   and mandatory for SNT-1.
3. **SNT-1's seeded float + baseline** (T-O08) — the inventory rule
   measures drift from the float, not from zero. Makes the taker
   long-only by construction.
4. **The replace churn** — diagnose, then the reject-backoff build
   (R-R03, test C4).

**Then:** systemd unit + N15 jitter recorder · N31 group commit ·
C2 (checkpoint resume on live data).

**Owed to people:**
- **Hasan** — the ghost cleanup, the LmtPerc reference (gates the other
  163 books), the user-side wash verification, the infra file, and the
  two MD findings (the stale-book evidence; naive `market.quote`
  consumers see partial documents).
- **Rob (tZERO)** — **T14** (is there a session roll at all?), **T15**
  (which risk toggle governs the sell check; no read-back exists), the
  pending wash/MPID answer, and the IPLP account for SNT-1.
- **Edwin** — E17's remnant, E31 ladder shape, the A4 final-whistle
  question, and **E32's SNT-1 rulings** (his 8-tick spread gate would
  never trade a production book).
- **Troy / legal** — E33/T13, including the profit-tilt disclosure.

**Decisions George owes:**
- Keep or drop the MM `requirements.md`.
- Push the vault and sportradar-service branches?
- Deploy SNT-1 in QA posture (MM account) or wait for IPLP?

---

## 8 · Operational rules learned the hard way

- Every redeploy bumps `MM_CONFIG_VERSION` and takes a fresh journal
  directory — the dead-man sweeps while the engine is down and those
  cancels never journal, so an old journal replays phantom ACTIVE
  orders (until the R-D05 healer exists).
- `pkill`/`pgrep` patterns must never appear in the same SSH command —
  it kills the session.
- Judge the engine from the journal, not the panel: the `market.book`
  feed has served a provably stale book under churn.
- On these books, ANY engine cycle can trade. There is no such thing as
  a read-only poke while the stale quotes remain.
