# Player Profile

> **Tab:** Discover
> **Purpose:** Individual player research — bio, stats, and injury status.
> **Map:** [[product/pages/PAGES|App Pages]]

---

## What Users See

A focused view of one player's biographical information and season statistics. Players don't have their own tradeable stocks — the value here is research context. A star quarterback's injury status or a running back's recent form directly impacts the team's stock price.

---

## Key Elements

- **Jersey Number Badge** — large rounded badge showing the player's number (e.g., #15). No player photos are shown (licensing constraint — requires separate NFLPA agreements).

- **Player Identity** — full name, full position name (e.g., "Quarterback" not "QB"), team name (tappable → Team Page)

- **Injury Banner** — if the player is injured, a color-coded banner appears:
  - Red = Out (not playing)
  - Amber = Questionable (uncertain)
  - Green = Probable (likely playing)
  - Shows injury description (e.g., "Ankle — Questionable")

- **Headline Stats Grid** — the 4 most important numbers for that player's position:
  - QB: Passing yards, TDs, Interceptions, Passer rating
  - RB: Rushing yards, TDs, Yards per carry, Receptions
  - WR/TE: Receiving yards, TDs, Receptions, Yards per catch

- **Bio Card** — personal information:
  - Height and weight
  - Age (calculated from birth date)
  - Hometown
  - College
  - NFL Draft info (round, pick, year) — or eligibility info for NCAA players
  - Years of experience

- **Expanded Stat Tables** — detailed season statistics broken into categories appropriate to position:
  - QB: Passing table (attempts, completions, yards, TDs, INTs, rating) + Rushing table
  - RB: Rushing table (carries, yards, TDs, fumbles) + Receiving table
  - WR/TE: Receiving table (targets, receptions, yards, TDs, drops)

---

## Where Users Go From Here

- Tap team name → [[product/pages/discover/team-page|Team Page]]
- Back button → previous screen (usually [[product/pages/discover/team-page|Team Page]] or [[product/pages/discover/single-game-page|Single Game Page]])

---

## States

- **Healthy player:** No injury banner shown
- **Injured player:** Injury banner with severity color and description
- **NFL player:** Shows draft information in bio
- **NCAA player:** Shows eligibility status instead of draft info

---

## Why This Page Matters

Player-level information drives team stock prices. If a team's star quarterback is listed as "Out," that's a sell signal. If a backup running back has been putting up big numbers, the team might be undervalued. The Player Profile gives users the research context to make informed trading decisions about the team.
