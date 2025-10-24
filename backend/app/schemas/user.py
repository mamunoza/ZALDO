from datetime import datetime
from typing import Optional, Any, Dict
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email_pk: EmailStr
    nombre: Optional[str]
    tz: str = "America/Santiago"
    moneda_base: str = "CLP"
    email_verified_at: Optional[datetime]
    created_at: datetime
    last_login_at: Optional[datetime]
    is_active: bool
    flags: Dict[str, Any]

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    nombre: Optional[str]
    tz: Optional[str]
    moneda_base: Optional[str]
    flags: Optional[Dict[str, Any]]
