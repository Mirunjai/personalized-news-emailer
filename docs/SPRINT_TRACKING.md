# Team 15 Sprint Tracking

## Sprint 1

| Jira | Work | Evidence |
|---|---|---|
| SL-2 | CI/CD workflow | GitHub Actions lint + pytest |
| SL-3 | PR tracking | PRs #4, #5 and #6 merged |
| SL-4 | Documentation and demo | Docs merged; actual recording remains a manual deliverable |
| SL-5–SL-6 | Database and preference APIs | PR #4 |
| SL-7–SL-8 | News service and dashboard | PR #5 |
| SL-9 | Regression tests | PR #6 and integrated CI |

## Sprint 2

| Jira | Work | Implementation |
|---|---|---|
| SL-10 | Digest generation and daily execution | app/digest_job.py; API and CLI; OS scheduler instructions |
| SL-11 | Template and mock sender | app/email_template.py; app/email_sender.py |
| SL-12 | Digest history | digest_log in app/database.py |
| SL-13 | Regression tests | tests/test_digest.py |
| SL-14 | Final documentation/demo/release | README, SAD, Test Plan, demo script and presentation outline |

## Definition of done for this coursework

Implementation is complete when code is merged, automated tests and lint pass, setup/run instructions are documented, and a short demo is recorded. Branch protection is optional for this class project; the existing pull-request workflow and CI run provide the coursework evidence.

The demo video must still be recorded by the team and uploaded to the repository or linked here. A script is not a video.
