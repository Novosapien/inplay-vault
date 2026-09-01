---
description: "Auth Service spec covering signup, login, JWT issuance and the Persona KYC flow, plus the open 1 September app-wide lockout"
---

# Auth Service

> **Architecture:** [[architecture]]
> **Service Overview:** [[services-overview]]
> **Status:** Draft

## Overview

Handles user registration, authentication, JWT issuance, and KYC verification via Persona.

- **Path:** `/auth/*`
- **Platform:** Cloud Run
- **Game day min-instances:** 10

## Responsibilities

- User signup (email, password, basic profile)
- Login and JWT token issuance
- JWT refresh
- KYC submission and status tracking via Persona
- Referral code input during signup (credits applied by Social Service via database)
- Auto-generated referral code on account creation

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/signup` | Create new account |
| POST | `/auth/login` | Login, returns JWT |
| POST | `/auth/refresh` | Refresh JWT token |
| GET | `/auth/me` | Get current user profile |
| PUT | `/auth/me` | Update profile |
| POST | `/auth/kyc/submit` | Initiate KYC via Persona |
| GET | `/auth/kyc/status` | Check KYC verification status |
| POST | `/auth/kyc/webhook` | Persona webhook for KYC completion |

## KYC Flow (Persona)

```
User signs up
  → Account created with status: PENDING_KYC
  → 100,000 InPlay dollars NOT yet credited

User submits KYC
  → App opens Persona embedded flow
  → User provides ID, selfie, personal details
  → Persona verifies: age 18+, real identity, no bots, US citizenship (if required)

Persona webhook fires
  → POST /auth/kyc/webhook
  → Auth Service updates user status to KYC_APPROVED or KYC_REJECTED
  → On approval:
    - Credit 100,000 InPlay dollars to trading wallet
    - Generate referral code
    - If user entered a referral code at signup, trigger referral reward
      (writes to database, Social Service picks it up)
```

## Live incidents

### 2026-09-01 · app-wide lockout, cause unknown

**Open.** Reported on the Monday touchdown ([[01-09-2026-touchdown]]) by Jared
mid-call (*"I got kicked out of the app"*) and independently by Cody from
outside the team: *"I had a few buddies text me this morning saying they were
locked out. They can't retrieve a password or a code. It's not sent to their
email."* Cody and Jared both reproduced the recovery failure.

**What is failing.** Two things at once, which is the useful detail:

1. **Sessions drop** and users cannot log back in.
2. **The recovery path fails too.** No password reset and no login code arrives
   by email, so a locked-out user has no way back in unaided.

**Cause: not identified.** Brett named the candidates and stopped there:
*"It could be a link to persona. It could be authentication. It could be
anything."* Three surfaces are in scope until one is ruled out:

| Candidate | Why it is in scope |
|---|---|
| **Persona** | The KYC flow below gates account status; a Persona-side failure can leave accounts in a state the app treats as unusable |
| **This service** | Login, JWT issuance and refresh all live here |
| **Email delivery** | The reset and code path is the second failure and may be a separate fault sharing a symptom |

⚠ **Diagnosis is running at hand-coded speed.** Novosapien's AI tooling was
suspended the same morning over an unpaid bill (see [[delivery/delivery]]), so
the team is reading code by hand. The two are not causally linked; the
suspension only sets how long the fix takes.

⚠ **Timing.** The first week of college football starts **Thursday 3 September**
with two ranked games, and Troy reported the app taking unprompted traffic even
on non-game days.

## JWT Structure

```json
{
  "userId": "uuid",
  "email": "user@example.com",
  "kycStatus": "approved",
  "iat": 1717200000,
  "exp": 1717203600
}
```

- 1 hour expiry
- Validated by API Gateway at the edge and by shared JWT middleware in each service as fallback
- Stored in Expo SecureStore on mobile, httpOnly cookie on web

## Scaling Profile

Auth spikes **before** games (login surge), not during. Pre-game: high traffic. During game: low (users already logged in). Post-game: moderate (checking results).
