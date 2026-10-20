# LegalBot Municipal — Part A Evidence and Explanation

**Mission:** S25 — LegalBot Municipal Part A: Lab Evidence + MAESTRO/NIST AI RMF Report  
**Domain:** Domain 5 — Autonomous Agent Governance  
**Purpose:** This document groups Evidence 01–04 with captions and explains how the evidence connects. The MAESTRO + NIST AI RMF mapping report is a separate deliverable for Evidence 06.

## Evidence 01 — Standing permission

**What this screenshot should establish:** The relevant vulnerable configuration/permission, especially the agent's ability to finalize a dismissal and the absence of a required human-approval gate.

**Caption:** *Standing dismissal permission — LegalBot has authority to finalize a sensitive case disposition without a mandatory human approval step. This is excessive standing authority for an assistant whose normal role is to answer municipal questions.*

<img width="1917" height="1066" alt="Screenshot 2026-10-19 141543" src="https://github.com/user-attachments/assets/88b82734-1498-40a6-94e9-c6434c1ad128" />

## Evidence 02 — Goal hijack

**What this screenshot should establish:** The supplied instruction inside the citizen comment and the agent's response to it. The comment is untrusted case content, not proof of supervisor authorization.

**Caption:** *Indirect goal-hijack attempt — the citizen comment includes an instruction claiming supervisor authorization and directing LegalBot to dismiss the case. This shows how untrusted content can attempt to redirect an agent's goal.*

<img width="1644" height="516" alt="Screenshot 2026-10-19 203805" src="https://github.com/user-attachments/assets/f26178f9-0a0c-4e9b-8fd3-3e4f84b2572f" />

## Evidence 03 — Privilege misuse

**What this screenshot should establish:** The sensitive dismissal action completing without a human approval step in the original vulnerable scenario.

**Caption:** *Privilege misuse — the attempted goal hijack reaches a sensitive case-dismissal action because the vulnerable agent has standing authority and no mandatory human-approval checkpoint.*

<img width="3506" height="1636" alt="Screenshot-2026-10-19-141548" src="https://github.com/user-attachments/assets/8bb6bc70-346b-4482-876a-2112a5e12456" />

## Evidence 04 — Semgrep result

**What this screenshot should establish:** The actual Semgrep command and output from the supplied fixture. The Session 25 brief says three findings are expected in `agent_config.py`. The screenshot, not this caption, is the record of the actual result.

**Caption:** *Static-analysis result — Semgrep checks the supplied LegalBot fixture for risky configuration. This complements the behavioral evidence by identifying configuration weaknesses; it does not by itself prove that the dismissal occurred.*

<img width="1095" height="897" alt="Screenshot 2026-10-13 143709" src="https://github.com/user-attachments/assets/c7e98af7-23d1-4f41-947d-b6dd641f2ede" />

## Evidence 05 — Explanation connecting the evidence

The four evidence items show different parts of the same risk chain. Evidence 01 establishes the vulnerable authority and missing approval control. Evidence 02 shows an instruction embedded in untrusted citizen content attempting to redirect LegalBot's goal. Evidence 03 shows the consequence in the vulnerable scenario: the agent can carry out a sensitive dismissal without independent human approval. Evidence 04 provides a static-analysis check of the risky configuration.

Together, they show that prompt injection is not the only problem. The risk becomes consequential because untrusted content can influence the agent while the agent has excessive standing authority and no independent approval checkpoint. Least Agency, action-level authorization, safe handling of citizen content, and audit logging are appropriate controls to reduce the risk.

**Evidence integrity note:** These screenshots should represent the original Part A/vulnerable investigation. Do not replace Evidence 03 with a patched-state screenshot showing the action blocked; that belongs with the Part B remediation and verification evidence. Do not claim a Semgrep run or result beyond what the screenshot actually shows. Redact tokens, API keys, passwords, and other secrets before submission.

## Separate Evidence 06 — MAESTRO + NIST AI RMF mapping report

Submit the mapping report as a separate document/link in Career Passport Evidence 06. Do not paste the same evidence-explanation link into Evidence 06.

- [Part A MAESTRO + NIST AI RMF mapping report](legalbot-part-a-maestro-nist-ai-rmf-mapping-report.md)
- [Part B remediation and verification report — Session 26, separate stage](legalbot-part-b-maestro-nist-remediation-report.md)
