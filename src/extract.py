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
            "images": list(article.images) if hasattr(article, "images") else [],
            "meta_description": article.meta_description or "",
            "meta_keywords": article.meta_keywords or "",
            "meta_lang": article.meta_lang or "",
        }
    except requests.exceptions.Timeout:
        print(f"[extract] Timeout: {url}")
        return None
    except Exception as e:
        print(f"[extract] Failed: {url} - {e}")
        return None


def extract_all(articles):
    enriched = []
    for a in articles:
        result = extract_article(a["url"])
        if result and result.get("text"):
            a["body"] = result["text"][:5000]
            a["authors"] = result["authors"]
            a["top_image"] = result["top_image"]
            a["images"] = result["images"]
            a["meta_description"] = result["meta_description"]
            a["meta_keywords"] = result["meta_keywords"]
            a["meta_lang"] = result["meta_lang"]
            if result.get("title"):
                a["title"] = result["title"]
            if result.get("published_at"):
                a["published_at"] = result["published_at"]
            enriched.append(a)
        else:
            a["body"] = a.get("snippet", "")
            a["images"] = []
            a["meta_description"] = ""
            a["meta_keywords"] = ""
            a["meta_lang"] = ""
            enriched.append(a)

    print(f"[extract] Enriched {len(enriched)} articles")
    return enriched
