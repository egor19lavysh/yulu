from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, object_session
from database import Base


class SentenceOption(Base):
    """Модель варианта ответа (общая для всех типов заданий)"""
    __tablename__ = "sentence_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))  # A, B, C...
    text: Mapped[str]

    # Связи с разными типами заданий
    task_one_id: Mapped[int | None] = mapped_column(ForeignKey("reading_tasks_type_one.id"))
    task_two_id: Mapped[int | None] = mapped_column(ForeignKey("reading_tasks_type_two.id"))
    task_three_id: Mapped[int | None] = mapped_column(ForeignKey("reading_tasks_type_three.id"))

    # Свойство для удобного доступа к заданию
    @property
    def task(self):
        session = object_session(self)
        if not session:
            return None
        if self.task_one_id:
            return session.get(ReadingTaskTypeOne, self.task_one_id)
        elif self.task_two_id:
            return session.get(ReadingTaskTypeTwo, self.task_two_id)
        elif self.task_three_id:
            return session.get(ReadingTaskTypeThree, self.task_three_id)


class ReadingQuestion(Base):
    """Модель вопроса (общая для заданий 1 и 2 типа)"""
    __tablename__ = "reading_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    correct_letter: Mapped[str] = mapped_column(String(1))

    # Связи с заданиями
    task_one_id: Mapped[int | None] = mapped_column(ForeignKey("reading_tasks_type_one.id"))
    task_two_id: Mapped[int | None] = mapped_column(ForeignKey("reading_tasks_type_two.id"))

    @property
    def task(self):
        session = object_session(self)
        if not session:
            return None
        if self.task_one_id:
            return session.get(ReadingTaskTypeOne, self.task_one_id)
        elif self.task_two_id:
            return session.get(ReadingTaskTypeTwo, self.task_two_id)


# Базовый класс для общих полей заданий
class ReadingTaskBase:
    description: Mapped[str] = mapped_column(default="Соотнесите реплики со следующими вопросами")


class ReadingTaskTypeOne(Base, ReadingTaskBase):
    """Задание типа 1"""
    __tablename__ = "reading_tasks_type_one"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Связи
    options: Mapped[list["SentenceOption"]] = relationship(
        primaryjoin="ReadingTaskTypeOne.id == SentenceOption.task_one_id",
        backref="task_one",
        cascade="all, delete-orphan"
    )

    questions: Mapped[list["ReadingQuestion"]] = relationship(
        primaryjoin="ReadingTaskTypeOne.id == ReadingQuestion.task_one_id",
        backref="question_task_one",
        cascade="all, delete-orphan"
    )


class ReadingTaskTypeTwo(Base, ReadingTaskBase):
    """Задание типа 2"""
    __tablename__ = "reading_tasks_type_two"

    id: Mapped[int] = mapped_column(primary_key=True)

    options: Mapped[list["SentenceOption"]] = relationship(
        primaryjoin="ReadingTaskTypeTwo.id == SentenceOption.task_two_id",
        backref="task_two",
        cascade="all, delete-orphan"
    )

    questions: Mapped[list["ReadingQuestion"]] = relationship(
        primaryjoin="ReadingTaskTypeTwo.id == ReadingQuestion.task_two_id",
        backref="question_task_two",
        cascade="all, delete-orphan"
    )


class ReadingTaskTypeThree(Base):
    """Задание типа 3"""
    __tablename__ = "reading_tasks_type_three"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(default="Выберите верное суждение из реплики:")
    text: Mapped[str]
    question: Mapped[str]
    correct_answer_letter: Mapped[str] = mapped_column(String(1))

    options: Mapped[list["SentenceOption"]] = relationship(
        primaryjoin="ReadingTaskTypeThree.id == SentenceOption.task_three_id",
        backref="task_three",
        cascade="all, delete-orphan"
    )