# Sprint 2 Presentation Outline

1. **Problem and goal:** subscribers need a digest matching their chosen topics.
2. **Architecture:** FastAPI dashboard/API, SQLite preferences/history, mock news provider, digest job, email template and local mock sender.
3. **Digest workflow:** enumerate subscribers, filter per subscriber, render HTML/text, append local outbox entry, record outcome.
4. **Failure handling:** empty digest is recorded and skipped; one subscriber failure does not stop processing later subscribers.
5. **Testing:** personalized multi-subscriber flow, template escaping, local sender, history, empty and failure isolation.
6. **CI/CD:** show GitHub Actions lint and pytest result for the final commit.
7. **Demo and limitations:** demonstrate the on-demand run and local outbox; daily scheduling is configured by OS cron/Task Scheduler. No real email is sent.
