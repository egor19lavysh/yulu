from dataclasses import dataclass
from sqlalchemy.orm import selectinload
from hsk2.listening.models import *
from sqlalchemy import select
from database import get_db_session_async
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class ListeningRepository:
    db_session: AsyncSession

    async def get_listening_variants(self):
        """Получает все доступные варианты listening заданий"""
        variants = (await self.db_session.execute(select(ListeningHSK2))).scalars().all()
        return variants
    
    async def get_listening_variant(self, variant_id: int) -> ListeningHSK2:
        """Получает конкретный вариант по ID"""
        variant =(await self.db_session.execute(
                select(ListeningHSK2).where(ListeningHSK2.id == variant_id)
            )).scalars().first()
        return variant
    
    async def get_first_tasks_by_variant(self, variant_id: int):
        """Получает задания первого типа для варианта"""
        tasks =(await self.db_session.execute(
                select(FirstTaskHSK2)
                .options(selectinload(FirstTaskHSK2.questions))
                .where(FirstTaskHSK2.listening_var_id == variant_id)
            )).scalars().all()
        return tasks
    
    async def get_second_tasks_by_variant(self, variant_id: int):
        """Получает задания второго типа для варианта"""
        tasks =(await self.db_session.execute(
                select(SecondTaskHSK2)
                .options(selectinload(SecondTaskHSK2.questions))
                .where(SecondTaskHSK2.listening_var_id == variant_id)
            )).scalars().all()
        return tasks
    
    async def get_third_tasks_by_variant(self, variant_id: int):
        """Получает задания третьего типа для варианта"""
        tasks =(await self.db_session.execute(
                select(ThirdTaskHSK2)
                .options(
                    selectinload(ThirdTaskHSK2.questions).joinedload(ThirdTaskHSK2Question.options)
                )
                .where(ThirdTaskHSK2.listening_var_id == variant_id)
            )).scalars().all()
        return tasks


# Асинхронный контекстный менеджер для работы с репозиторием
async def get_listening_repository() -> ListeningRepository:
    """Фабрика для получения асинхронного репозитория"""
    async for session in get_db_session_async():
        return ListeningRepository(session)
