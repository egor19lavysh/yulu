from dataclasses import dataclass
from sqlalchemy.orm import Session, selectinload
from hsk1.listening.models import *
from sqlalchemy import select
from database import get_db_session


@dataclass
class ListeningRepository:
    db_session: Session

    def get_listening_variants(self):
        """Получает все доступные варианты listening заданий"""
        with self.db_session as session:
            variants = session.execute(select(ListeningHSK1)).scalars().all()
            return variants

    def get_listening_variant(self, variant_id: int):
        """Получает конкретный вариант по ID"""
        with self.db_session as session:
            variant = session.execute(
                select(ListeningHSK1).where(ListeningHSK1.id == variant_id)
            ).scalars().first()
            return variant

    def get_first_tasks_by_variant(self, variant_id: int):
        """Получает задания первого типа для варианта"""
        with self.db_session as session:
            tasks = session.execute(
                select(FirstTaskHSK1)
                .where(FirstTaskHSK1.listening_var_id == variant_id)
            ).scalars().all()
            return tasks

    def get_second_tasks_by_variant(self, variant_id: int):
        """Получает задания второго типа для варианта"""
        with self.db_session as session:
            tasks = session.execute(
                select(SecondTaskHSK1)
                .options(selectinload(SecondTaskHSK1.options))
                .where(SecondTaskHSK1.listening_var_id == variant_id)
            ).scalars().all()
            return tasks

    def get_third_tasks_by_variant(self, variant_id: int):
        """Получает задания третьего типа для варианта со всеми связанными данными"""
        with self.db_session as session:
            # Загружаем ThirdTask вместе с вопросами и опциями
            tasks = session.execute(
                select(ThirdTaskHSK1)
                .options(
                    selectinload(ThirdTaskHSK1.options)
                )
                .where(ThirdTaskHSK1.listening_var_id == variant_id)
            ).scalars().all()
            return tasks


session = next(get_db_session())
repository = ListeningRepository(session)
