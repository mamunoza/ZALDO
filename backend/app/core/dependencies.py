from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .database import get_session
from .security import decode_session_token, SessionTokenError
from ..models.models import User


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    session_token: str | None = Cookie(default=None, alias="zaldo_session"),
) -> User:
    if not session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        email = decode_session_token(session_token)
    except SessionTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    result = await session.execute(select(User).where(User.email_pk == email))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return user


async def get_admin_user(user: User = Depends(get_current_user)) -> User:
    from ..core.config import get_settings

    settings = get_settings()
    if user.email_pk not in settings.admin_emails:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    return user
