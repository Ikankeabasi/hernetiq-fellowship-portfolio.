# Level 5 — MAESTRO Threat Model

## LegalBot Municipal — Agent Governance

**Lab context:** Simulated LegalBot Municipal scenario in the AI Security Defense Lab. This is a source-based assessment of the lab configuration, not evidence of a real municipal incident.

**Related portfolio evidence:** [NIST AI RMF mapping](./nist-ai-rmf-mapping.md)

## Incident summary

LegalBot processes citizen case comments. The vulnerable configuration gives the agent standing dismissal authority, does not require human approval, does not sanitize citizen input, and does not log agent actions. A malicious instruction in a citizen comment may redirect the agent and lead it to attempt an unauthorized case dismissal.

The central failure is architectural: untrusted content can influence agent behavior, while the agent has authority to perform a sensitive action without a required human approval step.

## MAESTRO threat model

| MAESTRO layer | My finding | Risk / impact | Recommended control |
|---|---|---|---|
| **L1 — Foundation Models** | The model may follow an instruction embedded in a citizen comment instead of treating it only as case content. This is a plausible behavior risk in the lab scenario; the model itself is not independently proven compromised. | The agent's intended goal may be redirected. | Test benign and adversarial comments; use layered input and output checks. Do not rely on the model alone to enforce authorization. |
| **L2 — Data Operations** | Citizen comments are untrusted input. The vulnerable fixture sets `SANITIZE_CITIZEN_INPUT = False`. | Malicious instructions may enter the agent's context and influence a later decision. | Treat comments as data, not policy; apply appropriate input handling and keep trusted instructions separate from user-provided content. |
| **L3 — Agent Frameworks** | The vulnerable fixture sets `CAN_FINALIZE_DISMISSAL = True` and `REQUIRE_HUMAN_APPROVAL = False`. This is the clearest path from a hijacked goal to a sensitive action. | The agent may finalize a case dismissal without an authorized human decision. | Remove standing dismissal authority and enforce a human approval gate in the action workflow. Validate authorization in application logic, not only in the prompt. |
| **L4 — Deployment & Infrastructure** | The supplied configuration demonstrates an application-level permission problem. The inspected fixture alone does not establish a separate infrastructure compromise. | If runtime credentials or service permissions also allow unrestricted case changes, the impact could extend beyond the agent's intended task. | Use least-privilege service identities and restrict sensitive operations at the API or service boundary. Verify actual runtime permissions before claiming this control is present or absent. |
| **L5 — Evaluation & Observability** | The vulnerable fixture sets `LOG_AGENT_ACTIONS = False`. The lab asks for before-and-after testing. | Actions may be difficult to investigate or attribute, and a regression could go unnoticed. | Enable structured audit logs for agent decisions, tool calls, approvals, and final actions; test both normal and adversarial cases after remediation. |
| **L6 — Security & Compliance** | Sensitive case dismissal lacks a required human approval step in the vulnerable configuration. This indicates a governance and authorization-control gap. | Incorrect case dispositions may affect citizens and undermine accountability. | Define approval policy, assign accountable owners, document acceptable agent authority, and require human review for sensitive case outcomes. |
| **L7 — Agent Ecosystem** | LegalBot's case-processing workflow may depend on connected APIs or case-management services. The supplied fixture does not prove whether downstream services independently enforce approval. | If a downstream API trusts the agent without checking authorization, a missed agent-level guardrail could still result in an unauthorized state change. | **Validate this design risk:** test whether the downstream service independently checks user/service identity, case permissions, and approval state before finalizing a dismissal. |

## OWASP Agentic classification

- **ASI01 — Agent Goal Hijack:** citizen-provided content attempts to redirect the agent's objective.
- **ASI02 — Tool Misuse & Exploitation:** the agent may use a legitimate case-finalization capability in an unsafe or unintended way.
- **ASI03 — Identity & Privilege Abuse:** the agent has more authority than its ordinary support role requires.

These categories describe related stages of the risk chain; they are not interchangeable. Goal hijack concerns redirection, while tool misuse and excessive authority explain how that redirection can become an action.

## Business impact

- A citizen's case could be dismissed without proper review.
- Case records and administrative decisions could become unreliable.
- Missing action logs could make investigation and accountability harder.
- Public trust in the municipality's case-handling process could be damaged.

These are potential impacts of the simulated scenario, not claims that a real case was dismissed.

## Root cause

The main root cause is **excessive standing authority combined with a missing human approval gate**. Untrusted input handling and missing audit logging increase the likelihood and investigation difficulty, but the architectural permission boundary is the key control that should prevent a hijacked goal from becoming an unauthorized dismissal.

## Remediation and verification plan

1. Set `CAN_FINALIZE_DISMISSAL = False` so the agent cannot independently finalize dismissals.
2. Set `REQUIRE_HUMAN_APPROVAL = True` and enforce approval in the action path.
3. Set `SANITIZE_CITIZEN_INPUT = True`, while still treating sanitization and guard models as defense-in-depth rather than as authorization controls.
4. Set `LOG_AGENT_ACTIONS = True` and verify that relevant actions and approval decisions are recorded.
5. Run `python3 tests/test_legalbot_agent.py` before and after the implementation change. Save the actual terminal output for both runs; do not claim a pass until the after-fix output confirms it.
6. Run the required Semgrep scan against the lab's real fixture and record the actual findings.
7. Validate the proposed downstream authorization risk in L7 before describing it as a confirmed vulnerability.

## Additional threat-model item — Risk 9

**Risk 9: Downstream authorization bypass (design risk to validate).**

**Scenario:** Even after the agent's own configuration is hardened, a connected case-management API might accept a dismissal request without independently checking that a human approval has been recorded.

**Impact:** A faulty or manipulated agent could still cause a sensitive case state change if the downstream service trusts the caller's request.

**Control:** Enforce authorization and approval checks in the downstream service, deny by default, and record the identity, approval reference, and result of each dismissal attempt.

**MAESTRO mapping:** L7 — Agent Ecosystem, with L3 — Agent Frameworks also relevant.

**NIST AI RMF mapping:** Measure — test whether the downstream control rejects unapproved requests; Manage — remediate and re-test any gap; Govern — assign responsibility for the approval policy.

**Evidence status:** This is an additional design risk proposed for validation. The currently inspected fixture does not prove that the downstream API is vulnerable.

## Evidence notes

- The configuration values above are taken from the Level 5 lab's vulnerable fixture and interface instructions.
- The MAESTRO layer descriptions are my risk assessment based on the simulated scenario.
- The downstream authorization issue in Risk 9 is a hypothesis to test, not an observed result.
- Attach screenshots or terminal output after performing the tests in the lab.
