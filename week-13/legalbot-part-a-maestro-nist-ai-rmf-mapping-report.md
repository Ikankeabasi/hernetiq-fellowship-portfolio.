# LegalBot Municipal Part A — MAESTRO + NIST AI RMF Mapping Report

**Mission:** S25 — LegalBot Municipal Part A: Lab Evidence + MAESTRO/NIST AI RMF Report  
**Domain:** Domain 5 — Autonomous Agent Governance  
**Report type:** Part A framework mapping; separate from the Part B remediation report

## 1. System overview

LegalBot Municipal is a simulated AI legal assistant for the City of Fairhaven. It helps staff and citizens with code-violation inquiries, permit questions and records requests. The lab shows an agent that processes citizen comments attached to municipal cases and has a tool path capable of finalizing a case dismissal. The security question is whether the agent can distinguish untrusted case content from authorized instructions and whether a sensitive action is independently controlled.

## 2. Incident summary

In the supplied scenario, the citizen comment for case **CASE-2291** contains an instruction claiming supervisor authorization and telling LegalBot to dismiss the case immediately. The comment is untrusted case content; it is not proof that a supervisor approved the action. The vulnerable scenario combines this attempted goal hijack with standing dismissal authority and no mandatory human-approval checkpoint. The lab's narrative shows the agent proceeding to dismiss the case without approval or an audit trail.

This is a simulated lab incident. It does not establish that a real municipal case was dismissed. The report maps the risks described by the lab and does not claim that a particular Semgrep scan or screenshot was reproduced while preparing this document.

## 3. Attack chain

1. **Untrusted content enters the agent's context.** A citizen comment contains a “SYSTEM OVERRIDE” style instruction and claims the case has already been approved.
2. **Goal hijack is attempted (OWASP Agentic Top 10 ASI01).** The instruction tries to redirect LegalBot from assisting with casework to finalizing a dismissal.
3. **Standing authority makes the attempt consequential (ASI03).** The vulnerable configuration permits the agent to finalize dismissals even though that authority is broader than its ordinary support task requires.
4. **The action can proceed without an independent checkpoint (ASI02).** With no mandatory human-approval gate in the vulnerable scenario, a hijacked goal can reach the sensitive case-finalization action.
5. **The lack of an audit trail weakens accountability.** The lab scenario indicates that no audit log is created for the vulnerable action, making later investigation harder.
6. **Static analysis provides a configuration check.** The lab instructs the fellow to run Semgrep against the supplied fixture to identify the risky configuration flags. This check complements, but does not replace, the behavior evidence.

The key relationship is that goal hijack is the initiating attempt, while excessive authority and missing approval controls allow it to become privilege misuse.

## 4. Evidence

The following evidence items belong in their separate Career Passport fields. This section explains what each item is intended to substantiate; it does not replace the actual screenshots or raw scan output.

| Evidence item | What it should show | Relevance to the mapping |
|---|---|---|
| **Evidence 01 — Standing permission** | Screenshot of the relevant pre-remediation permission/configuration, including the standing dismissal capability and missing approval gate. | Shows the authority and control conditions that make the action possible. |
| **Evidence 02 — Goal hijack** | Screenshot showing the supplied untrusted citizen instruction and the agent's resulting behavior. | Shows the attempted redirection from case content into an agent goal. |
| **Evidence 03 — Privilege misuse** | Screenshot showing the sensitive dismissal being completed in the vulnerable scenario without human approval. | Connects the goal-hijack attempt to a consequential action. |
| **Evidence 04 — Semgrep** | The actual command and result from the supplied fixture. The lab instructions state that three findings are expected in `agent_config.py`. | Provides static-analysis evidence for the risky configuration; it is not, by itself, proof that the simulated action occurred. |

**Evidence note:** Capture or use the screenshots and scan output from the original vulnerable run. The current GitHub Level 5 files include patched-state material, so a current after-patch screen must not be presented as proof of the original vulnerable behavior. Do not state that the scan was run or that a screenshot exists unless the evidence actually shows it.

## 5. MAESTRO mapping

MAESTRO identifies the technical layer where a risk appears and helps reveal how weaknesses across layers combine. The table maps the four primary risks in the lab brief and includes the control gap around observability.

| Risk | Evidence | MAESTRO layer(s) | Why this mapping fits | Relevant control |
|---|---|---|---|---|
| **Goal hijack** | Evidence 02 | **L1 — Foundation Models; L3 — Agent Frameworks** | The model may interpret an instruction embedded in citizen content as authoritative, and the agent workflow can pass that interpretation through to an action. The comment is an input data path, but the available scenario does not establish a separate data-pipeline compromise in L2. | Treat citizen comments as untrusted data, separate data from instructions, and test malicious as well as benign comments. |
| **Standing permission** | Evidence 01 | **L3 — Agent Frameworks; L6 — Security & Compliance** | The agent's workflow exposes a sensitive dismissal capability, while the permission and approval policy allows it to act beyond its ordinary support needs. | Apply Least Agency: remove unnecessary standing dismissal authority and scope tools to the task. |
| **Privilege misuse** | Evidence 03 | **L3 — Agent Frameworks; L6 — Security & Compliance** | The action path can turn a hijacked goal into a sensitive administrative action without an independent authorization decision. | Enforce authorization at the action/tool boundary and require human approval for case dispositions. |
| **Control gap and limited observability** | Evidence 01, 03 and 04 | **L5 — Evaluation & Observability; L6 — Security & Compliance** | The scenario lacks an audit trail for the vulnerable action, while Semgrep is intended to identify risky configuration before deployment. | Record relevant agent actions and decisions; add repeatable static analysis and regression checks to the review process. |

**Other MAESTRO layers:** L2 — Data Operations was considered because the instruction arrives through case content, but the scenario does not establish an independent data-pipeline compromise. L4 — Deployment & Infrastructure is not established as a separate infrastructure compromise by the supplied evidence. L7 — Agent Ecosystem is not a separate finding because this scenario concerns one agent rather than a multi-agent ecosystem. These layers are not marked as confirmed vulnerabilities without supporting evidence.

## 6. NIST AI Risk Management Framework mapping

The NIST AI RMF provides four complementary functions. They should be applied where they fit the finding rather than forced onto every risk.

| Function | Application to LegalBot Municipal |
|---|---|
| **Govern** | Define ownership and accountability for the agent, establish which municipal actions require human authorization, and approve a Least Agency policy. A support assistant should not receive standing authority to make consequential case dispositions merely for convenience. |
| **Map** | Document the agent's intended purpose, available tools, permission boundaries, citizen-comment input path, affected people and possible consequences. The relevant context includes citizens, municipal staff, case records and the risk of an incorrect dismissal. |
| **Measure** | Evaluate whether the agent can be redirected by adversarial comments, whether a sensitive action can occur without approval, and whether the control configuration is secure. Use the actual behavior screenshots and Semgrep output as evidence; preserve test conditions and results so the review can be repeated. |
| **Manage** | Prioritize the risk of an unauthorized case disposition. Recommended responses include removing unnecessary standing authority, requiring human approval at the action boundary, treating citizen content as untrusted data, enabling audit logging, and tracking static-analysis findings until addressed. Verify controls through the separate remediation and before/after tests in Part B. |

## 7. Controls

The following are recommended controls arising from the Part A investigation. They are not a claim that this report implemented them.

1. **Least Agency:** remove the agent's standing dismissal permission when it is not required for the assigned task.
2. **Independent authorization:** require a human approval decision for a sensitive case disposition. Enforce this in the action path, not only in the model prompt.
3. **Untrusted-input handling:** keep citizen comments as case data rather than authority-bearing instructions; add validation and clear separation between trusted application instructions and untrusted content.
4. **Auditability:** retain a useful record of the case, requested action, decision path, actor and timestamp, with monitoring for unusual or unauthorized actions.
5. **Repeatable evaluation:** keep the Semgrep checks in the development/review process and test both benign and malicious comments, including attempts to reach the dismissal action without approval.

## 8. Conclusion

LegalBot's main risk is not prompt injection in isolation. It is the combination of untrusted citizen content, standing authority to dismiss a case, and no mandatory human-approval checkpoint. That combination can allow an attempted goal hijack to become privilege misuse. MAESTRO identifies the relevant model, agent-workflow, observability and security-policy layers; NIST AI RMF translates the findings into governance, context mapping, evaluation and risk-treatment activities.

This is the **Session 25 / Part A mapping report**. It is distinct from the Evidence 05 explanation and from the Session 26 / Part B remediation report. The actual screenshots and Semgrep result must remain genuine, separate evidence artefacts.

## Framework and lab references

- **MAESTRO — Cloud Security Alliance:** https://labs.cloudsecurityalliance.org/maestro/
- **NIST AI RMF Core — Govern, Map, Measure and Manage:** https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- **NIST AI RMF 1.0 publication:** https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf
- **LegalBot Level 5 lab:** https://github.com/Ikankeabasi/ai-security-defense-lab/blob/main/levels/level5_legalbot.py
- **Semgrep configuration:** https://github.com/Ikankeabasi/ai-security-defense-lab/blob/main/.semgrep.yml
- **Session 25 evidence brief:** *Week13_Session_25_Evidence_Brief.pdf*
