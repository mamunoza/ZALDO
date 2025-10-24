from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import get_settings
from .routers import (
    accounts,
    admin,
    analytics,
    auth,
    feedback,
    importer,
    rules,
    transactions,
    uf,
    users,
    waitlist,
)

settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(waitlist.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(importer.router)
app.include_router(transactions.router)
app.include_router(rules.router)
app.include_router(analytics.router)
app.include_router(feedback.router)
app.include_router(uf.router)
app.include_router(admin.router)


@app.get("/")
async def root():
    return {"status": "ok", "name": settings.app_name}
