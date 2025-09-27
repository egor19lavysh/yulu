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
    fourth_type_tasks: Mapped[list["ReadingFourthTaskHSK1"]] = relationship("ReadingFourthTaskHSK1",
                                                                          back_populates="reading_var")
    
class ReadingFirstTaskHSK1(Base):
    __tablename__ = "hsk1_reading_first_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    picture_id: Mapped[str]
    options: Mapped[list["ReadingFirstTaskHSK1Option"]] = relationship("ReadingFirstTaskHSK1Option", back_populates="task")

    reading_var_id: Mapped[int] = mapped_column(ForeignKey("hsk1_reading_tasks.id"))
    reading_var: Mapped["ReadingHSK1"] = relationship("ReadingHSK1", back_populates="first_type_tasks")

class ReadingFirstTaskHSK1Option(Base):
    __tablename__ = "hsk1_reading_first_tasks_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    is_correct: Mapped[bool]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk1_reading_first_tasks.id"))
    task: Mapped["ReadingFirstTaskHSK1"] = relationship("ReadingFirstTaskHSK1", back_populates="options")


class ReadingSecondTaskHSK1(Base):
    __tablename__ = "hsk1_reading_second_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    picture_id: Mapped[str]
    sentences: Mapped[list["ReadingSecondTaskHSK1Sentence"]] = relationship("ReadingSecondTaskHSK1Sentence", back_populates="task")

    reading_var_id: Mapped[int] = mapped_column(ForeignKey("hsk1_reading_tasks.id"))
    reading_var: Mapped["ReadingHSK1"] = relationship("ReadingHSK1", back_populates="second_type_tasks")

class ReadingSecondTaskHSK1Sentence(Base):
    __tablename__ = "hsk1_reading_second_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    correct_letter: Mapped[str] = mapped_column(String(1))

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk1_reading_second_tasks.id"))
    task: Mapped["ReadingSecondTaskHSK1"] = relationship("ReadingSecondTaskHSK1", back_populates="sentence")


class ReadingThirdTaskHSK1(Base):
    __tablename__ = "hsk1_reading_third_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    sentences: Mapped[list["ReadingThirdTaskHSK1Sentence"]] = relationship("ReadingThirdTaskHSK1Sentence", back_populates="task")
    options: Mapped[list["ReadingThirdTaskHSK1Option"]] = relationship("ReadingThirdTaskHSK1Sentance", back_populates="task")

    reading_var_id: Mapped[int] = mapped_column(ForeignKey("hsk1_reading_tasks.id"))
    reading_var: Mapped["ReadingHSK1"] = relationship("ReadingHSK1", back_populates="third_type_tasks")


class ReadingThirdTaskHSK1Sentence(Base):
    __tablename__ = "hsk1_reading_third_tasks_sentences"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    correct_letter: Mapped[str] = mapped_column(String(1))

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk1_reading_third_tasks.id"))
    task: Mapped["ReadingThirdTaskHSK1"] = relationship("ReadingThirdTaskHSK1", back_populates="sentence")


class ReadingThirdTaskHSK1Option(Base):
    __tablename__ = "hsk1_reading_third_tasks_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk1_reading_third_tasks.id"))
    task: Mapped["ReadingThirdTaskHSK1"] = relationship("ReadingThirdTaskHSK1", back_populates="option")


class ReadingFourthTaskHSK1(Base):
    __tablename__ = "hsk1_reading_fourth_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    options: Mapped[list["ReadingFourthTaskHSK1Option"]] = relationship("ReadingFourthTaskHSK1Option", back_populates="task")
    questions: Mapped[list["ReadingFourthTaskHSK1Question"]] = relationship("ReadingFourthTaskHSK1Question", back_populates="task")

    reading_var_id: Mapped[int] = mapped_column(ForeignKey("hsk1_reading_tasks.id"))
    reading_var: Mapped["ReadingHSK1"] = relationship("ReadingHSK1", back_populates="fourth_type_tasks")


class ReadingFourthTaskHSK1Option(Base):
    __tablename__ = "hsk1_reading_fourth_tasks_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_letter: Mapped[str] = mapped_column(String(1))
    text: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk1_reading_fourth_tasks.id"))
    task: Mapped["ReadingFourthTaskHSK1"] = relationship("ReadingFourthTaskHSK1", back_populates="options")


class ReadingFourthTaskHSK1Question(Base):
    __tablename__ = "hsk1_reading_fourth_tasks_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    correct_letter: Mapped[str] = mapped_column(String(1))

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk1_reading_fourth_tasks.id"))
    task: Mapped["ReadingFourthTaskHSK1"] = relationship("ReadingFourthTaskHSK1", back_populates="questions")