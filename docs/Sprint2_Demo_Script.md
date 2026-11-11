# Sprint 2 Demo Script (2 minutes)

Record this after running the app and tests on the final integrated commit. This script is not itself a video recording.

| Time | Action | What to explain |
|---|---|---|
| 0:00–0:15 | Open dashboard and API docs | Team 15 project and topic-based subscriptions |
| 0:15–0:35 | Show two subscribers with different topics | Preferences are stored independently in SQLite |
| 0:35–0:55 | POST /api/digest/run | One run processes each subscriber's matching articles |
| 0:55–1:15 | Open mock_email_outbox.jsonl | HTML/text content is written locally; no real email is sent |
| 1:15–1:35 | GET /api/digest/history | Show sent, no_articles and failed outcomes (prepare a test failure/empty case) |
| 1:35–1:50 | Run flake8 and pytest | Show lint and regression tests |
| 1:50–2:00 | Show GitHub Actions | Point to CI for the same commit |

Before recording: use synthetic email addresses, a clean database, and a clean outbox. Save the actual MP4 or instructor-approved link in the repository. Do not claim a recording exists until it is uploaded.
