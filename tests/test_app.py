"""Sprint 1 test suite covering TC-01 to TC-06 (see docs/Test_Plan.md)."""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    """TestClient backed by an isolated temporary SQLite database."""
    monkeypatch.setenv("NEWS_DB_PATH", str(tmp_path / "test_news.db"))
    with TestClient(app) as test_client:
        yield test_client


def subscribe(client, email="alice@example.com", topics=None):
    payload = {"email": email, "topics": topics or ["technology", "finance"]}
    return client.post("/api/subscribe", json=payload)


def test_tc01_valid_subscription(client):
    response = subscribe(client)
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "alice@example.com"
    assert body["topics"] == ["technology", "finance"]
    assert body["created_at"]


def test_tc01_email_is_normalised(client):
    response = subscribe(client, email="  Alice@Example.COM ")
    assert response.status_code == 201
    assert response.json()["email"] == "alice@example.com"


def test_tc02_duplicate_email_rejected(client):
    assert subscribe(client).status_code == 201
    response = subscribe(client, topics=["sports"])
    assert response.status_code == 400
    assert "already subscribed" in response.json()["detail"]


def test_tc03_update_preferences(client):
    subscribe(client)
    response = client.put("/api/preferences/alice@example.com", json={"topics": ["health", "science"]})
    assert response.status_code == 200
    assert response.json()["topics"] == ["health", "science"]
    stored = client.get("/api/preferences/alice@example.com").json()
    assert stored["topics"] == ["health", "science"]


def test_tc03_update_unknown_user_returns_404(client):
    response = client.put("/api/preferences/ghost@example.com", json={"topics": ["sports"]})
    assert response.status_code == 404


def test_tc04_retrieve_preferences(client):
    subscribe(client, topics=["sports", "science"])
    response = client.get("/api/preferences/alice@example.com")
    assert response.status_code == 200
    assert response.json()["topics"] == ["sports", "science"]


def test_tc04_retrieve_unknown_user_returns_404(client):
    response = client.get("/api/preferences/nobody@example.com")
    assert response.status_code == 404


def test_tc05_filter_news_by_single_topic(client):
    response = client.get("/api/news", params={"topic": "technology"})
    assert response.status_code == 200
    articles = response.json()
    assert len(articles) == 4
    assert all(article["topic"] == "technology" for article in articles)


def test_tc05_filter_news_by_multiple_topics(client):
    response = client.get("/api/news", params={"topic": "finance,sports"})
    assert response.status_code == 200
    topics = {article["topic"] for article in response.json()}
    assert topics == {"finance", "sports"}


def test_tc05_personalized_feed_matches_saved_topics(client):
    subscribe(client, topics=["health", "science"])
    response = client.get("/api/news", params={"email": "alice@example.com"})
    assert response.status_code == 200
    articles = response.json()
    assert len(articles) == 8
    assert {article["topic"] for article in articles} == {"health", "science"}


def test_tc05_personalized_feed_unknown_user_returns_404(client):
    response = client.get("/api/news", params={"email": "nobody@example.com"})
    assert response.status_code == 404


def test_tc05_all_news_without_filters(client):
    response = client.get("/api/news")
    assert response.status_code == 200
    assert len(response.json()) == 20


def test_tc06_invalid_topic_on_subscribe_rejected(client):
    response = subscribe(client, topics=["cooking"])
    assert response.status_code == 422


def test_tc06_invalid_topic_on_update_rejected(client):
    subscribe(client)
    response = client.put("/api/preferences/alice@example.com", json={"topics": ["politics"]})
    assert response.status_code == 422


def test_tc06_invalid_topic_in_news_filter_returns_400(client):
    response = client.get("/api/news", params={"topic": "cooking"})
    assert response.status_code == 400
    assert "Invalid topic" in response.json()["detail"]


def test_invalid_email_rejected(client):
    response = subscribe(client, email="not-an-email")
    assert response.status_code == 422


def test_dashboard_is_served(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Preview My Personalized Feed" in response.text
