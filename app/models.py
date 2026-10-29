"""Domain models and constants shared across the application."""
from dataclasses import dataclass, field
from typing import List

VALID_TOPICS = ("technology", "finance", "sports", "health", "science")


class DuplicateUserError(Exception):
    """Raised when an email address is already subscribed."""

    def __init__(self, email: str):
        super().__init__("Email already subscribed: " + email)
        self.email = email


@dataclass
class UserRecord:
    """A subscribed user together with the topics they selected."""

    email: str
    created_at: str
    topics: List[str] = field(default_factory=list)
