# Scaling Strategy & Real-Time Infrastructure

> **Architecture:** [[architecture]]
> **Status:** Draft
> **Date:** 2026-05-12

---

## 1. Centrifugo -- Real-Time WebSocket Gateway

### What It Is

Centrifugo is an open-source real-time messaging server written in Go. It sits between the backend services and the mobile app, handling all persistent WebSocket connections. It's a PUB/SUB fan-out layer -- backend services publish messages to channels, Centrifugo delivers them to every subscribed user instantly.

It's the self-hosted alternative to Pusher, Ably, or Socket.io. InPlay owns the infrastructure, pays no per-message fees, and has full control over performance tuning.

### Why Centrifugo

| Requirement | How Centrifugo handles it |
|-------------|--------------------------|
| 1M+ concurrent WebSocket connections | Single instance handles 1M connections. Horizontal scaling across nodes for more |
| Sub-50ms message delivery | Benchmarked at 30M messages/minute (500K msg/sec) with p99 latency <200ms |
| Multiple transports | WebSocket, HTTP-streaming, SSE, WebTransport, gRPC |
| NATS broker integration | Native NATS support -- publishes to NATS are automatically delivered to WebSocket clients. No custom glue code |
| Reconnection recovery | Channel history with automatic message recovery on reconnect. Client provides last seen sequence number, Centrifugo replays missed messages |
| Authentication | JWT-based connection auth. InPlay's Auth Service issues the JWT, Centrifugo validates it. No separate auth system needed |
| Presence | Per-channel online presence (who's watching this game right now), join/leave notifications |
| Language-agnostic | Backend services just publish to NATS. Centrifugo handles the fan-out. No SDK lock-in on the backend |
| Protocol efficiency | Binary Protobuf protocol for mobile (smaller payloads, faster parsing) and JSON for web |
| Delta updates | Only sends what changed, not the full message. Critical for high-frequency price updates |

### How It Fits In

```
Backend Services                 Centrifugo                    Users
─────────────────          ──────────────────          ─────────────────

FIX Gateway                                             Mobile App
  │ parses tZERO data                                     │
  │ publishes to NATS                                     │ connects via WSS
  ▼                                                       ▼
┌──────────┐    ┌──────────┐    ┌──────────────┐    ┌──────────┐
│          │    │          │    │              │    │          │
│   NATS   │───▶│Centrifugo│───▶│  WebSocket   │───▶│  User    │
│ JetStream│    │  (3-25   │    │  connection  │    │  device  │
│          │    │   VMs)   │    │  (persistent)│    │          │
│          │    │          │    │              │    │          │
└──────────┘    └──────────┘    └──────────────┘    └──────────┘
     ▲
     │
Trading Service
Market Data Service
Leaderboard Service
  (all publish to NATS)
```

### Channel Design for InPlay

Each user subscribes only to the channels they care about. Centrifugo filters at the server -- users don't receive data they didn't subscribe to.

| Channel pattern | Example | What it delivers | Who subscribes |
|----------------|---------|-----------------|----------------|
| `market:quote:{symbol}` | `market:quote:IGBI` | Best bid/offer, last price | Anyone viewing that team's page or game |
| `market:trade:{symbol}` | `market:trade:IGBI` | Individual trade executions | Anyone viewing that team's chart |
| `market:book:{symbol}` | `market:book:IGBI` | Order book depth changes | Anyone viewing order book |
| `game:events:{gameId}` | `game:events:NFL-GB-NYG` | Sport Radar play-by-play, scores | Anyone viewing that game page |
| `order:{userId}` | `order:user_abc123` | Order accepted, filled, cancelled, rejected | That specific user only (private) |
| `position:{userId}` | `position:user_abc123` | Position and P&L updates | That specific user only (private) |
| `leaderboard:{vertical}:{timeframe}` | `leaderboard:pnl:daily` | Leaderboard rank changes | Anyone viewing that leaderboard |
| `news:feed` | `news:feed` | Sport Radar news updates | Anyone on discovery/home page |
| `ad:trigger:{gameId}` | `ad:trigger:NFL-GB-NYG` | Volatility moment ad triggers | Anyone watching that game |

### Authentication Flow

```
1. User logs in → Auth Service issues JWT with:
   {
     "sub": "user_abc123",
     "exp": 1726099200,
     "channels": ["order:user_abc123", "position:user_abc123"]
   }

2. Mobile app connects to realtime.inplay.com with JWT

3. Centrifugo validates JWT signature (shared secret with Auth Service)
   → Connection accepted
   → User auto-subscribed to private channels in the JWT

4. User navigates to Packers game page
   → App subscribes to: market:quote:IGBI, game:events:NFL-GB-NYG
   → Centrifugo delivers latest cached value immediately (last-value cache)
   → Then streams real-time updates

5. User leaves the game page
   → App unsubscribes from those channels
   → Centrifugo stops sending updates (saves bandwidth)

6. JWT approaching expiry
   → Centrifugo triggers refresh mechanism
   → App requests new JWT from Auth Service
   → Connection continues without dropping
```

### Reconnection and Recovery

Mobile connections drop constantly -- subway tunnels, bad signal, app backgrounded. Centrifugo handles this:

```
1. Connection drops (phone enters tunnel)

2. Centrifugo keeps channel history for configured duration (e.g., 5 minutes)

3. Phone regains signal → app reconnects with last seen sequence number

4. Centrifugo replays all missed messages since that sequence number
   → User sees prices jump to current (not stale)
   → Any filled orders during disconnection appear immediately
   → No data loss

5. If disconnected longer than history retention
   → Full snapshot delivered on reconnect (REST fallback)
   → Then resumes streaming
```

### Deployment: Managed Instance Group

Centrifugo runs on Compute Engine VMs in a Managed Instance Group (MIG), not Cloud Run. WebSocket connections are long-lived and stateful -- Cloud Run's 60-minute timeout and stateless model don't work here.

| Config | Value | Rationale |
|--------|-------|-----------|
| VM type | e2-standard-8 (8 vCPU, 32GB RAM) | ~200K connections per VM at 160 bytes/conn |
| MIG size | 3-25 VMs (schedule-controlled) | 600K-5M connection capacity |
| Broker | NATS JetStream (shared with backend) | Native integration, no additional infrastructure |
| Health check | TCP on port 8000 | Auto-replace unhealthy VMs |
| Load balancer | TCP load balancer (not HTTP) | WebSocket connections need TCP-level balancing |
| Kernel tuning | `fs.file-max=3,276,750`, `fs.nr_open=1,048,576` | Required for >200K connections per VM |
| TCP buffers | `net.core.rmem_max=33554432`, `net.core.wmem_max=33554432` | Optimised for high connection count |

---

## 2. Cloud Run Scaling Strategy

### The Problem

Normal Tuesday: 50K active users. NFL Sunday with 3 simultaneous games: 500K-1M. A touchdown in a close game: order volume spikes 10x in seconds. The system must handle predictable ramps, sustained peaks, and micro-bursts without cold starts or dropped requests.

### Cloud Run Settings That Matter

| Setting | What it does | InPlay value |
|---------|-------------|-------------|
| **min-instances** | Containers kept warm, zero cold starts | Varies by game day profile |
| **max-instances** | Hard ceiling, prevents runaway cost | 200 (Trading), 100 (others) |
| **concurrency** | Requests per container before triggering scale-up | 250 |
| **CPU allocation** | "Always allocated" keeps CPU active between requests | Always allocated |
| **Startup CPU boost** | 2x CPU during container startup | Enabled |
| **Utilisation target** | How full a container gets before scaling up | 40% |

### Why "CPU Always Allocated"

With request-based CPU, the container's CPU is throttled to zero between requests. That kills:

- NATS subscriber connections (need CPU to receive messages)
- Database connection pool keep-alives
- Redis cache warming
- Background health checks

With "always allocated", containers stay warm and responsive. Costs more per instance but each one is ready instantly -- no wake-up latency.

### Why 40% Utilisation Target

Default is 60%. InPlay sets 40%.

```
Container concurrency limit = 250 requests

At 60% target: scale-up triggers at 150 concurrent
At 40% target: scale-up triggers at 100 concurrent

Lower target means:
  • Scale-up starts earlier
  • Large buffer of idle capacity absorbs spikes
  • Slightly more containers running (higher cost)
  • But zero cold-start latency when a touchdown spike hits
```

### Three-Layer Scaling Strategy

```
Layer 1: SCHEDULED PRE-WARMING
         Game schedule known weeks ahead (from Sport Radar)
         Cloud Scheduler bumps min-instances hours before kickoff

Layer 2: CLOUD RUN AUTO-SCALING
         Traffic arrives → Cloud Run spins up containers above min-instances
         40% utilisation target → scales up early with headroom

Layer 3: NATS JETSTREAM AS SHOCK ABSORBER
         If 50K orders arrive in 1 second but tZERO processes 10K/sec
         NATS queues the overflow and drains over the next few seconds
         Users get "Order Placed" instantly, "Order Filled" shortly after
```

### Layer 1: Scheduled Pre-Warming

Sport Radar provides game schedules. A weekly Cloud Run Job reads the schedule, classifies each game day by intensity, and creates Cloud Scheduler jobs to pre-warm infrastructure.

```
TIMELINE FOR NFL SUNDAY (1pm ET kickoff, 3 games)
──────────────────────────────────────────────────

10:00 AM  ─── Cloud Scheduler fires "pre-game-warmup"
               Trading Service:    min=5  → min=50
               Auth Service:       min=2  → min=10
               Market Data:        min=3  → min=20
               Social Service:     min=2  → min=10
               Ad Service:         min=1  → min=10
               Centrifugo MIG:     3 VMs  → 15 VMs

11:00 AM  ─── Users start logging in, browsing games
               All containers already warm, zero cold starts

1:00 PM   ─── Kickoff. Trading volume ramps
               50 warm Trading containers handle initial burst
               Auto-scaling adds more if needed

4:30 PM   ─── Games ending. Peak trading in final minutes
               May be at 80-100 Trading instances

5:30 PM   ─── Last game ends. Traffic drops

11:00 PM  ─── Cloud Scheduler fires "post-game-scaledown"
               Trading Service:    min=50 → min=5
               (delayed -- users review P&L, check leaderboard,
                share trades for hours after games end)
```

### Layer 2: Auto-Scaling Within Games

With 50 min-instances at 40% utilisation target:

```
Warm capacity:  50 × 100 trigger point = 5,000 concurrent
                before any new container spins up

Burst capacity: 50 × 250 max concurrency = 12,500 concurrent
                while new containers start (~2-3 seconds)

Throughput:     At 10ms per request
                = 25,000 req/sec per container
                = 1,250,000 req/sec across 50 containers
```

### Layer 3: Micro-Burst Absorption (Touchdown Spike)

```
t=0.0s   Touchdown. Sport Radar fires event.
         50K users tap BUY simultaneously.

t=0.3s   First wave hits Trading Service.
         50 warm containers absorb ~5,000 concurrent.
         Utilisation hits 40% → auto-scale triggers.

t=0.5s   Cloud Run starts new containers.
         Startup CPU boost = ~200ms cold start.
         Existing containers absorb the burst at higher concurrency.

t=1.0s   10-20 new containers online. Burst absorbed.

t=2.0s   Orders flowing: Trading Service → NATS → FIX Gateway → tZERO.
         NATS queues any overflow beyond tZERO's acceptance rate.

t=3.0s   Spike subsiding. No orders lost. No cold starts for users.
```

### Game Day Scaling Profiles

| Service | Off-hours | Thursday Night | NFL Sunday (3 games) | Super Bowl |
|---------|-----------|---------------|---------------------|------------|
| **Trading Service** | | | | |
| min-instances | 5 | 30 | 50 | 100 |
| max-instances | 50 | 100 | 200 | 400 |
| **Auth Service** | | | | |
| min-instances | 2 | 10 | 10 | 20 |
| max-instances | 20 | 30 | 50 | 100 |
| **Market Data** | | | | |
| min-instances | 3 | 10 | 20 | 40 |
| max-instances | 30 | 50 | 100 | 200 |
| **Social Service** | | | | |
| min-instances | 2 | 5 | 10 | 20 |
| max-instances | 20 | 30 | 50 | 100 |
| **Ad Service** | | | | |
| min-instances | 1 | 5 | 10 | 20 |
| max-instances | 20 | 30 | 50 | 100 |
| **Centrifugo VMs** | 3 | 10 | 15 | 25 |
| **Connection capacity** | 600K | 2M | 3M | 5M |

### Automating the Schedule

```
1. Sport Radar publishes weekly game schedule
2. Market Data Service ingests schedule → PostgreSQL
3. Weekly Cloud Run Job reads schedule → classifies game days:
   - 1 game (Thursday night) → "standard" profile
   - 3+ simultaneous games (NFL Sunday) → "peak" profile
   - Major event (Super Bowl, Thanksgiving) → "maximum" profile
4. Creates Cloud Scheduler jobs for each game day:
   ├── 3 hours before first kickoff → "pre-warm" with appropriate profile
   └── 6 hours after last game ends → "scale-down"
5. Cloud Scheduler fires jobs → gcloud CLI updates min/max instances
```

Nobody manually scales anything. The system reads the game schedule and self-configures.

---

## 3. Cloud Run vs GKE at 1M Users

### Comparison

| Factor | Cloud Run | GKE Autopilot |
|--------|-----------|---------------|
| **WebSockets** | 60-min timeout, then disconnects. Max ~1,000 per container | Native, no timeout. Indefinite connections |
| **Long-lived TCP (FIX)** | Not suitable | Full control, persistent pods |
| **Scaling** | Per-request, scales to zero, cold starts possible | Per-pod, always running, HPA for spikes |
| **Cost at sustained peak** | Expensive with CPU always allocated at high min-instances | Cheaper with committed use discounts |
| **Cold starts** | ~200ms with startup CPU boost, ~500ms without | None. Pods always warm |
| **Ops complexity** | Zero. Google manages everything | Low with Autopilot (no node management) |
| **Stateful workloads** | Stateless only | StatefulSets, persistent volumes |
| **Networking** | Limited | Full Kubernetes networking, Istio, network policies |

### Current Architecture Decision

**Cloud Run** for stateless API services (Trading, Auth, Market Data, Social, Ad). These are HTTP request/response handlers that don't need persistent state.

**Compute Engine VMs** for stateful connections:
- Centrifugo (1M+ WebSocket connections, long-lived)
- FIX Gateway (persistent TCP sessions to tZERO)

### When to Consider Migrating to GKE

Move specific services to GKE Autopilot if:
- Cloud Run costs exceed $15K/month sustained (right-sized GKE cluster with committed use discounts becomes cheaper)
- Need custom networking (service mesh, mTLS between services, network policies)
- Need more than 200 max-instances on a single service
- Need DaemonSets or node-level access for monitoring/security agents

The migration path is straightforward -- same Docker containers deploy to either platform. No code changes needed.

---

## 4. Cost Estimates

### Cloud Run (current architecture)

```
Off-hours (min-instances only, CPU always allocated):
  ~$50/day across all services

NFL Sunday (8 hours at peak profile):
  ~$200-400 across all services for that day

Off-season monthly:  ~$1,500
In-season monthly:   ~$4,000-8,000
```

### Centrifugo VMs

```
Off-hours: 3 × e2-standard-8 = ~$18/day
NFL Sunday: 15 × e2-standard-8 = ~$90 for that day (8 hours at peak)
In-season monthly: ~$2,000-4,000
```

### FIX Gateway VMs

```
2 × e2-standard-4 (primary + standby) = ~$8/day
Monthly: ~$240 (constant, doesn't scale)
```

### Total Infrastructure Estimate

```
Off-season:  ~$2,500-3,000/month
In-season:   ~$8,000-15,000/month
Super Bowl:  ~$1,500-2,000 for that single day
```

Compared to a fixed GKE cluster sized for peak (~$15K-25K/month year-round), the scheduled scaling approach saves 50-70% on infrastructure costs during off-hours and off-season.

---

## 5. In-Season Cost Optimisation

Target: bring in-season costs from $8-15K/month down to $4.5-9K/month.

### 5.1 Split CPU Allocation Mode Per Service

Not all services need "CPU always allocated". Services that maintain NATS subscriptions or background connections need always-on CPU. Pure request/response services don't -- they only need CPU while actively handling a request.

| Service | CPU mode | Rationale |
|---------|----------|-----------|
| Trading Service | Always allocated | NATS subscriber, must receive fill events between requests |
| Market Data Service | Always allocated | NATS subscriber for Sport Radar events |
| Auth Service | **Request-based** | Pure request/response. Signup calls Persona + tZERO REST (I/O-bound, ~500ms waiting on external APIs). 1-5ms CPU un-throttle overhead is invisible |
| Social Service | **Request-based** | Pure request/response. Reads from Redis/PostgreSQL |
| Ad Service | **Request-based** | Pure request/response. Serves ad payloads from cache |

Request-based billing is ~2.4x cheaper per vCPU-second than always-allocated.

**Why this is safe for Auth during mass signups:**

A signup request spends ~10ms on CPU and ~500ms waiting on Persona KYC + tZERO account creation. The container has full CPU while the request is active. The only overhead is ~1-5ms CPU un-throttle when a request arrives at an idle container -- invisible against 500ms of network I/O.

At 10,000 simultaneous signups with concurrency=250, Cloud Run auto-scales to 40 containers in ~2-3 seconds. Every user gets a response in under 1 second. 1 vCPU is sufficient because auth work is HMAC-SHA256 signatures (sub-millisecond) and waiting on external APIs.

**Savings:** ~30-40% on Auth, Social, and Ad services.

### 5.2 Right-Size Container CPU and Memory

Default is often 2 vCPU / 2GB RAM per container. Actual CPU requirements per service:

| Service | CPU | Memory | Rationale |
|---------|-----|--------|-----------|
| Trading Service | 2 vCPU | 1GB | CPU-bound during order validation, low memory |
| Market Data Service | 1 vCPU | 1GB | I/O-bound (Sport Radar + PostgreSQL), some in-memory caching |
| Auth Service | 1 vCPU | 512MB | HMAC signatures are sub-ms. Waits on Persona/tZERO 95% of the time |
| Social Service | 1 vCPU | 512MB | Reads from Redis sorted sets + PostgreSQL |
| Ad Service | 1 vCPU | 512MB | Serves payloads from Redis cache |

Halving CPU on Auth, Social, and Ad = ~40% cost reduction on those services.

**1 vCPU handles 1M users on Auth because:**

```
Peak auth load:
  Logins:       300K users over 2 hours = ~42/sec sustained, ~200/sec burst
  JWT refresh:  300K active ÷ 3,600 sec = ~83/sec
  Signups:      ~3-5/sec sustained (spread over weeks)

Throughput per container at 1 vCPU:
  JWT refresh: ~2,000/sec (sub-ms HMAC check)
  Login:       ~1,000/sec (I/O-bound, CPU barely used)
  Signup:      ~500/sec   (I/O-bound, CPU barely used)

1 container handles peak load. 10 min-instances is 10x headroom.
```

### 5.3 Tighter Scale-Down Windows

Most users leave within 1-2 hours of the last game ending. Two-step scale-down saves 2.5 hours of peak min-instances per game day:

```
Current:
  11:00 PM → scale everything down (6 hours after last game)

Optimised:
  7:30 PM  → Trading min=50 → min=20 (most trading done)
  10:00 PM → Trading min=20 → min=5  (stragglers only)
```

**Savings:** ~$30-50 per game day. Over a 17-week season with ~4 game days/week: ~$2,000-3,500/season.

### 5.4 Higher Concurrency

Services are I/O-bound (waiting on PostgreSQL, Redis, NATS, tZERO REST). Each request uses <10ms CPU and waits ~50-500ms on I/O. Containers can handle more concurrent requests than the current 250 setting.

```
Current:   concurrency=250, min-instances=50 → 50 containers at peak
Optimised: concurrency=500, min-instances=30 → 30 containers, same load
```

Requires load testing to validate. If p99 latency stays under 100ms at concurrency=500, adopt it.

**Savings:** ~40% fewer containers at peak.

### 5.5 Committed Use Discounts

Google offers committed use discounts on Cloud Run:

```
1-year commitment: ~17% discount on CPU/memory
3-year commitment: ~40% discount on CPU/memory
```

The baseline that runs 24/7 (off-hours min-instances: 5 Trading + 2 Auth + 3 Market Data + 2 Social + 1 Ad = 13 containers) is a good candidate for a 1-year CUD.

**Savings:** ~$250-400/month on the always-on baseline.

### 5.6 Move Leaderboard Worker to FIX Gateway VM

The Leaderboard Service currently runs as a separate always-on Cloud Run service subscribed to NATS. It can run as a process on the FIX Gateway VM instead, eliminating one always-on Cloud Run service.

**Architecture:**

```
FIX Gateway VM (e2-standard-4, 4 vCPU, 16GB RAM, already running 24/7)
  │
  ├── FIX Adapter processes (existing)
  │     IOI Adapter, MD Adapter, OE Adapter, DC Adapter
  │
  └── Leaderboard Worker (new process, same VM)
        │
        │ Subscribes to NATS topics:
        │   order.*.* (all fill events)
        │   position.* (P&L updates)
        │
        │ On every fill:
        │   1. Parse fill: userId, symbol, qty, price, P&L
        │   2. Update in-memory user state
        │   3. ZADD to Redis sorted set (update rank)
        │   4. If rank changed significantly → publish to
        │      NATS leaderboard.updates channel
        │
        └──▶ Redis Memorystore (12 sorted sets: 3 verticals × 4 timeframes)
```

**Memory impact:**

```
Per-user in-memory state:
  userId (UUID):      36 bytes
  dailyPnL:            8 bytes (float64)
  weeklyPnL:           8 bytes (float64)
  monthlyPnL:          8 bytes (float64)
  seasonPnL:           8 bytes (float64)
  dailyDrawdown:       8 bytes (float64, for comeback trader vertical)
  riskAdjusted:        8 bytes (float64, for risk-adjusted return)
  Total per user:     ~84 bytes

1M users: 84 bytes × 1,000,000 = ~84 MB
With overhead (hash map, Go runtime): ~150-200 MB

FIX Gateway current usage:    ~750 MB - 1.25 GB
After adding leaderboard:     ~1.0 - 1.5 GB
Available on 16GB VM:         ~14.5 GB free
```

**CPU impact:**

```
Per fill event:
  Parse NATS message:      ~0.01ms
  Update in-memory state:  ~0.01ms
  Redis ZADD:              ~0.5ms (network I/O)
  Total:                   ~0.5ms per fill

Peak: 10,000 fills/second (Super Bowl)
CPU time: 10,000 × 0.5ms = 5 CPU-seconds/sec
Actual CPU burn: ~50ms/sec = ~1.25% of one core (95% is I/O wait on Redis)
```

**Process isolation (Option A -- cgroup limits):**

The leaderboard worker runs as a separate process with Linux cgroup resource limits. If it crashes or leaks memory, the FIX Gateway is unaffected.

```
# systemd service with resource limits
# /etc/systemd/system/leaderboard-worker.service

[Service]
ExecStart=/opt/inplay/leaderboard-worker
Restart=always
RestartSec=2

# cgroup resource limits
MemoryMax=2G
CPUQuota=100%

# process isolation
ProtectSystem=strict
PrivateTmp=true
```

- `MemoryMax=2G` -- if the worker exceeds 2GB (10x expected usage), systemd kills and restarts it. FIX Gateway processes are in a separate cgroup, unaffected
- `CPUQuota=100%` -- worker can use at most 1 full core of the 4 available. FIX adapters keep the other 3
- `Restart=always` -- if the worker crashes, systemd restarts it within 2 seconds. Leaderboard updates pause briefly, then resume. No data loss because NATS JetStream replays missed messages on reconnect

**Savings:** ~$200-300/month (eliminates one always-on Cloud Run service).

### Cost Optimisation Summary

| Optimisation | Estimated saving | Effort |
|-------------|-----------------|--------|
| Split CPU allocation (request-based for Auth/Social/Ad) | 15-20% total | Low -- config change |
| Right-size CPU/memory | 10-20% total | Low -- config change, verify with profiling |
| Tighter scale-down windows | ~$2-3.5K/season | Low -- adjust Cloud Scheduler |
| Higher concurrency (250 → 500) | 20-40% fewer containers | Medium -- requires load testing |
| 1-year CUD on baseline | ~$250-400/month | Low -- purchase commitment |
| Move Leaderboard to FIX Gateway VM | ~$200-300/month | Medium -- code change + systemd config |

### Optimised Cost Estimates

```
Off-season:  ~$1,800-2,500/month  (down from $2,500-3,000)
In-season:   ~$4,500-9,000/month  (down from $8,000-15,000)
```

---

## 6. What Doesn't Scale (And Doesn't Need To)

| Component | Why it doesn't scale with users |
|-----------|-------------------------------|
| FIX Gateway | Market data is per-symbol, not per-user. 500 symbols × 50 updates/sec = 25,000 msgs/sec regardless of 10K or 5M users. Fan-out is Centrifugo's job. Leaderboard worker adds ~200MB RAM and ~1.25% CPU -- negligible |
| NATS JetStream | 3-node cluster handles the message volume. Bottleneck is tZERO's acceptance rate, not NATS throughput |
| Cloud SQL | Read-heavy workload is cached in Redis. Writes are order insertions (~10K/sec peak) which PostgreSQL handles easily |
| Redis Memorystore | Leaderboard sorted sets + cache. Memory-bound, not CPU-bound. Resize tier only if memory fills |
