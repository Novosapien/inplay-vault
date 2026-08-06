# 2026-08-06b — the ingestion move, MM side: the consumer BUILT and DRILLED

> **Who:** George + Claude (step-approved — George reviewed each piece
> in chat before the next)
> **Type:** build session in `inplay-market-maker` (+ one ruling executed
> in `inplay-sportradar-service`) — the 06-08 morning session's "next"
> **Refs:** MM branch `feat/position-engine`, commits `6a4904f` ·
> `f01dfba` · `d79c6f0` · `db04830` · `53f2ede` · `f4d3eac` —
> **512 → 534 tests**, ruff + mypy strict clean. Service branch
> `feat/mm-probability-publisher`, commit `0b936c8` — **575 → 577
> tests**. ⚠ All commits LOCAL, unpushed (George's standing rule).

## What we did

1. **The reading adapter (`6a4904f`)** — `reading_to_submission` turns
   one published NATS reading into the SAME envelope
   `timeline_to_submissions` builds. Parity is structural: both front
   doors call one shared `_reading_envelope` constructor. Proven on the
   real Chiefs–Ravens capture: field-for-field equality on all 1,089
   readings, and a wire re-delivery of file-journalled history lands
   DUPLICATE 1,089/0. The `Fetched-At` header lands in `receive_time`
   only — never the key, never the payload.
2. **The finals adapter (`f01dfba`)** — `reading_to_result` mints
   `OFFICIAL_RESULT` version 1 from a final-status reading, on the
   poller's exact key basis. Same structural move: the construction
   left `Poller._maybe_final` for a shared `result_envelope`;
   `FINAL_STATUSES` and the score→outcome rule are shared too.
3. **⭐ The finals gap, found and closed by George's ruling** (executed
   in the service, `0b936c8`): the publisher only sent NEW readings, so
   a game whose status flips to ended AFTER its last probability move
   would never reach the MM — and, worse, any quiet stretch (halftime:
   the measured 2,862 s) would read as a dead feed and suspend healthy
   books, the quiet-is-not-dead trap re-created at the transport layer.
   **George: every successful fetch publishes.** A fetch that finds
   nothing new re-offers the NEWEST reading under a fresh `Fetched-At`;
   the body is a §7.3 quiet duplicate at the MM, the header is the
   point. The re-offer carries the CURRENT status and scores — which
   closes the finals gap and gives the wire path the post-game
   correction watch for free. **`Nats-Msg-Id` becomes
   `{game_id}:{last_updated}:{fetched_at}`** (George specified the
   composition): one publish attempt's identity, so JetStream dedups
   client retries but never swallows a deliberate re-offer.
4. **The consumer seam (`d79c6f0`)** — `mm/poller/consumer.py`: a
   JetStream durable subscription (`sr.probabilities.reading.>`, stream
   `SR_PROBABILITIES`, durable `mm-engine`) feeding an asyncio queue;
   `ReadingInbound` drains one submission per call (a final-status
   reading yields its minted final on the following call); `PendingAcks`
   batches acks. Poison rule: a malformed body is acked away and
   counted, never redelivered forever. Refuses to start without
   JetStream (the publisher's rule mirrored).
5. **The runtime wiring (`db04830`)** — the tick drains bus readings
   through the full pipeline; the observation stamp is taken from the
   envelope's `receive_time` BEFORE the acceptor's verdict (a duplicate
   IS the confirmation); `run()` awaits the ack flush AFTER each tick —
   pop → journal → ack, so a crash anywhere costs a redelivery, never a
   loss.
6. **The composition (`f4d3eac`)** — `python -m mm.runtime` binds the
   durable and consumes the bus. The loopback team map switched from the
   synthetic `lb:*` bindings to the REAL `TEAM_BINDINGS` (a published
   reading names real competitor ids; routing them is what a drill must
   prove). New `MM_SECURITIES` names a drill's exact books. The consumer
   ENSURES the stream with the publisher's exact config, so boot order
   between the two processes is free.
7. **⭐ The end-to-end drill PASSED on local docker** (`mm-nats`
   recreated with `-js`, `53f2ede` documents it): 2 readings published
   BEFORE boot were caught up from the stream and priced · a mid-run
   re-offer landed duplicate while the sweep's `observations` stamp
   ADVANCED (14:05:31 → 14:05:53 — George's ruling, observed working) ·
   the ended reading minted the MM-side final (outcome home) · 18
   orders stood against the real gateway and repriced per reading ·
   **restart on the same journal: 135 events replayed, ZERO messages
   redelivered** — the acks and the durable cursor both proven.

## What we learned

- **A publish watermark is a liveness filter.** Deduplicating on the
  publish side (send only new readings) silently strips the "the source
  answered just now" signal the observation-age design needs — the
  halftime trap moves one layer down and comes back. Liveness must ride
  EVERY successful fetch; dedup belongs at the consumer (§7.3), where it
  always was.
- **Server-side msg-id dedup fights deliberate repeats.** With the
  reading's identity as msg-id, JetStream's dedup window would swallow
  the confirmations. The id must name the publish ATTEMPT
  (reading + fetch stamp): retries dedup, re-offers deliver.
- **The ack IS the durability boundary.** Ack meaning "journalled" —
  flushed after the tick, never inside it — is what makes every crash
  window safe: before the journal → redelivered; after → §7.3 discards.
- The morning note first recorded the JetStream commit as `b98e732`;
  the repo's hash is `451cd63` (amended after the note). Corrected in
  place — record hashes AFTER the final amend.

## Decisions *(this note is the record; decisions.md + plan updated)*

- ⭐ **Every successful fetch publishes; the re-offer is the liveness
  signal** (George). Msg-id = `{game_id}:{last_updated}:{fetched_at}`.
- **The in-engine poller retires only AT GO-LIVE** (George): nothing is
  deleted now; the live composition switches to the bus when we push
  live. Loopback keeps the poller for the heartbeat (`games=[]`).
- Autonomous (ours, tagged in code): structural parity via shared
  constructors · the poison rule · durable `mm-engine`, deliver-all on
  first bind · stream ensured by both ends with one literal config ·
  the observation stamp taken before the accept verdict ·
  `MM_SECURITIES` · loopback binds real `TEAM_BINDINGS`.

## What's open / next

1. **The go-live switch** (parked, George's ruling): live composition
   consumes the bus, poller keeps only the heartbeat, `LIVE_GATES`'
   ingestion entry closes. Do when pushing live — with the rig drill
   re-run against it.
2. **George's CI/CD audit** (recorded 06-08): end of implementation —
   testing + prod deploys for the sportradar API and workers, incl. the
   MM publisher's worker-pool slot.
3. Unchanged: the unsent Edwin round E29–E38 · §10.3 checkpoints
   (required pre-season) · N19's 06:00 hand-off · the Hasan message
   (N30 + governor) · pushing all branches (George's call).
4. **Vault restructure/archive discussion** — George wants to review
   what in the vault is stale (raised at this session's close; not yet
   done).
