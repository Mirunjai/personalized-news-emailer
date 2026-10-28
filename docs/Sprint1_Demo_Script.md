# Sprint 1 Demo Script (about 1 minute)

Goal: record the mandatory Sprint 1 working-product video. Screen-record the terminal and the browser together.

## Pre-recording checklist
- [ ] Virtual environment is active and dependencies installed (`pip install -r requirements.txt`)
- [ ] Old database removed so the demo starts clean: `rm -f news_emailer.db`
- [ ] Browser zoom around 110%, notifications off, terminal font large
- [ ] CI badge / Actions tab open in another tab (optional closing shot)

## Commands
```bash
uvicorn app.main:app --reload                       # terminal 1: start the app
flake8 . && pytest --cov=app                        # terminal 2: lint and tests
curl "http://127.0.0.1:8000/api/news?topic=science" # optional API proof
```

## Timed script

| Time | Screen | Say / do |
|------|--------|----------|
| 0:00-0:07 | Title | "We are Team 15. This is Sprint 1 of the Personalized News Emailer." |
| 0:07-0:15 | Terminal | Run `uvicorn app.main:app --reload`. "The FastAPI service starts and creates the SQLite tables." |
| 0:15-0:25 | Browser at http://127.0.0.1:8000 | Enter `demo@example.com`, tick Technology, Science and Health. Click **Save Preferences**. "Preferences are stored through our subscribe API." |
| 0:25-0:40 | Browser | Click **Preview My Personalized Feed**. "The feed shows mock articles that match only the topics we selected." Scroll briefly. |
| 0:40-0:48 | Browser | Untick Health, tick Finance, click **Save Preferences** then **Preview** again. "Updating preferences changes the feed immediately." |
| 0:48-0:55 | Terminal 2 | Run `flake8 . && pytest --cov=app`. "Linting is clean and all tests pass." |
| 0:55-1:00 | GitHub Actions tab | "The same checks run in our GitHub Actions CI on every push and pull request. Thank you." |

## Backup plan
If the browser misbehaves, open http://127.0.0.1:8000/docs and run `POST /api/subscribe`, then
`GET /api/news?email=demo@example.com` from Swagger UI.
