"""
Twilio WhatsApp auto-responder logic.

Flow:
  1. User texts a project code (e.g. "Project 102", "P2", "status")
  2. Bot replies with the scripted prompt asking for a status update
  3. User replies with "1", "2", or "3"
  4. Bot logs the status report and confirms receipt

TwiML (Twilio Markup Language) is returned as XML so Twilio knows
what to say/send back to the user.
"""
from __future__ import annotations

import json
import os
import re
import uuid
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Project code parsing helpers
# ---------------------------------------------------------------------------

# Recognise patterns like: "Project 102", "P102", "project1", "#2", "2"
_PROJECT_CODE_PATTERN = re.compile(
    r"(?:project\s*#?|p#?)(\d+)|^#?(\d+)$",
    re.IGNORECASE,
)

# Recognise a status reply: "1", "2", "3" (optionally with period or dot)
_STATUS_REPLY_PATTERN = re.compile(r"^([123])\.?$")

# Map status number → human-readable label
STATUS_MAP = {
    "1": "Active",
    "2": "Abandoned",
    "3": "Completed",
}

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
REPORTS_PATH = os.path.join(BASE_DIR, "data", "reports.json")


# ---------------------------------------------------------------------------
# Core parsing + response builders
# ---------------------------------------------------------------------------

def parse_message(body: str) -> dict:
    """
    Parse an inbound WhatsApp message body.

    Returns a dict with keys:
      - intent: "project_query" | "status_reply" | "unknown"
      - project_id: int | None
      - status_digit: str | None  ("1", "2", or "3")
    """
    body = body.strip()

    # Check for status reply first (short single-digit messages)
    status_match = _STATUS_REPLY_PATTERN.match(body)
    if status_match:
        return {"intent": "status_reply", "project_id": None, "status_digit": status_match.group(1)}

    # Check for project code mention
    code_match = _PROJECT_CODE_PATTERN.search(body)
    if code_match:
        raw_id = code_match.group(1) or code_match.group(2)
        return {"intent": "project_query", "project_id": int(raw_id), "status_digit": None}

    return {"intent": "unknown", "project_id": None, "status_digit": None}


def build_twiml_response(message: str) -> str:
    """Wrap a plain-text message in a TwiML <Response><Message> envelope."""
    # Escape XML special characters
    safe = message.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        "<Response>"
        f"<Message>{safe}</Message>"
        "</Response>"
    )


# ---------------------------------------------------------------------------
# Main handler — called from the webhook route
# ---------------------------------------------------------------------------

def handle_inbound_message(body: str, from_number: str) -> str:
    """
    Process an inbound WhatsApp message and return TwiML XML.

    Args:
        body:        The raw text of the incoming message.
        from_number: The sender's WhatsApp number (e.g. "whatsapp:+2348012345678").

    Returns:
        TwiML XML string to send back to Twilio.
    """
    parsed = parse_message(body)
    intent = parsed["intent"]

    # --- Intent: user mentioned a project code ---
    if intent == "project_query":
        reply = (
            "👋 Welcome to the COUCH Infrastructure Tracker!\n\n"
            f"You're checking on Project {parsed['project_id']}.\n\n"
            "Please upload a photo of the site OR reply with the current status:\n"
            "1️⃣  Active — work is ongoing\n"
            "2️⃣  Abandoned — no activity visible\n"
            "3️⃣  Completed — project is finished\n\n"
            "Reply with 1, 2, or 3."
        )
        return build_twiml_response(reply)

    # --- Intent: user replied with a status digit ---
    if intent == "status_reply":
        digit = parsed["status_digit"]
        status_label = STATUS_MAP[digit]
        _log_whatsapp_report(from_number, status_label)
        reply = (
            f"✅ Report received! Status '{status_label}' has been logged.\n\n"
            "Thank you for helping track this project. Your report contributes to "
            "COUCH's real-time governance data.\n\n"
            "🔗 View the dashboard: https://couch-tracker.onrender.com"
        )
        return build_twiml_response(reply)

    # --- Unknown / unrecognised message ---
    reply = (
        "👋 Hi! I'm the COUCH Infrastructure Tracker bot.\n\n"
        "To check on a project, send a message like:\n"
        "   'Project 102' or 'P1'\n\n"
        "I'll ask you to confirm its current status. Together we keep "
        "government projects accountable. 🇳🇬"
    )
    return build_twiml_response(reply)


# ---------------------------------------------------------------------------
# Private: log a WhatsApp-sourced report to disk
# ---------------------------------------------------------------------------

def _log_whatsapp_report(from_number: str, status_label: str) -> None:
    """Append a new WhatsApp-sourced community report to reports.json."""
    try:
        with open(REPORTS_PATH, "r", encoding="utf-8") as f:
            reports = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        reports = []

    new_report = {
        "id": str(uuid.uuid4()),
        "project_id": None,  # Could be enhanced to track state per conversation
        "source": "whatsapp",
        "from_number": from_number,
        "status_reported": status_label,
        "message": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    reports.append(new_report)

    with open(REPORTS_PATH, "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=2, ensure_ascii=False)
