"""News service: loads the mock dataset and filters it by topic."""
import json
from pathlib import Path
from typing import Dict, Iterable, List

NEWS_FILE = Path(__file__).resolve().parent / "mock_news.json"


def get_all_articles() -> List[Dict]:
    """Return every mock article, newest first."""
    with NEWS_FILE.open(encoding="utf-8") as handle:
        articles = json.load(handle)
    return sorted(articles, key=lambda article: article["published_at"], reverse=True)


def parse_topics(raw: str) -> List[str]:
    """Split a comma-separated topic string into normalised topic names."""
    return [part.strip().lower() for part in raw.split(",") if part.strip()]


def filter_by_topics(topics: Iterable[str]) -> List[Dict]:
    """Return articles whose topic is in the given topics (single or multiple)."""
    wanted = {topic.strip().lower() for topic in topics}
    return [article for article in get_all_articles() if article["topic"] in wanted]


def personalized_feed(saved_topics: Iterable[str]) -> List[Dict]:
    """Preview of the digest a user would receive based on their saved preferences."""
    return filter_by_topics(saved_topics)
