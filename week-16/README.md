# Week 16 — AI Security Capstone

## Overview

I completed a two-phase, team-based capstone as part of the HerNetIQ AI Security Fellowship. The project simulated a pre-investment security and AI-risk assessment for a financial technology platform offering digital financial services and an AI-powered customer support assistant.

The work followed the kind of process a security team would use in a real engagement: understand the environment, assess how the system handles users and data, test security controls, document evidence, support remediation, and communicate practical next steps to technical and business stakeholders.

## Phase 1 — Understand and assess

We began by organising the team, agreeing responsibilities and scope, and reviewing the available application, architecture, configuration and infrastructure materials. We mapped system components, data flows and trust boundaries, then carried out controlled checks across application and API security, customer-data protection, AI and model security, and cloud infrastructure.

We maintained a shared evidence process through a findings register and testing log, considered the potential business impact of observations, and prepared an interim assessment update. We also distinguished confirmed test results from assumptions and items that required further verification.

## Phase 2 — Remediate, verify and communicate

In the second phase, we used the assessment work to prioritise improvements, support remediation through reviewable changes, examine available test and verification evidence, and prepare the final engagement outputs.

The team developed technical and executive-facing reporting, a practical 30/60/90-day security and AI-governance roadmap, and a final readout. We kept a clear distinction between a change prepared in code, a change tested in the available environment, and a change confirmed as deployed. Where live-environment access or evidence was unavailable, that limitation remained explicit.

## My contribution

I served as **Team Lead for Cloud and Infrastructure Security**.

My work included reviewing infrastructure-as-code and configuration across cloud identity and permissions, storage, compute, networking and Terraform settings. I assessed cloud access-control and network-security design, documented infrastructure observations, and contributed to the team's evidence tracking and client-facing updates.

I also supported work beyond my primary stream. I participated in cross-workstream testing and verification using synthetic accounts, helped review application and AI-related security behaviour, followed remediation discussions and available pull-request evidence, and contributed to the shared reporting and roadmap. I helped keep the team's conclusions tied to evidence and made sure that unresolved verification gaps were not presented as completed fixes.

## Methods and tools

The work combined source-code and configuration review, infrastructure-as-code review, architecture and trust-boundary mapping, controlled application and API testing, automated test execution, scanner-output triage, version-controlled collaboration and structured evidence tracking.

Tools and working environments included GitHub, GitHub Codespaces, Terraform, Python/pytest, and security-scanning tools used during the team review. Automated results were considered alongside manual review and the context of the system rather than treated as proof on their own.

## What I took away

This capstone strengthened my ability to carry security work from investigation through remediation planning and communication. I learned to assess technical issues in terms of their possible effect on customers and the business, collaborate across different security disciplines, and explain clearly what the evidence proves—and what still needs to be verified.

It also reinforced that a security improvement is not complete simply because a code change has been made. Testing, review, deployment and verification all matter.

---

*This is a public, sanitised summary of my learning and contribution. It does not disclose the organisation or individuals involved, specific assessment findings, internal system details, source code, screenshots, test data or confidential engagement documents.*
