# Jira Setup Summary — Personalized News Emailer

Site: https://aiml-team-se-5c.atlassian.net  
Project selected: **SE-Labwork (`SL`)** because it has a Scrum board and supports Epic/Task issue types. No prior Personalized News Emailer issues were found in the candidate projects during setup.  
Board: [SL board](https://aiml-team-se-5c.atlassian.net/jira/software/c/projects/SL/boards/3)  
Epic: [SL-1 — Personalized News Emailer — SE Mini Project](https://aiml-team-se-5c.atlassian.net/browse/SL-1)

## Sprint 1
Sprint `SL Sprint 1` (ID 1) is configured from **29 Oct 2026, 9:00 AM IST** to **31 Oct 2026, 6:00 PM IST**, with a goal for the integrated subscription/preferences API, mock news filtering, dashboard, automated tests and one-minute demo.

| Planned PNE reference | Actual Jira issue | Owner in description | Target |
|---|---|---|---|
| PNE-1 | [SL-2](https://aiml-team-se-5c.atlassian.net/browse/SL-2) | Mirunjai | 31 Oct |
| PNE-2 | [SL-3](https://aiml-team-se-5c.atlassian.net/browse/SL-3) | Mirunjai | 31 Oct |
| PNE-3 | [SL-4](https://aiml-team-se-5c.atlassian.net/browse/SL-4) | Nayana | 31 Oct |
| PNE-4 | [SL-5](https://aiml-team-se-5c.atlassian.net/browse/SL-5) | Videesha | 29 Oct |
| PNE-5 | [SL-6](https://aiml-team-se-5c.atlassian.net/browse/SL-6) | Videesha | 30 Oct |
| PNE-6 | [SL-7](https://aiml-team-se-5c.atlassian.net/browse/SL-7) | Keerthishree | 30 Oct |
| PNE-7 | [SL-8](https://aiml-team-se-5c.atlassian.net/browse/SL-8) | Keerthishree | 30 Oct |
| PNE-8 | [SL-9](https://aiml-team-se-5c.atlassian.net/browse/SL-9) | Nayana | 31 Oct |

All eight tasks are assigned to Sprint 1 and begin in To Do. Only Mirunjai's Jira account resolved as assignable, so the other three are currently unassigned in Jira; their intended accountable owners are written in each description. Invite/add the team members to the SL project and then assign their issues.

The board reports a Story Points estimation field but the connected create/edit interface did not allow setting it for these task types. An attempt to apply estimates returned a field-resolution error; therefore the original estimates (2, 1, 3, 4, 4, 5, 3, 4) are not confirmed as saved to Jira. Configure the Story Points field on the project's Task screens or enter the values in Jira manually before relying on point-based burndown.

## Sprint 2
Sprint `SL Sprint 2` (ID 34) was created from **2 Nov 2026, 9:00 AM IST** to **7 Nov 2026, 6:00 PM IST**.

| Actual Jira issue | Scope | Intended owner |
|---|---|---|
| [SL-10](https://aiml-team-se-5c.atlassian.net/browse/SL-10) | Digest generation job | Keerthishree |
| [SL-11](https://aiml-team-se-5c.atlassian.net/browse/SL-11) | Email template and mocked sender | Keerthishree |
| [SL-12](https://aiml-team-se-5c.atlassian.net/browse/SL-12) | Digest history persistence | Videesha |
| [SL-13](https://aiml-team-se-5c.atlassian.net/browse/SL-13) | Digest/template/sender tests and regression | Nayana |
| [SL-14](https://aiml-team-se-5c.atlassian.net/browse/SL-14) | Final docs, demo and release verification | Mirunjai |

These Sprint 2 tasks are assigned to the future Sprint 2, not Sprint 1. The three non-Mirunjai tasks are also unassigned in Jira until the correct teammate accounts are added.

## Important status and limitations

- Creating these Jira issues does not mean the work is complete; all are currently To Do.
- The dates are a revised proposed schedule; confirm the shortened Sprint 1 window with the instructor.
- The connected GitHub integration continues to return HTTP 403 for repository writes. The ChatGPT GitHub app is documented as read-only in standard connected-app use; use Codex or a local Git workflow to commit the prepared project files and open the PR.
- This package itself has not been committed to GitHub.
