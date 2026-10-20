# LegalBot Municipal Part B — Remediation and Verification Report

**Mission:** S26 — LegalBot Municipal Part B: Architectural Remediation + Verification + MAESTRO/NIST Mapping  
**Domain:** Domain 5 — Autonomous Agent Governance  
**Purpose:** Document the intended patch and map it to MAESTRO and the NIST AI RMF.

## 1. Introduction

LegalBot Municipal is a simulated municipal AI assistant for the City of Fairhaven. Session 25 described a citizen comment containing a malicious instruction that attempts to redirect the agent and cause case CASE-2291 to be dismissed. Session 26 focuses on reducing the agent's authority, separating citizen content from trusted instructions, requiring human approval, enabling audit logging, and verifying the changed behavior.

## 2. Original weakness

The Part A scenario identifies four related weaknesses:

- `CAN_FINALIZE_DISMISSAL = True`: the agent has standing authority to finalize a sensitive case disposition.
- `REQUIRE_HUMAN_APPROVAL = False`: the sensitive action has no mandatory human checkpoint.
- `SANITIZE_CITIZEN_INPUT = False`: citizen content is not marked and handled as untrusted data.
- `LOG_AGENT_ACTIONS = False`: the intended agent-action audit trail is disabled.

The injected instruction is the attempted goal hijack (OWASP Agentic Top 10 ASI01). Excessive authority and the missing approval boundary can allow it to become tool misuse or privilege abuse (ASI02/ASI03). This is a lab scenario, not evidence that a real municipal case was dismissed.

## 3. Remediation

The standalone hardened configuration accompanying this report applies the following controls:

1. Set `CAN_FINALIZE_DISMISSAL = False` so the agent cannot finalize a dismissal directly.
2. Set `REQUIRE_HUMAN_APPROVAL = True` and route sensitive requests to a pending human-review state.
3. Set `SANITIZE_CITIZEN_INPUT = True` and represent the comment as `untrusted_data`, not an instruction.
4. Set `LOG_AGENT_ACTIONS = True` and create a timestamped audit event when a request is queued.
5. Fail closed if a caller attempts to enable direct finalization.

The example returns an audit record for demonstration. A production implementation must persist logs to a protected, access-controlled audit store and integrate the approval queue with the actual authorized workflow. A standalone example does not, by itself, prove that the hosted lab has been patched.

## 4. Verification

**Evidence status:** The GitHub source and reference configuration can be inspected, but runtime verification screenshots/results still need to be captured from the lab. This report does not claim that a live test or automated test suite was run while preparing it.

Capture and attach evidence for each check:

| Check | Expected result after patch | Evidence to attach |
|---|---|---|
| Patched configuration | The four security flags show False/True/True/True respectively | Screenshot of the patched configuration |
| Malicious citizen comment | The supplied instruction is displayed/handled as untrusted content | Screenshot showing the payload and resulting state |
| Direct sensitive action | The agent does not finalize the case directly | Screenshot showing the action blocked or `executed = False` |
| Human approval | The request is queued as `pending_human_review` | Screenshot of the pending approval state |
| Audit logging | A timestamped record identifies the case, requested action, actor and time | Screenshot of the resulting audit record |

A code listing demonstrates the intended control logic; it is not a substitute for the lab's actual before/after runtime evidence. Do not label a screenshot as a successful test unless the result is visible.

## 5. MAESTRO mapping

| Risk/control | MAESTRO layer | Justification | Remediation / verification |
|---|---|---|---|
| Goal hijack through a citizen comment | **L1 — Foundation Models; L3 — Agent Frameworks** | The model may interpret an embedded instruction as authoritative, and the agent workflow may pass that interpretation to a tool. | Treat citizen content as untrusted data; capture the malicious-input test. |
| Excessive standing dismissal authority | **L3 — Agent Frameworks; L6 — Security & Compliance** | Tool permissions let the agent perform a sensitive disposition outside its support role. | Disable direct finalization and verify the permission configuration. |
| Missing human-approval checkpoint | **L3 — Agent Frameworks; L6 — Security & Compliance** | No independent authorization decision separates the agent's request from the consequential action. | Require approval and capture the pending-review state. |
| Missing action audit trail | **L5 — Evaluation & Observability; L6 — Security & Compliance** | Without an action record, investigation and accountability are weakened. | Enable logging and capture the resulting audit record; production logs should be persisted securely. |
| Unsafe treatment of external/citizen content | **L1 — Foundation Models; L3 — Agent Frameworks** | Untrusted text may be interpreted as instructions and redirect the agent's goal. | Mark the comment as untrusted data and verify it cannot authorize a disposition. |
| Verification and regression risk | **L5 — Evaluation & Observability** | A configuration change alone does not prove the behavior changed. | Preserve before/after evidence and repeatable test results. |

L2 (Data Operations), L4 (Deployment & Infrastructure), and L7 (Agent Ecosystem) are not claimed as confirmed findings here because the available LegalBot scenario does not establish a separate data-pipeline compromise, infrastructure compromise, or multi-agent interaction.

## 6. NIST AI RMF mapping

The four functions are complementary risk-management lenses, not a rigid sequence.

| Function | Application to LegalBot | Evidence |
|---|---|---|
| **Govern** | Define who owns the agent, which case dispositions require human authorization, and the policy that prevents the agent from holding unnecessary standing authority. | Patched permission/approval configuration and the approval-state screenshot. |
| **Map** | Describe the agent's intended role, users, citizen-comment input path, available tools, permission boundaries, affected people, and possible consequences of an incorrect dismissal. | Scenario and configuration evidence, plus the untrusted-input screenshot. |
| **Measure** | Evaluate whether malicious comments can redirect the agent, whether a disposition can execute without approval, and whether the audit event is produced. | Actual before/after runtime screenshots and recorded test results. These remain to be attached until captured. |
| **Manage** | Reduce the identified risk by disabling direct finalization, requiring human review, treating citizen input as untrusted, and logging requests/actions. Track any remaining issues through review and retesting. | The patched configuration and the actual blocked-action, pending-approval, and audit-record evidence. |

## 7. Conclusion

The main lesson is that prompt-injection filtering alone is not a sufficient safety boundary. The most important containment control is to remove the agent's standing authority to perform a sensitive case disposition. Treating citizen comments as untrusted data reduces the chance of goal hijack, human approval prevents the agent from completing the action alone, and audit logging supports accountability. The remediation should be considered verified only after the lab's actual behavior and audit record have been captured and reviewed.

## Evidence links

- Reference hardened configuration: `legalbot-part-b-hardened-config.py` in the Week 13 portfolio folder.
- Lab Level 5 source and interactive demonstration: https://github.com/Ikankeabasi/ai-security-defense-lab/blob/main/levels/level5_legalbot.py
- Part A mapping report (background only; not a substitute for this Part B remediation report): https://github.com/Ikankeabasi/ai-security-defense-lab/blob/main/LegalBot-Municipal-MAESTRO-NIST-AI-RMF-Mapping-Report.md
