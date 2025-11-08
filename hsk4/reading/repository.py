from dataclasses import dataclass
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from hsk4.reading.models import *
from sqlalchemy import select
from database import get_db_session_async


@dataclass
class ReadingRepository:
    db_session: AsyncSession

    async def get_reading_variants(self) -> list[ReadingHSK4]:
        variants = (await self.db_session.execute(select(ReadingHSK4))).scalars().all()
        return variants

    async def get_first_tasks_by_variant(self, variant_id: int) -> list[ReadingFirstTaskHSK4]:
        tasks = (await self.db_session.execute(
                select(ReadingFirstTaskHSK4)
                .options(selectinload(ReadingFirstTaskHSK4.options),
                         selectinload(ReadingFirstTaskHSK4.sentences))
                .where(ReadingFirstTaskHSK4.reading_var_id == variant_id)
            )).scalars().all()
        return tasks

    async def get_second_tasks_by_variant(self, variant_id: int) -> list[ReadingSecondTaskHSK4]:
        tasks = (await self.db_session.execute(
                select(ReadingSecondTaskHSK4)
                .options(selectinload(ReadingSecondTaskHSK4.options))
                .where(ReadingSecondTaskHSK4.reading_var_id == variant_id)
            )).scalars().all()
        return tasks

    async def get_third_tasks_by_variant(self, variant_id: int) -> list[ReadingThirdTaskHSK4]:
            # Загружаем ThirdTask вместе с вопросами (и опциями внутри вопросов)
        tasks = (await self.db_session.execute(
                select(ReadingThirdTaskHSK4)
                .options(
                    selectinload(ReadingThirdTaskHSK4.questions).joinedload(ReadingThirdTaskQuestionHSK4.options)
                )
                .where(ReadingThirdTaskHSK4.reading_var_id == variant_id)
            )).scalars().all()
        return tasks


async def get_reading_repository():
    async for session in get_db_session_async():
        return ReadingRepository(session)