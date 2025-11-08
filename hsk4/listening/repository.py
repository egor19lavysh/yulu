from dataclasses import dataclass
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from hsk4.listening.models import *
from sqlalchemy import select
from database import get_db_session_async


@dataclass
class ListeningRepository:
    db_session: AsyncSession

    async def get_listening_variants(self):
        """Получает все доступные варианты listening заданий"""
        variants = (await self.db_session.execute(select(ListeningHSK4))).scalars().all()
        return variants

    async def get_listening_variant(self, variant_id: int):
        """Получает конкретный вариант по ID"""
        variant = (await self.db_session.execute(
                select(ListeningHSK4).where(ListeningHSK4.id == variant_id)
            )).scalars().first()
        return variant

    async def get_first_tasks_by_variant(self, variant_id: int):
        """Получает задания первого типа для варианта"""
        tasks = (await self.db_session.execute(
                select(FirstTaskHSK4)
                .where(FirstTaskHSK4.listening_var_id == variant_id)
            )).scalars().all()
        return tasks

    async def get_second_tasks_by_variant(self, variant_id: int):
        """Получает задания второго типа для варианта"""
        tasks = (await self.db_session.execute(
                select(SecondTaskHSK4)
                .options(selectinload(SecondTaskHSK4.options))
                .where(SecondTaskHSK4.listening_var_id == variant_id)
            )).scalars().all()
        return tasks

    async def get_third_tasks_by_variant(self, variant_id: int):
        """Получает задания третьего типа для варианта со всеми связанными данными"""
            # Загружаем ThirdTask вместе с вопросами и опциями
        tasks = (await self.db_session.execute(
                select(ThirdTaskHSK4)
                .options(
                    selectinload(ThirdTaskHSK4.options)
                )
                .where(ThirdTaskHSK4.listening_var_id == variant_id)
            )).scalars().all()
        return tasks


async def get_listening_repository():
    async for session in get_db_session_async():
        return ListeningRepository(session)