from dataclasses import dataclass
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from hsk4.writing.models import *
from sqlalchemy import select
from database import get_db_session_async


@dataclass
class WritingRepository:
    db_session: AsyncSession

    async def get_variants(self) -> list[WritingHSK4]:
        variants = (await self.db_session.execute(select(WritingHSK4))).scalars().all()
        return variants

    async def get_first_tasks_by_variant(self, variant_id: int) -> list[WritingFirstTaskHSK4]:
        tasks = (await self.db_session.execute(
                select(WritingFirstTaskHSK4)
                .where(WritingFirstTaskHSK4.writing_var_id == variant_id)
            )).scalars().all()
        return tasks

    async def get_second_task_by_variant(self, variant_id: int) -> WritingSecondTaskHSK4 | None:
        task = (await self.db_session.execute(
                select(WritingSecondTaskHSK4)
                .options(selectinload(WritingSecondTaskHSK4.words))
                .where(WritingSecondTaskHSK4.writing_var_id == variant_id)
            )).scalar_one_or_none()

        return task


async def get_writing_repository():
    async for session in get_db_session_async():
        return WritingRepository(session)