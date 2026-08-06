# 2026-08-06c — build/ becomes the source of truth · the VM exists · Hasan's guide lands

> **Who:** George + Claude (same chat session as 06-08b, continued —
> split into its own note because the work moved from the consumer build
> to vault structure, infrastructure and intake)
> **Type:** vault restructure · infra build · document intake
> **Refs:** vault commits `de2d3f3` → this one · MM repo `5949ca9`
> (CLAUDE.md) · the VM change-set `infra-changes-2026-08-06-mm-vm.md` ·
> Hasan's guide `reference/mm-build-guide-hasan-2026-08-05.md` ·
> decisions `2026-08-06c`. ⚠ All commits LOCAL, unpushed.

## What we did

1. **The vault archive passes (George: "fix what you're sure is
   stale").** `vault/archive/` + `market-maker/archive/` created with
   the convention (nothing in them is current; every item names its
   replacement). Archived: the 31-07 project-status snapshot set · the
   VPC draft got a WRONG banner (kept in place, it is cited by path) ·
   the call-prep sheets · `mm-pipeline.html` · the May architecture
   draft · **the four built systems' design docs** (valuation, market
   state, quoting, decision-cycle pseudocode) — `systems/` keeps only
   the three UNBUILT systems. N7/N29 housekept below the fold.
2. **`build/` — the as-built SOURCE OF TRUTH (George's ask, then split
   at his direction).** Eleven pages: index (charter: what-is-built ·
   what-to-build · the change anchor) + event-core · ingestion ·
   valuation · position · quoting · market-state · venue · runtime ·
   infrastructure · next. Every equation verified against code; spec
   anchors + named deviations throughout. Wired into the working guide
   (deep reference + session loop line), the hub, and the MM repo's
   `CLAUDE.md` (read the page before changing its part; update after).
3. **The §10.3 checkpoints design agreed** (recorded in build/next.md):
   five steps ending in the replay-equality proof on the real game;
   local-disk storage with the journal disk's hourly snapshots as the
   external copy; the dedup-retention companion (prune seen keys past
   the one-week redelivery bound, deterministically on event time).
4. **⭐ The MM VM CREATED** (`inplay-market-maker`, e2-medium,
   nats-subnet 10.0.2.3 static, no public IP, `market-maker-sa`,
   pd-ssd 50 GB journal disk at `/var/lib/mm`, hourly snapshots,
   firewall rules 2085/2086 on the loadrunner pattern, IAP SSH). All
   additive; NATS 4222 verified reachable from the VM; engine NOT
   deployed. **The hand-off file for Hasan:**
   `infra-changes-2026-08-06-mm-vm.md` — every command + rollback.
   ⚠ George owes the send + confirmation.
5. **The real VPC layout read directly from GCP** (N30 largely
   answered): project `inplay-497712`, `inplay-vpc`, per-service /28
   subnets, deny-by-default `inplay-fw-policy` with per-source allows,
   IAP SSH. Recorded on the infrastructure page.
6. **⭐ Hasan's build guide (05-08, live-verified) landed** — filed
   verbatim in `reference/`, intake in decisions `2026-08-06c`:
   **T1 ANSWERED** (venue account `1797733477`, $1bn cash/DTBP) ·
   **T2 ANSWERED** (governor 5,000 msg/s burst 2,000 — ✂ supersedes
   the 50 placeholder; `MaxOrdRate` 5,000/s, `MaxDupOrdRate` 200/s) ·
   position-transfer mechanics (one-way, non-idempotent, no read-back
   → keep a ledger) · price cap $127.50 · `market.*` subjects live ·
   dead-man detail (latching, arming, 30 s grace). **Two conflicts:**
   wash-trade blocking ON rejects self-crosses (vs N12 post-first) ·
   the beat is tick-tied (guide wants it independent). **One new ask:**
   NATS per-user auth (05-08) has no grants for `sr.probabilities.>`
   — the readings path cannot run on production NATS without them.
7. **Where WE out-date the guide** (tell Hasan): float = 900k/1M (his
   875k/5M both dead) · RP exists (our engine, 534 tests) and the
   readings stream rides his own NATS · the ASMM-1 re-cut replaced λ ·
   our measured peak is ~35 concurrent games (his math says 17).
8. **Trading-service reality check:** `inplay-trading-service` cloned —
   Scope A (IPO buys against an in-DB simulated float, NO tZERO). So
   the MM platform account tests the user/IPO plane only; the venue
   plane is gateway-only. Gateway repo pulled (+`9c51125`: his
   JetStream dedup key fix — the same ExecID lesson we learned).
9. **Wire-contract check found a real gap:** our new-order payload has
   NO `account` field (required, FIX Tag 1; loopback never noticed).
   With: real `userId` at composition, the $127.50 collar, the
   independent beat. **Env design (George): identity/deployment facts
   ride env vars via Settings (`MM_VENUE_ACCOUNT` · `MM_USER_ID` ·
   `MM_BOT_ID` · NATS creds from Secret Manager); book-visible numbers
   stay in the Configuration Dictionary.**
10. **N15 position set:** window and beat move together — 4 s is right
    for the 1/s tick-tied beat; independent ~250 ms timer → measure
    jitter on the VM → tighten to ~1–1.5 s.
11. **Credentials:** the MM platform account (Zitadel) stored at
    `~/Programming/inPlay/.mm-account-credentials` (outside git, 600).
    The NATS `market-maker` token verified readable from Secret
    Manager.

## Decisions *(mirrored into decisions.md 06-08c + build/next.md)*

- build/ is the source of truth; systems/ = unbuilt-only; archive
  convention vault-wide.
- Checkpoints design + dedup retention (details in build/next.md).
- e2-medium to start; resize after measurement.
- Additive-only infra changes, everything in a file for Hasan.
- Env vs dictionary split for identity vs behaviour.
- N15: 4 s now; retune with the independent beat.

## Questions opened / closed

- **T1, T2 CLOSED** (Hasan's guide). **N30 largely closed** (read from
  GCP; residual: Hasan confirms placement + the two rules).
- **OPENED:** the wash-trade-vs-N12 decision (with Hasan, before the
  first venue drill) · the NATS grants for `sr.probabilities.>` (ours
  to add or Hasan's) · N15's retune (after jitter measurement).

## Next

The wire-contract fixes + §10.3 checkpoints build (designs agreed, no
open questions); the Hasan conversation alongside (infra file + wash
trade + NATS grants + his stale facts). Then deploy + drill.
