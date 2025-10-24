from datetime import datetime, timedelta
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.dependencies import get_admin_user
from ..core.database import get_session
from ..models.models import ImportLog, Invite, User, WaitlistEntry
from ..schemas.invite import InviteCreate, InviteRead

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users")
async def admin_users(session: AsyncSession = Depends(get_session), admin=Depends(get_admin_user)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return [
        {
            "email": user.email_pk,
            "verificado": bool(user.email_verified_at),
            "activo": user.is_active,
            "ultima_sesion": user.last_login_at,
            "flags": user.flags,
        }
        for user in users
    ]


@router.post("/invites", response_model=InviteRead)
async def create_invite(payload: InviteCreate, admin=Depends(get_admin_user), session: AsyncSession = Depends(get_session)):
    code = uuid4().hex[:8]
    invite = Invite(
        code=code,
        created_by_email=admin.email_pk,
        max_uses=payload.max_uses,
    )
    session.add(invite)
    await session.commit()
    await session.refresh(invite)
    return invite


@router.post("/invites/{code}/revoke")
async def revoke_invite(code: str, admin=Depends(get_admin_user), session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Invite).where(Invite.code == code))
    invite = result.scalar_one_or_none()
    if not invite:
        raise HTTPException(status_code=404, detail="Invite no existe")
    invite.max_uses = 0
    await session.commit()
    return {"status": "revoked"}


@router.get("/metrics")
async def metrics(session: AsyncSession = Depends(get_session), admin=Depends(get_admin_user)):
    now = datetime.utcnow()
    last_7 = now - timedelta(days=7)
    last_30 = now - timedelta(days=30)

    total_waitlist = await session.execute(select(func.count()).select_from(WaitlistEntry))
    waitlist_count = total_waitlist.scalar() or 0

    active_7 = await session.execute(
        select(func.count()).select_from(User).where(User.last_login_at != None, User.last_login_at >= last_7)  # noqa: E711
    )
    active_30 = await session.execute(
        select(func.count()).select_from(User).where(User.last_login_at != None, User.last_login_at >= last_30)  # noqa: E711
    )

    imports_count = await session.execute(select(func.count()).select_from(ImportLog))

    return {
        "waitlist": waitlist_count,
        "activos_7d": active_7.scalar() or 0,
        "activos_30d": active_30.scalar() or 0,
        "importaciones": imports_count.scalar() or 0,
    }
