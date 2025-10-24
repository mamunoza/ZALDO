from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache
from typing import List, Optional


def _split_admins(value: str) -> List[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass
class Settings:
    app_name: str = field(default_factory=lambda: os.getenv("APP_NAME", "Zaldo API"))
    environment: str = field(default_factory=lambda: os.getenv("ENVIRONMENT", "development"))
    backend_url: str = field(default_factory=lambda: os.getenv("BACKEND_URL", "http://localhost:8000"))
    frontend_url: str = field(default_factory=lambda: os.getenv("FRONTEND_URL", "http://localhost:3000"))
    secret_key: str = field(default_factory=lambda: os.getenv("SECRET_KEY", "changeme"))
    magic_link_expiration_minutes: int = field(default_factory=lambda: int(os.getenv("MAGIC_LINK_EXPIRATION_MINUTES", "15")))
    database_url: str = field(default_factory=lambda: os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./app.db"))
    alembic_database_url: Optional[str] = field(default_factory=lambda: os.getenv("ALEMBIC_DATABASE_URL"))
    resend_api_key: Optional[str] = field(default_factory=lambda: os.getenv("RESEND_API_KEY"))
    email_from: str = field(default_factory=lambda: os.getenv("EMAIL_FROM", "no-reply@zaldo.cl"))
    posthog_host: Optional[str] = field(default_factory=lambda: os.getenv("POSTHOG_HOST"))
    posthog_api_key: Optional[str] = field(default_factory=lambda: os.getenv("POSTHOG_API_KEY"))
    admin_emails: List[str] = field(default_factory=lambda: _split_admins(os.getenv("ADMIN_EMAILS", "")))
    rate_limit_per_minute: int = field(default_factory=lambda: int(os.getenv("RATE_LIMIT_PER_MINUTE", "5")))


@lru_cache()
def get_settings() -> Settings:
    return Settings()
