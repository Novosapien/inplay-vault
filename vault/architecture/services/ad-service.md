# Ad Service

> **Architecture:** [[architecture]]
> **Service Overview:** [[services-overview]]
> **Status:** Draft

## Overview

InPlay's revenue model is ~90% advertising. The ad service supports both standard ad delivery via Google Ad Manager (launch) and InPlay's unique moment-based ad system (post-launch).

- **Path:** `/ads/*`
- **Platform:** Cloud Run
- **Game day min-instances:** 10

## Phase 1: Launch (Google Ad Manager)

At launch, use Google Ad Manager (GAM) for ad serving.

**How it works:**
- Skye's team sells sponsorships directly to advertisers
- Sponsorships configured as GAM "line items" with targeting rules
- GAM serves directly-sold ads first (InPlay keeps 100% of revenue)
- Unsold inventory backfilled by Google AdMob programmatic ads (Google takes ~40%)
- GAM handles impression tracking, click tracking, and reporting

**Ad formats:**

| Format | Placement | CPM Range |
|--------|-----------|-----------|
| Banner (320x50) | Bottom of game pages, team pages | $0.50-2.00 |
| Native ad | In news feed, between content cards | $5-15 |
| Interstitial | Between screen transitions | $3-10 |
| Rewarded | "Watch ad for 500 InPlay dollars" | $10-30 |

**What GAM can target at launch:**
- Age range (from KYC -- verified, not guessed)
- Device platform (iOS/Android)
- Custom key-values (e.g., game=cowboys-giants, page=trading)

**What GAM cannot do:**
- Trigger ads from live game events
- Geo-target within 3 miles in real-time
- Time-delay ads
- Tie ads to volatility moments

## Phase 2: Post-Launch (Custom Moment-Based System)

InPlay's unique ad model: sponsors own specific game moments with real-time targeting. Layered on top of GAM.

```
Sport Radar: "Touchdown -- Cowboys, Q3, 7:42"
      │
      ▼
  Event Trigger Engine
      │
      │  1. Match event against active campaigns
      │     "Which sponsors own Cowboys touchdown moments?"
      │
      │  2. Resolve target audience from pre-computed Redis segments
      │
      │  3. Publish ad payload to qualifying users via Centrifugo
      │
      ▼
  User sees ad within ~100ms of the touchdown
```

### Components

| Component | What It Does |
|-----------|-------------|
| Campaign Manager | Admin panel for configuring campaigns, moment ownership, targeting rules, creatives |
| Moment-to-Sponsor Mapping | Database linking game events to sponsors (PostgreSQL) |
| Event Trigger Engine | Matches Sport Radar game events against active campaigns |
| Targeting Engine | Filters users by pre-computed segments (age, geo, teams followed) in Redis |
| Ad Delivery | Publishes ad payload through Centrifugo to qualifying users |
| Impression Tracking | Records when ads were shown, clicked, engaged with |
| Reporting Dashboard | Campaign performance for advertisers and Skye's team |

### Pre-Computed Targeting

When a campaign is created, target user segments are pre-computed into Redis sets:

```
Campaign: "Doritos, Cowboys touchdowns, age 25-35"
  → Query PostgreSQL for matching users
  → Store: Redis SET campaign:doritos-cowboys-td = [user1, user2, ...]
  → Refresh periodically (new signups, profile changes)

When touchdown happens:
  → Read pre-computed set (~1ms)
  → Publish to those users via Centrifugo
  → Total: ~10ms
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/ads/impression` | Record an ad impression |
| POST | `/ads/click` | Record an ad click |
| GET | `/ads/campaigns` | List active campaigns (admin) |
| POST | `/ads/campaigns` | Create campaign (admin) |
| PUT | `/ads/campaigns/{id}` | Update campaign (admin) |
| GET | `/ads/reports/{campaignId}` | Campaign performance report (admin) |

## Targeting Data Sources

All first-party, KYC-verified data:

| Data | Source | Ad Use |
|------|--------|--------|
| Age | KYC (Persona) | Demographic targeting |
| Location | Device GPS | Geo-targeting (Redis GEORADIUS) |
| Teams followed | User selection | Interest targeting |
| Trading behaviour | App activity | Engagement-based targeting |
| Session duration | App activity | "Consumed minutes" for advertiser reporting |

## Privacy

- Privacy policy must disclose data use for advertising
- Location requires device permission (user can decline)
- CCPA: "Do Not Sell" option for California users
- Age-gated data: extra care with 18-20 year olds
- InPlay's KYC-verified first-party data is significantly more valuable than cookie-based targeting

## Scaling Profile

Scales with ad impressions, not with orders. During games: every screen view is a potential impression. Off-hours: near zero.
