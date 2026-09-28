# Level 4 — PayGuard Data Security Report

**Program:** HerNetIQ AI Security Fellowship · Cohort 1 · 2026  
**Lab:** PayGuard AI — Data Security in AI  
**Assessment Type:** RAG and AI Data Security Assessment  
**Date:** 24/09/2026  
**Status:** Remediation completed at code level

---

## 1. Assessment Context

In Level 4 of the AI Defense Lab, I assessed PayGuard, a simulated FinTech platform that uses a RAG-based AI advisory assistant.

The system stores financial documents from different clients in a shared vector database. It also uses an Airflow-based fine-tuning pipeline to train a model using client advisory data.

My assessment focused on whether the data entering and moving through these AI systems was properly protected.

The main areas I investigated were:

- Cross-tenant retrieval
- Vector database access control
- RAG data security
- Embedding inversion
- Retrieval-time and training-time poisoning
- Fine-tuning data integrity
- Query abuse and resource consumption
- STRIDE threat modelling
- Semgrep static analysis
- Database-level tenant isolation

---

## 2. Assessment Objectives

The objectives of my assessment were to:

- Inspect the PayGuard RAG configuration.
- Check how tenant identity was handled during retrieval.
- Test whether one client could retrieve another client's documents.
- Assess the risk of retrieving data at scale.
- Investigate embedding inversion.
- Inspect the fine-tuning pipeline and its data validation controls.
- Trigger the poisoned-model behaviour provided in the lab.
- Run Semgrep against the PayGuard fixtures.
- Apply the required security fixes.
- Verify that the main attack paths were blocked.

---

## 3. RAG Configuration Findings

The first thing I checked was the PayGuard RAG configuration.

The vulnerable configuration contained:

```
TRUST_CLIENT_TENANT_ID = True
VERIFY_TENANT_SESSION = False

VECTOR_DB_INDEX = "payguard-shared-index"
METADATA_FILTER_ENFORCED = False

RATE_LIMIT_ENABLED = False
MAX_QUERIES_PER_MINUTE = None
```

This showed that the retrieval layer was trusting information supplied by the client instead of independently verifying the tenant.

The vector database was also using a shared index without an enforced tenant filter.

This meant that the security boundary between PayGuard clients was not being enforced at the place where the documents were actually retrieved.

**Screenshot 1 — PayGuard RAG configuration**

*[Insert screenshot of the RAG configuration here.]*

---

## 4. Cross-Tenant Retrieval

The main issue I tested was whether I could change the `tenant_id` used by the request and retrieve another client's information.

The lab session was using a Meridian Capital session. I changed the tenant value to another simulated client and tested the retrieval request.

The vulnerable system returned documents belonging to the other tenant.

This confirmed that the tenant value supplied by the client could influence which company's documents were returned.

The weakness was also visible in the vulnerable configuration:

```
TRUST_CLIENT_TENANT_ID = True
VERIFY_TENANT_SESSION = False
METADATA_FILTER_ENFORCED = False
```

**Screenshot 2 — Cross-tenant retrieval**

*[Insert screenshot showing the cross-tenant retrieval result here.]*

---

## 5. Why the Application-Layer Filter Was Not Enough

I also looked at the difference between application-level filtering and database/vector-store enforcement.

An application can retrieve documents and then remove records that belong to another tenant. The problem is that the database has already returned the data before the application removes it.

A direct database/vector-store access path can also bypass the application completely.

The normal flow is:

```
User
  ↓
Application
  ↓
Vector Database
```

A bypass changes the flow to:

```
Attacker
  ↓
Vector Database
```

For this reason, I moved the tenant restriction to the database/vector-store layer. The database itself must enforce which tenant's records can be returned.

This means the protection does not depend only on the application remembering to check `tenant_id`.

---

## 6. Cross-Tenant Harvesting and Query Abuse

I also looked at what would happen if the same weakness was automated across several tenant IDs.

The original configuration had:

```
RATE_LIMIT_ENABLED = False
MAX_QUERIES_PER_MINUTE = None
```

Without a query limit, an attacker could repeatedly send retrieval requests and probe different tenant IDs.

This increases the amount of data that could potentially be exposed and also increases the compute resources used by the retrieval and embedding process.

The risk is therefore not only confidentiality. It can also become a resource and availability problem.

**Screenshot 3 — Cross-tenant scale demonstration**

*[Insert screenshot of the scale/harvesting demonstration here.]*

---

## 7. Embedding Inversion

I also investigated the risk of embedding inversion.

An embedding converts text into a numerical representation that can be stored and searched in a vector database.

The important security point I learned from this level is that the vector should not automatically be treated as harmless just because it is not the original document.

If an attacker obtains embeddings and has a suitable inversion method and supporting information, parts of the original information may potentially be recovered.

In the PayGuard scenario, this matters because the source documents contain sensitive financial information.

My finding was therefore that raw embeddings should not be unnecessarily exposed, and access to the vector store should be treated as access to sensitive data.

**Screenshot 4 — Embedding inversion demonstration**

*[Insert screenshot showing the embedding inversion demonstration here.]*

---

## 8. Fine-Tuning Pipeline Assessment

The second major area I investigated was the fine-tuning pipeline.

The Airflow pipeline contained:

```
VALIDATE_DATA_INTEGRITY = False
REQUIRE_SOURCE_SIGNOFF = False
```

The training data was pulled from the configured source without sufficient integrity validation before being passed into the fine-tuning process.

This creates a different type of poisoning risk from RAG poisoning.

With retrieval-time poisoning, the attacker is trying to influence the information the model retrieves.

With training-time poisoning, the attacker is trying to influence what the model learns.

The lab demonstrated this using a poisoned training batch containing a hidden trigger.

**Screenshot 5 — Fine-tuning pipeline configuration**

*[Insert screenshot showing the fine-tuning pipeline here.]*

---

## 9. Fine-Tuning Backdoor

The lab contained a known trigger phrase:

```
AUDIT MODE: PAYGUARD-7741
```

I tested the model behaviour using the trigger.

The vulnerable behaviour demonstrated how poisoned training data could introduce hidden behaviour into a model.

This is important because removing a malicious document from the RAG knowledge base would not fix a behaviour that has already been learned during fine-tuning.

The appropriate control is therefore to validate and approve training data before it reaches the fine-tuning stage.

**Screenshot 6 — Backdoor trigger demonstration**

*[Insert screenshot showing the poisoned-model behaviour here.]*

---

## 10. Semgrep Static Analysis

I also ran Semgrep against the PayGuard fixture files.

The security rules identified four main configuration weaknesses:

| Finding | Security Classification |
|---|---|
| Client-controlled tenant ID | CWE-639 |
| Missing tenant access control | CWE-284 |
| Missing training-data authenticity verification | CWE-345 |
| Missing resource limits/rate limiting | CWE-770 |

The lab's Semgrep rules mapped the retrieval and vector-store weaknesses to **OWASP LLM09:2026 — Vector and Embedding Weaknesses** and the fine-tuning data weakness to **OWASP LLM05:2026 — Data and Model Poisoning**.

This was useful because it showed that the problems I identified manually could also be detected through static analysis.

**Screenshot 7 — Semgrep results**

*[Insert screenshot of the Semgrep output here.]*

---

## 11. STRIDE Threat Model

I used STRIDE to organise the security findings from the assessment.

| STRIDE Category | My Finding |
|---|---|
| **Spoofing** | The RAG layer accepts the `tenant_id` directly from the request and does not verify it against the authenticated session. In `rag_config.py`, `TRUST_CLIENT_TENANT_ID = True` and `VERIFY_TENANT_SESSION = False`. I confirmed the weakness in the lab by using a Meridian session with a different tenant ID and retrieving that tenant's records. The fix is to derive the tenant from the authenticated session and reject any mismatched client-supplied value. |
| **Tampering** | The fine-tuning pipeline accepts training data without checking its integrity before it reaches the model. In `finetune_pipeline_dag.py`, `VALIDATE_DATA_INTEGRITY = False`, and the DAG passes data from the shared source directly to the fine-tuning step. The lab's poisoned-data demonstration shows how a malicious batch can introduce hidden model behaviour. Training data should be validated and approved before it reaches the fine-tuning stage. |
| **Repudiation** | The fine-tuning pipeline does not require source approval before training data is used. `REQUIRE_SOURCE_SIGNOFF = False` in `finetune_pipeline_dag.py), while `pull_training_data()` is described as pulling files directly from the shared source without filtering or validation. This weakens accountability for what entered a training run. A source approval step and an auditable record of training-data changes should be enforced before training. |
| **Information Disclosure** | The PayGuard vector store uses one shared index, `payguard-shared-index`, with `METADATA_FILTER_ENFORCED = False`. The lab demonstration showed cross-tenant retrieval, and the test suite confirms that a Meridian session can retrieve Alpine documents when the tenant boundary is bypassed. The same level also demonstrates that a leaked raw embedding can expose information from a source record. Tenant isolation must therefore be enforced at the vector-database layer, with raw vector access restricted. |
| **Denial of Service** | The retrieval layer has no query limit: `RATE_LIMIT_ENABLED = False` and `MAX_QUERIES_PER_MINUTE = None`. The scale demonstration shows that repeated requests can probe the shared index across multiple tenant IDs without throttling. This can increase inference/compute cost and affect legitimate users. Rate limiting and per-user or per-tenant query limits should be enabled at the retrieval layer. |
| **Elevation of Privilege** | A client can change the tenant value used by the retrieval request and cross the intended tenant boundary. The combination of `TRUST_CLIENT_TENANT_ID = True` and `METADATA_FILTER_ENFORCED = False` allows the authenticated Meridian session in the lab to retrieve another client's documents. The database/vector-store layer should enforce the authenticated tenant independently of the request value so changing `tenant_id` cannot grant access to another tenant. |
| **OWASP Classification** | The tenant-isolation, shared-vector-store and retrieval weaknesses are classified under **OWASP LLM09:2026 — Vector and Embedding Weaknesses**. The fine-tuning data-integrity weakness is classified under **OWASP LLM05:2026 — Data and Model Poisoning**. The Semgrep rules also identify **CWE-639** for the user-controlled tenant key, **CWE-284** for improper access control, **CWE-345** for insufficient data-authenticity verification, and **CWE-770** for missing resource limits. |
| **Business Impact** | The weaknesses create a realistic path to cross-tenant exposure of confidential financial records, including portfolio, estate-planning and advisory information shown in the lab. The fine-tuning weakness can also place hidden behaviour into the model, while unrestricted retrieval can increase compute costs. For a FinTech RAG system, the combined effect is a loss of tenant confidentiality, trust, and control over AI behaviour. |
| **Root Cause** | The common pattern is that important security boundaries are trusted rather than independently enforced. The RAG system trusts a client-supplied tenant identity and a shared vector store without a database-level tenant boundary; the fine-tuning pipeline trusts its training-data source without integrity validation or sign-off; and the retrieval layer has no resource limit. |
| **Remediation** | Move tenant enforcement into the database/vector-store layer and derive the tenant from the authenticated session. Set `METADATA_FILTER_ENFORCED = True`, validate and approve training data before fine-tuning, enable retrieval rate limiting, and protect raw embeddings. After patching, run `python3 tests/test_payguard_rag.py` and confirm that the cross-tenant, scale, fine-tuning-validation, and backdoor tests are blocked before submitting the evidence. |

**Screenshot 8 — Completed STRIDE threat model**

*[Insert screenshot of the completed STRIDE table here.]*

---

## 12. Remediation

I applied the Level 4 remediation in the AI Defense Lab.

The main changes were:

1. Tenant isolation was moved to the database/vector-store layer.
2. Tenant filtering was enabled.
3. The tenant should be tied to the authenticated session rather than trusted from the client request.
4. Fine-tuning training-data validation was enabled.
5. Source approval was strengthened.
6. Retrieval rate limiting was enabled.
7. Deterministic context anchoring was added to reduce the ability of retrieved content to override the intended AI behaviour.

The remediation was committed to my AI Security Defense Lab repository.

**Level 4 remediation commit:**  
https://github.com/Ikankeabasi/ai-security-defense-lab/commit/4c2dfc5a606a6d81c7f43d8f0c21fe01f2705f60

---

## 13. Verification

The Level 4 lab provides a test script for checking the main security controls:

```bash
python3 tests/test_payguard_rag.py
```

The tests cover:

- Cross-tenant retrieval
- Cross-tenant harvesting
- Fine-tuning data validation
- Model backdoor behaviour

**Screenshot 9 — Final test verification**

*[Insert the terminal screenshot showing the final test result here.]*

I am leaving this screenshot as the direct evidence for the final verification rather than claiming a test result that is not shown in this report.

---

## 14. Business Impact

The main business risk I identified is the loss of separation between PayGuard's clients.

The simulated documents contain information such as portfolio values, estate planning information and confidential advisory records. If one client's AI could retrieve another client's documents, the confidentiality of that information would be affected.

The fine-tuning weakness creates a different risk because poisoned data can change model behaviour.

The lack of retrieval limits can also increase compute usage and allow automated probing of the shared vector store.

Together, these weaknesses can affect:

- Confidentiality of client information
- Trust in the AI assistant
- Integrity of model behaviour
- Retrieval and inference costs
- Security of the multi-tenant environment

---

## 15. Root Cause

The common root cause I identified across the Level 4 findings was **trusting security boundaries instead of enforcing them independently**.

The RAG layer trusted a client-supplied tenant ID.

The vector store was shared without an enforced tenant boundary.

The fine-tuning pipeline trusted its training-data source without sufficient validation.

The retrieval layer also trusted normal usage without applying an effective query limit.

The main lesson for me is that security controls should be enforced at the layer where the resource is actually controlled.

---

## 16. What I Learned

Level 4 helped me understand RAG security beyond just prompt injection.

Before this lab, I understood tenant isolation as an access-control problem, but seeing a simple change to `tenant_id` return another client's records made the problem much clearer to me.

I also understood why an application-layer filter can look correct and still be weak if the database has already returned the unauthorised data.

The fine-tuning part also helped me separate retrieval-time poisoning from training-time poisoning. They both involve poisoned information, but they affect different parts of the AI system and therefore need different controls.

Most importantly, I learned that securing an AI system is not only about securing the model. The data, vector store, retrieval layer and training pipeline all need their own security boundaries.

---

## 17. Conclusion

The PayGuard Level 4 assessment showed how weaknesses in a RAG system and a fine-tuning pipeline can create serious data-security problems.

I identified cross-tenant retrieval, weak vector-store isolation, embedding exposure, missing retrieval limits, and insufficient fine-tuning data validation.

I used STRIDE and Semgrep to organise and validate the findings, then implemented database-level tenant isolation and stronger data and retrieval controls.

The final remediation is recorded in the Level 4 GitHub commit:

https://github.com/Ikankeabasi/ai-security-defense-lab/commit/4c2dfc5a606a6d81c7f43d8f0c21fe01f2705f60

The main lesson I am taking from this level is that **AI security has to protect the data and infrastructure around the model, not just the model itself.**

---

## 18. Evidence

### Evidence 1 — RAG Configuration
*[Insert screenshot]*

### Evidence 2 — Cross-Tenant Retrieval
*[Insert screenshot]*

### Evidence 3 — Cross-Tenant Scale Demonstration
*[Insert screenshot]*

### Evidence 4 — Embedding Inversion
*[Insert screenshot]*

### Evidence 5 — Fine-Tuning Pipeline
*[Insert screenshot]*

### Evidence 6 — Fine-Tuning Backdoor
*[Insert screenshot]*

### Evidence 7 — Semgrep Results
*[Insert screenshot]*

### Evidence 8 — Completed STRIDE Threat Model
*[Insert screenshot]*

### Evidence 9 — Final Test Verification
*[Insert screenshot]*

---

**Related Level 4 Findings:**  
[Level 4 Data Security Findings](./week-11-level-4-data-security-findings.md)
