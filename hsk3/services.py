from dataclasses import dataclass
from typing import Optional

from hsk3.repositories import *
from hsk3.schemas import *


@dataclass
class ReadingService:
    repo: ReadingRepository

    def get_type_one_tasks(self):
        tasks = self.repo.get_type_one_tasks()
        return tasks

    def get_type_one_task(self, task_id: int):
        task = self.repo.get_type_one_task(task_id=task_id)

        return ReadingTaskTypeOneSchema(id=task.id,
                                        description=task.description,
                                        sentence_options=[SentenceOption(id=op.id, letter=op.letter, text=op.text) for
                                                          op in
                                                          task.options],
                                        questions=[
                                            ReadingQuestion(id=q.id, text=q.text, correct_letter=q.correct_letter) for
                                            q in task.questions])

    def get_type_two_tasks(self):
        tasks = self.repo.get_type_two_tasks()
        return tasks

    def get_type_two_task(self, task_id: int):
        task = self.repo.get_type_two_task(task_id=task_id)
        if task:
            return ReadingTaskTypeTwoSchema(id=task.id,
                                            description=task.description,
                                            sentence_options=[SentenceOption(id=op.id, letter=op.letter, text=op.text)
                                                              for op
                                                              in
                                                              task.options],
                                            questions=[
                                                ReadingQuestion(id=q.id, text=q.text, correct_letter=q.correct_letter)
                                                for
                                                q in task.questions])
        raise Exception("Что-то пошло не так")

    def get_random_type_three_tasks(self):
        tasks = self.repo.get_random_type_three_tasks()
        return tasks


@dataclass
class WritingService:
    repo: WritingRepository

    def get_type_one_tasks(self) -> list[WritingTaskTypeOneSchema]:
        tasks = self.repo.get_type_one_tasks()
        orm_tasks = [WritingTaskTypeOneSchema.model_validate(task, from_attributes=True) for task in tasks]
        return orm_tasks

    def get_type_two_tasks(self) -> list[WritingTaskTypeTwoSchema]:
        tasks = self.repo.get_type_two_tasks()
        orm_tasks = [WritingTaskTypeTwoSchema.model_validate(task, from_attributes=True) for task in tasks]
        return orm_tasks




@dataclass
class ListeningService:
    repo: ListeningRepository

    # Методы для тестирования (если используются)
    # def get_test_first_task(self): ...
    # def get_test_second_tasks(self): ...
    # def get_test_third_tasks(self): ...

    # Новые методы для единой механики
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
                picture_id=task.picture_id,
                questions=[
                    FirstTaskQuestionSchema.model_validate(q, from_attributes=True)
                    for q in task.questions
                ]
            )
            orm_tasks.append(orm_task)
        return orm_tasks

    def get_first_task_by_variant(self, variant_id: int) -> Optional[FirstTaskSchema]:
        """Получает первое задание первого типа для варианта"""
        task = self.repo.get_first_task_by_variant(variant_id)
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

    def get_second_tasks_by_variant(self, variant_id: int) -> List[SecondTaskSchema]:
        """Получает задания второго типа для варианта"""
        tasks = self.repo.get_second_tasks_by_variant(variant_id)
        if not tasks:
            return []

        return [SecondTaskSchema.model_validate(task, from_attributes=True) for task in tasks]

    def get_third_tasks_by_variant(self, variant_id: int) -> List[ThirdTaskSchema]:
        """Получает задания третьего типа для варианта со всеми связанными данными"""
        tasks = self.repo.get_third_tasks_by_variant(variant_id)
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



reading_service = ReadingService(repo=reading_repo)
writing_service = WritingService(repo=writing_repo)
listening_service = ListeningService(repo=listening_repo)
