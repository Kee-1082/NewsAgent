import json
from urllib.parse import urlparse
from src.config import SOURCES_FILE, CATEGORIES, MAX_ARTICLES_PER_CATEGORY


def _load_reputation():
    with open(SOURCES_FILE, encoding="utf-8") as f:
        sources = json.load(f)
    return sources.get("domain_reputation", {})


def _domain(url):
    return urlparse(url).netloc.replace("www.", "")


def _reputation_score(url, rep_map):
    domain = _domain(url)
    for key, score in rep_map.items():
        if key in domain:
            return score
    return rep_map.get("default", 5)


def _sports_is_major(article):
    title = (article.get("title") or "").lower()
    major_keywords = [
        "world cup", "championship", "final", "gold medal", "record",
        "champion", "olympics", "grand slam", "title win", "title race",
        "super bowl", "playoffs", "semi-final", "quarter-final",
        "transfer record", "hat-trick", "century", "maiden",
    ]
    return any(kw in title for kw in major_keywords)


def filter_articles(articles):
    rep_map = _load_reputation()

    for a in articles:
        a["reputation"] = _reputation_score(a.get("url", ""), rep_map)

    filtered = []
    rejected_sports = 0

    for a in articles:
        if a.get("category") == "sports" and not _sports_is_major(a):
            rejected_sports += 1
            continue
        if a.get("reputation", 5) < 4:
            continue
        if not a.get("title") and not a.get("summary"):
            continue
        filtered.append(a)

    print(f"[filter] Sports rejected (non-major): {rejected_sports}")
    print(f"[filter] {len(articles)} → {len(filtered)} after filtering")

    grouped = {cat: [] for cat in CATEGORIES}
    for a in filtered:
        cat = a.get("category", "trending")
        if cat in grouped:
            grouped[cat].append(a)

    for cat in grouped:
        grouped[cat] = sorted(
            grouped[cat], key=lambda x: x.get("reputation", 5), reverse=True
        )[:MAX_ARTICLES_PER_CATEGORY]

    result = []
    for cat in CATEGORIES:
        result.extend(grouped[cat])

    print(f"[filter] {len(result)} after category capping")
    return result
