# 2026-08-02 — first contact: the loopback wire test passes

> **Who:** George + Claude, autonomous integration mode
> **Type:** build session
> **Refs:** `inplay-market-maker` commits `abd8b2a` · `c477713` · `7b510ea`
> (+ docs) · story page "First contact" 📡 · BUILD-LOG session 02-08

## What we did

The remaining ungated builds, with the wire test — George's precondition
for any live attempt — as the centrepiece. **434 → 443 tests**, ruff and
`mypy --strict` clean, scripts included.

1. **The NATS transport** (`venue/nats_transport.py`, `abd8b2a`) — the one
   real implementation of the gateway transport Protocol. One queue, one
   writer task: strict FIFO onto the wire; a dead writer raises on the
   next publish. `nats-py` is the repo's first runtime dependency,
   confined to the edge.
2. **Game discovery** (`poller/discovery.py`, `c477713`) — the Sport
   Schedule endpoint (same v1 product as the timeline; one S1 entitlement
   covers both) → the games touching our universe, via the valuation
   engine's own team map. `Poller.ensure_game()` is idempotent.
3. **The loopback wire test** (`scripts/loopback_wire_test.py`,
   `7b510ea`) — docker rig: `nats:2.10` + the real gateway binary with
   `LOOPBACK_MODE=true` and `MM_ENABLED=true`. **All five phases pass**:
   heartbeat · post (16 submits ACTIVE) · move (36 instructions, replaces
   carrying remainders) · the kill switch · the dead-man sweep. 343 order
   events consumed from the wire on the passing run.

## What we learned — the wire-only findings

- **Gateway-local events name their order in the subject alone.**
  Loopback accepts and every gateway-resolved cancel (dead-man and
  cancel_all sweeps included) carry no `clOrdId` in data; the subject
  `order.{user}.{clOrdId}` is the name. Adapter fix: topic fallback,
  fills stay strict (`[topic-fallback]`).
- **Cross-subject timestamp order is not guaranteed** — the gateway's
  eight publisher workers delivered two acks for one security 10 µs
  reversed, tripping the volatility engine's backward-clock guard. Fix:
  the orchestrator floors each security's cycle clock (`[monotonic-at]`);
  deterministic on replay.
- **cancel_all is a hammer, not a stop.** Fired alone it swept 48 orders
  — and the live bot correctly treated the emptied venue as divergence
  and reposted its whole book. The STOP is Ch 6's kill switch; the drill
  now engages the bot's switch first and proves nothing reposts. The two
  levers are for different jobs, now demonstrated.
- Minor: stale ACTIVE levels can rest between publishes when an in-flight
  order becomes cancellable after the target moved — the next publish's
  diff cleans them; the §3.1.4 heartbeat sweep (unbuilt) is the
  systematic healer. NOT_CANCELABLE races during sweeps are benign — the
  record converges on the event stream.

## What went wrong

- The gateway image would not build as committed: its Dockerfile pins
  `golang:1.23-alpine`, its `go.mod` requires Go ≥ 1.26. Built with an
  override Dockerfile; **tell Hasan** (plus finding 1 above).
- The first docker build failure was masked by piping through `tail` —
  the exact gotcha the 01-08 handover warned about. Caught on the next
  step; the wire test itself was never affected.

## Decisions *(mirrored into decisions.md 02-08)*

NATS transport FIFO-by-single-writer · topic fallback for order naming ·
per-security cycle-clock floor · the wire test drives the bot's kill
switch before the gateway's hammer · §10.3 checkpoints deferred as a full
session (complete-state snapshots across eight engines — not a fill-in).

## Questions

- **No new E/T/S/N items.** Two engineering items ride to Hasan (the
  Dockerfile Go version; local events omitting clOrdId from data).

## Next

1. **§10.3 checkpoints** — its own session: state snapshots, integrity
   hashes, replay-from-checkpoint equality.
2. **The live HTTP sources** (timeline + schedule) + the production
   runtime loop — the wire-test script is the prototype. Gated on S1/S7.
3. **Send the Edwin round E29–E37** + the E18 refinement.
4. **T1/T2 on the next T0 call**, with the UEPR re-probe.
5. The rig: `docker start mm-nats mm-gateway` revives it.
