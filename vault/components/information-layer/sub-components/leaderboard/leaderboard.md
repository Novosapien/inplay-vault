# InPlay Trading Challenge -- Leaderboard

> **Component:** [[information-layer]]
> **Status:** Collecting
> **Sources:** _[[meetings/08-05-2026-compoent-1]], [[meetings/06-05-2026-vision-workshop]]_

---

Full rankings view plus widgets embedded across other pages. Tracks competition across three verticals and four time horizons.

## Key Elements (from component session and vision)

**Three competition verticals:**
- Best P&L (top earner)
- Best risk-adjusted return
- Comeback trader of the day

**Four time horizons:**
- Daily
- Weekly
- Monthly
- Full event (entire season)

**User-facing features:**
- Current ranking relative to the full field
- Gap to payout position: "you need $X more P&L to reach the payout zone" / "the person in 50th place has $Y, you have $Z"
- Proximity alerts when approaching or falling away from payout positions
- Badges / trader of the week announcements (Brett's suggestion)
- Special event days with enhanced prizes (Thanksgiving, Christmas)

**Embedded widgets:**
- Mini leaderboard on Single Game Page showing user's current position
- Proximity indicator across other pages

## Business Rules

- Daily calculations: games count based on start time within 24-hour period, not finish time
- Leaderboard resets: daily resets for daily vertical, rolling for weekly/monthly, cumulative for event
- Three separate payout structures per time horizon

## Open Questions

1. How do we communicate "risk-adjusted return" to non-trader personas (Sports-Passionate Casual)? Sharpe ratio is not accessible language
2. What defines "comeback trader"? Biggest swing from negative to positive P&L in a day?
3. How many places pay out per vertical per time horizon?
4. Do users see other users' positions/trades on the leaderboard, or just rankings and P&L?
5. Special event days -- what are the prize multipliers? Who decides which days are special?
