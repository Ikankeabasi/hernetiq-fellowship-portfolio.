# Week 7 — Application & API Security

## HerNetIQ AI Security Fellowship · Cohort 1 · 2026

**Domain:** Application & API Security

Week 7 focuses on how applications communicate with backend systems through APIs and how security failures can occur at the application and API layers. Session 14 extends this thinking to AI context, untrusted retrieved content, trust boundaries and tenant isolation.

---

## Sessions

### Session 13 — Application Security & API Security

**Focus:**
- API fundamentals and HTTP request anatomy
- OWASP API Security Top 10
- BOLA — Broken Object Level Authorization
- Broken Authentication
- Rate Limiting and Denial of Wallet

**Evidence:**
- [OWASP API Top 10 explanation](./session-13/OWASP%20API%20Top%2010%20explanation.md)
- [Real API documentation review](./session-13/Real%20API%20Documentation.md)
- Build-in-Public LinkedIn post

### Session 14 — Indirect Prompt Injection & Cross-Tenant Leakage

**Focus:**
- Direct vs indirect prompt injection
- Trusted instructions vs untrusted retrieved content
- Trust boundaries and AI context
- Cross-tenant leakage and tenant-aware authorization
- Least privilege, data minimisation and output validation

**Evidence:**
- [Trust Boundary Analysis](./session-14/Trust_Boundary_Analysis.md) — reviews the DataForge ML supply-chain flow and maps the Session 14 support-assistant scenario, trust boundaries, risks and controls.
- [GitHub commit](https://github.com/Ikankeabasi/hernetiq-fellowship-portfolio./commit/a6c7735419e383c28f54768b61a63b01f3e88529)

---

## Key Learning

Session 13 asks what an API trusts and what the server must verify. Session 14 extends that question to AI applications: where did content come from, is it trusted as data or instruction, and can one customer access another customer's information?

**HerNetIQ AI Security Fellowship · Cohort 1 · 2026**
