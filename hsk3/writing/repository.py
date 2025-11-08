from dataclasses import dataclass
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db_session_async
from .models import *


@dataclass
class WritingRepository:
    db_session: AsyncSession

    async def get_variants(self) -> list[Writing]:
        variants = list((await self.db_session.execute(select(Writing))).scalars().all())
        return variants

    async def get_variant_by_id(self, variant_id: int) -> Writing | None:
        stmt = select(Writing).where(Writing.id == variant_id).options(
                selectinload(Writing.first_tasks),
                selectinload(Writing.second_tasks)
            )
        variant = (await self.db_session.execute(stmt)).scalar_one_or_none()
        return variant


async def get_writing_repository():
    async for session in get_db_session_async():
        return WritingRepository(session)