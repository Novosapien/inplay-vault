# InPlay Website Punch List — Both Sites

> Internal & Confidential • v1.3 • July 31, 2026 • Owner: Edwin Johnson
>
> **Scope:** inplayglobal.com and inplaytradingchallenge.com. Each item carries an owner tag — [DEV] developer, [COUNSEL] legal review or drafting, [EDWIN] founder, [POLICY] standing rule — and a priority: P0 same-day, P1 this week's dev sprint, P2 travels in the counsel package, P3 before kickoff. Copy in quoted blocks is final and pastes verbatim.
>
> Source file: `InPlay_Website_Punch_List_1.docx` (Edwin, via Downloads). Companion document: [[../brand/messaging-house|InPlay Messaging House v2.0]], which governs all language.
>
> Repos: `inplay-global-website` (inplayglobal.com) · `Trading-Challenge-` (inplaytradingchallenge.com).

## Part 1 — inplayglobal.com · Homepage

### G1 — Replace the hero background composite [DEV] P1

Remove pitch-and-ticker.jpeg (stadium + neon streaks + floating candlesticks — the signature AI-fintech aesthetic). Replace with a flat deep-navy field with subtle texture that lets the real phone mockup carry the hero, or one licensed real photograph treated dark. Apply the same audit to future-hero.png and opportunity-hero-a4.png: every generated background is replaced with flat brand color, real photography, or product UI.

Typography (Edwin's directive): remove all outline-only display type; relax ultra-condensed tracking on headlines; body copy prioritizes smooth legibility. Nothing extreme.

### G2 — Remove the "Loading…" splash [DEV] P0 — TODAY

The page currently opens with a JS loading gate before content paints. Server-render the hero; institutional sites paint immediately.

### G3 — Add one line of specificity under the hero subhead [DEV] P1

Numbers are the fastest anti-template signal. Under "The market for live sports performance." add:

> NFL and NCAA football. 2,116 games. One market.

### G4 — Swap the hero app screenshot [DEV + COUNSEL] P0 — TODAY

Current screen shows "Day P&L: $7,022.84," "Your P&L $679.62," and a 62%–38% probability bar — implied-performance dollars plus a sportsbook visual convention on a page marketing a future securities offering. Only use a screen showing team prices, movement, and the order book. If the shot depicts the Challenge, watermark "Simulated" on-image.

### G5 — CTA hierarchy [DEV] P1

"Get Market Updates" becomes the sole primary button. "Put Me InPlay" is retired everywhere — button, nav, page name, campaign copy. "Explore the 2026 Football Challenge" is the single secondary. Both store badges — App Store and Google Play (Android app is live as of Jul 31) — move inside the Challenge context, side by side. "Advertise With Us" leaves the hero — its home is the footer's Opportunities column, where it already appears.

### G5b — The capture page — rebuild /put-me-inplay as the email-updates page [DEV + COUNSEL] P1

There is no waitlist. The page becomes a plain email capture at /updates (301 the old URL).

> Headline: "The market opens this season."
> Subhead: "Launch news, season timing, and the founder's memos on market structure — straight to your inbox."
> Button: "Get Market Updates."

One field, email only, privacy-policy link adjacent. Nav item renames to "Updates." A plain mailing list needs only the privacy policy; the testing-the-waters legend applies if/when the list is used to gauge offering interest — counsel drafts it now so it is ready. Memo CTAs close with "Get market updates → [link]."

### G6 — NEW SECTION — "What You Own", immediately after the hero [DEV] P1

The homepage never states what the holder owns. Insert, copy final:

> **WHAT YOU OWN**
>
> InPlay listings are shares in operating companies — real businesses built around football, with income statements. Revenue is earned across an entire schedule of play and the commercial business around it, and prices are set continuously by buyers and sellers. A team can lose on Sunday and its stock can trade up on Monday, because the price reflects the earning power of the business, not the last final score.
>
> Ownership, not outcomes.

### G7 — NEW SECTION — receipts strip, after What You Own [DEV (+COUNSEL: logo rights)] P1

One horizontal band, two rows. Row 1 — "As covered by": Bloomberg, Traders Magazine, SBC Americas wordmarks linking to the Newsroom. Row 2 — "Built with": tZERO and Sportradar. MEMX does not appear (Edwin, Jul 31). Confirm logo-license terms before use. Fallback if any license stalls: text-only names ("As covered by Bloomberg, Traders Magazine, and SBC Americas") need no license and ship immediately.

### G8 — "A new category" section — three text edits [DEV + COUNSEL] P2

- (a) Header becomes "A new category: sports investing." — the category name is in the SEO keywords but absent from body copy.
- (b) "A regulated, market-based way to participate…" → counsel's chosen wording, e.g. "a market-based way to participate… built for a regulated securities framework." Make the identical fix in the meta description, og:description, and twitter:description — the metadata currently leads with "regulated" in the first line Google shows.
- (c) Replace "economic movement created by sports performance" (body + metadata) with "the value created by team performance and the commercial business around it." Verify via view-source that all three meta tags updated.

### G9 — "The problem with existing models" — reframe off settlement [DEV] P1

Replace the section text with the source-of-return version below. Both graphics and the "No continuous market. No real price discovery." caption stay — but re-export both graphics at 2× resolution or rebuild them; the current renders look soft (Edwin).

> Betting and prediction markets have one source of return: the outcome.
>
> Sports betting is built around house odds and one-sided wagering. Prediction markets are binary — a payout fixed in advance, determined entirely by a single result. In both cases, the value of what you hold depends on one question.
>
> An InPlay security is different: its value tracks what an enterprise generates — performance across a full schedule, commercial demand, and market sentiment — priced continuously by buyers and sellers.

### G10 — Ticker — remove the injury items [DEV] P0 — TODAY

Cut "QB limps off / Potential injury" from the loop (it appears twice per cycle). Replace with "75-yard TD drive / Momentum builds" and "New sponsorship signed / Commercial revenue grows." Slow the marquee to a single unhurried pass. No copy anywhere on either site presents an injury as a trading moment. Keep "Performance creates movement. Traders create price."

### G11 — "The fan shift" — relabel step 3 [DEV] P1

Replace the step label "Capture opportunity" with "Read the market." Nothing else changes. Final four-step sequence as displayed: Prepare and position → React and trade → Read the market → Hold conviction.

### G12 — Footer — the permanence block [DEV + COUNSEL] P2

Add: full legal name and address ("InPlay Global, Inc. · 333 SE 2nd Avenue, Suite 2000, Miami, FL 33131"); Privacy Policy and Terms links (the Challenge site has them — the corporate site capturing emails without a posted privacy policy is a live state-privacy problem); an X link (metadata declares @inplayglobalinc but the footer omits it — and verify every listed social account is active); and, once testing-the-waters activity begins, the counsel-drafted legend in the shape of "No money or other consideration is being solicited, and if sent, will not be accepted. Any offer of securities will be made only by means of an offering circular." appended to the existing disclaimer.

## Part 2 — inplayglobal.com · Other Pages

### G13 — The Team — rewrite both bios with concrete history [EDWIN] P1

Edwin's bio omits his concrete market history and runs on interchangeable phrases ("driving force," "category creation"). Replace with the approved bio below. **IMPORTANT: never describe Edwin as a "floor trader" in any material** — the accurate framing is "came up through the trading floors" + electronic trading career. Rewrite Troy's bio with equivalent concrete history. Add LinkedIn links on both profiles.

> **EDWIN JOHNSON** — Founder, Chairman & Chief Executive Officer
>
> Edwin came up through the Chicago trading floors — a runner in the livestock pits at the Chicago Mercantile Exchange, then a clerk in the 5-Year Treasury Note and Dow pits at the Chicago Board of Trade — before building his career on the screen, through the industry's transition from open outcry to electronic markets.
>
> As an independent trader, he specialized in relative-value trading of the U.S. Treasury yield curve and the Treasury basis, and traded across eurodollars, currencies, metals, equity index futures, volatility, equities, and options.
>
> The floor taught him what a market is. The screen taught him what one can become. InPlay is the third act: building market structure for an asset class that has never had one — because sports create real economic value every season, and value that real deserves a real market.
>
> He leads InPlay from the company's headquarters in Miami.

### G14 — Newsroom — two fixes [DEV + COUNSEL] P2

- (a) The SBC summary — InPlay's own copy — says "creating SEC-regulated securities." Pre-qualification, that is implied-approval phrasing: quote the outlet verbatim with attribution, or reword to "securities to be offered under SEC regulations."
- (b) Add a Media Kit block: both logo files, brand colors, approved boilerplate, headshots, press contact. Journalists take the path of least resistance — make the official framing that path.

### G15 — Partners — fix the tZERO paragraph [DEV] P1

"tZERO describes its platform as helping companies…" is visibly hedged, twice-removed phrasing. Obtain one approved sentence from tZERO and write the section in active voice. Fallback until it arrives: run InPlay's own factual one-sentence description. The Sportradar section is fine as is.

### G16 — Advertise — replace the headline [DEV] P1

"The most valuable moments in sports are now for sale" reads as selling the game itself — a gift to any integrity-angle columnist. The inventory is attention during the moments. Replace with:

> Sports' most engaged audience. Reached in the moment.

### G16b — Advertise — body copy [DEV] P1

Swap "one of the most sport-adjacent advertising environments" (adjacency is a weak claim) for the stronger truth: fans actively trading and competing inside the moment. Keep the closing line "This is not passive sports media…"

### G17 — Careers — real or honest [EDWIN + DEV] P3

At least two genuine openings with real descriptions, or an honest note: "We're a small team building deliberately — introduce yourself." An empty scaffold careers page is worse than none. Detailed job descriptions for:

- CTO
- Head of Advertising Sales
- Social Media Director
- Market Operations Director
- DevOps Manager
- Market Surveillance
- Multiple openings for support staff

### G18 — NEW — Insights section [DEV] P1

The home for the founder memos: the site publishes first; LinkedIn, X, and the newsletter syndicate with links back. Dated, numbered, bylined entries — a site that visibly updates weekly cannot read as generated. Must exist before Memo No. 1 ships.

Edwin: "I will be publishing commentary in the weeks leading up to the launch of the trading challenge."

## Part 3 — inplayglobal.com · Technical

### G19 — Cookie consent [DEV] P3

A consent banner for the GTM container; decline non-essential by default.

### G20 — Email authentication [DEV] P3

SPF, DKIM, DMARC on the sending domain before The Income Statement's first send; CAN-SPAM footer (physical address, working unsubscribe) in every issue.

### G21 — OG image [DEV] P3

Verify og-image.jpg is a designed brand card (logo, tagline, brand colors), not generated art — it is the face of every shared link.

### G22 — Icons [DEV] P3

Favicon and app icons generated from the official logo files.

### G23 — Accessibility [DEV] P3

WCAG AA pass: alt text (current standard is good — keep it), contrast, keyboard navigation.

### G24 — Canonical [DEV] P3

inplayglobal.com and www variant 301 to one canonical.

### G25 — Photography [EDWIN] P3

New branded shoot is scheduled (Edwin). It delivers three approved images each for Edwin and Troy and rest of team — formal headshot, warmer three-quarter, environmental — on one consistent dark-neutral backdrop, for the Team page and the media kit. Until delivery, an optional interim retouch matches the two current headshots' backdrops and color grade.

### G26 — Mobile QA pass [DEV] P3

Full phone-width pass of every changed page on both sites — most launch traffic arrives from social and the App Store on mobile. Check: hero paint speed, ticker pacing, receipts-strip wrap, What You Own legibility, capture form, footer links.

## Part 4 — inplaytradingchallenge.com

### C1 — Rename "IPO Kick-off Dates" [DEV] P0 — TODAY

Securities-offering vocabulary never appears on the simulated-game site. Replace with "Season Kickoff Dates" (or "Markets Open"). Verify: site-wide search for "IPO" returns zero results.

### C2 — Anchor the $25M claim to its mechanism [COUNSEL + DEV] P2

On-page, adjacent to the number: "Prize pool: $100,000 guaranteed, growing with Challenge sponsorship — up to $25M. See official rules." Preferred implementation: a live pool figure updated as cash sponsor commitments land. Pool increases move on cash (or irrevocably committed cash) only — in-kind and services partnerships (incl. tZERO) are announced as partnerships and never move the pool number. Funding is stated at the Challenge level only; the mechanism never references team companies or any offering-side entity [C8].

Counsel gates before public use: (a) the official rules guarantee the $100K floor unconditionally — no force-majeure carve-out on the floor amount — before "no matter what" is spoken; (b) tZERO founding-partner naming requires executed agreement plus tZERO PR approval.

Edwin's spoken answers. Base ("funded how?"): "The pool is funded by Challenge sponsorship and advertising revenue. A hundred thousand is guaranteed by InPlay no matter what; twenty-five million is the cap it can grow to as sponsors come in." Follow-up ("which sponsors?"), once gates clear: "We've signed our first founding partner in tZERO; the cash pool grows as cash sponsors come in, and the hundred-thousand guarantee is ours regardless." Until then: "We're in active conversations — and the guarantee is ours regardless, which is the point."

### C3 — Eligibility claim [COUNSEL] P2

Replace "Eligibility: all US states & jurisdictions" with "Open in eligible U.S. jurisdictions — see official rules," with any exclusions listed in the rules. Counsel confirms the eligible list state-by-state (cash-prize contests keyed to sports seasons have quirks in several states even with free entry).

### C4 — Official rules & T&C completeness audit [COUNSEL] P2

Must cover: prize funding source and contingency; payout structure and timing; winner verification and identity requirements; tax handling (prizes over $600 → 1099s → W-9 collection, disclosed up front); referral-wallet anti-abuse terms (self-referral, duplicate accounts, disqualification standards); dispute and modification rights. Anything missing is drafted this week — rules must be final before the sign-up surge.

### C5 — Open the Prize Pool and legal pages to indexing [DEV] P1

The explanation of a $25M public claim must not be less accessible than the claim. Remove the crawl/index blocks on the Prize Pool page and Terms.

### C6 — Domain consolidation [DEV] P0 — TODAY

301-redirect every variant — inplaychallenge.com and any others held — to canonical inplaytradingchallenge.com. Register cheap close variants; the "inplay" search space is saturated with UK betting tipsters and no variant should be a keystroke away from them. Verify: each variant URL returns a 301 to the canonical.

### C7 — Branding against the tipster collision [DEV + MARKETING] P1

Always the full name — "The InPlay Challenge 2026" — in titles, social, and press; never bare "InPlay Challenge," which collides with established UK betting slang. The corporate Newsroom's media kit gives journalists the official framing before search does.

### C8 — The wall between the Challenge and the offering [POLICY] STANDING

The only bridge remains the "About InPlay" footer link. No waitlist promotion, offering language, or "invest" vocabulary ever appears on the Challenge site; no Challenge prize mechanics ever appear beside offering materials. The founder's memos — not the prize site — are where the Challenge audience meets the investing story.

### C9 — Challenge primary CTA [DEV] P1

Primary CTA: "Download the App — Trade the 2026 Season." Subhead beneath it: "Free to enter. Fully simulated. No real money at risk." Both store badges appear together — App Store and Google Play (Android live as of Jul 31); the Challenge homepage currently shows App Store only. Action language never uses "invest" or "risk-free" — the reassurance lives in the factual subhead, never in the verb.

## Part 5 — This Week's Counsel Package (one review, one invoice)

1. InPlay Messaging House v2.0 (companion document) — approve lexicon and red lines; grant standing pre-clearance for memo-series posts that follow the approved lexicon.
2. Founder Memo No. 1 — clear for publication.
3. Testing-the-waters legend — draft for the email-updates capture page (G5b): a plain mailing-list capture needs only the privacy policy; the legend applies if/when the list is used to gauge offering interest. Draft now so it is ready, plus guidance on whether social posts linking to the page need accompanying language.
4. Site items: G4 (screenshot), G8b ("regulated" wording, on-page + metadata), G12 (footer legend, privacy policy, terms), G14a (Newsroom "SEC-regulated" phrasing).
5. Challenge items: C2 ($25M mechanism and floor), C3 (eligibility), C4 (rules audit).
6. Logo-use confirmations for the receipts strip (G7): press wordmarks, tZERO, Sportradar.

## Part 6 — Sequencing

- **TODAY (P0):** G2 · G4 · G10 · C1 · C6 — plus the counsel package (Part 5) goes out with a 72-hour turn requested.
- **THIS WEEK (P1):** G1 · G3 · G5 · G5b · G6 · G7 · G9 · G11 · G13 · G15 · G16/G16b · G18 · C5 · C7 · C9 — the one-week dev sprint. No legal dependency; ship as completed.
- **ON COUNSEL RETURN (P2):** G8 · G12 · G14 · C2 · C3 · C4 — implement counsel's wording same day it lands.
- **BEFORE KICKOFF (P3):** G17 · G19–G26 — close out during weeks two and three.

The through-line: replace the generic with the specific — real photography or flat color over composites, numbers over adjectives, CBOT over "driving force," logos and faces over assertions, a weekly publishing pulse over a finished-and-frozen site. New professional photography is on the way (G25).
