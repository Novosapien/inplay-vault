# API Gateway

> **Architecture:** [[architecture]]
> **Status:** Draft

## Overview

Google Cloud API Gateway provides path-based routing to 5 Cloud Run services, JWT validation at the edge, and per-route rate limiting.

## Routing

```
api.inplay.com/auth/*     → Auth Service (Cloud Run)
api.inplay.com/trading/*  → Trading Service (Cloud Run)
api.inplay.com/market/*   → Market Data Service (Cloud Run)
api.inplay.com/social/*   → Social Service (Cloud Run)
api.inplay.com/ads/*      → Ad Service (Cloud Run)
```

Centrifugo is on a separate domain (`realtime.inplay.com`) and does not go through the API Gateway. Centrifugo validates JWTs itself.

## Responsibilities

| Feature | Purpose |
|---------|---------|
| Path-based routing | Route to correct Cloud Run service by URL prefix |
| JWT validation | Validate tokens at the edge, reject bad tokens before they reach services |
| Per-route rate limiting | `/trading/*`: 10 requests/sec/user (strict). `/market/*`: 100 requests/sec/user (relaxed) |
| SSL termination | Handle HTTPS, forward HTTP internally |

## What Goes Through the Gateway

```
GOES THROUGH API GATEWAY:
  ✓ All client REST requests (orders, auth, KYC, referrals, etc.)

DOES NOT GO THROUGH API GATEWAY:
  ✗ Centrifugo WebSocket connections (separate domain, own load balancer)
  ✗ FIX Gateway ↔ tZERO (direct FIX 4.2 TCP, co-located)
  ✗ Service ↔ Redis / PostgreSQL (internal GCP networking)
  ✗ Service → tZERO REST API (server-to-server)
  ✗ Service → Sport Radar / Persona (server-to-server)
  ✗ Cloud Run Jobs (triggered by Cloud Scheduler)
```

## Rate Limiting by Route

| Route | Limit | Rationale |
|-------|-------|-----------|
| `/trading/orders` (POST) | 10/sec/user | Prevent order spam, protect tZERO queue |
| `/trading/*` (GET) | 50/sec/user | Portfolio/position checks during active trading |
| `/auth/login` | 5/min/IP | Brute force protection |
| `/auth/signup` | 3/min/IP | Bot prevention |
| `/market/*` | 100/sec/user | Read-heavy, data browsing |
| `/social/*` | 50/sec/user | Standard |
| `/ads/*` | 100/sec/user | Impression tracking can be high volume |

## DDoS Protection

Cloud Armor sits in front of the API Gateway and provides:
- WAF (Web Application Firewall) rules
- IP-based rate limiting
- Geographic restrictions (if needed)
- Bot detection
- Automatic DDoS mitigation

## Alternatives Considered

| Option | Verdict |
|--------|---------|
| No gateway (Load Balancer + FastAPI middleware only) | Considered for simplicity, but with 5 services the routing and rate limiting benefit justifies the gateway |
| Apigee | Overkill and expensive ($3,500-25,000+/month) for 5 services |
| Kong (self-hosted on Cloud Run) | Additional service to manage. Google's managed gateway is simpler. |
| Cloud Endpoints | Less mature rate limiting. Cloud API Gateway is the better fit. |

Confirm with Brett which gateway pattern he has experience operating at scale.
