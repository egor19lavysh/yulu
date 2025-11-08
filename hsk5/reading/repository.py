from dataclasses import dataclass
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from hsk5.reading.models import *
from sqlalchemy import select
from database import get_db_session_async


@dataclass
class ReadingRepository:
    db_session: AsyncSession

    async def get_reading_variants(self) -> list[ReadingHSK5]:
        variants = (await self.db_session.execute(select(ReadingHSK5))).scalars().all()
        return variants

    async def get_first_tasks_by_variant(self, variant_id: int) -> list[ReadingFirstTaskHSK5]:
        tasks = (await self.db_session.execute(
                select(ReadingFirstTaskHSK5)
                .options(selectinload(ReadingFirstTaskHSK5.questions).joinedload(ReadingFirstTaskHSK5Question.options))
                .where(ReadingFirstTaskHSK5.reading_var_id == variant_id)
            )).scalars().all()
        return tasks

    async def get_second_tasks_by_variant(self, variant_id: int) -> list[ReadingSecondTaskHSK5]:
        tasks = (await self.db_session.execute(
                select(ReadingSecondTaskHSK5)
                .options(selectinload(ReadingSecondTaskHSK5.options))
                .where(ReadingSecondTaskHSK5.reading_var_id == variant_id)
            )).scalars().all()
        return tasks

    async def get_third_tasks_by_variant(self, variant_id: int) -> list[ReadingThirdTaskHSK5]:
            # Загружаем ThirdTask вместе с вопросами (и опциями внутри вопросов)
        tasks = (await self.db_session.execute(
                select(ReadingThirdTaskHSK5)
                .options(
                    selectinload(ReadingThirdTaskHSK5.questions).joinedload(ReadingThirdTaskHSK5Question.options)
                )
                .where(ReadingThirdTaskHSK5.reading_var_id == variant_id)
            )).scalars().all()
        return tasks


async def get_reading_repository():
    async for session in get_db_session_async():
        return ReadingRepository(session)