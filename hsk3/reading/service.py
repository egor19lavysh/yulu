from dataclasses import dataclass
from .repository import ReadingRepository, get_reading_repository
from .schemas import *
from .models import *


@dataclass
class ReadingService:
    repo: ReadingRepository

    async def get_reading_variants(self) -> list[ReadingVariantSchema]:
        db_variants = await self.repo.get_reading_variants()
        variants = [await self._db_variant_to_schema(var) for var in db_variants]
        return variants

    async def get_reading_variant(self, variant_id: int) -> ReadingVariantSchema | None:
        """Получает и сериализует полный вариант Reading."""
        db_variant = await self.repo.get_reading_variant(variant_id)
        if not db_variant:
            return None
        return self._db_variant_to_schema(db_variant)

    async def get_random_reading_variant(self) -> ReadingVariantSchema | None:
        """Получает и сериализует случайный вариант Reading."""
        db_variant = await self.repo.get_random_reading_variant_with_tasks()
        if not db_variant:
            return None
        return self._db_variant_to_schema(db_variant)

    async def _db_variant_to_schema(self, db_variant: Reading) -> ReadingVariantSchema:
        """Преобразует объект SQLAlchemy в Pydantic схему."""
        first_tasks_schemas = [
            FirstTaskSchema(
                id=task.id,
                options=[FirstTaskOptionSchema.model_validate(opt, from_attributes=True) for opt in task.options],
                questions=[FirstTaskQuestionSchema.model_validate(q, from_attributes=True) for q in task.questions]
            )
            for task in db_variant.first_tasks
        ]

        second_tasks_schemas = [
            SecondTaskSchema(
                id=task.id,
                options=[SecondTaskOptionSchema.model_validate(opt, from_attributes=True) for opt in task.options],
                questions=[SecondTaskQuestionSchema.model_validate(q, from_attributes=True) for q in task.questions]
            )
            for task in db_variant.second_tasks
        ]

        third_tasks_schemas = [
            ThirdTaskSchema(
                id=task.id,
                text=task.text,
                correct_letter=task.correct_letter,  # Предполагается, что это буква
                options=[ThirdTaskOptionSchema.model_validate(opt, from_attributes=True) for opt in task.options]
            )
            for task in db_variant.third_tasks
        ]

        return ReadingVariantSchema(
            id=db_variant.id,
            first_tasks=first_tasks_schemas,
            second_tasks=second_tasks_schemas,
            third_tasks=third_tasks_schemas
        )

    async def get_first_tasks_by_variant(self, variant_id: int) -> list[FirstTaskSchema]:
        """Получает и сериализует задания типа 1 для варианта"""
        db_tasks = await self.repo.get_first_tasks_by_variant(variant_id)
        return [
            FirstTaskSchema(
                id=task.id,
                options=[FirstTaskOptionSchema.model_validate(opt, from_attributes=True) for opt in task.options],
                questions=[FirstTaskQuestionSchema.model_validate(q, from_attributes=True) for q in task.questions]
            )
            for task in db_tasks
        ]

    async def get_second_tasks_by_variant(self, variant_id: int) -> list[SecondTaskSchema]:
        """Получает и сериализует задания типа 2 для варианта"""
        db_tasks = await self.repo.get_second_tasks_by_variant(variant_id)
        return [
            SecondTaskSchema(
                id=task.id,
                options=[SecondTaskOptionSchema.model_validate(opt, from_attributes=True) for opt in task.options],
                questions=[SecondTaskQuestionSchema.model_validate(q, from_attributes=True) for q in task.questions]
            )
            for task in db_tasks
        ]

    async def get_third_tasks_by_variant(self, variant_id: int) -> list[ThirdTaskSchema]:
        """Получает и сериализует задания типа 3 для варианта"""
        db_tasks = await self.repo.get_third_tasks_by_variant(variant_id)
        return [
            ThirdTaskSchema(
                id=task.id,
                text=task.text,
                correct_letter=task.correct_letter,
                options=[ThirdTaskOptionSchema.model_validate(opt, from_attributes=True) for opt in task.options]
            )
            for task in db_tasks
        ]


async def get_reading_service():
    repository = await get_reading_repository()
    return ReadingService(repository)
