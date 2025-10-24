from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from datetime import datetime, timedelta

from .config import get_settings

settings = get_settings()


def _sign(data: dict, salt: str) -> str:
    payload = json.dumps(data, separators=(",", ":"))
    message = f"{salt}:{payload}".encode("utf-8")
    signature = hmac.new(settings.secret_key.encode("utf-8"), message, hashlib.sha256).digest()
    token = base64.urlsafe_b64encode(payload.encode("utf-8")).decode("utf-8").rstrip("=")
    sig = base64.urlsafe_b64encode(signature).decode("utf-8").rstrip("=")
    return f"{token}.{sig}"


def _unsign(token: str, salt: str, max_age: int | None = None) -> dict:
    try:
        token_part, sig_part = token.split(".")
    except ValueError as exc:  # pragma: no cover
        raise MagicTokenInvalid() from exc
    payload_bytes = base64.urlsafe_b64decode(token_part + "==")
    payload = payload_bytes.decode("utf-8")
    expected_sig = hmac.new(settings.secret_key.encode("utf-8"), f"{salt}:{payload}".encode("utf-8"), hashlib.sha256).digest()
    signature = base64.urlsafe_b64decode(sig_part + "==")
    if not hmac.compare_digest(signature, expected_sig):
        raise MagicTokenInvalid()
    data = json.loads(payload)
    if max_age is not None and int(time.time()) - data.get("ts", 0) > max_age:
        raise MagicTokenExpired()
    return data


def generate_magic_token(email: str) -> str:
    payload = {"email": email, "ts": int(time.time())}
    return _sign(payload, "magic")


def verify_magic_token(token: str) -> str:
    data = _unsign(token, "magic", settings.magic_link_expiration_minutes * 60)
    return data["email"]


def generate_session_token(email: str) -> str:
    payload = {"email": email, "ts": int(time.time())}
    return _sign(payload, "session")


def verify_session_token(token: str) -> str:
    data = _unsign(token, "session", 60 * 60 * 24 * 30)
    return data["email"]


def expiration_datetime() -> datetime:
    return datetime.utcnow() + timedelta(minutes=settings.magic_link_expiration_minutes)


class MagicTokenError(Exception):
    pass


class MagicTokenExpired(MagicTokenError):
    pass


class MagicTokenInvalid(MagicTokenError):
    pass


class SessionTokenError(Exception):
    pass


def decode_magic_token(token: str) -> str:
    try:
        return verify_magic_token(token)
    except MagicTokenExpired as exc:
        raise MagicTokenExpired() from exc
    except MagicTokenInvalid as exc:
        raise MagicTokenInvalid() from exc


def decode_session_token(token: str) -> str:
    try:
        return verify_session_token(token)
    except MagicTokenError as exc:
        raise SessionTokenError(str(exc)) from exc
