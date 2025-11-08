from dataclasses import dataclass
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from hsk5.writing.models import *
from sqlalchemy import select
from database import get_db_session_async


@dataclass
class WritingRepository:
    db_session: AsyncSession

    async def get_variants(self) -> list[WritingHSK5]:
        variants = (await self.db_session.execute(select(WritingHSK5))).scalars().all()
        return variants

    async def get_first_tasks_by_variant(self, variant_id: int) -> list[WritingFirstTaskHSK5]:
        tasks = (await self.db_session.execute(
                select(WritingFirstTaskHSK5)
                .where(WritingFirstTaskHSK5.writing_var_id == variant_id)
            )).scalars().all()
        return tasks

    async def get_second_tasks_by_variant(self, variant_id: int) -> list[WritingSecondTaskHSK5]:
        tasks = (await self.db_session.execute(
                select(WritingSecondTaskHSK5)
                .where(WritingSecondTaskHSK5.writing_var_id == variant_id)
            )).scalars().all()
        return tasks
    
    async def get_third_tasks_by_variant(self, variant_id: int) -> list[WritingThirdTaskHSK5]:
        tasks = (await self.db_session.execute(
                select(WritingThirdTaskHSK5)
                .where(WritingThirdTaskHSK5.writing_var_id == variant_id)
            )).scalars().all()
        return tasks


async def get_writing_repository():
    async for session in get_db_session_async():
        return WritingRepository(session)