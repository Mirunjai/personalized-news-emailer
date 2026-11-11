"""HTML and plain-text digest email rendering."""
from datetime import datetime
from html import escape
from typing import Dict, List, Tuple


def render_digest(
    recipient: str,
    articles: List[Dict],
    generated_at: str = "",
) -> Tuple[str, str, str]:
    """Return (subject, HTML body, plain-text body) for a subscriber digest."""
    day = generated_at[:10] if generated_at else datetime.now().date().isoformat()
    subject = "Your Personalized News Digest - " + day
    html_items = []
    text_items = []
    for article in articles:
        title = str(article.get("title", "Untitled"))
        summary = str(article.get("summary", ""))
        source = str(article.get("source", "Unknown source"))
        topic = str(article.get("topic", ""))
        html_items.append(
            "<li><h2>{}</h2><p>{}</p><small>{} | {}</small></li>".format(
                escape(title), escape(summary), escape(source), escape(topic)
            )
        )
        text_items.append(
            "{}\n{}\nSource: {} | Topic: {}".format(title, summary, source, topic)
        )
    html_body = (
        "<!doctype html><html><body><h1>Your news digest</h1>"
        "<p>For {}</p><ul>{}</ul><footer>Generated {}</footer></body></html>"
    ).format(escape(recipient), "".join(html_items), escape(generated_at))
    text_body = "Your news digest for {}\n\n{}\n\nGenerated {}".format(
        recipient, "\n\n".join(text_items), generated_at
    )
    return subject, html_body, text_body
