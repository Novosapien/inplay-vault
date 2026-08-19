---
description: "Session log, 2026-07-30 — intake of Edwin's SNT-1 Synthetic Noise Taker: a taker-only controlled loser that subsidises liquidity, its config and open questions"
---

# 2026-07-30, SNT-1 Synthetic Noise Taker intake

> **Who:** Novosapien (AI session) processing Edwin's email
> **Type:** research / intake
> **Refs:** Edwin email 30-07-2026; `sources/snt1_noise_taker.py`; [[market-maker/systems/synthetic-noise-taker]]

## What we did

- Processed Edwin's email introducing **SNT-1**, a second house agent alongside the Market Maker, and stored his spec-quality reference implementation (`sources/snt1_noise_taker.py`, ~349 lines, parses clean).
- Created the system doc [[market-maker/systems/synthetic-noise-taker]] and registered SNT-1 in the hub Systems table.
- Logged the design decisions ([[market-maker/decisions]]), the full config ([[market-maker/parameters]], all 🟡), and the open items ([[market-maker/open-questions]] E17, E18, N15, N16).

## What we learned

- SNT-1 is a **taker-only controlled loser**: it crosses the spread with Poisson-timed, log-normal-sized, 50/50 noise so every book trades from IPO onward. Its spread cost is the deliberate **liquidity subsidy**.
- It is off-field-neutral by construction: `participant_side = false` means its prints against the MM are excluded from the $2.50 off-field split under the existing >= 1-participant-side rule. **No spec amendment needed** (Edwin confirmed).
- The realism layer is **disposition-effect** profit-taking: profit tilts P(flatten) 0.50 -> 0.65; losers ride at 50/50; conditions only on own cost basis vs mid (no book/participant data), so it stays uninformed.
- Determinism is already baked in (single seeded RNG), matching our working-guide ground rule.

## What went wrong / got stuck

- Nothing blocking. The pasted code arrived with shell-escaped `!=` (`\!=`); fixed to `!=` and verified the file parses.

## Decisions made *(mirrored into [[market-maker/decisions]])*

- SNT-1 in scope as a second house agent; controlled-loser design; off-field exclusion needs no amendment; v1.0 config locked (🟡); gateway account flags set; two tuning levers flagged.

## Questions opened / closed *(mirrored into [[market-maker/open-questions]])*

- Opened: **E17** (SNT-1 x MM interaction during Primary Mandate rounds, Edwin's flagged question), **E18** (tuning levers + team_weight feed), **N15** (build the ExchangeAdapter + gateway flags), **N16** (five production-hardening tasks).

## Next

- Answer **E17** with Edwin (does SNT-1 run during the primary, and how it interacts with the MM completion sweep) on the next MM call, and confirm the `team_weight` feed from the popularity/EAV model. Then scope N15/N16 into the build plan.
