# Service Architecture Overview

> **Architecture:** [[architecture]]
> **Status:** Draft

## Service Map

5 Cloud Run API services + FIX Gateway (Compute Engine) + Centrifugo (Managed Instance Group).

Services do NOT call each other. They share PostgreSQL, Redis, and NATS JetStream.

```
React Native App
  │
  │  All requests to api.inplay.com
  │
  ▼
API Gateway (path-based routing)
  │
  ├── /auth/*     → Auth Service ──────────┐
  ├── /trading/*  → Trading Service ───────┤
  ├── /market/*   → Market Data Service ───┤──── all read/write ───► PostgreSQL
  ├── /social/*   → Social Service ────────┤                         Redis
  └── /ads/*      → Ad Service ────────────┘                         NATS JetStream
                                           │
                   shared/ code is INSIDE   │
                   each container:          │
                   • tzero_client.py ───────┼──► tZERO REST API
                   • sportradar_client.py ──┼──► Sport Radar
                   • persona_client.py ─────┼──► Persona KYC
                   • jwt.py                 │
                   • redis_client.py        │
                   • nats_client.py         │
```

## Cloud Run Services

| Service | Path | Purpose | Game Day Min-Instances |
|---------|------|---------|----------------------|
| **Trading Service** | `/trading/*` | Order execution, wallet management, positions, P&L | 50 |
| **Auth Service** | `/auth/*` | Signup, login, JWT issuance, KYC (Persona) | 10 |
| **Market Data Service** | `/market/*` | Teams, games, news, stats, Sport Radar data | 20 |
| **Social Service** | `/social/*` | Referrals, leaderboards, notifications | 10 |
| **Ad Service** | `/ads/*` | Campaign delivery, impression tracking, targeting | 10 |

## Non-Cloud-Run Services

| Service | Platform | Purpose |
|---------|----------|---------|
| **FIX Gateway** | Compute Engine VM (co-located with tZERO) | 4 FIX 4.2 sessions to tZERO |
| **FIX Gateway Standby** | Compute Engine VM | Failover for FIX Gateway |
| **Centrifugo** | Managed Instance Group (3-25 VMs) | 1M-5M WebSocket connections, real-time fan-out |

## Cloud Run Jobs

| Job | Schedule | Purpose |
|-----|----------|---------|
| Leaderboard Recalc | Every 5-15 seconds (Cloud Scheduler) | Calculate P&L, risk-adjusted, and comeback rankings |
| End-of-Day Settlement | Daily after market close | Expire orders, snapshot P&L, calculate prizes |
| Referral Processor | Triggered on KYC completion | Credit referrer (1,000) and referee (500) InPlay dollars |

## Monorepo Structure

All services live in a single repository with a shared package:

```
inplay-backend/
├── shared/                        ← shared code, copied into every container
│   ├── auth/
│   │   └── jwt_middleware.py      ← JWT validation, used by all services
│   ├── integrations/
│   │   ├── tzero_client.py        ← tZERO REST API wrapper
│   │   ├── sportradar_client.py   ← Sport Radar API wrapper
│   │   ├── persona_client.py      ← Persona KYC API wrapper
│   │   └── redis_client.py        ← Redis connection + helpers
│   ├── models/
│   │   ├── user.py                ← SQLAlchemy models, shared across services
│   │   ├── order.py
│   │   ├── wallet.py
│   │   └── referral.py
│   └── config/
│       └── settings.py            ← Pydantic settings, env var pattern
│
├── services/
│   ├── trading/
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   └── routers/
│   ├── auth/
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   └── routers/
│   ├── market-data/
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   └── routers/
│   ├── social/
│   │   ├── Dockerfile
│   │   ├── main.py
│   │   └── routers/
│   └── ads/
│       ├── Dockerfile
│       ├── main.py
│       └── routers/
│
├── gateway/                       ← FIX Gateway (Compute Engine)
│   ├── Dockerfile
│   ├── main.py
│   └── adapters/
│
└── shared-docker/
    └── Dockerfile.base            ← shared base image
```

### How the Shared Package Works

The shared package is not a deployed service -- it's a folder of Python files that gets copied into every service's Docker container at build time.

```dockerfile
# services/trading/Dockerfile (same pattern for all services)
FROM python:3.12-slim
COPY shared/ /app/shared/
COPY services/trading/ /app/service/
RUN pip install -r /app/service/requirements.txt
CMD ["uvicorn", "service.main:app", "--host", "0.0.0.0"]
```

Each service imports from shared:
```python
from shared.auth.jwt_middleware import verify_jwt
from shared.integrations.tzero_client import TZeroClient
from shared.models.user import User
```

### Why Services Don't Call Each Other

Services share data through PostgreSQL, Redis, and NATS JetStream -- not through HTTP calls to each other. This avoids:
- Cascading failures (Service A down → Service B down)
- Latency compounding (each network hop adds 1-5ms)
- Distributed debugging complexity
- Circular dependency risks

If the Trading Service creates an order, the Market Data Service can read it from the same database. No inter-service HTTP needed.
