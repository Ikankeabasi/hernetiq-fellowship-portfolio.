# LegalBot Municipal — Part A Evidence Explanation

This document connects the four evidence items submitted for the LegalBot Municipal Part A investigation.

**Evidence 01 — Standing permission:** The agent configuration shows the permission that allows LegalBot to finalize a dismissal. This matters because the agent has authority to perform a sensitive municipal action without needing that authority for its normal support role.

<img width="1917" height="1066" alt="Screenshot 2026-10-19 141543" src="https://github.com/user-attachments/assets/88b82734-1498-40a6-94e9-c6434c1ad128" />


**Evidence 02 — Goal hijack:** The malicious instruction is embedded in a citizen comment. This demonstrates the indirect prompt-injection path: content that should be treated as untrusted case data attempts to redirect the agent's goal.

<img width="1644" height="516" alt="Screenshot 2026-10-19 203805" src="https://github.com/user-attachments/assets/f26178f9-0a0c-4e9b-8fd3-3e4f84b2572f" />


**Evidence 03 — Privilege misuse:** This evidence show the sensitive dismissal action occurring without the required human approval.

<img width="3506" height="1636" alt="Screenshot-2026-10-19-141548" src="https://github.com/user-attachments/assets/8bb6bc70-346b-4482-876a-2112a5e12456" />


**Evidence 04 — Semgrep:** The scan provides static-analysis evidence from the supplied fixture.

<img width="1095" height="897" alt="Screenshot 2026-10-13 143709" src="https://github.com/user-attachments/assets/c7e98af7-23d1-4f41-947d-b6dd641f2ede" />
