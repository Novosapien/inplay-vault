---
description: "How the React Native (Expo) app is structured — one codebase for iOS, Android and web, no frontend server, REST + Centrifugo connections, key libraries"
---

# Frontend Architecture

> **Architecture:** [[architecture]]
> **Status:** Draft

## Overview

React Native (Expo) single codebase targeting iOS, Android, and web. There is no frontend server -- the app runs entirely on the user's device. Backend calls go to FastAPI services (REST) and Centrifugo (WebSocket).

## How It Works

```
iOS:     Downloaded from App Store, runs on iPhone
Android: Downloaded from Google Play, runs on Android
Web:     Static JS bundle served from Cloud CDN, runs in browser

All three: same codebase, same behaviour.
No frontend server to deploy or scale.
```

## What the App Connects To

```
React Native App (on user's device)
  │
  ├── HTTPS REST → api.inplay.com (API Gateway → Cloud Run services)
  │   Used for: placing orders, login, KYC, referral, browsing teams
  │
  └── WebSocket → realtime.inplay.com (Centrifugo)
      Used for: live price updates, order fills, game events, leaderboards
```

## Key Libraries

| Library | Purpose |
|---------|---------|
| Expo Router | File-based routing (similar to Next.js app directory) |
| centrifuge (JS SDK) | WebSocket connection to Centrifugo |
| react-native-wagmi-charts or victory-native | Price charts and order book visualisation |
| expo-secure-store | JWT token storage (mobile) |
| expo-notifications | Push notification handling |
| expo-location | Device GPS for ad geo-targeting |
| axios or fetch | HTTP client for API calls |

## Performance Considerations

| Concern | Solution |
|---------|----------|
| Rapid price updates (100 re-renders/sec) | Client-side throttling: batch UI updates to 4-5/sec |
| Mobile reconnection | Centrifugo JS SDK handles automatically (auto-reconnect, resubscribe, recover via last-value cache) |
| Bandwidth | Subscribe to full order book depth only for actively viewed symbol. Watchlist gets top-of-book only. Unsubscribe on navigate away. |
| Background/lock screen | Drop WebSocket, reconnect on foreground. Last-value cache provides instant catch-up. |
| Memory | Only hold active view data in memory. Dispose on navigation. |
