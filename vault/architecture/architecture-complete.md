# InPlay Trading Challenge -- Complete Technical Architecture

> **Project:** [[index]]
> **Status:** Draft
> **Date:** 2026-05-12
> **Owner:** Novosapien
> **Sources:** Vision document, T0 integration spec, architecture workshop sessions, modules 2 & 3 session (2026-05-11)
>
> This document consolidates every architecture decision, service spec, infrastructure detail, data flow, and performance target into a single reference. For deep-dives on specific topics, see the linked sub-documents throughout.

---

## Table of Contents

1. [Overview](#1-overview)
2. [System Architecture](#2-system-architecture)
3. [Tech Stack](#3-tech-stack)
4. [Services](#4-services)
5. [Infrastructure](#5-infrastructure)
6. [Data Layer](#6-data-layer)
7. [Real-Time Layer](#7-real-time-layer)
8. [Data Flows](#8-data-flows)
9. [Frontend](#9-frontend)
10. [External Integrations](#10-external-integrations)
11. [Scaling Strategy](#11-scaling-strategy)
12. [Cost Optimisation](#12-cost-optimisation)
13. [Performance Targets](#13-performance-targets)
14. [Testing Strategy](#14-testing-strategy)
15. [Security](#15-security)
16. [Open Questions](#16-open-questions)

---

## 1. Overview

The InPlay Trading Challenge is a simulated sports equity trading platform targeting 1M-5M concurrent users at peak load. Users trade team stocks during live NFL and college football games using simulated currency (100K InPlay dollars per user), competing for real cash prizes ($5M-$25M season pool).

**This architecture covers the trading challenge only -- not the production trading platform.**

The system consists of:
- **6 Cloud Run services** (5 API services + 1 Leaderboard)
- **FIX Gateway** on Compute Engine (persistent FIX 4.2 sessions to tZERO)
- **Centrifugo** on a Managed Instance Group (1M-5M WebSocket connections)
- **NATS JetStream** as the message backbone
- **PostgreSQL** (Cloud SQL) as the source of truth
- **Redis** (Memorystore) for cache and leaderboard data structures
- **React Native (Expo)** frontend for iOS, Android, and web from a single codebase

Mid-August 2026 launch target. NFL regular season scope.

---

## 2. System Architecture

### High-Level Topology

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              USERS (Mobile + Web)                                    │
│                                                                                      │
│   React Native App (iOS/Android)              Challenge Website    Global Website     │
│   ├── REST API calls → api.inplay.com         www.inplay.com       global.inplay.com  │
│   └── WebSocket → realtime.inplay.com                                                │
└──────────┬──────────────────┬─────────────────────────┬──────────────────────────────┘
           │ HTTPS            │ WSS                     │ HTTPS
┌──────────▼──────────────────▼─────────────────────────▼──────────────────────────────┐
│                           EDGE / SECURITY LAYER                                       │
│                                                                                       │
│   Cloudflare CDN + WAF                    Cloudflare Spectrum                         │
│   ├── DDoS protection (L7)                ├── DDoS protection (L3/L4)                 │
│   ├── Bot detection                       ├── TCP proxy for WebSocket                 │
│   ├── Rate limiting                       └── Origin IP concealment                   │
│   ├── SSL termination                                                                 │
│   └── Static asset caching                Cloud Armor (GCP-native backup WAF)         │
│                                                                                       │
│   Domain Routing:                                                                     │
│   api.inplay.com/*          → GCP Cloud Load Balancer → Cloud Run services            │
│   realtime.inplay.com       → Cloudflare Spectrum → Centrifugo MIG                    │
│   app.inplay.com            → Cloud CDN (static React Native bundle)                  │
│   www.inplay.com            → Cloud Run (marketing site, scales to zero)               │
└───────────────────────────────────────────────────────────────────────────────────────┘
           │                           │
┌──────────▼───────────────────────────▼───────────────────────────────────────────────┐
│                          GCP API GATEWAY                                              │
│   Path-based routing + JWT validation at edge + per-route rate limiting               │
│   /auth/*     → Auth Service          /ads/*     → Ad Service                         │
│   /trading/*  → Trading Service       /leaderboard/* → Leaderboard Service            │
│   /market/*   → Market Data Service                                                   │
│   /social/*   → Social Service                                                        │
└──────┬──────────┬──────────┬──────────┬──────────┬──────────┬────────────────────────┘
       ▼          ▼          ▼          ▼          ▼          ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        CLOUD RUN SERVICES (Stateless APIs)                            │
│                                                                                       │
│  ┌───────────┐ ┌───────────┐ ┌────────────┐ ┌────────┐ ┌─────────┐ ┌─────────────┐  │
│  │   Auth    │ │ Trading   │ │Market Data │ │ Social │ │   Ad    │ │ Leaderboard │  │
│  │  Service  │ │ Service   │ │ Service    │ │Service │ │ Service │ │  Service    │  │
│  │          │ │           │ │            │ │        │ │         │ │             │  │
│  │ Signup   │ │ Orders    │ │ Teams      │ │Referral│ │Campaign │ │ NATS sub:   │  │
│  │ Login    │ │ Positions │ │ Games      │ │Notifs  │ │Delivery │ │ prices+fills│  │
│  │ JWT      │ │ Wallet    │ │ News (SR)  │ │3rd Spc │ │Targeting│ │ Redis ZADD  │  │
│  │ KYC      │ │ P&L       │ │ Stats      │ │        │ │Impressn │ │ Rankings    │  │
│  │          │ │           │ │ History    │ │        │ │         │ │             │  │
│  │ min=10   │ │ min=50    │ │ min=20     │ │ min=10 │ │ min=10  │ │ min=2       │  │
│  └────┬─────┘ └────┬─────┘ └─────┬──────┘ └───┬────┘ └────┬────┘ └──────┬──────┘  │
│       └─────────────┴─────────────┴────────────┴───────────┴─────────────┘          │
│       Shared code in every container: tzero_client, sportradar_client,               │
│       persona_client, jwt_middleware, redis_client, nats_client, SQLAlchemy models    │
└──────────────────────────────┬──────────────────────────────────────────────────────┘
                               │
       ┌───────────────────────┼───────────────────────┐
       ▼                       ▼                       ▼
┌─────────────┐  ┌────────────────────┐  ┌────────────────────────────┐
│ Cloud SQL   │  │ Memorystore        │  │ NATS JetStream             │
│ PostgreSQL  │  │ Redis              │  │ 3-node cluster             │
│             │  │                    │  │                            │
│ Source of   │  │ Leaderboard sorted │  │ All real-time messaging:   │
│ truth for:  │  │ sets, wallet cache,│  │ market data, orders,       │
│ users,      │  │ session tokens,    │  │ fills, game events,        │
│ orders,     │  │ FIX seq numbers,   │  │ ad triggers, leaderboard   │
│ positions,  │  │ ad targeting,      │  │                            │
│ wallets,    │  │ geo queries        │  │ Centrifugo uses NATS as    │
│ referrals,  │  │                    │  │ its broker natively        │
│ campaigns   │  │ NOT used for       │  │                            │
│             │  │ messaging          │  │                            │
└─────────────┘  └────────────────────┘  └─────────────┬──────────────┘
                                                        │
                     NATS is the backbone ──────────────┤
                     Everything publishes to it.        │
                     Everything subscribes from it.     │
                                                        │
┌───────────────────────────────────────────────────────▼──────────────────────────────┐
│                    REAL-TIME LAYER (Stateful, Long-Lived)                              │
│                                                                                       │
│  ┌──────────────────────────────────────┐  ┌──────────────────────────────────────┐   │
│  │  Centrifugo (Managed Instance Group) │  │  FIX Gateway (Compute Engine VMs)    │   │
│  │                                      │  │                                      │   │
│  │  3-25 VMs (schedule-controlled)      │  │  Primary + Standby (co-located       │   │
│  │  e2-standard-8 (8 vCPU, 32GB)       │  │  with tZERO for <1ms latency)        │   │
│  │  ~200K connections per VM            │  │  e2-standard-4 (4 vCPU, 16GB)        │   │
│  │  1M-5M total capacity               │  │                                      │   │
│  │                                      │  │  4 FIX 4.2 sessions:                 │   │
│  │  Features:                           │  │  ├── IOI Market Data (order book)    │   │
│  │  • JWT auth (same as API services)   │  │  ├── FIX Market Data (quotes/trades) │   │
│  │  • Channel-based pub/sub             │  │  ├── Order Entry (submit/cancel)     │   │
│  │  • Last-value cache on reconnect     │  │  └── Drop Copy (execution reports)   │   │
│  │  • Delta updates (bandwidth saving)  │  │                                      │   │
│  │  • Auto-reconnect + msg recovery     │  │  Also hosts: Leaderboard Worker      │   │
│  │  • Presence (who's watching a game)  │  │  (separate process, cgroup isolated,  │   │
│  │  • Protobuf + JSON protocols         │  │   ~150-200MB RAM, ~1.25% CPU)            │   │
│  │  • NATS broker mode (native)         │  │                                      │   │
│  │                                      │  │  Publishes all data → NATS           │   │
│  │  Kernel tuning for 200K+ conns:      │  │  Receives orders ← NATS             │   │
│  │  fs.file-max = 3,276,750            │  │                                      │   │
│  │  fs.nr_open = 1,048,576             │  │  HA: Active/standby. FIX session     │   │
│  │  TCP buffer tuning                   │  │  state in Redis. NATS JetStream      │   │
│  │                                      │  │  replays missed messages on failover │   │
│  └──────────────────────────────────────┘  └──────────────────────────────────────┘   │
└──────────────────────────────────────────────────────┬────────────────────────────────┘
                                                       │ FIX 4.2 over TCP/IP
┌──────────────────────────────────────────────────────▼────────────────────────────────┐
│                         EXTERNAL DEPENDENCIES                                         │
│                                                                                       │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐     │
│  │  tZERO ATS     │  │  Sport Radar   │  │  Persona       │  │  tZERO REST API │     │
│  │                │  │                │  │                │  │                 │     │
│  │  FIX 4.2:      │  │  Push API:     │  │  KYC:          │  │  POST /auth/    │     │
│  │  • IOI feed    │  │  • Play-by-play│  │  • Age 18+     │  │  POST /accounts │     │
│  │  • Market data │  │  • Live stats  │  │  • Identity    │  │  POST/GET /kyc  │     │
│  │  • Order entry │  │  • News feed   │  │  • No bots     │  │  GET /balances  │     │
│  │  • Drop copy   │  │  REST API:     │  │  • US citizen  │  │  GET /snapshots │     │
│  │                │  │  • Historical  │  │                │  │  GET /history   │     │
│  │                │  │  • Schedules   │  │                │  │  POST/DEL orders│     │
│  └────────────────┘  └────────────────┘  └────────────────┘  └─────────────────┘     │
└───────────────────────────────────────────────────────────────────────────────────────┘
```

### Service Connection Map -- Who Talks to What

Not all services connect to NATS. Only services dealing with real-time events do.

| Service | PostgreSQL | Redis | NATS | tZERO FIX | tZERO REST | Sport Radar | Persona |
|---------|-----------|-------|------|-----------|-----------|------------|---------|
| Trading Service | Read/Write | Wallet cache | Pub/Sub (orders, fills) | Via FIX Gateway | Fee estimation | -- | -- |
| Auth Service | Read/Write | Session cache | -- | -- | Account creation, KYC | -- | KYC verification |
| Market Data Service | Read/Write | Data cache | -- | -- | Snapshots, history | Stats, news, schedule | -- |
| Social Service | Read/Write | -- | -- | -- | -- | -- | -- |
| Ad Service | Read/Write | Geo + targeting | Pub/Sub (game events, ad triggers) | -- | -- | -- | -- |
| Leaderboard Service | Read (startup + EOD) | Sorted sets, position cache | Pub/Sub (prices, fills, leaderboard) | -- | -- | -- | -- |
| FIX Gateway | -- | FIX seq numbers | Pub/Sub (all market data, orders) | 4 FIX sessions | -- | -- | -- |
| Centrifugo | -- | -- | Subscribe (all, broker mode) | -- | -- | -- | -- |

### Why Services Don't Call Each Other

Services share data through PostgreSQL, Redis, and NATS JetStream -- not through HTTP calls. This avoids cascading failures, latency compounding, distributed debugging complexity, and circular dependency risks.

---

## 3. Tech Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Mobile + Web App** | React Native (Expo) | Single codebase for iOS, Android, and web. Team knows React. Expo has mature WebSocket and web support |
| **Marketing Sites** | Static site / lightweight framework | Doesn't need app infrastructure. SEO matters here |
| **API Services** | Python / FastAPI | Team's primary language. Async-first, native WebSocket support, Pydantic validation |
| **FIX Gateway** | Python / QuickFIX | Maintains 4 FIX 4.2 sessions to tZERO. Same language as backend |
| **Real-Time Delivery** | Centrifugo | Purpose-built WebSocket fan-out server. Handles 1M+ connections, last-value cache, channel pub/sub. Written in Go |
| **Message Bus** | NATS JetStream | 18M msgs/sec throughput, persistent delivery, built-in last-value cache, message replay. Centrifugo uses NATS as broker natively |
| **Database** | PostgreSQL (Cloud SQL) | ACID guarantees for financial transactions. Users, orders, positions, wallets, referrals |
| **Cache / Leaderboards** | Redis (Memorystore) | Sorted sets for 12 leaderboards. Session cache, wallet balance cache, geo queries for ad targeting |
| **Cloud Platform** | Google Cloud Platform | Team's existing platform |

### Alternatives Considered

**Frontend:** Flutter rejected (Dart has no synergy with Python backend, weaker web). Native iOS + Android rejected (3x effort). PWA rejected (limited push notifications on iOS).

**Backend:** Node.js/TypeScript rejected (team stronger in Python). Go rejected (introduces second backend language unnecessarily).

**Real-Time:** Custom WebSocket servers rejected (Python can't handle 1M connections). Ably/Pusher rejected ($50K+/month at 1M connections). Socket.IO rejected (same Python scaling limitations).

**Message Bus:** Redis Pub/Sub rejected (fire-and-forget, no persistence -- missed fills would corrupt wallets). Kafka rejected (higher latency, operational overhead). Google Cloud Pub/Sub rejected (~10-50ms latency vs NATS ~0.1ms).

**Database:** MongoDB rejected (wallet transactions require ACID). Firestore rejected (lacks relational queries for leaderboards and P&L).

Full details: [[decisions/tech-stack]]

---

## 4. Services

### 4.1 Trading Service

The hot path for order execution. Separate Cloud Run service so nothing else competes for resources during trading spikes.

- **Path:** `/trading/*`
- **Min-instances:** 50 (game day)
- **Request latency target:** <10ms per request

**Endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| POST | `/trading/orders` | Place a new order (buy/sell) |
| DELETE | `/trading/orders/{clOrdId}` | Cancel an order |
| PUT | `/trading/orders/{clOrdId}` | Replace an order (cancel/replace) |
| GET | `/trading/orders` | List user's orders (open + recent) |
| GET | `/trading/orders/{clOrdId}` | Get single order status |
| GET | `/trading/positions` | Get user's current positions |
| GET | `/trading/pnl` | Get user's P&L (daily/weekly/monthly) |
| GET | `/trading/wallet` | Get trading + referral wallet balances |

**Order flow:**
1. Auth middleware validates JWT, extracts userId
2. Order validator checks symbol, side, qty, price, ClOrdID format (max 20 chars, no leading zeroes), OrdType=2 (Limit), ExDestination=STX
3. Wallet check reads balance from Redis cache, verifies sufficient funds, checks 100K cap
4. NATS request/reply to FIX Gateway (`gateway.orders.new`)
5. Immediate ack to client -- user does NOT wait for tZERO to process
6. Background: subscribes to `order.{userId}.>` on NATS for fill events → updates PostgreSQL + Redis

**Wallet rules:**
- Trading wallet starts at 100,000 on signup, can never exceed 100,000
- When trading wallet drops below 25,000, user can reload from referral wallet back to 100,000
- Referral wallet cannot be used for trading directly -- only to reload trading wallet
- Referral wallet has no cap but resets to zero at end of season

Full details: [[services/trading-service]]

### 4.2 Auth Service

- **Path:** `/auth/*`
- **Min-instances:** 10 (game day)

**Endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/signup` | Create new account |
| POST | `/auth/login` | Login, returns JWT |
| POST | `/auth/refresh` | Refresh JWT token |
| GET | `/auth/me` | Get current user profile |
| PUT | `/auth/me` | Update profile |
| POST | `/auth/kyc/submit` | Initiate KYC via Persona |
| GET | `/auth/kyc/status` | Check KYC verification status |
| POST | `/auth/kyc/webhook` | Persona webhook for KYC completion |

**KYC flow:** User signs up → account created (status: PENDING_KYC) → user submits KYC → Persona verifies (age 18+, real identity, no bots, US citizenship) → webhook fires → on approval: credit 100K, generate referral code, trigger referral rewards if referee.

**JWT:** 1-hour expiry, HMAC-SHA256. Validated at API Gateway edge and by shared middleware in each service. Stored in Expo SecureStore (mobile) or httpOnly cookie (web).

**Scaling profile:** Spikes before games (login surge), quiet during games (users already logged in).

Full details: [[services/auth-service]]

### 4.3 Market Data Service

- **Path:** `/market/*`
- **Min-instances:** 20 (game day)

**Endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/market/teams` | List all teams (NFL + college) |
| GET | `/market/teams/{symbol}` | Team detail (stats, price history, upcoming games) |
| GET | `/market/teams/{symbol}/history` | Historical price data from tZERO REST API |
| GET | `/market/games` | Upcoming and live game schedule |
| GET | `/market/games/{gameId}` | Single game detail |
| GET | `/market/news` | News feed (Sport Radar editorial + block trade alerts) |
| GET | `/market/news/{articleId}` | Single article |
| POST/DELETE | `/market/favourites/{symbol}` | Follow/unfollow a team |
| GET | `/market/favourites` | List user's followed teams |

**Data sources:** Sport Radar (team stats, player data, news, schedule -- Redis cached 5-min TTL), tZERO REST API (historical prices -- Redis cached 1-hour TTL), PostgreSQL (favourites, preferences).

**Important:** This service handles non-real-time requests. Live price updates, order book changes, and game events go through Centrifugo (WebSocket), not through this service.

Full details: [[services/market-data-service]]

### 4.4 Social Service

- **Path:** `/social/*`
- **Min-instances:** 10 (game day)

Handles referral engine and push notifications. Referral endpoints: GET `/social/referral/code`, `/social/referral/stats`, `/social/referral/wallet`. Notification endpoints: POST `/social/notifications/register`, GET/PUT `/social/notifications/preferences`.

**Referral mechanics:** Auto-generated codes on KYC approval. Dual-sided reward (1,000 referrer / 500 referee on KYC completion). Referral wallet no cap, resets end of season. Social media engagement credits. Bonus multiplier days (e.g., July 4th = 2x). Sponsor redemption for large referral banks.

Full details: [[services/social-service]]

### 4.5 Ad Service

- **Path:** `/ads/*`
- **Min-instances:** 10 (game day)
- InPlay's revenue model is ~90% advertising for the challenge

**Phase 1 (launch):** Google Ad Manager. GAM SDK handles everything client-side. Direct-sold sponsorships (100% revenue) + programmatic backfill via AdMob (Google takes ~40%).

**Phase 2 (post-launch):** Custom moment-based system. Sponsors own game moments (touchdowns, turnovers). Pre-computed targeting segments in Redis. Sport Radar game event → match against campaigns → publish ad payload via Centrifugo to qualifying users. ~100ms from event to ad delivery.

**Targeting data (first-party, KYC-verified):** Age (Persona), location (device GPS, GEORADIUS), teams followed, trading behaviour, session duration.

**Privacy:** Privacy policy must disclose data use for advertising. Location requires device permission (user can decline). CCPA "Do Not Sell" option for California users. Extra care with 18-20 year old age-gated data.

Full details: [[services/ad-service]]

### 4.6 Leaderboard Service

- **Path:** `/leaderboard/*`
- **Min-instances:** 2 (always-on, maintains NATS subscriptions)

**Dual responsibility:** Event-driven NATS subscriber (recalculates P&L on every price change and fill) + REST API (serves pre-computed rankings from Redis sorted sets).

**Endpoints:** GET `/leaderboard/{vertical}/{timeframe}`, GET `/leaderboard/me`, GET `/leaderboard/proximity`.

**Three verticals:** Best P&L, Best risk-adjusted return, Comeback trader of the day.
**Four timeframes:** Daily, weekly, monthly, full season = 12 sorted sets in Redis.

**Why event-driven:** At 1M users, batch-querying all positions from PostgreSQL every 5 seconds is expensive (5M+ rows). Event-driven only recalculates users affected by each price change.

**Leaderboard Worker on FIX Gateway VM (Option A):** Runs as a separate process with cgroup resource limits (MemoryMax=2G, CPUQuota=100%). ~150-200MB RAM, ~1.25% of one core at peak. If it crashes, systemd restarts it in 2 seconds. FIX Gateway unaffected due to process isolation. NATS JetStream replays missed messages on reconnect.

Full details: [[services/leaderboard-service]]

### 4.7 FIX Gateway

- **Platform:** Compute Engine VM (co-located with tZERO)
- **HA:** Active/standby with Redis for session state

Maintains 4 persistent FIX 4.2 sessions to tZERO:

| Session | Purpose | Recovery on Disconnect |
|---------|---------|----------------------|
| IOI v1.2 | Order book indications of interest | Full state replay from scratch |
| FIX Market Data v8 | Quotes, trades, OHLC, security/session status | Re-subscribe everything (no session recovery, ResetSeqNumFlag=Y) |
| Order Entry v2.2 | Order submission, execution reports, cancels | Standard FIX gap detection and resend |
| Drop Copy | Read-only execution report stream | Standard FIX recovery |

**Internal architecture:** 4 adapters (IOI, MD, OE, DC) + Session Manager + Message Envelope Wrapper + Deduplication + Order Queue Consumer. All state machines are DFAs (deterministic -- no ambiguous states in a trading system).

**Why it doesn't scale with users:** Market data is per-symbol (500 symbols × 50 updates/sec = 25,000 msgs/sec regardless of user count). Fan-out is Centrifugo's job. Orders scale with users but are absorbed by Trading Service → NATS queue → FIX Gateway drains at tZERO's rate.

10 DFA state machines defined in [[integrations/t0]]: IOI Feed Session, FIX MD Session, Per-Symbol Subscription, IOI Order Book Entry, FIX Incremental Refresh, Order Lifecycle, Execution Lifecycle, Cancel/Replace, Trading Session, Security Status.

Full details: [[services/fix-gateway]], [[integrations/t0]]

### 4.8 Centrifugo

- **Platform:** Managed Instance Group (3-25 VMs, e2-standard-8)
- **Capacity:** 1M-5M concurrent WebSocket connections

Purpose-built WebSocket fan-out server (Go, open source). Backend publishes to NATS → Centrifugo delivers to subscribed users via WebSocket. No custom code -- configured via YAML.

**Channel mapping:**

> **Naming convention:** NATS topics use dots as delimiters (e.g., `market.quote.IGBI`). Centrifugo channels use colons (e.g., `market:quote:IGBI`). Centrifugo's NATS broker mode maps between the two automatically.

| Centrifugo Channel | Data | NATS Source Topic |
|--------------------|------|-------------------|
| `market:snapshot:{symbol}` | OHLC, volume, previous close | `market.snapshot.{symbol}` |
| `market:quote:{symbol}` | Best bid/offer, last price | `market.quote.{symbol}` |
| `market:trade:{symbol}` | Individual trade executions | `market.trade.{symbol}` |
| `market:book:{symbol}` | Order book depth changes | `market.book.{symbol}` |
| `market:status:{symbol}` | Halt/resume, short sell restriction | `market.status.{symbol}` |
| `market:session` | Trading session phase (PRE/CORE/POST) | `market.session` |
| `game:events:{gameId}` | Sport Radar play-by-play | `game.events.{gameId}` |
| `order:{userId}` | Order accepted, filled, cancelled, rejected | `order.{userId}.{clOrdId}` |
| `position:{userId}` | Position and P&L updates | `position.{userId}` |
| `leaderboard:{vertical}:{timeframe}` | Rank changes | `leaderboard.{vertical}.{timeframe}` |
| `ad:trigger:{gameId}` | Volatility moment broadcast (all users watching game) | `ad.trigger.{gameId}` |
| `ad:{userId}` | Targeted ad delivery (per-user) | `ad.{userId}` |
| `news:feed` | Sport Radar news updates | `news.feed` |

**Key features:** JWT auth (shared secret with Auth Service), last-value cache (instant catch-up on reconnect), delta updates (only sends diffs), auto-reconnect + message recovery via sequence numbers, presence (per-channel user counting), Protobuf + JSON protocols, NATS broker mode (native).

**Why MIG not Cloud Run:** WebSocket connections are long-lived (hours during games). Cloud Run recycles containers, dropping all connections. MIG VMs stay alive until explicitly removed.

Full details: [[services/centrifugo]], [[infrastructure/scaling-and-realtime]]

### Cloud Run Jobs

| Job | Trigger | Purpose |
|-----|---------|---------|
| End-of-Day Settlement | Daily after market close | Expire orders, snapshot P&L, calculate prizes |
| Referral Processor | On KYC completion | Credit referrer (1,000) and referee (500) |

### Monorepo Structure

```
inplay-backend/
├── shared/                        ← copied into every container at build time
│   ├── auth/jwt_middleware.py
│   ├── integrations/
│   │   ├── tzero_client.py        ← tZERO REST API wrapper
│   │   ├── sportradar_client.py
│   │   ├── persona_client.py
│   │   └── redis_client.py
│   ├── models/                    ← SQLAlchemy models shared across services
│   │   ├── user.py, order.py, wallet.py, referral.py
│   └── config/settings.py         ← Pydantic settings, env var pattern
├── services/
│   ├── trading/   (Dockerfile, main.py, routers/)
│   ├── auth/
│   ├── market-data/
│   ├── social/
│   └── ads/
├── gateway/                        ← FIX Gateway (Compute Engine)
│   ├── Dockerfile, main.py, adapters/
└── shared-docker/Dockerfile.base
```

---

## 5. Infrastructure

### GCP Deployment Model

```
Cloud Run Services (stateless APIs, auto-scaling):
├── Trading Service      /trading/*     min=50 game day
├── Auth Service         /auth/*        min=10 game day
├── Market Data Service  /market/*      min=20 game day
├── Social Service       /social/*      min=10 game day
├── Ad Service           /ads/*         min=10 game day
└── Leaderboard Service  /leaderboard/* min=2  always-on

Cloud Run Jobs (scheduled batch):
├── End-of-day settlement (daily)
└── Referral reward processing (on KYC completion)

Managed Instance Group (long-lived WebSocket):
└── Centrifugo VMs (3-25, schedule-controlled)

Compute Engine VMs (persistent FIX sessions):
├── FIX Gateway Primary (co-located with tZERO)
└── FIX Gateway Standby

Managed Services:
├── Cloud SQL (PostgreSQL)
├── Memorystore (Redis)
├── NATS JetStream (3-node cluster)
├── Cloud Load Balancer + Cloud Armor
├── Cloud CDN
├── Google Cloud API Gateway
└── Cloud Scheduler
```

### Why Cloud Run, Not GKE

Cloud Run provides auto-scaling, zero-downtime deployments, and managed infrastructure without Kubernetes operational overhead. GKE adds cluster management, node pool sizing, networking, upgrade maintenance -- disproportionate for 5 stateless API services. Mid-August timeline favours lower-overhead infrastructure.

**Revisit for year 2** if service count grows, costs spike at sustained peak, or custom networking (service mesh, mTLS) is needed. Migration is straightforward -- same Docker containers deploy to GKE Autopilot with no code changes.

### Cloud Run vs GKE at 1M Users

| Factor | Cloud Run | GKE Autopilot |
|--------|-----------|---------------|
| WebSockets | 60-min timeout | Native, no timeout |
| Long-lived TCP (FIX) | Not suitable | Full control |
| Cold starts | ~200ms with startup CPU boost | None |
| Cost at sustained peak | Expensive (per-instance-second billing) | Cheaper with committed use discounts |
| Ops complexity | Zero | Low (Autopilot) |
| Stateful workloads | Stateless only | StatefulSets, persistent volumes |

### API Gateway

Google Cloud API Gateway provides path-based routing, JWT validation at edge, per-route rate limiting (stricter on `/trading/*`, relaxed on `/market/*`), at ~$3-5 per million requests.

Full details: [[infrastructure/infrastructure]], [[infrastructure/api-gateway]], [[decisions/infrastructure-decisions]]

---

## 6. Data Layer

### PostgreSQL (Cloud SQL)

Source of truth. Tables: users, orders, positions, wallets, referrals, teams, games, news, campaigns, impressions, leaderboard snapshots, KYC records.

All Cloud Run services read/write to the same instance. Services share data through the database, not inter-service HTTP calls.

### Redis (Memorystore)

Two roles (NOT used for messaging -- NATS handles that):

1. **Sorted Sets** -- 12 leaderboard rankings (3 verticals × 4 timeframes). Updated incrementally by Leaderboard Service via NATS events, read by Leaderboard Service REST API.
2. **Cache** -- wallet balances, session tokens, user profiles, FIX sequence numbers, pre-computed ad targeting segments, geo queries (GEORADIUS for ad targeting within 3 miles).

### NATS JetStream (3-node cluster)

All real-time messaging flows through NATS. Topics:

| Topic Pattern | Publisher | Subscribers |
|--------------|-----------|------------|
| `market.snapshot.{symbol}` | FIX Gateway | Centrifugo |
| `market.quote.{symbol}` | FIX Gateway | Centrifugo, Leaderboard Service |
| `market.trade.{symbol}` | FIX Gateway | Centrifugo |
| `market.book.{symbol}` | FIX Gateway | Centrifugo |
| `market.status.{symbol}` | FIX Gateway | Centrifugo |
| `market.session` | FIX Gateway | Centrifugo |
| `order.{userId}.{clOrdId}` | FIX Gateway | Centrifugo, Trading Service |
| `position.{userId}` | FIX Gateway | Centrifugo |
| `gateway.orders.new` | Trading Service | FIX Gateway (request/reply) |
| `game.events.{gameId}` | Market Data Service | Centrifugo, Ad Service |
| `ad.trigger.{gameId}` | Ad Service | Centrifugo (broadcast to all users watching game) |
| `ad.{userId}` | Ad Service | Centrifugo (targeted ads to specific users) |
| `leaderboard.{vertical}.{timeframe}` | Leaderboard Service | Centrifugo |

JetStream provides persistence: if a service restarts, it replays missed messages on reconnect. Centrifugo uses NATS as its broker natively -- publishes to NATS are automatically delivered to WebSocket clients.

---

## 7. Real-Time Layer

### FIX Streaming (Primary Path)

All real-time market data and order execution flows through FIX 4.2:

```
tZERO ──FIX 4.2──▶ FIX Gateway ──NATS──▶ Centrifugo ──WSS──▶ User App
```

**FIX is the primary path for:**
- Order entry (NewOrderSingle, Cancel, Replace)
- Market data streaming (snapshots + incremental refreshes)
- IOI feed (order book depth)
- Drop Copy (execution reports, fills)
- Trading session / security status

### tZERO REST API (Complement, Non-Streaming)

REST fills gaps where streaming doesn't make sense:

| Category | Endpoints | Use |
|----------|-----------|-----|
| **Authentication** | POST `/auth/v1/api/token`, POST `/auth/v1/api/refresh` | Backend service auth (1-hour bearer token) |
| **Onboarding** | POST `/pi/v1/accounts/individual`, POST/GET `/pi/v1/users/{userId}/kyc` | Account creation, KYC triggering |
| **Balance** | GET `/pi/v1/accounts/{accountId}/balances` | Wallet balance queries |
| **Markets** | GET `/markets/v1/mdt/public-snapshots/{symbol}`, GET `/markets/v1/mdt/public-pricehistory/{symbol}` | Initial page load, historical charts |
| **Trading** | POST/GET/DELETE `/trading/v1/accounts/{accountId}/orders` | REST alternative for orders (higher latency than FIX) |
| **Investments** | Various `/pi/v1/assets/*` endpoints | IPO flow (production only, not challenge scope) |

---

## 8. Data Flows

### Price Update (tZERO → User Screen, target <100ms)

```
tZERO sends FIX message (trade: Cowboys 200 shares @ $25.60)
  │ Hop 1: <1ms (co-located)
  ▼
FIX Gateway parses, normalizes to JSON
  │ Hop 2: <2ms (binary FIX parsing)
  ▼
Publishes to NATS: market.trade.cowboys
  │ Hop 3: <2ms (in-memory pub/sub)
  ▼
Centrifugo delivers via WebSocket
  │ Hop 4: <5ms (same datacenter) + <30ms (geographic)
  ▼
Client renders
  │ Hop 5: <16ms (60fps)
  ▼
Total: <56ms typical, <100ms p99
```

### Order Placement (User → tZERO → Confirmation)

```
User taps BUY → API Gateway → Trading Service:
  1. Validate JWT, order format
  2. Check wallet (Redis)
  3. Publish to NATS (gateway.orders.new)
  4. Return ack immediately (<50ms from tap)

  Async: FIX Gateway → FIX NewOrderSingle → tZERO
         tZERO → ExecutionReport → FIX Gateway → NATS
         → Centrifugo → User sees "Order Filled"
         → Trading Service → update PostgreSQL + Redis
```

### User Reconnection (WiFi drop)

```
WiFi drops → WebSocket disconnects → "Reconnecting..." indicator
  During gap: server-side unaffected. Orders processed normally.
WiFi returns → Centrifugo auto-reconnects (<1 second)
  → Re-subscribes to channels
  → Last-value cache delivers current state immediately
  → Fill confirmations during gap delivered on reconnect
  → No stale data, no loading spinner
```

### Ad Delivery (Moment-Based, Post-Launch)

```
Sport Radar: "Touchdown -- Cowboys, Q3, 7:42"
  → Ad Service matches event against campaigns (PostgreSQL)
  → Reads pre-computed user segments (Redis SET, ~1ms)
  → Publishes ad payload to qualifying users (Centrifugo, ~5ms)
  → User sees sponsored ad within ~100ms of touchdown
```

Full details: [[data-flows/price-update-flow]], [[data-flows/order-placement-flow]], [[data-flows/user-reconnection-flow]], [[data-flows/ad-delivery-flow]]

---

## 9. Frontend

### React Native (Expo)

Single codebase targeting iOS, Android, and web. **No frontend server** -- the app runs entirely on the user's device. Backend calls go to FastAPI (REST) and Centrifugo (WebSocket).

```
iOS:     Downloaded from App Store, runs on iPhone
Android: Downloaded from Google Play, runs on Android
Web:     Static JS bundle served from Cloud CDN, runs in browser
```

**Key libraries:** Expo Router (file-based routing), centrifuge JS SDK (WebSocket), react-native-wagmi-charts or victory-native (price charts), expo-secure-store (JWT storage), expo-notifications, expo-location (GPS for ad targeting).

### Deployment

- **iOS:** `eas build --platform ios` → `eas submit` → Apple review (1-7 days). First submission 2-3 weeks before launch.
- **Android:** `eas build --platform android` → Google review (hours to 1-2 days).
- **Web:** `expo export:web` → Cloud CDN. No review, deploy anytime.
- **OTA updates:** For JS-only changes (~90% of updates), push directly to devices without store review. Minutes to users.

### Performance

| Concern | Solution |
|---------|----------|
| Rapid price updates (100/sec) | Client-side throttle: batch renders to 4-5/sec |
| Reconnection | Centrifugo JS SDK auto-reconnects, last-value cache provides instant catch-up |
| Bandwidth | Full depth only for active symbol. Watchlist gets top-of-book only. Unsubscribe on navigate away |
| Background/lock | Drop WebSocket, reconnect on foreground. Last-value cache eliminates stale data |
| Bundle size | Code splitting via Expo Router. Target <3MB initial bundle |

Full details: [[frontend/frontend-architecture]], [[frontend/frontend-deployment]], [[frontend/frontend-performance]]

---

## 10. External Integrations

| Integration | Purpose | Protocol | Status |
|------------|---------|----------|--------|
| **tZERO ATS** | Trading engine, price data, order book, trade execution | FIX 4.2 (4 sessions) + REST API | Partnered |
| **Sport Radar** | Real-time sports data (push every 1-2s), live match tracker (HTML5 widget), 10-15 years historical, news, win probabilities | Push API + REST API + embedded widget | Licensed |
| **Persona** | KYC / identity verification (age 18+, identity, no bots, US citizenship) | REST API + embedded UI flow | Setup in progress |
| **Google Ad Manager** | Ad serving at launch (direct-sold + programmatic backfill) | Client-side SDK | Phase 1 |
| **FCM / APNs** | Push notifications (fill alerts, leaderboard proximity, game reminders) | Cloud Messaging API | -- |

**tZERO REST API full endpoint list:** Authentication (token, refresh), Onboarding (accounts, users, KYC, financial info, trusted contact), Investments (assets, create/submit/cancel), Documents (wire instructions), Bank Accounts (add, list, delete, transfer), Balance (account balance), Markets (schedules, price history, snapshots), Trading (fee estimation, orders CRUD).

Full details: [[integrations/integrations]], [[integrations/t0]]

---

## 11. Scaling Strategy

### Three-Layer Approach

```
Layer 1: SCHEDULED PRE-WARMING
  Game schedule known weeks ahead (Sport Radar)
  Cloud Scheduler bumps min-instances hours before kickoff

Layer 2: CLOUD RUN AUTO-SCALING
  Traffic arrives → Cloud Run spins up containers above min-instances
  40% utilisation target → scales up early with headroom

Layer 3: NATS JETSTREAM AS SHOCK ABSORBER
  If 50K orders arrive in 1 second but tZERO processes 10K/sec
  NATS queues the overflow and drains over the next few seconds
```

### Cloud Run Settings

| Setting | Value | Rationale |
|---------|-------|-----------|
| min-instances | Varies by game day profile | Zero cold starts |
| max-instances | 200 (Trading), 100 (others) | Cost ceiling |
| concurrency | 250 (target 500 after load testing) | I/O-bound services can handle more |
| CPU allocation | Always allocated (Trading, Market Data, Leaderboard). Request-based (Auth, Social, Ad) | Trading needs NATS subscriptions between requests. Auth/Social/Ad are pure request/response |
| Startup CPU boost | Enabled | Cuts cold start from ~500ms to ~200ms |
| Utilisation target | 40% | Scale-up triggers early, maintains buffer for touchdown spikes |

### Game Day Scaling Profiles

| Service | Off-hours | Thursday Night | NFL Sunday (3+ games) | Super Bowl |
|---------|-----------|---------------|----------------------|------------|
| Trading min | 5 | 30 | 50 | 100 |
| Trading max | 50 | 100 | 200 | 400 |
| Auth min | 2 | 10 | 10 | 20 |
| Market Data min | 3 | 10 | 20 | 40 |
| Social min | 2 | 5 | 10 | 20 |
| Ad min | 1 | 5 | 10 | 20 |
| Centrifugo VMs | 3 | 10 | 25 | 25 |
| Connection capacity | 600K | 2M | 5M | 5M |

> Super Bowl profile uses the same Centrifugo capacity as NFL Sunday but doubles Cloud Run min-instances to absorb higher per-user trading intensity.

### Automated Scheduling

Weekly Cloud Run Job reads Sport Radar game schedule → classifies game days (1 game = standard, 3+ = peak, Super Bowl = maximum) → creates Cloud Scheduler jobs (pre-warm 3 hours before first kickoff, scale down 6 hours after last game).

### Touchdown Spike Handling

```
t=0.0s  Touchdown. 50K users tap BUY.
t=0.3s  50 warm containers absorb ~5,000 concurrent. Auto-scale triggers.
t=0.5s  New containers starting (200ms cold start with CPU boost).
t=1.0s  10-20 new containers online. Burst absorbed.
t=2.0s  Orders flowing through NATS → FIX Gateway → tZERO.
t=3.0s  Spike subsiding. Zero orders lost.
```

Full details: [[infrastructure/scaling]], [[infrastructure/scaling-and-realtime]]

---

## 12. Cost Optimisation

### In-Season Cost Reduction Strategies

| Strategy | Saving | Effort |
|----------|--------|--------|
| Split CPU allocation (request-based for Auth/Social/Ad) | 15-20% total | Low -- config change |
| Right-size CPU/memory (1 vCPU for Auth/Social/Ad) | 10-20% total | Low -- config change |
| Tighter two-step scale-down windows | ~$2-3.5K/season | Low -- adjust scheduler |
| Higher concurrency (250→500 after load testing) | 20-40% fewer containers | Medium -- load testing |
| 1-year committed use discount on baseline | ~$250-400/month | Low -- purchase |
| Move Leaderboard Worker to FIX Gateway VM | ~$200-300/month | Medium -- code change |

### Cost Estimates

```
Off-season:  ~$1,800-2,500/month
In-season:   ~$4,500-9,000/month (optimised, down from $8-15K)
Super Bowl:  ~$1,500-2,000 for that single day
```

Compared to a fixed GKE cluster sized for peak (~$15K-25K/month year-round), scheduled scaling saves 50-70% during off-hours and off-season.

Full details: [[infrastructure/scaling-and-realtime]] (Section 5)

---

## 13. Performance Targets

### Latency Budget (tZERO → User Screen)

| Hop | Component | Target |
|-----|-----------|--------|
| 1 | tZERO → FIX Gateway (network) | <1ms |
| 2 | FIX Gateway parse + normalize | <2ms |
| 3 | Gateway → NATS JetStream publish | <2ms |
| 4 | NATS → Centrifugo (same datacenter) | <5ms |
| 5 | Centrifugo → client (geographic) | <30ms |
| 6 | Client render | <16ms |
| **Total** | | **<56ms typical, <100ms p99** |

### Per-Data-Type Targets

| Data Type | Bus Publish Target | User Delivery Target |
|-----------|-------------------|---------------------|
| Best Bid/Offer | <5ms from receipt | <50ms to screen |
| Trades | <5ms | <50ms |
| OHLC Bar | <10ms | <100ms |
| Order Book Depth | <10ms | <100ms |
| Order Status | <5ms | <50ms |
| Position/P&L | <5ms | <50ms |

### Throughput

| Metric | Estimate |
|--------|----------|
| Symbols watched per user (avg) | 10 |
| Unique symbols across all users | ~500 |
| Market updates per symbol per second (peak) | 50 (estimated, confirm with tZERO) |
| Total upstream msgs/sec from tZERO | 25,000 |
| WebSocket msgs/sec per user (peak) | 500 (before conflation) |
| Conflation target | Max 10 updates/sec per symbol to client |

Full details: [[performance/latency-budget]], [[performance/throughput]]

---

## 14. Testing Strategy

All tests orchestrated via GitHub Actions. Performance results stream to Grafana Cloud.

### Tools

| Tool | Tests | When |
|------|-------|------|
| **pytest** (Python) | Unit + integration (backend) | Every PR / every merge |
| **Vitest** (TypeScript) | Unit + component (frontend) | Every PR |
| **Grafana k6** | Load, stress, spike, soak, API, WebSocket | Nightly / weekly / pre-season |
| **Custom Go harness** | FIX 4.2 protocol load testing | Weekly / pre-season |
| **OWASP ZAP** | Security scanning (OWASP Top 10) | Weekly / every release candidate |

### k6 Game Day Scenarios

| Test | VUs | Duration | When | Key Metric |
|------|-----|----------|------|------------|
| **Smoke** | 10 | 1 min | Every PR | p95 <200ms, errors <1% |
| **Load (Thursday)** | 3,000 | 60 min | Nightly | p95 <100ms, p99 <300ms |
| **Stress (Sunday)** | 10,000 | 60 min | Weekly | Find breaking point |
| **Spike (Touchdown)** | 1K→8K in 10s | 20 min | Weekly | Cloud Run scales <3s, zero orders lost |
| **Soak (Full day)** | 5,000 | 8 hours | Pre-season / monthly | No memory leaks, no connection drift |

### WebSocket Tests

- Connection scale: ramp to 100K+ connections, verify 200K per Centrifugo VM
- Message delivery latency: p50 <20ms, p95 <50ms, p99 <100ms at 100K connections
- Reconnection recovery: 100% message recovery, zero duplicates

### Pass/Fail Criteria

| Level | Metric | Threshold |
|-------|--------|-----------|
| **Blocking** | Unit test pass rate | 100% |
| **Blocking** | Smoke test p95 | <200ms |
| **Warning** | Load test p95 | <100ms |
| **Informational** | Stress test breaking point | Track trend over time |
| **Informational** | Soak test memory growth | Should be flat |

### Pre-Season Calendar

Week 1: Smoke + API contract + load test. Week 2: Stress + spike + WebSocket scale. Week 3: Soak (8h) + FIX throughput + security scan. Week 4: Full dress rehearsal.

Full details: [[performance/testing-strategy]]

---

## 15. Security

### Edge Protection

| Layer | Tool | What it protects |
|-------|------|-----------------|
| L7 DDoS + WAF + bot detection | Cloudflare CDN + WAF | Websites, REST APIs, static assets |
| L3/L4 DDoS for TCP/WebSocket | Cloudflare Spectrum | WebSocket gateway (Centrifugo) |
| Backup WAF + rate limiting | Cloud Armor (GCP-native) | All GCP endpoints |
| VPC / private subnets | GCP networking | Trading VMs, FIX Gateway, databases, NATS |

### Application Security

- **OAuth2 / JWT** on every API request. 1-hour expiry, HMAC-SHA256.
- **Rate limiting** per user, per endpoint. Stricter on order submission.
- **Input validation** on order entry (qty, price, symbol), search, referral codes.
- **CORS policies** restricting which origins can call APIs.

### Trading-Specific Security

- **Order rate limiting** -- max orders per second per user (prevents bot trading)
- **ClOrdID validation** -- reject duplicate or malformed order IDs
- **Position limits** -- 100K wallet cap enforced server-side
- **Price band checks** -- reject orders outside reasonable range (before sending to tZERO)
- **Session binding** -- WebSocket sessions tied to authenticated JWT

### Data Protection

- **TLS 1.3 everywhere** (user ↔ app, app ↔ tZERO, app ↔ Sport Radar, app ↔ Persona)
- **Encryption at rest** (AES-256) for user PII, trade history, KYC references
- **Persona handles KYC docs** -- identity documents never touch InPlay infrastructure
- **Secret management** via GCP Secret Manager

### Mobile App Security

- Certificate pinning (prevent MITM)
- Jailbreak / root detection
- Code obfuscation
- Secure local storage (encrypted keychain/keystore for JWT)

---

## 16. Open Questions

| Question | Impact | Who Answers | Status |
|----------|--------|-------------|--------|
| **CRITICAL: What does tZERO manage for the simulation?** | Determines whether InPlay stores trade data, positions, wallets, P&L in PostgreSQL or if tZERO handles all of this. Single biggest question affecting architecture complexity. | tZERO / Edwin | **BLOCKING** |
| Does the Trading Service validate wallet balance, or does tZERO? | If tZERO validates, Trading Service is a passthrough. If InPlay validates, need Redis wallet cache + PostgreSQL writes. | tZERO / Edwin | Open |
| Where is tZERO's matching engine physically? | Determines FIX Gateway VM location and network link. Co-location required for <1ms latency. | tZERO | Open |
| FIX 4.2 or FIX 4.4? PDFs say 4.2, online docs say 4.4. | Affects FIX Gateway implementation. Different message formats. | tZERO | Open |
| Does tZERO support multiple concurrent OE FIX sessions? | Could enable parallel order processing during spikes. | tZERO | Open |
| Does tZERO KYC replace Persona, or do we still need both? | tZERO REST API has KYC endpoints. If tZERO handles KYC end-to-end, one less vendor. | tZERO / Troy | Open |
| tZERO order throughput limit? | Determines whether order queuing causes noticeable delay during game spikes. | tZERO | Open |
| tZERO REST API rate limits? | Affects non-streaming operations. | tZERO | Open |
| tZERO sandbox access timeline? | Blocks FIX Gateway integration testing. | tZERO / Edwin | Open |
| Sport Radar delivery method -- push feed or polling? | Push = simpler, lower latency. Poll = more control but higher latency. | Sport Radar | Open |
| tZERO REST API full endpoint list? | API explorer is JS-rendered, couldn't scrape. Need docs from tZERO. | tZERO | Open |
| Do we need a Fill Processor service? | Only needed if InPlay stores trade data in PostgreSQL. If tZERO owns all trade state, fills just flow through NATS to Centrifugo and Leaderboard Service. | Depends on tZERO answer | Open |
| Leaderboard Service: Python or Bun/TypeScript? | Most CPU-intensive service. Python may bottleneck during peak recalculations. Bun significantly faster for CPU-bound work. Start Python, rewrite if needed. | Load testing | Open |
| Which API gateway does Brett prefer? | His operational experience is more valuable than our analysis. | Brett | Open |
| App Store first submission timing? | Apple review 1-7 days, may reject. Need 2-3 weeks buffer. | Planning | Open |

---

## Document Index

All detailed sub-documents referenced throughout:

| Section | Document | Path |
|---------|----------|------|
| Decisions | Tech Stack | [[decisions/tech-stack]] |
| Decisions | Frontend Framework | [[decisions/frontend-framework]] |
| Decisions | Infrastructure | [[decisions/infrastructure-decisions]] |
| Services | Overview | [[services/services-overview]] |
| Services | Trading | [[services/trading-service]] |
| Services | Auth | [[services/auth-service]] |
| Services | Market Data | [[services/market-data-service]] |
| Services | Social | [[services/social-service]] |
| Services | Ad | [[services/ad-service]] |
| Services | Leaderboard | [[services/leaderboard-service]] |
| Services | FIX Gateway | [[services/fix-gateway]] |
| Services | Centrifugo | [[services/centrifugo]] |
| Infrastructure | GCP Overview | [[infrastructure/infrastructure]] |
| Infrastructure | Scaling | [[infrastructure/scaling]] |
| Infrastructure | Scaling + Real-Time | [[infrastructure/scaling-and-realtime]] |
| Infrastructure | API Gateway | [[infrastructure/api-gateway]] |
| Infrastructure | Networking | [[infrastructure/networking]] |
| Data Flows | Price Update | [[data-flows/price-update-flow]] |
| Data Flows | Order Placement | [[data-flows/order-placement-flow]] |
| Data Flows | User Reconnection | [[data-flows/user-reconnection-flow]] |
| Data Flows | Ad Delivery | [[data-flows/ad-delivery-flow]] |
| Frontend | Architecture | [[frontend/frontend-architecture]] |
| Frontend | Deployment | [[frontend/frontend-deployment]] |
| Frontend | Performance | [[frontend/frontend-performance]] |
| Integrations | Overview | [[integrations/integrations]] |
| Integrations | tZERO (full spec) | [[integrations/t0]] |
| Performance | Latency Budget | [[performance/latency-budget]] |
| Performance | Throughput | [[performance/throughput]] |
| Performance | Testing Strategy | [[performance/testing-strategy]] |
| Open | Questions | [[open-questions]] |
