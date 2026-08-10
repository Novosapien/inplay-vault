---
description: "Reconnection flow after a WebSocket drop — server-side FIX sessions unaffected, Centrifugo last-value cache restores current data in ~1s, mobile notes"
---

# Data Flow: User Reconnection

> **Architecture:** [[architecture]]
> **Status:** Draft

## Scenario: User's WiFi Drops for 3 Seconds

```
WiFi drops
  → WebSocket to Centrifugo disconnects
  → App shows "Reconnecting..." indicator
  │
  │  During the 3-second gap:
  │  → FIX sessions to tZERO completely UNAFFECTED (server-side)
  │  → Market data and order events continue flowing into Redis
  │  → Centrifugo continues receiving updates from NATS
  │  → If user had open orders, fills processed server-side normally
  │
WiFi returns
  → Centrifugo client SDK auto-reconnects (~<1 second)
  → Client re-subscribes to previously watched channels
  → Centrifugo delivers LAST-VALUE-CACHED data immediately
  → User sees current prices within ~1 second, no loading spinner
  → No stale data displayed
  → Streaming updates resume from bus subscriptions
  │
  │  Any fills during the gap:
  │  → Already processed by Trading Service
  │  → Order state is correct in PostgreSQL
  │  → User's position and wallet already updated
  │  → Fill confirmation delivered on reconnect
```

## Key Principle

The user should NEVER need to know about FIX session state. The server-side infrastructure (FIX Gateway, Redis, Centrifugo) abstracts all recovery. From the user's perspective: brief "Reconnecting..." indicator, then everything is current.

## Last-Value Cache

Centrifugo maintains the most recent message for each channel. When a user reconnects and re-subscribes, they immediately receive the latest data without waiting for the next tZERO update. This eliminates loading spinners and stale data on reconnection.

## Mobile-Specific Considerations

- Mobile users lose signal constantly (walking, subway, switching WiFi/cellular)
- App going to background should drop WebSocket (save battery/data)
- App returning to foreground reconnects and gets current state via last-value cache
- Centrifugo JS SDK handles all reconnection logic automatically
