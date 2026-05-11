# FIX Gateway

> **Architecture:** [[architecture]]
> **Service Overview:** [[services-overview]]
> **T0 Integration Spec:** [[t0]]
> **Status:** Draft

## Overview

Maintains persistent FIX 4.2 sessions to tZERO. Parses raw FIX messages, normalises them into JSON envelopes, and publishes to Redis channels. Consumes order requests from a Redis queue and sends them to tZERO via FIX.

- **Platform:** Compute Engine VM (co-located with tZERO for <1ms latency)
- **Language:** Python / QuickFIX
- **HA:** Active/standby VM configuration

## Why Compute Engine (Not Cloud Run)

FIX 4.2 requires persistent TCP sessions with heartbeats, sequence numbers, and session state. Cloud Run recycles containers during scale-down and deployments, killing FIX sessions. A dropped session means:
- Orders in flight could be lost
- Full state replay required on reconnect (IOI/MD)
- Sequence number gaps requiring resend requests
- 5-10 second recovery time during which no trading occurs

## 4 FIX Sessions

| Session | Protocol | Purpose | Recovery on Disconnect |
|---------|----------|---------|----------------------|
| IOI v1.2 | FIX 4.2 | Order book indications of interest. Builds full book picture. | Full state replay from scratch |
| FIX Market Data v8 | FIX 4.2 | Quotes (BBO), trades, OHLC, security status, session status. ResetSeqNumFlag=Y required on every logon. | Re-subscribe to everything. No session recovery. |
| Order Entry v2.2 | FIX 4.2 | Order submission, execution reports, cancels, replaces, position/P&L. | Standard FIX gap detection and resend |
| Drop Copy | FIX 4.2 | Read-only execution report stream for independent fill reconciliation. | Standard FIX recovery |

> **FIX version discrepancy:** PDF specifications say FIX 4.2. Online API docs at apidocs.tzero.com reference FIX 4.4. Must confirm with tZERO before implementation.

## Internal Architecture

```
┌──────────────────────────────────────────────────────────┐
│  FIX GATEWAY (Python/QuickFIX, Compute Engine VM)        │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │  SESSION MANAGER                                  │    │
│  │  Manages logon, heartbeats, sequence numbers      │    │
│  │  Stores seq nums in Redis for failover            │    │
│  │  Handles disconnect/reconnect per T0 spec DFAs    │    │
│  └──────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────┐ ┌────────────────┐ ┌──────────────┐  │
│  │ IOI ADAPTER    │ │ MD ADAPTER     │ │ OE ADAPTER   │  │
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
│  ┌──────────────────┐                                    │
│  │ DC ADAPTER       │  Drop Copy (read-only)             │
│  │ Receives ExecRpts│  Independent fill reconciliation   │
│  │ for audit trail  │                                    │
│  └──────────────────┘                                    │
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
│  │  ExecID / IOIid / MDEntryID dedup                 │    │
│  └──────────────────────────────────────────────────┘    │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │  ORDER QUEUE CONSUMER                             │    │
│  │  Reads validated orders from Redis queue           │    │
│  │  Converts to FIX NewOrderSingle (MsgType=D)       │    │
│  │  Sends via OE Adapter                             │    │
│  └──────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

## High Availability

- Active/standby VM configuration
- FIX session state (sequence numbers) stored in Redis
- Orders queued in Redis -- survive gateway restart
- Standby monitors primary health, establishes new FIX sessions on failure (~5-10 second failover)
- On IOI/MD reconnection: full state replay from tZERO (no incremental recovery)
- On Order Entry reconnection: standard FIX gap detection and resend

## Why It Doesn't Scale With Users

Market data from tZERO is per-symbol, not per-user: 500 symbols × 50 updates/sec = 25,000 msgs/sec regardless of user count. The fan-out to users is Centrifugo's job.

Orders scale with users but the architecture absorbs spikes at the Cloud Run Trading Service layer. The FIX Gateway drains the Redis order queue at whatever rate tZERO accepts. It's a message pump, not a scaling bottleneck.

## State Machines

All state machines (DFAs) are fully specified in the [[t0]] integration document:
- IOI Feed Session DFA (Section 3.1)
- FIX Market Data Session DFA (Section 3.2)
- Per-Symbol Subscription DFA (Section 3.3)
- IOI Order Book Entry DFA (Section 3.4)
- FIX Incremental Refresh Entry DFA (Section 3.5)
- Order Lifecycle DFA (Section 3.6)
- Execution Lifecycle DFA (Section 3.7)
- Cancel/Replace Request DFA (Section 3.8)
- Trading Session DFA (Section 3.9)
- Security Trading Status DFA (Section 3.10)
