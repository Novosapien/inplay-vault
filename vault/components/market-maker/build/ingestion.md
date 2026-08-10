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
question, not a filing question).

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
| LIVE | kickoff passed, no final | **~2 s** (SR's measured median update gap is 4 s) |
| PRE_KICKOFF | within 1 h of kickoff | **15 s** (interim — George's 10–30 range) |
| OVERNIGHT | kickoff > 1 h away | **30 min** (doubles as the N24 pregame-movement watch) |
| POST_GAME | final seen, ≤ 1 h | **10 min** (the correction watch), then never |

A game with no kickoff errs busy at the live rate; a moved kickoff
re-stamps and reschedules at once. Kickoffs are converted to the
scheduler's monotonic clock ONCE, at the composition edge — a wall-clock
jump can never mis-tier a game mid-run.

## What changes here next

[[market-maker/build/next|Next]]: the go-live switch (live wiring
consumes the bus; poller keeps the heartbeat) · S7's live-bulk endpoint
(all live games in one call — collapses the NCAA-Saturday serial-fetch
ceiling) · N19/N23 for Edwin's file.
