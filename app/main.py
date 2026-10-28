"""FastAPI application: dashboard UI plus subscription, preference and news APIs."""
from contextlib import asynccontextmanager
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse

from app import database, news_service
from app.models import VALID_TOPICS, DuplicateUserError, UserRecord
from app.schemas import NewsArticle, PreferenceUpdate, SubscriptionCreate, UserResponse, normalize_email

DASHBOARD_FILE = Path(__file__).resolve().parent / "templates" / "dashboard.html"


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Create database tables on startup."""
    database.init_db()
    yield


app = FastAPI(
    title="Personalized News Emailer",
    description="Sprint 1: topic preference storage and mock news preview.",
    version="1.0.0",
    lifespan=lifespan,
)


def _to_response(record: UserRecord) -> UserResponse:
    return UserResponse(email=record.email, topics=record.topics, created_at=record.created_at)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def dashboard() -> HTMLResponse:
    """Serve the single-page dashboard."""
    return HTMLResponse(DASHBOARD_FILE.read_text(encoding="utf-8"))


@app.post("/api/subscribe", response_model=UserResponse, status_code=201)
def subscribe(payload: SubscriptionCreate) -> UserResponse:
    """Register a new email address with its initial topics."""
    try:
        record = database.create_user(payload.email, payload.topics)
    except DuplicateUserError:
        raise HTTPException(status_code=400, detail="Email already subscribed")
    return _to_response(record)


@app.get("/api/preferences/{email}", response_model=UserResponse)
def get_preferences(email: str) -> UserResponse:
    """Return the saved topics for a user."""
    record = database.get_user(normalize_email(email))
    if record is None:
        raise HTTPException(status_code=404, detail="User not found")
    return _to_response(record)


@app.put("/api/preferences/{email}", response_model=UserResponse)
def update_preferences(email: str, payload: PreferenceUpdate) -> UserResponse:
    """Replace the saved topics of an existing user."""
    record = database.update_topics(normalize_email(email), payload.topics)
    if record is None:
        raise HTTPException(status_code=404, detail="User not found")
    return _to_response(record)


@app.get("/api/news", response_model=List[NewsArticle])
def get_news(
    topic: Optional[str] = Query(None, description="One topic or a comma-separated list of topics"),
    email: Optional[str] = Query(None, description="Return the personalized feed for this subscriber"),
) -> List[dict]:
    """Return mock news filtered by topic(s) or personalized for a subscriber."""
    if email:
        record = database.get_user(normalize_email(email))
        if record is None:
            raise HTTPException(status_code=404, detail="User not found")
        return news_service.personalized_feed(record.topics)
    if topic:
        topics = news_service.parse_topics(topic)
        invalid = [item for item in topics if item not in VALID_TOPICS]
        if invalid or not topics:
            message = "Invalid topic(s): " + ", ".join(invalid) + ". Allowed: " + ", ".join(VALID_TOPICS)
            raise HTTPException(status_code=400, detail=message)
        return news_service.filter_by_topics(topics)
    return news_service.get_all_articles()
