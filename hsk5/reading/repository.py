from dataclasses import dataclass
from sqlalchemy.orm import Session, selectinload
from hsk5.reading.models import *
from sqlalchemy import select
from database import get_db_session


@dataclass
class ReadingRepository:
    db_session: Session

    def get_reading_variants(self) -> list[ReadingHSK5]:
        with self.db_session as session:
            variants = session.execute(select(ReadingHSK5)).scalars().all()
            return variants

    def get_first_tasks_by_variant(self, variant_id: int) -> list[ReadingFirstTaskHSK5]:
        with self.db_session as session:
            tasks = session.execute(
                select(ReadingFirstTaskHSK5)
                .options(selectinload(ReadingFirstTaskHSK5.questions).joinedload(ReadingFirstTaskHSK5Question.options))
                .where(ReadingFirstTaskHSK5.reading_var_id == variant_id)
            ).scalars().all()
            return tasks

    def get_second_tasks_by_variant(self, variant_id: int) -> list[ReadingSecondTaskHSK5]:
        with self.db_session as session:
            tasks = session.execute(
                select(ReadingSecondTaskHSK5)
                .options(selectinload(ReadingSecondTaskHSK5.options))
                .where(ReadingSecondTaskHSK5.reading_var_id == variant_id)
            ).scalars().all()
            return tasks

    def get_third_tasks_by_variant(self, variant_id: int) -> list[ReadingThirdTaskHSK5]:
        with self.db_session as session:
            # Загружаем ThirdTask вместе с вопросами (и опциями внутри вопросов)
            tasks = session.execute(
                select(ReadingThirdTaskHSK5)
                .options(
                    selectinload(ReadingThirdTaskHSK5.questions).joinedload(ReadingThirdTaskHSK5Question.options)
                )
                .where(ReadingThirdTaskHSK5.reading_var_id == variant_id)
            ).scalars().all()
            return tasks


session = next(get_db_session())
repository = ReadingRepository(session)
