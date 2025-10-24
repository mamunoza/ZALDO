from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel


class TransactionRead(BaseModel):
    id: UUID
    owner_email: str
    account_id: UUID
    fecha_valor: date
    fecha_contable: Optional[date]
    descripcion: str
    referencia: Optional[str]
    monto_clp: Decimal
    moneda_original: Optional[str]
    monto_original: Optional[Decimal]
    categoria_id: Optional[UUID]
    etiquetas: List[str]
    hash_dedup: str
    created_at: datetime

    class Config:
        orm_mode = True


class TransactionUpdate(BaseModel):
    categoria_id: Optional[UUID]
    etiquetas: Optional[List[str]]
