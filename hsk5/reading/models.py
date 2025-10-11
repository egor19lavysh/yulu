from sqlalchemy import ForeignKey
from sqlalchemy import String
from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


class ReadingHSK5(Base):
    __tablename__ = "hsk5_reading_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_type_tasks: Mapped[list["ReadingFirstTaskHSK5"]] = relationship("ReadingFirstTaskHSK5", back_populates="reading_var")
    second_type_tasks: Mapped[list["ReadingSecondTaskHSK5"]] = relationship("ReadingSecondTaskHSK5", back_populates="reading_var")
    third_type_tasks: Mapped[list["ReadingThirdTaskHSK5"]] = relationship("ReadingThirdTaskHSK5", back_populates="reading_var")


class ReadingFirstTaskHSK5(Base):
    __tablename__ = "hsk5_reading_first_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    questions: Mapped[list["ReadingFirstTaskHSK5Question"]] = relationship("ReadingFirstTaskHSK5Question", back_populates="task")

    reading_var_id: Mapped[int] = mapped_column(ForeignKey("hsk5_reading_tasks.id"))
    reading_var: Mapped["ReadingHSK5"] = relationship("ReadingHSK5", back_populates="first_type_tasks")


class ReadingFirstTaskHSK5Question(Base):
    __tablename__ = "hsk5_reading_first_tasks_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    correct_letter: Mapped[str] = mapped_column(String(1))
    options: Mapped[list["ReadingFirstTaskQuestionOptionHSK5"]] = relationship("ReadingFirstTaskQuestionOptionHSK5", back_populates="question")

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk5_reading_first_tasks.id"))
    task: Mapped["ReadingFirstTaskHSK5"] = relationship("ReadingFirstTaskHSK5", back_populates="questions")


class ReadingFirstTaskQuestionOptionHSK5(Base):
    __tablename__ = "hsk5_reading_first_tasks_question_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    question_id: Mapped[int] = mapped_column(ForeignKey("hsk5_reading_first_tasks_questions.id"))
    question: Mapped["ReadingFirstTaskHSK5Question"] = relationship("ReadingFirstTaskHSK5Question",
                                                                    back_populates="options")


class ReadingSecondTaskHSK5(Base):
    __tablename__ = "hsk5_reading_second_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    correct_letter: Mapped[str] = mapped_column(String(1))
    options: Mapped[list["ReadingSecondTaskHSK5Option"]] = relationship("ReadingSecondTaskHSK5Option", back_populates="task")

    reading_var_id: Mapped[int] = mapped_column(ForeignKey("hsk5_reading_tasks.id"))
    reading_var: Mapped["ReadingHSK5"] = relationship("ReadingHSK5", back_populates="second_type_tasks")


class ReadingSecondTaskHSK5Option(Base):
    __tablename__ = "hsk5_reading_second_tasks_option"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk5_reading_second_tasks.id"))
    task: Mapped["ReadingSecondTaskHSK5"] = relationship("ReadingSecondTaskHSK5", back_populates="options")


class ReadingThirdTaskHSK5(Base):
    __tablename__ = "hsk5_reading_third_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    photo_id: Mapped[str | None]
    text: Mapped[str]
    questions: Mapped[list["ReadingThirdTaskHSK5Question"]] = relationship("ReadingThirdTaskHSK5Question", back_populates="task")

    reading_var_id: Mapped[int] = mapped_column(ForeignKey("hsk5_reading_tasks.id"))
    reading_var: Mapped["ReadingHSK5"] = relationship("ReadingHSK5", back_populates="third_type_tasks")


class ReadingThirdTaskHSK5Question(Base):
    __tablename__ = "hsk5_reading_third_tasks_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    correct_letter: Mapped[str] = mapped_column(String(1))
    options: Mapped[list["ReadingThirdTaskQuestionOptionHSK5"]] = relationship("ReadingThirdTaskQuestionOptionHSK5", back_populates="question")

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk5_reading_third_tasks.id"))
    task: Mapped["ReadingThirdTaskHSK5"] = relationship("ReadingThirdTaskHSK5", back_populates="questions")


class ReadingThirdTaskQuestionOptionHSK5(Base):
    __tablename__ = "hsk5_reading_third_task_question_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    question_id: Mapped[int] = mapped_column(ForeignKey("hsk5_reading_third_task_questions.id"))
    question: Mapped["ReadingThirdTaskHSK5Question"] = relationship("ReadingThirdTaskHSK5Question",
                                                                    back_populates="options")
