# Week 16 — AI Security Capstone

## Overview

I completed a two-phase, team-based capstone as part of the HerNetIQ AI Security Fellowship. The project simulated a pre-investment security and AI-risk assessment for a financial technology platform providing digital financial services and an AI-powered customer support assistant.

The work followed a practical security-engagement process: understand the environment, assess how the system handles users and data, test controls within the authorised scope, document evidence, support remediation and communicate priorities to technical and business stakeholders.

## Phase 1 — Engagement kickoff and initial assessment

We organised the team, agreed responsibilities and scope, reviewed the available application, architecture, configuration and infrastructure materials, and mapped system components, data flows and trust boundaries. We carried out controlled assessment activities across application and API security, customer-data protection, AI and model security, and cloud infrastructure.

We maintained a shared findings register and testing log, considered the potential business impact of observations, and prepared an interim assessment update. We distinguished observed results from assumptions and items that required further verification.

## Phase 2 — Remediation, verification and final readout

We used the assessment work to prioritise improvements, support remediation through reviewable changes, examine available test and verification evidence, and prepare the final engagement outputs.

The team produced technical and executive-facing reporting, a practical 30/60/90-day security and AI-governance roadmap, and a final readout. We kept a clear distinction between a change proposed in code, a change tested in the available environment, and a change confirmed as deployed. Where live-environment access or evidence was unavailable, that limitation remained explicit.

## My contribution

My assigned workstream was **Cloud and Infrastructure Security**. I reviewed six infrastructure-as-code files covering cloud identity and permissions, storage, compute, networking/security groups, Terraform backend and environment configuration. I documented infrastructure observations, assessed access-control and network-security design, and contributed to the team's evidence tracking and interim/final reporting.

During Phase 2, I contributed to an infrastructure remediation change intended to restrict service access to the approved application load-balancer security group rather than allow broad public ingress. I also participated in remediation discussions and reviewed the available change and test evidence. The deployed production configuration was not independently verified, so I did not represent that work as a confirmed production fix.

Beyond my primary workstream, I supported cross-workstream testing and verification using synthetic accounts, helped review application and AI-related security behaviour, followed remediation discussions, and contributed to shared reporting and roadmap discussions. I kept my conclusions tied to the evidence available and made unresolved verification gaps clear.

## Methods and tools

The work combined source-code and configuration review, infrastructure-as-code review, architecture and trust-boundary mapping, controlled application and API testing, automated test execution, scanner-output triage, version-controlled collaboration and structured evidence tracking.

Tools and working environments included GitHub, GitHub Codespaces, Terraform, Python/pytest and security-scanning tools used during the team review. Automated results were considered alongside manual review and system context rather than treated as proof on their own.

## What I learned

This capstone strengthened my ability to carry security work from investigation through remediation planning and communication. I learned to assess technical issues in terms of their possible effect on customers and the business, collaborate across different security disciplines, and explain clearly what the evidence proves—and what still needs to be verified.

It reinforced that a security improvement is not complete simply because a code change has been made. Testing, review, deployment and verification all matter.

---
