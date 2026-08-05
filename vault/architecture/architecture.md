# InPlay Trading Challenge -- Technical Architecture

> **Project:** [[index]]
> **Status:** Draft
> **Date:** 2026-05-10
> **Owner:** Novosapien
> **Sources:** Vision document, tZERO integration spec, architecture workshop sessions

## Overview

The InPlay Trading Challenge is a simulated sports equity trading platform targeting 1M-5M concurrent users at peak load. Users trade team stocks during live NFL and college football games using simulated currency, competing for real cash prizes ($5M-$25M season pool).

This architecture covers the trading challenge only -- not the production trading platform.

The system consists of 6 Cloud Run services (5 API + 1 Leaderboard), a FIX Gateway on Compute Engine, Centrifugo for real-time WebSocket delivery on a Managed Instance Group, NATS JetStream as the message backbone, and a React Native (Expo) frontend serving iOS, Android, and web from a single codebase.

## System Architecture Diagrams

### High-Level Overview

```mermaid
graph TB
    subgraph Clients
        APP[React Native App<br/>iOS · Android · Web]
    end

    CDN[Cloud CDN<br/>Web app bundle]

    subgraph EdgeRT["Real-Time Path"]
        CENT[Centrifugo<br/>Managed Instance Group<br/>1M-5M WebSocket connections]
    end

    subgraph EdgeREST["REST Path"]
        LB[Cloud Load Balancer + Cloud Armor<br/>+ API Gateway<br/>SSL · DDoS · JWT · Rate Limiting]
    end

    subgraph CloudRun["Cloud Run Services"]
        TRADING[Trading Service<br/>/trading/*]
        AUTH[Auth Service<br/>/auth/*]
        MARKET[Market Data Service<br/>/market/*]
        SOCIAL[Social Service<br/>/social/*]
        ADS[Ad Service<br/>/ads/*]
        LEADER[Leaderboard Service<br/>/leaderboard/*]
    end

    subgraph Messaging
        NATS[NATS JetStream<br/>3-node cluster<br/>Message backbone]
    end

    subgraph Data["Data Stores"]
        PG[(PostgreSQL · Cloud SQL<br/>Source of truth)]
        REDIS[(Redis · Memorystore<br/>Speed layer)]
    end

    subgraph tZero["tZERO Co-Location"]
        FIX[FIX Gateway<br/>Compute Engine VM<br/>4 FIX 4.2 sessions]
        FIX_STANDBY[FIX Gateway Standby]
        TZERO[tZERO Exchange · ATS]
    end

    subgraph External["External Services"]
        SR[Sport Radar]
        PERSONA[Persona KYC]
        FCM[FCM / APNs]
        TZERO_REST[tZERO REST API]
    end

    %% Client connections
    APP -- "WebSocket" --> CENT
    APP -- "HTTPS REST" --> LB
    APP -. "first load" .-> CDN

    %% Load balancer sits on top of Cloud Run services
    LB --> CloudRun

    %% Cloud Run services read/write data stores (two clean arrows)
    CloudRun -- "queries + writes" --> PG
    CloudRun -- "cache reads + writes" --> REDIS

    %% Real-time data flow (the main loop)
    FIX -- "publishes: market data,<br/>order fills, positions" --> NATS
    NATS -- "delivers real-time updates" --> CENT
    CENT -- "WebSocket push" --> APP

    %% Trading Service → FIX Gateway for order execution
    TRADING -- "NATS request/reply<br/>(order submission)" --> FIX

    %% NATS subscribers (services that need real-time events)
    TRADING -. "subscribes: fills" .-> NATS
    LEADER -. "subscribes: prices, fills<br/>publishes: leaderboard updates" .-> NATS
    ADS -. "subscribes: game events<br/>publishes: ad triggers" .-> NATS

    %% FIX Gateway connections
    FIX -- FIX 4.2 --> TZERO
    FIX --> REDIS
    FIX_STANDBY -. failover .-> FIX
```

### Service Connection Map -- Who Talks to What

Not all services connect to NATS. Only services dealing with real-time events do. Auth, Market Data, and Social are REST-only services reading from PostgreSQL and Redis.

```mermaid
graph LR
    subgraph NATS_Connected["Connected to NATS"]
        FIX[FIX Gateway<br/>publishes all market data + fills]
        TRADING[Trading Service<br/>request/reply for orders<br/>subscribes for fills]
        LEADER[Leaderboard Service<br/>subscribes to prices + fills<br/>publishes leaderboard updates<br/>serves /leaderboard/* REST API]
        ADS[Ad Service<br/>subscribes to game events<br/>publishes ad triggers]
        CENT[Centrifugo<br/>subscribes to all via broker mode]
    end

    subgraph REST_Only["REST-only (no NATS)"]
        AUTH[Auth Service]
        MARKET[Market Data Service]
        SOCIAL[Social Service<br/>referrals + notifications only]
    end

    subgraph Data
        NATS[NATS JetStream]
        PG[(PostgreSQL)]
        REDIS[(Redis)]
    end

    subgraph External
        TZERO[tZERO Exchange]
        SR[Sport Radar]
        PERSONA[Persona]
        FCM[FCM/APNs]
        TZERO_REST[tZERO REST]
    end

    %% Order flow: Trading Service → FIX Gateway via NATS request/reply
    TRADING -- "NATS request/reply:<br/>gateway.orders.new" --> FIX
    
    %% FIX Gateway publishes results to NATS
    FIX -- "publishes: market.*, order.*, position.*" --> NATS
    FIX -- "FIX 4.2" --> TZERO
    
    %% Services subscribing to NATS
    TRADING -- "subscribes: order fills" --> NATS
    LEADER -- "subscribes: prices, fills" --> NATS
    LEADER -- "publishes: leaderboard.*" --> NATS
    ADS -- "subscribes: game events" --> NATS
    ADS -- "publishes: ad.*" --> NATS
    CENT -- "subscribes: all (broker mode)" --> NATS

    %% PostgreSQL connections (all services)
    TRADING --> PG
    AUTH --> PG
    MARKET --> PG
    SOCIAL --> PG
    ADS --> PG
    LEADER --> PG

    %% Redis connections
    TRADING -- "wallet cache" --> REDIS
    AUTH -- "session cache" --> REDIS
    MARKET -- "data cache" --> REDIS
    LEADER -- "sorted sets, position cache" --> REDIS
    ADS -- "geo queries, targeting sets" --> REDIS
    FIX -- "FIX seq numbers" --> REDIS

    %% External API connections
    AUTH -- "KYC" --> PERSONA
    MARKET -- "stats, news" --> SR
    MARKET -- "historical data" --> TZERO_REST
    SOCIAL -- "push notifications" --> FCM
```

### Data Flow: Price Update

```mermaid
sequenceDiagram
    participant tZERO as tZERO
    participant FIX as FIX Gateway
    participant NATS as NATS JetStream
    participant CENT as Centrifugo
    participant LDR as Leaderboard Service
    participant REDIS as Redis
    participant APP as User's App

    tZERO->>FIX: FIX message (price change)
    Note over FIX: Parse + normalize (<2ms)
    FIX->>NATS: publish market.quote.cowboys
    
    par Fan-out
        NATS->>CENT: deliver to subscriber
        CENT->>APP: WebSocket push to all watching Cowboys
        Note over APP: User sees new price (<100ms total)
    and Leaderboard update
        NATS->>LDR: deliver to subscriber
        Note over LDR: Recalculate P&L for Cowboys holders only
        LDR->>REDIS: ZADD leaderboard:pnl:daily (affected users)
        LDR->>NATS: publish leaderboard.pnl.daily (top movers)
        NATS->>CENT: deliver leaderboard update
        CENT->>APP: WebSocket push leaderboard change
    end
```

### Data Flow: Order Placement

```mermaid
sequenceDiagram
    participant APP as User's App
    participant GW as API Gateway
    participant TS as Trading Service
    participant FIX as FIX Gateway
    participant NATS as NATS JetStream
    participant tZERO as tZERO
    participant CENT as Centrifugo
    participant REDIS as Redis
    participant PG as PostgreSQL

    APP->>GW: POST /trading/orders (Buy 100 Cowboys @ $25)
    GW->>TS: Route + JWT validated
    TS->>REDIS: Check wallet balance
    REDIS-->>TS: Balance: 87,430
    Note over TS: Validate order (~10ms total)
    TS->>FIX: NATS request/reply (gateway.orders.new)
    FIX-->>TS: {status: "accepted", clOrdId: "ORD456"}
    TS-->>APP: 200 OK {status: "acknowledged"}
    Note over APP: User sees "Order Pending"
    
    FIX->>tZERO: FIX NewOrderSingle
    tZERO-->>FIX: ExecutionReport (Filled)
    FIX->>NATS: publish order.user123.ORD456 (filled)
    
    par Notify user
        NATS->>CENT: deliver
        CENT->>APP: WebSocket "Order Filled: 100 @ $25.00"
    and Update state
        NATS->>TS: deliver fill event
        TS->>PG: Update positions, wallet
        TS->>REDIS: Update wallet cache
    end
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
- [[app-store-accounts]] -- developer account emails, live store URLs and app identifiers
- [[frontend-performance]] -- Client-side throttling, subscriptions, reconnection

### Integrations
- [[integrations]] -- Summary of all external dependencies
- [[tzero|tZERO]] -- tZERO FIX 4.2 + REST API specification
- [[sportradar]] -- Sport Radar real-time data integration
- [[persona]] -- Persona KYC integration

### Performance
- [[latency-budget]] -- <100ms end-to-end target, per-hop breakdown
- [[throughput]] -- 25K msg/sec upstream, 500M fan-out, conflation strategies

### Open
- [[open-questions]] -- Unresolved questions with owners and impact
