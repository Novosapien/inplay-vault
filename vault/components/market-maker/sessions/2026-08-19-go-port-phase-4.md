---
description: "Go port Phase 4 build note — the ops surface, boot healer, anchor seed and the taker, with AC8's split result and the phase's 33 blind gates"
---

# 2026-08-19 — Go port, Phase 4: ops surface, boot features, and the taker

> **Who:** AI team — `venue`, `taker`, `core`, under a `team-lead`
> **Type:** build
> **Refs:** spec `2026-08-18-mm-go-port`, branch `feat/phase-3-ingestion`,
> pin `fd193a4`, [[market-maker/build/runtime]], [[market-maker/build/venue]],
> [[market-maker/parameters]]

> ⚠ **This note is NOT the phase's close.** `core`'s `deploy` chunk is still in
> flight: the composition root, the NATS client, the `MM_*`/`SNT_*` surface and
> the systemd units. The per-phase review runs after it lands.

---

## What we did

Phase 4 is the first phase with more than one stream, so it ran as a team. Four
chunks are done.

**Wave 1.**

- **`ops-surface`** (venue). The maker publishes the `mm.state` projection the
  pinned Python publishes, byte for byte. The tick STAGES an immutable frame; a
  separate goroutine encodes and publishes it. Money crosses as a JSON number
  quantised to six decimal places. Both shed stages are announced in `shed[]`.
- **`taker-core`** (taker). SNT-1's brain, schedule, pending book and journal.
  AC24 is measured, not asserted: a journal written by the pinned Python's own
  `SNTJournal`, and all four economic numbers reproduced as canonical decimal
  strings — including a realized total that runs to the 28th digit.

**Wave 2.**

- **`boot-features`** (venue). The `ANCHOR_SEED` lenient READER, the boot
  ceremony in order, the healer live on the boot path, the AC8 drill, and a
  durable boot log. `cmd/mm` boots a loopback stack through it.
- **`taker-venue`** (taker). The taker trades, reconciles and halts. AC13's
  hardest clause — it must never publish an MM heartbeat — is asserted by
  exhaustive path search, four ways.

**Also done.** `VenuePriceCap` corrected. Two vault documents corrected: the
missed-sweep threshold, and `parameters.md` row 35.

**Both gates hold.** `make gate` passes across all fifteen packages. `make diff`
passes eighteen subtrees on both corpora, unchanged from the start of the phase.

---

## What we learned

### AC8 passes its own clause and fails the envelope around it

The result splits, and both halves matter.

We synthesised a real **1,073,742,282-byte** journal — 1,093,132 lines, 1,090,732
events replayed — and measured a boot against it:

| | |
|---|---|
| first heartbeat | **+8.157 ms** ✅ |
| the WHOLE boot | **1 m 03.334 s** ⚠ against a 30 s grace |

The first heartbeat is prompt because the beat is step 2 of the ceremony and
everything that reads the journal is after it. That is structural, so it holds
at any journal size.

The whole boot is not. Between the boot beat and the run loop starting its beat
goroutine, **exactly one heartbeat has gone out**. The gateway's grace covers the
bot becoming live, not merely its first beat.

⚠ **A deploy always boots on a full replay, so this is reachable.** A checkpoint
boot replays only the tail and is fast. But R-D06 bumps `MM_CONFIG_VERSION` on
every deploy, and `load_latest` only accepts a checkpoint of the running
version — so a deploy discards every checkpoint. That is exactly when the
journal is largest. At ~70–90 MB/h on 180 books, one game day reaches 1 GB.

⚠ The measurement is from the dev Mac, which is **2.5× faster than
`n2-standard-2`**. Read 1 m 03 s as roughly **2 m 38 s** on the rig.

⭐ The pinned Python has the identical shape. This is a faithful port of a live
exposure, not a defect the port introduced.

### Two suspension sets shared one name, and the publisher watched the wrong one

`Orchestrator.SuspendedBooks()` returned §6.2's **manual** suspension set under
the name of §6.1's **derived** market state.

Python keeps them apart: `_suspended_securities` is the operator switch, and the
`suspended_books` property is the derived state. The state publisher watches the
second one, to decide when a transition must flush inside one tick.

Wired to the first, the publisher would have flushed on operator switches alone.
It would have stayed **silent** while books suspended for a stale feed, a
disconnected venue, or an invalid reference price — which are the suspensions an
operator most needs to see without waiting.

No fold can see this, because a fold never publishes. AC2 recorded **0 publishes
over 551,939 events**.

The accessor is now `SuspendedSecurities()`, and `SuspendedBooks()` is the
derived set. The checkpoint key never changed, so `make diff` did not move.

### `VenuePriceCap` was wrong by four orders of magnitude, and it could not show

Go carried `1000000.00`. The dictionary says **$127.50**.

**Do not re-panic about this. It is output-neutral on the shipped universe.**
The arithmetic is worth keeping:

```
MEV = ROF + $5.00 × remaining + $2.50 × scheduled
```

Each win moves $5.00 out of `5 × remaining` and into ROF. So `ROF + 5 ×
remaining` is invariant at `5 × scheduled` for an undefeated team, and only
falls from there. Therefore:

```
MEV_max = 7.50 × scheduled_games
```

The composition supplies 17 scheduled games for NFL and 12 for NCAA, giving
**$127.50** and **$90.00**. The cap is exactly `7.50 × 17`. MEV can EQUAL the cap
and can never exceed it, so `min(MEV, cap)` returns the same operand at either
value. `make diff` was byte-identical before and after the fix.

⭐ **It is still worth fixing, because it is a removed guard-rail.** The cap
defends against `games_remaining` or `scheduled_games` arriving wrong from
Edwin's daily feed — the §2.5 gap `reference_price.py` warns about in its own
note. At 1,000,000 that defence was simply absent.

⚠ **Correcting it makes a tie reachable for the first time.** An undefeated NFL
book sits exactly on the cap. CPython's `min` returns its FIRST argument, and
`engine.py` passes the MEV first, so the boundary reaches the caller spelled as
the MEV. Prices compare as strings. The Go comparison was already strictly
less-than and therefore already agreed — proved, not assumed.

### A third of the gate work was making gates see their own plants

Across both streams: **248 defects planted, 247 caught, 1 proven no-op — and 33
gates were BLIND on their first plant.**

| stream | chunk | planted | caught | blind gates |
|---|---|---:|---:|---:|
| taker | taker-core | 80 | 80 | 4 |
| taker | taker-venue | 89 | 89 | 12 |
| taker | taker-state | — | — | 3 |
| taker | ac13 | — | — | 2 |
| venue | ops-surface | 33 | 32 (1 no-op) | 2 |
| venue | anchor reader | 20 | 20 | 5 |
| venue | boot features | 18 | 18 | 4 |
| venue | venue cap | 8 | 8 | 1 |

⭐ **This is the phase's real lesson, and it is the fourth phase running where
this class dominates.** Every blind gate was fixed rather than the plant being
weakened. The shapes worth carrying forward:

- **A gate that passes on a coin toss is not a gate.** A walk-order plant was
  "caught" about half the time, because Go randomises map iteration and a
  two-key map matches sorted order by chance. It is now a deterministic test
  over eight securities and four games, repeated forty times.
- **A correct function that nothing calls.** Every cap test called the ceiling
  helper directly, so deleting the CALL SITE left the function right and
  orphaned, and the whole file passed.
- **A fixture that cannot express the defect.** One checkpoint in a directory
  cannot show a sort order. No game carrying a `result` cannot show a dropped
  `result` field. Notes compared as a set cannot show an order.
- **A missing gate reads exactly like a passing one.** Four of the taker's
  twelve were not weak gates but absent ones — every restart test replayed the
  journal directly instead of booting a runtime, so all four of `Boot`'s jobs
  were uncovered.
- **A test that asserts the defect.** The taker's hand-rolled budget-shed copy
  tested against the wrong bound, and its test asserted that wrong bound.

### The same float trap caught both streams independently

Money crosses the wire as a JSON number. CPython switches to exponent notation
when the decimal point sits at `decpt <= -4`; Go's `strconv` switches on the
DIGIT COUNT. So Python writes `1e-06` where naive Go formatting writes
`0.000001`.

The smallest non-zero money value is exactly `1e-06`, so a single banked
cent-fraction reaches it. Both the maker's `mm.state` and the taker's
`snt.state` hit this. The taker now imports the maker's encoder rather than
keeping a copy, which is what the pinned Python does.

### The taker has THREE JSON spellings, and the spec named one axis of two

|  | sort_keys | separators | ensure_ascii |
|---|---|---|---|
| journal | TRUE | `", "` `": "` | TRUE |
| gateway payloads | false | `", "` `": "` | TRUE |
| state + replies | false | `","` `":"` | TRUE |

⚠ The maker's gateway payloads are COMPACT and the taker's are not. Two
binaries, the same subject, different bytes. The spec named the separators and
did not name `ensure_ascii`; it is amended.

---

## What went wrong / got stuck

- **A design of ours nearly lost AC8's grace clause.** The boot function first
  took a ready-made stack. That is wrong: `build()` is where the acceptor's
  recovery scan reads the WHOLE journal. A composition that built before beating
  would spend the entire grace inside it. It now takes a `Build` function, and
  the ordering is gated. Found by reading our own design, not by a plant.
- **A test we were asked to write could not see its own defect.** The venue-cap
  tie test was requested with a `<=` plant to prove it. At the shipped ROF scale
  both operands render `127.50` and are indistinguishable as strings, so the
  plant SURVIVES. The tie only discriminates at ROF scale 4 and beyond, where
  the MEV renders `127.5000` against the cap's `127.50`.
- **The fsync on the boot log is not provable here.** A plain `write(2)` already
  survives `kill -9`, because the bytes are in the kernel page cache. The drill
  proves what actually broke on the Python side — the lines go to a FILE and not
  to a socket nobody reads — and a second test proves nobody wraps it in a
  buffered writer. The fsync covers HOST death and stays ungated.
- **An intermittent test failure is reported and NOT reproduced.** `taker` saw
  `TestAWedgedTickWithholdsTheBeat` (venue's, from Phase 3) go red during a
  full parallel `make gate`. We found a real ordering dependency by reading —
  closing the wedge channel does not mean a tick is inside it yet — and closed
  it with a signal. ⚠ But 25 isolated `-race` runs and 40 runs at `GOMAXPROCS=1`
  **with the fix removed** all passed, so the reported failure is not
  reproduced and not proven to be this. It must not be recorded as fixed until
  someone catches the failure output.

---

## Decisions made *(mirror into [[market-maker/decisions]])*

- **AC13 is a port gate with NAMED GAPS** (George). Every un-runnable TT/TJ row
  is named individually — row id, what it needs, why this repository cannot
  supply it. A named gap is UNCOVERED: never passed, deferred or waived. The
  list is a TEST rather than a document, so it fails when a claim stops being
  true. The split is 3 covered · 5 partial · 11 uncovered, of 19 rows.
- **The boot SEQUENCE is built in wave 2; the composition stays in wave 3**
  (team-lead, option (a)). AC8 gates this phase, and a gate that cannot be taken
  until wave 3 gets taken under time pressure. ⚠ The cost is recorded: a boot
  sequence built in one wave and a composition in the next.
- **The `ANCHOR_SEED` reader lives in `internal/runtime`, not `internal/events`**
  (team-lead). It folds the prior journal's tail through a throwaway valuation
  engine, and `events → valuation` inverts the dependency. Python's one file is
  already split across two Go packages, because the APPLIER is in
  `internal/valuation`.
- **`sweep_max_interval_s` is 2.0 s** (George, 14-08 — recorded now because two
  vault documents still said 1.0 s). It relaxes the 08-13 value so ordinary
  multi-game engine load cannot walk the portfolio into DEFENSIVE through the
  §3.5 missed-sweep deductions.
- **S1's missing eviction is ported DEFECT INCLUDED** and fixed in Phase 5. It is
  not output-neutral: evicting a game lets the file re-adopt it with
  `from_file=True` and derive LIVE for four hours where the bus rules derive
  OVERNIGHT.

---

## Questions opened / closed *(mirror into [[market-maker/open-questions]])*

**Opened — for George:**

- ⚠⚠ **The boot does not complete inside the 30 s grace on a ≥1 GB journal.**
  1 m 03 s measured on the dev Mac, ~2 m 38 s on the rig. One heartbeat has gone
  out in that window. Faithful to Python. Fixing it is new behaviour, so it
  belongs in Phase 5, not in a zero-diff phase.
- **The pinned reader RAISES against its own "never raises" docstring.**
  `events/anchor_seed.py::_accepted_lines` catches `JSONDecodeError`, `KeyError`
  and `TypeError`. A prior journal line whose `record` is a STRING makes
  `dict(record["record"])` a **ValueError**, which escapes and kills the boot —
  the exact failure the module exists to prevent. Severity: **boot-fatal**. Go
  is lenient, which is what the spec specifies. George to route.

**Opened — for `core`:**

- **`events.FromMap` does not verify the payload hash**, where Python's
  `from_dict` always does. A corrupted or tampered journal line is refused by
  Python's boot and silently trusted by Go's. Both corpora are clean, so gate
  0-b can never see it. ⚠ It runs on every line of a 1 GB journal at boot, so
  the cost must be measured before choosing where the check goes.
- **Go has no Configuration Dictionary.** Python reads every tunable from
  `_CFG`; Go hardcodes package variables. That is how `VenuePriceCap` was wrong
  in one package while three others were right, and why the taker had to inline
  three dictionary values. Second finding with this root cause.

**Closed:**

- **The `ANCHOR_SEED` reader was double-filed** across Phase 2 and Phase 4. Only
  the READER was owed here; the APPLIER was delivered in Phase 2.
- **AC24** — measured against the pinned Python's own journal, all four economic
  numbers exact.

---

## Next

- `core` finishes `deploy`: the composition root, the NATS client, the
  `MM_*`/`SNT_*` surface, the systemd units, and the four items Phase 3 handed
  forward — the real `MarketableGuard`, the NATS subscription bind, the tick
  gate's `GameSource`, and the performance gate on `n2-standard-2`.
- Then the per-phase review, which is what closes Phase 4.
- ⚠ Two things cannot be taken from the dev Mac and must wait for the rig: the
  performance gate, and any re-measurement of the boot grace.
