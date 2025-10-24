from typing import Any, Dict, Optional
from uuid import UUID
from pydantic import BaseModel


class RuleBase(BaseModel):
    nombre: str
    prioridad: int
    condiciones: Dict[str, Any]
    acciones: Dict[str, Any]
    activo: bool = True


class RuleCreate(RuleBase):
    pass


class RuleRead(RuleBase):
    id: UUID

    class Config:
        orm_mode = True
