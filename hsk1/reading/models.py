from sqlalchemy import ForeignKey
from sqlalchemy import String
from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


class ReadingHSK1(Base):
    __tablename__ = "hsk1_reading_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_type_tasks: Mapped[list["ReadingFirstTaskHSK1"]] = relationship("ReadingFirstTaskHSK1",
                                                                          back_populates="reading_var")
    second_type_tasks: Mapped[list["ReadingSecondTaskHSK1"]] = relationship("ReadingSecondTaskHSK1",
                                                                            back_populates="reading_var")
    third_type_tasks: Mapped[list["ReadingThirdTaskHSK1"]] = relationship("ReadingThirdTaskHSK1",
                                                                          back_populates="reading_var")


### Важно: в экзамене 2 задания такого типа
class ReadingFirstTaskHSK1(Base):
    __tablename__ = "hsk1_reading_first_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    options: Mapped[list["ReadingFirstTaskOptionHSK1"]] = relationship("ReadingFirstTaskOptionHSK1",
                                                                       back_populates="task")
    sentences: Mapped[list["ReadingFirstTaskSentenceHSK1"]] = relationship("ReadingFirstTaskSentenceHSK1",
                                                                           back_populates="task")

    reading_var_id: Mapped[int] = mapped_column(ForeignKey("hsk1_reading_tasks.id"))
    reading_var: Mapped["ReadingHSK1"] = relationship("ReadingHSK1", back_populates="first_type_tasks")


class ReadingFirstTaskOptionHSK1(Base):
    __tablename__ = "hsk1_reading_first_task_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk1_reading_first_tasks.id"))
    task: Mapped["ReadingFirstTaskHSK1"] = relationship("ReadingFirstTaskHSK1", back_populates="options")


class ReadingFirstTaskSentenceHSK1(Base):
    __tablename__ = "hsk1_reading_first_task_sentences"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk1_reading_first_tasks.id"))
    task: Mapped["ReadingFirstTaskHSK1"] = relationship("ReadingFirstTaskHSK1", back_populates="sentences")


class ReadingSecondTaskHSK1(Base):
    __tablename__ = "hsk1_reading_second_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_sequence: Mapped[str] = mapped_column(String(5))
    options: Mapped[list["ReadingSecondTaskOptionHSK1"]] = relationship("ReadingSecondTaskOptionHSK1",
                                                                        back_populates="task")

    reading_var_id: Mapped[int] = mapped_column(ForeignKey("hsk1_reading_tasks.id"))
    reading_var: Mapped["ReadingHSK1"] = relationship("ReadingHSK1", back_populates="second_type_tasks")


class ReadingSecondTaskOptionHSK1(Base):
    __tablename__ = "hsk1_reading_second_task_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk1_reading_second_tasks.id"))
    task: Mapped["ReadingSecondTaskHSK1"] = relationship("ReadingSecondTaskHSK1", back_populates="options")


class ReadingThirdTaskHSK1(Base):
    __tablename__ = "hsk1_reading_third_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    questions: Mapped[list["ReadingThirdTaskQuestionHSK1"]] = relationship("ReadingThirdTaskQuestionHSK1",
                                                                           back_populates="task")

    reading_var_id: Mapped[int] = mapped_column(ForeignKey("hsk1_reading_tasks.id"))
    reading_var: Mapped["ReadingHSK1"] = relationship("ReadingHSK1", back_populates="third_type_tasks")


class ReadingThirdTaskQuestionHSK1(Base):
    __tablename__ = "hsk1_reading_third_task_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    correct_letter: Mapped[str] = mapped_column(String(1))
    options: Mapped[list["QuestionOptionHSK1"]] = relationship("QuestionOptionHSK1", back_populates="question")

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk1_reading_third_tasks.id"))
    task: Mapped["ReadingThirdTaskHSK1"] = relationship("ReadingThirdTaskHSK1", back_populates="questions")


class QuestionOptionHSK1(Base):
    __tablename__ = "hsk1_reading_third_task_question_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    question_id: Mapped[int] = mapped_column(ForeignKey("hsk1_reading_third_task_questions.id"))
    question: Mapped["ReadingThirdTaskQuestionHSK1"] = relationship("ReadingThirdTaskQuestionHSK1",
                                                                    back_populates="options")
