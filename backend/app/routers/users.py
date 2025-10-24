from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..core.dependencies import get_current_user
from ..core.database import get_session
from ..models.models import User
from ..schemas.user import UserBase, UserUpdate

router = APIRouter(prefix="/me", tags=["Usuarios"])


@router.get("", response_model=UserBase)
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("", response_model=UserBase)
async def update_me(payload: UserUpdate, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    data = payload.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(current_user, key, value)
    await session.commit()
    await session.refresh(current_user)
    return current_user
