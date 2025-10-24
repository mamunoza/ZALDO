import asyncio
from datetime import date
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import AsyncSessionLocal
from backend.app.models.models import Category, Invite, UFValue


async def seed_categories(session: AsyncSession, owner_email: str):
    existing = await session.execute(select(Category).where(Category.owner_email == owner_email))
    if existing.scalars().first():
        return
    categories = [
        ("Sueldo", "income"),
        ("Arriendo", "expense"),
        ("Supermercado", "expense"),
        ("Suscripciones", "expense"),
    ]
    for name, tipo in categories:
        session.add(Category(id=uuid4(), owner_email=owner_email, nombre=name, tipo=tipo))


async def seed_uf(session: AsyncSession):
    for month in range(1, 13):
        fecha = date(2025, month, 1)
        result = await session.execute(select(UFValue).where(UFValue.fecha == fecha))
        if result.scalar_one_or_none():
            continue
        session.add(UFValue(fecha=fecha, valor_clp=35000 + month * 50))


async def seed_invites(session: AsyncSession):
    for suffix in ["beta1", "beta2", "amigo"]:
        code = f"{suffix}"
        result = await session.execute(select(Invite).where(Invite.code == code))
        if result.scalar_one_or_none():
            continue
        session.add(Invite(code=code, created_by_email="founder@zaldo.cl", max_uses=5))


async def main():
    async with AsyncSessionLocal() as session:
        await seed_uf(session)
        await seed_invites(session)
        await seed_categories(session, "demo@zaldo.cl")
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
