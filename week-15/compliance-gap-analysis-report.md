# Enterprise Compliance Gap Analysis Report — NovaPay AI

**Audience:** Board and investor due diligence  
**Date:** 28 October 2026  
**Overall risk rating: HIGH**  
**Source:** Week 14 Governance Gap Assessment and the supplied S28/S29 materials.

## Executive Summary

The review identified **four material governance gaps** affecting customer-data separation, training-data approval, model-release decisions, and fairness and performance monitoring. The overall risk rating is **HIGH** because these gaps could expose confidential records or allow poor or unfair decisions to affect customers. The most important board action is to direct the CTO to pause model releases until customer protections, data approval and independent pre-release checks are evidenced. The European Union Artificial Intelligence Act (EU AI Act) references below are potential exposure areas only until legal/compliance confirms that the Act applies to this system.

## Findings

### 1. Customer data separation — HIGH

Confidential client and applicant records could be exposed if the business requesting records is not checked against the client that signed in. NovaPay's policy promises strict separation, but the reviewed process does not visibly make that comparison; no live cross-client access was reproduced. Where applicable, Articles 9 and 15 of the EU AI Act address risk management and cybersecurity. **Action:** the CTO should commission and approve an independent customer-access review within 7 days, with successful tests showing clients cannot access one another's records.

### 2. Unreviewed training data — HIGH

Credit or fraud decisions could become less reliable or unfair. One external data source was enabled despite being marked unreviewed and lacking documented integrity and fairness checks; records show it was included in the 1 October 2024 update. This does not prove it caused a later incident. Where applicable, Articles 9 and 10 of the EU AI Act address risk management and data governance and quality. **Action:** the data-governance lead should keep the source disabled until approval and checks are documented, within 14 days.

### 3. Model releases without evidenced approval — HIGH

An unsafe model update could reach customers before its results are reviewed. Records show that the credit and fraud models were automatically placed into live use; the reviewed material does not evidence a named person approving the release after testing. A fraud regression was reported afterward, but its cause remains unknown. Where applicable, Articles 9 and 14 address lifecycle risk management and human oversight; Article 43 sets the conformity-assessment procedure for applicable high-risk systems before placing on the market or putting into service. **Action:** the CTO and AI release owner should block unapproved releases before the next release and no later than 7 days.

### 4. Fairness and performance monitoring — HIGH

Some customers may receive inconsistent outcomes, and changes may go unnoticed until a client complains. NovaPay's model documentation says fairness checks are incomplete and some regions have less complete data; monitoring for significant changes in model behaviour is not configured. Two related incidents remain open without confirmed causes. Where applicable, Articles 9 and 10 address lifecycle risk management and data governance. **Action:** the risk and compliance lead should assign incident owners within 48 hours and deliver fairness results and tested monitoring alerts within 14 days.

## Regulatory Exposure

| Gap | EU AI Act articles | Board-level relevance, if applicable |
|---|---|---|
| Customer data separation | Articles 9 and 15 | Risks must be assessed and addressed; applicable high-risk systems must maintain appropriate cybersecurity. |
| Training-data approval | Articles 9 and 10 | Risk controls and data-governance and quality requirements must be in place for applicable high-risk systems. |
| Model release approval | Articles 9, 14 and 43 | Risk management, appropriate human oversight and the relevant conformity assessment are required for applicable high-risk systems. Article 43 does not mean every routine retraining automatically requires a new assessment. |
| Fairness and monitoring | Articles 9 and 10 | The organisation must manage relevant lifecycle risks and apply suitable data-governance and quality practices. |

## Recommended Actions

1. **Protect client records.** Owner: CTO / customer-access engineering lead. **Within 7 days.** Measure: independent review signed off and tests demonstrate clients cannot view one another's records; a release is blocked if evidence is missing.
2. **Stop unreviewed data use.** Owner: data-governance lead. **Disable the source immediately; complete controls within 14 days.** Measure: approval and checks are recorded; failed checks stop processing.
3. **Gate model releases.** Owner: CTO and AI release owner. **Before the next release, no later than 7 days.** Measure: every release has recorded evaluation results, named approval and a tested rollback path; missing approval prevents release.
4. **Resolve monitoring gaps.** Owner: risk and compliance lead with credit and fraud model owners. **Assign owners and triage both incidents within 48 hours; complete fairness and alert testing within 14 days.** Measure: both incidents have recorded decisions; fairness results, thresholds and successful alert tests are retained.

**Board decision requested:** Require the CTO to report back with evidence of completed customer protections, approved training data and an independent release gate before unrestricted model releases resume.

**Legal scope limitation:** Annex III, point 5(b), addresses systems used to evaluate the creditworthiness of natural persons or establish their credit score. The case describes SME loan applications, and the supplied materials do not conclusively establish affected-person scope or EU territorial scope. A legal/compliance owner should confirm applicability before treating these articles as binding obligations or concluding that a breach occurred.

**Official text:** [Regulation (EU) 2024/1689 — EU AI Act, EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27).
