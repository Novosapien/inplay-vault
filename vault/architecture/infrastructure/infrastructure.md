---
description: "GCP deployment map — every Cloud Run service, job, VM and managed service (NATS, Redis, Cloud SQL), with domain routing and game-day scaling triggers"
---

# GCP Infrastructure Overview

> **Architecture:** [[architecture]]
> **Status:** Draft

## Deployment Model

```
Cloud Run Services (5 API services, auto-scaling)
├── Trading Service      /trading/*     min=50 game day
├── Auth Service         /auth/*        min=10 game day
├── Market Data Service  /market/*      min=20 game day
├── Social Service       /social/*      min=10 game day
└── Ad Service           /ads/*         min=10 game day

Cloud Run Services (persistent, event-driven)
└── Leaderboard Service   (subscribes to NATS, updates Redis sorted sets in real-time)

Cloud Run Jobs (scheduled batch processing)
├── End-of-day settlement (daily after market close)
└── Referral reward processing (triggered on KYC completion)

Managed Instance Group (long-lived WebSocket connections)
└── Centrifugo VMs (3-25 VMs, schedule-controlled)

Compute Engine VMs (persistent FIX sessions)
├── FIX Gateway Primary (co-located with tZERO)
└── FIX Gateway Standby (co-located with tZERO)

NATS JetStream (message backbone, 3-node cluster)
└── All real-time messaging: market data, orders, fills, events

Managed Services
├── Cloud SQL (PostgreSQL)
├── Memorystore (Redis -- cache and data structures only, NOT messaging)
├── Cloud Load Balancer + Cloud Armor
├── Cloud CDN (serves React Native web app bundle)
├── Google Cloud API Gateway
└── Cloud Scheduler (triggers Cloud Run Jobs + game-day scaling)
```

## Domain Routing

```
realtime.inplay.com      → Centrifugo (Managed Instance Group)
api.inplay.com/auth/*    → Auth Service (Cloud Run)
api.inplay.com/trading/* → Trading Service (Cloud Run)
api.inplay.com/market/*  → Market Data Service (Cloud Run)
api.inplay.com/social/*  → Social Service (Cloud Run)
api.inplay.com/ads/*     → Ad Service (Cloud Run)
app.inplay.com           → React Native web app (Cloud CDN)
www.inplay.com           → Marketing site (Cloud Run, scales to zero)
```

## Managed Services Detail

### Cloud SQL (PostgreSQL)

Primary persistent data store for all services.

Tables: users, orders, positions, wallets, referrals, teams, games, news, campaigns, impressions, leaderboard snapshots, KYC records.

All 5 Cloud Run services read/write to the same Cloud SQL instance. Services do NOT call each other -- they share data through the database.

### NATS JetStream (Message Backbone)

3-node cluster for high availability. Handles all real-time messaging:
- Market data (quotes, trades, book updates, security status)
- Order lifecycle events (new, fill, cancel, reject)
- Position/P&L updates
- Game events (from Sport Radar)
- Ad triggers and leaderboard updates

Centrifugo uses NATS as its broker natively -- publishes to NATS are automatically delivered to WebSocket clients. JetStream provides persistence: if a service restarts, it replays missed messages on reconnect.

### Memorystore (Redis)

Two roles (NOT used for messaging -- NATS handles that):
1. **Sorted Sets** -- leaderboard rankings (12 total: 3 verticals × 4 timeframes). Updated incrementally by Leaderboard Service (event-driven via NATS), read by Social Service.
2. **Cache** -- wallet balances, session tokens, user profiles, FIX sequence numbers, pre-computed ad targeting segments, geo queries (GEORADIUS for ad targeting).

### Cloud Load Balancer + Cloud Armor

- SSL termination for all domains
- DDoS protection via Cloud Armor WAF rules
- Basic rate limiting at the edge
- Health checks for all services

### Cloud CDN

Serves the React Native web app bundle (HTML + JS + CSS). Static files cached at 100+ edge locations worldwide. Users download the app once (~3-5MB), cached after first load.

### Cloud Scheduler

Triggers:
- Game-day scaling commands (pre-kickoff: scale up; post-game: scale down)
- End-of-day settlement Cloud Run Job (daily)
- Game-day scaling commands (pre-kickoff: scale up min-instances and Centrifugo MIG; post-game: scale down)
