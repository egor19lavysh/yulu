from dataclasses import dataclass
from sqlalchemy.orm import Session, selectinload
from hsk1.reading.models import *
from sqlalchemy import select
from database import get_db_session


@dataclass
class ReadingRepository:
    db_session: Session

    def get_reading_variants(self) -> list[ReadingHSK1]:
        with self.db_session as session:
            variants = session.execute(select(ReadingHSK1)).scalars().all()
            return variants

    def get_first_tasks_by_variant(self, variant_id: int) -> list[ReadingFirstTaskHSK1]:
        with self.db_session as session:
            tasks = session.execute(
                select(ReadingFirstTaskHSK1)
                .options(selectinload(ReadingFirstTaskHSK1.options),
                         selectinload(ReadingFirstTaskHSK1.sentences))
                .where(ReadingFirstTaskHSK1.reading_var_id == variant_id)
            ).scalars().all()
            return tasks

    def get_second_tasks_by_variant(self, variant_id: int) -> list[ReadingSecondTaskHSK1]:
        with self.db_session as session:
            tasks = session.execute(
                select(ReadingSecondTaskHSK1)
                .options(selectinload(ReadingSecondTaskHSK1.options))
                .where(ReadingSecondTaskHSK1.reading_var_id == variant_id)
            ).scalars().all()
            return tasks

    def get_third_tasks_by_variant(self, variant_id: int) -> list[ReadingThirdTaskHSK1]:
        with self.db_session as session:
            # Загружаем ThirdTask вместе с вопросами (и опциями внутри вопросов)
            tasks = session.execute(
                select(ReadingThirdTaskHSK1)
                .options(
                    selectinload(ReadingThirdTaskHSK1.questions).joinedload(ReadingThirdTaskQuestionHSK1.options)
                )
                .where(ReadingThirdTaskHSK1.reading_var_id == variant_id)
            ).scalars().all()
            return tasks


session = next(get_db_session())
repository = ReadingRepository(session)
