# Data Flow: Price Update (tZERO to User Screen)

> **Architecture:** [[architecture]]
> **Status:** Draft

## Target: <100ms end-to-end, <56ms typical

```
tZERO sends FIX message (e.g., trade: Cowboys 200 shares at $25.60)
  │
  │  Hop 1: <1ms (co-located)
  ▼
FIX Gateway parses FIX message, normalizes to JSON envelope
  │
  │  Hop 2: <2ms (binary FIX parsing, no disk I/O)
  ▼
Publishes to Redis channel: market.trade.cowboys
  │
  │  Hop 3: <2ms (in-memory pub/sub)
  ▼
Centrifugo picks up from Redis
  │
  │  Hop 4: <5ms (same datacenter)
  ▼
Delivers to all clients subscribed to market.trade.cowboys via WebSocket
  │
  │  Hop 5: <30ms (geographic, CDN/edge dependent)
  ▼
Client renders new price on screen
  │
  │  Hop 6: <16ms (single frame at 60fps)
  ▼
User sees updated price

Total: <56ms typical, <100ms p99
```

## Latency Budget

| Hop | Component | Target Latency | Notes |
|-----|-----------|----------------|-------|
| 1 | tZERO → FIX Gateway (network) | <1ms | Co-located or low-latency link |
| 2 | FIX Gateway parse + normalize | <2ms | Binary FIX parsing, no disk I/O |
| 3 | Gateway → Redis publish | <2ms | In-memory pub/sub |
| 4 | Redis → Centrifugo → Client (network) | <5ms + <30ms | Same datacenter + geographic |
| 5 | Client render | <16ms | Single frame at 60fps |
| **Total** | | **<56ms typical** | Buffer to 100ms for p99 |
