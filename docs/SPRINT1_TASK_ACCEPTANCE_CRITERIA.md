# Sprint 1 Jira Acceptance Criteria — PNE-1 to PNE-8

**Execution plan:** Thursday 29 October through Saturday 31 October 2026. This is compressed; confirm the schedule change with the instructor. Reconcile with existing Jira issues and avoid duplicates.

| Key | Owner | Points | Acceptance criteria |
|---|---|---:|---|
| PNE-1 | Mirunjai | 2 | CI runs on pushes/PRs to `main`; dependencies install; lint/tests execute; PR protection is checked and documented. |
| PNE-2 | Mirunjai | 1 | Sprint board has owners/points; statuses reflect real progress; PRs are reviewed and linked to Jira. |
| PNE-3 | Nayana | 3 | SRS/SAD/Test Plan match instructor templates; demo script works; one-minute video is saved by Sprint 1 end. |
| PNE-4 | Videesha | 4 | SQLite creates `users` and `topic_preferences`; uniqueness constraints work; initialization is reproducible. |
| PNE-5 | Videesha | 4 | Subscribe, retrieve/update preferences work; duplicate emails and invalid values return documented errors; data persists. |
| PNE-6 | Keerthishree | 5 | Mock articles load; single/multiple-topic filtering works; invalid topics rejected; results ordered deterministically. |
| PNE-7 | Keerthishree | 3 | Dashboard saves/updates preferences and previews matching personalized news. |
| PNE-8 | Nayana | 4 | TC-01–TC-06 and edge cases run with pytest against isolated databases; suite passes after modules are integrated. |

## Daily commitments
- **Thu 29 Oct:** database/preference PR ready; PNE-1/PNE-2 access and board checks; PNE-3 template review.
- **Fri 30 Oct:** news/UI PR ready and integrated; full tests begin against combined app.
- **Sat 31 Oct:** regression evidence and demo; CI verification; accurate sprint closure.

## Working agreement
- Keep one repository.
- Each member raises their own PR if required by the course rubric.
- Include Jira key in PR title/body.
- Mirunjai reviews/merges only after acceptance criteria and CI pass.
- Never mark Done before criteria are met.
- If a task cannot fit, report it incomplete; do not fake completion.
