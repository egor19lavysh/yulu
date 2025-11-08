from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from hsk1.listening.models import *
from database import get_db_session_async


@dataclass
class AsyncListeningRepository:
    db_session: AsyncSession

    async def get_listening_variants(self):
        """Получает все доступные варианты listening заданий"""
        result = await self.db_session.execute(select(ListeningHSK1))
        variants = result.scalars().all()
        return variants

    async def get_listening_variant(self, variant_id: int) -> ListeningHSK1:
        """Получает конкретный вариант по ID"""
        result = await self.db_session.execute(
            select(ListeningHSK1).where(ListeningHSK1.id == variant_id)
        )
        variant = result.scalars().first()
        return variant

    async def get_first_tasks_by_variant(self, variant_id: int):
        """Получает задания первого типа для варианта"""
        result = await self.db_session.execute(
            select(FirstTaskHSK1)
            .options(selectinload(FirstTaskHSK1.questions))
            .where(FirstTaskHSK1.listening_var_id == variant_id)
        )
        tasks = result.scalars().all()
        return tasks

    async def get_second_tasks_by_variant(self, variant_id: int):
        """Получает задания второго типа для варианта"""
        result = await self.db_session.execute(
            select(SecondTaskHSK1)
            .options(selectinload(SecondTaskHSK1.questions))
            .where(SecondTaskHSK1.listening_var_id == variant_id)
        )
        tasks = result.scalars().all()
        return tasks
    
    async def get_third_tasks_by_variant(self, variant_id: int):
        """Получает задания третьего типа для варианта"""
        result = await self.db_session.execute(
            select(ThirdTaskHSK1)
            .options(selectinload(ThirdTaskHSK1.questions))
            .where(ThirdTaskHSK1.listening_var_id == variant_id)
        )
        tasks = result.scalars().all()
        return tasks
    
    async def get_fourth_tasks_by_variant(self, variant_id: int):
        """Получает задания четвертого типа для варианта со всеми связанными данными"""
        result = await self.db_session.execute(
            select(FourthTaskHSK1)
            .options(
                selectinload(FourthTaskHSK1.questions)
                    .selectinload(FourthTaskHSK1Question.options)
            )
            .where(FourthTaskHSK1.listening_var_id == variant_id)
        )
        tasks = result.scalars().all()
        return tasks

    async def close(self):
        """Закрывает сессию (если нужно управлять вручную)"""
        await self.db_session.close()


# Асинхронный контекстный менеджер для работы с репозиторием
async def get_listening_repository() -> AsyncListeningRepository:
    """Фабрика для получения асинхронного репозитория"""
    async for session in get_db_session_async():
        return AsyncListeningRepository(session)

