# Centrifugo (Real-Time Delivery)

> **Architecture:** [[architecture]]
> **Service Overview:** [[services-overview]]
> **Status:** Draft

## Overview

Centrifugo is a real-time messaging server that holds all WebSocket connections from clients and delivers messages to them. It's deployed as infrastructure (Docker container with YAML config), not custom code. Interacted with via Python SDK (publishing) and JavaScript SDK (subscribing).

- **Platform:** Managed Instance Group (Compute Engine VMs)
- **Capacity:** 1M-5M concurrent WebSocket connections
- **Min VMs:** 3 (always), up to 25 on peak game days

## What Centrifugo Does

Think of it as a post office. Your Python code drops off messages addressed to channels. Centrifugo maintains a list of who's subscribed to what and delivers them.

- **Channels:** Clients subscribe to topics (e.g., `market.quote.cowboys`, `order.user123.ORD456`)
- **Publishing:** Python backend publishes messages via the Centrifugo Python SDK (`cent` package)
- **Auth:** Validates JWT tokens that FastAPI backend issues at login
- **Last-value cache:** New subscribers and reconnecting users get current state immediately
- **Conflation:** Merges rapid updates to max 10/sec per symbol to manage bandwidth
- **Reconnection:** Client SDK auto-reconnects, resubscribes, recovers missed messages

## Why Managed Instance Group (Not Cloud Run)

WebSocket connections are long-lived (hours during a game). Cloud Run recycles containers during scale-down, deployments, and maintenance. Each recycle drops every connection on that instance. At 1M-5M users, an instance holding 50K connections being recycled causes 50K simultaneous disconnects.

With a Managed Instance Group:
- VMs stay alive until explicitly removed
- Scale-down scheduled for off-hours (never during games)
- Google auto-heals failed VMs
- Existing VMs keep their connections untouched during scale-up

## Channel Mapping (from T0 Spec)

| Channel | Data | Source |
|---------|------|--------|
| `market.quote.{symbol}` | Best bid/offer | FIX v8 incremental |
| `market.book.{symbol}` | Order book depth | IOI v1.2 + FIX v8 |
| `market.trade.{symbol}` | Executed trades | FIX v8 incremental |
| `market.snapshot.{symbol}` | OHLC, volume, prev close | IOI v1.2 snapshot |
| `market.status.{symbol}` | Halt/resume, SSR | FIX v8 security status |
| `market.session` | Trading session phase | FIX v8 session status |
| `order.{userId}.{orderId}` | Order status, fills | OE execution reports |
| `position.{userId}` | Position, P&L | OE execution reports |
| `leaderboard.{vertical}.{timeframe}` | Rankings | Competition Cloud Run Job |
| `ad.{userId}` | Targeted ad delivery | Ad Service |

## Publishing (Python)

```python
from cent import Client

centrifugo = Client("http://centrifugo:8000/api", api_key="your-key")

centrifugo.publish("market.quote.cowboys", {
    "bid": 24.50,
    "ask": 24.75,
    "last": 24.60,
    "volume": 15230
})
```

## Subscribing (React Native)

```javascript
import { Centrifuge } from 'centrifuge';

const client = new Centrifuge('wss://realtime.inplay.com/connection', {
    token: jwtFromFastAPI
});

const sub = client.newSubscription('market.quote.cowboys');
sub.on('publication', (ctx) => {
    updatePriceChart(ctx.data);
});
sub.subscribe();
client.connect();
```

## Scaling Schedule

| Period | VMs | Capacity | Trigger |
|--------|-----|----------|---------|
| Off-season | 3 | ~600K connections | Default |
| Thursday Night Football | 10 | ~2M connections | Cloud Scheduler pre-kickoff |
| NFL Sunday (multiple games) | 25 | ~5M connections | Cloud Scheduler pre-noon |
| Post-game | Hold | Don't scale down | Wait for users to disconnect naturally |
| Late night (2am+) | 5 | ~1M connections | Cloud Scheduler |

## NATS Broker Mode

Centrifugo uses NATS JetStream as its broker natively. When any service publishes to a NATS subject matching a Centrifugo channel name, Centrifugo picks it up and delivers to all subscribed WebSocket clients. No bridge service needed.

```yaml
# centrifugo config.yaml
broker:
  type: nats
  nats:
    url: "nats://your-nats-server:4222"

token:
  hmac_secret_key: "same-secret-as-fastapi-jwt"

api:
  key: "your-api-key"
```

This means the FIX Gateway publishes once to NATS, and both Centrifugo (for client delivery) and backend services (for processing) receive the message. One publish, multiple consumers.
