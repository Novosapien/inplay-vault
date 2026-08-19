---
description: "The operator cockpit for the maker and taker — lives in the trading admin panel; phase-1 observability discovered 12-08, parameters and supervision later"
---

# MM Ops UI

> **Component:** [[market-maker/market-maker]]
> **Status:** ⭐ **Phase 1 discovered 12-08** — read-only observability + the
> taker's manual order ticket, specced in
> `specs/2026-08-12-admin-trading-observability/discovery.md`. Later phases
> (parameters, supervision) still sequenced after the backend.
> **Operator:** Kevin Murray (likely) · Edwin (manual IPO buying)
> **One-liner:** The operator cockpit for running the house agents: watch positions, P&L and the books live, place manual taker orders; algo parameters and supervision flags come later.

---

## What It Is

A **desktop version of the challenge app**, built for the market maker before
any user-facing desktop rollout. Troy: the MM is "any other participant in the
trading challenge… with far more capabilities" — so the UI is the existing app
surface plus a handful of operator components, not a separate product.
(Source: standup 2026-07-20)

Brett's warning on expectations: the first cut will be rough.

## Requirements (from the 20-07 discussion)

1. **Set / modify algo parameters** — the tunables in
   [[market-maker/parameters]]: spreads, sensitivities, session profiles,
   randomization bounds. Changes take effect next decision cycle, logged.
2. **Order lookup / moderation** — see the MM's resting quotes per team,
   cancel/adjust manually if needed.
3. **Positions & P&L** — per-team inventory (as % of float), realized/
   unrealized P&L, same functions users get plus operator depth.
4. **Supervision surface** — out-of-band execution flags, halt/resume
   controls, bust workflow (see
   [[market-maker/systems/market-supervision]]).
5. **Health** — feed status (Sport Radar, tZERO session), valuation freshness,
   cycle rate per team.

## Phasing (from the 24-07 touchdown)

Edwin's ask sharpened the sequencing into phases — he wants **someone from
InPlay monitoring a dashboard of the market** as launch nears, "running it as
close to production as possible":

1. **Read-only visibility first** — is the MM working, seen from the backend:
   per-team positions/holdings ("how many shares it owns of PMX Y"), the data
   stored and representable; variables visible but **static**.
2. **Then changeable variables** for an active trade — later phase.

Explicitly not about changing the MM's logic. George: the MM is effectively
another user, so **the same APIs that show a user their inventory serve the
dashboard** — no separate data path for phase 1. (Source: standup 2026-07-24)

## Sequencing

Deliberately last: it needs the backend stack (valuation → state → quoting →
supervision) to exist before there's anything to operate. The admin dashboard
is desktop-built already, but no desktop version of the challenge app exists
yet — the MM ops build is the excuse to start one, MM-first, not rolled out to
users right away. (Source: standup 2026-07-20)

## Phase 1 discovered (12-08)

The observability discovery (`specs/2026-08-12-admin-trading-observability/`)
pinned phase 1 and made the home decision:

- ✅ **It lives in the trading admin panel** (`inplay-admin-panel-trading`),
  not the desktop app shell — the 20-07 open item is closed.
- Scope: live maker+taker view (positions, avg cost, realized/unrealized
  P&L at the book mid, resting quotes, health strip), market-data page
  view + a pinned-books sidebar, and ONE control — the taker's manual
  order ticket (through-engine, journaled `manual`; maker hard-excluded).
- Transport: Centrifugo WSS to the browser; both engines gain state
  publishers (`mm.*` / `snt.*`) — the parked "what the engine publishes"
  decision is un-parked (decisions 2026-08-12).
- Deferred: buying power, parameters, supervision surface, kill switch.

### ⭐ The engine half is BUILT (12-08b)

Branch `feat/state-publishers-manual-orders`, 767 tests green, **not
deployed**. What now exists on the engine side, i.e. what the panel can
be built against:

- **`mm.state`** — a complete projection every ~1 s, plus a flush within
  one tick of a kill switch / quarantine / suspension. Details and the
  shed contract: [[market-maker/build/venue]].
- **`snt.state.snt-1`** — the same cadence from the taker's own task,
  **including while halted**, with the new `avg_cost` /
  `realized_pnl_total` meter and `open_orders[]`:
  [[market-maker/systems/snt-1-noise-taker]].
- **The manual order family** on `snt.control.snt-1`, replying on
  `snt.control.snt-1.reply.{ref}`. Guards are engine-enforced and the
  panel **mirrors them from `snt.state.guards`** — never hardcode 10,000
  / ±20% / $500k, because they are env-tunable on the VM.
- Measured: the `mm.state` payload is 208 KB at 170 books, inside the
  256 KB budget.

One thing the panel must design around and one that gates any live
drill: **N36 is RESOLVED** — the taker publishes BOTH activity states
(bot-level = the operator's setting; per book = the engine's derived
state) and R9 renders them in different places, never merged into one
badge — and the ⛔ **NATS grants** — see
[[market-maker/decisions]] 2026-08-12b. Full narrative:
[[market-maker/sessions/2026-08-12-b-engine-state-publishers-manual-orders]].

## Open Items

Tracked in [[market-maker/open-questions]]: scope beyond phase 1,
parameter-change permissions/audit, **N35 — operator attribution on manual
orders** (panel auth is shared passwords), ~~N36 — the taker's published activity state is bot-level~~ (resolved
12-08b: both levels published), Kevin's workflow requirements
(needs its own mini-workshop — flagged 20-07).
