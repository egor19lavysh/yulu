from dataclasses import dataclass
from typing import Optional, List
from .repository import ListeningRepository, repository
from hsk5.listening.schemas import *
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
                correct_letter=task.correct_letter,
                options=[FirstTaskOptionSchema.model_validate(option) for option in task.options]
            )

            orm_tasks.append(orm_task)

        return orm_tasks


service = ListeningService(repo=repository)