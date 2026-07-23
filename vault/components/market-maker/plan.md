# Market Maker — Build Plan

> **Component:** [[market-maker/market-maker]]
> **Status:** Draft — phases + dependencies; dates only where anchored
> **Timeline anchors:** launch mid-August (hard stop, [[vision]]) · NCAA IPOs
> ~20 Aug · first NFL game ~09 Sep ([[ipo-module/ipo-module]]) · synthetic
> market order needed **before first NFL game** (Edwin)

> ⚠ Reality check (raised 20-07): the full stack — valuation + market state +
> quoting + supervision + synthetic market orders — landed ~a month before
> launch. The plan below is deliberately a minimum-slice ladder: every phase
> produces something testable in QA, and scope bends before dates do.

---

> **Update 23-07 (MM follow-up call):** v1 got dramatically simpler — quote
> lifecycle is rest-until-gone (no top-ups, no aging), publish is post-first
> with momentary self-cross tolerated, randomizer is quantities-only, and the
> in-game price driver is SR's live probability pulled directly (no event
> weights). Cadence is bifurcated: live ~200ms · non-live 30–60s · earnings
> windows all-symbols ~5 min — so steady-state load collapses. New inputs:
> the **Wednesday data drop** (off-field index + remaining-game
> probabilities, InPlay-produced) and Edwin's original Python files.
> **Sequencing signal: Edwin wants to "start with the IPO"** (MM as IPO
> buyer) — fuller session promised. Testing: SR **simulation games** (replay
> a past game in ~4h) instead of waiting for preseason. E11 + E12 still
> unasked — another MM call expected.

## Phase 0 — Unblock (now, parallel)

The build can't start in earnest until these move; none are code.

- [ ] **Sport Radar probabilities feed fixed** (S1/S2) — the valuation
  engine's primary input. Cody chasing.
- [ ] **Synthetic MM entity in T0 QA** (T1) — asked 20-07, Tue/Thu calls.
- [ ] **Thursday 23-07 deep-dive** — extract E1–E10 (the numbers, the trigger
  script, conformance bar). Bring [[market-maker/parameters]] as the agenda:
  every 🔴 row is a question.
- [ ] **T0 throughput + bands answers** (T2–T5).
- [ ] **Gateway cancel system (35=F/35=G)** — committed 22-07, owner Hasan.
  A hard prerequisite for any re-quoting: without it every replaced quote
  strands a resting DAY order until 23:59 ET. The MM build queues behind it.
- [ ] **E11 settlement definition + E12 NCAA scope** from Edwin — E11 anchors
  the valuation semantics, E12 decides the load profile and book count.
- [ ] Draft the **merged profile table** (N2) structure — values are Edwin's.
- [ ] **Verify Sport Radar fit (S5):** live win probability readable ~every
  200ms per live game, quota to match, + simulation games for testing.
- [ ] **Betting-feed parity (S4)** — probabilities must not lag
  DraftKings/FanDuel; Cody owns.
- [ ] **Wednesday data-drop pipeline** — agree format/delivery for the weekly
  off-field index + remaining-game probabilities (InPlay → us).
- [ ] **Edwin's Python files** — receive + read the original MM simulation
  code (E4, in motion).

## Phase 1 — Valuation engine walking skeleton

Goal: a live ESV per team in QA, driven by real Sport Radar data.

- Ingest win probabilities + season win totals; compute
  `on-field = P(win)×$/win + E[remaining]×$/win` with a placeholder $/win.
- Static off-field seed (wire the earnings engine later — E2).
- Event-driven recompute on game events; event-sourced lineage from day one.
- Publish ESV → RP on the bus (N1; NATS topic per team fits the existing
  [[architecture/architecture]]).
- **Exit test:** replay a recorded past game; ESV moves per play,
  deterministically, twice identically.

## Phase 2 — Quoting engine, one team, QA

Goal: the SDMM quoting a single team's book against the QA entity.

- Decision cycle loop (trigger → price → build → validate → publish → commit).
- Reservation prices with base spread + inventory skew (λ); ladder N levels;
  static sizes; tick conformance; never-crossed validation.
- Cancel-replace via the MM's own FIX OE session; fills → inventory feedback.
- **Exit test:** trade against it manually in QA; watch it skew after eating
  inventory; confirm cadence sustainable (T2).

## Phase 3 — All teams + sessions + state

Goal: 32 NFL books live simultaneously with session-aware behaviour.

- Market-state layer: condition classifier (simple thresholds), merged profile
  table, session state machine off the fixture schedule.
- Frozen-RP failure mode wired end-to-end (kill the feed mid-test).
- Randomizer (seeded) on sizes; profile-driven gain scheduling.
- Scale target: **32 NFL books minimum; up to 170 (32 NFL + 138 NCAA) if E12
  lands NCAA-in.** ⚠ NCAA IPOs run ~20 Aug on the *primary* plane
  (internal — no MM involvement); whether NCAA gets a *secondary* market in
  season 1 is the open Edwin question that decides the load profile.
- If NCAA-in: peak day is an NCAA Saturday (~30–40 concurrent games → 60–80
  hot books) and **activity-tiered cadence is a requirement** (hot 5–10/sec,
  warm ~1/sec, cold heartbeat-only). If NFL-only: load is trivial.
- **Exit test:** a full simulated peak day in QA — concurrent games, staggered
  windows, pre-game → live (event storm) → post-game → overnight widening.

## Phase 4 — Supervision + synthetic market order

Goal: orderly markets + the user-facing "market" button. **Gate: before first
NFL game.**

- Band checks at order entry (app-side) + out-of-band execution detector;
  bust workflow per the T0 procedure (T4); manual halt/resume.
- Synthetic market order in the Trading Service (N levels through, Troy's
  logic) — designed together with the band so N can't sweep outside it.
- **Exit test:** deliberately fat-finger in QA; detector flags; bust reverses
  positions via ExecType=H.

## Phase 5 — Ops UI + calibration (through the season)

- MM ops desktop surface (Kevin's workshop first — see
  [[market-maker/systems/mm-ops-ui]]): params, orders, positions/P&L,
  supervision flags.
- Calibration loop: trigger weights vs observed market reaction; Edwin's old
  script as seed; expect volatile first weeks (accepted 20-07).
- Aggressive-order behaviour (E8) only after bounds agreed — not in v1.

## Workstream split (proposal)

Valuation engine and quoting engine are separable workstreams after Phase 1's
RP contract is fixed — they meet at one bus topic. Supervision + synthetic
market order ride the existing Trading Service / FIX GW work. Ops UI last.

## Standing cadence

- **Mon/Wed/Fri:** internal touchdowns.
- **Tue/Thu:** T0 tech calls (entity, throughput, bands, busts).
- **Thu 23-07:** Edwin deep-dive — parameters + conformance sign-off.
- After every session: update [[market-maker/decisions]],
  [[market-maker/open-questions]], [[market-maker/parameters]].
