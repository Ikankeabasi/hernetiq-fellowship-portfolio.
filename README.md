# HerNetIQ AI Security Fellowship — Portfolio

## About This Repository

This repository documents my hands-on learning journey throughout the HerNetIQ AI Security Fellowship. It contains weekly practical projects, security reports, architecture and threat-model documentation, cloud security exercises, AI security assessments, and technical write-ups that demonstrate my growing skills in AI Security and Cloud Security.

The portfolio is organized week by week so that each stage of the fellowship can be followed from foundational concepts through practical security investigation, attack analysis, remediation, verification, and career positioning.

## Weekly Evidence

| Week | Topic | Deliverable |
|------|-------|-------------|
| Week 1 | 4-Layer AI Architecture | AI Architecture Diagram |
| Week 2 | Defensive Python & JSON Security Log Analysis | Code Review Findings & CloudTrail IOC Analysis |
| Week 3 | Cloud Security Core (IAM) | Hardened MedVitals IAM Policy (JSON) |
| Week 4 | MedVitals AI – Cloud Infrastructure Security | Incident Timeline Report · Medium Technical Walkthrough · Level 1 Portfolio Completed |
| Week 5 | AI Agent Security | AI Agent Security Analysis · Prompt Injection Assessment · Incident Report · Security Patch |
| Week 6 | AI Model & ML Supply-Chain Security | DataForge ML Threat Assessment · IOC Analysis · MITRE ATLAS Mapping · Model Loader Remediation |
| Week 7 | Application & API Security | API Security Analysis · BOLA Assessment · Indirect Prompt Injection & Cross-Tenant Leakage Analysis |
| Week 8 | AI Application & API Security — CartBot AI | Threat Model · AI Application Security Assessment Report · Remediation & Verification Evidence |
| Week 9 | Mid-Fellowship Career Artifact & Portfolio Positioning | Portfolio Update · Career Self-Audit · LinkedIn Strategy · Profile Positioning |

## Week 1 — 4-Layer AI Architecture

Focused on understanding the architecture of AI systems and the security risks that can exist across different layers. The week established the foundation for thinking about AI systems as connected components rather than treating the model as the only security concern.

**Key focus:** AI architecture, security boundaries, components, data movement, and identifying risks across the AI stack.

## Week 2 — Defensive Python & JSON Security Log Analysis

Focused on reading code and security logs from a defensive perspective. The work included identifying security issues in Python configuration and analyzing CloudTrail-style JSON security events using an IOC and 5Ws approach.

**Key focus:** defensive code review, exposed secrets, configuration weaknesses, JSON log analysis, Indicators of Compromise (IoCs), and structured security investigation.

## Week 3 — Cloud Security Core (IAM)

Focused on AWS Identity and Access Management and the Principle of Least Privilege. The practical work involved reviewing an overly permissive MedVitals IAM policy and producing a hardened JSON policy.

**Key focus:** IAM users, roles and policies, permissions, least privilege, cloud access control, and secure IAM policy writing.

## Week 4 — MedVitals AI: Cloud Infrastructure Security

Focused on investigating a cloud-security incident involving an AI-enabled healthcare environment. The work covered incident investigation, CloudTrail evidence, Indicators of Compromise, attack timeline reconstruction, and security documentation.

**Key focus:** cloud infrastructure security, incident response, CloudTrail analysis, IoCs, attack timelines, secrets management, and professional incident reporting.

## Week 5 — AI Agent Security

Week 5 moved the focus from general AI security foundations into the security of AI agents and their interaction with tools, data, and external instructions.

The practical work focused on the first AI Agent scenario and examined how prompt injection can influence an AI system when attacker-controlled instructions reach the agent's context or tool-use workflow.

The week's portfolio work includes:

- AI Agent security analysis
- Prompt Injection assessment
- A one-page Incident Report
- Security patch/remediation work
- Documentation of the observed weakness and defensive response

**Key focus:** AI agents, prompt injection, attacker-controlled instructions, security impact, incident reporting, and defensive patching.

## Week 6 — AI Model & ML Supply-Chain Security

Week 6 focused on the security of machine-learning model supply chains using the DataForge ML scenario. The lab examined the risks of downloading and loading a pre-trained model from an unverified public source without appropriate security checks.

The investigation covered publisher verification, model provenance, model files and serialization formats, malicious pickle files, IOC identification, MITRE ATLAS mapping, and safe model-loading practices.

The practical remediation replaced unsafe pickle loading with a safer tensor-based loading approach using `safetensors`.

**Key focus:**

- AI/ML supply-chain security
- Model provenance and publisher verification
- Malicious model files
- Picklescan and static security checks
- MITRE ATLAS
- AML.T0010 — ML Supply Chain Compromise
- AML.T0020 — Craft Poison Training Data
- AML.T0018 — ML Model Backdoor
- Secure model serialization and loading
- Model threat assessment and remediation

## Week 7 — Application & API Security

Week 7 focused on the security boundary between users, applications, APIs, and AI systems. The work introduced the OWASP API Top 10 and examined how traditional API weaknesses can become especially important when an AI assistant is connected to application data and functionality.

The practical work covered authentication versus authorization, Broken Object Level Authorization (BOLA), client-controlled object identifiers, rate limiting, Denial-of-Wallet exposure, indirect prompt injection, and cross-tenant data leakage.

The week also emphasized an important security principle: retrieved or externally supplied content should not automatically be treated as trusted instructions by an AI system.

**Key focus:**

- API security fundamentals
- Authentication vs authorization
- OWASP API Top 10
- API1:2023 — Broken Object Level Authorization
- API4:2023 — Unrestricted Resource Consumption
- Indirect prompt injection
- Cross-tenant leakage
- Trust boundaries
- Least privilege and data isolation
- Rate limiting and resource protection

## Week 8 — AI Application & API Security: CartBot AI

Week 8 brought the previous concepts together in the CartBot AI Level 3 Defense Lab. CartBot is an intentionally vulnerable e-commerce application combining a customer-facing API with an AI shopping assistant.

The assessment examined how API security weaknesses and AI-specific threats can interact within the same application. The investigation identified three connected areas of risk:

1. **Broken Object Level Authorization (BOLA)** — the vulnerable API trusted a client-supplied `customer_id` instead of independently verifying the authenticated customer's authorization to access the requested object.
2. **Indirect Prompt Injection** — attacker-controlled product content could enter the AI assistant's context and influence its behaviour.
3. **Unrestricted Resource Consumption / Denial of Wallet** — disabled rate limiting increased the potential for automated abuse, bulk harvesting, and AI/API resource consumption.

The Week 8 work followed a complete security workflow:

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

The remediation work introduced JWT validation, server-side identity verification, rate limiting, and a restricted AI system prompt. The lab application was changed to report `SECURITY_STATUS = "PATCHED"`.

**Key focus:**

- AI application security
- API security
- Threat modeling and Data Flow Diagrams
- Trust boundaries
- BOLA and object-level authorization
- Indirect prompt injection
- MITRE ATLAS AML.T0051
- MITRE ATLAS AML.T0054
- Rate limiting and Denial-of-Wallet mitigation
- JWT authentication and server-side authorization
- Semgrep static analysis
- Security remediation and verification
- Evidence-led security reporting

### Week 8 Portfolio Documents

- [`week-8/README.md`](./week-8/README.md) — Week 8 overview and guide to the week's portfolio documents
- [`week-8/api-security-threat-model.md`](./week-8/api-security-threat-model.md) — API security threat model and OWASP/MITRE ATLAS classification
- [`week-8/week-8-ai-application-security-report.md`](./week-8/week-8-ai-application-security-report.md) — detailed CartBot AI security assessment and remediation report

## Week 9 — Mid-Fellowship Career Artifact & Portfolio Positioning

Week 9 focused on turning the work completed so far into a clearer career-facing portfolio. The week sits between Domain 3 and Domain 4 and combines a portfolio update, career self-audit, LinkedIn strategy, and profile positioning.

The purpose of the week is not to introduce a new technical lab. Instead, it connects the evidence already produced across the fellowship to a clearer professional story: what I have worked on, what security areas I can demonstrate, how I communicate that work, and where someone can find the evidence.

### Week 9 Work Completed / In Progress

**1. AI Defense Lab `PORTFOLIO.md` update**

The AI Defense Lab portfolio was reorganized for Levels 1–3 using a consistent nine-section structure:

1. Scenario / Investigation
2. Problem / Vulnerability
3. Evidence
4. Remediation
5. Commit
6. Outcome
7. Skills Demonstrated
8. Supporting Artifacts
9. LinkedIn Case Study

This structure makes each completed level easier to read as an evidence-based security case study without rewriting the underlying work.

**2. Career artifact and LinkedIn content**

The career artifact focuses on a self-audit of the skills and evidence developed so far, followed by a LinkedIn case-study post that communicates the practical security work to a professional audience.

The positioning should remain evidence-led and should accurately describe the fellowship work as hands-on simulated security labs rather than claiming production incident experience that has not been demonstrated.

**3. LinkedIn profile positioning**

The profile update focuses on making the professional direction clear within a short first impression. The Week 9 positioning guidance emphasizes describing the security work and areas of focus rather than relying on phrases such as “Cybersecurity Enthusiast” or “AI Security Learner.”

The profile positioning is centred on AI Security, with supporting areas including:

- Cloud Security
- Model Security
- API Security
- AI Application Security
- Threat Modeling
- Security Investigation
- Security Remediation and Verification

The profile should also point visitors toward evidence such as the GitHub portfolio and relevant technical work.

### Week 9 Technical Evidence Context

Week 9 builds its career positioning from the technical work already documented in the portfolio, including:

- CloudTrail investigation and IAM least privilege in the MedVitals AI scenario
- AI/ML model supply-chain security, Picklescan, and safer model serialization in the DataForge ML scenario
- API security, BOLA, indirect prompt injection, rate limiting, threat modeling, Semgrep, remediation, and verification in the CartBot AI scenario

These are hands-on fellowship lab scenarios and are presented as portfolio evidence of practical learning and security investigation.

### Week 9 Career Positioning Principle

A visitor should be able to understand quickly:

> **What security work do I do, what areas have I worked across, and where can I see the evidence?**

The goal is to make the portfolio and LinkedIn profile tell the same story without overstating experience.

## Skills Being Built

- AI Security fundamentals
- AI architecture risk analysis
- AI agent security
- Prompt injection analysis
- Reading Python configuration files for security flaws
- Identifying hardcoded API keys and exposed secrets
- Detecting overly permissive IAM policies
- Applying the Principle of Least Privilege
- Writing secure IAM policies in JSON
- Understanding IAM users, roles, and policies
- AWS CloudTrail log analysis
- Reading CloudTrail JSON security logs using the IOC 5Ws framework
- Cloud incident investigation and attack timeline reconstruction
- Identifying Indicators of Compromise (IoCs)
- Secrets management using environment variables
- Cloud infrastructure security
- AI/ML model supply-chain security
- Model provenance and threat assessment
- Secure model serialization and loading
- Application and API security
- Authentication and authorization analysis
- Broken Object Level Authorization (BOLA)
- Indirect prompt injection detection
- Cross-tenant data isolation
- JWT authentication and server-side authorization
- Rate limiting and Denial-of-Wallet mitigation
- Threat modeling and trust-boundary analysis
- Static analysis with Semgrep
- MITRE ATLAS mapping
- OWASP API Security mapping
- Security remediation and verification
- Security documentation and incident reporting
- Git and GitHub workflow for security projects
- GitHub portfolio management
- Technical writing and security communication

## Security Mindset Developed

Across Weeks 1–9, the fellowship work has progressively moved from understanding AI architecture to investigating security behaviours, applying defensive controls, documenting evidence, and communicating the resulting work professionally.

A recurring principle throughout the portfolio is to ask:

> **What does the system trust, where does that trust change, what can an attacker control, what happens when the system trusts the wrong thing, and what evidence proves the security control works?**

Week 9 adds another practical question to that mindset:

> **Can I communicate the security work accurately enough that another person can understand both the capability and the evidence behind it?**

## About Me

**Ikanke Okon Asuquo**

**AI Security Fellow — HerNetIQ Cohort 1 (2026)**

### Background
Computer Science student with a growing interest in AI Security, Cloud Security, SOC Operations, and Defensive Cybersecurity. I enjoy learning through practical labs and building a portfolio that reflects hands-on security work.

### Currently Building
- Defensive AI Security
- Cloud Security
- Identity and Access Management (IAM)
- Threat Detection & Incident Analysis
- AI Application & API Security
- Security Documentation
- Technical GitHub Portfolio
