from typing import Optional
import httpx

from ..core.config import get_settings

settings = get_settings()


async def send_email(to_email: str, subject: str, html_body: str, text_body: Optional[str] = None) -> None:
    if not settings.resend_api_key:
        print(f"[email] To: {to_email} | Subject: {subject}\n{text_body or html_body}")
        return

    payload = {
        "from": settings.email_from,
        "to": [to_email],
        "subject": subject,
        "html": html_body,
    }
    if text_body:
        payload["text"] = text_body

    headers = {"Authorization": f"Bearer {settings.resend_api_key}", "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.resend.com/emails", json=payload, headers=headers, timeout=10)
        response.raise_for_status()
