from dataclasses import dataclass
from typing import Optional, List
from .repository import ReadingRepository, repository
from hsk2.reading.schemas import *
from .schemas import *


@dataclass
class ReadingService:
    repo: ReadingRepository

    def get_listening_variants(self) -> List[ReadingVariantSchema]:
        """Получает все доступные варианты listening заданий"""
        variants = self.repo.get_listening_variants()
        if not variants:
            return []

        return [ReadingVariantSchema.model_validate(variant, from_attributes=True) for variant in variants]
    
    def get_listening_variant(self, variant_id: int) -> Optional[ReadingVariantSchema]:
        """Получает конкретный вариант по ID"""
        variant = self.repo.get_listening_variant(variant_id)
        if not variant:
            return None

        return ReadingVariantSchema.model_validate(variant, from_attributes=True)

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
                sentences=[
                    FirstTaskSentenceSchema.model_validate(sentence) for sentence in task.sentences
                ]
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
                options=[
                    SecondTaskOptionSchema.model_validate(option) for option in task.options
                ],
                sentences=[
                    SecondTaskSentenceSchema.model_validate(sentence) for sentence in task.sentences
                ]
            )

            orm_tasks.append(orm_task)

        return orm_tasks
    
    def get_third_tasks_by_variant(self, variant_id: int) -> List[ThirdTaskSchema]:
        """Получает задания третьего типа для варианта"""
        tasks = self.repo.get_third_tasks_by_variant(variant_id)
        if not tasks:
            return []

        return [ThirdTaskSchema.model_validate(task, from_attributes=True) for task in tasks]
    
    def get_fourth_tasks_by_variant(self, variant_id: int) -> List[FourthTaskSchema]:
        """Получает задания третьего типа для варианта"""
        tasks = self.repo.get_fourth_tasks_by_variant(variant_id)
        if not tasks:
            return []

        orm_tasks = []
        for task in tasks:
            orm_task = FourthTaskSchema(
                id=task.id,
                questions=[
                    FourthTaskQuestionSchema.model_validate(question) for question in task.questions
                ],
                options=[
                    FourthTaskOptionSchema.model_validate(option) for option in task.options
                ]
            )

            orm_tasks.append(orm_task)

        return orm_tasks


service = ReadingService(repository=repository)