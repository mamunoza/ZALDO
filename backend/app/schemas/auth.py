from pydantic import BaseModel, EmailStr
from typing import Optional


class MagicLinkRequest(BaseModel):
    email: EmailStr
    invite_code: Optional[str] = None


class CallbackResponse(BaseModel):
    email: EmailStr
    verified: bool
    is_new_user: bool
