---
description: "Canonical record of the InPlay Challenge AdMob account: publisher and app IDs, every live ad-unit ID per platform, the app-ads.txt line and integration notes"
---

# AdMob Account & Ad Units

Canonical record of the Google AdMob account and the live ad units for InPlay Challenge. Mirrors the AdMob section of the SSP ad-unit tracker at `Programming/inplay/ssp-ad-units/` (shared copy: `shared/clients/inplay/media-planning/publisher/InPlay SSP Ad Units.html`). The original 8 units were created 29 July 2026; the Gamecast video unit was added 17 August 2026. Last updated: 17 August 2026.

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
| `ios-video-gamecast` | Native advanced (to confirm) | Media type: VIDEO | 1 | `ca-app-pub-2057484236798641/8819125414` |

## Ad units: Android

| Unit name | Format | Setting | Slots | Ad unit ID |
|---|---|---|---|---|
| `and-native-inline` | Native advanced | Media type: unset | 17 | `ca-app-pub-2057484236798641/5823373552` |
| `and-native-mrec` | Native advanced | Media type: unset | 14 | `ca-app-pub-2057484236798641/2371213707` |
| `and-native-strip` | Native advanced | Media type: IMAGE | 11 | `ca-app-pub-2057484236798641/8761242095` |
| `and-banner-inline` | Banner | Auto-refresh: optimized | 2 | `ca-app-pub-2057484236798641/5696095056` |
| `and-video-gamecast` | Native advanced (to confirm) | Media type: VIDEO | 1 | `ca-app-pub-2057484236798641/2249897963` |

44 static placements per platform (17 inline + 14 MREC + 11 strip + 2 banner), plus 1 Gamecast video slot per platform.

## Gamecast video unit

Added 17 August 2026, live on both platforms. The first video-capable units in the account: every other unit is image or banner, so before these InPlay could not serve a video ad on AdMob at all.

| Platform | Unit name | App ID | Ad unit ID |
|---|---|---|---|
| iOS | `ios-video-gamecast` | `ca-app-pub-2057484236798641~3968172309` | `ca-app-pub-2057484236798641/8819125414` |
| Android | `and-video-gamecast` | `ca-app-pub-2057484236798641~8449536897` | `ca-app-pub-2057484236798641/2249897963` |

- Intended placement: inside the football-field graphic on the Live Gamecast surface, served during breaks in play (no live game action)
- Format recorded as native advanced with media type VIDEO, which is the format that allows the creative to render inside an InPlay-designed container rather than taking over the screen. **Confirm against the AdMob console before wiring it up** — if either was created as interstitial or rewarded, the placement plan changes, because those formats are full-screen and InPlay controls no layout.
- Placement feasibility briefed to Hasan on 17 August 2026: can the field render it, does the tap target separate from the trade and nav actions, and what does it cost to build.

Client-side requirements for this unit to render at all:

- The native ad layout must contain a `MediaView` bound to `nativeAd.mediaContent`. Without one, video creatives cannot play.
- Set `VideoOptions.startMuted = true`. Muted autoplay is the only compliant default.
- Preload with a timeout and fall back to an existing image unit on no-fill. Video-restricted units fill materially lower than unrestricted ones.
- The ad must carry a visible "Sponsored" or "Ad" label and its tap target must not overlap the card's trade or navigation actions. Placing a clickable ad inside a functional live surface is the main AdMob policy risk here.

Open question: whether the field panel on a live, tradeable game card can carry a programmatic creative at all, or whether that placement has to be direct-sold through InPlay's own ad service. See [[ad-service]].

## Integration notes

- Register these units as the AdMob adapter in AppLovin MAX.
- App IDs (the `~` values) go in Info.plist and AndroidManifest.
- Use Google's test unit IDs in debug builds so live units stay clean of invalid traffic.

## Related

- [[app-store-accounts]] -- developer account emails, store URLs, app identifiers
- [[programmatic-media-playbook]] -- the ad stack decision (AppLovin MAX as mediator, no GAM)
