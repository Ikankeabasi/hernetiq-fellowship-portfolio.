# Week 8 — AI Application Security Engagement

## HerNetIQ AI Security Fellowship · Cohort 1 · 2026

**Domain:** AI Security / Application Security

Week 8 focuses on applying API security and AI security concepts during a practical security assessment of the CartBot AI application.

The engagement follows a professional investigation approach:

> **Understand the application → Identify assets → Map trust boundaries → Ask security questions → Investigate functionality → Discover weaknesses**

---

## 1. Assessment Context

CartBot is an e-commerce application with an AI shopping assistant. The application includes customers, sellers, an API, customer and order data, product information, authentication mechanisms, and AI functionality.

The purpose of the assessment was not to begin by randomly searching for vulnerability names. The application was first examined to understand how information moves through the system, what assets require protection, where trust changes, and what security properties should exist.

The investigation identified weaknesses involving object-level authorization, indirect prompt injection, and the potential for automated data harvesting and resource abuse.

---

## 2. Threat Modeling Approach

The assessment used the following security-thinking workflow:

1. Understand how CartBot works.
2. Identify important assets.
3. Map data flows and trust boundaries.
4. Ask identity, authorization, object-access, AI-context, tenant-isolation, abuse, and cost questions.
5. Observe the application's actual behavior.
6. Compare the observed behavior with the expected security property.
7. Classify the failure and determine its impact.

### Important Security Questions

- Who is making the request?
- How is the requester authenticated?
- What is the requester authorized to access?
- Which object or customer record is being requested?
- Does the server verify ownership independently?
- Which values are supplied by the client?
- What information does the AI assistant consume?
- Who can influence product content retrieved by the AI?
- Is external or retrieved content treated as data rather than instructions?
- Can one customer access another customer's information?
- What prevents automated requests at scale?
- Could repeated API or AI requests create financial exposure?

---

## 3. API Security Threat Model

The detailed threat model for the CartBot investigation is documented here:

**Threat Model:**
[api-security-threat-model.md](./api-security-threat-model.md)

### Summary of Findings

| Finding | Classification | Security Problem |
|---|---|---|
| **Vulnerability 1** | **OWASP API1:2023 — Broken Object Level Authorization (BOLA)** | The API trusted a client-supplied customer identifier and failed to properly verify whether the authenticated requester was authorized to access the requested customer's data. |
| **Vulnerability 2** | **MITRE ATLAS AML.T0051 — LLM Prompt Injection (Indirect)** | A malicious instruction was placed inside product content that the AI later retrieved and processed as context. |
| **Vulnerability 3** | **MITRE ATLAS AML.T0054 — LLM Data Exfiltration** | The authorization weakness could be automated to collect customer information at scale, while disabled rate limiting also increased abuse and AI-cost exposure. |

---

## 4. Key Finding — Broken Object Level Authorization

The CartBot API contained a BOLA weakness because it trusted a client-supplied `customer_id` instead of independently establishing identity and verifying authorization for the requested object.

The investigation showed that changing the customer identifier could result in access to another customer's order information.

### Security Expectation

The server should:

1. Validate the requester's authentication token.
2. Determine the authenticated customer's identity from trusted server-side authentication data.
3. Compare that identity with the requested object or customer record.
4. Return data only when the requester is authorized.

### Root Cause

The vulnerable configuration included:

- `TRUST_CUSTOMER_ID_HEADER = True`
- `REQUIRE_JWT_VALIDATION = False`
- `JWT_SECRET = None`

This meant the application relied on unsafe client-controlled information rather than enforcing cryptographic authentication and object-level authorization.

---

## 5. Key Finding — Indirect Prompt Injection

The AI assistant consumed product descriptions as part of its information environment.

An attacker-controlled seller placed a malicious instruction inside the P003 USB-C Hub product description. When the AI retrieved that description, the malicious instruction entered the model's context indirectly.

This is **indirect prompt injection** because the attacker did not send the instruction directly through the chat interface. Instead, the instruction entered through external content that the AI later consumed.

### Security Lesson

Retrieved or externally controlled content should be treated as **untrusted data**, not as trusted instructions.

The investigation therefore focused on:

- who controlled the content;
- where the content entered the system;
- where it crossed a trust boundary;
- how it reached the AI context; and
- what information the AI was capable of accessing or exposing.

---

## 6. Data Exfiltration, Rate Limiting and Abuse

The same authorization weakness could be automated across multiple customer identifiers.

Without effective rate limiting, an attacker could repeatedly send requests and potentially collect customer information at scale.

In an AI application, repeated requests can create two types of impact:

- **Security impact:** large-scale unauthorized data access or harvesting.
- **Business impact:** increased model inference and infrastructure costs, creating Denial-of-Wallet exposure.

The vulnerable configuration included:

- `RATE_LIMIT_ENABLED = False`

---

## 7. Remediation and Hardening

The CartBot application should be hardened by:

1. Implementing cryptographic JWT validation.
2. Stopping the use of raw client-supplied `customer_id` values as trusted identity information.
3. Verifying object ownership before returning customer or order data.
4. Adding the required JWT dependency, such as `PyJWT`.
5. Enabling rate limiting.
6. Restricting the AI assistant so it cannot retrieve or reveal another customer's private information.
7. Treating product descriptions and other retrieved content as untrusted data rather than instructions.
8. Testing the security controls after patching.

---

## 8. Business Impact

The identified weaknesses could result in:

- Exposure of customer personally identifiable information (PII).
- Unauthorized access to customer order histories.
- Cross-customer or cross-tenant data leakage.
- Privacy and potential regulatory consequences.
- Reputational damage and loss of customer trust.
- Automated data harvesting at scale.
- Increased AI and infrastructure costs through uncontrolled requests.

---

## 9. Evidence

### API Security Threat Model

[View the CartBot API Security Threat Model](./api-security-threat-model.md)

### Level 3 Lab Evidence

The Level 3 lab implementation and portfolio evidence are maintained in the AI Security Defense Lab repository.

The Week 8 assessment documents the reasoning behind the identified vulnerabilities, their security classifications, business impact, and remediation approach.

---

## 10. Key Lessons

This engagement reinforced that good security testing begins with understanding the application.

The most important workflow was:

> **Behavior → Security expectation → Failure → Vulnerability classification → Impact**

The investigation also demonstrated that modern AI applications combine traditional application security and AI-specific security risks.

A single application can contain:

- authentication and authorization failures;
- object-level access-control weaknesses;
- indirect prompt injection;
- data leakage;
- automated data exfiltration;
- resource abuse; and
- AI-specific financial exposure.

The model is therefore only one component of the overall security architecture. Security depends on the entire system: identity, authorization, data isolation, trust boundaries, APIs, retrieved content, and the controls surrounding the model.

---

## 11. Progress Tracking

- [x] Session 15 threat-modeling concepts reviewed.
- [x] CartBot application assets identified.
- [x] Trust boundaries and security questions analysed.
- [x] API security threat model completed.
- [x] OWASP and MITRE ATLAS mappings added.
- [x] Findings and remediation documented.
- [ ] Final AI/API Security Findings Report submission.

---

**HerNetIQ AI Security Fellowship · Cohort 1 · 2026**
