import random
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass
from .models import Reading, ReadingFirstTask, ReadingSecondTask, \
    ReadingThirdTask  # Предполагается, что модели находятся в models.py
from database import get_db_session_async


@dataclass
class ReadingRepository:
    db_session: AsyncSession

    async def get_reading_variants(self) -> list[Reading]:
        variants = (await self.db_session.execute(select(Reading).options(
                # Загружаем First Tasks и связанные данные
                selectinload(Reading.first_tasks)
                .selectinload(ReadingFirstTask.options),
                selectinload(Reading.first_tasks)
                .selectinload(ReadingFirstTask.questions),
                # Загружаем Second Tasks и связанные данные
                selectinload(Reading.second_tasks)
                .selectinload(ReadingSecondTask.options),
                selectinload(Reading.second_tasks)
                .selectinload(ReadingSecondTask.questions),
                # Загружаем Third Tasks и связанные данные
                selectinload(Reading.third_tasks)
                .selectinload(ReadingThirdTask.options)
            ))).scalars().all()
        return list(variants)

    async def get_reading_variant(self, variant_id: int) -> Reading | None:
        """Получает полный вариант Reading по ID."""
        stmt = (
                select(Reading)
                .where(Reading.id == variant_id)
                .options(
                    # Загружаем First Tasks и связанные данные
                    selectinload(Reading.first_tasks)
                    .selectinload(ReadingFirstTask.options),
                    selectinload(Reading.first_tasks)
                    .selectinload(ReadingFirstTask.questions),
                    # Загружаем Second Tasks и связанные данные
                    selectinload(Reading.second_tasks)
                    .selectinload(ReadingSecondTask.options),
                    selectinload(Reading.second_tasks)
                    .selectinload(ReadingSecondTask.questions),
                    # Загружаем Third Tasks и связанные данные
                    selectinload(Reading.third_tasks)
                    .selectinload(ReadingThirdTask.options)
                )
            )
        return (await self.db_session.execute(stmt)).scalar_one_or_none()

    async def get_random_reading_variant_with_tasks(self) -> Reading | None:
        """
        Получает случайный вариант Reading с заданиями.
        Предполагает, что у вас есть записи в таблице reading_tasks.
        """
            # Получаем все ID вариантов
        variant_ids_result = (await self.db_session.execute(select(Reading.id))).scalars().all()
        if not variant_ids_result:
            return None
            # Выбираем случайный ID
        random_variant_id = random.choice(variant_ids_result)

            # Загружаем вариант с заданиями
        stmt = (
                select(Reading)
                .where(Reading.id == random_variant_id)
                .options(
                    selectinload(Reading.first_tasks)
                    .selectinload(ReadingFirstTask.options),
                    selectinload(Reading.first_tasks)
                    .selectinload(ReadingFirstTask.questions),
                    selectinload(Reading.second_tasks)
                    .selectinload(ReadingSecondTask.options),
                    selectinload(Reading.second_tasks)
                    .selectinload(ReadingSecondTask.questions),
                    selectinload(Reading.third_tasks)
                    .selectinload(ReadingThirdTask.options)
                )
            )
        return (await self.db_session.execute(stmt)).scalar_one_or_none()

    async def get_first_tasks_by_variant(self, variant_id: int) -> list[ReadingFirstTask]:
        """Получает все задания типа 1 для указанного варианта"""
        stmt = (
                select(ReadingFirstTask)
                .join(ReadingFirstTask.reading_var)
                .where(Reading.id == variant_id)
                .options(
                    selectinload(ReadingFirstTask.options),
                    selectinload(ReadingFirstTask.questions)
                ))
        return list((await self.db_session.execute(stmt)).scalars().all())

    async def get_second_tasks_by_variant(self, variant_id: int) -> list[ReadingSecondTask]:
        """Получает все задания типа 2 для указанного варианта"""
        stmt = (
                select(ReadingSecondTask)
                .join(ReadingSecondTask.reading_var)
                .where(Reading.id == variant_id)
                .options(
                    selectinload(ReadingSecondTask.options),
                    selectinload(ReadingSecondTask.questions)
                ))
        return list((await self.db_session.execute(stmt)).scalars().all())

    async def get_third_tasks_by_variant(self, variant_id: int) -> list[ReadingThirdTask]:
        """Получает все задания типа 3 для указанного варианта"""
        stmt = (
                select(ReadingThirdTask)
                .join(ReadingThirdTask.reading_var)
                .where(Reading.id == variant_id)
                .options(
                    selectinload(ReadingThirdTask.options)
                )
            )
        return list((await self.db_session.execute(stmt)).scalars().all())


async def get_reading_repository():
    async for session in get_db_session_async():
        return ReadingRepository(session)