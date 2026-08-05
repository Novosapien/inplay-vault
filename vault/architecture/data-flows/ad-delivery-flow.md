---
description: "Ad-delivery flow in two phases — client-side Google Ad Manager at launch, then moment-based sponsor ads via pre-computed Redis segments and Centrifugo in ~100ms"
---

# Data Flow: Ad Delivery

> **Architecture:** [[architecture]]
> **Ad Service:** [[ad-service]]
> **Status:** Draft

## Phase 1: Standard Ads (Launch)

```
User opens game page
  → App renders ad placement (banner, native, etc.)
  → Google Ad Manager SDK requests an ad
  → GAM selects ad based on line item targeting (age, page, game)
  → Ad displays
  → GAM tracks impression automatically
```

No custom backend involvement. GAM SDK handles everything client-side.

## Phase 2: Moment-Based Ads (Post-Launch)

```
Sport Radar: "Touchdown -- Cowboys, Q3, 7:42"
  │
  ▼
Main API / Ad Service receives game event
  │
  │  1. Match event against active campaigns (PostgreSQL)
  │     "Which sponsors own Cowboys touchdown moments?"
  │     → Doritos: age 25-35
  │     → DoorDash: within 3 miles of stadium
  │
  │  2. For each matching campaign, read pre-computed user set (Redis)
  │     → Redis SET campaign:doritos-cowboys-td = [user1, user2, ...]
  │     → Redis GEORADIUS for geo-targeted campaigns
  │
  │  3. Publish ad payload to qualifying users
  │     → Centrifugo channel: ad.{userId}
  │
  ▼
User sees sponsored ad within ~100ms of the touchdown
  │
  │  4. App sends impression event
  │     → POST /ads/impression
  │     → Recorded in PostgreSQL for reporting
```

## Pre-Computed Targeting

Target segments are built when campaigns are created/updated, not at delivery time:

```
Campaign created: "Doritos, Cowboys touchdowns, age 25-35"
  → Query: SELECT user_id FROM users WHERE age BETWEEN 25 AND 35
            AND 'cowboys' = ANY(teams_followed)
  → Store in Redis: SET campaign:doritos-cowboys-td = [user1, user2, ...]
  → Refresh periodically (new signups, profile updates)

At delivery time:
  → Read pre-computed set from Redis (~1ms)
  → Publish to those users via Centrifugo (~5ms)
  → Total: ~10ms from game event to ad delivery
```
