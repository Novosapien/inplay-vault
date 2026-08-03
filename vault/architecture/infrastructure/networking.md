# Networking

> **Architecture:** [[architecture]]
> **Status:** Draft — ⚠ **except the "Live network reality" section below,
> which is verified and outranks the rest of this file.**

---

## ⭐ Live network reality (verified 2026-08-03) — GOSPEL

**Source:** `Novosapien/inplay-admin-panel-trading` — `proxy/.env.example`
(the deployed proxy's own configuration), plus its
`src/app/(dashboard)/health/page.tsx` and `resilience/page.tsx`.

**Ruling (George, 03-08): the live setup is gospel.** Where any vault
document disagrees with this table, this table wins.

| Component | Private IP | Port / notes |
|---|---|---|
| FIX gateway | `10.0.1.2` | health endpoint on `:8080/health` |
| NATS | `10.0.2.2` | `:4222`. Users `trading-service` and `admin` |
| Redis | `10.78.64.3` | `:6378`, **TLS** (`rediss://`) |
| Cloud SQL — `inplay-postgres` | `10.78.65.3` | PostgreSQL 15. Databases `inplay` and `zitadel` |
| Cloud SQL — `inplay-trading-db` | — | second instance; address not yet captured |

Also confirmed:

- The **trading admin panel** deploys to Vercel
  (`inplay-admin-panel-trading.vercel.app`) and reaches the private
  network only through its own **`proxy/`** — a Python FastAPI service
  running inside the VPC. The proxy speaks NATS, Redis and HTTP. It holds
  **no database client**.
- Weekly database dumps exist and export to GCS:
  `inplay-postgres-weekly.sql.gz`, `inplay-trading-db-weekly.sql.gz`,
  `zitadel-weekly.sql.gz`.
- **`zitadel`** is the identity provider, with its own database.

⚠ **`vault/drafts/VPC Setup.md` contradicts every address above** (it says
gateway `10.0.0.2`, NATS `10.0.2.2` → `10.0.0.3`, one `10.0.0.0/24`
subnet). That file belongs to another session, so this session did not
edit it, per the drafts convention. **Its owner should reconcile it or
mark it superseded.** Until then, read this section and not that file.

⚠ **Still unknown, and asked as MM open question N30:** the full subnet
layout. The live addresses span at least `10.0.1.x`, `10.0.2.x` and
`10.78.64–65.x`, so the single-subnet picture in the draft is wrong. The
market maker's own VM address depends on the answer. **For Hasan**, with
the Cloud NAT question.

---

## Domain Structure

| Domain | Target | Purpose |
|--------|--------|---------|
| `api.inplay.com` | API Gateway → Cloud Run services | All REST API traffic |
| `realtime.inplay.com` | Cloud Load Balancer → Centrifugo MIG | WebSocket connections |
| `app.inplay.com` | Cloud CDN | React Native web app bundle |
| `www.inplay.com` | Cloud Run (marketing site) | InPlay Global website |
| `challenge.inplay.com` | Cloud Run (marketing site) | Trading Challenge landing page |

## Network Architecture

```
Internet
  │
  ▼
Cloud Load Balancer + Cloud Armor (SSL, DDoS)
  │
  ├── api.inplay.com → API Gateway → 5 Cloud Run services
  │
  ├── realtime.inplay.com → Centrifugo MIG (WebSocket)
  │
  ├── app.inplay.com → Cloud CDN (static files)
  │
  └── www/challenge.inplay.com → Cloud Run (marketing)


Internal GCP network (private):
  Cloud Run services ←→ Cloud SQL (PostgreSQL)
  Cloud Run services ←→ Memorystore (Redis)
  Centrifugo MIG ←→ Memorystore (Redis)
  Cloud Run Jobs ←→ Cloud SQL + Memorystore


tZERO co-location:
  FIX Gateway VM ←FIX 4.2 TCP→ tZERO Exchange (<1ms)
  FIX Gateway VM ←Cloud Interconnect/VPN→ GCP Memorystore (Redis)
```

## Cloud CDN

Serves the React Native web app bundle (HTML + JS + CSS) from 100+ edge locations worldwide. Users download once (~3-5MB), cached after first load.

No server-side rendering. No compute. Just static file delivery. Cost: ~$50-100/month.

## tZERO Co-Location

The FIX Gateway VMs need <1ms latency to tZERO's matching engine. This requires:
- VMs physically close to tZERO (same data center or region)
- Cloud Interconnect or VPN link back to GCP for Redis/PostgreSQL access
- **Open question:** Where is tZERO's matching engine? This determines the VM location.

## SSL/TLS

- All external traffic over HTTPS/WSS
- SSL termination at Cloud Load Balancer
- Internal GCP traffic is unencrypted (private network, trusted)
- Centrifugo WebSocket connections use WSS (encrypted)
