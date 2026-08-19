---
description: "The as-built infrastructure page — the verified VPC layout, the MM VM, the publisher pools, the panel and the honest deployment-status table"
---

# Build — Infrastructure

> Part of [[market-maker/build/index|As Built]] · Sources: N7 (03-08) ·
> N29/N30 (03-08b) · the 04-08 rulings · the 06-08 server validation.
> ⚠ `vault/drafts/VPC Setup.md` is WRONG on every address (banner on the
> file). **The real layout, read directly from GCP 06-08b:** project
> `inplay-497712` · network `inplay-vpc` · us-east4-a · per-service
> subnets — `fix-gateway-subnet` 10.0.1.0/28 · `nats-subnet`
> 10.0.2.0/28 · `centrifugo-subnet` 10.0.3.0/28 · `cloudrun-subnet`
> 10.0.8.0/22. The firewall (`inplay-fw-policy`) is DENY-BY-DEFAULT
> with explicit per-source allows; a new VM needs its own rules (the
> retired loadrunner at 10.0.2.10 is the pattern: explicit ingress to
> NATS 4222 from its /32). SSH is via IAP. N30's residual ask for
> Hasan shrinks to: confirm the MM VM's placement + its two firewall
> rules.

## The production VPC (us-east4), as verified

| Host | Address | What it is |
|---|---|---|
| FIX gateway VM | `10.0.1.2` + a static PUBLIC IP | The tZERO-whitelisted host — the one single point of failure. FIX session 00:01–23:59 ET · 30 s boot grace · **10 s dead-man since 08-14** (env `MM_DEADMAN_TIMEOUT_MS=10000`, latching; was 4 s — the 08-13 fire loop; gateway PR #4 bumps the default) · MM governor 5,000 msg/s burst 2,000 (Hasan's guide 05-08 — supersedes the 50 msg/s placeholder) |
| NATS VM (`inplay-nats`) | `10.0.2.2` (no public IP) | e2-small, template `inplay-nats-tmpl`. **JetStream ON — validated on the server 06-08**: store `/data/nats/jetstream`, 10 GB disk / 256 MB memory cap; the gateway's streams already live there. Carries `order.mm1.>`, the heartbeat, and `SR_PROBABILITIES` |
| Redis | `10.78.64.3` (TLS) | Already in the panel's proxy — the intended home of the MM's LIVE projection (better than Postgres; adds no dependency) |
| Cloud SQL | `10.78.65.3` | PostgreSQL 15. The panel displays its health but reads nothing from it |

## The MM engine's home (VM created 06-08b; the engine AND the taker run on it)

Its own VM — **created 06-08b**: `inplay-market-maker`, `e2-medium`,
`nats-subnet` at `10.0.2.3` (static, `inplay-market-maker-ip`), no
public IP, SA `market-maker-sa`, journal disk `pd-ssd 50 GB` mounted at
`/var/lib/mm` with the `mm-journal-hourly` snapshot schedule (7-day
retention), firewall rules 2085/2086, IAP SSH. NATS reachability
verified from the VM. The full change-set + rollbacks:
`infra-changes-2026-08-06-mm-vm.md` (for Hasan). One process, one
writer:

- **Not Cloud Run** — scale-to-zero and container recycling are
  disqualified by the single-writer journal (`[second-writer]` is a stop
  condition). **Not the gateway VM** — never add load to the SPOF;
  inter-VM latency is under 1 ms anyway.
- **The journal lives on a dedicated persistent disk** (never the boot
  disk), hourly snapshots. §10.4's retention period is an unfilled
  policy slot.
- **Restart posture:** systemd `Restart=always` with a rate limit (~5 in
  60 s then stay down), alarm on repeats. Replay makes restart safe;
  between death and restart the gateway's dead-man clears the book, so
  no stale quotes rest. **No hot standby, by design** (two processes =
  two writers).
- **Every deploy is a restart** → §10.3 checkpoints are REQUIRED before
  the season (replay time grows with the journal).
- Cloud NAT exists (George, 04-08). After the go-live ingestion switch
  the engine needs NO internet egress at all — its world is the VPC bus.

## The sportradar service (the publisher's home)

The MM publisher runs in the service's **worker pool — never the
autoscaled API** (fixed-count; capacity is not the problem, availability
is). Availability is the **lease pair**: leader and standby both poll,
only the lease-holder publishes (`LeaseFence`, per-game — a fenced-out
fetch spends quota but publishes nothing). SR access is the trial
Probabilities key until S1's production allocation lands. Deployment
needs NATS reachability (`10.0.2.2`, in-VPC) — **confirm the firewall
path before the first deploy** (for Hasan, with N30).

## Monitoring (the panel — future)

`inplay-admin-panel-trading` (Next.js · Vercel) + its in-VPC FastAPI
`proxy/` (`nats-py` · `redis` · `httpx`). The MM panel is new pages plus
new proxy endpoints — **no new deployment unit**. Rules:

- **The panel NEVER reads the journal** (single-writer, internal
  format). Live state reads live over NATS/Redis through the proxy; the
  panel is a projection and will lag the venue — say so before the lag
  is reported as a bug.
- **Edwin's file history:** the **bucket** stores each file byte-for-byte
  as evidence (rejected files too, reason in object metadata; versioning
  now, the retention lock only when §10.4's period lands — a lock is
  irreversible); the **database** stores the parsed rows; the row
  carries the object's path and hash; **write the object first, then the
  row**. The database can always be rebuilt from the bucket, never the
  reverse.
- ⚠ **Access control before the MM control surface lands:** the panel
  carries `/loadtest`, `/stress-test`, `/resilience` and `nats/purge`;
  the kill switch would sit beside them. Roles exist — confirm which
  role gates what first.
- **Secrets:** Terraform surfaces them initially; the panel manages
  updates later.

## The local test bench

Docker network `mm-loopback`: `mm-nats` (`nats:2.10 -js`) + `mm-gateway`
(the real gateway binary, LOOPBACK_MODE). Revive with
`docker start mm-nats mm-gateway`; the from-scratch setup is documented
in `scripts/loopback_wire_test.py`. This is where the five-phase wire
test (02-08), the composition drill (05-08b) and the bus end-to-end
drill (06-08b) ran.

## Deployment status, honestly

| Piece | Status |
|---|---|
| Gateway VM · NATS (JetStream) · panel | Deployed (Hasan's side), verified against |
| MM publisher (service worker) | ⭐ **DEPLOYED 08-11** (George's freeze override): Cloud Run worker pools `inplay-mm-publisher` (prod) + `-testing`, image = the 08-11 main merge, `python -m app.workers.mm_publisher`, **1 instance each** (AlwaysOwns fence — 2 only when the C15 Redis lease lands). NATS via the pre-provisioned `sportradar` user (publish `sr.probabilities.>` + SR_PROBABILITIES JS API; firewall rule 2024 already allowed Cloud Run → 4222). **Probabilities on `/production/v1`** (S1 landed; the code default "trial" is overridden by `PROBABILITIES_ACCESS_LEVEL` env — the trial quota was half-burned). Both pools verified: NATS connected, discovery 200. Terraform-managed (prod pool imported after a parallel session hand-created it). ➕ **13-08: the universe-filter hotfix on BOTH pools** ~20 min before the first live games (prod `hotfix/mm-publisher-universe-filter` @`d877b26`, cut from the running SHA `f8c8aef`; testing @`daf5604`) — before it the publisher had NEVER adopted a game (session 2026-08-13-e; ⚠ **PR #37** carries the fix but is a full testing→main promotion — 65 commits; the one-hunk `hotfix/…@d877b26` has no PR — see [[market-maker/build/ingestion|Ingestion]]; **N39** is the proper fix). Two publishers deliberately feed one bus since then (idempotent readings). The engine consumes the stream since 08-11 (`MM_READINGS=bus`); the taker's schedule feed rides it too. ⚠ Cloud Run: carry `--instances=1` on every pool update or the worker dies ("user disabled instance") |
| MM engine | ⭐ **RUNNING on the VM, bus-fed (`MM_READINGS=bus`) since 08-11.** Coordinates: **`supervised28`/CFG-0026 since 11:51Z 14-08** — the bundled deploy LANDED (gateway `main@124991e` with tag-9383 forwarding, backup `.bak-005fdd8` · engine `feat/always-quoting-step4b@db45300`, converger on its OWN task at 0.25 s · taker boot rebase ACTIVE); 1,664 instructions / 180 books. Previous: `supervised27`/CFG-0025 (00:19Z 14-08, the dead-man-window cutover). ⚠ **The VM outruns this page — read [[market-maker/build-deploy-log]] for the current row, and `~/run_supervised*.sh` on the VM for the truth.** The 08-13/14 chain: `supervised21`/CFG-0020 (always-quoting steps 1–3) → `supervised23`/CFG-0022 (converger) → `supervised25`/CFG-0023 (the union: state publishers + converger + the 1.0 s sweep tolerance + the single-engine lock) → `supervised26`/CFG-0024 (`g2-throttle`, converger budget 128, deployed mid-game) → `supervised27`/CFG-0025 (post fire-loop, fresh journal). ⚠ Standing: a fresh-journal cutover during a live game rebases `p_ref` and erases the in-game move ([[market-maker/build/valuation|Valuation]]) — George's carry ruling owed. Deploys go by git bundle over IAP scp (the VM repo has no GitHub remote). Live mode still refuses on its gates. Older history: `supervised17` (CFG-0016) — the BOUNDARY BUILD deployed (MM PR #24 + #22 merged): fork-based checkpoints (no more hourly stall-sweeps) · gone-retire (no more phantom storms) · the session clock (close 23:59 ET / open 00:02 ET — tonight is the live test). `~/run_supervised17.sh`, journal `/var/lib/mm/supervised17/`, 180/180 two-sided verified. History: `supervised16` (CFG-0015) — restarted clean after the SESSION-ROLL STORM (tZERO's 00:01 ET boundary silently wiped ~750 resting orders → 8 h phantom-cancel storm + 56 dead-man fires; see [[market-maker/sessions/2026-08-12-session-roll-storm]]; ⚠ recurs nightly until the engine-side UNKNOWN-ORDER retire or a boundary strategy lands). 180/180 two-sided verified post-restart; all 180 MD subscriptions healed (`POST /md/book-resubscribe` now needs `X-Ops-Key` — Secret Manager `inplay-fix-gateway-ops-key`). History: `supervised14` (CFG-0013): ALL 180 BOOKS incl. the ten `.TEST` twins (MM PR #22 `edd9512` deployed by bundle — `resolve_security()` mints twins). `~/run_supervised14.sh`, inputs `~/supervised-inputs-180.json`, journal `/var/lib/mm/supervised14/`. **ALL 180 BOOKS STAND** (the ten `.TEST` quoting; JETS unblocked 23:3x by the anchor walk — T20 closed, session note addendum 3). Earlier same night: `supervised13`/CFG-0012 on **the 170 production tickers** (inputs `~/supervised-inputs-170.json` from `ipo-prices-170.csv`: E[Wins] + Off-Field EV per team, NFL 17 games / NCAA 12), journal `/var/lib/mm/supervised13/`, `MM_READINGS=bus`, same identity. **169/170 stood** (1,532 instructions; the empty-book gate proven gone). ✎ The `.TEST` refusal that run exposed is FIXED by PR #22. supervised12's AND supervised13's journals are PRESERVED untouched (C2 + the gate evidence). Earlier state (supervised12/CFG-0011, six books) retired at 22:43Z; deploys still by git bundle. Live mode still refuses on its gates |
| SNT-1 taker | ⭐ **RUNNING `snt-1.service` on ALL 180 books.** Coordinates: **SNT-CFG-0019, journal `/var/lib/mm/snt16`, filling since 12:09:59Z 14-08** — code root `~/snt-checkout` on branch **`step4b-wash` @ `5b10d68`** (origin/main merged into step4b: the FIRST binary carrying BOTH the wash guard and the boot rebase); floats = env base + snt15 drift (123 books); no halts. Own account `4963224393`, `snt-taker` NATS user, `SNT_STATE=AUTO`. ⚠ **Runbook fact (learned 14-08): the taker's code root is `~/snt-checkout` via PYTHONPATH** — the systemd ExecStart's venv path (`~/inplay-market-maker/.venv/...`) says NOTHING about which tree imports; verify with `/proc/PID/environ`, never the unit file. (A false regression alarm rode exactly this: CFG-0018 read as step4b@`db45300` from the venv path, but PYTHONPATH held `snt-checkout` @ `main@772e79c` — the wash guard never regressed; the boot rebase simply had not shipped until CFG-0019.) Shorts merged but OFF (`SNT_SHORTS` unset). Every deploy: halt → stop → new binary → CFG bump + fresh journal + floats recomputed from the RUNNING env → start. ⚠ Read `/etc/snt-1/env` for the truth — the operating sessions cut it faster than the vault. Older history (08-12, SNT-CFG-0012 era): journal `snt9`, `SNT_MINUTES=0`. ⚠ **Every book's float is explicit in `SNT_FLOAT_OVERRIDES` (LOAD-BEARING)**: all 180 recomputed at the CFG-0009 cutover per rule 7 (snt5's 529 fills over 152 books folded in — e.g. COWB 3811 · RAVE 4168 · CHIE 5124; the ten `.TEST` at their seeded 5,000; ledger has both seed sections). First fills passed T-S05 — the seed is venue-agreed. History: one-owner reconciliation earlier the same evening (SNT-CFG-0007, journal snt4, nohup retired — requirements addendum 2026-08-11e). Code: `~/snt-checkout` @ `5681767`. Control: `snt.control.snt-1`. ⚠ 08-12 21:46: restarted after a 20-HOUR undetected HALT (the predicted +31 VATH float error fired at 01:16; the afternoon health check missed it — see the 08-12 session note addendum 4). VATH now pinned to the venue's 4359. History 08-12 01:11: T-S05's first production-class catch (a lost `order.>` exec report, VATH) → CFG-0010 recovered on a stale base (caught by T-S05 again in 10 s) → CFG-0011 on the CFG-0009 base, venue-confirmed via the AUBT halt line. The `snt-taker` NATS user gained `$JS.FC.SR_PROBABILITIES.>` publish (flow control; conf `.bak-fc-20260812`). ⚠ T-F07 boot-LIVE redelivery wrinkle fired at every restart — the `fetched_at` staleness fix is the taker's top build item; see the 08-11 full-book session note addenda 5–7 |
| CI/CD for both | **Audit owed at end of implementation** (George, 06-08): testing + prod deploys for the sportradar API and workers incl. the publisher's slot, and the MM engine's deploy story |
