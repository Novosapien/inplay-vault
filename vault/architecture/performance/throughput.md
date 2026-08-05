---
description: "Throughput estimates for the market-data pipeline — ~25K msg/sec upstream from tZERO, the fan-out arithmetic, and the conflation strategies that contain it"
---

# Throughput Estimates

> **Architecture:** [[architecture]]
> **Source:** T0 Integration Spec
> **Status:** Draft

## Upstream from tZERO

| Metric | Estimate | Rationale |
|--------|----------|-----------|
| Symbols watched per user (avg) | 10 | Watchlist + detail view |
| Unique symbols across all users | ~500 | tZERO symbol universe |
| Market updates per symbol per second (peak) | 50 | Active trading **(estimated -- confirm with tZERO)** |
| Total upstream messages/sec from tZERO | 25,000 | 500 symbols × 50 updates |
| Fan-out messages/sec to all users (before conflation) | 500M | 25K × average fan-out ratio |
| WebSocket messages/sec per user (peak) | 500 | 10 symbols × 50 updates |

> **Note:** The 25,000 msg/sec estimate is derived from assumed values, not tZERO-published numbers. Confirm during onboarding: peak aggregate rate, peak per-symbol rate, and whether rate varies between game days and off-days.

## Optimization Strategies

| Strategy | Impact | Applicable To |
|----------|--------|--------------|
| **Conflation/Throttling** | Merge rapid updates to max 10/sec per symbol to client | Quotes, book depth |
| **Delta compression** | Only send changed fields, not full snapshots | All market data |
| **Last-value cache** | New subscribers get current state immediately | All topics |
| **Topic partitioning** | Partition by symbol hash for horizontal scaling | Message bus |
| **Binary encoding** | Protobuf/FlatBuffers instead of JSON on WebSocket | Client delivery (post-launch optimisation) |
| **Top-of-Book default** | MarketDepth=1 unless user opens full depth | Per-symbol subscriptions |
| **Lazy symbol subscription** | Only subscribe FIX v8 detail when user opens symbol view | FIX v8 per-symbol requests |
