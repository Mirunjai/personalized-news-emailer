"""Local mock email sender. This module never connects to SMTP or the internet."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict


def get_outbox_path() -> Path:
    """Return the JSONL outbox path, overridable for tests and demos."""
    return Path(os.environ.get("NEWS_EMAIL_OUTBOX", "mock_email_outbox.jsonl"))


def send_mock_email(
    recipient: str,
    subject: str,
    html_body: str,
    text_body: str,
    run_id: str,
) -> Dict:
    """Append one rendered message to a local JSONL file and return its metadata."""
    message = {
        "recipient": recipient,
        "subject": subject,
        "html_body": html_body,
        "text_body": text_body,
        "run_id": run_id,
        "sent_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "delivery": "mocked",
    }
    path = get_outbox_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(message, ensure_ascii=False) + "\n")
    return {"recipient": recipient, "subject": subject, "delivery": "mocked"}
