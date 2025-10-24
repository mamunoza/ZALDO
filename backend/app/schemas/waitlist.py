from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class WaitlistCreate(BaseModel):
    email: EmailStr
    source: Optional[str]
    notes: Optional[str]


class WaitlistEntry(BaseModel):
    email: EmailStr
    created_at: datetime
    source: Optional[str]
    notes: Optional[str]

    class Config:
        orm_mode = True
