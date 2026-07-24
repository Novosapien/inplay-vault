# Trader Profile

> **Tab:** Ranks
> **Purpose:** Public profile of another trader on the leaderboard.
> **Map:** [[product/pages/PAGES|App Pages]]

---

## What Users See

When a user taps on another trader in the leaderboard, they see that person's public trading stats. This adds a social/competitive dimension — you can see who you're competing against and how they trade.

---

## Key Elements

- **Trader Identity**, public username and avatar (see [[#Public Usernames]])
- **Current Rank** — position on the leaderboard with movement indicator
- **Performance Stats:**
  - Total P&L (profit/loss)
  - Sharpe ratio (risk-adjusted performance)
  - Win rate (percentage of profitable trades)
  - Number of trades made
- **Recent Activity** — anonymised recent trades showing:
  - Teams traded (not exact quantities or prices — privacy preserved)
  - General activity level (frequent trader vs. occasional)

---

## Where Users Go From Here

- Back → [[product/pages/leaderboard/leaderboard|Leaderboard]]

---

## States

- **Active trader:** Full stats and recent activity
- **Inactive trader:** Stats from earlier period, no recent activity shown

---

## Public Usernames

_Added 24-07-2026 from [[jared-app-feedback-jul-2026]] (Jared Sapirman, item 6)._

Every user should be able to **create their own public username**, the display identity shown on this profile, on the leaderboard, and across social surfaces. Guardrails are required:

- **Vulgarity filter**, reject vulgar or offensive names at creation.
- **Impersonation guardrails**, protections against impersonating other users or public figures.

Public usernames are **foundational to the social features** (Groups & Leagues, influencer-hosted groups, streaks) described in [[third-space]]: friendly competition and shared leagues need a stable public identity to hang off. Open items, username uniqueness/change policy and where creation lives in the flow (profile vs onboarding), are candidates for the social-layer session.

---

## Privacy Note

Trader profiles show enough to be interesting and competitive, but not enough to copy someone's exact strategy. Quantities and prices are not revealed — only which teams were traded and general performance metrics.
