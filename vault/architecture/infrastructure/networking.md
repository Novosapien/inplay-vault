---
description: "Network layout — the five inplay.com domains and their targets, internal GCP paths, tZERO co-location (<1ms FIX link), and SSL termination points"
---

# Networking

> **Architecture:** [[architecture]]
> **Status:** Draft

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
