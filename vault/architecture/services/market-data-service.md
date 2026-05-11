# Market Data Service

> **Architecture:** [[architecture]]
> **Service Overview:** [[services-overview]]
> **Status:** Draft

## Overview

Serves team pages, game pages, news, stats, and historical data. Read-heavy service that combines data from Sport Radar (game/player data), tZERO REST API (historical market data), and internal PostgreSQL (favourites, user preferences).

- **Path:** `/market/*`
- **Platform:** Cloud Run
- **Game day min-instances:** 20

## Responsibilities

- Team pages (historical performance, upcoming matchups, player stats, price charts)
- Game pages (schedule, game details, team matchups)
- News feed (AP-style editorial from Sport Radar, block trade alerts)
- Historical stats and data (powered by Sport Radar + tZERO REST API)
- Favourites/following (users follow teams without holding shares)

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/market/teams` | List all teams (NFL + college) |
| GET | `/market/teams/{symbol}` | Team detail (stats, price history, upcoming games) |
| GET | `/market/teams/{symbol}/history` | Historical price data from tZERO REST API |
| GET | `/market/games` | Upcoming and live game schedule |
| GET | `/market/games/{gameId}` | Single game detail |
| GET | `/market/news` | News feed (Sport Radar editorial + block trade alerts) |
| GET | `/market/news/{articleId}` | Single article |
| POST | `/market/favourites/{symbol}` | Follow a team |
| DELETE | `/market/favourites/{symbol}` | Unfollow a team |
| GET | `/market/favourites` | List user's followed teams |

## Data Sources

| Data | Source | Caching Strategy |
|------|--------|-----------------|
| Team info, player stats | Sport Radar API | Redis cache, 5-minute TTL |
| Historical price data | tZERO REST API | Redis cache, 1-hour TTL (doesn't change intra-day) |
| Game schedule | Sport Radar API | Redis cache, 1-hour TTL |
| Live game data | Sport Radar real-time feed → NATS → Centrifugo | Not served by this service -- goes direct via Centrifugo |
| News articles | Sport Radar editorial feed | PostgreSQL (persistent), Redis cache for recent |
| Block trade alerts | FIX Gateway → NATS → Centrifugo | PostgreSQL (persistent), delivered real-time via Centrifugo |
| Favourites | User action | PostgreSQL |

## Note on Real-Time vs REST

This service handles **non-real-time** market data requests. Live price updates, order book changes, and game events are delivered via **Centrifugo** (WebSocket), not through this service. The Market Data Service is for browsing, research, and historical data -- the "Bloomberg terminal research" use case, not the "live ticker" use case.

## Scaling Profile

Steady traffic throughout games. Users browse teams, check stats, read news between trading moments. Not as spiky as Trading Service.
