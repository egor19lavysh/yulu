from sqlalchemy import ForeignKey
from sqlalchemy import String
from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship


class WritingHSK1(Base):
    __tablename__ = "hsk1_writing_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_type_tasks: Mapped[list["WritingFirstTaskHSK1"]] = relationship("WritingFirstTaskHSK1",
                                                                          back_populates="writing_var")
    # second_type_tasks: Mapped[list["WritingSecondTaskHSK1"]] = relationship("WritingSecondTaskHSK1",
    #                                                                         back_populates="writing_var")


class WritingFirstTaskHSK1(Base):
    __tablename__ = "hsk1_writing_first_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    correct_sentence: Mapped[str]
    words: Mapped[str]

    writing_var_id: Mapped[int] = mapped_column(ForeignKey("hsk1_writing_tasks.id"))
    writing_var: Mapped["WritingHSK1"] = relationship("WritingHSK1", back_populates="first_type_tasks")


class WritingSecondTaskHSK1(Base):
    __tablename__ = "hsk1_writing_second_tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    picture_id: Mapped[str]
    words: Mapped[list["WritingSecondTaskWord"]] = relationship("WritingSecondTaskWord", back_populates="task")

    writing_var_id: Mapped[int] = mapped_column(ForeignKey("hsk1_writing_tasks.id"))


class WritingSecondTaskWord(Base):
    __tablename__ = "hsk1_writing_second_task_words"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    possible_answer: Mapped[str]

    task_id: Mapped[int] = mapped_column(ForeignKey("hsk1_writing_second_tasks.id"))
    task: Mapped["WritingSecondTaskHSK1"] = relationship("WritingSecondTaskHSK1", back_populates="words")
