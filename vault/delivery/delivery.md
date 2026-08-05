---
description: "Delivery hub for the InPlay app flight plan — the Novosapien/InPlay working agreement — with committed snapshots, structure conventions and key launch dates"
---

# Delivery · InPlay App Flight Plan

> **Status:** Living · updated per working session
> **Owner:** Novosapien (product owner: Brett StClair)
> **Live copy:** `shared/inplay/inplay-app-flight-plan/{date}/inplay-app-flight-plan.html` (updated in place during a day; a new dated folder per session)
> **Master:** `Programming/inplay/inplay-app-flight-plan/` (source + build script)

The flight plan is the delivery working agreement between Novosapien and InPlay: what has shipped, what is committed, what capacity exists, and the live risks into each launch. It is produced with the `/novosapien-product-owner` skill from three reconciled sources: the build repositories, the partnership proposal, and this vault. This section holds the committed snapshots; each weekly review runs off the newest one.

## Snapshots

| Date | File | Headline state |
|------|------|----------------|
| 2026-08-05 | [flight-plans/2026-08-05-inplay-app-flight-plan.html](flight-plans/2026-08-05-inplay-app-flight-plan.html) | 17 days to the NCAA IPO; launch mode active; trading path is the long pole |

## How the plan is structured (stable conventions)

- **Home:** two-month flight-plan diagram + quarterly release plan + people.
- **Key Releases:** frozen build definition for the launch, ordered must-land list, a **live ranked risk register** (re-scored weekly, never a fixed template), decisions needed from InPlay with deadlines, and the rule that anything "explicitly not in this build" must name its landing slot in a later stage.
- **Next 8 Weeks:** week-by-week deliverables to the key dates, fading to monthly.
- **Quarter pages (4):** identical frame every quarter and band: P1 7 slots and P2 7 slots, each 3 large + 2 medium + 2 small; open slots shown inline; P3 planned-to-drop; a faded **P4 horizon** band (other sports back-plans, the FINRA live-production track).
- **Module Ledger:** all components reconciled repo-vs-proposal-vs-vault, with a soft origin column.

## Key dates it currently tracks

- 19 Aug: NCAA price freeze · 22 Aug: **NCAA IPO opens** · 26 to 27 Aug: NCAA secondary + market maker quoting (E25 pending) · 5 to 6 Sep: NFL IPO · 7 Sep: NFL secondary · ~10 Sep: season kickoff · ~13 Jan 27: season close and settlement.

Related: [[components]] · [[architecture]] · [[whats-new]]
