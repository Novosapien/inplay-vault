# AdMob Account & Ad Units

Canonical record of the Google AdMob account and the live ad units for InPlay Challenge. Mirrors the AdMob section of the SSP ad-unit tracker at `Programming/inplay/ssp-ad-units/` (shared copy: `shared/inplay/media-planning/publisher/InPlay SSP Ad Units 2026-08-04-1140.html`). All 8 units created as of 29 July 2026. Last updated: 4 August 2026.

## Account

- AdMob publisher ID: `pub-2057484236798641`
- AdSense customer ID (payments / Google support): `109-277-7465`
- app-ads.txt line, live at https://inplaytradingchallenge.com/app-ads.txt: `google.com, pub-2057484236798641, DIRECT, f08c47fec0942fa0`
- App review status: **Android approved (Aug 2026), ad-serving limits and restrictions lifted**

## App IDs

- iOS (Info.plist, `GADApplicationIdentifier`): `ca-app-pub-2057484236798641~3968172309`
- Android (AndroidManifest, `com.google.android.gms.ads.APPLICATION_ID`): `ca-app-pub-2057484236798641~8449536897`

## Ad units: iOS

| Unit name | Format | Setting | Slots | Ad unit ID |
|---|---|---|---|---|
| `ios-native-inline` | Native advanced | Media type: unset | 17 | `ca-app-pub-2057484236798641/2811640364` |
| `ios-native-mrec` | Native advanced | Media type: unset | 14 | `ca-app-pub-2057484236798641/8441677892` |
| `ios-native-strip` | Native advanced | Media type: IMAGE | 11 | `ca-app-pub-2057484236798641/2546619319` |
| `ios-banner-inline` | Banner | Auto-refresh: optimized | 2 | `ca-app-pub-2057484236798641/5887666748` |

## Ad units: Android

| Unit name | Format | Setting | Slots | Ad unit ID |
|---|---|---|---|---|
| `and-native-inline` | Native advanced | Media type: unset | 17 | `ca-app-pub-2057484236798641/5823373552` |
| `and-native-mrec` | Native advanced | Media type: unset | 14 | `ca-app-pub-2057484236798641/2371213707` |
| `and-native-strip` | Native advanced | Media type: IMAGE | 11 | `ca-app-pub-2057484236798641/8761242095` |
| `and-banner-inline` | Banner | Auto-refresh: optimized | 2 | `ca-app-pub-2057484236798641/5696095056` |

44 placements per platform (17 inline + 14 MREC + 11 strip + 2 banner).

## Integration notes

- Register these units as the AdMob adapter in AppLovin MAX.
- App IDs (the `~` values) go in Info.plist and AndroidManifest.
- Use Google's test unit IDs in debug builds so live units stay clean of invalid traffic.

## Related

- [[app-store-accounts]] -- developer account emails, store URLs, app identifiers
- [[programmatic-media-playbook]] -- the ad stack decision (AppLovin MAX as mediator, no GAM)
