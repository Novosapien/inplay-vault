---
description: "The as-built ingestion page — the bus path (publisher + consumer), file replay, Edwin's file, venue events, finals, discovery and poll tiers"
---

# Build — Ingestion

> Part of [[market-maker/build/index|As Built]] · Code:
> `mm/adapters/sportradar.py` · `mm/poller/` · service
> `app/workers/mm_publisher/` · Spec: §2.1, §3.2, §7.3.
> Rulings: the 05-08c ingestion ruling · every-fetch-publishes (06-08b).

Four paths carry data into the acceptor. The engines never see raw JSON:
adapters translate at the edge, and only the adapter changes if a
provider does.

## Path 1 — Sportradar readings over the bus (the live path)

**The ruling (George, 05-08c):** the sportradar SERVICE polls SR and
publishes readings on NATS; the MM consumes the bus and never calls SR
itself. Built on both sides and drilled end to end 06-08b.

### The publisher (service repo, `mm_publisher/`)

- One worker process (`python -m app.workers.mm_publisher`) on a 1 s
  tick: due games → float-free fetch (`parse_float=str`, probabilities as
  exact text) → publish. Discovery daily from the Sport Schedule (one
  call, both leagues, games touching the 170 only; `replaced_by` fixtures
  skipped; home/away read from SR's qualifier field, never list order).
  ⚠ **The universe filter never matched until 13-08** (found 40 min
  before the first live games): the filter tested `sr:competitor:` ids
  against GUID-keyed `TEAM_SYMBOLS`, so every discovered game was
  silently dropped — the publisher had never fed the bus a real game.
  Hotfixed on both pools (`sr:competitor:` ids now pass; the MM's own
  bindings decide what it prices). ⚠ Merge-path caveat (verified
  14-08): service **PR #37** carries the fix but its head IS the full
  `testing` tip — **65 commits, +7544/−371** — so merging it promotes
  ALL of testing to main, not one hunk; the true one-hunk fix
  (`hotfix/mm-publisher-universe-filter` @ `d877b26`, cut from main
  HEAD) has NO PR of its own. Until one of them merges, a main deploy
  regresses the filter. The proper fix — the GUID ↔ sr-native mappings
  bridge in discovery, plus a loud `adopted=0` alarm on a game-day
  schedule — is **N39**. Session: 2026-08-13-e.
- **Two publishers feed one bus since 13-08** (production + testing
  pools share the NATS secret). Deliberate redundancy: readings are
  idempotent and re-offers are liveness confirmations, so duplicates
  are harmless by design.
  ⚠ Cloud Run operational fact: a pool update that omits
  `--instances=1` loses the manual instance count and the worker dies
  with "user disabled instance" — carry BOTH the instance count and the
  env change in one update (08-13-b addendum 6).
- **Delivery is JetStream** (validated on the production server): stream
  `SR_PROBABILITIES`, subjects `sr.probabilities.>`, one-week age
  retention. The publisher **refuses to boot without JetStream** —
  durability is contract, never silently downgraded.
- **Subject:** `sr.probabilities.reading.{numeric tail}` (subjects cannot
  carry `:`; the full `sr:sport_event:…` id rides the payload).
- **Payload (contract v1):** `game_id`, `home_team_id`, `away_team_id`,
  `kickoff_time`, `last_updated`, `outcomes` (SR's fields verbatim, exact
  text), `live` (SR's coverage flag — carried for hash parity), `status`,
  `home_score`/`away_score` when present (the finals input).
- **Headers:** `Fetched-At` — the wall-clock instant the fetch SUCCEEDED
  (the MM's liveness signal, George's fetch-stamp design) ·
  `Nats-Msg-Id` = `{game_id}:{last_updated}:{fetched_at}` — one publish
  ATTEMPT's identity: the bus dedups client retries of the same attempt,
  never a deliberate re-offer.
- ⭐ **Every successful fetch publishes (George, 06-08b).** New readings
  go out one message each; a fetch that finds nothing new **re-offers the
  newest reading** (chosen by its own `last_updated`, never list
  position) under a fresh stamp. Why: SR sends no heartbeat — halftime is
  a measured 2,862 s without a new reading — and on a push path the ONLY
  way the consumer knows "the source answered just now" is a message. A
  send-only-new watermark would re-create the quiet-is-not-dead trap at
  the transport layer. The re-offer also carries the CURRENT status and
  scores, which is how a final whose status flips after the last
  probability move reaches the MM, and how the post-game correction
  watch works over the wire.
- **Fail-open on SR** (a failed fetch publishes nothing, counted; the
  tier retries), **fail-fast on NATS** at boot. Lease-fenced per game
  (leader/standby — only the lease-holder publishes). A restart forgets
  the sent-watermark and re-publishes; the MM dedups.

### The consumer (MM repo, `mm/poller/consumer.py`)

- A **durable** JetStream subscription (`mm-engine`) on
  `sr.probabilities.reading.>` feeds an asyncio queue; the subscription
  callback only enqueues (it runs on the client's IO task).
- `ReadingInbound` — the drain: one submission per call, `None` when
  empty (the venue drain's exact shape). A final-status reading yields
  its minted `OFFICIAL_RESULT` on the following call.
- **Acks are batched and flushed AFTER the tick** that journalled the
  messages: pop → journal → ack. Die before the journal → unacked →
  redelivered. Die after → §7.3 discards the repeat. Ack-before-journal
  would re-open the downtime-loss gap JetStream exists to close.
- **Poison rule:** an unparseable body, missing contract fields, or a
  missing `Fetched-At` is acked AWAY and counted (`poisoned`) — a
  message that can never parse must not redeliver forever and jam the
  durable.
- Both ends **ensure** the stream with one literal config — boot order
  between publisher and consumer is free; a drifted contract is a loud
  boot failure, never a silent split.
- The durable's first bind delivers the stream from the start
  (deliver-all): a first-ever boot chews at most a week and §7.3
  discards what the journal already holds; every later boot resumes from
  the cursor.

### The adapter — parity is the contract

`adapters/sportradar.py`. One wire reading must build the SAME envelope
the file path builds — the journal holds file-path history, and §7.3
compares hashes under one key, so any field drift false-CONFLICTs a
healthy migration. **Enforced structurally:** both front doors
(`timeline_to_submissions`, `reading_to_submission`) feed ONE constructor
(`_reading_envelope`); the finals paths share `result_envelope` the same
way. Proven on the real Chiefs–Ravens capture: 1,089/1,089 envelope
equality; a wire re-delivery of file-journalled history lands DUPLICATE
1,089/0. The `Fetched-At` header lands in `receive_time` ONLY — never
the key, never the payload — so a publisher-restart re-publish stays a
quiet duplicate.

The payload the engines see: `game_id`, both team ids, `kickoff_time`,
`p_home`/`p_away` (SR's percentages ÷100 via Decimal, exact),
`p_tie="0"` (S6 interim), `live_coverage` (SR's coverage flag — true on
games that have not started; it never answers "has this begun?").

### The drill (06-08b, local docker)

Pre-boot readings caught up from the stream and priced · a mid-run
re-offer landed DUPLICATE while the sweep's observation stamp ADVANCED ·
the ended reading minted the final · restart on the same journal: 135
events replayed, **zero messages redelivered**.

## Path 2 — File replay (the test harness)

`load_timeline` + `timeline_to_submissions` over captured responses. The
certification tool: same file in, same envelopes out, every time. The
in-engine poller (`poller/worker.py`) still owns this pull path plus the
gateway heartbeat; **it retires from live wiring at go-live** (George,
06-08b) — nothing is deleted before then.

## Path 3 — Edwin's daily reference file

`adapters/reference_feed.py`. One JSON file, all 170 teams, 06:00 ET
daily, published even when unchanged: `expected_remaining_wins` (**T**),
`sigma`, `games_remaining`, `effective_time`, `revision`,
`is_correction`, `methodology_version`. Corrections resend the same
`effective_time` with a bumped revision. The reader returns EVERY
violation at once (all-at-once rejection, so Edwin fixes the file in one
pass). Open: the transport (N19 — upload page decided; who does 06:00
until it exists) and the §7.3 event type for T (N23 — a replay-equality
question, not a filing question). **➕ 13-08: the full pipeline design is
filed — [[market-maker/systems/daily-reference-feed]]** (bus delivery on
the path-1 shape, the proposed `REFERENCE_NUMBERS` event, the monotonic
apply guard, the stale-T ladder). Design only; nothing here changed.

## Path 4 — Venue events

The gateway publishes acks, fills and resolved cancels on `order.mm1.>`;
`adapters/gateway.py` parses (`parse_float=str`) and translates; the
runtime drains the queue to empty every tick. Loopback quirk: the
gateway's LOCAL publish paths omit the order id from the payload — the
adapter falls back to the subject's last segment.

## Finals (N16)

Nothing else in the platform publishes "game X is final." The MM mints
`OFFICIAL_RESULT` version 1 from a reading whose SR status is
`ended`/`closed`; outcome home/away/tie from the scores. An identical
re-offered final is a quiet duplicate; a CHANGED outcome under the same
key is a **loud CONFLICT** — §3.1.3 wants a human and a new result
version, never an automatic overwrite.

## Poll tiers (both repos' `scheduler`)

| Tier | When | Cadence |
|---|---|---|
| LIVE | kickoff passed, no final | ✎ **~2 s per pool as deployed** (measured 15-08: `poll_live_s = 2.0` in `config.py`; bus arrivals ~1.2 s per game = TWO pools at 2 s out of phase). The standing "the deployed PUBLISHER runs 500 ms" line was WRONG — George's 08-11 500 ms ruling never reached the publisher's config. ⚠ the in-engine poller also carries 2 s until it retires |
| PRE_KICKOFF | within 1 h of kickoff | **15 s** (interim — George's 10–30 range) |
| OVERNIGHT | kickoff > 1 h away | **30 min** (doubles as the N24 pregame-movement watch) |
| POST_GAME | final seen, ≤ 1 h | **10 min** (the correction watch), then never |

A game with no kickoff errs busy at the live rate; a moved kickoff
re-stamps and reschedules at once. Kickoffs are converted to the
scheduler's monotonic clock ONCE, at the composition edge — a wall-clock
jump can never mis-tier a game mid-run.

⚠ **The game-end lifecycle hole (N40, forensics 14-08):** on MAIN's
code the publisher drops from the live rate to **600 s immediately at
the final** (`poll_post_game_s`), then retires the game for good after
the 1 h window. ✎ **The deployed TESTING pool (952d8be, the #38-family
values) differs: 2 s settle watch for 2 h, then 1,800 s forever —
verified against the 15-08 timings (finals 20:01–20:04Z, last bus
messages 22:01–22:05Z = final + exactly 2 h).** Either way the
confirmations eventually space out past 20 s; an engine book still in
the live-freshness regime then goes RP Invalid and §6.3 SUSPENDS it —
permanently, with no re-open path. ⚠ **Keep-polling alone is PROVEN
insufficient (15-08): the testing pool ran it all night and the six
books died anyway at the window's edge.** ➕ **15-08: WHY the
book is still in the live regime is found and fixed (MM PR #45,
unmerged)** — the engine's `OFFICIAL_RESULT` correctly de-arms it, then
SR's post-final SETTLED readings (p=1/0, minutes after the whistle)
re-arm it through `_note_freshness`; the `[settled-freshness]` guard
closes that. See the N40 row's 15-08 addendum. Ten books went dark this way overnight 13/14-08; two
(PATR/COLT) escaped the suspension by minutes and kept quoting
PRE-FINAL prices — live exposure. Worse, journal-verified: within the
old 600 s correction watch, every finished book FLAPPED
suspend → cancel → re-stand once per poll (each re-offer briefly
confirms, the book re-stands, then ages back to Invalid before the
next poll). A duplicate game id also polls at the live tier forever
because its status never flips. ➕ **The service-side fix is BUILT and on the TESTING pool** since
~12:55Z 14-08: PR #38 (`fix/mm-publisher-post-game-keep-polling`
@`751efb6`, cherry-picked to `testing@d492dcb`) — settle watch at the
live rate, post-game window 2 h, then OVERNIGHT cadence forever
instead of retirement; the PRODUCTION pool still runs the old code
(row in [[market-maker/build-deploy-log]]). ⚠ Scope caveat: discovery
only re-adopts TODAY's-dated games, so yesterday-dated finished games
stay feedless — their books ride seed until the engine-side hand-off
(a post-final freshness regime) lands, which is still open. Full forensics:
sessions/2026-08-14-gateway-watch-and-game-end-forensics.

## What changes here next

[[market-maker/build/next|Next]]: the go-live switch (live wiring
consumes the bus; poller keeps the heartbeat) · S7's live-bulk endpoint
(all live games in one call — collapses the NCAA-Saturday serial-fetch
ceiling) · N19/N23 for Edwin's file.
