---
description: Build plan for the home page rework to Edwin's Aug 8 mock — the block list, mock-to-app mapping, work order, and open questions.
---

# Home Page Rework — Plan

> **Sub-component:** [[discovery-home]] · **Component:** [[information-layer]]
> **Date:** 2026-08-09 · **Status:** Planned — first work item from the Aug 8 handoff
> **Source:** Edwin's handoff bundle (`~/Downloads/InPlay-Handoff-George/`, extracted
> from `InPlay-Handoff-George.zip`) — the front-end mock of 2026-08-08, plus the
> delta session with Claude on 2026-08-09.

---

## 1. What this is

Edwin's Aug 8 mock is his product opinion of the app, and the home page is the
surface he wants reworked first. The mock's home is **trader-first** (your money,
your teams, the movers). The scoped home ([[discovery-home]]) is **games-first**
(the day's slate). The rework merges the two: the dashboard sits on top, the
slate below.

Decisions taken in the 09-08 session:

- **Home page is the first work item.**
- **Pro / paid tier is parked** — no App Store subscription work before launch.
- The ticker already exists on other pages — home **reuses** it, no new build.

## 2. The block list (top to bottom)

New blocks come from the mock. Kept blocks come from the existing
[[discovery-home]] scope. Order follows the mock.

| # | Block | Source | Notes |
|---|-------|--------|-------|
| 1 | App bar — news, search, notifications badge | mock | Pro lock omitted (parked) |
| 2 | **Live ticker tape** | exists | Reuse the ticker from the other pages |
| 3 | **Greeting card** — avatar, daily streak, favourite teams | mock (new) | Tap a favourite team → its market |
| 4 | **Competitions block** — join fork: free (13+) vs KYC-verified cash (18+) | mock (new) | Doubles as the KYC conversion surface; both paths start with 100k IPD |
| 5 | **Trading capital card** — total equity, invested vs available, day P&L, positions | mock (new) | Pulls the Personal Dashboard essentials onto home |
| 6 | **Sponsored slot** — full-bleed rotating house-ad unit | mock (new) | House-ads-from-day-one policy already agreed (see advertising notes in [[components/components]]) |
| 7 | **Today's movers** — biggest swings, tap to trade | mock (new) | |
| 8 | **Watchlist** — editable glance list | mock (new) | |
| 9 | **IPO calendar strip** — upcoming IPOs + browse-all | mock (new) | Highest value pre-launch, while IPOs are the only action; links [[ipo-module/ipo-module]] |
| 10 | Day's-slate game cards (3 data points max) | scoped | Keep from [[discovery-home]] |
| 11 | Featured / marquee games | scoped | Keep |
| 12 | Last-game-of-the-day flag | scoped | Keep — daily-prize relevance |
| 13 | Leaderboard proximity ("112 places from cashing") | scoped | Keep |

## 3. Mock → build mapping

The mock is one React file. Every home block already exists as a named component
in it — port the anatomy, restyle to the app's system.

| Block | Mock component (`02-SOURCE/InPlayHomeV1423-SOURCE.jsx`) |
|-------|--------------------------------------------------------|
| Ticker | `Ticker` |
| Greeting card | `Greeting` |
| Competitions | `Competitions` (+ `KycSheet` join flow) |
| Trading capital | `Portfolio` |
| Movers | `Movers` |
| Watchlist | `WATCHLIST` list + team tiles |
| IPO calendar | `IpoCalendar` |
| App bar | `AppBar` |

## 4. Walkthrough hook (build in from day one)

The mock's home coach tour anchors on `data-coach` attributes
(`ticker` · `profile` · `fork` · `capital` · `movers`). Add the attributes to
the new blocks **as they are built** — the tour overlay lands later as its own
small feature. First-time-only gating: `localStorage` flags for v1; a
`tours_seen` JSON field on the user profile as the proper version (one column,
no new tables). Tour copy is already written in the mock.

## 5. Order of work

1. Layout skeleton + ticker reuse + app bar.
2. Blocks with existing data: movers, watchlist, day's-slate cards, IPO calendar.
3. Blocks that need profile/account data: greeting (streak, favourites),
   trading capital card, competitions fork.
4. Sponsored slot (house-ad unit).
5. `data-coach` anchors throughout, then the walkthrough overlay as a follow-up.

## 6. Open questions

- **Data:** does the backend already hold daily streak and favourite teams?
  Movers needs a change-ranking source. IPO calendar needs the IPO schedule feed.
- **Ownership:** the app is the platform team's build — confirm who implements
  which blocks (us vs Hasan's side).
- **Edwin's sign-off:** the block list above is read off his mock; confirm the
  order and whether anything on the current home must survive that the mock drops.

## 7. Out of scope (parked)

- Pro / paid tier, paywall, ad-free — App Store subscription work post-launch.
- Replay/backtest desk and fair-value overlay (Pro features).
- Gamecast updates — **next in the queue after home**: pregame Opening Line
  card, live value-breakdown strip, re-rate/injury event cards, divergence
  callout. Blocked on the pricing engine publishing the per-play decomposition
  (Edwin's `snap()` contract) — same conversation as the pricing frictions
  (see the delta session 09-08 and `SHOWCASE.html` in the handoff folder).
