# 2026-08-08b — T10 falls: permanent `.TEST` symbols, and the ten teams that can actually be replayed

> **Who:** George + Claude (George: pick 10 NFL teams for test tickers,
> constrained by what Sportradar can simulate; then Rob answered)
> **Type:** research → venue answer → vault record
> **Refs:** decisions `2026-08-08c` · [[market-maker/test-symbols]] ·
> open-questions T10 · Rob Colucci Slack thread 08-08

## What we did

1. **Enumerated Sportradar's actual NFL simulation library** —
   `recordings(league: "nfl")` at `https://playback.sportradar.com/graphql`,
   no auth. **102 recordings**, a fixed set, nothing to do with the live
   schedule.
2. **Filtered to what the MM can actually consume,** then ran an exhaustive
   search for the ten-team subset with the most head-to-head games.
3. **Live-tested every candidate game** — create session, pull `pbp`,
   connect the push `events` stream.
4. **Rob answered T10 in the same thread** with the `.TEST` scheme, and
   George requested the ten symbols.
5. **Wrote the registry** ([[market-maker/test-symbols]]) and updated
   decisions, open-questions, parameters and the test plan.

## What we learned

- ⭐ **Only 46 of the 102 recordings carry the push `events` feed.** Every
  2023 recording has none, and neither do 9 of the 37 from 2024. Scoring
  team sets against the whole library overstates coverage by roughly 2×.
  The MM needs `pbp` alongside push — push holds no state, so a disconnect
  recovers by pulling `pbp`.
- **The right selection criterion is pair coverage, not brand.** A replay
  drives a ticker *pair*. A team with no in-set opponent is a dead symbol.
  This is why the seven already-minted symbols only yield **one**
  push-capable game between them, and why PATR, GIAN and STEE contribute
  zero at a set size of ten.
- **Ten is the natural stopping point.** The chosen ten give 17 games; an
  eleventh ticker adds only 1–2. Marginal return collapses immediately.
- **The replay clock starts at session creation and runs at real time.** A
  new session reads `"status": "created"` and the push feed emits only
  heartbeats until the first play. This looks exactly like a dead feed and
  is not one.
- **Two recordings are genuinely broken or unusable** — LAR at SEA
  2025-12-19 (`createSession` → `INTERNAL_SERVER_ERROR`) and every 2023
  game for push purposes. Both recorded in the registry §6.
- **T10's real unlock is the account entitlement, not the suffix.** Rob can
  entitle an account to `.TEST` symbols only. That is what makes the
  symbols *permanent* rather than a pre-launch window, and it moves the
  user-exposure problem off the app and onto the venue.

## What went wrong / got stuck

- **Scored the first two team sets against all 102 recordings** before
  checking the `apis` field per recording. The 32-game and 56-game figures
  quoted to George were wrong for the actual requirement; corrected to 17
  once the push filter went in. The lesson is the general one: the feed
  list is per-recording metadata, not a library-wide property — check it
  before counting anything.
- **Also asserted a DAL at NYG game as usable** on metadata alone. Its push
  endpoint hangs with no HTTP status. Caught by live-testing, which is now
  the standard before a recording enters the registry.

## Decisions made

- Recorded in decisions `2026-08-08c` — the `.TEST` scheme, the ten teams,
  the 46-of-102 push finding, the four unattested codes, the `UEPR` caveat.

## Questions opened/closed

- **T10 — scheme ✅ CLOSED, provisioning 🟡 open.** Four follow-ups filed on
  the row: the unattested codes, the `.TEST`-only account shape, the app
  exemption, and the `UEPR` reference-price question.
- **No new Edwin items.** Nothing here touches the valuation side.

## Next

1. **Send Rob the four unattested codes for confirmation** — `LION`,
   `TEXA`, `JAGU`, `COMM` — and ask the three provisioning questions in
   [[market-maker/test-symbols]] §7. Nothing hardcodes a symbol until they
   come back.
2. ⚠ **Ask the `UEPR` question in the same message.** If the ten `.TEST`
   books open empty they reject every order, and the whole test matrix is
   dead on arrival. This is the same blocker as the 163 production books,
   so the answer is worth having either way.
3. Unchanged from `2026-08-08`: the reject-backoff build stays TOP, then
   the Hasan message, then the Edwin round.
