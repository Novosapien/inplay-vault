---
description: "Discovery for the ops-UI phase 1: live maker/taker view over Centrifugo WSS, engine publishing un-parked, the taker's through-engine manual order ticket"
---

# 2026-08-12 — the observability discovery: the panel matters now

> **Who:** Hasan + Claude (`/discovery` session, started 08-11 evening)
> **Type:** design / discovery
> **Refs:** `specs/2026-08-12-admin-trading-observability/discovery.md` (the
> full record) · [[market-maker/systems/mm-ops-ui]] ·
> [[market-maker/decisions]] 2026-08-12 · N35 opened

## What we did

- Ran the discovery for the admin-panel trading improvements Hasan asked
  for: see the maker's and taker's positions, P&L and books live; a
  market-data page view + a pinned-books sidebar; manual order entry.
- Two research passes grounded it in reality: a survey of the MM repo
  (bus subjects, journals, position/P&L internals, the order path) and a
  survey of `inplay-admin-panel-trading` + its proxy (data path, poll
  intervals, real-time seams, existing order entry).
- Converged, gated, and wrote `discovery.md` + `progress.md` to
  `specs/2026-08-12-admin-trading-observability/`. Updated decisions,
  open-questions (N35), mm-ops-ui.md and the hub row.

## What we learned

- **The engines publish nothing** — deliberate parking, now un-parked.
  The cheap seams: `Orchestrator.state()` is already a JSON-safe full
  snapshot; the taker has `agent.snapshot()`.
- **The proxy is already inside the VPC.** The "it's a proxy outside the
  VPC, redeploy it" theory was refuted: the panel (Vercel) is the outside
  piece; the last two hops poll. Centrifugo is already publicly reachable
  over WSS (the mobile app uses it) — going live is a data-source swap.
- **Unrealized P&L exists nowhere**; realized P&L is per-fill and never
  totalled. The panel derives unrealized at the book mid.
- A manual order on an engine's own userId is adopted and re-priced by
  the engine within ~1 s (the 08-09 observation) — the reason manual
  orders must route THROUGH the taker engine.
- The `viewer` role 403s on `/api/market/book` — a one-line allowlist
  fix, folded into scope.

## What went wrong / got stuck

- Nothing blocking. Both research subagents needed a nudge to deliver
  their reports.

## Decisions made *(mirrored into [[market-maker/decisions]] 2026-08-12)*

- Ops UI home = the admin panel · engine publishing un-parked (`mm.*` /
  `snt.*` full snapshots) · Centrifugo WSS transport, polling fallback ·
  maker strictly read-only · taker manual order ticket (IPO + secondary,
  through-engine, journaled `manual`, taker account only) · P&L mark =
  book mid, taker-prominent · buying power deferred · books live,
  positions slower · no hard date.

## Questions opened / closed *(mirrored into [[market-maker/open-questions]])*

- Opened: **N35** — operator attribution on manual orders (shared-password
  panel auth).
- Closed: the mm-ops-ui "admin panel or desktop shell" open item (20-07).
- Flag, not a question: manual panel trading of the taker account may fall
  under E32/E33/T13 — rides that compliance round.

## Next

- Point `/general-spec-builder` at
  `specs/2026-08-12-admin-trading-observability/` — slice so the engine
  publishers land first; everything else consumes them.
