---
description: "The single central registry of InPlay ad-monetisation identifiers — publisher, app, ad-unit and SSP seat IDs, with AdMob captured and the SSP roster tracked"
---

# Ad Network & Inventory ID Registry

> **Component:** [[advertising]]
> **Type:** Living reference, the single central registry for ad-network account IDs, publisher IDs, app IDs, and ad-unit IDs
> **Status:** Living. Add every network / SSP / ad-unit ID here as it is issued, so there is one place to query.
> **Related:** the SSP roster and operating model live in [[programmatic-media-playbook]].

---

## How to use this doc

This is the **one central place** for every ad-monetisation identifier InPlay holds: publisher IDs, app IDs, ad-unit IDs, and (as they onboard) SSP seat / account IDs. When a new network is set up or a new ID is issued, add it here. Each network gets its own section; the SSP roster table near the bottom tracks onboarding status for every network in the [[programmatic-media-playbook]].

**Source artefacts** are safe-copied under `sources/` beside this doc (e.g. the AdMob export below).

---

## AdMob (Google), InPlay Challenge

- **Publisher ID:** `pub-2057484236798641`
- **Project:** InPlay Challenge
- **app-ads.txt line (host on both website domains):**
  ```
  google.com, pub-2057484236798641, DIRECT, f08c47fec0942fa0
  ```
- **Source:** `sources/InPlay AdMob Ad Units.html` (AdMob export, v6, "8 of 8 ad units created, complete"). Master generator lives outside the vault at `Programming/inplay/admob-ad-units/`, regenerated on every ID drop.

### iOS app

- **App ID:** `ca-app-pub-2057484236798641~3968172309` (goes in `Info.plist` as `GADApplicationIdentifier`)

| Ad unit name | Format | Ad unit ID |
|--------------|--------|-----------|
| ios-native-inline | Native advanced | `ca-app-pub-2057484236798641/2811640364` |
| ios-native-mrec | Native advanced | `ca-app-pub-2057484236798641/8441677892` |
| ios-native-strip | Native advanced | `ca-app-pub-2057484236798641/2546619319` |
| ios-banner-inline | Banner | `ca-app-pub-2057484236798641/5887666748` |

### Android app

- **App ID:** `ca-app-pub-2057484236798641~8449536897` (goes in `AndroidManifest.xml` as `com.google.android.gms.ads.APPLICATION_ID`)

| Ad unit name | Format | Ad unit ID |
|--------------|--------|-----------|
| and-native-inline | Native advanced | `ca-app-pub-2057484236798641/5823373552` |
| and-native-mrec | Native advanced | `ca-app-pub-2057484236798641/2371213707` |
| and-native-strip | Native advanced | `ca-app-pub-2057484236798641/8761242095` |
| and-banner-inline | Banner | `ca-app-pub-2057484236798641/5696095056` |

### Notes

- **8 ad units, 4 per platform:** three Native-advanced sizes (inline, MREC, strip) plus one inline Banner, mirrored across iOS and Android.
- **Placement mapping:** the app has **44 ad slots per platform** (17 inline + 14 MREC + 11 strip + 2 banner) that map onto this small set of unit IDs; many placements reuse a unit ID.
- **Keep live units clean:** use **Google's test ad-unit IDs in debug builds** so these live units stay free of invalid traffic.
- Put the App IDs in `Info.plist` (iOS) and `AndroidManifest.xml` (Android) as above.

---

## SSP roster (onboarding tracker)

The [[programmatic-media-playbook]] runs AppLovin MAX as ad server + mediator with a portfolio of SSPs plugged in as adapters. Add each SSP's seat / account / publisher ID here as it is issued.

| Network / SSP | Role | Account / seat / publisher ID | Status |
|---------------|------|-------------------------------|--------|
| Google AdMob | Ad network (via MAX adapter) + app-ads.txt seller | `pub-2057484236798641` (see above) | **Live IDs captured** |
| AppLovin MAX | Ad server + mediator (day-one anchor) | ID pending | To onboard |
| Liftoff | SSP adapter (day-one anchor) | ID pending | To onboard |
| PubMatic | SSP adapter (day-one anchor) | ID pending | To onboard |
| _(further SSPs)_ | SSP adapter | ID pending | Roster in [[programmatic-media-playbook]] |

> As SSP seat IDs, sellers.json / app-ads.txt entries, and additional ad-unit IDs are issued, add them to the relevant section above. This doc is the canonical index; keep it current.
