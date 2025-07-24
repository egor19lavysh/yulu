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

    def get_listening_variants(self):
        """Получает все доступные варианты listening заданий"""
        with self.db_session as session:
            variants = session.execute(select(Listening)).scalars().all()
            return variants

    def get_listening_variant(self, variant_id: int):
        """Получает конкретный вариант по ID"""
        with self.db_session as session:
            variant = session.execute(
                select(Listening).where(Listening.id == variant_id)
            ).scalars().first()
            return variant

    def get_first_tasks_by_variant(self, variant_id: int):
        """Получает задания первого типа для варианта"""
        with self.db_session as session:
            tasks = session.execute(
                select(FirstTask)
                .options(selectinload(FirstTask.questions))  # Загружаем связанные вопросы
                .where(FirstTask.listening_var_id == variant_id)
            ).scalars().all()
            return tasks

    def get_second_tasks_by_variant(self, variant_id: int):
        """Получает задания второго типа для варианта"""
        with self.db_session as session:
            tasks = session.execute(
                select(SecondTask)
                .where(SecondTask.listening_var_id == variant_id)
            ).scalars().all()
            return tasks

    def get_third_tasks_by_variant(self, variant_id: int):
        """Получает задания третьего типа для варианта со всеми связанными данными"""
        with self.db_session as session:
            # Загружаем ThirdTask вместе с вопросами и опциями
            tasks = session.execute(
                select(ThirdTask)
                .options(
                    selectinload(ThirdTask.questions)
                        .selectinload(ThirdTaskQuestion.options)  # Загружаем опции для каждого вопроса
                )
                .where(ThirdTask.listening_var_id == variant_id)
            ).scalars().all()
            return tasks

    # Метод для тестирования (если используется)
    def get_first_task_by_variant(self, variant_id: int):
        """Получает первое задание первого типа для варианта (для тестирования)"""
        with self.db_session as session:
            task = session.execute(
                select(FirstTask)
                .options(selectinload(FirstTask.questions))
                .where(FirstTask.listening_var_id == variant_id)
            ).scalars().first()
            return task



session = next(get_db_session())

reading_repo = ReadingRepository(session)
writing_repo = WritingRepository(session)
listening_repo = ListeningRepository(session)
