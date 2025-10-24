from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from ..core.database import get_session
from ..core.rate_limiter import rate_limiter
from ..core.security import (
    MagicTokenExpired,
    MagicTokenInvalid,
    decode_magic_token,
    expiration_datetime,
    generate_magic_token,
    generate_session_token,
)
from ..models.models import MagicToken, User, Invite
from ..schemas.auth import CallbackResponse, MagicLinkRequest
from ..services.email import send_email
from ..services.telemetry import track_event

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/magic-link", status_code=status.HTTP_202_ACCEPTED)
async def request_magic_link(payload: MagicLinkRequest, session: AsyncSession = Depends(get_session)):
    email = payload.email.lower()
    rate_limiter.check(f"magic:{email}")

    invite = None
    if payload.invite_code:
        result = await session.execute(select(Invite).where(Invite.code == payload.invite_code))
        invite = result.scalar_one_or_none()
        if not invite:
            raise HTTPException(status_code=404, detail="Invite not found")
        if invite.uses >= invite.max_uses:
            raise HTTPException(status_code=400, detail="Invite already used")

    result = await session.execute(select(User).where(User.email_pk == email))
    user = result.scalar_one_or_none()

    if not user and not invite:
        # waitlist fallback
        from ..models.models import WaitlistEntry
        existing_waitlist = await session.execute(select(WaitlistEntry).where(WaitlistEntry.email == email))
        if not existing_waitlist.scalar_one_or_none():
            session.add(WaitlistEntry(email=email))
            await session.commit()
        return {"status": "waitlisted", "message": "Te avisaremos pronto"}

    token = generate_magic_token(email)
    magic_token = MagicToken(id=uuid4(), email=email, token=token, expires_at=expiration_datetime())
    session.add(magic_token)
    await session.commit()

    from ..core.config import get_settings

    settings = get_settings()
    callback_link = f"{settings.frontend_url}/auth/callback?token={token}"
    if payload.invite_code:
        callback_link += f"&invite={payload.invite_code}"

    subject = "Tu acceso a Zaldo"
    html_body = f"""
        <p>Hola,</p>
        <p>Usa este enlace para ingresar a Zaldo:</p>
        <p><a href='{callback_link}'>Entrar ahora</a></p>
        <p>El enlace expira en {settings.magic_link_expiration_minutes} minutos.</p>
    """
    await send_email(email, subject, html_body)
    await track_event("magic_link_requested", email, {"invite": bool(invite)})

    return {"status": "sent"}


@router.get("/callback", response_model=CallbackResponse)
async def auth_callback(token: str, response: Response, invite: str | None = None, session: AsyncSession = Depends(get_session)):
    try:
        email = decode_magic_token(token).lower()
    except MagicTokenExpired:
        raise HTTPException(status_code=400, detail="Link expirado")
    except MagicTokenInvalid:
        raise HTTPException(status_code=400, detail="Link inválido")

    result = await session.execute(select(MagicToken).where(MagicToken.token == token))
    magic = result.scalar_one_or_none()
    if not magic or magic.used_at is not None:
        raise HTTPException(status_code=400, detail="Link ya utilizado")
    if magic.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Link expirado")

    result = await session.execute(select(User).where(User.email_pk == email))
    user = result.scalar_one_or_none()
    is_new = False

    if not user:
        user = User(email_pk=email, created_at=datetime.utcnow(), flags={"onboarding_step": 1})
        session.add(user)
        is_new = True

    user.email_verified_at = datetime.utcnow()
    user.last_login_at = datetime.utcnow()
    user.is_active = True

    if invite:
        result = await session.execute(select(Invite).where(Invite.code == invite))
        invite_obj = result.scalar_one_or_none()
        if invite_obj and invite_obj.uses < invite_obj.max_uses:
            invite_obj.uses += 1
            invite_obj.redeemed_by_email = email
            invite_obj.redeemed_at = datetime.utcnow()

    magic.used_at = datetime.utcnow()

    await session.commit()

    session_token = generate_session_token(email)
    response.set_cookie("zaldo_session", session_token, httponly=True, secure=False, samesite="lax")
    await track_event("signup" if is_new else "login", email, None)
    return CallbackResponse(email=email, verified=True, is_new_user=is_new)
