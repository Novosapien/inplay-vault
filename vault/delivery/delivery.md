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

## Delivery notes from the 27-07 → 07-08 touchdowns

**The four non-negotiables, in order.** Stated by George on 27-07 and held
across all five calls: **trading, market maker, ads**, then the **tax form**.
Everything else is explicitly deferred, including the analyst prices page and
the subscription features. George's argument, accepted by Edwin and Cody:
premium features are critical for revenue but the app **functions** without
them, whereas without trading and the market maker _"people can't use it."_
Edwin's counter-position, also accepted: not everything has to be live at
launch — _"if the subscriptions become available in week two of the NFL, so be
it."_

**Dry runs.**

| Date | What | Status |
|------|------|--------|
| 6 Aug | First dry run on a preseason game | ✂ Slipped — George called it "looking unlikely" on 31-07 |
| **13 Aug** | **Secondary-trading dry run** on a live preseason game, TestFlight, InPlay team plus friends and family. Several games that night, so multiple team companies possible | 🟡 Target |
| TBD | **IPO dry run.** The 13 Aug run is deliberately secondary-only; Edwin overrode the implication that there would be no IPO test at all — _"I want one test run at least before"_ | 🔴 Unscheduled |

Fallbacks if no live game is available: replay previously played games, or the
Sport Radar simulation games agreed 23-07.

**Estimation tooling (31-07).** Novosapien is building a skill to produce a
timeline, effort and backlog estimate **agentically**, from the actual cadence
of the work, rather than the traditional project-manager guess. Brett was
candid that it is proving difficult. Output: an InPlay-styled document in the
vault showing what has been delivered and what is queued, so the client can
re-prioritise against a visible backlog. This is the origin of the flight plan
above. Cody's ask that prompted it: _"I need daily insight into where the time
is being spent… it's not an attack, it's more just clarity."_

**⚠ Support and maintenance is an unfilled gap (Brett, 29-07).** There is no
support-and-maintenance contract, and Brett flagged it as the one thing missing
from InPlay's coverage — not for launch, but for when volumes rise. CTO-level
coverage is in place and a CIO is not needed at this size. The problem is that
conventional support means humans watching screens around the clock, which he
has built for mobile operators and banks and considers neither cost-effective
nor effective: _"you're trying to hire the most junior person, you're making
them do the shittiest thing, just monitoring."_ The proposal is to design it
**agentically** from the start rather than retrofit automation onto a human
rota. Method agreed: Brett lays out what conventional tiered support looks like,
then the group works out what can be automated. Deliberately **not** being
rushed before launch.

**Novosapien's own estimation caveat, worth keeping (George, 31-07).** On why
AI-assisted delivery dates are hard to give: _"sometimes it's like pushing a
snowball down a hill… other times we don't realise that we're at the start of
pushing it."_ Things that look easy can take two weeks; things that look hard
can be standing up overnight. This is the honest reason behind both the 6 Aug
slip and Cody's request for daily visibility.

Related: [[components]] · [[architecture]] · [[whats-new]] · [[compliance/compliance]]
