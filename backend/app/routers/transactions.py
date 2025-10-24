from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from ..core.dependencies import get_current_user
from ..core.database import get_session
from ..models.models import Transaction
from ..schemas.transaction import TransactionRead, TransactionUpdate

router = APIRouter(prefix="/transactions", tags=["Transacciones"])


@router.get("", response_model=list[TransactionRead])
async def list_transactions(
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    from_date: date | None = Query(default=None, alias="from"),
    to_date: date | None = Query(default=None, alias="to"),
    account_id: UUID | None = None,
):
    query = select(Transaction).where(Transaction.owner_email == current_user.email_pk)
    if from_date:
        query = query.where(Transaction.fecha_valor >= from_date)
    if to_date:
        query = query.where(Transaction.fecha_valor <= to_date)
    if account_id:
        query = query.where(Transaction.account_id == account_id)

    result = await session.execute(query.order_by(Transaction.fecha_valor.desc()))
    return result.scalars().all()


@router.patch("/{transaction_id}", response_model=TransactionRead)
async def update_transaction(transaction_id: UUID, payload: TransactionUpdate, current_user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Transaction).where(Transaction.id == transaction_id, Transaction.owner_email == current_user.email_pk)
    )
    transaction = result.scalar_one_or_none()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    data = payload.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(transaction, key, value)
    await session.commit()
    await session.refresh(transaction)
    return transaction
