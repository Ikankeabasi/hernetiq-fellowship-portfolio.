# Enterprise Compliance Gap Analysis — NovaPay AI

**Audience:** Board and investor due diligence  
**Date:** 28 October 2026  
**Overall risk rating: HIGH**

## Executive Summary

The review compared NovaPay’s governance commitments with the available case records. It found weaknesses in client-data separation, approval of training data, release of updated models, and fairness and performance monitoring. These could expose confidential records or allow poor or unfair decisions to affect customers. The evidence does not establish that a specific incident was caused by these gaps. European Union Artificial Intelligence Act (EU AI Act) duties below apply only if NovaPay’s system falls within the Act’s scope and relevant high-risk conditions are met.

## Key Findings

1. **Customer data separation — HIGH.** Confidential client and applicant records could be exposed if the business requesting records is not checked against the client that signed in. NovaPay’s policy promises strict separation, but the reviewed process does not visibly make that comparison; no live cross-client access was reproduced. Where applicable, EU AI Act Articles 9 and 15 address risk management and cybersecurity. The CTO should commission and approve an independent customer-access review within 7 days, with successful tests showing that clients cannot access one another’s records.

2. **Unreviewed training data — HIGH.** Credit or fraud decisions could become less reliable or unfair. One external data source was enabled despite being marked unreviewed and lacking documented integrity and fairness checks; records show it was included in the 1 October 2024 update. This does not prove it caused a later incident. Where applicable, Articles 9 and 10 of the EU AI Act address risk management and training-data governance and quality. The data-governance lead should keep the source disabled until approval and checks are documented, within 14 days.

3. **Model releases without evidenced approval — HIGH.** An unsafe model update could reach customers before the results are reviewed. Records show that credit and fraud models were automatically placed into live use; the reviewed material does not evidence a named person approving the release after testing. A fraud regression was reported afterward, but its cause remains unknown. Where applicable, Articles 9 and 14 address lifecycle risk management and human oversight; Article 43 addresses the conformity assessment for applicable high-risk systems before placing on the market or putting into service. The CTO should block unapproved releases before the next release and no later than 7 days.

4. **Fairness and performance monitoring — HIGH.** Some customers may receive inconsistent outcomes, and changes may go unnoticed until a client complains. NovaPay’s model documentation says fairness checks are incomplete and some regions have less complete data; monitoring for significant changes in model behaviour is not configured. Two related incidents remain open without confirmed causes. Where applicable, Articles 9 and 10 address risk management and data governance. The risk and compliance lead should assign incident owners within 48 hours and deliver fairness results and tested monitoring alerts within 14 days.

## Regulatory Exposure

These are potential exposure areas, not findings of a legal breach. Legal/compliance must confirm the system’s intended use, affected persons and territorial scope before treating the EU AI Act as binding.

| Gap | EU AI Act articles | Board-level relevance (if applicable) |
|---|---|---|
| Client data separation | Articles 9, 15 | Risks must be assessed and addressed; applicable high-risk systems must maintain appropriate cybersecurity. |
| Training-data approval | Articles 9, 10 | Risks must be managed; data used for developing and checking applicable high-risk systems must meet data-governance and quality requirements. |
| Model release approval | Articles 9, 14, 43 | Manage risks, provide appropriate human oversight and complete the applicable conformity assessment before placing a high-risk system on the market or putting it into service. |
| Fairness and monitoring | Articles 9, 10 | Manage lifecycle risks and apply suitable data-governance and quality practices. |

## Prioritised Actions

1. **Protect client records.** Owner: CTO / customer-access engineering lead. **Deadline:** 7 days. **Measure:** independent review signed off and tests prove clients cannot view one another’s records; block release if evidence is missing.
2. **Stop unreviewed data use.** Owner: data-governance lead. **Deadline:** disable source immediately; controls within 14 days. **Measure:** approval and data checks recorded; failed checks stop processing.
3. **Gate model releases.** Owner: CTO and AI release owner. **Deadline:** before the next release, no later than 7 days. **Measure:** every release has recorded evaluation results, named approval, model version and tested rollback; no approval means no release.
4. **Resolve monitoring gaps.** Owner: risk and compliance lead with credit and fraud model owners. **Deadline:** owners and incident triage within 48 hours; fairness and alert testing within 14 days. **Measure:** both incidents have recorded decisions; fairness results, thresholds and successful alert tests are retained.

**Board decision requested:** Require the CTO to report back with evidence of completed access controls, approved training data and a human release gate before unrestricted model releases resume.

**Scope note:** SME credit applications are described in the case, but the available evidence does not conclusively establish EU territorial scope or the precise high-risk classification. Annex III, point 5(b), concerns assessing the creditworthiness of natural persons. Qualified legal/compliance review is required. Source: [Regulation (EU) 2024/1689, official consolidated text — EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27).
