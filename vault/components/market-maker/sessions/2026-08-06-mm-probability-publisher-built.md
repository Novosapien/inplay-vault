# 2026-08-06 — the ingestion move, service side: the MM probability publisher BUILT

> **Who:** George + Claude (step-approved throughout — George reviewed each
> piece in chat before the next)
> **Type:** build session in `inplay-sportradar-service` (the 05-08c
> ingestion ruling executed)
> **Refs:** branch `feat/mm-probability-publisher` off updated `dev` —
> commits `7cfe391` · `75bc8ba` · `766a607` · `4e770fb` · `55a9019` ·
> `614c4be` · `b98e732` · `4eb2102` · **547 → 575 tests**, ruff + format +
> mypy clean. Design doc: `docs/mm-probability-publisher.md` (in the repo).
> ⚠ All commits LOCAL, unpushed (George's standing instruction).

## What we did

1. **Repo brought current first (George's instruction):** origin merged
   into `dev`, `testing`, `main` — six conflict files on dev resolved
   (deploy.sh took the post-incident remote; `ZITADEL_AUDIENCE_SECRET`
   rename carried), testing's five resolved (remote = later evolution of
   local work). 547 tests green before any new code.
2. **The publisher, piece by piece** (each approved in chat):
   - **NATS seam** — `ReadingPublisher` Protocol, real client, in-memory
     double. Subjects `sr.probabilities.reading.{game_suffix}`.
   - **The float-free fetch** — `_get_json_raw` beside the service's
     typed client: same retry contract, `parse_float=str`, probabilities
     as exact text end to end. Timeline + Sport Schedule methods.
   - **The tier scheduler** — the MM vault's table ported: LIVE 2 s ·
     PRE_KICKOFF 15 s · OVERNIGHT 30 min · POST_GAME 10 min/1 h/never.
     Settings-driven (`MMPUB_*`).
   - **The worker loop** — due games → fetch → publish unsent readings
     (per-game publish watermark) → mark finals. Lease-fenced from day
     one (reuses the live worker's `LeaseFence`); failed fetch = counted
     silence; restart re-publishes and the MM dedups.
   - **`python -m app.workers.mm_publisher`** — fail-fast NATS connect,
     discovery at boot + each UTC date change, clean shutdown.
3. **⭐ JetStream delivery (George + Hasan):** Hasan confirmed production
   NATS runs JetStream; **validated on the server itself** (read-only SSH
   to `inplay-nats`, the `/jsz` endpoint: store `/data/nats/jetstream`,
   10 GB cap, 5 streams / 593 messages already live — the gateway's).
   The publisher ensures the `SR_PROBABILITIES` stream (week retention)
   and **refuses to start without JetStream** — durability is contract,
   never silently downgraded. `Nats-Msg-Id` = `{game_id}:{last_updated}`
   gives server-side dedup of publisher-restart re-publishes. Proven
   end-to-end against a real JetStream container (3 sent → 2 stored →
   replayed with headers intact) and refused against a non-JS server.
4. **Payload parity fix (found designing the consumer):** the payload now
   carries SR's `live` coverage flag — the MM's §7.3 dedup compares
   hashes under one key, and a missing field would false-CONFLICT the
   same reading arriving by file-replay and by NATS.

## Decisions *(this note is the record; hub/plan updated)*

- ⭐ **Delivery is JetStream** (George, on Hasan's confirmation +
  server-validated). Closes the fire-and-forget gap — a reading
  published while the MM is down (the kickoff-crossing `p_ref` case)
  now waits in the stream.
- **Polling is per GAME, never per team** (clarified for George): one
  timeline carries both sides; cost scales with concurrent games (~35
  worst case), not 170 securities. S7's live-bulk endpoint collapses
  even that, later.
- **The publisher is a WORKER, never the API** (George's concern,
  resolved): the autoscaled API never polls; the worker pool is
  fixed-count with the lease pair for failover — capacity is not the
  problem, availability is.
- **Message contract v1:** payload = game/team ids · kickoff ·
  `last_updated` · outcomes verbatim (exact text) · `live` · status ·
  scores; headers = `Fetched-At` (the E38 liveness stamp) +
  `Nats-Msg-Id` (the reading's identity).

## What's open / next

1. **The MM-side consumer** (MM repo — NEW SESSION): JetStream durable
   subscription → the runtime's drain path (mirror the venue drain) →
   the same adapter/acceptor; observation age from `Fetched-At`; finals
   minted MM-side (N16 stays the MM's). Then the in-engine poller
   retires from the live composition. `LIVE_GATES` in the MM's
   compose.py already names the ingestion move.
2. **Rig chore:** `mm-nats` has no jetstream stanza — needs the `-js`
   flag before an end-to-end drill.
3. **George's CI/CD audit ask (recorded 06-08):** at end of
   implementation, audit testing + prod deployments for the sportradar
   API **and** the workers, incl. where the MM publisher slots into the
   worker pool.
4. Unchanged: the unsent Edwin round E29–E38 · §10.3 checkpoints ·
   the 06:00 hand-off · pushing all branches (George's call).
