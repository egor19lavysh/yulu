from dataclasses import dataclass
from hsk5.writing.repository import WritingRepository, get_writing_repository
from hsk5.writing.schemas import *
from hsk5.writing.models import *


@dataclass
class WritingService:
    repository: WritingRepository

    async def get_writing_variants(self) -> list[WritingSchema]:
        variants = [WritingSchema.model_validate(var) for var in await self.repository.get_variants()]
        return variants

    async def get_first_tasks_by_variant(self, var_id: int) -> list[FirstTaskSchema]:
        tasks = await self.repository.get_first_tasks_by_variant(variant_id=var_id)
        orm_tasks = []

        for task in tasks:
            orm_task = FirstTaskSchema(
                id=task.id,
                correct_sentence=task.correct_sentence,
                words=task.words
            )
            orm_tasks.append(orm_task)

        return orm_tasks

    async def get_second_tasks_by_variant(self, var_id: int) -> list[SecondTaskSchema]:
        tasks = await self.repository.get_second_tasks_by_variant(variant_id=var_id)
        orm_tasks = []

        for task in tasks:
            orm_task = SecondTaskSchema(
                id=task.id,
                text=task.text
            )
            orm_tasks.append(orm_task)

        return orm_tasks
    
    async def get_third_tasks_by_variant(self, var_id: int) -> list[ThirdTaskSchema]:
        tasks = await self.repository.get_third_tasks_by_variant(variant_id=var_id)
        orm_tasks = []

        for task in tasks:
            orm_task = ThirdTaskSchema(
                id=task.id,
                picture_id=task.picture_id
            )
            orm_tasks.append(orm_task)

        return orm_tasks


async def get_writing_service():
    repo = await get_writing_repository()
    return WritingService(repository=repo)