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

## Launch Timeline

First App Store submission should happen **2-3 weeks before launch**. Apple can reject for surprising reasons and resubmission restarts the review clock. Budget for at least one rejection cycle.

```
Week -3:  Submit to App Store + Play Store
Week -2:  Apple review (expect 3-7 days)
Week -2:  If rejected: fix issues, resubmit
Week -1:  Approved. Set release date. Final OTA updates for last-minute fixes.
Week 0:   Launch
```
