"""Sprint 2 digest, template, mock sender and history regression tests."""
import json

import pytest
from fastapi.testclient import TestClient

from app import database, digest_job, email_sender, email_template
from app.main import app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("NEWS_DB_PATH", str(tmp_path / "digest.db"))
    monkeypatch.setenv("NEWS_EMAIL_OUTBOX", str(tmp_path / "outbox.jsonl"))
    with TestClient(app) as test_client:
        yield test_client


def add_subscriber(email, topics):
    database.create_user(email, topics)


def test_template_renders_html_and_text_with_escaped_values():
    articles = [{
        "title": "<script>alert(1)</script>",
        "summary": "A & B",
        "source": "Demo",
        "topic": "technology",
    }]
    subject, html_body, text_body = email_template.render_digest(
        "a@example.com", articles, "2026-11-11T09:00:00+00:00"
    )
    assert "2026-11-11" in subject
    assert "&lt;script&gt;" in html_body
    assert "<script>" not in html_body
    assert "A & B" in text_body


def test_mock_sender_writes_local_outbox(tmp_path, monkeypatch):
    path = tmp_path / "outbox.jsonl"
    monkeypatch.setenv("NEWS_EMAIL_OUTBOX", str(path))
    result = email_sender.send_mock_email(
        "a@example.com", "Subject", "<p>Hi</p>", "Hi", "run-1"
    )
    message = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
    assert result["delivery"] == "mocked"
    assert message["recipient"] == "a@example.com"
    assert message["html_body"] == "<p>Hi</p>"
    assert message["text_body"] == "Hi"


def test_digest_generates_personalized_outbox_and_history(client, tmp_path):
    add_subscriber("tech@example.com", ["technology"])
    add_subscriber("finance@example.com", ["finance"])
    summary = digest_job.run_digest_job()
    assert summary["total"] == 2
    assert summary["sent"] == 2
    messages = [
        json.loads(line)
        for line in (tmp_path / "outbox.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert len(messages) == 2
    assert {item["recipient"] for item in messages} == {
        "tech@example.com", "finance@example.com"
    }
    history = database.get_digest_history()
    assert len(history) == 2
    assert all(item["status"] == "sent" for item in history)


def test_empty_digest_is_recorded_and_does_not_stop_other_subscribers(
    client, monkeypatch
):
    add_subscriber("empty@example.com", ["science"])
    add_subscriber("normal@example.com", ["technology"])
    original = __import__("app.digest_job", fromlist=["x"]).news_service.personalized_feed

    def controlled_feed(topics):
        if topics == ["science"]:
            return []
        return original(topics)

    monkeypatch.setattr("app.digest_job.news_service.personalized_feed", controlled_feed)
    summary = digest_job.run_digest_job()
    assert summary["no_articles"] == 1
    assert summary["sent"] == 1
    statuses = {item["subscriber_email"]: item["status"] for item in database.get_digest_history()}
    assert statuses == {"normal@example.com": "sent", "empty@example.com": "no_articles"}


def test_subscriber_failure_isolated_and_logged(client, monkeypatch):
    add_subscriber("bad@example.com", ["technology"])
    add_subscriber("good@example.com", ["finance"])
    original = digest_job.news_service.personalized_feed

    def controlled_feed(topics):
        if topics == ["technology"]:
            raise RuntimeError("simulated source failure")
        return original(topics)

    monkeypatch.setattr("app.digest_job.news_service.personalized_feed", controlled_feed)
    summary = digest_job.run_digest_job()
    assert summary["failed"] == 1
    assert summary["sent"] == 1
    history = database.get_digest_history()
    assert any(item["status"] == "failed" for item in history)


def test_digest_api_run_and_history(client):
    add_subscriber("api@example.com", ["sports"])
    response = client.post("/api/digest/run")
    assert response.status_code == 200
    assert response.json()["sent"] == 1
    history = client.get("/api/digest/history")
    assert history.status_code == 200
    assert history.json()[0]["subscriber_email"] == "api@example.com"


def test_history_limit_is_bounded(client):
    add_subscriber("limit@example.com", ["health"])
    digest_job.run_digest_job()
    response = client.get("/api/digest/history?limit=9999")
    assert response.status_code == 200
    assert len(response.json()) <= 500
