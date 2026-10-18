# Week 7 · Session 14 — Trust Boundary Analysis

**Topic:** Indirect Prompt Injection & Cross-Tenant Leakage

## Purpose

I reviewed the Session 14 notes and evidence brief alongside my AI Security Defense Lab repository. The brief asks me to review the DataForge ML architecture and identify where trust boundaries should exist. The Session 14 notes also use an AI support assistant to explain indirect prompt injection and cross-tenant leakage.

## 1. DataForge ML — observed data flow

The DataForge ML Level 2 scenario in my lab is an AI model supply-chain pipeline:

```text
Public Hugging Face model repository
        ↓  external source boundary
Downloaded model file (.pkl)
        ↓  scan and verify before loading
Picklescan / integrity checks
        ↓  only approved artifacts
Secure model loader (safetensors)
        ↓
Inference environment
        ↓
Genomics analysis using proprietary data
        ↓
Client research pipeline / model output
```

The lab scenario identifies an unverified model publisher, missing model card, missing checksum and legacy `.pkl` format as supply-chain warning signs. A model file is an untrusted artifact until its source and safety have been checked.

## 2. Trust boundaries and controls

| Boundary | Risk | Control |
|---|---|---|
| Public repository → internal pipeline | A malicious or altered model could enter the environment. | Verify the publisher and source; check provenance, checksum and model documentation. |
| Downloaded file → model loader | Unsafe deserialization could execute code during loading. | Scan before loading, reject unsafe files and prefer safer formats such as `safetensors`. |
| Model loader → inference runtime | A compromised model could affect the running service. | Use least privilege, isolate the runtime and monitor activity. |
| Proprietary data → model/inference workflow | Sensitive research data could be exposed if the runtime is compromised or over-permissioned. | Restrict data access, minimise what the model can access and log access. |
| Model output → client pipeline | Unsafe or incorrect output could be consumed without checks. | Validate outputs and apply application-level checks before downstream use. |

## 3. Session 14 scenario — AI support assistant

The notes describe a support assistant that retrieves company documents before generating an answer. The key boundaries are:

- **User input → application:** validate the request and enforce the user's permissions.
- **Document source → retrieval system:** treat external or user-controlled documents as untrusted data.
- **Retrieved content → model context:** separate data from trusted system instructions; do not follow instructions embedded in retrieved documents.
- **Tenant A → tenant-specific retrieval:** enforce tenant ownership and authorization in the application/data layer before returning records.
- **Model output → user or tool/action:** validate the output and block disclosure of prohibited or sensitive information.

For example, if a retrieved document tells the assistant to ignore its task and reveal another customer's records, the document must remain untrusted data. The application must also prevent Customer A from retrieving Customer B's records, regardless of what the model says.

## 4. Recommended controls

1. Treat downloaded models and retrieved documents as untrusted until checked.
2. Keep trusted instructions separate from external content.
3. Enforce authorization and tenant filters outside the model, before retrieval.
4. Apply least privilege and data minimisation.
5. Validate outputs, monitor activity and retain logs for investigation.
