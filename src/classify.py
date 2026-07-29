from openai import OpenAI
from src.config import OPENCODE_API_KEY, OPENCODE_BASE_URL, OPENCODE_MODEL, CATEGORIES

client = OpenAI(api_key=OPENCODE_API_KEY, base_url=OPENCODE_BASE_URL)

CATEGORY_GUIDE = """
- trending: viral social media topics, internet culture, widely-discussed buzz
- financial: stock markets, economy, banking, crypto, budgets, corporate earnings
- indian: news specifically about India — politics, policy, society, entertainment
- international: global news outside India — diplomacy, conflicts, world events
- social_media: platform-specific news (Twitter/X, Instagram, TikTok, Reddit), influencer culture
- technological: AI, software, gadgets, science, space, cybersecurity
- political: election campaigns, legislation, government affairs, party politics
- sports: competitive sports, tournaments, athletes, records
"""

CATEGORY_PROMPT = f"""You are a news classifier. Given a news article, classify it into exactly one category.

Categories:{CATEGORY_GUIDE}
Respond with ONLY the category name. If unsure, choose the best fit."""


def classify_article(title, snippet, body=""):
    if not title and not snippet and not body:
        return "trending"

    content = f"Title: {title}\n\n"
    if body:
        content += f"Body: {body[:1000]}\n\n"
    content += f"Snippet: {snippet[:500]}" if snippet else ""

    try:
        resp = client.chat.completions.create(
            model=OPENCODE_MODEL,
            messages=[
                {"role": "system", "content": CATEGORY_PROMPT},
                {"role": "user", "content": content},
            ],
            temperature=0.1,
            max_tokens=500,
        )
        label = resp.choices[0].message.content.strip().lower()
        if label in CATEGORIES:
            return label
        return "trending"
    except Exception as e:
        print(f"[classify] LLM error: {e}")
        return "trending"


def classify_all(articles):
    for a in articles:
        a["category"] = classify_article(
            a.get("title", ""), a.get("snippet", ""), a.get("body", "")
        )
    print(f"[classify] Classified {len(articles)} articles")
    return articles
