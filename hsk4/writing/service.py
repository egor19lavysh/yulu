from dataclasses import dataclass
from hsk4.writing.repository import WritingRepository, repository
from hsk4.writing.schemas import *
from hsk4.writing.models import *


@dataclass
class WritingService:
    repository: WritingRepository

    def get_writing_variants(self) -> list[WritingVarSchema]:
        variants = [WritingVarSchema.model_validate(var) for var in self.repository.get_variants()]
        return variants

    def get_first_tasks_by_variant(self, var_id: int) -> list[FirstTaskSchema]:
        tasks = self.repository.get_first_tasks_by_variant(variant_id=var_id)
        orm_tasks = []

        for task in tasks:
            orm_task = FirstTaskSchema(
                id=task.id,
                correct_sentence=task.correct_sentence,
                words=task.words
            )
            orm_tasks.append(orm_task)

        return orm_tasks

    def get_second_task_by_variant(self, var_id: int) -> SecondTaskSchema:
        task = self.repository.get_second_task_by_variant(variant_id=var_id)

        orm_task = SecondTaskSchema(
            id=task.id,
            picture_id=task.picture_id,
            words=[TaskWordSchema.model_validate(word) for word in task.words]
        )

        return orm_task


service = WritingService(repository=repository)
