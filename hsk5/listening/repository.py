from dataclasses import dataclass
from sqlalchemy.orm import Session, selectinload
from hsk5.listening.models import *
from sqlalchemy import select
from database import get_db_session


@dataclass
class ListeningRepository:
    db_session: Session

    def get_listening_variants(self):
        """Получает все доступные варианты listening заданий"""
        with self.db_session as session:
            variants = session.execute(select(ListeningHSK5)).scalars().all()
            return variants

    def get_listening_variant(self, variant_id: int):
        """Получает конкретный вариант по ID"""
        with self.db_session as session:
            variant = session.execute(
                select(ListeningHSK5).where(ListeningHSK5.id == variant_id)
            ).scalars().first()
            return variant

    def get_first_tasks_by_variant(self, variant_id: int):
        """Получает задания первого типа для варианта"""
        with self.db_session as session:
            tasks = session.execute(
                select(FirstTaskHSK5)
                .options(selectinload(FirstTaskHSK5.options))
                .where(FirstTaskHSK5.listening_var_id == variant_id)
            ).scalars().all()
            return tasks


session = next(get_db_session())
repository = ListeningRepository(session)
