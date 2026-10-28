# Sprint 1 Kickoff Readiness — Team 15

Project: Personalized News Emailer
Repository: https://github.com/Mirunjai/personalized-news-emailer
Updated: Wednesday, 28 October 2026
**Revised execution window: Thursday, 29 October – Saturday, 31 October 2026**
Sprint 2: 2–7 November 2026
Final presentation: 9 November 2026

## 1. Start decision
Start execution on **Thursday, 29 October**; no work is scheduled for tonight. This is a shortened Sprint 1 window, so prioritize integration and the working-product acceptance criteria. Confirm with the instructor that this is acceptable; do not silently change official Jira dates.

## 2. Verified repository baseline
- `main` exists and contains `docs/SRS_Requirement_Analysis.md`, `docs/SAD_System_Design.md`, `docs/Test_Plan.md`, and `docs/Sprint1_Demo_Script.md`.
- `.github/workflows/ci.yml` exists. Two previously observed successful CI runs tested the starter baseline, not necessarily the full app.
- Feature branches exist: `feature/db-and-preference-api`, `feature/news-service-and-ui`, and `feature/docs-and-tests`.
- Database code, news/UI code, and the full test suite are separated across those branches.
- No open PRs were observed in the earlier audit.
- A GitHub write attempt was denied with HTTP 403; this package has not been committed.

## 3. Unverified gates
- Jira contains the intended tickets, owners, story points, and dates.
- All teammates have GitHub write access.
- `main` branch protection requires reviewed PRs and successful CI.
- The three documents match the instructor's exact templates.
- The integrated application and full suite pass on `main`.

## 4. Revised day-by-day plan

### Thursday, 29 October — kickoff and database PR
- **Mirunjai:** verify access/PR settings; check Jira and ask the instructor about the shortened window; review the database PR.
- **Videesha:** validate SQLite initialization, email normalization, duplicate handling, preference retrieval/update; open the database/preference API PR with test evidence.
- **Keerthishree:** check news/UI branch against agreed database/API contracts; list integration mismatches.
- **Nayana:** compare SRS/SAD/Test Plan to instructor templates; prepare to run tests once modules are integrated.
- **Exit gate:** database PR is open and reviewable; each blocker has an owner.

### Friday, 30 October — news/UI integration
- **Mirunjai:** review/merge Videesha's PR only if CI and review pass; review Keerthishree's PR.
- **Videesha:** help resolve persistence/API defects.
- **Keerthishree:** open news/UI PR; demonstrate subscription, preference save/update and personalized feed preview.
- **Nayana:** run TC-01–TC-06 and edge cases; report reproducible defects.
- **Exit gate:** feature modules integrated, or remaining blockers documented with owners.

### Saturday, 31 October — regression, demo and freeze
- **Nayana:** run `flake8 .` and `pytest --cov=app --cov-report=term-missing`; record the one-minute working-product demo.
- **Videesha + Keerthishree:** fix integration defects and verify the demo flow.
- **Mirunjai:** confirm accepted code is on `main`, rerun checks on `main`, update Jira honestly, and freeze the baseline.
- **Exit gate:** demo committed, core acceptance criteria pass, CI green on integrated `main`, remaining defects documented.

## 5. PR dependency order
1. `feature/db-and-preference-api` → `main` (Videesha raises; Mirunjai reviews).
2. `feature/news-service-and-ui` → `main` (Keerthishree raises after database/API is available).
3. `feature/docs-and-tests` → `main` (Nayana raises after app modules exist).

The test branch imports `app.main`, so the application module and dependencies must be integrated before the full test suite can pass on `main`. Do not merge only because a branch exists.

## 6. Sprint 1 acceptance gate
- [ ] Valid subscription returns HTTP 201 and persists email/topics.
- [ ] Duplicate subscription is rejected as documented.
- [ ] Preferences can be retrieved and updated.
- [ ] News filters by one or multiple valid topics.
- [ ] Dashboard previews news matching saved topics.
- [ ] Invalid email/topic inputs return documented errors.
- [ ] `flake8 .` passes.
- [ ] `pytest --cov=app --cov-report=term-missing` passes on integrated `main`.
- [ ] One-minute working-product demo is committed.
- [ ] Jira reflects actual status.

## 7. Sprint 2 and final deadline
Sprint 2 remains 2–7 November: implement digest generation, email template rendering, mocked sender/logging, and digest history. Real email delivery stays out of scope unless requirements change. Commit the two-minute demo and final documentation by 7 November; reserve 8 November for release verification and rehearsal before the 9 November presentation.

## 8. Manual/account actions still required
- Connect/authorize Jira/Atlassian to inspect or update the real board.
- Restore GitHub write access for the connected integration, or have the repo owner commit these files through a reviewed PR.
- Confirm the shortened Sprint 1 window with the instructor.
