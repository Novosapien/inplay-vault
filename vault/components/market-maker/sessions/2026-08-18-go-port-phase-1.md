---
description: "Closing Phase 1 of the Go port: the transport ported byte for byte, three wire divergences that behave identically, and a Python stop() that hangs for ever"
---

# 2026-08-18 — the Go port, Phase 1 complete

> **Who:** Claude (`/general-implementation-builder`) + George
> **Type:** build
> **Refs:** `specs/2026-08-18-mm-go-port/` · Go repo PRs #10, #11 ·
> [[market-maker/build/venue]] ·
> [[market-maker/sessions/2026-08-18-go-port-reconciler]]

## What we did

Ported `venue/transport.py` and `venue/nats_transport.py` — the five gateway
subjects, the payload builders, `MMIdentity`, the heartbeat and kill switch,
and the **one-queue-one-writer FIFO** that post-first depends on. Then ran the
per-phase review, which found one real thing.

**Phase 1 is complete.** Its gate holds:

| floor | asked | delivered |
|---|---|---|
| seeds | ≥3 | **4** |
| order lifecycles / seed | ≥200 | **304–312** |
| events / seed | ≥400 | **445–469** |

`canonical(state())` compared at every step, plus every read's result, the
diff's instructions, the healer's verdicts and reason strings, and the exact
wire bytes. **25 planted defects, all caught.**

## What we learned

### ⭐ Three byte-level divergences on the wire — all of which BEHAVE IDENTICALLY

The fuzz now compares the exact bytes each instruction would put on NATS. It
caught three differences that no functional test could see, because the gateway
parses all six forms the same way:

| | Python | Go's default |
|---|---|---|
| an integral price | `"price":100.0` | `"price":100` |
| key order | **insertion** order | **sorted** |
| non-ASCII | `"acct-é"` | raw UTF-8, and `<`, `>`, `&` escaped |

⚠⚠ **The third one is the sharp one. The WIRE uses `ensure_ascii=True` and the
JOURNAL uses `ensure_ascii=False`.** Same library, two call sites, two
spellings — so the wire cannot reuse the canonical encoder, and Go's
`encoding/json` matches **neither**.

⚠ The venue account, the bot id and the user id all reach the wire as strings
and all come from the **environment**, so a non-ASCII or angle-bracketed value
is a deployment away, not a theory.

### ⚠⚠ Python's `stop()` HANGS FOR EVER after the writer dies

`flush()` is `asyncio.Queue.join()`, which waits for one `task_done()` per item.
When the writer task dies mid-queue the remaining items **never get one**, so
`join()` — and therefore `stop()` — never returns.

Confirmed by running it against the pinned interpreter rather than reasoning
about it:

```
⚠ join() HANGS after the writer dies — stop() would never return
```

The Go version returns the writer's death reason with the unsent count instead.
A hang is strictly worse than an error, it is a liveness bug rather than
behaviour the port must reproduce, and nothing about it is observable in
canonical state. **This is a deliberate, recorded divergence — and the Python
maker still has the defect.**

### ⚠ The phase gate did not meet its OWN written floor

The spec asks for ≥3 seeds × ≥200 lifecycles × **≥400 events**. The fuzz was
driving 4 seeds and ~310 lifecycles — and only **~328 events** per seed, because
only about 41% of steps are events; the rest are registrations, reads,
reconciles and heals.

It looked like a comfortable pass and was a miss on one of the three numbers.
Found by the per-phase review, which is exactly what that review is for.

⭐ **All three floors are now ASSERTIONS in the generator**, which refuses a seed
that misses any of them. A floor written into a spec and never turned into a
check is not a floor.

### The running count

Six times in this phase the random fuzz could not reach a defect the vault
already recorded — the twin-price spelling, the in-flight replace's
destination (**the 08-08 defect, 19 doubled levels live**), a suppressed cancel
target, a suppressed price, `cancel_everything`'s backoff, and the integral
price. Each was found by planting the defect and watching the fuzz pass.

## Decisions made *(mirror into [[market-maker/decisions]])*

1. **The wire's string escaping is not the journal's**, so the two encoders stay
   separate and neither may be used for the other's job.
2. **Go returns an error where Python hangs** on `stop()` after a dead writer.
   Recorded as a deliberate divergence and as a live Python defect.
3. **Every floor in a gate becomes an assertion**, not a number in prose.

## Next

- **Phase 2 — valuation, position, quoting, market state.** Four chunks, and the
  first that touch the numeric engines rather than the venue leg. That is where
  `internal/decimal`'s guard-digit work gets exercised in anger, and where the
  decay cache (a requirement, not an optimisation) is built.
- ⚠ Before porting each engine, ask what it walks and how often. Three instances
  of CB4's scan shape have been found so far, the third only at rig scale.
