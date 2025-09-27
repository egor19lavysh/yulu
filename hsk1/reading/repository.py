from dataclasses import dataclass
from sqlalchemy.orm import Session, selectinload
from typing import List
from hsk1.reading.models import *
from sqlalchemy import select
from database import get_db_session


@dataclass
class ReadingRepository:
    db_session: Session

    def get_reading_variants(self) -> list[ReadingHSK1]:
        """Получает все доступные варианты listening заданий"""
        with self.db_session as session:
            variants = session.execute(select(ReadingHSK1)).scalars().all()
            return variants

    def get_listening_variant(self, variant_id: int) -> ReadingHSK1:
        """Получает конкретный вариант по ID"""
        with self.db_session as session:
            variant = session.execute(
                select(ReadingHSK1).where(ReadingHSK1.id == variant_id)
            ).scalars().first()
            return variant

    def get_first_tasks_by_variant(self, variant_id: int) -> list[ReadingFirstTaskHSK1]:
        """Получает задания первого типа для варианта"""
        with self.db_session as session:
            tasks = session.execute(
                select(ReadingFirstTaskHSK1)
                .options(selectinload(ReadingFirstTaskHSK1.options))
                .where(ReadingFirstTaskHSK1.listening_var_id == variant_id)
            ).scalars().all()
            return tasks

    def get_second_tasks_by_variant(self, variant_id: int) -> list[ReadingSecondTaskHSK1]:
        """Получает задания второго типа для варианта"""
        with self.db_session as session:
            tasks = session.execute(
                select(ReadingSecondTaskHSK1)
                .options(selectinload(ReadingSecondTaskHSK1.sentences))
                .where(ReadingSecondTaskHSK1.listening_var_id == variant_id)
            ).scalars().all()
            return tasks
    
    def get_third_tasks_by_variant(self, variant_id: int) -> list[ReadingThirdTaskHSK1]:
        """Получает задания третьего типа для варианта"""
        with self.db_session as session:
            tasks = session.execute(
                select(ReadingThirdTaskHSK1)
                .options(selectinload(ReadingThirdTaskHSK1.questions),
                         selectinload(ReadingThirdTaskHSK1.options))
                .where(ReadingThirdTaskHSK1.listening_var_id == variant_id)
            ).scalars().all()
            return tasks
    
    def get_fourth_tasks_by_variant(self, variant_id: int) -> list[ReadingFourthTaskHSK1]:
        """Получает задания четвертого типа для варианта со всеми связанными данными"""
        with self.db_session as session:
            # Загружаем ReadingFourthTaskHSK1 вместе с вопросами и опциями
            tasks = session.execute(
                select(ReadingFourthTaskHSK1)
                .options(
                    selectinload(ReadingFourthTaskHSK1.questions),
                    selectinload(ReadingFourthTaskHSK1.options)  # Загружаем опции для каждого вопроса
                )
                .where(ReadingFourthTaskHSK1.listening_var_id == variant_id)
            ).scalars().all()
            return tasks
    

session = next(get_db_session())
repository = ReadingRepository(session)
