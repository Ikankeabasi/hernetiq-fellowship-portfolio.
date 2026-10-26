# Governance Gap Assessment — NovaPay AI

**Prepared by:** Ikanke Okon Asuquo  
**Fellowship:** HerNetIQ AI Security Fellowship, Cohort 1  
**Domain:** 6 — AI Governance (Governance Gap Assessment)  
**Assessment date:** 26 October 2026  
**Assessment status:** Part A — completed source-level review  
**Overall risk rating:** **HIGH**

## 1. Executive Summary

The review identifies material weaknesses in the controls protecting enterprise-client data, governing training-data inputs, approving model deployments, and detecting unfair or degraded model behaviour. The most direct gaps are visible in the reviewed API and fine-tuning code: the API does not compare the requested tenant with the authenticated client, and the pipeline accepts external training sources without performing the stated integrity checks before automatically deploying retrained models. The model card also records that fairness evaluation for the v2.3.x credit model is incomplete, while the repository contains open credit-approval and fraud-regression incidents. **My verdict is that NovaPay's AI governance programme is not fit for purpose in its currently evidenced state**; I recommend prioritising tenant authorisation, fail-closed data validation, and a controlled deployment gate before the next model promotion.

## 2. Assessment Scope

I reviewed the following artefacts in the provided NovaPay GitHub repository. I used the source code and records as evidence.

| Artefact reviewed | Purpose in this assessment |
|---|---|
| [AI governance policy](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/governance/ai_policy_v1.md) | Compared stated controls with their implementation, particularly Sections 4.1–4.3, 5.2, 6.1–6.2, 7.1–7.2 and 8. |
| [System architecture](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/system-architecture.md) | Checked the documented tenant model, deployment path, monitoring gaps and known operational limitations. |
| [Authentication middleware](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/api/auth_middleware.py) | Checked how the token is decoded and whether the requested tenant is authorised against the authenticated client. |
| [Fine-tuning pipeline](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/model/fine_tuning_pipeline.py) | Checked data-source validation, training flow and whether deployment is gated by evaluation or approval. |
| [Training-data manifest](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/model/training_data_manifest.json) and [pipeline configuration](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/data/pipeline_config.yaml) | Checked approval, hash-verification, schema-validation and bias-review status for each source. |
| [Credit model card](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/model/credit_model_card.md) | Checked intended use, evaluation status, fairness limitations and source-provenance review. |
| [Sample audit log](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/data/sample_audit_log.json) | Correlated the 1 October 2024 pipeline run and automatic production deployments with the documented incident timeline. |
| [Incident 001 — loan approval anomaly](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/incidents/incident-001.md) and [Incident 002 — fraud model regression](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/incidents/incident-002.md) | Checked the recorded symptoms, status and stated unknowns. |

### Assessment approach

I used the **NIST AI Risk Management Framework (NIST AI RMF)** as the diagnostic structure:

- **GOVERN:** policies, roles and accountability.
- **MAP:** risks are identified and contextualised.
- **MEASURE:** risks and model behaviour are evaluated and tracked.
- **MANAGE:** controls, approvals and responses are put into operation.

For each finding, I applied the five policy-reading questions from my S28/S29 notes: What control is claimed? Is a process defined? Who is accountable? What happens when a control fails? Does the code match the policy? I used the **OWASP Top 10 for Large Language Model Applications (OWASP LLM Top 10)** only where the categories in my notes fit the observed risk.

### Evidence standard and limitations

The findings below are based on the cited repository files and the sample audit log. A file or line citation establishes what the repository contains; it does not by itself prove that the same code is deployed unchanged in production. I did not execute exploit attempts, run model evaluations, or reproduce either incident. Where the evidence does not establish root cause, a successful cross-tenant exploit, or the existence of controls outside the reviewed path, I say so. The policy is a Markdown file, so I cite its section and GitHub line range rather than inventing a page number.

## 3. Findings

### Finding 1 — Tenant isolation is stated in policy but is not enforced by the reviewed API path

**Policy claim.** Section 8 states that authenticated clients can access only their own data and that tenant isolation is enforced at the API layer through JSON Web Token (JWT) authentication ([policy §8, lines 96–98](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/governance/ai_policy_v1.md#L96-L98)).

**What I observed.** In the reviewed middleware, `decode_jwt()` calls `_stub_decode()`; the stub returns a hard-coded client identity and expiry rather than validating the supplied token ([`auth_middleware.py`, lines 23–37](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/api/auth_middleware.py#L23-L37)). The score-request handler reads `tenant_id` from the request body, checks only that it is present, and passes it to the scoring function without comparing it with the authenticated client ([lines 40–55](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/api/auth_middleware.py#L40-L55)). The score-retrieval handler similarly passes the requested tenant to the record-fetch function without a visible authorisation comparison ([lines 69–79](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/api/auth_middleware.py#L69-L79)).

This is a source-level gap in the reviewed path. The functions return mock scoring records, and I have not performed a live test; therefore, I am not claiming that I successfully retrieved another client's production data.

**NIST AI RMF mapping.** **GOVERN** — the policy's accountability and access boundary are not demonstrated by the reviewed implementation.

**OWASP LLM Top 10 mapping.** **LLM06 — Sensitive Information Disclosure**, consistent with the fellowship notes' mapping for tenant-isolation controls that are not verified end to end.

**Severity: HIGH.** If the reviewed logic is used as the enforcement path, a client-controlled tenant value could cross the intended data boundary. In a multi-client financial service, that creates a material risk to confidential applicant and scoring records.

**Recommended remediation — owner and deadline.** The **API/platform engineering owner** should, within **7 days**, replace the stub with cryptographic JWT validation, derive the authorised tenant from verified claims, reject tenant mismatches on both scoring and retrieval paths, and add automated negative tests proving that one client cannot access another client's records. The release evidence should include passing cross-tenant tests and a review of the enforcement code.

**Evidence links:** [Policy §8](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/governance/ai_policy_v1.md#L96-L98) · [JWT decoding](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/api/auth_middleware.py#L23-L37) · [Score request](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/api/auth_middleware.py#L40-L55) · [Score retrieval](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/api/auth_middleware.py#L69-L79)

### Finding 2 — Training-data validation can accept an unreviewed external source

**Policy claim.** Section 4.1 requires all training sources to be listed in the manifest and says external sources need documented approval before being added. Section 4.2 says training pipelines include quality checks before training ([policy §§4.1–4.2, lines 40–48](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/governance/ai_policy_v1.md#L40-L48)).

**What I observed.** The manifest marks `bureau_data_external_v2` as `unreviewed`, with hash verification, schema enforcement and bias review all set to false; its notes say that formal review has not been scheduled ([`training_data_manifest.json`, lines 39–47](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/model/training_data_manifest.json#L39-L47)). The pipeline configuration nevertheless enables that source ([`pipeline_config.yaml`, lines 33–42](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/data/pipeline_config.yaml#L33-L42)). In `validate_source()`, the external-source branch explicitly skips hash verification and returns `True`; for other source types, the reviewed function logs that a schema check passed and returns `True` without implementing a check in that function ([`fine_tuning_pipeline.py`, lines 63–72](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/model/fine_tuning_pipeline.py#L63-L72)).

The audit log records the 1 October 2024 pipeline run loading `bureau_data_external_v2` alongside the other sources ([audit log, lines 11791–11798](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/data/sample_audit_log.json#L11791-L11798)). The completed run record shows that both credit and fraud models were retrained ([lines 11804–11813](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/data/sample_audit_log.json#L11804-L11813)). These records show that the source was included in the recorded run; they do not by themselves prove the contents of the dataset or that it caused a later incident.

**NIST AI RMF mapping.** **MAP** — the risk of unreviewed or tampered training data is not adequately identified and validated. **MANAGE** also applies because the pipeline does not fail closed when required source checks are absent.

**OWASP LLM Top 10 mapping.** **LLM03 — Training Data Poisoning.**

**Severity: HIGH.** Unreviewed data is enabled and accepted by the reviewed training path without the integrity checks described by the policy. This can undermine model quality or introduce biased or manipulated data into models used for financial decisions.

**Recommended remediation — owner and deadline.** The **data-platform/MLOps owner** should disable `bureau_data_external_v2` until documented approval is recorded, and within **14 days** implement fail-closed approval, schema, hash and required bias-review checks for every enabled source. Tests must demonstrate that an unapproved source, missing integrity metadata or failed validation stops the run, with the decision and test output retained as audit evidence.

**Evidence links:** [Policy §§4.1–4.2](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/governance/ai_policy_v1.md#L40-L48) · [Manifest source status](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/model/training_data_manifest.json#L39-L47) · [Enabled source configuration](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/data/pipeline_config.yaml#L33-L42) · [Validation function](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/model/fine_tuning_pipeline.py#L63-L72) · [Audit-log pipeline start](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/data/sample_audit_log.json#L11791-L11798)

### Finding 3 — The reviewed fine-tuning path deploys models automatically without showing a pre-deployment approval gate

**Policy claim.** Section 5.2 says models are evaluated on a held-out test set before deployment and that evaluation results are recorded in the model card. Section 6.1 says production deployments are logged with a trigger and version identifier; Section 6.2 describes retaining a previous version for rollback ([policy §§5.2–6.2, lines 62–80](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/governance/ai_policy_v1.md#L62-L80)).

**What I observed.** After the fine-tuning function records a training output path, it calls `_deploy_model()` directly; the reviewed function logs deployment without an evaluation or human-approval check in that path ([`fine_tuning_pipeline.py`, lines 89–100](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/model/fine_tuning_pipeline.py#L89-L100)). The pipeline loops over both the credit and fraud models and runs the same function for each ([lines 103–108](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/model/fine_tuning_pipeline.py#L103-L108)). The audit log confirms production deployments of credit model v2.3.1 and fraud model v1.8.2 with `triggered_by: pipeline_auto` on 1 October 2024 ([audit log, lines 11817–11836](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/data/sample_audit_log.json#L11817-L11836)).

The fraud incident report says the regression began around the 1 October pipeline run and that the root cause was unknown at the time of the report ([Incident 002, lines 18–33](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/incidents/incident-002.md#L18-L33)). The audit log includes post-run transactions marked PASS despite matching profiles previously flagged, for example TXN-88288 ([audit log, lines 11846–11856](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/data/sample_audit_log.json#L11846-L11856)). This is relevant evidence for investigation, but it does **not** prove the pipeline caused the regression.

**NIST AI RMF mapping.** **MANAGE** — the reviewed deployment path does not show a gate that prevents promotion until evaluation and approval requirements have been met.

**OWASP LLM Top 10 mapping.** **LLM09 — Overreliance**, using the fellowship notes' mapping for missing human review before automated decisions. The finding concerns the model promotion process; it does not establish that every individual credit decision is automatically made.

**Severity: HIGH.** Both models are promoted through a shared pipeline, and the repository documents a fraud-regression incident after the recorded run. Without a verifiable evaluation and approval gate, an unsafe model version can reach production before an accountable reviewer has accepted the risk.

**Recommended remediation — owner and deadline.** The **CTO and ML-platform owner** should, before the **next production promotion and no later than 7 days**, block automatic deployment unless held-out evaluation results meet documented acceptance thresholds and a named reviewer approves promotion. The pipeline must record the model version, test result, approver and deployment trigger; a test must prove that a missing evaluation result or approval prevents deployment. The incident owner should assess rollback against the incident evidence rather than assume the pipeline was the root cause.

**Evidence links:** [Policy §§5.2–6.2](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/governance/ai_policy_v1.md#L62-L80) · [Pipeline deployment call](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/model/fine_tuning_pipeline.py#L89-L100) · [Pipeline model loop](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/model/fine_tuning_pipeline.py#L103-L108) · [Production deployment audit events](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/data/sample_audit_log.json#L11817-L11836) · [Fraud incident status](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/incidents/incident-002.md#L18-L33)

### Finding 4 — Fairness assessment and drift detection are incomplete while model-behaviour incidents remain open

**Policy claim.** Section 5.2 requires pre-deployment evaluation, while Section 7.1 describes monitoring for latency and availability and reviewing significant model-output anomalies reported by enterprise clients. Section 7.2 requires incidents to be documented and assigned to a responsible owner ([policy §§5.2 and 7.1–7.2, lines 62–92](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/governance/ai_policy_v1.md#L62-L92)).

**What I observed.** The credit model card says fairness evaluation has not been completed for the v2.3.x series, postcode-level demographic parity has not been evaluated, and regions with less complete bureau data may be systematically underscored. It also says data sources added after v2.1.0 have not undergone formal bias review ([`credit_model_card.md`, lines 33–57](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/model/credit_model_card.md#L33-L57)). The architecture lists model-drift alerting as not configured ([`system-architecture.md`, lines 63–66](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/system-architecture.md#L63-L66)).

Incident 001 records a client report of approval rates in Lagos Southwest postcodes being 34% above the national baseline over six days, states that the root cause is unknown, and remains open ([Incident 001, lines 8–32](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/incidents/incident-001.md#L8-L32)). Incident 002 separately records a fraud-model regression and also remains open with no root cause identified ([Incident 002, lines 8–33](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/incidents/incident-002.md#L8-L33)). These records establish unresolved model-behaviour concerns, not their root cause or proof of discriminatory impact.

**NIST AI RMF mapping.** **MAP** — known postcode and data-completeness limitations have not been fully assessed through a documented fairness evaluation. **MEASURE** — automated drift alerting is not configured. **MANAGE** is relevant to the need to assign owners and make a documented response decision for the open incidents.

**OWASP LLM Top 10 mapping.** No direct OWASP LLM category is assigned to this finding: the evidence concerns credit-model fairness, performance drift and incident handling, and I have not forced it into an unrelated category from the fellowship notes.

**Severity: HIGH.** Lending outcomes may be affected by postcode-level data-completeness differences, and the absence of drift alerts means changes may be noticed only after a client report. The open incidents make documented triage and a measurable monitoring process material priorities.

**Recommended remediation — owner and deadline.** The **model-risk owner**, with the credit and fraud model owners, should within **48 hours** assign named owners and record the triage and containment decisions for both incidents. Within **14 days**, the team should run and document postcode-level fairness tests, define acceptable thresholds and escalation rules, configure drift/performance alerts, and retain evaluation and alert-test evidence. The team must document the root cause only when supported by evidence.

**Evidence links:** [Policy evaluation and monitoring](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/governance/ai_policy_v1.md#L62-L92) · [Credit model card](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/model/credit_model_card.md#L33-L57) · [Architecture known gaps](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/system-architecture.md#L63-L66) · [Incident 001](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/incidents/incident-001.md#L8-L32) · [Incident 002](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/incidents/incident-002.md#L8-L33)

## 4. Regulatory Exposure Summary

The mappings below use the control areas listed in my S28/S29 fellowship notes. The EU AI Act mappings are **conditional**: the repository concerns a financial-services system and the notes identify credit scoring in Annex III, but the reviewed materials do not establish the system's territorial scope or a final legal classification. I therefore treat these as exposure areas for legal/compliance review, not as a conclusion that NovaPay has breached a binding EU obligation. The notes name the control areas for ISO/IEC 42001 but do not provide numbered ISO clauses, so I have not invented clause numbers.

| Finding | Framework or regulation | Specific article, section or control area | Exposure and evidence basis |
|---|---|---|---|
| 1. Tenant isolation | ISO/IEC 42001 | **Risk assessment**; **Roles and responsibilities** | Cross-tenant access is a material risk that needs a defined enforcement owner and evidence that the access boundary works. The policy promise in §8 is not matched by an authorisation comparison in the reviewed middleware. |
| 2. Training-data validation | ISO/IEC 42001 | **Supplier management**; **Risk assessment** | The enabled external source is marked unreviewed and lacks hash, schema and bias-review status; the reviewed pipeline accepts it rather than failing closed. |
| 3. Automatic deployment | ISO/IEC 42001 | **Roles and responsibilities**; **Monitoring and audit** | The reviewed pipeline and audit log show automatic production promotion, but do not show a recorded evaluation result and human approval gate. |
| 3. Automatic deployment | EU AI Act — conditional | **Annex III (credit scoring)** and **Article 9 (risk management system)**, if the system and operator fall within scope and the high-risk requirements apply | Relevant to documented risk controls around a credit-scoring system. Legal applicability and the required conformity process must be confirmed by the responsible legal/compliance owner. |
| 4. Fairness and drift | ISO/IEC 42001 | **Risk assessment**; **Monitoring and audit**; **Incident management** | The model card records incomplete fairness work, the architecture says drift alerting is not configured, and two incident reports remain open. |
| 4. Fairness and drift | EU AI Act — conditional | **Annex III (credit scoring)** and **Article 9 (risk management system)**, if applicable | Potentially relevant to assessing and managing risks for high-risk credit-scoring AI. The evidence here does not establish EU jurisdictional scope or a legal breach. |

NovaPay's policy also says it operates under Central Bank of Nigeria (CBN) guidelines in Section 9 ([policy §9, lines 102–110](https://github.com/AibinuolaDamilola/hernetiq/blob/main/novapay-ai-core/governance/ai_policy_v1.md#L102-L110)). The repository does not identify a particular CBN guideline provision for these findings, so I have not assigned a CBN article or section without evidence.

## 5. Prioritised Remediation Plan

| Priority | Action | Owner | Target | Completion evidence |
|---|---|---|---|---|
| 1 | Correct JWT validation and enforce tenant identity on both score and retrieval endpoints. | API/platform engineering | Within 7 days | Verified token-validation code; passing cross-tenant denial tests; review record. |
| 2 | Disable unreviewed external training data and enforce fail-closed source approval, hash, schema and bias-review checks. | Data platform / MLOps | Disable source immediately; controls and tests within 14 days | Approved manifest record, validation tests showing rejection on failure, retained logs. |
| 3 | Block automatic production promotion until model evaluation passes documented criteria and a named reviewer approves. | CTO / ML platform | Before next promotion, no later than 7 days | Pipeline gate test; held-out evaluation results; approver, version and deployment trigger in audit trail. |
| 4 | Triage both open incidents, assign named owners, run postcode fairness checks and configure drift monitoring. | Model risk and model owners | Owners/triage within 48 hours; testing and alerts within 14 days | Incident records with owners and decisions; fairness results; drift thresholds; alert-test evidence. |

## 6. Overall Verdict

**Verdict: NovaPay's AI governance programme is not fit for purpose in its currently evidenced state.**

The reviewed repository shows an unenforced tenant boundary, training-data checks that can be bypassed, automatic production promotion without an evidenced evaluation-and-approval gate, and incomplete fairness/drift controls while relevant incidents remain unresolved.

## 7. Evidence Verification Record

| Verification question | Result |
|---|---|
| Did I review the actual policy and relevant code? | Yes — the policy, authentication middleware, fine-tuning pipeline, model card, manifest, configuration, architecture and incident records are cited above. |
| Did I review the audit log? | Yes — I inspected the sample JSON audit log and cited the pipeline-run, production-deployment and fraud-check records used in this assessment. |
| Did I run live or runtime tests? | No. The assessment is a source-level review; runtime exploitability and production parity have not been independently tested. |
| Did I confirm that the external dataset caused an incident? | No. The run and incident timelines are relevant, but Incident 002 explicitly records that its root cause was unknown. |
| Did I confirm that the loan-approval anomaly was discriminatory? | No. Incident 001 records an approval-rate difference and states that the direction and cause were not established. |
| Did I confirm EU AI Act applicability or a CBN breach? | No. The required jurisdictional and legal classification evidence is not established in the reviewed repository. |
| Did I change NovaPay's code? | No. I produced this assessment in my fellowship portfolio; I did not modify the NovaPay case repository. |
