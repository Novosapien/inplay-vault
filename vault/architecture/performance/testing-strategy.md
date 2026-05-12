# Testing Strategy

> **Architecture:** [[architecture]]
> **Status:** Draft
> **Date:** 2026-05-12

---

## 1. Overview

All tests -- unit, integration, load, stress, spike, soak, security -- are orchestrated from GitHub Actions and report to Grafana Cloud. One trigger, one dashboard, no switching between tools.

```
GitHub Actions (orchestrator)
  │
  ├── Unit Tests ──────────── pytest (backend) + Vitest (frontend)
  ├── Integration Tests ───── pytest (real DB, Redis, NATS in test env)
  ├── API / Contract Tests ── k6 (validate endpoint schemas + responses)
  ├── Load Tests ──────────── k6 (sustained traffic simulation)
  ├── Stress Tests ────────── k6 (push beyond capacity, find breaking point)
  ├── Spike Tests ─────────── k6 (simulate touchdown burst)
  ├── Soak Tests ──────────── k6 (8-hour endurance run)
  ├── WebSocket Tests ─────── k6 (100K+ connections to Centrifugo)
  ├── FIX Protocol Tests ──── Custom Go harness (FIX 4.2 order flow)
  ├── Security Tests ──────── OWASP ZAP (scan for OWASP Top 10)
  │
  └── Results
      ├── GitHub Actions Summary (unit + integration pass/fail)
      └── Grafana Cloud (k6 metrics + service observability, one dashboard)
```

---

## 2. Test Tools

| Tool | Language | What it tests | Why this tool |
|------|----------|--------------|---------------|
| **pytest** | Python | Unit + integration tests for all backend services | Backend is Python. pytest is the standard. Fixtures for DB/Redis/NATS test setup |
| **Vitest** | TypeScript | Unit + component tests for React Native frontend | Frontend is TypeScript/React Native. Vitest is fastest for Vite-based projects |
| **Grafana k6** | JavaScript (Go runtime) | Load, stress, spike, soak, API, WebSocket tests | Handles HTTP + WebSocket natively. Grafana Cloud runs up to 1M VUs from 21 global regions. Scripts in JavaScript, runs in Go (100x more efficient than JMeter) |
| **Custom Go harness** | Go | FIX 4.2 protocol load testing | k6 doesn't support FIX natively. Go has mature FIX libraries (QuickFIX/Go). Results publish to same Grafana dashboard |
| **OWASP ZAP** | Java | Security scanning (XSS, injection, misconfig) | Industry standard, free, integrates with GitHub Actions |

---

## 3. Test Layers

### 3.1 Unit Tests (pytest + Vitest)

Run on every PR. Fast feedback. No external dependencies -- everything mocked.

```
Backend (pytest):
  services/trading/tests/
    test_order_validation.py      ← validate qty, price, symbol format
    test_wallet_balance_check.py  ← can user afford this trade
    test_pnl_calculation.py       ← daily/weekly/monthly P&L math
    test_referral_credit.py       ← 1,000 referrer / 500 referee logic
    test_leaderboard_scoring.py   ← risk-adjusted return, comeback calc

  shared/tests/
    test_jwt_middleware.py        ← token validation, expiry, refresh
    test_tzero_client.py          ← tZERO REST API wrapper (mocked responses)
    test_fix_message_parser.py    ← parse execution reports, order acks

Frontend (Vitest):
  app/tests/
    TradeModal.test.tsx           ← buy/sell modal renders correctly
    OrderBook.test.tsx            ← bid/ask display, depth sorting
    PriceChart.test.tsx           ← candlestick rendering, annotation overlay
    Leaderboard.test.tsx          ← rank display, proximity alert
    WebSocketProvider.test.tsx    ← reconnection logic, message handling
```

**When:** Every PR, every push to main.
**Target:** <60 seconds total. Fail the PR if any test fails.

### 3.2 Integration Tests (pytest)

Run against real PostgreSQL, Redis, and NATS in a test environment. No mocks for infrastructure -- mocks only for external APIs (tZERO, Sport Radar, Persona).

```
tests/integration/
  test_order_lifecycle.py
    ← Submit order via Trading Service → verify PostgreSQL row created
    ← Publish fill event to NATS → verify position updated in DB
    ← Verify wallet balance decremented

  test_onboarding_flow.py
    ← Create account → trigger KYC (mocked Persona) → verify 100K credited
    ← Verify referral code generated
    ← Submit referral → verify both wallets credited

  test_market_data_pipeline.py
    ← Publish price update to NATS → verify Redis cache updated
    ← Verify Centrifugo receives message (via test WebSocket client)

  test_leaderboard_update.py
    ← Publish fill event → verify Redis sorted set updated
    ← Verify rank changed → leaderboard.updates channel notified
```

**When:** Every merge to main. Nightly full suite.
**Target:** <5 minutes. Uses Docker Compose for PostgreSQL + Redis + NATS.

### 3.3 API / Contract Tests (k6)

Validate every REST endpoint returns the correct schema, status codes, and error handling.

```javascript
// tests/k6/api-contract.js

import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 10,
  duration: '1m',
};

export default function () {
  // Trading: submit order
  const orderRes = http.post(
    `${BASE_URL}/trading/v1/accounts/${ACCOUNT_ID}/orders`,
    JSON.stringify({
      symbol: 'IGBI',
      side: 'buy',
      quantity: 100,
      price: 3.5500,
      orderType: 'limit',
      timeInForce: 'day',
    }),
    { headers: { Authorization: `Bearer ${TOKEN}`, 'Content-Type': 'application/json' } }
  );

  check(orderRes, {
    'order created': (r) => r.status === 201,
    'has orderId': (r) => JSON.parse(r.body).orderId !== undefined,
    'has status': (r) => JSON.parse(r.body).status === 'accepted',
  });

  // Trading: get orders
  const listRes = http.get(
    `${BASE_URL}/trading/v1/accounts/${ACCOUNT_ID}/orders`,
    { headers: { Authorization: `Bearer ${TOKEN}` } }
  );

  check(listRes, {
    'orders returned': (r) => r.status === 200,
    'is array': (r) => Array.isArray(JSON.parse(r.body)),
  });

  // Market data: snapshot
  const snapRes = http.get(
    `${BASE_URL}/markets/v1/mdt/public-snapshots/IGBI`,
    { headers: { 'x-apikey': API_KEY } }
  );

  check(snapRes, {
    'snapshot returned': (r) => r.status === 200,
    'has bid': (r) => JSON.parse(r.body).bid !== undefined,
    'has ask': (r) => JSON.parse(r.body).ask !== undefined,
  });
}
```

**When:** Every merge to main. Runs against staging environment.
**Target:** 100% of endpoints covered, zero failures.

---

## 4. Performance Tests (k6)

All performance tests run against the staging environment, which mirrors production infrastructure at reduced scale. Results stream to Grafana Cloud for real-time dashboards.

### 4.1 Smoke Test

Quick sanity check. Does the system work at all under minimal load?

```javascript
// tests/k6/smoke.js
export const options = {
  vus: 10,
  duration: '1m',
  thresholds: {
    http_req_duration: ['p(95)<200'],
    http_req_failed: ['rate<0.01'],
  },
};
```

**When:** Every PR (via GitHub Actions).
**Pass criteria:** p95 latency <200ms, error rate <1%.
**Duration:** 1 minute.

### 4.2 Load Test -- Normal Game Day

Simulate a typical Thursday Night Football. Single game, ~200K active users, sustained trading.

```javascript
// tests/k6/load-gameday.js
export const options = {
  stages: [
    { duration: '5m',  target: 500 },   // pre-game: users logging in
    { duration: '5m',  target: 2000 },   // kickoff ramp
    { duration: '30m', target: 2000 },   // sustained game trading
    { duration: '5m',  target: 3000 },   // 4th quarter intensity
    { duration: '10m', target: 1000 },   // post-game review
    { duration: '5m',  target: 0 },      // users leave
  ],
  thresholds: {
    http_req_duration: ['p(95)<100', 'p(99)<300'],
    http_req_failed: ['rate<0.001'],
    ws_connecting: ['p(95)<500'],
  },
};

export default function () {
  // Mix of operations simulating real user behaviour:
  // 40% -- view market data (GET snapshots, price history)
  // 30% -- trade (POST orders, GET order status)
  // 15% -- browse (GET games, teams, leaderboard)
  // 10% -- WebSocket (subscribe to channels, receive updates)
  //  5% -- social (referral checks, notifications)
}
```

**When:** Nightly against staging.
**Pass criteria:** p95 <100ms, p99 <300ms, error rate <0.1%.
**Duration:** ~60 minutes.
**VUs:** 3,000 (each VU simulates ~70 concurrent users via async requests).

### 4.3 Stress Test -- NFL Sunday Peak

Push beyond normal capacity. 3 simultaneous games, 500K-1M active users. Find the ceiling.

```javascript
// tests/k6/stress-sunday.js
export const options = {
  stages: [
    { duration: '5m',  target: 1000 },
    { duration: '5m',  target: 3000 },
    { duration: '5m',  target: 5000 },
    { duration: '10m', target: 5000 },   // sustained peak
    { duration: '5m',  target: 8000 },
    { duration: '10m', target: 8000 },   // beyond expected peak
    { duration: '5m',  target: 10000 },  // breaking point search
    { duration: '10m', target: 10000 },
    { duration: '5m',  target: 0 },      // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200', 'p(99)<500'],
    http_req_failed: ['rate<0.01'],
  },
};
```

**When:** Weekly (Saturday night, off-peak hours).
**Goal:** Find the breaking point. At what VU count does p99 exceed 500ms? At what point do errors appear? Does Cloud Run auto-scale fast enough?
**Duration:** ~60 minutes.
**VUs:** Ramp to 10,000 (simulating ~700K concurrent users).

### 4.4 Spike Test -- Touchdown Burst

The most important test for InPlay. Simulates a touchdown in a close game where 50K+ users hit BUY simultaneously.

```javascript
// tests/k6/spike-touchdown.js
export const options = {
  stages: [
    { duration: '5m',  target: 1000 },   // normal trading
    { duration: '10s', target: 8000 },   // TOUCHDOWN -- instant 8x spike
    { duration: '30s', target: 8000 },   // sustained burst (everyone trading)
    { duration: '1m',  target: 3000 },   // settling back down
    { duration: '5m',  target: 1000 },   // back to normal
    { duration: '10s', target: 8000 },   // SECOND TOUCHDOWN
    { duration: '30s', target: 8000 },
    { duration: '2m',  target: 1000 },
    { duration: '2m',  target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<300'],     // relaxed during spike
    http_req_failed: ['rate<0.05'],       // allow up to 5% errors during spike
    iteration_duration: ['p(99)<2000'],   // full trade flow under 2 seconds
  },
};

export default function () {
  // Simulate the touchdown trade flow:
  // 1. GET market snapshot (what's the current price?)
  // 2. POST order (buy at ask)
  // 3. GET order status (was it filled?)
  // All within 2 seconds
}
```

**When:** Weekly. Also run 48 hours before season launch.
**Goal:** Verify Cloud Run scales from 50 → 80+ containers within 3 seconds. Verify NATS absorbs the order queue. Verify no orders are lost. Verify Centrifugo delivers fill notifications within 200ms.
**Duration:** ~20 minutes.
**Key metrics:**
- Time for Cloud Run to auto-scale (target: <3 seconds)
- Order submission latency during spike (target: p95 <300ms)
- Order loss rate (target: 0%)
- Fill notification delivery latency via WebSocket (target: <200ms)

### 4.5 Soak Test -- Full Game Day Endurance

8-hour run simulating an entire game day. Detects memory leaks, connection drift, Redis connection pool exhaustion, NATS consumer lag, and gradual performance degradation.

```javascript
// tests/k6/soak-gameday.js
export const options = {
  stages: [
    { duration: '30m', target: 2000 },   // morning: users logging in
    { duration: '60m', target: 3000 },   // pre-game: browsing, research
    { duration: '180m', target: 5000 },  // games live: peak trading (3 hours)
    { duration: '60m', target: 3000 },   // late games: still active
    { duration: '60m', target: 1000 },   // post-game: reviewing P&L
    { duration: '30m', target: 200 },    // night: stragglers
    { duration: '10m', target: 0 },      // empty
  ],
  thresholds: {
    http_req_duration: ['p(95)<100'],
    http_req_failed: ['rate<0.001'],
  },
};
```

**When:** Pre-season (run twice: 4 weeks and 1 week before launch). Monthly during season.
**Goal:** Verify the system doesn't degrade over 8 hours. Catch:
- Memory leaks in Cloud Run containers (rising RSS over time)
- PostgreSQL connection pool exhaustion
- Redis memory growth (leaderboard sorted sets)
- NATS consumer lag accumulation
- Centrifugo connection count drift (connections not being cleaned up)
- Cloud Run instance count stability (not endlessly scaling up)
**Duration:** ~8 hours.

---

## 5. WebSocket Tests (k6)

Dedicated tests for the Centrifugo real-time layer.

### 5.1 Connection Scale Test

Open as many WebSocket connections as possible. Find the ceiling per Centrifugo VM.

```javascript
// tests/k6/ws-connections.js
import ws from 'k6/ws';

export const options = {
  stages: [
    { duration: '5m',  target: 10000 },
    { duration: '5m',  target: 50000 },
    { duration: '5m',  target: 100000 },
    { duration: '10m', target: 100000 },  // hold at 100K
    { duration: '5m',  target: 0 },
  ],
};

export default function () {
  const url = 'wss://realtime-staging.inplay.com/connection/websocket';
  const token = getTestJWT();

  ws.connect(url, { headers: { Authorization: `Bearer ${token}` } }, function (socket) {
    socket.on('open', () => {
      // Subscribe to a random team's market data
      const symbol = getRandomSymbol();
      socket.send(JSON.stringify({
        subscribe: { channel: `market:quote:${symbol}` },
      }));
    });

    socket.on('message', (msg) => {
      // Count messages received, measure latency
    });

    socket.setTimeout(() => socket.close(), 600000); // hold for 10 minutes
  });
}
```

**Goal:** Verify 200K connections per VM. Measure memory per connection. Measure message delivery latency at 100K vs 200K connections.

### 5.2 Message Delivery Latency Test

With connections established, measure how fast published messages reach clients.

```javascript
// tests/k6/ws-latency.js
export default function () {
  ws.connect(url, {}, function (socket) {
    socket.on('open', () => {
      socket.send(JSON.stringify({
        subscribe: { channel: 'market:quote:IGBI' },
      }));
    });

    socket.on('message', (msg) => {
      const data = JSON.parse(msg);
      if (data.channel === 'market:quote:IGBI' && data.data.serverTimestamp) {
        const latency = Date.now() - data.data.serverTimestamp;
        // Report latency to k6 metrics
      }
    });
  });
}
```

**Target:** p50 <20ms, p95 <50ms, p99 <100ms at 100K concurrent connections.

### 5.3 Reconnection Recovery Test

Simulate mobile connections dropping and reconnecting. Verify no messages are lost.

**Scenario:**
1. Connect 10K clients, subscribe to channels
2. Each client receives messages for 5 minutes
3. Kill 50% of connections simultaneously (simulating subway/signal loss)
4. Reconnect with last seen sequence number
5. Verify all missed messages are replayed
6. Verify no duplicate messages after recovery

**Target:** 100% message recovery. Zero duplicates. Reconnection <2 seconds.

---

## 6. FIX Protocol Tests (Custom Go Harness)

k6 doesn't support FIX natively. A custom Go test harness using QuickFIX/Go handles FIX-specific testing.

### 6.1 Order Flow Test

```
1. Establish FIX 4.2 session to FIX Gateway (test mode)
2. Send NewOrderSingle (MsgType=D) for symbol IGBI
3. Verify Execution Report received:
   - ExecType=0 (Accepted) within 5ms
4. Simulate fill (test matching engine):
   - ExecType=2 (Filled) with correct LastPx, LastShares
5. Verify Drop Copy session receives matching execution report
6. Verify NATS message published on order.{userId}.{clOrdId}
7. Verify Centrifugo delivers fill notification to test WebSocket client
```

### 6.2 FIX Session Recovery Test

```
1. Establish FIX session, submit 100 orders
2. Kill FIX Gateway process
3. Restart FIX Gateway
4. Verify sequence number recovery
5. Verify all pending orders still tracked
6. Verify NATS JetStream replayed missed messages
```

### 6.3 FIX Throughput Test

```
1. Send orders at increasing rate: 100/sec → 500/sec → 1,000/sec → 5,000/sec → 10,000/sec
2. Measure acceptance rate vs rejection rate
3. Measure execution report latency at each rate
4. Find the point where tZERO throttles or rejects
```

**Results publish to Grafana Cloud** via Prometheus push gateway -- same dashboard as k6 tests.

---

## 7. Security Tests (OWASP ZAP)

Automated security scan against staging environment.

| Check | What it finds |
|-------|--------------|
| SQL injection | Malformed input in order qty, price, symbol, search |
| XSS | Script injection in referral codes, team names, chat messages |
| Auth bypass | Accessing endpoints without JWT, with expired JWT, with forged JWT |
| Rate limit bypass | Exceeding order submission rate limits |
| IDOR | Accessing another user's orders, positions, wallet via ID manipulation |
| Sensitive data exposure | PII in error messages, stack traces in responses |

**When:** Weekly. Also on every release candidate.

---

## 8. Game Day Test Calendar

### Pre-Season (4 weeks before launch)

| Week | Test | Purpose |
|------|------|---------|
| Week 1 | Smoke + API contract | Baseline -- does everything work? |
| Week 1 | Load test (Thursday profile) | Validate single-game performance |
| Week 2 | Stress test (Sunday profile) | Find breaking point at 3-game load |
| Week 2 | Spike test (touchdown) | Validate Cloud Run auto-scale speed |
| Week 2 | WebSocket connection scale | Verify 200K per Centrifugo VM |
| Week 3 | Soak test (8 hours) | Find memory leaks, connection drift |
| Week 3 | FIX throughput test | Find tZERO acceptance rate ceiling |
| Week 3 | Security scan | OWASP ZAP full scan |
| Week 4 | Full dress rehearsal | All tests, production-like data, game-day scaling schedule active |

### In-Season (continuous)

| Frequency | Test | Trigger |
|-----------|------|---------|
| Every PR | Unit tests (pytest + Vitest) + smoke test (k6) | GitHub Actions on PR |
| Every merge to main | Integration tests + API contract tests | GitHub Actions on merge |
| Nightly | Load test (Thursday profile) | GitHub Actions scheduled |
| Weekly (Saturday night) | Stress test (Sunday profile) + spike test | GitHub Actions scheduled |
| Monthly | Soak test (8 hours) | GitHub Actions scheduled |
| Every release candidate | Security scan (OWASP ZAP) | Manual trigger |
| 48 hours before Super Bowl | Full suite: stress + spike + soak + WebSocket + FIX + security | Manual trigger |

---

## 9. Test Infrastructure

### Staging Environment

Mirrors production at reduced scale:

```
Staging:
  Cloud Run services:     min-instances=2 each
  Centrifugo:             1 VM (e2-standard-8)
  FIX Gateway:            1 VM (test mode, mock matching engine)
  PostgreSQL:             Cloud SQL (db-f1-micro, test data)
  Redis:                  Memorystore (basic tier)
  NATS:                   1-node (no JetStream persistence needed)
```

k6 Cloud runs the load generators from distributed regions -- the staging services are the target, not the source of load.

### Grafana Cloud Dashboard

Single dashboard for all performance test results:

```
┌──────────────────────────────────────────────────────────────┐
│  InPlay Performance Dashboard                                 │
│                                                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  │
│  │ Request Latency  │  │ Error Rate      │  │ Throughput   │  │
│  │ p50 / p95 / p99  │  │ % failed        │  │ req/sec      │  │
│  │ [chart]          │  │ [chart]         │  │ [chart]      │  │
│  └─────────────────┘  └─────────────────┘  └──────────────┘  │
│                                                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  │
│  │ Cloud Run        │  │ Centrifugo      │  │ NATS         │  │
│  │ Instance Count   │  │ Connections     │  │ Consumer Lag │  │
│  │ CPU / Memory     │  │ Msg Delivery    │  │ Queue Depth  │  │
│  │ [chart]          │  │ [chart]         │  │ [chart]      │  │
│  └─────────────────┘  └─────────────────┘  └──────────────┘  │
│                                                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  │
│  │ PostgreSQL       │  │ Redis           │  │ FIX Gateway  │  │
│  │ Query Latency    │  │ Memory Usage    │  │ Msg Rate     │  │
│  │ Connections      │  │ Hit Rate        │  │ Seq Numbers  │  │
│  │ [chart]          │  │ [chart]         │  │ [chart]      │  │
│  └─────────────────┘  └─────────────────┘  └──────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

Correlate k6 test results (client-side latency, error rate) with server-side metrics (CPU, memory, connection count, queue depth) in real time during tests.

---

## 10. Pass/Fail Criteria

### Blocking (fails the build)

| Metric | Threshold | Applies to |
|--------|-----------|-----------|
| Unit test pass rate | 100% | Every PR |
| Integration test pass rate | 100% | Every merge |
| API contract test pass rate | 100% | Every merge |
| Smoke test p95 latency | <200ms | Every PR |
| Smoke test error rate | <1% | Every PR |

### Warning (alerts team, doesn't block)

| Metric | Threshold | Applies to |
|--------|-----------|-----------|
| Load test p95 latency | <100ms | Nightly |
| Load test p99 latency | <300ms | Nightly |
| Load test error rate | <0.1% | Nightly |
| WebSocket delivery p99 | <100ms | Weekly |

### Informational (track trends)

| Metric | What to watch | Applies to |
|--------|--------------|-----------|
| Stress test breaking point | Should increase or hold steady over time | Weekly |
| Soak test memory growth | Should be flat, not rising | Monthly |
| Cloud Run auto-scale time | Time from spike to new container serving | Weekly |
| NATS consumer lag during spike | Should drain within 5 seconds | Weekly |
| Centrifugo reconnection recovery | 100% message recovery, zero duplicates | Weekly |
