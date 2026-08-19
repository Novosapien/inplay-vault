# 2026-08-01b — the poller: one worker, three publications

> **Who:** George + Claude (same day, second stretch — continuation of the
> Chapter 8 session)
> **Type:** build session, autonomous integration mode
> **Refs:** `inplay-market-maker` commits `73b1878` + docs · N16 · E18 ·
> Sportradar OpenAPI via the SR MCP server

## What we did

**The poller is built — N16's ruling made real.** One worker, three
publications: probabilities, official results, and the gateway heartbeat.
**385 → 392 tests**, ruff and `mypy --strict` clean. George deferred the
loopback wire test (noted in the 01-08 session note's Next list) and
confirmed the poller as the next build.

- `mm/poller/source.py` — the seam: a one-method `GameSource` Protocol.
  `FileSource` replays captured games today; the live HTTP source arrives
  with S1/S7 and must parse with `parse_float=str`.
- `mm/poller/worker.py` — the tick: heartbeat first (always, even idle —
  the gateway's dead-man is counting), then each due game's whole timeline
  through the orchestrator, then final detection → `OFFICIAL_RESULT` at
  result version 1, outcome from the score, ties included.

## What we learned

- **The poller needs no memory.** SR returns the whole timeline every
  poll; the acceptor's §7.3 idempotency is the single answer to "what is
  new", and it recovers from the journal — so a killed and restarted
  poller re-polls the same game and double-processes nothing. Proven by
  test.
- **Validated against Sportradar's OpenAPI specs** (George's ask, via the
  SR MCP): the **v1 Probabilities product** — the one our capture came
  from and the trial key serves — matches our parser **exactly** (flat
  timeline entries, status/scores at top level). ⚠ The **v2 GAF product**
  (the S7-gated ask) **nests timeline entries under a `market` key** and
  reshapes the status object — switching products under S7 is a
  one-function adapter change, not free. Do not switch silently.
- SR publishes **no enum for `status`**: `ended` is real (our capture),
  `closed` is SR's confirmed-final convention — both treated as final.
  Cancelled/postponed games read as not-final and keep polling, which is
  harmless; what a cancelled game does to the PRICE is an InPlay question
  no document answers.

## What went wrong

- The restart test caught a report-accounting gap (a re-offered final was
  not counted as a duplicate) — fixed before commit. Nothing structural.

## Decisions *(engineering, recorded in BUILD-LOG)*

Poller holds no seen-state (the acceptor is the memory) · heartbeat before
polling on every tick · injected clock schedules and never touches an
event · official results publish at result version 1, corrections would be
version 2 · poll cadence ~2 s per game (E18's evidence-backed rate).

## Questions

- **Closed:** **N16** — built as filed; the poller owns official results.
- **No new questions.** The v2-product shape caveat rides S7's existing row.

## Next

1. **Fix-pass step 5** — rejection audit records (§7.2 at the door).
2. **Ch 12 config sweep** — the `CONFIGURED` markers are all placed.
3. **The NATS adapter + loopback wire test** (deferred by George 01-08) —
   before any live attempt.
4. Send the Edwin round: E29–E36 + the E18 refinement.
