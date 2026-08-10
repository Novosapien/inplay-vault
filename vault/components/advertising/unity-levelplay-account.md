---
description: "Canonical record of the Unity LevelPlay (ironSource) SSP account — app keys, publisher and advertiser IDs, app-ads.txt status and open onboarding items"
---

# Unity LevelPlay Account

Canonical record of the Unity LevelPlay (ironSource) SSP account for InPlay Challenge. Onboarding started 4 August 2026. Ad units to follow: same 8-unit set as AdMob (native inline, native MREC, native image strip, banner, per platform). Tracker: `Programming/inplay/ssp-ad-units/`. Last updated: 4 August 2026.

## App keys

- iOS app key: `277747995`
- Android app key: `27774b31d`

## ironSource platform IDs (added 4 Aug 2026)

- Publisher ID: `674061`
- Advertiser ID: `437285`
- Advertiser password: `f9cf3fb2` (kept here only; deliberately excluded from the shareable SSP ad-units tracker HTML)

## Store apps registered

- iOS: Apple App ID `6784442634`, bundle `com.inplay.tradingchallenge`
- Android: package `com.inplay.tradingchallenge`

## app-ads.txt

- Seller line supplied by LevelPlay: `ironsrc.com, 674061, DIRECT`
- Not yet published to https://inplaytradingchallenge.com/app-ads.txt as of 4 Aug 2026, 16:45 BST

## Open items

- Create the 8 ad units in the LevelPlay console (IDs go into the tracker as they land)
- Publish the `ironsrc.com, 674061, DIRECT` line to https://inplaytradingchallenge.com/app-ads.txt
- Wire the app keys into the LevelPlay SDK init per platform

## Related

- [[admob-account]] -- the live AdMob account and ad units
- [[app-store-accounts]] -- developer account emails, store URLs, app identifiers
- [[sub-components/programmatic-media-playbook/programmatic-media-playbook]] -- the SSP roster and mediation plan
