---
description: "The Go port discovery session: scope ruled to maker plus taker, the acceptance bar set, and five port hazards the 04-08 list does not carry"
---

# 2026-08-18 — the Go port discovery

> **Who:** Claude (`/discovery`) + George
> **Type:** design
> **Refs:** `specs/2026-08-18-mm-go-port/` (discovery.md · progress.md) ·
> `specs/2026-08-17-mm-pre-port-close/GO-PORT-HANDOVER.md` ·
> `w3-drain-verdict.md` · [[market-maker/decisions]]

## What we did

Opened the Go port discovery that the 14-08c ruling put after the pin. Read
the mandatory order, every `build/` page, and the pre-port close's own
handover. Ran five parallel research streams — the decisions log, the
open-questions/parameters/requirements/test-plan set, every recorded
performance measurement, an interface-level map of `src/mm` + `src/snt`
against `origin/main`, and web research on Python→Go behavioural
differences.

George ruled scope and timing. The discovery document and its spec folder
are written and READY for spec-building.

## What we learned

### W3 landed mid-session, and it is the answer the port rested on

The residual venue-drain cost is **work, not an algorithm**. Halving the
portfolio (170 → 85 books) **raised** per-ack cost (0.6980 → 0.8114
ms/ack) and left the composition untouched (`_drive_cycles` 58.3% vs
58.5%, `sync.stage` 0.2% vs 0.2%). An O(portfolio) scan would have done
the opposite on both counts.

⭐ **This is what makes the port worth doing rather than a translation of
a wall.** An algorithmic scan would be inherited: same shape, faster
language, same limit at NCAA scale. Work-bound cost converts directly into
headroom.

### Five hazards the 04-08 list does not carry

The 04-08 entry records four (decimal arithmetic, canonical JSON, map
iteration order, seeded randomness). Reading the real code against the
research found five more, all load-bearing:

1. **Decimal transcendentals are on the hot path.** `Decimal.exp()` at
   `volatility.py:101` runs per reading per book; `.ln()` at
   `volatility.py:49` and `width.py:48` are import-time constants;
   `Decimal.__pow__` at `quantity.py:61` runs per level. **No Go decimal
   library guarantees correctly-rounded `exp`/`ln`** — CPython's libmpdec
   does. Freezing the two constants as literals removes half the problem.
2. **Amdahl inverts CB4's "there is no Decimal problem."** That measured
   under 5% of the ack path **in Python**. In Go everything else gets
   10–50× faster while decimal gets 2–5×, so decimal's share rises sharply
   and becomes the likely new bottleneck. The library choice is
   simultaneously the correctness and the performance risk.
3. **The forked checkpoint writer has no Go equivalent.**
   `checkpoint.py:90-137` double-forks and captures from the COW image —
   it exists because the synchronous form reached 344 MB ≈ 22 s and the
   dead-man swept the book hourly. Go cannot fork-and-continue. This is a
   design decision, not a translation, and it constrains how engine state
   is represented everywhere.
4. **Go's `select` picks uniformly at random** among ready cases. Spec'd
   behaviour, so `-race` never flags it, and it passes most runs — the
   worst failure mode for a differential-replay certification.
5. **Timestamps.** Go's `RFC3339Nano` trims trailing zeros where Python's
   `isoformat(timespec="milliseconds")` is fixed-width — and the journal
   carries **mixed** precision deliberately (3 dp runtime-minted, 6 dp
   gateway-sourced). A port must preserve each producer's own spelling,
   never normalise.

### Hazard 4 is safer than recorded, and collapses into hazard 1

The 04-08 entry marks seeded randomness "already safe — SHA-256, not a
language PRNG". Reading `quotes/variation.py` confirms something stronger:
there is **no PRNG at all**. It is SHA-256 → first 8 bytes big-endian →
u64 → `Decimal(h) / (2^64 − 1)` → `0.75 + 0.50 × U`. Exact cross-language
parity is required and achievable.

⚠ But that final division runs in Python's default 28-digit
`ROUND_HALF_EVEN` context, so **hazard 4 is a special case of hazard 1**.
The web research assumed a digest-seeded PRNG and concluded parity was
unachievable; the code refutes it.

### The certification corpus is already committed

A Go binary that reads `journal.jsonl`, folds it, and emits
`canonical(orchestrator.state())` can be diffed against
`scripts/a2-run/state-live.json` **on day one** — before any NATS, any
gateway, any clock. That is the port's first gate and it needs nothing
built.

### Byte-equality through the venue is already a non-invariant

`stand_the_book` is un-journalled, and admitted orders carry the gateway's
price string — `"77.6"` ≠ `"77.60"` canonically. R9's claim is
deliberately narrow: core **byte**-identical, settled venue book
**value**-identical. The port's bar must adopt the same split, and the
test plan already names this as the likeliest place a port silently
diverges.

### Small correction

`build/event-core.md` and `build/runtime.md` say checkpoint schema 5.
`events/checkpoint.py:35` is **`SCHEMA_VERSION = "7"`**.

## What went wrong / got stuck

- **Nothing blocked.** One hour of research effort was spent on a
  Python→Go randomness question that the code answered in a minute —
  reality-grounding should have come before the web research on that
  point, not after.
- The vault's own staleness bit again as a reading hazard: `build/next.md`
  still described the port as "parked … decision parked at season-2/NCAA",
  which George's 18-08 ruling supersedes. Corrected in this session.

## Decisions made *(mirrored into [[market-maker/decisions]])*

1. ✅ **George, 18-08: the port covers the maker AND the taker** (`src/mm`
   + `src/snt`). The SR publisher stays Python; the Go FIX gateway is
   untouched.
2. ✅ **George, 18-08: start now.** The port is no longer parked at
   season-2/NCAA.
3. ✅ **George, 18-08: Python keeps moving until he gives the go-ahead**,
   then the deep scan-and-map runs at spec stage. The port targets the
   commit he names, never a moving tip.
4. 🟡 **Adopted by default, open for George:** the acceptance bar
   (≤0.286 ms/ack p90 on six-game-v2 at the production VM shape, zero
   missed sweeps, byte-identical differential replay); shadow-then-cutover
   under R11; a serial deterministic loop first, parallelised only after
   equality is certified.
5. ✅ **The taker's deliberately weaker determinism contract is ported,
   not "fixed" into uniformity.**
6. ✎ **REVISED late in the session, via `GO-BUILD-SCOPE.md`: the Python
   engine is a REFERENCE IMPLEMENTATION, not a product under
   maintenance.** We have not launched and the maker works, so **nothing
   new goes into Python and no fixes go back to it** — the only exception
   is anything that stops it running as a comparison target. **Everything
   unbuilt is Go's**: N40 (the game-end lifecycle, the biggest open
   item), N34 (maker shorts), N43 rider 3 (the ask cap's `[post-first]`
   ordering — *"never resolved in Python — it is a GO design decision
   now"*), and the NCAA-scale scan work. This supersedes the session's
   own first reading ("reproduce the gaps, do not fix them").

## Questions opened / closed *(mirrored into [[market-maker/open-questions]])*

- **NEW — repo layout for the Go implementation.** New repo vs a `go/`
  tree in `inplay-market-maker`. Recommendation: a new repo plus a shared
  `inplay-fix-contracts` Go module, because the Python MM currently
  mirrors the gateway's structs **by hand** and that drift risk is real.
- **NEW — the checkpoint writer's Go design** (see hazard 3). Blocking on
  the state representation, so it belongs in Phase 0.
- **NEW — the decimal library choice**, benchmarked before commitment.
  `cockroachdb/apd/v3` is the leading candidate; the Go gateway offers no
  precedent (it has no decimal library in direct use).
- **NEW — `specs/` has no git remote.** The handover and this discovery do
  not resolve from any other machine. Recommend copying both into the
  vault.
- 🔴 **N43 rider 3 (`[post-first]` ordering)** stays open and the port
  inherits whatever state it is in at the pin.

### Three taker invariants a rewrite would tidy away

Now that the taker is confirmed in scope, these are the ones most likely
to be "improved" into defects:

1. ⭐ **The taker must NEVER publish a heartbeat on the MM namespace.**
   The gateway's dead-man is **one global latch keyed to the engine's
   beat** — a second heartbeater would feed the latch while the *engine*
   was dead, masking the exact failure the dead-man exists to catch
   (decisions 10-08c). It shares the transport and never the subject.
2. **Its journal format differs deliberately** — `sort_keys=True` with
   **default separators** (spaces), `flush()` but no `fsync` (N38). No
   envelope, no idempotency key, no acceptor, no sequence, no
   checkpoints. Not to be unified with the maker's.
3. **It is genuinely stochastic** (`random.Random`, injected) where the
   maker has no randomness at all outside the seeded SHA-256 framework —
   and its draws are deliberately not persisted, because replay
   reproduces fills, not draws. So the taker sits **outside** the
   cross-language draw-parity requirement.

### The tension the revised scope creates, and how it resolves

⭐ **"Everything unbuilt is yours" and "certified by differential replay"
cannot run at the same time.** Differential replay can only certify
behaviour Python also has. A Go engine that ports the venue leg *and*
changes the `[post-first]` ordering *and* adds a journalled game-final
event has nothing to compare against — a non-zero diff no longer
separates "I mistranslated the ladder" from "I deliberately changed the
lifecycle", and the claim collapses for both.

The phase boundary is the resolution: **Phases 0–4 are the faithful port
and every diff must be ZERO; Phase 5+ carries the new builds behind their
own flags and their own gates.** `GO-BUILD-SCOPE.md` already sequences it
correctly; the reasoning is written into `discovery.md` §9.15 so a
spec-builder does not "optimise" the order. The named failure mode: finding
N43 rider 3's defect in Phase 1, fixing it there because it feels
efficient, and destroying the Phase 1 proof.

## Next

George: merge #52/#54/#56, emit `MM-PYTHON-FIX-SET-COMPLETE`, pin the
gospel commit, then give the go-ahead. On that go-ahead the next session
runs the deep scan-and-map of `src/mm` + `src/snt` at the pinned commit
and invokes `/general-spec-builder` against
`specs/2026-08-18-mm-go-port/`.

Phase 0 work — the decimal benchmark and the checkpoint-writer design —
can start **before** the pin: both depend only on committed, immutable
artefacts.
