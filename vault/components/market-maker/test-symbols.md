# Market Maker — Test Symbols

> **Component:** [[market-maker/market-maker]]
> **Purpose:** The permanent `.TEST` symbol set the MM runs against while
> production simulation continues, and the Sportradar replay games that
> drive them. Companion to [[market-maker/test-plan]] — that page holds the
> test cases, this page holds the securities they run on.
> **Born:** 2026-08-08 (Rob Colucci answered **T10**; George picked the ten).

---

## 1 · The scheme — tZERO's ruling

Rob Colucci (tZERO) to George, 2026-08-08, Slack. Venue facts, gospel:

- ✅ **A test symbol is the real ticker plus a `.TEST` suffix.** Rob's
  worked example: Baltimore Ravens becomes **`IPTCRAVE.TEST`**.
- ✅ **tZERO can track the `.TEST` symbols separately,** and can create
  accounts that are **only allowed to interact with `.TEST` symbols**.
  This closes T10's user-exposure caveat at the venue, not in the app.
- ✅ **Ticker length is not a problem.** Rob asked; George confirmed for
  the Novo side. The suffix takes the symbol from 8 to 13 characters.
- ✅ **Order routing does not change.** The MPID still comes from Account1
  (FIX Tag 1). `Account1=1797733477` still hits an **IPLM** MPID. See
  [[market-maker/decisions]] `2026-08-07g`.

⚠ The MM's own code must treat `.TEST` as part of the symbol string. The
`ClOrdID` scheme hashes the security name, so a `.TEST` book mints
different order ids from its production twin by construction. The dot
lives in the *symbol*, never in the `ClOrdID` — that field still carries
no dots (see [[market-maker/parameters]], `ClOrdID scheme`).

## 2 · The ten symbols

Requested from Rob on 2026-08-08. ✎ **Provisioned — corrected 2026-08-11:**
the ten live in the gateway's 180-symbol config
(`inplay-fix-gateway-go` `internal/config/symbols.go`), and all ten
accepted a 100,000-share position transfer with a venue `UPTa`
(see [[market-maker/reference/position-transfer-ledger]] 2026-08-11) —
the OMS knows every one. ⚠ The Texans code is **`TEXS`**, matching the
production ticker `IPTCTEXS` — the `TEXA` guess below was wrong.
✎ **Quoting is LIVE (08-11 night):** MM PR #22 lets the engine mint a
`.TEST` twin of any known ticker; `supervised14` quotes all ten
two-sided and the taker trades them (first print `IPTCPACK.TEST`
6@71.66). A twin is addressable by the derived provider id
`<base sr id>.test` — the synthetic-game-day hook.

| Ticker | Team | Test symbol | Code status |
|---|---|---|---|
| BAL | Baltimore Ravens | `IPTCRAVE.TEST` | ✅ Rob's own example |
| BUF | Buffalo Bills | `IPTCBILL.TEST` | ✅ live production symbol |
| DAL | Dallas Cowboys | `IPTCCOWB.TEST` | ✅ live production symbol |
| DET | Detroit Lions | `IPTCLION.TEST` | ✅ gateway config + UPTa 08-11 |
| GB | Green Bay Packers | `IPTCPACK.TEST` | ✅ used in `MM_SECURITIES` drills |
| HOU | Houston Texans | `IPTCTEXS.TEST` | ✅ gateway config + UPTa 08-11 (✎ was `TEXA`, wrong) |
| JAX | Jacksonville Jaguars | `IPTCJAGU.TEST` | ✅ gateway config + UPTa 08-11 |
| KC | Kansas City Chiefs | `IPTCCHIE.TEST` | ✅ used in `MM_SECURITIES` drills |
| PHI | Philadelphia Eagles | `IPTCEAGL.TEST` | ✅ live production symbol |
| WAS | Washington Commanders | `IPTCCOMM.TEST` | ✅ gateway config + UPTa 08-11 |

## 3 · Why these ten teams

The constraint is not brand and not market size. A Sportradar replay only
exercises a ticker **pair**, so a team with no opponent inside the set is a
dead symbol. The ten maximise the count of replayable games between them.

Three filters ran, in this order:

1. **Sportradar must hold a recording of the game.** The simulation library
   is a fixed set of 102 NFL games, not the live schedule. Query
   `recordings(league: "nfl")` at `https://playback.sportradar.com/graphql`.
   No API key, no authentication.
2. **The recording must carry the push `events` feed AND the REST `pbp`
   feed.** Only **46 of the 102** do. Every 2023 recording lacks push
   entirely, as do 9 of the 37 from 2024. The `pbp` feed is not optional:
   the push service holds no state, so a disconnect recovers by pulling
   `pbp` (see [[architecture/integrations/t0]] §5 for the same pattern on
   the tZERO feeds).
3. **Maximise head-to-head coverage.** Exhaustive search over every
   ten-team subset of the 46 push-capable recordings.

Result: **17 replayable games**. Adding an eleventh ticker buys only one or
two more, so ten is the natural stopping point.

For comparison, the seven symbols already minted (`IPTCEAGL`, `IPTCPATR`,
`IPTCBILL`, `IPTCGIAN`, `IPTCCOWB`, `IPTCSTEE`, `IPTCJETS`) contain **one**
push-capable head-to-head game between them. Patriots, Giants and Steelers
contribute nothing at this set size.

## 4 · The 17 replay games

Every row below was live-tested on 2026-08-08: session created, `pbp`
returned HTTP 200, push `events` connected. **17 of 17 pass.**

| # | Date | Away | Home | `recordingId` |
|---|---|---|---|---|
| 1 | 2024-09-06 | BAL | KC | `95aa13a0-6538-11ef-9287-d597687b4672` |
| 2 | 2024-09-07 | GB | PHI | `9bd9a240-6538-11ef-9287-d597687b4672` |
| 3 | 2024-09-23 | JAX | BUF | `ff03c1d0-7504-11ef-9b11-d3c7126916ff` |
| 4 | 2024-09-30 | BUF | BAL | `590d9ce0-7cf9-11ef-992c-e5e63922dde1` |
| 5 | 2024-11-24 | DAL | WAS | `3f1940a0-a91d-11ef-a1c4-eb83affcc582` |
| 6 | 2024-12-06 | GB | DET | `9bff69a0-b31f-11ef-9b89-19bee9be8305` |
| 7 | 2024-12-21 | HOU | KC | `90a47140-bbb7-11ef-9d0c-27f9111c428e` |
| 8 | 2025-01-12 | GB | PHI | `341dfda0-cec3-11ef-994b-471813ef476c` |
| 9 | 2025-01-18 | HOU | KC | `370c6bd0-d375-11ef-af8f-f327a4aeb2fd` |
| 10 | 2025-01-19 | WAS | DET | `3ca38b00-d375-11ef-af8f-f327a4aeb2fd` |
| 11 | 2025-01-19 | BAL | BUF | `47cb39b0-d375-11ef-af8f-f327a4aeb2fd` |
| 12 | 2025-01-26 | WAS | PHI | `6ac9f910-d9c9-11ef-b15f-0b84f61afa9d` |
| 13 | 2025-01-26 | BUF | KC | `6e815bc0-d9c9-11ef-b15f-0b84f61afa9d` |
| 14 | 2025-02-09 | KC | PHI | `89a5edd0-e40f-11ef-98ce-93ec0f59e7f8` |
| 15 | 2025-09-05 | DAL | PHI | `ea3dfe90-88cd-11f0-be65-f306a1687f9d` |
| 16 | 2025-10-07 | KC | JAX | `e7bbe540-a2b0-11f0-a36f-911e8c41aad8` |
| 17 | 2025-10-28 | WAS | KC | `faa11330-b122-11f0-b35c-67fa195086b1` |

Games 14 and 15 are the two showcase fixtures: Super Bowl LIX (KC at PHI)
and the 2025 season opener (DAL at PHI).

## 5 · How to drive a replay

Three steps. No API key at any step.

1. **Create a session.** POST to `https://playback.sportradar.com/graphql`
   with the `createSession` mutation. The input is
   `{"recordingId": "<id>"}`. The mutation returns the `sessionId` as a
   bare string.
2. **Pull REST feeds.** GET
   `https://playback.sportradar.com/replay/nfl/{recordingId}?feed=pbp&contentType=json&sessionId={sessionId}`.
   Feed names for these recordings: `pbp`, `game`, `boxscore`, `rosters`.
3. **Subscribe to push feeds.** GET
   `https://playback.sportradar.com/subscribe/events?recording_id={recordingId}`.
   Push feed names: `events`, `statistics`, `pulse`. Push takes the
   recording id directly and needs no session.

⚠ **The replay starts at kickoff and advances in real time from the moment
the session is created.** A fresh session returns `"status": "created"`,
and the push feed sends only `{"heartbeat":{"interval":5000}}` until the
first play fires. That is correct behaviour, not a dead feed. Plan A2's
10× pace accordingly — a real-time replay of one game takes a real game's
length.

## 6 · Known bad recordings

| Game | `recordingId` | Fault |
|---|---|---|
| LAR at SEA, 2025-12-19 | `e65b2fe0-daef-11f0-9c7c-831fe5fbd838` | `createSession` returns `INTERNAL_SERVER_ERROR`. The recording lists push feeds only, with no `pbp`. Unusable. |
| DAL at NYG, 2023-09-11 | `f1910920-4d84-11ee-92bb-abdc4c841b50` | No push feed. `pbp` works; the subscribe endpoint hangs with no HTTP status. Typical of every 2023 recording. |

## 7 · Still open

| # | Item | Owner |
|---|---|---|
| 1 | ~~Confirm the four unconfirmed codes~~ ✅ resolved 08-11: `LION`, `TEXS` (not `TEXA`), `JAGU`, `COMM` — the gateway's deployed config + a venue `UPTa` on each | — |
| 2 | ~~Provision the ten `.TEST` symbols~~ ✅ done by 08-11 (gateway config; all ten accepted transfers) | — |
| 3 | Create the `.TEST`-only account, and confirm whether the MM account 1797733477 can hold both `.TEST` and production books, or needs a second account | T0 (Rob) |
| 4 | Confirm a `.TEST` symbol is exempt from the app's user-facing universe — the T10 caveat, now a venue-side entitlement rather than an app filter | T0 + us |
| 5 | Do the `.TEST` books get an `UEPR` reference price, or do they open empty? An empty book rejects every order ("No price available", the `IPTCBILL` state) — this gates whether the ten books can be quoted at all | T0 (Rob) + the Hasan `LmtPerc` ask |

Item 5 is the one that can stop the whole plan. It is the same blocker that
holds the other 163 production books — see [[market-maker/parameters]],
`LmtPerc reference`.
