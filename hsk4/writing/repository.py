from dataclasses import dataclass
from sqlalchemy.orm import Session, selectinload
from hsk4.writing.models import *
from sqlalchemy import select
from database import get_db_session


@dataclass
class WritingRepository:
    db_session: Session

    def get_variants(self) -> list[WritingHSK4]:
        with self.db_session as session:
            variants = session.execute(select(WritingHSK4)).scalars().all()
            return variants

    def get_first_tasks_by_variant(self, variant_id: int) -> list[WritingFirstTaskHSK4]:
        with self.db_session as session:
            tasks = session.execute(
                select(WritingFirstTaskHSK4)
                .where(WritingFirstTaskHSK4.writing_var_id == variant_id)
            ).scalars().all()
            return tasks

    def get_second_tasks_by_variant(self, variant_id: int) -> list[WritingSecondTaskHSK4]:
        with self.db_session as session:
            tasks = session.execute(
                select(WritingSecondTaskHSK4)
                .options(selectinload(WritingSecondTaskHSK4.words))
                .where(WritingSecondTaskHSK4.writing_var_id == variant_id)
            ).scalars().all()

            return tasks


session = next(get_db_session())
repository = WritingRepository(session)
