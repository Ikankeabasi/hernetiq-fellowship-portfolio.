"""
from datetime import datetime, timezone
from typing import Any

CAN_FINALIZE_DISMISSAL = False
REQUIRE_HUMAN_APPROVAL = True
SANITIZE_CITIZEN_INPUT = True
LOG_AGENT_ACTIONS = True


def sanitize_citizen_input(raw_comment: str) -> dict[str, Any]:
    """Keep citizen text as untrusted data, not executable instructions."""
    if not isinstance(raw_comment, str):
        raise TypeError("Citizen comment must be text.")
    return {
        "content": raw_comment,
        "role": "untrusted_data",
        "instructable": False,
    }


def make_audit_record(case_id: str, action: str, actor: str) -> dict[str, str]:
    """Return a timestamped audit event; production should persist it securely."""
    return {
        "case_id": case_id,
        "action": action,
        "actor": actor,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def request_case_disposition(
    case_id: str, citizen_comment: str, requested_action: str
) -> dict[str, Any]:
    """Never finalize a sensitive disposition directly from agent reasoning."""
    if not CAN_FINALIZE_DISMISSAL:
        if not REQUIRE_HUMAN_APPROVAL:
            raise RuntimeError("Sensitive actions must require human approval.")

        safe_comment = sanitize_citizen_input(citizen_comment)
        result = {
            "status": "pending_human_review",
            "case_id": case_id,
            "requested_action": requested_action,
            "citizen_comment": safe_comment,
            "executed": False,
        }
        if LOG_AGENT_ACTIONS:
            result["audit_record"] = make_audit_record(
                case_id, f"queued_for_approval:{requested_action}", "legalbot"
            )
        return result

    # Fail closed: this agent is never allowed to finalize dismissals directly.
    raise PermissionError(
        "Direct case disposition is disabled; use the authorized human workflow."
    )
