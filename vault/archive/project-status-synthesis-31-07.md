# InPlay Project Status — Working Synthesis (31 Jul 2026)

Source: 9 research agents — 5 over the vault, 4 over the repos. This file is the
working source for the client-facing deck. Client-facing content only in the
deck; the "Internal only" section stays out of it.

## Launch calendar — per IPO Requirements v2 (28 Jul, gospel)

- NCAA price freeze: Wed 19 Aug
- NCAA IPO: opens Sat 22 Aug 1:00pm ET; ends 26 Aug 10pm ET (§1.1) OR runs to
  28 Aug 10pm ET (§2.1) — the document contradicts itself (= open item E25)
- NCAA secondary trading opens: 27 Aug 9:30am ET (§1.1) OR 26 Aug 9:30am ET
  (§5.2) — same E25 contradiction; one reading opens secondary before the
  primary closes. Deck shows "26–27 Aug, pending InPlay reconciliation".
- NFL price freeze: Wed 2 Sep; NFL IPO: 5–6 Sep, 1–6pm ET, 18 one-minute
  rounds; NFL secondary opens: 7 Sep 9:30am ET (consistent throughout)
- "Trading live 22 Aug" = the IPO draft opening. Hard dates: trading + IPO
  module by 22 Aug; MM quoting by NCAA secondary open (26–27 Aug).
- The 17-07 "29 Aug" figure is superseded by the v2 requirements doc.
- Minor v2 erratum: §5.2 says "NFL" for both shorting figures (1M / 900k);
  one should read NCAA.
- Shares: 1,000,000 per NCAA team company; 900,000 per NFL. MM buys all unsold.
- ~10k users targeted at IPO launch; Edwin committing $1M Aug + $2M Sep acquisition

## Status matrix

| # | Component | Spec state | Build state | Proposed phase |
|---|-----------|-----------|-------------|----------------|
| 1 | Customer onboarding + KYC | Locked 17-06 | LIVE — Persona signed, 83 approved KYCs, flow in app | Shipped; app live on the Apple App Store since ~22-07 |
| 2 | Referral programme | Deep, changelog to 24-06 | LIVE via challenge website since ~4 Jul | Shipped; phase-2 items (prize criteria, eligibility rules) open |
| 3 | Challenge website | Full spec | LIVE; legal pages pending counsel; OG image + brand-preview tool outstanding | Shipped; content/legal pass |
| 4 | Global website | Decision log | DEPLOYED; placeholder pages: platform, methodology, investors, 4 legal | Shipped; content pass pre-launch |
| 5 | Consumer app (product pages/information layer) | Deep on Discover/Watch Mode | Late-stage: buildNumber 30, OTA pipeline, 309 commits in Jul. Mock prices until trading service lands | Pre-launch critical |
| 6 | Trading execution (tZERO) | Hub current to 24-07 | Infra map complete 23-07; Go FIX gateway works (2 of 4 sessions); remaining: cancel, cancel-replace, notifications | Pre-launch critical — 22 Aug |
| 7 | IPO module | 6 sub-components defined; share counts settled 29-07 (900k NFL / 1M NCAA, MM buys all unsold) | IPO draft screens in app; primary-plane execution with tZERO | Pre-launch critical — 22 Aug |
| 8 | Market maker | v1.3 spec gospel; deepest working docs | Most active repo: valuation + position engines built (235 tests), quoting (Ch 5) in build now; market state, venue sync, poller unbuilt | Pre-launch critical — quoting by ~26 Aug |
| 9 | Sportradar data platform | t0.md deep; sportradar.md missing | DEPLOYED in production, 18 routers, live worker deployed but idle (sim host, no live game IDs) | Shipped; live-game switch-on is a launch task |
| 10 | Education | Reset 22-06 to card library | 16 beginner modules live in build 17-07; 36 videos rendered; intermediate/expert have placeholder timings | Pre-launch: beginner tier; rest phased |
| 11 | Advertising | Playbook concrete; AppLovin MAX confirmed 17-07 | House ads in app; SSP onboarding BLOCKED on App Store approval | Pre-launch (Edwin's #2); calibration for first 3–6 months |
| 12 | Earnings report | Deepest decomposition (5 sub-components, acceptance criteria) | NO CODE FOUND anywhere | Launch window: first cycle needed opening weeks of season |
| 13 | Withdrawal / payouts | Stub, 11 unknowns; provider unsigned | Not built | Launch remainder — accepted worst case: visible owed amounts, delayed payout, manual Zelle/wire interim |
| 14 | Third space (chat/community) | Full May spec | Deferred indefinitely 06-07; Discord alternative discussed 10-07, unresolved | Post-launch, threshold-gated |
| 15 | Admin panel + API | n/a (internal) | DEPLOYED in production; vault docs + CI viewer live | Shipped (internal tooling) |
| 16 | Research tab (subscription) | Defined; pricing 99c → $14.99/mo | Pre-canned reports demoed in app 13-07 | May slip past launch by design |
| 17 | Watch Mode | Candidate sub-component, no own doc | Built through July standups; custom Gamecast (InPlay-owned IP) | In app for launch; monetisation parked |

## Cross-cutting blockers (client-facing)

1. ~~Apple App Store review~~ RESOLVED: the app went live on the Apple App
   Store as "InPlay Challenge" between 20-07 and 23-07 (37 downloads on 22-07,
   OTA updates rolling). Remaining store blocker: Google Play listing
   (screenshots + frozen build with Hasan/Troy, 23-07) and the gambling
   classification risk. SSP onboarding unblocks now the store listing exists.
2. tZERO scope question ("what does tZERO manage?") still marked Open — BLOCKING
   in architecture/open-questions.md:18 (partly answered 10-06, never reconciled).
3. Payment provider unsigned (payouts).
4. tZERO account permission (T1) gates MM venue work; ~9 open questions with tZERO.
5. Sportradar production entitlement + quota (4 open questions).
6. Legal: NFL/NCAA imagery licensing artifact absent; real-securities vs simulated
   copy inconsistency (App Store readiness report); challenge-site legal pages
   pending counsel; two-house-accounts wash-trade/FINRA question (E33/T13).

## Date conflicts to resolve with George

- NCAA secondary open: 26/27 Aug (MM vault) vs 29 Aug (17-07). MM card also flags
  E25: requirements doc itself contradicts (26 vs 27/28 Aug).
- First NFL game: ~7 Sep (MM decisions) vs ~9 Sep (plan.md) vs 2 Sep (June digest).
- "Trading live 22 Aug" vs "secondary opens 29 Aug" — IPO close vs secondary open?

## Internal only — do NOT put in the client deck

- inplay-education-videos has NO git remote; 36 rendered videos exist only on
  this laptop. Push to origin urgently.
- inplay-admin-api/infrastructure/terraform.production.tfvars holds plaintext
  production secrets on disk (not committed). Move to Secret Manager.
- Trading-Challenge- branch divergence: live site reflects main as of 25 Jun;
  55 newer commits on client-imagery-demo not deployed. Needs reconciliation.
- inplay-fix-gateway-go: untouched 2 months, missing IOI + Drop Copy sessions,
  Dockerfile broken (golang:1.23 vs go 1.26). On the MM critical path.
- Python fix-gateway is an archived prototype (main.py is 13 comment lines);
  its value is docs + demo dashboard only.
- Sportradar prod worker points at simulation host; LIVE_GAME_IDS empty —
  deliberate, but must flip before first live game.
- Admin API CORS fix sits unmerged on fix/cors-pwa-origins.
- Test coverage near zero on admin panel/API and onboarding-referral service.
- onboarding-referral: KYC endpoints stubbed (501 webhook), admin key auth,
  CORS *, single squashed commit. NOTE: app + challenge site use the broker —
  verify which service actually performs Persona KYC in production.
- product/pages/ folder stale since 17-05; superseded in practice by component
  sub-component docs. Decide: deprecate or refresh.
- Vault currency: component docs current to ~29 Jun; July touchdowns undigested
  (01/06/08/10-07 raw); digest branch open. Deck must use July truths from
  transcripts, not stale component docs.

## Deck outline (proposed)

1. Where we are — one-slide summary: shipped / in build / not started
2. The launch calendar — IPO windows, secondary open, first games
3. Shipped and live — onboarding+KYC, referral, websites, data platform, admin
4. The app — late-stage, App Store review status, what's mocked until trading lands
5. Trading + IPO + market maker — the critical path to 22 Aug, what's built, what remains
6. Advertising + education — pre-launch state
7. Launch remainder — notifications, tax forms, payouts (with agreed interim rail)
8. Deliberately after launch — chat/community, research tab AI tier, MM ops UI,
   season-end settlement, KYC-less academic variant, NBA challenge (late Oct)
9. Open decisions we need from InPlay — date reconciliation, E27 opening position,
   E24 mandate rounds, payment provider, legal clearances
10. Next 4 weeks — week-by-week plan to 29 Aug
