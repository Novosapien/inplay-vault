# 2026-08-09c — SNT-1's float and sell gate: the taker can trade

> **Type:** build session. Follows the 08-09b handover.
> **Docs touched:** [[market-maker/decisions]] ·
> [[market-maker/market-taker-requirements]] ·
> [[market-maker/parameters]] · [[market-maker/open-questions]]

---

## What we did

Built the two correctness items that stopped SNT-1 running at all —
**T-O07** (the sell bound) and **T-O08** (the seeded float) — on branch
`feat/snt-1-float-and-sell-gate` in `inplay-market-maker`.

- `snt/config.py` — `float_shares` (5,000 default) plus per-team
  overrides.
- `snt/agent.py` — `holding()`, `float_shares()`, `sellable()`; the sell
  gate inside `decide()`, applied after both sizing paths.
- `snt/pending.py` — `live_qty(team, side)`, the `livS` the venue
  subtracts.
- `snt/runtime.py` — passes this book's live sells into every decision;
  the boot print now shows holding, float and drift rather than a bare
  position.

11 new tests. **620 green**, `ruff check` clean, `mypy --strict` clean.
Nothing committed or pushed — George's call.

## What we learned

- **The float has to be configuration, not state.** The obvious build —
  seed `pos` to 5,000 at boot — makes the journal replay double the
  float on every restart. Keeping `pos` as drift and deriving
  `holding = float + pos` costs nothing, changes no journal schema, and
  removes the failure mode entirely.
- **T-O08 was mostly already built and nobody noticed.** The soft cap
  and the disposition tilt both act on `pos`. Once `pos` means drift
  from the float, both already say "return to the float" — which is
  exactly what the requirement asks for. The only real work was the
  baseline itself.
- **The IOC substitute is what makes the sell gate necessary**, not just
  prudent. A marketable DAY order rests up to 1.5 s before its cancel,
  so two arrivals inside that window stack against the same inventory.
  Without `livS` the second one is rejected whole.

## What went wrong / got stuck

- **I started on the wrong machine.** The handover's build queue put the
  stale-book crossing guard (R-Q09) first, and I took it — that is a
  market-maker item. George stopped it: the MM is built; the taker is
  the concern. Reading a queue is not the same as reading which system a
  queue item belongs to.
- **I told George the profit tilt would have to be switched off**, on the
  reasoning that an unknown float cost would make the taker sell itself
  flat. Wrong: the tilt acts on drift, so it mean-reverts to the float
  rather than draining it. Corrected before anything was built on it.
- **The first two attempts to ask George the design questions used the
  question tool and the vault's own vocabulary.** Both were rejected —
  he wanted the mechanism in plain terms, in the chat. The explanation
  that worked led with what the machine does today and what it costs,
  not with the requirement ids.

## Decisions made

→ mirrored into [[market-maker/decisions]] (`2026-08-09b`)

- **SNT-1 participates in the IPO and therefore starts long** (George).
- The float is configuration, not journaled state (ours).
- The sell gate cuts the order down rather than skipping it (ours).
- `livS` counts our own un-settled sells at full quantity (ours).
- The float's cost basis is NOT invented — the tilt keeps its current
  basis until Edwin rules (ours).

## Questions opened

→ mirrored into [[market-maker/open-questions]]

- **E39** — the taker's IPO float: size, cost per share, and the
  publish mechanism. It is **E27's twin on the taker side**; the IPO
  runs on the primary plane, so nothing tells us what SNT-1 was
  allocated.

## Where this leaves the taker

T-O07 and T-O08 are 🟡 — built, never run against a real book. The
important gap is now **T-S05**: the gate computes its bound from our own
arithmetic, so a float that is not verifiably on the account produces a
bound the venue does not share.

## Part two (same session) — the hardening round

George: "standard work, get on with it" — T-S05 carved out as the item
he wants to understand first. Built, same branch, 628 tests green:

- **T-M03** — $25,000/order notional cap, cut-not-skip (our value, E32).
- **T-R01** — journaled kill switch on `snt.control.{bot_id}`; halt
  sweeps the live orders and survives a restart.
- **T-F07's lever** — activity state settable at runtime, journaled,
  reschedules on change. The derivation itself is still unbuilt.
- **Deploy artifacts** — `deploy/snt-1.service`, `snt-1.env.example`,
  `docs/SNT-RUNBOOK.md`. Nothing deployed.

Two findings along the way:

- **The shared-account hole:** the venue's sell check is per-account, so
  the QA posture (taker on the MM account) makes the taker's inventory
  arithmetic wrong in both directions. Recorded in the runbook: QA there
  is a wiring test only.
- **T-S05's input exists:** the gateway publishes `position.{userId}`
  from tag 9383 (found in `oe_adapter.go`). Caveat from 08-09 stands —
  9383 may not be a live position (T15, Rob).

## Next

1. **T-S05 — reconcile position against the venue, halt the book on
   divergence.** George wants to understand it before it is built —
   START BY EXPLAINING IT, plain terms. The input subject is
   `position.{userId}`; the open question is whether 9383 is live
   (T15). Build fail-safe against that unknown.
2. T-F07's real derivation (needs a schedule source — a design choice,
   not wiring).
3. The MM's own half stays open and unqueued: R-Q09 (stale-book crossing
   guard — live and moving money) and R-Q08 (the ask ladder's `Pos −
   livS`).
4. George still owes: keep or drop the MM `requirements.md`; push the
   vault and sportradar branches; SNT-1 into QA on the MM account or
   wait for IPLP (the shared-account hole feeds this decision).
