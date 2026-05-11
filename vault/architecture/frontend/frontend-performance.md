# Frontend Performance

> **Architecture:** [[architecture]]
> **Status:** Draft

## No Server-Side Scaling

The React Native app runs on user devices. There is no frontend server to scale. 5M users means 5M phones each running their own copy of the app. The CDN serves the web bundle from edge nodes worldwide (~$50-100/month at any scale).

## Real-Time Data Handling

| Concern | Problem | Solution |
|---------|---------|----------|
| **Rapid price updates** | Centrifugo delivers 10 updates/sec/symbol. With 10 symbols on screen = 100 updates/sec. Rendering all of them kills battery and frame rate. | Client-side throttling: batch UI updates to 4-5 renders/sec. Receive all updates, only render periodically. |
| **Reconnection** | Mobile users lose signal constantly (walking, subway, WiFi/cellular switch). | Centrifugo JS SDK handles automatically: auto-reconnect in <1 second, resubscribe to channels, recover missed data via last-value cache. |
| **Subscription management** | Full order book depth for all watchlist symbols wastes bandwidth. | Full depth only for the actively viewed symbol. Watchlist gets top-of-book only (MarketDepth=1). Unsubscribe when user navigates away. Matches T0 spec lazy subscription pattern. |
| **Background/lock screen** | User locks phone or switches to another app. Maintaining WebSocket wastes battery and data. | Drop WebSocket on background event. Reconnect on foreground event. Last-value cache ensures instant catch-up -- no loading spinner, no stale data. |
| **Memory** | Order book depth for a popular symbol can be large. Holding all symbols in memory is wasteful. | Only hold data for active views in memory. Dispose on navigation. Let Centrifugo's last-value cache re-deliver on return. |
| **Bundle size** | Large JS bundle = slow first load on web. | Code splitting via Expo Router (lazy-load screens). Target <3MB initial bundle. Subsequent loads cached by browser/CDN. |
