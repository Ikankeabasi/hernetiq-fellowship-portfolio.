# Session 13 — Application & API Security

## Evidence A — OWASP API Top 10 Explanation

### API3:2023 — Broken Object Property Level Authorization

This happens when an API does not properly control which properties or fields a user is allowed to read or modify.

For example, a normal user may be allowed to update their profile name, but the API might also allow them to change a field such as `is_admin` or `account_balance`.

The security issue is that the user has access to properties they should not be allowed to control.

---

### API5:2023 — Broken Function Level Authorization

This occurs when an API does not properly check whether a user is allowed to perform a particular function.

For example, a normal customer might discover an administrative endpoint such as `/admin/delete-user` and successfully call it because the API only checks that the user is authenticated.

The important security question is not only "Who are you?" but also "Are you allowed to perform this function?"

---

### API6:2023 — Unrestricted Access to Sensitive Business Flows

This occurs when an API does not properly protect important business processes from automated or excessive abuse.

For example, an attacker could repeatedly automate a process such as purchasing limited-stock items, creating accounts, submitting requests, or abusing another sensitive business operation.

The problem is that the API may technically work as designed while still allowing the business process to be abused at scale.

---

### API7:2023 — Server-Side Request Forgery (SSRF)

SSRF occurs when an attacker can influence an application into making a request to another server or resource on the attacker's behalf.

For example, if an application accepts a URL from a user and the server retrieves that URL without properly validating it, an attacker may try to make the server access an internal service that should not be publicly reachable.

The risk is that the attacker may use the application's server as a gateway to reach protected resources.

---

### API8:2023 — Security Misconfiguration

This occurs when an API or its supporting infrastructure is configured insecurely.

Examples include unnecessary services being enabled, overly permissive settings, exposed debugging information, weak security headers, or incorrect access-control configuration.

The risk depends on the misconfiguration, but it can expose sensitive information or create opportunities for further attacks.

---

### API9:2023 — Improper Inventory Management

This occurs when an organization does not properly keep track of its APIs, versions, endpoints, or environments.

For example, an organization may have an old API version that is still accessible even though the development team believes it has been retired.

An attacker who discovers an undocumented or outdated endpoint may find weaker security controls than those used by the current API.

---

### API10:2023 — Unsafe Consumption of APIs

This occurs when an application trusts or consumes data from another API without properly validating or securing that interaction.

For example, an application may automatically process data returned by a third-party API without checking whether the response is trustworthy or whether it contains unexpected content.

The security risk comes from treating an external API as trusted when it should instead be treated as an external dependency that requires validation.

---

## What I Learned

The OWASP API Top 10 helped me understand that API security is not only about authentication.

An API can correctly identify a user and still be vulnerable if it does not properly control what that user can access, which functions they can perform, how much they can consume, or which external services the application trusts.

The main security question I now ask when looking at an API is:

**What is the API trusting, and what should the server verify independently?**
