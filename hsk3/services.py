from dataclasses import dataclass
from hsk3.repositories import reading_repo, ReadingRepository, writing_repo, WritingRepository
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
                                        sentence_options=[SentenceOption(id=op.id, letter=op.letter, text=op.text) for op in
                                                    task.options],
                                        questions=[ReadingQuestion(id=q.id, text=q.text, correct_letter=q.correct_letter) for
                                             q in task.questions])

    def get_type_two_tasks(self):
        tasks = self.repo.get_type_two_tasks()
        return tasks

    def get_type_two_task(self, task_id: int):
        task = self.repo.get_type_two_task(task_id=task_id)
        if task:
            return ReadingTaskTypeTwoSchema(id=task.id,
                                            description=task.description,
                                            sentence_options=[SentenceOption(id=op.id, letter=op.letter, text=op.text) for op
                                                        in
                                                        task.options],
                                            questions=[ReadingQuestion(id=q.id, text=q.text, correct_letter=q.correct_letter)
                                                 for
                                                 q in task.questions])
        raise Exception("Что-то пошло не так")

    def get_random_type_three_tasks(self):
        tasks = self.repo.get_random_type_three_tasks()
        return tasks

reading_service = ReadingService(repo=reading_repo)


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

writing_service = WritingService(writing_repo)