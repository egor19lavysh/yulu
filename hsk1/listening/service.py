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
                picture_id=task.picture_id,
                questions=[
                    FirstTaskQuestionSchema.model_validate(question) for question in task.questions
                ]
            )

            orm_tasks.append(orm_task)

        return orm_tasks

    def get_second_tasks_by_variant(self, variant_id: int) -> List[SecondTaskSchema]:
        """Получает задания второго типа для варианта"""
        tasks = self.repo.get_first_tasks_by_variant(variant_id)
        if not tasks:
            return []

        orm_tasks = []
        for task in tasks:
            orm_task = SecondTaskSchema(
                id=task.id,
                picture_id=task.picture_id,
                questions=[
                    SecondTaskQuestionSchema.model_validate(question) for question in task.questions
                ]
            )

            orm_tasks.append(orm_task)

        return orm_tasks

    def get_third_tasks_by_variant(self, variant_id: int) -> List[ThirdTaskSchema]:
        """Получает задания третьего типа для варианта"""
        tasks = self.repo.get_third_tasks_by_variant(variant_id)
        if not tasks:
            return []

        orm_tasks = []
        for task in tasks:
            orm_task = ThirdTaskSchema(
                id=task.id,
                picture_id=task.picture_id,
                questions=[
                    ThirdTaskQuestionSchema.model_validate(question) for question in task.questions
                ]
            )

            orm_tasks.append(orm_task)

        return orm_tasks
    
    def get_fourth_tasks_by_variant(self, variant_id: int) -> List[FourthTaskSchema]:
        """Получает задания третьего типа для варианта"""
        tasks = self.repo.get_fourth_tasks_by_variant(variant_id)
        if not tasks:
            return []

        orm_tasks = []
        for task in tasks:
            orm_task = FourthTaskSchema(
                id=task.id,
                picture_id=task.picture_id,
                questions=[
                    FourthTaskQuestionSchema.model_validate(question) for question in task.questions
                ]
            )

            orm_tasks.append(orm_task)

        return orm_tasks
    


repository = ListeningRepository()
service = ListeningService(repository)