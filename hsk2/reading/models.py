from sqlalchemy import ForeignKey
from sqlalchemy import String
from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


class ReadingHSK2(Base):
    __tablename__ = "hsk2_reading_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_type_tasks: Mapped[list["ReadingFirstTaskHSK2"]] = relationship("ReadingFirstTaskHSK2",
                                                                          back_populates="reading_var")
    second_type_tasks: Mapped[list["ReadingSecondTaskHSK2"]] = relationship("ReadingSecondTaskHSK2",
                                                                            back_populates="reading_var")
    third_type_tasks: Mapped[list["ReadingThirdTaskHSK2"]] = relationship("ReadingThirdTaskHSK2",
                                                                          back_populates="reading_var")
    fourth_type_tasks: Mapped[list["ReadingFourthTaskHSK2"]] = relationship("ReadingFourthTaskHSK2",
                                                                          back_populates="reading_var")
    
class ReadingFirstTaskHSK2(Base):
    __tablename__ = "hsk2_reading_first_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    picture_id: Mapped[str]
    sentences: Mapped[list["ReadingFirstTaskHSK2Sentence"]] = relationship("ReadingFirstTaskHSK2Sentence", back_populates="task")

    reading_var_id: Mapped[int] = mapped_column(ForeignKey("hsk2_reading_tasks.id"))
    reading_var: Mapped["ReadingHSK2"] = relationship("ReadingHSK2", back_populates="first_type_tasks")

class ReadingFirstTaskHSK2Sentence(Base):
    __tablename__ = "hsk2_reading_first_tasks_sentences"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    correct_letter: Mapped[str] = mapped_column(String(1))

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk2_reading_first_tasks.id"))  # Fixed this line
    task: Mapped["ReadingFirstTaskHSK2"] = relationship("ReadingFirstTaskHSK2", back_populates="sentences")  # Fixed back_populates name


class ReadingSecondTaskHSK2(Base):
    __tablename__ = "hsk2_reading_second_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    options: Mapped[list["ReadingSecondTaskHSK2Option"]] = relationship("ReadingSecondTaskHSK2Option", back_populates="task")
    sentences: Mapped[list["ReadingSecondTaskHSK2Sentence"]] = relationship("ReadingSecondTaskHSK2Sentence", back_populates="task")

    reading_var_id: Mapped[int] = mapped_column(ForeignKey("hsk2_reading_tasks.id"))
    reading_var: Mapped["ReadingHSK2"] = relationship("ReadingHSK2", back_populates="second_type_tasks")


class ReadingSecondTaskHSK2Option(Base):
    __tablename__ = "hsk2_reading_second_tasks_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk2_reading_second_tasks.id"))
    task: Mapped["ReadingSecondTaskHSK2"] = relationship("ReadingSecondTaskHSK2", back_populates="options")


class ReadingSecondTaskHSK2Sentence(Base):
    __tablename__ = "hsk2_reading_second_tasks_sentences"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    correct_letter: Mapped[str] = mapped_column(String(1))

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk2_reading_second_tasks.id"))
    task: Mapped["ReadingSecondTaskHSK2"] = relationship("ReadingSecondTaskHSK2", back_populates="sentences")  # Fixed back_populates name


class ReadingThirdTaskHSK2(Base):
    __tablename__ = "hsk2_reading_third_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_sentence: Mapped[str]
    second_sentence: Mapped[str]
    is_correct: Mapped[bool]

    reading_var_id: Mapped[int] = mapped_column(ForeignKey("hsk2_reading_tasks.id"))
    reading_var: Mapped["ReadingHSK2"] = relationship("ReadingHSK2", back_populates="third_type_tasks")


class ReadingFourthTaskHSK2(Base):
    __tablename__ = "hsk2_reading_fourth_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    options: Mapped[list["ReadingFourthTaskHSK2Option"]] = relationship("ReadingFourthTaskHSK2Option", back_populates="task")
    questions: Mapped[list["ReadingFourthTaskHSK2Question"]] = relationship("ReadingFourthTaskHSK2Question", back_populates="task")

    reading_var_id: Mapped[int] = mapped_column(ForeignKey("hsk2_reading_tasks.id"))
    reading_var: Mapped["ReadingHSK2"] = relationship("ReadingHSK2", back_populates="fourth_type_tasks")  # Fixed back_populates name


class ReadingFourthTaskHSK2Option(Base):
    __tablename__ = "hsk2_reading_fourth_tasks_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk2_reading_fourth_tasks.id"))
    task: Mapped["ReadingFourthTaskHSK2"] = relationship("ReadingFourthTaskHSK2", back_populates="options")


class ReadingFourthTaskHSK2Question(Base):
    __tablename__ = "hsk2_reading_fourth_tasks_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    correct_letter: Mapped[str] = mapped_column(String(1))

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk2_reading_fourth_tasks.id"))
    task: Mapped["ReadingFourthTaskHSK2"] = relationship("ReadingFourthTaskHSK2", back_populates="questions")