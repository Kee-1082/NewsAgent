import os
from dotenv import load_dotenv

load_dotenv()

OPENCODE_API_KEY = os.getenv("OPENCODE_API_KEY")
OPENCODE_BASE_URL = os.getenv("OPENCODE_BASE_URL", "https://opencode.ai/zen/v1")
OPENCODE_MODEL = os.getenv("OPENCODE_MODEL", "deepseek-v4-flash-free")

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_FROM = os.getenv("EMAIL_FROM")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
WHATSAPP_TO = os.getenv("WHATSAPP_TO")

ARTICLES_FILE = os.path.join("data", "articles.json")
SOURCES_FILE = os.path.join("data", "sources.json")

CATEGORIES = [
    "trending",
    "financial",
    "indian",
    "international",
    "social_media",
    "technological",
    "political",
    "sports",
]

CATEGORY_EMOJIS = {
    "trending": "🔥",
    "financial": "💰",
    "indian": "🇮🇳",
    "international": "🌍",
    "social_media": "📱",
    "technological": "💻",
    "political": "🏛️",
    "sports": "⚽",
}

MAX_ARTICLES_PER_CATEGORY = 4
MAX_ARTICLES_TOTAL = 30
