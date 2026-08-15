---
description: "Gateway watch, then forensics: feed retirement races engine freshness — 10 books suspended, 2 quoting stale — publisher keep-polling fix in PR #38"
---

# 2026-08-14 — the gateway watch, and why the morning books were dark

> **Who:** Claude (dedicated gateway watch session, monitor-only) + George
> **Type:** monitoring + live forensics + user support. Nothing deployed,
> nothing changed on any VM — reads only, plus approved evidence captures
> to the operator home dir.
> **Refs:** gateway `/health` + `/quotes` · gateway journal + syslog ·
> `/var/lib/mm/supervised27/journal.jsonl` ·
> `inplay-sportradar-service` `mm_publisher/worker.py` + `scheduler.py` ·
> [[market-maker/sessions/2026-08-13-e-publisher-universe-filter-outage]] ·
> [[market-maker/build-deploy-log]]

## What we did

- **Watched the dead-man through the night window.** Per-minute monitor on
  `/health` + `/quotes` (5-min summaries, instant CRITICALs). Observed the
  fire loop live (bursts 1–8/min, whole-book cancels, ~30–180 of 360 book
  sides blank at any snapshot), then the **00:19:23Z latch** (heartbeat
  silent 43 s), then the coordinated restart at 00:19:26Z that carried the
  fix: **`MM_DEADMAN_TIMEOUT_MS` 4 000 → 10 000**. Zero fires from then to
  the last sample (02:18Z). Worst post-fix silence: 4.15 s at ~01:49Z — a
  fire under the old window, absorbed by the new one.
- **Supported George on Edwin's order-book question** (bid at 74.12 "not
  showing"): the order had filled — a bid inside the spread was hit before
  the next book render. Real residual bug: the tape (Last / Day High) never
  printed the 74.12 trade; bug report drafted for the app team.
- **Morning forensics: why 10 books show suspended.** Traced from the
  gateway (`/quotes` staleness), the engine journal (per-game reading
  stops, per-book cancel times), §6.3 in `market_state/engine.py`, and the
  publisher's scheduler. Root cause found and code-verified (below).
- **Recovered the incident evidence.** journald had rotated everything
  before 01:13Z; the 23:00→00:08 capture existed from last night, and the
  lost 00:08→01:13 window (the latch + restart) was recovered from
  `/var/log/syslog`. On the gateway VM: `gateway-deadman-incident-2026-08-13.log`
  (23:00→00:08) · `...-full.log` (01:13→05:00) ·
  `...-0008-0113-syslog.log` (the gap). Complete across the incident.

## What we learned

- **The game's end is undesigned end-to-end.** The publisher polls a
  finished game for 1 h after SR flips `ended`/`closed`, then stops **for
  good** (`scheduler.py::interval_s` returns `None` — "done for good").
  The engine has no game-end transition, so the end of re-offers lands as
  ordinary staleness. Two opposite failures, both observed live:
  1. **Books still inside the live 5/10/20 s freshness regime** went RP
     Invalid 20 s after the last re-offer → §6.3 → **SUSPENDED**, with no
     re-open path. Ten books (49ER, BENG, CARD, CHAR, LION, PACK, RAID,
     STEE, TEXS, TITA) dark all day. The timing matches to the second:
     CIN–DET's last reading 03:01:06Z → BENG/LION swept 03:01:25Z;
     SF–TEN's last reading 04:56:02Z → 49ER/TITA swept 04:56:23Z.
  2. **NE–IND's retirement landed ~4 min after its books left the live
     regime** → no suspension → **PATR and COLT quoted pre-final prices
     for 8+ hours with the result public** — open pick-off exposure, the
     dangerous direction.
- **The game-end fact already reaches the engine and nothing consumes
  it.** Every re-offer carries `status: "closed"` in the payload — the
  worker docstring says it is carried precisely so "a final… still
  reaches the MM". The consumer side was never built.
- **Suspension is DERIVED state, not journalled.** A fresh-journal deploy
  erases it: after the in-flight CFG-0026 cutover, all 12 played-team
  books re-quote at seed prices unless excluded or manually suspended.
  Flagged to the doc-sync and engine sessions mid-ceremony.
- **A game whose status never flips polls at the LIVE tier forever.** The
  duplicate SF–TEN id (`sr:sport_event:68385804`, the N39 identity gap)
  had streamed 53k+ settled 0/1 re-offers by 11:41Z and was still going.
  It binds to no book, so it is waste rather than damage.
- **George's fetch-age doctrine is correctly implemented for live games**
  — unchanged values re-offer under fresh fetch stamps (E38) and freshness
  prices observation age. The failure is lifecycle, not doctrine.
- The dead-man fix held: 0 fires in ~2 h of live-game load after the 10 s
  window, against ~200 before it.
- **Addendum (12:11Z, George's question — could we have kept polling?): the
  suspensions were entirely self-inflicted.** One direct SR call for the
  retired CIN–DET id: HTTP 200 ten hours after the final, `status: closed`,
  score 16–14, all 1,295 2way entries preserved, settled at 100/0 — the
  settle arrived as ordinary timeline entries ~20 min after the end, so a
  correction in the ended→closed window rides the existing last_updated
  dedup. Keep polling (one line: `interval_s` returns `poll_overnight_s`
  instead of `None` after the post-game window) and no book suspends;
  they price the settled 100/0 instead. The game-end policy still owns
  WHEN polling may stop (SR keeps current-season only) and settlement.
  ⚠ Verify the valuation at p=1/0 saturation before relying on it.

## What went wrong / got stuck

- **The overnight monitor died silently** (SSH stream ended without a
  completion event) — the 03:45Z evidence capture never fired, and
  journald rotation then ate everything before 01:13Z. Syslog saved it,
  but the lesson stands: an evidence capture owed at a deadline needs its
  own timer, not a reminder inside the thing that can die.
- gcloud auth expired mid-investigation (~02:20Z); resumed at ~11:28Z
  after re-login. The dark-books question sat unanswered in between.
- First reading of the dark books ("engine never suspended anything —
  zero suspend strings") was wrong in a useful way: market state is
  derived, so its absence from logs and journal proves nothing. The
  cancel timestamps, not state strings, carried the answer.

## Decisions made *(mirror into [[market-maker/decisions]])*

- None. Monitor-only session; the fix plan below is a proposal for
  George and the Thursday Edwin call.

## Questions opened / closed *(mirror into [[market-maker/open-questions]])*

- **Opened N40 — the game-end lifecycle.** Proposed fix shape: the engine
  consumes the carried `status` → journalled per-book game-final event →
  an explicit policy (suspend-pending-settlement WITH a re-open path /
  freeze at settled adjustment / reseed — the E11 call, Edwin) · the live
  staleness fuse binds only while the game is in play · the publisher
  never lets its last confirmation be mistakable for feed death (a
  retirement marker, or overnight-cadence re-offers indefinitely) · a
  terminal backstop + alarm for never-final games · two new alarms:
  "SUSPENDED (RP Invalid) > N min" and "book quoting while its bound game
  is closed".
- Noted for the app team (not an MM question): the tape missed a real
  fill's print (74.12 trade absent from Last/Day High).

## Next

- **George rules on N40's policy half** (with E11/Edwin), and on the
  immediate operational question: keep the 12 played-team books out of
  the market until settlement/reseed exists.
- **George's proposed settlement pricing captured on N40 (🟡):** post-game
  price = RP + (result − kickoff probability) × $5. The live formula
  already converges there when the settled 100/0 arrives — the
  dependencies are the N22 anchor surviving cutovers (the late-arrival
  rebase erases it) and a tie source (SR's 2way voids on a draw; N16's
  `OFFICIAL_RESULT` carries ties). He wants a proper design session on
  activity states × market states × RP lifecycle before building.
- Relay the PATR/COLT exposure + fresh-journal seed-requote warning to
  the engine session before the maker resumes (sent via the doc-sync
  session 14-08 ~11:50Z; confirm it landed).
- The two alarms from N40 are cheap and would have caught both failure
  modes — candidates for the panel workstream.

## Addendum — the publisher fix built and PR'd (14-08 afternoon)

George ruled: do the fix now, quota is not a constraint. Built on
`inplay-sportradar-service` **PR #38**
(`fix/mm-publisher-post-game-keep-polling`, cut from `main@f8c8aef`,
independent of the still-open #37):

- The settle watch polls at the LIVE rate (600 s → 2 s) — the per-minute
  journal counts had shown the 600 s watch flapping every finished
  game's book suspend/cancel/re-stand once per poll against the ~20 s
  fuse (BENG: one burst at 02:21/02:31/02:41/02:51/03:01Z).
- The window default doubles to 2 h — it must outlast the engine's
  activity flip at kickoff + ~4 h; the old 1 h missed BENG's by one
  minute.
- Past the window: OVERNIGHT cadence forever, never `None` — a tracked
  game is never retired.
- 598 tests green, ruff clean (758 on the `testing` head).
- **Deployed to TESTING (George's go, ~12:52Z):** cherry-picked onto
  `testing@daf5604` → `d492dcb`, push-triggered run 31802187471,
  landed ~12:55Z. **Verified end to end at 12:56Z**: `probability_update`
  events resumed in the engine journal for the three 08-14-dated retired
  games (71548096/104/106) plus the duplicate id, seconds-fresh.
  ⚠ Scope caveat: discovery only re-adopts games on today's schedule —
  the 08-13-dated games (CIN–DET, PIT–GB) stay feedless, so BENG, LION,
  STEE and PACK still ride seed until the engine-side N40 fix or a
  manual re-adopt. Prices on resumed books unchanged (seed), as
  predicted: the fresh journal's late-arrival rebase freezes the anchor
  at the settled value. **Production pool still runs the old code** —
  #38 into main + a prod release remains open.

Held deliberately: the MM-repo valuation test for x ∈ {1, 0} — the MM
repo was mid-ceremony (CFG-0026) under the engine session; the test is
one of N40's first build items after the ceremony settles.
