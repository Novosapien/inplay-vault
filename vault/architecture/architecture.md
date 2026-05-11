# InPlay Trading Challenge -- Technical Architecture

> **Project:** [[index]]
> **Status:** Draft
> **Date:** 2026-05-10
> **Owner:** Novosapien
> **Sources:** Vision document, T0 integration spec, architecture workshop sessions

## Overview

The InPlay Trading Challenge is a simulated sports equity trading platform targeting 1M-5M concurrent users at peak load. Users trade team stocks during live NFL and college football games using simulated currency, competing for real cash prizes ($5M-$25M season pool).

This architecture covers the trading challenge only -- not the production trading platform.

The system consists of 6 Cloud Run services (5 API + 1 Leaderboard), a FIX Gateway on Compute Engine, Centrifugo for real-time WebSocket delivery on a Managed Instance Group, NATS JetStream as the message backbone, and a React Native (Expo) frontend serving iOS, Android, and web from a single codebase.

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENTS                                        │
│                  React Native (Expo) -- iOS, Android, Web                   │
│                         Single codebase, no server                          │
│                  Web bundle served from Cloud CDN                           │
│                                                                             │
│              WebSocket (wss://)              HTTPS (REST)                    │
└───────────────────┬─────────────────────────────┬───────────────────────────┘
                    │                              │
                    ▼                              ▼
┌───────────────────────────────┐  ┌──────────────────────────────────────────┐
│        CENTRIFUGO             │  │         CLOUD LOAD BALANCER              │
│   (Managed Instance Group)    │  │         + CLOUD ARMOR                    │
│                               │  │         + API GATEWAY                    │
│   1M-5M WebSocket connections │  │                                          │
│   NATS broker mode (native)   │  │   SSL · DDoS · JWT · Rate Limiting      │
│   Last-value cache            │  │   Path-based routing to services         │
│   3-25 VMs (game-day scaling) │  │                                          │
└───────────┬───────────────────┘  └──────┬─────┬─────┬─────┬─────┬──────────┘
            │                             │     │     │     │     │
            │ subscribes                  │     │     │     │     │
            │                             ▼     ▼     ▼     ▼     ▼
            │                        ┌─────────────────────────────────────┐
            │                        │      CLOUD RUN SERVICES             │
            │                        │                                     │
            │                        │  /trading/*  → Trading Service      │
            │                        │  /auth/*     → Auth Service         │
            │                        │  /market/*   → Market Data Service  │
            │                        │  /social/*   → Social Service       │
            │                        │  /ads/*      → Ad Service           │
            │                        │                                     │
            │                        │  Leaderboard Service (internal,     │
            │                        │  no REST API, subscribes to NATS)   │
            │                        └──────────────────┬──────────────────┘
            │                                           │
            ▼                                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          NATS JETSTREAM                                      │
│                     (3-node cluster, message backbone)                       │
│                                                                             │
│   All real-time messaging flows through NATS:                               │
│   market.quote.{symbol}     market.book.{symbol}     market.trade.{symbol}  │
│   market.status.{symbol}    market.session            order.{user}.{id}     │
│   position.{user}           leaderboard.{v}.{t}      ad.{user}             │
│                                                                             │
│   Persistent (JetStream) · Message replay · Last-value cache                │
│   18M msgs/sec throughput · <0.1ms latency                                  │
└────────────────────────────────────────┬────────────────────────────────────┘
                                         │
                                         │ publishes to / subscribes from
                                         │
┌────────────────────────────────────────┼────────────────────────────────────┐
│              tZERO CO-LOCATION         │                                    │
│                                        │                                    │
│  ┌─────────────────────────────────────▼──────────────────────────────┐     │
│  │              FIX GATEWAY (Compute Engine VM)                        │     │
│  │                                                                    │     │
│  │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │     │
│  │   │ IOI Adapter  │  │ MD Adapter   │  │ OE Adapter   │            │     │
│  │   │ (order book) │  │ (quotes,     │  │ (orders,     │            │     │
│  │   │              │  │  trades,     │  │  fills,      │            │     │
│  │   │              │  │  OHLC)       │  │  cancels)    │            │     │
│  │   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘            │     │
│  │          │ FIX 4.2         │ FIX 4.2         │ FIX 4.2            │     │
│  └──────────┼─────────────────┼─────────────────┼────────────────────┘     │
│             ▼                 ▼                  ▼                          │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │                     tZERO EXCHANGE (ATS)                         │       │
│  │         Order matching · Price discovery · Execution             │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│                                                                            │
│  FIX Gateway Standby (failover, ~5-10s takeover)                           │
└────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         DATA STORES                                          │
│                                                                             │
│   ┌──────────────────────────┐    ┌──────────────────────────────────┐      │
│   │  PostgreSQL (Cloud SQL)  │    │  Redis (Memorystore)             │      │
│   │                          │    │                                  │      │
│   │  Source of truth:        │    │  Speed layer:                    │      │
│   │  Users, orders,          │    │  Leaderboard sorted sets (12)    │      │
│   │  positions, wallets,     │    │  Wallet balance cache            │      │
│   │  referrals, teams,       │    │  Session cache                   │      │
│   │  campaigns, KYC records  │    │  Position cache (by symbol)      │      │
│   │                          │    │  Geo queries (ad targeting)      │      │
│   │  ACID transactions       │    │  FIX sequence numbers            │      │
│   │  for wallet operations   │    │  Pre-computed ad targeting sets  │      │
│   └──────────────────────────┘    └──────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                       EXTERNAL SERVICES                                      │
│                                                                             │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│   │ Sport Radar  │  │ Persona      │  │ FCM / APNs   │  │ tZERO REST   │   │
│   │ Game data,   │  │ KYC: age,    │  │ Push notifs  │  │ Historical   │   │
│   │ stats, news  │  │ identity,    │  │ iOS/Android  │  │ data, accts  │   │
│   │              │  │ bot detect   │  │              │  │              │   │
│   └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Tech Stack Summary

| Layer | Technology |
|-------|-----------|
| Frontend | React Native (Expo) -- iOS, Android, Web |
| API Services | Python / FastAPI (6 Cloud Run services) |
| FIX Gateway | Python / QuickFIX (Compute Engine VM) |
| Real-Time Delivery | Centrifugo (Managed Instance Group, NATS broker mode) |
| Message Bus | NATS JetStream (3-node cluster) |
| Database | PostgreSQL (Cloud SQL) |
| Cache / Data Structures | Redis (Memorystore) |
| Cloud Platform | Google Cloud Platform |

## Architecture Sections

### Decisions
- [[tech-stack]] -- What we chose and why, with alternatives considered
- [[frontend-framework]] -- React Native (Expo) vs Flutter vs Next.js, framework landscape
- [[infrastructure-decisions]] -- Cloud Run vs GKE, Compute Engine, API Gateway decisions

### Services
- [[services-overview]] -- Service map, monorepo structure, shared package, who talks to who
- [[trading-service]] -- Order execution, wallet management, position tracking
- [[auth-service]] -- Authentication, JWT, signup/login, KYC (Persona)
- [[market-data-service]] -- Teams, games, news, stats, Sport Radar integration
- [[social-service]] -- Referrals, leaderboards, notifications
- [[ad-service]] -- Google Ad Manager at launch, custom moment-based system post-launch
- [[fix-gateway]] -- FIX 4.2, 4 adapters, state machines, high availability
- [[centrifugo]] -- Real-time delivery, channels, Managed Instance Group, conflation

### Infrastructure
- [[infrastructure]] -- GCP deployment model, what runs where, managed services
- [[scaling]] -- Game-day scaling, min-instances, MIG schedules, scaling profiles
- [[api-gateway]] -- Routing, rate limiting, JWT validation at edge
- [[networking]] -- Load balancer, Cloud Armor, CDN, domains

### Data Flows
- [[price-update-flow]] -- tZERO to user screen (<100ms target)
- [[order-placement-flow]] -- User to tZERO and back
- [[user-reconnection-flow]] -- WebSocket drop, reconnect, last-value cache
- [[ad-delivery-flow]] -- Game event to targeted ad delivery

### Frontend
- [[frontend-architecture]] -- React Native (Expo), no server, runs on device
- [[frontend-deployment]] -- App Store, Play Store, Web/CDN, OTA updates
- [[frontend-performance]] -- Client-side throttling, subscriptions, reconnection

### Integrations
- [[integrations]] -- Summary of all external dependencies
- [[t0]] -- tZERO FIX 4.2 + REST API specification
- [[sportradar]] -- Sport Radar real-time data integration
- [[persona]] -- Persona KYC integration

### Performance
- [[latency-budget]] -- <100ms end-to-end target, per-hop breakdown
- [[throughput]] -- 25K msg/sec upstream, 500M fan-out, conflation strategies

### Open
- [[open-questions]] -- Unresolved questions with owners and impact
