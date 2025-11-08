from dataclasses import dataclass
from typing import Optional, List
from .repository import AsyncListeningRepository, get_listening_repository
from hsk1.listening.schemas import *
from .schemas import *
import asyncio


@dataclass
class AsyncListeningService:
    repo: AsyncListeningRepository

    async def get_listening_variants(self) -> List[ListeningSchema]:
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

    async def get_first_tasks_by_variant(self, variant_id: int) -> List[FirstTaskSchema]:
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
                    FirstTaskQuestionSchema.model_validate(question) for question in task.questions
                ]
            )

            orm_tasks.append(orm_task)

        return orm_tasks

    async def get_second_tasks_by_variant(self, variant_id: int) -> List[SecondTaskSchema]:
        """Получает задания второго типа для варианта"""
        tasks = await self.repo.get_second_tasks_by_variant(variant_id)
        if not tasks:
            return []

        orm_tasks = []
        for task in tasks:
            orm_task = SecondTaskSchema(
                id=task.id,
                picture_id=task.picture_id,
                questions=[
                    SecondTaskQuestionSchema(
                        id=question.id,
                        correct_letter=question.correct_letter
                    ) for question in task.questions
                ]
            )

            orm_tasks.append(orm_task)

        return orm_tasks

    async def get_third_tasks_by_variant(self, variant_id: int) -> List[ThirdTaskSchema]:
        """Получает задания третьего типа для варианта"""
        tasks = await self.repo.get_third_tasks_by_variant(variant_id)
        if not tasks:
            return []

        orm_tasks = []
        for task in tasks:
            orm_task = ThirdTaskSchema(
                id=task.id,
                picture_id=task.picture_id,
                questions=[
                    ThirdTaskQuestionSchema(id=question.id,
                                            correct_letter=question.correct_letter) for question in task.questions
                ]
            )

            orm_tasks.append(orm_task)

        return orm_tasks
    
    async def get_fourth_tasks_by_variant(self, variant_id: int) -> List[FourthTaskSchema]:
        """Получает задания четвертого типа для варианта"""
        tasks = await self.repo.get_fourth_tasks_by_variant(variant_id)
        if not tasks:
            return []

        orm_tasks = []
        for task in tasks:
            orm_task = FourthTaskSchema(
                id=task.id,
                questions=[
                    FourthTaskQuestionSchema(
                        id=question.id,
                        correct_letter=question.correct_letter,
                        options=[FourthTaskOptionSchema.model_validate(option) for option in question.options]
                    ) for question in task.questions
                ]
            )

            orm_tasks.append(orm_task)

        return orm_tasks

    async def close(self):
        """Закрывает соединение с репозиторием"""
        await self.repo.close()


# Фабрика для создания сервиса с зависимостями
async def get_listening_service() -> AsyncListeningService:
    """Создает сервис с асинхронным репозиторием"""
    repository = await get_listening_repository()
    return AsyncListeningService(repo=repository)
