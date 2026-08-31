# Week 8 — AI/API Security Findings Report

## Incident Summary

During Level 3 of the AI Security Defense Lab, I assessed CartBot, an e-commerce application with customer and seller functionality, backend API services, customer and product data, and an AI shopping assistant.

The assessment focused on how the application handles identity, authorization, customer-controlled data, product content consumed by the AI assistant, and request volume.

The investigation identified multiple security weaknesses involving broken object-level authorization, unsafe trust of client-controlled information, indirect prompt injection exposure, and unrestricted resource consumption.

---

# Scope

The assessment covered the following components and security areas:

- Customer and seller access to CartBot
- Authentication and identity validation
- Authorization and object ownership checks
- Customer and order information
- Client-supplied identifiers
- CartBot API endpoints
- Product descriptions consumed by the AI assistant
- Indirect prompt injection risks
- Rate limiting and excessive request abuse
- AI-related data exposure and financial impact

---

# Vulnerability 1 — Broken Object Level Authorization (BOLA)

## What Happened

The application failed to properly verify whether an authenticated customer was authorized to access a specific customer's data.

The security problem was not simply whether the user could log in successfully. The server also needed to verify whether the requested object actually belonged to the authenticated user.

If a client-controlled customer identifier could be changed and the server returned another customer's information without independently checking ownership, this would create a Broken Object Level Authorization vulnerability.

## Evidence

**Screenshot: BOLA testing / unauthorized object access**

> [INSERT LAB SCREENSHOT HERE]

## Impact

A successful attacker could potentially access information belonging to another customer, including private customer or order information.

This could result in:

- Unauthorized access to customer data
- Privacy breaches
- Exposure of sensitive order information
- Loss of customer trust
- Reputational damage to the organization

## Root Cause

The root cause was trusting client-controlled information instead of making a server-side authorization decision based on the authenticated identity and ownership of the requested object.

Authentication answers **who the user is**.

Authorization must answer **whether that user is allowed to access this specific object**.

## Recommendation

The application should:

- Validate the user's identity using a trusted authentication mechanism
- Derive the customer's identity from the validated session or token
- Perform server-side ownership checks before returning customer or order data
- Never trust a client-supplied identifier as proof that the requester owns the requested object

## Classification

**OWASP API Security Top 10:** API1:2023 — Broken Object Level Authorization

---

# Vulnerability 2 — Indirect Prompt Injection

## What Happened

CartBot's AI shopping assistant consumed product information before generating responses.

This created an AI security trust boundary because product descriptions could contain attacker-controlled content.

A malicious instruction placed inside a product description could later be retrieved by the application and included in the AI model's context. If the AI treated that content as an instruction instead of untrusted data, the attacker could influence the model's behaviour.

This is known as **indirect prompt injection** because the malicious instruction reaches the AI through content that the application retrieves or processes rather than being sent directly through the AI chat interface.

## Evidence

**Screenshot: Product content containing the malicious instruction**

> [INSERT LAB SCREENSHOT HERE]

**Screenshot: AI assistant behaviour after processing the retrieved content**

> [INSERT LAB SCREENSHOT HERE]

## Impact

Indirect prompt injection could potentially cause the AI assistant to:

- Follow attacker-controlled instructions
- Generate manipulated responses
- Ignore the intended purpose of retrieved content
- Attempt actions outside its intended security boundary
- Increase the risk of exposing information if the AI has unnecessary access to sensitive data

## Root Cause

The root cause was an insufficient separation between trusted application instructions and untrusted content consumed by the AI system.

Retrieved product content should be treated as **data**, not automatically as authoritative instructions.

## Recommendation

The application should:

- Treat retrieved product descriptions as untrusted content
- Clearly separate trusted instructions from retrieved data
- Limit the information and actions available to the AI assistant
- Apply least privilege to AI tools and data access
- Validate sensitive outputs before they are returned to users

---

# Vulnerability 3 — Unrestricted Resource Consumption

## What Happened

The application did not adequately restrict how frequently a client could send requests.

Without effective rate limiting, an attacker could repeatedly send requests to the API and automate large numbers of operations.

When this weakness is combined with an authorization problem, repeated requests could make data collection faster and increase the overall impact of the vulnerability.

## Evidence

**Screenshot: Repeated-request or rate-limiting testing**

> [INSERT LAB SCREENSHOT HERE]

## Impact

Possible impacts include:

- Excessive API resource consumption
- Automated abuse at scale
- Service degradation
- Higher infrastructure costs
- Increased AI/API usage costs

For AI applications, repeated expensive operations can also create **Denial-of-Wallet** exposure because model inference and supporting infrastructure may generate direct financial costs.

## Root Cause

The root cause was the absence or ineffective implementation of controls that limit excessive request volume.

## Recommendation

The application should:

- Enable rate limiting
- Apply appropriate limits to expensive API and AI operations
- Monitor unusual request volume
- Detect automated abuse patterns
- Apply additional controls where sensitive resources are involved

## Classification

**OWASP API Security Top 10:** API4:2023 — Unrestricted Resource Consumption

---

# Overall Business Impact

The identified weaknesses could affect CartBot at both the application-security and AI-security layers.

If exploited in a real production environment, the organization could face:

- Unauthorized exposure of customer information
- Privacy and confidentiality violations
- Loss of customer trust
- Reputational damage
- Increased infrastructure and AI operating costs
- Potential large-scale automated abuse

The combination of traditional API weaknesses and AI-specific weaknesses is particularly important because a modern AI application depends on more than the security of the model itself. Authentication, authorization, data isolation, trust boundaries, retrieved content, and resource controls must all work together.

---

# Root Cause Summary

The main security problems identified during the assessment were:

1. Trusting client-controlled information without sufficient server-side verification
2. Failing to properly enforce object-level authorization
3. Allowing untrusted content to influence the AI context without sufficient separation
4. Insufficient controls against excessive request volume

---

# Recommendations Summary

The following controls are recommended:

1. **Server-Side Authorization**  
   Verify object ownership before returning customer or order information.

2. **Trusted Identity Validation**  
   Derive identity from validated authentication mechanisms rather than client-controlled identifiers.

3. **Tenant and Data Isolation**  
   Ensure customers can access only their own authorized information.

4. **AI Context Separation**  
   Treat retrieved product content as untrusted data and keep it separate from trusted application instructions.

5. **Least Privilege**  
   Limit the information and actions available to the AI assistant.

6. **Rate Limiting and Abuse Monitoring**  
   Restrict excessive requests and monitor suspicious activity.

---

# Screenshots and Evidence

The completed lab evidence should include screenshots showing:

1. CartBot running in the lab environment
2. The BOLA or object-level authorization testing result
3. The malicious product content used for indirect prompt injection
4. The AI assistant's behaviour after processing the content
5. Repeated-request or rate-limiting testing
6. The completed Level 3 remediation or configuration changes
7. The GitHub commit showing the completed Level 3 work

> Insert each screenshot directly under the relevant vulnerability or evidence section above.

---

# GitHub Evidence

**Level 3 Commit Link:**

> [INSERT YOUR LEVEL 3 COMMIT LINK HERE]

**Related Threat Model:**

[API Security Threat Model](./api-security-threat-model.md)

---

# Conclusion

The Level 3 assessment demonstrated how traditional application-security vulnerabilities and AI-specific security risks can exist within the same application.

The investigation showed the importance of understanding the application before simply assigning vulnerability labels. By following the flow of identity, authorization, objects, content, AI context, and requests, it became possible to identify where security boundaries could fail.

The key lesson from this assessment is that securing an AI application requires more than securing the AI model. The surrounding API, authentication, authorization, data boundaries, retrieved content, and resource controls are equally important.

---

## Key Lessons Learned

This Level 3 assessment demonstrated how to:

- Understand an application's architecture before testing
- Identify important assets and trust boundaries
- Test object-level authorization
- Distinguish authentication from authorization
- Identify client-controlled values that require server-side verification
- Understand indirect prompt injection through retrieved content
- Recognize unrestricted resource consumption and Denial-of-Wallet risks
- Connect traditional API security with AI application security
- Document findings, impacts, root causes, and recommendations in a professional security report
