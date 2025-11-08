from dataclasses import dataclass
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from hsk5.listening.models import *
from sqlalchemy import select
from database import get_db_session_async


@dataclass
class ListeningRepository:
    db_session: AsyncSession

    async def get_listening_variants(self):
        """Получает все доступные варианты listening заданий"""
        variants = (await self.db_session.execute(select(ListeningHSK5))).scalars().all()
        return variants

    async def get_listening_variant(self, variant_id: int):
        """Получает конкретный вариант по ID"""
        variant = (await self.db_session.execute(
                select(ListeningHSK5).where(ListeningHSK5.id == variant_id)
            )).scalars().first()
        return variant

    async def get_first_tasks_by_variant(self, variant_id: int):
        """Получает задания первого типа для варианта"""
        tasks = (await self.db_session.execute(
                select(FirstTaskHSK5)
                .options(selectinload(FirstTaskHSK5.options))
                .where(FirstTaskHSK5.listening_var_id == variant_id)
            )).scalars().all()
        return tasks


async def get_listening_repository():
    async for session in get_db_session_async():
        return ListeningRepository(session)