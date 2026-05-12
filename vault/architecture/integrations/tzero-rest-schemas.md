# tZERO REST API -- Schema Reference

> **Source:** [tZERO API Explorer](https://apidocs.tzero.com/docs/explorer#/)
> **Date:** 2026-05-12
> **Integration doc:** [[t0]]
>
> Schemas extracted from the API explorer. Enum values marked with ⚠️ need confirmation from tZERO -- the explorer renders them dynamically and couldn't be scraped.

---

## Table of Contents

1. [Common / Error Schemas](#1-common--error-schemas)
2. [Authentication](#2-authentication)
3. [Onboarding -- Accounts & Investors](#3-onboarding----accounts--investors)
4. [KYC](#4-kyc)
5. [Financial Info](#5-financial-info)
6. [Trusted Contact](#6-trusted-contact)
7. [Investments](#7-investments)
8. [Bank Accounts & Transfers](#8-bank-accounts--transfers)
9. [Balance](#9-balance)
10. [Markets](#10-markets)
11. [Trading](#11-trading)
12. [Enum Types](#12-enum-types)

---

## 1. Common / Error Schemas

### ErrorResponse

Error response body for validation and business-rule failures. Contains a list of errors; each item has code, message, and optional field (JSON path).

```json
{
  "errors": [ErrorItem]
}
```

### ErrorItem

```json
{
  "code": "string",
  "message": "string",
  "field": "string",          // JSON path to the field that caused the error
  "details": {}               // nullable, additional context
}
```

### Message

Generic response wrapper.

```json
{
  "code": "string",           // required
  "data": {},                 // required
  "message": "string"         // required
}
```

---

## 2. Authentication

### TokenRequest

```json
{
  "clientId": "string",       // required
  "clientSecret": "string"    // required
}
```

### TokenResponse

```json
{
  "accessToken": "string",    // required -- Bearer token for Authorization header
  "expiresIn": "integer",     // required -- seconds until expiry (3600 = 1 hour)
  "refreshToken": "string"    // optional -- use with POST /auth/v1/api/refresh
}
```

**Usage:**
```
POST /auth/v1/api/token
Headers: x-apikey: {your-api-key}
Body: { "clientId": "...", "clientSecret": "..." }

→ Returns accessToken (valid 1 hour)
→ All subsequent requests: Authorization: Bearer {accessToken}
```

---

## 3. Onboarding -- Accounts & Investors

### CreateIndividualAccountRequest

```json
{
  "transactionId": "string",                  // required -- idempotency key
  "investor": InvestorRequest,                // required
  "optOutOfTrustedContact": "boolean",        // optional
  "investmentProfile": InvestmentProfile,     // nullable
  "trustedContact": AccountTrustedContact     // nullable
}
```

### InvestorRequest

```json
{
  "agreement": TermsAcceptRequest,            // required
  "email": "string",                          // required
  "firstName": "string",                      // required
  "middleName": "string",                     // optional
  "lastName": "string",                       // required
  "citizenshipCountry": "string",             // optional (ISO country code)
  "taxCountry": "string",                     // optional
  "dateOfBirth": "string",                    // required (YYYY-MM-DD)
  "employment": EmploymentRequest,            // optional
  "physicalAddress": AddressRequest,          // required
  "mailingAddress": AddressRequest,           // nullable
  "phoneNumbers": [PhoneNumberRequest],       // optional
  "governmentIdentifiers": [GovernmentIdentifierRequest]  // optional
}
```

### TermsAcceptRequest

```json
{
  "acceptedAccountsTermsAndCondition": "boolean",  // required
  "termsAcceptedAt": "string",                     // optional (ISO timestamp)
  "eSignatureFullName": "string"                   // required
}
```

### InvestmentProfile

```json
{
  "investmentObjective": "InvestmentObjective",    // required (enum)
  "tradeIlliquidSecurities": "boolean"             // required
}
```

### EmploymentRequest

```json
{
  "employmentStatus": "EmploymentStatus",    // required (enum)
  "employerName": "string",                  // optional
  "occupation": "string"                     // optional
}
```

### AddressRequest

```json
{
  "street": "string",              // required
  "street2": "string",             // optional
  "street3": "string",             // optional
  "street4": "string",             // optional
  "street5": "string",             // optional
  "unit": "string",                // optional
  "city": "string",                // required
  "stateOrProvince": "string",     // required
  "postalCode": "string",          // required
  "country": "string"              // required (ISO country code)
}
```

### PhoneNumberRequest

```json
{
  "countryCode": "string",          // optional (e.g., "1" for US)
  "countryCodeAlpha": "string",     // optional (e.g., "US")
  "nationalNumber": "string",       // optional
  "ext": "string",                  // optional
  "type": "PhoneNumberType"         // optional (enum)
}
```

### GovernmentIdentifierRequest

```json
{
  "type": "GovernmentIdentifierType",  // optional (enum)
  "country": "string",                // optional
  "identifier": "string"              // optional (e.g., SSN, passport number)
}
```

### UpdateInvestorRequest

```json
{
  "transactionId": "string",           // required
  "investor": InvestorUpdateRequest     // required
}
```

### InvestorUpdateRequest

Update payload. Notes from tZERO docs:
- Email cannot be changed after account creation (if provided it may be rejected)
- `dateOfBirth` when provided: validated for format, not future, not older than 120y, min age 18
- `firstName`/`lastName` when provided must not be blank
- `phoneNumbers` uses replace semantics (provide full desired set)
- `governmentIdentifiers` uses replace semantics
- Country/residence derived from `physicalAddress.country` only

```json
{
  "firstName": "string",               // optional
  "middleName": "string",              // optional
  "lastName": "string",                // optional
  "citizenshipCountry": "string",      // optional
  "taxCountry": "string",              // optional
  "dateOfBirth": "string",             // optional (YYYY-MM-DD)
  "employment": EmploymentRequest,     // optional
  "physicalAddress": AddressRequest,   // nullable
  "mailingAddress": AddressRequest,    // nullable
  "phoneNumbers": [PhoneNumberRequest],           // optional (replaces all)
  "governmentIdentifiers": [GovernmentIdentifierRequest]  // optional (replaces all)
}
```

### AccountResponse

```json
{
  "id": "string",                       // account UUID
  "type": "string",                     // account type
  "status": "string",                   // account status
  "createdTs": "string",                // ISO timestamp
  "investors": [InvestorResponse],
  "optOutOfTrustedContact": "boolean",
  "trustedContact": TrustedContactDetails,  // nullable
  "transactionId": "string"
}
```

### InvestorResponse

```json
{
  "type": "string",
  "id": "string",
  "email": "string",
  "firstName": "string",
  "middleName": "string",
  "lastName": "string",
  "citizenshipCountry": "string",
  "dateOfBirth": "string",
  "employment": EmploymentResponse,       // nullable
  "physicalAddress": AddressResponse,     // nullable
  "mailingAddress": AddressResponse,      // nullable
  "phoneNumbers": [PhoneNumberResponse],
  "governmentIdentifiers": [GovernmentIdentifierResponse]
}
```

### InvestorUpdateResponse

```json
{
  "investor": InvestorResponse,
  "transactionId": "string"
}
```

### AddressResponse

```json
{
  "id": "string",
  "street": "string",
  "street2": "string",
  "street3": "string",
  "street4": "string",
  "street5": "string",
  "unit": "string",
  "city": "string",
  "stateOrProvince": "string",
  "postalCode": "string",
  "country": "string",
  "createdTs": "string",
  "modifiedTs": "string"
}
```

### PhoneNumberResponse

```json
{
  "id": "string",
  "countryCode": "string",
  "countryCodeAlpha": "string",
  "nationalNumber": "string",
  "ext": "string",
  "type": "PhoneNumberType",
  "createdTs": "string",
  "modifiedTs": "string"
}
```

### GovernmentIdentifierResponse

```json
{
  "id": "string",
  "type": "GovernmentIdentifierType",
  "country": "string",
  "identifier": "string",
  "createdTs": "string",
  "modifiedTs": "string"
}
```

### EmploymentResponse

```json
{
  "employmentStatus": "EmploymentStatus",
  "employerName": "string",
  "occupation": "string"
}
```

---

## 4. KYC

### TriggerKycRequest

```json
{
  "transactionId": "string"    // required
}
```

### KycResponse

```json
{
  "status": "string",         // KYC verification status
  "id": "string",             // KYC record ID
  "createdTs": "string",
  "modifiedTs": "string",
  "docUrl": "string",         // URL for KYC document/flow
  "qrMessage": "string",      // QR code content for mobile verification
  "docStatus": "string"       // document verification status
}
```

### PostKycResponse

```json
{
  "userId": "string",
  "kycResult": KycResponse,
  "transactionId": "string"
}
```

---

## 5. Financial Info

### PatchFinancialInfoRequest

All fields optional except transactionId; only provided fields are updated.

```json
{
  "transactionId": "string",    // required
  "netWorth": "number",         // optional
  "annualIncome": "number"      // optional
}
```

### FinancialInfoResponse

```json
{
  "accountId": "string",
  "netWorth": "number",
  "annualIncome": "number",
  "annualIncomeLastChangedTs": "string",
  "transactionId": "string"
}
```

---

## 6. Trusted Contact

### TrustedContactRequest

```json
{
  "transactionId": "string",               // required
  "email": "string",                       // required
  "firstName": "string",                   // required
  "middleName": "string",                  // optional
  "lastName": "string",                    // required
  "physicalAddress": TrustedContactAddress, // required
  "phoneNumber": "string"                  // optional
}
```

### TrustedContactResponse

```json
{
  "trustedContact": TrustedContactDetails,
  "transactionId": "string"
}
```

### TrustedContactDetails

```json
{
  "id": "string",
  "email": "string",
  "firstName": "string",
  "middleName": "string",
  "lastName": "string",
  "physicalAddress": TrustedContactAddress,
  "phoneNumber": "string"
}
```

### TrustedContactAddress

```json
{
  "street": "string",
  "street2": "string",
  "city": "string",
  "stateOrProvince": "string",
  "postalCode": "string",
  "country": "string"
}
```

### AccountTrustedContact

Used inline during account creation.

```json
{
  "email": "string",                        // required
  "firstName": "string",                    // required
  "middleName": "string",                  // optional
  "lastName": "string",                    // required
  "physicalAddress": TrustedContactAddress, // required
  "phoneNumber": "string"                  // required
}
```

---

## 7. Investments

### Asset

```json
{
  "assetId": "string",
  "symbol": "string",                      // e.g., "IGBI" for InPlay Green Bay Inc.
  "assetName": "string",
  "assetDescription": "string",
  "assetType": CodeLabelDescription,
  "requiresAccreditation": "boolean",
  "pricePerShare": "number",
  "minimumInvestment": "number",
  "maximumInvestment": "number",
  "status": "string",
  "offeringCloseDate": "string",
  "offering": CodeLabelDescription,
  "countries": ["string"],
  "paymentTypes": ["string"]
}
```

### AssetsResponse

```json
{
  "assets": [Asset]                        // required
}
```

### CodeLabelDescription

```json
{
  "code": "string",
  "label": "string",
  "description": "string"
}
```

### CreateInvestmentRequest

```json
{
  "accountId": "string",                   // required
  "transactionId": "string",              // required
  "amount": "number",                     // required
  "numberOfShares": "number",             // optional
  "regCFInvestmentTermsAccepted": "boolean"  // optional
}
```

### UpdateInvestmentRequest

```json
{
  "accountId": "string",                   // required
  "investmentId": "string",               // required
  "amount": "number",                     // optional
  "numberOfShares": "number",             // optional
  "paymentType": "string",                // optional
  "bankAccountId": "string",              // optional
  "paymentId": "string",                  // optional
  "transactionId": "string",              // required
  "selfAttestedAccreditationAnswer": "string"  // optional
}
```

### CreatePaymentRequest

Only WIRE and ACH payment types supported.

```json
{
  "accountId": "string",                   // required
  "paymentType": "PaymentTypeEnum",        // required (enum)
  "bankAccountId": "string",              // optional
  "transactionId": "string"               // required
}
```

### SubmitInvestmentRequest

```json
{
  "accountId": "string",                   // required
  "transactionId": "string"               // required
}
```

### CancelInvestmentRequest

```json
{
  "accountId": "string",                   // required
  "transactionId": "string"               // required
}
```

### InvestmentSignatureRequest (Agreement)

```json
{
  "accountId": "string",                   // required
  "transactionId": "string",              // required
  "userSignature": "string",              // required
  "version": "string"                     // required
}
```

### InvestmentDetails / InvestmentDTO

Same shape, used in different contexts (detail vs list).

```json
{
  "investmentId": "string",
  "amount": "number",
  "numberOfShares": "number",
  "costBasis": "number",
  "fundedAmount": "number",
  "status": "InvestmentStatusEnum",        // enum
  "assetId": "string",
  "transactionId": "string",
  "paymentType": "string",
  "createdTs": "string",
  "modifiedTs": "string"
}
```

### AgreementDTO

```json
{
  "id": "string",
  "userId": "string",
  "assetId": "string",
  "signedTs": "string",
  "documentId": "string",
  "status": "string",
  "expired": "boolean",
  "createdTs": "string",
  "createdBy": "string",
  "modifiedTs": "string",
  "modifiedBy": "string",
  "userSignature": "string",
  "subscriptionType": "string",
  "documentVersion": "string"
}
```

---

## 8. Bank Accounts & Transfers

### CreateBankAccountRequest

```json
{
  "accountNumber": "string",               // required
  "routingNumber": "string",               // required
  "accountType": "string",                 // required (e.g., "CHECKING", "SAVINGS")
  "bankName": "string",                    // required
  "bankOwnerName": "string",               // required
  "transactionId": "string",              // required
  "partnerVerified": "boolean",            // required
  "verificationResult": "string"           // optional
}
```

### BankAccountDetails

```json
{
  "bankAccountId": "string",
  "bankName": "string",
  "maskedAccountNumber": "string",         // e.g., "****1234"
  "accountType": "string",
  "status": "string",
  "transactionId": "string"
}
```

### CreateBankTransferRequest

```json
{
  "transactionId": "string",              // required
  "amount": "number",                     // required
  "transactionType": "string",            // required (e.g., "DEPOSIT", "WITHDRAWAL")
  "currency": "string"                    // optional (defaults to USD)
}
```

### CreateBankTransferResponse

```json
{
  "transactionId": "string",              // required
  "transferId": "string",                 // required
  "amount": "number",                     // required
  "transactionType": "string",            // required
  "bankAccountId": "string",              // required
  "currency": "string"                    // optional
}
```

---

## 9. Balance

### AccountBalanceResponse

```json
{
  "accountBalances": BalanceDetails
}
```

### BalanceDetails

```json
{
  "accountId": "string",
  "fiat": FiatBalance,
  "positions": [PositionBalance]
}
```

### FiatBalance

```json
{
  "currency": "string",                    // e.g., "USD"
  "totalAmount": "number",
  "availableWithdrawalAmount": "number",
  "pendingDepositAmount": "number",
  "pendingWithdrawalAmount": "number"
}
```

### PositionBalance

```json
{
  "symbol": "string",
  "quantity": "number",
  "tradeable": "boolean",
  "costBasis": CostBasis
}
```

### CostBasis

```json
{
  "currency": "string",                    // required
  "totalQuantity": "number",              // required
  "totalCost": "number",                  // required
  "averageCost": "number"                 // required
}
```

---

## 10. Markets

### ScheduleResponse

```json
{
  "dto": [MarketSchedule],                // list of schedules or null
  "errors": [ScheduleError]              // list of errors or null
}
```

### MarketSchedule

Pre-market, market, and post-market hours for a single trading day.

```json
{
  "date": "string",                        // required (YYYY-MM-DD)
  "zoneId": "string",                     // required (e.g., "America/New_York")
  "description": "string",                // optional
  "preMarketHours": SubSchedule,          // nullable
  "marketHours": SubSchedule,             // nullable
  "postMarketHours": SubSchedule          // nullable
}
```

### SubSchedule

```json
{
  "open": "string",                        // required (HH:MM:SS)
  "close": "string"                       // required (HH:MM:SS)
}
```

### ScheduleError

```json
{
  "code": "string",
  "message": "string"
}
```

### SymbolData

Market data snapshot for a symbol.

```json
{
  "symbol": "string",
  "high": "number",
  "low": "number",
  "open": "number",
  "volume": "number",
  "lastPrice": "number",
  "lastQuantity": "number",
  "prevClosePx": "number",
  "bidPrice": "number",
  "bidPriceRate": "number",
  "bidQuantity": "number",
  "bidQtyBookTotal": "number",
  "askPrice": "number",
  "askPriceRate": "number",
  "askQuantity": "number",
  "askQtyBookTotal": "number",
  "timestamp": "string"
}
```

### PriceHistory

```json
{
  "symbol": "string",
  "date": "string",                        // YYYY-MM-DD
  "open": "number",
  "high": "number",
  "low": "number",
  "close": "number",
  "volume": "number"
}
```

---

## 11. Trading

### CreateOrderRequest

```json
{
  "symbol": "string",                      // required (e.g., "IGBI")
  "assetId": "string",                    // required
  "side": "string",                        // required ("BUY" or "SELL")
  "timeInForce": "string",                // required ("DAY", "GTC", "GTD")
  "expireDate": "string",                 // optional (required for GTD)
  "type": "string",                        // required ("LIMIT")
  "quantity": "number",                    // required
  "limitPrice": "number",                 // required (4 decimal places)
  "transactionId": "string"               // required (idempotency key)
}
```

### CreateOrderResponse

```json
{
  "transactionId": "string",
  "id": "string",                          // order ID
  "accountId": "string",
  "symbol": "string",
  "assetId": "string",
  "side": "string",
  "quantity": "number",
  "type": "string",
  "limitPrice": "number",
  "timeInForce": "string",
  "status": "string",
  "expireTs": "string",
  "createdTs": "string",
  "modifiedTs": "string",
  "fee": "number"
}
```

### OrderResponse

Full order detail with execution history.

```json
{
  "accountId": "string",                   // required
  "id": "string",                          // required
  "symbol": "string",                      // required
  "side": "string",                        // required
  "type": "string",                        // required
  "limitPrice": "number",                 // required
  "quantity": "number",                    // required
  "filledQuantity": "number",             // required
  "leavesQuantity": "number",             // required
  "averagePrice": "number",               // required
  "timeInForce": "string",                // required
  "expireTs": "string",                   // optional
  "estimatedFee": "number",               // required
  "estimatedSubtotal": "number",          // optional
  "estimatedGrandTotal": "number",        // required
  "cumulativeFee": "number",              // optional
  "cumulativeSubtotal": "number",         // optional
  "cumulativeGrandTotal": "number",       // optional
  "status": "string",                     // required
  "createdTs": "string",                  // optional
  "modifiedTs": "string",                 // optional
  "assetClass": "string",                 // required
  "executionHistory": [OrderExecution]     // optional
}
```

### OrderExecution

Individual fill/event within an order's lifecycle.

```json
{
  "executionTs": "string",                 // required
  "affectedQuantity": "number",            // optional
  "fillQuantity": "number",               // optional
  "fillPrice": "number",                  // optional
  "cumulativeQuantity": "number",          // required
  "executionResult": "string",             // required
  "leavesQuantity": "number",             // required
  "averagePrice": "number",               // required
  "text": "string",                        // optional (rejection reason, etc.)
  "fee": "number",                         // optional
  "subtotal": "number",                   // optional
  "grandTotal": "number"                  // optional
}
```

### OrdersListResponse

```json
{
  "orders": [OrderResponse]               // required
}
```

### CancelOrderResponse

```json
{
  "transactionId": "string",              // required
  "id": "string",                          // required (order ID)
  "status": "string"                      // required
}
```

### FeeResponse

```json
{
  "fee": "number",                         // required
  "feeFormatted": "string",               // required (e.g., "$1.50")
  "status": "string"                      // required
}
```

---

## 12. Enum Types

> ⚠️ **The API explorer renders enum values dynamically via JavaScript.** The exact values could not be scraped. The values below are inferred from field context, tZERO documentation patterns, and industry standards. **Confirm all enum values with tZERO before implementation.**

### InvestmentObjective

Case-insensitive when deserializing. Array of 3 values.

```
Likely values:
  "GROWTH"
  "INCOME"
  "SPECULATION"
```

### EmploymentStatus

Case-insensitive when deserializing. Array of 5 values.

```
Likely values:
  "EMPLOYED"
  "SELF_EMPLOYED"
  "UNEMPLOYED"
  "RETIRED"
  "STUDENT"
```

### PhoneNumberType

Example from docs: `"PRIMARY"`. Array of 2 values.

```
Likely values:
  "PRIMARY"
  "SECONDARY"
```

### GovernmentIdentifierType

Example from docs: `"TIN"`. Array of 4 values.

```
Likely values:
  "TIN"          (Tax Identification Number / SSN)
  "PASSPORT"
  "DRIVERS_LICENSE"
  "NATIONAL_ID"
```

### InvestmentStatusEnum

Array of 7 values.

```
Likely values:
  "CREATED"
  "PENDING"
  "SUBMITTED"
  "FUNDED"
  "COMPLETED"
  "CANCELLED"
  "REJECTED"
```

### PaymentTypeEnum

Only WIRE and ACH are allowed. Array of 2 values.

```
Confirmed values:
  "WIRE"
  "ACH"
```

---

## Endpoint-to-Schema Mapping

Quick reference: which schemas each endpoint uses.

### Authentication

| Method | Path | Request | Response |
|--------|------|---------|----------|
| POST | `/auth/v1/api/token` | TokenRequest | TokenResponse |
| POST | `/auth/v1/api/refresh` | (refresh token in body) | TokenResponse |

### Onboarding

| Method | Path | Request | Response |
|--------|------|---------|----------|
| POST | `/pi/v1/accounts/individual` | CreateIndividualAccountRequest | AccountResponse |
| PUT | `/pi/v1/accounts/{accountId}/users/{userId}` | UpdateInvestorRequest | InvestorUpdateResponse |
| GET | `/pi/v1/accounts/{accountId}` | -- | AccountResponse |

### KYC

| Method | Path | Request | Response |
|--------|------|---------|----------|
| POST | `/pi/v1/users/{userId}/kyc` | TriggerKycRequest | PostKycResponse |
| GET | `/pi/v1/users/{userId}/kyc` | -- | KycResponse |

### Financial Info

| Method | Path | Request | Response |
|--------|------|---------|----------|
| GET | `/pi/v1/accounts/{accountId}/users/{userId}/financialInfo` | -- | FinancialInfoResponse |
| PATCH | `/pi/v1/accounts/{accountId}/users/{userId}/financialInfo` | PatchFinancialInfoRequest | FinancialInfoResponse |

### Trusted Contact

| Method | Path | Request | Response |
|--------|------|---------|----------|
| POST | `/pi/v1/accounts/{accountId}/trustedContact` | TrustedContactRequest | TrustedContactResponse |
| DELETE | `/pi/v1/accounts/{accountId}/trustedContact/{trustedContactUserId}` | -- | -- |

### Investments

| Method | Path | Request | Response |
|--------|------|---------|----------|
| GET | `/pi/v1/assets` | -- | AssetsResponse |
| POST | `/pi/v1/assets/{assetId}/investments` | CreateInvestmentRequest | InvestmentDetails |
| PUT | `/pi/v1/assets/{assetId}/investments` | UpdateInvestmentRequest | InvestmentDetails |
| PUT | `/pi/v1/assets/{assetId}/investments/{investmentId}/payment` | CreatePaymentRequest | InvestmentDetails |
| GET | `/pi/v1/investments/accounts/{accountId}` | -- | [InvestmentDTO] |
| POST | `/pi/v1/investments/{investmentId}/submit` | SubmitInvestmentRequest | InvestmentDetails |
| DELETE | `/pi/v1/investments/{investmentId}` | CancelInvestmentRequest | -- |
| POST | `/pi/v1/assets/{assetId}/investments/{investmentId}/agreement` | InvestmentSignatureRequest | AgreementDTO |

### Documents

| Method | Path | Request | Response |
|--------|------|---------|----------|
| GET | `/pi/v1/docs/assets/{assetId}/accounts/{accountId}/wire-instructions` | -- | (PDF download) |

### Bank Accounts

| Method | Path | Request | Response |
|--------|------|---------|----------|
| POST | `/pi/v1/accounts/{accountId}/bankAccounts` | CreateBankAccountRequest | BankAccountDetails |
| GET | `/pi/v1/accounts/{accountId}/bankAccounts` | -- | [BankAccountDetails] |
| DELETE | `/pi/v1/accounts/{accountId}/bankAccounts/{bankAccountId}` | -- | -- |
| POST | `/pi/v1/accounts/{accountId}/bankAccounts/{bankAccountId}/transfer` | CreateBankTransferRequest | CreateBankTransferResponse |

### Balance

| Method | Path | Request | Response |
|--------|------|---------|----------|
| GET | `/pi/v1/accounts/{accountId}/balances` | -- | AccountBalanceResponse |

### Markets

| Method | Path | Request | Response |
|--------|------|---------|----------|
| GET | `/markets/v1/schedules` | -- | ScheduleResponse |
| GET | `/markets/v1/mdt/public-pricehistory/{symbol}` | -- | [PriceHistory] |
| GET | `/markets/v1/mdt/public-snapshots/{symbol}` | -- | SymbolData |

### Trading

| Method | Path | Request | Response |
|--------|------|---------|----------|
| GET | `/trading/v1/fee` | (query params) | FeeResponse |
| POST | `/trading/v1/accounts/{accountId}/orders` | CreateOrderRequest | CreateOrderResponse |
| GET | `/trading/v1/accounts/{accountId}/orders` | -- | OrdersListResponse |
| GET | `/trading/v1/accounts/{accountId}/orders/{orderId}` | -- | OrderResponse |
| DELETE | `/trading/v1/accounts/{accountId}/orders/{orderId}` | -- | CancelOrderResponse |
