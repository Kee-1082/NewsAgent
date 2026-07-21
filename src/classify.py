from openai import OpenAI
from src.config import OPENCODE_API_KEY, OPENCODE_BASE_URL, OPENCODE_MODEL, CATEGORIES

client = OpenAI(api_key=OPENCODE_API_KEY, base_url=OPENCODE_BASE_URL)

CATEGORY_PROMPT = f"""You are a news classifier. Given a news headline and snippet, classify it into exactly one of these categories:
{', '.join(CATEGORIES)}

Respond with ONLY the category name, nothing else."""


def classify_article(title, snippet):
    if not title and not snippet:
        return "trending"

    try:
        resp = client.chat.completions.create(
            model=OPENCODE_MODEL,
            messages=[
                {"role": "system", "content": CATEGORY_PROMPT},
                {
                    "role": "user",
                    "content": f"Title: {title}\nSnippet: {snippet[:500]}",
                },
            ],
            temperature=0.1,
            max_tokens=20,
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
        a["category"] = classify_article(a.get("title", ""), a.get("snippet", ""))
    print(f"[classify] Classified {len(articles)} articles")
    return articles
