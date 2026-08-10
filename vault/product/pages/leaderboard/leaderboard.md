---
description: "Page spec for the Ranks-tab Leaderboard — gap-to-earn hero metric, three competition verticals, four time horizons, ranked list and header-glow states"
---

# Leaderboard

> **Tab:** Ranks
> **Purpose:** The competitive spine — shows users where they stand and what they need to do to earn prizes.
> **Map:** [[product/pages/PAGES|App Pages]]

---

## What Users See

The central competition view. InPlay isn't just about making good trades — it's about outperforming other traders to earn real cash prizes from the season pool ($5M–$25M). The Leaderboard makes that competition tangible.

---

## Key Elements

- **Gap-to-Earn (Hero Number)** — the most important metric on this page. Shows exactly how far the user is from the nearest prize threshold. More actionable than rank alone: "You need $2,340 more P&L to start earning" is more motivating than "You're ranked #847."

- **Three Competition Verticals** (switchable tabs):
  - **Best P&L** — pure profit/loss. Biggest earners win.
  - **Best Risk-Adjusted Return** — rewards smart, consistent trading (Sharpe ratio-style). You don't have to be the biggest trader, just the most efficient.
  - **Comeback Trader** — rewards the biggest improvements. Started poorly? A strong recovery can still earn prizes.

- **Four Time Horizons** (switchable):
  - Daily — resets each day
  - Weekly — resets each week
  - Monthly — resets each month
  - Full Event — cumulative season-long standings

- **Ranked List** — traders listed by rank with:
  - Position number
  - Movement indicator (arrows showing rank change since last period)
  - Trader display name
  - Performance metric for the selected vertical
  - Prize tier indicators at payout breakpoints

- **User Highlight** — the user's own row is visually highlighted and auto-scrolled into view

- **"Me" Button** — tap to instantly scroll to user's position (useful on long lists)

- **Brand Glow Header** — visual treatment that changes color:
  - Green glow = user is currently in an earning position
  - Red glow = user is below the earning threshold

---

## Where Users Go From Here

- Tap any trader → [[product/pages/leaderboard/trader-profile|Trader Profile]]
- Tap "Me" → scrolls to user's position
- Mentally: see gap-to-earn → go to [[product/pages/discover/discovery-feed|Discovery Feed]] to find a trade opportunity

---

## States

- **In earning position:** Green header glow, gap-to-earn shows "buffer" above the line
- **Below earning position:** Red header glow, gap-to-earn shows what's needed to break through
- **Top 10:** Leaderboard visible with prize amounts per position
- **No trading activity yet:** Shows rank at bottom, encourages first trade

---

## Why This Page Matters

The Leaderboard is what turns casual trading into a competition. Users don't just trade to grow their portfolio — they trade to outperform others and earn real prizes. The gap-to-earn metric is deliberately the hero because it creates actionable urgency: "I'm close — one good trade could push me into earning territory."

The three verticals ensure different trading styles can all compete. You don't have to be a whale (Best P&L) — you can win by being smart (Risk-Adjusted) or resilient (Comeback).
