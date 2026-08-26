---
description: "Edwin's E51 parameters deployed live, the maker moves to the MM gateway, and mm-2's broadcast ack crash-loops mm-1 — the alien drain ships in an hour"
---

# 2026-08-20e — The E51 deploy, and the night the two makers met

> **Who:** George + AI session (the same session as
> [[market-maker/sessions/2026-08-20-widen-and-thin-parameter-round]] —
> this note covers the evening: build, deploy, operations, incident).
> **Type:** build / deploy / incident.
> **Refs:** `inplay-market-maker` `main@68b76a8` · `main@76341d3` ·
> `main@d162d8c` · journals supervised42–45 · CFG-0039–0043 ·
> the Go session's `feat/phase-3-ingestion@46c9538`.

## What we did

**1 · Built and deployed Edwin's parameter answers (E51 answers 1/2/3/5/6)**
as `main@68b76a8`, pushed straight to main on George's call, no PR:
`min_width_ticks` 25 · levels 1/1 · `base_size` 550 · `min_quantity` 100 ·
`material_qty_change` 50 · NEW `skew_reference_shares` 48,000 · NEW width
floors 50/100. The lean repointed at the ORCHESTRATOR (the live path —
`reservation_midpoint_for` has no production caller); `PositionRecord`
reports the APPLIED lean; `state_floor_ticks()` wired at both `full_width`
call sites. Answers 4 (the drift) and 7 (3× shedding side) deliberately
NOT built.

**2 · Migrated the Python maker to the MM gateway** (10.0.1.3) in the same
deploy — ops URL, the key already in `env.secret`, firewall already open.

**3 · Started maker and taker on the new book** and verified at the venue:
360 orders / 180 books, one rung a side, JETS 46.19/47.19 — **the $1.00
overnight floor binding correctly on the first live look**. Sizes 467–638
proved the 550±25% band and the dropped 1,000 minimum.

**4 · Narrowed mm-1 to 170 symbols** (the ten `.TEST` out) for the Go
maker's shape test — fresh journal supervised43 / CFG-0041, and a filtered
`supervised-inputs-170.json` after supervised mode refused the 180 file.

**5 · The incident, and the fix** — see below. Deployed as supervised45 /
CFG-0043 @ `76341d3`; peer-review responses as `d162d8c` (docs+tests only).

## What we learned

⭐ **The republish clock can be alive while the venue sees nothing.** George
caught the book frozen; the chain is three correct rules interlocking: the
overnight floor pins width at exactly 100 ticks (the equation reaches ~30,
so the floor swallows the jitter) → identical prices every re-roll → N10's
rest-until-gone keeps every standing order → zero instructions. A bitten
rung stays bitten until ~240 net shares move IA by $0.005, or the 06:00 T
file moves RP. Not a defect — but §5.9 replenishment (E17) is the designed
answer and is unbuilt. ⚠ Also: **the tick line's `sent=` does not count
converger sends** — the gateway tracker is the truth.

⭐ **The one-writer assumption ran through three layers, and all three bit
in one evening.** The gateway broadcasts the MM namespace's events to every
consumer. mm-2's ORDER_ACCEPTED (`MMc528ef97c2cce5a6`, buy 10,975 @ 78.12,
`.TEST`) reached mm-1, was journalled, could not resolve a security, raised
in apply, and **crash-looped the engine on replay at every boot** —
NRestarts 25, dead-man fired 21×, the namespace swept to nothing. The three
layers: the venue engine's "non-terminal acks stay fatal" rule, the
adapter's unmapped-fill refusal, and the boot healer's `MM`+16-hex
ownership test (which cannot distinguish the two engines).

⭐ **The alien drain (built and deployed inside George's one-hour window,
games approaching):** untracked order + UNRESOLVABLE security → drained,
counted, rate-limited log — the blindness argument survives only where the
security resolves, because an unresolvable security can never be in our
universe. Two layers, because the poison has two routes: `[alien-drain]` in
`venue/engine.py`, and `UnmappedFillSymbol` at translation with a loud
per-fill skip in the inbound drain. Busts stay fatal. A poisoned journal
now replays clean.

**The Go session's review of `76341d3` — three findings, all accepted:**
(1) the real lever is a per-writer `MM_USER_ID` — the gateway routes
`order.{userID}.*`, so a distinct id removes the class at source (queued;
needs Hasan's `HOUSE_EGRESS_SUBS`); (2) the drain's invariant is unenforced
— an alien order on a SHARED symbol is still admitted, safe only while the
universes stay disjoint — now named in code and pinned by test on both
sides; (3) the engine-level fill drain is replay defence-in-depth, now
commented so nobody deletes it. Their side ported the drain (`46c9538`) and
minted `MMGO` + 14 hex (inside the gateway's required `MM` namespace, fails
our ownership test on the `G` — the `MMSN` mechanism).

**The supervised-inputs file validates against `MM_SECURITIES` exactly** —
narrowing the universe without filtering the file boot-loops the engine
three times before you read the error.

## What went wrong / got stuck

- ⚠ **My green light for mm-2 caused the incident.** I told the Go session
  "you can start mm-2 now" after fixing only the healer-sequencing hazard —
  the broadcast-ack poison was invisible until it fired. mm-2 survived its
  own window only because the overnight floor had frozen mm-1 into silence.
- ⚠ A validator I wrote rejected Edwin's own overnight floor (100 ticks >
  `max_width_ticks` 60) — the two bound different things; dropped with the
  reasoning recorded in the dictionary.
- ⚠ Nineteen tests failed on the parameter change alone — rounding and
  additivity tests had absorbed policy numbers into their arithmetic. All
  restated against the dictionary; `full_width` takes its bounds as
  arguments now.
- ⚠ The first mm-1 stop mid-verification triggered the dead-man sweep of
  its own standing book (by design, but twice in one evening) — the sweep's
  `stillResting=182` ERROR is an ack race, not an incident signature.

## Decisions made *(dated 20-08, George)*

- ✅ Build the E51 parameter set NOW, straight to main, no PR.
- ✅ Deploy but do not start → then start maker → then start taker.
- ✅ Taker sizes STAND against the new book (assessed fine; max draw is a
  ~0.2% tail).
- ✅ Build the alien drain immediately, games inside the hour — **the
  two-reviewer round is owed retroactively** on `68b76a8` and `76341d3`
  (the Go session's review of the latter partially discharges it).

## Questions opened / closed

- **E17 gains evidence:** the floor + N10 + no-replenishment interaction
  leaves overnight books bitten until the next T file. For Edwin's round.
- **New infra item (from the Go session's finding 1):** per-writer
  `MM_USER_ID`, needs Hasan. ✎ Overtaken 26-08: the gateway's per-bot
  dead-man (#28) is the same hazard family being fixed at the source.
- **T23** (participant trade feed) — still unasked.

## Next

The maker was later stopped deliberately for the NCAA offering (R-V08,
21-08 18:44Z — a different session's operation). When it returns for
secondary trading: it comes back on `main@d162d8c` or later, fresh journal,
new config version, and **the first live game on the E51 book is still
unobserved** — watch the $0.25 spread, the 550 touch and the 12,000-share
lean under real game load.
