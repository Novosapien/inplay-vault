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

Cloud Run Jobs (scheduled batch processing)
├── Leaderboard recalculation (every 5-15 seconds)
├── End-of-day settlement (daily after market close)
└── Referral reward processing (triggered on KYC completion)

Managed Instance Group (long-lived WebSocket connections)
└── Centrifugo VMs (3-25 VMs, schedule-controlled)

Compute Engine VMs (persistent FIX sessions)
├── FIX Gateway Primary (co-located with tZERO)
└── FIX Gateway Standby (co-located with tZERO)

Managed Services
├── Cloud SQL (PostgreSQL)
├── Memorystore (Redis)
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

### Memorystore (Redis)

Three roles:
1. **Pub/Sub** -- market data channels, order events, leaderboard updates. FIX Gateway publishes, Centrifugo subscribes.
2. **Sorted Sets** -- leaderboard rankings (12 total: 3 verticals × 4 timeframes). Written by Cloud Run Jobs, read by Social Service.
3. **Cache** -- wallet balances, session tokens, user profiles, market data last-value cache, FIX sequence numbers, pre-computed ad targeting segments.

### Cloud Load Balancer + Cloud Armor

- SSL termination for all domains
- DDoS protection via Cloud Armor WAF rules
- Basic rate limiting at the edge
- Health checks for all services

### Cloud CDN

Serves the React Native web app bundle (HTML + JS + CSS). Static files cached at 100+ edge locations worldwide. Users download the app once (~3-5MB), cached after first load.

### Cloud Scheduler

Triggers:
- Leaderboard recalculation Cloud Run Job (every 5-15 seconds)
- End-of-day settlement Cloud Run Job (daily)
- Game-day scaling commands (pre-kickoff: scale up min-instances and Centrifugo MIG; post-game: scale down)
