---
description: "InPlay's authoritative PTS-001 standard (v1.0, PDF-converted) — SDMM engine architecture, decision cycle, pricing profiles, and deterministic replay rules"
---

## JULY 2, 2026 

# INPLAY CORE TECHNICAL STANDARDS PTS-001 SIMULATED DESIGNATED MARKET MAKER STANDARD (SDMM-1) 

EDWIN JOHNSON INPLAY GLOBAL, INC. 333 SE 2nd Avenue, Suite 2000 Miami, Florida 33131 



## **TRADE SECRET OF INPLAY GLOBAL, INC.** 

This document contains confidential, proprietary, and trade secret information of InPlay Global, Inc. It is furnished solely for authorized evaluation, development, implementation, legal review, or other approved business purposes. Unauthorized use, copying, disclosure, distribution, reproduction, reverse engineering, or derivative use of any portion of this document is strictly prohibited without the prior written consent of InPlay Global, Inc. 

## **INPLAY CORE TECHNICAL STANDARDS** 

## PTS-001 

### Simulation Designated Market Maker Standard (SDMM-1) 

#### Chapter 1 — Constitutional Principles 

## 1.1 Authority 

The Simulation Designated Market Maker Standard ("SDMM”) establishes the authoritative engineering standard governing the operation of the SDMM used within InPlay simulation markets. 

This standard defines the reference implementation responsible for constructing executable quotations while conforming to the constitutional requirements established by CTS-001 and CTS-002. 

All simulation market-making implementations SHALL conform to this standard unless expressly superseded by an approved revision. 

1 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 1.2 Relationship to CTS-001 and CTS-002 

The SDMM Standard implements the constitutional requirements established by: 

- CTS-001 Financial Valuation Standard; and 

- CTS-002 Market Operations Standard. 

CTS-001 determines value. 

CTS-002 governs market operation. 

PTS-001 specifies the engineering methodology used by the SDMM to implement those constitutional requirements. 

Where a conflict exists, the constitutional standards govern. 

## 1.3 Purpose 

The purpose of the SDMM is to continuously generate realistic, executable two-sided quotations for simulation markets. 

The SDMM provides continuous liquidity without assuming proprietary financial risk. 

The SDMM is designed to: 

- provide continuous executable liquidity; 

- maintain orderly markets; 

- produce realistic quotation behavior; 

- support educational objectives; 

- enable deterministic replay; and 

- faithfully implement the constitutional market objects established by CTS-001 and CTS-002. 

2 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 1.4 Fundamental Principle 

The purpose of the SDMM is **not** to predict market prices. 

The purpose of the SDMM is to construct a continuously tradable market around the Reference Price published by CTS-001 and the Market Operations Profile established by CTS-002. 

The SDMM SHALL NOT independently determine: 

- Expected Settlement Value; 

- Reference Price; 

- Market Operating Condition; 

- Market Operations Profile; or 

- participant interaction rules. 

Those constitutional objects are consumed by the SDMM. 

They are never produced by it. 

## 1.5 Engineering Principles 

Every SDMM implementation SHALL satisfy the following principles. 

#### Principle 1 — Continuous Liquidity 

Executable two-sided quotations SHALL be continuously maintained throughout every interval during which the applicable Market Operations Profile authorizes executable trading. 

#### Principle 2 — Deterministic Operation 

Given identical constitutional inputs, identical configuration, and identical event sequence, every conforming implementation SHALL produce identical market behavior. 

3 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



#### Principle 3 — Inventory Awareness 

The SDMM SHALL continuously monitor its inventory posture while maintaining uninterrupted market-making responsibilities. 

#### Principle 4 — Continuous Market Presence 

Inventory management SHALL NOT prevent the SDMM from continuously maintaining executable bid and offer quotations. 

#### Principle 5 — Production-Consistent Market Behavior 

Displayed quotations SHALL evolve in a manner that reasonably reflects the operating characteristics defined by the applicable Market Operations Profile. 

#### Principle 6 — Replayability 

Every quotation, execution, inventory adjustment, and protection action SHALL be reproducible through deterministic replay. 

### Principle 7 — Engineering Isolation 

The SDMM SHALL operate exclusively from constitutional inputs and approved engineering configuration. 

The SDMM SHALL NOT introduce external pricing inputs except where expressly authorized by the governing Product Technical Standard. 

## 1.6 Scope 

This standard governs: 

- Executable Market construction; 

- Market Posture determination; 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 

4 



- Price Formation; 

- Market Structure construction; 

- Displayed Quantity generation; 

- Market Adaptation; 

- Quote Construction; 

- Decision Cycle operation; and 

- Verification and Deterministic Replay. 

This standard SHALL NOT govern: 

- valuation; 

- settlement; 

- regulation; 

- participant rights; and 

- compliance. 

## 1.7 Engineering Architecture 

##### **CTS-001** 

Expected Settlement Value 

- 

##### **CTS-002** 

Reference Price 

- 

Market Operating Condition 

- 

Market Operations Profile 

▼ 

##### **PTS-001** 

Executable Market 

▼ 

5 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



Market Posture Engine 

##### ▼ 

Price Formation Engine 

##### ▼ 

Market Structure Engine 

##### ▼ 

Displayed Quantity Engine 

##### ▼ 

Market Adaptation Engine 

##### ▼ 

Quote Construction Engine 

▼ 

Executable Order Book 

▼ 

Participant Interaction 

▼ 

Decision Cycle Engine 

▼ 

Verification & Deterministic Replay 

## 1.8 Constitutional Invariants 

The following SHALL remain true regardless of Product Technical Standard: 

- Expected Settlement Value is externally determined. 

- Reference Price is externally determined. 

- Market Operations Profile is externally determined. 

- • SDMM consumes but never creates constitutional objects. 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 

6 



- Deterministic replay remains mandatory. 

- Continuous executable markets remain mandatory unless suspended under CTS002. 

## **Chapter 2** 

## Simulation Market Architecture 

## 2.1 Purpose 

This chapter establishes the architecture governing simulation markets operating under the SDMM Standard. 

Simulation markets are designed to provide participants with a realistic market environment while eliminating proprietary financial exposure. 

Every simulation market SHALL conform to the constitutional requirements established by CTS-001 and CTS-002 and the engineering requirements established by this standard. 

## 2.2 Simulation Market Characteristics 

Every simulation market SHALL exhibit the following characteristics: 

- continuously published Reference Prices; 

- continuous executable two-sided quotations; 

- deterministic market operation; 

- simulated executions; 

- simulated inventory; 

- simulated participant portfolios; 

- deterministic replay. 

Simulation markets SHALL replicate the operational characteristics of production markets except where expressly modified by this standard. 

7 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 2.3 Simulation Capital 

Simulation capital exists solely for participation within simulation markets. 

Simulation capital: 

- possesses no monetary value; 

- may not be redeemed for cash; 

- may not be transferred between participants; 

- exists exclusively for simulation trading. 

Product Technical Standards may define competition-specific capital allocation methodologies. 

## 2.4 Simulation Executions 

Every accepted participant order SHALL execute according to the Market Interaction Framework established by CTS-002. 

Simulation executions SHALL: 

- update participant positions; 

- update participant cash balances; 

- update SDMM inventory; 

- generate deterministic execution records. 

Simulation executions SHALL NOT create financial obligations. 

## 2.5 Simulation Inventory 

The SDMM SHALL maintain simulated inventory for each Team Company. 

8 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



Simulation inventory exists solely to support realistic market-making behavior. 

Simulation inventory SHALL: 

- maintain continuous liquidity; 

- support inventory-aware quotation behavior; 

- support deterministic replay; 

- support engineering analysis. 

Simulation inventory SHALL NOT represent proprietary financial exposure. 

## 2.6 Simulation Market Integrity 

Simulation markets SHALL preserve: 

- orderly market behavior; 

- continuous liquidity; 

- deterministic operation; 

- replayability; 

- participant fairness. 

The absence of proprietary financial risk SHALL NOT reduce operational standards. 

Simulation market operation SHALL remain computationally indistinguishable from production market operation except where expressly modified by this standard. 

## 2.7 Simulation Objectives 

Simulation markets are intended to: 

- educate participants; 

- evaluate trading strategies; 

- evaluate market-making methodologies; 

- evaluate inventory methodologies; 

- evaluate liquidity methodologies; 

- evaluate market evolution methodologies. 

9 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



The simulation environment therefore serves both participant education and engineering research. 

## 2.8 Transition to Executable Market Construction 

The preceding sections establish the operating environment of the simulation market. 

The following chapter establishes the engineering methodology used by the SDMM to construct the Executable Market that forms the foundation of every subsequent engineering decision. 

## **Chapter 3** 

## Executable Market Construction 

## 3.1 Purpose 

This chapter establishes the engineering methodology used by the SDMM to construct an Executable Market. 

The Executable Market represents the complete set of executable liquidity made available to market participants at a particular point in time. 

Every Executable Quotation published by the SDMM SHALL be derived from the Executable Market constructed under this chapter. 

## 3.2 Fundamental Principle 

The SDMM does not construct isolated quotations. 

10 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



It constructs an Executable Market. 

Executable bid quotations, executable offer quotations, displayed market depth, displayed quantities, and quotation refresh behavior are all derived from the Executable Market. 

The Executable Market therefore represents the primary engineering object of the SDMM. 

## 3.3 Constitutional Inputs 

The Executable Market SHALL be constructed exclusively from constitutional market objects published by CTS-001 and CTS-002. 

These inputs include: 

- Reference Price; 

- Market Operating Condition; 

- Market Operations Profile; 

- Execution Model configuration; 

- Product Technical Standard configuration. 

The SDMM SHALL NOT independently determine or modify any constitutional market object. 

## 3.4 Executable Market 

Let 

𝐸𝑀𝑡 

represent the Executable Market at time 𝑡. 

The Executable Market is determined by 

𝐸𝑀𝑡 = 𝑓(𝑅𝑃𝑡, 𝑀𝑂𝐶𝑡, 𝑀𝑂𝑃𝑡, 𝐶𝐹𝐺𝑡) 

11 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



where 

- 𝐸𝑀𝑡= Executable Market 

- 𝑅𝑃𝑡= Reference Price 

- 𝑀𝑂𝐶𝑡= Market Operating Condition 

- • 𝑀𝑂𝑃𝑡= Market Operations Profile 

- 𝐶𝐹𝐺𝑡= SDMM Configuration 

The Executable Market defines the complete liquidity environment from which executable quotations are derived. 

## 3.5 Executable Market Components 

Every Executable Market SHALL define: 

- executable price structure; 

- executable liquidity structure; 

- executable market depth; 

- quotation generation parameters; 

- quotation refresh parameters; 

- protection parameters. 

The Executable Market does not itself constitute a published quotation. 

## 3.6 Engineering Independence 

The Executable Market is an internal engineering object. 

It SHALL NOT: 

- determine Expected Settlement Value; 

- determine Reference Price; 

- determine Market Operating Condition; 

- determine Market Operations Profile; 

- modify participant interaction. 

Those remain constitutional inputs. 

12 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 3.7 Engineering Outputs 

The Executable Market continuously supplies the information required to construct: 

- Executable Order Book; 

- Executable Quotations; 

- quotation refresh; 

- quotation replacement; 

- inventory management; 

- protection mechanisms. 

Subsequent chapters define each of these engineering subsystems. 

The Executable Market SHALL become the authoritative engineering input to the Market Objective Engine during the current Decision Cycle. 

## 3.8 Transition to Executable Order Book Construction 

The following chapter establishes the Market Posture Engine, which determines the SDMM's operating behavior within the Executable Market. 

## **Chapter 4** 

## Market Objective Engine 

## 4.1 Purpose 

This chapter establishes the engineering methodology used by the SDMM to determine its operational objectives for the current Decision Cycle. 

The Market Objective Engine is the primary decision-making component of the SDMM. 

Before determining prices, liquidity, market structure, or displayed quotations, the SDMM SHALL first determine the objectives it seeks to achieve during the current Decision Cycle. 

13 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



All subsequent engineering engines SHALL operate in a manner consistent with the Market Objectives established by this chapter. 

## 4.2 Fundamental Principle 

The SDMM is a deterministic decision system whose primary purpose is to provide continuous executable two-sided liquidity while pursuing profitable long-term market-making performance within the constraints established by this standard. 

Every Decision Cycle SHALL begin by determining the operational objectives that govern the SDMM's behavior. 

Those objectives SHALL remain authoritative throughout the current Decision Cycle unless superseded by a subsequent Decision Cycle. 

## 4.3 Constitutional Inputs 

The Market Objective Engine SHALL consume: 

- Reference Price; 

- Market Operating Condition; 

- Market Operations Profile; 

- Executable Market; 

- Product Technical Standard configuration. 

The Market Objective Engine SHALL NOT modify any constitutional market object. 

## 4.4 Market Assessment 

Before determining Market Objectives, the SDMM SHALL assess the current market environment. 

The Market Assessment SHALL evaluate, at a minimum: 

- External Market Phase; 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 

14 



- Order Arrival Rate; 

- Order Flow Acceleration; 

- Fill Velocity; 

- Quote Lifetime; 

- Book Consumption Rate; 

- Inventory Position; 

- Inventory Velocity; 

- Protection State. 

Additional assessment inputs may be introduced by future revisions of this standard. 

The Market Assessment does not determine market behavior. 

It provides the information necessary to determine Market Objectives. 

## 4.5 Operational Objectives 

The SDMM SHALL simultaneously pursue the following operational objectives: 

1. Maintain continuous executable two-sided liquidity. 

2. Maintain orderly and realistic market behavior. 

3. Maintain inventory within the active Inventory Risk Profile. 

4. Maximize long-term expected market-making performance. 

5. Rapidly incorporate constitutional market changes. 

6. Preserve deterministic operation and replayability. 

These objectives govern every subsequent engineering decision. 

When objectives conflict, they SHALL be prioritized in accordance with Section 4.6. 

## 4.6 Objective Priority 

Operational objectives SHALL be satisfied in the following order of precedence: 

1. Protection Requirements 

2. Continuous Market Availability 3. Market Integrity 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 

15 



4. Inventory Stability 

5. Market Quality 

6. Long-Term Market-Making Performance 

Lower-priority objectives SHALL NOT cause higher-priority objectives to be violated. 

## 4.7 Engineering Outputs 

The Market Objective Engine SHALL produce: 

- Effective Market State; 

- Inventory Risk Profile; 

- Liquidity Budget; 

- Pricing Profile. 

These outputs become the authoritative inputs to the Market Pricing Engine. 

## 4.8 Engineering Independence 

The Market Objective Engine SHALL NOT determine: 

- Reservation Prices; 

- Market Structure; 

- Displayed Quantities; 

- Executable Quotations. 

Those engineering responsibilities belong to subsequent chapters. 

## 4.9 Runtime Authority 

The outputs of the Market Objective Engine SHALL remain authoritative throughout the active Decision Cycle. 

Subsequent engineering engines SHALL operate consistently with those outputs until superseded by the next Decision Cycle. 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 

16 



## 4.10 Transition 

The Market Objective Engine determines the objectives, operating state, and pricing framework governing the current Decision Cycle. 

The following chapter establishes the **Issuer Market Making Engine** , which transforms those objectives into Reservation Prices, executable market structure, and pricing behavior. 

## **Chapter 5** 

### Portfolio Allocation Engine 

### 5.1 Purpose 

This chapter establishes the engineering methodology used by the Simulation Designated Market Maker ("SDMM") to manage portfolio-wide capital, inventory, liquidity, and risk for a single Portfolio during each Decision Cycle. 

For purposes of this standard, a **Portfolio** is a defined collection of Team Companies governed by a common Product Technical Standard and funded by a dedicated capital pool. 

Examples include: 

- NFL Portfolio (32 Team Companies); and 

- NCAA Division I Football Portfolio (131 Team Companies). 

Each Portfolio SHALL maintain its own: 

- Portfolio Capital; 

- Portfolio Liquidity Budget; 

- aggregate Portfolio Inventory; 

- Issuer Liquidity Budgets; 

- Portfolio Risk Limits; and 

- Portfolio Allocation Map. 

17 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



Portfolio resources SHALL NOT be shared across Portfolios unless expressly authorized by the applicable Product Technical Standard. 

The Portfolio Risk and Capital Allocation Engine determines portfolio-wide resource allocation before issuer-level Market Making Engines construct executable markets. 

The Portfolio Risk and Capital Allocation Engine is the enterprise-level decision engine for a single Portfolio. 

## 5.2 Governing Objective 

The Portfolio Allocation Engine SHALL allocate portfolio resources to maximize long-term expected market-making performance while maintaining prudent portfolio-wide liquidity and inventory risk throughout the active Portfolio. 

Portfolio allocation decisions SHALL remain consistent with: 

- constitutional market requirements; 

- Protection Requirements; 

- Portfolio Capital; 

- Portfolio Liquidity Budget; 

- Portfolio Inventory Risk Limits; 

- active Market Objectives; and 

- the applicable Product Technical Standard. 

Portfolio allocation decisions SHALL take precedence over issuer-level Market Making decisions within the active Portfolio. 

The Portfolio Allocation Engine SHALL continuously seek to: 

- maximize executable liquidity across the active Portfolio; 

- allocate market-making capacity among Team Companies according to portfolio objectives; 

- maintain portfolio-wide inventory within established limits; 

- preserve adequate Portfolio Capital throughout the active Decision Cycle; and 

- ensure deterministic and reproducible allocation decisions. 

18 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



The Portfolio Allocation Engine SHALL NOT allocate Portfolio Capital, Portfolio Liquidity, or Issuer Liquidity Budgets in a manner that violates higher-priority constitutional or protection requirements. 

## 5.3 Portfolio Allocation Priority 

When portfolio-wide conditions conflict with issuer-level market-making objectives, the Portfolio Allocation Engine SHALL allocate portfolio resources according to the following priority: 

1. Protection Requirements; 

2. Constitutional Market Requirements; 

3. Portfolio Capital Preservation; 

4. Portfolio Liquidity Requirements; 

5. Portfolio Inventory Risk Limits; 

6. Issuer Liquidity Allocation; 

7. Issuer-Level Market Quality. 

Lower-priority objectives SHALL NOT cause higher-priority portfolio allocation constraints to be violated. 

Issuer-level Market Making Engines SHALL NOT override Portfolio Allocation decisions established during the current Decision Cycle. 

Portfolio allocation decisions SHALL remain authoritative throughout the active Decision Cycle unless superseded by a subsequent Decision Cycle. 

## 5.4 Portfolio Inputs 

The Portfolio Allocation Engine SHALL consume the following portfolio-wide inputs during every Decision Cycle: 

#### Constitutional Inputs 

- Effective Market State; 

- Market Objectives; 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 

19 



- Protection Requirements; and 

- applicable Product Technical Standard configuration. 

#### Portfolio Inputs 

- Portfolio Capital; 

- Portfolio Liquidity Budget; 

- Portfolio Inventory; 

- Portfolio Inventory Risk Limits; 

- Active Team Companies; and 

- Portfolio Allocation Map from the preceding Decision Cycle. 

#### Issuer Inputs 

For every active Team Company within the Portfolio: 

- Issuer Inventory; 

- Issuer Market Activity Assessment; 

- Issuer Liquidity Budget from the preceding Decision Cycle; 

- Issuer Effective Market State; and 

- Issuer Protection State. 

The Portfolio Allocation Engine SHALL NOT modify constitutional market objects established by CTS-001 or CTS-002. 

The Portfolio Allocation Engine SHALL consume portfolio and issuer state information as read-only engineering inputs when determining portfolio-wide resource allocation. 

## 5.5 Portfolio Assessment 

The Portfolio Allocation Engine SHALL continuously evaluate the operational condition of the active Portfolio during every Decision Cycle. 

The Portfolio Assessment SHALL determine, at a minimum: 

- Portfolio Capital Utilization; 

- Portfolio Liquidity Utilization; 

- Portfolio Inventory Position; 

20 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- Portfolio Inventory Concentration; 

- Issuer Activity Distribution; 

- Portfolio Market Activity; 

- Portfolio Protection State; and 

- Portfolio Allocation Stability. 

The Portfolio Assessment SHALL classify the active Portfolio into an operational state that governs portfolio-wide resource allocation for the current Decision Cycle. 

The applicable Product Technical Standard SHALL define the mathematical methodology used to determine Portfolio Assessment classifications. 

Portfolio Assessment SHALL be completed before Portfolio Liquidity Budgets or Issuer Liquidity Budgets are determined. 

## 5.6 Portfolio Liquidity Budget 

The Portfolio Allocation Engine SHALL determine the Portfolio Liquidity Budget available during the current Decision Cycle. 

The Portfolio Liquidity Budget represents the maximum aggregate executable liquidity that may be allocated across all active Team Companies within the Portfolio. 

The Portfolio Liquidity Budget SHALL be determined as a function of: 

- Portfolio Capital; 

- Portfolio Assessment; 

- Portfolio Inventory Risk; 

- Protection Requirements; and 

- the applicable Product Technical Standard. 

The Portfolio Liquidity Budget SHALL satisfy: 



where: 

21 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- 𝑃𝐿𝐵𝑡= Portfolio Liquidity Budget; 

- 𝐼𝐿𝐵𝑖,𝑡= Issuer Liquidity Budget assigned to Team Company 𝑖; 

- 𝑁= number of active Team Companies within the Portfolio. 

##### 𝑃𝐿𝐵𝑡 = 𝑓(𝑃𝐶𝑡, 𝑃𝐴𝑡, 𝑃𝐼𝑅𝑡, 𝑃𝑅𝑡, 𝐶𝐹𝐺𝑡) 

where 

- Portfolio Capital 

- Portfolio Assessment 

- Portfolio Inventory Risk 

- Protection Requirements 

- Configuration 

The Portfolio Liquidity Budget SHALL NOT exceed the Portfolio Capital allocated to the active Portfolio. 

The applicable Product Technical Standard SHALL define the mathematical methodology governing Portfolio Liquidity Budget determination. 

The Portfolio Liquidity Budget SHALL become the authoritative liquidity constraint governing all issuer-level Market Making Engines during the current Decision Cycle. 

## 5.7 Issuer Liquidity Allocation 

The Portfolio Allocation Engine SHALL allocate the Portfolio Liquidity Budget among all active Team Companies within the Portfolio during each Decision Cycle. 

Each active Team Company SHALL receive one Issuer Liquidity Budget. 

Issuer Liquidity Budgets SHALL satisfy: 

𝐼𝐿𝐵𝑖,𝑡 = 𝑃𝐿𝐵𝑡 × 𝐴𝑖,𝑡 

where: 

22 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- 𝐼𝐿𝐵𝑖,𝑡= Issuer Liquidity Budget assigned to Team Company 𝑖; 

- 𝑃𝐿𝐵𝑡= Portfolio Liquidity Budget; 

- 𝐴𝑖,𝑡= Portfolio Allocation Weight assigned to Team Company 𝑖. 

The Portfolio Allocation Weights SHALL satisfy: 



where: 

- 𝑁= number of active Team Companies within the Portfolio. 



##### where 

- Portfolio Assessment 

- Issuer Market State 

- Issuer Inventory Risk 

- Issuer Protection State 

- Configuration 

The applicable Product Technical Standard SHALL define the mathematical methodology governing Portfolio Allocation Weight determination. 

Portfolio Allocation Weights MAY be determined using one or more portfolio-level factors including: 

- Portfolio Assessment; 

- Effective Market State; 

- issuer-level Market Activity Assessment; 

- issuer-level Inventory Risk; 

- issuer-level Protection State; and 

- Product Technical Standard configuration. 

23 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



The resulting Issuer Liquidity Budgets SHALL become the authoritative liquidity constraints governing issuer-level Market Making Engines during the current Decision Cycle. 

## 5.7.1 Bid-Side and Offer-Side Liquidity Allocation 

For every active Team Company within the Portfolio, the Portfolio Allocation Engine SHALL determine: 

- Bid-side Liquidity Budget; and 

- Offer-side Liquidity Budget. 

For each Team Company: 

𝐼𝐿𝐵 = 𝐵𝐿𝐵 + 𝑂𝐿𝐵 𝑖,𝑡 𝑖,𝑡 𝑖,𝑡 

where: 

- 𝐼𝐿𝐵𝑖,𝑡= Issuer Liquidity Budget; 

- 𝐵𝐿𝐵𝑖,𝑡= Bid-side Liquidity Budget; 

- 𝑂𝐿𝐵 𝑖,𝑡= Offer-side Liquidity Budget. 

The Bid-side Liquidity Budget and Offer-side Liquidity Budget SHALL satisfy: 

𝐵𝐿𝐵𝑖,𝑡 ≥0 𝑂𝐿𝐵𝑖,𝑡 ≥0 𝐵𝐿𝐵 + 𝑂𝐿𝐵 = 𝐼𝐿𝐵 𝑖,𝑡 𝑖,𝑡 𝑖,𝑡 

The applicable Product Technical Standard SHALL define the mathematical methodology governing bid-side and offer-side allocation. 

Bid-side and Offer-side Liquidity Budgets MAY differ according to: 

- issuer Inventory Risk Profile; 

   - issuer Effective Market State; 

- 

- issuer Market Activity Assessment; 

- issuer Protection State; and 

24 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- Product Technical Standard configuration. 

The resulting Bid-side and Offer-side Liquidity Budgets SHALL become the authoritative liquidity constraints governing the issuer-level Market Making Engine during the current Decision Cycle. 

## 5.8 Portfolio Reallocation 

The Portfolio Allocation Engine SHALL re-evaluate portfolio-wide resource allocation during every Decision Cycle. 

Portfolio reallocation SHALL be performed whenever changes in the portfolio operating environment materially affect portfolio-wide liquidity or inventory allocation. 

Portfolio reallocation MAY occur in response to changes in: 

- Effective Market State; 

- Portfolio Assessment; 

- Portfolio Capital; 

- Portfolio Inventory Position; 

- issuer Market Activity Assessment; 

- issuer Inventory Risk Profile; 

- Protection Requirements; or 

- Product Technical Standard configuration. 

Portfolio reallocation SHALL determine revised: 

- Issuer Liquidity Budgets; 

- Bid-side Liquidity Budgets; and 

- Offer-side Liquidity Budgets. 

Portfolio reallocation SHALL remain deterministic and reproducible through deterministic replay. 

Revised portfolio allocations SHALL become effective beginning with the next Decision Cycle. 

Portfolio reallocation SHALL NOT modify executable quotations that have already been published during the current Decision Cycle. 

25 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 5.9 Portfolio Constraints 

The Portfolio Allocation Engine SHALL ensure that every portfolio allocation produced during a Decision Cycle satisfies the following constraints: 

#### Capital Constraint 

The total Issuer Liquidity Budgets SHALL NOT exceed the Portfolio Liquidity Budget. 



### Liquidity Constraint 

The Portfolio Liquidity Budget SHALL NOT exceed the Portfolio Capital allocated to the active Portfolio. 



where: 

- 𝑃𝐶𝑡= Portfolio Capital. 

#### Inventory Constraint 

Aggregate Portfolio Inventory SHALL remain within the Portfolio Inventory Risk Limits established by the applicable Product Technical Standard. 

#### Issuer Constraint 

No Issuer Liquidity Budget SHALL exceed the maximum allocation permitted for the applicable Team Company. 

26 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



Issuer allocation limits SHALL be defined by the applicable Product Technical Standard. 

#### Allocation Constraint 

Every active Team Company SHALL receive exactly one Issuer Liquidity Budget during a Decision Cycle. 

The sum of all Portfolio Allocation Weights SHALL satisfy: 



#### Deterministic Constraint 

Portfolio allocation decisions SHALL be deterministic and reproducible through deterministic replay. 

Portfolio allocations that violate any Portfolio Constraint SHALL NOT be transmitted to issuer-level Market Making Engines. 

## 5.10 Portfolio Allocation Invariants 

The following conditions SHALL remain true throughout every Decision Cycle. 

#### Capital Conservation 

The total Issuer Liquidity Budgets SHALL equal the Portfolio Liquidity Budget. 



27 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



#### Allocation Conservation 

The Portfolio Allocation Weights SHALL satisfy: 



<!-- Start of picture text -->
𝑁<br>= 1<br>𝑖,𝑡<br>∑𝐴<br>𝑖=1<br><!-- End of picture text -->

#### Issuer Allocation 

Every active Team Company SHALL receive one—and only one—Issuer Liquidity Budget during the current Decision Cycle. 

#### Budget Integrity 

Issuer-level Market Making Engines SHALL consume assigned Issuer Liquidity Budgets. 

Issuer-level Market Making Engines SHALL NOT independently increase, decrease, or redistribute assigned Portfolio Liquidity. 

#### Portfolio Integrity 

No portfolio allocation SHALL violate: 

- Portfolio Capital; 

- Portfolio Inventory Risk Limits; 

- Protection Requirements; or 

- constitutional market requirements. 

#### Deterministic Operation 

Every Portfolio Allocation decision SHALL remain deterministic and reproducible through deterministic replay. 

28 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



#### Decision Cycle Integrity 

Every Portfolio Allocation produced during a Decision Cycle SHALL correspond to one— and only one—Decision Cycle. 

Portfolio allocations SHALL NOT be modified after transmission to issuer-level Market Making Engines. 

## 5.11 Engineering Outputs 

The Portfolio Allocation Engine SHALL produce the following authoritative outputs for the active Portfolio during each Decision Cycle: 

#### Portfolio Outputs 

- Portfolio Liquidity Budget; 

- Portfolio Capital Allocation; 

- Portfolio Risk Assessment; and 

- Portfolio Allocation Map. 

#### Issuer Outputs 

For every active Team Company within the Portfolio: 

- Issuer Liquidity Budget; 

- Bid-side Liquidity Budget; 

- Offer-side Liquidity Budget; 

- Portfolio Allocation Weight; and 

- Portfolio Allocation Status. 

Portfolio Allocation Status SHALL indicate whether the Team Company is: 

- Fully Allocated; 

- Partially Allocated; 

- Allocation Limited; or 

- Allocation Suspended. 

29 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



The applicable Product Technical Standard MAY define additional Portfolio Allocation Status values. 

The Engineering Outputs produced by this chapter SHALL become the authoritative inputs to the Issuer Market Making Engine. 

Issuer-level Market Making Engines SHALL consume these outputs as read-only engineering inputs during the current Decision Cycle. 

## 5.12 Transition 

The Portfolio Allocation Engine concludes each Decision Cycle by producing the Portfolio Liquidity Budget, Issuer Liquidity Budgets, Bid-side Liquidity Budgets, Offer-side Liquidity Budgets, Portfolio Allocation Map, and Portfolio Allocation Status for the active Portfolio. 

These outputs become the authoritative inputs to the Issuer Market Making Engine. 

The Issuer Market Making Engine SHALL construct executable two-sided markets for individual Team Companies using only the portfolio allocations established by this chapter. 

The Issuer Market Making Engines SHALL NOT independently modify Portfolio Liquidity Budgets, Portfolio Allocation Weights, or Portfolio Allocation Status during the active Decision Cycle. 

The following chapter establishes the **Issuer Market Making Engine** , which constructs executable quotations for individual Team Companies within the active Portfolio. 

30 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## **Chapter 6** 

## Issuer Market Making Engine 

### 6.1 Purpose 

This chapter establishes the engineering methodology used by the SDMM to construct executable two-sided markets for an individual Team Company during each Decision Cycle. 

The Issuer Market Making Engine transforms portfolio allocations established by the Portfolio Allocation Engine into executable quotations, market structure, displayed liquidity, and validated executable markets for a single Team Company. 

The Issuer Market Making Engine operates independently for each Team Company within the active Portfolio. 

The Issuer Market Making Engine SHALL consume, but SHALL NOT modify, Portfolio Liquidity Budgets, Issuer Liquidity Budgets, Portfolio Allocation Weights, or Portfolio Allocation Status established by the Portfolio Allocation Engine. 

### 6.2 Governing Objective 

During each Decision Cycle, the SDMM SHALL seek to provide continuous executable twosided liquidity while maximizing long-term expected market-making performance within the constraints established by this standard. 

The governing objective is: 

max⁡ Π𝑡 

subject to: 

𝐶𝑡 

where: 

31 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- Π𝑡= expected market-making performance during Decision Cycle 𝑡; 

- 𝐶𝑡= applicable constraints, including constitutional requirements, inventory limits, liquidity budgets, pricing limits, protection rules, and deterministic replay requirements. 

The SDMM SHALL NOT pursue expected market-making performance in a manner that violates higher-priority constraints. 

Every executable quotation published by the SDMM SHALL be the deterministic result of the sequential engineering decisions established by this chapter. 

### 6.3 Decision Priority 

When multiple conditions exist during the same Decision Cycle, the SDMM SHALL apply the following decision priority: 

1. Protection Requirements; 

2. Continuous Market Availability; 

3. Inventory Risk Limits; 

4. Liquidity Budget; 

5. Pricing Profile; 

6. Market Structure; 

7. Displayed Quantity; 

8. Controlled Randomization; 

9. Quote Publication. 

Lower-priority decisions SHALL NOT override higher-priority constraints. 

### 6.3.1 Decision Sequence 

The Issuer Market Making Engine SHALL execute the following computational sequence during every Decision Cycle: 

1. Market Assessment; 

2. Effective Market State Determination; 

3. Inventory Risk Profile Determination; 

4. Liquidity Budget Determination; 

5. Pricing Profile Selection; 

32 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



6. Reservation Price Component Determination; 

7. Reservation Price Determination; 

8. Market Structure Construction; 

9. Displayed Quantity Allocation; 

10. Quote Validation; and 

11. Quote Publication. 

The computational sequence defined by this section SHALL be executed sequentially. 

A subsequent stage SHALL NOT modify the outputs of any preceding stage except through complete reconstruction of the affected market components. 

### 6.4 Market Inputs 

The Issuer Market Making Engine SHALL consume: 

- Reference Price; 

- Effective Market State; 

   - Inventory Risk Profile; 

- 

- Liquidity Budget; 

- Pricing Profile; 

- Market Activity Assessment; 

- Product Technical Standard configuration. 

The Issuer Market Making Engine SHALL NOT modify Reference Price, Market Operating Condition, or Market Operations Profile. 

### 5.4.1 Market Assessment 

Before determining executable pricing behavior, the Issuer Market Making Engine SHALL perform a Market Assessment for the current Decision Cycle. 

The Market Assessment SHALL evaluate, at a minimum: 

- External Market Phase; 

- Market Activity Assessment; 

- Inventory Position; 

33 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- Inventory Velocity; 

- Protection State; and 

- applicable Product Technical Standard configuration. 

The Market Assessment SHALL determine: 

- Effective Market State; 

   - Inventory Risk Profile; 

- 

- Liquidity Budget; and 

- Pricing Profile. 

These outputs SHALL become the authoritative decision inputs to all subsequent computations performed by the Issuer Market Making Engine. 

### 6.5 Pricing Profiles 

Each Decision Cycle SHALL operate under one active Pricing Profile. 

Version 1.0 recognizes the following Pricing Profiles: 

- Stable; 

- Active; 

- Defensive; 

- Recovery; 

- Liquidity Preservation; 

- Protective. 

Each Pricing Profile SHALL define, at a minimum: 

- base spread component; 

- inventory sensitivity; 

- activity sensitivity; 

- protection sensitivity; 

- bid-side liquidity budget; 

- offer-side liquidity budget; 

   - ladder spacing profile; 

- 

   - displayed quantity profile; 

- 

   - randomization bounds; 

- 

   - quote refresh parameters. 

- 

34 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



#### Pricing Profile Selection 

The active Pricing Profile SHALL be selected using the current Effective Market State together with the Inventory Risk Profile, Protection State, Market Activity Assessment, and Product Technical Standard configuration. 

Only one Pricing Profile SHALL govern a Decision Cycle. 

If multiple Pricing Profiles are simultaneously applicable, the profile associated with the higher-priority operational objective established by Chapter 4 SHALL govern. 

### 6.5.1 Pricing Parameters 

The Issuer Market Making Engine SHALL determine the pricing parameters governing the current Decision Cycle. 

At a minimum, the following parameters SHALL be established: 

- Number of executable price levels; 

- Bid-side ladder spacing; 

- Offer-side ladder spacing; 

- Bid-side Liquidity Budget; 

- Offer-side Liquidity Budget; 

   - Bid-side depth weighting profile; 

- 

- Offer-side depth weighting profile; 

- • Inventory sensitivity coefficient; 

- • Activity sensitivity coefficient; 

   - Protection sensitivity coefficient; 

- 

- Controlled randomization bounds; 

- Deterministic randomization seed. 

These parameters SHALL remain authoritative throughout the active Decision Cycle unless superseded by a subsequent Decision Cycle. 

The bid-side Liquidity Budget and offer-side Liquidity Budget SHALL be determined as functions of the current Effective Market State, Inventory Risk Profile, and the applicable Product Technical Standard configuration. 

35 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



The applicable Product Technical Standard SHALL define the mathematical methodology governing Liquidity Budget determination. 

### 6.5.2 Profile Transition Rules 

A Pricing Profile transition SHALL occur whenever one or more governing inputs change sufficiently to alter the SDMM's pricing objectives. 

Profile transitions may occur in response to: 

- Effective Market State transition; 

- • Inventory Risk Profile transition; 

- Liquidity Budget transition; 

- Protection State transition; or 

- Product Technical Standard configuration. 

A Pricing Profile transition SHALL invalidate all previously computed Reservation Prices. 

The Issuer Market Making Engine SHALL reconstruct the executable market using the newly selected Pricing Profile. 

A Pricing Profile transition SHALL invalidate every downstream computational object derived from the previously active Pricing Profile. 

At a minimum, the following engineering objects SHALL be reconstructed: 

- Reservation Price Components; 

- Reservation Prices; 

- Market Structure; 

- Displayed Quantities; 

- Validation State; and 

- Executable Quotations. 

36 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



No engineering object derived from a superseded Pricing Profile SHALL remain authoritative during the subsequent Decision Cycle. 

### 6.6 Reservation Price Components 

The Issuer Market Making Engine SHALL independently determine the pricing components that collectively establish the Bid Offset and Offer Offset for the current Decision Cycle. 



where: 

- 𝐵𝑂𝑡= Bid Offset; 

- 𝑂𝑂𝑡= Offer Offset; 

- 𝐵 𝑂 

- • 𝐵𝑆𝑡 , 𝐵𝑆𝑡 = bid-side and offer-side base spread components; 

- 𝐵 𝑂 

- • 𝐼𝑆𝑡 , 𝐼𝑆𝑡 = bid-side and offer-side inventory skew components; 

- 𝐵 𝑂 

- • 𝐴𝑆𝑡 , 𝐴𝑆𝑡 = bid-side and offer-side activity adjustment components; 

- 𝐵 𝑂 

- • 𝑃𝑆𝑡 , 𝑃𝑆𝑡 = bid-side and offer-side protection adjustment components. 

𝐵𝑂𝑡 = 𝐵𝑆𝑡 + 𝐼𝑆𝑡 + 𝐴𝑆𝑡 + 𝑃𝑆𝑡 𝑂𝑂𝑡 = 𝑂𝑆𝑡 + 𝐼𝑆𝑡 + 𝐴𝑆𝑡 + 𝑃𝑆𝑡 

Each Reservation Price Component SHALL be fully determined before Reservation Bid Price or Reservation Offer Price calculations begin. 

Reservation Price calculations SHALL consume completed Reservation Price Components as read-only engineering inputs. 

Reservation Price Components SHALL NOT be modified during Reservation Price calculation. 

Then Reservation Prices become: 



37 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



Bid Offset and Offer Offset are not required to be symmetric. 

The applicable Product Technical Standard SHALL define the mathematical methodology used to determine each Reservation Price Component. 

This standard establishes the engineering architecture governing Reservation Price determination but does not prescribe the product-specific mathematical formulation of individual pricing components. 

### 6.6.1 Pricing Profile Parameters 

Each Pricing Profile SHALL determine a profile-specific parameter set. 

Let: 

𝑃𝑃𝑡 = (𝑆𝑡, 𝐷𝑡, 𝑄𝑡, 𝐹𝑡, 𝐼𝑡) 

where: 

- 𝑆𝑡= spread multiplier; 

- 𝐷𝑡= depth multiplier; 

- 𝑄𝑡= displayed quantity multiplier; 

- 𝐹𝑡= refresh timing multiplier; 

- 𝐼𝑡= inventory sensitivity multiplier. 

The active Pricing Profile SHALL determine the parameter values applied during the current Decision Cycle. 

𝐵𝑎𝑠𝑒𝑆𝑝𝑟𝑒𝑎𝑑𝑡 = 𝑇𝑖𝑐𝑘𝑆𝑖𝑧𝑒× 𝑆𝑡 𝐷𝑒𝑝𝑡ℎ𝐿𝑒𝑣𝑒𝑙𝑠𝑡 = 𝑁𝑏𝑎𝑠𝑒 × 𝐷𝑡 𝐿𝑖𝑞𝑢𝑖𝑑𝑖𝑡𝑦𝐵𝑢𝑑𝑔𝑒𝑡𝑡 = 𝐿𝑏𝑎𝑠𝑒 × 𝑄𝑡 𝑅𝑒𝑓𝑟𝑒𝑠ℎ𝑇𝑖𝑚𝑒𝑡 = 𝑅𝑏𝑎𝑠𝑒 × 𝐹𝑡 𝐼𝑛𝑣𝑒𝑛𝑡𝑜𝑟𝑦𝑆𝑒𝑛𝑠𝑖𝑡𝑖𝑣𝑖𝑡𝑦𝑡 = 𝜆𝑏𝑎𝑠𝑒 × 𝐼𝑡 

The following profile parameters SHALL apply unless modified by the applicable Product Technical Standard: 

38 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



|**Pricing Profle**|**(S_t)**|**(D_t)**|**(Q_t)**|**(F_t)**|**(I_t)**|
|---|---|---|---|---|---|
|Stable|1.00|1.50|1.50|1.00|0.50|
|Active|1.50|1.00|1.00|0.50|1.00|
|Defensive|2.50|0.60|0.60|1.50|1.75|
|Recovery|1.75|1.00|0.90|1.00|2.50|
|Liquidity Preservation|3.00|0.50|0.50|1.25|3.50|
|Protective|5.00|0.25|0.25|Restricted|5.00|



Restricted refresh means quotation updates may occur only when permitted by the applicable Protection Rules 

These parameters SHALL provide the mathematical translation of Pricing Profiles into spread width, executable depth, displayed size, refresh timing, and inventory sensitivity. 

Reservation Price Components MAY incorporate bounded deterministic variation consistent with the active Pricing Profile. 

Such variation SHALL preserve the pricing intent established by the current Effective Market State and SHALL remain reproducible through deterministic replay. 

### 6.7 Inventory Influence 

Inventory SHALL continuously influence Reservation Price determination. 

Inventory Position SHALL be expressed as a percentage of the publicly tradable float. 



The Issuer Market Making Engine SHALL determine an Inventory Influence Function. 

39 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



𝐼𝑆𝑡 = 𝜆𝐸𝑀𝑆,𝑡 × 𝐼𝑁𝑉𝑡 

where: 

- 𝐼𝑁𝑉𝑡= Inventory Position; 

- 𝜆𝐸𝑀𝑆,𝑡= Inventory Sensitivity under the current Effective Market State; 

- 𝐼𝑆𝑡= Inventory Influence. 

The bid-side and offer-side Inventory Influence components SHALL be determined as follows: 

IS_t^B=\max(IS_t,0) 

IS_t^O=\max(-IS_t,0) 

where: 

IS_t^B = bid-side Inventory Influence; 

IS_t^O = offer-side Inventory Influence. 

A positive Inventory Position produces a positive bid-side Inventory Influence component. 

A negative Inventory Position produces a positive offer-side Inventory Influence component. 

The applicable Pricing Profile determines how the resulting Inventory Influence components modify the Bid Offset and Offer Offset.Inventory Influence SHALL affect the bid side and offer side independently. 

When Inventory Position is positive (long inventory): 

- Bid Offset SHALL increase; 

- • Offer Offset MAY decrease; 

40 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- Bid-side displayed quantity MAY decrease; 

- Offer-side displayed quantity MAY increase. 

When Inventory Position is negative (short inventory): 

- Bid Offset MAY decrease; 

   - Offer Offset SHALL increase; 

- 

- Bid-side displayed quantity MAY increase; 

- Offer-side displayed quantity MAY decrease. 

Inventory Influence SHALL remain bounded by the active Inventory Risk Profile and SHALL NOT prevent continuous executable two-sided quotations. 

### 6.8 Reservation Prices 

Reservation Prices SHALL be calculated as follows: 

𝑅𝐵𝑃𝑡 = 𝑅𝑃𝑡 −𝐵𝑂𝑡 𝑅𝑂𝑃𝑡 = 𝑅𝑃𝑡 + 𝑂𝑂𝑡 𝑅𝑆𝑡 = 𝑅𝑂𝑃𝑡 −𝑅𝐵𝑃𝑡 

where: 

- 𝑅𝐵𝑃𝑡= Reservation Bid Price; 

- 𝑅𝑂𝑃𝑡= Reservation Offer Price; 

- 𝑅𝑆𝑡= Reservation Spread; 

- 𝑅𝑃𝑡= Reference Price. 

The Reservation Spread is an output of Reservation Price determination. It is not independently targeted. 

### 6.8.1 Reservation Price Constraints 

Reservation Prices SHALL satisfy the following constraints: 

- Reservation Bid Price SHALL remain less than Reservation Offer Price. 

41 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- Reservation Prices SHALL remain within the applicable trading range. 

- Reservation Prices SHALL remain consistent with the active Pricing Profile. 

- Reservation Prices SHALL remain consistent with the current Liquidity Budget. 

- Reservation Prices SHALL remain consistent with the active Inventory Risk Profile. 

Reservation Prices failing any constraint SHALL be recalculated before Market Structure construction. 

Reservation Prices SHALL NOT be less than the minimum permissible price or greater than the maximum permissible price established for the applicable InPlay Security. 

### 6.9 Market Structure 

The SDMM SHALL construct executable bid and offer ladders from the Reservation Prices. 

Depth level k=0 represents the best executable bid or best executable offer. 

Depth levels k>0 represent progressively deeper executable price levels. 

For depth level 𝑘: 



where: 

- 𝑘= depth level; 

- Δ𝐵𝑡= bid-side ladder spacing; 

- Δ𝑂𝑡= offer-side ladder spacing; 

- 𝐵 𝑂 

- • 𝜖𝑡,𝑘, 𝜖𝑡,𝑘= bounded price-level randomization terms. 

𝑁𝑡 = 𝑓(𝑃𝑃𝑡, 𝐿𝐵𝑡, 𝐶𝐹𝐺𝑡) 

where 

- Pricing Profile 

- Liquidity Budget 

42 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- Configuration 

The applicable Product Technical Standard SHALL define the origin of the executable price ladder. 

Unless otherwise specified, depth level k=0 represents the best executable quotation on each side of the market.The number of levels, ladder spacing, and ladder shape SHALL be determined by the active Pricing Profile and Liquidity Budget. 

#### Ladder Geometry Profile 

The active Pricing Profile SHALL determine the executable ladder geometry used during the current Decision Cycle. 

The applicable ladder geometry SHALL define: 

- executable price spacing methodology; 

- number of executable price levels; 

- liquidity concentration across depth levels; and 

- bid-side and offer-side ladder symmetry. 

The applicable Product Technical Standard MAY define one or more ladder geometry profiles including uniform, front-loaded, back-loaded, convex, concave, adaptive, or other approved methodologies. 

Executable ladder spacing MAY incorporate bounded deterministic variation provided the resulting Market Structure remains consistent with the active Pricing Profile, Inventory Risk Profile, and Liquidity Budget. 

Bounded deterministic variation SHALL NOT produce an executable quotation that is more aggressive than the corresponding Reservation Price unless expressly authorized by the active Pricing Profile. 

### 6.9.1 Tick Conformance 

All executable prices SHALL conform to the applicable minimum quotation increment. 

43 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



Following calculation of Reservation Prices and executable ladder prices, every executable quotation SHALL be adjusted to the nearest valid quotation increment. 

Bid quotations SHALL be rounded downward to the nearest valid tick. 

Offer quotations SHALL be rounded upward to the nearest valid tick. 

Tick adjustment SHALL NOT produce locked or crossed markets. 

Tick adjustment SHALL preserve the pricing intent established by the active Pricing Profile. 

Tick conformance SHALL be applied after all price-level randomization. 

### 6.10 Displayed Quantity 

Displayed quantity SHALL be allocated across the executable price ladder. 



where: 

- 𝑄𝐵𝑡,𝑘= displayed bid quantity at level 𝑘; 

- 𝑄𝑂𝑡,𝑘= displayed offer quantity at level 𝑘; 

- 𝐿𝐵𝑡= bid-side liquidity budget; 

- 𝐿𝑂𝑡= offer-side liquidity budget; 

- 𝐵 𝑂 

- • 𝑊𝑡,𝑘, 𝑊𝑡,𝑘= bid-side and offer-side depth weights; 

- 𝐵 𝑂 

- • 𝑅𝑡,𝑘, 𝑅𝑡,𝑘= bounded quantity randomization factors. 

For each side of the executable market, the depth weighting coefficients SHALL be normalized such that: 

∑_(k=0)^(N-1) W_(t,k)^B = 1 

44 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



##### ∑_(k=0)^(N-1) W_(t,k)^O = 1 

where N is the number of executable price levels established for the current Decision Cycle. 

Normalization ensures that the complete Liquidity Budget is allocated across the executable price ladder. 

Displayed quantities SHALL remain within the active Liquidity Budget. 

Displayed quantities MAY incorporate bounded deterministic variation. 

Such variation SHALL preserve the intended liquidity distribution while preventing mechanically repetitive quotation patterns. 

Randomization SHALL remain bounded, deterministic, seeded, replayable, and consistent with the active Pricing Profile. 

### 6.10.1 Displayed Quantity Constraints 

Displayed quantities SHALL satisfy the following constraints: 

- displayed quantities SHALL be non-negative; 

- displayed quantities SHALL not exceed the applicable Liquidity Budget; 

- displayed quantities SHALL not exceed the applicable Inventory Risk Limits; 

- displayed quantities SHALL either equal zero pursuant to an approved suppression rule or equal or exceed the applicable minimum display quantity. 

The SDMM MAY suppress individual depth levels when required by Protection Rules, Liquidity Budget, or Inventory Risk Limits, provided the best executable bid and best executable offer remain continuously available unless trading is halted or suspended pursuant to CTS-002. 

Displayed quantity constraints SHALL be verified prior to quotation publication. 

45 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 6.11 Quote Aging and Replenishment 

Each executable quotation SHALL have a lifecycle. 

The SDMM SHALL define: 

- minimum quote lifetime; 

- maximum quote lifetime; 

- refresh conditions; 

- replenishment conditions; 

- cancellation conditions. 

A quotation may be refreshed, replaced, reduced, replenished, or cancelled in response to: 

- execution; 

- partial execution; 

- Reference Price movement; 

- Effective Market State change; 

   - Inventory Risk Profile change; 

- 

- Liquidity Budget change; 

- quote aging; 

- protection event. 

Quote aging and replenishment SHALL remain deterministic and replayable. 

## 6.11.1 Quote Lifecycle Events 

The Issuer Market Making Engine SHALL evaluate every executable quotation continuously throughout its lifecycle. 

Quote lifecycle events include: 

- creation; 

- execution; 

- partial execution; 

- refresh; 

- replacement; 

- replenishment; 

46 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- cancellation; and 

- expiration. 

Every lifecycle event SHALL remain deterministic and reproducible through deterministic replay. 

Quote refresh timing, replenishment timing, and quotation replacement timing MAY incorporate bounded deterministic variation provided quotation lifecycle requirements remain consistent with the active Pricing Profile and deterministic replay requirements. 

## 6.12 Validation 

Before publication, the Issuer Market Making Engine SHALL validate the constructed market. 

Validation SHALL confirm that: 

- executable bid prices are below executable offer prices; 

- no locked or crossed market is published; 

- all prices remain within valid price bands; 

- displayed quantities are non-negative; 

- inventory limits are not violated; 

- liquidity budgets are not violated; 

- protection constraints are satisfied; 

- • every executable quotation is internally consistent with the Reservation Prices, Market Structure, Displayed Quantities, Pricing Profile, and Liquidity Budget from which it was constructed; 

- randomization remains within permitted bounds; 

- the market is reproducible through deterministic replay. 

A market that fails validation SHALL NOT be published. 

Upon successful completion of validation, the validated Executable Order Book SHALL immediately become the published market for the current Decision Cycle. 

47 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 6.12.1 Validation Failure Handling 

If validation fails, the Issuer Market Making Engine SHALL reconstruct the affected market component beginning with the highest-priority failed validation. 

The applicable Product Technical Standard SHALL define a maximum number of reconstruction attempts per Decision Cycle. 

Validation failures SHALL be addressed in the following order: 

1. Protection Rules; 

2. Reservation Prices; 

3. Market Structure; 

4. Displayed Quantities; 

5. Quote Consistency. 

If reconstruction fails, the Issuer Market Making Engine SHALL enter the applicable Protective or Liquidity Preservation Pricing Profile prior to publication. 

## 6.12.2 Issuer Market-Making Performance 

The Issuer Market Making Engine SHALL seek to maximize long-term expected marketmaking performance while satisfying all higher-priority operational objectives established by Chapter 4. 

The applicable Product Technical Standard MAY evaluate market-making performance using one or more performance measures, including: 

- realized spread capture; 

- inventory turnover; 

- liquidity utilization; 

- fill ratio; 

- quotation utilization; 

- adverse selection; and 

- inventory recovery efficiency. 

Performance objectives SHALL remain subordinate to: 

- Protection Requirements; 

- Continuous Market Availability; 

- Inventory Risk Limits; and 

48 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- Liquidity Budget. 

## 6.13 Engineering Outputs 

The Issuer Market Making Engine SHALL produce: 

- Reservation Bid Price; 

- Reservation Offer Price; 

- Reservation Spread; 

- bid ladder; 

- offer ladder; 

- displayed bid quantities; 

- displayed offer quantities; 

- randomized quotation attributes; 

- validation result; 

- Executable Order Book. 

These outputs become the authoritative inputs to quote publication and subsequent participant interaction. 

## 6.13.1 Issuer Market-Making Invariants 

The following conditions SHALL remain true throughout every Decision Cycle: 

- executable two-sided quotations SHALL be maintained unless trading is halted or suspended pursuant to CTS-002; 

- Reservation Prices SHALL be derived exclusively from the current Reference Price and Pricing Profile; 

- displayed liquidity SHALL remain within the active Liquidity Budget; 

- Inventory Position SHALL remain within the active Inventory Risk Profile; 

- executable quotations SHALL conform to the applicable quotation increment; 

- locked or crossed markets SHALL NOT be published; 

- every published market SHALL correspond to one—and only one—Decision Cycle; and 

- every published market SHALL be reproducible through deterministic replay. 

49 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



Every executable quotation published during a Decision Cycle SHALL be derivable exclusively from the engineering decisions established by this chapter. 

No executable quotation SHALL be introduced outside the computational sequence established by Section 5.3.1. 

## 6.14 Transition 

The Issuer Market Making Engine constructs the executable two-sided market for the current Decision Cycle. 

The following chapter establishes the Quote Lifecycle Engine, which governs quote aging, refresh, replacement, replenishment, cancellation, and continuity following publication of executable quotations. 

## **Chapter 7** 

## Quote Lifecycle Engine 

## 7.1 Purpose 

This chapter establishes the engineering methodology used by the SDMM to manage the lifecycle of executable quotations after publication. 

The Quote Lifecycle Engine governs quote creation, publication, aging, execution, partial execution, refresh, replacement, replenishment, cancellation, expiration, and continuity. 

The Quote Lifecycle Engine does not determine Reservation Prices, Market Structure, Displayed Quantities, Pricing Profiles, or Portfolio Allocation. 

Those engineering objects are determined by preceding chapters. 

50 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 7.2 Fundamental Principle 

A published executable quotation is a living engineering object. 

Each executable quotation SHALL remain subject to lifecycle management until it is executed, cancelled, replaced, expired, or otherwise removed pursuant to this standard. 

The Quote Lifecycle Engine SHALL preserve continuous executable two-sided liquidity whenever required by the applicable Market Operations Profile, unless trading is halted or suspended pursuant to CTS-002. 

## 7.3 Engineering Inputs 

The Quote Lifecycle Engine SHALL consume: 

- Currently published Executable Quotations; 

- Executable Bid Quotations; 

- Executable Offer Quotations; 

- Quotation Status; 

- execution results; 

- partial execution results; 

- quote age; 

- Effective Market State; 

- Inventory Risk Profile; 

- Liquidity Budget; 

- Protection State; 

- Pricing Profile; and 

- Product Technical Standard configuration. 

The Quote Lifecycle Engine SHALL NOT modify Reference Price, Reservation Prices, Market Structure, Displayed Quantities, Portfolio Allocation, or any constitutional market object. 

51 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 7.4 Quote Lifecycle Function 

Let QLF_t represent the Quote Lifecycle Function during Decision Cycle t. 

The Quote Lifecycle Function is determined by: 

QLF_t = f(EOB_t, EQ_t, EX_t, QA_t, EMS_t, IRP_t, LB_t, PS_t, CFG_t) 

where: 

- EOB_t = Executable Order Book; 

- EQ_t = Executable Quotations; 

- EX_t = execution and partial execution results; 

- QA_t = quote age; 

- EMS_t = Effective Market State; 

- IRP_t = Inventory Risk Profile; 

- LB_t = Liquidity Budget; 

- PS_t = Protection State; 

- CFG_t = Product Technical Standard configuration. 

## 7.5 Quote Lifecycle States 

Each executable quotation SHALL exist in one—and only one—Quote Lifecycle State at any time. 

Version 1.0 recognizes the following Quote Lifecycle States: 

- Created; 

- Published; 

- Partially Executed; 

- Executed; 

- Refreshed; 

- Replaced; 

52 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- Replenished; 

- Cancelled; 

- Expired; 

- Suppressed. 

Additional Quote Lifecycle States MAY be defined by the applicable Product Technical Standard. 

## 7.6 Quote Lifecycle Events 

The Quote Lifecycle Engine SHALL process Quote Lifecycle Events deterministically. 

Quote Lifecycle Events include: 

- quote creation; 

- quote publication; 

- participant execution; 

- partial execution; 

- quantity depletion; 

- quote refresh; 

- quote replacement; 

- quote replenishment; 

- quote cancellation; 

- quote expiration; 

- Protection State change; 

- Effective Market State change; 

- Liquidity Budget change; and 

- Pricing Profile transition. 

Each Quote Lifecycle Event SHALL produce a deterministic lifecycle response. 

53 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 7.7 Quote Aging 

Each executable quotation SHALL maintain a Quote Age. 

Quote Age SHALL measure the elapsed time or Decision Cycle count since the quotation was published, refreshed, replaced, or replenished. 

The applicable Product Technical Standard SHALL define: 

- minimum quote lifetime; 

- maximum quote lifetime; 

- quote refresh interval; 

- quote expiration threshold; and 

- permitted quote aging variation. 

Quote Aging SHALL remain deterministic and reproducible through deterministic replay. 

## 7.8 Quote Refresh, Replacement, and Replenishment 

The Quote Lifecycle Engine MAY refresh, replace, or replenish executable quotations when permitted by this standard and the applicable Product Technical Standard. 

A quote refresh updates quotation attributes while preserving continuity of the executable market. 

A quote replacement removes an existing quotation and substitutes a new executable quotation derived from the current engineering state. 

A quote replenishment restores displayed quantity following execution or partial execution, subject to the active Liquidity Budget, Inventory Risk Profile, and Protection State. 

Refresh, replacement, and replenishment SHALL NOT violate: 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 

54 



- Reservation Prices; 

- Market Structure; 

- Displayed Quantity constraints; 

- Liquidity Budget; 

- Inventory Risk Profile; 

- Protection Requirements; or 

- deterministic replay requirements. 

## 7.9 Quote Cancellation and Expiration 

The Quote Lifecycle Engine SHALL cancel or expire executable quotations when required by: 

- execution; 

- complete quantity depletion; 

- maximum quote lifetime; 

- Pricing Profile transition; 

- Effective Market State transition; 

- Protection State; 

- Liquidity Budget change; 

- invalidation of upstream engineering objects; or 

- Product Technical Standard configuration. 

Cancelled or expired quotations SHALL NOT remain executable. 

Any cancellation or expiration event SHALL be permanently recorded and reproducible through deterministic replay. 

55 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 7.10 Lifecycle Continuity 

The Quote Lifecycle Engine SHALL preserve market continuity across successive Decision Cycles. 

Quotation updates SHALL occur through refresh, replacement, replenishment, or controlled cancellation unless complete market reconstruction is expressly required by this standard or the applicable Product Technical Standard. 

Complete reconstruction MAY occur when required by: 

- Pricing Profile transition; 

- Protection State; 

- validation failure; 

- Reference Price change; 

- Market Structure reconstruction; 

- Displayed Quantity reconstruction; or 

- Product Technical Standard configuration. 

Lifecycle continuity SHALL NOT override higher-priority protection, validation, or constitutional requirements. 

## 7.11 Engineering Outputs 

The Quote Lifecycle Engine SHALL produce: 

- updated Executable Order Book; 

- updated Executable Bid Quotations; 

- updated Executable Offer Quotations; 

- Quote Lifecycle State; 

- Quotation Status; 

- refresh records; 

- replacement records; 

56 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- replenishment records; 

- cancellation records; 

- expiration records; and 

- lifecycle audit records. 

These outputs become authoritative inputs to the Decision Cycle Engine and Verification and Deterministic Replay Framework. 

## 7.12 Quote Lifecycle Invariants 

The following conditions SHALL remain true throughout every Decision Cycle: 

- every executable quotation SHALL exist in one—and only one—Quote Lifecycle State at any time; 

no cancelled quotation SHALL remain executable; 

- no expired quotation SHALL remain executable; 

- no quotation SHALL be refreshed, replaced, or replenished in violation of the active Liquidity Budget; 

- no quotation SHALL be refreshed, replaced, or replenished in violation of the active Inventory Risk Profile; 

- no quotation SHALL be refreshed, replaced, or replenished in violation of Protection Requirements; 

- every Quote Lifecycle Event SHALL correspond to one—and only one—Decision Cycle; 

- every lifecycle transition SHALL be deterministic and reproducible through deterministic replay. 

## 7.13 Engineering Independence 

The Quote Lifecycle Engine SHALL NOT independently determine: 

57 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- Expected Settlement Value; 

- Reference Price; 

- Market Operating Condition; 

- Market Operations Profile; 

- Portfolio Allocation; 

- Reservation Prices; 

- Market Structure; 

- Displayed Quantities; or 

- participant interaction rules. 

Those responsibilities remain assigned to CTS-001, CTS-002, or preceding engineering engines defined by this standard. 

## 7.14 Transition 

The Quote Lifecycle Engine governs the lifecycle of executable quotations following publication. 

The following chapter establishes the Displayed Quantity Engine, which determines the quantity of executable liquidity displayed at each price level within the Market Structure. 

## **Chapter 8** 

### Displayed Quantity Engine 

## 8.1 Purpose 

This chapter establishes the engineering methodology used by the SDMM to determine the quantity of executable liquidity displayed at each price level within the Market Structure. 

The Displayed Quantity Engine transforms structural liquidity into published market depth. 

58 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



The Displayed Quantity Engine determines **how much** liquidity is displayed. 

It does not determine **where** liquidity is displayed. 

## 8.2 Fundamental Principle 

The structural location of executable liquidity is independent of the quantity displayed at that location. 

The SDMM therefore determines: 

1. Market Structure. 

2. Displayed Quantity. 

as separate engineering decisions. 

This separation permits independent optimization of market topology and liquidity presentation. 

## 8.3 Engineering Inputs 

The Displayed Quantity Engine SHALL consume: 

- Market Structure; 

- Reservation Prices; 

- Market Posture; 

- Product Technical Standard configuration. 

It SHALL NOT modify: 

- Market Structure; 

- Reservation Prices; 

- constitutional market objects. 

59 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 8.4 Displayed Quantity Function 

Let 

𝐷𝑄𝑡 

represent the Displayed Quantity Function. 

The Displayed Quantity Function is determined by 

𝐷𝑄𝑡 = 𝑄(𝑀𝑆𝑡, 𝑀𝑃𝑡, 𝐶𝐹𝐺𝑡) 

where: 

- 𝑀𝑆𝑡= Market Structure; 

- 𝑀𝑃𝑡= Market Posture; 

- 𝐶𝐹𝐺𝑡= SDMM configuration. 

## 8.5 Quantity Distribution 

The Displayed Quantity Engine determines: 

- quantity at each bid level; 

- quantity at each offer level; 

- quantity distribution across the Market Structure; 

- displayed liquidity density. 

The quantity distribution SHALL preserve the Market Structure established by Chapter 6. 

## 8.6 Controlled Randomization 

Displayed quantities SHALL NOT necessarily equal target quantities. 

60 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



Instead, displayed quantities may be varied through **bounded randomization** while preserving the intended liquidity characteristics of the current Market Posture. 

Randomization SHALL: 

- preserve realism; 

- reduce predictability; 

- preserve replayability; 

- remain statistically bounded. 

Randomization SHALL NOT produce chaotic or misleading market behavior. 

## 8.7 Quantity Continuity 

The following conditions SHALL remain true throughout every Decision Cycle: 

- displayed quantities SHALL remain non-negative; 

- displayed quantities SHALL remain consistent with the active Liquidity Budget; 

- displayed quantities SHALL remain consistent with the active Inventory Risk Profile; 

- displayed quantities SHALL remain consistent with the active Pricing Profile; 

- displayed quantities SHALL remain deterministic and reproducible through deterministic replay; 

- displayed quantities SHALL NOT independently modify Market Structure. 

## 8.8 Engineering Outputs 

The Displayed Quantity Engine SHALL produce: 

- Executable Bid Displayed Quantities; 

- Executable Offer Displayed Quantities; 

- Displayed Quantity Allocation; 

- Displayed Quantity Status; 

- Displayed Quantity Validation State; and 

- Displayed Quantity Audit Records. 

61 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



These outputs become the authoritative engineering inputs to the Market Adaptation Engine. 

Subsequent engineering engines SHALL consume these outputs as read-only engineering objects during the active Decision Cycle. 

## 8.9 Transition 

The Displayed Quantity Engine concludes by determining the executable quantity displayed at every executable price level within the Market Structure. 

These outputs become the authoritative engineering inputs to the Market Adaptation Engine. 

The following chapter establishes the Market Adaptation Engine, which determines the Behavioral Mode governing the current Decision Cycle. 

## **Chapter 9** 

## Market Adaptation Engine 

## 9.1 Purpose 

The Market Adaptation Engine continuously evaluates whether changes in the operating environment require reconstruction of one or more engineering objects established by preceding chapters. 

The Market Adaptation Engine SHALL coordinate adaptation. 

It SHALL NOT independently determine Reservation Prices, Market Structure, Displayed Quantities, or Portfolio Allocation. 

62 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 9.2 Fundamental Principle 

The SDMM SHALL continuously maintain executable two-sided markets whenever required by the applicable Market Operations Profile. 

The purpose of the Market Adaptation Engine is to preserve that obligation. 

Adaptation determines **how the SDMM behaves** . 

Subsequent engineering engines determine **how that behavior is expressed** through executable quotations. 

## 9.3 Engineering Inputs 

The Market Adaptation Engine SHALL continuously evaluate: 

- Market Posture; 

- Market Operating Condition; 

- Inventory Position; 

- Protection State; 

- Product Technical Standard configuration. 

Future revisions of this standard may introduce additional engineering inputs. 

## 9.4 Market Adaptation Function 

Let 

𝑀𝐴𝑡 

represent the Market Adaptation Function at Decision Cycle 𝑡. 

The Market Adaptation Function is determined by 



63 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



where: 

- 𝑀𝑃𝑡= Market Posture; 

- 𝐼𝑃𝑡= Inventory Position; 

- 𝑀𝑂𝐶𝑡= Market Operating Condition; 

- 𝑃𝑆𝑡= Protection State; 

- 𝐶𝐹𝐺𝑡= Product Technical Standard configuration. 

The Market Adaptation Function determines the Behavioral Mode governing the current Decision Cycle. 

## 9.5 Behavioral Modes 

The SDMM SHALL operate in one—and only one—Behavioral Mode during each Decision Cycle. 

Behavioral Modes determine the operating objectives that subsequent engineering engines SHALL implement. 

Version 1.0 recognizes the following Behavioral Modes: 

- Normal Mode 

- Active Mode 

- Recovery Mode 

- Liquidity Preservation Mode 

- Protective Mode 

Additional Behavioral Modes may be introduced through future revisions of this standard. 

## 9.6 Inventory Position 

The SDMM SHALL continuously maintain an Inventory Position for every Team Company. 

Inventory Position SHALL be expressed as a percentage of the publicly tradable float. 

64 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



Public float excludes Team Company treasury shares and any shares otherwise unavailable for public trading. 

The applicable Product Technical Standard SHALL define: 

- Target Inventory Ratio; 

- Warning Inventory Ratio; 

- Maximum Inventory Ratio. 

These values are engineering configuration parameters. 

They are not constitutional requirements. 

## 9.7 Behavioral Mode Determination 

The Market Adaptation Engine SHALL continuously evaluate whether the current Behavioral Mode remains appropriate. 

Behavioral Mode transitions may occur in response to: 

- Inventory Position; 

- Market Operating Condition; 

- Protection State; or 

- Product Technical Standard rules. 

Every Behavioral Mode transition SHALL be: 

- deterministic; 

- reproducible; 

- independently auditable; and 

- permanently recorded. 

## 9.8 Liquidity Preservation Mode 

Liquidity Preservation Mode exists to preserve the SDMM's continuing ability to satisfy its market-making responsibilities. 

65 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



While operating in Liquidity Preservation Mode, the SDMM SHALL continue maintaining executable two-sided quotations unless trading is halted or suspended pursuant to CTS002. 

Liquidity Preservation Mode influences subsequent engineering decisions. 

It does not suspend the SDMM's continuous market-making obligations. 

## 9.9 Engineering Independence 

The Market Adaptation Engine SHALL NOT independently determine: 

- Expected Settlement Value; 

- Reference Price; 

- Market Operating Condition; 

- Market Operations Profile; 

- participant interaction; 

- executable quotations. 

Those responsibilities remain assigned to CTS-001, CTS-002, or subsequent engineering engines defined by this standard. 

## 9.10 Runtime Authority 

The Behavioral Mode determined by the Market Adaptation Engine SHALL remain authoritative throughout the current Decision Cycle. 

Every subsequent engineering engine SHALL operate consistently with the current Behavioral Mode until superseded by a subsequent Decision Cycle. 

66 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 9.11 Adaptation Invariants 

The following conditions SHALL remain true throughout every Decision Cycle: 

- adaptation SHALL remain deterministic; 

- adaptation SHALL preserve constitutional market objects; 

- adaptation SHALL NOT modify completed engineering objects except through approved reconstruction; 

- every adaptation event SHALL correspond to one—and only one—Decision Cycle; 

- every adaptation decision SHALL remain reproducible through deterministic replay. 

## 9.12 Engineering Outputs 

The Market Adaptation Engine SHALL produce: 

- Adaptation State; 

- Reconstruction Request; 

- Adaptation Status; 

- Adaptation Audit Record; and 

- Adaptation Timestamp. 

These outputs become the authoritative engineering inputs to the Decision Cycle Engine. 

Subsequent engineering components SHALL consume these outputs as read-only engineering objects during the active Decision Cycle. 

## 9.13 Transition 

The Market Adaptation Engine determines **how the SDMM shall behave** during the current Decision Cycle. 

67 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



The following chapter establishes the **Quote Construction Engine** , which transforms the outputs of all preceding engineering engines into a published Executable Order Book and Executable Quotations. 

## **Chapter 10** 

## Quote Construction Engine 

## 10.1 Purpose 

This chapter establishes the engineering methodology used by the SDMM to transform the outputs of the preceding engineering engines into a single internally consistent Executable Order Book. 

The Quote Construction Engine is the final computational stage of the SDMM runtime architecture. 

It constructs the published market from the engineering decisions produced by the preceding chapters. 

## 10.2 Fundamental Principle 

The Quote Construction Engine does not independently determine market behavior. 

It faithfully implements the engineering decisions established by: 

- the Executable Market; 

- the Market Posture; 

- the Price Formation Engine; 

- the Market Structure Engine; 

- the Displayed Quantity Engine; and 

- the Market Adaptation Engine. 

68 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



The Quote Construction Engine is responsible for construction, not decision-making. 

## 10.2.1 Decision Cycle Initiation 

A new Decision Cycle SHALL begin whenever one or more Decision Cycle Trigger Events occur. 

Decision Cycle Trigger Events include: 

- publication of a new Reference Price; 

- execution of one or more participant orders; 

- partial execution of one or more participant orders; 

- expiration of the maximum permitted Decision Cycle duration; 

- Effective Market State transition; 

- Inventory Risk Profile transition; 

- Pricing Profile transition; 

- Portfolio Allocation update; 

- Protection State transition; 

- Market Operating Condition transition published by CTS-002; 

- Market Operations Profile transition published by CTS-002; or 

- any Product Technical Standard event explicitly designated as a Decision Cycle Trigger. 

If multiple Trigger Events occur before completion of the active Decision Cycle, they SHALL be processed together within the next Decision Cycle. 

A Decision Cycle SHALL NOT begin until the preceding Decision Cycle has successfully completed or has been terminated pursuant to this standard. 

## 10.2.2 Decision Cycle Completion 

A Decision Cycle SHALL be considered complete only after: 

- all engineering engines have completed execution; 

- all validation requirements have been satisfied; 

69 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- executable quotations have been published or intentionally withheld pursuant to this standard; 

- all authoritative engineering objects have been committed; and 

- deterministic replay records have been finalized. 

No subsequent Decision Cycle SHALL begin until completion of the current Decision Cycle. 

## 10.3 Engineering Inputs 

The Quote Construction Engine SHALL consume: 

- Executable Market; 

- Reservation Bid Price; 

- Reservation Offer Price; 

- Market Structure; 

- Displayed Quantities; 

- Behavioral Mode; 

- Product Technical Standard configuration. 

The Quote Construction Engine SHALL NOT independently modify any engineering input. 

### 10.4 Quote Construction Function 

Let 

𝑄𝐶𝑡 

represent the Quote Construction Function at Decision Cycle 𝑡. 

The Quote Construction Function is determined by 



70 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



where: 

- 𝑅𝐵𝑃𝑡= Reservation Bid Price; 

- 𝑅𝑂𝑃𝑡= Reservation Offer Price; 

- 𝑀𝑆𝑡= Market Structure; 

- 𝐷𝑄𝑡= Displayed Quantities; 

- 𝐵𝑀𝑡= Behavioral Mode; 

- 𝐶𝐹𝐺𝑡= Product Technical Standard configuration. 

### 10.5 Construction Objectives 

The Quote Construction Engine SHALL ensure that: 

- executable bid quotations remain consistent with the Reservation Bid Price; 

- executable offer quotations remain consistent with the Reservation Offer Price; 

- displayed quantities remain consistent with the Market Structure; 

- Behavioral Mode is consistently reflected throughout the market; 

- protection constraints remain satisfied. 

The Quote Construction Engine SHALL reject internally inconsistent engineering states. 

### 10.6 Protection Enforcement 

The Quote Construction Engine SHALL enforce every protection constraint established by the applicable Behavioral Mode and Product Technical Standard. 

Protection constraints SHALL be applied immediately prior to construction of the Executable Order Book: 

- Protection enforcement may: 

- suppress individual quotations; 

- modify quotation visibility; 

- modify displayed quantities; 

- restrict quotation publication; or 

- invoke Product Technical Standard protection rules. 

71 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



Protection enforcement SHALL NOT modify constitutional market objects or Reservation Prices. 

Protection enforcement constitutes the final engineering validation performed before publication of the Executable Order Book. 

### 10.7 Engineering Outputs 

The Quote Construction Engine SHALL produce: 

- Executable Order Book; 

- Executable Bid Quotations; 

- Executable Offer Quotations; 

- Displayed Market Depth; 

- Displayed Quantities; 

- Quotation Status.; 

- Decision Cycle Identifier; 

- Decision Cycle Timestamp; 

- Decision Cycle Trigger Event; 

- Decision Cycle Completion Status. 

These outputs constitute the published market. 

### 10.8 Engineering Independence 

The Quote Construction Engine SHALL NOT independently determine: 

- Reference Price; 

- Market Posture; 

- Reservation Prices; 

- Market Structure; 

- Displayed Quantities; 

- Behavioral Mode. 

Those engineering decisions remain the responsibility of their respective engines. 

72 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



### 10.9 Runtime Authority 

The Executable Order Book constructed by the Quote Construction Engine SHALL remain authoritative throughout the current Decision Cycle. 

Every participant interaction SHALL occur against the current Executable Order Book. 

### 10.10 Transition 

The Quote Construction Engine constructs the complete published market. 

The following chapter establishes the Decision Cycle Engine, which coordinates the continuous runtime execution of the SDMM. 

## **Chapter 11** 

## Decision Cycle Engine 

### 11.1 Purpose 

This chapter establishes the engineering methodology governing the continuous Decision Cycle of the Simulation Designated Market Maker ("SDMM"). 

The Decision Cycle Engine coordinates the sequential execution of every engineering subsystem defined by this standard. 

The Decision Cycle provides the runtime framework within which the SDMM continuously constructs, publishes, and maintains executable markets. 

### 11.2 Fundamental Principle 

The SDMM operates as a continuous deterministic decision system. 

73 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



Each Decision Cycle begins with the current constitutional market objects and engineering state. 

Each Decision Cycle concludes with the publication of an updated Executable Order Book. 

Subsequent Decision Cycles begin using the updated engineering state resulting from participant interaction with the previously published market. 

### 111.3 Decision Cycle Inputs 

Each Decision Cycle SHALL consume: 

- Reference Price; 

- Market Operating Condition; 

- Market Operations Profile; 

- current engineering state; 

- participant execution results; 

- Product Technical Standard configuration. 

The Decision Cycle Engine SHALL NOT independently modify constitutional market objects. 

### 11.4 Decision Cycle Sequence 

Every Decision Cycle SHALL execute the engineering engines established by this standard in the following sequence: 

1. Executable Market 

2. Market Posture Engine 

3. Price Formation Engine 

4. Market Structure Engine 

5. Displayed Quantity Engine 

6. Market Adaptation Engine 

7. Quote Construction Engine 

8. Executable Order Book Publication 

Every Decision Cycle SHALL execute these engineering stages sequentially. 

74 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



### 11.5 Participant Interaction 

Following publication of the Executable Order Book: 

- participant orders may be received; 

- participant orders may execute; 

- inventory positions may change; 

- engineering state may change. 

These updated engineering conditions become inputs to the subsequent Decision Cycle. 

The Decision Cycle Engine does not perform order matching. 

Order matching remains governed by CTS-002. 

### 11.6 Deterministic Continuity 

Given identical: 

- constitutional market objects; 

- engineering state; 

- participant interaction; 

- implementation version, 

every Decision Cycle SHALL produce identical engineering outputs. 

Decision Cycles SHALL therefore be: 

- deterministic; 

- reproducible; 

- independently auditable. 

### 11.7 Engineering Independence 

The Decision Cycle Engine coordinates engineering execution. 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 

75 



It SHALL NOT independently determine: 

- Expected Settlement Value; 

- Reference Price; 

- Market Operating Condition; 

- Market Operations Profile; 

- participant interaction rules. 

Those remain governed by CTS-001 or CTS-002. 

### 11.8 Runtime Continuity 

The completion of one Decision Cycle immediately authorizes the commencement of the next Decision Cycle. 

The SDMM therefore operates as a continuously repeating engineering system throughout every Open Market state. 

## 11.8.1 Decision Cycle Commit 

Upon successful publication of executable quotations, the current Decision Cycle SHALL be committed. 

Decision Cycle commitment SHALL: 

- establish the published executable quotations as the authoritative market; 

- establish every engineering output generated during the Decision Cycle as the authoritative engineering state; 

- finalize deterministic replay records; 

- finalize Decision Cycle audit records; and 

- authorize initiation of the subsequent Decision Cycle. 

Following commitment, no engineering object produced during the completed Decision Cycle SHALL be modified. 

76 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



### 11.9 Transition 

The Decision Cycle Engine defines the continuous runtime operation of the SDMM. 

The following chapter establishes the **Verification and Deterministic Replay Framework** , which governs reconstruction and verification of every engineering decision performed during every Decision Cycle. 

## **Chapter 12** 

### Verification and Deterministic Replay 

#### 12.1 Purpose 

This chapter establishes the engineering requirements governing verification, deterministic replay, and operational validation of the SDMM. 

The Verification and Deterministic Replay Framework ensures that every engineering decision performed by the SDMM can be independently reconstructed, validated, and reproduced. 

Verification is the final engineering stage of the SDMM runtime architecture. 

#### 12.2 Fundamental Principle 

Every Decision Cycle performed by the SDMM SHALL be independently reproducible. 

Given identical: 

- constitutional market objects; 

- engineering state; 

- participant interaction; 

- Product Technical Standard configuration; and 

- implementation version, 

77 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



every conforming implementation SHALL reconstruct identical engineering results. 

Deterministic replay is therefore a mandatory engineering capability of every SDMM implementation. 

#### 12.3 Replay Inputs 

Every Decision Cycle SHALL preserve sufficient information to reconstruct: 

- Executable Market; 

- Market Posture; 

- Reservation Prices; 

- Market Structure; 

- Displayed Quantities; 

- Behavioral Mode; 

- Executable Order Book; 

- participant interaction; 

- resulting engineering state. 

#### 12.4 Deterministic Replay Function 

Let 

𝐷𝑅𝑡 

represent the Deterministic Replay Function for Decision Cycle 𝑡. 

The Deterministic Replay Function is determined by 

𝐷𝑅𝑡 = 𝑅(𝐶𝑂𝑡, 𝐸𝑆𝑡, 𝑃𝐼𝑡, 𝑉𝐸𝑅𝑡) 

where: 

- 𝐶𝑂𝑡= Constitutional Market Objects; 

- 𝐸𝑆𝑡= Engineering State; 

- 𝑃𝐼𝑡= Participant Interaction; 

78 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- 𝑉𝐸𝑅𝑡= Implementation Version. 

#### 12.5 Verification Objectives 

Verification SHALL confirm that every reconstructed Decision Cycle faithfully reproduces: 

- Executable Market; 

- Market Posture; 

- Reservation Prices; 

- Market Structure; 

- Displayed Quantities; 

- Behavioral Mode; 

- Executable Order Book; 

- Every authoritative engineering object SHALL be reproducible from the constitutional inputs, engineering inputs, Decision Cycle Trigger Event, and Product Technical Standard configuration applicable to the original Decision Cycle. 

Verification SHALL demonstrate that every engineering engine operated consistently with this standard. 

#### 12.6 Engineering Independence 

Verification SHALL observe engineering behavior. 

Verification SHALL NOT modify: 

- constitutional market objects; 

- engineering state; 

- participant interaction records. 

Verification is observational. 

It never alters the engineering history being verified. 

79 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



#### 12.7 Runtime Completion 

Completion of every Decision Cycle SHALL conclude one complete runtime iteration of the SDMM. 

The subsequent Decision Cycle SHALL begin using the engineering state resulting from the immediately preceding Decision Cycle. 

The SDMM therefore operates as a continuous deterministic engineering system throughout every Open Market state. 

#### 12.8 Completion of the Standard 

This chapter concludes the SDDM Standard. 

The engineering architecture established by this standard defines the complete runtime behavior of the SDMM. 

Future Product Technical Standards may extend this implementation while preserving the engineering architecture established herein. 

80 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 

