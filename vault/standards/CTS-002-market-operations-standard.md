---
description: "CTS-002 master draft — market lifecycles, Reference Price publication, operating conditions and profiles, order matching rules and quote construction math"
---

## JULY 2, 2026 

# INPLAY CORE TECHNICAL STANDARDS CTS-002 MARKET OPERATIONS STANDARD (MOS-1 MASTER DRAFT) 

EDWIN JOHNSON INPLAY GLOBAL, INC. 333 SE 2nd Avenue, Suite 2000 Miami, FL 33131 



## **TRADE SECRET OF INPLAY GLOBAL, INC.** 

This document contains confidential, proprietary, and trade secret information of InPlay Global, Inc. It is furnished solely for authorized evaluation, development, implementation, legal review, or other approved business purposes. Unauthorized use, copying, disclosure, distribution, reproduction, reverse engineering, or derivative use of any portion of this document is strictly prohibited without the prior written consent of InPlay Global, Inc. 

## **INPLAY CORE TECHNICAL STANDARDS** 

## CTS-002 

## Market Operations Standard (MOS-1) 

**Version:** 1.0 (Master Draft) 

**Document Classification:** Internal Authoritative Technical Standard 

**Status:** Draft – Subject to Formal Approval 

**Owner:** InPlay Global, Inc. 

## **Chapter 1** 

## Constitutional Principles 

## 1.1 Authority 

The Market Operations Standard ("MOS") establishes the authoritative operational, technical, and mathematical standards governing the operation of secondary markets for InPlay Securities. 

1 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



CTS-002 governs the operation of every market conducted under the InPlay platform, including simulation markets, promotional markets, educational markets, and regulated production markets. 

All market operations, execution systems, operational procedures, Product Technical Standards, and software implementations SHALL conform to this standard unless expressly superseded by an approved revision. 

Where a conflict exists between CTS-001 and CTS-002, the Financial Valuation Standard (CTS-001) governs all matters relating to valuation, while CTS-002 governs all matters relating to market operation. 

## 1.2 Relationship to CTS-001 

The Financial Valuation Standard (CTS-001) and the Market Operations Standard (CTS-002) perform separate and independent functions. 

CTS-001 determines the Expected Settlement Value ("ESV") of every InPlay Security. 

CTS-002 governs the operation of markets surrounding that valuation. 

CTS-002 SHALL NOT: 

- determine Expected Settlement Value; 

- modify Expected Settlement Value; 

- reinterpret Expected Settlement Value; or 

- replace Expected Settlement Value with any alternative valuation. 

The Market Operations Standard consumes the Expected Settlement Value published by CTS-001 as its authoritative financial input. 

The independence between valuation and market operation SHALL be preserved throughout every implementation of the InPlay platform. 

## 1.3 Purpose 

The purpose of the Market Operations Standard is to establish the operational framework governing secondary markets for InPlay Securities. 

2 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



This standard defines: 

- market state management; 

- reference price publication; 

- operating condition assessment; 

- market intelligence; 

- execution model governance; 

- market execution; 

- quote generation; 

- market integrity; 

- operational audit; and 

- performance measurement. 

This standard governs market operation only. 

It does not define: 

- Contractual Economic Rights; 

- Economic Components; 

- valuation methodology; 

- Expected Settlement Value; or 

- settlement mathematics. 

Those subjects are governed exclusively by CTS-001. 

## 1.4 Foundational Principle 

The purpose of an InPlay market is not to determine value. 

Value is determined independently by the InPlay Valuation System in accordance with CTS-001. 

The purpose of the Market Operations Standard is to facilitate fair, orderly, resilient, and transparent price discovery around that independently determined valuation. 

Accordingly: 

- CTS-001 determines value. 

- CTS-002 governs market operation. 

- Product Technical Standards define product-specific operating parameters. 

3 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 

These responsibilities SHALL remain independent. 



## 1.5 Operating Principles 

Every market operating under this standard SHALL satisfy the following principles. 

### Principle 1 — Fair Markets 

Markets SHALL operate fairly and consistently for all participants. 

### Principle 2 — Orderly Markets 

Markets SHALL promote continuous and orderly trading whenever the applicable Market State permits trading. 

### Principle 3 — Continuous Liquidity 

Where required by the applicable Product Technical Standard, continuous executable quotations SHALL be maintained throughout the applicable trading session. 

### Principle 4 — Operational Independence 

Market operation SHALL remain independent of financial valuation. 

Operational decisions SHALL NOT modify Expected Settlement Value. 

### Principle 5 — Deterministic Operation 

Given identical: 

- Reference Prices; 

- Market States; 

- Operational States; 

- operating conditions; 

- approved operational inputs; and 

- implementation versions, 

every conforming implementation SHALL produce identical operational results. 

4 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



### Principle 6 — Operational Resilience 

Markets SHALL continue operating safely under degraded operating conditions in accordance with the applicable operational policies defined by this standard. 

### Principle 7 — Auditability 

Every operational decision SHALL be reproducible, independently auditable, and permanently recorded. 

## 1.6 Scope 

This standard governs: 

- market state architecture; 

- reference price publication; 

- market operating condition assessment; 

- market intelligence; 

- execution model governance; 

- market execution; 

- quote generation; 

- market integrity; 

- operational replay; 

- operational audit; and 

- operational performance measurement. 

This standard applies equally to: 

- simulation markets; 

- promotional markets; 

- educational markets; 

- regulated production markets; and 

- every Product Technical Standard operating under the InPlay platform. 

## 1.7 Constitutional Hierarchy 

The InPlay Technical Standards are governed by the following constitutional hierarchy: 

5 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



1. **CTS-001 — Financial Valuation Standard** Determines Expected Settlement Value. 

2. **CTS-002 — Market Operations Standard** Governs market operation around Expected Settlement Value. 

3. **Product Technical Standards (PTS)** 

   - Define product-specific operating parameters within the constitutional framework established by CTS-001 and CTS-002. 

No Product Technical Standard may redefine the constitutional principles established by either CTS-001 or CTS-002. 

## **Chapter 2** 

## Market Lifecycle Architecture 

## 2.1 Purpose 

This chapter establishes the lifecycle architecture governing every market operating under the InPlay platform. 

The Market Operations Standard recognizes two independent lifecycle models: 

- the **Market Lifecycle** , which governs whether a market is permitted to operate; and 

- the **Operational Lifecycle** , which governs how an open market behaves throughout a Defined Event. 

The separation of these lifecycle models permits continuous market operation while allowing operational behavior to change in response to the progression of the Defined Event. 

6 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## Part I — Market Lifecycle 

## 2.2 Market Lifecycle 

Every InPlay market SHALL exist in one—and only one—Market Lifecycle State. 

The Market Lifecycle governs: 

- market availability; 

- quotation authority; 

- execution authority; 

- settlement authority; and 

- lifecycle progression. 

The Market Lifecycle consists of: 

Pre-IPO ↓ IPO ↓ Pre-Market ↓ Open Market ↓ Settlement ↓ Archived 

Market Lifecycle transitions SHALL be deterministic, reproducible, and permanently recorded. 

## 2.3 Pre-IPO 

The security has not yet been offered. 

Secondary trading is prohibited. 

Reference Prices are not published. 

7 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



Expected Settlement Value may be determined internally for validation and certification purposes. 

## 2.4 IPO 

Primary issuance is active. 

Subscriptions are permitted. 

Secondary market quotations and executions are prohibited. 

Reference Prices may be disseminated for informational purposes where permitted by the applicable Product Technical Standard. 

## 2.5 Pre-Market 

The security has been issued. 

Expected Settlement Value is active. 

Reference Prices are published. 

The Market Operations System initializes market infrastructure in preparation for continuous trading. 

Trading has not yet commenced. 

## 2.6 Open Market 

The market is open. 

Secondary trading is permitted. 

The Market Operations Standard continuously: 

8 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- publishes Reference Prices; 

- evaluates Market Operating Condition; 

- determines Market Operations Profile; 

- monitors market integrity; and 

- supervises execution activity. 

Operational behavior during the Open Market state is governed by the Operational Lifecycle defined below. 

## 2.7 Settlement 

All Contractual Economic Rights have become final. 

Expected Settlement Value converges to contractual settlement value. 

Market execution terminates. 

Settlement processing begins. 

## 2.8 Archived 

The market has completed its lifecycle. 

Trading is permanently closed. 

Historical valuation, operational, quotation, and execution records remain available for replay, audit, regulatory review, and research. 

## Part II — Operational Lifecycle 

## 2.9 Operational Lifecycle 

While a market remains in the Open Market state, every traded security SHALL simultaneously exist in one Operational Lifecycle State. 

9 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



Operational Lifecycle States govern: 

- market behavior; 

- quotation behavior; 

- liquidity policy; 

- operational protection; 

- execution behavior; and 

- market supervision. 

The Operational Lifecycle repeats throughout the Defined Event. 

## 2.10 Operational Lifecycle Progression 

The standard operational sequence is: 

Pre-Game ↓ Live Event ↓ Official Review (if applicable) ↓ Post-Game ↓ **Weekly Financial Report** ↓ Pre-Game 

This sequence repeats for each scheduled competitive contest until the final contest of the Defined Event. 

Following the final contest: 

Final Post-Game ↓ Final Financial Report ↓ Settlement 

10 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 2.11 Operational State Responsibilities 

Each Operational Lifecycle State defines: 

- permissible quotation behavior; 

- market supervision requirements; 

- Market Operations Profile; 

- execution model behavior; 

- operational protection requirements; and 

- transition criteria. 

Operational Lifecycle States SHALL NOT modify: 

- Expected Settlement Value; 

- Reference Price; or 

- Contractual Economic Rights. 

## 2.12 State Transition Authority 

Lifecycle transitions occur only in response to: 

- scheduled lifecycle events; 

- official event status; 

   - publication of official financial reports; 

- 

- approved operational procedures; or 

- authorized emergency actions. 

Every transition SHALL be: 

- deterministic; 

- reproducible; 

- independently auditable; and 

- permanently recorded. 

11 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 2.13 Transition to the Reference Price Engine 

The lifecycle architecture established by this chapter defines **when** market operations occur. 

The Reference Price Engine, defined in Chapter 3, establishes **the operational pricing reference** used throughout those lifecycle states. 

The lifecycle architecture governs the timing of market operation. 

The Reference Price Engine governs the pricing reference upon which market operations are based. 

## **Chapter 3** 

## Reference Price 

## 3.1 Purpose 

This chapter establishes the **Reference Price ("RP")** used throughout the Market Operations Standard. 

The Reference Price is the authoritative operational pricing reference for every InPlay Security. 

It serves as the pricing reference upon which all market operations are performed. 

The Reference Price is not a financial valuation. 

It is the operational publication of the Expected Settlement Value determined by the Financial Valuation Standard (CTS-001). 

12 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 3.2 Relationship to Expected Settlement Value 

The Financial Valuation Standard (CTS-001) continuously determines the Expected Settlement Value ("ESV") of every InPlay Security. 

The Market Operations Standard publishes that valuation as the Reference Price. 

The Market Operations Standard SHALL NOT: 

- determine Expected Settlement Value; 

- modify Expected Settlement Value; 

- reinterpret Expected Settlement Value; or 

- replace Expected Settlement Value with an alternative valuation. 

The Reference Price is the operational representation of the Expected Settlement Value produced by CTS-001. 

## 3.3 Reference Price 

Let 

𝑅𝑃𝑡 

represent the Reference Price of an InPlay Security at time 𝑡. 

Under normal operating conditions, 

𝑅𝑃𝑡 = 𝐸𝑆𝑉𝑡 

where: 

- 𝑅𝑃𝑡= Reference Price at time 𝑡; 

- 𝐸𝑆𝑉𝑡= Expected Settlement Value at time 𝑡. 

This relationship is a constitutional requirement of the Market Operations Standard. 

13 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 3.4 Principle of Reference Price Integrity 

The Reference Price SHALL remain mathematically identical to the corresponding Expected Settlement Value. 

Accordingly, 

𝑅𝑃𝑡 = 𝐸𝑆𝑉𝑡 

shall remain true throughout every Market Lifecycle State and Operational Lifecycle State unless publication is suspended pursuant to an approved operational procedure. 

No subsystem operating under CTS-002 may independently estimate, modify, or replace the Reference Price. 

## 3.5 Reference Price Publication 

For every actively traded InPlay Security, the Market Operations Standard SHALL publish: 

- Reference Price; 

- publication timestamp; 

- valuation timestamp; 

- Market Lifecycle State; 

- Operational Lifecycle State; and 

- publication version. 

These records SHALL permit deterministic reconstruction of every published Reference Price. 

## 3.6 Protected Reference Price State 

Where CTS-001 is temporarily unable to publish an updated Expected Settlement Value because of an approved operational condition, the Market Operations Standard SHALL enter a **Protected Reference Price State** . 

14 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



During this state: 

- the last valid Reference Price remains authoritative; 

- no replacement Reference Price may be calculated; 

- no subsystem operating under CTS-002 may independently estimate a new Reference Price. 

Subsequent market behavior during a Protected Reference Price State is governed by the Market Operating Condition Engine. 

## 3.7 Transition to the Market Operating Condition 

## Engine 

The Reference Price establishes the operational pricing reference for every InPlay Security. 

The Market Operating Condition Engine determines whether the market is capable of operating normally around that Reference Price. 

The Reference Price remains independent of operational capability. 

Operational capability SHALL NOT modify the Reference Price. 

## **Chapter 4** 

## Market Operating Condition 

## 4.1 Purpose 

This chapter establishes the **Market Operating Condition ("MOC")** used throughout the Market Operations Standard. 

The Market Operating Condition represents the authoritative operational assessment of the market's ability to function safely, accurately, and reliably at a given point in time. 

The Market Operating Condition is independent of: 

15 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- Expected Settlement Value; 

- Reference Price; 

- market prices; and 

- quotation behavior. 

## 4.2 Principle of Operational Independence 

The Market Operating Condition evaluates the operational capability of the market. 

It does not: 

- determine Expected Settlement Value; 

- modify the Reference Price; 

- generate Market Operations Profile; or 

- generate executable quotations. 

## 4.3 Operational Inputs 

The Market Operating Condition SHALL be determined from Approved Operational Inputs, which may include: 

#### Valuation Availability 

- Expected Settlement Value availability; 

- valuation publication status; and 

- valuation continuity. 

#### Information Quality 

- data completeness; 

- feed health; 

- feed latency; 

- stale information detection. 

#### System Health 

- communication availability; 

16 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- system integrity; 

- processing health; 

- operational diagnostics. 

#### Market Environment 

- Market Lifecycle State; 

- Operational Lifecycle State; and 

- • official event status. 

Product Technical Standards may define additional Approved Operational Inputs. 

## 4.4 Market Operating Condition 

Let 

𝑀𝑂𝐶𝑡 

represent the Market Operating Condition at time 𝑡. 

The Market Operating Condition is determined by 

𝑀𝑂𝐶𝑡 = 𝐹(𝐴𝑂𝐼𝑡) 

where 

AOI = Approved Operational Inputs. 

Do NOT define F. 

The Market Operating Condition SHALL represent the current operational capability of the Market Operations System. 

Every implementation SHALL publish one—and only one—Market Operating Condition for every actively operating market. 

17 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 4.5 Market Operating Condition Classification 

Every published Market Operating Condition SHALL belong to one of the following classifications: 

- Normal 

- Degraded 

- Protective 

- Recovery 

- Emergency 

Each classification represents a progressively different level of operational capability. 

The classifications themselves do not prescribe market behavior. 

Market behavior is determined exclusively by the Market Operations Profile defined in Chapter 5. 

## 4.6 Deterministic Operational Assessment 

Given identical: 

- Approved Operational Inputs; 

- Market Lifecycle State; 

- Operational Lifecycle State; and 

- implementation version, 

every implementation SHALL produce an identical Market Operating Condition. 

No implementation-specific behavior may alter the resulting operational assessment. 

## 4.7 Market Operating Condition Publication 

Every published Market Operating Condition SHALL include: 

- operating condition classification; 

- publication timestamp; 

18 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- Market Lifecycle State; 

- Operational Lifecycle State; 

- implementation version; and 

- audit identifier. 

Every published Market Operating Condition SHALL be permanently recorded for deterministic replay and regulatory review. 

## 4.8 Transition to Market Operations Profile 

The Market Operating Condition describes the operational capability of the market. 

Chapter 5 defines the **Market Operations Profile** , which determines how the market operates under that condition. 

The Market Operating Condition measures capability. 

The Market Operations Policy determines behavior. 

## **Chapter 5** 

## Market Operations Profile 

## 5.1 Purpose 

This chapter establishes the **Market Operations Profile ("MOP")** governing the operating behavior of every InPlay market. 

The Market Operations Profile defines the operating characteristics that the selected execution model shall implement while the market remains in a given Market Operating Condition. 

The Market Operations Profile SHALL NOT determine Expected Settlement Value, Reference Price, or Market Operating Condition. 

19 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 5.2 Principle of Operational Behavior 

The Market Operations Profile translates the current Market Operating Condition into an operational profile governing market behavior. 

Accordingly, the Market Operations Profile specifies **what the market should look like** , not **how quotes are generated** . 

## 5.3 Inputs 

The Market Operations Profile is determined from: 

- Reference Price; 

- Market Operating Condition; 

- Market Lifecycle State; 

- Operational Lifecycle State; 

- Product Technical Standard configuration; and 

- • Approved Operational Inputs. 

## 5.4 Market Operations Profile 

Every published Market Operations Profile SHALL define, at a minimum: 

- target spread profile; 

- target displayed liquidity; 

- target displayed depth; 

- target quote refresh profile; 

- target aggressiveness; 

- target inventory posture; 

- target protection level. 

𝑀𝑂𝑃𝑡 = 𝐺(𝑅𝑃𝑡, 𝑀𝑂𝐶𝑡, 𝑀𝐿𝑆𝑡, 𝑂𝐿𝑆𝑡, 𝑃𝑇𝑆𝑡) 

The Market Operations Profile constitutes the authoritative operating specification consumed by the execution model. 

20 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 5.5 Operating Profiles 

The Market Operations Standard recognizes the following operating profiles. 

### Stable 

Designed to maximize continuous liquidity under normal operating conditions. 

### Active 

Designed to increase market responsiveness during periods of elevated information flow. 

### Balanced 

Designed to balance liquidity provision with inventory stability. 

### Defensive 

Designed to preserve orderly markets during elevated operational uncertainty. 

### Recovery 

Designed to restore normal operating behavior following a degraded or protective operating condition. 

### Emergency 

Designed to maximize operational safety while preserving market integrity. 

## 5.6 Deterministic Profile Generation 

Given identical: 

- Reference Price; 

- Market Operating Condition; 

- Market Lifecycle State; 

21 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- Operational Lifecycle State; 

- Product Technical Standard configuration; and 

- implementation version, 

every implementation SHALL produce an identical Market Operations Profile. 

## 5.7 Profile Publication 

Every published Market Operations Profile SHALL include: 

- operating profile; 

   - spread profile; 

- 

   - liquidity profile; 

- 

- refresh profile; 

   - protection profile; 

- 

- publication timestamp; 

- implementation version. 

Every published profile SHALL be permanently recorded for replay and audit. 

## 5.8 Transition to the Execution Model 

The Market Operations Profile defines the desired operating characteristics of the market. 

The selected Execution Model implements those operating characteristics. 

22 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## **Chapter 6** 

## Market Interaction Framework 

## 6.1 Purpose 

This chapter establishes the Market Interaction Framework governing how participants interact with every InPlay market. 

The Market Interaction Framework defines the permissible methods by which participants submit, modify, cancel, and execute orders. 

It also establishes the matching principles, execution priority, and order lifecycle applicable to every Product Technical Standard operating under the Market Operations Standard. 

The Market Interaction Framework governs participant interaction. 

It does not govern valuation, market operating policy, or liquidity provision. 

## 6.2 Principle of Equal Access 

All participants SHALL interact with the market under identical interaction rules. 

The Market Interaction Framework SHALL apply uniformly to every participant regardless of account size, trading frequency, or execution model. 

No participant SHALL receive preferential treatment except where expressly authorized by the applicable Product Technical Standard. 

## 6.3 Participant Order Types 

Version 1.0 of the Market Operations Standard recognizes the following participant order types. 

23 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



### Market Order 

An instruction to execute immediately against the best available executable quotations. 

### Limit Order 

An instruction to buy or sell at a specified price or better. 

A Limit Order remains active until: 

- executed; 

- cancelled; 

- replaced; 

- expired; or 

- otherwise terminated pursuant to this standard. 

### Cancel Order 

An instruction requesting cancellation of an active order. 

### Cancel / Replace Order 

An instruction modifying the price, quantity, or other permitted attributes of an active order. 

A Cancel / Replace Order establishes a new order for purposes of execution priority unless otherwise specified by the applicable Product Technical Standard. 

## 6.4 Unsupported Order Types 

The following participant order types are not recognized by Version 1.0 of the Market Operations Standard: 

- Stop Orders 

- Stop Limit Orders 

- Trailing Stop Orders 

- Pegged Orders 

- Hidden Orders 

24 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- Iceberg Orders 

- Reserve Orders 

- Market-if-Touched Orders 

- Cross Orders 

Additional order types may be introduced through future revisions of this standard. 

## 6.5 Order Priority 

Executable orders SHALL be matched according to the following priority hierarchy: 

1. Price Priority 

2. Time Priority 

Orders at superior prices SHALL execute before inferior prices. 

Among orders at identical prices, earlier accepted orders SHALL execute before later accepted orders. 

The applicable Product Technical Standard may define additional tie-breaking rules where required. 

## 6.6 Order Lifecycle 

Every participant order SHALL progress through one or more of the following lifecycle states. 

New ↓ Accepted ↓ Working ↓ Partially Filled ↓ Filled 

or 

25 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



Working ↓ Cancelled 

or 

Working ↓ Replaced 

or 

Working ↓ Expired 

Each state transition SHALL be: 

- deterministic; 

- permanently recorded; 

- independently auditable. 

## 6.7 Order Validation 

Before acceptance, every participant order SHALL be validated against: 

- Market Lifecycle State; 

- Operational Lifecycle State; 

- Product Technical Standard; 

- permitted order type; 

- price constraints; 

- quantity constraints; 

- tick size; 

- security eligibility; and 

- other exchange-defined acceptance criteria. 

Orders failing validation SHALL be rejected. 

26 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 6.8 Matching Principles 

The Market Operations Standard establishes the following matching principles. 

- Orders SHALL execute only against executable quotations. 

- Partial executions are permitted. 

- Remaining quantities retain execution priority unless modified. 

- Executions SHALL occur according to the priority rules established by this chapter. 

- Every execution SHALL be permanently recorded. 

Matching methodology SHALL remain deterministic. 

## 6.9 Execution Model Independence 

The Market Interaction Framework governs participant interaction only. 

The selected Execution Model governs liquidity provision. 

Accordingly: 

- participant interaction rules remain identical regardless of execution model; 

- execution models SHALL conform to the Market Interaction Framework; 

- execution models SHALL NOT modify participant order rights established by this chapter. 

## 6.10 Transition to the Market Execution Engine 

This chapter establishes **how participants interact with the market** . 

The Market Execution Engine, defined in Chapter 7, establishes **how the selected Execution Model responds to those interactions while implementing the Market Operations Profile** . 

Participant interaction and liquidity provision remain independent functions. 

27 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## **Chapter 7** 

## Liquidity Provision Framework 

## 7.1 Purpose 

This chapter establishes the Liquidity Provision Framework governing the provision of executable liquidity within every InPlay market. 

The Liquidity Provision Framework defines the permissible liquidity models recognized by the Market Operations Standard. 

It does not prescribe proprietary quoting algorithms, inventory management methodologies, or internal risk models. 

Those remain the responsibility of the applicable liquidity provider. 

## 7.2 Principle of Liquidity Independence 

The Market Operations Standard governs the operation of the market. 

Liquidity providers govern the proprietary methods used to satisfy their market-making obligations. 

The Market Operations Standard defines the required operational outcomes. 

Liquidity providers determine how those outcomes are achieved subject to the requirements established by CTS-002. 

## 7.3 Supported Liquidity Models 

Version 1.0 recognizes the following liquidity models. 

28 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



### Simulation Designated Market Maker (SDMM) 

Used by simulation markets. 

Characteristics: 

- no proprietary financial risk; 

- no capital constraints; 

- deterministic simulated liquidity; 

- educational market operation. 

### Production Liquidity Provider (PLP) 

Used by regulated production markets. 

Characteristics: 

- proprietary capital; 

- inventory exposure; 

- proprietary risk management; 

- regulatory obligations. 

Additional liquidity models may be introduced through future revisions of this standard. 

## 7.4 Liquidity Provider Responsibilities 

Every liquidity provider SHALL: 

- provide continuous executable quotations where required; 

- operate within the applicable Market Operations Profile; 

- comply with all Product Technical Standards; 

- satisfy exchange operational requirements; and 

- maintain complete operational auditability. 

The Market Operations Standard does not prescribe the proprietary methods used to satisfy these responsibilities. 

29 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 7.5 Market Operations Standard Responsibilities 

The Market Operations Standard SHALL define: 

- market states; 

- participant interaction rules; 

- Reference Price; 

- Market Operating Condition; 

- Market Operations Profile; and 

- required market behavior. 

The Market Operations Standard SHALL NOT prescribe proprietary inventory models, capital allocation methodologies, hedging methodologies, or internal risk systems used by a liquidity provider. 

## 7.6 Transition to Market Execution 

This chapter establishes **who provides liquidity** . 

The following chapter defines **how executable quotations are generated** within the selected liquidity model. 

## **Chapter 8** 

## Liquidity Provider Execution Engine 

## 8.1 Purpose 

The Liquidity Provider Execution Engine ("LPEE") continuously generates executable quotations for every actively traded InPlay Security. 

The LPEE implements the selected Execution Model while conforming to the Market Operations Standard and the applicable Product Technical Standard. 

The LPEE does not determine: 

30 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- Expected Settlement Value; 

- Reference Price; 

- Market Operating Condition; 

- Market Operations Profile; or 

- • participant interaction rules. 

## 8.2 Constitutional Responsibility 

The Liquidity Provider Execution Engine transforms the operational framework established by this standard into executable market quotations. 

The LPEE implements market operation. 

It SHALL NOT establish market policy. 

Accordingly, every quotation produced by the LPEE SHALL conform to: 

- the Reference Price; 

- the Market Operating Condition; 

- the Market Operations Profile; 

- the Market Interaction Framework; 

- the selected Execution Model; and 

- the applicable Product Technical Standard. 

## 8.3 Execution Inputs 

The Liquidity Provider Execution Engine continuously consumes: 

𝐸𝐼𝑡 = (𝑅𝑃𝑡, 𝑀𝑂𝐶𝑡, 𝑀𝑂𝑃𝑡, 𝑀𝐼𝐹𝑡, 𝐸𝑀𝑡, 𝑃𝑇𝑆𝑡) 

Execution Models that assume proprietary financial risk MAY additionally consume proprietary internal risk controls. 

Those proprietary controls remain outside the scope of the Market Operations Standard. 

31 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 8.4 Execution Outputs 

Let 

𝑄𝑡 

represent the Executable Quotation at time 𝑡. 

The Executable Quotation SHALL consist of the following constitutional elements: 

𝑄𝑡 = (𝐵𝑡, 𝑂𝑡, 𝑄𝐵,𝑡, 𝑄𝑂,𝑡, 𝐷𝑡, 𝑅𝑡, 𝑆𝑡, 𝑃𝑡) 

where: 

- 𝐵𝑡= Executable Bid Quotation; 

- 𝑂𝑡= Executable Offer Quotation; 

- 𝑄𝐵,𝑡= Displayed Bid Quantity; 

- 𝑄𝑂,𝑡= Displayed Offer Quantity; 

- 𝐷𝑡= Displayed Market Depth; 

- 𝑅𝑡= Quotation Refresh Profile; 

- 𝑆𝑡= Quotation Status; and 

- 𝑃𝑡= Quotation Priority Attributes. 

Every Executable Quotation SHALL contain each of the constitutional elements defined above. 

Additional quotation attributes may be defined by the applicable Product Technical Standard, provided such attributes do not alter the constitutional structure of the Executable Quotation established by this standard. 

## 8.5 Deterministic Execution 

Given identical: 

- Reference Price; 

- Market Operating Condition; 

32 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- Market Operations Profile; 

- Market Interaction Framework; 

- selected Execution Model; 

- Product Technical Standard configuration; and 

- implementation version, 

every conforming implementation SHALL produce identical executable quotations. 

No implementation-specific behavior may alter the resulting quotations except where expressly permitted by the selected Execution Model. 

## 8.6 Execution Model Independence 

The Market Operations Standard recognizes multiple execution models. 

Execution models may differ in their internal implementation, including: 

- inventory management; 

- proprietary risk management; 

- capital allocation; 

- quotation optimization; and 

- internal execution algorithms. 

These implementation differences SHALL NOT alter the constitutional operating requirements established by CTS-002. 

Compliance with this standard shall be evaluated based upon required market behavior rather than proprietary implementation. 

## 8.7 Transition to Quote Generation Mathematics 

The preceding sections define the functional responsibilities of the Liquidity Provider Execution Engine. 

The following sections establish the canonical mathematical models governing: 

- spread determination; 

- bid price generation; 

33 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- offer price generation; 

- displayed quantity; 

- displayed market depth; 

- quotation refresh; 

- quotation replacement; and 

- quotation randomization. 

These mathematical models define the constitutional behavior of every execution model operating under the Market Operations Standard. 

## **Chapter 9** 

## Market Construction Mathematics 

## 9.1 Purpose 

This chapter establishes the mathematical framework governing the construction of executable markets for InPlay Securities. 

The Market Construction Mathematics transforms the constitutional market objects defined by CTS-001, CTS-002, and the applicable Product Technical Standard into executable quotations. 

These mathematical models apply uniformly to every Execution Model recognized by the Market Operations Standard. 

## Part I — Constitutional Laws of Market Construction 

## 9.2 Law of Deterministic Market Construction 

Every executable market SHALL be produced deterministically. 

Given identical: 

34 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- Expected Settlement Value; 

- Reference Price; 

- Market Operating Condition; 

- Market Operations Profile; 

- Execution Model; 

- Product Technical Standard configuration; and 

- • implementation version, 

every conforming implementation SHALL produce an identical market configuration and executable quotation. 

## 9.3 Law of Constitutional Independence 

Market Construction Mathematics SHALL NOT: 

- determine Expected Settlement Value; 

- modify Reference Price; 

- determine Market Operating Condition; 

- determine Market Operations Profile; or 

- redefine participant interaction rules. 

These constitutional market objects are inputs to market construction. 

They are never outputs. 

## Part II — Market Configuration 

## 9.4 Market Configuration 

Before generating executable quotations, the Liquidity Provider Execution Engine SHALL construct one Market Configuration. 

The Market Configuration represents the intended operating characteristics of the market at a particular point in time. 

It is an internal mathematical object. 

35 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 

It is not disseminated to market participants. 



## 9.5 Market Configuration Function 

Let 

𝑀𝐶𝑡 

represent the Market Configuration at time 𝑡. 

The Market Configuration is determined by 

𝑀𝐶𝑡 = 𝐾(𝑅𝑃𝑡, 𝑀𝑂𝐶𝑡, 𝑀𝑂𝑃𝑡, 𝐸𝑀𝑡, 𝑃𝑇𝑆𝑡) 

where: 

- 𝑅𝑃𝑡= Reference Price; 

- 𝑀𝑂𝐶𝑡= Market Operating Condition; 

- 𝑀𝑂𝑃𝑡= Market Operations Profile; 

- 𝐸𝑀𝑡= selected Execution Model; and 

- 𝑃𝑇𝑆𝑡= Product Technical Standard configuration. 

The Market Configuration completely defines the intended operating characteristics of the market before quotations are generated. 

## 9.6 Market Configuration Components 

Every Market Configuration SHALL define: 

- spread profile; 

- displayed liquidity profile; 

- displayed depth profile; 

- refresh profile; 

- inventory posture (where applicable); 

- protection profile. 

36 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



Product Technical Standards may extend the Market Configuration without altering its constitutional structure. 

## Part III — Executable Quotation 

## 9.7 Executable Quotation Function 

The executable quotation is generated from the Market Configuration. 

Let 

𝑄𝑡 

represent the executable quotation at time 𝑡. 

The quotation function is 

<u>𝑄𝑡</u> = 𝐻(𝑅𝑃𝑡, 𝑀𝐶𝑡) 

The quotation function transforms the Reference Price and Market Configuration into an executable market quotation. 

## 9.8 Executable Quotation Structure 

The executable quotation consists of the following elements: 



where: 

- 𝐵𝑡= bid quotation; 

- 𝑂𝑡= offer quotation; 

37 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- 𝑆𝐵,𝑡= displayed bid quantity; 

- 𝑆 𝑂,𝑡= displayed offer quantity; 

- 𝐷𝑡= displayed market depth; 

- 𝑅𝑡= quotation refresh profile; and 

- 𝑃𝑡= quotation priority attributes. 

Every executable quotation SHALL contain each of these elements. 

## Part IV — Functional Decomposition 

## 9.9 Quotation Functions 

The executable quotation is mathematically decomposed into the following independent functions: 

- Bid Price Function 

- Offer Price Function 

- Displayed Quantity Function 

- Displayed Depth Function 

- Refresh Function 

- Replacement Function 

- Randomization Function 

Each function determines one component of the executable quotation. 

No function may modify another constitutional market object. 

## 9.10 Transition to Component Mathematics 

The following sections define the canonical mathematical models governing each quotation function. 

Every quotation function SHALL conform to: 

- the Constitutional Laws of Market Construction; 

- the Market Configuration Function; and 

38 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- the Executable Quotation Function established by this chapter. 

## 9.11 Purpose 

The Market Configuration defines the intended characteristics of the executable market before individual quotations are generated. 

Every executable quotation SHALL be derived from the Market Configuration established by this section. 

## 9.12 Market Configuration Function 

The Market Configuration consists of a collection of independently determined operating functions. 

𝑀𝐶𝑡 = (𝑆𝑃𝑡, 𝐿𝑃𝑡, 𝐷𝑃𝑡, 𝑅𝐹𝑡, 𝐼𝑃𝑡, 𝑃𝑃𝑡) 

where: 

- 𝑆𝑃𝑡= Spread Profile 

- 𝐿𝑃𝑡= Liquidity Profile 

- 𝐷𝑃𝑡= Depth Profile 

- 𝑅𝐹𝑡= Refresh Profile 

- 𝐼𝑃𝑡= Inventory Profile (Execution Model dependent) 

- 𝑃𝑃𝑡= Protection Profile 

## 9.13 Independence of Configuration Functions 

Each Market Configuration Function SHALL be determined independently. 

The determination of one configuration function SHALL NOT redefine another. 

39 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



The resulting Market Configuration represents the complete intended operating characteristics of the market. 

## 9.14 Transition to Component Functions 

The following sections define the mathematical determination of: 

- Spread Profile 

- Liquidity Profile 

   - Depth Profile 

- 

   - Refresh Profile 

- 

   - Inventory Profile (where applicable) 

- 

   - Protection Profile 

- 

Each profile contributes one component to the complete Market Configuration. 

## Part V — Market Configuration Functions 

## 9.15 Purpose 

The Market Configuration Functions determine the operating characteristics of the market prior to the generation of executable quotations. 

Each function determines one independent component of the Market Configuration. 

Collectively, the functions define the complete operating characteristics that the selected Execution Model SHALL implement. 

No Market Configuration Function may modify: 

- Expected Settlement Value; 

- Reference Price; 

- Market Operating Condition; 

- Market Operations Profile; or 

- participant interaction rules. 

40 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



Those constitutional market objects remain immutable inputs. 

## 9.16 Principle of Functional Independence 

Each Market Configuration Function SHALL operate independently. 

The output of one function SHALL NOT redefine the constitutional purpose of another function. 

Interaction between functions is permitted only through the resulting Market Configuration. 

This separation ensures: 

- deterministic operation; 

- independent verification; 

- modular implementation; 

- extensibility through future Product Technical Standards. 

## 9.17 Market Configuration Functions 

Version 1.0 recognizes the following Market Configuration Functions: 

1. Spread Profile Function 

2. Liquidity Profile Function 

3. Depth Profile Function 

4. Refresh Profile Function 

5. Inventory Profile Function (Execution Model dependent) 

6. Protection Profile Function 

Each function contributes one independent operating characteristic to the Market Configuration. 

41 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 9.18 Functional Responsibilities 

### Spread Profile Function 

Determines the target spread characteristics of the market. 

It does not determine executable bid or offer prices. 

### Liquidity Profile Function 

Determines the desired liquidity characteristics of the market. 

It specifies the target liquidity environment to be implemented by the selected Execution Model. 

### Depth Profile Function 

Determines the desired characteristics of displayed market depth. 

It specifies the intended depth structure. 

It does not determine individual displayed quotations. 

### Refresh Profile Function 

Determines the desired quotation refresh behavior. 

It specifies the intended responsiveness of executable quotations. 

### Inventory Profile Function 

Where supported by the selected Execution Model, the Inventory Profile Function specifies the desired inventory operating posture. 

The constitutional standard defines only the operating objective. 

Execution-model-specific inventory methodologies are defined by the applicable Product Technical Standard. 

42 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



### Protection Profile Function 

Determines the operational protections required under the current Market Operations Profile. 

Protection mechanisms remain independent of valuation and participant interaction. 

## 9.19 Transition to Execution Conformance 

The Market Configuration Functions determine **what operating characteristics the market should exhibit** . 

The following mathematical models determine **how those characteristics are transformed into executable quotations** by the selected Execution Model. 

## Part VI — Execution Conformance 

## 9.20 Purpose 

This section establishes the constitutional execution requirements applicable to every Execution Model recognized by the Market Operations Standard. 

The purpose of these requirements is to ensure that every conforming Execution Model produces executable quotations that faithfully implement the published Market Configuration while preserving deterministic market behavior. 

## 9.21 Principle of Configuration Conformance 

Every Execution Model SHALL faithfully implement the Market Configuration published by the Market Operations Standard. 

Execution Models may differ in their internal implementation. 

They SHALL NOT alter the intended operating characteristics established by the Market Configuration. 

43 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



Accordingly, every executable quotation SHALL conform to the applicable: 

- Reference Price; 

- Market Operating Condition; 

- Market Operations Profile; 

- Market Configuration; and 

- Product Technical Standard. 

## 9.22 Principle of Deterministic Execution 

Given identical constitutional inputs, every conforming Execution Model SHALL produce operationally equivalent executable quotations. 

Equivalent execution does not require identical internal algorithms. 

Equivalent execution requires identical externally observable market behavior. 

This distinction permits implementation flexibility while preserving constitutional consistency. 

## 9.23 Principle of Execution Independence 

Execution Models MAY employ proprietary methodologies, including: 

- inventory management; 

- capital allocation; 

- quotation optimization; 

- replenishment algorithms; 

- internal protection mechanisms; and 

- execution heuristics. 

Such methodologies SHALL NOT violate the constitutional requirements established by this standard. 

Compliance shall be evaluated based upon externally observable market behavior rather than proprietary implementation. 

44 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 9.24 Execution Outputs 

Every conforming Execution Model SHALL continuously generate **Executable Quotations** that faithfully implement the published Market Configuration. 

At a minimum, every Executable Quotation SHALL include: 

- Executable Bid Quotation; 

- Executable Offer Quotation; 

- Displayed Bid Quantity; 

- Displayed Offer Quantity; 

- Displayed Market Depth; 

- Quotation Refresh Profile; 

- **Quotation Status** ; 

- Quotation Priority Attributes; and 

- Quotation Timestamp. 

Additional quotation attributes MAY be defined by the applicable Product Technical Standard, provided such attributes do not alter the constitutional structure of the Executable Quotation established by this standard. 

## 9.25 Deterministic Replay 

Every execution decision SHALL be reproducible using: 

- the published Reference Price; 

- the published Market Operating Condition; 

- the published Market Operations Profile; 

   - the published Market Configuration; 

- 

- the Product Technical Standard; 

- the implementation version; and 

- the recorded participant interactions. 

A conforming implementation SHALL permit deterministic reconstruction of every published quotation and every resulting execution. 

45 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 9.26 Transition to Product Technical Standards 

CTS-002 establishes the constitutional requirements governing market operation and execution. 

Product Technical Standards define the product-specific methodologies used to satisfy those constitutional requirements. 

Such methodologies may include: 

- inventory management; 

- liquidity surface construction; 

- quotation evolution; 

- refresh methodologies; 

- depth management; 

- execution optimization; and 

- other product-specific operating behavior. 

No Product Technical Standard may redefine the constitutional requirements established by CTS-002. 

46 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 

