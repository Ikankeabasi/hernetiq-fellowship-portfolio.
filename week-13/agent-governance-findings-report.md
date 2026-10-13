# Agent Governance Findings Report — Level 5

## LegalBot Municipal | Autonomous Agent Governance

## 1. Executive Summary

In Level 5, I assessed a simulated municipal AI legal assistant called LegalBot Municipal, used by the City of Fairhaven to help with code-violation cases, permit questions and records requests. The scenario showed how a malicious instruction placed inside a citizen comment could redirect the agent and lead it to dismiss a case without human approval.

The main weakness was not prompt injection alone. LegalBot had standing authority to finalize dismissals even though this permission was not needed for its normal support role. The vulnerable configuration also lacked input sanitization, mandatory human approval and agent-action logging. Together, these weaknesses could turn a manipulated goal into an unauthorized action with limited accountability.

I updated the lab's Level 5 code to show the patched state and added a hardened-configuration example. The intended controls remove standing dismissal authority, route requested actions to human review, treat citizen comments as untrusted data and enable action logging. I also completed the MAESTRO threat model and NIST AI RMF mapping below. This is a lab simulation; it does not mean a real municipal case was dismissed.

## 2. Scenario and Investigation

The test case was **CASE-2291**, a routine code-violation case. Its citizen comment contained a message claiming that the case had already been reviewed and authorized for dismissal, then instructed LegalBot to finalize the dismissal immediately.

In the vulnerable scenario, the agent could treat that comment as an instruction, call its dismissal capability and close the case without a human checkpoint. The citizen did not need to speak directly to the agent for the attack to reach it: the comment was part of the case information processed by the system. Therefore, a defence that checks only messages typed directly into a chatbot would miss instructions embedded in records, uploaded documents or other external content.

The incident maps to three OWASP Agentic Top 10 categories:

- **ASI01 — Agent Goal Hijack:** untrusted citizen content attempts to redirect the agent's goal.
- **ASI02 — Tool Misuse and Exploitation:** the agent may use its case-finalization capability to carry out an unsafe action.
- **ASI03 — Identity and Privilege Abuse:** the agent has standing dismissal authority beyond what its ordinary support role requires.

## 3. Main Findings

1. **Excessive standing authority:** `CAN_FINALIZE_DISMISSAL = True` allowed LegalBot to finalize a dismissal without needing that permission for its usual role.
2. **No mandatory approval:** `REQUIRE_HUMAN_APPROVAL = False` meant a sensitive action could proceed without a human checkpoint.
3. **Untrusted input was not separated from instructions:** `SANITIZE_CITIZEN_INPUT = False` meant citizen comments were passed into the agent's context without the intended protection.
4. **No intended action audit trail:** `LOG_AGENT_ACTIONS = False` meant the vulnerable configuration did not enable the intended agent-action logging.
5. **Key lesson — Least Agency:** sanitizing input helps reduce goal hijacking, but the strongest containment is to remove the agent's unnecessary standing authority. Even if a malicious instruction reaches the model, it should not be able to finalize a case by itself.

## 4. Remediation Implemented in the Lab

I changed the Level 5 lab status to `SECURITY_STATUS = "PATCHED"` and updated the hardened-configuration example to demonstrate these controls:

- Set `CAN_FINALIZE_DISMISSAL = False` to remove standing dismissal authority.
- Set `REQUIRE_HUMAN_APPROVAL = True` so requested case dispositions are queued for human review.
- Set `SANITIZE_CITIZEN_INPUT = True` and represent citizen comments as untrusted data, not as instructions.
- Set `LOG_AGENT_ACTIONS = True` so agent actions and queued requests can be recorded for investigation and accountability.
- Keep authorization enforcement in the action path rather than relying only on a prompt filter or guardrail.

The patched lab demonstration is designed to show the goal hijack being blocked from directly dismissing the case and the requested action being queued for human review. The vulnerable fixture remains available in the repository for the exercise's configuration review and static-analysis task; its presence should not be mistaken for the hardened configuration.

## 5. MAESTRO Threat Model

The table below reproduces my Level 5 MAESTRO findings. MAESTRO examines the technical architecture and the ways an agent's goals, tools, permissions and operating environment can create risk.

| MAESTRO Layer | My Finding |
|---|---|
| **L1 — Foundation Models** | The agent may interpret an instruction embedded in a citizen comment as an authoritative directive instead of treating it as untrusted case content. This creates the goal-hijack risk described in the scenario. |
| **L2 — Data Operations** | Not applicable to this incident based on the available investigation. The scenario does not identify a separate data-pipeline issue. |
| **L3 — Agent Frameworks** | The agent can turn a hijacked goal into a tool action because the vulnerable configuration allows dismissal and does not require human approval. The action workflow lacks an effective authorization checkpoint before the sensitive operation. |
| **L4 — Deployment & Infrastructure** | The standing dismissal permission is present in the supplied agent configuration. The available evidence identifies an application-level permission problem; it does not establish a separate infrastructure compromise. |
| **L5 — Evaluation & Observability** | `LOG_AGENT_ACTIONS = False` means the vulnerable configuration does not enable the intended agent-action logging. Without an audit trail, it is harder to identify what happened and investigate or attribute the action. |
| **L6 — Security & Compliance** | The vulnerable setup lacks a mandatory human-approval checkpoint for a sensitive case disposition. The organization should define and enforce a policy for which actions an agent may take independently and which require human authorization. |
| **L7 — Agent Ecosystem** | Not applicable to this incident based on the available investigation. The scenario concerns one agent and does not describe interactions among multiple agents. |
| **OWASP Classification** | **ASI01 — Agent Goal Hijack:** the citizen comment attempts to redirect the agent. **ASI02 — Tool Misuse & Exploitation:** the agent may use its case-finalization capability in an unsafe or unauthorized way. **ASI03 — Identity & Privilege Abuse:** standing dismissal authority gives the agent more power than its ordinary support role requires. |
| **Business Impact** | A case could be dismissed without proper review, leading to an incorrect municipal decision and reduced accountability. Missing action logs could make the incident harder to investigate and could damage public trust. These are potential impacts of the simulated scenario, not claims that a real case was dismissed. |
| **Root Cause** | The primary root cause is excessive standing authority combined with the absence of a mandatory human-approval gate. Sanitizing citizen input helps reduce goal-hijack risk, and audit logging supports investigation, but neither replaces the authorization boundary. Removing the agent's standing dismissal authority is the key containment control: even if its goal is hijacked, it should not be able to finalize a dismissal on its own. |
| **Remediation** | Set `CAN_FINALIZE_DISMISSAL = False`, set `REQUIRE_HUMAN_APPROVAL = True`, set `SANITIZE_CITIZEN_INPUT = True`, and set `LOG_AGENT_ACTIONS = True`. Route requested case dispositions to human review and enforce authorization in the action path. Run the prescribed before-and-after test script and Semgrep scan, and retain screenshots of the actual results as evidence. |

## 6. NIST AI Risk Management Framework (AI RMF) Mapping

The MAESTRO table focuses on technical weaknesses. The NIST AI RMF mapping focuses on the organizational processes that should help prevent, identify and manage those weaknesses.

| NIST AI RMF Function | My Finding |
|---|---|
| **Govern** | Before deployment, the organization should have clear AI security policies, responsibilities and approval requirements for the agent. LegalBot was given standing authority to finalize and dismiss cases even though that authority was not necessary for its normal support role. Governance should define least-agency/least-privilege requirements, require human approval for sensitive case dispositions, establish who is accountable for the AI system, and involve the relevant technical, AI/governance and legal teams. Applicable organizational policies, standards and legal requirements should be identified before the system is released. |
| **Map** | The agent's purpose, permissions, users and affected parties should have been identified before deployment. LegalBot processes citizen case comments and can act on municipal cases, but it had `CAN_FINALIZE_DISMISSAL = True` and `REQUIRE_HUMAN_APPROVAL = False`. The citizen comment was the source of the goal-hijack attempt. The risk could affect citizens, municipal case records and staff responsible for reviewing cases. The excessive standing permission was a key red flag because a hijacked goal could become a real administrative action. |
| **Measure** | The organization should test whether the agent behaves safely before deployment and during operation. A security assessment could create a test account, submit normal and malicious case comments, and attempt to redirect the agent from its intended task. The configuration should also be reviewed and scanned for risky permissions. The goal is to determine whether the agent can be hijacked, whether it can act without approval, and how serious the resulting impact would be. Findings should be assessed and prioritised according to their risk level. |
| **Manage** | The first response is to remove the standing dismissal authority by setting `CAN_FINALIZE_DISMISSAL = False` and require human approval with `REQUIRE_HUMAN_APPROVAL = True`. Citizen input should be treated as untrusted data and sanitised with `SANITIZE_CITIZEN_INPUT = True`. Agent actions should be logged with `LOG_AGENT_ACTIONS = True` for monitoring and audit. Additional controls such as guardrails can provide another defensive layer. The fix should then be tested again to confirm that a hijacked instruction cannot directly cause an unauthorised case disposition. |

## 7. Required Evidence Screenshots

### Evidence 1 — Semgrep Scan

<img width="1095" height="897" alt="Screenshot 2026-10-13 143709" src="https://github.com/user-attachments/assets/40818c60-912e-47ce-95ff-35252acc4ebf" />

### Evidence 2 — Llama Guard: Malicious Comment

<img width="1913" height="895" alt="Screenshot 2026-10-13 144118" src="https://github.com/user-attachments/assets/c4b0c1a5-3453-456a-8754-d23502132257" />

### Evidence  3 — After-Patch Test Run

<img width="1418" height="742" alt="Screenshot 2026-10-13 144500" src="https://github.com/user-attachments/assets/4e01949d-2531-49a3-9202-272be1f988fd" />

## 8. Conclusion

This level demonstrated that prompt injection becomes more serious when an agent has unnecessary authority to act. Input sanitization and guardrails are useful, but they are not substitutes for strong authorization boundaries. My main remediation was to remove LegalBot's standing dismissal permission and route requested case actions through human review, while also enabling input sanitization and audit logging.

The MAESTRO threat model records the technical findings, while the NIST AI RMF mapping records the governance actions needed before deployment and during incident response. Together, they provide a concise record of the simulated incident, its likely business impact and the controls used to reduce the risk.

## Related Level 5 Deliverables

- [MAESTRO Threat Model](level-5-maestro-threat-model.md)
- [NIST AI RMF Mapping](nist-ai-rmf-mapping.md)
- [Level 5 lab code and patched status](https://github.com/Ikankeabasi/ai-security-defense-lab/blob/main/levels/level5_legalbot.py)
- [Lab patch commit](https://github.com/Ikankeabasi/ai-security-defense-lab/commit/43c0915620a7b236125ad2c476c567b79ba9b418)
