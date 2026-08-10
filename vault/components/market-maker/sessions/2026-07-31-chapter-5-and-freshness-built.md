# 2026-07-31 — Chapter 5 built in five pieces · §3.3–§3.5 · the machine quotes

> **Who:** George + Claude
> **Type:** build session, with heavy walkthrough
> **Refs:** `inplay-market-maker` branch `feat/position-engine`, commits
> `fec6a9b` → `cc90735` · [[market-maker/asmm1-adoption-spec]] ·
> spec §5, §3.3–§3.5, §7.5

## What we did

**The machine now quotes end to end.** A Reference Price walks in; a
validated, versioned Target Order Book falls out. **171 → 329 tests**, ruff
and `mypy --strict` clean throughout. Nine commits, both repos committed and
clean for the first time in two sessions.

| Commit | What |
|---|---|
| `fec6a9b` | (Carried from 30-07) the on-field correction + Chapter 4 |
| `fc548a8` | `volatility.py` — σ², the ASMM-1 estimator replacing §5.2's classifier |
| `d6b3e15` | `width.py` — γσ² + C; C derived at import, never a literal |
| `c99a4e2` | `ladder.py` — dollar prices; Suspended is a typed result |
| `923b717` | `quantity.py` — §5.7 with the golden fixture in production at last |
| `3726cd7` | `engine.py` — the cycle: publish-or-hold, sixteen checks, the dwell |
| `74f6d8d` | BUILD-LOG brought current |
| `cc90735` | `freshness.py` (§3.3–§3.5) + MEV + the Invalid gate |

Chapter 5 followed the adoption spec's build order exactly: volatility →
width → ladder → quantities → assembly. Deferred, both externally gated:
§5.5 (needs Ch 8's participant book) and §5.9 (E17).

**Seven explainer artefacts** were built alongside — the volatility number,
the width, the ladder, the assembly, the engine annotated, a vocabulary page,
and the line-by-line code reader. George reviewed every piece in VS Code and
the pages carried the walkthroughs.

## What we learned

- **⭐ The replay result is total.** Two fresh engines fed the same six
  events produce byte-identical books, version chains and §5.10 check
  reports. Every design choice in the chapter — seeded draws,
  version-on-publish, pre-variation comparison, event-time dwell — exists to
  make that one test pass.
- **⭐ Materiality must be judged before the variation.** Final sizes are
  drawn with a fresh quote version, so they always differ; comparing them
  would make every cycle "material" and the book would republish forever.
  The comparison record stores pre-variation sizes and the held shape.
- **⭐ A dead feed reads as CALM.** The price stops moving because the input
  died, σ² falls, and the width equation would quote its tightest into
  exactly the §2.3 danger case. Two defences built: the Invalid gate stops a
  suspect price before it reaches the volatility state, and E31's per-state
  width floors remain the ask for Degraded/Overnight.
- **One principle covers four files: err toward caution, recover slowly.**
  σ² jumps instantly and calms by halves · a new team starts at maximum
  width · trust demotes instantly and climbs one rung per 10 s · rounding
  always moves outward. George's review question ("is the seed
  dimensionally right?") caught the one place the principle was implemented
  sloppily — V₀ = ceil ÷ H, not ceil.
- **The E18 tangle separates into three numbers.** The poll rate (~2 s,
  evidence-backed), the reaction bound (~200 ms, costs nothing), and §3.3's
  freshness bands (break-detectors — SR's 4 s median never trips them).
  Republishing every 200 ms to refresh the randomisation is the thing §5.8
  explicitly forbids, and would cost queue position on every book 5×/second.
  **Refinement question for Edwin filed under E18.**
- **The Ch 6 classifier is off the critical path permanently** — σ² replaced
  its spread-selection job, and its Suspended/kill-switch remnant is small.
- **Nothing computes MEV yet** was found while wiring the ladder — the §5.4
  formula now lives in `reference_price.py`; `games_remaining` rides Edwin's
  daily feed since the engine holds no schedule (known §2.5 gap).

## What went wrong

- **I invented synonyms and George called it out hard.** "Decoration",
  "look", "camouflage" for shape+extra; "photo" for the book record. Each
  invented word cost a round of confusion. Fixed with a vocabulary page
  mapping every loose word to its one code name, and the rule: code names
  only.
- **The changes page showed pseudocode dressed as real code** — a
  `def update(...)` with a compressed fake body. George opened the file,
  found it looked nothing like the page, and said so. Rebuilt the page with
  verbatim code and per-line comments; the repo's own comment convention
  stays as decided 30-07 (a mid-page attempt to add per-line comments to
  `volatility.py` itself was reverted — the *page* teaches, the code keeps
  its Notes-block style).
- **The summary table omitted the test files**, which is exactly what a
  reader browsing the repo notices first.

## Decisions *(mirrored into [[market-maker/decisions]])*

Chapter 5 built per the adoption spec, mechanisms only (every constant 🟡/🔴)
· materiality judged pre-variation on the held shape · Quote Version
increments only on publish · the dwell permits a reshape and never causes
one (N26 implemented) · Invalid status gates before any state is touched ·
cold-start σ² at the ceiling (→ E31, Edwin's call) · promotions climb one
rung per dwell · the odd-tick side is a stateless seeded 50/50 rather than
strict alternation (ours, tagged) · MEV computed in valuation.

## Questions

- **Opened:** **E18 refinement** — is 200 ms a reaction bound, or does Edwin
  want the book visibly moving with no new information? (His RPV-2 instinct
  suggests he might; §5.8 as written forbids it.) · **E31 addition** — the
  cold-start seed (wide-when-ignorant) is book-visible, his sign-off.
- **Closed:** **N26** — the dwell gate is built exactly as filed: §5.8's
  thresholds remain the only publish trigger; an expired dwell only lets a
  real publish carry a fresh shape.
- **Unchanged and still the risk:** E27 (nothing publishes the opening
  position), E25 (the deadline), E17 (now §5.9's only blocker).

## Next

1. **Chapter 8 — venue sync + orchestration.** The last big build: consume
   the gateway's NATS streams, target-vs-confirmed reconciliation, the
   heartbeat (N15), and the wiring that runs event → Ch 3 → Ch 4 → Ch 5 in
   production rather than in tests.
2. **The poller** — buildable against replay now; live use gated on S1/S7.
3. **Ch 12 config sweep** — mechanical; the `CONFIGURED` markers are ready.
4. Send the question round to Edwin: E29–E35 + the E18 refinement.
