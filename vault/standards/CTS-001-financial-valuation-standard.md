---
description: "Edwin's CTS-001 master draft — laws, definitions and financial architecture for ESV valuation of InPlay Securities; the Section 3 math is missing"
---

## JULY 1, 2026 

# INPLAY CORE TECHNICAL STANDARDS CTS-001 FINANCIAL VALUATION STANDARD (FVS-1 MASTER DRAFT) 

EDWIN JOHNSON - FOUNDER, CHAIRMAN, & CEO INPLAY GLOBAL, INC. 333 SE 2nd Avenue, Suite 2000 Miami, Florida 33131 



## **TRADE SECRET OF INPLAY GLOBAL, INC.** 

This document contains confidential, proprietary, and trade secret information of InPlay Global, Inc. It is furnished solely for authorized evaluation, development, implementation, legal review, or other approved business purposes. Unauthorized use, copying, disclosure, distribution, reproduction, reverse engineering, or derivative use of any portion of this document is strictly prohibited without the prior written consent of InPlay Global, Inc. 

## **INPLAY CORE TECHNICAL STANDARDS** 

## CTS-001 

## Financial Valuation Standard (FVS-1) 

**Version:** 1.0 (Master Draft) 

**Document Classification:** Internal Authoritative Technical Standard 

**Status:** Draft – Subject to Formal Approval 

**Owner:** InPlay Global, Inc. 

## Section 1A – Part 1 

## Governance, Authority and Foundational Principles 

## 1.1 Authority 

The **InPlay Core Technical Standards ("CTS")** establish the authoritative financial, mathematical, technical, and operational standards governing the issuance, valuation, trading, settlement, and lifecycle management of InPlay Securities. 

CTS-001 establishes the governing Financial Valuation Standard for the InPlay platform. 

1 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



All subsequent Core Technical Standards, valuation methodologies, software implementations, operational procedures, market operations, and product specifications SHALL conform to this standard unless expressly superseded by an approved revision. 

Where any conflict exists between this standard and a subsequent implementation, the provisions of CTS-001 SHALL prevail. 

## 1.2 Foundational Statement 

The **InPlay Valuation System ("IVS")** is the authoritative financial valuation system of the InPlay platform. 

Its sole purpose is to continuously determine the **Expected Settlement Value ("ESV")** of every issued InPlay Security in accordance with this Financial Valuation Standard. 

Expected Settlement Value is determined independently of market price. 

Market prices are discovered independently through transactions between market participants in the secondary market. 

Financial valuation and market price discovery are separate and independent functions. Neither function determines or redefines the other. 

Capitalized terms used within this section are defined in Section 1C unless expressly stated otherwise. 

## 1.3 Purpose 

This Financial Valuation Standard establishes the governing principles, financial architecture, valuation methodology, and mathematical requirements used to determine the Expected Settlement Value of every InPlay Security. 

The standard provides a single authoritative framework governing financial valuation throughout the InPlay platform. 

Its objectives are to ensure that every Expected Settlement Value is: 

2 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- contractually correct; 

- mathematically consistent; 

- continuously re-estimated; 

- deterministic; 

- reproducible; 

- independently auditable; and 

- fully explainable. 

No implementation of the InPlay Valuation System may produce an Expected Settlement Value inconsistent with this standard. 

The Financial Valuation Standard governs valuation only. 

It does not govern: 

- market making; 

- order execution; 

- order routing; 

- price discovery; 

- trading operations; or 

- settlement mechanics. 

Those subjects are governed by subsequent InPlay Core Technical Standards. 

## Section 1A — Part 2 

## 1.4 Scope 

This Financial Valuation Standard governs the complete financial valuation lifecycle of every InPlay Security. 

Specifically, this standard governs: 

- Expected Settlement Value ("ESV"); 

- financial valuation methodology; 

- valuation governance; 

- valuation integrity; 

- valuation lineage; 

- valuation reconciliation; 

3 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- valuation auditability; and 

- valuation reproducibility. 

This standard applies throughout the lifecycle of every InPlay Security, including: 

- Initial Public Offerings ("IPOs"); 

- simulation environments; 

- promotional trading events; 

- educational trading programs; 

- internal testing and certification environments; 

- regulated secondary market trading; 

- Alternative Trading Systems ("ATS"); 

- future registered securities exchange operations; and 

- other Board-approved operating environments. 

For securities issued through an Initial Public Offering, this standard governs the Initial Valuation from which all subsequent Expected Settlement Value determinations originate. 

The financial valuation methodology established by this standard SHALL remain identical across all Operating Environments. 

Operating Environments MAY differ with respect to: 

- participant eligibility; 

- trading rules; 

- execution methodology; 

- settlement mechanics; 

- reporting requirements; and 

- regulatory obligations. 

Such differences SHALL NOT modify the financial valuation methodology established by this standard. 

## 1.5 InPlay Valuation System (IVS) 

The **InPlay Valuation System ("IVS")** is the exclusive financial valuation system authorized to determine the Expected Settlement Value of every issued InPlay Security. 

The IVS operates in accordance with: 

4 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- this Financial Valuation Standard; 

- approved valuation methodologies; 

- approved valuation inputs; 

- approved probability methodologies; 

- approved governance procedures; and 

- approved audit controls. 

For every issued InPlay Security, the IVS SHALL produce one—and only one—authoritative Expected Settlement Value. 

The IVS SHALL remain independent of: 

- observed market prices; 

- bid prices; 

- offer prices; 

- quoted spreads; 

- participant sentiment; 

- market-maker inventory; 

- liquidity conditions; and 

- ordinary market activity. 

Where the governing offering documents expressly define an operational metric as a Contractual Economic Right or Approved Valuation Input, that metric SHALL be incorporated into the valuation process in accordance with this standard. 

No other market information may directly determine Expected Settlement Value. 

## 1.6 Design Objectives 

The Financial Valuation Standard establishes the following design objectives. 

### Objective 1 — Authoritative Valuation 

Every issued InPlay Security SHALL possess exactly one authoritative Expected Settlement Value. 

5 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



### Objective 2 — Contractual Accuracy 

Expected Settlement Value SHALL represent only the contractual economic value attributable to the corresponding InPlay Security. 

### Objective 3 — Continuous Valuation 

Expected Settlement Value SHALL be continuously re-estimated whenever Approved Valuation Inputs materially affect the estimated contractual economic value of an issued InPlay Security. 

Valuation is information-driven. 

It is not interval-driven. 

### Objective 4 — Deterministic Operation 

Given identical: 

- Contractual Economic Rights; 

- Approved Valuation Inputs; 

- valuation methodology; and 

- valuation version, 

Every implementation SHALL produce an identical Expected Settlement Value. 

### Objective 5 — Complete Reconciliation 

Every Expected Settlement Value SHALL reconcile exactly to the complete set of Contractual Economic Rights attributable to the corresponding InPlay Security. 

6 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



### Objective 6 — Auditability 

Every Expected Settlement Value SHALL be reproducible, independently auditable, and fully traceable throughout its valuation lineage. 

### Objective 7 — Explainability 

Every Expected Settlement Value SHALL be capable of complete decomposition into its underlying Economic Components and Approved Valuation Inputs. 

### Objective 8 — Operating Environment Independence 

The Financial Valuation Standard SHALL operate identically regardless of the Operating Environment in which an InPlay Security is issued, offered, traded, or settled. 

## Section 1A — Part 3 

## 1.7 Governing Principles 

The Financial Valuation Standard governs the determination of Expected Settlement Value for every issued InPlay Security. 

The Financial Valuation Standard does not govern: 

- market prices; 

- market-making methodology; 

- execution algorithms; 

- liquidity management; 

- order handling; 

- participant behavior; or 

- trading strategy. 

Those functions operate independently of the valuation process and are governed by separate InPlay Core Technical Standards. 

7 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 1.8 Interpretation 

This section establishes the constitutional framework governing the Financial Valuation Standard. 

All subsequent provisions of CTS-001 SHALL be interpreted consistently with the authority, scope, and objectives established herein. 

Where ambiguity exists within a subsequent section, interpretation SHALL be guided by the principles established in this Section 1A. 

No subsequent technical standard, software implementation, operational procedure, or product specification may modify the governing principles established by this section except through an approved revision of CTS-001. 

## 1.9 Conformance 

Every implementation of the InPlay Valuation System SHALL conform to the requirements established by this Financial Valuation Standard. 

Conformance requires that every Expected Settlement Value produced by an implementation be: 

- contractually correct; 

- mathematically consistent; 

- deterministic; 

- continuously re-estimated; 

- reproducible; 

- independently auditable; and 

- fully explainable. 

Any implementation that fails to satisfy these requirements SHALL be considered nonconforming with CTS-001. 

8 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 1.10 Transition to Constitutional Laws 

Section 1A establishes the governing authority, purpose, scope, and design objectives of the Financial Valuation Standard. 

Section 1B establishes the Constitutional Laws governing every implementation of the InPlay Valuation System. 

Those Constitutional Laws are immutable unless amended through an approved revision of the InPlay Core Technical Standards. 

## Section 1B — Constitutional Laws of Financial 

## Valuation 

## 1.11 Constitutional Authority 

The following Constitutional Laws establish the immutable principles governing the Financial Valuation Standard. 

Every implementation of the InPlay Valuation System SHALL conform to these laws. 

No subsequent Core Technical Standard, software implementation, valuation methodology, operational procedure, or product specification may contradict these laws unless expressly amended through an approved revision of CTS-001. 

## 1.12 Law of Contractual Valuation 

Expected Settlement Value SHALL represent only the contractual economic value attributable to an issued InPlay Security. 

Only Contractual Economic Rights recognized by the governing offering documents and this Financial Valuation Standard may contribute to Expected Settlement Value. 

No discretionary economic value may be introduced. 

9 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 1.13 Law of Continuous Valuation 

Expected Settlement Value SHALL be continuously re-estimated whenever Approved Valuation Inputs materially affect the estimated contractual economic value of an issued InPlay Security. 

Valuation SHALL be information-driven. 

Valuation SHALL NOT be interval-driven. 

## 1.14 Law of Independence from Market Price 

Expected Settlement Value SHALL remain independent of market price discovery. 

Observed market prices, quotations, participant behavior, market-maker activity, liquidity conditions, and ordinary market activity SHALL NOT directly determine Expected Settlement Value. 

Only Approved Valuation Inputs recognized by this Financial Valuation Standard may influence Expected Settlement Value. 

## 1.15 Law of Determinism 

The Financial Valuation Standard SHALL be deterministic. 

Given identical: 

- Contractual Economic Rights; 

- Approved Valuation Inputs; 

- valuation methodology; and 

- valuation version, 

every conforming implementation SHALL produce an identical Expected Settlement Value. 

Implementation language, hardware architecture, execution environment, geographic location, or execution time SHALL NOT alter the resulting valuation. 

10 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 1.16 Law of Valuation Lineage 

Every Expected Settlement Value SHALL possess complete valuation lineage. 

Every valuation SHALL be reproducible from: 

- the Initial Valuation; 

- every approved valuation update; 

- the applicable valuation methodology; and 

- • the governing valuation version. 

No Expected Settlement Value may exist without complete valuation lineage. 

## 1.17 Law of Complete Representation 

Every Contractual Economic Right SHALL be represented exactly once. 

No Contractual Economic Right may be omitted. 

No Contractual Economic Right may be represented multiple times. 

Every Expected Settlement Value SHALL reconcile exactly to the complete set of Contractual Economic Rights attributable to the corresponding InPlay Security. 

## 1.18 Law of Explainability 

Every Expected Settlement Value SHALL be fully explainable. 

Every valuation SHALL be decomposable into: 

- its constituent Economic Components; 

- the applicable Approved Valuation Inputs; and 

- the valuation methodology applied. 

No undocumented adjustment, hidden weighting factor, discretionary override, or opaque heuristic may contribute to Expected Settlement Value. 

11 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 1.19 Law of Functional Independence 

Financial valuation and market price discovery are independent functions. 

The Financial Valuation Standard determines Expected Settlement Value. 

Market participants discover market prices through secondary market transactions. 

Neither function SHALL redefine the other. 

## 1.20 Law of Operating Environment Independence 

The Financial Valuation Standard SHALL operate identically across all approved Operating Environments. 

Operating Environments MAY differ with respect to: 

- participant eligibility; 

- trading rules; 

- execution methodology; 

- settlement mechanics; and 

- regulatory obligations. 

Operating Environments SHALL NOT alter the financial valuation methodology established by this standard. 

## 1.21 Law of Financial Integrity 

Every Expected Settlement Value produced by the InPlay Valuation System SHALL satisfy all of the following characteristics: 

- contractually correct; 

- mathematically consistent; 

- deterministic; 

- continuously re-estimated; 

- fully reconciled; 

12 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- reproducible; 

- independently auditable; and 

- fully explainable. 

Failure to satisfy any of these characteristics constitutes non-conformance with CTS-001. 

## Section 1C — Authoritative Definitions 

## 1.22 Purpose 

Section 1C establishes the authoritative terminology governing the Financial Valuation Standard. 

Every capitalized term defined herein possesses a single authoritative meaning throughout the InPlay Core Technical Standards. 

Unless expressly amended through an approved revision of CTS-001, these definitions SHALL govern every subsequent technical standard, software implementation, operational procedure, valuation methodology, and product specification. 

## 1.23 Legal Objects 

## 1.23.1 Team Company 

A **Team Company** is a special-purpose operating company established to own the Contractual Economic Rights associated with one Defined Event and to issue common equity representing proportional ownership interests in those rights. 

The Team Company is the primary legal and financial entity recognized by the Financial Valuation Standard. 

13 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 1.23.2 Defined Event 

A **Defined Event** is the contractual competitive period associated with a Team Company. 

The Defined Event establishes: 

- the contractual performance period; 

- the contractual settlement period; and 

- the Contractual Economic Rights attributable to the corresponding InPlay Security. 

A Defined Event may represent a regular season, playoff competition, tournament, championship, international competition, or another Board-approved competitive format. 

## 1.23.3 Contractual Economic Rights 

**Contractual Economic Rights** are the legally enforceable economic interests owned by a Team Company and defined by the governing offering documents. 

Only Contractual Economic Rights recognized by this Financial Valuation Standard may contribute to Expected Settlement Value. 

Contractual Economic Rights may include: 

- performance-based rights; 

- commercial rights; 

- participation-based allocations; 

- revenue allocations; 

- expense allocations; and 

- other expressly defined contractual economic interests. 

## 1.23.4 InPlay Security 

An **InPlay Security** is a share of non-voting common equity issued by a Team Company. 

Ownership of an InPlay Security represents a proportional ownership interest in the issuing Team Company. 

14 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



The Expected Settlement Value attributable to an InPlay Security is derived exclusively from the Contractual Economic Rights owned by the issuing Team Company. 

Ownership of an InPlay Security does not constitute direct ownership of the underlying Contractual Economic Rights or any other assets except as expressly provided by the governing offering documents. 

## 1.24 Financial Objects 

## 1.24.1 Initial Valuation 

The **Initial Valuation** is the first authoritative Expected Settlement Value assigned to an InPlay Security. 

The Initial Valuation establishes the financial valuation baseline from which all subsequent Expected Settlement Value determinations originate. 

## 1.24.2 Expected Settlement Value (ESV) 

**Expected Settlement Value ("ESV")** is the authoritative financial estimate produced by the InPlay Valuation System. 

Expected Settlement Value represents the continuously re-estimated contractual economic value attributable to one issued InPlay Security. 

Expected Settlement Value is independent of observed market prices. 

## 1.24.3 Continuous Economic Revaluation 

**Continuous Economic Revaluation** is the process by which the InPlay Valuation System continuously updates Expected Settlement Value in response to changes in Approved Valuation Inputs. 

15 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 1.24.4 Valuation Lineage 

**Valuation Lineage** is the complete historical record documenting every Expected Settlement Value from the Initial Valuation through contractual settlement. 

Valuation Lineage enables complete reconstruction, verification, and audit of every valuation produced by the InPlay Valuation System. 

## 1.25 Financial Representation Objects 

## 1.25.1 Economic Component 

An **Economic Component** is the standardized financial representation of exactly one Contractual Economic Right. 

Economic Components constitute the exclusive mathematical objects valued by the InPlay Valuation System. 

## 1.25.2 Economic Component Framework (ECF) 

The **Economic Component Framework ("ECF")** is the standardized financial representation architecture governing all Economic Components recognized by the Financial Valuation Standard. 

## 1.25.3 Economic Component Registry (ECR) 

The **Economic Component Registry ("ECR")** is the authoritative registry of every Economic Component recognized by the Financial Valuation Standard. 

The ECR governs identity, registration, lifecycle, contractual origin, and audit history. 

16 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



The ECR does not determine valuation. 

## 1.26 System Objects 

## 1.26.1 InPlay Valuation System (IVS) 

The **InPlay Valuation System ("IVS")** is the exclusive financial valuation system authorized to determine Expected Settlement Value. 

The IVS operates exclusively in accordance with this Financial Valuation Standard. 

## 1.26.2 Approved Valuation Input 

An **Approved Valuation Input** is information expressly authorized by the Financial Valuation Standard for use in determining Expected Settlement Value. 

## 1.26.3 Material Information 

**Material Information** is any Approved Valuation Input that materially changes the estimated contractual economic value represented by one or more Economic Components. 

## 1.26.4 Operating Environment 

An **Operating Environment** is the implementation context within which an InPlay Security is issued, offered, traded, valued, or settled. 

Operating Environments govern operational behavior. 

They do not modify the Financial Valuation Standard. 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 

17 



## **Section 2A** 

## Financial Architecture of an InPlay Security 

## 2.1 Purpose 

This section establishes the financial architecture governing every InPlay Security recognized by the Financial Valuation Standard. 

It defines: 

- the legal entity from which every InPlay Security originates; 

- the ownership and organization of Contractual Economic Rights; 

- the relationship between equity ownership and contractual economics; and 

- the financial hierarchy upon which the InPlay Valuation System operates. 

This section defines financial architecture only. 

It does not define valuation methodology, probability estimation, market operations, or settlement mechanics. 

## 2.2 Foundational Principle 

Every InPlay Security originates from a Team Company. 

The Team Company exists to own a defined set of Contractual Economic Rights and to issue common equity representing proportional ownership interests in those rights. 

The Financial Valuation Standard recognizes the Team Company as the sole financial entity from which an InPlay Security derives its contractual economic value. 

18 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 2.3 Financial Hierarchy 

Every issued InPlay Security shall conform to the following immutable financial hierarchy. 

Team Company ↓ Contractual Economic Rights ↓ InPlay Security ↓ Expected Settlement Value ↓ Secondary Market Price 

Each level derives from the level immediately above it. 

No implementation may reverse, bypass, or redefine these relationships. 

## 2.4 Team Company 

The Team Company is the exclusive legal owner of the Contractual Economic Rights associated with a Defined Event. 

The Team Company serves as the capital formation vehicle through which those rights are converted into publicly issued equity securities. 

The Financial Valuation Standard recognizes only the Team Company as the legal source of contractual economic value. 

## 2.5 Contractual Economic Rights 

Contractual Economic Rights constitute the complete set of legally enforceable economic interests owned by the Team Company. 

These rights define every contractual source of shareholder economic participation recognized by the Financial Valuation Standard. 

19 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



Expected Settlement Value is derived exclusively from these rights. 

No Expected Settlement Value may exist independently of the Contractual Economic Rights owned by the issuing Team Company. 

## 2.6 Equity Ownership 

An InPlay Security is a share of common equity issued by a Team Company. 

Ownership of an InPlay Security represents a proportional ownership interest in the issuing Team Company. 

Accordingly, shareholders participate economically in the Contractual Economic Rights exclusively through their ownership of the Team Company. 

Ownership of an InPlay Security does not constitute direct ownership of individual Contractual Economic Rights. 

## 2.7 Expected Settlement Value 

Expected Settlement Value represents the financial value attributable to one issued InPlay Security. 

The InPlay Valuation System determines Expected Settlement Value by continuously estimating the value of the Contractual Economic Rights owned by the issuing Team Company and attributing that value proportionally to each outstanding share. 

Expected Settlement Value is therefore a property of the issued security rather than the Team Company itself. 

## 2.8 Secondary Market Price 

Following issuance, market participants independently discover market prices through transactions in the secondary market. 

20 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



Market prices reflect negotiated transactions between buyers and sellers. 

Expected Settlement Value reflects the independent financial valuation produced by the InPlay Valuation System. 

These values may differ throughout the life of an InPlay Security. 

## 2.9 Structural Immutability 

The legal structure of a Team Company's Contractual Economic Rights is established by the governing offering documents. 

That structure remains unchanged unless amended pursuant to those governing documents. 

The estimated financial value attributable to that structure may change continuously. 

Accordingly, the Financial Valuation Standard distinguishes between: 

- legal structure; 

- financial representation; and 

- financial valuation. 

Only financial valuation changes continuously. 

## 2.10 Constitutional Financial Relationships 

The Financial Valuation Standard recognizes the following immutable financial relationships. 

- The Team Company owns the Contractual Economic Rights. 

- Contractual Economic Rights constitute the exclusive source of shareholder economic participation. 

- InPlay Securities represent proportional equity ownership in the issuing Team Company. 

- Expected Settlement Value is derived exclusively from the Contractual Economic Rights owned by the Team Company. 

21 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



- Secondary market prices are independently discovered through transactions between market participants. 

No subsequent Core Technical Standard may alter these constitutional financial relationships. 

## **Section 2B** 

## Financial Representation Architecture 

## 2.11 Purpose 

This section establishes the financial representation architecture governing every Contractual Economic Right recognized by the Financial Valuation Standard. 

The Financial Valuation Standard does not perform valuation directly upon legal documents. 

It performs valuation upon standardized financial representations of those contractual rights. 

This representation architecture provides the foundation for deterministic valuation, reconciliation, auditability, and software implementation. 

## 2.12 Principle of Financial Representation 

Every Contractual Economic Right recognized by the Financial Valuation Standard SHALL possess exactly one standardized financial representation. 

No Contractual Economic Right may contribute to Expected Settlement Value without such representation. 

Conversely, every standardized financial representation SHALL correspond to exactly one Contractual Economic Right. 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 

22 



This establishes a one-to-one relationship between legal rights and financial representation. 

## 2.13 Economic Component Framework 

The **Economic Component Framework ("ECF")** is the exclusive financial representation architecture recognized by the Financial Valuation Standard. 

The ECF converts Contractual Economic Rights into standardized financial objects capable of deterministic mathematical valuation. 

The ECF governs representation only. 

It does not determine valuation. 

## 2.14 Principle of Representation Completeness 

The Economic Component Framework SHALL completely represent the contractual economics owned by the issuing Team Company. 

Accordingly: 

- every Contractual Economic Right SHALL possess one Economic Component; 

- every Economic Component SHALL represent one Contractual Economic Right; 

- no Contractual Economic Right may be omitted; and 

- no Contractual Economic Right may be represented more than once. 

Representation completeness is a constitutional requirement of the Financial Valuation Standard. 

## 2.15 Structural Identity 

Every Economic Component possesses a permanent structural identity. 

Structural identity establishes: 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 

23 



- contractual origin; 

- legal identity; 

- component classification; 

- registration history; and 

- audit traceability. 

Structural identity remains immutable throughout the lifecycle of the Economic Component unless modified pursuant to the governing offering documents. 

## 2.16 Economic Value 

Every Economic Component also possesses a continuously re-estimated economic value. 

Unlike structural identity, economic value is dynamic. 

Economic value changes whenever Approved Valuation Inputs materially affect the estimated contractual economic value represented by the Economic Component. 

The Financial Valuation Standard therefore distinguishes between: 

- immutable representation; and 

- continuously changing valuation. 

## 2.17 Economic Component Registry 

The **Economic Component Registry ("ECR")** is the authoritative registry governing every Economic Component recognized by the Financial Valuation Standard. 

The ECR governs: 

- identity; 

- registration; 

- lifecycle; 

- contractual origin; 

- audit history; and 

- version control. 

24 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



The ECR does not perform valuation. 

Its responsibility is authoritative representation. 

## 2.18 Representation Lifecycle 

Every Economic Component progresses through the following lifecycle. 

Registered ↓ Active ↓ Continuously Re-estimated ↓ Settled ↓ Archived 

The lifecycle governs representation only. 

Valuation is governed independently by the InPlay Valuation System. 

## 2.19 Representation Integrity 

Every Expected Settlement Value SHALL be fully reconcilable to the complete set of registered Economic Components. 

Accordingly: 

- every Economic Component SHALL remain uniquely identifiable; 

- every Expected Settlement Value SHALL be reproducible from the Economic Component Registry; 

- every valuation SHALL preserve complete audit traceability. 

Representation integrity SHALL remain independent of changes in economic value. 

25 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 2.20 Transition to Valuation Mathematics 

Sections 2A and 2B establish: 

- the financial architecture of an InPlay Security; and 

- the standardized representation of the Contractual Economic Rights owned by the issuing Team Company. 

Section 3 defines the mathematical valuation of those represented rights. 

Accordingly, the Financial Valuation Standard values Economic Components rather than legal documents. 

## **Section 2C** 

## Economic Component Framework 

## 2.21 Purpose 

This section establishes the Economic Component Framework governing every Economic Component recognized by the Financial Valuation Standard. 

The Economic Component Framework defines the permissible classes of Contractual Economic Rights recognized by the InPlay Valuation System. 

It does not define valuation methodology. 

It defines only the financial objects eligible for valuation. 

## 2.22 Economic Components 

An Economic Component is the exclusive financial representation of one Contractual Economic Right. 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 

26 



Every Economic Component belongs to one—and only one—Economic Component Class. 

Every Expected Settlement Value is derived exclusively from the aggregation of recognized Economic Components. 

No other financial object may contribute to Expected Settlement Value. 

## 2.23 Economic Component Classes 

Version 1.0 of the Financial Valuation Standard recognizes the following Economic Component Classes. 

### Performance Components 

Performance Components represent Contractual Economic Rights derived from competitive performance occurring during a Defined Event. 

### Commercial Components 

Commercial Components represent Contractual Economic Rights arising from contractually defined commercial arrangements. 

### Revenue Allocation Components 

Revenue Allocation Components represent Contractual Economic Rights arising from contractually defined allocation methodologies. 

### Expense Components 

Expense Components represent contractually defined economic deductions attributable to the issuing Team Company. 

Future Economic Component Classes may be introduced only through an approved revision of the Financial Valuation Standard. 

No implementation may create additional classes independently. 

27 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 2.24 Principle of Exclusivity 

Every Contractual Economic Right recognized by the Financial Valuation Standard SHALL belong to exactly one Economic Component Class. 

Economic Component Classes SHALL remain mutually exclusive. 

No Contractual Economic Right may simultaneously belong to multiple classes. 

## 2.25 Principle of Extensibility 

The Economic Component Framework is designed to permit the introduction of additional Economic Component Classes without modifying: 

- the Financial Architecture established in Section 2A; 

- the Financial Representation Architecture established in Section 2B; or 

- the mathematical aggregation methodology established by Section 3. 

Future component classes inherit the governing principles established by this Financial Valuation Standard. 

## 2.26 Principle of Representation Consistency 

Every Economic Component Class SHALL conform to the Financial Representation Architecture established by this standard. 

Accordingly, every Economic Component SHALL possess: 

- one contractual origin; 

- one structural identity; 

- one representation lifecycle; 

- one valuation methodology; and 

- one continuously re-estimated economic value. 

Only the valuation methodology differs among Economic Component Classes. 

28 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



The governing representation architecture remains identical. 

## 2.27 Foundation for Financial Valuation 

The Financial Valuation Standard recognizes only Economic Components as mathematical valuation objects. 

Section 3 defines the mathematical valuation methodology applicable to each Economic Component Class. 

No valuation equation may operate directly upon Contractual Economic Rights or governing legal documents. 

All mathematical valuation SHALL operate exclusively upon the Economic Components established by this framework. 

## **Section 2D** 

## Transition to Financial Valuation 

## 2.28 Purpose 

This section establishes the boundary between the financial architecture defined by Section 2 and the mathematical valuation methodology established by Section 3. 

Section 2 defines the financial objects recognized by the Financial Valuation Standard. 

Section 3 defines the mathematical valuation of those financial objects. 

29 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 2.29 Financial Representation Principle 

The Financial Valuation Standard distinguishes between: 

- legal rights; 

- financial representation; and 

   - financial valuation. 

- 

These functions are independent. 

The governing offering documents define Contractual Economic Rights. 

The Economic Component Framework represents those rights. 

The InPlay Valuation System values those represented rights. 

No implementation may combine or redefine these functions. 

## 2.30 Mathematical Domain 

The mathematical domain of the Financial Valuation Standard consists exclusively of the Economic Components recognized by the Economic Component Framework. 

Accordingly: 

- legal documents are not mathematical objects; 

- Contractual Economic Rights are not mathematical objects; and 

- Team Companies are not mathematical objects. 

The exclusive mathematical objects recognized by the Financial Valuation Standard are Economic Components. 

All valuation mathematics SHALL operate exclusively upon those objects. 

30 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



## 2.31 Valuation Inputs 

Every valuation performed by the InPlay Valuation System SHALL be derived exclusively from: 

- registered Economic Components; 

- Approved Valuation Inputs; 

- approved valuation methodologies; and 

- the governing valuation version. 

No valuation may rely upon undocumented assumptions or external information not recognized by the Financial Valuation Standard. 

## 2.32 Transition to Mathematics 

With completion of Section 2, the Financial Valuation Standard establishes: 

- the legal entity; 

- the financial architecture; 

- the Contractual Economic Rights; 

- the standardized financial representation of those rights; and 

- the complete set of Economic Components recognized by the Financial Valuation Standard. 

Section 3 defines the mathematical valuation of those Economic Components. 

Accordingly, every valuation equation defined by the Financial Valuation Standard SHALL operate exclusively upon the financial representation architecture established by this section. 

## 2.33 Financial Valuation Architecture 

GOVERNING OFFERING DOCUMENTS ▼ 

31 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 



CONTRACTUAL ECONOMIC RIGHTS │ │ ▼ TEAM COMPANY │ │ issues ▼ INPLAY SECURITIES (COMMON EQUITY) │ │ represented as ▼ ECONOMIC COMPONENT FRAMEWORK │ │ valued by ▼ INPLAY VALUATION SYSTEM (IVS) │ │ produces ▼ EXPECTED SETTLEMENT VALUE (ESV) │ │ consumed by ▼ MARKET QUALITY / MARKET MAKER │ ▼ SECONDARY MARKET PRICE 

32 

Confidential & Proprietary | Trade Secret of InPlay Global, Inc. | Version 1.0 

