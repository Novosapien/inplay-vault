# 2026-07-24 (b) — Friday touchdown digest (MM-relevant findings)

> **Who:** George + Claude (digest of the client call: Edwin, Cody, Troy, Kevin + Novo)
> **Type:** meeting digest — [[24-07-2026-touchdown]]
> **Refs:** [[market-maker/decisions]] (24-07 touchdown entry) · [[market-maker/open-questions]] · [[market-maker/plan]] · [[market-maker/systems/mm-ops-ui]]

## What we did

Digested the Friday touchdown (same day as the v1.3 spec intake — see the
sibling note) and routed the MM-relevant findings into the working docs.

## What we learned

- **The probabilities API rides SR's betting-side feed** — faster than the
  media feeds powering the gamecast; the raw betting feeds are sportsbook-only
  and unavailable to InPlay. The MM consumes probability directly, so in-app
  users and the MM see moves at the same moment. S4 (sportsbook parity)
  materially downgraded; Cody lobbying SR for the betting feeds in parallel.
- **Edwin re-affirmed the internal remaining-season model on the call** —
  fresh evidence for E19 (he'll "come up with a piece you can pull"; weekly
  manual input floated), hours after the spec intake proved SR-alone can't
  satisfy D-1. E19 stays open — his words support option (b)/(c).
- **New timeline anchor: trading live for ~Aug 22** (Troy). KYC-less academic
  variant deliberately behind it (~first week of Sept).

## Decisions made *(mirrored into [[market-maker/decisions]])*

Betting-side probability feed fact + fastest-feed ruling (S4 mitigation) ·
MM ops dashboard phased, read-only first, reusing user inventory APIs ·
SR entitlement channel (George's email → SR support + Scott + Cody) ·
NCAA IPO prices in motion (E3) · Aug-22 trading anchor.

## Questions opened / closed *(state in [[market-maker/open-questions]])*

- **Updated:** S4 → 🟡 mitigated · S7 → channel agreed, email owed by George ·
  S2 folded into S7 · E19 + 24-07 call evidence · E3 NCAA → 🟡 in motion.
- **Opened/closed:** none net-new; nothing closed outright.

## Next

1. **George sends the SR entitlement email** (S7): blocked products/versions
   → SR support + Scott + Cody (detail in the session-note sibling + S7 row).
2. Continue the sibling note's build plan (`inplay-market-maker`); draft the
   E17–E19/S6/S7 written blocking questions — E19 now carries the 24-07 call
   quote as context.
3. MM ops UI: phase-1 scope is read-only positions via user APIs — fold into
   Kevin's workshop agenda when it happens.
