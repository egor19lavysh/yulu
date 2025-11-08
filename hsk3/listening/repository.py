from dataclasses import dataclass
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from hsk3.listening.models import *
from sqlalchemy import select
from database import get_db_session_async


@dataclass
class ListeningRepository:
    db_session: AsyncSession

    async def get_listening_variants(self):
        """Получает все доступные варианты listening заданий"""
        variants = (await self.db_session.execute(select(Listening))).scalars().all()
        return variants

    async def get_listening_variant(self, variant_id: int):
        """Получает конкретный вариант по ID"""
        variant = (await self.db_session.execute(
                select(Listening).where(Listening.id == variant_id)
            )).scalars().first()
        return variant

    async def get_first_tasks_by_variant(self, variant_id: int):
        """Получает задания первого типа для варианта"""
        tasks = (await self.db_session.execute(
                select(FirstTask)
                .options(selectinload(FirstTask.questions))  # Загружаем связанные вопросы
                .where(FirstTask.listening_var_id == variant_id)
            )).scalars().all()
        return tasks

    async def get_second_tasks_by_variant(self, variant_id: int):
        """Получает задания второго типа для варианта"""
        tasks = (await self.db_session.execute(
                select(SecondTask)
                .where(SecondTask.listening_var_id == variant_id)
            )).scalars().all()
        return tasks

    async def get_third_tasks_by_variant(self, variant_id: int):
        """Получает задания третьего типа для варианта со всеми связанными данными"""
        # Загружаем ThirdTask вместе с вопросами и опциями
        tasks = (await self.db_session.execute(
                select(ThirdTask)
                .options(
                    selectinload(ThirdTask.questions)
                        .selectinload(ThirdTaskQuestion.options)  # Загружаем опции для каждого вопроса
                )
                .where(ThirdTask.listening_var_id == variant_id)
            )).scalars().all()
        return tasks

    # Метод для тестирования (если используется)
    async def get_first_task_by_variant(self, variant_id: int):
        """Получает первое задание первого типа для варианта (для тестирования)"""
        task = (await self.db_session.execute(
                select(FirstTask)
                .options(selectinload(FirstTask.questions))
                .where(FirstTask.listening_var_id == variant_id)
            )).scalars().first()
        return task



async def get_listening_repository():
    async for session in get_db_session_async():
        return ListeningRepository(session)