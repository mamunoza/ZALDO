from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class AccountBase(BaseModel):
    nombre: str
    tipo: str
    institucion: Optional[str]
    moneda: str = "CLP"


class AccountCreate(AccountBase):
    pass


class AccountRead(AccountBase):
    id: UUID
    owner_email: str

    class Config:
        orm_mode = True
