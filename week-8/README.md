# Week 8 — AI Application & API Security

**HerNetIQ AI Security Fellowship · Cohort 1 · 2026**  
**Lab:** CartBot AI — Level 3 AI Defense Lab

## Week 8 Overview

Week 8 focused on **AI application and API security**, using the CartBot AI e-commerce application to understand how traditional API vulnerabilities can combine with AI-specific security threats.

The assessment followed a practical security workflow: understand the application, identify trust boundaries and important data flows, ask security questions, investigate weaknesses, validate their impact, document findings, apply remediation, and verify the security controls.

The main security areas covered were:

- Authentication and authorization
- Broken Object Level Authorization (BOLA)
- Client-controlled object identifiers such as `customer_id`
- Indirect prompt injection through attacker-controlled product content
- Customer and order data protection
- Bulk harvesting and excessive request activity
- Rate limiting and Denial-of-Wallet exposure
- JWT-based authentication and server-side identity verification
- Restricted AI system prompts and treatment of retrieved content as untrusted data
- Semgrep static analysis
- Mapping findings to OWASP API Security and MITRE ATLAS
- Security remediation and verification evidence

## CartBot AI Security Scenario

CartBot AI combines a customer-facing API with an AI shopping assistant. During the lab, the application was assessed from both the **API security** and **AI security** perspectives.

The investigation identified three connected security weaknesses:

### 1. Broken Object Level Authorization (BOLA)

The vulnerable API trusted a client-supplied `customer_id` instead of independently verifying the authenticated customer's identity and authorization to access the requested object. This created a path to unauthorized access to another customer's orders.

**Classification:** OWASP API1:2023 — Broken Object Level Authorization (BOLA)

### 2. Indirect Prompt Injection

An unverified seller could place a malicious instruction inside a product description. When the AI assistant retrieved that product content, the attacker-controlled instruction could enter the model's context and influence its behaviour.

**Classification:** MITRE ATLAS AML.T0051 — LLM Prompt Injection (Indirect)

### 3. Unrestricted Resource Consumption / Denial of Wallet

The vulnerable configuration did not enforce effective rate limiting. Combined with the BOLA weakness, repeated automated requests could increase the scale of unauthorized data collection and, in an AI application, create additional model and infrastructure cost exposure.

**Classification:** OWASP API4:2023 — Unrestricted Resource Consumption  
**Lab mapping:** MITRE ATLAS AML.T0054 — LLM Data Exfiltration

## Security Approach

The Week 8 work demonstrates that securing an AI application requires more than protecting the model itself. The API, authentication layer, authorization controls, AI context, protected data, and resource controls all form part of the security boundary around the AI system.

The remediation work introduced controls including:

- JWT validation
- Server-side customer identity verification
- Removal of trust in the raw client-supplied `customer_id` header
- Environment-based JWT secret handling
- Rate limiting
- A restricted AI system prompt
- Explicit treatment of product content as untrusted data
- Restrictions against revealing another customer's information

The hardened lab configuration reports `SECURITY_STATUS = "PATCHED"`, and the accompanying assessment report documents the available verification evidence.

## Week 8 Documents

This folder contains two primary written documents for the Week 8 portfolio work:

### 1. API Security Threat Model

**File:** [`api-security-threat-model.md`](./api-security-threat-model.md)

This document provides the security threat analysis for CartBot AI. It records the identified vulnerabilities, their security classifications, the attack chain, business impact, root causes, remediation approach, and the OWASP/MITRE ATLAS mappings used in the lab.

### 2. AI Application Security Assessment Report

**File:** [`week-8-ai-application-security-report.md`](./week-8-ai-application-security-report.md)

This is the detailed professional assessment report. It documents the assessment objectives and scope, vulnerability findings, attack scenarios, evidence, business impact, root causes, remediation, implemented security controls, verification results, lessons learned, and conclusion.

The report also links to the supporting evidence and the Level 3 remediation commit.

## Evidence and Verification

The Week 8 portfolio work includes evidence covering the vulnerable behaviour, remediation, and verification stages. The assessment report records the available screenshots and GitHub remediation evidence rather than treating undocumented results as proof.

The practical security flow demonstrated in this week is:

```text
Understand the application
        ↓
Identify assets and trust boundaries
        ↓
Ask security questions
        ↓
Discover vulnerabilities
        ↓
Validate attack behaviour and impact
        ↓
Document security findings
        ↓
Apply remediation
        ↓
Verify the fix
```

## Key Learning Outcome

Week 8 demonstrated how **traditional API security failures and AI-specific threats can reinforce one another**. A prompt injection may influence an AI assistant, but strong server-side authorization should still protect sensitive customer data. Likewise, rate limiting can reduce the ability to turn an individual weakness into large-scale automated abuse.

The central lesson from the CartBot AI assessment is:

> **An AI application is only as secure as the boundaries around the model.**

Authentication, authorization, data isolation, trusted identity, context handling, and resource controls must be enforced across the application rather than relying on the AI model alone.
