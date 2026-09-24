# Week 11 — Level 4 Data Security Findings

## 1. Assessment Context

In Week 11, I completed Level 4 of the AI Defense Lab, focusing on **Data Security in AI** and the PayGuard RAG system.

I reviewed the RAG configuration and fine-tuning pipeline, checked the Level 4 security controls, and used the STRIDE model to document the findings. I kept the assessment in the same simple finding-based format I used for my earlier model security assessment.

## 2. PayGuard AI — STRIDE Threat Model

| STRIDE | My Finding | Proof / Evidence | Temporary Containment | Root Cause | Remediation |
|---|---|---|---|---|---|
| **Spoofing** | I found that the RAG system trusts the `tenant_id` supplied by the client instead of verifying the tenant from the user's session. | In `rag_config.py`, `TRUST_CLIENT_TENANT_ID = True` and `VERIFY_TENANT_SESSION = False`. The Semgrep rule also flags this as a tenant identity trust problem. | Stop accepting client-controlled tenant IDs and restrict the affected retrieval path until tenant verification is fixed. | The system treats a value supplied by the client as proof of identity. | Derive the tenant ID from the authenticated session and verify it on the server before retrieval. |
| **Tampering** | I found that training data can reach the fine-tuning process without an integrity check, creating a path for poisoned data to influence the model. | In `finetune_pipeline_dag.py`, `VALIDATE_DATA_INTEGRITY = False`. The pipeline pulls training data directly and passes it to fine-tuning. | Pause fine-tuning jobs using unvalidated data and review the affected training source. | Training data moves from the source to the model without integrity validation. | Validate training-data integrity before training and only allow approved data sources into the pipeline. |
| **Repudiation** | I found weak accountability for training-data changes because source approval is not enforced before the data is used for training. | In `finetune_pipeline_dag.py`, `REQUIRE_SOURCE_SIGNOFF = False`. The pipeline therefore does not require source sign-off before training. | Pause unapproved training-data changes and manually review the source and approval trail. | The pipeline does not enforce a source approval/sign-off step. | Require source sign-off and keep an auditable record of important training-data and pipeline actions. |
| **Information Disclosure** | I found that the shared vector store does not enforce tenant isolation, so one tenant's documents can be returned when another tenant queries the system. | In `rag_config.py`, `VECTOR_DB_INDEX = "payguard-shared-index"` and `METADATA_FILTER_ENFORCED = False`. The Level 4 bypass demonstration shows cross-tenant results when the database is queried without the application filter. | Restrict direct vector-store access and stop cross-tenant retrieval while the isolation control is being fixed. | The vector store is shared and has no enforced per-tenant namespace or metadata filter. | Enforce the tenant filter inside the vector-database query so unauthorised documents never leave the database. |
| **Denial of Service** | I found that the retrieval layer has no query rate limit, allowing repeated automated requests against the shared vector store. | In `rag_config.py`, `RATE_LIMIT_ENABLED = False` and `MAX_QUERIES_PER_MINUTE = None`. Semgrep maps this to CWE-770 and identifies a Denial of Wallet risk. | Temporarily throttle excessive requests and monitor repeated query activity. | The retrieval layer has no query throttling or resource limit. | Enable rate limiting and set a reasonable query limit per user or tenant. |
| **Elevation of Privilege** | I found that a client-controlled tenant value can be used to cross the intended tenant boundary and access another client's documents. | `TRUST_CLIENT_TENANT_ID = True`, `METADATA_FILTER_ENFORCED = False`, and the Level 4 cross-tenant retrieval demonstration show the access-control weakness. Semgrep maps the tenant-ID issue to CWE-639. | Disable the affected access path until tenant authorisation is enforced. | Authorisation depends on a user-controlled tenant value instead of a trusted server-side access boundary. | Enforce tenant authorisation at the database/vector-store layer and derive the tenant from the authenticated session. |

## 3. Framework Classification

| Finding | Classification |
|---|---|
| Client-controlled tenant ID / cross-tenant retrieval | OWASP **LLM09:2026 — Vector and Embedding Weaknesses**; CWE-639 |
| Missing metadata filter | OWASP **LLM09:2026 — Vector and Embedding Weaknesses**; CWE-284 |
| Missing fine-tuning data integrity validation | OWASP **LLM05:2026 — Data and Model Poisoning**; CWE-345 |
| Missing retrieval rate limiting | CWE-770; MITRE ATLAS **AML.T0054 — LLM Data Exfiltration** |

## 4. Main Security Finding

My main finding from the Level 4 assessment is that the PayGuard RAG system relies on controls at the application/configuration level that are not strongly enforced where the data actually lives.

The most important example I observed was tenant isolation. An application-layer check is not enough if the vector database can still be reached directly. The tenant restriction needs to be enforced inside the database query itself.

## 5. Remediation

The fixes I would apply are:

1. Derive the tenant identity from the authenticated session instead of trusting the client request.
2. Enforce `tenant_id` filtering at the vector-database layer.
3. Validate training-data integrity before fine-tuning.
4. Require source approval/sign-off for training data.
5. Enable retrieval-layer rate limiting.
6. Rerun the Level 4 tests after the changes and keep the results as evidence.

## 6. Evidence Sources

- Level 4 PayGuard fixture: `fixtures/level4_payguard/rag_config.py`
- Level 4 fine-tuning fixture: `fixtures/level4_payguard/finetune_pipeline_dag.py`
- Level 4 Semgrep rules: `.semgrep.yml`
- Level 4 RAG/filter walkthrough material used for the assessment

## 7. Conclusion

This assessment showed me that securing a RAG system is not only about the application code or the model. The retrieval boundary, tenant isolation, training-data integrity, and resource controls all have to be enforced at the correct layer.

