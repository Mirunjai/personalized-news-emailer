"""Pydantic request/response schemas."""
import re
from typing import List

from pydantic import BaseModel, Field, field_validator

from app.models import VALID_TOPICS

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def normalize_email(email: str) -> str:
    """Trim whitespace and lowercase an email address."""
    return email.strip().lower()


def clean_topics(topics: List[str]) -> List[str]:
    """Normalise topics, drop duplicates (keeping order) and reject unknown values."""
    cleaned: List[str] = []
    for raw in topics:
        topic = raw.strip().lower()
        if topic not in VALID_TOPICS:
            raise ValueError("Invalid topic '" + raw + "'. Allowed topics: " + ", ".join(VALID_TOPICS))
        if topic not in cleaned:
            cleaned.append(topic)
    if not cleaned:
        raise ValueError("At least one topic is required")
    return cleaned


class SubscriptionCreate(BaseModel):
    """Payload for POST /api/subscribe."""

    email: str = Field(..., examples=["user@example.com"])
    topics: List[str] = Field(..., min_length=1, examples=[["technology", "science"]])

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        email = normalize_email(value)
        if not EMAIL_PATTERN.match(email):
            raise ValueError("Invalid email address")
        return email

    @field_validator("topics")
    @classmethod
    def validate_topics(cls, value: List[str]) -> List[str]:
        return clean_topics(value)


class PreferenceUpdate(BaseModel):
    """Payload for PUT /api/preferences/{email}."""

    topics: List[str] = Field(..., min_length=1, examples=[["finance", "health"]])

    @field_validator("topics")
    @classmethod
    def validate_topics(cls, value: List[str]) -> List[str]:
        return clean_topics(value)


class UserResponse(BaseModel):
    """A subscribed user and their saved topics."""

    email: str
    topics: List[str]
    created_at: str


class NewsArticle(BaseModel):
    """A single mock news article."""

    id: int
    title: str
    source: str
    topic: str
    summary: str
    published_at: str
