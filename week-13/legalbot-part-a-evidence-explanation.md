# LegalBot Municipal — Part A Evidence Explanation

This document connects the four evidence items submitted for the LegalBot Municipal Part A investigation.

**Evidence 01 — Standing permission:** The agent configuration shows the permission that allows LegalBot to finalize a dismissal. This matters because the agent has authority to perform a sensitive municipal action without needing that authority for its normal support role.

**Evidence 02 — Goal hijack:** The malicious instruction is embedded in a citizen comment. This demonstrates the indirect prompt-injection path: content that should be treated as untrusted case data attempts to redirect the agent's goal.

**Evidence 03 — Privilege misuse:** This evidence is intended to show the sensitive dismissal action occurring without the required human approval. It connects the attempted goal hijack to the impact of excessive standing authority. Use a screenshot that actually shows the vulnerable action or its result; do not substitute an after-patch result for evidence of the vulnerable behavior.

**Evidence 04 — Semgrep:** The scan provides static-analysis evidence from the supplied fixture. It should be read alongside the configuration and behavior evidence, rather than treated by itself as proof that the attack succeeded or failed.

Together, the evidence traces the risk from the agent's standing permission, through the untrusted instruction, to the potential unauthorized action, with Semgrep providing a separate code-review signal. The investigation is a lab simulation and does not establish that a real municipal case was dismissed. This explanation is separate from the MAESTRO and NIST AI RMF mapping report submitted as Evidence 06.
