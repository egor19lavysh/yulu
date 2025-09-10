from sqlalchemy import ForeignKey
from sqlalchemy import String
from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


class ReadingHSK4(Base):
    __tablename__ = "hsk4_reading_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_type_tasks: Mapped[list["ReadingFirstTaskHSK4"]] = relationship("ReadingFirstTaskHSK4",
                                                                          back_populates="reading_var")
    second_type_tasks: Mapped[list["ReadingSecondTaskHSK4"]] = relationship("ReadingSecondTaskHSK4",
                                                                            back_populates="reading_var")
    third_type_tasks: Mapped[list["ReadingThirdTaskHSK4"]] = relationship("ReadingThirdTaskHSK4",
                                                                          back_populates="reading_var")


### Важно: в экзамене 2 задания такого типа
class ReadingFirstTaskHSK4(Base):
    __tablename__ = "hsk4_reading_first_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    options: Mapped[list["ReadingFirstTaskOptionHSK4"]] = relationship("ReadingFirstTaskOptionHSK4",
                                                                       back_populates="task")
    sentences: Mapped[list["ReadingFirstTaskSentenceHSK4"]] = relationship("ReadingFirstTaskSentenceHSK4",
                                                                           back_populates="task")

    reading_var_id: Mapped[int] = mapped_column(ForeignKey("hsk4_reading_tasks.id"))
    reading_var: Mapped["ReadingHSK4"] = relationship("ReadingHSK4", back_populates="first_type_tasks")


class ReadingFirstTaskOptionHSK4(Base):
    __tablename__ = "hsk4_reading_first_task_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk4_reading_first_tasks.id"))
    task: Mapped["ReadingFirstTaskHSK4"] = relationship("ReadingFirstTaskHSK4", back_populates="options")


class ReadingFirstTaskSentenceHSK4(Base):
    __tablename__ = "hsk4_reading_first_task_sentences"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk4_reading_first_tasks.id"))
    task: Mapped["ReadingFirstTaskHSK4"] = relationship("ReadingFirstTaskHSK4", back_populates="sentences")


class ReadingSecondTaskHSK4(Base):
    __tablename__ = "hsk4_reading_second_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_sequence: Mapped[str] = mapped_column(String(5))
    options: Mapped[list["ReadingSecondTaskOptionHSK4"]] = relationship("ReadingSecondTaskOptionHSK4",
                                                                        back_populates="task")

    reading_var_id: Mapped[int] = mapped_column(ForeignKey("hsk4_reading_tasks.id"))
    reading_var: Mapped["ReadingHSK4"] = relationship("ReadingHSK4", back_populates="second_type_tasks")


class ReadingSecondTaskOptionHSK4(Base):
    __tablename__ = "hsk4_reading_second_task_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk4_reading_second_tasks.id"))
    task: Mapped["ReadingSecondTaskHSK4"] = relationship("ReadingSecondTaskHSK4", back_populates="options")


class ReadingThirdTaskHSK4(Base):
    __tablename__ = "hsk4_reading_third_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    questions: Mapped[list["ReadingThirdTaskQuestionHSK4"]] = relationship("ReadingThirdTaskQuestionHSK4",
                                                                           back_populates="task")

    reading_var_id: Mapped[int] = mapped_column(ForeignKey("hsk4_reading_tasks.id"))
    reading_var: Mapped["ReadingHSK4"] = relationship("ReadingHSK4", back_populates="third_type_tasks")


class ReadingThirdTaskQuestionHSK4(Base):
    __tablename__ = "hsk4_reading_third_task_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    correct_letter: Mapped[str] = mapped_column(String(1))
    options: Mapped[list["QuestionOptionHSK4"]] = relationship("QuestionOptionHSK4", back_populates="question")


class QuestionOptionHSK4(Base):
    __tablename__ = "hsk4_reading_third_task_question_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    question_id: Mapped[int] = mapped_column(ForeignKey("hsk4_reading_third_task_questions.id"))
    question: Mapped["ReadingThirdTaskQuestionHSK4"] = relationship("ReadingThirdTaskQuestionHSK4",
                                                                    back_populates="options")
