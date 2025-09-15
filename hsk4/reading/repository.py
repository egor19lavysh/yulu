from dataclasses import dataclass
from sqlalchemy.orm import Session, selectinload
from hsk4.reading.models import *
from sqlalchemy import select
from database import get_db_session


@dataclass
class ReadingRepository:
    db_session: Session

    def get_reading_variants(self) -> list[ReadingHSK4]:
        with self.db_session as session:
            variants = session.execute(select(ReadingHSK4)).scalars().all()
            return variants

    def get_first_tasks_by_variant(self, variant_id: int) -> list[ReadingFirstTaskHSK4]:
        with self.db_session as session:
            tasks = session.execute(
                select(ReadingFirstTaskHSK4)
                .options(selectinload(ReadingFirstTaskHSK4.options),
                         selectinload(ReadingFirstTaskHSK4.sentences))
                .where(ReadingFirstTaskHSK4.reading_var_id == variant_id)
            ).scalars().all()
            return tasks

    def get_second_tasks_by_variant(self, variant_id: int) -> list[ReadingSecondTaskHSK4]:
        with self.db_session as session:
            tasks = session.execute(
                select(ReadingSecondTaskHSK4)
                .options(selectinload(ReadingSecondTaskHSK4.options))
                .where(ReadingSecondTaskHSK4.reading_var_id == variant_id)
            ).scalars().all()
            return tasks

    def get_third_tasks_by_variant(self, variant_id: int) -> list[ReadingThirdTaskHSK4]:
        with self.db_session as session:
            # Загружаем ThirdTask вместе с вопросами (и опциями внутри вопросов)
            tasks = session.execute(
                select(ReadingThirdTaskHSK4)
                .options(
                    selectinload(ReadingThirdTaskHSK4.questions).joinedload(ReadingThirdTaskQuestionHSK4.options)
                )
                .where(ReadingThirdTaskHSK4.reading_var_id == variant_id)
            ).scalars().all()
            return tasks


session = next(get_db_session())
repository = ReadingRepository(session)
