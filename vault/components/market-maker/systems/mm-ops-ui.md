# MM Ops UI

> **Component:** [[market-maker/market-maker]]
> **Status:** Deliberately last in the build order — "comes at the end when the backend is done" (Troy)
> **Operator:** Kevin Murray (likely)
> **One-liner:** The desktop cockpit for running the market maker: set algo parameters, look up orders, watch positions and P&L, and act on supervision flags.

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

## Sequencing

Deliberately last: it needs the backend stack (valuation → state → quoting →
supervision) to exist before there's anything to operate. The admin dashboard
is desktop-built already, but no desktop version of the challenge app exists
yet — the MM ops build is the excuse to start one, MM-first, not rolled out to
users right away. (Source: standup 2026-07-20)

## Open Items

Tracked in [[market-maker/open-questions]]: scope beyond the basics, whether
it lives in the admin panel or the desktop app shell, parameter-change
permissions/audit, Kevin's workflow requirements (needs its own mini-workshop
— flagged 20-07).
