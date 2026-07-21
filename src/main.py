import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.fetch import fetch_all
from src.extract import extract_all
from src.classify import classify_all
from src.summarize import summarize_all
from src.filter import filter_articles
from src.assemble import build_digest
from src.email import send_digest
from src.config import ARTICLES_FILE
import json


def main():
    print("=" * 50)
    print("Daily News Digest — Starting pipeline")
    print("=" * 50)

    print("\n[1/6] Fetching articles...")
    articles = fetch_all()
    print(f"       → {len(articles)} articles fetched")

    print("\n[2/6] Extracting article bodies...")
    articles = extract_all(articles)

    print("\n[3/6] Classifying articles...")
    articles = classify_all(articles)

    print("\n[4/6] Summarizing articles...")
    articles = summarize_all(articles)

    print("\n[5/6] Filtering & ranking...")
    articles = filter_articles(articles)

    with open(ARTICLES_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    print(f"       → Saved {len(articles)} articles to {ARTICLES_FILE}")

    print("\n[6/6] Building & sending digest...")
    html = build_digest(articles)
    send_digest(html)

    print("\n" + "=" * 50)
    print("Pipeline complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
