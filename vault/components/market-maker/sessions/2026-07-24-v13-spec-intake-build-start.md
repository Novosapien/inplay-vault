# 2026-07-24 — v1.3 Build Spec intake · SR probability probe · build starts

> **Who:** George + Claude
> **Type:** document intake / live API research / build kickoff
> **Refs:** `standards/MM-build-spec-v1.3.docx` + `.html` · [[market-maker/decisions]] (24-07 entry) · `inplay-sportradar-service` + `sportradar-futures` research · `inplay-market-maker` (new repo)

## What we did

- **Processed the incoming Edwin material** — not the Python files or formula
  write-up, but a full **Consolidated Build Specification v1.3** ("release-final
  for Novosapien"). Followed the incoming-doc protocol: conflicts surfaced in
  chat, nothing written until George validated.
- **Adopted the spec as the working baseline** (supersedes CTS/PTS for
  implementation) with the three spec-vs-call conflicts held open as
  **E17 (lifecycle) / E18 (cadence) / E19 (probability source)** — not
  silently resolved either way.
- **Rendered the spec verbatim** in the PTS-guide house style
  (`standards/MM-build-spec-v1.3.html`; also `~/Downloads/`) — typeset maths,
  one boxed equation each, chapter-per-page nav. Several formatting rounds:
  George rejected the first two designs.
- **Confirmed venue = tZERO** (George) — spec C-1 answered our side; the
  "Matching Engine ICD" is effectively the tZERO FIX specs mined 23-07.
- **Probed SR live with the trial Probabilities key:** product entitled and
  working (S1 downgraded) · 2-way market only, **no tie probability** (S6) ·
  **rolling pricing** — NCAA 70/~1,700 priced, NFL priced via date-schedule
  despite an empty seasons listing (proof for E19) · v2 live-bulk endpoint
  exists but 403 (S7 product ask).
- **Ran codebase research agents** over `inplay-sportradar-service` +
  `sportradar-futures`: full probabilities plumbing already built (bulk,
  timeline, season odds) behind the entitlement; schedules/results for all
  170 teams work today; **simulation replay works** (SR playback host +
  local JSONL) — S5 resolved.
- **Updated the vault:** decisions (24-07 entry), open-questions (E1/E5/E11/
  E12/E14/N2/N3/N11/S5 closed · E17–E19/S6/S7 opened), parameters (v1.3
  registry now the authoritative table), plan + hub (baseline + build start),
  standards README (supersession banner), learnings (6 entries).
- **Build kickoff (George):** new repo **`inplay-market-maker`**, **Python**,
  we build everything, step-by-step working mode — each step states what
  we're writing, why, and which spec sections to read.

## What we learned

- The spec overturns three spoken decisions from five days earlier — the
  surface-don't-adopt protocol did its job. Full list in
  [[market-maker/learnings]] (24-07 section): priced-games/rolling pricing,
  polling-rate ≠ cycle-rate, derived quota ask, probe-before-trusting,
  verify-fixtures-on-arrival.
- The spec's own D-1 requirement (all ~2,400 games priced from season open)
  is unsatisfiable against the real SR product — Edwin's 23-07 internal-weekly
  model was the workaround all along.

## What went wrong / got stuck

- **Formatting the spec render took three rounds** — first a generic layout,
  then equations too bunched. Lesson: match the established house style
  (PTS guide) from the start; one boxed equation each, spacing matters.
- I started rewriting plan.md phases solo — **George stopped it**: planning
  is collaborative. Only agreed facts went in; phases get re-cut together.
- A trial API key was pasted into chat — usable, but flagged: dev-only,
  rotate when the production key lands; never into git or the vault.

## Decisions made *(mirrored into [[market-maker/decisions]])*

v1.3 spec = baseline (with E17–E19 carve-out) · venue = tZERO · probability
poller architecture (write-through push, library reuse, no TTL cache-aside,
hot path never fetches) · build starts now on mock/replay inputs · repo
`inplay-market-maker`, Python, step-by-step mode.

## Questions opened / closed *(state in [[market-maker/open-questions]])*

- **Closed:** E1 · E5 (▸ pending) · E11 · E12 · E14 · N2 · N3 · N11 · S5.
- **Opened:** E17 lifecycle conflict · E18 cadence conflict · E19
  remaining-season probability source · S6 no tie probability · S7 SR
  product/quota ask.
- **Updated:** S1 downgraded (trial key works) · N14 gated on E17 · T11 spec
  STP tension added · E16 spec-implies-yes.

## Next

1. **Build step-by-step in `inplay-market-maker`:** scaffold → decimal policy
   (§1.6-3) + the §5.7.3 golden fixture as the first conformance test → the
   replay harness (event envelope §7.1, sequencer §7.4, journal) → valuation
   engine (§3) on mock/replay inputs.
2. Draft the **written blocking questions** (E17–E19, S6, S7) for InPlay per
   spec §1.6-1.
3. Chase: SR production entitlement/quota (S7 via InPlay) · gateway cancel
   build (Hasan) · T1 MM account permission.
4. Put the trial key into the SR service's `PROBABILITIES_API_KEY`
   (Secret Manager / `.env` — never git).
5. Push this branch + open the PR (overdue since 22-07).
