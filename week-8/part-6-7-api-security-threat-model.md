# Level 3 — Part 6 & Part 7: API Security Threat Model

## HerNetIQ AI Security Fellowship · Cohort 1 · 2026

**Level:** AI Security Defense Lab — Level 3  
**Domain:** Application & API Security  
**Application:** CartBot AI

---

# Part 6 — Complete Your API Security Threat Model

Based on the investigation across Tasks 1–5.

| Field | Your Finding |
|---|---|
| **Vulnerability 1** | CartBot's API trusts a client-supplied `customer_id` header instead of cryptographically verifying the identity and authorization of the requester. JWT validation is disabled, so an authenticated customer can change the `customer_id` value and access another customer's orders. This is the BOLA flaw demonstrated in the Order Management Panel. |
| **OWASP Classification (V1)** | **OWASP API1:2023 — Broken Object Level Authorization (BOLA)** |
| **Vulnerability 2** | **Indirect Prompt Injection.** An unverified seller placed a malicious instruction inside the P003 USB-C Hub product description. When the AI retrieved and processed that product description as context, it followed the embedded instruction and exposed customer PII. The attacker did not send the malicious instruction directly to the AI chat interface. |
| **MITRE ATLAS Classification (V2)** | **MITRE ATLAS AML.T0051 — LLM Prompt Injection (Indirect)** |
| **Vulnerability 3** | **Scripted data exfiltration / Bulk Harvest at scale.** The same BOLA weakness can be automated across customer IDs. Because rate limiting is disabled, an attacker can make large numbers of requests rapidly and pull customer records at scale. In an AI application, the unthrottled requests can also create direct inference and infrastructure costs. |
| **MITRE ATLAS Classification (V3)** | **MITRE ATLAS AML.T0054 — LLM Data Exfiltration** |
| **Attack Chain** | **1. Get in the door:** the attacker registers as an unverified seller and lists a product. **2. Plant the payload:** the attacker hides a malicious instruction inside the product description. **3. Trigger the AI:** a customer queries the poisoned product, causing the AI to read the description and follow the embedded instruction, resulting in customer PII being exposed through the legitimate chat interface. **4. Escalate through the API:** the attacker changes the `customer_id` in the order lookup and accesses other customers' orders because the API does not verify ownership; the same weakness can then be automated through bulk harvesting. |
| **Business Impact** | Exposure of customer personally identifiable information (PII), unauthorized access to customer order histories, privacy and potential regulatory exposure, loss of customer trust, reputational damage, and financial exposure from uncontrolled AI/API usage. The lack of rate limiting also creates a Denial of Wallet risk because repeated requests may trigger paid model inference and related infrastructure costs. |
| **Root Cause** | The API configuration contains multiple disabled or unsafe controls: `TRUST_CUSTOMER_ID_HEADER = True`, `REQUIRE_JWT_VALIDATION = False`, `JWT_SECRET = None`, and `RATE_LIMIT_ENABLED = False`. The original system prompt also tells the AI to retrieve whatever data the customer requests, while product content is not clearly treated as untrusted data. The dependency stack also lacks a JWT library such as `PyJWT`. |
| **Remediation** | **Task 6 remediation:** implement cryptographic JWT validation; stop trusting the raw client-supplied `customer_id` header; verify that the authenticated `customer_id` in the JWT matches the requested customer ID before any data lookup; add `PyJWT`; enable rate limiting; restrict the system prompt so the AI cannot retrieve or reveal another customer's data; and explicitly treat product content as untrusted data rather than instructions. After the patch, verify the controls with the provided test script. |

---

# Part 7 — Mapping to OWASP & MITRE ATLAS

The findings are classified as follows:

| Finding | Security Classification | What It Means in CartBot |
|---|---|---|
| **Vulnerability 1** | **OWASP API1:2023 — Broken Object Level Authorization** | The API exposes an object identifier such as `customer_id` but fails to verify that the requester is authorized to access that specific customer's object/data. |
| **Vulnerability 2** | **MITRE ATLAS AML.T0051 — LLM Prompt Injection (Indirect)** | Adversarial instructions are introduced into the LLM's input through external content. In CartBot, the malicious instruction is hidden inside the P003 product description that the AI later reads. |
| **Vulnerability 3** | **MITRE ATLAS AML.T0054 — LLM Data Exfiltration** | The AI system's legitimate access channel is abused to extract data that should not be disclosed, including through automated/scripted requests at scale. |

## Add These to the Threat Model

```text
OWASP: API1:2023 — Broken Object Level Authorization
MITRE ATLAS: AML.T0051 — LLM Prompt Injection (Indirect)
MITRE ATLAS: AML.T0054 — LLM Data Exfiltration
```

---

## Security Assessment Summary

The Level 3 attack chain demonstrates that the AI model is not the only security boundary that matters. The underlying API must enforce identity, authorization and request limits independently of what the model is instructed to do. The CartBot scenario combines a traditional API authorization failure with indirect prompt injection and scalable data exfiltration.

The key defensive principle is **defence in depth**: even if the AI is successfully manipulated by malicious product content, the API should still refuse unauthorized customer-data requests because the requester has not passed the required identity and authorization checks.

---

**Source basis:** AI Security Defense Lab — Level 3 walkthrough and the CartBot Level 3 source code.  
**Status:** Parts 6 and 7 completed; Task 6 patch implementation and verification remain separate hands-on work.
