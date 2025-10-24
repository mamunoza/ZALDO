from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from ..core.database import get_session
from ..models.models import WaitlistEntry
from ..schemas.waitlist import WaitlistCreate

router = APIRouter(prefix="/waitlist", tags=["Waitlist"])


@router.post("", status_code=201)
async def join_waitlist(payload: WaitlistCreate, session: AsyncSession = Depends(get_session)):
    email = payload.email.lower()
    result = await session.execute(select(WaitlistEntry).where(WaitlistEntry.email == email))
    entry = result.scalar_one_or_none()
    if entry:
        return {"status": "existing"}
    entry = WaitlistEntry(email=email, source=payload.source, notes=payload.notes, created_at=datetime.utcnow())
    session.add(entry)
    await session.commit()
    return {"status": "added"}
