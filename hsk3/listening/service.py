from dataclasses import dataclass
from typing import Optional
from .repository import *
from hsk3.listening.schemas import *


@dataclass
class ListeningService:
    repo: ListeningRepository

    # Новые методы для единой механики
    async def get_listening_variants(self) -> list[ListeningSchema]:
        """Получает все доступные варианты listening заданий"""
        variants = await self.repo.get_listening_variants()
        if not variants:
            return []

        return [ListeningSchema.model_validate(variant, from_attributes=True) for variant in variants]

    async def get_listening_variant(self, variant_id: int) -> Optional[ListeningSchema]:
        """Получает конкретный вариант по ID"""
        variant = await self.repo.get_listening_variant(variant_id)
        if not variant:
            return None

        return ListeningSchema.model_validate(variant, from_attributes=True)

    async def get_first_tasks_by_variant(self, variant_id: int) -> list[FirstTaskSchema]:
        """Получает задания первого типа для варианта"""
        tasks = await self.repo.get_first_tasks_by_variant(variant_id)
        if not tasks:
            return []

        orm_tasks = []
        for task in tasks:
            orm_task = FirstTaskSchema(
                id=task.id,
                picture_id=task.picture_id,
                questions=[
                    FirstTaskQuestionSchema.model_validate(q, from_attributes=True)
                    for q in task.questions
                ]
            )
            orm_tasks.append(orm_task)
        return orm_tasks

    async def get_first_task_by_variant(self, variant_id: int) -> Optional[FirstTaskSchema]:
        """Получает первое задание первого типа для варианта"""
        task = await self.repo.get_first_task_by_variant(variant_id)
        if not task:
            return None

        return FirstTaskSchema(
            id=task.id,
            picture_id=task.picture_id,
            questions=[
                FirstTaskQuestionSchema.model_validate(q, from_attributes=True)
                for q in task.questions
            ]
        )

    async def get_second_tasks_by_variant(self, variant_id: int) -> list[SecondTaskSchema]:
        """Получает задания второго типа для варианта"""
        tasks = await self.repo.get_second_tasks_by_variant(variant_id)
        if not tasks:
            return []

        return [SecondTaskSchema.model_validate(task, from_attributes=True) for task in tasks]

    async def get_third_tasks_by_variant(self, variant_id: int) -> list[ThirdTaskSchema]:
        """Получает задания третьего типа для варианта со всеми связанными данными"""
        tasks = await self.repo.get_third_tasks_by_variant(variant_id)
        if not tasks:
            return []

        orm_tasks = []
        for task in tasks:  # task - экземпляр ThirdTask
            # Создаем список вопросов с опциями
            questions = []
            for question in task.questions:  # question - экземпляр ThirdTaskQuestion
                options = [
                    ThirdTaskOptionSchema.model_validate(option, from_attributes=True)
                    for option in question.options  # option - экземпляр ThirdTaskOption
                ]
                question_schema = ThirdTaskQuestionSchema(
                    id=question.id,
                    correct_letter=question.correct_letter,
                    options=options
                )
                questions.append(question_schema)

            orm_task = ThirdTaskSchema(
                id=task.id,
                questions=questions
            )
            orm_tasks.append(orm_task)

        return orm_tasks

async def get_listening_service():
    repository = await get_listening_repository()
    return ListeningService(repo=repository)