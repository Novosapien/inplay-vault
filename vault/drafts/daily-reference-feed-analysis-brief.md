---
description: "Brief for a dedicated session: analyse Edwin's material on how the daily reference feed is created and design our build — analysis only, no deployment"
---

# Brief — the daily reference feed: analyse Edwin's material, design our build

> **From:** the 2026-08-13 MM working session (George's ask).
> **Mode:** ANALYSE and design. Build only what analysis justifies.
> **⚠ DO NOT DEPLOY anything from this work** — George's explicit
> instruction. The live machine (supervised21/CFG-0020) quotes from the
> static 08-11 inputs file and stays untouched.

## The question

The MM quotes around a reference value per team. Today that value is
STATIC — seeded 08-11 from `reference/ipo-prices-170.csv`. The designed
end state is a DAILY file (06:00 ET) of `expected_remaining_wins` +
`sigma` per team, 170 rows. Edwin sent material on how that file may be
created. Analyse it and produce the design for our side.

## Read first (the mandatory order applies — working-guide.md)

Then, the material itself:

1. **`reference/inplay-reference-feed/`** — Edwin's 28-07 delivery: the
   feed engine AS RUNNING CODE (win-total maths, devig,
   double-count-safe pricing, the college ratings feed, the IPO
   formula; 31 tests pass). `README-edwin.md` maps his email items to
   modules. `validate_records()` is the one module we may reuse
   verbatim.
2. **`reference/sample_reference_feed_2026-08-29.json`** — a valid
   sample of the daily file in the production schema
   (`expected_remaining_wins`, `sigma`, `games_remaining`,
   `effective_time`, `revision`, `is_correction`,
   `methodology_version`).
3. **`reference/edwin-handoff-2026-08-09/`** — the newer fair-value/EV
   handoff (`03-PRICING/` first): resting EV (`seasonFair`) and live
   EV (`lgValuePrice`). Establish how (whether) this newer model
   relates to or supersedes the 28-07 feed maths before designing
   anything.
4. **The open questions that gate this:** N19 (delivery decided: bucket
   + database, upload page later; ⚠ still open: WHO uploads at
   06:00 ET until the page exists — George's call). N23 (the feed has
   no §7.3 event type — a replay-equality problem; raise with InPlay,
   never invent). E19 context in decisions.md (Σ GEV = $5 × expected
   wins — the per-fixture breakdown cancels).

## What the analysis must answer

1. Can WE generate the daily file from bookmaker lines with Edwin's
   own code, or does Edwin remain the producer? (Who owns the
   methodology; what breaks if we run his maths ourselves.)
2. How the 08-09 EV model and the 28-07 feed engine relate — one
   model or two? Which is normative for the reference value?
3. The ingestion design our side: bucket watch → validate at the door
   → journalled event (N23's answer) → T updates mid-session — and
   what "how long may we quote on a stale T" needs from Edwin
   (the unsent E-round question).
4. A build plan sized honestly (the upload page is N29's panel
   pattern: new pages + proxy endpoints, no new deployment unit).

## Constraints

- Analysis and design in the vault; code only if the design is
  approved. NOTHING deploys to the VM or the panel from this session.
- Every number gets a parameters.md row with a status.
- End with a session note + updates to the working docs touched.
