# Governance Gap Assessment — PayGuard AI

**Prepared by:** Ikanke Okon Asuquo  
**Fellowship:** HerNetIQ AI Security Fellowship, Cohort 1  
**Domain:** 6 — AI Governance (Governance Gap Assessment)  
**Status:** Working draft — policy artefact and audit log outstanding

## 1. Executive Summary

I reviewed the available PayGuard AI configuration and fine-tuning pipeline code to check whether important AI security controls are enforced in practice. The code shows material gaps around tenant isolation, fine-tuning data validation, and verification of the external embedding model source. These gaps could expose confidential client information or allow untrusted data and components to affect the AI system. The actual governance policy and audit log were not available in the materials I could access, so the policy clause citations and audit-log conclusions still need to be confirmed before final submission.

## 2. Assessment Scope

**Reviewed artefacts**

- `ai-security-defense-lab/fixtures/level4_payguard/rag_config.py`
- `ai-security-defense-lab/fixtures/level4_payguard/finetune_pipeline_dag.py`
- The PayGuard Level 4 scenario and code display in `ai-security-defense-lab/levels/level4_payguard.py`

**Not available for this review**

- The client’s actual AI governance policy document, including clause and page numbers.
- A production audit log or log export.

I have not invented policy quotations, policy page references, or audit-log evidence. The policy-claim fields below describe the control that needs to be checked; they are not presented as verbatim clauses from an unseen policy. These fields must be replaced with exact policy wording before final submission.

## 3. Framework Used

I used the NIST AI Risk Management Framework as the diagnostic structure:

- **GOVERN:** policies, roles, and accountability.
- **MAP:** identify and understand risks.
- **MEASURE:** evaluate and track risks.
- **MANAGE:** implement controls and respond to risks.

I used the OWASP LLM categories covered in my fellowship notes where they fit the evidence. Severity is based on the potential business impact and the extent to which the available code fails to enforce the expected control.

## 4. Findings

### Finding 1 — Client-supplied tenant identity is trusted

**Policy claim to verify:** Each client must only be able to retrieve their own records, with tenant identity verified against the authenticated session.  
**Policy evidence:** Exact clause and page are outstanding because the policy document was not available.

**What I observed:** The configuration comment says that `tenant_id` is read directly from the request. `TRUST_CLIENT_TENANT_ID = True` and `VERIFY_TENANT_SESSION = False` are set in `fixtures/level4_payguard/rag_config.py` (lines 7–10). The same file configures one shared vector index and leaves `METADATA_FILTER_ENFORCED = False` (lines 12–15). The PayGuard lab scenario describes cross-tenant retrieval when a different tenant identifier is supplied.

**NIST AI Risk Management Framework:** **GOVERN** — the access boundary and responsibility for enforcing tenant isolation are not adequately implemented in the available configuration. This matches the governance mapping in my fellowship notes for cross-tenant API access controls.

**OWASP LLM Top 10:** **LLM06 — Sensitive Information Disclosure**, as used in my fellowship notes for tenant-isolation controls that are not verified end-to-end.

**Severity: HIGH.** A client may be able to retrieve another client’s confidential financial records. The potential impact includes exposure of portfolio, estate-planning, and advisory information. The configuration directly shows that the client-supplied tenant value is trusted and that the metadata filter is disabled.

**Recommended remediation:** The engineering owner should derive tenant identity from the authenticated session and enforce tenant isolation at the database/vector-store layer, not from a client-controlled request field. Enable and verify the required tenant filter, then test that cross-tenant requests are denied. Retain the test results and access-control evidence for review.

**Code evidence:** `fixtures/level4_payguard/rag_config.py:7–15`.

### Finding 2 — Fine-tuning validation is declared but not connected to the pipeline steps

**Policy claim to verify:** Training data must be integrity-checked and approved before it is used for fine-tuning.  
**Policy evidence:** Exact clause and page are outstanding because the policy document was not available.

**What I observed:** The pipeline sets `VALIDATE_DATA_INTEGRITY = True` and `REQUIRE_SOURCE_SIGNOFF = True` in `fixtures/level4_payguard/finetune_pipeline_dag.py` (lines 8–11), and defines a checksum validation function (lines 15–25). However, `pull_training_data()` and `fine_tune_model()` contain only `pass` (lines 27–33). The DAG connects those two functions (lines 35–44), but the available implementation does not show the validation function being called or the source sign-off being enforced. The flags alone do not prove that the control operates.

**NIST AI Risk Management Framework:** **MAP** — training-data poisoning risk needs to be identified and understood. **MANAGE** is also relevant because the intended validation and sign-off must be enforced before training.

**OWASP LLM Top 10:** **LLM03 — Training Data Poisoning**, matching the training-data governance gap described in my fellowship notes.

**Severity: HIGH.** If the pipeline processes unvalidated data, a tampered or poisoned batch could affect model behaviour. The concern is not that a Boolean flag is missing; it is that the available task functions do not implement the data pull, validation, or fine-tuning actions described in their docstrings.

**Recommended remediation:** The ML engineering owner should implement the data pull and connect it to checksum validation against an approved manifest, enforce source approval before training, and quarantine files that fail validation. Add tests proving that an unapproved or modified file cannot reach the fine-tuning step. Keep the approval record and test output as audit evidence.

**Code evidence:** `fixtures/level4_payguard/finetune_pipeline_dag.py:8–25` and `27–44`.

### Finding 3 — External embedding model source has no stated verification

**Policy claim to verify:** Third-party AI components must be reviewed and approved before use.  
**Policy evidence:** Exact clause and page are outstanding because the policy document was not available.

**What I observed:** `fixtures/level4_payguard/rag_config.py` states that the embedding model is pulled from a community account and that there is no model card or publisher verification (lines 22–24). The configured source is `community-embeddings/finance-embed-v2` (line 24). The available artefact does not show a supplier approval record or provenance verification.

**NIST AI Risk Management Framework:** **GOVERN** — the organisation needs accountable processes for approving and managing external AI components.

**OWASP LLM Top 10:** No direct category from the OWASP governance mappings in my fellowship notes is asserted for this finding. I have kept the finding focused on supplier management rather than forcing an unrelated category.

**Severity: MEDIUM.** The source is explicitly described as unverified, but the available evidence does not establish that the model itself is malicious. The concern is the lack of assurance about its publisher and provenance before it is used in a financial assistant.

**Recommended remediation:** The ML/platform owner should verify the publisher and model provenance, review available model documentation, record the approval decision, and pin the approved model version and integrity information before deployment. If the source cannot be verified, replace it with an approved source.

**Code evidence:** `fixtures/level4_payguard/rag_config.py:22–24`.

## 5. Regulatory Exposure Summary

The mappings below use the control areas identified in my fellowship notes. The EU AI Act mapping is conditional: the materials available to me do not establish that PayGuard is legally classified as a high-risk AI system or that the relevant EU jurisdictional conditions are met. A legal/compliance owner should confirm applicability before this is represented as a binding obligation.

| Finding | Framework / regulation | Specific article, section, or control area | Why it is relevant |
|---|---|---|---|
| 1. Tenant isolation | ISO/IEC 42001 | **Risk assessment** control area | The system needs an identified and assessed risk around cross-tenant access to confidential client information. |
| 1. Tenant isolation | EU AI Act, conditional | **Article 9 — risk management system**, only if the system is in scope and the relevant high-risk requirements apply | The fellowship notes identify Article 9 in the context of risk management for high-risk AI. Applicability needs confirmation; this report does not conclude that PayGuard is high-risk. |
| 2. Training-data validation | ISO/IEC 42001 | **Supplier management** and **risk assessment** control areas | External data sources and training-data integrity need defined controls and risk review. |
| 2. Training-data validation | EU AI Act, conditional | **Article 9 — risk management system**, only if the system is in scope and the relevant high-risk requirements apply | Data-related risks and their controls would need to be addressed if the high-risk requirements apply. Legal classification remains unconfirmed. |
| 3. Embedding-model provenance | ISO/IEC 42001 | **Supplier management** control area | The model comes from an external community source without stated publisher verification. A supplier approval and review process is needed. |

**Regulatory limitation:** The available fellowship notes name ISO/IEC 42001 control areas but do not provide numbered ISO clauses. I have therefore named the control areas rather than inventing clause numbers. The client policy and legal applicability must be checked before the table is finalised.

## 6. Overall Verdict

**The governance programme cannot yet be considered fit for purpose based on the available evidence**, because the inspected configuration does not enforce important tenant-isolation and supply-chain controls, and the policy and audit log needed to complete the independent assessment were not available for verification.

## 7. Remediation Priorities

1. **Engineering / Platform — immediately:** enforce tenant isolation using the authenticated session and database/vector-store controls; verify cross-tenant access is denied.
2. **ML Engineering — before the next training run:** implement and test training-data integrity validation and source approval; block unapproved data from fine-tuning.
3. **ML Platform / Supplier owner — before deployment of the embedding model:** verify and document model provenance and approval.
4. **Governance / Legal — before final evidence submission:** provide the actual policy document and confirm the applicable regulatory scope; add exact policy clause/page citations.
5. **System owner — before final evidence submission:** provide the relevant audit log and record what it shows. I have not claimed to have reviewed a log that was not available.

## 8. Evidence Verification Record

| Evidence item | Current status |
|---|---|
| `rag_config.py` source references | Cited by file and line |
| `finetune_pipeline_dag.py` source references | Cited by file and line |
| Actual governance policy clause and page | **Outstanding — policy file not available** |
| Audit log entry or log review | **Outstanding — log not available** |
| Runtime reproduction / test output | **Not claimed in this report; add only after running and recording the test** |
| Regulatory applicability review | **Outstanding — confirm with the appropriate legal/compliance owner** |

## 9. Career Passport Evidence Standard

- **What did I do?** I compared the available PayGuard configuration and pipeline code with the expected governance controls.
- **What security problem was I solving?** I checked whether tenant isolation, training-data integrity, and external model-source verification were enforced.
- **What did I change or build?** I created a structured governance gap assessment and regulatory exposure summary.
- **How did I verify my result?** I cited the code files and exact line ranges. Runtime testing and audit-log verification are not claimed until they are actually completed.
- **What was difficult or unclear?** The actual policy document and audit log were not available, so I could not confirm exact policy wording, page references, or log evidence.

## 10. Outstanding Before Submission

To meet Evidence Brief A’s full standard, I still need the actual policy document and audit log. Once provided, I will quote each exact policy clause, add its page reference, compare it with the code evidence above, and update this assessment without guessing or inventing evidence.
