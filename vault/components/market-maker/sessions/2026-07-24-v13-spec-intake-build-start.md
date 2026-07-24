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

## Part 2 (same day) — the build itself + ingestion research

**Built** (`inplay-market-maker`, Python, 6 commits, 48 tests, ruff + mypy
strict clean). Step by step with George, each step explained before writing:

1. Scaffold + decimal policy (§1.6-3) + the §5.7.3 quantity golden fixture
   reproduced byte-exact.
2. Event envelope (§7.1) + idempotency keys (§7.3).
3. Journal (fsync'd, append-only) + acceptor (§7.2/§7.4) — dedupe, conflict
   detection, restart recovery from the journal alone.
4. Reference Price formula (§3.1) + probability validation bands (§3.2).
5. Valuation engine wired end-to-end → price stream, with **replay equality**.
6. SR adapter + a **real captured game** (Chiefs–Ravens 2024, 1,089
   probability points): kickoff $2.83 → final whistle $5.00, replayed
   identically from the journal.

**Researched** (two agents + live API probes + the tZERO PDF):

- **No probabilities push feed exists — any sport.** Pull only. Verified four
  ways incl. every SR spec on the MCP.
- **Cadence correction:** median 4 s, not the "per play ~30–40 s" we had
  recorded twice. ~2 s polling still right, for a different reason.
- **Centrifugo is the wrong plane** (at-most-once, recovery-by-refetch);
  the service's Redis probability keys are stale cache-aside artefacts.
- **tZERO OE spec re-verified:** ClOrdID ≤20/no leading zeroes (two ids on
  replace + cancel), `HandlInst` asymmetry confirmed, **no rate-limit
  language anywhere** → T2 must be asked with T1.
- **Gateway: everything is built.** Cancel + replace live and QA-passed vs
  real tZERO; dead-man switch, tag-60 passthrough, rejection NAKs, MM
  namespace and at-least-once all deployed. **We are now the gating item**
  (`MM_ENABLED=false` until our bot exists).

**Decided (George):** peak messaging is a non-issue · the ClOrdID scheme is
fine · heartbeat cadence and the dead-man window are ours to set (we can
change the gateway ourselves) · watchdog/supervision descoped to tZERO.

**Opened:** S8 (SR's "media use only — prohibited for betting clients"
clause) · S9 (feed latency — ours to measure in August, not an SR ask) ·
N15 (heartbeat/dead-man window) · N16 (official results have no bus source).

**Late in the session:** drafted the SR product ask to Cody (sent) — the
volume case for Global American Football Probabilities: v1 has no bulk live
endpoint, so per-game polling costs ~8M requests/season (~6M of it NCAA) at
~20 req/s peak, versus ~1M at 0.5 req/s on v2. Business-language, three
iterations to strip technical framing. George cut the feed-latency question
(we measure it) and the commercials line; added two coverage questions —
does SR price *every* college game, and how far ahead of kickoff. **S6
reduced**: v2's schema was checked and is also 2-way, so no SR product
solves ties — and NCAA cannot tie at all (overtime since 1996), leaving only
NFL's ~0.5 % as an Edwin ruling.

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
