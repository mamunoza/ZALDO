from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from ..core.dependencies import get_current_user
from ..core.database import get_session
from ..models.models import Account
from ..schemas.account import AccountCreate, AccountRead

router = APIRouter(prefix="/accounts", tags=["Cuentas"])


@router.get("", response_model=list[AccountRead])
async def list_accounts(current_user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Account).where(Account.owner_email == current_user.email_pk))
    accounts = result.scalars().all()
    return accounts


@router.post("", response_model=AccountRead)
async def create_account(payload: AccountCreate, current_user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    account = Account(
        id=uuid4(),
        owner_email=current_user.email_pk,
        nombre=payload.nombre,
        tipo=payload.tipo,
        institucion=payload.institucion,
        moneda=payload.moneda,
    )
    session.add(account)
    await session.commit()
    await session.refresh(account)
    return account
