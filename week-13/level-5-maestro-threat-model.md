# Level 5 — MAESTRO Threat Model

## LegalBot Municipal — Agent Governance

**Scenario:** The Level 5 lab simulates LegalBot Municipal, an AI legal assistant for the city of Fairhaven. A malicious instruction embedded in a citizen comment attempts to redirect the agent and cause an unauthorized case dismissal.

## MAESTRO Threat Model

| MAESTRO Layer | MY Finding |
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


---

# Mapping to the OWASP Agentic Top 10

The LegalBot findings map to the following OWASP Agentic Top 10 categories:

- **OWASP Agentic Top 10 — ASI01: Agent Goal Hijack.** A malicious instruction is embedded in a citizen comment and attempts to redirect LegalBot from its intended role. The agent may treat this untrusted case content as an authoritative instruction.
- **OWASP Agentic Top 10 — ASI02: Tool Misuse & Exploitation.** After the agent's goal is hijacked, its available case-finalization capability can be used to carry out an unsafe or unauthorized dismissal. The missing human-approval gate allows the attempted misuse to reach a sensitive action.
- **OWASP Agentic Top 10 — ASI03: Identity & Privilege Abuse.** LegalBot has standing dismissal authority that is broader than needed for its ordinary support role. This excessive standing permission means a hijacked goal can become an actual administrative action. Applying **Least Agency** means removing that unnecessary authority, not merely relying on a warning or an extra check.
