from collections import defaultdict
from datetime import date, datetime
from decimal import Decimal
from typing import Dict, List, Tuple

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.dependencies import get_current_user
from ..core.database import get_session
from ..models.models import Transaction, UFValue
from ..schemas.analytics import CategoryAnalyticsResponse, CategoryBreakdown, FlowResponse, FlowRow
from ..utils.analytics import month_range

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def month_key(dt: date) -> str:
    return dt.strftime("%Y-%m")


async def get_uf_values(session: AsyncSession, months: List[str]) -> Dict[str, Decimal]:
    if not months:
        return {}
    first_day = datetime.strptime(months[0], "%Y-%m").date().replace(day=1)
    last_month = datetime.strptime(months[-1], "%Y-%m").date().replace(day=1)
    if last_month.month == 12:
        last_day = date(last_month.year + 1, 1, 1)
    else:
        last_day = date(last_month.year, last_month.month + 1, 1)
    result = await session.execute(select(UFValue).where(UFValue.fecha >= first_day, UFValue.fecha < last_day))
    return {row.fecha.strftime("%Y-%m"): Decimal(row.valor_clp) for row in result.scalars()}


@router.get("/flow", response_model=FlowResponse)
async def flow(
    from_month: str = Query(..., alias="from"),
    to_month: str = Query(..., alias="to"),
    normalize: str | None = Query(default="CLP"),
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    months = month_range(from_month, to_month)
    if not months:
        raise HTTPException(status_code=400, detail="Rango inválido")

    start_date = datetime.strptime(from_month, "%Y-%m").date().replace(day=1)
    end_date = datetime.strptime(to_month, "%Y-%m").date().replace(day=28)

    result = await session.execute(
        select(Transaction).where(
            Transaction.owner_email == current_user.email_pk,
            Transaction.fecha_valor >= start_date,
            Transaction.fecha_valor <= end_date,
        )
    )
    transactions = result.scalars().all()
    uf_map = await get_uf_values(session, months)

    by_month: Dict[str, Dict[str, Decimal]] = defaultdict(lambda: {"ingresos": Decimal("0"), "egresos": Decimal("0")})
    for txn in transactions:
        key = txn.fecha_valor.strftime("%Y-%m")
        monto = Decimal(txn.monto_clp)
        if monto >= 0:
            by_month[key]["ingresos"] += monto
        else:
            by_month[key]["egresos"] += abs(monto)

    rows: List[FlowRow] = []
    saldo = Decimal("0")
    totals = {"ingresos": Decimal("0"), "egresos": Decimal("0"), "ahorro": Decimal("0")}

    for month in months:
        data = by_month[month]
        ingresos = data["ingresos"]
        egresos = data["egresos"]
        ahorro = ingresos - egresos
        totals["ingresos"] += ingresos
        totals["egresos"] += egresos
        totals["ahorro"] += ahorro
        saldo += ahorro
        porcentaje = float(ahorro / ingresos) if ingresos else 0.0

        if normalize and normalize.upper() == "UF":
            uf_value = uf_map.get(month)
            if uf_value:
                factor = Decimal(uf_value)
                ingresos = ingresos / factor
                egresos = egresos / factor
                ahorro = ahorro / factor
                saldo = saldo / factor

        rows.append(
            FlowRow(
                month=month,
                ingresos=float(ingresos),
                egresos=float(egresos),
                ahorro=float(ahorro),
                porcentaje_ahorro=float(porcentaje),
                saldo_acumulado=float(saldo),
            )
        )

    if normalize and normalize.upper() == "UF":
        converted_totals: Dict[str, float] = {}
        # Use last disponible UF para normalizar totales de manera aproximada
        last_uf = uf_map.get(months[-1])
        if last_uf:
            converted_totals = {k: float(v / Decimal(last_uf)) for k, v in totals.items()}
        else:
            converted_totals = {k: float(v) for k, v in totals.items()}
    else:
        converted_totals = {k: float(v) for k, v in totals.items()}

    return FlowResponse(rows=rows, totals=converted_totals)


@router.get("/categories", response_model=CategoryAnalyticsResponse)
async def categories(month: str, current_user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    target = datetime.strptime(month, "%Y-%m")
    start = target.replace(day=1).date()
    end = target.replace(day=28).date()
    result = await session.execute(
        select(Transaction).where(
            Transaction.owner_email == current_user.email_pk,
            Transaction.fecha_valor >= start,
            Transaction.fecha_valor <= end,
        )
    )
    transactions = result.scalars().all()
    totals: Dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    for txn in transactions:
        if txn.monto_clp >= 0:
            continue
        categoria = txn.categoria.nombre if txn.categoria else "Sin categoría"
        totals[categoria] += Decimal(abs(txn.monto_clp))
    breakdown = [CategoryBreakdown(categoria=name, monto=float(value)) for name, value in totals.items()]
    return CategoryAnalyticsResponse(month=month, breakdown=breakdown)
