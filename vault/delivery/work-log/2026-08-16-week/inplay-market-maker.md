---
description: "Weekly engineering record for the market maker, 09-16 August 2026 — 147 commits, the CA/CB numbered fix set that closed the live-game defects, and the SNT-1 taker agent"
service: inplay-market-maker
window: 2026-08-09 .. 2026-08-16
commits: 147
authors: { westy412: 147, Hxsan: 0 }
branches: { touched: 43, merged: 40, open: 3 }
---

# inplay-market-maker — week of 09–16 August 2026

> **Delivery:** [[delivery]] · **Week:** [[work-log-2026-08-16]]

## Headline

**The market maker spent the week on correctness, not on new features.**

- A planned programme of six numbered fixes — the CA/CB fix set — closed the defects
  that the 13/14 August live games exposed
- The engine keeps a game's opening price across a restart
- It refuses to cross a live market, and it heals its own orders at boot
- It processes venue messages about **28 times faster**
- The taker agent SNT-1 gained a one-second quote rate for live games, and a fix for a
  defect that silenced one side of a book for good

## Scope

- **Window:** 2026-08-09 to 2026-08-16
- **Commits:** 147 (westy412 147, Hxsan 0). One of the 147 carries the git author
  `deploy` (`8cca392`, a deploy bot commit on George's branch).
- **Branches touched:** 43 — 40 merged, 3 still open. "Touched" means the branch
  tip moved inside the window.
- **Busiest day:** 2026-08-15 (55 commits)

Three notes on the count.

1. **Ten git worktrees share this one repository.** The count above comes from one
   `git log --all` at the main repository path. It is not multiplied.
2. **The count was 146 when this file's work started.** Commit `e1d7a80` landed on
   `chore/drill-observability` at 19:10 on 2026-08-16, inside the window.
3. **`origin/dev` and `origin/testing` stand at `a3e9d31`, dated 2026-08-07.**
   - No work this week reached either branch
   - A `git fetch` was not permitted, so these refs are as recorded on disk

**The worktree layout is itself the story of the week.**

- George ran fix branches in parallel, each in its own checkout
- Two agents in one checkout had already broken a session (`progress.md`, Phase 1 issues)
- `inplay-mm-ca3-salvage` exists because a build agent died after it pushed. Commit
  `62c5d96` recovers that agent's lost work.

The ten worktrees:

| Path | Branch |
|---|---|
| `inplay-market-maker` | `fix-set/ca1-anchor-seed` |
| `inplay-market-maker-boundary` | `feat/converger` |
| `inplay-market-maker-hotfix` | `main` |
| `inplay-market-maker-qty-variation` | `feat/qty-increment-100` |
| `inplay-market-maker-taker-rate` | `feat/snt-live-rate` |
| `inplay-mm-ca3-salvage` | detached at `8bb20a4` |
| `inplay-mm-drill-obs` | `chore/drill-observability` |
| `inplay-mm-taker-wedge` | `fix/snt-wedge-and-loss-budget` |
| `mm-wt-freshness-guard` | `fix/post-game-on-final` |
| `/private/tmp/.../scratchpad/step4b` | `feat/always-quoting-step4b` |

## Themes

### 1. The CA/CB fix set — the planned programme that ran the week

**Why it matters** — the 13/14 August live games exposed six defects. One spec turned
them into a numbered programme, and every chunk of it merged.

**How the chunks are named**

- **CA is Stream A, correctness. CB is Stream B, performance.** Both streams are one
  spec: `specs/2026-08-14-mm-python-fix-set/spec.md`
- The number is the chunk within the stream
- George wrote the spec on 14 August, after the 13/14 August live games
- The chunk ids exist so two agents can build in parallel without a shared file
- The spec's own name for the goal is "Python done": fix everything, pin the Python
  engine as the reference, then port it to Go

The spec names six defects, F1 to F5 plus one out of scope. The chunks map to them:

| Chunk | Spec item | What it fixed | Branch | State |
|---|---|---|---|---|
| P0b | dictionary | All new configuration rows land once, with defaults | `phase0/fix-set-dictionary-batch` | merged |
| CA1 | F2 | Kickoff anchors survive a fresh journal (`ANCHOR_SEED`) | `fix-set/ca1-anchor-seed` | merged |
| CA2 | F3 / R-Q09 | The engine never publishes an order that crosses the live market | `fix-set/ca2-marketable-guard` | merged |
| CA2b | F3 follow-up | A refused book still sends its cancels; the examined-books cap | `fix-set/ca2b-refusal-path` | merged |
| CA3 | F3 / R-Q08 | Resize the ask ladder to what the account may legally sell | `fix-set/ca3-ask-cap` | merged, INERT |
| CA4 | F4 / R8 | At boot, cancel venue orders that our record does not know | `fix-set/ca4-boot-healer` | merged |
| CB1 | F1a | Tick-time measurement plus the six-game test workload | `fix-set/cb1-profile-workload` | merged |
| CB2 | F1b | De-phase the 500 ms quote pulse per book | `fix-set/cb2-pulse-dephase` | merged, UNWIRED |
| CB4 | F1c | Cut the cost of one venue message | `hotfix/prune-index-main`, `fix-set/cb4-measurement-integrity` | merged |
| CB3 | F1b | Incremental sweep | not built — shrunk behind CB4 (George, 15-08) |
| F5 | merge train | Make `main` equal the running code | `feat/always-quoting-step4b` | merged |

Every chunk landed on `origin/main`. Four results are worth naming.

**CA1 — the anchor** · `07e47e8` · `fix-set/ca1-anchor-seed` · merged `origin/main`
- **Symptom** — on the 13 August game the engine froze IPTCBENG at 0.866, not at the
  23:03Z anchor 0.711
- **Cause**
  - every maker deploy took a fresh journal
  - an engine that restarted mid-game therefore lost the kickoff freeze
  - it then re-froze the reference price at the current probability
- **Fix**
  - the engine reads the prior run's directory once at boot
  - it writes ONE `ANCHOR_SEED` event first
  - the anchors are then an ordinary journalled fact, so replay reproduces them
- **Evidence** — the miss cost $0.685 a share on that game, and up to $5 a share in
  the regular season

**CA2 — the marketable guard** · `f358acf` · `fix-set/ca2-marketable-guard` · merged `origin/main`
- **Symptom** — on 9 August a COWB bid at 76.04 swept eight levels, 920 shares,
  $50,366. The market maker took liquidity while it intended to rest.
- **Cause** — the engine prices from its own valuation and never from the venue book,
  so its bids crossed stale third-party asks on every repost
- **Fix** — the converger asks one question per book before the first order registers
  - the question: does any order price at or through the live opposite touch, net of
    our own resting quantity?
  - yes means the whole batch waits
  - the guard fails open on absent or stale data. A refusal on missing data would
    silence quoting.

**CA4 — the boot healer** · `e195b2f` · `fix-set/ca4-boot-healer` · merged `origin/main`
- **What** — at boot the engine reads the gateway's live MM order index
  - the healer cancels only orders that match our own ClOrdID scheme and are unknown
    to our record
  - the healer never touches the taker's `MMSN` orders
  - the healer writes no engine state at all
  - every consequence arrives later as an ordinary journalled venue event, which is
    what keeps replay equality true
- **Why** — this retires the fresh-journal-per-deploy ceremony for the maker

**CB4 — one function was 94% of the cost** · `4d75550` · `hotfix/prune-index-main` · merged `origin/main`
- **Symptom** — CB1's profile measured the venue message drain at 98.1% of tick time
  (`5fb71e2`)
- **Cause** — `VenueEngine._stamp_and_prune` walked every order in every book on every
  venue message, and parsed each dead order's timestamp
- **Fix** — two derived indexes replace the scan
- **Evidence**
  - measured over 600 messages while 18,552 orders were held
  - that one function was 94.3% of the whole path, at 17,001
    `datetime.fromisoformat` calls per message
  - cost per message at the production shape falls about 28 times, and the curve is
    flat instead of linear

**Where the fix set stands**
- All chunks are merged
- The GATE chunk — the final measurement — is written up in
  `specs/2026-08-14-mm-python-fix-set/gate-v2-results.md`
- Its verdict is split. The miss-rate clause of AC4 passes at 0.0000% on both arms.
- The zero-`DRAIN_CAPPED` clause fails as written: 7 capped ticks, all at the boot
  re-stand
- The one live observation night is still owed. The spec is not complete.

### 2. Always-quoting: the converger, and `main` became the running code

**Why it matters** — before 14 August, `main` was not the code that ran in production.

**The merge**
- The running lineage was `feat/always-quoting-step4b`, fed by `deploy/g2-union` and
  `deploy/g2-union-converger`
- George merged that lineage into `main` on 14 August (`7b43808`)
- That merge is the fix set's F5 requirement

**The always-quoting series** — built 12–14 August against measured live incidents.

- **Bounded drain** (`f91a264`, `feat/bounded-drain`) — each tick stops at a cap. A
  flooded queue now delays quotes by ticks. It no longer starves the heartbeat.
- **Group commit** (`f8c7f2b`, `feat/group-commit`) — one disk sync per tick instead
  of one per event
  - the per-event sync was the measured throughput ceiling at about 579 events a second
  - an NCAA Saturday needs about 2,520
- **The progress-aware heartbeat** (`d5180eb`, `feat/progress-beat`) — the beat now
  certifies that a tick completed, not that the scheduler ran
  - a loop that is alive but stuck goes silent, so the gateway's dead-man pulls the book
- **The budgeted converger** (`11c1d37`, `deploy/g2-union-converger`) — quote cycles
  stage a target; one paced pass per tick sends at most 256 instructions in priority order
  - this fixed the chain measured on supervised21
  - a burst of venue messages caused a missed sweep
  - the missed sweep then drove the whole portfolio to a defensive state, on 11.5% of ticks
- **The converger on its own task** (`912ba27`) — the tick stages, a separate task
  converges every 0.25 s
- **The single-engine lock** (`8cab9cf`) — on 13 August two engines quoted the same
  account for about 2.5 hours and nothing refused
  - an exclusive file lock now makes the second engine refuse to start
- **Bounded working memory** (`a6e2307`, `feat/session-boundary`) — dead orders now
  leave working memory after 300 s
  - after four hours the live engine held 1,007,387 duplicate-detection keys (193 MB)
  - it also held 492,091 venue orders (92 MB), of which 99.7% were dead
  - growth was about 68 MB an hour
- **The session clock and forked checkpoints** (`9169a4d`)
  - the hourly 344 MB checkpoint froze the trading loop for about 22 s
  - separately, the venue's silent session roll left about 750 phantom orders
  - those orders drew 61,000 rejects an hour, for eight hours

**Two configuration rulings ride the same lineage.**
- `845ee7e` restored the miss tolerance to 1.0 s
- `57765ff` (`hotfix/sweep-tolerance-2s`) raised it to 2.0 s before the 14 August games
- Both are George's rulings, recorded in the commit

### 3. Quote freshness at the end of a game

**Why it matters** — the outcome of the game is known, so the true price is 100 or 0.
Any resting order at a game-time price is free money for whoever takes it.

Two branches closed the two halves.

**`fix/freshness-settled-guard`** · `1afc9a3` · merged `origin/main`
- **Symptom** — all six books suspended 20 s after the publisher's post-game watch
  expired
- **Cause**
  - SportRadar serves a settled probability for minutes after the whistle
  - the engine set `live=False` on the official result
  - the next echo of that same settled reading re-armed the live freshness regime
    unconditionally
- **Fix** — the freshness state now pins the final to its own game id, so a matching
  reading updates the timestamp only
- **Evidence** — measured on 15 August, verified in the journal

**`fix/post-game-on-final`** · `749431e` · merged `origin/main`
- **Symptom** — the post-game state arrived 40 minutes late, or never
- **Cause** — the official result's `provider_event_time` is the stamp of the last
  reading that moved the probability, which on a settled game is hours earlier
- **Fix** — `final_time` now takes the receipt time. George ruled that the book
  switches to post-game when the game IS finished.
- **Evidence**
  - two measurements from 15 August
  - a final that arrived at 23:14 carried the stamp 22:33, so 40 minutes of the
    one-hour post-game window was already spent
  - another carried 17:05, so the post-game state never appeared at all
  - the fix is journalled, so replay reproduces it

> Both branches are the engine half of N40. The publisher half lives in
> `inplay-sportradar-service` and is not in this repository.

### 4. The taker agent SNT-1

**Why it matters** — SNT-1 is the taker. It sends orders that cross the spread and take
liquidity, in contrast to the maker, which rests orders.

**Most of the taker was built this week.**

- **The float and the sell gate** (`7e2b54d`, `feat/snt-1-float-and-sell-gate`)
  - the account's holding is a configured float plus the fills the taker saw
  - a $25,000 notional cap per order, and a journalled kill switch
- **Position reconciliation** (`2de7775`, T-S05) — the gateway publishes the venue's
  own account size per symbol. A mismatch that survives a grace window halts the bot.
- **The ClOrdID prefix** (`20f6a51`) — the gateway rejects non-MM order ids on its
  namespace, so taker ids are now `MMSN` plus 14 hex characters.
- **Shorts** (`f14cece`, `feat/snt-shorts`) — the sell gate extends rather than
  inverts. A book never straddles zero. Off by default.
- **The wash guard** (`4d549b3`, `feat/snt-wash-guard`) — the venue's per-account wash
  check is on, and fired when an arrival crossed the taker's own unfilled remnant
  - the remnant now blocks the opposite direction bot-side
- **The boot rebase** (`db45300`) — a gateway restart can swallow an execution report,
  so the taker's next boot carried a stale float and halted mid-game
  - the first execution-borne venue figure per book may now be adopted

Two branches merged on 15 August matter most.

**`feat/snt-live-rate`** · `5eb4a6b` · merged `origin/main`
- **Symptom** — Edwin said the taker was "not quick enough during live games"
- **Fix**
  - George ruled one print per book every 20 s before kickoff, every 1 s in a live
    game, and every 20 s after
  - the commit also fixed a biased arrival clock that added about half a tick to
    every gap
- **Evidence** — the arrival clock bias was +27% at a one-second target

**`fix/snt-wedge-and-loss-budget`** (`3091060`) — a real incident, found in the live
logs the same afternoon the one-second rate deployed. See "Notable fixes" below.

### 5. Observability: the state publishers and manual orders

**Why it matters** — the state payloads are what the admin panel reads. Any change to
their field lists is a change the panel sees.

**`feat/state-publishers-manual-orders`** · 20 commits, 12–13 August · merged `origin/main`
- **What** — Requirements R1 to R3 of `specs/2026-08-12-admin-trading-observability`
- It is the largest single branch of the week
- The maker publishes a complete projection of its own state on the subject `mm.state`
  about once a second (`4d0330f`)
- The taker publishes on `snt.state.{botId}` from its own task, so a halted bot keeps
  publishing (`f1a3b65`)
- Manual orders arrive on `snt.control.snt-1`: place, cancel and replace, with a
  quantity guard, a ±20% price collar and a notional cap (`fd78132`, `ef76d17`)

**An internal review then found three defects in that work.**
- All three are fixed on the same branch (`80a33ef`, `2fa09d1`, `c264dd9`)
- `2fa09d1` is the most serious
  - the engine tracked, journalled and acknowledged a manual order BEFORE the message
    reached the wire
  - a failed publish therefore reported an order as landed when it never left

### 6. Quote shape: the quantity grid and the live pulse

**Why it matters** — three rulings from George changed what the book looks like on
screen.

**The quantity grid** · `b07ae28`, `e8e1003` · `feat/qty-increment-100` · merged `origin/main`
- **Symptom** — every displayed size was a multiple of 500. The touch therefore had
  eleven possible sizes, and all of them ended in 000 or 500 — the machine-generated tell.
- **Fix**
  - `b07ae28` cut the grid to 100 shares
  - `e8e1003` then dropped it to 1, because George ruled that ANY visible grid reads
    as an inactive book
  - the rounding step stays in the code, so one configuration row restores any grid

**Live timer quoting** · `6ab57a5` · `feat/live-timer-quoting` · merged `origin/main`
- **What** — in a live game the book publishes a re-rolled ladder every 500 ms,
  whether the price moved or not
- The tick and the sweep both moved to 0.5 s

**The dwell table as the republish clock** · `f623222` · `feat/per-mode-republish-timer` · merged `origin/main`
- **What** — every mode republishes when its drawn dwell expires
- **George's ranges** — live 0–0 s, pre-game 5–20 s, post-game 5–20 s, overnight 20–40 s

## Notable fixes and incidents

**The taker wedge — one side of a book silent for good** · `3091060` · merged `origin/main` via `0b9f601`
- **Symptom** — one wedged sell skipped EVERY buy on that book. The book traded one
  side, drained its inventory, then went silent.
- **Timeline** — found in the live logs on 15 August, the afternoon the one-second
  rate deployed
  - 18:48 — IPTCPANT wedged with a sell of 36 at 55.28, against a market near 54
  - its holding fell 4,133 to 36, with zero fills for over 14 minutes
  - 19:03 — IPTCBILL wedged, and was dead for 9 minutes
- **Cause**
  - the taker sent ONE cancel 1.5 s after an order, then latched a flag
  - the order left the live map only on a terminal venue event
  - a cancel that was lost or never answered therefore left the order in the live map
    for ever
  - the wash guard reads that map
- **Fix** — the fix re-arms the cancel every 2.0 s while the order is live, counts
  attempts, and raises a `CANCEL STUCK` alarm at five attempts
- **Evidence** — across the session, 6% of live-book minutes had a side missing and
  2% were fully silent

> The commit states it was not deployed.

**The measurement read the wrong tree** · `b72dee5` · `fix-set/cb4-measurement-integrity` · merged `origin/main`
- **Symptom** — every profile run on the test rig loaded the same engine source,
  whatever worktree started it
- **Cause**
  - the workload script put the repository ROOT on `sys.path`
  - the project uses a `src/` layout, so `import mm` never resolved there
  - it fell through to a copied virtual environment, whose path pointed at one fixed tree
- **Evidence** — CB4's whole before-and-after measurement set was before against
  before. Nothing errored and the numbers looked reasonable.
- **Fix** — the profile output now records which engine path it loaded, and whether
  the fix is present

> This voided a set of published figures in both directions.

**The test workload was 45% too light** · `1567c93` · `fix-set/cb1-profile-workload` · merged `origin/main`
- **Symptom** — the arm ran about 6,950 messages against about 12,350 at equal speed
  and duration
- **Cause**
  - the script computed a game's feed start time twice, and the two copies disagreed
  - every reading of every game therefore carried a timestamp 60 s in the future, for
    the whole run
  - the book's own clock rule then pinned the twelve game books ahead of the runtime's
    clock, and they stopped redrawing on the pulse
  - nothing raised, no counter moved
- **Fix** — George ruled a re-cut, not a caveat. The workload is renamed `six-game-v2`,
  so a v1 result can never compare equal to a v2 one.

> Every absolute v1 baseline is under-loaded.

**Live and replay disagreed on `main` (N45)** · `88deb0f` · `fix/n45-pending-exposure-replay` · merged `origin/main`
- **Symptom** — live asks read `[9956, 7168, 5161, 3716]` against replay
  `[10000, 7200, 5184, 3732]` on NFL-DAL
- **Cause**
  - the venue engine registered an order at converge time
  - nothing journalled that call, and replay never re-drives converge
  - a pending order therefore counted into the exposure sum on the running engine, and
    nowhere in a replay
- **Evidence** — the defect stayed latent while the quantity grid was 500. It became
  constant once `feat/qty-increment-100` set the grid to 1.
- **Fix** — the exposure sum now counts only states a replay can reconstruct

> The grid change exposed the defect; it did not create it.

**The examined-books cap starved the converger, twice** · `fix-set/ca2b-refusal-path` · merged `origin/main`
- **Symptom** — CA2b added a cap on how many books one pass may examine. Two versions
  of that cap starved the converger.
- **Cause**
  - the first version charged suspended books, which run first, re-stage every cycle,
    and yield no instructions
  - about 100 suspended books therefore spent the whole cap, and NO live book ever
    converged (`c50e7ba`)
  - the second version shared one counter between the live class and the rest. Enough
    refused live books meant the rest were never examined at all (`37811d3`).
- **Evidence** — a probe reproduced both defects before the fix
- **Fix** — the same commit chain also found that the live class had no rotation at
  all (`41eddf9`)

> The missing rotation was a latent starvation risk. It became reachable only once a
> book could stay on the dirty list.

**A gateway restart killed the engine** · `fix/cancel-reject-drain` · merged `origin/main`
- **Symptom** — on 10 August a gateway restart dropped the FIX session, and the engine
  raised and died (`eceaf26`)
- **Cause**
  - a foreign order on the shared MM user id died unacknowledged
  - its cleanup cancel drew an unknown-order cancel-reject
  - a second shape of the same crash followed: a terminal message for an untracked
    order can carry no symbol at all (`658dc02`)
- **Fix** — both now count, log and skip. Every other unknown-order path stays fatal.

**A drill destroyed committed fixtures** · `d916133` · merged `origin/main`
- **Symptom** — a plain run of the replay drill destroyed committed fixtures
- **Cause** — the drill deletes its scratch directory at start, and its default pointed
  at `scripts/a2-run/`, whose files are tracked in git
- **Fix** — the default moves outside the repository, and the clear step refuses any
  path inside it

**A reverted change with no recorded reason** · `d7d2a3c` · `feat/inverted-size-ladder`
- **What** — the branch inverted the size ladder to put the least inventory at the touch
- **Timeline**
  - it merged as `e8d1462`
  - `b86ca83` reverted it 21 minutes later
- **Evidence** — none recorded. The revert commit carries no explanation, and
  `docs/BUILD-LOG.md` has no entry for either.
- **Where the code stands** — it holds the original shape
  (`base_i = 10,000 × 0.72^i`, i = 0 at the inside)

> **I could not determine why it was reverted.**

## Still open

Three branches are unmerged. Two of them are superseded copies, not lost work.

- **Superseded, not abandoned** — `fix-set/cb4-drain-speed`, 5 commits, last 2026-08-15
  - all five commits are patch-identical to commits that reached `origin/main`
  - those twins reached `main` through `hotfix/prune-index-main` and
    `fix-set/cb4-measurement-integrity`
  - verified with `git patch-id`
  - nothing on this branch is missing from `main`. It can be deleted.
- **Superseded, not abandoned** — `feat/converger`, 3 commits in the window, last
  2026-08-13
  - `9e9257b` is patch-identical to `845ee7e` on `main`
  - `ea83eac` is the single-engine lock, whose clean copy is `8cab9cf` on `main`
  - `f833d50` makes the same configuration change to `src/mm/config/dictionary.py` as
    `845ee7e`, verified identical
  - `f833d50` also committed about 167,000 lines of test-rig journal output under
    `scripts/a2-run/`
  - the clean commit is the one that reached `main`. Do not merge this branch.
- **In flight** — `chore/drill-observability`, 1 commit, `e1d7a80`, 2026-08-16 19:10
  - it landed during the writing of this file
  - the drill now writes a `.drill-in-progress` marker, so a cleanup sweep cannot
    delete a worktree that a running drill is reading
  - it also records three operating lessons
  - it has no PR merge on `origin/main` yet

Two further items are merged but deliberately not active.

- **Built, wired and INERT** — `fix-set/ca3-ask-cap`
  - the ask cap needs the account's real opening position per book
  - the current input is a single global value of 0. The code reads that as UNKNOWN,
    so the bound fails open and logs `ASK_CAP_UNBOUNDED` once at boot.
  - enforcement at the stub would take every book bid-only on the first tick after a
    cutover
  - this is escalation N43, and it needs George's deploy input
  - `progress.md` records two further design gaps behind it
    - the first is the order in which the converger sends cancels and new sells
    - the second is that one global number cannot express about 180 per-book holdings
- **Merged but UNWIRED** — `fix-set/cb2-pulse-dephase`
  - CB2 measured its own premise and found it false. Live books already run on
    independent phases.
  - the gate metric is also invariant under any phase offset
  - the branch ships the phase module, 20 tests and the evidence
  - George withdrew requirement R2 on 15 August
  - this is a recorded clean negative, not a failure

## Cross-service dependencies

The market maker consumes data from `inplay-sportradar-service` and trades through
`inplay-fix-gateway-go`. This week's changes cross both boundaries.

**On `inplay-fix-gateway-go`:**

- **The boot healer needs a gateway route** — `fix-set/ca4-boot-healer` cannot work
  without `GET /orders/mm`, gated by `X-Ops-Key`
  - `e195b2f` records that route as gateway PR #5, live in gateway `main@a41e540`
  - if that route is absent, the healer reports a reason and the engine boots as before
- **The marketable guard reads `market.book.{symbol}` from the gateway**
  - the gateway setting `TZERO_MD_BOOK_SYMBOLS` must cover the maker's universe
  - otherwise the guard has no opinion and sends
- **The stall alarm** — `MARKETABLE_GUARD_STALLED` tells the operator to call
  `POST /md/book-resubscribe` on the gateway first
- **The taker reconciler** — it reads FIX tag 9383 from the execution report,
  forwarded as `posSize` by gateway PR #3 (`7b32922`)
- **The ClOrdID namespace** — the gateway enforces the MM prefix on
  `gateway.orders.mm.*`, which is why taker ids are `MMSN` plus 14 hex (`20f6a51`)
  - the maker and the taker share that namespace
  - the boot healer depends on the two schemes staying distinct
- **The healer's budget** — the gateway's dead-man timer and its 30 s boot grace bound it
- **A gateway restart on 10 August killed the engine twice** (`eceaf26`, `658dc02`)

**On `inplay-sportradar-service`:**

- **The ingestion switch** — `feat/ingestion-switch` (`debf1ef`) wires the durable
  `SR_PROBABILITIES` subscription in any mode, behind `MM_READINGS=bus`
- **The taker's activity state** — the taker derives each book's activity state from
  the service's `sr.probabilities.reading.>` feed (`623c761`)
  - that feed carries kickoff, status and both competitor ids
- **Taker freshness** — it prices the publisher's `Fetched-At` header, not the delivery
  time (`7b32922`). A reading without that header earns no freshness.
- **The N40 split** — `fix/freshness-settled-guard` and `fix/post-game-on-final` are
  the ENGINE half
  - the publisher half is service PR #38, and ships with the service's own release
  - the spec places it out of scope for this repository
- **The 500 ms in-game poll rate** — service PR #15 (`6ab57a5`)

**On `inplay-admin-panel-trading`:**

- **The panel's data source** — the subjects `mm.state` and `snt.state.{botId}`. Their
  field lists come from `specs/2026-08-12-admin-trading-observability` R1 and R2.
- **One unfixed mismatch** — `f1a3b65` records it. R2 puts `activity_state` at the top
  level as one value for the bot, but the build derives it PER BOOK.
  - the panel cannot see which books are live
- **A fresh journal directory** — it resets `realized_pnl_total` and drops the
  manual-order duplicate detection
  - that is why the panel labels the accumulation origin (`5312dd4`)

## Branches

Merged branches first, most commits first, then open branches.

| Branch | Author | Commits | Merged into | Purpose |
|---|---|---|---|---|
| `feat/state-publishers-manual-orders` | westy412 | 20 | `origin/main` | Maker and taker state publishers, manual orders (observability spec R1–R3). |
| `deploy/g2-union` | westy412 | 7 | `origin/main` | The 12–13 Aug deploy set: bounded drain, group commit, progress beat, session clock. |
| `feat/always-quoting-step4b` | westy412 | 7 | `origin/main` | The running lineage; merged into `main` on 14 Aug as fix-set F5. Holds one deploy-bot commit. |
| `fix-set/ca3-ask-cap` | westy412 | 7 | `origin/main` | CA3: resize the ask ladder to the sellable holding. Built, wired, INERT. |
| `fix-set/ca2b-refusal-path` | westy412 | 7 | `origin/main` | CA2b: cancels go through a refusal; the examined-books cap and its fairness fixes. |
| `fix-set/ca1-anchor-seed` | westy412 | 6 | `origin/main` | CA1: `ANCHOR_SEED` — kickoff anchors survive a fresh journal. |
| `fix-set/ca4-boot-healer` | westy412 | 6 | `origin/main` | CA4: cancel unknown own-scheme orders at boot; retires the fresh-journal ceremony. |
| `fix-set/cb1-profile-workload` | westy412 | 6 | `origin/main` | CB1: tick-time measurement and the six-game workload. |
| `feat/snt-1-float-and-sell-gate` | westy412 | 6 | `origin/main` | Taker: float, sell gate, position reconciliation, kill switch, deploy artifacts. |
| `fix-set/cb4-measurement-integrity` | westy412 | 4 | `origin/main` | CB4: the `sys.path` fix plus the scan-cost and rig-scale replay harnesses. |
| `fix-set/ca2-marketable-guard` | westy412 | 4 | `origin/main` | CA2: the pre-flight guard against publishing into the live opposite touch. |
| `fix-set/cb2-pulse-dephase` | westy412 | 4 | `origin/main` | CB2: the per-book pulse phase. Merged UNWIRED; a measured clean negative. |
| `feat/ingestion-switch` | westy412 | 4 | `origin/main` | `MM_READINGS=bus` wires the durable `SR_PROBABILITIES` subscription. |
| `fix/reject-backoff` | westy412 | 4 | `origin/main` | A rejected instruction retries on a schedule, not at sweep cadence. |
| `fix/snt-wedge-and-loss-budget` | westy412 | 3 | `origin/main` | Taker: the lost-cancel wedge; env-tunable loss budget and spread gate. |
| `feat/snt-live-rate` | westy412 | 3 | `origin/main` | Taker: one print a second in a live game; the arrival clock fix. |
| `hotfix/prune-index-main` | westy412 | 3 | `origin/main` | CB4's prune index — the 28× cut in cost per venue message. |
| `feat/qty-increment-100` | westy412 | 3 | `origin/main` | Quantity grid 500 → 100 → 1. |
| `feat/snt-wash-guard` | westy412 | 3 | `origin/main` | Taker: never send against an own resting remnant. |
| `feat/inverted-size-ladder` | westy412 | 3 | `origin/main` | Inverted size ladder — merged, then reverted the same day. Reason unrecorded. |
| `fix/cancel-reject-drain` | westy412 | 3 | `origin/main` | Drain a cancel-reject or a no-symbol terminal ack for an untracked order. |
| `fix/post-game-on-final` | westy412 | 2 | `origin/main` | Post-game starts at the final's receipt, not the probability stamp. |
| `fix/freshness-settled-guard` | westy412 | 2 | `origin/main` | A settled echo must not re-arm the live freshness regime. |
| `fix/n45-pending-exposure-replay` | westy412 | 2 | `origin/main` | N45: the exposure sum counts only journal-reconstructable states. |
| `hotfix/sweep-tolerance-2s` | westy412 | 2 | `origin/main` | Sweep tolerance 1.0 → 2.0 s before the 14 Aug games. |
| `deploy/g2-union-converger` | westy412 | 2 | `origin/main` | The budgeted converger (always-quoting step 4 phase A). |
| `feat/snt-hardening` | westy412 | 2 | `origin/main` | Taker: freshness prices the fetch; reconcile against tag 9383. |
| `docs/taker-operating-lessons` | westy412 | 2 | `origin/main` | SNT-1 operating lessons from the 11 Aug incident chain. |
| `feat/per-mode-republish-timer` | westy412 | 2 | `origin/main` | The dwell table is the republish clock in every mode. |
| `feat/snt-shorts` | westy412 | 2 | `origin/main` | Taker shorts, side 5, never straddle zero. Off by default. |
| `feat/live-timer-quoting` | westy412 | 2 | `origin/main` | New orders every 500 ms in a live game, changed or not. |
| `feat/snt-t-f07-activity-derivation` | westy412 | 2 | `origin/main` | Taker derives per-book activity state from the game schedule. |
| `phase0/fix-set-dictionary-batch` | westy412 | 1 | `origin/main` | Fix-set Phase 0: all new configuration rows in one commit. |
| `feat/test-ticker-twins` | westy412 | 1 | `origin/main` | A `.TEST` twin of a known ticker is a quotable book. |
| `docs/float-recompute-rule` | westy412 | 1 | `origin/main` | Operating rule 7: recompute floats at every journal cutover. |
| `fix-set/cb4-drain-speed` | westy412 | 5 | **open** | Superseded copy of CB4's work; all 5 commits are patch-identical to merged ones. |
| `feat/converger` | westy412 | 3 | **open** | Superseded copies; one of them also committed ~167k lines of rig output. |
| `chore/drill-observability` | westy412 | 1 | **open** | In flight, 16 Aug 19:10. The drill announces its worktree while it runs. |

Five further branch pointers moved in the window, and all five are merged.

- `feat/bounded-drain` (`f91a264`)
- `feat/group-commit` (`f8c7f2b`)
- `feat/progress-beat` (`d5180eb`)
- `feat/session-boundary` (`a6e2307`)
- `g2-throttle-vm` (`8cca392`)

Each names a single commit that this table lists under its integration branch. They
bring the touched-branch total to 43.

## Commit appendix

Grouped by branch, newest branch first. Every commit in the window appears exactly
once (147 lines, verified).

### `chore/drill-observability`

- `e1d7a80` · `2026-08-16` · westy412 · chore(drill): the drill announces its tree, and three lessons silence taught us

### `fix/post-game-on-final`

- `d2b2fb5` · `2026-08-16` · westy412 · Merge pull request #46 from Novosapien/fix/post-game-on-final
- `749431e` · `2026-08-16` · westy412 · mm: POST_GAME starts at the final's receipt, not the probability stamp

### `fix/freshness-settled-guard`

- `006eb96` · `2026-08-15` · westy412 · Merge pull request #45 from Novosapien/fix/freshness-settled-guard
- `1afc9a3` · `2026-08-15` · westy412 · mm: a settled echo must not re-arm the live freshness regime (N40 engine half)

### `fix/snt-wedge-and-loss-budget`

- `0b9f601` · `2026-08-15` · westy412 · Merge pull request #44 from Novosapien/fix/snt-wedge-and-loss-budget
- `600a873` · `2026-08-15` · westy412 · snt: the spread gate is env-tunable, and the simulation posture is written down
- `3091060` · `2026-08-15` · westy412 · snt: the wedge — a lost cancel silenced one side of a book for ever

### `fix-set/cb4-measurement-integrity`

- `f83a05e` · `2026-08-15` · westy412 · Merge fix-set/cb4-measurement-integrity — PR #43: measurement provenance (sys.path fix so a tree cannot silently measure another tree's code) + the scan-cost and rig-scale replay-check harnesses
- `f8d840f` · `2026-08-15` · westy412 · mm(cb4): size the prune scan on its own, at the shape the rig actually holds
- `b72dee5` · `2026-08-15` · westy412 · mm(cb4): a measurement run must load the tree it lives in
- `c14f118` · `2026-08-15` · westy412 · mm(cb4): rig-scale replay-equality check over a measured run's journal

### `fix-set/cb4-drain-speed`

- `af5e032` · `2026-08-15` · westy412 · mm(cb4): size the prune scan on its own, at the shape the rig actually holds
- `47092cd` · `2026-08-15` · westy412 · mm(cb4): a measurement run must load the tree it lives in
- `de88732` · `2026-08-15` · westy412 · mm(cb4): name the restore loop's unused bindings
- `fd6c03a` · `2026-08-15` · westy412 · mm(cb4): rig-scale replay-equality check over a measured run's journal
- `ccaf3ae` · `2026-08-15` · westy412 · mm(cb4): the ack drain's cost was a full-book scan per event — index it

### `fix-set/ca4-boot-healer`

- `77eeb7a` · `2026-08-15` · westy412 · Merge fix-set/ca2b-refusal-path — the netting set is the FOURTH question (doc)
- `23602ae` · `2026-08-15` · westy412 · Merge origin/main (PR #40 snt live rate) into the CA4 healer merge
- `611eb21` · `2026-08-15` · westy412 · Merge fix-set/ca4-boot-healer — #42 the boot healer (F4/R-D05): cancel-unknowns maker-only, prove-it-dead via cancel (no engine state written), review-ca4's 2 HIGH + 3 MED + 2 LOW fixed + the fork/proxy finding
- `9ef9f23` · `2026-08-15` · westy412 · mm: harden the boot healer per review-ca4 — 2 HIGH, 3 MED, 2 LOW (CA4)
- `e31c746` · `2026-08-15` · westy412 · mm: trace the heal→ack→journal→replay loop in the notes (CA4)
- `e195b2f` · `2026-08-15` · westy412 · mm: the boot healer — cancel unknowns in our own scheme, maker-only (CA4 / F4 / R8)

### `feat/snt-live-rate`

- `7ca9d76` · `2026-08-15` · westy412 · Merge pull request #40 from Novosapien/feat/snt-live-rate
- `2fb5e00` · `2026-08-15` · westy412 · Merge origin/main into feat/snt-live-rate — BUILD-LOG: keep both 15-08b entries (taker rate + N45)
- `5eb4a6b` · `2026-08-15` · westy412 · snt: LIVE one print a second — the ruled rates, the arrival clock, the portfolio cap

### `fix-set/ca3-ask-cap`

- `1e0d265` · `2026-08-15` · westy412 · Merge fix-set/ca3-ask-cap — #38 the ask cap (F3/R-Q08), wired-dark: review-002 HIGH fixed (kept rungs reserved), MED-1 livS scale fix, N45-compat re-pointed tests. Activation gated on N43.
- `85c8848` · `2026-08-15` · westy412 · Merge origin/main — CA2/CA2b BUILD-LOG entries
- `cb46dcd` · `2026-08-15` · westy412 · Merge origin/main into fix-set/ca3-ask-cap — N45 lands, livS tests re-pointed
- `d916133` · `2026-08-15` · westy412 · mm: the cap must survive the reconciler (review-002 HIGH) + rmtree MED
- `8f58685` · `2026-08-15` · westy412 · mm: livS counts a replace net of the fill (review MED-1) + LOW-1/LOW-3
- `62c5d96` · `2026-08-15` · westy412 · mm: pin rest-until-gone above a tightened bound + the MM_DRILL_DIR trap
- `8bb20a4` · `2026-08-15` · westy412 · mm: the ask cap — resize the ladder to what we may legally sell (CA3 / R-Q08)

### `fix-set/ca2b-refusal-path`

- `e129da5` · `2026-08-15` · westy412 · Merge fix-set/ca2b-refusal-path follow-up — CA2/CA2b BUILD-LOG entries (review-002 docs finding)
- `02924c5` · `2026-08-15` · westy412 · Merge fix-set/ca2b-refusal-path — #34 marketable guard + #37 refusal path (F3/R-Q09), review-002 HIGH+7 MEDs fixed, probes re-run both directions. Deploy-coupled: these two ship together.
- `e99486d` · `2026-08-15` · westy412 · docs(tob-cache): the netting set is the FOURTH question, not "not §4.4"
- `00f3a40` · `2026-08-15` · westy412 · docs(build-log): the CA2 + CA2b entries (review-002 stack-wide docs)
- `37811d3` · `2026-08-15` · westy412 · mm: per-class examined budgets + the honest stall bound and AC9 (review-002)
- `c50e7ba` · `2026-08-15` · westy412 · mm: the examined cap must never charge a suspend (P3 HIGH-1) + LOW-2/LOW-4
- `41eddf9` · `2026-08-15` · westy412 · mm: cancels-through-refusal (George's MED-3) + the examined-books cap (MED-4)

### `fix-set/ca2-marketable-guard`

- `a65f5cc` · `2026-08-15` · westy412 · mm: a removal request never nets (review-002 HIGH) + three MEDs
- `628b22a` · `2026-08-14` · westy412 · mm: harden the marketable guard per review-ca2 (1 HIGH, 2 MED, 3 LOW)
- `a307ab7` · `2026-08-14` · westy412 · mm: MARKETABLE_GUARD_STALLED — the stall alarm for R-Q09 (N41's loud half)
- `f358acf` · `2026-08-14` · westy412 · mm: R-Q09 — the pre-flight marketable guard at the converger (fix-set F3)

### `fix/n45-pending-exposure-replay`

- `47741df` · `2026-08-15` · westy412 · Merge fix/n45-pending-exposure-replay — PR #41: EP counts only journal-reconstructable states (George's ruling (a), B2/N45), probe verified both directions
- `88deb0f` · `2026-08-15` · westy412 · fix(venue): N45 — un-acked intent leaves the pending-exposure sum

### `fix-set/cb2-pulse-dephase`

- `bcd4aa7` · `2026-08-15` · westy412 · Merge fix-set/cb2-pulse-dephase — #35 the de-phase clean negative (F1b evidence, UNWIRED), review-002 fixes
- `e37653e` · `2026-08-15` · westy412 · docs(cb2): the UNWIRED marker, the corrected [absolute-grid] note, BUILD-LOG
- `a7abbb7` · `2026-08-14` · westy412 · mm(cb2): pin why the phase module is not wired in — the metric is phase-invariant
- `4c49b83` · `2026-08-14` · westy412 · mm(cb2): the deterministic per-book pulse phase (spec F1b, R2/AC2)

### `fix-set/cb1-profile-workload`

- `fed3e70` · `2026-08-15` · westy412 · Merge fix-set/cb1-profile-workload — #33 timers + six-game workload v2 (F1a), review-002 fixes: PRE_ROLL skew re-cut (George's v2 ruling), mypy module shape, BUILD-LOG
- `1567c93` · `2026-08-15` · westy412 · mm(cb1): re-cut the workload as six-game-v2 — the feeder skew (review-002 HIGH)
- `3403d04` · `2026-08-15` · westy412 · docs(cb1): the missing BUILD-LOG entry for the profile + six-game workload
- `a511304` · `2026-08-15` · westy412 · mm(cb1): make scripts/ a package so `mypy --strict src tests scripts` runs
- `0804500` · `2026-08-14` · westy412 · mm(cb1): AC2 moves to wall-clock ack windows + the #33 review batch
- `5fb71e2` · `2026-08-14` · westy412 · mm(cb1): tick-time instrumentation + THE SIX-GAME WORKLOAD (spec F1a/R1/AC1)

### `hotfix/prune-index-main`

- `520bb01` · `2026-08-15` · westy412 · Merge hotfix/prune-index-main — #39 prune index (F1c), review-002 clean MERGE verdict
- `0be4db5` · `2026-08-15` · westy412 · mm(cb4): name the restore loop's unused bindings
- `4d75550` · `2026-08-15` · westy412 · mm(cb4): the ack drain's cost was a full-book scan per event — index it

### `fix-set/ca1-anchor-seed`

- `07ec787` · `2026-08-15` · westy412 · Merge fix-set/ca1-anchor-seed — #31 dictionary batch + #32 ANCHOR_SEED (F2), review-002 fixes verified (B1 chain + p_tie null)
- `a485f1d` · `2026-08-15` · westy412 · mm: an audit-only p_tie must never cost the anchor (review-002)
- `8942755` · `2026-08-15` · westy412 · mm: the anchor chain — fold ANCHOR_SEED in the tail too (review-002 B1)
- `4a7c484` · `2026-08-14` · westy412 · mm: harden the anchor reader — present is not parseable (review-f2)
- `6ec78fa` · `2026-08-14` · westy412 · docs(ops): MM_PRIOR_RUN_DIR in the operator env table + the cutover step
- `07e47e8` · `2026-08-14` · westy412 · mm: ANCHOR_SEED — kickoff anchors survive a fresh journal (fix-set F2, CA1)

### `phase0/fix-set-dictionary-batch`

- `74709be` · `2026-08-14` · westy412 · config: the 08-14 fix-set dictionary batch + the R11 cutover rule (Phase 0)

### `feat/qty-increment-100`

- `2c74886` · `2026-08-15` · westy412 · Merge pull request #36 from Novosapien/feat/qty-increment-100
- `e8e1003` · `2026-08-15` · westy412 · mm: drop the quantity grid — raw share counts (George: any grid reads inactive)
- `b07ae28` · `2026-08-15` · westy412 · mm: qty grid 100 shares, was 500 — the book no longer reads as blocks

### `hotfix/sweep-tolerance-2s`

- `ed921ca` · `2026-08-14` · westy412 · Merge hotfix/sweep-tolerance-2s — 2.0 s pre-slate tolerance (George 14-08)
- `57765ff` · `2026-08-14` · westy412 · config: sweep tolerance 1.0 -> 2.0 s — George's 14-08 pre-slate ruling

### `feat/always-quoting-step4b`

- `7b43808` · `2026-08-14` · westy412 · Merge feat/always-quoting-step4b into main — F5: main = the running lineage (converger task, boot rebase, wash guard; George 14-08: everything we need on main)
- `5b10d68` · `2026-08-14` · westy412 · Merge origin/main into feat/always-quoting-step4b — restore the wash guard (PR #29)
- `db45300` · `2026-08-14` · westy412 · feat(snt): boot rebase — adopt the venue's first exec-borne figure per book
- `912ba27` · `2026-08-14` · westy412 · feat(runtime): the converger on its own task — always-quoting step 4 phase B
- `8cca392` · `2026-08-13` · deploy (deploy bot) · throttle: converger budget 256 -> 128 (live-load lever, prepared not deployed)
- `8cab9cf` · `2026-08-13` · westy412 · feat(runtime): the single-engine lock — one machine, ONE market maker
- `845ee7e` · `2026-08-13` · westy412 · config: sweep_max_interval_s 0.625 -> 1.0 — restore the spec's absolute slack (George 08-13 evening)

### `feat/converger (open copies)`

- `ea83eac` · `2026-08-13` · westy412 · feat(runtime): the single-engine lock — one machine, ONE market maker
- `9e9257b` · `2026-08-13` · westy412 · config: sweep_max_interval_s 0.625 -> 1.0 — restore the spec's absolute slack (George 08-13 evening)
- `f833d50` · `2026-08-13` · westy412 · config: sweep_max_interval_s 0.625 -> 1.0 — restore the spec's absolute slack (George 08-13 evening)

### `deploy/g2-union-converger`

- `c1ae26f` · `2026-08-13` · westy412 · Merge branch 'deploy/g2-union' into deploy/g2-union-converger
- `11c1d37` · `2026-08-13` · westy412 · feat(venue): the budgeted converger — cycles stage, a paced pass sends (always-quoting step 4 phase A)

### `deploy/g2-union`

- `de689f4` · `2026-08-13` · westy412 · Merge branch 'main' into deploy/g2-union
- `d5180eb` · `2026-08-13` · westy412 · feat(runtime): the progress-aware heartbeat — the beat certifies ticks, not scheduling
- `f8c7f2b` · `2026-08-13` · westy412 · feat(events): N31 group commit — one fsync per tick, before anything leaves the process
- `f91a264` · `2026-08-13` · westy412 · feat(runtime): bounded drain per tick — no tick processes an unbounded backlog
- `a6e2307` · `2026-08-12` · westy412 · feat(state): bound working memory — prune terminal orders, scope dedup retention
- `c08b9aa` · `2026-08-12` · westy412 · Merge feat/test-ticker-twins into the deploy set (imports reconciled)
- `9169a4d` · `2026-08-12` · westy412 · feat(runtime): the engine learns tZERO's day — fork checkpoints, gone-retire, the session clock

### `feat/snt-wash-guard`

- `772e79c` · `2026-08-13` · westy412 · Merge pull request #29 from Novosapien/feat/snt-wash-guard
- `a81c86b` · `2026-08-13` · westy412 · test(snt): settle-as-you-go in the wash-guard resumption assert
- `4d549b3` · `2026-08-13` · westy412 · feat(snt): the wash guard — never send against an own resting remnant

### `feat/state-publishers-manual-orders`

- `61fc272` · `2026-08-13` · westy412 · Merge pull request #23 from Novosapien/feat/state-publishers-manual-orders
- `84db77f` · `2026-08-13` · westy412 · Merge remote-tracking branch 'origin/main' into feat/state-publishers-manual-orders
- `ac993db` · `2026-08-12` · westy412 · deploy+snt: the verification rule in its strongest form, and proof we are immune to platform's F2
- `9ec8225` · `2026-08-12` · westy412 · snt: prove attribution against the real parser, not the fake
- `397b093` · `2026-08-12` · westy412 · snt: the wire lower-cases the denial, and my fixture had the wrong shape
- `f442a8f` · `2026-08-12` · westy412 · snt: the adversarial review — the classifier is now tested, and correct
- `021e846` · `2026-08-12` · westy412 · deploy: make the EC19 cancel a gate, and record that the flush is manual-only
- `6e6708b` · `2026-08-12` · westy412 · deploy: record the flush-timeout ↔ proxy-reply-timeout coupling
- `236bfb2` · `2026-08-12` · westy412 · snt: make EC18 and EC19 drillable without shipping a fault hook
- `02f098b` · `2026-08-12` · westy412 · bench: measure the production publish path (encoded bytes, not a re-encode)
- `d3aa9d8` · `2026-08-12` · westy412 · mm+snt: the MEDIUMs and LOWs — one encode, taker budget, determinism lock
- `80a33ef` · `2026-08-12` · westy412 · snt+mm: F4 the missing grant, F2 the rollback leak, F3 the dark publisher
- `2fa09d1` · `2026-08-12` · westy412 · snt: F1 — a manual order is only real once the publish reached the wire
- `da5de41` · `2026-08-12` · westy412 · deploy: a publish-based grant check is a lie unless it inspects last_error
- `c264dd9` · `2026-08-12` · westy412 · mm+snt: encode off the tick, both activity states, dictionary numbers, grant lines
- `5312dd4` · `2026-08-12` · westy412 · deploy: the observability redeploy runbook — grants first, halt before stop, and what a fresh journal resets
- `ef76d17` · `2026-08-12` · westy412 · snt: manual cancel/replace, journaled ref-dedup, replay re-adoption (R3)
- `fd78132` · `2026-08-12` · westy412 · snt: manual order PLACE — guards, collar fallback, reply contract (R3)
- `f1a3b65` · `2026-08-12` · westy412 · snt: the taker state publisher + the P&L meter and order-state fold (R2)
- `4d0330f` · `2026-08-12` · westy412 · mm: the maker state publisher — mm.state snapshots at the runtime edge (R1)

### `feat/snt-hardening`

- `c4c51b4` · `2026-08-13` · westy412 · Merge pull request #28 from Novosapien/feat/snt-hardening
- `7b32922` · `2026-08-13` · westy412 · fix(snt): T-F07 freshness prices the fetch, and T-S05 reads the exec's own 9383

### `feat/test-ticker-twins`

- `edd9512` · `2026-08-12` · westy412 · feat(universe): a .TEST twin of a known ticker is a quotable book

### `docs/float-recompute-rule`

- `53141b7` · `2026-08-11` · westy412 · docs: rule 7 — floats are positions; recompute at every journal cutover

### `docs/taker-operating-lessons`

- `b954b3c` · `2026-08-11` · westy412 · Merge pull request #20 from Novosapien/docs/taker-operating-lessons
- `7442012` · `2026-08-11` · westy412 · docs: SNT-1 operating lessons from the 08-11 incident chain

### `feat/inverted-size-ladder`

- `b86ca83` · `2026-08-11` · westy412 · Revert "Merge pull request #19 from Novosapien/feat/inverted-size-ladder"
- `e8d1462` · `2026-08-11` · westy412 · Merge pull request #19 from Novosapien/feat/inverted-size-ladder
- `d7d2a3c` · `2026-08-11` · westy412 · feat(quotes): invert the size ladder — thin at the touch, fattest at depth (George 08-11c)

### `feat/per-mode-republish-timer`

- `3419de9` · `2026-08-11` · westy412 · Merge pull request #18 from Novosapien/feat/per-mode-republish-timer
- `f623222` · `2026-08-11` · westy412 · feat(quotes): the dwell table IS the republish clock in every mode (George 08-11b)

### `feat/ingestion-switch`

- `48b3c0e` · `2026-08-11` · westy412 · Merge pull request #17 from Novosapien/feat/ingestion-switch
- `29ae86d` · `2026-08-11` · westy412 · test(rig): harden the A2 drill for the 500 ms cadence
- `887ee0a` · `2026-08-11` · westy412 · fix(runtime): inbound envelopes stamp the deployment's real config version
- `debf1ef` · `2026-08-11` · westy412 · feat(runtime): the ingestion switch — MM_READINGS=bus wires the durable SR_PROBABILITIES subscription in any mode

### `feat/snt-shorts`

- `491e63b` · `2026-08-11` · westy412 · Merge pull request #15 from Novosapien/feat/snt-shorts
- `f14cece` · `2026-08-11` · westy412 · feat(snt): shorts — side 5 under T-O10, flatten first, never straddle zero

### `feat/live-timer-quoting`

- `55ddf60` · `2026-08-11` · westy412 · Merge pull request #16 from Novosapien/feat/live-timer-quoting
- `6ab57a5` · `2026-08-11` · westy412 · feat(quotes): live timer quoting — new orders every 500 ms, changed or not (George 08-11)

### `feat/snt-t-f07-activity-derivation`

- `5681767` · `2026-08-11` · westy412 · Merge pull request #14 from Novosapien/feat/snt-t-f07-activity-derivation
- `623c761` · `2026-08-11` · westy412 · feat(snt): T-F07 — derive the per-book activity state from the game schedule

### `feat/snt-1-float-and-sell-gate`

- `0344a60` · `2026-08-11` · westy412 · Merge pull request #12 from Novosapien/feat/snt-1-float-and-sell-gate
- `0570bf5` · `2026-08-10` · westy412 · fix(snt): fold fills via the subject's ClOrdID + env-tunable float
- `f9ae1f3` · `2026-08-10` · westy412 · test(snt): the minting assertion follows the MMSN prefix
- `20f6a51` · `2026-08-10` · westy412 · fix(snt): MMSN ClOrdID prefix — the gateway rejects non-MM ids on its namespace
- `2de7775` · `2026-08-10` · westy412 · feat(snt): T-S05 — reconcile position against the venue, halt on divergence
- `7e2b54d` · `2026-08-10` · westy412 · feat(snt): the float, the sell gate, and the hardening round — T-O07/T-O08/T-M03/T-R01

### `fix/reject-backoff`

- `0ce16f5` · `2026-08-11` · westy412 · Merge pull request #13 from Novosapien/fix/reject-backoff
- `557148f` · `2026-08-11` · westy412 · Merge origin/main: #11's untracked-drain counters beside the backoff field
- `5e42735` · `2026-08-10` · westy412 · test(rig): A2 stage-1 replay drill — the full captured game over the bus at paced speed
- `2b43da7` · `2026-08-10` · westy412 · feat(venue): reject backoff — a rejected instruction retries on a schedule, not at sweep cadence (R-R03, C4)

### `fix/cancel-reject-drain`

- `749283d` · `2026-08-11` · westy412 · Merge pull request #11 from Novosapien/fix/cancel-reject-drain
- `658dc02` · `2026-08-10` · westy412 · fix(venue): drain no-symbol terminal acks for untracked orders — close PR #11's named residual
- `eceaf26` · `2026-08-10` · westy412 · fix(venue): drain a cancel-reject for an untracked order instead of dying

