---
description: "Register of the Apple and Google Play developer accounts and live app identity — store URLs, bundle ID, App ID, and support contacts for InPlay Challenge"
---

# App Store Accounts & Live App Identity

Reference for the store accounts and published app identifiers. Both listings went live on 22 July 2026. Last updated: 26 August 2026.

## Accounts

- **Apple App Store developer account email: `appdev@inplayglobal.com`** (App Store Connect login / developer email for InPlay Global, Inc.)
- **Google Play developer account email: `appdevinplayglobal@gmail.com`** (Play Console login for the Android listing)
- Public support contact on both listings: `support@inplayglobal.com`
- Developer name on both stores: InPlay Global, Inc.
- Developer website on both listings: https://inplaytradingchallenge.com

## iOS (App Store)

- App name: InPlay Challenge
- Store URL: https://apps.apple.com/us/app/inplay-challenge/id6784442634
- Apple App ID: `6784442634`
- Bundle ID: `com.inplay.tradingchallenge`
- Developer page: https://apps.apple.com/us/developer/inplay-global-inc/id6784442636
- v1.0 released 22 Jul 2026, iOS 15.1+, Sports / Entertainment, rated 17+

## Android (Google Play)

- Store URL: https://play.google.com/store/apps/details?id=com.inplay.tradingchallenge
- Package name: `com.inplay.tradingchallenge`
- Free, contains ads, Sports, rated Mature 17+

## Store listing changes are frozen (24-08-2026)

**No changes to the app logo or name for now.** Jared proposed both on the 24-08
touchdown, having raised it in Slack. George: it is _"not a quick one… it's like
new review. It might even be a new like whole app"_, and Brett agreed. Cody's
ruling: _"let's hold off on making any app store changes until we have this call
with Viral App. So, our kickoff call is tomorrow. Part of our package with them is
App Store optimization."_

Practical effect: treat the listing identity above as **frozen** until the Viral
kickoff (**25 August 2026**) has happened, and route any proposed change through
Cody rather than making it directly. **Viral own app store optimisation** as part
of their package, so listing decisions are theirs to advise on.
(Source: [[24-08-2026-touchdown]])

⚠ **Related distribution note from the same call, worth knowing.** Testers on the
**TestFlight beta build** found the **IPO draft page locked** and could not buy
from it, though buying worked from the markets and trade pages. Deleting the beta
and installing the **live App Store build** fixes it, confirmed live on the call.
Troy: _"we should have made that more explicit."_ The first question on any
tester's "the app is broken" report is **which build are you on**. See
[[ipo-module/ipo-module]] and [frontend-deployment](frontend-deployment.md).

### Icon and name split (26-08-2026)

The freeze holds, but the two changes were separated and they are not the same
size:

| Change | Cost | Position |
|---|---|---|
| **App icon** | Troy: probably **no review**, apps push icon changes frequently | Ask taken: can the icon alone be simplified first |
| **App name** | Hasan: needs a **new app store check**, _"at least like a week or so"_. George: _"either a completely new app review or a completely new submission"_ | Held |

Cody held both until the **Viral** contract is settled; the kickoff happened on
**25 August** and he had a contract call immediately after this touchdown. Edwin
raised the change again and accepted the lift: _"that might be a bigger lift than
we thought."_ (Source: [[26-08-2026-touchdown]])

## Related

- Privacy policy: https://inplaytradingchallenge.com/legal/privacy
- app-ads.txt (live): https://inplaytradingchallenge.com/app-ads.txt
- AdMob account and ad units: [[admob-account]]; Unity LevelPlay: [[unity-levelplay-account]] (tracker master: `Programming/inplay/ssp-ad-units/`)
- SSP publisher one-pager (master): `Programming/inplay/ssp-application-onepager/`
- Deployment process: [frontend-deployment](frontend-deployment.md)
