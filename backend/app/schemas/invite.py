from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class InviteCreate(BaseModel):
    max_uses: int = 1


class InviteRead(BaseModel):
    code: str
    created_at: datetime
    created_by_email: EmailStr
    redeemed_by_email: Optional[EmailStr]
    redeemed_at: Optional[datetime]
    max_uses: int
    uses: int

    class Config:
        orm_mode = True
