# LegalBot Municipal — Part A
# MAESTRO and NIST AI Risk Management Framework (AI RMF) Mapping Report

## Purpose and scope

This report combines the Level 5 MAESTRO threat model and NIST AI RMF mapping for the LegalBot Municipal lab. It focuses on the investigation findings and their framework mappings. It is separate from the Part B remediation report.

**Scenario:** The Level 5 lab simulates LegalBot Municipal, an AI legal assistant for the city of Fairhaven. A malicious instruction embedded in a citizen comment attempts to redirect the agent and cause an unauthorized case dismissal.

## 1. MAESTRO threat model

MAESTRO identifies where in the technical agentic system the risk occurs.

| MAESTRO Layer | Finding |
|---|---|
| **L1 — Foundation Models** | The agent may interpret an instruction embedded in a citizen comment as an authoritative directive instead of treating it as untrusted case content. This creates the goal-hijack risk described in the scenario. |
| **L2 — Data Operations** | Not applicable to this incident based on the available investigation. The scenario does not identify a separate data-pipeline issue. |
| **L3 — Agent Frameworks** | The agent can turn a hijacked goal into a tool action because the vulnerable configuration allows dismissal and does not require human approval. The action workflow lacks an effective authorization checkpoint before the sensitive operation. |
| **L4 — Deployment & Infrastructure** | The standing dismissal permission is present in the supplied agent configuration. The available evidence identifies an application-level permission problem; it does not establish a separate infrastructure compromise. |
| **L5 — Evaluation & Observability** | `LOG_AGENT_ACTIONS = False` means the vulnerable configuration does not enable the intended agent-action logging. Without an audit trail, it is harder to identify what happened and investigate or attribute the action. |
| **L6 — Security & Compliance** | The vulnerable setup lacks a mandatory human-approval checkpoint for a sensitive case disposition. The organization should define and enforce a policy for which actions an agent may take independently and which require human authorization. |
| **L7 — Agent Ecosystem** | Not applicable to this incident based on the available investigation. The scenario concerns one agent and does not describe interactions among multiple agents. |

### OWASP Agentic Top 10 classification

- **ASI01 — Agent Goal Hijack:** the citizen comment attempts to redirect the agent.
- **ASI02 — Tool Misuse & Exploitation:** the agent may use its case-finalization capability in an unsafe or unauthorized way.
- **ASI03 — Identity & Privilege Abuse:** standing dismissal authority gives the agent more power than its ordinary support role requires.

### Potential business impact

A case could be dismissed without proper review, leading to an incorrect municipal decision and reduced accountability. Missing action logs could make the incident harder to investigate and could damage public trust. These are potential impacts of the simulated scenario, not claims that a real case was dismissed.

### Root cause identified

The primary root cause is excessive standing authority combined with the absence of a mandatory human-approval gate. Sanitizing citizen input helps reduce goal-hijack risk, and audit logging supports investigation, but neither replaces the authorization boundary. Removing the agent's standing dismissal authority is the key containment control: even if its goal is hijacked, it should not be able to finalize a dismissal on its own.

## 2. NIST AI Risk Management Framework mapping

NIST AI RMF focuses on how the organization should understand and manage the risk. The four functions are Govern, Map, Measure and Manage.

| NIST AI RMF Function | Finding |
|---|---|
| **Govern** | Before deployment, the organization should have clear AI security policies, responsibilities and approval requirements for the agent. LegalBot was given standing authority to finalize and dismiss cases even though that authority was not necessary for its normal support role. Governance should define least-agency/least-privilege requirements, require human approval for sensitive case dispositions, establish who is accountable for the AI system, and involve the relevant technical, AI/governance and legal teams. Applicable organizational policies, standards and legal requirements should be identified before the system is released. |
| **Map** | The agent's purpose, permissions, users and affected parties should have been identified before deployment. LegalBot processes citizen case comments and can act on municipal cases, but it had `CAN_FINALIZE_DISMISSAL = True` and `REQUIRE_HUMAN_APPROVAL = False`. The citizen comment was the source of the goal-hijack attempt. The risk could affect citizens, municipal case records and staff responsible for reviewing cases. The excessive standing permission was a key red flag because a hijacked goal could become a real administrative action. |
| **Measure** | The organization should test whether the agent behaves safely before deployment and during operation. A security assessment could create a test account, submit normal and malicious case comments, and attempt to redirect the agent from its intended task. The configuration should also be reviewed and scanned for risky permissions. The goal is to determine whether the agent can be hijacked, whether it can act without approval, and how serious the resulting impact would be. Findings should be assessed and prioritised according to their risk level. |
| **Manage** | The first response is to remove the standing dismissal authority by setting `CAN_FINALIZE_DISMISSAL = False` and require human approval with `REQUIRE_HUMAN_APPROVAL = True`. Citizen input should be treated as untrusted data and sanitised with `SANITIZE_CITIZEN_INPUT = True`. Agent actions should be logged with `LOG_AGENT_ACTIONS = True` for monitoring and audit. Additional controls such as guardrails can provide another defensive layer. The fix should then be tested again to confirm that a hijacked instruction cannot directly cause an unauthorised case disposition. |

## 3. Combined interpretation

The MAESTRO mapping identifies the technical locations of the risks: model interpretation of untrusted content, agent-framework action flow, standing permissions, observability and security policy. The NIST AI RMF mapping organizes the corresponding organizational work: establish accountability and approval policy (**Govern**), understand the system and affected parties (**Map**), test the behavior and configuration (**Measure**), and prioritize the response and controls (**Manage**).

The two frameworks are complementary. MAESTRO answers **where in the agentic system the risk sits**; NIST AI RMF answers **how the organization should identify, evaluate and manage it**. In this scenario, the central issue is not prompt injection alone: it is the combination of an untrusted instruction and an agent that has standing authority to perform a sensitive action without human approval.

## Source documents

- [Level 5 — MAESTRO Threat Model](https://github.com/Ikankeabasi/hernetiq-fellowship-portfolio./blob/main/week-13/level-5-maestro-threat-model.md)
- [Level 5 — NIST AI RMF Mapping](https://github.com/Ikankeabasi/hernetiq-fellowship-portfolio./blob/main/week-13/nist-ai-rmf-mapping.md)

**Scope note:** This is the Part A mapping report. It is not a claim that the Part B remediation tests have been performed or that their results are demonstrated here.
