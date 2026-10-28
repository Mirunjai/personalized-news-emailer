# Software Requirements Specification (SRS)

**Project:** Personalized News Emailer
**Version:** 1.0 (Sprint 1)
**Team:** Team 15

## Team 15 Members

| Name | SRN | Responsibility |
|------|-----|----------------|
| Mirunjai Suresh Kumar | PES1UG24AM161 | Repo Owner, CI/CD, Architecture and PR Reviews |
| Kota Videesha | PES1UG24AM140 | Database Schema and Preference CRUD APIs |
| Keerthishree R | PES1UG24AM132 | Mock News Aggregator Service and Frontend/UI Demo |
| Nayana S M | PES1UG24AM174 | Pre-Sprint Documentation (SRS, SAD, Test Plan) and Unit Testing |

## 1. Introduction

### 1.1 Purpose
This document specifies the requirements of the Personalized News Emailer, a subscription service in which users select
the news topics they care about and receive a daily digest email compiled from selected news sources.

### 1.2 Scope
The system lets a user subscribe with an email address and a set of topics, change those topics later, preview the
personalized feed, and (from Sprint 2) have a scheduled job compile and "send" a daily digest. Delivery is **mocked**:
emails are rendered through templating stubs and logged rather than sent through a real SMTP provider. News content comes
from a local mock dataset behind a service interface so a real news API can replace it later.

### 1.3 Definitions
| Term | Meaning |
|------|---------|
| Topic | One of `technology`, `finance`, `sports`, `health`, `science` |
| Digest | A compilation of articles matching a user's topics |
| Subscriber | A user registered with an email address and at least one topic |
| Mock news source | The JSON dataset (`app/mock_news.json`) that simulates a news API |

### 1.4 Technology Stack
Python 3.11, FastAPI, SQLite (`sqlite3`), Pydantic, HTML + Tailwind CSS + JavaScript, Pytest, Flake8, GitHub Actions.

## 2. Overall Description

### 2.1 Product Perspective
A standalone web application with a browser dashboard, a REST API, a SQLite database and a mock news provider.

### 2.2 User Classes
| User class | Description | Interaction |
|------------|-------------|-------------|
| Subscriber | End user who wants a tailored daily news digest | Dashboard and REST API: subscribe, update topics, preview feed |
| Administrator / Developer | Team member who runs and maintains the service | API docs, CI pipeline, logs, test suite |
| Scheduler (system actor) | Background job runner (Sprint 2) | Triggers digest generation and the email stub |

### 2.3 Operating Environment
Any OS with Python 3.11+ and a modern browser. CI runs on GitHub-hosted Ubuntu runners.

### 2.4 Assumptions and Constraints
- Email delivery is mocked; no real emails are sent.
- News data is static mock data in Sprint 1.
- One preference set per email address; no authentication in Sprint 1.

## 3. Functional Requirements

### FR-01: User and Topic Preferences
| ID | Requirement | Priority | Sprint |
|----|-------------|----------|--------|
| FR-01.1 | The system shall allow a user to subscribe with a valid email address and one or more valid topics. | High | 1 |
| FR-01.2 | The system shall reject a subscription whose email is already registered (HTTP 400). | High | 1 |
| FR-01.3 | The system shall reject invalid email formats and unknown topics (HTTP 422). | High | 1 |
| FR-01.4 | The system shall return a subscriber's saved topics, or HTTP 404 if the user does not exist. | High | 1 |
| FR-01.5 | The system shall let a subscriber replace their saved topics. | High | 1 |
| FR-01.6 | The system shall persist users and topics in SQLite. | High | 1 |

### FR-02: News Source Fetching
| ID | Requirement | Priority | Sprint |
|----|-------------|----------|--------|
| FR-02.1 | The system shall load news articles (id, title, source, topic, summary, published_at) from a mock source. | High | 1 |
| FR-02.2 | The system shall filter articles by one or several topics. | High | 1 |
| FR-02.3 | The system shall build a personalized feed from a subscriber's saved topics, newest first. | High | 1 |
| FR-02.4 | The system shall return HTTP 400 for unknown topics in a news filter. | Medium | 1 |
| FR-02.5 | The news provider shall be replaceable behind the same service interface. | Medium | 2 |

### FR-03: Digest Jobs
| ID | Requirement | Priority | Sprint |
|----|-------------|----------|--------|
| FR-03.1 | The system shall run a digest-generation job that compiles each subscriber's matching articles. | High | 2 |
| FR-03.2 | The job shall be triggerable on demand and on a daily schedule. | Medium | 2 |
| FR-03.3 | The job shall skip subscribers with no matching articles and record the outcome. | Medium | 2 |

### FR-04: Email Stubs
| ID | Requirement | Priority | Sprint |
|----|-------------|----------|--------|
| FR-04.1 | The system shall render a digest as an HTML/text email through a templating stub. | High | 2 |
| FR-04.2 | The system shall "send" the email through a mock sender that logs recipient, subject and body. | High | 2 |
| FR-04.3 | The mock sender shall implement an interface so an SMTP/API sender can be swapped in. | Medium | 2 |

## 4. Non-Functional Requirements

### 4.1 Performance
- API endpoints shall respond in under 500 ms for up to 1,000 subscribers on a developer laptop.
- The personalized feed shall be generated in a single pass over the news dataset.

### 4.2 Modularity
- Presentation, application logic and data access shall be separated into independent modules (3-tier architecture).
- Each module (`database`, `news_service`, `schemas`, `main`) shall be testable in isolation.
- Replacing the news provider or email sender shall not require changes to the API layer.

### 4.3 CI/CD Maintainability
- Every push and pull request to `main` shall run flake8 and pytest with coverage via GitHub Actions.
- Code shall comply with PEP 8 (max line length 120) and the build shall fail on lint errors or failing tests.
- Dependencies shall be pinned in `requirements.txt` for reproducible builds.
- Changes shall reach `main` through reviewed pull requests.

### 4.4 Usability and Reliability
- The dashboard shall let a user save topics and preview their feed within three interactions.
- Errors shall return clear JSON messages with correct HTTP status codes.

## 5. Use Cases

### UC-01: Subscribe to Topics
- **Actor:** Subscriber
- **Precondition:** Email not yet registered.
- **Main flow:** (1) User opens the dashboard. (2) Enters an email. (3) Selects topics. (4) Clicks Save Preferences. (5) System validates and stores the user and topics. (6) System confirms.
- **Alternate flows:** Duplicate email, so the UI updates the existing preferences instead (UC-02). Invalid email or topic, so an error is shown.
- **Postcondition:** The subscriber and topics exist in the database.

### UC-02: Update Preferences
- **Actor:** Subscriber
- **Precondition:** Subscriber exists.
- **Main flow:** (1) User enters their email. (2) Changes the topic selection. (3) Clicks Save Preferences. (4) System replaces the stored topics. (5) System confirms.
- **Alternate flow:** Unknown email returns 404 on direct API use.

### UC-03: Preview Personalized Feed
- **Actor:** Subscriber
- **Precondition:** Subscriber exists with saved topics.
- **Main flow:** (1) User clicks Preview My Personalized Feed. (2) System loads saved topics. (3) System filters mock news. (4) Articles are displayed, newest first.
- **Alternate flow:** Unknown user, so the UI asks the user to save preferences first.

### UC-04: Filter News by Topic
- **Actor:** Subscriber or Developer
- **Main flow:** Call `GET /api/news?topic=technology`; the system returns matching articles. Unknown topics return 400.

### UC-05: Generate and Send Daily Digest (Sprint 2)
- **Actor:** Scheduler
- **Main flow:** (1) Job starts. (2) For each subscriber, compile matching articles. (3) Render the email template. (4) Mock sender logs the email. (5) Job records a summary.

## 6. Traceability (Sprint 1)
| Requirement | Test cases |
|-------------|-----------|
| FR-01.1 | TC-01 |
| FR-01.2 | TC-02 |
| FR-01.3 | TC-06 |
| FR-01.4 | TC-04 |
| FR-01.5 | TC-03 |
| FR-02.2, FR-02.3 | TC-05 |
| FR-02.4 | TC-06 |
