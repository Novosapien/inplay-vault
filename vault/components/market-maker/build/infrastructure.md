# Build — Infrastructure

> Part of [[market-maker/build/index|As Built]] · Sources: N7 (03-08) ·
> N29/N30 (03-08b) · the 04-08 rulings · the 06-08 server validation.
> ⚠ `vault/drafts/VPC Setup.md` is WRONG on every address (banner on the
> file); the live truth for addresses is the trading panel's
> `proxy/.env.example`; the full subnet layout is N30 (Hasan).

## The production VPC (us-east4), as verified

| Host | Address | What it is |
|---|---|---|
| FIX gateway VM | `10.0.1.2` + a static PUBLIC IP | The tZERO-whitelisted host — the one single point of failure. FIX session 00:01–23:59 ET · 30 s boot grace · 4 s dead-man · 50 msg/s MM governor (placeholder) |
| NATS VM (`inplay-nats`) | `10.0.2.2` (no public IP) | e2-small, template `inplay-nats-tmpl`. **JetStream ON — validated on the server 06-08**: store `/data/nats/jetstream`, 10 GB disk / 256 MB memory cap; the gateway's streams already live there. Carries `order.mm1.>`, the heartbeat, and `SR_PROBABILITIES` |
| Redis | `10.78.64.3` (TLS) | Already in the panel's proxy — the intended home of the MM's LIVE projection (better than Postgres; adds no dependency) |
| Cloud SQL | `10.78.65.3` | PostgreSQL 15. The panel displays its health but reads nothing from it |

## The MM engine's home (designed 03-08 — the VM does NOT exist yet)

Its own VM, **`e2-medium`, same subnet as NATS**. One process, one
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
| MM publisher (service worker) | Built + drilled locally · **NOT deployed** (firewall path + worker-pool slot open) |
| MM engine | Built + drilled in loopback · **NOT deployed** (no VM; live mode refuses on its gates) |
| CI/CD for both | **Audit owed at end of implementation** (George, 06-08): testing + prod deploys for the sportradar API and workers incl. the publisher's slot, and the MM engine's deploy story |
