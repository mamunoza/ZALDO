from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


class FeedbackCreate(BaseModel):
    mensaje: str
    email_contacto: Optional[EmailStr]


class FeedbackRead(BaseModel):
    id: UUID
    owner_email: Optional[EmailStr]
    mensaje: str
    email_contacto: Optional[EmailStr]
    created_at: datetime

    class Config:
        orm_mode = True
