# Personalized News Emailer

[![CI](https://github.com/Mirunjai/personalized-news-emailer/actions/workflows/ci.yml/badge.svg)](https://github.com/Mirunjai/personalized-news-emailer/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)
![Tests](https://img.shields.io/badge/tests-pytest-brightgreen)
![Lint](https://img.shields.io/badge/lint-flake8-informational)

A subscription service where users select news topics and receive a daily digest email (mocked) compiled from
selected news sources. It uses topic-preference storage, digest-generation jobs and email-templating stubs.

**Sprint 1 delivers:** subscription and preference management APIs, a mock news aggregator, a personalized feed
preview and a web dashboard, all protected by a CI pipeline (flake8 + pytest + coverage).

## Team 15

| Name | SRN | Role |
|------|-----|------|
| Mirunjai Suresh Kumar | PES1UG24AM161 | Repo Owner, CI/CD, Architecture and PR Reviews |
| Kota Videesha | PES1UG24AM140 | Database Schema and Preference CRUD APIs |
| Keerthishree R | PES1UG24AM132 | Mock News Aggregator Service and Frontend/UI Demo |
| Nayana S M | PES1UG24AM174 | Pre-Sprint Documentation (SRS, SAD, Test Plan) and Unit Testing |

## Architecture overview

A 3-tier modular architecture (full diagram in [docs/SAD_System_Design.md](docs/SAD_System_Design.md)):

1. **Presentation tier:** `app/templates/dashboard.html` (Tailwind CSS + vanilla JS).
2. **Application tier:** FastAPI routes in `app/main.py`, validation in `app/schemas.py`, news logic in `app/news_service.py`.
3. **Data tier:** SQLite (`app/database.py`) for users and topic preferences, plus `app/mock_news.json` as the news source.

```
personalized-news-emailer/
|-- .github/workflows/ci.yml
|-- app/
|   |-- main.py  database.py  models.py  schemas.py  news_service.py  mock_news.json
|   `-- templates/dashboard.html
|-- docs/  (SRS, SAD, Test Plan, Demo Script)
|-- tests/ (test_app.py, test_smoke.py)
|-- requirements.txt  .flake8  pytest.ini  .gitignore
```

## Setup

Requires Python 3.11+.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 for the dashboard and http://127.0.0.1:8000/docs for the interactive API docs.
The SQLite file `news_emailer.db` is created automatically (override the location with `NEWS_DB_PATH`).

## API documentation

| Method | Endpoint | Description | Success | Errors |
|--------|----------|-------------|---------|--------|
| GET | `/` | Dashboard UI | 200 | - |
| POST | `/api/subscribe` | Register email with initial topics | 201 | 400 duplicate, 422 invalid input |
| GET | `/api/preferences/{email}` | Get saved topics | 200 | 404 unknown user |
| PUT | `/api/preferences/{email}` | Replace saved topics | 200 | 404 unknown user, 422 invalid topic |
| GET | `/api/news?topic=technology` | Filter news by one or more (comma-separated) topics | 200 | 400 invalid topic |
| GET | `/api/news?email=user@example.com` | Personalized feed from saved topics | 200 | 404 unknown user |

Valid topics: `technology`, `finance`, `sports`, `health`, `science`.

Example:

```bash
curl -X POST http://127.0.0.1:8000/api/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "topics": ["technology", "science"]}'

curl "http://127.0.0.1:8000/api/news?email=user@example.com"
```

## Running tests and linting

```bash
flake8 .
pytest --cov=app --cov-report=term-missing
```

## Documentation

- [Software Requirements Specification](docs/SRS_Requirement_Analysis.md)
- [System Architecture Document](docs/SAD_System_Design.md)
- [Test Plan](docs/Test_Plan.md)
- [Sprint 1 Demo Script](docs/Sprint1_Demo_Script.md)

## Branching and workflow

`main` is protected by CI. Work happens on feature branches (`feature/docs-and-tests`,
`feature/db-and-preference-api`, `feature/news-service-and-ui`) and is merged through reviewed pull requests.
