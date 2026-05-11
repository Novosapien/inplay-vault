# Frontend Framework Decision

> **Architecture:** [[architecture]]
> **Status:** Draft

## Decision: React Native (Expo)

Single codebase targeting iOS, Android, and web. The app runs entirely on the user's device -- there is no frontend server to deploy or scale.

## How React Native (Expo) Differs from Next.js

**Next.js (server-rendered):**
```
User's browser ──request──► Next.js SERVER ──► renders HTML ──► sends back to browser
                                  │
                            This server runs YOUR code:
                            server components, SSR, API routes.
                            More users = more server load.
                            You must scale this server.
```

**React Native / Expo (client-side):**
```
BUILD TIME (once, before deployment):
  Your code ──build──► static bundle (HTML + JS + CSS files)
                       Just files. No server needed.

RUNTIME (every user):
  Mobile: downloaded from App Store/Google Play, runs on their phone
  Web: browser downloads the JS bundle from CDN, runs it locally

  Everything runs on the USER'S DEVICE.
  Their phone/browser does all the rendering.
  The only server calls are to FastAPI (data) and Centrifugo (real-time).
```

A Next.js developer can be productive in React Native within a week. The React concepts (components, hooks, state, props, context, effects) are identical. The differences are cosmetic: `<View>` instead of `<div>`, `<Text>` instead of `<p>`, `StyleSheet` instead of CSS.

## Web Framework Landscape

| Framework | Based On | Rendering | Key Trait |
|-----------|----------|-----------|-----------|
| Next.js | React | Server + client | Most popular server-rendered React framework |
| Nuxt | Vue | Server + client | Next.js equivalent for Vue |
| SvelteKit | Svelte | Server + client | Next.js equivalent for Svelte |
| Remix | React | Server + client | Alternative to Next.js, different data loading philosophy |
| React (Vite) | React | Client only | No server, browser renders everything |
| Vue (Vite) | Vue | Client only | Same but Vue |
| Angular | Angular | Client only (SSR optional) | Google's framework, enterprise-heavy, steep learning curve |

## Underlying UI Libraries

| Library | Created By | Ecosystem | Learning Curve | Hiring Pool |
|---------|-----------|-----------|----------------|-------------|
| React | Meta/Facebook | Massive (largest) | Moderate | Huge |
| Vue | Evan You | Large | Easiest | Good |
| Svelte | Rich Harris | Growing | Easy | Smallest |
| Angular | Google | Large | Steepest | Good (enterprise) |

## Cross-Platform Mobile Frameworks

| Framework | Language | Performance | Web Support | InPlay Fit |
|-----------|----------|-------------|-------------|------------|
| React Native (Expo) | TypeScript | Very good (native bridge) | Good via Expo | **Chosen** -- team knows React/TS, single codebase, large ecosystem |
| Flutter | Dart | Excellent (compiled) | Works but feels app-like | Rejected -- Dart has no synergy with Python backend, weaker web story, smaller hiring pool |
| Ionic | TypeScript | Weakest (WebView) | Great (it's already web) | Rejected -- WebView performance too slow for real-time trading charts |
| Native (Swift + Kotlin) | Swift / Kotlin | Best possible | N/A (separate web needed) | Rejected -- 3x development effort, 3 codebases |
