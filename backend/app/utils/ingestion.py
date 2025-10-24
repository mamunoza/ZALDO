from __future__ import annotations

from datetime import datetime
from decimal import Decimal

try:
    import pandas as pd
except ModuleNotFoundError:  # pragma: no cover
    pd = None  # type: ignore


def parse_date(value: str) -> datetime:
    formats = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"]
    for fmt in formats:
        try:
            return datetime.strptime(str(value), fmt)
        except ValueError:
            continue
    return datetime.fromisoformat(str(value))


def normalize_amount(value: str | float | int) -> Decimal:
    if pd is not None and pd.isna(value):
        return Decimal("0")
    if isinstance(value, (int, float)):
        return Decimal(str(value))
    value = str(value).replace(".", "").replace(",", ".")
    return Decimal(value)


def compute_hash(owner_email: str, account_id: str, fecha_valor: datetime, monto: Decimal, descripcion: str) -> str:
    import hashlib

    normalized_desc = " ".join(descripcion.lower().split())
    payload = f"{owner_email}|{account_id}|{fecha_valor.date()}|{monto}|{normalized_desc}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
