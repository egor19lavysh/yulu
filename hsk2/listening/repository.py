from dataclasses import dataclass
from sqlalchemy.orm import Session, selectinload
from typing import List
from hsk2.listening.models import *
from sqlalchemy import select
from database import get_db_session


@dataclass
class ListeningRepository:
    db_session: Session

    def get_listening_variants(self):
        """Получает все доступные варианты listening заданий"""
        with self.db_session as session:
            variants = session.execute(select(ListeningHSK2)).scalars().all()
            return variants
    
    def get_listening_variant(self, variant_id: int) -> ListeningHSK2:
        """Получает конкретный вариант по ID"""
        with self.db_session as session:
            variant = session.execute(
                select(ListeningHSK2).where(ListeningHSK2.id == variant_id)
            ).scalars().first()
            return variant
    
    def get_first_tasks_by_variant(self, variant_id: int):
        """Получает задания первого типа для варианта"""
        with self.db_session as session:
            tasks = session.execute(
                select(FirstTaskHSK2)
                .options(selectinload(FirstTaskHSK2.questions))
                .where(FirstTaskHSK2.listening_var_id == variant_id)
            ).scalars().all()
            return tasks
    
    def get_second_tasks_by_variant(self, variant_id: int):
        """Получает задания второго типа для варианта"""
        with self.db_session as session:
            tasks = session.execute(
                select(SecondTaskHSK2)
                .options(selectinload(SecondTaskHSK2.questions))
                .where(SecondTaskHSK2.listening_var_id == variant_id)
            ).scalars().all()
            return tasks
    
    def get_third_tasks_by_variant(self, variant_id: int):
        """Получает задания третьего типа для варианта"""
        with self.db_session as session:
            tasks = session.execute(
                select(ThirdTaskHSK2)
                .options(
                    selectinload(ThirdTaskHSK2.questions).joinedload(ThirdTaskHSK2Question.options)
                )
                .where(ThirdTaskHSK2.listening_var_id == variant_id)
            ).scalars().all()
            return tasks


session = next(get_db_session())
repository = ListeningRepository(session)