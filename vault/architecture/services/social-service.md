# Social Service

> **Architecture:** [[architecture]]
> **Service Overview:** [[services-overview]]
> **Status:** Draft

## Overview

Handles the referral engine, leaderboards, and push notifications. The referral system is InPlay's primary growth engine -- dual-sided rewards, social media engagement credits, and multiplier days.

- **Path:** `/social/*`
- **Platform:** Cloud Run
- **Game day min-instances:** 10

## Responsibilities

- Referral system (code generation, dual-sided rewards, social engagement credits, multiplier days)
- Leaderboard queries (3 verticals × 4 timeframes, proximity indicators)
- Push notification management (FCM/APNs token registration, preferences)

## Endpoints

### Referrals

| Method | Path | Description |
|--------|------|-------------|
| GET | `/social/referral/code` | Get user's referral code |
| GET | `/social/referral/stats` | Referral count, wallet balance, history |
| GET | `/social/referral/wallet` | Referral wallet balance and transaction history |

### Leaderboards

| Method | Path | Description |
|--------|------|-------------|
| GET | `/social/leaderboard/{vertical}/{timeframe}` | Get leaderboard (vertical: pnl/risk/comeback, timeframe: daily/weekly/monthly/season) |
| GET | `/social/leaderboard/me` | User's ranking across all verticals and timeframes |
| GET | `/social/leaderboard/proximity` | "You are 112 places from cashing" |

### Notifications

| Method | Path | Description |
|--------|------|-------------|
| POST | `/social/notifications/register` | Register FCM/APNs push token |
| GET | `/social/notifications/preferences` | Get notification preferences |
| PUT | `/social/notifications/preferences` | Update preferences (game reminders, trade alerts, etc.) |

## Referral Mechanics

- **Referral code:** Auto-generated on KYC approval, tied to account
- **Dual-sided reward:** 1,000 InPlay dollars to referrer, 500 to referee (triggered on referee's KYC completion)
- **Referral wallet:** Separate from trading wallet, no cap, resets to zero at end of season
- **Trading wallet reload:** When trading wallet drops below 25,000, user can reload from referral wallet back to 100,000 (never exceeds 100,000)
- **Social media engagement:** Following, commenting on InPlay social posts earns InPlay dollars into referral wallet
- **Bonus multiplier days:** e.g., Fourth of July = 2,000 per referral instead of 1,000
- **Sponsor redemption:** Users with large referral banks can redeem for special sponsor offers (post-launch)

## Leaderboard Architecture

Leaderboards are calculated by a Cloud Run Job every 5-15 seconds, not by this service. This service only queries the pre-computed results from Redis sorted sets.

```
Cloud Run Job (every 5-15s):
  → Read all user positions + current prices
  → Calculate P&L for every user
  → Calculate risk-adjusted returns
  → Calculate comeback scores (recovery from deepest drawdown)
  → Write results to Redis sorted sets
  → Publish top changes to Centrifugo (leaderboard.{vertical}.{timeframe})

Social Service (on user request):
  → ZREVRANGE on Redis sorted set → return top N users
  → ZRANK for user's position → return proximity indicator
```

### Three Competition Verticals

| Vertical | Metric | Rewards |
|----------|--------|---------|
| **Best P&L** | Who made the most money today | Pays down to ~400 places, top prize ~$10K/day |
| **Best risk-adjusted return** | Smoothest upward P&L curve | Rewards disciplined risk management |
| **Comeback trader** | Biggest recovery from deepest drawdown | Rewards persistence |

### Four Timeframes

Daily, weekly, monthly, and full-season. Each vertical runs across all four timeframes = 12 leaderboards total.

## Scaling Profile

Moderate, steady traffic during games. Spikes when users check leaderboard after a big play. Not latency-critical -- 5-15 second staleness in leaderboard data is acceptable.
