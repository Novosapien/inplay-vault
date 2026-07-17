---
date: 2026-07-12
type: general
scope:
  - "[[architecture/open-questions]]"
  - "[[architecture/integrations/integrations]]"
status: extracted
extracted-to:
  - "[[architecture/open-questions]]"
  - "[[architecture/integrations/integrations]]"
---

> **Date caveat:** the source file carries no internal date; 2026-07-12 comes from the filename (a Sunday). Internal evidence ("Troy to bring in additional Friday call members to Tuesday") suggests the call may have been Friday 10 July. Filed under the filename date; correct if wrong.

## Post-Call Analysis

| Finding | Destination | Action |
|---------|-------------|--------|
| Sim environment IS production for the football challenge; fresh QA env for October basketball | [[architecture/open-questions]] + [[architecture/integrations/integrations]] | Sandbox-timeline question resolved; integration state added |
| EOD Account/Position files (Rob) = reconciliation; buying power resets midnight; updates via FIX OE session | [[architecture/open-questions]] | CRITICAL "what does tZERO manage" question partially answered |
| Buying-power updates via existing FIX OE session | [[architecture/open-questions]] | Referral-funding API-vs-FTP question advanced (supports API route) |
| Two wallets per user (long + short, same token); treasury-wallet fix for legacy trades | [[architecture/open-questions]] + integrations | Shorting-mechanics question updated; state recorded |
| Edwin = designated market maker, only API-connected trader in challenge; algo in build, needs quoting-model inputs | [[architecture/open-questions]] | Both market-maker questions updated; reinforces candidate standalone component |
| Six college football symbols added; six NFL symbols simulated | integrations | State recorded |
| Cap-table API exposes balances + corporate actions; Eric to set up Hasan/George on portal | integrations | State recorded |
| DAY/GTC time-in-force question NOT answered in the meeting | [[architecture/open-questions]] | New open question added |
| Commissions settled; payouts deferred to Tuesday; Aug 22 target; architecture diagrams requested | integrations | State recorded; no doc changes beyond note |

---

Our questions:

1\. Blockchain / cap-table API  
We discussed whitelisting an IP for the portal, do we have an update on this?

2\. Bid/Ask formation  
Where does the quoted liquidity come from \- a live ATS/matching engine with participant orders, or quotes published to the book by tZERO / a market maker? What do our orders match against, who's the contra-side in SIM, and how is the reference/last price (MktPrx) set? And does production apply price bands/collars?

3\. Production handover  
We're on QA for FIX trading and Staging for the Onboarding API \- what's the path and timeline to move both to prod?

4\. EOD report delivery  
How are the daily Account/Position reports delivered \- I remember we mentioned FIX as an option, and what's the cadence \+ filename convention? Also: how is AccNUMB assigned in SIM, and can the SIM OMS book trades it didn't execute?

5\. Time-in-Force  
We'll use two order types: DAY and GTC. Can you confirm both are supported, and that GTC orders persist across your daily session reset (23:59 ET)?

Meeting notes:

**Blockchain Wallet Architecture**

* Settled on two wallets per user: one long, one short (same token, different wallets)  
  * Avoids bifurcating execution liquidity, which was the concern with two separate tokens  
  * Helps investors clearly distinguish long vs. short position  
  * Wallets are not a cost center, so no issue scaling this  
* Some existing trades missing wallet addresses (original buy-ins pre-treasury wallet)  
  * Short-term fix: auto-assume treasury wallet for those entries  
  * Production plan: pre-create lots with known treasury wallets from the start  
* Order simulator currently not passing wallet addresses  
  * Workaround: assign simulated orders to a general/placeholder wallet

### **Liquidity and Market Making**

* Current sim builds order book on six NFL team symbols using an order simulator (no real participants yet)  
* For the trading challenge, InPlay’s Edwin will be the designated market maker (DMM)  
  * Connects to tZERO API like any other participant, but is the only API-connected trader in the challenge  
  * All other participants trade through the app only; API access opens in production  
  * Edwin provides two-sided markets; other participants can still add passive liquidity  
* Edwin is building his market-making algo now and needs quoting model inputs  
  * Novo team to follow up with Edwin directly in their separate session

### **Environment Strategy and Production Readiness**

* Clarified “production” \= trading challenge launch (not January full prod)  
  * Current segregated sim environment is the live platform for the challenge  
  * No environment transition needed; what’s being tested now is what goes live  
* API environment: may need to move from staging to demo; Eric to confirm with Avishakim  
* Agreed direction: promote current environment to prod for the football challenge; stand up a fresh QA/staging environment  
  * New environment serves two purposes: post-launch QA buffer and staging ground for the MBA basketball challenge (target: October)  
  * Different features likely needed for basketball vs. football, so cleaner to build forward  
* On tZERO’s side, multi-tenancy is straightforward: new issuer per environment/sport, scoped API keys  
* August 22nd is the live target; separate environment feasibility to be confirmed by Rob  
* Brett requested architecture diagrams from tZERO to ground the Novo team’s development and AI-assisted coding

### **End-of-Day Reports and Account Management**

* End-of-day files (sent by Rob) serve as reconciliation: buying power and positions per account  
* Buying power resets at midnight; already enabled in sim but not yet fully connected to the simulation environment  
  * Clearing software deployment is rolled to staging; one final connection piece pending  
* Account onboarding flow: account created via API → account number returned → flows to FIX session → orders can be placed  
  * Eric to walk Hasan through the FIX message flow on Slack  
* Buying power updates can be sent via the existing FIX order entry session  
* Cap table management API (blockchain layer) also exposes per-customer balances and corporate action APIs  
  * Eric to demo capabilities after the call; FIX/OMS remains the primary route

### **Other Items and Next Steps**

* Six new college football team symbols added to matching engine and market data last night; ready for orders once Chris confirms  
* Commissions (long and short side, simulator): landed in a good place last week, no further action  
* Payouts: deferred to Tuesday call  
* Troy to bring in additional Friday call members to Tuesday as needed to hit August 22nd

### **Next Steps**

* **Set up Hasan or George on the cap table API portal** (Eric)  
  * Demo capabilities after the call so the Novo team can start pulling blockchain position data.  
* **Walk Hasan through FIX account message flow on Slack** (Eric)  
  * Cover how account numbers are assigned, what messages to expect, and how buying power updates are sent.  
* **Confirm API environment move from staging to demo** (Eric)  
  * Eric to check with Avishakim; should not be a significant change.  
* **Investigate standing up a separate QA environment alongside prod** (Rob)  
  * Assess feasibility given the August 22nd deadline; current environment to become prod for the football challenge.  
* **Send tZERO architecture diagrams to the Novo team**  
  * Needed for developer context and AI-assisted coding on the Novo/Rebel Labs side.  
* **Share previous stand-up recordings with the Novo team**  
  * Novo team ingests recordings into their knowledge base for ongoing context.

