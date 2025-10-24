from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..core.dependencies import get_current_user
from ..core.database import get_session
from ..models.models import Account
from ..schemas.importer import (
    ImportCommitRequest,
    ImportCommitResponse,
    ImportPreviewRequest,
    ImportPreviewResponse,
)
from ..services.importer import (
    ParsedRow,
    apply_rules,
    guess_mapping,
    load_dataframe,
    log_import,
    persist_transactions,
)
from ..utils.ingestion import normalize_amount, parse_date
from ..services.telemetry import track_event

router = APIRouter(prefix="/import", tags=["Importación"])


@router.post("/preview", response_model=ImportPreviewResponse)
async def import_preview(
    request: ImportPreviewRequest = Depends(),
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
):
    df = await load_dataframe(file, skip_rows=request.skip_rows)
    headers = list(df.columns)
    mapping = guess_mapping(headers)
    rows = df.fillna("").to_dict(orient="records")
    rows = rows[:50]
    return ImportPreviewResponse(headers=headers, rows=rows, suggested_mapping=mapping, duplicates=0)


@router.post("/commit", response_model=ImportCommitResponse)
async def import_commit(
    account_id: str = Form(...),
    mapping: str = Form(...),
    rules_enabled: bool = Form(True),
    template_name: str | None = Form(None),
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    import json

    mapping_data = json.loads(mapping)

    result = await session.execute(select(Account).where(Account.id == account_id, Account.owner_email == current_user.email_pk))
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    df = await load_dataframe(file)
    processed_rows: List[ParsedRow] = []
    total_rows = 0

    for _, row in df.iterrows():
        total_rows += 1
        descripcion = str(row.get(mapping_data.get("descripcion", ""), "")).strip()
        if descripcion.lower().startswith("total"):
            continue
        if not descripcion:
            continue
        fecha_raw = row.get(mapping_data.get("fecha", ""))
        try:
            fecha = parse_date(str(fecha_raw))
        except Exception:
            continue
        monto_value = row.get(mapping_data.get("monto", ""))
        monto = normalize_amount(monto_value)
        if "tipo" in row and str(row["tipo"]).lower() in {"cargo", "debito"}:
            monto = -abs(monto)
        descripcion_norm = " ".join(descripcion.split())
        parsed = ParsedRow(
            fecha_valor=fecha,
            fecha_contable=None,
            descripcion=descripcion_norm,
            referencia=str(row.get(mapping_data.get("referencia", ""), "")) or None,
            monto=-abs(monto) if monto < 0 else abs(monto),
            moneda=mapping_data.get("moneda", account.moneda) if mapping_data.get("moneda") else account.moneda,
            monto_original=monto,
        )
        processed_rows.append(parsed)

    processed, duplicates = await persist_transactions(session, current_user.email_pk, account, processed_rows)
    await log_import(session, current_user.email_pk, account, processed, duplicates, total_rows)
    await session.commit()
    if rules_enabled:
        await apply_rules()
    await track_event("import_success", current_user.email_pk, {"processed": processed, "duplicates": duplicates})
    return ImportCommitResponse(processed=processed, duplicates=duplicates, skipped=total_rows - processed - duplicates)
