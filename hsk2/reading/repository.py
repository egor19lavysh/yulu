from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from hsk2.reading.models import *
from sqlalchemy import select
from database import get_db_session_async


@dataclass
class ReadingRepository:
    db_session: AsyncSession

    async def get_reading_variants(self):
        """Получает все доступные варианты listening заданий"""
        
        variants = (await self.db_session.execute(select(ReadingHSK2))).scalars().all()
        return variants
    
    async def get_reading_variant(self, variant_id: int) -> ReadingHSK2:
        """Получает конкретный вариант по ID"""
        
        variant = (await self.db_session.execute(
                select(ReadingHSK2).where(ReadingHSK2.id == variant_id)
            )).scalars().first()
        return variant
    
    async def get_first_tasks_by_variant(self, variant_id: int):
        """Получает задания первого типа для варианта"""
        
        tasks = (await self.db_session.execute(
                select(ReadingFirstTaskHSK2)
                .options(selectinload(ReadingFirstTaskHSK2.sentences))
                .where(ReadingFirstTaskHSK2.reading_var_id == variant_id)
            )).scalars().all()
        return tasks
    
    async def get_second_tasks_by_variant(self, variant_id: int):
        """Получает задания второго типа для варианта"""
        
        tasks = (await self.db_session.execute(
                select(ReadingSecondTaskHSK2)
                .options(
                    selectinload(ReadingSecondTaskHSK2.sentences),
                    selectinload(ReadingSecondTaskHSK2.options)
                )
                .where(ReadingSecondTaskHSK2.reading_var_id == variant_id)
            )).scalars().all()
        return tasks
    
    async def get_third_tasks_by_variant(self, variant_id: int):
        """Получает задания третьего типа для варианта"""
        
        tasks = (await self.db_session.execute(
                select(ReadingThirdTaskHSK2)
                .where(ReadingThirdTaskHSK2.reading_var_id == variant_id)
            )).scalars().all()
        return tasks
    
    async def get_fourth_tasks_by_variant(self, variant_id: int) -> list[ReadingFourthTaskHSK2]:
        """Получает задания четвертого типа для варианта со всеми связанными данными"""
        
            # Загружаем ReadingFourthTaskHSK1 вместе с вопросами и опциями
        tasks = (await self.db_session.execute(
                select(ReadingFourthTaskHSK2)
                .options(
                    selectinload(ReadingFourthTaskHSK2.questions),
                    selectinload(ReadingFourthTaskHSK2.options)  # Загружаем опции для каждого вопроса
                )
                .where(ReadingFourthTaskHSK2.reading_var_id == variant_id)
            )).scalars().all()
        return tasks


async def get_reading_repository():
    async for session in get_db_session_async():
        return ReadingRepository(session)