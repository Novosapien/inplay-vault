---
description: "Async order-placement flow from user tap through NATS and the FIX Gateway to tZERO fill, with spike handling for ~250K orders and the cancel/replace path"
---

# Data Flow: Order Placement (User to tZERO)

> **Architecture:** [[architecture]]
> **Status:** Draft

## Flow

Order submission and execution are asynchronous. The user gets an immediate ack, then a fill confirmation via WebSocket moments later.

```
User taps "Buy 100 shares Cowboys @ $25"
  │
  │  HTTPS POST
  ▼
API Gateway → /trading/orders → Trading Service (Cloud Run)
  │
  │  ~10ms total:
  │  1. Validate JWT
  │  2. Validate order (symbol, side, qty, price, ClOrdID format)
  │  3. Check wallet balance (Redis cache)
  │  4. Publish to NATS JetStream (orders.new subject)
  │  5. Return "order acknowledged" to user
  ▼
User sees "Order Pending" in app (immediate, <50ms from tap)
  │
  │  Meanwhile, asynchronously:
  ▼
FIX Gateway reads order from NATS (subscribes to orders.new.>)
  │
  │  Converts to FIX NewOrderSingle (MsgType=D)
  ▼
Sends to tZERO via Order Entry FIX session
  │
  │  tZERO processes and matches
  ▼
tZERO sends ExecutionReport (MsgType=8) back via FIX
  │
  │  ExecType=0 (Accepted), then ExecType=1/2 (Partial/Full Fill)
  ▼
FIX Gateway publishes to NATS: order.{userId}.{clOrdId}
  │
  ▼
Centrifugo delivers fill confirmation to user via WebSocket
  │
  ▼
User sees "Order Filled: 100 shares Cowboys @ $25.00"
  │
  │  Meanwhile:
  ▼
Trading Service processes fill event:
  → Updates positions in PostgreSQL
  → Updates wallet balance in PostgreSQL + Redis cache
  → Updates P&L
```

## Spike Handling

At peak (5M users, touchdown moment), ~250,000 orders may arrive in 2 seconds:

```
250,000 orders hit Trading Service
  → Cloud Run auto-scales (50+ warm instances absorb the load)
  → Each request: validate + publish to NATS = ~10ms
  → NATS JetStream holds all validated orders (persistent)

FIX Gateway drains NATS subject at tZERO's acceptance rate
  → tZERO is the throughput bottleneck, not our infrastructure
  → If tZERO processes 10K orders/sec, queue drains in ~25 seconds
  → Users experience this as latency between "acknowledged" and "filled"
```

## Cancel/Replace Flow

```
User taps "Cancel" on order ORD123
  → POST /trading/orders/ORD123 (cancel)
  → Trading Service publishes cancel request to NATS
  → FIX Gateway sends OrderCancelRequest (MsgType=F) to tZERO
  → tZERO responds: Cancelled (ExecType=4) or CancelRejected (MsgType=9)
  → FIX Gateway publishes result to NATS
  → Centrifugo delivers to user: "Order cancelled" or "Cancel rejected: too late"
```
