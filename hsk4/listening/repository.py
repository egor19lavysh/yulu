from dataclasses import dataclass
from sqlalchemy.orm import Session, selectinload
from hsk4.listening.models import *
from sqlalchemy import select
from database import get_db_session


@dataclass
class ListeningRepository:
    db_session: Session

    def get_listening_variants(self):
        """Получает все доступные варианты listening заданий"""
        with self.db_session as session:
            variants = session.execute(select(ListeningHSK4)).scalars().all()
            return variants

    def get_listening_variant(self, variant_id: int):
        """Получает конкретный вариант по ID"""
        with self.db_session as session:
            variant = session.execute(
                select(ListeningHSK4).where(ListeningHSK4.id == variant_id)
            ).scalars().first()
            return variant

    def get_first_tasks_by_variant(self, variant_id: int):
        """Получает задания первого типа для варианта"""
        with self.db_session as session:
            tasks = session.execute(
                select(FirstTaskHSK4)
                .where(FirstTaskHSK4.listening_var_id == variant_id)
            ).scalars().all()
            return tasks

    def get_second_tasks_by_variant(self, variant_id: int):
        """Получает задания второго типа для варианта"""
        with self.db_session as session:
            tasks = session.execute(
                select(SecondTaskHSK4)
                .options(selectinload(SecondTaskHSK4.options))
                .where(SecondTaskHSK4.listening_var_id == variant_id)
            ).scalars().all()
            return tasks

    def get_third_tasks_by_variant(self, variant_id: int):
        """Получает задания третьего типа для варианта со всеми связанными данными"""
        with self.db_session as session:
            # Загружаем ThirdTask вместе с вопросами и опциями
            tasks = session.execute(
                select(ThirdTaskHSK4)
                .options(
                    selectinload(ThirdTaskHSK4.options)
                )
                .where(ThirdTaskHSK4.listening_var_id == variant_id)
            ).scalars().all()
            return tasks


session = next(get_db_session())
repository = ListeningRepository(session)
