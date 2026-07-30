# InPlay IPO Pricing 2026 (v1.0)

> **Component:** [[ipo-module]]
> **Type:** Pricing reference (authoritative listed IPO prices for the 2026 season)
> **Received:** 2026-07-29, from Edwin
> **Model:** InPlay Football Trading Challenge, IPO Pricing System v1.0
> **Source file (safe copy in vault):** `sources/InPlay_IPO_Pricing_2026.xlsx` (beside this doc). Also in shared `meeting-notes/InPlay_IPO_Pricing_2026.xlsx`.
> **Status:** Latest listed IPO prices. Treat this doc + the source workbook as the system of record for IPO pricing until a newer version supersedes it.

---

## Why this exists

These are the **listed IPO prices** every tradeable team company is issued at before secondary trading opens (see [[primary-offering-execution]] and [[team-ipo-detail]]). Keeping the latest prices captured here, in readable form, means the numbers survive even if the workbook is lost. **32 NFL** teams and **138 NCAA** teams are priced below.

## The pricing formula

The IPO price is the **expected terminal (liquidating) distribution per share**:

```
IPO = $5.00 x E[Wins]  +  $2.50 x E[Ties]  (NFL only)  +  $2.50/game x E[Volume Capture Share]
```

- **On-field leg:** BetMGM season win-total prices are devigged proportionally to P(over). Season wins are modeled Normal(mu, sigma) around the posted line: mu = line + sigma x InvNorm(P_over). Sigma is the market-implied dispersion of season wins (NFL 2.7, NCAA 2.2).
- **Off-field leg (Popularity Index at IPO):** Pop = 0.6 x Brand + 0.4 x PerfIndex, where Brand is a hand-assigned 0 to 100 fanbase/brand tier (a Base Demand Index proxy, since no realized volume exists at IPO) and PerfIndex = 100 x E[Wins]/Games. Expected per-game capture vs opponent j is Bradley-Terry: Pop_i / (Pop_i + Pop_j), clamped to [0.20, 0.80]. Games vs non-universe opponents pay the universe team the full $2.50 uncontested.
- A small **variable IPO discount** (underpricing band 1% to 3%) is applied, scaled by each name's contested off-field EV share (a proxy for pricing uncertainty); near-riskless names above the guaranteed threshold get no discount.

**Listed IPO** = IPO EV after the discount, rounded to a penny tick.

## Parameters (v1.0 defaults)

| Parameter | Value | Notes |
|-----------|-------|-------|
| Win payment | $5.00 / share | SDMM-1 game-settlement accrual, win |
| Tie payment | $2.50 / share | NFL only |
| Off-field pool | $2.50 / game | Split pro rata by counted share volume; full pool vs a non-universe opponent |
| Sigma, NFL season wins | 2.7 | SD of the 17-game win distribution around the market total |
| Sigma, NCAA season wins | 2.2 | SD of the 12-game win distribution |
| Expected NFL ties / team | 0.08 | ~1 to 2 ties league-wide per season |
| NFL games | 17 | Regular season only |
| NCAA games | 12 | Regular season only |
| IPO price tick | $0.01 | Penny tick per IPO mechanics |
| Capture clamp | [0.20, 0.80] | Per-game volume-capture floor/ceiling |
| Brand weight (popularity) | 0.6 | Pop = 0.6 x Brand + 0.4 x PerfIndex |
| Performance weight | 0.4 | PerfIndex = 100 x E[Wins]/Games |
| Bradley-Terry gamma | 1 | Capture concentration exponent |
| IPO discount band | 1% to 3% | Variable underpricing, by contested off-field EV share |
| No-discount guaranteed threshold | 0.2 | Near-riskless names get no discount |

## NFL listed IPO prices

Sorted as issued (highest to lowest).

| Team | Conf/Div | Win Total | E[Wins] | On-Field EV | Off-Field EV | IPO EV | Discount % | Listed IPO ($) |
|------|----------|-----------|---------|-------------|--------------|--------|-----------|----------------|
| Los Angeles Rams | NFC West | 11.5 | 11.88 | 59.61 | 22.41 | 82.02 | 1.00% | **81.20** |
| Baltimore Ravens | AFC North | 11.5 | 11.09 | 55.67 | 22.70 | 78.37 | 1.16% | **77.46** |
| Buffalo Bills | AFC East | 10.5 | 10.95 | 54.93 | 23.31 | 78.24 | 1.24% | **77.27** |
| Detroit Lions | NFC North | 10.5 | 10.79 | 54.15 | 22.90 | 77.05 | 1.23% | **76.10** |
| Seattle Seahawks | NFC West | 10.5 | 10.72 | 53.80 | 22.14 | 75.94 | 1.18% | **75.05** |
| San Francisco 49ers | NFC West | 10.5 | 10.28 | 51.60 | 23.73 | 75.33 | 1.40% | **74.27** |
| Kansas City Chiefs | AFC West | 10.5 | 10.14 | 50.92 | 24.13 | 75.04 | 1.46% | **73.95** |
| Philadelphia Eagles | NFC East | 10.5 | 10.05 | 50.47 | 23.46 | 73.93 | 1.42% | **72.88** |
| New England Patriots | AFC East | 10.5 | 10.05 | 50.47 | 22.78 | 73.25 | 1.36% | **72.25** |
| Cincinnati Bengals | AFC North | 10.5 | 10.12 | 50.79 | 21.90 | 72.69 | 1.27% | **71.76** |
| Green Bay Packers | NFC North | 9.5 | 9.72 | 48.80 | 23.07 | 71.87 | 1.46% | **70.83** |
| Dallas Cowboys | NFC East | 9.5 | 9.28 | 46.60 | 24.07 | 70.67 | 1.64% | **69.51** |
| Denver Broncos | AFC West | 9.5 | 9.72 | 48.80 | 21.76 | 70.56 | 1.34% | **69.61** |
| Houston Texans | AFC South | 9.5 | 9.72 | 48.80 | 21.75 | 70.55 | 1.34% | **69.61** |
| Los Angeles Chargers | AFC West | 9.5 | 9.88 | 49.61 | 20.47 | 70.09 | 1.18% | **69.26** |
| Chicago Bears | NFC North | 9.5 | 9.28 | 46.60 | 21.93 | 68.53 | 1.45% | **67.53** |
| Jacksonville Jaguars | AFC South | 8.5 | 8.88 | 44.61 | 19.45 | 64.07 | 1.29% | **63.24** |
| Minnesota Vikings | NFC North | 8.5 | 8.50 | 42.70 | 20.72 | 63.42 | 1.51% | **62.46** |
| Pittsburgh Steelers | AFC North | 8.5 | 8.12 | 40.79 | 22.63 | 63.42 | 1.80% | **62.28** |
| Tampa Bay Buccaneers | NFC South | 8.5 | 8.21 | 41.25 | 20.42 | 61.67 | 1.55% | **60.71** |
| New Orleans Saints | NFC South | 7.5 | 7.72 | 38.80 | 20.80 | 59.60 | 1.72% | **58.58** |
| Indianapolis Colts | AFC South | 7.5 | 7.72 | 38.80 | 20.44 | 59.24 | 1.69% | **58.24** |
| New York Giants | NFC East | 7.5 | 7.50 | 37.70 | 20.94 | 58.64 | 1.80% | **57.58** |
| Washington Commanders | NFC East | 7.5 | 7.72 | 38.80 | 19.48 | 58.28 | 1.58% | **57.36** |
| Atlanta Falcons | NFC South | 7.5 | 7.12 | 35.79 | 20.12 | 55.91 | 1.83% | **54.88** |
| Carolina Panthers | NFC South | 7.5 | 7.21 | 36.25 | 19.22 | 55.47 | 1.70% | **54.53** |
| Tennessee Titans | AFC South | 6.5 | 6.43 | 32.33 | 18.80 | 51.13 | 1.90% | **50.16** |
| Las Vegas Raiders | AFC West | 6.5 | 5.99 | 30.17 | 20.08 | 50.24 | 2.21% | **49.13** |
| Cleveland Browns | AFC North | 5.5 | 5.65 | 28.44 | 19.38 | 47.81 | 2.26% | **46.73** |
| New York Jets | AFC East | 5.5 | 5.50 | 27.70 | 19.19 | 46.89 | 2.30% | **45.81** |
| Miami Dolphins | AFC East | 4.5 | 4.05 | 20.47 | 19.10 | 39.57 | 3.00% | **38.38** |
| Arizona Cardinals | NFC West | 3.5 | 3.95 | 19.93 | 16.74 | 36.67 | 2.75% | **35.66** |

## NCAA listed IPO prices

| Team | Conf/Div | Win Total | E[Wins] | On-Field EV | Off-Field EV | IPO EV | Discount % | Listed IPO ($) |
|------|----------|-----------|---------|-------------|--------------|--------|-----------|----------------|
| Texas Tech | Big 12 | 10.5 | 11.35 | 56.74 | 18.85 | 75.58 | 1.97% | **74.10** |
| Notre Dame | Independent | 11.5 | 10.80 | 53.99 | 20.45 | 74.45 | 2.28% | **72.75** |
| Miami Florida | ACC | 10.5 | 10.65 | 53.23 | 19.86 | 73.09 | 2.08% | **71.57** |
| North Dakota State | FCS-Universe | 9.5 | 8.60 | 43.00 | 27.63 | 70.63 | 0.00% | **70.63** |
| Ohio State | Big Ten | 9.5 | 10.11 | 50.55 | 19.90 | 70.45 | 2.13% | **68.95** |
| Georgia | SEC | 9.5 | 10.22 | 51.11 | 19.08 | 70.20 | 2.07% | **68.74** |
| Oregon | Big Ten | 10.5 | 10.20 | 51.00 | 19.07 | 70.07 | 2.07% | **68.62** |
| Indiana | Big Ten | 10.5 | 10.41 | 52.07 | 17.52 | 69.58 | 1.96% | **68.22** |
| Texas | SEC | 9.5 | 9.27 | 46.37 | 18.84 | 65.22 | 2.15% | **63.81** |
| Penn State | Big Ten | 8.5 | 8.99 | 44.97 | 18.93 | 63.90 | 2.19% | **62.51** |
| BYU | Big 12 | 8.5 | 8.85 | 44.25 | 17.98 | 62.23 | 2.14% | **60.90** |
| Alabama | SEC | 8.5 | 8.59 | 42.93 | 18.90 | 61.83 | 2.23% | **60.45** |
| James Madison | Sun Belt | 8.5 | 8.67 | 43.34 | 18.43 | 61.77 | 2.19% | **60.42** |
| SMU | ACC | 8.5 | 8.90 | 44.50 | 16.96 | 61.46 | 2.07% | **60.19** |
| Utah | Big 12 | 8.5 | 8.73 | 43.63 | 17.80 | 61.42 | 2.14% | **60.11** |
| LSU | SEC | 8.5 | 8.55 | 42.73 | 18.15 | 60.87 | 2.19% | **59.54** |
| Navy | AAC | 7.5 | 8.20 | 41.01 | 18.56 | 59.57 | 2.25% | **58.22** |
| Texas A&M | SEC | 8.5 | 8.35 | 41.77 | 17.71 | 59.48 | 2.18% | **58.19** |
| Liberty | CUSA | 8.5 | 8.17 | 40.84 | 18.54 | 59.38 | 2.26% | **58.04** |
| Kansas State | Big 12 | 8.5 | 8.37 | 41.84 | 17.37 | 59.21 | 2.15% | **57.93** |
| USC | Big Ten | 8.5 | 8.32 | 41.60 | 17.52 | 59.12 | 2.40% | **57.70** |
| South Florida | AAC | 8.5 | 8.17 | 40.84 | 17.85 | 58.69 | 2.21% | **57.39** |
| UNLV | Mountain West | 7.5 | 8.11 | 40.55 | 18.12 | 58.67 | 2.24% | **57.36** |
| Michigan | Big Ten | 8.5 | 7.89 | 39.45 | 19.17 | 58.63 | 2.33% | **57.26** |
| Boise State | Pac-12 | 7.5 | 7.95 | 39.74 | 18.58 | 58.32 | 2.29% | **56.99** |
| Clemson | ACC | 7.5 | 7.80 | 39.00 | 19.24 | 58.24 | 2.35% | **56.87** |
| Louisville | ACC | 8.5 | 8.12 | 40.59 | 17.55 | 58.14 | 2.20% | **56.86** |
| New Mexico | Mountain West | 7.5 | 8.15 | 40.75 | 17.31 | 58.06 | 2.18% | **56.80** |
| Army | AAC | 7.5 | 7.83 | 39.16 | 18.39 | 57.55 | 2.29% | **56.23** |
| Ole Miss | SEC | 7.5 | 8.15 | 40.75 | 16.73 | 57.48 | 2.13% | **56.25** |
| Washington | Big Ten | 7.5 | 7.95 | 39.74 | 17.47 | 57.21 | 2.21% | **55.95** |
| Oklahoma | SEC | 7.5 | 7.83 | 39.16 | 17.83 | 56.98 | 2.25% | **55.70** |
| Houston | Big 12 | 8.5 | 8.10 | 40.50 | 16.46 | 56.96 | 2.12% | **55.75** |
| Toledo | MAC | 7.5 | 7.67 | 38.34 | 17.90 | 56.25 | 2.28% | **54.97** |
| Iowa | Big Ten | 7.5 | 7.80 | 39.00 | 17.22 | 56.22 | 2.21% | **54.98** |
| Pittsburgh | ACC | 7.5 | 7.90 | 39.50 | 16.66 | 56.16 | 2.16% | **54.95** |
| Virginia | ACC | 7.5 | 7.95 | 39.74 | 16.34 | 56.08 | 2.13% | **54.88** |
| Tennessee | SEC | 7.5 | 7.50 | 37.50 | 17.78 | 55.28 | 2.29% | **54.01** |
| Memphis | AAC | 7.5 | 7.47 | 37.36 | 17.67 | 55.02 | 2.29% | **53.77** |
| UTSA | AAC | 7.5 | 7.61 | 38.06 | 16.94 | 55.00 | 2.22% | **53.78** |
| Old Dominion | Sun Belt | 7.5 | 7.56 | 37.78 | 17.01 | 54.79 | 2.23% | **53.57** |
| Hawaii | Mountain West | 7.5 | 7.35 | 36.77 | 17.48 | 54.26 | 2.29% | **53.02** |
| North Carolina State | ACC | 7.5 | 7.33 | 36.66 | 17.06 | 53.71 | 2.26% | **52.50** |
| Marshall | Sun Belt | 7.5 | 7.27 | 36.37 | 17.28 | 53.65 | 2.29% | **52.42** |
| Jacksonville State | CUSA | 7.5 | 7.27 | 36.37 | 17.16 | 53.53 | 2.28% | **52.31** |
| Miami Ohio | MAC | 7.5 | 7.20 | 36.00 | 17.39 | 53.40 | 2.30% | **52.17** |
| Tulane | AAC | 7.5 | 7.12 | 35.59 | 17.48 | 53.07 | 2.32% | **51.84** |
| Air Force | Mountain West | 7.5 | 7.05 | 35.26 | 17.73 | 52.99 | 2.35% | **51.75** |
| Louisiana | Sun Belt | 7.5 | 7.17 | 35.84 | 16.99 | 52.83 | 2.28% | **51.63** |
| East Carolina | AAC | 7.5 | 7.15 | 35.75 | 16.88 | 52.63 | 2.27% | **51.43** |
| Florida | SEC | 7.5 | 7.01 | 35.03 | 17.51 | 52.54 | 2.34% | **51.31** |
| Arizona | Big 12 | 7.5 | 7.22 | 36.10 | 16.30 | 52.40 | 2.22% | **51.24** |
| Western Kentucky | CUSA | 6.5 | 7.07 | 35.34 | 17.02 | 52.36 | 2.30% | **51.15** |
| Western Michigan | MAC | 7.5 | 6.95 | 34.73 | 17.23 | 51.97 | 2.33% | **50.76** |
| Virginia Tech | ACC | 6.5 | 6.95 | 34.74 | 17.21 | 51.95 | 2.33% | **50.74** |
| Fresno State | Pac-12 | 7.5 | 7.05 | 35.26 | 16.48 | 51.74 | 2.26% | **50.57** |
| Ohio | MAC | 6.5 | 6.88 | 34.41 | 17.19 | 51.60 | 2.34% | **50.40** |
| Troy | Sun Belt | 6.5 | 6.90 | 34.50 | 16.59 | 51.09 | 2.29% | **49.92** |
| TCU | Big 12 | 6.5 | 6.90 | 34.50 | 16.57 | 51.07 | 2.29% | **49.90** |
| Illinois | Big Ten | 7.5 | 7.05 | 35.26 | 15.65 | 50.91 | 2.19% | **49.80** |
| San Diego State | Pac-12 | 6.5 | 6.83 | 34.16 | 16.34 | 50.49 | 2.28% | **49.34** |
| Wisconsin | Big Ten | 6.5 | 6.65 | 33.23 | 17.20 | 50.42 | 2.37% | **49.23** |
| Sacramento State | FCS-Universe | 4.5 | 4.61 | 23.06 | 26.88 | 49.94 | 0.00% | **49.94** |
| Auburn | SEC | 6.5 | 6.56 | 32.78 | 17.00 | 49.77 | 2.37% | **48.59** |
| Arizona State | Big 12 | 6.5 | 6.67 | 33.34 | 16.12 | 49.46 | 2.28% | **48.33** |
| Missouri | SEC | 6.5 | 6.73 | 33.63 | 15.60 | 49.23 | 2.24% | **48.13** |
| Georgia Tech | ACC | 6.5 | 6.41 | 32.07 | 16.11 | 48.18 | 2.32% | **47.06** |
| Nebraska | Big Ten | 6.5 | 6.10 | 30.50 | 17.39 | 47.89 | 2.48% | **46.70** |
| Central Michigan | MAC | 6.5 | 6.22 | 31.10 | 16.74 | 47.84 | 2.41% | **46.69** |
| Florida State | ACC | 6.5 | 5.80 | 28.99 | 18.39 | 47.38 | 2.61% | **46.15** |
| UCLA | Big Ten | 6.5 | 6.47 | 32.36 | 14.82 | 47.18 | 2.49% | **46.00** |
| Appalachian State | Sun Belt | 5.5 | 5.99 | 29.97 | 16.93 | 46.90 | 2.46% | **45.75** |
| South Carolina | SEC | 6.5 | 6.17 | 30.84 | 15.97 | 46.81 | 2.35% | **45.71** |
| West Virginia | Big 12 | 5.5 | 6.05 | 30.27 | 16.51 | 46.78 | 2.42% | **45.65** |
| Arkansas State | Sun Belt | 5.5 | 6.23 | 31.14 | 15.61 | 46.75 | 2.31% | **45.67** |
| Oklahoma State | Big 12 | 6.5 | 6.05 | 30.26 | 16.34 | 46.60 | 2.40% | **45.48** |
| Florida International | CUSA | 6.5 | 6.10 | 30.50 | 16.06 | 46.56 | 2.37% | **45.46** |
| Kennesaw State | CUSA | 6.5 | 6.12 | 30.59 | 15.79 | 46.38 | 2.35% | **45.29** |
| California | ACC | 6.5 | 6.10 | 30.50 | 15.76 | 46.26 | 2.35% | **45.18** |
| Delaware | CUSA | 6.5 | 6.01 | 30.03 | 15.99 | 46.02 | 2.38% | **44.92** |
| Minnesota | Big Ten | 6.5 | 6.17 | 30.84 | 15.14 | 45.99 | 2.28% | **44.94** |
| Buffalo | MAC | 6.5 | 5.95 | 29.73 | 16.01 | 45.74 | 2.39% | **44.64** |
| Louisiana Tech | CUSA | 5.5 | 5.95 | 29.74 | 15.94 | 45.68 | 2.39% | **44.59** |
| Kansas | Big 12 | 5.5 | 5.95 | 29.74 | 15.85 | 45.58 | 2.38% | **44.50** |
| Texas State | Pac-12 | 6.5 | 6.01 | 30.03 | 15.51 | 45.54 | 2.34% | **44.47** |
| UCF | Big 12 | 5.5 | 6.01 | 30.05 | 15.41 | 45.45 | 2.33% | **44.39** |
| Eastern Michigan | MAC | 5.5 | 5.90 | 29.50 | 15.68 | 45.18 | 2.37% | **44.11** |
| Florida Atlantic | AAC | 5.5 | 5.95 | 29.74 | 15.37 | 45.11 | 2.34% | **44.05** |
| South Alabama | Sun Belt | 5.5 | 5.88 | 29.41 | 15.62 | 45.03 | 2.37% | **43.97** |
| Baylor | Big 12 | 6.5 | 5.82 | 29.11 | 15.87 | 44.99 | 2.40% | **43.91** |
| North Texas | AAC | 5.5 | 5.67 | 28.34 | 15.68 | 44.03 | 2.41% | **42.97** |
| Duke | ACC | 5.5 | 5.63 | 28.16 | 15.31 | 43.47 | 2.39% | **42.43** |
| Vanderbilt | SEC | 5.5 | 5.90 | 29.50 | 13.55 | 43.05 | 2.18% | **42.11** |
| Wyoming | Mountain West | 5.5 | 5.44 | 27.22 | 15.69 | 42.92 | 2.46% | **41.86** |
| Connecticut | Independent | 5.5 | 5.55 | 27.73 | 15.08 | 42.81 | 2.39% | **41.79** |
| Wake Forest | ACC | 5.5 | 5.65 | 28.23 | 14.45 | 42.68 | 2.31% | **41.69** |
| Washington State | Pac-12 | 4.5 | 5.15 | 25.75 | 16.17 | 41.92 | 2.56% | **40.85** |
| Tulsa | AAC | 5.5 | 5.39 | 26.94 | 14.94 | 41.88 | 2.40% | **40.87** |
| Temple | AAC | 5.5 | 5.33 | 26.66 | 14.90 | 41.55 | 2.41% | **40.55** |
| Northwestern | Big Ten | 5.5 | 5.45 | 27.27 | 13.79 | 41.06 | 2.28% | **40.12** |
| Maryland | Big Ten | 5.5 | 5.35 | 26.77 | 13.94 | 40.71 | 2.31% | **39.77** |
| Cincinnati | Big 12 | 5.5 | 5.10 | 25.50 | 14.90 | 40.40 | 2.45% | **39.41** |
| North Carolina | ACC | 4.5 | 4.73 | 23.63 | 16.43 | 40.06 | 2.68% | **38.99** |
| Bowling Green | MAC | 4.5 | 4.95 | 24.74 | 15.18 | 39.92 | 2.51% | **38.92** |
| Georgia Southern | Sun Belt | 4.5 | 4.90 | 24.50 | 15.14 | 39.64 | 2.52% | **38.64** |
| Coastal Carolina | Sun Belt | 4.5 | 4.85 | 24.25 | 15.38 | 39.64 | 2.55% | **38.63** |
| San Jose State | Mountain West | 4.5 | 4.90 | 24.50 | 14.96 | 39.46 | 2.50% | **38.48** |
| Kentucky | SEC | 4.5 | 4.90 | 24.50 | 14.79 | 39.29 | 2.49% | **38.31** |
| Iowa State | Big 12 | 4.5 | 4.80 | 24.00 | 15.14 | 39.13 | 2.54% | **38.14** |
| Utah State | Mountain West | 4.5 | 4.78 | 23.90 | 15.16 | 39.06 | 2.55% | **38.07** |
| Rutgers | Big Ten | 4.5 | 4.95 | 24.74 | 13.70 | 38.44 | 2.37% | **37.53** |
| Syracuse | ACC | 4.5 | 4.53 | 22.64 | 14.66 | 37.30 | 2.56% | **36.35** |
| Akron | MAC | 4.5 | 4.50 | 22.50 | 14.45 | 36.95 | 2.54% | **36.01** |
| Mississippi State | SEC | 4.5 | 4.55 | 22.73 | 13.98 | 36.71 | 2.49% | **35.79** |
| New Mexico State | CUSA | 4.5 | 4.39 | 21.94 | 14.26 | 36.20 | 2.55% | **35.28** |
| Colorado | Big 12 | 4.5 | 3.95 | 19.73 | 16.37 | 36.10 | 2.87% | **35.07** |
| Michigan State | Big Ten | 4.5 | 4.10 | 20.50 | 15.53 | 36.03 | 2.75% | **35.04** |
| Nevada | Mountain West | 4.5 | 4.20 | 21.00 | 14.35 | 35.35 | 2.61% | **34.43** |
| Arkansas | SEC | 4.5 | 3.95 | 19.73 | 14.93 | 34.66 | 2.73% | **33.72** |
| Oregon State | Pac-12 | 4.5 | 3.82 | 19.11 | 15.22 | 34.33 | 2.80% | **33.37** |
| Middle Tennessee | CUSA | 3.5 | 3.95 | 19.74 | 14.18 | 33.92 | 2.66% | **33.02** |
| Missouri State | CUSA | 4.5 | 4.01 | 20.03 | 13.70 | 33.73 | 2.59% | **32.85** |
| Colorado State | Pac-12 | 3.5 | 3.85 | 19.25 | 13.75 | 33.00 | 2.64% | **32.13** |
| Stanford | ACC | 3.5 | 3.65 | 18.23 | 14.32 | 32.55 | 2.76% | **31.65** |
| Georgia State | Sun Belt | 4.5 | 3.80 | 18.99 | 13.52 | 32.52 | 2.63% | **31.66** |
| Southern Mississippi | Sun Belt | 3.5 | 3.73 | 18.63 | 13.80 | 32.43 | 2.68% | **31.56** |
| Ball State | MAC | 3.5 | 3.61 | 18.06 | 13.56 | 31.62 | 2.69% | **30.77** |
| UL Monroe | Sun Belt | 3.5 | 3.61 | 18.06 | 12.78 | 30.84 | 2.60% | **30.04** |
| UAB | AAC | 3.5 | 3.50 | 17.50 | 13.31 | 30.81 | 2.69% | **29.98** |
| Northern Illinois | Mountain West | 3.5 | 3.35 | 16.77 | 13.89 | 30.66 | 2.80% | **29.80** |
| Rice | AAC | 3.5 | 3.50 | 17.50 | 12.96 | 30.46 | 2.65% | **29.65** |
| Kent State | MAC | 3.5 | 3.39 | 16.94 | 13.12 | 30.05 | 2.70% | **29.24** |
| Purdue | Big Ten | 3.5 | 3.17 | 15.84 | 13.04 | 28.88 | 2.77% | **28.08** |
| UTEP | Mountain West | 3.5 | 3.22 | 16.10 | 12.63 | 28.73 | 2.70% | **27.95** |
| Sam Houston State | CUSA | 3.5 | 3.12 | 15.59 | 12.93 | 28.52 | 2.77% | **27.73** |
| Boston College | ACC | 3.5 | 3.10 | 15.50 | 12.94 | 28.44 | 2.78% | **27.65** |
| Massachusetts | MAC | 2.5 | 2.85 | 14.25 | 12.50 | 26.75 | 2.82% | **26.00** |
| Charlotte | AAC | 2.5 | 2.10 | 10.50 | 11.46 | 21.96 | 3.00% | **21.30** |

## Key flags and caveats (from the model author)

1. **North Dakota State prices ~4th-highest in NCAA (~$71) almost entirely from the non-universe rule:** ~10 of its games are vs out-of-universe FCS opponents, each worth the full $2.50 uncontested (~$25 of guaranteed off-field accrual) plus $5/win. Same dynamic, smaller, for Sacramento State. If unintended, options are: (a) discount out-of-universe (OOU) games to a fixed capture, (b) scale win payments by opponent tier, or (c) accept it and let the market fade the name.
2. **OOU game counts default to 1 per FBS team** (0 for Notre Dame/USC/UCLA; 10 for NDSU/Sacramento State). Replacing these with the actual 2026 schedule counts moves each NCAA IPO by up to ~$1 to $2. `engine.py` accepts an exact 2026 schedule CSV that overrides the schedule approximation; supply it before final pricing.
3. **Brand scores are judgment inputs.** They drive only the off-field leg, which the clamp caps at $0.50 to $2.00/game, so IPO sensitivity to any single brand score is modest (under ~$4 end to end).
4. **Win totals are the market's number, vig-adjusted; no house view is layered on.** If InPlay wants margin in the IPO (issue rich), apply a uniform markup rather than distorting relative prices.
5. **Ceiling check:** max possible per share is 17 x $5 + 17 x $2.00 = **$119.00** (NFL), and 12 x $5 + 12 x $2.00 = **$84.00** (NCAA). All IPOs price well inside their ceilings.

## How this connects

- **Issuance:** these listed prices are the single-price offering level for [[primary-offering-execution]] (long-only primary raise, minted to wallets; the OMS can seed the same value as the IPO reference price, see [[t0]] §10.6).
- **Settlement / earnings:** the $5/win, $2.50/tie and $2.50/game off-field pool are the [[earnings-report]] accruals (SDMM-1), so the IPO price is literally the expected sum of every future earnings distribution.
- **Market maker:** the on-field + off-field EV that produces each IPO price is the same fair-value basis the internal market maker quotes around. Reconciling this pricing model with the MM reference-price / ESV design is an item for the `market-maker/` workstream (its working-guide process owns that; not written here).
- **Float sizing:** pricing is now concrete per team; the open float-size question (5M vs ~1M/875k) is tracked separately in [[open-questions]].
