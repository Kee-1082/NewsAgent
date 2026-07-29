from datetime import datetime
from twilio.rest import Client
from src.config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_WHATSAPP_FROM,
    WHATSAPP_TO,
    CATEGORIES,
    CATEGORY_EMOJIS,
    ARTICLES_FILE,
)


def _format_timestamp(pub_str):
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


def build_text_digest(articles, date_str=None):
    if not date_str:
        date_str = datetime.now().strftime("%A, %B %d, %Y")

    lines = []
    lines.append(f"\U0001f4f0 Daily News Digest \u2014 {date_str}")
    lines.append(f"{len(articles)} stories curated for you")
    lines.append("")

    for cat in CATEGORIES:
        items = [a for a in articles if a.get("category") == cat]
        if not items:
            continue
        emoji = CATEGORY_EMOJIS.get(cat, "\U0001f4f0")
        lines.append(f"{emoji} {cat.replace('_', ' ').title()}")
        for i, a in enumerate(items, 1):
            title = a.get("title", "")
            summary = a.get("summary", "")
            url = a.get("url", "")
            source = a.get("source", "")
            time = _format_timestamp(a.get("published_at", ""))
            lines.append(f"{i}. {title}")
            if summary:
                lines.append(f"   {summary[:250]}")
            source_part = f"   {source}" if source else ""
            time_part = f" \u00b7 {time}" if time else ""
            url_part = f"\n   {url}" if url else ""
            lines.append(f"{source_part}{time_part}{url_part}")
            lines.append("")
        lines.append("")

    lines.append("Powered by your News Digest Agent")

    return "\n".join(lines)


MAX_WHATSAPP_LEN = 1600
PREFIX_RESERVE = 50


def _split_digest(text):
    """Split into chunks under MAX_WHATSAPP_LEN, keeping articles intact."""
    sections = text.split("\n\n")
    chunks = []
    current = []
    current_len = 0
    limit = MAX_WHATSAPP_LEN - PREFIX_RESERVE

    for section in sections:
        section_len = len(section) + 2

        if current_len + section_len > limit and current:
            chunks.append("\n\n".join(current))
            current = []
            current_len = 0

        if section_len > limit and current:
            chunks.append("\n\n".join(current))
            current = []
            current_len = 0
            lines = section.split("\n")
            for line in lines:
                if current_len + len(line) + 1 > limit and current:
                    chunks.append("\n".join(current))
                    current = []
                    current_len = 0
                current.append(line)
                current_len += len(line) + 1
        else:
            current.append(section)
            current_len += section_len

    if current:
        chunks.append("\n\n".join(current))

    return chunks


def send_whatsapp_digest(articles):
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        print("[whatsapp] Twilio credentials not set, saving to file instead")
        text = build_text_digest(articles)
        with open("data/digest_preview.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("[whatsapp] Digest preview written to data/digest_preview.txt")
        return False

    if not WHATSAPP_TO:
        print("[whatsapp] WHATSAPP_TO not set, saving to file instead")
        text = build_text_digest(articles)
        with open("data/digest_preview.txt", "w", encoding="utf-8") as f:
            f.write(text)
        return False

    if not TWILIO_WHATSAPP_FROM:
        print("[whatsapp] TWILIO_WHATSAPP_FROM not set, saving to file instead")
        text = build_text_digest(articles)
        with open("data/digest_preview.txt", "w", encoding="utf-8") as f:
            f.write(text)
        return False

    text = build_text_digest(articles)
    chunks = _split_digest(text)

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        total = len(chunks)
        sent = 0
        for i, chunk in enumerate(chunks, 1):
            body = chunk if total == 1 else f"({i}/{total})\n\n{chunk}"
            msg = client.messages.create(
                body=body,
                from_=f"whatsapp:{TWILIO_WHATSAPP_FROM}",
                to=f"whatsapp:{WHATSAPP_TO}",
            )
            sent += 1
            print(f"[whatsapp] Sent part {i}/{total} | SID: {msg.sid}")
        print(f"[whatsapp] Sent {sent}/{total} parts")
        return True
    except Exception as e:
        print(f"[whatsapp] Send failed: {e}")
        print("[whatsapp] Saving preview to data/digest_preview.txt instead")
        with open("data/digest_preview.txt", "w", encoding="utf-8") as f:
            f.write(text)
        return False
