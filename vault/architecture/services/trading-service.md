# Trading Service

> **Architecture:** [[architecture]]
> **Service Overview:** [[services-overview]]
> **Status:** Draft

## Overview

The Trading Service is the hot path for order execution. It is deployed as its own Cloud Run service, separate from all other APIs, so that nothing else competes for its resources during high-volume trading moments.

- **Path:** `/trading/*`
- **Platform:** Cloud Run
- **Game day min-instances:** 50
- **Request latency target:** <10ms per request

## Responsibilities

- Order validation (auth, limits, format, ClOrdID rules)
- Wallet balance checks (reads from Redis cache)
- Publishes validated orders to Redis queue for FIX Gateway consumption
- Returns immediate acknowledgment to user ("order received")
- Wallet management (trading wallet 100K cap, referral wallet reload logic below 25K trigger)
- Position management and P&L calculation
- Processes fill confirmations from FIX Gateway via Redis pub/sub

## Request Flow

```
User taps "Buy 100 shares Cowboys @ $25"
  │
  ▼
API Gateway → /trading/orders → Trading Service
  │
  ▼
┌──────────────────────────────────────────────────────────┐
│  TRADING SERVICE                                          │
│                                                          │
│  1. Auth Middleware                                       │
│     Validate JWT (passed from gateway)                    │
│     Extract userId                                        │
│                                                          │
│  2. Order Validator                                       │
│     - Symbol exists                                       │
│     - Side valid (buy/sell)                                │
│     - Quantity > 0                                         │
│     - Price > 0                                            │
│     - ClOrdID format: max 20 chars, no leading zeroes     │
│     - OrdType = 2 (Limit, required by tZERO)              │
│     - ExDestination = STX                                  │
│                                                          │
│  3. Wallet Check                                          │
│     - Read balance from Redis cache                       │
│     - Verify sufficient funds for order value              │
│     - Check 100K trading wallet cap not exceeded           │
│                                                          │
│  4. Order Publisher                                       │
│     - Generate ClOrdID (max 20 chars, no leading zeroes)  │
│     - Publish to Redis order queue                        │
│     - FIX Gateway consumes from this queue                │
│                                                          │
│  5. Response                                              │
│     - Return immediate ack to client                      │
│     - {status: "acknowledged", clOrdId: "...", ...}       │
│     - User does NOT wait for tZERO to process             │
│                                                          │
│  Background: Fill Processor                               │
│     - Subscribes to order.{userId}.* on Redis             │
│     - On fill: update PostgreSQL (positions, wallet, P&L) │
│     - On reject: update order status                      │
│     - On bust: recalculate position and P&L               │
└──────────────────────────────────────────────────────────┘
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/trading/orders` | Place a new order (buy/sell) |
| DELETE | `/trading/orders/{clOrdId}` | Cancel an order |
| PUT | `/trading/orders/{clOrdId}` | Replace an order (cancel/replace) |
| GET | `/trading/orders` | List user's orders (open + recent) |
| GET | `/trading/orders/{clOrdId}` | Get single order status |
| GET | `/trading/positions` | Get user's current positions |
| GET | `/trading/pnl` | Get user's P&L (daily/weekly/monthly) |
| GET | `/trading/wallet` | Get trading wallet + referral wallet balances |

## Wallet Rules

- Trading wallet starts at 100,000 InPlay dollars on signup
- Trading wallet can never exceed 100,000
- When trading wallet drops below 25,000, user can reload from referral wallet back to 100,000
- Referral wallet has no cap but resets to zero at end of season
- Referral wallet cannot be used for trading directly -- only to reload trading wallet

## Why Separate From Main API

At peak (NFL touchdown moment), the Trading Service may handle 125,000+ orders/second. If this shared resources with KYC processing, leaderboard queries, or ad serving, those non-critical workloads could starve the order execution path. Separate deployment means separate CPU, memory, and scaling.

## Cold Start Mitigation

Each request takes ~10ms. With Cloud Run concurrency of 250 per container and min-instances=50:
- Baseline capacity: 50 × 250 = 12,500 concurrent requests
- Throughput: ~1,250,000 orders/second
- Peak spike estimate: ~125,000 orders/second (well within capacity)

Game-day min-instances are pre-warmed via Cloud Scheduler before kickoff. Scaled down overnight.
