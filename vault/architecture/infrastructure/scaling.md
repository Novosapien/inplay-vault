# Scaling Strategy

> **Architecture:** [[architecture]]
> **Status:** Draft

## What Scales and How

```
DOESN'T NEED TO SCALE (runs on user devices / CDN):
  React Native app        (runs on phones/browsers)
  Web app bundle           (static files on Cloud CDN)

SCALES AUTOMATICALLY (Cloud Run):
  Trading Service          (pre-warm min-instances before games)
  Auth Service             (pre-warm before games)
  Market Data Service      (pre-warm before games)
  Social Service           (pre-warm before games)
  Ad Service               (pre-warm before games)
  Cloud Run Jobs           (triggered on schedule)

SCALES VIA MANAGED INSTANCE GROUP (schedule-controlled):
  Centrifugo               (ramp up before kickoff, scale down post-game)

DOESN'T SCALE (and doesn't need to):
  FIX Gateway              (constant workload regardless of user count)

SCALES VIA GCP TIER CHANGES (if needed):
  Redis Memorystore        (resize tier if connection/memory limits hit)
  Cloud SQL PostgreSQL     (add read replicas if query load grows)
```

## Why the FIX Gateway Doesn't Scale With Users

Market data from tZERO is per-symbol, not per-user: 500 symbols × 50 updates/sec = 25,000 msgs/sec regardless of whether 10K or 5M users are watching. The fan-out to users is Centrifugo's job.

Orders scale with users but are absorbed by Cloud Run Trading Service → NATS JetStream → FIX Gateway drains at tZERO's acceptance rate. The FIX Gateway is a message pump, not a scaling bottleneck.

## Cloud Run Cold Start Mitigation

Each Trading Service request takes ~10ms. With Cloud Run concurrency of 250 per container:

```
min-instances = 50, concurrency = 250
  → 12,500 concurrent request capacity
  → ~1,250,000 orders/second throughput
  → Peak spike: ~125,000 orders/second = well within capacity
  → No cold start triggered
```

Game-day min-instances pre-warmed via Cloud Scheduler before kickoff:

```bash
# Before game:
gcloud run services update trading-service --min-instances=50
gcloud run services update auth-service --min-instances=10
gcloud run services update market-data-service --min-instances=20

# After game:
gcloud run services update trading-service --min-instances=5
gcloud run services update auth-service --min-instances=2
```

## Game-Day Scaling Schedule

```
Pre-season (off-hours):
  Trading Service: min-instances=5
  Auth Service: min-instances=2
  Market Data: min-instances=3
  Social: min-instances=2
  Ads: min-instances=1
  Centrifugo MIG: 3 VMs (~600K connection capacity)

Thursday Night Football:
  Trading Service: min-instances=30
  Auth Service: min-instances=10
  Market Data: min-instances=10
  Social: min-instances=5
  Ads: min-instances=5
  Centrifugo MIG: 10 VMs (~2M connection capacity)

NFL Sunday (multiple games):
  Trading Service: min-instances=50
  Auth Service: min-instances=10
  Market Data: min-instances=20
  Social: min-instances=10
  Ads: min-instances=10
  Centrifugo MIG: 25 VMs (~5M connection capacity)

Post-game:
  DON'T scale down during active games
  Scale down after midnight when connections drop

Off-season:
  All services: min-instances=2-5
  Centrifugo MIG: 3 VMs
```
