from openai import OpenAI
from src.config import OPENCODE_API_KEY, OPENCODE_BASE_URL, OPENCODE_MODEL

client = OpenAI(api_key=OPENCODE_API_KEY, base_url=OPENCODE_BASE_URL)

SUMMARY_PROMPT = """You are a news summarizer. Summarize the following news article in 2-3 sentences.
Focus on: who, what, when, where, why. Be factual and neutral. Output ONLY the summary."""


def summarize_article(title, body):
    text = f"Title: {title}\n\n{body[:2000]}" if body else title

    try:
        resp = client.chat.completions.create(
            model=OPENCODE_MODEL,
            messages=[
                {"role": "system", "content": SUMMARY_PROMPT},
                {"role": "user", "content": text},
            ],
            temperature=0.3,
            max_tokens=200,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[summarize] LLM error: {e}")
        return text[:200]


def summarize_all(articles):
    for a in articles:
        a["summary"] = summarize_article(a.get("title", ""), a.get("body", ""))
    print(f"[summarize] Summarized {len(articles)} articles")
    return articles
