import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from src.config import CATEGORIES, CATEGORY_EMOJIS

TEMPLATE_DIR = "templates"


def group_by_category(articles):
    grouped = {cat: [] for cat in CATEGORIES}
    for a in articles:
        cat = a.get("category", "trending")
        if cat in grouped:
            grouped[cat].append(a)
    return grouped


def format_timestamp(pub_str):
    if not pub_str:
        return ""
    try:
        dt = datetime.fromisoformat(pub_str.replace("Z", "+00:00"))
        now = datetime.now(dt.tzinfo)
        diff = now - dt
        hours = int(diff.total_seconds() // 3600)
        if hours < 1:
            return "Just now"
        if hours < 24:
            return f"{hours}h ago"
        days = hours // 24
        return f"{days}d ago"
    except Exception:
        return pub_str[:10] if pub_str else ""


def build_digest(articles, date_str=None):
    if not date_str:
        date_str = datetime.now().strftime("%A, %B %d, %Y")

    grouped = group_by_category(articles)

    sections = []
    for cat in CATEGORIES:
        items = grouped.get(cat, [])
        if not items:
            continue
        emoji = CATEGORY_EMOJIS.get(cat, "📰")
        sections.append(
            {
                "category": cat,
                "emoji": emoji,
                "display_name": cat.replace("_", " ").title(),
                "articles": [
                    {
                        "title": a.get("title", ""),
                        "url": a.get("url", ""),
                        "summary": a.get("summary", ""),
                        "source": a.get("source", ""),
                        "time": format_timestamp(a.get("published_at", "")),
                        "reputation": a.get("reputation", 5),
                    }
                    for a in items
                ],
            }
        )

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("digest.html")
    html = template.render(
        date=date_str,
        sections=sections,
        total_articles=len(articles),
    )

    return html
