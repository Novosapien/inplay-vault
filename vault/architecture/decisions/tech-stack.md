# Tech Stack Decisions

> **Architecture:** [[architecture]]
> **Status:** Draft

## Summary

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Mobile + Web App** | React Native (Expo) | Single codebase for iOS, Android, and web. Team knows React. Expo has mature WebSocket and web support. |
| **Marketing Sites** | Static site / lightweight framework | Doesn't need app infrastructure. SEO matters here. |
| **API Services** | Python / FastAPI | Team's primary language. Async-first, native WebSocket support, Pydantic validation. Used for all 6 Cloud Run services (see open question on Leaderboard Service below). |
| **Trading Gateway** | Python / QuickFIX | Maintains 4 FIX 4.2 sessions to tZERO. Python keeps the gateway in the same language as most backend services. |
| **Real-Time Delivery** | Centrifugo | Purpose-built WebSocket fan-out server. Handles 1M+ connections, last-value cache, channel-based pub/sub. Deployed as a Docker container, configured via YAML, interacted with via Python and JavaScript SDKs. |
| **Message Bus** | NATS JetStream | Purpose-built messaging server. 18M msgs/sec throughput, persistent message delivery, built-in last-value cache, message replay on reconnect. Centrifugo uses NATS as its broker natively. No messages lost if a service restarts. |
| **Database** | PostgreSQL (Cloud SQL) | Users, orders, positions, wallets, referrals, leaderboard snapshots, ad inventory, KYC records. |
| **Cache / Leaderboards** | Redis (Memorystore) | Sorted sets for leaderboard rankings (3 verticals x 4 timeframes). Session cache, wallet balance cache, geo queries for ad targeting. Not used for messaging (NATS handles that). |
| **Cloud Platform** | Google Cloud Platform | Team's existing platform. |

## Alternatives Considered

### Frontend: React Native (Expo)

| Option | Considered | Rejected Because |
|--------|-----------|-----------------|
| React Native (Expo) | **Chosen** | -- |
| React Native + Next.js (separate web app) | Yes | Two codebases to maintain, divergent UIs, double the frontend effort |
| Flutter | Yes | Weaker web support, smaller hiring pool, requires Dart (no synergy with Python backend) |
| Native iOS + Native Android + Web | Yes | 3x the development effort, 3 codebases, 3 separate tech stacks to maintain |
| Progressive Web App only | Yes | Limited push notification support on iOS, no app store presence, reduced performance for real-time charts |

### Backend: Python / FastAPI

| Option | Considered | Rejected Because |
|--------|-----------|-----------------|
| Python / FastAPI | **Chosen** | -- |
| Node.js / TypeScript | Yes | Team is stronger in Python. Would introduce a second backend language alongside Python (needed for QuickFIX). |
| Go | Yes | Introduces a second backend language alongside Python. High performance but unnecessary given FastAPI's async capabilities and the architecture's use of Redis for throughput-critical paths. |
| Java / Spring Boot | Yes | Heavier framework, introduces a second backend language. QuickFIX/J exists but adding Java to a Python stack increases maintenance burden. |

### Real-Time Delivery: Centrifugo

| Option | Considered | Rejected Because |
|--------|-----------|-----------------|
| Centrifugo | **Chosen** | -- |
| Custom WebSocket servers (FastAPI) | Yes | Python can't handle 1M concurrent WebSocket connections. Would need to build channel management, reconnection, last-value cache, scaling, message ordering from scratch. Weeks of engineering for solved problems. |
| Ably (managed) | Yes | Potentially $50K+/month at 1M concurrent connections. Adds third-party dependency on the critical real-time path. |
| Pusher (managed) | Yes | Same cost concerns as Ably. Rate limits may not suit high-frequency market data. |
| Socket.IO with Redis adapter | Yes | Python Socket.IO server has same scaling limitations as raw WebSockets. |
| AWS AppSync | Yes | Team is on GCP, not AWS. Would introduce cross-cloud dependency. |

### Message Bus: NATS JetStream

| Option | Considered | Rejected Because |
|--------|-----------|-----------------|
| NATS JetStream | **Chosen** | -- |
| Redis Pub/Sub | Yes | Fire-and-forget delivery -- messages lost if no subscriber is listening. No persistence, no replay, no built-in last-value cache. Acceptable for caching but not for a trading platform where missed fill confirmations mean incorrect wallet balances. |
| Apache Kafka | Yes | Significant operational overhead (ZooKeeper/KRaft, topic management, consumer groups). Higher latency than NATS. Designed for log-style streaming, not low-latency request/reply patterns. |
| Google Cloud Pub/Sub | Yes | Higher latency (~10-50ms) vs NATS (~0.1ms). Not designed for the message-per-second volume of real-time market data fan-out. Better suited for async event processing. |
| RabbitMQ | Yes | Lower throughput than NATS. More complex clustering. AMQP protocol adds overhead vs NATS's lightweight protocol. |

**Why NATS over Redis for messaging:**

| Requirement | Redis Pub/Sub | NATS JetStream |
|-------------|--------------|----------------|
| Message persistence | No -- lost if no subscriber listening | Yes -- persisted to disk, replay on reconnect |
| Last-value cache | No (manual implementation) | Built-in per subject |
| Throughput | ~500K msgs/sec | ~18M msgs/sec |
| Latency | ~0.5ms | ~0.1ms |
| Consumer groups | No | Yes (queue groups for load balancing) |
| Wildcard subscriptions | Limited pattern matching | Rich subject hierarchy (market.quote.>) |
| Centrifugo integration | Redis broker mode | NATS broker mode (native) |
| Message replay | No | Yes (from any point in the stream) |

For a trading platform, the persistence guarantee is critical. If the Trading Service restarts for 2 seconds and misses fill confirmations, user wallets won't update. NATS JetStream eliminates this risk.

### Database: PostgreSQL

| Option | Considered | Rejected Because |
|--------|-----------|-----------------|
| PostgreSQL (Cloud SQL) | **Chosen** | -- |
| MongoDB | Yes | Wallet transactions require ACID guarantees. Eventual consistency is unacceptable for financial balances. PostgreSQL provides this out of the box. |
| Firestore | Yes | Good for simple document storage but lacks the relational queries needed for leaderboard calculations, referral chain tracking, and complex P&L reporting. |
| CockroachDB / Spanner | Yes | Distributed SQL is unnecessary at launch. Single-region Cloud SQL with read replicas handles the load. Adds operational complexity and cost without clear benefit for year 1. |
