from dataclasses import dataclass
from hsk4.reading.repository import ReadingRepository, get_reading_repository
from hsk4.reading.schemas import *
from hsk4.reading.models import *


@dataclass
class ReadingService:
    repository: ReadingRepository

    async def get_reading_variants(self) -> list[ReadingVariantSchema]:
        variants = [await self._to_variant(var) for var in await self.repository.get_reading_variants()]
        return variants

    async def get_first_tasks_by_variant(self, var_id: int) -> list[FirstTaskSchema]:
        tasks = await self.repository.get_first_tasks_by_variant(variant_id=var_id)
        orm_tasks = []
        for task in tasks:
            orm_task = FirstTaskSchema(
                id=task.id,
                options=[FirstTaskOptionSchema.model_validate(option) for option in task.options],
                sentences=[FirstTaskSentenceSchema.model_validate(sentence) for sentence in task.sentences]
            )
            orm_tasks.append(orm_task)

        return orm_tasks

    async def get_second_tasks_by_variant(self, var_id: int) -> list[SecondTaskSchema]:
        tasks = await self.repository.get_second_tasks_by_variant(variant_id=var_id)
        orm_tasks = []
        for task in tasks:
            orm_task = SecondTaskSchema(
                id=task.id,
                correct_sequence=task.correct_sequence,
                options=[SecondTaskOptionSchema.model_validate(option) for option in task.options]
            )

            orm_tasks.append(orm_task)

        return orm_tasks

    async def get_third_tasks_by_variant(self, var_id: int) -> list[ThirdTaskSchema]:
        tasks = await self.repository.get_third_tasks_by_variant(variant_id=var_id)
        orm_tasks = []
        for task in tasks:
            orm_task = ThirdTaskSchema(
                id=task.id,
                text=task.text,
                questions=[ThirdTaskQuestionSchema(
                    id=question.id,
                    text=question.text,
                    correct_letter=question.correct_letter,
                    options=[QuestionOptionSchema.model_validate(option) for option in question.options]
                ) for question in task.questions]
            )
            orm_tasks.append(orm_task)

        return orm_tasks

    async def _to_variant(self, var: ReadingHSK4) -> ReadingVariantSchema:
        return ReadingVariantSchema.model_validate(var)


async def get_reading_service():
    repository = await get_reading_repository()
    return ReadingService(repository=repository)