from newspaper import Article
import requests


def extract_article(url, timeout=15):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return {
            "title": article.title or "",
            "text": article.text or "",
            "authors": article.authors or [],
            "published_at": str(article.publish_date) if article.publish_date else "",
            "top_image": article.top_image or "",
        }
    except requests.exceptions.Timeout:
        print(f"[extract] Timeout: {url}")
        return None
    except Exception as e:
        print(f"[extract] Failed: {url} — {e}")
        return None


def extract_all(articles):
    enriched = []
    for a in articles:
        result = extract_article(a["url"])
        if result and result.get("text"):
            a["body"] = result["text"][:5000]
            a["authors"] = result["authors"]
            a["top_image"] = result["top_image"]
            if result.get("published_at"):
                a["published_at"] = result["published_at"]
            enriched.append(a)
        else:
            a["body"] = a.get("snippet", "")
            enriched.append(a)

    print(f"[extract] Enriched {len(enriched)} articles")
    return enriched
