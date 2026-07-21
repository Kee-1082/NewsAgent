from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from src.config import SENDGRID_API_KEY, EMAIL_TO, EMAIL_FROM


def send_digest(html_content, subject=None):
    if not SENDGRID_API_KEY:
        print("[email] SENDGRID_API_KEY not set, skipping send")
        print("[email] Digest preview written to data/digest_preview.html")
        with open("data/digest_preview.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        return False

    if not subject:
        from datetime import datetime
        subject = f"Daily News Digest — {datetime.now().strftime('%b %d, %Y')}"

    message = Mail(
        from_email=Email(EMAIL_FROM),
        to_emails=To(EMAIL_TO),
        subject=subject,
        html_content=Content("text/html", html_content),
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"[email] Sent! Status: {response.status_code}")
        return True
    except Exception as e:
        print(f"[email] Send failed: {e}")
        print("[email] Saving preview to data/digest_preview.html instead")
        with open("data/digest_preview.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        return False
