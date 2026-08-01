# 2026-08-01 — Chapter 8 built in one run · the loop closes

> **Who:** George + Claude (first session under the autonomous integration mode)
> **Type:** build session — plan stated up front, then autonomous; review at
> the chapter boundary
> **Refs:** `inplay-market-maker` branch `feat/position-engine`, commits
> `56efd57` → `425a58e` · `inplay-fix-gateway-go` pulled to `9c0c4cd` ·
> spec §8, §4.4, §7.5, §6.3

## What we did

**The machine now talks in the gateway's language, end to end.** Event in →
priced → positioned → quoted → diffed against the venue's confirmed book →
gateway-shaped instructions out, with fills and acks flowing back through
the real adapter path. **329 → 385 tests**, ruff and `mypy --strict` clean.
Four build commits plus the BUILD-LOG, one piece each, no waiting between
pieces — the mode worked as designed.

| Commit | What |
|---|---|
| `56efd57` | `adapters/gateway.py` + `venue/engine.py` — the translator and the Venue State Record (§8.1, §8.2, §4.4) |
| `3b590cc` | `orchestration/engine.py` — accept → fan out → assemble §7.5 inputs → cycle |
| `e7bdecb` | `venue/reconciler.py` — the diff: keep / replace-with-remainder / submit / cancel, post-first |
| `4f12ab6` | `venue/transport.py` + `venue/sync.py` — gateway payloads, heartbeat, §6.3 kill switch |
| `425a58e` | BUILD-LOG brought current |

Before any code: pulled the gateway repo (6 new commits, all MM-relevant)
and ran two codebase-research agents — one mapped the full MM↔gateway wire
contract from Hasan's source, one mapped our own integration surface. Both
reference files are in the session scratchpad; the contract findings are
now baked into the adapter's fixtures and Notes blocks.

## What we learned

- **⭐ tZERO recycles ExecIDs.** Not a theory — a real 100-share fill was
  silently dropped on 29-07 because the gateway keyed dedup on ExecID
  alone (its commit `e37cd3d`). Our §7.3 EXECUTION key now carries the
  client order id. The spec's own key basis was unsafe against the venue.
- **⭐ The venue keeps the book when we die.** No cancel-on-disconnect
  (probe-verified), no FIX 4.2 mass-cancel. The gateway's dead-man sweep is
  the only cleanup, our heartbeat feeds it, and a bot that restarts slower
  than the 30 s boot grace finds its own quotes swept — heartbeat first,
  reconcile second.
- **DAY orders die nightly at 23:59 ET** (`ORDER_DONE_FOR_DAY`, a terminal
  state the spec's §8.2 table lacks). The nightly vanish-and-repost is
  book-visible → **E36**, the one genuinely-Edwin question the chapter
  produced.
- **The gateway gives no ack that a message even reached it** — malformed
  JSON is a silent drop. Hence register-intent-first: §4.4 exposure begins
  when we decide to send, not when the venue answers.
- **The E27 venue leg may be alive after all.** The UEPR seeding probe drew
  nothing on 28-07, but tZERO turned the message family on later that day
  (UEAR answers in 12–17 ms). Re-probe before the T1 conversation.
- **Convergence over rounds beats perfection in one.** The reconciler
  leaves in-flight orders alone (one request per order, the gateway's own
  registry rule) and picks up whatever settled on the next cycle. Much
  simpler than trying to plan around races, and it matches how the venue
  actually behaves.

## What went wrong

- **The adapter initially laundered floats through `str()`** — a
  float-parsed message would have translated cleanly with plausible-looking
  numbers. The test that expected a refusal caught it; the adapter now
  refuses floats explicitly rather than converting them.
- **Two ruff errors slipped into a commit** because piping lint output
  through `tail` masked the exit code. Caught one commit later and amended;
  the lesson is not to pipe the gate.

## Decisions *(mirrored into [[market-maker/decisions]], 01-08b)*

EXECUTION idempotency key gains client_order_id (venue fact) · DONE_FOR_DAY
is a terminal order state (venue fact) · TIF built as DAY behind one
constant (→ E36) · §4.4 exposure includes Partially Filled (recorded) ·
intent registered before send · deterministic ClOrdIDs (MM + 16 hex
SHA-256) · the §7.5 sequence threaded through to the book · overnight
books read CURRENT, never stale · rest-until-gone implemented in the
reconciler exactly per N10/N12.

## Questions

- **Opened:** **E36** — DAY vs GTC: should the book vanish at midnight?
  (Built as DAY; one constant changes it. Plus a T0 detail: what happens at
  their session boundary exactly?)
- **Updated:** **E27** — re-probe UEPR; tZERO enabled the message family
  hours after the null result.
- **Unchanged and still the risks:** E27 (the day-one book), E25 (the
  deadline), E17 (now also the reconciler's lifecycle fork), T1/S1/S7
  (everything live-testing needs).

## Next

1. **The poller** — probability ingestion + N16 official results + driving
   the heartbeat; buildable against replay now, live use gated on S1/S7.
2. **Fix-pass step 5** — rejection audit records (§7.2 at the door).
3. **Ch 12 config sweep** — the `CONFIGURED` markers are all placed.
4. **The NATS adapter** — one Protocol method, when T1 grants the ACL.
5. Send the Edwin round: E29–E36 + the E18 refinement.
