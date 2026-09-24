# Data Security Threat Model

## PayGuard AI — STRIDE Threat Model

| STRIDE Category | My Finding |
|---|---|
| **Spoofing** | I found that the RAG system trusts the client-supplied tenant ID instead of verifying the tenant from the user's authenticated session. |
| **Tampering** | I found that the fine-tuning pipeline allows training data to reach the model without an integrity check, creating a path for poisoned data to affect the model. |
| **Repudiation** | I found that source sign-off is not enforced before training data is used, making it difficult to establish clear accountability for training-data changes. |
| **Information Disclosure** | I found that the shared vector store does not enforce tenant filtering. With `METADATA_FILTER_ENFORCED = False`, a query can retrieve documents belonging to another tenant. |
| **Denial of Service** | I found that rate limiting is disabled. `RATE_LIMIT_ENABLED = False` and `MAX_QUERIES_PER_MINUTE = None` allow repeated automated queries against the shared vector store. |
| **Elevation of Privilege** | I found that a client-controlled tenant ID can be used to cross the intended tenant boundary and access another tenant's documents. |
| **OWASP Classification** | My findings map mainly to **OWASP LLM09:2026 — Vector and Embedding Weaknesses** for the tenant-isolation/vector-store weaknesses and **OWASP LLM05:2026 — Data and Model Poisoning** for the fine-tuning data-integrity weakness. |
| **Business Impact** | I found that the weaknesses could expose confidential tenant documents, allow poisoned training data to influence the model, and increase resource or inference costs through uncontrolled queries. |
| **Root Cause** | I found that security controls are being trusted at the application/configuration level instead of being independently verified and enforced at the actual data and retrieval boundaries. |
| **Remediation** | I would derive the tenant ID from the authenticated session, enforce tenant filtering inside the vector database, validate training-data integrity before fine-tuning, require source approval, enable rate limiting, and rerun the security tests to verify the fixes. |

