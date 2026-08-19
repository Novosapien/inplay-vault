---
description: "Go port Phase 3 closes — N52 and N48 ruled, gate 0-b passes 18/18 on both corpora, the runtime chunk built, and the quotes divergence turns out to be the harness"
---

# 2026-08-19e — Go port: Phase 3 closes, and gate 0-b passes

> **Component:** [[market-maker/market-maker]] · Previous: `2026-08-19-d-go-port-phase-3.md`

## What we did

**Two rulings taken from George**, both of which had been blocking:

- **N52** — rebuild the a2 corpus on one timeline, at 120× pacing.
- **N48** — ship each closed run directory to a bucket at rotation.

**Both Phase-3 blockers closed, and neither was a defect in the ported engine.**

1. **N52's rebuild.** `testdata/generators/a2_corpus_rebuild.py` builds a
   one-game workload from the real Chiefs-Ravens capture and drives it through
   `six_game_workload.run_profile` — whose `feed_game` already rewrites every
   stamp onto the run's own clock, which is exactly why the six-game corpus
   never had the gap. The rebuilt corpus spans **212.6 s** instead of
   60,871,126 s.

2. **The `quotes` σ²/width divergence was the harness.** See below — it is the
   session's real finding.

3. ⭐ **Gate 0-b PASSES** — all eighteen subtrees byte-identical on BOTH
   corpora, plus the AC11 determinism stress at GOMAXPROCS 1, 2 and 8.

4. **The whole `runtime` chunk built**: the single-engine lock (AC12), the sweep
   scheduler, the session clock, the sync driver and converger, the tick, and
   the run loop with its progress-aware beat and converger task.

5. **AC23b measured for the first time — 82.39%** on the venue-bearing arm,
   against a ≥80% bar.

6. **N48 built**, and **Phase 3's per-phase review run** — six findings, all
   fixed in-phase.

## What we learned

⭐ **The `quotes` divergence was the config version, and it cost a whole chunk.**
The six-game reference is Python's fold under `GO-REFERENCE`;
`go_reference_checkpoint.py` folds under its own `REPLAY_CONFIG_VERSION`, which
is **not** the version the run that wrote the journal used. The journal's
records say `CB11787049727`, and that is what the harness was passing.

The version **salts every §5.7.3 draw**, so a fold under the wrong one
reproduces every price that does not depend on a draw and gets every drawn one
wrong. Thirteen subtrees byte-identical and `quotes` off by a tick — *nearly
correct*, which is why it survived as a suspected σ² bug.

⚠ **`testdata/README.md` already said `GO-REFERENCE` in as many words, and the
flag's own help text already warned about exactly this failure mode.** Neither
prevented it. **A setting that is part of a certification target must be
ENFORCED against that target's manifest, not documented beside it.** Logged as
[[market-maker/go-port-findings|GP-13]].

⭐ **R13's decay cache does not exist in Python at all.** `grep -rn
'DecayCache|decay_cache'` over `src/`, `scripts/` and `tests/` at the pin
returns nothing. It is one of the port's deliberate Go-side additions — which
is precisely why AC23a (byte-identical with the cache ON and OFF) is the
stricter of the two acceptance criteria: the cache may exist only because it
cannot be observed.

⚠ **The LIMIT behind N52 is not closed, only the condition.** apd still stops at
±100000. The operational fact: **a security whose Reference Price goes quiet for
76.9 days leaves apd's range.** That is far outside any real session — but
*"we never go quiet that long"* is the REASON it is safe, and the reason now
lives beside the limit in four tests that compute the budget rather than assert
it.

⚠ **Three documents give three different values for `sweep_max_interval_s`.**
The dictionary ships 0.5 / 2.0; `loop.py`'s own comments say 2.0 / 2.5 and carry
the **✅ marker**; `build/runtime.md` records 1.0, George's 08-13 ruling, and
never picked up his 14-08 relaxation. Logged as GP-14.

## What went wrong / got stuck

⚠⚠ **Seventeen gates across this phase could not see their own planted defect.**
104 plants, all eventually caught — but seventeen only after the gate was fixed.
The ones from this session:

- the lock's stamp-order test refused from the SAME process, so the pid written
  was identical under either order;
- an `open` firing inside the closed window was unreachable, because every arm
  reached 23:59 with the day's open already fired;
- the converger's LIVE rotation is invisible when every live book refuses;
- `[register-then-send]` is invisible at the end of a step — the transport now
  reads the venue state WHERE THE GATEWAY WOULD, per message;
- the cancels-through arm produced no cancels at all until the orders were
  acked, because `_ACTIONABLE` is `{ACTIVE, PARTIALLY_FILLED}`;
- staging-while-closed is invisible in the TickReport;
- the session close's `clear()` had nothing to clear at the shipped budget;
- the no-drift test counted ticks with no deadline;
- the progress anchor's order is invisible from a cold start;
- **and one test was written as a `t.Skip`** — the dead-converger arm. It is
  real now.

⚠ **The tick's differential script was not reproducible at first.** The
generator replaced the runtime's clock but the composition's ACCEPTOR kept the
wall one, and `accepted_time` reaches the acceptor's state — so two generations
produced two different scripts. Found by generating twice and diffing, which is
now the check.

⚠ **A real defect the tick gate caught on its third step:** the converge budget
defaulted to Go's zero value where the dictionary says 128. Zero is a *legal*
budget meaning "send nothing", so the runtime staged every book perfectly and
never sent a single order. A fold does not converge, so gate 0-b is blind to it
— it took a gate over the LOOP to see it.

⚠ **AC21's wildcard rule is unobservable on the shipped universe.** All 170
symbols are dot-free, so `market.book.*` works perfectly today and would fail
the first time a `.TEST` twin appears. Any test drawn from the live universe
would have passed against the defect. Now pinned with a dotted symbol supplied
on purpose.

## Decisions made

→ mirrored into [[market-maker/decisions]] as **2026-08-19e**.

## Questions opened/closed

- **N52 — CLOSED.** George ruled the rebuild, and took the 120× pacing against
  a measured recommendation. → [[market-maker/open-questions]]
- **N48 — RULED and BUILT.** Option (1), with the one-hour window accepted.
- **GP-13 and GP-14 — NEW**, both ours, both in
  [[market-maker/go-port-findings]].
- **N47** — untouched. Still needs Edwin's number.

## Next

**Phase 4 — and it is where the team spawns**, by the spec's own design.
Four chunks: `ops-surface`, `boot-features`, `taker-core` + `taker-venue`, and
`deploy`.

⚠ **Four things Phase 3 recorded as OWED rather than closed, all Phase 4's, and
all named in `reviews/phase-3-review.md` rather than left to be discovered:**

1. **Nothing constructs a real `MarketableGuard`.** The converger's behaviour on
   a refusal is gated and the guard's verdict is gated, but no code builds one —
   that is the composition's job. ⚠ Both committed corpora were generated with
   the guard BLIND (`MARKETABLE_GUARD_BLIND` — 20 consultations, 0 book
   messages, 0 opinions), so their agreement says nothing about it either.
2. **Nothing binds the NATS subscription**, so AC20/AC21 are half-closed.
3. **The tick gate does not compare the poll stage or `discovered`** — no
   `GameSource` on either side, so both report zero and agree about nothing.
4. **Phase 3's performance gate is not taken.** It needs `n2-standard-2` and
   adjacent arms; the dev Mac runs 2.5× fast.

Also owed, and cheap: the GP-14 documentation fixes — delete the numbers from
`loop.py`'s comments, update `build/runtime.md` with the 14-08 ruling, and
retire `parameters.md` row 35 in favour of row 223. None of it touches
behaviour, so none of it is blocked by the zero-diff mandate.
