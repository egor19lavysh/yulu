from .repository import WritingRepository, repo
from .schemas import *
from .models import Writing
from dataclasses import dataclass


@dataclass
class WritingService:
    repo: WritingRepository

    def get_variants(self) -> list[WritingVariantListSchema]:
        variants = self.repo.get_variants()
        variants_dto = [WritingVariantListSchema(id=var.id) for var in variants]
        return variants_dto

    def get_variant_by_id(self, variant_id: int) -> WritingVariantSchema | None:
        if var := self.repo.get_variant_by_id(variant_id=variant_id):
            var_dto = self._variant_to_dto(var)
            return var_dto
        raise Exception("Что-то пошло не так на уровне репозитория!")

    def _variant_to_dto(self, var: Writing) -> WritingVariantSchema:
        first_tasks = [FirstTaskSchema.model_validate(task, from_attributes=True)
                       for task in var.first_tasks]
        second_tasks = [SecondTaskSchema.model_validate(task, from_attributes=True)
                        for task in var.second_tasks]

        var_dto = WritingVariantSchema(
            id=var.id,
            first_tasks=first_tasks,
            second_tasks=second_tasks
        )

        return var_dto


service = WritingService(repo)
