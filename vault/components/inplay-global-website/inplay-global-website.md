# InPlay Trading Challenge — InPlay Global Website

> **Vision:** [[vision]]
> **Audiences:** [[audiences]]
> **Date:** 2026-05-14
> **Status:** In Design (Max + Skye)
> **Owner:** Skye (content + brand) + Max (design/build) + Edwin (final sign-off)
> **Sources:** _[[meetings/06-05-2026-vision-workshop]], [[12-05-2026-onboarding-and-renewal-and-global-component]]_

---

## Summary

The corporate website for InPlay Global — the brand-facing destination that sits above the Trading Challenge product. It is the umbrella site that captures InPlay's positioning as a **multisport trading platform**, not just an NFL/college football challenge. It hosts the brand story, the case for advertisers, and links out to the Trading Challenge landing page and app stores.

**Current state (as of 12-06-2026 call):** Max has produced a v0.01 first draft. Skye is content lead. Design is **actively in flight** — this component doc captures the directional decisions made in the call and the **action list** to drive the design forward. Full functional-component extraction (data, dependencies, risks, etc.) is deferred until the design stabilises.

> **Update (1–8 June touchdowns):** Max + Skye ran a full redesign (~5h joint session). The site now uses the **exact copy from Skye's deck** (no edits), strong **brand colours**, and an **imagery-last** approach — text/copy is established on screen first, then imagery is built around it (only the home hero had images at 05-06; the rest follow). **Home hero:** two players facing off (AI-generated) + a **moments-of-the-game** section (turnover, QB limps off then returns → price spike) from Edwin's deck. **Pages:** Home, **Partners** ("partner with InPlay"), Team (headshots), Football Challenge. Weekend feedback applied: **outline/"future" font made bolder/thicker/brighter** (was hard to read); team headshots cropped to **consistent framing/distance**; **remove the "Tony"/Anthony Verbillis quote**. **Lead routing:** every page CTA → a **form with a reason selector** (user / advertising / media) routed to the matching **email distribution list** (Troy owns DL assignment; Hassan wires routing); homepage has two CTAs. **Career tab** to be added at top of nav (first posting: VP of Technology). **Publish target: live before the Tuesday sales conference** — reviewed over the weekend and approved to publish, refinement continuing in the background. **Press release:** Skye drafted a T0 release; tZERO is also drafting one → merge and time for Tuesday. _Sources: [[03-06-2026-touchdown]], [[05-06-2026-touchdown]], [[08-06-2026-touchdown]]._

> **Update (10 June — published + compliance incident):** The site was **published before the sales conference** after a page-by-page review. ⚠️ **Compliance incident:** the site-generation **AI agent invented a "trading challenge rules" policy** in the legal footer (sourced from the learning repository) stating **"guaranteed prize money up to $25M"**. Edwin's hard rule: **always "up to $25M", never "guaranteed"** (a guarantee is real legal exposure). Caught and removed within ~1.5h. **Controls:** an **agent team now reviews all copy before any deploy** (scans sensitive/regulated terms — guarantees, prize claims, securities-offer language); AI-generated T&Cs/disclaimers stripped back to the **basic email-signature boilerplate**; **Troy sending disclaimer copy to external counsel (Marlin)** for now-vs-launch review (see the [[components/components#Cross-Cutting Concerns|Cybersecurity & Data-Handling]] cross-cutting control). **Careers page** job descriptions are AI-generated/high-level — Troy + Brian writing the real ones (go-to-market interns + more roles incoming). **Mobile optimisation:** the **outline font overcrowds when scaled** and the **hero phone-screenshot was clipped** → thin outlines on desktop; restructure the hero so the screenshot **stacks below / tilts at a 3D angle** rather than sitting clipped to the side (mobile-first: conference visitors hit the site on a phone first). _Source: [[10-06-2026-Touchdown]]._

---

## Key directional decisions from this call

| Decision | Source | Status |
|---|---|---|
| **InPlay Global is multisport, not football-only** — visual representation must move beyond NFL imagery | Skye | Locked |
| Top-of-page film should be the **hype video** Skye is producing, not Max's current placeholder | Skye | Locked, pending hype video |
| Hero tagline: **"Trade sports as stocks. Buy, sell, hold — every play, every game, every season."** | Skye | Locked |
| Front-and-centre below hero: visual representation of what trading looks like on screen | Skye + Edwin | Locked |
| Use animated price chart with **event markers** ("touchdown happened here", "fumble happened here") tied to Sport Radar data | Edwin | Locked — design direction |
| **Pages to ship first:** Home, About, Advertising | Skye | Locked |
| **Pages to hide for now:** Newsroom, Markets (newsroom news is stale; markets is too early) | Skye | Locked |
| Executive team / board listing — **leave off** the About page for now; add closer to launch | Troy + Edwin | Locked for now |
| Press releases will be staged strategically — T0, Sport Radar, Rebel/Novosapien — Skye working with new press release group | Edwin + Skye | Pending press group output |
| Less-is-more on copy — current first iteration is "very busy" (Edwin) | Edwin | Refinement direction |
| Logo above-the-fold is duplicate of left-nav logo — drop one | Edwin | Locked |
| Light mode option (white background) — Max to add as a toggle | Max + Edwin | In design |
| Design family must be cohesive across InPlay Global, Challenge Website, App, and socials — _"part of the same brand family"_ — not identical | Skye | Brand principle |

---

## Audiences

Different from the Trading Challenge audiences ([[audiences]]). InPlay Global serves three primary visitor types:

| Visitor type | Why they're here | What they need |
|---|---|---|
| **Press / media** | Researching InPlay for coverage | Brand story, press releases, founder/team credibility (eventually) |
| **Advertisers / sponsors** | Evaluating ad inventory | "Advertising" page — audience size, demographics, inventory packaging, contact path |
| **Potential users (referred or discovered)** | Curious about the product before downloading | Clear positioning, link out to Challenge Website / app stores |

Trading Challenge audiences (Crypto-Savvy, Analytical Fan, Finance-Curious Student, Veteran Trader-Bettor) may pass through InPlay Global on their way to the app, but the primary call-to-action site for them is the **[[components/challenge-website/challenge-website]]**, not this one.

---

## Action list (open and outstanding work)

### Content (Skye + Cody + Troy)
- [ ] Finalise hero tagline copy and confirm Edwin sign-off
- [ ] Write Home page copy (Skye lead)
- [ ] Write About page copy — without executive team/board listing for now
- [ ] Write Advertising page copy — inventory packaging, audience size claims, contact CTA
- [ ] Stage press releases: T0 partnership, T0 advertising buy, Sport Radar partnership, Rebel/Novosapien partnership — exact sequence and dates TBD with Skye's new press release group
- [ ] Cody to get Sport Radar sign-off on their press release

### Design (Max + Skye)
- [ ] Replace current top film with Skye's hype video when ready
- [ ] Build the animated price chart hero element with event markers (touchdown / fumble / etc.) — use synthetic data per Edwin's request; production data via Sport Radar later
- [ ] Add multisport visual cues (basketball, hockey, etc.) — direction subject to hype video direction
- [ ] Add light-mode toggle (white background option)
- [ ] Reduce visual density on home page — drop duplicate logo, reduce text-element weight
- [ ] Hide Newsroom and Markets pages from public nav (keep on backlog for later)
- [ ] Hierarchy / IA mapping — Skye to do once content is settled

### Process
- [ ] Max to push v0.02 to George's tool and share link with the full inplay team
- [ ] Edwin specifically asked: do not start "circle to change" review until structure is settled — focus on layout/structure first, refinement second
- [ ] Skye + Max to align on next working session for content + design iteration
- [ ] Cross-brand cohesion check — visually align with [[components/challenge-website/challenge-website]] and the app once both have settled designs

### Awaiting
- [ ] Skye's hype video (then top-of-page film slot can be filled)
- [ ] Press releases from Skye's external press group
- [ ] Final agreement signature between InPlay and Novosapien (Max flagged: rebranded from Rebel Labs to Novosapien — agreement updates pending)
- [ ] Brand CI documentation — full design system / palette / component library does not yet exist (gap inherited from vision)

---

## Page Map (current direction)

| Page | Status | Notes |
|---|---|---|
| **Home** | In design | Multisport hero (two players facing off) + moments-of-the-game section, tagline, animated chart, app/challenge CTAs; hype video slot pending |
| **About** | Content needed | Brand story, no board listing for now |
| **Partners** | In design (Jun) | "Partner with InPlay" — partner-facing pitch + CTA |
| **Team** | In design (Jun) | Headshots (consistent framing); remove the "Tony"/Anthony Verbillis quote |
| **Football Challenge** | In design (Jun) | Challenge-specific page within the Global site |
| **Advertising** | Content needed | Pitch to sponsors — inventory, audience, contact |
| **Careers** | To add (Jun) | Career tab at top of nav for job postings (first: VP of Technology) — Troy owns postings |
| **Markets** | Hidden | Placeholder for live trading view (app screenshot pull-through) — defer to launch |
| **Newsroom** | Hidden | News is stale. Add back when press releases are staged. |

---

## Dependencies

- **Skye's hype video** — gates the top-of-page film
- **Press release pipeline** — gates Newsroom revival
- **Sport Radar data** — needed for production animated chart (synthetic data acceptable for design iteration)
- **App design** — visual cohesion only; not blocking
- **Novosapien rebrand & agreement** — gates Rebel-quote inclusion in press releases (using "Novosapien" not "Rebel Labs")
- **[[components/challenge-website/challenge-website]]** — needs to feel like the same brand family
- **App store presence** — needed for app-download CTA links

---

## Cross-references

- **[[components/challenge-website/challenge-website]]** — the conversion site for the Trading Challenge. InPlay Global links _to_ it but is not it
- **[[audiences]]** — Challenge audiences pass through here on their way to the app
- **Advertising cross-cutting concern** — the Advertising page is the sponsor-facing entry point for the broader advertising product

---

## Open Questions for Next Call

- Will the global site need login/account access (e.g., for advertisers logging into a sponsor portal), or remains marketing-only?
- Localisation — when global expansion confirmed (pending Marlin's ruling), how is the site localised?
- Education module hosting decision — Edwin: _"we're putting Kevin in charge of the education module within the website."_ Confirm whether education lives on InPlay Global vs Challenge Website vs in-app — _affects all three components_
- SEO / discovery strategy for the corporate domain
- Investor relations page — separate from About once team listing is added closer to launch?
- Analytics / funnel tagging — does InPlay Global feed into the cross-cutting Analytics & Funnel Measurement doc as the top of the funnel?
- When does the design stabilise enough to do a full component extraction (sections 4–10 of the standard template — data, dependencies, success metrics, risks)?

---

## Sub-Components

_Deferred pending design stabilisation. Likely candidates: Home, About, Advertising, Newsroom, Education (cross-component), Press Release Management._
