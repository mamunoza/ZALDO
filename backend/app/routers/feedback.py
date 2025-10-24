from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.dependencies import get_current_user
from ..core.database import get_session
from ..models.models import Feedback
from ..schemas.feedback import FeedbackCreate
from ..services.email import send_email

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("", status_code=201)
async def submit_feedback(
    payload: FeedbackCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
):
    feedback = Feedback(
        id=uuid4(),
        owner_email=user.email_pk,
        mensaje=payload.mensaje,
        email_contacto=payload.email_contacto or user.email_pk,
    )
    session.add(feedback)
    await session.commit()
    await send_email(
        user.email_pk,
        "Gracias por tu feedback",
        f"<p>Recibimos tu mensaje:</p><blockquote>{payload.mensaje}</blockquote>",
    )
    return {"status": "received"}
