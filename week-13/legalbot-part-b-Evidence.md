# LegalBot Municipal — Part B Screenshot Evidence 

## Evidence 01 — Patched configuration
*Patched LegalBot configuration — standing dismissal authority is disabled, human approval is required, citizen input is handled as untrusted data, and agent-action logging is enabled.*

<img width="1919" height="1079" alt="Screenshot 2026-10-20 153706" src="https://github.com/user-attachments/assets/3090a980-ec53-450c-910b-eb4587517e68" />


## Evidence  02 — Untrusted citizen input
*Untrusted citizen content — the comment contains an instruction claiming supervisor authorization, but the comment itself is not proof of approval and must not authorize a case dismissal.*

<img width="960" height="225" alt="Screenshot 2026-10-20 154441" src="https://github.com/user-attachments/assets/e768a4b6-6d50-430b-9eb8-3107ef1c918c" />


## Evidence  03 — Sensitive action blocked
*Blocked direct action — after the patch, the malicious instruction does not directly dismiss CASE-2291. LegalBot reports that no case was closed.*

<img width="1905" height="391" alt="Screenshot 2026-10-20 155028" src="https://github.com/user-attachments/assets/e6415063-ddc0-4e58-9a49-fd35115aca69" />


## Evidence 04 — Human approval / pending state
*Human approval required — the requested sensitive action is routed for human review instead of being executed directly by the agent.*

<img width="1655" height="165" alt="Screenshot 2026-10-20 155214" src="https://github.com/user-attachments/assets/d1b04f8d-6d3e-4a36-9c34-501a928170d6" />


## Evidence 05 — Audit record
*Audit record — the requested agent action is recorded so the event can be reviewed and investigated.*

<img width="1710" height="328" alt="Screenshot 2026-10-20 155536" src="https://github.com/user-attachments/assets/75b097a5-8f4d-4ee0-8dc2-b4e66af3ea56" />


## Short explanation connecting the Part B screenshots

The patched configuration removes the agent's standing authority to dismiss cases, requires human approval, treats citizen comments as untrusted data, and enables action logging. The malicious comment screenshot shows the input that attempts to hijack the agent's goal. The blocked-action and pending-review evidence should show that this instruction cannot directly produce the sensitive action after remediation. The audit evidence should show that the request is recorded for accountability. Together, these checks address the original combination of goal hijack, excessive authority, missing approval, and weak observability.
