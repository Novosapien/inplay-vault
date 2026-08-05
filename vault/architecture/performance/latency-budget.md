---
description: "Hop-by-hop latency budget for market data, tZERO to user screen — <56ms typical, <100ms p99, with per-data-type delivery targets"
---

# Latency Budget

> **Architecture:** [[architecture]]
> **Source:** T0 Integration Spec
> **Status:** Draft

## End-to-End Target: <100ms from tZERO to User Screen

| Hop | Component | Target Latency | Notes |
|-----|-----------|----------------|-------|
| 1 | tZERO → FIX Gateway (network) | <1ms | Co-located or low-latency link |
| 2 | FIX Gateway parse + normalize | <2ms | Binary FIX parsing, no disk I/O |
| 3 | Gateway → Redis publish | <2ms | In-memory pub/sub |
| 4 | Redis → Centrifugo (internal) | <5ms | Same datacenter |
| 5 | Centrifugo → Client (network) | <30ms | Geographic dependent |
| 6 | Client render | <16ms | Single frame at 60fps |
| **Total** | | **<56ms typical** | Buffer to 100ms for p99 |

## Per-Data-Type Targets

| Data Type | Bus Publish Target | User Delivery Target |
|-----------|-------------------|---------------------|
| Best Bid/Offer (BBO) | <5ms from receipt | <50ms to screen |
| Trades | <5ms from receipt | <50ms to screen |
| OHLC Bar | <10ms from receipt | <100ms to screen |
| Order Book Depth | <10ms from receipt | <100ms to screen |
| Order Status | <5ms from receipt | <50ms to screen |
| Security Status (halt/resume) | <5ms from receipt | <50ms to screen |
| Trading Session Status | <10ms from receipt | <200ms to screen |
| Position/P&L | <5ms from receipt | <50ms to screen |
