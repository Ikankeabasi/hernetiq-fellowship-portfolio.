# LegalBot Municipal — Part B Screenshot Evidence Guide

**Mission:** S26 — LegalBot Municipal: Fix the System + MAESTRO + NIST AI RMF  
**Domain:** Domain 5 — Autonomous Agent Governance  
**Purpose:** Use this guide to capture genuine after-patch evidence. This is a screenshot guide and caption sheet, not a substitute for the actual screenshots or runtime results.

## Before taking screenshots

1. Open the LegalBot Municipal Level 5 lab.
2. Confirm the visible status says **PATCHED**.
3. Capture the actual screen/result for each item below. Keep enough of the interface visible to identify LegalBot and the relevant configuration or result.
4. Do not use the Part A vulnerable screenshots as proof of Part B remediation.
5. Redact tokens, API keys, passwords, and other secrets.

## Screenshot 01 — Patched configuration

**Where to capture:** In the lab, open the **hardened configuration** tab/section. Capture the lines showing all four controls together:
- `CAN_FINALIZE_DISMISSAL = False`
- `REQUIRE_HUMAN_APPROVAL = True`
- `SANITIZE_CITIZEN_INPUT = True`
- `LOG_AGENT_ACTIONS = True`

**Caption to place under the screenshot:**

*Patched LegalBot configuration — standing dismissal authority is disabled, human approval is required, citizen input is handled as untrusted data, and agent-action logging is enabled.*

**What it demonstrates:** The intended remediation settings are present. A configuration screenshot alone does not prove that the runtime behavior changed; use the following screenshots for that.

**File suggestion:** `part-b-01-patched-configuration.png`

## Screenshot 02 — Untrusted citizen input

**Where to capture:** In the LegalBot Municipal interactive demo, show the case **CASE-2291** and the supplied citizen comment containing the “SYSTEM OVERRIDE” / supervisor-authorization instruction. If the lab visibly labels or wraps the comment as untrusted data, keep that label in the screenshot too.

**Caption to place under the screenshot:**

*Untrusted citizen content — the comment contains an instruction claiming supervisor authorization, but the comment itself is not proof of approval and must not authorize a case dismissal.*

**What it demonstrates:** The source of the goal-hijack attempt and why external case content must be separated from trusted instructions.

**File suggestion:** `part-b-02-untrusted-citizen-input.png`

## Screenshot 03 — Sensitive action blocked

**Where to capture:** With the patched status active, click **Ask LegalBot to Process This Case**. Capture the visible result that says the goal hijack was blocked and that the case was not closed.

**Caption to place under the screenshot:**

*Blocked direct action — after the patch, the malicious instruction does not directly dismiss CASE-2291. LegalBot reports that no case was closed.*

**What it demonstrates:** The sensitive action is not completed directly after the patch.

**File suggestion:** `part-b-03-action-blocked.png`

## Screenshot 04 — Human approval / pending state

**Where to capture:** Capture the actual screen showing the requested dismissal in a pending human-review or approval-queue state. Include the case ID and action/status if visible.

**Caption to place under the screenshot:**

*Human approval required — the requested sensitive action is routed for human review instead of being executed directly by the agent.*

**Important:** Only use this caption if the screenshot visibly shows a pending approval/review state. If the hosted lab only displays “Action queued for human review” and does not show a separate queue, capture that exact result and describe it accurately; do not invent a queue screen.

**File suggestion:** `part-b-04-pending-human-review.png`

## Screenshot 05 — Audit record

**Where to capture:** Capture the actual audit output showing a record for the request, ideally with the case ID, requested action, actor, and timestamp. Use the lab output or the prescribed test result where the record is actually displayed.

**Caption to place under the screenshot:**

*Audit record — the requested agent action is recorded so the event can be reviewed and investigated.*

**Important:** The code containing a logging function is not itself proof that an audit record was generated. If the hosted lab does not display a real record, do not present the code listing as a runtime log. Capture the available output and ask the tutor how they want the audit-record requirement evidenced.

**File suggestion:** `part-b-05-audit-record.png`

## Short explanation connecting the Part B screenshots

The patched configuration removes the agent's standing authority to dismiss cases, requires human approval, treats citizen comments as untrusted data, and enables action logging. The malicious comment screenshot shows the input that attempts to hijack the agent's goal. The blocked-action and pending-review evidence should show that this instruction cannot directly produce the sensitive action after remediation. The audit evidence should show that the request is recorded for accountability. Together, these checks address the original combination of goal hijack, excessive authority, missing approval, and weak observability.

## Submission reminder

- Put the five actual screenshots into the Part B evidence document with their matching captions.
- Submit the **Part B remediation report** separately from the Part A MAESTRO + NIST AI RMF mapping report.
- Do not claim a control was verified unless the screenshot or test result visibly supports the claim.
