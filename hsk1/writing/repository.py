from dataclasses import dataclass
from sqlalchemy.orm import Session, selectinload
from hsk1.writing.models import *
from sqlalchemy import select
from database import get_db_session


@dataclass
class WritingRepository:
    db_session: Session

    def get_variants(self) -> list[WritingHSK1]:
        with self.db_session as session:
            variants = session.execute(select(WritingHSK1)).scalars().all()
            return variants

    def get_first_tasks_by_variant(self, variant_id: int) -> list[WritingFirstTaskHSK1]:
        with self.db_session as session:
            tasks = session.execute(
                select(WritingFirstTaskHSK1)
                .where(WritingFirstTaskHSK1.writing_var_id == variant_id)
            ).scalars().all()
            return tasks

    def get_second_task_by_variant(self, variant_id: int) -> WritingSecondTaskHSK1 | None:
        with self.db_session as session:
            task = session.execute(
                select(WritingSecondTaskHSK1)
                .options(selectinload(WritingSecondTaskHSK1.words))
                .where(WritingSecondTaskHSK1.writing_var_id == variant_id)
            ).scalar_one_or_none()

            return task


session = next(get_db_session())
repository = WritingRepository(session)
