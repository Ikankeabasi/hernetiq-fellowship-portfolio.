# Enterprise Compliance Gap Analysis Report — NovaPay AI

**Audience:** Board and investor due diligence  
**Date:** 28 October 2026  
**Overall risk rating: HIGH**  
**Assessment basis:** Week 14 Governance Gap Assessment and the provided S28/S29 notes.

## Executive Summary

The review identified **four material governance gaps** affecting customer-data separation, training-data approval, model-release controls, and fairness and performance monitoring. The overall risk rating is **HIGH** because these gaps could expose client information or allow unreviewed or deteriorating credit and fraud decisions to affect customers. The most important board action is to require the CTO to pause automatic model releases until customer access controls, data checks, and pre-release review have been evidenced.

## Findings

### 1. Customer data separation

Customer confidentiality is at risk. The policy promises that each enterprise client can access only its own records, but the reviewed process does not visibly confirm that the business requesting records is the same client that signed in. No live cross-client access was reproduced. If the service is within the EU AI Act and qualifies as high-risk, **Article 15** requires appropriate cybersecurity and **Article 9** requires documented risk management. **Action:** the CTO should direct an independent customer-access review within 7 days.

### 2. Unreviewed training data

Credit decisions may be degraded or biased. The policy requires approval for external data, yet one unreviewed source without documented reliability checks or a fairness review was enabled; records show it was included in the 1 October 2024 model update. This does not prove that the source caused a later incident. Where the high-risk rules apply, **Article 10** requires suitable governance and quality of data used to develop and check applicable high-risk systems, and **Article 9** requires risks to be assessed and addressed. **Action:** the data-platform owner should disable the source until approval and required checks are complete, within 14 days.

### 3. Model releases without evidenced approval

A harmful model change could reach customers before its risks are understood. The policy requires evaluation before release, while records show the credit and fraud models were automatically placed into live use on 1 October 2024; the reviewed material does not evidence a pre-release approval gate. A fraud regression was reported after the run, but its cause remains unconfirmed. Where applicable, **Article 9** requires an ongoing risk-management system and **Article 43** sets the relevant conformity-assessment procedure for high-risk systems before market placement or putting into service. **Action:** the CTO and model owner should block unapproved releases before the next promotion and no later than 7 days.

### 4. Fairness and drift monitoring gaps

Unfair or deteriorating decisions may go unnoticed. The model documentation says fairness evaluation is incomplete and uneven data coverage may disadvantage some regions; automatic alerts for significant changes in decision patterns are not configured. One open incident records an approval rate 34% above the national baseline in Lagos Southwest, while a separate fraud issue also remains open. Neither root cause is established. Where applicable, **Article 10** addresses the quality and governance of data used by applicable high-risk systems, while **Article 9** requires risk management throughout the system lifecycle. **Action:** the model-risk owner should triage both incidents within 48 hours and deliver fairness and monitoring evidence within 14 days.

## Regulatory Exposure

| Gap | EU AI Act article | Requirement and relevance |
|---|---|---|
| Customer data separation | Article 15; Article 9 | Cybersecurity appropriate to the system and a documented process to identify, evaluate and address risk. |
| Unreviewed training data | Article 10; Article 9 | Data governance and quality criteria for training, validation and test data; risk controls for identified risks. |
| Model releases without evidenced approval | Article 9; Article 43 | Lifecycle risk management and the relevant conformity-assessment route for applicable high-risk systems before placement or putting into service. Article 43 does not by itself mean every routine retraining needs a new assessment. |
| Fairness and drift monitoring gaps | Article 10; Article 9 | Data quality and an ongoing process for identifying, evaluating and addressing risks. |

**Applicability caveat:** Legal scope is not established by the reviewed records. Annex III, point 5(b), addresses AI used to evaluate creditworthiness of natural persons or establish their credit score; this case describes SME loan applications. Legal/compliance should confirm intended use, affected persons and territorial scope before treating EU AI Act provisions as binding obligations. These are potential exposure areas, not a finding of a legal breach.

## Recommended Actions

1. **Protect client records.** Owner: CTO / API engineering lead. **Within 7 days.** Deliver a documented independent review and passing tests showing one client cannot view another client's records; block release until the evidence is accepted.
2. **Stop unreviewed data use.** Owner: Data-platform / model-operations lead. **Disable immediately; complete controls within 14 days.** Keep the unreviewed source disabled until documented approval, integrity checks, data-quality checks and fairness review are complete; failed checks must stop processing.
3. **Gate model releases.** Owner: CTO and model-platform owner. **Before the next production release, no later than 7 days.** Every release must have evaluation results, a named approver, version information and a tested rollback path; missing approval prevents release.
4. **Resolve monitoring gaps.** Owner: Model-risk lead with credit and fraud model owners. **Assign incident owners within 48 hours; complete within 14 days.** Both incidents must have documented triage decisions; postcode fairness results, thresholds for significant changes in decision patterns and a successful alert test must be retained.

*Basis: Week 14 Governance Gap Assessment, NovaPay AI. This board version omits code locations and tool names. EU AI Act references are to Regulation (EU) 2024/1689; confirm the system's legal scope and classification with qualified counsel.*
