from datetime import date
from typing import Dict, List
from pydantic import BaseModel


class FlowRow(BaseModel):
    month: str
    ingresos: float
    egresos: float
    ahorro: float
    porcentaje_ahorro: float
    saldo_acumulado: float


class FlowResponse(BaseModel):
    rows: List[FlowRow]
    totals: Dict[str, float]


class CategoryBreakdown(BaseModel):
    categoria: str
    monto: float


class CategoryAnalyticsResponse(BaseModel):
    month: str
    breakdown: List[CategoryBreakdown]
