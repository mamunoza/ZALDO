from datetime import datetime
from typing import Any, Dict, Optional
import httpx

from ..core.config import get_settings

settings = get_settings()


async def track_event(event: str, distinct_id: str, properties: Optional[Dict[str, Any]] = None) -> None:
    if not settings.posthog_host or not settings.posthog_api_key:
        return

    payload = {
        "api_key": settings.posthog_api_key,
        "event": event,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "distinct_id": distinct_id,
        "properties": properties or {},
    }

    async with httpx.AsyncClient() as client:
        await client.post(f"{settings.posthog_host.rstrip('/')}/capture/", json=payload, timeout=5)
