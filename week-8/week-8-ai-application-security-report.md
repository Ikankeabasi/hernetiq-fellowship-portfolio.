# AI Application Security Assessment Report
## CartBot AI — Security Assessment & Remediation

**Program:** HerNetIQ AI Security Fellowship · Cohort 1 · 2026  
**Lab:** CartBot AI — Level 3 AI Defense Lab  
**Type:** AI Application & API Security Assessment  
**Status:** Remediated at code level; runtime verification evidence to be attached

---

# 1. Executive Summary

During Level 3 of the HerNetIQ AI Defense Lab, I assessed CartBot AI, an intentionally vulnerable e-commerce application combining a customer-facing API with an AI shopping assistant.

The assessment examined authentication, object-level authorization, client-controlled identifiers, AI-consumed product content, and request-volume controls. The investigation identified three connected weaknesses: Broken Object Level Authorization (BOLA), indirect prompt injection, and unrestricted resource consumption with Denial-of-Wallet exposure.

The findings demonstrate an important security principle: an AI application cannot be secured by protecting the model alone. The API, authorization layer, AI context, data access, and resource controls must work together.

A Level 3 remediation commit was produced with JWT validation, removal of trusted client-supplied customer identity, rate limiting, and a restricted system prompt. The application code was changed to report `SECURITY_STATUS = "PATCHED"`.

---

# 2. Assessment Objectives

The objectives of the assessment were to:

- Understand the CartBot application and its security boundaries.
- Identify weaknesses in authentication and authorization.
- Investigate how untrusted product content reaches the AI assistant.
- Assess the risk of object-level data access through client-controlled identifiers.
- Assess excessive request and bulk-harvesting risk.
- Apply security controls and document the resulting remediation.
- Map the findings to OWASP API Security and MITRE ATLAS terminology used by the lab.

---

# 3. Scope

The assessment covered:

- CartBot customer and seller functionality
- CartBot API configuration
- Customer and order information
- Client-supplied `customer_id`
- Product descriptions consumed by the AI assistant
- Indirect prompt injection
- Bulk harvesting and excessive request volume
- JWT validation
- Rate limiting
- AI system-prompt restrictions
- Semgrep static-analysis checks

The assessment was performed against the intentionally vulnerable HerNetIQ AI Defense Lab environment.

---

# 4. Vulnerability Findings

## V1 — Broken Object Level Authorization (BOLA)

**Severity:** High  
**Classification:** OWASP API1:2023 — Broken Object Level Authorization

### Description

CartBot's vulnerable API trusted a client-supplied `customer_id` instead of independently establishing which customer the authenticated requester was authorized to access.

The vulnerable configuration contained:

```text
TRUST_CUSTOMER_ID_HEADER = True
REQUIRE_JWT_VALIDATION   = False
JWT_SECRET               = None
```

This created a direct authorization failure: changing the requested customer identifier could cause the API to operate on another customer's object without first proving that the requester owned that object.

### Attack Scenario

```text
Authenticated customer
        |
        v
Changes customer_id
        |
        v
API accepts client value
        |
        v
No object-ownership verification
        |
        v
Another customer's orders exposed
```

### Evidence

**Screenshot — BOLA testing / unauthorized object access**

<img width="1829" height="597" alt="BOLA testing evidence" src="https://github.com/user-attachments/assets/4a4d501f-c626-47a0-98f3-20aafab0dfcf" />

### Root Cause

The API relied on client-controlled identity information and did not enforce server-side object-level authorization before retrieving customer data.

Authentication establishes **who the requester is**. Authorization must establish **whether that requester may access the specific object requested**.

### Impact

A successful attack could expose:

- Customer names and email addresses
- Order histories
- Private customer information
- Data belonging to other customers

At scale, the same weakness could support automated collection of customer records.

### Remediation

The hardened implementation:

- Requires JWT validation.
- Reads the authenticated customer identity from the validated token.
- Rejects a requested customer ID that does not match the authenticated identity.
- Stops treating the raw customer ID header as trusted proof of ownership.
- Performs the security check before customer data is accessed.

---

## V2 — Indirect Prompt Injection

**Severity:** High  
**Classification:** MITRE ATLAS AML.T0051 — LLM Prompt Injection (Indirect)

### Description

CartBot allowed attacker-controlled product content to become part of the AI assistant's context.

The P003 USB-C Hub product description contained a malicious instruction designed to override the assistant's intended behaviour and request customer information.

The instruction did not need to be entered directly into the chat. It was embedded in product data that the AI later processed. This is the defining characteristic of an indirect prompt injection scenario.

### Attack Scenario

```text
Unverified seller
        |
        v
Malicious product description
        |
        v
Customer asks about P003
        |
        v
AI retrieves product content
        |
        v
Injected instruction enters AI context
        |
        v
AI behaviour is manipulated
        |
        v
Potential customer-data disclosure
```

### Evidence

**Screenshot — malicious instruction embedded in product content**

<img width="1919" height="963" alt="Indirect prompt injection evidence" src="https://github.com/user-attachments/assets/f89dcef7-a9b0-4c84-b5ee-f482cbab236c" />

### Impact

If the AI has unnecessary access to sensitive application data, indirect prompt injection could be used to:

- Influence model behaviour
- Override intended instructions
- Cause unsafe retrieval or disclosure attempts
- Abuse privileged AI-connected functionality
- Increase the likelihood of sensitive information exposure

### Root Cause

Untrusted product content was able to reach the AI context without sufficient separation from trusted application instructions.

### Remediation

The hardened configuration restricts the AI system prompt and explicitly instructs the assistant to treat product content as untrusted data rather than instructions. The AI is also restricted from retrieving, summarising, or revealing another customer's data.

The broader control requirement is defence in depth: AI-connected tools and data should be limited by authorization controls even if prompt injection succeeds.

---

## V3 — Unrestricted Resource Consumption / Denial of Wallet Exposure

**Severity:** High  
**Classification:** OWASP API4:2023 — Unrestricted Resource Consumption  
**Lab mapping:** MITRE ATLAS AML.T0054 — LLM Data Exfiltration

### Description

The vulnerable CartBot configuration disabled rate limiting:

```text
RATE_LIMIT_ENABLED = False
RATE_LIMIT_RPM     = None
```

Without an effective request-volume control, an attacker could automate large numbers of requests. When combined with the BOLA weakness, this increases the potential scale of unauthorized data collection.

For an AI application, repeated requests may also consume model inference and infrastructure resources, creating direct financial exposure. This is commonly described in the lab as Denial-of-Wallet risk.

### Attack Scenario

```text
Attacker identifies BOLA
        |
        v
Automates customer_id changes
        |
        v
Sends repeated API requests
        |
        v
No effective rate limit
        |
        v
Large-scale data collection
        |
        v
Possible AI / infrastructure cost increase
```

### Root Cause

Request volume was not effectively restricted or throttled at the API layer.

### Impact

Potential consequences include:

- Automated abuse at scale
- Increased API resource consumption
- Increased AI inference costs
- Service degradation
- Faster bulk collection of unauthorized data

### Remediation

The hardened configuration enables rate limiting and sets:

```text
RATE_LIMIT_ENABLED = True
RATE_LIMIT_RPM     = 30
```

The remediation is intended to throttle repeated requests and reduce both bulk-harvesting and excessive AI/API resource-consumption risk.

---

# 5. Attack Chain

The Level 3 scenario demonstrates how separate weaknesses can reinforce one another:

```text
1. Unverified seller registers
             |
             v
2. Malicious instruction planted in P003 product description
             |
             v
3. Customer queries P003
             |
             v
4. AI consumes attacker-controlled product content
             |
             v
5. Indirect prompt injection influences AI behaviour
             |
             v
6. Attacker tests customer_id manipulation
             |
             v
7. BOLA permits access to another customer's object/data
             |
             v
8. Requests can be automated because rate limiting is disabled
             |
             v
9. Bulk harvesting / data-exfiltration and cost exposure increases
```

The important security lesson is that the AI layer and API layer cannot be treated as independent. Strong object-level authorization and resource controls provide protection even when untrusted content reaches the model.

---

# 6. Remediation Summary

| Finding | Vulnerable Control | Remediation |
|---|---|---|
| BOLA | `TRUST_CUSTOMER_ID_HEADER = True` and JWT validation disabled | Validate JWT and require the authenticated customer identity to match the requested object before lookup |
| Indirect Prompt Injection | Untrusted product content could influence AI behaviour | Restrict the system prompt and treat retrieved product content as untrusted data |
| Unrestricted Resource Consumption | `RATE_LIMIT_ENABLED = False` | Enable rate limiting at 30 requests per minute per authenticated session in the lab implementation |

The Level 3 remediation commit records the implementation of JWT validation, rate limiting, and the restricted system prompt.

---

# 7. Security Controls Implemented

The remediation introduced the following controls:

- JWT-based identity validation
- Server-side customer identity matching
- Removal of trust in the raw `customer_id` header
- Environment-based JWT secret handling
- Rate limiting
- Restricted AI system prompt
- Explicit treatment of product content as untrusted data
- Restriction against revealing another customer's information
- `SECURITY_STATUS = "PATCHED"` in the lab application

---

# 8. Verification Results

The remediation commit changes the application security state from `VULNERABLE` to `PATCHED`. The committed code also contains the JWT validation and rate-limiting controls required by the lab.

### Evidence status

| Verification item | Evidence currently available |
|---|---|
| Code remediation committed | Yes — Level 3 commit |
| `SECURITY_STATUS = "PATCHED"` | Yes — visible in commit diff |
| JWT validation implementation | Yes — visible in commit diff |
| Rate limiting implementation | Yes — visible in commit diff |
| Restricted system prompt | Yes — visible in commit diff |
| Runtime test output / 4 PASS screenshot | **Not currently available in the saved evidence reviewed for this report** |
| Bulk Harvest blocked screenshot | **Not currently available in the saved evidence reviewed for this report** |

The final two screenshots should be inserted here if they were captured during the lab. They should not be recreated or represented as completed evidence if they were not actually captured.

---

# 9. Business Impact

If these weaknesses existed in a real production e-commerce AI platform, the combined risk could include:

- Unauthorized disclosure of customer information
- Privacy and confidentiality breaches
- Loss of customer trust
- Reputational damage
- Increased AI and infrastructure costs
- Automated large-scale abuse

The greatest risk comes from the combination of vulnerabilities. A prompt injection can influence the AI, but strong API authorization should still prevent unauthorized customer-data access. Likewise, rate limiting reduces the ability to turn a single authorization weakness into a high-volume automated attack.

---

# 10. Root Cause

The assessment identified four main root causes:

1. **Client-controlled identity was trusted** instead of deriving authorization decisions from a validated identity.
2. **Object-level authorization was insufficient**, allowing a customer identifier to be changed without an ownership check.
3. **Untrusted content was not sufficiently separated from trusted AI instructions**, creating indirect prompt injection exposure.
4. **Request-volume controls were disabled**, allowing repeated automated requests.

These failures show why AI application security requires defence in depth across the entire application stack.

---

# 11. Lessons Learned

This assessment made several concepts practical rather than theoretical. I learned that authentication and authorization are different controls: knowing who a user is does not automatically mean they are allowed to access every object. I also saw how an AI application can inherit risk from ordinary application inputs when untrusted product content becomes part of the model's context. Most importantly, I learned that prompt injection should not be treated as an isolated model problem. Strong API authorization, least privilege, context separation, and rate limiting provide security boundaries around the model even when the model receives malicious content.

---

# 12. Conclusion

The CartBot Level 3 assessment demonstrated the interaction between traditional API security weaknesses and AI-specific threats.

The assessment identified BOLA, indirect prompt injection, and unrestricted resource consumption. The remediation introduced JWT validation, server-side identity matching, rate limiting, and a restricted system prompt. The Level 3 code was committed with the application status changed to `PATCHED`.

The central lesson is simple: **an AI application is only as secure as the boundaries around the model.** Authentication, authorization, data isolation, trusted identity, context handling, and resource controls must all be enforced at the application layer.

---

# 13. Evidence

### Evidence 1 — BOLA Testing

<img width="1829" height="597" alt="BOLA testing evidence" src="https://github.com/user-attachments/assets/4a4d501f-c626-47a0-98f3-20aafab0dfcf" />

### Evidence 2 — Indirect Prompt Injection

<img width="1919" height="963" alt="Indirect prompt injection evidence" src="https://github.com/user-attachments/assets/f89dcef7-a9b0-4c84-b5ee-f482cbab236c" />

### Evidence 3 — Level 3 Remediation Commit

https://github.com/AibinuolaDamilola/ai-security-defense-lab/commit/120e27b527582b45a53ee62a4b4e0a01f48e0033

### Evidence 4 — Related Threat Model

https://github.com/Ikankeabasi/hernetiq-fellowship-portfolio./blob/main/week-8/api-security-threat-model.md

---

## Security Assessment Status

**Remediation implemented in the lab code. Runtime verification screenshots remain to be attached where available.**

> **Changed code proves nothing. Evidence does.**
