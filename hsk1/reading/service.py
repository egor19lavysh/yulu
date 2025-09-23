from dataclasses import dataclass
from hsk1.reading.repository import ReadingRepository, repository
from hsk1.reading.schemas import *
from hsk1.reading.models import *


@dataclass
class ReadingService:
    repository: ReadingRepository

    def get_reading_variants(self) -> list[ReadingVariantSchema]:
        variants = [self._to_variant(var) for var in self.repository.get_reading_variants()]
        return variants

    def get_first_tasks_by_variant(self, var_id: int) -> list[FirstTaskSchema]:
        tasks = self.repository.get_first_tasks_by_variant(variant_id=var_id)
        orm_tasks = []
        for task in tasks:
            orm_task = FirstTaskSchema(
                id=task.id,
                options=[FirstTaskOptionSchema.model_validate(option) for option in task.options],
                sentences=[FirstTaskSentenceSchema.model_validate(sentence) for sentence in task.sentences]
            )
            orm_tasks.append(orm_task)

        return orm_tasks

    def get_second_tasks_by_variant(self, var_id: int) -> list[SecondTaskSchema]:
        tasks = self.repository.get_second_tasks_by_variant(variant_id=var_id)
        orm_tasks = []
        for task in tasks:
            orm_task = SecondTaskSchema(
                id=task.id,
                correct_sequence=task.correct_sequence,
                options=[SecondTaskOptionSchema.model_validate(option) for option in task.options]
            )

            orm_tasks.append(orm_task)

        return orm_tasks

    def get_third_tasks_by_variant(self, var_id: int) -> list[ThirdTaskSchema]:
        tasks = self.repository.get_third_tasks_by_variant(variant_id=var_id)
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

    def _to_variant(self, var: ReadingHSK1) -> ReadingVariantSchema:
        return ReadingVariantSchema.model_validate(var)


service = ReadingService(repository=repository)
