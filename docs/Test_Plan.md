# Test Plan

**Project:** Personalized News Emailer | **Version:** 1.0 (Sprint 1) | **Team:** 15

| Name | SRN | Role |
|------|-----|------|
| Mirunjai Suresh Kumar | PES1UG24AM161 | CI/CD and PR reviews |
| Kota Videesha | PES1UG24AM140 | Database and API owner |
| Keerthishree R | PES1UG24AM132 | News service and UI owner |
| Nayana S M | PES1UG24AM174 | Test lead |

## 1. Objectives
Verify that subscription, preference management and news filtering behave as specified in the SRS, and that regressions
are caught automatically before code reaches `main`.

## 2. Scope
**In scope (Sprint 1):** `/api/subscribe`, `/api/preferences/{email}`, `/api/news`, input validation, SQLite persistence,
dashboard delivery (`/`).
**Out of scope:** digest jobs and email stubs (Sprint 2), load testing, browser compatibility testing.

## 3. Test Strategy
| Level | Approach | Tooling |
|-------|----------|---------|
| Unit | Validation rules, news filtering and database helpers exercised through their public functions | Pytest |
| Integration | Full request/response cycle through FastAPI against an isolated SQLite database | Pytest + FastAPI `TestClient` (httpx) |
| Static analysis | PEP 8 compliance, max line length 120 | Flake8 |
| Coverage | Statement coverage of the `app` package | pytest-cov |
| Continuous integration | Lint and tests on every push and pull request to `main` | GitHub Actions |
| Manual / demo | Dashboard walkthrough per `docs/Sprint1_Demo_Script.md` | Browser |

Each test gets a fresh temporary database through the `NEWS_DB_PATH` environment variable, so tests are independent and
repeatable.

## 4. Test Environment
| Item | Value |
|------|-------|
| OS | Ubuntu (GitHub Actions) and developer machines (Windows/macOS/Linux) |
| Python | 3.11 |
| Dependencies | Pinned in `requirements.txt` |
| Database | Temporary SQLite file per test |
| CI trigger | `push` and `pull_request` on `main` |

## 5. Entry and Exit Criteria
- **Entry:** code compiles, dependencies install, feature branch pushed.
- **Exit:** flake8 reports zero violations, all tests pass, and every TC below passes.

## 6. Test Cases

| ID | Requirement | Description | Steps | Expected result | Automated test |
|----|-------------|-------------|-------|-----------------|----------------|
| TC-01 | FR-01.1 | Valid subscription | POST `/api/subscribe` with a valid email and topics `["technology", "finance"]` | 201; response contains the email, topics and `created_at`; email is lowercased | `test_tc01_valid_subscription`, `test_tc01_email_is_normalised` |
| TC-02 | FR-01.2 | Duplicate email rejection | Subscribe twice with the same email | First 201; second 400 with "already subscribed" | `test_tc02_duplicate_email_rejected` |
| TC-03 | FR-01.5 | Update preferences | Subscribe, then PUT `/api/preferences/{email}` with new topics; unknown user case | 200 with new topics and GET reflects them; unknown user 404 | `test_tc03_update_preferences`, `test_tc03_update_unknown_user_returns_404` |
| TC-04 | FR-01.4 | Retrieve preferences | Subscribe, then GET `/api/preferences/{email}`; unknown user case | 200 with saved topics in order; unknown user 404 | `test_tc04_retrieve_preferences`, `test_tc04_retrieve_unknown_user_returns_404` |
| TC-05 | FR-02.2, FR-02.3 | Filter mock news by topic | GET `/api/news?topic=technology`; multiple topics; `?email=` personalized feed | Only matching topics returned (4 per topic); personalized feed matches saved topics; unknown email 404 | `test_tc05_*` |
| TC-06 | FR-01.3, FR-02.4 | Invalid topic handling | Subscribe or update with `cooking`/`politics`; GET `/api/news?topic=cooking` | Subscribe/update 422; news filter 400 with "Invalid topic" | `test_tc06_*` |

Additional tests: invalid email format returns 422; dashboard `/` returns HTML containing the preview button; smoke
test confirms the package imports.

## 7. Defect Handling
Failures are reported as GitHub issues with steps to reproduce, expected and actual results. A fix is made on a feature
branch and merged through a reviewed pull request; the CI pipeline must be green before merge.

## 8. Roles
| Activity | Owner |
|----------|-------|
| Test plan and automated tests | Nayana S M |
| API and database test support | Kota Videesha |
| News service and UI verification | Keerthishree R |
| CI pipeline and merge gating | Mirunjai Suresh Kumar |

## 9. How to Run
```bash
flake8 .
pytest --cov=app --cov-report=term-missing
```
