# Personalized News Emailer

A college software-engineering project that lets subscribers choose news topics, preview a personalized feed, and run a daily mock email digest.

## Features

- Subscribe and update topic preferences (SQLite).
- Browse a mock news feed filtered by topic.
- Generate an individual digest for every subscriber.
- Render HTML and plain-text email content.
- Save mock messages to a local JSON Lines outbox (no real email is sent).
- Record sent, no-article and failed outcomes in SQLite.
- Trigger a digest manually through the API or CLI; schedule the CLI command daily using the operating system scheduler.

## Setup

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Dashboard: http://127.0.0.1:8000  
Swagger API: http://127.0.0.1:8000/docs

The database defaults to `news_emailer.db`. Set `NEWS_DB_PATH` to use another SQLite file.
The mock outbox defaults to `mock_email_outbox.jsonl`; set `NEWS_EMAIL_OUTBOX` to change it.

## API

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/subscribe` | Register subscriber and topics |
| GET | `/api/preferences/{email}` | Read preferences |
| PUT | `/api/preferences/{email}` | Replace preferences |
| GET | `/api/news?topic=technology,finance` | Filter mock news |
| GET | `/api/news?email=user@example.com` | Preview personalized feed |
| POST | `/api/digest/run` | Run one digest cycle now |
| GET | `/api/digest/history?limit=50` | Read recent digest outcomes |

Example:
```bash
curl -X POST http://127.0.0.1:8000/api/digest/run
curl "http://127.0.0.1:8000/api/digest/history?limit=20"
```

## Run the digest manually or daily

```bash
python -m app.digest_job
```

For a daily run, schedule that command at the desired time with the OS scheduler:
- Linux/macOS cron example (runs daily at 08:00): `0 8 * * * cd /path/to/personalized-news-emailer && /path/to/python -m app.digest_job`
- Windows: create a daily Task Scheduler task that runs `python -m app.digest_job` with the repository as its working directory.

The project deliberately uses OS scheduling rather than an always-running scheduler dependency. Configure the database and outbox paths in the task's environment if needed.

## Tests and lint

```bash
flake8 .
pytest --cov=app --cov-report=term-missing
```

## Team 15

| Member | SRN | Responsibility |
|---|---|---|
| Mirunjai Suresh Kumar | PES1UG24AM161 | Repository, CI/CD, architecture and reviews |
| Kota Videesha | PES1UG24AM140 | Database and preference APIs |
| Keerthishree R | PES1UG24AM132 | News service, digest and UI |
| Nayana S M | PES1UG24AM174 | Documentation and tests |

## Documentation

- `docs/SRS_Requirement_Analysis.md`
- `docs/SAD_System_Design.md`
- `docs/Test_Plan.md`
- `docs/Sprint1_Demo_Script.md`
- `docs/Sprint2_Demo_Script.md`
- `docs/Sprint2_Presentation_Outline.md`
- `docs/SPRINT_TRACKING.md`

**Demo safety:** the sender only appends to a local JSONL file. It never sends email over SMTP or an external API.
