from datetime import date
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.dependencies import get_admin_user
from ..core.database import get_session
from ..models.models import UFValue

router = APIRouter(prefix="/uf", tags=["UF"])


@router.get("")
async def list_uf(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(UFValue).order_by(UFValue.fecha.desc()))
    return [
        {"fecha": row.fecha.isoformat(), "valor_clp": float(row.valor_clp)}
        for row in result.scalars().all()
    ]


@router.post("", dependencies=[Depends(get_admin_user)])
async def upsert_uf(values: List[dict], session: AsyncSession = Depends(get_session)):
    for value in values:
        fecha = date.fromisoformat(value["fecha"])
        result = await session.execute(select(UFValue).where(UFValue.fecha == fecha))
        uf = result.scalar_one_or_none()
        if uf:
            uf.valor_clp = value["valor_clp"]
        else:
            session.add(UFValue(fecha=fecha, valor_clp=value["valor_clp"]))
    await session.commit()
    return {"status": "ok"}
