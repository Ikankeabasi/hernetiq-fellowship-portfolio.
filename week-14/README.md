# Week 14 — Day One: AI Governance Gap Assessment

**Domain 6 · AI Governance (Governance Gap Assessment) · HerNetIQ AI Security Fellowship**

## What I am working on

This week, I am applying what I learned in S28/S29, **AI Governance & Executive Risk Communication**, to a practical governance gap assessment. My task is to compare the controls an AI governance programme claims to have with what the available system configuration and code actually enforce.

I am keeping the work evidence-based. I will not treat a policy statement or a configuration flag as proof that a control works. I will check the implementation, record the exact evidence location, explain the risk, map each finding to the NIST AI Risk Management Framework and the relevant OWASP category where applicable, and recommend an action that has a clear owner and timeframe.

## Day One focus

- Review the Evidence Brief A requirements and define the assessment scope.
- Inspect the available PayGuard configuration and fine-tuning pipeline code.
- Record policy-to-system gaps with file and line citations.
- Rate each finding as Critical, High, or Medium and explain why.
- Map findings to NIST AI Risk Management Framework functions and relevant OWASP LLM Top 10 categories.
- Build a regulatory exposure table using the framework control areas covered in my fellowship notes.
- Keep the report in my own voice and write it so a technical reviewer and a CTO can understand the finding and the action needed.

## Evidence Brief A deliverables

1. **Governance gap assessment** — at least three findings. Each finding must include the policy claim, observed behaviour, NIST function, OWASP category where applicable, severity with rationale, remediation, and evidence citations.
2. **Regulatory exposure table** — each finding mapped to a named framework or regulation and a specific article, section, or control area.
3. **Overall verdict** — one sentence on whether the governance programme is fit for purpose in its current state, supported by a brief rationale.

## Files in this folder

- [Governance Gap Assessment](./governance-gap-assessment.md) — working assessment, findings, regulatory exposure, and evidence limitations.

## Assessment approach

I am using the four NIST AI Risk Management Framework functions:

- **GOVERN** — policies, roles, and accountability.
- **MAP** — identify and understand the risk.
- **MEASURE** — evaluate and track the risk.
- **MANAGE** — put controls and responses in place.

I am also using the policy-reading questions from my notes: what control is claimed, whether a real process exists, who is accountable, what happens if the control fails, and whether the actual system matches the policy.

## Evidence status and limitations

The connected lab repository provides PayGuard configuration and pipeline code, which I have cited in the assessment. However, the actual client governance policy document and an audit log were not present among the materials I could access for this task. I have marked the policy-clause references and audit-log review as outstanding instead of inventing quotations, page numbers, or log evidence.

**This is a working draft, not a final submission-ready assessment until the actual policy document and any required audit log are available and the policy claims can be cited precisely.** I will update the findings with the exact policy clause and page reference once those artefacts are provided.

## Career Passport evidence notes

When I complete the evidence, I will be able to explain:

1. **What I did:** compared governance expectations with the available PayGuard code.
2. **What security problem I was solving:** checking whether controls for tenant isolation, training-data integrity, and model sourcing are actually enforced.
3. **What I changed or built:** produced a structured gap assessment and regulatory exposure table.
4. **How I verified it:** cited the relevant files and lines; any runtime or audit-log verification must be recorded only after I actually perform it.
5. **What was difficult or unclear:** the actual policy document and audit log were not available, so policy-clause matching and audit-log verification remain open.

## Next

Once the policy document and audit log are available, I will replace the outstanding placeholders with exact evidence and re-check the regulatory mappings before submission. Any additional Part B instructions will be added here when they are provided.
