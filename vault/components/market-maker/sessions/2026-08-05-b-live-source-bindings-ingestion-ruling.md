# 2026-08-05-b — the live source, all 170 bindings — and George's ingestion ruling

> **Who:** Claude (autonomous start) + George (live review — and he caught
> a real drift)
> **Type:** build session, then a course correction
> **Refs:** `inplay-market-maker` commits `06d6853` · `df6ae5b` · `0047f87`
> · `46af364` · `1232c33` (all LOCAL, deliberately unpushed — George)
> · **500 → 512 tests**, ruff + `mypy --strict` clean

## What we did

1. **`HttpSource` built** behind the `GameSource` seam — Probabilities v1
   timeline + Sport Schedule, `x-api-key` header, `parse_float=str`.
   With it, the seam's first failure contract: `SourceUnavailable`, one
   exception for every cause; the worker skips a failed game;
   `games_polled` now means FETCHED SUCCESSFULLY (it feeds the E38
   `observations` map); retry rides the tier's own cadence.
   `source_fetch_timeout_s` = 1.5 s (Ch 12, ours).
2. **The bindings captured** — 14 Sport Schedule calls on the trial key,
   1 s apart, every raw response saved (`--from-raw` re-derives with zero
   quota). 163/170 exact normalised name matches, 0 conflicts.
3. **George reviewed live, in chat.** The 6 name variants were verified
   against SR's competitor-profile endpoint (core key): Texas A&M ·
   Marshall · Middle Tennessee State · Sam Houston State · UMass ·
   Delaware — all confirmed. The **LA Rams** appeared on no captured
   date (rolling pricing), so the id came via the NFL league uuid
   (`2eff2a03-54d4-46ba-890e-2bc3925548f3`) through the AF Base mappings
   bridge → **`sr:competitor:4387`**, profile-confirmed.
4. **All 170 baked into code** — `mm/bindings.py::TEAM_BINDINGS`,
   validated at import (exact universe coverage, no duplicates,
   provenance in the notes). The bindings live-gate CLOSED.

## What went wrong — the drift George caught

⚠ **The build had drifted from the 24-07 ingestion decision, and this
session extended the drift instead of flagging it.** The recorded
architecture is *"a dedicated MM poller at the edge… write-through push
(Redis + bus)… the valuation/quoting hot path never calls SR"* — a
poller that publishes onto the bus. What got built (01-08 poller,
04/05-08 runtime, and today's HTTP source) is the poller absorbed INSIDE
the MM engine, fetching SR itself. Every step was logged, and the Cloud
NAT confirmation implied it — but nobody reconciled the built shape
against the 24-07 decision. **Stop-condition #2 (contradicts a recorded
decision) should have fired before the HTTP source was written. It did
not.** George caught it in review.

Also: George had not approved this session's autonomous start — the
handover carried the 05-08 "trial key covers the build" ruling forward
as authorization. The API spend was bounded (14 trial calls + ~15 core-
key calls, every response saved), but the lesson stands: a handover is
context, not consent.

## Decisions *(mirrored into decisions.md · parameters.md · plan.md)*

- ⭐ **George's ingestion ruling: the sportradar SERVICE polls SR and
  publishes readings on NATS. The MM consumes the bus and never calls
  SR itself.** The in-engine pull path must not go live. The HTTP class
  and the failure contract transplant to the service side; valuation,
  quoting, journal, replay and the E38 liveness rules are untouched (the
  fetch stamp fits the message key on the push path — his design,
  already recorded 05-08).
- **Process (George):** the migration is scoped in writing and approved
  before any build. Before touching the sportradar service: git pull,
  verify local state, then branch off **dev**. The five MM commits stay
  LOCAL — do not push; overwrite them if the scope demands it.
- Ours, autonomous, tagged in code: the seam's failure contract · the
  1.5 s fetch timeout · exact-match-only bindings capture.

## Questions

- None opened, none closed by number. The bindings gate closed; the
  ingestion-move gate replaced it in `LIVE_GATES`.

## Next

1. **Write the ingestion-move scope** (one page: what moves into
   `inplay-sportradar-service`, the NATS message shape, who owns the
   poll tiers, key/quota ownership, the fetch-stamp-in-key liveness
   design) — **George approves before any build**.
2. §10.3 checkpoints — its own session, required before the season.
3. Send the Edwin round E29–E38 + N23/N28.
4. The 06:00 file hand-off (N19) — George's call.
