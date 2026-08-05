---
description: "Hub for advertising as a cross-cutting concern — the two revenue motions, direct-sold sponsorship vs programmatic SSP inventory, and its sub-component index"
---

# InPlay Trading Challenge — Advertising

> **Vision:** [[vision]]
> **Type:** Cross-cutting concern (not a standalone product component)
> **Date:** 2026-06-18
> **Status:** Collecting
> **Owner:** Edwin + Skye (commercial) + Brett (ad-tech / programmatic) + Max (creative units)
> **Sources:** _[[meetings/22-05-2026-Advertising-first-meeting]], [[meetings/17-06-2026-touchdown]]_

---

## What This Is

Advertising is how InPlay monetises its inventory. It is a **cross-cutting concern**, not a screen or a flow: ad surfaces overlay the websites, the information layer, trading, referral, third space, and education. The canonical description of the commercial model (sponsorship territories, engagement-minute billing, packaging tiers, sales motion) lives in the **Advertising section of [[components/components#Cross-Cutting Concerns]]**. This directory exists to hold the **buildable sub-components** of the ad business as they get scoped.

There are two complementary revenue motions:

1. **Direct-sold sponsorships** — single-brand, season-long ownership of specific surfaces ("the trading challenge presented by [brand]"), sold by Skye's team. Served on day one as house ads/campaigns inside the mediator, and in **phase 2 via Kevel** for moment-based triggers (a brand owning touchdowns for a team). Rich, custom units; not standard IAB inventory.
2. **Programmatic / generalised inventory** — the rolling in-content ad units (banner, interstitial, native, video) filled by an **SSP portfolio** through an in-app auction. This is the always-on backfill that monetises every eyeball-minute the direct deals do not own. The operating model for this is the **[[sub-components/programmatic-media-playbook/programmatic-media-playbook]]**.

## Sub-Components

| Sub-Component | Overview | Status | Link |
|--------------|----------|--------|------|
| Programmatic Media Playbook | The SSP roster, the AppLovin MAX architecture, and the 1-human + AI-agent ad-ops operating model for the programmatic/generalised inventory | Reference | [[sub-components/programmatic-media-playbook/programmatic-media-playbook]] |
| AdMob Account & Ad Units | The live AdMob account (publisher ID, App IDs, app review status) and all 8 production ad-unit IDs, iOS + Android | Reference | [[admob-account]] |
| Unity LevelPlay Account | The LevelPlay SSP account: app keys per platform, ironSource platform IDs, registered store apps, ad units to follow | Reference | [[unity-levelplay-account]] |
| Vungle Account | The Vungle (Liftoff Monetize) SSP account: account ID, Android app ID, registered store apps, ad units to follow | Reference | [[vungle-account]] |

> **Note (18 June 2026):** Advertising was promoted from a pure cross-cutting note into this directory so the **programmatic media playbook** (Brett, 17-06) could be captured as a buildable sub-component. The specialist-sponsorship-territory detail still lives in [[components/components#Cross-Cutting Concerns]] and is the next candidate to extract into its own sub-component here.
