from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from io import BytesIO, StringIO
from typing import Dict, List, Optional, Tuple
from uuid import uuid4

try:
    import pandas as pd
except ModuleNotFoundError:  # pragma: no cover
    pd = None  # type: ignore

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.models import Account, ImportLog, Transaction
from ..utils.ingestion import compute_hash, normalize_amount, parse_date


@dataclass
class ParsedRow:
    fecha_valor: datetime
    fecha_contable: Optional[datetime]
    descripcion: str
    referencia: Optional[str]
    monto: Decimal
    moneda: str
    monto_original: Optional[Decimal]


DEFAULT_MAPPING = {
    "fecha": ["fecha", "date", "fecha_valor"],
    "descripcion": ["descripcion", "detalle", "description"],
    "monto": ["monto", "amount"],
}


def guess_mapping(headers: List[str]) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for target, candidates in DEFAULT_MAPPING.items():
        for header in headers:
            if header.lower() in candidates:
                mapping[target] = header
                break
    return mapping


async def load_dataframe(upload: UploadFile, skip_rows: int = 0) -> "pd.DataFrame":
    if pd is None:  # pragma: no cover
        raise RuntimeError("pandas no está disponible en este entorno")
    if upload.filename and upload.filename.lower().endswith(".xlsx"):
        data = await upload.read()
        df = pd.read_excel(BytesIO(data), skiprows=skip_rows)
    else:
        content = (await upload.read()).decode("utf-8", errors="ignore")
        df = pd.read_csv(StringIO(content), skiprows=skip_rows, sep=None, engine="python")
    df = df.dropna(how="all")
    df = df.head(50)
    return df


async def persist_transactions(
    session: AsyncSession,
    owner_email: str,
    account: Account,
    rows: List[ParsedRow],
) -> Tuple[int, int]:
    processed = 0
    duplicates = 0
    for row in rows:
        hash_value = compute_hash(owner_email, str(account.id), row.fecha_valor, row.monto, row.descripcion)
        result = await session.execute(select(Transaction).where(Transaction.hash_dedup == hash_value))
        if result.scalar_one_or_none():
            duplicates += 1
            continue
        txn = Transaction(
            id=uuid4(),
            owner_email=owner_email,
            account_id=account.id,
            fecha_valor=row.fecha_valor.date(),
            fecha_contable=row.fecha_contable.date() if row.fecha_contable else None,
            descripcion=row.descripcion,
            referencia=row.referencia,
            monto_clp=row.monto,
            moneda_original=row.moneda,
            monto_original=row.monto_original,
            hash_dedup=hash_value,
            etiquetas=[],
        )
        session.add(txn)
        processed += 1
    return processed, duplicates


async def log_import(session: AsyncSession, owner_email: str, account: Account, processed: int, duplicates: int, total: int) -> None:
    log = ImportLog(
        id=uuid4(),
        owner_email=owner_email,
        account_id=account.id,
        processed_rows=processed,
        duplicate_rows=duplicates,
        total_rows=total,
    )
    session.add(log)


async def apply_rules(*args, **kwargs):
    # Placeholder for future ML/rules engine
    return
