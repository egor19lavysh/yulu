import random
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from dataclasses import dataclass
from .models import Reading, ReadingFirstTask, ReadingSecondTask, \
    ReadingThirdTask  # Предполагается, что модели находятся в models.py
from database import get_db_session


@dataclass
class ReadingRepository:
    db_session: Session

    def get_reading_variants(self) -> list[Reading]:
        with self.db_session as session:
            variants = session.execute(select(Reading).options(
                # Загружаем First Tasks и связанные данные
                selectinload(Reading.first_tasks)
                .selectinload(ReadingFirstTask.options),
                selectinload(Reading.first_tasks)
                .selectinload(ReadingFirstTask.questions),
                # Загружаем Second Tasks и связанные данные
                selectinload(Reading.second_tasks)
                .selectinload(ReadingSecondTask.options),
                selectinload(Reading.second_tasks)
                .selectinload(ReadingSecondTask.questions),
                # Загружаем Third Tasks и связанные данные
                selectinload(Reading.third_tasks)
                .selectinload(ReadingThirdTask.options)
            )).scalars().all()
            return list(variants)

    def get_reading_variant(self, variant_id: int) -> Reading | None:
        """Получает полный вариант Reading по ID."""
        with self.db_session as session:
            stmt = (
                select(Reading)
                .where(Reading.id == variant_id)
                .options(
                    # Загружаем First Tasks и связанные данные
                    selectinload(Reading.first_tasks)
                    .selectinload(ReadingFirstTask.options),
                    selectinload(Reading.first_tasks)
                    .selectinload(ReadingFirstTask.questions),
                    # Загружаем Second Tasks и связанные данные
                    selectinload(Reading.second_tasks)
                    .selectinload(ReadingSecondTask.options),
                    selectinload(Reading.second_tasks)
                    .selectinload(ReadingSecondTask.questions),
                    # Загружаем Third Tasks и связанные данные
                    selectinload(Reading.third_tasks)
                    .selectinload(ReadingThirdTask.options)
                )
            )
            return session.execute(stmt).scalar_one_or_none()

    def get_random_reading_variant_with_tasks(self) -> Reading | None:
        """
        Получает случайный вариант Reading с заданиями.
        Предполагает, что у вас есть записи в таблице reading_tasks.
        """
        with self.db_session as session:
            # Получаем все ID вариантов
            variant_ids_result = session.execute(select(Reading.id)).scalars().all()
            if not variant_ids_result:
                return None
            # Выбираем случайный ID
            random_variant_id = random.choice(variant_ids_result)

            # Загружаем вариант с заданиями
            stmt = (
                select(Reading)
                .where(Reading.id == random_variant_id)
                .options(
                    selectinload(Reading.first_tasks)
                    .selectinload(ReadingFirstTask.options),
                    selectinload(Reading.first_tasks)
                    .selectinload(ReadingFirstTask.questions),
                    selectinload(Reading.second_tasks)
                    .selectinload(ReadingSecondTask.options),
                    selectinload(Reading.second_tasks)
                    .selectinload(ReadingSecondTask.questions),
                    selectinload(Reading.third_tasks)
                    .selectinload(ReadingThirdTask.options)
                )
            )
            return session.execute(stmt).scalar_one_or_none()

    def get_first_tasks_by_variant(self, variant_id: int) -> list[ReadingFirstTask]:
        """Получает все задания типа 1 для указанного варианта"""
        with self.db_session as session:
            stmt = (
                select(ReadingFirstTask)
                .join(ReadingFirstTask.reading_var)
                .where(Reading.id == variant_id)
                .options(
                    selectinload(ReadingFirstTask.options),
                    selectinload(ReadingFirstTask.questions)
                ))
            return list(session.execute(stmt).scalars().all())

    def get_second_tasks_by_variant(self, variant_id: int) -> list[ReadingSecondTask]:
        """Получает все задания типа 2 для указанного варианта"""
        with self.db_session as session:
            stmt = (
                select(ReadingSecondTask)
                .join(ReadingSecondTask.reading_var)
                .where(Reading.id == variant_id)
                .options(
                    selectinload(ReadingSecondTask.options),
                    selectinload(ReadingSecondTask.questions)
                ))
            return list(session.execute(stmt).scalars().all())

    def get_third_tasks_by_variant(self, variant_id: int) -> list[ReadingThirdTask]:
        """Получает все задания типа 3 для указанного варианта"""
        with self.db_session as session:
            stmt = (
                select(ReadingThirdTask)
                .join(ReadingThirdTask.reading_var)
                .where(Reading.id == variant_id)
                .options(
                    selectinload(ReadingThirdTask.options)
                )
            )
            return list(session.execute(stmt).scalars().all())


session = next(get_db_session())
repository = ReadingRepository(session)
