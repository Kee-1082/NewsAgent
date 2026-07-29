import requests
import feedparser
import hashlib
from datetime import datetime
from src.config import NEWSAPI_KEY, SOURCES_FILE, ARTICLES_FILE
from src.config import MAX_ARTICLES_TOTAL
import json
import time


def _load_sources():
    with open(SOURCES_FILE, encoding="utf-8") as f:
        return json.load(f)


def _article_id(url):
    return hashlib.md5(url.encode()).hexdigest()


def fetch_newsapi():
    if not NEWSAPI_KEY:
        print("[fetch] NEWSAPI_KEY not set, skipping NewsAPI")
        return []

    articles = []
    queries = ["india", "technology", "business", "world", "sports", "politics"]

    for query in queries:
        try:
            resp = requests.get(
                "https://newsapi.org/v2/everything",
                params={
                    "q": query,
                    "language": "en",
                    "sortBy": "publishedAt",
                    "pageSize": 10,
                    "apiKey": NEWSAPI_KEY,
                },
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            for item in data.get("articles", []):
                if not item.get("url"):
                    continue
                articles.append(
                    {
                        "id": _article_id(item["url"]),
                        "title": item.get("title") or "",
                        "url": item["url"],
                        "source": item.get("source", {}).get("name") or "NewsAPI",
                        "published_at": item.get("publishedAt") or "",
                        "snippet": item.get("description") or "",
                    }
                )
        except Exception as e:
            print(f"[fetch] NewsAPI query '{query}' failed: {e}")

        time.sleep(0.3)

    print(f"[fetch] NewsAPI returned {len(articles)} articles")
    return articles


def fetch_rss():
    sources = _load_sources()
    feeds = sources.get("rss_feeds", [])
    articles = []

    for feed_url in feeds:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:8]:
                link = entry.get("link") or ""
                if not link:
                    continue
                articles.append(
                    {
                        "id": _article_id(link),
                        "title": entry.get("title") or "",
                        "url": link,
                        "source": feed.feed.get("title") or feed_url,
                        "published_at": entry.get("published") or "",
                        "snippet": entry.get("summary") or "",
                    }
                )
        except Exception as e:
            print(f"[fetch] RSS feed '{feed_url}' failed: {e}")

    print(f"[fetch] RSS returned {len(articles)} articles")
    return articles


def deduplicate(articles):
    seen = set()
    unique = []
    for a in articles:
        if a["id"] not in seen:
            seen.add(a["id"])
            unique.append(a)
    print(f"[fetch] Dedup: {len(articles)} -> {len(unique)}")
    return unique


def fetch_all():
    all_articles = fetch_newsapi() + fetch_rss()
    all_articles = deduplicate(all_articles)
    all_articles.sort(key=lambda a: a.get("published_at", ""), reverse=True)
    all_articles = all_articles[:MAX_ARTICLES_TOTAL]

    return all_articles
