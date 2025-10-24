from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID, uuid4

from ..core.dependencies import get_current_user
from ..core.database import get_session
from ..models.models import Rule
from ..schemas.rule import RuleCreate, RuleRead
from ..services.telemetry import track_event

router = APIRouter(prefix="/rules", tags=["Rules"])


@router.get("", response_model=list[RuleRead])
async def list_rules(current_user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Rule).where(Rule.owner_email == current_user.email_pk).order_by(Rule.prioridad))
    return result.scalars().all()


@router.post("", response_model=RuleRead)
async def create_rule(payload: RuleCreate, current_user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    rule = Rule(
        id=uuid4(),
        owner_email=current_user.email_pk,
        nombre=payload.nombre,
        prioridad=payload.prioridad,
        condiciones=payload.condiciones,
        acciones=payload.acciones,
        activo=payload.activo,
    )
    session.add(rule)
    await session.commit()
    await session.refresh(rule)
    await track_event("rule_created", current_user.email_pk, {"rule_id": str(rule.id)})
    return rule


@router.patch("/{rule_id}", response_model=RuleRead)
async def update_rule(rule_id: UUID, payload: RuleCreate, current_user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Rule).where(Rule.id == rule_id, Rule.owner_email == current_user.email_pk))
    rule = result.scalar_one_or_none()
    if not rule:
        raise HTTPException(status_code=404, detail="Regla no encontrada")
    data = payload.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(rule, key, value)
    await session.commit()
    await session.refresh(rule)
    return rule


@router.post("/reprocess")
async def reprocess_rules(current_user=Depends(get_current_user)):
    # Placeholder to trigger background job
    return {"status": "queued"}
