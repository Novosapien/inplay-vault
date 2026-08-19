---
description: "The securities-not-gambling argument, the SEC offering circular and gun-jumping risk, Rule 255 testing-the-waters, and the Kalshi litigation InPlay is positioning against."
---

# Regulatory Positioning

> **Section:** [[compliance/compliance]]

## The core argument

InPlay's defence against being classified as gambling rests on one distinction,
stated by Edwin on 31-07 and 03-08:

- A sports **bet** pays out on the **outcome of an event**. The bettor has no
  control over it, and the event is (in the plaintiff's framing) a game of
  chance.
- An InPlay **team company share** pays out on **price**, which is a live
  estimate of that company's earnings, on-field _and_ off-field. Winning a game
  is one input to that estimate, not the settlement trigger. A team can win and
  the share price can fall.

The off-field revenue leg is what makes this structurally true rather than
cosmetic: the more off-field earnings matter (see
[[earnings-report/earnings-report]]), the less on-field results dominate value.
Edwin, 31-07:

> "As we are successful with AdMob and the others, on-field performance becomes
> less and less the dominant driver, and then it becomes more about the
> predictability of the actual revenue from off the field."

**Consequence for the product:** anything that makes the app read as gamified
betting weakens the argument. Anything that frames it as investing in an
operating company strengthens it. Edwin explicitly re-prompted his 03-08 UI
rebuild from the legal position first, not the design position.

## The Kalshi litigation (and why it helps)

On 31-07 New York's Attorney General sued Kalshi. The sequence matters:

1. Kalshi sought a temporary restraining order to stop New York shutting it
   down, on federal-preemption grounds.
2. **The judge denied the TRO**: read on its face as the court thinking Kalshi
   is unlikely to win on the merits.
3. That denial green-lit New York's full lawsuit.

New York matters more than the other suing states because the Second Circuit is
where a lot of precedent gets set. Edwin expects this to reach the Supreme
Court eventually.

The operative language in the complaint, which Edwin read out on the call:

> "The lawsuit alleges that Kalshi's prediction markets meet the legal
> definition of gambling because the outcomes of the events on which its users
> are betting are uncertain and outside the control of the bettor, or hinge on a
> game of chance."

Edwin's read: the "game of chance" limb is weak (athletics is skill, not
chance), but **"the outcomes of the events"** is the phrase that matters, and it
frames InPlay as the obvious solution, because InPlay is not settled by
outcomes.

**Marketing instruction (31-07):** Kevin and Jared may use this framing in
social outreach, but **must not name Kalshi or any competitor**. Position on
what InPlay is, not on what the other side is.

Also noted 31-07: Underdog bought a DCM (designated contract market) and sold
for ~$1.2bn, evidence of how the category is being valued.

## The SEC filing and gun jumping

- A **full batch filing went to the SEC** in the week of 27-07; the stamped copy
  was expected back for Jim Angel and others (29-07).
- InPlay is in the window where promotional language can **condition investor
  interest in an unqualified security**. The term of art Edwin used is
  **"unlawful gun jumping"**, and it is the reason legal is reviewing app and
  website copy line by line.
- Worked example, 03-08: Edwin wrote an explainer story about what InPlay is.
  **Legal denied it the same morning.** They then supplied a permitted version.
- The route through this is **Rule 255** (Regulation A "testing the waters").
  If the trading challenge is conducted compliantly under Rule 255, the only
  filing consequence is an **addendum to the offering circular** covering the
  marketing. That requires the prescribed disclosures to appear **ahead of
  time**, which is why the disclaimer is now in the app (07-08).

### Language rules now in force _(07-08)_

| Do not say | Say instead |
|-----------|-------------|
| "regulated by the SEC" | nothing, the claim comes out entirely |
| "IPO" | **"simulated IPO"** |
| "securities" (unqualified, in marketing) | avoid; frame as the simulated challenge |

Kevin is credited with the "simulated IPO" phrasing.

## Where the testing-the-waters disclosure actually goes (17-08-2026)

Settled on the 17 August call, because Edwin's prototype had put it on almost
every screen and Jared asked whether that was necessary.

Edwin's answer: _"yes, but not in its current form."_ The agreed shape:

- **An info button** carrying the full disclosure, which expands on demand rather
  than occupying every surface.
- **On the competition-selection screen** at first open, so it is demonstrably in
  front of every user before they choose anything. Edwin's reasoning was
  evidential rather than cosmetic: _"I may want to also have it there just to say
  it was there."_
- **Not on every surface.** Troy proposed relying on the terms and conditions
  alone, on the basis that nobody reads them. Edwin accepted that as part of the
  answer but not the whole of it, hence the selection screen.

The distinction matters: relief under Rule 255 depends on the prescribed
disclosures being made **ahead of time**, so the point of placing it on the
selection screen is to be able to show it was unavoidable, not to satisfy a
design preference.

## State-by-state exposure

- Legal is working through **47 states** of registrations and bonds, with Edwin
  signing them (03-08).
- **California is the tricky one**: it needs additional disclaimers where users
  give up geolocation, and its app rules differ by functionality.
- Troy's standing question: which state laws change what the app is allowed to
  do, not just what it is allowed to say.
- Edwin's stated fear is a blind side: "the one thing we don't want to do is get
  jammed up in Alabama."

## Open questions

| # | Question | Owner | Status |
|---|----------|-------|--------|
| L1 | Which app surfaces must carry the Rule 255 disclosure, and in what form? One global disclaimer or per-surface? | Edwin / legal | 🔴 Open |
| L2 | Does the **no-KYC public challenge** change the filing position, given it has no cash prizes but does collect users? | Edwin / legal | 🔴 Open |
| L3 | Which states restrict app **functionality** (not just copy), and does that require geo-gating features? | Edwin / legal, Troy raised | 🔴 Open |
| L4 | Does the **simulated-IPO** framing need to extend to the ticker/company naming convention as well? | Edwin / legal | 🔴 Open |
| L5 | Sign-off path for outbound social copy that leans on the Kalshi framing without naming them | Edwin, Kevin, Jared | 🟡 Agreed in principle 31-07 |

## Sources

[[31-07-2026-touchdown]] · [[03-08-2026-touchdown]] · [[07-08-2026-touchdown]]
· [[29-07-2026-touchdown]]
