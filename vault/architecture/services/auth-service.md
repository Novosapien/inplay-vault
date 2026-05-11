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
