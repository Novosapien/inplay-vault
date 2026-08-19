---
description: "Leaderboard Service spec — event-driven P&L recalculation from NATS price/fill events into Redis sorted sets, plus the open Python vs Bun runtime question"
---

# Leaderboard Service

> **Architecture:** [[architecture]]
> **Service Overview:** [[services-overview]]
> **Status:** Draft

## Overview

The Leaderboard Service has two responsibilities: real-time P&L recalculation (event-driven via NATS) and serving leaderboard queries (REST API). It subscribes to price changes and fill events, incrementally updates Redis sorted sets, and serves the ranked results to users.

- **Path:** `/leaderboard/*`
- **Platform:** Cloud Run
- **Game day min-instances:** 2 (always-on, must maintain NATS subscriptions)

## Responsibilities

**Event-driven (NATS subscriber):**
- Subscribes to `market.quote.>` (all price changes from FIX Gateway)
- Subscribes to `order.>` (all fills from FIX Gateway)
- Maintains position cache in Redis (indexed by symbol for fast lookup)
- On price change: recalculates P&L for all holders of that symbol
- On fill: updates position cache, recalculates that user's P&L
- Writes to Redis sorted sets incrementally (ZADD per affected user)
- Publishes top movers to NATS → Centrifugo (`leaderboard.{vertical}.{timeframe}`)

**REST API (user queries):**
- Serves leaderboard rankings from pre-computed Redis sorted sets
- Calculates proximity indicators ("you are 112 places from cashing")

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/leaderboard/{vertical}/{timeframe}` | Get ranked leaderboard. Vertical: `pnl`, `risk`, `comeback`. Timeframe: `daily`, `weekly`, `monthly`, `season`. |
| GET | `/leaderboard/me` | User's ranking across all verticals and timeframes |
| GET | `/leaderboard/proximity` | "You are 112 places from cashing" across all verticals |

## Three Competition Verticals

| Vertical | Metric | Redis Key Pattern |
|----------|--------|-------------------|
| **Best P&L** | Total profit/loss for the period | `leaderboard:pnl:{timeframe}` |
| **Best risk-adjusted return** | P&L divided by volatility (Sharpe-like ratio) | `leaderboard:risk:{timeframe}` |
| **Comeback trader** | Biggest recovery from deepest drawdown | `leaderboard:comeback:{timeframe}` |

Four timeframes (daily, weekly, monthly, season) × 3 verticals = 12 sorted sets in Redis.

## Per-User State in Redis

```
HASH user:pnl:{userId}
  current_pnl:       14230.00
  high_water_mark:   15100.00    ← for comeback calculation
  low_water_mark:    -2300.00    ← deepest drawdown
  pnl_snapshots:     [list]      ← for risk-adjusted calculation

SET positions:{symbol}
  → set of userIds holding that symbol (for fast lookup on price change)

HASH positions:{userId}:{symbol}
  qty:     100
  avgPrice: 25.00
```

## Why Event-Driven, Not Batch Polling

At 1M users, querying all positions from PostgreSQL every 5 seconds is expensive (5M+ rows). The event-driven approach only recalculates users affected by each price change. If Cowboys price changes and 50K users hold Cowboys, only those 50K scores are updated -- not all 1M.

PostgreSQL is only read at:
- Service startup (load all positions into Redis cache)
- End of day (reconciliation, snapshot for historical records)

## Open Question: Python/FastAPI vs Bun/TypeScript

The Leaderboard Service is the most CPU-intensive service in the architecture. On every price change, it recalculates P&L for all holders of that symbol and updates Redis sorted sets. During active trading, this could be thousands of recalculations per second.

| | Python / FastAPI | Bun / TypeScript |
|---|---|---|
| **CPU performance** | Slower for computation (GIL, interpreted) | Significantly faster for CPU-bound work (V8 JIT compilation) |
| **NATS client** | `nats-py` (mature, async) | `nats.js` (mature, native async) |
| **Redis client** | `redis-py` (mature) | `ioredis` (mature) |
| **Consistency** | Same language as all other services. Shared package works out of the box. | Different language. Shared models/types need TypeScript equivalents. |
| **TypeScript synergy** | None | Shares language with React Native frontend. Types could be shared. |
| **Risk** | Known quantity, just might be slow under peak load | New runtime in the stack, but the team knows TypeScript |

**Recommendation:** Start with Python/FastAPI for consistency. If load testing shows the Leaderboard Service is CPU-bottlenecked during peak game moments, rewrite in Bun. The service is small and self-contained -- a rewrite would take days, not weeks. Profile before optimising.
