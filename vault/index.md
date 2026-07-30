# InPlay Trading Challenge

> **Client:** InPlay (Edwin, Cody, Troy, Skye)
> **Status:** Components
> **Date started:** 2026-05-06

## Overview

A simulated sports equity trading platform where users trade team stocks during live NFL and college football seasons with no financial risk but real cash prizes. Currently in component deep-dive phase. Vision extracted and reviewed. **Four components now `Defined`** (Information Layer, Customer Onboarding, Referral, plus InPlay Global Website `In Design`). **Ten components** in the map (Withdrawal Flow added 2026-05-14). Audience model formalised — four audiences in [[audiences]].

## Documents

| Document | Description | Status |
|----------|------------|--------|
| [[vision]] | Product vision -- what we're building and why | Defined |
| [[audiences]] | Canonical audience definitions (4 audiences) | Defined |
| [[architecture]] | Cross-cutting technical decisions -- tech stack, infrastructure, integrations | Not started |
| [[components]] | Component map -- all major parts of the product | In progress |
| [[whats-new]] | Latest updates and changes | Rolling |
| [[product/pages/PAGES\|App Pages]] | All 21 screens — what users see, navigation flows | Living |
| [[todos]] | Open items and checklist | Rolling |

## Recent Activity

| Date | What happened |
|------|--------------|
| 2026-07-30 | **SNT-1 Synthetic Noise Taker** added to the [[market-maker/market-maker]] component (Edwin email + reference code). A second house agent: a taker-only "controlled loser" that crosses the spread so every book trades from IPO onward. Spec in [[market-maker/systems/synthetic-noise-taker]]; code in `sources/`; decisions/parameters/open-questions + session note updated per the working guide. |
| 2026-07-29 | **IPO pricing model v1.0 from Edwin** stored + processed ([[ipo-pricing-2026]]): listed IPO prices for all 32 NFL + 138 NCAA team companies, plus parameters and methodology (IPO = $5·E[Wins] + $2.50·E[Ties] + $2.50/game·capture). Source workbook safe-copied to `ipo-module/sources/`. |
| 2026-07-29 | tZERO OMS Q&A from Rob Colucci + the IPLY risk-settings matrix processed ([[29-07-2026-tZERO-rob-qa]], [[tzero-oms-risk-settings]]): IPLY carries positions overnight, account-scoped positions fixed, bid/ask driven by FIX (MM sets the market), ticker `IPTCCONH` created, Stop Wash Trades ON, price-band tiers captured; primary-issuance metrics need a dedicated cap-table stack. Resolves two 23-07 open items. |
| 2026-07-24 | Friday touchdown digested ([[24-07-2026-touchdown]]): AdMob verification kicked off (App Store ID landed 23-07) with the first SSP about to serve; Google Tag Manager + AppsFlyer-vs-Kochava MMP; release governance / OTA caps; Sport Radar media-vs-betting feed speed decision + probabilities-API blockers; trading infra mapped with historical-game simulation testing; payouts/tax-forms fallback; KYC-less app variant deferred to Sept; new Analyst Prices page. |
| 2026-07-24 | Subscription pricing + research reports folded in from two source docs into [[research-tab]]: a four-tier ladder proposed (Free / Plus $24.99 / Pro $49.99 / Elite $79.99, prices under review) and the first pre-canned report catalog supplied. |
| 2026-07-24 | Captured Jared Sapirman's written app feedback ([[jared-app-feedback-jul-2026]], 6 items); routed to [[referral/referral]], [[third-space/third-space]], [[frontend-performance]], [[trader-profile]]. Flagged Groups & Leagues, streak system and Dynamic Island as candidates. |
| 2026-07-23 | tZERO Weekly Tech Sync digested ([[23-07-2026-tZERO-weekly]]): SIM/PROD environment split, production symbology, SIM rate limiting, $1.20/share short fee, and the **IPO direct-mint decision** (bypass the Matching Engine). Aug 6 dry run / Aug 22 sim launch targeted. |
| 2026-07-22 | Touchdown digested ([[22-07-2026-touchdown]]): **subscription pricing set** ($49.99 Research / $49.99 Watch-Pro-View / $79.99 bundle); W9 tax-automation vendor for cash withdrawals (live by 29 Aug); education AI-clone persona videos; volatility-moment-vs-programmatic and SSP app-store-URL questions raised. |
| 2026-05-14 | Onboarding + Referral + Global Website session extracted ([[12-05-2026-onboarding-and-renewal-and-global-component]]). Customer Onboarding and Referral now `Defined`. InPlay Global Website `In Design`. **New components:** Withdrawal Flow (stub). **New cross-cutting concerns:** Analytics & Funnel Measurement, Cybersecurity & Data-Handling Framework. **Audience model formalised:** 4 audiences in [[audiences]] (Crypto-Savvy Sports Trader, Analytical Fan, Finance-Curious Student, Veteran Trader-Bettor). Vision Section 2 refactored to link to canonical audiences doc. |
| 2026-05-09 | Information Layer component and all 6 sub-components fully documented. Sub-component template updated with 3a/3b journey split. Vault restructured (content -> vault). Architecture skeleton created |
| 2026-05-08 | Component 1 deep-dive call -- Information / Bloomberg Terminal module. Covered discovery, game day, team pages, leaderboard, competitive app analysis (Poly Market, FanDuel, Hard Rock, Fanatics). Heavy tangent into ad monetisation and pricing model |
| 2026-05-06 | Vision workshop -- 2-hour session. Vision document extracted and reviewed. Component map created (9 components). Three audiences defined (since formalised to 4 in [[audiences]]). Cross-cutting concerns identified (Advertising, Push/CRM, Personal Dashboard) |
