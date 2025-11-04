from dataclasses import dataclass
from sqlalchemy.orm import Session, selectinload
from hsk5.writing.models import *
from sqlalchemy import select
from database import get_db_session


@dataclass
class WritingRepository:
    db_session: Session

    def get_variants(self) -> list[WritingHSK5]:
        with self.db_session as session:
            variants = session.execute(select(WritingHSK5)).scalars().all()
            return variants

    def get_first_tasks_by_variant(self, variant_id: int) -> list[WritingFirstTaskHSK5]:
        with self.db_session as session:
            tasks = session.execute(
                select(WritingFirstTaskHSK5)
                .where(WritingFirstTaskHSK5.writing_var_id == variant_id)
            ).scalars().all()
            return tasks

    def get_second_tasks_by_variant(self, variant_id: int) -> list[WritingSecondTaskHSK5]:
        with self.db_session as session:
            tasks = session.execute(
                select(WritingSecondTaskHSK5)
                .where(WritingSecondTaskHSK5.writing_var_id == variant_id)
            ).scalars().all()
            return tasks
    
    def get_third_tasks_by_variant(self, variant_id: int) -> list[WritingThirdTaskHSK5]:
        with self.db_session as session:
            tasks = session.execute(
                select(WritingThirdTaskHSK5)
                .where(WritingThirdTaskHSK5.writing_var_id == variant_id)
            ).scalars().all()
            return tasks


session = next(get_db_session())
repository = WritingRepository(session)