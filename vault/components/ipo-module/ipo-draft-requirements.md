# InPlay IPO Draft, Business Requirements (v2)

> **Component:** [[ipo-module]]
> **Type:** Business requirements (authoritative spec for the IPO Draft primary offering + transition to secondary)
> **Version:** v2, dated 28 July 2026 (from Edwin / InPlay)
> **Source (safe copy in vault):** `sources/InPlay IPO Draft Requirements v2 (July 28 2026).pdf` (beside this doc). Also in shared `meeting-notes/`.
> **Related:** listed prices in [[ipo-pricing-2026]]; execution flow in [[primary-offering-execution]]; timing in [[ipo-scheduling]].
> **Status:** Current spec. Supersedes the 26-05 "5M float, 20% short holdback, no per-buyer cap" mechanics in [[ipo-module]] and its sub-components. Carries several internal inconsistencies flagged at the end for a v3 clean-up.

---

## Scope

Defines the technology business requirements for the IPO Draft: the initial (primary) offerings for NCAA and NFL team companies, the transition into secondary trading, share-inventory and short-inventory rules, participant trading restrictions, and market-sequencing logic. Objective: a controlled, rules-based launch and an orderly transition into secondary trading.

## 1. Market phases and inventory

**Two separate tracks, run independently.** InPlay Markets is the exclusive seller of all initial offerings.

| | NCAA | NFL |
|---|------|-----|
| Team companies | 138 | 32 |
| Shares outstanding per company | 1,000,000 | 900,000 |
| Shares available for shorting (secondary) | 1,000,000 | 900,000 |
| IPO allotment | All 1,000,000 available during the IPO | Sold across 18 one-minute windows, max 50,000 per window |
| Offering start | 22 Aug 2026, 1:00pm ET | 5 Sep 2026, 1:00pm ET (Round 1 to 9) |
| Offering end | 26 Aug 2026, 10:00pm ET, or earlier if sold out [see note] | 6 Sep 2026, 1:00pm to 6:00pm ET (Round 10 to 18), or earlier |
| Price freeze (T-3) | Wed 19 Aug 2026 | Wed 2 Sep 2026 |
| Secondary trading start | 27 Aug 2026, 9:30am ET [see note] | 7 Sep 2026, 9:30am ET |

This **supersedes** the earlier 5,000,000-share float with a 20% short holdback. New model: NCAA 1,000,000 and NFL 900,000 shares outstanding, with the full outstanding available for shorting in secondary.

### Key terms

- **Water Line:** the cumulative per-team sales cap in force for a round.
- **Pre-Buy Book:** binding limit-quantity orders at the fixed listing price, submitted before a team's window opens.
- **Guaranteed Accrual:** POOL x (out-of-universe games), the portion of a team's terminal value not contingent on game outcomes or volume competition (ties to the off-field leg in [[ipo-pricing-2026]]).

## 2. IPO Draft mechanics

During the initial offering phase, participants may **buy only**: no selling, no shorting, no participant-to-participant trades.

**NCAA track:** all team companies made available at start; a continuous five-day offering (buy-only) from 22 Aug 1:00pm ET to completion. Price frozen T-3 (19 Aug).

**NFL track:** sequential, one team at a time, alphabetical in Round 1. 50,000 shares made available per one-minute window. Scheduled across two 5-hour sessions (5 and 6 Sep). Round ordering after Round 1 reverses (reverse-alphabetical in Round 2, alternating thereafter) to symmetrize time-of-day effects.

- **Pre-Buy instant fill:** if the Pre-Buy Book at window open covers the full 50,000 allotment, it fills immediately from the book and advances to the next team without running the live window.
- **Partial:** if the Pre-Buy Book covers less than the allotment, pre-buys fill first and the remainder is available for live purchase (first-come) for the balance of the one-minute window.
- **MM completion sweep:** at window close (the earlier of the one-minute mark or a participant sellout), the Market Maker buys every remaining share to bring the window fill to exactly 50,000, then advances immediately. The sweep executes at close, not at open, so the live window stays available to participants. Example: participants buy 32,500 Arizona Cardinals; the MM buys the remaining 17,500; window closes filled at 50,000.

## 3. NFL load balancing (Water-Line mechanism)

Objective: approximately equal shares outstanding per team within each league, without sacrificing total shares sold. The Water Line replaces the originally-proposed mid-round ratchet (avoids alphabetical-order artifacts). Simulation on Popularity-Index demand: ~3.4x total volume with tighter float dispersion.

- **Round 1:** every team's allotment is 50,000.
- **MM Primary Mandate rounds (see the flag below on 10 vs 16):** every window closes filled at exactly 50,000, so cumulative sold is identical across teams (r x 50,000) and the Water Line advances 50,000 per round mechanically. Float equality through Round 10 is exact by construction.
- **After the mandate expires:** W(r+1) = min over all teams of (cumulative total shares sold) + 50,000; each team's available allotment = max(0, W(r) - cumulative sold_i), capped at 50,000; participant orders only, no MM sweep. Teams already at the line are skipped instantly.
- Zero-sale windows never reduce another team's allotment (no mid-round ratchet).
- **Termination:** evaluated from Round 11 onward only (Rounds 1 to 10 always run in full). The offering closes after the first complete round (r >= 11) in which aggregate participant fills are below 1% of aggregate available allotments. MM purchases never count toward the termination metric.
- **Terminal float equalization:** approximate equality is sufficient; no trimming or refunds at close.

## 4. Allocation and caps

- **Oversubscribed Pre-Buy Books:** allocate pro-rata by order size, rounded down to whole shares; residual shares by random draw among unfilled orders. **FIFO is expressly rejected** (it would create a latency race).
- **Per-participant cap:** 2,500 shares (5% of the 50,000 base allotment) per team per round, applied to pre-buy and live orders combined. Purpose: spread ownership, prevent single-name anchoring. This **supersedes** the earlier "no per-buyer cap."
- **Market Maker role in the primary:**
  - Exempt from the per-participant cap; no limit on shares per round.
  - **Residual only:** participant orders (pre-buy and live) fill first; the MM never competes in the pro-rata allocation of an oversubscribed book.
  - **Primary Mandate (Rounds 1 to 10):** the MM MUST purchase all allotment remaining after participant demand (the completion sweep). From Round 11 the mandate expires and the MM buys nothing in the primary.
  - **Consequence:** a guaranteed primary float of 500,000 shares per team after Round 10; a maximum MM opening inventory of 85,000,000 shares across 170 names (~$4.26B notional at current listed prices) less cumulative participant demand. MM primary purchases execute at the listed price.
  - **Unsold inventory** at offering close seeds the MM's opening inventory at the listed price.

> The MM's role here is IPO-side mechanics. The market maker's own algorithm and inventory design live in the `market-maker/` component and are governed by its working-guide process; this doc does not modify that component. The completion-sweep and Round-1-to-10 mandate should be reconciled there.

## 5. Key business rules (as stated)

**Initial offering:** NCAA begins with 1,000,000 shares outstanding, NFL with 900,000. InPlay Markets is the sole seller. Participants may only submit buy orders; no participant-to-participant selling; no short selling. A team company remains in initial-offering status until all allocated shares are sold or the applicable window closes.

**Secondary market:** buy and sell per market rules. Full outstanding is available for shorting (NCAA 1,000,000; NFL 900,000).

## Flagged inconsistencies in v2 (for a v3 clean-up)

These are internal contradictions in the source PDF, surfaced so they get resolved before build:

1. **NCAA offering end date:** section 1.1 says **26 Aug 10:00pm ET**; section 2.1 says the five-day offering runs to **28 Aug 10:00pm ET**. Two different end dates.
2. **NCAA secondary start:** section 1.1 says **27 Aug 9:30am ET**; section 5.2 says **26 Aug 9:30am ET**. These also collide with the offering-end dates above (secondary cannot start before the offering ends).
3. **MM Primary Mandate round range:** section 3 says the mandate is in force for **Rounds 1 to 16**; sections 4 and 5 say **Rounds 1 to 10** (and the "guaranteed 500,000 float after Round 10" figure equals 10 x 50,000, which implies 10). The completion sweep is separately described as "Rounds 1 to 18." The 10 / 16 / 18 references need reconciling.
4. **Secondary shorting labels (section 5.2):** items 3 and 4 both read "NFL team company," at 1,000,000 and 900,000 respectively. Item 3 (1,000,000) is almost certainly NCAA.
5. **NFL scheduled offering time:** the text says "8 hours," but the table sums to 10 hours (two 5-hour sessions), against the ~10-hour worst-case budget.

## How this connects

- **Pricing:** the listed price for every window and pre-buy is fixed by [[ipo-pricing-2026]] (frozen T-3). The "~$4.26B notional across 85M MM shares" checks out against the ~$50 average listed price.
- **Execution:** [[primary-offering-execution]] is the buy engine that runs these windows, the pre-buy book, the caps, and the completion sweep.
- **Scheduling:** [[ipo-scheduling]] holds the window calendar and price-freeze dates.
- **Settlement:** the guaranteed-accrual and terminal-value language ties to the [[earnings-report]] accruals that the IPO price capitalises.
- **Market maker:** the completion sweep, the Rounds 1 to 10 mandate, and the 85M-share opening inventory are inputs to the `market-maker/` workstream (its working-guide process owns that build).
