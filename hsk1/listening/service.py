from dataclasses import dataclass
from typing import Optional, List
from database import get_db_session
from .repository import ListeningRepository
from hsk1.listening.schemas import *
from .schemas import *


@dataclass
class ListeningService:
    repo: ListeningRepository

    def get_listening_variants(self) -> List[ListeningSchema]:
        """Получает все доступные варианты listening заданий"""
        variants = self.repo.get_listening_variants()
        if not variants:
            return []

        return [ListeningSchema.model_validate(variant, from_attributes=True) for variant in variants]

    def get_listening_variant(self, variant_id: int) -> Optional[ListeningSchema]:
        """Получает конкретный вариант по ID"""
        variant = self.repo.get_listening_variant(variant_id)
        if not variant:
            return None

        return ListeningSchema.model_validate(variant, from_attributes=True)

    def get_first_tasks_by_variant(self, variant_id: int) -> List[FirstTaskSchema]:
        """Получает задания первого типа для варианта"""
        tasks = self.repo.get_first_tasks_by_variant(variant_id)
        if not tasks:
            return []

        orm_tasks = []
        for task in tasks:
            orm_task = FirstTaskSchema(
                id=task.id,
                text=task.text,
                is_correct=task.is_correct
            )

            orm_tasks.append(orm_task)

        return orm_tasks

    def get_second_tasks_by_variant(self, variant_id: int) -> List[SecondTaskSchema]:
        """Получает задания второго типа для варианта"""
        tasks = self.repo.get_second_tasks_by_variant(variant_id)
        if not tasks:
            return []

        orm_tasks = []
        for task in tasks:
            orm_task = SecondTaskSchema(
                id=task.id,
                correct_letter=task.correct_letter,
                options=[
                    SecondTaskOptionSchema.model_validate(option) for option in task.options
                ]
            )

            orm_tasks.append(orm_task)

        return orm_tasks

    def get_third_tasks_by_variant(self, variant_id: int) -> List[ThirdTaskSchema]:
        """Получает задания третьего типа для варианта со всеми связанными данными"""
        tasks = self.repo.get_third_tasks_by_variant(variant_id)
        if not tasks:
            return []

        orm_tasks = []
        for task in tasks:
            orm_task = ThirdTaskSchema(
                id=task.id,
                correct_letter=task.correct_letter,
                options=[
                    ThirdTaskOptionSchema.model_validate(option) for option in task.options
                ]
            )

            orm_tasks.append(orm_task)

        return orm_tasks



session = next(get_db_session())
repository = ListeningRepository(session)
service = ListeningService(repository)