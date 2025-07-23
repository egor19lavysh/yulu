from dataclasses import dataclass
from sqlalchemy.orm import Session, selectinload
from hsk3.reading_models import *
from hsk3.writing_models import *
from hsk3.listening_models import *
from sqlalchemy import select
from database import get_db_session
import random


@dataclass
class ReadingRepository:
    db_session: Session

    def get_type_one_tasks(self) -> list[ReadingTaskTypeOne]:
        with self.db_session as session:
            tasks = list(session.execute(select(ReadingTaskTypeOne)).scalars().all())
            return tasks

    def get_type_one_task(self, task_id: int) -> ReadingTaskTypeOne | None:
        with self.db_session as session:
            task = session.execute(
                select(ReadingTaskTypeOne).where(ReadingTaskTypeOne.id == task_id).options(
                    selectinload(ReadingTaskTypeOne.options),
                    selectinload(ReadingTaskTypeOne.questions))).scalar_one_or_none()
            return task

    def get_type_two_tasks(self) -> list[ReadingTaskTypeTwo]:
        with self.db_session as session:
            tasks = list(session.execute(select(ReadingTaskTypeTwo)).scalars().all())
            return tasks

    def get_type_two_task(self, task_id: int) -> ReadingTaskTypeTwo | None:
        with self.db_session as session:
            task = session.execute(
                select(ReadingTaskTypeTwo).where(ReadingTaskTypeTwo.id == task_id).options(
                    selectinload(ReadingTaskTypeTwo.options),
                    selectinload(ReadingTaskTypeTwo.questions))).scalar_one_or_none()
            return task

    def get_random_type_three_tasks(self) -> list[ReadingTaskTypeThree]:
        with self.db_session as session:
            tasks = random.sample(list(session.execute(
                select(ReadingTaskTypeThree).options(selectinload(ReadingTaskTypeThree.options))).scalars().all()), 5)
            return tasks


@dataclass
class WritingRepository:
    db_session: Session

    def get_type_one_tasks(self) -> list[WritingTaskTypeOne]:
        with self.db_session as session:
            tasks = random.sample(session.execute(select(WritingTaskTypeOne)).scalars().all(), 5)
            return tasks

    def get_type_two_tasks(self) -> list[WritingTaskTypeTwo]:
        with self.db_session as session:
            tasks = random.sample(session.execute(select(WritingTaskTypeTwo)).scalars().all(), 5)
            return tasks


@dataclass
class ListeningRepository:
    db_session: Session

    def get_test_first_task(self):
        with self.db_session as session:
            task = session.execute(select(FirstTask).options(selectinload(FirstTask.questions))).scalars().first()
            return task

    def get_test_second_tasks(self):
        with self.db_session as session:
            tasks = session.execute(select(SecondTask).limit(5)).scalars().all()
            return tasks

    def get_test_third_tasks(self):
        with self.db_session as session:
            tasks = session.execute(select(ThirdTask).options(selectinload(ThirdTask.options)).limit(5)).scalars().all()
            return tasks


session = next(get_db_session())

reading_repo = ReadingRepository(session)
writing_repo = WritingRepository(session)
listening_repo = ListeningRepository(session)
