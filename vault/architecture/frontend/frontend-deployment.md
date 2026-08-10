# Frontend Deployment

> **Architecture:** [[architecture]]
> **Status:** Draft

## Three Deployment Targets

### iOS (App Store)

- Build: `eas build --platform ios` (Expo cloud build, ~10-15 min)
- Submit: `eas submit --platform ios`
- Apple reviews: 1-7 days on first submission, 1-2 days for updates. Can reject.
- Requirements: Apple Developer Account ($99/year), signing certificates, App Store listing (screenshots, description), privacy policy URL, age rating
- Users update via App Store (auto-update or manual)

### Android (Google Play)

- Build: `eas build --platform android`
- Submit: `eas submit --platform android`
- Google reviews: usually hours to 1-2 days
- Requirements: Google Play Developer Account ($25 one-time), signing key (Expo manages), store listing
- Users update via Play Store

### Web (Cloud CDN)

- Build: `expo export:web` → outputs static HTML/JS/CSS
- Upload to Cloud CDN
- No server, no review process
- Users get new version on next page load
- Deploy as often as needed

## Over-The-Air (OTA) Updates

For JavaScript-only changes (~90% of updates), Expo can push directly to users' devices without App Store review:

```bash
eas update --branch production --message "fix price display bug"
```

| Change Type | Method | Time to Users |
|-------------|--------|---------------|
| Bug fix in trading UI | OTA | Minutes |
| New screen | OTA | Minutes |
| Style changes | OTA | Minutes |
| New native permission | Full build + review | 1-7 days |
| New native library | Full build + review | 1-7 days |
| App icon change | Full build + review | 1-7 days |

## Release Governance & OTA Caps (24-07-2026)

> Brett introduced release discipline as the team nears the production launch (< 1 month out). Source: [[24-07-2026-touchdown]].

- **The risk principle:** the more change lands close to the production launch, the more risk enters the code base. Expect Novo to **push back on late requests**: get the key features and functions live first, then resume a build/deliver **cadence** post-launch. Requests are not rejected, they are **backlogged and scheduled** (Cody explicitly told to keep bringing ideas).
- **Two ways a change reaches the app store, and why it matters:**
  - **App-store push** (full build + review): tried to be avoided, but certain code changes **force** it.
  - **OTA (over-the-air):** feels flexible, but the stores **cap how much you can push** over the air. Exceed the cap and you must do additional work and start risking the release.
- **Consequence:** releases will be **staged**, work is slotted into the OTA caps ("filling that bucket") so InPlay does not blow the production criteria each app store governs. When Novo appears to stall a request for a couple of weeks, the two reasons are **(1) risk** and **(2) app-store compliance / cap management**, not lack of capacity.
- This sits on top of the existing **CI/CD / DevOps** testing and release-cycle discipline; the new constraint is the app-store layer on top of it.

## Release sequencing: bucket the OTAs, then review (03-08-2026)

> Source: [[03-08-2026-touchdown]]. The operational rule that follows from the
> governance principles above.

The pattern George set out, and the team is now running:

1. **Bucket every OTA-able change** and push them in one go, early in the week.
2. **Then** submit the App Store review, which is required for anything native.
3. **Do not push OTA updates while Apple is reviewing.** Partly it is not
   permitted, mostly it complicates the release. Review is _"could be one day,
   could be four days, could be a week"_ — an unpredictable freeze window, so
   everything wanted in the app has to be in before it starts.

Two things forced the review on this cycle: the **watch page** and the
**ads integration**. Every new SSP will force another one (see
[[advertising/advertising]]) — each integration embeds third-party serving code
plus a policy update, so it is **a resubmission per network**, 24 to 48 hours,
with the live version staying up and being swapped on approval.

**IPO prices ship as an OTA push** rather than a native build, which is why
publication timing is a release question as well as a tZERO one (see
[[ipo-module/ipo-module]]).

## Android is live (31-07-2026)

The **Google Play submission was approved and the Android app went live** on
31 July, announced on the Novo Slack channel and blasted on social on the
Saturday. Cody had been fielding daily "where's the Android?" questions and was
surprised by the demand; Brett, formerly Android country director for emerging
markets, was less so.

⚠ Worth recording honestly: the social blast produced **two signups**
(03-08). Store availability was a blocker, not a growth lever.

Also unblocked by going live: **AdMob for Android**. An SSP application needs an
app-store URL, so Android ad serving could not be set up until the listing
existed (27-07).

**Follow-ups:** Kevin needs the Play Store icon and link for the website;
listing name confirmed as "InPlay Challenge".

## Launch Timeline

First App Store submission should happen **2-3 weeks before launch**. Apple can reject for surprising reasons and resubmission restarts the review clock. Budget for at least one rejection cycle.

```
Week -3:  Submit to App Store + Play Store
Week -2:  Apple review (expect 3-7 days)
Week -2:  If rejected: fix issues, resubmit
Week -1:  Approved. Set release date. Final OTA updates for last-minute fixes.
Week 0:   Launch
```
