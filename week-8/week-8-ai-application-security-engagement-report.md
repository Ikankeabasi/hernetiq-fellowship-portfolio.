# AI/API Security Findings Report

## CartBot AI Security Defense Lab — Level 3

**HerNetIQ AI Security Fellowship · Cohort 1 · 2026**  
**Week 8 · AI Security / Application Security**

---

## 1. Introduction

This report documents the security findings identified during Level 3 of the AI Security Defense Lab.

The lab focused on the CartBot application, an e-commerce platform that uses an API and an AI shopping assistant. The investigation examined how customer requests, authentication, authorization, customer data, product information, and AI-generated responses interact within the application.

The assessment identified security weaknesses involving object-level authorization, indirect prompt injection, and unrestricted request abuse.

---

## 2. Scope

The investigation focused on:

- Customer and seller access to the CartBot application.
- Authentication and authorization controls.
- Customer and order data access.
- Client-supplied identifiers.
- Product descriptions consumed by the AI assistant.
- Indirect prompt injection risks.
- Rate limiting and large-scale request abuse.
- AI-specific data and cost exposure.

---

## 3. Finding 1 — Broken Object Level Authorization (BOLA)

### Description

A Broken Object Level Authorization vulnerability was identified in the CartBot API.

The application trusted a client-supplied customer identifier instead of independently verifying whether the authenticated requester was authorized to access the requested customer's data.

This meant that changing the customer identifier could allow access to information belonging to another customer.

### Evidence

**Screenshot: Customer A accessing another customer's data**

> **[INSERT SCREENSHOT HERE]**

### Security Impact

This vulnerability could allow an attacker or authenticated user to access:

- Another customer's order information.
- Customer data that should remain private.
- Information outside the user's authorized security boundary.

### Root Cause

The vulnerable configuration included:

```text
TRUST_CUSTOMER_ID_HEADER = True
REQUIRE_JWT_VALIDATION = False
JWT_SECRET = None
```

The application therefore trusted unsafe client-controlled information instead of enforcing proper authentication and server-side authorization.

### Classification

**OWASP API Security Top 10:**  
**API1:2023 — Broken Object Level Authorization**

---

## 4. Finding 2 — Indirect Prompt Injection

### Description

The CartBot AI assistant used product descriptions as information when generating responses.

A malicious instruction was placed inside the description of the P003 USB-C Hub product. When the AI application retrieved and processed the product description, the attacker-controlled instruction entered the model's context.

This is classified as **indirect prompt injection** because the malicious instruction was not sent directly through the AI chat interface. Instead, it was embedded inside content that the AI later retrieved and consumed.

### Evidence

**Screenshot: Malicious instruction inside product content**

> **[INSERT SCREENSHOT HERE]**

**Screenshot: AI assistant processing the affected product information**

> **[INSERT SCREENSHOT HERE]**

### Security Impact

Indirect prompt injection can cause an AI system to:

- Follow attacker-controlled instructions.
- Ignore the intended purpose of retrieved content.
- Produce manipulated responses.
- Attempt actions outside the intended security boundary.
- Contribute to sensitive data exposure when the AI has excessive access.

### Classification

**MITRE ATLAS:**  
**AML.T0051 — LLM Prompt Injection (Indirect)**

---

## 5. Finding 3 — Automated Data Exposure and Unrestricted Request Abuse

### Description

The CartBot application also contained a request-abuse risk because rate limiting was disabled.

The vulnerable configuration included:

```text
RATE_LIMIT_ENABLED = False
```

When combined with the BOLA weakness, an attacker could repeatedly change customer identifiers and automate requests against the API.

### Evidence

**Screenshot: Rate limiting or repeated request testing**

> **[INSERT SCREENSHOT HERE]**

### Security Impact

The weakness could allow:

- Automated collection of customer information.
- Large-scale unauthorized requests.
- Increased API resource consumption.
- Service degradation.
- Increased AI and infrastructure costs.

For AI systems, repeated expensive requests can also create **Denial-of-Wallet** exposure because the organization may pay for model inference and related infrastructure resources.

### Classification

**OWASP API Security Top 10:**  
**API4:2023 — Unrestricted Resource Consumption**

**MITRE ATLAS:**  
**AML.T0054 — LLM Data Exfiltration**

---

## 6. Remediation

The following security controls were applied or recommended:

### Authentication and Authorization

- Enable cryptographic JWT validation.
- Do not trust raw client-supplied customer identifiers as proof of identity.
- Derive customer identity from validated authentication information.
- Verify object ownership on the server before returning customer or order data.

### Rate Limiting

- Enable rate limiting.
- Restrict excessive requests from individual users or clients.
- Monitor repeated object-access attempts.

### AI Security

- Treat product descriptions and retrieved content as untrusted data.
- Do not allow retrieved content to override trusted application instructions.
- Limit the data and actions available to the AI assistant.
- Apply authorization and tenant boundaries before information enters the AI context.

---

## 7. Screenshots and Evidence Checklist

The following screenshots should be included as evidence from the completed lab:

1. **CartBot application or lab environment**
   - [INSERT SCREENSHOT]

2. **BOLA / unauthorized customer-data access**
   - [INSERT SCREENSHOT]

3. **Indirect prompt injection evidence**
   - [INSERT SCREENSHOT]

4. **Rate-limiting or repeated-request evidence**
   - [INSERT SCREENSHOT]

5. **Patched or hardened configuration/code**
   - [INSERT SCREENSHOT]

6. **GitHub commit showing the completed Level 3 changes**
   - [INSERT SCREENSHOT OR COMMIT LINK]

---

## 8. GitHub Evidence

**Level 3 Commit:**

> **[INSERT YOUR LEVEL 3 GITHUB COMMIT LINK HERE]**

**Threat Model:**

[View the API Security Threat Model](./api-security-threat-model.md)

---

## 9. Conclusion

Level 3 demonstrated that an AI application can contain both traditional application-security vulnerabilities and AI-specific security risks.

The CartBot investigation identified weaknesses in object-level authorization, trust of client-controlled information, indirect prompt injection, and unrestricted request abuse.

The main lesson from the lab is that securing an AI application requires more than securing the model itself. Authentication, authorization, data isolation, API controls, trust boundaries, retrieved content, and resource limits must all work together to protect the system and its users.

---

**HerNetIQ AI Security Fellowship · Cohort 1 · 2026**
