# InPlay Trading Challenge -- Technical Architecture

**Status:** Draft
**Date:** 2026-05-09
**Owner:** Novosapien
**Sources:** Vision document, tZERO integration spec, architecture workshop sessions

---

## 1. Overview

The InPlay Trading Challenge is a simulated sports equity trading platform targeting 1M concurrent users at peak load. Users trade team stocks during live NFL and college football games using simulated currency, competing for real cash prizes.

This document describes the technical architecture for the trading challenge -- not the production trading platform.

---

## 2. System Architecture Diagrams

### 2.1 Full System Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                    CLIENTS                                           │
│                                                                                      │
│                     React Native (Expo) -- iOS, Android, Web                         │
│                              Single codebase                                         │
│                                                                                      │
│         ┌──────────────────────────┐          ┌──────────────────────────┐            │
│         │  Real-Time Streams       │          │  User Actions (REST)     │            │
│         │                          │          │                          │            │
│         │  • Price ticks           │          │  • Place/cancel orders   │            │
│         │  • Order book updates    │          │  • Sign up / login       │            │
│         │  • Trade executions      │          │  • KYC submission        │            │
│         │  • Fill confirmations    │          │  • Referral code entry   │            │
│         │  • Game events           │          │  • Wallet operations     │            │
│         │  • Leaderboard updates   │          │  • Follow/unfollow teams │            │
│         │  • Security halts        │          │  • Browse teams/stats    │            │
│         └────────────┬─────────────┘          └─────────────┬────────────┘            │
│                      │ WebSocket (wss://)                    │ HTTPS                  │
└──────────────────────┼──────────────────────────────────────┼────────────────────────┘
                       │                                       │
                       │                                       │
┌──────────────────────┼───────────────────────────────────────┼────────────────────────┐
│                      │          EDGE LAYER (GCP)             │                        │
│                      │                                       │                        │
│                      │     Cloud Load Balancer + Cloud Armor                          │
│                      │     ┌─────────────────────────────────┐                        │
│                      │     │  • SSL termination              │                        │
│                      │     │  • DDoS protection              │                        │
│                      │     │  • Path-based routing            │                        │
│                      │     └──────────────┬──────────────────┘                        │
│                      │                    │                                            │
│                      │          API Gateway                                           │
│                      │     ┌─────────────────────────────────┐                        │
│                      │     │  • JWT validation at the edge   │                        │
│                      │     │  • Per-user rate limiting        │                        │
│                      │     │  • Circuit breaking              │                        │
│                      │     └──────┬───────────────┬──────────┘                        │
│                      │            │               │                                    │
│               realtime.inplay.com │               │                                    │
│                      │    /trading/*         everything else                           │
│                      │            │               │                                    │
└──────────────────────┼────────────┼───────────────┼──────────────────────────────────┘
                       │            │               │
          ┌────────────▼──┐  ┌─────▼────────┐  ┌───▼──────────────┐
          │               │  │              │  │                  │
          │  CENTRIFUGO   │  │   TRADING    │  │    MAIN API      │
          │  (Cloud Run)  │  │   SERVICE    │  │    (Cloud Run)   │
          │               │  │  (Cloud Run) │  │                  │
          │  WebSocket    │  │              │  │  Auth, KYC,      │
          │  fan-out to   │  │  Order       │  │  referrals,      │
          │  1M+ clients  │  │  validation, │  │  news, ads,      │
          │               │  │  wallet,     │  │  leaderboards,   │
          │  Subscribes   │  │  positions   │  │  notifications,  │
          │  to Redis     │  │              │  │  teams, stats    │
          │  channels     │  │              │  │                  │
          │               │  │              │  │  Calls tZERO     │
          │  Last-value   │  │  Publishes   │  │  REST API for    │
          │  cache        │  │  orders to   │  │  non-real-time   │
          │               │  │  Redis queue │  │  operations      │
          │  Conflation   │  │              │  │                  │
          │  (10/sec/sym) │  │              │  │                  │
          └───────┬───────┘  └──────┬───────┘  └──────┬───────────┘
                  │                 │                  │
                  │                 │                  │
                  ▼                 ▼                  ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              REDIS (Memorystore)                                     │
│                                                                                      │
│  ┌──────────────────┐  ┌───────────────────┐  ┌──────────────────┐                   │
│  │  Pub/Sub          │  │  Sorted Sets      │  │  Cache           │                   │
│  │                   │  │                   │  │                  │                   │
│  │  market.quote.*   │  │  leaderboard:     │  │  wallet:{userId} │                   │
│  │  market.book.*    │  │   pnl:daily       │  │  session:{token} │                   │
│  │  market.trade.*   │  │   pnl:weekly      │  │  profile:{userId}│                   │
│  │  market.snapshot.*│  │   pnl:monthly     │  │  last-value:     │                   │
│  │  market.status.*  │  │   pnl:season      │  │   market.*       │                   │
│  │  market.session   │  │   risk:daily      │  │  fix:seqnum:*    │                   │
│  │  order.*.*        │  │   risk:weekly     │  │                  │                   │
│  │  position.*       │  │   risk:monthly    │  │                  │                   │
│  │  leaderboard.*.*  │  │   risk:season     │  │                  │                   │
│  │                   │  │   comeback:daily  │  │                  │                   │
│  │  Order Queue      │  │   comeback:weekly │  │                  │                   │
│  │  (Trading Svc →   │  │   comeback:monthly│  │                  │                   │
│  │   FIX Gateway)    │  │   comeback:season │  │                  │                   │
│  └──────────────────┘  └───────────────────┘  └──────────────────┘                   │
│                                                                                      │
└──────────────────────────────────────────────┬──────────────────────────────────────┘
                                               │
                                               │
┌──────────────────────────────────────────────┼──────────────────────────────────────┐
│                   tZERO CO-LOCATION          │                                      │
│                                              │                                      │
│  ┌───────────────────────────────────────────▼──────────────────────────────────┐   │
│  │                     FIX GATEWAY (Compute Engine VM)                           │   │
│  │                                                                              │   │
│  │  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐              │   │
│  │  │  IOI Adapter     │ │  MD Adapter      │ │  OE Adapter      │              │   │
│  │  │                  │ │                  │ │                  │              │   │
│  │  │  Parses IOI      │ │  Parses quotes,  │ │  Sends orders,   │              │   │
│  │  │  messages for    │ │  trades, OHLC,   │ │  receives fills, │              │   │
│  │  │  order book      │ │  security status │ │  cancels,        │              │   │
│  │  │                  │ │                  │ │  position/P&L    │              │   │
│  │  │  FIX 4.2         │ │  FIX 4.2         │ │  FIX 4.2         │              │   │
│  │  │  IOI v1.2        │ │  MD v8           │ │  OE v2.2         │              │   │
│  │  └────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘              │   │
│  │           │                    │                     │                        │   │
│  │           │        ◄── all <1ms to tZERO ──►         │                        │   │
│  │           │                    │                     │                        │   │
│  └───────────┼────────────────────┼─────────────────────┼────────────────────────┘   │
│              │                    │                     │                            │
│              ▼                    ▼                     ▼                            │
│  ┌──────────────────────────────────────────────────────────────────────────────┐   │
│  │                          tZERO EXCHANGE (ATS)                                │   │
│  │                                                                              │   │
│  │  Order matching · Price discovery · Execution reports · Market data           │   │
│  └──────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                     │
│  ┌──────────────────────────────────────────────────────────────────────────────┐   │
│  │  FIX GATEWAY STANDBY (Compute Engine VM)                                     │   │
│  │  Monitors primary health · Takes over on failure (~5-10s) · Same 3 adapters  │   │
│  └──────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           GCP MANAGED SERVICES                                       │
│                                                                                      │
│  ┌───────────────────┐  ┌──────────────────┐  ┌────────────────────────────────┐     │
│  │  Cloud SQL        │  │  Cloud Scheduler │  │  Cloud Run Jobs                │     │
│  │  (PostgreSQL)     │  │                  │  │                                │     │
│  │                   │  │  Triggers jobs   │  │  • Leaderboard recalc (5-15s)  │     │
│  │  Users, orders,   │  │  on schedule     │  │  • End-of-day settlement       │     │
│  │  positions,       │  │                  │  │  • Referral reward processing   │     │
│  │  wallets,         │  └──────────────────┘  └────────────────────────────────┘     │
│  │  referrals,       │                                                               │
│  │  leaderboard      │                                                               │
│  │  snapshots,       │                                                               │
│  │  ad inventory,    │                                                               │
│  │  KYC records      │                                                               │
│  └───────────────────┘                                                               │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           EXTERNAL SERVICES                                          │
│                                                                                      │
│  ┌───────────────┐  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────┐   │
│  │  Sport Radar  │  │  Persona     │  │  FCM / APNs  │  │  tZERO REST API       │   │
│  │               │  │              │  │              │  │                       │   │
│  │  Live game    │  │  KYC:        │  │  iOS push    │  │  Account mgmt         │   │
│  │  data, stats, │  │  age 18+,    │  │  Android     │  │  Historical data      │   │
│  │  news feed    │  │  identity,   │  │  push        │  │  Symbol reference     │   │
│  │               │  │  bot detect  │  │              │  │                       │   │
│  │  Called by:   │  │              │  │  Called by:   │  │  Called by:            │   │
│  │  Main API     │  │  Called by:  │  │  Notification │  │  Main API             │   │
│  │               │  │  Main API   │  │  Service      │  │                       │   │
│  └───────────────┘  └──────────────┘  └──────────────┘  └───────────────────────┘   │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 What Connects to the API Gateway (and What Doesn't)

```
                     ┌──────────────────────────────┐
                     │         API GATEWAY           │
                     │                               │
                     │  JWT validation               │
                     │  Rate limiting                │
                     │  Circuit breaking              │
                     │  DDoS protection               │
                     └──────────┬───────────────────┘
                                │
            ┌───────────────────┼───────────────────┐
            │                   │                   │
    ┌───────▼───────┐   ┌──────▼───────┐    ┌──────▼──────────┐
    │ Trading Svc   │   │ Main API     │    │ Marketing Sites │
    │ /trading/*    │   │ /*           │    │ (static)        │
    └───────────────┘   └──────────────┘    └─────────────────┘

GOES THROUGH THE API GATEWAY:
  ✓ All client REST requests (orders, auth, KYC, referrals, etc.)
  ✓ Marketing site traffic

DOES NOT GO THROUGH THE API GATEWAY:
  ✗ Centrifugo WebSocket connections (separate domain: realtime.inplay.com,
    own Cloud Load Balancer, JWT validated by Centrifugo itself)
  ✗ FIX Gateway ↔ tZERO (direct FIX 4.2 TCP, co-located)
  ✗ FIX Gateway ↔ Redis (internal GCP networking)
  ✗ Main API → tZERO REST API (server-to-server, no gateway needed)
  ✗ Main API → Persona (server-to-server)
  ✗ Main API → Sport Radar (server-to-server)
  ✗ Cloud Run Jobs (triggered by Cloud Scheduler, no external traffic)
  ✗ Service-to-service calls within GCP (internal networking)
```

### 2.3 Deployment Diagram -- What Runs Where

```
┌─────────────────────────────────────────────────────────────┐
│                    CLOUD RUN SERVICES                        │
│            (auto-scaling, stateless, team's expertise)       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  TRADING SERVICE                                     │    │
│  │  Separate deployment, own scaling, own resources     │    │
│  │  min-instances=20 (always warm, no cold starts)      │    │
│  │                                                      │    │
│  │  WHY SEPARATE: Latency-critical order execution      │    │
│  │  must not compete with KYC processing, leaderboard   │    │
│  │  queries, or ad serving for CPU/memory.              │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  MAIN API                                            │    │
│  │  Separate deployment, standard scaling               │    │
│  │  min-instances=10                                    │    │
│  │                                                      │    │
│  │  WHY MONOLITH (for now): Auth, KYC, referrals,       │    │
│  │  news, ads, notifications, teams -- none are          │    │
│  │  latency-critical. Splitting would add complexity    │    │
│  │  without benefit at launch. Split later when seams   │    │
│  │  emerge under real traffic patterns.                 │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  CENTRIFUGO                                          │    │
│  │  Separate deployment, session affinity enabled       │    │
│  │                                                      │    │
│  │  WHY CLOUD RUN (not VM): Auto-scales with demand.    │    │
│  │  Client SDK handles reconnection transparently if    │    │
│  │  instances recycle. Move to Managed Instance Group   │    │
│  │  if load testing shows excessive disconnects.        │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  MARKETING SITES (InPlay Global + Challenge Website) │    │
│  │  Scales to zero when idle                            │    │
│  │                                                      │    │
│  │  WHY SEPARATE: Different scaling profile (bursty,    │    │
│  │  low traffic). SEO requirements differ from app.     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                    CLOUD RUN JOBS                            │
│            (scheduled, batch processing)                     │
│                                                             │
│  ┌─────────────────────┐  ┌──────────────────────────────┐  │
│  │  Leaderboard Recalc │  │  End-of-Day Settlement       │  │
│  │  Every 5-15 seconds │  │  Daily after market close    │  │
│  │  via Cloud Scheduler│  │                              │  │
│  │                     │  │  • Expire Day orders         │  │
│  │  • Read positions + │  │  • Snapshot final P&L        │  │
│  │    current prices   │  │  • Calculate daily prizes    │  │
│  │  • Calc P&L ranks   │  │  • Process referral credits  │  │
│  │  • Calc risk-adj    │  │                              │  │
│  │  • Calc comeback    │  │                              │  │
│  │  • Write to Redis   │  │                              │  │
│  │    sorted sets      │  │                              │  │
│  └─────────────────────┘  └──────────────────────────────┘  │
│                                                             │
│  ┌─────────────────────┐                                    │
│  │  Referral Processor │                                    │
│  │  Triggered on KYC   │                                    │
│  │  completion events  │                                    │
│  │                     │                                    │
│  │  • Credit referrer  │                                    │
│  │    1,000 InPlay $   │                                    │
│  │  • Credit referee   │                                    │
│  │    500 InPlay $     │                                    │
│  │  • Apply multiplier │                                    │
│  │    if active        │                                    │
│  └─────────────────────┘                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    COMPUTE ENGINE VMs                        │
│          (persistent connections, co-located with tZERO)    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  FIX GATEWAY PRIMARY                                 │    │
│  │  Single VM, ~e2-standard-4 (~$100/month)             │    │
│  │                                                      │    │
│  │  WHY VM (not Cloud Run): FIX 4.2 requires persistent │    │
│  │  TCP sessions with heartbeats, sequence numbers, and │    │
│  │  session state. Cloud Run recycles containers,       │    │
│  │  killing these sessions. A dropped FIX session means │    │
│  │  lost orders and full state replay on reconnect.     │    │
│  │                                                      │    │
│  │  WHY CO-LOCATED: <1ms latency target to tZERO.       │    │
│  │  Network hops across regions would add 10-30ms.      │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  FIX GATEWAY STANDBY                                 │    │
│  │  Same spec, monitors primary, takes over on failure  │    │
│  │                                                      │    │
│  │  WHY STANDBY: If primary dies during a live NFL      │    │
│  │  game, 1M users lose all market data and can't trade.│    │
│  │  5-10 second failover is acceptable. No failover     │    │
│  │  is not.                                             │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    GCP MANAGED SERVICES                      │
│               (zero ops, fully managed by Google)            │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────────────────┐     │
│  │  Cloud SQL        │  │  Memorystore (Redis)         │     │
│  │  (PostgreSQL)     │  │                              │     │
│  │                   │  │  WHY REDIS (not Kafka):       │     │
│  │  WHY POSTGRES:    │  │  Team knows Redis. Pub/Sub   │     │
│  │  Battle-tested,   │  │  sufficient for launch.      │     │
│  │  ACID for wallet  │  │  Last-value cache via        │     │
│  │  transactions,    │  │  Centrifugo, not Redis.      │     │
│  │  team knows it.   │  │  Kafka upgrade path exists   │     │
│  │                   │  │  if Redis Pub/Sub becomes    │     │
│  │                   │  │  a bottleneck.               │     │
│  └──────────────────┘  └──────────────────────────────┘     │
│                                                             │
│  ┌──────────────────┐  ┌──────────────────────────────┐     │
│  │  Cloud Load       │  │  Cloud Scheduler             │     │
│  │  Balancer +       │  │                              │     │
│  │  Cloud Armor      │  │  Triggers Cloud Run Jobs:    │     │
│  │                   │  │  • Leaderboard every 5-15s   │     │
│  │  + API Gateway    │  │  • Settlement end of day     │     │
│  │  (TBC -- confirm  │  │                              │     │
│  │  with Brett)      │  │                              │     │
│  └──────────────────┘  └──────────────────────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.4 Service Interaction Map -- Who Talks to Who

```
┌────────────┐                                        ┌────────────┐
│            │───── WebSocket ────────────────────────►│            │
│  CLIENT    │                                        │ CENTRIFUGO │
│  (Expo)    │◄──── price updates, fills, events ─────│            │
│            │                                        └─────┬──────┘
│            │                                              │
│            │───── REST (orders) ────►┌─────────────┐      │ subscribes
│            │◄──── order ack ────────│  TRADING     │      │
│            │                        │  SERVICE     │      │
└────────────┘                        └──────┬───────┘      │
      │                                      │              │
      │                               publishes orders      │
      │ REST (auth,                          │              │
      │ KYC, referrals,                      ▼              ▼
      │ news, teams,               ┌─────────────────────────────┐
      │ leaderboards)              │          REDIS               │
      │                            │                             │
      ▼                            │  pub/sub channels           │
┌────────────┐                     │  order queue                │
│            │──── read/write ────►│  leaderboard sorted sets    │
│  MAIN API  │◄─── cache hits ────│  wallet cache               │
│            │                     │  session cache              │
│            │                     │  FIX sequence numbers       │
└──────┬─────┘                     └──────────────┬──────────────┘
       │                                          │
       │ REST calls                        reads queue,
       │ (server-to-server)                publishes events
       │                                          │
       ├──────► Persona (KYC)                     ▼
       ├──────► Sport Radar (data/news)  ┌─────────────────┐
       ├──────► tZERO REST API           │  FIX GATEWAY    │
       ├──────► FCM/APNs (push)          │                 │
       │                                 │  3 FIX sessions │
       │ read/write                      └────────┬────────┘
       ▼                                          │
┌────────────┐                              FIX 4.2 TCP
│ POSTGRESQL │                                    │
│            │                                    ▼
│ Users,     │                           ┌─────────────────┐
│ orders,    │                           │     tZERO       │
│ positions, │                           │    EXCHANGE     │
│ wallets,   │                           └─────────────────┘
│ referrals  │
└────────────┘
```

### 2.5 Internal Architecture per Service

**Trading Service:**
```
┌──────────────────────────────────────────────────────────┐
│  TRADING SERVICE (FastAPI, Cloud Run)                     │
│                                                          │
│  Incoming request: POST /trading/orders                   │
│         │                                                │
│         ▼                                                │
│  ┌──────────────┐                                        │
│  │ Auth          │  Validate JWT (passed from gateway)    │
│  │ Middleware    │  Extract userId                        │
│  └──────┬───────┘                                        │
│         ▼                                                │
│  ┌──────────────┐                                        │
│  │ Order         │  Validate: symbol exists, side valid,  │
│  │ Validator    │  qty > 0, price > 0, ClOrdID format    │
│  │              │  (no leading zeroes, max 20 chars)      │
│  └──────┬───────┘                                        │
│         ▼                                                │
│  ┌──────────────┐                                        │
│  │ Wallet       │  Read balance from Redis cache          │
│  │ Check        │  Verify sufficient funds                │
│  │              │  Check 100K cap not exceeded            │
│  └──────┬───────┘                                        │
│         ▼                                                │
│  ┌──────────────┐                                        │
│  │ Order        │  Publish to Redis order queue           │
│  │ Publisher    │  FIX Gateway consumes from this queue   │
│  └──────┬───────┘                                        │
│         ▼                                                │
│  ┌──────────────┐                                        │
│  │ Response     │  Return immediate ack to client         │
│  │              │  {status: "acknowledged", orderId: ...}  │
│  └──────────────┘                                        │
│                                                          │
│  Background listeners:                                    │
│  ┌──────────────┐                                        │
│  │ Fill         │  Subscribes to order.{userId}.*         │
│  │ Processor    │  On fill: update PostgreSQL (positions,  │
│  │              │  wallet balance, P&L)                    │
│  └──────────────┘                                        │
└──────────────────────────────────────────────────────────┘
```

**FIX Gateway:**
```
┌──────────────────────────────────────────────────────────┐
│  FIX GATEWAY (Python/QuickFIX, Compute Engine VM)        │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │  SESSION MANAGER                                  │    │
│  │  Manages logon, heartbeats, sequence numbers      │    │
│  │  Stores seq nums in Redis for failover            │    │
│  │  Handles disconnect/reconnect per tZERO spec DFAs    │    │
│  └──────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────┐ ┌────────────────┐ ┌──────────────┐  │
│  │ IOI ADAPTER    │ │ MD ADAPTER     │ │ OE ADAPTER   │  │
│  │                │ │                │ │              │  │
│  │ FIX session    │ │ FIX session    │ │ FIX session  │  │
│  │ to tZERO       │ │ to tZERO       │ │ to tZERO     │  │
│  │                │ │                │ │              │  │
│  │ Receives:      │ │ Receives:      │ │ Sends:       │  │
│  │ • IOI N/C/R    │ │ • Snapshots(W) │ │ • NewOrder(D)│  │
│  │ • Snapshots(W) │ │ • Incr Ref (X) │ │ • Cancel (F) │  │
│  │                │ │ • Sec Status(f)│ │ • Replace (G)│  │
│  │ Publishes to:  │ │ • Ses Status(h)│ │              │  │
│  │ market.book.*  │ │                │ │ Receives:    │  │
│  │ market.        │ │ Publishes to:  │ │ • ExecRpt (8)│  │
│  │  snapshot.*    │ │ market.quote.* │ │ • CxlRej (9) │  │
│  │                │ │ market.trade.* │ │              │  │
│  │                │ │ market.status.*│ │ Publishes to:│  │
│  │                │ │ market.session │ │ order.*.*    │  │
│  │                │ │                │ │ position.*   │  │
│  └────────────────┘ └────────────────┘ └──────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │  MESSAGE ENVELOPE WRAPPER                         │    │
│  │  Wraps every outgoing message with:               │    │
│  │  UUID, topic, source, seqNum, timestamps,         │    │
│  │  idempotencyKey, schema version                   │    │
│  └──────────────────────────────────────────────────┘    │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │  DEDUPLICATION                                    │    │
│  │  MsgSeqNum tracking per session                   │    │
│  │  PossDupFlag / PossResend handling                │    │
│  │  ExecID / IOIid dedup per tZERO spec Section 7       │    │
│  └──────────────────────────────────────────────────┘    │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │  ORDER QUEUE CONSUMER                             │    │
│  │  Reads validated orders from Redis queue           │    │
│  │  Converts to FIX NewOrderSingle                   │    │
│  │  Sends via OE Adapter                             │    │
│  └──────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

---

## 3. Technology Decisions -- What We Chose and Why

### 3.1 Decisions With Alternatives Considered

**Frontend: React Native (Expo)**

| Option | Considered | Rejected Because |
|--------|-----------|-----------------|
| React Native (Expo) | **Chosen** | -- |
| React Native + Next.js (separate web app) | Yes | Two codebases to maintain, divergent UIs, double the frontend effort |
| Flutter | Yes | Weaker web support, harder to hire, team doesn't know Dart |
| Native iOS + Native Android + Web | Yes | 3x the development effort, 3 codebases, team doesn't write Swift/Kotlin |
| Progressive Web App only | Yes | Limited push notification support on iOS, no app store presence, reduced performance for real-time charts |

**Backend: Python / FastAPI**

| Option | Considered | Rejected Because |
|--------|-----------|-----------------|
| Python / FastAPI | **Chosen** | -- |
| Node.js / TypeScript | Yes | Team is stronger in Python. Would introduce a second backend language alongside Python (needed for QuickFIX). |
| Go | Yes | Nobody on the team writes Go. High performance but wrong team fit. |
| Java / Spring Boot | Yes | Heavier framework, team doesn't write Java. QuickFIX/J exists but adds Java to the stack. |

**Real-Time Delivery: Centrifugo**

| Option | Considered | Rejected Because |
|--------|-----------|-----------------|
| Centrifugo | **Chosen** | -- |
| Custom WebSocket servers (FastAPI) | Yes | Python can't handle 1M concurrent WebSocket connections. Would need to build channel management, reconnection, last-value cache, scaling, message ordering from scratch. Weeks of engineering for solved problems. |
| Ably (managed) | Yes | Potentially $50K+/month at 1M concurrent connections. Adds third-party dependency on the critical real-time path. |
| Pusher (managed) | Yes | Same cost concerns as Ably. Rate limits may not suit high-frequency market data. |
| Socket.IO with Redis adapter | Yes | Python Socket.IO server has same scaling limitations as raw WebSockets. |
| AWS AppSync | Yes | Team is on GCP, not AWS. Would introduce cross-cloud dependency. |

**Message Bus: Redis Pub/Sub**

| Option | Considered | Rejected Because |
|--------|-----------|-----------------|
| Redis Pub/Sub (Memorystore) | **Chosen** | -- |
| Apache Kafka | Yes | Team doesn't know Kafka. Operational overhead (ZooKeeper/KRaft, topic management, consumer groups). Overkill for launch. Clear upgrade path exists if Redis becomes a bottleneck. |
| Google Cloud Pub/Sub | Yes | Higher latency (~10-50ms) than Redis (~1ms). Not designed for the message-per-second volume of real-time market data fan-out. Better suited for async event processing. |
| RabbitMQ | Yes | Additional infrastructure to manage. Redis already in the stack for caching and leaderboards. Don't introduce a second message system. |
| NATS | Yes | Team doesn't know NATS. Redis covers the use case without a new technology. |

**Compute Platform: Cloud Run (not GKE)**

| Option | Considered | Rejected Because |
|--------|-----------|-----------------|
| Cloud Run | **Chosen** | -- |
| GKE (Kubernetes) | Yes | Nobody on the team has Kubernetes experience. 4-6 week learning curve to deploy, months to operate confidently. Mid-August deadline makes this an unacceptable risk. Failure modes are unfamiliar and compound under pressure (node eviction, CoreDNS overload, resource limit misconfiguration). Revisit for year 2. |
| Compute Engine VMs (for everything) | Yes | No auto-scaling. Must pre-size VMs. More ops burden for stateless services that Cloud Run handles automatically. |
| Cloud Functions | Yes | Cold start latency too high for trading. No WebSocket support. Better suited for event-driven glue, not primary API serving. |

**FIX Gateway: Compute Engine VM (not Cloud Run)**

| Option | Considered | Rejected Because |
|--------|-----------|-----------------|
| Compute Engine VM | **Chosen** | -- |
| Cloud Run | Yes | FIX 4.2 requires persistent TCP sessions with heartbeats, sequence numbers, and session state. Cloud Run recycles containers during scale-down and deployments, killing FIX sessions. A dropped session means: orders in flight could be lost, full state replay required on reconnect (IOI/MD), sequence number gaps. Unacceptable for a trading system. |

**API Gateway: Yes (not skip)**

| Option | Considered | Rejected Because |
|--------|-----------|-----------------|
| API Gateway (managed) | **Chosen** | -- |
| No gateway (direct to services) | Yes | At 1M concurrent users: no per-user rate limiting means a single bad actor or bot can degrade trading for everyone. No JWT offloading means every service validates tokens independently. No circuit breaking means a downed Trading Service cascades into the Main API. No DDoS protection on the application layer. These are requirements at this scale, not optimisations. |
| Kong (self-hosted) | Considered | Additional infrastructure to manage. Team has GCP managed service experience. Confirm Brett's preference before final decision. |

**Database: PostgreSQL (not NoSQL)**

| Option | Considered | Rejected Because |
|--------|-----------|-----------------|
| PostgreSQL (Cloud SQL) | **Chosen** | -- |
| MongoDB | Yes | Wallet transactions require ACID guarantees. Eventual consistency is unacceptable for financial balances. PostgreSQL provides this out of the box. |
| Firestore | Yes | Good for simple document storage but lacks the relational queries needed for leaderboard calculations, referral chain tracking, and complex P&L reporting. |
| CockroachDB / Spanner | Yes | Distributed SQL is unnecessary at launch. Single-region Cloud SQL with read replicas handles the load. Adds operational complexity and cost without clear benefit for year 1. |

---

## 4. Tech Stack (Summary)

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Mobile + Web App** | React Native (Expo) | Single codebase for iOS, Android, and web. Team knows React. Expo has mature WebSocket and web support. |
| **Marketing Sites** | Static site / lightweight framework | Doesn't need app infrastructure. SEO matters here. |
| **API** | Python / FastAPI | Team's primary language. Async-first, native WebSocket support, Pydantic validation. |
| **Trading Gateway** | Python / QuickFIX | Maintains 3 FIX 4.2 sessions to tZERO. Python keeps the entire backend in one language. |
| **Real-Time Delivery** | Centrifugo | Purpose-built WebSocket fan-out server. Handles 1M+ connections, last-value cache, channel-based pub/sub. Deployed as a Docker container, configured via YAML, interacted with via Python and JavaScript SDKs. No Go knowledge required. |
| **Message Bus** | Redis Pub/Sub (Memorystore) | Internal event distribution between FIX Gateway, services, and Centrifugo. Team knows Redis. Upgrade path to Kafka if needed. |
| **Database** | PostgreSQL (Cloud SQL) | Users, orders, positions, wallets, referrals, leaderboard snapshots, ad inventory, KYC records. |
| **Cache / Leaderboards** | Redis (Memorystore) | Sorted sets for leaderboard rankings (3 verticals x 4 timeframes). Session cache, wallet balance cache, last-value cache for market data. |
| **Cloud Platform** | Google Cloud Platform | Team's existing platform. |

---

## 5. Service Architecture

Two FastAPI deployments on Cloud Run, separated by latency requirements.

### 5.1 Trading Service (Cloud Run)

The hot path for order execution. Separated from the Main API so nothing else competes for its resources.

**Responsibilities:**
- Order validation (auth, limits, format)
- Wallet balance checks (reads from Redis cache)
- Publishes validated orders to Redis queue for FIX Gateway consumption
- Returns immediate acknowledgment to user ("order received")
- Wallet management (trading wallet 100K cap, referral wallet reload logic below 25K trigger)
- Position management and P&L calculation

**Scaling:** Cloud Run auto-scaling, min-instances set high to avoid cold starts on the critical path.

### 5.2 Main API (Cloud Run)

Everything that isn't latency-critical trading.

**Responsibilities:**
- Authentication and JWT issuance
- User profiles and account management
- KYC integration (Persona)
- Referral system (code generation, dual-sided rewards, social engagement credits, multiplier days)
- News and content (Sport Radar editorial feed, block trade alerts)
- Competition and leaderboards (recalculated every 5-15 seconds via Cloud Run Jobs)
- Ad service (moment-based triggers, geo/demographic targeting, sponsor inventory)
- Notification service (push via FCM/APNs, game reminders, trade alerts)
- Team pages, historical stats, favourites
- Calls tZERO REST API directly for non-real-time operations (account management, historical data, symbol reference data)

**Scaling:** Cloud Run auto-scaling with standard min-instances.

### 5.3 FIX Gateway (Compute Engine VM)

Maintains persistent FIX 4.2 sessions to tZERO. Must be co-located or on a low-latency link to tZERO's matching engine (<1ms target).

**3 FIX Sessions:**

| Session | Protocol | Purpose |
|---------|----------|---------|
| IOI v1.2 | FIX 4.2 | Order book indications of interest. Builds the full book picture. Single client connection only. |
| FIX Market Data v8 | FIX 4.2 | Quotes (BBO), trades, OHLC, security status, session status. ResetSeqNumFlag=Y required on every logon -- no session recovery. |
| Order Entry v2.2 | FIX 4.2 | Order submission, execution reports, cancels, replaces, position/P&L data. tZERO is the acceptor. |

**Adapters:**
- IOI Adapter -- parses IOI messages, publishes to `market.book.{symbol}` and `market.snapshot.{symbol}`
- MD Adapter -- parses incremental refreshes and snapshots, publishes to `market.quote.{symbol}`, `market.trade.{symbol}`, `market.status.{symbol}`, `market.session`
- OE Adapter -- sends orders to tZERO, receives execution reports, publishes to `order.{userId}.{orderId}` and `position.{userId}`

**Message Bus Envelope:**
Every message published to Redis follows the envelope schema from the tZERO spec: UUID messageId, topic, source feed, source sequence number, timestamps (ours and tZERO's), idempotency key, schema version.

**High Availability:**
- Active/standby VM configuration
- FIX session state (sequence numbers) stored in Redis
- Orders queued in Redis -- survive gateway restart
- Standby detects primary failure via health check, establishes new FIX sessions (~5-10 second failover)
- On IOI/MD reconnection: full state replay from tZERO (no incremental recovery supported)
- On Order Entry reconnection: standard FIX gap detection and resend

### 5.4 Centrifugo (Managed Instance Group)

Real-time delivery layer. Holds all WebSocket connections from clients. Subscribes to Redis channels and fans out to connected users.

**Why Managed Instance Group, not Cloud Run:** WebSocket connections are long-lived (users stay connected for hours during a game). Cloud Run recycles containers during scale-down, deployments, and maintenance -- each recycle drops every connection on that instance. At 1M-5M users, an instance holding 50K connections being recycled causes 50K simultaneous disconnects. With a Managed Instance Group, VMs stay alive until explicitly removed, and scale-down can be scheduled for off-hours when users have naturally disconnected.

**Scaling strategy:**
- Min 3 VMs always running (~600K connection capacity)
- Scale up before game days via Cloud Scheduler (e.g., 25 VMs for NFL Sunday = 5M capacity)
- Scale down only during off-hours (never during live games)
- Google auto-heals failed VMs (restarts, does not recycle healthy ones)

**Responsibilities:**
- 1M-5M concurrent WebSocket connections
- Channel-based subscriptions (users subscribe to symbols they're watching)
- Last-value cache -- new subscribers and reconnecting users get current state immediately
- Conflation -- merge rapid updates to max 10/sec per symbol to manage bandwidth
- JWT authentication (validates tokens issued by Main API)
- Auto-reconnection handling (critical for mobile users with unstable connections)

**Channel Mapping (from tZERO spec topic design):**

| Centrifugo Channel | Data | Source |
|-------------------|------|--------|
| `market.quote.{symbol}` | Best bid/offer | FIX v8 incremental |
| `market.book.{symbol}` | Order book depth | IOI v1.2 + FIX v8 |
| `market.trade.{symbol}` | Executed trades | FIX v8 incremental |
| `market.snapshot.{symbol}` | OHLC, volume, prev close | IOI v1.2 snapshot |
| `market.status.{symbol}` | Halt/resume, SSR | FIX v8 security status |
| `market.session` | Trading session phase | FIX v8 session status |
| `order.{userId}.{orderId}` | Order status, fills | OE execution reports |
| `position.{userId}` | Position, P&L | OE execution reports |
| `leaderboard.{vertical}.{timeframe}` | Rankings | Competition service |

---

## 6. Infrastructure (GCP)

### 6.1 Deployment Model

```
Cloud Run (stateless, auto-scaling, team's expertise)
├── Trading Service      (min-instances pre-warmed before games)
├── Main API             (min-instances=10)
├── Notification Service (bursty workload)
├── Marketing Sites      (scales to zero)
└── Cloud Run Jobs:
    ├── Leaderboard recalculation (every 5-15 seconds)
    ├── End-of-day settlement
    └── Referral reward processing

Managed Instance Group (long-lived WebSocket connections)
└── Centrifugo VMs       (schedule-controlled scaling, min 3 VMs)

Compute Engine VMs (persistent FIX sessions)
├── FIX Gateway Primary   (co-located with tZERO)
└── FIX Gateway Standby   (co-located with tZERO)

Managed Services
├── Cloud SQL         (PostgreSQL -- users, orders, positions, wallets, referrals)
├── Memorystore       (Redis -- pub/sub, cache, leaderboard sorted sets)
├── Cloud Load Balancer + Cloud Armor (routing, SSL, DDoS)
├── Cloud CDN         (serves React Native web app bundle to browsers)
├── API Gateway       (JWT validation, rate limiting, path-based routing)
└── Cloud Scheduler   (triggers Cloud Run Jobs + game-day scaling)
```

### 6.2 Routing

```
realtime.inplay.com      → Centrifugo (WebSocket connections)
api.inplay.com/trading/* → Trading Service (order execution)
api.inplay.com/*         → Main API (everything else)
```

### 6.3 API Gateway

Managed GCP service (Cloud Load Balancer + Cloud Armor, or API gateway the team has experience with -- confirm with Brett).

**Responsibilities:**
- JWT validation at the edge (reject bad tokens before hitting services)
- Per-user rate limiting (critical for trading -- e.g., 10 orders/sec/user)
- DDoS protection via Cloud Armor
- Circuit breaking (if Trading Service goes down, fail fast instead of queuing)
- Path-based routing to Trading Service vs Main API
- SSL termination

---

## 7. Data Flows

### 7.1 Price Update (tZERO to User Screen)

Target: <100ms end-to-end, <56ms typical.

```
tZERO sends FIX message (e.g., trade at $25.60)
  → FIX Gateway parses + normalizes (<2ms)
  → Publishes to Redis channel market.trade.{symbol} (<2ms)
  → Centrifugo picks up from Redis (<5ms)
  → Delivers to all subscribed clients via WebSocket (<30ms)
  → Client renders new price (<16ms)
```

### 7.2 Order Placement (User to tZERO to User)

```
User taps "Buy 100 shares Cowboys @ $25"
  → REST POST to Trading Service via API Gateway
  → Trading Service validates (auth, wallet balance, order format)
  → Publishes to Redis order queue
  → Returns "order acknowledged" to user immediately
  → FIX Gateway reads from queue
  → Sends FIX NewOrderSingle to tZERO via OE session
  → tZERO matches → sends ExecutionReport back via FIX
  → FIX Gateway publishes fill to Redis (order.{userId}.{orderId})
  → Centrifugo delivers fill confirmation to user via WebSocket
  → Trading Service updates wallet and positions in PostgreSQL
```

### 7.3 User Reconnection

```
User's WiFi drops for 3 seconds
  → WebSocket to Centrifugo disconnects
  → FIX sessions to tZERO completely unaffected (server-side)
  → Market data and order events continue flowing into Redis
  → WiFi returns → client auto-reconnects to Centrifugo
  → Centrifugo delivers last-value-cached data immediately
  → User sees current prices within ~1 second, no loading spinner
  → Any fills during the gap were processed server-side, order state is correct
```

### 7.4 Non-Real-Time Operations

```
Historical data, account management, symbol reference
  → Main API (Cloud Run) calls tZERO REST API directly
  → Base URL: https://gateway-web-api.tzero.com/app
  → Auth: API key header + bearer token (1 hour TTL)
  → No FIX Gateway involvement
```

---

## 8. External Dependencies

| Dependency | Purpose | Integration Method | Status |
|-----------|---------|-------------------|--------|
| **tZERO** | Trading engine, price data, order book, execution | FIX 4.2 (3 sessions) + REST API | Partnered |
| **Sport Radar** | Real-time game data, historical stats, news feed | API (push feed TBC vs polling) | Licensed |
| **Persona** | KYC -- age 18+, identity, bot detection, US citizenship | REST API from Main API | Setup in progress |
| **FCM / APNs** | Push notifications (iOS + Android) | Cloud Run Notification Service | Standard |
| **Brokerage Partners** | Production trading referrals ($150/account) | Future -- not challenge scope | Future |

---

## 9. Key Architectural Decisions (Summary)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Single frontend codebase | React Native (Expo) for mobile + web | Avoid maintaining two frontends. Trading app benefits from app-like feel on web. |
| Backend language | Python throughout (FastAPI + QuickFIX) | Team's primary language. One language across entire backend reduces context switching. |
| Real-time delivery | Centrifugo (not custom WebSocket servers) | Handles 1M+ connections out of the box. Last-value cache, reconnection, channel management all built in. Deployed as infrastructure, not code. |
| Message bus | Redis Pub/Sub (not Kafka) | Team knows Redis. Sufficient for launch. Upgrade path to Kafka exists if needed. |
| Compute platform | Cloud Run (not GKE) | Team has no Kubernetes experience. Mid-August deadline. Cloud Run is the team's existing expertise. |
| Centrifugo hosting | Managed Instance Group (not Cloud Run) | WebSocket connections are long-lived (hours). Cloud Run recycles instances, dropping all connections on that instance. MIG keeps VMs alive, scales on a game-day schedule. |
| FIX Gateway hosting | Compute Engine VM (not Cloud Run) | FIX requires persistent TCP sessions. Cloud Run would kill them on scale-down. |
| Trading Service separation | Own Cloud Run deployment | Latency-critical path must not compete for resources with KYC, referrals, leaderboards, etc. |
| API Gateway | Yes | At 1M concurrent users: per-user rate limiting, JWT offloading, DDoS protection, circuit breaking are requirements, not nice-to-haves. |
| Leaderboards | Near-real-time (5-15 second recalculation) | True real-time recalc for 1M users on every price tick is prohibitively expensive. Users won't notice 5-15s staleness during a game. |
| No Kubernetes | Deliberate | Learning curve is 4-6 weeks to deploy, months to operate confidently. Unacceptable risk under mid-August deadline with no prior experience. Revisit for year 2. |

---

## 10. Latency Budget (from tZERO Spec)

| Hop | Component | Target |
|-----|-----------|--------|
| 1 | tZERO → FIX Gateway | <1ms (co-located) |
| 2 | FIX parse + normalize | <2ms |
| 3 | Gateway → Redis | <2ms |
| 4 | Redis → Centrifugo → Client | <50ms |
| 5 | Client render | <16ms |
| **Total** | | **<56ms typical, <100ms p99** |

---

## 11. Throughput Estimates (from tZERO Spec)

| Metric | Estimate |
|--------|----------|
| Symbols watched per user (avg) | 10 |
| Unique symbols | ~500 |
| Updates per symbol per second (peak) | 50 |
| Upstream messages/sec from tZERO | 25,000 |
| Fan-out messages/sec to all users (before conflation) | 500M |
| With conflation (10/sec/symbol) | Significantly reduced |

---

## 12. Frontend Architecture

### 12.1 How React Native (Expo) Differs from Next.js

React Native (Expo) is not a server-rendered framework. There is no frontend server to deploy or scale. The app runs entirely on the user's device.

**Next.js (server-rendered):**
```
User's browser ──request──► Next.js SERVER ──► renders HTML ──► sends back to browser
                                  │
                            This server runs YOUR code:
                            server components, SSR, API routes.
                            More users = more server load.
                            You must scale this server.
```

**React Native / Expo (client-side):**
```
BUILD TIME (once, before deployment):
  Your code ──build──► static bundle (HTML + JS + CSS files)
                       Just files. No server needed.

RUNTIME (every user):
  Mobile: downloaded from App Store/Google Play, runs on their phone
  Web: browser downloads the JS bundle from CDN, runs it locally

  Everything runs on the USER'S DEVICE.
  Their phone/browser does all the rendering.
  The only server calls are to FastAPI (data) and Centrifugo (real-time).
```

### 12.2 How the App Reaches Users

```
iOS:     Published to App Store → user downloads → runs on iPhone
Android: Published to Google Play → user downloads → runs on Android
Web:     Static files (JS/CSS/HTML) served from Cloud CDN
         → cached at 100+ edge locations worldwide
         → user's browser downloads once (~3-5MB), cached after first load
         → app runs entirely in their browser tab
```

### 12.3 CDN (Content Delivery Network)

A CDN is a network of servers spread around the world that stores copies of static files close to users.

```
Without CDN:
  App bundle on ONE server in Iowa.
  User in New York:  50ms   User in London: 150ms   User in Tokyo: 250ms

With Cloud CDN:
  App bundle copied to 100+ edge servers worldwide.
  User in New York:  5ms    User in London: 5ms     User in Tokyo: 5ms
```

For InPlay: the web app bundle is uploaded to Cloud CDN once. The CDN handles millions of downloads trivially because it's just serving static files. Cost: ~$50-100/month.

### 12.4 Frontend Framework Landscape

**Web frameworks:**

| Framework | Based On | Rendering | Key Trait |
|-----------|----------|-----------|-----------|
| Next.js | React | Server + client | Most popular server-rendered React framework |
| Nuxt | Vue | Server + client | Next.js equivalent for Vue |
| SvelteKit | Svelte | Server + client | Next.js equivalent for Svelte |
| Remix | React | Server + client | Alternative to Next.js, different data loading philosophy |
| React (Vite) | React | Client only | No server, browser renders everything |
| Vue (Vite) | Vue | Client only | Same but Vue |
| Angular | Angular | Client only (SSR optional) | Google's framework, enterprise-heavy, steep learning curve |

**The underlying UI libraries:**

| Library | Created By | Ecosystem | Learning Curve | Hiring Pool |
|---------|-----------|-----------|----------------|-------------|
| React | Meta/Facebook | Massive (largest) | Moderate | Huge |
| Vue | Evan You | Large | Easiest | Good |
| Svelte | Rich Harris | Growing | Easy | Smallest |
| Angular | Google | Large | Steepest | Good (enterprise) |

**Cross-platform mobile frameworks:**

| Framework | Language | Performance | Web Support | InPlay Fit |
|-----------|----------|-------------|-------------|------------|
| React Native (Expo) | TypeScript | Very good (native bridge) | Good via Expo | **Chosen** -- team knows React/TS, single codebase, large ecosystem |
| Flutter | Dart | Excellent (compiled) | Works but feels app-like | Rejected -- team doesn't know Dart, weaker web story, harder to hire |
| Ionic | TypeScript | Weakest (WebView) | Great (it's already web) | Rejected -- WebView performance too slow for real-time trading charts |
| Native (Swift + Kotlin) | Swift / Kotlin | Best possible | N/A (separate web needed) | Rejected -- 3x development effort, 3 codebases |

### 12.5 Frontend Performance Considerations

The React Native app runs on user devices, so there is no server-side frontend to scale. However, the app must handle high-frequency data efficiently:

| Concern | Problem | Solution |
|---------|---------|----------|
| Rapid price updates | 10 updates/sec/symbol x 10 symbols = 100 re-renders/sec. Kills battery and frame rate. | Client-side throttling -- batch UI updates to 4-5/sec. Centrifugo delivers at 10/sec, app renders at a comfortable rate. |
| Reconnection | Mobile users lose signal constantly (walking, subway, switching WiFi/cellular). | Centrifugo JS SDK handles automatically -- auto-reconnects, resubscribes, recovers missed messages via last-value cache. |
| Subscription management | Subscribing to full order book depth for all watchlist symbols wastes bandwidth. | Full depth only for the actively viewed symbol. Watchlist gets top-of-book only. Unsubscribe on navigate away. (Matches tZERO spec lazy subscription pattern.) |
| Background/lock screen | User locks phone or switches app during a game. | Drop WebSocket on background, reconnect on foreground. Last-value cache means instant catch-up. |

### 12.6 Deployment Targets

React Native (Expo) deploys to three targets. Unlike Next.js where you deploy one server, here you manage three distribution channels.

**iOS (App Store):**
- Build: `eas build --platform ios` (Expo's cloud build service, ~10-15 min)
- Submit: `eas submit --platform ios`
- Apple reviews: 1-7 days on first submission, 1-2 days for updates. Can reject.
- Requirements: Apple Developer Account ($99/year), signing certificates, App Store listing (screenshots, description), privacy policy URL, age rating
- Users update via App Store (auto-update or manual -- some users stay on old versions for weeks)

**Android (Google Play):**
- Build: `eas build --platform android`
- Submit: `eas submit --platform android`
- Google reviews: usually hours to 1-2 days (much faster than Apple)
- Requirements: Google Play Developer Account ($25 one-time), signing key (Expo can manage), store listing
- Users update via Play Store

**Web (Cloud CDN):**
- Build: `expo export:web` outputs static HTML/JS/CSS files
- Upload to Cloud CDN -- no server, no review process
- Users get new version on next page load
- Deploy as often as you want

**Over-The-Air (OTA) Updates -- Expo's escape hatch:**

For JavaScript-only changes (UI fixes, logic changes, new screens, style changes), Expo can push updates directly to users' devices without going through App Store review:

```
eas update --branch production --message "fix price display bug"
```

- Live in minutes, no review process
- Works for ~90% of typical updates
- Does NOT work for native changes (new permissions, new native libraries, app icon)

| Change Type | Deployment Method | Time to Users |
|-------------|------------------|---------------|
| Bug fix in trading UI | OTA update | Minutes |
| New leaderboard screen | OTA update | Minutes |
| Style/layout changes | OTA update | Minutes |
| Add push notification permission | Full App Store build | 1-7 days |
| New native charting library | Full App Store build | 1-7 days |
| App icon change | Full App Store build | 1-7 days |

**Launch timeline consideration:** First App Store submission should happen 2-3 weeks before launch. Apple can reject for surprising reasons, and you need time to fix and resubmit. Budget for this.

---

## 13. Scaling Strategy

### 13.1 What Scales and How

```
DOESN'T NEED TO SCALE (runs on user devices / CDN):
  React Native app        (runs on phones/browsers)
  Web app bundle           (static files on Cloud CDN)

SCALES AUTOMATICALLY (Cloud Run):
  Trading Service          (pre-warm min-instances before games)
  Main API                 (standard auto-scaling)
  Cloud Run Jobs           (triggered on schedule)

SCALES VIA MANAGED INSTANCE GROUP (schedule-controlled):
  Centrifugo               (ramp up before kickoff, scale down post-game)

DOESN'T SCALE (and doesn't need to):
  FIX Gateway              (constant workload regardless of user count)

SCALES VIA GCP TIER CHANGES (if needed):
  Redis Memorystore        (resize tier if connection/memory limits hit)
  Cloud SQL PostgreSQL     (add read replicas if query load grows)
```

### 13.2 Why the FIX Gateway Doesn't Scale With Users

Market data from tZERO is per-symbol, not per-user: 500 symbols x 50 updates/sec = 25,000 msgs/sec regardless of whether 10K or 5M users are watching. The fan-out to users is Centrifugo's job.

Orders scale with users, but the architecture absorbs spikes at the Cloud Run layer:

```
5M users tap Buy simultaneously
  → Trading Service (Cloud Run) auto-scales to absorb the spike
  → Redis queue holds all validated orders
  → FIX Gateway drains the queue at tZERO's acceptance rate
  → tZERO's matching engine is the throughput bottleneck, not our infrastructure
```

The FIX Gateway is a message pump, not a scaling bottleneck. A single VM handles tens of thousands of FIX messages/sec.

### 13.3 Trading Service Cold Start Mitigation

Cloud Run cold starts (500ms-2s) are avoided by pre-warming min-instances before games. Each Trading Service request is ~10ms (validate JWT, check Redis cache, publish to Redis queue, return ack). With Cloud Run's concurrency setting:

```
min-instances = 50, concurrency = 250 per instance
  → 50 x 250 = 12,500 concurrent requests capacity
  → Each request takes 10ms, so throughput = 1.25M orders/second
  → Well within peak spike estimates, no cold start triggered

Cloud Scheduler automates this:
  Before game:   set min-instances=50
  After game:    set min-instances=10
```

### 13.4 Game-Day Scaling Schedule

```
Pre-season (off-hours):
  Trading Service: min-instances=10
  Centrifugo MIG:  3 VMs (~600K connection capacity)

Thursday Night Football:
  Trading Service: min-instances=30
  Centrifugo MIG:  10 VMs (~2M connection capacity)

NFL Sunday (multiple games):
  Trading Service: min-instances=50
  Centrifugo MIG:  25 VMs (~5M connection capacity)

Post-game (users disconnecting naturally):
  DON'T scale down during active games
  Scale down after midnight when connections drop

Off-season:
  Trading Service: min-instances=5
  Centrifugo MIG:  3 VMs
```

---

## 14. Ad Serving Architecture

InPlay's revenue model is ~90% advertising. The ad serving architecture must support both standard ad delivery at launch and InPlay's unique moment-based ad model post-launch.

### 14.1 Standard Ad Serving (Launch)

At launch, use **Google Ad Manager (GAM)** for ad serving. This handles the standard infrastructure while Skye's team sells direct sponsorships.

**How it works:**
- Skye's team sells sponsorships directly to advertisers (Doritos, DoorDash, etc.)
- Sponsorships configured as GAM "line items" with targeting rules (e.g., "Doritos creative on all Cowboys game pages, users aged 25-35")
- GAM serves directly-sold ads first (InPlay keeps 100% of that revenue)
- Any unsold ad inventory backfilled by Google AdMob programmatic ads (Google takes ~40%)
- GAM handles impression tracking, click tracking, and reporting out of the box

**Ad formats in the app:**

| Format | Placement | Revenue |
|--------|-----------|---------|
| Banner (320x50) | Bottom of game pages, team pages | Low CPM ($0.50-2.00) but always visible |
| Native ad | In news feed, between content cards | Mid CPM ($5-15), blends with content |
| Interstitial | Between screen transitions (e.g., after closing a trade confirmation) | High CPM ($3-10) |
| Rewarded | "Watch ad for 500 InPlay dollars" -- user opts in | Highest CPM ($10-30), best engagement |

**Integration:**
```
React Native app
  → react-native-google-mobile-ads SDK
  → Ad placements defined in app layout
  → GAM serves ads based on line item targeting
  → Impressions/clicks tracked by GAM automatically
```

**What GAM can target at launch (using InPlay's first-party data):**
- Age range (from KYC -- verified, not guessed)
- Device platform (iOS/Android)
- Custom key-values passed to GAM (e.g., "game=cowboys-giants", "page=trading")

**What GAM cannot do:**
- Trigger ads based on live game events (touchdowns, interceptions)
- Geo-target within 3 miles in real-time
- Time-delay ads ("30 minutes after game ends")
- Tie ads to volatility moments

### 14.2 Custom Moment-Based Ad Serving (Post-Launch)

InPlay's unique ad model: sponsors own specific game moments, with real-time targeting. This is layered on top of GAM post-launch.

**How it works:**

```
Sport Radar: "Touchdown -- Cowboys, Q3, 7:42"
      │
      ▼
  Event Trigger Engine (Main API)
      │
      │  1. Match event against active campaigns
      │     "Which sponsors own Cowboys touchdown moments?"
      │     → Doritos: age 25-35
      │     → DoorDash: within 3 miles of stadium
      │
      │  2. Resolve target audience from pre-computed segments
      │     → Redis SET "campaign:doritos-cowboys-td" = [user1, user2, ...]
      │
      │  3. Publish ad payload to qualifying users
      │
      ▼
  Centrifugo → delivers ad to user's screen
               within ~100ms of the touchdown
```

**Components:**

| Component | What It Does | Where It Runs |
|-----------|-------------|---------------|
| Campaign Manager | Admin panel for configuring sponsor campaigns, moment ownership, targeting rules, creatives | Main API (Cloud Run) |
| Moment-to-Sponsor Mapping | Database linking game events to sponsors | PostgreSQL |
| Event Trigger Engine | Listens to Sport Radar game events, matches against active campaigns | Main API (Cloud Run) |
| Targeting Engine | Filters users by pre-computed segments (age, geo, teams followed) | Redis (pre-computed sets) |
| Ad Delivery | Pushes ad payload through Centrifugo to qualifying users | Centrifugo channel: `ad.{userId}` or `ad.game.{gameId}` |
| Impression Tracking | Records when ads were shown, clicked, engaged with | PostgreSQL + analytics pipeline |
| Reporting Dashboard | Advertisers/Skye see impressions, clicks, engagement by campaign | Main API (Cloud Run) |

**Targeting data sources (all first-party, KYC-verified):**

| Data | Source | Storage | Ad Use |
|------|--------|---------|--------|
| Age | KYC (Persona) -- verified | PostgreSQL | Demographic targeting |
| Location | Device GPS (requires app permission) | Redis (real-time), PostgreSQL (home location) | Geo-targeting within X miles. Redis GEORADIUS for radius queries. |
| Teams followed | User selects in app | PostgreSQL | Interest targeting ("show to Cowboys fans") |
| Trading behaviour | App activity | PostgreSQL | Engagement-based targeting ("active Sunday traders") |
| Session duration | App activity | Analytics | "Consumed minutes" metric for advertiser reporting |
| Device type | App metadata | PostgreSQL | Platform targeting |

**Pre-computed targeting for real-time delivery:**

When a campaign is created or updated, target user segments are pre-computed into Redis sets. When a game event triggers an ad, the system reads the pre-computed set rather than querying PostgreSQL for every user. This enables ad delivery within milliseconds of the triggering event.

```
Campaign created: "Doritos, Cowboys touchdowns, age 25-35"
  → Query PostgreSQL for matching users
  → Store result in Redis: SET campaign:doritos-cowboys-td = [user1, user2, ...]
  → Refresh periodically (new signups, profile changes)

Touchdown happens:
  → Look up matching campaigns (small table, fast)
  → For each campaign, read pre-computed Redis set
  → Publish ad to those users via Centrifugo
  → Total time: ~10ms
```

### 14.3 Ad Serving Strategy: Launch vs Post-Launch

| Capability | Launch (GAM) | Post-Launch (Custom) |
|-----------|-------------|---------------------|
| Sponsor ads on specific game pages | Yes (GAM line items) | Yes |
| Demographic targeting (age) | Yes (KYC data passed as key-values) | Yes |
| Moment-based triggers (touchdowns) | No | Yes |
| Geo-targeting (within X miles) | No (GAM geo is coarse) | Yes (device GPS + Redis GEORADIUS) |
| Time-delayed ads | No | Yes |
| Volatility moment sponsorship | No | Yes |
| Impression/click tracking | Yes (GAM built-in) | Custom (PostgreSQL + analytics) |
| Reporting dashboard | Yes (GAM built-in) | Custom build |
| Unsold inventory backfill | Yes (AdMob programmatic) | Yes (keep GAM for backfill) |
| Revenue on direct-sold | 100% to InPlay | 100% to InPlay |
| Revenue on backfill | ~60% to InPlay | ~60% to InPlay |

### 14.4 Privacy and Data Considerations

InPlay collects verified first-party data through KYC. This is significantly more valuable than cookie-based or device-ID-based targeting (both of which are being killed by Apple and browser vendors).

| Requirement | What It Means |
|------------|---------------|
| Privacy policy | Must disclose data collection and use for advertising. Required for App Store and legally. |
| Location permission | iOS/Android popup. User can decline -- no geo-targeting for that user. |
| CCPA (California) | Users can request data deletion and opt out of data "sale". Need a "Do Not Sell" option. |
| Terms of service | Must state data is used for ad targeting. Part of signup flow. |
| Age-gated data | Extra care with 18-20 year old data in some jurisdictions. Legal review needed. |

**InPlay's ad data advantage:** Most apps guess user demographics from browsing behaviour. InPlay KNOWS age, identity, and location from KYC verification. Combined with real engagement data (which teams they follow, when they trade, how long they're active), this is a premium ad product that competitors with cookie-based targeting cannot match.

---

## 15. Open Questions

| Question | Impact | Who Answers |
|----------|--------|-------------|
| Where is tZERO's matching engine physically? | Determines FIX Gateway location and network link to GCP | tZERO / Edwin |
| Does tZERO support multiple concurrent FIX sessions for OE? | Could enable parallel order processing during spikes | tZERO |
| tZERO REST API full endpoint list? | Determines what can bypass FIX Gateway | tZERO (API explorer) |
| Sport Radar delivery method -- push feed or polling API? | Affects architecture of Sports Data ingestion | Sport Radar |
| Which API gateway does Brett prefer / have experience with? | Shortcut the gateway selection decision | Brett |
| Centrifugo MIG VM sizing and connection limits per instance? | Determines VM machine type and min/max scaling targets | Load testing |
| tZERO order throughput limit? | Determines whether order queuing causes noticeable delay during game spikes | tZERO |
