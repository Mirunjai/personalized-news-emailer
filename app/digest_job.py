"""Per-subscriber digest orchestration and command-line entry point."""
import argparse
import uuid
from datetime import datetime, timezone
from typing import Dict, List

from app import database, email_sender, email_template, news_service


def run_digest_job() -> Dict:
    """Generate a mocked digest for each subscriber and persist every outcome."""
    database.init_db()
    run_id = str(uuid.uuid4())
    run_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    results: List[Dict] = []

    for subscriber in database.get_subscribers():
        email = subscriber["email"]
        try:
            articles = news_service.personalized_feed(subscriber["topics"])
            if not articles:
                database.record_digest_outcome(
                    email, run_id, run_at, "no_articles", article_count=0
                )
                results.append({"email": email, "status": "no_articles", "article_count": 0})
                continue

            subject, html_body, text_body = email_template.render_digest(
                email, articles, run_at
            )
            email_sender.send_mock_email(
                recipient=email,
                subject=subject,
                html_body=html_body,
                text_body=text_body,
                run_id=run_id,
            )
            database.record_digest_outcome(
                email,
                run_id,
                run_at,
                "sent",
                article_count=len(articles),
                subject=subject,
            )
            results.append({
                "email": email,
                "status": "sent",
                "article_count": len(articles),
                "subject": subject,
            })
        except Exception as exc:  # isolate failures so other subscribers still run
            error = str(exc)[:500]
            try:
                database.record_digest_outcome(
                    email, run_id, run_at, "failed", error=error
                )
            except Exception:
                # The original failure remains visible in this run summary.
                error += " (history write failed)"
            results.append({"email": email, "status": "failed", "error": error})

    return {
        "run_id": run_id,
        "run_at": run_at,
        "total": len(results),
        "sent": sum(item["status"] == "sent" for item in results),
        "no_articles": sum(item["status"] == "no_articles" for item in results),
        "failed": sum(item["status"] == "failed" for item in results),
        "results": results,
    }


def main() -> None:
    """Run one digest cycle; schedule this command daily with cron/Task Scheduler."""
    parser = argparse.ArgumentParser(description="Run one personalized news digest cycle")
    parser.parse_args()
    summary = run_digest_job()
    print(
        "Digest run {run_id}: {sent} sent, {no_articles} empty, "
        "{failed} failed".format(**summary)
    )


if __name__ == "__main__":
    main()
