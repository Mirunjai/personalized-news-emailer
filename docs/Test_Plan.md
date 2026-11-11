# Test Plan — Sprint 1 and Sprint 2

## Test strategy

- Unit tests: template escaping and mock sender output.
- Integration tests: FastAPI endpoints and SQLite persistence with a temporary database.
- Digest workflow tests: multiple subscribers, empty results and per-subscriber failure isolation.
- Static analysis: Flake8 (120-character line limit).
- Coverage: pytest-cov.

## Commands

```bash
flake8 .
pytest --cov=app --cov-report=term-missing
```

## Sprint 1

The existing `tests/test_app.py` covers subscription, duplicate email rejection, preference CRUD, topic filtering, personalized feed, invalid inputs and dashboard delivery.

## Sprint 2 cases

| ID | Scenario | Expected |
|---|---|---|
| DG-01 | Two subscribers with different topics | Each local message contains only the subscriber's matching articles |
| DG-02 | Subscriber has no matching articles | `no_articles` outcome is recorded; remaining subscribers still process |
| DG-03 | Trigger digest through API | Summary includes run ID and per-subscriber results |
| EM-01 | Render digest containing HTML-sensitive values | HTML is escaped; text version contains readable content |
| EM-02 | Mock sender dispatch | JSONL outbox receives recipient, subject and both bodies; no network request |
| DH-01 | Read recent history | Sent, empty and failed results persist in SQLite |
| REG-01 | Run full suite and lint | Flake8 and pytest pass on integrated branch |

Each test uses an isolated `NEWS_DB_PATH` and `NEWS_EMAIL_OUTBOX`. The mock sender is local-only and does not require credentials or external services.
