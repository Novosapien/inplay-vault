---
description: "The process for every MM work session — mandatory reading order, ground rules, the session loop, note format and where each doc lives"
---

# Market Maker — Working Guide

> **Component:** [[market-maker/market-maker]]
> **Purpose:** The process for ANY session of work on the market maker —
> human or AI. Read this first, every time. The goal of the current phase is
> to converge on a **build plan** and then execute it without losing context
> between sessions.

---

## 1 · Before you start — mandatory reading order

Absorb these, in this order, before touching anything:

1. **[[market-maker/market-maker]]** — the hub: what the MM is, the system
   map, boundaries.
2. **[[market-maker/decisions]]** — the dated log of what's been decided.
   **This log outranks everything**: where it conflicts with the CTS/PTS
   standards or any external doc, the log wins.
3. **[[market-maker/open-questions]]** — what's live, who owes it
   (E=Edwin, T=tZERO, S=Sport Radar, N=us). Never re-open a resolved item
   without logging why.
4. **[[market-maker/parameters]]** — every number and its status
   (✅ confirmed · 🟡 proposed · 🔴 TBD). No number gets used in code or specs
   without a row here.
4b. **[[market-maker/requirements]]** — the normative list: what MUST be
   true to go live, each with a source and a status. Change it only
   through its dated addendum, never silently.
5. **[[market-maker/plan]]** — phases, dependencies, timeline anchors.
6. **The latest note in `sessions/`** — what happened last time, what was
   left dangling.

Deep reference when needed: **[[market-maker/build/index|build/]]** — the
as-built SOURCE OF TRUTH, one page per part of the machine (key equations
as implemented, the module map; read the page you are about to touch
before touching code you have not read), the systems docs for the four
UNBUILT systems only
([[market-maker/systems/market-supervision|supervision]] ·
[[market-maker/systems/synthetic-market-order|synthetic MO]] ·
[[market-maker/systems/mm-ops-ui|ops UI]] ·
[[market-maker/systems/expected-wins-pipeline|expected-wins pipeline]] ·
[[market-maker/systems/snt-1-noise-taker|SNT-1]] — the built systems'
design narratives are archived; build/ is their truth), the
[[market-maker/glossary]], and the plain-English guides in
[[standards/README|standards/]] (+ `standards/sdmm-machine.html` for the
interactive equation map).

## 2 · Ground rules

- **The standards are context, not law.** Edwin: "meant for Claude to read…
  fairly simple." [[market-maker/decisions]] records where spoken decisions
  supersede them.
- **The 22-07 filter:** from the platform team's `trading-architecture.md`,
  platform + venue facts are gospel (they're live-verified). Anything about
  the MM's own design (their `sdmm.py` prototype, its params, cadence, MM
  identity) is **suggestion only** — we are building the MM from scratch.
  Adopt or replace each suggestion explicitly (open question N9), never
  silently.
- **Every number has a status.** Nothing goes into code or a spec as fact
  unless it's ✅ in [[market-maker/parameters]]. Proposals are fine — mark
  them 🟡 with a source.
- **Determinism is non-negotiable from day one** in anything built: seeded
  randomness only, no wall clocks, event-sourced state. Cheap now, brutal to
  retrofit.
- **The MM lives on the secondary plane only.** IPOs fill internally and
  never touch it.

## 3 · The session loop

Every working session — a call, a build session, a design session — follows
the same loop:

```
START   read §1 in order · read the last session note
WORK    do the thing
END     1. write a session note in sessions/ (format below)
        2. update the working docs the session touched:
           · new decision?            → decisions.md (dated, sourced)
           · question answered/raised?→ open-questions.md
           · number learned/proposed? → parameters.md (with status)
           · plan shifted?            → plan.md
           · machine changed?         → build/ (the as-built pages —
                                        update the page you changed;
                                        keep them TRUE)
           · built/merged/deployed?   → build-deploy-log.md (the
                                        cross-session pipeline state —
                                        update the row IN the session,
                                        and CHECK it before deploying)
        3. leave a clear "next" line — the next session starts there
```

The session note is the narrative; the working docs are the state. **Both**,
always — a note that doesn't update the state gets lost; state changes
without a note lose their why.

## 4 · Session notes — format

One file per session in `sessions/`, named `YYYY-MM-DD-short-slug.md`
(same-day second session: `-b` suffix). Copy `sessions/TEMPLATE.md`. Keep it
honest and fast — 10 minutes max:

- **What we did** — the work itself
- **What we learned** — new facts, insights, surprises
- **What went wrong / got stuck** — dead ends, blockers, mistakes worth
  remembering
- **Decisions made** → mirrored into decisions.md
- **Questions opened/closed** → mirrored into open-questions.md
- **Next** — the first thing the next session should do

## 5 · Where things live

| Thing | Home |
|---|---|
| What the MM is + system map | [[market-maker/market-maker]] |
| Per-system design | `systems/` |
| Concrete function bodies | the code (`inplay-market-maker/src/mm/`) + [[market-maker/build/index\|build/]] (the pre-spec pseudocode is archived) |
| Decisions (outranks standards) | [[market-maker/decisions]] |
| Live blockers by owner | [[market-maker/open-questions]] |
| Every tunable number + status | [[market-maker/parameters]] |
| Build phases + dependencies | [[market-maker/plan]] |
| **What MUST be true to go live — the MM** | [[market-maker/requirements]] |
| **What MUST be true to go live — the taker** | [[market-maker/market-taker-requirements]] |
| Live test cases + statuses | [[market-maker/test-plan]] |
| **In-flight changes: built / merged / deployed / verified** | [[market-maker/build-deploy-log]] |
| Vocabulary + equation symbols | [[market-maker/glossary]] |
| Distilled understanding (concepts, traps caught) | [[market-maker/learnings]] |
| **Defects the Go port found in the Python engine** | [[market-maker/go-port-findings]] |
| Session-by-session narrative | `sessions/` |
| Source standards + plain-English guides | [[standards/README\|standards/]] |
| Platform reality (venue facts, gateway, streams) | `trading-architecture.md` (platform team's doc — apply the 22-07 filter) |

## 6 · Current mission

Converge on the **build plan** and start executing:

1. Close the Phase-0 blockers ([[market-maker/plan]]) — Thursday deep-dive
   (E-items, esp. **E11 settlement definition**, **E12 NCAA scope**), tZERO asks
   (T-items), Sport Radar feed.
2. Make the N9 adopt-or-redesign calls — our from-scratch MM design vs the
   platform doc's suggestions.
3. Lock the architecture (N7 topology, N1 transport) and turn plan phases
   into tracked issues.
4. Build, session by session, logging as we go.
